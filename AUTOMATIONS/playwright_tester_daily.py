#!/usr/bin/env python3
"""
PLAYWRIGHT TESTER - Daily Health Check (2026-03-20)
Tests deployed surge.sh sites for:
- HTTP status (200 = GREEN, 3xx/4xx = RED, warnings = YELLOW)
- Console errors and warnings
- Page load time (target < 3s)
- Content visibility (not blank)
- Screenshots for proof
"""

import asyncio
import json
import time
from datetime import datetime
from pathlib import Path
from playwright.async_api import async_playwright, Browser, Page
import sys

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SCREENSHOTS_DIR = PROJECT_ROOT / "AUTOMATIONS/agent/swarm/screenshots"
REPORTS_DIR = PROJECT_ROOT / "AUTOMATIONS/agent/swarm/reports"

# Key sites to test from each category
TEST_SITES = [
    # FLAGGED YELLOW (performance) - need improvement check
    ("https://invoiceforge.surge.sh", "tool_app", "FLAGGED_SLOW"),
    ("https://prayerlock-web.surge.sh", "pwa_app", "FLAGGED_SLOW"),
    ("https://pdfmaxx.surge.sh", "pwa_app", "FLAGGED_SLOW"),

    # Core brand pages
    ("https://printmaxx.surge.sh", "brand", "CORE"),
    ("https://printmaxx-tools.surge.sh", "brand", "CORE"),

    # Tool apps (key revenue)
    ("https://coldmaxx.surge.sh", "tool_app", "KEY"),
    ("https://stackmaxx.surge.sh", "tool_app", "KEY"),
    ("https://pagescorer.surge.sh", "tool_app", "KEY"),

    # PWA apps (high value)
    ("https://coreday.surge.sh", "pwa_app", "HIGH_VALUE"),
    ("https://ramadan-tracker.surge.sh", "pwa_app", "TIME_CRITICAL"),
    ("https://walktounlock-web.surge.sh", "pwa_app", "HIGH_VALUE"),

    # Comparison pages
    ("https://semrush-vs-ahrefs.surge.sh", "comparison", "AFFILIATE"),
    ("https://prayerlock-vs-hallow.surge.sh", "comparison", "AFFILIATE"),

    # Lead magnets
    ("https://cold-email-roi-calculator.surge.sh", "lead_magnet", "HIGH_VALUE"),
    ("https://saas-stack-audit.surge.sh", "lead_magnet", "HIGH_VALUE"),

    # Denomination streaks
    ("https://sunni-streak.surge.sh", "denomination_app", "VOLUME"),
    ("https://catholic-streak.surge.sh", "denomination_app", "VOLUME"),
    ("https://buddhist-streak.surge.sh", "denomination_app", "VOLUME"),

    # Local biz pages (volume)
    ("https://spodak-dental-group-miami-fl.surge.sh", "local_biz", "VOLUME"),
    ("https://milestone-electric-a-c-plumbing-dallas-tx.surge.sh", "local_biz", "VOLUME"),
    ("https://goldsberry-portz-divorce-family-lawyers-pllc-houston-tx.surge.sh", "local_biz", "VOLUME"),

    # Fiverr service pages
    ("https://printmaxx-website-design.surge.sh", "fiverr_service", "MONETIZE"),
    ("https://printmaxx-cold-email.surge.sh", "fiverr_service", "MONETIZE"),

    # Others
    ("https://mcp-marketplace.surge.sh", "brand", "CORE"),
    ("https://claude-code-agent-bible.surge.sh", "product", "HIGH_VALUE"),
]

