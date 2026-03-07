#!/usr/bin/env python3
"""
PRINTMAXX Playwright Site Tester
Tests all deployed surge.sh sites for status, load time, content, and console errors.
Outputs: screenshots + test_report_{date}.md + quality_alerts.txt
"""

import json
import os
import sys
import time
from datetime import datetime
from pathlib import Path

PROJECT_ROOT = Path("/Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt")
SCREENSHOTS_DIR = PROJECT_ROOT / "AUTOMATIONS/agent/swarm/screenshots"
REPORTS_DIR = PROJECT_ROOT / "AUTOMATIONS/agent/swarm/reports"
DEPLOYED_ASSETS = PROJECT_ROOT / "AUTOMATIONS/agent/swarm/deployed_assets.json"

SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)
REPORTS_DIR.mkdir(parents=True, exist_ok=True)

TODAY = datetime.now().strftime("%Y%m%d")
REPORT_PATH = REPORTS_DIR / f"test_report_{TODAY}.md"
ALERTS_PATH = PROJECT_ROOT / "AUTOMATIONS/agent/swarm/quality_alerts.txt"

# All surge.sh deployments from the live surge list
ALL_SITES = [
    # Recently deployed (< 1 hour)
    ("FocusLock App (new)", "https://focuslock-app.surge.sh", "app"),
    ("ColdMailer App (new)", "https://coldmaxx-app.surge.sh", "app"),
    ("PrayerLock App (new)", "https://prayerlock-app.surge.sh", "app"),
    ("Handyman Matters Jacksonville", "https://handyman-matters-jacksonville-jacksonville-fl.surge.sh", "local_biz"),
    ("Jacksonville Emergency Plumber", "https://jacksonville-emergency-plumber-jacksonville-fl.surge.sh", "local_biz"),
    ("Professional Plumbing Memphis", "https://professional-plumbing-heating-cooling-memphis-tn.surge.sh", "local_biz"),
    ("South Tampa Locksmith", "https://south-tampa-locksmith-tampa-fl.surge.sh", "local_biz"),
    ("PrintMaxx Services", "https://printmaxx-services.surge.sh", "hub"),
    # Streak apps (2 hours ago)
    ("Torah Streak", "https://torah-streak-app.surge.sh", "streak"),
    ("Guru Streak", "https://guru-streak-app.surge.sh", "streak"),
    ("Quran Streak", "https://quran-streak-app.surge.sh", "streak"),
    ("Scripture Streak LDS", "https://scripture-streak-lds.surge.sh", "streak"),
    ("Gita Streak", "https://gita-streak-app.surge.sh", "streak"),
    ("Sutra Streak", "https://sutra-streak-app.surge.sh", "streak"),
    ("Reading Streak", "https://reading-streak-app.surge.sh", "streak"),
    ("Meditation Streak", "https://meditation-streak-app.surge.sh", "streak"),
    ("Language Streak", "https://language-streak-app.surge.sh", "streak"),
    ("Journal Streak", "https://journal-streak-app.surge.sh", "streak"),
    ("Fitness Streak", "https://fitness-streak-app.surge.sh", "streak"),
    ("Coding Streak", "https://coding-streak-app.surge.sh", "streak"),
    ("Art Streak", "https://art-streak-app.surge.sh", "streak"),
    # Local biz OpenClaw pages
    ("Local Plumbing Miami", "https://local-plumbing-miami-fl.surge.sh", "local_biz"),
    ("Local Plumbing Miami (zip)", "https://local-plumbing-experts-plumbers-just-start-with-your-zip-miami-fl.surge.sh", "local_biz"),
    ("Plumbers Miami (zip code)", "https://plumbers-just-enter-your-zip-code-miami-fl.surge.sh", "local_biz"),
    ("Best Dentist Austin", "https://best-dentist-office-austin-your-neighborhood-dentist-austin-tx.surge.sh", "local_biz"),
    ("Find Plumbers Houston", "https://find-plumbers-in-houston-texas-meetaplumber-com-houston-tx.surge.sh", "local_biz"),
    ("Plumbers Houston (zip)", "https://plumbers-just-enter-your-zip-code-houston-tx.surge.sh", "local_biz"),
    ("Local Plumbing Houston", "https://local-plumbing-experts-replace-plumbing-houston-tx.surge.sh", "local_biz"),
    # Core apps (2 days ago)
    ("PrintMaxx Apps Hub", "https://printmaxx-apps.surge.sh", "hub"),
    ("Social Dashboard", "https://social-dashboard-pm.surge.sh", "tool"),
    ("WalkToUnlock App", "https://walktounlock-app.surge.sh", "app"),
    ("SleepMaxx App", "https://sleepmaxx-app.surge.sh", "app"),
    ("Hilal App", "https://hilal-app.surge.sh", "app"),
    ("MealMaxx App", "https://mealmaxx-app.surge.sh", "app"),
    ("Content Calendar", "https://contentcalendar.surge.sh", "tool"),
    ("Website Audit Tool", "https://website-audit-tool.surge.sh", "tool"),
    ("Invoice Tracker", "https://invoicetracker.surge.sh", "tool"),
    ("ProspectMaxx", "https://prospectmaxx.surge.sh", "tool"),
    ("ROI Calc", "https://roicalc.surge.sh", "tool"),
    ("Page Scorer", "https://pagescorer.surge.sh", "tool"),
    ("StackMaxx", "https://stackmaxx.surge.sh", "tool"),
    ("Invoice Forge", "https://invoiceforge.surge.sh", "tool"),
    ("Pitch Deck", "https://pitchdeck.surge.sh", "tool"),
    ("MCP Hub", "https://mcphub.surge.sh", "hub"),
    ("ColdMaxx", "https://coldmaxx.surge.sh", "app"),
    ("FocusLock", "https://focuslock.surge.sh", "app"),
    ("Ramadan Tracker", "https://ramadan-tracker.surge.sh", "app"),
    ("PrayerLock", "https://prayerlock.surge.sh", "app"),
    ("WalkToUnlock", "https://walktounlock.surge.sh", "app"),
    ("SleepMaxx", "https://sleepmaxx.surge.sh", "app"),
    ("MealMaxx", "https://mealmaxx.surge.sh", "app"),
    ("PrayerLock Web", "https://prayerlock-web.surge.sh", "app"),
    # Older deployments (2 weeks - 3 weeks)
    ("PrintMaxx Demos", "https://printmaxx-demos.surge.sh", "hub"),
    ("ShopMetrics Dashboard", "https://shopmetrics-dashboard.surge.sh", "tool"),
    ("FlowStack Demo", "https://flowstack-demo.surge.sh", "demo"),
    ("PrintMaxx Dashboard", "https://printmaxx-dashboard.surge.sh", "hub"),
    ("SiteScore Analyzer", "https://sitescore-analyzer.surge.sh", "tool"),
    ("SiteScore App", "https://sitescore-app.surge.sh", "tool"),
    ("PrintMaxx SEO", "https://printmaxx-seo.surge.sh", "hub"),
    ("WalkToUnlock Web", "https://walktounlock-web.surge.sh", "app"),
    ("SleepMaxx Web", "https://sleepmaxx-web.surge.sh", "app"),
    ("MealMaxx Web", "https://mealmaxx-web.surge.sh", "app"),
    ("HabitForge Web", "https://habitforge-web.surge.sh", "app"),
    ("FocusLock Web", "https://focuslock-web.surge.sh", "app"),
    ("PrintMaxx Command", "https://printmaxx-command.surge.sh", "hub"),
    ("PrintMaxx Portfolio", "https://printmaxx-portfolio.surge.sh", "hub"),
    ("PrintMaxx Analyzer", "https://printmaxx-analyzer.surge.sh", "tool"),
    ("PrintMaxx Local Demos", "https://printmaxx-local-demos.surge.sh", "demo"),
    ("HabitForge App", "https://habitforge-app.surge.sh", "app"),
    ("Restaurant Motion", "https://restaurant-motion.surge.sh", "demo"),
    ("Realtor Motion", "https://realtor-motion.surge.sh", "demo"),
    ("Dental Motion", "https://dental-motion.surge.sh", "demo"),
    ("Restaurant Site Demo", "https://restaurant-site-demo.surge.sh", "demo"),
    ("Hilal Ramadan", "https://hilal-ramadan.surge.sh", "app"),
    ("Realtor Demo", "https://realtor-demo.surge.sh", "demo"),
    ("Plumber Demo", "https://plumber-demo.surge.sh", "demo"),
    ("Legal Demo", "https://legal-demo.surge.sh", "demo"),
    ("Fitness Demo", "https://fitness-demo.surge.sh", "demo"),
    ("Dental Demo", "https://dental-demo.surge.sh", "demo"),
]

