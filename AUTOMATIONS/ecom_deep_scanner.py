#!/usr/bin/env python3
"""
PRINTMAXX Ecom Deep Scanner - REAL OPPORTUNITY FINDER

Deep ecom opportunity scanner that aggregates signals from:
- Amazon Movers & Shakers (trending products)
- Google Trends product searches
- Reddit communities (r/dropship, r/FulfillmentByAmazon, r/Flipping)

For each opportunity: true margin after ALL fees, competition density,
trend trajectory, capital required.

Edge: bundle arbitrage, seasonal front-running, geographic arbitrage,
white-label upgrade, review mining.

Output: LEDGER/ECOM_DEEP_OPPORTUNITIES.csv

Usage:
    python3 ecom_deep_scanner.py --scan               # Full scan all sources
    python3 ecom_deep_scanner.py --deep PRODUCT        # Deep analysis of specific product
    python3 ecom_deep_scanner.py --margins             # Margin calculator for known products
    python3 ecom_deep_scanner.py --trending            # Show trending products only
    python3 ecom_deep_scanner.py --bundles             # Bundle arbitrage opportunities
"""

import argparse
import csv
import json
import os
import random
import re
import sys
import time
import urllib.request
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from types import SimpleNamespace
from urllib.parse import quote as urlquote

# ============================================================
# DEPENDENCIES
# ============================================================

try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    requests = None
    HAS_REQUESTS = False

try:
    from pytrends.request import TrendReq
    HAS_PYTRENDS = True
except ImportError:
    HAS_PYTRENDS = False
    TrendReq = None

# ============================================================
# PROJECT PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent
LEDGER_DIR = PROJECT_ROOT / "LEDGER"
OUTPUT_CSV = LEDGER_DIR / "ECOM_DEEP_OPPORTUNITIES.csv"
LOG_FILE = PROJECT_ROOT / "AUTOMATIONS" / "logs" / f"ecom_deep_{datetime.now().strftime('%Y-%m-%d')}.log"

# ============================================================
# PLATFORM FEES (comprehensive — every cost matters)
# ============================================================

PLATFORM_FEES = {
    'amazon_fba': {
        'referral_pct': 0.15, 'fba_fee_light': 3.22, 'fba_fee_medium': 5.40,
        'fba_fee_heavy': 8.26, 'storage_monthly_per_cuft': 0.87,
        'payment_pct': 0.0, 'payment_fixed': 0.0, 'name': 'Amazon FBA',
    },
    'amazon_fbm': {
        'referral_pct': 0.15, 'fba_fee_light': 0.0, 'fba_fee_medium': 0.0,
        'fba_fee_heavy': 0.0, 'storage_monthly_per_cuft': 0.0,
        'payment_pct': 0.0, 'payment_fixed': 0.0, 'name': 'Amazon FBM',
    },
    'ebay': {
        'referral_pct': 0.1325, 'fba_fee_light': 0.0, 'fba_fee_medium': 0.0,
        'fba_fee_heavy': 0.0, 'storage_monthly_per_cuft': 0.0,
        'payment_pct': 0.029, 'payment_fixed': 0.30, 'name': 'eBay',
    },
    'shopify': {
        'referral_pct': 0.0, 'fba_fee_light': 0.0, 'fba_fee_medium': 0.0,
        'fba_fee_heavy': 0.0, 'storage_monthly_per_cuft': 0.0,
        'payment_pct': 0.029, 'payment_fixed': 0.30, 'name': 'Shopify',
        'monthly_plan': 39.0,
    },
    'walmart': {
        'referral_pct': 0.15, 'fba_fee_light': 0.0, 'fba_fee_medium': 0.0,
        'fba_fee_heavy': 0.0, 'storage_monthly_per_cuft': 0.0,
        'payment_pct': 0.0, 'payment_fixed': 0.0, 'name': 'Walmart',
    },
    'etsy': {
        'referral_pct': 0.065, 'fba_fee_light': 0.0, 'fba_fee_medium': 0.0,
        'fba_fee_heavy': 0.0, 'storage_monthly_per_cuft': 0.0,
        'payment_pct': 0.03, 'payment_fixed': 0.25, 'name': 'Etsy',
        'listing_fee': 0.20,
    },
}

SHIPPING_COSTS = {
    'light': {'domestic': 4.50, 'source_china': 0.0, 'source_fast': 5.00},
    'medium': {'domestic': 8.00, 'source_china': 0.0, 'source_fast': 8.00},
    'heavy': {'domestic': 14.00, 'source_china': 3.00, 'source_fast': 15.00},
    'oversized': {'domestic': 22.00, 'source_china': 10.00, 'source_fast': 25.00},
}

# ============================================================
# AMAZON MOVERS & SHAKERS CATEGORIES
# ============================================================

AMAZON_MOVERS_CATEGORIES = {
    'overall': 'https://www.amazon.com/gp/moversandshakers/',
    'electronics': 'https://www.amazon.com/gp/moversandshakers/electronics/',
    'home_kitchen': 'https://www.amazon.com/gp/moversandshakers/home-garden/',
    'beauty': 'https://www.amazon.com/gp/moversandshakers/beauty/',
    'health': 'https://www.amazon.com/gp/moversandshakers/hpc/',
    'sports': 'https://www.amazon.com/gp/moversandshakers/sporting-goods/',
    'tools': 'https://www.amazon.com/gp/moversandshakers/hi/',
    'pet_supplies': 'https://www.amazon.com/gp/moversandshakers/pet-supplies/',
    'toys': 'https://www.amazon.com/gp/moversandshakers/toys-and-games/',
    'kitchen': 'https://www.amazon.com/gp/moversandshakers/kitchen/',
}

