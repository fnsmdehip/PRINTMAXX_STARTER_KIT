#!/usr/bin/env python3
"""
PRINTMAXX Scheduled Runs Manager
==================================
Central manager for all scheduled agent runs, cron jobs, and CLI automations.
Provides API for the webapp + perpetual self-improvement loop.

Features:
  - Lists all active cron jobs with status/last-run/next-run
  - Manages scheduled Claude agent sessions
  - Creates new scheduled runs based on output analysis
  - Perpetual improvement: analyzes run outputs, creates follow-up runs
  - Logical guardrails: max runs/day, cooldown periods, disk guards

Usage:
  python3 scheduled_runs_manager.py --status          # all scheduled runs
  python3 scheduled_runs_manager.py --history          # recent run history
  python3 scheduled_runs_manager.py --create SPEC      # create new scheduled run
  python3 scheduled_runs_manager.py --analyze          # analyze outputs, suggest new runs
  python3 scheduled_runs_manager.py --perpetual        # run perpetual improvement cycle
  python3 scheduled_runs_manager.py --api-json         # JSON for webapp API
"""

import json
import os
import re
import csv
import subprocess
import sys
from pathlib import Path
from datetime import datetime, timedelta

BASE = Path(__file__).resolve().parent.parent
AUTO = BASE / "AUTOMATIONS"
OPS = BASE / "OPS"
LEDGER = BASE / "LEDGER"
LOGS = AUTO / "logs"
RUNS_DIR = OPS / "scheduled_runs"
RUNS_DIR.mkdir(parents=True, exist_ok=True)
HISTORY_FILE = RUNS_DIR / "run_history.jsonl"
SCHEDULED_FILE = RUNS_DIR / "scheduled_runs.json"

# Guardrails
MAX_RUNS_PER_DAY = 20
MIN_COOLDOWN_MINUTES = 5
MAX_DISK_USAGE_PERCENT = 98
MAX_NEW_RUNS_PER_CYCLE = 3


def get_cron_jobs():
    """Parse current crontab and return structured job list."""
    try:
        result = subprocess.run(["crontab", "-l"], capture_output=True, text=True, timeout=5)
        if result.returncode != 0:
            return []
    except Exception:
        return []

    jobs = []
    for line in result.stdout.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("SHELL=") or line.startswith("PATH=") or line.startswith("BASE=") or line.startswith("PYTHON="):
            continue

        # Parse cron expression
        parts = line.split(None, 5)
        if len(parts) < 6:
            continue

        schedule = " ".join(parts[:5])
        command = parts[5]

        # Extract script name
        script_match = re.search(r'(?:python3?|bash|/bin/bash)\s+(?:\$PYTHON\s+)?(?:AUTOMATIONS/|scripts/)?(\S+\.(?:py|sh))', command)
        script_name = script_match.group(1) if script_match else command[:60]

        # Extract log file
        log_match = re.search(r'>>\s*(\S+)', command)
        log_file = log_match.group(1) if log_match else None

        # Check last run from log
        last_run = None
        last_status = "UNKNOWN"
        if log_file:
            log_path = BASE / log_file if not log_file.startswith("/") else Path(log_file)
            if log_path.exists():
                try:
                    stat = log_path.stat()
                    last_run = datetime.fromtimestamp(stat.st_mtime).isoformat()
                    # Check last few lines for errors
                    with open(log_path, "rb") as f:
                        f.seek(max(0, stat.st_size - 2000))
                        tail = f.read().decode("utf-8", errors="replace")
                    if "error" in tail.lower() or "traceback" in tail.lower():
                        last_status = "ERROR"
                    elif "complete" in tail.lower() or "done" in tail.lower() or "saved" in tail.lower():
                        last_status = "OK"
                    else:
                        last_status = "RAN"
                except Exception:
                    pass

        # Determine frequency
        freq = parse_cron_frequency(schedule)

        jobs.append({
            "schedule": schedule,
            "script": script_name,
            "command": command[:120],
            "log_file": log_file,
            "last_run": last_run,
            "last_status": last_status,
            "frequency": freq,
            "type": "cron",
        })

    return jobs


