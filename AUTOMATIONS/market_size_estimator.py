#!/usr/bin/env python3

from __future__ import annotations
"""
PRINTMAXX Market Size Estimator
================================
Estimates TAM/SAM/SOM for each PrintMaxx venture using free public data:
  - Google Trends (via public widget endpoint, no API key)
  - iTunes App Store category size estimation
  - Gumroad category sales volume estimation
  - Reddit community sizes as market proxies

Outputs:
  LEDGER/MARKET_SIZE_ESTIMATES.csv

Usage:
    python3 market_size_estimator.py --all
    python3 market_size_estimator.py --estimate faith
    python3 market_size_estimator.py --estimate screen_time
    python3 market_size_estimator.py --trends
    python3 market_size_estimator.py --compare

Cron (monthly, 1st at 5AM):
  0 5 1 * * cd /Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt && python3 AUTOMATIONS/market_size_estimator.py --all >> AUTOMATIONS/logs/market_size.log 2>&1
"""

import argparse
import csv
import json
import os
import re
import ssl
import sys
import time
import random
from datetime import datetime
from pathlib import Path
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError
from urllib.parse import quote

try:
    import certifi
    SSL_CONTEXT = ssl.create_default_context(cafile=certifi.where())
except ImportError:
    SSL_CONTEXT = ssl.create_default_context()

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parent.parent
LEDGER_DIR = PROJECT_ROOT / "LEDGER"
LOGS_DIR = PROJECT_ROOT / "AUTOMATIONS" / "logs"
CACHE_DIR = PROJECT_ROOT / "AUTOMATIONS" / "logs" / "market_cache"
OUTPUT_CSV = LEDGER_DIR / "MARKET_SIZE_ESTIMATES.csv"
LOG_FILE = LOGS_DIR / "market_size.log"

for d in [LEDGER_DIR, LOGS_DIR, CACHE_DIR]:
    d.mkdir(parents=True, exist_ok=True)

def safe_path(target):
    resolved = Path(target).resolve()
    if not str(resolved).startswith(str(PROJECT_ROOT)):
        raise ValueError(f"BLOCKED: {resolved} is outside project root")
    return resolved

# ---------------------------------------------------------------------------
# Utilities
# ---------------------------------------------------------------------------
_last_request_time = 0.0

def rate_limit(min_delay=1.5):
    global _last_request_time
    elapsed = time.time() - _last_request_time
    if elapsed < min_delay:
        jitter = random.uniform(0.1, 0.4)
        time.sleep(min_delay - elapsed + jitter)
    _last_request_time = time.time()

def log(msg):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] {msg}"
    print(line)
    try:
        with open(LOG_FILE, "a") as f:
            f.write(line + "\n")
    except Exception:
        pass

def fetch_url(url, timeout=20, min_delay=1.5):
    rate_limit(min_delay)
    req = Request(url, headers={
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    })
    for attempt in range(3):
        try:
            with urlopen(req, timeout=timeout, context=SSL_CONTEXT) as resp:
                data = resp.read()
                encoding = resp.headers.get_content_charset() or "utf-8"
                return data.decode(encoding, errors="replace")
        except (URLError, HTTPError) as e:
            if attempt < 2:
                time.sleep(2 * (attempt + 1))
                continue
            return None
        except Exception:
            return None
    return None

def fetch_json(url, timeout=15, min_delay=1.0):
    rate_limit(min_delay)
    req = Request(url, headers={
        "User-Agent": "PrintMaxx-MarketEstimator/1.0",
        "Accept": "application/json",
    })
    try:
        with urlopen(req, timeout=timeout, context=SSL_CONTEXT) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except Exception:
        return None

