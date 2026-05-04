#!/usr/bin/env python3
"""
USAspending.gov Contract Awards Scraper
========================================
Pulls recent government contract awards from the free public API.
Filters for small business sweet spot ($50K-$500K).
Outputs CSV for lead gen pipeline.

API Docs: https://api.usaspending.gov
No auth required. Rate limit: ~10 req/sec (be polite).

Usage:
    python3 usaspending_scraper.py
    python3 usaspending_scraper.py --category "IT services"
    python3 usaspending_scraper.py --min-amount 100000 --max-amount 300000
    python3 usaspending_scraper.py --naics 541512  # specific NAICS code
"""

import argparse
import csv
import json
import os
import sys
import time
from datetime import datetime, timedelta
from pathlib import Path

try:
    import requests
except ImportError:
    print("ERROR: requests library not found. Install with: pip3 install requests")
    sys.exit(1)

# --- Config ---
BASE_URL = "https://api.usaspending.gov/api/v2"
OUTPUT_DIR = Path(__file__).parent / "leads"
OUTPUT_FILE = OUTPUT_DIR / "usaspending_awards.csv"
RATE_LIMIT_DELAY = 0.5  # seconds between requests

# NAICS codes for high-value service categories
# These are the categories where cold outreach to losing bidders works best
NAICS_CATEGORIES = {
    "IT_SERVICES": {
        "codes": ["541512", "541511", "541513", "541519", "518210"],
        "label": "IT Services & Computer Systems Design",
        "description": "Custom software, IT consulting, systems integration, cloud hosting"
    },
    "CONSULTING": {
        "codes": ["541611", "541612", "541613", "541614", "541618", "541690"],
        "label": "Management & Technical Consulting",
        "description": "Strategic consulting, HR consulting, marketing consulting"
    },
    "JANITORIAL": {
        "codes": ["561720", "561710", "561210"],
        "label": "Janitorial & Facility Services",
        "description": "Building cleaning, landscaping, facility support"
    },
    "STAFFING": {
        "codes": ["561320", "561311", "561312"],
        "label": "Staffing & Temporary Help",
        "description": "Temporary staffing, employment placement, executive search"
    },
    "ENGINEERING": {
        "codes": ["541330", "541310", "541320", "541340"],
        "label": "Engineering Services",
        "description": "Engineering design, surveying, drafting, testing"
    },
    "TRAINING": {
        "codes": ["611430", "611420", "611410", "611710"],
        "label": "Training & Professional Development",
        "description": "Professional training, computer training, educational support"
    },
    "MARKETING": {
        "codes": ["541810", "541820", "541830", "541840", "541850", "541860", "541890"],
        "label": "Advertising & Marketing Services",
        "description": "Ad agencies, PR, media buying, direct mail, display advertising"
    },
    "SECURITY": {
        "codes": ["561612", "561613", "561621"],
        "label": "Security Guard & Patrol Services",
        "description": "Guard services, security systems, locksmiths"
    },
}

# PSC (Product Service Codes) for services - broader search
SERVICE_PSC_PREFIXES = ["D", "R", "S", "J", "K", "L", "B", "C", "F", "G", "H"]


def search_awards_by_keyword(keyword, min_amount=50000, max_amount=500000,
                              start_date=None, end_date=None, page=1, limit=50):
    """
    Search contract awards using the spending_by_award endpoint.
    Uses keyword search across award descriptions.
    """
    if not end_date:
        end_date = datetime.now().strftime("%Y-%m-%d")
    if not start_date:
        start_date = (datetime.now() - timedelta(days=365)).strftime("%Y-%m-%d")

    url = f"{BASE_URL}/search/spending_by_award/"

    payload = {
        "filters": {
            "keywords": [keyword],
            "award_type_codes": ["A", "B", "C", "D"],  # Contracts only (not grants)
            "time_period": [
                {
                    "start_date": start_date,
                    "end_date": end_date
                }
            ],
            "award_amounts": [
                {
                    "lower_bound": min_amount,
                    "upper_bound": max_amount
                }
            ]
        },
        "fields": [
            "Award ID",
            "Recipient Name",
            "Start Date",
            "End Date",
            "Award Amount",
            "Total Outlays",
            "Description",
            "def_codes",
            "COVID-19 Obligations",
            "COVID-19 Outlays",
            "Infrastructure Obligations",
            "Infrastructure Outlays",
            "Awarding Agency",
            "Awarding Sub Agency",
            "Contract Award Type",
            "recipient_id",
            "prime_award_recipient_id",
            "NAICS Code",
            "generated_internal_id"
        ],
        "page": page,
        "limit": limit,
        "sort": "Award Amount",
        "order": "desc",
        "subawards": False
    }

    try:
        resp = requests.post(url, json=payload, timeout=30)
        resp.raise_for_status()
        return resp.json()
    except requests.exceptions.RequestException as e:
        print(f"  ERROR requesting {url}: {e}")
        return None


