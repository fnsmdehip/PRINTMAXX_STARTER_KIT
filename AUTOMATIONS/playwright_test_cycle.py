#!/usr/bin/env python3
"""
PLAYWRIGHT TESTER CYCLE
Tests deployed sites for HTTP status, console errors, content rendering, load time, links
"""

import asyncio
import json
import time
from pathlib import Path
from datetime import datetime
import sys

try:
    from playwright.async_api import async_playwright
except ImportError:
    print("Installing playwright...")
    import subprocess
    subprocess.run(["pip3", "install", "playwright"], check=True)
    from playwright.async_api import async_playwright

# Test sites - prioritized by criticality
CRITICAL_SITES = [
    # Core apps
    "https://cnsnt-web.surge.sh",
    "https://cnsnt.surge.sh",
    "https://prayerlock-web.surge.sh",
    "https://prayerlock-app.surge.sh",
    "https://prayerlock.surge.sh",
    "https://prayerlock-landing.surge.sh",
    "https://walktounlock-web.surge.sh",
    "https://walktounlock-app.surge.sh",
    "https://walktounlock-landing.surge.sh",
    "https://sleepmaxx-web.surge.sh",
    "https://sleepmaxx-app.surge.sh",
    "https://sleepmaxx-landing.surge.sh",
    "https://mealmaxx-web.surge.sh",
    "https://mealmaxx-app.surge.sh",
    "https://mealmaxx-landing.surge.sh",
    "https://focuslock-web.surge.sh",
    "https://focuslock-landing.surge.sh",
    "https://focuslock.surge.sh",
    "https://tasksmash-web.surge.sh",
    "https://ramadan-tracker.surge.sh",
    "https://hilal-app.surge.sh",
    "https://hilal-landing.surge.sh",
    "https://hilal.surge.sh",
    "https://coreday.surge.sh",

    # Comparison pages
    "https://n8n-vs-zapier-vs-make.surge.sh",
    "https://prayerlock-vs-hallow.surge.sh",
    "https://focuslock-vs-opal.surge.sh",
    "https://sleepmaxx-vs-sleepcycle.surge.sh",
    "https://pagescorer-vs-gtmetrix.surge.sh",
    "https://instantly-vs-lemlist.surge.sh",
    "https://coldmaxx-vs-instantly.surge.sh",
    "https://cursor-vs-claudecode.surge.sh",

    # Affiliate pages
    "https://smartlead-vs-instantly.surge.sh",
    "https://best-ai-tools-2026.surge.sh",
    "https://ai-stack-2026.surge.sh",
    "https://convertkit-vs-beehiiv.surge.sh",
    "https://semrush-vs-ahrefs.surge.sh",

    # Lead magnets
    "https://cold-email-roi-calculator.surge.sh",
    "https://saas-stack-audit.surge.sh",
    "https://subject-line-grader.surge.sh",
    "https://ramadan-daily-planner.surge.sh",
    "https://revenue-leak-audit.surge.sh",
    "https://solopreneur-launch-checklist.surge.sh",
    "https://side-project-revenue-estimator.surge.sh",
    "https://vibe-coding-profit-calculator.surge.sh",

    # Brand pages
    "https://printmaxx.surge.sh",
    "https://printmaxx-site.surge.sh",
    "https://printmaxx-apps.surge.sh",
    "https://printmaxx-comparisons.surge.sh",

    # Streak apps
    "https://scripture-streak.surge.sh",
    "https://scripture-streak-landing.surge.sh",
    "https://sunni-streak.surge.sh",
    "https://shia-streak.surge.sh",
    "https://quran-streak.surge.sh",
    "https://torah-streak.surge.sh",
    "https://gita-streak.surge.sh",
    "https://buddhist-streak.surge.sh",
    "https://meditation-streak.surge.sh",
    "https://reading-streak.surge.sh",
    "https://fitness-streak.surge.sh",

    # Tool apps
    "https://coldmaxx.surge.sh",
    "https://pagescorer.surge.sh",
    "https://stackmaxx.surge.sh",
    "https://invoiceforge.surge.sh",

    # Landing pages & research
    "https://builders-ledger.surge.sh",
    "https://fnsmdehip-research.surge.sh",
    "https://mcp-marketplace.surge.sh",

    # Sample local biz (newly deployed)
    "https://spodak-dental-group-miami-fl.surge.sh",
    "https://milestone-electric-a-c-plumbing-dallas-tx.surge.sh",
    "https://best-joint-supplement-men-over-50.surge.sh",
    "https://best-prostate-supplement-men-over-60.surge.sh",
    "https://best-testosterone-booster-men-over-50.surge.sh",
]

