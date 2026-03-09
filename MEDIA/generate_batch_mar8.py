#!/usr/bin/env python3
"""
PRINTMAXX Image Factory — Mar 8 Batch
Generates images for alpha_content_2026_03_08.md + approved posts queue + Gumroad covers.
"""

import json
from pathlib import Path
from datetime import datetime
from playwright.sync_api import sync_playwright

BASE_DIR = Path(__file__).parent
TEMPLATES_DIR = BASE_DIR / "image_templates"
OUTPUT_DIR = BASE_DIR / "generated_images"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# ── MAR 8 ALPHA CONTENT: 5 TWEETS ────────────────────────────

STAT_HIGHLIGHTS = [
    {
        "id": "stat_bible_gpt_300k",
        "template": "stat_highlight.html",
        "width": 1200, "height": 675,
        "replacements": {
            ">340<": ">$300K<",
            "customers from reddit. zero ad spend.": "per month MRR. 2-man team. Bible chatbot app.",
            "the trick is not marketing at all. just be useful in the right threads.":
                "2 billion christians with smartphones. most Bible apps built in 2014.",
        },
    },
    {
        "id": "stat_linkedin_15k",
        "template": "stat_highlight.html",
        "width": 1200, "height": 675,
        "replacements": {
            ">340<": ">$15K<",
            "customers from reddit. zero ad spend.": "MRR from LinkedIn only. no cold email. no ads.",
            "the trick is not marketing at all. just be useful in the right threads.":
                "buyer-intent signals baked into the platform. most people use it like a resume.",
        },
    },
    {
        "id": "stat_149m_arr",
        "template": "stat_highlight.html",
        "width": 1200, "height": 675,
        "replacements": {
            ">340<": ">$149M<",
            "customers from reddit. zero ad spend.": "ARR. almost zero customer acquisition cost.",
            "the trick is not marketing at all. just be useful in the right threads.":
                "most founders burn 40-60% on paid acquisition. this company compounds instead.",
        },
    },
    {
        "id": "stat_va_market_55b",
        "template": "stat_highlight.html",
        "width": 1200, "height": 675,
        "replacements": {
            ">340<": ">$55B<",
            "customers from reddit. zero ad spend.": "projected VA market by 2035. currently $19.5B.",
            "the trick is not marketing at all. just be useful in the right threads.":
                "most VAs charge $20/hr. the ones at $150/hr built a pricing ladder.",
        },
    },
    {
        "id": "stat_famewall_1k",
        "template": "stat_highlight.html",
        "width": 1200, "height": 675,
        "replacements": {
            ">340<": ">$1K<",
            "customers from reddit. zero ad spend.": "MRR in 12 months. testimonial SaaS. near-zero churn.",
            "the trick is not marketing at all. just be useful in the right threads.":
                "the market is every single business with a website. AI-generated snippets from raw reviews.",
        },
    },
]


# ── MAR 8 THREAD: RELIGIOUS APP MARKET ────────────────────────

THREAD_CARDS = [
    {
        "id": "thread_religious_apps_mar8",
        "template": "thread_card.html",
        "width": 1200, "height": 675,
        "replacements": {
            "cold email reality check: ran <span class=\"highlight\">464K emails</span> last year.":
                "a 2-man team makes <span class=\"highlight\">$300K/mo</span> from a Bible chatbot.",
            "<div class=\"bullet\">tested every list source</div>":
                "<div class=\"bullet\">2.4B christians, 1.9B muslims, 500M buddhists</div>",
            "<div class=\"bullet\">buying lists is dead</div>":
                "<div class=\"bullet\">most devotional apps have 2-star ratings</div>",
            "<div class=\"bullet\">here's what actually works</div>":
                "<div class=\"bullet\">one template, 15+ denomination versions</div>",
        },
    },
]


# ── SOCIAL CARDS: CROSS-NICHE ADAPTATIONS ─────────────────────

