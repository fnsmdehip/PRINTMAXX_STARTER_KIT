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

from __future__ import annotations

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
from typing import Any, Optional

from agent_resilience import locked_file

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
STRATEGY = PROJECT / "01_STRATEGY"
OPS_GTM = PROJECT / "06_OPERATIONS" / "gtm"
OPS_RESEARCH = PROJECT / "06_OPERATIONS" / "research"
TREND_INTEL = PROJECT / "06_OPERATIONS" / "trend_intel" / "analyses"
EMAIL = PROJECT / "EMAIL"
RESEARCH_DIR = PROJECT / "RESEARCH"
RALPH = PROJECT / "ralph"
CATALOG_PATH = OPS / "INTELLIGENCE_CATALOG.json"
ALPHA_QUERY = AUTOMATIONS / "alpha_query.py"
SQLITE_ALPHA_INDEX = AUTOMATIONS / "sqlite_alpha_index.py"
PYTHON = sys.executable


def safe_path(p: str | Path) -> Path:
    """Verify path is within project root. Raises ValueError if not."""
    resolved = Path(p).resolve()
    if not str(resolved).startswith(str(PROJECT.resolve())):
        raise ValueError(f"BLOCKED: {resolved} outside {PROJECT}")
    return resolved


def ts() -> str:
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
               "distribution", "partnerships", "engagement", "warmup", "grey_hat"],
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
            (MONEY_METHODS / "CONTENT_FARM" / "FB_REELS_GTM.md",
             "FB Reels 440x RPM arbitrage vs YouTube Shorts — same content, 100-440x more revenue, day-by-day execution"),
            (MONEY_METHODS / "CONTENT_FARM" / "YOUTUBE_AI_AUTOMATION_PLAYBOOK.md",
             "Full YouTube AI automation ops — per-video cost $1.15-2.50, July 2025 crackdown details, $1K-3K/mo target"),
            (MONEY_METHODS / "AI_CONTENT_AFFILIATE" / "AI_CONTENT_AFFILIATE_PLAYBOOK.md",
             "Seedance 2.0 + free AI video tools + affiliate = $250-1000/day, $0 stack for 5-8 videos/day"),
            (MONEY_METHODS / "AI_INFLUENCER" / "AI_VIDEO_TOOLS_COMPARISON.md",
             "Feb 2026 AI video tool comparison — 8 tools ranked by quality, Veo 3.1 (9.5/10), free tier specs, paid pricing"),
            (PROJECT / "NICHE_CONTENT_RESEARCH_2025_2026.md",
             "36KB niche content research — viral tweet formats per niche, platform monetization rates, AI UGC tools, pricing benchmarks"),
            (OPS_RESEARCH / "COPY_PSYCHOLOGY_MASTER_REFERENCE.md",
             "Battle-tested psychological frameworks — reply bait Comment Keyword funnel, comments boost reach 10x vs likes"),
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
                CONTENT / "growth" / "buildout" / "G01_G15_growth" / "multi_account_warmup.md",
                CONTENT / "growth" / "buildout" / "G01_G15_growth" / "grey_hat_legal.md",
            ],
            "engagement": [
                GROWTH_OPS / "ENGAGEMENT_FARMING_TACTICS.md",
                CONTENT / "social" / "REPLY_ENGAGEMENT_STRATEGY.md",
                GROWTH_OPS / "EDGE_GROWTH_TACTICS.md",
                GROWTH_OPS / "TWITTER_META_JANUARY_2026.md",
                CONTENT / "growth" / "buildout" / "N_series" / "reply_guy_strategy.md",
                CONTENT / "growth" / "buildout" / "G01_G15_growth" / "platform_algorithm_notes.md",
            ],
            "distribution": [
                GROWTH_OPS / "TWITTER_GROWTH_PLAYBOOK_2026.md",
                GROWTH_OPS / "DM_FUNNEL_PLAYBOOK.md",
                CONTENT / "growth" / "buildout" / "N_series" / "clipper_army_sop.md",
                CONTENT / "growth" / "buildout" / "N_series" / "swarm_promotion.md",
                CONTENT / "growth" / "buildout" / "G01_G15_growth" / "cross_pollination_playbook.md",
            ],
            "repurpose": [
                GROWTH_OPS / "NICHE_POSTING_STRATEGY.md",
                GROWTH_OPS / "TWITTER_GROWTH_PLAYBOOK_2026.md",
                CONTENT / "growth" / "buildout" / "G01_G15_growth" / "cross_pollination_playbook.md",
                CONTENT / "growth" / "buildout" / "N_series" / "medium_substack_strategy.md",
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
             "LinkedIn growth playbook — connection strategy, content, DMs, Depth Score algo"),
            (GROWTH_OPS / "LINKEDIN_ALGORITHM_RESEARCH_2025.md",
             "LinkedIn algorithm research — what gets distribution"),
            (GROWTH_OPS / "EDGE_GROWTH_TACTICS.md",
             "Edge growth tactics — cold email warmup protocols, automation safe limits"),
            (GROWTH_OPS / "GREY_HAT_UPDATE_JAN_2026.md",
             "Grey hat update — cold email warmup tools (MailReach, Warmup Inbox $15/inbox), 2-4 weeks minimum"),
            (GROWTH_OPS / "PLATFORM_AUTOMATION_LIMITS_2026.md",
             "Platform limits — LinkedIn 10-20 connections/day (new), email 25-30/day per inbox, ban recovery"),
            (GROWTH_OPS / "LANDING_PAGE_OPTIMIZATION_GUIDE.md",
             "Landing page optimization — for outbound traffic conversion"),
            (GROWTH_OPS / "GTM_OPTIMIZATION_CHECKLIST.md",
             "GTM optimization checklist — go-to-market readiness"),
            (AUTOMATIONS / "leads" / "COLD_EMAILS_READY_TO_SEND.md",
             "Cold emails ready to deploy — pre-written sequences"),
            (CONTENT / "growth" / "buildout" / "N_series" / "linkedin_automation.md",
             "LinkedIn automation guide — what's ALLOWED vs PROHIBITED, systematic manual outreach SOP"),
            (MONEY_METHODS / "COLD_OUTBOUND" / "TIER1_COLD_EMAIL_SEQUENCES.md",
             "3 vertical cold email sequences (healthcare, SaaS, ecom) — @pipelineabuser style, 6-question framework, case studies with ROI math"),
            (MONEY_METHODS / "COLD_OUTBOUND" / "AUSTIN_LOCAL_BIZ_COLD_EMAIL_SEQUENCES.md",
             "Austin-specific local business cold email sequences — geo-targeted outreach templates"),
            (EMAIL / "GOV_CONTRACT_COLD_EMAIL.md",
             "Government contract cold email templates — Direct Undercut for losing bidders, 6-question framework, A/B subject lines"),
            (EMAIL / "triggering_events" / "competitor_layoff_template.txt",
             "Triggering event cold email — competitor layoff signal, ready-to-send with merge fields"),
        ],
        "dirs": [
            (AUTOMATIONS / "leads",
             "Lead database — local biz leads, competitor reports, bulk leads"),
            (AUTOMATIONS / "email_templates",
             "Email templates — cold outreach, follow-up, closing sequences"),
            (AUTOMATIONS / "freelance_response_templates",
             "Freelance response templates — pre-written proposal responses"),
            (EMAIL / "triggering_events",
             "Triggering event email templates — layoffs, Glassdoor spikes, leadership changes, SEC filings"),
            (EMAIL,
             "All email templates — gov contract, ecom outreach, launch/welcome/reengagement sequences"),
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
                GROWTH_OPS / "EDGE_GROWTH_TACTICS.md",
                GROWTH_OPS / "GREY_HAT_UPDATE_JAN_2026.md",
            ],
            "dm": [
                GROWTH_OPS / "DM_FUNNEL_PLAYBOOK.md",
                GROWTH_OPS / "LINKEDIN_GROWTH_PLAYBOOK_2026.md",
                GROWTH_OPS / "PLATFORM_AUTOMATION_LIMITS_2026.md",
            ],
            "prospecting": [
                GROWTH_OPS / "LINKEDIN_GROWTH_PLAYBOOK_2026.md",
                CONTENT / "growth" / "buildout" / "N_series" / "linkedin_automation.md",
                CONTENT / "growth" / "buildout" / "N_series" / "competitive_intel_reports.md",
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
            (MONEY_METHODS / "APP_FACTORY" / "APP_CLONE_REBRAND_STRATEGY.md",
             "Clone-and-localize strategy — regional arbitrage into Arabic/Spanish/Hindi, 30-app portfolio = $15K-60K/mo"),
            (MONEY_METHODS / "APP_FACTORY" / "COMPETITOR_GTM_TACTICS.md",
             "How Forest/Strava/Duolingo/Calm got first 10K users — real acquisition strategies with real numbers"),
            (MONEY_METHODS / "APP_FACTORY" / "ARB_OPPORTUNITIES_10.md",
             "10 validated app arbitrage opportunities — Arabic Ramadan tracker $30K-200K first year, zero competition gaps"),
            (MONEY_METHODS / "APP_FACTORY" / "APP_DISCOVERY_ENGINE.md",
             "Systematic app discovery engine — finding high-value clone/localize targets at scale"),
            (MONEY_METHODS / "APP_FACTORY" / "TOP_APP_AUDIT.md",
             "Top app audit with revenue data — competitive benchmarks for monetization and retention"),
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
                CONTENT / "growth" / "buildout" / "N_series" / "product_hunt_playbook.md",
                CONTENT / "growth" / "buildout" / "N_series" / "build_in_public.md",
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
            (MONEY_METHODS / "LOCAL_BIZ" / "NATIONWIDE_LEAD_GEN_SYSTEM.md",
             "$500 setup + $99/mo per client recurring — 6 auto-personalized templates, 100 clients = $130K/year"),
            (MONEY_METHODS / "LOCAL_BIZ" / "AI_CALL_OUTREACH.md",
             "AI voice call outreach via Bland.ai ($0.09/min) and Vapi.ai ($0.06-0.08/min) — 2-5% incremental conversion, 200 calls/day = $28/day"),
            (MONEY_METHODS / "LOCAL_BIZ" / "COLD_EMAIL_DEMO_TEMPLATE.md",
             "Cold email with pre-built demo link — show-don't-tell outreach for local biz"),
        ],
        "dirs": [
            (AUTOMATIONS / "leads",
             "Lead database — dentist, contractor, local biz leads by city"),
            (MONEY_METHODS / "LOCAL_BIZ",
             "Local biz method docs — lead gen, AI calling, motion upsell, agency website"),
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
            (STRATEGY / "HEDGE_FUND_INTELLIGENCE_REPORT.md",
             "Top 5 highest-ROI moves ranked — Notion templates $500-10K/mo, app portfolio $5K-185K/mo, tier 1-4 time-to-revenue"),
            (STRATEGY / "METHOD_STACKING_PLAYBOOK.md",
             "10 method stack blueprints with synergy scores 85-95 — revenue multiplier formula 1.3-2.5x synergy x 1.0-3.0x automation"),
            (STRATEGY / "ULTRATHINK_CAPITAL_STACKS.md",
             "Non-obvious stacking — flash sale email hack $15-45K in 48h from 200 subs, 500-clipper network at $0 marginal cost"),
            (MONEY_METHODS / "SKOOL_COMMUNITY" / "SKOOL_LAUNCH_PLAN.md",
             "PRINTMAXX Inner Circle Skool — 3 tiers $0/47/97, ship or get out positioning, week-by-week launch"),
            (MONEY_METHODS / "NEWSLETTER" / "NEWSLETTER_LAUNCH_PLAN.md",
             "The Print Run newsletter on Beehiiv — weekly format, phase 1-3 growth, revenue from boosts + flash sales"),
            (OPS_GTM / "FIRST_1K_REVENUE_PLAN.md",
             "Tactical 7-day sprint to $1,000 — hour-by-hour Day 1, zero budget required"),
            (OPS_GTM / "FASTEST_REVENUE_PATHS_FEB_2026.md",
             "Complete asset inventory ready to sell — 5 Notion templates, Paywall Playbook $27, 105+ posts, 20+ email sequences"),
            (MONEY_METHODS / "SYNERGY_PACKAGES" / "SYNERGY_PACKAGE_COLD_EMAIL_EMPIRE.md",
             "8 synergy stacks scores 85-96 — combined $5K-55K/mo, Clay+Apollo+Instantly, flash sale backend, FOIA lead gen"),
        ],
        "dirs": [
            (MONEY_METHODS,
             "All money methods — APP_FACTORY, POD, ECOM, COLD_OUTBOUND, etc."),
            (DIGITAL_PRODUCTS,
             "Digital products — Gumroad listings, lead magnets, micro products"),
            (PRODUCTS,
             "Products — ARB listings, Etsy, Fiverr, Gumroad ready uploads"),
            (STRATEGY,
             "Strategic planning — capital genesis, method stacking, hedge fund intel"),
            (OPS_GTM,
             "GTM plans — fastest revenue paths, first $1K sprint, Gumroad product specs"),
            (MONEY_METHODS / "SYNERGY_PACKAGES",
             "Synergy package playbooks — cross-method stacking with scored combos"),
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
            (PRODUCTS / "GUMROAD_INSTANT_UPLOAD" / "LISTING_METADATA.md",
             "Gumroad instant upload — 13 product specs with listing metadata, ready to upload"),
            (PRODUCTS / "FIVERR_INSTANT_UPLOAD",
             "Fiverr instant upload — 10 gigs with full specs (website, landing page, cold email, scraping, AI chatbot)"),
            (PRODUCTS / "KDP_JOURNALS_10.md",
             "10 KDP journal specs ready to upload — passive income print products"),
            (PRODUCTS / "WHOP_INSTANT_UPLOAD",
             "Whop instant upload — 8 listing specs ready to deploy"),
            (PRODUCTS / "ETSY_INSTANT_UPLOAD" / "ETSY_LISTINGS_ALL.md",
             "All Etsy listings ready — instant upload specs for Etsy storefront"),
            (PRODUCTS / "ECOM_UPLOAD_CHECKLIST.md",
             "Ecom upload checklist — cross-platform listing readiness tracker"),
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
            (PRODUCTS / "GUMROAD_INSTANT_UPLOAD",
             "Gumroad instant upload — 13 product specs, AI automation kit, cold email playbook, lead machine"),
            (PRODUCTS / "FIVERR_INSTANT_UPLOAD",
             "Fiverr instant upload — 10 gig specs ready to list"),
            (PRODUCTS / "WHOP_INSTANT_UPLOAD",
             "Whop instant upload — 8 listing specs ready to deploy"),
            (PRODUCTS / "ETSY_INSTANT_UPLOAD",
             "Etsy instant upload — all Etsy listings ready"),
            (PRODUCTS / "ECOM_LISTINGS_READY",
             "Ecom listings ready — 15 auto listings, Etsy complete, Redbubble, Gumroad enhanced"),
            (PRODUCTS / "FREELANCE_LISTINGS_READY",
             "Freelance listings ready — 10 Fiverr gigs, multi-platform, 5 Upwork profiles"),
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
            (TREND_INTEL / "CLAVVICULAR_FUNNEL_BREAKDOWN.md",
             "$50-100K/mo reverse-engineered funnel — 750+ clipper army, Framer VSSL to $49/mo Skool to high-ticket"),
            (TREND_INTEL / "COMPETITIVE_LANDSCAPE_MAP.md",
             "Full competitive landscape mapping — competitor positioning and gaps"),
            (OPS_RESEARCH / "YOUTUBE_2026_TACTICS_AND_COMPLIANCE.md",
             "YouTube 2026 inauthentic content crackdown — AI as tool = allowed, AI as entire process = NOT monetizable"),
            (TREND_INTEL / "TREND002_nicksaraev.md",
             "Nick Saraev breakdown — automation agency model, revenue, and tactics"),
            (TREND_INTEL / "TREND007_studytok_productivity_timers.md",
             "StudyTok productivity timer trend — app opportunity analysis"),
            (TREND_INTEL / "TREND008_senada_greca.md",
             "Senada Greca fitness influencer breakdown — funnel and revenue model"),
            (TREND_INTEL / "TREND011_aliabdaal.md",
             "Ali Abdaal funnel breakdown — content to course revenue ladder"),
            (TREND_INTEL / "TREND013_dankoe.md",
             "Dan Koe business model — one-person business, content, digital products"),
            (TREND_INTEL / "TREND014_marclou.md",
             "Marc Lou indie hacker breakdown — rapid shipping model"),
            (TREND_INTEL / "TREND015_tonydinh.md",
             "Tony Dinh indie hacker breakdown — micro-SaaS portfolio"),
            (TREND_INTEL / "TREND016_levelsio.md",
             "Levelsio revenue breakdown — solo founder, multiple products"),
            (TREND_INTEL / "TREND021_waitlist_funnel.md",
             "Waitlist funnel tactics — pre-launch demand generation"),
            (TREND_INTEL / "TREND023_clipping_agency.md",
             "Clipping agency business model — content repurposing as service"),
            (TREND_INTEL / "TREND026_circle_community_model.md",
             "Circle community model — paid community revenue"),
            (TREND_INTEL / "TREND029_skool_case_study.md",
             "Skool case study — community platform revenue deep dive"),
            (TREND_INTEL / "TREND031_pipelineabuser.md",
             "@pipelineabuser tactics breakdown — cold email, scraping, automation"),
            (TREND_INTEL / "TREND033_gregisenberg.md",
             "Greg Isenberg business model — startup studio, community"),
            (TREND_INTEL / "TREND034_dickiebush_nicolascole.md",
             "Dickie Bush/Nicolas Cole writing model — Ship 30, Premium Ghostwriting Academy"),
            (TREND_INTEL / "TREND035_dannypostmaa.md",
             "Danny Postma indie hacker model — AI-powered products"),
            (TREND_INTEL / "TREND036_codyschneiderxx.md",
             "Cody Schneider tactics — programmatic SEO, cold email, rapid experimentation"),
            (TREND_INTEL / "TREND040_tier2_condensed.md",
             "Tier 2 creator breakdowns condensed — multiple secondary creator analyses"),
        ],
        "dirs": [
            (LEDGER / "GROWTH_OPPORTUNITIES",
             "Growth opportunities — dated research findings"),
            (AUTOMATIONS / "research_pipeline_output",
             "Research pipeline output — automated research results"),
            (TREND_INTEL,
             "Trend intelligence analyses — 30+ creator/funnel breakdowns, competitive landscape, tactics"),
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
            (RALPH / ".swarm" / "SWARM_RESEARCH_SUMMARY_FEB2026.md",
             "Feb 2026 swarm research summary — aggregated findings from all scraping tasks"),
            (RALPH / ".swarm" / "output" / "T1_TWITTER_ALPHA.csv",
             "Swarm output — Twitter alpha scraped data"),
            (RALPH / ".swarm" / "output" / "T2_REDDIT_ALPHA.csv",
             "Swarm output — Reddit alpha scraped data"),
            (RALPH / ".swarm" / "output" / "T3_ECOM_ARB.csv",
             "Swarm output — Ecom arbitrage opportunities data"),
            (RALPH / ".swarm" / "output" / "T4_POD_TRENDS.csv",
             "Swarm output — POD trends data"),
            (RALPH / ".swarm" / "output" / "T5_PLATFORM_ARB.csv",
             "Swarm output — Platform arbitrage data"),
            (RALPH / ".swarm" / "output" / "T6_AI_TOOLS_ALPHA.csv",
             "Swarm output — AI tools alpha data"),
        ],
        "dirs": [
            (AUTOMATIONS / "scraper_output",
             "Scraper output — raw scraping results"),
            (AUTOMATIONS / "reddit_scraper_output",
             "Reddit scraper output — subreddit scraping data"),
            (AUTOMATIONS / "twitter_scraper_output",
             "Twitter scraper output — timeline/bookmark scraping"),
            (RALPH / ".swarm" / "output",
             "Ralph swarm output — 6 research CSVs (Twitter, Reddit, Ecom, POD, Platform arb, AI tools)"),
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
            (GROWTH_OPS / "EDGE_GROWTH_TACTICS.md",
             "Aggressive grey-hat growth tactics — Instagram/TikTok/X safe limits, mobile proxies, warmup protocols"),
            (GROWTH_OPS / "GREY_HAT_UPDATE_JAN_2026.md",
             "Grey hat update Jan 2026 — what's DEAD (follow/unfollow), what's ALIVE (warming), what's DYING (pods)"),
            (GROWTH_OPS / "ENGAGEMENT_FARMING_TACTICS.md",
             "Engagement farming — reply guy strategy, reply bait patterns, 1 reply = 4x value of like"),
            (GROWTH_OPS / "TWITTER_GROWTH_PLAYBOOK_2026.md",
             "Twitter growth playbook — Grok-based algo scoring, Premium 4x visibility, small account boost"),
            (GROWTH_OPS / "TWITTER_META_JANUARY_2026.md",
             "Twitter meta Jan 2026 — vibe coding 150K+ views, reply guy validated 3.1M impressions, revenue screenshots viral"),
            (GROWTH_OPS / "DM_FUNNEL_PLAYBOOK.md",
             "DM funnel playbook — keyword funnels 15-30% reply rate, Telegram 5-15% join"),
            (GROWTH_OPS / "LINKEDIN_GROWTH_PLAYBOOK_2026.md",
             "LinkedIn growth 2026 — Depth Score, reach down 50%, first 90 min = 70% reach"),
            (GROWTH_OPS / "PLATFORM_AUTOMATION_LIMITS_2026.md",
             "Platform automation limits — hourly/daily limits for IG/TikTok/X/LinkedIn/YouTube/Email, ban recovery"),
            (GROWTH_OPS / "PLATFORM_UPDATES_JAN_2026.md",
             "Platform updates Jan 2026 — TikTok Oracle algo, IG carousel 2.33% engagement, declining rates"),
            (GROWTH_OPS / "SEO_GEO_ASO_TACTICS_2026.md",
             "SEO/GEO/ASO tactics — E-E-A-T, AI Overview optimization, topic authority clusters"),
            (GROWTH_OPS / "SEO_GEO_ASO_ACTION_PLAN_2026.md",
             "SEO/GEO/ASO action plan — week-by-week execution, quick wins first"),
            (GROWTH_OPS / "GROWTH_EXPERIMENTS_FRAMEWORK.md",
             "Growth experiments — ICE scoring, 30+ experiments, 8.0+ = run immediately"),
            (GROWTH_OPS / "REFERRAL_PROGRAM_TEMPLATES.md",
             "Referral program templates — viral loop mechanics, fraud prevention"),
            (GROWTH_OPS / "LANDING_PAGE_OPTIMIZATION_GUIDE.md",
             "Landing page optimization — 5-second test, 80% conversions above-fold"),
            (GROWTH_OPS / "PUSH_NOTIFICATION_STRATEGY.md",
             "Push notification strategy — app-specific timing, day-of-week patterns"),
            (GROWTH_OPS / "GTM_OPTIMIZATION_CHECKLIST.md",
             "GTM optimization checklist — ASO/SEO/GEO per money method"),
            (GROWTH_OPS / "NICHE_POSTING_STRATEGY.md",
             "Niche posting strategy — reply bait, DM funnel triggers, tech/faith/fitness templates"),
            (GROWTH_OPS / "PARTNERSHIP_OPPORTUNITIES.md",
             "Partnership opportunities — POD/design/ecom partners"),
            (GROWTH_OPS / "X_ALGORITHM_OPTIMIZATION.md",
             "X algorithm optimization — Grok model, Thunder/Phoenix/Home Mixer"),
            (GROWTH_OPS / "SEO_KEYWORD_RESEARCH_GUIDE.md",
             "SEO keyword research — intent types, difficulty assessment, keyword research workflow"),
            (CONTENT / "growth" / "buildout" / "G01_G15_growth" / "grey_hat_legal.md",
             "Grey hat legal guide — ALLOWED/RISKY/ILLEGAL classification per tactic"),
            (CONTENT / "growth" / "buildout" / "G01_G15_growth" / "cross_pollination_playbook.md",
             "Cross-pollination matrix — one input to 4+ output channels across 3 niche pillars"),
            (CONTENT / "growth" / "buildout" / "G01_G15_growth" / "platform_algorithm_notes.md",
             "Platform algorithm notes March 2026 — X 1500 candidates, reply=Very High, link clicks=Very Low"),
            (CONTENT / "growth" / "buildout" / "G01_G15_growth" / "multi_account_warmup.md",
             "Multi-account warmup SOP — 21-30 days, device/IP separation, platform risk rankings"),
            (CONTENT / "growth" / "buildout" / "N_series" / "reply_guy_strategy.md",
             "Reply guy strategy — 500-2000 followers/month at $0, 45-60 min/day, tiered target list"),
            (CONTENT / "growth" / "buildout" / "N_series" / "clipper_army_sop.md",
             "Clipper army SOP — 5-10 secondary accounts for 10x distribution, $0-47/mo"),
            (CONTENT / "growth" / "buildout" / "N_series" / "swarm_promotion.md",
             "Swarm promotion — 4-layer coordinated launch creating FOMO + social proof"),
            (CONTENT / "growth" / "buildout" / "N_series" / "entity_seo.md",
             "Entity SEO — build PRINTMAXX as Google Knowledge Graph entity, 60-90 days to recognition"),
            (CONTENT / "growth" / "buildout" / "N_series" / "product_hunt_playbook.md",
             "Product Hunt launch — top 5 Product of Day drives 500-2000 signups in 24h"),
            (CONTENT / "growth" / "buildout" / "N_series" / "github_trending.md",
             "GitHub trending — 50-200 stars/24h = trending, drives newsletter features + Twitter virality"),
            (CONTENT / "growth" / "buildout" / "N_series" / "build_in_public.md",
             "Build in public — 3-5x conversion vs cold launch, content from free"),
        ],
        "dirs": [
            (GROWTH_OPS, "All growth playbooks and edge tactics"),
            (CONTENT / "growth", "Content growth buildout docs — warmup SOPs, cross-pollination, grey hat legal"),
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
                GROWTH_OPS / "EDGE_GROWTH_TACTICS.md",
                CONTENT / "growth" / "buildout" / "N_series" / "reply_guy_strategy.md",
            ],
            "retention": [
                GROWTH_OPS / "PUSH_NOTIFICATION_STRATEGY.md",
                GROWTH_OPS / "GROWTH_EXPERIMENTS_FRAMEWORK.md",
                GROWTH_OPS / "REFERRAL_PROGRAM_TEMPLATES.md",
            ],
            "viral": [
                GROWTH_OPS / "ENGAGEMENT_FARMING_TACTICS.md",
                GROWTH_OPS / "EDGE_GROWTH_TACTICS.md",
                GROWTH_OPS / "REFERRAL_PROGRAM_TEMPLATES.md",
                CONTENT / "growth" / "buildout" / "N_series" / "clipper_army_sop.md",
                CONTENT / "growth" / "buildout" / "N_series" / "swarm_promotion.md",
            ],
            "referral": [
                GROWTH_OPS / "REFERRAL_PROGRAM_TEMPLATES.md",
                GROWTH_OPS / "PARTNERSHIP_OPPORTUNITIES.md",
            ],
            "seo": [
                GROWTH_OPS / "SEO_GEO_ASO_TACTICS_2026.md",
                GROWTH_OPS / "SEO_GEO_ASO_ACTION_PLAN_2026.md",
                GROWTH_OPS / "SEO_KEYWORD_RESEARCH_GUIDE.md",
                CONTENT / "growth" / "buildout" / "N_series" / "entity_seo.md",
            ],
            "distribution": [
                GROWTH_OPS / "DM_FUNNEL_PLAYBOOK.md",
                GROWTH_OPS / "NICHE_POSTING_STRATEGY.md",
                CONTENT / "growth" / "buildout" / "N_series" / "clipper_army_sop.md",
                CONTENT / "growth" / "buildout" / "N_series" / "swarm_promotion.md",
                CONTENT / "growth" / "buildout" / "N_series" / "product_hunt_playbook.md",
                CONTENT / "growth" / "buildout" / "N_series" / "github_trending.md",
                CONTENT / "growth" / "buildout" / "N_series" / "medium_substack_strategy.md",
            ],
            "partnerships": [
                GROWTH_OPS / "PARTNERSHIP_OPPORTUNITIES.md",
                GROWTH_OPS / "REFERRAL_PROGRAM_TEMPLATES.md",
            ],
            "engagement": [
                GROWTH_OPS / "ENGAGEMENT_FARMING_TACTICS.md",
                GROWTH_OPS / "EDGE_GROWTH_TACTICS.md",
                GROWTH_OPS / "TWITTER_META_JANUARY_2026.md",
                CONTENT / "growth" / "buildout" / "N_series" / "reply_guy_strategy.md",
                CONTENT / "growth" / "buildout" / "G01_G15_growth" / "platform_algorithm_notes.md",
            ],
            "warmup": [
                GROWTH_OPS / "PLATFORM_AUTOMATION_LIMITS_2026.md",
                GROWTH_OPS / "GREY_HAT_UPDATE_JAN_2026.md",
                CONTENT / "growth" / "buildout" / "G01_G15_growth" / "multi_account_warmup.md",
                CONTENT / "growth" / "buildout" / "G01_G15_growth" / "grey_hat_legal.md",
            ],
            "grey_hat": [
                GROWTH_OPS / "EDGE_GROWTH_TACTICS.md",
                GROWTH_OPS / "GREY_HAT_UPDATE_JAN_2026.md",
                GROWTH_OPS / "PLATFORM_AUTOMATION_LIMITS_2026.md",
                CONTENT / "growth" / "buildout" / "G01_G15_growth" / "grey_hat_legal.md",
                CONTENT / "growth" / "buildout" / "G01_G15_growth" / "multi_account_warmup.md",
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

def load_catalog() -> Optional[dict[str, Any]]:
    """Load INTELLIGENCE_CATALOG.json if it exists, merge with hardcoded map."""
    if CATALOG_PATH.exists():
        try:
            with locked_file(CATALOG_PATH, mode="r") as f:
                catalog = json.load(f)
            return catalog
        except Exception:
            pass
    return None


def query_alpha(venture_type: str, top: int = 10) -> list[dict[str, Any]]:
    """Query alpha entries relevant to a venture.

    Tries SQLite FTS5 index first (33ms), falls back to alpha_query.py (slower).
    """
    alpha_venture_map = {
        "APP_FACTORY": "APP_FACTORY",
        "OUTBOUND": "OUTBOUND",
        "CONTENT": "CONTENT",
        "LOCAL_BIZ": "LOCAL_BIZ",
        "MONETIZATION": "MONETIZATION",
        "RESEARCH": "RESEARCH",
        "PRODUCT": "PRODUCT",
        "SCRAPING": "SCRAPING",
        "GROWTH": "CONTENT",
    }
    alpha_venture = alpha_venture_map.get(venture_type.upper(), venture_type.upper())

    # Try SQLite FTS5 index first (much faster)
    if SQLITE_ALPHA_INDEX.exists():
        try:
            result = subprocess.run(
                [PYTHON, str(SQLITE_ALPHA_INDEX),
                 "--venture", alpha_venture, "--status", "APPROVED",
                 "--top", str(top), "--json"],
                capture_output=True, text=True, cwd=str(PROJECT),
                timeout=10
            )
            if result.returncode == 0 and result.stdout.strip():
                return json.loads(result.stdout)
        except (subprocess.TimeoutExpired, json.JSONDecodeError, Exception):
            pass

    # Fallback to alpha_query.py
    if not ALPHA_QUERY.exists():
        return []
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


def find_existing_docs(venture_type: str) -> list[tuple[str, str, bool]]:
    """Return list of (path, description, exists) for a venture's docs.
    Merges hardcoded INTELLIGENCE_MAP with INTELLIGENCE_CATALOG.json."""
    venture_type = venture_type.upper()

    results = []
    seen_paths = set()

    # 1. Hardcoded docs from INTELLIGENCE_MAP
    if venture_type in INTELLIGENCE_MAP:
        config = INTELLIGENCE_MAP[venture_type]
        for path, desc in config.get("docs", []):
            try:
                p = safe_path(path)
                results.append((str(p), desc, p.exists()))
                seen_paths.add(str(p))
            except ValueError:
                continue

    # 2. Merge docs from INTELLIGENCE_CATALOG.json (if it exists)
    catalog = load_catalog()
    if catalog:
        venture_data = catalog.get("ventures", {}).get(venture_type, {})
        for doc in venture_data.get("docs", []):
            doc_path = doc.get("path", "")
            if not doc_path:
                continue
            try:
                full_path = safe_path(PROJECT / doc_path)
                if str(full_path) not in seen_paths:
                    desc = doc.get("summary", doc_path)
                    results.append((str(full_path), desc, full_path.exists()))
                    seen_paths.add(str(full_path))
            except ValueError:
                continue

    return results


def find_existing_dirs(venture_type: str) -> list[tuple[str, str, int, list[str]]]:
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


def find_existing_csvs(venture_type: str) -> list[tuple[str, str, bool, int]]:
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


def find_swarm_reports(venture_type: str, max_reports: int = 5) -> list[tuple[str, str]]:
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


def find_task_docs(venture_type: str, task_type: Optional[str]) -> list[tuple[str, bool]]:
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


def extract_doc_summary(doc_path: str, max_lines: int = 30) -> Optional[str]:
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

def get_intelligence(venture_type: str, task_type: Optional[str] = None, include_summaries: bool = False,
                     alpha_count: int = 10) -> dict[str, Any]:
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

def compute_stats() -> dict[str, Any]:
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

def format_human_output(intel: dict[str, Any], mode: str = "default") -> str:
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


def format_stats_output(stats: dict[str, Any]) -> str:
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


def format_catalog_output() -> str:
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

def main() -> None:
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
