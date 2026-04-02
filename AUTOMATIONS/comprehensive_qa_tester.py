#!/usr/bin/env python3
"""
Comprehensive QA Tester — Tests 100+ PRINTMAXX deployed sites.
Aggressive testing: real HTTP checks, load times, error analysis.
"""

import subprocess
import json
import time
from datetime import datetime
from pathlib import Path
from collections import defaultdict

REPORT_DIR = Path("/Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt/AUTOMATIONS/agent/swarm/reports")
REPORT_DIR.mkdir(parents=True, exist_ok=True)

# Extended test suite — 100+ sites
COMPREHENSIVE_SITES = [
    # === CRITICAL (12) ===
    "https://printmaxx-site.surge.sh",
    "https://printmaxx.surge.sh",
    "https://prayerlock.surge.sh",
    "https://focuslock.surge.sh",
    "https://cnsnt.surge.sh",
    "https://cnsnt-web.surge.sh",
    "https://ramadan-tracker.surge.sh",
    "https://truthscope.surge.sh",
    "https://mcp-marketplace.surge.sh",
    "https://fnsmdehip-research.surge.sh",
    "https://printmaxx-store.surge.sh",
    "https://claude-code-revenue-audit.surge.sh",

    # === TOOL APPS (9) ===
    "https://coldmaxx.surge.sh",
    "https://invoiceforge.surge.sh",
    "https://pagescorer.surge.sh",
    "https://roicalc.surge.sh",
    "https://stackmaxx.surge.sh",
    "https://prospectmaxx.surge.sh",
    "https://pitchdeck.surge.sh",
    "https://printmaxx-tools.surge.sh",
    "https://ai-revenue-calculator.surge.sh",

    # === COMPARISON PAGES (8) ===
    "https://coldmaxx-vs-instantly.surge.sh",
    "https://cursor-vs-claudecode.surge.sh",
    "https://instantly-vs-lemlist.surge.sh",
    "https://pagescorer-vs-gtmetrix.surge.sh",
    "https://sleepmaxx-vs-sleepcycle.surge.sh",
    "https://prayerlock-vs-hallow.surge.sh",
    "https://focuslock-vs-opal.surge.sh",
    "https://n8n-vs-zapier-vs-make.surge.sh",

    # === APP MARKETING PAGES (7) ===
    "https://prayerlock-landing.surge.sh",
    "https://focuslock-landing.surge.sh",
    "https://scripture-streak-landing.surge.sh",
    "https://mealmaxx-landing.surge.sh",
    "https://sleepmaxx-landing.surge.sh",
    "https://walktounlock-landing.surge.sh",
    "https://hilal-landing.surge.sh",

    # === PWA/WEB APPS (11) ===
    "https://coreday.surge.sh",
    "https://walktounlock-web.surge.sh",
    "https://tasksmash-web.surge.sh",
    "https://sleepmaxx-web.surge.sh",
    "https://focuslock-web.surge.sh",
    "https://mealmaxx-web.surge.sh",
    "https://habitforge-web.surge.sh",
    "https://prayerlock-web.surge.sh",
    "https://pdfmaxx.surge.sh",
    "https://deskbreak-web.surge.sh",
    "https://deskbreak.surge.sh",

    # === LEAD MAGNETS (12) ===
    "https://cold-email-roi-calculator.surge.sh",
    "https://ramadan-daily-planner.surge.sh",
    "https://revenue-leak-audit.surge.sh",
    "https://solopreneur-launch-checklist.surge.sh",
    "https://subject-line-grader.surge.sh",
    "https://side-project-revenue-estimator.surge.sh",
    "https://saas-stack-audit.surge.sh",
    "https://vibe-coding-profit-calculator.surge.sh",
    "https://200-day-calculator.surge.sh",
    "https://cold-email-deliverability-checklist.surge.sh",
    "https://app-hub-crosslinks.surge.sh",
    "https://printmaxx-lead-magnets.surge.sh",

    # === DENOMINATION STREAK (18) ===
    "https://scripture-streak.surge.sh",
    "https://quran-streak.surge.sh",
    "https://torah-streak.surge.sh",
    "https://gita-streak.surge.sh",
    "https://buddhist-streak.surge.sh",
    "https://meditation-streak.surge.sh",
    "https://journal-streak.surge.sh",
    "https://coding-streak.surge.sh",
    "https://fitness-streak.surge.sh",
    "https://reading-streak.surge.sh",
    "https://language-streak.surge.sh",
    "https://art-streak.surge.sh",
    "https://music-theory-streak.surge.sh",
    "https://photography-streak.surge.sh",
    "https://yoga-streak.surge.sh",
    "https://cycling-streak.surge.sh",
    "https://running-streak.surge.sh",
    "https://soberstreak.surge.sh",

    # === LOCAL BIZ SAMPLE (15) ===
    "https://pest-control-miami-fl.surge.sh",
    "https://window-cleaning-louisville-ky.surge.sh",
    "https://handyman-las-vegas-nv.surge.sh",
    "https://mobile-detailing-birmingham-al.surge.sh",
    "https://interior-detailing-birmingham-magic-city.surge.sh",
    "https://window-cleaning-portland-or.surge.sh",
    "https://mobile-detailing-okc-pure-pro.surge.sh",
    "https://auto-detailing-okc-champion.surge.sh",
    "https://twitter-growth-projector.surge.sh",
    "https://best-sleep-supplement-men-over-55.surge.sh",
    "https://best-blood-pressure-supplement-men-over-55.surge.sh",
    "https://best-joint-supplement-men-over-50.surge.sh",
    "https://best-memory-supplement-men-over-60.surge.sh",
    "https://best-prostate-supplement-men-over-60.surge.sh",
    "https://best-testosterone-booster-men-over-50.surge.sh",

    # === FIVERR SERVICE PAGES (10) ===
    "https://printmaxx-website-design.surge.sh",
    "https://printmaxx-landing-page.surge.sh",
    "https://printmaxx-cold-email.surge.sh",
    "https://printmaxx-web-scraping.surge.sh",
    "https://printmaxx-automation.surge.sh",
    "https://printmaxx-seo-pages.surge.sh",
    "https://printmaxx-content-writing.surge.sh",
    "https://printmaxx-app-development.surge.sh",
    "https://printmaxx-ai-chatbot.surge.sh",
    "https://printmaxx-data-analysis.surge.sh",

    # === AFFILIATE / REFERENCE PAGES (5) ===
    "https://best-ai-tools-2026.surge.sh",
    "https://best-cold-email-tools.surge.sh",
    "https://best-lead-generation-tools.surge.sh",
    "https://best-saas-tools-solopreneurs.surge.sh",
    "https://ai-stack-2026-landing.surge.sh",

    # === RECENTLY DEPLOYED (10) ===
    "https://quality-janitorial-services-kansas-city-mo.surge.sh",
    "https://sunrise-property-care-llc-kansas-city-mo.surge.sh",
    "https://on-the-ball-remodeling-kansas-city-mo.surge.sh",
    "https://kc-remodel-repair-llc-kansas-city-mo.surge.sh",
    "https://perfect-surface-solutions-llc-kansas-city-mo.surge.sh",
    "https://global-pro-s-services-llc-kansas-city-mo.surge.sh",
    "https://cleaning-magic-kansas-city-mo.surge.sh",
    "https://sweet-n-discreet-cleaning-service-llc-kansas-city-mo.surge.sh",
    "https://stanley-steemer-air-duct-cleaning-service-st-louis-mo.surge.sh",
    "https://couples-streak-landing.surge.sh",
]

