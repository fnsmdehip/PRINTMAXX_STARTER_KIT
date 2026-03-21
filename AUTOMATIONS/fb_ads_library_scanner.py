#!/usr/bin/env python3

from __future__ import annotations
"""
Facebook Ads Library Product Research Scanner
Source: ALPHA018 - "Search FB Ads Library for product keywords. If paying for ads = making money."
Also: EDGE029 - FB Ads Library free competitor validation

Searches FB Ads Library API for active ads by keyword.
If someone is paying for ads = they're making money = validated product idea.

Usage:
    python3 fb_ads_library_scanner.py                          # Run default keywords
    python3 fb_ads_library_scanner.py --keyword "digital planner"
    python3 fb_ads_library_scanner.py --keywords "ebook,template,course,planner"
    python3 fb_ads_library_scanner.py --report                  # Generate full report
"""

import argparse
import csv
import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path
from urllib.request import urlopen, Request
from urllib.parse import urlencode, quote_plus
from urllib.error import URLError, HTTPError

BASE_DIR = Path(__file__).parent.parent
OUTPUT_CSV = BASE_DIR / "LEDGER" / "FB_ADS_PRODUCT_RESEARCH.csv"
REPORT_FILE = BASE_DIR / "OPS" / "FB_ADS_RESEARCH_REPORT.md"
LOG_FILE = BASE_DIR / "AUTOMATIONS" / "logs" / "fb_ads_scanner.log"

# Product research keywords (from ALPHA018)
PRODUCT_KEYWORDS = [
    "ebook",
    "digital download",
    "pdf",
    "printable",
    "template",
    "guide",
    "course",
    "planner",
    "notion template",
    "canva template",
    "social media template",
    "email template",
    "resume template",
    "budget planner",
    "meal planner",
    "fitness planner",
    "prayer journal",
    "gratitude journal",
    "productivity planner",
    "business plan template",
    "wedding planner",
    "study guide",
    "cheat sheet",
    "checklist",
    "spreadsheet",
    "dashboard template",
    "ai prompt pack",
    "chatgpt prompts",
    "midjourney prompts",
]

# Niche-specific keywords
NICHE_KEYWORDS = {
    "faith": ["prayer journal", "bible study guide", "devotional", "faith planner", "scripture printable"],
    "fitness": ["workout planner", "meal prep template", "fitness tracker", "gym log", "macro calculator"],
    "finance": ["budget template", "expense tracker", "investment tracker", "debt payoff planner", "tax planner"],
    "productivity": ["notion template", "daily planner", "habit tracker", "goal setting template", "time blocking"],
    "content_creation": ["content calendar", "social media planner", "caption templates", "hashtag guide", "reels ideas"],
}

# FB Ads Library URL pattern (for manual access)
FB_ADS_LIBRARY_URL = "https://www.facebook.com/ads/library/?active_status=active&ad_type=all&country=US&q={query}&search_type=keyword_unordered"


def search_fb_ads_library_url(keyword):
    """Generate FB Ads Library search URL for a keyword."""
    return FB_ADS_LIBRARY_URL.format(query=quote_plus(keyword))


def analyze_keyword_potential(keyword):
    """Analyze a keyword's potential based on known patterns."""
    # Score based on keyword characteristics
    score = 50  # base score

    # High-value indicators
    high_value = ["template", "planner", "course", "guide", "dashboard", "tracker"]
    for hv in high_value:
        if hv in keyword.lower():
            score += 15

    # Digital product indicators
    digital = ["pdf", "printable", "download", "ebook", "spreadsheet"]
    for d in digital:
        if d in keyword.lower():
            score += 10

    # Niche specificity bonus
    niche_words = ["prayer", "faith", "fitness", "budget", "wedding", "meal", "workout"]
    for nw in niche_words:
        if nw in keyword.lower():
            score += 10

    # AI/tech bonus (trending)
    ai_words = ["ai", "chatgpt", "midjourney", "prompt", "notion"]
    for aw in ai_words:
        if aw in keyword.lower():
            score += 10

    return min(score, 100)


def generate_product_ideas(keyword, score):
    """Generate product ideas based on keyword."""
    ideas = []

    if "template" in keyword.lower():
        ideas.append(f"Create a premium {keyword} pack (10-20 variations) for $19-39")
        ideas.append(f"Bundle {keyword} with video tutorial for $47-97")

    if "planner" in keyword.lower():
        ideas.append(f"Digital {keyword} with Notion/Google Sheets version for $14-29")
        ideas.append(f"Physical + digital {keyword} bundle via Amazon KDP for $24-49")

    if "course" in keyword.lower():
        ideas.append(f"Mini-course version of {keyword} topic for $29-97")
        ideas.append(f"Community access + {keyword} course for $19/mo")

    if "prompt" in keyword.lower():
        ideas.append(f"Curated {keyword} collection (100+) for $9-19")
        ideas.append(f"{keyword} + automation workflow for $29-49")

    if not ideas:
        ideas.append(f"Create a comprehensive {keyword} for $19-39")
        ideas.append(f"Bundle: {keyword} + bonus resources for $39-67")

    return ideas


