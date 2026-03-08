#!/usr/bin/env python3
"""
PRINTMAXX Playwright Site Tester (async/concurrent)
Tests all deployed surge.sh sites for uptime, content, and errors.
Outputs: screenshots + test_report_{date}.md + quality_alerts.txt
Concurrency: 8 parallel tabs — full test in ~2 min vs 20+ min serial.
"""

import asyncio
import json
import re
import sys
import time
from datetime import datetime
from pathlib import Path

from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeout

# ── Paths ──────────────────────────────────────────────────────────────────────
PROJECT_ROOT    = Path("/Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt")
SCREENSHOTS_DIR = PROJECT_ROOT / "AUTOMATIONS/agent/swarm/screenshots"
REPORTS_DIR     = PROJECT_ROOT / "AUTOMATIONS/agent/swarm/reports"
DEPLOYED_ASSETS = PROJECT_ROOT / "AUTOMATIONS/agent/swarm/deployed_assets.json"
ALERTS_PATH     = PROJECT_ROOT / "AUTOMATIONS/agent/swarm/quality_alerts.txt"

SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)
REPORTS_DIR.mkdir(parents=True, exist_ok=True)

TODAY       = datetime.now().strftime("%Y%m%d")
REPORT_PATH = REPORTS_DIR / f"test_report_{TODAY}.md"

CONCURRENCY = 8       # parallel browser tabs
TIMEOUT_MS  = 15_000  # ms per site

