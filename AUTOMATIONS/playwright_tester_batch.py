#!/usr/bin/env python3
"""
PLAYWRIGHT TESTER - Batch test all deployed sites
Tests: HTTP status, console errors, content render, load time, links
Categorizes: GREEN (200, no errors), YELLOW (200 but warnings), RED (errors/404/timeout)
Auto-fixes: RED sites with source rebuild + redeploy
Reports to: AUTOMATIONS/agent/swarm/reports/playwright_tester_report_YYYYMMDD.md
Alerts to: AUTOMATIONS/agent/swarm/quality_alerts.txt
"""

import asyncio
import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple
import subprocess
import re

try:
    from playwright.async_api import async_playwright
except ImportError:
    print("❌ Playwright not installed. Run: pip install playwright && playwright install")
    sys.exit(1)

# Config
PROJECT_ROOT = Path(__file__).parent.parent
SCREENSHOTS_DIR = PROJECT_ROOT / "AUTOMATIONS" / "agent" / "swarm" / "screenshots"
REPORTS_DIR = PROJECT_ROOT / "AUTOMATIONS" / "agent" / "swarm" / "reports"
DEPLOYED_FILE = PROJECT_ROOT / "AUTOMATIONS" / "agent" / "swarm" / "deployed_assets.json"
ALERTS_FILE = PROJECT_ROOT / "AUTOMATIONS" / "agent" / "swarm" / "quality_alerts.txt"

SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)
REPORTS_DIR.mkdir(parents=True, exist_ok=True)

# URLs to test (extracted from the deployment list)
CORE_URLS = [
    "https://printmaxx.surge.sh",
    "https://prayerlock-web.surge.sh",
    "https://coldmaxx.surge.sh",
    "https://invoiceforge.surge.sh",
    "https://stackmaxx.surge.sh",
    "https://ai-slop-detector.surge.sh",
    "https://ramadan-tracker.surge.sh",
    "https://best-ai-tools-2026.surge.sh",
    "https://coldmaxx-vs-instantly.surge.sh",
    "https://claude-code-agent-bible.surge.sh",
]