def parse_cron_frequency(schedule):
    """Convert cron schedule to human-readable frequency."""
    parts = schedule.split()
    if len(parts) != 5:
        return schedule

    minute, hour, dom, month, dow = parts

    if minute.startswith("*/") and hour == "*":
        return f"Every {minute[2:]} minutes"
    if hour.startswith("*/"):
        return f"Every {hour[2:]} hours"
    if dow == "1" and dom == "*":
        return f"Weekly (Mon {hour}:{minute.zfill(2)})"
    if dow == "0" and dom == "*":
        return f"Weekly (Sun {hour}:{minute.zfill(2)})"
    if dom == "*" and month == "*" and dow == "*":
        return f"Daily at {hour}:{minute.zfill(2)}"
    if minute == "*/30" and hour == "0-8":
        return "Every 30min midnight-8AM"

    return schedule


def get_claude_sessions():
    """Get scheduled Claude agent sessions from schedule_claude.sh config."""
    sessions = []
    schedule_sh = AUTO / "schedule_claude.sh"
    if not schedule_sh.exists():
        return sessions

    # Check cron for claude sessions
    try:
        result = subprocess.run(["crontab", "-l"], capture_output=True, text=True, timeout=5)
        for line in result.stdout.splitlines():
            if "schedule_claude" in line and not line.strip().startswith("#"):
                parts = line.strip().split(None, 5)
                if len(parts) >= 6:
                    schedule = " ".join(parts[:5])
                    # Extract session type
                    type_match = re.search(r'(morning|midday|evening)', line)
                    session_type = type_match.group(1) if type_match else "unknown"
                    sessions.append({
                        "schedule": schedule,
                        "script": f"schedule_claude.sh {session_type}",
                        "type": "claude_session",
                        "session_type": session_type,
                        "frequency": parse_cron_frequency(schedule),
                        "last_run": None,
                        "last_status": "UNKNOWN",
                    })
    except Exception:
        pass

    # Check session logs
    session_logs = sorted(LOGS.glob("sessions/*.log"), key=lambda p: p.stat().st_mtime, reverse=True)
    for log in session_logs[:5]:
        for s in sessions:
            if s["session_type"] in log.name:
                s["last_run"] = datetime.fromtimestamp(log.stat().st_mtime).isoformat()
                try:
                    content = log.read_text(errors="replace")[-500:]
                    if "error" in content.lower():
                        s["last_status"] = "ERROR"
                    else:
                        s["last_status"] = "OK"
                except Exception:
                    pass
                break

    return sessions


def get_custom_scheduled_runs():
    """Get custom scheduled runs created by the perpetual improvement system."""
    if not SCHEDULED_FILE.exists():
        return []
    try:
        return json.loads(SCHEDULED_FILE.read_text())
    except Exception:
        return []


def save_custom_runs(runs):
    """Save custom scheduled runs."""
    SCHEDULED_FILE.write_text(json.dumps(runs, indent=2))


def get_run_history(limit=50):
    """Get recent run history from JSONL file."""
    if not HISTORY_FILE.exists():
        return []
    entries = []
    try:
        for line in HISTORY_FILE.read_text().splitlines():
            if line.strip():
                try:
                    entries.append(json.loads(line))
                except json.JSONDecodeError:
                    pass
    except Exception:
        pass
    return entries[-limit:]


def log_run(entry):
    """Append a run to history."""
    entry["timestamp"] = datetime.now().isoformat()
    with open(HISTORY_FILE, "a") as f:
        f.write(json.dumps(entry) + "\n")


def check_guardrails():
    """Check if we're within guardrail limits."""
    issues = []

    # Check disk usage
    try:
        stat = os.statvfs(str(BASE))
        usage_pct = round((1 - stat.f_bavail / stat.f_blocks) * 100, 1)
        if usage_pct > MAX_DISK_USAGE_PERCENT:
            issues.append(f"Disk usage {usage_pct}% exceeds {MAX_DISK_USAGE_PERCENT}% limit")
    except Exception:
        pass

    # Check runs today
    today = datetime.now().strftime("%Y-%m-%d")
    history = get_run_history(200)
    today_runs = sum(1 for h in history if h.get("timestamp", "").startswith(today))
    if today_runs >= MAX_RUNS_PER_DAY:
        issues.append(f"Already {today_runs} runs today (max {MAX_RUNS_PER_DAY})")

    # Check cooldown
    if history:
        last = history[-1]
        try:
            last_time = datetime.fromisoformat(last["timestamp"])
            elapsed = (datetime.now() - last_time).total_seconds() / 60
            if elapsed < MIN_COOLDOWN_MINUTES:
                issues.append(f"Cooldown: {MIN_COOLDOWN_MINUTES - elapsed:.0f} min remaining")
        except Exception:
            pass

    return issues


