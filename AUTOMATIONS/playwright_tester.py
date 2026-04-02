#!/usr/bin/env python3
"""
Playwright Tester Agent: Test deployed surge.sh sites for health
Tests HTTP status, console errors, rendering, load time, and content visibility
"""

import asyncio
import json
import time
from datetime import datetime
from pathlib import Path
from playwright.async_api import async_playwright, Browser, Page
import sys

# Config
PROJECT_ROOT = Path(__file__).resolve().parent.parent
REPORT_DIR = PROJECT_ROOT / "AUTOMATIONS/agent/swarm/reports"
SCREENSHOT_DIR = PROJECT_ROOT / "AUTOMATIONS/agent/swarm/screenshots"
REPORT_DIR.mkdir(parents=True, exist_ok=True)
SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)

# Test sites (prioritize RED/broken ones, plus sample of others)
TEST_SITES = [
    # DNS-fixed local biz sites (previously broken due to >63 char subdomain)
    "https://auto-detailing-okc-champion.surge.sh",
    "https://mobile-detailing-okc-pure-pro.surge.sh",
    "https://window-cleaning-portland-or.surge.sh",
    "https://interior-detailing-birmingham-magic-city.surge.sh",
    "https://mobile-detailing-birmingham-al.surge.sh",
    "https://handyman-las-vegas-nv.surge.sh",
    "https://window-cleaning-louisville-ky.surge.sh",
    "https://pest-control-miami-fl.surge.sh",

    # Known RED sites (other issues)
    "https://pentecostal-streak-landing.surge.sh",
    "https://baptist-streak-landing.surge.sh",
    "https://saas-stack-audit-200.surge.sh",

    # Brand sites (priority 2)
    "https://printmaxx-site.surge.sh",
    "https://printmaxx.surge.sh",
    "https://claude-code-agent-bible.surge.sh",

    # PWA apps (priority 2)
    "https://prayerlock-web.surge.sh",
    "https://focuslock-web.surge.sh",
    "https://sleepmaxx-web.surge.sh",
    "https://ramadan-tracker.surge.sh",

    # Tool apps (priority 2)
    "https://invoiceforge.surge.sh",
    "https://pagescorer.surge.sh",
    "https://coldmaxx.surge.sh",
    "https://roicalc.surge.sh",

    # Lead magnets (priority 2)
    "https://cold-email-roi-calculator.surge.sh",
    "https://solopreneur-launch-checklist.surge.sh",
    "https://revenue-leak-audit.surge.sh",

    # Comparison pages (priority 2)
    "https://n8n-vs-zapier-vs-make.surge.sh",
    "https://cursor-vs-claudecode.surge.sh",
    "https://prayerlock-vs-hallow.surge.sh",

    # Streak landing pages (priority 3)
    "https://scripture-streak-landing.surge.sh",
    "https://quran-streak-landing.surge.sh",
    "https://torah-streak-landing.surge.sh",

    # Local biz pages (priority 3 - sample)
    "https://handyman-service-in-dallas-tx-reliable-amp-affordable-dallas-tx.surge.sh",
    "https://atlanta-electricians-mister-sparky-of-atlanta-atlanta-ga.surge.sh",
]

class SiteTest:
    def __init__(self, url: str):
        self.url = url
        self.name = url.split("https://")[1].replace(".surge.sh", "")
        self.status = None
        self.status_code = None
        self.console_errors = []
        self.console_warnings = []
        self.load_time_ms = 0
        self.screenshot = None
        self.content_visible = False
        self.page_height = 0
        self.links_broken = []
        self.result = "UNKNOWN"
        self.error_msg = ""

    async def test(self, page: Page, timeout_ms: int = 15000) -> None:
        """Test a single site"""
        try:
            start = time.time()

            # Collect console messages
            def on_console(msg):
                if msg.type == "error":
                    self.console_errors.append(msg.text)
                elif msg.type == "warning":
                    self.console_warnings.append(msg.text)

            page.on("console", on_console)

            # Navigate with timeout
            response = await page.goto(self.url, wait_until="domcontentloaded", timeout=timeout_ms)
            self.status_code = response.status if response else 999
            self.status = "OK" if response and 200 <= response.status < 400 else "ERROR"

            # Load time
            self.load_time_ms = int((time.time() - start) * 1000)

            # Check content visibility
            try:
                body_text = await page.text_content("body")
                self.content_visible = len(body_text.strip()) > 50
                self.page_height = await page.evaluate("document.body.scrollHeight")
            except:
                self.content_visible = False
                self.page_height = 0

            # Screenshot
            try:
                screenshot_path = SCREENSHOT_DIR / f"{self.name}.png"
                await page.screenshot(path=str(screenshot_path), full_page=False)
                self.screenshot = str(screenshot_path)
            except Exception as e:
                self.screenshot = f"FAILED: {str(e)}"

            # Check for blank page (height < 100px = likely blank)
            if self.page_height < 100:
                self.result = "RED"
                self.error_msg = "Blank page (height < 100px)"
            elif self.status_code != 200:
                self.result = "RED"
                self.error_msg = f"HTTP {self.status_code}"
            elif self.console_errors:
                self.result = "YELLOW"
                self.error_msg = f"{len(self.console_errors)} console errors"
            elif not self.content_visible:
                self.result = "RED"
                self.error_msg = "No content rendered"
            elif self.load_time_ms > 5000:
                self.result = "YELLOW"
                self.error_msg = f"Slow load: {self.load_time_ms}ms"
            else:
                self.result = "GREEN"

        except asyncio.TimeoutError:
            self.result = "RED"
            self.error_msg = f"Timeout after {timeout_ms}ms"
            self.status_code = 999
        except Exception as e:
            self.result = "RED"
            self.error_msg = str(e)
            self.status_code = 999

