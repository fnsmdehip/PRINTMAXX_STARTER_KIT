#!/usr/bin/env python3

from __future__ import annotations
"""
ProductHunt B2B Launch Scraper
===============================
New B2B SaaS that just launched need customers immediately.
They have zero outbound, small teams, and burning cash.
Perfect targets for outbound services, dev tools, marketing, etc.

Uses ProductHunt's public GraphQL API (no auth needed for basic queries)
and search engine fallback.

Usage:
    python3 producthunt_scraper.py
    python3 producthunt_scraper.py --days 7
    python3 producthunt_scraper.py --categories "SaaS" "Developer Tools" "Marketing"
"""

import argparse
import csv
import json
import os
import re
import sys
import time
from datetime import datetime, timedelta
from pathlib import Path
from urllib.parse import quote_plus, urlparse, parse_qs

try:
    import requests
except ImportError:
    print("ERROR: requests library not found. Install with: pip3 install requests")
    sys.exit(1)

try:
    from bs4 import BeautifulSoup
except ImportError:
    print("ERROR: beautifulsoup4 not found. Install with: pip3 install beautifulsoup4")
    sys.exit(1)

# --- Config ---
OUTPUT_DIR = Path(__file__).parent / "leads"
OUTPUT_FILE = OUTPUT_DIR / "producthunt_b2b_leads.csv"
RATE_LIMIT_DELAY = 2.0

PH_GRAPHQL_URL = "https://www.producthunt.com/frontend/graphql"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "en-US,en;q=0.9",
    "Content-Type": "application/json",
    "Origin": "https://www.producthunt.com",
    "Referer": "https://www.producthunt.com/",
}

# B2B-relevant categories/topics
B2B_TOPICS = [
    "saas", "b2b", "developer-tools", "marketing", "sales",
    "productivity", "analytics", "artificial-intelligence",
    "api", "automation", "crm", "email", "fintech",
    "project-management", "security", "design-tools",
    "no-code", "open-source", "chrome-extensions",
]


def fetch_producthunt_posts(cursor=None, topic=None):
    """
    Fetch posts from ProductHunt's public GraphQL endpoint.
    No auth required for basic post listing.
    """
    query = """
    query HomefeedQuery($cursor: String, $topic: String) {
        posts(first: 20, after: $cursor, topic: $topic, order: NEWEST) {
            edges {
                node {
                    id
                    name
                    tagline
                    description
                    url
                    slug
                    votesCount
                    commentsCount
                    createdAt
                    featuredAt
                    website
                    reviewsRating
                    reviewsCount
                    topics {
                        edges {
                            node {
                                name
                                slug
                            }
                        }
                    }
                    makers {
                        id
                        name
                        username
                        headline
                    }
                    thumbnail {
                        url
                    }
                }
            }
            pageInfo {
                endCursor
                hasNextPage
            }
        }
    }
    """

    variables = {}
    if cursor:
        variables["cursor"] = cursor
    if topic:
        variables["topic"] = topic

    try:
        resp = requests.post(
            PH_GRAPHQL_URL,
            headers=HEADERS,
            json={"query": query, "variables": variables},
            timeout=15
        )

        if resp.status_code in (401, 403, 429):
            print(f"    ProductHunt API returned {resp.status_code}, using search fallback")
            return None

        resp.raise_for_status()
        data = resp.json()

        if "errors" in data:
            print(f"    GraphQL errors: {data['errors']}")
            return None

        return data.get("data", {}).get("posts", {})

    except requests.exceptions.RequestException as e:
        print(f"    ProductHunt API error: {e}")
        return None


def scrape_producthunt_page(days_back=7):
    """
    Scrape ProductHunt directly for recent launches.
    """
    products = []

    for day_offset in range(days_back):
        date = datetime.now() - timedelta(days=day_offset)
        date_str = date.strftime("%Y-%m-%d")
        url = f"https://www.producthunt.com/leaderboard/daily/{date.year}/{date.month}/{date.day}"

        try:
            resp = requests.get(url, headers={
                "User-Agent": HEADERS["User-Agent"],
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            }, timeout=15)

            if resp.status_code in (403, 429):
                print(f"    PH blocked direct access for {date_str}")
                continue

            resp.raise_for_status()
            soup = BeautifulSoup(resp.text, "html.parser")

            # Try to extract products from the page
            # PH uses React, so we may need to find JSON data
            script_tags = soup.find_all("script", type="application/json")
            for script in script_tags:
                try:
                    data = json.loads(script.string)
                    # Look for product data in the JSON
                    if isinstance(data, dict):
                        # ProductHunt embeds data in various ways
                        products_data = _extract_products_from_json(data, date_str)
                        products.extend(products_data)
                except (json.JSONDecodeError, TypeError):
                    continue

            # Also try traditional HTML parsing
            for item in soup.select('[data-test="post-item"], .styles_item__Dk_nz, [class*="post-item"]'):
                product = _extract_product_from_html(item, date_str)
                if product:
                    products.append(product)

            time.sleep(RATE_LIMIT_DELAY)

        except requests.exceptions.RequestException as e:
            print(f"    Error scraping PH for {date_str}: {e}")

    return products


