"""Fill out hand-written achievement lists to at least 20 goals per game.

These are manual goals for the Tesla overlay (A toggles them). They are not
claims about any game's built-in achievement system. Template nouns are chosen
per game category so each list reads naturally.
"""

CATEGORY_PARAMS = {
    'rpg': dict(unit='chapter', plural='chapters', collect='items', chars='party members',
                char='party member', boss='final boss'),
    'adventure': dict(unit='area', plural='areas', collect='items', chars='abilities',
                      char='ability', boss='final boss'),
    'platformer': dict(unit='level', plural='levels', collect='coins', chars='characters',
                       char='character', boss='final boss'),
    'racing': dict(unit='race', plural='races', collect='trophies', chars='racers',
                   char='racer', boss='final championship'),
    'fighter': dict(unit='match', plural='matches', collect='victories', chars='fighters',
                    char='fighter', boss='final opponent'),
    'party': dict(unit='board', plural='boards', collect='stars', chars='players',
                  char='player', boss='final board'),
    'sports': dict(unit='match', plural='matches', collect='points', chars='athletes',
                   char='athlete', boss='final tournament'),
    'shooter': dict(unit='mission', plural='missions', collect='supplies', chars='weapons',
                    char='weapon', boss='final boss'),
    'puzzle': dict(unit='puzzle', plural='puzzles', collect='stars', chars='hints',
                   char='hint', boss='final puzzle'),
    'sim': dict(unit='day', plural='days', collect='resources', chars='friends',
                char='friend', boss='final milestone'),
    'action': dict(unit='stage', plural='stages', collect='souls', chars='weapons',
                   char='weapon', boss='final boss'),
    'collection': dict(unit='minigame', plural='minigames', collect='points',
                       chars='activities', char='activity', boss='final challenge'),
}

# 20 template goals. Existing hand-written goals are kept, so games with 2-3
# stock goals end up with 22-23 total.
TEMPLATES = [
    ('01', 'First Steps', 'Complete your first {unit}'),
    ('02', 'Getting Started', 'Complete 5 {plural}'),
    ('03', 'Warming Up', 'Complete 10 {plural}'),
    ('04', 'Halfway There', 'Complete 25 {plural}'),
    ('05', 'Veteran', 'Complete 50 {plural}'),
    ('06', 'Story Complete', 'Finish every {unit} in the main story'),
    ('07', 'Collector', 'Collect 100 {collect}'),
    ('08', 'Treasure Hunter', 'Collect 500 {collect}'),
    ('09', 'Sharp Eyes', 'Find every collectible in one {unit}'),
    ('10', 'Perfectionist', 'Earn a perfect score in 5 {plural}'),
    ('11', 'Speedrunner', 'Complete a {unit} under the target time'),
    ('12', 'No Continues', 'Complete a {unit} without continuing'),
    ('13', 'Challenge Accepted', 'Complete a hard-difficulty {unit}'),
    ('14', 'Full Roster', 'Unlock every playable {chars}'),
    ('15', 'Mastery', 'Max out one {char}'),
    ('16', 'Side Objectives', 'Complete 10 side objectives'),
    ('17', 'Secret Finder', 'Discover every secret area'),
    ('18', 'Boss Slayer', 'Defeat 10 bosses'),
    ('19', 'Final Victory', 'Defeat the {boss}'),
    ('20', 'Full Clear', 'Finish the game with every main objective complete'),
]

OVERRIDES = {
    'ARMS': 'fighter', 'MINECRAFT': 'sim', 'ACNH': 'sim', 'GBG': 'sim', 'HELLOKITTY': 'sim',
    'DETECTIVE': 'adventure', 'LIS': 'adventure', 'OKAMI': 'adventure',
    'UNDERTALE': 'rpg', 'DELTARUNE': 'rpg', 'W101': 'action',
    'SMM2': 'platformer', 'MKLIVE': 'racing', 'UNITE': 'sports',
    'AC3': 'action', 'ACREBEL': 'action', 'ONEPIECE': 'adventure',
    'TRANSFORMERS': 'action', 'THPS': 'sports', 'GOVACATION': 'sim',
    'NSSPORTS': 'sports', 'MARIOSONIC': 'sports', 'PICOPARK': 'puzzle',
    'DST': 'sim', '12SWITCH': 'collection', 'CLUBHOUSE': 'collection',
    'JUSTDANCE': 'collection', 'FITBOX': 'collection', 'FITBOX2': 'collection',
    'RINGFIT': 'collection', 'WARIOWARE': 'collection',
    'WARIOWARE_MOVE': 'collection', 'BRAIN': 'collection',
}

def category_for(slug, name):
    if slug in OVERRIDES:
        return 'collection' if slug in {
            '12SWITCH', 'CLUBHOUSE', 'JUSTDANCE', 'FITBOX', 'FITBOX2',
            'RINGFIT', 'WARIOWARE', 'WARIOWARE_MOVE', 'BRAIN'
        } else OVERRIDES[slug]
    n = name.upper()
    checks = [
        (('POKEMON', 'FIRE EMBLEM', 'XENO', 'FINAL FANTASY', 'DRAGON QUEST',
          'PERSONA', 'SHIN MEGAMI', 'OCTOPATH', 'BRAVELY', 'NI NO KUNI',
          'TOKYO MIRAGE', 'CRISIS CORE'), 'rpg'),
        (('ZELDA', 'METROID', 'LUIGI', 'OKAMI'), 'adventure'),
        (('KART', 'RACING', 'BURNOUT', 'GRID', 'MOTOGP', 'CRASH TEAM'), 'racing'),
        (('SMASH', 'FIGHTER', 'SAMURAI', 'GUILTY GEAR', 'MORTAL KOMBAT',
          'NARUTO', 'JUJUTSU', 'DEMON SLAYER', 'MY HERO', 'POWER RANGERS',
          'BAYONETTA'), 'fighter'),
        (('PARTY', 'TENNIS', 'GOLF', 'SPORTS', 'STRIKERS', 'NBA', 'MLB',
          'EA SPORTS', 'OLYMPIC', 'SKATE'), 'sports'),
        (('SPLATOON', 'DIABLO', 'BORDERLANDS'), 'shooter'),
        (('PIKMIN', 'TOAD', 'CAPTAIN'), 'puzzle'),
        (('ANIMAL CROSSING', 'MINECRAFT', 'ISLAND', "DON'T STARVE"), 'sim'),
        (('WARRIORS', 'CASTLEVANIA', 'BLOODSTAINED', 'SCOTT PILGRIM',
          'RIVER CITY', 'ASSASSIN', 'WONDERFUL 101', 'LEGO', 'RABBIDS'), 'action'),
    ]
    for keywords, category in checks:
        if any(k in n for k in keywords):
            return category
    return 'platformer'


def expand_goals(slug, name, goals, minimum=20):
    """Return goals plus generated ones until `minimum` is reached."""
    out = list(goals)
    if len(out) >= minimum:
        return out
    category = category_for(slug, name)
    params = CATEGORY_PARAMS[category]
    seen = {g[0] for g in out}
    for suffix, title, template in TEMPLATES:
        if len(out) >= minimum:
            break
        aid = f'G{slug}_{suffix}'
        if aid in seen:
            continue
        seen.add(aid)
        out.append((aid, title, template.format(**params)))
    return out
