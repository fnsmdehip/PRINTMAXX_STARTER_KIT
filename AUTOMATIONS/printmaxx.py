#!/usr/bin/env python3
"""
PRINTMAXX Unified CLI - One command to rule them all.

Usage:
    python3 printmaxx.py <command> [options]

Commands:
    pipeline    Closed-loop pipeline (scrape -> score -> email -> track)
    leads       Lead management (hot/warm/enrich/scrape)
    emails      Email operations (generate/send/ab-test/health)
    dashboard   Refresh live dashboard
    propose     Generate proposal for a lead
    onboard     Client onboarding from lead
    deploy      Deploy apps and sites
    content     Content generation from metrics
    memory      Memory manager (heartbeat/full)
    overnight   Overnight orchestrator
    scrape      Run scrapers (reddit/twitter/nationwide)
    quant       Quant terminal and analytics
    rbi         RBI scanner and venture tracker
    status      Full system status
    help        Show all commands with examples
"""

import argparse
import csv
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path

# Project root and automations directory
PROJECT_ROOT = Path(__file__).resolve().parent.parent
AUTOMATIONS_DIR = Path(__file__).resolve().parent
PYTHON = sys.executable

# Script registry: maps CLI commands to actual scripts + args
SCRIPT_REGISTRY = {
    # Pipeline
    "pipeline.status": ("closed_loop_pipeline.py", ["--status"]),
    "pipeline.run": ("closed_loop_pipeline.py", ["--cycles", "5", "--batch", "2000"]),

    # Leads
    "leads.enrich": ("lead_enrichment.py", ["--enrich"]),
    "leads.scrape": ("nationwide_scraper.py", []),
    "leads.qualify": ("intelligent_lead_qualifier.py", []),
    "leads.score": ("website_signal_scorer.py", []),

    # Emails
    "emails.generate": ("generate_cold_emails.py", []),
    "emails.send": ("email_sender.py", ["--dry-run"]),
    "emails.send_live": ("email_sender.py", []),
    "emails.ab_test": ("cold_email_ab_test.py", ["--split"]),
    "emails.health": ("email_domain_health.py", ["--check-all"]),

    # Dashboard
    "dashboard": ("refresh_dashboard.py", []),

    # Proposals
    "propose": ("generate_proposal.py", []),

    # Onboarding
    "onboard": ("client_onboarding.py", []),

    # Deploy
    "deploy.all": ("deploy_all_apps.sh", []),

    # Content
    "content.generate": ("auto_content_from_metrics.py", []),
    "content.multiply": ("content_multiplier.py", []),
    "content.posting": ("platform_posting_optimizer.py", []),

    # Memory
    "memory.heartbeat": ("memory_manager.py", ["--heartbeat"]),
    "memory.full": ("memory_manager.py", ["--full"]),

    # Overnight
    "overnight.run": ("overnight_orchestrator.py", ["--run"]),
    "overnight.status": ("overnight_orchestrator.py", ["--status"]),

    # Scrapers
    "scrape.reddit": ("background_reddit_scraper.py", ["--scrape"]),
    "scrape.twitter": ("twitter_alpha_scraper.py", ["--all"]),
    "scrape.nationwide": ("nationwide_scraper.py", []),
    "scrape.producthunt": ("producthunt_scraper.py", []),
    "scrape.trends": ("trend_aggregator.py", []),
    "scrape.freelance": ("freelance_demand_scanner.py", []),
    "scrape.ecom": ("ecom_arb_engine.py", []),
    "scrape.viral": ("viral_product_scanner.py", []),

    # Quant
    "quant.terminal": ("printmaxx_quant_terminal.py", []),
    "quant.summary": ("printmaxx_quant_terminal.py", ["--summary"]),
    "quant.dashboard": ("quant_dashboard.py", []),
    "quant.ops": ("ops_dashboard.py", []),
    "quant.revenue": ("revenue_projector.py", []),
    "quant.alpha": ("alpha_screening.py", ["--pending"]),
    "quant.paper": ("paper_trade.py", ["--list"]),
    "quant.performance": ("method_performance_analyzer.py", []),

    # RBI
    "rbi.scan": ("daily_nocost_rbi_scanner.py", ["--scan"]),
    "rbi.next": ("daily_nocost_rbi_scanner.py", ["--next-actions"]),
    "rbi.ready": ("daily_nocost_rbi_scanner.py", ["--ready-to-list"]),
    "rbi.ventures": ("venture_performance_tracker.py", ["--recommend"]),
    "rbi.agent": ("daily_agent_runner.py", ["--status"]),

    # SEO Competitor Analysis
    "seo.summary": ("seo_competitor_analyzer.py", ["--summary"]),
    "seo.all_hot": ("seo_competitor_analyzer.py", ["--all-hot"]),
    "seo.brief": ("seo_competitor_analyzer.py", ["--brief", "--all-hot"]),
}


