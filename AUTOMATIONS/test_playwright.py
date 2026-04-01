#!/usr/bin/env python3
"""Playwright Tester - Test all deployed sites for health."""

import asyncio
import json
import time
from datetime import datetime
from pathlib import Path
from typing import Optional
import re

try:
    from playwright.async_api import async_playwright, Page
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False
    print("⚠️  Playwright not installed. Install: pip3 install playwright")
    print("   Then run: playwright install")

# URLs to test
RED_SITES = [
    "https://mobile-auto-detailing-experts-in-oklahoma-city-champion-deta-oklahoma-city-ok.surge.sh",
    "https://top-rated-mobile-car-detailing-in-oklahoma-city-ok-pure-prof-oklahoma-city-ok.surge.sh",
    "https://window-cleaning-in-portland-or-all-pro-metro-services-llc-portland-or.surge.sh",
    "https://saas-stack-audit-200.surge.sh",
    "https://mobile-interior-detailing-birmingham-al-magic-city-detailing-birmingham-al.surge.sh",
    "https://home-professional-mobile-detailing-amp-products-super-store-birmingham-al.surge.sh",
    "https://the-10-best-handyman-services-in-las-vegas-nv-2026-homeguide-las-vegas-nv.surge.sh",
    "https://local-window-cleaning-in-louisville-pink-x27-s-windows-louisville-ky.surge.sh",
    "https://residential-and-commercial-window-cleaning-cherry-window-cle-louisville-ky.surge.sh",
]

# Sample green sites (from deployed_assets.json)
SAMPLE_GREEN = [
    "https://printmaxx.surge.sh",
    "https://prayerlock.surge.sh",
    "https://mcp-marketplace.surge.sh",
    "https://ramadan-tracker.surge.sh",
    "https://focuslock.surge.sh",
    "https://coldmaxx.surge.sh",
    "https://invoiceforge.surge.sh",
    "https://pagescorer.surge.sh",
    "https://coreday.surge.sh",
    "https://walktounlock-web.surge.sh",
    "https://scripture-streak.surge.sh",
    "https://best-ai-tools-2026.surge.sh",
    "https://cold-email-roi-calculator.surge.sh",
    "https://prayerlock-vs-hallow.surge.sh",
    "https://n8n-vs-zapier-vs-make.surge.sh",
]

async def test_site(page: Page, url: str, timeout: int = 10000) -> dict:
    """Test a single site and return results."""
    start_time = time.time()
    result = {
        "url": url,
        "status": "UNKNOWN",
        "http_code": 0,
        "load_time_ms": 0,
        "console_errors": [],
        "console_warnings": [],
        "has_content": False,
        "content_length": 0,
        "links_checked": 0,
        "broken_links": [],
        "screenshot_path": None,
        "error": None,
    }

    try:
        # Capture console messages
        console_messages = []
        page.on("console", lambda msg: console_messages.append({"type": msg.type, "text": msg.text}))

        # Navigate
        response = await page.goto(url, wait_until="networkidle", timeout=timeout)
        result["http_code"] = response.status if response else 0

        # Get load time
        result["load_time_ms"] = int((time.time() - start_time) * 1000)

        # Check content
        try:
            content = await page.content()
            result["content_length"] = len(content)
            result["has_content"] = len(content.strip()) > 100
        except:
            result["has_content"] = False

        # Classify console messages
        for msg in console_messages:
            if msg["type"] == "error":
                result["console_errors"].append(msg["text"])
            elif msg["type"] == "warning":
                result["console_warnings"].append(msg["text"])

        # Determine status
        if result["http_code"] == 200 and result["has_content"]:
            if result["load_time_ms"] > 5000:
                result["status"] = "YELLOW"
            elif result["console_errors"]:
                result["status"] = "YELLOW"
            else:
                result["status"] = "GREEN"
        elif result["http_code"] in [301, 302, 307]:
            result["status"] = "REDIRECT"
        elif result["http_code"] >= 400:
            result["status"] = "RED"
        elif not result["has_content"]:
            result["status"] = "RED"
        else:
            result["status"] = "YELLOW"

        # Take screenshot
        screenshot_name = url.replace("https://", "").replace(".", "_").replace("/", "_") + ".png"
        screenshot_path = f"AUTOMATIONS/agent/swarm/screenshots/{screenshot_name}"
        try:
            await page.screenshot(path=screenshot_path)
            result["screenshot_path"] = screenshot_path
        except Exception as e:
            result["screenshot_path"] = None

    except Exception as e:
        result["status"] = "ERROR"
        result["error"] = str(e)

    return result

async def run_tests():
    """Run all tests with Playwright."""
    if not PLAYWRIGHT_AVAILABLE:
        print("❌ Playwright not available. Skipping tests.")
        return []

    results = []

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()

        # Test red sites first
        print("\n📍 Testing 9 RED sites from last cycle...")
        for url in RED_SITES:
            page = await context.new_page()
            print(f"  Testing: {url.replace('https://', '')}")
            result = await test_site(page, url)
            results.append(result)
            print(f"    → {result['status']} ({result['http_code']}) - {result['load_time_ms']}ms")
            await page.close()

        # Test green samples
        print("\n📍 Testing 15 sample GREEN sites...")
        for url in SAMPLE_GREEN:
            page = await context.new_page()
            print(f"  Testing: {url.replace('https://', '')}")
            result = await test_site(page, url)
            results.append(result)
            print(f"    → {result['status']} ({result['http_code']}) - {result['load_time_ms']}ms")
            await page.close()

        await context.close()
        await browser.close()

    return results

