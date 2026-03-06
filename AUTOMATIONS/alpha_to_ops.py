#!/usr/bin/env python3
"""
alpha_to_ops.py — Closes the gap between approved alpha and actual execution.

Reads APPROVED alpha from ALPHA_STAGING.csv and AUTO-GENERATES actionable ops:
  - App specs, cold email templates, content drafts, tool evals,
    growth playbooks, listing specs, monetization plans, service listings,
    AI integration specs.

Each output is tracked in AUTO_OPS_TRACKER.csv. Processed alpha entries get
flagged ops_generated=TRUE so they're never re-processed.

Usage:
    python3 AUTOMATIONS/alpha_to_ops.py --process        # process all unprocessed
    python3 AUTOMATIONS/alpha_to_ops.py --process-id ALPHA248
    python3 AUTOMATIONS/alpha_to_ops.py --status          # summary dashboard
    python3 AUTOMATIONS/alpha_to_ops.py --cron            # skip if already ran today
    python3 AUTOMATIONS/alpha_to_ops.py --dry-run         # preview without writing
    python3 AUTOMATIONS/alpha_to_ops.py --deploy          # mark ops READY_TO_DEPLOY
"""

import argparse
import csv
import datetime
import fcntl
import hashlib
import os
import re
import sys
import textwrap
import time

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ALPHA_CSV = os.path.join(PROJECT_ROOT, "LEDGER", "ALPHA_STAGING.csv")
TRACKER_CSV = os.path.join(PROJECT_ROOT, "LEDGER", "AUTO_OPS_TRACKER.csv")
AUTO_OPS_DIR = os.path.join(PROJECT_ROOT, "AUTOMATIONS", "auto_ops")
LOCK_FILE = os.path.join(AUTO_OPS_DIR, ".alpha_to_ops.lock")
CRON_MARKER = os.path.join(AUTO_OPS_DIR, ".last_cron_run")

SUBDIRS = {
    "APP_FACTORY": "app_specs",
    "OUTBOUND": "email_templates",
    "CONTENT_FORMAT": "content",
    "CONTENT_FARM": "content",
    "TOOL_ALPHA": "tool_evals",
    "GROWTH_HACK": "playbooks",
    "ECOM": "listings",
    "ECOM_ARB": "listings",
    "MONETIZATION": "monetization",
    "FREELANCE": "freelance",
    "AI_ALPHA": "ai_tools",
    "AI_INFLUENCER": "ai_tools",
    "SEO_GEO_ASO": "playbooks",
    "PLATFORM_META": "playbooks",
    "GENERAL": "playbooks",
}

TRACKER_FIELDS = [
    "alpha_id", "category", "ops_type", "output_file",
    "created_at", "status", "priority", "notes",
]

# Known clean categories we can process
VALID_CATEGORIES = set(SUBDIRS.keys())

# ---------------------------------------------------------------------------
# Utility helpers
# ---------------------------------------------------------------------------

def safe_path(path: str) -> str:
    """Ensure path stays within PROJECT_ROOT. Raise on escape attempt."""
    resolved = os.path.realpath(path)
    if not resolved.startswith(os.path.realpath(PROJECT_ROOT)):
        raise ValueError(f"path escape blocked: {path}")
    return resolved


def ensure_dirs():
    """Create all output subdirectories."""
    os.makedirs(AUTO_OPS_DIR, exist_ok=True)
    for subdir in set(SUBDIRS.values()):
        os.makedirs(safe_path(os.path.join(AUTO_OPS_DIR, subdir)), exist_ok=True)


def now_iso() -> str:
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def today_str() -> str:
    return datetime.datetime.now().strftime("%Y-%m-%d")


def priority_from_roi(roi: str) -> str:
    roi = (roi or "").strip().upper()
    if roi in ("HIGHEST",):
        return "HIGH"
    if roi in ("HIGH",):
        return "HIGH"
    if roi in ("MEDIUM",):
        return "MEDIUM"
    return "LOW"


def truncate(text: str, maxlen: int = 120) -> str:
    text = (text or "").strip()
    if len(text) <= maxlen:
        return text
    return text[: maxlen - 3] + "..."


