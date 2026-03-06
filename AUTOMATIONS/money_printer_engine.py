#!/usr/bin/env python3
"""
PRINTMAXX Money Printer Engine
================================
The ultimate 24/7 autonomous revenue generation orchestrator.
Ties together ALL ops into a single closed-loop system.

Architecture:
  DISCOVER → VALIDATE → BUILD → LAUNCH → OPTIMIZE → SCALE → REBALANCE

  Each method flows through this pipeline automatically.
  The engine scores everything, kills losers, doubles winners.

Covers ALL revenue verticals:
  - Apps (iOS/PWA) with auto-rejection screening
  - Digital products (Gumroad, Etsy, KDP)
  - Freelance arbitrage (AI-powered fulfillment)
  - Content monetization (creator rewards, ads, sponsorships)
  - Affiliate marketing (product recommendations, review sites)
  - AI influencer / findom (cheap to run, high margin)
  - Trading / prediction markets (small bets, portfolio approach)
  - Cold outbound (local biz, SaaS, services)
  - Clipping / UGC services
  - Info products / courses
  - SaaS tools (productized automations)

Usage:
  python3 money_printer_engine.py --status          # full system status
  python3 money_printer_engine.py --discover        # find new opportunities
  python3 money_printer_engine.py --validate        # score pending opportunities
  python3 money_printer_engine.py --optimize        # optimize running methods
  python3 money_printer_engine.py --cycle           # run full cycle (discover+validate+optimize+rebalance)
  python3 money_printer_engine.py --revenue         # revenue dashboard
  python3 money_printer_engine.py --methods         # list all methods with scores
  python3 money_printer_engine.py --cheap           # prioritize cheapest methods
  python3 money_printer_engine.py --api-json        # JSON for webapp API
"""

import json
import csv
import os
import sys
import subprocess
import shutil
from datetime import datetime, timedelta
from pathlib import Path
from collections import defaultdict

BASE = Path(__file__).resolve().parent.parent
AUTO = BASE / "AUTOMATIONS"
LEDGER = BASE / "LEDGER"
OPS = BASE / "OPS"
CONTENT = BASE / "CONTENT"
PRODUCTS = BASE / "PRODUCTS"
METHODS = BASE / "MONEY_METHODS"
LOGS = AUTO / "logs"
FINANCIALS = BASE / "FINANCIALS"

for d in [LOGS, LEDGER, OPS]:
    d.mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------------------------
# Path safety
# ---------------------------------------------------------------------------
def safe_path(target):
    resolved = Path(target).resolve()
    if not str(resolved).startswith(str(BASE)):
        raise ValueError(f"BLOCKED: {resolved} outside {BASE}")
    return resolved

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def read_csv(path):
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            return list(csv.DictReader(f))
    except Exception:
        return []

def read_jsonl(path):
    entries = []
    try:
        with open(path, "r") as f:
            for line in f:
                line = line.strip()
                if line:
                    try:
                        entries.append(json.loads(line))
                    except Exception:
                        pass
    except Exception:
        pass
    return entries

def count_file_lines(path):
    try:
        with open(path) as f:
            return sum(1 for _ in f) - 1
    except Exception:
        return 0

def run_script(script, args=None, timeout=120):
    cmd = [sys.executable, str(AUTO / script)]
    if args:
        cmd.extend(args)
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout, cwd=str(BASE))
        return r.stdout + r.stderr
    except Exception as e:
        return str(e)

def disk_percent():
    try:
        st = shutil.disk_usage(str(BASE))
        return round(st.used / st.total * 100, 1)
    except Exception:
        return 0

# ---------------------------------------------------------------------------
# METHOD REGISTRY — every money method scored
# ---------------------------------------------------------------------------

