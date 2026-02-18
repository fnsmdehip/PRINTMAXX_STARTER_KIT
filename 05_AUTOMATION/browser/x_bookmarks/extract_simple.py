#!/usr/bin/env python3
"""
Simple X Bookmarks Extractor
Opens Brave, waits for you to login and navigate to bookmarks, then extracts everything.
"""

import asyncio
import json
import csv
from datetime import datetime
from playwright.async_api import async_playwright
import os

async def main():
    async with async_playwright() as p:
        print("🚀 Opening Brave browser...")
        print("=" * 60)
        print("INSTRUCTIONS:")
        print("1. Login to X.com")
        print("2. Navigate to your bookmarks (https://x.com/i/bookmarks)")
        print("3. Wait for bookmarks to load")
        print("4. Come back here and type 'go' then press ENTER")
        print("=" * 60)

        # Launch Brave
        browser = await p.chromium.launch(
            headless=False,
            executable_path='/Applications/Brave Browser.app/Contents/MacOS/Brave Browser',
            args=['--start-maximized']
        )

        context = await browser.new_context(
            viewport={'width': 1920, 'height': 1080}
        )

        page = await context.new_page()

        # Navigate to X
        await page.goto('https://x.com')

        # Wait for user confirmation
        user_input = input("\n👉 Type 'go' when you're on the bookmarks page: ").strip().lower()

        if user_input != 'go':
            print("❌ Cancelled. Closing browser...")
            await browser.close()
            return

        print("\n⏳ Starting extraction...\n")

        # Extract bookmarks
        bookmarks = []
        prev_count = 0
        scroll_attempts = 0
        max_scrolls = 150

        while scroll_attempts < max_scrolls:
            # Get all tweets
            tweets = await page.query_selector_all('[data-testid="tweet"]')

            for tweet in tweets:
                try:
                    # Text
                    text_elem = await tweet.query_selector('[data-testid="tweetText"]')
                    text = await text_elem.inner_text() if text_elem else ""

                    # Author
                    author_elem = await tweet.query_selector('[data-testid="User-Name"]')
                    author_raw = await author_elem.inner_text() if author_elem else ""
                    author = author_raw.split('\n')[0] if author_raw else ""

                    # Timestamp
                    time_elem = await tweet.query_selector('time')
                    timestamp = await time_elem.get_attribute('datetime') if time_elem else ""

                    # URL
                    link_elem = await tweet.query_selector('a[href*="/status/"]')
                    url = await link_elem.get_attribute('href') if link_elem else ""
                    if url and not url.startsWith('http'):
                        url = f"https://x.com{url}"

                    if text and url:
                        bookmarks.append({
                            'text': text,
                            'author': author,
                            'timestamp': timestamp,
                            'url': url
                        })

                except Exception as e:
                    continue

            # Dedupe
            unique = {b['url']: b for b in bookmarks}
            bookmarks = list(unique.values())

            current_count = len(bookmarks)

            # Progress
            if current_count != prev_count:
                print(f"📊 Collected: {current_count} bookmarks")

            # Check if done
            if current_count == prev_count:
                print("\n✅ No new bookmarks found - extraction complete!")
                break

            prev_count = current_count

            # Scroll
            await page.evaluate('window.scrollBy(0, window.innerHeight)')
            await asyncio.sleep(1.5)
            scroll_attempts += 1

        print(f"\n📦 Total bookmarks extracted: {len(bookmarks)}")

        # Save raw data
        ts = datetime.now().strftime('%Y%m%d_%H%M%S')
        base = '/Users/macbookpro/Downloads/PRINTMAXX_STARTER_KIT/AUTOMATIONS/x_bookmarks'

        os.makedirs(base, exist_ok=True)

        raw_json = f'{base}/raw_{ts}.json'
        with open(raw_json, 'w', encoding='utf-8') as f:
            json.dump(bookmarks, f, indent=2, ensure_ascii=False)
        print(f"💾 Saved: {raw_json}")

        raw_csv = f'{base}/raw_{ts}.csv'
        with open(raw_csv, 'w', newline='', encoding='utf-8') as f:
            if bookmarks:
                writer = csv.DictWriter(f, fieldnames=['text', 'author', 'timestamp', 'url'])
                writer.writeheader()
                writer.writerows(bookmarks)
        print(f"💾 Saved: {raw_csv}")

        print("\n✅ Extraction complete!")
        print(f"   Next step: Run analyzer to filter and extract insights")

        await asyncio.sleep(3)
        await browser.close()

        return raw_json

if __name__ == "__main__":
    result = asyncio.run(main())
    if result:
        print(f"\n🎯 Run this next:")
        print(f"   python3 analyze_bookmarks.py {result}")
