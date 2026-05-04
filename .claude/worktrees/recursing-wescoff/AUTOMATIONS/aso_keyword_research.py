#!/usr/bin/env python3

from __future__ import annotations
"""
aso_keyword_research.py - App Store Optimization keyword research
Searches for trending app keywords, tracks keyword positions for our apps.
Output: LEDGER/ASO_KEYWORDS.csv
Schedule: WEEKLY
"""

import csv
import json
import os
import re
import sys
import time
from datetime import datetime
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
OUTPUT_CSV = BASE_DIR / "LEDGER" / "ASO_KEYWORDS.csv"
CSV_COLUMNS = ["date", "app_name", "keyword", "search_volume", "difficulty", "current_rank", "competitor_apps", "opportunity_score"]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
}

# Our apps and their target keywords
OUR_APPS = {
    "PrayerLock": {
        "category": "faith",
        "description": "Lock phone during prayer times. Islamic prayer tracker.",
        "primary_keywords": [
            "prayer times", "muslim prayer", "islamic prayer", "salah tracker",
            "prayer reminder", "ramadan tracker", "adhan app", "quran app",
            "prayer lock", "phone lock prayer", "digital detox prayer",
            "islamic app", "dua app", "dhikr counter", "tasbih counter",
        ],
        "competitor_keywords": [
            "muslim pro", "athan", "prayer now", "salaat first",
            "my prayer", "qibla finder", "islamic calendar",
        ],
    },
    "WalkToUnlock": {
        "category": "fitness",
        "description": "Walk a set number of steps to unlock phone. Fitness motivation.",
        "primary_keywords": [
            "walk to unlock", "step counter lock", "fitness phone lock",
            "walking motivation", "step tracker", "pedometer lock",
            "phone addiction", "screen time lock", "walk app",
            "exercise motivation", "healthy habits", "step challenge",
        ],
        "competitor_keywords": [
            "stepbet", "sweatcoin", "charity miles", "walkfit",
            "step counter", "pedometer", "walk tracker",
        ],
    },
    "FocusLock": {
        "category": "productivity",
        "description": "Lock distracting apps during focus sessions. Pomodoro + app blocker.",
        "primary_keywords": [
            "focus lock", "app blocker", "focus timer", "pomodoro timer",
            "study timer", "screen time limit", "distraction blocker",
            "phone addiction", "focus mode", "do not disturb",
            "productivity app", "study app", "concentration app",
        ],
        "competitor_keywords": [
            "forest app", "flora", "offtime", "appblock",
            "freedom app", "cold turkey", "opal app",
        ],
    },
    "HabitForge": {
        "category": "productivity",
        "description": "Habit tracker with streaks, accountability, and social features.",
        "primary_keywords": [
            "habit tracker", "habit builder", "daily habits",
            "streak tracker", "routine tracker", "habit app",
            "goal tracker", "accountability app", "21 day challenge",
            "morning routine", "self improvement", "discipline app",
        ],
        "competitor_keywords": [
            "habitica", "streaks app", "habit bear", "done app",
            "strides", "loop habit", "productive app",
        ],
    },
    "SleepMaxx": {
        "category": "health",
        "description": "Sleep optimization app with sounds, tracking, and smart alarm.",
        "primary_keywords": [
            "sleep tracker", "sleep sounds", "white noise",
            "sleep app", "smart alarm", "sleep quality",
            "insomnia help", "sleep meditation", "rain sounds",
            "bedtime routine", "sleep hygiene", "sleep optimizer",
        ],
        "competitor_keywords": [
            "sleep cycle", "pillow", "calm app", "headspace sleep",
            "rain rain", "white noise app", "slumber",
        ],
    },
    "MealMaxx": {
        "category": "health",
        "description": "Meal tracking and nutrition app optimized for muscle building.",
        "primary_keywords": [
            "meal tracker", "calorie counter", "macro tracker",
            "nutrition app", "meal planner", "food diary",
            "protein tracker", "muscle building diet", "bulk diet",
            "meal prep", "fitness nutrition", "bodybuilding diet",
        ],
        "competitor_keywords": [
            "myfitnesspal", "cronometer", "lose it", "noom",
            "macros app", "yazio", "lifesum",
        ],
    },
    "RamadanTracker": {
        "category": "faith",
        "description": "Ramadan-specific prayer, fasting, and Quran tracking app.",
        "primary_keywords": [
            "ramadan tracker", "ramadan app", "fasting tracker",
            "iftar time", "suhoor time", "ramadan calendar",
            "quran tracker", "ramadan goals", "ramadan planner",
            "islamic fasting", "ramadan countdown", "ramadan 2026",
        ],
        "competitor_keywords": [
            "muslim pro ramadan", "ramadan times", "iftar tracker",
            "ramadan kareem app", "quran majeed",
        ],
    },
}