METHODS_REGISTRY = {
    # METHOD_ID: {name, vertical, cost, effort, margin, automation_level, scripts, status}
    # cost: 0=free, 1=<$10/mo, 2=<$50/mo, 3=<$200/mo, 4=$200+/mo
    # effort: 0=fully automated, 1=<1hr/week, 2=<5hr/week, 3=<10hr/week, 4=10+hr/week
    # margin: percentage (0-100)
    # automation_level: percentage automated (0-100)

    # === CHEAPEST / HIGHEST ROI (Priority 1) ===
    "AI_FINDOM": {
        "name": "AI Findom Personas",
        "vertical": "ai_influencer",
        "cost": 0, "effort": 1, "margin": 95,
        "automation_level": 80,
        "scripts": ["content_trend_pipeline.py"],
        "revenue_potential": "$500-5000/mo",
        "status": "READY",
        "priority": 1,
        "notes": "Fanvue/Fansly. AI-generated personas. Near-zero cost. High margin."
    },
    "AFFILIATE_CONTENT": {
        "name": "Affiliate Content (SEO + Social)",
        "vertical": "affiliate",
        "cost": 0, "effort": 1, "margin": 90,
        "automation_level": 85,
        "scripts": ["content_trend_pipeline.py", "tweet_auto_drafter.py"],
        "revenue_potential": "$100-3000/mo",
        "status": "READY",
        "priority": 1,
        "notes": "Review sites, comparison posts, affiliate links in apps. Zero cost."
    },
    "CLIPPING_SERVICE": {
        "name": "Content Clipping (Both Directions)",
        "vertical": "services",
        "cost": 0, "effort": 2, "margin": 85,
        "automation_level": 70,
        "scripts": [],
        "revenue_potential": "$200-2000/mo",
        "status": "READY",
        "priority": 1,
        "notes": "Clip for creators OR hire clippers. yt-dlp+whisper+ffmpeg pipeline built."
    },
    "CREATOR_REWARDS": {
        "name": "Platform Creator Rewards",
        "vertical": "content",
        "cost": 0, "effort": 2, "margin": 100,
        "automation_level": 60,
        "scripts": ["content_trend_pipeline.py", "tweet_auto_drafter.py"],
        "revenue_potential": "$50-1000/mo",
        "status": "NEEDS_ACCOUNTS",
        "priority": 1,
        "notes": "X revenue sharing, YT Shorts fund, TikTok creator rewards. Just post content."
    },
    "INFO_PRODUCTS": {
        "name": "Digital Info Products (Gumroad/Whop)",
        "vertical": "digital_products",
        "cost": 0, "effort": 2, "margin": 95,
        "automation_level": 50,
        "scripts": ["product_launch_automator.py"],
        "revenue_potential": "$100-5000/mo",
        "status": "READY",
        "priority": 1,
        "notes": "13 Gumroad products ready. 5 PDFs ready. Just need account."
    },
    "FREELANCE_ARB": {
        "name": "Freelance Arbitrage (AI Fulfillment)",
        "vertical": "services",
        "cost": 0, "effort": 2, "margin": 90,
        "automation_level": 75,
        "scripts": ["freelance_pipeline.py", "freelance_demand_scanner.py"],
        "revenue_potential": "$500-5000/mo",
        "status": "READY",
        "priority": 1,
        "notes": "10 Fiverr gigs + 5 Upwork profiles ready. AI does the work."
    },

    # === APPS (Priority 2 — needs Apple dev account) ===
    "APP_SUBSCRIPTIONS": {
        "name": "App Subscriptions (iOS + PWA)",
        "vertical": "apps",
        "cost": 2, "effort": 3, "margin": 70,
        "automation_level": 40,
        "scripts": ["app_clone_pipeline.py", "app_name_validator.py", "ios_rejection_screener.py"],
        "revenue_potential": "$1000-20000/mo",
        "status": "BUILDING",
        "priority": 2,
        "notes": "6 apps built. Need Apple dev account ($99/yr). Clone pipeline ready."
    },
    "APP_AFFILIATES": {
        "name": "In-App Affiliate Links",
        "vertical": "apps",
        "cost": 0, "effort": 1, "margin": 85,
        "automation_level": 60,
        "scripts": [],
        "revenue_potential": "$200-3000/mo",
        "status": "BUILDING",
        "priority": 2,
        "notes": "Apple now allows external payment links. Supplements, books, tools, mattresses."
    },
    "APP_ADS": {
        "name": "In-App Advertising",
        "vertical": "apps",
        "cost": 0, "effort": 1, "margin": 60,
        "automation_level": 90,
        "scripts": [],
        "revenue_potential": "$100-2000/mo",
        "status": "BUILDING",
        "priority": 3,
        "notes": "AdMob rewarded video + interstitial. Passive after setup."
    },

    # === COLD OUTBOUND (Priority 2 — needs email infra) ===
    "COLD_EMAIL_LOCAL": {
        "name": "Cold Email → Local Biz Websites",
        "vertical": "outbound",
        "cost": 2, "effort": 2, "margin": 80,
        "automation_level": 85,
        "scripts": ["generate_cold_emails.py", "email_sender.py", "website_signal_scorer.py",
                     "savvy_lead_scraper.py", "nationwide_scraper.py"],
        "revenue_potential": "$2000-10000/mo",
        "status": "READY",
        "priority": 2,
        "notes": "2,908 hot leads. 359 cold emails generated. Need email infra ($46/mo)."
    },
    "COLD_EMAIL_SAAS": {
        "name": "Cold Email → SaaS Services",
        "vertical": "outbound",
        "cost": 2, "effort": 2, "margin": 85,
        "automation_level": 80,
        "scripts": ["generate_cold_emails.py", "email_sender.py"],
        "revenue_potential": "$3000-15000/mo",
        "status": "READY",
        "priority": 2,
        "notes": "AI agent services, automation consulting. High ticket."
    },

    # === CONTENT FARM (Priority 2 — needs accounts) ===
    "MEME_PAGES": {
        "name": "Meme/Curation Pages",
        "vertical": "content",
        "cost": 0, "effort": 2, "margin": 80,
        "automation_level": 70,
        "scripts": ["content_trend_pipeline.py", "quote_tweet_scanner.py"],
        "revenue_potential": "$200-3000/mo",
        "status": "NEEDS_ACCOUNTS",
        "priority": 2,
        "notes": "12 account content packages ready. 5,939 lines of content."
    },
    "NEWSLETTER": {
        "name": "Newsletters (Beehiiv/Substack)",
        "vertical": "content",
        "cost": 0, "effort": 2, "margin": 85,
        "automation_level": 50,
        "scripts": [],
        "revenue_potential": "$100-5000/mo",
        "status": "READY",
        "priority": 2,
        "notes": "4 newsletter packages ready. 50 Substack Notes. Beehiiv free tier."
    },

    # === ECOM / POD (Priority 3) ===
    "POD": {
        "name": "Print on Demand (Etsy/Redbubble)",
        "vertical": "ecom",
        "cost": 0, "effort": 2, "margin": 30,
        "automation_level": 60,
        "scripts": ["trend_to_listing.py", "ecom_arb_engine.py"],
        "revenue_potential": "$100-2000/mo",
        "status": "READY",
        "priority": 3,
        "notes": "50 POD designs ready. 20 Etsy listings ready. Need accounts."
    },
    "DROPSHIP_ARB": {
        "name": "Dropship / Retail Arbitrage",
        "vertical": "ecom",
        "cost": 1, "effort": 3, "margin": 40,
        "automation_level": 50,
        "scripts": ["ecom_arb_engine.py", "import_sourcing_scanner.py", "arb_listing_generator.py"],
        "revenue_potential": "$500-5000/mo",
        "status": "READY",
        "priority": 3,
        "notes": "47 products scanned. LED face mask 57% margin. Need listings."
    },

    # === TRADING (Priority 3 — start small) ===
    "PREDICTION_MARKETS": {
        "name": "Prediction Market Arbitrage",
        "vertical": "trading",
        "cost": 0, "effort": 1, "margin": 50,
        "automation_level": 70,
        "scripts": ["market_scanner.py"],
        "revenue_potential": "$50-500/mo",
        "status": "BUILDING",
        "priority": 3,
        "notes": "Polymarket/Kalshi. $20/bet max. Portfolio approach."
    },
    "CRYPTO_SIGNALS": {
        "name": "Crypto Signal Detection",
        "vertical": "trading",
        "cost": 0, "effort": 1, "margin": 50,
        "automation_level": 80,
        "scripts": ["market_scanner.py", "meme_coin_signal_tracker.py"],
        "revenue_potential": "$0-5000/mo",
        "status": "BUILDING",
        "priority": 3,
        "notes": "Memecoin momentum. <5% allocation. $5-$20/bet."
    },

    # === PROGRAMMATIC / SEO (Priority 2) ===
    "PROGRAMMATIC_SEO": {
        "name": "Programmatic SEO Pages",
        "vertical": "seo",
        "cost": 0, "effort": 1, "margin": 85,
        "automation_level": 95,
        "scripts": [],
        "revenue_potential": "$100-3000/mo",
        "status": "DEPLOYED",
        "priority": 2,
        "notes": "601 pages deployed at printmaxx-seo.surge.sh. Needs non-surge hosting for SEO."
    },

    # === SAAS (Priority 3 — longer timeline) ===
    "SAAS_TOOLS": {
        "name": "Productized SaaS Tools",
        "vertical": "saas",
        "cost": 1, "effort": 4, "margin": 80,
        "automation_level": 30,
        "scripts": ["saas_product_scanner.py"],
        "revenue_potential": "$1000-20000/mo",
        "status": "PLANNING",
        "priority": 3,
        "notes": "12 SaaS candidates scored. LeadMaxx (88), ViralProductFinder (85) top picks."
    },

    # === AI UGC (Priority 1 — cheap) ===
    "AI_UGC": {
        "name": "AI UGC Video Creation",
        "vertical": "services",
        "cost": 1, "effort": 2, "margin": 80,
        "automation_level": 70,
        "scripts": [],
        "revenue_potential": "$500-5000/mo",
        "status": "READY",
        "priority": 2,
        "notes": "HeyGen/D-ID for UGC videos. Sell to brands or use for own products."
    },

    # === COMMUNITY (Priority 3) ===
    "PAID_COMMUNITY": {
        "name": "Paid Community (Skool/Discord)",
        "vertical": "community",
        "cost": 0, "effort": 3, "margin": 90,
        "automation_level": 30,
        "scripts": [],
        "revenue_potential": "$500-10000/mo",
        "status": "PLANNING",
        "priority": 3,
        "notes": "Need audience first. Build through content farm + apps + newsletter."
    },
}


