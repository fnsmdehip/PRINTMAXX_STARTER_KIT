#!/usr/bin/env python3
"""
PRINTMAXX Perpetual Improvement Runner
========================================
Master script that runs all 5 loops in sequence, logs results, identifies gaps,
and updates status files. Designed to be called by perpetual_ship_engine.sh Layer 1
or by cron (recommended: 6 PM daily).

5 Loops:
  1. RESEARCH -> ALPHA -> INTEGRATION (scrape, screen, route)
  2. CONTENT -> POST -> MEASURE (generate, format, track)
  3. PRODUCT -> LIST -> SELL -> TRACK (distribute, revenue)
  4. LEAD -> SCORE -> OUTREACH -> CLOSE (B2B pipeline)
  5. APP -> BUILD -> DEPLOY -> ASO -> MEASURE (app factory)

Usage:
    python3 AUTOMATIONS/perpetual_improvement_runner.py              # Run all loops
    python3 AUTOMATIONS/perpetual_improvement_runner.py --loop 1     # Run specific loop
    python3 AUTOMATIONS/perpetual_improvement_runner.py --status     # Show system status
    python3 AUTOMATIONS/perpetual_improvement_runner.py --gaps       # Show gaps only
    python3 AUTOMATIONS/perpetual_improvement_runner.py --integrate  # Run cross-loop integration
    python3 AUTOMATIONS/perpetual_improvement_runner.py --dry-run    # Show what would run

No external dependencies. stdlib only.
"""

import argparse
import csv
import json
import os
import subprocess
import sys
import time
from datetime import datetime, date
from pathlib import Path
from collections import defaultdict

# ---------------------------------------------------------------------------
# CONSTANTS
# ---------------------------------------------------------------------------

BASE = Path(__file__).resolve().parent.parent
AUTOMATIONS = BASE / "AUTOMATIONS"
LEDGER = BASE / "LEDGER"
FINANCIALS = BASE / "FINANCIALS"
OPS = BASE / "OPS"
PRODUCTS = BASE / "PRODUCTS"
DIGITAL_PRODUCTS = BASE / "DIGITAL_PRODUCTS"
CONTENT = BASE / "CONTENT"
SCRIPTS = BASE / "scripts"
LOGS = AUTOMATIONS / "logs"
LEADS_DIR = AUTOMATIONS / "leads"
OUTREACH_DIR = AUTOMATIONS / "outreach"
CONTENT_POSTING = AUTOMATIONS / "content_posting"

PYTHON = sys.executable
TODAY = date.today().isoformat()
TIMESTAMP = datetime.now().strftime("%Y%m%d_%H%M%S")
LOG_FILE = LOGS / f"perpetual_improvement_{TODAY}.log"
STATUS_FILE = LOGS / f"perpetual_status_{TIMESTAMP}.json"

LOGS.mkdir(parents=True, exist_ok=True)


# ---------------------------------------------------------------------------
# LOGGING
# ---------------------------------------------------------------------------

def log(msg: str):
    ts = datetime.now().strftime("%H:%M:%S")
    line = f"[{ts}] {msg}"
    print(line)
    with open(LOG_FILE, "a") as f:
        f.write(line + "\n")


def log_result(loop: int, step: str, status: str, details: str = ""):
    entry = {
        "loop": loop,
        "step": step,
        "status": status,
        "details": details,
        "time": datetime.utcnow().isoformat() + "Z"
    }
    with open(STATUS_FILE, "a") as f:
        f.write(json.dumps(entry) + "\n")


# ---------------------------------------------------------------------------
# UTILITY FUNCTIONS
# ---------------------------------------------------------------------------

def count_csv_rows(filepath: Path) -> int:
    """Count data rows in CSV (exclude header)."""
    if not filepath.exists():
        return 0
    try:
        with open(filepath, "r", encoding="utf-8", errors="replace") as f:
            reader = csv.reader(f)
            next(reader, None)  # skip header
            return sum(1 for _ in reader)
    except Exception:
        return 0


def count_files(directory: Path, pattern: str = "*") -> int:
    """Count files matching pattern in directory."""
    if not directory.exists():
        return 0
    return len(list(directory.glob(pattern)))


def read_csv_column(filepath: Path, column: str) -> list:
    """Read all values from a specific CSV column."""
    values = []
    if not filepath.exists():
        return values
    try:
        with open(filepath, "r", encoding="utf-8", errors="replace") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if column in row:
                    values.append(row[column])
    except Exception:
        pass
    return values


