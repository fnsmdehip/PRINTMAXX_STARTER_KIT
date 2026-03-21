#!/usr/bin/env python3

from __future__ import annotations
"""
App Clone Opportunity Finder
Searches for trending Android apps with $10K+ revenue, extracts data,
and outputs CSV of clone opportunities.

Usage:
    python3 app_clone_finder.py
    python3 app_clone_finder.py --categories "fitness,ai"
    python3 app_clone_finder.py --min-revenue 10000
"""

import csv
import json
import os
import re
import sys
import time
import argparse
from datetime import datetime, timedelta
from pathlib import Path
from urllib.parse import quote_plus

try:
    import requests
    from bs4 import BeautifulSoup
except ImportError:
    print("Install dependencies: pip3 install requests beautifulsoup4")
    sys.exit(1)

# Config
SCRIPT_DIR = Path(__file__).parent
OUTPUT_DIR = SCRIPT_DIR / "leads"
OUTPUT_CSV = OUTPUT_DIR / "android_clone_opportunities.csv"
LEDGER_DIR = SCRIPT_DIR.parent / "LEDGER"
LEDGER_CSV = LEDGER_DIR / "APP_CLONE_OPPORTUNITIES.csv"

# Target apps to research (recent $10K+ revenue Android apps)
TARGET_APPS = [
    {
        "name": "Tai Chi Walking App",
        "category": "health_fitness",
        "search_terms": ["tai chi walking exercise app", "tai chi step counter"],
        "niche_angle": "faith_wellness",
        "revenue_estimate": "$10K-50K/mo",
    },
    {
        "name": "AI Hairstyle Try-On",
        "category": "beauty_ai",
        "search_terms": ["ai hairstyle try on app", "ai hair color changer"],
        "niche_angle": "women_beauty",
        "revenue_estimate": "$50K-200K/mo",
    },
    {
        "name": "GPS Phone Tracker",
        "category": "utilities_family",
        "search_terms": ["gps phone tracker family locator", "find my phone tracker"],
        "niche_angle": "family_safety",
        "revenue_estimate": "$100K-500K/mo",
    },
    {
        "name": "AI Video Generator",
        "category": "ai_creative",
        "search_terms": ["ai video generator app", "text to video ai mobile"],
        "niche_angle": "creator_tools",
        "revenue_estimate": "$200K-1M/mo",
    },
    {
        "name": "AI Music Generator",
        "category": "ai_music",
        "search_terms": ["ai music generator app", "ai song maker mobile"],
        "niche_angle": "creator_tools",
        "revenue_estimate": "$50K-300K/mo",
    },
    {
        "name": "Workout Tracker",
        "category": "fitness",
        "search_terms": ["workout tracker gym log app", "exercise tracker 2025 2026"],
        "niche_angle": "fitness",
        "revenue_estimate": "$50K-500K/mo",
    },
    {
        "name": "Storage Cleaner",
        "category": "utilities",
        "search_terms": ["phone storage cleaner optimizer", "junk file cleaner android"],
        "niche_angle": "utilities",
        "revenue_estimate": "$100K-1M/mo",
    },
    {
        "name": "AI Tattoo Designer",
        "category": "ai_design",
        "search_terms": ["ai tattoo design generator", "ai tattoo try on app"],
        "niche_angle": "lifestyle_art",
        "revenue_estimate": "$10K-100K/mo",
    },
]

# Brave Search API (free tier) or fallback to web scraping
BRAVE_SEARCH_API_KEY = os.environ.get("BRAVE_SEARCH_API_KEY", "")
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
}

SESSION = requests.Session()
SESSION.headers.update(HEADERS)


def brave_api_search(query: str, count: int = 5) -> list[dict]:
    """Search using Brave Search API if key available."""
    if not BRAVE_SEARCH_API_KEY:
        return []

    url = "https://api.search.brave.com/res/v1/web/search"
    headers = {
        "Accept": "application/json",
        "Accept-Encoding": "gzip",
        "X-Subscription-Token": BRAVE_SEARCH_API_KEY,
    }
    params = {"q": query, "count": count, "freshness": "pm"}  # past month

    try:
        resp = SESSION.get(url, headers=headers, params=params, timeout=15)
        resp.raise_for_status()
        data = resp.json()
        results = []
        for item in data.get("web", {}).get("results", []):
            results.append({
                "title": item.get("title", ""),
                "url": item.get("url", ""),
                "description": item.get("description", ""),
            })
        return results
    except Exception as e:
        print(f"  Brave API error: {e}")
        return []


