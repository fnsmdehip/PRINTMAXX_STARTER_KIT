#!/usr/bin/env python3
"""
ROI Analyzer - Calculate return on investment across all money methods.

Integrates:
- FINANCIALS/REVENUE_TRACKER.csv (income)
- FINANCIALS/EXPENSE_TRACKER.csv (costs)
- LEDGER/PAPER_TRADES/ (paper trade results)
- LEDGER/BACKTESTS/ (backtest scores)

Usage:
    python3 roi_analyzer.py methods          # ROI by method
    python3 roi_analyzer.py revenue-per-hour # Revenue per hour ranking
    python3 roi_analyzer.py projections      # Revenue projections
    python3 roi_analyzer.py winners          # Top performers
    python3 roi_analyzer.py losers           # Underperformers (candidates for kill)
    python3 roi_analyzer.py report           # Full ROI report
"""

import csv
import argparse
from pathlib import Path
from datetime import datetime, timedelta
from collections import defaultdict
from typing import Dict, List

PROJECT_DIR = Path("/Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt")
FINANCIALS_DIR = PROJECT_DIR / "FINANCIALS"
LEDGER_DIR = PROJECT_DIR / "LEDGER"
PAPER_TRADE_DIR = LEDGER_DIR / "PAPER_TRADES"
BACKTEST_DIR = LEDGER_DIR / "BACKTESTS"


def parse_amount(value: str) -> float:
    try:
        return float(str(value).replace('$', '').replace(',', '').strip())
    except (ValueError, TypeError):
        return 0.0


def load_revenue() -> List[Dict]:
    rows = []
    filepath = FINANCIALS_DIR / "REVENUE_TRACKER.csv"
    if not filepath.exists():
        return rows
    with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row.get('customer_id') != 'EXAMPLE':
                rows.append(row)
    return rows


def load_expenses() -> List[Dict]:
    rows = []
    filepath = FINANCIALS_DIR / "EXPENSE_TRACKER.csv"
    if not filepath.exists():
        return rows
    with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row.get('category') != 'EXAMPLE':
                rows.append(row)
    return rows


def load_paper_trades() -> List[Dict]:
    rows = []
    if not PAPER_TRADE_DIR.exists():
        return rows
    for filepath in PAPER_TRADE_DIR.glob("*.csv"):
        with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
            reader = csv.DictReader(f)
            for row in reader:
                rows.append(row)
    return rows


def load_backtests() -> List[Dict]:
    rows = []
    filepath = BACKTEST_DIR / "BACKTEST_RESULTS.csv"
    if not filepath.exists():
        return rows
    with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)
    return rows


def cmd_methods(args):
    """ROI by method."""
    revenue_rows = load_revenue()
    expense_rows = load_expenses()

    method_revenue = defaultdict(float)
    method_expenses = defaultdict(float)

    for row in revenue_rows:
        mid = row.get('method_id', 'UNKNOWN')
        method_revenue[mid] += parse_amount(row.get('net_amount', row.get('amount', '0')))

    for row in expense_rows:
        mid = row.get('method_id', 'ALL')
        method_expenses[mid] += parse_amount(row.get('amount', '0'))

    all_methods = set(list(method_revenue.keys()) + list(method_expenses.keys()))
    all_methods.discard('ALL')
    all_methods.discard('NONE')

    # Allocate shared expenses
    shared = method_expenses.get('ALL', 0)
    active_count = max(len([m for m in all_methods if method_revenue.get(m, 0) > 0]), 1)
    per_method_shared = shared / active_count

    print(f"\n{'Method':<25} {'Revenue':>12} {'Direct Cost':>12} {'Shared':>10} {'Net ROI':>12} {'ROI%':>8}")
    print("-" * 85)

    results = []
    for method in sorted(all_methods):
        rev = method_revenue.get(method, 0)
        direct = method_expenses.get(method, 0)
        alloc = per_method_shared if rev > 0 else 0
        net = rev - direct - alloc
        roi_pct = (net / (direct + alloc) * 100) if (direct + alloc) > 0 else 0

        results.append((method, rev, direct, alloc, net, roi_pct))

    results.sort(key=lambda x: -x[4])  # Sort by net

    for method, rev, direct, alloc, net, roi_pct in results:
        print(f"{method:<25} ${rev:>10,.2f} ${direct:>10,.2f} ${alloc:>8,.2f} ${net:>10,.2f} {roi_pct:>6.1f}%")


def cmd_winners(args):
    """Top performing methods."""
    revenue_rows = load_revenue()
    method_revenue = defaultdict(float)
    for row in revenue_rows:
        mid = row.get('method_id', 'UNKNOWN')
        method_revenue[mid] += parse_amount(row.get('net_amount', row.get('amount', '0')))

    sorted_methods = sorted(method_revenue.items(), key=lambda x: -x[1])

    print(f"\nTop Performers (by revenue):")
    print(f"\n{'Rank':<6} {'Method':<25} {'Revenue':>12}")
    print("-" * 45)

    for i, (method, rev) in enumerate(sorted_methods[:10], 1):
        action = "SCALE 2x" if rev > 0 else "NEEDS DATA"
        print(f"{i:<6} {method:<25} ${rev:>10,.2f}  -> {action}")

    if not sorted_methods or all(v == 0 for _, v in sorted_methods):
        print("\n  No revenue data yet. This is pre-revenue stage.")
        print("  Once revenue comes in, this tool auto-ranks methods.")


