"""Approved batch 10 games for NX-Achievements.

All title IDs were resolved from blawar/titledb US.en.json and checked against
the current catalog. Steam appids were verified against Steam achievement
schemas; only ports with at least 20 mirrored achievements are listed here.
"""

# Non-Steam games use checklist modules in tools/checklists/batch10*.py.
NEW_EXTRA_GAMES = [
    ('GRIM', 'GrimGrimoire OnceMore', '0100189018E56000', []),
    ('LEGO2K', 'LEGO 2K Drive', '0100739018020000', []),
    ('SUBBELOW', 'Subnautica: Below Zero', '010014C011146000', []),
    ('APEX', 'Apex Legends', '0100D9500FC66000', []),
    ('DAUNTLESS', 'Dauntless', '0100B9500D1B0000', []),
    ('TURING', 'The Turing Test', '0100EA100F516000', []),
    ('SHANTAE1', 'Shantae', '0100430013120000', []),
    ('CURSE1', 'Bloodstained: Curse of the Moon', '01004B800AF5A000', []),
    ('CURSE2', 'Bloodstained: Curse of the Moon 2', '01004680124E6000', []),
    ('ASTRAL', 'ASTRAL CHAIN', '01007300020FA000', []),
    ('ODDMAR', 'Oddmar', '01001F100FA04000', []),
    ('PICROSSLORD', 'PICROSS LORD OF THE NAZARICK', '010012100E8DC000', []),
]

# Steam ports mirrored by name/description only; no checklist goals are mixed in.
NEW_STEAM_EXTRA = [
    ('MHS', 'Monster Hunter Stories', '010069301B1D4000', 2356560),
    ('TOGRE', 'Tactics Ogre: Reborn', '0100E12013C1A000', 1451090),
    ('OCTOPATH0', 'OCTOPATH TRAVELER 0', '01005270232F2000', 3014320),
    ('VC1', 'Valkyria Chronicles', '0100CAF00B744000', 294860),
    ('VC4', 'Valkyria Chronicles 4', '01005C600AC68000', 790820),
    ('LOSTSPHEAR', 'LOST SPHEAR', '010077B0038B2000', 525240),
    ('SAGA3', 'Romancing SaGa 3', '0100D0400D27A000', 952540),
    ('SAGAMS', 'Romancing SaGa -Minstrel Song- Remastered', '01004A6017E8A000', 1793030),
    ('MANA', 'Trials of Mana', '0100D7800E9E0000', 924980),
    ('SAGAF1', 'SaGa Frontier Remastered', '0100A51013530000', 1295270),
    ('SAGAF2', 'SaGa Frontier 2 Remastered', '0100F2301BD98000', 2452080),
    ('FFTA', 'FINAL FANTASY TACTICS - The Ivalice Chronicles', '010038B015560000', 1004640),
    ('BIOSHOCK2', 'BioShock 2 Remastered', '01002620102C6000', 409720),
    ('FC25', 'EA SPORTS FC 25', '010054E01D878000', 2669320),
    ('MK1', 'Mortal Kombat 1', '01006560184E6000', 1971870),
    ('ARKHAM1', 'Batman: Arkham Asylum', '0100E870163CA000', 35140),
    ('ARKHAM2', 'Batman: Arkham City', '01003F00163CE000', 200260),
    ('ARKHAM3', 'Batman: Arkham Knight', '0100ACD0163D0000', 208650),
    ('GBUSTERS', 'Ghostbusters: The Video Game Remastered', '0100EAE00D9EC000', 1449280),
    ('GBSPIRITS', 'Ghostbusters: Spirits Unleashed Ecto Edition', '01005D2016934000', 2383990),
    ('LEGOBRICK', 'LEGO Bricktales', '0100B12017F0A000', 1898290),
    ('KCD', 'Kingdom Come Deliverance: Royal Edition', '0100650018FE0000', 379430),
    ('OUTERWORLDS', 'The Outer Worlds', '0100626011656000', 1920490),
    ('FALLOUTS', 'Fallout Shelter', '010043500A17A000', 588430),
    ('MINELEGENDS', 'Minecraft Legends', '01007C6012CC8000', 1928870),
    ('NMS', 'No Man\'s Sky', '0100853015E86000', 275850),
    ('WARFRAME', 'Warframe', '0100FEE00A64E000', 230410),
    ('TALOS', 'The Talos Principle: Deluxe Edition', '010092A00D43C000', 257510),
    ('PORTAL2', 'Portal 2', '0100ABD01785C000', 620),
    ('TETRISE', 'Tetris Effect: Connected', '0100DE501433A000', 1003590),
    ('BOMBR2', 'SUPER BOMBERMAN R 2', '0100B87017D94000', 1913740),
    ('NEONW', 'Neon White', '0100B9201406A000', 1533420),
    ('PATHLESS', 'The Pathless', '0100D5501522C000', 1492680),
    ('ARY', 'Ary and the Secret of Seasons', '0100C2500CAB6000', 935570),
    ('TRINE4', 'Trine 4: The Nightmare Prince', '010055E00CA68000', 690640),
    ('PPT1', 'Puyo Puyo Tetris', '010073C001D5E000', 546050),
    ('SHANTAE2', 'Shantae: Half-Genie Hero', '0100AE0003424000', 253840),
    ('SHANTAE3', 'Shantae and the Seven Sirens', '0100EB901040A000', 1191630),
    ('SHANTAE4', 'Shantae and the Pirate\'s Curse', '0100EFD00A4FA000', 345820),
    ('SHANTAE5', 'Shantae Advance: Risky Revolution', '010031101D400000', 3055950),
    ('SHANTAE6', 'Shantae: Risky\'s Revenge - Director\'s Cut', '0100ADA012370000', 277890),
    ('VRAN', 'Victor Vran Overkill Edition', '0100E81007A06000', 345180),
    ('BOLTGUN', 'Warhammer 40,000: Boltgun', '01005FD017E60000', 2005010),
    ('MECHANICUS', 'Warhammer 40,000: Mechanicus', '0100C6000EEA8000', 673880),
    ('DAEMONX', 'DAEMON X MACHINA', '0100B6400CA56000', 1167450),
    ('RAJI', 'Raji: An Ancient Epic', '010010B00DDA2000', 730390),
    ('DEFGRID2', 'Defense Grid 2', '010061300BBF8000', 221540),
]
