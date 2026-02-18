#!/usr/bin/env python3
"""
X Bookmarks Extractor - Stealth Mode
Uses stealth patches to avoid detection + CDP session to connect to existing browser
"""

import asyncio
import json
import csv
from datetime import datetime
from playwright.async_api import async_playwright
from pathlib import Path

async def main():
    async with async_playwright() as p:
        print("🚀 Launching Brave with stealth mode...")
        print("=" * 80)

        # Launch with stealth settings
        browser = await p.chromium.launch(
            headless=False,
            executable_path='/Applications/Brave Browser.app/Contents/MacOS/Brave Browser',
            args=[
                '--start-maximized',
                '--disable-blink-features=AutomationControlled',  # Key fix
                '--disable-dev-shm-usage',
                '--no-sandbox',
                '--disable-web-security',
                '--disable-features=IsolateOrigins,site-per-process',
                '--disable-site-isolation-trials',
            ]
        )

        # Create context with realistic settings
        context = await browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            locale='en-US',
            timezone_id='America/New_York',
            permissions=['geolocation'],
            geolocation={'latitude': 40.7128, 'longitude': -74.0060},  # NYC
            color_scheme='dark',
            reduced_motion='no-preference',
            forced_colors='none',
        )

        # Add extra stealth
        await context.add_init_script("""
            // Remove webdriver property
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            });

            // Mock plugins
            Object.defineProperty(navigator, 'plugins', {
                get: () => [1, 2, 3, 4, 5]
            });

            // Mock languages
            Object.defineProperty(navigator, 'languages', {
                get: () => ['en-US', 'en']
            });

            // Chrome object
            window.chrome = {
                runtime: {}
            };

            // Permissions
            const originalQuery = window.navigator.permissions.query;
            window.navigator.permissions.query = (parameters) => (
                parameters.name === 'notifications' ?
                    Promise.resolve({ state: Notification.permission }) :
                    originalQuery(parameters)
            );
        """)

        page = await context.new_page()

        print("✅ Browser launched with stealth settings")
        print("📌 Manual steps:")
        print("   1. Login to X.com (should work normally now)")
        print("   2. Navigate to https://x.com/i/bookmarks")
        print("   3. Wait for bookmarks to load")
        print()
        print("⏳ Waiting for bookmarks page...")
        print()

        # Navigate to X
        await page.goto('https://x.com', wait_until='domcontentloaded')

        # Wait for bookmarks URL
        max_wait = 600  # 10 minutes
        waited = 0

        while '/bookmarks' not in page.url and waited < max_wait:
            await asyncio.sleep(3)
            waited += 3

            if waited % 30 == 0:
                print(f"   Still waiting... ({waited}s) Current URL: {page.url[:50]}...")

        if '/bookmarks' not in page.url:
            print("❌ Timeout. Exiting...")
            await browser.close()
            return

        print(f"✅ Detected bookmarks page!")
        print("⏳ Waiting 5 seconds for page to fully load...\n")
        await asyncio.sleep(5)

        print("🔄 Starting extraction...\n")

        # Extract
        bookmarks = []
        prev_count = 0
        scroll_attempts = 0
        max_scrolls = 200
        no_change_count = 0

        while scroll_attempts < max_scrolls:
            tweets = await page.query_selector_all('[data-testid="tweet"]')

            for tweet in tweets:
                try:
                    text_elem = await tweet.query_selector('[data-testid="tweetText"]')
                    text = await text_elem.inner_text() if text_elem else ""

                    author_elem = await tweet.query_selector('[data-testid="User-Name"]')
                    author_raw = await author_elem.inner_text() if author_elem else ""
                    author = author_raw.split('\n')[0] if author_raw else ""

                    time_elem = await tweet.query_selector('time')
                    timestamp = await time_elem.get_attribute('datetime') if time_elem else ""

                    link_elem = await tweet.query_selector('a[href*="/status/"]')
                    url = await link_elem.get_attribute('href') if link_elem else ""
                    if url and not url.startswith('http'):
                        url = f"https://x.com{url}"

                    if text and url:
                        bookmarks.append({
                            'text': text,
                            'author': author,
                            'timestamp': timestamp,
                            'url': url
                        })
                except:
                    continue

            # Dedupe
            unique = {b['url']: b for b in bookmarks}
            bookmarks = list(unique.values())
            current_count = len(bookmarks)

            if current_count != prev_count:
                print(f"📊 {current_count} bookmarks")
                no_change_count = 0
            else:
                no_change_count += 1

            # Stop if no new bookmarks for 3 scrolls
            if no_change_count >= 3:
                print("\n✅ No new bookmarks found. Complete!")
                break

            prev_count = current_count

            # Scroll with random delay (more human-like)
            await page.evaluate('window.scrollBy(0, window.innerHeight)')
            delay = 1.2 + (scroll_attempts % 3) * 0.2  # Vary between 1.2-1.6s
            await asyncio.sleep(delay)
            scroll_attempts += 1

        print(f"\n📦 Total: {len(bookmarks)} bookmarks\n")

        # Save
        ts = datetime.now().strftime('%Y%m%d_%H%M%S')
        base = Path('/Users/macbookpro/Downloads/PRINTMAXX_STARTER_KIT/AUTOMATIONS/x_bookmarks')
        base.mkdir(parents=True, exist_ok=True)

        raw_json = base / f'raw_{ts}.json'
        with open(raw_json, 'w', encoding='utf-8') as f:
            json.dump(bookmarks, f, indent=2, ensure_ascii=False)
        print(f"💾 Saved: {raw_json}")

        raw_csv = base / f'raw_{ts}.csv'
        with open(raw_csv, 'w', newline='', encoding='utf-8') as f:
            if bookmarks:
                writer = csv.DictWriter(f, fieldnames=['text', 'author', 'timestamp', 'url'])
                writer.writeheader()
                writer.writerows(bookmarks)
        print(f"💾 Saved: {raw_csv}")

        print("\n✅ Extraction complete!")
        print(f"\n🎯 Next step:")
        print(f"   python3 analyze_bookmarks.py {raw_json.name}")
        print("\nBrowser will close in 10 seconds...")

        await asyncio.sleep(10)
        await browser.close()

        return str(raw_json)

if __name__ == "__main__":
    result = asyncio.run(main())
