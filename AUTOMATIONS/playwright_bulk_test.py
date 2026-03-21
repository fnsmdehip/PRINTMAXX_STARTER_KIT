#!/usr/bin/env python3

from __future__ import annotations
"""Bulk HTTP health check for all PRINTMAXX surge.sh deployments."""

import concurrent.futures
import json
import time
import requests
from datetime import datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
REPORT_DIR = PROJECT_ROOT / "AUTOMATIONS" / "agent" / "swarm" / "reports"
ALERTS_FILE = PROJECT_ROOT / "AUTOMATIONS" / "agent" / "swarm" / "quality_alerts.txt"

SITES = [
    "printmaxx-store.surge.sh",
    "instantly-vs-lemlist.surge.sh",
    "cursor-vs-claudecode.surge.sh",
    "pagescorer-vs-gtmetrix.surge.sh",
    "coldmaxx-vs-instantly.surge.sh",
    "sleepmaxx-vs-sleepcycle.surge.sh",
    "printmaxx-twitter-pfp.surge.sh",
    "printmaxx-twitter-banner.surge.sh",
    "walktounlock-app.surge.sh",
    "sleepmaxx-app.surge.sh",
    "prayerlock-app.surge.sh",
    "focuslock-app.surge.sh",
    "stackmaxx-app.surge.sh",
    "roicalc-app.surge.sh",
    "prospectmaxx-app.surge.sh",
    "pitchdeck-app.surge.sh",
    "pagescorer-app.surge.sh",
    "invoiceforge-app.surge.sh",
    "coldmaxx-app.surge.sh",
    "subject-line-grader-pm.surge.sh",
    "sutra-streak-app.surge.sh",
    "art-streak-app.surge.sh",
    "printmaxx-local-demos.surge.sh",
    "walktounlock-web.surge.sh",
    "printmaxx-thanks.surge.sh",
    "sunni-streak.surge.sh",
    "sleepmaxx-web.surge.sh",
    "shia-streak.surge.sh",
    "protestant-streak.surge.sh",
    "presbyterian-streak.surge.sh",
    "prayerlock-web.surge.sh",
    "pentecostal-streak.surge.sh",
    "orthodox-streak.surge.sh",
    "methodist-streak.surge.sh",
    "mealmaxx-web.surge.sh",
    "lutheran-streak.surge.sh",
    "hilal-app.surge.sh",
    "focuslock-web.surge.sh",
    "evangelical-streak.surge.sh",
    "episcopal-streak.surge.sh",
    "convertkit-vs-beehiiv.surge.sh",
    "coldmaxx.surge.sh",
    "catholic-streak.surge.sh",
    "baptist-streak.surge.sh",
    "anglican-streak.surge.sh",
    "ai-stack-2026.surge.sh",
    "adhd-streak.surge.sh",
    "printmaxx-site.surge.sh",
    "printmaxx-apps.surge.sh",
    "printmaxx.surge.sh",
    "jss-janitorial-memphis.surge.sh",
    "shop-of-memphis-preview.surge.sh",
    "website-analyzer-pm.surge.sh",
    "printmaxx-control-panel.surge.sh",
    "fitness-streak-landing.surge.sh",
    "coding-streak-landing.surge.sh",
    "buddhist-streak-landing.surge.sh",
    "art-streak-landing.surge.sh",
    "solopreneur-launch-checklist.surge.sh",
    "ramadan-daily-planner.surge.sh",
    "printmaxx-comparisons.surge.sh",
    "prayerlock-vs-hallow.surge.sh",
    "focuslock-vs-opal.surge.sh",
    "hilal.surge.sh",
    "magnolia-cafe-austin.surge.sh",
    "kelly-personal-training-austin.surge.sh",
    "galaxia-dental-austin.surge.sh",
    "barton-springs-saloon-austin.surge.sh",
    "zax-pints-plates-austin.surge.sh",
    "artz-rib-house-austin.surge.sh",
    "memphis-plumbing-preview.surge.sh",
    "jax-emergency-plumber-preview.surge.sh",
    "south-tampa-locksmith-preview.surge.sh",
    "atlanta-roofing-company-preview.surge.sh",
    "mealmaxx-app.surge.sh",
    "printmaxx-magnets.surge.sh",
    "printmaxx-storefront.surge.sh",
    "quran-streak.surge.sh",
    "printmaxx-content-calendar.surge.sh",
    "printmaxx-website-audit.surge.sh",
    "printmaxx-invoice-tracker.surge.sh",
    "printmaxx-compare.surge.sh",
    "torah-streak.surge.sh",
    "sikh-streak.surge.sh",
    "reading-streak.surge.sh",
    "mormon-streak.surge.sh",
    "meditation-streak.surge.sh",
    "language-streak.surge.sh",
    "journal-streak.surge.sh",
    "gita-streak.surge.sh",
    "fitness-streak.surge.sh",
    "coding-streak.surge.sh",
    "buddhist-streak.surge.sh",
    "art-streak.surge.sh",
    "ramadan-tracker.surge.sh",
    "reliable-fence-nashville.surge.sh",
    "accurate-auto-nashville.surge.sh",
    "shopmetrics-pro.surge.sh",
    "printmaxx-digital-services.surge.sh",
    "printmaxx-flowstack.surge.sh",
    "sitescore-free.surge.sh",
    "sitescore-pro.surge.sh",
    "printmaxx-command.surge.sh",
    "miami-plumbing-zip.surge.sh",
    "elite-fitness-demo.surge.sh",
    "joes-plumbing-demo.surge.sh",
    "smith-dentistry-demo.surge.sh",
    "bellas-salon-demo.surge.sh",
    "mikes-hvac-demo.surge.sh",
    "perfect-lawn-demo.surge.sh",
    "tonys-restaurant-demo.surge.sh",
    "fiverr-services-pm.surge.sh",
    "local-plumbing-experts-plumbers-just-start-with-your-zip-miami-fl.surge.sh",
    "sikh-streak-app.surge.sh",
    "mormon-streak-app.surge.sh",
    "cold-email-calc.surge.sh",
    "handyman-matters-jacksonville-jacksonville-fl.surge.sh",
    "jacksonville-emergency-plumber-jacksonville-fl.surge.sh",
    "professional-plumbing-heating-cooling-memphis-tn.surge.sh",
    "south-tampa-locksmith-tampa-fl.surge.sh",
    "printmaxx-services.surge.sh",
    "torah-streak-app.surge.sh",
    "guru-streak-app.surge.sh",
    "quran-streak-app.surge.sh",
    "scripture-streak-lds.surge.sh",
    "gita-streak-app.surge.sh",
    "reading-streak-app.surge.sh",
    "meditation-streak-app.surge.sh",
    "language-streak-app.surge.sh",
    "journal-streak-app.surge.sh",
    "fitness-streak-app.surge.sh",
    "coding-streak-app.surge.sh",
    "local-plumbing-miami-fl.surge.sh",
    "plumbers-just-enter-your-zip-code-miami-fl.surge.sh",
    "best-dentist-office-austin-your-neighborhood-dentist-austin-tx.surge.sh",
    "find-plumbers-in-houston-texas-meetaplumber-com-houston-tx.surge.sh",
    "plumbers-just-enter-your-zip-code-houston-tx.surge.sh",
    "local-plumbing-experts-replace-plumbing-houston-tx.surge.sh",
    "social-dashboard-pm.surge.sh",
    "contentcalendar.surge.sh",
    "website-audit-tool.surge.sh",
    "invoicetracker.surge.sh",
    "prospectmaxx.surge.sh",
    "roicalc.surge.sh",
    "pagescorer.surge.sh",
    "stackmaxx.surge.sh",
    "invoiceforge.surge.sh",
    "pitchdeck.surge.sh",
    "mcphub.surge.sh",
    "focuslock.surge.sh",
    "prayerlock.surge.sh",
    "walktounlock.surge.sh",
    "sleepmaxx.surge.sh",
    "mealmaxx.surge.sh",
    "printmaxx-demos.surge.sh",
    "shopmetrics-dashboard.surge.sh",
    "flowstack-demo.surge.sh",
    "printmaxx-dashboard.surge.sh",
    "sitescore-analyzer.surge.sh",
    "sitescore-app.surge.sh",
    "printmaxx-seo.surge.sh",
    "habitforge-web.surge.sh",
    "printmaxx-portfolio.surge.sh",
    "printmaxx-analyzer.surge.sh",
    "habitforge-app.surge.sh",
    "restaurant-motion.surge.sh",
    "realtor-motion.surge.sh",
    "dental-motion.surge.sh",
    "restaurant-site-demo.surge.sh",
    "hilal-ramadan.surge.sh",
    "realtor-demo.surge.sh",
    "plumber-demo.surge.sh",
    "legal-demo.surge.sh",
    "fitness-demo.surge.sh",
    "dental-demo.surge.sh",
]

