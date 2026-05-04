#!/usr/bin/env python3

from __future__ import annotations
"""
PRINTMAXX Workflow Wirer — OpenClaw-Style Autonomous Task Generator

Scans ALL existing automations, cron jobs, and workflows in the PRINTMAXX project,
then generates autonomous task queue entries so the supervisor can run them all.

When a script fails, the LLM agent loop figures out alternatives within guardrails.

Usage:
    # Scan and show what would be wired
    python3 AUTOMATIONS/workflow_wirer.py --scan

    # Wire everything into the task queue
    python3 AUTOMATIONS/workflow_wirer.py --wire

    # Wire a specific pipeline
    python3 AUTOMATIONS/workflow_wirer.py --wire --pipeline research

    # Show current wiring status
    python3 AUTOMATIONS/workflow_wirer.py --status

    # Generate daily task set (run at midnight)
    python3 AUTOMATIONS/workflow_wirer.py --daily

    # Dry run (show tasks, don't write to queue)
    python3 AUTOMATIONS/workflow_wirer.py --dry-run
"""

import json
import os
import re
import sys
import subprocess
import argparse
from pathlib import Path
from datetime import datetime, timedelta
from collections import defaultdict

PROJECT_ROOT = Path(__file__).resolve().parent.parent
AUTOMATIONS_DIR = PROJECT_ROOT / "AUTOMATIONS"
QUEUE_PATH = PROJECT_ROOT / "OPS" / "AUTONOMOUS_TASK_QUEUE.jsonl"
WIRING_REGISTRY = PROJECT_ROOT / "OPS" / "WORKFLOW_WIRING_REGISTRY.json"
CRONTAB_V2 = AUTOMATIONS_DIR / "crontab_printmaxx_v2.txt"
CRONTAB_V1 = AUTOMATIONS_DIR / "crontab_printmaxx.txt"
CRON_NEW = AUTOMATIONS_DIR / "new_cron_entries.txt"

# ============================================================
# Pipeline Definitions — Groups of scripts that run together
# Each pipeline maps to a scheduled time window and has
# ordered steps with dependencies
# ============================================================

