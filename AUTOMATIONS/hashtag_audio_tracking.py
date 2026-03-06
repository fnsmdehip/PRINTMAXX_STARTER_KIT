#!/usr/bin/env python3
"""
hashtag_audio_tracking.py - Track trending hashtags and audio across platforms
Scrapes TikTok Creative Center, Reddit, and web search for trending content.
Output: LEDGER/TRENDING_HASHTAGS_AUDIO.csv
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
OUTPUT_CSV = BASE_DIR / "LEDGER" / "TRENDING_HASHTAGS_AUDIO.csv"
CSV_COLUMNS = ["date", "platform", "type", "name", "view_count", "growth_rate", "relevant_niches", "use_recommendation"]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
}

# Our niches for cross-referencing
NICHES = {
    "faith": ["prayer", "faith", "god", "christian", "muslim", "ramadan", "bible", "quran", "worship", "spiritual", "church", "mosque", "blessed", "halal", "hijab", "dua"],
    "fitness": ["fitness", "gym", "workout", "exercise", "gains", "muscle", "bulk", "cut", "protein", "lift", "run", "cardio", "yoga", "health", "weight"],
    "tech": ["tech", "coding", "programming", "ai", "startup", "saas", "developer", "software", "app", "build", "ship", "indie", "hacker", "automation"],
    "sleep": ["sleep", "insomnia", "rest", "melatonin", "dream", "bedtime", "nap", "circadian", "relaxation", "asmr", "calm"],
    "memes": ["meme", "funny", "humor", "viral", "trending", "comedy", "joke", "lol", "brainrot", "sigma", "skibidi", "rizz"],
}

# Reddit subs for trending content
TRENDING_SUBS = ["TikTokTrending", "TikTokCreators", "Instagram", "socialmedia", "youtube"]

# Search queries for trending hashtags and audio
TRENDING_QUERIES = [
    "trending TikTok hashtags february 2026",
    "trending TikTok sounds february 2026",
    "trending Instagram reels hashtags 2026",
    "trending YouTube shorts hashtags 2026",
    "viral TikTok audio this week",
    "trending hashtags social media today",
    "TikTok creative center trending",
    "trending Twitter hashtags today",
]


def init_csv():
    """Create CSV with headers if it doesn't exist."""
    if not OUTPUT_CSV.exists():
        OUTPUT_CSV.parent.mkdir(parents=True, exist_ok=True)
        with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(CSV_COLUMNS)
        print(f"[+] Created {OUTPUT_CSV}")


