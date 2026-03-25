#!/usr/bin/env python3
"""
Usage Optimizer — Maximize Claude Pro/Max subscription utilization.

Rate limits work on a 5h rolling window. When the window is about to reset
and there's unused capacity, fire all queued tasks to use 100% of the allocation.

How it works:
1. Check usage via OAuth usage endpoint (GET /api/oauth/usage)
2. If <30 min left in window AND usage < 80%, trigger queued tasks
3. Tasks are prioritized: revenue-generating > maintenance > research

Usage:
    python3 usage_optimizer.py --check          # Check current usage window
    python3 usage_optimizer.py --optimize       # Fire tasks if window ending
    python3 usage_optimizer.py --status         # Show optimization history
    python3 usage_optimizer.py --queue          # Show queued tasks
    python3 usage_optimizer.py --add "task"     # Add task to burst queue

Cron: Run every 15 minutes to catch window ends
*/15 * * * * python3 AUTOMATIONS/usage_optimizer.py --optimize >> AUTOMATIONS/logs/usage_optimizer.log 2>&1
"""

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime, timedelta
from pathlib import Path

PROJECT = Path(__file__).resolve().parent.parent
AUTOMATIONS = PROJECT / "AUTOMATIONS"
LOG_FILE = AUTOMATIONS / "logs" / "usage_optimizer.log"
STATE_FILE = AUTOMATIONS / "agent" / "usage_optimizer_state.json"
QUEUE_FILE = AUTOMATIONS / "agent" / "burst_queue.json"

# Tasks to fire during burst windows, ordered by priority
# These are real scripts that produce value when run
DEFAULT_BURST_TASKS = [
    # P0: Revenue-generating
    {"name": "integrator", "cmd": "python3 AUTOMATIONS/autonomous_integrator.py --process-today --limit 50", "priority": 0, "category": "revenue"},
    {"name": "rbi_loop", "cmd": "python3 AUTOMATIONS/rbi_loop.py --full", "priority": 0, "category": "revenue"},
    {"name": "method_discovery", "cmd": "python3 AUTOMATIONS/method_discovery_crawler.py --crawl", "priority": 0, "category": "revenue"},
    # P1: Pipeline maintenance
    {"name": "loop_closer", "cmd": "python3 AUTOMATIONS/loop_closer.py --cycle", "priority": 1, "category": "maintenance"},
    {"name": "alpha_backlog", "cmd": "python3 AUTOMATIONS/alpha_backlog_scanner.py --scan", "priority": 1, "category": "maintenance"},
    {"name": "capital_genesis", "cmd": "python3 AUTOMATIONS/capital_genesis_ranker.py --rank --report", "priority": 1, "category": "maintenance"},
    # P2: Research / intelligence
    {"name": "edgar", "cmd": "python3 AUTOMATIONS/sec_edgar_scanner.py --scan", "priority": 2, "category": "research"},
    {"name": "crunchbase", "cmd": "python3 AUTOMATIONS/crunchbase_scanner.py --scan", "priority": 2, "category": "research"},
    {"name": "orphan_docs", "cmd": "python3 AUTOMATIONS/orphan_doc_scanner.py --scan", "priority": 2, "category": "research"},
    {"name": "refiner", "cmd": "python3 AUTOMATIONS/user_sim_refiner.py --all", "priority": 2, "category": "research"},
    {"name": "cognitive_engine", "cmd": "python3 AUTOMATIONS/cognitive_engine.py --build-model", "priority": 2, "category": "research"},
]

PYTHON = sys.executable


def log(msg: str, level: str = "INFO") -> None:
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] [USAGE-OPT] [{level}] {msg}"
    print(line)
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(LOG_FILE, "a") as f:
        f.write(line + "\n")


def load_state() -> dict:
    if STATE_FILE.exists():
        try:
            return json.loads(STATE_FILE.read_text())
        except (json.JSONDecodeError, OSError):
            pass
    return {"last_burst": None, "bursts_today": 0, "total_tasks_fired": 0, "history": []}


