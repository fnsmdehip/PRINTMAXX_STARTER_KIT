#!/usr/bin/env python3
"""
PRINTMAXX Quote Tweet Scanner
==============================
Scans high-signal accounts' recent tweets (from Brave scraper JSON output) and
generates quote-tweet draft ideas for PRINTMAXX niche accounts.

The idea: monitor what high-signal accounts post, then generate quote-tweet
angles that add value while riding their engagement wave.

Usage:
    python3 AUTOMATIONS/quote_tweet_scanner.py                    # scan latest scrape
    python3 AUTOMATIONS/quote_tweet_scanner.py --min-likes 500    # only high-engagement
    python3 AUTOMATIONS/quote_tweet_scanner.py --account PRINTMAXXER  # one account only
    python3 AUTOMATIONS/quote_tweet_scanner.py --dry-run          # print, don't save
    python3 AUTOMATIONS/quote_tweet_scanner.py --status           # show stats

Cron:
    0 8 * * * cd $BASE && python3 AUTOMATIONS/quote_tweet_scanner.py --min-likes 200 >> AUTOMATIONS/logs/quote_scanner.log 2>&1
"""

from __future__ import annotations

import argparse
import csv
import glob
import json
import os
import random
import sys
from datetime import datetime
from pathlib import Path

# ---------------------------------------------------------------------------
# Path safety
# ---------------------------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parent.parent
SCRAPER_OUTPUT = PROJECT_ROOT / "AUTOMATIONS" / "twitter_scraper_output"
SOURCES_CSV = PROJECT_ROOT / "LEDGER" / "HIGH_SIGNAL_SOURCES.csv"
OUTPUT_DIR = PROJECT_ROOT / "CONTENT" / "social" / "quote_tweets"
LOG_DIR = PROJECT_ROOT / "AUTOMATIONS" / "logs"


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
    with open(safe_path(LOG_DIR / "quote_scanner.log"), "a") as f:
        f.write(line + "\n")


# ---------------------------------------------------------------------------
# Account definitions (which accounts can quote-tweet)
# ---------------------------------------------------------------------------
ACCOUNTS = {
    "PRINTMAXXER": {
        "handle": "@PRINTMAXXER",
        "niche": "tech/building-in-public",
        "angle_templates": [
            "this is the play. {insight}. i tested this last week and {result}.",
            "been saying this for months. {insight}. the numbers don't lie.",
            "{insight}. borderline illegal how few people know this.",
            "the real alpha here: {insight}. most people will scroll past this.",
            "this. {insight}. stop overthinking it.",
        ],
        "relevant_topics": [
            "app", "saas", "revenue", "mrr", "ship", "build", "launch", "code",
            "automation", "ai", "gpt", "claude", "deploy", "startup", "indie",
            "hacker", "product", "distribution", "growth", "hack", "cold email",
            "outbound", "gumroad", "stripe", "monetiz", "profit", "scraper",
            "tool", "wrapper", "api", "mcp", "agent",
        ],
    },
    "repscheme": {
        "handle": "@repscheme",
        "niche": "fitness",
        "angle_templates": [
            "the discipline version of this: {insight}. act accordingly.",
            "{insight}. consistency beats intensity. every time.",
            "this applies to the gym too. {insight}. stop overcomplicating it.",
            "basics > hacks. {insight}. the fundamentals never change.",
        ],
        "relevant_topics": [
            "gym", "fitness", "workout", "lift", "muscle", "protein", "creatine",
            "sleep", "discipline", "consistency", "body", "health", "supplement",
            "train", "physique", "diet", "calories", "cardio", "walk", "steps",
        ],
    },
    "drifthour": {
        "handle": "@drifthour",
        "niche": "aesthetic/ambient",
        "angle_templates": [
            "there's something beautiful about this. {insight}.",
            "curate your inputs. {insight}. the rest follows.",
            "{insight}. less noise. more signal. always.",
            "the aesthetic of {insight}. that's the whole thing.",
        ],
        "relevant_topics": [
            "aesthetic", "lofi", "ambient", "music", "curate", "vibe", "golden hour",
            "morning", "walk", "silence", "nature", "sunset", "peace", "calm",
            "minimal", "design", "art", "film", "analog", "vintage", "taste",
        ],
    },
    "voidpilled": {
        "handle": "@voidpilled",
        "niche": "esoteric",
        "angle_templates": [
            "the esoteric reading of this: {insight}. they're not ready for this conversation.",
            "{insight}. the simulation is glitching again.",
            "deep pattern: {insight}. most people can't see it because they're not looking.",
            "{insight}. consciousness isn't what you think it is.",
        ],
        "relevant_topics": [
            "consciousness", "psychedelic", "ketamine", "brain", "neuroscience",
            "epigenetic", "longevity", "meditation", "energy", "frequency",
            "quantum", "simulation", "matrix", "reality", "perception",
            "philosophy", "metaphysic", "sacred", "geometry", "dna",
        ],
    },
    "selahmoments": {
        "handle": "@selahmoments",
        "niche": "faith",
        "angle_templates": [
            "the stewardship lens: {insight}. selah.",
            "{insight}. 'whatever you do, work at it with all your heart.' - colossians 3:23",
            "there's a parable in this. {insight}. the harvest comes after the sowing.",
            "{insight}. build quietly. let the work speak. selah.",
        ],
        "relevant_topics": [
            "faith", "god", "prayer", "steward", "parable", "grace", "blessing",
            "church", "ministry", "serve", "community", "ramadan", "worship",
            "scripture", "bible", "spiritual", "soul", "purpose", "calling",
        ],
    },
}


