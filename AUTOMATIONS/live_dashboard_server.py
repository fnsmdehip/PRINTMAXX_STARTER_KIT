#!/usr/bin/env python3
"""
PRINTMAXX Live Dashboard Server
================================
Bloomberg-style live monitoring dashboard for the entire PRINTMAXX project.
Reads ALL real data from CSVs, logs, and files. Zero mock data.

Usage:
    python3 AUTOMATIONS/live_dashboard_server.py
    # Opens http://localhost:8888 in browser

Architecture:
    - Flask server on localhost:8888
    - /api/status endpoint returns real-time JSON from all project files
    - Static HTML dashboard auto-refreshes every 30 seconds
    - Robust error handling: missing files show "NO DATA", never crashes
"""

import csv
import json
import os
import sys
import time
import glob
import subprocess
import threading
import webbrowser
from datetime import datetime, timedelta
from pathlib import Path
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed

try:
    from flask import Flask, jsonify, send_file, Response
except ImportError:
    print("ERROR: Flask not installed. Run: pip3 install flask")
    sys.exit(1)

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parent.parent
PORT = 8888
DASHBOARD_HTML = Path(__file__).resolve().parent / "live_dashboard.html"

# Live site URLs to health-check
LIVE_SITES = [
    ("Hilal Ramadan", "https://hilal-ramadan.surge.sh"),
    ("SEO Pages (601)", "https://printmaxx-seo.surge.sh"),
    ("FocusLock", "https://focuslock-app.surge.sh"),
    ("HabitForge", "https://habitforge-app.surge.sh"),
    ("SleepMaxx", "https://sleepmaxx-app.surge.sh"),
    ("WalkToUnlock", "https://walktounlock-app.surge.sh"),
    ("MealMaxx", "https://mealmaxx-app.surge.sh"),
    ("Demo Sites", "https://printmaxx-demos.surge.sh"),
    ("SiteScore SaaS", "https://sitescore-app.surge.sh"),
    ("SiteScore Analyzer", "https://sitescore-analyzer.surge.sh"),
    ("ShopMetrics", "https://shopmetrics-dashboard.surge.sh"),
    ("Flowstack", "https://flowstack-demo.surge.sh"),
]

# Cache for site health checks (avoid hammering sites every 30s)
_site_health_cache = {"data": [], "last_check": 0}
SITE_CHECK_INTERVAL = 300  # 5 minutes

app = Flask(__name__)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def safe_read_csv(filepath, max_rows=50000):
    """Read CSV file safely. Returns list of dicts or empty list on error."""
    full = PROJECT_ROOT / filepath
    if not full.exists():
        return []
    try:
        rows = []
        with open(full, "r", encoding="utf-8", errors="replace") as f:
            reader = csv.DictReader(f)
            for i, row in enumerate(reader):
                if i >= max_rows:
                    break
                rows.append(row)
        return rows
    except Exception:
        return []


def safe_count_csv(filepath):
    """Count rows in CSV without loading all into memory."""
    full = PROJECT_ROOT / filepath
    if not full.exists():
        return 0
    try:
        with open(full, "r", encoding="utf-8", errors="replace") as f:
            return sum(1 for _ in f) - 1  # subtract header
    except Exception:
        return 0


def safe_read_text(filepath, max_chars=5000):
    """Read text file safely, return string or None."""
    full = PROJECT_ROOT / filepath
    if not full.exists():
        return None
    try:
        with open(full, "r", encoding="utf-8", errors="replace") as f:
            return f.read(max_chars)
    except Exception:
        return None


def safe_count_lines(filepath):
    """Count lines in file."""
    full = PROJECT_ROOT / filepath
    if not full.exists():
        return 0
    try:
        with open(full, "r", encoding="utf-8", errors="replace") as f:
            return sum(1 for _ in f)
    except Exception:
        return 0


def safe_file_mtime(filepath):
    """Get file modification time as ISO string."""
    full = PROJECT_ROOT / filepath
    if not full.exists():
        return None
    try:
        ts = os.path.getmtime(full)
        return datetime.fromtimestamp(ts).isoformat()
    except Exception:
        return None


def glob_count(pattern):
    """Count files matching glob pattern under PROJECT_ROOT."""
    try:
        return len(glob.glob(str(PROJECT_ROOT / pattern)))
    except Exception:
        return 0