# ============================================================
# REDDIT SUBREDDITS FOR ECOM INTEL
# ============================================================

REDDIT_SUBREDDITS = {
    'dropship': {
        'url': 'https://www.reddit.com/r/dropship/top.json?t=week&limit=25',
        'signal': 'product ideas, supplier tips, niche validation',
    },
    'FulfillmentByAmazon': {
        'url': 'https://www.reddit.com/r/FulfillmentByAmazon/top.json?t=week&limit=25',
        'signal': 'FBA insights, product research, PPC tips',
    },
    'Flipping': {
        'url': 'https://www.reddit.com/r/Flipping/top.json?t=week&limit=25',
        'signal': 'arbitrage finds, sourcing tips, flip opportunities',
    },
    'AmazonSeller': {
        'url': 'https://www.reddit.com/r/AmazonSeller/top.json?t=week&limit=25',
        'signal': 'seller strategies, product launches, listing optimization',
    },
    'ecommerce': {
        'url': 'https://www.reddit.com/r/ecommerce/top.json?t=week&limit=25',
        'signal': 'general ecom trends, platform updates, growth tactics',
    },
}

# ============================================================
# PRODUCT DATABASE (known products with validated margins)
# ============================================================

KNOWN_PRODUCTS = {
    'portable blender': {'source': 6.50, 'sell': 29.99, 'weight': 'medium', 'category': 'kitchen'},
    'led face mask': {'source': 12.00, 'sell': 49.99, 'weight': 'medium', 'category': 'beauty'},
    'posture corrector': {'source': 3.50, 'sell': 19.99, 'weight': 'light', 'category': 'health'},
    'wireless earbuds': {'source': 5.00, 'sell': 24.99, 'weight': 'light', 'category': 'tech'},
    'resistance bands set': {'source': 3.00, 'sell': 14.99, 'weight': 'light', 'category': 'fitness'},
    'dog puzzle toy': {'source': 4.50, 'sell': 19.99, 'weight': 'medium', 'category': 'pet'},
    'shower head filter': {'source': 5.00, 'sell': 24.99, 'weight': 'medium', 'category': 'home'},
    'massage gun mini': {'source': 15.00, 'sell': 49.99, 'weight': 'medium', 'category': 'fitness'},
    'ice roller face': {'source': 2.00, 'sell': 12.99, 'weight': 'light', 'category': 'beauty'},
    'air fryer liner': {'source': 1.50, 'sell': 9.99, 'weight': 'light', 'category': 'kitchen'},
    'cat water fountain': {'source': 7.00, 'sell': 29.99, 'weight': 'medium', 'category': 'pet'},
    'gua sha tool': {'source': 1.50, 'sell': 14.99, 'weight': 'light', 'category': 'beauty'},
    'laptop stand': {'source': 6.00, 'sell': 29.99, 'weight': 'medium', 'category': 'tech'},
    'teeth whitening kit': {'source': 3.00, 'sell': 19.99, 'weight': 'light', 'category': 'beauty'},
    'vegetable chopper': {'source': 5.00, 'sell': 24.99, 'weight': 'medium', 'category': 'kitchen'},
    'ring light': {'source': 5.00, 'sell': 24.99, 'weight': 'medium', 'category': 'tech'},
    'foam roller': {'source': 4.50, 'sell': 19.99, 'weight': 'medium', 'category': 'fitness'},
    'bidet attachment': {'source': 8.00, 'sell': 34.99, 'weight': 'medium', 'category': 'home'},
    'scalp massager': {'source': 2.00, 'sell': 12.99, 'weight': 'light', 'category': 'beauty'},
    'knife sharpener': {'source': 3.00, 'sell': 14.99, 'weight': 'light', 'category': 'kitchen'},
    'neck stretcher': {'source': 4.00, 'sell': 19.99, 'weight': 'light', 'category': 'health'},
    'silk pillowcase': {'source': 4.50, 'sell': 24.99, 'weight': 'light', 'category': 'home'},
    'smart plug 4pack': {'source': 8.00, 'sell': 29.99, 'weight': 'light', 'category': 'tech'},
    'cold brew maker': {'source': 5.00, 'sell': 24.99, 'weight': 'medium', 'category': 'kitchen'},
    'ankle weights pair': {'source': 4.00, 'sell': 19.99, 'weight': 'medium', 'category': 'fitness'},
}

# ============================================================
# SEASONAL CALENDAR (front-running opportunities)
# ============================================================

SEASONAL_CALENDAR = {
    1: {'season': 'New Year', 'hot': ['fitness', 'health', 'planner', 'organizer', 'diet', 'gym'],
        'prep_months_before': 1},
    2: {'season': 'Valentine', 'hot': ['gift', 'jewelry', 'candle', 'beauty', 'couples'],
        'prep_months_before': 1},
    3: {'season': 'Spring', 'hot': ['garden', 'outdoor', 'cleaning', 'allergy', 'organizer'],
        'prep_months_before': 1},
    4: {'season': 'Easter/Spring', 'hot': ['garden', 'outdoor', 'basket', 'craft', 'decor'],
        'prep_months_before': 1},
    5: {'season': 'Mother Day', 'hot': ['gift', 'beauty', 'jewelry', 'spa', 'flower', 'kitchen'],
        'prep_months_before': 2},
    6: {'season': 'Father Day/Summer', 'hot': ['grill', 'tool', 'outdoor', 'golf', 'tech', 'cooler'],
        'prep_months_before': 2},
    7: {'season': 'Prime Day/Summer', 'hot': ['deals', 'pool', 'travel', 'camping', 'cooler', 'fan'],
        'prep_months_before': 2},
    8: {'season': 'Back to School', 'hot': ['backpack', 'laptop', 'desk', 'organizer', 'lunch box'],
        'prep_months_before': 2},
    9: {'season': 'Fall Prep', 'hot': ['halloween', 'costume', 'decor', 'candle', 'blanket'],
        'prep_months_before': 2},
    10: {'season': 'Halloween/Q4 Prep', 'hot': ['costume', 'decor', 'candy', 'led', 'gift prep'],
         'prep_months_before': 3},
    11: {'season': 'Black Friday/Thanksgiving', 'hot': ['deals', 'gift', 'kitchen', 'tech', 'toy'],
         'prep_months_before': 3},
    12: {'season': 'Christmas/Holiday', 'hot': ['gift', 'toy', 'decor', 'stocking', 'candle', 'game'],
         'prep_months_before': 3},
}

USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:122.0) Gecko/20100101 Firefox/122.0',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
]


def get_headers():
    return {
        'User-Agent': random.choice(USER_AGENTS),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
    }


def http_get(url: str, *, headers: dict = None, timeout: int = 15):
    """Best-effort HTTP GET with fallback from requests to urllib."""
    if headers is None:
        headers = get_headers()

    if HAS_REQUESTS:
        try:
            resp = requests.get(url, headers=headers, timeout=timeout)
            return resp
        except Exception:
            pass

    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            code = int(resp.getcode() or 0)
            body = resp.read()
        text = body.decode('utf-8', errors='replace')
        return SimpleNamespace(status_code=code, text=text, json=lambda: json.loads(text))
    except Exception:
        return SimpleNamespace(status_code=0, text='', json=lambda: {})


# ============================================================
# AMAZON MOVERS & SHAKERS SCANNER
# ============================================================

def scan_amazon_movers(categories: list = None, quiet: bool = False) -> list:
    """Scan Amazon Movers & Shakers for trending products."""
    if categories is None:
        categories = list(AMAZON_MOVERS_CATEGORIES.keys())

    products = []

    for cat in categories:
        url = AMAZON_MOVERS_CATEGORIES.get(cat)
        if not url:
            continue

        if not quiet:
            print(f"  Scanning Amazon Movers & Shakers: {cat}...")

        try:
            resp = http_get(url, headers=get_headers(), timeout=20)
            if resp.status_code != 200:
                if not quiet:
                    print(f"    Status {resp.status_code}, skipping")
                continue

            html = resp.text

            # Extract product titles and rank changes
            title_pattern = re.compile(
                r'<span[^>]*class="[^"]*a-size-base[^"]*"[^>]*>\s*([^<]{10,80})\s*</span>',
                re.DOTALL
            )
            price_pattern = re.compile(r'\$(\d+\.?\d{0,2})')

            titles = title_pattern.findall(html)
            prices = price_pattern.findall(html)

            # Deduplicate and clean
            seen = set()
            float_prices = [float(p) for p in prices if 3 < float(p) < 500]

            for i, title in enumerate(titles[:20]):
                title = title.strip()
                if len(title) < 5 or title in seen:
                    continue
                # Skip navigation elements
                if any(skip in title.lower() for skip in
                       ['see more', 'all categories', 'department', 'customer',
                        'back to', 'sign in', 'account', 'cart', 'menu']):
                    continue
                seen.add(title)

                price = float_prices[i] if i < len(float_prices) else None

                products.append({
                    'title': title,
                    'category': cat,
                    'source': 'amazon_movers',
                    'price': price,
                    'rank_change': None,  # would need JS rendering for actual rank %
                    'url': url,
                    'timestamp': datetime.now().isoformat(),
                })

            if not quiet:
                print(f"    Found {len(seen)} products in {cat}")

        except Exception as e:
            if not quiet:
                print(f"    Error scanning {cat}: {e}")

        time.sleep(random.uniform(2, 4))

    return products


# ============================================================
# REDDIT SCANNER
# ============================================================

def scan_reddit_ecom(subreddits: list = None, quiet: bool = False) -> list:
    """Scan Reddit ecom communities for product opportunities and intel."""
    if subreddits is None:
        subreddits = list(REDDIT_SUBREDDITS.keys())

    intel = []

    for sub_name in subreddits:
        sub_info = REDDIT_SUBREDDITS.get(sub_name)
        if not sub_info:
            continue

        if not quiet:
            print(f"  Scanning r/{sub_name}...")

        try:
            headers = get_headers()
            headers['Accept'] = 'application/json'
            resp = http_get(sub_info['url'], headers=headers, timeout=15)

            if resp.status_code != 200:
                if not quiet:
                    print(f"    Status {resp.status_code}, skipping")
                continue

            try:
                data = resp.json()
            except Exception:
                if not quiet:
                    print(f"    Failed to parse JSON for r/{sub_name}")
                continue

            posts = data.get('data', {}).get('children', [])

            for post_wrapper in posts:
                post = post_wrapper.get('data', {})
                title = post.get('title', '')
                selftext = post.get('selftext', '')[:500]
                score = post.get('score', 0)
                num_comments = post.get('num_comments', 0)
                permalink = post.get('permalink', '')

                if score < 5:
                    continue

                # Extract product mentions
                product_mentions = extract_product_mentions(title + ' ' + selftext)

                # Classify post type
                post_type = classify_reddit_post(title, selftext)

                intel.append({
                    'subreddit': sub_name,
                    'title': title[:120],
                    'score': score,
                    'comments': num_comments,
                    'post_type': post_type,
                    'product_mentions': product_mentions,
                    'url': f"https://reddit.com{permalink}" if permalink else '',
                    'signal': sub_info['signal'],
                    'timestamp': datetime.now().isoformat(),
                })

            if not quiet:
                print(f"    Found {len(posts)} posts, {sum(1 for p in intel if p['subreddit'] == sub_name)} relevant")

        except Exception as e:
            if not quiet:
                print(f"    Error scanning r/{sub_name}: {e}")

        time.sleep(random.uniform(2, 4))

    return intel


