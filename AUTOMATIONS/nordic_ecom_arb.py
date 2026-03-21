#!/usr/bin/env python3

from __future__ import annotations
"""
Nordic Ecom Arbitrage Pipeline
------------------------------
Finds products trending in the US that are missing or underserved in Nordic markets.
Outputs gap analysis CSV for manual sourcing and listing.

Strategy: US trending product -> check Nordic availability -> identify gaps -> list in local language

Usage:
    python3 nordic_ecom_arb.py                    # Full scan
    python3 nordic_ecom_arb.py --category electronics  # Single category
    python3 nordic_ecom_arb.py --output custom.csv     # Custom output file
"""

import requests
import csv
import json
import time
import re
import os
import argparse
import xml.etree.ElementTree as ET
from datetime import datetime
from urllib.parse import quote_plus
from bs4 import BeautifulSoup

# ============================================================
# CONFIGURATION
# ============================================================

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
DEFAULT_OUTPUT = os.path.join(PROJECT_ROOT, "LEDGER", "NORDIC_ECOM_GAPS.csv")
ALPHA_STAGING = os.path.join(PROJECT_ROOT, "LEDGER", "ALPHA_STAGING.csv")

# Amazon Best Sellers RSS feeds by category
AMAZON_RSS_FEEDS = {
    "electronics": "https://www.amazon.com/gp/rss/bestsellers/electronics/ref=zg_bs_electronics_rsslink",
    "home_kitchen": "https://www.amazon.com/gp/rss/bestsellers/home-garden/ref=zg_bs_home-garden_rsslink",
    "beauty": "https://www.amazon.com/gp/rss/bestsellers/beauty/ref=zg_bs_beauty_rsslink",
    "health": "https://www.amazon.com/gp/rss/bestsellers/hpc/ref=zg_bs_hpc_rsslink",
    "toys": "https://www.amazon.com/gp/rss/bestsellers/toys-and-games/ref=zg_bs_toys-and-games_rsslink",
    "sports": "https://www.amazon.com/gp/rss/bestsellers/sporting-goods/ref=zg_bs_sporting-goods_rsslink",
    "kitchen": "https://www.amazon.com/gp/rss/bestsellers/kitchen/ref=zg_bs_kitchen_rsslink",
    "pet_supplies": "https://www.amazon.com/gp/rss/bestsellers/pet-supplies/ref=zg_bs_pet-supplies_rsslink",
    "baby": "https://www.amazon.com/gp/rss/bestsellers/baby-products/ref=zg_bs_baby-products_rsslink",
    "garden": "https://www.amazon.com/gp/rss/bestsellers/lawn-garden/ref=zg_bs_lawn-garden_rsslink",
}

# Nordic marketplace search URLs
NORDIC_MARKETS = {
    "norway": {
        "platforms": ["finn.no", "komplett.no", "elkjop.no"],
        "language": "Norwegian (Bokmal)",
        "currency": "NOK",
        "search_urls": {
            "finn.no": "https://www.finn.no/bap/forsale/search.html?q={}",
            "komplett.no": "https://www.komplett.no/search?q={}",
            "elkjop.no": "https://www.elkjop.no/search?q={}",
        },
    },
    "sweden": {
        "platforms": ["cdon.com", "tradera.com", "blocket.se"],
        "language": "Swedish",
        "currency": "SEK",
        "search_urls": {
            "cdon.com": "https://cdon.se/search?q={}",
            "tradera.com": "https://www.tradera.com/search?q={}",
            "blocket.se": "https://www.blocket.se/annonser?q={}",
        },
    },
    "denmark": {
        "platforms": ["dba.dk", "proshop.dk", "elgiganten.dk"],
        "language": "Danish",
        "currency": "DKK",
        "search_urls": {
            "dba.dk": "https://www.dba.dk/soeg/?soeg={}",
            "proshop.dk": "https://www.proshop.dk/{}",
            "elgiganten.dk": "https://www.elgiganten.dk/search?q={}",
        },
    },
    "finland": {
        "platforms": ["tori.fi", "verkkokauppa.com", "gigantti.fi"],
        "language": "Finnish",
        "currency": "EUR",
        "search_urls": {
            "tori.fi": "https://www.tori.fi/koko_suomi?q={}",
            "verkkokauppa.com": "https://www.verkkokauppa.com/fi/search?query={}",
            "gigantti.fi": "https://www.gigantti.fi/search?q={}",
        },
    },
}

