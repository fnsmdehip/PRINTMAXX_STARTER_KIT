#!/usr/bin/env python3

from __future__ import annotations
"""
PRINTMAXX Auto Content Poster
==============================
Reads content from CONTENT/social/, rewrites with viral hooks,
posts via X/Twitter API, tracks engagement, identifies winners,
and generates ad boost recommendations.

CLI:
  --post        Post next batch of content
  --check       Check engagement on posted content
  --winners     Show winners from last 7 days
  --boost       Show ad boost recommendations
  --schedule    Show upcoming post schedule
  --dry-run     Preview without posting
  --cron        Quiet mode (post + check + flag winners)
  --rewrite     Rewrite content in viral hook style (preview only)
  --status      Quick status overview

Usage:
  python3 AUTOMATIONS/auto_content_poster.py --post --dry-run
  python3 AUTOMATIONS/auto_content_poster.py --check
  python3 AUTOMATIONS/auto_content_poster.py --winners
  python3 AUTOMATIONS/auto_content_poster.py --cron
"""

import os
import sys
import csv
import json
import re
import time
import random
import hashlib
import logging
import argparse
from datetime import datetime, timedelta, timezone
from pathlib import Path


def utcnow() -> datetime:
    """Return current UTC time (timezone-aware)."""
    return datetime.now(timezone.utc)

# ---------------------------------------------------------------------------
# PATHS
# ---------------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent
CONTENT_SOCIAL = BASE_DIR / "CONTENT" / "social"
LEDGER_DIR = BASE_DIR / "LEDGER"
OPS_DIR = BASE_DIR / "OPS"
SECRETS_DIR = BASE_DIR / "SECRETS"
CREDENTIALS_FILE = SECRETS_DIR / "CREDENTIALS.env"
PERFORMANCE_CSV = LEDGER_DIR / "CONTENT_PERFORMANCE.csv"
WINNERS_CSV = LEDGER_DIR / "CONTENT_WINNERS.csv"
POSTED_CSV = LEDGER_DIR / "CONTENT_POSTED.csv"
QUEUE_CSV = LEDGER_DIR / "CONTENT_QUEUE.csv"
AD_BOOST_MD = OPS_DIR / "AD_BOOST_RECOMMENDATIONS.md"
LOG_FILE = BASE_DIR / "AUTOMATIONS" / "logs" / "auto_content_poster.log"

# ---------------------------------------------------------------------------
# ACCOUNT CONFIG
# ---------------------------------------------------------------------------
# account_key -> { niche, content_dir (relative to CONTENT/social/), handle }
ACCOUNTS = {
    "printmaxxer":   {"niche": "tech/solopreneur", "dir": "printmaxxer",            "handle": "@PRINTMAXXER"},
    "growthpilled":  {"niche": "growth/marketing",  "dir": "growthpilled",           "handle": "@growthpilled"},
    "outboundtwts":  {"niche": "cold outreach",     "dir": "outboundtwts",           "handle": "@outboundtwts"},
    "clipvault":     {"niche": "clipping/content",   "dir": "clipvault",             "handle": "@clipvault_"},
    "toolstwts":     {"niche": "tools/saas",         "dir": "toolstwts",             "handle": "@toolstwts"},
    "repscheme":     {"niche": "fitness/self-improvement", "dir": "repscheme",        "handle": "@repscheme"},
    "voidpilled":    {"niche": "esoteric/philosophy", "dir": "esoteric",             "handle": "@voidpilled"},
    "selahmoments":  {"niche": "faith/prayer",       "dir": "selahmoments",          "handle": "@selahmoments"},
    "shiplog":       {"niche": "building-in-public",  "dir": "shiplog",              "handle": "@shiplog_"},
    "silentframes":  {"niche": "aesthetic/visual",    "dir": "aesthetic",             "handle": "@silentframes"},
    "velvetframes":  {"niche": "beauty/curated",      "dir": "beauty_curated",       "handle": "@velvetframes"},
    "drifthour":     {"niche": "ambient/chill",       "dir": "drifthour",            "handle": "@drifthour"},
}

# Posting schedule: account -> list of (hour, minute) UTC slots per day
# Spread through the day. 2-4 posts per account per day max.
POSTING_SCHEDULE = {
    "printmaxxer":   [(9, 0), (13, 30), (18, 0), (21, 30)],
    "growthpilled":  [(8, 30), (12, 0), (17, 0)],
    "outboundtwts":  [(10, 0), (14, 0), (19, 0)],
    "clipvault":     [(11, 0), (16, 0), (20, 30)],
    "toolstwts":     [(9, 30), (14, 30), (19, 30)],
    "repscheme":     [(7, 0), (12, 30), (18, 30)],
    "voidpilled":    [(22, 0), (2, 0)],
    "selahmoments":  [(5, 30), (12, 0), (20, 0)],
    "shiplog":       [(10, 30), (15, 0), (20, 0)],
    "silentframes":  [(8, 0), (17, 30)],
    "velvetframes":  [(11, 30), (16, 30)],
    "drifthour":     [(23, 0), (6, 0)],
}

# Niche benchmarks for ad CPC/CPM estimates (USD)
NICHE_AD_BENCHMARKS = {
    "tech/solopreneur":       {"cpc": 1.20, "cpm": 8.50,  "best_platform": "X Ads"},
    "growth/marketing":       {"cpc": 1.50, "cpm": 10.00, "best_platform": "X Ads"},
    "cold outreach":          {"cpc": 2.00, "cpm": 12.00, "best_platform": "Meta Ads"},
    "clipping/content":       {"cpc": 0.80, "cpm": 6.00,  "best_platform": "TikTok Ads"},
    "tools/saas":             {"cpc": 1.80, "cpm": 11.00, "best_platform": "X Ads"},
    "fitness/self-improvement": {"cpc": 0.60, "cpm": 5.00, "best_platform": "Meta Ads"},
    "esoteric/philosophy":    {"cpc": 0.40, "cpm": 3.50,  "best_platform": "X Ads"},
    "faith/prayer":           {"cpc": 0.50, "cpm": 4.00,  "best_platform": "Meta Ads"},
    "building-in-public":     {"cpc": 1.10, "cpm": 8.00,  "best_platform": "X Ads"},
    "aesthetic/visual":       {"cpc": 0.70, "cpm": 5.50,  "best_platform": "Meta Ads"},
    "beauty/curated":         {"cpc": 0.90, "cpm": 7.00,  "best_platform": "Meta Ads"},
    "ambient/chill":          {"cpc": 0.35, "cpm": 3.00,  "best_platform": "TikTok Ads"},
}

# X API free tier: 500 posts/month per app, 1,500 reads/month
X_FREE_TIER_POST_LIMIT = 500
X_FREE_TIER_READ_LIMIT = 1500

# ---------------------------------------------------------------------------
# X ALGORITHM WEIGHTS (Feb 2026 — confirmed working)
# ---------------------------------------------------------------------------
# These multipliers determine how X ranks content in the For You feed.
# Source: X open-source algorithm analysis + high-signal accounts
X_ALGO_WEIGHTS = {
    "like": 1,           # Baseline signal
    "retweet": 20,       # 20x a like
    "reply": 13.5,       # 13.5x a like
    "profile_click": 12, # 12x a like
    "bookmark": 10,      # 10x a like (hardest to fake)
    "author_engaged_reply": 75,  # Reply where OP engages back = 150x a like equivalent
}

# TweepCred: X's hidden 0-100 reputation score
# Accounts below 0.5% engagement on first 100 tweets get Cold Start Suppression
TWEEPCRED_COLD_START_THRESHOLD = 0.005  # 0.5% engagement rate minimum
TWEEPCRED_MIN_TWEETS_FOR_EVAL = 100

# Reply Guy Strategy Constants
REPLY_WINDOW_MINUTES = 15       # Reply within 15 min = 30x visibility vs original posts
REPLIES_PER_DAY_0_1K = 30       # 0-1K followers: 20-30 replies/day
REPLIES_PER_DAY_1K_10K = 50     # 1K-10K: 30-50 replies/day
REPLIES_PER_DAY_10K_PLUS = 50   # 10K+: 50+ replies/day

