#!/usr/bin/env python3
"""
G2 Reviewer Lead Scraper
=========================
People who reviewed competitor products on G2 are ACTIVELY evaluating solutions.
This is one of the highest-intent lead sources that exists for free.

Uses DuckDuckGo to find G2 review pages and extracts reviewer details
from search snippets.

Usage:
    python3 g2_reviewer_scraper.py
    python3 g2_reviewer_scraper.py --products "salesforce" "hubspot" "outreach"
    python3 g2_reviewer_scraper.py --categories "sales-automation" "crm" "email-marketing"
"""

import argparse
import csv
import json
import os
import re
import sys
import time
from datetime import datetime
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
OUTPUT_FILE = OUTPUT_DIR / "g2_reviewer_leads.csv"
RATE_LIMIT_DELAY = 2.5  # be polite

# Competitor products to scrape reviews for (G2 product slugs)
DEFAULT_PRODUCTS = [
    # CRM
    {"slug": "salesforce-sales-cloud", "category": "CRM", "name": "Salesforce"},
    {"slug": "hubspot-crm", "category": "CRM", "name": "HubSpot CRM"},
    {"slug": "pipedrive", "category": "CRM", "name": "Pipedrive"},
    # Sales Engagement
    {"slug": "outreach", "category": "Sales Engagement", "name": "Outreach"},
    {"slug": "salesloft", "category": "Sales Engagement", "name": "SalesLoft"},
    {"slug": "apollo-io", "category": "Sales Engagement", "name": "Apollo.io"},
    {"slug": "lemlist", "category": "Sales Engagement", "name": "Lemlist"},
    # Email Marketing
    {"slug": "mailchimp", "category": "Email Marketing", "name": "Mailchimp"},
    {"slug": "activecampaign", "category": "Email Marketing", "name": "ActiveCampaign"},
    {"slug": "convertkit", "category": "Email Marketing", "name": "ConvertKit"},
    # Marketing Automation
    {"slug": "marketo", "category": "Marketing Automation", "name": "Marketo"},
    {"slug": "pardot", "category": "Marketing Automation", "name": "Pardot"},
    # Project Management
    {"slug": "monday-com", "category": "Project Management", "name": "Monday.com"},
    {"slug": "asana", "category": "Project Management", "name": "Asana"},
    {"slug": "clickup", "category": "Project Management", "name": "ClickUp"},
    # Analytics
    {"slug": "amplitude", "category": "Analytics", "name": "Amplitude"},
    {"slug": "mixpanel", "category": "Analytics", "name": "Mixpanel"},
    # Customer Success
    {"slug": "gainsight", "category": "Customer Success", "name": "Gainsight"},
    {"slug": "churnzero", "category": "Customer Success", "name": "ChurnZero"},
    # AI/Automation
    {"slug": "jasper", "category": "AI Writing", "name": "Jasper"},
    {"slug": "copy-ai", "category": "AI Writing", "name": "Copy.ai"},
    {"slug": "zapier", "category": "Automation", "name": "Zapier"},
]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
}


def search_google(query, max_results=30):
    """Search Google and parse results."""
    results = []
    url = f"https://www.google.com/search?q={quote_plus(query)}&num={max_results}"

    try:
        resp = requests.get(url, headers=HEADERS, timeout=15)
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
        print(f"  ERROR searching Google: {e}")

    return results


def search_duckduckgo_html(query, max_results=30):
    """Search DuckDuckGo HTML version (fallback)."""
    results = []
    url = f"https://html.duckduckgo.com/html/?q={quote_plus(query)}"

    try:
        resp = requests.get(url, headers=HEADERS, timeout=15)
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

            results.append({
                "title": title,
                "url": actual_url,
                "snippet": snippet
            })

            if len(results) >= max_results:
                break

    except requests.exceptions.RequestException as e:
        print(f"  ERROR searching DuckDuckGo: {e}")

    return results


