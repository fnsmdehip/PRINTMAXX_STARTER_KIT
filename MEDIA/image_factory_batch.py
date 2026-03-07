#!/usr/bin/env python3
"""IMAGE FACTORY -- Batch image generator using Playwright HTML->PNG screenshots.
Generates social cards, quote cards, product covers, app promos, and data viz
from HTML templates. Zero external image dependencies. Pixel-perfect output.

All content is hardcoded in this script (no external input). Templates are read
as strings and content is injected via Python string replacement before rendering."""

import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path
from playwright.sync_api import sync_playwright

PROJECT_ROOT = Path(__file__).resolve().parent.parent
TEMPLATES_DIR = PROJECT_ROOT / "MEDIA" / "image_templates"
OUTPUT_DIR = PROJECT_ROOT / "MEDIA" / "generated_images"
CATALOG_PATH = OUTPUT_DIR / "catalog.json"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def read_template(name):
    """Read an HTML template file and return its content as a string."""
    path = TEMPLATES_DIR / name
    with open(path, "r") as f:
        return f.read()


def build_social_card(hook_html, subtitle):
    """Build a social_card from template with content replaced."""
    tmpl = read_template("social_card.html")
    tmpl = re.sub(
        r'<div class="hook">.*?</div>',
        f'<div class="hook">{hook_html}</div>',
        tmpl, count=1, flags=re.DOTALL
    )
    tmpl = re.sub(
        r'<div class="subtitle">.*?</div>',
        f'<div class="subtitle">{subtitle}</div>',
        tmpl, count=1, flags=re.DOTALL
    )
    return tmpl


def build_quote_card(quote_text):
    """Build a quote_card from template with quote replaced."""
    tmpl = read_template("quote_card.html")
    tmpl = re.sub(
        r'<div class="quote">.*?</div>',
        f'<div class="quote">{quote_text}</div>',
        tmpl, count=1, flags=re.DOTALL
    )
    return tmpl


def build_product_cover(badge, title_html, description, stats):
    """Build a product_cover from template with content replaced."""
    tmpl = read_template("product_cover.html")

    tmpl = re.sub(
        r'<div class="badge">.*?</div>',
        f'<div class="badge">{badge}</div>',
        tmpl, count=1, flags=re.DOTALL
    )
    tmpl = re.sub(
        r'<div class="title">.*?</div>',
        f'<div class="title">{title_html}</div>',
        tmpl, count=1, flags=re.DOTALL
    )
    tmpl = re.sub(
        r'<div class="description">.*?</div>',
        f'<div class="description">{description}</div>',
        tmpl, count=1, flags=re.DOTALL
    )

    stats_html = ""
    for s in stats:
        stats_html += (
            f'<div class="stat">'
            f'<div class="stat-value">{s["value"]}</div>'
            f'<div class="stat-label">{s["label"]}</div>'
            f'</div>'
        )
    # Match from <div class="stats-row"> to its closing </div> (greedy inner, stops at brand div)
    tmpl = re.sub(
        r'<div class="stats-row">.*?</div>\s*<div class="brand">',
        f'<div class="stats-row">{stats_html}</div>\n  <div class="brand">',
        tmpl, count=1, flags=re.DOTALL
    )
    return tmpl


def build_niche_card(niche, hook_html, subtitle, handle):
    """Build a niche_card from template with content replaced."""
    tmpl = read_template("niche_card.html")

    tmpl = tmpl.replace('data-niche="printmaxxer"', f'data-niche="{niche}"')
    tmpl = re.sub(
        r'<div class="hook">.*?</div>',
        f'<div class="hook">{hook_html}</div>',
        tmpl, count=1, flags=re.DOTALL
    )
    tmpl = re.sub(
        r'<div class="subtitle">.*?</div>',
        f'<div class="subtitle">{subtitle}</div>',
        tmpl, count=1, flags=re.DOTALL
    )
    tmpl = re.sub(
        r'<div class="handle">.*?</div>',
        f'<div class="handle">{handle}</div>',
        tmpl, count=1, flags=re.DOTALL
    )
    return tmpl


