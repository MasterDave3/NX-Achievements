#include <switch.h>
#include <switch/crypto/sha256.h>
#include <switch/kernel/svc.h>
#include <switch/services/acc.h>
#include <switch/services/fs.h>
#include <switch/runtime/devices/fs_dev.h>
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

#define INNER_HEAP_SIZE 0x80000

u32 __nx_applet_type = AppletType_None;
u32 __nx_fs_num_sessions = 4;

// Independent boot marker: uses fsdev/std::FILE instead of the raw FS handle
// used by the watcher, so we can tell "module started" from "SD FS failed".
bool g_bootMarkerMounted = false;

void writeBootMarker(const char *line) {
    if (!g_bootMarkerMounted) {
        if (R_FAILED(fsdevMountSdmc())) return;
        g_bootMarkerMounted = true;
    }
    FILE *file = std::fopen("/sdmc:/switch/achievements/watcher.boot", "a");
    if (file == nullptr) return;
    std::fprintf(file, "%s", line);
    std::fclose(file);
}

void __libnx_initheap(void) {
    static u8 inner_heap[INNER_HEAP_SIZE];
    extern void *fake_heap_start;
    extern void *fake_heap_end;
    fake_heap_start = inner_heap;
    fake_heap_end = inner_heap + sizeof(inner_heap);
}

void __appInit(void) {
    writeBootMarker("__appInit\n");
    // Keep boot-time initialization minimal. pmdmnt/account are intentionally
    // NOT opened here: connecting to them as a boot2 sysmodule raced system
    // services and made dmnt abort with 0xffe. Account is initialized lazily
    // from main() after the boot sequence has settled.
    if (R_FAILED(smInitialize())) diagAbortWithResult(MAKERESULT(Module_Libnx, LibnxError_InitFail_SM));

    Result rc = fsInitialize();
    if (R_FAILED(rc)) diagAbortWithResult(rc);

    smExit();
}

