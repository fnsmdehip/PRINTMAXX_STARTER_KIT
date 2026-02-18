#!/usr/bin/env python3
"""
profit_analyzer.py - Generate P&L reports from revenue and expense data

Reads FINANCIALS/ CSVs, generates monthly/quarterly/annual P&L reports,
identifies trends, and flags anomalies.

Usage:
    python3 profit_analyzer.py --period monthly
    python3 profit_analyzer.py --period quarterly --output json
    python3 profit_analyzer.py --update-pnl
    python3 profit_analyzer.py --forecast 3

Example:
    # Generate monthly P&L report
    python3 profit_analyzer.py --period monthly

    # Update P_AND_L_MONTHLY.csv with current data
    python3 profit_analyzer.py --update-pnl

    # Forecast next 3 months based on trends
    python3 profit_analyzer.py --forecast 3
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
LOG_DIR = PROJECT_DIR / "AUTOMATIONS" / "logs"

LOG_DIR.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_DIR / "profit_analyzer.log"),
        logging.StreamHandler(sys.stdout),
    ],
)
logger = logging.getLogger(__name__)


def load_csv(filepath):
    """Load CSV safely."""
    if not filepath.exists():
        logger.warning(f"File not found: {filepath}")
        return []
    with open(filepath, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def parse_amount(value):
    """Safely parse amount to float."""
    try:
        return float(value)
    except (ValueError, TypeError):
        return 0.0


def build_monthly_pnl():
    """Build P&L by month from raw data."""
    revenue = load_csv(FINANCIALS_DIR / "REVENUE_TRACKER.csv")
    expenses = load_csv(FINANCIALS_DIR / "EXPENSE_TRACKER.csv")

    months = defaultdict(lambda: {
        "revenue": 0, "expenses": 0, "fees": 0,
        "revenue_by_method": defaultdict(float),
        "expense_by_category": defaultdict(float),
        "transactions": 0,
    })

    for entry in revenue:
        if entry.get("customer_id") == "EXAMPLE":
            continue
        date_str = entry.get("date", "")
        try:
            month = datetime.strptime(date_str, "%Y-%m-%d").strftime("%Y-%m")
        except ValueError:
            continue

        amount = parse_amount(entry.get("amount", 0))
        fees = parse_amount(entry.get("fees", 0))
        method = entry.get("method_id", "UNKNOWN")

        months[month]["revenue"] += amount
        months[month]["fees"] += fees
        months[month]["revenue_by_method"][method] += amount
        months[month]["transactions"] += 1

    for entry in expenses:
        date_str = entry.get("date", "")
        try:
            month = datetime.strptime(date_str, "%Y-%m-%d").strftime("%Y-%m")
        except ValueError:
            continue

        amount = parse_amount(entry.get("amount", 0))
        category = entry.get("category", "other")

        months[month]["expenses"] += amount
        months[month]["expense_by_category"][category] += amount

    return dict(months)


def build_quarterly_pnl(monthly_data):
    """Aggregate monthly into quarterly."""
    quarters = defaultdict(lambda: {"revenue": 0, "expenses": 0, "fees": 0, "months": 0})

    for month, data in monthly_data.items():
        try:
            dt = datetime.strptime(month, "%Y-%m")
            q = (dt.month - 1) // 3 + 1
            quarter_key = f"{dt.year}-Q{q}"
        except ValueError:
            continue

        quarters[quarter_key]["revenue"] += data["revenue"]
        quarters[quarter_key]["expenses"] += data["expenses"]
        quarters[quarter_key]["fees"] += data["fees"]
        quarters[quarter_key]["months"] += 1

    return dict(quarters)


def calculate_trends(monthly_data):
    """Calculate month-over-month growth trends."""
    sorted_months = sorted(monthly_data.keys())
    trends = []

    for i in range(1, len(sorted_months)):
        prev_month = sorted_months[i - 1]
        curr_month = sorted_months[i]
        prev_rev = monthly_data[prev_month]["revenue"]
        curr_rev = monthly_data[curr_month]["revenue"]

        growth = 0
        if prev_rev > 0:
            growth = ((curr_rev - prev_rev) / prev_rev) * 100

        trends.append({
            "month": curr_month,
            "revenue": curr_rev,
            "prev_revenue": prev_rev,
            "growth_pct": round(growth, 1),
            "profit": curr_rev - monthly_data[curr_month]["expenses"],
        })

    return trends


def forecast_revenue(monthly_data, months_ahead=3):
    """Simple linear forecast based on recent trends."""
    sorted_months = sorted(monthly_data.keys())
    if len(sorted_months) < 2:
        return []

    # Use last 3 months for trend
    recent = sorted_months[-3:]
    revenues = [monthly_data[m]["revenue"] for m in recent]

    if len(revenues) < 2:
        avg_growth = 0
    else:
        growths = []
        for i in range(1, len(revenues)):
            if revenues[i - 1] > 0:
                growths.append((revenues[i] - revenues[i - 1]) / revenues[i - 1])
            else:
                growths.append(0)
        avg_growth = sum(growths) / len(growths) if growths else 0

    forecasts = []
    last_rev = revenues[-1] if revenues else 0
    last_month = datetime.strptime(sorted_months[-1], "%Y-%m")

    for i in range(1, months_ahead + 1):
        forecast_month = last_month + timedelta(days=32 * i)
        forecast_month = forecast_month.replace(day=1)
        projected = last_rev * (1 + avg_growth) ** i

        forecasts.append({
            "month": forecast_month.strftime("%Y-%m"),
            "projected_revenue": round(projected, 2),
            "growth_rate": round(avg_growth * 100, 1),
            "confidence": "LOW" if len(recent) < 3 else "MEDIUM",
        })

    return forecasts


def update_pnl_file(monthly_data):
    """Update P_AND_L_MONTHLY.csv."""
    pnl_file = FINANCIALS_DIR / "P_AND_L_MONTHLY.csv"
    fieldnames = [
        "month", "total_revenue", "total_expenses", "gross_profit",
        "margin_pct", "revenue_by_method", "top_expense_category",
        "runway_months", "reinvestment_amount", "investment_amount", "notes",
    ]

    rows = []
    for month in sorted(monthly_data.keys()):
        data = monthly_data[month]
        revenue = data["revenue"]
        expenses = data["expenses"]
        profit = revenue - expenses
        margin = (profit / revenue * 100) if revenue > 0 else -100 if expenses > 0 else 0

        # Top expense category
        top_cat = ""
        if data["expense_by_category"]:
            top_cat = max(data["expense_by_category"], key=data["expense_by_category"].get)

        # Revenue by method string
        rev_str = "|".join(
            f"{m}:{v:.0f}" for m, v in sorted(data["revenue_by_method"].items())
        )

        rows.append({
            "month": month,
            "total_revenue": round(revenue, 2),
            "total_expenses": round(expenses, 2),
            "gross_profit": round(profit, 2),
            "margin_pct": round(margin, 1),
            "revenue_by_method": rev_str or "none",
            "top_expense_category": top_cat or "none",
            "runway_months": 0,
            "reinvestment_amount": 0,
            "investment_amount": 0,
            "notes": f"Auto-generated {datetime.now().strftime('%Y-%m-%d')}",
        })

    with open(pnl_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    logger.info(f"Updated {pnl_file} with {len(rows)} months")


def print_pnl_report(monthly_data, period="monthly"):
    """Print formatted P&L report."""
    if period == "quarterly":
        data = build_quarterly_pnl(monthly_data)
        period_label = "Quarter"
    else:
        data = monthly_data
        period_label = "Month"

    print("\n" + "=" * 70)
    print(f"  PRINTMAXX P&L REPORT ({period.upper()})")
    print("=" * 70)
    print(f"  {period_label:<15} {'Revenue':>12} {'Expenses':>12} {'Profit':>12} {'Margin':>8}")
    print("-" * 70)

    total_rev = 0
    total_exp = 0

    for key in sorted(data.keys()):
        d = data[key]
        revenue = d["revenue"]
        expenses = d["expenses"]
        profit = revenue - expenses
        margin = (profit / revenue * 100) if revenue > 0 else 0

        total_rev += revenue
        total_exp += expenses

        margin_str = f"{margin:.1f}%"
        print(
            f"  {key:<15} "
            f"${revenue:>11,.2f} "
            f"${expenses:>11,.2f} "
            f"${profit:>11,.2f} "
            f"{margin_str:>8}"
        )

    total_profit = total_rev - total_exp
    total_margin = (total_profit / total_rev * 100) if total_rev > 0 else 0

    print("-" * 70)
    print(
        f"  {'TOTAL':<15} "
        f"${total_rev:>11,.2f} "
        f"${total_exp:>11,.2f} "
        f"${total_profit:>11,.2f} "
        f"{total_margin:.1f}%"
    )
    print("=" * 70)

    # Trends
    trends = calculate_trends(monthly_data)
    if trends:
        print(f"\n{'--- TRENDS ---':^70}")
        for t in trends[-6:]:
            direction = "+" if t["growth_pct"] >= 0 else ""
            print(
                f"  {t['month']}: ${t['revenue']:,.2f} "
                f"({direction}{t['growth_pct']}% MoM)"
            )


def main():
    parser = argparse.ArgumentParser(
        description="Generate P&L reports from FINANCIALS data"
    )
    parser.add_argument(
        "--period",
        choices=["monthly", "quarterly"],
        default="monthly",
        help="Report period",
    )
    parser.add_argument("--update-pnl", action="store_true", help="Update P_AND_L_MONTHLY.csv")
    parser.add_argument("--forecast", type=int, default=0, help="Forecast N months ahead")
    parser.add_argument("--output", choices=["text", "json"], default="text", help="Output format")
    args = parser.parse_args()

    monthly_data = build_monthly_pnl()

    if args.update_pnl:
        update_pnl_file(monthly_data)
        return

    if args.output == "json":
        result = {
            "monthly": {k: {kk: vv for kk, vv in v.items() if kk not in ("revenue_by_method", "expense_by_category")} for k, v in monthly_data.items()},
            "trends": calculate_trends(monthly_data),
        }
        if args.forecast:
            result["forecast"] = forecast_revenue(monthly_data, args.forecast)
        print(json.dumps(result, indent=2, default=str))
    else:
        print_pnl_report(monthly_data, args.period)

        if args.forecast:
            forecasts = forecast_revenue(monthly_data, args.forecast)
            if forecasts:
                print(f"\n{'--- FORECAST ---':^70}")
                for f in forecasts:
                    print(
                        f"  {f['month']}: ${f['projected_revenue']:,.2f} "
                        f"(growth: {f['growth_rate']}%, confidence: {f['confidence']})"
                    )


if __name__ == "__main__":
    main()
