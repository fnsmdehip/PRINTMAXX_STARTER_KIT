#!/usr/bin/env python3

from __future__ import annotations
"""
PRINTMAXX Trend Aggregator - Multi-Source Viral Trend Detection

First-principles approach: Detect what's trending → figure out what products/services
fit that trend → source cheaply → list at profit. Like quant trading but for ecom.

Sources:
  1. Google Trends (pytrends) - what people search for
  2. Reddit trending (r/shutupandtakemymoney, r/BuyItForLife, r/DidntKnowIWantedThat)
  3. TikTok trending hashtags (via web scrape)
  4. Amazon Movers & Shakers (price/rank changes)
  5. Product Hunt (new products = inspiration)
  6. Exploding Topics alternative (Google Trends rising queries)

Output: LEDGER/TREND_SIGNALS.csv

Usage:
    python3 trend_aggregator.py --scan           # Full multi-source scan
    python3 trend_aggregator.py --reddit          # Reddit product trends only
    python3 trend_aggregator.py --rising          # Google Trends rising queries
    python3 trend_aggregator.py --report          # Show latest signals
    python3 trend_aggregator.py --match           # Match trends to products we can source
    python3 trend_aggregator.py --hourly          # Cron mode
"""

import argparse
import csv
import json
import os
import random
import re
import sys
import time
from datetime import datetime
from pathlib import Path

try:
    import requests
except ImportError:
    print("Run: pip install requests")
    sys.exit(1)

try:
    from pytrends.request import TrendReq
    HAS_PYTRENDS = True
except ImportError:
    HAS_PYTRENDS = False

PROJECT_ROOT = Path(__file__).resolve().parent.parent
LEDGER_DIR = PROJECT_ROOT / "LEDGER"
OUTPUT_CSV = LEDGER_DIR / "TREND_SIGNALS.csv"
LOG_DIR = PROJECT_ROOT / "AUTOMATIONS" / "logs"

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
    'Accept': 'text/html,application/xhtml+xml',
}

# ============================================================
# SOURCE 1: GOOGLE TRENDS RISING QUERIES
# ============================================================

def get_rising_queries(seed_keywords=None):
    """Get rising/breakout queries from Google Trends."""
    if not HAS_PYTRENDS:
        print("  [!] pytrends not installed, skipping Google Trends")
        return []

    if seed_keywords is None:
        seed_keywords = [
            'trending products', 'viral product', 'tiktok made me buy',
            'amazon finds', 'best seller'
        ]

    pytrends = TrendReq(hl='en-US', tz=360)
    results = []

    for kw in seed_keywords:
        try:
            pytrends.build_payload([kw], timeframe='now 7-d', geo='US')
            related = pytrends.related_queries()
            if kw in related:
                rising = related[kw].get('rising')
                if rising is not None and not rising.empty:
                    for _, row in rising.head(10).iterrows():
                        results.append({
                            'source': 'google_trends_rising',
                            'signal': row['query'],
                            'strength': int(row['value']) if row['value'] != 'Breakout' else 1000,
                            'seed_keyword': kw,
                            'signal_type': 'rising_query',
                        })
            time.sleep(random.uniform(2, 4))
        except Exception as e:
            print(f"  [!] Trends error for '{kw}': {e}")
            time.sleep(5)

    return results

# ============================================================
# SOURCE 2: REDDIT PRODUCT TRENDS
# ============================================================

PRODUCT_SUBREDDITS = [
    ('shutupandtakemymoney', 'viral_product'),
    ('DidntKnowIWantedThat', 'impulse_buy'),
    ('BuyItForLife', 'quality_product'),
    ('coolguides', 'educational'),
    ('Entrepreneur', 'business_trend'),
    ('ecommerce', 'ecom_trend'),
    ('dropship', 'dropship_trend'),
    ('FulfillmentByAmazon', 'fba_trend'),
    ('AmazonSeller', 'amazon_trend'),
    ('tiktokgossip', 'tiktok_trend'),
]

def scan_reddit_trends(limit=15):
    """Scan product-oriented subreddits for trending items."""
    results = []

    for sub, signal_type in PRODUCT_SUBREDDITS:
        try:
            url = f"https://www.reddit.com/r/{sub}/hot.json?limit={limit}"
            resp = None
            for attempt in range(3):
                resp = requests.get(
                    url,
                    headers={'User-Agent': 'PRINTMAXX-TrendAgg/1.0'},
                    timeout=15,
                )
                if resp.status_code == 429:
                    wait = 2 ** (attempt + 1)
                    time.sleep(wait)
                    continue
                break

            if resp is not None and resp.status_code == 200:
                posts = resp.json().get('data', {}).get('children', [])
                for post in posts:
                    p = post.get('data', {})
                    score = p.get('ups', 0)
                    if score < 10:
                        continue  # Skip low-engagement posts

                    title = p.get('title', '')
                    results.append({
                        'source': f'reddit/r/{sub}',
                        'signal': title[:120],
                        'strength': min(score, 10000),
                        'seed_keyword': sub,
                        'signal_type': signal_type,
                        'url': f"https://reddit.com{p.get('permalink', '')}",
                        'comments': p.get('num_comments', 0),
                            'age_hours': round((time.time() - p.get('created_utc', 0)) / 3600, 1),
                        })

            time.sleep(random.uniform(1.5, 3.0))
        except Exception as e:
            print(f"  [!] Error r/{sub}: {e}")

    return results