def extract_product_mentions(text: str) -> list:
    """Extract potential product mentions from text."""
    # Common ecom product keywords
    product_keywords = [
        'portable', 'wireless', 'bluetooth', 'LED', 'silicone', 'stainless',
        'bamboo', 'organic', 'reusable', 'foldable', 'magnetic', 'electric',
        'rechargeable', 'waterproof', 'adjustable', 'mini', 'smart',
    ]
    product_types = [
        'gadget', 'tool', 'device', 'kit', 'set', 'holder', 'organizer',
        'light', 'charger', 'cleaner', 'massager', 'bottle', 'bag', 'mat',
        'stand', 'cover', 'case', 'pad', 'roller', 'brush', 'rack',
    ]

    mentions = []
    text_lower = text.lower()

    for kw in product_keywords:
        if kw.lower() in text_lower:
            # Find the surrounding context
            idx = text_lower.find(kw.lower())
            start = max(0, idx - 20)
            end = min(len(text), idx + len(kw) + 30)
            context = text[start:end].strip()
            # Extract a clean product reference
            for pt in product_types:
                if pt in text_lower[idx:idx+50]:
                    mentions.append(f"{kw} {pt}")
                    break

    return list(set(mentions))[:5]


def classify_reddit_post(title: str, body: str) -> str:
    """Classify the type of Reddit post for ecom intel."""
    combined = (title + ' ' + body).lower()

    if any(w in combined for w in ['found', 'sourced', 'supplier', 'aliexpress', 'alibaba']):
        return 'SOURCING'
    if any(w in combined for w in ['profit', 'margin', 'revenue', 'sold', 'sales']):
        return 'RESULTS'
    if any(w in combined for w in ['trending', 'viral', 'hot', 'demand', 'growing']):
        return 'TREND'
    if any(w in combined for w in ['review', 'feedback', 'quality', 'complaint', 'return']):
        return 'REVIEW_INTEL'
    if any(w in combined for w in ['beginner', 'start', 'new to', 'advice', 'tips']):
        return 'ADVICE'
    if any(w in combined for w in ['niche', 'category', 'market', 'research']):
        return 'RESEARCH'
    if any(w in combined for w in ['ppc', 'ad', 'campaign', 'targeting', 'conversion']):
        return 'MARKETING'

    return 'GENERAL'


# ============================================================
# GOOGLE TRENDS SCANNER
# ============================================================

def scan_google_trends(keywords: list, timeframe: str = 'now 7-d',
                       quiet: bool = False) -> dict:
    """Get Google Trends interest scores for product keywords."""
    if not HAS_PYTRENDS:
        if not quiet:
            print("  [!] pytrends not installed. Using neutral scores.")
        return {k: 50 for k in keywords}

    try:
        pytrends = TrendReq(hl='en-US', tz=360)
    except Exception:
        return {k: 50 for k in keywords}

    results = {}

    for i in range(0, len(keywords), 5):
        batch = keywords[i:i+5]
        try:
            pytrends.build_payload(batch, timeframe=timeframe, geo='US')
            data = pytrends.interest_over_time()
            if not data.empty:
                for kw in batch:
                    if kw in data.columns:
                        values = data[kw].tolist()
                        results[kw] = int(data[kw].mean())
                        # Trend trajectory: compare last 3 days vs first 3 days
                        if len(values) >= 6:
                            early = sum(values[:3]) / 3
                            late = sum(values[-3:]) / 3
                            trajectory = 'rising' if late > early * 1.1 else \
                                        'falling' if late < early * 0.9 else 'stable'
                            results[f"{kw}_trajectory"] = trajectory
            time.sleep(random.uniform(1.5, 3))
        except Exception as e:
            if not quiet:
                print(f"    [!] Trends error for {batch}: {e}")
            for kw in batch:
                results[kw] = 50
            time.sleep(5)

    return results


# ============================================================
# TRUE MARGIN CALCULATOR
# ============================================================

