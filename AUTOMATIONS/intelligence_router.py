#!/usr/bin/env python3
"""
INTELLIGENCE ROUTER — The Missing Link Between Intel and Execution
===================================================================

Every agent in the PRINTMAXX system has access to this. Before executing ANY task,
an agent calls get_intelligence() to pull ALL relevant:
  - Alpha entries (scored, ranked, from ALPHA_STAGING.csv via alpha_query.py)
  - Strategy docs (growth playbooks, tactics, platform guides)
  - Swarm reports (latest agent-generated intel)
  - Method CSVs (from LEDGER/)
  - Growth tactics (from 06_OPERATIONS/growth/)

Without this, agents operate on default LLM knowledge. WITH this, they operate
on 10,000+ alpha entries, 25+ growth playbooks, and real competitive intel.

Usage (CLI):
    python3 intelligence_router.py --venture CONTENT --task posting
    python3 intelligence_router.py --venture OUTBOUND --task outreach --json
    python3 intelligence_router.py --venture APP_FACTORY --brief
    python3 intelligence_router.py --venture MONETIZATION --full
    python3 intelligence_router.py --stats
    python3 intelligence_router.py --list-ventures
    python3 intelligence_router.py --catalog

Usage (Module):
    from intelligence_router import get_intelligence
    intel = get_intelligence("CONTENT", task_type="posting")
    # intel["alpha"] = top alpha entries
    # intel["docs"] = relevant strategy doc paths + summaries
    # intel["swarm_reports"] = latest swarm intel
    # intel["methods"] = method-specific CSV paths
    # intel["tactics"] = extracted tactical directives
    # intel["brief"] = one-paragraph summary
"""

import argparse
import csv
import json
import os
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from collections import defaultdict

# ── Paths & Guardrails ─────────────────────────────────────────────────
PROJECT = Path(__file__).resolve().parent.parent
AUTOMATIONS = PROJECT / "AUTOMATIONS"
LEDGER = PROJECT / "LEDGER"
OPS = PROJECT / "OPS"
CONTENT = PROJECT / "CONTENT"
GROWTH_OPS = PROJECT / "06_OPERATIONS" / "growth"
MONEY_METHODS = PROJECT / "MONEY_METHODS"
DIGITAL_PRODUCTS = PROJECT / "DIGITAL_PRODUCTS"
PRODUCTS = PROJECT / "PRODUCTS"
SWARM_REPORTS = AUTOMATIONS / "agent" / "swarm" / "reports"
CATALOG_PATH = OPS / "INTELLIGENCE_CATALOG.json"
ALPHA_QUERY = AUTOMATIONS / "alpha_query.py"
PYTHON = sys.executable


def safe_path(p):
    """Verify path is within project root. Raises ValueError if not."""
    resolved = Path(p).resolve()
    if not str(resolved).startswith(str(PROJECT.resolve())):
        raise ValueError(f"BLOCKED: {resolved} outside {PROJECT}")
    return resolved


def ts():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# ── Venture Type Definitions ───────────────────────────────────────────

VENTURE_TYPES = [
    "CONTENT", "OUTBOUND", "APP_FACTORY", "LOCAL_BIZ",
    "MONETIZATION", "PRODUCT", "RESEARCH", "SCRAPING", "GROWTH",
]

# Task types per venture — narrows intelligence to the most relevant subset
TASK_TYPES = {
    "CONTENT": ["posting", "warmup", "engagement", "distribution", "repurpose",
                "scheduling", "reply", "thread", "carousel", "video"],
    "OUTBOUND": ["outreach", "warmup", "email", "dm", "prospecting",
                 "followup", "qualifying", "closing"],
    "APP_FACTORY": ["launch", "aso", "pricing", "monetization", "retention",
                    "onboarding", "distribution", "update"],
    "LOCAL_BIZ": ["prospecting", "outreach", "demo", "pricing", "closing",
                  "delivery", "upsell"],
    "MONETIZATION": ["pricing", "funnel", "checkout", "upsell", "affiliate",
                     "launch", "listing"],
    "PRODUCT": ["creation", "listing", "pricing", "distribution", "launch",
                "bundle", "upsell"],
    "RESEARCH": ["scraping", "analysis", "scoring", "routing", "monitoring"],
    "SCRAPING": ["setup", "monitoring", "extraction", "analysis", "alerting"],
    "GROWTH": ["acquisition", "retention", "viral", "referral", "seo",
               "distribution", "partnerships"],
}

# ── Document Mapping ───────────────────────────────────────────────────
# Maps venture types to relevant intelligence sources.
# Each entry is a dict with:
#   docs: list of (path, description) tuples
#   dirs: list of (path, description) tuples — all files in dir are relevant
#   csvs: list of (path, description) tuples — LEDGER CSVs
#   task_docs: dict mapping task_type -> list of most relevant doc paths

