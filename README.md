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
- Loads achievements from `sdmc:/switch/achievements/achievements.txt`.
- Data-driven: adding games needs no rebuild of the `.ovl`.
- Saves unlock state and counters to `sdmc:/switch/achievements/progress.txt`.
- Countable goals show `current/target`; **A** adds 1, **X** subtracts 1, **Y** resets.
- Shows `old  +1  ->  new` on every counter step, e.g. `1/10  +1  ->  2/10`.
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
Boot CFW and open Ultrahand (default **ZL + ZR + D-Pad Down**) or Tesla.

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

## Limitations

- Achievements are tracked manually: A toggles or counts up, X counts down, Y resets.
  A normal Ultrahand/Tesla overlay cannot draw automatic popups over arbitrary
  games; that requires a game-specific plugin.
- Steam entries are names/descriptions only — the overlay cannot read a Steam
  account or unlock Steam achievements.
- Automatic checks from save data or memory can be added later per game.

## Changelog

All notable changes to NX-Achievements. The version shown in the overlay matches
the tags below.

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

**228 games · 9,891 achievements** (plus one global `FIRST_BOOT` goal)

IGN-style checklist goals cover all 133 non-Steam games, using IGN where available
and other reputable checklists otherwise. 670 goals across the catalog are countable
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
| 164 | Demon Slayer: The Hinokami Chronicles | `0100309016E7A000` | 24 |
| 165 | Jujutsu Kaisen Cursed Clash | `010000B01A452000` | 24 |
| 166 | Naruto Shippuden: Ultimate Ninja Storm 4 | `010084D00CF5E000` | 22 |
| 167 | My Hero One's Justice 2 | `01007E700DBF6000` | 22 |
| 168 | One Piece Odyssey | `0100D9601A994000` | 27 |
| 169 | Guilty Gear -Strive- | `0100AB401F136000` | 39 |
| 170 | Samurai Shodown | `01002DF00F76C000` | 45 |
| 171 | Power Rangers: Battle for the Grid | `0100E1E00CF1A000` | 24 |
| 172 | Transformers: Battlegrounds | `01005E500E528000` | 30 |
| 173 | Hello Kitty Island Adventure | `010027901C89C000` | 32 |
| 174 | Moving Out | `0100C4C00E73E000` | 38 |
| 175 | Moving Out 2 | `010065D018172000` | 28 |
| 176 | Untitled Goose Game | `010082400BCC6000` | 25 |
| 177 | Baba Is You | `01002CD00A51C000` | 26 |
| 178 | Risk of Rain 2 | `010076D00E4BA000` | 205 |
| 179 | Spelunky 2 | `01007EC013ABC000` | 32 |
| 180 | Slay the Spire | `010026300BA4A000` | 46 |
| 181 | Vampire Survivors | `010089A0197E4000` | 243 |
| 182 | Balatro | `0100CD801CE5E000` | 31 |
| 183 | Dave the Diver | `010097F018538000` | 56 |
| 184 | Katana ZERO | `010029600D56A000` | 22 |
| 185 | Bloodstained: Ritual of the Night | `0100BF500207C000` | 30 |
| 186 | Castlevania Advance Collection | `0100B33014710000` | 33 |
| 187 | River City Girls 2 | `0100026016320000` | 28 |
| 188 | Scott Pilgrim vs. The World: The Game - Complete Edition | `0100394011C30000` | 27 |
| 189 | Okami HD | `0100276009872000` | 30 |
| 190 | Red Dead Redemption | `01007820196A6000` | 51 |
| 191 | Tomb Raider I-III Remastered | `010024601BB16000` | 284 |
| 192 | Borderlands: Game of the Year Edition | `010064800F66A000` | 31 |
| 193 | Wolfenstein II: The New Colossus | `01009040091E0000` | 80 |
| 194 | Metro 2033 Redux | `0100D4900E82C000` | 49 |
| 195 | Metro: Last Light Redux | `0100F0400E850000` | 49 |
| 196 | BioShock Remastered | `0100AD10102B2000` | 65 |
| 197 | Portal Knights | `0100437004170000` | 40 |
| 198 | Bridge Constructor Portal | `010016E004796000` | 20 |
| 199 | House Flipper | `0100CAE00EB02000` | 96 |
| 200 | PowerWash Simulator | `0100926016012000` | 100 |
| 201 | PICO PARK | `01004EA00DF70000` | 21 |
| 202 | Duck Game | `0100750001C70000` | 38 |
| 203 | Don't Starve Together | `010090100E334000` | 29 |
| 204 | Grounded | `01006F301AE9C000` | 45 |
| 205 | Subnautica | `0100429011144000` | 20 |
| 206 | Astroneer | `0100E63013E60000` | 116 |
| 207 | Slime Rancher: Plortable Edition | `0100B9C0148D0000` | 57 |
| 208 | Green Hell | `0100453012FEA000` | 68 |
| 209 | Dead by Daylight | `01004C400CF96000` | 318 |
| 210 | Outlast 2 | `0100DE70085E8000` | 24 |
| 211 | Little Nightmares Complete Edition | `01002FC00412C000` | 22 |
| 212 | Little Nightmares II | `010097100EDD6000` | 35 |
| 213 | INSIDE | `0100D2D009028000` | 20 |
| 214 | LIMBO | `01009C8009026000` | 20 |
| 215 | Firewatch | `0100AC300919A000` | 20 |
| 216 | Life is Strange Remastered | `0100DC301186A000` | 22 |
| 217 | Life is Strange: True Colors | `0100500012AB4000` | 40 |
| 218 | Cat Quest III | `010088501B8F2000` | 30 |
| 219 | Minecraft Dungeons | `01006C100EC08000` | 104 |
| 220 | Cooking Simulator | `01001E400FD58000` | 20 |
| 221 | This War of Mine: Complete Edition | `0100A8700BC2A000` | 59 |
| 222 | Plague Inc: Evolved | `01000CE00CBB8000` | 250 |
| 223 | Overcooked! 2 | `01006FD0080B2000` | 54 |
| 224 | ARK: Survival Evolved | `0100D4A00B284000` | 32 |
| 225 | Don't Starve: Nintendo Switch Edition | `0100751007ADA000` | 113 |
| 226 | Until Dawn | `01001E1025697001` | 29 |
| 227 | 20 Minutes Till Dawn | `0100212019FB6000` | 34 |
| 228 | Hollow Knight: Silksong | `010013C00E930000` | 52 |

