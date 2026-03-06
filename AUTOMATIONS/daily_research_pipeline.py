#!/usr/bin/env python3
"""
DAILY RESEARCH PIPELINE — Master orchestrator for daily alpha extraction
=========================================================================
Chains: Scrape → Extract Alpha → Filter → Repurpose Content → Log

Runs automatically via cron. User NEVER needs to manually trigger scrapers.

Pipeline stages:
  1. SCRAPE:   Twitter (Brave cookies) + Reddit (JSON API) + bookmarks
  2. EXTRACT:  Parse scraped JSON → structured alpha entries
  3. FILTER:   Score 0-100, auto-approve HIGH, flag MEDIUM for review
  4. REPURPOSE: Generate niche content from approved alpha
  5. LOG:      Append to ALPHA_STAGING.csv + generate daily digest

Usage:
    python3 daily_research_pipeline.py --full          # Full pipeline (scrape + extract + filter + repurpose)
    python3 daily_research_pipeline.py --scrape-only    # Just run scrapers
    python3 daily_research_pipeline.py --extract-only   # Process existing scrape data
    python3 daily_research_pipeline.py --repurpose      # Generate content from approved alpha
    python3 daily_research_pipeline.py --status          # Show pipeline status
    python3 daily_research_pipeline.py --cron            # Lightweight daily cron mode (skip if already ran today)

Cron entry (add to crontab):
    0 6 * * * cd /Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt && /Library/Frameworks/Python.framework/Versions/3.12/bin/python3 AUTOMATIONS/daily_research_pipeline.py --full >> AUTOMATIONS/logs/daily_research_pipeline.log 2>&1
"""

import argparse
import csv
import json
import os
import re
import subprocess
import sys
import time
import hashlib
import logging
from datetime import datetime, timedelta
from pathlib import Path

# ─── Paths (auto-detected from script location) ─────────────
PROJECT_DIR = Path(__file__).resolve().parent.parent
AUTOMATIONS = PROJECT_DIR / "AUTOMATIONS"
LEDGER = PROJECT_DIR / "LEDGER"
CONTENT = PROJECT_DIR / "CONTENT"
OPS = PROJECT_DIR / "OPS"

ALPHA_STAGING = LEDGER / "ALPHA_STAGING.csv"
HIGH_SIGNAL_SOURCES = LEDGER / "HIGH_SIGNAL_SOURCES.csv"

# Scraper outputs
TWITTER_OUTPUT = AUTOMATIONS / "twitter_scraper_output"
REDDIT_OUTPUT = AUTOMATIONS / "reddit_scraper_output"

# Pipeline outputs
PIPELINE_DIR = AUTOMATIONS / "research_pipeline_output"
PIPELINE_DIR.mkdir(exist_ok=True)
CONTENT_OUTPUT = CONTENT / "social" / "auto_generated"
CONTENT_OUTPUT.mkdir(parents=True, exist_ok=True)

# Lock + state
LOCK_FILE = AUTOMATIONS / ".daily_research_pipeline.lock"
STATE_FILE = PIPELINE_DIR / "pipeline_state.json"
LOG_DIR = AUTOMATIONS / "logs"
LOG_DIR.mkdir(exist_ok=True)

PYTHON = "/Library/Frameworks/Python.framework/Versions/3.12/bin/python3"

# Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(LOG_DIR / "daily_research_pipeline.log")
    ]
)
log = logging.getLogger("research_pipeline")


# ─── State Management ────────────────────────────────────────
def load_state():
    if STATE_FILE.exists():
        with open(STATE_FILE) as f:
            return json.load(f)
    return {"last_run": None, "runs": [], "total_alpha": 0, "total_content": 0}

def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2, default=str)

def already_ran_today(state):
    if not state.get("last_run"):
        return False
    last = datetime.fromisoformat(state["last_run"])
    return last.date() == datetime.now().date()


# ─── Lock File ─────────────────────────────────────────────
def acquire_lock():
    if LOCK_FILE.exists():
        try:
            pid = int(LOCK_FILE.read_text().strip())
            # Check if process still running
            os.kill(pid, 0)
            log.warning(f"Pipeline already running (PID {pid})")
            return False
        except (ProcessLookupError, ValueError):
            LOCK_FILE.unlink()
    LOCK_FILE.write_text(str(os.getpid()))
    return True

def release_lock():
    if LOCK_FILE.exists():
        LOCK_FILE.unlink()


