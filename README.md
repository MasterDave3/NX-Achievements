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
NX-Achievements/watcher/ Automatic-detection sysmodule proof of concept
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
- Experimental automatic detection through a generic sysmodule that reads
  per-game rules from `sdmc:/switch/achievements/detectors.txt`, reads the live
  save, and writes Ultrahand notification JSON files. New games can be added by
  editing that data file without rebuilding the sysmodule.
- First implemented detector: **Pokémon Legends Z-A** Lumiose Pokedex (`CZA_01`).

## Build

Requires devkitPro `switch-dev`:

```bash
export DEVKITPRO=/opt/devkitpro
export PATH="$DEVKITPRO/tools/bin:$PATH"
cd NX-Achievements
make -j2
```

Output: `NX-Achievements/NX-Achievements.ovl`

Build the Z-A watcher sysmodule:

```bash
cd NX-Achievements/watcher
make -j2
```

Output: `NX-Achievements/watcher/NXAchievementsWatcher.nsp`

## Install

Copy these files to the Switch SD card:

```
sd:/switch/.overlays/NX-Achievements.ovl
sd:/switch/achievements/achievements.txt
sd:/switch/achievements/detectors.txt
```

Then run **hekate → Tools → Fix Archive Bit** if you wrote from a computer.
Boot CFW and open Ultrahand (default **ZL + ZR + D-Pad Down**) or Tesla.
The first screen lists detected games; press **A** on one to open its achievements.

### Automatic detection (Z-A proof of concept)

The watcher is a separate Atmosphère sysmodule. Install it like this:

```
sd:/atmosphere/contents/6900000000000A01/exefs.nsp        <- NXAchievementsWatcher.nsp
sd:/atmosphere/contents/6900000000000A01/toolbox.json     <- watcher/toolbox.json
sd:/atmosphere/contents/6900000000000A01/flags/boot2.flag  <- empty file
```

Reboot CFW, then launch a game that has a rule in `detectors.txt`. The watcher
reads that game's live account save only while the game is running. On its first
successful read it records the current value silently so launching the game
does not fire a fake unlock. Every later increment writes one Ultrahand toast
and updates the matching line in `progress.txt`. Diagnostics are appended to
`sd:/switch/achievements/watcher.log`.

Only Z-A `CZA_01` has a real detector right now. Every other goal and game still
uses the manual A/X/Y controls until a verified save/memory rule is added.
Ultrahand must be active for the external `.notify` toasts to appear; Tesla-only
users still get the progress file updates but not the automatic popup.

### Detector format

```
title_id|achievement_id|kind|target|save_path|block_key|dex_list
```

Current kind:

- `swish_pokedex_caught` — count caught Pokémon in a SwishCrypto Pokédex block.
  `dex_list` currently supports `lumio_se_230`.

The shipped rule is:

```
0100F43008C44000|CZA_01|swish_pokedex_caught|230|/main|2D87BE5C|lumio_se_230
```

Adding a new game is a data-only change: edit `detectors.txt` on the SD card and
restart CFW. No `.ovl` rebuild is required.

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
  games. The Z-A watcher is the first game-specific exception.
- Steam entries are names/descriptions only — the overlay cannot read a Steam
  account or unlock Steam achievements.
- Automatic checks from save data or memory are game-specific. The watcher is
  generic, but only `CZA_01` has a verified detector; the remaining goals need
  save/memory mappings before they can notify automatically.

## Changelog

All notable changes to NX-Achievements. The version shown in the overlay matches
the tags below.

### [Unreleased]

- Added an independent boot marker to the watcher using `fsdevMountSdmc()` and
  `sd:/switch/achievements/watcher.boot`, so a launch can be confirmed even when
  the raw `fsOpenSdCardFileSystem()` path fails. Also raised
  `__nx_fs_num_sessions` from 1 to 4. Build is now v0.3.1.
- Reworked the watcher to remove the boot-time `pmdmnt`/account service race:
  `__appInit` now opens only `sm` and `fs`, the process waits 10 seconds, then
  account services are initialized lazily. `pmdmnt` is no longer used at all;
  detector state is keyed by configured title ID instead of the foreground
  process. Build is now v0.3.0.
- Disabled the experimental watcher on the SD card after repeated Atmosphère
  crashes: both `boot2.flag` and `exefs.nsp` are renamed with `.disabled`, so the
  module cannot start automatically or manually. Automatic in-game notifications
  are unavailable until a stable replacement is validated; the safe overlay
  remains installed.
- Replaced the overlay UI with a minimal safe build. Opening it no longer parses
  the full 21,643-entry catalog, enumerates installed titles, or calls
  `nsInitialize()`, so it cannot crash Atmosphère from heap exhaustion or
  service-session conflicts. The previous full UI is preserved at
  `NX-Achievements/tools/full_overlay_main.cpp.txt` and will be restored in
  bounded stages after hardware stability is confirmed.
- Fixed the overlay not appearing in Tesla/Ultrahand's Overlays list. The build
  now embeds `control.nacp` with `elf2nro --nacp`, so the loader can read the
  `NX-Achievements` display name instead of skipping the `.ovl`.
- Fixed an Atmosphère boot crash (`ams_mitm`, `std::abort() 0xffe`) caused by
  the watcher being built as a normal application: it now uses
  `AppletType_None`, a bounded 512 KiB sysmodule heap, a 16 KiB main-thread
  stack, streaming reads for `achievements.txt`, and on-demand SwishCrypto
  decryption so the ~3 MiB save and the 2 MB catalog never sit in memory.
- Refactored the watcher into a **generic detector framework**. Rules live in
  `sdmc:/switch/achievements/detectors.txt` as
  `title_id|achievement_id|kind|target|save_path|block_key|dex_list`, so any
  supported game can be added without rebuilding the sysmodule.
- The watcher now loads achievement name/description/target from the normal
  `achievements.txt` catalog, keeps silent baselines per active title, and emits
  the same `old/target  +1  ->  new/target` toast for every new rule.
- Added an experimental **NX-Achievements Watcher** sysmodule for Pokémon Legends
  Z-A. It reads the live account save with `fsOpenReadOnlySaveDataFileSystem`,
  decrypts SwishCrypto blocks in C, and counts registered Lumiose Pokedex entries
  (`CZA_01`).
- On each new registered Pokémon the watcher writes an Ultrahand external
  notification JSON under `/config/ultrahand/notifications/` with the same
  `old/target  +1  ->  new/target` text as the overlay, then updates
  `progress.txt`. The first successful save read after launch sets a silent
  baseline so no fake unlock is emitted.
- Added `NX-Achievements/watcher/source/za_save.hpp`, a host parser test
  (`tools/za_parse_test.cpp`), and a verified Python prototype
  (`tools/za_save_probe.py`). The C parser matches PKHeX byte-for-byte on the
  available Z-A saves and uses the PKHeX-derived 230-species Lumiose dex list.
- Expanded the catalog by 170 approved games after verifying each title ID in
  blawar/titledb. Steam ports with at least 20 achievements are mirrored only;
  all other games use IGN-style completion checklists. Catalog is now
  **406 games / 16,826 achievements**.
- Added batch 9 checklist modules and `tools/new_games_batch9.py` so the large
  catalog expansion stays auditable. Data-only change: no `.ovl` rebuild needed.
- Added 59 more approved games after verifying each title ID in blawar/titledb.
  Steam ports with at least 20 achievements are mirrored only; the rest use
  IGN-style completion checklists. Catalog is now
  **465 games / 19,457 achievements**.
- Added batch 10 checklist modules and `tools/new_games_batch10.py`, keeping the
  same data-only release workflow.
- Added 38 more approved indie games after verifying each title ID in
  blawar/titledb. Steam ports with at least 20 achievements are mirrored only;
  the rest use IGN-style completion checklists. Catalog is now
  **503 games / 21,643 achievements**.
- Added the batch 11 checklist module and `tools/new_games_batch11.py`.

### [v0.6.0] - 2026-11-26

- Added a **Detected games** menu. The overlay now enumerates installed
  applications from NAND, the SD card, and an inserted game card through the
  `ns` service, then lists the matching achievement count for each game.
- Selecting any detected game opens its achievement list. The currently running
  game is marked with a star and stays available at the top of the list.
- Achievements now stay on the selected game after a counter change instead of
  returning to the game list.
- Bumped Makefile app version and overlay subtitle to `v0.6.0`.
- Added **Little Nightmares III** with 44 Steam-mirrored achievements (Switch
  Title ID `010066101A55A000`, Steam appid `1392860`).
- Added the remaining Sonic games available on Switch: **Sonic X Shadow
  Generations**, **Sonic Forces**, **Team Sonic Racing**, **Sonic Origins /
  Origins Plus**, **Sonic Racing CrossWorlds**, plus checklist-based goals for
  **SEGA AGES Sonic The Hedgehog** and **SEGA AGES Sonic The Hedgehog 2**.
  Catalog is now **236 games / 10,212 achievements**.

### [v0.5.0] - 2026-11-26

- Notification is now a single row: name and description on the left, progress on
  the right, e.g. `Weaved - Defeat Widow` / `1/10  +1  ->  2/10`.
- Removed the separate `Progress` and `Continue` rows from the popup.
- Press **A** or **B** to close the notification.
- Commit: `884e702`

### [v0.4.0] - 2026-11-26

- Counter popups now show the old and new value, e.g.
  `56/900  +1  ->  57/900`.
- The final step still switches the header to **Achievement unlocked!**.
- Commit: `451302d`

### [v0.3.0] - 2026-11-26

- Popups now appear on **every** counter increment, not just at completion.
- Added an **Achievement progress** header for partial steps.
- **X** and **Y** still subtract/reset silently.
- Commit: `78ed09e`

### [v0.2.0] - 2026-11-26

- Added countable goals with a numeric target in `achievements.txt`.
- Countable goals display `current/target`; **A** adds 1, **X** subtracts 1,
  **Y** resets, and progress is saved as `ID|count` in `progress.txt`.
- Replaced Tears of the Kingdom goals with a 45-goal IGN-style 100% checklist.
- Added 20 Minutes Till Dawn with 34 mirrored Steam achievements.
- Added IGN-style checklist goals for all **133 non-Steam games** (2,938 goals),
  sourced in `CHECKLIST_SOURCES.md`. Steam ports were left untouched.
- Added Hollow Knight: Silksong as a Steam mirror with 52 achievements.
- Added `tools/validate_achievements.py` and `tools/generate_supported_games.py`.
- Catalog grew to **228 games / 9,891 achievements**.
- Documented Ultrahand compatibility; the `.ovl` works in Ultrahand and Tesla.
- Commits: `68d3fe7`, `01f11d7`, `774f0f5`, `1d0696c`

