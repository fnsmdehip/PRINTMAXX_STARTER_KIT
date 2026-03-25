#!/usr/bin/env python3
"""
ph_launch_content_router.py — PRINTMAXX Automation System

Routes Product Hunt launch signals through the content pipeline:
  1. Scrapes the Optimo PH launch page (upvotes, comments, maker info, pricing)
  2. Classifies tool category and affiliate potential
  3. Generates comparison content via engagement_bait_converter
     (3 standalone tweets + a tweet thread)
  4. Pushes generated content to posting_queue
  Secondary: if maker is a solo founder with no CTO, adds them to the
  EAS cold outreach queue.

Trigger context: [PH LAUNCH] optimo: effortless media optimizer for the web

Usage (cron-safe, no interactive input):
  python ph_launch_content_router.py --run
  python ph_launch_content_router.py --status
  python ph_launch_content_router.py --dry-run
"""

import argparse
import csv
import json
import logging
import re
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

# ---------------------------------------------------------------------------
# Bootstrap: import from _common or define local fallbacks
# ---------------------------------------------------------------------------
try:
    from _common import PROJECT, safe_path, recall_skills_for_task, capture_skill_from_result
except ImportError:
    PROJECT = Path(__file__).resolve().parent.parent

    def safe_path(path):
        """Validate that path is within PROJECT root before any file operation."""
        resolved = Path(path).resolve()
        try:
            resolved.relative_to(PROJECT)
        except ValueError:
            raise ValueError(f"Unsafe path escape: {resolved} is outside {PROJECT}")
        return resolved

    def recall_skills_for_task(task):
        return []

    def capture_skill_from_result(result):
        pass

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
AUTOMATIONS       = PROJECT / "AUTOMATIONS"
LOG_PATH          = AUTOMATIONS / "logs"   / "ph_launch_content_router.log"
POSTING_QUEUE     = AUTOMATIONS / "queues" / "posting_queue.json"
EAS_QUEUE         = AUTOMATIONS / "queues" / "eas_cold_outreach.csv"
STATE_FILE        = AUTOMATIONS / "state"  / "ph_launch_content_router_state.json"

PH_BASE_URL       = "https://www.producthunt.com"
PH_LAUNCH_SLUG    = "optimo"
PH_LAUNCH_URL     = f"{PH_BASE_URL}/posts/{PH_LAUNCH_SLUG}"
SIGNAL_CONTEXT    = "[PH LAUNCH] optimo: effortless media optimizer for the web"
HTTP_TIMEOUT      = 15

TOOL_CATEGORY_KEYWORDS = {
    "media_optimizer": ["media", "optimizer", "image", "video", "compression", "web", "optimize"],
    "seo":             ["seo", "search", "rank", "organic", "visibility", "keyword"],
    "content":         ["content", "blog", "article", "writing", "copy", "editor"],
    "analytics":       ["analytics", "metrics", "tracking", "data", "insights", "dashboard"],
    "marketing":       ["marketing", "ads", "campaign", "growth", "conversion", "funnel"],
    "developer_tool":  ["api", "developer", "code", "integration", "sdk", "cli"],
    "productivity":    ["productivity", "workflow", "automation", "efficiency", "task"],
}

AFFILIATE_SIGNAL_KEYWORDS = [
    "pricing", "plan", "subscribe", "free trial", "pro", "enterprise",
    "upgrade", "premium", "monthly", "annual", "lifetime", "deal",
]


# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------

def setup_logging() -> logging.Logger:
    log_dir = safe_path(LOG_PATH.parent)
    log_dir.mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger("ph_launch_content_router")
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        fmt = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")

        fh = logging.FileHandler(safe_path(LOG_PATH), mode="a", encoding="utf-8")
        fh.setFormatter(fmt)
        logger.addHandler(fh)

        sh = logging.StreamHandler(sys.stdout)
        sh.setFormatter(logging.Formatter("[%(levelname)s] %(message)s"))
        logger.addHandler(sh)

    return logger


