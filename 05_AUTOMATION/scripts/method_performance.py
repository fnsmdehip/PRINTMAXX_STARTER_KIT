#!/usr/bin/env python3
"""
method_performance.py - Track revenue/hour per money method

Combines revenue data with time tracking estimates to calculate
revenue per hour for each method. Identifies which methods are
worth scaling and which should be killed.

Usage:
    python3 method_performance.py
    python3 method_performance.py --top 5
    python3 method_performance.py --log-time MM001 --hours 2.5 --task "App icon generation"
    python3 method_performance.py --threshold 20

Example:
    # Show performance for all methods
    python3 method_performance.py

    # Log time spent on a method
    python3 method_performance.py --log-time MM001 --hours 3 --task "RevenueCat integration"

    # Show only methods earning above $20/hr
    python3 method_performance.py --threshold 20
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
AUTOMATIONS_DIR = PROJECT_DIR / "AUTOMATIONS"
TIME_LOG = AUTOMATIONS_DIR / "logs" / "time_tracking.csv"
LOG_DIR = AUTOMATIONS_DIR / "logs"

LOG_DIR.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_DIR / "method_performance.log"),
        logging.StreamHandler(sys.stdout),
    ],
)
logger = logging.getLogger(__name__)

# Kill/Scale thresholds (from quant infrastructure)
THRESHOLDS = {
    "SCALE": 50,     # $/hr - scale aggressively
    "GOOD": 20,      # $/hr - continue and optimize
    "HOLD": 10,      # $/hr - monitor closely
    "REVIEW": 5,     # $/hr - review in 2 weeks
    "KILL": 0,       # $/hr - consider killing
}


def load_csv(filepath):
    """Load CSV safely."""
    if not filepath.exists():
        return []
    with open(filepath, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def load_time_log():
    """Load time tracking data."""
    if not TIME_LOG.exists():
        return {}

    entries = load_csv(TIME_LOG)
    hours_by_method = defaultdict(float)
    for entry in entries:
        method = entry.get("method_id", "")
        try:
            hours = float(entry.get("hours", 0))
        except (ValueError, TypeError):
            hours = 0
        hours_by_method[method] += hours

    return dict(hours_by_method)


def log_time(method_id, hours, task=""):
    """Log time spent on a method."""
    fieldnames = ["date", "method_id", "hours", "task", "notes"]

    file_exists = TIME_LOG.exists()
    with open(TIME_LOG, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        writer.writerow({
            "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "method_id": method_id,
            "hours": hours,
            "task": task,
            "notes": "",
        })

    logger.info(f"Logged {hours}h for {method_id}: {task}")


def calculate_performance():
    """Calculate revenue per hour for each method."""
    revenue_entries = load_csv(FINANCIALS_DIR / "REVENUE_TRACKER.csv")
    methods = load_csv(LEDGER_DIR / "MONEY_METHODS_TRACKER.csv")
    time_data = load_time_log()

    # Method name lookup
    method_info = {}
    for m in methods:
        mid = m.get("method_id", "")
        method_info[mid] = {
            "name": m.get("method_name", mid),
            "status": m.get("status", "Unknown"),
            "potential": m.get("monthly_potential", ""),
        }

    # Revenue per method
    rev_by_method = defaultdict(float)
    txn_by_method = defaultdict(int)
    for entry in revenue_entries:
        if entry.get("customer_id") == "EXAMPLE":
            continue
        try:
            amount = float(entry.get("net_amount", 0))
        except (ValueError, TypeError):
            amount = 0
        mid = entry.get("method_id", "UNKNOWN")
        rev_by_method[mid] += amount
        txn_by_method[mid] += 1

    # Calculate performance
    all_methods = set(list(rev_by_method.keys()) + list(time_data.keys()) + list(method_info.keys()))
    results = []

    for method_id in sorted(all_methods):
        if method_id in ("UNKNOWN", ""):
            continue

        revenue = rev_by_method.get(method_id, 0)
        hours = time_data.get(method_id, 0)
        info = method_info.get(method_id, {"name": method_id, "status": "Unknown", "potential": ""})
        txns = txn_by_method.get(method_id, 0)

        # If no time tracked, estimate from status
        if hours == 0:
            if info["status"] == "Active":
                hours = 10  # Minimum estimate for active methods
            elif revenue > 0:
                hours = 5
            else:
                hours = 1  # Placeholder

        rev_per_hour = revenue / hours if hours > 0 else 0

        # Determine action
        if rev_per_hour >= THRESHOLDS["SCALE"]:
            action = "SCALE"
        elif rev_per_hour >= THRESHOLDS["GOOD"]:
            action = "GROW"
        elif rev_per_hour >= THRESHOLDS["HOLD"]:
            action = "HOLD"
        elif rev_per_hour >= THRESHOLDS["REVIEW"]:
            action = "REVIEW"
        elif revenue == 0 and info["status"] in ("Planning", "Active"):
            action = "INVEST"
        else:
            action = "KILL"

        results.append({
            "method_id": method_id,
            "method_name": info["name"],
            "status": info["status"],
            "revenue": round(revenue, 2),
            "hours": round(hours, 1),
            "rev_per_hour": round(rev_per_hour, 2),
            "transactions": txns,
            "potential": info["potential"],
            "action": action,
        })

    return results


def print_performance(results, top=None, threshold=None):
    """Print performance table."""
    # Apply filters
    if threshold is not None:
        results = [r for r in results if r["rev_per_hour"] >= threshold]

    # Sort by revenue per hour
    results.sort(key=lambda x: x["rev_per_hour"], reverse=True)

    if top:
        results = results[:top]

    print("\n" + "=" * 95)
    print("  PRINTMAXX METHOD PERFORMANCE")
    print("=" * 95)
    print(f"  {'Method':<25} {'Status':<10} {'Revenue':>10} {'Hours':>7} {'$/hr':>8} {'Txns':>5}  Action")
    print("-" * 95)

    for r in results:
        action_colors = {
            "SCALE": ">>>", "GROW": " >>", "HOLD": "  >",
            "REVIEW": " !!", "INVEST": " $$", "KILL": " XX",
        }
        indicator = action_colors.get(r["action"], "   ")

        print(
            f"  {r['method_id']:<25} "
            f"{r['status']:<10} "
            f"${r['revenue']:>9,.2f} "
            f"{r['hours']:>6.1f} "
            f"${r['rev_per_hour']:>7,.2f} "
            f"{r['transactions']:>5} "
            f"{indicator} {r['action']}"
        )

    print("-" * 95)

    # Summary stats
    total_rev = sum(r["revenue"] for r in results)
    total_hours = sum(r["hours"] for r in results)
    avg_rph = total_rev / total_hours if total_hours > 0 else 0

    print(f"\n  Total Revenue: ${total_rev:,.2f}")
    print(f"  Total Hours:   {total_hours:,.1f}")
    print(f"  Avg $/hr:      ${avg_rph:,.2f}")

    # Action summary
    from collections import Counter
    actions = Counter(r["action"] for r in results)
    print(f"\n  Actions: {dict(actions)}")
    print("=" * 95)


def main():
    parser = argparse.ArgumentParser(
        description="Track revenue per hour for each money method"
    )
    parser.add_argument("--top", type=int, default=None, help="Show top N methods only")
    parser.add_argument("--threshold", type=float, default=None, help="Min $/hr to show")
    parser.add_argument("--log-time", type=str, default=None, help="Log time for method ID")
    parser.add_argument("--hours", type=float, default=None, help="Hours to log")
    parser.add_argument("--task", type=str, default="", help="Task description")
    parser.add_argument("--output", choices=["text", "json"], default="text")
    args = parser.parse_args()

    if args.log_time:
        if not args.hours:
            parser.error("--log-time requires --hours")
        log_time(args.log_time, args.hours, args.task)
        return

    results = calculate_performance()

    if args.output == "json":
        print(json.dumps(results, indent=2))
    else:
        print_performance(results, top=args.top, threshold=args.threshold)


if __name__ == "__main__":
    main()
