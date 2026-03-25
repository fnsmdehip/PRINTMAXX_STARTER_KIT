#!/usr/bin/env python3
"""
PRINTMAXX AI Notetaker Affiliate Content Generator
====================================================
Scrapes Amazon for AI notetaker hardware specs/pricing (Limitless Pendant,
Plaud Note, Otter AI, etc.), generates SEO comparison pages with embedded
affiliate links, and repurposes to social channels targeting business
professionals and remote workers.

Niche: AI notetaking hardware + software
Audience: Business professionals, remote workers, meeting-heavy roles
Monetization: Amazon Associates + direct affiliate programs

Usage:
    python3 AUTOMATIONS/ai_notetaker_affiliate_content.py --run
    python3 AUTOMATIONS/ai_notetaker_affiliate_content.py --status
    python3 AUTOMATIONS/ai_notetaker_affiliate_content.py --dry-run

Cron:
    0 6 * * 1 cd $BASE && $PYTHON AUTOMATIONS/ai_notetaker_affiliate_content.py --run >> AUTOMATIONS/logs/ai_notetaker_affiliate_content.log 2>&1
"""

from __future__ import annotations

import argparse
import csv
import json
import subprocess
import sys
import time
import urllib.request
import urllib.parse
import urllib.error
from datetime import datetime
from pathlib import Path

# ---------------------------------------------------------------------------
# Project root + _common imports
# ---------------------------------------------------------------------------
PROJECT = Path(__file__).resolve().parent.parent

sys.path.insert(0, str(PROJECT / "AUTOMATIONS"))
try:
    from _common import (
        PROJECT as _COMMON_PROJECT,
        safe_path,
        recall_skills_for_task,
        capture_skill_from_result,
    )
    PROJECT = _COMMON_PROJECT
except ImportError:
    def safe_path(target) -> Path:
        resolved = Path(target).resolve()
        if not str(resolved).startswith(str(PROJECT)):
            raise ValueError(f"BLOCKED: {resolved} is outside project root {PROJECT}")
        return resolved

    def recall_skills_for_task(task_description: str, max_chars: int = 600) -> str:
        return ""

    def capture_skill_from_result(task: str, result: str, success: bool = True) -> None:
        pass

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
LOG_FILE = PROJECT / "AUTOMATIONS" / "logs" / "ai_notetaker_affiliate_content.log"
OUTPUT_DIR = PROJECT / "CONTENT" / "affiliate" / "ai_notetakers"
CACHE_FILE = PROJECT / "AUTOMATIONS" / "logs" / "ai_notetaker_cache.json"
SOCIAL_DIR = PROJECT / "CONTENT" / "social" / "auto_generated"

# ---------------------------------------------------------------------------
# Affiliate configuration
# ---------------------------------------------------------------------------
AMAZON_AFFILIATE_TAG = "printmaxx-20"  # Replace with actual tag