def analyze_outputs():
    """Analyze recent outputs to suggest new scheduled runs."""
    suggestions = []

    # Check ALPHA_STAGING for unprocessed entries
    alpha_path = LEDGER / "ALPHA_STAGING.csv"
    if alpha_path.exists():
        try:
            with open(alpha_path) as f:
                reader = csv.DictReader(f)
                pending = sum(1 for row in reader if row.get("status") == "PENDING_REVIEW")
            if pending > 50:
                suggestions.append({
                    "reason": f"{pending} alpha entries pending review",
                    "action": "Run alpha auto-processor",
                    "command": f"cd {BASE} && python3 AUTOMATIONS/alpha_auto_processor.py --process-new",
                    "priority": "HIGH",
                    "type": "one_time",
                })
        except Exception:
            pass

    # Check for stale logs (scrapers not running)
    scraper_logs = {
        "twitter_alpha_scraper": AUTO / "logs" / "scraper_daily.log",
        "reddit_scraper": AUTO / "logs" / "scraper_daily_reddit.log",
        "unified_alpha_monitor": AUTO / "logs" / "unified_alpha.log",
    }
    for name, log_path in scraper_logs.items():
        if log_path.exists():
            age_hours = (datetime.now().timestamp() - log_path.stat().st_mtime) / 3600
            if age_hours > 48:
                suggestions.append({
                    "reason": f"{name} hasn't run in {age_hours:.0f} hours",
                    "action": f"Re-run {name}",
                    "priority": "MEDIUM",
                    "type": "one_time",
                })

    # Check rebalancer for methods to kill/double down
    rebalancer_log = AUTO / "logs" / "rebalancer_scores.json"
    if rebalancer_log.exists():
        try:
            scores = json.loads(rebalancer_log.read_text())
            kills = [s for s in scores if s.get("action") == "KILL"]
            doubles = [s for s in scores if s.get("action") == "DOUBLE_DOWN"]
            if kills:
                suggestions.append({
                    "reason": f"{len(kills)} methods flagged for KILL",
                    "action": "Review and execute kills via checkpoint_manager",
                    "priority": "HIGH",
                    "type": "review",
                })
            if doubles:
                suggestions.append({
                    "reason": f"{len(doubles)} methods flagged for DOUBLE_DOWN",
                    "action": "Allocate more resources to winning methods",
                    "priority": "HIGH",
                    "type": "review",
                })
        except Exception:
            pass

    # Check content queue
    content_dir = BASE / "OPS" / "CONTENT_QA_QUEUE"
    if content_dir.exists():
        pending_content = list(content_dir.glob("*.md"))
        if len(pending_content) > 20:
            suggestions.append({
                "reason": f"{len(pending_content)} content pieces in QA queue",
                "action": "Run content compliance scanner + batch approve",
                "command": f"cd {BASE} && python3 AUTOMATIONS/compliance_scanner.py --audit-all --save",
                "priority": "MEDIUM",
                "type": "one_time",
            })

    # Check if app name validation is overdue
    name_val_dir = BASE / "MONEY_METHODS" / "APP_FACTORY" / "name_validation"
    if name_val_dir.exists():
        audits = sorted(name_val_dir.glob("audit_*.json"), reverse=True)
        if not audits or (datetime.now().timestamp() - audits[0].stat().st_mtime) > 7 * 86400:
            suggestions.append({
                "reason": "App name audit overdue (>7 days)",
                "action": "Run app name validator audit",
                "command": f"cd {BASE} && python3 AUTOMATIONS/app_name_validator.py --audit",
                "priority": "LOW",
                "type": "one_time",
            })

    return suggestions