### [v0.1.0] - 2026-11-26

- Initial Tesla overlay with title-ID detection, data-driven achievements from
  `sdmc:/switch/achievements/achievements.txt`, manual **A** toggles, and
  `progress.txt` saving.
- Initial catalog of 91 games, expanded to 226 games / 7,083 achievements.
- Added `SUPPORTED_GAMES.md` and vendored `libtesla`.
- Guaranteed every game has at least 20 goals.
- Commits: `f8a7141`, `cf00769`, `f38cd16`, `153474e`

## Supported games

Every game below has at least 20 achievements in `NX-Achievements/data/achievements.txt`.
Switch title IDs come from [blawar/titledb](https://github.com/blawar/titledb);
Steam achievement names/descriptions are mirrored from public Steam community pages.
Non-Steam games use IGN-style checklist goals; sources are listed in `CHECKLIST_SOURCES.md`.

**503 games · 21,643 achievements** (plus one global `FIRST_BOOT` goal)

IGN-style checklist goals cover all 227 non-Steam games, using IGN where available
and other reputable checklists otherwise. 1529 goals across the catalog are countable
(`current/target`) and advance with A/X/Y on the overlay.

| # | Game | Title ID | Achievements |
|---|---|---|---|
| 1 | The Legend of Zelda: Breath of the Wild | `01007EF00011E000` | 22 |
| 2 | The Legend of Zelda: Tears of the Kingdom | `0100F2C0115B6000` | 45 |
| 3 | Mario Kart 8 Deluxe | `0100152000022000` | 34 |
| 4 | Super Mario Odyssey | `0100000000010000` | 24 |
| 5 | Super Smash Bros. Ultimate | `01006A800016E000` | 26 |
| 6 | Pokemon Legends Z-A | `0100F43008C44000` | 24 |
| 7 | Pokemon Scarlet | `0100A3D008C5C000` | 24 |
| 8 | Pokemon Violet | `01008F6008C5E000` | 24 |
| 9 | Pokemon Legends Arceus | `01001F5010DFA000` | 25 |
| 10 | Pokemon Sword | `0100ABF008968000` | 24 |
| 11 | Pokemon Shield | `01008DB008C2C000` | 24 |
| 12 | Pokemon Lets Go Pikachu | `010003F003A34000` | 22 |
| 13 | Pokemon Lets Go Eevee | `0100187003A36000` | 22 |
| 14 | Animal Crossing New Horizons | `01006F8002326000` | 25 |
| 15 | Splatoon 3 | `0100C2500FC20000` | 24 |
| 16 | Splatoon 2 | `01003BC0000A0000` | 24 |
| 17 | Super Mario Party | `010036B0034E4000` | 24 |
| 18 | Mario Party Superstars | `01006FE013472000` | 24 |
| 19 | Mario + Rabbids Sparks of Hope | `0100317013770000` | 24 |
| 20 | Mario + Rabbids Kingdom Battle | `010067300059A000` | 24 |
| 21 | Luigis Mansion 3 | `0100DCA0064A6000` | 20 |
| 22 | Super Mario Maker 2 | `01009B90006DC000` | 20 |
| 23 | Mario Tennis Aces | `0100BDE00862A000` | 20 |
| 24 | Mario Golf Super Rush | `0100C9C00E25C000` | 20 |
| 25 | Fire Emblem Three Houses | `010055D009F78000` | 20 |
| 26 | Fire Emblem Engage | `0100A6301214E000` | 20 |
| 27 | Xenoblade Chronicles 2 | `0100E95004038000` | 20 |
| 28 | Xenoblade Chronicles 3 | `010074F013262000` | 20 |
| 29 | Xenoblade Chronicles Definitive Edition | `0100FF500E34A000` | 20 |
| 30 | Metroid Dread | `010093801237C000` | 20 |
| 31 | Metroid Prime Remastered | `010012101468C000` | 20 |
| 32 | Hyrule Warriors Age of Calamity | `01002B00111A2000` | 20 |
| 33 | Zelda Links Awakening | `01006BB00C6F0000` | 20 |
| 34 | Super Mario 3D World Bowsers Fury | `010028600EBDA000` | 20 |
| 35 | New Super Mario Bros U Deluxe | `0100EA80032EA000` | 20 |
| 36 | Donkey Kong Country Tropical Freeze | `0100C1F0051B6000` | 20 |
| 37 | Captain Toad Treasure Tracker | `01009BF0072D4000` | 20 |
| 38 | Kirby and the Forgotten Land | `01004D300C5AE000` | 20 |
| 39 | Kirby Star Allies | `01007E3006DDA000` | 20 |
| 40 | Kirby Return to Dream Land Deluxe | `01006B601380E000` | 20 |
| 41 | Yoshis Crafted World | `01006000040C2000` | 22 |
| 42 | Pikmin 3 Deluxe | `0100F4C009322000` | 22 |
| 43 | Pikmin 4 | `0100B7C00933A000` | 22 |
| 44 | Warioware Get it Together | `0100563010E0C000` | 22 |
| 45 | 1-2-Switch | `01000320000CC000` | 29 |
| 46 | ARMS | `01009B500007C000` | 22 |
| 47 | Ring Fit Adventure | `01002FF008C24000` | 22 |
| 48 | Nintendo Switch Sports | `0100D2F00D5C0000` | 22 |
| 49 | Mario Strikers Battle League | `010019401051C000` | 22 |
| 50 | Advance Wars 1+2 Re-Boot Camp | `0100300012F2A000` | 22 |
| 51 | Pokemon UNITE | `0100939011ED4000` | 22 |
| 52 | Super Mario Bros Wonder | `010015100B514000` | 24 |
| 53 | Minecraft | `0100D71004694000` | 22 |
| 54 | Diablo III Eternal Collection | `01001B300B9BE000` | 22 |
| 55 | Undertale | `010080B00AD66000` | 22 |
| 56 | Deltarune | `0100A0D022A68000` | 22 |
| 57 | Mario Kart Live Home Circuit | `0100ED100BA3A000` | 22 |
| 58 | Terraria | `0100E46006708000` | 137 |
| 59 | Stardew Valley | `0100E65002BB8000` | 49 |
| 60 | Hollow Knight | `0100633007D48000` | 63 |
| 61 | The Binding of Isaac Afterbirth+ | `010021C000B6A000` | 641 |
| 62 | Enter the Gungeon | `01009D60076F6000` | 54 |
| 63 | Dead Cells | `0100646009FBE000` | 121 |
| 64 | Celeste | `01002B30028F6000` | 32 |
| 65 | Cuphead | `0100A5C00D162000` | 42 |
| 66 | Hades | `0100535012974000` | 49 |
| 67 | The Elder Scrolls V Skyrim | `01000A10041EA000` | 75 |
| 68 | DOOM | `0100416004C00000` | 54 |
| 69 | DOOM Eternal | `0100B1A00D8CE000` | 50 |
| 70 | Rocket League | `01005EE0036EC000` | 88 |
| 71 | Among Us | `0100B0C013912000` | 33 |
| 72 | Fall Guys | `0100C3C015738000` | 34 |
| 73 | Ori and the Will of the Wisps | `01008DD013200000` | 37 |
| 74 | Ori and the Blind Forest | `010061D00DB74000` | 57 |
| 75 | Shovel Knight Treasure Trove | `010057D0021E8000` | 138 |
| 76 | Sonic Frontiers | `01004AD014BF0000` | 40 |
| 77 | Sonic Mania | `01009AA000FAA000` | 20 |
| 78 | Crash Bandicoot 4 Its About Time | `010073401175E000` | 51 |
| 79 | Spyro Reignited Trilogy | `010077B00E046000` | 105 |
| 80 | Monster Hunter Rise | `0100B04011742000` | 100 |
| 81 | Monster Hunter Stories 2 Wings of Ruin | `0100E21011446000` | 48 |
| 82 | Resident Evil 4 | `010099A00BC1E000` | 20 |
| 83 | Resident Evil Village | `0100CA0018C52000` | 56 |
| 84 | Resident Evil 2 | `01008800185B2000` | 44 |
| 85 | Dragon Ball FighterZ | `0100A250097F0000` | 35 |
| 86 | Persona 5 Royal | `01005CA01580E000` | 53 |
| 87 | Final Fantasy VIII Remastered | `01008B900DC0A000` | 34 |
| 88 | The Witcher 3 Wild Hunt | `0100BFE00E9CA000` | 78 |
| 89 | Disco Elysium The Final Cut | `01006C5015E84000` | 45 |
| 90 | Divinity Original Sin 2 | `010027400CDC6000` | 97 |
| 91 | Overcooked All You Can Eat | `0100F28011892000` | 42 |
| 92 | The Legend of Zelda: Skyward Sword HD | `01002DA013484000` | 22 |
| 93 | The Legend of Zelda: Echoes of Wisdom | `01008CF01BAAC000` | 22 |
| 94 | Detective Pikachu Returns | `010007500F27C000` | 22 |
| 95 | Fire Emblem Warriors | `0100F15003E64000` | 20 |
| 96 | Fire Emblem Warriors: Three Hopes | `010071F0143EA000` | 20 |
| 97 | Xenoblade Chronicles X: Definitive Edition | `0100453019AA8000` | 20 |
| 98 | Metroid Prime 4: Beyond | `010019A01E2F2000` | 20 |
| 99 | Luigi's Mansion 2 HD | `010048701995E000` | 20 |
| 100 | Pikmin 1 | `0100AA80194B0000` | 20 |
| 101 | Pikmin 2 | `0100D680194B2000` | 20 |
| 102 | Kirby Fighters 2 | `0100227010460000` | 20 |
| 103 | Hyrule Warriors: Definitive Edition | `0100AE00096EA000` | 20 |
| 104 | WarioWare: Move It! | `010045B018EC2000` | 20 |
| 105 | Super Mario Party Jamboree | `0100965017338000` | 20 |
| 106 | Mario & Sonic at the Olympic Games Tokyo 2020 | `010003000E146000` | 20 |
| 107 | Mario vs. Donkey Kong | `0100B99019412000` | 20 |
| 108 | Donkey Kong Country Returns HD | `01009D901BC56000` | 20 |
| 109 | Fitness Boxing | `0100E7300AAD4000` | 20 |
| 110 | Fitness Boxing 2: Rhythm & Exercise | `0100073011382000` | 20 |
| 111 | Clubhouse Games: 51 Worldwide Classics | `010047700D540000` | 20 |
| 112 | Game Builder Garage | `0100FA5010788000` | 20 |
| 113 | Big Brain Academy: Brain vs. Brain | `0100620012D6E000` | 20 |
| 114 | Go Vacation | `0100C1800A9B6000` | 20 |
| 115 | Just Dance 2020 | `0100DDB00DB38000` | 20 |
| 116 | Octopath Traveler | `010057D006492000` | 20 |
| 117 | Octopath Traveler II | `0100A3501946E000` | 21 |
| 118 | LIVE A LIVE | `0100CF801776C000` | 20 |
| 119 | Bravely Default II | `01006DC010326000` | 20 |
| 120 | Dragon Quest XI S: Echoes of an Elusive Age | `01006C300E9F0000` | 20 |
| 121 | Dragon Quest Builders 2 | `010042000A986000` | 20 |
| 122 | Ni no Kuni: Wrath of the White Witch | `0100E5600D446000` | 20 |
| 123 | Ni no Kuni II: Revenant Kingdom | `0100BE7013E06000` | 20 |
| 124 | Persona 4 Golden | `010062B01525C000` | 20 |
| 125 | Persona 3 Portable | `0100DCD01525A000` | 20 |
| 126 | Shin Megami Tensei V | `010063B012DC6000` | 20 |
| 127 | Shin Megami Tensei V: Vengeance | `010069C01AB82000` | 20 |
| 128 | Shin Megami Tensei III Nocturne HD Remaster | `01003B0012DC2000` | 20 |
| 129 | Tokyo Mirage Sessions #FE Encore | `0100A9400C9C2000` | 20 |
| 130 | Final Fantasy VII | `0100A5B00BDC6000` | 20 |
| 131 | Crisis Core -Final Fantasy VII- Reunion | `01004BC0166CC000` | 20 |
| 132 | Final Fantasy X/X-2 HD Remaster | `0100BC300CB48000` | 20 |
| 133 | Final Fantasy XII: The Zodiac Age | `0100EB100AB42000` | 20 |
| 134 | Final Fantasy XV Pocket Edition HD | `010068F00AA78000` | 20 |
| 135 | Bayonetta | `010076F0049A2000` | 22 |
| 136 | Bayonetta 2 | `01007960049A0000` | 22 |
| 137 | Bayonetta 3 | `01004A4010FEA000` | 24 |
| 138 | Bayonetta Origins: Cereza and the Lost Demon | `0100CF5010FEC000` | 22 |
| 139 | The Wonderful 101: Remastered | `0100B1300FF08000` | 24 |
| 140 | NBA 2K20 | `010026000E466000` | 22 |
| 141 | MLB The Show 23 | `0100913019170000` | 22 |
| 142 | EA SPORTS FC 24 | `0100BDB01A0E6000` | 22 |
| 143 | Tony Hawk's Pro Skater 1 + 2 | `0100CC00102B4000` | 24 |
| 144 | LEGO Star Wars: The Skywalker Saga | `010042D00D900000` | 20 |
| 145 | LEGO Marvel Super Heroes 2 | `0100D3A00409E000` | 75 |
| 146 | LEGO Jurassic World | `01001C100E772000` | 49 |
| 147 | LEGO Harry Potter Collection | `010052A00B5D2000` | 20 |
| 148 | LEGO CITY Undercover | `01003A30012C0000` | 27 |
| 149 | Mortal Kombat 11 | `0100F2200C984000` | 58 |
| 150 | Sid Meier’s Civilization VI | `010044500C182000` | 320 |
| 151 | Cities: Skylines - Nintendo Switch Edition | `0100D8800B87C000` | 135 |
| 152 | Tropico 6 | `0100FBE0113CC000` | 40 |
| 153 | Need for Speed Hot Pursuit Remastered | `010029B0118E8000` | 20 |
| 154 | Burnout Paradise Remastered | `0100DBF01000A000` | 22 |
| 155 | GRID Autosport | `0100DC800A602000` | 22 |
| 156 | WRC 8 FIA World Rally Championship | `010087800DCEA000` | 100 |
| 157 | MotoGP 24 | `010040401D564000` | 22 |
| 158 | Assassin's Creed III Remastered | `01007F600B134000` | 24 |
| 159 | Assassin's Creed: The Rebel Collection | `010044700DEB0000` | 22 |
| 160 | Crash Team Racing Nitro-Fueled | `0100F9F00C696000` | 25 |
| 161 | Crash Bandicoot N. Sane Trilogy | `0100D1B006744000` | 74 |
| 162 | Sonic Colors: Ultimate | `010040E0116B8000` | 47 |
| 163 | Sonic Superstars | `01008F701C074000` | 38 |
| 164 | SEGA AGES Sonic The Hedgehog | `010051F00AC5E000` | 28 |
| 165 | SEGA AGES Sonic The Hedgehog 2 | `01000D200C614000` | 30 |
| 166 | Demon Slayer: The Hinokami Chronicles | `0100309016E7A000` | 24 |
| 167 | Jujutsu Kaisen Cursed Clash | `010000B01A452000` | 24 |
| 168 | Naruto Shippuden: Ultimate Ninja Storm 4 | `010084D00CF5E000` | 22 |
| 169 | My Hero One's Justice 2 | `01007E700DBF6000` | 22 |
| 170 | One Piece Odyssey | `0100D9601A994000` | 27 |
| 171 | Guilty Gear -Strive- | `0100AB401F136000` | 39 |
| 172 | Samurai Shodown | `01002DF00F76C000` | 45 |
| 173 | Power Rangers: Battle for the Grid | `0100E1E00CF1A000` | 24 |
| 174 | Transformers: Battlegrounds | `01005E500E528000` | 30 |
| 175 | Hello Kitty Island Adventure | `010027901C89C000` | 32 |
| 176 | Moving Out | `0100C4C00E73E000` | 38 |
| 177 | Moving Out 2 | `010065D018172000` | 28 |
| 178 | Untitled Goose Game | `010082400BCC6000` | 25 |
| 179 | Baba Is You | `01002CD00A51C000` | 26 |
| 180 | Risk of Rain 2 | `010076D00E4BA000` | 205 |
| 181 | Spelunky 2 | `01007EC013ABC000` | 32 |
| 182 | Slay the Spire | `010026300BA4A000` | 46 |
| 183 | Vampire Survivors | `010089A0197E4000` | 243 |
| 184 | Balatro | `0100CD801CE5E000` | 31 |
| 185 | Dave the Diver | `010097F018538000` | 56 |
| 186 | Katana ZERO | `010029600D56A000` | 22 |
| 187 | Bloodstained: Ritual of the Night | `0100BF500207C000` | 30 |
| 188 | Castlevania Advance Collection | `0100B33014710000` | 33 |
| 189 | River City Girls 2 | `0100026016320000` | 28 |
| 190 | Scott Pilgrim vs. The World: The Game - Complete Edition | `0100394011C30000` | 27 |
| 191 | Okami HD | `0100276009872000` | 30 |
| 192 | Red Dead Redemption | `01007820196A6000` | 51 |
| 193 | Tomb Raider I-III Remastered | `010024601BB16000` | 284 |
| 194 | Borderlands: Game of the Year Edition | `010064800F66A000` | 31 |
| 195 | Wolfenstein II: The New Colossus | `01009040091E0000` | 80 |
| 196 | Metro 2033 Redux | `0100D4900E82C000` | 49 |
| 197 | Metro: Last Light Redux | `0100F0400E850000` | 49 |
| 198 | BioShock Remastered | `0100AD10102B2000` | 65 |
| 199 | Portal Knights | `0100437004170000` | 40 |
| 200 | Bridge Constructor Portal | `010016E004796000` | 20 |
| 201 | House Flipper | `0100CAE00EB02000` | 96 |
| 202 | PowerWash Simulator | `0100926016012000` | 100 |
| 203 | PICO PARK | `01004EA00DF70000` | 21 |
| 204 | Duck Game | `0100750001C70000` | 38 |
| 205 | Don't Starve Together | `010090100E334000` | 29 |
| 206 | Grounded | `01006F301AE9C000` | 45 |
| 207 | Subnautica | `0100429011144000` | 20 |
| 208 | Astroneer | `0100E63013E60000` | 116 |
| 209 | Slime Rancher: Plortable Edition | `0100B9C0148D0000` | 57 |
| 210 | Green Hell | `0100453012FEA000` | 68 |
| 211 | Dead by Daylight | `01004C400CF96000` | 318 |
| 212 | Outlast 2 | `0100DE70085E8000` | 24 |
| 213 | Little Nightmares Complete Edition | `01002FC00412C000` | 22 |
| 214 | Little Nightmares II | `010097100EDD6000` | 35 |
| 215 | Little Nightmares III | `010066101A55A000` | 44 |
| 216 | INSIDE | `0100D2D009028000` | 20 |
| 217 | LIMBO | `01009C8009026000` | 20 |
| 218 | Firewatch | `0100AC300919A000` | 20 |
| 219 | Life is Strange Remastered | `0100DC301186A000` | 22 |
| 220 | Life is Strange: True Colors | `0100500012AB4000` | 40 |
| 221 | Cat Quest III | `010088501B8F2000` | 30 |
| 222 | Minecraft Dungeons | `01006C100EC08000` | 104 |
| 223 | Mario & Luigi: Brothership | `01006D0017F7A000` | 26 |
| 224 | Princess Peach: Showtime! | `01007A3009184000` | 26 |
| 225 | Paper Mario: The Thousand-Year Door | `0100ECD018EBE000` | 26 |
| 226 | Paper Mario: The Origami King | `0100A3900C3E2000` | 26 |
| 227 | Miitopia | `01003DA010E8A000` | 26 |
| 228 | Pokemon Brilliant Diamond | `0100000011D90000` | 26 |
| 229 | Pokemon Shining Pearl | `010018E011D92000` | 26 |
| 230 | New Pokemon Snap | `0100F4300BF2C000` | 26 |
| 231 | Pokemon Mystery Dungeon: Rescue Team DX | `01003D200BAA2000` | 26 |
| 232 | Pokemon Champions | `01005B7008C52000` | 26 |
| 233 | Kirbys Dream Buffet | `0100A8E016236000` | 26 |
| 234 | Super Kirby Clash | `01003FB00C5A8000` | 26 |
| 235 | Fitness Boxing 3: Your Personal Trainer | `010020101F804000` | 26 |
| 236 | Fitness Boxing Fist of the North Star | `01008DA01A400000` | 26 |
| 237 | Fitness Boxing feat. HATSUNE MIKU | `01000C201FCDA000` | 26 |
| 238 | Nintendo Labo Toy-Con 01 Variety Kit | `0100C4B0034B2000` | 26 |
| 239 | Nintendo Labo Toy-Con 02 Robot Kit | `01009AB0034E0000` | 26 |
| 240 | Nintendo Labo Toy-Con 03 Vehicle Kit | `01001E9003502000` | 26 |
| 241 | Nintendo Labo Toy-Con 04 VR Kit | `0100165003504000` | 26 |
| 242 | Pokemon Cafe ReMix | `010072400E04A000` | 26 |
| 243 | THEATRHYTHM FINAL BAR LINE | `010081B01777C000` | 26 |
| 244 | WORLD OF FINAL FANTASY MAXIMA | `010072000BD32000` | 26 |
| 245 | Dragon Quest Monsters: The Dark Prince | `0100A77018EA0000` | 26 |
| 246 | Kingdom Hearts HD 1.5+2.5 ReMIX Cloud Version | `01000E6016A22000` | 26 |
| 247 | Kingdom Hearts HD 2.8 Final Chapter Prologue Cloud Version | `0100806016A24000` | 26 |
| 248 | Kingdom Hearts III + Re Mind Cloud Version | `0100479016834000` | 26 |
| 249 | Kingdom Hearts Melody of Memory | `01005D2011EA8000` | 26 |
| 250 | Brigandine The Legend of Runersia | `010011000EA7A000` | 26 |
| 251 | Disgaea 1 Complete | `01004B100AF18000` | 26 |
| 252 | Disgaea 6 Defiance of Destiny | `0100ABC013136000` | 26 |
| 253 | Monster Hunter Generations Ultimate | `0100770008DD8000` | 26 |
| 254 | Star Ocean First Departure R | `0100EBF00E702000` | 26 |
| 255 | Triangle Strategy | `0100CC80140F8000` | 26 |
| 256 | Baldur Gate and Baldur Gate II Enhanced Editions | `010010A00DA48000` | 26 |
| 257 | Baldurs Gate Dark Alliance | `0100FD1014726000` | 26 |
| 258 | Just Dance 2017 | `0100BCE000598000` | 26 |
| 259 | Just Dance 2018 | `0100A0500348A000` | 26 |
| 260 | Just Dance 2019 | `010075600AE96000` | 26 |
| 261 | Just Dance 2021 | `0100BF9011B52000` | 26 |
| 262 | Just Dance 2022 | `0100EA6014BB8000` | 26 |
| 263 | EA SPORTS FIFA 23 Legacy Edition | `01001C8016B4E000` | 26 |
| 264 | NBA 2K21 | `0100E24011D1E000` | 26 |
| 265 | NBA 2K22 | `0100B94014F8E000` | 26 |
| 266 | NBA 2K23 | `0100ACA017E4E000` | 26 |
| 267 | NBA 2K24 | `010006501A8D8000` | 26 |
| 268 | NBA 2K25 | `0100DFF01ED44000` | 26 |
| 269 | PGA TOUR 2K21 | `010053401147C000` | 26 |
| 270 | Overwatch 2 | `0100F8600E21E000` | 26 |
| 271 | Assassins Creed The Ezio Collection | `0100670014482000` | 26 |
| 272 | Street Fighter 30th Anniversary Collection | `0100024008310000` | 26 |
| 273 | SIGNALIS | `0100307018934000` | 26 |
| 274 | GRIS | `0100E1700C31C000` | 26 |
| 275 | A Short Hike | `01004890117B2000` | 26 |
| 276 | The Stanley Parable Ultra Deluxe | `010029300E5C4000` | 26 |
| 277 | Braid Anniversary Edition | `010089C00B026000` | 26 |
| 278 | The Case of the Golden Idol | `0100D1C01B5B6000` | 26 |
| 279 | Return of the Obra Dinn | `010032E00E6E2000` | 26 |
| 280 | Griftlands | `0100E49013514000` | 26 |
| 281 | PICROSS S | `0100BA0003EEA000` | 26 |
| 282 | PICROSS S+ | `0100D7B01AE58000` | 26 |
| 283 | PICROSS S2 | `0100C9600A88E000` | 26 |
| 284 | PICROSS S3 | `010079200D330000` | 26 |
| 285 | PICROSS S4 | `0100C250115DC000` | 26 |
| 286 | PICROSS S5 | `0100AC30133EC000` | 26 |
| 287 | PICROSS S6 | `010025901432A000` | 26 |
| 288 | PICROSS S7 | `01009B2016104000` | 26 |
| 289 | PICROSS S8 | `01002CE017D26000` | 26 |
| 290 | PICROSS S9 | `010021A0197BA000` | 26 |
| 291 | PICROSS S Capcom Classics Edition | `01009AD023F90000` | 26 |
| 292 | PICROSS S Doraemon Edition | `01002B901FA74000` | 26 |
| 293 | PICROSS S Genesis and Master System Edition | `010089701567A000` | 26 |
| 294 | PICROSS S Konami Antiques Edition | `0100D730260E4000` | 26 |
| 295 | PICROSS S Namco Legendary Edition | `010015101DEF8000` | 26 |
| 296 | PICROSS S SNK Classics and NeoGeo Edition | `0100122023706000` | 26 |
| 297 | GrimGrimoire OnceMore | `0100189018E56000` | 26 |
| 298 | LEGO 2K Drive | `0100739018020000` | 26 |
| 299 | Subnautica: Below Zero | `010014C011146000` | 26 |
| 300 | Apex Legends | `0100D9500FC66000` | 26 |
| 301 | Dauntless | `0100B9500D1B0000` | 26 |
| 302 | The Turing Test | `0100EA100F516000` | 26 |
| 303 | Shantae | `0100430013120000` | 26 |
| 304 | Bloodstained: Curse of the Moon | `01004B800AF5A000` | 26 |
| 305 | Bloodstained: Curse of the Moon 2 | `01004680124E6000` | 26 |
| 306 | ASTRAL CHAIN | `01007300020FA000` | 26 |
| 307 | Oddmar | `01001F100FA04000` | 26 |
| 308 | PICROSS LORD OF THE NAZARICK | `010012100E8DC000` | 26 |
| 309 | Risk of Rain | `0100AAA00ACBE000` | 26 |
| 310 | Owlboy | `0100BC2004FF4000` | 26 |
| 311 | Wonder Boy: The Dragon's Trap | `0100A6300150C000` | 26 |
| 312 | Venba | `01002F20193C6000` | 26 |
| 313 | Keep Talking and Nobody Explodes | `01008D400A584000` | 26 |
| 314 | Bad North | `0100E98006F22000` | 26 |
| 315 | Cooking Simulator | `01001E400FD58000` | 20 |
| 316 | This War of Mine: Complete Edition | `0100A8700BC2A000` | 59 |
| 317 | Plague Inc: Evolved | `01000CE00CBB8000` | 250 |
| 318 | Overcooked! 2 | `01006FD0080B2000` | 54 |
| 319 | ARK: Survival Evolved | `0100D4A00B284000` | 32 |
| 320 | Don't Starve: Nintendo Switch Edition | `0100751007ADA000` | 113 |
| 321 | Until Dawn | `01001E1025697001` | 29 |
| 322 | 20 Minutes Till Dawn | `0100212019FB6000` | 34 |
| 323 | Hollow Knight: Silksong | `010013C00E930000` | 52 |
| 324 | Sonic X Shadow Generations | `01005EA01C0FC000` | 40 |
| 325 | Sonic Forces | `01001270012B6000` | 48 |
| 326 | Team Sonic Racing | `010092B0091D0000` | 51 |
| 327 | Sonic Origins / Origins Plus | `01009FB016286000` | 36 |
| 328 | Sonic Racing CrossWorlds | `01006E001823C000` | 44 |
| 329 | FINAL FANTASY (Pixel Remaster) | `01000EA014150000` | 24 |
| 330 | FINAL FANTASY II (Pixel Remaster) | `01006B7014156000` | 28 |
| 331 | FINAL FANTASY III (Pixel Remaster) | `01002E2014158000` | 31 |
| 332 | FINAL FANTASY IV (Pixel Remaster) | `01004B301415A000` | 30 |
| 333 | FINAL FANTASY V (Pixel Remaster) | `0100AA201415C000` | 39 |
| 334 | FINAL FANTASY VI (Pixel Remaster) | `0100AA001415E000` | 37 |
| 335 | FINAL FANTASY IX | `01007EF00B094000` | 85 |
| 336 | Dragon Quest Builders | `010008900705C000` | 20 |
| 337 | Dragon Quest Treasures | `010049B017774000` | 50 |
| 338 | Dragon Quest III HD-2D Remake | `01003E601E324000` | 42 |
| 339 | NieR Automata The End of YoRHa Edition | `010056B015FE8000` | 47 |
| 340 | Persona 4 Arena Ultimax | `010075A016A3A000` | 51 |
| 341 | Ys VIII Lacrimosa of Dana | `01007F200B0C0000` | 54 |
| 342 | Ys IX Monstrum Nox | `0100E390124D8000` | 54 |
| 343 | Ys Origin | `0100F90010882000` | 46 |
| 344 | Trails of Cold Steel III | `01005420101DA000` | 53 |
| 345 | Trails of Cold Steel IV | `0100D3C010DE8000` | 53 |
| 346 | Trails in the Sky 1st Chapter | `01002C9022770000` | 43 |
| 347 | Trails in the Sky 2nd Chapter | `01007A2027548000` | 49 |
| 348 | Trails from Zero | `01001920156C2000` | 49 |
| 349 | Trails to Azure | `0100FBE015910000` | 57 |
| 350 | Trails through Daybreak | `010040C01D248000` | 53 |
| 351 | Trails through Daybreak II | `0100F6701FED4000` | 53 |
| 352 | Trails into Reverie | `01008CB0156BC000` | 53 |
| 353 | Romancing SaGa 2 | `01001F600829A000` | 42 |
| 354 | Romancing SaGa 2 Revenge of the Seven | `010045301B86C000` | 51 |
| 355 | SaGa SCARLET GRACE AMBITIONS | `010003A00D0B4000` | 56 |
| 356 | Disgaea 4 Complete+ | `0100A9800E9B4000` | 51 |
| 357 | Disgaea 5 Complete | `01005700031AE000` | 51 |
| 358 | Disgaea 7 Vows of the Virtueless | `0100A7801A530000` | 50 |
| 359 | Rune Factory 3 Special | `0100E000191B4000` | 38 |
| 360 | Rune Factory 4 Special | `010051D00E3A4000` | 38 |
| 361 | Rune Factory 5 | `01002F7013224000` | 47 |
| 362 | Rune Factory Guardians of Azuma | `010022A02008C000` | 81 |
| 363 | Wizardry Proving Grounds of the Mad Overlord | `010033F01AD2E000` | 28 |
| 364 | Labyrinth of Refrain Coven of Dusk | `010058500B3E0000` | 57 |
| 365 | Fairy Fencer F Advent Dark Force | `010002300C632000` | 30 |
| 366 | Fairy Fencer F Refrain Chord | `0100F760195F2000` | 47 |
| 367 | Suikoden I&II HD Remaster | `01004BD017080000` | 56 |
| 368 | Star Ocean Second Story R | `010065301A2E0000` | 51 |
| 369 | Sea of Stars | `01008C0016544000` | 54 |
| 370 | The Last Spell | `0100F7101906A000` | 94 |
| 371 | Baldurs Gate Dark Alliance II | `0100A61018680000` | 26 |
| 372 | Hogwarts Legacy | `0100F7E00C70E000` | 45 |
| 373 | Prince of Persia The Lost Crown | `0100210019428000` | 40 |
| 374 | Dark Souls Remastered | `01004AB00A260000` | 41 |
| 375 | Resident Evil | `010050F00BC1A000` | 44 |
| 376 | Resident Evil 0 | `010097000BC10000` | 47 |
| 377 | Resident Evil 5 | `010018100CD46000` | 70 |
| 378 | Resident Evil 6 | `01002A000CD48000` | 70 |
| 379 | Resident Evil Revelations | `0100643002136000` | 50 |
| 380 | Resident Evil Revelations 2 | `010095300212A000` | 43 |
| 381 | Resident Evil 3 Cloud | `0100FCE0185B4000` | 32 |
| 382 | Resident Evil 7 biohazard Cloud | `0100E890185B6000` | 58 |
| 383 | Borderlands The Pre-Sequel | `010007400FF24000` | 63 |
| 384 | BioShock Infinite The Complete Edition | `0100D560102C8000` | 80 |
| 385 | Yakuza Kiwami | `0100C9801FEE6000` | 55 |
| 386 | Phoenix Wright Ace Attorney Trilogy | `0100CB000A142000` | 30 |
| 387 | The Great Ace Attorney Chronicles | `010036E00FB20000` | 30 |
| 388 | Mega Man 11 | `0100B0C0086B0000` | 50 |
| 389 | Mega Man Legacy Collection | `01002D4007AE0000` | 24 |
| 390 | Mega Man Legacy Collection 2 | `0100842008EC4000` | 21 |
| 391 | Mega Man X Legacy Collection | `01005C60086BE000` | 52 |
| 392 | Mega Man X Legacy Collection 2 | `01005250086C4000` | 52 |
| 393 | Mega Man Zero/ZX Legacy Collection | `010025C00D410000` | 37 |
| 394 | Grand Theft Auto III Definitive Edition | `0100C3C012718000` | 29 |
| 395 | Grand Theft Auto Vice City Definitive Edition | `0100182014022000` | 34 |
| 396 | Grand Theft Auto San Andreas Definitive Edition | `010065A014024000` | 35 |
| 397 | LEGO Horizon Adventures | `010073C01AF34000` | 23 |
| 398 | Inscryption | `010027F017B12000` | 40 |
| 399 | TUNIC | `0100DA801624E000` | 36 |
| 400 | ANIMAL WELL | `010020D01AD24000` | 20 |
| 401 | Lorelei and the Laser Eyes | `01009F701688E000` | 20 |
| 402 | Outer Wilds | `01003DC0144B6000` | 31 |
| 403 | Spiritfarer | `0100BD400DC52000` | 39 |
| 404 | Unpacking | `0100701015846000` | 25 |
| 405 | Hyper Light Drifter Special Edition | `01003B200B372000` | 23 |
| 406 | Into the Breach | `010057D00B612000` | 70 |
| 407 | Wargroove | `01000F0002BB6000` | 23 |
| 408 | Wargroove 2 | `0100AD401A2F0000` | 23 |
| 409 | Puyo Puyo Tetris 2 | `010038E011940000` | 43 |
| 410 | Human Fall Flat | `01000CA004DCA000` | 155 |
| 411 | Yooka-Laylee | `0100F110029C8000` | 35 |
| 412 | Yooka-Laylee and the Impossible Lair | `010022F00DA66000` | 47 |
| 413 | Skul The Hero Slayer | `0100ACF013E9A000` | 101 |
| 414 | Brotato | `01002EF01A316000` | 200 |
| 415 | Cassette Beasts | `010066F01A0E0000` | 123 |
| 416 | Coromon | `010048D014322000` | 80 |
| 417 | Nexomon Extinction | `01005A5011A44000` | 56 |
| 418 | Monster Crown | `0100E0600C78E000` | 33 |
| 419 | Hades II | `0100A00019DE0000` | 50 |
| 420 | Cris Tales | `0100B0400EBC4000` | 46 |
| 421 | WRC 9 | `01001A0011798000` | 43 |
| 422 | WRC 10 | `01003E3014AFE000` | 46 |
| 423 | WRC Generations | `0100041018810000` | 44 |
| 424 | VA-11 Hall-A | `010086500D3C8000` | 34 |
| 425 | Monster Hunter Stories | `010069301B1D4000` | 50 |
| 426 | Tactics Ogre: Reborn | `0100E12013C1A000` | 34 |
| 427 | OCTOPATH TRAVELER 0 | `01005270232F2000` | 37 |
| 428 | Valkyria Chronicles | `0100CAF00B744000` | 20 |
| 429 | Valkyria Chronicles 4 | `01005C600AC68000` | 36 |
| 430 | LOST SPHEAR | `010077B0038B2000` | 50 |
| 431 | Romancing SaGa 3 | `0100D0400D27A000` | 41 |
| 432 | Romancing SaGa -Minstrel Song- Remastered | `01004A6017E8A000` | 46 |
| 433 | Trials of Mana | `0100D7800E9E0000` | 44 |
| 434 | SaGa Frontier Remastered | `0100A51013530000` | 46 |
| 435 | SaGa Frontier 2 Remastered | `0100F2301BD98000` | 44 |
| 436 | FINAL FANTASY TACTICS - The Ivalice Chronicles | `010038B015560000` | 50 |
| 437 | BioShock 2 Remastered | `01002620102C6000` | 53 |
| 438 | EA SPORTS FC 25 | `010054E01D878000` | 39 |
| 439 | Mortal Kombat 1 | `01006560184E6000` | 50 |
| 440 | Batman: Arkham Asylum | `0100E870163CA000` | 47 |
| 441 | Batman: Arkham City | `01003F00163CE000` | 64 |
| 442 | Batman: Arkham Knight | `0100ACD0163D0000` | 113 |
| 443 | Ghostbusters: The Video Game Remastered | `0100EAE00D9EC000` | 40 |
| 444 | Ghostbusters: Spirits Unleashed Ecto Edition | `01005D2016934000` | 51 |
| 445 | LEGO Bricktales | `0100B12017F0A000` | 21 |
| 446 | Kingdom Come Deliverance: Royal Edition | `0100650018FE0000` | 82 |
| 447 | The Outer Worlds | `0100626011656000` | 68 |
| 448 | Fallout Shelter | `010043500A17A000` | 35 |
| 449 | Minecraft Legends | `01007C6012CC8000` | 40 |
| 450 | No Man's Sky | `0100853015E86000` | 27 |
| 451 | Warframe | `0100FEE00A64E000` | 193 |
| 452 | The Talos Principle: Deluxe Edition | `010092A00D43C000` | 40 |
| 453 | Portal 2 | `0100ABD01785C000` | 51 |
| 454 | Tetris Effect: Connected | `0100DE501433A000` | 43 |
| 455 | SUPER BOMBERMAN R 2 | `0100B87017D94000` | 39 |
| 456 | Neon White | `0100B9201406A000` | 63 |
| 457 | The Pathless | `0100D5501522C000` | 43 |
| 458 | Ary and the Secret of Seasons | `0100C2500CAB6000` | 38 |
| 459 | Trine 4: The Nightmare Prince | `010055E00CA68000` | 39 |
| 460 | Puyo Puyo Tetris | `010073C001D5E000` | 42 |
| 461 | Shantae: Half-Genie Hero | `0100AE0003424000` | 65 |
| 462 | Shantae and the Seven Sirens | `0100EB901040A000` | 40 |
| 463 | Shantae and the Pirate's Curse | `0100EFD00A4FA000` | 44 |
| 464 | Shantae Advance: Risky Revolution | `010031101D400000` | 33 |
| 465 | Shantae: Risky's Revenge - Director's Cut | `0100ADA012370000` | 26 |
| 466 | Victor Vran Overkill Edition | `0100E81007A06000` | 90 |
| 467 | Warhammer 40,000: Boltgun | `01005FD017E60000` | 21 |
| 468 | Warhammer 40,000: Mechanicus | `0100C6000EEA8000` | 34 |
| 469 | DAEMON X MACHINA | `0100B6400CA56000` | 61 |
| 470 | Raji: An Ancient Epic | `010010B00DDA2000` | 21 |
| 471 | Defense Grid 2 | `010061300BBF8000` | 65 |
| 472 | DUSK | `01007740160D4000` | 30 |
| 473 | Rogue Legacy 2 | `01007DA0134C0000` | 39 |
| 474 | Dead Estate | `01009DC017B4E000` | 200 |
| 475 | Void Bastards | `0100D010113A8000` | 24 |
| 476 | Dungreed | `0100FAD00C2AA000` | 24 |
| 477 | Backpack Hero | `0100B6301ABD6000` | 35 |
| 478 | Shogun Showdown | `010096F01B4D8000` | 36 |
| 479 | Bastion | `010038600B27E000` | 24 |
| 480 | Transistor | `0100BE500BEA2000` | 33 |
| 481 | The Messenger | `0100DC300AC78000` | 48 |
| 482 | Axiom Verge | `0100052004384000` | 29 |
| 483 | Axiom Verge 2 | `01002FC010240000` | 28 |
| 484 | RUINER | `01006EC00F2CC000` | 33 |
| 485 | Furi | `01009D3008D20000` | 33 |
| 486 | Salt and Sanctuary | `0100D250083B4000` | 37 |
| 487 | Blasphemous | `0100698009C6E000` | 45 |
| 488 | Blasphemous 2 | `010040801A4C8000` | 60 |
| 489 | Greak: Memories of Azur | `010045E012ECE000` | 24 |
| 490 | The Swords of Ditto: Mormo's Curse | `010037D00D568000` | 20 |
| 491 | Eastward | `010071B00F63A000` | 30 |
| 492 | Dinkum | `0100A5A020D5E000` | 25 |
| 493 | Garden Story | `0100B4D012490000` | 21 |
| 494 | Lil Gator Game | `0100100016FB0000` | 41 |
| 495 | Monster Sanctuary | `0100A0F00DA68000` | 41 |
| 496 | Siralim Ultimate | `0100AC1019560000` | 320 |
| 497 | Wobbly Life | `010039501F11C000` | 68 |
| 498 | Q.U.B.E. 2 | `010023600AA34000` | 29 |
| 499 | Mini Metro | `0100091008272000` | 73 |
| 500 | Mini Motorways | `01000D3015088000` | 170 |
| 501 | Dorfromantik | `01007F2019132000` | 85 |
| 502 | Stacklands | `01008B701BEE8000` | 36 |
| 503 | Northgard | `0100A9E00D97A000` | 289 |

## Checklist sources

Sources used for the non-Steam IGN-style checklist goals. Steam ports
are deliberately omitted because they mirror real Steam achievements.

| Game | Slug | Source |
|---|---|---|
| 1-2-Switch | `12SWITCH` | https://www.ign.com/wikis/1-2switch |
| A Short Hike | `SHORT` | https://steamcommunity.com/stats/1055540/achievements/?l=english |
| ARMS | `ARMS` | https://www.ign.com/wikis/arms |
| ASTRAL CHAIN | `ASTRAL` | https://www.ign.com/wikis/astral-chain/Walkthrough |
| Advance Wars 1+2 Re-Boot Camp | `ADVANCEWARS` | https://www.ign.com/wikis/advance-wars-reboot-camp |
| Animal Crossing New Horizons | `ACNH` | https://www.ign.com/games/animal-crossing-new-horizons/checklists |
| Apex Legends | `APEX` | https://www.ign.com/wikis/apex-legends |
| Assassin's Creed III Remastered | `AC3` | https://mapgenie.io/assassins-creed-3/checklist |
| Assassin's Creed: The Rebel Collection | `ACREBEL` | https://www.ign.com/wikis/assassins-creed-4-black-flag |
| Assassins Creed The Ezio Collection | `ACEZIO` | https://gamefaqs.gamespot.com/xboxone/196141-assassins-creed-the-ezio-collection/achievements |
| Bad North | `BADNORTH` | https://steamcommunity.com/stats/688420/achievements |
| Baldur Gate and Baldur Gate II Enhanced Editions | `BGE` | https://www.ign.com/wikis/baldur-gate-enhanced-edition |
| Baldurs Gate Dark Alliance | `BGD` | https://www.ign.com/wikis/baldurs-gate-dark-alliance |
| Bayonetta | `BAYONETTA` | https://www.ign.com/wikis/bayonetta/Achievements_and_Trophies |
| Bayonetta 2 | `BAYONETTA2` | https://www.ign.com/wikis/bayonetta-2/Walkthrough |
| Bayonetta 3 | `BAYONETTA3` | https://www.ign.com/wikis/bayonetta-3/Collectibles |
| Bayonetta Origins: Cereza and the Lost Demon | `BAYORIGINS` | https://samurai-gamers.com/bayonetta-origins-cereza-and-the-lost-demon/all-collectibles-list-and-guides/ |
| Big Brain Academy: Brain vs. Brain | `BRAIN` | https://www.ign.com/games/big-brain-academy-brain-vs-brain |
| Bloodstained: Curse of the Moon | `CURSE1` | https://steamcommunity.com/stats/838310/achievements |
| Bloodstained: Curse of the Moon 2 | `CURSE2` | https://steamcommunity.com/stats/1257360/achievements |
| Bloodstained: Ritual of the Night | `BLOODSTAINED` | https://www.ign.com/wikis/bloodstained-ritual-of-the-night/Achievements_and_Trophies |
| Borderlands: Game of the Year Edition | `BORDERLANDS` | https://steamcommunity.com/stats/729040/achievements/?l=english |
| Braid Anniversary Edition | `BRAID` | https://steamcommunity.com/stats/499180/achievements/?l=english |
| Bravely Default II | `BRAVELY` | https://www.ign.com/wikis/bravely-default-2 |
| Brigandine The Legend of Runersia | `BRIG` | https://www.ign.com/games/brigandine-the-legend-of-runersia |
| Burnout Paradise Remastered | `BURNOUT` | https://www.ign.com/wikis/burnout-paradise/Smashes_Locations_and_Maps |
| Captain Toad Treasure Tracker | `TOAD` | https://www.ign.com/wikis/captain-toad-treasure-tracker/Super_Gems |
| Castlevania Advance Collection | `CASTLEVANIA` | https://www.ign.com/wikis/castlevania-advance-collection-collection |
| Clubhouse Games: 51 Worldwide Classics | `CLUBHOUSE` | https://www.nintendo.com/my/switch/as7t/index.html |
| Crash Team Racing Nitro-Fueled | `CTR` | https://www.ign.com/wikis/crash-team-racing-nitro-fueled/Adventure_Mode_Explained |
| Crisis Core -Final Fantasy VII- Reunion | `CRISISCORE` | https://www.ign.com/wikis/crisis-core-final-fantasy-vii |
| Dauntless | `DAUNTLESS` | https://www.ign.com/wikis/dauntless |
| Deltarune | `DELTARUNE` | https://www.ign.com/wikis/deltarune |
| Demon Slayer: The Hinokami Chronicles | `DSLAYER` | https://www.ign.com/wikis/demon-slayer-the-hinokami-chronicles/Achievements_and_Trophies |
| Detective Pikachu Returns | `DETECTIVE` | https://www.ign.com/wikis/detective-pikachu-returns |
| Diablo III Eternal Collection | `DIABLO3` | https://www.ign.com/wikis/diablo-3/Achievements_and_Trophies |
| Disgaea 1 Complete | `DISGAEA1` | https://www.ign.com/search?q=Disgaea%201%20Complete |
| Disgaea 6 Defiance of Destiny | `DISGAEA6` | https://www.ign.com/search?q=Disgaea%206%20Defiance%20of%20Destiny |
| Don't Starve Together | `DST` | https://dontstarve.wiki.gg/wiki/Don%27t_Starve_Together |
| Donkey Kong Country Returns HD | `DKCR` | https://www.ign.com/wikis/donkey-kong-country-returns/100_Percent_Completion_Checklist |
| Donkey Kong Country Tropical Freeze | `DKC` | https://www.ign.com/wikis/donkey-kong-country-tropical-freeze/100_Percent_Completion_Checklist |
| Dragon Quest Builders 2 | `DQB2` | https://en.wikipedia.org/wiki/Dragon_Quest_Builders_2 |
| Dragon Quest Monsters: The Dark Prince | `DQM` | https://www.ign.com/search?q=Dragon%20Quest%20Monsters%20The%20Dark%20Prince |
| Dragon Quest XI S: Echoes of an Elusive Age | `DQ11S` | https://www.ign.com/wikis/dragon-quest-xi |
| EA SPORTS FC 24 | `FC24` | https://www.ign.com/wikis/ea-sports-fc-24 |
| EA SPORTS FIFA 23 Legacy Edition | `FIFA23` | https://gamefaqs.gamespot.com/xboxone/373102-fifa-23/achievements |
| Final Fantasy VII | `FF7` | https://www.ign.com/wikis/final-fantasy-vii |
| Final Fantasy X/X-2 HD Remaster | `FFX` | https://www.ign.com/wikis/final-fantasy-x |
| Final Fantasy XII: The Zodiac Age | `FF12` | https://www.ign.com/wikis/final-fantasy-xii |
| Final Fantasy XV Pocket Edition HD | `FF15P` | https://en.wikipedia.org/wiki/Final_Fantasy_XV:_Pocket_Edition |
| Fire Emblem Engage | `FE_ENGAGE` | https://www.ign.com/wikis/fire-emblem-engage |
| Fire Emblem Three Houses | `FE3H` | https://www.ign.com/wikis/fire-emblem-three-houses |
| Fire Emblem Warriors | `FEW` | https://www.ign.com/wikis/fire-emblem-warriors |
| Fire Emblem Warriors: Three Hopes | `FE3HOPES` | https://www.ign.com/wikis/fire-emblem-three-hopes |
| Fitness Boxing | `FITBOX` | https://en.wikipedia.org/wiki/Fitness_Boxing |
| Fitness Boxing 2: Rhythm & Exercise | `FITBOX2` | https://www.nintendo.com/en-gb/Games/Nintendo-Switch-games/Fitness-Boxing-2-Rhythm-Exercise-1843189.html |
| Fitness Boxing 3: Your Personal Trainer | `FITBOX3` | https://www.nintendo.com/us/store/products/fitness-boxing-3-your-personal-trainer-switch/ |
| Fitness Boxing Fist of the North Star | `FITBOX_FN` | https://www.ign.com/games/fitness-boxing-fist-of-the-north-star |
| Fitness Boxing feat. HATSUNE MIKU | `FITBOX_MIKU` | https://www.ign.com/games/fitness-boxing-feat-hatsune-miku |
| GRID Autosport | `GRID` | https://www.ign.com/articles/2014/06/24/grid-autosport-review |
| GRIS | `GRIS` | https://steamcommunity.com/stats/683320/achievements/?l=english |
| Game Builder Garage | `GBG` | https://www.nintendo.com/ph/switch/awux/lesson/index.html |
| Go Vacation | `GOVACATION` | https://es.ign.com/go-vacation-nintendo-switch/136959/review/analisis-de-go-vacation-para-nintendo-switch |
| Griftlands | `GRIFT` | https://steamcommunity.com/stats/601840/achievements/?l=english |
| GrimGrimoire OnceMore | `GRIM` | https://gamefaqs.gamespot.com/switch/364622-grimgrimoire-oncemore/faqs |
| Hello Kitty Island Adventure | `HELLOKITTY` | https://steamcommunity.com/stats/2495100/achievements/?l=english |
| Hyrule Warriors Age of Calamity | `AOC` | https://zeldacentral.com/games/hyrule-warriors-age-of-calamity/100-completion-checklist/ |
| Hyrule Warriors: Definitive Edition | `HRW` | https://www.ign.com/wikis/hyrule-warriors |
| Jujutsu Kaisen Cursed Clash | `JJK` | https://www.playstationtrophies.org/game/jujustu-kaisen-cursed-clash/trophies |
| Just Dance 2017 | `JD2017` | https://www.ign.com/search?q=Just%20Dance%202017 |
| Just Dance 2018 | `JD2018` | https://www.ign.com/search?q=Just%20Dance%202018 |
| Just Dance 2019 | `JD2019` | https://www.ign.com/search?q=Just%20Dance%202019 |
| Just Dance 2020 | `JUSTDANCE` | https://en.wikipedia.org/wiki/Just_Dance_2020 |
| Just Dance 2021 | `JD2021` | https://www.ign.com/search?q=Just%20Dance%202021 |
| Just Dance 2022 | `JD2022` | https://www.ign.com/search?q=Just%20Dance%202022 |
| Keep Talking and Nobody Explodes | `KTANE` | https://steamcommunity.com/stats/341800/achievements |
| Kingdom Hearts HD 1.5+2.5 ReMIX Cloud Version | `KH15` | https://www.ign.com/wikis/kingdom-hearts-hd-15-remix |
| Kingdom Hearts HD 2.8 Final Chapter Prologue Cloud Version | `KH28` | https://www.ign.com/wikis/kingdom-hearts-hd-2-8-final-chapter-prologue |
| Kingdom Hearts III + Re Mind Cloud Version | `KH3` | https://www.ign.com/wikis/kingdom-hearts-3 |
| Kingdom Hearts Melody of Memory | `KHMEL` | https://www.ign.com/games/kingdom-hearts-melody-of-memory |
| Kirby Fighters 2 | `KIRBYFIGHT` | https://wikirby.com/wiki/100%25_completion |
| Kirby Return to Dream Land Deluxe | `KIRBY_RTDL` | https://www.ign.com/wikis/kirbys-return-to-dream-land/Energy_Spheres |
| Kirby Star Allies | `KIRBY_SA` | https://www.ign.com/wikis/kirby-switch |
| Kirby and the Forgotten Land | `KIRBY_FL` | https://www.ign.com/wikis/kirby-and-the-forgotten-land/How_to_Unlock_Everything |
| Kirbys Dream Buffet | `KIRBY_BUFFET` | https://www.ign.com/games/kirbys-dream-buffet |
| LEGO 2K Drive | `LEGO2K` | https://www.ign.com/wikis/lego-2k-drive |
| LEGO CITY Undercover | `LEGOCITY` | https://www.ign.com/wikis/lego-city-undercover/Gold_Bricks |
| LIVE A LIVE | `LIVEALIVE` | https://www.ign.com/wikis/live-a-live |
| Life is Strange Remastered | `LIS` | https://steamcommunity.com/stats/1265920/achievements/?l=english |
| Luigi's Mansion 2 HD | `LM2HD` | https://www.ign.com/wikis/luigis-mansion-2/100%25_Completion_Tracker |
| Luigis Mansion 3 | `LM3` | https://www.ign.com/wikis/luigis-mansion-3 |
| MLB The Show 23 | `MLB23` | https://primagames.com/tips/mlb-the-show-23-trophies-and-achievements-listed |
| Mario & Luigi: Brothership | `MARIOLUIGI` | https://www.ign.com/wikis/mario-and-luigi-brothership/Walkthrough |
| Mario & Sonic at the Olympic Games Tokyo 2020 | `MARIOSONIC` | https://www.nintendolife.com/news/2019/10/guide_mario_and_sonic_at_the_olympic_games_tokyo_2020_all_events_story_mode_minigames_and_characters |
| Mario + Rabbids Kingdom Battle | `RABBIDS_KB` | https://www.ign.com/wikis/mario-rabbids-kingdom-battle/Collectible_Chests |
| Mario + Rabbids Sparks of Hope | `RABBIDS_H` | https://www.ign.com/wikis/mario-rabbids-sparks-of-hope/Mario%2BRabbids_Sparks_of_Hope_Sparks_List_and_Where_to_Find_All_Sparks |
| Mario Golf Super Rush | `MGOLF` | https://www.ign.com/wikis/mario-golf-super-rush/Unlockables |
| Mario Kart 8 Deluxe | `MK8D` | https://www.ign.com/wikis/mario-kart-8/Deluxe_DLC_-_Booster_Course_Pass |
| Mario Kart Live Home Circuit | `MKLIVE` | https://www.ign.com/wikis/mario-kart-live-home-circuit |
| Mario Party Superstars | `MPSS` | https://www.ign.com/wikis/mario-party-superstars/All_Minigames |
| Mario Strikers Battle League | `STRIKERS` | https://www.ign.com/wikis/mario-strikers-battle-league |
| Mario Tennis Aces | `MTENNIS` | https://www.ign.com/wikis/mario-tennis-aces |
| Mario vs. Donkey Kong | `MVS` | https://www.ign.com/wikis/mario-vs-donkey-kong/Walkthrough |
| Metroid Dread | `DREAD` | https://www.ign.com/wikis/metroid-dread |
| Metroid Prime 4: Beyond | `METROID4` | https://www.ign.com/wikis/metroid-prime-4-beyond/100%25_Completion_Guide |
| Metroid Prime Remastered | `PRIME` | https://www.ign.com/wikis/metroid-prime |
| Miitopia | `MIITOPIA` | https://www.ign.com/wikis/miitopia/Walkthrough |
| Minecraft | `MINECRAFT` | https://www.ign.com/wikis/minecraft/Achievements |
| Monster Hunter Generations Ultimate | `MHGU` | https://www.ign.com/wikis/monster-hunter-generations |
| MotoGP 24 | `MOTOGP24` | https://racinggames.gg/article/motogp-24-trophies-and-achievements-complete-guide |
| My Hero One's Justice 2 | `MHA2` | https://www.playstationtrophies.org/game/my-hero-ones-justice-2/trophies |
| NBA 2K20 | `NBA2K` | https://www.ign.com/wikis/nba-2k20 |
| NBA 2K21 | `NBA21` | https://steamcommunity.com/stats/1225330/achievements/?l=english |
| NBA 2K22 | `NBA22` | https://steamcommunity.com/stats/1644960/achievements/?l=english |
| NBA 2K23 | `NBA23` | https://steamcommunity.com/stats/1919590/achievements/?l=english |
| NBA 2K24 | `NBA24` | https://steamcommunity.com/stats/2338770/achievements/?l=english |
| NBA 2K25 | `NBA25` | https://steamcommunity.com/stats/2878980/achievements/?l=english |
| Naruto Shippuden: Ultimate Ninja Storm 4 | `NARUTO4` | https://www.ign.com/wikis/naruto-shippuden-ultimate-ninja-storm-4/Memory_Fragments |
| New Pokemon Snap | `POKESNAP` | https://www.ign.com/wikis/new-pokemon-snap/Walkthrough_-_Course_Guides |
| New Super Mario Bros U Deluxe | `NSMBU` | https://www.ign.com/wikis/new-super-mario-bros-u |
| Ni no Kuni II: Revenant Kingdom | `NINO2` | https://en.wikipedia.org/wiki/Ni_no_Kuni_II:_Revenant_Kingdom |
| Ni no Kuni: Wrath of the White Witch | `NINO1` | https://www.ign.com/wikis/ni-no-kuni-wrath-of-the-white-witch |
| Nintendo Labo Toy-Con 01 Variety Kit | `LABO01` | https://www.ign.com/wikis/nintendo-labo/Variety_Kit_01 |
| Nintendo Labo Toy-Con 02 Robot Kit | `LABO02` | https://www.ign.com/wikis/nintendo-labo/Robot_Kit_02 |
| Nintendo Labo Toy-Con 03 Vehicle Kit | `LABO03` | https://www.ign.com/search?q=Nintendo%20Labo%20Toy-Con%2003%20Vehicle%20Kit |
| Nintendo Labo Toy-Con 04 VR Kit | `LABO04` | https://www.ign.com/search?q=Nintendo%20Labo%20Toy-Con%2004%20VR%20Kit |
| Nintendo Switch Sports | `NSSPORTS` | https://www.ign.com/wikis/nintendo-switch-sports |
| Octopath Traveler | `OCTOPATH` | https://www.ign.com/wikis/octopath-traveler |
| Octopath Traveler II | `OCTOPATH2` | https://www.ign.com/wikis/octopath-traveler-2 |
| Oddmar | `ODDMAR` | https://www.exophase.com/game/oddmar-android/achievements |
| Okami HD | `OKAMI` | https://www.ign.com/wikis/okami/Trophies |
| One Piece Odyssey | `ONEPIECE` | https://steamcommunity.com/stats/814000/achievements/?l=english |
| Overwatch 2 | `OW2` | https://steamcommunity.com/stats/2357570/achievements/?l=english |
| Owlboy | `OWLBOY` | https://steamcommunity.com/stats/115800/achievements |
| PGA TOUR 2K21 | `PGA21` | https://steamcommunity.com/stats/1016120/achievements/?l=english |
| PICO PARK | `PICOPARK` | https://www.nintendo.com/us/store/products/pico-park-switch/ |
| PICROSS LORD OF THE NAZARICK | `PICROSSLORD` | https://www.nintendo.com/us/store/products/picross-lord-of-the-nazarick-switch |
| PICROSS S | `PICROSS_S` | https://www.nintendo.com/us/store/products/picross-s-switch/ |
| PICROSS S Capcom Classics Edition | `PICROSS_CAPCOM` | https://nintendo.com/us/store/products/picross-s-capcom-classics-edition-switch |
| PICROSS S Doraemon Edition | `PICROSS_DORA` | https://nintendo.com/us/store/products/picross-s-doraemon-and-f-characters-edition-switch |
| PICROSS S Genesis and Master System Edition | `PICROSS_GENESIS` | https://www.nintendo.com/us/store/products/picross-s-genesis-and-master-system-edition-switch |
| PICROSS S Konami Antiques Edition | `PICROSS_KONAMI` | https://www.jupiter.co.jp/e/switch/picrosssknm/ |
| PICROSS S Namco Legendary Edition | `PICROSS_NAMCO` | https://www.jupiter.co.jp/e/switch/picrosssnle |
| PICROSS S SNK Classics and NeoGeo Edition | `PICROSS_SNK` | https://www.nintendo.com/us/store/products/picross-s-snk-classics-and-neogeo-edition-switch |
| PICROSS S+ | `PICROSS_SP` | https://www.nintendo.com/us/store/products/picross-s-plus-switch/ |
| PICROSS S2 | `PICROSS_S2` | https://www.nintendo.com/us/store/products/picross-s2-switch |
| PICROSS S3 | `PICROSS_S3` | https://www.nintendo.com/us/store/products/picross-s3-switch |
| PICROSS S4 | `PICROSS_S4` | https://www.nintendo.com/us/store/products/picross-s4-switch |
| PICROSS S5 | `PICROSS_S5` | https://www.nintendo.com/us/store/products/picross-s5-switch |
| PICROSS S6 | `PICROSS_S6` | https://www.nintendo.com/us/store/products/picross-s6-switch |
| PICROSS S7 | `PICROSS_S7` | https://nintendo.com/us/store/products/picross-s7-switch |
| PICROSS S8 | `PICROSS_S8` | https://www.nintendo.com/us/store/products/picross-s8-switch/ |
| PICROSS S9 | `PICROSS_S9` | https://nintendo.com/us/store/products/picross-s9-switch |
| Paper Mario: The Origami King | `PAPER_OK` | https://www.ign.com/wikis/paper-mario-origami-king/Walkthrough |
| Paper Mario: The Thousand-Year Door | `PAPER_TYD` | https://www.ign.com/wikis/paper-mario-the-thousand-year-door/Walkthrough_and_Collectibles_Guide |
| Persona 3 Portable | `P3P` | https://www.ign.com/wikis/persona-3-portable |
| Persona 4 Golden | `P4G` | https://www.ign.com/wikis/shin-megami-tensei-persona-4-golden |
| Pikmin 1 | `PIKMIN1` | https://www.ign.com/wikis/pikmin/Ship_Parts_Locations |
| Pikmin 2 | `PIKMIN2` | https://www.ign.com/wikis/pikmin-2/Treasure_Locations |
| Pikmin 3 Deluxe | `PIKMIN3` | https://www.ign.com/wikis/pikmin-3/Fruit_Locations |
| Pikmin 4 | `PIKMIN4` | https://www.ign.com/wikis/pikmin-4 |
| Pokemon Brilliant Diamond | `POKEMON_BD` | https://www.ign.com/wikis/pokemon-diamond-pearl-platinum-version/Brilliant_Diamond_and_Shining_Pearl_Walkthrough |
| Pokemon Cafe ReMix | `POKECAFE` | https://www.ign.com/games/pokemon-cafe-remix |
| Pokemon Champions | `POKECHAMP` | https://www.ign.com/wikis/pokemon-champions |
| Pokemon Legends Arceus | `ARCEUS` | https://www.ign.com/wikis/pokemon-legends-arceus/Pokedex_(List_of_Pokemon) |
| Pokemon Legends Z-A | `ZA` | https://www.ign.com/games/pokemon-legends-z-a/checklists |
| Pokemon Lets Go Eevee | `LETSGO_E` | https://www.ign.com/wikis/pokemon-lets-go-pikachu-eevee/List_of_Pokemon_in_Let%27s_Go_%28Pokedex%29 |
| Pokemon Lets Go Pikachu | `LETSGO_P` | https://www.ign.com/wikis/pokemon-lets-go-pikachu-eevee/List_of_Pokemon_in_Let%27s_Go_%28Pokedex%29 |
| Pokemon Mystery Dungeon: Rescue Team DX | `PMD_RTX` | https://www.ign.com/wikis/pokemon-mystery-dungeon-rescue-team-dx/Walkthrough |
| Pokemon Scarlet | `SCARLET` | https://www.ign.com/wikis/pokemon-scarlet-violet/Pokedex_-_All_Pokemon_in_Scarlet_and_Violet |
| Pokemon Shield | `SHIELD` | https://www.ign.com/wikis/pokemon-sword-shield/Post_Game%3A_Things_to_Do_After_You_Become_Champion |
| Pokemon Shining Pearl | `POKEMON_SP` | https://www.ign.com/wikis/pokemon-diamond-pearl-platinum-version/New_Features_and_Changes_in_Brilliant_Diamond_and_Shining_Pearl |
| Pokemon Sword | `SWORD` | https://www.ign.com/wikis/pokemon-sword-shield/Post_Game%3A_Things_to_Do_After_You_Become_Champion |
| Pokemon UNITE | `UNITE` | https://www.ign.com/wikis/pokemon-unite |
| Pokemon Violet | `VIOLET` | https://www.ign.com/wikis/pokemon-scarlet-violet/Pokedex_-_All_Pokemon_in_Scarlet_and_Violet |
| Power Rangers: Battle for the Grid | `POWERR` | https://steamcommunity.com/stats/1110100/achievements/?l=english |
| Princess Peach: Showtime! | `PEACH` | https://www.ign.com/wikis/princess-peach-showtime/Princess_Peach:_Showtime_Walkthrough |
| Return of the Obra Dinn | `OBRA` | https://www.ign.com/wikis/return-of-the-obra-dinn/Crewmembers_and_Fates |
| Ring Fit Adventure | `RINGFIT` | https://www.ign.com/wikis/ring-fit-adventure |
| Risk of Rain | `RISKOFRAIN` | https://steamcommunity.com/stats/248820/achievements |
| River City Girls 2 | `RCG2` | https://steamcommunity.com/stats/1920480/achievements/?l=english |
| SEGA AGES Sonic The Hedgehog | `SAGES1` | https://gamefaqs.gamespot.com/switch/237014-sega-ages-sonic-the-hedgehog/cheats |
| SEGA AGES Sonic The Hedgehog 2 | `SAGES2` | https://gamefaqs.gamespot.com/switch/247860-sega-ages-sonic-the-hedgehog-2/cheats |
| SIGNALIS | `SIGNALIS` | https://steamcommunity.com/stats/1262350/achievements/?l=english |
| Scott Pilgrim vs. The World: The Game - Complete Edition | `SCOTT` | https://steamcommunity.com/stats/2215260/achievements/?l=english |
| Shantae | `SHANTAE1` | https://www.ign.com/wikis/shantae |
| Shin Megami Tensei III Nocturne HD Remaster | `SMT3` | https://www.ign.com/wikis/shin-megami-tensei-iii-nocturne-hd-remaster |
| Shin Megami Tensei V | `SMTV` | https://en.wikipedia.org/wiki/Shin_Megami_Tensei_V |
| Shin Megami Tensei V: Vengeance | `SMTVV` | https://en.wikipedia.org/wiki/Shin_Megami_Tensei_V |
| Splatoon 2 | `SPLATOON2` | https://www.ign.com/wikis/splatoon-2/Sunken_Scroll_Locations |
| Splatoon 3 | `SPLATOON3` | https://www.ign.com/wikis/splatoon-3/Sunken_Sea_Scroll_Locations |
| Star Ocean First Departure R | `SO1` | https://www.ign.com/wikis/psp-cheats/Star_Ocean:_First_Departure_Cheats |
| Street Fighter 30th Anniversary Collection | `SF30` | https://steamcommunity.com/stats/586200/achievements/?l=english |
| Subnautica: Below Zero | `SUBBELOW` | https://www.ign.com/wikis/subnautica-below-zero |
| Super Kirby Clash | `KIRBY_CLAN` | https://www.ign.com/games/super-kirby-clash |
| Super Mario 3D World Bowsers Fury | `S3DW` | https://www.ign.com/wikis/super-mario-3d-world-and-bowsers-fury |
| Super Mario Bros Wonder | `WONDER` | https://www.ign.com/wikis/super-mario-bros-wonder/List_of_Medals_and_100%25_Completion_Guide |
| Super Mario Maker 2 | `SMM2` | https://www.ign.com/wikis/super-mario-maker-2 |
| Super Mario Odyssey | `ODYSSEY` | https://www.ign.com/wikis/super-mario-odyssey/Power_Moon_Locations |
| Super Mario Party | `SMP` | https://www.ign.com/wikis/super-mario-party/How_to_Unlock_Characters,_Boards,_and_Gems |
| Super Mario Party Jamboree | `JAMBOREE` | https://www.ign.com/wikis/super-mario-party-jamboree/How_to_Unlock_All_Characters,_Boards,_and_Modes |
| Super Smash Bros. Ultimate | `SSBU` | https://www.ign.com/wikis/super-smash-bros-ultimate/Primary_Spirits:_Rank,_Traits,_Power,_and_Slots |
| THEATRHYTHM FINAL BAR LINE | `THEATRHYTHM` | https://www.ign.com/search?q=Theatrhythm%20Final%20Bar%20Line |
| The Case of the Golden Idol | `GOLD` | https://steamcommunity.com/stats/1677770/achievements/?l=english |
| The Legend of Zelda: Breath of the Wild | `BOTW` | https://www.ign.com/wikis/the-legend-of-zelda-breath-of-the-wild/100_Percent_Completion_Checklist |
| The Legend of Zelda: Echoes of Wisdom | `ECHOES` | https://www.ign.com/wikis/the-legend-of-zelda-echoes-of-wisdom |
| The Legend of Zelda: Skyward Sword HD | `SKYSWORD` | https://www.ign.com/wikis/the-legend-of-zelda-skyward-sword/100%_Completion_Checklist |
| The Legend of Zelda: Tears of the Kingdom | `TOTK` | https://www.ign.com/wikis/the-legend-of-zelda-tears-of-the-kingdom/100_Percent_Completion_Checklist |
| The Stanley Parable Ultra Deluxe | `STANLEY` | https://steamcommunity.com/stats/1703340/achievements/?l=english |
| The Turing Test | `TURING` | https://www.gamepressure.com/theturingtest |
| The Wonderful 101: Remastered | `W101` | https://www.ign.com/wikis/the-wonderful-101 |
| Tokyo Mirage Sessions #FE Encore | `TMS` | https://www.ign.com/wikis/tokyo-mirage-sessions-fe |
| Tony Hawk's Pro Skater 1 + 2 | `THPS` | https://www.ign.com/wikis/tony-hawks-pro-skater-1-and-2 |
| Transformers: Battlegrounds | `TRANSFORMERS` | https://www.exophase.com/game/transformers-battlegrounds-xbox/achievements/ |
| Triangle Strategy | `TRIANGLE` | https://www.ign.com/wikis/triangle-strategy |
| Undertale | `UNDERTALE` | https://www.ign.com/wikis/undertale |
| Venba | `VENBA` | https://steamcommunity.com/stats/1491670/achievements |
| WORLD OF FINAL FANTASY MAXIMA | `WOFF` | https://www.ign.com/wikis/world-of-final-fantasy |
| WarioWare: Move It! | `WARIOWARE_MOVE` | https://www.ign.com/wikis/warioware-move-it/Cheats,_Secrets,_and_Unlockables |
| Warioware Get it Together | `WARIOWARE` | https://www.ign.com/wikis/warioware-get-it-together |
| Wonder Boy: The Dragon's Trap | `WONDERBOYTRAP` | https://steamcommunity.com/stats/543260/achievements |
| Xenoblade Chronicles 2 | `XC2` | https://www.ign.com/wikis/xenoblade-chronicles-2 |
| Xenoblade Chronicles 3 | `XC3` | https://www.ign.com/wikis/xenoblade-chronicles-3 |
| Xenoblade Chronicles Definitive Edition | `XC1` | https://www.ign.com/wikis/xenoblade-chronicles |
| Xenoblade Chronicles X: Definitive Edition | `XCX` | https://www.ign.com/wikis/xenoblade-chronicles-x/Collectopedia_Guide |
| Yoshis Crafted World | `YOSHI` | https://www.ign.com/wikis/yoshis-crafted-world |
| Zelda Links Awakening | `LA` | https://www.ign.com/wikis/the-legend-of-zelda-links-awakening-switch/The_Legend_of_Zelda:_Link%27s_Awakening_Walkthrough |

## License

The overlay code is released under GPL-2.0-or-later to match the vendored
libtesla license. See `libtesla/LICENSE`.