## Checklist sources

Sources used for the non-Steam IGN-style checklist goals. Steam ports
are deliberately omitted because they mirror real Steam achievements.

| Game | Slug | Source |
|---|---|---|
| 1-2-Switch | `12SWITCH` | https://www.ign.com/wikis/1-2switch |
| ARMS | `ARMS` | https://www.ign.com/wikis/arms |
| Advance Wars 1+2 Re-Boot Camp | `ADVANCEWARS` | https://www.ign.com/wikis/advance-wars-reboot-camp |
| Animal Crossing New Horizons | `ACNH` | https://www.ign.com/games/animal-crossing-new-horizons/checklists |
| Assassin's Creed III Remastered | `AC3` | https://mapgenie.io/assassins-creed-3/checklist |
| Assassin's Creed: The Rebel Collection | `ACREBEL` | https://www.ign.com/wikis/assassins-creed-4-black-flag |
| Bayonetta | `BAYONETTA` | https://www.ign.com/wikis/bayonetta/Achievements_and_Trophies |
| Bayonetta 2 | `BAYONETTA2` | https://www.ign.com/wikis/bayonetta-2/Walkthrough |
| Bayonetta 3 | `BAYONETTA3` | https://www.ign.com/wikis/bayonetta-3/Collectibles |
| Bayonetta Origins: Cereza and the Lost Demon | `BAYORIGINS` | https://samurai-gamers.com/bayonetta-origins-cereza-and-the-lost-demon/all-collectibles-list-and-guides/ |
| Big Brain Academy: Brain vs. Brain | `BRAIN` | https://www.ign.com/games/big-brain-academy-brain-vs-brain |
| Bloodstained: Ritual of the Night | `BLOODSTAINED` | https://www.ign.com/wikis/bloodstained-ritual-of-the-night/Achievements_and_Trophies |
| Borderlands: Game of the Year Edition | `BORDERLANDS` | https://steamcommunity.com/stats/729040/achievements/?l=english |
| Bravely Default II | `BRAVELY` | https://www.ign.com/wikis/bravely-default-2 |
| Burnout Paradise Remastered | `BURNOUT` | https://www.ign.com/wikis/burnout-paradise/Smashes_Locations_and_Maps |
| Captain Toad Treasure Tracker | `TOAD` | https://www.ign.com/wikis/captain-toad-treasure-tracker/Super_Gems |
| Castlevania Advance Collection | `CASTLEVANIA` | https://www.ign.com/wikis/castlevania-advance-collection-collection |
| Clubhouse Games: 51 Worldwide Classics | `CLUBHOUSE` | https://www.nintendo.com/my/switch/as7t/index.html |
| Crash Team Racing Nitro-Fueled | `CTR` | https://www.ign.com/wikis/crash-team-racing-nitro-fueled/Adventure_Mode_Explained |
| Crisis Core -Final Fantasy VII- Reunion | `CRISISCORE` | https://www.ign.com/wikis/crisis-core-final-fantasy-vii |
| Deltarune | `DELTARUNE` | https://www.ign.com/wikis/deltarune |
| Demon Slayer: The Hinokami Chronicles | `DSLAYER` | https://www.ign.com/wikis/demon-slayer-the-hinokami-chronicles/Achievements_and_Trophies |
| Detective Pikachu Returns | `DETECTIVE` | https://www.ign.com/wikis/detective-pikachu-returns |
| Diablo III Eternal Collection | `DIABLO3` | https://www.ign.com/wikis/diablo-3/Achievements_and_Trophies |
| Don't Starve Together | `DST` | https://dontstarve.wiki.gg/wiki/Don%27t_Starve_Together |
| Donkey Kong Country Returns HD | `DKCR` | https://www.ign.com/wikis/donkey-kong-country-returns/100_Percent_Completion_Checklist |
| Donkey Kong Country Tropical Freeze | `DKC` | https://www.ign.com/wikis/donkey-kong-country-tropical-freeze/100_Percent_Completion_Checklist |
| Dragon Quest Builders 2 | `DQB2` | https://en.wikipedia.org/wiki/Dragon_Quest_Builders_2 |
| Dragon Quest XI S: Echoes of an Elusive Age | `DQ11S` | https://www.ign.com/wikis/dragon-quest-xi |
| EA SPORTS FC 24 | `FC24` | https://www.ign.com/wikis/ea-sports-fc-24 |
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
| GRID Autosport | `GRID` | https://www.ign.com/articles/2014/06/24/grid-autosport-review |
| Game Builder Garage | `GBG` | https://www.nintendo.com/ph/switch/awux/lesson/index.html |
| Go Vacation | `GOVACATION` | https://es.ign.com/go-vacation-nintendo-switch/136959/review/analisis-de-go-vacation-para-nintendo-switch |
| Hello Kitty Island Adventure | `HELLOKITTY` | https://steamcommunity.com/stats/2495100/achievements/?l=english |
| Hyrule Warriors Age of Calamity | `AOC` | https://zeldacentral.com/games/hyrule-warriors-age-of-calamity/100-completion-checklist/ |
| Hyrule Warriors: Definitive Edition | `HRW` | https://www.ign.com/wikis/hyrule-warriors |
| Jujutsu Kaisen Cursed Clash | `JJK` | https://www.playstationtrophies.org/game/jujustu-kaisen-cursed-clash/trophies |
| Just Dance 2020 | `JUSTDANCE` | https://en.wikipedia.org/wiki/Just_Dance_2020 |
| Kirby Fighters 2 | `KIRBYFIGHT` | https://wikirby.com/wiki/100%25_completion |
| Kirby Return to Dream Land Deluxe | `KIRBY_RTDL` | https://www.ign.com/wikis/kirbys-return-to-dream-land/Energy_Spheres |
| Kirby Star Allies | `KIRBY_SA` | https://www.ign.com/wikis/kirby-switch |
| Kirby and the Forgotten Land | `KIRBY_FL` | https://www.ign.com/wikis/kirby-and-the-forgotten-land/How_to_Unlock_Everything |
| LEGO CITY Undercover | `LEGOCITY` | https://www.ign.com/wikis/lego-city-undercover/Gold_Bricks |
| LIVE A LIVE | `LIVEALIVE` | https://www.ign.com/wikis/live-a-live |
| Life is Strange Remastered | `LIS` | https://steamcommunity.com/stats/1265920/achievements/?l=english |
| Luigi's Mansion 2 HD | `LM2HD` | https://www.ign.com/wikis/luigis-mansion-2/100%25_Completion_Tracker |
| Luigis Mansion 3 | `LM3` | https://www.ign.com/wikis/luigis-mansion-3 |
| MLB The Show 23 | `MLB23` | https://primagames.com/tips/mlb-the-show-23-trophies-and-achievements-listed |
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
| Minecraft | `MINECRAFT` | https://www.ign.com/wikis/minecraft/Achievements |
| MotoGP 24 | `MOTOGP24` | https://racinggames.gg/article/motogp-24-trophies-and-achievements-complete-guide |
| My Hero One's Justice 2 | `MHA2` | https://www.playstationtrophies.org/game/my-hero-ones-justice-2/trophies |
| NBA 2K20 | `NBA2K` | https://www.ign.com/wikis/nba-2k20 |
| Naruto Shippuden: Ultimate Ninja Storm 4 | `NARUTO4` | https://www.ign.com/wikis/naruto-shippuden-ultimate-ninja-storm-4/Memory_Fragments |
| New Super Mario Bros U Deluxe | `NSMBU` | https://www.ign.com/wikis/new-super-mario-bros-u |
| Ni no Kuni II: Revenant Kingdom | `NINO2` | https://en.wikipedia.org/wiki/Ni_no_Kuni_II:_Revenant_Kingdom |
| Ni no Kuni: Wrath of the White Witch | `NINO1` | https://www.ign.com/wikis/ni-no-kuni-wrath-of-the-white-witch |
| Nintendo Switch Sports | `NSSPORTS` | https://www.ign.com/wikis/nintendo-switch-sports |
| Octopath Traveler | `OCTOPATH` | https://www.ign.com/wikis/octopath-traveler |
| Octopath Traveler II | `OCTOPATH2` | https://www.ign.com/wikis/octopath-traveler-2 |
| Okami HD | `OKAMI` | https://www.ign.com/wikis/okami/Trophies |
| One Piece Odyssey | `ONEPIECE` | https://steamcommunity.com/stats/814000/achievements/?l=english |
| PICO PARK | `PICOPARK` | https://www.nintendo.com/us/store/products/pico-park-switch/ |
| Persona 3 Portable | `P3P` | https://www.ign.com/wikis/persona-3-portable |
| Persona 4 Golden | `P4G` | https://www.ign.com/wikis/shin-megami-tensei-persona-4-golden |
| Pikmin 1 | `PIKMIN1` | https://www.ign.com/wikis/pikmin/Ship_Parts_Locations |
| Pikmin 2 | `PIKMIN2` | https://www.ign.com/wikis/pikmin-2/Treasure_Locations |
| Pikmin 3 Deluxe | `PIKMIN3` | https://www.ign.com/wikis/pikmin-3/Fruit_Locations |
| Pikmin 4 | `PIKMIN4` | https://www.ign.com/wikis/pikmin-4 |
| Pokemon Legends Arceus | `ARCEUS` | https://www.ign.com/wikis/pokemon-legends-arceus/Pokedex_(List_of_Pokemon) |
| Pokemon Legends Z-A | `ZA` | https://www.ign.com/games/pokemon-legends-z-a/checklists |
| Pokemon Lets Go Eevee | `LETSGO_E` | https://www.ign.com/wikis/pokemon-lets-go-pikachu-eevee/List_of_Pokemon_in_Let%27s_Go_%28Pokedex%29 |
| Pokemon Lets Go Pikachu | `LETSGO_P` | https://www.ign.com/wikis/pokemon-lets-go-pikachu-eevee/List_of_Pokemon_in_Let%27s_Go_%28Pokedex%29 |
| Pokemon Scarlet | `SCARLET` | https://www.ign.com/wikis/pokemon-scarlet-violet/Pokedex_-_All_Pokemon_in_Scarlet_and_Violet |
| Pokemon Shield | `SHIELD` | https://www.ign.com/wikis/pokemon-sword-shield/Post_Game%3A_Things_to_Do_After_You_Become_Champion |
| Pokemon Sword | `SWORD` | https://www.ign.com/wikis/pokemon-sword-shield/Post_Game%3A_Things_to_Do_After_You_Become_Champion |
| Pokemon UNITE | `UNITE` | https://www.ign.com/wikis/pokemon-unite |
| Pokemon Violet | `VIOLET` | https://www.ign.com/wikis/pokemon-scarlet-violet/Pokedex_-_All_Pokemon_in_Scarlet_and_Violet |
| Power Rangers: Battle for the Grid | `POWERR` | https://steamcommunity.com/stats/1110100/achievements/?l=english |
| Ring Fit Adventure | `RINGFIT` | https://www.ign.com/wikis/ring-fit-adventure |
| River City Girls 2 | `RCG2` | https://steamcommunity.com/stats/1920480/achievements/?l=english |
| Scott Pilgrim vs. The World: The Game - Complete Edition | `SCOTT` | https://steamcommunity.com/stats/2215260/achievements/?l=english |
| Shin Megami Tensei III Nocturne HD Remaster | `SMT3` | https://www.ign.com/wikis/shin-megami-tensei-iii-nocturne-hd-remaster |
| Shin Megami Tensei V | `SMTV` | https://en.wikipedia.org/wiki/Shin_Megami_Tensei_V |
| Shin Megami Tensei V: Vengeance | `SMTVV` | https://en.wikipedia.org/wiki/Shin_Megami_Tensei_V |
| Splatoon 2 | `SPLATOON2` | https://www.ign.com/wikis/splatoon-2/Sunken_Scroll_Locations |
| Splatoon 3 | `SPLATOON3` | https://www.ign.com/wikis/splatoon-3/Sunken_Sea_Scroll_Locations |
| Super Mario 3D World Bowsers Fury | `S3DW` | https://www.ign.com/wikis/super-mario-3d-world-and-bowsers-fury |
| Super Mario Bros Wonder | `WONDER` | https://www.ign.com/wikis/super-mario-bros-wonder/List_of_Medals_and_100%25_Completion_Guide |
| Super Mario Maker 2 | `SMM2` | https://www.ign.com/wikis/super-mario-maker-2 |
| Super Mario Odyssey | `ODYSSEY` | https://www.ign.com/wikis/super-mario-odyssey/Power_Moon_Locations |
| Super Mario Party | `SMP` | https://www.ign.com/wikis/super-mario-party/How_to_Unlock_Characters,_Boards,_and_Gems |
| Super Mario Party Jamboree | `JAMBOREE` | https://www.ign.com/wikis/super-mario-party-jamboree/How_to_Unlock_All_Characters,_Boards,_and_Modes |
| Super Smash Bros. Ultimate | `SSBU` | https://www.ign.com/wikis/super-smash-bros-ultimate/Primary_Spirits:_Rank,_Traits,_Power,_and_Slots |
| The Legend of Zelda: Breath of the Wild | `BOTW` | https://www.ign.com/wikis/the-legend-of-zelda-breath-of-the-wild/100_Percent_Completion_Checklist |
| The Legend of Zelda: Echoes of Wisdom | `ECHOES` | https://www.ign.com/wikis/the-legend-of-zelda-echoes-of-wisdom |
| The Legend of Zelda: Skyward Sword HD | `SKYSWORD` | https://www.ign.com/wikis/the-legend-of-zelda-skyward-sword/100%_Completion_Checklist |
| The Legend of Zelda: Tears of the Kingdom | `TOTK` | https://www.ign.com/wikis/the-legend-of-zelda-tears-of-the-kingdom/100_Percent_Completion_Checklist |
| The Wonderful 101: Remastered | `W101` | https://www.ign.com/wikis/the-wonderful-101 |
| Tokyo Mirage Sessions #FE Encore | `TMS` | https://www.ign.com/wikis/tokyo-mirage-sessions-fe |
| Tony Hawk's Pro Skater 1 + 2 | `THPS` | https://www.ign.com/wikis/tony-hawks-pro-skater-1-and-2 |
| Transformers: Battlegrounds | `TRANSFORMERS` | https://www.exophase.com/game/transformers-battlegrounds-xbox/achievements/ |
| Undertale | `UNDERTALE` | https://www.ign.com/wikis/undertale |
| WarioWare: Move It! | `WARIOWARE_MOVE` | https://www.ign.com/wikis/warioware-move-it/Cheats,_Secrets,_and_Unlockables |
| Warioware Get it Together | `WARIOWARE` | https://www.ign.com/wikis/warioware-get-it-together |
| Xenoblade Chronicles 2 | `XC2` | https://www.ign.com/wikis/xenoblade-chronicles-2 |
| Xenoblade Chronicles 3 | `XC3` | https://www.ign.com/wikis/xenoblade-chronicles-3 |
| Xenoblade Chronicles Definitive Edition | `XC1` | https://www.ign.com/wikis/xenoblade-chronicles |
| Xenoblade Chronicles X: Definitive Edition | `XCX` | https://www.ign.com/wikis/xenoblade-chronicles-x/Collectopedia_Guide |
| Yoshis Crafted World | `YOSHI` | https://www.ign.com/wikis/yoshis-crafted-world |
| Zelda Links Awakening | `LA` | https://www.ign.com/wikis/the-legend-of-zelda-links-awakening-switch/The_Legend_of_Zelda:_Link%27s_Awakening_Walkthrough |

## License

The overlay code is released under GPL-2.0-or-later to match the vendored
libtesla license. See `libtesla/LICENSE`.