def run_script(script_name, extra_args=None):
    """Run a script from AUTOMATIONS/ directory. Handles missing scripts gracefully."""
    script_path = AUTOMATIONS_DIR / script_name

    if not script_path.exists():
        print(f"\n  [NOT BUILT] {script_name}")
        print(f"  This script hasn't been created yet.")
        print(f"  Expected at: {script_path}")
        print(f"  Coming soon.\n")
        return 1

    args = extra_args or []

    if script_name.endswith(".sh"):
        cmd = ["bash", str(script_path)] + args
    else:
        cmd = [PYTHON, str(script_path)] + args

    try:
        result = subprocess.run(cmd, cwd=str(PROJECT_ROOT))
        return result.returncode
    except KeyboardInterrupt:
        print("\nInterrupted.")
        return 130
    except Exception as e:
        print(f"\n  [ERROR] Failed to run {script_name}: {e}\n")
        return 1


def cmd_pipeline(args):
    """Closed-loop pipeline: scrape -> score -> email -> track."""
    if args.status:
        return run_script(*_lookup("pipeline.status"))
    if args.run:
        extra = ["--cycles", str(args.cycles), "--batch", str(args.batch)]
        return run_script("closed_loop_pipeline.py", extra)
    # Default: show status
    return run_script(*_lookup("pipeline.status"))


def cmd_leads(args):
    """Lead management."""
    if args.hot:
        return _show_leads("hot")
    if args.warm:
        return _show_leads("warm")
    if args.all:
        return _show_leads("all")
    if args.enrich:
        return run_script(*_lookup("leads.enrich"))
    if args.scrape:
        extra = []
        if args.city:
            extra += ["--city", args.city]
        if args.industry:
            extra += ["--industry", args.industry]
        return run_script("savvy_lead_scraper.py", extra)
    if args.score:
        extra = []
        if args.input:
            extra += ["--input", args.input]
        return run_script("website_signal_scorer.py", extra)
    # Default: show summary
    return _show_leads("summary")


def cmd_emails(args):
    """Email operations."""
    if args.generate:
        extra = []
        if args.industry:
            extra += ["--industry", args.industry]
        if args.dry_run:
            extra += ["--dry-run"]
        return run_script("generate_cold_emails.py", extra)
    if args.send:
        extra = []
        if args.dry_run:
            extra += ["--dry-run"]
        if args.preview:
            extra += ["--preview"]
        return run_script("email_sender.py", extra)
    if args.ab_test:
        return run_script(*_lookup("emails.ab_test"))
    if args.health:
        return run_script(*_lookup("emails.health"))
    # Default: show email status
    _show_email_status()
    return 0


def cmd_dashboard(args):
    """Refresh dashboard."""
    return run_script(*_lookup("dashboard"))


def cmd_propose(args):
    """Generate proposal for a lead."""
    extra = []
    if args.lead_id:
        extra += ["--lead-id", args.lead_id]
    return run_script("generate_proposal.py", extra)


