#!/usr/bin/env python3
"""
X Bookmarks Extractor - File Signal Version
Opens Brave, waits for GO signal file, then extracts.
"""

import asyncio
import json
import csv
import os
from datetime import datetime
from playwright.async_api import async_playwright
from pathlib import Path

SIGNAL_FILE = '/tmp/bookmark_extraction_go.signal'

async def main():
    async with async_playwright() as p:
        print("🚀 Opening Brave browser...")
        print("=" * 80)
        print("INSTRUCTIONS:")
        print("1. Login to X.com in the browser that opens")
        print("2. Navigate to: https://x.com/i/bookmarks")
        print("3. Wait for bookmarks to load")
        print("4. In a NEW TERMINAL, run this command:")
        print()
        print(f"   touch {SIGNAL_FILE}")
        print()
        print("=" * 80)

        # Launch Brave
        browser = await p.chromium.launch(
            headless=False,
            executable_path='/Applications/Brave Browser.app/Contents/MacOS/Brave Browser',
            args=['--start-maximized', '--disable-blink-features=AutomationControlled']
        )

        context = await browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        )

        page = await context.new_page()
        await page.goto('https://x.com')

        # Clean up old signal
        if os.path.exists(SIGNAL_FILE):
            os.remove(SIGNAL_FILE)

        # Wait for signal
        print(f"\n⏳ Waiting for GO signal...")
        print(f"   (Checking for file: {SIGNAL_FILE})")

        waited = 0
        while not os.path.exists(SIGNAL_FILE) and waited < 600:  # 10 min max
            await asyncio.sleep(2)
            waited += 2

            if waited % 20 == 0:
                print(f"   Still waiting... ({waited}s)")

        if not os.path.exists(SIGNAL_FILE):
            print("❌ Timeout - no signal received. Exiting...")
            await browser.close()
            return

        print("\n✅ GO signal received! Starting extraction...\n")

        # Give user 3 seconds to see message
        await asyncio.sleep(3)

        # Extract
        bookmarks = []
        prev_count = 0
        scroll_attempts = 0
        max_scrolls = 200

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

            unique = {b['url']: b for b in bookmarks}
            bookmarks = list(unique.values())
            current_count = len(bookmarks)

            if current_count != prev_count:
                print(f"📊 {current_count} bookmarks")

            if current_count == prev_count:
                print("\n✅ Extraction complete!")
                break

            prev_count = current_count
            await page.evaluate('window.scrollBy(0, window.innerHeight)')
            await asyncio.sleep(1.2)
            scroll_attempts += 1

        print(f"\n📦 Total: {len(bookmarks)} bookmarks")

        # Save
        ts = datetime.now().strftime('%Y%m%d_%H%M%S')
        base = Path('/Users/macbookpro/Downloads/PRINTMAXX_STARTER_KIT/AUTOMATIONS/x_bookmarks')
        base.mkdir(parents=True, exist_ok=True)

        raw_json = base / f'raw_{ts}.json'
        with open(raw_json, 'w', encoding='utf-8') as f:
            json.dump(bookmarks, f, indent=2, ensure_ascii=False)
        print(f"💾 {raw_json}")

        raw_csv = base / f'raw_{ts}.csv'
        with open(raw_csv, 'w', newline='', encoding='utf-8') as f:
            if bookmarks:
                writer = csv.DictWriter(f, fieldnames=['text', 'author', 'timestamp', 'url'])
                writer.writeheader()
                writer.writerows(bookmarks)
        print(f"💾 {raw_csv}")

        # Cleanup
        if os.path.exists(SIGNAL_FILE):
            os.remove(SIGNAL_FILE)

        print("\n✅ Done! Browser will close in 5 seconds...")
        await asyncio.sleep(5)
        await browser.close()

        return str(raw_json)

if __name__ == "__main__":
    result = asyncio.run(main())
    if result:
        print(f"\n🎯 Next: python3 analyze_bookmarks.py {result}")
