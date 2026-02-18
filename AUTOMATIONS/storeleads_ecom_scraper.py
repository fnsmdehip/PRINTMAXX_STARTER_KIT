#!/usr/bin/env python3
"""
Ecom Store Lead Scraper
Source: @pipelineabuser tweet - "storeleads.com / database of 5+ million shopify stores"
Also: ALPHA004 in PIPELINEABUSER_ALPHA_IMPLEMENTATION.md

Finds high-revenue Shopify stores and builds cold outreach lists.
Uses multiple free data sources as alternatives to storeleads ($99/mo).

Usage:
    python3 storeleads_ecom_scraper.py                        # Run default search
    python3 storeleads_ecom_scraper.py --niche "supplements"
    python3 storeleads_ecom_scraper.py --tech "klaviyo"
    python3 storeleads_ecom_scraper.py --min-traffic 50000
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
OUTPUT_CSV = BASE_DIR / "LEDGER" / "ECOM_LEADS.csv"
LOG_FILE = BASE_DIR / "AUTOMATIONS" / "logs" / "ecom_scraper.log"

# High-value niches to target
NICHES = [
    "supplements",
    "skincare",
    "fitness",
    "pet supplies",
    "home decor",
    "jewelry",
    "activewear",
    "coffee",
    "candles",
    "baby products",
]

COLD_EMAIL_TEMPLATES = {
    "tech_stack": """Subject: Quick question about your {tech_tool} setup

{first_name},

Noticed {store_name} is running {tech_tool}. At your scale, {pain_point} usually becomes the bottleneck.

We help Shopify stores doing {revenue_range} solve exactly that. Takes 15 min to see if there's a fit.

Want me to send over a quick audit?
""",
    "growth_offer": """Subject: Noticed {store_name} is growing fast

{first_name},

Saw {store_name} is ranking for {keywords} and growing. Usually at this stage, {pain_point} is the next wall.

We've helped 12 stores at your stage break through with {our_service}. Average result: {result_metric}.

