#!/usr/bin/env python3
"""
Reddit Deep Scraper - Quant-level alpha extraction from ALL 41 subreddits
Uses Reddit's JSON API (no auth, no browser, no anti-bot issues).

What this actually does (not stubs):
- Scrapes top posts (week/month) from ALL 41 subreddits in RESEARCH_SUBREDDITS.csv
- Scrapes top comments on high-engagement posts (real reply data)
- Extracts specific numbers ($revenue, %growth, Nx multipliers)
- Detects funnels in comments (people pitching tools/services)
- Categorizes by method (APP_FACTORY, COLD_OUTBOUND, etc.)
- Estimates ROI with engagement-weighted scoring
- Flags suspicious engagement / inflated earnings
- Appends to ALPHA_STAGING.csv (never overwrites)
- Full JSON backup with comments and engagement

Usage:
    python3 reddit_deep_scraper.py                    # All 41 subreddits, top week
    python3 reddit_deep_scraper.py --daily             # Daily scrape: top/day (freshest signal)
    python3 reddit_deep_scraper.py --full-scan         # Multi-timeframe: day + month + year with staleness detection
    python3 reddit_deep_scraper.py --time month        # Top month
    python3 reddit_deep_scraper.py --limit 10          # Only top 10 subreddits
    python3 reddit_deep_scraper.py --deep              # Also scrape top comments on hot posts
    python3 reddit_deep_scraper.py --sub SideProject   # Single subreddit
    python3 reddit_deep_scraper.py --all-time          # Top all-time (for initial seed)

    # Recommended daily:
    python3 reddit_deep_scraper.py --daily --deep

    # Recommended weekly deep scan:
    python3 reddit_deep_scraper.py --full-scan --deep

    # Background:
    nohup python3 reddit_deep_scraper.py --daily --deep > /tmp/reddit_scrape.log 2>&1 &
"""

import csv
import json
import re
import time
import requests
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional
import argparse

# Paths
PROJECT_DIR = Path("/Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt")
LEDGER_DIR = PROJECT_DIR / "LEDGER"
ALPHA_STAGING = LEDGER_DIR / "ALPHA_STAGING.csv"
SUBREDDIT_CSV = LEDGER_DIR / "RESEARCH_SUBREDDITS.csv"
OUTPUT_DIR = PROJECT_DIR / "AUTOMATIONS" / "reddit_scraper_output"
OUTPUT_DIR.mkdir(exist_ok=True)

HEADERS = {'User-Agent': 'PRINTMAXX-AlphaBot/2.0 (research; contact: printmaxxer@proton.me)'}

# Rate limiting: Reddit allows ~60 requests/min for unauthenticated
REQUEST_DELAY = 1.2  # seconds between requests


def load_subreddits(limit=None, single_sub=None):
    """Load subreddits from CSV. Returns list of dicts."""
    if single_sub:
        return [{'subreddit_name': f"r/{single_sub.replace('r/', '')}", 'signal_quality': 'HIGH', 'category': 'CUSTOM', 'focus_area': 'custom'}]

    subs = []
    with open(SUBREDDIT_CSV, 'r', encoding='utf-8') as f:
        for row in csv.DictReader(f):
            if row.get('auto_monitor') == 'TRUE':
                subs.append(row)

    # Sort: HIGHEST first
    quality_order = {'HIGHEST': 0, 'HIGH': 1, 'MEDIUM': 2, 'LOW': 3}
    subs.sort(key=lambda x: quality_order.get(x.get('signal_quality', 'MEDIUM'), 2))

    if limit:
        subs = subs[:limit]

    return subs


def fetch_reddit_json(url, retries=3):
    """Fetch JSON from Reddit API with retry and rate limiting."""
    for attempt in range(retries):
        try:
            resp = requests.get(url, headers=HEADERS, timeout=15)
            if resp.status_code == 200:
                time.sleep(REQUEST_DELAY)
                return resp.json()
            elif resp.status_code == 429:
                wait = int(resp.headers.get('Retry-After', 60))
                print(f"    Rate limited. Waiting {wait}s...")
                time.sleep(wait)
            elif resp.status_code == 403:
                print(f"    403 Forbidden (subreddit may be private)")
                return None
            elif resp.status_code == 404:
                print(f"    404 Not Found")
                return None
            else:
                print(f"    HTTP {resp.status_code}, retry {attempt+1}/{retries}")
                time.sleep(5)
        except requests.exceptions.Timeout:
            print(f"    Timeout, retry {attempt+1}/{retries}")
            time.sleep(3)
        except Exception as e:
            print(f"    Error: {str(e)[:60]}, retry {attempt+1}/{retries}")
            time.sleep(3)
    return None


