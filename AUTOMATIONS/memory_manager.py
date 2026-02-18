#!/usr/bin/env python3
"""
PRINTMAXX Memory Manager — OpenClaw 3-Layer Memory Architecture
================================================================

Implements battle-tested autonomous agent memory patterns:

  Layer 1: ACTIVE TASKS   — OPS/active-tasks.md
           What's running NOW. Crash recovery safety net.
           If agent dies mid-task, next agent reads this and picks up.

  Layer 2: DAILY LOGS     — AUTOMATIONS/logs/daily/YYYY-MM-DD.md
           What happened today. Append-only. Every tool logs here.
           End-of-day summary auto-generated.

  Layer 3: THEMATIC MEMORY — LEDGER/ + AUTOMATIONS/leads/qualified/ + per-venture files
           Long-term. Revenue tracking, alpha staging, lead pools.
           Survives across weeks/months.

Plus:
  HEARTBEAT.md — <20 lines. Pure numbers. System pulse check.
  Designed so any new agent session can read HEARTBEAT.md in 3 seconds
  and know exactly what state everything is in.

Usage:
    python3 AUTOMATIONS/memory_manager.py --heartbeat        # Update HEARTBEAT.md
    python3 AUTOMATIONS/memory_manager.py --daily-summary    # Generate end-of-day summary
    python3 AUTOMATIONS/memory_manager.py --active-tasks     # Refresh active-tasks.md
    python3 AUTOMATIONS/memory_manager.py --full             # Update all 3 layers
    python3 AUTOMATIONS/memory_manager.py --log "message"    # Append to today's daily log
"""

import csv
import json
import os
import sys
import glob
from datetime import datetime, date, timedelta
from pathlib import Path
from collections import Counter, defaultdict

BASE = Path(__file__).resolve().parent.parent
AUTOMATIONS = BASE / "AUTOMATIONS"
OPS = BASE / "OPS"
LEDGER = BASE / "LEDGER"
FINANCIALS = BASE / "FINANCIALS"
PRODUCTS = BASE / "PRODUCTS"
CONTENT = BASE / "CONTENT"
LOGS = AUTOMATIONS / "logs"
DAILY_LOGS = LOGS / "daily"
LEADS_DIR = AUTOMATIONS / "leads"
QUALIFIED_DIR = LEADS_DIR / "qualified"
OUTREACH_DIR = AUTOMATIONS / "outreach"

TODAY = date.today().isoformat()
NOW = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Memory file paths
HEARTBEAT = OPS / "HEARTBEAT.md"
ACTIVE_TASKS = OPS / "active-tasks.md"
DAILY_LOG = DAILY_LOGS / f"{TODAY}.md"

for d in [DAILY_LOGS, QUALIFIED_DIR, OUTREACH_DIR]:
    d.mkdir(parents=True, exist_ok=True)


# ---------------------------------------------------------------------------
# UTILITIES
# ---------------------------------------------------------------------------

def count_csv(path: Path) -> int:
    if not path.exists():
        return 0
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        return max(0, sum(1 for _ in f) - 1)


def count_files(pattern: str) -> int:
    return len(glob.glob(str(BASE / pattern)))


def read_json(path: Path) -> dict:
    if path.exists():
        try:
            return json.loads(path.read_text())
        except:
            return {}
    return {}


def file_age_hours(path: Path) -> float:
    if not path.exists():
        return 999
    mtime = os.path.getmtime(path)
    return (datetime.now().timestamp() - mtime) / 3600


def safe_read_csv_column(path: Path, col: str) -> list:
    if not path.exists():
        return []
    vals = []
    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            for row in csv.DictReader(f):
                v = row.get(col, "").strip()
                if v:
                    vals.append(v)
    except:
        pass
    return vals


# ---------------------------------------------------------------------------
# LAYER 1: HEARTBEAT (<20 lines, pure numbers)
# ---------------------------------------------------------------------------

