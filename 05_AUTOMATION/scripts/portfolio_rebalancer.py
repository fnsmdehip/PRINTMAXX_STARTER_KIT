#!/usr/bin/env python3
"""
portfolio_rebalancer.py - Auto-recommend kill/scale decisions for method portfolio

Analyzes revenue, time investment, and ROI across all money methods.
Applies quant-inspired rules to recommend portfolio rebalancing:
- Kill bottom 50% performers after 30 days
- 2x investment in top performers
- Maintain diversification (no method >40% of revenue)
- Flag concentration risk

Usage:
    python3 portfolio_rebalancer.py
    python3 portfolio_rebalancer.py --strict
    python3 portfolio_rebalancer.py --output json
    python3 portfolio_rebalancer.py --apply (writes recommendations to file)

Example:
    # Get rebalancing recommendations
    python3 portfolio_rebalancer.py

    # Strict mode (lower thresholds, faster kill decisions)
    python3 portfolio_rebalancer.py --strict

    # Save recommendations to file
    python3 portfolio_rebalancer.py --apply
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
LEDGER_DIR = PROJECT_DIR / "LEDGER"
AUTOMATIONS_DIR = PROJECT_DIR / "AUTOMATIONS"
LOG_DIR = AUTOMATIONS_DIR / "logs"
REBALANCE_FILE = AUTOMATIONS_DIR / "logs" / "rebalance_recommendations.csv"

LOG_DIR.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_DIR / "portfolio_rebalancer.log"),
        logging.StreamHandler(sys.stdout),
    ],
)
logger = logging.getLogger(__name__)

# Thresholds
NORMAL_THRESHOLDS = {
    "min_rev_per_hour": 15,      # Kill if below this for 30 days
    "scale_rev_per_hour": 50,    # Scale if above this
    "max_concentration": 0.40,   # Max 40% of revenue from one method
    "min_win_rate": 0.30,        # Kill if win rate below 30% for 60 days
    "min_days_before_kill": 30,  # Don't kill before this many days
    "review_period_days": 14,    # Review period for new methods
}

STRICT_THRESHOLDS = {
    "min_rev_per_hour": 20,
    "scale_rev_per_hour": 40,
    "max_concentration": 0.30,
    "min_win_rate": 0.40,
    "min_days_before_kill": 14,
    "review_period_days": 7,
}


def load_csv(filepath):
    """Load CSV safely."""
    if not filepath.exists():
        return []
    with open(filepath, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def parse_float(value, default=0.0):
    """Safely parse float."""
    try:
        return float(value)
    except (ValueError, TypeError):
        return default


def analyze_portfolio(thresholds):
    """Analyze the full method portfolio."""
    revenue = load_csv(FINANCIALS_DIR / "REVENUE_TRACKER.csv")
    expenses = load_csv(FINANCIALS_DIR / "EXPENSE_TRACKER.csv")
    methods = load_csv(LEDGER_DIR / "MONEY_METHODS_TRACKER.csv")

    # Method info
    method_info = {}
    for m in methods:
        mid = m.get("method_id", "")
        method_info[mid] = {
            "name": m.get("method_name", mid),
            "status": m.get("status", "Unknown"),
            "created": m.get("created_date", ""),
            "potential": m.get("monthly_potential", ""),
        }

    # Revenue aggregation
    rev_by_method = defaultdict(float)
    first_rev_date = {}
    for entry in revenue:
        if entry.get("customer_id") == "EXAMPLE":
            continue
        mid = entry.get("method_id", "UNKNOWN")
        amount = parse_float(entry.get("net_amount", 0))
        rev_by_method[mid] += amount

        date_str = entry.get("date", "")
        if date_str and mid not in first_rev_date:
            first_rev_date[mid] = date_str

    # Expense aggregation
    exp_by_method = defaultdict(float)
    for entry in expenses:
        mid = entry.get("method_id", "ALL")
        amount = parse_float(entry.get("amount", 0))
        if mid == "ALL":
            active = [m for m in methods if m.get("status") == "Active"]
            if active:
                per_method = amount / len(active)
                for am in active:
                    exp_by_method[am.get("method_id", "")] += per_method
        else:
            exp_by_method[mid] += amount

    # Total revenue
    total_revenue = sum(rev_by_method.values())

    # Build recommendations
    recommendations = []
    now = datetime.now()

    for mid, info in method_info.items():
        revenue_total = rev_by_method.get(mid, 0)
        expenses_total = exp_by_method.get(mid, 0)
        profit = revenue_total - expenses_total

        # Estimate hours (rough)
        estimated_hours = max(1, expenses_total / 15) if expenses_total > 0 else 5
        rev_per_hour = revenue_total / estimated_hours if estimated_hours > 0 else 0

        # Calculate concentration
        concentration = (revenue_total / total_revenue) if total_revenue > 0 else 0

        # Calculate days active
        created = info.get("created", "")
        try:
            days_active = (now - datetime.strptime(created, "%Y-%m-%d")).days
        except (ValueError, TypeError):
            days_active = 30  # Default assumption

        # Determine recommendation
        rec = determine_action(
            mid, info, revenue_total, expenses_total, rev_per_hour,
            concentration, days_active, thresholds,
        )

        recommendations.append({
            "method_id": mid,
            "method_name": info["name"],
            "status": info["status"],
            "revenue": round(revenue_total, 2),
            "expenses": round(expenses_total, 2),
            "profit": round(profit, 2),
            "rev_per_hour": round(rev_per_hour, 2),
            "concentration": round(concentration * 100, 1),
            "days_active": days_active,
            "action": rec["action"],
            "reason": rec["reason"],
            "priority": rec["priority"],
        })

    # Sort by priority
    priority_order = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3}
    recommendations.sort(key=lambda x: priority_order.get(x["priority"], 4))

    return recommendations


def determine_action(mid, info, revenue, expenses, rph, concentration, days, thresholds):
    """Determine the recommended action for a method."""
    # Concentration risk
    if concentration > thresholds["max_concentration"]:
        return {
            "action": "DIVERSIFY",
            "reason": f"Concentration {concentration*100:.0f}% exceeds {thresholds['max_concentration']*100:.0f}% limit",
            "priority": "CRITICAL",
        }

    # Too early to kill
    if days < thresholds["min_days_before_kill"] and info["status"] in ("Active", "Planning"):
        if revenue == 0:
            return {
                "action": "INVEST",
                "reason": f"Only {days} days active, under review period",
                "priority": "LOW",
            }

    # Scale high performers
    if rph >= thresholds["scale_rev_per_hour"]:
        return {
            "action": "SCALE_2X",
            "reason": f"${rph:.0f}/hr exceeds scale threshold (${thresholds['scale_rev_per_hour']})",
            "priority": "HIGH",
        }

    # Good performers
    if rph >= thresholds["min_rev_per_hour"]:
        return {
            "action": "CONTINUE",
            "reason": f"${rph:.0f}/hr above minimum",
            "priority": "LOW",
        }

    # Underperformers with enough time
    if days >= thresholds["min_days_before_kill"] and rph < thresholds["min_rev_per_hour"]:
        if revenue == 0:
            return {
                "action": "KILL",
                "reason": f"Zero revenue after {days} days",
                "priority": "HIGH",
            }
        return {
            "action": "REVIEW_KILL",
            "reason": f"${rph:.0f}/hr below minimum after {days} days",
            "priority": "MEDIUM",
        }

    # New methods
    if info["status"] == "Planning":
        return {
            "action": "START",
            "reason": "Not yet started",
            "priority": "MEDIUM",
        }

    return {
        "action": "MONITOR",
        "reason": "Insufficient data",
        "priority": "LOW",
    }


def print_recommendations(recommendations):
    """Print formatted recommendations."""
    print("\n" + "=" * 100)
    print("  PRINTMAXX PORTFOLIO REBALANCER")
    print("=" * 100)

    # Group by action
    actions = defaultdict(list)
    for r in recommendations:
        actions[r["action"]].append(r)

    action_order = ["KILL", "REVIEW_KILL", "DIVERSIFY", "SCALE_2X", "CONTINUE", "START", "INVEST", "MONITOR"]

    for action in action_order:
        if action not in actions:
            continue

        items = actions[action]
        emoji = {
            "KILL": "XX", "REVIEW_KILL": "!!", "DIVERSIFY": "//",
            "SCALE_2X": ">>", "CONTINUE": "OK", "START": "++",
            "INVEST": "$$", "MONITOR": "..",
        }.get(action, "  ")

        print(f"\n  [{emoji}] {action} ({len(items)} methods)")
        print("-" * 100)

        for r in items:
            print(
                f"    {r['method_id']:<20} "
                f"Rev: ${r['revenue']:>8,.2f} | "
                f"$/hr: ${r['rev_per_hour']:>6,.2f} | "
                f"Conc: {r['concentration']:>5.1f}% | "
                f"Days: {r['days_active']:>3} | "
                f"{r['reason']}"
            )

    # Portfolio summary
    total_rev = sum(r["revenue"] for r in recommendations)
    active = [r for r in recommendations if r["status"] == "Active"]
    profitable = [r for r in recommendations if r["profit"] > 0]

    print(f"\n{'--- PORTFOLIO SUMMARY ---':^100}")
    print(f"  Total Methods: {len(recommendations)}")
    print(f"  Active: {len(active)}")
    print(f"  Profitable: {len(profitable)}")
    print(f"  Total Revenue: ${total_rev:,.2f}")
    print(f"  To Kill: {len(actions.get('KILL', []))}")
    print(f"  To Scale: {len(actions.get('SCALE_2X', []))}")
    print("=" * 100)


def save_recommendations(recommendations):
    """Save recommendations to CSV."""
    fieldnames = [
        "date", "method_id", "method_name", "action", "reason",
        "priority", "revenue", "rev_per_hour", "concentration",
    ]

    with open(REBALANCE_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for r in recommendations:
            writer.writerow({
                "date": datetime.now().strftime("%Y-%m-%d"),
                "method_id": r["method_id"],
                "method_name": r["method_name"],
                "action": r["action"],
                "reason": r["reason"],
                "priority": r["priority"],
                "revenue": r["revenue"],
                "rev_per_hour": r["rev_per_hour"],
                "concentration": r["concentration"],
            })

    logger.info(f"Saved recommendations to {REBALANCE_FILE}")


def main():
    parser = argparse.ArgumentParser(
        description="Auto-recommend kill/scale decisions for method portfolio"
    )
    parser.add_argument("--strict", action="store_true", help="Use strict thresholds")
    parser.add_argument("--apply", action="store_true", help="Save recommendations to file")
    parser.add_argument("--output", choices=["text", "json"], default="text")
    args = parser.parse_args()

    thresholds = STRICT_THRESHOLDS if args.strict else NORMAL_THRESHOLDS
    recommendations = analyze_portfolio(thresholds)

    if args.apply:
        save_recommendations(recommendations)

    if args.output == "json":
        print(json.dumps(recommendations, indent=2))
    else:
        print_recommendations(recommendations)


if __name__ == "__main__":
    main()
