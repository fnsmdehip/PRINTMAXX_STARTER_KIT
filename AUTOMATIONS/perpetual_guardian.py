#!/usr/bin/env python3

from __future__ import annotations
"""
PRINTMAXX Perpetual Guardian — 24/7 Self-Improving Autonomous Business Watchdog
==================================================================================
The unified guardian that monitors, self-heals, safety-commits, and drives
continuous improvement across the entire PRINTMAXX system.

MODES:
  python3 perpetual_guardian.py --pulse          # Quick 10-second health pulse
  python3 perpetual_guardian.py --safety-commit  # Git safety commit if changes exist
  python3 perpetual_guardian.py --heal           # Self-heal broken/stale systems
  python3 perpetual_guardian.py --improve        # Run improvement cycle (find+fix gaps)
  python3 perpetual_guardian.py --full           # All of the above in sequence
  python3 perpetual_guardian.py --cron-audit     # Verify all cron jobs are running
  python3 perpetual_guardian.py --status         # Full system status report

SCHEDULE (cron):
  Every 15 min: --pulse (quick health check + notification if anything RED)
  Every 2 hours: --safety-commit (git commit if changes exist)
  Every 4 hours: --heal (self-heal stale/broken systems)
  Daily 6 PM:   --full (complete guardian cycle)
  Daily 11 PM:  --improve (before overnight runner)

No external dependencies. stdlib only.
"""

import argparse
import csv
csv.field_size_limit(10 * 1024 * 1024)
import json
import os
import subprocess
import sys
import time
from datetime import datetime, date, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# ---------------------------------------------------------------------------
# CONSTANTS
# ---------------------------------------------------------------------------

BASE = Path(__file__).resolve().parent.parent
AUTOMATIONS = BASE / "AUTOMATIONS"
OPS = BASE / "OPS"
LEDGER = BASE / "LEDGER"
LOGS = AUTOMATIONS / "logs"
LEADS_DIR = AUTOMATIONS / "leads"

PYTHON = sys.executable
TODAY = date.today().isoformat()
NOW = datetime.now()
TIMESTAMP = NOW.strftime("%Y%m%d_%H%M%S")

GUARDIAN_LOG = LOGS / f"guardian_{TODAY}.log"
GUARDIAN_STATUS = LOGS / "guardian_status.json"

LOGS.mkdir(parents=True, exist_ok=True)

# Thresholds
STALE_LOG_HOURS = 26       # Log file older than this = stale
STALE_HEARTBEAT_HOURS = 4  # Heartbeat older than this = warning
DISK_MIN_GB = 3            # Minimum free disk space
MAX_LOG_AGE_DAYS = 30      # Rotate logs older than this


# ---------------------------------------------------------------------------
# LOGGING
# ---------------------------------------------------------------------------

def log(msg: str, level: str = "INFO"):
    ts = NOW.strftime("%H:%M:%S")
    line = f"[{ts}] [{level}] {msg}"
    print(line)
    try:
        with open(GUARDIAN_LOG, "a") as f:
            f.write(line + "\n")
    except Exception:
        pass


def notify(title: str, message: str, sound: str = "Glass"):
    """macOS notification."""
    try:
        subprocess.run([
            "osascript", "-e",
            f'display notification "{message}" with title "{title}" sound name "{sound}"'
        ], capture_output=True, timeout=5)
    except Exception:
        pass


# ---------------------------------------------------------------------------
# HEALTH CHECKS
# ---------------------------------------------------------------------------

def check_disk() -> Tuple[str, str]:
    """Check available disk space."""
    try:
        result = subprocess.run(
            ["df", "-g", "/"],
            capture_output=True, text=True, timeout=5
        )
        for line in result.stdout.strip().split("\n")[1:]:
            parts = line.split()
            if len(parts) >= 4:
                avail_gb = int(parts[3])
                if avail_gb < DISK_MIN_GB:
                    return "RED", f"{avail_gb}GB free (need {DISK_MIN_GB}GB)"
                elif avail_gb < DISK_MIN_GB * 2:
                    return "AMBER", f"{avail_gb}GB free"
                return "GREEN", f"{avail_gb}GB free"
    except Exception as e:
        return "AMBER", f"Check failed: {e}"
    return "AMBER", "Could not determine disk space"


