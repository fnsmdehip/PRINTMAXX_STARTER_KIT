#!/usr/bin/env python3
"""
Tweet Scraper - Extract tweets from HIGH_SIGNAL_SOURCES.csv accounts
Uses Playwright for browser automation (no API key required for public profiles)

Usage:
    python scrape_tweets.py                      # Scrape all X accounts from HIGH_SIGNAL_SOURCES.csv
    python scrape_tweets.py --handles @levelsio @tdinh_me  # Specific accounts
    python scrape_tweets.py --tier HIGHEST       # Only HIGHEST signal accounts
    python scrape_tweets.py --max 5              # Limit to 5 accounts
    python scrape_tweets.py --output tweets.csv  # Custom output file
    python scrape_tweets.py --headless           # Run without browser window

Environment Variables:
    LEDGER_DIR: Path to LEDGER directory (default: ../LEDGER)

Output:
    CSV file with columns: handle, tweet_id, text, likes, retweets, replies, timestamp, url
"""

import argparse
import asyncio
import csv
import json
import os
import re
import time
from datetime import datetime
from pathlib import Path
from typing import Optional

try:
    from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeout
except ImportError:
    print("ERROR: playwright not installed. Run: pip install playwright && playwright install")
    exit(1)


# Paths
BASE_DIR = Path(__file__).parent.parent.parent
LEDGER_DIR = Path(os.getenv("LEDGER_DIR", BASE_DIR / "LEDGER"))
HIGH_SIGNAL_FILE = LEDGER_DIR / "HIGH_SIGNAL_SOURCES.csv"
DEFAULT_OUTPUT = LEDGER_DIR / "SCRAPED_TWEETS.csv"