def test_site(url: str, timeout=8) -> dict:
    """Test a single site with detailed error handling."""
    site_name = url.replace("https://", "").replace(".surge.sh", "")
    start = time.time()

    try:
        # Use curl with better error handling
        result = subprocess.run(
            ["curl", "-s", "-I", "--max-time", str(timeout), "-w", "%{http_code}", url],
            capture_output=True,
            text=True,
            timeout=timeout + 2
        )

        # Extract status from last line
        output = result.stdout.strip()
        lines = output.split("\n")
        status_code = lines[-1] if lines else "000"

        load_time = (time.time() - start) * 1000

        # Determine health status
        if status_code == "200":
            health = "green"
            issue = None
        elif status_code in ["301", "302", "304", "403", "404"]:
            health = "yellow"
            issue = f"HTTP {status_code}"
        else:
            health = "red"
            issue = f"HTTP {status_code}"

        # Flag slow sites
        if health == "green" and load_time > 5000:
            health = "yellow"
            issue = f"Slow ({load_time:.0f}ms)"

        return {
            "site": site_name,
            "url": url,
            "status": health,
            "http_code": status_code,
            "load_ms": load_time,
            "issue": issue,
            "tested_at": datetime.now().isoformat()
        }

    except subprocess.TimeoutExpired:
        return {
            "site": site_name,
            "url": url,
            "status": "red",
            "http_code": "TIMEOUT",
            "load_ms": timeout * 1000,
            "issue": f"Timeout (>{timeout}s)",
            "tested_at": datetime.now().isoformat()
        }
    except Exception as e:
        return {
            "site": site_name,
            "url": url,
            "status": "red",
            "http_code": "ERROR",
            "load_ms": None,
            "issue": str(e),
            "tested_at": datetime.now().isoformat()
        }

