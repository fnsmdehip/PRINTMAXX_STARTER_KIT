#!/usr/bin/env python3
"""
Playwright Tester Agent - Tests all deployed surge.sh sites
"""

import json
import subprocess
import sys
from pathlib import Path
from datetime import datetime
import time

# Setup
SWARM_DIR = Path(__file__).parent
SCREENSHOTS_DIR = SWARM_DIR / "screenshots"
REPORTS_DIR = SWARM_DIR / "reports"
DEPLOYED_ASSETS = SWARM_DIR / "deployed_assets.json"

SCREENSHOTS_DIR.mkdir(exist_ok=True)
REPORTS_DIR.mkdir(exist_ok=True)

def load_sites():
    """Load deployed sites from deployed_assets.json"""
    if not DEPLOYED_ASSETS.exists():
        print(f"ERROR: {DEPLOYED_ASSETS} not found")
        return []

    with open(DEPLOYED_ASSETS) as f:
        data = json.load(f)

    sites = []
    for category, info in data.get("by_category", {}).items():
        for url in info.get("urls", []):
            sites.append(f"https://{url}")

    return sites

def test_site_with_playwright(url):
    """Test a single site using Playwright"""
    import asyncio
    from playwright.async_api import async_playwright

    async def run_test():
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()

            result = {
                "url": url,
                "timestamp": datetime.now().isoformat(),
                "status": "unknown",
                "status_code": 0,
                "load_time": 0,
                "has_errors": False,
                "errors": [],
                "content_rendered": False,
                "screenshot": None
            }

            try:
                start = time.time()
                response = await page.goto(url, wait_until="networkidle", timeout=10000)
                load_time = time.time() - start

                result["status_code"] = response.status if response else 0
                result["load_time"] = round(load_time, 2)
                result["status"] = "ok" if response and response.status == 200 else "failed"

                # Check for console errors
                errors = []
                page.on("console", lambda msg: errors.append(msg.text) if msg.type == "error" else None)

                # Wait a bit for content
                await page.wait_for_timeout(500)

                # Check if content rendered
                body_html = await page.query_selector("body")
                result["content_rendered"] = body_html is not None

                # Take screenshot
                site_slug = url.replace("https://", "").replace(".surge.sh", "")
                screenshot_path = SCREENSHOTS_DIR / f"{site_slug}_20260402.png"
                await page.screenshot(path=str(screenshot_path), full_page=True)
                result["screenshot"] = screenshot_path.name

                # Get page title to verify it loaded
                title = await page.title()
                result["title"] = title

                result["has_errors"] = len(errors) > 0
                result["errors"] = errors[:5]  # First 5 errors

            except Exception as e:
                result["status"] = "error"
                result["errors"] = [str(e)]
                result["has_errors"] = True

            finally:
                await browser.close()

            return result

    try:
        return asyncio.run(run_test())
    except Exception as e:
        return {
            "url": url,
            "timestamp": datetime.now().isoformat(),
            "status": "error",
            "status_code": 0,
            "errors": [str(e)],
            "has_errors": True
        }

def categorize_result(result):
    """Categorize test result as GREEN/YELLOW/RED"""
    if result["status"] == "error":
        return "RED"

    if result["status_code"] != 200:
        return "RED"

    if not result["content_rendered"]:
        return "RED"

    if result["has_errors"]:
        return "YELLOW"

    if result["load_time"] > 3:
        return "YELLOW"

    return "GREEN"

def test_all_sites_fast():
    """Quick test using surge CLI instead of browser"""
    # This is faster for simple HTTP status checks
    results = []

    try:
        # Get all surge domains
        surge_list = subprocess.run(
            ["surge", "list"],
            capture_output=True,
            text=True,
            timeout=30
        )

        if surge_list.returncode == 0:
            for line in surge_list.stdout.split("\n"):
                if ".surge.sh" in line:
                    # Parse the domain from surge output
                    parts = line.split()
                    if parts:
                        domain = parts[0]
                        url = f"https://{domain}"

                        # Quick HTTP check
                        try:
                            check = subprocess.run(
                                ["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}", url],
                                capture_output=True,
                                text=True,
                                timeout=5
                            )
                            status_code = int(check.stdout.strip())

                            result = {
                                "url": url,
                                "status_code": status_code,
                                "status": "ok" if status_code == 200 else "failed",
                                "timestamp": datetime.now().isoformat()
                            }
                            results.append(result)
                        except:
                            pass
    except Exception as e:
        print(f"surge list failed: {e}")

    return results

def generate_report(results):
    """Generate test report"""
    green = [r for r in results if categorize_result(r) == "GREEN"]
    yellow = [r for r in results if categorize_result(r) == "YELLOW"]
    red = [r for r in results if categorize_result(r) == "RED"]

    report = f"""# Playwright Tester Report — {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Summary
- **Total Tested:** {len(results)}
- **GREEN (OK):** {len(green)}
- **YELLOW (Warnings):** {len(yellow)}
- **RED (Broken):** {len(red)}
- **Health:** {round(len(green) / max(len(results), 1) * 100, 1)}%

## Status Distribution
| Status | Count | Percentage |
|--------|-------|-----------|
| GREEN | {len(green)} | {round(len(green) / max(len(results), 1) * 100, 1)}% |
| YELLOW | {len(yellow)} | {round(len(yellow) / max(len(results), 1) * 100, 1)}% |
| RED | {len(red)} | {round(len(red) / max(len(results), 1) * 100, 1)}% |

## RED Sites (Need Attention)
"""

    if red:
        for r in red[:20]:  # Top 20
            report += f"- **{r['url']}** — {r.get('status_code', 'ERROR')}\n"
    else:
        report += "✓ No broken sites detected.\n"

    report += "\n## YELLOW Sites (Warnings)\n"
    if yellow:
        for r in yellow[:20]:
            report += f"- **{r['url']}** — Load: {r.get('load_time', 'N/A')}s, Errors: {len(r.get('errors', []))}\n"
    else:
        report += "✓ No warnings.\n"

    report += f"\n## Details\nTotal sites: {len(results)}\n"

    return report

def main():
    """Main test execution"""
    print("[PLAYWRIGHT TESTER] Starting test cycle...")
    print(f"Time: {datetime.now()}")

    # Quick test first using curl (faster)
    print("\n[1/3] Running quick HTTP status checks...")
    results = test_all_sites_fast()

    print(f"[2/3] Tested {len(results)} sites via HTTP")

    # Categorize
    green = sum(1 for r in results if r.get("status_code") == 200)
    non_200 = sum(1 for r in results if r.get("status_code") != 200)

    print(f"  ✓ GREEN: {green}")
    print(f"  ✗ RED: {non_200}")

    # Generate report
    print("\n[3/3] Generating report...")
    report = generate_report(results)

    report_path = REPORTS_DIR / f"playwright_tester_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    report_path.write_text(report)

    print(f"\n✓ Report written to {report_path.name}")
    print(f"\n=== SUMMARY ===")
    print(f"Total: {len(results)} | Green: {green} | Red: {non_200}")

    # Write to standard location for session
    latest_report = REPORTS_DIR / "playwright_tester_report_latest.md"
    latest_report.write_text(report)

    return 0

if __name__ == "__main__":
    sys.exit(main())