def search_awards_by_naics(naics_codes, min_amount=50000, max_amount=500000,
                            start_date=None, end_date=None, page=1, limit=50):
    """
    Search contract awards by NAICS code for more precise targeting.
    """
    if not end_date:
        end_date = datetime.now().strftime("%Y-%m-%d")
    if not start_date:
        start_date = (datetime.now() - timedelta(days=365)).strftime("%Y-%m-%d")

    url = f"{BASE_URL}/search/spending_by_award/"

    payload = {
        "filters": {
            "naics_codes": {"require": naics_codes},
            "award_type_codes": ["A", "B", "C", "D"],
            "time_period": [
                {
                    "start_date": start_date,
                    "end_date": end_date
                }
            ],
            "award_amounts": [
                {
                    "lower_bound": min_amount,
                    "upper_bound": max_amount
                }
            ]
        },
        "fields": [
            "Award ID",
            "Recipient Name",
            "Start Date",
            "End Date",
            "Award Amount",
            "Total Outlays",
            "Description",
            "Awarding Agency",
            "Awarding Sub Agency",
            "Contract Award Type",
            "recipient_id",
            "prime_award_recipient_id",
            "NAICS Code",
            "generated_internal_id"
        ],
        "page": page,
        "limit": limit,
        "sort": "Award Amount",
        "order": "desc",
        "subawards": False
    }

    try:
        resp = requests.post(url, json=payload, timeout=30)
        resp.raise_for_status()
        return resp.json()
    except requests.exceptions.RequestException as e:
        print(f"  ERROR requesting {url}: {e}")
        return None


def get_award_details(generated_internal_id):
    """
    Get detailed info on a specific award (includes more fields).
    """
    url = f"{BASE_URL}/awards/{generated_internal_id}/"
    try:
        resp = requests.get(url, timeout=30)
        resp.raise_for_status()
        return resp.json()
    except requests.exceptions.RequestException as e:
        print(f"  ERROR getting award details: {e}")
        return None


def get_recipient_profile(recipient_id):
    """
    Get recipient (vendor) profile info including DUNS, address, etc.
    """
    if not recipient_id:
        return None
    url = f"{BASE_URL}/recipient/{recipient_id}/"
    try:
        resp = requests.get(url, timeout=30)
        resp.raise_for_status()
        return resp.json()
    except requests.exceptions.RequestException as e:
        print(f"  ERROR getting recipient profile: {e}")
        return None