INTELLIGENCE_MAP = {
    "CONTENT": {
        "docs": [
            (GROWTH_OPS / "TWITTER_GROWTH_PLAYBOOK_2026.md",
             "Full Twitter/X growth strategy — hooks, threads, engagement loops"),
            (GROWTH_OPS / "ENGAGEMENT_FARMING_TACTICS.md",
             "Proven engagement farming patterns — reply bait, QT strategy"),
            (GROWTH_OPS / "EDGE_GROWTH_TACTICS.md",
             "Aggressive growth tactics at the edge of platform rules"),
            (GROWTH_OPS / "NICHE_POSTING_STRATEGY.md",
             "Niche account posting frameworks — timing, format, frequency"),
            (GROWTH_OPS / "DM_FUNNEL_PLAYBOOK.md",
             "DM funnel sequences for converting followers to customers"),
            (GROWTH_OPS / "GREY_HAT_UPDATE_JAN_2026.md",
             "Grey hat tactics update — what still works, what got patched"),
            (GROWTH_OPS / "PLATFORM_AUTOMATION_LIMITS_2026.md",
             "Platform rate limits and automation boundaries to avoid bans"),
            (GROWTH_OPS / "TWITTER_META_JANUARY_2026.md",
             "Current Twitter algorithm meta — what the algo rewards now"),
            (GROWTH_OPS / "X_ALGORITHM_OPTIMIZATION.md",
             "X/Twitter algorithm optimization tactics"),
            (GROWTH_OPS / "TIKTOK_ALGORITHM_RESEARCH_2025.md",
             "TikTok algorithm research — what drives distribution"),
            (GROWTH_OPS / "INSTAGRAM_ALGORITHM_RESEARCH_2025.md",
             "Instagram algorithm research — reels, stories, feed ranking"),
            (GROWTH_OPS / "PINTEREST_ALGORITHM_RESEARCH_2025.md",
             "Pinterest algorithm research — pin distribution mechanics"),
            (CONTENT / "social" / "REPLY_ENGAGEMENT_STRATEGY.md",
             "Reply engagement strategy — systematic reply farming"),
            (CONTENT / "social" / "TIKTOK_VIRAL_STRATEGY_2026.md",
             "TikTok viral strategy — hooks, sounds, posting patterns"),
            (CONTENT / "social" / "TWITTER_PROFILE_SPEC.md",
             "Twitter profile optimization spec — bio, banner, pinned"),
            (PROJECT / "ralph" / "loops" / "social_setup" / "output" / "T5_warmup_schedule.md",
             "Account warmup schedule — day-by-day posting ramp"),
        ],
        "dirs": [
            (CONTENT / "growth" / "buildout",
             "Content growth buildout docs — full growth system construction"),
        ],
        "csvs": [
            (LEDGER / "WINNING_CONTENT_STRUCTURES.csv",
             "Winning content structures — formats with proven engagement"),
            (LEDGER / "ALPHA_CONTENT_LOG.csv",
             "Alpha content tracking log"),
        ],
        "task_docs": {
            "posting": [
                GROWTH_OPS / "NICHE_POSTING_STRATEGY.md",
                GROWTH_OPS / "TWITTER_GROWTH_PLAYBOOK_2026.md",
                GROWTH_OPS / "PLATFORM_AUTOMATION_LIMITS_2026.md",
                CONTENT / "social" / "TWITTER_PROFILE_SPEC.md",
            ],
            "warmup": [
                PROJECT / "ralph" / "loops" / "social_setup" / "output" / "T5_warmup_schedule.md",
                GROWTH_OPS / "PLATFORM_AUTOMATION_LIMITS_2026.md",
                GROWTH_OPS / "GREY_HAT_UPDATE_JAN_2026.md",
            ],
            "engagement": [
                GROWTH_OPS / "ENGAGEMENT_FARMING_TACTICS.md",
                CONTENT / "social" / "REPLY_ENGAGEMENT_STRATEGY.md",
                GROWTH_OPS / "EDGE_GROWTH_TACTICS.md",
            ],
            "distribution": [
                GROWTH_OPS / "TWITTER_GROWTH_PLAYBOOK_2026.md",
                GROWTH_OPS / "DM_FUNNEL_PLAYBOOK.md",
            ],
            "repurpose": [
                GROWTH_OPS / "NICHE_POSTING_STRATEGY.md",
                GROWTH_OPS / "TWITTER_GROWTH_PLAYBOOK_2026.md",
            ],
            "video": [
                CONTENT / "social" / "TIKTOK_VIRAL_STRATEGY_2026.md",
                GROWTH_OPS / "TIKTOK_ALGORITHM_RESEARCH_2025.md",
            ],
        },
    },

    "OUTBOUND": {
        "docs": [
            (GROWTH_OPS / "DM_FUNNEL_PLAYBOOK.md",
             "DM funnel playbook — sequence templates, timing, conversion"),
            (GROWTH_OPS / "LINKEDIN_GROWTH_PLAYBOOK_2026.md",
             "LinkedIn growth playbook — connection strategy, content, DMs"),
            (GROWTH_OPS / "LINKEDIN_ALGORITHM_RESEARCH_2025.md",
             "LinkedIn algorithm research — what gets distribution"),
            (GROWTH_OPS / "LANDING_PAGE_OPTIMIZATION_GUIDE.md",
             "Landing page optimization — for outbound traffic conversion"),
            (GROWTH_OPS / "GTM_OPTIMIZATION_CHECKLIST.md",
             "GTM optimization checklist — go-to-market readiness"),
            (AUTOMATIONS / "leads" / "COLD_EMAILS_READY_TO_SEND.md",
             "Cold emails ready to deploy — pre-written sequences"),
        ],
        "dirs": [
            (AUTOMATIONS / "leads",
             "Lead database — local biz leads, competitor reports, bulk leads"),
            (AUTOMATIONS / "email_templates",
             "Email templates — cold outreach, follow-up, closing sequences"),
            (AUTOMATIONS / "freelance_response_templates",
             "Freelance response templates — pre-written proposal responses"),
        ],
        "csvs": [
            (LEDGER / "MARKETING_CHANNELS_MASTER.csv",
             "Marketing channels master — all channels with performance data"),
        ],
        "task_docs": {
            "outreach": [
                GROWTH_OPS / "DM_FUNNEL_PLAYBOOK.md",
                AUTOMATIONS / "leads" / "COLD_EMAILS_READY_TO_SEND.md",
            ],
            "warmup": [
                GROWTH_OPS / "PLATFORM_AUTOMATION_LIMITS_2026.md",
                GROWTH_OPS / "GREY_HAT_UPDATE_JAN_2026.md",
            ],
            "email": [
                GROWTH_OPS / "DM_FUNNEL_PLAYBOOK.md",
                AUTOMATIONS / "leads" / "COLD_EMAILS_READY_TO_SEND.md",
            ],
            "prospecting": [
                GROWTH_OPS / "LINKEDIN_GROWTH_PLAYBOOK_2026.md",
            ],
            "qualifying": [
                GROWTH_OPS / "GTM_OPTIMIZATION_CHECKLIST.md",
            ],
            "closing": [
                GROWTH_OPS / "LANDING_PAGE_OPTIMIZATION_GUIDE.md",
                GROWTH_OPS / "DM_FUNNEL_PLAYBOOK.md",
            ],
        },
    },

    "APP_FACTORY": {
        "docs": [
            (GROWTH_OPS / "SEO_GEO_ASO_TACTICS_2026.md",
             "SEO/GEO/ASO tactics — app store optimization, keyword strategy"),
            (GROWTH_OPS / "SEO_GEO_ASO_ACTION_PLAN_2026.md",
             "SEO/GEO/ASO action plan — step-by-step execution"),
            (GROWTH_OPS / "SEO_KEYWORD_RESEARCH_GUIDE.md",
             "SEO keyword research guide — finding high-intent keywords"),
            (GROWTH_OPS / "PUSH_NOTIFICATION_STRATEGY.md",
             "Push notification strategy — retention and re-engagement"),
            (GROWTH_OPS / "GROWTH_EXPERIMENTS_FRAMEWORK.md",
             "Growth experiments framework — systematic A/B testing"),
        ],
        "dirs": [
            (MONEY_METHODS / "APP_FACTORY",
             "App factory method docs — all app monetization strategies"),
        ],
        "csvs": [
            (LEDGER / "APP_FACTORY_METHODS.csv",
             "App factory methods — all app-specific alpha and tactics"),
            (LEDGER / "APP_IDEATION_RESULTS.csv",
             "App ideation results — scored app ideas with market data"),
            (LEDGER / "ASO_KEYWORDS.csv",
             "ASO keywords — researched keywords for app store ranking"),
            (LEDGER / "APP_CLONE_OPPORTUNITIES.csv",
             "App clone opportunities — validated clone targets"),
        ],
        "task_docs": {
            "launch": [
                GROWTH_OPS / "SEO_GEO_ASO_ACTION_PLAN_2026.md",
                GROWTH_OPS / "GROWTH_EXPERIMENTS_FRAMEWORK.md",
            ],
            "aso": [
                GROWTH_OPS / "SEO_GEO_ASO_TACTICS_2026.md",
                GROWTH_OPS / "SEO_KEYWORD_RESEARCH_GUIDE.md",
            ],
            "pricing": [
                GROWTH_OPS / "GROWTH_EXPERIMENTS_FRAMEWORK.md",
            ],
            "retention": [
                GROWTH_OPS / "PUSH_NOTIFICATION_STRATEGY.md",
            ],
            "distribution": [
                GROWTH_OPS / "SEO_GEO_ASO_TACTICS_2026.md",
                GROWTH_OPS / "SEO_GEO_ASO_ACTION_PLAN_2026.md",
            ],
        },
    },

    "LOCAL_BIZ": {
        "docs": [
            (GROWTH_OPS / "LANDING_PAGE_OPTIMIZATION_GUIDE.md",
             "Landing page optimization — conversion rate tactics for local biz sites"),
            (GROWTH_OPS / "DM_FUNNEL_PLAYBOOK.md",
             "DM funnel playbook — outreach sequences for local business owners"),
            (GROWTH_OPS / "SEO_GEO_ASO_TACTICS_2026.md",
             "Local SEO tactics — Google Business, local directories, citations"),
            (GROWTH_OPS / "REFERRAL_PROGRAM_TEMPLATES.md",
             "Referral program templates — word-of-mouth for local businesses"),
            (AUTOMATIONS / "openclaw_local_biz.py",
             "OpenClaw local biz engine — discovery/preview/outreach patterns"),
            (AUTOMATIONS / "local_biz_pipeline.py",
             "Local biz pipeline — full find-build-pitch-close automation"),
            (AUTOMATIONS / "leads" / "COLD_EMAILS_READY_TO_SEND.md",
             "Cold emails ready to send — local biz outreach templates"),
        ],
        "dirs": [
            (AUTOMATIONS / "leads",
             "Lead database — dentist, contractor, local biz leads by city"),
        ],
        "csvs": [
            (LEDGER / "MARKETING_CHANNELS_MASTER.csv",
             "Marketing channels — which channels work for local biz outreach"),
        ],
        "task_docs": {
            "prospecting": [
                AUTOMATIONS / "openclaw_local_biz.py",
                AUTOMATIONS / "local_biz_pipeline.py",
            ],
            "outreach": [
                GROWTH_OPS / "DM_FUNNEL_PLAYBOOK.md",
                AUTOMATIONS / "leads" / "COLD_EMAILS_READY_TO_SEND.md",
            ],
            "demo": [
                GROWTH_OPS / "LANDING_PAGE_OPTIMIZATION_GUIDE.md",
            ],
            "pricing": [
                GROWTH_OPS / "REFERRAL_PROGRAM_TEMPLATES.md",
            ],
            "closing": [
                GROWTH_OPS / "DM_FUNNEL_PLAYBOOK.md",
                GROWTH_OPS / "LANDING_PAGE_OPTIMIZATION_GUIDE.md",
            ],
        },
    },

    "MONETIZATION": {
        "docs": [
            (GROWTH_OPS / "REFERRAL_PROGRAM_TEMPLATES.md",
             "Referral program templates — viral loop revenue expansion"),
            (GROWTH_OPS / "LANDING_PAGE_OPTIMIZATION_GUIDE.md",
             "Landing page optimization — conversion funnels for monetization"),
            (GROWTH_OPS / "GROWTH_EXPERIMENTS_FRAMEWORK.md",
             "Growth experiments framework — A/B test pricing and offers"),
            (GROWTH_OPS / "GTM_OPTIMIZATION_CHECKLIST.md",
             "GTM checklist — go-to-market readiness for monetization"),
            (GROWTH_OPS / "PUSH_NOTIFICATION_STRATEGY.md",
             "Push notifications — re-engagement for subscription revenue"),
        ],
        "dirs": [
            (MONEY_METHODS,
             "All money methods — APP_FACTORY, POD, ECOM, COLD_OUTBOUND, etc."),
            (DIGITAL_PRODUCTS,
             "Digital products — Gumroad listings, lead magnets, micro products"),
            (PRODUCTS,
             "Products — ARB listings, Etsy, Fiverr, Gumroad ready uploads"),
        ],
        "csvs": [
            (LEDGER / "ACTIVE_INVESTMENTS.csv",
             "Active investments tracker"),
            (LEDGER / "AD_BUDGET_TRACKER.csv",
             "Ad budget tracking — spend vs ROI"),
        ],
        "task_docs": {
            "pricing": [
                GROWTH_OPS / "GROWTH_EXPERIMENTS_FRAMEWORK.md",
            ],
            "funnel": [
                GROWTH_OPS / "LANDING_PAGE_OPTIMIZATION_GUIDE.md",
                GROWTH_OPS / "DM_FUNNEL_PLAYBOOK.md",
            ],
            "affiliate": [
                GROWTH_OPS / "REFERRAL_PROGRAM_TEMPLATES.md",
                GROWTH_OPS / "PARTNERSHIP_OPPORTUNITIES.md",
            ],
            "launch": [
                GROWTH_OPS / "GTM_OPTIMIZATION_CHECKLIST.md",
                GROWTH_OPS / "GROWTH_EXPERIMENTS_FRAMEWORK.md",
            ],
            "listing": [
                GROWTH_OPS / "SEO_GEO_ASO_TACTICS_2026.md",
                GROWTH_OPS / "LANDING_PAGE_OPTIMIZATION_GUIDE.md",
            ],
        },
    },

    "PRODUCT": {
        "docs": [
            (GROWTH_OPS / "PUSH_NOTIFICATION_STRATEGY.md",
             "Push notification strategy — retention for product users"),
            (GROWTH_OPS / "SEO_GEO_ASO_TACTICS_2026.md",
             "SEO/ASO tactics — discovery and ranking for products"),
            (GROWTH_OPS / "LANDING_PAGE_OPTIMIZATION_GUIDE.md",
             "Landing page optimization — product sales pages"),
            (GROWTH_OPS / "REFERRAL_PROGRAM_TEMPLATES.md",
             "Referral programs — viral loops for product distribution"),
            (GROWTH_OPS / "GROWTH_EXPERIMENTS_FRAMEWORK.md",
             "Growth experiments — test pricing, offers, bundles"),
        ],
        "dirs": [
            (MONEY_METHODS / "POD",
             "Print on demand methods and strategies"),
            (MONEY_METHODS / "DIGITAL_PRODUCTS",
             "Digital product methods — creation, pricing, distribution"),
            (DIGITAL_PRODUCTS,
             "Digital products — ready-to-sell assets, listings, magnets"),
            (PRODUCTS,
             "Products — all product listings and uploads"),
        ],
        "csvs": [],
        "task_docs": {
            "creation": [
                GROWTH_OPS / "GROWTH_EXPERIMENTS_FRAMEWORK.md",
            ],
            "listing": [
                GROWTH_OPS / "SEO_GEO_ASO_TACTICS_2026.md",
                GROWTH_OPS / "LANDING_PAGE_OPTIMIZATION_GUIDE.md",
            ],
            "pricing": [
                GROWTH_OPS / "GROWTH_EXPERIMENTS_FRAMEWORK.md",
            ],
            "distribution": [
                GROWTH_OPS / "SEO_GEO_ASO_TACTICS_2026.md",
                GROWTH_OPS / "REFERRAL_PROGRAM_TEMPLATES.md",
            ],
            "launch": [
                GROWTH_OPS / "GTM_OPTIMIZATION_CHECKLIST.md",
                GROWTH_OPS / "GROWTH_EXPERIMENTS_FRAMEWORK.md",
            ],
        },
    },

    "RESEARCH": {
        "docs": [
            (GROWTH_OPS / "GROWTH_EXPERIMENTS_FRAMEWORK.md",
             "Growth experiments framework — systematic research methodology"),
            (GROWTH_OPS / "PLATFORM_UPDATES_JAN_2026.md",
             "Platform updates — latest changes across all platforms"),
            (GROWTH_OPS / "EDGE_GROWTH_TACTICS.md",
             "Edge growth tactics — aggressive research-driven plays"),
        ],
        "dirs": [
            (LEDGER / "GROWTH_OPPORTUNITIES",
             "Growth opportunities — dated research findings"),
            (AUTOMATIONS / "research_pipeline_output",
             "Research pipeline output — automated research results"),
        ],
        "csvs": [
            (LEDGER / "ALPHA_RESEARCH_RESULTS.csv",
             "Alpha research results — scored research findings"),
            (LEDGER / "BREAKTHROUGH_TOOLS_FEB2026.csv",
             "Breakthrough tools — newly discovered high-value tools"),
        ],
        "task_docs": {
            "analysis": [
                GROWTH_OPS / "GROWTH_EXPERIMENTS_FRAMEWORK.md",
            ],
            "monitoring": [
                GROWTH_OPS / "PLATFORM_UPDATES_JAN_2026.md",
            ],
        },
    },

    "SCRAPING": {
        "docs": [
            (GROWTH_OPS / "PLATFORM_AUTOMATION_LIMITS_2026.md",
             "Platform automation limits — rate limits, ban prevention"),
            (GROWTH_OPS / "PLATFORM_UPDATES_JAN_2026.md",
             "Platform updates — API changes, new restrictions"),
            (GROWTH_OPS / "EDGE_GROWTH_TACTICS.md",
             "Edge tactics — scraping at scale without detection"),
        ],
        "dirs": [
            (AUTOMATIONS / "scraper_output",
             "Scraper output — raw scraping results"),
            (AUTOMATIONS / "reddit_scraper_output",
             "Reddit scraper output — subreddit scraping data"),
            (AUTOMATIONS / "twitter_scraper_output",
             "Twitter scraper output — timeline/bookmark scraping"),
        ],
        "csvs": [
            (LEDGER / "BREAKTHROUGH_TOOLS_FEB2026.csv",
             "Breakthrough tools — scraping tool discoveries"),
        ],
        "task_docs": {
            "setup": [
                GROWTH_OPS / "PLATFORM_AUTOMATION_LIMITS_2026.md",
            ],
            "monitoring": [
                GROWTH_OPS / "PLATFORM_UPDATES_JAN_2026.md",
            ],
        },
    },

    "GROWTH": {
        "docs": [
            (GROWTH_OPS / "TWITTER_GROWTH_PLAYBOOK_2026.md",
             "Twitter growth playbook — full strategy"),
            (GROWTH_OPS / "ENGAGEMENT_FARMING_TACTICS.md",
             "Engagement farming tactics"),
            (GROWTH_OPS / "EDGE_GROWTH_TACTICS.md",
             "Edge growth tactics"),
            (GROWTH_OPS / "DM_FUNNEL_PLAYBOOK.md",
             "DM funnel playbook"),
            (GROWTH_OPS / "LINKEDIN_GROWTH_PLAYBOOK_2026.md",
             "LinkedIn growth playbook"),
            (GROWTH_OPS / "SEO_GEO_ASO_TACTICS_2026.md",
             "SEO/GEO/ASO tactics"),
            (GROWTH_OPS / "SEO_GEO_ASO_ACTION_PLAN_2026.md",
             "SEO/GEO/ASO action plan"),
            (GROWTH_OPS / "GROWTH_EXPERIMENTS_FRAMEWORK.md",
             "Growth experiments framework"),
            (GROWTH_OPS / "REFERRAL_PROGRAM_TEMPLATES.md",
             "Referral program templates"),
            (GROWTH_OPS / "LANDING_PAGE_OPTIMIZATION_GUIDE.md",
             "Landing page optimization"),
            (GROWTH_OPS / "PUSH_NOTIFICATION_STRATEGY.md",
             "Push notification strategy"),
            (GROWTH_OPS / "GTM_OPTIMIZATION_CHECKLIST.md",
             "GTM optimization checklist"),
            (GROWTH_OPS / "NICHE_POSTING_STRATEGY.md",
             "Niche posting strategy"),
            (GROWTH_OPS / "PARTNERSHIP_OPPORTUNITIES.md",
             "Partnership opportunities"),
        ],
        "dirs": [
            (GROWTH_OPS, "All growth playbooks"),
            (CONTENT / "growth", "Content growth docs"),
            (LEDGER / "GROWTH_OPPORTUNITIES", "Growth opportunities research"),
        ],
        "csvs": [
            (LEDGER / "MARKETING_CHANNELS_MASTER.csv",
             "Marketing channels master"),
            (LEDGER / "AB_TESTS_MASTER.csv",
             "A/B test results master"),
            (LEDGER / "AB_EXPERIMENTS_MASTER.csv",
             "A/B experiments master"),
        ],
        "task_docs": {
            "acquisition": [
                GROWTH_OPS / "TWITTER_GROWTH_PLAYBOOK_2026.md",
                GROWTH_OPS / "LINKEDIN_GROWTH_PLAYBOOK_2026.md",
                GROWTH_OPS / "SEO_GEO_ASO_TACTICS_2026.md",
            ],
            "retention": [
                GROWTH_OPS / "PUSH_NOTIFICATION_STRATEGY.md",
                GROWTH_OPS / "GROWTH_EXPERIMENTS_FRAMEWORK.md",
            ],
            "viral": [
                GROWTH_OPS / "ENGAGEMENT_FARMING_TACTICS.md",
                GROWTH_OPS / "EDGE_GROWTH_TACTICS.md",
                GROWTH_OPS / "REFERRAL_PROGRAM_TEMPLATES.md",
            ],
            "referral": [
                GROWTH_OPS / "REFERRAL_PROGRAM_TEMPLATES.md",
                GROWTH_OPS / "PARTNERSHIP_OPPORTUNITIES.md",
            ],
            "seo": [
                GROWTH_OPS / "SEO_GEO_ASO_TACTICS_2026.md",
                GROWTH_OPS / "SEO_GEO_ASO_ACTION_PLAN_2026.md",
                GROWTH_OPS / "SEO_KEYWORD_RESEARCH_GUIDE.md",
            ],
            "distribution": [
                GROWTH_OPS / "DM_FUNNEL_PLAYBOOK.md",
                GROWTH_OPS / "NICHE_POSTING_STRATEGY.md",
            ],
        },
    },
}