def build_data_viz(title, subtitle, stats):
    """Build a data_viz from template with content replaced."""
    tmpl = read_template("data_viz.html")

    tmpl = re.sub(
        r'<div class="title">.*?</div>',
        f'<div class="title">{title}</div>',
        tmpl, count=1, flags=re.DOTALL
    )
    tmpl = re.sub(
        r'<div class="subtitle">.*?</div>',
        f'<div class="subtitle">{subtitle}</div>',
        tmpl, count=1, flags=re.DOTALL
    )

    stats_html = ""
    for s in stats:
        stats_html += (
            f'<div class="stat-card">'
            f'<div class="stat-value">{s["value"]}</div>'
            f'<div class="stat-label">{s["label"]}</div>'
            f'<div class="stat-delta">{s["delta"]}</div>'
            f'</div>'
        )
    tmpl = re.sub(
        r'<div class="stats-grid">.*?</div>\s*<div class="brand">',
        f'<div class="stats-grid">{stats_html}</div><div class="brand">',
        tmpl, count=1, flags=re.DOTALL
    )
    return tmpl


# ──────────────────────────────────────────────
# IMAGE DEFINITIONS
# ──────────────────────────────────────────────

IMAGES = [
    # === SOCIAL CARDS (1200x675) ===
    {
        "id": "social_3400hr_math",
        "width": 1200, "height": 675,
        "category": "Social Cards (1200x675)",
        "template": "social_card.html",
        "html_fn": lambda: build_social_card(
            'calculated ROI: <span class="highlight">60 min human = $3,400/mo</span>. infinite agent hours = $0.',
            "the bottleneck was never the building"
        ),
    },
    {
        "id": "social_data_hoarder",
        "width": 1200, "height": 675,
        "category": "Social Cards (1200x675)",
        "template": "social_card.html",
        "html_fn": lambda: build_social_card(
            '<span class="highlight">2.87 million leads</span> in my database. zero emails sent.',
            "the most expensive procrastination tool ever built"
        ),
    },
    {
        "id": "social_agents_reality",
        "width": 1200, "height": 675,
        "category": "Social Cards (1200x675)",
        "template": "social_card.html",
        "html_fn": lambda: build_social_card(
            '<span class="highlight">32 AI agents</span> running 24/7 for a month. revenue: $0.',
            "14 apps. 26 sites. 269 scripts. 1,036 leads. publish = still pending."
        ),
    },
    {
        "id": "social_swarm_brain",
        "width": 1200, "height": 675,
        "category": "Social Cards (1200x675)",
        "template": "social_card.html",
        "html_fn": lambda: build_social_card(
            'my AI swarm brain <span class="highlight">throttled 12 agents</span>. reasoning: building more has negative ROI.',
            "when your AI tells you to stop building and start selling"
        ),
    },
    {
        "id": "social_406_graveyard",
        "width": 1200, "height": 675,
        "category": "Social Cards (1200x675)",
        "template": "social_card.html",
        "html_fn": lambda: build_social_card(
            '<span class="highlight">406 posts</span> queued. 0 posted. 16 emails drafted. 0 sent. 13 PDFs ready. 0 listed.',
            "a content strategy with no distribution is a diary"
        ),
    },
    {
        "id": "social_overnight_test",
        "width": 1200, "height": 675,
        "category": "Social Cards (1200x675)",
        "template": "social_card.html",
        "html_fn": lambda: build_social_card(
            'wrong question: what should i build tonight?<br>right question: what\'s built that i could have <span class="highlight">SOLD tonight</span>?',
            "the answer is always more than you think"
        ),
    },
    {
        "id": "social_cold_email_first",
        "width": 1200, "height": 675,
        "category": "Social Cards (1200x675)",
        "template": "social_card.html",
        "html_fn": lambda: build_social_card(
            '<span class="highlight">58%</span> of cold email replies come from the first email. not the follow-up.',
            "4-6 lines. no tracking pixels. mention their tech stack."
        ),
    },
    {
        "id": "social_hub_spoke",
        "width": 1200, "height": 675,
        "category": "Social Cards (1200x675)",
        "template": "social_card.html",
        "html_fn": lambda: build_social_card(
            '1 piece of content should become <span class="highlight">20</span>. every single time.',
            "hub-and-spoke model. same content, different packaging."
        ),
    },
    {
        "id": "social_131_zero",
        "width": 1200, "height": 675,
        "category": "Social Cards (1200x675)",
        "template": "social_card.html",
        "html_fn": lambda: build_social_card(
            'built <span class="highlight">131 products</span>. listed 0 for sale.',
            "if you haven't listed it where someone can buy it, you built a hobby."
        ),
    },

    # === QUOTE CARDS (1080x1080) ===
    {
        "id": "quote_building_trap",
        "width": 1080, "height": 1080,
        "category": "Quote Cards (1080x1080)",
        "template": "quote_card.html",
        "html_fn": lambda: build_quote_card(
            "the most dangerous thing in solopreneurship is feeling productive while making $0."
        ),
    },
    {
        "id": "quote_hot_take_bip",
        "width": 1080, "height": 1080,
        "category": "Quote Cards (1080x1080)",
        "template": "quote_card.html",
        "html_fn": lambda: build_quote_card(
            "most 'build in public' accounts are actually 'procrastinate in public' accounts."
        ),
    },
    {
        "id": "quote_unsexy_work",
        "width": 1080, "height": 1080,
        "category": "Quote Cards (1080x1080)",
        "template": "quote_card.html",
        "html_fn": lambda: build_quote_card(
            "the unsexy work is the only work that pays."
        ),
    },
    {
        "id": "quote_confession_automated",
        "width": 1080, "height": 1080,
        "category": "Quote Cards (1080x1080)",
        "template": "quote_card.html",
        "html_fn": lambda: build_quote_card(
            "i automated everything except the one thing that makes money."
        ),
    },
    {
        "id": "quote_build_sell_ratio",
        "width": 1080, "height": 1080,
        "category": "Quote Cards (1080x1080)",
        "template": "quote_card.html",
        "html_fn": lambda: build_quote_card(
            "build-to-sell ratio: 131 built. 0 listed. beating that should be easy."
        ),
    },
    {
        "id": "quote_diary",
        "width": 1080, "height": 1080,
        "category": "Quote Cards (1080x1080)",
        "template": "quote_card.html",
        "html_fn": lambda: build_quote_card(
            "what do you call a content strategy with no distribution? a diary."
        ),
    },

    # === PRODUCT COVERS (1280x720) ===
    {
        "id": "cover_vibe_coding",
        "width": 1280, "height": 720,
        "category": "Product Covers (1280x720)",
        "template": "product_cover.html",
        "html_fn": lambda: build_product_cover(
            "DIGITAL PRODUCT",
            'Vibe Coding <span class="accent">Playbook</span>',
            "build apps with AI pair programming. ship in hours, not weeks.",
            [{"value": "40+", "label": "Hours Research"}, {"value": "$47", "label": "One-Time"}, {"value": "PDF", "label": "Format"}],
        ),
    },
    {
        "id": "cover_local_biz_machine",
        "width": 1280, "height": 720,
        "category": "Product Covers (1280x720)",
        "template": "product_cover.html",
        "html_fn": lambda: build_product_cover(
            "DIGITAL PRODUCT",
            'Local Biz <span class="accent">Client Machine</span>',
            "scrape, qualify, and close local business clients on autopilot.",
            [{"value": "2.87M", "label": "Leads Available"}, {"value": "$97", "label": "One-Time"}, {"value": "PDF", "label": "Format"}],
        ),
    },
    {
        "id": "cover_twitter_growth",
        "width": 1280, "height": 720,
        "category": "Product Covers (1280x720)",
        "template": "product_cover.html",
        "html_fn": lambda: build_product_cover(
            "DIGITAL PRODUCT",
            'Twitter/X <span class="accent">Growth Playbook</span>',
            "algorithms, hooks, and posting systems that build real audiences.",
            [{"value": "50+", "label": "Hook Templates"}, {"value": "$27", "label": "One-Time"}, {"value": "PDF", "label": "Format"}],
        ),
    },
    {
        "id": "cover_content_farm",
        "width": 1280, "height": 720,
        "category": "Product Covers (1280x720)",
        "template": "product_cover.html",
        "html_fn": lambda: build_product_cover(
            "DIGITAL PRODUCT",
            'AI Content Farm <span class="accent">Blueprint</span>',
            "1 piece of content becomes 20. hub-and-spoke model with AI.",
            [{"value": "6", "label": "Platforms"}, {"value": "$37", "label": "One-Time"}, {"value": "PDF", "label": "Format"}],
        ),
    },
    {
        "id": "cover_sleep_youtube",
        "width": 1280, "height": 720,
        "category": "Product Covers (1280x720)",
        "template": "product_cover.html",
        "html_fn": lambda: build_product_cover(
            "STARTER KIT",
            'Sleep YouTube <span class="accent">Starter Kit</span>',
            "faceless youtube channel. rain sounds. sleep music. passive income.",
            [{"value": "10+", "label": "Audio Templates"}, {"value": "$19", "label": "One-Time"}, {"value": "KIT", "label": "Format"}],
        ),
    },
    {
        "id": "cover_viral_tweets",
        "width": 1280, "height": 720,
        "category": "Product Covers (1280x720)",
        "template": "product_cover.html",
        "html_fn": lambda: build_product_cover(
            "TEMPLATE PACK",
            '50 Viral Tweet <span class="accent">Templates</span>',
            "copy-paste tweet frameworks tested across 100K+ impressions.",
            [{"value": "50", "label": "Templates"}, {"value": "$9", "label": "One-Time"}, {"value": "PDF", "label": "Format"}],
        ),
    },

    # === APP PROMO CARDS (1200x675) ===
    {
        "id": "app_coldmaxx",
        "width": 1200, "height": 675,
        "category": "App Promo Cards (1200x675)",
        "template": "niche_card.html",
        "html_fn": lambda: build_niche_card(
            "printmaxxer",
            '<span class="highlight">ColdMaxx</span>: 55KB. offline-capable. zero dependencies.',
            "built in one session with claude code. PWAs are free.",
            "@PRINTMAXXER",
        ),
    },
    {
        "id": "app_focuslock",
        "width": 1200, "height": 675,
        "category": "App Promo Cards (1200x675)",
        "template": "niche_card.html",
        "html_fn": lambda: build_niche_card(
            "printmaxxer",
            '<span class="highlight">FocusLock</span>: lock your phone. build deep work streaks.',
            "opal charges $99/yr. this is free. PWA. works offline.",
            "@PRINTMAXXER",
        ),
    },
    {
        "id": "app_prayerlock",
        "width": 1200, "height": 675,
        "category": "App Promo Cards (1200x675)",
        "template": "niche_card.html",
        "html_fn": lambda: build_niche_card(
            "selahmoments",
            '<span class="highlight">PrayerLock</span>: never miss a prayer. streak-based accountability.',
            "hallow charges $9.99/mo. this is free. every denomination.",
            "@selahmoments",
        ),
    },
    {
        "id": "app_sleepmaxx",
        "width": 1200, "height": 675,
        "category": "App Promo Cards (1200x675)",
        "template": "niche_card.html",
        "html_fn": lambda: build_niche_card(
            "drifthour",
            '<span class="highlight">SleepMaxx</span>: track sleep quality. build consistency.',
            "no subscriptions. no accounts. just open it and track.",
            "@drifthour",
        ),
    },
    {
        "id": "app_walktounlock",
        "width": 1200, "height": 675,
        "category": "App Promo Cards (1200x675)",
        "template": "niche_card.html",
        "html_fn": lambda: build_niche_card(
            "repscheme",
            '<span class="highlight">WalkToUnlock</span>: walk to unlock your phone. gamified movement.',
            "55KB PWA. works offline. no excuses.",
            "@repscheme",
        ),
    },

    # === DATA VIZ (1200x675) ===
    {
        "id": "data_viz_competitive",
        "width": 1200, "height": 675,
        "category": "Data Viz (1200x675)",
        "template": "data_viz.html",
        "html_fn": lambda: build_data_viz(
            "competitive landscape -- our position",
            "131 products built. 0 activated. competitors printing money.",
            [
                {"value": "131", "label": "Products Built", "delta": "+14 this week"},
                {"value": "$0", "label": "Revenue", "delta": "day 32 at zero"},
                {"value": "2.87M", "label": "Leads Scraped", "delta": "0 contacted"},
                {"value": "32", "label": "AI Agents", "delta": "24/7 autonomous"},
            ],
        ),
    },
    {
        "id": "data_viz_activation_gap",
        "width": 1200, "height": 675,
        "category": "Data Viz (1200x675)",
        "template": "data_viz.html",
        "html_fn": lambda: build_data_viz(
            "the activation gap -- built vs selling",
            "everything is built. nothing is selling.",
            [
                {"value": "406", "label": "Posts Queued", "delta": "0 posted"},
                {"value": "16", "label": "Emails Drafted", "delta": "0 sent"},
                {"value": "13", "label": "PDFs Ready", "delta": "0 listed"},
                {"value": "26", "label": "Sites Live", "delta": "0 monetized"},
            ],
        ),
    },
]