PRODUCTS: list[dict] = [
    {
        "id": "plaud_note",
        "name": "PLAUD NOTE AI Voice Recorder",
        "brand": "PLAUD",
        "category": "hardware",
        "asin": "B0CW19QGBT",
        "search_query": "PLAUD NOTE AI voice recorder pendant",
        "price_usd": 169.00,
        "key_features": [
            "ChatGPT-powered transcription",
            "Magnetic card form factor",
            "Phone call recording",
            "90+ language support",
            "Unlimited cloud storage",
        ],
        "pros": ["Ultra-slim design", "Works with calls", "No subscription for basic"],
        "cons": ["Requires PLAUD app", "Small battery for all-day recording"],
        "best_for": "Business professionals who record calls",
        "rating": 4.2,
    },
    {
        "id": "limitless_pendant",
        "name": "Limitless AI Pendant",
        "brand": "Limitless",
        "category": "hardware",
        "asin": None,
        "search_query": "Limitless AI pendant wearable recorder",
        "price_usd": 99.00,
        "key_features": [
            "Always-on ambient recording",
            "GPT-4 meeting summaries",
            "Wearable pendant form factor",
            "Consent beacon LED",
            "Personalized AI memory",
        ],
        "pros": ["Truly always-on", "Strong AI summaries", "Stylish form factor"],
        "cons": ["Subscription required ($19/mo)", "Privacy concerns from others"],
        "best_for": "Power users who want full-day meeting capture",
        "rating": 4.4,
    },
    {
        "id": "otter_ai",
        "name": "Otter.ai Business Plan",
        "brand": "Otter.ai",
        "category": "software",
        "asin": None,
        "search_query": "Otter AI meeting transcription business",
        "price_usd": 20.00,
        "key_features": [
            "Real-time transcription",
            "Zoom/Meet/Teams integration",
            "AI meeting summaries",
            "Action item extraction",
            "Team collaboration",
        ],
        "pros": ["Best integrations", "Real-time captions", "Team features"],
        "cons": ["Software-only", "Free tier limited (300 min/mo)"],
        "best_for": "Teams using Zoom/Google Meet",
        "rating": 4.5,
    },
    {
        "id": "zoom_ai",
        "name": "Zoom AI Companion",
        "brand": "Zoom",
        "category": "software",
        "asin": None,
        "search_query": "Zoom AI Companion meeting summary",
        "price_usd": 0.00,
        "key_features": [
            "Built into Zoom",
            "Auto meeting summaries",
            "Chat thread summaries",
            "Ask questions about meetings",
            "No extra cost with Zoom Pro+",
        ],
        "pros": ["Free with Zoom paid", "Zero friction setup", "Deep Zoom integration"],
        "cons": ["Zoom meetings only", "Less powerful than dedicated tools"],
        "best_for": "Zoom-centric teams who want zero extra cost",
        "rating": 4.0,
    },
    {
        "id": "fathom_ai",
        "name": "Fathom AI Notetaker",
        "brand": "Fathom",
        "category": "software",
        "asin": None,
        "search_query": "Fathom AI notetaker free meeting recorder",
        "price_usd": 0.00,
        "key_features": [
            "Free unlimited recordings",
            "Zoom + Meet + Teams",
            "Highlight moments live",
            "Auto summaries + action items",
            "CRM integrations (HubSpot, Salesforce)",
        ],
        "pros": ["Free tier is genuinely unlimited", "CRM sync", "Clean UI"],
        "cons": ["Fewer language options than PLAUD", "No hardware component"],
        "best_for": "Sales teams needing CRM integration",
        "rating": 4.7,
    },
    {
        "id": "plaud_notepin",
        "name": "PLAUD NotePin AI Wearable",
        "brand": "PLAUD",
        "category": "hardware",
        "asin": "B0D5QG3FZJ",
        "search_query": "PLAUD NotePin AI wearable recorder pin",
        "price_usd": 129.00,
        "key_features": [
            "Wearable pin form factor",
            "Offline + online transcription",
            "100+ language support",
            "30 day standby battery",
            "AI summarization via app",
        ],
        "pros": ["Lightweight wearable", "Long battery life", "Works offline"],
        "cons": ["Newer product, less reviews", "App required for summaries"],
        "best_for": "Remote workers in hybrid environments",
        "rating": 4.3,
    },
]

SOCIAL_TEMPLATES = {
    "awareness": [
        "These AI notetaking devices can help you record and transcribe your meetings — no more manual notes.",
        "If you're in back-to-back meetings all day, these AI recorders will change your workflow.",
        "The best AI notetakers in 2026 compared — hardware vs software, and which actually works.",
        "You don't need to take notes in meetings anymore. Here's the best gear doing it for you.",
    ],
    "comparison": [
        "{product_a} vs {product_b}: which AI notetaker wins for {use_case}?",
        "I tested {count} AI meeting recorders. Here's what I found.",
        "{product_a} ({price_a}) vs {product_b} ({price_b}) — the honest comparison.",
    ],
    "review": [
        "{product}: Is the {price} price tag worth it for remote workers?",
        "Week 2 with the {product} — here's what nobody tells you before you buy.",
        "{product} review: the good, the bad, and whether it actually saves time.",
    ],
}

SEO_KEYWORDS = [
    "best AI notetaker 2026",
    "AI meeting recorder",
    "Limitless Pendant review",
    "PLAUD Note review",
    "AI voice recorder for business",
    "meeting transcription device",
    "Otter AI vs Fathom",
    "best meeting recorder remote work",
    "wearable AI recorder",
    "hands-free meeting notes",
]

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------
def log(msg: str, level: str = "INFO") -> None:
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] [{level}] {msg}"
    print(line)
    try:
        log_dir = safe_path(LOG_FILE.parent)
        log_dir.mkdir(parents=True, exist_ok=True)
        with open(safe_path(LOG_FILE), "a", encoding="utf-8") as f:
            f.write(line + "\n")
    except Exception as e:
        print(f"[LOG ERROR] {e}", file=sys.stderr)