def slug(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", text.lower()).strip("_")[:60]


def clean_for_voice(text: str) -> str:
    """Strip AI slop vocabulary and em dashes from text."""
    replacements = {
        "—": ". ",
        "–": ". ",
        "leverage": "use",
        "Leverage": "Use",
        "utilize": "use",
        "Utilize": "Use",
        "comprehensive": "",
        "Comprehensive": "",
        "innovative": "",
        "Innovative": "",
        "robust": "solid",
        "Robust": "Solid",
        "seamless": "smooth",
        "Seamless": "Smooth",
        "game-changer": "big deal",
        "cutting-edge": "new",
        "revolutionary": "",
        "Revolutionary": "",
        "delve": "look at",
        "Delve": "Look at",
        "empower": "help",
        "Empower": "Help",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    # collapse double spaces
    text = re.sub(r"  +", " ", text)
    return text.strip()


# ---------------------------------------------------------------------------
# Lock helpers
# ---------------------------------------------------------------------------

class FileLock:
    """Simple file-based lock to prevent concurrent runs."""

    def __init__(self, path: str):
        self.path = safe_path(path)
        self._fd = None

    def __enter__(self):
        self._fd = open(self.path, "w")
        try:
            fcntl.flock(self._fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except (IOError, OSError):
            self._fd.close()
            print("ERROR: another alpha_to_ops process is running. exiting.")
            sys.exit(1)
        self._fd.write(str(os.getpid()))
        self._fd.flush()
        return self

    def __exit__(self, *_):
        if self._fd:
            fcntl.flock(self._fd, fcntl.LOCK_UN)
            self._fd.close()
        try:
            os.remove(self.path)
        except OSError:
            pass


# ---------------------------------------------------------------------------
# CSV I/O
# ---------------------------------------------------------------------------

def read_alpha_csv() -> list[dict]:
    """Read ALPHA_STAGING.csv, return list of row dicts."""
    if not os.path.exists(ALPHA_CSV):
        print(f"ERROR: {ALPHA_CSV} not found")
        sys.exit(1)
    rows = []
    with open(ALPHA_CSV, "r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)
    return rows


def read_tracker() -> list[dict]:
    """Read AUTO_OPS_TRACKER.csv. Return empty list if missing."""
    if not os.path.exists(TRACKER_CSV):
        return []
    with open(TRACKER_CSV, "r", newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def get_processed_ids() -> set[str]:
    """Return set of alpha_ids already in the tracker."""
    return {row["alpha_id"] for row in read_tracker() if row.get("alpha_id")}


def append_tracker_row(row: dict):
    """Append a single row to AUTO_OPS_TRACKER.csv, creating headers if needed."""
    exists = os.path.exists(TRACKER_CSV)
    with open(safe_path(TRACKER_CSV), "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=TRACKER_FIELDS)
        if not exists:
            writer.writeheader()
        writer.writerow(row)


def write_alpha_csv(rows: list[dict], fieldnames: list[str]):
    """Rewrite ALPHA_STAGING.csv with updated rows (adds ops_generated col)."""
    if "ops_generated" not in fieldnames:
        fieldnames = list(fieldnames) + ["ops_generated"]
    with open(safe_path(ALPHA_CSV), "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def init_tracker_if_missing():
    """Create tracker CSV with headers if it doesn't exist."""
    if not os.path.exists(TRACKER_CSV):
        with open(safe_path(TRACKER_CSV), "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=TRACKER_FIELDS)
            writer.writeheader()


# ---------------------------------------------------------------------------
# Content generators — one per category
# ---------------------------------------------------------------------------

def _extract_insight(alpha: dict) -> str:
    """Pull the best text snippet from the alpha row."""
    candidates = [
        alpha.get("extracted_method", ""),
        alpha.get("tactic", ""),
        alpha.get("reviewer_notes", ""),
    ]
    for c in candidates:
        if c and len(c.strip()) > 10:
            return clean_for_voice(c.strip())
    return clean_for_voice(
        alpha.get("reviewer_notes", "") or alpha.get("source", "unknown alpha")
    )


def gen_app_factory(alpha: dict) -> str:
    insight = _extract_insight(alpha)
    aid = alpha["alpha_id"]
    source = alpha.get("source", "")
    roi = alpha.get("roi_potential", "MEDIUM")
    niches = alpha.get("applicable_niches", "") or "faith, fitness, tech, finance"
    return clean_for_voice(f"""# App Spec: {aid}
## source: {source}
## generated: {now_iso()}
## roi_potential: {roi}

## core insight
{insight}

## app concept
build a focused utility app around this insight. single-purpose, solves one problem well.

### target niches
{niches}

### suggested name direction
- insider baseball naming. something someone in the niche would say.
- no generic "AI Helper Pro" slop. research actual top apps in the category.
- 1-2 words max. lowercase energy.

### monetization model
- freemium with 7-day trial
- $4.99/mo or $29.99/yr subscription via RevenueCat
- affiliate links to relevant physical products (supplements, books, gear)
- apple now allows external payment links. use them.

### ASO keywords (research and expand)
- extract 5-10 keywords from the insight
- check App Store search volume before committing
- long-tail beats head terms for new apps

### competitor notes
- find top 3 apps in this space
- what are they missing? what do 1-star reviews complain about?
- that gap is the product.

### implementation
- PWA first (ships fastest), wrap with Capacitor for iOS
- use aggregate design system v2 (MONEY_METHODS/APP_FACTORY/AGGREGATE_DESIGN_SYSTEM_V2.md)
- 4-screen onboarding minimum
- lighthouse score > 90 before submission

### next action
build MVP in one session. test in simulator. deploy to surge.sh. wrap for iOS.
""")


def gen_outbound(alpha: dict) -> str:
    insight = _extract_insight(alpha)
    aid = alpha["alpha_id"]
    source = alpha.get("source", "")
    roi = alpha.get("roi_potential", "MEDIUM")
    return clean_for_voice(f"""# Cold Email Template: {aid}
## source: {source}
## generated: {now_iso()}
## roi_potential: {roi}

## key insight
{insight}

## target industry
- identify the industry this alpha applies to best
- local businesses, SaaS companies, agencies, or ecom brands

---

## email 1: the opener (send day 1)

subject: quick question about [their specific pain point]

hey [first name],

noticed [specific observation about their business from website scoring].

{truncate(insight, 200)}

built a quick demo showing what this looks like for [industry]: [surge.sh demo URL]

worth a look?

[your name]

---

## email 2: the value add (send day 3)

subject: re: quick question about [pain point]

hey [first name],

one more thing. ran the numbers on businesses like yours.

[insert specific metric from this alpha]. most [industry] businesses leave this on the table.

the demo is still live: [demo URL]

takes 2 minutes to see what I mean.

[your name]

---

## email 3: the break-up (send day 7)

subject: closing the loop

[first name],

not trying to clog your inbox. if [pain point] isn't a priority right now, no worries.

deleting your file on Friday. if you want the demo link before then: [demo URL]

cheers,
[your name]

---

## implementation notes
- use subdomain for cold email. protect main domain.
- warmup 14-21 days before sending (2026 requirement per ALPHA282)
- 4-6 lines per email (per ALPHA286)
- no tracking pixels (per ALPHA276, Gmail warns users)
- casual tone beats polished (per ALPHA281)
- first email matters most: 58% of replies come from email 1 (per ALPHA278)
""")


def gen_content_format(alpha: dict) -> str:
    insight = _extract_insight(alpha)
    aid = alpha["alpha_id"]
    source = alpha.get("source", "")
    roi = alpha.get("roi_potential", "MEDIUM")
    return clean_for_voice(f"""# Content Pack: {aid}
## source: {source}
## generated: {now_iso()}
## roi_potential: {roi}

## core insight
{insight}

---

## tweet 1: the hook
{truncate(insight, 240)}

this changes how you think about content distribution.

## tweet 2: the proof
specific numbers from testing this:
- [insert metric from alpha]
- [insert comparison]
- most people don't know this yet.

## tweet 3: the action
here's exactly how to do it:
1. [step from insight]
2. [second step]
3. [third step]

took me 30 minutes to set up. saves hours every week.

---

## thread: full breakdown (5-7 tweets)

1/ {truncate(insight, 200)}

here's the full breakdown of what's working right now.

2/ the old way: [what most people do]
the new way: [what this alpha reveals]
the difference: [specific metric]

3/ step 1: [actionable step]
this is where most people stop. don't stop.

4/ step 2: [next step]
key detail most guides skip: [specific detail from alpha]

5/ step 3: [final step]
the results: [expected outcome]

6/ why this works now and didn't work 6 months ago:
[platform change / market shift that created this window]

7/ tldr:
- [step 1]
- [step 2]
- [step 3]
start today. the window won't last forever.

---

## niche variants

### faith niche (@prayerlock)
adapt the insight for faith/spiritual community. focus on discipline, consistency, daily practice.

### fitness niche (@walktounlock)
adapt for fitness/health audience. numbers, tracking, accountability angle.

### tech niche (@PRINTMAXXER)
the building-in-public angle. how we implemented this, real results.

### finance niche
adapt for money/investing audience. ROI framing, specific dollar amounts.

---

## posting schedule
- tweet 1: Monday 8am EST (highest engagement window)
- tweet 2: Tuesday 12pm EST
- tweet 3: Wednesday 6pm EST
- thread: Thursday 9am EST
- cross-post to Reddit on Friday (r/SideProject or r/indiehackers)
""")


def gen_tool_eval(alpha: dict) -> str:
    insight = _extract_insight(alpha)
    aid = alpha["alpha_id"]
    source = alpha.get("source", "")
    source_url = alpha.get("source_url", "")
    roi = alpha.get("roi_potential", "MEDIUM")
    return clean_for_voice(f"""# Tool Evaluation: {aid}
## source: {source}
## url: {source_url}
## generated: {now_iso()}
## roi_potential: {roi}

## what it is
{insight}

## pricing
- [ ] free tier available?
- [ ] free tier limits?
- [ ] paid tier starting price?
- [ ] annual discount?
- research actual pricing at: {source_url}

## use case for PRINTMAXX
- how does this fit our stack?
- what does it replace or augment?
- which money methods benefit most?

## integration points
1. quant terminal integration (AUTOMATIONS/printmaxx_quant_terminal.py)
2. ralph loop automation (can this be automated overnight?)
3. content pipeline (does this help generate or distribute content?)
4. lead gen (does this help find or qualify leads?)
5. app factory (does this help build or ship apps faster?)

## ROI estimate
- time saved per week: [estimate]
- cost per month: [from pricing research]
- breakeven: [time saved value > cost]
- at our current stage ($0 revenue), only adopt if free tier covers our needs

## verdict
- [ ] ADOPT NOW (free tier, immediate ROI)
- [ ] ADOPT LATER (need revenue first)
- [ ] MONITOR (not ready yet, check back in 30 days)
- [ ] SKIP (doesn't fit our stack)

## next action
sign up for free tier and test for 1 week. log results.
""")


def gen_growth_hack(alpha: dict) -> str:
    insight = _extract_insight(alpha)
    aid = alpha["alpha_id"]
    source = alpha.get("source", "")
    roi = alpha.get("roi_potential", "MEDIUM")
    return clean_for_voice(f"""# Growth Playbook: {aid}
## source: {source}
## generated: {now_iso()}
## roi_potential: {roi}

## tactic summary
{insight}

## implementation steps

### step 1: setup (day 1, ~30 min)
- what tools/accounts needed
- what content/assets to prepare
- what automation to configure

### step 2: first test (day 1-2)
- run smallest possible version
- measure: [specific metric to track]
- success threshold: [number]

### step 3: evaluate (day 3)
- did it hit the threshold?
- what broke? what surprised you?
- adjust approach based on data

### step 4: scale or kill (day 4-7)
- above threshold: double down. increase volume 2x.
- below threshold: try one variation. if still below, kill it.
- never spend more than 7 days on an unvalidated tactic.

## estimated timeline
- setup: 30 minutes
- first results: 24-48 hours
- meaningful data: 5-7 days
- decision to scale or kill: day 7

## required tools
- list specific tools from the insight
- check if we already have them (OPS/FREE_TIER_SETUP_GUIDE.md)
- free tier only until this tactic is validated

## risk level
- LOW: no account risk, no money required
- MEDIUM: small account risk or small spend ($10-50)
- HIGH: significant account risk or significant spend ($50+)
- assess based on the specific tactic

## connection to other ops
- which money methods does this amplify?
- which content niches benefit most?
- cross-reference LEDGER/CROSS_POLLINATION_MATRIX.csv

## next action
execute step 1 today. no planning beyond that until you have data.
""")


def gen_ecom(alpha: dict) -> str:
    insight = _extract_insight(alpha)
    aid = alpha["alpha_id"]
    source = alpha.get("source", "")
    roi = alpha.get("roi_potential", "MEDIUM")
    return clean_for_voice(f"""# Listing Spec: {aid}
## source: {source}
## generated: {now_iso()}
## roi_potential: {roi}

## product insight
{insight}

## product idea
- what physical or digital product does this alpha suggest?
- is it POD, digital download, template, or sourced product?

## platform selection
- [ ] Gumroad (digital products, highest margin)
- [ ] Etsy (templates, printables, POD)
- [ ] Redbubble (POD designs)
- [ ] Amazon KDP (journals, planners)
- pick the platform with lowest friction for this product type

## pricing
- research competing products on chosen platform
- price at market rate or slightly below for first 30 days
- raise price after getting 5+ reviews

## listing copy (ready to paste)

### title
[product name] - [primary benefit] | [secondary benefit]

### description
{truncate(insight, 300)}

what you get:
- [deliverable 1]
- [deliverable 2]
- [deliverable 3]

instant download. no fluff. just the stuff that works.

### tags
- extract 13 tags from the insight (Etsy allows 13)
- mix broad and long-tail
- research actual search volume on the platform

## margin analysis
- production cost: $[X]
- platform fee: [percentage]
- selling price: $[X]
- profit per unit: $[X]
- breakeven units: [X]

## next action
create the product asset. list it today. first sale > perfection.
""")


def gen_monetization(alpha: dict) -> str:
    insight = _extract_insight(alpha)
    aid = alpha["alpha_id"]
    source = alpha.get("source", "")
    roi = alpha.get("roi_potential", "MEDIUM")
    return clean_for_voice(f"""# Monetization Plan: {aid}
## source: {source}
## generated: {now_iso()}
## roi_potential: {roi}

## core insight
{insight}

## monetization model
based on this alpha, the revenue path is:

### primary revenue
- what's the direct way to make money from this?
- pricing: $[X] per [unit/month/project]
- estimated monthly potential: $[X]-$[X]

### secondary revenue (stacking)
- what adjacent revenue can this generate?
- affiliate links to tools mentioned
- upsell to done-for-you service
- content from the process (building-in-public)

### funnel position
where does this fit in the PRINTMAXX funnel?
- top of funnel (free content that drives signups)
- middle of funnel (low-ticket product $5-$50)
- bottom of funnel (high-ticket service $500-$3000)
- recurring (subscription or retainer)

## implementation priority
- is this a "this week" or "this month" opportunity?
- what's blocking it? (accounts, assets, content?)
- minimum viable version that generates first dollar?

## tracking
- log revenue in FINANCIALS/REVENUE_TRACKER.csv
- log expenses in FINANCIALS/EXPENSE_TRACKER.csv
- track conversion in LEDGER/FUNNEL_METRICS.csv

## next action
identify the fastest path to first dollar from this insight. execute today.
""")


def gen_freelance(alpha: dict) -> str:
    insight = _extract_insight(alpha)
    aid = alpha["alpha_id"]
    source = alpha.get("source", "")
    roi = alpha.get("roi_potential", "MEDIUM")
    return clean_for_voice(f"""# Freelance Service Listing: {aid}
## source: {source}
## generated: {now_iso()}
## roi_potential: {roi}

## service insight
{insight}

---

## fiverr gig (ready to paste)

### title
I will [specific deliverable based on this alpha insight]

### category
select the most relevant Fiverr category

### description
{truncate(insight, 300)}

what you get:
- [deliverable 1 with specific quantity]
- [deliverable 2]
- [deliverable 3]
- delivery in [X] days

i've tested this approach and it works. no fluff, no filler. just results.

### pricing tiers
- BASIC ($50): [minimal deliverable]
- STANDARD ($150): [full deliverable]
- PREMIUM ($300): [full deliverable + strategy + implementation]

### FAQs
1. how long does this take? [X] business days.
2. do you need access to my accounts? only [specific access needed].
3. what if I'm not happy? unlimited revisions until you are.

---

## upwork proposal template

### title
[Service] specialist. [specific result] in [timeframe].

### overview
{truncate(insight, 200)}

i've built systems around this exact approach. here's what I can do for you:
- [deliverable 1]
- [deliverable 2]
- [deliverable 3]

### rate
$[X]/hour or $[X] fixed for [scope]

---

## next action
list on Fiverr today. apply to 5 relevant Upwork jobs this week.
""")


def gen_ai_tool(alpha: dict) -> str:
    insight = _extract_insight(alpha)
    aid = alpha["alpha_id"]
    source = alpha.get("source", "")
    source_url = alpha.get("source_url", "")
    roi = alpha.get("roi_potential", "MEDIUM")
    return clean_for_voice(f"""# AI Tool Integration: {aid}
## source: {source}
## url: {source_url}
## generated: {now_iso()}
## roi_potential: {roi}

## what it does
{insight}

## integration spec

### current stack gaps this fills
- what problem in our pipeline does this solve?
- what manual process does this automate?
- estimated time savings per week

### implementation plan
1. sign up / install / configure
2. test with small batch (10 items max)
3. compare output quality to manual process
4. if quality >= 80% of manual: automate fully
5. if quality < 80%: use as assist, not replacement

### automation potential
- can this run in a ralph loop? (overnight, unattended)
- can this feed into the quant terminal?
- can this connect to existing cron jobs?
- does it have an API? CLI? Python SDK?

### cost analysis
- free tier covers our current volume: YES / NO
- paid tier cost: $[X]/mo
- breakeven: [X] hours saved * $[hourly value] > cost

### risk assessment
- data privacy: does our data leave our machine?
- vendor lock-in: can we switch tools easily?
- reliability: what happens if this tool goes down?

## next action
test with 5 real inputs from our pipeline. measure quality and speed. decide in 48 hours.
""")


# Map categories to generators
GENERATORS = {
    "APP_FACTORY": gen_app_factory,
    "OUTBOUND": gen_outbound,
    "CONTENT_FORMAT": gen_content_format,
    "CONTENT_FARM": gen_content_format,  # same generator, content-focused
    "TOOL_ALPHA": gen_tool_eval,
    "GROWTH_HACK": gen_growth_hack,
    "ECOM": gen_ecom,
    "ECOM_ARB": gen_ecom,
    "MONETIZATION": gen_monetization,
    "FREELANCE": gen_freelance,
    "AI_ALPHA": gen_ai_tool,
    "AI_INFLUENCER": gen_ai_tool,
    "SEO_GEO_ASO": gen_growth_hack,    # SEO tactics use growth playbook format
    "PLATFORM_META": gen_growth_hack,   # platform intel uses growth playbook format
    "GENERAL": gen_growth_hack,         # general alpha uses growth playbook format
}

# Ops type labels for tracker
OPS_TYPES = {
    "APP_FACTORY": "app_spec",
    "OUTBOUND": "email_template",
    "CONTENT_FORMAT": "content_pack",
    "CONTENT_FARM": "content_pack",
    "TOOL_ALPHA": "tool_eval",
    "GROWTH_HACK": "growth_playbook",
    "ECOM": "listing_spec",
    "ECOM_ARB": "listing_spec",
    "MONETIZATION": "monetization_plan",
    "FREELANCE": "service_listing",
    "AI_ALPHA": "ai_integration",
    "AI_INFLUENCER": "ai_integration",
    "SEO_GEO_ASO": "growth_playbook",
    "PLATFORM_META": "growth_playbook",
    "GENERAL": "growth_playbook",
}

# File prefixes per category
FILE_PREFIXES = {
    "APP_FACTORY": "APP_SPEC",
    "OUTBOUND": "EMAIL",
    "CONTENT_FORMAT": "CONTENT",
    "CONTENT_FARM": "CONTENT",
    "TOOL_ALPHA": "TOOL",
    "GROWTH_HACK": "PLAYBOOK",
    "ECOM": "LISTING",
    "ECOM_ARB": "LISTING",
    "MONETIZATION": "PLAN",
    "FREELANCE": "SERVICE",
    "AI_ALPHA": "AI",
    "AI_INFLUENCER": "AI",
    "SEO_GEO_ASO": "PLAYBOOK",
    "PLATFORM_META": "PLAYBOOK",
    "GENERAL": "PLAYBOOK",
}


# ---------------------------------------------------------------------------
# Core processing logic
# ---------------------------------------------------------------------------

def get_unprocessed_alpha(rows: list[dict], specific_id: str | None = None) -> list[dict]:
    """Filter to approved alpha that hasn't been ops-generated yet."""
    processed_ids = get_processed_ids()
    results = []
    for row in rows:
        aid = row.get("alpha_id", "").strip()
        status = row.get("status", "").strip()
        category = row.get("category", "").strip()
        ops_done = (row.get("ops_generated") or "").strip().upper()

        # Filter for specific ID if requested
        if specific_id and aid != specific_id:
            continue

        # Must be approved
        if status not in ("APPROVED", "AUTO_APPROVED"):
            continue

        # Must be a processable category
        if category not in VALID_CATEGORIES:
            continue

        # Must not already be processed
        if ops_done == "TRUE" or aid in processed_ids:
            continue

        results.append(row)

    return results


def process_alpha(alpha: dict, dry_run: bool = False) -> dict | None:
    """Process a single alpha entry. Returns tracker row or None."""
    aid = (alpha.get("alpha_id") or "").strip()
    category = (alpha.get("category") or "").strip()
    if not aid or not category:
        return None
    roi = alpha.get("roi_potential", "MEDIUM")

    generator = GENERATORS.get(category)
    if not generator:
        return None

    subdir = SUBDIRS[category]
    prefix = FILE_PREFIXES[category]
    filename = f"{prefix}_{aid}.md"
    rel_path = os.path.join("AUTOMATIONS", "auto_ops", subdir, filename)
    abs_path = safe_path(os.path.join(PROJECT_ROOT, rel_path))

    # Generate content
    content = generator(alpha)

    if dry_run:
        insight = _extract_insight(alpha)
        print(f"  [{aid}] {category} -> {rel_path}")
        print(f"    insight: {truncate(insight, 80)}")
        print(f"    priority: {priority_from_roi(roi)}")
        print()
        return {
            "alpha_id": aid,
            "category": category,
            "ops_type": OPS_TYPES.get(category, "unknown"),
            "output_file": rel_path,
            "created_at": now_iso(),
            "status": "DRY_RUN",
            "priority": priority_from_roi(roi),
            "notes": truncate(_extract_insight(alpha), 120),
        }

    # Write the ops file
    with open(abs_path, "w", encoding="utf-8") as f:
        f.write(content)

    # Build tracker row
    tracker_row = {
        "alpha_id": aid,
        "category": category,
        "ops_type": OPS_TYPES.get(category, "unknown"),
        "output_file": rel_path,
        "created_at": now_iso(),
        "status": "GENERATED",
        "priority": priority_from_roi(roi),
        "notes": truncate(_extract_insight(alpha), 120),
    }

    # Append to tracker
    append_tracker_row(tracker_row)

    print(f"  [{aid}] {category} -> {rel_path} (priority: {tracker_row['priority']})")

    return tracker_row


def mark_alpha_processed(rows: list[dict], processed_ids: set[str], fieldnames: list[str]):
    """Update ops_generated=TRUE for processed alpha IDs in the CSV."""
    updated = 0
    for row in rows:
        aid = row.get("alpha_id", "").strip()
        if aid in processed_ids:
            row["ops_generated"] = "TRUE"
            updated += 1
    write_alpha_csv(rows, fieldnames)
    return updated


# ---------------------------------------------------------------------------
# CLI commands
# ---------------------------------------------------------------------------

def cmd_process(args):
    """Process all unprocessed approved alpha."""
    ensure_dirs()
    init_tracker_if_missing()

    rows = read_alpha_csv()
    if not rows:
        print("no alpha entries found.")
        return

    # Get original fieldnames
    with open(ALPHA_CSV, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        fieldnames = list(reader.fieldnames)

    specific_id = getattr(args, "process_id", None)
    unprocessed = get_unprocessed_alpha(rows, specific_id)

    if not unprocessed:
        if specific_id:
            print(f"alpha {specific_id} not found, already processed, or not APPROVED.")
        else:
            print("no unprocessed approved alpha found. everything is up to date.")
        return

    dry_run = getattr(args, "dry_run", False)
    mode_label = "DRY RUN" if dry_run else "PROCESSING"

    print(f"\n=== {mode_label}: {len(unprocessed)} alpha entries ===\n")

    processed_set = set()
    by_category = {}
    by_priority = {"HIGH": 0, "MEDIUM": 0, "LOW": 0}

    for alpha in unprocessed:
        result = process_alpha(alpha, dry_run=dry_run)
        if result:
            aid = result["alpha_id"]
            cat = result["category"]
            pri = result["priority"]
            processed_set.add(aid)
            by_category[cat] = by_category.get(cat, 0) + 1
            by_priority[pri] = by_priority.get(pri, 0) + 1

    # Update ALPHA_STAGING.csv with ops_generated flag
    if not dry_run and processed_set:
        updated = mark_alpha_processed(rows, processed_set, fieldnames)
        print(f"\nupdated {updated} alpha entries with ops_generated=TRUE")

    # Summary
    print(f"\n=== SUMMARY ===")
    print(f"total processed: {len(processed_set)}")
    print(f"\nby category:")
    for cat, count in sorted(by_category.items(), key=lambda x: -x[1]):
        print(f"  {cat}: {count}")
    print(f"\nby priority:")
    for pri in ("HIGH", "MEDIUM", "LOW"):
        if by_priority[pri]:
            print(f"  {pri}: {by_priority[pri]}")

    if not dry_run:
        print(f"\nops files written to: AUTOMATIONS/auto_ops/")
        print(f"tracker updated at: LEDGER/AUTO_OPS_TRACKER.csv")


def cmd_status(args):
    """Show processing status dashboard."""
    tracker = read_tracker()
    if not tracker:
        print("no ops generated yet. run --process first.")
        return

    by_status = {}
    by_category = {}
    by_priority = {}
    by_ops_type = {}

    for row in tracker:
        st = row.get("status", "UNKNOWN")
        cat = row.get("category", "UNKNOWN")
        pri = row.get("priority", "UNKNOWN")
        ot = row.get("ops_type", "UNKNOWN")
        by_status[st] = by_status.get(st, 0) + 1
        by_category[cat] = by_category.get(cat, 0) + 1
        by_priority[pri] = by_priority.get(pri, 0) + 1
        by_ops_type[ot] = by_ops_type.get(ot, 0) + 1

    # Count unprocessed
    rows = read_alpha_csv()
    unprocessed = get_unprocessed_alpha(rows)

    print(f"\n{'='*60}")
    print(f"  ALPHA -> OPS STATUS DASHBOARD")
    print(f"  {now_iso()}")
    print(f"{'='*60}")

    print(f"\n  total ops generated: {len(tracker)}")
    print(f"  unprocessed alpha remaining: {len(unprocessed)}")

    print(f"\n  by status:")
    for st, count in sorted(by_status.items(), key=lambda x: -x[1]):
        bar = "#" * min(count, 40)
        print(f"    {st:20s} {count:4d}  {bar}")

    print(f"\n  by category:")
    for cat, count in sorted(by_category.items(), key=lambda x: -x[1]):
        bar = "#" * min(count, 40)
        print(f"    {cat:20s} {count:4d}  {bar}")

    print(f"\n  by priority:")
    for pri in ("HIGH", "MEDIUM", "LOW"):
        count = by_priority.get(pri, 0)
        if count:
            bar = "#" * min(count, 40)
            print(f"    {pri:20s} {count:4d}  {bar}")

    print(f"\n  by ops type:")
    for ot, count in sorted(by_ops_type.items(), key=lambda x: -x[1]):
        print(f"    {ot:20s} {count:4d}")

    # Show recent entries
    recent = sorted(tracker, key=lambda x: x.get("created_at", ""), reverse=True)[:10]
    if recent:
        print(f"\n  latest 10 ops:")
        for r in recent:
            print(f"    [{r['alpha_id']}] {r['ops_type']:18s} {r['status']:12s} {r['priority']}")

    print(f"\n{'='*60}")


def cmd_cron(args):
    """Cron mode: skip if already ran today."""
    ensure_dirs()

    if os.path.exists(CRON_MARKER):
        with open(CRON_MARKER, "r") as f:
            last_run = f.read().strip()
        if last_run == today_str():
            print(f"already ran today ({today_str()}). skipping.")
            return

    # Run the process
    cmd_process(args)

    # Write cron marker
    with open(safe_path(CRON_MARKER), "w") as f:
        f.write(today_str())
    print(f"\ncron marker set for {today_str()}")


def cmd_deploy(args):
    """Mark all GENERATED ops as READY_TO_DEPLOY."""
    tracker = read_tracker()
    if not tracker:
        print("no ops to deploy. run --process first.")
        return

    updated = 0
    new_rows = []
    for row in tracker:
        if row.get("status") == "GENERATED":
            row["status"] = "READY_TO_DEPLOY"
            updated += 1
        new_rows.append(row)

    if updated == 0:
        print("no GENERATED ops to mark for deployment.")
        return

    # Rewrite tracker
    with open(safe_path(TRACKER_CSV), "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=TRACKER_FIELDS)
        writer.writeheader()
        writer.writerows(new_rows)

    print(f"marked {updated} ops as READY_TO_DEPLOY")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="alpha_to_ops: auto-execute on approved alpha entries",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent("""\
            examples:
              python3 AUTOMATIONS/alpha_to_ops.py --process
              python3 AUTOMATIONS/alpha_to_ops.py --process-id ALPHA248
              python3 AUTOMATIONS/alpha_to_ops.py --dry-run
              python3 AUTOMATIONS/alpha_to_ops.py --status
              python3 AUTOMATIONS/alpha_to_ops.py --cron
              python3 AUTOMATIONS/alpha_to_ops.py --deploy
        """),
    )

    group = parser.add_mutually_exclusive_group()
    group.add_argument("--process", action="store_true", default=True,
                       help="process all unprocessed approved alpha (default)")
    group.add_argument("--process-id", type=str, metavar="ALPHA_ID",
                       help="process a specific alpha entry by ID")
    group.add_argument("--status", action="store_true",
                       help="show summary dashboard")
    group.add_argument("--cron", action="store_true",
                       help="cron mode: process + skip if already ran today")
    group.add_argument("--deploy", action="store_true",
                       help="mark generated ops as READY_TO_DEPLOY")

    parser.add_argument("--dry-run", action="store_true",
                        help="show what would be generated without writing files")

    args = parser.parse_args()

    # Route to command
    if args.status:
        cmd_status(args)
        return

    if args.deploy:
        cmd_deploy(args)
        return

    # For process/cron, use lock
    ensure_dirs()

    with FileLock(LOCK_FILE):
        if args.cron:
            cmd_cron(args)
        elif args.process_id:
            args.dry_run = getattr(args, "dry_run", False)
            cmd_process(args)
        else:
            cmd_process(args)


if __name__ == "__main__":
    main()