def calculate_true_margin(sell_price: float, source_price: float,
                          weight_tier: str = 'medium',
                          platform: str = 'amazon_fba',
                          units_per_month: int = 30,
                          return_rate: float = 0.05,
                          ad_spend_pct: float = 0.15) -> dict:
    """
    Calculate TRUE margin after ALL costs.

    Most sellers forget: returns, ad spend, storage, payment processing.
    This calculator includes everything.
    """
    fees = PLATFORM_FEES.get(platform, PLATFORM_FEES['amazon_fba'])
    shipping = SHIPPING_COSTS.get(weight_tier, SHIPPING_COSTS['medium'])

    # Revenue
    gross_revenue = sell_price

    # Platform fees
    referral_fee = sell_price * fees['referral_pct']
    payment_fee = sell_price * fees['payment_pct'] + fees['payment_fixed']

    # Fulfillment fee (FBA)
    fba_fee = fees.get(f'fba_fee_{weight_tier}', fees.get('fba_fee_medium', 0))

    # Shipping from source
    source_shipping = shipping['source_china']

    # Domestic shipping (FBM only)
    domestic_shipping = 0.0
    if platform in ('amazon_fbm', 'ebay', 'etsy', 'shopify'):
        domestic_shipping = shipping['domestic']

    # Storage (FBA, estimated per unit)
    storage_cost = fees.get('storage_monthly_per_cuft', 0) * 0.25  # assume 0.25 cuft avg

    # Returns cost (lost product + return shipping)
    return_cost = (source_price + fba_fee) * return_rate

    # Ad spend
    ad_cost = sell_price * ad_spend_pct

    # Platform-specific costs
    listing_fee = fees.get('listing_fee', 0)
    monthly_plan = fees.get('monthly_plan', 0) / max(units_per_month, 1)

    # Total costs
    total_cost = (source_price + source_shipping + referral_fee + payment_fee +
                  fba_fee + domestic_shipping + storage_cost + return_cost +
                  ad_cost + listing_fee + monthly_plan)

    net_profit = gross_revenue - total_cost
    margin_pct = (net_profit / gross_revenue * 100) if gross_revenue > 0 else 0

    # Capital required
    initial_inventory = source_price * 100  # start with 100 units
    first_month_ads = ad_cost * units_per_month
    total_capital = initial_inventory + first_month_ads + (monthly_plan * max(units_per_month, 1))

    # Monthly projections
    monthly_revenue = sell_price * units_per_month
    monthly_profit = net_profit * units_per_month
    monthly_roi = (monthly_profit / total_capital * 100) if total_capital > 0 else 0

    return {
        'sell_price': round(sell_price, 2),
        'source_price': round(source_price, 2),
        'platform': fees['name'],
        'referral_fee': round(referral_fee, 2),
        'payment_fee': round(payment_fee, 2),
        'fba_fee': round(fba_fee, 2),
        'source_shipping': round(source_shipping, 2),
        'domestic_shipping': round(domestic_shipping, 2),
        'storage_cost': round(storage_cost, 2),
        'return_cost': round(return_cost, 2),
        'ad_cost': round(ad_cost, 2),
        'listing_fee': round(listing_fee, 2),
        'monthly_plan_per_unit': round(monthly_plan, 2),
        'total_cost': round(total_cost, 2),
        'net_profit': round(net_profit, 2),
        'margin_pct': round(margin_pct, 1),
        'capital_required': round(total_capital, 2),
        'monthly_revenue': round(monthly_revenue, 2),
        'monthly_profit': round(monthly_profit, 2),
        'monthly_roi_pct': round(monthly_roi, 1),
        'weight_tier': weight_tier,
        'units_per_month': units_per_month,
        'return_rate': return_rate,
        'ad_spend_pct': ad_spend_pct,
    }


def find_best_platform_deep(sell_price: float, source_price: float,
                            weight_tier: str = 'medium') -> dict:
    """Find the best platform with full margin breakdown."""
    best = None
    best_profit = -9999

    for platform_key in PLATFORM_FEES:
        result = calculate_true_margin(sell_price, source_price, weight_tier, platform_key)
        if result['net_profit'] > best_profit:
            best_profit = result['net_profit']
            best = result
            best['platform_key'] = platform_key

    return best


# ============================================================
# BUNDLE ARBITRAGE FINDER
# ============================================================

def find_bundle_opportunities(quiet: bool = False) -> list:
    """Find bundle arbitrage opportunities from known products."""
    bundles = []

    # Group products by category
    by_category = defaultdict(list)
    for name, info in KNOWN_PRODUCTS.items():
        by_category[info['category']].append((name, info))

    if not quiet:
        print(f"\n  Analyzing bundle opportunities across {len(by_category)} categories...")

    for category, products in by_category.items():
        if len(products) < 2:
            continue

        # Try all pairs
        for i in range(len(products)):
            for j in range(i + 1, len(products)):
                name_a, info_a = products[i]
                name_b, info_b = products[j]

                # Bundle pricing: 15-25% discount from buying separately
                individual_total = info_a['sell'] + info_b['sell']
                bundle_price = round(individual_total * 0.82, 2)  # 18% discount
                bundle_source = info_a['source'] + info_b['source']

                # Calculate bundle margin
                margin = calculate_true_margin(
                    bundle_price, bundle_source, 'medium', 'amazon_fba'
                )

                # Only include if bundle margin > individual margins
                margin_a = calculate_true_margin(
                    info_a['sell'], info_a['source'], info_a['weight'], 'amazon_fba'
                )
                margin_b = calculate_true_margin(
                    info_b['sell'], info_b['source'], info_b['weight'], 'amazon_fba'
                )

                individual_profit = margin_a['net_profit'] + margin_b['net_profit']

                if margin['net_profit'] > individual_profit * 0.9:
                    bundles.append({
                        'bundle_name': f"{name_a} + {name_b}",
                        'category': category,
                        'bundle_price': bundle_price,
                        'bundle_source_cost': bundle_source,
                        'bundle_profit': margin['net_profit'],
                        'bundle_margin_pct': margin['margin_pct'],
                        'individual_profit': round(individual_profit, 2),
                        'savings_to_customer': round(individual_total - bundle_price, 2),
                        'discount_pct': round((1 - bundle_price / individual_total) * 100, 1),
                        'edge': 'BUNDLE_ARBITRAGE',
                    })

    # Sort by bundle profit
    bundles.sort(key=lambda x: x['bundle_profit'], reverse=True)

    if not quiet:
        print(f"  Found {len(bundles)} bundle opportunities")

    return bundles


# ============================================================
# SEASONAL FRONT-RUNNING
# ============================================================

