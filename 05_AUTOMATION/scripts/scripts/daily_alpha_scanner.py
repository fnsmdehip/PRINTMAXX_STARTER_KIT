#!/usr/bin/env python3
"""
Daily Alpha Scanner - Main Orchestrator
Scans HIGH_SIGNAL_SOURCES.csv accounts across platforms.
Extracts new tactics/tools, scores by engagement and relevance.
Outputs to ALPHA_STAGING.csv for human review.

Usage:
    python3 daily_alpha_scanner.py                    # Full scan (all auto_monitor sources)
    python3 daily_alpha_scanner.py --platform X       # Scan only X/Twitter
    python3 daily_alpha_scanner.py --platform Reddit  # Scan only Reddit
    python3 daily_alpha_scanner.py --platform HN      # Scan only HackerNews
    python3 daily_alpha_scanner.py --tier HIGHEST     # Only HIGHEST signal sources
    python3 daily_alpha_scanner.py --dry-run          # Preview without scraping
    python3 daily_alpha_scanner.py --max 10           # Limit sources processed
    python3 daily_alpha_scanner.py --report-only      # Generate report from existing staging
"""

import argparse
import asyncio
import csv
import json
import logging
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

# Add parent directory for imports
sys.path.insert(0, str(Path(__file__).parent))

from source_scrapers.twitter_scraper import TwitterScraper
from source_scrapers.reddit_scraper import RedditScraper
from source_scrapers.hackernews_scraper import HackerNewsScraper
from alpha_processor import AlphaProcessor
from daily_report_generator import DailyReportGenerator

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(Path(__file__).parent.parent.parent / 'OPS' / 'logs' / 'alpha_scanner.log')
    ]
)
logger = logging.getLogger('AlphaScanner')

# Paths
BASE_DIR = Path(__file__).parent.parent.parent
LEDGER_DIR = BASE_DIR / 'LEDGER'
OPS_DIR = BASE_DIR / 'OPS'
HIGH_SIGNAL_FILE = LEDGER_DIR / 'HIGH_SIGNAL_SOURCES.csv'
ALPHA_STAGING_FILE = LEDGER_DIR / 'ALPHA_STAGING.csv'
REPORTS_DIR = OPS_DIR / 'reports'


