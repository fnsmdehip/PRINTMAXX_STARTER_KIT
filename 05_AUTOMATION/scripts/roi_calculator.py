#!/usr/bin/env python3
"""
roi_calculator.py - Calculate ROI per money method

Combines revenue and expense data to compute ROI, revenue/hour,
and payback period for each method. Identifies top performers
and methods to scale or kill.

Usage:
    python3 roi_calculator.py
    python3 roi_calculator.py --method MM001
    python3 roi_calculator.py --threshold 100 --sort roi
    python3 roi_calculator.py --output json

Example:
    # Show ROI for all methods
    python3 roi_calculator.py

    # Show detailed ROI for APP_FACTORY
    python3 roi_calculator.py --method MM001

    # Find methods with ROI above 100%
    python3 roi_calculator.py --threshold 100
"""

import argparse
import csv
import json
import logging
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent.parent
FINANCIALS_DIR = PROJECT_DIR / "FINANCIALS"
LEDGER_DIR = PROJECT_DIR / "LEDGER"
LOG_DIR = PROJECT_DIR / "AUTOMATIONS" / "logs"

LOG_DIR.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_DIR / "roi_calculator.log"),
        logging.StreamHandler(sys.stdout),
    ],
)
logger = logging.getLogger(__name__)


def load_csv(filepath):
    """Load CSV file."""
    if not filepath.exists():
        logger.warning(f"File not found: {filepath}")
        return []
    with open(filepath, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def calculate_method_roi():
    """Calculate ROI for each money method."""
    revenue_entries = load_csv(FINANCIALS_DIR / "REVENUE_TRACKER.csv")
    expense_entries = load_csv(FINANCIALS_DIR / "EXPENSE_TRACKER.csv")
    methods = load_csv(LEDGER_DIR / "MONEY_METHODS_TRACKER.csv")

    # Build method name lookup
    method_names = {}
    for m in methods:
        method_names[m.get("method_id", "")] = m.get("method_name", "")

    # Aggregate revenue per method
    rev_by_method = defaultdict(float)
    for entry in revenue_entries:
        if entry.get("customer_id") == "EXAMPLE":
            continue
        try:
            amount = float(entry.get("net_amount", 0))
        except (ValueError, TypeError):
            amount = 0
        rev_by_method[entry.get("method_id", "UNKNOWN")] += amount

    # Aggregate expenses per method
    exp_by_method = defaultdict(float)
    for entry in expense_entries:
        try:
            amount = float(entry.get("amount", 0))
        except (ValueError, TypeError):
            amount = 0
        method_id = entry.get("method_id", "ALL")
        if method_id == "ALL":
            # Distribute shared expenses across all active methods
            active_methods = [m for m in methods if m.get("status") == "Active"]
            if active_methods:
                per_method = amount / len(active_methods)
                for am in active_methods:
                    exp_by_method[am.get("method_id", "")] += per_method
        else:
            exp_by_method[method_id] += amount

    # Calculate ROI per method
    results = []
    all_methods = set(list(rev_by_method.keys()) + list(exp_by_method.keys()))

    for method_id in sorted(all_methods):
        revenue = rev_by_method.get(method_id, 0)
        expenses = exp_by_method.get(method_id, 0)
        profit = revenue - expenses
        roi = (profit / expenses * 100) if expenses > 0 else 0

        # Estimate hours invested (rough: $20/hr equivalent value of time)
        # This is a placeholder. Real tracking would use time_tracker.py
        estimated_hours = max(1, expenses / 20) if expenses > 0 else 10

        results.append({
            "method_id": method_id,
            "method_name": method_names.get(method_id, method_id),
            "total_revenue": round(revenue, 2),
            "total_expenses": round(expenses, 2),
            "profit": round(profit, 2),
            "roi_pct": round(roi, 1),
            "revenue_per_hour": round(revenue / estimated_hours, 2) if estimated_hours > 0 else 0,
            "estimated_hours": round(estimated_hours, 1),
            "status": "PROFITABLE" if profit > 0 else "INVEST" if expenses > 0 else "NO_DATA",
            "recommendation": get_recommendation(roi, revenue, expenses),
        })

    return results


def get_recommendation(roi, revenue, expenses):
    """Generate recommendation based on ROI metrics."""
    if revenue == 0 and expenses == 0:
        return "START - No activity yet"
    if revenue == 0 and expenses > 0:
        return "MONITOR - Invested but no revenue yet"
    if roi >= 200:
        return "SCALE AGGRESSIVELY - 2x investment"
    if roi >= 100:
        return "SCALE - Increase investment 50%"
    if roi >= 50:
        return "OPTIMIZE - Good, improve efficiency"
    if roi >= 0:
        return "HOLD - Breaking even, optimize before scaling"
    if roi >= -50:
        return "REVIEW - Slightly negative, give 30 more days"
    return "KILL - Negative ROI, redirect resources"


def print_roi_table(results, threshold=None, sort_by="roi"):
    """Print ROI results as formatted table."""
    if threshold is not None:
        results = [r for r in results if r["roi_pct"] >= threshold]

    if sort_by == "roi":
        results.sort(key=lambda x: x["roi_pct"], reverse=True)
    elif sort_by == "revenue":
        results.sort(key=lambda x: x["total_revenue"], reverse=True)
    elif sort_by == "profit":
        results.sort(key=lambda x: x["profit"], reverse=True)

    print("\n" + "=" * 90)
    print("  PRINTMAXX ROI CALCULATOR")
    print("=" * 90)
    print(f"  {'Method':<25} {'Revenue':>10} {'Expenses':>10} {'Profit':>10} {'ROI':>8} {'$/hr':>8}  Rec")
    print("-" * 90)

    for r in results:
        roi_str = f"{r['roi_pct']:>6.1f}%"
        print(
            f"  {r['method_id']:<25} "
            f"${r['total_revenue']:>9,.2f} "
            f"${r['total_expenses']:>9,.2f} "
            f"${r['profit']:>9,.2f} "
            f"{roi_str:>8} "
            f"${r['revenue_per_hour']:>7,.2f}  "
            f"{r['recommendation'][:30]}"
        )

    print("-" * 90)
    totals = {
        "revenue": sum(r["total_revenue"] for r in results),
        "expenses": sum(r["total_expenses"] for r in results),
        "profit": sum(r["profit"] for r in results),
    }
    overall_roi = (totals["profit"] / totals["expenses"] * 100) if totals["expenses"] > 0 else 0
    print(
        f"  {'TOTAL':<25} "
        f"${totals['revenue']:>9,.2f} "
        f"${totals['expenses']:>9,.2f} "
        f"${totals['profit']:>9,.2f} "
        f"{overall_roi:>6.1f}%"
    )
    print("=" * 90)


def main():
    parser = argparse.ArgumentParser(
        description="Calculate ROI per PRINTMAXX money method"
    )
    parser.add_argument("--method", type=str, default=None, help="Filter by method ID")
    parser.add_argument("--threshold", type=float, default=None, help="Minimum ROI percent to show")
    parser.add_argument(
        "--sort",
        choices=["roi", "revenue", "profit"],
        default="roi",
        help="Sort by (default: roi)",
    )
    parser.add_argument("--output", choices=["text", "json"], default="text", help="Output format")
    args = parser.parse_args()

    results = calculate_method_roi()

    if args.method:
        results = [r for r in results if r["method_id"] == args.method]

    if args.output == "json":
        print(json.dumps(results, indent=2))
    else:
        print_roi_table(results, threshold=args.threshold, sort_by=args.sort)


if __name__ == "__main__":
    main()
