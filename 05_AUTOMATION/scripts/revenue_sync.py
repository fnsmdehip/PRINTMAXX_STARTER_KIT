#!/usr/bin/env python3
"""
Revenue & Financial Sync - Keep FINANCIALS/ in sync with actual data.

Automatically:
1. Calculate P&L from REVENUE_TRACKER + EXPENSE_TRACKER
2. Update FINANCIAL_DASHBOARD.md with latest numbers
3. Check expense budget thresholds (60% revenue cap)
4. Track method-level profitability
5. Generate tax deduction summary

Usage:
    python3 revenue_sync.py                  # Full sync
    python3 revenue_sync.py --pnl            # Update P&L only
    python3 revenue_sync.py --dashboard      # Update dashboard only
    python3 revenue_sync.py --method MM001   # Method profitability
    python3 revenue_sync.py --monthly 2026-02  # Specific month
"""

import csv
import argparse
from pathlib import Path
from datetime import datetime
from collections import defaultdict
from typing import Dict, List

PROJECT_DIR = Path("/Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt")
FINANCIALS_DIR = PROJECT_DIR / "FINANCIALS"
LEDGER_DIR = PROJECT_DIR / "LEDGER"


def load_csv_rows(filepath: Path) -> List[Dict]:
    """Load CSV rows, skipping example rows."""
    rows = []
    if not filepath.exists():
        return rows
    with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Skip example rows
            if any(v == 'EXAMPLE' for v in row.values()):
                continue
            rows.append(row)
    return rows


def parse_amount(value: str) -> float:
    """Parse a monetary amount string to float."""
    try:
        return float(str(value).replace('$', '').replace(',', '').strip())
    except (ValueError, TypeError):
        return 0.0


def sync_pnl():
    """Calculate and update P&L from revenue and expense data."""
    revenue_rows = load_csv_rows(FINANCIALS_DIR / "REVENUE_TRACKER.csv")
    expense_rows = load_csv_rows(FINANCIALS_DIR / "EXPENSE_TRACKER.csv")

    # Group by month
    revenue_by_month = defaultdict(float)
    expenses_by_month = defaultdict(float)
    revenue_by_method = defaultdict(float)
    expenses_by_method = defaultdict(float)

    for row in revenue_rows:
        date_str = row.get('date', '')
        if len(date_str) >= 7:
            month = date_str[:7]  # YYYY-MM
            amount = parse_amount(row.get('net_amount', row.get('amount', '0')))
            revenue_by_month[month] += amount
            method = row.get('method_id', 'UNKNOWN')
            revenue_by_method[method] += amount

    for row in expense_rows:
        date_str = row.get('date', '')
        if len(date_str) >= 7:
            month = date_str[:7]
            amount = parse_amount(row.get('amount', '0'))
            expenses_by_month[month] += amount
            method = row.get('method_id', 'ALL')
            expenses_by_method[method] += amount

    # Write P&L
    pnl_path = FINANCIALS_DIR / "P_AND_L_MONTHLY.csv"
    all_months = sorted(set(list(revenue_by_month.keys()) + list(expenses_by_month.keys())))

    with open(pnl_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['month', 'total_revenue', 'total_expenses', 'net_profit', 'margin_pct', 'notes'])

        cumulative_profit = 0.0
        for month in all_months:
            rev = revenue_by_month.get(month, 0)
            exp = expenses_by_month.get(month, 0)
            profit = rev - exp
            cumulative_profit += profit
            margin = (profit / rev * 100) if rev > 0 else 0

            notes = ""
            if exp > rev * 0.6 and rev > 0:
                notes = "WARNING: expenses exceed 60% of revenue"

            writer.writerow([
                month,
                f"{rev:.2f}",
                f"{exp:.2f}",
                f"{profit:.2f}",
                f"{margin:.1f}",
                notes
            ])

    print(f"P&L updated: {len(all_months)} months in {pnl_path}")
    return revenue_by_month, expenses_by_month, revenue_by_method, expenses_by_method