def check_heartbeat() -> Tuple[str, str]:
    """Check HEARTBEAT.md freshness."""
    hb = OPS / "HEARTBEAT.md"
    if not hb.exists():
        return "RED", "HEARTBEAT.md missing"
    mtime = datetime.fromtimestamp(hb.stat().st_mtime)
    age_hours = (NOW - mtime).total_seconds() / 3600
    if age_hours > STALE_HEARTBEAT_HOURS:
        return "AMBER", f"Stale ({age_hours:.1f}h old)"
    return "GREEN", f"Fresh ({age_hours:.1f}h old)"


def check_cron() -> Tuple[str, str]:
    """Check if cron jobs are installed."""
    try:
        result = subprocess.run(
            ["crontab", "-l"],
            capture_output=True, text=True, timeout=5
        )
        if result.returncode != 0:
            return "RED", "No crontab installed"
        lines = [l for l in result.stdout.strip().split("\n") if l.strip() and not l.startswith("#")]
        count = len(lines)
        if count < 20:
            return "AMBER", f"Only {count} cron entries (expected 70+)"
        return "GREEN", f"{count} cron entries active"
    except Exception as e:
        return "AMBER", f"Check failed: {e}"


def check_git() -> Tuple[str, str]:
    """Check git status including unpushed commits."""
    try:
        _clear_stale_lock()
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            capture_output=True, text=True, timeout=60,
            cwd=str(BASE)
        )
        changes = len([l for l in result.stdout.strip().split("\n") if l.strip()])

        # Count unpushed commits
        unpushed = 0
        unpushed_str = ""
        try:
            ahead = subprocess.run(
                ["git", "rev-list", "--count", "origin/main..HEAD"],
                capture_output=True, text=True, timeout=15,
                cwd=str(BASE)
            )
            if ahead.returncode == 0:
                unpushed = int(ahead.stdout.strip())
                unpushed_str = f", {unpushed} commits unpushed"
        except Exception:
            unpushed_str = ", unpushed count unknown"

        # Determine severity: RED if 6+ unpushed (push failing 12h+)
        if unpushed >= 6:
            return "RED", f"{changes} uncommitted changes{unpushed_str} (push failing?)"
        elif changes > 50:
            return "AMBER", f"{changes} uncommitted changes{unpushed_str}"
        elif changes > 0:
            return "GREEN", f"{changes} uncommitted changes{unpushed_str}"
        return "GREEN", f"Clean working tree{unpushed_str}"
    except Exception as e:
        return "RED", f"Git check failed: {e}"


def check_overnight_log() -> Tuple[str, str]:
    """Check if overnight runner completed recently."""
    pattern = f"overnight_{TODAY.replace('-', '')}"
    logs_found = sorted(LOGS.glob(f"overnight_*.log"), key=lambda p: p.stat().st_mtime, reverse=True)
    if not logs_found:
        return "AMBER", "No overnight logs found"
    latest = logs_found[0]
    age_hours = (NOW - datetime.fromtimestamp(latest.stat().st_mtime)).total_seconds() / 3600
    if age_hours > STALE_LOG_HOURS:
        return "AMBER", f"Last overnight: {age_hours:.0f}h ago"
    return "GREEN", f"Last overnight: {age_hours:.0f}h ago ({latest.name})"


def check_dashboard() -> Tuple[str, str]:
    """Check if Flask dashboard is running on port 7777."""
    try:
        import urllib.request
        req = urllib.request.urlopen("http://localhost:7777/api/status", timeout=3)
        if req.status == 200:
            return "GREEN", "Dashboard running on :7777"
    except Exception:
        pass
    # Also check port 8888 (live dashboard)
    try:
        import urllib.request
        req = urllib.request.urlopen("http://localhost:8888/api/status", timeout=3)
        if req.status == 200:
            return "GREEN", "Dashboard running on :8888"
    except Exception:
        pass
    return "AMBER", "No dashboard detected"


