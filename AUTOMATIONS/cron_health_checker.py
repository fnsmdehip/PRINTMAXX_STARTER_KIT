#!/usr/bin/env python3
"""
PRINTMAXX Cron Health Checker
Reads crontab_printmaxx.txt, validates each script, checks log freshness,
flags scripts that haven't run in 24h, suggests missing cron entries.

Usage: python3 AUTOMATIONS/cron_health_checker.py
Zero external dependencies.
"""

import os
import re
import sys
from pathlib import Path
from datetime import datetime, timedelta

PROJECT_ROOT = Path(__file__).resolve().parent.parent


def safe_path(target):
    resolved = Path(target).resolve()
    if not str(resolved).startswith(str(PROJECT_ROOT)):
        raise ValueError(f"BLOCKED: {resolved} is outside project root {PROJECT_ROOT}")
    return resolved


def parse_crontab(filepath):
    """Parse crontab file and extract cron entries."""
    fp = safe_path(filepath)
    if not fp.exists():
        print(f"[ERROR] Crontab file not found: {fp}")
        return []

    entries = []
    with open(fp, "r", encoding="utf-8") as f:
        for line_num, line in enumerate(f, 1):
            stripped = line.strip()
            # Skip comments, empty lines, variable assignments
            if not stripped or stripped.startswith("#") or "=" in stripped.split()[0] if stripped.split() else True:
                continue
            # Check if it's a variable assignment like SHELL=/bin/bash
            if re.match(r'^[A-Z_]+=', stripped):
                continue
            # Try to parse as cron entry: min hour dom month dow command
            parts = stripped.split(None, 5)
            if len(parts) >= 6:
                schedule = " ".join(parts[:5])
                command = parts[5]
                # Extract script path from command
                script_match = re.search(r'(?:AUTOMATIONS/[\w/.]+\.(?:py|sh))', command)
                script_name = script_match.group(0) if script_match else None
                # Extract log file
                log_match = re.search(r'>>\s*([\w/.]+\.log)', command)
                log_file = log_match.group(1) if log_match else None
                entries.append({
                    "line": line_num,
                    "schedule": schedule,
                    "command": command,
                    "script": script_name,
                    "log_file": log_file,
                    "raw": stripped,
                })
    return entries


def check_script_exists(script_path):
    """Check if a script exists and is valid Python/Bash."""
    if not script_path:
        return "NO_SCRIPT_FOUND", ""
    full_path = safe_path(PROJECT_ROOT / script_path)
    if not full_path.exists():
        return "MISSING", str(full_path)

    ext = full_path.suffix
    if ext == ".py":
        try:
            with open(full_path, "r", encoding="utf-8", errors="replace") as f:
                source = f.read()
            compile(source, str(full_path), "exec")
            return "VALID_PYTHON", str(full_path)
        except SyntaxError as e:
            return f"SYNTAX_ERROR: {e.msg} line {e.lineno}", str(full_path)
    elif ext == ".sh":
        return "BASH_SCRIPT", str(full_path)
    else:
        return "UNKNOWN_TYPE", str(full_path)


def check_log_freshness(log_path):
    """Check when a log file was last modified."""
    if not log_path:
        return None, "NO_LOG_FILE"
    full_path = safe_path(PROJECT_ROOT / log_path)
    if not full_path.exists():
        return None, "LOG_MISSING"
    try:
        mtime = datetime.fromtimestamp(full_path.stat().st_mtime)
        age = datetime.now() - mtime
        return mtime, age
    except Exception as e:
        return None, f"ERROR: {e}"


def find_uncronned_scripts():
    """Find automation scripts not in crontab."""
    automations_dir = safe_path(PROJECT_ROOT / "AUTOMATIONS")
    v2 = safe_path(PROJECT_ROOT / "AUTOMATIONS" / "crontab_printmaxx_v2.txt")
    crontab_path = v2 if v2.exists() else safe_path(PROJECT_ROOT / "AUTOMATIONS" / "crontab_printmaxx.txt")

    # Read crontab to find referenced scripts
    cronned_scripts = set()
    if crontab_path.exists():
        with open(crontab_path, "r", encoding="utf-8") as f:
            content = f.read()
        for match in re.finditer(r'AUTOMATIONS/([\w.]+\.py)', content):
            cronned_scripts.add(match.group(1))

    # Find all automation scripts
    all_scripts = set()
    for f in automations_dir.glob("*.py"):
        all_scripts.add(f.name)

    # Scripts that look like they should be cronned
    cron_candidates = set()
    cron_keywords = ["daily", "scraper", "scanner", "monitor", "tracker", "pipeline",
                     "scheduler", "runner", "engine", "radar", "intelligence",
                     "optimizer", "checker", "health"]
    for s in all_scripts - cronned_scripts:
        name_lower = s.lower()
        if any(kw in name_lower for kw in cron_keywords):
            cron_candidates.add(s)

    return sorted(cron_candidates)


