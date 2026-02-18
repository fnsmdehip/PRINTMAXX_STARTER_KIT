#!/usr/bin/env python3
"""Append .ralph alpha entries into LEDGER/ALPHA_STAGING.csv."""

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
main_csv = BASE_DIR / "LEDGER" / "ALPHA_STAGING.csv"
new_csv = BASE_DIR / ".ralph" / "new_content_farm_alpha.csv"

with open(main_csv, "a", encoding="utf-8", newline="") as main:
    with open(new_csv, "r", encoding="utf-8") as new:
        content = new.read().strip()
        if content:
            main.write("\n" + content)

print(f"SUCCESS: Appended entries from {new_csv.name} to {main_csv.name}")