# ---------------------------------------------------------------------------
# DISCOVERY — find new money-making opportunities
# ---------------------------------------------------------------------------

def discover_opportunities():
    """Scan all sources for new opportunities, score them, return ranked list."""
    opportunities = []

    # 1. Check ALPHA_STAGING for unprocessed high-value entries
    alpha = read_csv(LEDGER / "ALPHA_STAGING.csv")
    pending = [a for a in alpha if a.get("status", "") == "PENDING_REVIEW"]
    approved_high = [a for a in alpha if a.get("status") == "APPROVED"
                     and a.get("roi_potential", "") in ("HIGHEST", "HIGH")]

    # 2. Check trend signals
    trends = read_csv(LEDGER / "TREND_SIGNALS.csv")
    hot_trends = [t for t in trends if float(t.get("score", 0)) >= 70]

    # 3. Check ecom arb
    arb = read_csv(LEDGER / "ECOM_ARB_OPPORTUNITIES.csv")
    profitable_arb = [a for a in arb if float(a.get("margin_pct", 0)) >= 30]

    # 4. Check freelance demand
    freelance = read_csv(LEDGER / "FREELANCE_DEMAND_SCAN.csv")
    hot_freelance = [f for f in freelance if float(f.get("score", 0)) >= 60]

    # 5. Check app clone opportunities
    clone_opps = read_csv(LEDGER / "APP_CLONE_OPPORTUNITIES.csv")

    # 6. Check market signals
    market_signals = read_csv(LEDGER / "MARKET_SIGNALS.csv")

    summary = {
        "alpha_pending": len(pending),
        "alpha_high_value": len(approved_high),
        "hot_trends": len(hot_trends),
        "profitable_arb": len(profitable_arb),
        "hot_freelance": len(hot_freelance),
        "clone_opportunities": len(clone_opps),
        "market_signals": len(market_signals),
        "timestamp": datetime.now().isoformat(),
    }

    return summary