# ---------------------------------------------------------------------------
# REPLY GUY TARGET LISTS (per account — from OPS/REPLY_GUY_TARGET_LISTS.md)
# ---------------------------------------------------------------------------
# Top 5 highest-ROI targets per account for automated reply scheduling
REPLY_GUY_TARGETS = {
    "printmaxxer": [
        "@levelsio", "@marc_louvion", "@tdinh_me", "@dannypostmaa", "@ProductHunt",
    ],
    "growthpilled": [
        "@heyshrutimishra", "@ecomchasedimond", "@SahilBloom", "@thesamparr", "@alexgarcia_atx",
    ],
    "outboundtwts": [
        "@pipelineabuser", "@codyschneiderxx", "@seanb2b", "@caiden_cole", "@Instantly_ai",
    ],
    "clipvault": [
        "@Culture_Crave", "@InternetH0F", "@historyinmemes", "@PopBase", "@WatcherGuru",
    ],
    "toolstwts": [
        "@therundownai", "@ProductHunt", "@ai_for_success", "@TechCrunch", "@heyshrutimishra",
    ],
    "repscheme": [
        "@IronSage_", "@JeffNippard", "@hubermanlab", "@MikeIsraetel", "@drlayne",
    ],
    "voidpilled": [
        "@DeepPsycho_HQ", "@naval", "@existentialcoms", "@JordanBPeterson", "@DEagleman",
    ],
    "selahmoments": [
        "@JoelOsteen", "@RickWarren", "@BishopJakes", "@JoyceMeyer", "@TheSelfLab",
    ],
    "shiplog": [
        "@levelsio", "@marc_louvion", "@johnrushx", "@ProductHunt", "@tdinh_me",
    ],
    "silentframes": [
        "@LiminalSpaces", "@NatGeo", "@ArchDailyX", "@cozyplaces", "@AcademiaDreams",
    ],
    "velvetframes": [
        "@FemenineFrames", "@thedimevault", "@NikkieTutorials", "@AlixEarle", "@skincarebyhyram",
    ],
    "drifthour": [
        "@lofigirl", "@ChilledCow", "@steezyasfuck", "@MrSuicideSheep", "@ChillNation",
    ],
}

# ---------------------------------------------------------------------------
# BANNED AI SLOP WORDS (from copy-style.md)
# ---------------------------------------------------------------------------
AI_SLOP_WORDS = [
    "additionally", "moreover", "furthermore", "testament", "landscape",
    "paradigm", "leverage", "utilize", "delve", "unpack", "comprehensive",
    "robust", "streamlined", "game-changer", "unlock", "elevate",
    "cutting-edge", "innovative", "revolutionary", "empower", "enable",
    "foster", "seamless", "frictionless", "journey", "dive into",
    "breathtaking", "groundbreaking", "nestled", "tapestry", "multifaceted",
]

# ---------------------------------------------------------------------------
# VIRAL HOOK TEMPLATES
# ---------------------------------------------------------------------------
VIRAL_HOOK_PATTERNS = [
    "I {action}. here's what happened.",
    "{number} {things} in {timeframe}. the {result} is insane.",
    "stop {bad_thing}. just {good_thing}.",
    "the uncomfortable truth about {topic}: {insight}",
    "I spent {time} on {thing}. {result}.",
    "everyone is {wrong_thing}. meanwhile {right_thing}.",
    "{number} people asked me about {topic}. here's the answer.",
    "built {thing}. ran it. {result}.",
    "most people {common_mistake}. the ones printing {correct_action}.",
    "the gap between $0 and ${amount} is {insight}.",
]

# Leonardo.ai prompt templates by niche
LEONARDO_PROMPTS = {
    "tech/solopreneur": "dark minimalist workspace with glowing monitors showing code and dashboards, purple and cyan accent lighting, ultra-modern desk setup, 4K, cinematic lighting, no text",
    "growth/marketing": "abstract growth chart visualization with upward arrows, dark background with neon green data lines, modern data dashboard aesthetic, no text",
    "cold outreach": "professional inbox visualization with highlighted emails, dark theme email client, blue accent glow, clean UI mockup, no text",
    "clipping/content": "content creation studio with multiple screens showing video editing timeline, purple and orange neon glow, modern creator setup, no text",
    "tools/saas": "floating holographic tool icons and interfaces, dark background with blue and white glow, futuristic software visualization, no text",
    "fitness/self-improvement": "dramatic gym silhouette with morning light, motivational atmosphere, dark tones with warm highlights, cinematic, no text",
    "esoteric/philosophy": "cosmic void with scattered light particles, deep space meditation visual, black background with subtle purple nebula, ethereal, no text",
    "faith/prayer": "warm golden hour light streaming through window onto prayer beads, peaceful atmosphere, soft bokeh, warm tones, no text",
    "building-in-public": "construction blueprint visualization with code overlay, transparent layers showing progress, blue and white wireframe aesthetic, no text",
    "aesthetic/visual": "minimalist photography composition with rule of thirds, muted desaturated colors, fine art aesthetic, film grain, no text",
    "beauty/curated": "luxury beauty product flat lay with soft diffused lighting, rose gold and marble textures, editorial photography style, no text",
    "ambient/chill": "lo-fi room at sunset with warm lamp glow, rainy window, cozy ambient atmosphere, soft focus, warm muted palette, no text",
}

# ---------------------------------------------------------------------------
# LOGGER
# ---------------------------------------------------------------------------
def setup_logger(quiet=False):
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    level = logging.WARNING if quiet else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler(LOG_FILE, encoding="utf-8"),
            logging.StreamHandler(sys.stdout),
        ],
    )
    return logging.getLogger("auto_content_poster")

log = setup_logger()

# ---------------------------------------------------------------------------
# CREDENTIAL LOADING
# ---------------------------------------------------------------------------
def load_credentials() -> dict:
    """Load credentials from SECRETS/CREDENTIALS.env."""
    creds = {}
    if not CREDENTIALS_FILE.exists():
        log.warning(f"Credentials file not found: {CREDENTIALS_FILE}")
        return creds
    with open(CREDENTIALS_FILE, "r") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" in line:
                key, _, value = line.partition("=")
                creds[key.strip()] = value.strip()
    return creds


def get_twitter_api_creds(account_key: str, creds: dict) -> dict | None:
    """
    Extract Twitter API v2 OAuth 1.0a credentials for a given account.
    Expected env vars in CREDENTIALS.env:
      TWITTER_{ACCOUNT}_API_KEY
      TWITTER_{ACCOUNT}_API_SECRET
      TWITTER_{ACCOUNT}_ACCESS_TOKEN
      TWITTER_{ACCOUNT}_ACCESS_TOKEN_SECRET
      TWITTER_{ACCOUNT}_BEARER_TOKEN
    """
    prefix = f"TWITTER_{account_key.upper()}"
    api_key = creds.get(f"{prefix}_API_KEY", "")
    api_secret = creds.get(f"{prefix}_API_SECRET", "")
    access_token = creds.get(f"{prefix}_ACCESS_TOKEN", "")
    access_secret = creds.get(f"{prefix}_ACCESS_TOKEN_SECRET", "")
    bearer = creds.get(f"{prefix}_BEARER_TOKEN", "")

    if not all([api_key, api_secret, access_token, access_secret]):
        return None

    return {
        "api_key": api_key,
        "api_secret": api_secret,
        "access_token": access_token,
        "access_token_secret": access_secret,
        "bearer_token": bearer,
    }


def check_credentials_status(creds: dict):
    """Print which accounts have API credentials configured."""
    print("\n=== TWITTER API CREDENTIAL STATUS ===\n")
    configured = 0
    for acct in ACCOUNTS:
        api_creds = get_twitter_api_creds(acct, creds)
        status = "CONFIGURED" if api_creds else "MISSING"
        symbol = "+" if api_creds else "-"
        print(f"  [{symbol}] {acct:20s} {status}")
        if api_creds:
            configured += 1

    print(f"\n  {configured}/{len(ACCOUNTS)} accounts have API credentials.\n")
    if configured == 0:
        print("  To configure, add these to SECRETS/CREDENTIALS.env for each account:")
        print("    TWITTER_{ACCOUNT}_API_KEY=...")
        print("    TWITTER_{ACCOUNT}_API_SECRET=...")
        print("    TWITTER_{ACCOUNT}_ACCESS_TOKEN=...")
        print("    TWITTER_{ACCOUNT}_ACCESS_TOKEN_SECRET=...")
        print("    TWITTER_{ACCOUNT}_BEARER_TOKEN=...")
        print()
        print("  Get keys from https://developer.x.com/en/portal/dashboard")
        print("  Free tier: 500 posts/month, 1,500 reads/month per app.")
        print()

# ---------------------------------------------------------------------------
# CONTENT PARSING
# ---------------------------------------------------------------------------
def parse_md_content(filepath: Path) -> list[dict]:
    """
    Parse a markdown content file and extract individual tweets/posts.
    Supports formats:
      - ### Tweet N / ### N.N / ### 1/7 headers with content below
      - ```code blocks``` containing tweets
      - Plain paragraphs under ### headers
    Returns list of dicts: {text, source_file, section, index}
    """
    items = []
    if not filepath.exists():
        return items

    text = filepath.read_text(encoding="utf-8", errors="replace")
    # Split into sections by ### headers
    sections = re.split(r"(?m)^###\s+", text)

    for i, section in enumerate(sections):
        if not section.strip():
            continue

        # Extract section title (first line)
        lines = section.strip().split("\n", 1)
        title = lines[0].strip()
        body = lines[1].strip() if len(lines) > 1 else ""

        # Skip metadata sections
        if any(kw in title.lower() for kw in ["status:", "voice:", "source:", "date:", "real numbers"]):
            continue
        # Skip section headers that are just labels
        if title.startswith("SECTION") or title.startswith("---"):
            continue

        # Extract content from code blocks or plain text
        code_blocks = re.findall(r"```\s*\n(.*?)```", body, re.DOTALL)
        if code_blocks:
            for block in code_blocks:
                content = block.strip()
                if content and len(content) > 15:
                    items.append({
                        "text": content,
                        "source_file": str(filepath.relative_to(BASE_DIR)),
                        "section": title,
                        "index": len(items),
                    })
        elif body and len(body) > 15:
            # Plain text content (no code block wrapper)
            # Skip if it looks like metadata or file-level preamble
            skip_prefixes = ("Generated", "Status:", "**Account:**", "**Created:",
                             "**Status:", "**Voice:", "**Schedule:", "**Niche:")
            if body.startswith(skip_prefixes):
                continue
            # Strip leading bold label like "**Tweet 1 (Monday AM)**\n\n"
            cleaned = re.sub(r"^\*\*[Tt]weet\s+\d+.*?\*\*\s*\n*", "", body).strip()
            if not cleaned or len(cleaned) < 15:
                continue
            items.append({
                "text": cleaned,
                "source_file": str(filepath.relative_to(BASE_DIR)),
                "section": title,
                "index": len(items),
            })

    return items