PIPELINES = {
    "research": {
        "description": "Full alpha research pipeline — scrape all sources, process, score, route",
        "schedule": "05:00",
        "category": "research",
        "priority": 1,
        "risk_level": "LOW",
        "steps": [
            {
                "name": "twitter_scrape",
                "script": "twitter_alpha_scraper.py",
                "flags": "--all",
                "timeout_min": 30,
                "description": "Scrape 116+ high-signal Twitter accounts via Brave cookies",
                "success_criteria": "New tweets extracted, alpha entries appended to ALPHA_STAGING.csv",
            },
            {
                "name": "reddit_scrape",
                "script": "background_reddit_scraper.py",
                "flags": "--scrape",
                "timeout_min": 15,
                "description": "Scrape Reddit JSON API across 41 subreddits",
                "success_criteria": "Reddit posts extracted, alpha entries appended to ALPHA_STAGING.csv",
            },
            {
                "name": "research_orchestrator",
                "script": "daily_research_orchestrator.py",
                "flags": "--full",
                "timeout_min": 45,
                "description": "Master orchestrator: HN + PH + dedup + score 0-100",
                "success_criteria": "All sources scraped, scored, deduped, digest generated",
            },
            {
                "name": "unified_alpha_monitor",
                "script": "unified_alpha_monitor.py",
                "flags": "--full",
                "timeout_min": 30,
                "description": "350+ sources: Reddit niche + GitHub MIT + ASO + competitors + freshness",
                "success_criteria": "Unified digest generated, new alpha entries added",
            },
            {
                "name": "pain_point_miner",
                "script": "reddit_pain_point_miner.py",
                "flags": "--scan",
                "timeout_min": 20,
                "description": "Extract buying intent from 25 subreddits",
                "success_criteria": "Pain points CSV updated with new entries",
            },
            {
                "name": "daily_twitter_scrape",
                "script": "daily_twitter_scraper.py",
                "flags": "",
                "timeout_min": 20,
                "description": "Daily Twitter signal account scraper for alpha extraction",
                "success_criteria": "Twitter signal data scraped, new entries appended to ALPHA_STAGING.csv",
            },
            {
                "name": "daily_reddit_scrape",
                "script": "daily_reddit_scraper.py",
                "flags": "",
                "timeout_min": 15,
                "description": "Daily Reddit subreddit scraper for alpha extraction",
                "success_criteria": "Reddit subreddit data scraped, new entries appended to ALPHA_STAGING.csv",
            },
            {
                "name": "daily_research_pipeline",
                "script": "daily_research_pipeline.py",
                "flags": "--cron",
                "timeout_min": 30,
                "description": "Master research pipeline: scrape, extract, filter, repurpose alpha",
                "success_criteria": "Research pipeline complete, alpha extracted and content repurposed",
                "depends_on": ["daily_twitter_scrape", "daily_reddit_scrape"],
            },
            {
                "name": "alpha_screening",
                "script": "alpha_screening.py",
                "flags": "--pending",
                "timeout_min": 15,
                "description": "Screen new alpha entries with institutional-grade scoring",
                "success_criteria": "Pending alpha entries screened and scored",
                "depends_on": ["daily_research_pipeline"],
            },
            {
                "name": "alpha_to_ops",
                "script": "alpha_to_ops.py",
                "flags": "--cron",
                "timeout_min": 15,
                "description": "Convert approved alpha into actionable ops files",
                "success_criteria": "Approved alpha converted to ops entries, files generated",
                "depends_on": ["alpha_screening"],
            },
            {
                "name": "alpha_processing",
                "script": "alpha_auto_processor.py",
                "flags": "--process-new",
                "timeout_min": 15,
                "description": "Route processed alpha to ventures/OPS/cron/archive",
                "success_criteria": "0 PENDING_REVIEW entries remaining, all routed",
                "depends_on": ["twitter_scrape", "reddit_scrape", "research_orchestrator",
                               "unified_alpha_monitor", "pain_point_miner",
                               "alpha_screening", "alpha_to_ops"],
            },
        ],
    },
    "content": {
        "description": "Content generation from approved alpha — tweets, threads, posts",
        "schedule": "08:00",
        "category": "content",
        "priority": 2,
        "risk_level": "LOW",
        "steps": [
            {
                "name": "content_generation",
                "script": None,  # LLM task, not a script
                "llm_prompt": (
                    "Read LEDGER/ALPHA_STAGING.csv. Find entries with status=APPROVED and score >= 80. "
                    "For the top 5 entries, generate: 1 tweet per entry (consequence-first hook, "
                    "specific numbers, @pipelineabuser voice per .claude/rules/copy-style.md). "
                    "Then pick the single best entry and write a 5-7 tweet thread. "
                    "Save all output to CONTENT/social/auto_generated/{date}_tweets.md "
                    "with PENDING_REVIEW status."
                ),
                "timeout_min": 30,
                "description": "Generate tweets + thread from top approved alpha",
                "success_criteria": "5+ tweets + 1 thread saved with PENDING_REVIEW status",
            },
        ],
    },
    "competitor": {
        "description": "Competitive intelligence — app monitoring, price tracking, market scan",
        "schedule": "07:00",
        "category": "analysis",
        "priority": 3,
        "risk_level": "LOW",
        "steps": [
            {
                "name": "competitor_monitor",
                "script": "competitor_monitor.py",
                "flags": "--scan",
                "timeout_min": 20,
                "description": "Scan 19 apps across 6 niches via iTunes API",
                "success_criteria": "Competitor data updated, changes flagged",
            },
            {
                "name": "app_store_tracker",
                "script": "app_store_competitor_tracker.py",
                "flags": "",
                "timeout_min": 15,
                "description": "Track 36 apps for price/rating/version changes",
                "success_criteria": "Change detection complete, alerts if significant changes",
            },
        ],
    },
    "leads": {
        "description": "Lead qualification and outreach pipeline",
        "schedule": "03:00",
        "category": "building",
        "priority": 4,
        "risk_level": "LOW",
        "steps": [
            {
                "name": "lead_qualification",
                "script": "closed_loop_pipeline.py",
                "flags": "--cycles 3 --batch 1000 --workers 20",
                "timeout_min": 60,
                "description": "Qualify leads: website analysis, scoring, cold email generation",
                "success_criteria": "New leads qualified, emails generated, pipeline metrics updated",
            },
        ],
    },
    "ecom": {
        "description": "Ecom arbitrage scanning and trend-to-listing pipeline",
        "schedule": "09:00",
        "category": "analysis",
        "priority": 4,
        "risk_level": "LOW",
        "steps": [
            {
                "name": "ecom_arb_scan",
                "script": "ecom_arb_engine.py",
                "flags": "--scan --top 10",
                "timeout_min": 20,
                "description": "Scan Amazon/eBay pricing, AliExpress sourcing, calculate margins",
                "success_criteria": "ECOM_ARB_OPPORTUNITIES.csv updated with new products",
            },
            {
                "name": "trend_scan",
                "script": "trend_aggregator.py",
                "flags": "--scan",
                "timeout_min": 15,
                "description": "Google Trends + Reddit + PH viral trend detection",
                "success_criteria": "TREND_SIGNALS.csv updated with new signals",
            },
            {
                "name": "trend_to_listing",
                "script": "trend_to_listing.py",
                "flags": "--scan",
                "timeout_min": 20,
                "description": "Auto-generate POD/Gumroad/Etsy listings from trending products",
                "success_criteria": "New listing drafts generated for trending products",
                "depends_on": ["ecom_arb_scan", "trend_scan"],
            },
        ],
    },
    "freelance": {
        "description": "Freelance demand scanning and pipeline management",
        "schedule": "10:00",
        "category": "analysis",
        "priority": 4,
        "risk_level": "LOW",
        "steps": [
            {
                "name": "freelance_scan",
                "script": "freelance_demand_scanner.py",
                "flags": "--scan",
                "timeout_min": 15,
                "description": "Find active hiring posts on 9 Reddit subreddits",
                "success_criteria": "FREELANCE_DEMAND_SCAN.csv updated with new posts",
            },
            {
                "name": "freelance_pipeline",
                "script": "freelance_pipeline.py",
                "flags": "--daily",
                "timeout_min": 20,
                "description": "Run full daily freelance pipeline: scan + pipeline + portfolio",
                "success_criteria": "Pipeline status updated, new opportunities flagged",
            },
        ],
    },
    "compliance": {
        "description": "Compliance and regulatory scanning",
        "schedule": "08:45",
        "category": "maintenance",
        "priority": 5,
        "risk_level": "LOW",
        "steps": [
            {
                "name": "compliance_deadlines",
                "script": "compliance_deadline_tracker.py",
                "flags": "--check",
                "timeout_min": 10,
                "description": "Check 21 regulatory deadlines, scan RSS for changes",
                "success_criteria": "Compliance digest generated, urgent deadlines flagged",
            },
            {
                "name": "content_compliance",
                "script": "compliance_scanner.py",
                "flags": "--audit-all --save",
                "timeout_min": 20,
                "description": "Scan all publishable content for FTC/CAN-SPAM/PII violations",
                "success_criteria": "Compliance report generated, CRITICAL issues counted",
            },
        ],
    },
    "telegram": {
        "description": "Telegram community monitoring for alpha signals",
        "schedule": "09:15",
        "category": "research",
        "priority": 3,
        "risk_level": "LOW",
        "steps": [
            {
                "name": "telegram_monitor",
                "script": "telegram_community_monitor.py",
                "flags": "--scan",
                "timeout_min": 15,
                "description": "Monitor 26 public Telegram channels across 8 niches",
                "success_criteria": "New signals extracted, high-score entries added to ALPHA_STAGING.csv",
            },
        ],
    },
    "health": {
        "description": "System health check and maintenance",
        "schedule": "12:00",
        "category": "maintenance",
        "priority": 5,
        "risk_level": "LOW",
        "steps": [
            {
                "name": "system_health",
                "script": "system_health_monitor.py",
                "flags": "--check",
                "timeout_min": 10,
                "description": "14-point system health check: cron, pipeline, sites, memory, leads",
                "success_criteria": "Health report with GREEN/AMBER/RED for all 14 points",
            },
            {
                "name": "memory_refresh",
                "script": "memory_manager.py",
                "flags": "--full",
                "timeout_min": 10,
                "description": "Refresh all 3 memory layers: heartbeat, active-tasks, daily log",
                "success_criteria": "HEARTBEAT.md and active-tasks.md updated",
            },
        ],
    },
    "overnight": {
        "description": "Overnight builder — longer running builds, tools, features",
        "schedule": "22:00",
        "category": "building",
        "priority": 4,
        "risk_level": "MEDIUM",
        "steps": [
            {
                "name": "overnight_build",
                "script": None,  # LLM task
                "llm_prompt": (
                    "You are the overnight autonomous builder for PRINTMAXX. "
                    "Read OPS/PERSISTENT_TASK_TRACKER.md for pending tasks. "
                    "Read OPS/HEARTBEAT.md for system state. "
                    "Pick the highest-priority PENDING task that is buildable overnight "
                    "(not blocked on human, not requiring accounts). "
                    "Build it fully: write code, run it, show output, save results. "
                    "Update the task tracker with DONE status and proof. "
                    "If the task involves creating a script, run it and capture output."
                ),
                "timeout_min": 120,
                "description": "Pick and execute highest-priority pending build task",
                "success_criteria": "At least 1 task moved from PENDING to DONE with proof",
            },
        ],
    },
    "retrospective": {
        "description": "Daily retrospective — review runs, extract learnings, improve",
        "schedule": "22:30",
        "category": "self_improvement",
        "priority": 6,
        "risk_level": "LOW",
        "steps": [
            {
                "name": "retrospective",
                "script": None,  # LLM task
                "llm_prompt": (
                    "Review today's autonomous run logs in AUTOMATIONS/logs/autonomous/. "
                    "Identify: what took longer than expected, what failed and why, "
                    "what patterns emerge, what should be changed. "
                    "Write 3+ specific learnings (not generic) to LEDGER/RBI_STRATEGIC/LEARNINGS.jsonl. "
                    "Each learning must be actionable: 'Do X instead of Y because Z.'"
                ),
                "timeout_min": 30,
                "description": "Review logs, extract learnings, write to LEARNINGS.jsonl",
                "success_criteria": "3+ specific learnings appended to LEARNINGS.jsonl",
            },
        ],
    },
    "app_ideation": {
        "description": "App ideation — scan trends, find app ideas, score viability",
        "schedule": "06:00",
        "category": "research",
        "priority": 3,
        "risk_level": "LOW",
        "steps": [
            {
                "name": "app_ideation_scan",
                "script": "app_ideation_specialist.py",
                "flags": "--scan",
                "timeout_min": 30,
                "description": "Full trend scan: Google Trends, Reddit, TikTok, YouTube + gap analysis + scoring",
                "success_criteria": "Ideas scored 16/20+ saved to LEDGER/APP_IDEATION_RESULTS.csv",
            },
        ],
    },
    "venture_tracking": {
        "description": "Track venture performance and recommend KILL/MAINTAIN/DOUBLE_DOWN",
        "schedule": "16:00",
        "category": "analysis",
        "priority": 4,
        "risk_level": "LOW",
        "steps": [
            {
                "name": "venture_performance",
                "script": "venture_performance_tracker.py",
                "flags": "--recommend",
                "timeout_min": 10,
                "description": "Score all methods 0-100, recommend actions",
                "success_criteria": "Venture report generated with recommendations",
            },
        ],
    },
    # ============================================================
    # NEW PIPELINES — Added by workflow_wirer expansion
    # Covers 16 additional script categories (~60 scripts)
    # ============================================================
    "lead_qualification": {
        "description": "Full lead qualification pipeline — scrape, score, enrich, qualify leads",
        "schedule": "03:30",
        "category": "building",
        "priority": 2,
        "risk_level": "LOW",
        "steps": [
            {
                "name": "closed_loop_qualify",
                "script": "closed_loop_pipeline.py",
                "flags": "--cycles 3 --batch 500 --workers 15",
                "timeout_min": 45,
                "description": "Run closed-loop lead qualification: website analysis + scoring + email gen",
                "success_criteria": "New leads qualified, pipeline_metrics.jsonl updated with cycle stats",
            },
            {
                "name": "intelligent_qualify",
                "script": "intelligent_lead_qualifier.py",
                "flags": "--analyze --batch 2000 --workers 20",
                "timeout_min": 60,
                "description": "Quant-level lead qualification: pre-filter + website analysis + 0-100 scoring",
                "success_criteria": "HOT_LEADS_QUALIFIED.csv and WARM_LEADS_QUALIFIED.csv updated",
                "depends_on": ["closed_loop_qualify"],
            },
            {
                "name": "lead_enrich",
                "script": "lead_enrichment.py",
                "flags": "--enrich --top 100",
                "timeout_min": 30,
                "description": "Enrich top leads with Google rating, social presence, tech stack, competitors",
                "success_criteria": "Enriched leads CSV updated with social/tech/competitor data",
                "depends_on": ["intelligent_qualify"],
            },
            {
                "name": "website_scoring",
                "script": "website_signal_scorer.py",
                "flags": "--input AUTOMATIONS/leads/HOT_LEADS.csv",
                "timeout_min": 30,
                "description": "Score hot lead websites 0-100 across 15 signals (design, SEO, AIO/GIO)",
                "success_criteria": "SCORED_LEADS.csv updated with website scores for all hot leads",
                "depends_on": ["lead_enrich"],
            },
        ],
    },
    "cold_outreach": {
        "description": "Cold email generation, A/B testing, sending (dry-run), and response tracking",
        "schedule": "04:00",
        "category": "building",
        "priority": 2,
        "risk_level": "MEDIUM",
        "steps": [
            {
                "name": "generate_emails",
                "script": "generate_cold_emails.py",
                "flags": "--min-score 40 --dry-run",
                "timeout_min": 20,
                "description": "Generate personalized 3-email sequences from scored leads with demo URLs",
                "success_criteria": "Cold emails CSV generated with personalized sequences",
            },
            {
                "name": "email_variant_gen",
                "script": "cold_email_2026.py",
                "flags": "--generate",
                "timeout_min": 15,
                "description": "Generate 2026-optimized cold email variants with updated hooks and CTAs",
                "success_criteria": "New email variants written to outreach directory",
                "depends_on": ["generate_emails"],
            },
            {
                "name": "ab_test_split",
                "script": "cold_email_ab_test.py",
                "flags": "--split --limit 200",
                "timeout_min": 10,
                "description": "Hash-based A/B split of email variants with chi-square significance testing",
                "success_criteria": "A/B split CSV generated with variant assignments",
                "depends_on": ["email_variant_gen"],
            },
            {
                "name": "email_send",
                "script": "email_sender.py",
                "flags": "--dry-run",
                "timeout_min": 15,
                "description": "Preview cold email sends via smtplib (dry-run, no actual sends)",
                "success_criteria": "Dry-run log showing email previews, rate limits respected",
                "depends_on": ["ab_test_split"],
            },
            {
                "name": "response_track",
                "script": "response_tracker.py",
                "flags": "dashboard",
                "timeout_min": 10,
                "description": "Track campaign funnel: QUEUED to SENT to OPENED to REPLIED to BOOKED to CLOSED",
                "success_criteria": "Campaign funnel dashboard updated with open/reply/book rates",
                "depends_on": ["email_send"],
            },
            {
                "name": "email_domain_health",
                "script": "email_domain_health.py",
                "flags": "--check-all",
                "timeout_min": 15,
                "description": "Check email domain health: SPF, DKIM, DMARC, MX, blacklist, domain age (weekly)",
                "success_criteria": "Email domain health scores updated, issues flagged",
                "depends_on": ["response_track"],
            },
            {
                "name": "seo_competitor_analysis",
                "script": "seo_competitor_analyzer.py",
                "flags": "--summary",
                "timeout_min": 20,
                "description": "SEO competitor analysis for cold outreach targeting intel",
                "success_criteria": "SEO competitor data updated with competitive grouping and cold email snippets",
                "depends_on": ["email_domain_health"],
            },
        ],
    },
    "ecom_operations": {
        "description": "Full ecom arbitrage pipeline — scan, distribute, autopilot, list",
        "schedule": "09:30",
        "category": "analysis",
        "priority": 3,
        "risk_level": "LOW",
        "steps": [
            {
                "name": "ecom_arb",
                "script": "ecom_arb_engine.py",
                "flags": "--scan --top 15",
                "timeout_min": 25,
                "description": "Scan Amazon/eBay pricing vs AliExpress sourcing, calculate net margins",
                "success_criteria": "ECOM_ARB_OPPORTUNITIES.csv updated with profitable products",
            },
            {
                "name": "ecom_arb_scanner",
                "script": "ecom_arb_scanner.py",
                "flags": "",
                "timeout_min": 20,
                "description": "Weekly ecom arbitrage scanner for product opportunities (Monday)",
                "success_criteria": "Ecom arbitrage opportunities identified and logged",
                "depends_on": ["ecom_arb"],
            },
            {
                "name": "trending_products",
                "script": "trending_products_scanner.py",
                "flags": "",
                "timeout_min": 15,
                "description": "Scan for trending products across platforms (weekly Monday)",
                "success_criteria": "Trending products identified and added to opportunities list",
                "depends_on": ["ecom_arb_scanner"],
            },
            {
                "name": "ecom_distribute",
                "script": "ecom_distributor.py",
                "flags": "--distribute-all",
                "timeout_min": 20,
                "description": "Distribute listings across all connected ecom platforms",
                "success_criteria": "Products distributed to target platforms, distribution log updated",
                "depends_on": ["ecom_arb"],
            },
            {
                "name": "ecom_auto",
                "script": "ecom_autopilot.py",
                "flags": "--run",
                "timeout_min": 30,
                "description": "Autopilot ecom operations: restock alerts, repricing, order routing",
                "success_criteria": "Autopilot cycle complete, alerts generated for low-stock items",
                "depends_on": ["ecom_distribute"],
            },
            {
                "name": "viral_scan",
                "script": "viral_product_scanner.py",
                "flags": "--keywords trending",
                "timeout_min": 20,
                "description": "Scan FB Ads Library for validated viral products with spend signals",
                "success_criteria": "Viral product candidates identified with ad spend estimates",
            },
            {
                "name": "trend_listings",
                "script": "trend_to_listing.py",
                "flags": "--scan",
                "timeout_min": 20,
                "description": "Auto-generate POD/Gumroad/Etsy listings from trending products",
                "success_criteria": "New listing drafts generated for trending products",
                "depends_on": ["viral_scan", "ecom_arb"],
            },
            {
                "name": "arb_listings",
                "script": "arb_listing_generator.py",
                "flags": "--generate",
                "timeout_min": 15,
                "description": "Generate FB Marketplace/eBay/Mercari listings from arb scan data",
                "success_criteria": "Copy-paste listings generated in ARB_LISTINGS directory",
                "depends_on": ["trend_listings"],
            },
        ],
    },
    "freelance_pipeline": {
        "description": "Freelance demand scanning, auto-responding (dry-run), and pipeline management",
        "schedule": "10:30",
        "category": "building",
        "priority": 3,
        "risk_level": "LOW",
        "steps": [
            {
                "name": "freelance_scan",
                "script": "freelance_demand_scanner.py",
                "flags": "--scan",
                "timeout_min": 15,
                "description": "Scan 9 Reddit subreddits for active hiring posts matched to AI services",
                "success_criteria": "FREELANCE_DEMAND_SCAN.csv updated with new posts and scores",
            },
            {
                "name": "freelance_respond",
                "script": "auto_freelance_responder.py",
                "flags": "--dry-run",
                "timeout_min": 15,
                "description": "Auto-generate responses for matched freelance posts (dry-run, no sends)",
                "success_criteria": "Response drafts generated in outreach directory for review",
                "depends_on": ["freelance_scan"],
            },
            {
                "name": "freelance_manage",
                "script": "freelance_pipeline.py",
                "flags": "--daily",
                "timeout_min": 20,
                "description": "Full daily freelance pipeline: scan + pipeline status + portfolio update",
                "success_criteria": "FREELANCE_PIPELINE_ACTIVE.csv updated, new opportunities flagged",
                "depends_on": ["freelance_respond"],
            },
        ],
    },
    "local_biz_pipeline": {
        "description": "Local business lead gen — scrape, analyze websites, personalize demos, outreach",
        "schedule": "11:00",
        "category": "building",
        "priority": 3,
        "risk_level": "MEDIUM",
        "steps": [
            {
                "name": "local_biz_scrape",
                "script": "local_biz_website_scraper.py",
                "flags": "--scan",
                "timeout_min": 20,
                "description": "Scrape local business websites for quality signals and contact info",
                "success_criteria": "Local biz lead data extracted with website quality scores",
            },
            {
                "name": "nationwide_leads",
                "script": "nationwide_scraper.py",
                "flags": "--cities AUTOMATIONS/cities_top200.csv --industries dentist,plumber,lawyer --max-cities 5",
                "timeout_min": 45,
                "description": "Scrape leads across 203 cities with 0-100 scoring (5 cities per run)",
                "success_criteria": "New leads appended to nationwide leads CSV with scores",
                "depends_on": ["local_biz_scrape"],
            },
            {
                "name": "personalize",
                "script": "personalize_demos.py",
                "flags": "--top 50",
                "timeout_min": 20,
                "description": "Generate personalized demo landing pages for top scored leads",
                "success_criteria": "Personalized demo HTML files generated in output/personalized_demos/",
                "depends_on": ["nationwide_leads"],
            },
            {
                "name": "local_biz_pipeline_run",
                "script": "local_biz_pipeline.py",
                "flags": "--dry-run",
                "timeout_min": 25,
                "description": "Full local biz pipeline: scrape, analyze, generate cold emails (dry-run)",
                "success_criteria": "Pipeline run complete, cold email drafts generated for review",
                "depends_on": ["personalize"],
            },
            {
                "name": "mass_outreach_preview",
                "script": "mass_outreach.py",
                "flags": "--dry-run --min-score 60",
                "timeout_min": 15,
                "description": "Preview mass outreach 4-email sequences for qualified leads (dry-run)",
                "success_criteria": "Outreach preview log showing email sequences, no actual sends",
                "depends_on": ["local_biz_pipeline_run"],
            },
        ],
    },
    "content_production": {
        "description": "Content multiplication — metrics-driven content, engagement bait, self-reply funnels",
        "schedule": "08:30",
        "category": "content",
        "priority": 2,
        "risk_level": "LOW",
        "steps": [
            {
                "name": "content_multiply",
                "script": "content_multiplier.py",
                "flags": "--multiply",
                "timeout_min": 20,
                "description": "Multiply one piece of content into 20+ variants across platforms",
                "success_criteria": "Content variants generated for X, LinkedIn, Reddit, newsletter",
            },
            {
                "name": "metrics_content",
                "script": "auto_content_from_metrics.py",
                "flags": "--generate",
                "timeout_min": 15,
                "description": "Auto-generate content from performance metrics (what worked, real numbers)",
                "success_criteria": "Metric-driven posts generated in CONTENT/social/auto_generated/",
                "depends_on": ["content_multiply"],
            },
            {
                "name": "engagement_convert",
                "script": "engagement_bait_converter.py",
                "flags": "--convert",
                "timeout_min": 15,
                "description": "Convert high-engagement alpha into niche account posts with hooks",
                "success_criteria": "Engagement bait posts generated for each niche account",
                "depends_on": ["metrics_content"],
            },
            {
                "name": "self_reply",
                "script": "self_reply_funnel.py",
                "flags": "--generate",
                "timeout_min": 10,
                "description": "Generate self-reply thread funnels: hook, value, CTA chain",
                "success_criteria": "Self-reply thread drafts saved to content queue as PENDING_REVIEW",
                "depends_on": ["engagement_convert"],
            },
            {
                "name": "viral_content_scan",
                "script": "viral_content_scanner.py",
                "flags": "--scan --limit 50",
                "timeout_min": 15,
                "description": "Detect viral content patterns for content farm strategy",
                "success_criteria": "Viral content patterns identified and logged for replication",
                "depends_on": ["self_reply"],
            },
            {
                "name": "auto_content_post",
                "script": "auto_content_poster.py",
                "flags": "--post-next",
                "timeout_min": 15,
                "description": "Post approved content from queue to connected platforms",
                "success_criteria": "Approved content posted, posting log updated",
                "depends_on": ["viral_content_scan"],
            },
        ],
    },
    "voice_pipeline": {
        "description": "Voice content pipeline — approved script to audio via TTS",
        "schedule": "14:00",
        "category": "content",
        "priority": 4,
        "risk_level": "LOW",
        "steps": [
            {
                "name": "voice_runner",
                "script": "approved_script_voice_runner.py",
                "flags": "--run",
                "timeout_min": 30,
                "description": "Run approved scripts through voice generation pipeline",
                "success_criteria": "Audio files generated from approved scripts in output directory",
            },
            {
                "name": "tts_longform",
                "script": "qwen3_tts_longform.py",
                "flags": "--generate",
                "timeout_min": 45,
                "description": "Generate longform TTS audio using Qwen3 model for podcasts/narration",
                "success_criteria": "Longform audio files generated, quality check passed",
                "depends_on": ["voice_runner"],
            },
        ],
    },
    "app_intelligence": {
        "description": "App market intelligence — competitor tracking, clone finding, ideation",
        "schedule": "06:30",
        "category": "research",
        "priority": 3,
        "risk_level": "LOW",
        "steps": [
            {
                "name": "app_store_track",
                "script": "app_store_competitor_tracker.py",
                "flags": "",
                "timeout_min": 15,
                "description": "Track 36 apps for price/rating/version changes via iTunes API",
                "success_criteria": "Change detection complete, significant changes flagged",
            },
            {
                "name": "app_clone_scan",
                "script": "app_clone_finder.py",
                "flags": "--scan",
                "timeout_min": 20,
                "description": "Find successful apps that can be cloned for different niches/regions",
                "success_criteria": "Clone candidates identified with revenue estimates and niche gaps",
                "depends_on": ["app_store_track"],
            },
            {
                "name": "aso_keyword_research",
                "script": "aso_keyword_research.py",
                "flags": "",
                "timeout_min": 20,
                "description": "ASO keyword research for app store optimization (weekly Monday)",
                "success_criteria": "ASO keyword data updated with search volume and competition scores",
                "depends_on": ["app_clone_scan"],
            },
            {
                "name": "app_ideation",
                "script": "app_ideation_specialist.py",
                "flags": "--scan",
                "timeout_min": 30,
                "description": "Full trend scan: Google Trends + Reddit + TikTok + YouTube + gap analysis",
                "success_criteria": "Ideas scored 16/20+ saved to LEDGER/APP_IDEATION_RESULTS.csv",
                "depends_on": ["aso_keyword_research"],
            },
        ],
    },
    "gov_contracts": {
        "description": "Government contract intelligence — scrape tenders, SAM.gov, USAspending, package bids",
        "schedule": "04:30",
        "category": "research",
        "priority": 4,
        "risk_level": "LOW",
        "steps": [
            {
                "name": "gov_tenders",
                "script": "gov_tenders_scraper.py",
                "flags": "--scan",
                "timeout_min": 20,
                "description": "Scrape government tender listings for IT/software/consulting opportunities",
                "success_criteria": "New tenders extracted and saved to gov contracts CSV",
            },
            {
                "name": "sam_gov",
                "script": "sam_gov_scraper.py",
                "flags": "--scan",
                "timeout_min": 20,
                "description": "Scrape SAM.gov for active federal contract opportunities",
                "success_criteria": "SAM.gov opportunities extracted with NAICS codes and deadlines",
                "depends_on": ["gov_tenders"],
            },
            {
                "name": "usaspending",
                "script": "usaspending_scraper.py",
                "flags": "--scan",
                "timeout_min": 20,
                "description": "Scrape USAspending.gov for awarded contracts and spending patterns",
                "success_criteria": "Spending data extracted, high-value categories identified",
                "depends_on": ["sam_gov"],
            },
            {
                "name": "sam_gov_monitor",
                "script": "sam_gov_monitor.py",
                "flags": "",
                "timeout_min": 20,
                "description": "Monitor SAM.gov for federal contract updates (every 6 hours)",
                "success_criteria": "SAM.gov contract updates detected and logged",
                "depends_on": ["sam_gov"],
            },
            {
                "name": "uk_contracts",
                "script": "uk_contracts_finder.py",
                "flags": "",
                "timeout_min": 20,
                "description": "Scan UK Contracts Finder for international gov contract opportunities (weekly)",
                "success_criteria": "UK contract opportunities extracted and saved",
                "depends_on": ["usaspending"],
            },
            {
                "name": "bid_package",
                "script": "gov_bid_packager.py",
                "flags": "--generate",
                "timeout_min": 25,
                "description": "Auto-generate bid response packages from scraped tender data",
                "success_criteria": "Bid packages drafted for top matching opportunities",
                "depends_on": ["sam_gov_monitor", "uk_contracts"],
            },
        ],
    },
    "sourcing_intel": {
        "description": "Product sourcing intelligence — ImportYeti customs data + StoreLeads ecom data",
        "schedule": "04:15",
        "category": "research",
        "priority": 4,
        "risk_level": "LOW",
        "steps": [
            {
                "name": "import_sourcing",
                "script": "import_sourcing_scanner.py",
                "flags": "--daily",
                "timeout_min": 30,
                "description": "Scan ImportYeti for US customs data, factory intel, supplier contacts",
                "success_criteria": "IMPORT_SOURCING_INTEL.csv and CONTACT_READY_FACTORIES.csv updated",
            },
            {
                "name": "storeleads_scan",
                "script": "storeleads_ecom_scraper.py",
                "flags": "--scan",
                "timeout_min": 20,
                "description": "Scrape StoreLeads for ecom store intelligence and tech stack data",
                "success_criteria": "Ecom store data extracted with tech stack and traffic estimates",
                "depends_on": ["import_sourcing"],
            },
        ],
    },
    "social_intelligence": {
        "description": "Social signal mining — Telegram, Reddit pain points, FB Ads Library, Product Hunt",
        "schedule": "09:00",
        "category": "research",
        "priority": 2,
        "risk_level": "LOW",
        "steps": [
            {
                "name": "telegram_signals",
                "script": "telegram_community_monitor.py",
                "flags": "--scan",
                "timeout_min": 15,
                "description": "Monitor 26 public Telegram channels across 8 niches for signals",
                "success_criteria": "TELEGRAM_SIGNALS.csv updated, high-score entries added to ALPHA_STAGING",
            },
            {
                "name": "reddit_pain_points",
                "script": "reddit_pain_point_miner.py",
                "flags": "--scan",
                "timeout_min": 20,
                "description": "Extract buying intent from 25 subreddits for product opportunities",
                "success_criteria": "Pain points CSV updated with new buying-intent signals",
            },
            {
                "name": "fb_ads_scan",
                "script": "fb_ads_library_scanner.py",
                "flags": "--scan",
                "timeout_min": 20,
                "description": "Scan Facebook Ads Library for high-spend ads revealing validated products",
                "success_criteria": "High-spend ad creatives extracted with product categories and spend",
                "depends_on": ["telegram_signals"],
            },
            {
                "name": "producthunt_scan",
                "script": "producthunt_scraper.py",
                "flags": "--scan",
                "timeout_min": 15,
                "description": "Scrape Product Hunt for trending launches and upvote patterns",
                "success_criteria": "PH launches extracted with vote counts and maker data",
                "depends_on": ["reddit_pain_points"],
            },
        ],
    },
    "platform_monitoring": {
        "description": "Platform monitoring — competitor pricing, meta changes, compliance deadlines",
        "schedule": "07:30",
        "category": "analysis",
        "priority": 3,
        "risk_level": "LOW",
        "steps": [
            {
                "name": "price_monitor",
                "script": "competitor_price_monitor.py",
                "flags": "--scan",
                "timeout_min": 15,
                "description": "Monitor competitor pricing across tracked products and services",
                "success_criteria": "Price change alerts generated for significant movements",
            },
            {
                "name": "platform_meta",
                "script": "platform_meta_monitor.py",
                "flags": "--scan",
                "timeout_min": 15,
                "description": "Monitor TikTok/X/IG algorithm changes and platform policy updates",
                "success_criteria": "Platform change digest generated with impact assessment",
                "depends_on": ["price_monitor"],
            },
            {
                "name": "platform_algo_detection",
                "script": "platform_algo_detection.py",
                "flags": "",
                "timeout_min": 15,
                "description": "Detect platform algorithm changes across TikTok, X, Instagram, YouTube",
                "success_criteria": "Algorithm change signals detected and logged",
                "depends_on": ["platform_meta"],
            },
            {
                "name": "hashtag_audio_tracking",
                "script": "hashtag_audio_tracking.py",
                "flags": "",
                "timeout_min": 15,
                "description": "Track trending hashtags and audio across social platforms",
                "success_criteria": "Trending hashtags and audio data updated",
                "depends_on": ["platform_algo_detection"],
            },
            {
                "name": "platform_rpm_tracking",
                "script": "platform_rpm_tracking.py",
                "flags": "",
                "timeout_min": 15,
                "description": "Track RPM rates across creator platforms (weekly Monday)",
                "success_criteria": "Platform RPM data updated with latest rates",
                "depends_on": ["hashtag_audio_tracking"],
            },
            {
                "name": "creator_program_monitoring",
                "script": "creator_program_monitoring.py",
                "flags": "",
                "timeout_min": 15,
                "description": "Monitor creator program changes across platforms (weekly Monday)",
                "success_criteria": "Creator program updates detected and logged",
                "depends_on": ["platform_rpm_tracking"],
            },
            {
                "name": "compliance_check",
                "script": "compliance_deadline_tracker.py",
                "flags": "--check",
                "timeout_min": 10,
                "description": "Check 21 regulatory deadlines, scan RSS for new regulation changes",
                "success_criteria": "Compliance digest generated, urgent deadlines within 30 days flagged",
                "depends_on": ["creator_program_monitoring"],
            },
        ],
    },
    "analytics_dashboard": {
        "description": "Analytics and dashboard refresh — aggregate signals, optimize, update brain",
        "schedule": "13:00",
        "category": "analysis",
        "priority": 3,
        "risk_level": "LOW",
        "steps": [
            {
                "name": "signal_aggregate",
                "script": "signal_aggregator.py",
                "flags": "--aggregate",
                "timeout_min": 15,
                "description": "Aggregate signals from all scrapers into unified signal score",
                "success_criteria": "Aggregated signal report generated with cross-source correlations",
            },
            {
                "name": "dashboard_refresh",
                "script": "refresh_dashboard.py",
                "flags": "",
                "timeout_min": 10,
                "description": "Refresh Bloomberg-style pipeline dashboard with latest data",
                "success_criteria": "Dashboard HTML regenerated with current pipeline metrics",
                "depends_on": ["signal_aggregate"],
            },
            {
                "name": "performance_opt",
                "script": "performance_optimizer.py",
                "flags": "--analyze",
                "timeout_min": 20,
                "description": "Analyze pipeline performance and recommend optimizations",
                "success_criteria": "Performance report with specific optimization recommendations",
                "depends_on": ["dashboard_refresh"],
            },
            {
                "name": "brain_update",
                "script": "printmaxx_brain.py",
                "flags": "--update",
                "timeout_min": 15,
                "description": "Update PRINTMAXX brain with latest signal, performance, and strategy data",
                "success_criteria": "Brain state updated, decision recommendations refreshed",
                "depends_on": ["performance_opt"],
            },
        ],
    },
    "system_maintenance": {
        "description": "System maintenance — backup, loop fixes, health monitoring, guardrails",
        "schedule": "21:00",
        "category": "maintenance",
        "priority": 5,
        "risk_level": "LOW",
        "steps": [
            {
                "name": "backup",
                "script": "backup_system.py",
                "flags": "--incremental",
                "timeout_min": 15,
                "description": "Incremental backup of all project files to ~/PRINTMAXX_BACKUPS/",
                "success_criteria": "Backup completed with file count and size logged",
            },
            {
                "name": "loop_fix",
                "script": "ralph_loop_fixer.py",
                "flags": "--scan",
                "timeout_min": 10,
                "description": "Scan ralph loops for health issues: stale locks, broken state files",
                "success_criteria": "Loop health report generated, stuck loops identified",
                "depends_on": ["backup"],
            },
            {
                "name": "system_health",
                "script": "system_health_monitor.py",
                "flags": "--check",
                "timeout_min": 15,
                "description": "14-point system health check: cron, pipeline, sites, memory, leads",
                "success_criteria": "Health report with GREEN/AMBER/RED for all 14 check points",
                "depends_on": ["loop_fix"],
            },
            {
                "name": "guardrails_test",
                "script": "guardrails.py",
                "flags": "--test",
                "timeout_min": 5,
                "description": "Run guardrails safety test to verify path restrictions are enforced",
                "success_criteria": "ALL TESTS PASSED confirmation from guardrails safety check",
                "depends_on": ["system_health"],
            },
        ],
    },
    "master_ops_sync": {
        "description": "Master ops synchronization — execute, enhance, run daily agent, generate TODOs",
        "schedule": "05:30",
        "category": "maintenance",
        "priority": 2,
        "risk_level": "LOW",
        "steps": [
            {
                "name": "ops_execute",
                "script": "master_ops_executor.py",
                "flags": "--run",
                "timeout_min": 30,
                "description": "Execute pending ops from master ops spreadsheet task queue",
                "success_criteria": "Pending ops executed, status updated in tracker",
            },
            {
                "name": "ops_enhance",
                "script": "master_ops_enhancer.py",
                "flags": "--enhance",
                "timeout_min": 20,
                "description": "Enhance master ops spreadsheet with new scripts, alpha, and status updates",
                "success_criteria": "Master ops XLSX updated with latest automation coverage",
                "depends_on": ["ops_execute"],
            },
            {
                "name": "daily_agent",
                "script": "daily_agent_runner.py",
                "flags": "--status",
                "timeout_min": 10,
                "description": "Auto-orient agent: check priorities, blockers, venture performance",
                "success_criteria": "Daily status report generated with top priorities ranked",
                "depends_on": ["ops_enhance"],
            },
            {
                "name": "daily_todo",
                "script": "daily_todo_generator.py",
                "flags": "",
                "timeout_min": 10,
                "description": "Generate prioritized daily TODO from overnight results and pending tasks",
                "success_criteria": "DAILY_TODO_{date}.md generated with prioritized action items",
                "depends_on": ["daily_agent"],
            },
        ],
    },
    "memory_refresh": {
        "description": "Memory layer refresh — update heartbeat, active tasks, and daily logs",
        "schedule": "05:00",
        "category": "maintenance",
        "priority": 1,
        "risk_level": "LOW",
        "steps": [
            {
                "name": "memory_full",
                "script": "memory_manager.py",
                "flags": "--full",
                "timeout_min": 10,
                "description": "Refresh all 3 memory layers: HEARTBEAT.md, active-tasks.md, daily log",
                "success_criteria": "HEARTBEAT.md and active-tasks.md updated with current system state",
            },
        ],
    },
}