# ---------------------------------------------------------------------------
# Amazon scraping (urllib only)
# ---------------------------------------------------------------------------
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/122.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
}


def fetch_url(url: str, timeout: int = 10) -> str | None:
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as e:
        log(f"HTTP {e.code} fetching {url}", "WARN")
        return None
    except urllib.error.URLError as e:
        log(f"URL error fetching {url}: {e.reason}", "WARN")
        return None
    except Exception as e:
        log(f"Fetch error {url}: {e}", "WARN")
        return None


def parse_amazon_price(html: str) -> str | None:
    import re
    markers = [
        'class="a-price-whole"',
        'id="priceblock_ourprice"',
        'id="priceblock_dealprice"',
        '"priceAmount"',
    ]
    for marker in markers:
        idx = html.find(marker)
        if idx == -1:
            continue
        chunk = html[idx:idx + 200]
        match = re.search(r"\$?([\d,]+\.\d{2})", chunk)
        if match:
            return match.group(1)
    return None


def parse_amazon_rating(html: str) -> str | None:
    import re
    match = re.search(r'"ratingScore"[^>]*>([0-9.]+)', html)
    if match:
        return match.group(1)
    match = re.search(r'([0-9.]+) out of 5 stars', html)
    if match:
        return match.group(1)
    return None


def build_affiliate_url(asin: str, tag: str = AMAZON_AFFILIATE_TAG) -> str:
    return f"https://www.amazon.com/dp/{asin}?tag={tag}"


def scrape_amazon_product(product: dict) -> dict:
    result = {
        "id": product["id"],
        "name": product["name"],
        "price_usd": product["price_usd"],
        "rating": product["rating"],
        "affiliate_url": None,
        "scraped": False,
        "scraped_at": datetime.now().isoformat(),
    }

    asin = product.get("asin")
    if not asin:
        log(f"  {product['name']}: no ASIN (direct purchase only)")
        return result

    url = build_affiliate_url(asin)
    result["affiliate_url"] = url

    log(f"  Fetching Amazon: {product['name']} (ASIN {asin})")
    html = fetch_url(f"https://www.amazon.com/dp/{asin}")

    if not html:
        log(f"  {product['name']}: fetch failed, using catalog data", "WARN")
        return result

    price = parse_amazon_price(html)
    rating = parse_amazon_rating(html)

    if price:
        try:
            result["price_usd"] = float(price.replace(",", ""))
            result["scraped"] = True
            log(f"  {product['name']}: price=${price}, rating={rating or 'N/A'}")
        except ValueError:
            pass

    if rating:
        try:
            result["rating"] = float(rating)
        except ValueError:
            pass

    time.sleep(2)
    return result


# ---------------------------------------------------------------------------
# Cache
# ---------------------------------------------------------------------------
def load_cache() -> dict:
    if not CACHE_FILE.exists():
        return {}
    try:
        return json.loads(CACHE_FILE.read_text(encoding="utf-8"))
    except Exception:
        return {}


def save_cache(data: dict) -> None:
    try:
        cache_path = safe_path(CACHE_FILE)
        cache_path.parent.mkdir(parents=True, exist_ok=True)
        cache_path.write_text(json.dumps(data, indent=2), encoding="utf-8")
    except Exception as e:
        log(f"Cache save error: {e}", "WARN")


# ---------------------------------------------------------------------------
# SEO page generation
# ---------------------------------------------------------------------------
def format_price(price_usd: float) -> str:
    if price_usd == 0.0:
        return "Free"
    return f"${price_usd:.2f}"


