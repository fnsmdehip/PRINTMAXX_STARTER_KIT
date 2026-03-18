#!/usr/bin/env python3
"""
Batch test Surge.sh deployments with Playwright.
Test 30 high-priority sites across all categories.
"""

import asyncio
import json
import time
from datetime import datetime
from pathlib import Path

try:
    from playwright.async_api import async_playwright
except ImportError:
    print("ERROR: playwright not installed. Run: pip install playwright")
    exit(1)

# Test URLs - prioritized list
TEST_URLS = [
    # Previously RED (DNS failures) - retest
    "https://mobile-auto-detailing-experts-in-oklahoma-city-champion-deta-oklahoma-city-ok.surge.sh",
    "https://window-cleaning-in-portland-or-all-pro-metro-services-llc-portland-or.surge.sh",
    "https://local-window-cleaning-in-louisville-pink-x27-s-windows-louisville-ky.surge.sh",

    # Previously GREEN - verify still healthy
    "https://printmaxx.surge.sh",
    "https://prayerlock-web.surge.sh",
    "https://coldmaxx.surge.sh",
    "https://mcp-marketplace.surge.sh",
    "https://stackmaxx.surge.sh",

    # PWA Apps
    "https://coreday.surge.sh",
    "https://walktounlock-web.surge.sh",
    "https://tasksmash-web.surge.sh",
    "https://sleepmaxx-web.surge.sh",
    "https://focuslock-web.surge.sh",
    "https://ramadan-tracker.surge.sh",

    # Comparison pages
    "https://coldmaxx-vs-instantly.surge.sh",
    "https://cursor-vs-claudecode.surge.sh",
    "https://prayerlock-vs-hallow.surge.sh",

    # Lead magnets
    "https://cold-email-roi-calculator.surge.sh",
    "https://subject-line-grader.surge.sh",
    "https://revenue-leak-audit.surge.sh",

    # Tool apps
    "https://invoiceforge.surge.sh",
    "https://pagescorer.surge.sh",
    "https://prospectmaxx.surge.sh",

    # Fiverr service pages
    "https://printmaxx-website-design.surge.sh",
    "https://printmaxx-cold-email.surge.sh",
    "https://printmaxx-automation.surge.sh",

    # Brand pages
    "https://printmaxx-tools.surge.sh",
    "https://printmaxx-apps.surge.sh",
    "https://claude-code-agent-bible.surge.sh",

    # Denomination streak apps (sample)
    "https://scripture-streak.surge.sh",
    "https://prayerlock-landing.surge.sh",

    # Local biz (sample)
    "https://old-settlers-dental-p-a-austin-tx.surge.sh",
]

async def test_site(page, url: str) -> dict:
    """Test a single site and return results."""
    result = {
        "url": url,
        "domain": url.replace("https://", "").replace("http://", "").split("/")[0],
        "status_code": None,
        "load_time_ms": None,
        "has_content": False,
        "console_errors": [],
        "page_title": None,
        "category": "GREEN",
        "error": None
    }

    start = time.time()

    try:
        # Capture console messages
        console_msgs = []
        page.on("console", lambda msg: console_msgs.append({
            "type": msg.type,
            "text": msg.text
        }))

        response = await page.goto(url, wait_until="networkidle", timeout=10000)
        load_time = (time.time() - start) * 1000

        if response:
            result["status_code"] = response.status

        result["load_time_ms"] = round(load_time, 2)
        result["page_title"] = await page.title()

        # Check for visible content
        body_text = await page.evaluate("() => document.body.innerText.length")
        result["has_content"] = body_text > 50  # More than 50 chars = has content

        # Filter console errors
        result["console_errors"] = [
            msg for msg in console_msgs
            if msg["type"] == "error"
        ]

        # Categorize
        if result["status_code"] == 200 and result["has_content"]:
            result["category"] = "GREEN"
        elif result["status_code"] in [200, 301, 302]:
            result["category"] = "YELLOW"  # Loads but may have issues
        elif result["status_code"] and result["status_code"] >= 400:
            result["category"] = "RED"
        else:
            result["category"] = "RED"

        # Slow page check
        if result["load_time_ms"] and result["load_time_ms"] > 5000:
            if result["category"] == "GREEN":
                result["category"] = "YELLOW"

    except asyncio.TimeoutError:
        result["error"] = "Timeout (>10s)"
        result["category"] = "RED"
    except Exception as e:
        result["error"] = str(e)
        result["category"] = "RED"

    return result

async def main():
    """Run batch tests."""
    results = {
        "tested_at": datetime.now().isoformat(),
        "total": len(TEST_URLS),
        "green": 0,
        "yellow": 0,
        "red": 0,
        "sites": []
    }

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        context = await browser.new_context()
        page = await context.new_page()

        print(f"\n🎭 PLAYWRIGHT TESTER - Batch Testing {len(TEST_URLS)} Sites")
        print("=" * 70)

        for i, url in enumerate(TEST_URLS, 1):
            domain = url.replace("https://", "").split("/")[0]
            print(f"\n[{i}/{len(TEST_URLS)}] Testing {domain[:50]}...", end=" ", flush=True)

            result = await test_site(page, url)
            results["sites"].append(result)

            # Update category counts
            if result["category"] == "GREEN":
                results["green"] += 1
                print("✅ GREEN")
            elif result["category"] == "YELLOW":
                results["yellow"] += 1
                print("⚠️  YELLOW")
            else:
                results["red"] += 1
                print("❌ RED")

            if result["error"]:
                print(f"   Error: {result['error']}")
            else:
                print(f"   Status: {result['status_code']} | Load: {result['load_time_ms']}ms | Content: {result['has_content']}")

        await context.close()
        await browser.close()

    # Calculate pass rate
    results["pass_rate"] = f"{(results['green'] / results['total'] * 100):.1f}%"

    # Save results
    report_file = Path("/Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt/AUTOMATIONS/agent/swarm/reports/playwright_test_20260318.json")
    report_file.parent.mkdir(parents=True, exist_ok=True)

    with open(report_file, "w") as f:
        json.dump(results, f, indent=2)

    print("\n" + "=" * 70)
    print(f"\n📊 RESULTS SUMMARY")
    print(f"   GREEN:  {results['green']}/{results['total']} ({(results['green']/results['total']*100):.1f}%)")
    print(f"   YELLOW: {results['yellow']}/{results['total']} ({(results['yellow']/results['total']*100):.1f}%)")
    print(f"   RED:    {results['red']}/{results['total']} ({(results['red']/results['total']*100):.1f}%)")
    print(f"\n   Report saved to: {report_file}")
    print("=" * 70)

    return results

if __name__ == "__main__":
    results = asyncio.run(main())
