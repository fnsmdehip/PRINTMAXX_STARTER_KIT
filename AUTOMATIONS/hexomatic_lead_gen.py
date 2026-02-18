#!/usr/bin/env python3
"""
Google Maps Lead Gen Scraper
Source: @pipelineabuser tweet - "hexomatic.com / scrape google maps -> enrich with emails -> verify -> export"

Free alternative: uses Google Maps Places API (via SerpAPI free tier or direct scraping)
to find local businesses, then enriches with email/phone data.

Stacks with: MM070 (Local Biz Website Redesign), MM005 (Cold Outbound)

Usage:
    python3 hexomatic_lead_gen.py --query "dentist" --city "Austin TX"
    python3 hexomatic_lead_gen.py --query "plumber" --city "Denver CO" --radius 20
    python3 hexomatic_lead_gen.py --batch-cities "Austin TX,Denver CO,Miami FL" --query "HVAC"
"""

import argparse
import csv
import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path
from urllib.request import urlopen, Request
from urllib.parse import urlencode, quote
from urllib.error import URLError, HTTPError

BASE_DIR = Path(__file__).parent.parent
OUTPUT_CSV = BASE_DIR / "LEDGER" / "LOCAL_BIZ_LEADS.csv"
LOG_FILE = BASE_DIR / "AUTOMATIONS" / "logs" / "lead_gen.log"

# High-value local business categories (from MM070 Local Biz Redesign)
BUSINESS_CATEGORIES = [
    "dentist",
    "plumber",
    "hvac",
    "electrician",
    "roofing",
    "landscaping",
    "auto repair",
    "personal injury lawyer",
    "real estate agent",
    "chiropractor",
    "veterinarian",
    "accountant",
    "insurance agent",
    "wedding photographer",
    "home remodeling",
]

# Top 30 US cities by population
TOP_CITIES = [
    "New York NY", "Los Angeles CA", "Chicago IL", "Houston TX", "Phoenix AZ",
    "Philadelphia PA", "San Antonio TX", "San Diego CA", "Dallas TX", "Austin TX",
    "Jacksonville FL", "San Jose CA", "Fort Worth TX", "Columbus OH", "Charlotte NC",
    "Indianapolis IN", "San Francisco CA", "Seattle WA", "Denver CO", "Nashville TN",
    "Oklahoma City OK", "Portland OR", "Las Vegas NV", "Memphis TN", "Louisville KY",
    "Baltimore MD", "Milwaukee WI", "Albuquerque NM", "Tucson AZ", "Miami FL",
]


def log(msg):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_msg = f"[{timestamp}] {msg}"
    print(log_msg)
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(LOG_FILE, "a") as f:
        f.write(log_msg + "\n")


def fetch_url(url, headers=None):
    default_headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
        "Accept": "application/json,text/html",
    }
    if headers:
        default_headers.update(headers)
    try:
        req = Request(url, headers=default_headers)
        with urlopen(req, timeout=30) as response:
            return response.read().decode("utf-8", errors="replace")
    except Exception as e:
        log(f"Fetch error for {url}: {e}")
        return None


def search_businesses_ddg(query, city):
    """Search for businesses using DuckDuckGo (free, no API key)."""
    leads = []
    search_query = f"{query} {city} phone email"
    url = f"https://api.duckduckgo.com/?q={quote(search_query)}&format=json"
    data = fetch_url(url)
    if data:
        try:
            result = json.loads(data)
            # Process related topics
            for topic in result.get("RelatedTopics", [])[:10]:
                text = topic.get("Text", "")
                first_url = topic.get("FirstURL", "")
                if text:
                    # Try to extract business info
                    phone_match = re.search(r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}', text)
                    email_match = re.search(r'[\w.+-]+@[\w-]+\.[\w.-]+', text)
                    leads.append({
                        "business_name": text.split(" - ")[0][:100] if " - " in text else text[:100],
                        "category": query,
                        "city": city,
                        "phone": phone_match.group() if phone_match else "",
                        "email": email_match.group() if email_match else "",
                        "website": first_url,
                        "source": "DuckDuckGo",
                        "description": text[:200],
                    })
        except json.JSONDecodeError:
            pass
    return leads


def search_businesses_yelp_fusion(query, city):
    """Search Yelp Fusion API (free tier: 500 calls/day)."""
    api_key = os.environ.get("YELP_API_KEY", "")
    if not api_key:
        return []

    leads = []
    params = urlencode({
        "term": query,
        "location": city,
        "limit": 20,
        "sort_by": "rating",
    })
    url = f"https://api.yelp.com/v3/businesses/search?{params}"
    data = fetch_url(url, headers={"Authorization": f"Bearer {api_key}"})
    if data:
        try:
            result = json.loads(data)
            for biz in result.get("businesses", []):
                leads.append({
                    "business_name": biz.get("name", ""),
                    "category": query,
                    "city": city,
                    "phone": biz.get("phone", ""),
                    "email": "",
                    "website": biz.get("url", ""),
                    "source": "Yelp",
                    "rating": str(biz.get("rating", "")),
                    "review_count": str(biz.get("review_count", "")),
                    "address": ", ".join(biz.get("location", {}).get("display_address", [])),
                    "description": ", ".join([c.get("title", "") for c in biz.get("categories", [])]),
                })
        except json.JSONDecodeError:
            pass
    return leads