def scrape_g2_review_page(product_slug):
    """
    Try to scrape G2 review page directly for structured review data.
    G2 may block this, so we have search fallback.
    """
    reviews = []
    url = f"https://www.g2.com/products/{product_slug}/reviews"

    try:
        resp = requests.get(url, headers={
            **HEADERS,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Referer": "https://www.google.com/",
        }, timeout=15)

        if resp.status_code == 403 or resp.status_code == 429:
            print(f"    G2 blocked direct access (HTTP {resp.status_code}), using search fallback")
            return None

        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")

        # Try to find review cards
        review_cards = soup.select('[itemprop="review"], .paper--white, .nested-ajax-loading')

        for card in review_cards[:20]:
            review = {}

            # Reviewer name
            name_el = card.select_one('[itemprop="author"], .link--header-color')
            if name_el:
                review["reviewer_name"] = name_el.get_text(strip=True)

            # Company/title
            title_el = card.select_one('.mt-4th, [class*="job-title"]')
            if title_el:
                text = title_el.get_text(strip=True)
                review["reviewer_title"] = text

            # Rating
            rating_el = card.select_one('[class*="stars"], [itemprop="ratingValue"]')
            if rating_el:
                val = rating_el.get("content", "") or rating_el.get_text(strip=True)
                review["rating"] = val

            # Review text
            review_text_el = card.select_one('[itemprop="reviewBody"], .formatted-text')
            if review_text_el:
                review["review_text"] = review_text_el.get_text(strip=True)[:500]

            # Date
            date_el = card.select_one('time, [itemprop="datePublished"]')
            if date_el:
                review["review_date"] = date_el.get("datetime", "") or date_el.get_text(strip=True)

            if review.get("reviewer_name") or review.get("review_text"):
                reviews.append(review)

        return reviews if reviews else None

    except requests.exceptions.RequestException as e:
        print(f"    G2 direct scrape failed: {e}")
        return None


def extract_review_data_from_search(result, product_name):
    """
    Extract reviewer information from search result snippets.
    """
    url = result.get("url", "")
    snippet = result.get("snippet", "")
    title = result.get("title", "")

    if "g2.com" not in url:
        return None

    review = {
        "source_url": url,
        "product_reviewed": product_name,
    }

    # Extract reviewer name - common patterns in G2 search results
    name_patterns = [
        r'(?:Review by|Reviewed by|by)\s+([A-Z][a-z]+ [A-Z][a-z]+(?:\s+[A-Z]\.?)?)',
        r'([A-Z][a-z]+ [A-Z][a-z]+)\s+(?:gave|rated|reviewed|says)',
        r'(?:^|\.\s)([A-Z][a-z]+ [A-Z][a-z]+)\s*[-,]',
    ]
    for pattern in name_patterns:
        match = re.search(pattern, snippet)
        if match:
            review["reviewer_name"] = match.group(1).strip()
            break

    # Extract company from snippet
    company_patterns = [
        r'(?:at|from|of|@)\s+([A-Z][A-Za-z0-9\s&.-]+?)(?:\s*[-,.|]|\s+(?:said|says|gave|rated|thinks))',
        r'([A-Z][A-Za-z0-9\s&.-]+?)\s*(?:employee|user|admin|manager)',
    ]
    for pattern in company_patterns:
        match = re.search(pattern, snippet)
        if match:
            company = match.group(1).strip()
            if len(company) < 50 and company.lower() not in ["the", "a", "an"]:
                review["reviewer_company"] = company
                break

    # Extract rating
    rating_patterns = [
        r'(\d(?:\.\d)?)\s*(?:/\s*5|out of 5|stars?)',
        r'Rating:\s*(\d(?:\.\d)?)',
        r'Rated\s+(\d(?:\.\d)?)',
    ]
    for pattern in rating_patterns:
        match = re.search(pattern, snippet, re.IGNORECASE)
        if match:
            review["rating"] = match.group(1)
            break

    # Extract review snippet
    review["review_snippet"] = snippet[:400]

    # Extract job title
    title_patterns = [
        r'(?:is a|works as)\s+([A-Za-z\s]+?)(?:\s+at|\s+from|\s+who)',
        r'([A-Z][a-z]+ (?:Manager|Director|VP|CEO|CTO|CMO|Head|Lead|Senior|Chief|Engineer|Analyst|Coordinator|Specialist))',
    ]
    for pattern in title_patterns:
        match = re.search(pattern, snippet)
        if match:
            review["reviewer_title"] = match.group(1).strip()
            break

    # Determine review sentiment
    positive_words = ["love", "great", "excellent", "amazing", "best", "recommend", "easy"]
    negative_words = ["hate", "terrible", "worst", "frustrating", "expensive", "slow", "poor", "disappointed"]
    snippet_lower = snippet.lower()

    pos_count = sum(1 for w in positive_words if w in snippet_lower)
    neg_count = sum(1 for w in negative_words if w in snippet_lower)

    if neg_count > pos_count:
        review["sentiment"] = "NEGATIVE"
        review["lead_quality"] = "HIGH"  # unhappy users = ready to switch
    elif pos_count > neg_count:
        review["sentiment"] = "POSITIVE"
        review["lead_quality"] = "MEDIUM"  # happy but evaluating
    else:
        review["sentiment"] = "NEUTRAL"
        review["lead_quality"] = "MEDIUM"

    return review


