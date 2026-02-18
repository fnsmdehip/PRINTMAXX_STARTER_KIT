#!/usr/bin/env python3
"""
Scrape @caiden_cole tweets using Playwright with Chrome profile
"""

import asyncio
import json
import os
from datetime import datetime
from playwright.async_api import async_playwright

# Chrome profile path (user's logged-in Chrome)
CHROME_USER_DATA = os.path.expanduser("~/Library/Application Support/Google/Chrome")

async def scrape_caiden():
    async with async_playwright() as p:
        # Launch Chrome with user's profile
        browser = await p.chromium.launch_persistent_context(
            CHROME_USER_DATA,
            headless=False,
            channel="chrome",
            args=['--disable-blink-features=AutomationControlled']
        )

        page = await browser.new_page()

        try:
            # Navigate to Caiden's profile
            print("🔍 Navigating to @caiden_cole...")
            await page.goto("https://x.com/caiden_cole", wait_until="networkidle")
            await asyncio.sleep(3)

            # Scroll to load tweets
            print("📜 Scrolling to load tweets...")
            for _ in range(5):
                await page.evaluate("window.scrollBy(0, 1000)")
                await asyncio.sleep(1)

            # Extract tweets
            tweets = []
            articles = await page.query_selector_all('article[data-testid="tweet"]')

            print(f"📊 Found {len(articles)} tweets")

            for i, article in enumerate(articles[:20]):  # Get top 20 tweets
                try:
                    # Get tweet text
                    text_element = await article.query_selector('[data-testid="tweetText"]')
                    tweet_text = await text_element.inner_text() if text_element else ""

                    # Get timestamp link
                    time_element = await article.query_selector('time')
                    tweet_url = ""
                    if time_element:
                        link = await time_element.evaluate("el => el.parentElement.href")
                        tweet_url = link if link else ""

                    # Get engagement metrics
                    reply_count = await article.query_selector('[data-testid="reply"]')
                    retweet_count = await article.query_selector('[data-testid="retweet"]')
                    like_count = await article.query_selector('[data-testid="like"]')

                    replies = await reply_count.inner_text() if reply_count else "0"
                    retweets = await retweet_count.inner_text() if retweet_count else "0"
                    likes = await like_count.inner_text() if like_count else "0"

                    if tweet_text and len(tweet_text) > 10:
                        tweet_data = {
                            "text": tweet_text,
                            "url": tweet_url,
                            "replies": replies,
                            "retweets": retweets,
                            "likes": likes,
                            "scraped_at": datetime.now().isoformat()
                        }
                        tweets.append(tweet_data)
                        print(f"✅ Tweet {i+1}: {tweet_text[:80]}...")

                except Exception as e:
                    print(f"⚠️  Error extracting tweet {i+1}: {e}")
                    continue

            # Save to JSON
            output_file = f"AUTOMATIONS/twitter_scraper_output/caiden_tweets_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            os.makedirs("AUTOMATIONS/twitter_scraper_output", exist_ok=True)

            with open(output_file, 'w') as f:
                json.dump(tweets, f, indent=2)

            print(f"\n✅ SCRAPING COMPLETE")
            print(f"📁 Saved {len(tweets)} tweets to: {output_file}")

            # Print tweets for review
            print("\n" + "="*80)
            print("CAIDEN'S RECENT TWEETS:")
            print("="*80)
            for i, tweet in enumerate(tweets[:10], 1):
                print(f"\n{i}. {tweet['text'][:200]}...")
                print(f"   URL: {tweet['url']}")
                print(f"   💬 {tweet['replies']} | 🔄 {tweet['retweets']} | ❤️  {tweet['likes']}")

            return tweets

        except Exception as e:
            print(f"❌ Error: {e}")
            return []

        finally:
            await browser.close()

if __name__ == "__main__":
    tweets = asyncio.run(scrape_caiden())
    print(f"\n🎯 Total tweets scraped: {len(tweets)}")