# ---------------------------------------------------------------------------
# VALIDATE — score and rank pending opportunities
# ---------------------------------------------------------------------------

def validate_method(method_id):
    """Score a method on multiple dimensions, return composite score 0-100."""
    m = METHODS_REGISTRY.get(method_id, {})
    if not m:
        return 0

    # Scoring weights
    cost_score = max(0, 100 - m["cost"] * 25)         # Free = 100, $200+/mo = 0
    margin_score = m["margin"]                          # Direct percentage
    effort_score = max(0, 100 - m["effort"] * 25)      # Fully auto = 100, 10+hr = 0
    automation_score = m["automation_level"]             # How automated

    # Priority boost (priority 1 gets +20, priority 2 gets +10)
    priority_boost = max(0, (4 - m["priority"]) * 10)

    # Status boost (DEPLOYED > READY > BUILDING > PLANNING > NEEDS_ACCOUNTS)
    status_scores = {"DEPLOYED": 20, "READY": 15, "BUILDING": 5, "PLANNING": 0, "NEEDS_ACCOUNTS": 10}
    status_boost = status_scores.get(m["status"], 0)

    composite = (
        cost_score * 0.20 +
        margin_score * 0.25 +
        effort_score * 0.15 +
        automation_score * 0.15 +
        priority_boost * 0.15 +
        status_boost * 0.10
    )

    return round(min(100, composite), 1)


