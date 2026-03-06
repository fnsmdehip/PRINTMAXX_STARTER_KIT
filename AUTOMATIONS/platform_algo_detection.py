#!/usr/bin/env python3
"""
platform_algo_detection.py - Monitor platform algorithm changes
Scrapes Reddit + official newsrooms for TikTok, X, Instagram, YouTube algo changes.
Output: LEDGER/PLATFORM_ALGO_CHANGES.csv
Schedule: DAILY
"""

import csv
import json
import os
import re
import sys
import time
from datetime import datetime, timedelta
from pathlib import Path
from urllib.parse import quote_plus

try:
    import requests
    from bs4 import BeautifulSoup
except ImportError as e:
    print(f"ERROR: Missing dependency: {e}")
    print("Install with: pip3 install requests beautifulsoup4")
    sys.exit(1)

BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT_CSV = BASE_DIR / "LEDGER" / "PLATFORM_ALGO_CHANGES.csv"
CSV_COLUMNS = ["date", "platform", "change_type", "description", "source_url", "impact_level", "action_required"]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
}

# Reddit subreddits to monitor
REDDIT_SUBS = {
    "TikTok": ["TikTokCreators", "Tiktokhelp", "socialmediamarketing"],
    "Instagram": ["Instagram", "InstagramMarketing", "socialmediamarketing"],
    "YouTube": ["youtube", "youtubers", "NewTubers"],
    "X/Twitter": ["Twitter", "socialmediamarketing"],
}

# Search queries for algorithm changes
ALGO_QUERIES = [
    "TikTok algorithm change 2026",
    "Instagram algorithm update 2026",
    "YouTube algorithm change 2026",
    "Twitter X algorithm update 2026",
    "TikTok reach dropping 2026",
    "Instagram reels algorithm 2026",
    "YouTube shorts algorithm 2026",
]

# Keywords that signal algorithm changes
ALGO_KEYWORDS = [
    "algorithm", "algo", "reach", "impressions", "shadowban", "views dropped",
    "engagement rate", "distribution", "for you page", "fyp", "explore page",
    "recommended", "suggested", "feed change", "update", "rollout", "new feature",
    "monetization change", "creator fund", "partner program", "policy update",
]


def init_csv():
    """Create CSV with headers if it doesn't exist."""
    if not OUTPUT_CSV.exists():
        OUTPUT_CSV.parent.mkdir(parents=True, exist_ok=True)
        with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(CSV_COLUMNS)
        print(f"[+] Created {OUTPUT_CSV}")


