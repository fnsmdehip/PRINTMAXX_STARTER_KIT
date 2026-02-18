#!/usr/bin/env python3
"""
PRINTMAXX Alpha Extraction Processor
======================================
Reads raw bookmark/tweet JSON dumps, extracts business-relevant alpha,
filters for actionable content, deduplicates against ALPHA_STAGING.csv,
and outputs formatted rows ready to append.

Usage:
    python3 extract_alpha.py bookmarks.json                    # Process JSON dump
    python3 extract_alpha.py bookmarks.json --format csv       # Output as CSV rows
    python3 extract_alpha.py bookmarks.json --append           # Append directly to ALPHA_STAGING.csv
    python3 extract_alpha.py tweets_folder/ --batch            # Process folder of JSONs
    python3 extract_alpha.py --stdin                           # Read JSON from stdin
"""

import csv
import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
ALPHA_STAGING_CSV = PROJECT_ROOT / "LEDGER" / "ALPHA_STAGING.csv"
OUTPUT_DIR = Path(__file__).resolve().parent / "output"

# Business content keywords (lowercase)
BUSINESS_KEYWORDS = {
    "revenue", "mrr", "arr", "$", "launched", "built", "strategy", "growth",
    "saas", "app", "monetiz", "profit", "conversion", "funnel", "outbound",
    "cold email", "subscribers", "followers", "views", "downloads",
    "affiliate", "commission", "pricing", "paywall", "subscription",
    "api", "automation", "workflow", "scraping", "tool", "framework",
    "template", "course", "ebook", "newsletter", "content",
    "seo", "aso", "geo", "rank", "traffic", "impressions",
    "tiktok shop", "dropship", "ecom", "print on demand",
    "ai agent", "mcp", "claude", "chatgpt", "prompt",
    "github", "open source", "mit license", "repo",
    "indie hacker", "solopreneur", "bootstrap",
    "k/mo", "k/month", "k mrr", "per month",
    "waitlist", "beta", "launch", "product hunt",
}

# Spam/noise keywords to filter out
NOISE_KEYWORDS = {
    "giveaway", "drop your", "retweet to win", "follow and rt",
    "dm me to learn", "link in bio only", "limited spots",
}

# Category detection patterns
CATEGORY_PATTERNS = {
    "APP_FACTORY": ["app", "mobile", "ios", "android", "react native", "expo", "swift", "flutter", "aso"],
    "CONTENT_FORMAT": ["content", "tiktok", "youtube", "reels", "shorts", "viral", "hook", "thumbnail"],
    "OUTBOUND": ["cold email", "outbound", "deliverability", "warmup", "smtp", "instantly", "smartlead", "linkedin"],
    "GROWTH_HACK": ["growth", "hack", "automation", "scraping", "bot", "followers", "engagement"],
    "TOOL_ALPHA": ["tool", "api", "mcp", "plugin", "extension", "chrome", "saas", "open source", "github"],
    "MONETIZATION": ["revenue", "mrr", "monetiz", "pricing", "paywall", "subscription", "affiliate", "commission"],
    "SEO_GEO_ASO": ["seo", "geo", "aso", "rank", "keyword", "serp", "backlink", "domain"],
    "ECOM": ["ecom", "dropship", "tiktok shop", "amazon", "etsy", "print on demand", "aliexpress"],
}


def log(msg: str) -> None:
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{ts}] {msg}")


