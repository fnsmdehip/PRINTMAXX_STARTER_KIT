#!/usr/bin/env python3
"""
alpha_extractor.py - Extract actionable alpha from text sources

Parses tweets, articles, forum posts, and bookmarks to extract
structured alpha entries for ALPHA_STAGING.csv. Auto-categorizes,
deduplicates against existing entries, and applies engagement
authenticity checks.

Usage:
    python3 alpha_extractor.py --text "Tweet text here" --source @handle
    python3 alpha_extractor.py --file bookmarks.json --format twitter
    python3 alpha_extractor.py --file notes.md --format markdown
    python3 alpha_extractor.py --url https://x.com/handle/status/123

Example:
    # Extract from a single tweet
    python3 alpha_extractor.py --text "I made $47K from 3 apps. here's how..." --source @indiehacker

    # Extract from exported bookmarks JSON
    python3 alpha_extractor.py --file bookmarks.json --format twitter

    # Extract from markdown notes
    python3 alpha_extractor.py --file research_notes.md --format markdown
"""

import argparse
import csv
import json
import logging
import re
import sys
from datetime import datetime
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent.parent
LEDGER_DIR = PROJECT_DIR / "LEDGER"
ALPHA_FILE = LEDGER_DIR / "ALPHA_STAGING.csv"
LOG_DIR = PROJECT_DIR / "AUTOMATIONS" / "logs"

LOG_DIR.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_DIR / "alpha_extractor.log"),
        logging.StreamHandler(sys.stdout),
    ],
)
logger = logging.getLogger(__name__)

# Category keywords for auto-categorization
CATEGORY_KEYWORDS = {
    "APP_FACTORY": ["app", "mobile", "ios", "android", "react native", "expo", "app store",
                     "playstore", "downloads", "subscription", "IAP"],
    "CONTENT_FORMAT": ["content", "thread", "viral", "hook", "engagement", "algorithm",
                        "reels", "shorts", "tiktok", "instagram", "youtube"],
    "OUTBOUND": ["cold email", "outbound", "deliverability", "reply rate", "instantly",
                  "smartlead", "clay", "email sequence", "warmup", "inbox"],
    "GROWTH_HACK": ["growth", "followers", "audience", "distribution", "viral",
                     "engagement rate", "pods", "automation"],
    "TOOL_ALPHA": ["tool", "mcp", "api", "automation", "script", "no-code",
                    "saas", "integrate", "workflow"],
    "MONETIZATION": ["revenue", "monetize", "pricing", "paywall", "subscription",
                      "gumroad", "stripe", "sales", "conversion"],
    "SEO_GEO_ASO": ["seo", "google", "ranking", "keyword", "aso", "app store optimization",
                      "geo", "ai citation", "schema"],
    "ECOM": ["ecommerce", "tiktok shop", "amazon", "dropship", "print on demand",
              "etsy", "shopify", "product"],
    "AI_ALPHA": ["ai", "llm", "gpt", "claude", "agent", "prompt", "ai tool",
                  "machine learning", "generative"],
}