def sanitize_filename(url):
    return url.replace("https://", "").replace("/", "_").replace(".", "_")[:60]

def test_site(page, name, url):
    result = {
        "name": name,
        "url": url,
        "status": None,
        "load_time_ms": None,
        "console_errors": [],
        "has_content": False,
        "title": "",
        "screenshot": None,
        "grade": "RED",
        "notes": [],
    }

    console_errors = []
    page.on("console", lambda msg: console_errors.append(msg.text) if msg.type == "error" else None)

    try:
        start = time.time()
        response = page.goto(url, timeout=15000, wait_until="domcontentloaded")
        load_time = int((time.time() - start) * 1000)

        result["load_time_ms"] = load_time
        result["status"] = response.status if response else 0

        # Wait for body content
        try:
            page.wait_for_selector("body", timeout=5000)
        except Exception:
            pass

        # Get title
        result["title"] = page.title() or ""

        # Check content
        body_text = page.inner_text("body") if page.query_selector("body") else ""
        result["has_content"] = len(body_text.strip()) > 50

        result["console_errors"] = console_errors[:5]  # cap at 5

        # Screenshot
        safe_name = sanitize_filename(url)
        screenshot_path = str(SCREENSHOTS_DIR / f"{safe_name}.png")
        page.screenshot(path=screenshot_path, full_page=False)
        result["screenshot"] = screenshot_path

        # Grading
        if result["status"] == 200 and result["has_content"]:
            if load_time > 5000:
                result["grade"] = "YELLOW"
                result["notes"].append(f"Slow load: {load_time}ms")
            elif console_errors:
                result["grade"] = "YELLOW"
                result["notes"].append(f"{len(console_errors)} console error(s)")
            else:
                result["grade"] = "GREEN"
        elif result["status"] == 200 and not result["has_content"]:
            result["grade"] = "YELLOW"
            result["notes"].append("200 OK but page appears blank/empty")
        else:
            result["grade"] = "RED"
            result["notes"].append(f"HTTP {result['status']}")

    except Exception as e:
        result["grade"] = "RED"
        result["notes"].append(f"Exception: {str(e)[:120]}")

    return result


