#!/usr/bin/env python3
"""
Alpha Staging Migrator
======================

Normalizes LEDGER/ALPHA_STAGING.csv to the canonical 20-column schema used by
PRINTMAXX (alpha_to_ops, dashboards, etc).

Why this exists:
  Multiple historical ingestors appended different column layouts (10-col, 18-col),
  which silently corrupts CSV alignment. This migrator:
    - Detects non-canonical rows
    - Converts known legacy formats into the canonical schema
    - Pads/isolates unknown formats into a salvage file (no data loss)

It is safe to run repeatedly:
  - If no mismatched rows are found, it exits without writing backups.

Usage:
  python3 AUTOMATIONS/alpha_staging_migrate.py
"""

from __future__ import annotations

import csv
import json
import re
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import List, Tuple


BASE_DIR = Path(__file__).resolve().parent.parent
ALPHA_PATH = BASE_DIR / "LEDGER" / "ALPHA_STAGING.csv"
SALVAGE_DIR = BASE_DIR / "LEDGER" / "_salvage"

# Canonical schema (keep in sync with LEDGER/ALPHA_STAGING.csv header).
CANONICAL_FIELDS = [
    "alpha_id",
    "source",
    "source_url",
    "category",
    "tactic",
    "roi_potential",
    "priority",
    "status",
    "applicable_methods",
    "applicable_niches",
    "synergy_score",
    "cross_sell_products",
    "implementation_priority",
    "engagement_authenticity",
    "earnings_verified",
    "extracted_method",
    "compliance_notes",
    "reviewer_notes",
    "created_at",
    "ops_generated",
]


def now_stamp() -> str:
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def priority_from_roi(roi: str) -> str:
    roi = (roi or "").strip().upper()
    if roi in {"HIGHEST", "HIGH"}:
        return "HIGH"
    if roi in {"MEDIUM"}:
        return "MEDIUM"
    return "LOW"


def looks_like_date(s: str) -> bool:
    s = (s or "").strip()
    return bool(re.match(r"^\d{4}-\d{2}-\d{2}", s))


@dataclass
class MigrateStats:
    total_rows: int = 0
    canonical_rows: int = 0
    migrated_10: int = 0
    migrated_18: int = 0
    salvaged: int = 0


def _read_header_and_rows(path: Path) -> Tuple[List[str], List[List[str]]]:
    with open(path, newline="", encoding="utf-8", errors="replace") as f:
        reader = csv.reader(f)
        header = next(reader)
        rows = list(reader)
    return header, rows