# ============================================================
# Standalone scripts that should run on their own schedules
# (not part of a pipeline, but still autonomous)
# ============================================================

STANDALONE_TASKS = [
    {
        "script": "freshness_auditor.py",
        "flags": "--scan",
        "schedule": "weekly_sunday_04:00",
        "category": "maintenance",
        "priority": 5,
        "description": "Audit alpha entries >30 days old for staleness",
        "success_criteria": "Stale entries marked NEEDS_REVALIDATION",
        "timeout_min": 15,
    },
    {
        "script": "alpha_review_bot.py",
        "flags": "",
        "schedule": "06:00",
        "category": "research",
        "priority": 2,
        "description": "Auto-process PENDING_REVIEW alpha backlog",
        "success_criteria": "PENDING_REVIEW count reduced, entries classified",
        "timeout_min": 20,
    },
    {
        "script": "niche_meta_detector.py",
        "flags": "--live",
        "schedule": "07:30",
        "category": "research",
        "priority": 3,
        "description": "Detect emerging niches via signal pattern matching",
        "success_criteria": "Emerging niche signals identified and logged",
        "timeout_min": 15,
    },
    {
        "script": "backup_system.py",
        "flags": "--incremental",
        "schedule": "21:15",
        "category": "maintenance",
        "priority": 5,
        "description": "Incremental backup of all project files",
        "success_criteria": "Backup completed with file count logged",
        "timeout_min": 10,
    },
    {
        "script": "daily_nocost_rbi_scanner.py",
        "flags": "--scan",
        "schedule": "08:00",
        "category": "research",
        "priority": 3,
        "description": "Daily no-cost RBI scan across 17 zero-cost revenue categories",
        "success_criteria": "RBI scan complete, new zero-cost opportunities identified and logged",
        "timeout_min": 20,
    },
    {
        "script": "ops_orchestrator.py",
        "flags": "--run",
        "schedule": "every_4h_offset_30",
        "category": "maintenance",
        "priority": 3,
        "description": "Ops orchestrator execution cycle for pending operations",
        "success_criteria": "Pending ops executed, orchestrator cycle complete",
        "timeout_min": 30,
    },
    {
        "script": "live_dashboard_server.py",
        "flags": "--refresh",
        "schedule": "09:30",
        "category": "maintenance",
        "priority": 4,
        "description": "Refresh live monitoring dashboard data for real-time panels",
        "success_criteria": "Dashboard data refreshed with latest pipeline and alpha metrics",
        "timeout_min": 10,
    },
    {
        "script": "indeed_hiring_monitor.py",
        "flags": "",
        "schedule": "05:00",
        "category": "research",
        "priority": 3,
        "description": "Monitor Indeed hiring trends as leading indicator for service demand",
        "success_criteria": "Hiring trend data extracted and demand signals logged",
        "timeout_min": 20,
    },
    {
        "script": "meme_coin_signal_tracker.py",
        "flags": "",
        "schedule": "every_6h",
        "category": "research",
        "priority": 5,
        "description": "Track meme coin signals from Reddit and Twitter (low allocation <5%)",
        "success_criteria": "Meme coin signal scores updated in tracker",
        "timeout_min": 15,
    },
    {
        "script": "nordic_ecom_arb.py",
        "flags": "",
        "schedule": "weekly_thursday_04:00",
        "category": "analysis",
        "priority": 4,
        "description": "Scan Nordic markets for ecom arbitrage opportunities (weekly)",
        "success_criteria": "Nordic ecom arb opportunities identified and logged",
        "timeout_min": 20,
    },
    {
        "script": "theirstack_tech_intel.py",
        "flags": "",
        "schedule": "weekly_friday_05:00",
        "category": "research",
        "priority": 4,
        "description": "Technology stack intelligence for lead qualification (weekly)",
        "success_criteria": "Tech stack intel gathered for top leads",
        "timeout_min": 20,
    },
    {
        "script": "update_system_architecture.py",
        "flags": "",
        "schedule": "05:30",
        "category": "maintenance",
        "priority": 3,
        "description": "Daily system architecture update and documentation refresh",
        "success_criteria": "System architecture docs updated with current state",
        "timeout_min": 15,
    },
]