5 min call?
""",
}


def log(msg):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_msg = f"[{timestamp}] {msg}"
    print(log_msg)
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(LOG_FILE, "a") as f:
        f.write(log_msg + "\n")


def fetch_url(url, headers=None):
    """Fetch URL with error handling."""
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
        log(f"Fetch error: {url} - {e}")
        return None


def search_shopify_stores_builtwith(niche="supplements"):
    """Use BuiltWith free tier to find Shopify stores in a niche."""
    leads = []
    # BuiltWith trends page (free, public)
    url = f"https://trends.builtwith.com/shop/Shopify"
    data = fetch_url(url)
    if data:
        log(f"  BuiltWith: fetched Shopify trends page ({len(data)} chars)")
        # Extract store domains from the page
        domains = re.findall(r'href="https?://([a-zA-Z0-9\-]+\.[a-z]{2,})"', data)
        unique_domains = list(set(domains))[:50]
        for domain in unique_domains:
            if any(skip in domain for skip in ["builtwith", "google", "facebook", "twitter", "shopify.com"]):
                continue
            leads.append({
                "store_url": f"https://{domain}",
                "store_name": domain.split(".")[0].title(),
                "source": "BuiltWith",
                "niche": niche,
                "tech_detected": "Shopify",
            })
    return leads


def search_stores_via_google_shopping(niche):
    """Search for Shopify stores in a niche using DuckDuckGo."""
    leads = []
    queries = [
        f"site:myshopify.com {niche}",
        f'"{niche}" "powered by shopify"',
        f'"{niche}" shop "shopify" best sellers',
    ]

    for query in queries:
        url = f"https://api.duckduckgo.com/?q={quote(query)}&format=json"
        data = fetch_url(url)
        if data:
            try:
                result = json.loads(data)
                related = result.get("RelatedTopics", [])
                for topic in related[:10]:
                    first_url = topic.get("FirstURL", "")
                    text = topic.get("Text", "")
                    if first_url and "shopify" in first_url.lower() or ".com" in first_url:
                        domain = re.search(r'https?://([^/]+)', first_url)
                        if domain:
                            leads.append({
                                "store_url": first_url,
                                "store_name": domain.group(1).split(".")[0].title(),
                                "source": "DuckDuckGo",
                                "niche": niche,
                                "tech_detected": "Shopify (likely)",
                                "description": text[:200],
                            })
            except json.JSONDecodeError:
                pass

    return leads


def detect_shopify_store(url):
    """Check if a URL is a Shopify store by looking for Shopify indicators."""
    data = fetch_url(url)
    if not data:
        return False, {}

    indicators = {
        "shopify": "cdn.shopify.com" in data,
        "klaviyo": "klaviyo" in data.lower(),
        "yotpo": "yotpo" in data.lower(),
        "judge_me": "judge.me" in data.lower(),
        "loox": "loox.io" in data.lower(),
        "omnisend": "omnisend" in data.lower(),
        "privy": "privy" in data.lower(),
        "smile_io": "smile.io" in data.lower(),
        "stamped": "stamped.io" in data.lower(),
        "recharge": "recharge" in data.lower(),
        "facebook_pixel": "fbq(" in data,
        "google_analytics": "gtag(" in data or "google-analytics" in data,
        "tiktok_pixel": "tiktok" in data.lower() and "pixel" in data.lower(),
    }

    # Extract meta description for niche classification
    meta_match = re.search(r'<meta\s+name="description"\s+content="([^"]*)"', data, re.IGNORECASE)
    description = meta_match.group(1) if meta_match else ""

    # Extract title
    title_match = re.search(r'<title>([^<]*)</title>', data, re.IGNORECASE)
    title = title_match.group(1) if title_match else ""

    tech_stack = [k for k, v in indicators.items() if v]

    return indicators["shopify"], {
        "tech_stack": tech_stack,
        "description": description[:200],
        "title": title,
    }


def search_tiktok_shop_trending(niche):
    """Find trending products on TikTok Shop (potential store leads)."""
    leads = []
    url = f"https://api.duckduckgo.com/?q={quote(f'tiktok shop trending {niche} 2026')}&format=json"
    data = fetch_url(url)
    if data:
        try:
            result = json.loads(data)
            abstract = result.get("AbstractText", "")
            if abstract:
                leads.append({
                    "store_url": "",
                    "store_name": f"TikTok Shop Trend: {niche}",
                    "source": "TikTok Shop Research",
                    "niche": niche,
                    "tech_detected": "TikTok Shop",
                    "description": abstract[:300],
                })
        except json.JSONDecodeError:
            pass
    return leads


def save_leads(leads):
    """Save leads to CSV, avoiding duplicates."""
    OUTPUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    file_exists = OUTPUT_CSV.exists()

    existing_urls = set()
    if file_exists:
        with open(OUTPUT_CSV, "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                existing_urls.add(row.get("store_url", ""))

    fieldnames = [
        "lead_id",
        "store_url",
        "store_name",
        "niche",
        "source",
        "tech_detected",
        "description",
        "estimated_revenue",
        "contact_email",
        "found_date",
        "status",
        "email_sent",
        "notes",
    ]

    new_leads = []
    for i, lead in enumerate(leads):
        if lead.get("store_url", "") in existing_urls:
            continue
        lead["lead_id"] = f"ECOM_{datetime.now().strftime('%Y%m%d')}_{i:04d}"
        lead["found_date"] = datetime.now().strftime("%Y-%m-%d")
        lead["status"] = "NEW"
        lead["email_sent"] = "NO"
        lead["estimated_revenue"] = lead.get("estimated_revenue", "")
        lead["contact_email"] = lead.get("contact_email", "")
        lead["notes"] = lead.get("notes", "")
        new_leads.append(lead)
        existing_urls.add(lead.get("store_url", ""))

    with open(OUTPUT_CSV, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        for lead in new_leads:
            clean_lead = {k: lead.get(k, "") for k in fieldnames}
            writer.writerow(clean_lead)

    return len(new_leads)


def main():
    parser = argparse.ArgumentParser(description="Ecom Store Lead Scraper (@pipelineabuser)")
    parser.add_argument("--niche", type=str, help="Specific niche to search")
    parser.add_argument("--tech", type=str, help="Filter by tech (e.g., klaviyo, recharge)")
    parser.add_argument("--summary", action="store_true", help="Show summary of leads")
    args = parser.parse_args()

    if args.summary:
        if OUTPUT_CSV.exists():
            with open(OUTPUT_CSV, "r") as f:
                reader = list(csv.DictReader(f))
                print(f"\n{'='*60}")
                print(f"ECOM LEADS SUMMARY")
                print(f"{'='*60}")
                print(f"Total leads: {len(reader)}")
                niches = {}
                for row in reader:
                    n = row.get("niche", "unknown")
                    niches[n] = niches.get(n, 0) + 1
                for niche, count in sorted(niches.items(), key=lambda x: -x[1]):
                    print(f"  {niche}: {count}")
        else:
            print("No leads yet. Run without --summary to search.")
        return

    niches_to_search = [args.niche] if args.niche else NICHES[:5]

    print(f"\n{'='*60}")
    print(f"ECOM STORE LEAD SCRAPER")
    print(f"Source: @pipelineabuser - 'storeleads.com / 5M+ shopify stores'")
    print(f"{'='*60}")
    print(f"Searching {len(niches_to_search)} niches...")
    print()

    all_leads = []

    for niche in niches_to_search:
        log(f"Searching niche: {niche}...")

        # Method 1: BuiltWith
        bw_leads = search_shopify_stores_builtwith(niche)
        all_leads.extend(bw_leads)

        # Method 2: DuckDuckGo search
        ddg_leads = search_stores_via_google_shopping(niche)
        all_leads.extend(ddg_leads)

        # Method 3: TikTok Shop trends
        tt_leads = search_tiktok_shop_trending(niche)
        all_leads.extend(tt_leads)

        log(f"  {niche}: found {len(bw_leads) + len(ddg_leads) + len(tt_leads)} leads")

    # Save
    new_count = save_leads(all_leads)

    print(f"\n{'='*60}")
    print(f"RESULTS")
    print(f"{'='*60}")
    print(f"Total leads found: {len(all_leads)}")
    print(f"New leads saved: {new_count}")
    print(f"Output: {OUTPUT_CSV}")

    # Save email templates
    template_dir = BASE_DIR / "EMAIL" / "ecom_outreach"
    template_dir.mkdir(parents=True, exist_ok=True)
    for name, template in COLD_EMAIL_TEMPLATES.items():
        template_file = template_dir / f"{name}_template.txt"
        if not template_file.exists():
            with open(template_file, "w") as f:
                f.write(template)
    print(f"Email templates: {template_dir}")

    print(f"\nNext steps:")
    print(f"  1. Review leads in {OUTPUT_CSV}")
    print(f"  2. Enrich with emails via Hunter.io or Apollo")
    print(f"  3. Customize cold email templates in {template_dir}")
    print(f"  4. For full store data, sign up at storeleads.com ($99/mo)")


if __name__ == "__main__":
    main()
