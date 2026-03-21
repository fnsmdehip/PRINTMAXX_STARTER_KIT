#!/usr/bin/env python3

from __future__ import annotations
"""
PRINTMAXX Daily No-Cost RBI Scanner
====================================
Scans ALL zero-cost revenue opportunities across 17 categories.
Reads actual project state from disk. Not a template generator -- a real audit tool.

Usage:
    python3 daily_nocost_rbi_scanner.py --scan            # Full daily scan
    python3 daily_nocost_rbi_scanner.py --category affiliate  # Scan one category
    python3 daily_nocost_rbi_scanner.py --audit            # Audit existing ops status
    python3 daily_nocost_rbi_scanner.py --opportunities    # List all actionable ops
    python3 daily_nocost_rbi_scanner.py --revenue-map      # Show revenue projections
    python3 daily_nocost_rbi_scanner.py --next-actions     # Top 10 things to do RIGHT NOW
    python3 daily_nocost_rbi_scanner.py --integrate        # Output JSON for quant terminal
    python3 daily_nocost_rbi_scanner.py --blockers         # Show blocking items only
    python3 daily_nocost_rbi_scanner.py --critical-path    # Critical path to first $1K/mo

No external dependencies. stdlib only.
"""

import argparse
import csv
import json
import os
import sys
from datetime import datetime, date
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from collections import defaultdict
import textwrap

# ---------------------------------------------------------------------------
# CONSTANTS
# ---------------------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent
LEDGER = PROJECT_ROOT / "LEDGER"
PRODUCTS = PROJECT_ROOT / "PRODUCTS"
MONEY_METHODS = PROJECT_ROOT / "MONEY_METHODS"
AUTOMATIONS = PROJECT_ROOT / "AUTOMATIONS"
CONTENT = PROJECT_ROOT / "CONTENT"
FINANCIALS = PROJECT_ROOT / "FINANCIALS"
OPS = PROJECT_ROOT / "OPS"
APP_FACTORY = MONEY_METHODS / "APP_FACTORY"
RBI_AUDITS = LEDGER / "RBI_AUDITS"

TODAY = date.today().isoformat()

# Priority definitions
P0 = "P0"   # Do today. $0 cost. Assets already exist.
P1 = "P1"   # Do this week. $0 cost. Minimal work needed.
P2 = "P2"   # Do within 2 weeks. May need 1-2 hours setup.
P3 = "P3"   # Backlog. Good idea, lower urgency.

# Status definitions
NOT_STARTED = "NOT_STARTED"
READY_TO_LAUNCH = "READY_TO_LAUNCH"
IN_PROGRESS = "IN_PROGRESS"
ACTIVE = "ACTIVE"
BLOCKED = "BLOCKED"

# Category slugs for --category filtering
CATEGORIES = [
    "marketplace", "affiliate", "freelance", "clipping", "dropship",
    "domain", "ai_music", "directory", "free_tool_arb", "plr_mrr",
    "template", "community", "cold_email", "content_syndication",
    "referral", "repo", "data_leads",
]


# ---------------------------------------------------------------------------
# FILESYSTEM HELPERS
# ---------------------------------------------------------------------------

def file_exists(path: Path) -> bool:
    """Check if a file exists on disk."""
    return path.is_file()


def dir_exists(path: Path) -> bool:
    """Check if a directory exists on disk."""
    return path.is_dir()


def count_files(directory: Path, pattern: str = "*") -> int:
    """Count files matching a pattern in a directory."""
    if not dir_exists(directory):
        return 0
    return sum(1 for _ in directory.glob(pattern))


def read_csv_rows(filepath: Path) -> List[Dict]:
    """Read a CSV file and return list of dicts. Returns [] if file missing."""
    if not file_exists(filepath):
        return []
    try:
        with open(filepath, "r", encoding="utf-8", errors="replace") as f:
            reader = csv.DictReader(f)
            return list(reader)
    except Exception:
        return []


def read_csv_headers(filepath: Path) -> List[str]:
    """Read just the headers of a CSV. Returns [] if file missing."""
    if not file_exists(filepath):
        return []
    try:
        with open(filepath, "r", encoding="utf-8", errors="replace") as f:
            reader = csv.reader(f)
            return next(reader, [])
    except Exception:
        return []


def file_line_count(filepath: Path) -> int:
    """Count lines in a file. Returns 0 if missing."""
    if not file_exists(filepath):
        return 0
    try:
        with open(filepath, "r", encoding="utf-8", errors="replace") as f:
            return sum(1 for _ in f)
    except Exception:
        return 0


def search_file_for(filepath: Path, keyword: str) -> bool:
    """Check if a file contains a keyword (case-insensitive)."""
    if not file_exists(filepath):
        return False
    try:
        with open(filepath, "r", encoding="utf-8", errors="replace") as f:
            content = f.read().lower()
            return keyword.lower() in content
    except Exception:
        return False


# ---------------------------------------------------------------------------
# OPPORTUNITY DATA MODEL
# ---------------------------------------------------------------------------

class Opportunity:
    """Single zero-cost revenue opportunity."""

    def __init__(
        self,
        category: str,
        name: str,
        description: str,
        est_revenue_low: int,
        est_revenue_high: int,
        startup_cost: int,
        time_to_first_dollar: str,
        existing_assets: List[str],
        next_action: str,
        priority: str,
        status: str,
        blockers: List[str] = None,
        notes: str = "",
    ):
        self.category = category
        self.name = name
        self.description = description
        self.est_revenue_low = est_revenue_low
        self.est_revenue_high = est_revenue_high
        self.startup_cost = startup_cost
        self.time_to_first_dollar = time_to_first_dollar
        self.existing_assets = existing_assets or []
        self.next_action = next_action
        self.priority = priority
        self.status = status
        self.blockers = blockers or []
        self.notes = notes

    @property
    def est_revenue_range(self) -> str:
        return f"${self.est_revenue_low}-${self.est_revenue_high}/mo"

    @property
    def is_blocked(self) -> bool:
        return len(self.blockers) > 0

    @property
    def sort_key(self) -> Tuple:
        """Sort by priority then estimated revenue high (descending)."""
        prio_map = {P0: 0, P1: 1, P2: 2, P3: 3}
        return (prio_map.get(self.priority, 9), -self.est_revenue_high)

    def to_dict(self) -> Dict:
        return {
            "category": self.category,
            "name": self.name,
            "description": self.description,
            "est_revenue_low": self.est_revenue_low,
            "est_revenue_high": self.est_revenue_high,
            "est_revenue_range": self.est_revenue_range,
            "startup_cost": self.startup_cost,
            "time_to_first_dollar": self.time_to_first_dollar,
            "existing_assets": self.existing_assets,
            "next_action": self.next_action,
            "priority": self.priority,
            "status": self.status,
            "blockers": self.blockers,
            "notes": self.notes,
        }

    def to_csv_row(self) -> Dict:
        return {
            "category": self.category,
            "name": self.name,
            "description": self.description,
            "est_revenue_low": self.est_revenue_low,
            "est_revenue_high": self.est_revenue_high,
            "est_revenue_range": self.est_revenue_range,
            "startup_cost": self.startup_cost,
            "time_to_first_dollar": self.time_to_first_dollar,
            "existing_assets": "; ".join(self.existing_assets),
            "next_action": self.next_action,
            "priority": self.priority,
            "status": self.status,
            "blockers": "; ".join(self.blockers),
            "notes": self.notes,
            "scan_date": TODAY,
        }


# ---------------------------------------------------------------------------
# CATEGORY SCANNERS
# ---------------------------------------------------------------------------

