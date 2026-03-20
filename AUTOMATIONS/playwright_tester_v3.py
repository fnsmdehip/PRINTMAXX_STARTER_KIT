#!/usr/bin/env python3
"""
PLAYWRIGHT TESTER v3 - Batch test for all deployed sites
Tests all 355 surge.sh deployments efficiently with parallel workers
"""

import asyncio
import json
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List
import subprocess
import sys

# Add common path
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeout
except ImportError:
    print("ERROR: playwright not installed. Install with: pip install playwright")
    sys.exit(1)

PROJECT_ROOT = Path(__file__).resolve().parent.parent

class PlaywrightTesterV3:
    def __init__(self):
        self.results = {
            "test_date": datetime.now().isoformat(),
            "cycle": "playwright_test_v3_2026-03-19",
            "total": 0,
            "green": 0,
            "yellow": 0,
            "red": 0,
            "tests": [],
            "by_status": {"green": [], "yellow": [], "red": []},
            "errors": {},
            "summary": {}
        }
        self.screenshot_dir = PROJECT_ROOT / "AUTOMATIONS/agent/swarm/screenshots"
        self.screenshot_dir.mkdir(parents=True, exist_ok=True)

    async def test_site(self, url: str, name: str, timeout: int = 15000) -> Dict:
        """Test a single site with Playwright"""
        result = {
            "name": name,
            "url": url,
            "status": "unknown",
            "http_status": None,
            "load_time": None,
            "errors": [],
            "warnings": [],
            "screenshot": None,
            "timestamp": datetime.now().isoformat()
        }

        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                page = await browser.new_page()

                # Set timeout
                page.set_default_timeout(timeout)

                # Collect console messages
                console_messages = []
                page.on("console", lambda msg: console_messages.append({
                    "type": msg.type,
                    "text": msg.text
                }))

                # Navigate and measure time
                import time
                start = time.time()
                try:
                    response = await page.goto(url, wait_until="domcontentloaded")
                    result["load_time"] = round((time.time() - start) * 1000, 2)
                    result["http_status"] = response.status if response else None
                except Exception as e:
                    result["errors"].append(f"Navigation error: {str(e)}")
                    result["status"] = "red"
                    await browser.close()
                    return result

                # Check content
                try:
                    body_text = await page.query_selector("body")
                    if body_text:
                        content_length = len(await page.content())
                        if content_length < 500:
                            result["warnings"].append(f"Small page ({content_length} bytes)")
                            result["status"] = "yellow"
                except:
                    pass

                # Check for console errors
                for msg in console_messages:
                    if msg["type"] == "error":
                        result["errors"].append(msg["text"])
                    elif msg["type"] == "warning":
                        result["warnings"].append(msg["text"])

                # Check HTTP status
                if result["http_status"] == 200:
                    result["status"] = "green"
                elif result["http_status"] in [404, 503, 502]:
                    result["status"] = "red"
                    result["errors"].append(f"HTTP {result['http_status']}")
                elif result["http_status"] and result["http_status"] >= 400:
                    result["status"] = "yellow"
                    result["errors"].append(f"HTTP {result['http_status']}")

                # Screenshot
                screenshot_path = self.screenshot_dir / f"{name}_{datetime.now().strftime('%Y%m%d')}.png"
                try:
                    await page.screenshot(path=str(screenshot_path), timeout=5000)
                    result["screenshot"] = str(screenshot_path)
                except:
                    result["warnings"].append("Screenshot failed")

                await browser.close()

        except PlaywrightTimeout as e:
            result["status"] = "yellow"
            result["errors"].append(f"Timeout: {str(e)}")
        except Exception as e:
            result["status"] = "red"
            result["errors"].append(f"Test error: {str(e)}")

        # Overall status logic
        if not result["status"] or result["status"] == "unknown":
            result["status"] = "yellow" if result["errors"] else "green"

        # Slow load warning
        if result["load_time"] and result["load_time"] > 3000:
            result["warnings"].append(f"Slow load: {result['load_time']}ms")
            if result["status"] == "green":
                result["status"] = "yellow"

        return result

    async def run_tests(self, urls: List[tuple], max_concurrent: int = 5):
        """Run tests concurrently"""
        semaphore = asyncio.Semaphore(max_concurrent)

        async def test_with_semaphore(url, name):
            async with semaphore:
                return await self.test_site(url, name)

        tasks = [test_with_semaphore(url, name) for url, name in urls]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        for result in results:
            if isinstance(result, Exception):
                print(f"Task error: {result}")
                continue

            self.results["tests"].append(result)
            self.results["by_status"][result["status"]].append(result["name"])

            if result["status"] == "green":
                self.results["green"] += 1
            elif result["status"] == "yellow":
                self.results["yellow"] += 1
            else:
                self.results["red"] += 1

            self.results["total"] += 1

    def load_deployed_assets(self) -> List[tuple]:
        """Load URLs from deployed_assets.json"""
        assets_file = PROJECT_ROOT / "AUTOMATIONS/agent/swarm/deployed_assets.json"
        if not assets_file.exists():
            print(f"ERROR: {assets_file} not found")
            return []

        with open(assets_file) as f:
            data = json.load(f)

        urls = []

        # Add all from assets array
        for asset in data.get("assets", []):
            urls.append((asset["url"], asset["name"]))

        # Add by_category URLs
        for category, cat_data in data.get("by_category", {}).items():
            for url in cat_data.get("urls", []):
                urls.append((f"https://{url}", url))

        print(f"Loaded {len(urls)} URLs from deployed_assets.json")
        return list(set(urls))  # Deduplicate

    def write_report(self):
        """Write report to file"""
        report_file = PROJECT_ROOT / "AUTOMATIONS/agent/swarm/reports" / "playwright_tester_report_20260319.md"
        report_file.parent.mkdir(parents=True, exist_ok=True)

        # Calculate stats
        total = self.results["total"]
        pass_rate = (self.results["green"] / total * 100) if total > 0 else 0

        # Build markdown
        lines = [
            "# Playwright Tester Report - 2026-03-19",
            "",
            f"**Cycle:** playwright_test_v3_2026-03-19",
            f"**Timestamp:** {self.results['test_date']}",
            "",
            "## Summary",
            "",
            f"- **Total Sites Tested:** {total}",
            f"- **Green (OK):** {self.results['green']}",
            f"- **Yellow (Warnings):** {self.results['yellow']}",
            f"- **Red (Failed):** {self.results['red']}",
            f"- **Pass Rate:** {pass_rate:.1f}%",
            "",
        ]

        if self.results["red"] > 0:
            lines.extend([
                "## RED Sites (Action Required)",
                "",
            ])
            for test in [t for t in self.results["tests"] if t["status"] == "red"]:
                lines.append(f"### {test['name']}")
                lines.append(f"- **URL:** {test['url']}")
                lines.append(f"- **HTTP Status:** {test['http_status']}")
                lines.append(f"- **Load Time:** {test['load_time']}ms")
                for err in test["errors"]:
                    lines.append(f"- **Error:** {err}")
                lines.append("")

        if self.results["yellow"] > 0:
            lines.extend([
                "## YELLOW Sites (Review)",
                "",
            ])
            for test in [t for t in self.results["tests"] if t["status"] == "yellow"]:
                lines.append(f"### {test['name']}")
                lines.append(f"- **URL:** {test['url']}")
                if test["warnings"]:
                    for warn in test["warnings"]:
                        lines.append(f"- **Warning:** {warn}")
                lines.append("")

        lines.extend([
            "## GREEN Sites (All OK)",
            "",
            f"✓ {self.results['green']} sites passing",
            "",
            "## Screenshots",
            "",
            f"All screenshots saved to: AUTOMATIONS/agent/swarm/screenshots/",
            "",
        ])

        report = "\n".join(lines)
        report_file.write_text(report)
        print(f"✓ Report written: {report_file}")

        return report

    def write_quality_alerts(self):
        """Write alerts for RED sites"""
        alerts_file = PROJECT_ROOT / "AUTOMATIONS/agent/swarm/quality_alerts.txt"

        if self.results["red"] == 0:
            alerts_file.write_text("✓ All quality checks passed. No alerts.\n")
            return

        alerts = []
        for test in [t for t in self.results["tests"] if t["status"] == "red"]:
            alerts.append(f"[{datetime.now().isoformat()}] RED: {test['name']} - {test['url']}")
            for err in test["errors"]:
                alerts.append(f"  └─ {err}")

        alerts_file.write_text("\n".join(alerts) + "\n")
        print(f"✓ Alerts written: {alerts_file}")

    async def run(self):
        """Main test cycle"""
        urls = self.load_deployed_assets()
        if not urls:
            print("No URLs to test")
            return

        print(f"\n🎬 Starting Playwright Tester v3...")
        print(f"Testing {len(urls)} deployed sites (concurrent: 5)")
        print("")

        await self.run_tests(urls, max_concurrent=5)

        print(f"\n✓ Tests complete: {self.results['green']} green, {self.results['yellow']} yellow, {self.results['red']} red")

        self.write_report()
        self.write_quality_alerts()

        # Update deployed_assets.json with new results
        self.update_deployed_assets()

    def update_deployed_assets(self):
        """Update deployed_assets.json with latest test results"""
        assets_file = PROJECT_ROOT / "AUTOMATIONS/agent/swarm/deployed_assets.json"

        with open(assets_file) as f:
            data = json.load(f)

        data["live_test"] = {
            "tested_at": datetime.now().isoformat(),
            "cycle": "playwright_test_v3_2026-03-19",
            "total": self.results["total"],
            "green": self.results["green"],
            "yellow": self.results["yellow"],
            "red": self.results["red"],
            "pass_rate": f"{(self.results['green'] / self.results['total'] * 100):.1f}%",
            "red_sites": self.results["by_status"]["red"],
            "yellow_sites": self.results["by_status"]["yellow"],
            "timestamp": datetime.now().isoformat()
        }

        with open(assets_file, "w") as f:
            json.dump(data, f, indent=2)

        print(f"✓ deployed_assets.json updated")


async def main():
    tester = PlaywrightTesterV3()
    await tester.run()


if __name__ == "__main__":
    asyncio.run(main())
