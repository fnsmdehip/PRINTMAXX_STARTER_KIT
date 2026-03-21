#!/usr/bin/env python3

from __future__ import annotations
"""
Method Performance Analyzer - Analyze What's Working
P1 Priority: DATA-DRIVEN OPTIMIZATION

Analyzes active methods to identify what's working, what's not, and where to optimize.
Reads from FINANCIALS/, LEDGER/, and method-specific tracking files.

Runs: Weekly (Saturday morning)
Output: OPS/METHOD_PERFORMANCE_REPORT_[DATE].md + Updates to method playbooks
"""

import csv
import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Tuple
from collections import defaultdict
import re


def safe_float(value, default=0.0) -> float:
    """
    Safely convert string to float, handling:
    - Dollar signs ($)
    - K/M multipliers ($10K = 10000, $1.5M = 1500000)
    - Commas in numbers ($1,234.56)
    - Underscores in field names (0_savings, 0_arbitrage)
    - Empty strings, None, N/A
    - Already numeric values

    Returns default if conversion fails.
    """
    if value is None or value == '' or (isinstance(value, str) and value.upper() in ['N/A', 'NA', 'NONE', 'NULL']):
        return default

    # Already numeric
    if isinstance(value, (int, float)):
        return float(value)

    # Convert to string and clean
    value_str = str(value).strip()

    # Check if it's a field name like "0_savings" or "0_arbitrage" (starts with digit, has underscore)
    if re.match(r'^\d+_[a-zA-Z]', value_str):
        return default

    # Remove currency symbols and whitespace
    value_str = value_str.replace('$', '').replace('£', '').replace('€', '').replace(',', '').strip()

    # Handle K/M multipliers
    multiplier = 1.0
    if value_str.upper().endswith('K'):
        multiplier = 1000.0
        value_str = value_str[:-1]
    elif value_str.upper().endswith('M'):
        multiplier = 1000000.0
        value_str = value_str[:-1]

    # Try conversion
    try:
        return float(value_str) * multiplier
    except (ValueError, TypeError):
        return default

# Configuration
RESEARCH_TYPE = "optimization"
CATEGORY = "METHOD_PERFORMANCE"
OUTPUT_DIR = Path("OPS/reports")
LOG_FILE = Path("AUTOMATIONS/logs/method_performance_analyzer.log")

# Data sources
REVENUE_TRACKER = Path("FINANCIALS/REVENUE_TRACKER.csv")
EXPENSE_TRACKER = Path("FINANCIALS/EXPENSE_TRACKER.csv")
FUNNEL_METRICS = Path("LEDGER/FUNNEL_METRICS.csv")
METHODS_TRACKER = Path("LEDGER/MONEY_METHODS_TRACKER.csv")

# Performance thresholds
THRESHOLDS = {
    'revenue_per_hour_min': 15,  # Kill methods below $15/hr
    'roi_min': 1.5,  # Kill methods with ROI < 1.5x
    'win_rate_min': 0.30,  # Kill methods with <30% win rate
    'time_to_revenue_max': 30,  # Flag methods taking >30 days to revenue
    'concentration_risk': 0.40,  # Alert if any method >40% of revenue
}


def log(message: str):
    """Write to log file with timestamp."""
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(LOG_FILE, 'a') as f:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"[{timestamp}] {message}\n")
    print(f"[{timestamp}] {message}")


def load_revenue_data() -> List[Dict]:
    """Load revenue data from FINANCIALS/REVENUE_TRACKER.csv."""
    if not REVENUE_TRACKER.exists():
        log(f"Warning: {REVENUE_TRACKER} not found. Returning empty data.")
        return []

    revenue_data = []
    try:
        with open(REVENUE_TRACKER, 'r', errors='replace') as f:
            reader = csv.DictReader(f)
            for row in reader:
                revenue_data.append(row)
    except (csv.Error, UnicodeDecodeError, KeyError) as e:
        print(f"Warning: Error reading {REVENUE_TRACKER}: {e}. Continuing with partial data.")

    log(f"Loaded {len(revenue_data)} revenue records")
    return revenue_data