# Swarm report keywords per venture — used to find relevant swarm reports
SWARM_REPORT_KEYWORDS = {
    "CONTENT": ["content", "social", "posting", "engagement", "distribution",
                "inbound", "cross_pollination"],
    "OUTBOUND": ["outbound", "lead", "email", "prospect", "competitor"],
    "APP_FACTORY": ["app", "monetization", "conversion", "gap"],
    "LOCAL_BIZ": ["local", "lead", "competitor", "outbound"],
    "MONETIZATION": ["monetization", "conversion", "revenue", "pricing"],
    "PRODUCT": ["product", "conversion", "distribution", "gap"],
    "RESEARCH": ["alpha", "research", "trend", "cross_pollination", "gap"],
    "SCRAPING": ["scraper", "data", "trend", "alpha"],
    "GROWTH": ["growth", "inbound", "distribution", "engagement",
               "cross_pollination", "gap", "conversion"],
}


# ── Core Intelligence Functions ────────────────────────────────────────

def load_catalog():
    """Load INTELLIGENCE_CATALOG.json if it exists, merge with hardcoded map."""
    if CATALOG_PATH.exists():
        try:
            with open(CATALOG_PATH, "r") as f:
                catalog = json.load(f)
            return catalog
        except Exception:
            pass
    return None


