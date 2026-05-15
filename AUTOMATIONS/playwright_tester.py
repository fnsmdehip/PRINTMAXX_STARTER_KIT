#!/usr/bin/env python3
import subprocess
import json
import time
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
SCREENSHOTS_DIR = BASE_DIR / "AUTOMATIONS/agent/swarm/screenshots"
REPORTS_DIR = BASE_DIR / "AUTOMATIONS/agent/swarm/reports"

# Test sample across all categories
TEST_SITES = [
    # Critical apps (PWA)
    ("truthscope.surge.sh", "app", "Lie Detector"),
    ("cnsnt-web.surge.sh", "app", "Consent Manager"),
    ("prayerlock-web.surge.sh", "app", "Prayer Lock"),
    ("focuslock-web.surge.sh", "app", "Focus Lock"),
    # New deployments (landing pages)
    ("androx.surge.sh", "landing", "Androx"),
    ("printmaxx-privacy.surge.sh", "legal", "Privacy Policy"),
    ("printmaxx-tos.surge.sh", "legal", "Terms of Service"),
    ("fnsmdehip-research.surge.sh", "content", "Research Blog"),
    # Tools & calculators
    ("invoiceforge.surge.sh", "tool", "Invoice Forge"),
    ("pagescorer.surge.sh", "tool", "Page Scorer"),
    ("coldmaxx.surge.sh", "app", "ColdMaxx"),
    # Comparison pages
    ("smartlead-vs-instantly.surge.sh", "comparison", "Smartlead vs Instantly"),
    ("n8n-vs-zapier-vs-make.surge.sh", "comparison", "n8n vs Zapier"),
    ("best-cold-email-tools.surge.sh", "comparison", "Cold Email Tools"),
    # Landing pages
    ("scripture-streak-landing.surge.sh", "landing", "Scripture Streak"),
    ("hilal-landing.surge.sh", "landing", "Hilal"),
    ("couples-streak-landing.surge.sh", "landing", "Couples Streak"),
    # Content/research
    ("best-ai-tools-2026.surge.sh", "comparison", "Best AI Tools 2026"),
    ("best-saas-tools-solopreneurs.surge.sh", "comparison", "Best SaaS Tools"),
]

def test_site(url, category, name):
    """Test a single site using curl"""
    result = {
        "url": url,
        "category": category,
        "name": name,
        "status": "UNKNOWN",
        "http_status": None,
        "errors": [],
        "timestamp": datetime.now().isoformat(),
    }

    try:
        # Test using curl (simple HTTP status check)
        curl_cmd = f"curl -s -o /dev/null -w '%{{http_code}}' 'https://{url}' -m 5"
        response = subprocess.run(curl_cmd, shell=True, capture_output=True, text=True, timeout=10)
        http_status = response.stdout.strip()

        result["http_status"] = http_status

        if http_status == "200":
            result["status"] = "GREEN"
        elif http_status in ["301", "302", "303", "307"]:
            result["status"] = "YELLOW"  # Redirect
            result["errors"].append(f"Redirect: {http_status}")
        elif http_status in ["404", "500", "502", "503"]:
            result["status"] = "RED"
            result["errors"].append(f"HTTP {http_status}")
        else:
            result["status"] = "YELLOW"
            result["errors"].append(f"HTTP {http_status}")

    except Exception as e:
        result["status"] = "RED"
        result["errors"].append(str(e))

    return result

def main():
    """Run full test cycle"""
    print("[PLAYWRIGHT TESTER] Starting test cycle...")

    results = {
        "timestamp": datetime.now().isoformat(),
        "total_tested": len(TEST_SITES),
        "by_status": {"GREEN": 0, "YELLOW": 0, "RED": 0},
        "by_category": {},
        "sites": [],
    }

    for url, category, name in TEST_SITES:
        print(f"  Testing {name:30} ({url:45})...", end=" ", flush=True)

        test_result = test_site(url, category, name)
        results["sites"].append(test_result)
        results["by_status"][test_result["status"]] += 1

        if category not in results["by_category"]:
            results["by_category"][category] = {"total": 0, "passed": 0}
        results["by_category"][category]["total"] += 1
        if test_result["status"] == "GREEN":
            results["by_category"][category]["passed"] += 1

        print(f"[{test_result['status']}]")
        time.sleep(0.2)  # Rate limit

    # Write report
    report_file = REPORTS_DIR / f"playwright_tester_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"

    with open(report_file, "w") as f:
        f.write("# Playwright Tester Report\n\n")
        f.write(f"**Date:** {datetime.now().isoformat()}\n\n")
        f.write(f"**Total Sites Tested:** {results['total_tested']}\n\n")

        f.write("## Summary by Status\n\n")
        pct = 100*results['by_status']['GREEN']//results['total_tested'] if results['total_tested'] > 0 else 0
        f.write(f"- **GREEN (Passing):** {results['by_status']['GREEN']} ({pct}%)\n")
        f.write(f"- **YELLOW (Warnings):** {results['by_status']['YELLOW']}\n")
        f.write(f"- **RED (Failing):** {results['by_status']['RED']}\n\n")

        f.write("## By Category\n\n")
        for category, stats in results["by_category"].items():
            pass_rate = 100 * stats["passed"] // stats["total"] if stats["total"] > 0 else 0
            f.write(f"- **{category}**: {stats['passed']}/{stats['total']} passing ({pass_rate}%)\n")

        f.write("\n## Detailed Results\n\n")
        for site in results["sites"]:
            f.write(f"### {site['name']} ({site['url']})\n")
            f.write(f"- **Status:** {site['status']}\n")
            f.write(f"- **HTTP Status:** {site['http_status']}\n")
            if site['errors']:
                f.write(f"- **Errors:** {', '.join(site['errors'])}\n")
            f.write("\n")

    # Write JSON
    json_file = REPORTS_DIR / f"playwright_tester_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(json_file, "w") as f:
        json.dump(results, f, indent=2)

    print(f"\n[DONE] Report: {report_file}")
    print(f"[DONE] JSON: {json_file}")
    print(f"\nSummary: {results['by_status']['GREEN']} GREEN, {results['by_status']['YELLOW']} YELLOW, {results['by_status']['RED']} RED")

    return results

if __name__ == "__main__":
    main()