def _extract_products_from_json(data, date_str):
    """Recursively search JSON for product data."""
    products = []

    if isinstance(data, dict):
        # Check if this dict looks like a product
        if "name" in data and ("tagline" in data or "votesCount" in data):
            products.append({
                "product_name": data.get("name", ""),
                "tagline": data.get("tagline", ""),
                "description": data.get("description", ""),
                "votes": data.get("votesCount", 0),
                "comments": data.get("commentsCount", 0),
                "website": data.get("website", ""),
                "launch_date": date_str,
                "slug": data.get("slug", ""),
                "makers": ", ".join(m.get("name", "") for m in data.get("makers", []) if isinstance(m, dict)),
            })

        # Recurse into values
        for v in data.values():
            if isinstance(v, (dict, list)):
                products.extend(_extract_products_from_json(v, date_str))

    elif isinstance(data, list):
        for item in data:
            if isinstance(item, (dict, list)):
                products.extend(_extract_products_from_json(item, date_str))

    return products


def _extract_product_from_html(item, date_str):
    """Extract product from HTML element."""
    product = {"launch_date": date_str}

    name_el = item.select_one('a[href*="/posts/"], h3, [class*="title"]')
    if name_el:
        product["product_name"] = name_el.get_text(strip=True)
        href = name_el.get("href", "")
        if href:
            product["ph_url"] = f"https://www.producthunt.com{href}" if href.startswith("/") else href

    tagline_el = item.select_one('[class*="tagline"], p')
    if tagline_el:
        product["tagline"] = tagline_el.get_text(strip=True)

    votes_el = item.select_one('[class*="vote"], [class*="count"]')
    if votes_el:
        votes_text = votes_el.get_text(strip=True)
        votes_match = re.search(r'\d+', votes_text)
        if votes_match:
            product["votes"] = int(votes_match.group())

    return product if product.get("product_name") else None


def search_google(query, max_results=20):
    """Search Google and parse results."""
    results = []
    url = f"https://www.google.com/search?q={quote_plus(query)}&num={max_results}"

    try:
        resp = requests.get(url, headers={
            "User-Agent": HEADERS["User-Agent"],
            "Accept": "text/html",
        }, timeout=15)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")

        for g in soup.select("div.g, div[data-hveid]"):
            title_tag = g.select_one("h3")
            link_tag = g.select_one("a[href]")
            snippet_tag = g.select_one("div.VwiC3b, span.aCOpRe, div[data-sncf]")

            if not title_tag or not link_tag:
                continue

            href = link_tag.get("href", "")
            if href.startswith("/url?q="):
                href = href.split("/url?q=")[1].split("&")[0]
            if not href.startswith("http"):
                continue

            results.append({
                "title": title_tag.get_text(strip=True),
                "url": href,
                "snippet": snippet_tag.get_text(strip=True) if snippet_tag else ""
            })

            if len(results) >= max_results:
                break

    except requests.exceptions.RequestException as e:
        print(f"    Google search error: {e}")

    return results


def search_duckduckgo(query, max_results=20):
    """DuckDuckGo fallback."""
    results = []
    url = f"https://html.duckduckgo.com/html/?q={quote_plus(query)}"

    try:
        resp = requests.get(url, headers={
            "User-Agent": HEADERS["User-Agent"],
            "Accept": "text/html",
        }, timeout=15)
        if resp.status_code == 403:
            return results
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")

        for result_div in soup.select(".result"):
            title_tag = result_div.select_one(".result__title a, .result__a")
            snippet_tag = result_div.select_one(".result__snippet")
            if not title_tag:
                continue

            title = title_tag.get_text(strip=True)
            href = title_tag.get("href", "")
            if "uddg=" in href:
                parsed = parse_qs(urlparse(href).query)
                actual_url = parsed.get("uddg", [href])[0]
            else:
                actual_url = href

            snippet = snippet_tag.get_text(strip=True) if snippet_tag else ""
            results.append({"title": title, "url": actual_url, "snippet": snippet})
            if len(results) >= max_results:
                break

    except requests.exceptions.RequestException:
        pass

    return results


