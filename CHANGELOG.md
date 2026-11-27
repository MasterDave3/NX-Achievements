# Changelog

All notable changes to NX-Achievements. The version shown in the overlay matches
the tags below.

## [Unreleased]

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

## [v0.6.0] - 2026-11-26

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

## [v0.5.0] - 2026-11-26

- Notification is now a single row: name and description on the left, progress on
  the right, e.g. `Weaved - Defeat Widow` / `1/10  +1  ->  2/10`.
- Removed the separate `Progress` and `Continue` rows from the popup.
- Press **A** or **B** to close the notification.
- Commit: `884e702`

## [v0.4.0] - 2026-11-26

- Counter popups now show the old and new value, e.g.
  `56/900  +1  ->  57/900`.
- The final step still switches the header to **Achievement unlocked!**.
- Commit: `451302d`

## [v0.3.0] - 2026-11-26

- Popups now appear on **every** counter increment, not just at completion.
- Added an **Achievement progress** header for partial steps.
- **X** and **Y** still subtract/reset silently.
- Commit: `78ed09e`

## [v0.2.0] - 2026-11-26

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

## [v0.1.0] - 2026-11-26

- Initial Tesla overlay with title-ID detection, data-driven achievements from
  `sdmc:/switch/achievements/achievements.txt`, manual **A** toggles, and
  `progress.txt` saving.
- Initial catalog of 91 games, expanded to 226 games / 7,083 achievements.
- Added `SUPPORTED_GAMES.md` and vendored `libtesla`.
- Guaranteed every game has at least 20 goals.
- Commits: `f8a7141`, `cf00769`, `f38cd16`, `153474e`
