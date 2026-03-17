#!/usr/bin/env python3
"""
platform_rpm_tracking.py - Track RPM/CPM rates across platforms
Scrapes Reddit and web search for latest RPM reports by platform and niche.
Output: LEDGER/PLATFORM_RPM_TRACKER.csv
Schedule: WEEKLY
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
OUTPUT_CSV = BASE_DIR / "LEDGER" / "PLATFORM_RPM_TRACKER.csv"
CSV_COLUMNS = ["date", "platform", "niche", "rpm_low", "rpm_high", "rpm_median", "source", "notes"]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
}

# Platforms and their known RPM ranges (baseline data to supplement web scraping)
PLATFORM_RPM_BASELINE = {
    "YouTube": {
        "general": {"low": 2.0, "high": 12.0, "median": 5.0, "notes": "Standard AdSense RPM. Varies hugely by niche."},
        "finance": {"low": 10.0, "high": 40.0, "median": 20.0, "notes": "Highest RPM niche on YouTube."},
        "tech": {"low": 5.0, "high": 20.0, "median": 10.0, "notes": "Good RPM. Software/SaaS ads pay well."},
        "fitness": {"low": 3.0, "high": 12.0, "median": 6.0, "notes": "Supplement and fitness product ads."},
        "faith": {"low": 1.5, "high": 8.0, "median": 3.5, "notes": "Lower RPM but high engagement and loyalty."},
        "sleep": {"low": 3.0, "high": 15.0, "median": 7.0, "notes": "Sleep product/mattress ads pay well."},
        "entertainment": {"low": 1.0, "high": 5.0, "median": 2.5, "notes": "High volume, low RPM."},
    },
    "YouTube Shorts": {
        "general": {"low": 0.01, "high": 0.10, "median": 0.04, "notes": "Shorts RPM is 10-50x lower than long-form."},
        "tech": {"low": 0.03, "high": 0.15, "median": 0.07, "notes": "Slightly higher for tech shorts."},
        "fitness": {"low": 0.02, "high": 0.08, "median": 0.04, "notes": "Fitness shorts perform average."},
    },
    "TikTok": {
        "general": {"low": 0.02, "high": 0.10, "median": 0.05, "notes": "Creativity Program Beta. Must have 10K+ followers."},
        "tech": {"low": 0.03, "high": 0.12, "median": 0.06, "notes": "Tech niche slightly above average."},
        "fitness": {"low": 0.02, "high": 0.08, "median": 0.04, "notes": "Fitness content average RPM."},
        "entertainment": {"low": 0.01, "high": 0.05, "median": 0.02, "notes": "High volume, lowest RPM."},
    },
    "Instagram Reels": {
        "general": {"low": 0.01, "high": 0.05, "median": 0.02, "notes": "Reels Play Bonus program. Invite-only, being phased."},
        "fitness": {"low": 0.01, "high": 0.06, "median": 0.03, "notes": "Fitness reels can earn through brand deals instead."},
    },
    "Medium": {
        "general": {"low": 50.0, "high": 500.0, "median": 150.0, "notes": "Per 1000 reads. Partner Program. Highly variable."},
        "tech": {"low": 80.0, "high": 800.0, "median": 200.0, "notes": "Tech/programming articles perform well."},
        "finance": {"low": 100.0, "high": 1000.0, "median": 300.0, "notes": "Finance articles have highest Medium RPM."},
    },
    "Substack": {
        "general": {"low": 0.0, "high": 0.0, "median": 0.0, "notes": "No ad RPM. Revenue from paid subscriptions. Avg $5-15/mo per subscriber."},
        "tech": {"low": 0.0, "high": 0.0, "median": 0.0, "notes": "Tech newsletters avg $10/mo. Conversion 5-10% free to paid."},
    },
    "X/Twitter": {
        "general": {"low": 0.50, "high": 5.0, "median": 2.0, "notes": "X Premium revenue sharing. Per 1M impressions."},
        "tech": {"low": 1.0, "high": 8.0, "median": 3.0, "notes": "Tech content premium rate."},
    },
    "Beehiiv": {
        "general": {"low": 0.0, "high": 0.0, "median": 0.0, "notes": "No native RPM. Revenue from Beehiiv Ad Network or paid subs. Ad network ~$2-5 CPM."},
    },
}

# Reddit search queries for RPM data
REDDIT_RPM_QUERIES = [
    ("youtube", "YouTube RPM 2026 OR RPM per mille OR ad revenue"),
    ("NewTubers", "RPM OR CPM OR ad revenue 2026"),
    ("juststart", "RPM OR ad revenue OR display ads 2026"),
    ("blogging", "RPM OR Mediavine OR AdThrive 2026"),
    ("Medium", "earnings OR partner program OR per read 2026"),
]

# Web search queries
WEB_RPM_QUERIES = [
    "YouTube RPM by niche 2026",
    "TikTok creator program RPM 2026",
    "Instagram Reels monetization rate 2026",
    "Medium partner program earnings per read 2026",
    "Twitter X creator revenue sharing RPM 2026",
    "YouTube Shorts RPM 2026",
    "Beehiiv newsletter ad rates 2026",
    "Substack paid subscription conversion rate 2026",
]


def init_csv():
    """Create CSV with headers if it doesn't exist."""
    if not OUTPUT_CSV.exists():
        OUTPUT_CSV.parent.mkdir(parents=True, exist_ok=True)
        with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(CSV_COLUMNS)
        print(f"[+] Created {OUTPUT_CSV}")