# ============================================================
# SOURCE 3: PRODUCT HUNT (via RSS/JSON)
# ============================================================

def scan_product_hunt():
    """Get trending Product Hunt launches for inspiration."""
    results = []
    try:
        url = "https://www.producthunt.com/feed"
        resp = requests.get(url, headers=HEADERS, timeout=15)
        if resp.status_code == 200:
            # Extract product names from RSS feed
            titles = re.findall(r'<title><!\[CDATA\[(.*?)\]\]></title>', resp.text)
            for title in titles[:15]:
                if title and title != 'Product Hunt':
                    results.append({
                        'source': 'product_hunt',
                        'signal': title[:120],
                        'strength': 50,
                        'seed_keyword': 'product_hunt',
                        'signal_type': 'new_product',
                    })
    except Exception as e:
        print(f"  [!] Product Hunt error: {e}")

    return results

# ============================================================
# TREND → PRODUCT MATCHING
# ============================================================

def match_trend_to_products(signal_text):
    """First-principles: what products/services could serve this trend?"""
    matches = []
    text = signal_text.lower()

    # Product category matching
    category_keywords = {
        'health_wellness': ['health', 'wellness', 'vitamin', 'supplement', 'fitness',
                           'workout', 'exercise', 'therapy', 'massage', 'posture',
                           'sleep', 'meditation', 'mindfulness', 'cold plunge'],
        'beauty_skincare': ['skin', 'beauty', 'face', 'hair', 'glow', 'acne',
                           'wrinkle', 'serum', 'moisturizer', 'led mask'],
        'tech_gadget': ['tech', 'gadget', 'smart', 'wireless', 'bluetooth',
                       'ai', 'app', 'automation', 'robot', 'device'],
        'home_organization': ['home', 'kitchen', 'clean', 'organize', 'decor',
                             'storage', 'space', 'minimal', 'cozy'],
        'pet': ['dog', 'cat', 'pet', 'puppy', 'kitten', 'animal'],
        'productivity': ['productivity', 'work', 'focus', 'time', 'schedule',
                        'planner', 'journal', 'habit', 'goal'],
        'fashion_accessories': ['fashion', 'style', 'outfit', 'wear', 'jewelry',
                               'bag', 'shoe', 'sunglasses'],
    }

    for category, keywords in category_keywords.items():
        if any(kw in text for kw in keywords):
            matches.append(category)

    # Business opportunity matching
    biz_keywords = {
        'dropship_product': ['buy', 'purchase', 'amazon', 'cheap', 'deal', 'sale'],
        'digital_product': ['template', 'guide', 'course', 'ebook', 'download',
                           'printable', 'checklist', 'spreadsheet'],
        'service_opportunity': ['need help', 'looking for', 'anyone know', 'how to',
                               'recommendation', 'advice'],
        'content_opportunity': ['viral', 'trending', 'blew up', 'went viral',
                               'million views', 'followers'],
    }

    for biz_type, keywords in biz_keywords.items():
        if any(kw in text for kw in keywords):
            matches.append(biz_type)

    return matches if matches else ['general']

# ============================================================
# SCORING
# ============================================================

def score_signal(signal):
    """Score a trend signal 0-100."""
    score = 0

    strength = signal.get('strength', 0)
    if strength >= 1000: score += 30  # Breakout on Google Trends
    elif strength >= 500: score += 25
    elif strength >= 100: score += 20
    elif strength >= 50: score += 15
    elif strength >= 10: score += 10

    # Source reliability
    source = signal.get('source', '')
    if 'google_trends' in source: score += 20
    elif 'shutupandtakemymoney' in source: score += 15
    elif 'product_hunt' in source: score += 10
    elif 'reddit' in source: score += 10

    # Freshness
    age = signal.get('age_hours', 24)
    if age < 6: score += 20
    elif age < 12: score += 15
    elif age < 24: score += 10
    elif age < 48: score += 5

    # Product matchability
    matches = match_trend_to_products(signal.get('signal', ''))
    if len(matches) >= 2: score += 15
    elif len(matches) == 1: score += 10

    return min(score, 100)

# ============================================================
# OUTPUT
# ============================================================

