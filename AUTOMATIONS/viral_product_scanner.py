#!/usr/bin/env python3

from __future__ import annotations
"""
Viral Product Arbitrage Scanner

Scans Facebook Ad Library for products with high ad density (validated viral products),
cross-references with Instagram/TikTok viral signals, and scores products on a
0-100 virality confidence scale.

Output: LEDGER/VIRAL_PRODUCTS_SCAN.csv

Usage:
    python3 viral_product_scanner.py --keywords "posture corrector,ice roller,gua sha" --min-ads 50
    python3 viral_product_scanner.py --keywords "led face mask" --min-ads 20 --country US
    python3 viral_product_scanner.py --resume  # Resume from last scan
    python3 viral_product_scanner.py --report  # Show latest scan results

Requires: pip install requests beautifulsoup4
"""

import argparse
import csv
import json
import os
import random
import re
import sys
import time
from datetime import datetime, timedelta
from pathlib import Path
from urllib.parse import quote_plus, urlencode

try:
    import requests
    from bs4 import BeautifulSoup
except ImportError:
    print("Missing dependencies. Run: pip install requests beautifulsoup4")
    sys.exit(1)

# ============================================================
# CONFIGURATION
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent
LEDGER_DIR = PROJECT_ROOT / "LEDGER"
OUTPUT_CSV = LEDGER_DIR / "VIRAL_PRODUCTS_SCAN.csv"
STATE_FILE = PROJECT_ROOT / "AUTOMATIONS" / ".viral_scanner_state.json"

# Rate limiting
MIN_DELAY = 2.0   # seconds between requests
MAX_DELAY = 5.0   # seconds between requests
MAX_RETRIES = 3

# Scoring weights
SCORING_WEIGHTS = {
    "ad_count":       0.30,  # number of concurrent active ads
    "ad_longevity":   0.25,  # how long ads have been running
    "multi_advertiser": 0.20,  # multiple different advertisers (not just one player)
    "price_sweet_spot": 0.10,  # $15-60 retail = impulse purchase zone
    "category_fit":   0.15,  # product category historically converts well
}

# Categories that historically convert well for viral dropshipping
HIGH_CONVERT_CATEGORIES = [
    "health", "wellness", "beauty", "skincare", "fitness",
    "home", "kitchen", "gadget", "pet", "phone", "accessory",
    "posture", "massage", "led", "organizer", "cleaning",
    "baby", "car", "travel", "sleep", "hair",
]

USER_AGENTS = [
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
]


# ============================================================
# HELPERS
# ============================================================

def get_headers():
    """Return randomized request headers."""
    return {
        "User-Agent": random.choice(USER_AGENTS),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "DNT": "1",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
    }


def rate_limit():
    """Sleep a random amount between MIN_DELAY and MAX_DELAY."""
    delay = random.uniform(MIN_DELAY, MAX_DELAY)
    time.sleep(delay)


def safe_request(url, params=None, retries=MAX_RETRIES):
    """Make a request with retry logic and rate limiting."""
    for attempt in range(retries):
        try:
            rate_limit()
            resp = requests.get(
                url,
                params=params,
                headers=get_headers(),
                timeout=30,
                allow_redirects=True,
            )
            if resp.status_code == 200:
                return resp
            elif resp.status_code == 429:
                wait = (attempt + 1) * 10
                print(f"  [!] Rate limited. Waiting {wait}s before retry {attempt+1}/{retries}")
                time.sleep(wait)
            elif resp.status_code >= 500:
                wait = (attempt + 1) * 5
                print(f"  [!] Server error {resp.status_code}. Retry {attempt+1}/{retries} in {wait}s")
                time.sleep(wait)
            else:
                print(f"  [!] HTTP {resp.status_code} for {url}")
                return None
        except requests.exceptions.Timeout:
            print(f"  [!] Timeout. Retry {attempt+1}/{retries}")
            time.sleep(5)
        except requests.exceptions.ConnectionError:
            print(f"  [!] Connection error. Retry {attempt+1}/{retries}")
            time.sleep(10)
        except Exception as e:
            print(f"  [!] Request error: {e}")
            return None
    print(f"  [X] Failed after {retries} retries: {url}")
    return None


