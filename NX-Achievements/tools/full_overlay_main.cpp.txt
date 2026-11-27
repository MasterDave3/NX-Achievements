#define TESLA_INIT_IMPL
#include <tesla.hpp>
#include <switch/services/ns.h>

#include <algorithm>
#include <cstdio>
#include <cstdlib>
#include <fstream>
#include <memory>
#include <sstream>
#include <string>
#include <unordered_map>
#include <unordered_set>
#include <vector>
#include <sys/stat.h>

namespace {

constexpr const char *VERSION      = "v0.6.0";
constexpr const char *CONFIG_DIR   = "sdmc:/switch/achievements";
constexpr const char *CONFIG_FILE  = "sdmc:/switch/achievements/achievements.txt";
constexpr const char *PROGRESS_FILE = "sdmc:/switch/achievements/progress.txt";

struct Achievement {
    std::string titleId;
    std::string id;
    std::string name;
    std::string description;
    int target = 0;  // 0 = normal toggle; >0 = countable goal
};

struct Progress {
    std::unordered_set<std::string> unlocked;
    std::unordered_map<std::string, int> counts;

    int count(const std::string &id) const {
        auto it = counts.find(id);
        return it == counts.end() ? 0 : it->second;
    }
};

struct InstalledTitle {
    u64 titleId = 0;
    std::string name;
};

struct DetectedGame {
    u64 titleId = 0;
    std::string name;
    int achievements = 0;
};

std::vector<InstalledTitle> g_installedTitles;
bool g_installedLoaded = false;

std::string trim(const std::string &s) {
    const auto begin = s.find_first_not_of(" \t\r\n");
    if (begin == std::string::npos) return "";
    const auto end = s.find_last_not_of(" \t\r\n");
    return s.substr(begin, end - begin + 1);
}

std::vector<std::string> split(const std::string &s, char delim) {
    std::vector<std::string> out;
    std::stringstream ss(s);
    std::string part;
    while (std::getline(ss, part, delim))
        out.push_back(trim(part));
    return out;
}

std::string formatTitleId(u64 titleId) {
    char buffer[32];
    std::snprintf(buffer, sizeof(buffer), "%016llX", static_cast<unsigned long long>(titleId));
    return std::string(buffer);
}

size_t boundedStrLen(const char *s, size_t max) {
    size_t len = 0;
    while (len < max && s[len] != '\0') ++len;
    return len;
}

u64 currentTitleId() {
    u64 pid = 0;
    u64 titleId = 0;
    if (R_FAILED(pmdmntGetApplicationProcessId(&pid))) return 0;
    if (R_FAILED(pmdmntGetProgramId(&titleId, pid))) return 0;
    return titleId;
}

void ensureConfigDir() {
    mkdir("sdmc:/switch", 0777);
    mkdir(CONFIG_DIR, 0777);
}

std::vector<Achievement> loadAchievements() {
    ensureConfigDir();
    std::ifstream file(CONFIG_FILE);
    std::vector<Achievement> out;
    if (!file.is_open()) return out;

    std::string line;
    while (std::getline(file, line)) {
        line = trim(line);
        if (line.empty() || line[0] == '#') continue;
        auto parts = split(line, '|');
        if (parts.size() < 4) continue;
        int target = 0;
        if (parts.size() >= 5)
            target = std::max(0, std::atoi(parts[4].c_str()));
        out.push_back({parts[0], parts[1], parts[2], parts[3], target});
    }
    return out;
}

Progress loadProgress() {
    ensureConfigDir();
    Progress progress;
    std::ifstream file(PROGRESS_FILE);
    if (!file.is_open()) return progress;

    std::string line;
    while (std::getline(file, line)) {
        line = trim(line);
        if (line.empty() || line[0] == '#') continue;
        auto parts = split(line, '|');
        if (parts.empty()) continue;
        if (parts.size() >= 2) {
            int value = std::atoi(parts[1].c_str());
            if (value > 0) progress.counts[parts[0]] = value;
        } else {
            progress.unlocked.insert(parts[0]);
        }
    }
    return progress;
}

void saveProgress(const Progress &progress) {
    ensureConfigDir();
    std::ofstream file(PROGRESS_FILE, std::ios::trunc);
    for (const auto &entry : progress.counts) {
        if (entry.second > 0)
            file << entry.first << '|' << entry.second << '\n';
    }
    for (const auto &id : progress.unlocked) {
        if (progress.counts.count(id) == 0)
            file << id << '\n';
    }
}

bool matchesGame(const Achievement &achievement, u64 titleId) {
    if (achievement.titleId == "*") return true;
    if (achievement.titleId.empty()) return true;
    return achievement.titleId == formatTitleId(titleId);
}

std::vector<u64> enumeratedTitleIds() {
    std::vector<u64> ids;

    // Application records cover installed titles on both NAND and the SD card.
    std::vector<NsApplicationRecord> records(512);
    s32 written = 0;
    s32 total = 0;
    if (R_SUCCEEDED(nsListApplicationRecord(records.data(), static_cast<s32>(records.size()), 0, &written))) {
        for (s32 i = 0; i < written && i < static_cast<s32>(records.size()); ++i)
            ids.push_back(records[i].application_id);

        if (total > written) {
            records.resize(total);
            written = 0;
            if (R_SUCCEEDED(nsListApplicationRecord(records.data(), total, 0, &written))) {
                ids.clear();
                for (s32 i = 0; i < written && i < total; ++i)
                    ids.push_back(records[i].application_id);
            }
        }
    }

    // Include a game card if one is inserted, even if it has no record yet.
    u64 cardIds[16] = {};
    s32 cardTotal = 0;
    if (R_SUCCEEDED(nsListApplicationIdOnGameCard(cardIds, 16, &cardTotal))) {
        for (s32 i = 0; i < cardTotal && i < 16; ++i)
            ids.push_back(cardIds[i]);
    }

    std::sort(ids.begin(), ids.end());
    ids.erase(std::unique(ids.begin(), ids.end()), ids.end());
    return ids;
}

std::string applicationName(u64 titleId, NsApplicationControlData *control) {
    u64 actualSize = 0;
    if (R_SUCCEEDED(nsGetApplicationControlData(NsApplicationControlSource_Storage,
                                                titleId, control, sizeof(*control), &actualSize))) {
        NacpLanguageEntry *entry = nullptr;
        if (R_SUCCEEDED(nacpGetLanguageEntry(&control->nacp, &entry)) && entry != nullptr) {
            const size_t len = boundedStrLen(entry->name, sizeof(entry->name));
            if (len > 0) return std::string(entry->name, len);
        }
    }
    return formatTitleId(titleId);
}

void ensureInstalledTitles() {
    if (g_installedLoaded) return;
    g_installedLoaded = true;

    auto control = std::make_unique<NsApplicationControlData>();
    for (u64 titleId : enumeratedTitleIds()) {
        if (titleId == 0) continue;
        g_installedTitles.push_back({titleId, applicationName(titleId, control.get())});
    }

    std::sort(g_installedTitles.begin(), g_installedTitles.end(),
              [](const InstalledTitle &a, const InstalledTitle &b) { return a.name < b.name; });
}

std::string installedTitleName(u64 titleId) {
    auto it = std::find_if(g_installedTitles.begin(), g_installedTitles.end(),
                           [titleId](const InstalledTitle &title) { return title.titleId == titleId; });
    return it == g_installedTitles.end() ? formatTitleId(titleId) : it->name;
}

std::vector<DetectedGame> detectGames(const std::vector<Achievement> &achievements, u64 currentId) {
    ensureInstalledTitles();

    std::unordered_set<u64> seen;
    std::vector<DetectedGame> games;

    auto addGame = [&](u64 titleId, const std::string &name) {
        if (titleId == 0 || !seen.insert(titleId).second) return;
        int count = 0;
        for (const auto &achievement : achievements) {
            if (matchesGame(achievement, titleId)) ++count;
        }
        games.push_back({titleId, name, count});
    };

    if (currentId != 0) addGame(currentId, installedTitleName(currentId));
    for (const auto &title : g_installedTitles)
        addGame(title.titleId, title.name);

    std::sort(games.begin(), games.end(),
              [](const DetectedGame &a, const DetectedGame &b) { return a.name < b.name; });
    return games;
}

class GuiUnlock : public tsl::Gui {
private:
    std::string m_name;
    std::string m_description;
    std::string m_status;
    std::string m_progress;

public:
    GuiUnlock(std::string name, std::string description,
              std::string status = "Achievement unlocked!",
              std::string progress = "")
        : m_name(std::move(name)), m_description(std::move(description)),
          m_status(std::move(status)), m_progress(std::move(progress)) {}

