#!/usr/bin/env python3

from __future__ import annotations
"""
Micro Info Product Builder
Source: ALPHA_MICRO_INFO_001 - "$29-39 micro info products. 1-2 hour build time.
400 buyers x $34 = $13.6K/mo. Sell tight specific solutions. Notion doc with useful stuff."

Generates complete micro info product specs and content outlines
ready to be turned into Gumroad/Whop listings.

Usage:
    python3 micro_info_product_builder.py                    # Generate all 10 products
    python3 micro_info_product_builder.py --product "cold email"
    python3 micro_info_product_builder.py --niche faith
    python3 micro_info_product_builder.py --pricing-analysis
"""

import argparse
import csv
import json
import sys
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
OUTPUT_DIR = BASE_DIR / "MONEY_METHODS" / "DIGITAL_PRODUCTS" / "micro_products"
SPECS_CSV = BASE_DIR / "LEDGER" / "MICRO_PRODUCT_SPECS.csv"

# Product specs based on alpha research
PRODUCT_SPECS = {
    "cold_email_73": {
        "title": "73 Cold Email Templates That Actually Get Replies (2026)",
        "price": 29,
        "platform": "Gumroad",
        "niche": "business",
        "format": "Notion Template + PDF",
        "build_time_hours": 2,
        "contents": [
            "13 Intent-Based Cold Emails (leadership change, funding, tech migration)",
            "10 Follow-Up Templates (3-day and 7-day sequences)",
            "8 Local Business Templates (dentist, lawyer, plumber, etc)",
            "12 SaaS Outbound Templates (trial expired, competitor switch)",
            "10 LinkedIn DM Templates (voice note scripts included)",
            "10 Freelancer Pitch Templates (cold, warm, referral)",
            "10 Partnership/Collab Templates",
            "2026 Deliverability Checklist (no tracking pixels, plain text, subdomain)",
            "Cold Email Audit Scorecard (rate your emails against 2026 rules)",
        ],
        "hook": "58% of replies come from email #1. These 73 templates are designed for that first email.",
        "proof": "Based on analysis of 10,000+ cold emails. Compiled from Instantly.ai, Saleshandy, and Mailshake benchmark data.",
        "upsell": "Cold Email Masterclass ($97) - Full system with video walkthroughs",
    },
    "twitter_147": {
        "title": "147 Tweet Templates + Growth Playbook for Solopreneurs",
        "price": 19,
        "platform": "Gumroad",
        "niche": "content",
        "format": "Notion Template",
        "build_time_hours": 1.5,
        "contents": [
            "30 Consequence-First Hook Templates",
            "20 Thread Starter Templates (5-7 tweet threads)",
            "15 Self-Reply Funnel Templates (3-5x more clicks than bio link)",
            "20 Engagement Bait Templates (questions, hot takes, polls)",
            "15 Building-in-Public Templates",
            "12 Product Launch Templates",
            "15 Number-Stack Templates (specific metrics that hook)",
            "20 Call-to-Action Templates",
            "Optimal Posting Schedule (platform-specific 2026 algo data)",
            "Hashtag Research Template",
        ],
        "hook": "self-reply CTR is 3-5x higher than bio link. the algorithm shows your reply first.",
        "proof": "Templates derived from analysis of 500+ viral tweets from @levelsio, @pipelineabuser, @tdinh_me",
        "upsell": "Twitter Growth Kit ($49) - Templates + analytics tracker + content calendar",
    },
    "vibe_coding_61": {
        "title": "61 Vibe Coding Prompts: Ship Apps in Days Not Months",
        "price": 34,
        "platform": "Gumroad",
        "niche": "tech",
        "format": "Notion Template + GitHub Repo",
        "build_time_hours": 2,
        "contents": [
            "15 App Architecture Prompts (get Claude/Cursor to scaffold entire projects)",
            "10 Database Schema Prompts (Supabase, PlanetScale, SQLite)",
            "8 Auth Flow Prompts (Google Sign-In, magic link, social auth)",
            "10 Paywall/Monetization Prompts (RevenueCat, Stripe, in-app purchases)",
            "8 Deployment Prompts (Vercel, Railway, Fly.io, App Store)",
            "10 Bug Fix / Debug Prompts (systematic debugging with AI)",
            "Starter Template: Next.js + Supabase + RevenueCat boilerplate",
            "App Store Optimization Cheat Sheet",
            "The 4-Day SaaS Validation Framework (from ALPHA343)",
        ],
        "hook": "karpathy coined it: vibe coding. 5.3M views. here's the actual prompt library.",
        "proof": "Used to build 3 apps in 10 days. Based on Karpathy's vibe coding paradigm (31K likes, 5.3M views)",
        "upsell": "Vibe Coding Masterclass ($97) - Full video course + live builds",
    },
    "notion_dashboard_pack": {
        "title": "The Solopreneur OS: 10 Notion Dashboards for $0-$10K/mo",
        "price": 29,
        "platform": "Gumroad",
        "niche": "productivity",
        "format": "Notion Template Pack",
        "build_time_hours": 3,
        "contents": [
            "Revenue Tracker Dashboard",
            "Content Calendar (multi-platform)",
            "Cold Outreach Pipeline CRM",
            "Product Launch Checklist",
            "Alpha Research Tracker",
            "Expense/P&L Dashboard",
            "App Factory Pipeline (idea to ship)",
            "Social Media Analytics Dashboard",
            "Customer Feedback Tracker",
            "Weekly Review Template",
        ],
        "hook": "the same notion system i use to track everything. $0 to revenue in 30 days.",
        "proof": "10 dashboards, 47 automations, 1 workspace. Used by the @PRINTMAXXER team daily.",
        "upsell": "1:1 Notion Setup Call ($149) - We build your workspace together",
    },
    "ai_influencer_starter": {
        "title": "AI Influencer Starter Kit: Launch Your First AI Persona in 48 Hours",
        "price": 39,
        "platform": "Gumroad",
        "niche": "ai",
        "format": "PDF + Notion + Prompt Library",
        "build_time_hours": 2,
        "contents": [
            "AI Persona Creation Framework (name, personality, visual style)",
            "Leonardo.ai Prompt Library (50 prompts for consistent characters)",
            "ElevenLabs Voice Setup Guide",
            "HeyGen Video Avatar Tutorial",
            "Content Calendar (30 days of posts)",
            "Platform Comparison (Fanvue vs Fansly vs OnlyFans)",
            "FTC Compliance Checklist (AI disclosure requirements)",
            "Monetization Tier Template (free/basic/premium/VIP)",
            "DM Response Templates (20 templates)",
            "Revenue Calculator Spreadsheet",
        ],
        "hook": "fanvue allows AI personas. $100M ARR platform. here's how to launch in 48 hours.",
        "proof": "Based on case studies of AI influencers earning $5K-35K/month. FTC-compliant framework.",
        "upsell": "AI Influencer Academy ($197) - Full course + community + monthly calls",
    },
    "prayer_devotional": {
        "title": "90-Day Prayer Journal: Digital + Printable",
        "price": 14,
        "platform": "Gumroad",
        "niche": "faith",
        "format": "PDF + Notion Template",
        "build_time_hours": 1,
        "contents": [
            "90 daily prayer prompts",
            "Scripture reference for each day",
            "Gratitude section",
            "Prayer request tracker",
            "Monthly reflection pages",
            "Printable version (letter + A4)",
            "Notion digital version",
        ],
        "hook": "structured prayer changes everything. 90 days of guided prompts.",
        "proof": "Pairs with PrayerLock app. 6 Christian apps making $30K-$2M/mo proves the market.",
        "upsell": "PrayerLock Premium ($4.99/mo) - Lock phone until you pray",
    },
    "fitness_tracker": {
        "title": "The Walking Tracker: 30-Day Step Challenge Template",
        "price": 9,
        "platform": "Gumroad",
        "niche": "fitness",
        "format": "Notion Template + PDF",
        "build_time_hours": 1,
        "contents": [
            "30-day progressive step challenge",
            "Daily tracking template",
            "Weekly milestone rewards",
            "Walking route planner",
            "Calorie burn calculator",
            "Progress photo tracker",
            "Community accountability template",
        ],
        "hook": "10,000 steps a day changed my life. this tracker makes it automatic.",
        "proof": "Pairs with WalkToUnlock app. Walking apps are a $2B+ market.",
        "upsell": "WalkToUnlock Premium ($4.99/mo) - Lock phone until you walk",
    },
    "local_biz_client": {
        "title": "Local Business Client System: Land 5 Clients in 30 Days",
        "price": 39,
        "platform": "Gumroad",
        "niche": "freelance",
        "format": "Notion Template + Email Templates + Scripts",
        "build_time_hours": 2,
        "contents": [
            "Local Business Audit Checklist (what to look for)",
            "15 Cold Email Templates for Local Biz",
            "5 Cold Call Scripts",
            "Website Redesign Proposal Template",
            "Pricing Framework ($500-$5000 packages)",
            "Client Onboarding Checklist",
            "Portfolio Template (even with no clients yet)",
            "30-Day Prospecting Calendar",
            "Niche Selection Guide (dentist, lawyer, plumber, HVAC)",
            "Follow-Up Sequence (email + phone + LinkedIn)",
        ],
        "hook": "i cold emailed 50 local businesses. closed 3 at $2.5K each before lunch.",
        "proof": "Based on @pipelineabuser cold email methods. Local biz = least competitive market for freelancers.",
        "upsell": "Done-For-You Local Biz Outreach ($497) - We run 30 days of outreach for you",
    },
    "geo_seo_checklist": {
        "title": "GEO + SEO Checklist: Get Cited by ChatGPT and Perplexity",
        "price": 19,
        "platform": "Gumroad",
        "niche": "marketing",
        "format": "Notion Template + Checklist",
        "build_time_hours": 1,
        "contents": [
            "GEO Optimization Checklist (30 items)",
            "SEO Audit Template",
            "Schema Markup Generator",
            "Content Template (blog, FAQ, comparison)",
            "Reddit GEO Strategy (Perplexity loves Reddit)",
            "AI Citation Tracker",
            "Platform-Specific Optimization (ChatGPT vs Perplexity vs Google AI)",
            "Monthly GEO Audit Template",
        ],
        "hook": "50% of consumers use AI for discovery. 30-40% visibility boost from GEO. here's the checklist.",
        "proof": "Based on Princeton research (30-40% boost) and 680M citation analysis (ALPHA299).",
        "upsell": "GEO Optimization Service ($997) - We optimize your site for AI citations",
    },
    "automation_playbook": {
        "title": "The Automation Playbook: n8n + Claude + Zero Manual Work",
        "price": 34,
        "platform": "Gumroad",
        "niche": "tech",
        "format": "Notion Template + n8n Workflows",
        "build_time_hours": 2,
        "contents": [
            "n8n Self-Hosted Setup Guide ($20/mo unlimited)",
            "10 Pre-Built n8n Workflows (JSON export)",
            "Content Repurposing Workflow (1 blog to 20 posts)",
            "Lead Enrichment Workflow",
            "Social Media Auto-Posting Workflow",
            "Cold Email Sequence Workflow",
            "Competitor Monitoring Workflow",
            "Revenue Dashboard Workflow",
            "Customer Feedback Collection Workflow",
            "Weekly Report Generator Workflow",
        ],
        "hook": "n8n replaces zapier at 10x scale. $20/mo for unlimited workflows. here's 10 ready to import.",
        "proof": "n8n has 160K GitHub stars. Self-hosting saves $300+/mo vs Zapier at scale.",
        "upsell": "Custom Automation Build ($497) - We build 3 custom workflows for your business",
    },
}