# ── Full site list (deployed_assets.json + new surge deployments) ─────────────
ALL_SITES = [
    # Core apps
    ("PrayerLock App",        "https://prayerlock-app.surge.sh",     "core_apps"),
    ("FocusLock App",         "https://focuslock-app.surge.sh",      "core_apps"),
    ("Hilal App",             "https://hilal-app.surge.sh",           "core_apps"),
    ("MealMaxx App",          "https://mealmaxx-app.surge.sh",        "core_apps"),
    ("ColdMaxx App",          "https://coldmaxx-app.surge.sh",        "core_apps"),
    ("SleepMaxx App",         "https://sleepmaxx-app.surge.sh",       "core_apps"),
    ("WalkToUnlock App",      "https://walktounlock-app.surge.sh",    "core_apps"),
    ("HabitForge App",        "https://habitforge-app.surge.sh",      "core_apps"),
    # Streak apps (app pages)
    ("Art Streak App",        "https://art-streak-app.surge.sh",      "streak_apps"),
    ("Coding Streak App",     "https://coding-streak-app.surge.sh",   "streak_apps"),
    ("Fitness Streak App",    "https://fitness-streak-app.surge.sh",  "streak_apps"),
    ("Journal Streak App",    "https://journal-streak-app.surge.sh",  "streak_apps"),
    ("Language Streak App",   "https://language-streak-app.surge.sh", "streak_apps"),
    ("Meditation Streak App", "https://meditation-streak-app.surge.sh","streak_apps"),
    ("Reading Streak App",    "https://reading-streak-app.surge.sh",  "streak_apps"),
    ("Sutra Streak App",      "https://sutra-streak-app.surge.sh",    "streak_apps"),
    ("Gita Streak App",       "https://gita-streak-app.surge.sh",     "streak_apps"),
    ("Scripture Streak LDS",  "https://scripture-streak-lds.surge.sh","streak_apps"),
    ("Quran Streak App",      "https://quran-streak-app.surge.sh",    "streak_apps"),
    ("Guru Streak App",       "https://guru-streak-app.surge.sh",     "streak_apps"),
    ("Torah Streak App",      "https://torah-streak-app.surge.sh",    "streak_apps"),
    ("Mormon Streak App",     "https://mormon-streak-app.surge.sh",   "streak_apps"),
    ("Sikh Streak App",       "https://sikh-streak-app.surge.sh",     "streak_apps"),
    # Streak landing pages (new today)
    ("Art Streak Landing",        "https://art-streak.surge.sh",         "streak_landing"),
    ("Coding Streak Landing",     "https://coding-streak.surge.sh",      "streak_landing"),
    ("Fitness Streak Landing",    "https://fitness-streak.surge.sh",     "streak_landing"),
    ("Journal Streak Landing",    "https://journal-streak.surge.sh",     "streak_landing"),
    ("Language Streak Landing",   "https://language-streak.surge.sh",    "streak_landing"),
    ("Meditation Streak Landing", "https://meditation-streak.surge.sh",  "streak_landing"),
    ("Reading Streak Landing",    "https://reading-streak.surge.sh",     "streak_landing"),
    ("Quran Streak Landing",      "https://quran-streak.surge.sh",       "streak_landing"),
    ("Gita Streak Landing",       "https://gita-streak.surge.sh",        "streak_landing"),
    ("Torah Streak Landing",      "https://torah-streak.surge.sh",       "streak_landing"),
    ("Sikh Streak Landing",       "https://sikh-streak.surge.sh",        "streak_landing"),
    ("Mormon Streak Landing",     "https://mormon-streak.surge.sh",      "streak_landing"),
    ("Buddhist Streak Landing",   "https://buddhist-streak.surge.sh",    "streak_landing"),
    # Web marketing pages
    ("PrayerLock Web",   "https://prayerlock-web.surge.sh",   "web_marketing"),
    ("FocusLock Web",    "https://focuslock-web.surge.sh",    "web_marketing"),
    ("WalkToUnlock Web", "https://walktounlock-web.surge.sh", "web_marketing"),
    ("SleepMaxx Web",    "https://sleepmaxx-web.surge.sh",    "web_marketing"),
    ("MealMaxx Web",     "https://mealmaxx-web.surge.sh",     "web_marketing"),
    ("HabitForge Web",   "https://habitforge-web.surge.sh",   "web_marketing"),
    ("ColdMaxx",         "https://coldmaxx.surge.sh",         "web_marketing"),
    ("FocusLock",        "https://focuslock.surge.sh",        "web_marketing"),
    ("Ramadan Tracker",  "https://ramadan-tracker.surge.sh",  "web_marketing"),
    ("PrayerLock",       "https://prayerlock.surge.sh",       "web_marketing"),
    ("WalkToUnlock",     "https://walktounlock.surge.sh",     "web_marketing"),
    ("SleepMaxx",        "https://sleepmaxx.surge.sh",        "web_marketing"),
    ("MealMaxx",         "https://mealmaxx.surge.sh",         "web_marketing"),
    ("Hilal Ramadan",    "https://hilal-ramadan.surge.sh",    "web_marketing"),
    # New this session
    ("PrintMaxx Content Calendar", "https://printmaxx-content-calendar.surge.sh", "new_tools"),
    ("PrintMaxx Website Audit",    "https://printmaxx-website-audit.surge.sh",    "new_tools"),
    ("PrintMaxx Invoice Tracker",  "https://printmaxx-invoice-tracker.surge.sh",  "new_tools"),
    ("PrintMaxx Compare",          "https://printmaxx-compare.surge.sh",           "new_tools"),
    ("PrintMaxx Store",            "https://printmaxx-store.surge.sh",             "new_tools"),
    ("AI Stack 2026",              "https://ai-stack-2026.surge.sh",               "new_tools"),
    ("Reliable Fence Nashville",   "https://reliable-fence-nashville.surge.sh",    "new_tools"),
    ("Accurate Auto Nashville",    "https://accurate-auto-nashville.surge.sh",     "new_tools"),
    # Hubs
    ("PrintMaxx Apps Hub",   "https://printmaxx-apps.surge.sh",      "hubs"),
    ("PrintMaxx Services",   "https://printmaxx-services.surge.sh",  "hubs"),
    ("PrintMaxx Portfolio",  "https://printmaxx-portfolio.surge.sh", "hubs"),
    ("PrintMaxx Dashboard",  "https://printmaxx-dashboard.surge.sh", "hubs"),
    # Tools / SaaS
    ("InvoiceForge",        "https://invoiceforge.surge.sh",                "tools_saas"),
    ("ROI Calc",            "https://roicalc.surge.sh",                     "tools_saas"),
    ("StackMaxx",           "https://stackmaxx.surge.sh",                   "tools_saas"),
    ("PageScorer",          "https://pagescorer.surge.sh",                  "tools_saas"),
    ("ProspectMaxx",        "https://prospectmaxx.surge.sh",                "tools_saas"),
    ("PitchDeck",           "https://pitchdeck.surge.sh",                   "tools_saas"),
    ("MCP Hub",             "https://mcphub.surge.sh",                      "tools_saas"),
    ("Website Audit Tool",  "https://website-audit-tool.surge.sh",          "tools_saas"),
    ("Invoice Tracker",     "https://invoicetracker.surge.sh",              "tools_saas"),
    ("Content Calendar",    "https://contentcalendar.surge.sh",             "tools_saas"),
    ("SiteScore Analyzer",  "https://sitescore-analyzer.surge.sh",          "tools_saas"),
    ("SiteScore App",       "https://sitescore-app.surge.sh",               "tools_saas"),
    ("Fiverr Services PM",  "https://fiverr-services-pm.surge.sh",          "tools_saas"),
    ("SiteScore Pro",       "https://sitescore-pro.surge.sh",               "tools_saas"),
    ("SiteScore Free",      "https://sitescore-free.surge.sh",              "tools_saas"),
    ("PrintMaxx Flowstack", "https://printmaxx-flowstack.surge.sh",         "tools_saas"),
    ("PrintMaxx Digital Services","https://printmaxx-digital-services.surge.sh","tools_saas"),
    ("ShopMetrics Pro",     "https://shopmetrics-pro.surge.sh",             "tools_saas"),
    ("PrintMaxx SEO",       "https://printmaxx-seo.surge.sh",               "tools_saas"),
    ("PrintMaxx Analyzer",  "https://printmaxx-analyzer.surge.sh",          "tools_saas"),
    ("PrintMaxx Command",   "https://printmaxx-command.surge.sh",           "tools_saas"),
    ("Social Dashboard PM", "https://social-dashboard-pm.surge.sh",         "tools_saas"),
    ("Cold Email Calc",     "https://cold-email-calc.surge.sh",             "tools_saas"),
    # Local Biz / OpenClaw
    ("Plumber Houston MeetAPlumber","https://find-plumbers-in-houston-texas-meetaplumber-com-houston-tx.surge.sh","local_biz"),
    ("Plumber Houston ZIP",         "https://plumbers-just-enter-your-zip-code-houston-tx.surge.sh",              "local_biz"),
    ("Plumber Houston Local",       "https://local-plumbing-experts-replace-plumbing-houston-tx.surge.sh",        "local_biz"),
    ("Plumber Miami ZIP",           "https://plumbers-just-enter-your-zip-code-miami-fl.surge.sh",               "local_biz"),
    ("Plumber Miami Local",         "https://local-plumbing-miami-fl.surge.sh",                                  "local_biz"),
    ("Plumber Miami ZIP2",          "https://local-plumbing-experts-plumbers-just-start-with-your-zip-miami-fl.surge.sh","local_biz"),
    ("Dentist Austin",              "https://best-dentist-office-austin-your-neighborhood-dentist-austin-tx.surge.sh","local_biz"),
    ("Handyman Jacksonville",       "https://handyman-matters-jacksonville-jacksonville-fl.surge.sh",             "local_biz"),
    ("Emergency Plumber Jacksonville","https://jacksonville-emergency-plumber-jacksonville-fl.surge.sh",          "local_biz"),
    ("Plumbing HVAC Memphis",       "https://professional-plumbing-heating-cooling-memphis-tn.surge.sh",         "local_biz"),
    ("Locksmith Tampa",             "https://south-tampa-locksmith-tampa-fl.surge.sh",                           "local_biz"),
    ("Miami Plumbing ZIP",          "https://miami-plumbing-zip.surge.sh",                                      "local_biz"),
    ("PrintMaxx Local Demos",       "https://printmaxx-local-demos.surge.sh",                                   "local_biz"),
    # Demos
    ("Restaurant Motion",    "https://restaurant-motion.surge.sh",    "demos"),
    ("Realtor Motion",       "https://realtor-motion.surge.sh",       "demos"),
    ("Dental Motion",        "https://dental-motion.surge.sh",        "demos"),
    ("Restaurant Site Demo", "https://restaurant-site-demo.surge.sh", "demos"),
    ("Realtor Demo",         "https://realtor-demo.surge.sh",         "demos"),
    ("Plumber Demo",         "https://plumber-demo.surge.sh",         "demos"),
    ("Legal Demo",           "https://legal-demo.surge.sh",           "demos"),
    ("Fitness Demo",         "https://fitness-demo.surge.sh",         "demos"),
    ("Dental Demo",          "https://dental-demo.surge.sh",          "demos"),
    ("FlowStack Demo",       "https://flowstack-demo.surge.sh",       "demos"),
    ("ShopMetrics Dashboard","https://shopmetrics-dashboard.surge.sh","demos"),
    ("PrintMaxx Demos",      "https://printmaxx-demos.surge.sh",     "demos"),
    ("Mike's HVAC Demo",     "https://mikes-hvac-demo.surge.sh",      "demos"),
    ("Elite Fitness Demo",   "https://elite-fitness-demo.surge.sh",   "demos"),
    ("Smith Dentistry Demo", "https://smith-dentistry-demo.surge.sh", "demos"),
    ("Perfect Lawn Demo",    "https://perfect-lawn-demo.surge.sh",    "demos"),
    ("Bella's Salon Demo",   "https://bellas-salon-demo.surge.sh",    "demos"),
    ("Tony's Restaurant Demo","https://tonys-restaurant-demo.surge.sh","demos"),
    ("Joe's Plumbing Demo",  "https://joes-plumbing-demo.surge.sh",  "demos"),
    # ── New deployments (added this cycle) ─────────────────────────────────────
    # Main hub + hubs
    ("PrintMaxx Main",          "https://printmaxx.surge.sh",                  "hubs"),
    ("PrintMaxx Site",          "https://printmaxx-site.surge.sh",             "hubs"),
    ("PrintMaxx Control Panel", "https://printmaxx-control-panel.surge.sh",    "hubs"),
    ("PrintMaxx Thanks",        "https://printmaxx-thanks.surge.sh",           "hubs"),
    ("PrintMaxx Magnets",       "https://printmaxx-magnets.surge.sh",          "lead_magnets"),
    ("PrintMaxx Storefront",    "https://printmaxx-storefront.surge.sh",       "hubs"),
    # Comparison pages
    ("ConvertKit vs Beehiiv",   "https://convertkit-vs-beehiiv.surge.sh",      "comparison_pages"),
    ("PrayerLock vs Hallow",    "https://prayerlock-vs-hallow.surge.sh",       "comparison_pages"),
    ("FocusLock vs Opal",       "https://focuslock-vs-opal.surge.sh",          "comparison_pages"),
    ("PrintMaxx Comparisons",   "https://printmaxx-comparisons.surge.sh",      "comparison_pages"),
    # Tools
    ("Website Analyzer PM",     "https://website-analyzer-pm.surge.sh",        "tools_saas"),
    # Lead magnets
    ("ADHD Streak Landing",     "https://adhd-streak.surge.sh",                "streak_landing"),
    ("Solopreneur Checklist",   "https://solopreneur-launch-checklist.surge.sh","lead_magnets"),
    ("Ramadan Daily Planner",   "https://ramadan-daily-planner.surge.sh",      "lead_magnets"),
    ("Hilal Ramadan App",       "https://hilal.surge.sh",                      "apps"),
    # New streak landing variants
    ("Fitness Streak Landing2", "https://fitness-streak-landing.surge.sh",     "streak_landing"),
    ("Coding Streak Landing2",  "https://coding-streak-landing.surge.sh",      "streak_landing"),
    ("Buddhist Streak Landing2","https://buddhist-streak-landing.surge.sh",    "streak_landing"),
    ("Art Streak Landing2",     "https://art-streak-landing.surge.sh",         "streak_landing"),
    # Religious denomination streaks
    ("Sunni Streak",            "https://sunni-streak.surge.sh",               "streak_landing"),
    ("Shia Streak",             "https://shia-streak.surge.sh",                "streak_landing"),
    ("Presbyterian Streak",     "https://presbyterian-streak.surge.sh",        "streak_landing"),
    ("Anglican Streak",         "https://anglican-streak.surge.sh",            "streak_landing"),
    ("Evangelical Streak",      "https://evangelical-streak.surge.sh",         "streak_landing"),
    ("Pentecostal Streak",      "https://pentecostal-streak.surge.sh",         "streak_landing"),
    ("Episcopal Streak",        "https://episcopal-streak.surge.sh",           "streak_landing"),
    ("Lutheran Streak",         "https://lutheran-streak.surge.sh",            "streak_landing"),
    ("Methodist Streak",        "https://methodist-streak.surge.sh",           "streak_landing"),
    ("Baptist Streak",          "https://baptist-streak.surge.sh",             "streak_landing"),
    ("Protestant Streak",       "https://protestant-streak.surge.sh",          "streak_landing"),
    ("Orthodox Streak",         "https://orthodox-streak.surge.sh",            "streak_landing"),
    ("Catholic Streak",         "https://catholic-streak.surge.sh",            "streak_landing"),
    # Austin local biz
    ("Magnolia Cafe Austin",    "https://magnolia-cafe-austin.surge.sh",       "local_biz"),
    ("Kelly Personal Training", "https://kelly-personal-training-austin.surge.sh","local_biz"),
    ("Galaxia Dental Austin",   "https://galaxia-dental-austin.surge.sh",      "local_biz"),
    ("Barton Springs Saloon",   "https://barton-springs-saloon-austin.surge.sh","local_biz"),
    ("Zax Pints Plates Austin", "https://zax-pints-plates-austin.surge.sh",    "local_biz"),
    ("Artz Rib House Austin",   "https://artz-rib-house-austin.surge.sh",      "local_biz"),
    # Preview sites
    ("Memphis Plumbing Preview","https://memphis-plumbing-preview.surge.sh",   "local_biz"),
    ("JAX Emergency Plumber",   "https://jax-emergency-plumber-preview.surge.sh","local_biz"),
    ("S Tampa Locksmith Preview","https://south-tampa-locksmith-preview.surge.sh","local_biz"),
    ("Atlanta Roofing Preview", "https://atlanta-roofing-company-preview.surge.sh","local_biz"),
    # New local biz
    ("JSS Janitorial Memphis",  "https://jss-janitorial-memphis.surge.sh",     "local_biz"),
    ("Shop of Memphis Preview", "https://shop-of-memphis-preview.surge.sh",    "local_biz"),
]