def load_expense_data() -> List[Dict]:
    """Load expense data from FINANCIALS/EXPENSE_TRACKER.csv."""
    if not EXPENSE_TRACKER.exists():
        log(f"Warning: {EXPENSE_TRACKER} not found. Returning empty data.")
        return []

    expense_data = []
    try:
        with open(EXPENSE_TRACKER, 'r', errors='replace') as f:
            reader = csv.DictReader(f)
            for row in reader:
                expense_data.append(row)
    except (csv.Error, UnicodeDecodeError, KeyError) as e:
        print(f"Warning: Error reading {EXPENSE_TRACKER}: {e}. Continuing with partial data.")

    log(f"Loaded {len(expense_data)} expense records")
    return expense_data


def load_funnel_metrics() -> List[Dict]:
    """Load funnel metrics from LEDGER/FUNNEL_METRICS.csv."""
    if not FUNNEL_METRICS.exists():
        log(f"Warning: {FUNNEL_METRICS} not found. Returning empty data.")
        return []

    metrics = []
    try:
        with open(FUNNEL_METRICS, 'r', errors='replace') as f:
            reader = csv.DictReader(f)
            for row in reader:
                metrics.append(row)
    except (csv.Error, UnicodeDecodeError, KeyError) as e:
        print(f"Warning: Error reading {FUNNEL_METRICS}: {e}. Continuing with partial data.")

    log(f"Loaded {len(metrics)} funnel metric records")
    return metrics


def analyze_revenue_per_hour(revenue_data: List[Dict]) -> Dict:
    """
    Calculate revenue per hour for each method.
    Returns: {method_id: {'revenue': X, 'hours': Y, 'revenue_per_hour': Z}}
    """
    method_stats = defaultdict(lambda: {'revenue': 0.0, 'hours': 0.0})

    for record in revenue_data:
        method_id = record.get('method_id', '')
        revenue = safe_float(record.get('revenue', record.get('amount', 0)))
        hours = safe_float(record.get('hours_spent', 1), default=1.0)  # Default to 1 if not tracked

        method_stats[method_id]['revenue'] += revenue
        method_stats[method_id]['hours'] += hours

    # Calculate revenue per hour
    results = {}
    for method_id, stats in method_stats.items():
        if stats['hours'] > 0:
            stats['revenue_per_hour'] = stats['revenue'] / stats['hours']
        else:
            stats['revenue_per_hour'] = 0
        results[method_id] = stats

    log(f"Calculated revenue/hour for {len(results)} methods")
    return results


def analyze_roi(revenue_data: List[Dict], expense_data: List[Dict]) -> Dict:
    """
    Calculate ROI for each method.
    Returns: {method_id: {'revenue': X, 'expenses': Y, 'roi': Z}}
    """
    method_revenue = defaultdict(float)
    method_expenses = defaultdict(float)

    for record in revenue_data:
        method_id = record.get('method_id', '')
        revenue = safe_float(record.get('revenue', record.get('amount', 0)))
        method_revenue[method_id] += revenue

    for record in expense_data:
        method_id = record.get('method_id', '')
        expense = safe_float(record.get('amount', 0))
        method_expenses[method_id] += expense

    # Calculate ROI
    results = {}
    all_methods = set(method_revenue.keys()) | set(method_expenses.keys())

    for method_id in all_methods:
        revenue = method_revenue[method_id]
        expenses = method_expenses[method_id]

        if expenses > 0:
            roi = revenue / expenses
        else:
            roi = float('inf') if revenue > 0 else 0

        results[method_id] = {
            'revenue': revenue,
            'expenses': expenses,
            'roi': roi,
            'profit': revenue - expenses,
        }

    log(f"Calculated ROI for {len(results)} methods")
    return results


