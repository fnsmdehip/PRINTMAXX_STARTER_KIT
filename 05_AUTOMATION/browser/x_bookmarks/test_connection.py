#!/usr/bin/env python3
"""
Quick test - verify Playwright can connect to Brave
"""

import asyncio
from playwright.async_api import async_playwright

async def test():
    print("🔌 Testing connection to Brave...")

    async with async_playwright() as p:
        try:
            browser = await p.chromium.connect_over_cdp("http://localhost:9222")
            print("✅ Connected successfully!")

            contexts = browser.contexts
            print(f"📊 Found {len(contexts)} browser contexts")

            if contexts:
                pages = contexts[0].pages
                print(f"📄 Found {len(pages)} open pages")

                if pages:
                    page = pages[0]
                    url = page.url
                    print(f"🌐 Current page: {url}")

            await browser.close()
            print("\n✅ Connection test PASSED - ready to run full analysis!")

        except Exception as e:
            print(f"❌ Connection failed: {e}")
            print("\nTroubleshooting:")
            print("1. Make sure Brave is running")
            print("2. Start with: ./quick_start.sh")
            print("3. Wait 5 seconds after Brave opens")
            print("4. Try this test again")

if __name__ == "__main__":
    asyncio.run(test())