# Deduplicate by URL
_seen: set[str] = set()
SITES: list[tuple[str, str, str]] = []
for entry in ALL_SITES:
    if entry[1] not in _seen:
        _seen.add(entry[1])
        SITES.append(entry)


def _slug(url: str) -> str:
    return re.sub(r"[^\w]", "_", url.replace("https://", "").rstrip("/"))[:80]


async def test_site(sem: asyncio.Semaphore, browser, name: str, url: str, category: str) -> dict:
    async with sem:
        result: dict = {
            "name": name, "url": url, "category": category,
            "status": None, "load_time_ms": None, "title": "",
            "has_content": False, "console_errors": [],
            "screenshot": None, "grade": "RED", "notes": [],
        }
        ctx  = await browser.new_context(
            viewport={"width": 1280, "height": 800},
            user_agent=(
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/122.0.0.0 Safari/537.36"
            )
        )
        page = await ctx.new_page()
        errs: list[str] = []
        page.on("console", lambda m: errs.append(m.text) if m.type == "error" else None)

        try:
            t0       = time.monotonic()
            resp     = await page.goto(url, wait_until="domcontentloaded", timeout=TIMEOUT_MS)
            load_ms  = int((time.monotonic() - t0) * 1000)

            result["status"]       = resp.status if resp else 0
            result["load_time_ms"] = load_ms
            result["title"]        = (await page.title()) or ""
            result["console_errors"] = errs[:5]

            body = await page.evaluate("document.body ? document.body.innerText.trim() : ''")
            result["has_content"] = len(body) > 50

            shot_path = str(SCREENSHOTS_DIR / f"{_slug(url)}.png")
            await page.screenshot(path=shot_path, full_page=False)
            result["screenshot"] = shot_path

            ok = result["status"] == 200
            if ok and result["has_content"]:
                if load_ms > 5000:
                    result["grade"] = "YELLOW"
                    result["notes"].append(f"slow: {load_ms}ms")
                elif errs:
                    result["grade"] = "YELLOW"
                    result["notes"].append(f"{len(errs)} console error(s)")
                else:
                    result["grade"] = "GREEN"
            elif ok:
                result["grade"] = "YELLOW"
                result["notes"].append("200 OK but page blank/empty")
            else:
                result["notes"].append(f"HTTP {result['status']}")

        except PlaywrightTimeout:
            result["notes"].append("timeout >15s")
        except Exception as exc:
            result["notes"].append(str(exc)[:120])
        finally:
            await ctx.close()

        icon = {"GREEN": "✓", "YELLOW": "~", "RED": "✗"}.get(result["grade"], "?")
        notes_str = " | " + ", ".join(result["notes"]) if result["notes"] else ""
        print(f"  [{icon}] {result['grade']:6}  {str(result['load_time_ms'] or '?'):>5}ms  {name}{notes_str}")
        return result


