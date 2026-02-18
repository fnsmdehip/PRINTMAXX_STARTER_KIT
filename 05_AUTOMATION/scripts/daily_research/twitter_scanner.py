#!/usr/bin/env python3
"""
Twitter/X Scanner for PRINTMAXX Daily Research

Scans high-signal X accounts from HIGH_SIGNAL_SOURCES.csv for new alpha.
Requires: X API credentials (or uses nitter/scraping as fallback).

Usage:
    python twitter_scanner.py [--dry-run] [--tier HIGHEST|HIGH|MEDIUM]
"""

import csv
import json
import os
import sys
import time
import logging
import hashlib
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional
from dataclasses import dataclass, asdict
import argparse

# Rate limiting
import random

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('twitter_scanner')

# Paths
BASE_DIR = Path(__file__).parent.parent.parent
LEDGER_DIR = BASE_DIR / 'LEDGER'
HIGH_SIGNAL_SOURCES = LEDGER_DIR / 'HIGH_SIGNAL_SOURCES.csv'
ALPHA_STAGING = LEDGER_DIR / 'ALPHA_STAGING.csv'
CACHE_DIR = BASE_DIR / 'AUTOMATIONS' / 'daily_research' / '.cache'


@dataclass
class Tweet:
    """Represents a tweet/post from X"""
    id: str
    author: str
    content: str
    url: str
    timestamp: datetime
    engagement: dict  # likes, retweets, replies
    media_urls: list


@dataclass
class AlphaFinding:
    """Represents a potential alpha finding"""
    alpha_id: str
    source: str
    source_url: str
    category: str
    title: str
    description: str
    actionable_steps: str
    effort_level: str  # LOW, MEDIUM, HIGH
    roi_potential: str  # LOW, MEDIUM, HIGH, HIGHEST
    risk_level: str  # LOW, MEDIUM, HIGH
    applies_to_niches: str
    status: str = 'PENDING_REVIEW'
    reviewed_date: str = ''
    reviewer_notes: str = ''


class RateLimiter:
    """Simple rate limiter for API calls"""

    def __init__(self, calls_per_minute: int = 15):
        self.calls_per_minute = calls_per_minute
        self.call_times = []

    def wait_if_needed(self):
        """Wait if we've hit the rate limit"""
        now = time.time()
        # Remove calls older than 1 minute
        self.call_times = [t for t in self.call_times if now - t < 60]

        if len(self.call_times) >= self.calls_per_minute:
            wait_time = 60 - (now - self.call_times[0])
            if wait_time > 0:
                logger.info(f"Rate limit reached. Waiting {wait_time:.1f}s...")
                time.sleep(wait_time + random.uniform(0.5, 2.0))

        self.call_times.append(time.time())


