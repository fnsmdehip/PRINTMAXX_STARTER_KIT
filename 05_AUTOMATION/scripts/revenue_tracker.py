#!/usr/bin/env python3
"""
revenue_tracker.py - Aggregate revenue from all sources and methods

Reads FINANCIALS/REVENUE_TRACKER.csv, aggregates by method, platform, time period.
Generates summary reports and identifies top performers.

Usage:
    python3 revenue_tracker.py --period monthly --output summary
    python3 revenue_tracker.py --period weekly --method MM001
    python3 revenue_tracker.py --add --method MM001 --amount 49.99 --platform gumroad --product "AI Stack Guide"
    python3 revenue_tracker.py --dashboard

Example:
    # View monthly revenue summary
    python3 revenue_tracker.py --period monthly

    # Add a new revenue entry
    python3 revenue_tracker.py --add --method MM002 --amount 9.00 --platform gumroad --product "Paywall Playbook"

    # View revenue dashboard
    python3 revenue_tracker.py --dashboard
"""

import argparse
import csv
import json
import logging
import sys
from collections import defaultdict
from datetime import datetime, timedelta
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent.parent
FINANCIALS_DIR = PROJECT_DIR / "FINANCIALS"
REVENUE_FILE = FINANCIALS_DIR / "REVENUE_TRACKER.csv"
EXPENSE_FILE = FINANCIALS_DIR / "EXPENSE_TRACKER.csv"
PNL_FILE = FINANCIALS_DIR / "P_AND_L_MONTHLY.csv"
LOG_DIR = PROJECT_DIR / "AUTOMATIONS" / "logs"

LOG_DIR.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_DIR / "revenue_tracker.log"),
        logging.StreamHandler(sys.stdout),
    ],
)
logger = logging.getLogger(__name__)


