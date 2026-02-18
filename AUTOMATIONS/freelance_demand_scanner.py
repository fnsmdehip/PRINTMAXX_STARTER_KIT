#!/usr/bin/env python3
"""
PRINTMAXX Freelance Demand Scanner

Scans freelance platforms for ACTIVE requests/jobs people are hiring for,
then matches them to services we can deliver with AI in minutes.

Strategy: Find the demand FIRST, build the deliverable, respond with a sample.

Sources:
  - Reddit (r/forhire, r/slavelabour, r/freelance, r/graphic_design, r/web_design)
  - Fiverr buyer requests (via scraping)
  - Upwork job feed (via RSS/API)

Output: LEDGER/FREELANCE_DEMAND_SCAN.csv

Usage:
    python3 freelance_demand_scanner.py --scan          # Full scan all sources
    python3 freelance_demand_scanner.py --reddit         # Reddit only
    python3 freelance_demand_scanner.py --report         # Show latest matches
    python3 freelance_demand_scanner.py --hourly         # Cron mode
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

try:
    import requests
except ImportError:
    print("Run: pip install requests")
    sys.exit(1)

PROJECT_ROOT = Path(__file__).resolve().parent.parent
LEDGER_DIR = PROJECT_ROOT / "LEDGER"
OUTPUT_CSV = LEDGER_DIR / "FREELANCE_DEMAND_SCAN.csv"
LOG_DIR = PROJECT_ROOT / "AUTOMATIONS" / "logs"

# ============================================================
# SERVICES WE CAN DELIVER WITH AI (match against demand)
# ============================================================

AI_DELIVERABLE_SERVICES = {
    'website': {
        'keywords': ['website', 'landing page', 'web design', 'wordpress', 'shopify',
                     'wix', 'squarespace', 'portfolio site', 'business website',
                     'ecommerce site', 'web developer', 'frontend'],
        'delivery_time': '2-4 hours',
        'our_cost': 0,
        'typical_price': (100, 500),
        'tools': 'Lovable/Bolt/v0 + custom CSS',
        'sample_type': 'Live preview URL'
    },
    'logo': {
        'keywords': ['logo', 'brand identity', 'branding', 'logo design', 'brand design',
                     'company logo', 'mascot', 'icon design'],
        'delivery_time': '30 min',
        'our_cost': 0,
        'typical_price': (25, 150),
        'tools': 'Midjourney/DALL-E/Ideogram',
        'sample_type': '3 logo concepts PNG'
    },
    'copywriting': {
        'keywords': ['copywriting', 'sales copy', 'product description', 'email copy',
                     'ad copy', 'website copy', 'blog post', 'article writing',
                     'content writing', 'SEO content', 'ghostwriting'],
        'delivery_time': '1 hour',
        'our_cost': 0,
        'typical_price': (30, 200),
        'tools': 'Claude/GPT + human editing',
        'sample_type': 'First 500 words free'
    },
    'social_media': {
        'keywords': ['social media', 'instagram', 'tiktok', 'twitter management',
                     'social media manager', 'content calendar', 'social posts',
                     'social media marketing', 'smm'],
        'delivery_time': '2 hours',
        'our_cost': 0,
        'typical_price': (100, 500),
        'tools': 'Claude + Canva + Buffer',
        'sample_type': '7-day content calendar + 5 sample posts'
    },
    'video_editing': {
        'keywords': ['video edit', 'youtube edit', 'tiktok edit', 'reels',
                     'video editor', 'short form', 'podcast clip', 'clipping'],
        'delivery_time': '1-2 hours',
        'our_cost': 0,
        'typical_price': (25, 100),
        'tools': 'CapCut/DaVinci + AI captions',
        'sample_type': '30-sec sample clip'
    },
    'data_entry': {
        'keywords': ['data entry', 'spreadsheet', 'excel', 'google sheets',
                     'data scraping', 'web scraping', 'lead generation', 'research',
                     'data collection', 'virtual assistant'],
        'delivery_time': '1-3 hours',
        'our_cost': 0,
        'typical_price': (20, 100),
        'tools': 'Python + Claude for analysis',
        'sample_type': 'First 50 entries free'
    },
    'cold_email': {
        'keywords': ['cold email', 'email outreach', 'lead gen', 'b2b leads',
                     'email campaign', 'drip campaign', 'email sequence',
                     'outbound', 'prospecting'],
        'delivery_time': '2 hours',
        'our_cost': 0,
        'typical_price': (50, 300),
        'tools': 'Claude + our templates',
        'sample_type': '3-email sequence sample'
    },
    'seo': {
        'keywords': ['SEO', 'keyword research', 'backlinks', 'on-page SEO',
                     'technical SEO', 'SEO audit', 'rank', 'google ranking'],
        'delivery_time': '2-4 hours',
        'our_cost': 0,
        'typical_price': (50, 300),
        'tools': 'Ahrefs free + Claude analysis',
        'sample_type': 'Free SEO audit report'
    },
    'automation': {
        'keywords': ['automation', 'zapier', 'n8n', 'make.com', 'workflow',
                     'api integration', 'bot', 'script', 'automate'],
        'delivery_time': '2-6 hours',
        'our_cost': 0,
        'typical_price': (100, 500),
        'tools': 'Python/n8n/Zapier',
        'sample_type': 'Architecture diagram + demo'
    },
    'presentation': {
        'keywords': ['presentation', 'pitch deck', 'powerpoint', 'slides',
                     'google slides', 'keynote', 'investor deck'],
        'delivery_time': '2 hours',
        'our_cost': 0,
        'typical_price': (50, 200),
        'tools': 'Claude + Canva/Google Slides',
        'sample_type': 'First 5 slides free'
    },
}

# ============================================================
# REDDIT SCANNER
# ============================================================

HIRING_SUBREDDITS = [
    'forhire',          # Main freelance hiring
    'slavelabour',      # Budget freelance tasks
    'freelance',        # Freelance discussion + hiring
    'graphic_design',   # Design jobs
    'web_design',       # Web design jobs
    'DesignJobs',       # Design specific
    'hiring',           # General hiring
    'remotejs',         # JS/web dev jobs
    'webdev',           # Web dev discussion
]

def scan_reddit_hiring(subreddit, limit=25):
    """Scan a subreddit for hiring posts using Reddit JSON API."""
    results = []
    url = f"https://www.reddit.com/r/{subreddit}/new.json?limit={limit}"
    headers = {'User-Agent': 'PRINTMAXX-Scanner/1.0 (research purposes)'}

    try:
        resp = requests.get(url, headers=headers, timeout=15)
        if resp.status_code == 200:
            data = resp.json()
            posts = data.get('data', {}).get('children', [])

            for post in posts:
                p = post.get('data', {})
                title = p.get('title', '').lower()
                body = p.get('selftext', '').lower()
                flair = (p.get('link_flair_text') or '').lower()

                # Filter for hiring posts
                is_hiring = any(kw in title or kw in flair for kw in
                               ['hiring', '[hiring]', 'looking for', 'need',
                                'want', 'searching for', 'help needed', 'job'])

                # Skip if poster is looking FOR work (not hiring)
                is_seeking = any(kw in title for kw in
                                ['for hire', '[for hire]', 'available',
                                 'offering', 'i will', 'i can'])

                if is_hiring and not is_seeking:
                    # Match against our services
                    full_text = f"{title} {body}"
                    matched_services = []
                    for service_key, service in AI_DELIVERABLE_SERVICES.items():
                        if any(kw in full_text for kw in service['keywords']):
                            matched_services.append(service_key)

                    if matched_services:
                        # Extract budget if mentioned
                        budget_match = re.search(r'\$(\d+)', f"{title} {body}")
                        budget = int(budget_match.group(1)) if budget_match else None

                        results.append({
                            'source': f'r/{subreddit}',
                            'title': p.get('title', '')[:100],
                            'url': f"https://reddit.com{p.get('permalink', '')}",
                            'author': p.get('author', ''),
                            'budget': budget,
                            'matched_services': ','.join(matched_services),
                            'upvotes': p.get('ups', 0),
                            'comments': p.get('num_comments', 0),
                            'age_hours': round((time.time() - p.get('created_utc', 0)) / 3600, 1),
                            'body_preview': body[:200] if body else '',
                        })

        time.sleep(random.uniform(1.5, 3.0))
    except Exception as e:
        print(f"  [!] Error scanning r/{subreddit}: {e}")

    return results

def scan_all_reddit():
    """Scan all hiring subreddits."""
    all_results = []
    for sub in HIRING_SUBREDDITS:
        print(f"  Scanning r/{sub}...", end=' ')
        results = scan_reddit_hiring(sub)
        print(f"{len(results)} matches")
        all_results.extend(results)
    return all_results

# ============================================================
# SCORING & RANKING
# ============================================================

def score_opportunity(opp):
    """Score an opportunity 0-100 based on profitability and ease."""
    score = 0

    # Budget score (higher budget = better)
    budget = opp.get('budget')
    if budget:
        if budget >= 200: score += 30
        elif budget >= 100: score += 25
        elif budget >= 50: score += 20
        elif budget >= 20: score += 10

    # Freshness (newer = better, respond fast)
    age = opp.get('age_hours', 999)
    if age < 2: score += 25
    elif age < 6: score += 20
    elif age < 12: score += 15
    elif age < 24: score += 10
    elif age < 48: score += 5

    # Service match quality
    services = opp.get('matched_services', '').split(',')
    if len(services) >= 2: score += 15  # Multiple matches = flexible
    elif len(services) == 1: score += 10

    # Engagement (more comments might mean more competition, but also real demand)
    comments = opp.get('comments', 0)
    if comments < 3: score += 15  # Low competition
    elif comments < 10: score += 10
    elif comments < 20: score += 5

    # Upvotes (visibility/legitimacy)
    upvotes = opp.get('upvotes', 0)
    if upvotes >= 5: score += 10
    elif upvotes >= 2: score += 5

    # Cap at 100
    return min(score, 100)

# ============================================================
# OUTPUT
# ============================================================

def save_results(results):
    """Save to CSV."""
    LEDGER_DIR.mkdir(parents=True, exist_ok=True)

    # Score each opportunity
    for r in results:
        r['score'] = score_opportunity(r)
        r['timestamp'] = datetime.now().isoformat()

        # Add service details
        services = r.get('matched_services', '').split(',')
        if services:
            primary = services[0]
            svc = AI_DELIVERABLE_SERVICES.get(primary, {})
            r['delivery_time'] = svc.get('delivery_time', 'TBD')
            r['our_cost'] = svc.get('our_cost', 0)
            r['typical_price_low'] = svc.get('typical_price', (0, 0))[0]
            r['typical_price_high'] = svc.get('typical_price', (0, 0))[1]
            r['tools_needed'] = svc.get('tools', '')
            r['sample_type'] = svc.get('sample_type', '')

    # Sort by score
    results.sort(key=lambda x: x.get('score', 0), reverse=True)

    fieldnames = [
        'timestamp', 'score', 'source', 'title', 'url', 'author', 'budget',
        'matched_services', 'delivery_time', 'our_cost', 'typical_price_low',
        'typical_price_high', 'tools_needed', 'sample_type', 'upvotes',
        'comments', 'age_hours', 'body_preview'
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
            print("No scan data. Run --scan first.")
            return
        with open(OUTPUT_CSV, 'r') as f:
            results = list(csv.DictReader(f))

    hot = [r for r in results if int(r.get('score', 0)) >= 50]
    warm = [r for r in results if 30 <= int(r.get('score', 0)) < 50]

    print(f"\n{'='*70}")
    print(f"  FREELANCE DEMAND SCAN — {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"  Total: {len(results)} | HOT (50+): {len(hot)} | WARM (30-49): {len(warm)}")
    print(f"{'='*70}")

    if hot:
        print(f"\n  HOT OPPORTUNITIES (respond NOW):")
        print(f"  {'Score':>5} {'Source':<15} {'Services':<20} {'Budget':>8} {'Age':>6} {'Title':<50}")
        print(f"  {'-'*5} {'-'*15} {'-'*20} {'-'*8} {'-'*6} {'-'*50}")
        for r in hot[:15]:
            budget_str = f"${r['budget']}" if r.get('budget') else 'N/A'
            age_str = f"{float(r.get('age_hours', 0)):.0f}h"
            print(f"  {int(r['score']):>5} {r['source']:<15} {r['matched_services']:<20} "
                  f"{budget_str:>8} {age_str:>6} {r['title'][:50]}")

    if warm:
        print(f"\n  WARM OPPORTUNITIES:")
        for r in warm[:10]:
            print(f"  [{int(r['score'])}] {r['source']}: {r['title'][:60]}")

    if hot:
        print(f"\n  RESPONSE STRATEGY:")
        print(f"  1. Click URL → read full post")
        print(f"  2. Build sample deliverable with AI (30-60 min)")
        print(f"  3. Reply with: sample + price quote + timeline")
        print(f"  4. Follow up via DM with portfolio link")

    print(f"\n  Output: {OUTPUT_CSV}")

# ============================================================
# MAIN
# ============================================================

def main():
    parser = argparse.ArgumentParser(description='PRINTMAXX Freelance Demand Scanner')
    parser.add_argument('--scan', action='store_true', help='Full scan')
    parser.add_argument('--reddit', action='store_true', help='Reddit only')
    parser.add_argument('--report', action='store_true', help='Show report')
    parser.add_argument('--hourly', action='store_true', help='Cron mode')
    args = parser.parse_args()

    if args.report:
        print_report()
        return

    quiet = args.hourly

    if not quiet:
        print(f"\n{'='*60}")
        print(f"  PRINTMAXX FREELANCE DEMAND SCANNER")
        print(f"  Scanning {len(HIRING_SUBREDDITS)} subreddits for active hiring posts")
        print(f"  Matching against {len(AI_DELIVERABLE_SERVICES)} AI-deliverable services")
        print(f"{'='*60}\n")

    all_results = []

    # Reddit scan
    if not quiet:
        print("  [REDDIT] Scanning hiring subreddits...")
    reddit_results = scan_all_reddit()
    all_results.extend(reddit_results)

    if not quiet:
        print(f"\n  Total matches found: {len(all_results)}")

    if all_results:
        output_path = save_results(all_results)
        if not quiet:
            print_report(all_results)
    else:
        if not quiet:
            print("\n  No matching opportunities found this scan.")

    # Log
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    log_file = LOG_DIR / f"freelance_demand_{datetime.now().strftime('%Y-%m-%d')}.log"
    with open(log_file, 'a') as f:
        f.write(f"{datetime.now().isoformat()} | scanned: {len(all_results)} | "
                f"hot: {len([r for r in all_results if r.get('score', 0) >= 50])}\n")

if __name__ == '__main__':
    main()