SOCIAL_CARDS = [
    {
        "id": "social_faith_accountability",
        "template": "social_card.html",
        "width": 1200, "height": 675,
        "replacements": {
            "i monitor <span class=\"highlight\">200+ competitor pages</span>. they update something, i know in 30 seconds.":
                "prayer apps with <span class=\"highlight\">social accountability</span> have 4x daily active users vs solo devotional apps.",
            "the system that runs while you sleep":
                "the Romanian team proved the market. the next layer is community.",
        },
    },
    {
        "id": "social_indie_religion",
        "template": "social_card.html",
        "width": 1200, "height": 675,
        "replacements": {
            "i monitor <span class=\"highlight\">200+ competitor pages</span>. they update something, i know in 30 seconds.":
                "<span class=\"highlight\">2 developers. $300K/mo.</span> you're fighting over the same 50 SaaS niches while markets 10x bigger sit wide open.",
            "the system that runs while you sleep":
                "stop building the next project management tool. build for the 2.4B who pray every morning.",
        },
    },
    {
        "id": "social_pricing_ladder",
        "template": "social_card.html",
        "width": 1200, "height": 675,
        "replacements": {
            "i monitor <span class=\"highlight\">200+ competitor pages</span>. they update something, i know in 30 seconds.":
                "same person, same skills, same hours. <span class=\"highlight\">tier 3 makes 5-10x tier 1</span>. the difference isn't the work.",
            "the system that runs while you sleep":
                "hourly → retainer → equity. it's the packaging, not the skill.",
        },
    },
]


# ── QUOTE CARDS (1080x1080 for Instagram/carousel) ───────────

QUOTE_CARDS = [
    {
        "id": "quote_niche_cool_mar8",
        "template": "quote_card.html",
        "width": 1080, "height": 1080,
        "replacements": {
            "stop overthinking this. just set up the alerts and start watching.":
                "what niche are you ignoring because it doesn't seem cool enough?",
        },
    },
    {
        "id": "quote_resume_site_mar8",
        "template": "quote_card.html",
        "width": 1080, "height": 1080,
        "replacements": {
            "stop overthinking this. just set up the alerts and start watching.":
                "LinkedIn has buyer-intent signals baked into the platform. most people use it like a resume site. that's the arbitrage.",
        },
    },
    {
        "id": "quote_1k_mrr_hardest",
        "template": "quote_card.html",
        "width": 1080, "height": 1080,
        "replacements": {
            "stop overthinking this. just set up the alerts and start watching.":
                "$1K MRR is the hardest milestone. everything after that is math.",
        },
    },
    {
        "id": "quote_factory_not_product",
        "template": "quote_card.html",
        "width": 1080, "height": 1080,
        "replacements": {
            "stop overthinking this. just set up the alerts and start watching.":
                "one app concept. 15+ denomination-specific versions. that's not a product. that's a factory.",
        },
    },
]


# ── DATA VIZ: RELIGIOUS APP MARKET ────────────────────────────

DATA_VIZ = [
    {
        "id": "data_viz_religious_market",
        "template": "data_viz.html",
        "width": 1200, "height": 675,
        "replacements": {
            "system status — last 24 hours": "religious app market — untapped",
            "autonomous agent performance dashboard": "5+ billion religious people, most apps haven't been updated since 2021",
            ">27<": ">2.4B<",
            ">Active Agents<": ">Christians<",
            ">+6 today<": ">smartphones<",
            ">142<": ">1.9B<",
            ">Tasks Run<": ">Muslims<",
            ">+38 vs yesterday<": ">daily prayer<",
            ">89%<": ">$300K<",
            ">Success Rate<": ">MRR (Bible GPT)<",
            ">+12% this week<": ">2-man team<",
            ">$0<": ">15+<",
            ">Revenue<": ">Denominations<",
            ">soon<": ">one codebase<",
        },
    },
    {
        "id": "data_viz_va_market",
        "template": "data_viz.html",
        "width": 1200, "height": 675,
        "replacements": {
            "system status — last 24 hours": "VA market — pricing ladder math",
            "autonomous agent performance dashboard": "same skills, different packaging = 5-10x revenue",
            ">27<": ">$20<",
            ">Active Agents<": ">Fiverr Rate<",
            ">+6 today<": ">tier 1<",
            ">142<": ">$5K<",
            ">Tasks Run<": ">Retainer / Mo<",
            ">+38 vs yesterday<": ">tier 2<",
            ">89%<": ">$150<",
            ">Success Rate<": ">Hourly (top)<",
            ">+12% this week<": ">tier 3<",
            ">$0<": ">$55B<",
            ">Revenue<": ">Market 2035<",
            ">soon<": ">from $19.5B<",
        },
    },
]