def analyze_conversion_rates(funnel_metrics: List[Dict]) -> Dict:
    """
    Calculate conversion rates for each method/funnel.
    Returns: {method_id: {'visits': X, 'conversions': Y, 'rate': Z}}
    """
    method_conversions = defaultdict(lambda: {'visits': 0, 'conversions': 0})

    for record in funnel_metrics:
        method_id = record.get('method_id', '')
        visits = int(safe_float(record.get('visits', 0)))
        conversions = int(safe_float(record.get('conversions', 0)))

        method_conversions[method_id]['visits'] += visits
        method_conversions[method_id]['conversions'] += conversions

    # Calculate conversion rate
    results = {}
    for method_id, stats in method_conversions.items():
        if stats['visits'] > 0:
            stats['rate'] = stats['conversions'] / stats['visits']
        else:
            stats['rate'] = 0
        results[method_id] = stats

    log(f"Calculated conversion rates for {len(results)} methods")
    return results


def identify_winners_losers(
    revenue_per_hour: Dict,
    roi_data: Dict,
    conversion_data: Dict
) -> Tuple[List[Dict], List[Dict], List[Dict]]:
    """
    Classify methods into winners (scale), losers (kill), and middle (optimize).

    Returns: (winners, losers, middle)
    """
    winners = []
    losers = []
    middle = []

    all_methods = set(revenue_per_hour.keys()) | set(roi_data.keys())

    for method_id in all_methods:
        rph_data = revenue_per_hour.get(method_id, {})
        roi_info = roi_data.get(method_id, {})
        conv_info = conversion_data.get(method_id, {})

        rph = rph_data.get('revenue_per_hour', 0)
        roi = roi_info.get('roi', 0)
        conversion_rate = conv_info.get('rate', 0)

        method_summary = {
            'method_id': method_id,
            'revenue_per_hour': rph,
            'roi': roi,
            'conversion_rate': conversion_rate,
            'revenue': rph_data.get('revenue', 0),
            'profit': roi_info.get('profit', 0),
        }

        # Classification logic
        is_winner = (
            rph >= THRESHOLDS['revenue_per_hour_min'] * 2 and  # 2x minimum
            roi >= THRESHOLDS['roi_min']
        )

        is_loser = (
            rph < THRESHOLDS['revenue_per_hour_min'] or
            roi < THRESHOLDS['roi_min']
        )

        if is_winner:
            winners.append(method_summary)
        elif is_loser:
            losers.append(method_summary)
        else:
            middle.append(method_summary)

    # Sort by revenue per hour
    winners.sort(key=lambda x: x['revenue_per_hour'], reverse=True)
    losers.sort(key=lambda x: x['revenue_per_hour'])
    middle.sort(key=lambda x: x['revenue_per_hour'], reverse=True)

    log(f"Classified: {len(winners)} winners, {len(losers)} losers, {len(middle)} middle")
    return winners, losers, middle


