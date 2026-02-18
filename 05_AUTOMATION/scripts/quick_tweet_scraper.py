#!/usr/bin/env python3
"""Quick tweet scraper using existing browser session"""

import asyncio
import csv
import json
from datetime import datetime
from pathlib import Path
from playwright.async_api import async_playwright

URLS = [
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


async def scrape():
    results = []

    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp('http://127.0.0.1:9222')
        contexts = browser.contexts
        if not contexts:
            print('No browser contexts found')
            return []

        context = contexts[0]
        pages = context.pages
        if not pages:
            print('No pages found in browser')
            return []
        page = pages[0]
        print(f'Using page: {page.url[:60]}...')

        print(f"Scraping {len(URLS)} tweets...")

        for i, url in enumerate(URLS):
            handle = url.split('/')[3]
            print(f"[{i+1}/{len(URLS)}] @{handle}...")

            result = {
                "url": url,
                "handle": f"@{handle}",
                "content": "",
                "scraped_at": datetime.now().isoformat(),
                "status": "SUCCESS"
            }

            try:
                await page.goto(url, wait_until='domcontentloaded', timeout=15000)
                await page.wait_for_timeout(2500)

                body = await page.query_selector('body')
                if body:
                    text = await body.inner_text()
                    # Extract meaningful content lines
                    lines = text.split('\n')
                    content_lines = []
                    for line in lines:
                        line = line.strip()
                        # Skip short lines, UI elements, and common noise
                        if len(line) < 30:
                            continue
                        if any(skip in line.lower() for skip in ['sign up', 'log in', 'cookie', 'privacy policy', 'terms of service', 'trending', 'who to follow']):
                            continue
                        content_lines.append(line)
                        if len(content_lines) >= 10:
                            break

                    result["content"] = " | ".join(content_lines)
                    print(f"  ✓ {content_lines[0][:60]}..." if content_lines else "  ✓ (no content)")

            except Exception as e:
                result["status"] = f"ERROR: {str(e)[:100]}"
                print(f"  ✗ {str(e)[:60]}")

            results.append(result)
            await page.wait_for_timeout(1500)  # Rate limit

    return results


async def main():
    results = await scrape()

    if not results:
        print("No results to save")
        return

    # Save CSV
    csv_file = OUTPUT_DIR / "SCRAPED_TWEETS_ALPHA.csv"
    with open(csv_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=["url", "handle", "content", "scraped_at", "status"])
        writer.writeheader()
        writer.writerows(results)

    print(f"\n✓ Saved {len(results)} tweets to {csv_file}")

    # Save JSON for detailed view
    json_file = OUTPUT_DIR / "SCRAPED_TWEETS_ALPHA.json"
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print(f"✓ Saved JSON to {json_file}")


if __name__ == "__main__":
    asyncio.run(main())
