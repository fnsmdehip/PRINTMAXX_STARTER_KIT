#!/usr/bin/env python3
"""
Reddit Scanner for PRINTMAXX Daily Research

Scans subreddits from HIGH_SIGNAL_SOURCES.csv for new alpha.
Uses Reddit API (PRAW) or JSON API as fallback.

Usage:
    python reddit_scanner.py [--dry-run] [--tier HIGHEST|HIGH|MEDIUM]
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
import random

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('reddit_scanner')

# Paths
BASE_DIR = Path(__file__).parent.parent.parent
LEDGER_DIR = BASE_DIR / 'LEDGER'
HIGH_SIGNAL_SOURCES = LEDGER_DIR / 'HIGH_SIGNAL_SOURCES.csv'
ALPHA_STAGING = LEDGER_DIR / 'ALPHA_STAGING.csv'
CACHE_DIR = BASE_DIR / 'AUTOMATIONS' / 'daily_research' / '.cache'


@dataclass
class RedditPost:
    """Represents a Reddit post"""
    id: str
    subreddit: str
    title: str
    selftext: str
    url: str
    permalink: str
    score: int
    num_comments: int
    created_utc: float
    author: str
    link_flair_text: Optional[str]


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
    effort_level: str
    roi_potential: str
    risk_level: str
    applies_to_niches: str
    status: str = 'PENDING_REVIEW'
    reviewed_date: str = ''
    reviewer_notes: str = ''


class RateLimiter:
    """Simple rate limiter for API calls"""

    def __init__(self, calls_per_minute: int = 30):
        self.calls_per_minute = calls_per_minute
        self.call_times = []

    def wait_if_needed(self):
        """Wait if we've hit the rate limit"""
        now = time.time()
        self.call_times = [t for t in self.call_times if now - t < 60]

        if len(self.call_times) >= self.calls_per_minute:
            wait_time = 60 - (now - self.call_times[0])
            if wait_time > 0:
                logger.info(f"Rate limit reached. Waiting {wait_time:.1f}s...")
                time.sleep(wait_time + random.uniform(0.5, 2.0))

        self.call_times.append(time.time())