def cmd_losers(args):
    """Underperforming methods (kill candidates)."""
    revenue_rows = load_revenue()
    expense_rows = load_expenses()

    method_revenue = defaultdict(float)
    method_expenses = defaultdict(float)

    for row in revenue_rows:
        mid = row.get('method_id', 'UNKNOWN')
        method_revenue[mid] += parse_amount(row.get('net_amount', row.get('amount', '0')))

    for row in expense_rows:
        mid = row.get('method_id', 'ALL')
        if mid != 'ALL' and mid != 'NONE':
            method_expenses[mid] += parse_amount(row.get('amount', '0'))

    # Methods with expenses but low/no revenue
    losers = []
    for method in method_expenses:
        rev = method_revenue.get(method, 0)
        exp = method_expenses[method]
        if exp > 0 and (rev == 0 or rev < exp * 0.5):
            losers.append((method, rev, exp))

    losers.sort(key=lambda x: x[2] - x[1], reverse=True)

    print(f"\nUnderperformers (expense > 2x revenue):")
    print(f"\n{'Method':<25} {'Revenue':>12} {'Expenses':>12} {'Gap':>12} {'Action'}")
    print("-" * 75)

    for method, rev, exp in losers[:10]:
        gap = exp - rev
        action = "KILL" if gap > 100 else "ITERATE"
        print(f"{method:<25} ${rev:>10,.2f} ${exp:>10,.2f} ${gap:>10,.2f}  -> {action}")

    if not losers:
        print("  No clear losers identified (pre-revenue or all methods profitable).")


def cmd_projections(args):
    """Revenue projections based on current trajectory."""
    revenue_rows = load_revenue()

    monthly_rev = defaultdict(float)
    for row in revenue_rows:
        date_str = row.get('date', '')
        if len(date_str) >= 7:
            month = date_str[:7]
            monthly_rev[month] += parse_amount(row.get('net_amount', row.get('amount', '0')))

    if not monthly_rev:
        print("\nNo revenue data for projections.")
        print("Once you have 2+ months of data, projections will be calculated.")
        return

    months = sorted(monthly_rev.keys())
    values = [monthly_rev[m] for m in months]

    # Simple projection: average monthly growth rate
    if len(values) >= 2:
        growth_rates = []
        for i in range(1, len(values)):
            if values[i-1] > 0:
                rate = (values[i] - values[i-1]) / values[i-1]
                growth_rates.append(rate)
        avg_growth = sum(growth_rates) / len(growth_rates) if growth_rates else 0
    else:
        avg_growth = 0

    last_month_rev = values[-1] if values else 0

    print(f"\nRevenue Projections:")
    print(f"Last month revenue: ${last_month_rev:,.2f}")
    print(f"Average monthly growth: {avg_growth*100:.1f}%")
    print()

    projected = last_month_rev
    for i in range(1, 13):
        projected = projected * (1 + avg_growth) if avg_growth > 0 else projected
        month_label = f"Month +{i}"
        print(f"  {month_label:<12} ${projected:>10,.2f}")


def cmd_report(args):
    """Full ROI report."""
    print("=" * 70)
    print("   PRINTMAXX ROI ANALYSIS REPORT")
    print(f"   Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)

    # Revenue summary
    revenue_rows = load_revenue()
    total_rev = sum(parse_amount(r.get('net_amount', r.get('amount', '0'))) for r in revenue_rows)

    expense_rows = load_expenses()
    total_exp = sum(parse_amount(r.get('amount', '0')) for r in expense_rows)

    print(f"\n  Total Revenue: ${total_rev:,.2f}")
    print(f"  Total Expenses: ${total_exp:,.2f}")
    print(f"  Net Profit: ${total_rev - total_exp:,.2f}")

    # Paper trades
    paper_trades = load_paper_trades()
    print(f"\n  Paper Trades: {len(paper_trades)} total")

    # Backtests
    backtests = load_backtests()
    if backtests:
        avg_score = sum(int(float(b.get('backtest_score', 0))) for b in backtests) / len(backtests)
        print(f"  Backtests: {len(backtests)} total, avg score: {avg_score:.0f}/100")
    else:
        print(f"  Backtests: None yet")

    print(f"\n  Stage: {'Revenue generating' if total_rev > 0 else 'Pre-revenue (building infrastructure)'}")

    # Method breakdown
    print(f"\n  --- Method Details ---")
    cmd_methods(args)

    print(f"\n  --- Top Performers ---")
    cmd_winners(args)


def main():
    parser = argparse.ArgumentParser(description='ROI Analyzer')
    subparsers = parser.add_subparsers(dest='command')

    subparsers.add_parser('methods', help='ROI by method')
    subparsers.add_parser('winners', help='Top performers')
    subparsers.add_parser('losers', help='Underperformers')
    subparsers.add_parser('projections', help='Revenue projections')
    sub_rph = subparsers.add_parser('revenue-per-hour', help='Revenue per hour ranking')
    subparsers.add_parser('report', help='Full ROI report')

    args = parser.parse_args()

    commands = {
        'methods': cmd_methods,
        'winners': cmd_winners,
        'losers': cmd_losers,
        'projections': cmd_projections,
        'revenue-per-hour': cmd_winners,  # Same data source for now
        'report': cmd_report,
    }

    if args.command in commands:
        commands[args.command](args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