    tsl::elm::Element *createUI() override {
        auto *frame = new tsl::elm::OverlayFrame("NX-Achievements", m_status);
        auto *list = new tsl::elm::List();

        const std::string title = "\u2605 " + m_name + " - " + m_description;
        const std::string value = m_progress.empty() ? "Unlocked!" : m_progress;
        auto *item = new tsl::elm::ListItem(title, value);
        item->setClickListener([](u64 keys) {
            if (keys & HidNpadButton_A) {
                tsl::goBack();
                return true;
            }
            return false;
        });
        list->addItem(item);

        frame->setContent(list);
        return frame;
    }
};

class GuiGame : public tsl::Gui {
private:
    u64 m_titleId = 0;
    std::string m_titleIdText;
    std::string m_gameName;

public:
    GuiGame(u64 titleId, std::string gameName)
        : m_titleId(titleId), m_titleIdText(formatTitleId(titleId)),
          m_gameName(std::move(gameName)) {}

    tsl::elm::Element *createUI() override {
        auto *frame = new tsl::elm::OverlayFrame("NX-Achievements", VERSION + std::string(" - ") + m_gameName);
        auto *list = new tsl::elm::List();

        const auto achievements = loadAchievements();
        auto progress = loadProgress();

        int currentCount = 0;
        for (const auto &achievement : achievements) {
            if (!matchesGame(achievement, m_titleId)) continue;
            ++currentCount;
        }

        list->addItem(new tsl::elm::CategoryHeader(
            m_gameName + "  (" + std::to_string(currentCount) + " achievements)"));

        bool added = false;
        for (const auto &achievement : achievements) {
            if (!matchesGame(achievement, m_titleId)) continue;
            added = true;

            const bool counted = achievement.target > 0;
            const int current = counted ? progress.count(achievement.id) : 0;
            const bool complete = counted
                ? current >= achievement.target
                : progress.unlocked.count(achievement.id) != 0;

            const std::string marker = complete ? "\u2714 " : "\u2610 ";
            std::string title = marker + achievement.name;
            if (counted) {
                title += "  (" + std::to_string(std::min(current, achievement.target)) +
                         "/" + std::to_string(achievement.target) + ")";
            }
            const std::string value = complete ? "Unlocked" : achievement.description;

            auto *item = new tsl::elm::ListItem(title, value);

            const u64 gameId = m_titleId;
            const std::string gameName = m_gameName;
            const std::string id = achievement.id;
            const std::string name = achievement.name;
            const std::string description = achievement.description;
            const int target = achievement.target;

            item->setClickListener([gameId, gameName, id, name, description, target, counted](u64 keys) {
                auto state = loadProgress();

                if (counted) {
                    const int previous = state.count(id);
                    int value = previous;
                    bool changed = false;
                    bool progressed = false;
                    bool justCompleted = false;

                    if (keys & HidNpadButton_A) {
                        if (value < target) {
                            ++value;
                            changed = true;
                            progressed = true;
                        }
                        justCompleted = value >= target;
                    } else if (keys & HidNpadButton_X) {
                        if (value > 0) {
                            --value;
                            changed = true;
                        }
                    } else if (keys & HidNpadButton_Y) {
                        if (value != 0) {
                            value = 0;
                            changed = true;
                        }
                    }

                    if (!changed) return false;
                    if (value > 0) state.counts[id] = value;
                    else state.counts.erase(id);
                    state.unlocked.erase(id);
                    saveProgress(state);

                    if (progressed) {
                        const std::string progressText =
                            std::to_string(std::min(previous, target)) + "/" +
                            std::to_string(target) + "  +1  ->  " +
                            std::to_string(std::min(value, target)) + "/" +
                            std::to_string(target);
                        tsl::changeTo<GuiUnlock>(
                            name, description,
                            justCompleted ? "Achievement unlocked!" : "Achievement progress",
                            progressText);
                    } else {
                        tsl::changeTo<GuiGame>(gameId, gameName);
                    }
                    return true;
                }

                if (!(keys & HidNpadButton_A)) return false;
                if (state.unlocked.count(id)) {
                    state.unlocked.erase(id);
                    saveProgress(state);
                    tsl::changeTo<GuiGame>(gameId, gameName);
                } else {
                    state.unlocked.insert(id);
                    saveProgress(state);
                    tsl::changeTo<GuiUnlock>(name, description);
                }
                return true;
            });

            list->addItem(item);
        }

        if (!added) {
            list->addItem(new tsl::elm::ListItem("No achievements for this game",
                                                  "Add entries to achievements.txt"));
        }

        list->addItem(new tsl::elm::CategoryHeader("Info"));
        list->addItem(new tsl::elm::ListItem("Game Title ID", m_titleIdText));
        list->addItem(new tsl::elm::ListItem("Config", CONFIG_FILE));
        list->addItem(new tsl::elm::ListItem("A", "Toggle unlock / +1 with popup"));
        list->addItem(new tsl::elm::ListItem("X", "Counter -1"));
        list->addItem(new tsl::elm::ListItem("Y", "Reset counter"));

        frame->setContent(list);
        return frame;
    }
};

class GuiMain : public tsl::Gui {
private:
    u64 m_currentId = 0;

public:
    GuiMain() : m_currentId(currentTitleId()) {}