# ── GUMROAD PRODUCT COVERS (1280x720) ────────────────────────

PRODUCT_COVERS = [
    {
        "id": "cover_local_biz_system",
        "template": "product_cover.html",
        "width": 1280, "height": 720,
        "replacements": {
            "DIGITAL PRODUCT": "CLIENT SYSTEM",
            "73 Cold Email <span class=\"accent\">Subject Lines</span>":
                "Local Biz <span class=\"accent\">Client System</span>",
            "battle-tested subject lines that get 40%+ open rates":
                "scrape, score, and close local business clients on autopilot",
            ">73<": ">500+<",
            ">Subject Lines<": ">Leads / Day<",
            ">40%+<": ">$2.5K<",
            ">Open Rate<": ">Per Client<",
            ">$0<": ">$297<",
            ">Ad Spend<": ">Monthly Cost<",
        },
    },
    {
        "id": "cover_ai_automation_toolkit",
        "template": "product_cover.html",
        "width": 1280, "height": 720,
        "replacements": {
            "DIGITAL PRODUCT": "AUTOMATION KIT",
            "73 Cold Email <span class=\"accent\">Subject Lines</span>":
                "AI Automation <span class=\"accent\">Toolkit</span>",
            "battle-tested subject lines that get 40%+ open rates":
                "292 production scripts. scrapers, agents, pipelines. copy-paste ready.",
            ">73<": ">292<",
            ">Subject Lines<": ">Scripts<",
            ">40%+<": ">25+<",
            ">Open Rate<": ">Agents<",
            ">$0<": ">$0<",
            ">Ad Spend<": ">API Cost<",
        },
    },
    {
        "id": "cover_vibe_coding_playbook",
        "template": "product_cover.html",
        "width": 1280, "height": 720,
        "replacements": {
            "DIGITAL PRODUCT": "PLAYBOOK",
            "73 Cold Email <span class=\"accent\">Subject Lines</span>":
                "Vibe Coding <span class=\"accent\">Playbook</span>",
            "battle-tested subject lines that get 40%+ open rates":
                "ship 10 apps in 30 days with Claude Code. the system, not the tutorial.",
            ">73<": ">10<",
            ">Subject Lines<": ">Apps / Month<",
            ">40%+<": ">$0<",
            ">Open Rate<": ">Code Written<",
            ">$0<": ">22<",
            ">Ad Spend<": ">Apps Shipped<",
        },
    },
    {
        "id": "cover_cold_email_playbook",
        "template": "product_cover.html",
        "width": 1280, "height": 720,
        "replacements": {
            "DIGITAL PRODUCT": "OUTBOUND SYSTEM",
            "73 Cold Email <span class=\"accent\">Subject Lines</span>":
                "Cold Email <span class=\"accent\">Playbook</span>",
            "battle-tested subject lines that get 40%+ open rates":
                "the $297/mo system that replaces $5-10K agencies. 2,500 emails/day.",
            ">73<": ">2,500<",
            ">Subject Lines<": ">Emails / Day<",
            ">40%+<": ">6.8%<",
            ">Open Rate<": ">Reply Rate<",
            ">$0<": ">$297<",
            ">Ad Spend<": ">Monthly Cost<",
        },
    },
    {
        "id": "cover_twitter_growth",
        "template": "product_cover.html",
        "width": 1280, "height": 720,
        "replacements": {
            "DIGITAL PRODUCT": "GROWTH ENGINE",
            "73 Cold Email <span class=\"accent\">Subject Lines</span>":
                "Twitter <span class=\"accent\">Growth Playbook</span>",
            "battle-tested subject lines that get 40%+ open rates":
                "the content factory system. 1 piece becomes 20. automated scheduling.",
            ">73<": ">283<",
            ">Subject Lines<": ">Posts Ready<",
            ">40%+<": ">6<",
            ">Open Rate<": ">Platforms<",
            ">$0<": ">1→20<",
            ">Ad Spend<": ">Content Ratio<",
        },
    },
    {
        "id": "cover_content_farm_blueprint",
        "template": "product_cover.html",
        "width": 1280, "height": 720,
        "replacements": {
            "DIGITAL PRODUCT": "BLUEPRINT",
            "73 Cold Email <span class=\"accent\">Subject Lines</span>":
                "AI Content Farm <span class=\"accent\">Blueprint</span>",
            "battle-tested subject lines that get 40%+ open rates":
                "run 6 niche accounts from one system. automated content generation pipeline.",
            ">73<": ">6<",
            ">Subject Lines<": ">Accounts<",
            ">40%+<": ">1,278<",
            ">Open Rate<": ">Posts Made<",
            ">$0<": ">$0<",
            ">Ad Spend<": ">Marginal Cost<",
        },
    },
    {
        "id": "cover_solopreneur_stack",
        "template": "product_cover.html",
        "width": 1280, "height": 720,
        "replacements": {
            "DIGITAL PRODUCT": "TECH STACK",
            "73 Cold Email <span class=\"accent\">Subject Lines</span>":
                "Solopreneur <span class=\"accent\">Tech Stack</span>",
            "battle-tested subject lines that get 40%+ open rates":
                "the $240/mo toolchain that replaces a $15K/mo team. every tool, every config.",
            ">73<": ">$240<",
            ">Subject Lines<": ">Monthly Cost<",
            ">40%+<": ">33<",
            ">Open Rate<": ">Agents<",
            ">$0<": ">$0<",
            ">Ad Spend<": ">Employees<",
        },
    },
    {
        "id": "cover_sleep_youtube",
        "template": "product_cover.html",
        "width": 1280, "height": 720,
        "replacements": {
            "DIGITAL PRODUCT": "STARTER KIT",
            "73 Cold Email <span class=\"accent\">Subject Lines</span>":
                "Sleep YouTube <span class=\"accent\">Starter Kit</span>",
            "battle-tested subject lines that get 40%+ open rates":
                "faceless YouTube channel kit. rain sounds, lo-fi, ambient. auto-generated.",
            ">73<": ">10<",
            ">Subject Lines<": ">Videos Ready<",
            ">40%+<": ">8hr<",
            ">Open Rate<": ">Per Video<",
            ">$0<": ">$0<",
            ">Ad Spend<": ">Production<",
        },
    },
    {
        "id": "cover_funnel_teardown",
        "template": "product_cover.html",
        "width": 1280, "height": 720,
        "replacements": {
            "DIGITAL PRODUCT": "TEARDOWN GUIDE",
            "73 Cold Email <span class=\"accent\">Subject Lines</span>":
                "Funnel <span class=\"accent\">Teardown Guide</span>",
            "battle-tested subject lines that get 40%+ open rates":
                "9 high-converting funnels dissected. landing pages, email sequences, pricing psychology.",
            ">73<": ">9<",
            ">Subject Lines<": ">Funnels<",
            ">40%+<": ">$50K+<",
            ">Open Rate<": ">Each Earns<",
            ">$0<": ">27<",
            ">Ad Spend<": ">Pages Analyzed<",
        },
    },
    {
        "id": "cover_free_lead_magnet",
        "template": "product_cover.html",
        "width": 1280, "height": 720,
        "replacements": {
            "DIGITAL PRODUCT": "FREE DOWNLOAD",
            "73 Cold Email <span class=\"accent\">Subject Lines</span>":
                "5 AI Prompts That <span class=\"accent\">Save 2hrs/Week</span>",
            "battle-tested subject lines that get 40%+ open rates":
                "copy-paste prompts for content, outreach, research, analysis, and automation.",
            ">73<": ">5<",
            ">Subject Lines<": ">Prompts<",
            ">40%+<": ">2hrs<",
            ">Open Rate<": ">Saved / Week<",
            ">$0<": ">FREE<",
            ">Ad Spend<": ">Price<",
        },
    },
    {
        "id": "cover_cold_email_subjects",
        "template": "product_cover.html",
        "width": 1280, "height": 720,
        "replacements": {},  # Default content matches this product
    },
    {
        "id": "cover_viral_tweet_templates",
        "template": "product_cover.html",
        "width": 1280, "height": 720,
        "replacements": {
            "DIGITAL PRODUCT": "TEMPLATE PACK",
            "73 Cold Email <span class=\"accent\">Subject Lines</span>":
                "Viral Tweet <span class=\"accent\">Templates</span>",
            "battle-tested subject lines that get 40%+ open rates":
                "100 proven tweet formats. hooks, threads, reply bait. fill-in-the-blank.",
            ">73<": ">100<",
            ">Subject Lines<": ">Templates<",
            ">40%+<": ">5%+<",
            ">Open Rate<": ">Engagement<",
            ">$0<": ">6<",
            ">Ad Spend<": ">Niches<",
        },
    },
    {
        "id": "cover_local_biz_emails",
        "template": "product_cover.html",
        "width": 1280, "height": 720,
        "replacements": {
            "DIGITAL PRODUCT": "EMAIL PACK",
            "73 Cold Email <span class=\"accent\">Subject Lines</span>":
                "Local Biz Cold <span class=\"accent\">Email Pack</span>",
            "battle-tested subject lines that get 40%+ open rates":
                "50 industry-specific cold email templates for local business outreach.",
            ">73<": ">50<",
            ">Subject Lines<": ">Templates<",
            ">40%+<": ">12<",
            ">Open Rate<": ">Industries<",
            ">$0<": ">6.8%<",
            ">Ad Spend<": ">Reply Rate<",
        },
    },
]