def scan_marketplace_listings() -> List[Opportunity]:
    """Category 1: Gumroad, Whop, Lemon Squeezy, Etsy digital."""
    ops = []

    # --- Gumroad products ---
    gumroad_file = PRODUCTS / "GUMROAD_READY_LISTINGS.md"
    gumroad_exists = file_exists(gumroad_file)
    gumroad_lines = file_line_count(gumroad_file) if gumroad_exists else 0

    # Count listing sections in the gumroad file
    gumroad_count = 0
    if gumroad_exists:
        try:
            with open(gumroad_file, "r", encoding="utf-8", errors="replace") as f:
                for line in f:
                    if line.strip().startswith("## LISTING"):
                        gumroad_count += 1
        except Exception:
            pass

    products_csv = read_csv_rows(LEDGER / "PRODUCTS.csv")
    gumroad_listed = sum(1 for r in products_csv if r.get("GumroadURL", "").strip())
    gumroad_revenue = sum(float(r.get("Revenue", 0) or 0) for r in products_csv)

    assets = []
    if gumroad_exists:
        assets.append(f"PRODUCTS/GUMROAD_READY_LISTINGS.md ({gumroad_count} listings, {gumroad_lines} lines)")
    if products_csv:
        assets.append(f"LEDGER/PRODUCTS.csv ({len(products_csv)} products tracked)")

    # Descriptions directory
    desc_file = PRODUCTS / "descriptions" / "PRODUCT_DESCRIPTIONS_20.md"
    if file_exists(desc_file):
        assets.append("PRODUCTS/descriptions/PRODUCT_DESCRIPTIONS_20.md")

    status = NOT_STARTED
    blockers = []
    if gumroad_count > 0 and gumroad_listed == 0:
        status = READY_TO_LAUNCH
        blockers.append("Need Gumroad account + Stripe connected")
    elif gumroad_listed > 0 and gumroad_revenue == 0:
        status = IN_PROGRESS
    elif gumroad_revenue > 0:
        status = ACTIVE

    ops.append(Opportunity(
        category="marketplace",
        name="Gumroad Digital Products",
        description=f"{gumroad_count} products written and ready to list. "
                    f"{gumroad_listed} currently live on Gumroad. "
                    f"Products range $7-$97. Total GMV potential with zero marketing: "
                    f"$200-2,000/mo from organic Gumroad discovery + SEO.",
        est_revenue_low=200,
        est_revenue_high=2000,
        startup_cost=0,
        time_to_first_dollar="1-7 days" if gumroad_count > 0 else "3-7 days",
        existing_assets=assets,
        next_action="Copy listings from GUMROAD_READY_LISTINGS.md into Gumroad. Connect Stripe. Publish all 10."
                    if gumroad_count > 0 and gumroad_listed == 0
                    else "Drive traffic to existing listings" if gumroad_listed > 0
                    else "Write product listings first",
        priority=P0 if gumroad_count > 0 and gumroad_listed == 0 else P1,
        status=status,
        blockers=blockers,
        notes=f"Gumroad takes 10% fee. Stripe ~2.9%+30c. Net margin ~87%. "
              f"Gumroad Discover algorithm can send organic traffic to well-optimized listings.",
    ))

    # --- Whop listings ---
    whop_count = count_files(PRODUCTS / "listings", "WHOP_LISTING_*.md")
    whop_assets = []
    if whop_count > 0:
        whop_assets.append(f"PRODUCTS/listings/ ({whop_count} Whop listings ready)")

    ops.append(Opportunity(
        category="marketplace",
        name="Whop Digital Products",
        description=f"{whop_count} Whop listings written. Whop has built-in discovery, "
                    f"affiliate marketplace, and community features. Products can be access passes, "
                    f"digital downloads, or community memberships.",
        est_revenue_low=100,
        est_revenue_high=1500,
        startup_cost=0,
        time_to_first_dollar="1-7 days" if whop_count > 0 else "5-14 days",
        existing_assets=whop_assets,
        next_action="Create Whop account, paste listings, set up payment. Whop has Discover tab = free organic traffic."
                    if whop_count > 0
                    else "Write Whop listings based on Gumroad products",
        priority=P0 if whop_count > 0 else P2,
        status=READY_TO_LAUNCH if whop_count > 0 else NOT_STARTED,
        blockers=["Need Whop seller account"] if whop_count > 0 else ["Need Whop account", "Need listings"],
        notes="Whop Discover is underrated. Lower competition than Gumroad. "
              "Community memberships have higher LTV than one-time downloads. "
              f"$7 funnel teardown guide is ideal loss-leader for Whop.",
    ))

    # --- Etsy Digital ---
    ops.append(Opportunity(
        category="marketplace",
        name="Etsy Digital Downloads",
        description="List Notion templates, printable planners, and digital guides on Etsy. "
                    "Etsy's search algorithm favors new listings heavily in first 30 days. "
                    "Canva templates convert at 2-5% on Etsy.",
        est_revenue_low=50,
        est_revenue_high=800,
        startup_cost=0,
        time_to_first_dollar="3-14 days",
        existing_assets=["Can repurpose Gumroad products as Etsy listings"],
        next_action="Create Etsy shop. Reformat 3-5 products for Etsy (mockup images, Etsy SEO tags). List.",
        priority=P1,
        status=NOT_STARTED,
        blockers=["Need Etsy seller account"],
        notes="Etsy charges $0.20 listing fee + 6.5% transaction fee + 3% payment processing. "
              "Higher fees than Gumroad but massive organic discovery. "
              "Notion templates and digital planners are the sweet spot.",
    ))

    # --- Lemon Squeezy ---
    ops.append(Opportunity(
        category="marketplace",
        name="Lemon Squeezy Store",
        description="Lemon Squeezy handles global tax compliance (VAT/GST) automatically. "
                    "Lower fees than Gumroad (5%+50c vs 10%). Built-in affiliate program. "
                    "Good for non-US buyers.",
        est_revenue_low=50,
        est_revenue_high=500,
        startup_cost=0,
        time_to_first_dollar="3-14 days",
        existing_assets=["Same products as Gumroad, just different storefront"],
        next_action="Create Lemon Squeezy account. Mirror top 3 Gumroad products. Enable affiliate program.",
        priority=P2,
        status=NOT_STARTED,
        blockers=["Need Lemon Squeezy account"],
        notes="Lower priority than Gumroad/Whop due to less organic discovery. "
              "But 5% vs 10% fee makes it better for products you drive traffic to yourself.",
    ))

    return ops


def scan_affiliate_networks() -> List[Opportunity]:
    """Category 2: Affiliate networks and high-commission programs."""
    ops = []

    # Check existing affiliate data
    alpha_rows = read_csv_rows(LEDGER / "ALPHA_STAGING.csv")
    affiliate_alpha = [r for r in alpha_rows if "affiliate" in (r.get("category", "") + r.get("notes", "")).lower()]

    marketing_channels = read_csv_rows(LEDGER / "MARKETING_CHANNELS_MASTER.csv")
    affiliate_channels = [r for r in marketing_channels if "affiliate" in r.get("category", "").lower()]

    # Check for existing content that can embed affiliate links
    content_social_count = 0
    for niche_dir in ["ai", "faith", "fitness", "launch_posts"]:
        niche_path = CONTENT / "social" / niche_dir
        if dir_exists(niche_path):
            content_social_count += count_files(niche_path, "*.md") + count_files(niche_path, "*.txt")

    medium_exists = dir_exists(CONTENT / "medium_articles")
    substack_exists = dir_exists(CONTENT / "substack_posts")

    assets = []
    if content_social_count > 0:
        assets.append(f"CONTENT/social/ ({content_social_count} posts that can embed affiliate links)")
    if medium_exists:
        assets.append("CONTENT/medium_articles/ (articles ready for affiliate integration)")
    if substack_exists:
        assets.append("CONTENT/substack_posts/ (newsletter content for affiliate CTAs)")
    if affiliate_alpha:
        assets.append(f"LEDGER/ALPHA_STAGING.csv ({len(affiliate_alpha)} affiliate alpha entries)")

    # SaaS affiliate programs -- high commission, recurring
    ops.append(Opportunity(
        category="affiliate",
        name="SaaS Affiliate Programs (Recurring)",
        description="PartnerStack, Rewardful, and direct SaaS programs pay 20-40% recurring commission. "
                    "Notion ($10/signup), Webflow ($50/sale), Jasper (30% recurring), Surfer SEO (25% recurring), "
                    "ConvertKit (30% recurring for 24 months). One blog post ranking for 'best X tool' "
                    "can pay $200-2,000/mo indefinitely.",
        est_revenue_low=100,
        est_revenue_high=2000,
        startup_cost=0,
        time_to_first_dollar="7-30 days",
        existing_assets=assets,
        next_action="Sign up for PartnerStack + Impact. Apply to 5 SaaS programs matching our content niches "
                    "(AI tools, productivity, faith tech, fitness tech). Embed links in existing content.",
        priority=P1,
        status=NOT_STARTED,
        blockers=[],
        notes="Recurring SaaS commissions compound. 10 signups at $20/mo recurring = $200/mo passive after month 1, "
              "growing as you add more referrals. Medium articles with affiliate links are an evergreen play.",
    ))

    # Amazon Associates
    ops.append(Opportunity(
        category="affiliate",
        name="Amazon Associates (Physical Products)",
        description="1-10% commission but massive catalog. Prayer journals, fitness equipment, tech gadgets. "
                    "Low per-sale but high volume potential. Cookie lasts 24 hours (90 days if added to cart). "
                    "Real money is in high-ticket categories: electronics (4%), luxury beauty (10%).",
        est_revenue_low=50,
        est_revenue_high=500,
        startup_cost=0,
        time_to_first_dollar="14-30 days",
        existing_assets=["Content in faith, fitness, tech niches can all embed product links"],
        next_action="Sign up for Amazon Associates. Create 3 'best of' listicle articles in each niche. "
                    "Embed links in existing Medium/Substack content.",
        priority=P2,
        status=NOT_STARTED,
        blockers=["Need website with content (or social with 500+ followers for some programs)"],
        notes="Amazon rejects applications without existing traffic. Apply after listing Gumroad products "
              "and publishing 5+ Medium articles. Alternative: use existing content on personal site.",
    ))

    # Impact / ShareASale / CJ
    ops.append(Opportunity(
        category="affiliate",
        name="Impact/ShareASale/CJ Network Programs",
        description="Aggregator networks with thousands of merchants. ShareASale has Tailwind ($15/sale), "
                    "Grammarly ($20/sale), WP Engine ($200/sale). Impact has Shopify ($150 bounty), "
                    "Canva ($36/sale). CJ has GoDaddy, Overstock, TurboTax.",
        est_revenue_low=100,
        est_revenue_high=1000,
        startup_cost=0,
        time_to_first_dollar="14-30 days",
        existing_assets=assets,
        next_action="Apply to Impact, ShareASale, CJ Affiliate. Target 3 merchants per network "
                    "that align with existing content.",
        priority=P2,
        status=NOT_STARTED,
        blockers=[],
        notes="Pro tip: many programs auto-approve. Apply to 20+, get accepted to 10+, "
              "focus on the 3-5 that match your content.",
    ))

    return ops


