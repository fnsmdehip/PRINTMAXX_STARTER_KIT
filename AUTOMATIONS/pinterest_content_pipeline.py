#!/usr/bin/env python3

from __future__ import annotations
"""
Pinterest Content Pipeline — fills C08/N44 gap
Generates pin content from existing PRINTMAXX assets for compound affiliate traffic.
Pins have 6-12 month shelf life. 50-100 pins/day at scale.

Usage:
    python3 pinterest_content_pipeline.py --generate       # Generate pin batch
    python3 pinterest_content_pipeline.py --status         # Show pipeline status
    python3 pinterest_content_pipeline.py --export-csv     # Export to Tailwind CSV

Cron: 0 9 * * * cd $BASE && $PYTHON AUTOMATIONS/pinterest_content_pipeline.py --generate >> AUTOMATIONS/logs/pinterest.log 2>&1
"""

import json
import csv
import os
import sys
from pathlib import Path
from datetime import datetime, timedelta
import hashlib

PROJECT_ROOT = Path(__file__).resolve().parent.parent
PINS_DIR = PROJECT_ROOT / "CONTENT" / "social" / "pinterest"
PINS_DIR.mkdir(parents=True, exist_ok=True)
QUEUE_FILE = PINS_DIR / "pin_queue.json"
EXPORT_FILE = PINS_DIR / "tailwind_upload.csv"
STATS_FILE = PINS_DIR / "pipeline_stats.json"

