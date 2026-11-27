#include <switch.h>
#include <switch/crypto/sha256.h>
#include <switch/kernel/svc.h>
#include <switch/services/acc.h>
#include <switch/services/fs.h>
#include <switch/services/pm.h>
#include <switch/services/sm.h>

#include "za_save.hpp"

#include <algorithm>
#include <cstdarg>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <map>
#include <string>
#include <vector>

// Sysmodule runtime setup. Without these, libnx uses the application applet
// type and a large heap, which exhausts Atmosphere's small sysmodule memory
// pool and makes ams_mitm abort with 0xffe.
extern "C" {

#define INNER_HEAP_SIZE 0x400000

u32 __nx_applet_type = AppletType_None;
u32 __nx_fs_num_sessions = 1;

void __libnx_initheap(void) {
    static u8 inner_heap[INNER_HEAP_SIZE];
    extern void *fake_heap_start;
    extern void *fake_heap_end;
    fake_heap_start = inner_heap;
    fake_heap_end = inner_heap + sizeof(inner_heap);
}

void __appInit(void) {
    if (R_FAILED(smInitialize())) diagAbortWithResult(MAKERESULT(Module_Libnx, LibnxError_InitFail_SM));

    Result rc = fsInitialize();
    if (R_FAILED(rc)) diagAbortWithResult(rc);
    rc = pmdmntInitialize();
    if (R_FAILED(rc)) diagAbortWithResult(rc);
    rc = accountInitialize(AccountServiceType_System);
    if (R_FAILED(rc)) diagAbortWithResult(rc);

    smExit();
}

void __appExit(void) {
    accountExit();
    pmdmntExit();
    fsExit();
}

}  // extern "C"

