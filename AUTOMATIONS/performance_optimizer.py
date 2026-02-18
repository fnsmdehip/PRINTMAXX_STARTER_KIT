#!/usr/bin/env python3
"""
PRINTMAXX Performance Optimizer — System Health + Bottleneck Detector + Funnel Analysis
========================================================================================
Monitors every script, diagnoses failures, optimizes scheduling, detects bottlenecks,
tracks historical trends, and analyzes conversion funnels.

Usage:
  python3 AUTOMATIONS/performance_optimizer.py --health       System health dashboard
  python3 AUTOMATIONS/performance_optimizer.py --bottlenecks  Find conversion bottlenecks
  python3 AUTOMATIONS/performance_optimizer.py --optimize     Optimization recommendations
  python3 AUTOMATIONS/performance_optimizer.py --funnel       Conversion funnel analysis
  python3 AUTOMATIONS/performance_optimizer.py --history      Historical trend analysis
  python3 AUTOMATIONS/performance_optimizer.py --full         All of the above

Data Sources:
  - AUTOMATIONS/logs/overnight_status_*.json (per-run script results)
  - AUTOMATIONS/logs/*.log (execution logs)
  - LEDGER/REVENUE_STREAMS_TRACKER.csv
  - LEDGER/FREELANCE_PIPELINE.csv
  - AUTOMATIONS/leads/*.csv (lead data)
  - AUTOMATIONS/outreach/*.csv (outreach data)

Output:
  - LEDGER/SYSTEM_HEALTH.json (machine-readable snapshot)
  - LEDGER/OPTIMIZATION_RECOMMENDATIONS.md (human-readable)
"""

import argparse
import csv
import glob
import json
import os
import re
import subprocess
import sys
from collections import defaultdict
from datetime import datetime, timedelta
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
AUTOMATIONS = BASE / "AUTOMATIONS"
LOGS = AUTOMATIONS / "logs"
LEADS_DIR = AUTOMATIONS / "leads"
OUTREACH_DIR = AUTOMATIONS / "outreach"
LEDGER = BASE / "LEDGER"
OPS = BASE / "OPS"

TODAY = datetime.now().strftime("%Y-%m-%d")
NOW = datetime.now()

HEALTH_OUTPUT = LEDGER / "SYSTEM_HEALTH.json"
RECOMMENDATIONS_OUTPUT = LEDGER / "OPTIMIZATION_RECOMMENDATIONS.md"

# Critical scripts (failures are high-priority)
CRITICAL_SCRIPTS = {
    "alpha_screening", "ecom_arb_scanner", "daily_nocost_rbi_scanner",
    "signal_aggregation", "ops_orchestrator",
}


# ============================================================
# DATA LOADING
# ============================================================

def load_all_status_files():
    """Load all overnight status JSON-lines files, sorted by date."""
    pattern = str(LOGS / "overnight_status_*.json")
    status_files = sorted(glob.glob(pattern))
    all_entries = []

    for filepath in status_files:
        date_match = re.search(r"overnight_status_(\d{4}-\d{2}-\d{2})\.json", filepath)
        if not date_match:
            continue
        run_date = date_match.group(1)

        try:
            with open(filepath, "r") as f:
                for line in f:
                    line = line.strip()
                    if not line or line == "[]":
                        continue
                    try:
                        entry = json.loads(line)
                        entry["run_date"] = run_date
                        all_entries.append(entry)
                    except json.JSONDecodeError:
                        continue
        except IOError:
            continue

    return all_entries


def load_lead_files():
    """Load metadata about lead CSV files."""
    lead_files = []
    if LEADS_DIR.exists():
        for f in LEADS_DIR.glob("*.csv"):
            try:
                stat = f.stat()
                with open(f, "r") as fh:
                    rows = sum(1 for _ in fh) - 1
                lead_files.append({
                    "file": f.name,
                    "rows": max(0, rows),
                    "size_kb": round(stat.st_size / 1024, 1),
                    "modified": datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d"),
                })
            except Exception:
                continue
    return lead_files


def load_outreach_files():
    """Load metadata about outreach CSV files."""
    outreach_files = []
    if OUTREACH_DIR.exists():
        for f in OUTREACH_DIR.glob("*.csv"):
            try:
                stat = f.stat()
                with open(f, "r") as fh:
                    rows = sum(1 for _ in fh) - 1
                outreach_files.append({
                    "file": f.name,
                    "rows": max(0, rows),
                    "size_kb": round(stat.st_size / 1024, 1),
                    "modified": datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d"),
                })
            except Exception:
                continue
    return outreach_files