class TwitterScanner:
    """Scans X/Twitter accounts for alpha"""

    def __init__(self, api_key: Optional[str] = None, api_secret: Optional[str] = None):
        self.api_key = api_key or os.getenv('X_API_KEY')
        self.api_secret = api_secret or os.getenv('X_API_SECRET')
        self.bearer_token = os.getenv('X_BEARER_TOKEN')
        self.rate_limiter = RateLimiter(calls_per_minute=15)

        # Create cache directory
        CACHE_DIR.mkdir(parents=True, exist_ok=True)

        # Track what we've already seen
        self.seen_ids = self._load_seen_ids()

    def _load_seen_ids(self) -> set:
        """Load previously seen tweet IDs from cache"""
        cache_file = CACHE_DIR / 'seen_tweets.json'
        if cache_file.exists():
            try:
                with open(cache_file, 'r') as f:
                    data = json.load(f)
                    # Only keep IDs from last 7 days
                    cutoff = (datetime.now() - timedelta(days=7)).isoformat()
                    return {k for k, v in data.items() if v > cutoff}
            except Exception as e:
                logger.warning(f"Failed to load seen IDs: {e}")
        return set()

    def _save_seen_ids(self):
        """Save seen tweet IDs to cache"""
        cache_file = CACHE_DIR / 'seen_tweets.json'
        try:
            # Load existing and merge
            existing = {}
            if cache_file.exists():
                with open(cache_file, 'r') as f:
                    existing = json.load(f)

            # Add new IDs with current timestamp
            now = datetime.now().isoformat()
            for tweet_id in self.seen_ids:
                if tweet_id not in existing:
                    existing[tweet_id] = now

            # Prune old entries (older than 7 days)
            cutoff = (datetime.now() - timedelta(days=7)).isoformat()
            existing = {k: v for k, v in existing.items() if v > cutoff}

            with open(cache_file, 'w') as f:
                json.dump(existing, f)
        except Exception as e:
            logger.warning(f"Failed to save seen IDs: {e}")

    def get_x_sources(self, tier_filter: Optional[str] = None) -> list:
        """Get X accounts from HIGH_SIGNAL_SOURCES.csv"""
        sources = []

        with open(HIGH_SIGNAL_SOURCES, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row['platform'] == 'X' and row['auto_monitor'] == 'TRUE':
                    if tier_filter and row['signal_quality'] != tier_filter:
                        continue
                    sources.append({
                        'id': row['source_id'],
                        'name': row['source_name'],
                        'url': row['url'],
                        'focus_area': row['focus_area'],
                        'signal_quality': row['signal_quality'],
                        'notes': row['notes']
                    })

        return sources

    def fetch_tweets_api(self, username: str, count: int = 10) -> list[Tweet]:
        """
        Fetch tweets using X API v2.

        Requires X_BEARER_TOKEN environment variable.
        """
        if not self.bearer_token:
            logger.warning("No X_BEARER_TOKEN set. Skipping API fetch.")
            return []

        try:
            import requests

            self.rate_limiter.wait_if_needed()

            # Get user ID first
            username_clean = username.replace('@', '')
            user_url = f"https://api.twitter.com/2/users/by/username/{username_clean}"
            headers = {"Authorization": f"Bearer {self.bearer_token}"}

            user_response = requests.get(user_url, headers=headers, timeout=10)
            if user_response.status_code != 200:
                logger.error(f"Failed to get user {username}: {user_response.status_code}")
                return []

            user_data = user_response.json()
            if 'data' not in user_data:
                logger.warning(f"User not found: {username}")
                return []

            user_id = user_data['data']['id']

            # Get tweets
            self.rate_limiter.wait_if_needed()

            tweets_url = f"https://api.twitter.com/2/users/{user_id}/tweets"
            params = {
                'max_results': count,
                'tweet.fields': 'created_at,public_metrics,entities',
                'expansions': 'attachments.media_keys',
                'media.fields': 'url,preview_image_url'
            }

            tweets_response = requests.get(tweets_url, headers=headers, params=params, timeout=10)
            if tweets_response.status_code != 200:
                logger.error(f"Failed to get tweets for {username}: {tweets_response.status_code}")
                return []

            tweets_data = tweets_response.json()
            tweets = []

            for tweet in tweets_data.get('data', []):
                tweet_id = tweet['id']

                # Skip if already seen
                if tweet_id in self.seen_ids:
                    continue

                self.seen_ids.add(tweet_id)

                metrics = tweet.get('public_metrics', {})
                tweets.append(Tweet(
                    id=tweet_id,
                    author=username,
                    content=tweet['text'],
                    url=f"https://x.com/{username_clean}/status/{tweet_id}",
                    timestamp=datetime.fromisoformat(tweet['created_at'].replace('Z', '+00:00')),
                    engagement={
                        'likes': metrics.get('like_count', 0),
                        'retweets': metrics.get('retweet_count', 0),
                        'replies': metrics.get('reply_count', 0)
                    },
                    media_urls=[]
                ))

            return tweets

        except ImportError:
            logger.error("requests library not installed. Run: pip install requests")
            return []
        except Exception as e:
            logger.error(f"Error fetching tweets for {username}: {e}")
            return []

    def fetch_tweets_nitter(self, username: str, count: int = 10) -> list[Tweet]:
        """
        Fetch tweets using nitter (public instances).
        Fallback when API is not available.
        """
        try:
            import requests
            from bs4 import BeautifulSoup

            self.rate_limiter.wait_if_needed()

            username_clean = username.replace('@', '')

            # Try multiple nitter instances
            nitter_instances = [
                'nitter.privacydev.net',
                'nitter.poast.org',
                'nitter.1d4.us'
            ]

            for instance in nitter_instances:
                try:
                    url = f"https://{instance}/{username_clean}"
                    response = requests.get(url, timeout=10, headers={
                        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
                    })

                    if response.status_code == 200:
                        soup = BeautifulSoup(response.text, 'html.parser')
                        tweets = []

                        for tweet_elem in soup.select('.timeline-item')[:count]:
                            try:
                                content_elem = tweet_elem.select_one('.tweet-content')
                                if not content_elem:
                                    continue

                                link_elem = tweet_elem.select_one('.tweet-link')
                                tweet_url = f"https://x.com{link_elem['href']}" if link_elem else ''
                                tweet_id = tweet_url.split('/')[-1] if tweet_url else hashlib.md5(content_elem.text.encode()).hexdigest()

                                # Skip if already seen
                                if tweet_id in self.seen_ids:
                                    continue

                                self.seen_ids.add(tweet_id)

                                # Get engagement stats
                                stats = {}
                                for stat in tweet_elem.select('.tweet-stat'):
                                    icon = stat.select_one('.icon')
                                    if icon:
                                        stat_type = 'likes' if 'heart' in str(icon) else 'retweets' if 'retweet' in str(icon) else 'replies'
                                        stat_val = stat.text.strip()
                                        try:
                                            stats[stat_type] = int(stat_val.replace(',', '').replace('K', '000').replace('M', '000000'))
                                        except:
                                            stats[stat_type] = 0

                                tweets.append(Tweet(
                                    id=tweet_id,
                                    author=username,
                                    content=content_elem.text.strip(),
                                    url=tweet_url,
                                    timestamp=datetime.now(),  # Nitter doesn't always show exact time
                                    engagement=stats,
                                    media_urls=[]
                                ))
                            except Exception as e:
                                logger.debug(f"Failed to parse tweet: {e}")
                                continue

                        if tweets:
                            return tweets

                except Exception as e:
                    logger.debug(f"Nitter instance {instance} failed: {e}")
                    continue

            logger.warning(f"All nitter instances failed for {username}")
            return []

        except ImportError:
            logger.error("requests or bs4 not installed. Run: pip install requests beautifulsoup4")
            return []
        except Exception as e:
            logger.error(f"Error fetching from nitter for {username}: {e}")
            return []

    def analyze_tweet_for_alpha(self, tweet: Tweet, source_info: dict) -> Optional[AlphaFinding]:
        """
        Analyze a tweet to determine if it contains actionable alpha.

        Looks for:
        - Numbers/metrics (revenue, growth, conversions)
        - Tools/services mentioned
        - Tactics with specific steps
        - Case studies or results
        """
        content = tweet.content.lower()

        # Keywords that indicate potential alpha
        alpha_keywords = {
            'revenue': 'MONETIZATION',
            '$': 'MONETIZATION',
            'mrr': 'MONETIZATION',
            'arr': 'MONETIZATION',
            'conversion': 'GROWTH_HACK',
            'downloads': 'APP_FACTORY',
            'installs': 'APP_FACTORY',
            'subscribers': 'GROWTH_HACK',
            'views': 'CONTENT_FORMAT',
            'viral': 'CONTENT_FORMAT',
            'hook': 'CONTENT_FORMAT',
            'cold email': 'OUTBOUND',
            'reply rate': 'OUTBOUND',
            'open rate': 'OUTBOUND',
            'deliverability': 'OUTBOUND',
            'tool': 'TOOL_ALPHA',
            'app': 'APP_FACTORY',
            'launched': 'APP_FACTORY',
            'shipped': 'APP_FACTORY',
            'framework': 'GROWTH_HACK',
            'playbook': 'GROWTH_HACK',
            'strategy': 'GROWTH_HACK',
            'tactic': 'GROWTH_HACK',
            'seo': 'GROWTH_HACK',
            'traffic': 'GROWTH_HACK',
            'affiliate': 'MONETIZATION',
            'paywall': 'MONETIZATION'
        }

        # Check if tweet has high engagement (relative to author's typical)
        total_engagement = sum(tweet.engagement.values())

        # Look for alpha signals
        found_category = None
        for keyword, category in alpha_keywords.items():
            if keyword in content:
                found_category = category
                break

        # Skip if no alpha signals
        if not found_category:
            return None

        # Skip low-quality tweets (too short, no substance)
        if len(tweet.content) < 50:
            return None

        # Check for numbers (strong signal)
        import re
        has_numbers = bool(re.search(r'\d+[kKmM%$]|\$\d+|\d+%', tweet.content))

        # Determine effort and ROI based on content analysis
        effort_level = 'MEDIUM'
        if any(word in content for word in ['quick', 'easy', 'simple', 'free', '5 min', '10 min']):
            effort_level = 'LOW'
        elif any(word in content for word in ['complex', 'months', 'team', 'scale']):
            effort_level = 'HIGH'

        roi_potential = 'MEDIUM'
        if has_numbers:
            # Check for big numbers
            if re.search(r'\d{5,}|\$\d{4,}|[1-9]\d*[kKmM]', tweet.content):
                roi_potential = 'HIGHEST'
            elif re.search(r'\d{3,}|\$\d{2,}', tweet.content):
                roi_potential = 'HIGH'

        # Generate alpha ID
        alpha_id = f"ALPHA{hashlib.md5(tweet.id.encode()).hexdigest()[:6].upper()}"

        # Extract title (first sentence or first 100 chars)
        title = tweet.content.split('.')[0][:100]
        if len(title) < len(tweet.content):
            title += '...'

        return AlphaFinding(
            alpha_id=alpha_id,
            source=source_info['name'],
            source_url=tweet.url,
            category=found_category,
            title=title,
            description=tweet.content[:500],
            actionable_steps='Review and extract specific steps from source',
            effort_level=effort_level,
            roi_potential=roi_potential,
            risk_level='LOW',
            applies_to_niches='ALL',  # Can be refined later
            status='PENDING_REVIEW'
        )

    def scan_all_sources(self, tier_filter: Optional[str] = None, dry_run: bool = False) -> list[AlphaFinding]:
        """Scan all X sources and return findings"""
        sources = self.get_x_sources(tier_filter)
        logger.info(f"Scanning {len(sources)} X accounts...")

        all_findings = []

        for source in sources:
            logger.info(f"Scanning {source['name']}...")

            # Try API first, fall back to nitter
            tweets = self.fetch_tweets_api(source['name'])
            if not tweets:
                tweets = self.fetch_tweets_nitter(source['name'])

            for tweet in tweets:
                finding = self.analyze_tweet_for_alpha(tweet, source)
                if finding:
                    all_findings.append(finding)
                    logger.info(f"  Found potential alpha: {finding.title[:50]}...")

            # Be nice to servers
            time.sleep(random.uniform(1, 3))

        # Save seen IDs
        if not dry_run:
            self._save_seen_ids()

        return all_findings

    def save_findings(self, findings: list[AlphaFinding]) -> int:
        """Save findings to ALPHA_STAGING.csv"""
        if not findings:
            return 0

        # Load existing alpha IDs to avoid duplicates
        existing_ids = set()
        if ALPHA_STAGING.exists():
            with open(ALPHA_STAGING, 'r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    existing_ids.add(row['alpha_id'])

        # Filter out duplicates
        new_findings = [f for f in findings if f.alpha_id not in existing_ids]

        if not new_findings:
            logger.info("No new findings to save (all duplicates)")
            return 0

        # Append to CSV
        file_exists = ALPHA_STAGING.exists()
        with open(ALPHA_STAGING, 'a', newline='') as f:
            fieldnames = [
                'alpha_id', 'source', 'source_url', 'category', 'title',
                'description', 'actionable_steps', 'effort_level', 'roi_potential',
                'risk_level', 'applies_to_niches', 'status', 'reviewed_date', 'reviewer_notes'
            ]
            writer = csv.DictWriter(f, fieldnames=fieldnames)

            if not file_exists:
                writer.writeheader()

            for finding in new_findings:
                writer.writerow(asdict(finding))

        logger.info(f"Saved {len(new_findings)} new findings to ALPHA_STAGING.csv")
        return len(new_findings)


def main():
    parser = argparse.ArgumentParser(description='Scan X/Twitter for alpha')
    parser.add_argument('--dry-run', action='store_true', help='Preview without saving')
    parser.add_argument('--tier', choices=['HIGHEST', 'HIGH', 'MEDIUM'], help='Filter by signal tier')
    args = parser.parse_args()

    scanner = TwitterScanner()
    findings = scanner.scan_all_sources(tier_filter=args.tier, dry_run=args.dry_run)

    if args.dry_run:
        logger.info(f"DRY RUN: Would save {len(findings)} findings")
        for f in findings:
            print(f"  - [{f.category}] {f.title[:60]}...")
    else:
        saved = scanner.save_findings(findings)
        logger.info(f"Scan complete. Saved {saved} new findings.")

    return findings


if __name__ == '__main__':
    main()