# ---------------------------------------------------------------------------
# HTTP helpers
# ---------------------------------------------------------------------------

def fetch_url(url: str) -> str:
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": (
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0 Safari/537.36"
            ),
            "Accept":          "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
        },
    )
    with urllib.request.urlopen(req, timeout=HTTP_TIMEOUT) as resp:
        return resp.read().decode("utf-8", errors="replace")


def extract_meta(html: str, prop: str) -> str:
    """Return content= from an og: or name= meta tag."""
    for attr in ("property", "name"):
        m = re.search(
            rf'<meta[^>]+{attr}=["\']?{re.escape(prop)}["\']?[^>]+content=["\']([^"\']*)["\']',
            html, re.IGNORECASE,
        )
        if m:
            return m.group(1).strip()
    return ""


def extract_json_ld(html: str) -> dict:
    m = re.search(
        r'<script[^>]+type=["\']application/ld\+json["\'][^>]*>(.*?)</script>',
        html, re.DOTALL | re.IGNORECASE,
    )
    if m:
        try:
            return json.loads(m.group(1))
        except (json.JSONDecodeError, ValueError):
            pass
    return {}


# ---------------------------------------------------------------------------
# PH page parsers
# ---------------------------------------------------------------------------

def _parse_int_pattern(html: str, patterns: list) -> int:
    for pat in patterns:
        m = re.search(pat, html, re.IGNORECASE)
        if m:
            try:
                return int(m.group(1))
            except (ValueError, IndexError):
                pass
    return 0


def parse_upvotes(html: str) -> int:
    return _parse_int_pattern(html, [
        r'"votes_count"\s*:\s*(\d+)',
        r'"votesCount"\s*:\s*(\d+)',
        r'data-votes-count=["\'](\d+)["\']',
        r'(\d+)\s+upvote',
    ])


def parse_comments_count(html: str) -> int:
    return _parse_int_pattern(html, [
        r'"comments_count"\s*:\s*(\d+)',
        r'"commentsCount"\s*:\s*(\d+)',
        r'(\d+)\s+comment',
    ])


def parse_makers(html: str) -> list:
    """Return list of maker dicts extracted from PH JSON blobs."""
    makers = []
    m = re.search(r'"makers"\s*:\s*(\[.*?\])', html, re.DOTALL)
    if m:
        try:
            raw = json.loads(m.group(1))
            for entry in raw:
                makers.append({
                    "name":     entry.get("name", ""),
                    "username": entry.get("username", ""),
                    "headline": entry.get("headline", ""),
                    "twitter":  entry.get("twitter_username", ""),
                    "website":  entry.get("website_url", ""),
                })
        except (json.JSONDecodeError, ValueError, KeyError):
            pass

    if not makers:
        # Lightweight fallback: harvest first few name fields
        for name in re.findall(r'"name"\s*:\s*"([^"]{3,60})"', html)[:3]:
            makers.append({"name": name, "username": "", "headline": "", "twitter": "", "website": ""})

    return makers


def parse_pricing(html: str, description: str) -> dict:
    text = (html + " " + description).lower()
    if "free" in text and "open source" in text:
        tier = "open_source"
    elif "free" in text and any(w in text for w in ("pro", "paid", "plan", "upgrade", "premium")):
        tier = "freemium"
    elif "free" in text:
        tier = "free"
    elif any(w in text for w in ("$", "price", "plan", "subscribe", "pay", "billing")):
        tier = "paid"
    else:
        tier = "unknown"
    has_affiliate = any(w in text for w in AFFILIATE_SIGNAL_KEYWORDS)
    return {"tier": tier, "has_affiliate_signals": has_affiliate}