def load_revenue_streams():
    """Load revenue streams tracker."""
    tracker = LEDGER / "REVENUE_STREAMS_TRACKER.csv"
    if not tracker.exists():
        return []
    try:
        with open(tracker, "r") as f:
            return list(csv.DictReader(f))
    except Exception:
        return []


def load_freelance_pipeline():
    """Load freelance pipeline."""
    pipeline = LEDGER / "FREELANCE_PIPELINE.csv"
    if not pipeline.exists():
        return []
    try:
        with open(pipeline, "r") as f:
            return list(csv.DictReader(f))
    except Exception:
        return []


def get_log_disk_usage():
    """Calculate total disk usage of log files in MB."""
    total = 0
    if LOGS.exists():
        for f in LOGS.iterdir():
            if f.is_file():
                total += f.stat().st_size
    return round(total / (1024 * 1024), 2)


def get_crontab_entries():
    """Parse current crontab."""
    try:
        result = subprocess.run(["crontab", "-l"], capture_output=True, text=True, timeout=10)
        lines = [l.strip() for l in result.stdout.splitlines()
                 if l.strip() and not l.strip().startswith("#")]
        entries = []
        for line in lines:
            parts = line.split(None, 5)
            if len(parts) >= 6:
                entries.append({"schedule": " ".join(parts[:5]), "command": parts[5], "raw": line})
        return entries
    except Exception:
        return []


# ============================================================
# SECTION 1: SYSTEM HEALTH
# ============================================================

def analyze_script_health(entries, days=7):
    """Analyze per-script health from status entries."""
    cutoff = (NOW - timedelta(days=days)).strftime("%Y-%m-%d")
    recent = [e for e in entries if e.get("run_date", "") >= cutoff]

    script_stats = defaultdict(lambda: {
        "total": 0, "success": 0, "failed": 0, "timeout": 0,
        "last_status": "", "last_run": "",
    })

    for entry in recent:
        name = entry.get("script", "unknown")
        status = entry.get("status", "UNKNOWN")
        run_date = entry.get("run_date", "")

        stats = script_stats[name]
        stats["total"] += 1
        stats["last_run"] = run_date

        if status == "SUCCESS":
            stats["success"] += 1
            stats["last_status"] = "OK"
        elif status == "FAILED":
            stats["failed"] += 1
            stats["last_status"] = "FAIL"
        elif status == "TIMEOUT":
            stats["timeout"] += 1
            stats["last_status"] = "T/O"

    results = {}
    for name, stats in script_stats.items():
        total = stats["total"]
        success_rate = (stats["success"] / total * 100) if total > 0 else 0
        timeout_rate = (stats["timeout"] / total * 100) if total > 0 else 0
        fail_rate = (stats["failed"] / total * 100) if total > 0 else 0

        # Trend: compare first half vs second half
        trend = "STABLE"
        if total >= 4:
            entries_for = [e for e in recent if e.get("script") == name]
            mid = len(entries_for) // 2
            first_rate = sum(1 for e in entries_for[:mid] if e.get("status") == "SUCCESS") / max(mid, 1)
            second_rate = sum(1 for e in entries_for[mid:] if e.get("status") == "SUCCESS") / max(len(entries_for) - mid, 1)
            if second_rate < first_rate - 0.2:
                trend = "DEGRADING"
            elif second_rate > first_rate + 0.2:
                trend = "IMPROVING"

        # Category
        category = "other"
        if name.startswith("leads_"):
            category = "lead_scraping"
        elif name in ("gov_tenders_refresh", "usaspending_refresh", "sam_gov_monitor",
                       "linkedin_events", "g2_reviewers", "indeed_hiring"):
            category = "lead_gen"
        elif name in ("ecom_arb_scanner", "trending_products", "viral_product_scanner",
                       "nordic_ecom", "app_clone_finder"):
            category = "ecom"
        elif name in ("signal_aggregation", "ops_orchestrator", "performance_health", "brain_heal"):
            category = "brain"
        elif name in ("daily_nocost_rbi_scanner", "platform_meta_monitor", "niche_meta_detector",
                       "viral_content_scanner", "alpha_screening", "alpha_validator",
                       "platform_algo_detection", "hashtag_audio_tracking", "platform_rpm_tracking",
                       "creator_program_monitoring", "aso_keyword_research", "run_all_research_ops"):
            category = "research"

        results[name] = {
            "total_runs": total,
            "success_rate": round(success_rate, 1),
            "timeout_rate": round(timeout_rate, 1),
            "fail_rate": round(fail_rate, 1),
            "trend": trend,
            "category": category,
            "last_status": stats["last_status"],
            "last_run": stats["last_run"],
            "is_critical": name in CRITICAL_SCRIPTS,
        }

    return results


