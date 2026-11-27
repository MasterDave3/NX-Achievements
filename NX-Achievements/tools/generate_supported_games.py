#!/usr/bin/env python3
"""Generate SUPPORTED_GAMES.md from the generated achievement data."""
import re
from pathlib import Path

from games_extra import EXTRA_GAMES, STEAM_APPIDS, STEAM_EXTRA
from generate_achievements import GAMES

ROOT = Path(__file__).resolve().parent.parent.parent
DATA = ROOT / 'NX-Achievements' / 'data' / 'achievements.txt'
OUTPUT = ROOT / 'SUPPORTED_GAMES.md'


def non_steam_count():
    steam = {s for s, _, _, _ in STEAM_EXTRA} | set(STEAM_APPIDS)
    games = {s for s, _, _, appid, _ in GAMES if not appid}
    games |= {s for s, _, _, _ in EXTRA_GAMES if s not in steam}
    return len(games)


def main():
    games = []
    current = None
    countable = 0
    for line in DATA.read_text(encoding='utf8').splitlines():
        header = re.match(r'^# (.+) \(([0-9A-F*]{16,})\)$', line)
        if header:
            current = [header.group(1), header.group(2), 0]
            games.append(current)
            continue
        if not line or line.startswith('#'):
            continue
        if current is not None:
            current[2] += 1
            if len(line.split('|')) == 5:
                countable += 1

    lines = [
        '# Supported games',
        '',
        'Every game below has at least 20 achievements in '
        '`NX-Achievements/data/achievements.txt`.',
        'Switch title IDs come from [blawar/titledb]'
        '(https://github.com/blawar/titledb);',
        'Steam achievement names/descriptions are mirrored from public Steam '
        'community pages.',
        'Non-Steam games use IGN-style checklist goals; sources are listed in '
        '`CHECKLIST_SOURCES.md`.',
        '',
        f'**{len(games)} games · {sum(g[2] for g in games):,} achievements** '
        '(plus one global `FIRST_BOOT` goal)',
        '',
        f'IGN-style checklist goals cover all {non_steam_count()} non-Steam games, using IGN '
        'where available',
        'and other reputable checklists otherwise. '
        f'{countable} goals across the catalog are countable',
        '(`current/target`) and advance with A/X/Y on the overlay.',
        '',
        '| # | Game | Title ID | Achievements |',
        '|---|---|---|---|',
    ]
    for index, (name, title_id, count) in enumerate(games, 1):
        lines.append(f'| {index} | {name} | `{title_id}` | {count} |')

    OUTPUT.write_text('\n'.join(lines).rstrip() + '\n', encoding='utf8')
    print(f'Wrote {len(games)} games -> {OUTPUT}')


if __name__ == '__main__':
    main()
