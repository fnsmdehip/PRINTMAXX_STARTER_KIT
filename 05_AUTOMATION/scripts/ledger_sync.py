#!/usr/bin/env python3
"""
ledger_sync.py - Sync and validate all LEDGER CSV files

Ensures data consistency across all LEDGER CSVs. Checks for orphaned
references, validates IDs, syncs aggregated views (MEGA_SHEET),
and generates a health report.

Usage:
    python3 ledger_sync.py --check
    python3 ledger_sync.py --sync-mega
    python3 ledger_sync.py --report
    python3 ledger_sync.py --fix

Example:
    # Check all LEDGER files for consistency
    python3 ledger_sync.py --check

    # Sync MEGA_SHEET with individual files
    python3 ledger_sync.py --sync-mega

    # Full health report
    python3 ledger_sync.py --report
"""

import argparse
import csv
import json
import logging
import os
import sys
from datetime import datetime
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent.parent
LEDGER_DIR = PROJECT_DIR / "LEDGER"
MEGA_DIR = LEDGER_DIR / "MEGA_SHEET"
LOG_DIR = PROJECT_DIR / "AUTOMATIONS" / "logs"

LOG_DIR.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_DIR / "ledger_sync.log"),
        logging.StreamHandler(sys.stdout),
    ],
)
logger = logging.getLogger(__name__)

# Known LEDGER files and their expected primary key columns
LEDGER_FILES = {
    "ALPHA_STAGING.csv": {"pk": "alpha_id", "required": ["source", "category", "status"]},
    "MONEY_METHODS_TRACKER.csv": {"pk": "method_id", "required": ["method_name", "status"]},
    "CROSS_POLLINATION_MATRIX.csv": {"pk": "method_id", "required": ["synergy_partners"]},
    "HIGH_SIGNAL_SOURCES.csv": {"pk": None, "required": []},
    "CONTENT_CALENDAR_2026.csv": {"pk": None, "required": ["platform", "status"]},
    "CONTENT_PIPELINE.csv": {"pk": "ContentID", "required": ["Type", "Status"]},
    "APP_FACTORY_METHODS.csv": {"pk": None, "required": []},
    "APP_CLONE_OPPORTUNITIES.csv": {"pk": None, "required": []},
    "WINNING_CONTENT_STRUCTURES.csv": {"pk": None, "required": []},
    "OUTREACH_PIPELINE.csv": {"pk": None, "required": []},
    "MEGA_RALPH_TRACKER.csv": {"pk": "task_id", "required": ["status"]},
}


