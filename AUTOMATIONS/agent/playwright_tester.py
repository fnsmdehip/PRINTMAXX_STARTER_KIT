#!/usr/bin/env python3
"""
PLAYWRIGHT TESTER AGENT
Tests all deployed sites on surge.sh for functionality, errors, and load times.
Generates comprehensive report and alerts.
"""

import asyncio
import json
import time
import os
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple
import subprocess

try:
    from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeout
except ImportError:
    print("Installing playwright...")
    subprocess.run([sys.executable, "-m", "pip", "install", "playwright", "-q"], check=True)
    from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeout

BASE_DIR = Path(__file__).resolve().parent.parent.parent
REPORTS_DIR = BASE_DIR / "AUTOMATIONS" / "agent" / "swarm" / "reports"
SCREENSHOTS_DIR = BASE_DIR / "AUTOMATIONS" / "agent" / "swarm" / "screenshots"
REPORTS_DIR.mkdir(parents=True, exist_ok=True)
SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)

# Priority URLs to test (key apps + recent deployments)
DEPLOYED_URLS = [
    # Key apps
    "https://truthscope.surge.sh",
    "https://prayerlock.surge.sh",
    "https://cnsnt.surge.sh",
    "https://ramadan-tracker.surge.sh",
    "https://scripture-streak.surge.sh",
    "https://focuslock.surge.sh",
    "https://hilal.surge.sh",
    # Main dashboards
    "https://printmaxx.surge.sh",
    "https://mcp-marketplace.surge.sh",
    "https://fnsmdehip-research.surge.sh",
    # Recent comparisons
    "https://claude-code-revenue-audit.surge.sh",
    "https://best-saas-tools-solopreneurs.surge.sh",
    # Health/wellness
    "https://androx-trt.surge.sh",
    "https://dosewell.surge.sh",
    "https://mens-health-hub-over-50.surge.sh",
]

class PlaywrightTester:
    def __init__(self):
        self.results = {"green": [], "yellow": [], "red": []}
        self.start_time = datetime.now()

    async def test_url(self, url: str, browser) -> Dict:
        """Test a single URL with Playwright"""
        result = {
            "url": url,
            "status": "unknown",
            "http_code": None,
            "load_time": None,
            "has_errors": False,
            "content_visible": False,
            "error_messages": [],
            "timestamp": datetime.now().isoformat(),
        }

        context = await browser.new_context()
        page = await context.new_page()

        try:
            # Collect console messages
            console_messages = []
            page.on("console", lambda msg: console_messages.append({
                "type": msg.type,
                "text": msg.text,
                "location": msg.location
            }))

            # Measure load time
            start = time.time()
            response = await page.goto(url, wait_until="networkidle", timeout=15000)
            load_time = time.time() - start

            result["load_time"] = load_time
            result["http_code"] = response.status if response else None

            # Check if content visible
            try:
                body_text = await page.evaluate("document.body.innerText")
                result["content_visible"] = len(body_text.strip()) > 50
            except:
                result["content_visible"] = False

            # Check for console errors
            errors = [m for m in console_messages if m["type"] in ["error", "warning"]]
            result["has_errors"] = len([e for e in errors if e["type"] == "error"]) > 0
            result["error_messages"] = [e["text"] for e in errors if e["type"] == "error"][:5]

            # Take screenshot (skip for speed)
            # screenshot_path = SCREENSHOTS_DIR / f"{url.replace('https://', '').replace('/', '_')}.png"
            # await page.screenshot(path=str(screenshot_path), full_page=True)
            # result["screenshot"] = str(screenshot_path)

            # Categorize
            if result["http_code"] == 200 and not result["has_errors"] and result["content_visible"] and load_time < 3:
                result["status"] = "green"
            elif result["http_code"] == 200 and result["content_visible"]:
                result["status"] = "yellow"
            else:
                result["status"] = "red"

        except PlaywrightTimeout:
            result["status"] = "red"
            result["error_messages"].append("Timeout (>15s)")
        except Exception as e:
            result["status"] = "red"
            result["error_messages"].append(str(e)[:100])
        finally:
            await context.close()

        return result

    async def run_tests(self, batch_size: int = 5):
        """Run all tests with batching"""
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)

            # Test in batches
            for i in range(0, len(DEPLOYED_URLS), batch_size):
                batch = DEPLOYED_URLS[i:i+batch_size]
                tasks = [self.test_url(url, browser) for url in batch]
                batch_results = await asyncio.gather(*tasks)

                for result in batch_results:
                    self.results[result["status"]].append(result)
                    status_char = "✓" if result["status"] == "green" else "⚠" if result["status"] == "yellow" else "✗"
                    load = result['load_time'] if result['load_time'] else 0
                    print(f"{status_char} {result['url']} ({result['http_code']}, {load:.2f}s)")

            await browser.close()

    def generate_report(self):
        """Generate markdown report"""
        total = len(self.results["green"]) + len(self.results["yellow"]) + len(self.results["red"])
        green_pct = (len(self.results["green"]) / total * 100) if total > 0 else 0

        report = f"""# PLAYWRIGHT TESTER REPORT
**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Duration:** {(datetime.now() - self.start_time).total_seconds():.1f}s

## Summary
- **Total URLs:** {total}
- **Green (OK):** {len(self.results["green"])} ({green_pct:.1f}%)
- **Yellow (Warnings):** {len(self.results["yellow"])}
- **Red (Broken):** {len(self.results["red"])}

## Green Sites ✓
"""
        for r in self.results["green"][:20]:  # Top 20
            report += f"\n- [{r['url'].replace('https://', '')}]({r['url']}) - {r['load_time']:.2f}s"

        report += "\n\n## Yellow Sites ⚠\n"
        for r in self.results["yellow"]:
            report += f"\n- [{r['url'].replace('https://', '')}]({r['url']}) - {r['load_time']:.2f}s"
            if r["error_messages"]:
                report += f"\n  - Errors: {', '.join(r['error_messages'][:3])}"

        report += "\n\n## Red Sites ✗ (NEEDS FIXING)\n"
        for r in self.results["red"]:
            report += f"\n- [{r['url'].replace('https://', '')}]({r['url']}) - HTTP {r['http_code']}"
            if r["error_messages"]:
                report += f"\n  - {r['error_messages'][0]}"

        report += f"\n\n## Details\n```json\n{json.dumps(self.results, indent=2, default=str)}\n```"

        return report

    async def main(self):
        """Main execution"""
        print(f"🎬 Testing {len(DEPLOYED_URLS)} deployed sites...\n")
        await self.run_tests()

        # Generate report
        report = self.generate_report()
        report_file = REPORTS_DIR / f"playwright_tester_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        report_file.write_text(report)
        print(f"\n📄 Report: {report_file}")

        # Summary
        print(f"\n📊 Summary:")
        print(f"   Green:  {len(self.results['green'])}")
        print(f"   Yellow: {len(self.results['yellow'])}")
        print(f"   Red:    {len(self.results['red'])}")

        return self.results

if __name__ == "__main__":
    tester = PlaywrightTester()
    try:
        asyncio.run(tester.main())
    except KeyboardInterrupt:
        print("\n⏸ Test interrupted")
        sys.exit(1)
