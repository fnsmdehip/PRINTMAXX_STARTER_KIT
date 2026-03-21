#!/usr/bin/env python3

from __future__ import annotations
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

# ── Dynamic site list: loads from deployed_assets.json + hardcoded extras ──────
def _load_sites_from_json() -> list[tuple[str, str, str]]:
    """Load all URLs from deployed_assets.json."""
    sites = []
    try:
        data = json.loads(DEPLOYED_ASSETS.read_text())
        deployments = data.get("deployments", {})
        for category, items in deployments.items():
            if isinstance(items, list):
                for item in items:
                    url = item.get("url", "")
                    name = item.get("name", item.get("title", url))
                    if url:
                        sites.append((name, url, category))
    except Exception as e:
        print(f"  [warn] Could not load deployed_assets.json: {e}")
    return sites

# Extra sites from surge list not yet in deployed_assets.json
EXTRA_SITES = [
    # New cycle 15+ deployments
    ("SmartLead vs Instantly",  "https://smartlead-vs-instantly.surge.sh",  "comparison_pages"),
    ("Best AI Tools 2026",     "https://best-ai-tools-2026.surge.sh",      "comparison_pages"),
    ("SaaS Stack Audit",       "https://saas-stack-audit.surge.sh",        "tools_saas"),
    ("CoreDay",                "https://coreday.surge.sh",                  "apps"),
    # Fiverr service pages
    ("PM Website Design",      "https://printmaxx-website-design.surge.sh", "fiverr_services"),
    ("PM Landing Page",        "https://printmaxx-landing-page.surge.sh",   "fiverr_services"),
    ("PM Cold Email",          "https://printmaxx-cold-email.surge.sh",     "fiverr_services"),
    ("PM Web Scraping",        "https://printmaxx-web-scraping.surge.sh",   "fiverr_services"),
    ("PM Automation",          "https://printmaxx-automation.surge.sh",     "fiverr_services"),
    ("PM SEO Pages",           "https://printmaxx-seo-pages.surge.sh",     "fiverr_services"),
    ("PM Content Writing",     "https://printmaxx-content-writing.surge.sh","fiverr_services"),
    ("PM App Development",     "https://printmaxx-app-development.surge.sh","fiverr_services"),
    ("PM AI Chatbot",          "https://printmaxx-ai-chatbot.surge.sh",    "fiverr_services"),
    ("PM Data Analysis",       "https://printmaxx-data-analysis.surge.sh", "fiverr_services"),
    # Louisville KY local biz (35 sites)
    ("Coit Cleaning Louisville",    "https://coit-cleaning-restoration-louisville-ky.surge.sh",  "local_biz_louisville"),
    ("Whitehouse Painting Louisville","https://whitehouse-residential-commercial-painting-co-llc-louisville-ky.surge.sh","local_biz_louisville"),
    ("A1 Concrete Louisville",      "https://a-1-concrete-leveling-louisville-louisville-ky.surge.sh","local_biz_louisville"),
    ("Down To Earth Sealcoating",   "https://down-to-earth-sealcoating-inc-louisville-ky.surge.sh","local_biz_louisville"),
    ("CertaPro Painters Louisville","https://certapro-painters-of-louisville-metro-louisville-ky.surge.sh","local_biz_louisville"),
    ("Skyrockett Construction",     "https://skyrockett-construction-renovation-llc-louisville-ky.surge.sh","local_biz_louisville"),
    ("Garretts Pressure Washing",   "https://garrett-s-presure-washing-louisville-ky.surge.sh","local_biz_louisville"),
    ("Good Maintenance Cleaning",   "https://good-maintenance-cleaning-inc-louisville-ky.surge.sh","local_biz_louisville"),
    ("A1 Aluminum Louisville",      "https://a-1-aluminum-inc-louisville-ky.surge.sh","local_biz_louisville"),
    ("The Maids Louisville",        "https://the-maids-in-southern-louisville-llc-louisville-ky.surge.sh","local_biz_louisville"),
    ("McCoy Window Cleaning",       "https://mccoy-window-gutter-cleaning-llc-louisville-ky.surge.sh","local_biz_louisville"),
    ("Square It Away Contracting",  "https://square-it-away-contracting-llc-louisville-ky.surge.sh","local_biz_louisville"),
    ("Spindletop Draperies",        "https://spindletop-draperies-inc-louisville-ky.surge.sh","local_biz_louisville"),
    ("Naturescape Louisville",      "https://naturescape-louisville-ky.surge.sh","local_biz_louisville"),
    ("Cutting Hedge Landscaping",   "https://the-cutting-hedge-landscaping-mowing-louisville-ky.surge.sh","local_biz_louisville"),
    ("Greenworks Lawn Louisville",  "https://greenworks-lawn-landscape-tree-llc-louisville-ky.surge.sh","local_biz_louisville"),
    ("Accurate Lawn Louisville",    "https://accurate-lawn-landscaping-inc-louisville-ky.surge.sh","local_biz_louisville"),
    ("Daves Tree Surgeons",         "https://dave-s-tree-surgeons-inc-louisville-ky.surge.sh","local_biz_louisville"),
    ("Bob Ray Company",             "https://bob-ray-company-inc-louisville-ky.surge.sh","local_biz_louisville"),
    ("AB Landscaping Louisville",   "https://a-b-landscaping-inc-louisville-ky.surge.sh","local_biz_louisville"),
    ("ER Tree Care Louisville",     "https://er-tree-care-llc-louisville-ky.surge.sh","local_biz_louisville"),
    ("Climb Ax Tree Service",       "https://climb-ax-tree-crane-service-louisville-ky.surge.sh","local_biz_louisville"),
    ("Bright Hauling Louisville",   "https://bright-hauling-and-junk-removal-llc-louisville-ky.surge.sh","local_biz_louisville"),
    ("Mr Fix It Louisville",        "https://mr-fix-it-solutions-llc-louisville-ky.surge.sh","local_biz_louisville"),
    ("Complete Home Services",      "https://complete-home-services-louisville-ky.surge.sh","local_biz_louisville"),
    ("Wildcat Moving Louisville",   "https://wildcat-moving-llc-louisville-ky.surge.sh","local_biz_louisville"),
    ("Right Way Hauling Louisville","https://right-way-hauling-junk-removal-demolition-louisville-ky.surge.sh","local_biz_louisville"),
    ("JD Contractors Louisville",   "https://jd-contractors-and-lawnscaping-llc-louisville-ky.surge.sh","local_biz_louisville"),
    ("New Seasons Auction",         "https://new-seasons-auction-and-estates-louisville-ky.surge.sh","local_biz_louisville"),
    ("Kings Hands LLC",             "https://kings-hands-llc-louisville-ky.surge.sh","local_biz_louisville"),
    ("New Leaf Tree Service",       "https://new-leaf-tree-service-llc-louisville-ky.surge.sh","local_biz_louisville"),
    ("Jeff Reed Logging",           "https://jeff-reed-logging-tree-service-louisville-ky.surge.sh","local_biz_louisville"),
    ("Junk King Louisville",        "https://junk-king-louisville-louisville-ky.surge.sh","local_biz_louisville"),
    ("David Fox Roofer",            "https://david-fox-roofer-louisville-ky.surge.sh","local_biz_louisville"),
    # Las Vegas / Orlando local biz
    ("Handyman Las Vegas",          "https://handyman-services-in-las-vegas-nv-89121-las-vegas-nv.surge.sh","local_biz_other"),
    ("Auto Repair Orlando",         "https://top-rated-auto-repair-near-orlando-fl-carfax-orlando-fl.surge.sh","local_biz_other"),
    ("OKC Mobile Detailing",        "https://mobile-auto-detailing-experts-in-oklahoma-city-champion-deta-oklahoma-city-ok.surge.sh","local_biz_other"),
    ("OKC Car Detailing",           "https://top-rated-mobile-car-detailing-in-oklahoma-city-ok-pure-prof-oklahoma-city-ok.surge.sh","local_biz_other"),
    ("Portland Window Cleaning",    "https://window-cleaning-in-portland-or-all-pro-metro-services-llc-portland-or.surge.sh","local_biz_other"),
    # Streak landing page variants
    ("Sunni Streak Landing",       "https://sunni-streak-landing.surge.sh",      "streak_landing"),
    ("Shia Streak Landing",        "https://shia-streak-landing.surge.sh",       "streak_landing"),
    ("Presbyterian Streak Landing","https://presbyterian-streak-landing.surge.sh","streak_landing"),
    ("Anglican Streak Landing",    "https://anglican-streak-landing.surge.sh",   "streak_landing"),
    ("Evangelical Streak Landing", "https://evangelical-streak-landing.surge.sh","streak_landing"),
    ("Pentecostal Streak Landing", "https://pentecostal-streak-landing.surge.sh","streak_landing"),
    ("Episcopal Streak Landing",   "https://episcopal-streak-landing.surge.sh",  "streak_landing"),
    ("Lutheran Streak Landing",    "https://lutheran-streak-landing.surge.sh",   "streak_landing"),
    ("Methodist Streak Landing",   "https://methodist-streak-landing.surge.sh",  "streak_landing"),
    ("Baptist Streak Landing",     "https://baptist-streak-landing.surge.sh",    "streak_landing"),
    ("Protestant Streak Landing",  "https://protestant-streak-landing.surge.sh", "streak_landing"),
    ("Orthodox Streak Landing",    "https://orthodox-streak-landing.surge.sh",   "streak_landing"),
    ("Catholic Streak Landing",    "https://catholic-streak-landing.surge.sh",   "streak_landing"),
    # Lead magnets
    ("Cold Email ROI Calculator",  "https://cold-email-roi-calculator.surge.sh", "lead_magnets"),
    ("Side Project Estimator",     "https://side-project-estimator.surge.sh",    "lead_magnets"),
    ("Revenue Leak Audit",         "https://revenue-leak-audit.surge.sh",        "lead_magnets"),
    ("PrintMaxx Lead Magnets Hub", "https://printmaxx-lead-magnets.surge.sh",    "lead_magnets"),
    # Instantly vs Lemlist
    ("Instantly vs Lemlist",       "https://instantly-vs-lemlist.surge.sh",       "comparison_pages"),
    ("Cursor vs Claude Code",     "https://cursor-vs-claudecode.surge.sh",       "comparison_pages"),
    ("ColdMaxx vs Instantly",     "https://coldmaxx-vs-instantly.surge.sh",      "comparison_pages"),
    ("PageScorer vs GTmetrix",    "https://pagescorer-vs-gtmetrix.surge.sh",     "comparison_pages"),
    ("SleepMaxx vs Sleep Cycle",  "https://sleepmaxx-vs-sleepcycle.surge.sh",    "comparison_pages"),
    # Test deploys
    ("Test Deploy 001",            "https://printmaxx-test-debug-deploy-001.surge.sh","test_deploys"),
    ("Nested Test 001",            "https://printmaxx-nested-test-001.surge.sh",      "test_deploys"),
    ("OpenClaw Fix Test 001",      "https://printmaxx-openclaw-fix-test-001.surge.sh","test_deploys"),
    # Media templates
    ("Twitter Banner",             "https://printmaxx-twitter-banner.surge.sh",  "media"),
    ("Twitter PFP",                "https://printmaxx-twitter-pfp.surge.sh",     "media"),
    # Cold email deliverability
    ("Cold Email Deliverability",  "https://best-cold-email-tools.surge.sh",     "lead_magnets"),
    # ATX new cycle 15
    ("ATX Food Co Austin",         "https://atx-food-co-austin.surge.sh",        "local_biz"),
    ("Dailey Company Inc Austin",  "https://dailey-company-inc-austin.surge.sh", "local_biz"),
    # Cycle 16+ new deployments (Mar 14-15 2026)
    ("Semrush vs Ahrefs",          "https://semrush-vs-ahrefs.surge.sh",         "comparison_pages"),
    ("PDFMaxx",                    "https://pdfmaxx.surge.sh",                   "tools_saas"),
    ("ConvertKit vs Beehiiv",      "https://convertkit-vs-beehiiv.surge.sh",     "comparison_pages"),
    ("SaaS Stack Audit 200",       "https://saas-stack-audit-200.surge.sh",      "tools_saas"),
    ("Vibe Coding Profit Calc",    "https://vibe-coding-profit-calculator.surge.sh","lead_magnets"),
    # Milwaukee local biz
    ("Apps Chiropractic Milwaukee","https://apps-chiropractic-milwaukee-wi.surge.sh","local_biz_milwaukee"),
    ("Pope Family Chiro MKE",     "https://pope-family-chiropractic-milwaukee-wi.surge.sh","local_biz_milwaukee"),
    ("Carlitos Lawns MKE",        "https://carlitos-lawns-llc-milwaukee-wi.surge.sh","local_biz_milwaukee"),
    ("S Milwaukee Car Care",      "https://south-milwaukee-car-care-center-milwaukee-wi.surge.sh","local_biz_milwaukee"),
    ("Gians Flooring MKE",        "https://gians-flooring-mke.surge.sh",         "local_biz_milwaukee"),
    ("Landlords Pest MKE",        "https://a-landlords-pest-mke.surge.sh",       "local_biz_milwaukee"),
    ("Shorewood Family Chiro",    "https://shorewood-family-chiro-mke.surge.sh", "local_biz_milwaukee"),
    ("Milwaukee Plumber Service",  "https://milwaukee-plumber-service-mke.surge.sh","local_biz_milwaukee"),
    ("PM Local Demos",             "https://printmaxx-local-demos.surge.sh",     "fiverr_services"),
    ("PM Services",                "https://printmaxx-services.surge.sh",        "fiverr_services"),
    # Marketing landing pages for streaks
    ("Sunni Streak Marketing",     "https://sunni-streak-marketing.surge.sh",    "streak_marketing"),
    ("Shia Streak Marketing",      "https://shia-streak-marketing.surge.sh",     "streak_marketing"),
    ("Protestant Streak Marketing","https://protestant-streak-marketing.surge.sh","streak_marketing"),
    ("Presbyterian Streak Mkt",    "https://presbyterian-streak-marketing.surge.sh","streak_marketing"),
    ("Pentecostal Streak Mkt",     "https://pentecostal-streak-marketing.surge.sh","streak_marketing"),
    ("Orthodox Streak Marketing",  "https://orthodox-streak-marketing.surge.sh", "streak_marketing"),
    ("Methodist Streak Marketing", "https://methodist-streak-marketing.surge.sh","streak_marketing"),
    ("Lutheran Streak Marketing",  "https://lutheran-streak-marketing.surge.sh", "streak_marketing"),
    ("Evangelical Streak Mkt",     "https://evangelical-streak-marketing.surge.sh","streak_marketing"),
    ("Episcopal Streak Marketing", "https://episcopal-streak-marketing.surge.sh","streak_marketing"),
    ("Catholic Streak Marketing",  "https://catholic-streak-marketing.surge.sh", "streak_marketing"),
    ("Best Cold Email Tools Mkt",  "https://best-cold-email-tools-marketing.surge.sh","streak_marketing"),
    ("Baptist Streak Marketing",   "https://baptist-streak-marketing.surge.sh",  "streak_marketing"),
    ("Anglican Streak Marketing",  "https://anglican-streak-marketing.surge.sh", "streak_marketing"),
    # Additional lead magnets
    ("Cold Email Deliverability",  "https://cold-email-deliverability-checklist.surge.sh","lead_magnets"),
    ("Ramadan Daily Planner",      "https://ramadan-daily-planner.surge.sh",     "lead_magnets"),
    ("Solopreneur Launch Check",   "https://solopreneur-launch-checklist.surge.sh","lead_magnets"),
    ("Subject Line Grader",        "https://subject-line-grader.surge.sh",       "lead_magnets"),
    ("App Hub Crosslinks",         "https://app-hub-crosslinks.surge.sh",        "lead_magnets"),
    ("200 Day Calculator",         "https://200-day-calculator.surge.sh",        "lead_magnets"),
    ("AI Revenue Calculator",      "https://ai-revenue-calculator.surge.sh",     "lead_magnets"),
    # Portland & OKC detailed
    ("All Pro Window Portland",    "https://all-pro-window-cleaning-portland.surge.sh","local_biz_other"),
    ("Pure Pro Detailing OKC",     "https://pure-pro-detailing-okc.surge.sh",    "local_biz_other"),
    ("Champion Auto Detail OKC",   "https://champion-auto-detailing-okc.surge.sh","local_biz_other"),
    # Birmingham AL
    ("Birmingham Detailing",       "https://mobile-interior-detailing-birmingham-al-magic-city-detailing-birmingham-al.surge.sh","local_biz_other"),
    ("Birmingham Home Detailing",  "https://home-professional-mobile-detailing-amp-products-super-store-birmingham-al.surge.sh","local_biz_other"),
    ("Birmingham Handyman",        "https://handyman-and-home-modifications-in-birmingham-birmingham-al.surge.sh","local_biz_other"),
    # Las Vegas extended
    ("Homeguide Handyman LV",      "https://the-10-best-handyman-services-in-las-vegas-nv-2026-homeguide-las-vegas-nv.surge.sh","local_biz_other"),
    # Pink Windows Louisville
    ("Pink Windows Louisville",    "https://local-window-cleaning-in-louisville-pink-x27-s-windows-louisville-ky.surge.sh","local_biz_louisville"),
    ("Cherry Window Louisville",   "https://residential-and-commercial-window-cleaning-cherry-window-cle-louisville-ky.surge.sh","local_biz_louisville"),
    # Austin dentists
    ("Old Settlers Dental ATX",    "https://old-settlers-dental-p-a-austin-tx.surge.sh","local_biz_austin"),
    ("Vista Ridge Dentistry ATX",  "https://vista-ridge-family-dentistry-austin-tx.surge.sh","local_biz_austin"),
    ("Big Top Dentistry ATX",      "https://big-top-dentistry-for-kids-austin-tx.surge.sh","local_biz_austin"),
    ("Nursing Home Dental ATX",    "https://nursing-home-dental-care-austin-tx.surge.sh","local_biz_austin"),
    ("Austin Elite Smiles",        "https://austin-elite-smiles-pllc-austin-tx.surge.sh","local_biz_austin"),
    ("Lakeway Cosmetic Dent ATX",  "https://lakeway-cosmetic-dentistry-austin-tx.surge.sh","local_biz_austin"),
    ("Restora Dental Arts ATX",    "https://restora-dental-arts-austin-tx.surge.sh","local_biz_austin"),
    ("Helen Ragsdale DDS ATX",     "https://austin-laser-dentist-helen-ragsdale-dds-austin-tx.surge.sh","local_biz_austin"),
    ("About Smiles Dentistry",     "https://about-smiles-family-and-cosmetic-dentistry-austin-tx.surge.sh","local_biz_austin"),
    ("Dental Smiles ATX",          "https://dental-smiles-austin-tx.surge.sh",   "local_biz_austin"),
    ("Thiel Pediatric Dent ATX",   "https://thiel-pediatric-dentistry-austin-tx.surge.sh","local_biz_austin"),
    ("Smiles of Austin",           "https://leading-dentist-in-austin-tx-smiles-of-austin-austin-tx.surge.sh","local_biz_austin"),
    ("Vitadox Austin Dentists",    "https://dentists-in-austin-tx-vitadox-austin-tx.surge.sh","local_biz_austin"),
    ("Austin Dentistry",           "https://austin-dentistry-dentist-in-austin-tx-austin-tx.surge.sh","local_biz_austin"),
    # Miami dental
    ("Dental Blush Miami",        "https://dental-blush-associates-pa-miami-fl.surge.sh","local_biz_miami"),
    ("J Family Dental Miami",     "https://j-family-dental-llc-miami-fl.surge.sh","local_biz_miami"),
    # Dallas plumbing
    ("Hedricks Dallas",            "https://hedrick-s-service-now-dallas-tx.surge.sh","local_biz_dallas"),
    ("Berrett Home Dallas",        "https://berrett-home-services-dfw-dallas-tx.surge.sh","local_biz_dallas"),
    ("Cody Sons Plumbing Dallas",  "https://cody-sons-plumbing-heating-air-dallas-tx.surge.sh","local_biz_dallas"),
    ("Dial One Dallas",            "https://dial-one-plumbing-cooling-heating-dallas-tx.surge.sh","local_biz_dallas"),
    ("ARS Rescue Rooter Dallas",   "https://ars-rescue-rooter-dfw-dallas-tx.surge.sh","local_biz_dallas"),
    ("Harmony Plumbing Dallas",    "https://harmony-plumbing-and-drain-cleaning-dallas-tx.surge.sh","local_biz_dallas"),
    ("Public Service Plumber DAL", "https://public-service-plumbers-air-conditioning-llc-dallas-tx.surge.sh","local_biz_dallas"),
    ("Berkeys AC Plumbing Dallas", "https://berkeys-air-conditioning-plumbing-and-electrical-dallas-tx.surge.sh","local_biz_dallas"),
    ("Triune Plumbing Dallas",     "https://triune-plumbing-llc-dallas-tx.surge.sh","local_biz_dallas"),
    ("Accurate Leak Dallas",       "https://accurate-leak-and-line-dallas-tx.surge.sh","local_biz_dallas"),
    ("FindLaw Dallas",             "https://find-dallas-tx-attorneys-and-law-firms-findlaw-dallas-tx.surge.sh","local_biz_dallas"),
    # Miami plumbing (zip local)
    ("Miami Plumbing Zip Local",   "https://miami-plumbing-experts-zip-local.surge.sh","local_biz_miami"),
]

ALL_SITES = _load_sites_from_json() + EXTRA_SITES

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
        g = len([r for r in results if r["grade"] == "GREEN"])
        y = len([r for r in results if r["grade"] == "YELLOW"])
        r_count = len([r for r in results if r["grade"] == "RED"])
        total = len(results)
        loads = [r["load_time_ms"] for r in results if r.get("load_time_ms") and r["load_time_ms"] > 0]
        avg_load = int(sum(loads) / len(loads)) if loads else 0
        pass_pct = f"{(g + y) / total * 100:.1f}%" if total > 0 else "0%"
        red_sites = [r["url"] for r in results if r["grade"] == "RED"]
        data["live_test"] = {
            "tested_at": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
            "total": total,
            "green": g,
            "yellow": y,
            "red": r_count,
            "pass_rate": pass_pct,
            "avg_load_ms": avg_load,
            "playwright_visual_tested": total,
            "notes": f"Cycle 16 (Playwright Tester): Full async test of {total} sites. {g} GREEN, {y} YELLOW, {r_count} RED.",
            "still_broken": red_sites[:10],
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