class RedditScanner:
    """Scans Reddit for alpha"""

    def __init__(self):
        self.client_id = os.getenv('REDDIT_CLIENT_ID')
        self.client_secret = os.getenv('REDDIT_CLIENT_SECRET')
        self.user_agent = os.getenv('REDDIT_USER_AGENT', 'PRINTMAXX-Research/1.0')
        self.rate_limiter = RateLimiter(calls_per_minute=30)

        # Create cache directory
        CACHE_DIR.mkdir(parents=True, exist_ok=True)

        # Track what we've already seen
        self.seen_ids = self._load_seen_ids()

    def _load_seen_ids(self) -> set:
        """Load previously seen post IDs from cache"""
        cache_file = CACHE_DIR / 'seen_reddit.json'
        if cache_file.exists():
            try:
                with open(cache_file, 'r') as f:
                    data = json.load(f)
                    cutoff = (datetime.now() - timedelta(days=7)).isoformat()
                    return {k for k, v in data.items() if v > cutoff}
            except Exception as e:
                logger.warning(f"Failed to load seen IDs: {e}")
        return set()

    def _save_seen_ids(self):
        """Save seen post IDs to cache"""
        cache_file = CACHE_DIR / 'seen_reddit.json'
        try:
            existing = {}
            if cache_file.exists():
                with open(cache_file, 'r') as f:
                    existing = json.load(f)

            now = datetime.now().isoformat()
            for post_id in self.seen_ids:
                if post_id not in existing:
                    existing[post_id] = now

            cutoff = (datetime.now() - timedelta(days=7)).isoformat()
            existing = {k: v for k, v in existing.items() if v > cutoff}

            with open(cache_file, 'w') as f:
                json.dump(existing, f)
        except Exception as e:
            logger.warning(f"Failed to save seen IDs: {e}")

    def get_reddit_sources(self, tier_filter: Optional[str] = None) -> list:
        """Get subreddits from HIGH_SIGNAL_SOURCES.csv"""
        sources = []

        with open(HIGH_SIGNAL_SOURCES, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row['platform'] == 'Reddit' and row['auto_monitor'] == 'TRUE':
                    if tier_filter and row['signal_quality'] != tier_filter:
                        continue

                    # Extract subreddit name from URL
                    url = row['url']
                    subreddit = url.split('/r/')[-1].rstrip('/')

                    sources.append({
                        'id': row['source_id'],
                        'name': row['source_name'],
                        'subreddit': subreddit,
                        'url': url,
                        'focus_area': row['focus_area'],
                        'signal_quality': row['signal_quality'],
                        'notes': row['notes']
                    })

        return sources

    def fetch_posts_json_api(self, subreddit: str, limit: int = 25, sort: str = 'hot') -> list[RedditPost]:
        """
        Fetch posts using Reddit's public JSON API.
        No authentication required.
        """
        try:
            import requests

            self.rate_limiter.wait_if_needed()

            url = f"https://www.reddit.com/r/{subreddit}/{sort}.json"
            params = {'limit': limit, 'raw_json': 1}
            headers = {'User-Agent': self.user_agent}

            response = requests.get(url, params=params, headers=headers, timeout=10)

            if response.status_code != 200:
                logger.error(f"Failed to fetch r/{subreddit}: {response.status_code}")
                return []

            data = response.json()
            posts = []

            for child in data.get('data', {}).get('children', []):
                post_data = child.get('data', {})
                post_id = post_data.get('id', '')

                # Skip if already seen
                if post_id in self.seen_ids:
                    continue

                self.seen_ids.add(post_id)

                posts.append(RedditPost(
                    id=post_id,
                    subreddit=subreddit,
                    title=post_data.get('title', ''),
                    selftext=post_data.get('selftext', ''),
                    url=post_data.get('url', ''),
                    permalink=f"https://reddit.com{post_data.get('permalink', '')}",
                    score=post_data.get('score', 0),
                    num_comments=post_data.get('num_comments', 0),
                    created_utc=post_data.get('created_utc', 0),
                    author=post_data.get('author', '[deleted]'),
                    link_flair_text=post_data.get('link_flair_text')
                ))

            return posts

        except ImportError:
            logger.error("requests library not installed. Run: pip install requests")
            return []
        except Exception as e:
            logger.error(f"Error fetching r/{subreddit}: {e}")
            return []

    def fetch_posts_praw(self, subreddit: str, limit: int = 25) -> list[RedditPost]:
        """
        Fetch posts using PRAW (Python Reddit API Wrapper).
        Requires REDDIT_CLIENT_ID and REDDIT_CLIENT_SECRET.
        """
        if not self.client_id or not self.client_secret:
            logger.debug("No Reddit API credentials. Falling back to JSON API.")
            return []

        try:
            import praw

            reddit = praw.Reddit(
                client_id=self.client_id,
                client_secret=self.client_secret,
                user_agent=self.user_agent
            )

            self.rate_limiter.wait_if_needed()

            sub = reddit.subreddit(subreddit)
            posts = []

            for post in sub.hot(limit=limit):
                if post.id in self.seen_ids:
                    continue

                self.seen_ids.add(post.id)

                posts.append(RedditPost(
                    id=post.id,
                    subreddit=subreddit,
                    title=post.title,
                    selftext=post.selftext,
                    url=post.url,
                    permalink=f"https://reddit.com{post.permalink}",
                    score=post.score,
                    num_comments=post.num_comments,
                    created_utc=post.created_utc,
                    author=str(post.author) if post.author else '[deleted]',
                    link_flair_text=post.link_flair_text
                ))

            return posts

        except ImportError:
            logger.debug("praw not installed. Falling back to JSON API.")
            return []
        except Exception as e:
            logger.error(f"Error fetching r/{subreddit} via PRAW: {e}")
            return []

    def analyze_post_for_alpha(self, post: RedditPost, source_info: dict) -> Optional[AlphaFinding]:
        """
        Analyze a Reddit post to determine if it contains actionable alpha.
        """
        content = f"{post.title} {post.selftext}".lower()

        # Skip posts with low engagement (unless very new)
        post_age_hours = (time.time() - post.created_utc) / 3600
        if post.score < 10 and post_age_hours > 24:
            return None

        # Keywords that indicate potential alpha
        alpha_keywords = {
            'revenue': 'MONETIZATION',
            'income': 'MONETIZATION',
            '$': 'MONETIZATION',
            'mrr': 'MONETIZATION',
            'launched': 'APP_FACTORY',
            'shipped': 'APP_FACTORY',
            'released': 'APP_FACTORY',
            'built': 'APP_FACTORY',
            'case study': 'GROWTH_HACK',
            'how i': 'GROWTH_HACK',
            'guide': 'GROWTH_HACK',
            'strategy': 'GROWTH_HACK',
            'tactic': 'GROWTH_HACK',
            'tool': 'TOOL_ALPHA',
            'app': 'APP_FACTORY',
            'saas': 'APP_FACTORY',
            'growth': 'GROWTH_HACK',
            'traffic': 'GROWTH_HACK',
            'seo': 'GROWTH_HACK',
            'marketing': 'GROWTH_HACK',
            'cold email': 'OUTBOUND',
            'outreach': 'OUTBOUND',
            'affiliate': 'MONETIZATION',
            'conversion': 'GROWTH_HACK',
            'subscribers': 'GROWTH_HACK',
            'viral': 'CONTENT_FORMAT',
            'content': 'CONTENT_FORMAT'
        }

        found_category = None
        for keyword, category in alpha_keywords.items():
            if keyword in content:
                found_category = category
                break

        if not found_category:
            return None

        # Skip very short posts
        if len(post.selftext) < 100 and not any(c in post.title.lower() for c in ['how', 'guide', 'case', 'launched']):
            return None

        # Check for numbers (strong signal)
        import re
        has_numbers = bool(re.search(r'\d+[kKmM%$]|\$\d+|\d+%', content))

        # Determine effort and ROI
        effort_level = 'MEDIUM'
        if any(word in content for word in ['quick', 'easy', 'simple', 'free', 'minute']):
            effort_level = 'LOW'
        elif any(word in content for word in ['complex', 'months', 'team', 'enterprise']):
            effort_level = 'HIGH'

        roi_potential = 'MEDIUM'
        if has_numbers:
            if re.search(r'\d{5,}|\$\d{4,}|[1-9]\d*[kKmM]', content):
                roi_potential = 'HIGHEST'
            elif re.search(r'\d{3,}|\$\d{2,}', content):
                roi_potential = 'HIGH'

        # Boost ROI for high-engagement posts
        if post.score > 100:
            roi_potential = 'HIGH' if roi_potential == 'MEDIUM' else roi_potential
        if post.score > 500:
            roi_potential = 'HIGHEST'

        alpha_id = f"ALPHA{hashlib.md5(post.id.encode()).hexdigest()[:6].upper()}"

        # Create description from title and selftext
        description = post.title
        if post.selftext:
            description += f" - {post.selftext[:400]}"
            if len(post.selftext) > 400:
                description += "..."

        return AlphaFinding(
            alpha_id=alpha_id,
            source=f"r/{post.subreddit}",
            source_url=post.permalink,
            category=found_category,
            title=post.title[:100],
            description=description[:500],
            actionable_steps='Review post and comments for specific tactics',
            effort_level=effort_level,
            roi_potential=roi_potential,
            risk_level='LOW',
            applies_to_niches='ALL',
            status='PENDING_REVIEW'
        )

    def scan_all_sources(self, tier_filter: Optional[str] = None, dry_run: bool = False) -> list[AlphaFinding]:
        """Scan all Reddit sources and return findings"""
        sources = self.get_reddit_sources(tier_filter)
        logger.info(f"Scanning {len(sources)} subreddits...")

        all_findings = []

        for source in sources:
            subreddit = source['subreddit']
            logger.info(f"Scanning r/{subreddit}...")

            # Try PRAW first, fall back to JSON API
            posts = self.fetch_posts_praw(subreddit)
            if not posts:
                posts = self.fetch_posts_json_api(subreddit)

            for post in posts:
                finding = self.analyze_post_for_alpha(post, source)
                if finding:
                    all_findings.append(finding)
                    logger.info(f"  Found potential alpha: {finding.title[:50]}...")

            time.sleep(random.uniform(1, 2))

        if not dry_run:
            self._save_seen_ids()

        return all_findings

    def save_findings(self, findings: list[AlphaFinding]) -> int:
        """Save findings to ALPHA_STAGING.csv"""
        if not findings:
            return 0

        existing_ids = set()
        if ALPHA_STAGING.exists():
            with open(ALPHA_STAGING, 'r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    existing_ids.add(row['alpha_id'])

        new_findings = [f for f in findings if f.alpha_id not in existing_ids]

        if not new_findings:
            logger.info("No new findings to save (all duplicates)")
            return 0

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
    parser = argparse.ArgumentParser(description='Scan Reddit for alpha')
    parser.add_argument('--dry-run', action='store_true', help='Preview without saving')
    parser.add_argument('--tier', choices=['HIGHEST', 'HIGH', 'MEDIUM'], help='Filter by signal tier')
    args = parser.parse_args()

    scanner = RedditScanner()
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