def load_state():
    """Load scanner state for resume capability."""
    if STATE_FILE.exists():
        try:
            with open(STATE_FILE) as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            pass
    return {"scanned_keywords": [], "last_scan": None, "results": []}


def save_state(state):
    """Save scanner state for resume capability."""
    try:
        with open(STATE_FILE, "w") as f:
            json.dump(state, f, indent=2, default=str)
    except IOError as e:
        print(f"  [!] Could not save state: {e}")


# ============================================================
# FACEBOOK AD LIBRARY SCANNER
# ============================================================

def search_fb_ad_library(keyword, country="US"):
    """
    Search Facebook Ad Library for ads related to a keyword.

    The FB Ad Library has a public web interface at facebook.com/ads/library
    and a public API at graph.facebook.com. The API requires an access token
    for full results. This function uses the web interface as primary method
    and falls back to heuristic estimation.

    Returns dict with:
        - estimated_active_ads: int
        - sample_advertisers: list of advertiser names
        - sample_ad_start_dates: list of dates
        - landing_pages: list of URLs
        - ad_library_url: str (direct link to search results)
    """
    result = {
        "estimated_active_ads": 0,
        "sample_advertisers": [],
        "sample_ad_start_dates": [],
        "landing_pages": [],
        "ad_library_url": "",
        "scan_method": "web_scrape",
    }

    # Build the Ad Library search URL
    params = {
        "active_status": "active",
        "ad_type": "all",
        "country": country,
        "q": keyword,
        "search_type": "keyword_unordered",
        "media_type": "all",
    }
    search_url = "https://www.facebook.com/ads/library/?" + urlencode(params)
    result["ad_library_url"] = search_url

    print(f"  [*] Scanning FB Ad Library for: {keyword}")

    # Try the FB Ad Library API (requires access token, but we try public endpoint first)
    api_url = "https://graph.facebook.com/v18.0/ads_archive"
    api_params = {
        "search_terms": keyword,
        "ad_reached_countries": f'["{country}"]',
        "ad_active_status": "ACTIVE",
        "fields": "id,ad_creation_time,page_name,ad_snapshot_url",
        "limit": 500,
    }

    # Note: Without access_token, the API returns limited data.
    # We try anyway and supplement with heuristic methods.
    api_resp = safe_request(api_url, params=api_params)

    if api_resp and api_resp.status_code == 200:
        try:
            data = api_resp.json()
            ads = data.get("data", [])
            result["estimated_active_ads"] = len(ads)
            result["scan_method"] = "api"

            # Extract unique advertisers
            advertisers = set()
            dates = []
            for ad in ads[:50]:  # Sample first 50
                if "page_name" in ad:
                    advertisers.add(ad["page_name"])
                if "ad_creation_time" in ad:
                    dates.append(ad["ad_creation_time"][:10])

            result["sample_advertisers"] = list(advertisers)[:20]
            result["sample_ad_start_dates"] = sorted(dates)[:20]

            # Check for pagination (more results available)
            if "paging" in data and "next" in data["paging"]:
                # There are more pages, estimate total
                result["estimated_active_ads"] = max(
                    len(ads),
                    len(ads) * 3  # conservative multiplier
                )

            print(f"    Found {result['estimated_active_ads']} active ads via API")
            return result

        except (json.JSONDecodeError, KeyError) as e:
            print(f"    API parse error: {e}. Falling back to web scrape.")

    # Fallback: scrape the web interface
    print(f"    API unavailable (needs access token). Using web estimation.")
    web_resp = safe_request(search_url)

    if web_resp:
        try:
            soup = BeautifulSoup(web_resp.text, "html.parser")

            # Look for result count indicators in the page
            text = soup.get_text()

            # Try to find "X results" or similar count strings
            count_patterns = [
                r"(\d{1,3}(?:,\d{3})*)\s*results?",
                r"showing\s+(\d{1,3}(?:,\d{3})*)\s+ads?",
                r"(\d{1,3}(?:,\d{3})*)\s+active\s+ads?",
                r"found\s+(\d{1,3}(?:,\d{3})*)",
            ]

            for pattern in count_patterns:
                match = re.search(pattern, text, re.IGNORECASE)
                if match:
                    count_str = match.group(1).replace(",", "")
                    result["estimated_active_ads"] = int(count_str)
                    result["scan_method"] = "web_scrape_count"
                    print(f"    Found count in page: {result['estimated_active_ads']} ads")
                    break

            # Extract any visible advertiser names
            # FB Ad Library renders ads in cards with page names
            page_links = soup.find_all("a", href=re.compile(r"/ads/library/\?"))
            for link in page_links[:20]:
                name = link.get_text(strip=True)
                if name and len(name) > 2 and name not in result["sample_advertisers"]:
                    result["sample_advertisers"].append(name)

            # Extract landing page URLs
            external_links = soup.find_all("a", href=re.compile(r"https?://(?!facebook\.com)"))
            for link in external_links[:10]:
                href = link.get("href", "")
                if href and "facebook" not in href and "instagram" not in href:
                    result["landing_pages"].append(href)

        except Exception as e:
            print(f"    Web scrape parse error: {e}")

    # If we still have no data, try Google as additional signal
    if result["estimated_active_ads"] == 0:
        result["scan_method"] = "google_estimation"
        google_estimate = _estimate_from_google(keyword)
        result["estimated_active_ads"] = google_estimate
        print(f"    Google estimation: ~{google_estimate} ads (lower confidence)")

    return result