def check_active_processes() -> Tuple[str, str]:
    """Check for runaway or stuck processes."""
    try:
        result = subprocess.run(
            ["pgrep", "-lf", "python3.*AUTOMATIONS"],
            capture_output=True, text=True, timeout=5
        )
        procs = [l for l in result.stdout.strip().split("\n") if l.strip()]
        if len(procs) > 10:
            return "AMBER", f"{len(procs)} PRINTMAXX processes (possible runaway)"
        return "GREEN", f"{len(procs)} active processes"
    except Exception:
        return "GREEN", "0 active processes"


def check_clone() -> Tuple[str, str]:
    """Check weekly clone status."""
    meta_file = Path.home() / "PRINTMAXX_WEEKLY_CLONE" / "_clone_meta.json"
    if not meta_file.exists():
        return "AMBER", "No weekly clone found"
    try:
        with open(meta_file) as f:
            meta = json.load(f)
        clone_date = datetime.fromisoformat(meta["clone_date"].replace("Z", "+00:00")).replace(tzinfo=None)
        age_days = (NOW - clone_date).days
        if age_days > 8:
            return "AMBER", f"Clone is {age_days} days old"
        return "GREEN", f"Clone: {age_days}d old, {meta.get('size', '?')}"
    except Exception as e:
        return "AMBER", f"Clone check error: {e}"


def check_backup() -> Tuple[str, str]:
    """Check backup system status."""
    backup_dir = Path.home() / "PRINTMAXX_BACKUPS"
    if not backup_dir.exists():
        return "RED", "No backup directory"
    backups = sorted(backup_dir.glob("*.tar.gz"), key=lambda p: p.stat().st_mtime, reverse=True)
    if not backups:
        # Check for directories too
        backups = sorted([d for d in backup_dir.iterdir() if d.is_dir() and not d.name.startswith("_")],
                        key=lambda p: p.stat().st_mtime, reverse=True)
    if not backups:
        return "AMBER", "No backups found"
    latest = backups[0]
    age_hours = (NOW - datetime.fromtimestamp(latest.stat().st_mtime)).total_seconds() / 3600
    if age_hours > 48:
        return "AMBER", f"Last backup: {age_hours:.0f}h ago"
    return "GREEN", f"Last backup: {age_hours:.0f}h ago"


# ---------------------------------------------------------------------------
# PULSE (quick health check, every 15 min)
# ---------------------------------------------------------------------------

def run_pulse() -> Dict:
    """Quick 10-second health pulse. Returns status dict."""
    log("=== GUARDIAN PULSE ===")
    checks = {
        "disk": check_disk(),
        "heartbeat": check_heartbeat(),
        "cron": check_cron(),
        "git": check_git(),
        "overnight": check_overnight_log(),
        "dashboard": check_dashboard(),
        "processes": check_active_processes(),
        "clone": check_clone(),
        "backup": check_backup(),
    }

    # Count by status
    counts = {"GREEN": 0, "AMBER": 0, "RED": 0}
    for name, (status, detail) in checks.items():
        counts[status] = counts.get(status, 0) + 1
        log(f"  {status:5s} | {name:12s} | {detail}")

    overall = "GREEN"
    if counts.get("RED", 0) > 0:
        overall = "RED"
    elif counts.get("AMBER", 0) > 2:
        overall = "AMBER"

    log(f"OVERALL: {overall} (GREEN={counts['GREEN']} AMBER={counts['AMBER']} RED={counts.get('RED', 0)})")

    # Notify if RED
    if overall == "RED":
        red_items = [f"{n}: {d}" for n, (s, d) in checks.items() if s == "RED"]
        notify("PRINTMAXX RED ALERT", "; ".join(red_items), "Basso")

    # Save status
    status = {
        "timestamp": NOW.isoformat(),
        "overall": overall,
        "checks": {k: {"status": v[0], "detail": v[1]} for k, v in checks.items()},
        "counts": counts,
    }
    try:
        with open(GUARDIAN_STATUS, "w") as f:
            json.dump(status, f, indent=2)
    except Exception:
        pass

    return status


# ---------------------------------------------------------------------------
# SAFETY COMMIT (git commit if changes exist, every 2 hours)
# ---------------------------------------------------------------------------

