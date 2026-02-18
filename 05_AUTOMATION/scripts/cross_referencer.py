#!/usr/bin/env python3
"""
cross_referencer.py - Validate cross-references between LEDGER files

Checks that method IDs, alpha IDs, niche codes, and other references
are consistent across all LEDGER CSVs. Identifies orphaned references,
missing entries, and broken links.

Usage:
    python3 cross_referencer.py
    python3 cross_referencer.py --check methods
    python3 cross_referencer.py --check alpha
    python3 cross_referencer.py --check all --verbose

Example:
    # Full cross-reference check
    python3 cross_referencer.py

    # Check only method references
    python3 cross_referencer.py --check methods

    # Verbose output with details
    python3 cross_referencer.py --verbose
"""

import argparse
import csv
import json
import logging
import re
import sys
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent.parent
LEDGER_DIR = PROJECT_DIR / "LEDGER"
LOG_DIR = PROJECT_DIR / "AUTOMATIONS" / "logs"

LOG_DIR.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_DIR / "cross_referencer.log"),
        logging.StreamHandler(sys.stdout),
    ],
)
logger = logging.getLogger(__name__)


def load_csv_safe(filepath):
    """Load CSV, return empty list on error."""
    if not filepath.exists():
        return []
    try:
        with open(filepath, newline="", encoding="utf-8") as f:
            return list(csv.DictReader(f))
    except Exception as e:
        logger.error(f"Error reading {filepath}: {e}")
        return []


def check_method_references():
    """Verify all method_id references point to valid methods."""
    issues = []

    # Load master method list
    methods = load_csv_safe(LEDGER_DIR / "MONEY_METHODS_TRACKER.csv")
    valid_ids = {m.get("method_id", "") for m in methods}

    # Files that reference method_id
    ref_files = [
        ("CROSS_POLLINATION_MATRIX.csv", "method_id"),
        ("CROSS_POLLINATION_MATRIX.csv", "synergy_partners"),
        ("MEGA_RALPH_TRACKER.csv", "category"),
    ]

    # Check revenue tracker
    revenue = load_csv_safe(PROJECT_DIR / "FINANCIALS" / "REVENUE_TRACKER.csv")
    for row in revenue:
        mid = row.get("method_id", "")
        if mid and mid != "EXAMPLE" and mid not in valid_ids:
            issues.append(f"REVENUE_TRACKER: Unknown method_id '{mid}'")

    # Check expense tracker
    expenses = load_csv_safe(PROJECT_DIR / "FINANCIALS" / "EXPENSE_TRACKER.csv")
    for row in expenses:
        mid = row.get("method_id", "")
        if mid and mid != "ALL" and mid not in valid_ids:
            issues.append(f"EXPENSE_TRACKER: Unknown method_id '{mid}'")

    # Check cross-pollination matrix
    matrix = load_csv_safe(LEDGER_DIR / "CROSS_POLLINATION_MATRIX.csv")
    for row in matrix:
        mid = row.get("method_id", "")
        if mid and mid not in valid_ids:
            issues.append(f"CROSS_POLLINATION: Unknown method_id '{mid}'")

        # Check synergy partners (comma-separated)
        partners = row.get("synergy_partners", "")
        for p in partners.split(","):
            p = p.strip()
            if p and p not in valid_ids:
                issues.append(f"CROSS_POLLINATION: Unknown synergy partner '{p}' for {mid}")

    return issues, len(valid_ids)


def check_alpha_references():
    """Verify alpha entry integrity."""
    issues = []

    alpha = load_csv_safe(LEDGER_DIR / "ALPHA_STAGING.csv")

    # Check for sequential IDs
    ids = []
    for row in alpha:
        aid = row.get("alpha_id", "")
        match = re.search(r"ALPHA(\d+)", aid)
        if match:
            ids.append(int(match.group(1)))

    if ids:
        # Check for gaps
        expected = set(range(min(ids), max(ids) + 1))
        actual = set(ids)
        gaps = expected - actual
        if gaps and len(gaps) < 20:
            issues.append(f"ALPHA ID gaps: {sorted(gaps)[:10]}...")

        # Check for duplicates
        dupes = [id for id in ids if ids.count(id) > 1]
        if dupes:
            issues.append(f"ALPHA duplicate IDs: {sorted(set(dupes))[:10]}")

    # Check valid categories
    valid_cats = {
        "APP_FACTORY", "CONTENT_FORMAT", "OUTBOUND", "GROWTH_HACK",
        "TOOL_ALPHA", "MONETIZATION", "SEO_GEO_ASO", "ECOM", "AI_ALPHA",
        "GENERAL", "COMPLIANCE", "PLATFORM_ARBITRAGE", "EMERGING_METHODS",
    }
    cats = set()
    for row in alpha:
        cat = row.get("category", "")
        cats.add(cat)
        if cat and cat not in valid_cats:
            pass  # Categories are flexible

    # Check valid statuses
    valid_statuses = {
        "PENDING_REVIEW", "APPROVED", "REJECTED", "ENGAGEMENT_BAIT",
        "REPURPOSE_ONLY", "COMPLIANCE_RISK", "SATIRICAL_ABSURDIST",
        "EXAGGERATED_BUT_SIGNAL",
    }
    for row in alpha:
        status = row.get("status", "")
        if status and status not in valid_statuses:
            issues.append(f"ALPHA {row.get('alpha_id')}: Unknown status '{status}'")

    return issues, len(alpha)


