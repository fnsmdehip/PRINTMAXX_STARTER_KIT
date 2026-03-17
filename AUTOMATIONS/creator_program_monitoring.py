#!/usr/bin/env python3
"""
creator_program_monitoring.py - Monitor creator monetization programs
Tracks changes to TikTok, YouTube, Instagram, X, Medium, Substack creator programs.
Output: LEDGER/CREATOR_PROGRAMS.csv
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
OUTPUT_CSV = BASE_DIR / "LEDGER" / "CREATOR_PROGRAMS.csv"
CSV_COLUMNS = ["date", "platform", "program_name", "status", "requirements", "payout_rate", "changes", "source_url"]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
}

# Known creator programs with baseline data
CREATOR_PROGRAMS = [
    {
        "platform": "TikTok",
        "program_name": "Creativity Program Beta",
        "status": "active",
        "requirements": "10K+ followers, 100K views in 30 days, 18+, US/UK/FR/DE/BR/KR/JP, videos >1min",
        "payout_rate": "$0.50-$1.00 per 1000 qualified views",
        "changes": "Replaced original Creator Fund. Higher payouts for longer content (>1min).",
        "source_url": "https://www.tiktok.com/creators/creator-portal/en-us/getting-paid-to-create/creativity-program-beta/",
    },
    {
        "platform": "TikTok",
        "program_name": "TikTok Shop Affiliate",
        "status": "active",
        "requirements": "1K+ followers, 18+, US based",
        "payout_rate": "5-30% commission on product sales",
        "changes": "Growing fast. Small creators (<50K) get 4.3x higher CTR than large accounts.",
        "source_url": "https://shop.tiktok.com/business/en/creator",
    },
    {
        "platform": "YouTube",
        "program_name": "YouTube Partner Program (YPP)",
        "status": "active",
        "requirements": "500 subscribers + 3 uploads in 90 days + (3K watch hours OR 3M Shorts views in 90 days)",
        "payout_rate": "45% Shorts ad revenue, 55% long-form ad revenue (RPM $2-40 by niche)",
        "changes": "Lower threshold tier added. Shopping features expanded. Shorts ad revenue share improved to 45%.",
        "source_url": "https://support.google.com/youtube/answer/72851",
    },
    {
        "platform": "YouTube",
        "program_name": "YouTube Memberships",
        "status": "active",
        "requirements": "500+ subscribers (lower tier) or 1K+ for full YPP",
        "payout_rate": "70% of membership fees (after Apple/Google cut on mobile)",
        "changes": "Gift memberships available. Lower eligibility threshold added.",
        "source_url": "https://support.google.com/youtube/answer/7636690",
    },
    {
        "platform": "YouTube",
        "program_name": "YouTube Super Chat/Thanks",
        "status": "active",
        "requirements": "YPP membership required",
        "payout_rate": "70% of Super Chat/Thanks revenue",
        "changes": "Super Thanks now available on Shorts.",
        "source_url": "https://support.google.com/youtube/answer/7288782",
    },
    {
        "platform": "Instagram",
        "program_name": "Instagram Subscriptions",
        "status": "active",
        "requirements": "US-based, 10K+ followers, 18+, professional account, compliance with policies",
        "payout_rate": "$0.99-$99.99/month tiers. Instagram takes ~30% on iOS.",
        "changes": "Expanding to more creators. Exclusive content features improved.",
        "source_url": "https://about.instagram.com/blog/announcements/instagram-subscriptions",
    },
    {
        "platform": "Instagram",
        "program_name": "Instagram Reels Bonuses",
        "status": "winding_down",
        "requirements": "Invite-only. Being phased out.",
        "payout_rate": "Previously up to $35K/month based on performance",
        "changes": "Being phased out in 2025-2026. Replaced by Subscriptions and Shopping focus.",
        "source_url": "https://about.instagram.com/blog",
    },
    {
        "platform": "X/Twitter",
        "program_name": "X Creator Revenue Sharing",
        "status": "active",
        "requirements": "X Premium subscriber, 500+ followers, 5M impressions in last 3 months",
        "payout_rate": "Share of ad revenue from ads in replies. ~$2-8 per 1M impressions.",
        "changes": "Payouts via Stripe. Must have Premium subscription ($8-16/month).",
        "source_url": "https://help.twitter.com/en/using-x/creator-ads-revenue-sharing",
    },
    {
        "platform": "X/Twitter",
        "program_name": "X Subscriptions (Super Follows)",
        "status": "active",
        "requirements": "X Premium, 500+ followers, 18+",
        "payout_rate": "Creator sets price $2.99-$9.99/mo. X takes ~3-12% depending on Apple/web.",
        "changes": "Rebranded from Super Follows. Lower X commission on web vs iOS.",
        "source_url": "https://help.twitter.com/en/using-x/subscriptions",
    },
    {
        "platform": "Medium",
        "program_name": "Medium Partner Program",
        "status": "active",
        "requirements": "100+ followers, published 1+ story in last 6 months, Stripe-supported country",
        "payout_rate": "Based on member reading time. ~$50-500 per 1K member reads. Top writers $5K+/mo.",
        "changes": "Boosted distribution for Partner Program members. New referral bonuses.",
        "source_url": "https://help.medium.com/hc/en-us/articles/115011694187",
    },
    {
        "platform": "Substack",
        "program_name": "Substack Pro/Growth Programs",
        "status": "active",
        "requirements": "No minimum. Anyone can start. Paid features at any subscriber count.",
        "payout_rate": "90% of subscription revenue (Substack takes 10%). Avg $5-15/mo per paid sub.",
        "changes": "Substack Notes driving discovery. Recommendation network between newsletters.",
        "source_url": "https://substack.com/going-paid",
    },
    {
        "platform": "Beehiiv",
        "program_name": "Beehiiv Ad Network",
        "status": "active",
        "requirements": "1K+ subscribers for ad network access",
        "payout_rate": "$2-5 CPM for newsletter ads. Higher for premium niches (finance, tech).",
        "changes": "Ad network expanding. Boosts feature for cross-promotion.",
        "source_url": "https://www.beehiiv.com/advertise",
    },
    {
        "platform": "Fanvue",
        "program_name": "Fanvue Creator Program",
        "status": "active",
        "requirements": "No minimum. AI creators explicitly allowed.",
        "payout_rate": "80% revenue share (Fanvue takes 20%). Tips, subscriptions, PPV.",
        "changes": "AI-friendly platform. $100M+ ARR. Growing alternative to OnlyFans for AI creators.",
        "source_url": "https://www.fanvue.com/creators",
    },
    {
        "platform": "Spotify",
        "program_name": "Spotify for Creators (Music)",
        "status": "active",
        "requirements": "Distribute via DistroKid/TuneCore/etc. 1K+ streams for payout.",
        "payout_rate": "$0.003-$0.005 per stream. ~$3-5 per 1000 streams.",
        "changes": "AI-generated music policies tightening. Must disclose AI usage.",
        "source_url": "https://artists.spotify.com",
    },
]

# Search queries for program updates
UPDATE_QUERIES = [
    "TikTok creator program changes 2026",
    "YouTube partner program update 2026",
    "Instagram creator monetization 2026",
    "Twitter X revenue sharing update 2026",
    "Medium partner program changes 2026",
    "Substack creator earnings 2026",
    "creator monetization programs new 2026",
    "TikTok creativity program beta payout 2026",
]

# Reddit subs to monitor


def init_csv():
    """Create CSV with headers if it doesn't exist."""
    if not OUTPUT_CSV.exists():
        OUTPUT_CSV.parent.mkdir(parents=True, exist_ok=True)
        with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(CSV_COLUMNS)
        print(f"[+] Created {OUTPUT_CSV}")