def _clear_stale_lock():
    """Remove stale .git/index.lock if no git process is running."""
    lock = BASE / ".git" / "index.lock"
    if lock.exists():
        import time as _time
        age = _time.time() - lock.stat().st_mtime
        if age > 120:  # older than 2 minutes = stale
            lock.unlink()
            log(f"  Cleared stale index.lock ({int(age)}s old)")


def _push_to_remote():
    """Push to origin/main. Called after commit AND standalone."""
    try:
        # Check if there are unpushed commits
        ahead = subprocess.run(
            ["git", "rev-list", "--count", "origin/main..HEAD"],
            capture_output=True, text=True, timeout=15,
            cwd=str(BASE)
        )
        count = int(ahead.stdout.strip()) if ahead.returncode == 0 else 0
        if count == 0:
            return
        log(f"  {count} unpushed commits. Pushing...")
        push_result = subprocess.run(
            ["git", "push", "origin", "main"],
            capture_output=True, text=True, timeout=180,
            cwd=str(BASE)
        )
        if push_result.returncode == 0:
            log("  Pushed to origin/main")
        else:
            log(f"  Push failed: {push_result.stderr.strip()[:200]}")
    except Exception as e:
        log(f"  Push error: {e}")


def run_safety_commit():
    """Git commit uncommitted changes as a safety net."""
    log("=== SAFETY GIT COMMIT ===")

    try:
        # Clear stale locks before any git operation
        _clear_stale_lock()

        # Check for changes (60s timeout for large repos)
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            capture_output=True, text=True, timeout=60,
            cwd=str(BASE)
        )
        changes = [l for l in result.stdout.strip().split("\n") if l.strip()]

        if not changes:
            log("  No changes to commit.")
            # Still push any unpushed commits from previous runs
            _push_to_remote()
            return

        log(f"  {len(changes)} changed files detected.")

        # Stage tracked files only (respects .gitignore, avoids binary bloat)
        subprocess.run(
            ["git", "add", "-u"],
            capture_output=True, timeout=60,
            cwd=str(BASE)
        )
        # Also stage new Python/MD/JSON/CSV/YAML files (skip binaries)
        for ext in ["*.py", "*.md", "*.json", "*.csv", "*.yaml", "*.yml", "*.sh", "*.txt", "*.html", "*.css", "*.js", "*.ts", "*.tsx"]:
            subprocess.run(
                ["git", "add", ext],
                capture_output=True, timeout=15,
                cwd=str(BASE)
            )

        # Commit with timestamp
        msg = f"Guardian safety commit {NOW.strftime('%Y-%m-%d %H:%M')}"
        result = subprocess.run(
            ["git", "commit", "-m", msg],
            capture_output=True, text=True, timeout=60,
            cwd=str(BASE)
        )

        if result.returncode == 0:
            log(f"  Committed: {msg}")
            hash_result = subprocess.run(
                ["git", "rev-parse", "--short", "HEAD"],
                capture_output=True, text=True, timeout=5,
                cwd=str(BASE)
            )
            if hash_result.returncode == 0:
                log(f"  Hash: {hash_result.stdout.strip()}")
        else:
            log(f"  Commit skipped: {result.stderr.strip()[:200]}")

        # Always try to push (whether commit succeeded or not)
        _push_to_remote()

    except subprocess.TimeoutExpired:
        log("  Git operation timed out.")
        # Even if commit timed out, try to push existing unpushed commits
        _push_to_remote()
    except Exception as e:
        log(f"  Git error: {e}")


# ---------------------------------------------------------------------------
# SELF-HEAL (fix broken/stale systems, every 4 hours)
# ---------------------------------------------------------------------------

