#!/usr/bin/env python3

from __future__ import annotations
"""
run_all_research_ops.py - Master runner for all 5 research ops
Runs all ops in sequence, tracks success/failure, logs to file.
Can be called by cron.

Usage:
    python3 run_all_research_ops.py           # Run all ops
    python3 run_all_research_ops.py --daily    # Run only daily ops
    python3 run_all_research_ops.py --weekly   # Run only weekly ops
    python3 run_all_research_ops.py --op NAME  # Run specific op

Cron examples:
    # Daily at 6 AM
    0 6 * * * cd /Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt && python3 AUTOMATIONS/run_all_research_ops.py --daily
    # Weekly on Monday at 6 AM
    0 6 * * 1 cd /Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt && python3 AUTOMATIONS/run_all_research_ops.py --weekly
"""

import importlib
import importlib.util
import os
import sys
import time
import traceback
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
AUTOMATIONS_DIR = BASE_DIR / "AUTOMATIONS"
LOG_DIR = AUTOMATIONS_DIR / "logs"
LOG_FILE = LOG_DIR / "research_ops.log"

# All research ops with their schedules
RESEARCH_OPS = [
    {
        "name": "platform_algo_detection",
        "script": "platform_algo_detection.py",
        "schedule": "daily",
        "description": "Monitor platform algorithm changes (TikTok, X, Instagram, YouTube)",
        "output": "LEDGER/PLATFORM_ALGO_CHANGES.csv",
    },
    {
        "name": "hashtag_audio_tracking",
        "script": "hashtag_audio_tracking.py",
        "schedule": "daily",
        "description": "Track trending hashtags and audio across platforms",
        "output": "LEDGER/TRENDING_HASHTAGS_AUDIO.csv",
    },
    {
        "name": "platform_rpm_tracking",
        "script": "platform_rpm_tracking.py",
        "schedule": "weekly",
        "description": "Track RPM/CPM rates across platforms by niche",
        "output": "LEDGER/PLATFORM_RPM_TRACKER.csv",
    },
    {
        "name": "creator_program_monitoring",
        "script": "creator_program_monitoring.py",
        "schedule": "weekly",
        "description": "Monitor creator monetization programs across platforms",
        "output": "LEDGER/CREATOR_PROGRAMS.csv",
    },
    {
        "name": "aso_keyword_research",
        "script": "aso_keyword_research.py",
        "schedule": "weekly",
        "description": "App Store Optimization keyword research for our apps",
        "output": "LEDGER/ASO_KEYWORDS.csv",
    },
]


def setup_logging():
    """Ensure log directory exists."""
    LOG_DIR.mkdir(parents=True, exist_ok=True)


def log(message, level="INFO"):
    """Log message to file and stdout."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_line = f"[{timestamp}] [{level}] {message}"
    print(log_line)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(log_line + "\n")


def run_op(op):
    """Run a single research op by importing and calling its main()."""
    script_path = AUTOMATIONS_DIR / op["script"]
    if not script_path.exists():
        log(f"Script not found: {script_path}", "ERROR")
        return False

    log(f"Starting: {op['name']} - {op['description']}")
    start_time = time.time()

    try:
        # Import the module dynamically
        spec = importlib.util.spec_from_file_location(op["name"], script_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        # Call main()
        result = module.main()
        elapsed = time.time() - start_time

        log(f"Completed: {op['name']} in {elapsed:.1f}s - {result} entries", "SUCCESS")

        # Verify output file exists
        output_path = BASE_DIR / op["output"]
        if output_path.exists():
            size = output_path.stat().st_size
            log(f"Output: {op['output']} ({size} bytes)")
        else:
            log(f"Warning: Output file not created: {op['output']}", "WARN")

        return True

    except Exception as e:
        elapsed = time.time() - start_time
        log(f"Failed: {op['name']} after {elapsed:.1f}s - {str(e)}", "ERROR")
        log(f"Traceback: {traceback.format_exc()}", "ERROR")
        return False


def main():
    setup_logging()

    # Parse arguments
    args = sys.argv[1:]
    schedule_filter = None
    op_filter = None

    if "--daily" in args:
        schedule_filter = "daily"
    elif "--weekly" in args:
        schedule_filter = "weekly"

    for i, arg in enumerate(args):
        if arg == "--op" and i + 1 < len(args):
            op_filter = args[i + 1]

    # Filter ops
    ops_to_run = RESEARCH_OPS
    if schedule_filter:
        ops_to_run = [op for op in ops_to_run if op["schedule"] == schedule_filter]
    if op_filter:
        ops_to_run = [op for op in ops_to_run if op["name"] == op_filter]

    if not ops_to_run:
        log("No ops match the filter criteria.", "WARN")
        sys.exit(1)

    # Run
    log("=" * 60)
    log(f"PRINTMAXX RESEARCH OPS RUNNER")
    log(f"Running {len(ops_to_run)} ops ({schedule_filter or 'all'} schedule)")
    log("=" * 60)

    total_start = time.time()
    results = {}

    for op in ops_to_run:
        log(f"\n{'='*40}")
        success = run_op(op)
        results[op["name"]] = "SUCCESS" if success else "FAILED"
        log(f"{'='*40}")
        time.sleep(1)  # Brief pause between ops

    total_elapsed = time.time() - total_start

    # Summary
    log("\n" + "=" * 60)
    log("RUN SUMMARY")
    log("=" * 60)

    succeeded = sum(1 for v in results.values() if v == "SUCCESS")
    failed = sum(1 for v in results.values() if v == "FAILED")

    for name, status in results.items():
        emoji = "OK" if status == "SUCCESS" else "FAIL"
        log(f"  [{emoji}] {name}: {status}")

    log(f"\n  Total: {len(results)} ops | {succeeded} succeeded | {failed} failed")
    log(f"  Total time: {total_elapsed:.1f}s")
    log(f"  Log: {LOG_FILE}")
    log("=" * 60)

    # Exit with error code if any failed
    sys.exit(0 if failed == 0 else 1)


if __name__ == "__main__":
    main()