def glob_total_lines(pattern):
    """Count total lines across all files matching pattern."""
    total = 0
    try:
        for fp in glob.glob(str(PROJECT_ROOT / pattern)):
            try:
                with open(fp, "r", encoding="utf-8", errors="replace") as f:
                    total += sum(1 for _ in f)
            except Exception:
                pass
    except Exception:
        pass
    return total


def check_site_health(name, url):
    """Check if a site returns HTTP 200. Returns dict."""
    try:
        import urllib.request
        req = urllib.request.Request(url, method="HEAD")
        req.add_header("User-Agent", "PRINTMAXX-Dashboard/1.0")
        resp = urllib.request.urlopen(req, timeout=8)
        return {"name": name, "url": url, "status": resp.status, "ok": resp.status == 200}
    except Exception as e:
        return {"name": name, "url": url, "status": str(e)[:60], "ok": False}


def get_site_health():
    """Get health of all live sites. Cached for SITE_CHECK_INTERVAL seconds."""
    now = time.time()
    if now - _site_health_cache["last_check"] < SITE_CHECK_INTERVAL and _site_health_cache["data"]:
        return _site_health_cache["data"]

    results = []
    with ThreadPoolExecutor(max_workers=6) as executor:
        futures = {executor.submit(check_site_health, n, u): (n, u) for n, u in LIVE_SITES}
        for future in as_completed(futures, timeout=15):
            try:
                results.append(future.result())
            except Exception:
                n, u = futures[future]
                results.append({"name": n, "url": u, "status": "timeout", "ok": False})

    _site_health_cache["data"] = results
    _site_health_cache["last_check"] = now
    return results


# ---------------------------------------------------------------------------
# Data Collectors
# ---------------------------------------------------------------------------
def collect_alpha_funnel():
    """Alpha pipeline stats from ALPHA_STAGING.csv."""
    rows = safe_read_csv("LEDGER/ALPHA_STAGING.csv")
    if not rows:
        return {"total": 0, "by_status": {}, "by_category": {}, "today": 0}

    status_counts = Counter()
    cat_counts = Counter()
    today_str = datetime.now().strftime("%Y-%m-%d")
    today_count = 0

    for r in rows:
        s = (r.get("status") or "UNKNOWN").strip().upper()
        c = (r.get("category") or "UNKNOWN").strip()
        status_counts[s] += 1
        cat_counts[c] += 1
        created = r.get("created_at") or ""
        if created and today_str in created:
            today_count += 1

    return {
        "total": len(rows),
        "by_status": dict(status_counts.most_common(10)),
        "by_category": dict(cat_counts.most_common(15)),
        "today": today_count,
    }


def collect_auto_ops():
    """Auto-ops stats from AUTO_OPS_TRACKER.csv."""
    rows = safe_read_csv("LEDGER/AUTO_OPS_TRACKER.csv")
    if not rows:
        return {"total": 0, "by_status": {}, "by_category": {}}

    status_counts = Counter()
    cat_counts = Counter()
    for r in rows:
        s = (r.get("status") or "UNKNOWN").strip()
        c = (r.get("category") or "UNKNOWN").strip()
        status_counts[s] += 1
        cat_counts[c] += 1

    return {
        "total": len(rows),
        "by_status": dict(status_counts.most_common(10)),
        "by_category": dict(cat_counts.most_common(15)),
    }


def collect_research_pipeline():
    """Research pipeline: sources, latest digest, scraping status."""
    sources = safe_read_csv("LEDGER/HIGH_SIGNAL_SOURCES.csv")
    source_types = Counter()
    for s in sources:
        st = (s.get("source_type") or s.get("platform") or "unknown").strip()
        source_types[st] += 1

    # Latest digest
    digest_files = sorted(glob.glob(str(PROJECT_ROOT / "OPS/DAILY_RESEARCH_DIGEST_*.md")))
    latest_digest = None
    if digest_files:
        latest_digest = {
            "file": os.path.basename(digest_files[-1]),
            "modified": safe_file_mtime(os.path.relpath(digest_files[-1], PROJECT_ROOT)),
        }

    # Latest log
    log_path = PROJECT_ROOT / "AUTOMATIONS/logs/daily_research_pipeline.log"
    log_mtime = None
    if log_path.exists():
        log_mtime = datetime.fromtimestamp(os.path.getmtime(log_path)).isoformat()

    return {
        "total_sources": len(sources),
        "by_type": dict(source_types.most_common(10)),
        "latest_digest": latest_digest,
        "pipeline_log_last_run": log_mtime,
    }


