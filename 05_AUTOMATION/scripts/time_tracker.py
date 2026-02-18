#!/usr/bin/env python3
"""
time_tracker.py - Track time spent per method and task

Simple time tracking that logs hours per method/task to enable
accurate revenue-per-hour calculations. Integrates with
method_performance.py for ROI analysis.

Usage:
    python3 time_tracker.py start MM001 "Building PrayerLock paywall"
    python3 time_tracker.py stop
    python3 time_tracker.py log MM001 2.5 "RevenueCat integration"
    python3 time_tracker.py report
    python3 time_tracker.py report --method MM001

Example:
    # Start timing a task
    python3 time_tracker.py start MM001 "App icon generation"

    # Stop current timer
    python3 time_tracker.py stop

    # Log time manually (hours)
    python3 time_tracker.py log MM007 1.5 "Cold email sequence writing"

    # Show time report
    python3 time_tracker.py report
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
AUTOMATIONS_DIR = PROJECT_DIR / "AUTOMATIONS"
LOG_DIR = AUTOMATIONS_DIR / "logs"
TIME_LOG = LOG_DIR / "time_tracking.csv"
TIMER_FILE = LOG_DIR / "current_timer.json"

LOG_DIR.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_DIR / "time_tracker.log"),
        logging.StreamHandler(sys.stdout),
    ],
)
logger = logging.getLogger(__name__)


def start_timer(method_id, task):
    """Start a new timer."""
    if TIMER_FILE.exists():
        with open(TIMER_FILE) as f:
            current = json.load(f)
        if current.get("active"):
            logger.warning(f"Timer already running: {current.get('method_id')} - {current.get('task')}")
            logger.warning("Stop current timer first with: python3 time_tracker.py stop")
            return

    timer = {
        "active": True,
        "method_id": method_id,
        "task": task,
        "started_at": datetime.now().isoformat(),
    }

    with open(TIMER_FILE, "w") as f:
        json.dump(timer, f, indent=2)

    logger.info(f"Timer started: {method_id} - {task}")


def stop_timer():
    """Stop the current timer and log the time."""
    if not TIMER_FILE.exists():
        logger.warning("No timer running")
        return

    with open(TIMER_FILE) as f:
        timer = json.load(f)

    if not timer.get("active"):
        logger.warning("No active timer")
        return

    started = datetime.fromisoformat(timer["started_at"])
    elapsed = (datetime.now() - started).total_seconds() / 3600  # Hours

    log_time(timer["method_id"], round(elapsed, 2), timer["task"])

    timer["active"] = False
    with open(TIMER_FILE, "w") as f:
        json.dump(timer, f, indent=2)

    logger.info(f"Timer stopped: {elapsed:.2f} hours logged for {timer['method_id']}")


def log_time(method_id, hours, task="", notes=""):
    """Log time to the tracking CSV."""
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
            "notes": notes,
        })

    logger.info(f"Logged {hours}h for {method_id}: {task}")


def generate_report(method_filter=None, days=None):
    """Generate time tracking report."""
    if not TIME_LOG.exists():
        print("No time data found. Start tracking with: python3 time_tracker.py start MM001 'task'")
        return

    entries = []
    with open(TIME_LOG, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if method_filter and row.get("method_id") != method_filter:
                continue
            try:
                row["hours"] = float(row.get("hours", 0))
            except (ValueError, TypeError):
                row["hours"] = 0
            entries.append(row)

    if not entries:
        print("No matching entries found.")
        return

    # Aggregate by method
    by_method = defaultdict(lambda: {"hours": 0, "tasks": 0, "recent": ""})
    for entry in entries:
        mid = entry.get("method_id", "UNKNOWN")
        by_method[mid]["hours"] += entry["hours"]
        by_method[mid]["tasks"] += 1
        by_method[mid]["recent"] = entry.get("task", "")

    total_hours = sum(d["hours"] for d in by_method.values())

    print("\n" + "=" * 70)
    print("  TIME TRACKING REPORT")
    print("=" * 70)
    print(f"  {'Method':<20} {'Hours':>8} {'Tasks':>6} {'%':>6}  Recent Task")
    print("-" * 70)

    for mid in sorted(by_method, key=lambda x: by_method[x]["hours"], reverse=True):
        d = by_method[mid]
        pct = (d["hours"] / total_hours * 100) if total_hours > 0 else 0
        print(
            f"  {mid:<20} "
            f"{d['hours']:>7.1f}h "
            f"{d['tasks']:>5} "
            f"{pct:>5.1f}%  "
            f"{d['recent'][:30]}"
        )

    print("-" * 70)
    print(f"  {'TOTAL':<20} {total_hours:>7.1f}h {sum(d['tasks'] for d in by_method.values()):>5}")

    # Show current timer
    if TIMER_FILE.exists():
        with open(TIMER_FILE) as f:
            timer = json.load(f)
        if timer.get("active"):
            started = datetime.fromisoformat(timer["started_at"])
            elapsed = (datetime.now() - started).total_seconds() / 3600
            print(f"\n  ACTIVE TIMER: {timer['method_id']} - {timer['task']} ({elapsed:.1f}h)")

    print("=" * 70)


def main():
    parser = argparse.ArgumentParser(
        description="Track time spent per PRINTMAXX method"
    )
    subparsers = parser.add_subparsers(dest="command")

    # Start timer
    start_cmd = subparsers.add_parser("start", help="Start a timer")
    start_cmd.add_argument("method_id", help="Method ID (e.g., MM001)")
    start_cmd.add_argument("task", help="Task description")

    # Stop timer
    subparsers.add_parser("stop", help="Stop current timer")

    # Log time manually
    log_cmd = subparsers.add_parser("log", help="Log time manually")
    log_cmd.add_argument("method_id", help="Method ID")
    log_cmd.add_argument("hours", type=float, help="Hours spent")
    log_cmd.add_argument("task", nargs="?", default="", help="Task description")

    # Report
    report_cmd = subparsers.add_parser("report", help="Show time report")
    report_cmd.add_argument("--method", type=str, default=None, help="Filter by method")
    report_cmd.add_argument("--days", type=int, default=None, help="Lookback days")

    args = parser.parse_args()

    if args.command == "start":
        start_timer(args.method_id, args.task)
    elif args.command == "stop":
        stop_timer()
    elif args.command == "log":
        log_time(args.method_id, args.hours, args.task)
    elif args.command == "report":
        generate_report(args.method, args.days)
    else:
        generate_report()


if __name__ == "__main__":
    main()