# ---------------------------------------------------------------------------
# Market definitions
# ---------------------------------------------------------------------------
VENTURES = {
    "faith": {
        "label": "Faith/Prayer Apps",
        "trends_keywords": ["prayer app", "bible app", "devotional app", "christian app"],
        "itunes_search_terms": ["prayer meditation", "bible app", "devotional", "christian"],
        "reddit_subs": ["Christianity", "prayer", "Bible", "Catholicism", "Reformed", "latterdaysaints"],
        "gumroad_keywords": ["prayer", "devotional", "bible study", "faith"],
        "tam_base_usd": 5_800_000_000,  # Global religious apps market (Statista est)
        "sam_pct": 0.15,  # US iOS faith apps
        "som_pct": 0.001,  # Realistic year-1 capture
    },
    "screen_time": {
        "label": "Screen Time / Digital Wellness",
        "trends_keywords": ["screen time app", "phone addiction", "digital detox", "app blocker"],
        "itunes_search_terms": ["screen time", "phone addiction", "app blocker", "digital wellbeing"],
        "reddit_subs": ["nosurf", "digitalminimalism", "phonesarebad", "productivity"],
        "gumroad_keywords": ["digital detox", "screen time", "phone addiction"],
        "tam_base_usd": 3_200_000_000,  # Digital wellness market
        "sam_pct": 0.20,
        "som_pct": 0.001,
    },
    "study": {
        "label": "Study / EdTech Apps",
        "trends_keywords": ["study app", "flashcard app", "homework help", "ai tutor"],
        "itunes_search_terms": ["study help", "flashcards", "homework", "ai study"],
        "reddit_subs": ["GetStudying", "studytips", "college", "highschool", "HomeworkHelp", "learnprogramming"],
        "gumroad_keywords": ["study guide", "flashcards", "course", "tutorial"],
        "tam_base_usd": 18_000_000_000,  # EdTech mobile learning
        "sam_pct": 0.08,
        "som_pct": 0.0005,
    },
    "fitness": {
        "label": "Fitness / Workout Apps",
        "trends_keywords": ["workout app", "fitness tracker", "gym app", "exercise app"],
        "itunes_search_terms": ["workout tracker", "fitness app", "gym workout", "exercise"],
        "reddit_subs": ["Fitness", "bodyweightfitness", "GYM", "xxfitness", "running", "weightroom"],
        "gumroad_keywords": ["workout plan", "fitness guide", "gym program"],
        "tam_base_usd": 14_700_000_000,  # Fitness app market
        "sam_pct": 0.10,
        "som_pct": 0.0003,
    },
    "productivity": {
        "label": "Productivity / Focus Apps",
        "trends_keywords": ["focus app", "pomodoro app", "productivity app", "todo app"],
        "itunes_search_terms": ["focus timer", "pomodoro", "productivity", "task manager"],
        "reddit_subs": ["productivity", "getdisciplined", "ADHD", "bulletjournal", "notion"],
        "gumroad_keywords": ["productivity", "notion template", "planner", "focus"],
        "tam_base_usd": 8_500_000_000,  # Productivity apps market
        "sam_pct": 0.12,
        "som_pct": 0.0005,
    },
    "sleep": {
        "label": "Sleep / Relaxation Apps",
        "trends_keywords": ["sleep app", "sleep tracker", "white noise app", "meditation sleep"],
        "itunes_search_terms": ["sleep tracker", "sleep sounds", "meditation sleep", "sleep stories"],
        "reddit_subs": ["sleep", "insomnia", "Meditation", "relaxation", "ASMR"],
        "gumroad_keywords": ["sleep", "meditation", "relaxation", "ambient sounds"],
        "tam_base_usd": 6_200_000_000,  # Sleep aids/tech market
        "sam_pct": 0.15,
        "som_pct": 0.0005,
    },
    "journal": {
        "label": "Journal / Mental Health Apps",
        "trends_keywords": ["journal app", "gratitude app", "mood tracker", "mental health app"],
        "itunes_search_terms": ["journal diary", "gratitude", "mood tracker", "mental health"],
        "reddit_subs": ["Journaling", "mentalhealth", "selfimprovement", "DecidingToBeBetter", "gratitude"],
        "gumroad_keywords": ["journal", "gratitude", "mental health", "self care"],
        "tam_base_usd": 4_800_000_000,  # Mental health apps market
        "sam_pct": 0.12,
        "som_pct": 0.0008,
    },
}