def scan_freelance_platforms() -> List[Opportunity]:
    """Category 3: Fiverr, Upwork, Toptal service listings."""
    ops = []

    # Check existing service specs
    service_file = OPS / "SERVICE_OFFERING_PACKAGES.md"
    service_exists = file_exists(service_file)

    cold_outbound = MONEY_METHODS / "COLD_OUTBOUND"
    cold_outbound_exists = dir_exists(cold_outbound)

    local_biz_pipeline = AUTOMATIONS / "local_biz_pipeline.py"
    local_biz_exists = file_exists(local_biz_pipeline)

    auto_clip = AUTOMATIONS / "auto_clip_pipeline.py"
    auto_clip_exists = file_exists(auto_clip)

    assets = []
    if service_exists:
        assets.append("OPS/SERVICE_OFFERING_PACKAGES.md (service packages already spec'd)")
    if local_biz_exists:
        assets.append("AUTOMATIONS/local_biz_pipeline.py (automated website audit tool)")
    if auto_clip_exists:
        assets.append("AUTOMATIONS/auto_clip_pipeline.py (automated video clipping)")
    if cold_outbound_exists:
        assets.append("MONEY_METHODS/COLD_OUTBOUND/ (email sequences + templates)")

    # AI content writing service
    ops.append(Opportunity(
        category="freelance",
        name="Fiverr: AI-Powered Content Writing",
        description="Offer blog posts, email sequences, and social content packages on Fiverr. "
                    "Use Claude/GPT to 10x output. Charge $50-200/article, cost ~$5 in API calls. "
                    "Top content writers on Fiverr do $5K-15K/mo. New sellers get boosted for 60 days.",
        est_revenue_low=200,
        est_revenue_high=3000,
        startup_cost=0,
        time_to_first_dollar="7-21 days",
        existing_assets=assets,
        next_action="Create Fiverr seller account. List 3 gigs: blog writing, email sequences, social media content. "
                    "Price gig 1 at $25 for first 5 reviews (loss leader), then raise to $75-150.",
        priority=P1,
        status=NOT_STARTED,
        blockers=["Need Fiverr seller account"],
        notes="Fiverr new seller boost lasts 60 days. Undercut initially, stack reviews, raise prices. "
              "Upsell from $25 blog post to $200 content package. "
              "Deliver in 24h (AI makes this trivial) to win 'fast delivery' badge.",
    ))

    # Website audit / redesign service
    ops.append(Opportunity(
        category="freelance",
        name="Fiverr/Upwork: Local Business Website Audit",
        description="Use the existing local_biz_pipeline.py to auto-audit sites, then sell the fix. "
                    "Charge $200-500 for audit + recommendations, $1,500-5,000 for full redesign. "
                    "Pipeline already built: scrape, score, generate pitch.",
        est_revenue_low=500,
        est_revenue_high=5000,
        startup_cost=0,
        time_to_first_dollar="7-30 days",
        existing_assets=assets,
        next_action="List website audit gig on Fiverr ($99 audit, $499 audit + action plan). "
                    "Run local_biz_pipeline.py on 50 prospects. Cold email the worst-scoring ones with free preview." if local_biz_exists
                    else "Build local biz audit tool first, then list service",
        priority=P0 if local_biz_exists else P2,
        status=READY_TO_LAUNCH if local_biz_exists else NOT_STARTED,
        blockers=["Need Fiverr/Upwork account"],
        notes="This is the highest-margin freelance play. Automated audit takes 30 seconds. "
              "Charge $200+ for what takes you 5 minutes. The Gumroad product (Local Biz Client Machine at $97) "
              "teaches others this same system -- meta-level monetization.",
    ))

    # Video clipping service
    ops.append(Opportunity(
        category="freelance",
        name="Fiverr: Video Clipping Service",
        description="Use auto_clip_pipeline.py to clip podcasts/streams into viral shorts. "
                    "Charge $50-150 per batch of 10 clips. Podcasters/streamers pay $200-500/mo for ongoing clipping. "
                    "Your cost: ~$2 in compute per batch.",
        est_revenue_low=300,
        est_revenue_high=2000,
        startup_cost=0,
        time_to_first_dollar="7-21 days",
        existing_assets=[
            "AUTOMATIONS/auto_clip_pipeline.py (yt-dlp + whisper + Claude + ffmpeg)"
        ] if auto_clip_exists else [],
        next_action="List clipping gig on Fiverr. Run 3 demo clips from popular podcasts as portfolio samples. "
                    "Price: $15/clip or $99 for 10 clips." if auto_clip_exists
                    else "Set up auto_clip_pipeline.py dependencies first",
        priority=P1 if auto_clip_exists else P2,
        status=READY_TO_LAUNCH if auto_clip_exists else NOT_STARTED,
        blockers=["Need Fiverr account", "Need portfolio samples"],
        notes="Clipping market is booming. Podcasters and streamers pay $300-1,000/mo for ongoing clipping. "
              "Automation gives you 95%+ margins. Retainer clients are the real money.",
    ))

    # Upwork AI automation consulting
    ops.append(Opportunity(
        category="freelance",
        name="Upwork: AI Automation Consulting",
        description="Sell AI workflow setup as a service. Charge $500-2,000 per engagement. "
                    "Set up Claude/GPT automations, n8n workflows, content pipelines. "
                    "Position as 'AI operations consultant' not 'prompt writer'.",
        est_revenue_low=500,
        est_revenue_high=5000,
        startup_cost=0,
        time_to_first_dollar="14-30 days",
        existing_assets=assets,
        next_action="Create Upwork profile emphasizing AI automation. List 3 service offerings: "
                    "content automation setup ($500), full AI ops audit ($1,500), custom workflow build ($2,000).",
        priority=P1,
        status=NOT_STARTED,
        blockers=["Need Upwork profile"],
        notes="Upwork favors profiles with 100% Job Success Score. Take first 2-3 jobs at lower rate "
              "to build score, then raise to $100-200/hr. The AI Automation Toolkit Gumroad product "
              "serves as your portfolio/proof.",
    ))

    return ops


def scan_content_clipping() -> List[Opportunity]:
    """Category 4: Clip for others + recruit clippers for our content."""
    ops = []

    auto_clip = AUTOMATIONS / "auto_clip_pipeline.py"
    clip_scheduler = AUTOMATIONS / "clip_post_scheduler.py"

    assets = []
    if file_exists(auto_clip):
        assets.append("AUTOMATIONS/auto_clip_pipeline.py")
    if file_exists(clip_scheduler):
        assets.append("AUTOMATIONS/clip_post_scheduler.py")

    # Clipping as a service (covered in freelance too, but different angle here)
    ops.append(Opportunity(
        category="clipping",
        name="Clip Army: Recruit Clippers on Revenue Share",
        description="Model proven by @theclipgod and similar: recruit 10-50 clippers, "
                    "they clip content from creators, you manage distribution and take 20-50% rev share. "
                    "Zero cost. Clippers are motivated by learning + rev share. "
                    "Scale: 50 clippers x 5 clips/day = 250 clips/day across platforms.",
        est_revenue_low=200,
        est_revenue_high=3000,
        startup_cost=0,
        time_to_first_dollar="14-30 days",
        existing_assets=assets,
        next_action="Create Discord server for clip army. Post recruitment in r/editors, r/NewTubers, "
                    "Twitter. Offer: free training + 50% rev share on clips that monetize.",
        priority=P2,
        status=NOT_STARTED,
        blockers=["Need Discord server", "Need 2-3 creator partnerships for content supply"],
        notes="The clip army model prints because clippers do the work for free (they learn editing). "
              "You provide the distribution + creator relationships. "
              "Whop funnel teardown guide covers this exact model ($50-100K/mo proven).",
    ))

    # Our own clipping operation
    ops.append(Opportunity(
        category="clipping",
        name="Automated Clip Pipeline for Own Content",
        description="Run auto_clip_pipeline.py on trending podcasts/streams in our niches. "
                    "Post clips to TikTok/Reels/Shorts with credit. Monetize via creator programs. "
                    "Also: clip our own future content for multi-platform distribution.",
        est_revenue_low=50,
        est_revenue_high=500,
        startup_cost=0,
        time_to_first_dollar="30-60 days",
        existing_assets=assets,
        next_action="Run auto_clip_pipeline.py on 5 popular faith/fitness/tech podcasts. "
                    "Post 20 clips to new TikTok account. Test engagement before scaling.",
        priority=P2,
        status=READY_TO_LAUNCH if file_exists(auto_clip) else NOT_STARTED,
        blockers=["Need TikTok account", "Need yt-dlp + ffmpeg installed"] if not file_exists(auto_clip) else ["Need TikTok account"],
        notes="Clip accounts can grow fast (10K followers in 30 days if clips go viral). "
              "Monetization comes from TikTok Creator Fund + affiliate links in bio.",
    ))

    return ops


def scan_dropship_arbitrage() -> List[Opportunity]:
    """Category 5: Dropship, arbitrage, POD."""
    ops = []

    ecom_scanner = AUTOMATIONS / "ecom_arb_scanner.py"
    trending_scanner = AUTOMATIONS / "trending_products_scanner.py"
    pod_dir = MONEY_METHODS / "POD"
    pod_opportunities = MONEY_METHODS / "POD" / "TRENDING_OPPORTUNITIES.csv"
    tiktok_shop = MONEY_METHODS / "TIKTOK_SHOP"

    assets = []
    if file_exists(ecom_scanner):
        assets.append("AUTOMATIONS/ecom_arb_scanner.py")
    if file_exists(trending_scanner):
        assets.append("AUTOMATIONS/trending_products_scanner.py")
    if dir_exists(pod_dir):
        assets.append("MONEY_METHODS/POD/ (POD playbook + trending opportunities)")
    if file_exists(pod_opportunities):
        pod_rows = read_csv_rows(pod_opportunities)
        assets.append(f"POD/TRENDING_OPPORTUNITIES.csv ({len(pod_rows)} trending designs)")

    # Print on Demand
    ops.append(Opportunity(
        category="dropship",
        name="Print-on-Demand via Printful/Printify",
        description="Upload designs to Printful/Printify connected to Etsy or standalone store. "
                    "$0 upfront -- they print and ship on order. Margins: 30-60% on apparel, "
                    "40-70% on mugs/posters. Trending meme phrases convert best.",
        est_revenue_low=100,
        est_revenue_high=2000,
        startup_cost=0,
        time_to_first_dollar="7-30 days",
        existing_assets=assets,
        next_action="Create Printful account. Connect to Etsy. Upload 10 designs from trending phrases "
                    "(check POD/TRENDING_OPPORTUNITIES.csv). Launch.",
        priority=P1,
        status=READY_TO_LAUNCH if file_exists(pod_opportunities) else NOT_STARTED,
        blockers=["Need Printful account", "Need Etsy shop or standalone store"],
        notes="POD is a volume game. 100 designs, 5 will sell. The trending meme playbook "
              "at MONEY_METHODS/POD/TRENDING_MEME_POD_PLAYBOOK.md has the strategy. "
              "Best niches: faith statements, gym motivation, tech humor, pet quotes.",
    ))

    # TikTok Shop Affiliate
    if dir_exists(tiktok_shop):
        assets.append("MONEY_METHODS/TIKTOK_SHOP/ (TikTok Shop playbook)")

    ops.append(Opportunity(
        category="dropship",
        name="TikTok Shop Affiliate (Zero Inventory)",
        description="Promote other sellers' products on TikTok Shop for 15-30% commission. "
                    "$0 cost. Small creators (<50K followers) get 4.3x higher CTR than big accounts. "
                    "Beauty, skincare, and kitchen gadgets convert highest.",
        est_revenue_low=100,
        est_revenue_high=3000,
        startup_cost=0,
        time_to_first_dollar="14-30 days",
        existing_assets=assets,
        next_action="Apply for TikTok Shop affiliate program. Select 5 trending products. "
                    "Create 3 demo/review videos per product using AI voiceover.",
        priority=P1,
        status=NOT_STARTED,
        blockers=["Need TikTok account with 1K+ followers (or apply as new creator)"],
        notes="TikTok Shop affiliate is the hottest zero-cost play in 2026. "
              "Product sample programs give you free inventory to review. "
              "Commission stacks: 15-30% product + TikTok creator fund.",
    ))

    return ops


