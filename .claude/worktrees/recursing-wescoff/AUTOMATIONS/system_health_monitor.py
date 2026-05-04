#!/usr/bin/env python3

from __future__ import annotations
"""
PRINTMAXX System Health Monitor — 16-point check across all automated systems.

Answers the question: "Is our stuff ACTUALLY running?"

Usage:
    python3 AUTOMATIONS/system_health_monitor.py --check       # Full 16-point health check
    python3 AUTOMATIONS/system_health_monitor.py --quick       # Summary line only
    python3 AUTOMATIONS/system_health_monitor.py --json        # Machine-readable JSON output
    python3 AUTOMATIONS/system_health_monitor.py --skip-sites  # Skip HTTP checks (faster)

Output:
    Writes health report to AUTOMATIONS/logs/system_health_YYYY-MM-DD.json
    Prints human-readable status table to stdout

Severity:
    GREEN  = RUNNING  (fresh within expected window)
    AMBER  = STALE    (>24h since last update, or degraded)
    RED    = DEAD     (>48h since last update, missing, or broken)

Safety:
    - Uses Path(__file__).resolve().parent.parent as PROJECT_ROOT
    - All file operations stay within the project folder
    - Read-only: never modifies project files (only writes its own health report to logs/)
    - Exit codes: 0=healthy, 1=degraded, 2=critical
"""

import argparse
import csv
import json
import os
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path

# ---------------------------------------------------------------------------
# Project paths — all relative to the repo root via __file__
# ---------------------------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parent.parent

AUTOMATIONS    = PROJECT_ROOT / "AUTOMATIONS"
LEDGER         = PROJECT_ROOT / "LEDGER"
OPS            = PROJECT_ROOT / "OPS"
LOGS           = AUTOMATIONS / "logs"
LEADS          = AUTOMATIONS / "leads"
LEADS_QUAL     = LEADS / "qualified"
OUTREACH       = AUTOMATIONS / "outreach"
OUTPUT         = PROJECT_ROOT / "output"
DAILY_LOGS     = LOGS / "daily"
CONTENT        = PROJECT_ROOT / "CONTENT"

# Thresholds (hours)
AMBER_H = 24
RED_H   = 48

# All 16 live surge.sh sites from the deploy log
LIVE_SITES = [
    "https://printmaxx-seo.surge.sh",
    "https://ramadan-tracker.surge.sh",
    "https://focuslock-app.surge.sh",
    "https://habitforge-app.surge.sh",
    "https://mealmaxx-app.surge.sh",
    "https://sleepmaxx-app.surge.sh",
    "https://walktounlock-app.surge.sh",
    "https://dental-demo.surge.sh",
    "https://restaurant-site-demo.surge.sh",
    "https://fitness-demo.surge.sh",
    "https://legal-demo.surge.sh",
    "https://plumber-demo.surge.sh",
    "https://realtor-demo.surge.sh",
    "https://dental-motion.surge.sh",
    "https://realtor-motion.surge.sh",
    "https://restaurant-motion.surge.sh",
]

# Key crontab markers that prove the right crontab is installed
CRON_MARKERS = [
    "morning_intelligence_dag",
    "capital_genesis_ranker",
    "decision_engine",
    "rbi_loop",
    "daily_digest",
    "session_briefing",
    "auto_approve",
    "perpetual_guardian",
    "backup_system",
    "system_health_monitor",
]

# ANSI color codes
_GRN = "\033[32m"
_YEL = "\033[33m"
_RED = "\033[31m"
_CYN = "\033[36m"
_BLD = "\033[1m"
_RST = "\033[0m"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _now():
    return datetime.now()


def _file_age_h(p: Path) -> float:
    """Hours since file was last modified. Returns inf if missing."""
    try:
        return (_now().timestamp() - p.stat().st_mtime) / 3600.0
    except OSError:
        return float("inf")


def _newest_in_dir(directory: Path, pattern: str = "*") -> float:
    """Age in hours of newest file matching pattern in directory. inf if none."""
    if not directory.is_dir():
        return float("inf")
    best = 0.0
    for p in directory.glob(pattern):
        if p.is_file():
            try:
                mt = p.stat().st_mtime
                if mt > best:
                    best = mt
            except OSError:
                pass
    if best == 0.0:
        return float("inf")
    return (_now().timestamp() - best) / 3600.0