# ---------------------------------------------------------------------------
# 1. Google Trends demand signals
# ---------------------------------------------------------------------------
def get_google_trends_interest(keywords):
    """
    Query Google Trends explore page for relative interest data.
    Uses the public embed/widget endpoint (no API key needed).
    Returns interest score 0-100 for each keyword.
    """
    results = {}

    for kw in keywords:
        # Google Trends explore URL (public, returns HTML with embedded data)
        url = (
            f"https://trends.google.com/trends/api/dailytrends?"
            f"hl=en-US&tz=240&geo=US&ns=15"
        )
        # Alternate: use the interest over time widget
        explore_url = (
            f"https://trends.google.com/trends/explore?"
            f"q={quote(kw)}&geo=US&hl=en-US"
        )

        html = fetch_url(explore_url, min_delay=3.0)
        if not html:
            results[kw] = {"status": "fetch_failed", "interest": None}
            continue

        # Extract interest data from the page
        # Google Trends embeds JSON data in the page for rendering charts
        interest_score = None

        # Look for the interest over time data in page source
        # Pattern: numbers in the trend line data
        numbers = re.findall(r'"value":(\d+)', html)
        if numbers:
            values = [int(n) for n in numbers if 0 <= int(n) <= 100]
            if values:
                interest_score = values[-1]  # Most recent value
                avg_score = sum(values) / len(values)
                results[kw] = {
                    "status": "ok",
                    "interest": interest_score,
                    "avg_interest": round(avg_score, 1),
                    "data_points": len(values),
                    "trend": "rising" if values[-1] > avg_score else "declining",
                }
                continue

        # Fallback: check for "interest over time" related data
        # Try extracting from JSON-like structures
        json_blocks = re.findall(r'\{[^{}]{50,500}\}', html)
        for block in json_blocks[:20]:
            if "value" in block:
                vals = re.findall(r'"value"\s*:\s*(\d+)', block)
                if vals:
                    int_vals = [int(v) for v in vals if 0 <= int(v) <= 100]
                    if int_vals:
                        interest_score = int_vals[-1]
                        break

        results[kw] = {
            "status": "ok" if interest_score else "no_data",
            "interest": interest_score,
        }

    return results


# ---------------------------------------------------------------------------
# 2. App Store category size estimation
# ---------------------------------------------------------------------------
def estimate_app_store_category(search_terms):
    """
    Estimate category size by searching iTunes and analyzing results.
    Looks at rating counts as proxy for downloads.
    """
    total_ratings = 0
    apps_found = 0
    free_count = 0
    paid_count = 0
    paid_prices = []
    top_apps = []

    for term in search_terms:
        url = f"https://itunes.apple.com/search?term={quote(term)}&entity=software&country=us&limit=25"
        data = fetch_json(url, min_delay=1.2)
        if not data or not data.get("results"):
            continue

        seen_ids = set()
        for app in data["results"]:
            track_id = app.get("trackId")
            if track_id in seen_ids:
                continue
            seen_ids.add(track_id)

            rating_count = app.get("userRatingCount", 0)
            price = app.get("price", 0)

            total_ratings += rating_count
            apps_found += 1

            if price == 0:
                free_count += 1
            else:
                paid_count += 1
                paid_prices.append(price)

            top_apps.append({
                "name": app.get("trackName", ""),
                "rating_count": rating_count,
                "price": price,
                "rating": round(app.get("averageUserRating", 0), 1),
            })

    # Sort by rating count (proxy for popularity)
    top_apps.sort(key=lambda x: x["rating_count"], reverse=True)

    # Estimate downloads: roughly 1 rating per 30-50 downloads (industry average)
    est_downloads = total_ratings * 40  # Conservative middle estimate

    # Estimate revenue: downloads * conversion_rate * avg_price
    avg_price = (sum(paid_prices) / len(paid_prices)) if paid_prices else 4.99
    conversion_rate = 0.05  # 5% paid conversion is typical for freemium
    est_annual_revenue = est_downloads * conversion_rate * avg_price * 12 / len(search_terms)

    return {
        "apps_found": apps_found,
        "total_ratings": total_ratings,
        "estimated_downloads": est_downloads,
        "free_ratio": round(free_count / max(apps_found, 1) * 100, 1),
        "avg_paid_price": round(avg_price, 2),
        "estimated_category_annual_revenue": round(est_annual_revenue, 0),
        "top_apps": top_apps[:10],
    }


