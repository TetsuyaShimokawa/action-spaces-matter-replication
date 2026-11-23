"""Small helpers shared by the scripts: output location, CSV writing, headers."""
from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUTPUT = ROOT / "output"


def header(title: str) -> None:
    print("=" * 78)
    print(title)
    print("=" * 78)


def write_csv(name: str, fieldnames, rows) -> None:
    """Write rows (list of dicts) to output/<name> and print the relative path."""
    OUTPUT.mkdir(exist_ok=True)
    path = OUTPUT / name
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(rows)
    print("written:", path.relative_to(ROOT).as_posix())