def script_exists(script_name: str) -> bool:
    """Check if a script exists in AUTOMATIONS/."""
    return (AUTOMATIONS_DIR / script_name).exists()


def generate_task_id(pipeline: str, step: str, date: str = None) -> str:
    """Generate a unique task ID."""
    if date is None:
        date = datetime.now().strftime("%Y%m%d")
    return f"AUTO_{date}_{pipeline}_{step}"


def build_task_from_step(pipeline_name: str, pipeline: dict, step: dict,
                         date_str: str, step_deps: dict) -> dict:
    """Build a task queue entry from a pipeline step definition."""
    task_id = generate_task_id(pipeline_name, step["name"], date_str)
    date_path = datetime.now().strftime("%Y-%m-%d")

    task = {
        "id": task_id,
        "category": pipeline.get("category", "research"),
        "priority": pipeline.get("priority", 5),
        "risk_level": pipeline.get("risk_level", "LOW"),
        "description": step["description"],
        "success_criteria": step["success_criteria"],
        "estimated_minutes": step.get("timeout_min", 30),
        "output_path": f"OPS/autonomous_output/{date_path}/{pipeline_name}/",
        "status": "PENDING",
        "created_at": datetime.now().isoformat(),
        "dependencies": [],
        "pipeline": pipeline_name,
        "step_name": step["name"],
        "source": "workflow_wirer",
    }

    # Resolve dependencies within the pipeline
    if "depends_on" in step:
        for dep_name in step["depends_on"]:
            dep_id = step_deps.get(dep_name)
            if dep_id:
                task["dependencies"].append(dep_id)

    # Add execution details
    if step.get("script"):
        task["execution"] = {
            "type": "script",
            "script": step["script"],
            "flags": step.get("flags", ""),
            "command": f"python3 AUTOMATIONS/{step['script']} {step.get('flags', '')}".strip(),
        }
    elif step.get("llm_prompt"):
        task["execution"] = {
            "type": "llm",
            "prompt": step["llm_prompt"],
        }

    return task