# ---------------------------------------------------------------------------
# 3. Gumroad category estimation
# ---------------------------------------------------------------------------
def estimate_gumroad_category(keywords):
    """Estimate Gumroad sales volume for a category by scraping discover pages."""
    total_products = 0
    total_est_sales = 0
    prices = []

    for kw in keywords:
        url = f"https://gumroad.com/discover?query={quote(kw)}"
        html = fetch_url(url, min_delay=2.5)
        if not html:
            continue

        # Extract product prices
        price_matches = re.findall(r'\$(\d+(?:\.\d{2})?)', html)
        for p in price_matches[:30]:
            try:
                val = float(p)
                if 1 <= val <= 5000:
                    prices.append(val)
                    total_products += 1
            except ValueError:
                continue

        # Extract sales counts
        sales_matches = re.findall(r'(\d[\d,]*)\s*(?:sales|sold|ratings?)', html.lower())
        for s in sales_matches:
            try:
                total_est_sales += int(s.replace(",", ""))
            except ValueError:
                continue

    avg_price = round(sum(prices) / len(prices), 2) if prices else 0
    est_monthly_volume = total_est_sales / max(len(keywords), 1)

    return {
        "products_found": total_products,
        "avg_price": avg_price,
        "price_range": f"${min(prices):.0f}-${max(prices):.0f}" if prices else "N/A",
        "total_est_sales": total_est_sales,
        "est_monthly_volume": round(est_monthly_volume),
        "est_monthly_revenue": round(est_monthly_volume * avg_price, 0),
    }


# ---------------------------------------------------------------------------
# 4. Reddit community size as market proxy
# ---------------------------------------------------------------------------
def get_reddit_community_sizes(subreddits):
    """Get subscriber counts for subreddits using Reddit's JSON API (no auth)."""
    results = []
    total_subscribers = 0

    for sub in subreddits:
        url = f"https://www.reddit.com/r/{sub}/about.json"
        data = fetch_json(url, min_delay=2.0)

        if data and data.get("data"):
            sub_data = data["data"]
            subscribers = sub_data.get("subscribers", 0)
            active = sub_data.get("active_user_count") or sub_data.get("accounts_active", 0)
            total_subscribers += subscribers

            results.append({
                "subreddit": sub,
                "subscribers": subscribers,
                "active_users": active,
                "created_utc": sub_data.get("created_utc", 0),
            })
        else:
            results.append({
                "subreddit": sub,
                "subscribers": 0,
                "active_users": 0,
                "status": "fetch_failed",
            })

    return {
        "subreddits": results,
        "total_subscribers": total_subscribers,
        "largest": max(results, key=lambda x: x.get("subscribers", 0)) if results else None,
    }