namespace {

constexpr const char *DETECTOR_FILE = "/switch/achievements/detectors.txt";
constexpr const char *ACHIEVEMENT_FILE = "/switch/achievements/achievements.txt";
constexpr const char *PROGRESS_FILE = "/switch/achievements/progress.txt";
constexpr const char *PROGRESS_TMP = "/switch/achievements/progress.tmp";
constexpr const char *LOG_FILE = "/switch/achievements/watcher.log";
constexpr const char *NOTIFY_DIR = "/config/ultrahand/notifications";
constexpr const char *NOTIFY_APP_ID = "nxach";

constexpr const char *DEFAULT_DETECTORS =
    "# NX-Achievements detector rules.\n"
    "# title_id|achievement_id|kind|target|save_path|block_key|dex_list\n"
    "0100F43008C44000|CZA_01|swish_pokedex_caught|230|/main|2D87BE5C|lumio_se_230\n";

FsFileSystem g_sd;
bool g_sdReady = false;

struct Detector {
    u64 titleId = 0;
    std::string id;
    std::string kind;
    int target = 0;
    std::string savePath = "/main";
    u32 blockKey = 0;
    std::string dexList;
};

struct AchievementMeta {
    std::string name;
    std::string description;
    int target = 0;
};

struct DetectorState {
    Detector detector;
    bool ready = false;
    bool warned = false;
    int value = 0;
};

struct ProgressState {
    std::vector<std::string> otherLines;
    std::map<std::string, int> counts;
};

std::vector<std::string> splitFields(const std::string &line) {
    std::vector<std::string> parts;
    std::size_t start = 0;
    while (true) {
        const std::size_t bar = line.find('|', start);
        if (bar == std::string::npos) {
            parts.push_back(line.substr(start));
            break;
        }
        parts.push_back(line.substr(start, bar - start));
        start = bar + 1;
    }
    return parts;
}

std::string trim(const std::string &text) {
    const std::size_t begin = text.find_first_not_of(" \t\r\n");
    if (begin == std::string::npos) return "";
    const std::size_t end = text.find_last_not_of(" \t\r\n");
    return text.substr(begin, end - begin + 1);
}

std::string formatTitleId(u64 titleId) {
    char buffer[32];
    std::snprintf(buffer, sizeof(buffer), "%016llX", static_cast<unsigned long long>(titleId));
    return buffer;
}

u64 parseHex64(const std::string &text) {
    return static_cast<u64>(std::strtoull(text.c_str(), nullptr, 16));
}

u32 parseHex32(const std::string &text) {
    return static_cast<u32>(std::strtoul(text.c_str(), nullptr, 16));
}

void logMessage(const char *message) {
    if (!g_sdReady) return;
    fsFsCreateFile(&g_sd, LOG_FILE, 0, 0);  // ignore "already exists"
    FsFile file;
    if (R_FAILED(fsFsOpenFile(&g_sd, LOG_FILE, FsOpenMode_Append, &file))) return;
    fsFileWrite(&file, 0, message, std::strlen(message), FsWriteOption_Flush);
    fsFileClose(&file);
    fsFsCommit(&g_sd);
}

void logf(const char *format, ...) {
    char buffer[512];
    va_list args;
    va_start(args, format);
    std::vsnprintf(buffer, sizeof(buffer), format, args);
    va_end(args);
    logMessage(buffer);
}

void ensureDirectories() {
    fsFsCreateDirectory(&g_sd, "/config");
    fsFsCreateDirectory(&g_sd, "/config/ultrahand");
    fsFsCreateDirectory(&g_sd, NOTIFY_DIR);
    fsFsCreateDirectory(&g_sd, "/switch");
    fsFsCreateDirectory(&g_sd, "/switch/achievements");
}

bool readSdFile(const char *path, std::vector<u8> &out, std::size_t maxSize) {
    if (!g_sdReady) return false;
    FsFile file;
    if (R_FAILED(fsFsOpenFile(&g_sd, path, FsOpenMode_Read, &file))) return false;

    s64 fileSize = 0;
    if (R_FAILED(fsFileGetSize(&file, &fileSize)) || fileSize < 0 ||
        static_cast<u64>(fileSize) > maxSize) {
        fsFileClose(&file);
        return false;
    }

    out.resize(static_cast<std::size_t>(fileSize));
    u64 bytesRead = 0;
    const Result result = fsFileRead(&file, 0, out.data(), static_cast<u64>(out.size()),
                                     FsReadOption_None, &bytesRead);
    fsFileClose(&file);
    if (R_FAILED(result) || bytesRead != out.size()) return false;
    return true;
}

bool writeSdFile(const char *path, const void *data, std::size_t size) {
    if (!g_sdReady) return false;
    fsFsDeleteFile(&g_sd, path);  // ignore "not found"
    if (R_FAILED(fsFsCreateFile(&g_sd, path, static_cast<s64>(size), 0))) return false;

    FsFile file;
    if (R_FAILED(fsFsOpenFile(&g_sd, path, FsOpenMode_Write, &file))) return false;
    const Result result = fsFileWrite(&file, 0, data, static_cast<u64>(size), FsWriteOption_Flush);
    fsFileClose(&file);
    if (R_FAILED(result)) return false;
    return R_SUCCEEDED(fsFsCommit(&g_sd));
}

std::vector<Detector> loadDetectors() {
    std::vector<u8> raw;
    std::string content;
    if (readSdFile(DETECTOR_FILE, raw, 64 * 1024)) {
        content.assign(reinterpret_cast<const char *>(raw.data()), raw.size());
    } else {
        content = DEFAULT_DETECTORS;
        writeSdFile(DETECTOR_FILE, DEFAULT_DETECTORS, std::strlen(DEFAULT_DETECTORS));
        logMessage("wrote default detectors.txt\n");
    }

    std::vector<Detector> detectors;
    std::size_t start = 0;
    while (start <= content.size()) {
        std::size_t end = content.find('\n', start);
        if (end == std::string::npos) end = content.size();
        std::string line = trim(content.substr(start, end - start));
        if (!line.empty() && line[0] != '#') {
            auto parts = splitFields(line);
            if (parts.size() >= 4) {
                Detector detector;
                detector.titleId = parseHex64(parts[0]);
                detector.id = parts[1];
                detector.kind = parts[2];
                detector.target = std::atoi(parts[3].c_str());
                if (parts.size() > 4) detector.savePath = parts[4];
                if (parts.size() > 5) detector.blockKey = parseHex32(parts[5]);
                if (parts.size() > 6) detector.dexList = parts[6];
                if (detector.titleId != 0 && !detector.id.empty() && detector.target > 0)
                    detectors.push_back(detector);
            }
        }
        if (end == content.size()) break;
        start = end + 1;
    }
    logf("loaded %zu detector rule(s)\n", detectors.size());
    return detectors;
}

class SdLineReader {
public:
    explicit SdLineReader(const char *path) {
        if (R_SUCCEEDED(fsFsOpenFile(&g_sd, path, FsOpenMode_Read, &file_))) valid_ = true;
    }

