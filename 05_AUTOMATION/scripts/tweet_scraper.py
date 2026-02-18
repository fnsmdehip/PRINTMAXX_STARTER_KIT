#!/usr/bin/env python3
"""
Tweet Scraper - Extract full content from X/Twitter posts
Uses Playwright to handle JavaScript-rendered content
"""

import asyncio
import json
import csv
import re
import sys
from datetime import datetime
from pathlib import Path
from playwright.async_api import async_playwright

# Force unbuffered output
sys.stdout.reconfigure(line_buffering=True)

# Tweet URLs to extract (from user's high-signal research)
TWEET_URLS = [
    "https://x.com/xivy0k/status/2013267462616228102",
    "https://x.com/tatealax/status/2013347648321753524",
    "https://x.com/simonecanciello/status/2013290619313992028",
    "https://x.com/lottsnomad/status/2013281137234214961",
    "https://x.com/CEOLandshark/status/2012909226641993869",
    "https://x.com/knoxtwts/status/2011358199144648836",
    "https://x.com/knoxtwts/status/2012895519832518880",
    "https://x.com/wesocialgrowth/status/2012887735879565456",
    "https://x.com/gregisenberg/status/2012960814701949281",
    "https://x.com/matteo_spada/status/2012917994364805177",
    "https://x.com/alexcooldev/status/2013002551587901555",
    "https://x.com/alexcooldev/status/2012466735862182002",
    "https://x.com/pipelineabuser/status/2012028804407980354",
    "https://x.com/pipelineabuser/status/2011864820933673114",
    "https://x.com/pipelineabuser/status/2009717466600206558",
    "https://x.com/seanb2b/status/2012977071279014342",
    "https://x.com/WorkflowWhisper/status/2012566082326868407",
    "https://x.com/joelhooks/status/2012934260265816387",
    "https://x.com/wannercashcow/status/2013182221512036821",
    "https://x.com/mattwelter/status/2013271008342659529",
    "https://x.com/Jahjiren/status/2013195696824827981",
    "https://x.com/purpdevvv/status/2013201984916980003",
    "https://x.com/purpdevvv/status/2012442944947585410",
]

OUTPUT_DIR = Path(__file__).parent.parent / "LEDGER"
OUTPUT_FILE = OUTPUT_DIR / "SCRAPED_TWEETS_ALPHA.csv"


async def extract_tweet(page, url: str) -> dict:
    """Extract tweet content from a single URL"""
    result = {
        "url": url,
        "author": "",
        "handle": "",
        "text": "",
        "timestamp": "",
        "likes": "",
        "retweets": "",
        "replies": "",
        "views": "",
        "has_media": False,
        "media_type": "",
        "is_thread": False,
        "top_replies": [],
        "scraped_at": datetime.now().isoformat(),
        "alpha_notes": "",
        "status": "SUCCESS"
    }

    try:
        await page.goto(url, wait_until="networkidle", timeout=30000)
        await page.wait_for_timeout(2000)  # Extra wait for dynamic content

        # Extract author info
        try:
            author_el = await page.query_selector('[data-testid="User-Name"]')
            if author_el:
                author_text = await author_el.inner_text()
                lines = author_text.split('\n')
                result["author"] = lines[0] if lines else ""
                result["handle"] = lines[1] if len(lines) > 1 else ""
        except:
            pass

        # Extract tweet text
        try:
            tweet_el = await page.query_selector('[data-testid="tweetText"]')
            if tweet_el:
                result["text"] = await tweet_el.inner_text()
        except:
            pass

        # Extract timestamp
        try:
            time_el = await page.query_selector('time')
            if time_el:
                result["timestamp"] = await time_el.get_attribute('datetime')
        except:
            pass

        # Check for media
        try:
            img_el = await page.query_selector('[data-testid="tweetPhoto"]')
            video_el = await page.query_selector('[data-testid="videoPlayer"]')
            if video_el:
                result["has_media"] = True
                result["media_type"] = "video"
            elif img_el:
                result["has_media"] = True
                result["media_type"] = "image"
        except:
            pass

        # Extract engagement metrics
        try:
            metrics = await page.query_selector_all('[role="group"] [role="button"]')
            for i, metric in enumerate(metrics[:4]):
                text = await metric.inner_text()
                if i == 0:
                    result["replies"] = text
                elif i == 1:
                    result["retweets"] = text
                elif i == 2:
                    result["likes"] = text
        except:
            pass

        # Check if it's a thread (has "Show this thread" or multiple tweets)
        try:
            thread_indicator = await page.query_selector('text="Show this thread"')
            if thread_indicator:
                result["is_thread"] = True
        except:
            pass

        # Extract top replies (scroll down and grab first few)
        try:
            await page.evaluate("window.scrollBy(0, 500)")
            await page.wait_for_timeout(1000)

            reply_els = await page.query_selector_all('[data-testid="tweet"]')
            for reply in reply_els[1:4]:  # Skip first (main tweet), get next 3
                try:
                    reply_text_el = await reply.query_selector('[data-testid="tweetText"]')
                    if reply_text_el:
                        reply_text = await reply_text_el.inner_text()
                        result["top_replies"].append(reply_text[:200])  # Truncate
                except:
                    pass
        except:
            pass

    except Exception as e:
        result["status"] = f"ERROR: {str(e)[:100]}"

    return result


async def main():
    """Main scraping loop"""
    results = []

    async with async_playwright() as p:
        # Connect to existing Brave browser in debug mode (port 9222)
        try:
            browser = await p.chromium.connect_over_cdp("http://127.0.0.1:9222")
            print("✓ Connected to existing Brave browser")
            contexts = browser.contexts
            if contexts:
                context = contexts[0]
            else:
                context = await browser.new_context()
        except Exception as e:
            print(f"Could not connect to Brave (port 9222): {e}")
            print("Falling back to Chromium launch...")
            browser = await p.chromium.launch(
                headless=False,
                args=['--disable-blink-features=AutomationControlled']
            )
            context = await browser.new_context(
                viewport={'width': 1280, 'height': 800},
                user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
            )

        page = await context.new_page()

        print(f"Starting extraction of {len(TWEET_URLS)} tweets...")
        print("NOTE: X may require login for full content. Login manually if prompted.\n")

        for i, url in enumerate(TWEET_URLS):
            print(f"[{i+1}/{len(TWEET_URLS)}] Extracting: {url}")
            result = await extract_tweet(page, url)
            results.append(result)

            if result["status"] == "SUCCESS":
                print(f"  ✓ @{result['handle']}: {result['text'][:60]}...")
            else:
                print(f"  ✗ {result['status']}")

            # Rate limit protection
            await page.wait_for_timeout(2000)

        await browser.close()

    # Save to CSV
    if results:
        with open(OUTPUT_FILE, 'w', newline='', encoding='utf-8') as f:
            fieldnames = [
                "url", "author", "handle", "text", "timestamp",
                "likes", "retweets", "replies", "views",
                "has_media", "media_type", "is_thread", "top_replies",
                "scraped_at", "alpha_notes", "status"
            ]
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()

            for result in results:
                # Convert list to string for CSV
                result["top_replies"] = " | ".join(result["top_replies"])
                writer.writerow(result)

        print(f"\n✓ Saved {len(results)} tweets to {OUTPUT_FILE}")

    # Also save raw JSON for debugging
    json_file = OUTPUT_DIR / "SCRAPED_TWEETS_ALPHA.json"
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print(f"✓ Saved JSON to {json_file}")

    return results


if __name__ == "__main__":
    asyncio.run(main())