# ---------------------------------------------------------------------------
# TAM/SAM/SOM calculation
# ---------------------------------------------------------------------------
def estimate_market_size(venture_key, venture_data):
    """Calculate TAM/SAM/SOM for a single venture."""
    log(f"\n{'='*50}")
    log(f"ESTIMATING: {venture_data['label']}")
    log(f"{'='*50}")

    result = {
        "venture": venture_key,
        "label": venture_data["label"],
        "analysis_date": datetime.now().isoformat(),
    }

    # 1. Google Trends
    log("  [1/4] Google Trends demand signals...")
    trends = get_google_trends_interest(venture_data["trends_keywords"])
    trend_scores = [t.get("interest") for t in trends.values() if t.get("interest")]
    avg_trend = round(sum(trend_scores) / len(trend_scores), 1) if trend_scores else 0
    result["trends_avg_interest"] = avg_trend
    result["trends_data"] = trends
    log(f"    Avg interest: {avg_trend}/100 | Keywords: {len(trend_scores)}/{len(venture_data['trends_keywords'])}")

    # 2. App Store category
    log("  [2/4] App Store category size...")
    app_data = estimate_app_store_category(venture_data["itunes_search_terms"])
    result["app_store"] = app_data
    log(f"    Apps found: {app_data['apps_found']} | Total ratings: {app_data['total_ratings']:,}")
    log(f"    Est downloads: {app_data['estimated_downloads']:,} | Free ratio: {app_data['free_ratio']}%")
    log(f"    Est category revenue: ${app_data['estimated_category_annual_revenue']:,.0f}/yr")

    # 3. Gumroad
    log("  [3/4] Gumroad category volume...")
    gumroad = estimate_gumroad_category(venture_data["gumroad_keywords"])
    result["gumroad"] = gumroad
    log(f"    Products: {gumroad['products_found']} | Avg price: ${gumroad['avg_price']}")
    log(f"    Est monthly revenue: ${gumroad['est_monthly_revenue']:,.0f}")

    # 4. Reddit
    log("  [4/4] Reddit community sizes...")
    reddit = get_reddit_community_sizes(venture_data["reddit_subs"])
    result["reddit"] = reddit
    log(f"    Total subscribers: {reddit['total_subscribers']:,}")
    if reddit["largest"]:
        log(f"    Largest: r/{reddit['largest']['subreddit']} ({reddit['largest']['subscribers']:,})")

    # Calculate TAM/SAM/SOM
    tam = venture_data["tam_base_usd"]
    sam = tam * venture_data["sam_pct"]
    som = tam * venture_data["som_pct"]

    # Adjust based on signals
    # Trend adjustment: high interest = larger effective market
    if avg_trend > 70:
        trend_multiplier = 1.2
    elif avg_trend > 40:
        trend_multiplier = 1.0
    else:
        trend_multiplier = 0.8

    # Reddit adjustment: large communities = validated demand
    if reddit["total_subscribers"] > 1_000_000:
        community_multiplier = 1.15
    elif reddit["total_subscribers"] > 100_000:
        community_multiplier = 1.0
    else:
        community_multiplier = 0.85

    # App store adjustment: high competition = validated market but harder
    if app_data["apps_found"] > 50:
        competition_factor = 0.9  # Harder to capture share
    elif app_data["apps_found"] > 20:
        competition_factor = 1.0
    else:
        competition_factor = 1.1  # Less competition = easier capture

    adjusted_sam = sam * trend_multiplier * community_multiplier
    adjusted_som = som * trend_multiplier * community_multiplier * competition_factor

    result["tam"] = round(tam, 0)
    result["sam"] = round(adjusted_sam, 0)
    result["som"] = round(adjusted_som, 0)
    result["som_monthly"] = round(adjusted_som / 12, 0)
    result["trend_multiplier"] = trend_multiplier
    result["community_multiplier"] = community_multiplier
    result["competition_factor"] = competition_factor

    # Confidence score (0-100)
    data_points = 0
    if trend_scores:
        data_points += 25
    if app_data["apps_found"] > 0:
        data_points += 25
    if gumroad["products_found"] > 0:
        data_points += 25
    if reddit["total_subscribers"] > 0:
        data_points += 25
    result["confidence"] = data_points

    log(f"\n  MARKET SIZE ESTIMATES:")
    log(f"    TAM: ${tam:>15,.0f}")
    log(f"    SAM: ${adjusted_sam:>15,.0f} (trend: {trend_multiplier}x, community: {community_multiplier}x)")
    log(f"    SOM: ${adjusted_som:>15,.0f} (competition: {competition_factor}x)")
    log(f"    SOM/mo: ${adjusted_som/12:>12,.0f}")
    log(f"    Confidence: {data_points}/100")

    return result


