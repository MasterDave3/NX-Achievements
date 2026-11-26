#!/usr/bin/env python3
"""Generate data/achievements.txt for NX-Achievements.

Nintendo Switch title IDs come from blawar/titledb (US.en.json).
Steam achievement names/descriptions are mirrored from the Steam community
achievement pages for PC games that were ported to Switch.
"""
import importlib.util
import json
import re
import subprocess
import sys
from pathlib import Path

from games_extra import EXTRA_GAMES, STEAM_APPIDS, STEAM_EXTRA
from goals_extra import expand_goals
from totk_checklist import TOTK_GOALS, TOTK_SOURCE

TITLEDB = Path(sys.argv[1] if len(sys.argv) > 1 else '/tmp/titledb-US.json')
OUTPUT = Path(__file__).resolve().parent.parent / 'data' / 'achievements.txt'
SOURCE_OUTPUT = Path(__file__).resolve().parent.parent.parent / 'CHECKLIST_SOURCES.md'
CHECKLIST_DIR = Path(__file__).resolve().parent / 'checklists'


def load_checklists():
    """Load generated IGN-style goal batches keyed by game slug."""
    games = {}
    sources = {}
    if not CHECKLIST_DIR.is_dir():
        return games, sources
    for path in sorted(CHECKLIST_DIR.glob('batch*.py')):
        spec = importlib.util.spec_from_file_location(f'checklists.{path.stem}', path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        games.update(getattr(module, 'GAMES', {}))
        sources.update(getattr(module, 'SOURCES', {}))
    return games, sources

# slug, display name, Switch title ID, Steam appid (0 = no Steam mirror), goals
GAMES = [
    ('BOTW', 'The Legend of Zelda: Breath of the Wild', '01007EF00011E000', 0, [
        ('BOTW_FIRST', 'Great Plateau', 'Leave the Great Plateau in Breath of the Wild'),
        ('BOTW_BEASTS', 'Divine Beast Tamer', 'Free all four Divine Beasts'),
        ('BOTW_GANON', 'Calamity Slayer', 'Defeat Calamity Ganon'),
    ]),
    ('TOTK', 'The Legend of Zelda: Tears of the Kingdom', '0100F2C0115B6000', 0,
     TOTK_GOALS),
    ('MK8D', 'Mario Kart 8 Deluxe', '0100152000022000', 0, [
        ('MK8D_FIRST', 'First Grand Prix', 'Finish a Grand Prix in Mario Kart 8 Deluxe'),
        ('MK8D_150', '150cc Gold', 'Win gold in every 150cc cup'),
        ('MK8D_BCP', 'Booster Champion', 'Complete the Booster Course Pass cups'),
    ]),
    ('ODYSSEY', 'Super Mario Odyssey', '0100000000010000', 0, [
        ('ODY_KINGDOM', 'Kingdom Hopper', 'Visit your first kingdom'),
        ('ODY_MOONS', 'Moon Collector', 'Collect every Power Moon'),
        ('ODY_BOWSER', 'Wedding Crasher', 'Defeat Bowser and save Peach'),
    ]),
    ('SSBU', 'Super Smash Bros. Ultimate', '01006A800016E000', 0, [
        ('SSBU_FIRST', 'First Fighter', 'Play a match in Super Smash Bros. Ultimate'),
        ('SSBU_CLOUD', 'Cloud Strife', 'Win a match with Cloud'),
        ('SSBU_LIGHT', 'World of Light', 'Complete World of Light'),
    ]),
    ('ZA', 'Pokemon Legends Z-A', '0100F43008C44000', 0, [
        ('ZA_MASTER', 'Kalos Champion', 'Finish the main story of Pokemon Legends Z-A'),
        ('ZA_COLLECTOR', 'Pokedex Collector', 'Register every Pokemon in the Pokedex'),
        ('ZA_RICH', 'Deep Pockets', 'Hold 999,999 money in Z-A'),
        ('ZA_STARTER', 'Totodile Partner', 'Have Totodile in your party'),
    ]),
    ('SCARLET', 'Pokemon Scarlet', '0100A3D008C5C000', 0, [
        ('SCAR_GYM', 'Gym Challenger', 'Earn your first Gym Badge'),
        ('SCAR_CHAMP', 'Paldea Champion', 'Become the champion of Paldea'),
        ('SCAR_AREAZERO', 'Area Zero', 'Reach the bottom of Area Zero'),
    ]),
    ('VIOLET', 'Pokemon Violet', '01008F6008C5E000', 0, [
        ('VIO_GYM', 'Gym Challenger', 'Earn your first Gym Badge'),
        ('VIO_CHAMP', 'Paldea Champion', 'Become the champion of Paldea'),
        ('VIO_AREAZERO', 'Area Zero', 'Reach the bottom of Area Zero'),
    ]),
    ('ARCEUS', 'Pokemon Legends Arceus', '01001F5010DFA000', 0, [
        ('ARC_FIRST', 'New Explorer', 'Complete your first mission'),
        ('ARC_DEX', 'Hisui Researcher', 'Complete the Hisui Pokedex'),
        ('ARC_NOBLE', 'Noble Builder', 'Defeat every noble Pokemon'),
    ]),
    ('SWORD', 'Pokemon Sword', '0100ABF008968000', 0, [
        ('SWORD_GYM', 'Gym Challenger', 'Earn your first Gym Badge'),
        ('SWORD_CHAMP', 'Galar Champion', 'Become the Galar champion'),
        ('SWORD_CROWN', 'Crown Tundra', 'Complete the Crown Tundra storyline'),
    ]),
    ('SHIELD', 'Pokemon Shield', '01008DB008C2C000', 0, [
        ('SHIELD_GYM', 'Gym Challenger', 'Earn your first Gym Badge'),
        ('SHIELD_CHAMP', 'Galar Champion', 'Become the Galar champion'),
        ('SHIELD_CROWN', 'Crown Tundra', 'Complete the Crown Tundra storyline'),
    ]),
    ('LETSGO_P', 'Pokemon Lets Go Pikachu', '010003F003A34000', 0, [
        ('LGP_GYM', 'Gym Challenger', 'Earn your first Gym Badge'),
        ('LGP_ELITE', 'Elite Four', 'Defeat the Elite Four'),
        ('LGP_MASTER', 'Master Trainer', 'Catch a legendary Pokemon'),
    ]),
    ('LETSGO_E', 'Pokemon Lets Go Eevee', '0100187003A36000', 0, [
        ('LGE_GYM', 'Gym Challenger', 'Earn your first Gym Badge'),
        ('LGE_ELITE', 'Elite Four', 'Defeat the Elite Four'),
        ('LGE_MASTER', 'Master Trainer', 'Catch a legendary Pokemon'),
    ]),
    ('ACNH', 'Animal Crossing New Horizons', '01006F8002326000', 0, [
        ('ACNH_ISLAND', 'Island Life', 'Set up your first island'),
        ('ACNH_MUSEUM', 'Museum Curator', 'Complete the museum collection'),
        ('ACNH_BELLS', 'Bell Millionaire', 'Hold one million Bells'),
    ]),
    ('SPLATOON3', 'Splatoon 3', '0100C2500FC20000', 0, [
        ('S3_TURF', 'Turf Starter', 'Win your first Turf War'),
        ('S3_SALMON', 'Salmon Run', 'Clear a Salmon Run shift'),
        ('S3_STORY', 'Splatlands Hero', 'Complete the single-player campaign'),
    ]),
    ('SPLATOON2', 'Splatoon 2', '01003BC0000A0000', 0, [
        ('S2_TURF', 'Turf Starter', 'Win your first Turf War'),
        ('S2_SALMON', 'Salmon Run', 'Clear a Salmon Run shift'),
        ('S2_OCTO', 'Octo Expansion', 'Complete the Octo Expansion'),
    ]),
    ('SMP', 'Super Mario Party', '010036B0034E4000', 0, [
        ('SMP_MINI', 'Minigame Rookie', 'Play your first minigame'),
        ('SMP_STARS', 'Star Collector', 'Win a board with the most stars'),
    ]),
    ('MPSS', 'Mario Party Superstars', '01006FE013472000', 0, [
        ('MPSS_MINI', 'Minigame Rookie', 'Play your first minigame'),
        ('MPSS_STARS', 'Star Collector', 'Win a board with the most stars'),
    ]),
    ('RABBIDS_H', 'Mario + Rabbids Sparks of Hope', '0100317013770000', 0, [
        ('RSOH_FIRST', 'First Battle', 'Win your first tactical battle'),
        ('RSOH_SPARKS', 'Spark Hunter', 'Collect every Spark'),
        ('RSOH_BOSS', 'Galaxy Savior', 'Defeat the final boss'),
    ]),
    ('RABBIDS_KB', 'Mario + Rabbids Kingdom Battle', '010067300059A000', 0, [
        ('RKB_FIRST', 'First Battle', 'Win your first tactical battle'),
        ('RKB_WORLDS', 'World Explorer', 'Clear every world'),
        ('RKB_CHALLENGE', 'Challenge Accepted', 'Complete a challenge map'),
    ]),
    ('LM3', 'Luigis Mansion 3', '0100DCA0064A6000', 0, [
        ('LM3_FLOOR', 'First Floor', 'Clear the first hotel floor'),
        ('LM3_HOTEL', 'Hotel Master', 'Clear every floor of the hotel'),
        ('LM3_KINGBOO', 'Ghost Hunter', 'Defeat King Boo'),
    ]),
    ('SMM2', 'Super Mario Maker 2', '01009B90006DC000', 0, [
        ('SMM2_MAKE', 'First Course', 'Publish your first course'),
        ('SMM2_PLAY', 'Course Explorer', 'Play 100 Endless courses'),
        ('SMM2_STORY', 'Course Builder', 'Complete the story mode'),
    ]),
    ('MTENNIS', 'Mario Tennis Aces', '0100BDE00862A000', 0, [
        ('MTENNIS_FIRST', 'First Match', 'Win a tennis match'),
        ('MTENNIS_SWING', 'Swing Mode', 'Complete a Swing Mode challenge'),
        ('MTENNIS_TOURNEY', 'Tournament Champion', 'Win a tournament'),
    ]),
    ('MGOLF', 'Mario Golf Super Rush', '0100C9C00E25C000', 0, [
        ('MGOLF_ROUND', 'First Round', 'Complete a round of golf'),
        ('MGOLF_SPEED', 'Speed Golf', 'Win a Speed Golf match'),
        ('MGOLF_RECORD', 'Course Record', 'Set a course record'),
    ]),
    ('FE3H', 'Fire Emblem Three Houses', '010055D009F78000', 0, [
        ('FE3H_FIRST', 'First Battle', 'Win your first battle'),
        ('FE3H_RECRUIT', 'House Leader', 'Recruit every student'),
        ('FE3H_FINAL', 'Final Battle', 'Complete the final battle'),
    ]),
    ('FE_ENGAGE', 'Fire Emblem Engage', '0100A6301214E000', 0, [
        ('FEE_FIRST', 'First Battle', 'Win your first battle'),
        ('FEE_EMBLEMS', 'Emblem Collector', 'Summon every Emblem'),
        ('FEE_FINAL', 'Final Battle', 'Complete the final battle'),
    ]),
    ('XC2', 'Xenoblade Chronicles 2', '0100E95004038000', 0, [
        ('XC2_FIRST', 'First Battle', 'Win your first battle'),
        ('XC2_BLADES', 'Blade Collector', 'Collect every Blade'),
        ('XC2_FINAL', 'Final Battle', 'Complete the main story'),
    ]),
    ('XC3', 'Xenoblade Chronicles 3', '010074F013262000', 0, [
        ('XC3_FIRST', 'First Battle', 'Win your first battle'),
        ('XC3_HEROES', 'Hero Collector', 'Unlock every Hero'),
        ('XC3_FINAL', 'Final Battle', 'Complete the main story'),
    ]),
    ('XC1', 'Xenoblade Chronicles Definitive Edition', '0100FF500E34A000', 0, [
        ('XC1_FIRST', 'First Battle', 'Win your first battle'),
        ('XC1_SKETCH', 'Collector', 'Complete the Collectopedia'),
        ('XC1_FINAL', 'Final Battle', 'Complete the main story'),
    ]),
    ('DREAD', 'Metroid Dread', '010093801237C000', 0, [
        ('DREAD_FIRST', 'First Area', 'Leave the first area'),
        ('DREAD_MEDALLION', 'Medallion Hunter', 'Collect every E-Medallion'),
        ('DREAD_RAVEN', 'Raven Buster', 'Defeat Raven Beak'),
    ]),
    ('PRIME', 'Metroid Prime Remastered', '010012101468C000', 0, [
        ('PRIME_SCAN', 'First Scan', 'Scan your first object'),
        ('PRIME_ARTIFACT', 'Artifact Hunter', 'Collect all 12 artifacts'),
        ('PRIME_BOSS', 'Prime Slayer', 'Defeat Metroid Prime'),
    ]),
    ('AOC', 'Hyrule Warriors Age of Calamity', '01002B00111A2000', 0, [
        ('AOC_FIRST', 'First Battle', 'Complete your first battle'),
        ('AOC_ALL', 'Warrior', 'Complete every battle'),
        ('AOC_CALAMITY', 'Calamity Slayer', 'Defeat the Calamity'),
    ]),
    ('LA', 'Zelda Links Awakening', '01006BB00C6F0000', 0, [
        ('LA_DUNGEON', 'First Dungeon', 'Complete your first dungeon'),
        ('LA_ALL', 'Dungeon Master', 'Complete every dungeon'),
        ('LA_WIND', 'Wind Fish', 'Awaken the Wind Fish'),
    ]),
    ('S3DW', 'Super Mario 3D World Bowsers Fury', '010028600EBDA000', 0, [
        ('S3DW_WORLD', 'First World', 'Clear the first world'),
        ('S3DW_ALL', 'World Champion', 'Clear every world'),
        ('S3DW_FURY', 'Fury Buster', "Defeat Bowser's Fury"),
    ]),
    ('NSMBU', 'New Super Mario Bros U Deluxe', '0100EA80032EA000', 0, [
        ('NSMBU_WORLD', 'First World', 'Clear the first world'),
        ('NSMBU_ALL', 'World Champion', 'Clear every world'),
        ('NSMBU_BOWSER', 'Bowser Buster', 'Defeat Bowser'),
    ]),
    ('DKC', 'Donkey Kong Country Tropical Freeze', '0100C1F0051B6000', 0, [
        ('DKC_ISLAND', 'First Island', 'Clear the first island'),
        ('DKC_ALL', 'Island Hopper', 'Clear every island'),
        ('DKC_FREDRIK', 'Frozen Fury', 'Defeat Lord Fredrik'),
    ]),
    ('TOAD', 'Captain Toad Treasure Tracker', '01009BF0072D4000', 0, [
        ('TOAD_FIRST', 'First Course', 'Clear your first course'),
        ('TOAD_ALL', 'Treasure Hunter', 'Clear every course'),
        ('TOAD_GEM', 'Gem Collector', 'Collect every gem'),
    ]),
    ('KIRBY_FL', 'Kirby and the Forgotten Land', '01004D300C5AE000', 0, [
        ('KFL_STAGE', 'First Stage', 'Clear your first stage'),
        ('KFL_TREASURE', 'Treasure Hunter', 'Complete every Treasure Road'),
        ('KFL_BOSS', 'Final Boss', 'Defeat the final boss'),
    ]),
    ('KIRBY_SA', 'Kirby Star Allies', '01007E3006DDA000', 0, [
        ('KSA_STAGE', 'First Stage', 'Clear your first stage'),
        ('KSA_FRIENDS', 'Friend Collector', 'Recruit every Dream Friend'),
        ('KSA_BOSS', 'Final Boss', 'Defeat the final boss'),
    ]),
    ('KIRBY_RTDL', 'Kirby Return to Dream Land Deluxe', '01006B601380E000', 0, [
        ('KRTDL_STAGE', 'First Stage', 'Clear your first stage'),
        ('KRTDL_ALL', 'Stage Master', 'Clear every stage'),
        ('KRTDL_BOSS', 'Final Boss', 'Defeat the final boss'),
    ]),
    ('YOSHI', 'Yoshis Crafted World', '01006000040C2000', 0, [
        ('YOSHI_WORLD', 'First World', 'Clear the first world'),
        ('YOSHI_SOUVENIR', 'Souvenir Collector', 'Collect every souvenir'),
        ('YOSHI_BOSS', 'Final Boss', 'Defeat the final boss'),
    ]),
    ('PIKMIN3', 'Pikmin 3 Deluxe', '0100F4C009322000', 0, [
        ('P3_FIRST', 'First Area', 'Complete your first area'),
        ('P3_FRUIT', 'Fruit Collector', 'Collect all fruit types'),
        ('P3_BOSS', 'Final Boss', 'Defeat the final boss'),
    ]),
    ('PIKMIN4', 'Pikmin 4', '0100B7C00933A000', 0, [
        ('P4_FIRST', 'First Area', 'Complete your first area'),
        ('P4_TREASURE', 'Treasure Hunter', 'Collect every treasure'),
        ('P4_BOSS', 'Final Boss', 'Defeat the final boss'),
    ]),
    ('WARIOWARE', 'Warioware Get it Together', '0100563010E0C000', 0, [
        ('WW_FIRST', 'First Minigame', 'Play your first minigame'),
        ('WW_ALL', 'Minigame Master', 'Play every minigame'),
    ]),
    ('12SWITCH', '1-2-Switch', '01000320000CC000', 0, [
        ('12_FIRST', 'First Game', 'Play your first 1-2-Switch game'),
        ('12_ALL', 'Party Starter', 'Try every game'),
    ]),
    ('ARMS', 'ARMS', '01009B500007C000', 0, [
        ('ARMS_FIRST', 'First Match', 'Win your first ARMS match'),
        ('ARMS_FIGHTERS', 'Fighter Collector', 'Unlock every fighter'),
        ('ARMS_GRAND', 'Grand Slam', 'Win a Grand Slam tournament'),
    ]),
    ('RINGFIT', 'Ring Fit Adventure', '01002FF008C24000', 0, [
        ('RFA_FIRST', 'First Workout', 'Complete your first workout'),
        ('RFA_WORLDS', 'World Traveler', 'Complete every world'),
        ('RFA_BOSS', 'Fitness Hero', 'Defeat the final boss'),
    ]),
    ('NSSPORTS', 'Nintendo Switch Sports', '0100D2F00D5C0000', 0, [
        ('NSS_FIRST', 'First Match', 'Play your first sport match'),
        ('NSS_ALL', 'All-Rounder', 'Try every sport'),
        ('NSS_GOLD', 'Gold Medal', 'Win an online gold medal'),
    ]),
    ('STRIKERS', 'Mario Strikers Battle League', '010019401051C000', 0, [
        ('STRIKERS_FIRST', 'First Match', 'Win your first Strikers match'),
        ('STRIKERS_CUP', 'Cup Champion', 'Win a tournament cup'),
    ]),
    ('ADVANCEWARS', 'Advance Wars 1+2 Re-Boot Camp', '0100300012F2A000', 0, [
        ('AW_FIRST', 'First Mission', 'Complete your first mission'),
        ('AW_CAMPAIGN', 'Campaign Veteran', 'Complete both campaigns'),
    ]),
    ('UNITE', 'Pokemon UNITE', '0100939011ED4000', 0, [
        ('UNITE_FIRST', 'First Match', 'Play your first Unite match'),
        ('UNITE_MASTER', 'Master Rank', 'Reach Master rank'),
    ]),
    ('WONDER', 'Super Mario Bros Wonder', '010015100B514000', 0, [
        ('WONDER_FIRST', 'First World', 'Clear the first world'),
        ('WONDER_WONDERS', 'Wonder Collector', 'Collect every Wonder Flower'),
        ('WONDER_CASTLE', 'Final Castle', 'Complete the Special World'),
    ]),
    ('MINECRAFT', 'Minecraft', '0100D71004694000', 0, [
        ('MC_NIGHT', 'First Night', 'Survive your first night'),
        ('MC_NETHER', 'Nether Portal', 'Build a Nether portal'),
        ('MC_ENDER', 'Ender Dragon', 'Defeat the Ender Dragon'),
    ]),
    ('DIABLO3', 'Diablo III Eternal Collection', '01001B300B9BE000', 0, [
        ('D3_FIRST', 'First Quest', 'Complete your first quest'),
        ('D3_70', 'Level 70', 'Reach level 70'),
        ('D3_TORMENT', 'Torment Slayer', 'Clear a Torment difficulty rift'),
    ]),
    ('UNDERTALE', 'Undertale', '010080B00AD66000', 0, [
        ('UT_ROUTE', 'First Route', 'Finish a route'),
        ('UT_PACIFIST', 'True Pacifist', 'Complete the True Pacifist route'),
        ('UT_NO_MERCY', 'No Mercy', 'Complete the Genocide route'),
    ]),
    ('DELTARUNE', 'Deltarune', '0100A0D022A68000', 0, [
        ('DR_CH1', 'Chapter 1', 'Complete Chapter 1'),
        ('DR_CH2', 'Chapter 2', 'Complete Chapter 2'),
        ('DR_SECRET', 'Secret Boss', 'Defeat a secret boss'),
    ]),
    ('MKLIVE', 'Mario Kart Live Home Circuit', '0100ED100BA3A000', 0, [
        ('MKL_FIRST', 'First Race', 'Complete your first race'),
        ('MKL_CUP', 'Cup Champion', 'Win a cup'),
    ]),

    # ---- PC games ported to Switch: Steam achievements are mirrored below ----
    ('TERRARIA', 'Terraria', '0100E46006708000', 105600, []),
    ('STARDEW', 'Stardew Valley', '0100E65002BB8000', 413150, []),
    ('HOLLOW', 'Hollow Knight', '0100633007D48000', 367520, []),
    ('ISAAC', 'The Binding of Isaac Afterbirth+', '010021C000B6A000', 250900, []),
    ('GUNGEON', 'Enter the Gungeon', '01009D60076F6000', 311690, []),
    ('DEADCELLS', 'Dead Cells', '0100646009FBE000', 588650, []),
    ('CELESTE', 'Celeste', '01002B30028F6000', 504230, []),
    ('CUPHEAD', 'Cuphead', '0100A5C00D162000', 268910, []),
    ('HADES', 'Hades', '0100535012974000', 1145360, []),
    ('SKYRIM', 'The Elder Scrolls V Skyrim', '01000A10041EA000', 489830, []),
    ('DOOM', 'DOOM', '0100416004C00000', 379720, []),
    ('DOOME', 'DOOM Eternal', '0100B1A00D8CE000', 782330, []),
    ('ROCKETLEAGUE', 'Rocket League', '01005EE0036EC000', 252950, []),
    ('AMONGUS', 'Among Us', '0100B0C013912000', 945360, []),
    ('FALLGUYS', 'Fall Guys', '0100C3C015738000', 1097150, []),
    ('ORI_WISPS', 'Ori and the Will of the Wisps', '01008DD013200000', 1057090, []),
    ('ORI_BLIND', 'Ori and the Blind Forest', '010061D00DB74000', 387290, []),
    ('SHOVEL', 'Shovel Knight Treasure Trove', '010057D0021E8000', 250760, []),
    ('SONICF', 'Sonic Frontiers', '01004AD014BF0000', 1237320, []),
    ('SONICM', 'Sonic Mania', '01009AA000FAA000', 584400, []),
    ('CRASH4', 'Crash Bandicoot 4 Its About Time', '010073401175E000', 1378990, []),
    ('SPYRO', 'Spyro Reignited Trilogy', '010077B00E046000', 996580, []),
    ('MHR', 'Monster Hunter Rise', '0100B04011742000', 1446780, []),
    ('MHS2', 'Monster Hunter Stories 2 Wings of Ruin', '0100E21011446000', 1277400, []),
    ('RE4', 'Resident Evil 4', '010099A00BC1E000', 254700, []),
    ('RE8', 'Resident Evil Village', '0100CA0018C52000', 1196590, []),
    ('RE2', 'Resident Evil 2', '01008800185B2000', 883710, []),
    ('DBFZ', 'Dragon Ball FighterZ', '0100A250097F0000', 678950, []),
    ('P5R', 'Persona 5 Royal', '01005CA01580E000', 1687950, []),
    ('FF8', 'Final Fantasy VIII Remastered', '01008B900DC0A000', 1026680, []),
    ('WITCHER3', 'The Witcher 3 Wild Hunt', '0100BFE00E9CA000', 292030, []),
    ('DISCO', 'Disco Elysium The Final Cut', '01006C5015E84000', 632470, []),
    ('DOS2', 'Divinity Original Sin 2', '010027400CDC6000', 435150, []),
    ('OVERCOOKED', 'Overcooked All You Can Eat', '0100F28011892000', 1243830, []),
]


def clean(value):
    value = str(value or '').replace('|', '/')
    value = value.replace('\r', ' ').replace('\n', ' ')
    value = re.sub(r'\s+', ' ', value).strip()
    return value[:180]


def steam_achievements(appid):
    url = f'https://steamcommunity.com/stats/{appid}/achievements/?l=english'
    html = subprocess.run(['curl', '-sL', '--max-time', '40', '-A', 'Mozilla/5.0', url],
                          capture_output=True, check=True).stdout.decode('utf8', 'replace')
    match = re.search(r'<script type="application/json" id="valve-ssr-data"[^>]*>(.*?)</script>', html, re.S)
    if not match:
        raise RuntimeError(f'no Steam SSR data for {appid}')
    state = json.loads(match.group(1))
    query_data = json.loads(state['renderContext']['queryData'])
    for query in query_data.get('queries', []):
        data = query.get('state', {}).get('data')
        if isinstance(data, dict) and data.get('appid') == appid and 'groups' in data:
            achievements = []
            for group in data['groups']:
                achievements.extend(group.get('achievements', []))
            return achievements
    raise RuntimeError(f'no achievement schema for {appid}')


def main():
    if not TITLEDB.exists():
        raise SystemExit(f'titledb not found: {TITLEDB}')
    titledb = json.loads(TITLEDB.read_text())
    ids = {str(v.get('id')).upper() for v in titledb.values()
           if isinstance(v, dict) and v.get('id')}

    lines = [
        '# NX-Achievements definitions',
        '# Format: TitleID|AchievementID|Name|Description[|Target]',
        '# Use * as TitleID to show for every game.',
        '# A toggles, or with a Target counts up (+1); X counts down; Y resets.',
        '# Steam achievements are mirrored by name and description only;',
        '# the overlay cannot read or unlock Steam achievements automatically.',
        '',
        '*|FIRST_BOOT|First Boot|Open NX-Achievements at least once',
        '',
    ]

    checklists, sources = load_checklists()
    sources['TOTK'] = TOTK_SOURCE
    seen_checklist_ids = set()
    for slug, goals in checklists.items():
        for goal in goals:
            aid = goal[0]
            if aid in seen_checklist_ids:
                raise SystemExit(f'duplicate checklist ID: {aid} ({slug})')
            seen_checklist_ids.add(aid)

    all_games = list(GAMES)
    for slug, name, title_id, goals in EXTRA_GAMES:
        all_games.append((slug, name, title_id, STEAM_APPIDS.get(slug, 0), goals))
    for slug, name, title_id, appid in STEAM_EXTRA:
        all_games.append((slug, name, title_id, appid, []))

    total = 0
    for slug, name, title_id, appid, goals in all_games:
        if title_id not in ids:
            raise SystemExit(f'title ID not found in titledb: {name} {title_id}')
        lines.append(f'# {name} ({title_id})')
        entries = []
        if appid:
            try:
                for achievement in steam_achievements(appid):
                    api = re.sub(r'[^A-Za-z0-9_]', '_', achievement.get('api_name', ''))[:40]
                    aid = f'S{appid}_{api}'
                    title = clean(achievement.get('name')) or f'Steam achievement {api}'
                    desc = clean(achievement.get('description')) or 'Mirrored from Steam'
                    entries.append((aid, title, desc))
            except Exception as exc:
                print(f'warning: Steam {appid} ({name}) failed: {exc}; using local goals',
                      file=sys.stderr)
                entries = goals
        else:
            entries = checklists.get(slug, goals)
        entries = expand_goals(slug, name, entries)
        seen = set()
        for entry in entries:
            if len(entry) == 4:
                aid, title, desc, target = entry
            else:
                aid, title, desc = entry
                target = 0
            if aid in seen:
                continue
            seen.add(aid)
            line = f'{title_id}|{clean(aid)}|{clean(title)}|{clean(desc)}'
            if target:
                line += f'|{int(target)}'
            lines.append(line)
            total += 1
        lines.append('')

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text('\n'.join(lines).rstrip() + '\n')

    source_lines = [
        '# Checklist sources',
        '',
        'Sources used for the non-Steam IGN-style checklist goals. Steam ports',
        'are deliberately omitted because they mirror real Steam achievements.',
        '',
        '| Game | Slug | Source |',
        '|---|---|---|',
    ]
    names = {slug: name for slug, name, _, _, _ in all_games}
    for slug in sorted(sources, key=lambda s: names.get(s, s)):
        url = sources[slug] or 'No source found'
        source_lines.append(f'| {names.get(slug, slug)} | `{slug}` | {url} |')
    SOURCE_OUTPUT.write_text('\n'.join(source_lines).rstrip() + '\n')

    print(f'Wrote {total} achievements for {len(all_games)} games -> {OUTPUT}')
    print(f'Wrote {len(sources)} checklist sources -> {SOURCE_OUTPUT}')


if __name__ == '__main__':
    main()
