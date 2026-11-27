"""Additional notable Switch games for NX-Achievements.

Every title ID below was resolved from blawar/titledb (US.en.json); none are
guessed. Each entry is (slug, display name, title ID, [goals]). Steam ports
with mirrored achievements live in generate_achievements.py's GAMES list.
"""

EXTRA_GAMES = [
    # ---- Zelda / Nintendo first-party ----
    ('SKYSWORD', 'The Legend of Zelda: Skyward Sword HD', '01002DA013484000', [
        ('SSHD_FIRST', 'First Flight', 'Complete your first flight in Skyward Sword HD'),
        ('SSHD_SILENT', 'Silent Realm', 'Complete a Silent Realm trial'),
        ('SSHD_DEMISE', 'Demise Defeated', 'Defeat Demise and seal the Master Sword'),
    ]),
    ('ECHOES', 'The Legend of Zelda: Echoes of Wisdom', '01008CF01BAAC000', [
        ('EOW_FIRST', 'Echo Apprentice', 'Use your first echo in Echoes of Wisdom'),
        ('EOW_RIFT', 'Rift Walker', 'Close a rift in Hyrule'),
        ('EOW_NULL', 'Null Defeated', 'Defeat Null and restore Hyrule'),
    ]),
    ('DETECTIVE', 'Detective Pikachu Returns', '010007500F27C000', [
        ('DP_FIRST', 'First Case', 'Solve your first case in Ryme City'),
        ('DP_CASES', 'Case Closed', 'Solve every case in Detective Pikachu Returns'),
    ]),
    ('FEW', 'Fire Emblem Warriors', '0100F15003E64000', [
        ('FEW_FIRST', 'First Battle', 'Win your first Warriors battle'),
        ('FEW_ALL', 'War Veteran', 'Complete every story chapter'),
    ]),
    ('FE3HOPES', 'Fire Emblem Warriors: Three Hopes', '010071F0143EA000', [
        ('HOPES_FIRST', 'First Battle', 'Win your first battle in Three Hopes'),
        ('HOPES_ROUTE', 'Route Complete', 'Finish one of the three story routes'),
    ]),
    ('XCX', 'Xenoblade Chronicles X: Definitive Edition', '0100453019AA8000', [
        ('XCX_FIRST', 'First Mission', 'Complete your first mission on Mira'),
        ('XCX_SKETCH', 'Field Sketch', 'Complete the Collectopedia'),
        ('XCX_FINAL', 'Final Mission', 'Complete the main story'),
    ]),
    ('METROID4', 'Metroid Prime 4: Beyond', '010019A01E2F2000', [
        ('MP4_FIRST', 'First Scan', 'Scan your first object on Viewros'),
        ('MP4_TELEKINESIS', 'Psychic Explorer', 'Solve a telekinesis puzzle'),
        ('MP4_FINAL', 'Final Boss', 'Complete the main story of Metroid Prime 4'),
    ]),
    ('LM2HD', "Luigi's Mansion 2 HD", '010048701995E000', [
        ('LM2_FIRST', 'First Mansion', 'Clear the first mansion'),
        ('LM2_ALL', 'Mansion Master', 'Clear every mansion'),
        ('LM2_KINGBOO', 'Ghost Hunter', 'Defeat King Boo'),
    ]),
    ('PIKMIN1', 'Pikmin 1', '0100AA80194B0000', [
        ('P1_FIRST', 'First Day', 'Complete your first day'),
        ('P1_PARTS', 'Ship Parts', 'Recover every ship part'),
    ]),
    ('PIKMIN2', 'Pikmin 2', '0100D680194B2000', [
        ('P2_FIRST', 'First Cave', 'Enter your first cave'),
        ('P2_TREASURE', 'Treasure Hunter', 'Collect every treasure'),
    ]),
    ('KIRBYFIGHT', 'Kirby Fighters 2', '0100227010460000', [
        ('KF2_FIRST', 'First Match', 'Win your first Fighters match'),
        ('KF2_DECK', 'Deck Master', 'Complete a Destined Deck'),
    ]),
    ('HRW', 'Hyrule Warriors: Definitive Edition', '0100AE00096EA000', [
        ('HRW_FIRST', 'First Battle', 'Complete your first battle'),
        ('HRW_ALL', 'Warrior', 'Complete every Legend Mode battle'),
    ]),
    ('WARIOWARE_MOVE', 'WarioWare: Move It!', '010045B018EC2000', [
        ('WWM_FIRST', 'First Game', 'Play your first Move It! minigame'),
        ('WWM_ALL', 'Minigame Master', 'Play every minigame'),
    ]),

    # ---- Mario / party ----
    ('JAMBOREE', 'Super Mario Party Jamboree', '0100965017338000', [
        ('JAM_FIRST', 'First Board', 'Complete your first board'),
        ('JAM_STARS', 'Star Collector', 'Win a board with the most stars'),
        ('JAM_MINI', 'Minigame Master', 'Play every minigame'),
    ]),
    ('MARIOSONIC', 'Mario & Sonic at the Olympic Games Tokyo 2020', '010003000E146000', [
        ('MS_FIRST', 'First Event', 'Complete your first Olympic event'),
        ('MS_GOLD', 'Gold Medal', 'Win gold in an event'),
    ]),
    ('MVS', 'Mario vs. Donkey Kong', '0100B99019412000', [
        ('MVS_FIRST', 'First World', 'Clear the first world'),
        ('MVS_ALL', 'World Champion', 'Clear every world'),
    ]),
    ('DKCR', 'Donkey Kong Country Returns HD', '01009D901BC56000', [
        ('DKCR_FIRST', 'First World', 'Clear the first world'),
        ('DKCR_ALL', 'Jungle Champion', 'Clear every world'),
        ('DKCR_TIKI', 'Tiki Tongue', 'Defeat the Tiki Tong boss'),
    ]),
    ('FITBOX', 'Fitness Boxing', '0100E7300AAD4000', [
        ('FB_FIRST', 'First Workout', 'Complete your first workout'),
        ('FB_STREAK', 'Daily Habit', 'Complete a 7-day workout streak'),
    ]),
    ('FITBOX2', 'Fitness Boxing 2: Rhythm & Exercise', '0100073011382000', [
        ('FB2_FIRST', 'First Workout', 'Complete your first workout'),
        ('FB2_RHYTHM', 'Rhythm Master', 'Complete a full rhythm course'),
    ]),
    ('CLUBHOUSE', 'Clubhouse Games: 51 Worldwide Classics', '010047700D540000', [
        ('CH_FIRST', 'First Game', 'Play your first clubhouse game'),
        ('CH_ALL', 'All-Rounder', 'Try all 51 games'),
    ]),
    ('GBG', 'Game Builder Garage', '0100FA5010788000', [
        ('GBG_FIRST', 'First Game', 'Finish the first lesson'),
        ('GBG_MAKE', 'Game Creator', 'Create and share your own game'),
    ]),
    ('BRAIN', 'Big Brain Academy: Brain vs. Brain', '0100620012D6E000', [
        ('BB_FIRST', 'First Test', 'Complete your first brain test'),
        ('BB_GOLD', 'Gold Brain', 'Earn gold in every category'),
    ]),
    ('GOVACATION', 'Go Vacation', '0100C1800A9B6000', [
        ('GV_FIRST', 'First Activity', 'Try your first vacation activity'),
        ('GV_ALL', 'Vacation Pro', 'Try every activity on Kawawii Island'),
    ]),
    ('JUSTDANCE', 'Just Dance 2020', '0100DDB00DB38000', [
        ('JD_FIRST', 'First Dance', 'Complete your first dance'),
        ('JD_STARS', 'Dance Star', 'Earn five stars on a song'),
    ]),

    # ---- RPGs ----
    ('OCTOPATH', 'Octopath Traveler', '010057D006492000', [
        ('OCT_FIRST', 'First Chapter', 'Complete a character’s first chapter'),
        ('OCT_EIGHT', 'Eight Paths', 'Complete every character’s story'),
    ]),
    ('OCTOPATH2', 'Octopath Traveler II', '0100A3501946E000', [
        ('OCT2_FIRST', 'First Chapter', 'Complete a character’s first chapter'),
        ('OCT2_EIGHT', 'Eight Paths', 'Complete every character’s story'),
    ]),
    ('LIVEALIVE', 'LIVE A LIVE', '0100CF801776C000', [
        ('LAL_FIRST', 'First Era', 'Complete your first era'),
        ('LAL_ALL', 'All Eras', 'Complete every era'),
        ('LAL_FINAL', 'Final Boss', 'Defeat the final boss'),
    ]),
    ('BRAVELY', 'Bravely Default II', '01006DC010326000', [
        ('BD2_FIRST', 'First Chapter', 'Complete the first chapter'),
        ('BD2_FINAL', 'Final Chapter', 'Complete the final chapter'),
    ]),
    ('DQ11S', 'Dragon Quest XI S: Echoes of an Elusive Age', '01006C300E9F0000', [
        ('DQ11_FIRST', 'First Chapter', 'Complete the first story chapter'),
        ('DQ11_FINAL', 'Hero of Arboria', 'Complete the main story'),
    ]),
    ('DQB2', 'Dragon Quest Builders 2', '010042000A986000', [
        ('DQB2_FIRST', 'First Island', 'Complete your first island'),
        ('DQB2_FINAL', 'Builder Champion', 'Complete the main story'),
    ]),
    ('NINO1', 'Ni no Kuni: Wrath of the White Witch', '0100E5600D446000', [
        ('NINO_FIRST', 'First Chapter', 'Complete the first chapter'),
        ('NINO_FINAL', 'Final Boss', 'Complete the main story'),
    ]),
    ('NINO2', 'Ni no Kuni II: Revenant Kingdom', '0100BE7013E06000', [
        ('NINO2_FIRST', 'First Chapter', 'Complete the first chapter'),
        ('NINO2_FINAL', 'Final Boss', 'Complete the main story'),
    ]),
    ('P4G', 'Persona 4 Golden', '010062B01525C000', [
        ('P4G_FIRST', 'First Dungeon', 'Enter your first dungeon'),
        ('P4G_TRUE', 'True Ending', 'Reach the true ending'),
    ]),
    ('P3P', 'Persona 3 Portable', '0100DCD01525A000', [
        ('P3P_FIRST', 'First Tartarus', 'Enter Tartarus for the first time'),
        ('P3P_FINAL', 'Final Hour', 'Reach the true ending'),
    ]),
    ('SMTV', 'Shin Megami Tensei V', '010063B012DC6000', [
        ('SMTV_FIRST', 'First Demon', 'Fuse your first demon'),
        ('SMTV_FINAL', 'Final Boss', 'Complete the main story'),
    ]),
    ('SMTVV', 'Shin Megami Tensei V: Vengeance', '010069C01AB82000', [
        ('SMTVV_FIRST', 'First Demon', 'Fuse your first demon'),
        ('SMTVV_VENGEANCE', 'Vengeance Path', 'Complete the Vengeance route'),
    ]),
    ('SMT3', 'Shin Megami Tensei III Nocturne HD Remaster', '01003B0012DC2000', [
        ('SMT3_FIRST', 'First Demon', 'Fuse your first demon'),
        ('SMT3_FINAL', 'Final Boss', 'Complete the main story'),
    ]),
    ('TMS', 'Tokyo Mirage Sessions #FE Encore', '0100A9400C9C2000', [
        ('TMS_FIRST', 'First Session', 'Complete your first Idol Session'),
        ('TMS_FINAL', 'Final Boss', 'Complete the main story'),
    ]),
    ('FF7', 'Final Fantasy VII', '0100A5B00BDC6000', [
        ('FF7_FIRST', 'Midgar Escape', 'Escape Midgar with the Avalanche crew'),
        ('FF7_FINAL', 'Planet Saver', 'Defeat Sephiroth and save the Planet'),
    ]),
    ('CRISISCORE', 'Crisis Core -Final Fantasy VII- Reunion', '01004BC0166CC000', [
        ('CC_FIRST', 'First Mission', 'Complete your first mission as Zack'),
        ('CC_FINAL', 'Final Mission', 'Complete the main story'),
    ]),
    ('FFX', 'Final Fantasy X/X-2 HD Remaster', '0100BC300CB48000', [
        ('FFX_FIRST', 'First Temple', 'Complete your first temple trial'),
        ('FFX_FINAL', 'Final Aeon', 'Defeat Sin and save Spira'),
    ]),
    ('FF12', 'Final Fantasy XII: The Zodiac Age', '0100EB100AB42000', [
        ('FF12_FIRST', 'First Gambit', 'Set your first gambit'),
        ('FF12_FINAL', 'Final Boss', 'Complete the main story'),
    ]),
    ('FF15P', 'Final Fantasy XV Pocket Edition HD', '010068F00AA78000', [
        ('FF15P_FIRST', 'First Chapter', 'Complete the first chapter'),
        ('FF15P_FINAL', 'Final Chapter', 'Complete the final chapter'),
    ]),
    ('BAYONETTA', 'Bayonetta', '010076F0049A2000', [
        ('BAY_FIRST', 'First Chapter', 'Complete the first chapter'),
        ('BAY_FINAL', 'Final Chapter', 'Complete the final chapter'),
    ]),
    ('BAYONETTA2', 'Bayonetta 2', '01007960049A0000', [
        ('BAY2_FIRST', 'First Chapter', 'Complete the first chapter'),
        ('BAY2_FINAL', 'Final Chapter', 'Complete the final chapter'),
    ]),
    ('BAYONETTA3', 'Bayonetta 3', '01004A4010FEA000', [
        ('BAY3_FIRST', 'First Chapter', 'Complete the first chapter'),
        ('BAY3_FINAL', 'Final Chapter', 'Complete the final chapter'),
    ]),
    ('BAYORIGINS', 'Bayonetta Origins: Cereza and the Lost Demon', '0100CF5010FEC000', [
        ('BOR_FIRST', 'First Forest', 'Clear the first forest chapter'),
        ('BOR_FINAL', 'Final Chapter', 'Complete the main story'),
    ]),
    ('W101', 'The Wonderful 101: Remastered', '0100B1300FF08000', [
        ('W101_FIRST', 'First Mission', 'Complete your first mission'),
        ('W101_FINAL', 'Final Mission', 'Complete the final mission'),
    ]),

    # ---- Anime / fighters / sports ----
    ('NBA2K', 'NBA 2K20', '010026000E466000', [
        ('NBA_FIRST', 'First Game', 'Play your first NBA game'),
        ('NBA_RUMBLE', 'Rumble Champion', 'Win a title in MyCareer'),
    ]),
    ('MLB23', 'MLB The Show 23', '0100913019170000', [
        ('MLB_FIRST', 'First Game', 'Play your first game'),
        ('MLB_DIAMOND', 'Diamond Dynasty', 'Build a Diamond Dynasty team'),
    ]),
    ('FC24', 'EA SPORTS FC 24', '0100BDB01A0E6000', [
        ('FC_FIRST', 'First Match', 'Play your first match'),
        ('FC_ULTIMATE', 'Ultimate Team', 'Build your first Ultimate Team squad'),
    ]),
    ('THPS', "Tony Hawk's Pro Skater 1 + 2", '0100CC00102B4000', [
        ('THPS_FIRST', 'First Goal', 'Complete your first career goal'),
        ('THPS_ALL', 'All Goals', 'Complete every goal in both games'),
    ]),
    ('LEGOSTAR', 'LEGO Star Wars: The Skywalker Saga', '010042D00D900000', [
        ('LSW_FIRST', 'First Episode', 'Complete your first episode'),
        ('LSW_ALL', 'Skywalker Saga', 'Complete all nine episodes'),
    ]),
    ('LEGOMARVEL', 'LEGO Marvel Super Heroes 2', '0100D3A00409E000', [
        ('LMS2_FIRST', 'First Chapter', 'Complete the first story chapter'),
        ('LMS2_FINAL', 'Final Chapter', 'Complete the final story chapter'),
    ]),
    ('LEGOJUR', 'LEGO Jurassic World', '01001C100E772000', [
        ('LJW_FIRST', 'First Chapter', 'Complete the first story chapter'),
        ('LJW_ALL', 'Jurassic Analyst', 'Complete every story chapter'),
    ]),
    ('LEGOHARRY', 'LEGO Harry Potter Collection', '010052A00B5D2000', [
        ('LHP_FIRST', 'First Year', 'Complete your first year'),
        ('LHP_ALL', 'All Years', 'Complete every year of Hogwarts'),
    ]),
    ('LEGOCITY', 'LEGO CITY Undercover', '01003A30012C0000', [
        ('LCU_FIRST', 'First Case', 'Complete your first case'),
        ('LCU_ALL', 'Undercover Master', 'Complete every case'),
    ]),
    ('MK11', 'Mortal Kombat 11', '0100F2200C984000', [
        ('MK11_FIRST', 'First Match', 'Win your first match'),
        ('MK11_STORY', 'Story Complete', 'Complete the story mode'),
    ]),
    ('CIV6', 'Sid Meier’s Civilization VI', '010044500C182000', [
        ('CIV_FIRST', 'First City', 'Found your first city'),
        ('CIV_WIN', 'Victory', 'Win a match by any victory type'),
    ]),
    ('CITIES', 'Cities: Skylines - Nintendo Switch Edition', '0100D8800B87C000', [
        ('CS_FIRST', 'First City', 'Build your first city'),
        ('CS_POP', 'Metropolis', 'Reach 100,000 citizens'),
    ]),
    ('TROPICO', 'Tropico 6', '0100FBE0113CC000', [
        ('TRO_FIRST', 'First Term', 'Complete your first term as El Presidente'),
        ('TRO_FINAL', 'Final Term', 'Complete the final mission'),
    ]),
    ('NFSHP', 'Need for Speed Hot Pursuit Remastered', '010029B0118E8000', [
        ('NFS_FIRST', 'First Pursuit', 'Complete your first pursuit'),
        ('NFS_ALL', 'Racer Champion', 'Complete every event'),
    ]),
    ('BURNOUT', 'Burnout Paradise Remastered', '0100DBF01000A000', [
        ('BP_FIRST', 'First License', 'Earn your first driver license'),
        ('BP_ALL', 'Paradise Champion', 'Complete every event'),
    ]),
    ('GRID', 'GRID Autosport', '0100DC800A602000', [
        ('GRID_FIRST', 'First Race', 'Win your first race'),
        ('GRID_ALL', 'Autosport Champion', 'Win every championship'),
    ]),
    ('WRC8', 'WRC 8 FIA World Rally Championship', '010087800DCEA000', [
        ('WRC_FIRST', 'First Rally', 'Complete your first rally'),
        ('WRC_ALL', 'Rally Champion', 'Win the championship'),
    ]),
    ('MOTOGP24', 'MotoGP 24', '010040401D564000', [
        ('MOTO_FIRST', 'First Race', 'Complete your first race'),
        ('MOTO_CHAMP', 'World Champion', 'Win the championship'),
    ]),
    ('AC3', "Assassin's Creed III Remastered", '01007F600B134000', [
        ('AC3_FIRST', 'First Memory', 'Complete your first memory sequence'),
        ('AC3_FINAL', 'Final Memory', 'Complete the main story'),
    ]),
    ('ACREBEL', "Assassin's Creed: The Rebel Collection", '010044700DEB0000', [
        ('ACR_FIRST', 'First Mission', 'Complete your first mission'),
        ('ACR_ALL', 'Rebel Veteran', 'Complete both games'),
    ]),
    ('CTR', 'Crash Team Racing Nitro-Fueled', '0100F9F00C696000', [
        ('CTR_FIRST', 'First Cup', 'Win your first cup'),
        ('CTR_ALL', 'Nitro Champion', 'Win every cup'),
    ]),
    ('CRASHNSANE', 'Crash Bandicoot N. Sane Trilogy', '0100D1B006744000', [
        ('CNS_FIRST', 'First Level', 'Clear your first level'),
        ('CNS_ALL', 'Trilogy Master', 'Clear every level in all three games'),
    ]),
    ('SONICC', 'Sonic Colors: Ultimate', '010040E0116B8000', [
        ('SC_FIRST', 'First Act', 'Clear your first act'),
        ('SC_ALL', 'Wisp Master', 'Clear every act'),
    ]),
    ('SONICS', 'Sonic Superstars', '01008F701C074000', [
        ('SS_FIRST', 'First Zone', 'Clear the first zone'),
        ('SS_ALL', 'Superstar', 'Clear every zone'),
    ]),
    ('SAGES1', 'SEGA AGES Sonic The Hedgehog', '010051F00AC5E000', [
        ('SAGES1_FIRST', 'First Zone', 'Clear your first zone'),
        ('SAGES1_ALL', 'Classic Champion', 'Clear every zone'),
    ]),
    ('SAGES2', 'SEGA AGES Sonic The Hedgehog 2', '01000D200C614000', [
        ('SAGES2_FIRST', 'First Zone', 'Clear your first zone'),
        ('SAGES2_ALL', 'Classic Champion', 'Clear every zone'),
    ]),
    # Dragon Ball FighterZ is already in generate_achievements.py.

    # ---- Anime games ----
    ('DSLAYER', 'Demon Slayer: The Hinokami Chronicles', '0100309016E7A000', [
        ('DS_FIRST', 'First Match', 'Win your first match'),
        ('DS_STORY', 'Story Complete', 'Complete the story mode'),
    ]),
    ('JJK', 'Jujutsu Kaisen Cursed Clash', '010000B01A452000', [
        ('JJK_FIRST', 'First Match', 'Win your first match'),
        ('JJK_STORY', 'Story Complete', 'Complete the story mode'),
    ]),
    ('NARUTO4', 'Naruto Shippuden: Ultimate Ninja Storm 4', '010084D00CF5E000', [
        ('NAR_FIRST', 'First Battle', 'Win your first battle'),
        ('NAR_STORY', 'Story Complete', 'Complete the story mode'),
    ]),
    ('MHA2', "My Hero One's Justice 2", '01007E700DBF6000', [
        ('MHA_FIRST', 'First Battle', 'Win your first battle'),
        ('MHA_STORY', 'Story Complete', 'Complete the story mode'),
    ]),
    ('ONEPIECE', 'One Piece Odyssey', '0100D9601A994000', [
        ('OP_FIRST', 'First Chapter', 'Complete the first chapter'),
        ('OP_FINAL', 'Final Chapter', 'Complete the final chapter'),
    ]),
    ('GGST', 'Guilty Gear -Strive-', '0100AB401F136000', [
        ('GG_FIRST', 'First Match', 'Win your first match'),
        ('GG_STORY', 'Story Complete', 'Complete the story mode'),
    ]),
    ('SAMURAI', 'Samurai Shodown', '01002DF00F76C000', [
        ('SAM_FIRST', 'First Match', 'Win your first match'),
        ('SAM_STORY', 'Story Complete', 'Complete the story mode'),
    ]),
    ('POWERR', 'Power Rangers: Battle for the Grid', '0100E1E00CF1A000', [
        ('PR_FIRST', 'First Match', 'Win your first match'),
        ('PR_STORY', 'Story Complete', 'Complete the story mode'),
    ]),
    ('TRANSFORMERS', 'Transformers: Battlegrounds', '01005E500E528000', [
        ('TF_FIRST', 'First Mission', 'Complete your first mission'),
        ('TF_FINAL', 'Final Mission', 'Complete the campaign'),
    ]),
    ('HELLOKITTY', 'Hello Kitty Island Adventure', '010027901C89C000', [
        ('HK_FIRST', 'First Day', 'Complete your first day on the island'),
        ('HK_FRIENDS', 'Friend Collector', 'Befriend every visitor'),
    ]),

    # ---- Indie / sims ----
    ('MOVINGOUT', 'Moving Out', '0100C4C00E73E000', [
        ('MO_FIRST', 'First Job', 'Complete your first moving job'),
        ('MO_ALL', 'Master Mover', 'Complete every job'),
    ]),
    ('MOVINGOUT2', 'Moving Out 2', '010065D018172000', [
        ('MO2_FIRST', 'First Job', 'Complete your first moving job'),
        ('MO2_ALL', 'Master Mover', 'Complete every job'),
    ]),
    ('GOOSE', 'Untitled Goose Game', '010082400BCC6000', [
        ('GOOSE_FIRST', 'First To-Do', 'Complete your first to-do item'),
        ('GOOSE_ALL', 'Menace to Society', 'Complete every to-do item'),
    ]),
    ('BABA', 'Baba Is You', '01002CD00A51C000', [
        ('BABA_FIRST', 'First Level', 'Solve your first level'),
        ('BABA_ALL', 'Rule Bender', 'Solve every level'),
    ]),
    ('RO2', 'Risk of Rain 2', '010076D00E4BA000', [
        ('ROR2_FIRST', 'First Teleporter', 'Charge your first teleporter'),
        ('ROR2_FINAL', 'Final Boss', 'Defeat the final boss'),
    ]),
    ('SPLUNKY2', 'Spelunky 2', '01007EC013ABC000', [
        ('SP2_FIRST', 'First Cave', 'Reach the first cave'),
        ('SP2_FINAL', 'Final Boss', 'Defeat the final boss'),
    ]),
    ('STS', 'Slay the Spire', '010026300BA4A000', [
        ('STS_FIRST', 'First Act', 'Complete your first act'),
        ('STS_FINAL', 'Spire Slayer', 'Defeat the final boss'),
    ]),
    ('VSURV', 'Vampire Survivors', '010089A0197E4000', [
        ('VS_FIRST', 'First Minute', 'Survive your first minute'),
        ('VS_30', 'Half Hour Hero', 'Survive for 30 minutes in one run'),
    ]),
    ('BALATRO', 'Balatro', '0100CD801CE5E000', [
        ('BAL_FIRST', 'First Blind', 'Beat your first blind'),
        ('BAL_WIN', 'Final Boss', 'Win a full run'),
    ]),
    ('DAVE', 'Dave the Diver', '010097F018538000', [
        ('DAVE_FIRST', 'First Dive', 'Complete your first dive'),
        ('DAVE_REST', 'Sushi Master', 'Run your first successful sushi restaurant night'),
    ]),
    ('KATANA', 'Katana ZERO', '010029600D56A000', [
        ('KZ_FIRST', 'First Mission', 'Complete your first mission'),
        ('KZ_FINAL', 'Final Mission', 'Complete the final mission'),
    ]),
    ('BLOODSTAINED', 'Bloodstained: Ritual of the Night', '0100BF500207C000', [
        ('BS_FIRST', 'First Shard', 'Equip your first shard'),
        ('BS_FINAL', 'Final Boss', 'Defeat the final boss'),
    ]),
    ('CASTLEVANIA', 'Castlevania Advance Collection', '0100B33014710000', [
        ('CA_FIRST', 'First Game', 'Start your first Castlevania Advance game'),
        ('CA_ALL', 'Belmont Legacy', 'Complete all three games'),
    ]),
    ('RCG2', 'River City Girls 2', '0100026016320000', [
        ('RCG2_FIRST', 'First Mission', 'Complete your first mission'),
        ('RCG2_FINAL', 'Final Boss', 'Defeat the final boss'),
    ]),
    ('SCOTT', 'Scott Pilgrim vs. The World: The Game - Complete Edition', '0100394011C30000', [
        ('SP_FIRST', 'First Level', 'Clear your first level'),
        ('SP_ALL', 'Perfect Score', 'Complete every level'),
    ]),
    ('OKAMI', 'Okami HD', '0100276009872000', [
        ('OK_FIRST', 'First Brush', 'Use your first brush technique'),
        ('OK_FINAL', 'Final Boss', 'Defeat the final boss'),
    ]),
    ('REDDEAD', 'Red Dead Redemption', '01007820196A6000', [
        ('RDR_FIRST', 'First Mission', 'Complete your first mission'),
        ('RDR_FINAL', 'Final Mission', 'Complete the main story'),
    ]),
    ('TOMBRAIDER', 'Tomb Raider I-III Remastered', '010024601BB16000', [
        ('TR_FIRST', 'First Level', 'Clear your first level'),
        ('TR_ALL', 'Tomb Raider', 'Complete all three games'),
    ]),
    ('BORDERLANDS', 'Borderlands: Game of the Year Edition', '010064800F66A000', [
        ('BL_FIRST', 'First Mission', 'Complete your first mission'),
        ('BL_FINAL', 'Final Boss', 'Defeat the final boss'),
    ]),
    ('WOLF2', 'Wolfenstein II: The New Colossus', '01009040091E0000', [
        ('W2_FIRST', 'First Mission', 'Complete your first mission'),
        ('W2_FINAL', 'Final Mission', 'Complete the main story'),
    ]),
    ('METRO2033', 'Metro 2033 Redux', '0100D4900E82C000', [
        ('M2033_FIRST', 'First Station', 'Reach your first station'),
        ('M2033_FINAL', 'Final Boss', 'Complete the main story'),
    ]),
    ('METROLL', 'Metro: Last Light Redux', '0100F0400E850000', [
        ('MLL_FIRST', 'First Chapter', 'Complete the first chapter'),
        ('MLL_FINAL', 'Final Chapter', 'Complete the final chapter'),
    ]),
    ('BIOSHOCK', 'BioShock Remastered', '0100AD10102B2000', [
        ('BIOS_FIRST', 'First Plasmid', 'Use your first plasmid'),
        ('BIOS_FINAL', 'Final Boss', 'Complete the main story'),
    ]),
    ('PORTALK', 'Portal Knights', '0100437004170000', [
        ('PK_FIRST', 'First Island', 'Complete your first island'),
        ('PK_FINAL', 'Final Boss', 'Defeat the final boss'),
    ]),
    ('BRIDGEPORTAL', 'Bridge Constructor Portal', '010016E004796000', [
        ('BCP_FIRST', 'First Bridge', 'Build your first working bridge'),
        ('BCP_ALL', 'Chief Engineer', 'Complete every test chamber'),
    ]),
    ('HOUSEFLIP', 'House Flipper', '0100CAE00EB02000', [
        ('HF_FIRST', 'First Job', 'Complete your first renovation job'),
        ('HF_ALL', 'Master Flipper', 'Complete every job'),
    ]),
    ('POWERWASH', 'PowerWash Simulator', '0100926016012000', [
        ('PW_FIRST', 'First Job', 'Complete your first cleaning job'),
        ('PW_ALL', 'Spotless', 'Complete every job'),
    ]),
    ('PICOPARK', 'PICO PARK', '01004EA00DF70000', [
        ('PP_FIRST', 'First World', 'Clear the first world'),
        ('PP_ALL', 'Key Master', 'Collect every key'),
    ]),
    ('DUCKGAME', 'Duck Game', '0100750001C70000', [
        ('DG_FIRST', 'First Match', 'Win your first match'),
        ('DG_ALL', 'Duck Master', 'Complete every weekly challenge'),
    ]),
    ('DST', "Don't Starve Together", '010090100E334000', [
        ('DST_FIRST', 'First Day', 'Survive your first day'),
        ('DST_WINTER', 'Winter Survivor', 'Survive your first winter'),
    ]),
    ('GROUNDED', 'Grounded', '01006F301AE9C000', [
        ('GR_FIRST', 'First Night', 'Survive your first night'),
        ('GR_FINAL', 'Final Boss', 'Defeat the final boss'),
    ]),
    ('SUBNAUTICA', 'Subnautica', '0100429011144000', [
        ('SN_FIRST', 'First Base', 'Build your first base'),
        ('SN_FINAL', 'Final Rocket', 'Leave Planet 4546B'),
    ]),
    ('ASTRONEER', 'Astroneer', '0100E63013E60000', [
        ('AS_FIRST', 'First Base', 'Build your first base'),
        ('AS_FINAL', 'Final Launch', 'Launch the rocket and leave the planet'),
    ]),
    ('SLIME', 'Slime Rancher: Plortable Edition', '0100B9C0148D0000', [
        ('SR_FIRST', 'First Ranch', 'Complete your first day ranching'),
        ('SR_ALL', 'Ranch Master', 'Fill every plot in the ranch'),
    ]),
    ('GREENHELL', 'Green Hell', '0100453012FEA000', [
        ('GH_FIRST', 'First Night', 'Survive your first night'),
        ('GH_FINAL', 'Final Chapter', 'Complete the story mode'),
    ]),
    ('DBD', 'Dead by Daylight', '01004C400CF96000', [
        ('DBD_FIRST', 'First Match', 'Play your first match'),
        ('DBD_WIN', 'Escape Artist', 'Escape a trial as a survivor'),
    ]),
    ('OUTLAST2', 'Outlast 2', '0100DE70085E8000', [
        ('OL2_FIRST', 'First Chapter', 'Complete the first chapter'),
        ('OL2_FINAL', 'Final Chapter', 'Complete the final chapter'),
    ]),
    ('LN1', 'Little Nightmares Complete Edition', '01002FC00412C000', [
        ('LN_FIRST', 'First Chapter', 'Complete the first chapter'),
        ('LN_FINAL', 'Final Chapter', 'Complete the final chapter'),
    ]),
    ('LN2', 'Little Nightmares II', '010097100EDD6000', [
        ('LN2_FIRST', 'First Chapter', 'Complete the first chapter'),
        ('LN2_FINAL', 'Final Chapter', 'Complete the final chapter'),
    ]),
    ('LN3', 'Little Nightmares III', '010066101A55A000', [
        ('LN3_FIRST', 'First Chapter', 'Complete the first chapter'),
        ('LN3_FINAL', 'Final Chapter', 'Complete the final chapter'),
    ]),
    ('INSIDE', 'INSIDE', '0100D2D009028000', [
        ('IN_START', 'The Journey Begins', 'Begin your journey'),
        ('IN_END', 'Escape', 'Complete the final sequence'),
    ]),
    ('LIMBO', 'LIMBO', '01009C8009026000', [
        ('LIM_START', 'Into the Dark', 'Begin your journey'),
        ('LIM_END', 'Reunited', 'Complete the final sequence'),
    ]),
    ('FIREWATCH', 'Firewatch', '0100AC300919A000', [
        ('FW_FIRST', 'First Day', 'Complete your first day in the park'),
        ('FW_FINAL', 'Final Day', 'Complete the story'),
    ]),
    ('LIS', 'Life is Strange Remastered', '0100DC301186A000', [
        ('LIS_FIRST', 'First Episode', 'Complete the first episode'),
        ('LIS_FINAL', 'Final Episode', 'Complete the final episode'),
    ]),
    ('LISTC', 'Life is Strange: True Colors', '0100500012AB4000', [
        ('LITC_FIRST', 'First Episode', 'Complete the first episode'),
        ('LITC_FINAL', 'Final Episode', 'Complete the final episode'),
    ]),
    ('CATQUEST', 'Cat Quest III', '010088501B8F2000', [
        ('CQ3_FIRST', 'First Quest', 'Complete your first quest'),
        ('CQ3_FINAL', 'Final Boss', 'Defeat the final boss'),
    ]),
    ('MCDUNGEONS', 'Minecraft Dungeons', '01006C100EC08000', [
        ('MCD_FIRST', 'First Mission', 'Complete your first mission'),
        ('MCD_FINAL', 'Final Boss', 'Defeat the final boss'),
    ]),
]