def collect_lead_pipeline():
    """Lead counts from AUTOMATIONS/leads/ and outreach/."""
    lead_files = glob.glob(str(PROJECT_ROOT / "AUTOMATIONS/leads/*.csv"))
    total_leads = 0
    hot_leads = 0
    scored_leads = 0
    lead_files_count = len(lead_files)

    for fp in lead_files:
        try:
            with open(fp, "r", encoding="utf-8", errors="replace") as f:
                count = sum(1 for _ in f) - 1
                total_leads += max(count, 0)
                bn = os.path.basename(fp)
                if "HOT" in bn.upper():
                    hot_leads += max(count, 0)
                if "SCORED" in bn.upper():
                    scored_leads += max(count, 0)
        except Exception:
            pass

    # Outreach stats
    outreach_files = glob.glob(str(PROJECT_ROOT / "AUTOMATIONS/outreach/*.csv"))
    total_emails = 0
    for fp in outreach_files:
        try:
            with open(fp, "r", encoding="utf-8", errors="replace") as f:
                total_emails += max(sum(1 for _ in f) - 1, 0)
        except Exception:
            pass

    # Pipeline tracker
    pipeline_rows = safe_read_csv("AUTOMATIONS/outreach/PIPELINE_TRACKER.csv")
    pipeline_status = Counter()
    for r in pipeline_rows:
        s = (r.get("status") or "UNKNOWN").strip()
        pipeline_status[s] += 1

    return {
        "total_leads": total_leads,
        "hot_leads": hot_leads,
        "scored_leads": scored_leads,
        "lead_files": lead_files_count,
        "total_emails_generated": total_emails,
        "outreach_files": len(outreach_files),
        "pipeline_by_status": dict(pipeline_status.most_common(10)),
    }


def collect_revenue():
    """Revenue data from FINANCIALS/ and LEDGER/."""
    rev_rows = safe_read_csv("FINANCIALS/REVENUE_TRACKER.csv")
    total_revenue = 0
    total_expenses = 0
    total_profit = 0
    by_method = Counter()
    for r in rev_rows:
        try:
            rev = float(r.get("revenue", 0) or 0)
            exp = float(r.get("expenses", 0) or 0)
            total_revenue += rev
            total_expenses += exp
            total_profit += rev - exp
            m = r.get("method_name", "unknown")
            by_method[m] += rev
        except (ValueError, TypeError):
            pass

    # Revenue streams tracker
    streams = safe_read_csv("LEDGER/REVENUE_STREAMS_TRACKER.csv")
    stream_status = Counter()
    for s in streams:
        st = (s.get("status") or "UNKNOWN").strip()
        stream_status[st] += 1

    return {
        "total_revenue": round(total_revenue, 2),
        "total_expenses": round(total_expenses, 2),
        "total_profit": round(total_profit, 2),
        "by_method": dict(by_method.most_common(10)),
        "revenue_streams": len(streams),
        "streams_by_status": dict(stream_status.most_common(10)),
    }