def test_site(domain):
    """Test a single site and return result dict."""
    url = f"https://{domain}"
    result = {
        "domain": domain,
        "url": url,
        "status_code": None,
        "load_time_ms": None,
        "content_length": None,
        "has_content": False,
        "title": "",
        "grade": "RED",
        "error": None,
    }

    try:
        start = time.time()
        resp = requests.get(url, timeout=15, headers={
            "User-Agent": "PRINTMAXX-HealthCheck/1.0"
        })
        elapsed_ms = int((time.time() - start) * 1000)

        result["status_code"] = resp.status_code
        result["load_time_ms"] = elapsed_ms
        result["content_length"] = len(resp.text)

        # Check for actual content (not just empty HTML shell)
        text = resp.text.lower()
        has_body = len(resp.text) > 500
        not_error_page = "project not found" not in text and "404" not in text[:200]
        result["has_content"] = has_body and not_error_page

        # Extract title
        import re
        title_match = re.search(r'<title[^>]*>(.*?)</title>', resp.text, re.IGNORECASE | re.DOTALL)
        if title_match:
            result["title"] = title_match.group(1).strip()[:80]

        # Grade
        if resp.status_code == 200 and result["has_content"]:
            if elapsed_ms > 3000:
                result["grade"] = "YELLOW"
            else:
                result["grade"] = "GREEN"
        elif resp.status_code == 200 and not result["has_content"]:
            result["grade"] = "YELLOW"
        else:
            result["grade"] = "RED"

    except requests.exceptions.Timeout:
        result["error"] = "TIMEOUT (>15s)"
        result["grade"] = "RED"
    except requests.exceptions.ConnectionError as e:
        result["error"] = f"CONNECTION_ERROR: {str(e)[:100]}"
        result["grade"] = "RED"
    except Exception as e:
        result["error"] = f"ERROR: {str(e)[:100]}"
        result["grade"] = "RED"

    return result