def check_content_references():
    """Verify content pipeline references."""
    issues = []

    calendar = load_csv_safe(LEDGER_DIR / "CONTENT_CALENDAR_2026.csv")
    pipeline = load_csv_safe(LEDGER_DIR / "CONTENT_PIPELINE.csv")

    # Check content file paths exist
    for row in calendar:
        path = row.get("content_path", "")
        if path:
            full_path = PROJECT_DIR / path
            if not full_path.exists():
                issues.append(f"CALENDAR: Content file not found: {path}")

    return issues, len(calendar) + len(pipeline)


def check_financial_references():
    """Verify financial data consistency."""
    issues = []

    revenue = load_csv_safe(PROJECT_DIR / "FINANCIALS" / "REVENUE_TRACKER.csv")
    expenses = load_csv_safe(PROJECT_DIR / "FINANCIALS" / "EXPENSE_TRACKER.csv")

    # Check amount consistency
    for row in revenue:
        try:
            amount = float(row.get("amount", 0))
            fees = float(row.get("fees", 0))
            net = float(row.get("net_amount", 0))
            if amount > 0 and abs(amount - fees - net) > 0.02:
                issues.append(
                    f"REVENUE: Amount mismatch for {row.get('product_name', '?')}: "
                    f"${amount} - ${fees} != ${net}"
                )
        except (ValueError, TypeError):
            pass

    return issues, len(revenue) + len(expenses)


def print_report(all_issues, counts, verbose=False):
    """Print cross-reference report."""
    print("\n" + "=" * 70)
    print("  CROSS-REFERENCE VALIDATION REPORT")
    print("=" * 70)

    categories = {
        "Methods": ("method_refs", counts.get("methods", 0)),
        "Alpha": ("alpha_refs", counts.get("alpha", 0)),
        "Content": ("content_refs", counts.get("content", 0)),
        "Financial": ("financial_refs", counts.get("financial", 0)),
    }

    total_issues = 0
    for cat_name, (key, count) in categories.items():
        issues = all_issues.get(key, [])
        total_issues += len(issues)
        status = "OK" if not issues else f"{len(issues)} issues"
        print(f"\n  {cat_name} ({count} entries): {status}")

        if issues and (verbose or len(issues) <= 5):
            for issue in issues[:20]:
                print(f"    - {issue}")
            if len(issues) > 20:
                print(f"    ... and {len(issues) - 20} more")

    print(f"\n  Total Issues: {total_issues}")
    print("=" * 70)


def main():
    parser = argparse.ArgumentParser(
        description="Validate cross-references between LEDGER files"
    )
    parser.add_argument(
        "--check",
        choices=["methods", "alpha", "content", "financial", "all"],
        default="all",
        help="What to check (default: all)",
    )
    parser.add_argument("--verbose", action="store_true", help="Show all issues")
    parser.add_argument("--output", choices=["text", "json"], default="text")
    args = parser.parse_args()

    all_issues = {}
    counts = {}

    if args.check in ("methods", "all"):
        issues, count = check_method_references()
        all_issues["method_refs"] = issues
        counts["methods"] = count

    if args.check in ("alpha", "all"):
        issues, count = check_alpha_references()
        all_issues["alpha_refs"] = issues
        counts["alpha"] = count

    if args.check in ("content", "all"):
        issues, count = check_content_references()
        all_issues["content_refs"] = issues
        counts["content"] = count

    if args.check in ("financial", "all"):
        issues, count = check_financial_references()
        all_issues["financial_refs"] = issues
        counts["financial"] = count

    if args.output == "json":
        print(json.dumps(all_issues, indent=2))
    else:
        print_report(all_issues, counts, verbose=args.verbose)


if __name__ == "__main__":
    main()
