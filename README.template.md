# NX-Achievements

A Nintendo Switch overlay (`.ovl`) for
[Ultrahand](https://github.com/ppkantorski/Ultrahand-Overlay) or
[Tesla](https://github.com/WerWolv/Tesla) that shows achievement goals for the
game currently running. Ultrahand is a drop-in Tesla replacement built on
libultrahand, so the same overlay works in both. Open your overlay menu, select
**NX-Achievements**, and press **A** to unlock or lock an achievement.

> This `README.md` is generated from `README.template.md`. Edit the template,
> then run `python3 NX-Achievements/tools/generate_readme.py`. The standalone
> `.md` files are still kept and are mirrored into this page below.

## Repository layout

```
NX-Achievements/        Overlay source, Makefile, achievement data, generator
libtesla/               Vendored libtesla (GPLv2, see libtesla/LICENSE)
SUPPORTED_GAMES.md      Full list of supported games and their achievement counts
CHECKLIST_SOURCES.md    Sources for the non-Steam checklist goals
CHANGELOG.md            Version history and what changed in each version
README.template.md      Source template for this README
```

## Features

- Reads the current application Title ID with `pmdmnt`.
- Detects installed games on NAND, the SD card, and an inserted game card with
  the `ns` service, then shows the matching achievements for any game you open.
- Loads achievements from `sdmc:/switch/achievements/achievements.txt`.
- Data-driven: adding games needs no rebuild of the `.ovl`.
- Saves unlock state and counters to `sdmc:/switch/achievements/progress.txt`.
- Countable goals show `current/target`; **A** adds 1, **X** subtracts 1, **Y** resets.
- Shows `old  +1  ->  new` on every counter step, e.g. `1/10  +1  ->  2/10`.
- 21,643 achievements across 503 games: IGN-style checklists for all 227 non-Steam
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
Boot CFW and open Ultrahand (default **ZL + ZR + D-Pad Down**) or Tesla.
The first screen lists detected games; press **A** on one to open its achievements.

## Achievement format

```
TitleID|AchievementID|Name|Description[|Target]
```

- `TitleID` is the 16-digit uppercase application ID, or `*` for every game.
- Lines starting with `#` are comments.
- Without `Target`, **A** toggles unlock/lock.
- With `Target`, the goal is counted: **A** adds 1, **X** subtracts 1, **Y** resets.
  For example, `...|Shrines|Complete all 152 shrines|152` displays `0/152`.

## Regenerating the generated files

```bash
curl -fL -o /tmp/titledb-US.json \
  https://raw.githubusercontent.com/blawar/titledb/master/US.en.json
python3 NX-Achievements/tools/generate_achievements.py /tmp/titledb-US.json
python3 NX-Achievements/tools/validate_achievements.py
python3 NX-Achievements/tools/generate_supported_games.py
python3 NX-Achievements/tools/generate_readme.py
```

Switch title IDs come from [blawar/titledb](https://github.com/blawar/titledb).
Steam achievement names/descriptions are mirrored from public Steam community
achievement pages. Non-Steam games use IGN-style checklist goals where available;
see `CHECKLIST_SOURCES.md` for the per-game sources.

## Testing status

Not all achievements have been tested in game. The catalog is data-driven, so some
goal names, descriptions, targets, or title IDs may still need correction.

## Limitations

- Achievements are tracked manually: A toggles or counts up, X counts down, Y resets.
  A normal Ultrahand/Tesla overlay cannot draw automatic popups over arbitrary
  games; that requires a game-specific plugin.
- Steam entries are names/descriptions only — the overlay cannot read a Steam
  account or unlock Steam achievements.
- Automatic checks from save data or memory can be added later per game.

<!-- INCLUDE:CHANGELOG.md -->

<!-- INCLUDE:SUPPORTED_GAMES.md -->

<!-- INCLUDE:CHECKLIST_SOURCES.md -->

## License

The overlay code is released under GPL-2.0-or-later to match the vendored
libtesla license. See `libtesla/LICENSE`.