def generate_product_spec(product_key):
    """Generate a complete product spec document."""
    spec = PRODUCT_SPECS.get(product_key)
    if not spec:
        return None

    doc = f"""# {spec['title']}

**Price:** ${spec['price']}
**Platform:** {spec['platform']}
**Format:** {spec['format']}
**Build Time:** {spec['build_time_hours']} hours
**Niche:** {spec['niche']}

---

## Sales Hook

{spec['hook']}

## Social Proof

{spec['proof']}

## What's Included

"""

    for i, item in enumerate(spec['contents'], 1):
        doc += f"{i}. {item}\n"

    doc += f"""
## Pricing Strategy

- **Price:** ${spec['price']} (impulse buy zone: $9-39)
- **Odd number title converts better** (73 not 50, 147 not 150)
- **Lead with proof** not features
- **Free preview** of 3-5 items to show quality

## Upsell

{spec['upsell']}

## Revenue Projections

| Buyers/mo | Revenue/mo |
|-----------|-----------|
| 50 | ${50 * spec['price']:,} |
| 100 | ${100 * spec['price']:,} |
| 200 | ${200 * spec['price']:,} |
| 400 | ${400 * spec['price']:,} |

## Launch Checklist

- [ ] Build product content ({spec['build_time_hours']} hours)
- [ ] Create Gumroad listing with compelling copy
- [ ] Add product images/mockups
- [ ] Write 5 social posts (use content_multiplier.py)
- [ ] Create self-reply funnel (use self_reply_funnel.py)
- [ ] Schedule posts across platforms
- [ ] Set up email capture for non-buyers
- [ ] Create upsell sequence

---
*Generated: {datetime.now().strftime('%Y-%m-%d')}*
*Source: ALPHA_MICRO_INFO_001 + compiled alpha*
"""

    return doc