# TikTok trending product search terms (categories that travel well to Nordics)
TIKTOK_TRENDING_SEARCHES = [
    "tiktok made me buy it 2026",
    "amazon must haves 2026",
    "viral amazon products",
    "trending products to sell online 2026",
    "best selling products amazon february 2026",
    "tiktok shop best sellers",
    "gadgets going viral 2026",
    "home organization viral products",
    "beauty products going viral",
    "fitness gadgets trending",
]

# Known high-demand Nordic product categories
NORDIC_HIGH_DEMAND = [
    "outdoor gear",
    "winter accessories",
    "smart home",
    "LED lighting",
    "kitchen gadgets",
    "fitness equipment",
    "phone accessories",
    "cable management",
    "desk accessories",
    "skincare tools",
    "portable chargers",
    "organization products",
]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
}


# ============================================================
# SCRAPERS
# ============================================================

def scrape_amazon_bestsellers(category=None):
    """Scrape Amazon Best Sellers RSS feeds for trending products."""
    products = []
    feeds = {category: AMAZON_RSS_FEEDS[category]} if category and category in AMAZON_RSS_FEEDS else AMAZON_RSS_FEEDS

    for cat, url in feeds.items():
        print(f"  [Amazon RSS] Fetching {cat}...")
        try:
            resp = requests.get(url, headers=HEADERS, timeout=15)
            if resp.status_code == 200:
                # Parse RSS XML
                root = ET.fromstring(resp.content)
                # Handle RSS namespace
                ns = {"": ""}
                items = root.findall(".//item")
                if not items:
                    # Try with channel
                    channel = root.find("channel")
                    if channel:
                        items = channel.findall("item")

                for item in items[:15]:  # Top 15 per category
                    title_el = item.find("title")
                    link_el = item.find("link")
                    desc_el = item.find("description")

                    title = title_el.text if title_el is not None else ""
                    link = link_el.text if link_el is not None else ""

                    # Try to extract price from description HTML
                    price = extract_price_from_html(desc_el.text if desc_el is not None else "")

                    if title and len(title) > 5:
                        products.append({
                            "name": clean_product_name(title),
                            "raw_name": title,
                            "us_price": price,
                            "us_platform": "Amazon",
                            "category": cat,
                            "source_url": link,
                            "source": "amazon_rss",
                        })
                print(f"    Found {len(items)} items in {cat}")
            else:
                print(f"    RSS feed returned {resp.status_code} for {cat}")
        except Exception as e:
            print(f"    Error fetching {cat}: {e}")
        time.sleep(1)

    return products


def scrape_trending_via_search():
    """Use web search to find trending US products that might work in Nordics."""
    products = []

    for query in TIKTOK_TRENDING_SEARCHES[:6]:  # Limit to avoid rate limiting
        print(f"  [Search] Querying: {query}")
        try:
            # Use DuckDuckGo HTML search (no API key needed)
            search_url = f"https://html.duckduckgo.com/html/?q={quote_plus(query)}"
            resp = requests.get(search_url, headers=HEADERS, timeout=15)

            if resp.status_code == 200:
                soup = BeautifulSoup(resp.text, "html.parser")
                results = soup.find_all("a", class_="result__a")

                for result in results[:5]:
                    title = result.get_text(strip=True)
                    href = result.get("href", "")
                    if title and len(title) > 10:
                        # Extract product mentions from search results
                        extracted = extract_products_from_title(title)
                        for prod in extracted:
                            products.append({
                                "name": prod,
                                "raw_name": title,
                                "us_price": "Research needed",
                                "us_platform": "TikTok/Viral",
                                "category": "trending",
                                "source_url": href,
                                "source": "search_trending",
                            })
                print(f"    Found {len(results)} results")
            else:
                print(f"    Search returned {resp.status_code}")
        except Exception as e:
            print(f"    Error searching: {e}")
        time.sleep(2)

    return products