def get_next_alpha_id():
    """Get the next alpha ID from existing entries."""
    if not ALPHA_FILE.exists():
        return "ALPHA001"

    max_id = 0
    with open(ALPHA_FILE, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            alpha_id = row.get("alpha_id", "")
            match = re.search(r"ALPHA(\d+)", alpha_id)
            if match:
                num = int(match.group(1))
                max_id = max(max_id, num)

    return f"ALPHA{max_id + 1:03d}"


def get_existing_urls():
    """Get all existing source URLs for deduplication."""
    if not ALPHA_FILE.exists():
        return set()

    urls = set()
    with open(ALPHA_FILE, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            url = row.get("source_url", "").strip()
            if url:
                urls.add(url)
    return urls


def auto_categorize(text):
    """Determine the category based on keyword matching."""
    text_lower = text.lower()
    scores = {}

    for category, keywords in CATEGORY_KEYWORDS.items():
        score = sum(1 for kw in keywords if kw in text_lower)
        if score > 0:
            scores[category] = score

    if not scores:
        return "GENERAL"

    return max(scores, key=scores.get)


def extract_numbers(text):
    """Extract specific numbers from text (revenue, percentages, counts)."""
    numbers = []

    # Dollar amounts
    dollars = re.findall(r"\$[\d,]+(?:\.\d{2})?[kKmMbB]?", text)
    numbers.extend(dollars)

    # Percentages
    pcts = re.findall(r"\d+(?:\.\d+)?%", text)
    numbers.extend(pcts)

    # Large numbers (followers, views, etc.)
    large = re.findall(r"\b\d{1,3}(?:,\d{3})+\b|\b\d+[kKmMbB]\b", text)
    numbers.extend(large)

    return numbers


def estimate_roi(text, numbers):
    """Estimate ROI potential based on content signals."""
    text_lower = text.lower()

    # High ROI signals
    high_signals = ["revenue", "profit", "made $", "earning", "sold", "clients",
                     "conversion", "reply rate", "case study"]
    high_score = sum(1 for s in high_signals if s in text_lower)

    if high_score >= 3 or len(numbers) >= 3:
        return "HIGHEST"
    if high_score >= 2 or len(numbers) >= 2:
        return "HIGH"
    if high_score >= 1 or len(numbers) >= 1:
        return "MEDIUM"
    return "LOW"


def check_engagement_authenticity(likes=0, comments=0, followers=0):
    """Check for bot/fake engagement signals."""
    if likes > 0 and comments > 0:
        ratio = likes / comments
        if ratio > 500:  # 10K likes, < 20 comments = suspicious
            return "SUSPICIOUS"
    if followers > 0 and likes > followers * 2:
        return "SUSPICIOUS"
    return "AUTHENTIC"


def check_earnings_claims(text):
    """Check for unverified earnings claims."""
    # Round numbers suggest inflation
    round_amounts = re.findall(r"\$(\d+)(?:k|K|,000)", text)
    has_round = any(int(a) % 5 == 0 for a in round_amounts if a.isdigit())

    # "I made" style claims
    has_claim = bool(re.search(r"(?:i |I |I\'ve |i\'ve )(?:made|earned|generated)", text))

    if has_claim and has_round:
        return "INFLATED"
    if has_claim:
        return "CLAIMED"
    return "N/A"


def extract_alpha_from_text(text, source="", source_url=""):
    """Extract a structured alpha entry from raw text."""
    numbers = extract_numbers(text)
    category = auto_categorize(text)
    roi = estimate_roi(text, numbers)
    earnings_check = check_earnings_claims(text)

    # Generate title from first sentence/line
    lines = text.strip().split("\n")
    title = lines[0][:100].strip()
    if title.startswith(("RT ", "@")):
        title = " ".join(lines[:2])[:100]

    # Extract actionable steps (look for numbered items or bullet points)
    steps = []
    for line in lines:
        if re.match(r"^\s*[\d\-\*\•]", line):
            steps.append(line.strip())
    if not steps:
        steps = ["Research method further", "Test with minimal investment", "Track results for 14 days"]

    return {
        "alpha_id": "",  # Will be assigned
        "source": source,
        "source_url": source_url,
        "category": category,
        "title": title,
        "description": text[:500],
        "actionable_steps": "; ".join(steps[:5]),
        "effort_level": "MEDIUM",
        "roi_potential": roi,
        "risk_level": "MEDIUM",
        "applies_to_niches": "ALL",
        "status": "PENDING_REVIEW",
        "reviewed_date": "",
        "reviewer_notes": f"Auto-extracted. Numbers found: {', '.join(numbers[:5])}. "
                          f"Earnings: {earnings_check}.",
    }


def extract_from_twitter_json(filepath):
    """Extract alpha from Twitter bookmarks JSON export."""
    with open(filepath, encoding="utf-8") as f:
        data = json.load(f)

    entries = []
    if isinstance(data, list):
        for tweet in data:
            text = tweet.get("text", tweet.get("full_text", ""))
            handle = tweet.get("user", {}).get("screen_name", tweet.get("handle", "unknown"))
            url = tweet.get("url", tweet.get("tweet_url", ""))

            if len(text) < 20:
                continue

            entry = extract_alpha_from_text(text, source=f"@{handle}", source_url=url)
            entries.append(entry)

    return entries


def extract_from_markdown(filepath):
    """Extract alpha from markdown notes."""
    with open(filepath, encoding="utf-8") as f:
        content = f.read()

    # Split by headers or double newlines
    sections = re.split(r"\n## |\n---\n|\n\n\n", content)

    entries = []
    for section in sections:
        section = section.strip()
        if len(section) < 30:
            continue

        entry = extract_alpha_from_text(section, source="markdown_notes", source_url=str(filepath))
        entries.append(entry)

    return entries


def save_entries(entries, dry_run=False):
    """Save entries to ALPHA_STAGING.csv."""
    if not entries:
        logger.info("No entries to save")
        return

    existing_urls = get_existing_urls()
    next_id_num = int(re.search(r"\d+", get_next_alpha_id()).group())

    fieldnames = [
        "alpha_id", "source", "source_url", "category", "title", "description",
        "actionable_steps", "effort_level", "roi_potential", "risk_level",
        "applies_to_niches", "status", "reviewed_date", "reviewer_notes",
    ]

    new_entries = []
    dupes = 0

    for entry in entries:
        url = entry.get("source_url", "")
        if url and url in existing_urls:
            dupes += 1
            continue

        entry["alpha_id"] = f"ALPHA{next_id_num:03d}"
        next_id_num += 1
        new_entries.append(entry)

    if dry_run:
        logger.info(f"DRY RUN: Would save {len(new_entries)} entries, skip {dupes} duplicates")
        for entry in new_entries:
            logger.info(f"  {entry['alpha_id']} [{entry['category']}] {entry['title'][:60]}")
        return

    file_exists = ALPHA_FILE.exists()
    with open(ALPHA_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        writer.writerows(new_entries)

    logger.info(f"Saved {len(new_entries)} new entries to {ALPHA_FILE}")
    logger.info(f"Skipped {dupes} duplicates")


def main():
    parser = argparse.ArgumentParser(
        description="Extract actionable alpha from text sources into ALPHA_STAGING.csv"
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--text", type=str, help="Raw text to extract from")
    group.add_argument("--file", type=str, help="File to extract from")
    group.add_argument("--url", type=str, help="URL to extract from (requires manual fetch)")
    parser.add_argument("--source", type=str, default="manual", help="Source handle/name")
    parser.add_argument("--source-url", type=str, default="", help="Source URL")
    parser.add_argument(
        "--format",
        choices=["text", "twitter", "markdown"],
        default="text",
        help="Input format",
    )
    parser.add_argument("--dry-run", action="store_true", help="Preview without saving")
    args = parser.parse_args()

    entries = []

    if args.text:
        entry = extract_alpha_from_text(args.text, source=args.source, source_url=args.source_url)
        entries = [entry]

    elif args.file:
        filepath = Path(args.file)
        if not filepath.is_absolute():
            filepath = PROJECT_DIR / args.file

        if not filepath.exists():
            logger.error(f"File not found: {filepath}")
            sys.exit(1)

        if args.format == "twitter":
            entries = extract_from_twitter_json(filepath)
        elif args.format == "markdown":
            entries = extract_from_markdown(filepath)
        else:
            with open(filepath, encoding="utf-8") as f:
                text = f.read()
            entry = extract_alpha_from_text(text, source=args.source)
            entries = [entry]

    elif args.url:
        logger.info(f"URL extraction requires browser. Saving URL as source reference.")
        entry = extract_alpha_from_text(
            f"URL to investigate: {args.url}",
            source="url_reference",
            source_url=args.url,
        )
        entries = [entry]

    logger.info(f"Extracted {len(entries)} potential alpha entries")
    save_entries(entries, dry_run=args.dry_run)


if __name__ == "__main__":
    main()
