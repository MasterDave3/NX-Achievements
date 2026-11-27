#define TESLA_INIT_IMPL
#include <tesla.hpp>

#include <algorithm>
#include <cstdio>
#include <cstdlib>
#include <fstream>
#include <sstream>
#include <string>
#include <unordered_map>
#include <unordered_set>
#include <vector>
#include <sys/stat.h>

namespace {

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

        list->addItem(new tsl::elm::CategoryHeader("\u2605 " + m_status));

        auto *item = new tsl::elm::ListItem(m_name, m_description);
        list->addItem(item);

        if (!m_progress.empty()) {
            list->addItem(new tsl::elm::ListItem("Progress", m_progress));
        }

        auto *cont = new tsl::elm::ListItem("Continue", "Press A");
        cont->setClickListener([](u64 keys) {
            if (keys & HidNpadButton_A) {
                tsl::goBack();
                return true;
            }
            return false;
        });
        list->addItem(cont);

        frame->setContent(list);
        return frame;
    }
};

class GuiMain : public tsl::Gui {
private:
    u64 m_titleId = 0;
    std::string m_titleIdText;

public:
    GuiMain() {
        m_titleId = currentTitleId();
        m_titleIdText = formatTitleId(m_titleId);
    }

    tsl::elm::Element *createUI() override {
        auto *frame = new tsl::elm::OverlayFrame("NX-Achievements", "v0.4.0 - " + m_titleIdText);
        auto *list = new tsl::elm::List();

        const auto achievements = loadAchievements();
        auto progress = loadProgress();

        int currentCount = 0;
        for (const auto &achievement : achievements) {
            if (!matchesGame(achievement, m_titleId)) continue;
            currentCount++;
        }

        list->addItem(new tsl::elm::CategoryHeader(
            "Current game  (" + std::to_string(currentCount) + " achievements)"));

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
            const std::string id = achievement.id;
            const std::string name = achievement.name;
            const std::string description = achievement.description;
            const int target = achievement.target;

            item->setClickListener([id, name, description, target, counted](u64 keys) {
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
                        const std::string progress =
                            std::to_string(std::min(previous, target)) + "/" +
                            std::to_string(target) + "  +1  ->  " +
                            std::to_string(std::min(value, target)) + "/" +
                            std::to_string(target);
                        tsl::changeTo<GuiUnlock>(
                            name, description,
                            justCompleted ? "Achievement unlocked!" : "Achievement progress",
                            progress);
                    } else {
                        tsl::changeTo<GuiMain>();
                    }
                    return true;
                }

                if (!(keys & HidNpadButton_A)) return false;
                if (state.unlocked.count(id)) {
                    state.unlocked.erase(id);
                    saveProgress(state);
                    tsl::changeTo<GuiMain>();
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
        list->addItem(new tsl::elm::ListItem("Current Title ID", m_titleIdText));
        list->addItem(new tsl::elm::ListItem("Config", CONFIG_FILE));
        list->addItem(new tsl::elm::ListItem("A", "Toggle unlock / +1 with popup"));
        list->addItem(new tsl::elm::ListItem("X", "Counter -1"));
        list->addItem(new tsl::elm::ListItem("Y", "Reset counter"));

        frame->setContent(list);
        return frame;
    }
};

class OverlayNXA : public tsl::Overlay {
public:
    void initServices() override {
        ensureConfigDir();
    }

    std::unique_ptr<tsl::Gui> loadInitialGui() override {
        return initially<GuiMain>();
    }
};

} // namespace

int main(int argc, char **argv) {
    return tsl::loop<OverlayNXA>(argc, argv);
}
