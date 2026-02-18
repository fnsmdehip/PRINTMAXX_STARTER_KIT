#!/usr/bin/env python3
"""
Hacker News Scanner for PRINTMAXX Daily Research

Scans HN front page and relevant topics for new alpha.
Uses HN's public API (no auth required).

Usage:
    python hn_scanner.py [--dry-run] [--count 30]
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
from typing import Optional, List
from dataclasses import dataclass, asdict
import argparse
import random

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('hn_scanner')

# Paths
BASE_DIR = Path(__file__).parent.parent.parent
LEDGER_DIR = BASE_DIR / 'LEDGER'
ALPHA_STAGING = LEDGER_DIR / 'ALPHA_STAGING.csv'
CACHE_DIR = BASE_DIR / 'AUTOMATIONS' / 'daily_research' / '.cache'

# HN API endpoints
HN_API_BASE = "https://hacker-news.firebaseio.com/v0"


@dataclass
class HNItem:
    """Represents a Hacker News item"""
    id: int
    type: str  # story, comment, job, poll
    title: str
    url: Optional[str]
    text: Optional[str]
    score: int
    by: str
    time: int
    descendants: int  # comment count


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

    def __init__(self, calls_per_minute: int = 60):
        self.calls_per_minute = calls_per_minute
        self.call_times = []

    def wait_if_needed(self):
        now = time.time()
        self.call_times = [t for t in self.call_times if now - t < 60]

        if len(self.call_times) >= self.calls_per_minute:
            wait_time = 60 - (now - self.call_times[0])
            if wait_time > 0:
                logger.debug(f"Rate limit reached. Waiting {wait_time:.1f}s...")
                time.sleep(wait_time + random.uniform(0.1, 0.5))

        self.call_times.append(time.time())


class HNScanner:
    """Scans Hacker News for alpha"""

    def __init__(self):
        self.rate_limiter = RateLimiter(calls_per_minute=60)
        CACHE_DIR.mkdir(parents=True, exist_ok=True)
        self.seen_ids = self._load_seen_ids()

        # Keywords relevant to PRINTMAXX niches
        self.relevant_keywords = [
            # Solopreneur/indie
            'indie', 'solopreneur', 'solo founder', 'bootstrap', 'side project',
            'saas', 'mrr', 'arr', 'revenue', 'launched', 'shipped',
            # Growth
            'seo', 'marketing', 'growth', 'traffic', 'conversion', 'viral',
            'acquisition', 'retention', 'monetization',
            # AI/automation
            'ai', 'automation', 'llm', 'chatgpt', 'claude', 'gpt', 'agents',
            'workflow', 'n8n', 'zapier',
            # Apps
            'app', 'mobile', 'ios', 'android', 'react native', 'flutter',
            'subscription', 'paywall',
            # Content
            'content', 'newsletter', 'email', 'creator', 'influencer',
            # Niches
            'fitness', 'health', 'faith', 'prayer', 'meditation'
        ]

    def _load_seen_ids(self) -> set:
        cache_file = CACHE_DIR / 'seen_hn.json'
        if cache_file.exists():
            try:
                with open(cache_file, 'r') as f:
                    data = json.load(f)
                    cutoff = (datetime.now() - timedelta(days=7)).isoformat()
                    return {int(k) for k, v in data.items() if v > cutoff}
            except Exception as e:
                logger.warning(f"Failed to load seen IDs: {e}")
        return set()

    def _save_seen_ids(self):
        cache_file = CACHE_DIR / 'seen_hn.json'
        try:
            existing = {}
            if cache_file.exists():
                with open(cache_file, 'r') as f:
                    existing = json.load(f)

            now = datetime.now().isoformat()
            for item_id in self.seen_ids:
                if str(item_id) not in existing:
                    existing[str(item_id)] = now

            cutoff = (datetime.now() - timedelta(days=7)).isoformat()
            existing = {k: v for k, v in existing.items() if v > cutoff}

            with open(cache_file, 'w') as f:
                json.dump(existing, f)
        except Exception as e:
            logger.warning(f"Failed to save seen IDs: {e}")

    def _fetch_json(self, url: str) -> Optional[dict]:
        """Fetch JSON from URL with rate limiting"""
        try:
            import requests

            self.rate_limiter.wait_if_needed()

            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                return response.json()
            else:
                logger.warning(f"Failed to fetch {url}: {response.status_code}")
                return None
        except Exception as e:
            logger.error(f"Error fetching {url}: {e}")
            return None

    def get_top_stories(self, count: int = 30) -> List[int]:
        """Get IDs of top stories"""
        url = f"{HN_API_BASE}/topstories.json"
        data = self._fetch_json(url)
        return data[:count] if data else []

    def get_best_stories(self, count: int = 30) -> List[int]:
        """Get IDs of best stories"""
        url = f"{HN_API_BASE}/beststories.json"
        data = self._fetch_json(url)
        return data[:count] if data else []

    def get_new_stories(self, count: int = 30) -> List[int]:
        """Get IDs of new stories"""
        url = f"{HN_API_BASE}/newstories.json"
        data = self._fetch_json(url)
        return data[:count] if data else []

    def get_show_hn(self, count: int = 20) -> List[int]:
        """Get IDs of Show HN stories"""
        url = f"{HN_API_BASE}/showstories.json"
        data = self._fetch_json(url)
        return data[:count] if data else []

    def get_item(self, item_id: int) -> Optional[HNItem]:
        """Get a single HN item by ID"""
        if item_id in self.seen_ids:
            return None

        url = f"{HN_API_BASE}/item/{item_id}.json"
        data = self._fetch_json(url)

        if not data:
            return None

        self.seen_ids.add(item_id)

        return HNItem(
            id=data.get('id'),
            type=data.get('type', 'story'),
            title=data.get('title', ''),
            url=data.get('url'),
            text=data.get('text', ''),
            score=data.get('score', 0),
            by=data.get('by', 'unknown'),
            time=data.get('time', 0),
            descendants=data.get('descendants', 0)
        )

    def is_relevant(self, item: HNItem) -> bool:
        """Check if an item is relevant to PRINTMAXX"""
        content = f"{item.title} {item.text or ''}".lower()

        # Check for relevant keywords
        for keyword in self.relevant_keywords:
            if keyword in content:
                return True

        # Also include high-scoring items (400+ points) as they indicate trends
        if item.score >= 400:
            return True

        return False

    def analyze_item_for_alpha(self, item: HNItem) -> Optional[AlphaFinding]:
        """Analyze an HN item for alpha"""
        content = f"{item.title} {item.text or ''}".lower()

        # Categorize based on content
        category = 'GROWTH_HACK'  # Default

        category_keywords = {
            'APP_FACTORY': ['app', 'mobile', 'ios', 'android', 'launched', 'shipped', 'saas'],
            'MONETIZATION': ['revenue', 'mrr', 'arr', '$', 'monetize', 'pricing', 'subscription'],
            'TOOL_ALPHA': ['tool', 'api', 'service', 'platform', 'built', 'open source'],
            'CONTENT_FORMAT': ['content', 'newsletter', 'blog', 'youtube', 'tiktok', 'viral'],
            'OUTBOUND': ['email', 'outreach', 'cold', 'sales', 'b2b'],
            'GROWTH_HACK': ['growth', 'marketing', 'seo', 'traffic', 'acquisition']
        }

        for cat, keywords in category_keywords.items():
            if any(kw in content for kw in keywords):
                category = cat
                break

        # Determine effort level
        effort_level = 'MEDIUM'
        if any(word in content for word in ['simple', 'easy', 'quick', 'weekend', 'hour']):
            effort_level = 'LOW'
        elif any(word in content for word in ['complex', 'years', 'team', 'enterprise', 'scale']):
            effort_level = 'HIGH'

        # Determine ROI potential based on score and content
        roi_potential = 'MEDIUM'
        if item.score >= 500:
            roi_potential = 'HIGHEST'
        elif item.score >= 200:
            roi_potential = 'HIGH'

        # Check for numbers in content
        import re
        if re.search(r'\$\d{4,}|[1-9]\d*[kKmM]', content):
            roi_potential = 'HIGHEST' if roi_potential != 'HIGHEST' else roi_potential

        alpha_id = f"ALPHN{str(item.id)[-6:]}"

        description = item.title
        if item.text:
            description += f" - {item.text[:300]}"
        if item.url:
            description += f" (Link: {item.url})"

        hn_url = f"https://news.ycombinator.com/item?id={item.id}"

        return AlphaFinding(
            alpha_id=alpha_id,
            source='Hacker News',
            source_url=hn_url,
            category=category,
            title=item.title[:100],
            description=description[:500],
            actionable_steps='Review HN discussion for tactics and insights',
            effort_level=effort_level,
            roi_potential=roi_potential,
            risk_level='LOW',
            applies_to_niches='ALL',
            status='PENDING_REVIEW'
        )

    def scan_all(self, count: int = 30, dry_run: bool = False) -> List[AlphaFinding]:
        """Scan HN for alpha"""
        logger.info("Scanning Hacker News...")

        # Collect story IDs from different endpoints
        all_ids = set()

        logger.info("  Fetching top stories...")
        all_ids.update(self.get_top_stories(count))

        logger.info("  Fetching best stories...")
        all_ids.update(self.get_best_stories(count))

        logger.info("  Fetching Show HN...")
        all_ids.update(self.get_show_hn(20))

        logger.info(f"  Found {len(all_ids)} unique stories to check")

        all_findings = []

        for item_id in all_ids:
            item = self.get_item(item_id)
            if not item:
                continue

            if not self.is_relevant(item):
                continue

            finding = self.analyze_item_for_alpha(item)
            if finding:
                all_findings.append(finding)
                logger.info(f"  Found alpha: {finding.title[:50]}... (score: {item.score})")

        if not dry_run:
            self._save_seen_ids()

        logger.info(f"  Found {len(all_findings)} potential alpha items")
        return all_findings

    def save_findings(self, findings: List[AlphaFinding]) -> int:
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
            logger.info("No new findings to save")
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

        logger.info(f"Saved {len(new_findings)} new findings")
        return len(new_findings)


def main():
    parser = argparse.ArgumentParser(description='Scan Hacker News for alpha')
    parser.add_argument('--dry-run', action='store_true', help='Preview without saving')
    parser.add_argument('--count', type=int, default=30, help='Number of stories to check per category')
    args = parser.parse_args()

    scanner = HNScanner()
    findings = scanner.scan_all(count=args.count, dry_run=args.dry_run)

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