def load_existing():
    """Load existing entries."""
    entries = set()
    if OUTPUT_CSV.exists():
        with open(OUTPUT_CSV, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                key = f"{row.get('date','')}|{row.get('platform','')}|{row.get('program_name','')}"
                entries.add(key)
    return entries


def write_baseline(existing):
    """Write baseline creator program data."""
    today = datetime.now().strftime("%Y-%m-%d")
    results = []
    for prog in CREATOR_PROGRAMS:
        key = f"{today}|{prog['platform']}|{prog['program_name']}"
        if key in existing:
            continue
        results.append({
            "date": today,
            **prog,
        })
    return results


def scrape_reddit_updates(session, existing):
    """Search Reddit for creator program updates."""
    results = []
    today = datetime.now().strftime("%Y-%m-%d")

    for sub in REDDIT_SUBS:
        url = f"https://www.reddit.com/r/{sub}/search.json?q=creator+program+OR+monetization+OR+payout+OR+revenue+share&restrict_sr=1&sort=new&limit=10&t=month"
        try:
            time.sleep(2)
            resp = session.get(url, headers={**HEADERS, "User-Agent": "PRINTMAXX-CreatorPrograms/1.0"}, timeout=15)
            if resp.status_code != 200:
                print(f"  [-] r/{sub}: HTTP {resp.status_code}")
                continue
            data = resp.json()
            posts = data.get("data", {}).get("children", [])

            for post in posts:
                pd = post.get("data", {})
                title = pd.get("title", "")
                selftext = pd.get("selftext", "")[:500]
                permalink = pd.get("permalink", "")
                full_text = f"{title} {selftext}".lower()

                # Must mention monetization/creator program related terms
                if not any(w in full_text for w in ["creator program", "monetiz", "payout", "revenue shar", "partner program", "creator fund", "rpn", "rpm", "earning"]):
                    continue

                # Determine platform
                platform = "Unknown"
                if any(w in full_text for w in ["tiktok", "tt "]):
                    platform = "TikTok"
                elif any(w in full_text for w in ["youtube", "yt ", "ypp"]):
                    platform = "YouTube"
                elif any(w in full_text for w in ["instagram", " ig "]):
                    platform = "Instagram"
                elif any(w in full_text for w in ["twitter", " x "]):
                    platform = "X/Twitter"
                elif "medium" in full_text:
                    platform = "Medium"
                elif "substack" in full_text:
                    platform = "Substack"

                source_url = f"https://www.reddit.com{permalink}"
                program_name = f"{platform} program update (Reddit)"
                key = f"{today}|{platform}|{program_name}"
                if key in existing:
                    continue
                existing.add(key)

                results.append({
                    "date": today,
                    "platform": platform,
                    "program_name": program_name,
                    "status": "update_reported",
                    "requirements": "See source",
                    "payout_rate": "See source",
                    "changes": title[:200],
                    "source_url": source_url,
                })
            print(f"  [+] r/{sub}: checked for program updates")
        except Exception as e:
            print(f"  [-] r/{sub} error: {e}")
    return results


def search_brave_updates(session, existing):
    """Search web for creator program news."""
    results = []
    today = datetime.now().strftime("%Y-%m-%d")

    for query in UPDATE_QUERIES:
        search_url = f"https://search.brave.com/search?q={quote_plus(query)}&source=web"
        try:
            time.sleep(2)
            resp = session.get(search_url, headers=HEADERS, timeout=15)
            if resp.status_code != 200:
                print(f"  [-] Brave '{query}': HTTP {resp.status_code}")
                continue
            soup = BeautifulSoup(resp.text, "html.parser")

            for result in soup.select(".snippet")[:3]:
                title_el = result.select_one(".snippet-title")
                desc_el = result.select_one(".snippet-description")
                link_el = result.select_one("a")
                if not title_el:
                    continue

                title = title_el.get_text(strip=True)
                desc = desc_el.get_text(strip=True) if desc_el else ""
                url = link_el.get("href", "") if link_el else ""
                full_text = f"{title} {desc}".lower()

                # Determine platform
                platform = "Unknown"
                if "tiktok" in full_text:
                    platform = "TikTok"
                elif "youtube" in full_text:
                    platform = "YouTube"
                elif "instagram" in full_text:
                    platform = "Instagram"
                elif "twitter" in full_text or " x " in full_text:
                    platform = "X/Twitter"
                elif "medium" in full_text:
                    platform = "Medium"
                elif "substack" in full_text:
                    platform = "Substack"

                program_name = f"{platform} program news"
                key = f"{today}|{platform}|{program_name}"
                if key in existing:
                    continue
                existing.add(key)

                results.append({
                    "date": today,
                    "platform": platform,
                    "program_name": program_name,
                    "status": "news",
                    "requirements": "See source",
                    "payout_rate": "See source",
                    "changes": title[:200],
                    "source_url": url[:300],
                })
            print(f"  [+] Brave '{query}': checked")
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
    print("CREATOR PROGRAM MONITORING - PRINTMAXX")
    print(f"Run time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

    init_csv()
    existing = load_existing()
    session = requests.Session()
    all_results = []

    # Phase 1: Baseline programs
    print("\n[Phase 1] Writing baseline creator program data...")
    baseline = write_baseline(existing)
    all_results.extend(baseline)
    for r in baseline:
        existing.add(f"{r['date']}|{r['platform']}|{r['program_name']}")
    print(f"  [+] {len(baseline)} baseline programs")

    # Phase 2: Reddit updates
    print("\n[Phase 2] Scanning Reddit for program updates...")
    reddit = scrape_reddit_updates(session, existing)
    all_results.extend(reddit)

    # Phase 3: Web search
    print("\n[Phase 3] Searching web for program news...")
    web = search_brave_updates(session, existing)
    all_results.extend(web)

    # Write
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
        print(f"  {p}: {c} programs tracked")

    print(f"\n  TOTAL: {count} entries written")
    print(f"  Output: {OUTPUT_CSV}")

    # Active programs summary
    print("\n  ACTIVE PROGRAMS:")
    for prog in CREATOR_PROGRAMS:
        if prog["status"] == "active":
            print(f"    {prog['platform']} - {prog['program_name']}: {prog['payout_rate']}")
    print("=" * 60)

    return count


if __name__ == "__main__":
    count = main()
    sys.exit(0)