def summarize_results(results: list) -> dict:
    """Summarize test results."""
    summary = {
        "tested_at": datetime.now().isoformat(),
        "total_tests": len(results),
        "green": 0,
        "yellow": 0,
        "red": 0,
        "error": 0,
        "avg_load_ms": 0,
        "pass_rate": "0%",
        "broken_sites": [],
        "slow_sites": [],
        "sites_with_errors": [],
    }

    load_times = []
    for result in results:
        if result["status"] == "GREEN":
            summary["green"] += 1
        elif result["status"] == "YELLOW":
            summary["yellow"] += 1
        elif result["status"] == "RED":
            summary["red"] += 1
            summary["broken_sites"].append(result["url"])
        elif result["status"] == "ERROR":
            summary["error"] += 1
            summary["broken_sites"].append(result["url"])

        if result["load_time_ms"] > 5000:
            summary["slow_sites"].append((result["url"], result["load_time_ms"]))

        if result["console_errors"]:
            summary["sites_with_errors"].append((result["url"], result["console_errors"]))

        if result["load_time_ms"] > 0:
            load_times.append(result["load_time_ms"])

    if load_times:
        summary["avg_load_ms"] = int(sum(load_times) / len(load_times))

    if summary["total_tests"] > 0:
        summary["pass_rate"] = f"{((summary['green'] / summary['total_tests']) * 100):.1f}%"

    return summary

def save_report(results: list, summary: dict):
    """Save test report."""
    report_path = "AUTOMATIONS/agent/swarm/reports/playwright_tester_report_20260331.md"

    lines = [
        "# Playwright Test Report - 2026-03-31",
        f"\n**Test Time:** {summary['tested_at']}",
        f"**Total Tests:** {summary['total_tests']}",
        f"**Pass Rate:** {summary['pass_rate']}",
        f"\n## Summary",
        f"- ✅ GREEN: {summary['green']}/{summary['total_tests']}",
        f"- ⚠️  YELLOW: {summary['yellow']}/{summary['total_tests']}",
        f"- ❌ RED: {summary['red']}/{summary['total_tests']}",
        f"- 🔴 ERROR: {summary['error']}/{summary['total_tests']}",
        f"- ⏱️  Avg Load Time: {summary['avg_load_ms']}ms",
    ]

    if summary["broken_sites"]:
        lines.append("\n## Broken Sites")
        for site in summary["broken_sites"]:
            lines.append(f"- {site}")

    if summary["slow_sites"]:
        lines.append("\n## Slow Sites (>5s)")
        for url, ms in summary["slow_sites"]:
            lines.append(f"- {url} ({ms}ms)")

    if summary["sites_with_errors"]:
        lines.append("\n## Sites with Console Errors")
        for url, errors in summary["sites_with_errors"]:
            lines.append(f"- {url}")
            for error in errors[:3]:  # First 3 errors
                lines.append(f"  - {error}")

    lines.append("\n## Detailed Results")
    for result in results:
        lines.append(f"\n### {result['url']}")
        lines.append(f"- **Status:** {result['status']}")
        lines.append(f"- **HTTP Code:** {result['http_code']}")
        lines.append(f"- **Load Time:** {result['load_time_ms']}ms")
        lines.append(f"- **Has Content:** {result['has_content']}")
        if result["console_errors"]:
            lines.append(f"- **Console Errors:** {len(result['console_errors'])}")
        if result["screenshot_path"]:
            lines.append(f"- **Screenshot:** {result['screenshot_path']}")

    with open(report_path, "w") as f:
        f.write("\n".join(lines))

    print(f"\n✅ Report saved: {report_path}")
    return report_path

async def main():
    """Main execution."""
    print("🎭 PLAYWRIGHT TESTER - Testing all deployed sites")
    print("=" * 60)

    results = await run_tests()
    summary = summarize_results(results)

    print("\n" + "=" * 60)
    print("📊 TEST SUMMARY")
    print(f"Total: {summary['total_tests']} | GREEN: {summary['green']} | YELLOW: {summary['yellow']} | RED: {summary['red']} | ERROR: {summary['error']}")
    print(f"Pass Rate: {summary['pass_rate']}")
    print(f"Avg Load: {summary['avg_load_ms']}ms")

    report_path = save_report(results, summary)

    # Save JSON results too
    json_path = "AUTOMATIONS/agent/swarm/reports/playwright_results_20260331.json"
    with open(json_path, "w") as f:
        json.dump({"summary": summary, "results": results}, f, indent=2)

    print(f"✅ JSON results: {json_path}")

if __name__ == "__main__":
    if PLAYWRIGHT_AVAILABLE:
        asyncio.run(main())
    else:
        print("❌ Playwright not available. Cannot run tests.")