def _mock_scrape_data() -> dict:
    """Deterministic mock used for --dry-run."""
    return {
        "url":         PH_LAUNCH_URL,
        "slug":        PH_LAUNCH_SLUG,
        "name":        "Optimo",
        "tagline":     "Effortless media optimizer for the web",
        "description": "Optimo automatically optimises every image, video, and asset on your site.",
        "upvotes":     312,
        "comments":    58,
        "makers": [
            {
                "name":     "Jordan Reyes",
                "username": "jordanreyes",
                "headline": "Founder & CEO @ Optimo",
                "twitter":  "jordanreyes",
                "website":  "https://getoptimo.io",
            }
        ],
        "topics":  ["media", "optimization", "web performance", "images"],
        "pricing": {"tier": "freemium", "has_affiliate_signals": True},
        "scraped_at": datetime.now(timezone.utc).isoformat(),
    }


def scrape_ph_launch(url: str, logger: logging.Logger, dry_run: bool = False) -> dict:
    logger.info(f"Scraping PH launch page: {url}")

    if dry_run:
        logger.info("[DRY-RUN] Returning mock scrape data")
        return _mock_scrape_data()

    try:
        html = fetch_url(url)
    except urllib.error.URLError as exc:
        logger.error(f"Network error fetching {url}: {exc}")
        raise
    except Exception as exc:
        logger.error(f"Unexpected fetch error: {exc}")
        raise

    description = extract_meta(html, "og:description") or extract_meta(html, "description")
    raw_title   = extract_meta(html, "og:title") or "Optimo"

    # Strip PH suffixes: "Name - tagline | Product Hunt"
    name = raw_title.split(" - ")[0].split(" | ")[0].strip() or "Optimo"

    tagline = (
        description.split(".")[0].strip()
        if description
        else "Effortless media optimizer for the web"
    )

    upvotes  = parse_upvotes(html)
    comments = parse_comments_count(html)
    makers   = parse_makers(html)
    pricing  = parse_pricing(html, description)

    raw_keywords = extract_meta(html, "keywords")
    topics = (
        [t.strip().lower() for t in raw_keywords.split(",") if t.strip()]
        if raw_keywords
        else ["media", "web"]
    )

    return {
        "url":         url,
        "slug":        PH_LAUNCH_SLUG,
        "name":        name,
        "tagline":     tagline,
        "description": description,
        "upvotes":     upvotes,
        "comments":    comments,
        "makers":      makers,
        "topics":      topics,
        "pricing":     pricing,
        "scraped_at":  datetime.now(timezone.utc).isoformat(),
    }


# ---------------------------------------------------------------------------
# Classification
# ---------------------------------------------------------------------------

def classify_tool(data: dict) -> dict:
    corpus = " ".join([
        data.get("name", ""),
        data.get("tagline", ""),
        data.get("description", ""),
        " ".join(data.get("topics", [])),
    ]).lower()

    scores = {
        cat: sum(1 for kw in keywords if kw in corpus)
        for cat, keywords in TOOL_CATEGORY_KEYWORDS.items()
    }

    primary = max(scores, key=scores.get) if scores else "general"
    if scores.get(primary, 0) == 0:
        primary = "general"

    pricing = data.get("pricing", {})
    aff = 0
    if pricing.get("has_affiliate_signals"):
        aff += 2
    if pricing.get("tier") in ("freemium", "paid"):
        aff += 2
    if data.get("upvotes", 0) > 100:
        aff += 1
    if data.get("comments", 0) > 20:
        aff += 1

    affiliate_potential = "high" if aff >= 4 else "medium" if aff >= 2 else "low"

    return {
        "primary_category":  primary,
        "category_scores":   scores,
        "affiliate_potential": affiliate_potential,
        "affiliate_score":   aff,
    }


# ---------------------------------------------------------------------------
# Solo founder detection
# ---------------------------------------------------------------------------