def _newest_matching(base_dir: Path, pattern: str) -> float:
    """Age of newest file matching glob pattern under base_dir."""
    best = 0.0
    for p in base_dir.glob(pattern):
        if p.is_file():
            try:
                mt = p.stat().st_mtime
                if mt > best:
                    best = mt
            except OSError:
                pass
    if best == 0.0:
        return float("inf")
    return (_now().timestamp() - best) / 3600.0


def _csv_rows(p: Path) -> int:
    """Count data rows in CSV (excludes header). 0 if missing."""
    try:
        with open(p, "r", encoding="utf-8", errors="replace") as f:
            reader = csv.reader(f)
            next(reader, None)
            return sum(1 for _ in reader)
    except (OSError, csv.Error):
        return 0


def _http_status(url: str, timeout: int = 10) -> int:
    """HTTP status code for url. 0 on failure. Uses curl, then urllib fallback."""
    # curl is available on macOS and avoids import issues
    try:
        r = subprocess.run(
            ["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}",
             "--max-time", str(timeout), url],
            capture_output=True, text=True, timeout=timeout + 5,
        )
        code = int(r.stdout.strip())
        if code > 0:
            return code
    except Exception:
        pass
    # urllib fallback
    try:
        from urllib.request import urlopen, Request
        req = Request(url, method="HEAD")
        with urlopen(req, timeout=timeout) as resp:
            return resp.status
    except Exception:
        return 0


def _crontab_text() -> str:
    """Return current crontab contents as string, empty on error."""
    try:
        r = subprocess.run(["crontab", "-l"], capture_output=True, text=True, timeout=5)
        return r.stdout if r.returncode == 0 else ""
    except Exception:
        return ""


def _sev(age_h: float, amber: float = AMBER_H, red: float = RED_H) -> str:
    """Map age to severity: GREEN / AMBER / RED."""
    if age_h == float("inf"):
        return "RED"
    if age_h <= amber:
        return "GREEN"
    if age_h <= red:
        return "AMBER"
    return "RED"


def _status_word(sev: str) -> str:
    return {"GREEN": "RUNNING", "AMBER": "STALE", "RED": "DEAD"}.get(sev, "UNKNOWN")


def _fmt_age(h: float) -> str:
    if h == float("inf"):
        return "MISSING"
    if h < 1:
        return f"{h * 60:.0f}m ago"
    if h < 48:
        return f"{h:.1f}h ago"
    return f"{h / 24:.1f}d ago"


# ---------------------------------------------------------------------------
# 16 Health Checks
# ---------------------------------------------------------------------------

def check_01_cron_jobs() -> dict:
    """Cron job freshness: entries installed + key logs producing output."""
    ct = _crontab_text()
    if not ct.strip():
        return _result("01. Cron Jobs", "RED",
                       "crontab is EMPTY. Install: crontab AUTOMATIONS/crontab_printmaxx_v2.txt")

    found = sum(1 for m in CRON_MARKERS if m in ct)
    missing = [m for m in CRON_MARKERS if m not in ct]

    # Check freshness of key log files
    key_logs = {
        "overnight":       LOGS / "cron_overnight.log",
        "rbi_scanner":     LOGS / "rbi_scanner.log",
        "ventures":        LOGS / "cron_ventures.log",
        "signal_agg":      LOGS / "signal_agg.log",
        "brain_evening":   LOGS / "brain_evening.log",
        "closed_loop":     LOGS / "closed_loop.log",
    }
    stale_logs = sum(1 for p in key_logs.values() if _file_age_h(p) > AMBER_H)

    if found < len(CRON_MARKERS) // 2:
        sev = "RED"
        detail = f"Only {found}/{len(CRON_MARKERS)} key entries. Missing: {', '.join(missing[:3])}..."
    elif found < len(CRON_MARKERS):
        sev = "AMBER"
        detail = f"{found}/{len(CRON_MARKERS)} entries. Missing: {', '.join(missing)}"
    elif stale_logs > len(key_logs) // 2:
        sev = "AMBER"
        detail = f"All {found} entries installed but {stale_logs}/{len(key_logs)} key logs stale (>24h)"
    else:
        sev = "GREEN"
        detail = f"{found}/{len(CRON_MARKERS)} entries active, {len(key_logs) - stale_logs}/{len(key_logs)} logs fresh"

    log_ages = {k: round(_file_age_h(v), 1) if _file_age_h(v) != float("inf") else None
                for k, v in key_logs.items()}

    return _result("01. Cron Jobs", sev, detail, cron_entries=found,
                    missing_markers=missing, log_ages_h=log_ages)