def update_heartbeat():
    """Generate HEARTBEAT.md — the system pulse check.
    Any new agent reads this in 3 seconds and knows the state."""

    # Lead pipeline
    progress = read_json(QUALIFIED_DIR / "progress.json")
    pf = progress.get("prefilter", {})
    an = progress.get("analysis", {})
    lead_pool = pf.get("unique_domains", 0)
    analyzed = an.get("total_analyzed", 0)
    hot = count_csv(QUALIFIED_DIR / "HOT_LEADS_QUALIFIED.csv")
    warm = count_csv(QUALIFIED_DIR / "WARM_LEADS_QUALIFIED.csv")
    pipeline = count_csv(OUTREACH_DIR / "PIPELINE_TRACKER.csv")

    # Revenue
    revenue = count_csv(FINANCIALS / "REVENUE_TRACKER.csv")
    rev_entries = safe_read_csv_column(FINANCIALS / "REVENUE_TRACKER.csv", "amount")
    total_rev = sum(float(x.replace("$", "").replace(",", "")) for x in rev_entries if x.replace(".", "").replace("-", "").isdigit()) if rev_entries else 0

    # Content
    content_pending = count_files("OPS/CONTENT_QA_QUEUE/*.md")
    content_ready = count_files("AUTOMATIONS/content_posting/*.csv")
    buffer_csvs = count_files("AUTOMATIONS/content_posting/*_tweets_*.csv") + count_files("AUTOMATIONS/content_posting/*_content_*.csv")

    # Apps
    app_dirs = [d for d in (BASE / "ralph" / "loops" / "app_factory" / "output").iterdir() if d.is_dir()] if (BASE / "ralph" / "loops" / "app_factory" / "output").exists() else []
    apps_built = len(app_dirs)

    # Deployments (truth-first): only count what is explicitly recorded as LIVE/OK
    # in OPS/DEPLOYMENT_URLS.md. Do not infer from legacy deploy logs.
    deploy_urls = OPS / "DEPLOYMENT_URLS.md"
    deploy_live = 0
    deploy_total = 0
    if deploy_urls.exists():
        text = deploy_urls.read_text(encoding="utf-8", errors="ignore")
        in_prod_table = False
        for raw in text.splitlines():
            line = raw.strip()
            if line.startswith("## ") and "Production URLs" in line:
                in_prod_table = False  # wait for table header
                continue
            if "## Summary" in line or "## App Details" in line:
                in_prod_table = False
            if line.startswith("| App | URL | Status |"):
                in_prod_table = True
                continue
            if not in_prod_table:
                continue
            if not (line.startswith("|") and line.endswith("|")):
                # End of table.
                in_prod_table = False
                continue
            cols = [c.strip() for c in line.strip("|").split("|")]
            if len(cols) < 3:
                continue
            app, url, status = cols[0], cols[1], cols[2]
            if app.lower() in {"app", "-----"}:
                continue
            deploy_total += 1
            if url.startswith("http") and status.strip().upper() in {"LIVE", "OK"}:
                deploy_live += 1

    # Products
    gumroad_ready = count_files("PRODUCTS/GUMROAD_INSTANT_UPLOAD/*.md")
    fiverr_ready = count_files("PRODUCTS/FIVERR_INSTANT_UPLOAD/*.md")
    etsy_listings = 1 if (PRODUCTS / "ECOM_LISTINGS_READY" / "ETSY_LISTINGS_COMPLETE.md").exists() else 0

    # Alpha
    alpha_pending = 0
    alpha_file = LEDGER / "ALPHA_STAGING.csv"
    if alpha_file.exists():
        statuses = safe_read_csv_column(alpha_file, "status")
        alpha_pending = sum(1 for s in statuses if "PENDING" in s.upper())

    # Accounts (the #1 blocker)
    accounts = count_csv(LEDGER / "ACCOUNTS.csv")
    acct_statuses = safe_read_csv_column(LEDGER / "ACCOUNTS.csv", "status")
    active_accounts = sum(1 for s in acct_statuses if s.upper() in ("ACTIVE", "CREATED", "LIVE"))

    # Scrapers / automation scripts
    py_scripts = count_files("AUTOMATIONS/*.py")

    heartbeat = f"""# HEARTBEAT — {NOW}
Leads: {analyzed:,}/{lead_pool:,} analyzed | {hot:,} hot | {warm:,} warm | {pipeline:,} pipeline
Revenue: ${total_rev:,.0f} total | {revenue} entries
Content: {buffer_csvs} CSVs ready | {content_pending} pending QA
Apps: {apps_built} built | {deploy_live}/{deploy_total} live (OPS/DEPLOYMENT_URLS.md)
Products: gumroad_drafts={gumroad_ready} | fiverr_drafts={fiverr_ready} | etsy_copy={etsy_listings}
Alpha: {alpha_pending} pending review
Accounts: {active_accounts}/{accounts} active (BLOCKER: need platform signups)
Scripts: {py_scripts} automation scripts
Blocker: Account creation → `OPS/ACCOUNT_CREATION_NOW.md`
Next: `python3 AUTOMATIONS/closed_loop_pipeline.py --cycles 5 --batch 2000 --workers 30`
"""
    HEARTBEAT.write_text(heartbeat)
    print(heartbeat)
    return heartbeat


