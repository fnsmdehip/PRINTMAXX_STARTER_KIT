#!/usr/bin/env python3
"""Playwright Batch Site Tester for PRINTMAXX deployed surge.sh sites."""

import json
import os
import sys
import time
import re
from datetime import datetime
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

PROJECT_ROOT = Path("/Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt")
SCREENSHOTS_DIR = PROJECT_ROOT / "AUTOMATIONS/agent/swarm/screenshots"
REPORTS_DIR = PROJECT_ROOT / "AUTOMATIONS/agent/swarm/reports"

def get_surge_urls():
    """Extract all surge.sh URLs from the deployed list."""
    urls = []
    # Read from deployed_assets.json if it exists
    assets_file = PROJECT_ROOT / "AUTOMATIONS/agent/swarm/deployed_assets.json"
    if assets_file.exists():
        try:
            with open(assets_file) as f:
                data = json.load(f)
                if isinstance(data, list):
                    for item in data:
                        url = item.get("url", "") if isinstance(item, dict) else str(item)
                        if "surge.sh" in url:
                            if not url.startswith("http"):
                                url = f"https://{url}"
                            urls.append(url)
        except Exception:
            pass

    # Also get from surge list command output (passed as stdin or file)
    surge_list_file = PROJECT_ROOT / "AUTOMATIONS/surge_site_list.txt"
    if surge_list_file.exists():
        with open(surge_list_file) as f:
            for line in f:
                line = line.strip()
                match = re.match(r'^\s*(\S+\.surge\.sh)\s', line)
                if match:
                    domain = match.group(1)
                    if not domain.startswith("http"):
                        domain = f"https://{domain}"
                    if domain not in urls:
                        urls.append(domain)

    return urls


def test_single_site(url, browser_context_factory):
    """Test a single site and return results."""
    result = {
        "url": url,
        "status": "UNKNOWN",
        "http_status": None,
        "load_time_ms": None,
        "has_content": False,
        "console_errors": [],
        "screenshot": None,
        "error": None,
        "category": "RED"
    }

    domain = url.replace("https://", "").replace("http://", "").replace("/", "")
    screenshot_name = domain.replace(".", "_").replace("-", "_") + ".png"
    screenshot_path = SCREENSHOTS_DIR / screenshot_name

    try:
        context = browser_context_factory()
        page = context.new_page()

        # Collect console errors
        console_errors = []
        page.on("console", lambda msg: console_errors.append(msg.text) if msg.type == "error" else None)

        # Navigate with timeout
        start = time.time()
        response = page.goto(url, timeout=15000, wait_until="domcontentloaded")
        load_time = int((time.time() - start) * 1000)

        result["load_time_ms"] = load_time
        result["http_status"] = response.status if response else None

        # Wait a bit for rendering
        page.wait_for_timeout(1500)

        # Check if page has content (not blank)
        body_text = page.evaluate("document.body ? document.body.innerText.trim().length : 0")
        result["has_content"] = body_text > 20

        # Check title
        title = page.title()

        # Take screenshot
        try:
            page.screenshot(path=str(screenshot_path), full_page=False)
            result["screenshot"] = screenshot_name
        except Exception:
            pass

        # Collect console errors
        result["console_errors"] = console_errors[:5]  # Max 5

        # Categorize
        if response and response.status == 200 and result["has_content"]:
            if load_time > 5000 or len(console_errors) > 3:
                result["category"] = "YELLOW"
                result["status"] = "SLOW/WARNINGS"
            else:
                result["category"] = "GREEN"
                result["status"] = "OK"
        elif response and response.status == 200 and not result["has_content"]:
            result["category"] = "RED"
            result["status"] = "BLANK_PAGE"
        elif response and response.status == 404:
            result["category"] = "RED"
            result["status"] = "NOT_FOUND"
        elif response:
            result["category"] = "RED"
            result["status"] = f"HTTP_{response.status}"
        else:
            result["category"] = "RED"
            result["status"] = "NO_RESPONSE"

        context.close()

    except Exception as e:
        err_str = str(e)[:200]
        result["error"] = err_str
        result["category"] = "RED"
        result["status"] = "ERROR"

    return result


def run_tests(urls, max_concurrent=5):
    """Run tests on all URLs using Playwright."""
    from playwright.sync_api import sync_playwright

    results = []
    total = len(urls)

    print(f"Testing {total} sites...")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)

        for i, url in enumerate(urls):
            print(f"  [{i+1}/{total}] {url}...", end=" ", flush=True)

            def make_context():
                return browser.new_context(
                    viewport={"width": 1280, "height": 720},
                    user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) PRINTMAXX-Tester/1.0"
                )

            result = test_single_site(url, make_context)
            results.append(result)

            icon = {"GREEN": "G", "YELLOW": "Y", "RED": "R"}.get(result["category"], "?")
            load = f"{result['load_time_ms']}ms" if result['load_time_ms'] else "N/A"
            print(f"[{icon}] {result['status']} ({load})")

            # Every 50 sites, save intermediate results
            if (i + 1) % 50 == 0:
                save_results(results, interim=True)

        browser.close()

    return results