def search_product_reviews(product_slug, product_name, category):
    """
    Search for G2 reviews of a specific product.
    """
    queries = [
        f'site:g2.com/products/{product_slug}/reviews',
        f'site:g2.com "{product_name}" review 2025 OR 2026',
        f'g2.com "{product_name}" reviews "what do you like" OR "what do you dislike"',
        f'site:g2.com/products/{product_slug} "switched from" OR "moved to" OR "replaced"',
    ]

    all_reviews = []

    # First try direct scrape
    print(f"  Trying direct G2 scrape for {product_name}...")
    direct_reviews = scrape_g2_review_page(product_slug)
    if direct_reviews:
        for r in direct_reviews:
            r["product_reviewed"] = product_name
            r["product_slug"] = product_slug
            r["category"] = category
            r["source"] = "g2_direct"
            r["lead_quality"] = "HIGH"
        all_reviews.extend(direct_reviews)
        print(f"    Got {len(direct_reviews)} reviews from direct scrape")

    # Then augment with search
    for query in queries:
        print(f"    Searching: {query[:70]}...")
        results = search_google(query, max_results=20)
        if not results:
            results = search_duckduckgo_html(query, max_results=20)

        for result in results:
            review = extract_review_data_from_search(result, product_name)
            if review:
                review["product_slug"] = product_slug
                review["category"] = category
                review["source"] = "search"
                all_reviews.append(review)

        time.sleep(RATE_LIMIT_DELAY)

    return all_reviews


def write_csv(reviews, output_path):
    """Write reviews to CSV."""
    if not reviews:
        print("No reviews to write.")
        return

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    columns = [
        "product_reviewed", "product_slug", "category",
        "reviewer_name", "reviewer_company", "reviewer_title",
        "rating", "sentiment", "lead_quality",
        "review_snippet", "review_date",
        "source_url", "source", "scraped_at"
    ]

    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=columns, extrasaction="ignore")
        writer.writeheader()
        for review in reviews:
            review["scraped_at"] = datetime.now().isoformat()
            writer.writerow(review)

    print(f"\nWrote {len(reviews)} reviewer leads to {output_path}")