def check_data_freshness():
    """Check how fresh data sources are."""
    sources = {
        "Freelance demand": LEDGER / "FREELANCE_DEMAND_SCAN.csv",
        "Ecom arb": LEDGER / "ECOM_ARB_OPPORTUNITIES.csv",
        "Trend signals": LEDGER / "TREND_SIGNALS.csv",
        "Alpha staging": LEDGER / "ALPHA_STAGING.csv",
        "Fused signals": LEDGER / "FUSED_SIGNALS.csv",
        "Pipeline tracker": OUTREACH_DIR / "PIPELINE_TRACKER.csv",
        "Revenue streams": LEDGER / "REVENUE_STREAMS_TRACKER.csv",
        "System health": HEALTH_OUTPUT,
    }
    results = []
    for name, path in sources.items():
        if path.exists():
            mtime = datetime.fromtimestamp(path.stat().st_mtime)
            age = (NOW - mtime).total_seconds() / 3600
            rows = 0
            if path.suffix == ".csv":
                try:
                    with open(path) as f:
                        rows = sum(1 for _ in f) - 1
                except Exception:
                    pass
            results.append({
                "name": name, "age_hours": round(age, 1),
                "rows": rows, "status": "FRESH" if age < 12 else "AGING" if age < 48 else "STALE",
            })
        else:
            results.append({"name": name, "age_hours": -1, "rows": 0, "status": "MISSING"})
    return results


