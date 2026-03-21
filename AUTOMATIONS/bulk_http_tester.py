#!/usr/bin/env python3

from __future__ import annotations
"""Bulk HTTP status tester for all PRINTMAXX surge.sh deployments."""

import json
import time
import sys
import urllib.request
import urllib.error
import ssl
from datetime import datetime
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

PROJECT_ROOT = Path(__file__).resolve().parent.parent

# All known surge.sh sites from deploy list
SITES = [
    # Core Apps
    "prayerlock-app.surge.sh",
    "focuslock-app.surge.sh",
    "hilal-app.surge.sh",
    "mealmaxx-app.surge.sh",
    "coldmaxx-app.surge.sh",
    "sleepmaxx-app.surge.sh",
    "walktounlock-app.surge.sh",
    "habitforge-app.surge.sh",
    "adhd-streak.surge.sh",
    "stackmaxx-app.surge.sh",
    "roicalc-app.surge.sh",
    "prospectmaxx-app.surge.sh",
    "pitchdeck-app.surge.sh",
    "pagescorer-app.surge.sh",
    "invoiceforge-app.surge.sh",
    "sutra-streak-app.surge.sh",
    "art-streak-app.surge.sh",

    # Streak Apps
    "art-streak-app.surge.sh",
    "coding-streak-app.surge.sh",
    "fitness-streak-app.surge.sh",
    "journal-streak-app.surge.sh",
    "language-streak-app.surge.sh",
    "meditation-streak-app.surge.sh",
    "reading-streak-app.surge.sh",
    "gita-streak-app.surge.sh",
    "scripture-streak-lds.surge.sh",
    "quran-streak-app.surge.sh",
    "guru-streak-app.surge.sh",
    "torah-streak-app.surge.sh",
    "mormon-streak-app.surge.sh",
    "sikh-streak-app.surge.sh",

    # Streak Web Pages
    "art-streak.surge.sh",
    "buddhist-streak.surge.sh",
    "coding-streak.surge.sh",
    "fitness-streak.surge.sh",
    "gita-streak.surge.sh",
    "journal-streak.surge.sh",
    "language-streak.surge.sh",
    "meditation-streak.surge.sh",
    "mormon-streak.surge.sh",
    "quran-streak.surge.sh",
    "reading-streak.surge.sh",
    "sikh-streak.surge.sh",
    "torah-streak.surge.sh",
    "catholic-streak.surge.sh",
    "orthodox-streak.surge.sh",
    "protestant-streak.surge.sh",
    "baptist-streak.surge.sh",
    "methodist-streak.surge.sh",
    "lutheran-streak.surge.sh",
    "episcopal-streak.surge.sh",
    "pentecostal-streak.surge.sh",
    "evangelical-streak.surge.sh",
    "anglican-streak.surge.sh",
    "presbyterian-streak.surge.sh",
    "shia-streak.surge.sh",
    "sunni-streak.surge.sh",

    # Streak Landing Pages
    "shia-streak-landing.surge.sh",
    "sunni-streak-landing.surge.sh",
    "presbyterian-streak-landing.surge.sh",
    "anglican-streak-landing.surge.sh",
    "evangelical-streak-landing.surge.sh",
    "pentecostal-streak-landing.surge.sh",
    "episcopal-streak-landing.surge.sh",
    "lutheran-streak-landing.surge.sh",
    "methodist-streak-landing.surge.sh",
    "baptist-streak-landing.surge.sh",
    "protestant-streak-landing.surge.sh",
    "orthodox-streak-landing.surge.sh",
    "catholic-streak-landing.surge.sh",
    "fitness-streak-landing.surge.sh",
    "coding-streak-landing.surge.sh",
    "buddhist-streak-landing.surge.sh",
    "art-streak-landing.surge.sh",
    "torah-streak-landing.surge.sh",
    "sikh-streak-landing.surge.sh",
    "reading-streak-landing.surge.sh",
    "quran-streak-landing.surge.sh",
    "mormon-streak-landing.surge.sh",
    "meditation-streak-landing.surge.sh",
    "language-streak-landing.surge.sh",
    "journal-streak-landing.surge.sh",
    "gita-streak-landing.surge.sh",

    # Web Marketing Pages
    "prayerlock-web.surge.sh",
    "focuslock-web.surge.sh",
    "walktounlock-web.surge.sh",
    "sleepmaxx-web.surge.sh",
    "mealmaxx-web.surge.sh",
    "habitforge-web.surge.sh",
    "coldmaxx.surge.sh",
    "focuslock.surge.sh",
    "ramadan-tracker.surge.sh",
    "prayerlock.surge.sh",
    "walktounlock.surge.sh",
    "sleepmaxx.surge.sh",
    "mealmaxx.surge.sh",
    "hilal-ramadan.surge.sh",

    # Comparison Pages
    "printmaxx-comparisons.surge.sh",
    "prayerlock-vs-hallow.surge.sh",
    "focuslock-vs-opal.surge.sh",
    "coldmaxx-vs-instantly.surge.sh",
    "pagescorer-vs-gtmetrix.surge.sh",
    "sleepmaxx-vs-sleepcycle.surge.sh",
    "cursor-vs-claudecode.surge.sh",
    "instantly-vs-lemlist.surge.sh",
    "convertkit-vs-beehiiv.surge.sh",
    "best-cold-email-tools.surge.sh",

    # Lead Magnets
    "solopreneur-launch-checklist.surge.sh",
    "ramadan-daily-planner.surge.sh",
    "cold-email-calc.surge.sh",
    "subject-line-grader-pm.surge.sh",
    "cold-email-roi-calculator.surge.sh",
    "side-project-estimator.surge.sh",
    "printmaxx-tools.surge.sh",
    "financial-dashboard-pm.surge.sh",

    # Tools / SaaS
    "invoiceforge.surge.sh",
    "roicalc.surge.sh",
    "stackmaxx.surge.sh",
    "pagescorer.surge.sh",
    "prospectmaxx.surge.sh",
    "pitchdeck.surge.sh",
    "mcphub.surge.sh",
    "website-audit-tool.surge.sh",
    "invoicetracker.surge.sh",
    "contentcalendar.surge.sh",
    "sitescore-analyzer.surge.sh",
    "sitescore-app.surge.sh",
    "fiverr-services-pm.surge.sh",
    "printmaxx-content-calendar.surge.sh",
    "printmaxx-website-audit.surge.sh",
    "printmaxx-invoice-tracker.surge.sh",
    "printmaxx-compare.surge.sh",
    "printmaxx-store.surge.sh",
    "ai-stack-2026.surge.sh",
    "shopmetrics-pro.surge.sh",
    "sitescore-pro.surge.sh",
    "sitescore-free.surge.sh",
    "printmaxx-flowstack.surge.sh",
    "printmaxx-digital-services.surge.sh",
    "printmaxx-seo.surge.sh",
    "printmaxx-analyzer.surge.sh",
    "printmaxx-command.surge.sh",
    "social-dashboard-pm.surge.sh",

    # Hubs
    "printmaxx-apps.surge.sh",
    "printmaxx-services.surge.sh",
    "printmaxx-portfolio.surge.sh",
    "printmaxx-dashboard.surge.sh",
    "printmaxx-site.surge.sh",
    "printmaxx-control-panel.surge.sh",
    "website-analyzer-pm.surge.sh",
    "printmaxx.surge.sh",

    # Storefront / Thanks
    "printmaxx-storefront.surge.sh",
    "printmaxx-magnets.surge.sh",
    "printmaxx-thanks.surge.sh",

    # Local Biz / OpenClaw
    "find-plumbers-in-houston-texas-meetaplumber-com-houston-tx.surge.sh",
    "plumbers-just-enter-your-zip-code-houston-tx.surge.sh",
    "local-plumbing-experts-replace-plumbing-houston-tx.surge.sh",
    "plumbers-just-enter-your-zip-code-miami-fl.surge.sh",
    "local-plumbing-miami-fl.surge.sh",
    "miami-plumbing-zip.surge.sh",
    "best-dentist-office-austin-your-neighborhood-dentist-austin-tx.surge.sh",
    "handyman-matters-jacksonville-jacksonville-fl.surge.sh",
    "jacksonville-emergency-plumber-jacksonville-fl.surge.sh",
    "professional-plumbing-heating-cooling-memphis-tn.surge.sh",
    "south-tampa-locksmith-tampa-fl.surge.sh",
    "reliable-fence-nashville.surge.sh",
    "accurate-auto-nashville.surge.sh",
    "printmaxx-local-demos.surge.sh",
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
    "shop-of-memphis-preview.surge.sh",
    "jss-janitorial-memphis.surge.sh",
    "window-cleaning-in-portland-or-all-pro-metro-services-llc-portland-or.surge.sh",
    "top-rated-mobile-car-detailing-in-oklahoma-city-ok-pure-prof-oklahoma-city-ok.surge.sh",
    "mobile-auto-detailing-experts-in-oklahoma-city-champion-deta-oklahoma-city-ok.surge.sh",

    # Demos
    "restaurant-motion.surge.sh",
    "realtor-motion.surge.sh",
    "dental-motion.surge.sh",
    "restaurant-site-demo.surge.sh",
    "realtor-demo.surge.sh",
    "plumber-demo.surge.sh",
    "legal-demo.surge.sh",
    "fitness-demo.surge.sh",
    "dental-demo.surge.sh",
    "flowstack-demo.surge.sh",
    "shopmetrics-dashboard.surge.sh",
    "printmaxx-demos.surge.sh",
    "mikes-hvac-demo.surge.sh",
    "elite-fitness-demo.surge.sh",
    "smith-dentistry-demo.surge.sh",
    "perfect-lawn-demo.surge.sh",
    "bellas-salon-demo.surge.sh",
    "tonys-restaurant-demo.surge.sh",
    "joes-plumbing-demo.surge.sh",

    # Media
    "printmaxx-twitter-banner.surge.sh",
    "printmaxx-twitter-pfp.surge.sh",

    # Known broken (DNS label >63 chars)
    "local-plumbing-experts-plumbers-just-start-with-your-zip-miami-fl.surge.sh",

    # Older
    "hilal.surge.sh",

    # NEW: Louisville KY local biz (deployed Mar 8)
    "coit-cleaning-restoration-louisville-ky.surge.sh",
    "whitehouse-residential-commercial-painting-co-llc-louisville-ky.surge.sh",
    "a-1-concrete-leveling-louisville-louisville-ky.surge.sh",
    "down-to-earth-sealcoating-inc-louisville-ky.surge.sh",
    "certapro-painters-of-louisville-metro-louisville-ky.surge.sh",
    "skyrockett-construction-renovation-llc-louisville-ky.surge.sh",
    "garrett-s-presure-washing-louisville-ky.surge.sh",
    "david-fox-roofer-louisville-ky.surge.sh",
    "good-maintenance-cleaning-inc-louisville-ky.surge.sh",
    "a-1-aluminum-inc-louisville-ky.surge.sh",
    "the-maids-in-southern-louisville-llc-louisville-ky.surge.sh",
    "mccoy-window-gutter-cleaning-llc-louisville-ky.surge.sh",
    "square-it-away-contracting-llc-louisville-ky.surge.sh",
    "spindletop-draperies-inc-louisville-ky.surge.sh",
    "naturescape-louisville-ky.surge.sh",
    "jeff-reed-logging-tree-service-louisville-ky.surge.sh",
    "the-cutting-hedge-landscaping-mowing-louisville-ky.surge.sh",
    "greenworks-lawn-landscape-tree-llc-louisville-ky.surge.sh",
    "accurate-lawn-landscaping-inc-louisville-ky.surge.sh",
    "dave-s-tree-surgeons-inc-louisville-ky.surge.sh",
    "bob-ray-company-inc-louisville-ky.surge.sh",
    "a-b-landscaping-inc-louisville-ky.surge.sh",
    "er-tree-care-llc-louisville-ky.surge.sh",
    "new-leaf-tree-service-llc-louisville-ky.surge.sh",
    "climb-ax-tree-crane-service-louisville-ky.surge.sh",
    "bright-hauling-and-junk-removal-llc-louisville-ky.surge.sh",
    "new-seasons-auction-and-estates-louisville-ky.surge.sh",
    "mr-fix-it-solutions-llc-louisville-ky.surge.sh",
    "complete-home-services-louisville-ky.surge.sh",
    "wildcat-moving-llc-louisville-ky.surge.sh",
    "right-way-hauling-junk-removal-demolition-louisville-ky.surge.sh",
    "kings-hands-llc-louisville-ky.surge.sh",
    "jd-contractors-and-lawnscaping-llc-louisville-ky.surge.sh",
    "junk-king-louisville-louisville-ky.surge.sh",

    # NEW: Las Vegas / Orlando local biz
    "handyman-services-in-las-vegas-nv-89121-las-vegas-nv.surge.sh",
    "the-10-best-handyman-services-in-las-vegas-nv-2026-homeguide-las-vegas-nv.surge.sh",
    "top-rated-auto-repair-near-orlando-fl-carfax-orlando-fl.surge.sh",

    # NEW: Fiverr service pages (deployed Mar 8)
    "printmaxx-data-analysis.surge.sh",
    "printmaxx-ai-chatbot.surge.sh",
    "printmaxx-app-development.surge.sh",
    "printmaxx-content-writing.surge.sh",
    "printmaxx-seo-pages.surge.sh",
    "printmaxx-automation.surge.sh",
    "printmaxx-web-scraping.surge.sh",
    "printmaxx-cold-email.surge.sh",
    "printmaxx-landing-page.surge.sh",
    "printmaxx-website-design.surge.sh",

    # NEW: SaaS tools & misc (deployed Mar 8)
    "saas-stack-audit.surge.sh",
    "coreday.surge.sh",
    "revenue-leak-audit.surge.sh",

    # NEW: Test/debug deploys
    "printmaxx-openclaw-fix-test-001.surge.sh",
    "printmaxx-nested-test-001.surge.sh",
    "printmaxx-test-debug-deploy-001.surge.sh",

    # NEW: ColdMaxx marketing page (200.html)
    "coldmaxx.surge.sh",
]

