#!/usr/bin/env python3
"""
PRINTMAXX Image Factory — Mar 7 Batch
Generates images for all posting queue content that needs visuals.
"""

import json
import shutil
from pathlib import Path
from datetime import datetime
from playwright.sync_api import sync_playwright

BASE_DIR = Path(__file__).parent
TEMPLATES_DIR = BASE_DIR / "image_templates"
OUTPUT_DIR = BASE_DIR / "generated_images"
POSTING_QUEUE = BASE_DIR.parent / "CONTENT" / "social" / "posting_queue"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# ── MAR 7-8 SCHEDULED TWEETS ──────────────────────────────────

STAT_HIGHLIGHTS = [
    {
        "id": "stat_reddit_340",
        "template": "stat_highlight.html",
        "width": 1200, "height": 675,
        "replacements": {},  # default content is already for this tweet
        "pair_with": "twitter_PRINTMAXXER_mar7_0730.txt",
    },
    {
        "id": "stat_464k_emails",
        "template": "stat_highlight.html",
        "width": 1200, "height": 675,
        "replacements": {
            ">340<": ">464K<",
            "customers from reddit. zero ad spend.": "cold emails sent last year across clients.",
            "the trick is not marketing at all. just be useful in the right threads.":
                "tested every list source. apollo, zoominfo, manual scraping. buying lists is dead.",
        },
        "pair_with": "twitter_PRINTMAXXER_mar7_1100.txt",
    },
    {
        "id": "stat_2x_reply",
        "template": "stat_highlight.html",
        "width": 1200, "height": 675,
        "replacements": {
            ">340<": ">2x<",
            "customers from reddit. zero ad spend.": "reply rates after killing open tracking.",
            "the trick is not marketing at all. just be useful in the right threads.":
                "gmail flags tracking pixels now. write emails people respond to.",
        },
        "pair_with": "twitter_PRINTMAXXER_mar7_1430.txt",
    },
    {
        "id": "stat_2_4x_timing",
        "template": "stat_highlight.html",
        "width": 1200, "height": 675,
        "replacements": {
            ">340<": ">2-4x<",
            "customers from reddit. zero ad spend.": "reply rates with intent-based timing.",
            "the trick is not marketing at all. just be useful in the right threads.":
                "send outreach when someone just posted a hiring tweet or launched something.",
        },
        "pair_with": "twitter_PRINTMAXXER_mar7_1800.txt",
    },
    {
        "id": "stat_gmail_pixel",
        "template": "stat_highlight.html",
        "width": 1200, "height": 675,
        "replacements": {
            ">340<": ">0%<",
            "customers from reddit. zero ad spend.": "the value of open tracking in 2026.",
            "the trick is not marketing at all. just be useful in the right threads.":
                "gmail warns users about tracking pixels. disable it. focus on replies.",
        },
        "pair_with": "twitter_PRINTMAXXER_mar8_0730.txt",
    },
    {
        "id": "stat_300mo_cold_email",
        "template": "stat_highlight.html",
        "width": 1200, "height": 675,
        "replacements": {
            ">340<": ">$297<",
            "customers from reddit. zero ad spend.": "total cost to send 2,500 cold emails daily.",
            "the trick is not marketing at all. just be useful in the right threads.":
                "10 domains, 30 mailboxes, validation, platform. agencies charge $5-10K for this.",
        },
        "pair_with": "twitter_PRINTMAXXER_mar8_1100.txt",
    },
]

# ── COMPOUND CONTENT SOCIAL CARDS ──────────────────────────────

SOCIAL_CARDS = [
    {
        "id": "social_131_products",
        "template": "social_card.html",
        "width": 1200, "height": 675,
        "replacements": {
            "i monitor <span class=\"highlight\">200+ competitor pages</span>. they update something, i know in 30 seconds.":
                "built <span class=\"highlight\">131 products</span>. listed 0 for sale. the most dangerous thing in solopreneurship is feeling productive while making $0.",
            "the system that runs while you sleep":
                "if you haven't listed it where someone can buy it, you built a hobby.",
        },
        "pair_with": None,
    },
    {
        "id": "social_2_87m_leads",
        "template": "social_card.html",
        "width": 1200, "height": 675,
        "replacements": {
            "i monitor <span class=\"highlight\">200+ competitor pages</span>. they update something, i know in 30 seconds.":
                "<span class=\"highlight\">2.87 million leads</span> in my database. zero emails sent.",
            "the system that runs while you sleep":
                "this is not a flex. this is the most expensive procrastination tool ever built.",
        },
        "pair_with": None,
    },
    {
        "id": "social_32_agents_zero",
        "template": "social_card.html",
        "width": 1200, "height": 675,
        "replacements": {
            "i monitor <span class=\"highlight\">200+ competitor pages</span>. they update something, i know in 30 seconds.":
                "running <span class=\"highlight\">32 autonomous AI agents</span> 24/7 for a month. revenue: $0.",
            "the system that runs while you sleep":
                "they built 14 apps, 26 sites, 269 scripts. they couldn't click publish on gumroad.",
        },
        "pair_with": None,
    },
    {
        "id": "social_swarm_throttle",
        "template": "social_card.html",
        "width": 1200, "height": 675,
        "replacements": {
            "i monitor <span class=\"highlight\">200+ competitor pages</span>. they update something, i know in 30 seconds.":
                "my AI swarm brain <span class=\"highlight\">throttled 12 of its own agents</span>.",
            "the system that runs while you sleep":
                "its reasoning: building more has negative ROI at $0 revenue. start selling.",
        },
        "pair_with": None,
    },
]