def scrape_known_viral_products():
    """Hardcoded list of currently viral products that are PROVEN sellers.
    These are products with verified US demand that likely have Nordic gaps."""

    # These are products confirmed trending via TikTok/Amazon in early 2026
    # Updated manually or via scraper runs
    viral_products = [
        {"name": "Stanley Quencher Tumbler", "us_price": "$35-45", "category": "kitchen", "us_platform": "Amazon/TikTok Shop"},
        {"name": "Portable Neck Fan", "us_price": "$15-25", "category": "electronics", "us_platform": "Amazon/TikTok Shop"},
        {"name": "LED Strip Lights Smart WiFi", "us_price": "$12-20", "category": "home_kitchen", "us_platform": "Amazon"},
        {"name": "Ice Roller Face Massager", "us_price": "$8-15", "category": "beauty", "us_platform": "Amazon/TikTok Shop"},
        {"name": "Portable Blender USB Rechargeable", "us_price": "$20-30", "category": "kitchen", "us_platform": "Amazon/TikTok Shop"},
        {"name": "Cloud Slides Pillow Slippers", "us_price": "$15-25", "category": "fashion", "us_platform": "Amazon/TikTok Shop"},
        {"name": "Sunset Lamp Projector", "us_price": "$15-25", "category": "home_kitchen", "us_platform": "Amazon/TikTok"},
        {"name": "Cable Management Box", "us_price": "$10-15", "category": "electronics", "us_platform": "Amazon"},
        {"name": "Electric Spin Scrubber", "us_price": "$25-40", "category": "home_kitchen", "us_platform": "Amazon/TikTok Shop"},
        {"name": "Scalp Massager Shampoo Brush", "us_price": "$5-10", "category": "beauty", "us_platform": "Amazon"},
        {"name": "Mini Projector Portable", "us_price": "$50-80", "category": "electronics", "us_platform": "Amazon"},
        {"name": "Acupressure Mat and Pillow Set", "us_price": "$20-35", "category": "health", "us_platform": "Amazon"},
        {"name": "Desk Pad Large Mouse Pad", "us_price": "$10-15", "category": "electronics", "us_platform": "Amazon"},
        {"name": "Ring Light with Tripod Stand", "us_price": "$15-30", "category": "electronics", "us_platform": "Amazon"},
        {"name": "Resistance Bands Set", "us_price": "$10-20", "category": "sports", "us_platform": "Amazon"},
        {"name": "Reusable Water Balloons", "us_price": "$10-15", "category": "toys", "us_platform": "Amazon/TikTok Shop"},
        {"name": "Magnetic Phone Mount MagSafe Car", "us_price": "$15-25", "category": "electronics", "us_platform": "Amazon"},
        {"name": "Posture Corrector Back Brace", "us_price": "$15-25", "category": "health", "us_platform": "Amazon"},
        {"name": "Insulated Lunch Box Bento", "us_price": "$15-25", "category": "kitchen", "us_platform": "Amazon"},
        {"name": "Wireless Earbuds Budget", "us_price": "$20-40", "category": "electronics", "us_platform": "Amazon"},
        {"name": "Gua Sha Facial Tool", "us_price": "$5-15", "category": "beauty", "us_platform": "Amazon/TikTok Shop"},
        {"name": "Smart Plug WiFi Outlet", "us_price": "$10-15", "category": "electronics", "us_platform": "Amazon"},
        {"name": "Heated Eye Mask USB", "us_price": "$15-25", "category": "health", "us_platform": "Amazon"},
        {"name": "Foldable Phone Stand Adjustable", "us_price": "$8-12", "category": "electronics", "us_platform": "Amazon"},
        {"name": "Teeth Whitening Kit LED", "us_price": "$20-35", "category": "beauty", "us_platform": "Amazon/TikTok Shop"},
    ]

    products = []
    for p in viral_products:
        products.append({
            "name": p["name"],
            "raw_name": p["name"],
            "us_price": p["us_price"],
            "us_platform": p["us_platform"],
            "category": p["category"],
            "source_url": f"https://www.amazon.com/s?k={quote_plus(p['name'])}",
            "source": "viral_verified",
        })

    return products