def query_alpha(venture_type, top=10):
    """Query alpha_query.py for top alpha entries relevant to a venture."""
    if not ALPHA_QUERY.exists():
        return []

    # Map some venture types to alpha_query venture names
    alpha_venture_map = {
        "APP_FACTORY": "APP_FACTORY",
        "OUTBOUND": "OUTBOUND",
        "CONTENT": "CONTENT",
        "LOCAL_BIZ": "LOCAL_BIZ",
        "MONETIZATION": "MONETIZATION",
        "RESEARCH": "RESEARCH",
        "PRODUCT": "PRODUCT",
        "SCRAPING": "SCRAPING",
        "GROWTH": "CONTENT",  # Growth pulls from content alpha as baseline
    }

    alpha_venture = alpha_venture_map.get(venture_type.upper(), venture_type.upper())

    try:
        result = subprocess.run(
            [PYTHON, str(ALPHA_QUERY),
             "--venture", alpha_venture, "--json", "--top", str(top)],
            capture_output=True, text=True, cwd=str(PROJECT),
            timeout=30
        )
        if result.returncode == 0 and result.stdout.strip():
            return json.loads(result.stdout)
    except (subprocess.TimeoutExpired, json.JSONDecodeError, Exception):
        pass
    return []


def find_existing_docs(venture_type):
    """Return list of (path, description, exists) for a venture's docs."""
    venture_type = venture_type.upper()
    if venture_type not in INTELLIGENCE_MAP:
        return []

    config = INTELLIGENCE_MAP[venture_type]
    results = []

    for path, desc in config.get("docs", []):
        try:
            p = safe_path(path)
            results.append((str(p), desc, p.exists()))
        except ValueError:
            continue

    return results