def scan_pipelines(pipeline_filter: str = None) -> list:
    """Scan pipeline definitions and generate task entries."""
    tasks = []
    date_str = datetime.now().strftime("%Y%m%d")

    pipelines = PIPELINES
    if pipeline_filter:
        pipelines = {k: v for k, v in PIPELINES.items() if k == pipeline_filter}

    for pipeline_name, pipeline in pipelines.items():
        step_deps = {}
        for step in pipeline["steps"]:
            task = build_task_from_step(pipeline_name, pipeline, step, date_str, step_deps)

            # Check if script exists (for script-based tasks)
            if step.get("script") and not script_exists(step["script"]):
                task["_warning"] = f"Script not found: {step['script']}"

            step_deps[step["name"]] = task["id"]
            tasks.append(task)

    return tasks


def scan_standalone() -> list:
    """Scan standalone tasks and generate entries."""
    tasks = []
    date_str = datetime.now().strftime("%Y%m%d")

    for defn in STANDALONE_TASKS:
        task_id = generate_task_id("standalone", defn["script"].replace(".py", ""), date_str)
        task = {
            "id": task_id,
            "category": defn.get("category", "maintenance"),
            "priority": defn.get("priority", 5),
            "risk_level": "LOW",
            "description": defn["description"],
            "success_criteria": defn["success_criteria"],
            "estimated_minutes": defn.get("timeout_min", 15),
            "output_path": f"OPS/autonomous_output/{datetime.now().strftime('%Y-%m-%d')}/standalone/",
            "status": "PENDING",
            "created_at": datetime.now().isoformat(),
            "dependencies": [],
            "pipeline": "standalone",
            "step_name": defn["script"],
            "source": "workflow_wirer",
        }

        if script_exists(defn["script"]):
            task["execution"] = {
                "type": "script",
                "script": defn["script"],
                "flags": defn.get("flags", ""),
                "command": f"python3 AUTOMATIONS/{defn['script']} {defn.get('flags', '')}".strip(),
            }
        else:
            task["_warning"] = f"Script not found: {defn['script']}"

        tasks.append(task)

    return tasks