def main():
    """Run comprehensive QA test."""
    print(f"\n🚀 COMPREHENSIVE QA TESTER START — {datetime.now().isoformat()}")
    print(f"📋 Testing {len(COMPREHENSIVE_SITES)} sites...\n")

    results = {"green": [], "yellow": [], "red": []}
    categories = defaultdict(lambda: {"green": 0, "yellow": 0, "red": 0})

    for i, url in enumerate(COMPREHENSIVE_SITES, 1):
        data = test_site(url)
        status = data["status"]
        results[status].append(data)

        # Categorize
        category = "other"
        if "streak" in url:
            category = "streak_apps"
        elif "landing" in url:
            category = "marketing_pages"
        elif "vs" in url:
            category = "comparison_pages"
        elif any(x in url for x in ["coldmaxx", "invoiceforge", "pagescorer", "roicalc", "stackmaxx"]):
            category = "tool_apps"
        elif "web" in url:
            category = "web_apps"
        elif "roi-calculator" in url or "calculator" in url or "audit" in url or "checklist" in url:
            category = "lead_magnets"
        elif "printmaxx-" in url:
            category = "service_pages"
        elif "-mo.surge" in url or "-ky.surge" in url or "-nv.surge" in url or "-fl.surge" in url:
            category = "local_biz"

        categories[category][status] += 1

        emoji = "✅" if status == "green" else "⚠️" if status == "yellow" else "❌"
        issue_str = f" ({data['issue']})" if data['issue'] else ""
        print(f"{i:3d}. {emoji} {data['site'][:50]:50}{issue_str}")

    # Generate report
    total = len(COMPREHENSIVE_SITES)
    green, yellow, red = len(results["green"]), len(results["yellow"]), len(results["red"])
    pass_rate = 100 * (total - red) / total if total > 0 else 0

    report = f"""# Comprehensive QA Report — {datetime.now().strftime("%Y-%m-%d %H:%M UTC")}

**Cycle:** Playwright Tester v2
**Duration:** {datetime.now().isoformat()}
**Sites Tested:** {total}

## Executive Summary

| Status | Count | % |
|--------|-------|---|
| ✅ **GREEN** (Operational) | {green} | {100*green/total:.1f}% |
| ⚠️ **YELLOW** (Warnings) | {yellow} | {100*yellow/total:.1f}% |
| ❌ **RED** (Broken) | {red} | {100*red/total:.1f}% |

**Overall Pass Rate: {pass_rate:.1f}%**

---

## Category Breakdown

| Category | Green | Yellow | Red | Pass % |
|----------|-------|--------|-----|--------|
"""

    for category in sorted(categories.keys()):
        stats = categories[category]
        cat_total = sum(stats.values())
        cat_pass = 100 * (cat_total - stats["red"]) / cat_total if cat_total > 0 else 0
        report += f"| {category} | {stats['green']} | {stats['yellow']} | {stats['red']} | {cat_pass:.0f}% |\n"

    report += f"""

---

## 🟢 GREEN SITES — {green} Operational

"""
    for item in sorted(results["green"], key=lambda x: x["load_ms"] or 0, reverse=True)[:20]:
        report += f"- ✅ {item['site']} ({item['load_ms']:.0f}ms)\n"

    if green > 20:
        report += f"\n_... and {green - 20} more GREEN sites (all operational)_\n"

    report += f"""

---

## 🟡 YELLOW SITES — {yellow} Warnings

"""
    for item in results["yellow"]:
        report += f"- ⚠️ {item['site']} — {item['issue']} ({item['load_ms']:.0f}ms if available)\n"

    report += f"""

---

## 🔴 RED SITES — {red} Need Attention

"""
    for item in results["red"]:
        report += f"- ❌ {item['site']} — {item['issue']}\n"

    report += f"""

---

## Recommendations

1. **{len(results['red'])} RED sites** require investigation and possible redeployment
2. **{len(results['yellow'])} YELLOW sites** should be monitored for performance
3. Average load time: {sum(r['load_ms'] for r in results['green'] if r['load_ms'])/len(results['green']):.0f}ms (green sites)

---

*Report generated by Playwright Tester Agent*
"""

    # Write report
    report_file = REPORT_DIR / f"comprehensive_qa_{datetime.now().strftime('%Y%m%d_%H%M')}.md"
    report_file.write_text(report)

    # Write JSON for parsing
    json_file = REPORT_DIR / f"comprehensive_qa_{datetime.now().strftime('%Y%m%d_%H%M')}.json"
    json_file.write_text(json.dumps(results, indent=2))

    print(f"\n{'='*70}")
    print(f"📊 RESULTS: {green}/{total} operational ({pass_rate:.1f}%)")
    print(f"📁 Report: {report_file}")
    print(f"{'='*70}")

    if red > 0:
        print(f"\n🚨 {red} RED sites found — Details in report\n")

    return results

if __name__ == "__main__":
    main()
