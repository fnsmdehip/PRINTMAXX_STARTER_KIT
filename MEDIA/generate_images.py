#!/usr/bin/env python3
"""
PRINTMAXX Image Factory - Playwright Screenshot Generator
Generates pixel-perfect images from HTML templates at zero cost.

Usage: python3 MEDIA/generate_images.py
"""

import json
import os
from pathlib import Path
from datetime import datetime
from playwright.sync_api import sync_playwright

BASE_DIR = Path(__file__).parent
TEMPLATES_DIR = BASE_DIR / "image_templates"
OUTPUT_DIR = BASE_DIR / "generated_images"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# ── IMAGE DEFINITIONS ─────────────────────────────────────────

PRODUCT_COVERS = [
    {
        "id": "cover_cold_email_subjects",
        "template": "product_cover.html",
        "width": 1280, "height": 720,
        "replacements": {
            "DIGITAL PRODUCT": "EMAIL TEMPLATES",
            "73 Cold Email <span class=\"accent\">Subject Lines</span>": "73 Cold Email <span class=\"accent\">Subject Lines</span>",
            "battle-tested subject lines that get 40%+ open rates": "battle-tested openers that get 40%+ open rates. copy-paste ready.",
        },
    },
    {
        "id": "cover_funnel_teardown",
        "template": "product_cover.html",
        "width": 1280, "height": 720,
        "replacements": {
            "DIGITAL PRODUCT": "GROWTH PLAYBOOK",
            "73 Cold Email <span class=\"accent\">Subject Lines</span>": "Funnel <span class=\"accent\">Teardown</span> Pack",
            "battle-tested subject lines that get 40%+ open rates": "reverse-engineered funnels from $1M+ indie products",
            ">73<": ">12<",
            ">Subject Lines<": ">Teardowns<",
            ">40%+<": ">$1M+<",
            ">Open Rate<": ">Revenue Studied<",
            ">$0<": ">47<",
            ">Ad Spend<": ">Pages<",
        },
    },
    {
        "id": "cover_ai_automation",
        "template": "product_cover.html",
        "width": 1280, "height": 720,
        "replacements": {
            "DIGITAL PRODUCT": "AI BLUEPRINT",
            "73 Cold Email <span class=\"accent\">Subject Lines</span>": "AI Automation <span class=\"accent\">Blueprint</span>",
            "battle-tested subject lines that get 40%+ open rates": "automate 80% of your workflow with free AI tools",
            ">73<": ">15<",
            ">Subject Lines<": ">Workflows<",
            ">40%+<": ">10hrs<",
            ">Open Rate<": ">Saved / Week<",
            ">$0<": ">$0<",
            ">Ad Spend<": ">Tool Cost<",
        },
    },
    {
        "id": "cover_solopreneur_ops",
        "template": "product_cover.html",
        "width": 1280, "height": 720,
        "replacements": {
            "DIGITAL PRODUCT": "OPERATIONS SYSTEM",
            "73 Cold Email <span class=\"accent\">Subject Lines</span>": "Solopreneur <span class=\"accent\">Ops System</span>",
            "battle-tested subject lines that get 40%+ open rates": "the exact system running 32 agents, 7 apps, and 45 deploys",
            ">73<": ">32<",
            ">Subject Lines<": ">Agent Templates<",
            ">40%+<": ">7<",
            ">Open Rate<": ">App Configs<",
            ">$0<": ">24/7<",
            ">Ad Spend<": ">Automation<",
        },
    },
    {
        "id": "cover_cold_email_playbook",
        "template": "product_cover.html",
        "width": 1280, "height": 720,
        "replacements": {
            "DIGITAL PRODUCT": "OUTBOUND PLAYBOOK",
            "73 Cold Email <span class=\"accent\">Subject Lines</span>": "Cold Email <span class=\"accent\">Playbook</span>",
            "battle-tested subject lines that get 40%+ open rates": "from zero replies to booked meetings. the full cold outbound system.",
            ">73<": ">6<",
            ">Subject Lines<": ">Frameworks<",
            ">40%+<": ">87%<",
            ">Open Rate<": ">Margin<",
            ">$0<": ">$0<",
            ">Ad Spend<": ">To Start<",
        },
    },
]