def generate_comparison_html(products: list[dict], scraped: dict) -> str:
    ts = datetime.now().strftime("%B %Y")
    keywords_meta = ", ".join(SEO_KEYWORDS[:6])

    rows = ""
    for p in products:
        live = scraped.get(p["id"], {})
        price = format_price(live.get("price_usd", p["price_usd"]))
        rating = live.get("rating", p["rating"])
        aff_url = live.get("affiliate_url") or "#"
        cat_badge = "Hardware" if p["category"] == "hardware" else "Software"
        features_li = "".join(f"<li>{f}</li>" for f in p["key_features"][:4])
        pros_li = "".join(f"<li>✓ {pro}</li>" for pro in p["pros"])
        cons_li = "".join(f"<li>✗ {con}</li>" for con in p["cons"])
        cta = (
            f'<a href="{aff_url}" class="btn-affiliate" rel="sponsored noopener" target="_blank">'
            f'Check Price on Amazon →</a>'
            if aff_url != "#"
            else '<a href="#" class="btn-affiliate">Visit Official Site →</a>'
        )
        rows += f"""
        <div class="product-card" id="{p['id']}">
          <div class="product-header">
            <span class="badge">{cat_badge}</span>
            <h2>{p['name']}</h2>
            <div class="price">{price}</div>
            <div class="rating">{"★" * int(round(rating))} ({rating}/5)</div>
          </div>
          <div class="best-for"><strong>Best for:</strong> {p['best_for']}</div>
          <div class="features"><h3>Key Features</h3><ul>{features_li}</ul></div>
          <div class="pros-cons">
            <div class="pros"><h4>Pros</h4><ul>{pros_li}</ul></div>
            <div class="cons"><h4>Cons</h4><ul>{cons_li}</ul></div>
          </div>
          <div class="cta">{cta}</div>
          <p class="disclaimer">*Affiliate link. We may earn a commission at no extra cost to you.</p>
        </div>"""

    toc_items = "".join(
        f'<li><a href="#{p["id"]}">{p["name"]}</a></li>' for p in products
    )

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Best AI Notetakers for Business — {ts} Comparison</title>
  <meta name="description" content="Compare the best AI meeting recorders for business professionals: Limitless Pendant, PLAUD Note, Otter AI, Fathom, and more. Prices, pros/cons, and honest reviews.">
  <meta name="keywords" content="{keywords_meta}">
  <style>
    *{{box-sizing:border-box;margin:0;padding:0}}
    body{{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;color:#1a1a1a;background:#f8f9fa;line-height:1.6}}
    .container{{max-width:900px;margin:0 auto;padding:2rem 1rem}}
    h1{{font-size:2rem;margin-bottom:0.5rem}}
    .subtitle{{color:#666;margin-bottom:2rem}}
    .product-card{{background:#fff;border:1px solid #e0e0e0;border-radius:12px;padding:1.5rem;margin-bottom:1.5rem}}
    .product-header{{margin-bottom:1rem}}
    .badge{{background:#0066cc;color:#fff;font-size:0.7rem;padding:0.2rem 0.5rem;border-radius:4px;text-transform:uppercase}}
    .product-header h2{{font-size:1.4rem;margin:0.5rem 0 0.25rem}}
    .price{{font-size:1.6rem;font-weight:700;color:#0066cc}}
    .rating{{color:#f5a623;margin-top:0.25rem}}
    .best-for{{background:#f0f7ff;padding:0.75rem;border-radius:6px;margin:1rem 0;font-size:0.9rem}}
    .features h3,.pros-cons h4{{font-size:1rem;margin-bottom:0.4rem}}
    .features ul,.pros-cons ul{{padding-left:1.2rem}}
    .features li,.pros-cons li{{font-size:0.9rem;margin-bottom:0.25rem}}
    .pros-cons{{display:grid;grid-template-columns:1fr 1fr;gap:1rem;margin:1rem 0}}
    .pros li{{color:#2e7d32}}.cons li{{color:#c62828}}
    .btn-affiliate{{display:inline-block;background:#ff9900;color:#fff;padding:0.75rem 1.5rem;border-radius:8px;text-decoration:none;font-weight:600;margin-top:1rem}}
    .btn-affiliate:hover{{background:#e68900}}
    .disclaimer{{font-size:0.75rem;color:#999;margin-top:0.5rem}}
    .toc{{background:#fff;border:1px solid #e0e0e0;border-radius:8px;padding:1rem;margin-bottom:2rem}}
    .toc h2{{font-size:1rem;margin-bottom:0.5rem}}
    .toc ol{{padding-left:1.2rem}}
    .toc li{{font-size:0.9rem;margin-bottom:0.25rem}}
    .faq{{margin-top:2rem}}
    .faq h2{{font-size:1.5rem;margin-bottom:1rem}}
    .faq-item{{margin-bottom:1.5rem}}
    .faq-item h3{{font-size:1rem;font-weight:600;margin-bottom:0.4rem}}
    footer{{text-align:center;color:#999;font-size:0.8rem;margin-top:3rem;padding:1rem}}
  </style>
</head>
<body>
  <div class="container">
    <h1>Best AI Notetakers for Business ({ts})</h1>
    <p class="subtitle">Honest comparison of AI meeting recorders for professionals and remote workers — hardware &amp; software.</p>
    <div class="toc">
      <h2>Quick Navigation</h2>
      <ol>{toc_items}<li><a href="#faq">FAQ</a></li></ol>
    </div>
    {rows}
    <section class="faq" id="faq">
      <h2>Frequently Asked Questions</h2>
      <div class="faq-item">
        <h3>What is the best AI notetaker for business meetings?</h3>
        <p>Fathom AI leads for teams needing CRM integration (free tier), while PLAUD Note wins for hardware-based call recording. Limitless Pendant is best for always-on ambient capture.</p>
      </div>
      <div class="faq-item">
        <h3>Do AI notetakers work without the internet?</h3>
        <p>PLAUD NotePin offers offline recording with later sync. Most software-based tools (Otter, Fathom, Zoom AI) require a live internet connection for real-time transcription.</p>
      </div>
      <div class="faq-item">
        <h3>Are AI notetakers legal to use in meetings?</h3>
        <p>Consent laws vary by state and country. Most tools include a consent notification feature. Always inform meeting participants when recording is active.</p>
      </div>
      <div class="faq-item">
        <h3>What is the cheapest AI notetaker?</h3>
        <p>Fathom AI and Zoom AI Companion both offer free tiers. Fathom's free plan is unlimited for individuals; Zoom AI is included with any paid Zoom plan.</p>
      </div>
    </section>
    <footer><p>Last updated: {ts}. Prices subject to change. Some links are affiliate links.</p></footer>
  </div>
</body>
</html>"""


# ---------------------------------------------------------------------------
# Social content repurposing
# ---------------------------------------------------------------------------
def generate_social_posts(products: list[dict], scraped: dict) -> list[dict]:
    posts = []
    method_context = "These AI notetaking devices can help you record and transcribe your meetings"

    for template in SOCIAL_TEMPLATES["awareness"]:
        posts.append({
            "platform": "twitter",
            "type": "awareness",
            "text": template,
            "char_count": len(template),
            "status": "PENDING_REVIEW",
            "generated_at": datetime.now().isoformat(),
        })

    top_5 = products[:5]
    linkedin_lines = "\n".join(
        f"{i}. {p['name']} ({format_price(scraped.get(p['id'], {}).get('price_usd', p['price_usd']))}) — {p['best_for']}"
        for i, p in enumerate(top_5, 1)
    )
    linkedin_text = (
        f"{method_context} — no more scrambling to capture action items.\n\n"
        f"Here are the best options right now:\n\n{linkedin_lines}\n\n"
        "Which one fits your workflow? Drop a comment."
    )
    posts.append({
        "platform": "linkedin",
        "type": "listicle",
        "text": linkedin_text,
        "char_count": len(linkedin_text),
        "status": "PENDING_REVIEW",
        "generated_at": datetime.now().isoformat(),
    })

    if len(products) >= 3:
        p1, p2 = products[0], products[2]
        live1 = scraped.get(p1["id"], {})
        live2 = scraped.get(p2["id"], {})
        for template_key, kwargs in [
            ("comparison", dict(
                product_a=p1["name"],
                product_b=p2["name"],
                use_case="remote workers",
            )),
        ]:
            text = SOCIAL_TEMPLATES[template_key][0].format(**kwargs)
            posts.append({
                "platform": "twitter",
                "type": "comparison",
                "text": text,
                "char_count": len(text),
                "status": "PENDING_REVIEW",
                "generated_at": datetime.now().isoformat(),
            })

        honest = SOCIAL_TEMPLATES["comparison"][2].format(
            product_a=p1["name"],
            product_b=p2["name"],
            price_a=format_price(live1.get("price_usd", p1["price_usd"])),
            price_b=format_price(live2.get("price_usd", p2["price_usd"])),
        )
        posts.append({
            "platform": "twitter",
            "type": "comparison",
            "text": honest,
            "char_count": len(honest),
            "status": "PENDING_REVIEW",
            "generated_at": datetime.now().isoformat(),
        })

    tiktok_script = (
        f"POV: you just got out of a 2-hour meeting and didn't take a single note. "
        f"[cut] This is the {products[0]['name']} — it recorded everything. "
        "AI transcription, summary, action items. Done. Link in bio for the full comparison."
    )
    posts.append({
        "platform": "tiktok",
        "type": "hook_review",
        "text": tiktok_script,
        "char_count": len(tiktok_script),
        "status": "PENDING_REVIEW",
        "generated_at": datetime.now().isoformat(),
    })

    return posts


# ---------------------------------------------------------------------------
# Save outputs
# ---------------------------------------------------------------------------
def save_comparison_page(html: str, dry_run: bool = False) -> Path | None:
    ts = datetime.now().strftime("%Y%m%d")
    out_path = OUTPUT_DIR / f"ai_notetaker_comparison_{ts}.html"
    if dry_run:
        print(f"\n[DRY RUN] Would write HTML comparison page -> {out_path} ({len(html)} chars)")
        return None
    try:
        safe_path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)
        safe_path(out_path).write_text(html, encoding="utf-8")
        log(f"Wrote comparison page: {out_path}")
        return out_path
    except Exception as e:
        log(f"Failed to write comparison page: {e}", "ERROR")
        return None


def save_social_posts(posts: list[dict], dry_run: bool = False) -> Path | None:
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_path = SOCIAL_DIR / f"ai_notetaker_posts_{ts}.csv"
    if dry_run:
        print(f"\n[DRY RUN] Would write {len(posts)} social posts -> {out_path}")
        for p in posts:
            print(f"  [{p['platform']}:{p['type']}] {p['text'][:80]}...")
        return None
    try:
        safe_path(SOCIAL_DIR).mkdir(parents=True, exist_ok=True)
        fieldnames = ["platform", "type", "text", "char_count", "status", "generated_at"]
        with open(safe_path(out_path), "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(posts)
        log(f"Wrote {len(posts)} social posts: {out_path}")
        return out_path
    except Exception as e:
        log(f"Failed to write social posts: {e}", "ERROR")
        return None


def save_product_data(products: list[dict], scraped: dict, dry_run: bool = False) -> Path | None:
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_path = OUTPUT_DIR / f"product_data_{ts}.json"
    combined = [
        {**p, "live_price": scraped.get(p["id"], {}).get("price_usd"),
         "affiliate_url": scraped.get(p["id"], {}).get("affiliate_url"),
         "scraped": scraped.get(p["id"], {}).get("scraped", False)}
        for p in products
    ]
    if dry_run:
        print(f"\n[DRY RUN] Would write {len(combined)} product records -> {out_path}")
        return None
    try:
        safe_path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)
        safe_path(out_path).write_text(json.dumps(combined, indent=2), encoding="utf-8")
        log(f"Wrote product data: {out_path}")
        return out_path
    except Exception as e:
        log(f"Failed to write product data: {e}", "ERROR")
        return None


# ---------------------------------------------------------------------------
# Status
# ---------------------------------------------------------------------------
def show_status() -> None:
    print("\n--- AI Notetaker Affiliate Content Status ---\n")

    cache = load_cache()
    if cache:
        print(f"  Last scrape:     {cache.get('scraped_at', 'unknown')}")
        print(f"  Products cached: {len(cache.get('products', {}))}")
    else:
        print("  Cache: None (run --run to populate)")

    html_files: list[Path] = sorted(OUTPUT_DIR.glob("*.html"), reverse=True) if OUTPUT_DIR.exists() else []
    json_files: list[Path] = sorted(OUTPUT_DIR.glob("product_data_*.json"), reverse=True) if OUTPUT_DIR.exists() else []
    print(f"\n  Comparison pages: {len(html_files)}")
    for f in html_files[:3]:
        print(f"    {f.name} ({f.stat().st_size // 1024}KB)")

    print(f"\n  Product data files: {len(json_files)}")
    for f in json_files[:3]:
        print(f"    {f.name}")

    social_files: list[Path] = (
        sorted(SOCIAL_DIR.glob("ai_notetaker_posts_*.csv"), reverse=True)
        if SOCIAL_DIR.exists() else []
    )
    print(f"\n  Social post batches: {len(social_files)}")
    for f in social_files[:3]:
        try:
            count = sum(1 for _ in open(f, newline="", encoding="utf-8")) - 1
            print(f"    {f.name} ({count} posts)")
        except Exception:
            print(f"    {f.name}")

    if LOG_FILE.exists():
        try:
            lines = LOG_FILE.read_text(encoding="utf-8").splitlines()
            print(f"\n  Recent log ({len(lines)} entries):")
            for line in lines[-5:]:
                print(f"    {line}")
        except Exception:
            pass
    print()


# ---------------------------------------------------------------------------
# Main pipeline
# ---------------------------------------------------------------------------
def run_pipeline(dry_run: bool = False) -> None:
    log("=" * 60)
    log("AI Notetaker Affiliate Content — pipeline start")
    if dry_run:
        log("DRY RUN mode: no files will be written")

    task_desc = "generate affiliate review content for AI notetaker hardware"
    prior_skills = recall_skills_for_task(task_desc)
    if prior_skills:
        log(f"Recalled skills: {prior_skills[:120]}...")

    # Step 1: Scrape Amazon for live prices
    log("Step 1/4: Scraping Amazon product data...")
    scraped: dict[str, dict] = {}
    for product in PRODUCTS:
        try:
            scraped[product["id"]] = scrape_amazon_product(product)
        except Exception as e:
            log(f"  Error scraping {product['name']}: {e}", "ERROR")
            scraped[product["id"]] = {
                "id": product["id"],
                "price_usd": product["price_usd"],
                "rating": product["rating"],
                "scraped": False,
            }

    scraped_count = sum(1 for v in scraped.values() if v.get("scraped"))
    log(f"  Scraped {scraped_count}/{len(PRODUCTS)} products successfully")

    if not dry_run:
        save_cache({"scraped_at": datetime.now().isoformat(), "products": scraped})

    # Step 2: Generate comparison HTML page
    log("Step 2/4: Generating SEO comparison page...")
    try:
        html = generate_comparison_html(PRODUCTS, scraped)
        save_comparison_page(html, dry_run)
    except Exception as e:
        log(f"Comparison page generation failed: {e}", "ERROR")

    # Step 3: Generate social posts
    log("Step 3/4: Generating social posts...")
    posts: list[dict] = []
    try:
        posts = generate_social_posts(PRODUCTS, scraped)
        save_social_posts(posts, dry_run)
        platforms = len(set(p["platform"] for p in posts))
        log(f"  Generated {len(posts)} posts across {platforms} platforms")
    except Exception as e:
        log(f"Social post generation failed: {e}", "ERROR")

    # Step 4: Save product JSON
    log("Step 4/4: Saving product data...")
    try:
        save_product_data(PRODUCTS, scraped, dry_run)
    except Exception as e:
        log(f"Product data save failed: {e}", "ERROR")

    result_summary = (
        f"Pipeline complete: {scraped_count} products scraped, "
        f"{len(posts)} social posts generated"
    )
    log(result_summary)

    if not dry_run:
        capture_skill_from_result(task_desc, result_summary, success=True)

    log("=" * 60)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------
def main() -> None:
    parser = argparse.ArgumentParser(
        description="PRINTMAXX AI Notetaker Affiliate Content Generator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Examples:\n"
            "  python3 ai_notetaker_affiliate_content.py --run\n"
            "  python3 ai_notetaker_affiliate_content.py --dry-run\n"
            "  python3 ai_notetaker_affiliate_content.py --status"
        ),
    )
    parser.add_argument("--run", action="store_true", help="Run the full pipeline")
    parser.add_argument("--status", action="store_true", help="Show pipeline status")
    parser.add_argument("--dry-run", action="store_true", help="Preview without writing files")
    args = parser.parse_args()

    if args.status:
        show_status()
        return

    if args.run or args.dry_run:
        try:
            run_pipeline(dry_run=args.dry_run)
        except KeyboardInterrupt:
            log("Interrupted by user", "WARN")
            sys.exit(1)
        except Exception as e:
            log(f"Pipeline failed: {e}", "ERROR")
            sys.exit(1)
        return

    parser.print_help()


if __name__ == "__main__":
    main()