    ~SdLineReader() {
        if (valid_) fsFileClose(&file_);
    }

    SdLineReader(const SdLineReader &) = delete;
    SdLineReader &operator=(const SdLineReader &) = delete;

    bool next(std::string &line) {
        if (!valid_ || eof_) return false;
        line.clear();
        while (true) {
            const std::size_t newline = buffer_.find('\n');
            if (newline != std::string::npos) {
                line.assign(buffer_, 0, newline);
                buffer_.erase(0, newline + 1);
                return true;
            }

            char chunk[1024];
            u64 bytesRead = 0;
            const Result result = fsFileRead(&file_, offset_, chunk, sizeof(chunk),
                                             FsReadOption_None, &bytesRead);
            if (R_FAILED(result) || bytesRead == 0) {
                eof_ = true;
                if (!buffer_.empty()) {
                    line.swap(buffer_);
                    return true;
                }
                return false;
            }
            offset_ += bytesRead;
            buffer_.append(chunk, static_cast<std::size_t>(bytesRead));
        }
    }

private:
    FsFile file_{};
    bool valid_ = false;
    bool eof_ = false;
    u64 offset_ = 0;
    std::string buffer_;
};

AchievementMeta loadAchievementMeta(u64 titleId, const std::string &achievementId) {
    AchievementMeta meta;
    meta.name = achievementId;
    meta.description = achievementId;

    const std::string wantedTitle = formatTitleId(titleId);
    SdLineReader reader(ACHIEVEMENT_FILE);
    std::string line;
    while (reader.next(line)) {
        line = trim(line);
        if (line.empty() || line[0] == '#') continue;
        auto parts = splitFields(line);
        if (parts.size() >= 4 && parts[1] == achievementId &&
            (parts[0] == wantedTitle || parts[0] == "*")) {
            meta.name = parts[2];
            meta.description = parts[3];
            if (parts.size() >= 5) meta.target = std::atoi(parts[4].c_str());
            return meta;
        }
    }
    return meta;
}

bool hashValid(const std::vector<u8> &save) {
    if (save.size() <= 0x20) return false;
    Sha256Context context;
    sha256ContextCreate(&context);
    sha256ContextUpdate(&context, nxach::za::INTRO_HASH, sizeof(nxach::za::INTRO_HASH));
    sha256ContextUpdate(&context, save.data(), save.size() - 0x20);
    sha256ContextUpdate(&context, nxach::za::OUTRO_HASH, sizeof(nxach::za::OUTRO_HASH));

    u8 digest[0x20];
    sha256ContextGetHash(&context, digest);
    return std::memcmp(digest, save.data() + save.size() - 0x20, sizeof(digest)) == 0;
}

bool readSwishDexCount(FsFileSystem &saveFs, const std::string &savePath, u32 blockKey,
                       const std::string &dexList, int &count) {
    if (dexList != "lumio_se_230") return false;

    FsFile file;
    if (R_FAILED(fsFsOpenFile(&saveFs, savePath.c_str(), FsOpenMode_Read, &file))) return false;

    s64 fileSize = 0;
    if (R_FAILED(fsFileGetSize(&file, &fileSize)) || fileSize < 0 ||
        fileSize > 16 * 1024 * 1024) {
        fsFileClose(&file);
        return false;
    }

    std::vector<u8> raw(static_cast<std::size_t>(fileSize));
    u64 bytesRead = 0;
    const Result readResult = fsFileRead(&file, 0, raw.data(), static_cast<u64>(raw.size()),
                                         FsReadOption_None, &bytesRead);
    fsFileClose(&file);
    if (R_FAILED(readResult) || bytesRead != raw.size() || !hashValid(raw)) return false;

    raw.resize(raw.size() - 0x20);
    nxach::za::cryptStaticXorpad(raw);

    nxach::za::BlockView block;
    if (!nxach::za::parseBlocks(raw, blockKey, block)) return false;
    const int detected = nxach::za::countLumiosePokedex(block);
    if (detected < 0) return false;
    count = detected;
    return true;
}

int evaluateDetector(const AccountUid &uid, const Detector &detector) {
    FsSaveDataAttribute attr{};
    attr.application_id = detector.titleId;
    attr.uid = uid;
    attr.system_save_data_id = 0;
    attr.save_data_type = FsSaveDataType_Account;
    attr.save_data_rank = FsSaveDataRank_Primary;
    attr.save_data_index = 0;

    FsFileSystem saveFs;
    if (R_FAILED(fsOpenReadOnlySaveDataFileSystem(&saveFs, FsSaveDataSpaceId_User, &attr)))
        return -1;

    int count = -1;
    if (detector.kind == "swish_pokedex_caught") {
        readSwishDexCount(saveFs, detector.savePath, detector.blockKey, detector.dexList, count);
    }
    fsFsClose(&saveFs);
    return count;
}

int readDetector(const Detector &detector) {
    AccountUid lastUser{};
    std::vector<AccountUid> candidates;
    if (R_SUCCEEDED(accountGetLastOpenedUser(&lastUser))) candidates.push_back(lastUser);

    AccountUid users[16] = {};
    s32 total = 0;
    if (R_SUCCEEDED(accountListAllUsers(users, 16, &total))) {
        for (s32 i = 0; i < total && i < 16; ++i) {
            bool duplicate = false;
            for (const AccountUid &uid : candidates) {
                if (std::memcmp(&uid, &users[i], sizeof(uid)) == 0) duplicate = true;
            }
            if (!duplicate) candidates.push_back(users[i]);
        }
    }

    for (const AccountUid &uid : candidates) {
        const int count = evaluateDetector(uid, detector);
        if (count >= 0) return count;
    }
    return -1;
}

u64 currentTitleId() {
    u64 pid = 0;
    u64 titleId = 0;
    if (R_FAILED(pmdmntGetApplicationProcessId(&pid))) return 0;
    if (R_FAILED(pmdmntGetProgramId(&titleId, pid))) return 0;
    return titleId;
}

ProgressState loadProgress() {
    ProgressState state;
    std::vector<u8> raw;
    if (!readSdFile(PROGRESS_FILE, raw, 1024 * 1024)) return state;

    const std::string content(reinterpret_cast<const char *>(raw.data()), raw.size());
    std::size_t start = 0;
    while (start <= content.size()) {
        std::size_t end = content.find('\n', start);
        if (end == std::string::npos) end = content.size();
        std::string line = content.substr(start, end - start);
        while (!line.empty() && line.back() == '\r') line.pop_back();

        const std::size_t bar = line.find('|');
        if (bar != std::string::npos) {
            const int value = std::atoi(line.substr(bar + 1).c_str());
            if (value > 0) state.counts[line.substr(0, bar)] = value;
        } else if (!line.empty()) {
            state.otherLines.push_back(line);
        }
        if (end == content.size()) break;
        start = end + 1;
    }
    return state;
}

void storeProgress(const ProgressState &state) {
    std::string output;
    for (const std::string &line : state.otherLines) {
        output += line;
        output += '\n';
    }
    for (const auto &entry : state.counts) {
        if (entry.second <= 0) continue;
        output += entry.first;
        output += '|';
        output += std::to_string(entry.second);
        output += '\n';
    }
    writeSdFile(PROGRESS_TMP, output.data(), output.size());
    fsFsDeleteFile(&g_sd, PROGRESS_FILE);
    fsFsRenameFile(&g_sd, PROGRESS_TMP, PROGRESS_FILE);
    fsFsCommit(&g_sd);
}

void sendIncrement(u64 titleId, const Detector &detector, int previous, int current) {
    const AchievementMeta meta = loadAchievementMeta(titleId, detector.id);
    const int target = meta.target > 0 ? meta.target : detector.target;
    const int oldValue = std::min(previous, target);
    const int newValue = std::min(current, target);

    char notificationText[512];
    std::snprintf(notificationText, sizeof(notificationText),
                  "★ %s - %s  %d/%d  +1  ->  %d/%d",
                  meta.name.c_str(), meta.description.c_str(), oldValue, target, newValue, target);

    char json[1024];
    std::snprintf(json, sizeof(json),
                  "{\n"
                  "    \"text\": \"%s\",\n"
                  "    \"font_size\": 22,\n"
                  "    \"split_type\": \"word\",\n"
                  "    \"alignment\": \"left\",\n"
                  "    \"duration\": 5000,\n"
                  "    \"title\": \"NX-Achievements\",\n"
                  "    \"show_time\": \"false\",\n"
                  "    \"priority\": 20\n"
                  "}\n",
                  notificationText);

    char path[160];
    std::snprintf(path, sizeof(path), "%s/%s-%016llX-%llu.notify", NOTIFY_DIR, NOTIFY_APP_ID,
                  static_cast<unsigned long long>(titleId),
                  static_cast<unsigned long long>(svcGetSystemTick()));
    writeSdFile(path, json, std::strlen(json));
    logf("notify %s %s %d/%d -> %d/%d\n", formatTitleId(titleId).c_str(), detector.id.c_str(),
         oldValue, target, newValue, target);
}

std::vector<DetectorState> statesForTitle(const std::vector<Detector> &detectors, u64 titleId) {
    std::vector<DetectorState> states;
    for (const Detector &detector : detectors) {
        if (detector.titleId == titleId) states.push_back({detector, false, false, 0});
    }
    return states;
}

}  // namespace