    tsl::elm::Element *createUI() override {
        auto *frame = new tsl::elm::OverlayFrame("NX-Achievements", VERSION + std::string(" - detected games"));
        auto *list = new tsl::elm::List();

        const auto achievements = loadAchievements();
        const auto games = detectGames(achievements, m_currentId);

        list->addItem(new tsl::elm::CategoryHeader(
            "Detected games  (" + std::to_string(games.size()) + ")"));

        auto addGameRow = [list](const DetectedGame &game, bool isCurrent) {
            std::string title = isCurrent ? "\u2605 " : "  ";
            title += game.name;
            const std::string value =
                std::to_string(game.achievements) + " achievements  " + formatTitleId(game.titleId);

            auto *item = new tsl::elm::ListItem(title, value);
            const u64 titleId = game.titleId;
            const std::string name = game.name;
            item->setClickListener([titleId, name](u64 keys) {
                if (keys & HidNpadButton_A) {
                    tsl::changeTo<GuiGame>(titleId, name);
                    return true;
                }
                return false;
            });
            list->addItem(item);
        };

        for (const auto &game : games) {
            if (m_currentId != 0 && game.titleId == m_currentId) {
                addGameRow(game, true);
                break;
            }
        }
        for (const auto &game : games) {
            if (m_currentId != 0 && game.titleId == m_currentId) continue;
            addGameRow(game, false);
        }

        if (games.empty()) {
            list->addItem(new tsl::elm::ListItem("No games detected",
                                                  "Install a title or check ns services"));
        }

        list->addItem(new tsl::elm::CategoryHeader("Info"));
        list->addItem(new tsl::elm::ListItem("Installed titles",
                                              std::to_string(g_installedTitles.size())));
        list->addItem(new tsl::elm::ListItem("Sources", "NAND / SD card / game card"));
        list->addItem(new tsl::elm::ListItem("Current Title ID", formatTitleId(m_currentId)));
        list->addItem(new tsl::elm::ListItem("Config", CONFIG_FILE));
        list->addItem(new tsl::elm::ListItem("A", "Open game"));
        list->addItem(new tsl::elm::ListItem("B", "Back"));

        frame->setContent(list);
        return frame;
    }
};

class OverlayNXA : public tsl::Overlay {
private:
    bool m_nsInitialized = false;

public:
    void initServices() override {
        ensureConfigDir();
        m_nsInitialized = R_SUCCEEDED(nsInitialize());
    }

    void exitServices() override {
        if (m_nsInitialized) nsExit();
    }

    std::unique_ptr<tsl::Gui> loadInitialGui() override {
        return initially<GuiMain>();
    }
};

} // namespace

int main(int argc, char **argv) {
    return tsl::loop<OverlayNXA>(argc, argv);
}