def collect_content_pipeline():
    """Content stats from calendar, social, auto-generated."""
    cal_count = safe_count_csv("LEDGER/CONTENT_CALENDAR_30DAY.csv")

    # Content calendar by niche
    cal_rows = safe_read_csv("LEDGER/CONTENT_CALENDAR_30DAY.csv")
    by_niche = Counter()
    by_platform = Counter()
    by_status = Counter()
    for r in cal_rows:
        n = (r.get("niche") or "unknown").strip()
        p = (r.get("platform") or "unknown").strip()
        s = (r.get("status") or "unknown").strip()
        by_niche[n] += 1
        by_platform[p] += 1
        by_status[s] += 1

    # Auto-generated content
    auto_gen_files = glob.glob(str(PROJECT_ROOT / "CONTENT/social/auto_generated/*.csv"))
    auto_gen_count = 0
    for fp in auto_gen_files:
        try:
            with open(fp, "r", encoding="utf-8", errors="replace") as f:
                auto_gen_count += max(sum(1 for _ in f) - 1, 0)
        except Exception:
            pass

    # Buffer CSVs
    buffer_files = glob.glob(str(PROJECT_ROOT / "LEDGER/buffer_import_*.csv"))
    buffer_count = len(buffer_files)
    buffer_total_posts = 0
    for fp in buffer_files:
        try:
            with open(fp, "r", encoding="utf-8", errors="replace") as f:
                buffer_total_posts += max(sum(1 for _ in f) - 1, 0)
        except Exception:
            pass

    # Content posting CSVs
    posting_csvs = glob.glob(str(PROJECT_ROOT / "AUTOMATIONS/content_posting/*.csv"))
    posting_total = 0
    for fp in posting_csvs:
        try:
            with open(fp, "r", encoding="utf-8", errors="replace") as f:
                posting_total += max(sum(1 for _ in f) - 1, 0)
        except Exception:
            pass

    return {
        "calendar_posts": cal_count,
        "by_niche": dict(by_niche.most_common(10)),
        "by_platform": dict(by_platform.most_common(10)),
        "by_status": dict(by_status.most_common(5)),
        "auto_generated": auto_gen_count,
        "auto_gen_files": len(auto_gen_files),
        "buffer_files": buffer_count,
        "buffer_total_posts": buffer_total_posts,
        "posting_csvs": len(posting_csvs),
        "posting_total": posting_total,
    }


def collect_system_health():
    """System health: log files, cron status, file counts."""
    log_dir = PROJECT_ROOT / "AUTOMATIONS/logs"
    log_entries = []
    if log_dir.exists():
        for fp in sorted(log_dir.iterdir(), key=lambda x: x.stat().st_mtime, reverse=True)[:15]:
            try:
                log_entries.append({
                    "name": fp.name,
                    "modified": datetime.fromtimestamp(fp.stat().st_mtime).isoformat(),
                    "size_kb": round(fp.stat().st_size / 1024, 1),
                    "age_minutes": round((time.time() - fp.stat().st_mtime) / 60, 1),
                })
            except Exception:
                pass

    # Cron health (check key log files and their freshness)
    cron_jobs = {
        "backup": "AUTOMATIONS/logs/cron_backup.log",
        "ventures": "AUTOMATIONS/logs/cron_ventures.log",
        "orchestrator": "AUTOMATIONS/logs/orchestrator.log",
        "ecom_arb": "AUTOMATIONS/logs/ecom_arb_2026-02-13.log",
        "freelance_demand": "AUTOMATIONS/logs/freelance_demand_2026-02-13.log",
        "trend_agg": "AUTOMATIONS/logs/trend_agg_2026-02-13.log",
        "signal_agg": "AUTOMATIONS/logs/signal_agg.log",
        "daily_research": "AUTOMATIONS/logs/daily_research_pipeline.log",
        "competitor_sourcing": "AUTOMATIONS/logs/competitor_sourcing_2026-02-13.log",
        "video_pipeline": "AUTOMATIONS/logs/video_pipeline_2026-02-13.log",
    }
    cron_status = {}
    for job, path in cron_jobs.items():
        full = PROJECT_ROOT / path
        if full.exists():
            try:
                mt = full.stat().st_mtime
                age_min = (time.time() - mt) / 60
                cron_status[job] = {
                    "last_run": datetime.fromtimestamp(mt).isoformat(),
                    "age_minutes": round(age_min, 1),
                    "health": "green" if age_min < 120 else ("yellow" if age_min < 1440 else "red"),
                    "size_kb": round(full.stat().st_size / 1024, 1),
                }
            except Exception:
                cron_status[job] = {"last_run": None, "health": "red"}
        else:
            cron_status[job] = {"last_run": None, "health": "grey"}

    # Total project stats
    total_py = glob_count("**/*.py")
    total_csv = glob_count("LEDGER/*.csv") + glob_count("AUTOMATIONS/**/*.csv") + glob_count("FINANCIALS/*.csv")
    total_md = glob_count("OPS/*.md") + glob_count("MONEY_METHODS/**/*.md")

    return {
        "recent_logs": log_entries,
        "cron_status": cron_status,
        "total_py_scripts": total_py,
        "total_csv_files": total_csv,
        "total_md_docs": total_md,
        "total_log_files": glob_count("AUTOMATIONS/logs/*"),
    }


