#include <switch.h>
#include <switch/crypto/sha256.h>
#include <switch/kernel/svc.h>
#include <switch/services/acc.h>
#include <switch/services/fs.h>
#include <switch/services/pm.h>

#include "za_save.hpp"

#include <algorithm>
#include <cstdarg>
#include <cstdio>
#include <cstring>
#include <string>
#include <vector>

namespace {

constexpr u64 ZA_TITLE_ID = 0x0100F43008C44000ULL;
constexpr const char *ACH_ID = "CZA_01";
constexpr const char *ACH_NAME = "Lumiose Pokedex";
constexpr const char *ACH_DESCRIPTION = "Register all 230 unique Pokemon";
constexpr int ACH_TARGET = 230;
constexpr const char *NOTIFY_APP_ID = "nxach";
constexpr const char *NOTIFY_DIR = "/config/ultrahand/notifications";
constexpr const char *PROGRESS_DIR = "/switch/achievements";
constexpr const char *PROGRESS_FILE = "/switch/achievements/progress.txt";
constexpr const char *PROGRESS_TMP = "/switch/achievements/progress.tmp";
constexpr const char *LOG_FILE = "/switch/achievements/watcher.log";

FsFileSystem g_sd;
bool g_sdReady = false;

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
    fsFsCreateDirectory(&g_sd, PROGRESS_DIR);
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

bool readDexCountFromFile(FsFileSystem &saveFs, int &count) {
    FsFile file;
    if (R_FAILED(fsFsOpenFile(&saveFs, "/main", FsOpenMode_Read, &file))) return false;

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

    nxach::za::BlockView dex;
    if (!nxach::za::parseBlocks(raw, nxach::za::KPOKEDEX, dex)) return false;
    const int detected = nxach::za::countLumiosePokedex(dex);
    if (detected < 0) return false;
    count = std::min(detected, ACH_TARGET);
    return true;
}

int readDexCount() {
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
        FsSaveDataAttribute attr{};
        attr.application_id = ZA_TITLE_ID;
        attr.uid = uid;
        attr.system_save_data_id = 0;
        attr.save_data_type = FsSaveDataType_Account;
        attr.save_data_rank = FsSaveDataRank_Primary;
        attr.save_data_index = 0;

        FsFileSystem saveFs;
        if (R_FAILED(fsOpenReadOnlySaveDataFileSystem(&saveFs, FsSaveDataSpaceId_User, &attr)))
            continue;

        int count = 0;
        const bool ok = readDexCountFromFile(saveFs, count);
        fsFsClose(&saveFs);
        if (ok) return count;
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

struct ProgressState {
    std::vector<std::string> lines;
    int count = 0;
};

ProgressState loadProgress() {
    ProgressState state;
    std::vector<u8> raw;
    if (!readSdFile(PROGRESS_FILE, raw, 1024 * 1024)) return state;

    std::string content(reinterpret_cast<const char *>(raw.data()), raw.size());
    std::size_t start = 0;
    while (start <= content.size()) {
        std::size_t end = content.find('\n', start);
        if (end == std::string::npos) end = content.size();
        std::string line = content.substr(start, end - start);
        while (!line.empty() && line.back() == '\r') line.pop_back();

        const std::size_t bar = line.find('|');
        if (bar != std::string::npos && line.substr(0, bar) == ACH_ID) {
            state.count = std::max(0, std::atoi(line.substr(bar + 1).c_str()));
        } else if (!line.empty()) {
            state.lines.push_back(line);
        }
        if (end == content.size()) break;
        start = end + 1;
    }
    return state;
}

void storeProgress(const ProgressState &state, int value) {
    std::string output;
    for (const std::string &line : state.lines) {
        output += line;
        output += '\n';
    }
    if (value > 0) {
        output += ACH_ID;
        output += '|';
        output += std::to_string(value);
        output += '\n';
    }
    writeSdFile(PROGRESS_TMP, output.data(), output.size());
    fsFsDeleteFile(&g_sd, PROGRESS_FILE);
    fsFsRenameFile(&g_sd, PROGRESS_TMP, PROGRESS_FILE);
    fsFsCommit(&g_sd);
}

void sendIncrement(int previous, int current) {
    char notificationText[512];
    std::snprintf(notificationText, sizeof(notificationText),
                  "★ %s - %s  %d/%d  +1  ->  %d/%d",
                  ACH_NAME, ACH_DESCRIPTION, previous, ACH_TARGET, current, ACH_TARGET);

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
    std::snprintf(path, sizeof(path), "%s/%s-%016llX.notify", NOTIFY_DIR, NOTIFY_APP_ID,
                  static_cast<unsigned long long>(svcGetSystemTick()));
    writeSdFile(path, json, std::strlen(json));
    logf("notify %s %d/%d -> %d/%d\n", ACH_ID, previous, ACH_TARGET, current, ACH_TARGET);
}

}  // namespace

int main() {
    fsInitialize();
    pmdmntInitialize();
    accountInitialize(AccountServiceType_System);

    if (R_SUCCEEDED(fsOpenSdCardFileSystem(&g_sd))) {
        g_sdReady = true;
        ensureDirectories();
    }

    logMessage("NX-Achievements watcher v0.1.0 started\n");

    bool wasActive = false;
    bool baselineReady = false;
    int baselineCount = 0;

    while (true) {
        if (currentTitleId() != ZA_TITLE_ID) {
            if (wasActive) logMessage("Z-A closed; waiting for next launch\n");
            wasActive = false;
            baselineReady = false;
            svcSleepThread(2 * 1000 * 1000 * 1000ULL);
            continue;
        }

        if (!wasActive) {
            wasActive = true;
            baselineReady = false;
            logMessage("Z-A running; reading save baseline\n");
        }

        const int detected = readDexCount();
        if (detected >= 0) {
            ProgressState progress = loadProgress();
            const int stored = progress.count;

            if (!baselineReady) {
                baselineCount = std::max(stored, detected);
                if (baselineCount != stored) storeProgress(progress, baselineCount);
                logf("baseline %s=%d/%d (save=%d stored=%d)\n", ACH_ID, baselineCount,
                     ACH_TARGET, detected, stored);
                baselineReady = true;
            } else if (detected > baselineCount) {
                const int current = std::min(detected, ACH_TARGET);
                for (int value = baselineCount + 1; value <= current; ++value)
                    sendIncrement(value - 1, value);
                if (current > stored) storeProgress(progress, current);
                baselineCount = current;
            }
        }

        svcSleepThread(5 * 1000 * 1000 * 1000ULL);
    }
}