def scrape_subreddit_posts(sub_name, time_filter='week', post_limit=25):
    """Scrape top posts from a subreddit using JSON API."""
    clean_name = sub_name.replace('r/', '')
    url = f"https://www.reddit.com/r/{clean_name}/top.json?t={time_filter}&limit={post_limit}&raw_json=1"

    data = fetch_reddit_json(url)
    if not data or 'data' not in data:
        return []

    posts = []
    for child in data['data']['children']:
        post = child['data']
        posts.append({
            'post_id': post.get('id', ''),
            'title': post.get('title', ''),
            'selftext': post.get('selftext', '')[:2000],  # Cap at 2K chars
            'url': f"https://reddit.com{post.get('permalink', '')}",
            'external_url': post.get('url', ''),
            'score': post.get('score', 0),
            'upvote_ratio': post.get('upvote_ratio', 0),
            'num_comments': post.get('num_comments', 0),
            'created_utc': post.get('created_utc', 0),
            'author': post.get('author', '[deleted]'),
            'subreddit': clean_name,
            'is_self': post.get('is_self', True),
            'link_flair_text': post.get('link_flair_text', ''),
        })

    return posts


def scrape_post_comments(permalink, depth=2, comment_limit=10):
    """Scrape top comments from a specific post."""
    # Reddit JSON API: append .json to permalink
    url = f"https://www.reddit.com{permalink}.json?sort=top&limit={comment_limit}&depth={depth}&raw_json=1"

    data = fetch_reddit_json(url)
    if not data or len(data) < 2:
        return []

    comments = []

    def extract_comments(children, current_depth=1):
        if current_depth > depth:
            return
        for child in children:
            if child.get('kind') != 't1':
                continue
            c = child['data']
            body = c.get('body', '')
            if not body or body == '[deleted]' or body == '[removed]':
                continue

            comments.append({
                'comment_id': c.get('id', ''),
                'body': body[:1000],
                'score': c.get('score', 0),
                'author': c.get('author', '[deleted]'),
                'depth': current_depth,
                'has_link': bool(re.search(r'https?://', body)),
                'has_pitch': bool(re.search(r'(?i)(check out|sign up|my tool|i built|try it|discount|coupon|dm me)', body)),
                'has_numbers': bool(re.search(r'\$[\d,]+|\d+%|\d+x|\d+k\b', body, re.I)),
            })

            # Recurse into replies
            replies = c.get('replies', '')
            if replies and isinstance(replies, dict):
                reply_children = replies.get('data', {}).get('children', [])
                extract_comments(reply_children, current_depth + 1)

    comment_data = data[1].get('data', {}).get('children', [])
    extract_comments(comment_data)

    return comments


def extract_numbers(text):
    """Extract specific numbers from text (revenue, percentages, multipliers)."""
    numbers = {
        'dollar_amounts': re.findall(r'\$[\d,]+(?:\.\d+)?[kKmM]?', text),
        'percentages': re.findall(r'\d+(?:\.\d+)?%', text),
        'multipliers': re.findall(r'\d+(?:\.\d+)?[xX]\b', text),
        'mrr_arr': re.findall(r'(?i)(?:mrr|arr)[:\s]*\$?[\d,]+[kKmM]?', text),
        'user_counts': re.findall(r'(?i)(?:\d+[kKmM]?\+?\s*(?:users|customers|subscribers|signups|downloads|installs))', text),
        'time_frames': re.findall(r'(?i)(?:in\s+)?(\d+\s*(?:days?|weeks?|months?|hours?))', text),
    }
    return {k: v for k, v in numbers.items() if v}


