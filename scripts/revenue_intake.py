#!/usr/bin/env python3
"""
PRINTMAXX Revenue Intake CLI

Log, summarize, import, and visualize revenue data.

Usage:
    python3 scripts/revenue_intake.py log --method MM007 --amount 398 --source "Fiverr" --notes "First gig"
    python3 scripts/revenue_intake.py log --method MM007 --amount 398 --expenses 50 --source "Fiverr"
    python3 scripts/revenue_intake.py summary
    python3 scripts/revenue_intake.py import --file path.csv
    python3 scripts/revenue_intake.py dashboard
"""

import argparse
import csv
import os
import sys
from collections import defaultdict
from datetime import datetime, timedelta
from io import StringIO
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
REVENUE_CSV = BASE_DIR / "FINANCIALS" / "REVENUE_TRACKER.csv"
METHODS_CSV = BASE_DIR / "LEDGER" / "MEGA_SHEET" / "TAB1_MONEY_METHODS_MASTER.csv"

CSV_FIELDS = ["date", "method_id", "method_name", "revenue", "expenses", "profit", "source", "notes"]


def load_method_map():
    """Load method_id -> method_name mapping from master CSV."""
    method_map = {}
    if not METHODS_CSV.exists():
        return method_map
    with open(METHODS_CSV, "r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            mid = row.get("method_id", "").strip()
            mname = row.get("method_name", "").strip()
            if mid:
                method_map[mid] = mname
    return method_map


def ensure_csv():
    """Ensure the revenue CSV exists with a header row."""
    REVENUE_CSV.parent.mkdir(parents=True, exist_ok=True)
    if not REVENUE_CSV.exists():
        with open(REVENUE_CSV, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(CSV_FIELDS)


def read_rows():
    """Read all data rows from the revenue CSV."""
    if not REVENUE_CSV.exists():
        return []
    rows = []
    with open(REVENUE_CSV, "r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)
    return rows


def append_row(row_dict):
    """Append a single row dict to the revenue CSV."""
    ensure_csv()
    with open(REVENUE_CSV, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_FIELDS)
        writer.writerow(row_dict)


def resolve_method(method_id_input):
    """Resolve a method ID input to (method_id, method_name).

    Accepts: MM007, mm007, CF001, AI002, SWARM001, or full names like MM007_COLD_OUTBOUND.
    """
    raw = method_id_input.strip().upper()
    method_map = load_method_map()

    # Direct match: user typed something like MM007_COLD_OUTBOUND
    if raw in method_map:
        return raw, method_map[raw]

    # Check if raw matches any key (handles MM007 -> MM007)
    if raw in method_map:
        return raw, method_map[raw]

    # Try stripping suffix: user typed MM007_COLD_OUTBOUND but map has MM007
    base = raw.split("_")[0] if "_" in raw else raw
    if base in method_map:
        return base, method_map[base]

    # No match found -- use the raw input as both id and name
    return raw, raw


def cmd_log(args):
    """Log a revenue entry."""
    method_id, method_name = resolve_method(args.method)
    revenue = float(args.amount)
    expenses = float(args.expenses) if args.expenses else 0.0
    profit = revenue - expenses
    date_str = args.date if args.date else datetime.now().strftime("%Y-%m-%d")
    source = args.source or ""
    notes = args.notes or ""

    row = {
        "date": date_str,
        "method_id": method_id,
        "method_name": method_name,
        "revenue": f"{revenue:.2f}",
        "expenses": f"{expenses:.2f}",
        "profit": f"{profit:.2f}",
        "source": source,
        "notes": notes,
    }
    append_row(row)

    print(f"Logged: ${revenue:.2f} revenue, ${expenses:.2f} expenses, ${profit:.2f} profit")
    print(f"  Method: {method_id} ({method_name})")
    print(f"  Date:   {date_str}")
    print(f"  Source: {source}")
    if notes:
        print(f"  Notes:  {notes}")


def cmd_summary(args):
    """Show revenue summary."""
    rows = read_rows()
    if not rows:
        print("No revenue data yet. Log your first entry:")
        print("  python3 scripts/revenue_intake.py log --method MM007 --amount 100 --source 'Fiverr'")
        return

    today = datetime.now().date()
    week_start = today - timedelta(days=today.weekday())  # Monday
    month_start = today.replace(day=1)

    totals_today = {"revenue": 0.0, "expenses": 0.0, "profit": 0.0, "count": 0}
    totals_week = {"revenue": 0.0, "expenses": 0.0, "profit": 0.0, "count": 0}
    totals_month = {"revenue": 0.0, "expenses": 0.0, "profit": 0.0, "count": 0}
    totals_all = {"revenue": 0.0, "expenses": 0.0, "profit": 0.0, "count": 0}
    by_method = defaultdict(lambda: {"revenue": 0.0, "expenses": 0.0, "profit": 0.0, "count": 0})

    # Track unique revenue days for streak calculation
    revenue_dates = set()

    for row in rows:
        try:
            d = datetime.strptime(row["date"], "%Y-%m-%d").date()
        except (ValueError, KeyError):
            continue

        rev = float(row.get("revenue", 0))
        exp = float(row.get("expenses", 0))
        prof = float(row.get("profit", rev - exp))

        totals_all["revenue"] += rev
        totals_all["expenses"] += exp
        totals_all["profit"] += prof
        totals_all["count"] += 1

        mid = row.get("method_id", "UNKNOWN")
        mname = row.get("method_name", mid)
        label = f"{mid} ({mname})" if mname != mid else mid
        by_method[label]["revenue"] += rev
        by_method[label]["expenses"] += exp
        by_method[label]["profit"] += prof
        by_method[label]["count"] += 1

        if rev > 0:
            revenue_dates.add(d)

        if d == today:
            totals_today["revenue"] += rev
            totals_today["expenses"] += exp
            totals_today["profit"] += prof
            totals_today["count"] += 1

        if d >= week_start:
            totals_week["revenue"] += rev
            totals_week["expenses"] += exp
            totals_week["profit"] += prof
            totals_week["count"] += 1

        if d >= month_start:
            totals_month["revenue"] += rev
            totals_month["expenses"] += exp
            totals_month["profit"] += prof
            totals_month["count"] += 1

    # Calculate streak
    streak = 0
    check_date = today
    while check_date in revenue_dates:
        streak += 1
        check_date -= timedelta(days=1)

    # Print summary
    w = 60
    print("=" * w)
    print("  PRINTMAXX REVENUE SUMMARY".center(w))
    print("=" * w)

    def print_period(label, data):
        print(f"\n  {label}")
        print(f"  {'-' * (w - 4)}")
        print(f"  Revenue:   ${data['revenue']:>10,.2f}  ({data['count']} entries)")
        print(f"  Expenses:  ${data['expenses']:>10,.2f}")
        print(f"  Profit:    ${data['profit']:>10,.2f}")
        margin = (data["profit"] / data["revenue"] * 100) if data["revenue"] > 0 else 0
        print(f"  Margin:    {margin:>10.1f}%")

    print_period(f"TODAY ({today.strftime('%Y-%m-%d')})", totals_today)
    print_period(f"THIS WEEK (from {week_start.strftime('%Y-%m-%d')})", totals_week)
    print_period(f"THIS MONTH ({today.strftime('%B %Y')})", totals_month)
    print_period("ALL TIME", totals_all)

    # Streak
    print(f"\n  REVENUE STREAK: {streak} day{'s' if streak != 1 else ''}")
    if streak == 0:
        print("  No revenue logged today. Log something and start the streak.")

    # By method breakdown
    print(f"\n  BY METHOD")
    print(f"  {'-' * (w - 4)}")
    sorted_methods = sorted(by_method.items(), key=lambda x: x[1]["profit"], reverse=True)
    for label, data in sorted_methods:
        margin = (data["profit"] / data["revenue"] * 100) if data["revenue"] > 0 else 0
        print(f"  {label}")
        print(f"    Rev: ${data['revenue']:,.2f}  Exp: ${data['expenses']:,.2f}  "
              f"Profit: ${data['profit']:,.2f}  Margin: {margin:.0f}%  ({data['count']} txns)")

    print(f"\n{'=' * w}")


def cmd_import(args):
    """Import revenue entries from a CSV file."""
    import_path = Path(args.file)
    if not import_path.exists():
        print(f"Error: File not found: {import_path}")
        sys.exit(1)

    ensure_csv()
    imported = 0
    skipped = 0

    with open(import_path, "r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        if not reader.fieldnames:
            print("Error: CSV file appears empty or has no header.")
            sys.exit(1)

        # Check required columns
        required = {"date", "method_id", "revenue"}
        available = set(reader.fieldnames)
        missing = required - available
        if missing:
            print(f"Error: Missing required columns: {', '.join(missing)}")
            print(f"Available columns: {', '.join(reader.fieldnames)}")
            sys.exit(1)

        method_map = load_method_map()

        for i, row in enumerate(reader, start=2):  # line 2 is first data row
            date_str = row.get("date", "").strip()
            method_id_raw = row.get("method_id", "").strip()
            rev_str = row.get("revenue", "0").strip()

            if not date_str or not method_id_raw or not rev_str:
                skipped += 1
                continue

            # Validate date
            try:
                datetime.strptime(date_str, "%Y-%m-%d")
            except ValueError:
                print(f"  Warning: Skipping line {i}, invalid date: {date_str}")
                skipped += 1
                continue

            # Validate revenue
            try:
                revenue = float(rev_str)
            except ValueError:
                print(f"  Warning: Skipping line {i}, invalid revenue: {rev_str}")
                skipped += 1
                continue

            expenses = float(row.get("expenses", "0").strip() or "0")
            profit = float(row.get("profit", str(revenue - expenses)).strip() or str(revenue - expenses))

            method_id, method_name = resolve_method(method_id_raw)
            # Allow override from import file
            if row.get("method_name", "").strip():
                method_name = row["method_name"].strip()

            out = {
                "date": date_str,
                "method_id": method_id,
                "method_name": method_name,
                "revenue": f"{revenue:.2f}",
                "expenses": f"{expenses:.2f}",
                "profit": f"{profit:.2f}",
                "source": row.get("source", "").strip(),
                "notes": row.get("notes", "").strip(),
            }
            append_row(out)
            imported += 1

    print(f"Import complete: {imported} rows imported, {skipped} skipped")
    print(f"  Source: {import_path}")
    print(f"  Target: {REVENUE_CSV}")


def cmd_dashboard(args):
    """Show ASCII chart of daily revenue for last 30 days."""
    rows = read_rows()
    today = datetime.now().date()
    start_date = today - timedelta(days=29)

    # Aggregate revenue by day
    daily = defaultdict(float)
    for row in rows:
        try:
            d = datetime.strptime(row["date"], "%Y-%m-%d").date()
        except (ValueError, KeyError):
            continue
        if d >= start_date:
            daily[d] += float(row.get("revenue", 0))

    # Build 30-day series
    dates = []
    values = []
    for i in range(30):
        d = start_date + timedelta(days=i)
        dates.append(d)
        values.append(daily.get(d, 0.0))

    max_val = max(values) if values else 0
    total_30d = sum(values)
    days_with_rev = sum(1 for v in values if v > 0)
    avg_daily = total_30d / 30

    # Chart dimensions
    chart_height = 15
    chart_width = 30  # one column per day
    bar_char = "|"
    fill_char = "#"

    w = 70
    print("=" * w)
    print("  PRINTMAXX REVENUE DASHBOARD - LAST 30 DAYS".center(w))
    print("=" * w)
    print()
    print(f"  Total:     ${total_30d:>10,.2f}")
    print(f"  Avg/day:   ${avg_daily:>10,.2f}")
    print(f"  Days w/rev: {days_with_rev}/30")
    print(f"  Peak day:  ${max_val:>10,.2f}")
    print()

    if max_val == 0:
        print("  No revenue in the last 30 days.")
        print("  Log your first entry:")
        print("  python3 scripts/revenue_intake.py log --method MM007 --amount 100 --source 'Fiverr'")
        print(f"\n{'=' * w}")
        return

    # Render ASCII bar chart
    # Y-axis labels + bars
    for row_idx in range(chart_height, 0, -1):
        threshold = (row_idx / chart_height) * max_val
        # Y-axis label
        if row_idx == chart_height:
            label = f"${max_val:>8,.0f} "
        elif row_idx == chart_height // 2 + 1:
            label = f"${max_val / 2:>8,.0f} "
        elif row_idx == 1:
            label = f"${'0':>8} "
        else:
            label = " " * 10

        line = label + bar_char
        for val in values:
            bar_height = (val / max_val) * chart_height if max_val > 0 else 0
            if bar_height >= row_idx:
                line += fill_char
            else:
                line += " "
        print(line)

    # X-axis
    print(" " * 10 + "+" + "-" * chart_width)

    # Date labels (show a few reference points)
    first_label = dates[0].strftime("%m/%d")
    mid_label = dates[14].strftime("%m/%d")
    last_label = dates[29].strftime("%m/%d")

    spacing = chart_width // 2
    x_labels = " " * 11 + first_label
    x_labels += " " * (spacing - len(first_label) - len(mid_label) + 2) + mid_label
    x_labels += " " * (spacing - len(last_label) + 1) + last_label
    print(x_labels)

    # Per-day detail table for days with revenue
    rev_days = [(d, v) for d, v in zip(dates, values) if v > 0]
    if rev_days:
        print(f"\n  DAILY BREAKDOWN (revenue days only)")
        print(f"  {'-' * (w - 4)}")
        for d, v in rev_days:
            bar_len = int((v / max_val) * 30) if max_val > 0 else 0
            bar = "#" * bar_len
            print(f"  {d.strftime('%Y-%m-%d')}  ${v:>10,.2f}  {bar}")

    print(f"\n{'=' * w}")


def main():
    parser = argparse.ArgumentParser(
        description="PRINTMAXX Revenue Intake CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  Log revenue:
    python3 scripts/revenue_intake.py log --method MM007 --amount 398 --source "Fiverr" --notes "First gig"

  Log with expenses:
    python3 scripts/revenue_intake.py log --method MM007 --amount 398 --expenses 50 --source "Fiverr"

  View summary:
    python3 scripts/revenue_intake.py summary

  View dashboard:
    python3 scripts/revenue_intake.py dashboard

  Bulk import:
    python3 scripts/revenue_intake.py import --file data.csv
        """,
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # log
    log_parser = subparsers.add_parser("log", help="Log a revenue entry")
    log_parser.add_argument("--method", required=True, help="Method ID (e.g. MM007, CF001, AI002)")
    log_parser.add_argument("--amount", required=True, type=float, help="Revenue amount in dollars")
    log_parser.add_argument("--expenses", type=float, default=0, help="Expenses amount (default: 0)")
    log_parser.add_argument("--source", default="", help="Revenue source (e.g. Fiverr, Gumroad)")
    log_parser.add_argument("--notes", default="", help="Optional notes")
    log_parser.add_argument("--date", default=None, help="Date YYYY-MM-DD (default: today)")

    # summary
    subparsers.add_parser("summary", help="Show revenue summary")

    # import
    import_parser = subparsers.add_parser("import", help="Bulk import from CSV")
    import_parser.add_argument("--file", required=True, help="Path to CSV file to import")

    # dashboard
    subparsers.add_parser("dashboard", help="Show ASCII revenue dashboard")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    if args.command == "log":
        cmd_log(args)
    elif args.command == "summary":
        cmd_summary(args)
    elif args.command == "import":
        cmd_import(args)
    elif args.command == "dashboard":
        cmd_dashboard(args)


if __name__ == "__main__":
    main()