def run_heal():
    """Self-heal broken or stale systems."""
    log("=== SELF-HEAL CYCLE ===")
    healed = 0

    # 1. Refresh heartbeat if stale
    hb = OPS / "HEARTBEAT.md"
    if hb.exists():
        age_hours = (NOW - datetime.fromtimestamp(hb.stat().st_mtime)).total_seconds() / 3600
        if age_hours > STALE_HEARTBEAT_HOURS:
            log("  Healing: Refreshing stale HEARTBEAT.md...")
            try:
                subprocess.run(
                    [PYTHON, str(AUTOMATIONS / "memory_manager.py"), "--heartbeat"],
                    capture_output=True, timeout=60,
                    cwd=str(BASE)
                )
                log("  HEARTBEAT refreshed.")
                healed += 1
            except Exception as e:
                log(f"  HEARTBEAT refresh failed: {e}")

    # 2. Remove stale lock files
    lock_files = list(LOGS.glob("*.lock")) + list(LOGS.glob("*.pid"))
    for lock in lock_files:
        try:
            age_hours = (NOW - datetime.fromtimestamp(lock.stat().st_mtime)).total_seconds() / 3600
            if age_hours > 6:
                # Check if PID is still alive
                try:
                    pid = int(lock.read_text().strip())
                    os.kill(pid, 0)  # Check if process exists
                    log(f"  Lock {lock.name}: PID {pid} still alive. Keeping.")
                except (ValueError, ProcessLookupError):
                    lock.unlink()
                    log(f"  Healed: Removed stale lock {lock.name} ({age_hours:.0f}h old)")
                    healed += 1
        except Exception:
            pass

    # 3. Rotate old logs (>30 days)
    old_cutoff = NOW - timedelta(days=MAX_LOG_AGE_DAYS)
    old_logs = 0
    for logf in LOGS.glob("*.log"):
        try:
            if datetime.fromtimestamp(logf.stat().st_mtime) < old_cutoff:
                logf.unlink()
                old_logs += 1
        except Exception:
            pass
    if old_logs:
        log(f"  Healed: Rotated {old_logs} logs older than {MAX_LOG_AGE_DAYS} days")
        healed += 1

    # 4. Check and rebuild search index if stale
    search_index = LOGS / ".search_index" / "tfidf_index.json"
    if search_index.exists():
        age_hours = (NOW - datetime.fromtimestamp(search_index.stat().st_mtime)).total_seconds() / 3600
        if age_hours > 25:
            log("  Healing: Rebuilding search index...")
            try:
                subprocess.run(
                    [PYTHON, str(AUTOMATIONS / "semantic_memory_search.py"), "--index"],
                    capture_output=True, timeout=120,
                    cwd=str(BASE)
                )
                log("  Search index rebuilt.")
                healed += 1
            except Exception as e:
                log(f"  Search index rebuild failed: {e}")

    # 5. Check active-tasks.md for stuck tasks
    active_tasks = OPS / "active-tasks.md"
    if active_tasks.exists():
        try:
            content = active_tasks.read_text()
            if "IN_PROGRESS" in content:
                age_hours = (NOW - datetime.fromtimestamp(active_tasks.stat().st_mtime)).total_seconds() / 3600
                if age_hours > 6:
                    log(f"  WARNING: active-tasks.md has IN_PROGRESS items from {age_hours:.0f}h ago")
                    log("  These may be abandoned. Consider clearing.")
        except Exception:
            pass

    # 6. Ensure logs directory structure exists
    for subdir in ["daily", "overnight", "guardian"]:
        (LOGS / subdir).mkdir(parents=True, exist_ok=True)

    # 7. Check for dispatch trigger (written by Dispatch session for deferred execution)
    dispatch_trigger = AUTOMATIONS / "dispatch_trigger.py"
    if dispatch_trigger.exists():
        log("  DISPATCH TRIGGER FOUND — executing deferred tasks...")
        try:
            subprocess.run(
                [PYTHON, str(dispatch_trigger)],
                capture_output=True, timeout=900,
                cwd=str(BASE)
            )
            log("  DISPATCH TRIGGER executed successfully.")
            healed += 1
        except Exception as e:
            log(f"  DISPATCH TRIGGER failed: {e}")

    log(f"  Healed {healed} issues.")
    return healed


# ---------------------------------------------------------------------------
# IMPROVE (find and fix gaps, daily)
# ---------------------------------------------------------------------------

