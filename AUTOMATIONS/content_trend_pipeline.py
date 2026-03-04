#!/usr/bin/env python3
"""
PRINTMAXX Content Trend Pipeline
==================================
Finds top-performing posts on trending topics, then generates own versions
using the aggregate copy style from copy-style.md.

The idea: monitor what's going viral across platforms, extract the winning
hooks/angles/structures, then produce our own content adapted for each of
our 5 niche accounts.

Usage:
    python3 AUTOMATIONS/content_trend_pipeline.py --scan             # scan for trending content
    python3 AUTOMATIONS/content_trend_pipeline.py --generate         # generate from cached trends
    python3 AUTOMATIONS/content_trend_pipeline.py --scan --generate  # full pipeline
    python3 AUTOMATIONS/content_trend_pipeline.py --status           # show pipeline stats
    python3 AUTOMATIONS/content_trend_pipeline.py --dry-run          # preview without saving

Cron:
    0 */2 * * * cd $BASE && $PYTHON AUTOMATIONS/content_trend_pipeline.py --scan --generate >> AUTOMATIONS/logs/content_trends.log 2>&1
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
import random
from datetime import datetime
from pathlib import Path

# ---------------------------------------------------------------------------
# Path safety
# ---------------------------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parent.parent
TREND_SIGNALS = PROJECT_ROOT / "LEDGER" / "TREND_SIGNALS.csv"
ALPHA_STAGING = PROJECT_ROOT / "LEDGER" / "ALPHA_STAGING.csv"
HIGH_SIGNAL_SOURCES = PROJECT_ROOT / "LEDGER" / "HIGH_SIGNAL_SOURCES.csv"
OUTPUT_DIR = PROJECT_ROOT / "CONTENT" / "social" / "auto_generated"
SCRAPER_OUTPUT = PROJECT_ROOT / "AUTOMATIONS" / "twitter_scraper_output"
LOG_DIR = PROJECT_ROOT / "AUTOMATIONS" / "logs"
TREND_CACHE = PROJECT_ROOT / "AUTOMATIONS" / "logs" / "trend_cache.json"


def safe_path(target: Path) -> Path:
    resolved = Path(target).resolve()
    if not str(resolved).startswith(str(PROJECT_ROOT)):
        raise ValueError(f"BLOCKED: {resolved} is outside project root {PROJECT_ROOT}")
    return resolved


def log(msg: str) -> None:
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] {msg}"
    print(line, file=sys.stderr)
    safe_path(LOG_DIR).mkdir(parents=True, exist_ok=True)
    with open(safe_path(LOG_DIR / "content_trends.log"), "a") as f:
        f.write(line + "\n")


# ---------------------------------------------------------------------------
# Account definitions (which accounts we generate content for)
# ---------------------------------------------------------------------------
ACCOUNTS = {
    "PRINTMAXXER": {
        "handle": "@PRINTMAXXER",
        "niche": "tech/building-in-public",
        "hook_templates": [
            "{hook}. here's what nobody tells you about this.",
            "the real story: {hook}. most people get this wrong.",
            "{hook}. i tested this myself. results were wild.",
            "stop scrolling. {hook}. this changes everything.",
            "{hook}. the play is obvious if you're paying attention.",
        ],
        "relevant_keywords": [
            "saas", "revenue", "mrr", "ship", "build", "launch", "code",
            "automation", "ai", "gpt", "claude", "startup", "indie",
            "product", "growth", "cold email", "gumroad", "stripe",
            "scraper", "tool", "wrapper", "api", "agent", "deploy",
        ],
    },
    "repscheme": {
        "handle": "@repscheme",
        "niche": "fitness",
        "hook_templates": [
            "{hook}. the discipline angle: act accordingly.",
            "{hook}. consistency beats everything. every time.",
            "the real ones know: {hook}. stop overcomplicating it.",
            "{hook}. basics win. always have. always will.",
        ],
        "relevant_keywords": [
            "gym", "fitness", "workout", "lift", "muscle", "protein",
            "creatine", "sleep", "discipline", "consistency", "body",
            "health", "supplement", "train", "physique", "diet",
        ],
    },
    "drifthour": {
        "handle": "@drifthour",
        "niche": "aesthetic/ambient",
        "hook_templates": [
            "there's something about {hook}. curate your inputs.",
            "{hook}. less noise. more signal.",
            "the aesthetic: {hook}. that's the whole thing.",
            "{hook}. golden hour energy. always.",
        ],
        "relevant_keywords": [
            "aesthetic", "lofi", "ambient", "music", "curate", "vibe",
            "golden hour", "morning", "walk", "silence", "nature",
            "sunset", "peace", "calm", "minimal", "design", "art",
        ],
    },
    "voidpilled": {
        "handle": "@voidpilled",
        "niche": "esoteric",
        "hook_templates": [
            "the esoteric reading: {hook}. they're not ready.",
            "{hook}. the simulation is glitching again.",
            "deep pattern: {hook}. most can't see it.",
            "{hook}. consciousness isn't what you think it is.",
        ],
        "relevant_keywords": [
            "consciousness", "psychedelic", "brain", "neuroscience",
            "meditation", "energy", "frequency", "quantum", "simulation",
            "reality", "perception", "philosophy", "sacred", "dna",
            "pattern", "system", "data", "signal", "hidden", "deep",
            "truth", "matrix", "algorithm", "intelligence", "mind",
        ],
    },
    "selahmoments": {
        "handle": "@selahmoments",
        "niche": "faith",
        "hook_templates": [
            "the stewardship lens: {hook}. selah.",
            "{hook}. 'whatever you do, work at it with all your heart.'",
            "there's a parable in this. {hook}. the harvest comes.",
            "{hook}. build quietly. let the work speak. selah.",
        ],
        "relevant_keywords": [
            "faith", "god", "prayer", "steward", "grace", "blessing",
            "church", "ministry", "serve", "community", "worship",
            "scripture", "spiritual", "soul", "purpose", "calling",
        ],
    },
}


# ---------------------------------------------------------------------------
# Trend scanning
# ---------------------------------------------------------------------------
def scan_trend_signals() -> list[dict]:
    """Load existing trend signals from LEDGER/TREND_SIGNALS.csv."""
    trends = []
    if TREND_SIGNALS.exists():
        with open(TREND_SIGNALS, "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                trends.append(row)
    log(f"Loaded {len(trends)} trend signals from TREND_SIGNALS.csv")
    return trends


def scan_alpha_for_trends() -> list[dict]:
    """Scan ALPHA_STAGING.csv for recent high-engagement entries."""
    entries = []
    if ALPHA_STAGING.exists():
        with open(ALPHA_STAGING, "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                status = row.get("status", "")
                if status in ("APPROVED", "ENGAGEMENT_BAIT"):
                    entries.append(row)
    log(f"Found {len(entries)} APPROVED/ENGAGEMENT_BAIT alpha entries")
    return entries


def scan_scraper_output() -> list[dict]:
    """Scan latest Twitter scraper output for high-engagement tweets.

    Uses tiered thresholds: takes all 50+ likes tweets, prioritizes higher.
    Previous 500+ threshold was too strict and yielded 0 results.
    """
    import glob as g
    pattern = str(SCRAPER_OUTPUT / "scrape_*.json")
    files = sorted(g.glob(pattern), reverse=True)
    if not files:
        log("No scraper output files found")
        return []

    # Check up to 3 most recent scrape files for more data
    tweets = []
    for scrape_file in files[:3]:
        try:
            with open(scrape_file, "r") as f:
                data = json.load(f)
            if isinstance(data, dict):
                for handle, handle_data in data.items():
                    tweet_list = []
                    if isinstance(handle_data, dict):
                        tweet_list = handle_data.get("tweets", [])
                    elif isinstance(handle_data, list):
                        tweet_list = handle_data
                    for tweet in tweet_list:
                        likes = tweet.get("favorite_count", tweet.get("likes", 0))
                        if isinstance(likes, str):
                            likes = int(likes.replace(",", "")) if likes.replace(",", "").isdigit() else 0
                        # Tiered: take anything 50+ likes (was 500+, yielded 0 results)
                        if likes >= 50:
                            tweets.append({
                                "text": tweet.get("text", tweet.get("full_text", "")),
                                "likes": likes,
                                "source": handle,
                                "url": tweet.get("url", tweet.get("tweet_url", "")),
                            })
        except (json.JSONDecodeError, KeyError):
            continue

    # Deduplicate by text content
    seen_texts = set()
    unique_tweets = []
    for t in tweets:
        text_key = t["text"][:80].lower()
        if text_key not in seen_texts:
            seen_texts.add(text_key)
            unique_tweets.append(t)

    log(f"Found {len(unique_tweets)} engagement tweets (50+ likes) from {min(len(files), 3)} scrape files")
    return unique_tweets


def extract_winning_hooks(tweets: list[dict]) -> list[dict]:
    """Extract the winning hooks/angles from high-engagement content."""
    hooks = []
    for tweet in tweets:
        text = tweet.get("text", "")
        if not text or len(text) < 30:
            continue

        # Extract first sentence as the hook
        sentences = re.split(r'[.!?]\s', text)
        if sentences:
            hook = sentences[0].strip()
            if len(hook) > 140:
                hook = hook[:137] + "..."
            hooks.append({
                "hook": hook.lower(),
                "full_text": text[:300],
                "likes": tweet.get("likes", 0),
                "source": tweet.get("source", "unknown"),
                "url": tweet.get("url", ""),
            })

    # Sort by engagement
    hooks.sort(key=lambda x: x.get("likes", 0), reverse=True)
    return hooks[:50]  # Top 50 hooks


def cache_trends(trends: list[dict], hooks: list[dict], alpha: list[dict]) -> None:
    """Cache trend data for the generate step."""
    cache = {
        "timestamp": datetime.now().isoformat(),
        "trend_signals": trends[:30],
        "winning_hooks": hooks[:30],
        "alpha_entries": [
            {
                "alpha_id": a.get("alpha_id", ""),
                "title": (a.get("tactic", "") or a.get("title", "") or a.get("alpha_text", "") or a.get("extracted_method", ""))[:200],
                "category": a.get("category", ""),
                "source": a.get("source", ""),
            }
            for a in alpha[:50]
        ],
    }
    safe_path(TREND_CACHE.parent).mkdir(parents=True, exist_ok=True)
    with open(safe_path(TREND_CACHE), "w") as f:
        json.dump(cache, f, indent=2)
    log(f"Cached {len(cache['trend_signals'])} trends, {len(cache['winning_hooks'])} hooks, {len(cache['alpha_entries'])} alpha entries")


# ---------------------------------------------------------------------------
# Content generation
# ---------------------------------------------------------------------------
def load_cache() -> dict:
    """Load cached trend data."""
    if not TREND_CACHE.exists():
        return {}
    with open(TREND_CACHE, "r") as f:
        return json.load(f)


def score_relevance(text: str, keywords: list[str]) -> int:
    """Score how relevant a piece of content is to a keyword list."""
    text_lower = text.lower()
    matches = sum(1 for k in keywords if k in text_lower)
    return min(matches * 25, 100)


def generate_content_batch(cache: dict, dry_run: bool = False) -> dict[str, list[dict]]:
    """Generate content for each account based on trends and hooks."""
    output: dict[str, list[dict]] = {name: [] for name in ACCOUNTS}

    hooks = cache.get("winning_hooks", [])
    alpha = cache.get("alpha_entries", [])
    trends = cache.get("trend_signals", [])

    # Combine all three sources into a unified pool
    sources = []

    # Trend signals as content seeds
    for t in trends:
        title = t.get("signal", t.get("title", t.get("trend", t.get("keyword", ""))))
        if title:
            sources.append({
                "type": "trend",
                "text": title[:100],
                "full_text": title[:300],
                "likes": 75,  # Mid-tier: trends are validated signals
                "source": t.get("source", t.get("platform", "trend")),
            })

    for h in hooks:
        sources.append({
            "type": "hook",
            "text": h.get("hook", ""),
            "full_text": h.get("full_text", ""),
            "likes": h.get("likes", 0),
            "source": h.get("source", ""),
        })
    for a in alpha:
        sources.append({
            "type": "alpha",
            "text": a.get("title", ""),
            "full_text": a.get("title", ""),
            "likes": 100,  # Give alpha entries baseline engagement score so they compete with tweets
            "source": a.get("source", ""),
        })

    for acct_name, acct in ACCOUNTS.items():
        # Score each source for relevance to this account
        scored = []
        for src in sources:
            text = src.get("full_text", src.get("text", ""))
            relevance = score_relevance(text, acct["relevant_keywords"])
            if relevance >= 25:
                scored.append((relevance, src))

        # Sort by relevance, take top 5
        scored.sort(key=lambda x: (x[0], x[1].get("likes", 0)), reverse=True)
        top_sources = scored[:5]

        # Fallback: if zero relevant sources, pick 2 random trend sources
        if not top_sources and sources:
            fallback = random.sample(sources, min(2, len(sources)))
            top_sources = [(10, s) for s in fallback]

        for relevance, src in top_sources:
            hook_text = src.get("text", "")[:100]
            if not hook_text:
                continue

            template = random.choice(acct["hook_templates"])
            draft = template.format(hook=hook_text)

            # Ensure under 280 chars
            if len(draft) > 280:
                draft = draft[:277] + "..."

            output[acct_name].append({
                "account": acct["handle"],
                "draft": draft,
                "source_type": src.get("type", "unknown"),
                "source_handle": src.get("source", ""),
                "relevance": relevance,
                "generated_at": datetime.now().isoformat(),
                "status": "PENDING_REVIEW",
            })

    return output


def save_content(content: dict[str, list[dict]], dry_run: bool = False) -> int:
    """Save generated content to CONTENT/social/auto_generated/."""
    safe_path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    total = 0

    for acct_name, drafts in content.items():
        if not drafts:
            continue

        if dry_run:
            print(f"\n{'='*60}")
            print(f"  DRY RUN: {ACCOUNTS[acct_name]['handle']} ({len(drafts)} drafts)")
            print(f"{'='*60}\n")
            for d in drafts:
                print(f"  [{d['source_type']}:{d['source_handle']}] (rel:{d['relevance']})")
                print(f"  DRAFT: {d['draft']}")
                print()
            total += len(drafts)
            continue

        outfile = safe_path(OUTPUT_DIR / f"trends_{acct_name.lower()}_{ts}.csv")
        fieldnames = [
            "account", "draft", "source_type", "source_handle",
            "relevance", "generated_at", "status",
        ]

        with open(outfile, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for d in drafts:
                writer.writerow(d)

        log(f"Wrote {len(drafts)} trend drafts for {acct_name} -> {outfile}")
        total += len(drafts)

    return total


# ---------------------------------------------------------------------------
# Status
# ---------------------------------------------------------------------------
def show_status() -> None:
    """Show pipeline status."""
    print("--- Content Trend Pipeline Status ---\n")

    # Trend signals
    if TREND_SIGNALS.exists():
        with open(TREND_SIGNALS) as f:
            reader = csv.DictReader(f)
            signals = list(reader)
        print(f"  Trend signals: {len(signals)}")
    else:
        print("  Trend signals: 0 (TREND_SIGNALS.csv not found)")

    # Alpha entries
    if ALPHA_STAGING.exists():
        with open(ALPHA_STAGING) as f:
            reader = csv.DictReader(f)
            entries = list(reader)
        approved = sum(1 for e in entries if e.get("status") == "APPROVED")
        bait = sum(1 for e in entries if e.get("status") == "ENGAGEMENT_BAIT")
        pending = sum(1 for e in entries if e.get("status") == "PENDING_REVIEW")
        print(f"  Alpha entries: {len(entries)} total ({approved} APPROVED, {bait} ENGAGEMENT_BAIT, {pending} PENDING)")
    else:
        print("  Alpha entries: 0")

    # Scraper output
    import glob as g
    scrape_files = sorted(g.glob(str(SCRAPER_OUTPUT / "scrape_*.json")), reverse=True)
    if scrape_files:
        print(f"  Latest scrape: {Path(scrape_files[0]).name}")
    else:
        print("  Latest scrape: None found")

    # Cache
    if TREND_CACHE.exists():
        cache = load_cache()
        print(f"  Cache: {cache.get('timestamp', 'unknown')}")
        print(f"    Hooks: {len(cache.get('winning_hooks', []))}")
        print(f"    Alpha: {len(cache.get('alpha_entries', []))}")
    else:
        print("  Cache: None (run --scan first)")

    # Generated content
    import glob as g2
    existing = sorted(g2.glob(str(OUTPUT_DIR / "trends_*.csv")), reverse=True)
    print(f"\n  Generated content files: {len(existing)}")
    for f_path in existing[:5]:
        name = Path(f_path).name
        with open(f_path) as fh:
            lines = sum(1 for _ in fh) - 1
        print(f"    {name} ({lines} drafts)")
    print()


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main() -> None:
    parser = argparse.ArgumentParser(description="Content Trend Pipeline")
    parser.add_argument("--scan", action="store_true", help="Scan for trending content")
    parser.add_argument("--generate", action="store_true", help="Generate content from cached trends")
    parser.add_argument("--dry-run", action="store_true", help="Preview without saving")
    parser.add_argument("--status", action="store_true", help="Show pipeline stats")
    args = parser.parse_args()

    if args.status:
        show_status()
        return

    if not args.scan and not args.generate:
        parser.print_help()
        return

    if args.scan:
        log("Starting trend scan...")
        trends = scan_trend_signals()
        tweets = scan_scraper_output()
        hooks = extract_winning_hooks(tweets)
        alpha = scan_alpha_for_trends()
        cache_trends(trends, hooks, alpha)
        log(f"Scan complete: {len(trends)} trends, {len(hooks)} hooks, {len(alpha)} alpha entries")

    if args.generate:
        cache = load_cache()
        if not cache:
            log("ERROR: No cached trend data. Run --scan first.")
            sys.exit(1)

        log("Generating content from trends...")
        content = generate_content_batch(cache, args.dry_run)
        total = save_content(content, args.dry_run)

        total_by_acct = {k: len(v) for k, v in content.items() if v}
        log(f"Generated {total} trend-based drafts across {len(total_by_acct)} accounts: {total_by_acct}")

        if total == 0:
            log("No relevant trends found for any account. Try scanning more sources.")


if __name__ == "__main__":
    main()