# ── THREAD CARDS ───────────────────────────────────────────────

THREAD_CARDS = [
    {
        "id": "thread_cold_email_cost",
        "template": "thread_card.html",
        "width": 1200, "height": 675,
        "replacements": {
            "cold email reality check: ran <span class=\"highlight\">464K emails</span> last year.":
                "what it actually costs to send <span class=\"highlight\">2,500 cold emails</span> daily.",
            "<div class=\"bullet\">tested every list source</div>": "<div class=\"bullet\">10 domains at $12/yr each</div>",
            "<div class=\"bullet\">buying lists is dead</div>": "<div class=\"bullet\">30 mailboxes at $4/mo each</div>",
            "<div class=\"bullet\">here's what actually works</div>": "<div class=\"bullet\">total: under $300/mo</div>",
        },
        "pair_with": None,
    },
    {
        "id": "thread_building_trap",
        "template": "thread_card.html",
        "width": 1200, "height": 675,
        "replacements": {
            "cold email reality check: ran <span class=\"highlight\">464K emails</span> last year.":
                "day 32 at <span class=\"highlight\">$0 revenue</span>. here's the real bottleneck.",
            "<div class=\"bullet\">tested every list source</div>": "<div class=\"bullet\">131 products built, 0 listed</div>",
            "<div class=\"bullet\">buying lists is dead</div>": "<div class=\"bullet\">406 posts queued, 0 posted</div>",
            "<div class=\"bullet\">here's what actually works</div>": "<div class=\"bullet\">building is the drug. shipping is the medicine.</div>",
        },
        "pair_with": None,
    },
]

# ── QUOTE CARDS ────────────────────────────────────────────────

QUOTE_CARDS = [
    {
        "id": "quote_day32_zero",
        "template": "quote_card.html",
        "width": 1080, "height": 1080,
        "replacements": {
            "stop overthinking this. just set up the alerts and start watching.":
                "day 32 at $0 revenue. 63 assets built. 3,550 monthly pipeline value. the bottleneck isn't building. it's activating.",
        },
        "pair_with": "bip_day32_revenue.txt",
    },
    {
        "id": "quote_406_diary",
        "template": "quote_card.html",
        "width": 1080, "height": 1080,
        "replacements": {
            "stop overthinking this. just set up the alerts and start watching.":
                "406 social posts queued. 0 posted. what do you call a content strategy with no distribution? a diary.",
        },
        "pair_with": None,
    },
    {
        "id": "quote_publish_button",
        "template": "quote_card.html",
        "width": 1080, "height": 1080,
        "replacements": {
            "stop overthinking this. just set up the alerts and start watching.":
                "turns out you can automate everything except the part where someone gives you money. that part requires pressing publish.",
        },
        "pair_with": None,
    },
    {
        "id": "quote_right_question",
        "template": "quote_card.html",
        "width": 1080, "height": 1080,
        "replacements": {
            "stop overthinking this. just set up the alerts and start watching.":
                "wrong question: what should i build tonight? right question: what's already built that i could sell tonight?",
        },
        "pair_with": None,
    },
]

# ── DATA VIZ — SWARM STATUS ───────────────────────────────────

DATA_VIZ = [
    {
        "id": "data_viz_day32_status",
        "template": "data_viz.html",
        "width": 1200, "height": 675,
        "replacements": {
            "system status — last 24 hours": "day 32 — the activation gap",
            "autonomous agent performance dashboard": "everything built vs everything earning",
            ">27<": ">131<",
            ">Active Agents<": ">Products Built<",
            ">+6 today<": ">0 listed<",
            ">142<": ">406<",
            ">Tasks Run<": ">Posts Queued<",
            ">+38 vs yesterday<": ">0 posted<",
            ">89%<": ">2.87M<",
            ">Success Rate<": ">Leads Found<",
            ">+12% this week<": ">0 emailed<",
            ">$0<": ">$0<",
            ">Revenue<": ">Revenue<",
            ">soon<": ">activation needed<",
        },
        "pair_with": None,
    },
    {
        "id": "data_viz_cold_email_cost",
        "template": "data_viz.html",
        "width": 1200, "height": 675,
        "replacements": {
            "system status — last 24 hours": "cold email unit economics",
            "autonomous agent performance dashboard": "2,500 emails/day at under $300/month",
            ">27<": ">$120<",
            ">Active Agents<": ">Domains / Year<",
            ">+6 today<": ">10 domains<",
            ">142<": ">$120<",
            ">Tasks Run<": ">Mailboxes / Mo<",
            ">+38 vs yesterday<": ">30 accounts<",
            ">89%<": ">$97<",
            ">Success Rate<": ">Platform / Mo<",
            ">+12% this week<": ">sending infra<",
            ">$0<": ">$297<",
            ">Revenue<": ">Total Monthly<",
            ">soon<": ">vs $5-10K agency<",
        },
        "pair_with": None,
    },
]

