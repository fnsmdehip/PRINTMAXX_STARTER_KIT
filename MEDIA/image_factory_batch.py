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

    # === VIDEO THUMBNAILS (1200x675) ===
    {
        "id": "vid_thumb_ai_agents_33",
        "width": 1200, "height": 675,
        "category": "Video Thumbnails (1200x675)",
        "template": "custom",
        "html_fn": lambda: """<!DOCTYPE html>
<html><head><meta charset="utf-8"><style>
* { margin: 0; padding: 0; box-sizing: border-box; }
body {
    width: 1200px; height: 675px;
    background: linear-gradient(135deg, #0a0a0a 0%, #0f0f1a 50%, #0a0a0a 100%);
    font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', 'Inter', sans-serif;
    color: #fff; display: flex; flex-direction: column; justify-content: center;
    padding: 80px; overflow: hidden; position: relative;
}
.grid-overlay {
    position: absolute; top: 0; left: 0; right: 0; bottom: 0;
    background-image: linear-gradient(rgba(102,126,234,0.03) 1px, transparent 1px),
        linear-gradient(90deg, rgba(102,126,234,0.03) 1px, transparent 1px);
    background-size: 40px 40px;
}
.big-number {
    font-size: 140px; font-weight: 900;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #667eea 100%);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    line-height: 1; letter-spacing: -4px; margin-bottom: 12px; position: relative; z-index: 1;
}
.context {
    font-size: 38px; font-weight: 700; line-height: 1.3; max-width: 900px;
    margin-bottom: 16px; position: relative; z-index: 1;
}
.detail {
    font-size: 20px; font-weight: 400; color: rgba(255,255,255,0.4);
    max-width: 700px; line-height: 1.5; position: relative; z-index: 1;
}
.brand {
    position: absolute; bottom: 35px; right: 55px; font-size: 16px;
    font-weight: 700; color: rgba(255,255,255,0.15); letter-spacing: 4px;
    text-transform: uppercase; z-index: 1;
}
.glow {
    position: absolute; top: 50%; left: -80px; transform: translateY(-50%);
    width: 300px; height: 300px;
    background: radial-gradient(circle, rgba(102,126,234,0.08) 0%, transparent 70%);
    border-radius: 50%;
}
.stat-row {
    display: flex; gap: 48px; margin-top: 24px; position: relative; z-index: 1;
}
.stat-item { display: flex; flex-direction: column; }
.stat-val {
    font-size: 24px; font-weight: 800;
    background: linear-gradient(90deg, #667eea, #764ba2);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
}
.stat-label {
    font-size: 12px; color: rgba(255,255,255,0.3); text-transform: uppercase;
    letter-spacing: 1.5px; margin-top: 4px;
}
</style></head><body>
<div class="grid-overlay"></div>
<div class="glow"></div>
<div class="big-number">33</div>
<div class="context">AI agents running 24/7. $200/mo.</div>
<div class="detail">no team. no office. no VC. just Claude Code and a figure-it-the-fuck-out attitude.</div>
<div class="stat-row">
    <div class="stat-item"><div class="stat-val">287</div><div class="stat-label">Scripts</div></div>
    <div class="stat-item"><div class="stat-val">262</div><div class="stat-label">Sites</div></div>
    <div class="stat-item"><div class="stat-val">22</div><div class="stat-label">Apps</div></div>
</div>
<div class="brand">PRINTMAXX</div>
</body></html>""",
    },
    {
        "id": "vid_thumb_gumroad_vs_whop",
        "width": 1200, "height": 675,
        "category": "Video Thumbnails (1200x675)",
        "template": "custom",
        "html_fn": lambda: """<!DOCTYPE html>
<html><head><meta charset="utf-8"><style>
* { margin: 0; padding: 0; box-sizing: border-box; }
body {
    width: 1200px; height: 675px;
    background: linear-gradient(135deg, #0a0a0a 0%, #1a0a0a 50%, #0a0a1a 100%);
    font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', 'Inter', sans-serif;
    color: #fff; display: flex; align-items: center; justify-content: center;
    overflow: hidden; position: relative;
}
.vs-container { display: flex; align-items: center; gap: 60px; z-index: 1; }
.platform { display: flex; flex-direction: column; align-items: center; width: 340px; }
.platform-name { font-size: 48px; font-weight: 800; margin-bottom: 24px; letter-spacing: -1px; }
.platform-stat { font-size: 16px; color: rgba(255,255,255,0.5); margin-bottom: 8px; text-align: center; line-height: 1.6; }
.platform-stat strong { color: #fff; font-weight: 700; }
.loser .platform-name { color: #ef4444; }
.loser .platform-stat strong { color: #ef4444; }
.winner .platform-name {
    background: linear-gradient(90deg, #22c55e, #4ade80);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
}
.winner .platform-stat strong { color: #22c55e; }
.vs { font-size: 72px; font-weight: 900; color: rgba(255,255,255,0.1); letter-spacing: -2px; }
.verdict {
    position: absolute; bottom: 50px; left: 0; right: 0; text-align: center;
    font-size: 22px; font-weight: 600; color: rgba(255,255,255,0.5); z-index: 1;
}
.verdict span { color: #22c55e; font-weight: 800; }
.brand {
    position: absolute; bottom: 35px; right: 55px; font-size: 16px;
    font-weight: 700; color: rgba(255,255,255,0.15); letter-spacing: 4px;
    text-transform: uppercase; z-index: 1;
}
.glow-red {
    position: absolute; top: 30%; left: 10%; width: 250px; height: 250px;
    background: radial-gradient(circle, rgba(239,68,68,0.06) 0%, transparent 70%); border-radius: 50%;
}
.glow-green {
    position: absolute; top: 30%; right: 10%; width: 250px; height: 250px;
    background: radial-gradient(circle, rgba(34,197,94,0.06) 0%, transparent 70%); border-radius: 50%;
}
</style></head><body>
<div class="glow-red"></div><div class="glow-green"></div>
<div class="vs-container">
    <div class="platform loser">
        <div class="platform-name">Gumroad</div>
        <div class="platform-stat"><strong>10% + $0.50</strong> per sale</div>
        <div class="platform-stat"><strong>-48</strong> merchants in 90 days</div>
        <div class="platform-stat">no affiliate network</div>
    </div>
    <div class="vs">VS</div>
    <div class="platform winner">
        <div class="platform-name">Whop</div>
        <div class="platform-stat"><strong>5.7%</strong> flat fee</div>
        <div class="platform-stat"><strong>30K</strong> affiliates sell for you</div>
        <div class="platform-stat"><strong>$1.6B</strong> valuation</div>
    </div>
</div>
<div class="verdict">the platform war is over. <span>whop wins.</span></div>
<div class="brand">PRINTMAXX</div>
</body></html>""",
    },
    {
        "id": "vid_thumb_vibecoding_superbowl",
        "width": 1200, "height": 675,
        "category": "Video Thumbnails (1200x675)",
        "template": "custom",
        "html_fn": lambda: """<!DOCTYPE html>
<html><head><meta charset="utf-8"><style>
* { margin: 0; padding: 0; box-sizing: border-box; }
body {
    width: 1200px; height: 675px;
    background: linear-gradient(135deg, #0a0a0a 0%, #0f0f1a 50%, #0a0a0a 100%);
    font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', 'Inter', sans-serif;
    color: #fff; display: flex; flex-direction: column; justify-content: center;
    padding: 80px; overflow: hidden; position: relative;
}
.grid-overlay {
    position: absolute; top: 0; left: 0; right: 0; bottom: 0;
    background-image: linear-gradient(rgba(102,126,234,0.03) 1px, transparent 1px),
        linear-gradient(90deg, rgba(102,126,234,0.03) 1px, transparent 1px);
    background-size: 40px 40px;
}
.big-number {
    font-size: 120px; font-weight: 900;
    background: linear-gradient(135deg, #f59e0b 0%, #ef4444 50%, #f59e0b 100%);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    line-height: 1; letter-spacing: -4px; margin-bottom: 12px; position: relative; z-index: 1;
}
.context { font-size: 36px; font-weight: 700; line-height: 1.3; max-width: 900px; margin-bottom: 16px; position: relative; z-index: 1; }
.context .dim { color: rgba(255,255,255,0.4); }
.detail { font-size: 20px; font-weight: 400; color: rgba(255,255,255,0.4); max-width: 700px; line-height: 1.5; position: relative; z-index: 1; }
.brand { position: absolute; bottom: 35px; right: 55px; font-size: 16px; font-weight: 700; color: rgba(255,255,255,0.15); letter-spacing: 4px; text-transform: uppercase; z-index: 1; }
.glow { position: absolute; top: 40%; right: -50px; width: 350px; height: 350px; background: radial-gradient(circle, rgba(245,158,11,0.06) 0%, transparent 70%); border-radius: 50%; }
</style></head><body>
<div class="grid-overlay"></div><div class="glow"></div>
<div class="big-number">$7B</div>
<div class="context">vibe coding market. <span class="dim">they spent millions on a Super Bowl ad.</span></div>
<div class="detail">i built 22 apps for $200/mo. 33 agents. 262 sites. one MacBook. this is the other side.</div>
<div class="brand">PRINTMAXX</div>
</body></html>""",
    },
    {
        "id": "vid_thumb_platform_shifts",
        "width": 1200, "height": 675,
        "category": "Video Thumbnails (1200x675)",
        "template": "custom",
        "html_fn": lambda: """<!DOCTYPE html>
<html><head><meta charset="utf-8"><style>
* { margin: 0; padding: 0; box-sizing: border-box; }
body {
    width: 1200px; height: 675px;
    background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 50%, #16213e 100%);
    font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', 'Inter', sans-serif;
    color: #fff; display: flex; flex-direction: column; justify-content: center;
    padding: 80px; overflow: hidden; position: relative;
}
.accent-bar { width: 60px; height: 4px; background: linear-gradient(90deg, #ef4444, #f59e0b); border-radius: 2px; margin-bottom: 32px; }
.hook { font-size: 52px; font-weight: 800; line-height: 1.15; letter-spacing: -1px; margin-bottom: 32px; max-width: 900px; }
.hook .highlight { background: linear-gradient(90deg, #ef4444, #f59e0b); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
.shifts { display: flex; flex-direction: column; gap: 8px; position: relative; z-index: 1; }
.shift-item { font-size: 17px; color: rgba(255,255,255,0.55); display: flex; align-items: center; gap: 12px; }
.shift-num { font-weight: 800; font-size: 14px; color: rgba(255,255,255,0.2); min-width: 24px; }
.shift-item strong { color: rgba(255,255,255,0.85); font-weight: 600; }
.brand { position: absolute; bottom: 35px; right: 55px; font-size: 16px; font-weight: 700; color: rgba(255,255,255,0.15); letter-spacing: 4px; text-transform: uppercase; z-index: 1; }
</style></head><body>
<div class="accent-bar"></div>
<div class="hook"><span class="highlight">5 platform shifts</span> costing you money right now</div>
<div class="shifts">
    <div class="shift-item"><span class="shift-num">01</span><strong>Whop</strong> hit $1.6B. 30K affiliates.</div>
    <div class="shift-item"><span class="shift-num">02</span><strong>Gumroad</strong> lost 48 merchants in 90 days.</div>
    <div class="shift-item"><span class="shift-num">03</span><strong>X Free</strong> is dead. 0% link engagement.</div>
    <div class="shift-item"><span class="shift-num">04</span><strong>Vibe Marketplace</strong> by Greta. new channel.</div>
    <div class="shift-item"><span class="shift-num">05</span><strong>Reddit monitoring</strong> = $12K validated revenue.</div>
</div>
<div class="brand">PRINTMAXX</div>
</body></html>""",
    },
    {
        "id": "vid_thumb_ai_babysitting",
        "width": 1200, "height": 675,
        "category": "Video Thumbnails (1200x675)",
        "template": "custom",
        "html_fn": lambda: """<!DOCTYPE html>
<html><head><meta charset="utf-8"><style>
* { margin: 0; padding: 0; box-sizing: border-box; }
body {
    width: 1200px; height: 675px;
    background: linear-gradient(135deg, #0a0a0a 0%, #0a1a0a 50%, #0a0a0a 100%);
    font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', 'Inter', sans-serif;
    color: #fff; display: flex; flex-direction: column; justify-content: center;
    padding: 80px; overflow: hidden; position: relative;
}
.grid-overlay {
    position: absolute; top: 0; left: 0; right: 0; bottom: 0;
    background-image: linear-gradient(rgba(34,197,94,0.03) 1px, transparent 1px),
        linear-gradient(90deg, rgba(34,197,94,0.03) 1px, transparent 1px);
    background-size: 40px 40px;
}
.quote-mark { font-size: 100px; font-weight: 900; color: rgba(34,197,94,0.15); line-height: 0.6; margin-bottom: 8px; position: relative; z-index: 1; }
.hook { font-size: 44px; font-weight: 800; line-height: 1.2; letter-spacing: -1px; margin-bottom: 24px; max-width: 900px; position: relative; z-index: 1; }
.hook .highlight { background: linear-gradient(90deg, #22c55e, #4ade80); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
.proof { font-size: 18px; color: rgba(255,255,255,0.4); margin-bottom: 16px; position: relative; z-index: 1; }
.proof strong { color: #22c55e; font-weight: 700; }
.detail { font-size: 20px; font-weight: 400; color: rgba(255,255,255,0.5); max-width: 700px; line-height: 1.5; position: relative; z-index: 1; }
.brand { position: absolute; bottom: 35px; right: 55px; font-size: 16px; font-weight: 700; color: rgba(255,255,255,0.15); letter-spacing: 4px; text-transform: uppercase; z-index: 1; }
.glow { position: absolute; bottom: -100px; right: -100px; width: 350px; height: 350px; background: radial-gradient(circle, rgba(34,197,94,0.06) 0%, transparent 70%); border-radius: 50%; }
</style></head><body>
<div class="grid-overlay"></div><div class="glow"></div>
<div class="quote-mark">&ldquo;</div>
<div class="hook">the real AI gold rush isn't <span class="highlight">building</span> AI tools. it's <span class="highlight">babysitting</span> them.</div>
<div class="proof"><strong>241 upvotes</strong> on r/Entrepreneur. <strong>126 comments.</strong> everyone agrees.</div>
<div class="detail">$1,800/project for 25 min of work. the gap between "AI can do this" and "nobody knows how" is your business.</div>
<div class="brand">PRINTMAXX</div>
</body></html>""",
    },

    # === CLAUDE CODE AGENT BIBLE PRODUCT COVER (1280x720) ===
    {
        "id": "product_claude_code_agent_bible",
        "width": 1280, "height": 720,
        "category": "Product Covers (1280x720)",
        "template": "product_cover.html",
        "html_fn": lambda: build_product_cover(
            "DIGITAL PRODUCT",
            'The Claude Code <span class="accent">Agent Bible</span>',
            "33 autonomous agents running 24/7. the exact blueprints, prompts, and architecture.",
            [
                {"value": "33", "label": "Agents"},
                {"value": "287", "label": "Scripts"},
                {"value": "24/7", "label": "Autonomous"},
                {"value": "$200/mo", "label": "Total Cost"},
            ],
        ),
    },

    # === ALPHA SOCIAL CARDS (1200x675) — from 2026-03-09 alpha content ===
    {
        "id": "social_mcp_persistent_memory",
        "width": 1200, "height": 675,
        "category": "Social Cards (1200x675)",
        "template": "social_card.html",
        "html_fn": lambda: build_social_card(
            'MCP server giving Claude <span class="highlight">persistent memory</span> + local RAG',
            "zero-cost memory layer for AI agents. most people sleep on this."
        ),
    },
    {
        "id": "social_govcon_saas",
        "width": 1200, "height": 675,
        "category": "Social Cards (1200x675)",
        "template": "social_card.html",
        "html_fn": lambda: build_social_card(
            'daily <span class="highlight">SAM.gov</span> contract digest. B2B SaaS monetization angle.',
            "GovConToday matched to NAICS codes. the money is in boring B2B."
        ),
    },
    {
        "id": "social_4_ai_companies_terminal",
        "width": 1200, "height": 675,
        "category": "Social Cards (1200x675)",
        "template": "social_card.html",
        "html_fn": lambda: build_social_card(
            '<span class="highlight">4 AI-driven companies</span> from one terminal. agent orchestration.',
            "solopreneur-AI hybrid model. one person + agent swarm = multi-company operation."
        ),
    },
    {
        "id": "social_karpathy_autoresearch",
        "width": 1200, "height": 675,
        "category": "Social Cards (1200x675)",
        "template": "social_card.html",
        "html_fn": lambda: build_social_card(
            '<span class="highlight">Karpathy\'s Autoresearch.</span> agents auto-research ML on a single GPU.',
            "autonomous research agent that writes papers. maps to intelligence gathering."
        ),
    },
    {
        "id": "social_superx_growth_os",
        "width": 1200, "height": 675,
        "category": "Social Cards (1200x675)",
        "template": "social_card.html",
        "html_fn": lambda: build_social_card(
            '<span class="highlight">SuperX.</span> all-in-one growth OS for X creators. 873 PH votes.',
            "social media SaaS with serious traction. the tool creators are using to scale."
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