def search_engine_fallback(days_back=7):
    """
    Use search engines to find recent ProductHunt launches.
    Uses Google as primary, DuckDuckGo as fallback.
    """
    products = []
    queries = [
        'site:producthunt.com "B2B" launched 2026',
        'site:producthunt.com "SaaS" product 2026',
        'site:producthunt.com developer tools 2026',
        'site:producthunt.com "just launched" B2B saas',
        'producthunt.com launch marketing sales automation 2026',
        'site:producthunt.com "AI" tool February 2026',
        'site:producthunt.com "open source" 2026',
        'site:producthunt.com CRM analytics automation 2026',
        'producthunt.com new B2B SaaS startup launched',
    ]

    for query in queries:
        print(f"  Searching: {query[:70]}...")

        # Try Google first, then DuckDuckGo
        results = search_google(query, max_results=15)
        if not results:
            time.sleep(1)
            results = search_duckduckgo(query, max_results=15)

        for result in results:
            title = result.get("title", "")
            actual_url = result.get("url", "")
            snippet = result.get("snippet", "")

            if "producthunt.com" not in actual_url:
                continue

            product = extract_product_from_search(title, actual_url, snippet)
            if product:
                products.append(product)

        time.sleep(RATE_LIMIT_DELAY)

    return products


def extract_product_from_search(title, url, snippet):
    """Extract product info from search result."""
    # Skip non-product pages
    skip_patterns = ["/categories", "/topics", "/newsletter", "/stories", "/about", "/ship"]
    if any(p in url for p in skip_patterns):
        return None

    product = {
        "ph_url": url,
        "source": "search",
    }

    # Extract product name from title
    # Common pattern: "Product Name - Tagline | Product Hunt"
    title_clean = re.sub(r'\s*\|\s*Product Hunt\s*$', '', title, flags=re.IGNORECASE)
    parts = re.split(r'\s*[-]\s*', title_clean, maxsplit=1)
    product["product_name"] = parts[0].strip()
    if len(parts) > 1:
        product["tagline"] = parts[1].strip()

    # Extract info from snippet
    product["description"] = snippet[:300]

    # Try to find vote count
    votes_match = re.search(r'(\d+)\s*(?:upvotes?|votes?)', snippet, re.IGNORECASE)
    if votes_match:
        product["votes"] = int(votes_match.group(1))

    # Try to find launch date
    date_match = re.search(r'((?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\w*\s+\d{1,2},?\s*\d{4})', snippet)
    if date_match:
        product["launch_date"] = date_match.group(1)

    # Determine if B2B
    b2b_signals = ["b2b", "saas", "business", "team", "enterprise", "startup",
                   "productivity", "analytics", "crm", "api", "developer",
                   "marketing", "sales", "automation", "workflow"]
    text_lower = (product.get("product_name", "") + " " + snippet).lower()

    b2b_score = sum(1 for s in b2b_signals if s in text_lower)
    product["b2b_score"] = b2b_score
    product["is_b2b"] = b2b_score >= 2

    return product


def classify_product_lead(product):
    """
    Classify product as a lead based on signals.
    """
    lead_quality = "MEDIUM"
    signals = []

    votes = product.get("votes", 0) or 0

    # Low votes = small team, desperate for customers
    if votes < 50:
        signals.append("LOW_TRACTION")
        lead_quality = "HIGH"
    elif votes < 200:
        signals.append("EARLY_TRACTION")
        lead_quality = "HIGH"
    elif votes > 500:
        signals.append("VIRAL_LAUNCH")
        lead_quality = "MEDIUM"  # probably already have funding/resources

    # B2B signals
    if product.get("is_b2b"):
        signals.append("B2B_PRODUCT")
        lead_quality = "HIGH"

    # Has maker info (can reach out directly)
    if product.get("makers"):
        signals.append("MAKER_IDENTIFIED")

    # Has website (can research further)
    if product.get("website"):
        signals.append("HAS_WEBSITE")

    product["lead_quality"] = lead_quality
    product["lead_signals"] = "; ".join(signals)

    return product


def write_csv(products, output_path):
    """Write products to CSV."""
    if not products:
        print("No products to write.")
        return

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    columns = [
        "product_name", "tagline", "description", "website",
        "votes", "comments", "launch_date",
        "makers", "is_b2b", "b2b_score",
        "lead_quality", "lead_signals",
        "ph_url", "slug", "topics",
        "source", "scraped_at"
    ]

    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=columns, extrasaction="ignore")
        writer.writeheader()
        for product in products:
            product["scraped_at"] = datetime.now().isoformat()
            writer.writerow(product)

    print(f"\nWrote {len(products)} product leads to {output_path}")