def get_seasonal_opportunities(quiet: bool = False) -> list:
    """Identify seasonal front-running opportunities."""
    current_month = datetime.now().month
    opportunities = []

    # Look 1-3 months ahead
    for offset in range(1, 4):
        target_month = ((current_month - 1 + offset) % 12) + 1
        season_info = SEASONAL_CALENDAR.get(target_month, {})

        if not season_info:
            continue

        months_until = offset
        prep_window = season_info.get('prep_months_before', 2)

        # Are we in the prep window?
        if months_until <= prep_window:
            urgency = 'NOW' if months_until <= 1 else 'SOON' if months_until <= 2 else 'PREP'

            for hot_keyword in season_info['hot']:
                opportunities.append({
                    'season': season_info['season'],
                    'target_month': target_month,
                    'months_until': months_until,
                    'keyword': hot_keyword,
                    'urgency': urgency,
                    'edge': 'SEASONAL_FRONTRUN',
                    'action': f"Source {hot_keyword} products now, list {months_until} months before peak",
                })

    if not quiet:
        print(f"\n  Seasonal front-running: {len(opportunities)} opportunities")
        for opp in opportunities[:5]:
            print(f"    [{opp['urgency']}] {opp['season']}: {opp['keyword']} "
                  f"({opp['months_until']}mo ahead)")

    return opportunities


# ============================================================
# OUTPUT & REPORTING
# ============================================================

def save_opportunities(opportunities: list):
    """Save opportunities to CSV."""
    LEDGER_DIR.mkdir(parents=True, exist_ok=True)

    fieldnames = [
        'timestamp', 'product', 'source_type', 'category', 'sell_price',
        'source_price', 'net_profit', 'margin_pct', 'platform', 'trend_score',
        'competition', 'capital_required', 'edge_tactic', 'action',
        'monthly_profit_est', 'notes',
    ]

    file_exists = OUTPUT_CSV.exists()
    with open(OUTPUT_CSV, 'a', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction='ignore')
        if not file_exists:
            writer.writeheader()
        for opp in opportunities:
            writer.writerow(opp)

    return OUTPUT_CSV


def print_margin_report(quiet: bool = False):
    """Print detailed margin report for all known products."""
    if quiet:
        return

    print(f"\n{'='*70}")
    print(f"  TRUE MARGIN REPORT — ALL COSTS INCLUDED")
    print(f"  Platform fees + shipping + returns + ad spend + storage")
    print(f"{'='*70}")

    results = []
    for product, info in sorted(KNOWN_PRODUCTS.items()):
        best = find_best_platform_deep(info['sell'], info['source'], info['weight'])
        results.append((product, best))

    results.sort(key=lambda x: x[1]['margin_pct'], reverse=True)

    print(f"\n  {'Product':<25} {'Sell':>7} {'Source':>7} {'Profit':>7} {'Margin':>7} "
          f"{'Platform':<12} {'Capital':>8} {'Mo.Profit':>10}")
    print(f"  {'-'*25} {'-'*7} {'-'*7} {'-'*7} {'-'*7} {'-'*12} {'-'*8} {'-'*10}")

    total_monthly = 0
    for product, result in results:
        profit_color = '\033[92m' if result['net_profit'] > 3 else \
                       '\033[93m' if result['net_profit'] > 0 else '\033[91m'
        reset = '\033[0m'
        print(f"  {product:<25} ${result['sell_price']:>5.2f} ${result['source_price']:>5.2f} "
              f"{profit_color}${result['net_profit']:>5.2f}{reset} {result['margin_pct']:>5.1f}% "
              f"{result['platform']:<12} ${result['capital_required']:>6.0f} "
              f"${result['monthly_profit']:>8.2f}")
        total_monthly += result['monthly_profit']

    print(f"\n  Total estimated monthly profit (30 units each): ${total_monthly:,.2f}")
    print(f"  Total products analyzed: {len(results)}")

    # Top 5 by ROI
    by_roi = sorted(results, key=lambda x: x[1]['monthly_roi_pct'], reverse=True)
    print(f"\n  TOP 5 BY ROI:")
    for product, result in by_roi[:5]:
        print(f"    {product:<25} ROI: {result['monthly_roi_pct']:.0f}%/mo "
              f"(${result['capital_required']:.0f} capital)")