def create_scheduled_run(spec):
    """Create a new scheduled run (custom, not cron)."""
    runs = get_custom_scheduled_runs()

    new_run = {
        "id": f"run_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
        "created": datetime.now().isoformat(),
        "command": spec.get("command", ""),
        "description": spec.get("description", ""),
        "schedule": spec.get("schedule", "once"),  # once, daily, weekly, hourly
        "next_run": spec.get("next_run", datetime.now().isoformat()),
        "enabled": True,
        "run_count": 0,
        "last_status": None,
        "source": spec.get("source", "manual"),  # manual, perpetual, analysis
    }

    runs.append(new_run)
    save_custom_runs(runs)
    log_run({"action": "CREATED", "run_id": new_run["id"], "description": new_run["description"]})
    return new_run


def perpetual_improvement_cycle():
    """Run one cycle of the perpetual improvement loop.

    Analyzes system state -> identifies gaps -> creates new runs -> logs results.
    Guardrails prevent runaway creation.
    """
    print("\n" + "=" * 60)
    print("  PERPETUAL IMPROVEMENT CYCLE")
    print("=" * 60)

    # Check guardrails
    issues = check_guardrails()
    if issues:
        print(f"\n  GUARDRAILS BLOCKED:")
        for i in issues:
            print(f"    - {i}")
        return {"status": "BLOCKED", "issues": issues}

    # Analyze outputs
    suggestions = analyze_outputs()
    print(f"\n  Found {len(suggestions)} improvement opportunities:")
    for s in suggestions:
        print(f"    [{s['priority']}] {s['reason']}")
        print(f"      -> {s['action']}")

    # Create new runs (limited by guardrail)
    created = []
    for s in suggestions[:MAX_NEW_RUNS_PER_CYCLE]:
        if s.get("command"):
            run = create_scheduled_run({
                "command": s["command"],
                "description": s["reason"],
                "schedule": "once",
                "source": "perpetual",
            })
            created.append(run)
            print(f"    CREATED: {run['id']} - {s['reason']}")

    log_run({
        "action": "PERPETUAL_CYCLE",
        "suggestions": len(suggestions),
        "created": len(created),
    })

    return {
        "status": "OK",
        "suggestions": suggestions,
        "created": created,
    }


def get_api_json():
    """Return full status as JSON for the webapp API."""
    cron_jobs = get_cron_jobs()
    claude_sessions = get_claude_sessions()
    custom_runs = get_custom_scheduled_runs()
    history = get_run_history(20)
    guardrails = check_guardrails()

    # Categorize cron jobs
    categories = {}
    for job in cron_jobs:
        cat = categorize_job(job["script"])
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(job)

    return {
        "timestamp": datetime.now().isoformat(),
        "summary": {
            "total_cron_jobs": len(cron_jobs),
            "claude_sessions": len(claude_sessions),
            "custom_runs": len(custom_runs),
            "active_custom": sum(1 for r in custom_runs if r.get("enabled")),
            "jobs_ok": sum(1 for j in cron_jobs if j["last_status"] in ("OK", "RAN")),
            "jobs_error": sum(1 for j in cron_jobs if j["last_status"] == "ERROR"),
            "jobs_unknown": sum(1 for j in cron_jobs if j["last_status"] == "UNKNOWN"),
            "guardrail_issues": len(guardrails),
        },
        "categories": categories,
        "claude_sessions": claude_sessions,
        "custom_runs": custom_runs,
        "recent_history": history,
        "guardrails": {
            "ok": len(guardrails) == 0,
            "issues": guardrails,
            "limits": {
                "max_runs_per_day": MAX_RUNS_PER_DAY,
                "min_cooldown_minutes": MIN_COOLDOWN_MINUTES,
                "max_disk_usage_percent": MAX_DISK_USAGE_PERCENT,
            },
        },
    }