def find_existing_dirs(venture_type):
    """Return list of (dir_path, description, file_count, files) for directories."""
    venture_type = venture_type.upper()
    if venture_type not in INTELLIGENCE_MAP:
        return []

    config = INTELLIGENCE_MAP[venture_type]
    results = []

    for path, desc in config.get("dirs", []):
        try:
            p = safe_path(path)
            if p.exists() and p.is_dir():
                files = sorted([f for f in p.rglob("*") if f.is_file()
                               and not f.name.startswith(".")
                               and f.suffix in (".md", ".csv", ".py", ".txt", ".json")],
                              key=lambda x: x.stat().st_mtime, reverse=True)
                results.append((str(p), desc, len(files),
                               [str(f) for f in files[:20]]))  # Cap at 20 most recent
            else:
                results.append((str(p), desc, 0, []))
        except (ValueError, OSError):
            continue

    return results


def find_existing_csvs(venture_type):
    """Return list of (path, description, exists, row_count) for LEDGER CSVs."""
    venture_type = venture_type.upper()
    if venture_type not in INTELLIGENCE_MAP:
        return []

    config = INTELLIGENCE_MAP[venture_type]
    results = []

    for path, desc in config.get("csvs", []):
        try:
            p = safe_path(path)
            row_count = 0
            if p.exists():
                try:
                    with open(p, "r", encoding="utf-8", errors="replace") as f:
                        row_count = sum(1 for _ in f) - 1  # minus header
                except Exception:
                    pass
            results.append((str(p), desc, p.exists(), max(0, row_count)))
        except ValueError:
            continue

    return results


def find_swarm_reports(venture_type, max_reports=5):
    """Find the most recent swarm reports relevant to a venture type."""
    venture_type = venture_type.upper()
    keywords = SWARM_REPORT_KEYWORDS.get(venture_type, [])
    if not keywords or not SWARM_REPORTS.exists():
        return []

    relevant = []
    try:
        all_reports = sorted(
            [f for f in SWARM_REPORTS.iterdir()
             if f.is_file() and f.suffix == ".md"],
            key=lambda x: x.stat().st_mtime, reverse=True
        )
    except OSError:
        return []

    for report in all_reports[:50]:  # Check last 50 reports
        name_lower = report.stem.lower()
        score = sum(1 for kw in keywords if kw in name_lower)
        if score > 0:
            relevant.append((score, str(report), report.stem))
            if len(relevant) >= max_reports:
                break

    relevant.sort(key=lambda x: x[0], reverse=True)
    return [(path, name) for _, path, name in relevant[:max_reports]]


def find_task_docs(venture_type, task_type):
    """Get the most relevant docs for a specific task within a venture."""
    venture_type = venture_type.upper()
    task_type = task_type.lower() if task_type else None

    if venture_type not in INTELLIGENCE_MAP:
        return []

    config = INTELLIGENCE_MAP[venture_type]
    task_docs_map = config.get("task_docs", {})

    if task_type and task_type in task_docs_map:
        results = []
        for path in task_docs_map[task_type]:
            try:
                p = safe_path(path)
                results.append((str(p), p.exists()))
            except ValueError:
                continue
        return results

    return []