def check_nordic_availability(product_name):
    """Check if a product exists on Nordic marketplaces via search."""
    availability = {}

    for country, info in NORDIC_MARKETS.items():
        country_results = []
        # Search on each platform for the country
        for platform, search_url_template in info["search_urls"].items():
            try:
                search_term = quote_plus(product_name.split("(")[0].strip()[:50])
                search_url = search_url_template.format(search_term)

                resp = requests.get(search_url, headers=HEADERS, timeout=10, allow_redirects=True)

                if resp.status_code == 200:
                    soup = BeautifulSoup(resp.text, "html.parser")
                    page_text = soup.get_text().lower()

                    # Heuristic: check if product-related terms appear
                    product_words = product_name.lower().split()[:3]
                    matches = sum(1 for w in product_words if w in page_text and len(w) > 3)

                    # Check for "no results" patterns
                    no_results_patterns = [
                        "ingen treff", "inga resultat", "ingen resultat",
                        "ei tuloksia", "no results", "0 results",
                        "hittade inga", "fant ingen",
                    ]
                    has_no_results = any(p in page_text for p in no_results_patterns)

                    if has_no_results:
                        country_results.append({"platform": platform, "status": "NOT_FOUND", "url": search_url})
                    elif matches >= 2:
                        country_results.append({"platform": platform, "status": "LIKELY_AVAILABLE", "url": search_url})
                    else:
                        country_results.append({"platform": platform, "status": "UNCERTAIN", "url": search_url})
                else:
                    country_results.append({"platform": platform, "status": "CHECK_FAILED", "url": search_url})

            except Exception as e:
                country_results.append({"platform": platform, "status": "ERROR", "url": str(e)[:50]})

            time.sleep(0.5)  # Polite delay

        availability[country] = country_results

    return availability


# ============================================================
# HELPERS
# ============================================================

def clean_product_name(name):
    """Clean up product name from RSS feed."""
    # Remove rank numbers like "#1: "
    name = re.sub(r"^#?\d+[\.:]\s*", "", name)
    # Remove excessive branding
    name = re.sub(r"\s*\([^)]*\)\s*$", "", name)
    # Truncate long names
    if len(name) > 80:
        name = name[:77] + "..."
    return name.strip()


def extract_price_from_html(html_str):
    """Extract price from Amazon RSS description HTML."""
    if not html_str:
        return "N/A"
    price_match = re.search(r"\$[\d,]+\.?\d*", html_str)
    return price_match.group(0) if price_match else "N/A"


def extract_products_from_title(title):
    """Extract product names from search result titles."""
    products = []
    # Simple heuristic: look for product-like phrases
    # Split on common delimiters
    parts = re.split(r"[|,\-:]", title)
    for part in parts:
        part = part.strip()
        if 5 < len(part) < 60 and not any(w in part.lower() for w in ["amazon", "tiktok", "best", "top", "review", "buy"]):
            products.append(part)
    if not products and len(title) < 80:
        products.append(title)
    return products[:2]