def parse_csv_content(filepath: Path) -> list[dict]:
    """Parse a CSV content file. Expects columns: content or text or tweet."""
    items = []
    if not filepath.exists():
        return items

    with open(filepath, "r", encoding="utf-8", errors="replace") as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader):
            # Try multiple column names
            content = (
                row.get("content", "")
                or row.get("text", "")
                or row.get("tweet", "")
                or row.get("post", "")
                or row.get("body", "")
            )
            if content and len(content.strip()) > 15:
                items.append({
                    "text": content.strip(),
                    "source_file": str(filepath.relative_to(BASE_DIR)),
                    "section": f"row_{i}",
                    "index": i,
                })
    return items


def load_all_content() -> dict[str, list[dict]]:
    """
    Load all content from CONTENT/social/ directories.
    Returns: {account_key: [content_items]}
    """
    all_content = {}
    for acct_key, info in ACCOUNTS.items():
        content_dir = CONTENT_SOCIAL / info["dir"]
        items = []
        if content_dir.exists():
            for f in sorted(content_dir.iterdir()):
                if f.suffix == ".md":
                    items.extend(parse_md_content(f))
                elif f.suffix == ".csv":
                    items.extend(parse_csv_content(f))
        all_content[acct_key] = items
    return all_content


# ---------------------------------------------------------------------------
# VIRAL HOOK REWRITER
# ---------------------------------------------------------------------------
def content_hash(text: str) -> str:
    """Generate a short hash of content for dedup."""
    return hashlib.md5(text.encode("utf-8")).hexdigest()[:12]


def strip_ai_slop(text: str) -> str:
    """Remove banned AI vocabulary from text."""
    result = text
    for word in AI_SLOP_WORDS:
        # Case-insensitive replacement
        pattern = re.compile(re.escape(word), re.IGNORECASE)
        result = pattern.sub("", result)
    # Clean up double spaces and weird punctuation from removals
    result = re.sub(r"  +", " ", result)
    result = re.sub(r" ,", ",", result)
    result = re.sub(r" \.", ".", result)
    return result.strip()


def strip_em_dashes(text: str) -> str:
    """Replace em dashes with periods or commas."""
    # em dash variants
    text = text.replace("\u2014", ". ")   # —
    text = text.replace("\u2013", ". ")   # –
    text = text.replace(" - ", ". ")      # spaced hyphens used as dashes
    text = re.sub(r"  +", " ", text)
    return text


def make_lowercase_energy(text: str) -> str:
    """Convert to lowercase energy style (no all-caps shouting)."""
    # Lowercase everything except specific abbreviations
    keep_upper = {"AI", "API", "SEO", "PWA", "GTM", "ASO", "ROI", "CAC", "LTV",
                  "CPC", "CPM", "CTA", "KDP", "POD", "DM", "FB", "IG", "YT",
                  "TOS", "FTC", "URL", "CSV", "PDF", "SaaS", "MRR", "ARR",
                  "USD", "K", "M", "B", "DOGE", "ETH", "BTC", "USA", "US",
                  "AM", "PM", "UTC", "SOAX", "HTTPS", "HTTP"}
    words = text.split()
    result = []
    for w in words:
        stripped = re.sub(r"[^\w]", "", w)
        if stripped.upper() in keep_upper:
            result.append(w)
        elif w.startswith("@") or w.startswith("#") or w.startswith("$"):
            result.append(w)
        elif w.startswith("http"):
            result.append(w)
        else:
            result.append(w.lower())
    return " ".join(result)


def strip_markdown(text: str) -> str:
    """Remove markdown formatting artifacts from text."""
    result = text
    # Remove bold markers
    result = re.sub(r"\*\*(.+?)\*\*", r"\1", result)
    # Remove italic markers
    result = re.sub(r"\*(.+?)\*", r"\1", result)
    # Remove strikethrough
    result = re.sub(r"~~(.+?)~~", r"\1", result)
    # Remove inline code
    result = re.sub(r"`(.+?)`", r"\1", result)
    # Remove checkmark emoji and similar unicode
    result = result.replace("\u2705", "").replace("\u274c", "")
    # Remove numbered list prefixes at start
    result = re.sub(r"^\d+\.\s+", "", result)
    # Clean up double spaces
    result = re.sub(r"  +", " ", result)
    return result.strip()


def is_meta_content(text: str) -> bool:
    """Detect content that is metadata or naming discussions, not postable content."""
    lower = text.lower()
    # Account naming discussions
    if any(kw in lower for kw in ["handle exists on", "was first choice",
                                   "new primary choice", "handle taken",
                                   "best option. evokes", "underscore feels",
                                   "sounds like a curated",
                                   "matches the aesthetic of the images",
                                   "lowercase. two words", "lowercase. clean. minimal"]):
        return True
    # File/config references
    if lower.startswith(("created:", "status:", "generated", "source:")):
        return True
    # Markdown metadata blocks (starts with **Generated:** or similar)
    if re.match(r"^\*\*(Generated|Created|Status|Voice|Schedule|Niche|Account):", text):
        return True
    # Name handle analysis (e.g. "1. @voidpilled -- best option")
    if re.match(r"^(?:\d+\.\s*)?(?:~~)?\*?\*?@\w+\*?\*?(?:~~)?\s*[-\u2014]", text):
        return True
    # Has more bold labels than content (metadata-heavy)
    bold_count = len(re.findall(r"\*\*.*?\*\*", text))
    if bold_count > 3 and len(text) < 300:
        return True
    # Inline code block that is just a name/label (e.g. `silent frames`)
    if text.startswith("`") and len(text) < 100:
        return True
    return False


def rewrite_viral_hook(text: str, niche: str = "") -> str:
    """
    Rewrite content into a viral hook using @pipelineabuser patterns.
    Rules:
    - Consequence-first hooks
    - Specific numbers
    - Lowercase energy
    - No em dashes
    - No AI slop words
    - No markdown formatting
    - Short punchy sentences
    """
    # Step 0: strip markdown formatting
    result = strip_markdown(text)

    # Step 1: strip AI slop
    result = strip_ai_slop(result)

    # Step 2: strip em dashes
    result = strip_em_dashes(result)

    # Step 3: strip label patterns like "Post 1:" or "Tweet 3:" or "--- Tweet 2"
    result = re.sub(r"^(?:post|tweet)\s*\d+\s*[-:.]?\s*", "", result, flags=re.IGNORECASE).strip()
    # Also strip mid-text section breaks that leak from multi-tweet blocks
    result = re.sub(r"\s*---+\s*(?:tweet|post)\s*\d+[.:]?\s*", ". ", result, flags=re.IGNORECASE)
    result = re.sub(r"\s+(?:tweet|post)\s+\d+\s*:\s*", ". ", result, flags=re.IGNORECASE)

    # Step 4: lowercase energy
    result = make_lowercase_energy(result)

    # Step 5: collapse newlines into spaces for single tweet format
    result = re.sub(r"\n+", " ", result)
    result = re.sub(r"  +", " ", result)
    # Fix double periods from section break replacements
    result = re.sub(r"\.{2,}", ".", result)
    # Fix ". ." patterns
    result = re.sub(r"\.\s+\.", ".", result)

    # Step 6: trim to 280 chars for tweet (Twitter limit)
    if len(result) > 280:
        # Find a sentence break near 260 chars
        truncated = result[:270]
        last_period = truncated.rfind(".")
        last_newline = truncated.rfind("\n")
        cut_point = max(last_period, last_newline)
        if cut_point > 100:
            result = result[:cut_point + 1]
        else:
            result = result[:275] + "..."

    # Step 7: clean leading punctuation/whitespace artifacts
    result = re.sub(r"^[\s.,;:]+", "", result).strip()

    # Step 8: ensure it starts with lowercase (consequence-first energy)
    if result and result[0].isupper() and not result.startswith(("I ", "I'", "AI")):
        result = result[0].lower() + result[1:]

    return result.strip()


