#!/usr/bin/env python3
"""
PRINTMAXX Image Factory — Mar 7 Batch Wave 2
Generates images for mar8_1430 through mar16_1800 scheduled tweets.
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


ALL_IMAGES = [
    # ── MAR 8 (remaining) ─────────────────────────
    {
        "id": "social_mcp_servers",
        "template": "social_card.html",
        "width": 1200, "height": 675,
        "replacements": {
            "i monitor <span class=\"highlight\">200+ competitor pages</span>. they update something, i know in 30 seconds.":
                "MCP multi-server automation. one instruction hits <span class=\"highlight\">6 different tools</span> simultaneously.",
            "the system that runs while you sleep":
                "it's borderline illegal how much this saves you.",
        },
        "pair_with": "twitter_PRINTMAXXER_mar8_1430.txt",
    },
    {
        "id": "social_n8n_free",
        "template": "social_card.html",
        "width": 1200, "height": 675,
        "replacements": {
            "i monitor <span class=\"highlight\">200+ competitor pages</span>. they update something, i know in 30 seconds.":
                "n8n for AI-native workflow automation. <span class=\"highlight\">self-hosted. free.</span> runs every pipeline we have.",
            "the system that runs while you sleep":
                "if you're paying for zapier you're leaving money on the table.",
        },
        "pair_with": "twitter_PRINTMAXXER_mar8_1800.txt",
    },

    # ── MAR 9 ──────────────────────────────────────
    {
        "id": "social_browser_ai",
        "template": "social_card.html",
        "width": 1200, "height": 675,
        "replacements": {
            "i monitor <span class=\"highlight\">200+ competitor pages</span>. they update something, i know in 30 seconds.":
                "no-code browser automation via AI. record a workflow once, the agent runs it <span class=\"highlight\">1000 times</span>.",
            "the system that runs while you sleep":
                "price monitoring, lead scraping, form filling. zero code.",
        },
        "pair_with": "twitter_PRINTMAXXER_mar9_0730.txt",
    },
    {
        "id": "stat_1bit_llm",
        "template": "stat_highlight.html",
        "width": 1200, "height": 675,
        "replacements": {
            ">340<": ">$0<",
            "customers from reddit. zero ad spend.": "API cost for local LLM inference.",
            "the trick is not marketing at all. just be useful in the right threads.":
                "1-bit LLMs run full pipelines on a laptop. no rate limits. the cost curve just collapsed.",
        },
        "pair_with": "twitter_PRINTMAXXER_mar9_1100.txt",
    },
    {
        "id": "stat_1_to_20",
        "template": "stat_highlight.html",
        "width": 1200, "height": 675,
        "replacements": {
            ">340<": ">1:20<",
            "customers from reddit. zero ad spend.": "content multiplication ratio.",
            "the trick is not marketing at all. just be useful in the right threads.":
                "one piece of content. AI turns it into 20. twitter, linkedin, youtube, email, reddit.",
        },
        "pair_with": "twitter_PRINTMAXXER_mar9_1430.txt",
    },
    {
        "id": "stat_tiktok_10x",
        "template": "stat_highlight.html",
        "width": 1200, "height": 675,
        "replacements": {
            ">340<": ">10x<",
            "customers from reddit. zero ad spend.": "TikTok creator rewards vs AdSense per view.",
            "the trick is not marketing at all. just be useful in the right threads.":
                "stacked model: platform revenue + brand deals + affiliate. most people only run one.",
        },
        "pair_with": "twitter_PRINTMAXXER_mar9_1800.txt",
    },

    # ── MAR 10 ─────────────────────────────────────
    {
        "id": "stat_first_200",
        "template": "stat_highlight.html",
        "width": 1200, "height": 675,
        "replacements": {
            ">340<": ">200<",
            "customers from reddit. zero ad spend.": "first TikTok followers determine distribution.",
            "the trick is not marketing at all. just be useful in the right threads.":
                "bad early audience = dead reach permanently. fix this before you post another video.",
        },
        "pair_with": "twitter_PRINTMAXXER_mar10_0730.txt",
    },
    {
        "id": "stat_first_hour",
        "template": "stat_highlight.html",
        "width": 1200, "height": 675,
        "replacements": {
            ">340<": ">60<",
            "customers from reddit. zero ad spend.": "minutes that determine TikTok distribution.",
            "the trick is not marketing at all. just be useful in the right threads.":
                "10 real comments in the first hour. that's the active creator signal.",
        },
        "pair_with": "twitter_PRINTMAXXER_mar10_1100.txt",
    },
    {
        "id": "stat_50_60_seconds",
        "template": "stat_highlight.html",
        "width": 1200, "height": 675,
        "replacements": {
            ">340<": ">50-60s<",
            "customers from reddit. zero ad spend.": "the exact range for YouTube Shorts indexing.",
            "the trick is not marketing at all. just be useful in the right threads.":
                "under that: feed only. over that: search only. pick one goal and hit the right range.",
        },
        "pair_with": "twitter_PRINTMAXXER_mar10_1430.txt",
    },
    {
        "id": "stat_18_22_shorts",
        "template": "stat_highlight.html",
        "width": 1200, "height": 675,
        "replacements": {
            ">340<": ">18-22<",
            "customers from reddit. zero ad spend.": "Shorts per month. the optimal cadence.",
            "the trick is not marketing at all. just be useful in the right threads.":
                "not 5. not 60. trending audio in the first 5 seconds. this is the playbook.",
        },
        "pair_with": "twitter_PRINTMAXXER_mar10_1800.txt",
    },

    # ── MAR 11 ─────────────────────────────────────
    {
        "id": "social_ig_dm_shares",
        "template": "social_card.html",
        "width": 1200, "height": 675,
        "replacements": {
            "i monitor <span class=\"highlight\">200+ competitor pages</span>. they update something, i know in 30 seconds.":
                "IG DM shares are now the <span class=\"highlight\">#1 priority metric</span>. not likes. not comments.",
            "the system that runs while you sleep":
                "the algorithm reads this as high-trust content. design every post to be DM-share-worthy.",
        },
        "pair_with": "twitter_PRINTMAXXER_mar11_0730.txt",
    },
    {
        "id": "social_ig_originality",
        "template": "social_card.html",
        "width": 1200, "height": 675,
        "replacements": {
            "i monitor <span class=\"highlight\">200+ competitor pages</span>. they update something, i know in 30 seconds.":
                "IG Originality Score <span class=\"highlight\">penalizes TikTok reposts</span>. always remove watermarks.",
            "the system that runs while you sleep":
                "IG is filtering content farms. original content gets massive reach advantage.",
        },
        "pair_with": "twitter_PRINTMAXXER_mar11_1100.txt",
    },
    {
        "id": "social_ai_cicd",
        "template": "social_card.html",
        "width": 1200, "height": 675,
        "replacements": {
            "i monitor <span class=\"highlight\">200+ competitor pages</span>. they update something, i know in 30 seconds.":
                "AI CI/CD: push code, agent tests, stages, deploys, monitors, <span class=\"highlight\">rolls back if needed</span>.",
            "the system that runs while you sleep":
                "zero human in the loop after the push. shipping velocity 3x.",
        },
        "pair_with": "twitter_PRINTMAXXER_mar11_1430.txt",
    },
    {
        "id": "social_6_questions",
        "template": "social_card.html",
        "width": 1200, "height": 675,
        "replacements": {
            "i monitor <span class=\"highlight\">200+ competitor pages</span>. they update something, i know in 30 seconds.":
                "<span class=\"highlight\">6 qualifying questions</span>, all answered in under 100 words. that's the cold email stack.",
            "the system that runs while you sleep":
                "what you do. who for. how. problem solved. proof. ROI.",
        },
        "pair_with": "twitter_PRINTMAXXER_mar11_1800.txt",
    },

    # ── MAR 12 ─────────────────────────────────────
    {
        "id": "stat_58pct_first",
        "template": "stat_highlight.html",
        "width": 1200, "height": 675,
        "replacements": {
            ">340<": ">58%<",
            "customers from reddit. zero ad spend.": "of cold email replies come from the first email.",
            "the trick is not marketing at all. just be useful in the right threads.":
                "4-6 lines. no tracking pixels. mention their tech stack. that's it.",
        },
        "pair_with": "twitter_PRINTMAXXER_mar12_0730.txt",
    },
    {
        "id": "stat_ai_apps_40pct",
        "template": "stat_highlight.html",
        "width": 1200, "height": 675,
        "replacements": {
            ">340<": ">40%<",
            "customers from reddit. zero ad spend.": "better conversion for AI apps vs non-AI.",
            "the trick is not marketing at all. just be useful in the right threads.":
                "but they churn 30% faster. build conversion like AI, retention like non-AI.",
        },
        "pair_with": "twitter_PRINTMAXXER_mar12_1100.txt",
    },
    {
        "id": "stat_680m_citations",
        "template": "stat_highlight.html",
        "width": 1200, "height": 675,
        "replacements": {
            ">340<": ">680M<",
            "customers from reddit. zero ad spend.": "citations analyzed. GEO is eating SEO alive.",
            "the trick is not marketing at all. just be useful in the right threads.":
                "43% more brands cited by ChatGPT in 2026. $750B routes through AI discovery.",
        },
        "pair_with": "twitter_PRINTMAXXER_mar12_1430.txt",
    },
    {
        "id": "stat_pricing_2_4x",
        "template": "stat_highlight.html",
        "width": 1200, "height": 675,
        "replacements": {
            ">340<": ">2-4x<",
            "customers from reddit. zero ad spend.": "more impact from pricing vs customer acquisition.",
            "the trick is not marketing at all. just be useful in the right threads.":
                "credit-based models grew 126% YoY. stop charging per seat. start charging per result.",
        },
        "pair_with": "twitter_PRINTMAXXER_mar12_1800.txt",
    },

    # ── MAR 13 ─────────────────────────────────────
    {
        "id": "social_hub_spoke_model",
        "template": "social_card.html",
        "width": 1200, "height": 675,
        "replacements": {
            "i monitor <span class=\"highlight\">200+ competitor pages</span>. they update something, i know in 30 seconds.":
                "1 piece of content should become <span class=\"highlight\">20</span>. every single time. hub-and-spoke model.",
            "the system that runs while you sleep":
                "same content, different packaging. AI handles the transformation.",
        },
        "pair_with": "twitter_PRINTMAXXER_mar13_0730.txt",
    },
    {
        "id": "quote_building_vs_selling",
        "template": "quote_card.html",
        "width": 1080, "height": 1080,
        "replacements": {
            "stop overthinking this. just set up the alerts and start watching.":
                "what's more dangerous for a solopreneur? building too much or selling too little? it's always both.",
        },
        "pair_with": "twitter_PRINTMAXXER_mar13_1100.txt",
    },
    {
        "id": "quote_confession",
        "template": "quote_card.html",
        "width": 1080, "height": 1080,
        "replacements": {
            "stop overthinking this. just set up the alerts and start watching.":
                "confession: i automated everything except the one thing that makes money. how many of you are sitting on products you haven't listed?",
        },
        "pair_with": "twitter_PRINTMAXXER_mar13_1430.txt",
    },
    {
        "id": "quote_bip_hot_take",
        "template": "quote_card.html",
        "width": 1080, "height": 1080,
        "replacements": {
            "stop overthinking this. just set up the alerts and start watching.":
                "hot take: most 'build in public' accounts are actually 'procrastinate in public' accounts. nobody wants to hear 'i uploaded 3 PDFs to gumroad today.' but that's the post that leads to revenue.",
        },
        "pair_with": "twitter_PRINTMAXXER_mar13_1800.txt",
    },

    # ── MAR 14 ─────────────────────────────────────
    {
        "id": "stat_2_to_11_reply",
        "template": "stat_highlight.html",
        "width": 1200, "height": 675,
        "replacements": {
            ">340<": ">11%<",
            "customers from reddit. zero ad spend.": "reply rate after cutting email to 60 words.",
            "the trick is not marketing at all. just be useful in the right threads.":
                "up from 2%. shorter is not lazier. shorter wins.",
        },
        "pair_with": "twitter_PRINTMAXXER_mar14_0730.txt",
    },
    {
        "id": "social_1000_visitors",
        "template": "social_card.html",
        "width": 1200, "height": 675,
        "replacements": {
            "i monitor <span class=\"highlight\">200+ competitor pages</span>. they update something, i know in 30 seconds.":
                "<span class=\"highlight\">1000 visitors. 0 sales.</span> the traffic isn't the problem. the offer is.",
            "the system that runs while you sleep":
                "fix the conversion first. spending more to find out faster that the offer is broken isn't a strategy.",
        },
        "pair_with": "twitter_PRINTMAXXER_mar14_1100.txt",
    },
    {
        "id": "social_cold_calc",
        "template": "social_card.html",
        "width": 1200, "height": 675,
        "replacements": {
            "i monitor <span class=\"highlight\">200+ competitor pages</span>. they update something, i know in 30 seconds.":
                "built a cold email calculator. input close rate, deal size, goal. <span class=\"highlight\">it does the math</span>.",
            "the system that runs while you sleep":
                "free at cold-email-calc.surge.sh",
        },
        "pair_with": "twitter_PRINTMAXXER_mar14_1430.txt",
    },
    {
        "id": "stat_7_pwas_zero",
        "template": "stat_highlight.html",
        "width": 1200, "height": 675,
        "replacements": {
            ">340<": ">7<",
            "customers from reddit. zero ad spend.": "PWA apps shipped in 30 days. total cost: $0.",
            "the trick is not marketing at all. just be useful in the right threads.":
                "zero app store fees. zero review wait. deployed in hours not weeks.",
        },
        "pair_with": "twitter_PRINTMAXXER_mar14_1800.txt",
    },

    # ── MAR 15 ─────────────────────────────────────
    {
        "id": "stat_38_vs_9_subject",
        "template": "stat_highlight.html",
        "width": 1200, "height": 675,
        "replacements": {
            ">340<": ">38%<",
            "customers from reddit. zero ad spend.": "open rate for 'quick question' vs 9% for 'partnership opportunity'.",
            "the trick is not marketing at all. just be useful in the right threads.":
                "2 words. same list. 4x difference. test subject lines before you blame the list.",
        },
        "pair_with": "twitter_PRINTMAXXER_mar15_0730.txt",
    },
    {
        "id": "quote_two_types",
        "template": "quote_card.html",
        "width": 1080, "height": 1080,
        "replacements": {
            "stop overthinking this. just set up the alerts and start watching.":
                "there are 2 types of builders: ones who ship and ask for feedback. ones who polish and never ship. the first group wins every time, even when the product is worse.",
        },
        "pair_with": "twitter_PRINTMAXXER_mar15_1100.txt",
    },
    {
        "id": "social_focuslock_promo",
        "template": "social_card.html",
        "width": 1200, "height": 675,
        "replacements": {
            "i monitor <span class=\"highlight\">200+ competitor pages</span>. they update something, i know in 30 seconds.":
                "focuslock blocks every distraction site. no password bypass. <span class=\"highlight\">shipped 3x more</span> this week.",
            "the system that runs while you sleep":
                "90-minute deep work blocks. focuslock-app.surge.sh",
        },
        "pair_with": "twitter_PRINTMAXXER_mar15_1430.txt",
    },
    {
        "id": "social_audit_tool",
        "template": "social_card.html",
        "width": 1200, "height": 675,
        "replacements": {
            "i monitor <span class=\"highlight\">200+ competitor pages</span>. they update something, i know in 30 seconds.":
                "paste any URL, get pagespeed score, broken links, meta issues in <span class=\"highlight\">under 10 seconds</span>.",
            "the system that runs while you sleep":
                "built in 4 hours. free. website-audit-tool.surge.sh",
        },
        "pair_with": "twitter_PRINTMAXXER_mar15_1800.txt",
    },

    # ── MAR 16 ─────────────────────────────────────
    {
        "id": "stat_prayerlock_200",
        "template": "stat_highlight.html",
        "width": 1200, "height": 675,
        "replacements": {
            ">340<": ">200<",
            "customers from reddit. zero ad spend.": "installs for prayerlock. zero paid ads.",
            "the trick is not marketing at all. just be useful in the right threads.":
                "3 reddit posts, 1 facebook group, 2 tweets. 45 minutes of promotion total.",
        },
        "pair_with": "twitter_PRINTMAXXER_mar16_0730.txt",
    },
    {
        "id": "quote_90pct_teach",
        "template": "quote_card.html",
        "width": 1080, "height": 1080,
        "replacements": {
            "stop overthinking this. just set up the alerts and start watching.":
                "90% of solopreneur content is people teaching what they read, not what they built. follow the 10% who actually shipped something.",
        },
        "pair_with": "twitter_PRINTMAXXER_mar16_1100.txt",
    },
    {
        "id": "social_coldmaxx_promo",
        "template": "social_card.html",
        "width": 1200, "height": 675,
        "replacements": {
            "i monitor <span class=\"highlight\">200+ competitor pages</span>. they update something, i know in 30 seconds.":
                "3 of my 5 cold email sequences were <span class=\"highlight\">dead weight</span>. kept running them for 2 weeks.",
            "the system that runs while you sleep":
                "coldmaxx shows which sequences convert and which to kill. coldmaxx-app.surge.sh",
        },
        "pair_with": "twitter_PRINTMAXXER_mar16_1430.txt",
    },
    {
        "id": "social_32_agents_overnight",
        "template": "social_card.html",
        "width": 1200, "height": 675,
        "replacements": {
            "i monitor <span class=\"highlight\">200+ competitor pages</span>. they update something, i know in 30 seconds.":
                "<span class=\"highlight\">32 autonomous agents</span> running 24/7 across 8 ventures. scrape, generate, audit, route.",
            "the system that runs while you sleep":
                "the overnight output is borderline illegal.",
        },
        "pair_with": "twitter_PRINTMAXXER_mar16_1800.txt",
    },
]


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
    print("PRINTMAXX Image Factory — Mar 7 Batch (Wave 2)")
    print("=" * 55)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        catalog = []

        for item in ALL_IMAGES:
            try:
                result = generate_image(page, item)
                result["category"] = "Scheduled Tweet Images"
                result["template"] = item["template"]
                result["generated_at"] = datetime.now().isoformat()
                if item.get("pair_with"):
                    result["paired_with"] = item["pair_with"]
                catalog.append(result)
            except Exception as e:
                print(f'  [FAIL] {item["id"]}: {e}')

        browser.close()

    # Merge into catalog
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
    print(f"Paired: {sum(1 for i in catalog if i.get('paired_with'))}")

    # Update posting queue .txt files to reference images
    paired_count = 0
    for item in ALL_IMAGES:
        pw = item.get("pair_with")
        if not pw:
            continue
        txt_path = POSTING_QUEUE / pw
        if not txt_path.exists():
            continue
        content = txt_path.read_text()
        if "IMAGE: none" in content:
            img_name = Path(pw).stem + ".png"
            content = content.replace("IMAGE: none", f"IMAGE: {img_name}")
            txt_path.write_text(content)
            paired_count += 1
            print(f"  [UPDATED] {pw} -> {img_name}")

    print(f"Updated {paired_count} posting queue files with image references")


if __name__ == "__main__":
    main()
