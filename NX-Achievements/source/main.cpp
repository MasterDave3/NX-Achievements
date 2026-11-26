#define TESLA_INIT_IMPL
#include <tesla.hpp>

#include <algorithm>
#include <fstream>
#include <sstream>
#include <string>
#include <unordered_set>
#include <vector>
#include <cstdio>
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
        out.push_back({parts[0], parts[1], parts[2], parts[3]});
    }
    return out;
}

std::unordered_set<std::string> loadUnlocked() {
    ensureConfigDir();
    std::unordered_set<std::string> out;
    std::ifstream file(PROGRESS_FILE);
    if (!file.is_open()) return out;

    std::string line;
    while (std::getline(file, line)) {
        line = trim(line);
        if (!line.empty() && line[0] != '#') out.insert(line);
    }
    return out;
}

void saveUnlocked(const std::unordered_set<std::string> &ids) {
    ensureConfigDir();
    std::ofstream file(PROGRESS_FILE, std::ios::trunc);
    for (const auto &id : ids)
        file << id << '\n';
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

public:
    GuiUnlock(std::string name, std::string description)
        : m_name(std::move(name)), m_description(std::move(description)) {}

    tsl::elm::Element *createUI() override {
        auto *frame = new tsl::elm::OverlayFrame("NX-Achievements", "Achievement unlocked!");
        auto *list = new tsl::elm::List();

        list->addItem(new tsl::elm::CategoryHeader("\u2605 Achievement unlocked"));

        auto *item = new tsl::elm::ListItem(m_name, m_description);
        list->addItem(item);

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
        auto *frame = new tsl::elm::OverlayFrame("NX-Achievements", "v0.1.0 - " + m_titleIdText);
        auto *list = new tsl::elm::List();

        const auto achievements = loadAchievements();
        auto unlocked = loadUnlocked();

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

            const bool isUnlocked = unlocked.count(achievement.id) != 0;
            const std::string marker = isUnlocked ? "\u2714 " : "\u2610 ";
            const std::string title = marker + achievement.name;
            const std::string value = isUnlocked ? "Unlocked" : achievement.description;

            auto *item = new tsl::elm::ListItem(title, value);
            const std::string id = achievement.id;
            const std::string name = achievement.name;
            const std::string description = achievement.description;

            item->setClickListener([id, name, description](u64 keys) {
                if (!(keys & HidNpadButton_A)) return false;

                auto ids = loadUnlocked();
                if (ids.count(id)) {
                    ids.erase(id);
                    saveUnlocked(ids);
                    tsl::changeTo<GuiMain>();
                } else {
                    ids.insert(id);
                    saveUnlocked(ids);
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
        list->addItem(new tsl::elm::ListItem("A", "Unlock / lock achievement"));

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