# ---------------------------------------------------------------------------
# Output
# ---------------------------------------------------------------------------
def write_csv(estimates):
    """Write all estimates to CSV."""
    safe_path(OUTPUT_CSV)
    fieldnames = [
        "venture", "label", "tam", "sam", "som", "som_monthly",
        "trends_avg_interest", "app_store_apps_found", "app_store_total_ratings",
        "app_store_est_downloads", "app_store_free_ratio", "app_store_est_revenue",
        "gumroad_products", "gumroad_avg_price", "gumroad_est_monthly_rev",
        "reddit_total_subs", "reddit_largest_sub", "reddit_largest_count",
        "confidence", "trend_multiplier", "community_multiplier", "competition_factor",
        "analysis_date",
    ]

    rows = []
    for est in estimates:
        reddit = est.get("reddit", {})
        largest = reddit.get("largest", {})
        app = est.get("app_store", {})
        gm = est.get("gumroad", {})

        rows.append({
            "venture": est["venture"],
            "label": est["label"],
            "tam": est["tam"],
            "sam": est["sam"],
            "som": est["som"],
            "som_monthly": est["som_monthly"],
            "trends_avg_interest": est.get("trends_avg_interest", ""),
            "app_store_apps_found": app.get("apps_found", ""),
            "app_store_total_ratings": app.get("total_ratings", ""),
            "app_store_est_downloads": app.get("estimated_downloads", ""),
            "app_store_free_ratio": app.get("free_ratio", ""),
            "app_store_est_revenue": app.get("estimated_category_annual_revenue", ""),
            "gumroad_products": gm.get("products_found", ""),
            "gumroad_avg_price": gm.get("avg_price", ""),
            "gumroad_est_monthly_rev": gm.get("est_monthly_revenue", ""),
            "reddit_total_subs": reddit.get("total_subscribers", ""),
            "reddit_largest_sub": largest.get("subreddit", "") if largest else "",
            "reddit_largest_count": largest.get("subscribers", "") if largest else "",
            "confidence": est.get("confidence", ""),
            "trend_multiplier": est.get("trend_multiplier", ""),
            "community_multiplier": est.get("community_multiplier", ""),
            "competition_factor": est.get("competition_factor", ""),
            "analysis_date": est.get("analysis_date", ""),
        })

    with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    log(f"\nWrote {len(rows)} estimates to {OUTPUT_CSV}")