def cmd_onboard(args):
    """Client onboarding."""
    extra = []
    if args.lead_id:
        extra += ["--from-lead", args.lead_id]
    return run_script("client_onboarding.py", extra)


def cmd_deploy(args):
    """Deploy apps and sites."""
    if args.all:
        return run_script(*_lookup("deploy.all"))
    print("  Usage: printmaxx deploy --all")
    return 0


def cmd_content(args):
    """Content generation."""
    if args.generate:
        return run_script(*_lookup("content.generate"))
    if args.multiply:
        return run_script(*_lookup("content.multiply"))
    if args.posting:
        return run_script(*_lookup("content.posting"))
    print("  Usage: printmaxx content --generate | --multiply | --posting")
    return 0


def cmd_memory(args):
    """Memory manager."""
    if args.heartbeat:
        return run_script(*_lookup("memory.heartbeat"))
    if args.full:
        return run_script(*_lookup("memory.full"))
    # Default: heartbeat
    return run_script(*_lookup("memory.heartbeat"))


def cmd_overnight(args):
    """Overnight orchestrator."""
    if args.run:
        return run_script(*_lookup("overnight.run"))
    if args.status:
        return run_script(*_lookup("overnight.status"))
    # Default: status
    return run_script(*_lookup("overnight.status"))


def cmd_scrape(args):
    """Run scrapers."""
    if args.reddit:
        return run_script(*_lookup("scrape.reddit"))
    if args.twitter:
        return run_script(*_lookup("scrape.twitter"))
    if args.nationwide:
        extra = []
        if args.cities:
            extra += ["--cities", args.cities]
        if args.industries:
            extra += ["--industries", args.industries]
        return run_script("nationwide_scraper.py", extra)
    if args.producthunt:
        return run_script(*_lookup("scrape.producthunt"))
    if args.trends:
        return run_script(*_lookup("scrape.trends"))
    if args.freelance:
        return run_script(*_lookup("scrape.freelance"))
    if args.ecom:
        return run_script(*_lookup("scrape.ecom"))
    if args.viral:
        return run_script(*_lookup("scrape.viral"))
    if args.all:
        print("  Running all scrapers in sequence...")
        for key in ["scrape.reddit", "scrape.trends", "scrape.freelance", "scrape.ecom"]:
            name, default_args = _lookup(key)
            print(f"\n  >>> {name}")
            run_script(name, default_args)
        return 0
    print("  Usage: printmaxx scrape --reddit | --twitter | --nationwide | --trends | --all")
    return 0


def cmd_quant(args):
    """Quant terminal and analytics."""
    if args.terminal:
        return run_script(*_lookup("quant.terminal"))
    if args.summary:
        return run_script(*_lookup("quant.summary"))
    if args.dashboard:
        return run_script(*_lookup("quant.dashboard"))
    if args.ops:
        return run_script(*_lookup("quant.ops"))
    if args.revenue:
        return run_script(*_lookup("quant.revenue"))
    if args.alpha:
        return run_script(*_lookup("quant.alpha"))
    if args.paper:
        return run_script(*_lookup("quant.paper"))
    if args.performance:
        return run_script(*_lookup("quant.performance"))
    # Default: summary
    return run_script(*_lookup("quant.summary"))


def cmd_rbi(args):
    """RBI scanner and venture tracker."""
    if args.scan:
        return run_script(*_lookup("rbi.scan"))
    if args.next:
        return run_script(*_lookup("rbi.next"))
    if args.ready:
        return run_script(*_lookup("rbi.ready"))
    if args.ventures:
        return run_script(*_lookup("rbi.ventures"))
    if args.agent:
        return run_script(*_lookup("rbi.agent"))
    # Default: next actions
    return run_script(*_lookup("rbi.next"))