def scan_domain_flipping() -> List[Opportunity]:
    """Category 6: Expired domains, brandable names."""
    ops = []

    ops.append(Opportunity(
        category="domain",
        name="Expired Domain Flipping (Free Research)",
        description="Scan ExpiredDomains.net for domains with existing backlinks/DA. "
                    "Register for $8-12, flip for $50-500. Target: .com domains with DA 10+, "
                    "existing backlinks, brandable names in trending niches (AI, faith tech, fitness apps). "
                    "Also: hand-register brandable names for $8-12 and list on Afternic/Sedo.",
        est_revenue_low=50,
        est_revenue_high=500,
        startup_cost=0,
        time_to_first_dollar="30-90 days",
        existing_assets=["Research is free. Registration costs $8-12 per domain."],
        next_action="Browse ExpiredDomains.net for .com domains with DA 10+ in AI/faith/fitness niches. "
                    "Register 2-3 best finds. List on Afternic, Sedo, and Dan.com.",
        priority=P3,
        status=NOT_STARTED,
        blockers=["Requires $8-12 per domain registration (not truly $0)"],
        notes="Domain flipping is a slower play but can hit big. Focus on AI-related names "
              "('aiX.com' pattern) since AI domain prices are inflated right now. "
              "Brandable 2-word .coms sell for $200-2,000 on average.",
    ))

    return ops


def scan_ai_music_streaming() -> List[Opportunity]:
    """Category 7: Suno/Udio to DistroKid to Spotify."""
    ops = []

    sleep_yt = MONEY_METHODS / "CONTENT_FARM" / "SLEEP_YOUTUBE"
    sleep_exists = dir_exists(sleep_yt)

    assets = []
    if sleep_exists:
        assets.append("MONEY_METHODS/CONTENT_FARM/SLEEP_YOUTUBE/ (sleep channel kit built)")

    ops.append(Opportunity(
        category="ai_music",
        name="AI Ambient/Lo-fi Music on Spotify",
        description="Generate lo-fi, ambient, worship, or study music with Suno/Udio (free tier: 10 songs/day). "
                    "Distribute via DistroKid ($22/yr unlimited uploads). Spotify pays $3-5/1K streams. "
                    "One album of 10 study beats can pull 5K-50K streams/mo if playlisted.",
        est_revenue_low=20,
        est_revenue_high=500,
        startup_cost=0,
        time_to_first_dollar="30-90 days",
        existing_assets=assets,
        next_action="Generate 10 lo-fi study beats on Suno free tier. Create artist profile. "
                    "Upload to DistroKid. Submit to Spotify playlists via SubmitHub (free tier) "
                    "and SpotOnTrack.",
        priority=P2,
        status=NOT_STARTED,
        blockers=["Need DistroKid account ($22/yr -- cheapest tier)"],
        notes="AI music is a compounding play. Each track earns forever. 100 tracks x 1K streams/mo each "
              "= 100K streams/mo = $300-500/mo passive. Sleep/study/worship playlists have the most "
              "consistent streams (people play them 8+ hours). The sleep YouTube kit is a synergy play.",
    ))

    # AI worship music specifically
    ops.append(Opportunity(
        category="ai_music",
        name="AI Worship/Devotional Music (Faith Niche)",
        description="Generate worship instrumentals and devotional ambient music. "
                    "Faith music listeners are highly loyal and stream repeatedly. "
                    "Cross-promote with PrayerLock app and faith newsletter.",
        est_revenue_low=10,
        est_revenue_high=200,
        startup_cost=0,
        time_to_first_dollar="30-90 days",
        existing_assets=assets + ["PrayerLock PWA (cross-promo opportunity)"],
        next_action="Generate 5 worship instrumentals on Suno. Title for SEO: "
                    "'Morning Prayer Piano', 'Evening Devotional Ambient', etc.",
        priority=P3,
        status=NOT_STARTED,
        blockers=["Need DistroKid account"],
        notes="Synergy with faith content empire. Music links in newsletter, app, social posts. "
              "Worship music has extremely loyal repeat listeners.",
    ))

    return ops


def scan_directory_listings() -> List[Opportunity]:
    """Category 8: Product Hunt, AlternativeTo, G2, etc."""
    ops = []

    launch_dirs = read_csv_rows(LEDGER / "LAUNCH_DIRECTORIES.csv")
    prayerlock = APP_FACTORY / "builds" / "prayerlock-web"
    prayerlock_exists = dir_exists(prayerlock)
    biomaxx = APP_FACTORY / "builds" / "biomaxx-sdk54"
    biomaxx_exists = dir_exists(biomaxx)

    ph_launch = prayerlock / "PRODUCT_HUNT_LAUNCH.md" if prayerlock_exists else None
    ph_exists = ph_launch and file_exists(ph_launch)

    assets = []
    if launch_dirs:
        assets.append(f"LEDGER/LAUNCH_DIRECTORIES.csv ({len(launch_dirs)} directories tracked)")
    if prayerlock_exists:
        assets.append("APP_FACTORY/builds/prayerlock-web/ (PWA ready to deploy)")
    if biomaxx_exists:
        assets.append("APP_FACTORY/builds/biomaxx-sdk54/ (app ready)")
    if ph_exists:
        assets.append("prayerlock-web/PRODUCT_HUNT_LAUNCH.md (PH launch plan written)")

    ops.append(Opportunity(
        category="directory",
        name="Product Hunt Launch (PrayerLock)",
        description="Product Hunt gives massive Day 1 traffic. Top 5 products get 5K-30K visitors. "
                    "Even top 20 gets 500-2K. PrayerLock PWA is ready to deploy. "
                    f"Launch plan {'already written' if ph_exists else 'needs to be written'}.",
        est_revenue_low=0,
        est_revenue_high=500,
        startup_cost=0,
        time_to_first_dollar="1-7 days (traffic -> Gumroad sales from profile link)",
        existing_assets=assets,
        next_action="Deploy PrayerLock to Vercel. Submit to Product Hunt with 5 upvote commitments. "
                    "Cross-post to HackerNews Show HN.",
        priority=P0 if prayerlock_exists else P2,
        status=READY_TO_LAUNCH if prayerlock_exists else NOT_STARTED,
        blockers=["Need to deploy PrayerLock first", "Need Product Hunt account"],
        notes="Product Hunt is free. The traffic spike alone can generate Gumroad sales if profile "
              "links to products. Also submit to AlternativeTo, SaaSHub, BetaList. "
              f"LEDGER tracks {len(launch_dirs)} directories to submit to.",
    ))

    # Submit to ALL directories
    ops.append(Opportunity(
        category="directory",
        name="Mass Directory Submission (All Apps/Products)",
        description=f"{len(launch_dirs)} directories tracked in LEDGER. Most are free. "
                    "Each submission = permanent backlink + discovery traffic. "
                    "Batch submission takes 2-3 hours, gives months of organic traffic.",
        est_revenue_low=0,
        est_revenue_high=200,
        startup_cost=0,
        time_to_first_dollar="7-30 days (indirect via traffic)",
        existing_assets=assets,
        next_action="Go through LAUNCH_DIRECTORIES.csv row by row. Submit each product to every "
                    "applicable directory. Track submission date and status.",
        priority=P1 if prayerlock_exists or biomaxx_exists else P3,
        status=NOT_STARTED,
        blockers=["Need at least 1 deployed product"],
        notes="This is grunt work but high ROI per hour. Each directory submission takes 5-15 min. "
              "Do 10/day for a week = 70 submissions = months of backlink juice + discovery.",
    ))

    return ops


def scan_free_tool_arbitrage() -> List[Opportunity]:
    """Category 9: Use free tool tiers to deliver paid services."""
    ops = []

    tools = read_csv_rows(LEDGER / "TOOLS_SERVICES_MASTER.csv")
    free_tools = [t for t in tools if t.get("free_tier", "").upper() in ("YES", "TRUE")]

    assets = []
    if free_tools:
        assets.append(f"LEDGER/TOOLS_SERVICES_MASTER.csv ({len(free_tools)} tools with free tiers)")

    ops.append(Opportunity(
        category="free_tool_arb",
        name="Canva Free Tier Design Service",
        description="Canva free tier gives access to thousands of templates. "
                    "Offer social media design packages on Fiverr: 30 branded posts for $50-150. "
                    "Your time: 30 min with Canva templates. Client's alternative: hire designer for $500+.",
        est_revenue_low=200,
        est_revenue_high=1500,
        startup_cost=0,
        time_to_first_dollar="7-14 days",
        existing_assets=assets,
        next_action="Create 3 portfolio samples in Canva (faith, fitness, business niches). "
                    "List on Fiverr: '30 Social Media Posts - $49' as starter gig.",
        priority=P1,
        status=NOT_STARTED,
        blockers=["Need Fiverr account"],
        notes="Canva free -> paid service is one of the highest-margin freelance plays. "
              "Upsell: $49 for 30 posts -> $149 for 30 posts + stories + highlights. "
              "Canva Pro ($13/mo) only needed if client wants premium templates.",
    ))

    ops.append(Opportunity(
        category="free_tool_arb",
        name="AI Tool Arbitrage (Free API Tiers)",
        description="Claude free tier, GPT free tier, Gemini free tier, Mistral free tier. "
                    "Stack free tiers across providers for ~500K tokens/day total. "
                    "Sell AI-written deliverables: cold emails, product descriptions, blog posts. "
                    "Charge $25-100 per deliverable, cost $0.",
        est_revenue_low=200,
        est_revenue_high=2000,
        startup_cost=0,
        time_to_first_dollar="7-14 days",
        existing_assets=assets,
        next_action="Stack free tiers: Claude.ai (free), ChatGPT (free), Gemini (free). "
                    "Offer AI content writing service. Deliver using whichever model performs best per task.",
        priority=P1,
        status=NOT_STARTED,
        blockers=[],
        notes="The arbitrage: clients think AI content costs money. It doesn't on free tiers. "
              "You charge for expertise in prompting + editing + quality control, not the AI itself.",
    ))

    return ops


def scan_plr_mrr_resale() -> List[Opportunity]:
    """Category 10: PLR and MRR digital products."""
    ops = []

    ops.append(Opportunity(
        category="plr_mrr",
        name="PLR Product Bundle Resale",
        description="Buy PLR (Private Label Rights) bundles for $5-27 one-time. Rebrand. "
                    "Sell as your own for $17-97 each. Categories: business templates, social media kits, "
                    "email sequences, ebook templates. Rebrand takes 30 min per product.",
        est_revenue_low=50,
        est_revenue_high=500,
        startup_cost=0,
        time_to_first_dollar="3-14 days",
        existing_assets=["Gumroad store (once set up) for distribution"],
        next_action="Browse PLRMines.com, BigProductStore.com, or InDigitalWorks.com for $0-5 PLR packs. "
                    "Rebrand top 3 products. List on Gumroad/Whop.",
        priority=P2,
        status=NOT_STARTED,
        blockers=["Need to find quality PLR sources (many are low quality)"],
        notes="PLR quality varies wildly. The play: find decent PLR, add your expertise, "
              "rebrand with better copy and design, price 3-5x what you paid. "
              "MRR (Master Resell Rights) products can be sold AND give buyers resell rights "
              "= viral distribution mechanism.",
    ))

    return ops


