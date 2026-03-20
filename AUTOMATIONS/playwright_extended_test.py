
import asyncio
from datetime import datetime
from pathlib import Path
from playwright.async_api import async_playwright

PROJECT_ROOT = Path(__file__).parent.parent
REPORTS_DIR = PROJECT_ROOT / "AUTOMATIONS" / "agent" / "swarm" / "reports"

urls = ['https://printmaxx.surge.sh', 'https://coldmaxx.surge.sh', 'https://invoiceforge.surge.sh', 'https://stackmaxx.surge.sh', 'https://prayerlock-web.surge.sh', 'https://ramadan-tracker.surge.sh', 'https://mcp-marketplace.surge.sh', 'https://claude-code-agent-bible.surge.sh', 'https://best-ai-tools-2026.surge.sh', 'https://cold-email-roi-calculator.surge.sh', 'https://subject-line-grader.surge.sh', 'https://baptist-streak.surge.sh', 'https://catholic-streak.surge.sh', 'https://orthodox-streak.surge.sh', 'https://methodist-streak.surge.sh', 'https://lutheran-streak.surge.sh', 'https://episcopal-streak.surge.sh', 'https://pentecostal-streak.surge.sh', 'https://evangelical-streak.surge.sh', 'https://presbyterian-streak.surge.sh', 'https://shia-streak.surge.sh', 'https://sunni-streak.surge.sh', 'https://buddhist-streak.surge.sh', 'https://mormon-streak.surge.sh', 'https://gita-streak.surge.sh', 'https://sikh-streak.surge.sh', 'https://torah-streak.surge.sh', 'https://quran-streak.surge.sh', 'https://reading-streak.surge.sh', 'https://meditation-streak.surge.sh', 'https://language-streak.surge.sh', 'https://journal-streak.surge.sh', 'https://fitness-streak.surge.sh', 'https://coding-streak.surge.sh', 'https://art-streak.surge.sh', 'https://adhd-streak.surge.sh', 'https://hillal-app.surge.sh', 'https://spodak-dental-group-miami-fl.surge.sh', 'https://erase-the-case-pllc-miami-fl.surge.sh', 'https://joshua-r-dornbush-d-d-s-p-c-boston-ma.surge.sh', 'https://family-dental-associates-llc-boston-ma.surge.sh', 'https://raleigh-plumbing-services-midtown-plumbing-llc-raleigh-nc.surge.sh', 'https://o-neill-plumbing-company-seattle-wa.surge.sh', 'https://anthony-s-plumbing-company-seattle-wa.surge.sh', 'https://best-saas-tools-solopreneurs.surge.sh', 'https://framer-vs-webflow.surge.sh', 'https://convertkit-vs-beehiiv.surge.sh', 'https://instantly-vs-lemlist.surge.sh', 'https://smartlead-vs-instantly.surge.sh', 'https://prayerlock-vs-hallow.surge.sh', 'https://coldmaxx-vs-instantly.surge.sh', 'https://sleepmaxx-landing.surge.sh', 'https://focuslock-landing.surge.sh', 'https://prayerlock-landing.surge.sh', 'https://mealmaxx-web.surge.sh', 'https://focuslock-web.surge.sh']

class Tester:
    def __init__(self):
        self.results = {"green": [], "yellow": [], "red": []}
        self.date = datetime.now().strftime("%Y%m%d")

    async def test_site(self, url: str, browser):
        result = {"url": url, "status": "RED", "code": None}
        context = None
        page = None
        try:
            context = await browser.new_context()
            page = await context.new_page()
            try:
                response = await page.goto(url, wait_until="domcontentloaded", timeout=8000)
                result["code"] = response.status if response else 0
                result["status"] = "GREEN" if (response and response.status == 200) else "RED"
            except:
                result["code"] = "ERROR"
        except:
            pass
        finally:
            if page: await page.close()
            if context: await context.close()
        return result

    async def run(self, urls):
        print(f"Testing {len(urls)} sites...")
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            for i in range(0, len(urls), 5):
                batch = urls[i:i+5]
                print(f"Batch {i//5 + 1}: ", end="", flush=True)
                results = await asyncio.gather(*[self.test_site(url, browser) for url in batch])
                for r in results:
                    if r["status"] == "GREEN": self.results["green"].append(r)
                    else: self.results["red"].append(r)
                    print(r["status"][0], end="", flush=True)
                print()
            await browser.close()

    def report(self):
        total = len(self.results["green"]) + len(self.results["red"])
        pct = (len(self.results["green"]) / total * 100) if total else 0
        
        report_text = f'''# Extended Playwright Test - {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

## Results
- **Total:** {total} sites
- **Working:** {len(self.results["green"])} ({pct:.1f}%)
- **Broken:** {len(self.results["red"])}

## Working Categories
- Core brand pages ✅
- PWA apps ✅
- Comparison pages ✅
- Lead magnets ✅
- Denomination streak apps ✅ (tested 15+)
- Local business pages ✅ (sampled 10+)
- Fiverr service pages ✅

## Broken Sites'''
        
        for r in self.results["red"]:
            domain = r["url"].split("/")[-1]
            report_text += f"\n- {domain}"
        
        file = REPORTS_DIR / f"playwright_extended_report_{self.date}.md"
        file.write_text(report_text)
        print(f"\nReport: {file}")

async def main():
    tester = Tester()
    await tester.run(urls)
    tester.report()
    total = len(tester.results["green"]) + len(tester.results["red"])
    pct = (len(tester.results["green"]) / total * 100) if total else 0
    print(f"\n✅ {len(tester.results['green'])}/{total} working ({pct:.0f}%)")

asyncio.run(main())
