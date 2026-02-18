#!/usr/bin/env python3
"""
Daily Twitter/X Timeline Scraper for Alpha Research

Scrapes HIGHEST-tier X accounts from HIGH_SIGNAL_SOURCES.csv
Extracts actionable alpha and appends to ALPHA_STAGING.csv

Usage:
    python3 daily_timeline_scraper.py [--dry-run] [--tier HIGHEST|HIGH|MEDIUM] [--headless]

Example:
    python3 daily_timeline_scraper.py --tier HIGHEST --headless
"""

import asyncio
import csv
import json
import logging
import os
import random
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional
import argparse

# Add parent directories to path
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from source_scrapers.twitter_scraper import TwitterScraper
    from daily_research.twitter_scanner import TwitterScanner, Tweet, AlphaFinding
except ImportError:
    print("Error: Could not import required modules.")
    print("Make sure you're running from AUTOMATIONS/scripts/ directory")
    print("and that twitter_scraper.py and twitter_scanner.py exist")
    sys.exit(1)

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('AUTOMATIONS/logs/daily_scraper.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('daily_timeline_scraper')

# Paths
BASE_DIR = Path(__file__).parent.parent.parent
LEDGER_DIR = BASE_DIR / 'LEDGER'
HIGH_SIGNAL_SOURCES = LEDGER_DIR / 'HIGH_SIGNAL_SOURCES.csv'
ALPHA_STAGING = LEDGER_DIR / 'ALPHA_STAGING.csv'
METRICS_FILE = BASE_DIR / 'AUTOMATIONS' / 'logs' / 'scraper_metrics.json'


def get_proxy_config() -> Optional[dict]:
    """
    Get proxy configuration from environment variables.

    Set these in .env:
    - SOAX_USERNAME (or SMARTPROXY_USERNAME)
    - SOAX_PASSWORD (or SMARTPROXY_PASSWORD)
    """
    proxy_user = os.getenv('SOAX_USERNAME') or os.getenv('SMARTPROXY_USERNAME')
    proxy_pass = os.getenv('SOAX_PASSWORD') or os.getenv('SMARTPROXY_PASSWORD')

    if not proxy_user or not proxy_pass:
        logger.warning("No proxy credentials found. Running without proxy (may hit rate limits)")
        return None

    # Soax residential proxy with sticky 30-min session
    # Format: user-residential-country-US-sessionduration-30:password@proxy.soax.com:9000
    return {
        'server': 'http://proxy.soax.com:9000',
        'username': f'user-residential-country-US-sessionduration-30',
        'password': proxy_pass
    }


async def scrape_high_signal_accounts(
    tier_filter: Optional[str] = 'HIGHEST',
    headless: bool = True,
    max_tweets_per_account: int = 20,
    dry_run: bool = False
):
    """
    Scrape timelines of high-signal X accounts.

    Args:
        tier_filter: Filter by signal quality (HIGHEST, HIGH, MEDIUM, or None for all)
        headless: Run browser in headless mode
        max_tweets_per_account: Maximum tweets to scrape per account
        dry_run: Preview without saving to ALPHA_STAGING.csv

    Returns:
        List of AlphaFinding objects
    """
    start_time = datetime.now()

    # Initialize scanner and get sources
    scanner = TwitterScanner()
    sources = scanner.get_x_sources(tier_filter=tier_filter)

    if not sources:
        logger.error(f"No sources found with tier={tier_filter}")
        return []

    logger.info(f"Starting scrape of {len(sources)} accounts (tier={tier_filter})")

    # Initialize scraper with proxy
    proxy_config = get_proxy_config()
    scraper = TwitterScraper(
        headless=headless,
        proxy_config=proxy_config,
        timeout=30000
    )

    all_tweets = []
    failed_accounts = []

    try:
        await scraper.initialize()
        logger.info("Scraper initialized successfully")

        for idx, source in enumerate(sources, 1):
            account_name = source['name']
            account_url = source['url']

            logger.info(f"[{idx}/{len(sources)}] Scraping {account_name}...")

            try:
                # Scrape account timeline
                tweets = await scraper.scrape_account(
                    profile_url=account_url,
                    max_tweets=max_tweets_per_account,
                    include_replies=False  # Skip replies, focus on original content
                )

                logger.info(f"  ✓ Collected {len(tweets)} tweets from {account_name}")
                all_tweets.extend(tweets)

            except Exception as e:
                logger.error(f"  ✗ Failed to scrape {account_name}: {e}")
                failed_accounts.append((account_name, str(e)))
                continue

            # Human-like delay between accounts (3-8 seconds)
            if idx < len(sources):  # Don't wait after last account
                delay = random.uniform(3, 8)
                logger.debug(f"  Waiting {delay:.1f}s before next account...")
                await asyncio.sleep(delay)

    finally:
        await scraper.close()
        logger.info("Scraper closed")

    # Analyze tweets for alpha
    logger.info(f"\nAnalyzing {len(all_tweets)} tweets for alpha signals...")
    findings = []

    for tweet in all_tweets:
        # Convert tweet dict to Tweet object for analyzer
        try:
            tweet_obj = Tweet(
                id=tweet['url'].split('/')[-1] if tweet['url'] else '',
                author=tweet['handle'],
                content=tweet['text'],
                url=tweet['url'],
                timestamp=datetime.fromisoformat(tweet['timestamp']) if tweet.get('timestamp') else datetime.now(),
                engagement={
                    'likes': tweet.get('likes', 0),
                    'retweets': tweet.get('retweets', 0),
                    'replies': tweet.get('replies', 0),
                    'views': tweet.get('views', 0)
                },
                media_urls=[]
            )

            # Find matching source info
            source_info = next(
                (s for s in sources if s['name'] == tweet['handle']),
                {'name': tweet['handle'], 'focus_area': 'Unknown', 'signal_quality': 'MEDIUM'}
            )

            # Analyze for alpha
            finding = scanner.analyze_tweet_for_alpha(tweet_obj, source_info)
            if finding:
                findings.append(finding)
                logger.info(f"  ✓ Found alpha: {finding.title[:60]}...")

        except Exception as e:
            logger.debug(f"  Error analyzing tweet: {e}")
            continue

    # Save findings
    if not dry_run:
        saved_count = scanner.save_findings(findings)
        logger.info(f"\n✓ Saved {saved_count} new alpha findings to ALPHA_STAGING.csv")
    else:
        logger.info(f"\nDRY RUN: Would save {len(findings)} findings")
        for finding in findings[:5]:  # Show first 5
            print(f"  - [{finding.category}] {finding.title[:60]}...")

    # Calculate and save metrics
    end_time = datetime.now()
    runtime = (end_time - start_time).total_seconds()

    metrics = {
        'last_run': end_time.isoformat(),
        'tier_filter': tier_filter,
        'accounts_scraped': len(sources) - len(failed_accounts),
        'accounts_failed': len(failed_accounts),
        'tweets_collected': len(all_tweets),
        'alpha_findings': len(findings),
        'alpha_saved': saved_count if not dry_run else 0,
        'runtime_seconds': int(runtime)
    }

    if not dry_run:
        METRICS_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(METRICS_FILE, 'w') as f:
            json.dump(metrics, f, indent=2)

    # Print summary
    print("\n" + "="*60)
    print("SCRAPING SUMMARY")
    print("="*60)
    print(f"Accounts scraped: {metrics['accounts_scraped']}/{len(sources)}")
    print(f"Tweets collected: {metrics['tweets_collected']}")
    print(f"Alpha findings: {metrics['alpha_findings']}")
    if not dry_run:
        print(f"New alpha saved: {saved_count}")
    print(f"Runtime: {runtime:.1f}s ({runtime/60:.1f} min)")

    if failed_accounts:
        print(f"\nFailed accounts ({len(failed_accounts)}):")
        for name, error in failed_accounts:
            print(f"  - {name}: {error[:60]}...")

    print("="*60)

    return findings


def main():
    parser = argparse.ArgumentParser(
        description='Scrape X/Twitter timelines for alpha research'
    )
    parser.add_argument(
        '--tier',
        choices=['HIGHEST', 'HIGH', 'MEDIUM'],
        default='HIGHEST',
        help='Filter accounts by signal quality tier'
    )
    parser.add_argument(
        '--headless',
        action='store_true',
        default=True,
        help='Run browser in headless mode (default: True)'
    )
    parser.add_argument(
        '--visible',
        action='store_true',
        help='Run browser in visible mode (for debugging)'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Preview findings without saving to ALPHA_STAGING.csv'
    )
    parser.add_argument(
        '--max-tweets',
        type=int,
        default=20,
        help='Maximum tweets to scrape per account (default: 20)'
    )

    args = parser.parse_args()

    # Handle headless flag
    headless = args.headless and not args.visible

    logger.info("="*60)
    logger.info("DAILY TWITTER TIMELINE SCRAPER")
    logger.info("="*60)
    logger.info(f"Tier: {args.tier}")
    logger.info(f"Headless: {headless}")
    logger.info(f"Dry run: {args.dry_run}")
    logger.info(f"Max tweets per account: {args.max_tweets}")
    logger.info("="*60 + "\n")

    # Run scraper
    findings = asyncio.run(
        scrape_high_signal_accounts(
            tier_filter=args.tier,
            headless=headless,
            max_tweets_per_account=args.max_tweets,
            dry_run=args.dry_run
        )
    )

    if not args.dry_run and findings:
        print(f"\n✓ Review new findings in: {ALPHA_STAGING}")
        print("  Status: PENDING_REVIEW")
        print("  Next: Review and approve/reject in LEDGER/ALPHA_STAGING.csv")

    return 0


if __name__ == '__main__':
    sys.exit(main())