def extract_doc_summary(doc_path, max_lines=30):
    """Extract key sections from a doc (headers + first few lines under each)."""
    try:
        p = Path(doc_path)
        if not p.exists():
            return None

        with open(p, "r", encoding="utf-8", errors="replace") as f:
            lines = f.readlines()

        if not lines:
            return None

        # Extract title + headers + first substantive content
        summary_parts = []
        header_count = 0
        in_header_section = False

        for i, line in enumerate(lines[:200]):  # First 200 lines max
            stripped = line.strip()

            # Capture headers
            if stripped.startswith("#"):
                header_count += 1
                if header_count <= 15:  # Cap headers
                    summary_parts.append(stripped)
                    in_header_section = True
                    continue

            # Capture first line after header
            if in_header_section and stripped and not stripped.startswith("---"):
                summary_parts.append(f"  {stripped[:150]}")
                in_header_section = False

            # Capture bullet points near top
            if i < 50 and stripped.startswith(("-", "*", "1.", "2.", "3.")):
                summary_parts.append(f"  {stripped[:150]}")

        return "\n".join(summary_parts[:max_lines]) if summary_parts else None

    except Exception:
        return None


# ── Main Intelligence Gatherer ─────────────────────────────────────────

def get_intelligence(venture_type, task_type=None, include_summaries=False,
                     alpha_count=10):
    """
    Main intelligence function. Returns a dict with all relevant intelligence
    for a venture type and optional task type.

    Args:
        venture_type: One of VENTURE_TYPES (CONTENT, OUTBOUND, APP_FACTORY, etc.)
        task_type: Optional task narrowing (posting, warmup, outreach, etc.)
        include_summaries: If True, includes doc content summaries (slower)
        alpha_count: Number of alpha entries to return (default 10)

    Returns:
        dict with keys: alpha, docs, dirs, csvs, swarm_reports, task_docs,
                        tactics, brief, meta
    """
    venture_type = venture_type.upper()

    if venture_type not in INTELLIGENCE_MAP:
        # Try fuzzy matching
        for vt in INTELLIGENCE_MAP:
            if venture_type in vt or vt in venture_type:
                venture_type = vt
                break
        else:
            return {
                "error": f"Unknown venture type: {venture_type}",
                "available": list(INTELLIGENCE_MAP.keys()),
                "alpha": [], "docs": [], "dirs": [], "csvs": [],
                "swarm_reports": [], "task_docs": [], "tactics": [],
                "brief": "", "meta": {},
            }

    # Check for catalog override
    catalog = load_catalog()

    # Gather all intelligence
    alpha = query_alpha(venture_type, top=alpha_count)
    docs = find_existing_docs(venture_type)
    dirs = find_existing_dirs(venture_type)
    csvs = find_existing_csvs(venture_type)
    swarm_reports = find_swarm_reports(venture_type)
    task_docs = find_task_docs(venture_type, task_type) if task_type else []

    # Add doc summaries if requested
    doc_summaries = {}
    if include_summaries:
        for path, desc, exists in docs:
            if exists:
                summary = extract_doc_summary(path)
                if summary:
                    doc_summaries[path] = summary

        for path, exists in task_docs:
            if exists and path not in doc_summaries:
                summary = extract_doc_summary(path)
                if summary:
                    doc_summaries[path] = summary

    # Extract tactical directives from alpha
    tactics = []
    for entry in alpha[:5]:  # Top 5 alpha entries
        tactic = entry.get("tactic", "")
        method = entry.get("extracted_method", "")
        if tactic:
            tactics.append(tactic[:200])
        if method and method != tactic:
            tactics.append(f"METHOD: {method[:200]}")

    # Generate brief
    existing_doc_count = sum(1 for _, _, e in docs if e)
    existing_csv_count = sum(1 for _, _, e, _ in csvs if e)
    alpha_count_actual = len(alpha)

    brief_parts = []
    brief_parts.append(
        f"For {venture_type}"
        + (f" ({task_type})" if task_type else "")
        + f": {alpha_count_actual} alpha entries scored and ranked"
        + f", {existing_doc_count} strategy docs available"
        + f", {existing_csv_count} method CSVs"
        + f", {len(swarm_reports)} recent swarm reports."
    )
    if tactics:
        brief_parts.append(f"Top tactic: {tactics[0][:120]}")
    if task_docs:
        priority_docs = [Path(p).name for p, e in task_docs if e]
        if priority_docs:
            brief_parts.append(
                f"Priority reads for {task_type}: {', '.join(priority_docs[:3])}"
            )

    brief = " ".join(brief_parts)

    meta = {
        "venture_type": venture_type,
        "task_type": task_type,
        "timestamp": ts(),
        "alpha_count": alpha_count_actual,
        "doc_count": existing_doc_count,
        "csv_count": existing_csv_count,
        "swarm_report_count": len(swarm_reports),
        "catalog_loaded": catalog is not None,
        "valid_tasks": TASK_TYPES.get(venture_type, []),
    }

    return {
        "alpha": alpha,
        "docs": [
            {"path": p, "description": d, "exists": e,
             **({"summary": doc_summaries.get(p)} if p in doc_summaries else {})}
            for p, d, e in docs
        ],
        "dirs": [
            {"path": p, "description": d, "file_count": c, "recent_files": f}
            for p, d, c, f in dirs
        ],
        "csvs": [
            {"path": p, "description": d, "exists": e, "row_count": r}
            for p, d, e, r in csvs
        ],
        "swarm_reports": [
            {"path": p, "name": n} for p, n in swarm_reports
        ],
        "task_docs": [
            {"path": p, "exists": e,
             **({"summary": doc_summaries.get(p)} if p in doc_summaries else {})}
            for p, e in task_docs
        ],
        "tactics": tactics,
        "brief": brief,
        "meta": meta,
        **({"doc_summaries": doc_summaries} if doc_summaries else {}),
    }


# ── Statistics & Coverage ──────────────────────────────────────────────