def check_staleness(post, time_filter):
    """Detect if insights from older posts may be expired/outdated.

    For month/year/all-time posts, checks if advice references tools,
    platforms, or strategies known to have changed since the post date.
    """
    if time_filter == 'day':
        return 'FRESH'
    if time_filter == 'week':
        return 'RECENT'

    text = (post.get('title', '') + ' ' + post.get('selftext', '')).lower()
    created = post.get('created_utc', 0)
    post_age_days = (time.time() - created) / 86400 if created else 999

    stale_signals = []

    # Platform/tool changes that make old advice stale
    stale_markers = {
        'heroku free': 'Heroku killed free tier Nov 2022',
        'twitter api free': 'Twitter API paywalled Feb 2023',
        'gpt-3.5': 'GPT-4o and Claude 4.5 are current',
        'gpt-4 turbo': 'GPT-4o replaced GPT-4 Turbo',
        'notion ai free': 'Notion AI now paid add-on',
        'facebook organic': 'FB organic reach near zero 2024+',
        'instagram reels bonus': 'IG Reels bonus program ended 2023',
        'tiktok creator fund': 'TikTok Creator Fund replaced by Creativity Program',
        'youtube shorts fund': 'YT Shorts Fund ended, now revenue sharing',
        'stripe atlas': 'Stripe Atlas pricing changed multiple times',
        'product hunt launch': 'PH algorithm changed significantly 2024-2025',
        'jasper ai': 'Jasper AI lost market share to Claude/ChatGPT',
        'copy.ai': 'Copy.ai pivoted, less relevant for content',
        'dalle-2': 'DALL-E 3 and Midjourney v6 are current',
        'midjourney v4': 'Midjourney v6+ is current',
        'chatgpt plugin': 'ChatGPT Plugins replaced by GPTs/Actions',
        'google bard': 'Bard renamed to Gemini',
        'bing chat': 'Bing Chat renamed to Copilot',
    }

    for marker, reason in stale_markers.items():
        if marker in text:
            stale_signals.append(reason)

    # Price/fee references older than 6 months are suspect
    if post_age_days > 180 and ('pricing' in text or 'fee' in text or '$' in text):
        stale_signals.append(f'Post is {int(post_age_days)}d old, pricing may have changed')

    # Algorithm advice older than 3 months
    if post_age_days > 90 and any(w in text for w in ['algorithm', 'algo ', 'reach', 'impressions', 'engagement rate']):
        stale_signals.append(f'Algorithm advice from {int(post_age_days)}d ago may be outdated')

    # API/integration advice older than 6 months
    if post_age_days > 180 and any(w in text for w in ['api', 'integration', 'webhook', 'endpoint']):
        stale_signals.append(f'API/integration details from {int(post_age_days)}d ago may have changed')

    if not stale_signals:
        if post_age_days < 30:
            return 'FRESH'
        elif post_age_days < 90:
            return 'RECENT'
        elif post_age_days < 180:
            return 'AGING'
        else:
            return 'VERIFY'

    return f"STALE: {'; '.join(stale_signals[:2])}"


def categorize_post(title, selftext):
    """Categorize post by method type."""
    text = (title + ' ' + selftext).lower()
    cats = [
        (['cold email', 'outbound', 'deliverability', 'smtp', 'email list', 'b2b email'], 'COLD_OUTBOUND'),
        (['app store', 'ios app', 'android app', 'mobile app', 'react native', 'flutter', 'aso'], 'APP_FACTORY'),
        (['mcp', 'claude', 'chatgpt', 'gpt', 'llm', 'ai agent', 'automation', 'cursor'], 'TOOL_ALPHA'),
        (['tiktok', 'reels', 'youtube', 'shorts', 'content', 'faceless', 'viral video'], 'CONTENT_FARM'),
        (['saas', 'mrr', 'arr', 'subscription', 'churn', 'b2b saas', 'micro saas'], 'SAAS'),
        (['seo', 'google', 'ranking', 'organic', 'backlink', 'serp', 'keyword'], 'SEO_GEO'),
        (['revenue', 'pricing', 'monetiz', 'paywall', 'freemium', 'conversion'], 'MONETIZATION'),
        (['growth', 'viral', 'distribution', 'launch', 'product hunt', 'beta'], 'GROWTH_HACK'),
        (['ecom', 'dropship', 'amazon', 'etsy', 'shopify', 'fba', 'print on demand'], 'ECOM_ARB'),
        (['affiliate', 'commission', 'referral', 'partner program'], 'AFFILIATE'),
        (['newsletter', 'beehiiv', 'substack', 'email list', 'subscriber'], 'NEWSLETTER'),
        (['freelanc', 'client', 'agency', 'consulting', 'service'], 'SERVICES'),
        (['scraping', 'api', 'data', 'automation', 'script', 'bot'], 'AUTOMATION'),
        (['design', 'figma', 'ui', 'ux', 'template', 'notion'], 'DIGITAL_PRODUCTS'),
    ]
    for keywords, cat in cats:
        if any(kw in text for kw in keywords):
            return cat
    return 'ALPHA_GENERAL'