# ─── Stage 1: SCRAPE ─────────────────────────────────────────
def run_scrapers():
    """Run Twitter (Brave cookies) + Reddit scrapers in parallel-ish fashion"""
    log.info("=" * 60)
    log.info("STAGE 1: SCRAPING")
    log.info("=" * 60)

    results = {"twitter": None, "reddit": None, "bookmarks": None}

    # 1a. Twitter high-signal accounts + bookmarks (uses Brave cookies)
    twitter_script = AUTOMATIONS / "twitter_alpha_scraper.py"
    if twitter_script.exists():
        log.info("Running Twitter alpha scraper (Brave cookies, all accounts + bookmarks)...")
        try:
            proc = subprocess.run(
                [PYTHON, str(twitter_script), "--all"],
                capture_output=True, text=True, timeout=600,
                cwd=str(PROJECT_DIR)
            )
            results["twitter"] = "OK" if proc.returncode == 0 else f"FAIL: {proc.stderr[:200]}"
            log.info(f"Twitter scraper: {results['twitter']}")
        except subprocess.TimeoutExpired:
            results["twitter"] = "TIMEOUT (10m)"
            log.warning("Twitter scraper timed out after 10 minutes")
        except Exception as e:
            results["twitter"] = f"ERROR: {e}"
            log.error(f"Twitter scraper error: {e}")
    else:
        results["twitter"] = "MISSING"
        log.warning(f"Twitter scraper not found at {twitter_script}")

    # 1b. Reddit scraper (JSON API, no auth needed)
    reddit_script = AUTOMATIONS / "background_reddit_scraper.py"
    if reddit_script.exists():
        log.info("Running Reddit scraper (all monitored subreddits)...")
        try:
            proc = subprocess.run(
                [PYTHON, str(reddit_script), "--full"],
                capture_output=True, text=True, timeout=300,
                cwd=str(PROJECT_DIR)
            )
            results["reddit"] = "OK" if proc.returncode == 0 else f"FAIL: {proc.stderr[:200]}"
            log.info(f"Reddit scraper: {results['reddit']}")
        except subprocess.TimeoutExpired:
            results["reddit"] = "TIMEOUT (5m)"
            log.warning("Reddit scraper timed out after 5 minutes")
        except Exception as e:
            results["reddit"] = f"ERROR: {e}"
            log.error(f"Reddit scraper error: {e}")
    else:
        # Fallback to alternate reddit scrapers
        for alt in ["reddit_deep_scraper.py", "enhanced_reddit_scraper.py", "browser_scraper_daily.py"]:
            alt_path = AUTOMATIONS / alt
            if alt_path.exists():
                log.info(f"Using fallback Reddit scraper: {alt}")
                try:
                    proc = subprocess.run(
                        [PYTHON, str(alt_path), "--reddit" if "browser" in alt else "--scrape"],
                        capture_output=True, text=True, timeout=300,
                        cwd=str(PROJECT_DIR)
                    )
                    results["reddit"] = f"OK (via {alt})" if proc.returncode == 0 else f"FAIL"
                    break
                except Exception:
                    continue

    log.info(f"Scrape results: {results}")
    return results


# ─── Stage 2: EXTRACT ─────────────────────────────────────────
def extract_alpha():
    """Parse scraped JSON files → structured alpha entries"""
    log.info("=" * 60)
    log.info("STAGE 2: EXTRACTING ALPHA")
    log.info("=" * 60)

    alpha_entries = []

    # 2a. Process Twitter scrape output
    alpha_entries.extend(_extract_twitter_alpha())

    # 2b. Process Reddit scrape output
    alpha_entries.extend(_extract_reddit_alpha())

    log.info(f"Extracted {len(alpha_entries)} raw alpha entries")
    return alpha_entries