def extract_emails_from_website(url):
    """Visit a business website and extract contact emails."""
    if not url or "yelp.com" in url or "duckduckgo" in url:
        return []

    data = fetch_url(url)
    if not data:
        return []

    # Extract emails
    emails = re.findall(r'[\w.+-]+@[\w-]+\.[\w.-]+', data)
    # Filter out common junk emails
    junk_patterns = ["example.com", "wordpress", "schema.org", "w3.org", "google.com",
                     "facebook.com", "twitter.com", "instagram.com", "wix.com", "squarespace.com"]
    clean_emails = [e for e in emails if not any(j in e.lower() for j in junk_patterns)]

    # Also extract phone numbers
    phones = re.findall(r'(?:\+1)?[\s.-]?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}', data)

    return list(set(clean_emails))[:3], list(set(phones))[:3]


def save_leads(leads):
    """Save leads to CSV."""
    OUTPUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    file_exists = OUTPUT_CSV.exists()

    fieldnames = [
        "lead_id", "business_name", "category", "city", "phone", "email",
        "website", "source", "rating", "review_count", "address",
        "description", "found_date", "status", "email_sent", "notes",
    ]

    existing = set()
    if file_exists:
        with open(OUTPUT_CSV, "r") as f:
            for row in csv.DictReader(f):
                existing.add(row.get("business_name", "").lower() + row.get("city", "").lower())

    new_count = 0
    with open(OUTPUT_CSV, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()

        for i, lead in enumerate(leads):
            key = lead.get("business_name", "").lower() + lead.get("city", "").lower()
            if key in existing:
                continue
            existing.add(key)

            lead["lead_id"] = f"LBZ_{datetime.now().strftime('%Y%m%d')}_{i:04d}"
            lead["found_date"] = datetime.now().strftime("%Y-%m-%d")
            lead["status"] = "NEW"
            lead["email_sent"] = "NO"
            lead.setdefault("notes", "")
            lead.setdefault("rating", "")
            lead.setdefault("review_count", "")
            lead.setdefault("address", "")

            clean = {k: lead.get(k, "") for k in fieldnames}
            writer.writerow(clean)
            new_count += 1

    return new_count


def main():
    parser = argparse.ArgumentParser(description="Google Maps Lead Gen (@pipelineabuser hexomatic)")
    parser.add_argument("--query", type=str, help="Business type (e.g., 'dentist', 'plumber')")
    parser.add_argument("--city", type=str, help="City and state (e.g., 'Austin TX')")
    parser.add_argument("--batch-cities", type=str, help="Comma-separated cities for batch search")
    parser.add_argument("--enrich", action="store_true", help="Visit websites to extract emails")
    parser.add_argument("--summary", action="store_true", help="Show lead summary")
    args = parser.parse_args()

    if args.summary:
        if OUTPUT_CSV.exists():
            with open(OUTPUT_CSV, "r") as f:
                reader = list(csv.DictReader(f))
                print(f"\n{'='*60}")
                print(f"LOCAL BIZ LEADS SUMMARY")
                print(f"{'='*60}")
                print(f"Total leads: {len(reader)}")
                cities = {}
                categories = {}
                with_email = 0
                with_phone = 0
                for row in reader:
                    cities[row.get("city", "?")] = cities.get(row.get("city", "?"), 0) + 1
                    categories[row.get("category", "?")] = categories.get(row.get("category", "?"), 0) + 1
                    if row.get("email"):
                        with_email += 1
                    if row.get("phone"):
                        with_phone += 1
                print(f"With email: {with_email}")
                print(f"With phone: {with_phone}")
                print(f"\nBy city:")
                for city, count in sorted(cities.items(), key=lambda x: -x[1])[:10]:
                    print(f"  {city}: {count}")
                print(f"\nBy category:")
                for cat, count in sorted(categories.items(), key=lambda x: -x[1])[:10]:
                    print(f"  {cat}: {count}")
        else:
            print("No leads yet.")
        return

    queries = [args.query] if args.query else BUSINESS_CATEGORIES[:5]
    cities = args.batch_cities.split(",") if args.batch_cities else ([args.city] if args.city else TOP_CITIES[:5])

    print(f"\n{'='*60}")
    print(f"LOCAL BUSINESS LEAD GEN SCRAPER")
    print(f"Source: @pipelineabuser - 'hexomatic.com / scrape google maps'")
    print(f"{'='*60}")
    print(f"Searching {len(queries)} categories x {len(cities)} cities...")
    print()

    all_leads = []
    for city in cities:
        for query in queries:
            log(f"Searching '{query}' in '{city}'...")
            ddg_leads = search_businesses_ddg(query, city)
            yelp_leads = search_businesses_yelp_fusion(query, city)
            batch_leads = ddg_leads + yelp_leads
            all_leads.extend(batch_leads)
            log(f"  Found {len(batch_leads)} leads")

    # Enrich with emails if requested
    if args.enrich:
        log("Enriching leads with website data...")
        for lead in all_leads:
            if lead.get("website") and not lead.get("email"):
                try:
                    emails, phones = extract_emails_from_website(lead["website"])
                    if emails:
                        lead["email"] = emails[0]
                    if phones and not lead.get("phone"):
                        lead["phone"] = phones[0]
                except Exception:
                    pass

    new_count = save_leads(all_leads)

    print(f"\n{'='*60}")
    print(f"RESULTS")
    print(f"{'='*60}")
    print(f"Total leads found: {len(all_leads)}")
    print(f"New leads saved: {new_count}")
    print(f"Output: {OUTPUT_CSV}")
    print(f"\nNext steps:")
    print(f"  1. Run with --enrich to extract emails from websites")
    print(f"  2. Use with local_biz_pipeline.py for website redesign offers")
    print(f"  3. Feed into cold email system")
    if not os.environ.get("YELP_API_KEY"):
        print(f"  4. Set YELP_API_KEY env var for better results (free: 500 calls/day)")


if __name__ == "__main__":
    main()