def main():
    print(f"Testing {len(SITES)} sites...")
    start_all = time.time()

    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        future_map = {executor.submit(test_site, s): s for s in SITES}
        for i, future in enumerate(concurrent.futures.as_completed(future_map)):
            r = future.result()
            results.append(r)
            icon = {"GREEN": "G", "YELLOW": "Y", "RED": "R"}[r["grade"]]
            print(f"  [{i+1}/{len(SITES)}] [{icon}] {r['domain']} - {r['status_code']} ({r.get('load_time_ms', '?')}ms)")

    total_time = int(time.time() - start_all)

    # Sort by grade (RED first, then YELLOW, then GREEN)
    grade_order = {"RED": 0, "YELLOW": 1, "GREEN": 2}
    results.sort(key=lambda x: (grade_order[x["grade"]], x["domain"]))

    # Stats
    green = [r for r in results if r["grade"] == "GREEN"]
    yellow = [r for r in results if r["grade"] == "YELLOW"]
    red = [r for r in results if r["grade"] == "RED"]

    avg_load = 0
    loaded = [r for r in results if r["load_time_ms"]]
    if loaded:
        avg_load = sum(r["load_time_ms"] for r in loaded) // len(loaded)

    # Generate report
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    date_slug = datetime.now().strftime("%Y%m%d")

    report = f"""# PRINTMAXX Site Health Report
**Generated:** {now}
**Total sites tested:** {len(SITES)}
**Test duration:** {total_time}s
**Average load time:** {avg_load}ms

## Summary
- GREEN (healthy): {len(green)}
- YELLOW (warnings): {len(yellow)}
- RED (broken): {len(red)}
- **Health score: {len(green)}/{len(SITES)} ({100*len(green)//len(SITES)}%)**

"""

    if red:
        report += "## RED - Broken Sites\n\n"
        report += "| Site | Status | Error | Load Time |\n"
        report += "|------|--------|-------|----------|\n"
        for r in red:
            err = r["error"] or f"HTTP {r['status_code']}"
            lt = f"{r['load_time_ms']}ms" if r['load_time_ms'] else "N/A"
            report += f"| {r['domain']} | {r['status_code']} | {err} | {lt} |\n"
        report += "\n"

    if yellow:
        report += "## YELLOW - Warnings\n\n"
        report += "| Site | Status | Issue | Load Time |\n"
        report += "|------|--------|-------|----------|\n"
        for r in yellow:
            issue = "Slow (>3s)" if r.get("load_time_ms", 0) and r["load_time_ms"] > 3000 else "Low content"
            lt = f"{r['load_time_ms']}ms" if r['load_time_ms'] else "N/A"
            report += f"| {r['domain']} | {r['status_code']} | {issue} | {lt} |\n"
        report += "\n"

    report += "## GREEN - Healthy Sites\n\n"
    report += "| Site | Status | Title | Load Time |\n"
    report += "|------|--------|-------|----------|\n"
    for r in green:
        lt = f"{r['load_time_ms']}ms" if r['load_time_ms'] else "N/A"
        title = r["title"][:50] if r["title"] else "(no title)"
        report += f"| {r['domain']} | {r['status_code']} | {title} | {lt} |\n"

    # Write report
    report_path = REPORT_DIR / f"test_report_{date_slug}.md"
    report_path.write_text(report)
    print(f"\nReport saved: {report_path}")

    # Write alerts for RED sites
    if red:
        alert_lines = [f"[{now}] ALERT: {len(red)} sites are RED (broken)\n"]
        for r in red:
            alert_lines.append(f"  - {r['domain']}: {r['error'] or f'HTTP {r['status_code']}'}\n")
        with open(ALERTS_FILE, "a") as f:
            f.writelines(alert_lines)
        print(f"Alerts written: {ALERTS_FILE}")

    # Write JSON results for programmatic use
    json_path = REPORT_DIR / f"test_results_{date_slug}.json"
    json_path.write_text(json.dumps(results, indent=2))
    print(f"JSON results: {json_path}")

    # Print summary
    print(f"\n{'='*60}")
    print(f"RESULTS: {len(green)} GREEN | {len(yellow)} YELLOW | {len(red)} RED")
    print(f"Health score: {len(green)}/{len(SITES)} ({100*len(green)//len(SITES)}%)")
    print(f"{'='*60}")

    return results


if __name__ == "__main__":
    main()