# Pin templates keyed by niche — each maps to existing PRINTMAXX assets
PIN_TEMPLATES = {
    "productivity_apps": {
        "boards": ["Productivity Apps", "Study Tips", "Focus Tools", "Best Free Apps 2026"],
        "pins": [
            {
                "title": "Free Pomodoro Timer That Actually Works (No Signup)",
                "description": "Built a free pomodoro timer with ambient sounds, session tracking, and streak heatmaps. runs in your browser, works offline, no account needed. saves your data locally.\n\n#pomodoro #studytimer #focusapp #productivity #freapps",
                "link": "https://focuslock-web.surge.sh",
                "image_spec": "1000x1500 vertical. Dark glassmorphism background. Timer display showing 25:00. Streak heatmap preview. Text overlay: 'Free Pomodoro Timer'",
                "category": "APP",
                "affiliate_potential": False,
            },
            {
                "title": "Free Habit Tracker with GitHub-Style Heatmap",
                "description": "track habits with a github-style contribution heatmap. 5 categories, milestone celebrations, streak tracking. zero cost, no signup, works offline.\n\n#habittracker #streaks #productivity #selfimprovement #freeapp",
                "link": "https://habitforge-web.surge.sh",
                "image_spec": "1000x1500 vertical. Dark theme. Green heatmap grid. Streak counter. Text: 'Track Every Habit Free'",
                "category": "APP",
                "affiliate_potential": False,
            },
            {
                "title": "Best Free Sleep Tracker App (No Subscription)",
                "description": "sleep tracker with heatmap visualization, bedtime routine builder, and sleep score calculator. works offline, saves locally, zero monthly fees.\n\n#sleeptracker #sleeptips #healthyhabits #wellness #freapps",
                "link": "https://sleepmaxx-web.surge.sh",
                "image_spec": "1000x1500 vertical. Dark blue theme. Moon icon. Sleep score ring. Heatmap. Text: 'Track Your Sleep Free'",
                "category": "APP",
                "affiliate_potential": False,
            },
            {
                "title": "Free Meal Planner with Macro Tracking",
                "description": "weekly meal planner with macro rings, water tracker, and auto grocery list. no subscription, no account, works on your phone.\n\n#mealplanner #mealprep #macros #healthyeating #freeapp",
                "link": "https://mealmaxx-web.surge.sh",
                "image_spec": "1000x1500 vertical. Clean dark theme. Macro rings (protein/carbs/fat/cal). Weekly grid. Text: 'Plan Every Meal Free'",
                "category": "APP",
                "affiliate_potential": False,
            },
        ],
    },
    "invoice_tools": {
        "boards": ["Small Business Tools", "Freelancer Tips", "Invoice Templates", "Plumber Business Tips"],
        "pins": [
            {
                "title": "Free Invoice Generator for Plumbers (No Signup)",
                "description": "built a free invoice generator with plumbing-specific templates. service call + hourly labor + parts breakdown. auto tax calc, PDF export, stripe payment links. your data never leaves your device.\n\n#plumber #invoicing #smallbusiness #freelancer #fretools",
                "link": "https://invoiceforge.surge.sh",
                "image_spec": "1000x1500 vertical. Dark theme. Invoice preview. Plumber wrench icon. Text: 'Free Plumber Invoice Template'",
                "category": "APP",
                "affiliate_potential": False,
            },
            {
                "title": "Free Invoice Generator for Electricians",
                "description": "invoice generator with electrical work templates. diagnostic fee + labor + wiring/components with auto tax calc. PDF export, works offline, zero monthly fees.\n\n#electrician #invoicetemplate #smallbusiness #contractor #freetools",
                "link": "https://invoiceforge.surge.sh",
                "image_spec": "1000x1500 vertical. Dark theme. Invoice preview. Lightning bolt icon. Text: 'Free Electrician Invoice Template'",
                "category": "APP",
                "affiliate_potential": False,
            },
            {
                "title": "Free HVAC Invoice Template Generator",
                "description": "free invoice generator with HVAC-specific template. system diagnostic + tech labor + refrigerant/parts. auto tax calculation, PDF export. no quickbooks, no subscription.\n\n#hvac #invoicing #contractor #smallbusiness #freetools",
                "link": "https://invoiceforge.surge.sh",
                "image_spec": "1000x1500 vertical. Dark theme. Invoice preview. HVAC/snowflake icon. Text: 'Free HVAC Invoice Template'",
                "category": "APP",
                "affiliate_potential": False,
            },
        ],
    },
    "business_tools": {
        "boards": ["Business Tools", "Startup Tools", "Cold Email Tips", "Website Building"],
        "pins": [
            {
                "title": "Free Website Audit Tool (Check Any Site in 30 Seconds)",
                "description": "paste any URL, get a full audit in 30 seconds. checks mobile responsiveness, load speed, SEO basics, SSL, meta tags. completely free, no account.\n\n#websiteaudit #seo #webdesign #smallbusiness #freetools",
                "link": "https://website-audit.surge.sh",
                "image_spec": "1000x1500 vertical. Dark theme. Audit score display. Green/yellow/red indicators. Text: 'Audit Any Website Free'",
                "category": "APP",
                "affiliate_potential": False,
            },
            {
                "title": "Free ROI Calculator for Marketing Campaigns",
                "description": "calculate ROI on any marketing spend. supports multiple campaigns, ad channels, time periods. export results. no signup required.\n\n#roi #marketing #digitalmarketing #smallbusiness #analytics",
                "link": "https://roicalc.surge.sh",
                "image_spec": "1000x1500 vertical. Dark theme. Calculator display. ROI percentage. Chart. Text: 'Calculate Marketing ROI Free'",
                "category": "APP",
                "affiliate_potential": False,
            },
            {
                "title": "Free PDF Toolkit (Merge, Split, Compress)",
                "description": "merge, split, compress PDFs. extract pages, convert formats. everything runs in your browser. no file upload to any server. completely private and free.\n\n#pdf #tools #productivity #freelancer #freetools",
                "link": "https://pdfmaxx.surge.sh",
                "image_spec": "1000x1500 vertical. Dark theme. PDF icon. Tool icons (merge/split/compress). Text: 'Free PDF Tools'",
                "category": "APP",
                "affiliate_potential": False,
            },
        ],
    },
    "cold_email_affiliate": {
        "boards": ["Cold Email Tips", "B2B Sales", "Lead Generation", "Email Marketing"],
        "pins": [
            {
                "title": "Best Cold Email Tools 2026 (Free + Paid Compared)",
                "description": "compared every cold email tool: Instantly ($30/mo unlimited), Smartlead ($39/mo), Lemlist ($59/mo). which one actually works? full comparison with real numbers.\n\n#coldemail #b2bsales #leadgen #emailmarketing #saas",
                "link": "https://best-cold-email-tools-marketing.surge.sh",
                "image_spec": "1000x1500 vertical. Comparison table graphic. Tool logos. Checkmarks. Text: 'Best Cold Email Tools 2026'",
                "category": "AFFILIATE",
                "affiliate_potential": True,
            },
            {
                "title": "Cold Email Template That Gets 5%+ Reply Rate",
                "description": "the 6-question cold email framework: what you do, who for, how, problem solved, proof, ROI. answer all 6 in under 100 words. tested on 500+ sends.\n\n#coldemail #sales #b2b #outreach #emailtemplate",
                "link": "https://coldmaxx.surge.sh",
                "image_spec": "1000x1500 vertical. Email template preview. 6 numbered questions. Reply rate stat. Text: '5%+ Reply Rate Template'",
                "category": "APP",
                "affiliate_potential": False,
            },
        ],
    },
    "faith_apps": {
        "boards": ["Prayer Apps", "Ramadan", "Islamic Apps", "Faith & Spirituality"],
        "pins": [
            {
                "title": "Free Ramadan Fasting Tracker (Bilingual EN/AR)",
                "description": "track your Ramadan fasts, prayer times, Quran progress, and dua collection. bilingual english/arabic with RTL support. works offline, saves locally.\n\n#ramadan #fasting #islamicapp #prayer #muslim",
                "link": "https://ramadan-tracker.surge.sh",
                "image_spec": "1000x1500 vertical. Dark green/gold theme. Crescent moon. Fasting timer. Arabic text sample. Text: 'Free Ramadan Tracker'",
                "category": "APP",
                "affiliate_potential": False,
            },
            {
                "title": "Free Prayer Lock Screen App (Focus on Salah)",
                "description": "lock your phone during prayer time. set prayer duration, track your prayer streak, beautiful islamic UI. zero data collection, works offline.\n\n#prayer #salah #islamicapp #muslim #focusapp",
                "link": "https://prayerlock-web.surge.sh",
                "image_spec": "1000x1500 vertical. Dark theme with islamic geometric pattern. Lock icon. Prayer time display. Text: 'Focus on Prayer'",
                "category": "APP",
                "affiliate_potential": False,
            },
        ],
    },
    "streak_apps": {
        "boards": ["Self Improvement", "Daily Habits", "Meditation", "Reading Goals"],
        "pins": [
            {
                "title": "Free Coding Streak Tracker (GitHub-Style)",
                "description": "track your daily coding habit with a github-style heatmap. set goals, track streaks, celebrate milestones. perfect for #100DaysOfCode.\n\n#coding #programming #100daysofcode #developer #habits",
                "link": "https://coding-streak-landing.surge.sh",
                "image_spec": "1000x1500 vertical. Dark theme. Green heatmap grid. Code brackets icon. Streak counter. Text: 'Track Your Coding Streak'",
                "category": "APP",
                "affiliate_potential": False,
            },
            {
                "title": "Free Meditation Streak Tracker",
                "description": "track your daily meditation practice. set duration goals, track consistency with heatmap, celebrate milestones. no account, works offline.\n\n#meditation #mindfulness #mentalhealth #wellness #dailyhabits",
                "link": "https://meditation-streak-landing.surge.sh",
                "image_spec": "1000x1500 vertical. Dark purple theme. Lotus icon. Heatmap. Timer. Text: 'Track Your Meditation Streak'",
                "category": "APP",
                "affiliate_potential": False,
            },
            {
                "title": "Free Reading Streak Tracker (Hit Your Book Goals)",
                "description": "track pages read daily, set book goals, celebrate finishing streaks. heatmap shows your consistency. no signup, no subscription.\n\n#reading #bookstagram #booklover #readinggoals #habits",
                "link": "https://reading-streak-landing.surge.sh",
                "image_spec": "1000x1500 vertical. Dark warm theme. Book icon. Heatmap. Page counter. Text: 'Track Your Reading Streak'",
                "category": "APP",
                "affiliate_potential": False,
            },
        ],
    },
}