def estimate_roi(post, numbers_found):
    """Estimate ROI potential based on post signals."""
    score = 0

    # Engagement signals
    if post['score'] > 500: score += 3
    elif post['score'] > 100: score += 2
    elif post['score'] > 25: score += 1

    if post['num_comments'] > 100: score += 2
    elif post['num_comments'] > 30: score += 1

    # Content quality signals
    if numbers_found.get('dollar_amounts'): score += 3
    if numbers_found.get('mrr_arr'): score += 3
    if numbers_found.get('percentages'): score += 2
    if numbers_found.get('multipliers'): score += 2
    if numbers_found.get('user_counts'): score += 2
    if numbers_found.get('time_frames'): score += 1

    # Actionability signals
    text = (post['title'] + ' ' + post['selftext']).lower()
    if re.search(r'(?:step|how|guide|tutorial|framework|playbook|method)', text): score += 2
    if re.search(r'(?:i built|i made|i launched|my results|case study)', text): score += 2
    if post.get('is_self') and len(post.get('selftext', '')) > 500: score += 1  # Long self-posts = more detail

    if score >= 10: return 'HIGHEST'
    if score >= 6: return 'HIGH'
    if score >= 3: return 'MEDIUM'
    return 'LOW'


def check_engagement_authenticity(post):
    """Flag suspicious engagement patterns."""
    score = post.get('score', 0)
    comments = post.get('num_comments', 0)
    ratio = post.get('upvote_ratio', 0)

    # Very high score but almost no comments = suspicious
    if score > 500 and comments < 5:
        return 'SUSPICIOUS'
    # Low upvote ratio on high-score post = controversial or manipulated
    if score > 200 and ratio < 0.7:
        return 'CONTROVERSIAL'
    # Normal
    return 'AUTHENTIC'


def check_earnings_claims(text):
    """Check if earnings claims are verifiable."""
    has_earnings = bool(re.search(r'(?i)(?:made|earned|revenue|income|profit)\s*\$[\d,]+', text))
    if not has_earnings:
        return 'N/A'

    # Round numbers are more likely inflated
    amounts = re.findall(r'\$([\d,]+)', text)
    for amt in amounts:
        clean = amt.replace(',', '')
        if clean and int(clean) > 0:
            if int(clean) % 1000 == 0 and int(clean) >= 10000:
                return 'LIKELY_INFLATED'

    # Has screenshot reference = slightly more credible
    if re.search(r'(?i)(screenshot|proof|dashboard|stripe|analytics)', text):
        return 'SCREENSHOT_CLAIMED'

    return 'UNVERIFIED'


def build_alpha_entry(post, comments=None, sub_info=None, time_filter='week'):
    """Build a full alpha entry from a post and its comments."""
    full_text = post['title'] + '\n' + post.get('selftext', '')
    numbers = extract_numbers(full_text)
    category = categorize_post(post['title'], post.get('selftext', ''))
    roi = estimate_roi(post, numbers)
    authenticity = check_engagement_authenticity(post)
    freshness = check_staleness(post, time_filter)
    earnings = check_earnings_claims(full_text)

    # Build engagement summary
    engagement = f"score={post['score']} comments={post['num_comments']} ratio={post.get('upvote_ratio', 0):.0%}"

    # Numbers summary
    num_summary = ""
    if numbers:
        parts = []
        for k, v in numbers.items():
            parts.append(f"{k}: {', '.join(v[:3])}")
        num_summary = " | NUMBERS: " + '; '.join(parts)

    # Comment insights
    comment_summary = ""
    if comments:
        funnel_comments = [c for c in comments if c.get('has_pitch')]
        number_comments = [c for c in comments if c.get('has_numbers')]
        top_comments = sorted(comments, key=lambda c: c.get('score', 0), reverse=True)[:3]

        parts = [f"{len(comments)} comments scraped"]
        if funnel_comments:
            parts.append(f"{len(funnel_comments)} pitches/funnels")
        if number_comments:
            parts.append(f"{len(number_comments)} with specific numbers")

        comment_summary = " | COMMENTS: " + ', '.join(parts)

        # Add top comment excerpts
        if top_comments:
            excerpts = [f"[{c['score']}pts] {c['body'][:120]}" for c in top_comments]
            comment_summary += " | TOP: " + " /// ".join(excerpts)

    # Build tactic text (title + key selftext)
    tactic = post['title']
    if post.get('selftext'):
        # Get first substantive paragraph
        paragraphs = [p.strip() for p in post['selftext'].split('\n') if p.strip() and len(p.strip()) > 30]
        if paragraphs:
            tactic += ' | ' + paragraphs[0][:300]

    return {
        'source': f"r/{post['subreddit']}",
        'source_url': post['url'],
        'tactic': tactic[:500],
        'category': category,
        'roi_potential': roi,
        'status': 'PENDING_REVIEW',
        'engagement_authenticity': authenticity,
        'earnings_verified': earnings,
        'created_at': datetime.now().isoformat(),
        'notes': f"[{freshness}] {engagement}{num_summary}{comment_summary}",
    }