SOCIAL_CARDS = [
    {
        "id": "social_plumber_saas",
        "template": "social_card.html",
        "width": 1200, "height": 675,
        "replacements": {
            "i monitor <span class=\"highlight\">200+ competitor pages</span>. they update something, i know in 30 seconds.":
                "a guy makes <span class=\"highlight\">$14K/month</span> from an app that sends invoice reminders to plumbers.",
            "the system that runs while you sleep":
                "he found the idea in a reddit comment section.",
        },
    },
    {
        "id": "social_pdf_product",
        "template": "social_card.html",
        "width": 1200, "height": 675,
        "replacements": {
            "i monitor <span class=\"highlight\">200+ competitor pages</span>. they update something, i know in 30 seconds.":
                "someone spent $250 on a PDF guide. now makes <span class=\"highlight\">$2,300/month</span> selling it.",
            "the system that runs while you sleep":
                "92% profit margin. gumroad listing. zero monthly cost.",
        },
    },
    {
        "id": "social_ai_wrapper",
        "template": "social_card.html",
        "width": 1200, "height": 675,
        "replacements": {
            "i monitor <span class=\"highlight\">200+ competitor pages</span>. they update something, i know in 30 seconds.":
                "studied 53 indie app businesses. ChatBase hit <span class=\"highlight\">$250K MRR</span>.",
            "the system that runs while you sleep":
                "both are wrappers on existing AI. nobody wants to learn prompts. they want a button.",
        },
    },
    {
        "id": "social_geo_seo",
        "template": "social_card.html",
        "width": 1200, "height": 675,
        "replacements": {
            "i monitor <span class=\"highlight\">200+ competitor pages</span>. they update something, i know in 30 seconds.":
                "forget SEO. the next $10K/mo category is <span class=\"highlight\">GEO</span>. Generative Engine Optimization.",
            "the system that runs while you sleep":
                "making your content rank in ChatGPT, Gemini, Claude answers.",
        },
    },
    {
        "id": "social_build_trap",
        "template": "social_card.html",
        "width": 1200, "height": 675,
        "replacements": {
            "i monitor <span class=\"highlight\">200+ competitor pages</span>. they update something, i know in 30 seconds.":
                "<span class=\"highlight\">58 assets built</span>. 45 deployed. 0 generating revenue.",
            "the system that runs while you sleep":
                "the bottleneck is listing something for sale and pressing publish.",
        },
    },
]

QUOTE_CARDS = [
    {
        "id": "quote_publish_gap",
        "template": "quote_card.html",
        "width": 1080, "height": 1080,
        "replacements": {
            "stop overthinking this. just set up the alerts and start watching.":
                "the gap between $0 and $200/month is literally 45 minutes of copy-paste. building is the drug. shipping is the medicine.",
        },
    },
    {
        "id": "quote_boring_problems",
        "template": "quote_card.html",
        "width": 1080, "height": 1080,
        "replacements": {
            "stop overthinking this. just set up the alerts and start watching.":
                "boring problems. recurring revenue. no competition. find the complaint that appears 50+ times. build the simplest possible fix.",
        },
    },
    {
        "id": "quote_automate_everything",
        "template": "quote_card.html",
        "width": 1080, "height": 1080,
        "replacements": {
            "stop overthinking this. just set up the alerts and start watching.":
                'turns out you can automate everything except the part where someone pays you money. that part requires pressing "publish."',
        },
    },
]