def load_x_accounts(
    tier_filter: Optional[str] = None,
    handles_filter: Optional[list] = None,
    max_accounts: Optional[int] = None
) -> list[dict]:
    """Load X/Twitter accounts from HIGH_SIGNAL_SOURCES.csv"""
    accounts = []

    if not HIGH_SIGNAL_FILE.exists():
        print(f"ERROR: {HIGH_SIGNAL_FILE} not found")
        return accounts

    with open(HIGH_SIGNAL_FILE, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Only X/Twitter accounts with auto_monitor=TRUE
            if row.get("platform") != "X":
                continue
            if row.get("auto_monitor", "").upper() != "TRUE":
                continue

            # Apply tier filter
            if tier_filter and row.get("signal_quality") != tier_filter:
                continue

            # Extract handle from source_name or URL
            handle = row.get("source_name", "")
            if not handle.startswith("@"):
                url = row.get("url", "")
                match = re.search(r"x\.com/(@?\w+)", url)
                if match:
                    handle = "@" + match.group(1).lstrip("@")

            # Apply handles filter
            if handles_filter:
                if handle not in handles_filter and handle.lstrip("@") not in [h.lstrip("@") for h in handles_filter]:
                    continue

            accounts.append({
                "id": row.get("source_id"),
                "handle": handle,
                "url": row.get("url"),
                "focus": row.get("focus_area"),
                "signal": row.get("signal_quality"),
            })

    if max_accounts:
        accounts = accounts[:max_accounts]

    return accounts


async def scrape_account_tweets(page, handle: str, max_tweets: int = 10) -> list[dict]:
    """Scrape recent tweets from an X profile"""
    tweets = []
    clean_handle = handle.lstrip("@")
    profile_url = f"https://x.com/{clean_handle}"

    try:
        # Navigate to profile
        await page.goto(profile_url, wait_until="networkidle", timeout=30000)
        await asyncio.sleep(3)  # Wait for dynamic content

        # Check if profile exists
        if "This account doesn't exist" in await page.content():
            print(f"  Account @{clean_handle} not found")
            return tweets

        # Scroll to load more tweets
        for _ in range(2):
            await page.evaluate("window.scrollBy(0, 1000)")
            await asyncio.sleep(1)

        # Extract tweets using JavaScript
        tweets_data = await page.evaluate("""
            () => {
                const tweets = document.querySelectorAll('[data-testid="tweet"]');
                const results = [];

                for (let i = 0; i < Math.min(tweets.length, """ + str(max_tweets) + """); i++) {
                    const tweet = tweets[i];

                    // Get tweet text
                    const textEl = tweet.querySelector('[data-testid="tweetText"]');
                    const text = textEl ? textEl.innerText : '';

                    // Get timestamp
                    const timeEl = tweet.querySelector('time');
                    const timestamp = timeEl ? timeEl.getAttribute('datetime') : '';

                    // Get tweet URL (contains tweet ID)
                    const linkEl = tweet.querySelector('a[href*="/status/"]');
                    let tweetUrl = '';
                    let tweetId = '';
                    if (linkEl) {
                        const href = linkEl.getAttribute('href');
                        tweetUrl = 'https://x.com' + href;
                        const match = href.match(/status\\/(\\d+)/);
                        if (match) tweetId = match[1];
                    }

                    // Get metrics
                    const metricsContainer = tweet.querySelector('[role="group"]');
                    let likes = 0, retweets = 0, replies = 0;

                    if (metricsContainer) {
                        const buttons = metricsContainer.querySelectorAll('[data-testid$="-count"]');
                        buttons.forEach(btn => {
                            const testId = btn.getAttribute('data-testid') || '';
                            const value = parseInt(btn.innerText.replace(/[,K]/g, '')) || 0;
                            // Handle K suffix
                            const multiplier = btn.innerText.includes('K') ? 1000 : 1;

                            if (testId.includes('reply')) replies = value * multiplier;
                            else if (testId.includes('retweet')) retweets = value * multiplier;
                            else if (testId.includes('like')) likes = value * multiplier;
                        });
                    }

                    if (text && tweetId) {
                        results.push({
                            tweet_id: tweetId,
                            text: text.substring(0, 1000),
                            timestamp: timestamp,
                            url: tweetUrl,
                            likes: likes,
                            retweets: retweets,
                            replies: replies
                        });
                    }
                }

                return results;
            }
        """)

        tweets = tweets_data or []

    except PlaywrightTimeout:
        print(f"  Timeout loading @{clean_handle}")
    except Exception as e:
        print(f"  Error scraping @{clean_handle}: {e}")

    return tweets


async def run_scraper(
    accounts: list[dict],
    output_file: Path,
    headless: bool = True,
    max_tweets_per_account: int = 10
):
    """Main scraper function"""
    all_tweets = []

    async with async_playwright() as p:
        # Launch browser
        browser = await p.chromium.launch(headless=headless)
        context = await browser.new_context(
            viewport={"width": 1280, "height": 800},
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
        )
        page = await context.new_page()

        for i, account in enumerate(accounts):
            handle = account["handle"]
            print(f"[{i+1}/{len(accounts)}] Scraping {handle}...", end=" ", flush=True)

            tweets = await scrape_account_tweets(page, handle, max_tweets_per_account)

            for tweet in tweets:
                tweet["handle"] = handle
                tweet["signal_tier"] = account["signal"]
                tweet["focus_area"] = account["focus"]
                all_tweets.append(tweet)

            print(f"Found {len(tweets)} tweets")

            # Rate limiting between accounts
            if i < len(accounts) - 1:
                await asyncio.sleep(2)

        await browser.close()

    # Save to CSV
    if all_tweets:
        fieldnames = [
            "handle", "tweet_id", "text", "likes", "retweets", "replies",
            "timestamp", "url", "signal_tier", "focus_area"
        ]

        file_exists = output_file.exists()
        existing_ids = set()

        # Load existing tweet IDs to avoid duplicates
        if file_exists:
            with open(output_file, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    existing_ids.add(row.get("tweet_id"))

        # Filter out duplicates
        new_tweets = [t for t in all_tweets if t["tweet_id"] not in existing_ids]

        if new_tweets:
            with open(output_file, "a", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                if not file_exists:
                    writer.writeheader()
                writer.writerows(new_tweets)

            print(f"\nSaved {len(new_tweets)} new tweets to {output_file}")
        else:
            print(f"\nNo new tweets to save (all {len(all_tweets)} already in file)")
    else:
        print("\nNo tweets found")

    return all_tweets


def main():
    parser = argparse.ArgumentParser(
        description="Scrape tweets from HIGH_SIGNAL_SOURCES.csv X accounts"
    )
    parser.add_argument(
        "--handles",
        nargs="+",
        help="Specific handles to scrape (e.g., @levelsio @tdinh_me)"
    )
    parser.add_argument(
        "--tier",
        choices=["HIGHEST", "HIGH", "MEDIUM"],
        help="Filter by signal tier"
    )
    parser.add_argument(
        "--max",
        type=int,
        help="Maximum number of accounts to scrape"
    )
    parser.add_argument(
        "--max-tweets",
        type=int,
        default=10,
        help="Maximum tweets per account (default: 10)"
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help=f"Output CSV file (default: {DEFAULT_OUTPUT})"
    )
    parser.add_argument(
        "--headless",
        action="store_true",
        help="Run browser in headless mode"
    )
    parser.add_argument(
        "--show-browser",
        action="store_true",
        help="Show browser window (opposite of --headless)"
    )

    args = parser.parse_args()

    # Determine headless mode
    headless = args.headless or not args.show_browser

    print("=" * 60)
    print("TWEET SCRAPER - HIGH_SIGNAL_SOURCES")
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

    # Load accounts
    accounts = load_x_accounts(
        tier_filter=args.tier,
        handles_filter=args.handles,
        max_accounts=args.max
    )

    if not accounts:
        print("No accounts found matching criteria")
        return

    print(f"\nAccounts to scrape: {len(accounts)}")
    for acc in accounts[:5]:
        print(f"  - {acc['handle']} ({acc['signal']})")
    if len(accounts) > 5:
        print(f"  ... and {len(accounts) - 5} more")

    print(f"\nOutput: {args.output}")
    print(f"Mode: {'Headless' if headless else 'Visible browser'}")
    print()

    # Run scraper
    asyncio.run(run_scraper(
        accounts=accounts,
        output_file=args.output,
        headless=headless,
        max_tweets_per_account=args.max_tweets
    ))

    print("\n" + "=" * 60)
    print("COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    main()