void __appExit(void) {
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

bool g_accountReady = false;
bool g_accountTried = false;

// Account is opened only after boot has settled, never from __appInit.
void ensureAccount() {
    if (g_accountReady || g_accountTried) return;
    g_accountTried = true;
    if (R_FAILED(accountInitialize(AccountServiceType_System))) return;
    g_accountReady = true;
}

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

constexpr std::size_t SAVE_CACHE_SIZE = 4096;
constexpr std::size_t XOR_STEP = 0x7f;

bool hashValid(FsFile &file, s64 fileSize) {
    if (fileSize <= 0x20) return false;

    Sha256Context context;
    sha256ContextCreate(&context);
    sha256ContextUpdate(&context, nxach::za::INTRO_HASH, sizeof(nxach::za::INTRO_HASH));

    u8 buffer[4096];
    s64 remaining = fileSize - 0x20;
    s64 offset = 0;
    while (remaining > 0) {
        const u64 chunk = std::min<u64>(sizeof(buffer), static_cast<u64>(remaining));
        u64 bytesRead = 0;
        if (R_FAILED(fsFileRead(&file, offset, buffer, chunk, FsReadOption_None, &bytesRead)) ||
            bytesRead == 0)
            return false;
        sha256ContextUpdate(&context, buffer, static_cast<std::size_t>(bytesRead));
        offset += bytesRead;
        remaining -= bytesRead;
    }
    sha256ContextUpdate(&context, nxach::za::OUTRO_HASH, sizeof(nxach::za::OUTRO_HASH));

    u8 digest[0x20];
    sha256ContextGetHash(&context, digest);
    u8 stored[0x20];
    u64 bytesRead = 0;
    if (R_FAILED(fsFileRead(&file, fileSize - 0x20, stored, sizeof(stored), FsReadOption_None,
                            &bytesRead)) ||
        bytesRead != sizeof(stored))
        return false;
    return std::memcmp(digest, stored, sizeof(digest)) == 0;
}

// Decrypts SwishCrypto's static XOR pad on demand, so the ~3 MiB save does not
// need to be held in the sysmodule's small heap.
class DecryptedSaveReader {
public:
    DecryptedSaveReader(FsFile &file, std::size_t size) : file_(file), size_(size) {}

    std::size_t size() const { return size_; }

    u8 get(std::size_t offset) {
        if (offset >= size_) return 0;
        if (offset < cacheBase_ || offset >= cacheBase_ + cacheLen_) load(offset);
        if (offset >= cacheBase_ + cacheLen_) return 0;
        return cache_[offset - cacheBase_];
    }

    u32 getU32(std::size_t offset) {
        return static_cast<u32>(get(offset)) |
               (static_cast<u32>(get(offset + 1)) << 8) |
               (static_cast<u32>(get(offset + 2)) << 16) |
               (static_cast<u32>(get(offset + 3)) << 24);
    }

private:
    void load(std::size_t offset) {
        cacheBase_ = (offset / XOR_STEP) * XOR_STEP;
        cacheLen_ = 0;
        if (cacheBase_ >= size_) return;

        const u64 wanted = static_cast<u64>(
            std::min<std::size_t>(sizeof(cache_), size_ - cacheBase_));
        u64 bytesRead = 0;
        if (R_FAILED(fsFileRead(&file_, cacheBase_, cache_, wanted, FsReadOption_None,
                                &bytesRead)))
            return;
        cacheLen_ = static_cast<std::size_t>(bytesRead);

        for (std::size_t i = 0; i < cacheLen_; ++i) {
            const std::size_t position = cacheBase_ + i;
            const std::size_t modulus = position % XOR_STEP;
            u8 pad = nxach::za::STATIC_XORPAD[modulus];
            if (modulus == 0 && position != 0) pad ^= nxach::za::STATIC_XORPAD[0x7f];
            cache_[i] ^= pad;
        }
    }

    FsFile &file_;
    std::size_t size_;
    std::size_t cacheBase_ = static_cast<std::size_t>(-1);
    std::size_t cacheLen_ = 0;
    u8 cache_[SAVE_CACHE_SIZE]{};
};

bool countLumioseDexStream(DecryptedSaveReader &reader, u32 wantedKey, int &count) {
    count = -1;
    std::size_t offset = 0;
    while (offset + 5 <= reader.size()) {
        const u32 key = reader.getU32(offset);
        offset += 4;
        nxach::za::SCXorShift32 rng(key);
        const u8 type = static_cast<u8>(reader.get(offset) ^ rng.next());
        ++offset;
        if (type == 1 || type == 2) continue;  // boolean blocks have no payload

        s32 length = 0;
        if (type == 4) {
            if (offset + 4 > reader.size()) return false;
            length = static_cast<s32>(reader.getU32(offset) ^ rng.next32());
            offset += 4;
        } else if (type == 5) {
            if (offset + 5 > reader.size()) return false;
            const s32 entries = static_cast<s32>(reader.getU32(offset) ^ rng.next32());
            offset += 4;
            const u8 subtype = static_cast<u8>(reader.get(offset) ^ rng.next());
            ++offset;
            const s32 subSize = nxach::za::typeSize(subtype);
            if (entries < 0 || subSize <= 0) return false;
            if (static_cast<std::size_t>(entries) >
                reader.size() / static_cast<std::size_t>(subSize))
                return false;
            length = entries * subSize;
        } else {
            length = nxach::za::typeSize(type);
            if (length < 0) return false;
        }
        if (length < 0 || static_cast<std::size_t>(length) > reader.size() - offset)
            return false;

        const bool wanted = key == wantedKey;
        if (wanted && type != 4) return false;

        const std::size_t payload = static_cast<std::size_t>(length);
        std::size_t dexPos = 0;
        std::size_t nextTarget = wanted
                                     ? static_cast<std::size_t>(
                                           nxach::za::LUMIOSE_DEX_INTERNAL[0]) *
                                           nxach::za::POKEDEX_ENTRY_SIZE
                                     : 0;
        int detected = 0;

        for (std::size_t i = 0; i < payload; ++i) {
            if (wanted && i == nextTarget) {
                if (i + 4 > payload) return false;
                u32 flag = 0;
                for (std::size_t j = 0; j < 4; ++j)
                    flag |= static_cast<u32>(reader.get(offset + i + j) ^ rng.next())
                            << (8 * j);
                if (flag != 0) ++detected;
                i += 3;
                ++dexPos;
                if (dexPos < 230)
                    nextTarget = static_cast<std::size_t>(
                                     nxach::za::LUMIOSE_DEX_INTERNAL[dexPos]) *
                                 nxach::za::POKEDEX_ENTRY_SIZE;
                continue;
            }
            (void)(reader.get(offset + i) ^ rng.next());
        }
        if (wanted) {
            if (dexPos != 230) return false;
            count = detected;
        }
        offset += payload;
    }
    return offset == reader.size();
}

bool readSwishDexCount(FsFileSystem &saveFs, const std::string &savePath, u32 blockKey,
                       const std::string &dexList, int &count) {
    if (dexList != "lumio_se_230") return false;

    FsFile file;
    if (R_FAILED(fsFsOpenFile(&saveFs, savePath.c_str(), FsOpenMode_Read, &file))) return false;

    s64 fileSize = 0;
    if (R_FAILED(fsFileGetSize(&file, &fileSize)) || fileSize <= 0x20 ||
        fileSize > 16 * 1024 * 1024) {
        fsFileClose(&file);
        return false;
    }

    if (!hashValid(file, fileSize)) {
        fsFileClose(&file);
        return false;
    }

    DecryptedSaveReader reader(file, static_cast<std::size_t>(fileSize - 0x20));
    int detected = -1;
    const bool parsed = countLumioseDexStream(reader, blockKey, detected);
    fsFileClose(&file);
    if (!parsed || detected < 0) return false;
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
    ensureAccount();
    if (!g_accountReady) return -1;

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

std::vector<DetectorState> statesFrom(const std::vector<Detector> &detectors) {
    std::vector<DetectorState> states;
    for (const Detector &detector : detectors)
        states.push_back({detector, false, false, 0});
    return states;
}

}  // namespace

int main() {
    writeBootMarker("main\n");
    const Result sdResult = fsOpenSdCardFileSystem(&g_sd);
    char marker[128];
    std::snprintf(marker, sizeof(marker), "fsOpenSdCardFileSystem=0x%08x\n",
                  static_cast<unsigned>(sdResult));
    writeBootMarker(marker);
    if (R_SUCCEEDED(sdResult)) {
        g_sdReady = true;
        ensureDirectories();
    }

    logMessage("NX-Achievements watcher v0.3.1 started\n");
    const std::vector<Detector> detectors = loadDetectors();
    std::vector<DetectorState> states = statesFrom(detectors);
    logf("loaded %zu detector rule(s)\n", states.size());

    // Give boot2/Atmosphère time to finish before opening account services.
    svcSleepThread(10ULL * 1000 * 1000 * 1000ULL);

    while (true) {
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
                    sendIncrement(state.detector.titleId, state.detector, value - 1, value);
                if (current > stored) {
                    progress.counts[state.detector.id] = current;
                    progressChanged = true;
                }
                state.value = current;
            }
        }

        if (progressChanged) storeProgress(progress);
        svcSleepThread(5ULL * 1000 * 1000 * 1000ULL);
    }
}
