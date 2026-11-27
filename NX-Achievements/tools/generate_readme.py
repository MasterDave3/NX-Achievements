#!/usr/bin/env python3
"""Generate README.md from README.template.md.

Any line shaped like ``<!-- INCLUDE:FILE.md -->`` is replaced with the contents
of that file from the repository root. Markdown headings in the included file
are shifted down by one level so they nest under the generated README.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TEMPLATE = ROOT / "README.template.md"
OUTPUT = ROOT / "README.md"

# Only simple filenames are accepted; no subdirectories or "..".
INCLUDE_RE = re.compile(r"^<!--\s*INCLUDE:([A-Za-z0-9._-]+)\s*-->$", re.MULTILINE)
HEADING_RE = re.compile(r"^(#{1,6})(\s+.*)$")


def shift_headings(text: str) -> str:
    """Add one '#' to Markdown headings, skipping fenced code blocks."""
    lines: list[str] = []
    fence: str | None = None

    for line in text.splitlines():
        stripped = line.lstrip()
        marker = None
        if stripped.startswith("```"):
            marker = "```"
        elif stripped.startswith("~~~"):
            marker = "~~~"

        if fence is None and marker is not None:
            fence = marker
            lines.append(line)
            continue
        if fence is not None and marker == fence:
            fence = None
            lines.append(line)
            continue

        if fence is None:
            match = HEADING_RE.match(line)
            if match:
                line = "#" + line

        lines.append(line)

    return "\n".join(lines)


def main() -> int:
    if not TEMPLATE.is_file():
        print(f"error: missing template: {TEMPLATE}", file=sys.stderr)
        return 1

    template = TEMPLATE.read_text(encoding="utf-8")

    def replace(match: re.Match[str]) -> str:
        name = match.group(1)
        if name == OUTPUT.name:
            raise ValueError("README.md cannot include itself")

        path = ROOT / name
        if path.parent != ROOT or not path.is_file():
            raise FileNotFoundError(f"included file not found in repo root: {name}")

        return shift_headings(path.read_text(encoding="utf-8").rstrip("\n"))

    try:
        generated = INCLUDE_RE.sub(replace, template)
    except (FileNotFoundError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    OUTPUT.write_text(generated, encoding="utf-8")
    print(f"Wrote {OUTPUT.relative_to(ROOT)} from {TEMPLATE.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