def generate_pin_batch():
    """Generate a batch of pins from templates, avoiding duplicates."""
    queue = load_queue()
    generated_ids = {p["id"] for p in queue}
    new_pins = []

    for niche, data in PIN_TEMPLATES.items():
        for pin in data["pins"]:
            pin_id = hashlib.md5(f"{niche}:{pin['title']}".encode()).hexdigest()[:12]
            if pin_id in generated_ids:
                continue

            new_pins.append({
                "id": pin_id,
                "niche": niche,
                "title": pin["title"],
                "description": pin["description"],
                "link": pin["link"],
                "image_spec": pin["image_spec"],
                "boards": data["boards"],
                "category": pin["category"],
                "affiliate": pin["affiliate_potential"],
                "status": "READY",
                "created": datetime.now().isoformat(),
                "posted": None,
            })

    queue.extend(new_pins)
    save_queue(queue)
    print(f"Generated {len(new_pins)} new pins. Total queue: {len(queue)}")
    return new_pins


def export_tailwind_csv():
    """Export pin queue to Tailwind-compatible CSV for bulk scheduling."""
    queue = load_queue()
    ready = [p for p in queue if p["status"] == "READY"]

    with open(EXPORT_FILE, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Board", "Pin Title", "Pin Description", "Destination Link", "Image URL", "Schedule Date"])

        schedule_date = datetime.now()
        for pin in ready:
            for board in pin["boards"]:
                writer.writerow([
                    board,
                    pin["title"],
                    pin["description"],
                    pin["link"],
                    f"[Generate from spec: {pin['image_spec'][:50]}...]",
                    schedule_date.strftime("%Y-%m-%d %H:%M"),
                ])
                schedule_date += timedelta(hours=4)

    print(f"Exported {len(ready)} pins ({len(ready) * len(PIN_TEMPLATES.get('productivity_apps', {}).get('boards', [1,2,3,4]))} board placements) to {EXPORT_FILE}")


def show_status():
    """Show pipeline statistics."""
    queue = load_queue()
    stats = {
        "total_pins": len(queue),
        "ready": len([p for p in queue if p["status"] == "READY"]),
        "posted": len([p for p in queue if p["status"] == "POSTED"]),
        "by_niche": {},
        "by_category": {},
        "affiliate_pins": len([p for p in queue if p.get("affiliate")]),
    }

    for pin in queue:
        niche = pin.get("niche", "unknown")
        cat = pin.get("category", "unknown")
        stats["by_niche"][niche] = stats["by_niche"].get(niche, 0) + 1
        stats["by_category"][cat] = stats["by_category"].get(cat, 0) + 1

    print(f"\n=== Pinterest Content Pipeline ===")
    print(f"Total pins: {stats['total_pins']}")
    print(f"Ready to post: {stats['ready']}")
    print(f"Already posted: {stats['posted']}")
    print(f"Affiliate pins: {stats['affiliate_pins']}")
    print(f"\nBy niche:")
    for niche, count in sorted(stats["by_niche"].items(), key=lambda x: -x[1]):
        print(f"  {niche}: {count}")
    print(f"\nBy category:")
    for cat, count in sorted(stats["by_category"].items(), key=lambda x: -x[1]):
        print(f"  {cat}: {count}")

    with open(STATS_FILE, "w") as f:
        json.dump(stats, f, indent=2)


def load_queue():
    if QUEUE_FILE.exists():
        with open(QUEUE_FILE) as f:
            return json.load(f)
    return []


def save_queue(queue):
    with open(QUEUE_FILE, "w") as f:
        json.dump(queue, f, indent=2)


if __name__ == "__main__":
    args = sys.argv[1:]

    if "--generate" in args:
        generate_pin_batch()
    elif "--export-csv" in args:
        export_tailwind_csv()
    elif "--status" in args:
        show_status()
    else:
        print("Usage: pinterest_content_pipeline.py --generate | --export-csv | --status")
        print("\nGenerates Pinterest pin content from PRINTMAXX app portfolio.")
        print("Each pin links to a live app/tool on surge.sh.")
        print("Pins have 6-12 month shelf life. Compound traffic.")