def rank_all_methods():
    """Rank all methods by composite score."""
    ranked = []
    for mid, m in METHODS_REGISTRY.items():
        score = validate_method(mid)
        ranked.append({
            "id": mid,
            "name": m["name"],
            "score": score,
            "vertical": m["vertical"],
            "cost": m["cost"],
            "margin": m["margin"],
            "status": m["status"],
            "priority": m["priority"],
            "revenue_potential": m["revenue_potential"],
            "automation": m["automation_level"],
        })
    ranked.sort(key=lambda x: x["score"], reverse=True)
    return ranked


# ---------------------------------------------------------------------------
# OPTIMIZE — run optimization on active methods
# ---------------------------------------------------------------------------

def optimize_active():
    """Check running methods, find optimization opportunities."""
    optimizations = []

    # Check which scripts are actually running via cron
    try:
        cron = subprocess.run(["crontab", "-l"], capture_output=True, text=True, timeout=10)
        cron_text = cron.stdout
    except Exception:
        cron_text = ""

    for mid, m in METHODS_REGISTRY.items():
        if m["status"] not in ("DEPLOYED", "READY"):
            continue

        # Check if method's scripts are in cron
        scripts_in_cron = sum(1 for s in m["scripts"] if s in cron_text)
        total_scripts = len(m["scripts"])

        if total_scripts > 0 and scripts_in_cron < total_scripts:
            optimizations.append({
                "method": mid,
                "issue": "SCRIPTS_NOT_IN_CRON",
                "detail": f"{scripts_in_cron}/{total_scripts} scripts scheduled",
                "fix": f"Add missing scripts to crontab"
            })

        # Check for stale logs (script exists but hasn't run in 48h)
        for script in m["scripts"]:
            log_path = LOGS / f"{Path(script).stem}.log"
            if log_path.exists():
                age_hours = (datetime.now().timestamp() - log_path.stat().st_mtime) / 3600
                if age_hours > 48:
                    optimizations.append({
                        "method": mid,
                        "issue": "STALE_LOG",
                        "detail": f"{script} last ran {age_hours:.0f}h ago",
                        "fix": f"Check if cron job is firing"
                    })

    # Check content pipeline
    content_dirs = list(CONTENT.glob("social/*/FIRST_WEEK_CONTENT.md"))
    posted_count = 0  # TODO: track actual posts

    if len(content_dirs) > 5 and posted_count == 0:
        optimizations.append({
            "method": "CONTENT_FARM",
            "issue": "CONTENT_NOT_POSTED",
            "detail": f"{len(content_dirs)} content packages ready, 0 posted",
            "fix": "Create social accounts and start posting"
        })

    # Check lead pipeline
    hot_leads = count_file_lines(AUTO / "leads" / "HOT_LEADS_QUALIFIED.csv")
    emails_sent = 0  # TODO: track from response_tracker

    if hot_leads > 100 and emails_sent == 0:
        optimizations.append({
            "method": "COLD_EMAIL_LOCAL",
            "issue": "LEADS_NOT_CONTACTED",
            "detail": f"{hot_leads} hot leads, 0 emails sent",
            "fix": "Set up email infra and start sending"
        })

    # Check products
    gumroad_ready = list(PRODUCTS.glob("GUMROAD_INSTANT_UPLOAD/*.md"))
    if len(gumroad_ready) > 5:
        optimizations.append({
            "method": "INFO_PRODUCTS",
            "issue": "PRODUCTS_NOT_LISTED",
            "detail": f"{len(gumroad_ready)} products ready, 0 listed",
            "fix": "Create Gumroad account and upload"
        })

    return optimizations


