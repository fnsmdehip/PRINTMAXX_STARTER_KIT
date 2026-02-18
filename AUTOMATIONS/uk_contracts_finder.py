#!/usr/bin/env python3
"""
UK Contracts Finder Scraper
============================
https://www.contractsfinder.service.gov.uk/ has a free public API.
Same play as USAspending but for the UK market.

Pulls active tenders and recently awarded contracts.
Companies that win or lose these tenders are high-intent B2B leads.

API docs: https://www.contractsfinder.service.gov.uk/apidocumentation/home

Usage:
    python3 uk_contracts_finder.py
    python3 uk_contracts_finder.py --keyword "cybersecurity"
    python3 uk_contracts_finder.py --keyword "cloud" --min-value 50000
    python3 uk_contracts_finder.py --categories "IT" "consulting" "marketing"
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
from urllib.parse import quote_plus

try:
    import requests
except ImportError:
    print("ERROR: requests library not found. Install with: pip3 install requests")
    sys.exit(1)

# --- Config ---
OUTPUT_DIR = Path(__file__).parent / "leads"
OUTPUT_FILE = OUTPUT_DIR / "uk_contracts_finder_leads.csv"
RATE_LIMIT_DELAY = 1.0  # public API, be polite

BASE_URL = "https://www.contractsfinder.service.gov.uk"
SEARCH_API = f"{BASE_URL}/Published/Notices/OCDS/Search"

# Search categories
DEFAULT_KEYWORDS = [
    "cybersecurity",
    "artificial intelligence",
    "cloud computing",
    "data analytics",
    "digital transformation",
    "software development",
    "IT services",
    "web development",
    "consultancy",
    "marketing services",
    "training",
    "managed services",
    "data management",
    "automation",
]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
    "Accept": "application/json",
}


def search_contracts(keyword=None, stages=None, published_from=None,
                     published_to=None, min_value=None, max_value=None,
                     page=1, size=100):
    """
    Search UK Contracts Finder API.

    stages: "tender" (open opportunities), "award" (awarded contracts)
    """
    if stages is None:
        stages = "tender"

    if published_from is None:
        published_from = (datetime.now() - timedelta(days=90)).strftime("%Y-%m-%d")

    if published_to is None:
        published_to = datetime.now().strftime("%Y-%m-%d")

    params = {
        "stages": stages,
        "publishedFrom": published_from,
        "publishedTo": published_to,
        "size": size,
        "page": page,
    }

    if keyword:
        params["keyword"] = keyword

    if min_value:
        params["valueFrom"] = min_value

    if max_value:
        params["valueTo"] = max_value

    try:
        resp = requests.get(SEARCH_API, params=params, headers=HEADERS, timeout=60)
        resp.raise_for_status()
        return resp.json()
    except requests.exceptions.RequestException as e:
        print(f"  ERROR: {e}")
        return None


def search_notices_html(keyword=None, published_from=None):
    """
    Fallback: Scrape the HTML search page if API fails.
    """
    from bs4 import BeautifulSoup

    url = f"{BASE_URL}/Search/Results"
    params = {
        "searchTerm": keyword or "",
        "publishedFromDate": published_from or (datetime.now() - timedelta(days=30)).strftime("%d/%m/%Y"),
        "publishedToDate": datetime.now().strftime("%d/%m/%Y"),
    }

    notices = []

    try:
        resp = requests.get(url, params=params, headers={
            "User-Agent": HEADERS["User-Agent"],
            "Accept": "text/html",
        }, timeout=15)

        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")

        for item in soup.select(".search-result, .standard-col"):
            notice = {}

            title_el = item.select_one("h2 a, .search-result-header a")
            if title_el:
                notice["title"] = title_el.get_text(strip=True)
                href = title_el.get("href", "")
                if href.startswith("/"):
                    href = f"{BASE_URL}{href}"
                notice["url"] = href

            # Extract details from description
            desc_el = item.select_one(".search-result-sub-header, p")
            if desc_el:
                notice["description"] = desc_el.get_text(strip=True)[:500]

            # Try to find buyer
            buyer_el = item.select_one('[class*="buyer"], [class*="organisation"]')
            if buyer_el:
                notice["buyer"] = buyer_el.get_text(strip=True)

            # Try to find value
            value_el = item.select_one('[class*="value"], [class*="amount"]')
            if value_el:
                text = value_el.get_text(strip=True)
                value_match = re.search(r'[\d,]+(?:\.\d+)?', text.replace('£', '').replace(',', ''))
                if value_match:
                    notice["value_gbp"] = float(value_match.group())

            if notice.get("title"):
                notices.append(notice)

    except Exception as e:
        print(f"  HTML scrape error: {e}")

    return notices


def parse_ocds_results(data):
    """
    Parse OCDS (Open Contracting Data Standard) format results.
    """
    contracts = []

    if not data:
        return contracts

    # The API returns releases in OCDS format
    releases = data.get("releases", [])

    if not releases:
        # Try alternative structure
        results = data.get("results", [])
        if results:
            releases = results

    for release in releases:
        contract = {}

        # Basic info
        contract["notice_id"] = release.get("id", "")
        contract["ocid"] = release.get("ocid", "")

        # Tender info
        tender = release.get("tender", {})
        if tender:
            contract["title"] = tender.get("title", "")
            contract["description"] = (tender.get("description", "") or "")[:500]
            contract["status"] = tender.get("status", "")
            contract["procurement_method"] = tender.get("procurementMethod", "")

            # Value
            value = tender.get("value", {})
            if value:
                contract["value_amount"] = value.get("amount", "")
                contract["value_currency"] = value.get("currency", "GBP")

            # Min/max value
            min_val = tender.get("minValue", {})
            max_val = tender.get("maxValue", {})
            if min_val:
                contract["min_value"] = min_val.get("amount", "")
            if max_val:
                contract["max_value"] = max_val.get("amount", "")

            # Dates
            tender_period = tender.get("tenderPeriod", {})
            if tender_period:
                contract["tender_start"] = tender_period.get("startDate", "")
                contract["tender_end"] = tender_period.get("endDate", "")

            contract_period = tender.get("contractPeriod", {})
            if contract_period:
                contract["contract_start"] = contract_period.get("startDate", "")
                contract["contract_end"] = contract_period.get("endDate", "")

            # Items/categories
            items = tender.get("items", [])
            if items:
                categories = []
                for item in items[:5]:
                    classification = item.get("classification", {})
                    if classification:
                        desc = classification.get("description", "")
                        if desc:
                            categories.append(desc)
                contract["categories"] = "; ".join(categories)

        # Buyer info
        buyer = release.get("buyer", {})
        if buyer:
            contract["buyer_name"] = buyer.get("name", "")
            contract["buyer_id"] = buyer.get("id", "")

            address = buyer.get("address", {})
            if address:
                contract["buyer_region"] = address.get("region", "")
                contract["buyer_locality"] = address.get("locality", "")
                contract["buyer_country"] = address.get("countryName", "")

            contact = buyer.get("contactPoint", {})
            if contact:
                contract["contact_name"] = contact.get("name", "")
                contract["contact_email"] = contact.get("email", "")
                contract["contact_phone"] = contact.get("telephone", "")

        # Awards (if awarded)
        awards = release.get("awards", [])
        if awards:
            for award in awards[:3]:
                suppliers = award.get("suppliers", [])
                if suppliers:
                    contract["awarded_to"] = ", ".join(s.get("name", "") for s in suppliers)
                contract["award_date"] = award.get("date", "")
                award_val = award.get("value", {})
                if award_val:
                    contract["award_value"] = award_val.get("amount", "")

        # Tags/tag
        tag = release.get("tag", [])
        if tag:
            contract["notice_type"] = ", ".join(tag) if isinstance(tag, list) else str(tag)

        # Published date
        contract["published_date"] = release.get("date", "")

        # Contract finder URL
        if contract.get("ocid"):
            contract["cf_url"] = f"{BASE_URL}/Notice/{contract['ocid'].split('/')[-1] if '/' in contract['ocid'] else contract['ocid']}"

        if contract.get("title"):
            contracts.append(contract)

    return contracts


def classify_contract_lead(contract):
    """Classify contract as a lead."""
    signals = []
    lead_quality = "MEDIUM"

    title_lower = (contract.get("title", "") + " " + contract.get("description", "")).lower()

    # High value contracts
    value = contract.get("value_amount") or contract.get("max_value") or 0
    try:
        value = float(value)
    except (ValueError, TypeError):
        value = 0

    if value > 500000:
        signals.append("HIGH_VALUE")
        lead_quality = "HIGH"
    elif value > 100000:
        signals.append("MEDIUM_VALUE")
    elif value > 0 and value < 50000:
        signals.append("SMALL_CONTRACT")

    # Tech-related
    tech_terms = ["software", "digital", "cloud", "cyber", "data", "ai ", "artificial intelligence",
                  "machine learning", "analytics", "automation", "api", "saas", "platform"]
    if any(t in title_lower for t in tech_terms):
        signals.append("TECH_CONTRACT")
        lead_quality = "HIGH"

    # Active tenders (can still bid)
    if contract.get("status") == "active" or "tender" in contract.get("notice_type", "").lower():
        signals.append("ACTIVE_TENDER")
        lead_quality = "HIGHEST"

    # Has contact info
    if contract.get("contact_email"):
        signals.append("HAS_CONTACT_EMAIL")
        lead_quality = "HIGHEST"

    contract["lead_quality"] = lead_quality
    contract["lead_signals"] = "; ".join(signals)

    return contract


def write_csv(contracts, output_path):
    """Write contracts to CSV."""
    if not contracts:
        print("No contracts to write.")
        return

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    columns = [
        "title", "buyer_name", "buyer_region", "buyer_locality",
        "value_amount", "value_currency", "min_value", "max_value",
        "status", "notice_type", "lead_quality", "lead_signals",
        "categories", "description",
        "tender_start", "tender_end",
        "contract_start", "contract_end",
        "contact_name", "contact_email", "contact_phone",
        "awarded_to", "award_date", "award_value",
        "procurement_method", "published_date",
        "notice_id", "ocid", "cf_url",
        "search_keyword", "scraped_at"
    ]

    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=columns, extrasaction="ignore")
        writer.writeheader()
        for c in contracts:
            c["scraped_at"] = datetime.now().isoformat()
            writer.writerow(c)

    print(f"\nWrote {len(contracts)} contracts to {output_path}")


def print_summary(contracts):
    """Print summary."""
    if not contracts:
        print("No contracts found.")
        return

    print("\n" + "=" * 70)
    print("UK CONTRACTS FINDER SCRAPE SUMMARY")
    print("=" * 70)
    print(f"Total contracts/tenders found: {len(contracts)}")

    # By type
    by_type = {}
    for c in contracts:
        t = c.get("notice_type", "Unknown")
        by_type[t] = by_type.get(t, 0) + 1
    print(f"\nBy type:")
    for t, count in sorted(by_type.items(), key=lambda x: x[1], reverse=True):
        print(f"  {t}: {count}")

    # By quality
    by_quality = {}
    for c in contracts:
        q = c.get("lead_quality", "Unknown")
        by_quality[q] = by_quality.get(q, 0) + 1
    print(f"\nBy lead quality:")
    for q, count in sorted(by_quality.items(), key=lambda x: x[1], reverse=True):
        print(f"  {q}: {count}")

    # Total value
    values = []
    for c in contracts:
        v = c.get("value_amount") or c.get("max_value") or 0
        try:
            values.append(float(v))
        except (ValueError, TypeError):
            pass

    if values:
        print(f"\nValue stats:")
        print(f"  Total value: GBP {sum(values):,.0f}")
        print(f"  Average: GBP {sum(values)/len(values):,.0f}")
        print(f"  Highest: GBP {max(values):,.0f}")
        print(f"  Contracts with value: {len(values)}/{len(contracts)}")

    # With contact email
    with_email = [c for c in contracts if c.get("contact_email")]
    print(f"\nContracts with contact email: {len(with_email)}")

    # Top buyers
    buyer_counts = {}
    for c in contracts:
        buyer = c.get("buyer_name", "Unknown")
        if buyer:
            buyer_counts[buyer] = buyer_counts.get(buyer, 0) + 1

    if buyer_counts:
        print(f"\nTop buyers (most contracts):")
        for buyer, count in sorted(buyer_counts.items(), key=lambda x: x[1], reverse=True)[:10]:
            print(f"  {buyer[:50]:50s} {count} contracts")

    # Top 10 by value
    valued = [c for c in contracts if c.get("value_amount")]
    if valued:
        valued_sorted = sorted(valued, key=lambda x: float(x.get("value_amount", 0) or 0), reverse=True)
        print(f"\nTop 10 by value:")
        for i, c in enumerate(valued_sorted[:10]):
            val = float(c.get("value_amount", 0) or 0)
            print(f"  {i+1}. GBP {val:>12,.0f}  {c['title'][:50]}")

    # By keyword
    by_keyword = {}
    for c in contracts:
        kw = c.get("search_keyword", "Unknown")
        by_keyword[kw] = by_keyword.get(kw, 0) + 1
    print(f"\nBy search keyword:")
    for kw, count in sorted(by_keyword.items(), key=lambda x: x[1], reverse=True):
        print(f"  {kw}: {count}")

    print("=" * 70)


def main():
    parser = argparse.ArgumentParser(description="UK Contracts Finder Scraper")
    parser.add_argument("--keyword", type=str, help="Single keyword to search")
    parser.add_argument("--keywords", nargs="+", help="Multiple keywords to search")
    parser.add_argument("--stages", choices=["tender", "award", "both"], default="both",
                        help="tender=open opps, award=awarded, both=all (default: both)")
    parser.add_argument("--days-back", type=int, default=90, help="Days back to search (default: 90)")
    parser.add_argument("--min-value", type=int, help="Minimum contract value in GBP")
    parser.add_argument("--max-value", type=int, help="Maximum contract value in GBP")
    parser.add_argument("--max-per-keyword", type=int, default=100, help="Max results per keyword")
    parser.add_argument("--output", type=str, default=str(OUTPUT_FILE))

    args = parser.parse_args()

    print("=" * 70)
    print("UK CONTRACTS FINDER SCRAPER")
    print("=" * 70)
    print("Strategy: UK government contracts = verified buyers with real budgets.")
    print("Same play as USAspending but for the GBP 290B+ UK public procurement market.\n")

    keywords = []
    if args.keyword:
        keywords = [args.keyword]
    elif args.keywords:
        keywords = args.keywords
    else:
        keywords = DEFAULT_KEYWORDS

    published_from = (datetime.now() - timedelta(days=args.days_back)).strftime("%Y-%m-%d")
    published_to = datetime.now().strftime("%Y-%m-%d")

    stages_to_search = []
    if args.stages == "both":
        stages_to_search = ["tender", "award"]
    else:
        stages_to_search = [args.stages]

    print(f"Keywords: {len(keywords)}")
    print(f"Stages: {stages_to_search}")
    print(f"Date range: {published_from} to {published_to}")
    if args.min_value:
        print(f"Min value: GBP {args.min_value:,}")
    print()

    all_contracts = []
    seen_ids = set()

    for keyword in keywords:
        for stage in stages_to_search:
            print(f"\n--- {keyword} ({stage}) ---")
            page = 1
            keyword_count = 0

            while keyword_count < args.max_per_keyword:
                data = search_contracts(
                    keyword=keyword,
                    stages=stage,
                    published_from=published_from,
                    published_to=published_to,
                    min_value=args.min_value,
                    max_value=args.max_value,
                    page=page,
                    size=min(100, args.max_per_keyword - keyword_count)
                )

                if not data:
                    print(f"  No data returned from API, trying HTML fallback...")
                    html_results = search_notices_html(keyword=keyword, published_from=published_from)
                    for r in html_results:
                        r["search_keyword"] = keyword
                        r["notice_type"] = stage
                    all_contracts.extend(html_results)
                    break

                contracts = parse_ocds_results(data)

                if not contracts:
                    print(f"  No more results (page {page})")
                    break

                for c in contracts:
                    cid = c.get("notice_id", "") or c.get("ocid", "")
                    if cid not in seen_ids:
                        seen_ids.add(cid)
                        c["search_keyword"] = keyword
                        all_contracts.append(c)
                        keyword_count += 1

                print(f"  Page {page}: {len(contracts)} results (total: {keyword_count})")

                if len(contracts) < 100:
                    break

                page += 1
                time.sleep(RATE_LIMIT_DELAY)

        time.sleep(RATE_LIMIT_DELAY)

    # Classify leads
    for c in all_contracts:
        classify_contract_lead(c)

    print(f"\n{len(all_contracts)} unique contracts after deduplication")

    print_summary(all_contracts)
    write_csv(all_contracts, args.output)

    print(f"\nNext steps:")
    print(f"  1. Filter for ACTIVE_TENDER (can still bid or partner with bidder)")
    print(f"  2. Contracts with contact_email = direct outreach possible")
    print(f"  3. Look at awarded_to companies = they won, they need subcontractors")
    print(f"  4. Losing bidders from big contracts = they need an edge")
    print(f"  5. Cold email UK gov suppliers offering complementary services")


if __name__ == "__main__":
    main()
