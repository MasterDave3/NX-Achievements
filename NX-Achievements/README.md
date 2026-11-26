# NX-Achievements

A Tesla overlay for Nintendo Switch that shows achievement goals for the currently running game.

## Build

```bash
export DEVKITPRO=/opt/devkitpro
export PATH="$DEVKITPRO/tools/bin:$PATH"
cd NX-Achievements   # from the repository root
make -j2
```

Output: `NX-Achievements.ovl`

## Install

Copy to the Switch SD card:

```
sd:/switch/.overlays/NX-Achievements.ovl
sd:/switch/achievements/achievements.txt   (from data/achievements.txt)
```

Launch Tesla with its hotkey (default: L + D-Pad Down), select **NX-Achievements**, and press **A** on an achievement to toggle it. When unlocking, a popup shows the achievement name.

Progress is saved to `sd:/switch/achievements/progress.txt`.

## Achievement file format

```
TitleID|AchievementID|Name|Description
```

- `TitleID` is the 16-digit uppercase application ID, e.g. `0100F43008C44000`.
- Use `*` to show an achievement for every game.
- Lines starting with `#` are comments.

## Achievement data

`data/achievements.txt` currently contains **2,776 achievements for 91 games**:

- Famous first-party and third-party Switch games use hand-written goals.
- PC games ported to Switch mirror their Steam achievement names and descriptions
  (for example Stardew Valley, Terraria, Hollow Knight, Hades, Skyrim, DOOM).
- Switch title IDs come from `blawar/titledb` (`US.en.json`).
- Steam data comes from the public Steam community achievement pages.

Regenerate the file after editing `tools/generate_achievements.py`:

```bash
python3 tools/generate_achievements.py /tmp/titledb-US.json
```

## Current limitations

- Achievements are tracked manually with A (Tesla overlays cannot draw automatic popups over arbitrary games).
- Steam achievements are mirrored names/descriptions only; the Switch overlay cannot
  read a Steam account or unlock Steam achievements automatically.
- Save-data-based automatic checks can be added later with per-game parsers.