def load_revenue():
    """Load all revenue entries."""
    if not REVENUE_FILE.exists():
        logger.warning(f"Revenue file not found: {REVENUE_FILE}")
        return []

    entries = []
    with open(REVENUE_FILE, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Skip example rows
            if row.get("customer_id", "") == "EXAMPLE":
                continue
            try:
                row["amount"] = float(row.get("amount", 0))
                row["fees"] = float(row.get("fees", 0))
                row["net_amount"] = float(row.get("net_amount", 0))
            except (ValueError, TypeError):
                row["amount"] = 0
                row["fees"] = 0
                row["net_amount"] = 0
            entries.append(row)
    return entries


def load_expenses():
    """Load all expense entries."""
    if not EXPENSE_FILE.exists():
        return []

    entries = []
    with open(EXPENSE_FILE, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                row["amount"] = float(row.get("amount", 0))
            except (ValueError, TypeError):
                row["amount"] = 0
            entries.append(row)
    return entries


def add_revenue_entry(method_id, amount, platform, product, recurring=False, notes=""):
    """Add a new revenue entry."""
    fieldnames = [
        "date", "method_id", "method_name", "source_platform", "transaction_type",
        "amount", "currency", "fees", "net_amount", "customer_id", "product_name",
        "recurring", "notes",
    ]

    # Estimate fees based on platform
    fee_rates = {
        "gumroad": 0.10,
        "stripe": 0.029,
        "app_store_ios": 0.30,
        "google_play": 0.30,
        "whop": 0.057,
        "beehiiv": 0,
        "youtube": 0,
    }
    fee_rate = fee_rates.get(platform, 0.05)
    fees = round(amount * fee_rate, 2)
    net = round(amount - fees, 2)

    entry = {
        "date": datetime.now().strftime("%Y-%m-%d"),
        "method_id": method_id,
        "method_name": method_id,  # Can be enriched later
        "source_platform": platform,
        "transaction_type": "subscription" if recurring else "one_time",
        "amount": amount,
        "currency": "USD",
        "fees": fees,
        "net_amount": net,
        "customer_id": f"CUST_{datetime.now().strftime('%Y%m%d%H%M%S')}",
        "product_name": product,
        "recurring": str(recurring).upper(),
        "notes": notes,
    }

    file_exists = REVENUE_FILE.exists()
    with open(REVENUE_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        writer.writerow(entry)

    logger.info(f"Added revenue: ${amount} from {platform} ({product})")
    return entry


def aggregate_by_method(entries):
    """Aggregate revenue by method."""
    methods = defaultdict(lambda: {"total": 0, "net": 0, "count": 0, "fees": 0})
    for e in entries:
        mid = e.get("method_id", "UNKNOWN")
        methods[mid]["total"] += e["amount"]
        methods[mid]["net"] += e["net_amount"]
        methods[mid]["fees"] += e["fees"]
        methods[mid]["count"] += 1
    return dict(methods)


def aggregate_by_platform(entries):
    """Aggregate revenue by platform."""
    platforms = defaultdict(lambda: {"total": 0, "net": 0, "count": 0})
    for e in entries:
        plat = e.get("source_platform", "UNKNOWN")
        platforms[plat]["total"] += e["amount"]
        platforms[plat]["net"] += e["net_amount"]
        platforms[plat]["count"] += 1
    return dict(platforms)


def aggregate_by_period(entries, period="monthly"):
    """Aggregate revenue by time period."""
    periods = defaultdict(lambda: {"total": 0, "net": 0, "count": 0})
    for e in entries:
        date_str = e.get("date", "")
        try:
            dt = datetime.strptime(date_str, "%Y-%m-%d")
            if period == "monthly":
                key = dt.strftime("%Y-%m")
            elif period == "weekly":
                key = f"{dt.strftime('%Y')}-W{dt.strftime('%W')}"
            elif period == "daily":
                key = date_str
            else:
                key = dt.strftime("%Y-%m")
        except ValueError:
            key = "UNKNOWN"

        periods[key]["total"] += e["amount"]
        periods[key]["net"] += e["net_amount"]
        periods[key]["count"] += 1
    return dict(periods)


def print_dashboard(entries, expenses):
    """Print a revenue dashboard."""
    total_rev = sum(e["amount"] for e in entries)
    total_net = sum(e["net_amount"] for e in entries)
    total_fees = sum(e["fees"] for e in entries)
    total_exp = sum(e["amount"] for e in expenses)

    by_method = aggregate_by_method(entries)
    by_platform = aggregate_by_platform(entries)
    by_month = aggregate_by_period(entries, "monthly")

    print("\n" + "=" * 60)
    print("  PRINTMAXX REVENUE DASHBOARD")
    print("=" * 60)

    print(f"\n  Total Revenue:    ${total_rev:>10,.2f}")
    print(f"  Total Fees:       ${total_fees:>10,.2f}")
    print(f"  Net Revenue:      ${total_net:>10,.2f}")
    print(f"  Total Expenses:   ${total_exp:>10,.2f}")
    print(f"  Net Profit:       ${total_net - total_exp:>10,.2f}")
    print(f"  Transactions:     {len(entries):>10}")

    if by_method:
        print(f"\n{'--- BY METHOD ---':^60}")
        sorted_methods = sorted(by_method.items(), key=lambda x: x[1]["total"], reverse=True)
        for method, data in sorted_methods[:10]:
            print(f"  {method:<25} ${data['total']:>10,.2f}  ({data['count']} txns)")

    if by_platform:
        print(f"\n{'--- BY PLATFORM ---':^60}")
        sorted_plats = sorted(by_platform.items(), key=lambda x: x[1]["total"], reverse=True)
        for plat, data in sorted_plats[:10]:
            print(f"  {plat:<25} ${data['total']:>10,.2f}  ({data['count']} txns)")

    if by_month:
        print(f"\n{'--- BY MONTH ---':^60}")
        for month in sorted(by_month.keys()):
            data = by_month[month]
            print(f"  {month:<25} ${data['total']:>10,.2f}  ({data['count']} txns)")

    print("\n" + "=" * 60)


def print_summary(entries, period="monthly", method_filter=None):
    """Print a period summary."""
    if method_filter:
        entries = [e for e in entries if e.get("method_id") == method_filter]

    by_period = aggregate_by_period(entries, period)

    if not by_period:
        print("No revenue data found for the specified filters.")
        return

    print(f"\n{'--- REVENUE SUMMARY (' + period.upper() + ') ---':^60}")
    total = 0
    for key in sorted(by_period.keys()):
        data = by_period[key]
        total += data["total"]
        print(f"  {key:<20} ${data['total']:>10,.2f}  (net: ${data['net']:>10,.2f})")

    print(f"\n  {'TOTAL':<20} ${total:>10,.2f}")


def main():
    parser = argparse.ArgumentParser(
        description="Track and aggregate revenue from all PRINTMAXX methods"
    )
    parser.add_argument("--dashboard", action="store_true", help="Show full dashboard")
    parser.add_argument(
        "--period",
        choices=["daily", "weekly", "monthly"],
        default=None,
        help="Aggregation period",
    )
    parser.add_argument("--method", type=str, default=None, help="Filter by method ID")
    parser.add_argument("--add", action="store_true", help="Add a new revenue entry")
    parser.add_argument("--amount", type=float, default=None, help="Revenue amount")
    parser.add_argument("--platform", type=str, default=None, help="Source platform")
    parser.add_argument("--product", type=str, default=None, help="Product name")
    parser.add_argument("--recurring", action="store_true", help="Is recurring revenue")
    parser.add_argument("--notes", type=str, default="", help="Additional notes")
    parser.add_argument("--output", choices=["text", "json"], default="text", help="Output format")
    args = parser.parse_args()

    if args.add:
        if not all([args.method, args.amount, args.platform, args.product]):
            parser.error("--add requires --method, --amount, --platform, and --product")
        add_revenue_entry(
            args.method, args.amount, args.platform, args.product,
            recurring=args.recurring, notes=args.notes,
        )
        return

    entries = load_revenue()
    expenses = load_expenses()

    if args.dashboard:
        print_dashboard(entries, expenses)
    elif args.period:
        print_summary(entries, args.period, args.method)
    else:
        print_dashboard(entries, expenses)


if __name__ == "__main__":
    main()