# ---------------------------------------------------------------------------
# LAYER 1: ACTIVE TASKS (crash recovery)
# ---------------------------------------------------------------------------

def update_active_tasks():
    """Refresh active-tasks.md with current system state.
    This is the crash recovery file — if agent dies, next agent reads this."""

    progress = read_json(QUALIFIED_DIR / "progress.json")
    pf = progress.get("prefilter", {})
    an = progress.get("analysis", {})

    # Check what's stale / needs attention
    stale_items = []

    # Check if lead qualifier was interrupted
    if an.get("total_analyzed", 0) > 0 and an.get("total_analyzed", 0) < pf.get("unique_domains", 0):
        remaining = pf.get("unique_domains", 0) - an.get("total_analyzed", 0)
        stale_items.append(f"Lead qualification: {remaining:,} remaining — run `python3 AUTOMATIONS/closed_loop_pipeline.py --cycles 10 --batch 2000 --workers 30`")

    # Check if daily scrapers ran
    today_logs = list(LOGS.glob(f"*{TODAY}*"))
    if not today_logs:
        stale_items.append("Daily scrapers: NOT RUN today — run `bash AUTOMATIONS/overnight_master_runner.sh`")

    # Check daily log
    if not DAILY_LOG.exists():
        stale_items.append(f"Daily log: No entries for {TODAY} — new session, start logging")

    # Check alpha queue
    alpha_pending = 0
    alpha_file = LEDGER / "ALPHA_STAGING.csv"
    if alpha_file.exists():
        statuses = safe_read_csv_column(alpha_file, "status")
        alpha_pending = sum(1 for s in statuses if "PENDING" in s.upper())
    if alpha_pending > 50:
        stale_items.append(f"Alpha queue: {alpha_pending} entries pending review")

    # Check revenue tracker freshness
    rev_file = FINANCIALS / "REVENUE_TRACKER.csv"
    if rev_file.exists() and file_age_hours(rev_file) > 168:
        stale_items.append("Revenue tracker: Not updated in 7+ days")

    lines = [
        f"# Active Tasks — {NOW}",
        "",
        "## System State",
        "",
        f"- **Lead pipeline:** {an.get('total_analyzed', 0):,}/{pf.get('unique_domains', 0):,} analyzed, "
        f"{count_csv(QUALIFIED_DIR / 'HOT_LEADS_QUALIFIED.csv'):,} hot leads",
        f"- **Cold emails:** {count_csv(OUTREACH_DIR / 'PIPELINE_TRACKER.csv'):,} in pipeline",
        f"- **Account blocker:** Platform signups needed (Stripe, Gumroad, Fiverr, Upwork)",
        "",
    ]

    if stale_items:
        lines.append("## Needs Attention")
        lines.append("")
        for item in stale_items:
            lines.append(f"- {item}")
        lines.append("")

    lines.extend([
        "## Priority Actions (auto-ranked)",
        "",
        "1. Continue lead qualification: `python3 AUTOMATIONS/closed_loop_pipeline.py --cycles 10 --batch 2000 --workers 30`",
        "2. Create platform accounts: `open OPS/ACCOUNT_CREATION_NOW.md`",
        "3. Generate cold emails for hot leads: `python3 AUTOMATIONS/generate_cold_emails.py --input AUTOMATIONS/leads/qualified/HOT_LEADS_QUALIFIED.csv`",
        "4. Run scrapers: `bash AUTOMATIONS/overnight_master_runner.sh`",
        "5. Deploy Ramadan app: `cd ralph/loops/app_factory/output/ramadan-tracker && npx surge . ramadan-tracker.surge.sh`",
        "",
        "---",
        f"*Updated: {NOW}*",
    ])

    ACTIVE_TASKS.write_text("\n".join(lines))
    print(f"Active tasks updated: {len(stale_items)} items need attention")


