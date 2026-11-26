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

Launch Tesla with its hotkey (default: L + D-Pad Down) and select **NX-Achievements**.
Normal achievements use **A** to toggle lock/unlock. Countable achievements show
`current/target`: **A** adds 1, **X** subtracts 1, and **Y** resets the count.
Completing an achievement shows a popup with its name.

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

`data/achievements.txt` currently contains **9,541 achievements for 227 games**:

- Famous first-party and third-party Switch games use hand-written goals.
- PC games ported to Switch mirror their Steam achievement names and descriptions
  (for example Stardew Valley, Terraria, Hollow Knight, Hades, Skyrim, DOOM,
  Balatro, Vampire Survivors, Dead by Daylight, Civilization VI, and 20 Minutes
  Till Dawn).
- Switch title IDs come from `blawar/titledb` (`US.en.json`); none are guessed.
- Steam data comes from the public Steam community achievement pages.

Every game has at least 20 goals. Games with short Steam lists are padded with
manual goals so nothing is left thin.

Game definitions live in four files:

- `tools/generate_achievements.py` — the original curated set.
- `tools/games_extra.py` — the expanded catalog plus verified Steam appid mappings.
- `tools/goals_extra.py` — category templates that fill thin lists to 20+, with
  game-specific wording for Zelda titles (shrines, towers, dungeons/temples,
  Koroks, Zonai abilities).
- `tools/totk_checklist.py` — Tears of the Kingdom 100% checklist with countable
  targets from IGN's guide.

Regenerate the file after editing any of the tools files:

```bash
python3 tools/generate_achievements.py /tmp/titledb-US.json
```

## Current limitations

- Achievements are tracked manually with A (Tesla overlays cannot draw automatic popups over arbitrary games).
- Steam achievements are mirrored names/descriptions only; the Switch overlay cannot
  read a Steam account or unlock Steam achievements automatically.
- Save-data-based automatic checks can be added later with per-game parsers.
