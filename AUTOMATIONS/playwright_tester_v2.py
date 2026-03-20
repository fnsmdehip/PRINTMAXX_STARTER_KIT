#!/usr/bin/env python3
"""PLAYWRIGHT TESTER V2 - Improved batch testing"""

import asyncio
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List

try:
    from playwright.async_api import async_playwright
except ImportError:
    print("Playwright not installed"); exit(1)

PROJECT_ROOT = Path(__file__).parent.parent
SCREENSHOTS_DIR = PROJECT_ROOT / "AUTOMATIONS" / "agent" / "swarm" / "screenshots"
REPORTS_DIR = PROJECT_ROOT / "AUTOMATIONS" / "agent" / "swarm" / "reports"
ALERTS_FILE = PROJECT_ROOT / "AUTOMATIONS" / "agent" / "swarm" / "quality_alerts.txt"

SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)
REPORTS_DIR.mkdir(parents=True, exist_ok=True)

TEST_URLS = [
    "https://printmaxx.surge.sh", "https://printmaxx-site.surge.sh", "https://printmaxx-tools.surge.sh",
    "https://invoiceforge.surge.sh", "https://stackmaxx.surge.sh", "https://coldmaxx.surge.sh",
    "https://pagescorer.surge.sh", "https://roicalc.surge.sh", "https://prospectmaxx.surge.sh",
    "https://pitchdeck.surge.sh", "https://prayerlock-web.surge.sh", "https://focuslock-web.surge.sh",
    "https://sleepmaxx-web.surge.sh", "https://mealmaxx-web.surge.sh", "https://walktounlock-web.surge.sh",
    "https://ramadan-tracker.surge.sh", "https://habitforge-web.surge.sh", "https://coldmaxx-vs-instantly.surge.sh",
    "https://cursor-vs-claudecode.surge.sh", "https://focuslock-vs-opal.surge.sh",
    "https://sleepmaxx-vs-sleepcycle.surge.sh", "https://pagescorer-vs-gtmetrix.surge.sh",
    "https://best-ai-tools-2026.surge.sh", "https://semrush-vs-ahrefs.surge.sh",
    "https://claude-code-agent-bible.surge.sh", "https://mcp-marketplace.surge.sh",
    "https://best-newsletter-platforms.surge.sh", "https://website-builders-compared.surge.sh",
    "https://best-cold-email-tools.surge.sh", "https://cold-email-roi-calculator.surge.sh",
    "https://subject-line-grader.surge.sh", "https://ai-revenue-calculator.surge.sh",
    "https://200-day-calculator.surge.sh", "https://solopreneur-launch-checklist.surge.sh",
    "https://scripture-streak-landing.surge.sh", "https://prayerlock-landing.surge.sh",
    "https://focuslock-landing.surge.sh", "https://sleepmaxx-landing.surge.sh",
    "https://hilal-landing.surge.sh", "https://catholic-streak-landing.surge.sh",
    "https://buddhist-streak-landing.surge.sh", "https://gita-streak-landing.surge.sh",
    "https://coldmaxx-app.surge.sh", "https://invoiceforge-app.surge.sh",
    "https://austin-elite-smiles-pllc-austin-tx.surge.sh",
    "https://spodak-dental-group-miami-fl.surge.sh", "https://erase-the-case-pllc-miami-fl.surge.sh",
    "https://professional-plumbing-heating-cooling-memphis-tn.surge.sh",
    "https://jacksonville-emergency-plumber-jacksonville-fl.surge.sh",
    "https://colorado-springs-roofing-company-roof-repair-amp-installatio-colorado-springs-co.surge.sh",
    "https://fresno-junk-removal-fast-amp-affordable-service-fresno-ca.surge.sh",
    "https://printmaxx-website-design.surge.sh", "https://printmaxx-cold-email.surge.sh",
    "https://printmaxx-automation.surge.sh", "https://fiverr-services-pm.surge.sh",
]