def render_report(entries):
    """Render the health check report."""
    width = 80
    now = datetime.now()
    cutoff_24h = now - timedelta(hours=24)

    def line(text=""):
        print(f"  {text}")

    print("=" * width)
    print("  PRINTMAXX CRON HEALTH CHECKER")
    print(f"  Generated: {now.strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * width)
    print()

    # Per-entry checks
    total = len(entries)
    valid = 0
    missing = 0
    stale = 0
    syntax_errors = 0
    no_log = 0

    print(f"  Found {total} cron entries in crontab_printmaxx.txt")
    print("-" * width)

    for entry in entries:
        script_status, script_full = check_script_exists(entry["script"])
        log_mtime, log_age = check_log_freshness(entry["log_file"])

        # Determine overall status
        if "MISSING" in script_status:
            status_icon = "[MISSING]"
            missing += 1
        elif "SYNTAX_ERROR" in script_status:
            status_icon = "[BROKEN] "
            syntax_errors += 1
        elif "NO_SCRIPT" in script_status:
            status_icon = "[??????] "
        else:
            status_icon = "[  OK  ] "
            valid += 1

        # Log freshness
        if log_mtime is None:
            log_str = f"Log: {log_age}"
            if entry["log_file"]:
                no_log += 1
        else:
            age_hours = log_age.total_seconds() / 3600
            if age_hours > 24:
                log_str = f"Log: STALE ({age_hours:.0f}h ago) - {log_mtime.strftime('%m/%d %H:%M')}"
                stale += 1
            else:
                log_str = f"Log: Fresh ({age_hours:.1f}h ago) - {log_mtime.strftime('%m/%d %H:%M')}"

        script_display = entry["script"] or "???"
        print(f"  {status_icon} {script_display}")
        print(f"             Schedule: {entry['schedule']}")
        print(f"             Status:   {script_status}")
        print(f"             {log_str}")
        print()

    # Summary
    print("=" * width)
    print("  SUMMARY")
    print("-" * width)
    print(f"  Total cron entries:     {total}")
    print(f"  Scripts valid:          {valid}")
    print(f"  Scripts MISSING:        {missing}")
    print(f"  Scripts SYNTAX ERROR:   {syntax_errors}")
    print(f"  Logs stale (>24h):      {stale}")
    print(f"  Logs missing:           {no_log}")
    print()

    # Stale warnings
    if stale > 0:
        print("=" * width)
        print("  STALE LOG WARNINGS (scripts that haven't run in 24h)")
        print("-" * width)
        for entry in entries:
            log_mtime, log_age = check_log_freshness(entry["log_file"])
            if log_mtime and log_age.total_seconds() / 3600 > 24:
                age_h = log_age.total_seconds() / 3600
                print(f"  [!] {entry['script'] or '???'} -- last ran {age_h:.0f}h ago")
        print()

    # Missing script suggestions
    uncronned = find_uncronned_scripts()
    if uncronned:
        print("=" * width)
        print("  SUGGESTED CRON ADDITIONS (scripts not in crontab)")
        print("-" * width)
        suggested_times = [
            ("0 5 * * *", "5:00 AM daily"),
            ("30 5 * * *", "5:30 AM daily"),
            ("0 6 * * *", "6:00 AM daily"),
            ("30 6 * * *", "6:30 AM daily"),
            ("0 7 * * *", "7:00 AM daily"),
            ("30 7 * * *", "7:30 AM daily"),
            ("0 8 * * *", "8:00 AM daily"),
            ("30 8 * * *", "8:30 AM daily"),
        ]
        for i, script in enumerate(uncronned[:15]):
            sched, desc = suggested_times[i % len(suggested_times)]
            log_name = script.replace(".py", ".log")
            print(f"  # {script} ({desc})")
            print(f"  {sched} cd $BASE && $PYTHON AUTOMATIONS/{script} >> AUTOMATIONS/logs/{log_name} 2>&1")
            print()
        print(f"  ... {len(uncronned)} total scripts could be added to cron")
    print()
    print("=" * width)
    print("  DONE. Run `crontab -l` to see active system crontab.")
    print("=" * width)


def main():
    v2 = PROJECT_ROOT / "AUTOMATIONS" / "crontab_printmaxx_v2.txt"
    crontab_path = v2 if v2.exists() else PROJECT_ROOT / "AUTOMATIONS" / "crontab_printmaxx.txt"
    entries = parse_crontab(crontab_path)
    render_report(entries)


if __name__ == "__main__":
    main()