def categorize_job(script_name):
    """Categorize a cron job by its script name."""
    s = script_name.lower()
    if any(x in s for x in ["scraper", "twitter", "reddit", "research", "alpha", "monitor", "scanner"]):
        return "Research & Scraping"
    if any(x in s for x in ["brain", "orchestrator", "signal", "rebalancer"]):
        return "Brain & Orchestration"
    if any(x in s for x in ["pipeline", "lead", "email", "outreach", "enrichment"]):
        return "Lead Pipeline"
    if any(x in s for x in ["backup", "guardrails", "health", "memory", "heartbeat"]):
        return "System & Safety"
    if any(x in s for x in ["content", "compliance", "posting", "voice"]):
        return "Content & Compliance"
    if any(x in s for x in ["ecom", "arb", "trend", "product", "venture"]):
        return "Commerce & Trends"
    if any(x in s for x in ["todo", "handoff", "dashboard", "resume"]):
        return "Daily Ops"
    return "Other"


def print_status():
    """Print formatted status to terminal."""
    data = get_api_json()
    s = data["summary"]

    print("\n" + "=" * 70)
    print("  PRINTMAXX SCHEDULED RUNS STATUS")
    print("=" * 70)
    print(f"  Cron Jobs: {s['total_cron_jobs']}  (OK: {s['jobs_ok']}  ERROR: {s['jobs_error']}  UNKNOWN: {s['jobs_unknown']})")
    print(f"  Claude Sessions: {s['claude_sessions']}")
    print(f"  Custom Runs: {s['custom_runs']} ({s['active_custom']} active)")
    gr_text = "OK" if s['guardrail_issues'] == 0 else str(s['guardrail_issues']) + " issues"
    print(f"  Guardrails: {gr_text}")

    print(f"\n  BY CATEGORY:")
    for cat, jobs in sorted(data["categories"].items()):
        ok = sum(1 for j in jobs if j["last_status"] in ("OK", "RAN"))
        err = sum(1 for j in jobs if j["last_status"] == "ERROR")
        print(f"    {cat:30s}  {len(jobs):2d} jobs  ({ok} OK, {err} ERR)")

    if data["claude_sessions"]:
        print(f"\n  CLAUDE AGENT SESSIONS:")
        for cs in data["claude_sessions"]:
            status_icon = {"OK": "+", "ERROR": "!", "UNKNOWN": "?"}.get(cs["last_status"], "?")
            print(f"    [{status_icon}] {cs['script']:30s}  {cs['frequency']}")

    if data["custom_runs"]:
        print(f"\n  CUSTOM SCHEDULED RUNS:")
        for r in data["custom_runs"]:
            enabled = "ON" if r.get("enabled") else "OFF"
            print(f"    [{enabled}] {r['id']}  {r['description'][:50]}")

    if data["guardrails"]["issues"]:
        print(f"\n  GUARDRAIL ISSUES:")
        for issue in data["guardrails"]["issues"]:
            print(f"    ! {issue}")


def main():
    import argparse
    parser = argparse.ArgumentParser(description="PRINTMAXX Scheduled Runs Manager")
    parser.add_argument("--status", action="store_true", help="Show all scheduled runs")
    parser.add_argument("--history", action="store_true", help="Show run history")
    parser.add_argument("--create", metavar="JSON", help="Create new scheduled run (JSON spec)")
    parser.add_argument("--analyze", action="store_true", help="Analyze outputs, suggest new runs")
    parser.add_argument("--perpetual", action="store_true", help="Run perpetual improvement cycle")
    parser.add_argument("--api-json", action="store_true", help="Output JSON for webapp API")
    args = parser.parse_args()

    if args.status:
        print_status()
    elif args.history:
        history = get_run_history()
        for h in history:
            print(f"  {h.get('timestamp', '?'):25s}  {h.get('action', '?'):20s}  {h.get('description', h.get('run_id', ''))[:40]}")
    elif args.create:
        spec = json.loads(args.create)
        run = create_scheduled_run(spec)
        print(f"Created run: {run['id']}")
    elif args.analyze:
        suggestions = analyze_outputs()
        for s in suggestions:
            print(f"  [{s['priority']}] {s['reason']}")
            print(f"    -> {s['action']}")
    elif args.perpetual:
        perpetual_improvement_cycle()
    elif args.api_json:
        print(json.dumps(get_api_json(), indent=2))
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