def generate_all():
    """Generate all images using Playwright."""
    catalog = []
    generated = 0
    errors = 0

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)

        for config in IMAGES:
            img_id = config["id"]
            output_path = OUTPUT_DIR / f"{img_id}.png"

            try:
                html_content = config["html_fn"]()

                page = browser.new_page(
                    viewport={"width": config["width"], "height": config["height"]}
                )
                page.set_content(html_content, wait_until="networkidle")
                page.wait_for_timeout(150)
                page.screenshot(path=str(output_path), type="png")

                file_size = os.path.getsize(output_path)
                catalog.append({
                    "id": img_id,
                    "path": str(output_path),
                    "size": file_size,
                    "width": config["width"],
                    "height": config["height"],
                    "category": config["category"],
                    "template": config["template"],
                    "generated_at": datetime.now().isoformat(),
                })

                generated += 1
                print(f"  [{generated}/{len(IMAGES)}] {img_id}.png ({file_size:,} bytes)")
                page.close()

            except Exception as e:
                errors += 1
                print(f"  ERROR: {img_id} -- {e}", file=sys.stderr)

        browser.close()

    # Merge with existing catalog
    existing_catalog = []
    if CATALOG_PATH.exists():
        with open(CATALOG_PATH) as f:
            existing_catalog = json.load(f)

    new_ids = {entry["id"] for entry in catalog}
    merged = [e for e in existing_catalog if e["id"] not in new_ids] + catalog
    merged.sort(key=lambda x: x["id"])

    with open(CATALOG_PATH, "w") as f:
        json.dump(merged, f, indent=2)

    print(f"\nDone. Generated: {generated} | Errors: {errors} | Total catalog: {len(merged)}")
    return generated, errors


if __name__ == "__main__":
    print("IMAGE FACTORY -- Batch Generation")
    print(f"Templates: {TEMPLATES_DIR}")
    print(f"Output: {OUTPUT_DIR}")
    print(f"Images to generate: {len(IMAGES)}")
    print("---")
    generate_all()
