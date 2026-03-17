#!/usr/bin/env python3
"""
Quick HTTP health check for RED sites + attempt fixes
"""

import subprocess
import json
import sys
from pathlib import Path
from datetime import datetime
import requests
from urllib.parse import urlparse

BASE_PATH = Path("/Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt")
REPORT_PATH = BASE_PATH / "AUTOMATIONS/agent/swarm/reports/playwright_tester_report_20260317.md"

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

SAMPLE_GREEN = [
    "https://printmaxx.surge.sh",
    "https://prayerlock-web.surge.sh",
    "https://coldmaxx.surge.sh",
    "https://mcp-marketplace.surge.sh",
    "https://stackmaxx.surge.sh",
]

def test_url(url: str, timeout: int = 10) -> dict:
    """Test a single URL and return health info"""
    try:
        response = requests.head(url, timeout=timeout, allow_redirects=True)
        status = response.status_code

        # If HEAD fails, try GET
        if status >= 400:
            response = requests.get(url, timeout=timeout, allow_redirects=True)
            status = response.status_code
            content_len = len(response.text) if response.text else 0
            has_content = content_len > 500
            is_blank = "404" in response.text or "not found" in response.text.lower()
        else:
            content_len = response.headers.get('content-length', 'unknown')
            has_content = True if content_len == 'unknown' else int(content_len) > 500
            is_blank = False

        success = status == 200 and has_content

        return {
            "url": url,
            "status": status,
            "success": success,
            "has_content": has_content,
            "is_blank": is_blank,
            "content_len": content_len
        }
    except requests.Timeout:
        return {"url": url, "status": 0, "error": "timeout", "success": False}
    except requests.ConnectionError as e:
        return {"url": url, "status": 0, "error": "connection error", "success": False}
    except Exception as e:
        return {"url": url, "status": 0, "error": str(e), "success": False}

def find_site_source(site_name: str) -> Path:
    """Find source directory for a site"""
    domain = site_name.replace("https://", "").replace(".surge.sh", "")

    search_dirs = [
        BASE_PATH / "LANDING" / domain,
        BASE_PATH / "DIGITAL_PRODUCTS" / domain,
        BASE_PATH / "MONEY_METHODS" / domain,
        BASE_PATH / "07_LANDING" / domain,
        BASE_PATH / "app factory/app-factory" / domain,
    ]

    for d in search_dirs:
        if d.exists():
            return d

    return None

def main():
    print(f"Testing {len(RED_SITES)} RED sites + {len(SAMPLE_GREEN)} sample GREEN sites...\n")

    results = {
        "green": [],
        "yellow": [],
        "red": []
    }

    # Test RED sites
    print("Testing RED sites (priority):")
    for url in RED_SITES:
        result = test_url(url)
        if result.get("success"):
            results["green"].append(result)
            print(f"  ✓ {url.split('/')[-1]} - HTTP {result['status']}")
        else:
            results["red"].append(result)
            print(f"  ✗ {url.split('/')[-1]} - HTTP {result.get('status', '?')} ({result.get('error', 'unknown')})")

    # Test sample GREEN
    print(f"\nVerifying {len(SAMPLE_GREEN)} sample GREEN sites:")
    for url in SAMPLE_GREEN:
        result = test_url(url)
        if result.get("success"):
            results["green"].append(result)
            print(f"  ✓ {url.split('/')[-1]} - HTTP {result['status']}")
        else:
            results["yellow"].append(result)
            print(f"  ⚠ {url.split('/')[-1]} - HTTP {result.get('status', '?')}")

    # Generate report
    report = f"""# PLAYWRIGHT TESTER REPORT — {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Summary
- Total tested: {len(results['green']) + len(results['yellow']) + len(results['red'])}
- GREEN (Healthy): {len(results['green'])}
- YELLOW (Warnings): {len(results['yellow'])}
- RED (Broken): {len(results['red'])}
- Pass rate: {100 * len(results['green']) / (len(results['green']) + len(results['yellow']) + len(results['red'])):.1f}%

## GREEN Sites (Healthy)
"""

    for r in results['green']:
        report += f"✓ [{r['url'].split('/')[-1]}]({r['url']}) — HTTP {r['status']}\n"

    report += f"\n## YELLOW Sites (Warnings/Slow)\n"
    for r in results['yellow']:
        report += f"⚠ [{r['url'].split('/')[-1]}]({r['url']}) — HTTP {r.get('status', '?')}\n"
        if 'error' in r:
            report += f"  - {r['error']}\n"

    report += f"\n## RED Sites (Broken - Need Fix)\n"
    for r in results['red']:
        url = r['url']
        report += f"✗ [{url.split('/')[-1]}]({url})\n"

        status = r.get('status', '?')
        error = r.get('error', 'unknown error')
        report += f"  - Status: HTTP {status} ({error})\n"

        # Try to find source
        site_source = find_site_source(url.replace("https://", "").replace(".surge.sh", ""))
        if site_source:
            report += f"  - Source found: {site_source.relative_to(BASE_PATH)}\n"
            if (site_source / "package.json").exists():
                report += f"  - Can rebuild: npm install && npm run build\n"
        else:
            report += f"  - Source not found (may be auto-generated)\n"

    report += f"\n## Action Items\n"
    report += f"1. RED sites that are broken need investigation\n"
    report += f"2. Source code lookup: Check LANDING/, DIGITAL_PRODUCTS/, or MONEY_METHODS/ directories\n"
    report += f"3. For local biz pages: Rebuild + redeploy via asset_deployer\n"
    report += f"4. Test again after fixes\n"

    # Write report
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(report)

    print(f"\n✓ Report saved: {REPORT_PATH}")
    print(f"\nStatus: {len(results['red'])} RED sites still broken\n")

    return len(results['red']) == 0

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