# ---------------------------------------------------------------------------
# Core logic
# ---------------------------------------------------------------------------
def find_latest_scrape() -> Path | None:
    """Find the most recent scraper JSON output."""
    pattern = str(SCRAPER_OUTPUT / "scrape_*.json")
    files = sorted(glob.glob(pattern), reverse=True)
    return Path(files[0]) if files else None


def load_scrape_data(scrape_path: Path) -> list[dict]:
    """Load tweets from a scraper JSON output."""
    with open(safe_path(scrape_path), "r") as f:
        data = json.load(f)
    tweets = []
    if isinstance(data, dict):
        for handle, handle_data in data.items():
            if isinstance(handle_data, dict):
                for tweet in handle_data.get("tweets", []):
                    tweet["_source_handle"] = handle
                    tweets.append(tweet)
            elif isinstance(handle_data, list):
                for tweet in handle_data:
                    tweet["_source_handle"] = handle
                    tweets.append(tweet)
    elif isinstance(data, list):
        tweets = data
    return tweets


def score_relevance(tweet_text: str, topics: list[str]) -> int:
    """Score how relevant a tweet is to a set of topics (0-100)."""
    text_lower = tweet_text.lower()
    matches = sum(1 for t in topics if t in text_lower)
    # Base score from keyword matches
    score = min(matches * 20, 80)
    # Bonus for specific numbers (sign of real alpha)
    import re
    if re.search(r'\$[\d,]+', tweet_text):
        score += 10
    if re.search(r'\d+[kKmM]\b', tweet_text):
        score += 5
    if re.search(r'\d+%', tweet_text):
        score += 5
    return min(score, 100)


def extract_insight(tweet_text: str) -> str:
    """Extract the core insight from a tweet for use in quote templates."""
    # Take first sentence or up to 100 chars
    sentences = tweet_text.split(". ")
    if sentences:
        insight = sentences[0].strip()
        if len(insight) > 120:
            insight = insight[:117] + "..."
        return insight.lower()
    return tweet_text[:100].lower()


def generate_quote_drafts(
    tweets: list[dict],
    min_likes: int = 100,
    account_filter: str | None = None,
) -> dict[str, list[dict]]:
    """Generate quote tweet drafts for each account."""
    drafts: dict[str, list[dict]] = {name: [] for name in ACCOUNTS}

    for tweet in tweets:
        text = tweet.get("text", tweet.get("full_text", ""))
        if not text or len(text) < 30:
            continue

        # Check engagement threshold
        likes = tweet.get("favorite_count", tweet.get("likes", 0))
        if isinstance(likes, str):
            likes = int(likes.replace(",", "")) if likes.replace(",", "").isdigit() else 0
        if likes < min_likes:
            continue

        source_handle = tweet.get("_source_handle", "unknown")
        tweet_url = tweet.get("url", tweet.get("tweet_url", f"https://x.com/{source_handle}"))

        for acct_name, acct in ACCOUNTS.items():
            if account_filter and acct_name.lower() != account_filter.lower():
                continue

            relevance = score_relevance(text, acct["relevant_topics"])
            if relevance < 20:
                continue

            insight = extract_insight(text)
            template = random.choice(acct["angle_templates"])

            # Simple result generation for the template
            results = [
                "the ROI was instant",
                "it paid for itself in a week",
                "3x the output in half the time",
                "saved 10+ hours that week alone",
            ]

            draft_text = template.format(
                insight=insight,
                result=random.choice(results),
            )

            # Ensure under 280 chars
            if len(draft_text) > 280:
                draft_text = draft_text[:277] + "..."

            drafts[acct_name].append({
                "account": acct["handle"],
                "draft": draft_text,
                "source_handle": source_handle,
                "source_url": tweet_url,
                "source_likes": likes,
                "relevance_score": relevance,
                "original_text": text[:200],
            })

    # Sort by relevance within each account, keep top 10
    for acct_name in drafts:
        drafts[acct_name] = sorted(
            drafts[acct_name],
            key=lambda x: (x["relevance_score"], x["source_likes"]),
            reverse=True,
        )[:10]

    return drafts