int main() {
    if (R_SUCCEEDED(fsOpenSdCardFileSystem(&g_sd))) {
        g_sdReady = true;
        ensureDirectories();
    }

    logMessage("NX-Achievements watcher v0.2.0 started\n");
    const std::vector<Detector> detectors = loadDetectors();

    u64 activeTitleId = 0;
    std::vector<DetectorState> states;

    while (true) {
        const u64 titleId = currentTitleId();
        if (titleId != activeTitleId) {
            activeTitleId = titleId;
            states = statesForTitle(detectors, titleId);
            if (titleId != 0)
                logf("title %s: %zu detector rule(s)\n", formatTitleId(titleId).c_str(),
                     states.size());
        }

        if (titleId == 0 || states.empty()) {
            svcSleepThread(2 * 1000 * 1000 * 1000ULL);
            continue;
        }

        ProgressState progress = loadProgress();
        bool progressChanged = false;

        for (DetectorState &state : states) {
            const int detected = readDetector(state.detector);
            if (detected < 0) {
                if (!state.warned) {
                    logf("detector %s unavailable\n", state.detector.id.c_str());
                    state.warned = true;
                }
                continue;
            }
            state.warned = false;

            const int stored = progress.counts.count(state.detector.id)
                                   ? progress.counts[state.detector.id]
                                   : 0;

            if (!state.ready) {
                state.value = std::max(stored, detected);
                if (state.value != stored) {
                    progress.counts[state.detector.id] = state.value;
                    progressChanged = true;
                }
                logf("baseline %s=%d/%d (save=%d stored=%d)\n", state.detector.id.c_str(),
                     state.value, state.detector.target, detected, stored);
                state.ready = true;
                continue;
            }

            if (detected > state.value) {
                const int current = std::min(detected, state.detector.target);
                for (int value = state.value + 1; value <= current; ++value)
                    sendIncrement(titleId, state.detector, value - 1, value);
                if (current > stored) {
                    progress.counts[state.detector.id] = current;
                    progressChanged = true;
                }
                state.value = current;
            }
        }

        if (progressChanged) storeProgress(progress);
        svcSleepThread(5 * 1000 * 1000 * 1000ULL);
    }
}