class DailyAlphaScanner:
    """Main orchestrator for daily alpha research scanning."""

    def __init__(
        self,
        platform_filter: Optional[str] = None,
        tier_filter: Optional[str] = None,
        max_sources: Optional[int] = None,
        dry_run: bool = False,
        headless: bool = True,
        proxy_config: Optional[dict] = None
    ):
        self.platform_filter = platform_filter
        self.tier_filter = tier_filter
        self.max_sources = max_sources
        self.dry_run = dry_run
        self.headless = headless
        self.proxy_config = proxy_config or {}

        # Initialize components
        self.processor = AlphaProcessor()
        self.report_generator = DailyReportGenerator()

        # Scrapers (initialized lazily)
        self._twitter_scraper = None
        self._reddit_scraper = None
        self._hn_scraper = None

        # Results tracking
        self.scan_results = {
            'sources_scanned': 0,
            'findings': [],
            'errors': [],
            'skipped': [],
            'started_at': None,
            'completed_at': None
        }

    @property
    def twitter_scraper(self):
        if self._twitter_scraper is None:
            self._twitter_scraper = TwitterScraper(
                headless=self.headless,
                proxy_config=self.proxy_config.get('twitter', {})
            )
        return self._twitter_scraper

    @property
    def reddit_scraper(self):
        if self._reddit_scraper is None:
            self._reddit_scraper = RedditScraper(
                headless=self.headless,
                proxy_config=self.proxy_config.get('reddit', {})
            )
        return self._reddit_scraper

    @property
    def hn_scraper(self):
        if self._hn_scraper is None:
            self._hn_scraper = HackerNewsScraper(
                headless=self.headless
            )
        return self._hn_scraper

    def load_sources(self) -> list[dict]:
        """Load sources from HIGH_SIGNAL_SOURCES.csv with filters applied."""
        sources = []

        if not HIGH_SIGNAL_FILE.exists():
            logger.error(f"HIGH_SIGNAL_SOURCES.csv not found at {HIGH_SIGNAL_FILE}")
            return sources

        with open(HIGH_SIGNAL_FILE, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Only auto_monitor=TRUE
                if row.get('auto_monitor', '').upper() != 'TRUE':
                    continue

                platform = row.get('platform', '')

                # Map platforms to our scraper categories
                platform_map = {
                    'X': 'X',
                    'Reddit': 'Reddit',
                    'Web': 'Web',
                    'YouTube': 'YouTube',
                    'Email': 'Email',
                    'Podcast': 'Podcast'
                }

                normalized_platform = platform_map.get(platform, platform)

                # Apply platform filter
                if self.platform_filter:
                    if self.platform_filter == 'HN':
                        # HackerNews is a special case, not in sources file
                        continue
                    if normalized_platform != self.platform_filter:
                        continue

                # Apply tier filter
                if self.tier_filter:
                    if row.get('signal_quality') != self.tier_filter:
                        continue

                sources.append({
                    'id': row.get('source_id', ''),
                    'name': row.get('source_name', ''),
                    'platform': normalized_platform,
                    'url': row.get('url', ''),
                    'focus_area': row.get('focus_area', ''),
                    'signal_quality': row.get('signal_quality', ''),
                    'notes': row.get('notes', '')
                })

        # Apply max limit
        if self.max_sources:
            sources = sources[:self.max_sources]

        return sources

    def load_existing_urls(self) -> set:
        """Load existing URLs from ALPHA_STAGING to avoid duplicates."""
        existing = set()

        if not ALPHA_STAGING_FILE.exists():
            return existing

        with open(ALPHA_STAGING_FILE, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                url = row.get('source_url', '')
                if url:
                    existing.add(url)

        return existing

    async def scan_twitter_sources(self, sources: list[dict], existing_urls: set) -> list[dict]:
        """Scan all Twitter/X sources."""
        twitter_sources = [s for s in sources if s['platform'] == 'X']
        if not twitter_sources:
            return []

        logger.info(f"Scanning {len(twitter_sources)} X/Twitter sources...")

        findings = []
        try:
            await self.twitter_scraper.initialize()

            for source in twitter_sources:
                try:
                    logger.info(f"  Scanning {source['name']}...")
                    tweets = await self.twitter_scraper.scrape_account(
                        source['url'],
                        max_tweets=10
                    )

                    for tweet in tweets:
                        if tweet.get('url') in existing_urls:
                            continue

                        finding = {
                            'source': source['name'],
                            'source_url': tweet.get('url', ''),
                            'platform': 'X',
                            'content': tweet.get('text', ''),
                            'engagement': {
                                'likes': tweet.get('likes', 0),
                                'retweets': tweet.get('retweets', 0),
                                'replies': tweet.get('replies', 0),
                                'views': tweet.get('views', 0)
                            },
                            'timestamp': tweet.get('timestamp', ''),
                            'focus_area': source['focus_area'],
                            'signal_tier': source['signal_quality']
                        }
                        findings.append(finding)
                        existing_urls.add(tweet.get('url', ''))

                    self.scan_results['sources_scanned'] += 1

                except Exception as e:
                    logger.error(f"  Error scanning {source['name']}: {e}")
                    self.scan_results['errors'].append({
                        'source': source['name'],
                        'error': str(e)
                    })

                # Rate limiting between accounts
                await asyncio.sleep(3)

        finally:
            await self.twitter_scraper.close()

        return findings

    async def scan_reddit_sources(self, sources: list[dict], existing_urls: set) -> list[dict]:
        """Scan all Reddit sources."""
        reddit_sources = [s for s in sources if s['platform'] == 'Reddit']
        if not reddit_sources:
            return []

        logger.info(f"Scanning {len(reddit_sources)} Reddit sources...")

        findings = []
        try:
            await self.reddit_scraper.initialize()

            for source in reddit_sources:
                try:
                    logger.info(f"  Scanning {source['name']}...")
                    posts = await self.reddit_scraper.scrape_subreddit(
                        source['url'],
                        max_posts=10,
                        sort='hot'
                    )

                    for post in posts:
                        if post.get('url') in existing_urls:
                            continue

                        finding = {
                            'source': source['name'],
                            'source_url': post.get('url', ''),
                            'platform': 'Reddit',
                            'content': f"{post.get('title', '')}\n\n{post.get('body', '')}",
                            'engagement': {
                                'upvotes': post.get('upvotes', 0),
                                'comments': post.get('comments', 0),
                                'upvote_ratio': post.get('upvote_ratio', 0)
                            },
                            'timestamp': post.get('timestamp', ''),
                            'focus_area': source['focus_area'],
                            'signal_tier': source['signal_quality']
                        }
                        findings.append(finding)
                        existing_urls.add(post.get('url', ''))

                    self.scan_results['sources_scanned'] += 1

                except Exception as e:
                    logger.error(f"  Error scanning {source['name']}: {e}")
                    self.scan_results['errors'].append({
                        'source': source['name'],
                        'error': str(e)
                    })

                # Rate limiting
                await asyncio.sleep(5)

        finally:
            await self.reddit_scraper.close()

        return findings

    async def scan_hackernews(self, existing_urls: set) -> list[dict]:
        """Scan HackerNews front page and Show HN."""
        if self.platform_filter and self.platform_filter not in ['HN', None]:
            return []

        logger.info("Scanning HackerNews...")

        findings = []
        try:
            await self.hn_scraper.initialize()

            # Scan front page
            logger.info("  Scanning front page...")
            front_page = await self.hn_scraper.scrape_front_page(
                min_points=50,
                max_items=30
            )

            for item in front_page:
                if item.get('url') in existing_urls:
                    continue

                finding = {
                    'source': 'HackerNews',
                    'source_url': item.get('url', ''),
                    'platform': 'HN',
                    'content': item.get('title', ''),
                    'engagement': {
                        'points': item.get('points', 0),
                        'comments': item.get('comments', 0)
                    },
                    'timestamp': item.get('timestamp', ''),
                    'focus_area': 'Tech trends',
                    'signal_tier': 'HIGH'
                }
                findings.append(finding)
                existing_urls.add(item.get('url', ''))

            # Scan Show HN
            logger.info("  Scanning Show HN...")
            show_hn = await self.hn_scraper.scrape_show_hn(
                min_points=20,
                max_items=20
            )

            for item in show_hn:
                if item.get('url') in existing_urls:
                    continue

                finding = {
                    'source': 'HackerNews Show HN',
                    'source_url': item.get('url', ''),
                    'platform': 'HN',
                    'content': item.get('title', ''),
                    'engagement': {
                        'points': item.get('points', 0),
                        'comments': item.get('comments', 0)
                    },
                    'timestamp': item.get('timestamp', ''),
                    'focus_area': 'New tools/launches',
                    'signal_tier': 'HIGH'
                }
                findings.append(finding)
                existing_urls.add(item.get('url', ''))

            self.scan_results['sources_scanned'] += 2  # Front page + Show HN

        except Exception as e:
            logger.error(f"Error scanning HackerNews: {e}")
            self.scan_results['errors'].append({
                'source': 'HackerNews',
                'error': str(e)
            })
        finally:
            await self.hn_scraper.close()

        return findings

    async def run_scan(self) -> dict:
        """Execute the full alpha scan."""
        self.scan_results['started_at'] = datetime.now().isoformat()

        logger.info("=" * 60)
        logger.info("DAILY ALPHA SCANNER")
        logger.info(f"Started: {self.scan_results['started_at']}")
        logger.info("=" * 60)

        # Load sources and existing URLs
        sources = self.load_sources()
        existing_urls = self.load_existing_urls()

        logger.info(f"Loaded {len(sources)} sources to scan")
        logger.info(f"Existing alpha entries: {len(existing_urls)}")

        if self.dry_run:
            logger.info("\n[DRY RUN MODE] - Would scan the following sources:")
            for source in sources:
                logger.info(f"  - {source['name']} ({source['platform']})")
            return self.scan_results

        all_findings = []

        # Scan each platform
        twitter_findings = await self.scan_twitter_sources(sources, existing_urls)
        all_findings.extend(twitter_findings)
        logger.info(f"Twitter findings: {len(twitter_findings)}")

        reddit_findings = await self.scan_reddit_sources(sources, existing_urls)
        all_findings.extend(reddit_findings)
        logger.info(f"Reddit findings: {len(reddit_findings)}")

        # Always scan HN unless explicitly filtered to another platform
        if not self.platform_filter or self.platform_filter == 'HN':
            hn_findings = await self.scan_hackernews(existing_urls)
            all_findings.extend(hn_findings)
            logger.info(f"HackerNews findings: {len(hn_findings)}")

        # Process findings
        logger.info(f"\nProcessing {len(all_findings)} raw findings...")
        processed = self.processor.process_findings(all_findings)

        logger.info(f"After processing: {len(processed)} findings staged")

        # Save to staging
        if processed:
            self.processor.save_to_staging(processed, ALPHA_STAGING_FILE)
            logger.info(f"Saved to {ALPHA_STAGING_FILE}")

        self.scan_results['findings'] = processed
        self.scan_results['completed_at'] = datetime.now().isoformat()

        # Generate report
        REPORTS_DIR.mkdir(parents=True, exist_ok=True)
        report_path = self.report_generator.generate_report(
            self.scan_results,
            REPORTS_DIR
        )
        logger.info(f"Report saved to {report_path}")

        # Summary
        logger.info("\n" + "=" * 60)
        logger.info("SCAN COMPLETE")
        logger.info(f"Sources scanned: {self.scan_results['sources_scanned']}")
        logger.info(f"Findings staged: {len(processed)}")
        logger.info(f"Errors: {len(self.scan_results['errors'])}")
        logger.info("=" * 60)

        return self.scan_results


def load_proxy_config() -> dict:
    """Load proxy configuration from environment or config file."""
    config = {}

    # Try environment variables first
    if os.getenv('PROXY_HOST'):
        config['twitter'] = {
            'server': f"{os.getenv('PROXY_HOST')}:{os.getenv('PROXY_PORT', '8080')}",
            'username': os.getenv('PROXY_USER', ''),
            'password': os.getenv('PROXY_PASS', '')
        }
        config['reddit'] = config['twitter'].copy()

    # Try config file
    config_file = BASE_DIR / 'AUTOMATIONS' / 'proxy_config.json'
    if config_file.exists():
        with open(config_file, 'r') as f:
            file_config = json.load(f)
            config.update(file_config)

    return config


def main():
    parser = argparse.ArgumentParser(
        description='Daily Alpha Scanner - Multi-Platform Research System',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python3 daily_alpha_scanner.py                    # Full scan
    python3 daily_alpha_scanner.py --platform X       # Twitter only
    python3 daily_alpha_scanner.py --tier HIGHEST     # Top sources only
    python3 daily_alpha_scanner.py --dry-run          # Preview mode
    python3 daily_alpha_scanner.py --max 5 --debug    # Limited debug scan
        """
    )

    parser.add_argument(
        '--platform',
        choices=['X', 'Reddit', 'HN', 'Web'],
        help='Filter by platform'
    )
    parser.add_argument(
        '--tier',
        choices=['HIGHEST', 'HIGH', 'MEDIUM'],
        help='Filter by signal tier'
    )
    parser.add_argument(
        '--max',
        type=int,
        help='Maximum sources to process'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Preview mode - no actual scraping'
    )
    parser.add_argument(
        '--report-only',
        action='store_true',
        help='Generate report from existing staging data'
    )
    parser.add_argument(
        '--headless',
        action='store_true',
        default=True,
        help='Run browser in headless mode (default: True)'
    )
    parser.add_argument(
        '--no-headless',
        action='store_true',
        help='Show browser window during scraping'
    )
    parser.add_argument(
        '--debug',
        action='store_true',
        help='Enable debug logging'
    )

    args = parser.parse_args()

    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)

    # Report-only mode
    if args.report_only:
        generator = DailyReportGenerator()
        REPORTS_DIR.mkdir(parents=True, exist_ok=True)

        # Load existing staging data
        processor = AlphaProcessor()
        findings = []
        if ALPHA_STAGING_FILE.exists():
            with open(ALPHA_STAGING_FILE, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                findings = list(reader)

        results = {
            'sources_scanned': 0,
            'findings': findings,
            'errors': [],
            'started_at': datetime.now().isoformat(),
            'completed_at': datetime.now().isoformat()
        }

        report_path = generator.generate_report(results, REPORTS_DIR)
        print(f"Report generated: {report_path}")
        return

    # Load proxy config
    proxy_config = load_proxy_config()

    # Create and run scanner
    scanner = DailyAlphaScanner(
        platform_filter=args.platform,
        tier_filter=args.tier,
        max_sources=args.max,
        dry_run=args.dry_run,
        headless=not args.no_headless,
        proxy_config=proxy_config
    )

    # Run async scan
    asyncio.run(scanner.run_scan())


if __name__ == '__main__':
    main()