def _estimate_from_google(keyword):
    """
    Use Google search to estimate ad density for a product keyword.
    Searches for "[keyword] facebook ads" and counts results as a proxy.
    """
    query = f'"{keyword}" facebook ads shopify'
    url = f"https://www.google.com/search?q={quote_plus(query)}&num=50"

    resp = safe_request(url)
    if not resp:
        return 0

    try:
        soup = BeautifulSoup(resp.text, "html.parser")

        # Count search results as rough proxy
        results = soup.find_all("div", class_="g")
        result_count = len(results)

        # Look for "About X results" text
        stats = soup.find("div", id="result-stats")
        if stats:
            text = stats.get_text()
            match = re.search(r"About\s+([\d,]+)\s+results", text)
            if match:
                total = int(match.group(1).replace(",", ""))
                # Heuristic: 1% of Google results mentioning FB ads = rough ad count
                return min(total // 100, 500)

        # Fallback: use visible result count as multiplier
        return result_count * 3

    except Exception:
        return 0


# ============================================================
# INSTAGRAM VIRAL SIGNAL DETECTION
# ============================================================

def check_instagram_signals(keyword):
    """
    Check Instagram for viral signals on a product keyword.

    Uses Instagram's web interface to look for:
    - Hashtag post counts
    - Recent viral reels
    - Comment sentiment signals

    Returns dict with:
        - hashtag_post_count: int
        - recent_viral_reels: int (estimate)
        - comment_buy_signals: int (comments asking to buy)
        - ig_search_url: str
    """
    result = {
        "hashtag_post_count": 0,
        "recent_viral_reels": 0,
        "comment_buy_signals": 0,
        "ig_search_url": f"https://www.instagram.com/explore/tags/{quote_plus(keyword.replace(' ', ''))}/",
    }

    # Instagram heavily blocks scraping. Use web search as proxy.
    query = f'site:instagram.com "{keyword}" (link OR buy OR "where to get" OR "need this")'
    url = f"https://www.google.com/search?q={quote_plus(query)}&num=30&tbs=qdr:m"

    resp = safe_request(url)
    if not resp:
        return result

    try:
        soup = BeautifulSoup(resp.text, "html.parser")
        results = soup.find_all("div", class_="g")
        result["recent_viral_reels"] = len(results)

        # Check for buy-intent keywords in result snippets
        buy_keywords = ["where to buy", "link", "need this", "want this", "how to get",
                        "price", "shop", "store", "order", "purchase"]
        buy_signals = 0
        for r in results:
            snippet = r.get_text().lower()
            for kw in buy_keywords:
                if kw in snippet:
                    buy_signals += 1
                    break
        result["comment_buy_signals"] = buy_signals

    except Exception as e:
        print(f"    IG signal check error: {e}")

    # Also check hashtag volume via Google
    hashtag = keyword.replace(" ", "")
    hashtag_query = f'instagram.com/explore/tags/{hashtag} posts'
    resp2 = safe_request(f"https://www.google.com/search?q={quote_plus(hashtag_query)}")
    if resp2:
        try:
            text = resp2.text
            # Look for post count mentions
            count_match = re.search(r"([\d,.]+[KMB]?)\s*posts?", text, re.IGNORECASE)
            if count_match:
                count_str = count_match.group(1).replace(",", "")
                multiplier = 1
                if "K" in count_str.upper():
                    multiplier = 1000
                    count_str = count_str.upper().replace("K", "")
                elif "M" in count_str.upper():
                    multiplier = 1000000
                    count_str = count_str.upper().replace("M", "")
                elif "B" in count_str.upper():
                    multiplier = 1000000000
                    count_str = count_str.upper().replace("B", "")
                try:
                    result["hashtag_post_count"] = int(float(count_str) * multiplier)
                except ValueError:
                    pass
        except Exception:
            pass

    return result


# ============================================================
# TIKTOK VIRAL SIGNAL DETECTION
# ============================================================

def check_tiktok_signals(keyword):
    """
    Check TikTok for viral signals via web search proxy.

    Returns dict with:
        - tiktok_mentions: int
        - tiktok_buy_signals: int
        - tiktok_search_url: str
    """
    result = {
        "tiktok_mentions": 0,
        "tiktok_buy_signals": 0,
        "tiktok_search_url": f"https://www.tiktok.com/search?q={quote_plus(keyword)}",
    }

    query = f'site:tiktok.com "{keyword}" (review OR unboxing OR "must have" OR viral)'
    url = f"https://www.google.com/search?q={quote_plus(query)}&num=30&tbs=qdr:m"

    resp = safe_request(url)
    if not resp:
        return result

    try:
        soup = BeautifulSoup(resp.text, "html.parser")
        results = soup.find_all("div", class_="g")
        result["tiktok_mentions"] = len(results)

        buy_keywords = ["link in bio", "shop", "buy", "store", "must have", "need"]
        buy_count = 0
        for r in results:
            snippet = r.get_text().lower()
            for kw in buy_keywords:
                if kw in snippet:
                    buy_count += 1
                    break
        result["tiktok_buy_signals"] = buy_count

    except Exception:
        pass

    return result


# ============================================================
# ALIEXPRESS SOURCING CHECK
# ============================================================

def check_aliexpress_sourcing(keyword):
    """
    Check AliExpress for product sourcing availability and pricing.

    Returns dict with:
        - available: bool
        - price_range_low: float
        - price_range_high: float
        - supplier_count: int
        - orders_count: int (estimated)
        - aliexpress_url: str
    """
    result = {
        "available": False,
        "price_range_low": 0.0,
        "price_range_high": 0.0,
        "supplier_count": 0,
        "orders_count": 0,
        "aliexpress_url": f"https://www.aliexpress.com/wholesale?SearchText={quote_plus(keyword)}",
    }

    # AliExpress blocks scraping heavily. Use Google as proxy.
    query = f'site:aliexpress.com "{keyword}" orders'
    url = f"https://www.google.com/search?q={quote_plus(query)}&num=20"

    resp = safe_request(url)
    if not resp:
        return result

    try:
        soup = BeautifulSoup(resp.text, "html.parser")
        results = soup.find_all("div", class_="g")

        if results:
            result["available"] = True
            result["supplier_count"] = len(results)

            # Try to extract prices from snippets
            prices = []
            for r in results:
                text = r.get_text()
                price_matches = re.findall(r"\$(\d+\.?\d*)", text)
                for p in price_matches:
                    try:
                        price = float(p)
                        if 0.5 < price < 100:  # reasonable product price range
                            prices.append(price)
                    except ValueError:
                        pass

                # Extract order counts
                order_match = re.search(r"([\d,]+)\s*(?:orders?|sold|bought)", text, re.IGNORECASE)
                if order_match:
                    try:
                        orders = int(order_match.group(1).replace(",", ""))
                        result["orders_count"] = max(result["orders_count"], orders)
                    except ValueError:
                        pass

            if prices:
                result["price_range_low"] = round(min(prices), 2)
                result["price_range_high"] = round(max(prices), 2)

    except Exception as e:
        print(f"    AliExpress check error: {e}")

    return result


# ============================================================
# VIRALITY SCORING ENGINE
# ============================================================

def calculate_virality_score(fb_data, ig_data, tt_data, ae_data, keyword):
    """
    Score a product 0-100 on virality confidence.

    Scoring breakdown:
    - Ad count (30%): more concurrent ads = more validated
    - Ad longevity (25%): ads running 30+ days = profitable
    - Multi-advertiser (20%): many different advertisers = open market
    - Price sweet spot (10%): $15-60 retail
    - Category fit (15%): historically high-converting categories

    Returns tuple of (score, breakdown_dict)
    """
    breakdown = {}

    # 1. Ad count score (0-100, then weighted)
    ad_count = fb_data.get("estimated_active_ads", 0)
    if ad_count >= 200:
        ad_score = 100
    elif ad_count >= 100:
        ad_score = 85
    elif ad_count >= 50:
        ad_score = 70
    elif ad_count >= 20:
        ad_score = 50
    elif ad_count >= 10:
        ad_score = 30
    elif ad_count >= 5:
        ad_score = 15
    else:
        ad_score = 0
    breakdown["ad_count"] = ad_score

    # 2. Ad longevity score (approximated from dates if available)
    dates = fb_data.get("sample_ad_start_dates", [])
    if dates:
        try:
            oldest = datetime.strptime(min(dates)[:10], "%Y-%m-%d")
            days_running = (datetime.now() - oldest).days
            if days_running >= 60:
                longevity_score = 100
            elif days_running >= 30:
                longevity_score = 80
            elif days_running >= 14:
                longevity_score = 50
            elif days_running >= 7:
                longevity_score = 25
            else:
                longevity_score = 10
        except (ValueError, TypeError):
            longevity_score = 40  # unknown, give moderate score
    else:
        # No date data, estimate based on ad count (more ads = probably been running longer)
        longevity_score = min(ad_count, 100) * 0.5
    breakdown["ad_longevity"] = longevity_score

    # 3. Multi-advertiser score
    advertiser_count = len(fb_data.get("sample_advertisers", []))
    if advertiser_count >= 20:
        multi_score = 100
    elif advertiser_count >= 10:
        multi_score = 80
    elif advertiser_count >= 5:
        multi_score = 60
    elif advertiser_count >= 3:
        multi_score = 40
    elif advertiser_count >= 2:
        multi_score = 20
    else:
        # Estimate from ad count
        multi_score = min(ad_count // 5, 60)
    breakdown["multi_advertiser"] = multi_score

    # 4. Price sweet spot score
    low = ae_data.get("price_range_low", 0)
    high = ae_data.get("price_range_high", 0)
    avg_source_price = (low + high) / 2 if (low and high) else 0

    if avg_source_price > 0:
        # Estimated retail = source * 4-6x markup
        est_retail = avg_source_price * 5
        if 15 <= est_retail <= 60:
            price_score = 100
        elif 10 <= est_retail <= 80:
            price_score = 70
        elif 5 <= est_retail <= 100:
            price_score = 40
        else:
            price_score = 20
    else:
        price_score = 50  # unknown price, neutral
    breakdown["price_sweet_spot"] = price_score

    # 5. Category fit score
    keyword_lower = keyword.lower()
    category_score = 30  # baseline
    for cat in HIGH_CONVERT_CATEGORIES:
        if cat in keyword_lower:
            category_score = 85
            break

    # Boost for IG/TT signals
    ig_viral = ig_data.get("recent_viral_reels", 0)
    tt_viral = tt_data.get("tiktok_mentions", 0)
    if ig_viral >= 10 or tt_viral >= 10:
        category_score = min(100, category_score + 15)
    if ig_data.get("comment_buy_signals", 0) >= 3 or tt_data.get("tiktok_buy_signals", 0) >= 3:
        category_score = min(100, category_score + 10)

    breakdown["category_fit"] = category_score

    # Calculate weighted total
    total = 0
    for key, weight in SCORING_WEIGHTS.items():
        total += breakdown.get(key, 0) * weight

    total = round(total, 1)

    return total, breakdown


# ============================================================
# MAIN SCANNER PIPELINE
# ============================================================

def scan_product(keyword, country="US"):
    """
    Run full scan pipeline for a single product keyword.

    Returns dict with all scan data and virality score.
    """
    print(f"\n{'='*60}")
    print(f"  SCANNING: {keyword}")
    print(f"{'='*60}")

    # Step 1: Facebook Ad Library
    print(f"\n  [1/4] Facebook Ad Library...")
    fb_data = search_fb_ad_library(keyword, country)
    print(f"    Active ads: ~{fb_data['estimated_active_ads']}")
    print(f"    Advertisers: {len(fb_data['sample_advertisers'])}")
    print(f"    Method: {fb_data['scan_method']}")

    # Step 2: Instagram signals
    print(f"\n  [2/4] Instagram viral signals...")
    ig_data = check_instagram_signals(keyword)
    print(f"    Viral reels found: {ig_data['recent_viral_reels']}")
    print(f"    Buy signals: {ig_data['comment_buy_signals']}")
    print(f"    Hashtag posts: {ig_data['hashtag_post_count']:,}")

    # Step 3: TikTok signals
    print(f"\n  [3/4] TikTok viral signals...")
    tt_data = check_tiktok_signals(keyword)
    print(f"    TikTok mentions: {tt_data['tiktok_mentions']}")
    print(f"    Buy signals: {tt_data['tiktok_buy_signals']}")

    # Step 4: AliExpress sourcing
    print(f"\n  [4/4] AliExpress sourcing check...")
    ae_data = check_aliexpress_sourcing(keyword)
    print(f"    Available: {ae_data['available']}")
    if ae_data["available"]:
        print(f"    Price range: ${ae_data['price_range_low']}-${ae_data['price_range_high']}")
        print(f"    Suppliers: {ae_data['supplier_count']}")
        if ae_data["orders_count"]:
            print(f"    Orders: {ae_data['orders_count']:,}")

    # Step 5: Calculate virality score
    score, breakdown = calculate_virality_score(fb_data, ig_data, tt_data, ae_data, keyword)

    print(f"\n  VIRALITY SCORE: {score}/100")
    print(f"  Breakdown:")
    for key, val in breakdown.items():
        weight = SCORING_WEIGHTS.get(key, 0)
        print(f"    {key}: {val:.0f}/100 (weight: {weight*100:.0f}%)")

    # Determine recommendation
    if score >= 75:
        recommendation = "STRONG_BUY"
        rec_text = "test immediately with $80/day ads"
    elif score >= 55:
        recommendation = "BUY"
        rec_text = "worth testing with $50/day"
    elif score >= 40:
        recommendation = "WATCHLIST"
        rec_text = "monitor for 1-2 weeks, may be early"
    elif score >= 25:
        recommendation = "WEAK"
        rec_text = "limited signal, probably skip"
    else:
        recommendation = "SKIP"
        rec_text = "not enough validation"

    print(f"  RECOMMENDATION: {recommendation} ({rec_text})")

    # Calculate estimated margin if sourcing data available
    est_margin = ""
    est_retail = ""
    if ae_data["price_range_low"] > 0:
        source_cost = (ae_data["price_range_low"] + ae_data["price_range_high"]) / 2
        retail = source_cost * 5  # 5x markup
        shipping = 3.0  # estimated
        ad_cost_per_sale = retail / 2.5  # assuming 2.5x ROAS
        profit = retail - source_cost - shipping - ad_cost_per_sale - (retail * 0.029)  # stripe fee
        margin_pct = (profit / retail * 100) if retail > 0 else 0
        est_margin = f"{margin_pct:.0f}%"
        est_retail = f"${retail:.2f}"

    return {
        "keyword": keyword,
        "scan_date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "virality_score": score,
        "recommendation": recommendation,
        "estimated_active_ads": fb_data["estimated_active_ads"],
        "unique_advertisers": len(fb_data["sample_advertisers"]),
        "scan_method": fb_data["scan_method"],
        "ig_viral_reels": ig_data["recent_viral_reels"],
        "ig_buy_signals": ig_data["comment_buy_signals"],
        "ig_hashtag_posts": ig_data["hashtag_post_count"],
        "tt_mentions": tt_data["tiktok_mentions"],
        "tt_buy_signals": tt_data["tiktok_buy_signals"],
        "ae_available": ae_data["available"],
        "ae_price_low": ae_data["price_range_low"],
        "ae_price_high": ae_data["price_range_high"],
        "ae_suppliers": ae_data["supplier_count"],
        "ae_orders": ae_data["orders_count"],
        "estimated_retail_price": est_retail,
        "estimated_margin": est_margin,
        "ad_library_url": fb_data["ad_library_url"],
        "ig_search_url": ig_data["ig_search_url"],
        "tt_search_url": tt_data["tiktok_search_url"],
        "ae_search_url": ae_data["aliexpress_url"],
        "landing_pages": "|".join(fb_data.get("landing_pages", [])[:5]),
        "score_ad_count": breakdown.get("ad_count", 0),
        "score_longevity": breakdown.get("ad_longevity", 0),
        "score_multi_adv": breakdown.get("multi_advertiser", 0),
        "score_price": breakdown.get("price_sweet_spot", 0),
        "score_category": breakdown.get("category_fit", 0),
        "country": country,
    }


def write_results_to_csv(results, output_path=OUTPUT_CSV):
    """Write scan results to CSV, appending to existing file."""
    if not results:
        return

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    file_exists = output_path.exists()

    fieldnames = [
        "keyword", "scan_date", "virality_score", "recommendation",
        "estimated_active_ads", "unique_advertisers", "scan_method",
        "ig_viral_reels", "ig_buy_signals", "ig_hashtag_posts",
        "tt_mentions", "tt_buy_signals",
        "ae_available", "ae_price_low", "ae_price_high", "ae_suppliers", "ae_orders",
        "estimated_retail_price", "estimated_margin",
        "ad_library_url", "ig_search_url", "tt_search_url", "ae_search_url",
        "landing_pages",
        "score_ad_count", "score_longevity", "score_multi_adv", "score_price", "score_category",
        "country",
    ]

    with open(output_path, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        for result in results:
            writer.writerow(result)

    print(f"\n  Results written to: {output_path}")


def print_report(output_path=OUTPUT_CSV):
    """Print a summary report of latest scan results."""
    if not Path(output_path).exists():
        print("No scan results found. Run a scan first.")
        return

    with open(output_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    if not rows:
        print("No results in CSV.")
        return

    # Sort by virality score descending
    rows.sort(key=lambda x: float(x.get("virality_score", 0)), reverse=True)

    print(f"\n{'='*80}")
    print(f"  VIRAL PRODUCT SCAN REPORT")
    print(f"  {len(rows)} products scanned")
    print(f"{'='*80}\n")

    print(f"{'Rank':<5} {'Score':<7} {'Rec':<13} {'Ads':<6} {'Advs':<6} {'IG':<5} {'TT':<5} {'Product':<30}")
    print(f"{'-'*5} {'-'*7} {'-'*13} {'-'*6} {'-'*6} {'-'*5} {'-'*5} {'-'*30}")

    for i, row in enumerate(rows, 1):
        score = float(row.get("virality_score", 0))
        rec = row.get("recommendation", "?")
        ads = row.get("estimated_active_ads", "0")
        advs = row.get("unique_advertisers", "0")
        ig = row.get("ig_viral_reels", "0")
        tt = row.get("tt_mentions", "0")
        kw = row.get("keyword", "?")[:30]

        # Color coding via ASCII markers
        if rec == "STRONG_BUY":
            marker = ">>>"
        elif rec == "BUY":
            marker = " >>"
        elif rec == "WATCHLIST":
            marker = "  >"
        else:
            marker = "   "

        print(f"{marker}{i:<2} {score:<7.1f} {rec:<13} {ads:<6} {advs:<6} {ig:<5} {tt:<5} {kw:<30}")

    # Summary stats
    strong_buys = sum(1 for r in rows if r.get("recommendation") == "STRONG_BUY")
    buys = sum(1 for r in rows if r.get("recommendation") == "BUY")
    watchlist = sum(1 for r in rows if r.get("recommendation") == "WATCHLIST")

    print(f"\n  Summary: {strong_buys} STRONG_BUY | {buys} BUY | {watchlist} WATCHLIST")

    if strong_buys > 0:
        top = [r for r in rows if r.get("recommendation") == "STRONG_BUY"]
        print(f"\n  Top opportunities:")
        for r in top:
            kw = r.get("keyword", "?")
            score = r.get("virality_score", "?")
            margin = r.get("estimated_margin", "?")
            url = r.get("ad_library_url", "")
            print(f"    - {kw} (score: {score}, margin: {margin})")
            print(f"      FB Ads: {url}")


# ============================================================
# CLI
# ============================================================

def main():
    parser = argparse.ArgumentParser(
        description="Viral Product Arbitrage Scanner - Find validated viral products via FB Ad Library",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python3 viral_product_scanner.py --keywords "posture corrector,ice roller,gua sha" --min-ads 50
    python3 viral_product_scanner.py --keywords "led face mask" --country US
    python3 viral_product_scanner.py --resume
    python3 viral_product_scanner.py --report
        """,
    )

    parser.add_argument(
        "--keywords",
        type=str,
        help="Comma-separated product keywords to scan",
    )
    parser.add_argument(
        "--min-ads",
        type=int,
        default=0,
        help="Minimum active ads to include in results (default: 0, show all)",
    )
    parser.add_argument(
        "--country",
        type=str,
        default="US",
        help="Country code for ad library search (default: US)",
    )
    parser.add_argument(
        "--resume",
        action="store_true",
        help="Resume from last interrupted scan",
    )
    parser.add_argument(
        "--report",
        action="store_true",
        help="Show latest scan results report",
    )
    parser.add_argument(
        "--output",
        type=str,
        default=str(OUTPUT_CSV),
        help=f"Output CSV path (default: {OUTPUT_CSV})",
    )

    args = parser.parse_args()

    # Report mode
    if args.report:
        print_report(args.output)
        return

    # Resume mode
    if args.resume:
        state = load_state()
        remaining = [kw for kw in state.get("all_keywords", [])
                     if kw not in state.get("scanned_keywords", [])]
        if not remaining:
            print("No keywords remaining to scan. Run with --keywords to start a new scan.")
            return
        print(f"Resuming scan. {len(remaining)} keywords remaining:")
        for kw in remaining:
            print(f"  - {kw}")

        results = []
        for keyword in remaining:
            result = scan_product(keyword.strip(), args.country)
            results.append(result)
            state["scanned_keywords"].append(keyword)
            state["results"].append(result)
            save_state(state)

        # Filter by min-ads
        if args.min_ads > 0:
            results = [r for r in results if r["estimated_active_ads"] >= args.min_ads]

        write_results_to_csv(results, args.output)
        print_report(args.output)
        return

    # Normal scan mode - default to report if no keywords given
    if not args.keywords:
        print_report(args.output)
        return

    keywords = [kw.strip() for kw in args.keywords.split(",") if kw.strip()]

    if not keywords:
        print("Error: No valid keywords provided.")
        sys.exit(1)

    print(f"\nViral Product Scanner")
    print(f"Scanning {len(keywords)} product keywords")
    print(f"Country: {args.country}")
    print(f"Min ads filter: {args.min_ads}")
    print(f"Output: {args.output}")

    # Save state for resume
    state = load_state()
    state["all_keywords"] = keywords
    state["scanned_keywords"] = []
    state["results"] = []
    state["last_scan"] = datetime.now().isoformat()
    save_state(state)

    results = []
    for keyword in keywords:
        result = scan_product(keyword, args.country)
        results.append(result)

        # Update state
        state["scanned_keywords"].append(keyword)
        state["results"].append(result)
        save_state(state)

    # Filter by min-ads
    if args.min_ads > 0:
        filtered = [r for r in results if r["estimated_active_ads"] >= args.min_ads]
        if len(filtered) < len(results):
            print(f"\n  Filtered: {len(results) - len(filtered)} products below {args.min_ads} ads threshold")
        results = filtered

    # Write to CSV
    write_results_to_csv(results, args.output)

    # Print report
    print_report(args.output)

    # Print next steps
    strong = [r for r in results if r["recommendation"] == "STRONG_BUY"]
    buys = [r for r in results if r["recommendation"] == "BUY"]

    if strong or buys:
        print(f"\n{'='*60}")
        print(f"  NEXT STEPS")
        print(f"{'='*60}")
        print(f"  1. Click the FB Ad Library URLs above to verify ad counts manually")
        print(f"  2. Analyze winning creatives (hooks, formats, CTAs)")
        print(f"  3. Order product samples from AliExpress ($3-10)")
        print(f"  4. Set up Shopify store (2 hours max)")
        print(f"  5. Produce 5 ad creatives per product")
        print(f"  6. Launch Meta ads at $80/day")
        print(f"\n  Full playbook: MONEY_METHODS/ECOM/VIRAL_PRODUCT_ARB_PLAYBOOK.md")


if __name__ == "__main__":
    main()