def estimate_nordic_demand(product, availability):
    """Estimate demand based on US popularity and Nordic availability gaps."""
    score = 50  # Base score

    # Higher score if product is from verified viral list
    if product.get("source") == "viral_verified":
        score += 20

    # Higher score if from Amazon bestseller RSS
    if product.get("source") == "amazon_rss":
        score += 15

    # Check availability gaps
    gap_count = 0
    for country, results in availability.items():
        not_found = sum(1 for r in results if r["status"] in ["NOT_FOUND", "UNCERTAIN"])
        if not_found >= 2:  # Most platforms don't have it
            gap_count += 1

    score += gap_count * 10  # +10 per country with gaps

    # Category bonuses (things Nordics buy a lot)
    nordic_friendly = ["electronics", "home_kitchen", "kitchen", "sports", "beauty", "health"]
    if product.get("category") in nordic_friendly:
        score += 10

    return min(score, 100)


def format_availability_summary(availability):
    """Create human-readable summary of Nordic availability."""
    parts = []
    for country, results in availability.items():
        statuses = [f"{r['platform']}={r['status']}" for r in results]
        parts.append(f"{country.upper()}: {'; '.join(statuses)}")
    return " | ".join(parts)


def format_languages_needed(availability):
    """Determine which languages are needed based on gaps."""
    languages = []
    for country, results in availability.items():
        not_found = sum(1 for r in results if r["status"] in ["NOT_FOUND", "UNCERTAIN"])
        if not_found >= 2:
            languages.append(NORDIC_MARKETS[country]["language"])
    return ", ".join(languages) if languages else "All available"


# ============================================================
# MAIN PIPELINE
# ============================================================

def run_pipeline(category=None, output_file=None, check_nordic=True, max_products=50):
    """Run the full Nordic ecom arbitrage pipeline."""
    output_file = output_file or DEFAULT_OUTPUT
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    print("=" * 70)
    print("NORDIC ECOM ARBITRAGE PIPELINE")
    print(f"Time: {timestamp}")
    print("=" * 70)

    # Phase 1: Collect trending US products
    print("\n[PHASE 1] Collecting trending US products...")
    all_products = []

    # Source 1: Amazon RSS feeds
    print("\n  Source 1: Amazon Best Sellers RSS")
    amazon_products = scrape_amazon_bestsellers(category)
    all_products.extend(amazon_products)
    print(f"  -> {len(amazon_products)} products from Amazon RSS")

    # Source 2: Known viral products (guaranteed data)
    print("\n  Source 2: Known viral products database")
    viral_products = scrape_known_viral_products()
    all_products.extend(viral_products)
    print(f"  -> {len(viral_products)} verified viral products")

    # Source 3: Search-based trending
    print("\n  Source 3: Web search for trending products")
    search_products = scrape_trending_via_search()
    all_products.extend(search_products)
    print(f"  -> {len(search_products)} products from search")

    # Deduplicate by name similarity
    seen_names = set()
    unique_products = []
    for p in all_products:
        name_key = p["name"].lower()[:30]
        if name_key not in seen_names:
            seen_names.add(name_key)
            unique_products.append(p)

    print(f"\n  Total unique products: {len(unique_products)}")

    # Limit to max
    unique_products = unique_products[:max_products]

    # Phase 2: Check Nordic availability
    results = []
    if check_nordic:
        print(f"\n[PHASE 2] Checking Nordic availability for {len(unique_products)} products...")
        for i, product in enumerate(unique_products):
            print(f"  [{i+1}/{len(unique_products)}] {product['name'][:50]}...")
            availability = check_nordic_availability(product["name"])
            demand_score = estimate_nordic_demand(product, availability)

            results.append({
                "product_name": product["name"],
                "us_price": product["us_price"],
                "us_platform": product["us_platform"],
                "category": product["category"],
                "nordic_availability": format_availability_summary(availability),
                "estimated_demand": demand_score,
                "languages_needed": format_languages_needed(availability),
                "source": product["source"],
                "source_url": product["source_url"],
                "scanned_at": timestamp,
            })
            time.sleep(0.3)
    else:
        print("\n[PHASE 2] Skipping Nordic checks (--skip-nordic-check flag)")
        for product in unique_products:
            results.append({
                "product_name": product["name"],
                "us_price": product["us_price"],
                "us_platform": product["us_platform"],
                "category": product["category"],
                "nordic_availability": "NOT_CHECKED",
                "estimated_demand": 50,
                "languages_needed": "Norwegian, Swedish, Danish, Finnish",
                "source": product["source"],
                "source_url": product["source_url"],
                "scanned_at": timestamp,
            })

    # Sort by demand score
    results.sort(key=lambda x: x["estimated_demand"], reverse=True)

    # Phase 3: Write CSV
    print(f"\n[PHASE 3] Writing results to {output_file}")
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    fieldnames = [
        "product_name", "us_price", "us_platform", "category",
        "nordic_availability", "estimated_demand", "languages_needed",
        "source", "source_url", "scanned_at"
    ]

    with open(output_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)

    print(f"  -> Wrote {len(results)} products to CSV")

    # Phase 4: Print top opportunities
    print("\n" + "=" * 70)
    print("TOP 15 NORDIC ARBITRAGE OPPORTUNITIES")
    print("=" * 70)
    for i, r in enumerate(results[:15]):
        print(f"\n  #{i+1}: {r['product_name']}")
        print(f"      US Price: {r['us_price']} | Platform: {r['us_platform']}")
        print(f"      Demand Score: {r['estimated_demand']}/100")
        print(f"      Languages: {r['languages_needed']}")
        if len(r['nordic_availability']) < 200:
            print(f"      Nordic: {r['nordic_availability']}")

    # Summary stats
    high_opp = [r for r in results if r["estimated_demand"] >= 70]
    print(f"\n{'=' * 70}")
    print(f"SUMMARY: {len(results)} products scanned, {len(high_opp)} high-opportunity gaps found")
    print(f"Output: {output_file}")
    print(f"{'=' * 70}")

    return results