def scan_crontab_for_unwired() -> list:
    """Scan crontab files for scripts not yet covered by pipelines."""
    wired_scripts = set()

    # Collect all scripts already wired in pipelines
    for pipeline in PIPELINES.values():
        for step in pipeline["steps"]:
            if step.get("script"):
                wired_scripts.add(step["script"])
    for defn in STANDALONE_TASKS:
        wired_scripts.add(defn["script"])

    # Parse crontab for Python scripts
    unwired = []
    for crontab_path in [CRONTAB_V2, CRONTAB_V1, CRON_NEW]:
        if not crontab_path.exists():
            continue
        for line in crontab_path.read_text().split("\n"):
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            # Extract python script name from cron entry
            match = re.search(r'AUTOMATIONS/(\w+\.py)', line)
            if match:
                script = match.group(1)
                if script not in wired_scripts:
                    # Extract flags
                    full_match = re.search(r'AUTOMATIONS/\w+\.py\s*(.*?)(?:\s*>>|\s*2>&1|\s*$)', line)
                    flags = full_match.group(1).strip() if full_match else ""
                    unwired.append({
                        "script": script,
                        "flags": flags,
                        "cron_line": line,
                        "source": str(crontab_path.name),
                    })
                    wired_scripts.add(script)  # Don't double-count

    return unwired