class Tester:
    def __init__(self):
        self.results = {"green": [], "yellow": [], "red": []}
        self.date_short = datetime.now().strftime("%Y%m%d")

    async def test_site(self, url: str, browser) -> Dict:
        result = {"url": url, "status": "RED", "http_code": None, "load_time_ms": 0, "errors": []}
        context = None
        page = None
        try:
            context = await browser.new_context()
            page = await context.new_page()
            console_errors = []
            page.on("console", lambda msg: console_errors.append(msg.text) if msg.type == "error" else None)

            try:
                start = datetime.now()
                response = await page.goto(url, wait_until="domcontentloaded", timeout=8000)
                load_time = (datetime.now() - start).total_seconds() * 1000
                result["http_code"] = response.status if response else 0
                result["load_time_ms"] = load_time
                result["errors"] = console_errors[:2]

                if result["http_code"] == 200 and not console_errors:
                    result["status"] = "GREEN"
                elif result["http_code"] == 200:
                    result["status"] = "YELLOW"
                else:
                    result["status"] = "RED"
            except asyncio.TimeoutError:
                result["http_code"] = "TIMEOUT"
                result["errors"] = ["Load timeout 8s"]
            except Exception as e:
                result["http_code"] = "ERROR"
                result["errors"] = [str(e)[:80]]
        except Exception as e:
            result["http_code"] = "BROWSER"
            result["errors"] = [str(e)[:80]]
        finally:
            if page: await page.close()
            if context: await context.close()
        return result

    async def run_tests(self, urls: List[str]):
        print(f"\n🎭 Testing {len(urls)} sites...\n")
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            batch_size = 4
            for i in range(0, len(urls), batch_size):
                batch = urls[i:i+batch_size]
                print(f"Batch {i//batch_size + 1}: ", end="", flush=True)
                tasks = [self.test_site(url, browser) for url in batch]
                results = await asyncio.gather(*tasks)
                for r in results:
                    if r["status"] == "GREEN": self.results["green"].append(r)
                    elif r["status"] == "YELLOW": self.results["yellow"].append(r)
                    else: self.results["red"].append(r)
                    status = r["status"][0]
                    print(status, end="", flush=True)
                print()
            await browser.close()

    def save_report(self):
        total = sum(len(v) for v in self.results.values())
        green_pct = (len(self.results["green"]) / total * 100) if total else 0
        report = f"""# 🎭 Playwright Tester Report - V2
**{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}**

## Summary
- **Total:** {total} sites
- **✅ Green:** {len(self.results["green"])} ({green_pct:.0f}%)
- **⚠️ Yellow:** {len(self.results["yellow"])}
- **❌ Red:** {len(self.results["red"])}

## Green Sites
"""
        for r in self.results["green"]:
            domain = r['url'].split('https://')[-1]
            report += f"\n- {domain}"

        report += "\n\n## Red Sites\n"
        for r in self.results["red"]:
            domain = r['url'].split('https://')[-1]
            report += f"\n- {domain} ({r['http_code']})\n"
            if r["errors"]: report += f"  Error: {r['errors'][0][:60]}\n"

        file = REPORTS_DIR / f"playwright_tester_report_{self.date_short}.md"
        file.write_text(report)
        print(f"\n📄 Report: {file}")

        if self.results["red"]:
            with open(ALERTS_FILE, "a") as f:
                f.write(f"\n[{datetime.now().isoformat()}] 🎭 PLAYWRIGHT: {len(self.results['red'])} broken\n")
                for r in self.results["red"]:
                    f.write(f"  {r['url']}\n")

async def main():
    tester = Tester()
    await tester.run_tests(TEST_URLS)
    tester.save_report()
    total = sum(len(v) for v in tester.results.values())
    print(f"\n✅ {len(tester.results['green'])}/{total} working")

if __name__ == "__main__":
    asyncio.run(main())