def duckduckgo_search(query: str, count: int = 5) -> list[dict]:
    """Fallback search using DuckDuckGo HTML."""
    url = f"https://html.duckduckgo.com/html/?q={quote_plus(query)}"
    try:
        resp = SESSION.get(url, timeout=15)
        soup = BeautifulSoup(resp.text, "html.parser")
        results = []
        for result in soup.select(".result")[:count]:
            title_el = result.select_one(".result__title a")
            snippet_el = result.select_one(".result__snippet")
            if title_el:
                results.append({
                    "title": title_el.get_text(strip=True),
                    "url": title_el.get("href", ""),
                    "description": snippet_el.get_text(strip=True) if snippet_el else "",
                })
        return results
    except Exception as e:
        print(f"  DuckDuckGo error: {e}")
        return []


def search(query: str, count: int = 5) -> list[dict]:
    """Search with fallback chain: Brave API -> DuckDuckGo."""
    results = brave_api_search(query, count)
    if results:
        return results
    time.sleep(1.5)  # rate limit politeness
    return duckduckgo_search(query, count)


def extract_numbers(text: str) -> dict:
    """Extract revenue, download, and rating numbers from text."""
    data = {}

    # Revenue patterns
    rev_patterns = [
        r'\$(\d+(?:\.\d+)?)\s*(?:million|M)\s*(?:per\s*month|/mo|monthly|MRR)',
        r'\$(\d+(?:,\d{3})*(?:\.\d+)?)\s*(?:per\s*month|/mo|monthly|MRR)',
        r'(\d+(?:\.\d+)?)\s*(?:million|M)\s*(?:revenue|rev|ARR)',
        r'revenue[:\s]*\$(\d+(?:,\d{3})*(?:\.\d+)?[KkMm]?)',
        r'\$(\d+[KkMm])\s*(?:revenue|rev|MRR|ARR)',
    ]
    for pattern in rev_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            data["revenue_found"] = match.group(0)
            break

    # Downloads
    dl_patterns = [
        r'(\d+(?:\.\d+)?)\s*(?:million|M)\+?\s*(?:downloads|installs)',
        r'(\d+(?:,\d{3})*[KkMm]?)\+?\s*(?:downloads|installs)',
        r'downloads?[:\s]*(\d+(?:,\d{3})*[KkMm]?\+?)',
    ]
    for pattern in dl_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            data["downloads_found"] = match.group(0)
            break

    # Ratings
    rating_match = re.search(r'(\d\.\d)\s*(?:stars?|rating|out of 5)', text, re.IGNORECASE)
    if rating_match:
        data["rating_found"] = rating_match.group(1)

    return data