def compute_stats():
    """Compute coverage statistics across all venture types."""
    stats = {}
    total_docs = 0
    total_existing = 0
    total_csvs = 0
    total_csv_existing = 0
    total_alpha = 0
    gaps = []

    for venture_type in INTELLIGENCE_MAP:
        docs = find_existing_docs(venture_type)
        dirs = find_existing_dirs(venture_type)
        csvs = find_existing_csvs(venture_type)
        swarm = find_swarm_reports(venture_type)

        doc_count = len(docs)
        doc_existing = sum(1 for _, _, e in docs if e)
        csv_count = len(csvs)
        csv_existing = sum(1 for _, _, e, _ in csvs if e)
        dir_files = sum(c for _, _, c, _ in dirs)
        total_csv_rows = sum(r for _, _, e, r in csvs if e)

        total_docs += doc_count
        total_existing += doc_existing
        total_csvs += csv_count
        total_csv_existing += csv_existing

        # Find gaps
        missing_docs = [Path(p).name for p, _, e in docs if not e]
        missing_csvs = [Path(p).name for p, _, e, _ in csvs if not e]
        if missing_docs:
            gaps.append((venture_type, "docs", missing_docs))
        if missing_csvs:
            gaps.append((venture_type, "csvs", missing_csvs))

        stats[venture_type] = {
            "docs": doc_count,
            "docs_existing": doc_existing,
            "dirs": len(dirs),
            "dir_files": dir_files,
            "csvs": csv_count,
            "csvs_existing": csv_existing,
            "csv_rows": total_csv_rows,
            "swarm_reports": len(swarm),
            "task_types": len(TASK_TYPES.get(venture_type, [])),
            "missing_docs": missing_docs,
            "missing_csvs": missing_csvs,
        }

    # Query total alpha count
    try:
        alpha_csv = LEDGER / "ALPHA_STAGING.csv"
        if alpha_csv.exists():
            with open(alpha_csv, "r", encoding="utf-8", errors="replace") as f:
                total_alpha = sum(1 for _ in f) - 1
    except Exception:
        pass

    return {
        "ventures": stats,
        "totals": {
            "venture_types": len(INTELLIGENCE_MAP),
            "total_docs_mapped": total_docs,
            "total_docs_existing": total_existing,
            "total_csvs_mapped": total_csvs,
            "total_csvs_existing": total_csv_existing,
            "total_alpha_entries": total_alpha,
            "coverage_pct": round(total_existing / total_docs * 100, 1) if total_docs > 0 else 0,
        },
        "gaps": gaps,
    }


# ── CLI Formatting ─────────────────────────────────────────────────────

def format_human_output(intel, mode="default"):
    """Format intelligence for human-readable CLI output."""
    venture = intel["meta"]["venture_type"]
    task = intel["meta"].get("task_type") or "general"

    lines = []
    lines.append(f"\n{'='*70}")
    lines.append(f"  INTELLIGENCE ROUTER | {venture} | task={task}")
    lines.append(f"  {intel['meta']['timestamp']}")
    lines.append(f"{'='*70}")

    if mode == "brief":
        lines.append(f"\n{intel['brief']}")
        lines.append("")
        return "\n".join(lines)

    # Alpha Intelligence
    alpha = intel.get("alpha", [])
    if alpha:
        lines.append(f"\n  ALPHA INTELLIGENCE ({len(alpha)} entries)")
        lines.append(f"  {'-'*50}")
        for i, entry in enumerate(alpha[:10], 1):
            score = entry.get("score", "?")
            alpha_id = entry.get("alpha_id", "?")
            roi = entry.get("roi_potential", "?")
            status = entry.get("status", "?")
            tactic = (entry.get("tactic") or "")[:100]
            lines.append(f"  [{i:2d}] ({score:3}) {alpha_id} | ROI:{roi} | {status}")
            lines.append(f"       {tactic}")

    # Task-Specific Docs (if task was specified)
    task_docs = intel.get("task_docs", [])
    if task_docs:
        lines.append(f"\n  PRIORITY READS for '{task}'")
        lines.append(f"  {'-'*50}")
        for td in task_docs:
            status = "OK" if td["exists"] else "MISSING"
            name = Path(td["path"]).name
            lines.append(f"  [{status:7s}] {name}")
            lines.append(f"           {td['path']}")
            if td.get("summary") and mode == "full":
                for sline in td["summary"].split("\n")[:5]:
                    lines.append(f"           {sline}")

    # Strategy Docs
    docs = intel.get("docs", [])
    if docs:
        existing = [d for d in docs if d["exists"]]
        missing = [d for d in docs if not d["exists"]]
        lines.append(f"\n  STRATEGY DOCS ({len(existing)} available, {len(missing)} missing)")
        lines.append(f"  {'-'*50}")
        for d in existing:
            name = Path(d["path"]).name
            lines.append(f"  [  OK   ] {name}")
            lines.append(f"            {d['description']}")
            if d.get("summary") and mode == "full":
                for sline in d["summary"].split("\n")[:3]:
                    lines.append(f"            {sline}")
            if mode == "full":
                lines.append(f"            PATH: {d['path']}")
        if missing and mode == "full":
            lines.append(f"\n  MISSING DOCS:")
            for d in missing:
                lines.append(f"  [MISSING] {Path(d['path']).name}")

    # Directories
    dirs = intel.get("dirs", [])
    if dirs and mode == "full":
        lines.append(f"\n  INTELLIGENCE DIRECTORIES")
        lines.append(f"  {'-'*50}")
        for d in dirs:
            lines.append(f"  [{d['file_count']:3d} files] {d['description']}")
            lines.append(f"              {d['path']}")
            if d.get("recent_files"):
                for rf in d["recent_files"][:3]:
                    lines.append(f"              - {Path(rf).name}")

    # CSVs
    csvs = intel.get("csvs", [])
    if csvs:
        existing_csvs = [c for c in csvs if c["exists"]]
        if existing_csvs:
            lines.append(f"\n  METHOD CSVs")
            lines.append(f"  {'-'*50}")
            for c in existing_csvs:
                name = Path(c["path"]).name
                lines.append(f"  [{c['row_count']:5d} rows] {name}")
                lines.append(f"               {c['description']}")
                if mode == "full":
                    lines.append(f"               PATH: {c['path']}")

    # Swarm Reports
    swarm = intel.get("swarm_reports", [])
    if swarm:
        lines.append(f"\n  RECENT SWARM REPORTS")
        lines.append(f"  {'-'*50}")
        for sr in swarm:
            lines.append(f"  - {sr['name']}")
            if mode == "full":
                lines.append(f"    PATH: {sr['path']}")

    # Tactics
    tactics = intel.get("tactics", [])
    if tactics:
        lines.append(f"\n  TOP TACTICS FROM ALPHA")
        lines.append(f"  {'-'*50}")
        for t in tactics[:5]:
            lines.append(f"  > {t[:120]}")

    # Doc summaries in full mode
    if mode == "full" and intel.get("doc_summaries"):
        lines.append(f"\n  DOC SUMMARIES")
        lines.append(f"  {'-'*50}")
        for path, summary in intel["doc_summaries"].items():
            lines.append(f"\n  --- {Path(path).name} ---")
            for sline in summary.split("\n")[:10]:
                lines.append(f"  {sline}")

    # Brief at the end
    lines.append(f"\n  BRIEF: {intel['brief']}")
    lines.append(f"\n  Valid tasks for {venture}: {', '.join(intel['meta'].get('valid_tasks', []))}")
    lines.append("")

    return "\n".join(lines)