def check_02_pipeline_freshness() -> dict:
    """Pipeline freshness: ANALYZED_LEADS, HOT_LEADS_QUALIFIED, progress.json."""
    # Core pipeline files (actively updated by closed_loop_pipeline.py)
    core_files = {
        "ANALYZED_LEADS.csv":       LEADS_QUAL / "ANALYZED_LEADS.csv",
        "HOT_LEADS_QUALIFIED.csv":  LEADS_QUAL / "HOT_LEADS_QUALIFIED.csv",
        "progress.json":            LEADS_QUAL / "progress.json",
    }
    # Legacy files (not updated by the newer pipeline, kept for reference)
    legacy_files = {
        "MASTER_LEADS.csv":         LEADS / "MASTER_LEADS.csv",
        "SCORED_LEADS.csv":         LEADS / "SCORED_LEADS.csv",
    }
    all_files = {**core_files, **legacy_files}

    ages = {}
    best_core = float("inf")
    for name, path in all_files.items():
        a = _file_age_h(path)
        ages[name] = round(a, 1) if a != float("inf") else None
        if name in core_files and a < best_core:
            best_core = a

    # Health is based on the freshest CORE pipeline file, not legacy files
    sev = _sev(best_core)
    if best_core == float("inf"):
        detail = "Core pipeline files missing"
    else:
        detail = f"Core pipeline: {_fmt_age(best_core)}, all files tracked"

    return _result("02. Pipeline Freshness", sev, detail, file_ages_h=ages)


def check_03_live_sites() -> dict:
    """Live site uptime: check all 16 surge.sh sites return 200."""
    up = 0
    down = []
    codes = {}

    for url in LIVE_SITES:
        code = _http_status(url)
        codes[url] = code
        if 200 <= code < 400:
            up += 1
        else:
            down.append(url)

    total = len(LIVE_SITES)
    pct = (up / total * 100) if total else 0

    if pct == 100:
        sev = "GREEN"
        detail = f"All {total} sites responding 200 OK"
    elif pct >= 75:
        sev = "AMBER"
        detail = f"{up}/{total} up, {len(down)} down"
    else:
        sev = "RED"
        detail = f"Only {up}/{total} sites up"

    return _result("03. Live Sites", sev, detail,
                    up=up, total=total, down_sites=down)


def check_04_memory_system() -> dict:
    """Memory system: HEARTBEAT.md + active-tasks.md freshness."""
    hb = _file_age_h(OPS / "HEARTBEAT.md")
    at = _file_age_h(OPS / "active-tasks.md")

    parts = []
    if hb != float("inf"):
        parts.append(f"HEARTBEAT {_fmt_age(hb)}")
    else:
        parts.append("HEARTBEAT MISSING")
    if at != float("inf"):
        parts.append(f"active-tasks {_fmt_age(at)}")
    else:
        parts.append("active-tasks MISSING")

    best = min(hb, at)
    sev = _sev(best)
    return _result("04. Memory System", sev, " | ".join(parts),
                    heartbeat_age_h=round(hb, 1) if hb != float("inf") else None,
                    active_tasks_age_h=round(at, 1) if at != float("inf") else None)


def check_05_lead_growth() -> dict:
    """Lead pipeline growth: row counts across lead files."""
    master_rows  = _csv_rows(LEADS / "MASTER_LEADS.csv")
    scored_rows  = _csv_rows(LEADS / "SCORED_LEADS.csv")
    hot_rows     = _csv_rows(LEADS / "HOT_LEADS.csv")
    analyzed     = _csv_rows(LEADS_QUAL / "ANALYZED_LEADS.csv")
    hot_qual     = _csv_rows(LEADS_QUAL / "HOT_LEADS_QUALIFIED.csv")

    # Count all *_leads.csv files
    all_lead_files = list(LEADS.glob("*_leads.csv"))
    total_files = len(all_lead_files)
    total_rows  = sum(_csv_rows(f) for f in all_lead_files)
    qualified   = analyzed + hot_qual

    if master_rows > 500 and qualified > 50:
        sev = "GREEN"
        detail = f"{master_rows} master, {scored_rows} scored, {hot_rows} hot, {qualified} qualified"
    elif master_rows > 100:
        sev = "AMBER"
        detail = f"{master_rows} master leads, only {qualified} qualified — pipeline needs cycling"
    else:
        sev = "RED"
        detail = f"Only {master_rows} master leads. Run closed_loop_pipeline."

    return _result("05. Lead Pipeline Growth", sev, detail,
                    master=master_rows, scored=scored_rows, hot=hot_rows,
                    qualified=qualified, total_files=total_files, total_rows=total_rows)


