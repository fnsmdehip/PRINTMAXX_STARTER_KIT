#!/usr/bin/env python3
"""
LinkedIn Events Lead Scraper (via Search Engines)
==================================================
LinkedIn blocks direct scraping. This tool uses DuckDuckGo HTML search
to find LinkedIn Events for specific industries/keywords.

People who attend industry webinars have "raised their hand" saying
they have a problem. These are warm outbound leads.

Usage:
    python3 linkedin_events_scraper.py
    python3 linkedin_events_scraper.py --keywords "sales automation" "CRM"
    python3 linkedin_events_scraper.py --industries "SaaS" "cybersecurity" "fintech"
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
OUTPUT_FILE = OUTPUT_DIR / "linkedin_events_leads.csv"
RATE_LIMIT_DELAY = 2.0  # be polite to search engines

# Default industry + keyword combos to search
DEFAULT_SEARCHES = [
    {"industry": "SaaS", "keywords": ["sales automation", "growth marketing", "product-led growth"]},
    {"industry": "Cybersecurity", "keywords": ["CISO summit", "security operations", "zero trust"]},
    {"industry": "AI/ML", "keywords": ["generative AI", "machine learning", "AI strategy"]},
    {"industry": "Fintech", "keywords": ["payment processing", "neobank", "financial compliance"]},
    {"industry": "Healthcare IT", "keywords": ["health tech", "EHR integration", "telehealth"]},
    {"industry": "eCommerce", "keywords": ["D2C brands", "Shopify scaling", "ecommerce operations"]},
    {"industry": "HR Tech", "keywords": ["talent acquisition", "employee engagement", "HR automation"]},
    {"industry": "Cloud Infrastructure", "keywords": ["cloud migration", "DevOps", "kubernetes"]},
    {"industry": "Sales/RevOps", "keywords": ["outbound sales", "revenue operations", "SDR training"]},
    {"industry": "Marketing", "keywords": ["B2B marketing", "demand generation", "ABM strategy"]},
]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
}


def search_google(query, max_results=20):
    """Search Google and parse results from HTML."""
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


def search_duckduckgo_html(query, max_results=20):
    """
    Search DuckDuckGo HTML version (fallback).
    Returns list of {title, url, snippet}.
    """
    results = []
    url = f"https://html.duckduckgo.com/html/?q={quote_plus(query)}"

    try:
        resp = requests.get(url, headers=HEADERS, timeout=15)
        if resp.status_code == 403:
            print(f"    DDG rate limited, skipping")
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


def search_brave(query, max_results=20):
    """
    Fallback: Search Brave Search web (no API key, scrape HTML).
    """
    results = []
    url = f"https://search.brave.com/search?q={quote_plus(query)}"

    try:
        resp = requests.get(url, headers=HEADERS, timeout=15)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")

        for item in soup.select(".snippet"):
            title_tag = item.select_one(".snippet-title")
            url_tag = item.select_one("a")
            desc_tag = item.select_one(".snippet-description")

            if not title_tag or not url_tag:
                continue

            results.append({
                "title": title_tag.get_text(strip=True),
                "url": url_tag.get("href", ""),
                "snippet": desc_tag.get_text(strip=True) if desc_tag else ""
            })

            if len(results) >= max_results:
                break

    except requests.exceptions.RequestException as e:
        print(f"  ERROR searching Brave: {e}")

    return results


def extract_linkedin_event_data(result):
    """
    Parse a search result and extract LinkedIn event details.
    Returns dict with event info or None if not a LinkedIn event.
    """
    url = result.get("url", "")
    title = result.get("title", "")
    snippet = result.get("snippet", "")

    # Must be a LinkedIn events URL
    if "linkedin.com/events" not in url and "linkedin.com/event" not in url:
        return None

    # Extract event ID from URL
    event_id = ""
    match = re.search(r'/events?/([^/?]+)', url)
    if match:
        event_id = match.group(1)

    # Try to extract attendee count from snippet
    attendee_count = ""
    attendee_match = re.search(r'(\d[\d,]*)\s*(?:attendees?|going|interested|registered)', snippet, re.IGNORECASE)
    if attendee_match:
        attendee_count = attendee_match.group(1).replace(",", "")

    # Try to extract date from snippet
    event_date = ""
    date_patterns = [
        r'(\w+ \d{1,2},?\s*\d{4})',
        r'(\d{1,2}/\d{1,2}/\d{2,4})',
        r'(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\w*\s+\d{1,2}',
    ]
    for pattern in date_patterns:
        date_match = re.search(pattern, snippet)
        if date_match:
            event_date = date_match.group(0)
            break

    # Try to extract organizer from title or snippet
    organizer = ""
    org_match = re.search(r'(?:hosted by|organized by|presented by|by)\s+([^|.\n]+)', snippet, re.IGNORECASE)
    if org_match:
        organizer = org_match.group(1).strip()

    # Clean up title - remove "| LinkedIn" suffix
    clean_title = re.sub(r'\s*\|\s*LinkedIn\s*$', '', title).strip()

    return {
        "event_title": clean_title,
        "event_url": url,
        "event_id": event_id,
        "attendee_count": attendee_count,
        "event_date": event_date,
        "organizer": organizer,
        "snippet": snippet[:300],
    }


def search_linkedin_events(industry, keyword, max_results=15):
    """
    Search for LinkedIn events matching industry + keyword.
    Uses multiple query patterns for better coverage.
    """
    queries = [
        f'site:linkedin.com/events "{keyword}" {industry}',
        f'site:linkedin.com/events {industry} {keyword} 2026',
        f'site:linkedin.com/events {keyword} webinar',
        f'linkedin.com events "{keyword}" summit conference',
    ]

    all_events = []
    seen_urls = set()

    for query in queries:
        print(f"    Searching: {query[:80]}...")
        results = search_google(query, max_results=max_results)

        if not results:
            # Fallback to DuckDuckGo
            results = search_duckduckgo_html(query, max_results=max_results)

        for result in results:
            event = extract_linkedin_event_data(result)
            if event and event["event_url"] not in seen_urls:
                event["industry"] = industry
                event["search_keyword"] = keyword
                seen_urls.add(event["event_url"])
                all_events.append(event)

        time.sleep(RATE_LIMIT_DELAY)

    return all_events


def write_csv(events, output_path):
    """Write events to CSV."""
    if not events:
        print("No events to write.")
        return

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    columns = [
        "event_title", "industry", "search_keyword", "attendee_count",
        "event_date", "organizer", "event_url", "event_id", "snippet",
        "scraped_at"
    ]

    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=columns, extrasaction="ignore")
        writer.writeheader()
        for event in events:
            event["scraped_at"] = datetime.now().isoformat()
            writer.writerow(event)

    print(f"\nWrote {len(events)} events to {output_path}")


def print_summary(events):
    """Print summary stats."""
    if not events:
        print("No events found.")
        return

    print("\n" + "=" * 70)
    print("LINKEDIN EVENTS SCRAPE SUMMARY")
    print("=" * 70)
    print(f"Total events found: {len(events)}")

    # By industry
    by_industry = {}
    for e in events:
        ind = e.get("industry", "Unknown")
        by_industry[ind] = by_industry.get(ind, 0) + 1

    print(f"\nBy industry:")
    for ind, count in sorted(by_industry.items(), key=lambda x: x[1], reverse=True):
        print(f"  {ind}: {count} events")

    # Events with attendee counts
    with_attendees = [e for e in events if e.get("attendee_count")]
    if with_attendees:
        counts = [int(e["attendee_count"]) for e in with_attendees]
        print(f"\nEvents with attendee data: {len(with_attendees)}")
        print(f"  Total attendees: {sum(counts):,}")
        print(f"  Average per event: {sum(counts)//len(counts):,}")
        print(f"  Largest event: {max(counts):,} attendees")

    # Top 10
    print(f"\nTop events:")
    sorted_events = sorted(events, key=lambda x: int(x.get("attendee_count", 0) or 0), reverse=True)
    for i, e in enumerate(sorted_events[:10]):
        attendees = e.get("attendee_count", "?")
        print(f"  {i+1}. [{e['industry']}] {e['event_title'][:60]} ({attendees} attendees)")

    print("=" * 70)


def main():
    parser = argparse.ArgumentParser(description="LinkedIn Events Lead Scraper (via Search Engines)")
    parser.add_argument("--keywords", nargs="+", help="Keywords to search for")
    parser.add_argument("--industries", nargs="+", help="Industries to search within")
    parser.add_argument("--output", type=str, default=str(OUTPUT_FILE), help=f"Output CSV (default: {OUTPUT_FILE})")
    parser.add_argument("--max-results", type=int, default=15, help="Max results per query (default: 15)")

    args = parser.parse_args()

    print("=" * 70)
    print("LINKEDIN EVENTS LEAD SCRAPER")
    print("=" * 70)
    print("Strategy: Find industry events on LinkedIn via search engines.")
    print("Attendees = warm leads who raised their hand about a problem.\n")

    all_events = []

    if args.keywords and args.industries:
        # Custom search
        searches = [{"industry": ind, "keywords": args.keywords} for ind in args.industries]
    elif args.keywords:
        searches = [{"industry": "General", "keywords": args.keywords}]
    elif args.industries:
        # Use default keywords for specified industries
        searches = []
        for ind in args.industries:
            matching = [s for s in DEFAULT_SEARCHES if s["industry"].lower() == ind.lower()]
            if matching:
                searches.extend(matching)
            else:
                searches.append({"industry": ind, "keywords": [ind]})
    else:
        searches = DEFAULT_SEARCHES

    total_searches = sum(len(s["keywords"]) for s in searches)
    print(f"Running {total_searches} searches across {len(searches)} industries...\n")

    for search in searches:
        industry = search["industry"]
        print(f"\n--- {industry} ---")

        for keyword in search["keywords"]:
            events = search_linkedin_events(industry, keyword, max_results=args.max_results)
            print(f"  Found {len(events)} events for '{keyword}'")
            all_events.extend(events)

    # Deduplicate by URL
    seen = set()
    deduped = []
    for event in all_events:
        if event["event_url"] not in seen:
            seen.add(event["event_url"])
            deduped.append(event)

    all_events = deduped
    print(f"\n{len(all_events)} unique events after deduplication")

    print_summary(all_events)
    write_csv(all_events, args.output)

    print(f"\nNext steps:")
    print(f"  1. Review events CSV for high-value industry events")
    print(f"  2. Visit event pages to see attendee lists (requires LinkedIn login)")
    print(f"  3. Export attendees via LinkedIn Sales Navigator or manual review")
    print(f"  4. Cold email attendees referencing the specific event they attended")
    print(f"  5. Angle: 'I saw you attended [event]. We solve [problem from event topic].'")


if __name__ == "__main__":
    main()
