# Changelog

All notable changes to NX-Achievements. The version shown in the overlay matches
the tags below.

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