async def run_all() -> list[dict]:
    sem = asyncio.Semaphore(CONCURRENCY)
    async with async_playwright() as pw:
        browser = await pw.chromium.launch(headless=True)
        tasks   = [test_site(sem, browser, name, url, cat) for name, url, cat in SITES]
        results = await asyncio.gather(*tasks)
        await browser.close()
    return list(results)


def write_report(results: list[dict]) -> None:
    green  = [r for r in results if r["grade"] == "GREEN"]
    yellow = [r for r in results if r["grade"] == "YELLOW"]
    red    = [r for r in results if r["grade"] == "RED"]

    avg_load = int(sum(r["load_time_ms"] for r in results if r["load_time_ms"]) /
                   max(len([r for r in results if r["load_time_ms"]]), 1))
    pass_pct = f"{len(green)/len(results)*100:.1f}%" if results else "0%"

    lines = [
        f"# PRINTMAXX Site Test Report — {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "",
        "## Summary",
        "",
        "| Metric | Value |",
        "|--------|-------|",
        f"| Total sites | {len(results)} |",
        f"| GREEN (passing) | {len(green)} |",
        f"| YELLOW (warnings) | {len(yellow)} |",
        f"| RED (broken) | {len(red)} |",
        f"| Pass rate | {pass_pct} |",
        f"| Avg load time | {avg_load}ms |",
        "",
    ]

    if red:
        lines += ["## RED — Broken Sites (Fix Immediately)", ""]
        for r in red:
            lines += [
                f"### {r['name']}",
                f"- **URL:** {r['url']}",
                f"- **HTTP:** {r['status']}",
                f"- **Issues:** {' | '.join(r['notes'])}",
                "",
            ]

    if yellow:
        lines += ["## YELLOW — Sites with Warnings", ""]
        for r in yellow:
            lines += [
                f"### {r['name']}",
                f"- **URL:** {r['url']}",
                f"- **HTTP:** {r['status']} | Load: {r['load_time_ms']}ms",
                f"- **Warnings:** {' | '.join(r['notes'])}",
                "",
            ]

    lines += ["## GREEN — All Passing", "",
              "| Site | URL | Load ms | Title |",
              "|------|-----|---------|-------|"]
    for r in green:
        lines.append(f"| {r['name']} | {r['url']} | {r['load_time_ms']} | {r['title'][:40]} |")

    lines += [
        "",
        "## Full Results",
        "",
        "| # | Site | Category | Grade | HTTP | Load ms | Notes |",
        "|---|------|----------|-------|------|---------|-------|",
    ]
    for i, r in enumerate(results, 1):
        badge = {"GREEN": "GREEN", "YELLOW": "YELLOW", "RED": "RED"}.get(r["grade"], r["grade"])
        notes = "; ".join(r["notes"])[:70] if r["notes"] else ""
        lines.append(
            f"| {i} | {r['name']} | {r['category']} | {badge} | "
            f"{r['status']} | {r['load_time_ms']} | {notes} |"
        )

    lines += [
        "",
        f"*Generated: {datetime.now().isoformat()}*",
        "*Screenshots: AUTOMATIONS/agent/swarm/screenshots/*",
    ]

    REPORT_PATH.write_text("\n".join(lines))
    print(f"\n  Report  → {REPORT_PATH}")