# Deduplicate
SITES = list(dict.fromkeys(SITES))


def check_site(url: str, timeout: int = 10) -> dict:
    """Check HTTP status and response time for a site."""
    full_url = f"https://{url}"
    result = {
        "url": url,
        "full_url": full_url,
        "status": 0,
        "load_time_ms": 0,
        "error": None,
        "category": "RED",
        "content_length": 0,
    }

    ctx = ssl.create_default_context()

    start = time.time()
    try:
        req = urllib.request.Request(full_url, headers={
            "User-Agent": "PRINTMAXX-Tester/1.0"
        })
        with urllib.request.urlopen(req, timeout=timeout, context=ctx) as resp:
            body = resp.read()
            result["status"] = resp.status
            result["content_length"] = len(body)
            result["load_time_ms"] = int((time.time() - start) * 1000)

            # Categorize
            if resp.status == 200 and len(body) > 100:
                if result["load_time_ms"] > 3000:
                    result["category"] = "YELLOW"
                else:
                    result["category"] = "GREEN"
            elif resp.status == 200 and len(body) <= 100:
                result["category"] = "YELLOW"
                result["error"] = "Very small response body (possibly blank)"
            else:
                result["category"] = "RED"
                result["error"] = f"HTTP {resp.status}"
    except urllib.error.HTTPError as e:
        result["status"] = e.code
        result["load_time_ms"] = int((time.time() - start) * 1000)
        result["error"] = f"HTTP {e.code}: {e.reason}"
        result["category"] = "RED"
    except urllib.error.URLError as e:
        result["load_time_ms"] = int((time.time() - start) * 1000)
        result["error"] = f"URL Error: {str(e.reason)[:100]}"
        result["category"] = "RED"
    except Exception as e:
        result["load_time_ms"] = int((time.time() - start) * 1000)
        result["error"] = f"Error: {str(e)[:100]}"
        result["category"] = "RED"

    return result