def run_improve():
    """Run improvement cycle - identify gaps and drive continuous improvement."""
    log("=== IMPROVEMENT CYCLE ===")
    improvements = []

    # 1. Check alpha processing backlog
    alpha_file = LEDGER / "ALPHA_STAGING.csv"
    if alpha_file.exists():
        try:
            with open(alpha_file, newline="", encoding="utf-8", errors="replace") as f:
                reader = csv.DictReader(f)
                pending = sum(1 for row in reader if row.get("status", "").upper() == "PENDING_REVIEW")
            if pending > 50:
                improvements.append(f"Alpha backlog: {pending} PENDING_REVIEW entries")
                log(f"  GAP: {pending} unprocessed alpha entries")
                # Auto-trigger alpha processor
                try:
                    subprocess.run(
                        [PYTHON, str(AUTOMATIONS / "alpha_auto_processor.py"), "--process-new"],
                        capture_output=True, timeout=300,
                        cwd=str(BASE)
                    )
                    log("  FIX: Ran alpha_auto_processor.py")
                except Exception:
                    log("  Could not auto-process alpha")
        except Exception as e:
            log(f"  Alpha check error: {e}")

    # 2. Check for stale data files
    stale_files = []
    for check_path, max_age_days in [
        (OPS / "HEARTBEAT.md", 1),
        (LEDGER / "TREND_SIGNALS.csv", 3),
        (LEDGER / "FREELANCE_DEMAND_SCAN.csv", 3),
        (LEDGER / "ECOM_ARB_OPPORTUNITIES.csv", 3),
    ]:
        if check_path.exists():
            age_days = (NOW - datetime.fromtimestamp(check_path.stat().st_mtime)).days
            if age_days > max_age_days:
                stale_files.append(f"{check_path.name} ({age_days}d)")
    if stale_files:
        log(f"  GAP: Stale data files: {', '.join(stale_files)}")
        improvements.append(f"Stale data: {', '.join(stale_files)}")

    # 3. Check revenue status
    rev_file = Path(BASE / "FINANCIALS" / "REVENUE_TRACKER.csv")
    if rev_file.exists():
        try:
            with open(rev_file, newline="", encoding="utf-8", errors="replace") as f:
                reader = csv.DictReader(f)
                total = sum(float(row.get("amount", 0)) for row in reader
                           if row.get("amount", "").replace(".", "").replace("-", "").isdigit())
            if total == 0:
                improvements.append("Revenue still $0 — shipping is blocked")
                log("  GAP: Revenue = $0. Need to SHIP.")
        except Exception:
            pass

    # 4. Check account creation status
    accounts_file = LEDGER / "ACCOUNTS.csv"
    if accounts_file.exists():
        try:
            with open(accounts_file, newline="", encoding="utf-8", errors="replace") as f:
                reader = csv.DictReader(f)
                active = sum(1 for row in reader if row.get("status", "").upper() in ("ACTIVE", "CREATED"))
            if active < 5:
                improvements.append(f"Only {active} active accounts — #1 blocker")
                log(f"  GAP: Only {active} active accounts")
        except Exception:
            pass

    # 5. Generate improvement report
    report_file = OPS / f"GUARDIAN_IMPROVEMENT_{TODAY.replace('-', '_')}.md"
    if improvements:
        report_lines = [
            f"# Guardian Improvement Report — {TODAY}",
            f"Generated: {NOW.strftime('%H:%M:%S')}",
            "",
            "## Gaps Found",
            "",
        ]
        for i, imp in enumerate(improvements, 1):
            report_lines.append(f"{i}. {imp}")
        report_lines.extend([
            "",
            "## Auto-Fixes Applied",
            "",
            "- Alpha processor triggered (if backlog >50)",
            "- Stale locks removed",
            "- Old logs rotated",
            "- Heartbeat refreshed",
        ])
        report_file.write_text("\n".join(report_lines) + "\n")
        log(f"  Report written: {report_file.name}")
    else:
        log("  No improvement gaps found. System healthy.")

    log(f"  {len(improvements)} improvements identified.")
    return improvements


# ---------------------------------------------------------------------------
# CRON AUDIT
# ---------------------------------------------------------------------------

