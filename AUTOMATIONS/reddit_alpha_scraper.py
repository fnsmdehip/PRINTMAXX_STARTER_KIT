#!/usr/bin/env python3
"""
Reddit Alpha Scraper - Extract Meta & Alpha from Subreddits

CRITICAL: Daily scraping of both research AND launch subreddits for:
1. Meta detection (trending topics, meme coins, viral products)
2. Alpha extraction (tactics, tools, methods)
3. Content opportunities (repost trending topics for visibility)
4. Trading signals (meme coin patterns for backtesting)

Runs: Daily (automated via cron or ralph loop)
Output: LEDGER/ALPHA_STAGING.csv + META_TRACKER.csv + MEME_COIN_SIGNALS.csv
"""

import csv
import json
import re
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Set
from collections import defaultdict
import time

# Configuration
OUTPUT_ALPHA = Path("LEDGER/ALPHA_STAGING.csv")
OUTPUT_META = Path("LEDGER/META_TRACKER.csv")
OUTPUT_MEME = Path("LEDGER/MEME_COIN_SIGNALS.csv")
SUBREDDIT_LIST = Path("LEDGER/RESEARCH_SUBREDDITS.csv")
LOG_FILE = Path("AUTOMATIONS/logs/reddit_scraper.log")
JSON_BACKUP_DIR = Path("AUTOMATIONS/reddit_scraper_output")

# Meta detection keywords
META_KEYWORDS = {
    'ai_products': ['claude', 'chatgpt', 'gemini', 'llm', 'ai agent', 'automation', 'mcp server'],
    'meme_coins': ['memecoin', 'meme coin', 'coin launch', 'token', 'presale', 'airdrop'],
    'viral_tools': ['blew up', 'went viral', 'trending', 'product hunt', 'launch'],
    'arbitrage': ['arbitrage', 'underpriced', 'mispriced', 'opportunity', 'exploit'],
    'platform_changes': ['algorithm', 'policy change', 'new feature', 'update', 'ban'],
}

# Meme coin signal patterns (for backtesting)
MEME_COIN_PATTERNS = [
    r'(?i)(\w+)\s+(?:coin|token).*(?:launched|dropping|presale)',
    r'(?i)(?:new|just)\s+(?:coin|token).*(?:called|named)\s+(\w+)',
    r'(?i)(\w+)\s+(?:to the moon|moon|pumping|mooning)',
    r'(?i)agent.*(?:coin|token)',  # Agent-related coins
]


def log(message: str):
    """Write to log file with timestamp."""
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(LOG_FILE, 'a') as f:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"[{timestamp}] {message}\n")
    print(f"[{timestamp}] {message}")


