"""Approved batch 11 indie games for NX-Achievements.

All title IDs were resolved from blawar/titledb US.en.json and checked against
the current catalog. Steam appids were verified against Steam achievement
schemas; only ports with at least 20 mirrored achievements are listed here.
"""

# Non-Steam games use the checklist module in tools/checklists/batch11.py.
NEW_EXTRA_GAMES = [
    ('RISKOFRAIN', 'Risk of Rain', '0100AAA00ACBE000', []),
    ('OWLBOY', 'Owlboy', '0100BC2004FF4000', []),
    ('WONDERBOYTRAP', 'Wonder Boy: The Dragon\'s Trap', '0100A6300150C000', []),
    ('VENBA', 'Venba', '01002F20193C6000', []),
    ('KTANE', 'Keep Talking and Nobody Explodes', '01008D400A584000', []),
    ('BADNORTH', 'Bad North', '0100E98006F22000', []),
]

# Steam ports mirrored by name/description only; no checklist goals are mixed in.
NEW_STEAM_EXTRA = [
    ('DUSK', 'DUSK', '01007740160D4000', 519860),
    ('ROGUELEGACY2', 'Rogue Legacy 2', '01007DA0134C0000', 1253920),
    ('DEADESTATE', 'Dead Estate', '01009DC017B4E000', 1484720),
    ('VOIDBASTARDS', 'Void Bastards', '0100D010113A8000', 857980),
    ('DUNGREED', 'Dungreed', '0100FAD00C2AA000', 753420),
    ('BACKPACKHERO', 'Backpack Hero', '0100B6301ABD6000', 1970580),
    ('SHOGUNSHOWDOWN', 'Shogun Showdown', '010096F01B4D8000', 2084000),
    ('BASTION', 'Bastion', '010038600B27E000', 107100),
    ('TRANSISTOR', 'Transistor', '0100BE500BEA2000', 237930),
    ('MESSENGER', 'The Messenger', '0100DC300AC78000', 764790),
    ('AXIOMV1', 'Axiom Verge', '0100052004384000', 332200),
    ('AXIOMV2', 'Axiom Verge 2', '01002FC010240000', 946030),
    ('RUINER', 'RUINER', '01006EC00F2CC000', 464060),
    ('FURI', 'Furi', '01009D3008D20000', 423230),
    ('SALTSANC', 'Salt and Sanctuary', '0100D250083B4000', 283640),
    ('BLASPHEMOUS1', 'Blasphemous', '0100698009C6E000', 774361),
    ('BLASPHEMOUS2', 'Blasphemous 2', '010040801A4C8000', 2114740),
    ('GREAK', 'Greak: Memories of Azur', '010045E012ECE000', 1311070),
    ('SWORDSDITTO', 'The Swords of Ditto: Mormo\'s Curse', '010037D00D568000', 619780),
    ('EASTWARD', 'Eastward', '010071B00F63A000', 977880),
    ('DINKUM', 'Dinkum', '0100A5A020D5E000', 1062520),
    ('GARDENSTORY', 'Garden Story', '0100B4D012490000', 1062140),
    ('LILGATOR', 'Lil Gator Game', '0100100016FB0000', 1586800),
    ('MONSANCT', 'Monster Sanctuary', '0100A0F00DA68000', 814370),
    ('SIRALIM', 'Siralim Ultimate', '0100AC1019560000', 1289810),
    ('WOBBLY', 'Wobbly Life', '010039501F11C000', 1211020),
    ('QUBE2', 'Q.U.B.E. 2', '010023600AA34000', 359100),
    ('MINIMETRO', 'Mini Metro', '0100091008272000', 287980),
    ('MINIMOTORWAYS', 'Mini Motorways', '01000D3015088000', 1127500),
    ('DORFO', 'Dorfromantik', '01007F2019132000', 1455840),
    ('STACKLANDS', 'Stacklands', '01008B701BEE8000', 1948280),
    ('NORTHGARD', 'Northgard', '0100A9E00D97A000', 466560),
]