def format_stats_output(stats):
    """Format stats for human-readable output."""
    lines = []
    lines.append(f"\n{'='*70}")
    lines.append(f"  INTELLIGENCE ROUTER | COVERAGE STATS")
    lines.append(f"{'='*70}")

    totals = stats["totals"]
    lines.append(f"\n  TOTALS:")
    lines.append(f"    Venture types covered:  {totals['venture_types']}")
    lines.append(f"    Docs mapped:            {totals['total_docs_mapped']}")
    lines.append(f"    Docs existing:          {totals['total_docs_existing']}")
    lines.append(f"    CSVs mapped:            {totals['total_csvs_mapped']}")
    lines.append(f"    CSVs existing:          {totals['total_csvs_existing']}")
    lines.append(f"    Alpha entries:          {totals['total_alpha_entries']:,}")
    lines.append(f"    Doc coverage:           {totals['coverage_pct']}%")

    lines.append(f"\n  {'VENTURE':<18s} {'DOCS':>6s} {'EXIST':>6s} {'DIRS':>6s} "
                 f"{'FILES':>6s} {'CSVs':>6s} {'ROWS':>8s} {'SWARM':>6s} {'TASKS':>6s}")
    lines.append(f"  {'-'*66}")

    for vt, vs in stats["ventures"].items():
        lines.append(
            f"  {vt:<18s} {vs['docs']:>6d} {vs['docs_existing']:>6d} "
            f"{vs['dirs']:>6d} {vs['dir_files']:>6d} "
            f"{vs['csvs_existing']:>6d} {vs['csv_rows']:>8d} "
            f"{vs['swarm_reports']:>6d} {vs['task_types']:>6d}"
        )

    gaps = stats.get("gaps", [])
    if gaps:
        lines.append(f"\n  GAPS (missing files):")
        lines.append(f"  {'-'*50}")
        for vt, gap_type, missing in gaps:
            for m in missing:
                lines.append(f"  [{vt:<15s}] {gap_type}: {m}")

    lines.append("")
    return "\n".join(lines)


def format_catalog_output():
    """Show the full document-to-venture mapping."""
    lines = []
    lines.append(f"\n{'='*70}")
    lines.append(f"  INTELLIGENCE CATALOG — Full Document Mapping")
    lines.append(f"{'='*70}")

    for venture_type, config in sorted(INTELLIGENCE_MAP.items()):
        lines.append(f"\n  {venture_type}")
        lines.append(f"  {'='*len(venture_type)}")

        if config.get("docs"):
            lines.append(f"  Strategy Docs:")
            for path, desc in config["docs"]:
                exists = "OK" if Path(path).exists() else "  "
                lines.append(f"    [{exists}] {Path(path).name}")
                lines.append(f"         {desc}")

        if config.get("dirs"):
            lines.append(f"  Directories:")
            for path, desc in config["dirs"]:
                exists = "OK" if Path(path).exists() else "  "
                lines.append(f"    [{exists}] {path}")
                lines.append(f"         {desc}")

        if config.get("csvs"):
            lines.append(f"  CSVs:")
            for path, desc in config["csvs"]:
                exists = "OK" if Path(path).exists() else "  "
                lines.append(f"    [{exists}] {Path(path).name}")

        if config.get("task_docs"):
            lines.append(f"  Task Specializations:")
            for task, doc_list in config["task_docs"].items():
                doc_names = [Path(p).name for p in doc_list]
                lines.append(f"    {task}: {', '.join(doc_names)}")

    lines.append("")
    return "\n".join(lines)


# ── CLI Entry Point ────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Intelligence Router — pull all relevant intel for any venture/task",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 intelligence_router.py --venture CONTENT --task posting
  python3 intelligence_router.py --venture OUTBOUND --task outreach --json
  python3 intelligence_router.py --venture APP_FACTORY --brief
  python3 intelligence_router.py --venture MONETIZATION --full
  python3 intelligence_router.py --stats
  python3 intelligence_router.py --catalog
  python3 intelligence_router.py --list-ventures
        """
    )
    parser.add_argument("--venture", type=str,
                        help=f"Venture type: {', '.join(VENTURE_TYPES)}")
    parser.add_argument("--task", type=str,
                        help="Task type for narrower intelligence (posting, warmup, outreach, etc.)")
    parser.add_argument("--json", action="store_true",
                        help="Output as JSON for programmatic use")
    parser.add_argument("--brief", action="store_true",
                        help="One-paragraph summary with top 3 actionable tactics")
    parser.add_argument("--full", action="store_true",
                        help="Full output including file paths, summaries, and all details")
    parser.add_argument("--stats", action="store_true",
                        help="Show coverage stats — docs per venture, gaps, totals")
    parser.add_argument("--catalog", action="store_true",
                        help="Show full document-to-venture mapping")
    parser.add_argument("--list-ventures", action="store_true",
                        help="List all venture types and their valid task types")
    parser.add_argument("--alpha-count", type=int, default=10,
                        help="Number of alpha entries to return (default 10)")
    args = parser.parse_args()

    # Stats mode
    if args.stats:
        stats = compute_stats()
        if args.json:
            print(json.dumps(stats, indent=2, default=str))
        else:
            print(format_stats_output(stats))
        return

    # Catalog mode
    if args.catalog:
        print(format_catalog_output())
        return

    # List ventures mode
    if args.list_ventures:
        print(f"\nVENTURE TYPES & TASK TYPES")
        print(f"{'='*50}")
        for vt in sorted(VENTURE_TYPES):
            tasks = TASK_TYPES.get(vt, [])
            print(f"\n  {vt}")
            if tasks:
                print(f"    Tasks: {', '.join(tasks)}")
            else:
                print(f"    Tasks: (none defined)")
        print()
        return

    # Require venture for intelligence query
    if not args.venture:
        parser.print_help()
        print(f"\nAvailable ventures: {', '.join(VENTURE_TYPES)}")
        sys.exit(1)

    # Validate task type
    venture_upper = args.venture.upper()
    if args.task:
        valid_tasks = TASK_TYPES.get(venture_upper, [])
        if valid_tasks and args.task.lower() not in valid_tasks:
            print(f"WARNING: '{args.task}' is not a known task for {venture_upper}.")
            print(f"Valid tasks: {', '.join(valid_tasks)}")
            print(f"Proceeding anyway (will use general intelligence).\n")

    # Get intelligence
    include_summaries = args.full or False
    intel = get_intelligence(
        args.venture,
        task_type=args.task,
        include_summaries=include_summaries,
        alpha_count=args.alpha_count,
    )

    if "error" in intel:
        print(f"ERROR: {intel['error']}")
        print(f"Available venture types: {', '.join(intel.get('available', []))}")
        sys.exit(1)

    # Output
    if args.json:
        # Convert Path objects to strings for JSON serialization
        print(json.dumps(intel, indent=2, default=str))
    elif args.brief:
        print(format_human_output(intel, mode="brief"))
    elif args.full:
        print(format_human_output(intel, mode="full"))
    else:
        print(format_human_output(intel, mode="default"))


if __name__ == "__main__":
    main()