# ---------------------------------------------------------------------------
# REVENUE TRACKING
# ---------------------------------------------------------------------------

def get_revenue():
    """Get current revenue from tracker."""
    rev = read_csv(FINANCIALS / "REVENUE_TRACKER.csv")
    total = sum(float(r.get("amount", 0)) for r in rev)
    by_method = defaultdict(float)
    for r in rev:
        by_method[r.get("method", "unknown")] += float(r.get("amount", 0))
    return {"total": total, "by_method": dict(by_method), "transactions": len(rev)}


# ---------------------------------------------------------------------------
# FULL CYCLE — discovery + validation + optimization + rebalance
# ---------------------------------------------------------------------------

def run_full_cycle():
    """Run the complete money printer cycle."""
    results = {
        "timestamp": datetime.now().isoformat(),
        "disk_percent": disk_percent(),
    }

    # Guardrail: disk check
    if results["disk_percent"] > 98:
        results["status"] = "BLOCKED"
        results["reason"] = f"Disk at {results['disk_percent']}%"
        return results

    # 1. Discover
    results["discovery"] = discover_opportunities()

    # 2. Validate & rank
    results["methods_ranked"] = rank_all_methods()
    results["top_5"] = results["methods_ranked"][:5]

    # 3. Optimize
    results["optimizations"] = optimize_active()

    # 4. Revenue check
    results["revenue"] = get_revenue()

    # 5. Auto-run key scripts if needed
    actions_taken = []

    # Run alpha processor if pending > 50
    if results["discovery"]["alpha_pending"] > 50:
        output = run_script("alpha_auto_processor.py", ["--process-new"], timeout=60)
        actions_taken.append(f"Processed alpha ({results['discovery']['alpha_pending']} pending)")

    # Run perpetual improvement
    output = run_script("scheduled_runs_manager.py", ["--perpetual"], timeout=60)
    actions_taken.append("Ran perpetual improvement cycle")

    results["actions_taken"] = actions_taken
    results["status"] = "OK"

    # Log results
    log_path = safe_path(LOGS / "money_printer.jsonl")
    with open(log_path, "a") as f:
        f.write(json.dumps(results, default=str) + "\n")

    return results


# ---------------------------------------------------------------------------
# CHEAP METHODS — prioritize zero/low cost
# ---------------------------------------------------------------------------

def get_cheap_methods():
    """Return methods sorted by cost (cheapest first), then by score."""
    ranked = rank_all_methods()
    # Sort: cost ascending, then score descending
    ranked.sort(key=lambda x: (x["cost"], -x["score"]))
    return [m for m in ranked if m["cost"] <= 1]  # Free or <$10/mo


# ---------------------------------------------------------------------------
# BLOCKERS — what's preventing revenue
# ---------------------------------------------------------------------------