def _write_csv(path: Path, header: List[str], rows: List[List[str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(header)
        w.writerows(rows)


def migrate() -> int:
    if not ALPHA_PATH.exists():
        print(f"alpha_staging_migrate: missing {ALPHA_PATH}")
        return 1

    header, rows = _read_header_and_rows(ALPHA_PATH)
    header_len = len(header)

    if header != CANONICAL_FIELDS:
        # Hard-stop: better to fail loudly than rewrite a file we don't understand.
        print("alpha_staging_migrate: unexpected header. refusing to migrate.")
        print(f"  expected ({len(CANONICAL_FIELDS)}): {CANONICAL_FIELDS}")
        print(f"  found    ({len(header)}): {header}")
        return 2

    mismatched = [(i, r) for i, r in enumerate(rows, start=2) if len(r) != header_len and len(r) > 0]
    if not mismatched:
        print("alpha_staging_migrate: already normalized (no mismatched rows).")
        return 0

    stats = MigrateStats(total_rows=len(rows))
    out_rows: List[List[str]] = []
    salvage: List[dict] = []

    for line_no, row in enumerate(rows, start=2):
        if not row:
            continue

        if len(row) == header_len:
            out_rows.append(row)
            stats.canonical_rows += 1
            continue

        # Legacy 10-col format (unified_alpha_monitor append):
        #   alpha_id, source, category, title, url, status, roi_potential, date_found, reviewer_notes, content_hash
        if len(row) == 10 and row[0].strip().startswith("ALPHA") and row[4].strip().startswith("http"):
            alpha_id, source, category, title, url, status, roi, date_found, notes, content_hash = row
            mapped = {k: "" for k in CANONICAL_FIELDS}
            mapped["alpha_id"] = alpha_id.strip()
            mapped["source"] = source.strip()
            mapped["source_url"] = url.strip()
            mapped["category"] = category.strip()
            mapped["tactic"] = title.strip()
            mapped["roi_potential"] = (roi.strip() or "MEDIUM").upper()
            mapped["priority"] = priority_from_roi(mapped["roi_potential"])
            mapped["status"] = (status.strip() or "PENDING_REVIEW").upper()
            mapped["engagement_authenticity"] = "UNKNOWN"
            mapped["earnings_verified"] = "N/A"
            mapped["reviewer_notes"] = (notes.strip() + (f" | content_hash={content_hash.strip()}" if content_hash.strip() else "")).strip()
            mapped["created_at"] = date_found.strip() if looks_like_date(date_found) else datetime.now().isoformat()
            mapped["ops_generated"] = "FALSE"
            out_rows.append([mapped.get(k, "") for k in CANONICAL_FIELDS])
            stats.migrated_10 += 1
            continue

        # Legacy 18-col format (missing compliance_notes + ops_generated).
        # Observed as:
        #   alpha_id,source,source_url,category,tactic,roi_potential,priority,status,
        #   applicable_methods,applicable_niches,synergy_score,reviewer_notes,
        #   cross_sell_products,implementation_priority,engagement_authenticity,earnings_verified,extracted_method,created_at
        if len(row) == 18 and row[0].strip().startswith("ALPHA") and row[2].strip().startswith("http") and looks_like_date(row[-1]):
            mapped = {k: "" for k in CANONICAL_FIELDS}
            mapped["alpha_id"] = row[0].strip()
            mapped["source"] = row[1].strip()
            mapped["source_url"] = row[2].strip()
            mapped["category"] = row[3].strip()
            mapped["tactic"] = row[4].strip()
            mapped["roi_potential"] = (row[5].strip() or "MEDIUM").upper()
            mapped["priority"] = row[6].strip() or priority_from_roi(mapped["roi_potential"])
            mapped["status"] = (row[7].strip() or "PENDING_REVIEW").upper()
            mapped["applicable_methods"] = row[8].strip()
            mapped["applicable_niches"] = row[9].strip()
            mapped["synergy_score"] = row[10].strip()
            mapped["reviewer_notes"] = row[11].strip()
            mapped["cross_sell_products"] = row[12].strip()
            mapped["implementation_priority"] = row[13].strip()
            mapped["engagement_authenticity"] = row[14].strip() or "UNKNOWN"
            mapped["earnings_verified"] = row[15].strip() or "N/A"
            mapped["extracted_method"] = row[16].strip()
            mapped["created_at"] = row[17].strip()
            mapped["ops_generated"] = "FALSE"
            out_rows.append([mapped.get(k, "") for k in CANONICAL_FIELDS])
            stats.migrated_18 += 1
            continue

        # Unknown row shape: salvage it losslessly.
        salvage.append(
            {
                "line_no": line_no,
                "cols": len(row),
                "row": row,
            }
        )
        stats.salvaged += 1

    # Backup current file before overwrite.
    backup_path = ALPHA_PATH.with_suffix(f".before_migrate_{now_stamp()}.csv")
    backup_path.write_bytes(ALPHA_PATH.read_bytes())

    # Write normalized file.
    _write_csv(ALPHA_PATH, CANONICAL_FIELDS, out_rows)

    # Write salvage file (JSONL wrapped in CSV for easy grep).
    if salvage:
        SALVAGE_DIR.mkdir(parents=True, exist_ok=True)
        salvage_path = SALVAGE_DIR / f"ALPHA_STAGING_salvage_{now_stamp()}.csv"
        with open(salvage_path, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["line_no", "cols", "row_json"])
            for item in salvage:
                w.writerow([item["line_no"], item["cols"], json.dumps(item["row"], ensure_ascii=False)])

        print(f"alpha_staging_migrate: wrote salvage: {salvage_path}")

    print("alpha_staging_migrate: migrated")
    print(f"  total_rows:     {stats.total_rows}")
    print(f"  canonical_rows: {stats.canonical_rows}")
    print(f"  migrated_10:    {stats.migrated_10}")
    print(f"  migrated_18:    {stats.migrated_18}")
    print(f"  salvaged:       {stats.salvaged}")
    print(f"  backup:         {backup_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(migrate())