def save_drafts(drafts: dict[str, list[dict]], dry_run: bool = False) -> int:
    """Save quote tweet drafts to CSV files."""
    safe_path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    total = 0

    for acct_name, acct_drafts in drafts.items():
        if not acct_drafts:
            continue

        if dry_run:
            print(f"\n{'='*60}")
            print(f"  DRY RUN: {ACCOUNTS[acct_name]['handle']} ({len(acct_drafts)} quote drafts)")
            print(f"  Would write to: {OUTPUT_DIR / f'quotes_{acct_name.lower()}_{ts}.csv'}")
            print(f"{'='*60}\n")
            for d in acct_drafts:
                print(f"  [{d['source_handle']}] (rel:{d['relevance_score']}, likes:{d['source_likes']})")
                print(f"  QUOTE: {d['draft']}")
                print(f"  ORIG: {d['original_text'][:100]}...")
                print()
            total += len(acct_drafts)
            continue

        outfile = safe_path(OUTPUT_DIR / f"quotes_{acct_name.lower()}_{ts}.csv")
        fieldnames = [
            "account", "draft", "source_handle", "source_url",
            "source_likes", "relevance_score", "original_text",
            "status", "generated_at",
        ]

        with open(outfile, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for d in acct_drafts:
                d["status"] = "PENDING_REVIEW"
                d["generated_at"] = datetime.now().isoformat()
                writer.writerow(d)

        log(f"Wrote {len(acct_drafts)} quote drafts for {acct_name} → {outfile}")
        total += len(acct_drafts)

    return total


def show_status() -> None:
    """Show scanner status."""
    print("--- Quote Tweet Scanner Status ---")

    # Latest scrape
    latest = find_latest_scrape()
    if latest:
        print(f"  Latest scrape: {latest.name}")
        data = load_scrape_data(latest)
        print(f"  Total tweets in scrape: {len(data)}")

        # Count by engagement
        high = sum(1 for t in data if int(t.get("favorite_count", t.get("likes", 0)) or 0) >= 500)
        med = sum(1 for t in data if 100 <= int(t.get("favorite_count", t.get("likes", 0)) or 0) < 500)
        print(f"  High engagement (500+ likes): {high}")
        print(f"  Medium engagement (100-499): {med}")
    else:
        print("  No scraper output found.")

    # Existing drafts
    print()
    pattern = str(OUTPUT_DIR / "quotes_*.csv")
    existing = sorted(glob.glob(pattern), reverse=True)
    print(f"  Existing quote draft files: {len(existing)}")
    for f in existing[:5]:
        name = Path(f).name
        with open(f) as fh:
            lines = sum(1 for _ in fh) - 1  # minus header
        print(f"    {name} ({lines} drafts)")

    # Sources
    if SOURCES_CSV.exists():
        with open(SOURCES_CSV) as f:
            reader = csv.DictReader(f)
            sources = [r for r in reader if r.get("auto_monitor", "").upper() == "TRUE"]
        print(f"\n  Monitored sources (auto_monitor=TRUE): {len(sources)}")
    print()


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main() -> None:
    parser = argparse.ArgumentParser(description="Quote Tweet Scanner")
    parser.add_argument("--min-likes", type=int, default=100, help="Min likes threshold")
    parser.add_argument("--account", type=str, help="Filter to one account")
    parser.add_argument("--scrape-file", type=str, help="Path to specific scrape JSON")
    parser.add_argument("--dry-run", action="store_true", help="Print, don't save")
    parser.add_argument("--status", action="store_true", help="Show status")
    args = parser.parse_args()

    if args.status:
        show_status()
        return

    # Find scrape data
    if args.scrape_file:
        scrape_path = Path(args.scrape_file)
    else:
        scrape_path = find_latest_scrape()

    if not scrape_path or not scrape_path.exists():
        log("ERROR: No scraper output found. Run twitter_alpha_scraper.py first.")
        sys.exit(1)

    log(f"Scanning: {scrape_path.name}, min_likes={args.min_likes}, account={args.account or 'ALL'}")

    tweets = load_scrape_data(scrape_path)
    log(f"Loaded {len(tweets)} tweets from scrape")

    drafts = generate_quote_drafts(tweets, args.min_likes, args.account)

    total = save_drafts(drafts, args.dry_run)

    total_by_acct = {k: len(v) for k, v in drafts.items() if v}
    log(f"Generated {total} quote drafts across {len(total_by_acct)} accounts: {total_by_acct}")

    if not args.dry_run and total > 0:
        log(f"Saved to: {OUTPUT_DIR}/quotes_*_{datetime.now().strftime('%Y%m%d')}*.csv")
    elif total == 0:
        log("No tweets matched criteria. Try lowering --min-likes.")


if __name__ == "__main__":
    main()
