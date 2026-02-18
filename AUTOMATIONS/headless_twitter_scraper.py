#!/usr/bin/env python3
"""
HEADLESS TWITTER SCRAPER - Runs in background, no visible browser.
Uses saved session cookies from previous login.
"""

import asyncio
import csv
import os
from pathlib import Path
from datetime import datetime
from playwright.async_api import async_playwright

BASE_DIR = Path(__file__).parent.parent
HIGH_SIGNAL_SOURCES = BASE_DIR / "LEDGER" / "HIGH_SIGNAL_SOURCES.csv"
ALPHA_STAGING = BASE_DIR / "LEDGER" / "ALPHA_STAGING.csv"
CHROME_PROFILE = Path.home() / ".printmaxx-chrome-profile"

def load_accounts():
    """Load Twitter accounts to scrape"""
    accounts = []
    with open(HIGH_SIGNAL_SOURCES, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row.get('platform') in ['X', 'Twitter'] and row.get('auto_monitor') == 'TRUE':
                handle = row.get('source_name', '').replace('@', '').strip()
                if handle:
                    accounts.append(handle)
    return accounts

def get_next_alpha_id():
    """Get next alpha ID from staging file"""
    if not ALPHA_STAGING.exists():
        return "ALPHA0001"

    with open(ALPHA_STAGING, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        if len(lines) <= 1:
            return "ALPHA0001"
        last_line = lines[-1]
        try:
            last_id = last_line.split(',')[0]
            num = int(last_id.replace('ALPHA', ''))
            return f"ALPHA{num + 1:04d}"
        except:
            return "ALPHA9000"

async def scrape_account(page, handle, batch_num):
    """Scrape tweets from a single account"""
    tweets = []
    try:
        print(f"[BATCH {batch_num}] Scraping @{handle}...")
        await page.goto(f"https://x.com/{handle}", timeout=30000)
        await page.wait_for_timeout(3000)

        # Scroll and extract 3 times
        for scroll in range(3):
            # Click "show more" buttons
            try:
                await page.evaluate("""
                    () => {
                        document.querySelectorAll('[data-testid="tweet-text-show-more-link"]').forEach(btn => {
                            try { btn.click(); } catch(e) {}
                        });
                    }
                """)
            except:
                pass

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

        print(f"[BATCH {batch_num}]   Found {len(unique)} tweets from @{handle}")
        return unique

    except Exception as e:
        print(f"[BATCH {batch_num}]   Error scraping @{handle}: {e}")
        return []

async def main():
    print("=" * 60)
    print("HEADLESS TWITTER SCRAPER - Background Mode")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

    accounts = load_accounts()
    print(f"Loaded {len(accounts)} accounts to scrape")

    if not CHROME_PROFILE.exists():
        print(f"ERROR: Chrome profile not found at {CHROME_PROFILE}")
        print("Run Chrome with --user-data-dir first and log into Twitter")
        return

    all_tweets = []

    async with async_playwright() as p:
        # Launch in HEADLESS mode using saved profile
        print("\nLaunching headless browser with saved session...")

        try:
            # Use persistent context to access saved cookies
            context = await p.chromium.launch_persistent_context(
                user_data_dir=str(CHROME_PROFILE),
                headless=True,  # NO VISIBLE BROWSER
                args=[
                    '--disable-blink-features=AutomationControlled',
                    '--no-sandbox',
                ]
            )

            # Create multiple pages for parallel scraping
            num_parallel = 5
            pages = [await context.new_page() for _ in range(num_parallel)]

            # Split accounts into batches
            batches = [accounts[i::num_parallel] for i in range(num_parallel)]

            # Scrape in parallel
            for batch_idx, batch in enumerate(batches):
                page = pages[batch_idx]
                for handle in batch:
                    tweets = await scrape_account(page, handle, batch_idx + 1)
                    all_tweets.extend(tweets)

            await context.close()

        except Exception as e:
            print(f"Error with persistent context: {e}")
            print("Trying headless without saved session...")

            # Fallback to fresh headless (won't have login)
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context()
            page = await context.new_page()

            for i, handle in enumerate(accounts[:20]):  # Limit to 20 for public view
                tweets = await scrape_account(page, handle, 1)
                all_tweets.extend(tweets)

            await browser.close()

    # Save to CSV
    print(f"\n{'=' * 60}")
    print(f"Total tweets found: {len(all_tweets)}")

    if all_tweets:
        # Load existing URLs to dedupe
        existing_urls = set()
        if ALPHA_STAGING.exists():
            with open(ALPHA_STAGING, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if row.get('source_url'):
                        existing_urls.add(row['source_url'])

        # Filter new tweets
        new_tweets = [t for t in all_tweets if t['url'] not in existing_urls]
        print(f"New unique tweets (not in staging): {len(new_tweets)}")

        if new_tweets:
            alpha_id_start = int(get_next_alpha_id().replace('ALPHA', ''))

            with open(ALPHA_STAGING, 'a', newline='', encoding='utf-8') as f:
                fieldnames = [
                    'alpha_id', 'source', 'source_url', 'category', 'tactic',
                    'roi_potential', 'priority', 'status', 'applicable_methods',
                    'applicable_niches', 'synergy_score', 'reviewer_notes',
                    'quality_issues', 'engagement_authenticity', 'earnings_verified',
                    'extracted_method', 'compliance_notes', 'date_added'
                ]
                writer = csv.DictWriter(f, fieldnames=fieldnames)

                for i, tweet in enumerate(new_tweets):
                    # Auto-categorize
                    text_lower = tweet['text'].lower()
                    if any(k in text_lower for k in ['cold email', 'outreach', 'email']):
                        category = 'COLD_OUTBOUND'
                    elif any(k in text_lower for k in ['app', 'ios', 'android', 'mobile']):
                        category = 'APP_FACTORY'
                    elif any(k in text_lower for k in ['content', 'tiktok', 'youtube', 'video']):
                        category = 'CONTENT_FARM'
                    elif any(k in text_lower for k in ['$', 'revenue', 'mrr', 'money']):
                        category = 'MONETIZATION'
                    elif any(k in text_lower for k in ['tool', 'api', 'automation']):
                        category = 'TOOL_ALPHA'
                    else:
                        category = 'GROWTH_HACK'

                    writer.writerow({
                        'alpha_id': f'ALPHA{alpha_id_start + i:04d}',
                        'source': f'@{tweet["handle"]} (Twitter)',
                        'source_url': tweet['url'],
                        'category': category,
                        'tactic': tweet['text'][:500],
                        'roi_potential': 'MEDIUM',
                        'priority': 'MEDIUM',
                        'status': 'PENDING_REVIEW',
                        'applicable_methods': '',
                        'applicable_niches': '',
                        'synergy_score': '',
                        'reviewer_notes': '',
                        'quality_issues': '',
                        'engagement_authenticity': 'UNKNOWN',
                        'earnings_verified': 'FALSE',
                        'extracted_method': '',
                        'compliance_notes': '',
                        'date_added': datetime.now().strftime('%Y-%m-%d')
                    })

            print(f"Saved {len(new_tweets)} new entries to ALPHA_STAGING.csv")

    print("=" * 60)
    print("DONE - Scraper ran in BACKGROUND (no visible browser)")
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(main())