# ── NEW PRODUCT COVERS ────────────────────────────────────────

PRODUCT_COVERS = [
    {
        "id": "cover_activation_playbook",
        "template": "product_cover.html",
        "width": 1280, "height": 720,
        "replacements": {
            "DIGITAL PRODUCT": "LAUNCH PLAYBOOK",
            "73 Cold Email <span class=\"accent\">Subject Lines</span>": "The Activation <span class=\"accent\">Playbook</span>",
            "battle-tested subject lines that get 40%+ open rates": "from 131 products built to first dollar. the step-by-step listing system.",
            ">73<": ">12<",
            ">Subject Lines<": ">Steps<",
            ">40%+<": ">45min<",
            ">Open Rate<": ">To First $<",
            ">$0<": ">$0<",
            ">Ad Spend<": ">To Start<",
        },
        "pair_with": None,
    },
    {
        "id": "cover_reddit_growth",
        "template": "product_cover.html",
        "width": 1280, "height": 720,
        "replacements": {
            "DIGITAL PRODUCT": "GROWTH SYSTEM",
            "73 Cold Email <span class=\"accent\">Subject Lines</span>": "Reddit <span class=\"accent\">Growth Machine</span>",
            "battle-tested subject lines that get 40%+ open rates": "340 customers from reddit comments. zero ad spend. zero marketing.",
            ">73<": ">340<",
            ">Subject Lines<": ">Customers<",
            ">40%+<": ">$0<",
            ">Open Rate<": ">Ad Spend<",
            ">$0<": ">41<",
            ">Ad Spend<": ">Subreddits<",
        },
        "pair_with": None,
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

    # Copy to posting queue if paired
    pair_with = definition.get("pair_with")
    if pair_with and POSTING_QUEUE.exists():
        pair_name = Path(pair_with).stem + ".png"
        pair_path = POSTING_QUEUE / pair_name
        shutil.copy2(output_path, pair_path)
        print(f'  [PAIRED] {pair_path.name}')

    return {
        "id": definition["id"],
        "path": str(output_path),
        "size": size,
        "width": definition["width"],
        "height": definition["height"],
    }


def main():
    print("PRINTMAXX Image Factory — Mar 7 Batch")
    print("=" * 55)
    print(f"Templates: {TEMPLATES_DIR}")
    print(f"Output: {OUTPUT_DIR}")
    print(f"Posting Queue: {POSTING_QUEUE}")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        catalog = []

        categories = [
            ("Stat Highlights (1200x675)", STAT_HIGHLIGHTS),
            ("Social Cards (1200x675)", SOCIAL_CARDS),
            ("Thread Cards (1200x675)", THREAD_CARDS),
            ("Quote Cards (1080x1080)", QUOTE_CARDS),
            ("Data Viz (1200x675)", DATA_VIZ),
            ("Product Covers (1280x720)", PRODUCT_COVERS),
        ]

        for cat_name, items in categories:
            print(f"\n{cat_name}")
            print("-" * 45)
            for item in items:
                try:
                    result = generate_image(page, item)
                    result["category"] = cat_name
                    result["template"] = item["template"]
                    result["generated_at"] = datetime.now().isoformat()
                    if item.get("pair_with"):
                        result["paired_with"] = item["pair_with"]
                    catalog.append(result)
                except Exception as e:
                    print(f'  [FAIL] {item["id"]}: {e}')

        browser.close()

    # Merge into existing catalog
    catalog_path = OUTPUT_DIR / "catalog.json"
    existing = []
    if catalog_path.exists():
        try:
            existing = json.loads(catalog_path.read_text())
        except Exception:
            existing = []

    catalog_map = {e["id"]: e for e in existing}
    for entry in catalog:
        catalog_map[entry["id"]] = entry
    merged = list(catalog_map.values())
    catalog_path.write_text(json.dumps(merged, indent=2))

    print(f"\n{'=' * 55}")
    print(f"Generated: {len(catalog)} new images")
    print(f"Catalog: {len(merged)} total entries")
    print(f"Paired to posting queue: {sum(1 for i in catalog if i.get('paired_with'))}")
    print(f"Output: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