def save_results(results, interim=False):
    """Save test results to JSON and markdown report."""
    today = datetime.now().strftime("%Y%m%d")
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")

    # Save JSON
    json_path = REPORTS_DIR / f"test_results_{today}.json"
    with open(json_path, "w") as f:
        json.dump(results, f, indent=2)

    if interim:
        return

    # Categorize
    green = [r for r in results if r["category"] == "GREEN"]
    yellow = [r for r in results if r["category"] == "YELLOW"]
    red = [r for r in results if r["category"] == "RED"]

    # Build markdown report
    report = f"""# Playwright Test Report — {timestamp}

## Summary

| Metric | Value |
|--------|-------|
| Total Sites Tested | {len(results)} |
| GREEN (healthy) | {len(green)} ({len(green)*100//max(len(results),1)}%) |
| YELLOW (warnings) | {len(yellow)} ({len(yellow)*100//max(len(results),1)}%) |
| RED (broken) | {len(red)} ({len(red)*100//max(len(results),1)}%) |
| Avg Load Time | {sum(r['load_time_ms'] for r in results if r['load_time_ms'])/max(sum(1 for r in results if r['load_time_ms']),1):.0f}ms |

---

"""

    if red:
        report += f"## RED — Broken Sites ({len(red)})\n\n"
        report += "| Site | Status | Error |\n|------|--------|-------|\n"
        for r in red:
            domain = r["url"].replace("https://", "")
            err = (r.get("error") or r.get("status", ""))[:80]
            report += f"| {domain} | {r['status']} | {err} |\n"
        report += "\n"

    if yellow:
        report += f"## YELLOW — Warnings ({len(yellow)})\n\n"
        report += "| Site | Load Time | Console Errors |\n|------|-----------|----------------|\n"
        for r in yellow:
            domain = r["url"].replace("https://", "")
            load = f"{r['load_time_ms']}ms" if r['load_time_ms'] else "N/A"
            errs = len(r.get("console_errors", []))
            report += f"| {domain} | {load} | {errs} |\n"
        report += "\n"

    report += f"## GREEN — Healthy ({len(green)})\n\n"
    report += "<details><summary>Click to expand</summary>\n\n"
    report += "| Site | Load Time |\n|------|-----------|\n"
    for r in sorted(green, key=lambda x: x.get("load_time_ms") or 99999):
        domain = r["url"].replace("https://", "")
        load = f"{r['load_time_ms']}ms" if r['load_time_ms'] else "N/A"
        report += f"| {domain} | {load} |\n"
    report += "\n</details>\n"

    # Write report
    report_path = REPORTS_DIR / f"test_report_{today}.md"
    with open(report_path, "w") as f:
        f.write(report)

    print(f"\nReport saved: {report_path}")
    print(f"JSON saved: {json_path}")

    # Write alerts for RED sites
    if red:
        alert_path = PROJECT_ROOT / "AUTOMATIONS/agent/swarm/quality_alerts.txt"
        with open(alert_path, "a") as f:
            f.write(f"\n--- ALERT {timestamp} ---\n")
            f.write(f"{len(red)} RED sites detected:\n")
            for r in red:
                f.write(f"  - {r['url']} [{r['status']}]\n")
        print(f"Alerts written: {alert_path}")

    return report_path


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Playwright batch site tester")
    parser.add_argument("--limit", type=int, default=0, help="Limit number of sites to test (0=all)")
    parser.add_argument("--category", type=str, default="all", help="Filter: apps, local, tools, streak, comparison, all")
    parser.add_argument("--retest-red", action="store_true", help="Only retest previously RED sites")
    args = parser.parse_args()

    urls = get_surge_urls()

    if not urls:
        print("No URLs found. Run `surge list` and save to AUTOMATIONS/surge_site_list.txt first.")
        sys.exit(1)

    # Filter by category
    if args.category != "all":
        filters = {
            "apps": ["-app.", "-web.", "streak.", "lock.", "maxx.", "forge.", "smash."],
            "local": ["-fl.", "-tx.", "-ky.", "-al.", "-tn.", "-nv.", "-or.", "-wi.", "mke.", "okc.", "austin.", "miami.", "houston.", "dallas.", "memphis.", "nashville.", "louisville.", "portland.", "jacksonville.", "birmingham.", "orlando.", "las-vegas."],
            "tools": ["calc.", "audit.", "grader.", "checker.", "scorer.", "dashboard.", "tracker."],
            "streak": ["streak"],
            "comparison": ["-vs-"],
            "printmaxx": ["printmaxx"],
        }
        keywords = filters.get(args.category, [])
        if keywords:
            urls = [u for u in urls if any(k in u for k in keywords)]

    if args.limit > 0:
        urls = urls[:args.limit]

    print(f"Found {len(urls)} URLs to test")

    results = run_tests(urls)
    save_results(results)

    # Print summary
    green = sum(1 for r in results if r["category"] == "GREEN")
    yellow = sum(1 for r in results if r["category"] == "YELLOW")
    red = sum(1 for r in results if r["category"] == "RED")
    print(f"\nFINAL: {green} GREEN | {yellow} YELLOW | {red} RED out of {len(results)} sites")


if __name__ == "__main__":
    main()