# ── APPROVED POSTS QUEUE (Mar 7-8 scheduled tweets) ──────────

APPROVED_QUEUE_CARDS = [
    {
        "id": "aq_prayer_apps_mar8",
        "template": "stat_highlight.html",
        "width": 1200, "height": 675,
        "replacements": {
            ">340<": ">13<",
            "customers from reddit. zero ad spend.": "denomination-specific apps. the corner nobody looked at.",
            "the trick is not marketing at all. just be useful in the right threads.":
                "Hallow: Catholic only. $33.4M/year. not a single app for Orthodox, Lutheran, or Sikh.",
        },
    },
    {
        "id": "aq_hevy_600k",
        "template": "stat_highlight.html",
        "width": 1200, "height": 675,
        "replacements": {
            ">340<": ">$600K<",
            "customers from reddit. zero ad spend.": "per month. bootstrapped workout tracker. zero VC money.",
            "the trick is not marketing at all. just be useful in the right threads.":
                "if a workout tracker can do $7.2M/year with no funding, your niche app can do $5K/month.",
        },
    },
    {
        "id": "aq_kelly_criterion",
        "template": "stat_highlight.html",
        "width": 1200, "height": 675,
        "replacements": {
            ">340<": ">87.4%<",
            "customers from reddit. zero ad spend.": "margins on cold outbound. $2.5K-$5K per client.",
            "the trick is not marketing at all. just be useful in the right threads.":
                "one client = 250 gumroad sales. most indie hackers avoid it because it feels salesy.",
        },
    },
    {
        "id": "aq_gumroad_vs_whop",
        "template": "stat_highlight.html",
        "width": 1200, "height": 675,
        "replacements": {
            ">340<": ">73%<",
            "customers from reddit. zero ad spend.": "lower fees on Whop vs Gumroad. $900/year difference.",
            "the trick is not marketing at all. just be useful in the right threads.":
                "Gumroad: 10% + $0.50. Whop: 2.7% + $0.30. on $1K/month that's $105 vs $30.",
        },
    },
    {
        "id": "aq_8_projects_pipeline",
        "template": "social_card.html",
        "width": 1200, "height": 675,
        "replacements": {
            "i monitor <span class=\"highlight\">200+ competitor pages</span>. they update something, i know in 30 seconds.":
                "connected <span class=\"highlight\">8 indie projects</span> into one data pipeline. 58 items wired across 9 connections.",
            "the system that runs while you sleep":
                "competitor updates become tweets. reddit posts become leads. zero wasted output.",
        },
    },
    {
        "id": "aq_abandoned_apps",
        "template": "social_card.html",
        "width": 1200, "height": 675,
        "replacements": {
            "i monitor <span class=\"highlight\">200+ competitor pages</span>. they update something, i know in 30 seconds.":
                "found <span class=\"highlight\">2 abandoned apps</span> with thousands of active users. last updated 2019-2020.",
            "the system that runs while you sleep":
                "abandoned apps with active users = free product specs. read their 1-star reviews.",
        },
    },
    {
        "id": "aq_building_vs_selling",
        "template": "social_card.html",
        "width": 1200, "height": 675,
        "replacements": {
            "i monitor <span class=\"highlight\">200+ competitor pages</span>. they update something, i know in 30 seconds.":
                "building 14 apps is easier than listing 1 product on gumroad. <span class=\"highlight\">building feels productive. selling feels vulnerable.</span>",
            "the system that runs while you sleep":
                "your github has more commits than your stripe has charges.",
        },
    },
    {
        "id": "aq_ai_agents_worse",
        "template": "social_card.html",
        "width": 1200, "height": 675,
        "replacements": {
            "i monitor <span class=\"highlight\">200+ competitor pages</span>. they update something, i know in 30 seconds.":
                "AI agents made me <span class=\"highlight\">worse at business</span>. before: built 1 thing, sold it. after: built 131 things, sold nothing.",
            "the system that runs while you sleep":
                "the speed increase made me skip the hard part. technology solved the wrong problem.",
        },
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
    print("PRINTMAXX Image Factory — Mar 8 Batch")
    print("=" * 55)
    print(f"Templates: {TEMPLATES_DIR}")
    print(f"Output: {OUTPUT_DIR}")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        catalog = []

        categories = [
            ("Alpha Tweet Cards (1200x675)", STAT_HIGHLIGHTS),
            ("Thread Cards (1200x675)", THREAD_CARDS),
            ("Cross-Niche Social Cards (1200x675)", SOCIAL_CARDS),
            ("Quote Cards (1080x1080)", QUOTE_CARDS),
            ("Data Viz (1200x675)", DATA_VIZ),
            ("Gumroad Product Covers (1280x720)", PRODUCT_COVERS),
            ("Approved Queue Cards (1200x675)", APPROVED_QUEUE_CARDS),
        ]

        total = sum(len(items) for _, items in categories)
        generated = 0
        failed = 0

        for cat_name, items in categories:
            print(f"\n{cat_name} ({len(items)} images)")
            print("-" * 50)
            for item in items:
                try:
                    result = generate_image(page, item)
                    result["category"] = cat_name
                    result["template"] = item["template"]
                    result["generated_at"] = datetime.now().isoformat()
                    catalog.append(result)
                    generated += 1
                except Exception as e:
                    print(f'  [FAIL] {item["id"]}: {e}')
                    failed += 1

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
    print(f"Generated: {generated}/{total} images ({failed} failed)")
    print(f"Catalog: {len(merged)} total entries")
    print(f"Output: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