def load_existing_entries():
    """Load existing entries to avoid duplicates."""
    entries = set()
    if OUTPUT_CSV.exists():
        with open(OUTPUT_CSV, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                key = f"{row.get('platform','')}|{row.get('type','')}|{row.get('name','')}"
                entries.add(key)
    return entries


def match_niches(text):
    """Match text against our niches."""
    text_lower = text.lower()
    matched = []
    for niche, keywords in NICHES.items():
        if any(kw in text_lower for kw in keywords):
            matched.append(niche)
    return matched if matched else ["general"]


def generate_recommendation(name, niche_list, entry_type):
    """Generate a use recommendation based on the trending item."""
    niches_str = "/".join(niche_list)
    if entry_type == "hashtag":
        if "general" in niche_list:
            return f"Use #{name} in next 48h on all niche accounts for reach boost"
        return f"Use #{name} on {niches_str} niche accounts. Post within 24h for peak trend."
    else:  # audio
        if "general" in niche_list:
            return f"Create content with '{name}' audio across all niche accounts"
        return f"Create {niches_str} niche content using '{name}' audio. Early adoption = more reach."


def parse_view_count(text):
    """Extract view count from text like '1.2B views' or '500K'."""
    text = text.strip().upper()
    match = re.search(r'([\d.]+)\s*([BMK])?', text)
    if not match:
        return "unknown"
    num = float(match.group(1))
    suffix = match.group(2) or ""
    multipliers = {"B": 1_000_000_000, "M": 1_000_000, "K": 1_000}
    total = int(num * multipliers.get(suffix, 1))
    if total >= 1_000_000_000:
        return f"{total/1_000_000_000:.1f}B"
    elif total >= 1_000_000:
        return f"{total/1_000_000:.1f}M"
    elif total >= 1_000:
        return f"{total/1_000:.0f}K"
    return str(total)


def scrape_reddit_trending(session, existing):
    """Scrape Reddit for trending hashtag/audio discussions."""
    results = []
    for sub in TRENDING_SUBS:
        url = f"https://www.reddit.com/r/{sub}/search.json?q=trending+hashtag+OR+trending+audio+OR+trending+sound&restrict_sr=1&sort=new&limit=15&t=week"
        try:
            time.sleep(2)
            resp = session.get(url, headers={**HEADERS, "User-Agent": "PRINTMAXX-HashtagTracker/1.0"}, timeout=15)
            if resp.status_code != 200:
                print(f"  [-] r/{sub}: HTTP {resp.status_code}")
                continue
            data = resp.json()
            posts = data.get("data", {}).get("children", [])
            for post in posts:
                pd = post.get("data", {})
                title = pd.get("title", "")
                selftext = pd.get("selftext", "")[:500]
                full_text = f"{title} {selftext}"

                # Extract hashtags from text
                hashtags = re.findall(r'#(\w+)', full_text)
                for tag in hashtags:
                    if len(tag) < 3 or len(tag) > 50:
                        continue
                    key = f"TikTok|hashtag|{tag.lower()}"
                    if key in existing:
                        continue
                    existing.add(key)
                    niches = match_niches(tag)
                    results.append({
                        "date": datetime.now().strftime("%Y-%m-%d"),
                        "platform": "TikTok",
                        "type": "hashtag",
                        "name": tag.lower(),
                        "view_count": "unknown",
                        "growth_rate": "trending",
                        "relevant_niches": "|".join(niches),
                        "use_recommendation": generate_recommendation(tag.lower(), niches, "hashtag"),
                    })

            print(f"  [+] r/{sub}: found {len(results)} hashtags/audio")
        except Exception as e:
            print(f"  [-] r/{sub} error: {e}")
    return results


def search_brave_trending(query, session, existing):
    """Search Brave for trending hashtags and audio."""
    results = []
    search_url = f"https://search.brave.com/search?q={quote_plus(query)}&source=web"
    try:
        time.sleep(2)
        resp = session.get(search_url, headers=HEADERS, timeout=15)
        if resp.status_code != 200:
            print(f"  [-] Brave '{query}': HTTP {resp.status_code}")
            return results
        soup = BeautifulSoup(resp.text, "html.parser")

        for result in soup.select(".snippet")[:8]:
            title_el = result.select_one(".snippet-title")
            desc_el = result.select_one(".snippet-description")
            if not title_el:
                continue
            title = title_el.get_text(strip=True)
            desc = desc_el.get_text(strip=True) if desc_el else ""
            full_text = f"{title} {desc}"

            # Extract hashtags
            hashtags = re.findall(r'#(\w+)', full_text)
            # Also look for patterns like "hashtag: word" or numbered lists of tags
            tag_patterns = re.findall(r'(?:^|\d+[\.\)]\s*)#?(\w{3,30})(?:\s*[-:]\s*[\d.]+[BMK]?\s*(?:views|posts))?', full_text, re.IGNORECASE)

            # Determine platform from query
            platform = "TikTok"
            if "instagram" in query.lower():
                platform = "Instagram"
            elif "youtube" in query.lower():
                platform = "YouTube"
            elif "twitter" in query.lower():
                platform = "X/Twitter"

            # Determine type
            entry_type = "hashtag"
            if any(w in query.lower() for w in ["sound", "audio", "music"]):
                entry_type = "audio"

            for tag in hashtags[:10]:
                if len(tag) < 3:
                    continue
                key = f"{platform}|{entry_type}|{tag.lower()}"
                if key in existing:
                    continue
                existing.add(key)
                niches = match_niches(tag)
                results.append({
                    "date": datetime.now().strftime("%Y-%m-%d"),
                    "platform": platform,
                    "type": entry_type,
                    "name": tag.lower(),
                    "view_count": "unknown",
                    "growth_rate": "trending",
                    "relevant_niches": "|".join(niches),
                    "use_recommendation": generate_recommendation(tag.lower(), niches, entry_type),
                })

            # Extract audio/song names from descriptions
            if entry_type == "audio":
                # Look for quoted song names or "by artist" patterns
                songs = re.findall(r'"([^"]{3,50})"', full_text)
                songs += re.findall(r"'([^']{3,50})'", full_text)
                for song in songs[:5]:
                    key = f"{platform}|audio|{song.lower()}"
                    if key in existing:
                        continue
                    existing.add(key)
                    niches = match_niches(song)
                    results.append({
                        "date": datetime.now().strftime("%Y-%m-%d"),
                        "platform": platform,
                        "type": "audio",
                        "name": song.lower(),
                        "view_count": "unknown",
                        "growth_rate": "trending",
                        "relevant_niches": "|".join(niches),
                        "use_recommendation": generate_recommendation(song, niches, "audio"),
                    })

        print(f"  [+] Brave '{query}': {len(results)} items")
    except Exception as e:
        print(f"  [-] Brave error '{query}': {e}")
    return results


def add_known_trending():
    """Add known evergreen trending hashtags per platform."""
    today = datetime.now().strftime("%Y-%m-%d")
    # These are consistently high-performing hashtags per niche
    known = [
        # Faith niche
        {"platform": "TikTok", "type": "hashtag", "name": "ramadan2026", "niches": "faith", "rec": "Post daily Ramadan content. Peak engagement during iftar time."},
        {"platform": "TikTok", "type": "hashtag", "name": "faithtok", "niches": "faith", "rec": "Use on all faith content. Consistent performer."},
        {"platform": "Instagram", "type": "hashtag", "name": "muslimtiktok", "niches": "faith", "rec": "Cross-post TikTok Reels with this tag on Instagram."},
        # Fitness niche
        {"platform": "TikTok", "type": "hashtag", "name": "gymbro", "niches": "fitness", "rec": "Pair with workout clips. High engagement for gym content."},
        {"platform": "TikTok", "type": "hashtag", "name": "fittok", "niches": "fitness", "rec": "Must-use for all fitness TikTok content."},
        {"platform": "Instagram", "type": "hashtag", "name": "fitnessmotivation", "niches": "fitness", "rec": "Evergreen. Use on all Instagram fitness posts."},
        # Tech niche
        {"platform": "TikTok", "type": "hashtag", "name": "techtok", "niches": "tech", "rec": "Growing category. Post dev/build content."},
        {"platform": "X/Twitter", "type": "hashtag", "name": "buildinpublic", "niches": "tech", "rec": "Core hashtag for @PRINTMAXXER. Use on every build thread."},
        {"platform": "X/Twitter", "type": "hashtag", "name": "indiehacker", "niches": "tech", "rec": "Pair with #buildinpublic for tech audience."},
        # Sleep niche
        {"platform": "TikTok", "type": "hashtag", "name": "sleeptok", "niches": "sleep", "rec": "Use for SleepMaxx content. Growing niche."},
        {"platform": "YouTube", "type": "hashtag", "name": "sleepsounds", "niches": "sleep", "rec": "Essential for YouTube sleep channel content."},
        # General viral
        {"platform": "TikTok", "type": "hashtag", "name": "viral", "niches": "general", "rec": "Broad reach tag. Use sparingly, pair with niche tags."},
        {"platform": "TikTok", "type": "hashtag", "name": "fyp", "niches": "general", "rec": "Decreasing effectiveness but still standard."},
    ]
    results = []
    for item in known:
        results.append({
            "date": today,
            "platform": item["platform"],
            "type": item["type"],
            "name": item["name"],
            "view_count": "evergreen",
            "growth_rate": "stable",
            "relevant_niches": item["niches"],
            "use_recommendation": item["rec"],
        })
    return results


def write_results(results):
    """Append unique results to CSV."""
    if not results:
        print("[!] No new results to write.")
        return 0

    # Deduplicate
    seen = set()
    unique = []
    for r in results:
        key = f"{r['platform']}|{r['type']}|{r['name']}"
        if key not in seen:
            seen.add(key)
            unique.append(r)

    with open(OUTPUT_CSV, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_COLUMNS)
        for row in unique:
            writer.writerow(row)

    print(f"[+] Wrote {len(unique)} entries to {OUTPUT_CSV}")
    return len(unique)


def main():
    print("=" * 60)
    print("HASHTAG & AUDIO TRACKING - PRINTMAXX")
    print(f"Run time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

    init_csv()
    existing = load_existing_entries()
    session = requests.Session()
    all_results = []

    # Phase 1: Known trending hashtags
    print("\n[Phase 1] Adding known trending hashtags per niche...")
    known = add_known_trending()
    # Filter out already existing
    for item in known:
        key = f"{item['platform']}|{item['type']}|{item['name']}"
        if key not in existing:
            all_results.append(item)
            existing.add(key)
    print(f"  [+] {len(all_results)} new known hashtags added")

    # Phase 2: Reddit trending
    print("\n[Phase 2] Scanning Reddit for trending hashtags/audio...")
    reddit_results = scrape_reddit_trending(session, existing)
    all_results.extend(reddit_results)

    # Phase 3: Web search
    print("\n[Phase 3] Searching web for trending content...")
    for query in TRENDING_QUERIES:
        results = search_brave_trending(query, session, existing)
        all_results.extend(results)

    # Write results
    print("\n[Phase 4] Writing results...")
    count = write_results(all_results)

    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    by_platform = {}
    by_type = {}
    by_niche = {}
    for r in all_results:
        p = r["platform"]
        t = r["type"]
        by_platform[p] = by_platform.get(p, 0) + 1
        by_type[t] = by_type.get(t, 0) + 1
        for n in r["relevant_niches"].split("|"):
            by_niche[n] = by_niche.get(n, 0) + 1

    print("  By Platform:")
    for p, c in sorted(by_platform.items()):
        print(f"    {p}: {c}")
    print("  By Type:")
    for t, c in sorted(by_type.items()):
        print(f"    {t}: {c}")
    print("  By Niche:")
    for n, c in sorted(by_niche.items()):
        print(f"    {n}: {c}")
    print(f"\n  TOTAL: {count} new entries written")
    print(f"  Output: {OUTPUT_CSV}")
    print("=" * 60)

    return count


if __name__ == "__main__":
    count = main()
    sys.exit(0)