def load_subreddits() -> List[Dict]:
    """Load subreddit list from CSV."""
    if not SUBREDDIT_LIST.exists():
        log(f"Warning: {SUBREDDIT_LIST} not found.")
        return []

    subreddits = []
    with open(SUBREDDIT_LIST, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row.get('auto_monitor') == 'TRUE':
                subreddits.append(row)

    log(f"Loaded {len(subreddits)} subreddits to monitor")
    return subreddits


def scrape_subreddit(subreddit_name: str, time_filter: str = 'week') -> List[Dict]:
    """
    Scrape top posts from a subreddit.

    In production, this would use:
    - PRAW (Python Reddit API Wrapper) for authenticated access
    - Or Reddit JSON API for public access
    - Or Playwright for browser automation

    For now: Returns template structure for manual implementation.
    """
    log(f"Scraping {subreddit_name} (top posts from {time_filter})")

    # Template structure - replace with actual Reddit API call
    # Example using Reddit JSON API (no auth needed):
    # url = f"https://www.reddit.com{subreddit_name}/top.json?t={time_filter}&limit=25"
    # response = requests.get(url, headers={'User-Agent': 'PRINTMAXX/1.0'})
    # data = response.json()

    posts = []

    # Example post structure - this is what actual scraping would return
    # for post_data in data['data']['children']:
    #     post = post_data['data']
    #     posts.append({
    #         'post_id': post['id'],
    #         'title': post['title'],
    #         'selftext': post.get('selftext', ''),
    #         'url': f"https://reddit.com{post['permalink']}",
    #         'score': post['score'],
    #         'num_comments': post['num_comments'],
    #         'created_utc': post['created_utc'],
    #         'author': post['author'],
    #         'subreddit': subreddit_name,
    #     })

    return posts


def scrape_post_comments(post_url: str, depth: int = 2) -> List[Dict]:
    """
    Scrape comments from a post, including nested replies.

    Args:
        post_url: Reddit post URL
        depth: How many levels deep to scrape (1=top-level, 2=replies to top-level, etc.)

    Returns list of comments with metadata.
    """
    log(f"Scraping comments from {post_url} (depth={depth})")

    # Template structure - replace with actual Reddit API call
    # url = f"{post_url}.json"
    # response = requests.get(url, headers={'User-Agent': 'PRINTMAXX/1.0'})
    # data = response.json()

    comments = []

    # Example comment extraction - this is what actual scraping would return
    # def extract_comments(comment_data, current_depth=1):
    #     if current_depth > depth:
    #         return
    #
    #     for comment in comment_data:
    #         if comment['kind'] == 't1':  # Comment type
    #             c = comment['data']
    #             comments.append({
    #                 'comment_id': c['id'],
    #                 'body': c['body'],
    #                 'score': c['score'],
    #                 'author': c['author'],
    #                 'created_utc': c['created_utc'],
    #                 'depth': current_depth,
    #             })
    #
    #             if 'replies' in c and c['replies']:
    #                 extract_comments(c['replies']['data']['children'], current_depth + 1)

    return comments


def detect_meta(posts: List[Dict], comments: List[Dict]) -> List[Dict]:
    """
    Detect trending meta from posts and comments.

    Looks for:
    - High-velocity topics (multiple posts about same thing in short time)
    - Meme coin mentions with timing data
    - Viral products/tools
    - Platform changes affecting operations
    """
    meta_findings = []

    # Combine all text for analysis
    all_text = []
    for post in posts:
        all_text.append({
            'text': f"{post.get('title', '')} {post.get('selftext', '')}",
            'type': 'post',
            'score': post.get('score', 0),
            'timestamp': post.get('created_utc', 0),
            'url': post.get('url', ''),
        })

    for comment in comments:
        all_text.append({
            'text': comment.get('body', ''),
            'type': 'comment',
            'score': comment.get('score', 0),
            'timestamp': comment.get('created_utc', 0),
            'url': '',
        })

    # Detect patterns
    for category, keywords in META_KEYWORDS.items():
        matches = []
        for item in all_text:
            text_lower = item['text'].lower()
            for keyword in keywords:
                if keyword in text_lower:
                    matches.append(item)
                    break

        if matches:
            # High-velocity check: multiple mentions in 24h = trending
            recent_matches = [m for m in matches if time.time() - m['timestamp'] < 86400]
            if len(recent_matches) >= 3:
                meta_findings.append({
                    'category': category,
                    'keywords': keywords,
                    'mention_count': len(recent_matches),
                    'total_score': sum(m['score'] for m in recent_matches),
                    'discovered_date': datetime.now().isoformat(),
                    'status': 'TRENDING',
                })

    return meta_findings


def detect_meme_coin_signals(posts: List[Dict], comments: List[Dict]) -> List[Dict]:
    """
    Detect meme coin launch signals for potential trading opportunities.

    Patterns to look for:
    - New coin mentions with agent/AI keywords
    - Coin launches with timestamps (for backtesting entry timing)
    - Community sentiment velocity (rapid comment growth = FOMO signal)
    """
    signals = []

    all_text = []
    for post in posts:
        all_text.append({
            'text': f"{post.get('title', '')} {post.get('selftext', '')}",
            'score': post.get('score', 0),
            'num_comments': post.get('num_comments', 0),
            'timestamp': post.get('created_utc', 0),
            'url': post.get('url', ''),
        })

    for comment in comments:
        all_text.append({
            'text': comment.get('body', ''),
            'score': comment.get('score', 0),
            'num_comments': 0,
            'timestamp': comment.get('created_utc', 0),
            'url': '',
        })

    # Match against meme coin patterns
    for item in all_text:
        for pattern in MEME_COIN_PATTERNS:
            match = re.search(pattern, item['text'])
            if match:
                coin_name = match.group(1) if match.lastindex >= 1 else 'UNKNOWN'

                signals.append({
                    'coin_name': coin_name,
                    'detected_timestamp': datetime.fromtimestamp(item['timestamp']).isoformat(),
                    'score': item['score'],
                    'comment_count': item['num_comments'],
                    'source_url': item['url'],
                    'text_snippet': item['text'][:200],
                    'pattern_matched': pattern,
                    'status': 'DETECTED',
                })

    # Deduplicate by coin name (keep highest score)
    unique_signals = {}
    for signal in signals:
        coin = signal['coin_name']
        if coin not in unique_signals or signal['score'] > unique_signals[coin]['score']:
            unique_signals[coin] = signal

    return list(unique_signals.values())


def extract_alpha(posts: List[Dict], comments: List[Dict]) -> List[Dict]:
    """
    Extract actionable alpha (tactics, tools, methods) from posts and comments.
    """
    alpha_entries = []

    # Look for high-signal patterns:
    # - Posts with specific numbers (revenue, growth %, conversion rate)
    # - Comments with step-by-step instructions
    # - Tool recommendations with proof (upvotes, replies)
    # - Case studies with metrics

    for post in posts:
        title = post.get('title', '')
        selftext = post.get('selftext', '')
        score = post.get('score', 0)

        # High score + specific numbers = potential alpha
        if score > 100 and any(char.isdigit() for char in title + selftext):
            alpha_entries.append({
                'source': post.get('subreddit', ''),
                'source_url': post.get('url', ''),
                'title': title,
                'snippet': selftext[:300],
                'score': score,
                'category': 'PENDING_CATEGORIZATION',
                'status': 'PENDING_REVIEW',
                'discovered_date': datetime.now().isoformat(),
            })

    # High-value comments (score > 50)
    for comment in comments:
        if comment.get('score', 0) > 50:
            alpha_entries.append({
                'source': 'Reddit comment',
                'source_url': '',
                'title': f"High-value comment ({comment['score']} upvotes)",
                'snippet': comment.get('body', '')[:300],
                'score': comment['score'],
                'category': 'PENDING_CATEGORIZATION',
                'status': 'PENDING_REVIEW',
                'discovered_date': datetime.now().isoformat(),
            })

    return alpha_entries


def dedupe_alpha(new_alpha: List[Dict]) -> List[Dict]:
    """Check if alpha entries already exist in ALPHA_STAGING.csv."""
    existing_urls = set()

    if OUTPUT_ALPHA.exists():
        with open(OUTPUT_ALPHA, 'r') as f:
            reader = csv.DictReader(f)
            existing_urls = {row.get('source_url', '') for row in reader if row.get('source_url')}

    unique_alpha = []
    for entry in new_alpha:
        if entry.get('source_url', '') not in existing_urls:
            unique_alpha.append(entry)
        else:
            log(f"Skipping duplicate: {entry.get('source_url', '')}")

    return unique_alpha


def save_alpha(alpha_entries: List[Dict]):
    """Append alpha entries to ALPHA_STAGING.csv."""
    if not alpha_entries:
        log("No new alpha to save.")
        return

    OUTPUT_ALPHA.parent.mkdir(parents=True, exist_ok=True)
    file_exists = OUTPUT_ALPHA.exists()

    # Get next alpha_id
    next_id = get_next_alpha_id()

    with open(OUTPUT_ALPHA, 'a', newline='') as f:
        fieldnames = [
            'alpha_id', 'source', 'source_url', 'category',
            'status', 'roi_potential', 'discovered_date', 'title', 'snippet', 'score'
        ]
        writer = csv.DictWriter(f, fieldnames=fieldnames)

        if not file_exists:
            writer.writeheader()

        for i, entry in enumerate(alpha_entries):
            row = {
                'alpha_id': f"ALPHA{next_id + i:04d}",
                'source': entry.get('source', ''),
                'source_url': entry.get('source_url', ''),
                'category': entry.get('category', 'PENDING_CATEGORIZATION'),
                'status': 'PENDING_REVIEW',
                'roi_potential': 'MEDIUM',  # Default, updated during review
                'discovered_date': entry.get('discovered_date', datetime.now().isoformat()),
                'title': entry.get('title', ''),
                'snippet': entry.get('snippet', ''),
                'score': entry.get('score', 0),
            }
            writer.writerow(row)

    log(f"✅ Saved {len(alpha_entries)} new alpha entries")


def save_meta(meta_findings: List[Dict]):
    """Save meta tracker data."""
    if not meta_findings:
        log("No meta findings to save.")
        return

    OUTPUT_META.parent.mkdir(parents=True, exist_ok=True)
    file_exists = OUTPUT_META.exists()

    with open(OUTPUT_META, 'a', newline='') as f:
        fieldnames = [
            'meta_id', 'category', 'keywords', 'mention_count',
            'total_score', 'discovered_date', 'status'
        ]
        writer = csv.DictWriter(f, fieldnames=fieldnames)

        if not file_exists:
            writer.writeheader()

        for i, meta in enumerate(meta_findings):
            row = {
                'meta_id': f"META{int(time.time())}_{i}",
                'category': meta['category'],
                'keywords': ', '.join(meta['keywords']),
                'mention_count': meta['mention_count'],
                'total_score': meta['total_score'],
                'discovered_date': meta['discovered_date'],
                'status': meta['status'],
            }
            writer.writerow(row)

    log(f"✅ Saved {len(meta_findings)} meta findings")


def save_meme_coin_signals(signals: List[Dict]):
    """Save meme coin signals for backtesting."""
    if not signals:
        log("No meme coin signals to save.")
        return

    OUTPUT_MEME.parent.mkdir(parents=True, exist_ok=True)
    file_exists = OUTPUT_MEME.exists()

    with open(OUTPUT_MEME, 'a', newline='') as f:
        fieldnames = [
            'signal_id', 'coin_name', 'detected_timestamp', 'score',
            'comment_count', 'source_url', 'text_snippet', 'pattern_matched', 'status'
        ]
        writer = csv.DictWriter(f, fieldnames=fieldnames)

        if not file_exists:
            writer.writeheader()

        for i, signal in enumerate(signals):
            row = {
                'signal_id': f"COIN{int(time.time())}_{i}",
                'coin_name': signal['coin_name'],
                'detected_timestamp': signal['detected_timestamp'],
                'score': signal['score'],
                'comment_count': signal['comment_count'],
                'source_url': signal['source_url'],
                'text_snippet': signal['text_snippet'],
                'pattern_matched': signal['pattern_matched'],
                'status': signal['status'],
            }
            writer.writerow(row)

    log(f"✅ Saved {len(signals)} meme coin signals")


def get_next_alpha_id() -> int:
    """Get next sequential alpha ID from existing entries."""
    max_id = 0
    if OUTPUT_ALPHA.exists():
        with open(OUTPUT_ALPHA, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                alpha_id = row.get('alpha_id', '')
                if alpha_id.startswith('ALPHA'):
                    try:
                        num = int(alpha_id.replace('ALPHA', ''))
                        max_id = max(max_id, num)
                    except Exception:
                        pass  # Non-numeric alpha_id suffix; skip
    return max_id + 1


def main():
    """Main execution flow."""
    log("=" * 60)
    log("Reddit Alpha Scraper - Starting")
    log("=" * 60)

    # 1. Load subreddits to monitor
    subreddits = load_subreddits()

    all_posts = []
    all_comments = []

    # 2. Scrape each subreddit
    for subreddit in subreddits:
        subreddit_name = subreddit['subreddit_name']

        # Scrape top posts from this week
        posts = scrape_subreddit(subreddit_name, time_filter='week')
        all_posts.extend(posts)

        # For high-signal posts, scrape comments
        for post in posts:
            if post.get('score', 0) > 100 or post.get('num_comments', 0) > 50:
                comments = scrape_post_comments(post['url'], depth=2)
                all_comments.extend(comments)

        # Rate limiting
        time.sleep(2)

    log(f"Scraped {len(all_posts)} posts and {len(all_comments)} comments")

    # 3. Extract insights
    meta_findings = detect_meta(all_posts, all_comments)
    meme_coin_signals = detect_meme_coin_signals(all_posts, all_comments)
    alpha_entries = extract_alpha(all_posts, all_comments)

    # 4. Deduplicate alpha
    unique_alpha = dedupe_alpha(alpha_entries)
    log(f"{len(unique_alpha)} unique alpha entries (out of {len(alpha_entries)} total)")

    # 5. Save all outputs
    save_alpha(unique_alpha)
    save_meta(meta_findings)
    save_meme_coin_signals(meme_coin_signals)

    # 6. Save raw JSON backup
    JSON_BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    with open(JSON_BACKUP_DIR / f"posts_{timestamp}.json", 'w') as f:
        json.dump(all_posts, f, indent=2)

    with open(JSON_BACKUP_DIR / f"comments_{timestamp}.json", 'w') as f:
        json.dump(all_comments, f, indent=2)

    log("=" * 60)
    log(f"Complete: {len(unique_alpha)} alpha, {len(meta_findings)} meta, {len(meme_coin_signals)} coin signals")
    log("=" * 60)


if __name__ == "__main__":
    main()