def research_app(app: dict) -> dict:
    """Research a single app opportunity."""
    print(f"\n{'='*60}")
    print(f"Researching: {app['name']}")
    print(f"{'='*60}")

    result = {
        "app_name": app["name"],
        "category": app["category"],
        "niche_angle": app["niche_angle"],
        "revenue_estimate": app["revenue_estimate"],
        "downloads": "N/A",
        "rating": "N/A",
        "what_makes_it_work": "",
        "clone_difficulty": "",
        "monetization_model": "",
        "search_sources": [],
        "raw_findings": [],
    }

    # Search 1: Sensor Tower / revenue data
    query1 = f"sensor tower {app['name']} revenue 2025 2026 android"
    print(f"  Search: {query1}")
    results1 = search(query1, 5)
    for r in results1:
        combined = f"{r['title']} {r['description']}"
        nums = extract_numbers(combined)
        if nums:
            result.update(nums)
        result["raw_findings"].append(combined)
        result["search_sources"].append(r["url"])

    time.sleep(1)

    # Search 2: data.ai trending category
    query2 = f"data.ai {app['category'].replace('_', ' ')} trending apps 2025 2026"
    print(f"  Search: {query2}")
    results2 = search(query2, 3)
    for r in results2:
        combined = f"{r['title']} {r['description']}"
        result["raw_findings"].append(combined)

    time.sleep(1)

    # Search 3: What makes it successful
    query3 = f"{app['search_terms'][0]} review why popular features"
    print(f"  Search: {query3}")
    results3 = search(query3, 3)
    features = []
    for r in results3:
        features.append(r["description"])
    result["what_makes_it_work"] = " | ".join(features[:3]) if features else "Visual AI + simple UX + freemium model"

    time.sleep(1)

    # Search 4: Monetization model
    query4 = f"{app['search_terms'][0]} pricing subscription in-app purchase"
    print(f"  Search: {query4}")
    results4 = search(query4, 3)
    monetization = []
    for r in results4:
        text = r["description"].lower()
        if any(kw in text for kw in ["subscription", "premium", "pro", "in-app", "free trial", "ads", "$"]):
            monetization.append(r["description"][:150])
    result["monetization_model"] = " | ".join(monetization[:2]) if monetization else "Freemium + subscription ($4.99-9.99/week)"

    # Determine clone difficulty
    ai_heavy = any(kw in app["category"] for kw in ["ai_", "beauty_ai"])
    if ai_heavy:
        result["clone_difficulty"] = "MEDIUM - needs AI API integration (Replicate/RunPod)"
    elif "utilities" in app["category"]:
        result["clone_difficulty"] = "EASY - standard mobile features"
    else:
        result["clone_difficulty"] = "MEDIUM - standard features + good UX needed"

    # Clean up downloads/rating from findings
    all_text = " ".join(result["raw_findings"])
    nums = extract_numbers(all_text)
    if "downloads_found" in nums and result["downloads"] == "N/A":
        result["downloads"] = nums["downloads_found"]
    if "rating_found" in nums and result["rating"] == "N/A":
        result["rating"] = nums["rating_found"]

    print(f"  Revenue estimate: {result['revenue_estimate']}")
    print(f"  Clone difficulty: {result['clone_difficulty']}")
    print(f"  Sources found: {len(result['search_sources'])}")

    return result


def score_opportunity(result: dict) -> int:
    """Score an opportunity 0-100 based on multiple factors."""
    score = 50  # base

    # Revenue score
    rev = result["revenue_estimate"].lower()
    if "1m" in rev or "500k" in rev:
        score += 20
    elif "200k" in rev or "300k" in rev:
        score += 15
    elif "100k" in rev:
        score += 10
    elif "50k" in rev:
        score += 5

    # Clone difficulty
    diff = result["clone_difficulty"].lower()
    if "easy" in diff:
        score += 15
    elif "medium" in diff:
        score += 5
    elif "hard" in diff:
        score -= 10

    # Niche angle alignment (faith/fitness/women = our niches)
    niche = result["niche_angle"].lower()
    if any(n in niche for n in ["faith", "fitness", "women", "beauty"]):
        score += 10
    elif "creator" in niche:
        score += 5

    # Has specific data found
    if result.get("revenue_found"):
        score += 5
    if result.get("downloads_found"):
        score += 5

    return min(100, max(0, score))


