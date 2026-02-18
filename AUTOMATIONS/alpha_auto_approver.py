#!/usr/bin/env python3
"""
PRINTMAXX Alpha Auto-Approver (guardrailed)
==========================================

Goal:
  Keep PRINTMAXX moving by auto-approving ONLY low-risk alpha entries
  so alpha_to_ops.py can generate concrete ops artifacts.

What it does:
  - Scans LEDGER/ALPHA_STAGING.csv
  - For rows in status=PENDING_REVIEW:
      - If source is whitelisted (by handle) AND the tactic text does not
        contain high-risk markers, set status=AUTO_APPROVED
      - Appends a small audit note in reviewer_notes

What it does NOT do:
  - Send emails
  - Create accounts
  - List products
  - Post content

Usage:
  python3 AUTOMATIONS/alpha_auto_approver.py --tick --max 50
"""

from __future__ import annotations

import argparse
import csv
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Dict


BASE_DIR = Path(__file__).resolve().parent.parent
ALPHA_PATH = BASE_DIR / "LEDGER" / "ALPHA_STAGING.csv"
COPY_STYLE_HANDLES_FILE = BASE_DIR / "OPS" / "COPY_STYLE_HANDLES.txt"


SAFE_CATEGORIES = {
    "TOOL_ALPHA",
    "APP_FACTORY",
    "ECOM_ARB",
    "SEO_GEO_ASO",
    "OUTBOUND",
    "GROWTH_HACK",
    "MONETIZATION",
    "CONTENT_FARM",
    "CONTENT_FORMAT",
    "GENERAL",
}

# For non-whitelisted sources, only auto-approve if ROI is high enough.
MIN_ROI_FOR_NON_WHITELIST = {"HIGH", "HIGHEST"}

# If any of these appear, leave PENDING_REVIEW for explicit human decision.
HIGH_RISK_MARKERS = [
    r"\bimpersonat(e|ion|ing)\b",
    r"\bcatfish\b",
    r"\bfake (id|identity|account|persona)\b",
    r"\bstolen\b",
    r"\bcredit card\b",
    r"\bssn\b",
    r"\bfraud\b",
    r"\bmoney laundering\b",
    r"\bbypass\b.*\bcaptcha\b",
    r"\bmalware\b",
    r"\bexploit\b.*\b0day\b",
]


def now_iso() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def load_whitelist_handles() -> set[str]:
    handles: set[str] = set()
    if COPY_STYLE_HANDLES_FILE.exists():
        for line in COPY_STYLE_HANDLES_FILE.read_text(encoding="utf-8", errors="replace").splitlines():
            s = line.strip()
            if not s or s.startswith("#"):
                continue
            handles.add(s.lstrip("@").strip().lower())
    return handles


def extract_handles_from_source(source: str) -> List[str]:
    s = (source or "").strip().lower()
    return [h.lstrip("@") for h in re.findall(r"@([a-z0-9_]{1,32})", s)]


def is_high_risk(tactic: str) -> bool:
    text = (tactic or "").lower()
    return any(re.search(p, text) for p in HIGH_RISK_MARKERS)


def run_tick(max_items: int) -> Dict[str, int]:
    if not ALPHA_PATH.exists():
        return {"scanned": 0, "approved": 0, "skipped": 0}

    whitelist = load_whitelist_handles()

    rows: List[Dict[str, str]] = []
    with open(ALPHA_PATH, "r", newline="", encoding="utf-8", errors="replace") as f:
        reader = csv.DictReader(f)
        fieldnames = list(reader.fieldnames or [])
        for row in reader:
            rows.append(row)

    approved = 0
    skipped = 0
    scanned = 0

    # Newest first (best-effort) so the loop is responsive.
    def sort_key(r: Dict[str, str]) -> str:
        return (r.get("created_at") or "")

    for row in sorted(rows, key=sort_key, reverse=True):
        if approved >= max_items:
            break

        scanned += 1
        status = (row.get("status") or "").strip().upper()
        if status != "PENDING_REVIEW":
            skipped += 1
            continue

        category = (row.get("category") or "").strip().upper()
        if category and category not in SAFE_CATEGORIES:
            skipped += 1
            continue

        tactic = (row.get("tactic") or "").strip()
        if not tactic:
            skipped += 1
            continue

        if is_high_risk(tactic):
            # Leave for human review.
            existing = (row.get("compliance_notes") or "").strip()
            note = "AUTO_APPROVER: high-risk marker detected; requires human review."
            row["compliance_notes"] = (existing + ("\n" if existing else "") + note).strip()
            skipped += 1
            continue

        source = (row.get("source") or "").strip()
        handles = extract_handles_from_source(source)
        is_whitelisted_source = bool(whitelist) and any(h in whitelist for h in handles)

        roi = (row.get("roi_potential") or "").strip().upper()
        if not is_whitelisted_source:
            # Non-whitelist sources must clear a higher bar.
            if roi not in MIN_ROI_FOR_NON_WHITELIST:
                skipped += 1
                continue

        row["status"] = "AUTO_APPROVED"
        rn = (row.get("reviewer_notes") or "").strip()
        audit = f"AUTO_APPROVED {now_iso()} ({'whitelist source' if is_whitelisted_source else f'roi>={sorted(MIN_ROI_FOR_NON_WHITELIST)[0]}'})"
        row["reviewer_notes"] = (rn + ("\n" if rn else "") + audit).strip()
        if "priority" in row and not (row.get("priority") or "").strip():
            roi = (row.get("roi_potential") or "").strip().upper()
            row["priority"] = "HIGH" if roi in {"HIGHEST", "HIGH"} else "MEDIUM" if roi == "MEDIUM" else "LOW"
        if "ops_generated" in row and not (row.get("ops_generated") or "").strip():
            row["ops_generated"] = "FALSE"
        approved += 1

    # Write back if we changed anything.
    if approved > 0:
        with open(ALPHA_PATH, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)

    return {"scanned": scanned, "approved": approved, "skipped": skipped}


def main() -> int:
    ap = argparse.ArgumentParser(description="PRINTMAXX alpha auto-approver (guardrailed)")
    ap.add_argument("--tick", action="store_true", help="Run one approval tick (recommended)")
    ap.add_argument("--max", type=int, default=50, help="Max items to auto-approve per run (default: 50)")
    args = ap.parse_args()

    if not args.tick:
        ap.print_help()
        return 0

    stats = run_tick(max_items=max(0, int(args.max or 0)))
    print(f"alpha_auto_approver: scanned={stats['scanned']} approved={stats['approved']} skipped={stats['skipped']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