def cmd_health(entries, days=7):
    """Full system health dashboard."""
    print("=" * 78)
    print(f"  PRINTMAXX SYSTEM HEALTH DASHBOARD")
    print(f"  Generated: {NOW.strftime('%Y-%m-%d %H:%M')} | Window: {days} days")
    print("=" * 78)

    health = analyze_script_health(entries, days=days)

    # Overall counts
    dates = sorted(set(e.get("run_date", "") for e in entries if e.get("run_date")))
    total_scripts = len(health)
    healthy = sum(1 for s in health.values() if s["success_rate"] >= 80)
    degrading = sum(1 for s in health.values() if s["trend"] == "DEGRADING")
    failing = sum(1 for s in health.values() if s["success_rate"] < 50)

    print(f"\n  Overnight runs analyzed: {len(dates)} days")
    print(f"  Scripts tracked: {total_scripts}")
    print(f"  Healthy (>80%%): {healthy}/{total_scripts}")
    print(f"  Degrading trend: {degrading}")
    print(f"  Failing (<50%%): {failing}")
    print(f"  Log disk usage: {get_log_disk_usage()} MB")

    # Script inventory
    py_count = sum(1 for f in AUTOMATIONS.glob("*.py")) if AUTOMATIONS.exists() else 0
    print(f"  Python scripts: {py_count}")

    # Data freshness
    print(f"\n  Data source freshness:")
    for s in check_data_freshness():
        icon = {"FRESH": "OK", "AGING": "!!", "STALE": "XX", "MISSING": "--"}[s["status"]]
        age_str = f"{s['age_hours']:.0f}h" if s['age_hours'] >= 0 else "N/A"
        print(f"    [{icon}] {s['name']:25s} {s['rows']:>5d} rows  {age_str:>6s} old")

    # Cron
    cron_entries = get_crontab_entries()
    print(f"\n  Cron jobs installed: {len(cron_entries)}")

    # Lead pipeline
    total_leads = 0
    if LEADS_DIR.exists():
        for f in LEADS_DIR.glob("*.csv"):
            try:
                with open(f) as fh:
                    total_leads += sum(1 for _ in fh) - 1
            except Exception:
                pass
    print(f"  Leads in pipeline: {total_leads:,}")

    # Per-category breakdown
    categories = defaultdict(list)
    for name, stats in health.items():
        categories[stats["category"]].append((name, stats))

    for cat in ["research", "lead_gen", "lead_scraping", "ecom", "brain", "other"]:
        scripts = categories.get(cat, [])
        if not scripts:
            continue

        print(f"\n  --- {cat.upper().replace('_', ' ')} ({len(scripts)} scripts) ---")
        print(f"  {'Script':<40} {'Rate':>6} {'Trend':>10} {'Last':>5} {'Runs':>5}")
        print(f"  {'-'*40} {'-'*6} {'-'*10} {'-'*5} {'-'*5}")

        scripts.sort(key=lambda x: x[1]["success_rate"])
        for name, stats in scripts:
            rate = f"{stats['success_rate']:.0f}%"
            trend = stats["trend"]
            last = stats["last_status"]
            runs = str(stats["total_runs"])
            crit = "!!" if stats["is_critical"] and stats["success_rate"] < 80 else ""
            display = name[:39]
            print(f"  {crit:>2}{display:<38} {rate:>6} {trend:>10} {last:>5} {runs:>5}")

    # Alerts
    alerts = []
    for name, stats in health.items():
        if stats["is_critical"] and stats["success_rate"] < 80:
            alerts.append(f"CRITICAL: {name} at {stats['success_rate']:.0f}%")
        if stats["trend"] == "DEGRADING" and stats["success_rate"] < 70:
            alerts.append(f"DEGRADING: {name} now {stats['success_rate']:.0f}%")

    if alerts:
        print(f"\n  {'='*40}")
        print(f"  ALERTS ({len(alerts)})")
        print(f"  {'='*40}")
        for a in alerts:
            print(f"  >> {a}")

    # Health score
    score = 0
    fresh_count = sum(1 for s in check_data_freshness() if s["status"] == "FRESH")
    score += min(25, fresh_count * 5)
    score += min(20, len(cron_entries))
    score += min(20, healthy * 2)
    score += min(15, py_count // 5)
    score += min(10, total_leads // 500)
    score += min(10, 10 if failing == 0 else 0)

    grade = "A+" if score >= 90 else "A" if score >= 80 else "B" if score >= 70 else "C" if score >= 60 else "D" if score >= 50 else "F"
    print(f"\n  {'='*50}")
    print(f"  OVERALL HEALTH SCORE: {score}/100 ({grade})")
    print(f"  {'='*50}")

    print()
    return health, score


# ============================================================
# SECTION 2: BOTTLENECK ANALYSIS
# ============================================================

def cmd_bottlenecks(entries, leads, outreach, revenue_streams, freelance):
    """Find conversion bottlenecks across the pipeline."""
    print("=" * 78)
    print("  CONVERSION FUNNEL BOTTLENECK ANALYSIS")
    print("=" * 78)

    bottlenecks = []

    # Compute funnel stages
    dates_7d = [(NOW - timedelta(days=i)).strftime("%Y-%m-%d") for i in range(7)]
    success_per_day = defaultdict(int)
    for e in entries:
        if e.get("status") == "SUCCESS" and e.get("run_date", "") in dates_7d:
            success_per_day[e["run_date"]] += 1
    avg_signals = sum(success_per_day.values()) / max(len(dates_7d), 1)

    stages = {
        "signal_discovery": {
            "metric": "Successful script runs/day",
            "value": round(avg_signals, 1), "target": 30,
        },
        "lead_generation": {
            "metric": "Total leads in pipeline",
            "value": sum(f.get("rows", 0) for f in leads), "target": 2000,
        },
        "outreach_volume": {
            "metric": "Emails in outreach pipeline",
            "value": sum(f.get("rows", 0) for f in outreach), "target": 1000,
        },
        "active_pipeline": {
            "metric": "Active pipeline items",
            "value": sum(1 for p in freelance
                         if p.get("status", "").lower() in ("active", "applied", "in_progress", "contacted")),
            "target": 20,
        },
        "revenue_streams": {
            "metric": "Active revenue streams",
            "value": sum(1 for r in revenue_streams
                         if r.get("status", "").lower() in ("active", "live", "earning")),
            "target": 5,
        },
    }

    # Find worst
    worst = None
    worst_gap = 0
    for stage, data in stages.items():
        gap = (data["target"] - data["value"]) / max(data["target"], 1)
        health = "GREEN" if gap <= 0.2 else "YELLOW" if gap <= 0.5 else "RED"
        data["health"] = health
        if gap > worst_gap:
            worst_gap = gap
            worst = stage

    # Account creation check
    accounts_file = LEDGER / "ACCOUNTS.csv"
    active_accounts = 0
    total_accounts = 0
    if accounts_file.exists():
        try:
            with open(accounts_file) as f:
                reader = csv.DictReader(f)
                for row in reader:
                    total_accounts += 1
                    if row.get("status", "").lower() in ("active", "live", "verified"):
                        active_accounts += 1
        except Exception:
            pass

    if active_accounts < 5:
        bottlenecks.append({
            "severity": "CRITICAL", "area": "Account Creation",
            "detail": f"Only {active_accounts}/{total_accounts} accounts active. Cannot list products.",
            "fix": "Follow OPS/ACCOUNT_CREATION_NOW.md",
            "revenue_blocked": "$2,500-13,500/mo",
        })

    # Email sending check
    emails_ready = sum(f.get("rows", 0) for f in outreach)
    if emails_ready > 100:
        bottlenecks.append({
            "severity": "HIGH", "area": "Cold Email Sending",
            "detail": f"{emails_ready:,} emails generated, likely 0 sent (no sending infra).",
            "fix": "Setup burner domain + warmup 2 weeks + email_sender.py",
            "revenue_blocked": "$1,000-5,000/mo",
        })

    # Product listing check
    products_dir = BASE / "PRODUCTS"
    listings_ready = 0
    if products_dir.exists():
        for f in products_dir.rglob("*.md"):
            try:
                text = f.read_text()[:500].lower()
                if any(kw in text for kw in ("ready", "listing", "gig", "upload")):
                    listings_ready += 1
            except Exception:
                pass
    if listings_ready > 5:
        bottlenecks.append({
            "severity": "HIGH", "area": "Product Listings",
            "detail": f"{listings_ready} listings ready, 0 live (need accounts).",
            "fix": "Create platform accounts, then paste from PRODUCTS/",
            "revenue_blocked": "$200-1,000/mo",
        })

    # Display stages
    print(f"\n  Signal -> Leads -> Outreach -> Pipeline -> Revenue\n")
    stage_order = ["signal_discovery", "lead_generation", "outreach_volume",
                   "active_pipeline", "revenue_streams"]

    for stage in stage_order:
        data = stages[stage]
        val = data["value"]
        tgt = data["target"]
        health = data["health"]
        pct = min(val / max(tgt, 1), 1.0)
        bar_len = 30
        filled = int(pct * bar_len)
        bar = "#" * filled + "." * (bar_len - filled)
        icon = {"GREEN": "+", "YELLOW": "!", "RED": "X"}[health]
        indicator = ">>>" if stage == worst else "   "
        print(f"  {indicator} [{icon}] {data['metric']}")
        print(f"        [{bar}] {val}/{tgt}")
        if stage == worst:
            print(f"        ^^ BIGGEST GAP")
        print()

    # Display bottlenecks
    if bottlenecks:
        print(f"  {'='*40}")
        print(f"  BLOCKERS ({len(bottlenecks)})")
        print(f"  {'='*40}")
        for i, b in enumerate(bottlenecks, 1):
            print(f"\n  {i}. [{b['severity']}] {b['area']}")
            print(f"     {b['detail']}")
            print(f"     FIX: {b['fix']}")
            print(f"     Revenue blocked: {b['revenue_blocked']}")

    print()
    return stages, worst, bottlenecks


# ============================================================
# SECTION 3: OPTIMIZATION RECOMMENDATIONS
# ============================================================

def cmd_optimize(health, stages, worst, entries):
    """Generate optimization recommendations."""
    print("=" * 78)
    print("  OPTIMIZATION RECOMMENDATIONS")
    print("=" * 78)

    recs = []

    # 1. Fix 0% success rate scripts
    for name, stats in health.items():
        if stats["success_rate"] == 0 and stats["total_runs"] >= 2:
            pri = "P0" if stats["is_critical"] else "P1"
            recs.append({
                "priority": pri, "action": "FIX_NEEDED", "script": name,
                "reason": f"0% success over {stats['total_runs']} runs",
                "impact": "HIGH" if stats["is_critical"] else "MEDIUM", "effort": "LOW",
            })

    # 2. Fix low success scripts
    for name, stats in health.items():
        if 0 < stats["success_rate"] < 50 and stats["total_runs"] >= 2:
            recs.append({
                "priority": "P1", "action": "FIX_NEEDED", "script": name,
                "reason": f"{stats['success_rate']:.0f}% success, {stats['trend']} trend",
                "impact": "MEDIUM", "effort": "LOW",
            })

    # 3. Lead scraper batch optimization
    lead_timeouts = sum(1 for n, s in health.items()
                        if n.startswith("leads_") and s["timeout_rate"] >= 60)
    if lead_timeouts >= 5:
        recs.append({
            "priority": "P0", "action": "BATCH_OPTIMIZE", "script": "lead_scrapers",
            "reason": f"{lead_timeouts} lead scrapers timing out. Use --limit 10, rotate cities nightly",
            "impact": "HIGH", "effort": "LOW",
        })

    # 4. Degrading scripts
    for name, stats in health.items():
        if stats["trend"] == "DEGRADING" and stats["success_rate"] < 80:
            recs.append({
                "priority": "P1", "action": "INVESTIGATE", "script": name,
                "reason": f"Degrading trend, now {stats['success_rate']:.0f}%",
                "impact": "MEDIUM", "effort": "MEDIUM",
            })

    # 5. High-performing scripts to increase frequency
    for name, stats in health.items():
        if stats["success_rate"] >= 95 and stats["category"] in ("research", "lead_gen"):
            recs.append({
                "priority": "P2", "action": "INCREASE_FREQUENCY", "script": name,
                "reason": f"{stats['success_rate']:.0f}% success, high-value category",
                "impact": "MEDIUM", "effort": "LOW",
            })

    # 6. Bottleneck fix
    if worst:
        bn = stages[worst]
        recs.append({
            "priority": "P0", "action": "FIX_BOTTLENECK", "script": worst,
            "reason": f"Biggest funnel gap: {bn['metric']} at {bn['value']}/{bn['target']}",
            "impact": "CRITICAL", "effort": "VARIES",
        })

    # 7. Log cleanup
    log_mb = get_log_disk_usage()
    if log_mb > 100:
        recs.append({
            "priority": "P3", "action": "CLEANUP", "script": "logs",
            "reason": f"Log directory at {log_mb} MB. Rotate >30 days.",
            "impact": "LOW", "effort": "LOW",
        })

    # Sort by priority
    pri_order = {"P0": 0, "P1": 1, "P2": 2, "P3": 3}
    recs.sort(key=lambda r: pri_order.get(r["priority"], 99))

    # Display
    if not recs:
        print("\n  All systems nominal. No actions needed.")
    else:
        print(f"\n  {len(recs)} actions identified\n")
        print(f"  {'#':>3} {'Pri':>4} {'Action':<22} {'Script':<35} {'Impact':>8}")
        print(f"  {'-'*3} {'-'*4} {'-'*22} {'-'*35} {'-'*8}")
        for i, rec in enumerate(recs, 1):
            script = rec["script"][:34]
            print(f"  {i:>3} {rec['priority']:>4} {rec['action']:<22} {script:<35} {rec['impact']:>8}")

        print(f"\n  --- TOP 5 DETAILS ---")
        for i, rec in enumerate(recs[:5], 1):
            print(f"\n  {i}. [{rec['priority']}] {rec['action']}: {rec['script']}")
            print(f"     Reason: {rec['reason']}")
            print(f"     Impact: {rec['impact']} | Effort: {rec['effort']}")

    print()
    return recs


# ============================================================
# SECTION 4: CONVERSION FUNNEL
# ============================================================

def cmd_funnel(leads, outreach, revenue_streams, freelance):
    """Detailed conversion funnel analysis."""
    print("=" * 78)
    print("  CONVERSION FUNNEL ANALYSIS")
    print("=" * 78)

    # Lead breakdown
    industry_leads = defaultdict(int)
    city_leads = defaultdict(int)
    for f in leads:
        name_parts = f.get("file", "").replace(".csv", "").lower().split("_")
        for part in name_parts:
            if part in ("dentist", "dental", "restaurant", "plumber",
                        "lawyer", "legal", "fitness", "realtor"):
                industry_leads[part] += f.get("rows", 0)

    total_leads = sum(f.get("rows", 0) for f in leads)
    total_outreach = sum(f.get("rows", 0) for f in outreach)

    print(f"\n  STAGE 1: LEADS")
    print(f"    Total leads: {total_leads:,}")
    print(f"    Lead files: {len(leads)}")

    if industry_leads:
        print(f"    By industry:")
        for ind, count in sorted(industry_leads.items(), key=lambda x: x[1], reverse=True):
            bar = "#" * min(count // 20, 40)
            print(f"      {ind:<15} {count:>6}  {bar}")

    print(f"\n  STAGE 2: OUTREACH")
    print(f"    Emails prepared: {total_outreach:,}")
    print(f"    Outreach files: {len(outreach)}")
    if total_leads > 0:
        print(f"    Lead -> Outreach: {total_outreach / total_leads * 100:.1f}%")

    print(f"\n  STAGE 3: PIPELINE")
    pipeline_statuses = defaultdict(int)
    for p in freelance:
        pipeline_statuses[p.get("status", "unknown").lower()] += 1
    if pipeline_statuses:
        for status, count in sorted(pipeline_statuses.items(), key=lambda x: x[1], reverse=True):
            print(f"    {status:<20} {count:>5}")
    else:
        print(f"    No pipeline data")

    print(f"\n  STAGE 4: REVENUE STREAMS")
    rev_statuses = defaultdict(int)
    for r in revenue_streams:
        rev_statuses[r.get("status", "unknown").lower()] += 1
    if rev_statuses:
        for status, count in sorted(rev_statuses.items(), key=lambda x: x[1], reverse=True):
            print(f"    {status:<20} {count:>5}")
    else:
        print(f"    No revenue stream data")

    active = sum(v for k, v in rev_statuses.items() if k in ("active", "live", "earning"))
    planned = sum(v for k, v in rev_statuses.items() if k in ("planned", "ready", "pending"))
    print(f"\n  Revenue projection (at $200/stream avg):")
    print(f"    Current:      ${active * 200}/mo ({active} active)")
    print(f"    After launch: ${(active + planned) * 200}/mo (+{planned} planned)")

    print()


# ============================================================
# SECTION 5: HISTORICAL ANALYSIS
# ============================================================

def cmd_history(entries):
    """Historical trend analysis with ASCII charts."""
    print("=" * 78)
    print("  HISTORICAL PERFORMANCE TRENDS")
    print("=" * 78)

    # Group by date
    by_date = defaultdict(lambda: {"success": 0, "failed": 0, "timeout": 0, "total": 0})
    for entry in entries:
        date = entry.get("run_date", "")
        if not date:
            continue
        status = entry.get("status", "")
        by_date[date]["total"] += 1
        if status == "SUCCESS":
            by_date[date]["success"] += 1
        elif status == "FAILED":
            by_date[date]["failed"] += 1
        elif status == "TIMEOUT":
            by_date[date]["timeout"] += 1

    dates = sorted(by_date.keys())
    if not dates:
        print("\n  No historical data found.")
        return

    print(f"\n  Success Rate Over Time ({len(dates)} runs)")
    print(f"  {'Date':<12} {'Pass':>5} {'Fail':>5} {'T/O':>5} {'Total':>6} {'Rate':>6} {'Chart'}")
    print(f"  {'-'*12} {'-'*5} {'-'*5} {'-'*5} {'-'*6} {'-'*6} {'-'*30}")

    for date in dates:
        d = by_date[date]
        total = d["total"]
        rate = d["success"] / total * 100 if total > 0 else 0
        bar_len = int(rate / 100 * 30)
        bar = "#" * bar_len + "." * (30 - bar_len)
        print(f"  {date:<12} {d['success']:>5} {d['failed']:>5} {d['timeout']:>5} "
              f"{total:>6} {rate:>5.1f}% [{bar}]")

    # Trend summary
    if len(dates) >= 2:
        first = by_date[dates[0]]
        last = by_date[dates[-1]]
        first_rate = first["success"] / max(first["total"], 1) * 100
        last_rate = last["success"] / max(last["total"], 1) * 100
        diff = last_rate - first_rate
        trend = "IMPROVING" if diff > 5 else "DEGRADING" if diff < -5 else "STABLE"

        print(f"\n  Trend: {trend}")
        print(f"    First ({dates[0]}): {first_rate:.1f}%")
        print(f"    Last  ({dates[-1]}): {last_rate:.1f}%")
        print(f"    Change: {diff:+.1f}%")

    # Timeout distribution
    timeout_scripts = defaultdict(int)
    for e in entries:
        if e.get("status") == "TIMEOUT":
            timeout_scripts[e.get("script", "unknown")] += 1

    if timeout_scripts:
        print(f"\n  Top timeout offenders:")
        for name, count in sorted(timeout_scripts.items(), key=lambda x: x[1], reverse=True)[:10]:
            bar = "X" * min(count, 30)
            print(f"    {name:<40} {count:>3} [{bar}]")

    # Failure distribution
    fail_scripts = defaultdict(int)
    for e in entries:
        if e.get("status") == "FAILED":
            fail_scripts[e.get("script", "unknown")] += 1

    if fail_scripts:
        print(f"\n  Top failure offenders:")
        for name, count in sorted(fail_scripts.items(), key=lambda x: x[1], reverse=True)[:10]:
            bar = "!" * min(count, 30)
            print(f"    {name:<40} {count:>3} [{bar}]")

    print()


# ============================================================
# OUTPUT
# ============================================================

def save_outputs(health, stages, recs, funnel_data=None):
    """Save JSON health snapshot and markdown recommendations."""
    LEDGER.mkdir(parents=True, exist_ok=True)

    # Health JSON
    snapshot = {
        "generated": NOW.isoformat(),
        "scripts": health,
        "stages": stages,
    }
    with open(HEALTH_OUTPUT, "w") as f:
        json.dump(snapshot, f, indent=2, default=str)
    print(f"  Saved: {HEALTH_OUTPUT}")

    # Recommendations MD
    if recs:
        lines = [
            f"# PRINTMAXX Optimization Recommendations",
            f"",
            f"Generated: {NOW.strftime('%Y-%m-%d %H:%M')}",
            f"",
            f"## Action Items ({len(recs)} total)",
            f"",
            f"| # | Priority | Action | Script | Impact | Effort |",
            f"|---|----------|--------|--------|--------|--------|",
        ]
        for i, rec in enumerate(recs, 1):
            lines.append(f"| {i} | {rec['priority']} | {rec['action']} | "
                         f"{rec['script']} | {rec['impact']} | {rec['effort']} |")
        lines.extend(["", "## Quick Fixes (P0/P1, LOW effort)", ""])
        quick = [r for r in recs if r["priority"] in ("P0", "P1") and r["effort"] == "LOW"]
        for fix in quick[:5]:
            lines.append(f"- **{fix['script']}**: {fix['reason']}")
        lines.extend(["", "## Script Health", "", "| Script | Rate | Trend |", "|--------|------|-------|"])
        for name in sorted(health.keys()):
            s = health[name]
            lines.append(f"| {name} | {s['success_rate']:.0f}% | {s['trend']} |")
        with open(RECOMMENDATIONS_OUTPUT, "w") as f:
            f.write("\n".join(lines) + "\n")
        print(f"  Saved: {RECOMMENDATIONS_OUTPUT}")


# ============================================================
# CLI
# ============================================================

def main():
    parser = argparse.ArgumentParser(
        description="PRINTMAXX Performance Optimizer",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--health", action="store_true", help="System health dashboard")
    parser.add_argument("--bottlenecks", action="store_true", help="Find conversion bottlenecks")
    parser.add_argument("--optimize", action="store_true", help="Optimization recommendations")
    parser.add_argument("--funnel", action="store_true", help="Conversion funnel analysis")
    parser.add_argument("--history", action="store_true", help="Historical trend analysis")
    parser.add_argument("--full", action="store_true", help="Run all analyses")
    parser.add_argument("--days", type=int, default=7, help="Analysis window in days (default: 7)")
    parser.add_argument("--json", action="store_true", help="JSON output to stdout")

    args = parser.parse_args()

    # Default to --health if nothing specified
    if not any([args.health, args.bottlenecks, args.optimize, args.funnel, args.history, args.full]):
        args.health = True

    if args.full:
        args.health = args.bottlenecks = args.optimize = args.funnel = args.history = True

    # Load all data
    entries = load_all_status_files()
    if not entries:
        print("No overnight status files found in AUTOMATIONS/logs/")
        print("Run: bash AUTOMATIONS/overnight_master_runner.sh")
        sys.exit(0)

    leads = load_lead_files()
    outreach = load_outreach_files()
    revenue_streams = load_revenue_streams()
    freelance = load_freelance_pipeline()

    # Pre-analyze (shared across commands)
    health = analyze_script_health(entries, days=args.days)

    if args.json:
        stages_data = {}
        output = {"health": health}
        print(json.dumps(output, indent=2, default=str))
        return

    # Execute requested analyses
    stages = {}
    worst = None
    recs = []
    score = 0

    if args.health:
        health, score = cmd_health(entries, days=args.days)

    if args.bottlenecks:
        stages, worst, _ = cmd_bottlenecks(entries, leads, outreach, revenue_streams, freelance)

    if args.optimize:
        if not stages:
            stages_simple = {}
            for stage_name in ["signal_discovery", "lead_generation", "outreach_volume",
                               "active_pipeline", "revenue_streams"]:
                stages_simple[stage_name] = {"metric": stage_name, "value": 0, "target": 10}
            # Re-run bottleneck to get stages
            stages, worst, _ = cmd_bottlenecks(entries, leads, outreach, revenue_streams, freelance)
        recs = cmd_optimize(health, stages, worst, entries)

    if args.funnel:
        cmd_funnel(leads, outreach, revenue_streams, freelance)

    if args.history:
        cmd_history(entries)

    # Save outputs
    save_outputs(health, stages, recs)


if __name__ == "__main__":
    main()