# Generic ASO search queries
ASO_SEARCH_QUERIES = [
    "trending app store keywords 2026",
    "most searched app store keywords health fitness",
    "app store optimization keywords productivity",
    "ASO keyword difficulty scores",
    "top app store search terms february 2026",
    "prayer app keywords ASO",
    "fitness app keywords ASO",
    "habit tracker app keywords app store",
    "sleep app keywords trending",
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
    """Load existing entries to avoid duplicates."""
    entries = set()
    if OUTPUT_CSV.exists():
        with open(OUTPUT_CSV, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                key = f"{row.get('date','')}|{row.get('app_name','')}|{row.get('keyword','')}"
                entries.add(key)
    return entries


def estimate_search_volume(keyword):
    """Estimate search volume tier based on keyword characteristics."""
    # Longer, more specific keywords = lower volume but easier to rank
    word_count = len(keyword.split())
    if word_count <= 1:
        return "high"
    elif word_count == 2:
        return "medium-high"
    elif word_count == 3:
        return "medium"
    else:
        return "low-medium"


def estimate_difficulty(keyword, is_competitor_keyword=False):
    """Estimate keyword difficulty."""
    word_count = len(keyword.split())
    if is_competitor_keyword:
        return "very_high"  # Branded keywords are hardest
    if word_count >= 4:
        return "low"
    elif word_count == 3:
        return "medium"
    elif word_count == 2:
        return "medium-high"
    else:
        return "high"


def calculate_opportunity_score(volume, difficulty, has_competitor):
    """Calculate opportunity score 0-100."""
    volume_scores = {"high": 80, "medium-high": 65, "medium": 50, "low-medium": 35, "low": 20}
    diff_scores = {"low": 90, "medium": 65, "medium-high": 40, "high": 25, "very_high": 10}

    v_score = volume_scores.get(volume, 50)
    d_score = diff_scores.get(difficulty, 50)

    # Weighted: 40% volume, 40% difficulty (inverted), 20% competitor presence
    score = (v_score * 0.4) + (d_score * 0.4) + (20 if not has_competitor else 5)
    return min(100, max(0, int(score)))


def generate_keyword_data(existing):
    """Generate keyword research data for all our apps."""
    today = datetime.now().strftime("%Y-%m-%d")
    results = []

    for app_name, app_info in OUR_APPS.items():
        print(f"\n  Analyzing keywords for {app_name}...")

        # Primary keywords
        for kw in app_info["primary_keywords"]:
            key = f"{today}|{app_name}|{kw}"
            if key in existing:
                continue

            volume = estimate_search_volume(kw)
            difficulty = estimate_difficulty(kw)
            competitors = ", ".join(app_info["competitor_keywords"][:3])
            opp_score = calculate_opportunity_score(volume, difficulty, False)

            results.append({
                "date": today,
                "app_name": app_name,
                "keyword": kw,
                "search_volume": volume,
                "difficulty": difficulty,
                "current_rank": "unranked",
                "competitor_apps": competitors,
                "opportunity_score": opp_score,
            })

        # Competitor keywords (harder to rank but high value)
        for kw in app_info["competitor_keywords"]:
            key = f"{today}|{app_name}|{kw}"
            if key in existing:
                continue

            volume = estimate_search_volume(kw)
            difficulty = estimate_difficulty(kw, is_competitor_keyword=True)
            opp_score = calculate_opportunity_score(volume, difficulty, True)

            results.append({
                "date": today,
                "app_name": app_name,
                "keyword": kw,
                "search_volume": volume,
                "difficulty": difficulty,
                "current_rank": "unranked",
                "competitor_apps": f"BRANDED: {kw}",
                "opportunity_score": opp_score,
            })

        print(f"    -> {len(app_info['primary_keywords'])} primary + {len(app_info['competitor_keywords'])} competitor keywords")

    return results


def search_brave_aso(session, existing):
    """Search web for additional ASO keyword insights."""
    results = []
    today = datetime.now().strftime("%Y-%m-%d")

    for query in ASO_SEARCH_QUERIES:
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
                if not title_el:
                    continue

                title = title_el.get_text(strip=True)
                desc = desc_el.get_text(strip=True) if desc_el else ""
                full_text = f"{title} {desc}"

                # Extract potential keywords from the results
                # Look for quoted terms or terms in lists
                potential_kws = re.findall(r'"([^"]{3,30})"', full_text)
                potential_kws += re.findall(r"'([^']{3,30})'", full_text)

                for kw in potential_kws[:3]:
                    kw_lower = kw.lower().strip()
                    if len(kw_lower) < 3 or len(kw_lower) > 40:
                        continue

                    # Match to our apps
                    for app_name, app_info in OUR_APPS.items():
                        category = app_info["category"]
                        if category in kw_lower or any(pk_word in kw_lower for pk in app_info["primary_keywords"][:3] for pk_word in pk.split()):
                            key = f"{today}|{app_name}|{kw_lower}"
                            if key in existing:
                                continue
                            existing.add(key)

                            volume = estimate_search_volume(kw_lower)
                            difficulty = estimate_difficulty(kw_lower)
                            opp_score = calculate_opportunity_score(volume, difficulty, False)

                            results.append({
                                "date": today,
                                "app_name": app_name,
                                "keyword": kw_lower,
                                "search_volume": volume,
                                "difficulty": difficulty,
                                "current_rank": "unranked",
                                "competitor_apps": "discovered_via_search",
                                "opportunity_score": opp_score,
                            })
                            break

            print(f"  [+] Brave '{query}': checked")
        except Exception as e:
            print(f"  [-] Brave error '{query}': {e}")
    return results


def search_reddit_aso(session, existing):
    """Search Reddit for ASO keyword insights."""
    results = []
    today = datetime.now().strftime("%Y-%m-%d")

    subs = ["iOSProgramming", "androiddev", "AppBusiness", "startups"]
    for sub in subs:
        url = f"https://www.reddit.com/r/{sub}/search.json?q=ASO+OR+app+store+optimization+OR+keywords+app+store&restrict_sr=1&sort=new&limit=10&t=month"
        try:
            time.sleep(2)
            resp = session.get(url, headers={**HEADERS, "User-Agent": "PRINTMAXX-ASOResearch/1.0"}, timeout=15)
            if resp.status_code != 200:
                print(f"  [-] r/{sub}: HTTP {resp.status_code}")
                continue
            data = resp.json()
            posts = data.get("data", {}).get("children", [])
            print(f"  [+] r/{sub}: {len(posts)} ASO-related posts found")

            for post in posts:
                pd = post.get("data", {})
                title = pd.get("title", "")
                selftext = pd.get("selftext", "")[:1000]
                full_text = f"{title} {selftext}"

                # Extract keywords mentioned in ASO discussions
                quoted = re.findall(r'"([^"]{3,30})"', full_text)
                for kw in quoted[:5]:
                    kw_lower = kw.lower().strip()
                    for app_name, app_info in OUR_APPS.items():
                        if app_info["category"] in kw_lower:
                            key = f"{today}|{app_name}|{kw_lower}"
                            if key not in existing:
                                existing.add(key)
                                volume = estimate_search_volume(kw_lower)
                                difficulty = estimate_difficulty(kw_lower)
                                opp_score = calculate_opportunity_score(volume, difficulty, False)
                                results.append({
                                    "date": today,
                                    "app_name": app_name,
                                    "keyword": kw_lower,
                                    "search_volume": volume,
                                    "difficulty": difficulty,
                                    "current_rank": "unranked",
                                    "competitor_apps": f"reddit_r/{sub}",
                                    "opportunity_score": opp_score,
                                })
                                break
        except Exception as e:
            print(f"  [-] r/{sub} error: {e}")
    return results


def write_results(results):
    """Append results to CSV."""
    if not results:
        print("[!] No new results to write.")
        return 0

    # Sort by opportunity score (highest first)
    results.sort(key=lambda x: int(x.get("opportunity_score", 0)), reverse=True)

    with open(OUTPUT_CSV, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_COLUMNS)
        for row in results:
            writer.writerow(row)

    print(f"[+] Wrote {len(results)} entries to {OUTPUT_CSV}")
    return len(results)


def main():
    print("=" * 60)
    print("ASO KEYWORD RESEARCH - PRINTMAXX")
    print(f"Run time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

    init_csv()
    existing = load_existing()
    session = requests.Session()
    all_results = []

    # Phase 1: Generate keyword data for our apps
    print("\n[Phase 1] Generating keyword research for our apps...")
    keyword_data = generate_keyword_data(existing)
    all_results.extend(keyword_data)
    for r in keyword_data:
        existing.add(f"{r['date']}|{r['app_name']}|{r['keyword']}")
    print(f"  [+] {len(keyword_data)} keyword entries generated")

    # Phase 2: Web search for additional keywords
    print("\n[Phase 2] Searching web for ASO insights...")
    web_results = search_brave_aso(session, existing)
    all_results.extend(web_results)

    # Phase 3: Reddit ASO discussions
    print("\n[Phase 3] Scanning Reddit for ASO discussions...")
    reddit_results = search_reddit_aso(session, existing)
    all_results.extend(reddit_results)

    # Write results
    print("\n[Phase 4] Writing results...")
    count = write_results(all_results)

    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    by_app = {}
    for r in all_results:
        a = r["app_name"]
        by_app[a] = by_app.get(a, 0) + 1
    for a, c in sorted(by_app.items()):
        print(f"  {a}: {c} keywords tracked")

    print(f"\n  TOTAL: {count} entries written")
    print(f"  Output: {OUTPUT_CSV}")

    # Top opportunities
    print("\n  TOP 10 KEYWORD OPPORTUNITIES (by score):")
    sorted_results = sorted(all_results, key=lambda x: int(x.get("opportunity_score", 0)), reverse=True)
    for r in sorted_results[:10]:
        print(f"    [{r['opportunity_score']}] {r['app_name']}: \"{r['keyword']}\" (vol: {r['search_volume']}, diff: {r['difficulty']})")
    print("=" * 60)

    return count


if __name__ == "__main__":
    count = main()
    sys.exit(0)