def generate_image_prompt(niche: str, content_preview: str = "") -> str:
    """
    Generate a Leonardo.ai image prompt based on niche.
    """
    base = LEONARDO_PROMPTS.get(niche, LEONARDO_PROMPTS["tech/solopreneur"])

    # Add content-specific keywords if available
    keywords = []
    if "revenue" in content_preview.lower() or "$" in content_preview:
        keywords.append("financial dashboard visualization")
    if "code" in content_preview.lower() or "script" in content_preview.lower():
        keywords.append("code on screen")
    if "lead" in content_preview.lower() or "email" in content_preview.lower():
        keywords.append("email pipeline visualization")
    if "app" in content_preview.lower() or "PWA" in content_preview:
        keywords.append("mobile app UI mockup")

    if keywords:
        base += ", " + ", ".join(keywords[:2])

    return f"Leonardo.ai prompt: {base}"


# ---------------------------------------------------------------------------
# CSV HELPERS
# ---------------------------------------------------------------------------
PERFORMANCE_FIELDS = [
    "post_id", "account", "platform", "content_hash", "content_preview",
    "full_text", "posted_at", "tweet_url",
    "likes_1h", "likes_6h", "likes_24h", "likes_7d",
    "retweets_1h", "retweets_6h", "retweets_24h", "retweets_7d",
    "replies_1h", "replies_6h", "replies_24h", "replies_7d",
    "impressions_1h", "impressions_6h", "impressions_24h", "impressions_7d",
    "engagement_rate", "winner_score", "status",
    "last_checked", "source_file",
]

POSTED_FIELDS = [
    "content_hash", "account", "posted_at", "tweet_id", "tweet_url",
    "source_file", "content_preview",
]

WINNERS_FIELDS = [
    "post_id", "account", "platform", "content_preview", "posted_at",
    "likes_7d", "retweets_7d", "replies_7d", "impressions_7d",
    "engagement_rate", "winner_score", "status", "boost_budget",
    "tweet_url",
]


def ensure_csv(filepath: Path, fields: list[str]):
    """Create CSV with headers if it does not exist."""
    filepath.parent.mkdir(parents=True, exist_ok=True)
    if not filepath.exists():
        with open(filepath, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fields)
            writer.writeheader()


def read_csv_rows(filepath: Path) -> list[dict]:
    """Read all rows from a CSV."""
    if not filepath.exists():
        return []
    with open(filepath, "r", encoding="utf-8", errors="replace") as f:
        return list(csv.DictReader(f))