def scan_template_marketplaces() -> List[Opportunity]:
    """Category 11: Notion, Canva, Figma template stores."""
    ops = []

    # Check if we have templates mentioned in products
    products_csv = read_csv_rows(LEDGER / "PRODUCTS.csv")
    notion_products = [p for p in products_csv if "notion" in (p.get("Name", "") + p.get("notes", "")).lower()]

    ops.append(Opportunity(
        category="template",
        name="Notion Template Marketplace",
        description="Notion has a built-in template marketplace. Templates sell for $5-49. "
                    "Top templates do $1K-10K/mo. Faith planner, fitness tracker, solopreneur OS, "
                    "content calendar, habit tracker all convert well. "
                    "Notion pays 90% of sales (10% platform fee).",
        est_revenue_low=50,
        est_revenue_high=1000,
        startup_cost=0,
        time_to_first_dollar="7-30 days",
        existing_assets=["Existing product specs can be adapted as Notion templates"],
        next_action="Build 3 Notion templates: Solopreneur OS ($29), Faith Daily Planner ($9), "
                    "Content Calendar ($19). Submit to Notion template marketplace + list on Gumroad.",
        priority=P1,
        status=NOT_STARTED,
        blockers=["Need to build the actual Notion templates"],
        notes="Notion templates have insane margins. Build once, sell forever. "
              "The Notion marketplace has less competition than Gumroad. "
              "Gumroad + Notion marketplace + Etsy = triple distribution for same product.",
    ))

    ops.append(Opportunity(
        category="template",
        name="Canva Template Store",
        description="Canva Creators program lets you sell templates in Canva's marketplace. "
                    "Social media templates, presentation decks, Instagram story templates. "
                    "Canva pays 35% royalty per use. Volume play: 100 templates x modest usage = $200-1K/mo.",
        est_revenue_low=50,
        est_revenue_high=500,
        startup_cost=0,
        time_to_first_dollar="30-60 days",
        existing_assets=[],
        next_action="Apply for Canva Creator program. Build 10 social media template sets "
                    "(faith quotes, fitness motivation, business tips). Submit.",
        priority=P2,
        status=NOT_STARTED,
        blockers=["Need Canva Creator approval (portfolio required)"],
        notes="Canva Creator approval takes 2-4 weeks. Lower royalty than selling direct but "
              "massive marketplace traffic. Good passive income layer.",
    ))

    return ops


def scan_community_monetization() -> List[Opportunity]:
    """Category 12: Discord, Telegram, Skool communities."""
    ops = []

    newsletter_dir = MONEY_METHODS / "NEWSLETTER"
    newsletter_exists = dir_exists(newsletter_dir)
    welcome_sequences = []
    for seq in ["WELCOME_SEQUENCE_FAITH.md", "WELCOME_SEQUENCE_FITNESS.md", "WELCOME_SEQUENCE_TECH.md"]:
        if file_exists(newsletter_dir / seq):
            welcome_sequences.append(seq)

    assets = []
    if welcome_sequences:
        assets.append(f"MONEY_METHODS/NEWSLETTER/ ({len(welcome_sequences)} welcome sequences ready)")

    ops.append(Opportunity(
        category="community",
        name="Free Discord/Telegram Community -> Premium Tier",
        description="Start free community in strongest niche (solopreneur/AI tools recommended). "
                    "Provide daily value: tool finds, alpha, tips. At 100+ members, launch premium tier "
                    "($29-99/mo). Conversion rate on engaged free -> paid: 3-8%.",
        est_revenue_low=100,
        est_revenue_high=2000,
        startup_cost=0,
        time_to_first_dollar="30-60 days",
        existing_assets=assets + ["1,008 social posts ready (content to share in community)"],
        next_action="Create Discord server with channels: #general, #tools, #alpha, #wins, #support. "
                    "Invite first 20 members from Twitter followers. Post daily value for 30 days. "
                    "Launch paid tier at 100+ members.",
        priority=P2,
        status=NOT_STARTED,
        blockers=["Need 100+ community members before monetizing"],
        notes="Communities have the highest LTV of any digital product. $49/mo x 50 members = $2,450/mo. "
              "Skool is the premium play ($99/mo platform fee but higher perceived value). "
              "Discord/Telegram are free to run. The Whop funnel teardown shows community models printing $50K+/mo.",
    ))

    return ops


def scan_cold_email_free() -> List[Opportunity]:
    """Category 13: Gmail free tier cold outreach."""
    ops = []

    cold_outbound = MONEY_METHODS / "COLD_OUTBOUND"
    outreach_pipeline = read_csv_rows(LEDGER / "OUTREACH_PIPELINE.csv")
    email_sequences = cold_outbound / "EMAIL_SEQUENCES_TIER1.md" if dir_exists(cold_outbound) else None
    tier1_exists = email_sequences and file_exists(email_sequences)

    assets = []
    if dir_exists(cold_outbound):
        assets.append("MONEY_METHODS/COLD_OUTBOUND/ (cold email playbooks)")
    if tier1_exists:
        assets.append("COLD_OUTBOUND/EMAIL_SEQUENCES_TIER1.md")
    if outreach_pipeline:
        assets.append(f"LEDGER/OUTREACH_PIPELINE.csv ({len(outreach_pipeline)} prospects tracked)")

    active_leads = [r for r in outreach_pipeline if r.get("status") in ("qualified", "discovery", "nurture")]

    ops.append(Opportunity(
        category="cold_email",
        name="Gmail Cold Outreach (500/day Free)",
        description="Gmail allows ~500 emails/day per account for free. "
                    "With 3 Gmail accounts = 1,500 emails/day. No paid tools needed. "
                    "Use existing cold email sequences. Target: local businesses, SaaS companies, "
                    "content creators who need services.",
        est_revenue_low=500,
        est_revenue_high=5000,
        startup_cost=0,
        time_to_first_dollar="7-21 days",
        existing_assets=assets,
        next_action="Create 3 Gmail accounts. Warm for 7 days (send 10-20 normal emails/day). "
                    "Start sending cold emails at 20/day, ramp to 100/day by week 2. "
                    "Use email sequences from COLD_OUTBOUND/." if tier1_exists
                    else "Write cold email sequences, then set up Gmail accounts",
        priority=P0 if tier1_exists else P1,
        status=READY_TO_LAUNCH if tier1_exists and len(active_leads) > 0 else NOT_STARTED,
        blockers=["Gmail warmup takes 7-14 days"],
        notes=f"Currently tracking {len(outreach_pipeline)} prospects in pipeline. "
              f"{len(active_leads)} are active leads. "
              "The cold email playbook on Gumroad ($27) teaches this exact system = meta-monetization. "
              "Critical: use Google Workspace ($6/mo/user) for better deliverability. "
              "Free Gmail works but higher spam risk.",
    ))

    return ops


def scan_content_syndication() -> List[Opportunity]:
    """Category 14: Medium Partner Program, Substack, HackerNoon, dev.to."""
    ops = []

    medium_dir = CONTENT / "medium_articles"
    substack_dir = CONTENT / "substack_posts"
    medium_exists = dir_exists(medium_dir)
    substack_exists = dir_exists(substack_dir)

    medium_count = count_files(medium_dir, "*.md") if medium_exists else 0
    buffer_csvs = count_files(LEDGER, "buffer_import_*.csv")
    reply_templates = CONTENT / "social" / "REPLY_TEMPLATES_100.md"
    content_cal = LEDGER / "CONTENT_CALENDAR_30DAY.csv"

    assets = []
    if medium_exists:
        assets.append(f"CONTENT/medium_articles/ ({medium_count} articles)")
    if substack_exists:
        assets.append("CONTENT/substack_posts/")
    if buffer_csvs > 0:
        assets.append(f"LEDGER/buffer_import_*.csv ({buffer_csvs} CSVs ready for Buffer upload)")
    if file_exists(content_cal):
        assets.append("LEDGER/CONTENT_CALENDAR_30DAY.csv (1,008 posts mapped)")
    if file_exists(reply_templates):
        assets.append("CONTENT/social/REPLY_TEMPLATES_100.md")

    # Medium Partner Program
    ops.append(Opportunity(
        category="content_syndication",
        name="Medium Partner Program Articles",
        description="Medium pays writers based on member reading time. "
                    "Well-optimized articles in tech/business/self-improvement earn $50-500/article/month. "
                    f"{'Articles already written and ready to publish.' if medium_count > 0 else 'Need to write articles.'} "
                    "Medium's domain authority (DA 96) means your articles rank on Google fast.",
        est_revenue_low=50,
        est_revenue_high=1000,
        startup_cost=0,
        time_to_first_dollar="7-30 days",
        existing_assets=assets,
        next_action="Join Medium Partner Program (free). Publish existing articles from CONTENT/medium_articles/. "
                    "Optimize titles for SEO. Publish 3-5x/week for first month.",
        priority=P0 if medium_count > 0 else P1,
        status=READY_TO_LAUNCH if medium_count > 0 else NOT_STARTED,
        blockers=["Need Medium account with Partner Program enabled"],
        notes="Medium SEO hack: write articles targeting 'best X for Y' keywords. "
              "Medium's DA means you outrank most blogs. Embed Gumroad affiliate links in articles. "
              "Double monetization: Medium partner revenue + affiliate commissions.",
    ))

    # Substack paid subscriptions
    ops.append(Opportunity(
        category="content_syndication",
        name="Substack Paid Newsletter",
        description="Substack is free to start, takes 10% of paid subscriptions. "
                    "Write in solopreneur/AI tools niche. Free tier builds audience, "
                    "paid tier ($5-10/mo) for premium content. Substack Notes = built-in discovery. "
                    "1,000 free subscribers -> 30-50 paid @ $7/mo = $210-350/mo.",
        est_revenue_low=50,
        est_revenue_high=500,
        startup_cost=0,
        time_to_first_dollar="30-90 days",
        existing_assets=assets,
        next_action="Create Substack. Import/cross-post existing Medium articles. "
                    "Publish 2x/week. Use Substack Notes for discovery. "
                    "Enable paid tier at 500 free subscribers.",
        priority=P1,
        status=READY_TO_LAUNCH if substack_exists else NOT_STARTED,
        blockers=["Need Substack account", "Need 500+ free subscribers before paid makes sense"],
        notes="Substack's recommendation algorithm can grow you faster than Medium. "
              "Cross-post between Medium and Substack (different audiences, same content). "
              "Welcome sequences already written at MONEY_METHODS/NEWSLETTER/.",
    ))

    # dev.to / HackerNoon
    ops.append(Opportunity(
        category="content_syndication",
        name="dev.to + HackerNoon Technical Content",
        description="dev.to is free to post on with massive developer audience. "
                    "HackerNoon pays writers (revenue share). Both index well on Google. "
                    "Write: AI tool reviews, vibe coding tutorials, automation how-tos. "
                    "Each post can include affiliate links + link back to products.",
        est_revenue_low=20,
        est_revenue_high=300,
        startup_cost=0,
        time_to_first_dollar="14-30 days",
        existing_assets=assets,
        next_action="Create dev.to and HackerNoon accounts. Publish 3 articles: "
                    "'How I Built X with Vibe Coding', 'Top 10 AI Tools for Solopreneurs', "
                    "'Automating Content Distribution with Python'.",
        priority=P2,
        status=NOT_STARTED,
        blockers=[],
        notes="dev.to has 1M+ monthly visitors. Canonical URL feature lets you cross-post "
              "without SEO penalties. HackerNoon editor review takes 1-3 days.",
    ))

    return ops