def load_existing_urls():
    """Load existing source URLs to avoid duplicates."""
    urls = set()
    if OUTPUT_CSV.exists():
        with open(OUTPUT_CSV, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if "source_url" in row:
                    urls.add(row["source_url"])
    return urls


def classify_impact(text):
    """Classify impact level based on content."""
    text_lower = text.lower()
    high_signals = ["shadowban", "demonetiz", "removed", "banned", "suspended", "major update", "huge change", "breaking"]
    medium_signals = ["algorithm", "reach drop", "views down", "engagement drop", "new feature", "rollout", "update"]
    if any(s in text_lower for s in high_signals):
        return "HIGH"
    if any(s in text_lower for s in medium_signals):
        return "MEDIUM"
    return "LOW"


def classify_platform(text):
    """Detect which platform a post is about."""
    text_lower = text.lower()
    platforms = []
    if any(w in text_lower for w in ["tiktok", "tt", "fyp", "for you page"]):
        platforms.append("TikTok")
    if any(w in text_lower for w in ["instagram", "ig", "reels", "explore page"]):
        platforms.append("Instagram")
    if any(w in text_lower for w in ["youtube", "yt", "shorts", "youtube partner"]):
        platforms.append("YouTube")
    if any(w in text_lower for w in ["twitter", " x ", "x/twitter", "elon", "tweet"]):
        platforms.append("X/Twitter")
    return platforms if platforms else ["Unknown"]


def classify_change_type(text):
    """Classify the type of algorithm change."""
    text_lower = text.lower()
    if any(w in text_lower for w in ["monetiz", "fund", "payout", "rpm", "cpm", "revenue"]):
        return "monetization"
    if any(w in text_lower for w in ["shadowban", "ban", "restrict", "removed", "violation"]):
        return "enforcement"
    if any(w in text_lower for w in ["algorithm", "algo", "reach", "distribution", "impression"]):
        return "algorithm"
    if any(w in text_lower for w in ["new feature", "launched", "rolling out", "beta", "test"]):
        return "feature"
    if any(w in text_lower for w in ["policy", "tos", "terms", "guideline", "rule"]):
        return "policy"
    return "general"


def generate_action(change_type, impact, platform):
    """Generate action recommendation."""
    actions = {
        ("monetization", "HIGH"): f"Review {platform} monetization settings immediately. Check payout dashboard.",
        ("monetization", "MEDIUM"): f"Monitor {platform} RPM for next 7 days. Track in RPM tracker.",
        ("enforcement", "HIGH"): f"Audit all {platform} content for compliance. Pause automation.",
        ("enforcement", "MEDIUM"): f"Review {platform} content guidelines. Check flagged content.",
        ("algorithm", "HIGH"): f"Test new content formats on {platform}. A/B test posting times.",
        ("algorithm", "MEDIUM"): f"Monitor {platform} analytics for reach changes this week.",
        ("feature", "HIGH"): f"Test new {platform} feature immediately for early-mover advantage.",
        ("feature", "MEDIUM"): f"Evaluate new {platform} feature for our content strategy.",
        ("policy", "HIGH"): f"Review all {platform} content against new policy. Update compliance checklist.",
        ("policy", "MEDIUM"): f"Read new {platform} policy. Flag any content that may be affected.",
    }
    return actions.get((change_type, impact), f"Monitor {platform} for further developments.")


def scrape_reddit_sub(subreddit, session, existing_urls):
    """Scrape a subreddit for algorithm-related posts."""
    results = []
    url = f"https://www.reddit.com/r/{subreddit}/new.json?limit=25"
    try:
        time.sleep(2)  # Rate limit
        resp = session.get(url, headers={**HEADERS, "User-Agent": "PRINTMAXX-AlgoDetector/1.0"}, timeout=15)
        if resp.status_code != 200:
            print(f"  [-] Reddit r/{subreddit}: HTTP {resp.status_code}")
            return results
        data = resp.json()
        posts = data.get("data", {}).get("children", [])
        for post in posts:
            pd = post.get("data", {})
            title = pd.get("title", "")
            selftext = pd.get("selftext", "")[:500]
            permalink = pd.get("permalink", "")
            created = pd.get("created_utc", 0)
            score = pd.get("score", 0)
            full_text = f"{title} {selftext}".lower()

            # Filter: must mention algorithm-related keywords
            if not any(kw in full_text for kw in ALGO_KEYWORDS):
                continue

            # Filter: must be recent (within 7 days)
            post_date = datetime.fromtimestamp(created)
            if datetime.now() - post_date > timedelta(days=7):
                continue

            source_url = f"https://www.reddit.com{permalink}"
            if source_url in existing_urls:
                continue

            platforms = classify_platform(full_text)
            change_type = classify_change_type(full_text)
            impact = classify_impact(full_text)
            description = title[:200]

            for platform in platforms:
                action = generate_action(change_type, impact, platform)
                results.append({
                    "date": post_date.strftime("%Y-%m-%d"),
                    "platform": platform,
                    "change_type": change_type,
                    "description": description,
                    "source_url": source_url,
                    "impact_level": impact,
                    "action_required": action,
                })
        print(f"  [+] r/{subreddit}: {len(results)} algo-related posts found")
    except Exception as e:
        print(f"  [-] r/{subreddit} error: {e}")
    return results


def search_brave(query, session, existing_urls):
    """Search Brave for algorithm change news."""
    results = []
    search_url = f"https://search.brave.com/search?q={quote_plus(query)}&source=web"
    try:
        time.sleep(2)
        resp = session.get(search_url, headers=HEADERS, timeout=15)
        if resp.status_code != 200:
            print(f"  [-] Brave search for '{query}': HTTP {resp.status_code}")
            return results
        soup = BeautifulSoup(resp.text, "html.parser")

        # Parse search results
        for result in soup.select(".snippet")[:5]:
            title_el = result.select_one(".snippet-title")
            desc_el = result.select_one(".snippet-description")
            link_el = result.select_one("a")

            if not title_el or not link_el:
                continue

            title = title_el.get_text(strip=True)
            desc = desc_el.get_text(strip=True) if desc_el else ""
            url = link_el.get("href", "")

            if url in existing_urls:
                continue

            full_text = f"{title} {desc}".lower()
            if not any(kw in full_text for kw in ALGO_KEYWORDS):
                continue

            platforms = classify_platform(full_text)
            change_type = classify_change_type(full_text)
            impact = classify_impact(full_text)

            for platform in platforms:
                action = generate_action(change_type, impact, platform)
                results.append({
                    "date": datetime.now().strftime("%Y-%m-%d"),
                    "platform": platform,
                    "change_type": change_type,
                    "description": title[:200],
                    "source_url": url,
                    "impact_level": impact,
                    "action_required": action,
                })
        print(f"  [+] Brave '{query}': {len(results)} results")
    except Exception as e:
        print(f"  [-] Brave search error for '{query}': {e}")
    return results


def write_results(results):
    """Append results to CSV."""
    if not results:
        print("[!] No new results to write.")
        return 0

    # Deduplicate by source_url + platform
    seen = set()
    unique = []
    for r in results:
        key = f"{r['source_url']}|{r['platform']}"
        if key not in seen:
            seen.add(key)
            unique.append(r)

    with open(OUTPUT_CSV, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_COLUMNS)
        for row in unique:
            writer.writerow(row)

    print(f"[+] Wrote {len(unique)} new entries to {OUTPUT_CSV}")
    return len(unique)


def main():
    print("=" * 60)
    print("PLATFORM ALGO DETECTION - PRINTMAXX")
    print(f"Run time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

    init_csv()
    existing_urls = load_existing_urls()
    session = requests.Session()
    all_results = []

    # Phase 1: Reddit scraping
    print("\n[Phase 1] Scanning Reddit for algorithm changes...")
    for platform, subs in REDDIT_SUBS.items():
        for sub in subs:
            results = scrape_reddit_sub(sub, session, existing_urls)
            all_results.extend(results)

    # Phase 2: Brave search for recent changes
    print("\n[Phase 2] Searching web for algorithm updates...")
    for query in ALGO_QUERIES:
        results = search_brave(query, session, existing_urls)
        all_results.extend(results)

    # Write results
    print("\n[Phase 3] Writing results...")
    count = write_results(all_results)

    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    platforms = {}
    for r in all_results:
        p = r["platform"]
        platforms[p] = platforms.get(p, 0) + 1
    for p, c in sorted(platforms.items()):
        print(f"  {p}: {c} changes detected")
    print(f"  TOTAL: {count} new entries written")
    print(f"  Output: {OUTPUT_CSV}")
    print("=" * 60)

    return count


if __name__ == "__main__":
    count = main()
    sys.exit(0)