def print_summary(reviews):
    """Print summary."""
    if not reviews:
        print("No reviews found.")
        return

    print("\n" + "=" * 70)
    print("G2 REVIEWER SCRAPE SUMMARY")
    print("=" * 70)
    print(f"Total reviewer leads: {len(reviews)}")

    # By product
    by_product = {}
    for r in reviews:
        prod = r.get("product_reviewed", "Unknown")
        by_product[prod] = by_product.get(prod, 0) + 1

    print(f"\nBy product reviewed:")
    for prod, count in sorted(by_product.items(), key=lambda x: x[1], reverse=True):
        print(f"  {prod}: {count} reviews")

    # By category
    by_cat = {}
    for r in reviews:
        cat = r.get("category", "Unknown")
        by_cat[cat] = by_cat.get(cat, 0) + 1

    print(f"\nBy category:")
    for cat, count in sorted(by_cat.items(), key=lambda x: x[1], reverse=True):
        print(f"  {cat}: {count} reviews")

    # By sentiment
    by_sentiment = {}
    for r in reviews:
        sent = r.get("sentiment", "Unknown")
        by_sentiment[sent] = by_sentiment.get(sent, 0) + 1

    print(f"\nBy sentiment:")
    for sent, count in sorted(by_sentiment.items(), key=lambda x: x[1], reverse=True):
        print(f"  {sent}: {count} reviews")

    # High quality leads
    high_quality = [r for r in reviews if r.get("lead_quality") == "HIGH"]
    print(f"\nHigh quality leads (unhappy users): {len(high_quality)}")

    # Named reviewers
    named = [r for r in reviews if r.get("reviewer_name")]
    print(f"Reviews with names: {len(named)}")

    # Reviews with companies
    with_company = [r for r in reviews if r.get("reviewer_company")]
    print(f"Reviews with company names: {len(with_company)}")

    print("=" * 70)


def main():
    parser = argparse.ArgumentParser(description="G2 Reviewer Lead Scraper")
    parser.add_argument("--products", nargs="+", help="G2 product slugs to search")
    parser.add_argument("--categories", nargs="+", help="Product categories to filter")
    parser.add_argument("--output", type=str, default=str(OUTPUT_FILE))
    parser.add_argument("--max-per-product", type=int, default=30, help="Max reviews per product")

    args = parser.parse_args()

    print("=" * 70)
    print("G2 REVIEWER LEAD SCRAPER")
    print("=" * 70)
    print("Strategy: People reviewing competitor products = actively evaluating.")
    print("Negative reviewers = highest intent (ready to switch).\n")

    products = DEFAULT_PRODUCTS

    if args.products:
        products = [{"slug": p, "category": "Custom", "name": p.replace("-", " ").title()} for p in args.products]
    elif args.categories:
        products = [p for p in DEFAULT_PRODUCTS if p["category"].lower() in [c.lower() for c in args.categories]]

    print(f"Searching {len(products)} products...\n")

    all_reviews = []
    for i, product in enumerate(products):
        print(f"\n[{i+1}/{len(products)}] {product['name']} ({product['category']})")
        reviews = search_product_reviews(product["slug"], product["name"], product["category"])
        print(f"  Found {len(reviews)} reviewer leads")
        all_reviews.extend(reviews)

    # Deduplicate by source_url
    seen = set()
    deduped = []
    for r in all_reviews:
        key = r.get("source_url", "") or f"{r.get('reviewer_name','')}-{r.get('product_reviewed','')}"
        if key not in seen:
            seen.add(key)
            deduped.append(r)

    all_reviews = deduped
    print(f"\n{len(all_reviews)} unique leads after deduplication")

    print_summary(all_reviews)
    write_csv(all_reviews, args.output)

    print(f"\nNext steps:")
    print(f"  1. Filter for NEGATIVE sentiment (highest intent - ready to switch)")
    print(f"  2. Look up reviewer companies on LinkedIn")
    print(f"  3. Find decision makers at those companies")
    print(f"  4. Cold email: 'I saw [company] reviewed [competitor]. We solve [specific complaint].'")
    print(f"  5. Reference their exact G2 complaint in the email for personalization")


if __name__ == "__main__":
    main()
