#define TESLA_INIT_IMPL
#include <tesla.hpp>

#include <memory>
#include <string>

namespace {

constexpr const char *VERSION = "v0.6.0";

// Deliberately tiny overlay: no catalog parsing, no ns enumeration, no extra
// services. libtesla already provides fs, hid, pl, pmdmnt, hidsys and setsys;
// this overlay only draws static text so opening it cannot exhaust heap or
// collide with Ultrahand's own service sessions.
class GuiMain : public tsl::Gui {
public:
    tsl::elm::Element *createUI() override {
        auto *frame = new tsl::elm::OverlayFrame(
            "NX-Achievements", std::string(VERSION) + " - safe mode");
        auto *list = new tsl::elm::List();

        list->addItem(new tsl::elm::CategoryHeader("Status"));
        list->addItem(new tsl::elm::ListItem("Overlay", "Loaded safely"));
        list->addItem(new tsl::elm::ListItem("Catalog",
                                             "503 games / 21,643 achievements"));
        list->addItem(new tsl::elm::ListItem("Config",
                                             "sdmc:/switch/achievements"));

        list->addItem(new tsl::elm::CategoryHeader("Watcher"));
        list->addItem(new tsl::elm::ListItem("Boot start",
                                             "Disabled until crash-free boot"));
        list->addItem(new tsl::elm::ListItem("Toasts",
                                             "Pending hardware validation"));

        list->addItem(new tsl::elm::CategoryHeader("Controls"));
        list->addItem(new tsl::elm::ListItem("B", "Close overlay"));

        frame->setContent(list);
        return frame;
    }
};

class OverlayNXA : public tsl::Overlay {
public:
    void initServices() override {}
    void exitServices() override {}

    std::unique_ptr<tsl::Gui> loadInitialGui() override {
        return initially<GuiMain>();
    }
};

} // namespace

int main(int argc, char **argv) {
    return tsl::loop<OverlayNXA>(argc, argv);
}
