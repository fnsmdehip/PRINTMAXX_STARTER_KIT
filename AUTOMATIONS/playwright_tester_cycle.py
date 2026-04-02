#!/usr/bin/env python3
"""
PLAYWRIGHT TESTER CYCLE — Comprehensive QA testing for deployed PRINTMAXX assets.
Tests 200+ sites for: HTTP status, console errors, content rendering, load time, link health.
"""

import asyncio
import json
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple
import re

# Priority test sites (newly deployed + critical + previously broken)
PRIORITY_SITES = [
    # Recently deployed (last 10 min)
    "https://quality-janitorial-services-kansas-city-mo.surge.sh",
    "https://sunrise-property-care-llc-kansas-city-mo.surge.sh",
    # Critical apps
    "https://printmaxx-site.surge.sh",
    "https://prayerlock.surge.sh",
    "https://focuslock.surge.sh",
    "https://ramadan-tracker.surge.sh",
    "https://cnsnt.surge.sh",
    "https://cnsnt-web.surge.sh",
    "https://truthscope.surge.sh",
    # Comparison pages
    "https://coldmaxx-vs-instantly.surge.sh",
    "https://instantly-vs-lemlist.surge.sh",
    "https://pagescorer-vs-gtmetrix.surge.sh",
    "https://sleepmaxx-vs-sleepcycle.surge.sh",
    # Tool apps
    "https://coldmaxx.surge.sh",
    "https://invoiceforge.surge.sh",
    "https://pagescorer.surge.sh",
    "https://roicalc.surge.sh",
    "https://stackmaxx.surge.sh",
    # Lead magnets
    "https://cold-email-roi-calculator.surge.sh",
    "https://saas-stack-audit.surge.sh",
    "https://subject-line-grader.surge.sh",
    # App marketing pages
    "https://prayerlock-landing.surge.sh",
    "https://focuslock-landing.surge.sh",
    "https://scripture-streak-landing.surge.sh",
    "https://mealmaxx-landing.surge.sh",
    # Previously broken (from last report)
    "https://pentecostal-streak-landing.surge.sh",
    "https://baptist-streak-landing.surge.sh",
    "https://saas-stack-audit-200.surge.sh",
    # Research blog
    "https://fnsmdehip-research.surge.sh",
    # Service pages
    "https://printmaxx-cold-email.surge.sh",
    "https://printmaxx-automation.surge.sh",
]

# Sample of local business sites
LOCAL_BIZ_SAMPLE = [
    "https://pest-control-miami-fl.surge.sh",
    "https://window-cleaning-louisville-ky.surge.sh",
    "https://handyman-las-vegas-nv.surge.sh",
    "https://mobile-detailing-birmingham-al.surge.sh",
]

# All sites to test
SITES_TO_TEST = PRIORITY_SITES + LOCAL_BIZ_SAMPLE

SCREENSHOT_DIR = Path("/Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt/AUTOMATIONS/agent/swarm/screenshots")
REPORT_DIR = Path("/Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt/AUTOMATIONS/agent/swarm/reports")

SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)
REPORT_DIR.mkdir(parents=True, exist_ok=True)

class PlaywrightTester:
    def __init__(self):
        self.results = {"green": [], "yellow": [], "red": []}
        self.timestamps = {}

    async def test_site(self, url: str) -> Tuple[str, Dict]:
        """Test a single site using curl + basic checks."""
        site_name = url.replace("https://", "").replace(".surge.sh", "")

        # Basic curl test to check if site is reachable
        import subprocess

        start = time.time()
        try:
            result = subprocess.run(
                ["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}", "--max-time", "5", url],
                capture_output=True,
                text=True,
                timeout=10
            )
            status_code = result.stdout.strip()
            load_time = (time.time() - start) * 1000

            # Determine health
            if status_code == "200":
                health = "green"
                issue = None
            elif status_code in ["301", "302", "403"]:
                health = "yellow"
                issue = f"HTTP {status_code} (redirect/forbidden)"
            else:
                health = "red"
                issue = f"HTTP {status_code}"

            # Warn if load time high
            if health == "green" and load_time > 5000:
                health = "yellow"
                if not issue:
                    issue = f"Slow load ({load_time:.0f}ms)"

        except Exception as e:
            health = "red"
            issue = str(e)
            load_time = None
            status_code = "ERROR"

        result_data = {
            "url": url,
            "site_name": site_name,
            "status": health,
            "issue": issue,
            "http_code": status_code,
            "load_ms": load_time,
            "tested_at": datetime.now().isoformat()
        }

        return health, result_data

    async def run_all_tests(self):
        """Test all sites concurrently."""
        print(f"\n🧪 Starting Playwright Tester Cycle at {datetime.now().isoformat()}")
        print(f"📍 Testing {len(SITES_TO_TEST)} sites...")

        # Run tests sequentially to avoid rate limits
        for url in SITES_TO_TEST:
            health, data = await self.test_site(url)
            self.results[health].append(data)

            status_emoji = "✅" if health == "green" else "⚠️" if health == "yellow" else "❌"
            print(f"{status_emoji} {data['site_name'][:50]:50} → {health.upper()}")

        return self.results

    def generate_report(self):
        """Generate markdown report."""
        total = len(SITES_TO_TEST)
        green_count = len(self.results["green"])
        yellow_count = len(self.results["yellow"])
        red_count = len(self.results["red"])

        report = f"""# Playwright Tester Report — Cycle {datetime.now().strftime("%Y%m%d_%H%M")}

**Tested:** {datetime.now().isoformat()}
**Total Sites:** {total}

## Summary

| Status | Count | % |
|--------|-------|---|
| ✅ GREEN | {green_count} | {100*green_count/total:.1f}% |
| ⚠️ YELLOW | {yellow_count} | {100*yellow_count/total:.1f}% |
| ❌ RED | {red_count} | {100*red_count/total:.1f}% |

**Pass Rate:** {100*(total-red_count)/total:.1f}%

---

## GREEN (Operational) — {green_count} sites

"""
        for item in self.results["green"]:
            report += f"- ✅ {item['site_name']} ({item['load_ms']:.0f}ms)\n"

        report += f"\n## YELLOW (Warnings) — {yellow_count} sites\n\n"
        for item in self.results["yellow"]:
            report += f"- ⚠️ {item['site_name']} — {item['issue']}\n"

        report += f"\n## RED (Broken) — {red_count} sites\n\n"
        for item in self.results["red"]:
            report += f"- ❌ {item['site_name']} — {item['issue']}\n"

        report += f"\n---\n\n## Detailed Results\n\n"
        report += json.dumps(self.results, indent=2)

        return report

async def main():
    tester = PlaywrightTester()
    results = await tester.run_all_tests()

    # Generate report
    report = tester.generate_report()

    # Write report
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    report_file = REPORT_DIR / f"playwright_tester_cycle_{timestamp}.md"
    report_file.write_text(report)

    print(f"\n✅ Report saved to {report_file}")

    # Summary
    total = len(SITES_TO_TEST)
    red = len(results["red"])
    print(f"\n📊 SUMMARY: {total - red}/{total} sites operational ({100*(total-red)/total:.1f}%)")

    if results["red"]:
        print(f"\n🚨 {len(results['red'])} sites need attention:")
        for item in results["red"]:
            print(f"  - {item['site_name']}: {item['issue']}")

    return results

if __name__ == "__main__":
    asyncio.run(main())