def scan_referral_bounty_programs() -> List[Opportunity]:
    """Category 15: SaaS referral programs with cash bounties."""
    ops = []

    # Known high-value referral programs
    referral_programs = [
        ("Notion", "$10/signup", "productivity"),
        ("Webflow", "$50/sale", "web design"),
        ("Shopify", "$150/referral", "ecommerce"),
        ("ConvertKit", "30% recurring 24mo", "email"),
        ("Jasper", "30% recurring", "AI writing"),
        ("Surfer SEO", "25% recurring", "SEO"),
        ("ClickUp", "$200/enterprise lead", "productivity"),
        ("Monday.com", "100% first payment", "project management"),
        ("Freshworks", "$300/enterprise", "CRM"),
        ("Semrush", "$200/sale + $10/trial", "SEO"),
    ]

    ops.append(Opportunity(
        category="referral",
        name="SaaS Referral Program Stack",
        description=f"{len(referral_programs)} high-value SaaS referral programs. "
                    "Write comparison articles ('Notion vs Obsidian', 'Best SEO Tools 2026'), "
                    "embed referral links. Each article can earn $50-500/mo in referral commissions "
                    "once it ranks. Stack: write articles on Medium (DA 96) with referral links. "
                    "Top programs: Shopify $150, Semrush $200, Freshworks $300 per referral.",
        est_revenue_low=100,
        est_revenue_high=2000,
        startup_cost=0,
        time_to_first_dollar="14-60 days",
        existing_assets=["Content in AI/tech niche naturally pairs with SaaS referrals"],
        next_action="Sign up for top 5 programs: Semrush, Shopify, ConvertKit, Surfer, Notion. "
                    "Write 3 comparison/review articles on Medium with embedded referral links.",
        priority=P1,
        status=NOT_STARTED,
        blockers=[],
        notes="Referral programs compound with content. One article ranking for 'best email marketing tool' "
              "can pay $200-500/mo indefinitely. Stack with Medium Partner Program revenue. "
              "Recurring commission programs (ConvertKit, Jasper) build passive income over time.",
    ))

    return ops


def scan_repo_monetization() -> List[Opportunity]:
    """Category 16: GitHub Sponsors, open source bounties, dual-license."""
    ops = []

    auto_clip_exists = file_exists(AUTOMATIONS / "auto_clip_pipeline.py")
    local_biz_exists = file_exists(AUTOMATIONS / "local_biz_pipeline.py")
    ecom_exists = file_exists(AUTOMATIONS / "ecom_arb_scanner.py")

    repo_assets = []
    if auto_clip_exists:
        repo_assets.append("AUTOMATIONS/auto_clip_pipeline.py")
    if local_biz_exists:
        repo_assets.append("AUTOMATIONS/local_biz_pipeline.py")
    if ecom_exists:
        repo_assets.append("AUTOMATIONS/ecom_arb_scanner.py")

    ops.append(Opportunity(
        category="repo",
        name="Open Source Tool + GitHub Sponsors",
        description="Build useful CLI tools or scripts, open-source them on GitHub. "
                    "Add GitHub Sponsors. Our existing Python automations "
                    "(auto_clip_pipeline, local_biz_pipeline, ecom_arb_scanner) could be packaged "
                    "as open-source tools. Sponsors pay $5-100/mo. 50 sponsors at $5 = $250/mo.",
        est_revenue_low=0,
        est_revenue_high=250,
        startup_cost=0,
        time_to_first_dollar="60-180 days",
        existing_assets=repo_assets,
        next_action="Pick the most useful automation script. Clean it up. Create GitHub repo with "
                    "good README, examples, and GitHub Sponsors enabled. Post to r/Python, HN.",
        priority=P3,
        status=NOT_STARTED,
        blockers=["Need clean public repo with good documentation"],
        notes="Open source is a long game but builds reputation + backlinks + sponsors. "
              "The real monetization: open-source free version, sell premium features or hosted version. "
              "Dual-license model: MIT for personal use, commercial license for businesses.",
    ))

    return ops


def scan_data_lead_lists() -> List[Opportunity]:
    """Category 17: Compile niche lead lists from public data, sell on Gumroad."""
    ops = []

    local_biz_scraper = AUTOMATIONS / "local_biz_website_scraper.py"
    local_biz_pipeline = AUTOMATIONS / "local_biz_pipeline.py"

    assets = []
    if file_exists(local_biz_scraper):
        assets.append("AUTOMATIONS/local_biz_website_scraper.py")
    if file_exists(local_biz_pipeline):
        assets.append("AUTOMATIONS/local_biz_pipeline.py")

    ops.append(Opportunity(
        category="data_leads",
        name="Niche Lead Lists on Gumroad",
        description="Compile lead lists from public data: Google Maps, Yelp, industry directories. "
                    "Package as CSV/Excel files. Sell on Gumroad for $27-97. "
                    "Niches: local dentists by city, SaaS founders with emails, "
                    "Etsy top sellers by category, YouTube channels in niche. "
                    "Our scraping tools already do the collection.",
        est_revenue_low=50,
        est_revenue_high=500,
        startup_cost=0,
        time_to_first_dollar="7-14 days",
        existing_assets=assets,
        next_action="Use local_biz_pipeline.py to scrape 500 dentists in top 10 US cities. "
                    "Package as 'US Dentist Lead List - 5,000 contacts'. List on Gumroad for $47.",
        priority=P1,
        status=READY_TO_LAUNCH if file_exists(local_biz_pipeline) else NOT_STARTED,
        blockers=["Verify data collection is compliant with CCPA/GDPR (public data only)"],
        notes="Lead lists are an evergreen product. Update monthly, charge for fresh data. "
              "Subscription model: $27/mo for monthly updated lists. "
              "Legal: only public data (business listings, public directories). No personal data scraping.",
    ))

    return ops


# ---------------------------------------------------------------------------
# SCANNER REGISTRY
# ---------------------------------------------------------------------------

SCANNER_REGISTRY = {
    "marketplace": scan_marketplace_listings,
    "affiliate": scan_affiliate_networks,
    "freelance": scan_freelance_platforms,
    "clipping": scan_content_clipping,
    "dropship": scan_dropship_arbitrage,
    "domain": scan_domain_flipping,
    "ai_music": scan_ai_music_streaming,
    "directory": scan_directory_listings,
    "free_tool_arb": scan_free_tool_arbitrage,
    "plr_mrr": scan_plr_mrr_resale,
    "template": scan_template_marketplaces,
    "community": scan_community_monetization,
    "cold_email": scan_cold_email_free,
    "content_syndication": scan_content_syndication,
    "referral": scan_referral_bounty_programs,
    "repo": scan_repo_monetization,
    "data_leads": scan_data_lead_lists,
}


def run_all_scanners() -> List[Opportunity]:
    """Run all scanners and return sorted opportunities."""
    all_ops = []
    for scanner_fn in SCANNER_REGISTRY.values():
        all_ops.extend(scanner_fn())
    all_ops.sort(key=lambda o: o.sort_key)
    return all_ops


def run_category_scanner(category: str) -> List[Opportunity]:
    """Run a single category scanner."""
    if category not in SCANNER_REGISTRY:
        print(f"ERROR: Unknown category '{category}'. Valid: {', '.join(CATEGORIES)}")
        sys.exit(1)
    ops = SCANNER_REGISTRY[category]()
    ops.sort(key=lambda o: o.sort_key)
    return ops


# ---------------------------------------------------------------------------
# OUTPUT FORMATTERS
# ---------------------------------------------------------------------------

def print_divider(char: str = "=", width: int = 80):
    print(char * width)


def print_header(title: str):
    print()
    print_divider()
    print(f"  {title}")
    print_divider()
    print()


def format_opportunity_text(op: Opportunity, index: int = 0) -> str:
    """Format a single opportunity as human-readable text."""
    lines = []
    lines.append(f"  [{op.priority}] {op.name}")
    lines.append(f"  Category: {op.category} | Status: {op.status}")
    lines.append(f"  Revenue: {op.est_revenue_range} | Cost: ${op.startup_cost} | Time: {op.time_to_first_dollar}")
    lines.append(f"  {op.description[:200]}{'...' if len(op.description) > 200 else ''}")
    if op.existing_assets:
        lines.append(f"  Assets: {', '.join(op.existing_assets[:3])}")
    lines.append(f"  NEXT: {op.next_action[:150]}")
    if op.blockers:
        lines.append(f"  BLOCKERS: {' | '.join(op.blockers)}")
    return "\n".join(lines)


