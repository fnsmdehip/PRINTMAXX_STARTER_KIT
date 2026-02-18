#!/usr/bin/env python3
"""
Scrape @caiden_cole using CDP (Chrome DevTools Protocol)
Connects to already-running Chrome instance
"""

import asyncio
import json
import csv
import re
from pathlib import Path
from datetime import datetime
from playwright.async_api import async_playwright

PROJECT_DIR = Path("/Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt")
ALPHA_STAGING = PROJECT_DIR / "LEDGER" / "ALPHA_STAGING.csv"

async def scrape_caiden_cdp():
    """Scrape Caiden's tweets via CDP connection to running Chrome"""

    # Get next alpha ID
    max_id = 0
    if ALPHA_STAGING.exists():
        with open(ALPHA_STAGING, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                match = re.match(r'ALPHA(\d+)', row.get('alpha_id', ''))
                if match:
                    max_id = max(max_id, int(match.group(1)))

    next_id = max_id + 1
    print(f"📋 Next alpha ID: ALPHA{next_id}")

    # Get existing URLs to avoid duplicates
    existing_urls = set()
    if ALPHA_STAGING.exists():
        with open(ALPHA_STAGING, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row.get('source_url'):
                    existing_urls.add(row['source_url'])

    print(f"📊 Existing URLs in alpha: {len(existing_urls)}")

    async with async_playwright() as p:
        # Try to connect to already-running Chrome on default CDP port
        try:
            print("🔌 Connecting to running Chrome via CDP...")
            browser = await p.chromium.connect_over_cdp("http://localhost:9222")
            print("✅ Connected!")
        except Exception as e:
            print(f"❌ Could not connect to Chrome: {e}")
            print("💡 Start Chrome with: /Applications/Google\\ Chrome.app/Contents/MacOS/Google\\ Chrome --remote-debugging-port=9222")
            return []

        try:
            # Get the first context (should have user's session)
            contexts = browser.contexts
            if not contexts:
                print("❌ No browser contexts found")
                return []

            context = contexts[0]
            pages = context.pages

            # Create new page or use existing
            if pages:
                page = pages[0]
            else:
                page = await context.new_page()

            # Navigate to Caiden's profile
            print("🔍 Navigating to @caiden_cole...")
            await page.goto("https://x.com/caiden_cole", wait_until="networkidle", timeout=30000)
            await asyncio.sleep(3)

            # Scroll to load tweets
            print("📜 Scrolling to load tweets...")
            for i in range(10):
                await page.evaluate("window.scrollBy(0, 1000)")
                await asyncio.sleep(1)
                print(f"  Scroll {i+1}/10")

            # Extract tweets
            print("\n🎯 Extracting tweets...")
            articles = await page.query_selector_all('article[data-testid="tweet"]')
            print(f"📊 Found {len(articles)} tweet elements")

            tweets = []
            for i, article in enumerate(articles):
                try:
                    # Get tweet text
                    text_elem = await article.query_selector('[data-testid="tweetText"]')
                    if not text_elem:
                        continue

                    text = await text_elem.inner_text()

                    # Get tweet URL
                    link = await article.query_selector('a[href*="/status/"]')
                    if not link:
                        continue

                    href = await link.get_attribute('href')
                    url = f"https://x.com{href}" if href.startswith('/') else href

                    # Skip if already in alpha
                    if url in existing_urls:
                        print(f"  ⏭️  Tweet {i+1}: Already in alpha")
                        continue

                    # Get engagement
                    reply_elem = await article.query_selector('[data-testid="reply"]')
                    retweet_elem = await article.query_selector('[data-testid="retweet"]')
                    like_elem = await article.query_selector('[data-testid="like"]')

                    replies = await reply_elem.inner_text() if reply_elem else "0"
                    retweets = await retweet_elem.inner_text() if retweet_elem else "0"
                    likes = await like_elem.inner_text() if like_elem else "0"

                    tweet_data = {
                        'text': text,
                        'url': url,
                        'replies': replies,
                        'retweets': retweets,
                        'likes': likes
                    }
                    tweets.append(tweet_data)
                    print(f"  ✅ Tweet {i+1}: {text[:80]}... ({likes} likes)")

                except Exception as e:
                    print(f"  ⚠️  Error on tweet {i+1}: {e}")
                    continue

            print(f"\n✅ Scraped {len(tweets)} new tweets from @caiden_cole")

            # Save to CSV
            if tweets:
                print("\n💾 Saving to ALPHA_STAGING.csv...")

                # Read existing rows
                existing_rows = []
                if ALPHA_STAGING.exists():
                    with open(ALPHA_STAGING, 'r') as f:
                        existing_rows = list(csv.DictReader(f))

                # Get fieldnames
                if existing_rows:
                    fieldnames = list(existing_rows[0].keys())
                else:
                    fieldnames = ['alpha_id', 'source', 'source_url', 'category', 'tactic', 'roi_potential', 'priority', 'status']

                # Add new tweets
                for tweet in tweets:
                    # Categorize
                    category = 'COLD_OUTBOUND'  # Caiden's specialty
                    if any(word in tweet['text'].lower() for word in ['brandwatch', 'mention', 'monitor', 'track']):
                        category = 'TOOL_ALPHA'

                    row = {k: '' for k in fieldnames}
                    row.update({
                        'alpha_id': f'ALPHA{next_id}',
                        'source': '@caiden_cole',
                        'source_url': tweet['url'],
                        'category': category,
                        'tactic': tweet['text'][:200],
                        'roi_potential': 'HIGH' if int(tweet['likes'].replace(',', '')) > 50 else 'MEDIUM',
                        'priority': 'IMMEDIATE',
                        'status': 'PENDING_REVIEW'
                    })
                    existing_rows.append(row)
                    next_id += 1

                # Write back
                with open(ALPHA_STAGING, 'w', newline='') as f:
                    writer = csv.DictWriter(f, fieldnames=fieldnames)
                    writer.writeheader()
                    writer.writerows(existing_rows)

                print(f"✅ Saved {len(tweets)} tweets (ALPHA{next_id-len(tweets)}-ALPHA{next_id-1})")

            # Print tweets
            print("\n" + "="*80)
            print("CAIDEN'S RECENT TWEETS:")
            print("="*80)
            for i, tweet in enumerate(tweets[:10], 1):
                print(f"\n{i}. {tweet['text']}")
                print(f"   URL: {tweet['url']}")
                print(f"   💬 {tweet['replies']} | 🔄 {tweet['retweets']} | ❤️  {tweet['likes']}")

            return tweets

        except Exception as e:
            print(f"❌ Error during scraping: {e}")
            import traceback
            traceback.print_exc()
            return []

if __name__ == "__main__":
    tweets = asyncio.run(scrape_caiden_cdp())
    print(f"\n🎯 Total: {len(tweets)} tweets scraped")