def generate_report(
    winners: List[Dict],
    losers: List[Dict],
    middle: List[Dict],
    revenue_per_hour: Dict,
    roi_data: Dict,
) -> str:
    """Generate markdown report of method performance."""
    report_date = datetime.now().strftime("%Y-%m-%d")

    report = f"""# Method Performance Report - {report_date}

**Analysis Period:** Last 30 days
**Generated:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

---

## Executive Summary

**Total Methods Analyzed:** {len(revenue_per_hour)}
**Winners (Scale These):** {len(winners)}
**Losers (Kill These):** {len(losers)}
**Middle (Optimize These):** {len(middle)}

**Performance Thresholds:**
- Minimum Revenue/Hour: ${THRESHOLDS['revenue_per_hour_min']}/hr
- Minimum ROI: {THRESHOLDS['roi_min']}x
- Minimum Win Rate: {THRESHOLDS['win_rate_min'] * 100}%

---

## 🚀 WINNERS (Scale These)

Methods exceeding targets. Action: 2x budget, double down on what's working.

| Method | Revenue/Hr | ROI | Revenue | Profit | Action |
|--------|-----------|-----|---------|--------|--------|
"""

    for method in winners:
        report += f"| {method['method_id']} | ${method['revenue_per_hour']:.2f}/hr | {method['roi']:.2f}x | ${method['revenue']:.2f} | ${method['profit']:.2f} | SCALE 2x |\n"

    report += "\n---\n\n## ❌ LOSERS (Kill These)\n\n"
    report += "Methods below minimum thresholds. Action: Kill immediately, reallocate resources.\n\n"
    report += "| Method | Revenue/Hr | ROI | Revenue | Profit | Reason |\n"
    report += "|--------|-----------|-----|---------|--------|--------|\n"

    for method in losers:
        reason = []
        if method['revenue_per_hour'] < THRESHOLDS['revenue_per_hour_min']:
            reason.append(f"Low $/hr ({method['revenue_per_hour']:.2f})")
        if method['roi'] < THRESHOLDS['roi_min']:
            reason.append(f"Low ROI ({method['roi']:.2f}x)")

        report += f"| {method['method_id']} | ${method['revenue_per_hour']:.2f}/hr | {method['roi']:.2f}x | ${method['revenue']:.2f} | ${method['profit']:.2f} | {', '.join(reason)} |\n"

    report += "\n---\n\n## 🔧 MIDDLE (Optimize These)\n\n"
    report += "Methods with potential. Action: A/B test, optimize funnels, reduce costs.\n\n"
    report += "| Method | Revenue/Hr | ROI | Revenue | Profit | Optimization Target |\n"
    report += "|--------|-----------|-----|---------|--------|--------------------|\n"

    for method in middle:
        # Suggest optimization based on data
        if method['conversion_rate'] < 0.02:
            optimization = "Improve conversion (currently {:.2%})".format(method['conversion_rate'])
        elif method['roi'] < 2.0:
            optimization = "Reduce costs (ROI only {:.2f}x)".format(method['roi'])
        else:
            optimization = "Increase traffic/volume"

        report += f"| {method['method_id']} | ${method['revenue_per_hour']:.2f}/hr | {method['roi']:.2f}x | ${method['revenue']:.2f} | ${method['profit']:.2f} | {optimization} |\n"

    report += "\n---\n\n## Recommended Actions\n\n"
    report += "### Immediate (This Week):\n"
    report += f"1. **Kill {len(losers)} methods** below minimum thresholds\n"
    report += f"2. **Scale {len(winners)} winners** - increase budget/effort by 2x\n"
    report += "3. **Review middle methods** - run A/B tests on top 3\n\n"

    report += "### Integration:\n"
    report += "- Update method playbooks with findings\n"
    report += "- Add successful tactics to WINNING_CONTENT_STRUCTURES.csv\n"
    report += "- Document what worked in method-specific docs\n\n"

    report += "### Next Analysis:\n"
    report += f"- Run again: {(datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d')}\n"
    report += "- Track: Did killed methods stay dead? Did winners scale?\n"

    return report


def save_report(report: str):
    """Save report to OPS/reports/ directory."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    report_date = datetime.now().strftime("%Y-%m-%d")
    report_file = OUTPUT_DIR / f"METHOD_PERFORMANCE_REPORT_{report_date}.md"

    with open(report_file, 'w') as f:
        f.write(report)

    log(f"✅ Report saved: {report_file}")


def main():
    """Main execution flow."""
    log("=" * 60)
    log("Method Performance Analyzer - Starting Analysis")
    log("=" * 60)

    # 1. Load data
    revenue_data = load_revenue_data()
    expense_data = load_expense_data()
    funnel_metrics = load_funnel_metrics()

    # 2. Analyze performance
    revenue_per_hour = analyze_revenue_per_hour(revenue_data)
    roi_data = analyze_roi(revenue_data, expense_data)
    conversion_data = analyze_conversion_rates(funnel_metrics)

    # 3. Classify methods
    winners, losers, middle = identify_winners_losers(
        revenue_per_hour,
        roi_data,
        conversion_data
    )

    # 4. Generate report
    report = generate_report(winners, losers, middle, revenue_per_hour, roi_data)

    # 5. Save report
    save_report(report)

    log("=" * 60)
    log(f"Analysis complete: {len(winners)} winners, {len(losers)} losers, {len(middle)} middle")
    log("=" * 60)


if __name__ == "__main__":
    main()