def check_06_cold_email() -> dict:
    """Cold email generation: outreach/ directory freshness + row counts."""
    if not OUTREACH.is_dir():
        return _result("06. Cold Email Gen", "RED", "outreach/ directory missing")

    age = _newest_in_dir(OUTREACH, "*.csv")
    email_files = list(OUTREACH.glob("*emails*.csv"))
    total_rows = sum(_csv_rows(f) for f in email_files)

    sev = _sev(age)
    if age == float("inf"):
        detail = "No cold email CSVs found in outreach/"
    else:
        detail = f"{len(email_files)} email files, {total_rows} rows, newest {_fmt_age(age)}"

    return _result("06. Cold Email Gen", sev, detail,
                    files=len(email_files), rows=total_rows,
                    newest_age_h=round(age, 1) if age != float("inf") else None)


def check_07_demo_generation() -> dict:
    """Demo generation: output/personalized_demos/ directory."""
    demos_dir = OUTPUT / "personalized_demos"
    if not demos_dir.is_dir():
        return _result("07. Demo Generation", "RED", "personalized_demos/ directory missing")

    # Count subdirectories (each is a personalized demo)
    demo_count = sum(1 for d in demos_dir.iterdir() if d.is_dir())
    age = _newest_in_dir(demos_dir)

    if demo_count == 0:
        sev = "RED"
        detail = "0 personalized demos generated"
    else:
        sev = _sev(age, amber=72, red=168)  # demos are generated less frequently
        detail = f"{demo_count} demos, newest {_fmt_age(age)}"

    return _result("07. Demo Generation", sev, detail, demo_count=demo_count)


def check_08_dashboard_freshness() -> dict:
    """Dashboard freshness: output/dashboard/index.html."""
    dash = OUTPUT / "dashboard" / "index.html"
    age = _file_age_h(dash)

    if age == float("inf"):
        # Check if SEO site is deployed as alternative dashboard
        seo_index = PROJECT_ROOT / "builds" / "programmatic_seo" / "index.html"
        seo_age = _file_age_h(seo_index)
        if seo_age != float("inf"):
            sev = _sev(seo_age, amber=72, red=168)
            detail = f"No dashboard/index.html, but SEO site exists ({_fmt_age(seo_age)})"
            return _result("08. Dashboard", sev, detail, seo_age_h=round(seo_age, 1))
        return _result("08. Dashboard", "RED", "No dashboard built. Neither output/dashboard/ nor builds/programmatic_seo/")

    sev = _sev(age, amber=72, red=168)
    detail = f"Dashboard updated {_fmt_age(age)}"
    return _result("08. Dashboard", sev, detail, age_h=round(age, 1))


def check_09_ecom_arb() -> dict:
    """Ecom arb scanner: LEDGER/ECOM_ARB_OPPORTUNITIES.csv + dated logs."""
    csv_path = LEDGER / "ECOM_ARB_OPPORTUNITIES.csv"
    csv_age = _file_age_h(csv_path)
    rows = _csv_rows(csv_path)

    # Check dated logs too (cron runs every 2h)
    log_age = _newest_matching(LOGS, "ecom_arb_*.log")
    effective = min(csv_age, log_age)

    sev = _sev(effective, amber=6, red=AMBER_H)  # should run every 2h
    if csv_age == float("inf"):
        detail = "ECOM_ARB_OPPORTUNITIES.csv MISSING"
    else:
        detail = f"{rows} opportunities, data {_fmt_age(csv_age)}, log {_fmt_age(log_age)}"

    return _result("09. Ecom Arb Scanner", sev, detail,
                    rows=rows, csv_age_h=round(csv_age, 1) if csv_age != float("inf") else None,
                    log_age_h=round(log_age, 1) if log_age != float("inf") else None)