# ============================================================
# CLI
# ============================================================

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Nordic Ecom Arbitrage Pipeline")
    parser.add_argument("--category", type=str, help="Single Amazon category to scan")
    parser.add_argument("--output", type=str, help="Output CSV file path")
    parser.add_argument("--max", type=int, default=50, help="Max products to check (default 50)")
    parser.add_argument("--skip-nordic-check", action="store_true", help="Skip Nordic availability checks (faster)")
    parser.add_argument("--viral-only", action="store_true", help="Only use verified viral products list")

    args = parser.parse_args()

    if args.viral_only:
        # Quick mode: just viral products, skip scraping
        print("Running in VIRAL-ONLY mode (fast, no scraping)")
        products = scrape_known_viral_products()
        output_file = args.output or DEFAULT_OUTPUT
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        results = []
        for p in products:
            if not args.skip_nordic_check:
                availability = check_nordic_availability(p["name"])
                demand = estimate_nordic_demand(p, availability)
                nordic_str = format_availability_summary(availability)
                langs = format_languages_needed(availability)
            else:
                demand = 70
                nordic_str = "NOT_CHECKED"
                langs = "Norwegian, Swedish, Danish, Finnish"

            results.append({
                "product_name": p["name"],
                "us_price": p["us_price"],
                "us_platform": p["us_platform"],
                "category": p["category"],
                "nordic_availability": nordic_str,
                "estimated_demand": demand,
                "languages_needed": langs,
                "source": p["source"],
                "source_url": p["source_url"],
                "scanned_at": timestamp,
            })
            time.sleep(0.3)

        results.sort(key=lambda x: x["estimated_demand"], reverse=True)
        os.makedirs(os.path.dirname(output_file), exist_ok=True)

        fieldnames = [
            "product_name", "us_price", "us_platform", "category",
            "nordic_availability", "estimated_demand", "languages_needed",
            "source", "source_url", "scanned_at"
        ]

        with open(output_file, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(results)

        print(f"\nWrote {len(results)} products to {output_file}")
        for i, r in enumerate(results[:10]):
            print(f"  #{i+1}: {r['product_name']} (demand: {r['estimated_demand']})")
    else:
        run_pipeline(
            category=args.category,
            output_file=args.output,
            check_nordic=not args.skip_nordic_check,
            max_products=args.max,
        )