def append_csv_row(filepath: Path, fields: list[str], row: dict):
    """Append a single row to a CSV."""
    ensure_csv(filepath, fields)
    with open(filepath, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writerow(row)


def write_csv_rows(filepath: Path, fields: list[str], rows: list[dict]):
    """Overwrite CSV with new rows."""
    filepath.parent.mkdir(parents=True, exist_ok=True)
    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def get_posted_hashes() -> set:
    """Return set of content_hash values already posted."""
    rows = read_csv_rows(POSTED_CSV)
    return {r.get("content_hash", "") for r in rows}


# ---------------------------------------------------------------------------
# TWITTER API v2 (OAuth 1.0a User Context)
# ---------------------------------------------------------------------------
def twitter_post_tweet(text: str, api_creds: dict) -> dict | None:
    """
    Post a tweet using X API v2 with OAuth 1.0a.
    Returns: {tweet_id, tweet_url} or None on failure.
    Uses requests + requests_oauthlib for OAuth signing.
    """
    try:
        from requests_oauthlib import OAuth1Session
    except ImportError:
        log.error("requests_oauthlib not installed. Run: pip3 install requests-oauthlib")
        return None

    url = "https://api.x.com/2/tweets"
    oauth = OAuth1Session(
        api_creds["api_key"],
        client_secret=api_creds["api_secret"],
        resource_owner_key=api_creds["access_token"],
        resource_owner_secret=api_creds["access_token_secret"],
    )

    payload = {"text": text}

    try:
        resp = oauth.post(url, json=payload)
        if resp.status_code == 201:
            data = resp.json()
            tweet_id = data.get("data", {}).get("id", "")
            # Construct URL from the user handle -- not always known, use ID
            tweet_url = f"https://x.com/i/status/{tweet_id}"
            log.info(f"Posted tweet {tweet_id}: {text[:60]}...")
            return {"tweet_id": tweet_id, "tweet_url": tweet_url}
        elif resp.status_code == 429:
            log.warning(f"Rate limited. Retry after: {resp.headers.get('x-rate-limit-reset', 'unknown')}")
            reset_ts = resp.headers.get("x-rate-limit-reset")
            if reset_ts:
                wait = max(0, int(reset_ts) - int(time.time())) + 5
                log.warning(f"Waiting {wait}s for rate limit reset...")
                time.sleep(min(wait, 900))  # cap at 15 min
            return None
        else:
            log.error(f"Twitter API error {resp.status_code}: {resp.text}")
            return None
    except Exception as e:
        log.error(f"Twitter post failed: {e}")
        return None


def twitter_get_tweet_metrics(tweet_id: str, api_creds: dict) -> dict | None:
    """
    Get tweet public metrics using X API v2.
    Returns: {likes, retweets, replies, impressions} or None.
    """
    try:
        from requests_oauthlib import OAuth1Session
    except ImportError:
        log.error("requests_oauthlib not installed.")
        return None

    url = f"https://api.x.com/2/tweets/{tweet_id}"
    params = {"tweet.fields": "public_metrics,non_public_metrics,organic_metrics"}

    oauth = OAuth1Session(
        api_creds["api_key"],
        client_secret=api_creds["api_secret"],
        resource_owner_key=api_creds["access_token"],
        resource_owner_secret=api_creds["access_token_secret"],
    )

    try:
        resp = oauth.get(url, params=params)
        if resp.status_code == 200:
            data = resp.json().get("data", {})
            public = data.get("public_metrics", {})
            # non_public_metrics only available to tweet owner with user context
            non_public = data.get("non_public_metrics", {})
            organic = data.get("organic_metrics", {})
            return {
                "likes": public.get("like_count", 0),
                "retweets": public.get("retweet_count", 0),
                "replies": public.get("reply_count", 0),
                "impressions": (
                    non_public.get("impression_count", 0)
                    or organic.get("impression_count", 0)
                    or public.get("impression_count", 0)
                ),
            }
        elif resp.status_code == 429:
            log.warning("Rate limited on metrics fetch. Skipping.")
            return None
        else:
            log.error(f"Metrics fetch error {resp.status_code}: {resp.text}")
            return None
    except Exception as e:
        log.error(f"Metrics fetch failed: {e}")
        return None


# ---------------------------------------------------------------------------
# POSTING LOGIC
# ---------------------------------------------------------------------------
def get_posts_this_month() -> int:
    """Count posts made this calendar month (for free tier limit)."""
    rows = read_csv_rows(POSTED_CSV)
    now = utcnow()
    count = 0
    for r in rows:
        posted = r.get("posted_at", "")
        if posted:
            try:
                dt = datetime.fromisoformat(posted)
                if dt.year == now.year and dt.month == now.month:
                    count += 1
            except ValueError:
                pass
    return count


def select_next_batch(all_content: dict[str, list[dict]], max_per_account: int = 2) -> list[dict]:
    """
    Select next batch of content to post.
    Skips already-posted content (by hash).
    Returns list of {account, text, viral_text, image_prompt, source_file, content_hash}
    """
    posted_hashes = get_posted_hashes()
    batch = []

    for acct_key, items in all_content.items():
        niche = ACCOUNTS[acct_key]["niche"]
        selected = 0
        for item in items:
            if selected >= max_per_account:
                break
            h = content_hash(item["text"])
            if h in posted_hashes:
                continue

            # Skip meta-content (naming discussions, config, etc.)
            if is_meta_content(item["text"]):
                continue

            viral_text = rewrite_viral_hook(item["text"], niche)
            if len(viral_text) < 20:
                continue

            img_prompt = generate_image_prompt(niche, viral_text[:100])

            batch.append({
                "account": acct_key,
                "text": item["text"],
                "viral_text": viral_text,
                "image_prompt": img_prompt,
                "source_file": item["source_file"],
                "content_hash": h,
            })
            selected += 1

    return batch


def post_batch(batch: list[dict], creds: dict, dry_run: bool = False) -> int:
    """
    Post a batch of content to Twitter.
    Returns number of successful posts.
    """
    posts_this_month = get_posts_this_month()
    remaining = X_FREE_TIER_POST_LIMIT - posts_this_month
    if remaining <= 0 and not dry_run:
        log.warning(f"Monthly post limit reached ({posts_this_month}/{X_FREE_TIER_POST_LIMIT}). Skipping posts.")
        return 0

    success = 0
    ensure_csv(POSTED_CSV, POSTED_FIELDS)
    ensure_csv(PERFORMANCE_CSV, PERFORMANCE_FIELDS)

    for item in batch:
        if success >= remaining and not dry_run:
            log.warning("Approaching monthly limit. Stopping batch.")
            break

        acct = item["account"]
        text = item["viral_text"]
        handle = ACCOUNTS[acct]["handle"]

        if dry_run:
            print(f"\n{'='*60}")
            print(f"  ACCOUNT:  {handle} ({acct})")
            print(f"  NICHE:    {ACCOUNTS[acct]['niche']}")
            print(f"  SOURCE:   {item['source_file']}")
            print(f"  HASH:     {item['content_hash']}")
            print(f"  IMAGE:    {item['image_prompt'][:80]}...")
            print(f"  ORIGINAL: {item['text'][:120]}...")
            print(f"  VIRAL:    {text[:280]}")
            print(f"  CHARS:    {len(text)}/280")
            print(f"{'='*60}")
            success += 1
            continue

        api_creds = get_twitter_api_creds(acct, creds)
        if not api_creds:
            log.warning(f"No API credentials for {acct}. Skipping.")
            continue

        result = twitter_post_tweet(text, api_creds)
        if result:
            now = utcnow().isoformat()
            # Track in posted CSV
            append_csv_row(POSTED_CSV, POSTED_FIELDS, {
                "content_hash": item["content_hash"],
                "account": acct,
                "posted_at": now,
                "tweet_id": result["tweet_id"],
                "tweet_url": result["tweet_url"],
                "source_file": item["source_file"],
                "content_preview": text[:100],
            })
            # Initialize performance tracking row
            append_csv_row(PERFORMANCE_CSV, PERFORMANCE_FIELDS, {
                "post_id": result["tweet_id"],
                "account": acct,
                "platform": "twitter",
                "content_hash": item["content_hash"],
                "content_preview": text[:100],
                "full_text": text,
                "posted_at": now,
                "tweet_url": result["tweet_url"],
                "likes_1h": "", "likes_6h": "", "likes_24h": "", "likes_7d": "",
                "retweets_1h": "", "retweets_6h": "", "retweets_24h": "", "retweets_7d": "",
                "replies_1h": "", "replies_6h": "", "replies_24h": "", "replies_7d": "",
                "impressions_1h": "", "impressions_6h": "", "impressions_24h": "", "impressions_7d": "",
                "engagement_rate": "",
                "winner_score": "",
                "status": "POSTED",
                "last_checked": now,
                "source_file": item["source_file"],
            })
            success += 1

            # Rate limit courtesy: wait between posts
            time.sleep(random.uniform(3, 8))
        else:
            log.warning(f"Failed to post for {acct}")

    return success


# ---------------------------------------------------------------------------
# ENGAGEMENT CHECKING
# ---------------------------------------------------------------------------
def determine_check_bucket(posted_at_str: str) -> str | None:
    """
    Determine which time bucket to check based on posted_at.
    Returns: '1h', '6h', '24h', '7d' or None if too early or all buckets filled.
    """
    try:
        posted = datetime.fromisoformat(posted_at_str)
    except (ValueError, TypeError):
        return None

    elapsed = utcnow() - posted
    hours = elapsed.total_seconds() / 3600

    if hours >= 168:  # 7 days
        return "7d"
    elif hours >= 24:
        return "24h"
    elif hours >= 6:
        return "6h"
    elif hours >= 1:
        return "1h"
    return None


def check_engagement(creds: dict, quiet: bool = False) -> int:
    """
    Check engagement metrics for posted content.
    Updates CONTENT_PERFORMANCE.csv at appropriate time buckets.
    Returns number of posts checked.
    """
    rows = read_csv_rows(PERFORMANCE_CSV)
    if not rows:
        if not quiet:
            print("No posts to check. Post content first with --post.")
        return 0

    updated = 0
    reads_used = 0
    max_reads = 50  # conservative per run to stay under free tier

    for row in rows:
        if reads_used >= max_reads:
            log.info(f"Reached per-run read limit ({max_reads}). Stopping.")
            break

        post_id = row.get("post_id", "")
        acct = row.get("account", "")
        posted_at = row.get("posted_at", "")

        if not post_id or not acct:
            continue

        bucket = determine_check_bucket(posted_at)
        if not bucket:
            continue

        # Check if this bucket already has data
        likes_key = f"likes_{bucket}"
        if row.get(likes_key, ""):
            continue  # already checked this bucket

        api_creds = get_twitter_api_creds(acct, creds)
        if not api_creds:
            continue

        metrics = twitter_get_tweet_metrics(post_id, api_creds)
        if metrics:
            row[f"likes_{bucket}"] = str(metrics["likes"])
            row[f"retweets_{bucket}"] = str(metrics["retweets"])
            row[f"replies_{bucket}"] = str(metrics["replies"])
            row[f"impressions_{bucket}"] = str(metrics["impressions"])
            row["last_checked"] = utcnow().isoformat()

            # Calculate engagement rate if we have impressions at 7d
            if bucket == "7d" and metrics["impressions"] > 0:
                total_eng = metrics["likes"] + metrics["retweets"] + metrics["replies"]
                row["engagement_rate"] = f"{(total_eng / metrics['impressions']) * 100:.2f}"

            updated += 1
            reads_used += 1

            if not quiet:
                print(f"  [{acct}] {post_id}: {bucket} -> {metrics['likes']}L {metrics['retweets']}RT {metrics['replies']}RP {metrics['impressions']}imp")

            time.sleep(random.uniform(1, 3))

    # Write back
    if updated > 0:
        write_csv_rows(PERFORMANCE_CSV, PERFORMANCE_FIELDS, rows)
        if not quiet:
            print(f"\nUpdated metrics for {updated} posts.")

    return updated


# ---------------------------------------------------------------------------
# WINNER IDENTIFICATION
# ---------------------------------------------------------------------------
def calculate_algo_weighted_score(likes: int, retweets: int, replies: int,
                                   impressions: int, bookmarks: int = 0) -> float:
    """
    Calculate X algorithm-weighted engagement score.
    Uses confirmed 2026 X algorithm multipliers:
      Like=1x, RT=20x, Reply=13.5x, Profile Click=12x, Bookmark=10x
    Returns raw algo score (higher = more algorithmic reach).
    """
    w = X_ALGO_WEIGHTS
    return (
        likes * w["like"]
        + retweets * w["retweet"]
        + replies * w["reply"]
        + bookmarks * w["bookmark"]
    )


def check_cold_start_risk(account_key: str) -> dict:
    """
    Check if an account is at risk of TweepCred Cold Start Suppression.
    X suppresses accounts with <0.5% engagement on first 100 tweets.
    Returns: {at_risk: bool, engagement_rate: float, tweets_counted: int}
    """
    rows = read_csv_rows(PERFORMANCE_CSV)
    acct_rows = [r for r in rows if r.get("account") == account_key]

    if len(acct_rows) < 10:
        return {"at_risk": True, "engagement_rate": 0.0, "tweets_counted": len(acct_rows),
                "note": "Too few tweets to evaluate. Focus on reply guy strategy for early growth."}

    total_eng = 0
    total_imp = 0
    for r in acct_rows[:TWEEPCRED_MIN_TWEETS_FOR_EVAL]:
        likes = int(r.get("likes_7d", 0) or 0)
        rt = int(r.get("retweets_7d", 0) or 0)
        replies = int(r.get("replies_7d", 0) or 0)
        imp = int(r.get("impressions_7d", 0) or 0)
        total_eng += likes + rt + replies
        total_imp += imp

    rate = (total_eng / max(total_imp, 1))
    at_risk = rate < TWEEPCRED_COLD_START_THRESHOLD

    return {
        "at_risk": at_risk,
        "engagement_rate": round(rate * 100, 2),
        "tweets_counted": min(len(acct_rows), TWEEPCRED_MIN_TWEETS_FOR_EVAL),
        "note": "COLD START RISK: Focus on reply guy strategy" if at_risk else "Above threshold",
    }


def get_reply_targets(account_key: str) -> list[str]:
    """Get reply guy target handles for an account."""
    return REPLY_GUY_TARGETS.get(account_key, [])


def calculate_winner_scores() -> list[dict]:
    """
    Score each post 0-100 using X algorithm weights.
    Uses confirmed 2026 multipliers: RT=20x, Reply=13.5x, Bookmark=10x, Like=1x.
    Mark top 10% as WINNERS.
    Returns sorted list of scored posts.
    """
    rows = read_csv_rows(PERFORMANCE_CSV)
    if not rows:
        return []

    # Group by account and calculate averages
    account_metrics = {}
    for row in rows:
        acct = row.get("account", "")
        likes_7d = int(row.get("likes_7d", 0) or 0)
        rt_7d = int(row.get("retweets_7d", 0) or 0)
        replies_7d = int(row.get("replies_7d", 0) or 0)
        imp_7d = int(row.get("impressions_7d", 0) or 0)

        if acct not in account_metrics:
            account_metrics[acct] = {"likes": [], "rt": [], "replies": [], "imp": []}

        if likes_7d > 0 or rt_7d > 0:  # only count posts with data
            account_metrics[acct]["likes"].append(likes_7d)
            account_metrics[acct]["rt"].append(rt_7d)
            account_metrics[acct]["replies"].append(replies_7d)
            account_metrics[acct]["imp"].append(imp_7d)

    # Calculate averages
    account_avgs = {}
    for acct, m in account_metrics.items():
        account_avgs[acct] = {
            "avg_likes": sum(m["likes"]) / max(len(m["likes"]), 1),
            "avg_rt": sum(m["rt"]) / max(len(m["rt"]), 1),
            "avg_replies": sum(m["replies"]) / max(len(m["replies"]), 1),
            "avg_imp": sum(m["imp"]) / max(len(m["imp"]), 1),
        }

    # Score each post using X algorithm weights
    scored = []
    for row in rows:
        acct = row.get("account", "")
        likes_7d = int(row.get("likes_7d", 0) or 0)
        rt_7d = int(row.get("retweets_7d", 0) or 0)
        replies_7d = int(row.get("replies_7d", 0) or 0)
        imp_7d = int(row.get("impressions_7d", 0) or 0)

        avgs = account_avgs.get(acct, {"avg_likes": 1, "avg_rt": 1, "avg_replies": 1, "avg_imp": 1})

        # Algorithm-weighted scoring:
        # RT and replies are worth FAR more than likes in X's algorithm
        # Weight the score components proportional to algo multipliers
        def ratio_score(val, avg, weight=25):
            if avg == 0:
                return min(weight, val * 5)  # raw score if no average
            ratio = val / avg
            return min(weight, ratio * (weight / 2))

        # Weights now reflect X algorithm: RT(20x) > Reply(13.5x) > Like(1x)
        score = (
            ratio_score(likes_7d, avgs["avg_likes"], 10)      # Likes = least valuable
            + ratio_score(rt_7d, avgs["avg_rt"], 35)           # RT = most valuable signal
            + ratio_score(replies_7d, avgs["avg_replies"], 35) # Replies = 2nd most valuable
            + ratio_score(imp_7d, avgs["avg_imp"], 20)
        )
        score = min(100, round(score, 1))

        row["winner_score"] = str(score)
        scored.append(row)

    # Sort by score descending
    scored.sort(key=lambda x: float(x.get("winner_score", 0) or 0), reverse=True)

    # Mark top 10% as WINNERS
    if scored:
        cutoff_idx = max(1, len(scored) // 10)
        for i, row in enumerate(scored):
            if i < cutoff_idx and float(row.get("winner_score", 0) or 0) > 20:
                row["status"] = "WINNER"
            elif float(row.get("winner_score", 0) or 0) > 50:
                row["status"] = "BOOST_CANDIDATE"
            elif row.get("status") != "POSTED":
                pass  # keep existing status

    # Write back performance CSV
    write_csv_rows(PERFORMANCE_CSV, PERFORMANCE_FIELDS, scored)

    return scored


def generate_winners_report(scored: list[dict]) -> int:
    """
    Generate CONTENT_WINNERS.csv from scored posts.
    Returns number of winners.
    """
    winners = [r for r in scored if r.get("status") in ("WINNER", "BOOST_CANDIDATE")]

    winner_rows = []
    for w in winners:
        niche = ACCOUNTS.get(w.get("account", ""), {}).get("niche", "")
        benchmark = NICHE_AD_BENCHMARKS.get(niche, {"cpc": 1.0})
        # Suggested boost budget: $5-50 based on score
        score = float(w.get("winner_score", 0) or 0)
        boost = round(max(5, min(50, score * 0.5)), 0)

        winner_rows.append({
            "post_id": w.get("post_id", ""),
            "account": w.get("account", ""),
            "platform": "twitter",
            "content_preview": w.get("content_preview", ""),
            "posted_at": w.get("posted_at", ""),
            "likes_7d": w.get("likes_7d", ""),
            "retweets_7d": w.get("retweets_7d", ""),
            "replies_7d": w.get("replies_7d", ""),
            "impressions_7d": w.get("impressions_7d", ""),
            "engagement_rate": w.get("engagement_rate", ""),
            "winner_score": w.get("winner_score", ""),
            "status": w.get("status", ""),
            "boost_budget": f"${int(boost)}",
            "tweet_url": w.get("tweet_url", ""),
        })

    write_csv_rows(WINNERS_CSV, WINNERS_FIELDS, winner_rows)
    return len(winner_rows)


def show_winners(quiet: bool = False):
    """Display winner posts."""
    scored = calculate_winner_scores()
    num = generate_winners_report(scored)

    if quiet:
        log.info(f"Winners identified: {num}")
        return

    winners = [r for r in scored if r.get("status") in ("WINNER", "BOOST_CANDIDATE")]
    if not winners:
        print("\nNo winners identified yet. Need 7+ days of post data.")
        print("Run --check to gather engagement metrics first.")
        return

    print(f"\n{'='*70}")
    print(f"  CONTENT WINNERS ({num} posts)")
    print(f"{'='*70}\n")

    for w in winners[:20]:
        acct = w.get("account", "")
        handle = ACCOUNTS.get(acct, {}).get("handle", acct)
        score = w.get("winner_score", "0")
        status = w.get("status", "")
        likes = w.get("likes_7d", "0")
        rt = w.get("retweets_7d", "0")
        replies = w.get("replies_7d", "0")
        imp = w.get("impressions_7d", "0")
        eng = w.get("engagement_rate", "0")
        preview = w.get("content_preview", "")[:80]

        tag = "***" if status == "WINNER" else " * "
        print(f"  {tag} Score: {score:>5} | {handle:18s} | {likes}L {rt}RT {replies}RP {imp}imp | ER:{eng}%")
        print(f"      {preview}")
        print(f"      {w.get('tweet_url', '')}")
        print()

    print(f"  Full report: {WINNERS_CSV}")
    print()


# ---------------------------------------------------------------------------
# AD BOOST RECOMMENDATIONS
# ---------------------------------------------------------------------------
def generate_ad_recommendations():
    """
    Generate OPS/AD_BOOST_RECOMMENDATIONS.md with specific
    budget allocations and targeting for winner content.
    """
    winners = read_csv_rows(WINNERS_CSV)
    if not winners:
        print("No winners to generate boost recommendations for.")
        print("Run --winners first to identify winning content.")
        return

    now = utcnow().strftime("%Y-%m-%d %H:%M UTC")
    total_budget = 0

    lines = [
        f"# Ad Boost Recommendations",
        f"",
        f"Generated: {now}",
        f"Source: LEDGER/CONTENT_WINNERS.csv",
        f"",
        f"## Summary",
        f"",
        f"| Metric | Value |",
        f"|--------|-------|",
        f"| Total winners | {len(winners)} |",
    ]

    recs = []
    for w in winners:
        acct = w.get("account", "")
        niche = ACCOUNTS.get(acct, {}).get("niche", "unknown")
        handle = ACCOUNTS.get(acct, {}).get("handle", acct)
        benchmark = NICHE_AD_BENCHMARKS.get(niche, {"cpc": 1.0, "cpm": 7.0, "best_platform": "X Ads"})
        score = float(w.get("winner_score", 0) or 0)
        budget = max(5, min(50, round(score * 0.5)))
        total_budget += budget

        est_clicks = round(budget / benchmark["cpc"])
        est_impressions = round((budget / benchmark["cpm"]) * 1000)

        recs.append({
            "account": acct,
            "handle": handle,
            "niche": niche,
            "score": score,
            "budget": budget,
            "platform": benchmark["best_platform"],
            "cpc": benchmark["cpc"],
            "cpm": benchmark["cpm"],
            "est_clicks": est_clicks,
            "est_impressions": est_impressions,
            "content_preview": w.get("content_preview", "")[:80],
            "tweet_url": w.get("tweet_url", ""),
            "engagement_rate": w.get("engagement_rate", ""),
        })

    lines.extend([
        f"| Total boost budget | ${total_budget} |",
        f"| Avg budget per post | ${total_budget // max(len(winners), 1)} |",
        f"",
        f"## Recommendations by Account",
        f"",
    ])

    # Group by account
    by_account = {}
    for r in recs:
        by_account.setdefault(r["account"], []).append(r)

    for acct, items in sorted(by_account.items()):
        info = ACCOUNTS.get(acct, {})
        acct_budget = sum(r["budget"] for r in items)
        lines.append(f"### {info.get('handle', acct)} ({info.get('niche', '')})")
        lines.append(f"")
        lines.append(f"Budget: ${acct_budget} | Platform: {items[0]['platform']} | Est CPC: ${items[0]['cpc']:.2f}")
        lines.append(f"")

        for r in items:
            lines.append(f"**Score {r['score']}** | Budget ${r['budget']} | Est {r['est_clicks']} clicks / {r['est_impressions']:,} impressions")
            lines.append(f"")
            lines.append(f"> {r['content_preview']}")
            lines.append(f"")
            if r["tweet_url"]:
                lines.append(f"URL: {r['tweet_url']}")
                lines.append(f"")

        # Targeting suggestions by niche
        targeting = get_targeting_suggestions(info.get("niche", ""))
        lines.append(f"**Targeting:**")
        lines.append(f"")
        for t in targeting:
            lines.append(f"- {t}")
        lines.append(f"")

    lines.extend([
        f"## Budget Tiers",
        f"",
        f"| Tier | Budget | Strategy |",
        f"|------|--------|----------|",
        f"| Minimal | $5-10/post | Boost top 3 posts only, X Ads promote button |",
        f"| Standard | $10-25/post | Boost top 10 posts, A/B test 2 audiences per post |",
        f"| Aggressive | $25-50/post | Boost all winners, multi-platform (X + Meta), retargeting |",
        f"",
        f"## Execution Steps",
        f"",
        f"1. Open X Ads Manager: https://ads.x.com/",
        f"2. Create Engagement campaign for each winner post",
        f"3. Set daily budget to recommended amount / 3 (run for 3 days)",
        f"4. Target audience per niche recommendations above",
        f"5. After 48h: kill ads with CPC > 2x benchmark, double budget on CPC < benchmark",
        f"6. Track conversions (newsletter signups, link clicks, follows) in LEDGER/AD_PERFORMANCE.csv",
        f"",
        f"## Meta Ads Alternative",
        f"",
        f"For niches with lower X engagement (fitness, faith, beauty):",
        f"1. Repurpose tweet as Instagram Reel script or carousel",
        f"2. Boost via Meta Ads Manager: https://adsmanager.facebook.com/",
        f"3. Target lookalike of existing followers",
        f"4. Set $5-10/day for 3 days, optimize for engagement",
        f"",
    ])

    OPS_DIR.mkdir(parents=True, exist_ok=True)
    AD_BOOST_MD.write_text("\n".join(lines), encoding="utf-8")
    print(f"\nAd boost recommendations written to: {AD_BOOST_MD}")
    print(f"Total suggested budget: ${total_budget}")
    print(f"Posts to boost: {len(recs)}")


def get_targeting_suggestions(niche: str) -> list[str]:
    """Return targeting suggestions for X Ads / Meta Ads by niche."""
    suggestions = {
        "tech/solopreneur": [
            "Interests: SaaS, indie hacking, startup, coding, automation",
            "Follow lookalikes: @levelsio, @paborojopx, @marc_louvion",
            "Keywords: solopreneur, bootstrapped, build in public, ship fast",
            "Age: 22-45, Male 70%",
        ],
        "growth/marketing": [
            "Interests: digital marketing, growth hacking, SEO, content marketing",
            "Follow lookalikes: @aaborojopx, @codyschneiderxx, @harrydry",
            "Keywords: growth, marketing, conversion, leads, funnel",
            "Age: 25-45, Both genders",
        ],
        "cold outreach": [
            "Interests: B2B sales, cold email, lead generation, outbound",
            "Follow lookalikes: @seanb2b, @alexberman, @patrickdang",
            "Keywords: cold email, outreach, sales, leads, B2B",
            "Age: 25-50, Male 60%",
        ],
        "clipping/content": [
            "Interests: content creation, video editing, YouTube, TikTok",
            "Follow lookalikes: @aliabdaal, @paddy_galloway",
            "Keywords: content creator, clips, viral, editing, shorts",
            "Age: 18-35, Both genders",
        ],
        "tools/saas": [
            "Interests: productivity tools, SaaS, software, automation",
            "Follow lookalikes: @ProductHunt, @BetaList",
            "Keywords: tools, software, productivity, automation, app",
            "Age: 22-45, Male 65%",
        ],
        "fitness/self-improvement": [
            "Interests: fitness, gym, self-improvement, health, motivation",
            "Follow lookalikes: @HubermanLab, @drchatterjee, @foundmyfitness",
            "Keywords: workout, gains, discipline, health, muscle",
            "Age: 18-40, Male 65%",
        ],
        "esoteric/philosophy": [
            "Interests: philosophy, spirituality, stoicism, consciousness",
            "Follow lookalikes: @naval, @TheStoicEmperor",
            "Keywords: consciousness, reality, philosophy, void, truth",
            "Age: 20-45, Male 60%",
        ],
        "faith/prayer": [
            "Interests: faith, prayer, Christianity, Islam, spirituality",
            "Follow lookalikes: @PrayerNow, @MuslimPro, @DailyDevotionHQ",
            "Keywords: prayer, faith, devotion, spiritual, worship",
            "Age: 20-55, Both genders",
        ],
        "building-in-public": [
            "Interests: startups, indie hackers, build in public, shipping",
            "Follow lookalikes: @levelsio, @marc_louvion, @dannypostmaa",
            "Keywords: shipped, build, launch, MVP, indie",
            "Age: 22-40, Male 70%",
        ],
        "aesthetic/visual": [
            "Interests: photography, visual art, design, aesthetics",
            "Keywords: aesthetic, visual, photography, minimal, mood",
            "Age: 18-35, Both genders",
        ],
        "beauty/curated": [
            "Interests: beauty, skincare, makeup, self-care, wellness",
            "Keywords: beauty, skincare, routine, glow, curated",
            "Age: 18-40, Female 75%",
        ],
        "ambient/chill": [
            "Interests: lo-fi, ambient, chill, relaxation, study music",
            "Keywords: chill, ambient, lo-fi, vibes, calm",
            "Age: 18-35, Both genders",
        ],
    }
    return suggestions.get(niche, [
        "Interests: general audience",
        "Broad targeting recommended. Test and refine.",
    ])


# ---------------------------------------------------------------------------
# SCHEDULE DISPLAY
# ---------------------------------------------------------------------------
def show_schedule():
    """Display upcoming post schedule."""
    all_content = load_all_content()
    posted_hashes = get_posted_hashes()
    now = utcnow()

    print(f"\n{'='*70}")
    print(f"  UPCOMING POST SCHEDULE")
    print(f"  Current time: {now.strftime('%Y-%m-%d %H:%M UTC')}")
    print(f"{'='*70}\n")

    posts_month = get_posts_this_month()
    remaining = X_FREE_TIER_POST_LIMIT - posts_month
    print(f"  Monthly posts: {posts_month}/{X_FREE_TIER_POST_LIMIT} (remaining: {remaining})\n")

    for acct_key in sorted(ACCOUNTS.keys()):
        info = ACCOUNTS[acct_key]
        items = all_content.get(acct_key, [])
        unposted = [it for it in items if content_hash(it["text"]) not in posted_hashes]
        slots = POSTING_SCHEDULE.get(acct_key, [])

        print(f"  {info['handle']:20s} | {len(unposted):>3} queued | {len(items):>3} total | {len(slots)} slots/day")
        for h, m in slots:
            slot_time = now.replace(hour=h, minute=m, second=0, microsecond=0)
            if slot_time < now:
                slot_time += timedelta(days=1)
            eta = slot_time - now
            eta_str = f"{int(eta.total_seconds() // 3600)}h {int((eta.total_seconds() % 3600) // 60)}m"
            print(f"    -> {slot_time.strftime('%H:%M UTC')} (in {eta_str})")
        print()

    if remaining <= 10:
        print(f"  WARNING: Only {remaining} posts remaining this month (free tier).")
        print(f"  Consider upgrading to X API Basic ($100/mo) for 3,000 posts/mo.")
    print()


# ---------------------------------------------------------------------------
# STATUS OVERVIEW
# ---------------------------------------------------------------------------
def show_status():
    """Quick status overview."""
    all_content = load_all_content()
    posted_hashes = get_posted_hashes()
    perf_rows = read_csv_rows(PERFORMANCE_CSV)
    winner_rows = read_csv_rows(WINNERS_CSV)
    posts_month = get_posts_this_month()

    total_content = sum(len(v) for v in all_content.values())
    total_unposted = sum(
        len([it for it in v if content_hash(it["text"]) not in posted_hashes])
        for v in all_content.values()
    )

    print(f"\n{'='*50}")
    print(f"  AUTO CONTENT POSTER STATUS")
    print(f"{'='*50}\n")
    print(f"  Content loaded:    {total_content}")
    print(f"  Already posted:    {len(posted_hashes)}")
    print(f"  Queued (unposted): {total_unposted}")
    print(f"  Posts this month:  {posts_month}/{X_FREE_TIER_POST_LIMIT}")
    print(f"  Tracked metrics:   {len(perf_rows)}")
    print(f"  Winners found:     {len(winner_rows)}")
    print()

    print(f"  By account:")
    for acct_key in sorted(ACCOUNTS.keys()):
        info = ACCOUNTS[acct_key]
        items = all_content.get(acct_key, [])
        unposted = len([it for it in items if content_hash(it["text"]) not in posted_hashes])
        total = len(items)
        bar = "#" * min(30, total) + "." * max(0, 30 - total)
        print(f"    {info['handle']:20s} {total:>4} total | {unposted:>4} queued | [{bar[:20]}]")

    print()

    # Credential check
    creds = load_credentials()
    configured = sum(1 for acct in ACCOUNTS if get_twitter_api_creds(acct, creds))
    print(f"  API credentials:   {configured}/{len(ACCOUNTS)} accounts configured")
    if configured == 0:
        print(f"  -> Add Twitter API keys to {CREDENTIALS_FILE}")
        print(f"     TWITTER_{{ACCOUNT}}_API_KEY=...")
        print(f"     TWITTER_{{ACCOUNT}}_API_SECRET=...")
        print(f"     TWITTER_{{ACCOUNT}}_ACCESS_TOKEN=...")
        print(f"     TWITTER_{{ACCOUNT}}_ACCESS_TOKEN_SECRET=...")
    print()


# ---------------------------------------------------------------------------
# REWRITE PREVIEW
# ---------------------------------------------------------------------------
def preview_rewrites():
    """Preview viral hook rewrites for all queued content."""
    all_content = load_all_content()
    posted_hashes = get_posted_hashes()
    count = 0

    for acct_key, items in all_content.items():
        niche = ACCOUNTS[acct_key]["niche"]
        handle = ACCOUNTS[acct_key]["handle"]
        for item in items[:3]:  # preview first 3 per account
            h = content_hash(item["text"])
            if h in posted_hashes:
                continue

            original = item["text"][:200]
            viral = rewrite_viral_hook(item["text"], niche)
            img = generate_image_prompt(niche, viral[:100])

            print(f"\n{'='*60}")
            print(f"  {handle} ({niche})")
            print(f"  Source: {item['source_file']}")
            print(f"  ORIGINAL: {original}...")
            print(f"  VIRAL:    {viral}")
            print(f"  CHARS:    {len(viral)}/280")
            print(f"  IMAGE:    {img[:80]}...")
            count += 1

    print(f"\n  Previewed {count} rewrites.\n")


# ---------------------------------------------------------------------------
# CRON MODE
# ---------------------------------------------------------------------------
def run_cron(creds: dict):
    """
    Quiet mode for crontab. Posts + checks + flags winners.
    Minimal output, logs to file.
    """
    log.info("=== CRON RUN START ===")

    # 1. Post next batch
    all_content = load_all_content()
    batch = select_next_batch(all_content, max_per_account=1)
    if batch:
        posted = post_batch(batch, creds, dry_run=False)
        log.info(f"Posted {posted} items.")
    else:
        log.info("No new content to post.")

    # 2. Check engagement
    checked = check_engagement(creds, quiet=True)
    log.info(f"Checked metrics for {checked} posts.")

    # 3. Score winners (weekly-ish: only on Mondays or if 7+ days of data)
    now = utcnow()
    if now.weekday() == 0:  # Monday
        scored = calculate_winner_scores()
        winners = generate_winners_report(scored)
        log.info(f"Winner scoring complete. {winners} winners identified.")

    log.info("=== CRON RUN END ===")


# ---------------------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(
        description="PRINTMAXX Auto Content Poster - post, track, identify winners, recommend boosts",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 AUTOMATIONS/auto_content_poster.py --status
  python3 AUTOMATIONS/auto_content_poster.py --post --dry-run
  python3 AUTOMATIONS/auto_content_poster.py --post
  python3 AUTOMATIONS/auto_content_poster.py --check
  python3 AUTOMATIONS/auto_content_poster.py --winners
  python3 AUTOMATIONS/auto_content_poster.py --boost
  python3 AUTOMATIONS/auto_content_poster.py --schedule
  python3 AUTOMATIONS/auto_content_poster.py --rewrite
  python3 AUTOMATIONS/auto_content_poster.py --cron
        """,
    )
    parser.add_argument("--post", action="store_true", help="Post next batch of content")
    parser.add_argument("--check", action="store_true", help="Check engagement on posted content")
    parser.add_argument("--winners", action="store_true", help="Show winners from last 7 days")
    parser.add_argument("--boost", action="store_true", help="Show ad boost recommendations")
    parser.add_argument("--schedule", action="store_true", help="Show upcoming post schedule")
    parser.add_argument("--dry-run", action="store_true", help="Preview without posting")
    parser.add_argument("--cron", action="store_true", help="Quiet mode for crontab")
    parser.add_argument("--rewrite", action="store_true", help="Preview viral hook rewrites")
    parser.add_argument("--status", action="store_true", help="Quick status overview")
    parser.add_argument("--creds", action="store_true", help="Check credential status")
    parser.add_argument("--max-per-account", type=int, default=2, help="Max posts per account per batch (default: 2)")
    parser.add_argument("--reply-targets", action="store_true", help="Show reply guy targets for all accounts")
    parser.add_argument("--cold-start", action="store_true", help="Check TweepCred cold start risk for all accounts")
    parser.add_argument("--algo-score", action="store_true", help="Show X algorithm-weighted scores for posted content")

    args = parser.parse_args()

    # Default to --status if no args
    if not any([args.post, args.check, args.winners, args.boost,
                args.schedule, args.dry_run, args.cron, args.rewrite,
                args.status, args.creds, args.reply_targets, args.cold_start,
                args.algo_score]):
        args.status = True

    if args.cron:
        setup_logger(quiet=True)

    # Ensure output directories exist
    LEDGER_DIR.mkdir(parents=True, exist_ok=True)
    OPS_DIR.mkdir(parents=True, exist_ok=True)
    ensure_csv(PERFORMANCE_CSV, PERFORMANCE_FIELDS)
    ensure_csv(POSTED_CSV, POSTED_FIELDS)

    creds = load_credentials()

    if args.creds:
        check_credentials_status(creds)
        return

    if args.reply_targets:
        print(f"\n{'='*70}")
        print(f"  REPLY GUY TARGETS (reply within {REPLY_WINDOW_MINUTES} min = 30x visibility)")
        print(f"  X Algorithm: Like=1x, RT=20x, Reply=13.5x, Bookmark=10x")
        print(f"  Author-engaged reply = +75 weight (150x a like)")
        print(f"{'='*70}\n")
        for acct_key in sorted(ACCOUNTS.keys()):
            handle = ACCOUNTS[acct_key]["handle"]
            targets = get_reply_targets(acct_key)
            niche = ACCOUNTS[acct_key]["niche"]
            print(f"  {handle:20s} ({niche})")
            for t in targets:
                print(f"    -> {t}")
            print()
        print(f"  Full target lists: OPS/REPLY_GUY_TARGET_LISTS.md")
        print(f"  Daily target: {REPLIES_PER_DAY_0_1K} replies/day (0-1K followers)")
        print()
        return

    if args.cold_start:
        print(f"\n{'='*70}")
        print(f"  TWEEPCRED COLD START RISK CHECK")
        print(f"  X suppresses accounts with <{TWEEPCRED_COLD_START_THRESHOLD*100}% engagement on first {TWEEPCRED_MIN_TWEETS_FOR_EVAL} tweets")
        print(f"{'='*70}\n")
        for acct_key in sorted(ACCOUNTS.keys()):
            handle = ACCOUNTS[acct_key]["handle"]
            result = check_cold_start_risk(acct_key)
            risk = "AT RISK" if result["at_risk"] else "OK"
            symbol = "-" if result["at_risk"] else "+"
            print(f"  [{symbol}] {handle:20s} ER: {result['engagement_rate']}% | Tweets: {result['tweets_counted']} | {risk}")
            if result["at_risk"]:
                targets = get_reply_targets(acct_key)[:3]
                print(f"      -> Focus: reply guy strategy targeting {', '.join(targets)}")
        print()
        return

    if args.algo_score:
        rows = read_csv_rows(PERFORMANCE_CSV)
        if not rows:
            print("No posts tracked yet. Post content first with --post.")
            return
        print(f"\n{'='*70}")
        print(f"  X ALGORITHM-WEIGHTED SCORES")
        print(f"  Weights: Like=1x, RT=20x, Reply=13.5x, Bookmark=10x")
        print(f"{'='*70}\n")
        scored_rows = []
        for r in rows:
            likes = int(r.get("likes_7d", 0) or 0)
            rt = int(r.get("retweets_7d", 0) or 0)
            replies = int(r.get("replies_7d", 0) or 0)
            algo = calculate_algo_weighted_score(likes, rt, replies, int(r.get("impressions_7d", 0) or 0))
            scored_rows.append((algo, r))
        scored_rows.sort(key=lambda x: x[0], reverse=True)
        for algo, r in scored_rows[:20]:
            acct = r.get("account", "")
            handle = ACCOUNTS.get(acct, {}).get("handle", acct)
            preview = r.get("content_preview", "")[:60]
            likes = r.get("likes_7d", "0")
            rt = r.get("retweets_7d", "0")
            rp = r.get("replies_7d", "0")
            print(f"  Algo:{algo:>8.0f} | {handle:18s} | {likes}L {rt}RT {rp}RP | {preview}")
        print()
        return

    if args.status:
        show_status()
        return

    if args.rewrite:
        preview_rewrites()
        return

    if args.schedule:
        show_schedule()
        return

    if args.post or args.dry_run:
        all_content = load_all_content()
        batch = select_next_batch(all_content, max_per_account=args.max_per_account)

        if not batch:
            print("No new content to post. All content has been posted already.")
            return

        is_dry = args.dry_run or (args.post and args.dry_run)
        if args.dry_run and not args.post:
            is_dry = True

        if is_dry:
            print(f"\n=== DRY RUN (preview only, nothing posted) ===")
            print(f"Batch size: {len(batch)} posts\n")

        posted = post_batch(batch, creds, dry_run=is_dry)
        print(f"\n{'Previewed' if is_dry else 'Posted'}: {posted}/{len(batch)} items.")

        if not is_dry:
            print(f"Tracked in: {POSTED_CSV}")
            print(f"Performance: {PERFORMANCE_CSV}")
        return

    if args.check:
        checked = check_engagement(creds)
        if checked == 0:
            print("No posts needed checking. Post content first or wait for check intervals.")
        return

    if args.winners:
        show_winners()
        return

    if args.boost:
        # Generate winners first if needed
        scored = calculate_winner_scores()
        generate_winners_report(scored)
        generate_ad_recommendations()
        return

    if args.cron:
        run_cron(creds)
        return


if __name__ == "__main__":
    main()