def load_existing_urls():
    """Load existing URLs to deduplicate."""
    urls = set()
    if ALPHA_STAGING.exists():
        with open(ALPHA_STAGING, 'r', encoding='utf-8') as f:
            for row in csv.DictReader(f):
                if row.get('source_url'):
                    urls.add(row['source_url'])
    return urls


def get_next_alpha_id():
    """Get next ALPHA ID."""
    max_id = 0
    if ALPHA_STAGING.exists():
        with open(ALPHA_STAGING, 'r', encoding='utf-8') as f:
            for row in csv.DictReader(f):
                m = re.match(r'ALPHA(\d+)', row.get('alpha_id', ''))
                if m:
                    max_id = max(max_id, int(m.group(1)))
    return max_id + 1


def save_to_alpha_staging(entries):
    """Append entries to ALPHA_STAGING.csv."""
    if not entries:
        return

    fieldnames = ['alpha_id', 'source', 'source_url', 'tactic', 'category',
                  'roi_potential', 'status', 'engagement_authenticity',
                  'earnings_verified', 'created_at', 'notes']

    if not ALPHA_STAGING.exists():
        with open(ALPHA_STAGING, 'w', encoding='utf-8', newline='') as f:
            csv.DictWriter(f, fieldnames=fieldnames).writeheader()

    with open(ALPHA_STAGING, 'a', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction='ignore')
        writer.writerows(entries)