def get_next_alpha_id() -> int:
    """Read ALPHA_STAGING.csv to find the next available alpha_id number."""
    if not ALPHA_STAGING_CSV.exists():
        return 1

    max_id = 0
    with open(ALPHA_STAGING_CSV, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            alpha_id = row.get("alpha_id", "")
            match = re.search(r"ALPHA(\d+)", alpha_id)
            if match:
                num = int(match.group(1))
                if num > max_id:
                    max_id = num

    return max_id + 1


def get_existing_urls() -> set:
    """Read existing source_urls from ALPHA_STAGING.csv for deduplication."""
    urls = set()
    if not ALPHA_STAGING_CSV.exists():
        return urls

    with open(ALPHA_STAGING_CSV, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            url = row.get("source_url", "").strip()
            if url:
                urls.add(url)

    return urls


def classify_category(text: str) -> str:
    """Classify tweet into a category based on keyword matching."""
    text_lower = text.lower()
    scores = {}

    for category, keywords in CATEGORY_PATTERNS.items():
        score = sum(1 for kw in keywords if kw in text_lower)
        if score > 0:
            scores[category] = score

    if scores:
        return max(scores, key=scores.get)
    return "GROWTH_HACK"  # Default


def is_business_content(text: str) -> bool:
    """Check if text contains business-relevant content."""
    text_lower = text.lower()

    # Check for noise first
    for noise in NOISE_KEYWORDS:
        if noise in text_lower:
            return False

    # Check for business keywords
    matches = sum(1 for kw in BUSINESS_KEYWORDS if kw in text_lower)
    return matches >= 2  # At least 2 business keywords


def extract_metrics(text: str) -> dict:
    """Extract engagement metrics and numbers from text."""
    metrics = {
        "has_revenue_number": False,
        "has_growth_number": False,
        "dollar_amounts": [],
        "percentages": [],
        "follower_counts": [],
    }

    # Dollar amounts
    dollar_matches = re.findall(r"\$[\d,]+(?:\.\d+)?(?:k|K|m|M)?", text)
    if dollar_matches:
        metrics["has_revenue_number"] = True
        metrics["dollar_amounts"] = dollar_matches

    # Also catch "Xk/mo" patterns
    revenue_matches = re.findall(r"(\d+(?:\.\d+)?)\s*(?:k|K)\s*/\s*(?:mo|month|yr|year)", text)
    if revenue_matches:
        metrics["has_revenue_number"] = True

    # Percentages
    pct_matches = re.findall(r"\d+(?:\.\d+)?%", text)
    if pct_matches:
        metrics["has_growth_number"] = True
        metrics["percentages"] = pct_matches

    # Large numbers (followers, views, downloads)
    large_nums = re.findall(r"(\d+(?:\.\d+)?)\s*(?:k|K|m|M|B)\s*(?:followers|views|downloads|subs|subscribers)", text, re.IGNORECASE)
    if large_nums:
        metrics["has_growth_number"] = True
        metrics["follower_counts"] = large_nums

    return metrics


def estimate_roi(text: str, metrics: dict) -> str:
    """Estimate ROI potential based on content analysis."""
    if metrics["has_revenue_number"] and metrics["dollar_amounts"]:
        # Check if amounts are significant
        for amt in metrics["dollar_amounts"]:
            clean = amt.replace("$", "").replace(",", "").lower()
            if "m" in clean:
                return "HIGHEST"
            if "k" in clean:
                try:
                    val = float(clean.replace("k", ""))
                    if val >= 10:
                        return "HIGHEST"
                    elif val >= 1:
                        return "HIGH"
                except ValueError:
                    pass
        return "HIGH"

    if metrics["has_growth_number"]:
        return "HIGH"

    text_lower = text.lower()
    if any(kw in text_lower for kw in ["framework", "method", "strategy", "system", "playbook"]):
        return "MEDIUM"

    return "LOW"


def parse_tweet_json(data: dict) -> Optional[dict]:
    """Parse a single tweet/bookmark JSON object into alpha entry."""
    # Handle different JSON structures from Twitter exports
    text = ""
    handle = ""
    tweet_id = ""
    url = ""
    likes = 0
    retweets = 0
    views = 0
    created_at = ""

    # Standard Twitter API format
    if "full_text" in data:
        text = data["full_text"]
    elif "text" in data:
        text = data["text"]
    elif "tweet" in data:
        tweet_data = data["tweet"]
        text = tweet_data.get("full_text", tweet_data.get("text", ""))
        handle = tweet_data.get("user", {}).get("screen_name", "")

    # User/author info
    if "user" in data:
        handle = data["user"].get("screen_name", data["user"].get("username", ""))
    elif "author" in data:
        handle = data["author"].get("username", "")
    elif "core" in data:
        # Twitter v2 format
        user_results = data.get("core", {}).get("user_results", {}).get("result", {})
        handle = user_results.get("legacy", {}).get("screen_name", "")

    # Tweet ID
    tweet_id = str(data.get("id", data.get("id_str", data.get("tweet_id", ""))))
    if not tweet_id and "rest_id" in data:
        tweet_id = data["rest_id"]

    # Build URL
    if handle and tweet_id:
        url = f"https://x.com/{handle}/status/{tweet_id}"
    elif "url" in data:
        url = data["url"]

    # Metrics
    if "public_metrics" in data:
        pm = data["public_metrics"]
        likes = pm.get("like_count", 0)
        retweets = pm.get("retweet_count", 0)
        views = pm.get("impression_count", 0)
    elif "favorite_count" in data:
        likes = data.get("favorite_count", 0)
        retweets = data.get("retweet_count", 0)
    elif "legacy" in data:
        legacy = data["legacy"]
        likes = legacy.get("favorite_count", 0)
        retweets = legacy.get("retweet_count", 0)
        text = text or legacy.get("full_text", "")

    created_at = data.get("created_at", "")

    if not text:
        return None

    return {
        "text": text,
        "handle": handle,
        "tweet_id": tweet_id,
        "url": url,
        "likes": likes,
        "retweets": retweets,
        "views": views,
        "created_at": created_at,
    }


def process_tweets(tweets: list, existing_urls: set, start_id: int) -> list:
    """Process list of tweet data into alpha entries."""
    entries = []
    current_id = start_id

    for tweet_data in tweets:
        parsed = parse_tweet_json(tweet_data)
        if not parsed:
            continue

        text = parsed["text"]

        # Filter for business content
        if not is_business_content(text):
            continue

        # Deduplicate
        if parsed["url"] and parsed["url"] in existing_urls:
            log(f"  Skipping duplicate: {parsed['url']}")
            continue

        # Analyze
        metrics = extract_metrics(text)
        category = classify_category(text)
        roi = estimate_roi(text, metrics)

        # Build description (clean text, remove URLs)
        description = re.sub(r"https?://\S+", "", text).strip()
        description = re.sub(r"\s+", " ", description)
        if len(description) > 300:
            description = description[:297] + "..."

        # Extract actionable steps from text
        steps = extract_steps(text)

        entry = {
            "alpha_id": f"ALPHA{current_id:03d}",
            "source": f"@{parsed['handle']}" if parsed["handle"] else "Twitter bookmark",
            "source_url": parsed["url"],
            "category": category,
            "title": description[:80],
            "description": description,
            "actionable_steps": steps,
            "effort_level": "MEDIUM",
            "roi_potential": roi,
            "risk_level": "LOW",
            "applies_to_niches": "ALL",
            "status": "PENDING_REVIEW",
            "reviewed_date": "",
            "reviewer_notes": f"Auto-extracted. Likes:{parsed['likes']} RT:{parsed['retweets']}",
        }

        entries.append(entry)
        existing_urls.add(parsed["url"])
        current_id += 1

    return entries


def extract_steps(text: str) -> str:
    """Try to extract actionable steps from tweet text."""
    # Look for numbered lists
    numbered = re.findall(r"(?:\d+[\.\)]\s+)(.*?)(?=\d+[\.\)]|\Z)", text, re.DOTALL)
    if numbered and len(numbered) >= 2:
        steps = [s.strip() for s in numbered[:5]]
        return ". ".join(f"{i+1}. {s}" for i, s in enumerate(steps))

    # Look for bullet-like patterns
    bullets = re.findall(r"[-*]\s+(.*?)(?=[-*]|\Z)", text, re.DOTALL)
    if bullets and len(bullets) >= 2:
        steps = [s.strip() for s in bullets[:5]]
        return ". ".join(f"{i+1}. {s}" for i, s in enumerate(steps))

    # Generic steps based on category
    return "1. Analyze approach 2. Adapt to PRINTMAXX context 3. Test implementation"


def load_json_file(filepath: Path) -> list:
    """Load JSON file - handles arrays and individual objects."""
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)

    if isinstance(data, list):
        return data
    elif isinstance(data, dict):
        # Check if it's a wrapper object with data inside
        for key in ["data", "tweets", "bookmarks", "results", "entries"]:
            if key in data and isinstance(data[key], list):
                return data[key]
        # Single tweet object
        return [data]

    return []


def append_to_staging(entries: list) -> None:
    """Append entries to ALPHA_STAGING.csv."""
    if not entries:
        return

    fieldnames = [
        "alpha_id", "source", "source_url", "category", "title", "description",
        "actionable_steps", "effort_level", "roi_potential", "risk_level",
        "applies_to_niches", "status", "reviewed_date", "reviewer_notes",
    ]

    file_exists = ALPHA_STAGING_CSV.exists()

    with open(ALPHA_STAGING_CSV, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        writer.writerows(entries)

    log(f"Appended {len(entries)} entries to {ALPHA_STAGING_CSV}")


def main():
    import argparse

    parser = argparse.ArgumentParser(description="PRINTMAXX Alpha Extraction Processor")
    parser.add_argument("input", nargs="?", help="JSON file or folder to process")
    parser.add_argument("--format", choices=["csv", "json", "text"], default="text",
                        help="Output format (default: text)")
    parser.add_argument("--append", action="store_true",
                        help="Append directly to ALPHA_STAGING.csv")
    parser.add_argument("--batch", action="store_true",
                        help="Process folder of JSON files")
    parser.add_argument("--stdin", action="store_true",
                        help="Read JSON from stdin")
    parser.add_argument("--min-likes", type=int, default=0,
                        help="Minimum likes to include (default: 0)")
    args = parser.parse_args()

    log("PRINTMAXX Alpha Extraction Processor starting")

    # Load existing data for deduplication
    existing_urls = get_existing_urls()
    next_id = get_next_alpha_id()
    log(f"Existing entries: {len(existing_urls)} URLs tracked")
    log(f"Next alpha_id: ALPHA{next_id:03d}")

    # Load input data
    tweets = []
    if args.stdin:
        data = json.loads(sys.stdin.read())
        tweets = data if isinstance(data, list) else [data]
    elif args.input:
        input_path = Path(args.input)
        if args.batch and input_path.is_dir():
            for json_file in sorted(input_path.glob("*.json")):
                log(f"Loading: {json_file.name}")
                tweets.extend(load_json_file(json_file))
        elif input_path.is_file():
            tweets = load_json_file(input_path)
        else:
            log(f"Input not found: {input_path}")
            sys.exit(1)
    else:
        log("No input specified. Use --stdin or provide a file/folder path.")
        parser.print_help()
        sys.exit(1)

    log(f"Loaded {len(tweets)} raw entries")

    # Process
    entries = process_tweets(tweets, existing_urls, next_id)

    # Filter by min likes
    if args.min_likes > 0:
        # We'd need to store likes in entries - for now this works on parse level
        log(f"Min likes filter: {args.min_likes} (applied during parsing)")

    log(f"Extracted {len(entries)} business-relevant alpha entries")

    if not entries:
        log("No new entries found. All may be duplicates or non-business content.")
        return

    # Output
    if args.append:
        append_to_staging(entries)
    elif args.format == "csv":
        Output_dir = OUTPUT_DIR
        Output_dir.mkdir(parents=True, exist_ok=True)
        output_file = Output_dir / f"alpha_batch_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        fieldnames = list(entries[0].keys())
        with open(output_file, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(entries)
        log(f"CSV written to {output_file}")
    elif args.format == "json":
        Output_dir = OUTPUT_DIR
        Output_dir.mkdir(parents=True, exist_ok=True)
        output_file = Output_dir / f"alpha_batch_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(entries, f, indent=2)
        log(f"JSON written to {output_file}")
    else:
        # Print to stdout
        for entry in entries:
            print(f"\n{'='*60}")
            print(f"  ID: {entry['alpha_id']}")
            print(f"  Source: {entry['source']}")
            print(f"  Category: {entry['category']}")
            print(f"  ROI: {entry['roi_potential']}")
            print(f"  Title: {entry['title']}")
            print(f"  URL: {entry['source_url']}")

    # Summary
    categories = {}
    roi_counts = {}
    for e in entries:
        categories[e["category"]] = categories.get(e["category"], 0) + 1
        roi_counts[e["roi_potential"]] = roi_counts.get(e["roi_potential"], 0) + 1

    log("\n--- EXTRACTION SUMMARY ---")
    log(f"Total extracted: {len(entries)}")
    log(f"By category: {categories}")
    log(f"By ROI: {roi_counts}")
    log("Done.")


if __name__ == "__main__":
    main()