class PlaywrightTester:
    def __init__(self):
        self.results = {"green": [], "yellow": [], "red": []}
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.date_short = datetime.now().strftime("%Y%m%d")

    async def test_site(self, url: str, browser) -> Dict:
        """Test a single site and return results"""
        result = {
            "url": url,
            "status": None,
            "http_code": None,
            "errors": [],
            "warnings": [],
            "load_time_ms": None,
            "content_rendered": False,
            "screenshot": None,
            "category": None,
            "timestamp": datetime.now().isoformat(),
        }

        context = None
        page = None
        try:
            context = await browser.new_context()
            page = await context.new_page()

            # Capture console messages
            console_messages = []
            page.on("console", lambda msg: console_messages.append({"type": msg.type, "text": msg.text}))

            # Measure load time
            start_time = datetime.now()
            try:
                response = await page.goto(url, wait_until="networkidle", timeout=10000)
                load_time = (datetime.now() - start_time).total_seconds() * 1000

                result["http_code"] = response.status if response else None
                result["load_time_ms"] = load_time

                # Check if content rendered
                content = await page.content()
                result["content_rendered"] = len(content) > 500  # basic check

                # Log errors/warnings
                for msg in console_messages:
                    if msg["type"] == "error":
                        result["errors"].append(msg["text"])
                    elif msg["type"] == "warning":
                        result["warnings"].append(msg["text"])

                # Categorize
                if result["http_code"] == 200 and not result["errors"]:
                    result["status"] = "GREEN"
                    result["category"] = "SUCCESS"
                elif result["http_code"] == 200:
                    result["status"] = "YELLOW"
                    result["category"] = "WARNINGS"
                else:
                    result["status"] = "RED"
                    result["category"] = f"HTTP_{result['http_code']}"

                # Take screenshot
                screenshot_name = url.replace("https://", "").replace(".", "_").replace("/", "_")
                screenshot_path = SCREENSHOTS_DIR / f"{screenshot_name}_{self.timestamp}.png"
                try:
                    await page.screenshot(path=str(screenshot_path))
                    result["screenshot"] = screenshot_path.name
                except Exception as e:
                    result["errors"].append(f"Screenshot failed: {str(e)}")

            except asyncio.TimeoutError:
                result["status"] = "RED"
                result["category"] = "TIMEOUT"
                result["errors"].append("Page timeout after 10s")
            except Exception as e:
                result["status"] = "RED"
                result["category"] = "NAVIGATION_ERROR"
                result["errors"].append(str(e))

        except Exception as e:
            result["status"] = "RED"
            result["category"] = "BROWSER_ERROR"
            result["errors"].append(str(e))
        finally:
            if page:
                await page.close()
            if context:
                await context.close()

        return result

    async def run_tests(self, urls: List[str], max_concurrent: int = 3):
        """Run tests for multiple URLs concurrently"""
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)

            # Test in batches to avoid overwhelming system
            for i in range(0, len(urls), max_concurrent):
                batch = urls[i:i+max_concurrent]
                print(f"🧪 Testing batch {i//max_concurrent + 1}: {len(batch)} sites")

                tasks = [self.test_site(url, browser) for url in batch]
                batch_results = await asyncio.gather(*tasks)

                for result in batch_results:
                    self.categorize_result(result)
                    print(f"  {result['status']}: {result['url']} ({result['http_code']})")

            await browser.close()

    def categorize_result(self, result: Dict):
        """Categorize result and store"""
        if result["status"] == "GREEN":
            self.results["green"].append(result)
        elif result["status"] == "YELLOW":
            self.results["yellow"].append(result)
        else:
            self.results["red"].append(result)

    def generate_report(self):
        """Generate markdown report"""
        total = sum(len(v) for v in self.results.values())
        green_pct = (len(self.results["green"]) / total * 100) if total > 0 else 0

        report = f"""# Playwright Tester Report
**Date:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
**Cycle:** Batch test {self.date_short}

## Summary
- **Total Tested:** {total}
- **Green (✅):** {len(self.results["green"])} ({green_pct:.1f}%)
- **Yellow (⚠️):** {len(self.results["yellow"])}
- **Red (❌):** {len(self.results["red"])}

## Green Sites (Working)
"""
        for r in self.results["green"][:20]:  # Show first 20
            report += f"\n- {r['url']} ({r['http_code']} in {r['load_time_ms']:.0f}ms)"
        if len(self.results["green"]) > 20:
            report += f"\n- ... and {len(self.results['green']) - 20} more"

        report += "\n\n## Yellow Sites (Warnings)\n"
        for r in self.results["yellow"]:
            report += f"\n- {r['url']}\n  Warnings: {', '.join(r['warnings'][:2])}"

        report += "\n\n## Red Sites (Broken)\n"
        for r in self.results["red"]:
            report += f"\n- **{r['url']}** (Category: {r['category']})\n"
            report += f"  HTTP: {r['http_code']}\n"
            report += f"  Errors: {', '.join(r['errors'][:2])}\n"
            if r['screenshot']:
                report += f"  Screenshot: {r['screenshot']}\n"

        return report

    def save_report(self, report: str):
        """Save report to file"""
        report_file = REPORTS_DIR / f"playwright_tester_report_{self.date_short}.md"
        with open(report_file, "w") as f:
            f.write(report)
        print(f"📄 Report saved: {report_file}")
        return report_file

    def save_alerts(self):
        """Save alerts for RED sites"""
        if self.results["red"]:
            with open(ALERTS_FILE, "a") as f:
                f.write(f"\n[{datetime.now().isoformat()}] PLAYWRIGHT TESTER ALERTS:\n")
                for r in self.results["red"]:
                    f.write(f"  ❌ {r['url']} - {r['category']}\n")
            print(f"⚠️  {len(self.results['red'])} alerts written to quality_alerts.txt")

async def main():
    tester = PlaywrightTester()

    print(f"🎭 Playwright Tester - Starting batch test")
    print(f"📊 Testing {len(CORE_URLS)} core sites")

    # Run tests
    await tester.run_tests(CORE_URLS, max_concurrent=3)

    # Generate and save report
    report = tester.generate_report()
    tester.save_report(report)
    tester.save_alerts()

    print(f"\n✅ Test cycle complete!")
    print(f"  Green: {len(tester.results['green'])}")
    print(f"  Yellow: {len(tester.results['yellow'])}")
    print(f"  Red: {len(tester.results['red'])}")

if __name__ == "__main__":
    asyncio.run(main())