def check_10_freelance_demand() -> dict:
    """Freelance demand scanner: LEDGER/FREELANCE_DEMAND_SCAN.csv + logs."""
    csv_path = LEDGER / "FREELANCE_DEMAND_SCAN.csv"
    csv_age = _file_age_h(csv_path)
    rows = _csv_rows(csv_path)

    log_age = _newest_matching(LOGS, "freelance_demand_*.log")
    effective = min(csv_age, log_age)

    sev = _sev(effective, amber=6, red=AMBER_H)  # runs every 2h
    if csv_age == float("inf"):
        detail = "FREELANCE_DEMAND_SCAN.csv MISSING"
    else:
        detail = f"{rows} demand signals, data {_fmt_age(csv_age)}, log {_fmt_age(log_age)}"

    return _result("10. Freelance Demand", sev, detail,
                    rows=rows, csv_age_h=round(csv_age, 1) if csv_age != float("inf") else None,
                    log_age_h=round(log_age, 1) if log_age != float("inf") else None)


def check_11_trend_aggregator() -> dict:
    """Trend aggregator: LEDGER/TREND_SIGNALS.csv + logs."""
    csv_path = LEDGER / "TREND_SIGNALS.csv"
    csv_age = _file_age_h(csv_path)
    rows = _csv_rows(csv_path)

    log_age = _newest_matching(LOGS, "trend_agg_*.log")
    effective = min(csv_age, log_age)

    sev = _sev(effective, amber=8, red=AMBER_H)  # runs every 4h
    if csv_age == float("inf"):
        detail = "TREND_SIGNALS.csv MISSING"
    else:
        detail = f"{rows} signals, data {_fmt_age(csv_age)}, log {_fmt_age(log_age)}"

    return _result("11. Trend Aggregator", sev, detail,
                    rows=rows, csv_age_h=round(csv_age, 1) if csv_age != float("inf") else None,
                    log_age_h=round(log_age, 1) if log_age != float("inf") else None)


def check_12_daily_logs() -> dict:
    """Daily log freshness: AUTOMATIONS/logs/daily/ directory."""
    if not DAILY_LOGS.is_dir():
        return _result("12. Daily Logs", "RED", "logs/daily/ directory missing")

    today_str = _now().strftime("%Y-%m-%d")
    today_log = DAILY_LOGS / f"{today_str}.md"

    log_files = sorted(DAILY_LOGS.glob("*.md"), reverse=True)
    recent = sum(1 for f in log_files if _file_age_h(f) < 72)

    if today_log.exists():
        age = _file_age_h(today_log)
        sev = "GREEN"
        detail = f"Today's log exists ({_fmt_age(age)}), {recent} recent logs"
    elif recent > 0:
        newest = _newest_in_dir(DAILY_LOGS, "*.md")
        sev = "AMBER"
        detail = f"No today log, newest {_fmt_age(newest)}, {recent} within 72h"
    else:
        sev = "RED"
        detail = "No recent daily logs found"

    return _result("12. Daily Logs", sev, detail,
                    today_exists=today_log.exists(), recent_count=recent)


def check_13_running_processes() -> dict:
    """Running processes: check for key background automations."""
    procs = [
        "closed_loop_pipeline",
        "intelligent_lead_qualifier",
        "memory_manager",
        "perpetual_improvement_runner",
        "perpetual_ship_engine",
        "freelance_demand_scanner",
        "ecom_arb_engine",
        "trend_aggregator",
        "signal_aggregator",
        "printmaxx_brain",
    ]

    running = {}
    my_pid = str(os.getpid())
    for name in procs:
        try:
            r = subprocess.run(["pgrep", "-f", name],
                               capture_output=True, text=True, timeout=5)
            pids = [p.strip() for p in r.stdout.strip().split("\n")
                    if p.strip() and p.strip() != my_pid]
            running[name] = len(pids) > 0
        except Exception:
            running[name] = False

    active = sum(1 for v in running.values() if v)
    total = len(procs)
    active_names = [k for k, v in running.items() if v]

    # Most of these are cron-scheduled, so 0 running between runs is normal.
    # We report what's active NOW but don't panic if nothing is running.
    if active > 2:
        sev = "GREEN"
        detail = f"{active}/{total} running: {', '.join(active_names[:3])}"
    elif active > 0:
        sev = "GREEN"
        detail = f"{active}/{total} running now ({', '.join(active_names)})"
    else:
        sev = "AMBER"
        detail = f"0/{total} running (normal between cron schedules)"

    return _result("13. Running Processes", sev, detail,
                    active=active, total=total, processes=running)