def _extract_twitter_alpha():
    """Extract actionable alpha from Twitter scrape JSONs"""
    entries = []
    if not TWITTER_OUTPUT.exists():
        return entries

    # Find most recent scrape files (last 24 hours)
    cutoff = datetime.now() - timedelta(days=14)
    for f in sorted(TWITTER_OUTPUT.glob("*.json"), key=lambda x: x.stat().st_mtime, reverse=True):
        mtime = datetime.fromtimestamp(f.stat().st_mtime)
        if mtime < cutoff:
            continue

        try:
            data = json.loads(f.read_text())
        except (json.JSONDecodeError, UnicodeDecodeError):
            continue

        if isinstance(data, list):
            tweets = data
        elif isinstance(data, dict):
            tweets = data.get("tweets", data.get("results", []))
            if not tweets and isinstance(data, dict):
                # Might be a single account scrape
                for key, val in data.items():
                    if isinstance(val, list):
                        tweets = val
                        break
        else:
            continue

        for tweet in tweets:
            if not isinstance(tweet, dict):
                continue
            text = tweet.get("text", tweet.get("content", ""))
            if not text or len(text) < 30:
                continue

            # Score the tweet for alpha potential
            score = _score_tweet(text, tweet)
            if score < 20:
                continue

            source = tweet.get("author", tweet.get("username", tweet.get("handle", "unknown")))
            url = tweet.get("url", tweet.get("tweet_url", ""))
            likes = tweet.get("likes", tweet.get("like_count", 0))
            retweets = tweet.get("retweets", tweet.get("retweet_count", 0))

            entries.append({
                "source": f"@{source}" if source and not source.startswith("@") else source,
                "text": text[:500],
                "url": url,
                "platform": "twitter",
                "likes": likes,
                "retweets": retweets,
                "alpha_score": score,
                "scraped_at": datetime.now().isoformat(),
                "file_source": f.name
            })

    log.info(f"Extracted {len(entries)} tweets with alpha potential")
    return entries


def _extract_reddit_alpha():
    """Extract actionable alpha from Reddit scrape JSONs"""
    entries = []
    if not REDDIT_OUTPUT.exists():
        return entries

    cutoff = datetime.now() - timedelta(days=14)
    for f in sorted(REDDIT_OUTPUT.glob("reddit_*.json"), key=lambda x: x.stat().st_mtime, reverse=True):
        mtime = datetime.fromtimestamp(f.stat().st_mtime)
        if mtime < cutoff:
            continue
        if f.stat().st_size < 10:
            continue

        try:
            data = json.loads(f.read_text())
        except (json.JSONDecodeError, UnicodeDecodeError):
            continue

        posts = []
        if isinstance(data, list):
            posts = data
        elif isinstance(data, dict):
            for key, val in data.items():
                if isinstance(val, list):
                    posts.extend(val)

        for post in posts:
            if not isinstance(post, dict):
                continue
            title = post.get("title", "")
            body = post.get("selftext", post.get("body", post.get("text", "")))
            text = f"{title} {body}".strip()
            if not text or len(text) < 30:
                continue

            score = _score_reddit_post(text, post)
            if score < 20:
                continue

            subreddit = post.get("subreddit", post.get("sub", "unknown"))
            url = post.get("url", post.get("permalink", ""))
            if url and not url.startswith("http"):
                url = f"https://reddit.com{url}"
            upvotes = post.get("score", post.get("ups", post.get("upvotes", 0)))

            entries.append({
                "source": f"r/{subreddit}",
                "text": text[:500],
                "url": url,
                "platform": "reddit",
                "likes": upvotes,
                "retweets": 0,
                "alpha_score": score,
                "scraped_at": datetime.now().isoformat(),
                "file_source": f.name
            })

    log.info(f"Extracted {len(entries)} Reddit posts with alpha potential")
    return entries


# ─── Scoring Functions ─────────────────────────────────────────
# Keywords that signal actionable alpha
ALPHA_KEYWORDS = [
    r'\$\d+[kK]?', r'\d+%', r'revenue', r'mrr', r'arr', r'profit',
    r'conversion', r'ctr', r'roi', r'cac', r'ltv', r'churn',
    r'cold email', r'outreach', r'affiliate', r'commission',
    r'scrape', r'automate', r'api', r'webhook', r'zapier', r'n8n',
    r'tiktok shop', r'gumroad', r'stripe', r'shopify', r'etsy',
    r'fiverr', r'upwork', r'freelance', r'saas', r'micro.saas',
    r'framework', r'template', r'playbook', r'stack',
    r'I built', r'I made', r'I shipped', r'I launched',
    r'case study', r'breakdown', r'step.by.step',
    r'hack', r'trick', r'secret', r'alpha', r'edge',
    r'arbitrage', r'arb', r'sourcing', r'wholesale',
    r'prompt', r'claude', r'gpt', r'cursor', r'v0',
    r'app.store', r'pwa', r'capacitor', r'react.native',
    r'seo', r'aso', r'backlink', r'ranking',
    r'newsletter', r'substack', r'beehiiv', r'subscriber',
    r'onlyfans', r'fanvue', r'creator', r'monetiz',
    r'clipping', r'ugc', r'short.form', r'reels',
    r'dropship', r'print.on.demand', r'pod', r'merch',
    r'ai.agent', r'workflow', r'automation',
]