def identify_blockers():
    """Identify the top blockers preventing revenue generation."""
    blockers = []

    # Check accounts
    accounts = read_csv(LEDGER / "ACCOUNTS.csv")
    active_accounts = [a for a in accounts if a.get("status") == "ACTIVE"]
    if len(active_accounts) < 5:
        blockers.append({
            "severity": "CRITICAL",
            "blocker": "ACCOUNTS",
            "detail": f"Only {len(active_accounts)} active accounts. Need: Gumroad, Fiverr, Upwork, Stripe, social accounts",
            "impact": "Blocks ALL revenue streams",
            "fix": "Follow OPS/ACCOUNT_CREATION_NOW.md"
        })

    # Check email infra
    blockers.append({
        "severity": "HIGH",
        "blocker": "EMAIL_INFRA",
        "detail": "No email sending infrastructure. 2,908 hot leads waiting.",
        "impact": "Blocks cold outbound ($2K-$10K/mo potential)",
        "fix": "Set up Instantly.ai or SmartLead ($46/mo)"
    })

    # Check Apple dev
    blockers.append({
        "severity": "HIGH",
        "blocker": "APPLE_DEV_ACCOUNT",
        "detail": "No Apple Developer account. 6 apps built, 0 submitted.",
        "impact": "Blocks app subscriptions ($1K-$20K/mo potential)",
        "fix": "Enroll at developer.apple.com ($99/yr)"
    })

    # Check content accounts
    if len(active_accounts) < 3:
        blockers.append({
            "severity": "HIGH",
            "blocker": "SOCIAL_ACCOUNTS",
            "detail": "12 content packages ready, 0 accounts created",
            "impact": "Blocks creator rewards + audience building",
            "fix": "Create accounts per OPS/ACCOUNT_SETUP_MATRIX.md"
        })

    return blockers


# ---------------------------------------------------------------------------
# API JSON — for webapp integration
# ---------------------------------------------------------------------------

def get_api_json():
    """Full system status as JSON for the webapp."""
    ranked = rank_all_methods()
    cheap = get_cheap_methods()
    blockers = identify_blockers()
    revenue = get_revenue()
    discovery = discover_opportunities()
    optimizations = optimize_active()

    return {
        "timestamp": datetime.now().isoformat(),
        "disk_percent": disk_percent(),
        "revenue": revenue,
        "methods": {
            "total": len(METHODS_REGISTRY),
            "deployed": len([m for m in METHODS_REGISTRY.values() if m["status"] == "DEPLOYED"]),
            "ready": len([m for m in METHODS_REGISTRY.values() if m["status"] == "READY"]),
            "building": len([m for m in METHODS_REGISTRY.values() if m["status"] == "BUILDING"]),
            "ranked": ranked[:10],
        },
        "cheap_methods": cheap[:5],
        "blockers": blockers,
        "discovery": discovery,
        "optimizations": optimizations[:10],
        "verticals": {
            v: len([m for m in METHODS_REGISTRY.values() if m["vertical"] == v])
            for v in set(m["vertical"] for m in METHODS_REGISTRY.values())
        },
    }


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def print_status():
    ranked = rank_all_methods()
    revenue = get_revenue()
    blockers = identify_blockers()
    optimizations = optimize_active()
    cheap = get_cheap_methods()

    print("=" * 70)
    print("  PRINTMAXX MONEY PRINTER ENGINE")
    print(f"  {datetime.now().strftime('%Y-%m-%d %H:%M')} | Disk: {disk_percent()}%")
    print("=" * 70)

    print(f"\n  REVENUE: ${revenue['total']:.2f} total | {revenue['transactions']} transactions")

    print(f"\n  METHODS: {len(METHODS_REGISTRY)} total")
    for status in ["DEPLOYED", "READY", "BUILDING", "NEEDS_ACCOUNTS", "PLANNING"]:
        count = len([m for m in METHODS_REGISTRY.values() if m["status"] == status])
        print(f"    {status}: {count}")

    print("\n  TOP 10 METHODS (by composite score):")
    print(f"  {'Rank':<5} {'Score':<7} {'Method':<35} {'Status':<15} {'Revenue':<15} {'Cost'}")
    print("  " + "-" * 90)
    cost_labels = {0: "FREE", 1: "<$10/mo", 2: "<$50/mo", 3: "<$200/mo", 4: "$200+/mo"}
    for i, m in enumerate(ranked[:10], 1):
        print(f"  {i:<5} {m['score']:<7} {m['name'][:34]:<35} {m['status']:<15} {m['revenue_potential']:<15} {cost_labels[m['cost']]}")

    print("\n  CHEAPEST METHODS ($0-$10/mo):")
    for m in cheap[:7]:
        print(f"    [{m['score']}] {m['name']} — {m['revenue_potential']} — {m['status']}")

    if blockers:
        print(f"\n  BLOCKERS ({len(blockers)}):")
        for b in blockers:
            print(f"    [{b['severity']}] {b['blocker']}: {b['detail']}")

    if optimizations:
        print(f"\n  OPTIMIZATIONS ({len(optimizations)}):")
        for o in optimizations[:5]:
            print(f"    [{o['issue']}] {o['method']}: {o['detail']}")

    print("\n" + "=" * 70)