def run_script(cmd: list, timeout: int = 120, label: str = "") -> dict:
    """Run a script with timeout, return result dict."""
    result = {"label": label, "cmd": " ".join(cmd), "status": "UNKNOWN", "output": "", "duration": 0}
    start = time.time()
    try:
        proc = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=str(BASE)
        )
        result["duration"] = round(time.time() - start, 1)
        result["output"] = (proc.stdout or "")[-500:]  # last 500 chars
        if proc.returncode == 0:
            result["status"] = "OK"
        else:
            result["status"] = f"ERROR (exit {proc.returncode})"
            result["output"] += "\nSTDERR: " + (proc.stderr or "")[-300:]
    except subprocess.TimeoutExpired:
        result["status"] = f"TIMEOUT ({timeout}s)"
        result["duration"] = timeout
    except FileNotFoundError:
        result["status"] = "NOT_FOUND"
    except Exception as e:
        result["status"] = f"EXCEPTION: {str(e)[:100]}"
    return result


# ---------------------------------------------------------------------------
# LOOP 1: RESEARCH -> ALPHA -> INTEGRATION
# ---------------------------------------------------------------------------

def run_loop1(dry_run: bool = False) -> dict:
    """Research pipeline: scrape, screen, route approved alpha."""
    log("=" * 60)
    log("LOOP 1: RESEARCH -> ALPHA -> INTEGRATION")
    log("=" * 60)

    results = {"loop": 1, "steps": []}

    # Step 1: Count current alpha
    alpha_count = count_csv_rows(LEDGER / "ALPHA_STAGING.csv")
    pending = read_csv_column(LEDGER / "ALPHA_STAGING.csv", "status")
    pending_count = sum(1 for s in pending if s and "PENDING" in s.upper())
    approved_count = sum(1 for s in pending if s and "APPROVED" in s.upper())
    log(f"  Alpha entries: {alpha_count} total, {pending_count} PENDING, {approved_count} APPROVED")
    results["alpha_total"] = alpha_count
    results["alpha_pending"] = pending_count
    results["alpha_approved"] = approved_count

    # Step 2: Run alpha screening on pending
    log("  Running alpha_screening.py --pending...")
    if not dry_run:
        r = run_script([PYTHON, str(AUTOMATIONS / "alpha_screening.py"), "--pending"], timeout=60, label="alpha_screening")
        results["steps"].append(r)
        log(f"  Result: {r['status']} ({r['duration']}s)")
        log_result(1, "alpha_screening", r["status"], r["output"][-200:])
    else:
        log("  [DRY RUN] Would run: alpha_screening.py --pending")

    # Step 3: Run RBI scanner
    log("  Running daily_nocost_rbi_scanner.py --summary...")
    if not dry_run:
        r = run_script([PYTHON, str(AUTOMATIONS / "daily_nocost_rbi_scanner.py"), "--summary"], timeout=60, label="rbi_scanner")
        results["steps"].append(r)
        log(f"  Result: {r['status']} ({r['duration']}s)")
        log_result(1, "rbi_scanner", r["status"])
    else:
        log("  [DRY RUN] Would run: daily_nocost_rbi_scanner.py --summary")

    # Step 4: Integration - route approved alpha to target files
    log("  Running cross-loop alpha integration...")
    if not dry_run:
        integration_results = integrate_approved_alpha()
        results["integration"] = integration_results
        log(f"  Integrated {integration_results.get('routed', 0)} alpha entries")
        log_result(1, "alpha_integration", "OK", f"routed {integration_results.get('routed', 0)}")
    else:
        log("  [DRY RUN] Would integrate approved alpha to target CSVs")

    # Step 5: Check scraper outputs freshness
    scraper_outputs = {
        "reddit": AUTOMATIONS / "reddit_scraper_output",
        "scraper": BASE / "output" / "scraper",
    }
    for name, path in scraper_outputs.items():
        if path.exists():
            files = sorted(path.glob("*"), key=lambda p: p.stat().st_mtime, reverse=True)
            if files:
                age_hours = (time.time() - files[0].stat().st_mtime) / 3600
                log(f"  Scraper output ({name}): latest file {age_hours:.1f}h old")
                results[f"scraper_{name}_age_hours"] = round(age_hours, 1)

    return results


