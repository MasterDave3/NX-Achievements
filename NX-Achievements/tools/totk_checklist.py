"""Tears of the Kingdom 100% goals based on IGN's completion checklist.

Each goal is (id, name, description, target). A target of 0 means a normal
A-toggle goal. Targeted goals are shown as current/target in the overlay and
A increments, X decrements, Y resets.

Counts come from IGN's TOTK 100% Completion Checklist:
https://www.ign.com/wikis/the-legend-of-zelda-tears-of-the-kingdom/100_Percent_Completion_Checklist
"""

TOTK_GOALS = [
    # Story / opening
    ('TOTK_SKY', 'Skyward Beginning', 'Complete the Great Sky Island opening', 0),
    ('TOTK_REGIONS', 'Regional Hero', 'Solve all four regional phenomena', 0),
    ('TOTK_GANON', 'Dragon Tamer', 'Defeat Ganondorf', 0),
    ('TOTK_STAR_SAVE', 'Completed Save Star', 'Beat the game and load the pre-boss save with a star', 0),

    # Map points that count toward the 100% map rating
    ('TOTK_KOROK', 'Korok Seeds', 'Find all 1,000 Korok Seeds (900 map points)', 1000),
    ('TOTK_NAMED', 'Named Locations', 'Discover all ~700 named map locations', 700),
    ('TOTK_CAVES', 'Cave Entrances', 'Find all 194 cave entrances', 194),
    ('TOTK_SHRINES', 'Shrines', 'Complete all 152 shrines', 152),
    ('TOTK_LIGHTROOTS', 'Lightroots', 'Activate all 120 Lightroots in the Depths', 120),
    ('TOTK_WELLS', 'Wells', 'Find all 58 wells', 58),
    ('TOTK_CHASMS', 'Chasm Entrances', 'Find all 35 chasm entrances', 35),
    ('TOTK_TOWNS', 'Towns, Settlements, and Stables', 'Register all ~35 towns, settlements, and stables', 35),
    ('TOTK_SHOPS', 'Specialty Shops', 'Find all ~43 specialty shops, including 7 Bargainer Statues', 43),
    ('TOTK_DISPENSERS', 'Zonai Device Dispensers', 'Activate all 30 Zonai Device Dispensers', 30),
    ('TOTK_SKYVIEW', 'Skyview Towers', 'Activate all 15 Skyview Towers', 15),
    ('TOTK_FORGES', 'Forge/Weapon Constructs and Refineries', 'Find all 14 Forge/Weapon Constructs and Refineries', 14),
    ('TOTK_DRAGON_TEARS', 'Tears of the Dragon', 'Collect all 12 Dragon Tears', 12),
    ('TOTK_TABLETS', 'Ancient Tablets', 'Decipher all 12 Ancient Tablets', 12),
    ('TOTK_FAIRIES', 'Great Fairy Fountains', 'Unlock all 5 Great Fairy Fountains, including Malanya', 5),
    ('TOTK_MAP_100', 'Map Completion', 'Reach 100% on the Purah Pad map', 100),

    # Adventure Log / Compendium counters
    ('TOTK_MAIN_QUESTS', 'Main Quests', 'Complete all 23 Main Quests', 23),
    ('TOTK_SIDE_ADVENTURES', 'Side Adventures', 'Complete all 60 Side Adventures', 60),
    ('TOTK_SHRINE_QUESTS', 'Shrine Quests', 'Complete all 31 Shrine Quests', 31),
    ('TOTK_SIDE_QUESTS', 'Side Quests', 'Complete all 139 Side Quests', 139),
    ('TOTK_MEMORIES', 'Memories', 'Find all 18 Memories, including 12 Dragon Tears', 18),
    ('TOTK_COMPENDIUM', 'Hyrule Compendium', 'Complete all 509 Compendium entries', 509),
    ('TOTK_RECIPES', 'Recipes', 'Register all 228 recipes', 228),

    # Gear and collectibles
    ('TOTK_ARMOR_SETS', 'Armor Sets', 'Collect all 36 armor sets', 36),
    ('TOTK_ARMOR_PIECES', 'Armor Pieces', 'Collect all 105 armor set pieces', 105),
    ('TOTK_UNIQUE_ARMOR', 'Unique Armor Pieces', 'Collect all 30 unique armor pieces', 30),
    ('TOTK_ENERGY_CELLS', 'Energy Cells', 'Unlock 21 Energy Cells for 8 full batteries', 21),
    ('TOTK_OVERCHARGED', 'Overcharged Energy Cells', 'Collect all 24 overcharged Blue Energy Cells', 24),
    ('TOTK_ZONAI_DEVICES', 'Zonai Devices', 'Unlock all 27 Zonai device types', 27),
    ('TOTK_PARAGLIDER', 'Paraglider Fabrics', 'Collect all 29 quest-reward paraglider fabrics', 29),
    ('TOTK_AMIIBO_FABRIC', 'Amiibo Paraglider Fabrics', 'Collect all 22 Amiibo-exclusive paraglider fabrics', 22),
    ('TOTK_SCHEMA_STONES', 'Schema Stones', 'Find all 12 Schema Stones', 12),
    ('TOTK_YIGA_SCHEMATICS', 'Yiga Schematics', 'Collect all 34 Yiga Schematics', 34),
    ('TOTK_OLD_MAPS', 'Old Maps', 'Find all 31 Old Maps', 31),
    ('TOTK_BUBBUL_GEMS', 'Bubbul Gems', 'Give all 147 Bubbul Gems to Koltin', 147),
    ('TOTK_TACKLE', 'Horse Tackle', 'Collect all 11 towing harnesses, saddles, and bridles', 11),
    ('TOTK_MEDALS', 'Medals of Honor', 'Earn all 6 Medals of Honor', 6),
    ('TOTK_ADDISON_SIGNS', 'Addison Signs', 'Put up all 81 Addison Signs', 81),

    # Key items
    ('TOTK_ALLS_WELL', "All's Well", 'Get the key item for finding all wells', 0),
    ('TOTK_DISPELLING_DARKNESS', 'Dispelling Darkness Medal', 'Light all Lightroots and get the medal', 0),
    ('TOTK_HESTU_GIFT', "Hestu's Gift", 'Find all 1,000 Koroks and get Hestu\'s Gift', 0),
]