def is_solo_founder_no_cto(data: dict, logger: logging.Logger) -> bool:
    makers = data.get("makers", [])
    if len(makers) != 1:
        logger.info(f"Solo founder check failed: {len(makers)} maker(s) found")
        return False

    headline = (makers[0].get("headline") or "").lower()
    cto_signals    = ("cto", "co-founder", "cofounder", "technical co", "vp eng", "head of eng")
    founder_signals = ("founder", "ceo", "solo", "indie", "maker", "creator", "owner")

    has_cto     = any(s in headline for s in cto_signals)
    is_founder  = any(s in headline for s in founder_signals)
    result = is_founder and not has_cto

    logger.info(
        f"Solo founder check: headline='{headline}' "
        f"is_founder={is_founder} has_cto={has_cto} → {result}"
    )
    return result


# ---------------------------------------------------------------------------
# Content generation (engagement_bait_converter)
# ---------------------------------------------------------------------------

_COMPARISON_ALTS = {
    "media_optimizer": ["TinyPNG",    "Squoosh",      "ImageOptim"],
    "seo":             ["Ahrefs",     "Semrush",       "Moz"],
    "content":         ["Jasper",     "Copy.ai",       "Writesonic"],
    "analytics":       ["Mixpanel",   "Amplitude",     "Heap"],
    "marketing":       ["HubSpot",    "Mailchimp",     "ActiveCampaign"],
    "developer_tool":  ["Vercel",     "Netlify",       "Railway"],
    "productivity":    ["Notion",     "Linear",        "Coda"],
    "general":         ["legacy SaaS","paid tools",    "clunky alternatives"],
}


def engagement_bait_converter(data: dict, classification: dict, logger: logging.Logger) -> dict:
    """
    Generate 3 standalone tweets and a 5-tweet thread from scraped + classified data.
    Outputs content optimised for engagement (comparison framing, social proof, CTA).
    """
    name       = data.get("name", "Optimo")
    tagline    = data.get("tagline", "Effortless media optimizer for the web")
    upvotes    = data.get("upvotes", 0)
    comments   = data.get("comments", 0)
    slug       = data.get("slug", PH_LAUNCH_SLUG)
    tier       = data.get("pricing", {}).get("tier", "unknown")
    category   = classification.get("primary_category", "general")
    affil      = classification.get("affiliate_potential", "low")

    alts = _COMPARISON_ALTS.get(category, _COMPARISON_ALTS["general"])
    a0, a1, a2 = alts[0], alts[1], alts[2] if len(alts) > 2 else "the rest"
    cat_label  = category.replace("_", " ")

    # ── Tweet 1: curiosity / comparison hook
    tweet1 = (
        f"Everyone's defaulting to {a0} and {a1} for {cat_label}.\n\n"
        f"Then {name} dropped on Product Hunt with {upvotes}+ upvotes in a day.\n\n"
        f"Here's the honest comparison 👇"
    )

    # ── Tweet 2: feature callout + pricing
    tweet2 = (
        f"{name}: \"{tagline}\"\n\n"
        f"vs {a0}  → needs manual setup, limited batch support\n"
        f"vs {a1}  → core features paywalled\n\n"
        f"{name} is {tier}. {upvotes} builders noticed on launch day.\n\n"
        f"#ProductHunt #{cat_label.replace(' ', '').title()}"
    )

    # ── Tweet 3: engagement bait
    tweet3 = (
        f"Drop a 🔥 if you've already tried {name}.\n"
        f"Drop a 💀 if you're still on {a0}.\n\n"
        f"(I'll post highlights from the {comments} PH comments below)"
    )

    # ── Thread: 5 tweets
    thread = [
        (
            f"I spent the morning digging into {name} — the {cat_label} tool "
            f"that hit {upvotes} upvotes on Product Hunt today.\n\n"
            f"Here's how it stacks up vs {a0}, {a1}, and {a2}: 🧵 (1/5)"
        ),
        (
            f"2/5 — The {a0} problem:\n\n"
            f"• Steep config curve for non-devs\n"
            f"• No real-time preview\n"
            f"• Weak bulk processing\n\n"
            f"{name} ships all three solved, out of the box."
        ),
        (
            f"3/5 — The {a1} problem:\n\n"
            f"• Freemium wall blocks key features\n"
            f"• Slow on large file sets\n"
            f"• API docs are an afterthought\n\n"
            f"{name} is {tier}. Full capability from day one."
        ),
        (
            f"4/5 — What makes {name} different:\n\n"
            f"✅ {tagline}\n"
            f"✅ Built for web performance workflows\n"
            f"✅ Affiliate potential rated: {affil.upper()}\n\n"
            f"The community validated it: {upvotes} upvotes, {comments} comments."
        ),
        (
            f"5/5 — My take:\n\n"
            f"If you deal with media on the web at any scale, "
            f"{name} deserves 10 minutes of your day.\n\n"
            f"→ producthunt.com/posts/{slug}\n\n"
            f"RT if this saved you the research 🔁"
        ),
    ]

    logger.info(f"engagement_bait_converter: generated 3 tweets + {len(thread)}-tweet thread")

    return {
        "tweets":             [tweet1, tweet2, tweet3],
        "thread":             thread,
        "generated_at":       datetime.now(timezone.utc).isoformat(),
        "source_signal":      SIGNAL_CONTEXT,
        "category":           category,
        "affiliate_potential": affil,
    }