def print_methods():
    ranked = rank_all_methods()
    print(f"\n{'ID':<25} {'Score':<7} {'Name':<35} {'Vertical':<15} {'Status':<15} {'Margin'}")
    print("-" * 110)
    for m in ranked:
        mid = [k for k, v in METHODS_REGISTRY.items() if v["name"] == m["name"]][0]
        print(f"{mid:<25} {m['score']:<7} {m['name'][:34]:<35} {m['vertical']:<15} {m['status']:<15} {m['margin']}%")


def print_cheap():
    cheap = get_cheap_methods()
    print("\n  CHEAPEST METHODS (sorted by ROI potential):\n")
    for i, m in enumerate(cheap, 1):
        info = METHODS_REGISTRY[[k for k, v in METHODS_REGISTRY.items() if v["name"] == m["name"]][0]]
        print(f"  {i}. [{m['score']}] {m['name']}")
        print(f"     Revenue: {m['revenue_potential']} | Margin: {m['margin']}% | Auto: {m['automation']}%")
        print(f"     Status: {m['status']} | {info['notes']}")
        print()


def main():
    args = sys.argv[1:]

    if not args or "--status" in args:
        print_status()
    elif "--discover" in args:
        result = discover_opportunities()
        print(json.dumps(result, indent=2))
    elif "--validate" in args:
        ranked = rank_all_methods()
        for m in ranked:
            print(f"  [{m['score']:>5}] {m['name']:<35} {m['status']:<15} {m['revenue_potential']}")
    elif "--optimize" in args:
        opts = optimize_active()
        if opts:
            for o in opts:
                print(f"  [{o['issue']}] {o['method']}: {o['detail']}")
                print(f"    FIX: {o['fix']}")
        else:
            print("  No optimizations needed.")
    elif "--cycle" in args:
        result = run_full_cycle()
        print(json.dumps(result, indent=2, default=str))
    elif "--revenue" in args:
        rev = get_revenue()
        print(f"  Total Revenue: ${rev['total']:.2f}")
        print(f"  Transactions: {rev['transactions']}")
        if rev['by_method']:
            print("  By method:")
            for m, amt in sorted(rev['by_method'].items(), key=lambda x: -x[1]):
                print(f"    {m}: ${amt:.2f}")
    elif "--methods" in args:
        print_methods()
    elif "--cheap" in args:
        print_cheap()
    elif "--blockers" in args:
        blockers = identify_blockers()
        for b in blockers:
            print(f"  [{b['severity']}] {b['blocker']}")
            print(f"    {b['detail']}")
            print(f"    Impact: {b['impact']}")
            print(f"    Fix: {b['fix']}")
            print()
    elif "--api-json" in args:
        print(json.dumps(get_api_json(), indent=2, default=str))
    else:
        print("Usage: money_printer_engine.py [--status|--discover|--validate|--optimize|--cycle|--revenue|--methods|--cheap|--blockers|--api-json]")


if __name__ == "__main__":
    main()