async def test_all_sites() -> dict:
    """Test all sites in parallel (limited concurrency)"""
    results = {
        "tested_at": datetime.now().isoformat(),
        "total": len(TEST_SITES),
        "green": 0,
        "yellow": 0,
        "red": 0,
        "avg_load_ms": 0,
        "sites": [],
        "summary_by_result": {"GREEN": [], "YELLOW": [], "RED": []}
    }

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            viewport={"width": 1280, "height": 720},
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
        )

        # Test with max 5 concurrent pages to avoid overload
        max_concurrent = 5
        semaphore = asyncio.Semaphore(max_concurrent)

        async def test_with_semaphore(url: str) -> SiteTest:
            async with semaphore:
                page = await context.new_page()
                try:
                    test = SiteTest(url)
                    await test.test(page)
                    return test
                finally:
                    await page.close()

        # Run all tests
        tests = await asyncio.gather(*[test_with_semaphore(url) for url in TEST_SITES])

        await context.close()
        await browser.close()

    # Aggregate results
    load_times = []
    for test in tests:
        result_data = {
            "url": test.url,
            "name": test.name,
            "result": test.result,
            "status_code": test.status_code,
            "load_time_ms": test.load_time_ms,
            "content_visible": test.content_visible,
            "page_height": test.page_height,
            "console_errors": len(test.console_errors),
            "console_warnings": len(test.console_warnings),
            "screenshot": test.screenshot,
            "error": test.error_msg
        }
        results["sites"].append(result_data)
        results["summary_by_result"][test.result].append(test.name)

        if test.result == "GREEN":
            results["green"] += 1
        elif test.result == "YELLOW":
            results["yellow"] += 1
        else:
            results["red"] += 1

        if test.load_time_ms > 0:
            load_times.append(test.load_time_ms)

    if load_times:
        results["avg_load_ms"] = int(sum(load_times) / len(load_times))

    results["pass_rate"] = f"{(results['green'] / results['total'] * 100):.1f}%"

    return results

async def main():
    print(f"[PLAYWRIGHT TESTER] Starting health check on {len(TEST_SITES)} sites...")
    print(f"[PLAYWRIGHT TESTER] Screenshots -> {SCREENSHOT_DIR}")

    results = await test_all_sites()

    # Write results to file
    report_file = REPORT_DIR / "playwright_tester_report_20260401.json"
    with open(report_file, "w") as f:
        json.dump(results, f, indent=2)

    # Print summary
    print(f"\n[PLAYWRIGHT TESTER] Results:")
    print(f"  GREEN:  {results['green']}/{results['total']}")
    print(f"  YELLOW: {results['yellow']}/{results['total']}")
    print(f"  RED:    {results['red']}/{results['total']}")
    print(f"  Pass rate: {results['pass_rate']}")
    print(f"  Avg load: {results['avg_load_ms']}ms")
    print(f"  Report: {report_file}")

    if results["red"] > 0:
        print(f"\n[PLAYWRIGHT TESTER] RED sites that need fixing:")
        for site in results["summary_by_result"]["RED"]:
            print(f"  - {site}")

    return results

if __name__ == "__main__":
    result = asyncio.run(main())
    sys.exit(0 if result["red"] == 0 else 1)