def check_14_disk_space() -> dict:
    """Disk space check."""
    try:
        usage = shutil.disk_usage(str(PROJECT_ROOT))
        free_gb = usage.free / (1024 ** 3)
        total_gb = usage.total / (1024 ** 3)
        used_pct = (usage.used / usage.total) * 100

        if used_pct > 95:
            sev = "RED"
        elif used_pct > 85:
            sev = "AMBER"
        else:
            sev = "GREEN"

        detail = f"{used_pct:.1f}% used, {free_gb:.1f}GB free of {total_gb:.0f}GB"
        return _result("14. Disk Space", sev, detail,
                        used_pct=round(used_pct, 1), free_gb=round(free_gb, 1))
    except Exception as e:
        return _result("14. Disk Space", "RED", f"Check failed: {e}")


def check_15_new_pipelines() -> dict:
    """New pipeline freshness: content_trend, app_clone, tweet_drafter, quote_scanner logs."""
    log_map = {
        "content_trends": LOGS / "content_trends.log",
        "app_clone":      LOGS / "app_clone.log",
        "tweet_drafter":  LOGS / "tweet_drafter.log",
        "quote_scanner":  LOGS / "quote_scanner.log",
    }
    ages = {}
    worst = 0.0
    for name, path in log_map.items():
        a = _file_age_h(path)
        ages[name] = round(a, 1) if a != float("inf") else None
        if a > worst:
            worst = a

    if worst == float("inf"):
        sev = "RED"
        detail = "Some new pipeline logs missing"
    elif worst > RED_H:
        sev = "RED"
        detail = f"New pipelines stale: worst {_fmt_age(worst)}"
    elif worst > AMBER_H:
        sev = "AMBER"
        detail = f"New pipelines aging: worst {_fmt_age(worst)}"
    else:
        sev = "GREEN"
        detail = f"New pipelines healthy: worst {_fmt_age(worst)}"

    return _result("15. New Pipelines", sev, detail, file_ages_h=ages)


def check_16_git_push_health() -> dict:
    """Git push health: unpushed commit count and age of last push."""
    try:
        # Count unpushed commits (HEAD ahead of origin/main)
        rev_list = subprocess.run(
            ["git", "rev-list", "--count", "origin/main..HEAD"],
            capture_output=True, text=True, timeout=15,
            cwd=str(PROJECT_ROOT)
        )
        if rev_list.returncode != 0:
            # origin/main may not exist (no remote configured or never pushed)
            stderr = rev_list.stderr.strip()
            if "unknown revision" in stderr or "bad revision" in stderr:
                return _result("16. Git Push Health", "AMBER",
                               "No origin/main ref — remote may not be configured",
                               unpushed=None, push_age_h=None)
            return _result("16. Git Push Health", "RED",
                           f"rev-list failed: {stderr[:120]}",
                           unpushed=None, push_age_h=None)

        unpushed = int(rev_list.stdout.strip())

        # Get age of last push by checking origin/main commit timestamp
        push_age_h = None
        try:
            ts_result = subprocess.run(
                ["git", "log", "-1", "--format=%ct", "origin/main"],
                capture_output=True, text=True, timeout=10,
                cwd=str(PROJECT_ROOT)
            )
            if ts_result.returncode == 0 and ts_result.stdout.strip():
                origin_ts = int(ts_result.stdout.strip())
                push_age_h = (_now().timestamp() - origin_ts) / 3600.0
        except Exception:
            pass

        # Severity based on unpushed count
        # GREEN: 0 unpushed
        # AMBER: 1-5 unpushed
        # RED: 6+ unpushed (push failing for 12+ hours given 4h guardian cycle)
        if unpushed == 0:
            sev = "GREEN"
            age_str = f", last push {_fmt_age(push_age_h)}" if push_age_h is not None else ""
            detail = f"0 unpushed commits{age_str}"
        elif unpushed <= 5:
            sev = "AMBER"
            age_str = f", last push {_fmt_age(push_age_h)}" if push_age_h is not None else ""
            detail = f"{unpushed} unpushed commits{age_str}"
        else:
            sev = "RED"
            age_str = f", last push {_fmt_age(push_age_h)}" if push_age_h is not None else ""
            detail = f"{unpushed} unpushed commits (push failing 12h+?){age_str}"

        return _result("16. Git Push Health", sev, detail,
                        unpushed=unpushed,
                        push_age_h=round(push_age_h, 1) if push_age_h is not None else None)

    except Exception as e:
        return _result("16. Git Push Health", "RED", f"Check failed: {e}",
                        unpushed=None, push_age_h=None)


