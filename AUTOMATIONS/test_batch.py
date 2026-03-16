#!/usr/bin/env python3
import asyncio
import json
from datetime import datetime
from pathlib import Path
import sys

# Test URLs - 10 RED + 20 samples
TEST_URLS = [
    # RED sites from last cycle
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

    # GREEN samples
    "https://printmaxx.surge.sh",
    "https://coldmaxx.surge.sh",
    "https://prayerlock-web.surge.sh",
    "https://stackmaxx.surge.sh",
    "https://invoiceforge.surge.sh",
    "https://pdfmaxx.surge.sh",
    "https://hilal-landing.surge.sh",
    "https://mcp-marketplace.surge.sh",
    "https://coreday.surge.sh",
    "https://ramadan-tracker.surge.sh",

    # YELLOW samples
    "https://printmaxx-tools.surge.sh",
    "https://printmaxx-site.surge.sh",
    "https://printmaxx-services.surge.sh",
    "https://semrush-vs-ahrefs.surge.sh",
    "https://convertkit-vs-beehiiv.surge.sh",
    "https://best-ai-tools-2026.surge.sh",
    "https://scripture-streak-landing.surge.sh",
    "https://prayerlock-landing.surge.sh",
    "https://spodak-dental-group-miami-fl.surge.sh",
    "https://goldsberry-portz-divorce-family-lawyers-pllc-houston-tx.surge.sh"
]

async def test_site(url):
    """Test a single site with Playwright"""
    try:
        from playwright.async_api import async_playwright

        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()

            start_time = datetime.now()
            try:
                response = await page.goto(url, wait_until="domcontentloaded", timeout=15000)
                load_time_ms = (datetime.now() - start_time).total_seconds() * 1000
                status = response.status if response else 999

                # Check console errors
                errors = []
                def log_handler(msg):
                    if 'error' in msg.type.lower():
                        errors.append(msg.text)
                page.on("console", log_handler)

                # Check for main content
                try:
                    body = await page.query_selector("body")
                    has_content = await body.evaluate("el => el.children.length > 0") if body else False
                except:
                    has_content = False

                # Categorize result
                if status == 200 and has_content and load_time_ms < 5000 and len(errors) == 0:
                    result = "GREEN"
                elif status == 200 and has_content:
                    result = "YELLOW"
                else:
                    result = "RED"

                return {
                    "url": url,
                    "status": status,
                    "result": result,
                    "load_time_ms": round(load_time_ms),
                    "has_content": has_content,
                    "error_count": len(errors),
                    "errors": errors[:2]  # first 2 errors only
                }
            except Exception as e:
                return {
                    "url": url,
                    "status": 0,
                    "result": "RED",
                    "load_time_ms": -1,
                    "has_content": False,
                    "error": str(e)[:100]
                }
            finally:
                await browser.close()
    except ImportError:
        return {
            "url": url,
            "status": 0,
            "result": "SKIP",
            "error": "Playwright not installed"
        }

async def main():
    print(f"Testing {len(TEST_URLS)} sites...")
    results = []

    for url in TEST_URLS:
        result = await test_site(url)
        results.append(result)
        print(f"[{result['result']}] {url.split('/')[-1]} - {result.get('load_time_ms', '?')}ms")

    # Summary
    green = sum(1 for r in results if r['result'] == 'GREEN')
    yellow = sum(1 for r in results if r['result'] == 'YELLOW')
    red = sum(1 for r in results if r['result'] == 'RED')
    total = len(results)
    pass_rate = ((green + yellow) / total * 100) if total > 0 else 0

    print(f"\n=== SUMMARY ===")
    print(f"GREEN: {green}/{total}")
    print(f"YELLOW: {yellow}/{total}")
    print(f"RED: {red}/{total}")
    print(f"Pass rate: {pass_rate:.1f}%")

    # Save results
    report = {
        "tested_at": datetime.now().isoformat(),
        "total": total,
        "green": green,
        "yellow": yellow,
        "red": red,
        "pass_rate": f"{pass_rate:.1f}%",
        "results": results,
        "red_sites": [r for r in results if r['result'] == 'RED']
    }

    Path("/Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt/AUTOMATIONS/agent/swarm/reports").mkdir(parents=True, exist_ok=True)

    with open("/Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt/AUTOMATIONS/agent/swarm/reports/test_batch_results.json", "w") as f:
        json.dump(report, f, indent=2)

    print(f"\nResults saved to test_batch_results.json")
    return report

if __name__ == "__main__":
    asyncio.run(main())