def main():
    parser = argparse.ArgumentParser(description='Reddit Deep Scraper - Quant-level alpha extraction')
    parser.add_argument('--time', default='week', choices=['day', 'week', 'month', 'year', 'all'],
                        help='Time filter for top posts (default: week)')
    parser.add_argument('--limit', type=int, help='Limit number of subreddits')
    parser.add_argument('--deep', action='store_true',
                        help='Also scrape top comments on high-engagement posts')
    parser.add_argument('--sub', type=str, help='Scrape a single subreddit (e.g. SideProject)')
    parser.add_argument('--posts-per-sub', type=int, default=25,
                        help='Posts per subreddit (default 25, max 100)')
    parser.add_argument('--all-time', action='store_true', help='Scrape top all-time')
    parser.add_argument('--daily', action='store_true',
                        help='Daily scrape: uses top/day for freshest signal')
    parser.add_argument('--full-scan', action='store_true',
                        help='Multi-timeframe scan: day + month + year with staleness detection')

    args = parser.parse_args()

    if args.all_time:
        args.time = 'all'
    elif args.daily:
        args.time = 'day'

    # Full-scan mode: run multiple timeframes
    if args.full_scan:
        timeframes = ['day', 'month', 'year']
        print(f"\n{'='*60}")
        print(f"FULL SCAN MODE: Running {', '.join(timeframes)} passes")
        print(f"Staleness detection ENABLED for month/year posts")
        print(f"{'='*60}\n")
    else:
        timeframes = [args.time]

    subreddits = load_subreddits(limit=args.limit, single_sub=args.sub)
    if not subreddits:
        print("No subreddits to scrape.")
        return

    existing_urls = load_existing_urls()
    next_id = get_next_alpha_id()
    all_entries = []
    all_raw = []  # For JSON backup
    total_posts = 0
    total_comments = 0
    skipped_dupes = 0

    print(f"\n{'='*60}")
    print(f"REDDIT DEEP SCRAPER")
    print(f"{'='*60}")
    print(f"Subreddits: {len(subreddits)}")
    print(f"Timeframes: {', '.join(f'top/{tf}' for tf in timeframes)}")
    print(f"Deep mode: {'ON' if args.deep else 'OFF'}")
    print(f"Starting ID: ALPHA{next_id}")
    print(f"{'='*60}\n")

    for tf_idx, current_tf in enumerate(timeframes, 1):
        if len(timeframes) > 1:
            print(f"\n{'='*40}")
            print(f"PASS {tf_idx}/{len(timeframes)}: top/{current_tf}")
            print(f"{'='*40}")

        for i, sub_info in enumerate(subreddits, 1):
            sub_name = sub_info.get('subreddit_name', '').replace('r/', '')
            if not sub_name:
                continue

            print(f"[{i}/{len(subreddits)}] r/{sub_name} ({sub_info.get('signal_quality', '?')}) top/{current_tf}...")

            posts = scrape_subreddit_posts(sub_name, time_filter=current_tf, post_limit=args.posts_per_sub)
            if not posts:
                print(f"  No posts found (may be private or empty)")
                continue

            sub_entries = []
            for post in posts:
                # Deduplicate (across all timeframes)
                if post['url'] in existing_urls:
                    skipped_dupes += 1
                    continue
                existing_urls.add(post['url'])

                # Skip very low quality (< 5 upvotes)
                if post['score'] < 5:
                    continue

                # Deep mode: scrape comments on high-engagement posts
                comments = None
                if args.deep and (post['score'] >= 50 or post['num_comments'] >= 20):
                    permalink = post['url'].replace('https://reddit.com', '')
                    comments = scrape_post_comments(permalink, depth=2, comment_limit=15)
                    total_comments += len(comments) if comments else 0

                # Build alpha entry with staleness detection for older timeframes
                entry = build_alpha_entry(post, comments=comments, sub_info=sub_info, time_filter=current_tf)
                entry['alpha_id'] = f"ALPHA{next_id}"
                next_id += 1
                sub_entries.append(entry)

                # Store raw data for JSON backup
                raw = {**post}
                raw['time_filter'] = current_tf
                if comments:
                    raw['comments'] = comments
                raw['extracted_numbers'] = extract_numbers(post['title'] + ' ' + post.get('selftext', ''))
                raw['freshness'] = check_staleness(post, current_tf)
                all_raw.append(raw)

            total_posts += len(sub_entries)
            all_entries.extend(sub_entries)

            # Stats per subreddit
            highest = len([e for e in sub_entries if e['roi_potential'] == 'HIGHEST'])
            high = len([e for e in sub_entries if e['roi_potential'] == 'HIGH'])
            print(f"  {len(sub_entries)} new posts ({highest} HIGHEST, {high} HIGH)")

    # Save to ALPHA_STAGING.csv
    if all_entries:
        save_to_alpha_staging(all_entries)

    # Save JSON backup
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    json_path = OUTPUT_DIR / f"reddit_{timestamp}.json"
    with open(json_path, 'w') as f:
        json.dump(all_raw, f, indent=2, default=str)

    # Stats summary
    cat_counts = {}
    roi_counts = {'HIGHEST': 0, 'HIGH': 0, 'MEDIUM': 0, 'LOW': 0}
    for e in all_entries:
        cat = e.get('category', 'UNKNOWN')
        cat_counts[cat] = cat_counts.get(cat, 0) + 1
        roi = e.get('roi_potential', 'LOW')
        roi_counts[roi] = roi_counts.get(roi, 0) + 1

    print(f"\n{'='*60}")
    print(f"SCRAPE COMPLETE")
    print(f"{'='*60}")
    print(f"Subreddits scraped: {len(subreddits)}")
    print(f"New entries: {total_posts}")
    print(f"Duplicates skipped: {skipped_dupes}")
    if args.deep:
        print(f"Comments scraped: {total_comments}")
    if len(timeframes) > 1:
        print(f"Timeframes scanned: {', '.join(timeframes)}")

    # Freshness breakdown for multi-timeframe scans
    if args.full_scan:
        freshness_counts = {}
        for e in all_entries:
            notes = e.get('notes', '')
            if notes.startswith('['):
                tag = notes.split(']')[0].replace('[', '')
                if tag.startswith('STALE'):
                    tag = 'STALE'
                freshness_counts[tag] = freshness_counts.get(tag, 0) + 1
        if freshness_counts:
            print(f"\nFreshness breakdown:")
            for f_tag, count in sorted(freshness_counts.items()):
                print(f"  {f_tag}: {count}")

    print(f"\nROI breakdown:")
    for roi, count in sorted(roi_counts.items(), key=lambda x: ['HIGHEST','HIGH','MEDIUM','LOW'].index(x[0])):
        if count > 0:
            print(f"  {roi}: {count}")
    print(f"\nCategory breakdown:")
    for cat, count in sorted(cat_counts.items(), key=lambda x: -x[1]):
        print(f"  {cat}: {count}")
    print(f"\nSaved to: {ALPHA_STAGING}")
    print(f"JSON backup: {json_path}")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