# ---------------------------------------------------------------------------
# Result builder
# ---------------------------------------------------------------------------

def _result(check: str, severity: str, detail: str, **extra) -> dict:
    """Build a standardized check result dict."""
    return {
        "check": check,
        "severity": severity,
        "status": _status_word(severity),
        "detail": detail,
        **extra,
    }


# ---------------------------------------------------------------------------
# Orchestrator
# ---------------------------------------------------------------------------

ALL_CHECKS = [
    check_01_cron_jobs,
    check_02_pipeline_freshness,
    check_03_live_sites,
    check_04_memory_system,
    check_05_lead_growth,
    check_06_cold_email,
    check_07_demo_generation,
    check_08_dashboard_freshness,
    check_09_ecom_arb,
    check_10_freelance_demand,
    check_11_trend_aggregator,
    check_12_daily_logs,
    check_13_running_processes,
    check_14_disk_space,
    check_15_new_pipelines,
    check_16_git_push_health,
]


def run_all(skip_sites: bool = False) -> list:
    """Execute all 16 health checks."""
    results = []
    for fn in ALL_CHECKS:
        if skip_sites and fn is check_03_live_sites:
            results.append(_result("03. Live Sites", "GREEN",
                                    "Skipped (--skip-sites)", skipped=True))
            continue
        try:
            results.append(fn())
        except Exception as e:
            name = fn.__doc__.split(":")[0].strip() if fn.__doc__ else fn.__name__
            results.append(_result(name, "RED", f"Check crashed: {e}"))
    return results


def compute_summary(results: list) -> dict:
    """Overall health percentage and grade."""
    scores = {"GREEN": 100, "AMBER": 50, "RED": 0}
    total_score = sum(scores.get(r["severity"], 0) for r in results)
    max_score = len(results) * 100
    pct = (total_score / max_score * 100) if max_score else 0

    green = sum(1 for r in results if r["severity"] == "GREEN")
    amber = sum(1 for r in results if r["severity"] == "AMBER")
    red   = sum(1 for r in results if r["severity"] == "RED")

    if pct >= 85:
        grade = "HEALTHY"
    elif pct >= 60:
        grade = "DEGRADED"
    elif pct >= 30:
        grade = "CRITICAL"
    else:
        grade = "DOWN"

    return {
        "health_pct": round(pct, 1),
        "grade": grade,
        "green": green,
        "amber": amber,
        "red": red,
        "total": len(results),
        "timestamp": _now().isoformat(),
    }


def write_report(results: list, summary: dict) -> Path:
    """Write JSON report to AUTOMATIONS/logs/system_health_YYYY-MM-DD.json."""
    LOGS.mkdir(parents=True, exist_ok=True)
    path = LOGS / f"system_health_{_now().strftime('%Y-%m-%d')}.json"
    report = {
        "summary": summary,
        "checks": results,
        "generated_at": _now().isoformat(),
        "project_root": str(PROJECT_ROOT),
    }
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2, default=str)
    except OSError:
        pass  # never crash on write failure
    return path


# ---------------------------------------------------------------------------
# Display
# ---------------------------------------------------------------------------

def _use_color() -> bool:
    if os.environ.get("NO_COLOR"):
        return False
    return hasattr(sys.stdout, "isatty") and sys.stdout.isatty()