ALPHA_PATTERN = re.compile("|".join(ALPHA_KEYWORDS), re.IGNORECASE)

# Noise words that reduce score
NOISE_KEYWORDS = [
    r'motivat', r'grind', r'mindset', r'believe', r'manifest',
    r'follow.for.more', r'like.and.share', r'drop.a.follow',
    r'thread.*below', r'comment.*below', r'dm.me',
]
NOISE_PATTERN = re.compile("|".join(NOISE_KEYWORDS), re.IGNORECASE)


def _score_tweet(text, tweet=None):
    """Score a tweet for alpha potential (0-100)"""
    score = 0
    tweet = tweet or {}

    # Keyword matches (+3 each, max 30)
    matches = len(ALPHA_PATTERN.findall(text))
    score += min(matches * 3, 30)

    # Has specific numbers (+15)
    if re.search(r'\$[\d,]+', text) or re.search(r'\d+%', text):
        score += 15

    # Has URL/tool mention (+5)
    if re.search(r'https?://|\.com|\.io|\.ai', text):
        score += 5

    # Engagement signals
    likes = int(tweet.get("likes", tweet.get("like_count", 0)) or 0)
    if likes > 1000:
        score += 15
    elif likes > 100:
        score += 10
    elif likes > 20:
        score += 5

    # Length bonus (longer = more likely substantive)
    if len(text) > 200:
        score += 5
    if len(text) > 400:
        score += 5

    # Noise penalty
    noise_matches = len(NOISE_PATTERN.findall(text))
    score -= noise_matches * 5

    # Has "I built/made/shipped" = strong signal
    if re.search(r'I (built|made|shipped|launched|created|automated)', text, re.IGNORECASE):
        score += 10

    # Has framework/step-by-step = very strong
    if re.search(r'(step|phase|stage)\s*\d', text, re.IGNORECASE):
        score += 10

    return max(0, min(100, score))


def _score_reddit_post(text, post=None):
    """Score a Reddit post for alpha potential (0-100)"""
    post = post or {}
    score = 0

    # Keyword matches
    matches = len(ALPHA_PATTERN.findall(text))
    score += min(matches * 3, 30)

    # Specific numbers
    if re.search(r'\$[\d,]+', text):
        score += 15

    # Upvotes
    upvotes = int(post.get("score", post.get("ups", 0)) or 0)
    if upvotes > 100:
        score += 15
    elif upvotes > 30:
        score += 10
    elif upvotes > 10:
        score += 5

    # Length bonus
    if len(text) > 300:
        score += 5
    if len(text) > 800:
        score += 10

    # Noise penalty
    noise_matches = len(NOISE_PATTERN.findall(text))
    score -= noise_matches * 5

    # Revenue/case study posts
    if re.search(r'(case study|breakdown|results|revenue report)', text, re.IGNORECASE):
        score += 10

    return max(0, min(100, score))


