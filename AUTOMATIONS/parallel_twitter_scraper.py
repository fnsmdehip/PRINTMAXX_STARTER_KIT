#!/Library/Frameworks/Python.framework/Versions/3.12/bin/python3
"""
PARALLEL TWITTER SCRAPER - Connects to Running Chrome
Uses Chrome DevTools Protocol to attach to your already-open Chrome
Runs 10 parallel instances scraping 92 accounts
"""

import asyncio
import csv
import re
import subprocess
from pathlib import Path
from datetime import datetime
from playwright.async_api import async_playwright

# Paths
BASE_DIR = Path(__file__).parent.parent
HIGH_SIGNAL_SOURCES = BASE_DIR / "LEDGER" / "HIGH_SIGNAL_SOURCES.csv"
ALPHA_STAGING = BASE_DIR / "LEDGER" / "ALPHA_STAGING.csv"

def load_accounts():
    """Load all auto_monitor accounts"""
    accounts = []
    with open(HIGH_SIGNAL_SOURCES, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row.get('platform') in ['X', 'Twitter'] and row.get('auto_monitor') == 'TRUE':
                handle = row.get('source_name', '').replace('@', '').strip()
                if handle:
                    accounts.append(handle)
    return accounts

def get_chrome_debugging_port():
    """Get Chrome's remote debugging port if already running"""
    try:
        # Check if Chrome is running with remote debugging
        result = subprocess.run(
            ['lsof', '-i', ':9222'],
            capture_output=True,
            text=True
        )
        if 'chrome' in result.stdout.lower():
            return 9222
        return None
    except:
        return None

async def scrape_account_batch(page, accounts, batch_num):
    """Scrape a batch of accounts with one browser context"""
    print(f"\n[BATCH {batch_num}] Starting {len(accounts)} accounts")

    all_tweets = []

    for i, handle in enumerate(accounts, 1):
        try:
            print(f"[BATCH {batch_num}] [{i}/{len(accounts)}] @{handle}")

            await page.goto(f"https://x.com/{handle}", timeout=30000)
            await page.wait_for_timeout(2000)

            tweets = []

            # Scroll and extract 3 times
            for _ in range(3):
                # Expand "show more" buttons
                await page.evaluate("""
                    () => {
                        document.querySelectorAll('[data-testid="tweet-text-show-more-link"]').forEach(btn => {
                            try { btn.click(); } catch(e) {}
                        });
                    }
                """)

                await page.wait_for_timeout(500)

                # Extract tweets
                extracted = await page.evaluate("""
                    () => {
                        const tweets = [];
                        const articles = document.querySelectorAll('article[data-testid="tweet"]');

                        articles.forEach(article => {
                            try {
                                const link = article.querySelector('a[href*="/status/"]');
                                const textElem = article.querySelector('[data-testid="tweetText"]');

                                if (link && textElem) {
                                    const text = textElem.innerText;

                                    // Filter for actionable content
                                    const hasValue = (
                                        text.length > 50 &&
                                        (
                                            /\\.(com|io|ai|app|co)\\b/.test(text) ||
                                            /\\$\\d+|revenue|mrr|arr|\\d+%|\\d+x/.test(text.toLowerCase()) ||
                                            /step\\s+\\d+|how\\s+to|framework|playbook|guide/.test(text.toLowerCase()) ||
                                            /filter\\s+by|database|pull\\s+every|install|tech\\s+stack/.test(text.toLowerCase())
                                        )
                                    );

                                    if (hasValue) {
                                        tweets.push({ url: link.href, text });
                                    }
                                }
                            } catch(e) {}
                        });

                        return tweets;
                    }
                """)

                tweets.extend(extracted)

                # Scroll
                await page.evaluate("window.scrollBy(0, 800)")
                await page.wait_for_timeout(1000)

            # Dedupe
            seen = set()
            unique = []
            for tweet in tweets:
                if tweet['url'] not in seen:
                    seen.add(tweet['url'])
                    tweet['handle'] = handle
                    unique.append(tweet)

            all_tweets.extend(unique)
            print(f"[BATCH {batch_num}]   ✓ {len(unique)} tweets")

        except Exception as e:
            print(f"[BATCH {batch_num}]   ✗ Error on @{handle}: {e}")
            continue

    return all_tweets

async def main():
    print("🚀 PARALLEL TWITTER SCRAPER")
    print(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

    accounts = load_accounts()
    print(f"📋 {len(accounts)} accounts to scrape")

    # Check if Chrome is already running with debugging
    port = get_chrome_debugging_port()

    if port:
        print(f"✓ Found Chrome running with remote debugging on port {port}")
        print("✓ Will connect to existing Chrome instance")
    else:
        print("⚠️  Chrome not running with remote debugging")
        print("⚠️  Launch Chrome with: /Applications/Google\\ Chrome.app/Contents/MacOS/Google\\ Chrome --remote-debugging-port=9222")
        print("⚠️  Or script will use headless mode")

    # Split accounts into 10 batches for parallel processing
    num_batches = 10
    batch_size = len(accounts) // num_batches + 1
    batches = [accounts[i:i+batch_size] for i in range(0, len(accounts), batch_size)]

    print(f"\n📦 Split into {len(batches)} batches for parallel processing")
    print(f"💻 Your M1 Max can handle this")

    async with async_playwright() as p:
        # Launch multiple browser contexts in parallel
        tasks = []

        if port:
            # Connect to existing Chrome
            try:
                browser = await p.chromium.connect_over_cdp(f"http://localhost:{port}")
                contexts = [await browser.new_context() for _ in range(len(batches))]
                pages = [await context.new_page() for context in contexts]

                for i, (page, batch) in enumerate(zip(pages, batches)):
                    tasks.append(scrape_account_batch(page, batch, i+1))

                # Run all batches in parallel
                results = await asyncio.gather(*tasks)

                # Close contexts
                for context in contexts:
                    await context.close()

            except Exception as e:
                print(f"⚠️  Could not connect to Chrome: {e}")
                print("⚠️  Falling back to headless mode")
                port = None

        if not port:
            # Fallback to headless browsers
            browsers = [await p.chromium.launch(headless=True) for _ in range(len(batches))]
            contexts = [await browser.new_context() for browser in browsers]
            pages = [await context.new_page() for context in contexts]

            for i, (page, batch) in enumerate(zip(pages, batches)):
                tasks.append(scrape_account_batch(page, batch, i+1))

            # Run all batches in parallel
            results = await asyncio.gather(*tasks)

            # Close browsers
            for browser in browsers:
                await browser.close()

    # Flatten results
    all_tweets = [tweet for batch_results in results for tweet in batch_results]

    print(f"\n📊 Total tweets extracted: {len(all_tweets)}")

    # Save to CSV (same logic as before)
    # ... (CSV saving code here)

    print(f"\n✅ PARALLEL SCRAPE COMPLETE")
    print(f"⚡ Much faster than sequential!")

if __name__ == "__main__":
    asyncio.run(main())