def generate_daily_tasks(pipeline_filter: str = None) -> list:
    """Generate the full daily task set."""
    tasks = []
    tasks.extend(scan_pipelines(pipeline_filter))
    if not pipeline_filter:
        tasks.extend(scan_standalone())
    return tasks


def write_to_queue(tasks: list, append: bool = True):
    """Write tasks to the JSONL queue."""
    QUEUE_PATH.parent.mkdir(parents=True, exist_ok=True)

    existing = []
    if append and QUEUE_PATH.exists():
        for line in QUEUE_PATH.read_text().strip().split("\n"):
            line = line.strip()
            if line:
                try:
                    existing.append(json.loads(line))
                except json.JSONDecodeError:
                    pass

    existing_ids = {t["id"] for t in existing}
    added = 0
    for task in tasks:
        if task["id"] not in existing_ids:
            existing.append(task)
            existing_ids.add(task["id"])
            added += 1

    lines = [json.dumps(t) for t in existing]
    QUEUE_PATH.write_text("\n".join(lines) + "\n" if lines else "")
    return added


def save_registry(tasks: list):
    """Save the wiring registry for reference."""
    registry = {
        "generated_at": datetime.now().isoformat(),
        "pipelines": list(PIPELINES.keys()),
        "standalone_count": len(STANDALONE_TASKS),
        "total_tasks": len(tasks),
        "tasks": [
            {
                "id": t["id"],
                "pipeline": t.get("pipeline", "unknown"),
                "step": t.get("step_name", "unknown"),
                "script": t.get("execution", {}).get("script", "LLM task"),
                "priority": t.get("priority", 5),
                "status": t.get("status", "PENDING"),
            }
            for t in tasks
        ],
    }
    WIRING_REGISTRY.parent.mkdir(parents=True, exist_ok=True)
    WIRING_REGISTRY.write_text(json.dumps(registry, indent=2))