def save_state(state: dict) -> None:
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(json.dumps(state, indent=2))


def load_queue() -> list:
    """Load burst queue (default tasks + any custom ones)."""
    tasks = list(DEFAULT_BURST_TASKS)
    if QUEUE_FILE.exists():
        try:
            custom = json.loads(QUEUE_FILE.read_text())
            tasks.extend(custom)
        except (json.JSONDecodeError, OSError):
            pass
    return sorted(tasks, key=lambda t: t.get("priority", 99))


def check_usage() -> dict:
    """Check Claude usage via OAuth endpoint or fallback heuristics."""
    result = {
        "window_minutes_remaining": None,
        "usage_percent": None,
        "can_burst": False,
        "method": "unknown",
    }

    # Method 1: Try the OAuth usage endpoint
    try:
        api_key = os.environ.get("ANTHROPIC_API_KEY", "")
        if api_key:
            proc = subprocess.run(
                ["curl", "-s", "-H", f"Authorization: Bearer {api_key}",
                 "https://api.anthropic.com/v1/usage"],
                capture_output=True, text=True, timeout=10
            )
            if proc.returncode == 0 and proc.stdout.strip().startswith("{"):
                data = json.loads(proc.stdout)
                # Parse window info if available
                if "rate_limit" in data or "usage" in data:
                    result["method"] = "api"
                    # Extract whatever fields are available
                    rate = data.get("rate_limit", data.get("usage", {}))
                    if "reset_at" in rate:
                        reset_time = datetime.fromisoformat(rate["reset_at"].replace("Z", "+00:00"))
                        remaining = (reset_time - datetime.now().astimezone()).total_seconds() / 60
                        result["window_minutes_remaining"] = max(0, remaining)
                    if "used" in rate and "limit" in rate:
                        result["usage_percent"] = (rate["used"] / rate["limit"]) * 100
    except Exception:
        pass

    # Method 2: Time-based heuristic (5h windows from first use today)
    if result["window_minutes_remaining"] is None:
        state = load_state()
        result["method"] = "heuristic"

        # Estimate based on when we last saw activity
        last_burst = state.get("last_burst")
        if last_burst:
            last_time = datetime.fromisoformat(last_burst)
            # 5h window from last burst
            window_end = last_time + timedelta(hours=5)
            remaining = (window_end - datetime.now()).total_seconds() / 60
            result["window_minutes_remaining"] = max(0, remaining)
        else:
            # No history — assume we're mid-window, check every 15 min anyway
            result["window_minutes_remaining"] = 150  # middle of window guess

    # Determine if we should burst
    mins = result.get("window_minutes_remaining") or 999
    usage = result.get("usage_percent") or 50  # conservative default
    result["can_burst"] = mins <= 30 and usage < 80

    return result


def fire_burst(dry_run: bool = False) -> dict:
    """Fire all queued tasks during burst window."""
    tasks = load_queue()
    state = load_state()
    fired = 0
    results = []

    log(f"BURST MODE: Firing {len(tasks)} queued tasks")

    for task in tasks:
        name = task["name"]
        cmd = task["cmd"]
        category = task.get("category", "unknown")

        if dry_run:
            log(f"  [DRY RUN] Would fire: {name} ({category})")
            results.append({"name": name, "status": "dry_run"})
            continue

        log(f"  Firing: {name} ({category})")
        try:
            proc = subprocess.Popen(
                cmd, shell=True, cwd=str(PROJECT),
                stdout=subprocess.PIPE, stderr=subprocess.PIPE
            )
            # Don't wait for completion — fire and forget for burst mode
            results.append({"name": name, "status": "fired", "pid": proc.pid})
            fired += 1
        except Exception as e:
            log(f"  FAIL: {name}: {e}", "ERROR")
            results.append({"name": name, "status": "error", "error": str(e)})

    # Update state
    state["last_burst"] = datetime.now().isoformat()
    state["bursts_today"] = state.get("bursts_today", 0) + 1
    state["total_tasks_fired"] = state.get("total_tasks_fired", 0) + fired
    state["history"] = (state.get("history", []) + [{
        "ts": datetime.now().isoformat(),
        "tasks_fired": fired,
        "results": results[:5],  # keep last 5 for brevity
    }])[-20:]  # keep last 20 bursts
    save_state(state)

    log(f"BURST COMPLETE: {fired}/{len(tasks)} tasks fired")
    return {"fired": fired, "total": len(tasks), "results": results}