# ---------------------------------------------------------------------------
# Queue writers
# ---------------------------------------------------------------------------

def push_to_posting_queue(
    content: dict,
    data: dict,
    dry_run: bool,
    logger: logging.Logger,
) -> None:
    queue_path = safe_path(POSTING_QUEUE)
    queue_path.parent.mkdir(parents=True, exist_ok=True)

    existing: list = []
    if queue_path.exists():
        try:
            with open(queue_path, "r", encoding="utf-8") as fh:
                existing = json.load(fh)
        except (json.JSONDecodeError, OSError):
            existing = []

    ts      = datetime.now(timezone.utc).isoformat()
    slug    = data.get("slug", PH_LAUNCH_SLUG)
    entries = []

    for idx, tweet_body in enumerate(content.get("tweets", []), start=1):
        entries.append({
            "id":                 f"ph_{slug}_{ts}_tweet{idx}",
            "type":               "tweet",
            "platform":           "twitter",
            "content":            tweet_body,
            "source":             SIGNAL_CONTEXT,
            "category":           content.get("category"),
            "affiliate_potential": content.get("affiliate_potential"),
            "ph_slug":            slug,
            "ph_upvotes":         data.get("upvotes"),
            "queued_at":          ts,
            "status":             "pending",
        })

    thread = content.get("thread", [])
    if thread:
        entries.append({
            "id":                 f"ph_{slug}_{ts}_thread",
            "type":               "tweet_thread",
            "platform":           "twitter",
            "content":            thread,
            "thread_length":      len(thread),
            "source":             SIGNAL_CONTEXT,
            "category":           content.get("category"),
            "affiliate_potential": content.get("affiliate_potential"),
            "ph_slug":            slug,
            "ph_upvotes":         data.get("upvotes"),
            "queued_at":          ts,
            "status":             "pending",
        })

    if dry_run:
        logger.info(f"[DRY-RUN] Would enqueue {len(entries)} item(s) to posting_queue")
        for e in entries:
            logger.info(f"  → [{e['type']}] {e['id']}")
        return

    existing.extend(entries)
    with open(queue_path, "w", encoding="utf-8") as fh:
        json.dump(existing, fh, indent=2, ensure_ascii=False)
    logger.info(f"Pushed {len(entries)} item(s) → {queue_path}")