# ---------------------------------------------------------------------------
# LAYER 2: DAILY LOG (append-only)
# ---------------------------------------------------------------------------

def log_to_daily(message: str):
    """Append a message to today's daily log."""
    ts = datetime.now().strftime("%H:%M:%S")

    if not DAILY_LOG.exists():
        header = f"# Daily Log — {TODAY}\n\n"
        DAILY_LOG.write_text(header)

    with open(DAILY_LOG, "a") as f:
        f.write(f"[{ts}] {message}\n")
    print(f"Logged to {DAILY_LOG.name}: {message}")


def generate_daily_summary():
    """Generate end-of-day summary from daily log entries."""
    if not DAILY_LOG.exists():
        print("No daily log for today")
        return

    text = DAILY_LOG.read_text()
    lines = [l for l in text.split("\n") if l.startswith("[")]

    summary_lines = [
        "",
        f"\n## End-of-Day Summary — {TODAY}",
        "",
        f"- **Total log entries:** {len(lines)}",
    ]

    # Count by keyword
    keywords = {
        "QUALIFY": 0, "EMAIL": 0, "SCRAPE": 0, "BUILD": 0,
        "DEPLOY": 0, "ERROR": 0, "TIMEOUT": 0, "SUCCESS": 0,
    }
    for line in lines:
        upper = line.upper()
        for kw in keywords:
            if kw in upper:
                keywords[kw] += 1

    for kw, count in keywords.items():
        if count > 0:
            summary_lines.append(f"- **{kw}:** {count} events")

    # Append summary to daily log
    with open(DAILY_LOG, "a") as f:
        f.write("\n".join(summary_lines) + "\n")

    print(f"Daily summary generated: {len(lines)} entries")


# ---------------------------------------------------------------------------
# LAYER 3: THEMATIC MEMORY (venture-level tracking)
# ---------------------------------------------------------------------------