def optimize() -> None:
    """Main optimization loop — check usage, burst if window ending."""
    usage = check_usage()
    mins = usage.get("window_minutes_remaining")
    pct = usage.get("usage_percent")

    log(f"Usage check: {mins:.0f} min remaining, ~{pct:.0f}% used (method: {usage['method']})" if mins and pct else f"Usage check: method={usage['method']}")

    if usage["can_burst"]:
        log("Window ending soon with unused capacity — triggering burst!")
        fire_burst()
    else:
        if mins is not None and mins > 30:
            log(f"Window has {mins:.0f} min remaining — no burst needed")
        elif pct is not None and pct >= 80:
            log(f"Already at {pct:.0f}% usage — no burst needed")
        else:
            log("Conditions not met for burst")


def show_status() -> None:
    state = load_state()
    usage = check_usage()

    print("=== Usage Optimizer Status ===")
    print(f"  Method: {usage['method']}")
    print(f"  Window remaining: {usage.get('window_minutes_remaining', '?'):.0f} min" if usage.get('window_minutes_remaining') else "  Window remaining: unknown")
    print(f"  Usage: ~{usage.get('usage_percent', '?'):.0f}%" if usage.get('usage_percent') else "  Usage: unknown")
    print(f"  Can burst: {usage['can_burst']}")
    print(f"  Last burst: {state.get('last_burst', 'never')}")
    print(f"  Bursts today: {state.get('bursts_today', 0)}")
    print(f"  Total tasks fired: {state.get('total_tasks_fired', 0)}")
    print(f"  Queue size: {len(load_queue())} tasks")

    history = state.get("history", [])
    if history:
        print("\n  Recent bursts:")
        for h in history[-5:]:
            print(f"    [{h['ts'][:16]}] {h['tasks_fired']} tasks fired")


def show_queue() -> None:
    tasks = load_queue()
    print("=== Burst Queue ===")
    for t in tasks:
        print(f"  P{t.get('priority', '?')} [{t.get('category', '?'):12s}] {t['name']:20s} | {t['cmd'][:60]}")


def add_task(task_str: str) -> None:
    """Add a custom task to the burst queue."""
    QUEUE_FILE.parent.mkdir(parents=True, exist_ok=True)
    custom = []
    if QUEUE_FILE.exists():
        try:
            custom = json.loads(QUEUE_FILE.read_text())
        except (json.JSONDecodeError, OSError):
            pass
    custom.append({"name": f"custom_{len(custom)}", "cmd": task_str, "priority": 1, "category": "custom"})
    QUEUE_FILE.write_text(json.dumps(custom, indent=2))
    print(f"Added to burst queue: {task_str}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Usage Optimizer — maximize Claude subscription utilization")
    parser.add_argument("--check", action="store_true", help="Check current usage window")
    parser.add_argument("--optimize", action="store_true", help="Fire tasks if window ending")
    parser.add_argument("--status", action="store_true", help="Show optimization history")
    parser.add_argument("--queue", action="store_true", help="Show queued tasks")
    parser.add_argument("--add", type=str, help="Add task to burst queue")
    parser.add_argument("--burst", action="store_true", help="Force burst NOW (ignore window)")
    parser.add_argument("--dry-run", action="store_true", help="Show what would fire without doing it")

    args = parser.parse_args()

    if args.status:
        show_status()
    elif args.queue:
        show_queue()
    elif args.add:
        add_task(args.add)
    elif args.check:
        usage = check_usage()
        print(json.dumps(usage, indent=2))
    elif args.burst:
        fire_burst(dry_run=args.dry_run)
    elif args.optimize:
        optimize()
    else:
        parser.print_help()