def print_comparison(estimates):
    """Print side-by-side comparison of all ventures."""
    print(f"\n{'='*100}")
    print(f"  PRINTMAXX MARKET SIZE COMPARISON")
    print(f"  {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"{'='*100}")

    # Sort by SOM descending
    sorted_est = sorted(estimates, key=lambda x: x.get("som", 0), reverse=True)

    print(f"\n  {'Venture':<20} {'TAM':>14} {'SAM':>14} {'SOM':>14} {'SOM/mo':>12} {'Trend':>7} {'Conf':>6}")
    print(f"  {'-'*20} {'-'*14} {'-'*14} {'-'*14} {'-'*12} {'-'*7} {'-'*6}")

    for est in sorted_est:
        venture = est.get("label", "?")[:18]
        tam = f"${est.get('tam', 0)/1e9:.1f}B"
        sam = f"${est.get('sam', 0)/1e6:.0f}M"
        som = f"${est.get('som', 0)/1e3:.0f}K"
        som_mo = f"${est.get('som_monthly', 0)/1e3:.1f}K"
        trend = f"{est.get('trends_avg_interest', 0)}/100"
        conf = f"{est.get('confidence', 0)}%"
        print(f"  {venture:<20} {tam:>14} {sam:>14} {som:>14} {som_mo:>12} {trend:>7} {conf:>6}")

    # Rankings
    print(f"\n  RANKINGS:")
    by_som = sorted(estimates, key=lambda x: x.get("som", 0), reverse=True)
    for i, est in enumerate(by_som, 1):
        print(f"  {i}. {est['label']} - SOM: ${est.get('som', 0):,.0f}/yr (${est.get('som_monthly', 0):,.0f}/mo)")

    # Opportunity signals
    print(f"\n  OPPORTUNITY SIGNALS:")
    for est in sorted_est:
        signals = []
        if est.get("trends_avg_interest", 0) > 60:
            signals.append("HIGH search demand")
        if est.get("competition_factor", 1) > 1:
            signals.append("LOW app competition")
        reddit = est.get("reddit", {})
        if reddit.get("total_subscribers", 0) > 500000:
            signals.append("LARGE reddit communities")
        if signals:
            print(f"  {est['label']}: {' | '.join(signals)}")

    print()


def print_trends_only(estimates):
    """Print Google Trends data comparison."""
    print(f"\n{'='*70}")
    print(f"  GOOGLE TRENDS DEMAND SIGNALS")
    print(f"{'='*70}")

    for est in estimates:
        print(f"\n  {est['label']}:")
        trends = est.get("trends_data", {})
        for kw, data in trends.items():
            interest = data.get("interest", "N/A")
            trend_dir = data.get("trend", "unknown")
            print(f"    [{interest:>3}] {kw} ({trend_dir})")
    print()


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(
        description="PrintMaxx Market Size Estimator - TAM/SAM/SOM for each venture"
    )
    parser.add_argument("--all", action="store_true", help="Estimate all ventures")
    parser.add_argument("--estimate", type=str, metavar="CATEGORY", help="Estimate a specific category")
    parser.add_argument("--trends", action="store_true", help="Show Google Trends data only")
    parser.add_argument("--compare", action="store_true", help="Compare all ventures side-by-side")
    parser.add_argument("--list", action="store_true", help="List available categories")

    args = parser.parse_args()

    if args.list:
        print("\nAvailable categories:")
        for key, data in VENTURES.items():
            print(f"  {key:<15} {data['label']}")
        return

    if not any([args.all, args.estimate, args.trends, args.compare]):
        parser.print_help()
        return

    log("=" * 60)
    log("PRINTMAXX MARKET SIZE ESTIMATOR")
    log(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    log("=" * 60)

    # Load cached estimates if just comparing
    cache_file = CACHE_DIR / "latest_estimates.json"
    cached_estimates = []
    if cache_file.exists():
        try:
            with open(cache_file) as f:
                cached_estimates = json.load(f)
        except (json.JSONDecodeError, IOError):
            cached_estimates = []

    if args.compare and cached_estimates and not args.all:
        print_comparison(cached_estimates)
        return

    if args.trends and cached_estimates and not args.all:
        print_trends_only(cached_estimates)
        return

    estimates = []

    if args.estimate:
        key = args.estimate.lower().replace(" ", "_")
        if key not in VENTURES:
            print(f"Unknown category: {key}")
            print(f"Available: {', '.join(VENTURES.keys())}")
            sys.exit(1)
        result = estimate_market_size(key, VENTURES[key])
        estimates.append(result)

    elif args.all:
        for key, data in VENTURES.items():
            result = estimate_market_size(key, data)
            estimates.append(result)

    if estimates:
        # Save to cache
        safe_path(cache_file)
        with open(cache_file, "w") as f:
            json.dump(estimates, f, indent=2, default=str)

        # Write CSV
        write_csv(estimates)

        # Print comparison
        print_comparison(estimates)

        if args.trends:
            print_trends_only(estimates)

    log(f"\nDone. CSV: {OUTPUT_CSV}")


if __name__ == "__main__":
    main()