def search_all_categories(min_amount=50000, max_amount=500000,
                          categories=None, max_per_category=100):
    """
    Search across all NAICS categories and aggregate results.
    Returns deduplicated list of awards.
    """
    all_awards = []
    seen_ids = set()

    if categories is None:
        categories = list(NAICS_CATEGORIES.keys())

    for cat_key in categories:
        cat = NAICS_CATEGORIES.get(cat_key)
        if not cat:
            print(f"  WARNING: Unknown category '{cat_key}', skipping")
            continue

        print(f"\n--- Searching: {cat['label']} ---")
        print(f"    NAICS codes: {', '.join(cat['codes'])}")

        page = 1
        category_count = 0

        while category_count < max_per_category:
            remaining = max_per_category - category_count
            batch_size = min(50, remaining)

            data = search_awards_by_naics(
                cat["codes"],
                min_amount=min_amount,
                max_amount=max_amount,
                page=page,
                limit=batch_size
            )

            if not data or not data.get("results"):
                print(f"    No more results (page {page})")
                break

            results = data["results"]
            total_available = data.get("page_metadata", {}).get("total", 0)
            print(f"    Page {page}: {len(results)} results (total available: {total_available})")

            for award in results:
                award_id = award.get("generated_internal_id") or award.get("Award ID", "")
                if award_id in seen_ids:
                    continue
                seen_ids.add(award_id)

                award["_category"] = cat_key
                award["_category_label"] = cat["label"]
                all_awards.append(award)
                category_count += 1

            if len(results) < batch_size:
                break

            page += 1
            time.sleep(RATE_LIMIT_DELAY)

        print(f"    Collected {category_count} awards for {cat['label']}")
        time.sleep(RATE_LIMIT_DELAY)

    return all_awards


def enrich_top_awards(awards, top_n=25):
    """
    Get detailed info for top N awards (by amount).
    Adds recipient location, contract period, etc.
    """
    sorted_awards = sorted(awards, key=lambda x: float(x.get("Award Amount", 0) or 0), reverse=True)
    top = sorted_awards[:top_n]

    enriched = []
    for i, award in enumerate(top):
        internal_id = award.get("generated_internal_id", "")
        print(f"  Enriching {i+1}/{len(top)}: {award.get('Recipient Name', 'Unknown')} - ${award.get('Award Amount', 0):,.0f}")

        details = None
        if internal_id:
            details = get_award_details(internal_id)
            time.sleep(RATE_LIMIT_DELAY)

        enriched_award = dict(award)

        if details:
            # Extract additional useful fields
            enriched_award["_place_of_performance_city"] = (
                details.get("place_of_performance", {}).get("city_name", "") if details.get("place_of_performance") else ""
            )
            enriched_award["_place_of_performance_state"] = (
                details.get("place_of_performance", {}).get("state_code", "") if details.get("place_of_performance") else ""
            )
            enriched_award["_recipient_city"] = ""
            enriched_award["_recipient_state"] = ""
            enriched_award["_recipient_zip"] = ""
            enriched_award["_recipient_country"] = ""

            recipient = details.get("recipient", {})
            if recipient:
                location = recipient.get("location", {})
                if location:
                    enriched_award["_recipient_city"] = location.get("city_name", "")
                    enriched_award["_recipient_state"] = location.get("state_code", "")
                    enriched_award["_recipient_zip"] = location.get("zip5", "")
                    enriched_award["_recipient_country"] = location.get("country_name", "")
                enriched_award["_recipient_uei"] = recipient.get("uei", "")
                enriched_award["_recipient_parent_name"] = recipient.get("parent_recipient_name", "")

            enriched_award["_period_of_performance_start"] = details.get("period_of_performance", {}).get("start_date", "") if details.get("period_of_performance") else ""
            enriched_award["_period_of_performance_end"] = details.get("period_of_performance", {}).get("end_date", "") if details.get("period_of_performance") else ""
            enriched_award["_potential_end_date"] = details.get("period_of_performance", {}).get("potential_end_date", "") if details.get("period_of_performance") else ""
            enriched_award["_contract_type"] = details.get("type_description", "")
            enriched_award["_naics_description"] = details.get("naics_hierarchy", {}).get("toptier_code", {}).get("description", "") if details.get("naics_hierarchy") else ""
            enriched_award["_psc_description"] = details.get("psc_hierarchy", {}).get("toptier_code", {}).get("description", "") if details.get("psc_hierarchy") else ""
            enriched_award["_usaspending_url"] = f"https://www.usaspending.gov/award/{internal_id}" if internal_id else ""

            # Executive compensation (if available)
            exec_comp = details.get("executive_details", {})
            if exec_comp:
                officers = exec_comp.get("officers", [])
                if officers:
                    enriched_award["_top_executive"] = officers[0].get("name", "") if officers else ""

        enriched.append(enriched_award)

    return enriched