def print_summary(products):
    """Print summary."""
    if not products:
        print("No products found.")
        return

    print("\n" + "=" * 70)
    print("PRODUCTHUNT B2B LAUNCH SCRAPE SUMMARY")
    print("=" * 70)
    print(f"Total products found: {len(products)}")

    # B2B vs all
    b2b = [p for p in products if p.get("is_b2b")]
    print(f"B2B products: {len(b2b)}")

    # By lead quality
    by_quality = {}
    for p in products:
        q = p.get("lead_quality", "Unknown")
        by_quality[q] = by_quality.get(q, 0) + 1

    print(f"\nBy lead quality:")
    for q, count in sorted(by_quality.items(), key=lambda x: x[1], reverse=True):
        print(f"  {q}: {count}")

    # Top products by votes
    voted = [p for p in products if p.get("votes")]
    if voted:
        voted_sorted = sorted(voted, key=lambda x: int(x.get("votes", 0) or 0), reverse=True)
        print(f"\nTop launches by votes:")
        for i, p in enumerate(voted_sorted[:15]):
            print(f"  {i+1}. {p['product_name'][:40]:40s} {p.get('votes', 0):>5} votes  {'B2B' if p.get('is_b2b') else '   '}")

    # Products with makers identified
    with_makers = [p for p in products if p.get("makers")]
    print(f"\nProducts with maker contact: {len(with_makers)}")

    print("=" * 70)


def main():
    parser = argparse.ArgumentParser(description="ProductHunt B2B Launch Scraper")
    parser.add_argument("--days", type=int, default=7, help="Days back to search (default: 7)")
    parser.add_argument("--topics", nargs="+", help="ProductHunt topics to filter")
    parser.add_argument("--output", type=str, default=str(OUTPUT_FILE))
    parser.add_argument("--b2b-only", action="store_true", help="Only show B2B products")

    args = parser.parse_args()

    print("=" * 70)
    print("PRODUCTHUNT B2B LAUNCH SCRAPER")
    print("=" * 70)
    print("Strategy: New B2B SaaS that just launched need customers immediately.")
    print("They have zero outbound, small teams, and are burning cash.\n")

    all_products = []

    # Method 1: Try GraphQL API
    print("Method 1: ProductHunt GraphQL API...")
    topics = args.topics or B2B_TOPICS[:5]  # limit to avoid rate limits

    for topic in topics:
        print(f"  Topic: {topic}")
        data = fetch_producthunt_posts(topic=topic)

        if data and data.get("edges"):
            for edge in data["edges"]:
                node = edge.get("node", {})
                product = {
                    "product_name": node.get("name", ""),
                    "tagline": node.get("tagline", ""),
                    "description": node.get("description", "")[:300],
                    "votes": node.get("votesCount", 0),
                    "comments": node.get("commentsCount", 0),
                    "website": node.get("website", ""),
                    "launch_date": node.get("createdAt", "")[:10],
                    "slug": node.get("slug", ""),
                    "ph_url": f"https://www.producthunt.com/posts/{node.get('slug', '')}",
                    "makers": ", ".join(m.get("name", "") for m in node.get("makers", [])),
                    "topics": ", ".join(t["node"]["name"] for t in node.get("topics", {}).get("edges", []) if "node" in t),
                    "source": "graphql_api",
                    "b2b_score": 2,  # already filtered by B2B topics
                    "is_b2b": True,
                }
                all_products.append(product)

            print(f"    Got {len(data['edges'])} products")
        else:
            print(f"    No data from API")

        time.sleep(RATE_LIMIT_DELAY)

    # Method 2: Direct page scraping
    if len(all_products) < 20:
        print(f"\nMethod 2: Direct page scraping (last {args.days} days)...")
        scraped = scrape_producthunt_page(days_back=args.days)
        print(f"  Got {len(scraped)} products from page scraping")
        all_products.extend(scraped)

    # Method 3: Search engine fallback
    print(f"\nMethod 3: Search engine fallback...")
    search_products = search_engine_fallback(days_back=args.days)
    print(f"  Got {len(search_products)} products from search")
    all_products.extend(search_products)

    # Deduplicate
    seen = set()
    deduped = []
    for p in all_products:
        key = p.get("product_name", "").lower().strip()
        if key and key not in seen:
            seen.add(key)
            deduped.append(p)
    all_products = deduped

    # Classify leads
    for p in all_products:
        classify_product_lead(p)

    # Filter B2B only if requested
    if args.b2b_only:
        all_products = [p for p in all_products if p.get("is_b2b")]

    print(f"\n{len(all_products)} unique products after deduplication")

    print_summary(all_products)
    write_csv(all_products, args.output)

    print(f"\nNext steps:")
    print(f"  1. Filter for B2B products with <200 votes (need customers badly)")
    print(f"  2. Visit their website, find founder LinkedIn/Twitter")
    print(f"  3. Cold email: 'Congrats on the PH launch! Noticed you're building [category].'")
    print(f"  4. Offer: first 50 users free, affiliate deal, co-marketing")
    print(f"  5. Speed matters: reach out within 48 hours of launch")


if __name__ == "__main__":
    main()
