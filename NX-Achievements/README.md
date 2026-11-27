# NX-Achievements

An Ultrahand/Tesla overlay for Nintendo Switch that detects installed games on NAND,
the SD card, and game cards, then shows achievement goals for the game you select.

See `../CHANGELOG.md` for the version history.

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

Open Ultrahand with its hotkey (default: ZL + ZR + D-Pad Down) or Tesla, then select **NX-Achievements**.
The first screen lists detected games. Press **A** on one to open its achievements.
Normal achievements use **A** to toggle lock/unlock. Countable achievements show
`current/target`: **A** adds 1, **X** subtracts 1, and **Y** resets the count.
Every counter step shows a one-row popup with the name/description on the left
and `1/10  +1  ->  2/10` on the right; reaching the target shows an unlock popup.

Progress is saved to `sd:/switch/achievements/progress.txt`.

## Achievement file format

```
TitleID|AchievementID|Name|Description[|Target]
```

- `TitleID` is the 16-digit uppercase application ID, e.g. `0100F43008C44000`.
- Use `*` to show an achievement for every game.
- Lines starting with `#` are comments.
- The optional `Target` makes a countable goal, e.g. `...|152` for 152 shrines.

## Achievement data

`data/achievements.txt` currently contains **9,891 achievements for 228 games**:

- All 133 non-Steam games use IGN-style checklist goals (IGN where available,
  other reputable checklists otherwise). Sources are in `CHECKLIST_SOURCES.md`.
- PC games ported to Switch mirror their Steam achievement names and descriptions
  (for example Stardew Valley, Terraria, Hollow Knight, Silksong, Hades, Skyrim,
  DOOM, Balatro, Vampire Survivors, Dead by Daylight, Civilization VI, and 20
  Minutes Till Dawn).
- Switch title IDs come from `blawar/titledb` (`US.en.json`); none are guessed.
- Steam data comes from the public Steam community achievement pages.

Every game has at least 20 goals. Games with short Steam lists are padded with
manual goals so nothing is left thin.

Game definitions live in five places:

- `tools/generate_achievements.py` — the original curated set.
- `tools/games_extra.py` — the expanded catalog plus verified Steam appid mappings.
- `tools/goals_extra.py` — category templates that fill thin lists to 20+, with
  game-specific wording for Zelda titles (shrines, towers, dungeons/temples,
  Koroks, Zonai abilities).
- `tools/totk_checklist.py` — Tears of the Kingdom 100% checklist with countable
  targets from IGN's guide.
- `tools/checklists/` — IGN-style checklist goals for the other non-Steam games.
  Sources are listed in `CHECKLIST_SOURCES.md`.

Regenerate the file after editing any of the tools files:

```bash
python3 tools/generate_achievements.py /tmp/titledb-US.json
python3 tools/validate_achievements.py
python3 tools/generate_supported_games.py
python3 tools/generate_readme.py
```

## Testing status

Not all achievements have been tested in game. Some goal names, descriptions,
targets, or title IDs may still need correction.

## Current limitations

- Achievements are tracked manually: A toggles or counts up, X counts down, Y resets.
  Ultrahand/Tesla overlays cannot draw automatic popups over arbitrary games.
- Steam achievements are mirrored names/descriptions only; the Switch overlay cannot
  read a Steam account or unlock Steam achievements automatically.
- Save-data-based automatic checks can be added later with per-game parsers.