def show_scan(tasks: list, unwired: list):
    """Display scan results."""
    print("\n" + "=" * 60)
    print("  PRINTMAXX WORKFLOW WIRER — SCAN RESULTS")
    print("=" * 60)

    # Group by pipeline
    by_pipeline = defaultdict(list)
    for t in tasks:
        by_pipeline[t.get("pipeline", "unknown")].append(t)

    total_minutes = 0
    for pipeline_name, pipeline_tasks in sorted(by_pipeline.items()):
        info = PIPELINES.get(pipeline_name, {})
        schedule = info.get("schedule", "on-demand")
        print(f"\n  [{pipeline_name.upper()}] ({schedule})")
        print(f"    {info.get('description', 'Standalone task')}")
        for t in pipeline_tasks:
            script_info = t.get("execution", {}).get("script", "LLM task")
            warning = t.get("_warning", "")
            status = "  MISSING" if warning else ""
            exists = "  OK" if not warning else ""
            est = t.get("estimated_minutes", 0)
            total_minutes += est
            deps = t.get("dependencies", [])
            dep_str = f"  (after: {', '.join(deps)})" if deps else ""
            print(f"    [{t['priority']}] {t.get('step_name', t['id'])}: "
                  f"{script_info} ~{est}min{exists}{status}{dep_str}")

    print(f"\n  TOTAL WIRED: {len(tasks)} tasks ({total_minutes} min estimated)")

    if unwired:
        print(f"\n  UNWIRED CRON SCRIPTS ({len(unwired)}):")
        for u in unwired[:20]:
            print(f"    {u['script']} {u['flags']}  [{u['source']}]")
        if len(unwired) > 20:
            print(f"    ... and {len(unwired) - 20} more")

    print("\n" + "=" * 60)


def show_status():
    """Show current wiring status."""
    print("\n" + "=" * 60)
    print("  WORKFLOW WIRER STATUS")
    print("=" * 60)

    # Pipeline coverage
    total_scripts = 0
    found_scripts = 0
    for pipeline in PIPELINES.values():
        for step in pipeline["steps"]:
            if step.get("script"):
                total_scripts += 1
                if script_exists(step["script"]):
                    found_scripts += 1

    for defn in STANDALONE_TASKS:
        total_scripts += 1
        if script_exists(defn["script"]):
            found_scripts += 1

    print(f"\n  Pipelines defined:    {len(PIPELINES)}")
    print(f"  Standalone tasks:     {len(STANDALONE_TASKS)}")
    print(f"  Script coverage:      {found_scripts}/{total_scripts} scripts found")

    # Queue status
    if QUEUE_PATH.exists():
        lines = [l for l in QUEUE_PATH.read_text().strip().split("\n") if l.strip()]
        tasks = []
        for l in lines:
            try:
                tasks.append(json.loads(l))
            except json.JSONDecodeError:
                pass
        pending = sum(1 for t in tasks if t.get("status") == "PENDING")
        completed = sum(1 for t in tasks if t.get("status") == "COMPLETED")
        failed = sum(1 for t in tasks if t.get("status") == "FAILED")
        in_progress = sum(1 for t in tasks if t.get("status") == "IN_PROGRESS")
        wirer_tasks = sum(1 for t in tasks if t.get("source") == "workflow_wirer")
        print(f"\n  Task Queue:")
        print(f"    Total:           {len(tasks)}")
        print(f"    Pending:         {pending}")
        print(f"    In Progress:     {in_progress}")
        print(f"    Completed:       {completed}")
        print(f"    Failed:          {failed}")
        print(f"    From wirer:      {wirer_tasks}")
    else:
        print("\n  Task Queue: NOT FOUND")

    # Unwired scripts
    unwired = scan_crontab_for_unwired()
    print(f"\n  Unwired cron scripts: {len(unwired)}")

    # Registry
    if WIRING_REGISTRY.exists():
        try:
            reg = json.loads(WIRING_REGISTRY.read_text())
            print(f"  Last wired:          {reg.get('generated_at', 'unknown')}")
        except json.JSONDecodeError:
            pass

    print("\n" + "=" * 60)


def main():
    parser = argparse.ArgumentParser(
        description="PRINTMAXX Workflow Wirer — auto-generate task queue from existing automations"
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--scan", action="store_true", help="Scan and show what would be wired")
    group.add_argument("--wire", action="store_true", help="Wire everything into the task queue")
    group.add_argument("--daily", action="store_true", help="Generate daily task set")
    group.add_argument("--status", action="store_true", help="Show current wiring status")
    group.add_argument("--dry-run", action="store_true", help="Show tasks without writing to queue")
    parser.add_argument("--pipeline", type=str, help="Filter to specific pipeline")

    args = parser.parse_args()

    if args.status:
        show_status()
        return

    if args.scan or args.dry_run:
        tasks = generate_daily_tasks(args.pipeline)
        unwired = scan_crontab_for_unwired()
        show_scan(tasks, unwired)
        if args.dry_run:
            print("\n  DRY RUN — no tasks written to queue\n")
        return

    if args.wire or args.daily:
        tasks = generate_daily_tasks(args.pipeline)

        # Remove internal warnings before writing
        for t in tasks:
            t.pop("_warning", None)

        added = write_to_queue(tasks)
        save_registry(tasks)

        print(f"\n  WIRED: {added} new tasks added to queue")
        print(f"  Total tasks generated: {len(tasks)}")
        print(f"  Queue: {QUEUE_PATH}")
        print(f"  Registry: {WIRING_REGISTRY}")

        # Show summary
        by_pipeline = defaultdict(int)
        for t in tasks:
            by_pipeline[t.get("pipeline", "unknown")] += 1
        print("\n  By pipeline:")
        for name, count in sorted(by_pipeline.items()):
            print(f"    {name}: {count} tasks")
        print()


if __name__ == "__main__":
    main()