def output_scan_results(ops: List[Opportunity]):
    """Print full scan results to terminal."""
    print_header("PRINTMAXX DAILY NO-COST RBI SCAN")
    print(f"  Date: {TODAY}")
    print(f"  Opportunities Found: {len(ops)}")
    print(f"  P0 (Do Today): {sum(1 for o in ops if o.priority == P0)}")
    print(f"  P1 (This Week): {sum(1 for o in ops if o.priority == P1)}")
    print(f"  P2 (Within 2 Weeks): {sum(1 for o in ops if o.priority == P2)}")
    print(f"  P3 (Backlog): {sum(1 for o in ops if o.priority == P3)}")
    print()

    ready = [o for o in ops if o.status == READY_TO_LAUNCH]
    if ready:
        print(f"  READY TO LAUNCH: {len(ready)} opportunities need ZERO additional work")
        for o in ready:
            print(f"    -> {o.name} ({o.est_revenue_range})")
        print()

    total_low = sum(o.est_revenue_low for o in ops)
    total_high = sum(o.est_revenue_high for o in ops)
    print(f"  Total Revenue Potential: ${total_low:,}-${total_high:,}/mo")
    p0_high = sum(o.est_revenue_high for o in ops if o.priority == P0)
    print(f"  P0 Revenue Potential: ${p0_high:,}/mo")
    print()

    # Group by category
    by_category = defaultdict(list)
    for op in ops:
        by_category[op.category].append(op)

    for cat in CATEGORIES:
        if cat not in by_category:
            continue
        cat_ops = by_category[cat]
        cat_revenue_high = sum(o.est_revenue_high for o in cat_ops)
        print_divider("-")
        print(f"  {cat.upper().replace('_', ' ')} ({len(cat_ops)} ops | up to ${cat_revenue_high:,}/mo)")
        print_divider("-")
        for i, op in enumerate(cat_ops):
            print(format_opportunity_text(op, i))
            print()


def output_next_actions(ops: List[Opportunity]):
    """Show top 10 next actions ranked by priority and revenue."""
    print_header("TOP 10 NEXT ACTIONS - DO THESE RIGHT NOW")

    # Sort by priority then revenue
    sorted_ops = sorted(ops, key=lambda o: o.sort_key)[:10]

    for i, op in enumerate(sorted_ops, 1):
        blocked_tag = " [BLOCKED]" if op.is_blocked else ""
        ready_tag = " [READY]" if op.status == READY_TO_LAUNCH else ""
        print(f"  {i}. [{op.priority}]{ready_tag}{blocked_tag} {op.name}")
        print(f"     Revenue: {op.est_revenue_range} | Time: {op.time_to_first_dollar}")
        wrapped = textwrap.wrap(op.next_action, width=70)
        for line in wrapped:
            print(f"     -> {line}")
        if op.blockers:
            print(f"     BLOCKERS: {' | '.join(op.blockers)}")
        print()


def output_revenue_map(ops: List[Opportunity]):
    """Show revenue projections by timeframe."""
    print_header("REVENUE MAP - PROJECTED MONTHLY INCOME BY TIMEFRAME")

    # Categorize by time to first dollar
    fast = [o for o in ops if any(x in o.time_to_first_dollar for x in ["1-7", "3-7", "3-14"])]
    medium = [o for o in ops if any(x in o.time_to_first_dollar for x in ["7-14", "7-21", "7-30", "14-30", "14-60"])]
    slow = [o for o in ops if any(x in o.time_to_first_dollar for x in ["30-60", "30-90", "60-180"])]

    # Deduplicate (an op can only be in one bucket)
    seen = set()
    fast_clean, medium_clean, slow_clean = [], [], []
    for o in fast:
        if o.name not in seen:
            fast_clean.append(o)
            seen.add(o.name)
    for o in medium:
        if o.name not in seen:
            medium_clean.append(o)
            seen.add(o.name)
    for o in slow:
        if o.name not in seen:
            slow_clean.append(o)
            seen.add(o.name)

    print("  FAST MONEY (1-14 days to first dollar):")
    for o in fast_clean:
        print(f"    {o.name}: {o.est_revenue_range}")
    fast_low = sum(o.est_revenue_low for o in fast_clean)
    fast_high = sum(o.est_revenue_high for o in fast_clean)
    print(f"    SUBTOTAL: ${fast_low:,}-${fast_high:,}/mo")
    print()

    print("  MEDIUM TERM (7-30 days to first dollar):")
    for o in medium_clean:
        print(f"    {o.name}: {o.est_revenue_range}")
    med_low = sum(o.est_revenue_low for o in medium_clean)
    med_high = sum(o.est_revenue_high for o in medium_clean)
    print(f"    SUBTOTAL: ${med_low:,}-${med_high:,}/mo")
    print()

    print("  SLOW BUILD (30-90+ days to first dollar):")
    for o in slow_clean:
        print(f"    {o.name}: {o.est_revenue_range}")
    slow_low = sum(o.est_revenue_low for o in slow_clean)
    slow_high = sum(o.est_revenue_high for o in slow_clean)
    print(f"    SUBTOTAL: ${slow_low:,}-${slow_high:,}/mo")
    print()

    total_low = sum(o.est_revenue_low for o in ops)
    total_high = sum(o.est_revenue_high for o in ops)
    print_divider("-")
    print(f"  ALL OPPORTUNITIES COMBINED: ${total_low:,}-${total_high:,}/mo")
    print()
    print("  CRITICAL PATH TO $1K/MO:")
    print("  Week 1: List Gumroad products + list Whop products + start Medium articles")
    print("  Week 2: Start cold email outreach + list Fiverr gigs + apply to affiliate programs")
    print("  Week 3: POD launch + directory submissions + first Substack posts")
    print("  Week 4: Optimize what's converting. Kill what's not. Double down on winners.")
    print()
    print("  Conservative estimate: $1,000-3,000/mo within 60 days")
    print("  Aggressive estimate: $3,000-8,000/mo within 60 days (if all P0+P1 execute)")


def output_audit(ops: List[Opportunity]):
    """Audit current operational status."""
    print_header("OPERATIONAL AUDIT - CURRENT STATE OF ALL REVENUE LANES")

    status_counts = defaultdict(int)
    for op in ops:
        status_counts[op.status] += 1

    print("  STATUS BREAKDOWN:")
    for status, count in sorted(status_counts.items()):
        print(f"    {status}: {count}")
    print()

    # Check key infrastructure files
    print("  INFRASTRUCTURE CHECK:")
    checks = [
        ("Gumroad Products", PRODUCTS / "GUMROAD_READY_LISTINGS.md"),
        ("Whop Listings", PRODUCTS / "listings" / "WHOP_LISTING_1.md"),
        ("Cold Email Sequences", MONEY_METHODS / "COLD_OUTBOUND" / "EMAIL_SEQUENCES_TIER1.md"),
        ("Auto Clip Pipeline", AUTOMATIONS / "auto_clip_pipeline.py"),
        ("Local Biz Pipeline", AUTOMATIONS / "local_biz_pipeline.py"),
        ("Ecom Arb Scanner", AUTOMATIONS / "ecom_arb_scanner.py"),
        ("Content Calendar", LEDGER / "CONTENT_CALENDAR_30DAY.csv"),
        ("Buffer CSVs", LEDGER / "buffer_import_faith_twitter.csv"),
        ("PrayerLock PWA", APP_FACTORY / "builds" / "prayerlock-web" / "index.html"),
        ("biomaxx App", APP_FACTORY / "builds" / "biomaxx-sdk54"),
        ("Revenue Tracker", FINANCIALS / "REVENUE_TRACKER.csv"),
        ("Products CSV", LEDGER / "PRODUCTS.csv"),
        ("Medium Articles", CONTENT / "medium_articles" / "MEDIUM_BATCH_10.md"),
        ("Newsletter Sequences", MONEY_METHODS / "NEWSLETTER" / "WELCOME_SEQUENCE_FAITH.md"),
        ("POD Trending", MONEY_METHODS / "POD" / "TRENDING_OPPORTUNITIES.csv"),
        ("Service Packages", OPS / "SERVICE_OFFERING_PACKAGES.md"),
        ("Launch Directories", LEDGER / "LAUNCH_DIRECTORIES.csv"),
    ]

    found = 0
    missing = 0
    for name, path in checks:
        exists = file_exists(path) if path.suffix else dir_exists(path)
        icon = "FOUND" if exists else "MISSING"
        if exists:
            found += 1
        else:
            missing += 1
        print(f"    [{icon}] {name}: {path.relative_to(PROJECT_ROOT)}")

    print(f"\n  Score: {found}/{found + missing} infrastructure files present ({found * 100 // (found + missing)}%)")
    print()

    # Detailed audit per category
    by_category = defaultdict(list)
    for op in ops:
        by_category[op.category].append(op)

    for cat in CATEGORIES:
        if cat not in by_category:
            continue
        cat_ops = by_category[cat]
        ready_count = sum(1 for o in cat_ops if o.status == READY_TO_LAUNCH)
        active_count = sum(1 for o in cat_ops if o.status == ACTIVE)

        status_icon = "OK" if active_count > 0 else ("READY" if ready_count > 0 else "TODO")
        print(f"  [{status_icon}] {cat.upper().replace('_', ' ')}")
        for op in cat_ops:
            icon = {
                ACTIVE: "LIVE",
                READY_TO_LAUNCH: "READY",
                IN_PROGRESS: "WIP",
                NOT_STARTED: "----",
                BLOCKED: "BLOCK",
            }.get(op.status, "????")
            print(f"    [{icon}] {op.name} ({op.est_revenue_range})")
            if op.blockers:
                for b in op.blockers:
                    print(f"           BLOCKER: {b}")
        print()


def output_blockers(ops: List[Opportunity]):
    """Show only blocking items."""
    print_header("BLOCKERS - ITEMS PREVENTING REVENUE")

    blocked = [o for o in ops if o.is_blocked]
    if not blocked:
        print("  No blockers found. All clear to launch.")
        return

    # Deduplicate blockers
    all_blockers = defaultdict(list)
    for op in blocked:
        for b in op.blockers:
            all_blockers[b].append(op.name)

    print(f"  {len(all_blockers)} unique blockers affecting {len(blocked)} opportunities:")
    print()

    # Sort by impact (number of ops affected)
    for blocker, affected_ops in sorted(all_blockers.items(), key=lambda x: -len(x[1])):
        print(f"  BLOCKER: {blocker}")
        print(f"  Affects: {', '.join(affected_ops)}")
        print(f"  Impact: {len(affected_ops)} opportunit{'y' if len(affected_ops) == 1 else 'ies'} blocked")
        print()