# ─── Stage 3: FILTER ─────────────────────────────────────────
def filter_alpha(entries):
    """Filter and categorize alpha entries"""
    log.info("=" * 60)
    log.info("STAGE 3: FILTERING ALPHA")
    log.info("=" * 60)

    # Deduplicate against existing ALPHA_STAGING
    existing_hashes = set()
    if ALPHA_STAGING.exists():
        with open(ALPHA_STAGING, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                text = row.get("raw_text", row.get("description", ""))
                if text:
                    existing_hashes.add(hashlib.md5(text[:200].encode()).hexdigest())

    # Get next alpha ID
    next_id = _get_next_alpha_id()

    filtered = []
    for entry in entries:
        text_hash = hashlib.md5(entry["text"][:200].encode()).hexdigest()
        if text_hash in existing_hashes:
            continue
        existing_hashes.add(text_hash)

        score = entry["alpha_score"]

        # Categorize
        category = _categorize_alpha(entry["text"])

        # Status based on score
        if score >= 60:
            status = "APPROVED"
        elif score >= 40:
            status = "PENDING_REVIEW"
        elif score >= 25:
            status = "ENGAGEMENT_BAIT"
        else:
            continue  # Skip low-quality

        alpha_id = f"ALPHA{next_id:04d}"
        next_id += 1

        filtered.append({
            "alpha_id": alpha_id,
            "date_found": datetime.now().strftime("%Y-%m-%d"),
            "source": entry["source"],
            "category": category,
            "raw_text": entry["text"],
            "url": entry.get("url", ""),
            "roi_potential": "HIGH" if score >= 60 else "MEDIUM" if score >= 40 else "LOW",
            "status": status,
            "alpha_score": score,
            "platform": entry["platform"],
            "engagement": entry.get("likes", 0),
            "reviewer_notes": f"Auto-extracted from {entry['platform']} scrape. Score: {score}/100."
        })

    log.info(f"Filtered to {len(filtered)} new alpha entries (deduped against {len(existing_hashes)} existing)")
    log.info(f"  APPROVED: {sum(1 for e in filtered if e['status'] == 'APPROVED')}")
    log.info(f"  PENDING_REVIEW: {sum(1 for e in filtered if e['status'] == 'PENDING_REVIEW')}")
    log.info(f"  ENGAGEMENT_BAIT: {sum(1 for e in filtered if e['status'] == 'ENGAGEMENT_BAIT')}")

    return filtered


def _get_next_alpha_id():
    """Get the next ALPHA ID number"""
    max_id = 0
    if ALPHA_STAGING.exists():
        with open(ALPHA_STAGING, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                aid = row.get("alpha_id", "")
                match = re.match(r"ALPHA(\d+)", aid)
                if match:
                    max_id = max(max_id, int(match.group(1)))
    return max_id + 1


def _categorize_alpha(text):
    """Auto-categorize alpha entry"""
    text_lower = text.lower()

    categories = {
        "APP_FACTORY": ["app store", "pwa", "mobile app", "capacitor", "react native", "ios", "android", "aso"],
        "CONTENT_FORMAT": ["content", "thread", "hook", "viral", "engagement", "reels", "tiktok", "shorts"],
        "OUTBOUND": ["cold email", "outreach", "cold dm", "b2b", "lead gen", "prospecting"],
        "GROWTH_HACK": ["hack", "algorithm", "seo", "ranking", "backlink", "growth"],
        "TOOL_ALPHA": ["tool", "api", "saas", "platform", "software", "chrome extension"],
        "MONETIZATION": ["revenue", "monetiz", "pricing", "subscription", "paywall", "affiliate"],
        "ECOM": ["shopify", "etsy", "amazon", "dropship", "pod", "print on demand", "sourcing", "alibaba"],
        "FREELANCE": ["fiverr", "upwork", "freelance", "gig", "client", "agency"],
        "AI_ALPHA": ["ai agent", "claude", "gpt", "prompt", "cursor", "automation", "workflow"],
    }

    scores = {}
    for cat, keywords in categories.items():
        scores[cat] = sum(1 for kw in keywords if kw in text_lower)

    if not any(scores.values()):
        return "GENERAL"

    return max(scores, key=scores.get)


# ─── Stage 4: REPURPOSE INTO CONTENT ─────────────────────────
def repurpose_content(alpha_entries):
    """Generate niche content from approved alpha entries"""
    log.info("=" * 60)
    log.info("STAGE 4: REPURPOSING INTO CONTENT")
    log.info("=" * 60)

    content_pieces = []
    approved = [e for e in alpha_entries if e["status"] == "APPROVED"]

    if not approved:
        log.info("No APPROVED alpha to repurpose. Skipping content generation.")
        return content_pieces

    # Generate @PRINTMAXXER tweets from alpha
    tweets = _generate_tweets(approved[:10])  # Top 10
    content_pieces.extend(tweets)

    # Generate niche account content variations
    niche_content = _generate_niche_variations(approved[:5])  # Top 5
    content_pieces.extend(niche_content)

    # Save all content
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = CONTENT_OUTPUT / f"auto_content_{timestamp}.csv"

    if content_pieces:
        fieldnames = ["niche", "platform", "content", "source_alpha", "category", "status", "generated_at"]
        with open(output_file, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(content_pieces)
        log.info(f"Generated {len(content_pieces)} content pieces → {output_file}")

    return content_pieces


def _generate_tweets(alpha_entries):
    """Generate @PRINTMAXXER style tweets from alpha"""
    tweets = []

    for entry in alpha_entries:
        text = entry["raw_text"]
        source = entry["source"]
        category = entry["category"]

        # Extract the key insight (first 2 sentences or 200 chars)
        sentences = re.split(r'[.!?]+', text)
        insight = ". ".join(sentences[:2]).strip()
        if len(insight) > 200:
            insight = insight[:197] + "..."

        # @PRINTMAXXER tweet - consequence-first, specific numbers
        tweet = _rewrite_as_printmaxxer(insight, category)
        if tweet:
            tweets.append({
                "niche": "printmaxxer",
                "platform": "twitter",
                "content": tweet,
                "source_alpha": entry["alpha_id"],
                "category": category,
                "status": "PENDING_REVIEW",
                "generated_at": datetime.now().isoformat()
            })

    return tweets


def _generate_niche_variations(alpha_entries):
    """Generate content variations for different niche accounts"""
    variations = []

    NICHES = {
        "faith": {"angle": "faith-based", "audience": "believers", "tone": "purposeful"},
        "fitness": {"angle": "discipline", "audience": "fitness community", "tone": "grind"},
        "tech": {"angle": "builder", "audience": "developers/indie hackers", "tone": "technical"},
        "finance": {"angle": "wealth building", "audience": "money-minded", "tone": "strategic"},
    }

    for entry in alpha_entries:
        text = entry["raw_text"]
        category = entry["category"]

        for niche, config in NICHES.items():
            # Only generate variations that make sense for the niche
            if niche == "faith" and category not in ["APP_FACTORY", "CONTENT_FORMAT", "MONETIZATION", "GENERAL"]:
                continue
            if niche == "fitness" and category not in ["APP_FACTORY", "CONTENT_FORMAT", "GROWTH_HACK", "GENERAL"]:
                continue

            # Create a niche-adapted version
            adapted = _adapt_to_niche(text, niche, config)
            if adapted:
                variations.append({
                    "niche": niche,
                    "platform": "twitter",
                    "content": adapted,
                    "source_alpha": entry["alpha_id"],
                    "category": category,
                    "status": "PENDING_REVIEW",
                    "generated_at": datetime.now().isoformat()
                })

    return variations


def _rewrite_as_printmaxxer(insight, category):
    """Rewrite an insight in @pipelineabuser / @PRINTMAXXER voice"""
    # Can't do full AI rewrite without API, so create a structured draft
    # These get marked PENDING_REVIEW for human polish

    if not insight:
        return None

    # Clean up
    insight = insight.strip()
    if insight.endswith("."):
        insight = insight[:-1]

    # Lowercase energy, consequence-first
    result = insight.lower()

    # Add engagement hook based on category
    hooks = {
        "ECOM": "found another sourcing edge.",
        "OUTBOUND": "cold email alpha.",
        "APP_FACTORY": "app store alpha that nobody talks about.",
        "GROWTH_HACK": "growth hack that actually works.",
        "TOOL_ALPHA": "tool find that saves hours.",
        "MONETIZATION": "monetization angle worth testing.",
        "AI_ALPHA": "ai workflow that prints.",
        "FREELANCE": "freelance arb opportunity.",
        "CONTENT_FORMAT": "content format that's working right now.",
    }

    hook = hooks.get(category, "signal worth paying attention to.")
    return f"{hook}\n\n{result}"


def _adapt_to_niche(text, niche, config):
    """Adapt alpha text for a specific niche audience"""
    if not text or len(text) < 50:
        return None

    # Simple extraction: take the core insight, add niche framing
    # These get marked PENDING_REVIEW for human polish
    sentences = re.split(r'[.!?]+', text)
    core = sentences[0].strip() if sentences else text[:150]
    if len(core) < 20:
        return None

    frames = {
        "faith": f"every hustle needs purpose. {core.lower()}",
        "fitness": f"discipline compounds. {core.lower()}",
        "tech": f"built this. {core.lower()}",
        "finance": f"alpha: {core.lower()}",
    }

    return frames.get(niche)


# ─── Stage 5: LOG ─────────────────────────────────────────────
def log_to_alpha_staging(filtered_entries):
    """Append new alpha entries to ALPHA_STAGING.csv"""
    if not filtered_entries:
        return

    # Check if file exists and has headers
    write_header = not ALPHA_STAGING.exists() or ALPHA_STAGING.stat().st_size < 10

    fieldnames = [
        "alpha_id", "date_found", "source", "category", "raw_text", "url",
        "roi_potential", "status", "alpha_score", "platform", "engagement",
        "reviewer_notes"
    ]

    with open(ALPHA_STAGING, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        if write_header:
            writer.writeheader()
        writer.writerows(filtered_entries)

    log.info(f"Appended {len(filtered_entries)} entries to ALPHA_STAGING.csv")


def generate_daily_digest(scrape_results, alpha_entries, content_pieces, state):
    """Generate daily digest markdown"""
    today = datetime.now().strftime("%Y-%m-%d")
    digest_file = OPS / f"DAILY_RESEARCH_DIGEST_{today.replace('-', '_')}.md"

    approved = [e for e in alpha_entries if e["status"] == "APPROVED"]
    pending = [e for e in alpha_entries if e["status"] == "PENDING_REVIEW"]
    bait = [e for e in alpha_entries if e["status"] == "ENGAGEMENT_BAIT"]

    lines = [
        f"# Daily Research Digest — {today}",
        "",
        f"**Pipeline run:** {datetime.now().strftime('%H:%M:%S')}",
        f"**Scrapers:** Twitter={scrape_results.get('twitter', 'N/A')}, Reddit={scrape_results.get('reddit', 'N/A')}",
        f"**Alpha extracted:** {len(alpha_entries)} total",
        f"  - APPROVED (auto): {len(approved)}",
        f"  - PENDING_REVIEW: {len(pending)}",
        f"  - ENGAGEMENT_BAIT: {len(bait)}",
        f"**Content generated:** {len(content_pieces)} pieces",
        f"**Lifetime total:** {state.get('total_alpha', 0)} alpha, {state.get('total_content', 0)} content",
        "",
        "---",
        "",
    ]

    if approved:
        lines.append("## Top Approved Alpha")
        lines.append("")
        for entry in sorted(approved, key=lambda x: x["alpha_score"], reverse=True)[:10]:
            lines.append(f"### {entry['alpha_id']} (Score: {entry['alpha_score']}, {entry['category']})")
            lines.append(f"**Source:** {entry['source']} | **ROI:** {entry['roi_potential']}")
            lines.append(f"> {entry['raw_text'][:300]}")
            lines.append("")

    if pending:
        lines.append("## Pending Review")
        lines.append("")
        for entry in sorted(pending, key=lambda x: x["alpha_score"], reverse=True)[:10]:
            lines.append(f"- **{entry['alpha_id']}** ({entry['source']}, score {entry['alpha_score']}): {entry['raw_text'][:100]}...")
        lines.append("")

    digest_file.write_text("\n".join(lines))
    log.info(f"Daily digest → {digest_file}")
    return digest_file


# ─── Status ──────────────────────────────────────────────────
def show_status():
    """Show pipeline status"""
    state = load_state()
    print("\n" + "=" * 60)
    print("DAILY RESEARCH PIPELINE STATUS")
    print("=" * 60)

    last_run = state.get("last_run", "NEVER")
    print(f"\nLast run:        {last_run}")
    print(f"Total runs:      {len(state.get('runs', []))}")
    print(f"Lifetime alpha:  {state.get('total_alpha', 0)}")
    print(f"Lifetime content:{state.get('total_content', 0)}")

    # Check scraper health
    print("\nScraper status:")
    scrapers = {
        "Twitter (Brave cookies)": AUTOMATIONS / "twitter_alpha_scraper.py",
        "Reddit (JSON API)": AUTOMATIONS / "background_reddit_scraper.py",
        "Reddit Deep": AUTOMATIONS / "reddit_deep_scraper.py",
        "Browser Daily": AUTOMATIONS / "browser_scraper_daily.py",
    }
    for name, path in scrapers.items():
        exists = path.exists()
        size = f"({path.stat().st_size // 1024}KB)" if exists else ""
        print(f"  {'OK' if exists else 'MISSING':8s} {name} {size}")

    # Recent scrape output
    print("\nRecent Twitter scrapes:")
    if TWITTER_OUTPUT.exists():
        for f in sorted(TWITTER_OUTPUT.glob("*.json"), key=lambda x: x.stat().st_mtime, reverse=True)[:3]:
            mtime = datetime.fromtimestamp(f.stat().st_mtime).strftime("%Y-%m-%d %H:%M")
            print(f"  {mtime}  {f.name} ({f.stat().st_size // 1024}KB)")

    print("\nRecent Reddit scrapes:")
    if REDDIT_OUTPUT.exists():
        for f in sorted(REDDIT_OUTPUT.glob("reddit_*.json"), key=lambda x: x.stat().st_mtime, reverse=True)[:3]:
            mtime = datetime.fromtimestamp(f.stat().st_mtime).strftime("%Y-%m-%d %H:%M")
            print(f"  {mtime}  {f.name} ({f.stat().st_size // 1024}KB)")

    # Cron check
    print("\nCron status:")
    try:
        cron = subprocess.run(["crontab", "-l"], capture_output=True, text=True)
        if "daily_research_pipeline" in cron.stdout:
            print("  OK  daily_research_pipeline.py is in crontab")
        else:
            print("  MISSING  daily_research_pipeline.py NOT in crontab")
            print("  Fix: Add to crontab or run --install-cron")
    except Exception:
        print("  ERROR checking crontab")

    print()


# ─── Main Pipeline ────────────────────────────────────────────
def run_full_pipeline(skip_scrape=False, skip_extract=False, skip_repurpose=False):
    """Run the full pipeline: Scrape → Extract → Filter → Repurpose → Log"""
    if not acquire_lock():
        log.error("Pipeline already running. Exiting.")
        return

    try:
        state = load_state()
        start_time = datetime.now()
        log.info(f"Pipeline started at {start_time}")

        # Stage 1: Scrape
        scrape_results = {}
        if not skip_scrape:
            scrape_results = run_scrapers()
        else:
            scrape_results = {"twitter": "SKIPPED", "reddit": "SKIPPED"}

        # Stage 2: Extract
        alpha_entries = []
        if not skip_extract:
            alpha_entries = extract_alpha()

        # Stage 3: Filter
        filtered = filter_alpha(alpha_entries) if alpha_entries else []

        # Stage 4: Repurpose
        content_pieces = []
        if not skip_repurpose and filtered:
            content_pieces = repurpose_content(filtered)

        # Stage 5: Log
        log_to_alpha_staging(filtered)

        # Update state
        state["last_run"] = datetime.now().isoformat()
        state["total_alpha"] = state.get("total_alpha", 0) + len(filtered)
        state["total_content"] = state.get("total_content", 0) + len(content_pieces)
        state.setdefault("runs", []).append({
            "timestamp": datetime.now().isoformat(),
            "alpha_count": len(filtered),
            "content_count": len(content_pieces),
            "scrape_results": scrape_results,
            "duration_seconds": (datetime.now() - start_time).total_seconds()
        })
        # Keep last 30 runs
        state["runs"] = state["runs"][-30:]
        save_state(state)

        # Generate digest
        generate_daily_digest(scrape_results, filtered, content_pieces, state)

        duration = (datetime.now() - start_time).total_seconds()
        log.info(f"Pipeline complete in {duration:.0f}s. Alpha: {len(filtered)}, Content: {len(content_pieces)}")

    finally:
        release_lock()


# ─── CLI ──────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="Daily Research Pipeline — Scrape → Extract → Filter → Repurpose")
    parser.add_argument("--full", action="store_true", help="Full pipeline (scrape + extract + filter + repurpose)")
    parser.add_argument("--scrape-only", action="store_true", help="Just run scrapers")
    parser.add_argument("--extract-only", action="store_true", help="Process existing scrape data (no scraping)")
    parser.add_argument("--repurpose", action="store_true", help="Generate content from recent approved alpha")
    parser.add_argument("--status", action="store_true", help="Show pipeline status")
    parser.add_argument("--cron", action="store_true", help="Cron mode: skip if already ran today")
    parser.add_argument("--install-cron", action="store_true", help="Install cron entry for daily runs")

    args = parser.parse_args()

    if args.status:
        show_status()
        return

    if args.install_cron:
        _install_cron()
        return

    if args.cron:
        state = load_state()
        if already_ran_today(state):
            log.info("Pipeline already ran today. Skipping (cron mode).")
            return
        run_full_pipeline()
        return

    if args.scrape_only:
        if not acquire_lock():
            return
        try:
            run_scrapers()
        finally:
            release_lock()
        return

    if args.extract_only:
        run_full_pipeline(skip_scrape=True)
        return

    if args.repurpose:
        run_full_pipeline(skip_scrape=True, skip_extract=True)
        return

    if args.full or not any(vars(args).values()):
        run_full_pipeline()
        return


def _install_cron():
    """Install daily research pipeline cron entry"""
    cron_line = (
        f"0 6 * * * cd {PROJECT_DIR} && {PYTHON} AUTOMATIONS/daily_research_pipeline.py --cron "
        f">> AUTOMATIONS/logs/daily_research_pipeline.log 2>&1"
    )

    try:
        result = subprocess.run(["crontab", "-l"], capture_output=True, text=True)
        existing = result.stdout if result.returncode == 0 else ""

        if "daily_research_pipeline" in existing:
            print("Cron entry already exists. No changes made.")
            return

        new_cron = existing.rstrip() + "\n\n# Daily research pipeline (scrape + alpha + content)\n" + cron_line + "\n"
        proc = subprocess.run(["crontab", "-"], input=new_cron, text=True, capture_output=True)
        if proc.returncode == 0:
            print(f"Cron entry installed. Pipeline will run daily at 6:00 AM.")
            print(f"Entry: {cron_line}")
        else:
            print(f"Failed to install cron: {proc.stderr}")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