# Slugs above whose Steam achievement lists are mirrored instead of the
# hand-written goals. Every appid was checked against Steam's achievement API.
STEAM_APPIDS = {
    'POWERWASH': 1290000, 'GROUNDED': 962130, 'SUBNAUTICA': 264710,
    'ASTRONEER': 1260320, 'SLIME': 433340, 'GREENHELL': 815370,
    'DBD': 381210, 'INSIDE': 304430, 'LIMBO': 48000, 'FIREWATCH': 383870,
    'BALATRO': 2379780, 'VSURV': 1794680, 'DAVE': 1868140,
    'KATANA': 460950, 'STS': 646570, 'RO2': 632360, 'BABA': 620980,
    'TOMBRAIDER': 2478970, 'REDDEAD': 1174180, 'CIV6': 289070,
    'CITIES': 255710, 'MK11': 976310, 'LEGOSTAR': 1142100,
    'LEGOHARRY': 1228870, 'HOUSEFLIP': 613100, 'PORTALK': 374040,
    'BRIDGEPORTAL': 642170, 'MOVINGOUT': 996770, 'MOVINGOUT2': 1641700,
    'GOOSE': 837470, 'WOLF2': 612880, 'METRO2033': 286690,
    'METROLL': 287390, 'BIOSHOCK': 409710, 'TROPICO': 492720,
    'LEGOMARVEL': 647830, 'LEGOJUR': 352400, 'WRC8': 1070330,
    'NFSHP': 1238300, 'CRASHNSANE': 731490, 'SONICC': 2055290,
    'SONICS': 2022670, 'MCDUNGEONS': 1672970, 'CATQUEST': 2305840,
    'SPLUNKY2': 418530, 'LN1': 424840, 'LN2': 860510, 'LN3': 1392860,
    'LISTC': 936790, 'GGST': 1384160, 'SAMURAI': 1342260,
    'OUTLAST2': 414700, 'DUCKGAME': 312450,
}