def write_alerts(results: list[dict]) -> None:
    red = [r for r in results if r["grade"] == "RED"]
    if not red:
        return
    ts = datetime.now().strftime("%Y-%m-%d %H:%M")
    lines = [f"\n[{ts}] PLAYWRIGHT ALERT — {len(red)} RED site(s):"]
    for r in red:
        lines.append(f"  ✗ {r['name']} | {r['url']} | {' | '.join(r['notes'])}")
    with open(ALERTS_PATH, "a") as f:
        f.write("\n".join(lines) + "\n")
    print(f"  Alerts  → {ALERTS_PATH}")


def update_deployed_assets(results: list[dict]) -> None:
    try:
        data = json.loads(DEPLOYED_ASSETS.read_text())
        data["last_updated"] = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        data["live_test"] = {
            "tested_at": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
            "total":  len(results),
            "green":  len([r for r in results if r["grade"] == "GREEN"]),
            "yellow": len([r for r in results if r["grade"] == "YELLOW"]),
            "red":    len([r for r in results if r["grade"] == "RED"]),
        }
        DEPLOYED_ASSETS.write_text(json.dumps(data, indent=2))
        print(f"  Assets  → {DEPLOYED_ASSETS} updated")
    except Exception as e:
        print(f"  [warn] deployed_assets.json not updated: {e}")


async def main() -> int:
    print(f"\nPRINTMAXX Playwright Tester — {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Testing {len(SITES)} sites | concurrency={CONCURRENCY} | timeout={TIMEOUT_MS}ms\n")

    results = await run_all()

    green  = [r for r in results if r["grade"] == "GREEN"]
    yellow = [r for r in results if r["grade"] == "YELLOW"]
    red    = [r for r in results if r["grade"] == "RED"]

    print(f"\n{'─'*60}")
    print(f"  GREEN:  {len(green)}/{len(results)}")
    print(f"  YELLOW: {len(yellow)}/{len(results)}")
    print(f"  RED:    {len(red)}/{len(results)}")

    write_report(results)
    write_alerts(results)
    update_deployed_assets(results)

    return 0 if not red else 1


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