def load_existing():
    """Load existing entries to check what we have."""
    entries = set()
    if OUTPUT_CSV.exists():
        with open(OUTPUT_CSV, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                key = f"{row.get('date','')}|{row.get('platform','')}|{row.get('niche','')}"
                entries.add(key)
    return entries


def write_baseline(existing):
    """Write baseline RPM data from known sources."""
    today = datetime.now().strftime("%Y-%m-%d")
    results = []

    for platform, niches in PLATFORM_RPM_BASELINE.items():
        for niche, data in niches.items():
            key = f"{today}|{platform}|{niche}"
            if key in existing:
                continue
            results.append({
                "date": today,
                "platform": platform,
                "niche": niche,
                "rpm_low": data["low"],
                "rpm_high": data["high"],
                "rpm_median": data["median"],
                "source": "industry_baseline_feb2026",
                "notes": data["notes"],
            })

    return results


def extract_rpm_from_text(text):
    """Extract RPM/CPM numbers from text."""
    rpms = []
    # Patterns: $X RPM, $X CPM, RPM of $X, $X per 1000, $X per mille
    patterns = [
        r'\$?([\d.]+)\s*(?:rpm|per\s*(?:1000|mille|1k))',
        r'(?:rpm|cpm)\s*(?:of|is|was|around|about|~)?\s*\$?([\d.]+)',
        r'\$?([\d.]+)\s*(?:cpm)',
        r'(?:earn|made|get|got|making)\s*\$?([\d.]+)\s*(?:per\s*1000|rpm)',
    ]
    for pattern in patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        for m in matches:
            try:
                val = float(m)
                if 0.001 <= val <= 10000:  # Reasonable RPM range
                    rpms.append(val)
            except ValueError:
                continue
    return rpms


def scrape_reddit_rpm(session, existing):
    """Search Reddit for RPM data."""
    results = []
    today = datetime.now().strftime("%Y-%m-%d")

    for sub, query in REDDIT_RPM_QUERIES:
        url = f"https://www.reddit.com/r/{sub}/search.json?q={quote_plus(query)}&restrict_sr=1&sort=new&limit=10&t=month"
        try:
            time.sleep(2)
            resp = session.get(url, headers={**HEADERS, "User-Agent": "PRINTMAXX-RPMTracker/1.0"}, timeout=15)
            if resp.status_code != 200:
                print(f"  [-] r/{sub}: HTTP {resp.status_code}")
                continue
            data = resp.json()
            posts = data.get("data", {}).get("children", [])
            for post in posts:
                pd = post.get("data", {})
                title = pd.get("title", "")
                selftext = pd.get("selftext", "")[:1000]
                permalink = pd.get("permalink", "")
                full_text = f"{title} {selftext}"

                rpms = extract_rpm_from_text(full_text)
                if not rpms:
                    continue

                # Determine platform from context
                platform = "Unknown"
                text_lower = full_text.lower()
                if "youtube" in text_lower or "yt " in text_lower:
                    platform = "YouTube"
                elif "tiktok" in text_lower or "tt " in text_lower:
                    platform = "TikTok"
                elif "instagram" in text_lower or " ig " in text_lower:
                    platform = "Instagram"
                elif "medium" in text_lower:
                    platform = "Medium"
                elif "twitter" in text_lower or " x " in text_lower:
                    platform = "X/Twitter"

                # Determine niche
                niche = "general"
                for n in ["tech", "finance", "fitness", "faith", "gaming", "food", "travel", "beauty"]:
                    if n in text_lower:
                        niche = n
                        break

                key = f"{today}|{platform}|{niche}"
                if key in existing:
                    continue
                existing.add(key)

                rpm_low = min(rpms)
                rpm_high = max(rpms)
                rpm_median = sorted(rpms)[len(rpms)//2]

                results.append({
                    "date": today,
                    "platform": platform,
                    "niche": niche,
                    "rpm_low": round(rpm_low, 2),
                    "rpm_high": round(rpm_high, 2),
                    "rpm_median": round(rpm_median, 2),
                    "source": f"reddit.com/r/{sub}",
                    "notes": title[:150],
                })
            print(f"  [+] r/{sub}: found {len(results)} RPM data points")
        except Exception as e:
            print(f"  [-] r/{sub} error: {e}")
    return results


def search_brave_rpm(session, existing):
    """Search web for RPM data."""
    results = []
    today = datetime.now().strftime("%Y-%m-%d")

    for query in WEB_RPM_QUERIES:
        search_url = f"https://search.brave.com/search?q={quote_plus(query)}&source=web"
        try:
            time.sleep(2)
            resp = session.get(search_url, headers=HEADERS, timeout=15)
            if resp.status_code != 200:
                print(f"  [-] Brave '{query}': HTTP {resp.status_code}")
                continue
            soup = BeautifulSoup(resp.text, "html.parser")

            for result in soup.select(".snippet")[:5]:
                title_el = result.select_one(".snippet-title")
                desc_el = result.select_one(".snippet-description")
                link_el = result.select_one("a")
                if not title_el:
                    continue

                title = title_el.get_text(strip=True)
                desc = desc_el.get_text(strip=True) if desc_el else ""
                url = link_el.get("href", "") if link_el else ""
                full_text = f"{title} {desc}"

                rpms = extract_rpm_from_text(full_text)
                if not rpms:
                    continue

                # Determine platform
                platform = "Unknown"
                text_lower = full_text.lower()
                if "youtube" in text_lower:
                    platform = "YouTube Shorts" if "shorts" in text_lower else "YouTube"
                elif "tiktok" in text_lower:
                    platform = "TikTok"
                elif "instagram" in text_lower:
                    platform = "Instagram Reels"
                elif "medium" in text_lower:
                    platform = "Medium"
                elif "twitter" in text_lower or " x " in text_lower:
                    platform = "X/Twitter"
                elif "substack" in text_lower:
                    platform = "Substack"
                elif "beehiiv" in text_lower:
                    platform = "Beehiiv"

                niche = "general"
                for n in ["tech", "finance", "fitness", "faith", "gaming"]:
                    if n in text_lower:
                        niche = n
                        break

                key = f"{today}|{platform}|{niche}"
                if key in existing:
                    continue
                existing.add(key)

                results.append({
                    "date": today,
                    "platform": platform,
                    "niche": niche,
                    "rpm_low": round(min(rpms), 2),
                    "rpm_high": round(max(rpms), 2),
                    "rpm_median": round(sorted(rpms)[len(rpms)//2], 2),
                    "source": url[:200] if url else "brave_search",
                    "notes": title[:150],
                })
            print(f"  [+] Brave '{query}': extracted RPM data")
        except Exception as e:
            print(f"  [-] Brave error '{query}': {e}")
    return results


def write_results(results):
    """Append results to CSV."""
    if not results:
        print("[!] No new results to write.")
        return 0

    with open(OUTPUT_CSV, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_COLUMNS)
        for row in results:
            writer.writerow(row)

    print(f"[+] Wrote {len(results)} entries to {OUTPUT_CSV}")
    return len(results)


def main():
    print("=" * 60)
    print("PLATFORM RPM TRACKING - PRINTMAXX")
    print(f"Run time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

    init_csv()
    existing = load_existing()
    session = requests.Session()
    all_results = []

    # Phase 1: Baseline data
    print("\n[Phase 1] Writing baseline RPM data...")
    baseline = write_baseline(existing)
    all_results.extend(baseline)
    for r in baseline:
        existing.add(f"{r['date']}|{r['platform']}|{r['niche']}")
    print(f"  [+] {len(baseline)} baseline entries")

    # Phase 2: Reddit RPM data
    print("\n[Phase 2] Scraping Reddit for RPM reports...")
    reddit_results = scrape_reddit_rpm(session, existing)
    all_results.extend(reddit_results)

    # Phase 3: Web search RPM data
    print("\n[Phase 3] Searching web for RPM data...")
    web_results = search_brave_rpm(session, existing)
    all_results.extend(web_results)

    # Write all results
    print("\n[Phase 4] Writing results...")
    count = write_results(all_results)

    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    by_platform = {}
    for r in all_results:
        p = r["platform"]
        by_platform[p] = by_platform.get(p, 0) + 1
    for p, c in sorted(by_platform.items()):
        print(f"  {p}: {c} RPM data points")
    print(f"\n  TOTAL: {count} entries written")
    print(f"  Output: {OUTPUT_CSV}")

    # Top RPM opportunities
    print("\n  TOP RPM OPPORTUNITIES:")
    sorted_results = sorted(all_results, key=lambda x: float(x.get("rpm_median", 0)), reverse=True)
    for r in sorted_results[:5]:
        print(f"    {r['platform']} ({r['niche']}): ${r['rpm_median']} median RPM")
    print("=" * 60)

    return count


if __name__ == "__main__":
    count = main()
    sys.exit(0)