def _sev_badge(sev: str, color: bool) -> str:
    if not color:
        return {"GREEN": "[RUNNING]", "AMBER": "[ STALE ]", "RED": "[ DEAD  ]"}.get(sev, "[ ??? ]")
    c = {"GREEN": _GRN, "AMBER": _YEL, "RED": _RED}.get(sev, _RST)
    w = _status_word(sev)
    return f"{c}[{w:^8s}]{_RST}"


def print_full(results: list, summary: dict, report_path: Path):
    """Print formatted 16-point health table."""
    color = _use_color()
    w = 80

    if color:
        print(f"\n{_BLD}{_CYN}{'=' * w}{_RST}")
        print(f"{_BLD}{_CYN}  PRINTMAXX SYSTEM HEALTH MONITOR{_RST}")
        print(f"{_CYN}  {_now().strftime('%Y-%m-%d %H:%M:%S')}{_RST}")
        print(f"{_BLD}{_CYN}{'=' * w}{_RST}\n")
    else:
        print(f"\n{'=' * w}")
        print(f"  PRINTMAXX SYSTEM HEALTH MONITOR")
        print(f"  {_now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'=' * w}\n")

    for r in results:
        badge = _sev_badge(r["severity"], color)
        name = r["check"]
        detail = r.get("detail", "")
        max_d = w - 42
        if len(detail) > max_d:
            detail = detail[:max_d - 3] + "..."
        if color:
            print(f"  {badge}  {_BLD}{name:<30s}{_RST} {detail}")
        else:
            print(f"  {badge}  {name:<30s} {detail}")

    # Summary
    pct = summary["health_pct"]
    grade = summary["grade"]
    g, a, rd = summary["green"], summary["amber"], summary["red"]

    print()
    if color:
        print(f"{_BLD}{'-' * w}{_RST}")
        gc = _GRN if pct >= 85 else (_YEL if pct >= 60 else _RED)
        print(f"  SYSTEM HEALTH: {gc}{_BLD}{pct:.0f}% ({grade}){_RST}  "
              f"|  {_GRN}GREEN={g}{_RST}  {_YEL}AMBER={a}{_RST}  {_RED}RED={rd}{_RST}")
        print(f"{_BLD}{'=' * w}{_RST}")
    else:
        print(f"{'-' * w}")
        print(f"  SYSTEM HEALTH: {pct:.0f}% ({grade})  |  GREEN={g}  AMBER={a}  RED={rd}")
        print(f"{'=' * w}")

    # List RED items with suggested fixes
    red_items = [r for r in results if r["severity"] == "RED"]
    if red_items:
        print()
        hdr = "  RED ITEMS (need attention):" if not color else f"  {_RED}{_BLD}RED ITEMS (need attention):{_RST}"
        print(hdr)
        for r in red_items:
            print(f"    - {r['check']}: {r['detail']}")
        print()

    print(f"  Report: {report_path}\n")


def print_quick(summary: dict):
    """Single summary line."""
    pct = summary["health_pct"]
    grade = summary["grade"]
    g, a, rd = summary["green"], summary["amber"], summary["red"]
    ts = _now().strftime("%Y-%m-%d %H:%M")
    print(f"PRINTMAXX HEALTH: {pct:.0f}% ({grade}) | GREEN={g} AMBER={a} RED={rd} | {ts}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="PRINTMAXX System Health Monitor - 16-point automated system check"
    )
    parser.add_argument("--check", action="store_true", default=True,
                        help="Full 16-point health check (default)")
    parser.add_argument("--quick", action="store_true",
                        help="Summary line only")
    parser.add_argument("--json", action="store_true",
                        help="Machine-readable JSON output")
    parser.add_argument("--skip-sites", action="store_true",
                        help="Skip live site HTTP checks (faster)")
    args = parser.parse_args()

    results = run_all(skip_sites=args.skip_sites)
    summary = compute_summary(results)
    report_path = write_report(results, summary)

    if args.json:
        out = {"summary": summary, "checks": results, "report_path": str(report_path)}
        print(json.dumps(out, indent=2, default=str))
    elif args.quick:
        print_quick(summary)
    else:
        print_full(results, summary, report_path)

    # Exit code: 0=healthy, 1=degraded, 2=critical/down
    if summary["health_pct"] >= 85:
        sys.exit(0)
    elif summary["health_pct"] >= 60:
        sys.exit(1)
    else:
        sys.exit(2)


if __name__ == "__main__":
    main()