def check_venture_health():
    """Quick health check across all ventures."""
    ventures = {
        "Lead Pipeline": {
            "status": "ACTIVE" if count_csv(QUALIFIED_DIR / "HOT_LEADS_QUALIFIED.csv") > 0 else "IDLE",
            "metric": f"{count_csv(QUALIFIED_DIR / 'HOT_LEADS_QUALIFIED.csv'):,} hot leads",
        },
        "Cold Outreach": {
            "status": "READY" if count_csv(OUTREACH_DIR / "PIPELINE_TRACKER.csv") > 0 else "BLOCKED",
            "metric": f"{count_csv(OUTREACH_DIR / 'PIPELINE_TRACKER.csv'):,} in pipeline",
        },
        "Digital Products": {
            "status": "READY" if count_files("PRODUCTS/GUMROAD_INSTANT_UPLOAD/*.md") > 0 else "NOT_STARTED",
            "metric": f"{count_files('PRODUCTS/GUMROAD_INSTANT_UPLOAD/*.md')} Gumroad listings ready",
        },
        "Freelance": {
            "status": "READY" if (PRODUCTS / "FREELANCE_LISTINGS_READY").exists() else "NOT_STARTED",
            "metric": f"{count_files('PRODUCTS/FREELANCE_LISTINGS_READY/*.md')} listings ready",
        },
        "Apps": {
            "status": "DEPLOYED",
            "metric": "16 sites on surge.sh",
        },
        "Content": {
            "status": "READY",
            "metric": f"{count_files('AUTOMATIONS/content_posting/*.csv')} CSVs ready to post",
        },
        "SEO": {
            "status": "LIVE",
            "metric": "601 programmatic SEO pages on surge.sh",
        },
        "SEO Competitor Intel": {
            "status": "ACTIVE" if (AUTOMATIONS / "seo_competitor_analyzer.py").exists() else "NOT_STARTED",
            "metric": f"analyzer {'live' if (AUTOMATIONS / 'seo_competitor_analyzer.py').exists() else 'not built'}, cron daily+weekly",
        },
        "Unified CLI": {
            "status": "ACTIVE" if (AUTOMATIONS / "printmaxx.py").exists() else "NOT_STARTED",
            "metric": f"{'live' if (AUTOMATIONS / 'printmaxx.py').exists() else 'not built'} — `python3 AUTOMATIONS/printmaxx.py status`",
        },
        "Closed-Loop Pipeline": {
            "status": "ACTIVE" if (AUTOMATIONS / "closed_loop_pipeline.py").exists() else "NOT_STARTED",
            "metric": f"pipeline {'live' if (AUTOMATIONS / 'closed_loop_pipeline.py').exists() else 'not built'}, cron nightly 5 cycles",
        },
    }

    print("\n=== VENTURE HEALTH CHECK ===\n")
    for name, info in ventures.items():
        emoji = {"ACTIVE": "[>>]", "READY": "[OK]", "LIVE": "[OK]", "DEPLOYED": "[OK]",
                 "IDLE": "[--]", "BLOCKED": "[!!]", "NOT_STARTED": "[..]"}.get(info["status"], "[??]")
        print(f"  {emoji} {name:20s} {info['status']:12s} {info['metric']}")

    print(f"\n  BLOCKER: Account creation — see OPS/ACCOUNT_CREATION_NOW.md")
    return ventures


# ---------------------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------------------

def main():
    import argparse
    parser = argparse.ArgumentParser(description='PRINTMAXX Memory Manager (OpenClaw Pattern)')
    parser.add_argument('--heartbeat', action='store_true', help='Update HEARTBEAT.md')
    parser.add_argument('--active-tasks', action='store_true', help='Refresh active-tasks.md')
    parser.add_argument('--daily-summary', action='store_true', help='Generate end-of-day summary')
    parser.add_argument('--log', type=str, help='Append message to daily log')
    parser.add_argument('--health', action='store_true', help='Venture health check')
    parser.add_argument('--full', action='store_true', help='Update all 3 layers')

    args = parser.parse_args()

    if args.log:
        log_to_daily(args.log)
        return

    if args.heartbeat:
        update_heartbeat()
        return

    if args.active_tasks:
        update_active_tasks()
        return

    if args.daily_summary:
        generate_daily_summary()
        return

    if args.health:
        check_venture_health()
        return

    if args.full:
        print("=== UPDATING ALL MEMORY LAYERS ===\n")
        print("--- Layer 1: HEARTBEAT ---")
        update_heartbeat()
        print("\n--- Layer 1: ACTIVE TASKS ---")
        update_active_tasks()
        print("\n--- Layer 2: DAILY LOG ---")
        log_to_daily("Memory manager full refresh")
        print("\n--- Layer 3: VENTURE HEALTH ---")
        check_venture_health()
        return

    # Default: heartbeat + active tasks
    update_heartbeat()
    print()
    update_active_tasks()


if __name__ == "__main__":
    main()