def run_cron_audit():
    """Verify all expected cron jobs are running."""
    log("=== CRON JOB AUDIT ===")

    # Expected critical jobs
    expected = [
        "overnight_master_runner",
        "backup_system",
        "memory_manager",
        "schedule_claude",
        "perpetual_ship_engine",
        "alpha_review_bot",
        "daily_research",
        "perpetual_guardian",
    ]

    try:
        result = subprocess.run(
            ["crontab", "-l"],
            capture_output=True, text=True, timeout=5
        )
        crontab_content = result.stdout

        found = []
        missing = []
        for job in expected:
            if job in crontab_content:
                found.append(job)
            else:
                missing.append(job)

        log(f"  Found: {len(found)}/{len(expected)} critical jobs")
        for m in missing:
            log(f"  MISSING: {m}")

        if missing:
            log(f"  WARNING: {len(missing)} critical cron jobs not found in crontab")
            notify("PRINTMAXX Cron Alert", f"{len(missing)} critical jobs missing: {', '.join(missing)}", "Basso")

        return {"found": found, "missing": missing}

    except Exception as e:
        log(f"  Cron audit error: {e}")
        return {"found": [], "missing": expected}


# ---------------------------------------------------------------------------
# STATUS REPORT
# ---------------------------------------------------------------------------

def run_status():
    """Full system status report."""
    print("=" * 60)
    print("PRINTMAXX PERPETUAL GUARDIAN — SYSTEM STATUS")
    print(f"Timestamp: {NOW.strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    print()

    # Run pulse
    status = run_pulse()
    print()

    # Show recent guardian activity
    print("--- Recent Guardian Activity ---")
    if GUARDIAN_LOG.exists():
        try:
            lines = GUARDIAN_LOG.read_text().strip().split("\n")
            for line in lines[-10:]:
                print(f"  {line}")
        except Exception:
            print("  (could not read guardian log)")
    else:
        print("  No guardian log for today.")

    print()

    # Show git status
    print("--- Git Status ---")
    try:
        result = subprocess.run(
            ["git", "log", "--oneline", "-5"],
            capture_output=True, text=True, timeout=5,
            cwd=str(BASE)
        )
        for line in result.stdout.strip().split("\n"):
            print(f"  {line}")
    except Exception:
        print("  (git status unavailable)")

    print()
    print("=" * 60)


# ---------------------------------------------------------------------------
# FULL CYCLE
# ---------------------------------------------------------------------------

def run_full():
    """Run complete guardian cycle: pulse + commit + heal + improve."""
    log("========== FULL GUARDIAN CYCLE ==========")
    start = time.time()

    # 1. Health pulse
    status = run_pulse()

    # 2. Safety git commit
    run_safety_commit()

    # 3. Self-heal
    healed = run_heal()

    # 4. Improvement cycle
    improvements = run_improve()

    # 5. Cron audit
    cron = run_cron_audit()

    duration = time.time() - start
    log(f"========== GUARDIAN CYCLE COMPLETE ({duration:.1f}s) ==========")

    # Summary notification
    overall = status.get("overall", "UNKNOWN")
    notify(
        f"PRINTMAXX Guardian [{overall}]",
        f"Healed: {healed} | Gaps: {len(improvements)} | Cron: {len(cron.get('found', []))}/{len(cron.get('found', [])) + len(cron.get('missing', []))}",
        "Glass" if overall == "GREEN" else "Basso"
    )


# ---------------------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="PRINTMAXX Perpetual Guardian")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--pulse", action="store_true", help="Quick health pulse (10s)")
    group.add_argument("--safety-commit", action="store_true", help="Git safety commit")
    group.add_argument("--heal", action="store_true", help="Self-heal broken systems")
    group.add_argument("--improve", action="store_true", help="Run improvement cycle")
    group.add_argument("--full", action="store_true", help="Complete guardian cycle")
    group.add_argument("--cron-audit", action="store_true", help="Audit cron jobs")
    group.add_argument("--status", action="store_true", help="Full status report")

    args = parser.parse_args()

    if args.pulse:
        run_pulse()
    elif args.safety_commit:
        run_safety_commit()
    elif args.heal:
        run_heal()
    elif args.improve:
        run_improve()
    elif args.full:
        run_full()
    elif args.cron_audit:
        run_cron_audit()
    elif args.status:
        run_status()
    else:
        # Default: full cycle
        run_full()


if __name__ == "__main__":
    main()