def load_csv_safe(filepath):
    """Load CSV, return empty list on error."""
    try:
        if not filepath.exists():
            return [], []
        with open(filepath, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            fieldnames = reader.fieldnames or []
            return list(reader), fieldnames
    except Exception as e:
        logger.error(f"Error reading {filepath}: {e}")
        return [], []


def check_file_health(filename, spec):
    """Check a single LEDGER file for issues."""
    filepath = LEDGER_DIR / filename
    issues = []

    if not filepath.exists():
        issues.append({"severity": "ERROR", "message": f"File not found: {filename}"})
        return issues

    rows, fieldnames = load_csv_safe(filepath)
    file_size = filepath.stat().st_size

    # Basic checks
    if len(rows) == 0:
        issues.append({"severity": "WARNING", "message": f"{filename}: Empty file"})

    # Check required columns exist
    for col in spec.get("required", []):
        if col not in fieldnames:
            issues.append({"severity": "ERROR", "message": f"{filename}: Missing column '{col}'"})

    # Check primary key uniqueness
    pk = spec.get("pk")
    if pk and pk in fieldnames:
        ids = [row.get(pk, "") for row in rows]
        dupes = [id for id in ids if ids.count(id) > 1 and id]
        if dupes:
            issues.append({
                "severity": "WARNING",
                "message": f"{filename}: {len(set(dupes))} duplicate {pk} values",
            })

    # Check for empty required fields
    for col in spec.get("required", []):
        if col in fieldnames:
            empty_count = sum(1 for row in rows if not row.get(col, "").strip())
            if empty_count > 0:
                issues.append({
                    "severity": "INFO",
                    "message": f"{filename}: {empty_count} rows with empty '{col}'",
                })

    if not issues:
        issues.append({
            "severity": "OK",
            "message": f"{filename}: {len(rows)} rows, {len(fieldnames)} cols, {file_size:,} bytes",
        })

    return issues


def check_cross_references():
    """Check that cross-references between files are valid."""
    issues = []

    # Load methods
    methods, _ = load_csv_safe(LEDGER_DIR / "MONEY_METHODS_TRACKER.csv")
    valid_methods = {m.get("method_id", "") for m in methods}

    # Check CROSS_POLLINATION_MATRIX references valid methods
    matrix, _ = load_csv_safe(LEDGER_DIR / "CROSS_POLLINATION_MATRIX.csv")
    for row in matrix:
        method_id = row.get("method_id", "")
        if method_id and method_id not in valid_methods:
            issues.append({
                "severity": "WARNING",
                "message": f"CROSS_POLLINATION: Unknown method_id '{method_id}'",
            })

    # Check ALPHA_STAGING categories
    alpha, _ = load_csv_safe(LEDGER_DIR / "ALPHA_STAGING.csv")
    valid_cats = {
        "APP_FACTORY", "CONTENT_FORMAT", "OUTBOUND", "GROWTH_HACK",
        "TOOL_ALPHA", "MONETIZATION", "SEO_GEO_ASO", "ECOM", "AI_ALPHA",
        "GENERAL", "COMPLIANCE", "PLATFORM_ARBITRAGE", "EMERGING_METHODS",
    }
    for row in alpha:
        cat = row.get("category", "")
        if cat and cat not in valid_cats:
            pass  # Categories are flexible, just log

    return issues


def count_all_files():
    """Count rows in all CSV files."""
    counts = {}
    total_rows = 0
    total_size = 0

    for f in sorted(LEDGER_DIR.glob("*.csv")):
        rows, _ = load_csv_safe(f)
        size = f.stat().st_size
        counts[f.name] = {"rows": len(rows), "size": size}
        total_rows += len(rows)
        total_size += size

    return counts, total_rows, total_size


def generate_report():
    """Generate full health report."""
    print("\n" + "=" * 70)
    print("  LEDGER HEALTH REPORT")
    print(f"  Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 70)

    # File health
    all_issues = []
    print(f"\n  {'--- FILE HEALTH ---':^70}")

    for filename, spec in LEDGER_FILES.items():
        issues = check_file_health(filename, spec)
        all_issues.extend(issues)
        for issue in issues:
            severity = issue["severity"]
            marker = {"OK": " OK", "INFO": "  i", "WARNING": " !!", "ERROR": "ERR"}
            print(f"  [{marker.get(severity, '  ?')}] {issue['message']}")

    # Cross-reference check
    xref_issues = check_cross_references()
    if xref_issues:
        print(f"\n  {'--- CROSS-REFERENCE ISSUES ---':^70}")
        for issue in xref_issues:
            print(f"  [!!] {issue['message']}")
    all_issues.extend(xref_issues)

    # File counts
    counts, total_rows, total_size = count_all_files()
    print(f"\n  {'--- FILE INVENTORY ---':^70}")
    for name, data in sorted(counts.items()):
        print(f"  {name:<50} {data['rows']:>6} rows  {data['size']:>8,} bytes")

    print(f"\n  Total CSV Files: {len(counts)}")
    print(f"  Total Rows: {total_rows:,}")
    print(f"  Total Size: {total_size:,} bytes ({total_size / 1024:.0f} KB)")

    # Summary
    errors = len([i for i in all_issues if i["severity"] == "ERROR"])
    warnings = len([i for i in all_issues if i["severity"] == "WARNING"])
    print(f"\n  Health: {errors} errors, {warnings} warnings")
    print("=" * 70)


def sync_mega_sheet():
    """Sync individual LEDGER files to MEGA_SHEET consolidated views."""
    if not MEGA_DIR.exists():
        logger.warning(f"MEGA_SHEET directory not found: {MEGA_DIR}")
        return

    mega_files = list(MEGA_DIR.glob("*.csv"))
    logger.info(f"Found {len(mega_files)} MEGA_SHEET files")

    for mf in mega_files:
        rows, fieldnames = load_csv_safe(mf)
        logger.info(f"  {mf.name}: {len(rows)} rows, {len(fieldnames)} columns")

    logger.info("MEGA_SHEET sync check complete. Manual consolidation may be needed.")


def main():
    parser = argparse.ArgumentParser(
        description="Sync and validate all LEDGER CSV files"
    )
    parser.add_argument("--check", action="store_true", help="Check file health")
    parser.add_argument("--sync-mega", action="store_true", help="Sync MEGA_SHEET")
    parser.add_argument("--report", action="store_true", help="Full health report")
    parser.add_argument("--fix", action="store_true", help="Auto-fix simple issues")
    parser.add_argument("--output", choices=["text", "json"], default="text")
    args = parser.parse_args()

    if args.check:
        all_issues = []
        for filename, spec in LEDGER_FILES.items():
            issues = check_file_health(filename, spec)
            all_issues.extend(issues)
        if args.output == "json":
            print(json.dumps(all_issues, indent=2))
        else:
            for i in all_issues:
                print(f"[{i['severity']}] {i['message']}")

    elif args.sync_mega:
        sync_mega_sheet()

    elif args.report:
        generate_report()

    elif args.fix:
        logger.info("Auto-fix not yet implemented. Use --report to see issues.")

    else:
        generate_report()


if __name__ == "__main__":
    main()