def write_csv(awards, output_path):
    """Write awards to CSV file."""
    if not awards:
        print("No awards to write.")
        return

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Define column order
    columns = [
        "Award ID",
        "Recipient Name",
        "Award Amount",
        "Awarding Agency",
        "Awarding Sub Agency",
        "Description",
        "NAICS Code",
        "Start Date",
        "End Date",
        "Contract Award Type",
        "_category",
        "_category_label",
        "_recipient_city",
        "_recipient_state",
        "_recipient_zip",
        "_recipient_country",
        "_recipient_uei",
        "_recipient_parent_name",
        "_place_of_performance_city",
        "_place_of_performance_state",
        "_period_of_performance_start",
        "_period_of_performance_end",
        "_potential_end_date",
        "_contract_type",
        "_naics_description",
        "_psc_description",
        "_top_executive",
        "_usaspending_url",
        "generated_internal_id",
    ]

    # Only include columns that exist in data
    all_keys = set()
    for a in awards:
        all_keys.update(a.keys())
    columns = [c for c in columns if c in all_keys]
    # Add any remaining keys not in our ordered list
    for k in sorted(all_keys):
        if k not in columns:
            columns.append(k)

    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=columns, extrasaction="ignore")
        writer.writeheader()
        for award in awards:
            # Clean up values
            row = {}
            for k, v in award.items():
                if v is None:
                    row[k] = ""
                elif isinstance(v, (dict, list)):
                    row[k] = json.dumps(v)
                else:
                    row[k] = v
            writer.writerow(row)

    print(f"\nWrote {len(awards)} awards to {output_path}")


def print_summary(awards):
    """Print summary statistics."""
    if not awards:
        print("No awards to summarize.")
        return

    amounts = [float(a.get("Award Amount", 0) or 0) for a in awards]

    print("\n" + "=" * 70)
    print("USASPENDING.GOV SCRAPE SUMMARY")
    print("=" * 70)
    print(f"Total awards collected: {len(awards)}")
    print(f"Total value: ${sum(amounts):,.0f}")
    print(f"Average award: ${sum(amounts)/len(amounts):,.0f}")
    print(f"Largest: ${max(amounts):,.0f}")
    print(f"Smallest: ${min(amounts):,.0f}")

    # By category
    cats = {}
    for a in awards:
        cat = a.get("_category_label", "Unknown")
        if cat not in cats:
            cats[cat] = {"count": 0, "total": 0}
        cats[cat]["count"] += 1
        cats[cat]["total"] += float(a.get("Award Amount", 0) or 0)

    print(f"\nBy category:")
    for cat, stats in sorted(cats.items(), key=lambda x: x[1]["total"], reverse=True):
        print(f"  {cat}: {stats['count']} awards, ${stats['total']:,.0f} total")

    # By agency
    agencies = {}
    for a in awards:
        agency = a.get("Awarding Agency", "Unknown")
        if agency not in agencies:
            agencies[agency] = 0
        agencies[agency] += 1

    print(f"\nTop agencies:")
    for agency, count in sorted(agencies.items(), key=lambda x: x[1], reverse=True)[:10]:
        print(f"  {agency}: {count} awards")

    # Top 10 awards
    print(f"\nTop 10 awards by amount:")
    sorted_awards = sorted(awards, key=lambda x: float(x.get("Award Amount", 0) or 0), reverse=True)
    for i, a in enumerate(sorted_awards[:10]):
        print(f"  {i+1}. {a.get('Recipient Name', 'Unknown')[:40]:40s} ${float(a.get('Award Amount', 0) or 0):>12,.0f}  {a.get('Awarding Agency', '')[:30]}")

    print("=" * 70)