# (slug, display name, Switch title ID, Steam appid) for Steam-mirrored
# ports that are not in EXTRA_GAMES.
STEAM_EXTRA = [
    ('COOKINGSIM', 'Cooking Simulator', '01001E400FD58000', 758880),
    ('TWOM', 'This War of Mine: Complete Edition', '0100A8700BC2A000', 282070),
    ('PLAGUE', 'Plague Inc: Evolved', '01000CE00CBB8000', 246620),
    ('OC2', 'Overcooked! 2', '01006FD0080B2000', 728880),
    ('ARK', 'ARK: Survival Evolved', '0100D4A00B284000', 346110),
    ('DONTS', "Don't Starve: Nintendo Switch Edition", '0100751007ADA000', 328080),
    ('UNTILDAWN', 'Until Dawn', '01001E1025697001', 2172010),
    ('20MTD', '20 Minutes Till Dawn', '0100212019FB6000', 1966900),
    ('SILKSONG', 'Hollow Knight: Silksong', '010013C00E930000', 1030300),
    ('SONICXS', 'Sonic X Shadow Generations', '01005EA01C0FC000', 2513280),
    ('SONICFR', 'Sonic Forces', '01001270012B6000', 637100),
    ('TSR', 'Team Sonic Racing', '010092B0091D0000', 785260),
    ('SONICOR', 'Sonic Origins / Origins Plus', '01009FB016286000', 1794960),
    ('SONICCW', 'Sonic Racing CrossWorlds', '01006E001823C000', 2486820),
]

# Approved batch 9 additions. Kept in a separate module so the large original
# catalog stays easy to audit; the validator imports this file and sees them.
from new_games_batch9 import NEW_EXTRA_GAMES, NEW_STEAM_EXTRA

EXTRA_GAMES.extend(NEW_EXTRA_GAMES)
STEAM_EXTRA.extend(NEW_STEAM_EXTRA)