def update_dashboard(revenue_by_month=None, expenses_by_month=None,
                    revenue_by_method=None, expenses_by_method=None):
    """Update the human-readable financial dashboard."""
    if revenue_by_month is None:
        # Load fresh data
        revenue_by_month, expenses_by_month, revenue_by_method, expenses_by_method = sync_pnl()

    total_revenue = sum(revenue_by_month.values())
    total_expenses = sum(expenses_by_month.values())
    net_profit = total_revenue - total_expenses

    # Current month
    current_month = datetime.now().strftime('%Y-%m')
    month_revenue = revenue_by_month.get(current_month, 0)
    month_expenses = expenses_by_month.get(current_month, 0)

    dashboard = f"""# Financial Dashboard

**Last Updated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## All-Time Summary

| Metric | Amount |
|--------|--------|
| Total Revenue | ${total_revenue:,.2f} |
| Total Expenses | ${total_expenses:,.2f} |
| Net Profit | ${net_profit:,.2f} |
| Profit Margin | {(net_profit/total_revenue*100 if total_revenue > 0 else 0):.1f}% |

## Current Month ({current_month})

| Metric | Amount |
|--------|--------|
| Revenue | ${month_revenue:,.2f} |
| Expenses | ${month_expenses:,.2f} |
| Net | ${month_revenue - month_expenses:,.2f} |

## Revenue by Method

| Method | Revenue | % of Total |
|--------|---------|-----------|
"""

    for method, rev in sorted(revenue_by_method.items(), key=lambda x: -x[1]):
        pct = (rev / total_revenue * 100) if total_revenue > 0 else 0
        dashboard += f"| {method} | ${rev:,.2f} | {pct:.1f}% |\n"

    dashboard += f"""
## Expenses by Category

| Method/Category | Expenses |
|-----------------|----------|
"""

    for method, exp in sorted(expenses_by_method.items(), key=lambda x: -x[1]):
        dashboard += f"| {method} | ${exp:,.2f} |\n"

    dashboard += f"""
## Budget Health

| Check | Status |
|-------|--------|
| Expense ratio | {'OK' if total_expenses <= total_revenue * 0.6 else 'WARNING: exceeds 60%'} |
| Runway | {'Revenue positive' if total_revenue > total_expenses else 'Pre-revenue'} |

## Monthly Trend

| Month | Revenue | Expenses | Net |
|-------|---------|----------|-----|
"""

    for month in sorted(revenue_by_month.keys()):
        rev = revenue_by_month.get(month, 0)
        exp = expenses_by_month.get(month, 0)
        dashboard += f"| {month} | ${rev:,.2f} | ${exp:,.2f} | ${rev - exp:,.2f} |\n"

    dashboard_path = FINANCIALS_DIR / "FINANCIAL_DASHBOARD.md"
    with open(dashboard_path, 'w') as f:
        f.write(dashboard)

    print(f"Dashboard updated: {dashboard_path}")


def method_profitability(method_id: str):
    """Calculate profitability for a specific method."""
    revenue_rows = load_csv_rows(FINANCIALS_DIR / "REVENUE_TRACKER.csv")
    expense_rows = load_csv_rows(FINANCIALS_DIR / "EXPENSE_TRACKER.csv")

    method_revenue = sum(
        parse_amount(r.get('net_amount', r.get('amount', '0')))
        for r in revenue_rows
        if r.get('method_id', '') == method_id
    )

    method_expenses = sum(
        parse_amount(r.get('amount', '0'))
        for r in expense_rows
        if r.get('method_id', '') in (method_id, 'ALL')
    )

    # For ALL expenses, divide proportionally
    all_expenses = sum(
        parse_amount(r.get('amount', '0'))
        for r in expense_rows
        if r.get('method_id', '') == 'ALL'
    )

    total_methods_with_revenue = len(set(
        r.get('method_id') for r in revenue_rows if r.get('method_id')
    ))

    allocated_overhead = all_expenses / max(total_methods_with_revenue, 1)

    print(f"\n=== Method Profitability: {method_id} ===")
    print(f"Direct Revenue: ${method_revenue:,.2f}")
    print(f"Direct Expenses: ${method_expenses:,.2f}")
    print(f"Allocated Overhead: ${allocated_overhead:,.2f}")
    print(f"Net Profit: ${method_revenue - method_expenses - allocated_overhead:,.2f}")


def main():
    parser = argparse.ArgumentParser(description='Revenue & Financial Sync')
    parser.add_argument('--pnl', action='store_true', help='Update P&L only')
    parser.add_argument('--dashboard', action='store_true', help='Update dashboard only')
    parser.add_argument('--method', help='Method profitability (e.g. MM001)')
    parser.add_argument('--monthly', help='Specific month (YYYY-MM)')

    args = parser.parse_args()

    if args.method:
        method_profitability(args.method)
    elif args.pnl:
        sync_pnl()
    elif args.dashboard:
        update_dashboard()
    else:
        # Full sync
        print("Running full financial sync...")
        rev_m, exp_m, rev_method, exp_method = sync_pnl()
        update_dashboard(rev_m, exp_m, rev_method, exp_method)
        print("\nDone. Check FINANCIALS/FINANCIAL_DASHBOARD.md for summary.")


if __name__ == "__main__":
    main()