def main():
    print(f"Testing {len(SITES)} sites...")
    print(f"Start: {datetime.now().isoformat()}")

    results = {"GREEN": [], "YELLOW": [], "RED": []}
    all_results = []

    with ThreadPoolExecutor(max_workers=20) as executor:
        future_to_url = {executor.submit(check_site, url): url for url in SITES}
        done_count = 0
        for future in as_completed(future_to_url):
            result = future.result()
            all_results.append(result)
            results[result["category"]].append(result)
            done_count += 1
            if done_count % 20 == 0:
                print(f"  Tested {done_count}/{len(SITES)}...")

    # Sort by category then URL
    for cat in results:
        results[cat].sort(key=lambda x: x["url"])

    # Calculate stats
    load_times = [r["load_time_ms"] for r in all_results if r["status"] == 200]
    avg_load = sum(load_times) / len(load_times) if load_times else 0
    max_load = max(load_times) if load_times else 0
    min_load = min(load_times) if load_times else 0

    # Summary
    print(f"\n{'='*60}")
    print(f"RESULTS: {len(SITES)} sites tested")
    print(f"  GREEN:  {len(results['GREEN'])} sites")
    print(f"  YELLOW: {len(results['YELLOW'])} sites")
    print(f"  RED:    {len(results['RED'])} sites")
    print(f"  Pass rate: {(len(results['GREEN']) + len(results['YELLOW'])) / len(SITES) * 100:.1f}%")
    print(f"  Avg load: {avg_load:.0f}ms | Min: {min_load}ms | Max: {max_load}ms")
    print(f"{'='*60}")

    if results["RED"]:
        print("\nRED (BROKEN):")
        for r in results["RED"]:
            print(f"  {r['url']} - {r['error']}")

    if results["YELLOW"]:
        print("\nYELLOW (WARNINGS):")
        for r in results["YELLOW"]:
            print(f"  {r['url']} - {r.get('error', f'{r["load_time_ms"]}ms')}")

    # Save JSON results
    output = {
        "tested_at": datetime.now().isoformat(),
        "total": len(SITES),
        "green": len(results["GREEN"]),
        "yellow": len(results["YELLOW"]),
        "red": len(results["RED"]),
        "pass_rate": f"{(len(results['GREEN']) + len(results['YELLOW'])) / len(SITES) * 100:.1f}%",
        "avg_load_ms": int(avg_load),
        "max_load_ms": max_load,
        "min_load_ms": min_load,
        "red_sites": [{"url": r["url"], "error": r["error"], "status": r["status"]} for r in results["RED"]],
        "yellow_sites": [{"url": r["url"], "error": r.get("error"), "load_ms": r["load_time_ms"]} for r in results["YELLOW"]],
        "all_results": sorted(all_results, key=lambda x: x["url"]),
    }

    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    out_path = PROJECT_ROOT / "AUTOMATIONS" / "agent" / "swarm" / "reports" / f"test_results_{timestamp}.json"
    with open(out_path, "w") as f:
        json.dump(output, f, indent=2)
    print(f"\nResults saved to {out_path}")

    return output


if __name__ == "__main__":
    main()