NICHE_CARDS = [
    {
        "id": "niche_printmaxxer_agents",
        "template": "niche_card.html",
        "width": 1200, "height": 675,
        "replacements": {
            '<span class="highlight">32 AI agents</span> running 24/7. cost: $0. revenue: also $0. the bottleneck is pressing publish.':
                'running <span class="highlight">32 AI agents</span> 24/7 on my laptop. CEO agent auto-promotes winners at 3am.',
            "building in public, for real":
                "cost: $0/month in compute. revenue generated: also $0.",
        },
    },
    {
        "id": "niche_selah_discipline",
        "template": "niche_card.html",
        "width": 1200, "height": 675,
        "replacements": {
            'data-niche="printmaxxer"': 'data-niche="selahmoments"',
            '<span class="highlight">32 AI agents</span> running 24/7. cost: $0. revenue: also $0. the bottleneck is pressing publish.':
                'discipline is choosing between what you want <span class="highlight">now</span> and what you want <span class="highlight">most</span>.',
            "building in public, for real":
                "your morning routine is your first prayer of the day",
            "@printmaxxer": "@selahmoments",
        },
    },
    {
        "id": "niche_drifthour_vibe",
        "template": "niche_card.html",
        "width": 1200, "height": 675,
        "replacements": {
            'data-niche="printmaxxer"': 'data-niche="drifthour"',
            '<span class="highlight">32 AI agents</span> running 24/7. cost: $0. revenue: also $0. the bottleneck is pressing publish.':
                'the version of you that wins everything <span class="highlight">just woke up</span>.',
            "building in public, for real":
                "aesthetic intuition is the alpha",
            "@printmaxxer": "@drifthour",
        },
    },
]

# OG Image (just screenshot the default template)
OG_IMAGES = [
    {
        "id": "og_printmaxx_default",
        "template": "og_image.html",
        "width": 1200, "height": 630,
        "replacements": {},
    },
]


# ── GENERATOR ──────────────────────────────────────────────────

def generate_image(page, definition):
    template_path = TEMPLATES_DIR / definition["template"]
    html = template_path.read_text()

    for find, replace in definition["replacements"].items():
        html = html.replace(find, replace)

    page.set_viewport_size({"width": definition["width"], "height": definition["height"]})
    page.set_content(html)
    page.wait_for_load_state("networkidle")

    output_path = OUTPUT_DIR / f'{definition["id"]}.png'
    page.screenshot(path=str(output_path), type="png")

    size = output_path.stat().st_size
    print(f'  [OK] {definition["id"]}.png ({size // 1024}KB)')
    return {
        "id": definition["id"],
        "path": str(output_path),
        "size": size,
        "width": definition["width"],
        "height": definition["height"],
    }


def main():
    print("PRINTMAXX Image Factory")
    print("-" * 50)
    print(f"Templates: {TEMPLATES_DIR}")
    print(f"Output: {OUTPUT_DIR}")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        catalog = []

        categories = [
            ("Product Covers (1280x720)", PRODUCT_COVERS),
            ("Social Cards (1200x675)", SOCIAL_CARDS),
            ("Quote Cards (1080x1080)", QUOTE_CARDS),
            ("Niche Cards (1200x675)", NICHE_CARDS),
            ("OG Images (1200x630)", OG_IMAGES),
        ]

        for cat_name, items in categories:
            print(f"\n{cat_name}")
            print("-" * 40)
            for item in items:
                try:
                    result = generate_image(page, item)
                    result["category"] = cat_name
                    result["template"] = item["template"]
                    result["generated_at"] = datetime.now().isoformat()
                    catalog.append(result)
                except Exception as e:
                    print(f'  [FAIL] {item["id"]}: {e}')

        browser.close()

    # Write catalog
    catalog_path = OUTPUT_DIR / "catalog.json"
    existing = []
    if catalog_path.exists():
        try:
            existing = json.loads(catalog_path.read_text())
        except Exception:
            existing = []

    # Merge by id
    catalog_map = {e["id"]: e for e in existing}
    for entry in catalog:
        catalog_map[entry["id"]] = entry
    merged = list(catalog_map.values())
    catalog_path.write_text(json.dumps(merged, indent=2))

    print(f"\n{'=' * 50}")
    print(f"Generated: {len(catalog)} images")
    print(f"Catalog: {len(merged)} total entries")
    print(f"Output: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