def push_to_eas_queue(
    makers: list,
    data: dict,
    dry_run: bool,
    logger: logging.Logger,
) -> None:
    if not makers:
        logger.warning("push_to_eas_queue called with empty makers list")
        return

    queue_path  = safe_path(EAS_QUEUE)
    queue_path.parent.mkdir(parents=True, exist_ok=True)
    write_header = not queue_path.exists()

    fieldnames = [
        "id", "name", "username", "headline", "twitter", "website",
        "product_name", "product_slug", "product_url", "product_tagline",
        "ph_upvotes", "ph_comments", "outreach_reason", "queued_at", "status",
    ]

    ts   = datetime.now(timezone.utc).isoformat()
    rows = []
    for maker in makers:
        uname = maker.get("username") or "unknown"
        rows.append({
            "id":              f"eas_{data.get('slug', PH_LAUNCH_SLUG)}_{uname}_{ts[:10]}",
            "name":            maker.get("name", ""),
            "username":        uname,
            "headline":        maker.get("headline", ""),
            "twitter":         maker.get("twitter", ""),
            "website":         maker.get("website", ""),
            "product_name":    data.get("name", ""),
            "product_slug":    data.get("slug", PH_LAUNCH_SLUG),
            "product_url":     data.get("url", PH_LAUNCH_URL),
            "product_tagline": data.get("tagline", ""),
            "ph_upvotes":      data.get("upvotes", 0),
            "ph_comments":     data.get("comments", 0),
            "outreach_reason": "solo_founder_no_cto_ph_launch",
            "queued_at":       ts,
            "status":          "pending",
        })

    if dry_run:
        logger.info(f"[DRY-RUN] Would add {len(rows)} maker(s) to EAS cold outreach queue")
        for r in rows:
            logger.info(f"  → {r['name']} ({r['username']}) — {r['outreach_reason']}")
        return

    with open(queue_path, "a", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        if write_header:
            writer.writeheader()
        writer.writerows(rows)
    logger.info(f"Added {len(rows)} maker(s) → {queue_path}")


# ---------------------------------------------------------------------------
# State persistence
# ---------------------------------------------------------------------------

def load_state() -> dict:
    state_path = safe_path(STATE_FILE)
    if state_path.exists():
        try:
            with open(state_path, "r", encoding="utf-8") as fh:
                return json.load(fh)
        except (json.JSONDecodeError, OSError):
            pass
    return {}


def save_state(state: dict, dry_run: bool, logger: logging.Logger) -> None:
    if dry_run:
        return
    state_path = safe_path(STATE_FILE)
    state_path.parent.mkdir(parents=True, exist_ok=True)
    with open(state_path, "w", encoding="utf-8") as fh:
        json.dump(state, fh, indent=2)
    logger.info(f"State persisted → {state_path}")


# ---------------------------------------------------------------------------
# Pipeline runner
# ---------------------------------------------------------------------------

def run_pipeline(dry_run: bool, logger: logging.Logger) -> int:
    logger.info(f"=== ph_launch_content_router START (dry_run={dry_run}) ===")
    logger.info(f"Signal: {SIGNAL_CONTEXT}")

    skills = recall_skills_for_task("ph_launch_content_routing")
    if skills:
        logger.info(f"Recalled {len(skills)} skill(s) for task")

    state  = load_state()
    run_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")

    try:
        # ── Step 1: Scrape
        data = scrape_ph_launch(PH_LAUNCH_URL, logger, dry_run=dry_run)
        logger.info(
            f"Scraped '{data['name']}' | upvotes={data['upvotes']} "
            f"comments={data['comments']} pricing={data['pricing']['tier']}"
        )

        # ── Step 2: Classify
        classification = classify_tool(data)
        logger.info(
            f"Classified: category={classification['primary_category']} "
            f"affiliate_potential={classification['affiliate_potential']} "
            f"score={classification['affiliate_score']}"
        )

        # ── Step 3: Generate content
        content = engagement_bait_converter(data, classification, logger)
        capture_skill_from_result(content)

        # ── Step 4: Push to posting_queue
        push_to_posting_queue(content, data, dry_run, logger)

        # ── Step 5 (secondary): EAS cold outreach
        solo = is_solo_founder_no_cto(data, logger)
        if solo:
            logger.info("Solo founder without CTO detected — routing to EAS cold outreach queue")
            push_to_eas_queue(data.get("makers", []), data, dry_run, logger)
        else:
            logger.info("EAS condition not met (multiple makers or CTO role present)")

        # ── Persist run record
        state[run_id] = {
            "status":             "success",
            "signal":             SIGNAL_CONTEXT,
            "ph_slug":            data.get("slug"),
            "upvotes":            data.get("upvotes"),
            "comments":           data.get("comments"),
            "category":           classification.get("primary_category"),
            "affiliate_potential": classification.get("affiliate_potential"),
            "content_items":      len(content["tweets"]) + 1,
            "eas_queued":         solo,
            "dry_run":            dry_run,
            "run_at":             datetime.now(timezone.utc).isoformat(),
        }
        save_state(state, dry_run, logger)
        logger.info(f"=== ph_launch_content_router DONE run_id={run_id} ===")
        return 0

    except Exception as exc:
        logger.error(f"Pipeline failed [{type(exc).__name__}]: {exc}", exc_info=True)
        state[run_id] = {
            "status":  "error",
            "error":   str(exc),
            "dry_run": dry_run,
            "run_at":  datetime.now(timezone.utc).isoformat(),
        }
        save_state(state, dry_run, logger)
        return 1


# ---------------------------------------------------------------------------
# Status reporter
# ---------------------------------------------------------------------------

def show_status(logger: logging.Logger) -> int:
    state = load_state()

    if not state:
        print("No pipeline runs recorded yet.")
    else:
        runs = sorted(state.items(), reverse=True)
        print(f"\n{'Run ID':<22} {'Status':<10} {'Category':<18} {'Affiliate':<10} {'Items':<6} {'EAS'}")
        print("-" * 78)
        for run_id, info in runs[:15]:
            print(
                f"{run_id:<22} {info.get('status','?'):<10} "
                f"{info.get('category','?'):<18} {info.get('affiliate_potential','?'):<10} "
                f"{str(info.get('content_items','?')):<6} "
                f"{'yes' if info.get('eas_queued') else 'no'}"
            )

    # Posting queue summary
    pq = safe_path(POSTING_QUEUE)
    if pq.exists():
        try:
            with open(pq, "r", encoding="utf-8") as fh:
                items = json.load(fh)
            pending = sum(1 for i in items if i.get("status") == "pending")
            print(f"\nPosting queue  : {len(items)} total  |  {pending} pending  ({pq})")
        except Exception as exc:
            print(f"\nPosting queue  : (read error: {exc})")
    else:
        print(f"\nPosting queue  : empty  ({pq})")

    # EAS queue summary
    eas = safe_path(EAS_QUEUE)
    if eas.exists():
        try:
            with open(eas, "r", encoding="utf-8") as fh:
                rows = list(csv.DictReader(fh))
            pending = sum(1 for r in rows if r.get("status") == "pending")
            print(f"EAS cold outreach: {len(rows)} total  |  {pending} pending  ({eas})")
        except Exception as exc:
            print(f"EAS cold outreach: (read error: {exc})")
    else:
        print(f"EAS cold outreach: empty  ({eas})")

    return 0


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        prog="ph_launch_content_router",
        description="PRINTMAXX: Route PH launch signal through the content pipeline.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"Trigger signal: {SIGNAL_CONTEXT}",
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--run",
        action="store_true",
        help="Execute the full pipeline (scrape → classify → generate → queue)",
    )
    group.add_argument(
        "--status",
        action="store_true",
        help="Display run history and queue sizes",
    )
    group.add_argument(
        "--dry-run",
        dest="dry_run",
        action="store_true",
        help="Simulate pipeline end-to-end without writing to any queue",
    )

    args   = parser.parse_args()
    logger = setup_logging()

    try:
        if args.run:
            sys.exit(run_pipeline(dry_run=False, logger=logger))
        elif args.dry_run:
            sys.exit(run_pipeline(dry_run=True, logger=logger))
        elif args.status:
            sys.exit(show_status(logger=logger))
    except KeyboardInterrupt:
        logger.info("Interrupted")
        sys.exit(130)
    except Exception as exc:
        logger.error(f"Fatal: {exc}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()