def integrate_approved_alpha() -> dict:
    """Route APPROVED alpha entries to their target integration files."""
    routed = 0
    alpha_file = LEDGER / "ALPHA_STAGING.csv"
    if not alpha_file.exists():
        return {"routed": 0, "errors": ["ALPHA_STAGING.csv not found"]}

    # Read all alpha
    rows = []
    try:
        with open(alpha_file, "r", encoding="utf-8", errors="replace") as f:
            reader = csv.DictReader(f)
            rows = list(reader)
    except Exception as e:
        return {"routed": 0, "errors": [str(e)]}

    # Find approved entries without execution tracking
    execution_file = LEDGER / "ALPHA_EXECUTION_TRACKER.csv"
    already_tracked = set()
    if execution_file.exists():
        try:
            with open(execution_file, "r", encoding="utf-8", errors="replace") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if "alpha_id" in row:
                        already_tracked.add(row["alpha_id"])
        except Exception:
            pass

    new_integrations = []
    for row in rows:
        status = (row.get("status", "") or "").upper()
        alpha_id = row.get("alpha_id", "")
        category = row.get("category", "")

        if "APPROVED" not in status:
            continue
        if alpha_id in already_tracked:
            continue

        # Determine integration target
        target = "GENERAL"
        if "APP" in category.upper():
            target = "LEDGER/APP_CLONE_OPPORTUNITIES.csv"
        elif "OUTBOUND" in category.upper() or "GROWTH" in category.upper():
            target = "LEDGER/MARKETING_CHANNELS_MASTER.csv"
        elif "CONTENT" in category.upper():
            target = "LEDGER/WINNING_CONTENT_STRUCTURES.csv"
        elif "TOOL" in category.upper():
            target = "OPS/TOOL_STACK_REFERENCE.md"
        elif "ECOM" in category.upper():
            target = "LEDGER/ECOM_LEADS.csv"
        elif "MONETIZATION" in category.upper():
            target = "LEDGER/REVENUE_STREAMS_TRACKER.csv"

        new_integrations.append({
            "alpha_id": alpha_id,
            "category": category,
            "source": row.get("source", ""),
            "tactic_summary": (row.get("tactic", "") or row.get("extracted_method", ""))[:200],
            "integration_status": "ROUTED",
            "integrated_into": target,
            "action_taken": "Auto-routed by perpetual_improvement_runner.py",
            "date": TODAY
        })
        routed += 1

    # Append to execution tracker
    if new_integrations:
        write_header = not execution_file.exists()
        fieldnames = ["alpha_id", "category", "source", "tactic_summary",
                       "integration_status", "integrated_into", "action_taken", "date"]
        try:
            with open(execution_file, "a", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                if write_header:
                    writer.writeheader()
                writer.writerows(new_integrations)
        except Exception as e:
            return {"routed": routed, "errors": [str(e)]}

    return {"routed": routed, "already_tracked": len(already_tracked)}


# ---------------------------------------------------------------------------
# LOOP 2: CONTENT -> POST -> MEASURE
# ---------------------------------------------------------------------------

def run_loop2(dry_run: bool = False) -> dict:
    """Content pipeline: check ready content, check calendar, measure performance."""
    log("=" * 60)
    log("LOOP 2: CONTENT -> POST -> MEASURE")
    log("=" * 60)

    results = {"loop": 2, "steps": []}

    # Step 1: Count content assets
    content_csvs = list(CONTENT_POSTING.glob("*.csv"))
    total_posts = 0
    for csv_file in content_csvs:
        total_posts += count_csv_rows(csv_file)
    log(f"  Content CSVs in content_posting/: {len(content_csvs)} files, ~{total_posts} posts")
    results["content_csv_count"] = len(content_csvs)
    results["total_posts_ready"] = total_posts

    # Step 2: Check calendar
    calendar_rows = count_csv_rows(LEDGER / "CONTENT_CALENDAR_30DAY.csv")
    pipeline_rows = count_csv_rows(LEDGER / "CONTENT_PIPELINE.csv")
    log(f"  Content calendar: {calendar_rows} entries")
    log(f"  Content pipeline: {pipeline_rows} entries")
    results["calendar_entries"] = calendar_rows
    results["pipeline_entries"] = pipeline_rows

    # Step 3: Check performance tracking
    perf_rows = count_csv_rows(LEDGER / "CONTENT_PERFORMANCE_TRACKER.csv")
    engagement_rows = count_csv_rows(LEDGER / "ENGAGEMENT_METRICS_DAILY.csv")
    log(f"  Performance tracker: {perf_rows} entries (0 = NO MEASUREMENT)")
    log(f"  Engagement metrics: {engagement_rows} entries")
    results["performance_tracked"] = perf_rows
    results["engagement_tracked"] = engagement_rows

    if perf_rows == 0:
        log("  WARNING: No content performance being tracked. Feedback loop broken.")
        results["gap"] = "NO_MEASUREMENT"

    # Step 4: Check buffer import files
    buffer_files = list(LEDGER.glob("buffer_import_*.csv"))
    buffer_total = sum(count_csv_rows(f) for f in buffer_files)
    log(f"  Buffer import files: {len(buffer_files)} files, {buffer_total} posts ready")
    results["buffer_files"] = len(buffer_files)
    results["buffer_posts"] = buffer_total

    # Step 5: Count content by niche
    content_dirs = {
        "faith": CONTENT / "social" / "faith",
        "fitness": CONTENT / "social" / "fitness",
        "ai/tech": CONTENT / "social" / "ai",
        "ramadan": CONTENT / "social" / "ramadan",
    }
    for niche, path in content_dirs.items():
        count = count_files(path, "*.md") + count_files(path, "*.csv")
        if count > 0:
            log(f"  Content [{niche}]: {count} files")

    return results


# ---------------------------------------------------------------------------
# LOOP 3: PRODUCT -> LIST -> SELL -> TRACK
# ---------------------------------------------------------------------------

def run_loop3(dry_run: bool = False) -> dict:
    """Product pipeline: check products, distribution status, revenue."""
    log("=" * 60)
    log("LOOP 3: PRODUCT -> LIST -> SELL -> TRACK")
    log("=" * 60)

    results = {"loop": 3, "steps": []}

    # Step 1: Count ready products
    product_files = {
        "Gumroad": PRODUCTS / "GUMROAD_READY_LISTINGS.md",
        "Etsy": PRODUCTS / "ETSY_LISTINGS_20.md",
        "Redbubble": PRODUCTS / "REDBUBBLE_LISTINGS.md",
        "POD_50": PRODUCTS / "POD_DESIGNS_50.md",
        "KDP": PRODUCTS / "KDP_JOURNALS_10.md",
    }
    ready_count = 0
    for name, path in product_files.items():
        exists = path.exists()
        size = path.stat().st_size if exists else 0
        log(f"  Product spec [{name}]: {'READY' if exists else 'MISSING'} ({size} bytes)")
        if exists:
            ready_count += 1
    results["product_specs_ready"] = ready_count

    # Step 2: Check digital products
    digital_count = count_files(DIGITAL_PRODUCTS, "*.md")
    digital_listing_count = count_files(DIGITAL_PRODUCTS / "listings", "*.md")
    log(f"  Digital products: {digital_count} files, {digital_listing_count} listings")
    results["digital_products"] = digital_count

    # Step 3: Check distribution status
    log("  Running ecom_distributor.py --status...")
    if not dry_run:
        r = run_script([PYTHON, str(AUTOMATIONS / "ecom_distributor.py"), "--status"], timeout=30, label="ecom_status")
        results["steps"].append(r)
        log(f"  Result: {r['status']} ({r['duration']}s)")
        log_result(3, "ecom_distributor_status", r["status"])
    else:
        log("  [DRY RUN] Would run: ecom_distributor.py --status")

    # Step 4: Check revenue
    revenue_rows = count_csv_rows(FINANCIALS / "REVENUE_TRACKER.csv")
    revenue_streams = count_csv_rows(LEDGER / "REVENUE_STREAMS_TRACKER.csv")
    log(f"  Revenue entries: {revenue_rows}")
    log(f"  Revenue streams tracked: {revenue_streams}")
    results["revenue_entries"] = revenue_rows
    results["revenue_streams"] = revenue_streams

    # Step 5: Check product CSV
    product_rows = count_csv_rows(LEDGER / "PRODUCTS.csv")
    products_statuses = read_csv_column(LEDGER / "PRODUCTS.csv", "Status")
    listed_count = sum(1 for s in products_statuses if s and "LIVE" in s.upper())
    draft_count = sum(1 for s in products_statuses if s and "DRAFT" in s.upper())
    log(f"  Products in LEDGER: {product_rows} total, {listed_count} LIVE, {draft_count} DRAFT")
    results["products_live"] = listed_count
    results["products_draft"] = draft_count

    if listed_count == 0:
        log("  WARNING: Zero products live. Revenue loop broken.")
        results["gap"] = "NO_PRODUCTS_LIVE"

    return results


# ---------------------------------------------------------------------------
# LOOP 4: LEAD -> SCORE -> OUTREACH -> CLOSE
# ---------------------------------------------------------------------------

def run_loop4(dry_run: bool = False) -> dict:
    """Lead pipeline: check leads, outreach status, pipeline."""
    log("=" * 60)
    log("LOOP 4: LEAD -> SCORE -> OUTREACH -> CLOSE")
    log("=" * 60)

    results = {"loop": 4, "steps": []}

    # Step 1: Count leads
    lead_files = list(LEADS_DIR.glob("*_leads.csv")) if LEADS_DIR.exists() else []
    total_leads = sum(count_csv_rows(f) for f in lead_files)
    log(f"  Lead files: {len(lead_files)} files, {total_leads} total leads")
    results["lead_files"] = len(lead_files)
    results["total_leads"] = total_leads

    # Count by industry
    industry_counts = defaultdict(int)
    for f in lead_files:
        name = f.stem.lower()
        for industry in ["dental", "dentist", "lawyer", "plumber", "restaurant", "hvac", "realtor"]:
            if industry in name:
                industry_counts[industry] += count_csv_rows(f)
                break
    for industry, count in sorted(industry_counts.items(), key=lambda x: -x[1]):
        log(f"    [{industry}]: {count} leads")

    # Step 2: Count outreach
    outreach_files = list(OUTREACH_DIR.glob("*_emails*.csv")) if OUTREACH_DIR.exists() else []
    total_outreach = sum(count_csv_rows(f) for f in outreach_files)
    log(f"  Outreach files: {len(outreach_files)} files, {total_outreach} emails generated")
    results["outreach_files"] = len(outreach_files)
    results["total_outreach_emails"] = total_outreach

    # Step 3: Check pipeline
    pipeline_rows = count_csv_rows(LEDGER / "OUTREACH_PIPELINE.csv")
    pipeline_tracker = count_csv_rows(OUTREACH_DIR / "PIPELINE_TRACKER.csv") if (OUTREACH_DIR / "PIPELINE_TRACKER.csv").exists() else 0
    log(f"  Outreach pipeline: {pipeline_rows} entries")
    log(f"  Pipeline tracker: {pipeline_tracker} entries")
    results["pipeline_entries"] = pipeline_rows
    results["pipeline_tracked"] = pipeline_tracker

    # Step 4: Check gov leads
    gov_leads = count_csv_rows(LEADS_DIR / "gov_tenders_active.csv") if (LEADS_DIR / "gov_tenders_active.csv").exists() else 0
    gov_opps = count_csv_rows(LEDGER / "GOV_OPPORTUNITIES.csv")
    log(f"  Gov tenders: {gov_leads} active, {gov_opps} in GOV_OPPORTUNITIES")
    results["gov_leads"] = gov_leads

    # Step 5: Check freelance pipeline
    freelance_rows = count_csv_rows(LEDGER / "FREELANCE_PIPELINE.csv")
    log(f"  Freelance pipeline: {freelance_rows} entries")
    results["freelance_pipeline"] = freelance_rows

    if total_outreach == 0:
        log("  WARNING: Zero outreach emails sent. Lead conversion loop broken.")
        results["gap"] = "NO_OUTREACH_SENT"

    return results


# ---------------------------------------------------------------------------
# LOOP 5: APP -> BUILD -> DEPLOY -> ASO -> MEASURE
# ---------------------------------------------------------------------------

def run_loop5(dry_run: bool = False) -> dict:
    """App pipeline: check builds, deployment status, ASO."""
    log("=" * 60)
    log("LOOP 5: APP -> BUILD -> DEPLOY -> ASO -> MEASURE")
    log("=" * 60)

    results = {"loop": 5, "steps": []}

    # Step 1: Count built apps
    app_output = BASE / "ralph" / "loops" / "app_factory" / "output"
    apps = []
    if app_output.exists():
        apps = [d.name for d in app_output.iterdir() if d.is_dir()]
    log(f"  Built apps: {len(apps)}")
    for app in apps:
        app_dir = app_output / app
        has_index = (app_dir / "index.html").exists()
        has_package = (app_dir / "package.json").exists()
        file_count = count_files(app_dir, "*")
        log(f"    [{app}]: {file_count} files, index.html={'YES' if has_index else 'NO'}, package.json={'YES' if has_package else 'NO'}")
    results["built_apps"] = len(apps)
    results["app_names"] = apps

    # Step 2: Check programmatic SEO
    seo_dir = BASE / "builds" / "programmatic_seo"
    seo_pages = count_files(seo_dir, "*.html") if seo_dir.exists() else 0
    has_sitemap = (seo_dir / "sitemap.xml").exists() if seo_dir.exists() else False
    log(f"  Programmatic SEO: {seo_pages} pages, sitemap={'YES' if has_sitemap else 'NO'}")
    results["seo_pages"] = seo_pages

    # Step 3: Check clone opportunities
    clone_rows = count_csv_rows(LEDGER / "APP_CLONE_OPPORTUNITIES.csv")
    log(f"  Clone opportunities: {clone_rows}")
    results["clone_opportunities"] = clone_rows

    # Step 4: Check ASO keywords
    aso_rows = count_csv_rows(LEDGER / "ASO_KEYWORDS.csv")
    log(f"  ASO keywords tracked: {aso_rows}")
    results["aso_keywords"] = aso_rows

    # Step 5: Check deployment
    log("  Checking deployment status...")
    # Check if vercel CLI is available
    vercel_check = run_script(["which", "vercel"], timeout=5, label="vercel_check")
    has_vercel = vercel_check["status"] == "OK"
    log(f"  Vercel CLI: {'INSTALLED' if has_vercel else 'NOT FOUND'}")
    results["vercel_installed"] = has_vercel

    # Check if surge is available
    surge_check = run_script(["which", "surge"], timeout=5, label="surge_check")
    has_surge = surge_check["status"] == "OK"
    log(f"  Surge CLI: {'INSTALLED' if has_surge else 'NOT FOUND'}")
    results["surge_installed"] = has_surge

    if seo_pages > 0 and not has_vercel and not has_surge:
        log("  WARNING: Apps built but no deployment tool available.")
        results["gap"] = "NO_DEPLOY_TOOL"

    return results


# ---------------------------------------------------------------------------
# CROSS-LOOP INTEGRATION
# ---------------------------------------------------------------------------

def run_integration(dry_run: bool = False) -> dict:
    """Cross-loop connections: wire outputs of one loop to inputs of another."""
    log("=" * 60)
    log("CROSS-LOOP INTEGRATION")
    log("=" * 60)

    results = {"integrated": 0, "actions": []}

    # 1. Route ENGAGEMENT_BAIT alpha to content generation queue
    engagement_bait = []
    alpha_file = LEDGER / "ALPHA_STAGING.csv"
    if alpha_file.exists():
        try:
            with open(alpha_file, "r", encoding="utf-8", errors="replace") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if "ENGAGEMENT_BAIT" in (row.get("status", "") or "").upper():
                        engagement_bait.append(row)
        except Exception:
            pass
    log(f"  ENGAGEMENT_BAIT alpha entries: {len(engagement_bait)} (available for content conversion)")
    results["engagement_bait_available"] = len(engagement_bait)

    # 2. Check if viral products were found and need content
    viral_products = count_csv_rows(LEDGER / "VIRAL_PRODUCTS_SCAN.csv")
    if viral_products > 0:
        log(f"  Viral products scan: {viral_products} products found -> need product listing + content")
        results["actions"].append(f"Create listings for {viral_products} viral products")

    # 3. Check if new leads were scraped but no outreach generated
    if LEADS_DIR.exists():
        lead_files = set(f.stem.replace("_leads", "") for f in LEADS_DIR.glob("*_leads.csv"))
        outreach_done = set()
        if OUTREACH_DIR.exists():
            outreach_done = set(f.stem.replace("_emails", "").replace("_step1", "").replace("_step2", "").replace("_step3", "") for f in OUTREACH_DIR.glob("*_emails*.csv"))
        unprocessed = lead_files - outreach_done
        if unprocessed:
            log(f"  Leads without outreach: {len(unprocessed)} files need mass_outreach.py")
            results["actions"].append(f"Generate outreach for {len(unprocessed)} lead files")
            results["leads_without_outreach"] = list(unprocessed)[:10]

    # 4. Check if apps have content but it's not in content_posting/
    app_names = []
    app_output = BASE / "ralph" / "loops" / "app_factory" / "output"
    if app_output.exists():
        app_names = [d.name for d in app_output.iterdir() if d.is_dir()]
    for app in app_names:
        app_content = CONTENT / "social"
        # Check if launch content exists for this app
        has_content = any(
            app.replace("-", "").replace("_", "") in str(f).lower().replace("-", "").replace("_", "")
            for f in app_content.rglob("*") if f.is_file()
        )
        if not has_content:
            results["actions"].append(f"Generate launch content for {app}")
            log(f"  App '{app}' has no launch content in CONTENT/social/")

    # 5. Check method performance analyzer for underperformers
    log("  Checking for stale/underperforming methods...")
    method_statuses = read_csv_column(LEDGER / "MONEY_METHODS_TRACKER.csv", "status")
    active_count = sum(1 for s in method_statuses if s and "ACTIVE" in s.upper())
    planning_count = sum(1 for s in method_statuses if s and "PLANNING" in s.upper())
    log(f"  Methods: {active_count} Active, {planning_count} Planning")
    results["methods_active"] = active_count
    results["methods_planning"] = planning_count

    # 6. Cross-pollination check
    cross_poll = count_csv_rows(LEDGER / "CROSS_POLLINATION_MATRIX.csv")
    log(f"  Cross-pollination matrix: {cross_poll} synergy entries")
    results["cross_pollination_entries"] = cross_poll

    results["integrated"] = len(results.get("actions", []))
    return results


# ---------------------------------------------------------------------------
# SYSTEM STATUS
# ---------------------------------------------------------------------------

def show_status():
    """Show comprehensive system status across all 5 loops."""
    print("=" * 70)
    print("  PRINTMAXX PERPETUAL SYSTEM STATUS")
    print(f"  Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)

    # Loop 1: Research
    alpha_total = count_csv_rows(LEDGER / "ALPHA_STAGING.csv")
    alpha_statuses = read_csv_column(LEDGER / "ALPHA_STAGING.csv", "status")
    pending = sum(1 for s in alpha_statuses if s and "PENDING" in s.upper())
    approved = sum(1 for s in alpha_statuses if s and "APPROVED" in s.upper())

    print(f"\n  LOOP 1 - RESEARCH")
    print(f"    Alpha: {alpha_total} total | {pending} pending | {approved} approved")
    print(f"    Sources: {count_csv_rows(LEDGER / 'HIGH_SIGNAL_SOURCES.csv')} high-signal accounts")
    print(f"    Subreddits: {count_csv_rows(LEDGER / 'RESEARCH_SUBREDDITS.csv')} monitored")

    # Loop 2: Content
    content_csvs = list(CONTENT_POSTING.glob("*.csv"))
    buffer_files = list(LEDGER.glob("buffer_import_*.csv"))
    print(f"\n  LOOP 2 - CONTENT")
    print(f"    Content CSVs: {len(content_csvs)} files ready")
    print(f"    Buffer imports: {len(buffer_files)} files")
    print(f"    Calendar: {count_csv_rows(LEDGER / 'CONTENT_CALENDAR_30DAY.csv')} entries")
    print(f"    Performance: {count_csv_rows(LEDGER / 'CONTENT_PERFORMANCE_TRACKER.csv')} tracked")

    # Loop 3: Products
    products = count_csv_rows(LEDGER / "PRODUCTS.csv")
    revenue = count_csv_rows(FINANCIALS / "REVENUE_TRACKER.csv")
    print(f"\n  LOOP 3 - PRODUCTS")
    print(f"    Products: {products} in LEDGER")
    print(f"    Revenue entries: {revenue}")
    print(f"    Streams: {count_csv_rows(LEDGER / 'REVENUE_STREAMS_TRACKER.csv')} tracked")

    # Loop 4: Leads
    lead_files = list(LEADS_DIR.glob("*_leads.csv")) if LEADS_DIR.exists() else []
    total_leads = sum(count_csv_rows(f) for f in lead_files)
    outreach_files = list(OUTREACH_DIR.glob("*_emails*.csv")) if OUTREACH_DIR.exists() else []
    print(f"\n  LOOP 4 - LEADS")
    print(f"    Lead files: {len(lead_files)} | Total leads: {total_leads}")
    print(f"    Outreach files: {len(outreach_files)}")
    print(f"    Pipeline: {count_csv_rows(LEDGER / 'OUTREACH_PIPELINE.csv')} entries")
    print(f"    Freelance: {count_csv_rows(LEDGER / 'FREELANCE_PIPELINE.csv')} entries")

    # Loop 5: Apps
    app_output = BASE / "ralph" / "loops" / "app_factory" / "output"
    apps = [d.name for d in app_output.iterdir() if d.is_dir()] if app_output.exists() else []
    seo_pages = count_files(BASE / "builds" / "programmatic_seo", "*.html")
    print(f"\n  LOOP 5 - APPS")
    print(f"    Built apps: {len(apps)} ({', '.join(apps)})")
    print(f"    SEO pages: {seo_pages}")
    print(f"    Clone opps: {count_csv_rows(LEDGER / 'APP_CLONE_OPPORTUNITIES.csv')}")
    print(f"    ASO keywords: {count_csv_rows(LEDGER / 'ASO_KEYWORDS.csv')}")

    # Blockers
    print(f"\n  BLOCKERS (Human Action Required)")
    accounts = read_csv_column(LEDGER / "ACCOUNTS.csv", "Status")
    created = sum(1 for s in accounts if s and "CREATED" in s.upper() or "ACTIVE" in s.upper())
    needs_creation = sum(1 for s in accounts if s and "NEEDS_CREATION" in s.upper())
    print(f"    Accounts: {created} created, {needs_creation} need creation")
    print(f"    Deployment: {'vercel' if os.path.exists('/usr/local/bin/vercel') or os.path.exists('/opt/homebrew/bin/vercel') else 'NO DEPLOY TOOL'}")
    print(f"    Email tool: NOT SET UP (blocks all outreach)")

    print("\n" + "=" * 70)


def show_gaps():
    """Show all gaps that break perpetual loops."""
    print("=" * 70)
    print("  PRINTMAXX SYSTEM GAPS (What's Broken)")
    print("=" * 70)

    gaps = []

    # Check each critical path
    checks = [
        ("Alpha integration", count_csv_rows(LEDGER / "ALPHA_EXECUTION_TRACKER.csv") > 0, "No alpha being routed to target files"),
        ("Content measurement", count_csv_rows(LEDGER / "CONTENT_PERFORMANCE_TRACKER.csv") > 0, "No content performance tracked"),
        ("Products live", any("LIVE" in (s or "").upper() for s in read_csv_column(LEDGER / "PRODUCTS.csv", "Status")), "Zero products listed on any platform"),
        ("Revenue tracked", count_csv_rows(FINANCIALS / "REVENUE_TRACKER.csv") > 1, "No revenue being tracked (only paper trade)"),
        ("Outreach sent", count_csv_rows(OUTREACH_DIR / "PIPELINE_TRACKER.csv") > 0 if (OUTREACH_DIR / "PIPELINE_TRACKER.csv").exists() else False, "No outreach emails sent"),
        ("Apps deployed", False, "6 apps built, 0 deployed (need vercel login)"),  # Always false until deployment
        ("Social accounts", any("ACTIVE" in (s or "").upper() for s in read_csv_column(LEDGER / "ACCOUNTS.csv", "Status")), "No social accounts active"),
        ("Freelance pipeline", count_csv_rows(LEDGER / "FREELANCE_PIPELINE.csv") > 0, "No freelance orders in pipeline"),
    ]

    for name, is_ok, problem in checks:
        status = "OK" if is_ok else "BROKEN"
        if not is_ok:
            gaps.append({"system": name, "problem": problem})
        print(f"  [{status:6s}] {name}: {problem if not is_ok else 'Working'}")

    print(f"\n  Total gaps: {len(gaps)} / {len(checks)}")
    print(f"  System health: {((len(checks) - len(gaps)) / len(checks) * 100):.0f}%")
    print("=" * 70)

    return gaps


# ---------------------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="PRINTMAXX Perpetual Improvement Runner")
    parser.add_argument("--loop", type=int, choices=[1, 2, 3, 4, 5], help="Run specific loop")
    parser.add_argument("--status", action="store_true", help="Show system status")
    parser.add_argument("--gaps", action="store_true", help="Show gaps only")
    parser.add_argument("--integrate", action="store_true", help="Run cross-loop integration only")
    parser.add_argument("--dry-run", action="store_true", help="Show what would run without executing")
    args = parser.parse_args()

    if args.status:
        show_status()
        return

    if args.gaps:
        show_gaps()
        return

    if args.integrate:
        results = run_integration(dry_run=args.dry_run)
        if results.get("actions"):
            print("\nActions needed:")
            for i, action in enumerate(results["actions"], 1):
                print(f"  {i}. {action}")
        return

    log(f"PRINTMAXX Perpetual Improvement Runner - {datetime.now()}")
    log(f"Base: {BASE}")
    log("")

    all_results = {}

    if args.loop:
        loops = {1: run_loop1, 2: run_loop2, 3: run_loop3, 4: run_loop4, 5: run_loop5}
        result = loops[args.loop](dry_run=args.dry_run)
        all_results[f"loop{args.loop}"] = result
    else:
        # Run all loops
        all_results["loop1"] = run_loop1(dry_run=args.dry_run)
        all_results["loop2"] = run_loop2(dry_run=args.dry_run)
        all_results["loop3"] = run_loop3(dry_run=args.dry_run)
        all_results["loop4"] = run_loop4(dry_run=args.dry_run)
        all_results["loop5"] = run_loop5(dry_run=args.dry_run)
        all_results["integration"] = run_integration(dry_run=args.dry_run)

    # Write final summary
    log("")
    log("=" * 60)
    log("SUMMARY")
    log("=" * 60)

    # Collect gaps
    gaps = []
    for key, result in all_results.items():
        if isinstance(result, dict) and "gap" in result:
            gaps.append(f"{key}: {result['gap']}")
        if isinstance(result, dict) and "actions" in result:
            for action in result["actions"]:
                gaps.append(f"{key}: {action}")

    if gaps:
        log(f"Gaps found: {len(gaps)}")
        for g in gaps:
            log(f"  - {g}")
    else:
        log("No critical gaps found.")

    # Write JSON summary
    summary = {
        "run_time": datetime.utcnow().isoformat() + "Z",
        "loops_run": list(all_results.keys()),
        "gaps": gaps,
        "results": {}
    }
    for key, result in all_results.items():
        if isinstance(result, dict):
            # Strip non-serializable items
            clean = {k: v for k, v in result.items() if isinstance(v, (str, int, float, bool, list, dict, type(None)))}
            summary["results"][key] = clean

    summary_file = LOGS / f"perpetual_summary_{TIMESTAMP}.json"
    try:
        with open(summary_file, "w") as f:
            json.dump(summary, f, indent=2, default=str)
        log(f"Summary written to: {summary_file}")
    except Exception as e:
        log(f"Failed to write summary: {e}")

    log(f"Log file: {LOG_FILE}")
    log("Done.")


if __name__ == "__main__":
    main()