def print_trending_report(amazon_products: list, reddit_intel: list,
                          trends_data: dict, quiet: bool = False):
    """Print consolidated trending report."""
    if quiet:
        return

    print(f"\n{'='*70}")
    print(f"  ECOM DEEP SCAN TRENDING REPORT — {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"{'='*70}")

    if amazon_products:
        print(f"\n  AMAZON MOVERS & SHAKERS ({len(amazon_products)} products):")
        by_cat = defaultdict(list)
        for p in amazon_products:
            by_cat[p['category']].append(p)

        for cat, prods in by_cat.items():
            print(f"\n    {cat.upper()}:")
            for p in prods[:5]:
                price_str = f"${p['price']:.2f}" if p.get('price') else 'N/A'
                print(f"      {p['title'][:50]:<50} {price_str}")

    if reddit_intel:
        print(f"\n  REDDIT INTEL ({len(reddit_intel)} posts):")
        by_type = defaultdict(list)
        for item in reddit_intel:
            by_type[item['post_type']].append(item)

        for post_type in ['TREND', 'RESULTS', 'SOURCING', 'RESEARCH']:
            posts = by_type.get(post_type, [])
            if posts:
                print(f"\n    {post_type} ({len(posts)} posts):")
                for p in sorted(posts, key=lambda x: x['score'], reverse=True)[:3]:
                    print(f"      [{p['score']:>4} pts] r/{p['subreddit']}: {p['title'][:60]}")
                    if p.get('product_mentions'):
                        print(f"               Products: {', '.join(p['product_mentions'][:3])}")

    if trends_data:
        rising = [(k, v) for k, v in trends_data.items()
                  if not k.endswith('_trajectory') and
                  trends_data.get(f"{k}_trajectory") == 'rising']
        if rising:
            print(f"\n  RISING TRENDS:")
            for kw, score in sorted(rising, key=lambda x: x[1], reverse=True)[:10]:
                bar = '#' * (score // 5)
                print(f"    {kw:<30} {score:>3}/100 {bar}")


# ============================================================
# MAIN
# ============================================================

def main():
    parser = argparse.ArgumentParser(
        description='PRINTMAXX Ecom Deep Scanner - Real opportunity finder'
    )
    parser.add_argument('--scan', action='store_true',
                        help='Full scan: Amazon Movers, Reddit, Trends')
    parser.add_argument('--deep', type=str, metavar='PRODUCT',
                        help='Deep analysis of specific product')
    parser.add_argument('--margins', action='store_true',
                        help='Show true margins for all known products')
    parser.add_argument('--trending', action='store_true',
                        help='Show trending products only')
    parser.add_argument('--bundles', action='store_true',
                        help='Show bundle arbitrage opportunities')
    parser.add_argument('--seasonal', action='store_true',
                        help='Show seasonal front-running opportunities')
    parser.add_argument('--platform', type=str, default='amazon_fba',
                        choices=list(PLATFORM_FEES.keys()),
                        help='Platform for margin calculations')
    parser.add_argument('--quiet', action='store_true',
                        help='Quiet mode for automation')
    args = parser.parse_args()

    if not any([args.scan, args.deep, args.margins, args.trending,
                args.bundles, args.seasonal]):
        parser.print_help()
        print("\n  example: python3 ecom_deep_scanner.py --scan")
        print("  example: python3 ecom_deep_scanner.py --deep 'portable blender'")
        print("  example: python3 ecom_deep_scanner.py --margins")
        print("  example: python3 ecom_deep_scanner.py --bundles")
        return

    if args.margins:
        print_margin_report(quiet=args.quiet)
        return

    if args.deep:
        product_name = args.deep.lower()
        print(f"\n{'='*60}")
        print(f"  DEEP ANALYSIS: {product_name}")
        print(f"{'='*60}")

        # Check known products
        known = KNOWN_PRODUCTS.get(product_name)
        if known:
            print(f"\n  Known product data:")
            print(f"    Source price: ${known['source']}")
            print(f"    Sell price:   ${known['sell']}")
            print(f"    Weight:       {known['weight']}")
            print(f"    Category:     {known['category']}")

            # Calculate margins on all platforms
            print(f"\n  Platform comparison:")
            print(f"  {'Platform':<18} {'Profit':>8} {'Margin':>8} {'Capital':>10} {'Mo.ROI':>8}")
            print(f"  {'-'*18} {'-'*8} {'-'*8} {'-'*10} {'-'*8}")

            for platform_key in PLATFORM_FEES:
                result = calculate_true_margin(
                    known['sell'], known['source'], known['weight'], platform_key
                )
                profit_color = '\033[92m' if result['net_profit'] > 3 else \
                               '\033[93m' if result['net_profit'] > 0 else '\033[91m'
                reset = '\033[0m'
                print(f"  {result['platform']:<18} "
                      f"{profit_color}${result['net_profit']:>6.2f}{reset} "
                      f"{result['margin_pct']:>6.1f}% "
                      f"${result['capital_required']:>8.0f} "
                      f"{result['monthly_roi_pct']:>6.1f}%")

            # Cost breakdown for best platform
            best = find_best_platform_deep(known['sell'], known['source'], known['weight'])
            print(f"\n  Best platform: {best['platform']}")
            print(f"\n  Full cost breakdown:")
            print(f"    Sell price:          ${best['sell_price']:.2f}")
            print(f"    Source cost:         -${best['source_price']:.2f}")
            print(f"    Referral fee:        -${best['referral_fee']:.2f}")
            print(f"    Payment fee:         -${best['payment_fee']:.2f}")
            print(f"    FBA/fulfillment:     -${best['fba_fee']:.2f}")
            print(f"    Source shipping:     -${best['source_shipping']:.2f}")
            print(f"    Domestic shipping:   -${best['domestic_shipping']:.2f}")
            print(f"    Storage:             -${best['storage_cost']:.2f}")
            print(f"    Returns ({best['return_rate']*100:.0f}%):       -${best['return_cost']:.2f}")
            print(f"    Ad spend ({best['ad_spend_pct']*100:.0f}%):     -${best['ad_cost']:.2f}")
            print(f"    {'':>24} {'='*8}")
            print(f"    Net profit/unit:     ${best['net_profit']:.2f} ({best['margin_pct']:.1f}%)")
            print(f"\n  Monthly (30 units):    ${best['monthly_profit']:.2f}")
            print(f"  Capital required:      ${best['capital_required']:.2f}")
            print(f"  Monthly ROI:           {best['monthly_roi_pct']:.1f}%")
        else:
            print(f"\n  '{product_name}' not in known products database.")
            print(f"  Known products: {', '.join(sorted(KNOWN_PRODUCTS.keys())[:10])}...")

        # Get Google Trends for this product
        print(f"\n  Checking Google Trends...")
        trends = scan_google_trends([product_name], quiet=args.quiet)
        score = trends.get(product_name, 0)
        trajectory = trends.get(f"{product_name}_trajectory", 'unknown')
        print(f"    Trend score: {score}/100 ({trajectory})")

        return

    if args.bundles:
        print(f"\n{'='*60}")
        print(f"  BUNDLE ARBITRAGE OPPORTUNITIES")
        print(f"{'='*60}")

        bundles = find_bundle_opportunities(quiet=args.quiet)

        if bundles:
            print(f"\n  {'Bundle':<40} {'Price':>7} {'Profit':>7} {'Margin':>7} {'Savings':>8}")
            print(f"  {'-'*40} {'-'*7} {'-'*7} {'-'*7} {'-'*8}")

            for bundle in bundles[:15]:
                print(f"  {bundle['bundle_name']:<40} "
                      f"${bundle['bundle_price']:>5.2f} "
                      f"${bundle['bundle_profit']:>5.2f} "
                      f"{bundle['bundle_margin_pct']:>5.1f}% "
                      f"${bundle['savings_to_customer']:>6.2f}")

        return

    if args.seasonal:
        seasonal = get_seasonal_opportunities(quiet=args.quiet)
        if seasonal and not args.quiet:
            print(f"\n  {'Season':<20} {'Keyword':<20} {'Months':>6} {'Urgency':<8} {'Action'}")
            print(f"  {'-'*20} {'-'*20} {'-'*6} {'-'*8} {'-'*40}")
            for opp in seasonal:
                print(f"  {opp['season']:<20} {opp['keyword']:<20} "
                      f"{opp['months_until']:>6} {opp['urgency']:<8} {opp['action'][:40]}")
        return

    # Full scan
    if args.scan or args.trending:
        if not args.quiet:
            print(f"\n{'='*60}")
            print(f"  PRINTMAXX ECOM DEEP SCANNER")
            print(f"  Scanning: Amazon Movers | Reddit | Google Trends")
            print(f"{'='*60}")

        # 1. Amazon Movers & Shakers
        if not args.quiet:
            print(f"\n  [1/4] Scanning Amazon Movers & Shakers...")
        amazon_products = scan_amazon_movers(quiet=args.quiet)

        # 2. Reddit ecom communities
        if not args.quiet:
            print(f"\n  [2/4] Scanning Reddit ecom communities...")
        reddit_intel = scan_reddit_ecom(quiet=args.quiet)

        # 3. Google Trends for known products
        if not args.quiet:
            print(f"\n  [3/4] Checking Google Trends...")
        product_keywords = list(KNOWN_PRODUCTS.keys())[:20]
        trends_data = scan_google_trends(product_keywords, quiet=args.quiet)

        # 4. Seasonal front-running
        if not args.quiet:
            print(f"\n  [4/4] Checking seasonal opportunities...")
        seasonal = get_seasonal_opportunities(quiet=args.quiet)

        # Print consolidated report
        print_trending_report(amazon_products, reddit_intel, trends_data, quiet=args.quiet)

        # Build opportunities list for CSV output
        all_opportunities = []

        # From known products with trends
        for product, info in KNOWN_PRODUCTS.items():
            trend_score = trends_data.get(product, 50)
            best = find_best_platform_deep(info['sell'], info['source'], info['weight'])

            action = 'LIST' if best['net_profit'] > 5 and best['margin_pct'] > 20 else \
                     'WATCH' if best['net_profit'] > 0 else 'SKIP'

            all_opportunities.append({
                'timestamp': datetime.now().isoformat(),
                'product': product,
                'source_type': 'known_product',
                'category': info['category'],
                'sell_price': best['sell_price'],
                'source_price': best['source_price'],
                'net_profit': best['net_profit'],
                'margin_pct': best['margin_pct'],
                'platform': best['platform'],
                'trend_score': trend_score,
                'competition': 'medium',
                'capital_required': best['capital_required'],
                'edge_tactic': 'KNOWN_VALIDATED',
                'action': action,
                'monthly_profit_est': best['monthly_profit'],
                'notes': f"weight={info['weight']}, roi={best['monthly_roi_pct']:.0f}%/mo",
            })

        # From Amazon movers
        for product in amazon_products[:20]:
            all_opportunities.append({
                'timestamp': datetime.now().isoformat(),
                'product': product['title'][:60],
                'source_type': 'amazon_movers',
                'category': product['category'],
                'sell_price': product.get('price', 0),
                'source_price': 0,
                'net_profit': 0,
                'margin_pct': 0,
                'platform': 'Amazon',
                'trend_score': 0,
                'competition': 'unknown',
                'capital_required': 0,
                'edge_tactic': 'TRENDING_MOVER',
                'action': 'RESEARCH',
                'monthly_profit_est': 0,
                'notes': f"source=amazon_movers, category={product['category']}",
            })

        # Save to CSV
        if all_opportunities:
            output_path = save_opportunities(all_opportunities)
            if not args.quiet:
                list_count = sum(1 for o in all_opportunities if o['action'] == 'LIST')
                print(f"\n  Saved {len(all_opportunities)} opportunities to {output_path}")
                print(f"  LIST: {list_count} | WATCH: {sum(1 for o in all_opportunities if o['action'] == 'WATCH')} | "
                      f"RESEARCH: {sum(1 for o in all_opportunities if o['action'] == 'RESEARCH')}")

    # Log run
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(LOG_FILE, 'a') as f:
        f.write(f"{datetime.now().isoformat()} | mode={'scan' if args.scan else 'trending' if args.trending else 'other'} | "
                f"completed\n")


if __name__ == '__main__':
    main()
