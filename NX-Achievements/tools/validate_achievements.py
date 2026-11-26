#!/usr/bin/env python3
"""Validate generated achievement data and checklist coverage."""
import re
import sys
from collections import Counter
from pathlib import Path

from games_extra import EXTRA_GAMES, STEAM_APPIDS, STEAM_EXTRA
from generate_achievements import GAMES, load_checklists

DATA = Path(__file__).resolve().parent.parent / 'data' / 'achievements.txt'


def main():
    checklists, sources = load_checklists()
    steam = {s for s, _, _, _ in STEAM_EXTRA} | set(STEAM_APPIDS)
    non_steam = {s for s, _, _, a, _ in GAMES if not a}
    non_steam |= {s for s, _, _, _ in EXTRA_GAMES if s not in steam}

    lines = DATA.read_text(encoding='utf8').splitlines()
    counts = {}
    ids = Counter()
    targets = 0
    bad = []
    name = tid = None
    for i, line in enumerate(lines, 1):
        m = re.match(r'^# (.+) \(([0-9A-F*]{16,})\)$', line)
        if m:
            name, tid = m.group(1), m.group(2)
            counts.setdefault((name, tid), 0)
            continue
        if not line or line.startswith('#'):
            continue
        parts = line.split('|')
        if len(parts) not in (4, 5):
            bad.append((i, 'field count'))
            continue
        if len(parts) == 5:
            if not parts[4].isdigit() or int(parts[4]) <= 0:
                bad.append((i, 'bad target'))
            else:
                targets += 1
        if parts[0] != '*' and not re.fullmatch(r'[0-9A-F]{16}', parts[0]):
            bad.append((i, 'bad title ID'))
        ids[parts[1]] += 1
        if name:
            counts[(name, tid)] += 1

    counts_only = list(counts.values())
    covered = set(checklists) | {'TOTK'}  # TOTK lives in totk_checklist.py
    missing_checklist = sorted(s for s in non_steam if s not in covered)
    empty_sources = sorted(s for s in checklists if not sources.get(s))

    print(f'games: {len(counts)}')
    print(f'achievements: {sum(counts_only)} (+1 global)')
    print(f'min/max/avg: {min(counts_only)}/{max(counts_only)}/'
          f'{round(sum(counts_only)/len(counts_only), 1)}')
    print(f'games under 20: {sum(c < 20 for c in counts_only)}')
    print(f'duplicate IDs: {sum(v > 1 for v in ids.values())}')
    print(f'bad lines: {len(bad)}')
    print(f'countable goals: {targets}')
    print(f'non-Steam games: {len(non_steam)}')
    print(f'checklist modules: {len(checklists)}')
    print(f'missing checklist: {len(missing_checklist)}')
    if missing_checklist:
        print('  ' + ', '.join(missing_checklist))
    print(f'empty sources: {len(empty_sources)}')
    if empty_sources:
        print('  ' + ', '.join(empty_sources))
    return 1 if bad or missing_checklist or any(c < 20 for c in counts_only) else 0


if __name__ == '__main__':
    sys.exit(main())