def main():
    parser = argparse.ArgumentParser(description="USAspending.gov Contract Awards Scraper")
    parser.add_argument("--min-amount", type=int, default=50000, help="Minimum award amount (default: 50000)")
    parser.add_argument("--max-amount", type=int, default=500000, help="Maximum award amount (default: 500000)")
    parser.add_argument("--categories", nargs="+", choices=list(NAICS_CATEGORIES.keys()),
                        help="Categories to search (default: all)")
    parser.add_argument("--max-per-category", type=int, default=100,
                        help="Max awards per category (default: 100)")
    parser.add_argument("--enrich-top", type=int, default=25,
                        help="Number of top awards to enrich with details (default: 25)")
    parser.add_argument("--output", type=str, default=str(OUTPUT_FILE),
                        help=f"Output CSV path (default: {OUTPUT_FILE})")
    parser.add_argument("--naics", type=str, help="Search specific NAICS code(s), comma-separated")
    parser.add_argument("--keyword", type=str, help="Search by keyword instead of NAICS")
    parser.add_argument("--list-categories", action="store_true", help="List available categories and exit")

    args = parser.parse_args()

    if args.list_categories:
        print("Available categories:")
        for key, cat in NAICS_CATEGORIES.items():
            print(f"  {key:15s} - {cat['label']}")
            print(f"                   NAICS: {', '.join(cat['codes'])}")
            print(f"                   {cat['description']}")
        return

    print("=" * 70)
    print("USASPENDING.GOV CONTRACT AWARDS SCRAPER")
    print("=" * 70)
    print(f"Amount range: ${args.min_amount:,} - ${args.max_amount:,}")
    print(f"Date range: Last 12 months")
    print(f"Output: {args.output}")
    print()

    all_awards = []

    if args.keyword:
        print(f"Searching by keyword: '{args.keyword}'")
        page = 1
        while len(all_awards) < args.max_per_category:
            data = search_awards_by_keyword(
                args.keyword,
                min_amount=args.min_amount,
                max_amount=args.max_amount,
                page=page,
                limit=50
            )
            if not data or not data.get("results"):
                break
            results = data["results"]
            for r in results:
                r["_category"] = "KEYWORD"
                r["_category_label"] = f"Keyword: {args.keyword}"
            all_awards.extend(results)
            print(f"  Page {page}: {len(results)} results")
            if len(results) < 50:
                break
            page += 1
            time.sleep(RATE_LIMIT_DELAY)

    elif args.naics:
        codes = [c.strip() for c in args.naics.split(",")]
        print(f"Searching NAICS codes: {codes}")
        page = 1
        while len(all_awards) < args.max_per_category:
            data = search_awards_by_naics(
                codes,
                min_amount=args.min_amount,
                max_amount=args.max_amount,
                page=page,
                limit=50
            )
            if not data or not data.get("results"):
                break
            results = data["results"]
            for r in results:
                r["_category"] = "NAICS"
                r["_category_label"] = f"NAICS: {args.naics}"
            all_awards.extend(results)
            print(f"  Page {page}: {len(results)} results")
            if len(results) < 50:
                break
            page += 1
            time.sleep(RATE_LIMIT_DELAY)

    else:
        categories = args.categories or list(NAICS_CATEGORIES.keys())
        all_awards = search_all_categories(
            min_amount=args.min_amount,
            max_amount=args.max_amount,
            categories=categories,
            max_per_category=args.max_per_category
        )

    if not all_awards:
        print("\nNo awards found. Try adjusting filters.")
        return

    print_summary(all_awards)

    # Enrich top awards with detailed info
    if args.enrich_top > 0:
        print(f"\nEnriching top {args.enrich_top} awards with detailed info...")
        enriched = enrich_top_awards(all_awards, top_n=args.enrich_top)

        # Replace enriched awards in the list
        enriched_ids = {a.get("generated_internal_id") for a in enriched}
        remaining = [a for a in all_awards if a.get("generated_internal_id") not in enriched_ids]
        all_awards = enriched + remaining

    # Write output
    write_csv(all_awards, args.output)

    print(f"\nDone. {len(all_awards)} awards saved to {args.output}")
    print(f"Next steps:")
    print(f"  1. Review CSV for high-value targets")
    print(f"  2. File FOIA requests for contract details on top targets")
    print(f"  3. Build intel reports from FOIA responses")
    print(f"  4. Cold email losing bidders with undercut offers")


if __name__ == "__main__":
    main()