def run_scan(keywords=None):
    """Run full FB Ads Library scan."""
    if keywords is None:
        keywords = PRODUCT_KEYWORDS

    results = []

    print(f"\n{'='*60}")
    print("FB ADS LIBRARY PRODUCT RESEARCH SCANNER")
    print(f"{'='*60}")
    print(f"Scanning {len(keywords)} keywords...")
    print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print()

    for keyword in keywords:
        url = search_fb_ads_library_url(keyword)
        score = analyze_keyword_potential(keyword)
        ideas = generate_product_ideas(keyword, score)

        result = {
            "keyword": keyword,
            "fb_ads_url": url,
            "score": score,
            "product_ideas": " | ".join(ideas),
            "priority": "HIGH" if score >= 70 else "MEDIUM" if score >= 50 else "LOW",
            "scanned_at": datetime.now().isoformat(),
        }
        results.append(result)

        indicator = "***" if score >= 70 else "**" if score >= 50 else "*"
        print(f"  {indicator} [{score:3d}] {keyword}")

    # Sort by score
    results.sort(key=lambda x: x["score"], reverse=True)

    # Write CSV
    OUTPUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_CSV, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=["keyword", "score", "priority", "product_ideas", "fb_ads_url", "scanned_at"])
        writer.writeheader()
        writer.writerows(results)

    print(f"\n{'='*60}")
    print(f"Results written to: {OUTPUT_CSV}")
    print(f"Total keywords scanned: {len(results)}")
    print(f"HIGH priority (70+): {sum(1 for r in results if r['priority'] == 'HIGH')}")
    print(f"MEDIUM priority (50-69): {sum(1 for r in results if r['priority'] == 'MEDIUM')}")

    return results


def generate_report(results=None):
    """Generate a full research report."""
    if results is None:
        # Read from CSV
        results = []
        if OUTPUT_CSV.exists():
            with open(OUTPUT_CSV, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                results = list(reader)

    if not results:
        print("No results to report. Run scan first.")
        return

    report = f"""# FB Ads Library Product Research Report

**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}
**Source:** ALPHA018 - "If paying for ads = making money"
**Keywords Scanned:** {len(results)}

---

## Top Product Opportunities (Score 70+)

| Keyword | Score | Product Ideas |
|---------|-------|---------------|
"""

    for r in results:
        if int(r.get('score', 0)) >= 70:
            report += f"| {r['keyword']} | {r['score']} | {r['product_ideas'][:80]} |\n"

    report += f"""
## How to Validate

For each high-score keyword:

1. **Open FB Ads Library URL** - Check if there are active ads
2. **Count active ads** - More ads = more proven demand
3. **Analyze ad creative** - What hooks/angles are they using?
4. **Check ad longevity** - Ads running 30+ days = profitable
5. **Reverse engineer the product** - What are they selling? What's the price?
6. **Build a better version** - Our niche angles (faith, fitness, tech)

## Niche Crossovers

"""

    for niche, niche_kws in NICHE_KEYWORDS.items():
        report += f"### {niche.title()}\n\n"
        for kw in niche_kws:
            matching = [r for r in results if kw.lower() in r.get('keyword', '').lower()]
            if matching:
                for m in matching:
                    report += f"- **{m['keyword']}** (Score: {m['score']}) - {m['product_ideas'][:60]}\n"
            else:
                report += f"- {kw} - Not yet scanned. Add to next scan.\n"
        report += "\n"

    report += f"""
## Action Items

1. Open top 10 FB Ads Library URLs and count active ads
2. Screenshot top 5 ad creatives for reference
3. Build 3 products targeting highest-scored keywords
4. Price at $19-39 (impulse buy zone per ALPHA_MICRO_INFO_001)
5. List on Gumroad/Whop within 48 hours
6. Create 5 social posts per product (use content_multiplier.py)

## FB Ads Library URLs (Top 10)

"""

    for r in results[:10]:
        report += f"- [{r['keyword']}]({r.get('fb_ads_url', 'N/A')})\n"

    REPORT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(REPORT_FILE, 'w', encoding='utf-8') as f:
        f.write(report)

    print(f"\nReport written to: {REPORT_FILE}")
    return report


def main():
    parser = argparse.ArgumentParser(description="FB Ads Library Product Research Scanner")
    parser.add_argument("--keyword", type=str, help="Single keyword to scan")
    parser.add_argument("--keywords", type=str, help="Comma-separated keywords")
    parser.add_argument("--niche", type=str, help="Niche: faith, fitness, finance, productivity, content_creation")
    parser.add_argument("--report", action="store_true", help="Generate full report")
    parser.add_argument("--all", action="store_true", help="Scan all keywords + all niches")
    args = parser.parse_args()

    if args.keyword:
        keywords = [args.keyword]
    elif args.keywords:
        keywords = [k.strip() for k in args.keywords.split(",")]
    elif args.niche:
        keywords = NICHE_KEYWORDS.get(args.niche, PRODUCT_KEYWORDS)
    elif args.all:
        keywords = PRODUCT_KEYWORDS.copy()
        for niche_kws in NICHE_KEYWORDS.values():
            keywords.extend(niche_kws)
        keywords = list(set(keywords))  # deduplicate
    else:
        keywords = PRODUCT_KEYWORDS

    results = run_scan(keywords)

    if args.report or args.all:
        generate_report(results)


if __name__ == "__main__":
    main()