class PlaywrightTester:
    def __init__(self):
        self.results = {
            "tested_at": datetime.now().isoformat(),
            "cycle": "playwright_tester_daily_20260320",
            "total": len(TEST_SITES),
            "green": 0,
            "yellow": 0,
            "red": 0,
            "green_sites": [],
            "yellow_sites": [],
            "red_sites": [],
            "performance_issues": [],
            "console_errors": {},
            "issues": {},
        }
        self.console_logs = {}

    async def test_site(self, browser: Browser, url: str, category: str, priority: str) -> dict:
        """Test a single site"""
        try:
            page = await browser.new_page()
            page.set_default_timeout(15000)

            console_logs = []
            errors = []

            def handle_console(msg):
                console_logs.append({"type": msg.type, "text": msg.text})
                if msg.type in ("error", "warning"):
                    errors.append({"type": msg.type, "text": msg.text})

            page.on("console", handle_console)

            start_time = time.time()

            try:
                response = await page.goto(url, wait_until="domcontentloaded")
                load_time = time.time() - start_time
                http_status = response.status if response else 0
            except Exception as e:
                load_time = time.time() - start_time
                http_status = 0
                errors.append({"type": "navigation_error", "text": str(e)})

            # Check content visibility
            try:
                content_visible = await page.locator("body").is_visible()
                body_text = await page.locator("body").inner_text()
                content_blank = len(body_text.strip()) < 50
            except:
                content_visible = False
                content_blank = True

            # Take screenshot
            screenshot_name = f"{url.split('://')[1].split('/')[0]}_20260320.png"
            screenshot_path = SCREENSHOTS_DIR / screenshot_name
            try:
                await page.screenshot(path=str(screenshot_path), full_page=False)
            except:
                screenshot_path = None

            await page.close()

            # Determine status
            if http_status == 200 and content_visible and not content_blank and not errors:
                status = "GREEN"
                self.results["green"] += 1
            elif http_status == 200 and load_time > 3.0:
                status = "YELLOW"
                self.results["yellow"] += 1
                self.results["performance_issues"].append(f"{url} ({load_time:.1f}s)")
            elif http_status == 200 and errors:
                status = "YELLOW"
                self.results["yellow"] += 1
            else:
                status = "RED"
                self.results["red"] += 1

            result = {
                "url": url,
                "category": category,
                "priority": priority,
                "status": status,
                "http_status": http_status,
                "load_time": round(load_time, 2),
                "content_visible": content_visible,
                "content_blank": content_blank,
                "errors": len(errors),
                "screenshot": str(screenshot_path) if screenshot_path else None,
            }

            if status == "GREEN":
                self.results["green_sites"].append(f"{url} ({load_time:.1f}s)")
            elif status == "YELLOW":
                self.results["yellow_sites"].append(f"{url} ({load_time:.1f}s) - {len(errors)} warnings")
            else:
                self.results["red_sites"].append(f"{url} (HTTP {http_status})")

            if errors:
                self.results["console_errors"][url] = errors

            if http_status != 200 or errors:
                self.results["issues"][url] = {
                    "http_status": http_status,
                    "console_errors": errors,
                    "content_visible": content_visible,
                }

            return result

        except Exception as e:
            self.results["red"] += 1
            self.results["red_sites"].append(f"{url} (CRASH: {str(e)[:50]})")
            self.results["issues"][url] = {"error": str(e)}
            return {"url": url, "status": "RED", "error": str(e)}

    async def run(self):
        """Run all tests"""
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)

            # Test in parallel (max 5 at a time to avoid rate limits)
            for i in range(0, len(TEST_SITES), 5):
                batch = TEST_SITES[i:i+5]
                tasks = [self.test_site(browser, url, cat, priority) for url, cat, priority in batch]
                results = await asyncio.gather(*tasks)
                print(f"✓ Tested batch {i//5 + 1} ({len(batch)} sites)")

            await browser.close()

        # Save results
        self.results["pass_rate"] = f"{(self.results['green'] / self.results['total'] * 100):.1f}%"

        report_path = REPORTS_DIR / "playwright_tester_report_20260320.md"
        with open(report_path, "w") as f:
            f.write(f"# PLAYWRIGHT TESTER REPORT — {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write(f"**Cycle:** {self.results['cycle']}\n")
            f.write(f"**Results:** {self.results['green']} GREEN | {self.results['yellow']} YELLOW | {self.results['red']} RED\n")
            f.write(f"**Pass Rate:** {self.results['pass_rate']}\n\n")

            if self.results["green_sites"]:
                f.write("## ✅ GREEN (Healthy)\n")
                for site in sorted(self.results["green_sites"]):
                    f.write(f"- {site}\n")
                f.write("\n")

            if self.results["yellow_sites"]:
                f.write("## ⚠️ YELLOW (Performance/Warnings)\n")
                for site in sorted(self.results["yellow_sites"]):
                    f.write(f"- {site}\n")
                f.write("\n")

            if self.results["red_sites"]:
                f.write("## ❌ RED (Broken)\n")
                for site in sorted(self.results["red_sites"]):
                    f.write(f"- {site}\n")
                f.write("\n")

            if self.results["issues"]:
                f.write("## Issues Found\n")
                for url, issue in self.results["issues"].items():
                    f.write(f"### {url}\n")
                    for k, v in issue.items():
                        f.write(f"- **{k}:** {v}\n")
                    f.write("\n")

        # Save JSON results
        json_path = REPORTS_DIR / "playwright_tester_results_20260320.json"
        with open(json_path, "w") as f:
            json.dump(self.results, f, indent=2)

        print(f"\n✓ Report saved: {report_path}")
        print(f"✓ Results saved: {json_path}")
        print(f"\n📊 SUMMARY: {self.results['green']} GREEN | {self.results['yellow']} YELLOW | {self.results['red']} RED ({self.results['pass_rate']})")

        return self.results

if __name__ == "__main__":
    tester = PlaywrightTester()
    results = asyncio.run(tester.run())

    # Alert on RED sites
    if results["red"] > 0:
        alert_path = PROJECT_ROOT / "AUTOMATIONS/agent/swarm/quality_alerts.txt"
        with open(alert_path, "a") as f:
            f.write(f"\n[{datetime.now().isoformat()}] PLAYWRIGHT ALERT: {results['red']} RED sites found\n")
            for site in results["red_sites"]:
                f.write(f"  - {site}\n")