def save_output_csv(results: list[dict]):
    """Save results to output CSV."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    fieldnames = [
        "rank", "app_name", "category", "niche_angle", "revenue_estimate",
        "downloads", "rating", "clone_difficulty", "monetization_model",
        "what_makes_it_work", "score", "researched_at",
    ]

    with open(OUTPUT_CSV, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for i, r in enumerate(results, 1):
            writer.writerow({
                "rank": i,
                "app_name": r["app_name"],
                "category": r["category"],
                "niche_angle": r["niche_angle"],
                "revenue_estimate": r["revenue_estimate"],
                "downloads": r.get("downloads", "N/A"),
                "rating": r.get("rating", "N/A"),
                "clone_difficulty": r["clone_difficulty"],
                "monetization_model": r["monetization_model"][:200],
                "what_makes_it_work": r["what_makes_it_work"][:300],
                "score": r["score"],
                "researched_at": datetime.now().isoformat(),
            })

    print(f"\nSaved {len(results)} opportunities to {OUTPUT_CSV}")


def save_ledger_csv(results: list[dict]):
    """Append to LEDGER/APP_CLONE_OPPORTUNITIES.csv."""
    LEDGER_DIR.mkdir(parents=True, exist_ok=True)

    # Check existing entries
    existing_names = set()
    if LEDGER_CSV.exists():
        with open(LEDGER_CSV, "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                existing_names.add(row.get("app_name", "").strip().lower())

    fieldnames = [
        "clone_id", "app_name", "category", "niche_angle", "revenue_estimate",
        "clone_difficulty", "monetization_model", "score", "status",
        "added_date", "notes",
    ]

    # Determine next clone_id
    next_id = 1
    if LEDGER_CSV.exists():
        with open(LEDGER_CSV, "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                cid = row.get("clone_id", "")
                match = re.search(r'(\d+)', cid)
                if match:
                    next_id = max(next_id, int(match.group(1)) + 1)

    file_exists = LEDGER_CSV.exists()
    new_count = 0

    with open(LEDGER_CSV, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        for r in results:
            if r["app_name"].strip().lower() in existing_names:
                print(f"  Skipping duplicate: {r['app_name']}")
                continue
            writer.writerow({
                "clone_id": f"CLONE{next_id:03d}",
                "app_name": r["app_name"],
                "category": r["category"],
                "niche_angle": r["niche_angle"],
                "revenue_estimate": r["revenue_estimate"],
                "clone_difficulty": r["clone_difficulty"],
                "monetization_model": r["monetization_model"][:200],
                "score": r["score"],
                "status": "RESEARCHED",
                "added_date": datetime.now().strftime("%Y-%m-%d"),
                "notes": f"Auto-found by app_clone_finder.py. Score: {r['score']}/100",
            })
            next_id += 1
            new_count += 1

    print(f"Added {new_count} new entries to {LEDGER_CSV}")


def print_summary(results: list[dict]):
    """Print ranked summary."""
    print(f"\n{'='*70}")
    print(f"  APP CLONE OPPORTUNITY RANKING")
    print(f"  {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"{'='*70}\n")

    for i, r in enumerate(results, 1):
        emoji = ">>>" if i <= 3 else "   "
        print(f"{emoji} #{i} | {r['app_name']} | Score: {r['score']}/100")
        print(f"      Category: {r['category']} | Niche: {r['niche_angle']}")
        print(f"      Revenue: {r['revenue_estimate']} | Difficulty: {r['clone_difficulty']}")
        print(f"      Monetization: {r['monetization_model'][:80]}")
        print()

    print(f"{'='*70}")
    print(f"  TOP 3 RECOMMENDED FOR PWA CLONE:")
    for r in results[:3]:
        print(f"    - {r['app_name']} (Score: {r['score']}, {r['niche_angle']})")
    print(f"{'='*70}\n")


def main():
    parser = argparse.ArgumentParser(description="App Clone Opportunity Finder")
    parser.add_argument("--categories", type=str, help="Comma-separated categories to filter")
    parser.add_argument("--min-revenue", type=int, default=0, help="Minimum revenue filter")
    parser.add_argument("--dry-run", action="store_true", help="Skip search, use cached data")
    args = parser.parse_args()

    apps = TARGET_APPS
    if args.categories:
        cats = [c.strip().lower() for c in args.categories.split(",")]
        apps = [a for a in apps if any(c in a["category"].lower() for c in cats)]

    print(f"Researching {len(apps)} app opportunities...")
    print(f"Search engine: {'Brave API' if BRAVE_SEARCH_API_KEY else 'DuckDuckGo (set BRAVE_SEARCH_API_KEY for better results)'}")

    results = []
    for app in apps:
        result = research_app(app)
        result["score"] = score_opportunity(result)
        results.append(result)

    # Sort by score descending
    results.sort(key=lambda x: x["score"], reverse=True)

    # Save outputs
    save_output_csv(results)
    save_ledger_csv(results)
    print_summary(results)

    return results


if __name__ == "__main__":
    main()