async def test_site(browser, url, timeout=15000):
    """Test a single site and return result."""
    start_time = time.time()
    result = {
        "url": url,
        "status": "RED",
        "http_code": 0,
        "load_time": 0,
        "has_errors": False,
        "error_count": 0,
        "warning_count": 0,
        "content_rendered": False,
        "is_blank": False,
        "errors": [],
        "warnings": [],
    }

    try:
        page = await browser.new_page()
        page.set_default_timeout(timeout)

        # Collect console messages
        errors = []
        warnings = []

        def handle_console(msg):
            if msg.type in ["error", "assert"]:
                errors.append(msg.text[:150])
            elif msg.type in ["warning"]:
                warnings.append(msg.text[:150])

        page.on("console", handle_console)

        # Navigate
        response = await page.goto(url, wait_until="networkidle")
        if response:
            result["http_code"] = response.status
            result["status"] = "GREEN" if response.status == 200 else "RED"

        # Check if page has content
        content = await page.content()
        result["is_blank"] = len(content) < 500

        # Check for rendered content (body text, not just HTML structure)
        visible_text = await page.evaluate("() => document.body.innerText.length")
        result["content_rendered"] = visible_text > 100

        result["load_time"] = round(time.time() - start_time, 2)
        result["error_count"] = len(errors)
        result["warning_count"] = len(warnings)
        result["errors"] = errors[:3]
        result["warnings"] = warnings[:3]
        result["has_errors"] = len(errors) > 0

        # Classify
        if result["http_code"] != 200:
            result["status"] = "RED"
        elif result["is_blank"] or not result["content_rendered"]:
            result["status"] = "RED"
        elif result["has_errors"]:
            result["status"] = "YELLOW"
        elif result["load_time"] > 5:
            result["status"] = "YELLOW"
        else:
            result["status"] = "GREEN"

        # Take screenshot
        screenshot_path = f"AUTOMATIONS/agent/swarm/screenshots/{url.split('://')[-1].replace('.surge.sh', '')}.png"
        Path(screenshot_path).parent.mkdir(parents=True, exist_ok=True)
        try:
            await page.screenshot(path=screenshot_path, full_page=False)
        except:
            pass

        await page.close()

    except asyncio.TimeoutError:
        result["status"] = "RED"
        result["errors"] = ["Page timeout (>15s)"]
    except Exception as e:
        result["status"] = "RED"
        result["errors"] = [str(e)[:150]]

    return result

async def run_tests():
    """Run all site tests."""
    results = {
        "timestamp": datetime.now().isoformat(),
        "cycle": "playwright_tester_20260328",
        "total": len(CRITICAL_SITES),
        "green": 0,
        "yellow": 0,
        "red": 0,
        "sites": [],
    }

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)

        for i, url in enumerate(CRITICAL_SITES, 1):
            print(f"[{i}/{len(CRITICAL_SITES)}] Testing {url}...", flush=True)
            result = await test_site(browser, url)
            results["sites"].append(result)

            if result["status"] == "GREEN":
                results["green"] += 1
                print(f"  ✓ GREEN ({result['load_time']}s)")
            elif result["status"] == "YELLOW":
                results["yellow"] += 1
                print(f"  ⚠ YELLOW ({result['load_time']}s) - {result['errors']}")
            else:
                results["red"] += 1
                print(f"  ✗ RED - {result['errors']}")

        await browser.close()

    results["pass_rate"] = f"{(results['green'] / results['total'] * 100):.1f}%"
    return results

# Run
if __name__ == "__main__":
    try:
        results = asyncio.run(run_tests())

        # Save results
        report_path = Path("AUTOMATIONS/agent/swarm/reports/playwright_tester_report_20260328.md")
        report_path.parent.mkdir(parents=True, exist_ok=True)

        # Write JSON for analysis
        with open("AUTOMATIONS/agent/swarm/test_results_20260328.json", "w") as f:
            json.dump(results, f, indent=2)

        # Write markdown report
        green_sites = [s for s in results["sites"] if s["status"] == "GREEN"]
        yellow_sites = [s for s in results["sites"] if s["status"] == "YELLOW"]
        red_sites = [s for s in results["sites"] if s["status"] == "RED"]

        report = f"""# PLAYWRIGHT TESTER REPORT — {results['timestamp']}

**Cycle:** {results['cycle']}
**Total Sites Tested:** {results['total']}
**Pass Rate:** {results['pass_rate']}

| Status | Count |
|--------|-------|
| ✓ GREEN | {results['green']} |
| ⚠ YELLOW | {results['yellow']} |
| ✗ RED | {results['red']} |

## RED Sites (Critical Issues)
"""
        for site in red_sites:
            report += f"\n### {site['url']}\n"
            report += f"- HTTP Code: {site['http_code']}\n"
            report += f"- Load Time: {site['load_time']}s\n"
            if site['errors']:
                report += f"- Errors: {', '.join(site['errors'])}\n"
            report += f"- Content Rendered: {site['content_rendered']}\n"

        if yellow_sites:
            report += f"\n## YELLOW Sites (Performance/Warnings)\n"
            for site in yellow_sites[:10]:
                report += f"\n### {site['url']}\n"
                report += f"- Load Time: {site['load_time']}s\n"
                if site['errors']:
                    report += f"- Errors: {', '.join(site['errors'])}\n"
                if site['warnings']:
                    report += f"- Warnings: {', '.join(site['warnings'])}\n"

        report += f"\n## GREEN Sites ({len(green_sites)})\n"
        report += "All sites below loaded successfully with no critical errors.\n"
        for site in sorted(green_sites, key=lambda s: s["load_time"]):
            report += f"- {site['url']} ({site['load_time']}s)\n"

        with open(report_path, "w") as f:
            f.write(report)

        print(f"\n✓ Test complete. Report: {report_path}")
        print(f"Green: {results['green']}, Yellow: {results['yellow']}, Red: {results['red']}")

    except Exception as e:
        print(f"✗ Test failed: {e}")
        sys.exit(1)