def collect_accounts():
    """Account status from LEDGER/ACCOUNTS.csv."""
    rows = safe_read_csv("LEDGER/ACCOUNTS.csv")
    status_counts = Counter()
    platform_counts = Counter()
    for r in rows:
        s = (r.get("Status") or "UNKNOWN").strip()
        p = (r.get("Platform") or "unknown").strip()
        status_counts[s] += 1
        platform_counts[p] += 1

    return {
        "total": len(rows),
        "by_status": dict(status_counts.most_common(10)),
        "by_platform": dict(platform_counts.most_common(15)),
    }


def collect_recent_activity():
    """Recent file modifications across the project (last 2 hours)."""
    cutoff = time.time() - 7200  # 2 hours
    recent = []
    search_dirs = [
        "LEDGER", "AUTOMATIONS", "OPS", "CONTENT", "PRODUCTS",
        "FINANCIALS", "MONEY_METHODS", "DIGITAL_PRODUCTS", "builds",
    ]
    for d in search_dirs:
        base = PROJECT_ROOT / d
        if not base.exists():
            continue
        try:
            for fp in base.rglob("*"):
                if fp.is_file() and fp.stat().st_mtime > cutoff:
                    try:
                        recent.append({
                            "path": str(fp.relative_to(PROJECT_ROOT)),
                            "modified": datetime.fromtimestamp(fp.stat().st_mtime).isoformat(),
                            "size_kb": round(fp.stat().st_size / 1024, 1),
                            "age_minutes": round((time.time() - fp.stat().st_mtime) / 60, 1),
                        })
                    except Exception:
                        pass
        except Exception:
            pass

    recent.sort(key=lambda x: x["modified"], reverse=True)
    return recent[:30]


def collect_prompt_log():
    """Prompt log stats from LEDGER/PROMPT_LOG.jsonl."""
    fp = PROJECT_ROOT / "LEDGER/PROMPT_LOG.jsonl"
    if not fp.exists():
        return {"total": 0, "today": 0}
    total = 0
    today_count = 0
    today_str = datetime.now().strftime("%Y-%m-%d")
    try:
        with open(fp, "r", encoding="utf-8", errors="replace") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                total += 1
                if today_str in line:
                    today_count += 1
    except Exception:
        pass
    return {"total": total, "today": today_count}


def collect_live_sites():
    """Check live site health."""
    return get_site_health()


# ---------------------------------------------------------------------------
# Main API endpoint
# ---------------------------------------------------------------------------
@app.route("/api/status")
def api_status():
    """Return full project status as JSON."""
    start = time.time()

    data = {
        "timestamp": datetime.now().isoformat(),
        "project_root": str(PROJECT_ROOT),
        "alpha_funnel": collect_alpha_funnel(),
        "auto_ops": collect_auto_ops(),
        "research_pipeline": collect_research_pipeline(),
        "lead_pipeline": collect_lead_pipeline(),
        "revenue": collect_revenue(),
        "content_pipeline": collect_content_pipeline(),
        "system_health": collect_system_health(),
        "accounts": collect_accounts(),
        "recent_activity": collect_recent_activity(),
        "prompt_log": collect_prompt_log(),
        "live_sites": collect_live_sites(),
        "query_time_ms": round((time.time() - start) * 1000, 1),
    }

    resp = jsonify(data)
    resp.headers["Cache-Control"] = "no-cache"
    return resp


@app.route("/")
def index():
    """Serve the dashboard HTML."""
    if DASHBOARD_HTML.exists():
        return send_file(DASHBOARD_HTML)
    return Response("<h1>Dashboard HTML not found</h1>", status=404, content_type="text/html")


@app.route("/api/health")
def health():
    return jsonify({"status": "ok", "timestamp": datetime.now().isoformat()})


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║           PRINTMAXX LIVE DASHBOARD SERVER                    ║
║                                                              ║
║   URL:  http://localhost:{PORT}                               ║
║   API:  http://localhost:{PORT}/api/status                    ║
║   Root: {str(PROJECT_ROOT)[:50]}   ║
║                                                              ║
║   Auto-refresh: 30 seconds                                   ║
║   Press Ctrl+C to stop                                       ║
╚══════════════════════════════════════════════════════════════╝
""")

    # Open browser after short delay
    def open_browser():
        time.sleep(1.5)
        webbrowser.open(f"http://localhost:{PORT}")

    threading.Thread(target=open_browser, daemon=True).start()

    app.run(host="0.0.0.0", port=PORT, debug=False)
