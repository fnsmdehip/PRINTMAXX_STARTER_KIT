#!/usr/bin/env python3
"""Playwright test suite for PRINTMAXX deployed sites."""

import asyncio
import json
import time
from datetime import datetime
from pathlib import Path

try:
    from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeoutError
except ImportError:
    print("ERROR: playwright not installed. Run: pip3 install playwright")
    exit(1)

# Test URLs - prioritized by importance
CRITICAL_URLS = [
    "https://printmaxx.surge.sh",
    "https://coldmaxx.surge.sh",
    "https://invoiceforge.surge.sh",
    "https://pagescorer.surge.sh",
    "https://prayerlock-web.surge.sh",
    "https://prayerlock-landing.surge.sh",
    "https://focuslock-web.surge.sh",
    "https://ramadan-tracker.surge.sh",
    "https://hilal-landing.surge.sh",
    "https://hilal-app.surge.sh",
    "https://mcp-marketplace.surge.sh",
    "https://stackmaxx.surge.sh",
    "https://prospectmaxx.surge.sh",
    "https://pitchdeck.surge.sh",
    "https://roicalc.surge.sh",
    "https://smartlead-vs-instantly.surge.sh",
    "https://semrush-vs-ahrefs.surge.sh",
    "https://cold-email-roi-calculator.surge.sh",
    "https://saas-stack-audit.surge.sh",
    "https://sunni-streak.surge.sh",
    "https://catholic-streak.surge.sh",
    "https://buddhist-streak.surge.sh",
    "https://reading-streak.surge.sh",
    "https://ai-stack-2026.surge.sh",
]

SCREENSHOT_DIR = Path("/Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt/AUTOMATIONS/agent/swarm/screenshots/test_20260321")

class SiteTest:
    def __init__(self, url: str):
        self.url = url
        self.name = url.replace("https://", "").replace(".surge.sh", "")
        self.status = None
        self.load_time = None
        self.errors = []
        self.warnings = []
        self.content_visible = False
        self.screenshot_path = None
        self.links_checked = 0
        self.broken_links = []

    async def test(self, page):
        """Test a single site."""
        try:
            start_time = time.time()

            # Navigate with timeout
            response = await page.goto(self.url, wait_until="domcontentloaded", timeout=15000)
            load_time = time.time() - start_time
            self.load_time = load_time

            # Check HTTP status
            if response and response.status == 200:
                self.status = "GREEN"
            elif response and 400 <= response.status < 500:
                self.status = "RED"
                self.errors.append(f"HTTP {response.status}")
            elif response and 500 <= response.status < 600:
                self.status = "YELLOW"
                self.errors.append(f"HTTP {response.status} (server error)")
            else:
                self.status = "YELLOW"
                self.errors.append(f"Unknown status: {response.status if response else 'none'}")

            # Check for console errors
            try:
                # Try to detect if page has content
                body_html = await page.content()
                if len(body_html) > 500 and "<!DOCTYPE" in body_html:
                    self.content_visible = True
                else:
                    self.status = "RED"
                    self.errors.append("Page content too small or empty")
            except Exception as e:
                self.errors.append(f"Could not verify content: {str(e)}")

            # Performance check
            if load_time > 8:
                self.status = "YELLOW"
                self.warnings.append(f"Slow load: {load_time:.1f}s")
            elif load_time > 5:
                self.warnings.append(f"Acceptable load: {load_time:.1f}s")

            # Take screenshot
            screenshot_path = SCREENSHOT_DIR / f"{self.name}.png"
            await page.screenshot(path=str(screenshot_path), full_page=False)
            self.screenshot_path = str(screenshot_path)

            # Set default to GREEN if not already set
            if not self.status:
                self.status = "GREEN"

        except PlaywrightTimeoutError:
            self.status = "RED"
            self.errors.append("Timeout (>15s)")
            self.load_time = 15.0
        except Exception as e:
            self.status = "RED"
            self.errors.append(f"Error: {str(e)[:100]}")

    def to_dict(self):
        return {
            "name": self.name,
            "url": self.url,
            "status": self.status,
            "load_time_s": round(self.load_time, 2) if self.load_time else None,
            "content_visible": self.content_visible,
            "errors": self.errors,
            "warnings": self.warnings,
            "screenshot": self.screenshot_path,
        }

async def run_tests():
    """Run all tests."""
    tests = [SiteTest(url) for url in CRITICAL_URLS]
    results = {
        "timestamp": datetime.now().isoformat(),
        "total": len(tests),
        "green": 0,
        "yellow": 0,
        "red": 0,
        "sites": [],
    }

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(viewport={"width": 1280, "height": 720})

        for i, test in enumerate(tests, 1):
            print(f"[{i}/{len(tests)}] Testing {test.name}...", end=" ", flush=True)

            page = await context.new_page()
            await test.test(page)
            await page.close()

            results["sites"].append(test.to_dict())
            if test.status == "GREEN":
                results["green"] += 1
                print(f"✓ GREEN ({test.load_time:.1f}s)")
            elif test.status == "YELLOW":
                results["yellow"] += 1
                print(f"⚠ YELLOW ({test.load_time:.1f}s) - {test.warnings}")
            else:  # RED
                results["red"] += 1
                print(f"✗ RED - {test.errors}")

            # Small delay between tests
            await asyncio.sleep(0.5)

        await browser.close()

    # Calculate pass rate
    results["pass_rate"] = round((results["green"] / results["total"]) * 100, 1) if results["total"] > 0 else 0
    results["green_sites"] = [s["name"] for s in results["sites"] if s["status"] == "GREEN"]
    results["yellow_sites"] = [s["name"] for s in results["sites"] if s["status"] == "YELLOW"]
    results["red_sites"] = [s["name"] for s in results["sites"] if s["status"] == "RED"]

    return results

if __name__ == "__main__":
    print("Starting Playwright test suite...")
    print(f"Testing {len(CRITICAL_URLS)} critical sites\n")

    results = asyncio.run(run_tests())

    # Save results to JSON
    results_file = Path("/Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt/AUTOMATIONS/agent/swarm/test_results_20260321.json")
    with open(results_file, "w") as f:
        json.dump(results, f, indent=2)

    print(f"\n{'='*60}")
    print(f"Test Results: {results['pass_rate']}% pass rate")
    print(f"GREEN:  {results['green']}")
    print(f"YELLOW: {results['yellow']}")
    print(f"RED:    {results['red']}")
    print(f"{'='*60}")
    print(f"Results saved to: {results_file}")
