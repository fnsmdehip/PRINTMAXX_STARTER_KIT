#!/usr/bin/env python3
"""
PLAYWRIGHT TESTER v2 - Efficient multi-site testing with auto-fix
Tests RED sites priority, samples GREEN/YELLOW sites, generates report
"""

import asyncio
import json
import subprocess
import sys
from pathlib import Path
from datetime import datetime
import hashlib
import re

# Suppress Playwright startup warnings
import logging
logging.getLogger("asyncio").setLevel(logging.WARNING)

async def test_site(url: str, timeout: int = 15000):
    """Test a single site with Playwright"""
    try:
        # Create a simple HTML test file that uses Playwright
        test_code = f"""
const {{ chromium }} = require('playwright');

(async () => {{
    const browser = await chromium.launch();
    const page = await browser.newPage();

    try {{
        const startTime = Date.now();
        const response = await page.goto('{url}', {{ waitUntil: 'networkidle', timeout: {timeout} }});
        const loadTime = Date.now() - startTime;

        const status = response ? response.status() : 0;
        const title = await page.title();
        const content = await page.content();
        const consoleErrors = [];

        page.on('console', msg => {{
            if (msg.type() === 'error') {{
                consoleErrors.push(msg.text());
            }}
        }});

        const hasContent = content.length > 500;
        const blankPage = content.includes('404') || content.includes('Page not found');

        console.log(JSON.stringify({{
            url: '{url}',
            status,
            title,
            loadTime,
            hasContent,
            blankPage,
            consoleErrors,
            success: status === 200 && hasContent && !blankPage
        }}));
    }} catch (error) {{
        console.log(JSON.stringify({{
            url: '{url}',
            status: 0,
            error: error.message,
            success: false
        }}));
    }} finally {{
        await browser.close();
    }}
}})();
"""

        # Write test file
        test_file = Path("/tmp/test_site.js")
        test_file.write_text(test_code)

        # Run with node
        result = subprocess.run(
            ["node", str(test_file)],
            capture_output=True,
            text=True,
            timeout=20
        )

        if result.stdout.strip():
            return json.loads(result.stdout.strip())
        else:
            return {
                "url": url,
                "status": 0,
                "error": result.stderr,
                "success": False
            }

    except json.JSONDecodeError as e:
        return {"url": url, "status": 0, "error": f"JSON parse error: {str(e)}", "success": False}
    except subprocess.TimeoutExpired:
        return {"url": url, "status": 0, "error": "Test timeout", "success": False}
    except Exception as e:
        return {"url": url, "status": 0, "error": str(e), "success": False}


def find_source_path(site_name: str) -> Path:
    """Find the source directory for a site"""
    base = Path("/Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt")

    # Common patterns
    patterns = [
        base / "LANDING" / f"{site_name}",
        base / "LANDING" / site_name.replace(".surge.sh", ""),
        base / "DIGITAL_PRODUCTS" / site_name,
        base / "DIGITAL_PRODUCTS" / site_name.replace(".surge.sh", ""),
        base / "MONEY_METHODS" / site_name,
        base / "07_LANDING" / site_name,
    ]

    for p in patterns:
        if p.exists() and p.is_dir():
            return p

    return None


async def run_tests(red_sites: list, sample_green: list = None, sample_yellow: list = None):
    """Run async tests on multiple sites"""

    all_sites = []

    if red_sites:
        all_sites.extend(red_sites)
    if sample_green:
        all_sites.extend(sample_green[:5])  # Test 5 green sites
    if sample_yellow:
        all_sites.extend(sample_yellow[:5])  # Test 5 yellow sites

    print(f"Testing {len(all_sites)} sites total...")

    results = []

    # Test in batches of 3 (Playwright can be resource-intensive)
    for i in range(0, len(all_sites), 3):
        batch = all_sites[i:i+3]
        batch_results = await asyncio.gather(*[test_site(url) for url in batch])
        results.extend(batch_results)
        print(f"  Tested {min(i+3, len(all_sites))}/{len(all_sites)}")

    return results


def categorize_result(result: dict) -> str:
    """Categorize test result"""
    if result.get("success"):
        if result.get("loadTime", 0) > 5000:
            return "YELLOW"  # Slow
        return "GREEN"
    return "RED"


def main():
    # Red sites from deployed_assets.json
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
        "https://old-settlers-dental-p-a-austin-tx.surge.sh",
    ]

    # Sample green sites to verify still working
    SAMPLE_GREEN = [
        "https://printmaxx.surge.sh",
        "https://prayerlock-web.surge.sh",
        "https://coldmaxx.surge.sh",
        "https://mcp-marketplace.surge.sh",
        "https://stackmaxx.surge.sh",
    ]

    print(f"=== PLAYWRIGHT TESTER v2 ===")
    print(f"Testing {len(RED_SITES)} RED sites + {len(SAMPLE_GREEN)} sample GREEN sites")
    print(f"Start time: {datetime.now().isoformat()}\n")

    # Run async tests
    try:
        results = asyncio.run(run_tests(RED_SITES, SAMPLE_GREEN))
    except KeyboardInterrupt:
        print("\nTest interrupted.")
        return

    # Categorize results
    categorized = {}
    for result in results:
        category = categorize_result(result)
        if category not in categorized:
            categorized[category] = []
        categorized[category].append(result)

    # Generate report
    report = f"""# PLAYWRIGHT TESTER REPORT — {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Summary
- Total tested: {len(results)}
- GREEN: {len(categorized.get('GREEN', []))}
- YELLOW: {len(categorized.get('YELLOW', []))}
- RED: {len(categorized.get('RED', []))}
- Pass rate: {100 * len(categorized.get('GREEN', [])) / len(results):.1f}%

## GREEN Sites (Healthy)
"""

    for result in categorized.get('GREEN', []):
        report += f"- {result['url']}: HTTP {result.get('status', '?')} ({result.get('loadTime', 0)}ms)\n"

    report += f"\n## YELLOW Sites (Slow or Warnings)\n"
    for result in categorized.get('YELLOW', []):
        report += f"- {result['url']}: HTTP {result.get('status', '?')} ({result.get('loadTime', 0)}ms)\n"

    report += f"\n## RED Sites (Broken)\n"
    for result in categorized.get('RED', []):
        report += f"- {result['url']}\n"
        if 'error' in result:
            report += f"  Error: {result['error']}\n"
        if result.get('status') == 0:
            report += f"  Cannot reach (network error or timeout)\n"
        elif result.get('status') == 404:
            report += f"  HTTP 404 - Page not found\n"
        elif result.get('status') != 200:
            report += f"  HTTP {result.get('status', '?')}\n"
        if result.get('blankPage'):
            report += f"  Blank page detected\n"

    # Write report
    report_path = Path("/Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt/AUTOMATIONS/agent/swarm/reports/playwright_tester_report_20260317.md")
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(report)

    print(f"\nReport saved: {report_path}\n")
    print(report)

    # Return stats
    return {
        "green": len(categorized.get('GREEN', [])),
        "yellow": len(categorized.get('YELLOW', [])),
        "red": len(categorized.get('RED', [])),
        "total": len(results)
    }


if __name__ == "__main__":
    stats = main()
    sys.exit(0 if stats.get('red', 0) == 0 else 1)