def cmd_seo(args):
    """SEO competitor analysis."""
    if args.summary:
        return run_script(*_lookup("seo.summary"))
    if args.all_hot:
        return run_script(*_lookup("seo.all_hot"))
    if args.brief:
        return run_script(*_lookup("seo.brief"))
    if args.lead_id:
        return run_script("seo_competitor_analyzer.py", ["--lead-id", args.lead_id])
    if args.industry:
        extra = ["--industry", args.industry]
        if args.top:
            extra += ["--top", str(args.top)]
        return run_script("seo_competitor_analyzer.py", extra)
    # Default: summary
    return run_script(*_lookup("seo.summary"))


def cmd_status(args):
    """Full system status."""
    print("=" * 70)
    print("  PRINTMAXX SYSTEM STATUS")
    print(f"  {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)

    # 1. Lead counts
    print("\n--- LEADS ---")
    _show_leads("summary")

    # 2. Email status
    print("\n--- EMAILS ---")
    _show_email_status()

    # 3. Pipeline scripts health
    print("\n--- SCRIPT HEALTH ---")
    total = 0
    exists = 0
    missing = []
    seen = set()
    for key, (script, _) in SCRIPT_REGISTRY.items():
        if script not in seen:
            seen.add(script)
            total += 1
            path = AUTOMATIONS_DIR / script
            if path.exists():
                exists += 1
            else:
                missing.append(script)
    print(f"  Scripts found: {exists}/{total}")
    if missing:
        print(f"  Not yet built ({len(missing)}):")
        for m in sorted(missing):
            print(f"    - {m}")

    # 4. Deployed sites
    print("\n--- DEPLOYED SITES ---")
    deploy_log = PROJECT_ROOT / "OPS" / "DEPLOY_LOG.md"
    if deploy_log.exists():
        count = 0
        with open(deploy_log, "r") as f:
            for line in f:
                if "surge.sh" in line and "http" in line:
                    count += 1
        print(f"  Live surge.sh sites: {count}")
    else:
        print("  Deploy log not found")

    # 5. Products ready
    print("\n--- PRODUCTS ---")
    gumroad_dir = PROJECT_ROOT / "PRODUCTS" / "GUMROAD_INSTANT_UPLOAD"
    fiverr_dir = PROJECT_ROOT / "PRODUCTS" / "FIVERR_INSTANT_UPLOAD"
    gumroad_count = len(list(gumroad_dir.glob("*.md"))) if gumroad_dir.exists() else 0
    fiverr_count = len(list(fiverr_dir.glob("*.md"))) if fiverr_dir.exists() else 0
    print(f"  Gumroad products ready: {gumroad_count}")
    print(f"  Fiverr gigs ready: {fiverr_count}")

    # 6. Content ready
    print("\n--- CONTENT ---")
    content_posting = AUTOMATIONS_DIR / "content_posting"
    if content_posting.exists():
        csv_count = len(list(content_posting.glob("*.csv")))
        print(f"  Buffer CSVs ready: {csv_count}")

    print("\n" + "=" * 70)
    print("  Run 'python3 printmaxx.py help' for all commands")
    print("=" * 70)
    return 0


def cmd_help(args):
    """Show all commands with examples."""
    print("""
================================================================================
  PRINTMAXX CLI - Unified Command Center
================================================================================

  PIPELINE (closed-loop: scrape -> score -> email -> track)
  ─────────────────────────────────────────────────────────
    printmaxx pipeline --status             Show pipeline status
    printmaxx pipeline --run                Run 5 cycles (2000 batch)
    printmaxx pipeline --run --cycles 10    Run 10 cycles

  LEADS
  ─────
    printmaxx leads --hot                   Show hot leads (score <= 30)
    printmaxx leads --warm                  Show warm leads (score 31-60)
    printmaxx leads --all                   Show all lead counts
    printmaxx leads --enrich                Enrich leads with extra data
    printmaxx leads --scrape --city "Austin TX" --industry dental
    printmaxx leads --score --input leads.csv

  EMAILS
  ──────
    printmaxx emails --generate             Generate cold email sequences
    printmaxx emails --generate --industry dental --dry-run
    printmaxx emails --send --dry-run       Preview emails (no sending)
    printmaxx emails --send                 Send emails (LIVE)
    printmaxx emails --ab-test              Split test email variants
    printmaxx emails --health               Check domain deliverability

  DASHBOARD
  ─────────
    printmaxx dashboard                     Refresh live dashboard

  PROPOSALS & ONBOARDING
  ──────────────────────
    printmaxx propose --lead-id LEAD_042    Generate proposal for lead
    printmaxx onboard --lead-id LEAD_042    Start client onboarding

  DEPLOY
  ──────
    printmaxx deploy --all                  Deploy all apps to surge.sh

  CONTENT
  ───────
    printmaxx content --generate            Auto-generate from metrics
    printmaxx content --multiply            Multiply content across formats
    printmaxx content --posting             Optimize posting schedule

  MEMORY
  ──────
    printmaxx memory --heartbeat            Quick memory sync
    printmaxx memory --full                 Full memory rebuild

  OVERNIGHT
  ─────────
    printmaxx overnight --run               Start overnight orchestrator
    printmaxx overnight --status            Check overnight status

  SCRAPERS
  ────────
    printmaxx scrape --reddit               Scrape Reddit (JSON API)
    printmaxx scrape --twitter              Scrape Twitter (Brave cookies)
    printmaxx scrape --nationwide            Nationwide lead scraper
    printmaxx scrape --trends               Trend aggregator
    printmaxx scrape --freelance            Freelance demand scan
    printmaxx scrape --ecom                 Ecom arbitrage engine
    printmaxx scrape --viral                Viral product scanner
    printmaxx scrape --producthunt          Product Hunt scraper
    printmaxx scrape --all                  Run all scrapers

  QUANT TERMINAL
  ──────────────
    printmaxx quant --terminal              Full TUI terminal
    printmaxx quant --summary               Quick health summary
    printmaxx quant --dashboard             Simple dashboard
    printmaxx quant --ops                   Ops dashboard
    printmaxx quant --revenue               Revenue projector
    printmaxx quant --alpha                 Alpha screener (pending)
    printmaxx quant --paper                 Paper trade list
    printmaxx quant --performance           Method performance

  RBI (Research-Based Improvement)
  ────────────────────────────────
    printmaxx rbi --scan                    Full daily RBI scan
    printmaxx rbi --next                    Top 10 next actions
    printmaxx rbi --ready                   Items ready to list NOW
    printmaxx rbi --ventures                Venture performance (KILL/DOUBLE_DOWN)
    printmaxx rbi --agent                   Agent daily runner status

  SEO COMPETITOR ANALYSIS
  ───────────────────────
    printmaxx seo --summary                 Aggregate stats across all leads
    printmaxx seo --all-hot                 Analyze ALL hot leads vs competitors
    printmaxx seo --brief                   Brief email snippets for outreach
    printmaxx seo --lead-id UUID            Analyze specific lead
    printmaxx seo --industry dentist --top 5   Top 5 dentist leads analyzed

  SYSTEM
  ──────
    printmaxx status                        Full system status
    printmaxx help                          This help message

================================================================================
  All commands delegate to scripts in AUTOMATIONS/
  Missing scripts show "Not yet built" instead of crashing.
  Project root: {root}
================================================================================
""".format(root=PROJECT_ROOT))
    return 0


# --- Helper functions ---

def _lookup(key):
    """Look up script name and default args from registry."""
    return SCRIPT_REGISTRY[key]


def _show_leads(mode):
    """Show lead counts from CSV files."""
    leads_dir = AUTOMATIONS_DIR / "leads"

    hot_path = leads_dir / "HOT_LEADS.csv"
    scored_path = leads_dir / "SCORED_LEADS.csv"
    master_path = leads_dir / "MASTER_LEADS.csv"

    def count_csv(path):
        if not path.exists():
            return 0
        try:
            with open(path, "r") as f:
                reader = csv.reader(f)
                next(reader, None)  # skip header
                return sum(1 for _ in reader)
        except Exception:
            return 0

    hot_count = count_csv(hot_path)
    scored_count = count_csv(scored_path)
    master_count = count_csv(master_path)
    warm_count = max(0, scored_count - hot_count)

    if mode == "summary":
        print(f"  Total leads: {master_count}")
        print(f"  Scored: {scored_count}")
        print(f"  Hot (score <= 30): {hot_count}")
        print(f"  Warm (score 31-60): {warm_count}")
        return 0

    if mode == "hot":
        print(f"\n  HOT LEADS ({hot_count} total, score <= 30)")
        print(f"  Source: {hot_path}")
        if hot_path.exists() and hot_count > 0:
            _print_csv_sample(hot_path, 10)
        else:
            print("  No hot leads found. Run: printmaxx leads --scrape")
        return 0

    if mode == "warm":
        print(f"\n  WARM LEADS ({warm_count} estimated, score 31-60)")
        print(f"  Source: {scored_path}")
        if scored_path.exists() and scored_count > 0:
            _print_csv_sample(scored_path, 10)
        else:
            print("  No scored leads found. Run: printmaxx leads --score")
        return 0

    if mode == "all":
        print(f"\n  ALL LEADS")
        print(f"  Master: {master_count}")
        print(f"  Scored: {scored_count}")
        print(f"  Hot: {hot_count}")
        print(f"  Warm: {warm_count}")

        # Also check for lead files in other locations
        other_lead_files = list(leads_dir.glob("*.csv")) if leads_dir.exists() else []
        if other_lead_files:
            print(f"\n  Lead files in {leads_dir}:")
            for f in sorted(other_lead_files):
                c = count_csv(f)
                print(f"    {f.name}: {c} rows")
        return 0

    return 0


def _print_csv_sample(path, n=5):
    """Print first n rows of a CSV file."""
    try:
        with open(path, "r") as f:
            reader = csv.reader(f)
            header = next(reader, None)
            if header:
                # Pick key columns to display
                key_cols = []
                for col_name in ["business_name", "name", "city", "industry", "score", "website", "email", "phone"]:
                    for i, h in enumerate(header):
                        if col_name.lower() in h.lower() and i not in [k[1] for k in key_cols]:
                            key_cols.append((h, i))
                            break

                if not key_cols:
                    key_cols = [(header[i], i) for i in range(min(5, len(header)))]

                col_names = [k[0] for k in key_cols]
                print(f"  {'  |  '.join(col_names[:5])}")
                print(f"  {'-' * 70}")

                for i, row in enumerate(reader):
                    if i >= n:
                        break
                    vals = []
                    for _, idx in key_cols[:5]:
                        if idx < len(row):
                            val = row[idx][:25]
                            vals.append(val)
                        else:
                            vals.append("")
                    print(f"  {'  |  '.join(vals)}")
    except Exception as e:
        print(f"  Error reading CSV: {e}")


def _show_email_status():
    """Show email outreach status."""
    outreach_dir = AUTOMATIONS_DIR / "outreach"

    master_emails = outreach_dir / "MASTER_LEADS_emails.csv"
    pipeline = outreach_dir / "PIPELINE_TRACKER.csv"

    if master_emails.exists():
        try:
            with open(master_emails, "r") as f:
                reader = csv.reader(f)
                next(reader, None)
                count = sum(1 for _ in reader)
            print(f"  Email sequences ready: {count}")
        except Exception:
            print(f"  Email sequences: error reading file")
    else:
        print("  Email sequences: none generated yet")

    if pipeline.exists():
        try:
            with open(pipeline, "r") as f:
                reader = csv.reader(f)
                next(reader, None)
                count = sum(1 for _ in reader)
            print(f"  Pipeline entries: {count}")
        except Exception:
            print(f"  Pipeline: error reading file")
    else:
        print("  Pipeline: no tracker yet")


# --- Argument Parser ---

def build_parser():
    parser = argparse.ArgumentParser(
        prog="printmaxx",
        description="PRINTMAXX Unified CLI - One command to rule them all.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="Run 'printmaxx help' for detailed command reference."
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # pipeline
    p_pipeline = subparsers.add_parser("pipeline", help="Closed-loop pipeline")
    p_pipeline.add_argument("--status", action="store_true", help="Show pipeline status")
    p_pipeline.add_argument("--run", action="store_true", help="Run pipeline cycles")
    p_pipeline.add_argument("--cycles", type=int, default=5, help="Number of cycles (default: 5)")
    p_pipeline.add_argument("--batch", type=int, default=2000, help="Batch size (default: 2000)")
    p_pipeline.set_defaults(func=cmd_pipeline)

    # leads
    p_leads = subparsers.add_parser("leads", help="Lead management")
    p_leads.add_argument("--hot", action="store_true", help="Show hot leads (score <= 30)")
    p_leads.add_argument("--warm", action="store_true", help="Show warm leads (score 31-60)")
    p_leads.add_argument("--all", action="store_true", help="Show all lead counts")
    p_leads.add_argument("--enrich", action="store_true", help="Enrich leads with extra data")
    p_leads.add_argument("--scrape", action="store_true", help="Scrape new leads")
    p_leads.add_argument("--score", action="store_true", help="Score leads by website quality")
    p_leads.add_argument("--city", type=str, help="City for scraping (e.g. 'Austin TX')")
    p_leads.add_argument("--industry", type=str, help="Industry filter")
    p_leads.add_argument("--input", type=str, help="Input CSV for scoring")
    p_leads.set_defaults(func=cmd_leads)

    # emails
    p_emails = subparsers.add_parser("emails", help="Email operations")
    p_emails.add_argument("--generate", action="store_true", help="Generate cold email sequences")
    p_emails.add_argument("--send", action="store_true", help="Send emails")
    p_emails.add_argument("--ab-test", action="store_true", help="A/B test email variants")
    p_emails.add_argument("--health", action="store_true", help="Check domain health")
    p_emails.add_argument("--dry-run", action="store_true", help="Dry run (no actual sending)")
    p_emails.add_argument("--preview", action="store_true", help="Preview emails")
    p_emails.add_argument("--industry", type=str, help="Industry filter for generation")
    p_emails.set_defaults(func=cmd_emails)

    # dashboard
    p_dashboard = subparsers.add_parser("dashboard", help="Refresh live dashboard")
    p_dashboard.set_defaults(func=cmd_dashboard)

    # propose
    p_propose = subparsers.add_parser("propose", help="Generate proposal for a lead")
    p_propose.add_argument("--lead-id", type=str, help="Lead ID")
    p_propose.set_defaults(func=cmd_propose)

    # onboard
    p_onboard = subparsers.add_parser("onboard", help="Client onboarding from lead")
    p_onboard.add_argument("--lead-id", type=str, help="Lead ID")
    p_onboard.set_defaults(func=cmd_onboard)

    # deploy
    p_deploy = subparsers.add_parser("deploy", help="Deploy apps and sites")
    p_deploy.add_argument("--all", action="store_true", help="Deploy everything")
    p_deploy.set_defaults(func=cmd_deploy)

    # content
    p_content = subparsers.add_parser("content", help="Content generation")
    p_content.add_argument("--generate", action="store_true", help="Auto-generate from metrics")
    p_content.add_argument("--multiply", action="store_true", help="Multiply across formats")
    p_content.add_argument("--posting", action="store_true", help="Optimize posting schedule")
    p_content.set_defaults(func=cmd_content)

    # memory
    p_memory = subparsers.add_parser("memory", help="Memory manager")
    p_memory.add_argument("--heartbeat", action="store_true", help="Quick memory sync")
    p_memory.add_argument("--full", action="store_true", help="Full memory rebuild")
    p_memory.set_defaults(func=cmd_memory)

    # overnight
    p_overnight = subparsers.add_parser("overnight", help="Overnight orchestrator")
    p_overnight.add_argument("--run", action="store_true", help="Start overnight run")
    p_overnight.add_argument("--status", action="store_true", help="Check overnight status")
    p_overnight.set_defaults(func=cmd_overnight)

    # scrape
    p_scrape = subparsers.add_parser("scrape", help="Run scrapers")
    p_scrape.add_argument("--reddit", action="store_true", help="Reddit scraper")
    p_scrape.add_argument("--twitter", action="store_true", help="Twitter scraper")
    p_scrape.add_argument("--nationwide", action="store_true", help="Nationwide lead scraper")
    p_scrape.add_argument("--producthunt", action="store_true", help="Product Hunt scraper")
    p_scrape.add_argument("--trends", action="store_true", help="Trend aggregator")
    p_scrape.add_argument("--freelance", action="store_true", help="Freelance demand scanner")
    p_scrape.add_argument("--ecom", action="store_true", help="Ecom arbitrage engine")
    p_scrape.add_argument("--viral", action="store_true", help="Viral product scanner")
    p_scrape.add_argument("--all", action="store_true", help="Run all scrapers")
    p_scrape.add_argument("--cities", type=str, help="Cities CSV for nationwide")
    p_scrape.add_argument("--industries", type=str, help="Industries for nationwide")
    p_scrape.set_defaults(func=cmd_scrape)

    # quant
    p_quant = subparsers.add_parser("quant", help="Quant terminal and analytics")
    p_quant.add_argument("--terminal", action="store_true", help="Full TUI terminal")
    p_quant.add_argument("--summary", action="store_true", help="Quick health summary")
    p_quant.add_argument("--dashboard", action="store_true", help="Simple dashboard")
    p_quant.add_argument("--ops", action="store_true", help="Ops dashboard")
    p_quant.add_argument("--revenue", action="store_true", help="Revenue projector")
    p_quant.add_argument("--alpha", action="store_true", help="Alpha screener")
    p_quant.add_argument("--paper", action="store_true", help="Paper trade list")
    p_quant.add_argument("--performance", action="store_true", help="Method performance")
    p_quant.set_defaults(func=cmd_quant)

    # rbi
    p_rbi = subparsers.add_parser("rbi", help="RBI scanner and venture tracker")
    p_rbi.add_argument("--scan", action="store_true", help="Full daily RBI scan")
    p_rbi.add_argument("--next", action="store_true", help="Top 10 next actions")
    p_rbi.add_argument("--ready", action="store_true", help="Items ready to list NOW")
    p_rbi.add_argument("--ventures", action="store_true", help="Venture performance")
    p_rbi.add_argument("--agent", action="store_true", help="Agent daily runner status")
    p_rbi.set_defaults(func=cmd_rbi)

    # seo
    p_seo = subparsers.add_parser("seo", help="SEO competitor analysis")
    p_seo.add_argument("--summary", action="store_true", help="Aggregate summary stats")
    p_seo.add_argument("--all-hot", action="store_true", help="Analyze ALL hot leads")
    p_seo.add_argument("--brief", action="store_true", help="Brief output (email snippets)")
    p_seo.add_argument("--lead-id", type=str, help="Analyze specific lead by UUID")
    p_seo.add_argument("--industry", type=str, help="Filter by industry (dentist, lawyer, etc)")
    p_seo.add_argument("--top", type=int, help="Analyze top N leads")
    p_seo.set_defaults(func=cmd_seo)

    # status
    p_status = subparsers.add_parser("status", help="Full system status")
    p_status.set_defaults(func=cmd_status)

    # help
    p_help = subparsers.add_parser("help", help="Show all commands with examples")
    p_help.set_defaults(func=cmd_help)

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    if not args.command:
        # No command given, show banner + status
        print("""
  ╔═══════════════════════════════════════════════════════════╗
  ║  PRINTMAXX CLI v1.0 - Ship. Deploy. Print. Compound.    ║
  ╚═══════════════════════════════════════════════════════════╝
""")
        cmd_status(args)
        return

    if hasattr(args, "func"):
        rc = args.func(args)
        sys.exit(rc or 0)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