def run_tests():
    from playwright.sync_api import sync_playwright

    results = []
    total = len(ALL_SITES)

    print(f"\n{'='*60}")
    print(f"PRINTMAXX PLAYWRIGHT TESTER — {TODAY}")
    print(f"Testing {total} sites...")
    print(f"{'='*60}\n")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            viewport={"width": 1280, "height": 800},
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
        )

        for i, (name, url, category) in enumerate(ALL_SITES, 1):
            page = context.new_page()
            print(f"[{i:02d}/{total}] Testing: {name} ({url})")
            r = test_site(page, name, url)
            r["category"] = category
            results.append(r)
            grade_icon = {"GREEN": "✓", "YELLOW": "⚠", "RED": "✗"}.get(r["grade"], "?")
            notes = " | ".join(r["notes"]) if r["notes"] else ""
            print(f"         {grade_icon} {r['grade']} | {r['status']} | {r['load_time_ms']}ms | {notes}")
            page.close()

        context.close()
        browser.close()

    return results


def write_report(results):
    green = [r for r in results if r["grade"] == "GREEN"]
    yellow = [r for r in results if r["grade"] == "YELLOW"]
    red = [r for r in results if r["grade"] == "RED"]

    avg_load = sum(r["load_time_ms"] for r in results if r["load_time_ms"]) / max(len(results), 1)

    lines = [
        f"# PRINTMAXX Site Test Report — {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "",
        "## Summary",
        "",
        f"| Metric | Value |",
        f"|--------|-------|",
        f"| Total Sites | {len(results)} |",
        f"| GREEN (passing) | {len(green)} |",
        f"| YELLOW (warnings) | {len(yellow)} |",
        f"| RED (broken) | {len(red)} |",
        f"| Pass Rate | {len(green)/len(results)*100:.1f}% |",
        f"| Avg Load Time | {avg_load:.0f}ms |",
        "",
    ]

    if red:
        lines += ["## 🔴 RED — Broken Sites (Fix Immediately)", ""]
        for r in red:
            lines.append(f"### {r['name']}")
            lines.append(f"- **URL:** {r['url']}")
            lines.append(f"- **Status:** {r['status']}")
            lines.append(f"- **Issues:** {' | '.join(r['notes'])}")
            lines.append("")

    if yellow:
        lines += ["## 🟡 YELLOW — Sites with Warnings", ""]
        for r in yellow:
            lines.append(f"### {r['name']}")
            lines.append(f"- **URL:** {r['url']}")
            lines.append(f"- **Status:** {r['status']} | Load: {r['load_time_ms']}ms")
            lines.append(f"- **Warnings:** {' | '.join(r['notes'])}")
            lines.append("")

    lines += ["## 🟢 GREEN — All Passing Sites", ""]
    lines.append("| Site | URL | Load Time | Title |")
    lines.append("|------|-----|-----------|-------|")
    for r in green:
        title = r["title"][:40] if r["title"] else "(no title)"
        lines.append(f"| {r['name']} | {r['url']} | {r['load_time_ms']}ms | {title} |")
    lines.append("")

    lines += [
        "## Full Results",
        "",
        "| # | Site | Category | Grade | Status | Load (ms) | Notes |",
        "|---|------|----------|-------|--------|-----------|-------|",
    ]
    for i, r in enumerate(results, 1):
        grade_badge = {"GREEN": "🟢", "YELLOW": "🟡", "RED": "🔴"}.get(r["grade"], "⚪")
        notes = "; ".join(r["notes"])[:60] if r["notes"] else ""
        lines.append(f"| {i} | {r['name']} | {r['category']} | {grade_badge} {r['grade']} | {r['status']} | {r['load_time_ms']} | {notes} |")

    lines += [
        "",
        f"*Generated by PRINTMAXX Playwright Tester — {datetime.now().isoformat()}*",
        f"*Screenshots saved to: AUTOMATIONS/agent/swarm/screenshots/*",
    ]

    report_text = "\n".join(lines)
    REPORT_PATH.write_text(report_text)
    print(f"\n✓ Report written: {REPORT_PATH}")
    return report_text


def write_alerts(results):
    red = [r for r in results if r["grade"] == "RED"]
    if not red:
        return

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    alert_lines = [f"\n[{timestamp}] QUALITY ALERT — {len(red)} RED site(s) detected:"]
    for r in red:
        alert_lines.append(f"  ✗ {r['name']} | {r['url']} | {' | '.join(r['notes'])}")

    with open(ALERTS_PATH, "a") as f:
        f.write("\n".join(alert_lines) + "\n")
    print(f"✓ Alerts written: {ALERTS_PATH}")


def main():
    results = run_tests()
    write_report(results)
    write_alerts(results)

    green = sum(1 for r in results if r["grade"] == "GREEN")
    yellow = sum(1 for r in results if r["grade"] == "YELLOW")
    red = sum(1 for r in results if r["grade"] == "RED")

    print(f"\n{'='*60}")
    print(f"DONE — {len(results)} sites tested")
    print(f"  GREEN:  {green}")
    print(f"  YELLOW: {yellow}")
    print(f"  RED:    {red}")
    print(f"{'='*60}")

    return 0 if red == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