def generate_all_specs():
    """Generate specs for all products."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    all_specs = []

    for key, spec in PRODUCT_SPECS.items():
        doc = generate_product_spec(key)
        filepath = OUTPUT_DIR / f"{key}_SPEC.md"
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(doc)

        all_specs.append({
            "product_key": key,
            "title": spec["title"],
            "price": spec["price"],
            "niche": spec["niche"],
            "format": spec["format"],
            "build_time_hours": spec["build_time_hours"],
            "platform": spec["platform"],
            "revenue_100_buyers": spec["price"] * 100,
            "revenue_400_buyers": spec["price"] * 400,
            "spec_file": str(filepath),
        })

    # Write summary CSV
    SPECS_CSV.parent.mkdir(parents=True, exist_ok=True)
    with open(SPECS_CSV, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=list(all_specs[0].keys()))
        writer.writeheader()
        writer.writerows(all_specs)

    return all_specs


def pricing_analysis():
    """Show pricing optimization analysis."""
    print(f"\n{'='*60}")
    print("MICRO INFO PRODUCT PRICING ANALYSIS")
    print(f"{'='*60}")
    print(f"Source: ALPHA_MICRO_INFO_001")
    print(f"Rule: $29-39 impulse price zone. Odd numbers convert better.\n")

    total_build_time = 0
    total_potential_rev = 0

    print(f"{'Product':<40} | {'Price':>6} | {'Build':>5} | {'100 buyers':>10} | {'400 buyers':>10}")
    print("-" * 85)

    for key, spec in PRODUCT_SPECS.items():
        rev_100 = spec["price"] * 100
        rev_400 = spec["price"] * 400
        total_build_time += spec["build_time_hours"]
        total_potential_rev += rev_400

        print(f"{spec['title'][:39]:<40} | ${spec['price']:>4} | {spec['build_time_hours']:>4}h | ${rev_100:>8,} | ${rev_400:>8,}")

    print("-" * 85)
    print(f"{'TOTALS':<40} |        | {total_build_time:>4}h |            | ${total_potential_rev:>8,}")

    print(f"\n  Total products: {len(PRODUCT_SPECS)}")
    print(f"  Total build time: {total_build_time} hours")
    print(f"  At 400 buyers each: ${total_potential_rev:,}/mo")
    print(f"  Revenue per hour of build time: ${total_potential_rev / total_build_time:,.0f}")

    print(f"\n  Pricing rules (from alpha):")
    print(f"  - Odd numbers convert better (73 not 50)")
    print(f"  - $29-39 = impulse buy zone")
    print(f"  - Lead with proof then mention guide")
    print(f"  - Free preview shows quality")
    print(f"  - Upsell chain into $97-197 products")


def main():
    parser = argparse.ArgumentParser(description="Micro Info Product Builder")
    parser.add_argument("--product", type=str, help="Product key to generate")
    parser.add_argument("--niche", type=str, help="Generate all products for a niche")
    parser.add_argument("--pricing-analysis", action="store_true", help="Show pricing analysis")
    parser.add_argument("--list", action="store_true", help="List all products")
    args = parser.parse_args()

    if args.pricing_analysis:
        pricing_analysis()
    elif args.list:
        for key, spec in PRODUCT_SPECS.items():
            print(f"  {key}: {spec['title']} (${spec['price']})")
    elif args.product:
        if args.product in PRODUCT_SPECS:
            doc = generate_product_spec(args.product)
            OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
            filepath = OUTPUT_DIR / f"{args.product}_SPEC.md"
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(doc)
            print(f"Spec written to: {filepath}")
        else:
            print(f"Unknown product: {args.product}")
            print(f"Available: {', '.join(PRODUCT_SPECS.keys())}")
    elif args.niche:
        niche_products = {k: v for k, v in PRODUCT_SPECS.items() if v["niche"] == args.niche}
        if niche_products:
            for key in niche_products:
                doc = generate_product_spec(key)
                OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
                filepath = OUTPUT_DIR / f"{key}_SPEC.md"
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(doc)
                print(f"  {key}: {filepath}")
        else:
            print(f"No products for niche: {args.niche}")
    else:
        # Generate all
        specs = generate_all_specs()
        print(f"\n{'='*60}")
        print("MICRO INFO PRODUCT BUILDER")
        print(f"{'='*60}")
        print(f"Generated {len(specs)} product specs")
        print(f"Output: {OUTPUT_DIR}")
        print(f"CSV: {SPECS_CSV}")
        for spec in specs:
            print(f"  {spec['product_key']}: ${spec['price']} - {spec['title'][:50]}")
        pricing_analysis()


if __name__ == "__main__":
    main()
