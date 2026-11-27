# NX-Achievements

A Nintendo Switch [Tesla](https://github.com/WerWolv/Tesla) overlay that shows
achievement goals for the game currently running. It works over any title:
open Tesla with the hotkey, select **NX-Achievements**, and press **A** to
unlock or lock an achievement.

## Repository layout

```
NX-Achievements/        Overlay source, Makefile, achievement data, generator
libtesla/               Vendored libtesla (GPLv2, see libtesla/LICENSE)
SUPPORTED_GAMES.md      Full list of supported games and their achievement counts
```

## Features

- Reads the current application Title ID with `pmdmnt`.
- Loads achievements from `sdmc:/switch/achievements/achievements.txt`.
- Data-driven: adding games needs no rebuild of the `.ovl`.
- Saves unlock state and counters to `sdmc:/switch/achievements/progress.txt`.
- Countable goals show `current/target`; **A** adds 1, **X** subtracts 1, **Y** resets.
- Shows an unlock popup when an achievement is completed.
- 9,891 achievements across 228 games: IGN-style checklists for all 133 non-Steam
  games, plus mirrored Steam names/descriptions for PC games ported to Switch.

## Build

Requires devkitPro `switch-dev`:

```bash
export DEVKITPRO=/opt/devkitpro
export PATH="$DEVKITPRO/tools/bin:$PATH"
cd NX-Achievements
make -j2
```

Output: `NX-Achievements/NX-Achievements.ovl`

## Install

Copy these files to the Switch SD card:

```
sd:/switch/.overlays/NX-Achievements.ovl
sd:/switch/achievements/achievements.txt
```

Then run **hekate → Tools → Fix Archive Bit** if you wrote from a computer.
Boot CFW and open Tesla (default **L + D-Pad Down**).

## Achievement format

```
TitleID|AchievementID|Name|Description[|Target]
```

- `TitleID` is the 16-digit uppercase application ID, or `*` for every game.
- Lines starting with `#` are comments.
- Without `Target`, **A** toggles unlock/lock.
- With `Target`, the goal is counted: **A** adds 1, **X** subtracts 1, **Y** resets.
  For example, `...|Shrines|Complete all 152 shrines|152` displays `0/152`.

## Regenerating the achievement list

```bash
curl -fL -o /tmp/titledb-US.json \
  https://raw.githubusercontent.com/blawar/titledb/master/US.en.json
python3 NX-Achievements/tools/generate_achievements.py /tmp/titledb-US.json
python3 NX-Achievements/tools/validate_achievements.py
python3 NX-Achievements/tools/generate_supported_games.py
```

Switch title IDs come from [blawar/titledb](https://github.com/blawar/titledb).
Steam achievement names/descriptions are mirrored from public Steam community
achievement pages. Non-Steam games use IGN-style checklist goals where available;
see `CHECKLIST_SOURCES.md` for the per-game sources.

## Limitations

- Achievements are tracked manually: A toggles or counts up, X counts down, Y resets.
  A normal Tesla overlay cannot draw automatic popups over arbitrary games; that
  requires a game-specific plugin.
- Steam entries are names/descriptions only — the overlay cannot read a Steam
  account or unlock Steam achievements.
- Automatic checks from save data or memory can be added later per game.

## License

The overlay code is released under GPL-2.0-or-later to match the vendored
libtesla license. See `libtesla/LICENSE`.