def output_critical_path(ops: List[Opportunity]):
    """Show critical path to first $1K/mo."""
    print_header("CRITICAL PATH TO $1,000/MONTH")

    p0_ops = [o for o in ops if o.priority == P0]
    p1_fast = [o for o in ops if o.priority == P1 and any(x in o.time_to_first_dollar for x in ["1-7", "3-7", "3-14", "7-14", "7-21", "7-30"])]

    print("  PHASE 1: IMMEDIATE LAUNCHES (Day 1-3)")
    print("  " + "-" * 50)
    total = 0
    for op in p0_ops:
        print(f"  -> {op.name} ({op.est_revenue_range})")
        print(f"     ACTION: {op.next_action[:120]}")
        total += op.est_revenue_high
    print(f"\n  Phase 1 potential: up to ${total:,}/mo")
    print()

    print("  PHASE 2: QUICK WINS (Day 4-14)")
    print("  " + "-" * 50)
    p2_total = 0
    for op in p1_fast[:8]:
        print(f"  -> {op.name} ({op.est_revenue_range})")
        print(f"     ACTION: {op.next_action[:120]}")
        p2_total += op.est_revenue_high
    print(f"\n  Phase 2 additional: up to ${p2_total:,}/mo")
    print()

    print("  PHASE 3: COMPOUND (Day 15-30)")
    print("  " + "-" * 50)
    print("  -> Optimize Phase 1+2 winners")
    print("  -> Launch remaining P1 opportunities")
    print("  -> Start P2 opportunities that show promise")
    print("  -> Write 2x Medium articles per week (SEO compounding)")
    print("  -> Build Notion templates (passive income layer)")
    print("  -> Apply to 10+ affiliate programs (stacks with content)")
    print()

    running_total = total + p2_total
    print_divider("-")
    print(f"  30-DAY TARGET: ${running_total // 3:,}-${running_total:,}/mo")
    print(f"  60-DAY TARGET: ${running_total // 2:,}-${int(running_total * 1.5):,}/mo (compounding)")
    print()
    print("  KEY INSIGHT: $1K/mo is crossed by stacking 5-10 small streams,")
    print("  not hitting one big winner.")
    print()
    print("  EXAMPLE STACK:")
    print("    $200/mo Gumroad products (10 listed, organic sales)")
    print("    $300/mo Fiverr services (2-3 clients at $100-150 each)")
    print("    $200/mo Affiliate commissions (Medium articles + referral links)")
    print("    $150/mo Medium Partner Program (5-10 articles ranking)")
    print("    $100/mo POD sales (Etsy + Printful)")
    print("    $100/mo Cold email clients (1 small client per month)")
    print("    ----")
    print("    $1,050/mo total from 6 revenue streams")
    print()
    print("  None of these require social media followers or ad spend.")
    print("  All leverage existing assets already built in this project.")


def output_integrate_json(ops: List[Opportunity]):
    """Output JSON for quant terminal integration."""
    data = {
        "scan_date": TODAY,
        "scanner_version": "2.0.0",
        "total_opportunities": len(ops),
        "p0_count": sum(1 for o in ops if o.priority == P0),
        "p1_count": sum(1 for o in ops if o.priority == P1),
        "p2_count": sum(1 for o in ops if o.priority == P2),
        "p3_count": sum(1 for o in ops if o.priority == P3),
        "ready_to_launch": sum(1 for o in ops if o.status == READY_TO_LAUNCH),
        "active": sum(1 for o in ops if o.status == ACTIVE),
        "blocked_count": sum(1 for o in ops if o.is_blocked),
        "total_revenue_low": sum(o.est_revenue_low for o in ops),
        "total_revenue_high": sum(o.est_revenue_high for o in ops),
        "p0_revenue_high": sum(o.est_revenue_high for o in ops if o.priority == P0),
        "categories": {},
        "opportunities": [o.to_dict() for o in ops],
    }

    by_category = defaultdict(list)
    for op in ops:
        by_category[op.category].append(op)

    for cat, cat_ops in by_category.items():
        data["categories"][cat] = {
            "count": len(cat_ops),
            "revenue_low": sum(o.est_revenue_low for o in cat_ops),
            "revenue_high": sum(o.est_revenue_high for o in cat_ops),
            "ready_to_launch": sum(1 for o in cat_ops if o.status == READY_TO_LAUNCH),
        }

    print(json.dumps(data, indent=2))


# ---------------------------------------------------------------------------
# FILE OUTPUT
# ---------------------------------------------------------------------------

def write_csv_output(ops: List[Opportunity]) -> Path:
    """Write scan results to CSV in LEDGER/RBI_AUDITS/."""
    RBI_AUDITS.mkdir(parents=True, exist_ok=True)
    csv_path = RBI_AUDITS / f"rbi_scan_{TODAY}.csv"

    fieldnames = [
        "category", "name", "description", "est_revenue_low", "est_revenue_high",
        "est_revenue_range", "startup_cost", "time_to_first_dollar",
        "existing_assets", "next_action", "priority", "status",
        "blockers", "notes", "scan_date",
    ]

    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for op in ops:
            writer.writerow(op.to_csv_row())

    print(f"  CSV written: {csv_path}")
    return csv_path


def write_summary_output(ops: List[Opportunity]) -> Path:
    """Write human-readable summary to LEDGER/RBI_AUDITS/."""
    RBI_AUDITS.mkdir(parents=True, exist_ok=True)
    md_path = RBI_AUDITS / f"rbi_summary_{TODAY}.md"

    total_low = sum(o.est_revenue_low for o in ops)
    total_high = sum(o.est_revenue_high for o in ops)
    p0_ops = [o for o in ops if o.priority == P0]
    ready_ops = [o for o in ops if o.status == READY_TO_LAUNCH]

    lines = []
    lines.append(f"# RBI Scan Summary - {TODAY}")
    lines.append("")
    lines.append(f"**Total Opportunities:** {len(ops)}")
    lines.append(f"**Revenue Potential:** ${total_low:,}-${total_high:,}/mo")
    lines.append(f"**Ready to Launch:** {len(ready_ops)}")
    lines.append(f"**P0 (Do Today):** {len(p0_ops)}")
    lines.append("")
    lines.append("---")
    lines.append("")

    # P0 section
    if p0_ops:
        lines.append("## P0 - DO TODAY")
        lines.append("")
        for op in p0_ops:
            lines.append(f"### {op.name}")
            lines.append(f"- **Revenue:** {op.est_revenue_range}")
            lines.append(f"- **Time to first dollar:** {op.time_to_first_dollar}")
            lines.append(f"- **Next action:** {op.next_action}")
            if op.existing_assets:
                lines.append(f"- **Existing assets:** {', '.join(op.existing_assets[:3])}")
            if op.blockers:
                lines.append(f"- **Blockers:** {', '.join(op.blockers)}")
            lines.append("")

    # Ready to launch section
    non_p0_ready = [o for o in ready_ops if o not in p0_ops]
    if non_p0_ready:
        lines.append("## READY TO LAUNCH (Non-P0)")
        lines.append("")
        for op in non_p0_ready:
            lines.append(f"- **{op.name}** ({op.est_revenue_range}) - {op.next_action[:100]}")
        lines.append("")

    # All opportunities table
    lines.append("## All Opportunities")
    lines.append("")
    lines.append("| Priority | Name | Revenue | Status | Time |")
    lines.append("|----------|------|---------|--------|------|")
    for op in ops:
        lines.append(f"| {op.priority} | {op.name} | {op.est_revenue_range} | {op.status} | {op.time_to_first_dollar} |")
    lines.append("")

    # Blockers summary
    blocked = [o for o in ops if o.is_blocked]
    if blocked:
        all_blockers = set()
        for op in blocked:
            all_blockers.update(op.blockers)
        lines.append("## Blockers")
        lines.append("")
        for b in sorted(all_blockers):
            lines.append(f"- {b}")
        lines.append("")

    with open(md_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"  Summary written: {md_path}")
    return md_path


# ---------------------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="PRINTMAXX Daily No-Cost RBI Scanner - "
                    "Scans all zero-cost revenue opportunities across 17 categories",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent("""\
            Categories:
                marketplace, affiliate, freelance, clipping, dropship,
                domain, ai_music, directory, free_tool_arb, plr_mrr,
                template, community, cold_email, content_syndication,
                referral, repo, data_leads

            Examples:
                python3 daily_nocost_rbi_scanner.py --scan
                python3 daily_nocost_rbi_scanner.py --category affiliate
                python3 daily_nocost_rbi_scanner.py --next-actions
                python3 daily_nocost_rbi_scanner.py --critical-path
                python3 daily_nocost_rbi_scanner.py --integrate > rbi.json
        """),
    )

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--scan", action="store_true",
                       help="Full daily scan across all 17 categories")
    group.add_argument("--category", type=str, metavar="NAME",
                       help=f"Scan one category: {', '.join(CATEGORIES)}")
    group.add_argument("--audit", action="store_true",
                       help="Audit current operational status of all lanes")
    group.add_argument("--opportunities", action="store_true",
                       help="List all actionable opportunities")
    group.add_argument("--revenue-map", action="store_true",
                       help="Revenue projections by timeframe")
    group.add_argument("--next-actions", action="store_true",
                       help="Top 10 things to do RIGHT NOW")
    group.add_argument("--integrate", action="store_true",
                       help="Output JSON for quant terminal integration")
    group.add_argument("--blockers", action="store_true",
                       help="Show blocking items only")
    group.add_argument("--critical-path", action="store_true",
                       help="Critical path to first $1K/mo")

    args = parser.parse_args()

    # Run scanners based on mode
    if args.category:
        ops = run_category_scanner(args.category)
    else:
        ops = run_all_scanners()

    # Output based on mode
    if args.scan:
        output_scan_results(ops)
        print()
        csv_path = write_csv_output(ops)
        md_path = write_summary_output(ops)
        print()
        print(f"  Scan complete. {len(ops)} opportunities identified.")
        print(f"  CSV: {csv_path}")
        print(f"  Summary: {md_path}")
    elif args.category:
        output_scan_results(ops)
    elif args.audit:
        output_audit(ops)
    elif args.opportunities:
        output_scan_results(ops)
    elif args.revenue_map:
        output_revenue_map(ops)
    elif args.next_actions:
        output_next_actions(ops)
    elif args.integrate:
        output_integrate_json(ops)
    elif args.blockers:
        output_blockers(ops)
    elif args.critical_path:
        output_critical_path(ops)


if __name__ == "__main__":
    main()