def save_results(results):
    """Save to CSV."""
    LEDGER_DIR.mkdir(parents=True, exist_ok=True)

    for r in results:
        r['score'] = score_signal(r)
        r['timestamp'] = datetime.now().isoformat()
        r['product_matches'] = ','.join(match_trend_to_products(r.get('signal', '')))

    results.sort(key=lambda x: x.get('score', 0), reverse=True)

    fieldnames = [
        'timestamp', 'score', 'source', 'signal', 'strength', 'signal_type',
        'product_matches', 'seed_keyword', 'url', 'comments', 'age_hours'
    ]

    file_exists = OUTPUT_CSV.exists()
    with open(OUTPUT_CSV, 'a', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction='ignore')
        if not file_exists:
            writer.writeheader()
        for r in results:
            writer.writerow(r)

    return OUTPUT_CSV

def print_report(results=None):
    """Print formatted report."""
    if results is None:
        if not OUTPUT_CSV.exists():
            print("No data. Run --scan first.")
            return
        with open(OUTPUT_CSV, 'r') as f:
            results = list(csv.DictReader(f))

    hot = [r for r in results if int(r.get('score', 0)) >= 50]

    print(f"\n{'='*70}")
    print(f"  TREND AGGREGATOR — {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"  Total signals: {len(results)} | HOT (50+): {len(hot)}")
    print(f"{'='*70}")

    if hot:
        print(f"\n  TOP TREND SIGNALS:")
        print(f"  {'Score':>5} {'Source':<25} {'Type':<15} {'Signal':<50}")
        print(f"  {'-'*5} {'-'*25} {'-'*15} {'-'*50}")
        for r in hot[:20]:
            print(f"  {int(r['score']):>5} {r['source']:<25} {r.get('signal_type', ''):<15} "
                  f"{r['signal'][:50]}")

    # Group by product category
    category_counts = {}
    for r in results:
        for cat in r.get('product_matches', '').split(','):
            if cat:
                category_counts[cat] = category_counts.get(cat, 0) + 1

    if category_counts:
        print(f"\n  TRENDING CATEGORIES (opportunity heat map):")
        for cat, count in sorted(category_counts.items(), key=lambda x: x[1], reverse=True)[:10]:
            bar = '█' * min(count, 30)
            print(f"    {cat:<25} {count:>3} signals {bar}")

    print(f"\n  FIRST-PRINCIPLES ACTION:")
    print(f"  1. Top category → source products on AliExpress at $2-15")
    print(f"  2. List on FB Marketplace/eBay at 3x markup")
    print(f"  3. Create content around trend → drive traffic to listings")
    print(f"  4. If trend sustained 7+ days → build dedicated store")
    print(f"\n  Output: {OUTPUT_CSV}")

# ============================================================
# MAIN
# ============================================================

def main():
    parser = argparse.ArgumentParser(description='PRINTMAXX Trend Aggregator')
    parser.add_argument('--scan', action='store_true', help='Full multi-source scan')
    parser.add_argument('--reddit', action='store_true', help='Reddit only')
    parser.add_argument('--rising', action='store_true', help='Google Trends rising only')
    parser.add_argument('--report', action='store_true', help='Show report')
    parser.add_argument('--match', action='store_true', help='Match trends to products')
    parser.add_argument('--hourly', action='store_true', help='Cron mode')
    args = parser.parse_args()

    # Default behavior for cron/manual runs with no source flag: run full scan.
    if not any([args.scan, args.reddit, args.rising, args.report, args.match, args.hourly]):
        args.scan = True
    if args.hourly and not any([args.scan, args.reddit, args.rising]):
        args.scan = True

    if args.report:
        print_report()
        return

    quiet = args.hourly
    all_signals = []

    if not quiet:
        print(f"\n{'='*60}")
        print(f"  PRINTMAXX TREND AGGREGATOR")
        print(f"  Multi-source viral trend detection")
        print(f"{'='*60}\n")

    # Source 1: Google Trends Rising
    if args.scan or args.rising:
        if not quiet:
            print("  [1/3] Google Trends rising queries...")
        rising = get_rising_queries()
        all_signals.extend(rising)
        if not quiet:
            print(f"    Found {len(rising)} rising queries")

    # Source 2: Reddit Product Trends
    if args.scan or args.reddit:
        if not quiet:
            print("  [2/3] Reddit product subreddits...")
        reddit = scan_reddit_trends()
        all_signals.extend(reddit)
        if not quiet:
            print(f"    Found {len(reddit)} product signals")

    # Source 3: Product Hunt
    if args.scan:
        if not quiet:
            print("  [3/3] Product Hunt feed...")
        ph = scan_product_hunt()
        all_signals.extend(ph)
        if not quiet:
            print(f"    Found {len(ph)} new products")

    if not quiet:
        print(f"\n  Total signals: {len(all_signals)}")

    if all_signals:
        save_results(all_signals)
        if not quiet:
            print_report(all_signals)

    # Log
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    with open(LOG_DIR / f"trend_agg_{datetime.now().strftime('%Y-%m-%d')}.log", 'a') as f:
        f.write(f"{datetime.now().isoformat()} | signals: {len(all_signals)} | "
                f"hot: {len([s for s in all_signals if s.get('score', 0) >= 50])}\n")

if __name__ == '__main__':
    main()
