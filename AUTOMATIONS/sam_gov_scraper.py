#!/usr/bin/env python3
"""
SAM.gov Federal Contract Opportunity Scraper
---------------------------------------------
Pulls active federal contract opportunities from the SAM.gov public search API.
Enriches each result with NAICS, set-aside, contacts from the detail endpoint.
Outputs to CSV for lead generation and bid analysis.

Usage:
    python3 sam_gov_scraper.py
    python3 sam_gov_scraper.py --state TX --max-results 50
    python3 sam_gov_scraper.py --keyword "IT services" --state TX

SAM.gov public search: https://sam.gov/search/
"""

import argparse
import csv
import json
import os
import re
import ssl
import sys
import time
from datetime import datetime, timedelta
from urllib.parse import urlencode, quote
from urllib.request import urlopen, Request
from urllib.error import HTTPError, URLError

# ---------- SSL ----------
SSL_CTX = ssl.create_default_context()
SSL_CTX.check_hostname = False
SSL_CTX.verify_mode = ssl.CERT_NONE

# ---------- CONFIG ----------
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "leads")
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "sam_gov_opportunities.csv")

# Endpoints
SEARCH_URL = "https://sam.gov/api/prod/sgs/v1/search/"
DETAIL_URL = "https://sam.gov/api/prod/opps/v2/opportunities/"

# Set-aside code map
SET_ASIDE_MAP = {
    "SBA": "Total Small Business Set-Aside",
    "SBP": "Partial Small Business Set-Aside",
    "8A": "8(a) Set-Aside",
    "8AN": "8(a) Sole Source",
    "HZC": "HUBZone Set-Aside",
    "HZS": "HUBZone Sole Source",
    "SDVOSBC": "Service-Disabled Veteran-Owned Small Business",
    "SDVOSBS": "SDVOSB Sole Source",
    "WOSB": "Women-Owned Small Business",
    "WOSBSS": "WOSB Sole Source",
    "EDWOSB": "Economically Disadvantaged WOSB",
    "EDWOSBSS": "EDWOSB Sole Source",
    "LAS": "Local Area Set-Aside",
    "IEE": "Indian Economic Enterprise",
    "ISBEE": "Indian Small Business Economic Enterprise",
    "BICiv": "Buy Indian Civilian",
    "VSA": "Veteran-Owned Small Business Set-Aside",
    "VSS": "Veteran-Owned Small Business Sole Source",
}

CSV_COLUMNS = [
    "notice_id",
    "title",
    "solicitation_number",
    "opportunity_type",
    "agency",
    "sub_agency",
    "office",
    "naics_code",
    "classification_code",
    "set_aside_type",
    "set_aside_description",
    "response_deadline",
    "posted_date",
    "archive_date",
    "place_of_performance_state",
    "place_of_performance_city",
    "description_snippet",
    "point_of_contact_name",
    "point_of_contact_email",
    "point_of_contact_phone",
    "sam_gov_link",
]


def fetch_json(url, retries=3):
    """Fetch JSON from URL with retry logic."""
    for attempt in range(retries):
        try:
            req = Request(url)
            req.add_header("User-Agent", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36")
            req.add_header("Accept", "application/json, text/plain, */*")
            req.add_header("Origin", "https://sam.gov")
            req.add_header("Referer", "https://sam.gov/search/")
            with urlopen(req, timeout=20, context=SSL_CTX) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except HTTPError as e:
            if e.code == 429:
                wait = 5 * (attempt + 1)
                print(f"    Rate limited. Waiting {wait}s...")
                time.sleep(wait)
            else:
                print(f"    HTTP {e.code} on attempt {attempt+1}")
                if attempt < retries - 1:
                    time.sleep(2)
        except (URLError, Exception) as e:
            print(f"    Error on attempt {attempt+1}: {e}")
            if attempt < retries - 1:
                time.sleep(2)
    return None


def clean_html(text):
    """Strip HTML tags and normalize whitespace."""
    if not text:
        return ""
    text = re.sub(r'<[^>]+>', ' ', text)
    text = re.sub(r'&nbsp;', ' ', text)
    text = re.sub(r'&amp;', '&', text)
    text = re.sub(r'&lt;', '<', text)
    text = re.sub(r'&gt;', '>', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def search_opportunities(keyword="", page=0, size=25):
    """Search SAM.gov for active opportunities."""
    params = {
        "index": "opp",
        "page": page,
        "sort": "-modifiedDate",
        "size": size,
        "mode": "search",
        "is_active": "true",
    }
    if keyword:
        params["q"] = keyword

    url = f"{SEARCH_URL}?{urlencode(params)}"
    return fetch_json(url)


def get_opportunity_detail(opp_id):
    """Get full details for a single opportunity."""
    url = f"{DETAIL_URL}{opp_id}"
    return fetch_json(url)


def parse_search_result(result):
    """Parse a search result into a basic record."""
    record = {}
    record["notice_id"] = result.get("_id", "")
    record["title"] = result.get("title", "")
    record["solicitation_number"] = result.get("solicitationNumber", "")

    opp_type = result.get("type", {})
    if isinstance(opp_type, dict):
        record["opportunity_type"] = opp_type.get("value", opp_type.get("code", ""))
    else:
        record["opportunity_type"] = str(opp_type)

    # Agency from org hierarchy
    org_hierarchy = result.get("organizationHierarchy", [])
    record["agency"] = ""
    record["sub_agency"] = ""
    record["office"] = ""
    for org in org_hierarchy:
        level = org.get("level", 0)
        name = org.get("name", "")
        if level == 1:
            record["agency"] = name
        elif level == 2:
            record["sub_agency"] = name
        elif level >= 4:
            record["office"] = name

    # Dates
    record["response_deadline"] = result.get("responseDate", "")
    record["posted_date"] = result.get("publishDate", "")

    # Description from search
    descs = result.get("descriptions", [])
    if descs and isinstance(descs, list):
        desc_content = descs[0].get("content", "")
        record["description_snippet"] = clean_html(desc_content)[:500]
    else:
        record["description_snippet"] = ""

    record["sam_gov_link"] = f"https://sam.gov/opp/{record['notice_id']}/view"

    # These get filled by detail endpoint
    record["naics_code"] = ""
    record["classification_code"] = ""
    record["set_aside_type"] = ""
    record["set_aside_description"] = ""
    record["archive_date"] = ""
    record["place_of_performance_state"] = ""
    record["place_of_performance_city"] = ""
    record["point_of_contact_name"] = ""
    record["point_of_contact_email"] = ""
    record["point_of_contact_phone"] = ""

    return record


def enrich_with_detail(record, detail):
    """Enrich a search result record with detail API data."""
    if not detail:
        return record

    data = detail.get("data2", {})

    # NAICS
    naics_list = data.get("naics", [])
    if naics_list:
        codes = []
        for n in naics_list:
            code_val = n.get("code", [])
            if isinstance(code_val, list):
                codes.extend(code_val)
            else:
                codes.append(str(code_val))
        record["naics_code"] = ", ".join(codes)

    # Classification code
    record["classification_code"] = data.get("classificationCode", "")

    # Set-aside
    sol = data.get("solicitation", {})
    set_aside_code = sol.get("setAside", "")
    record["set_aside_type"] = set_aside_code
    record["set_aside_description"] = SET_ASIDE_MAP.get(set_aside_code, set_aside_code)

    # Archive date
    archive = data.get("archive", {})
    record["archive_date"] = archive.get("date", "")

    # Place of performance
    pop = data.get("placeOfPerformance", {})
    if pop:
        state = pop.get("state", {})
        if isinstance(state, dict):
            record["place_of_performance_state"] = state.get("code", "")
        city = pop.get("city", {})
        if isinstance(city, dict):
            record["place_of_performance_city"] = city.get("name", "")

    # Contacts
    contacts = data.get("pointOfContact", [])
    if contacts and isinstance(contacts, list):
        c = contacts[0]
        record["point_of_contact_name"] = c.get("fullName", "")
        record["point_of_contact_email"] = c.get("email", "")
        record["point_of_contact_phone"] = c.get("phone", "")

    # Better description from detail
    desc_list = detail.get("description", [])
    if desc_list and isinstance(desc_list, list):
        body = desc_list[0].get("body", "")
        cleaned = clean_html(body)
        if len(cleaned) > len(record["description_snippet"]):
            record["description_snippet"] = cleaned[:800]

    return record


def filter_by_state(records, state):
    """Filter to records matching state or nationwide."""
    if not state:
        return records
    state = state.upper()
    return [r for r in records if
            r["place_of_performance_state"].upper() == state
            or r["place_of_performance_state"] == ""
            or r["place_of_performance_state"].upper() in ("US", "")]


def write_csv(records, output_file):
    """Write records to CSV."""
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_COLUMNS, extrasaction="ignore")
        writer.writeheader()
        for r in records:
            writer.writerow(r)
    print(f"\n  Wrote {len(records)} opportunities to: {output_file}")


def print_summary(records):
    """Print top results summary."""
    print(f"\n{'='*75}")
    print(f"  SAM.gov Opportunities - {len(records)} results")
    print(f"{'='*75}")

    if not records:
        print("  No opportunities found.")
        return

    for i, r in enumerate(records[:15], 1):
        title = r["title"][:65]
        agency = r["agency"][:35]
        naics = r["naics_code"][:15] if r["naics_code"] else "N/A"
        set_aside = r["set_aside_description"][:30] if r["set_aside_description"] else "Full & Open"
        deadline = r["response_deadline"][:10] if r["response_deadline"] else "No deadline"
        state = r["place_of_performance_state"] or "N/A"
        contact = r["point_of_contact_email"][:35] if r["point_of_contact_email"] else "N/A"

        print(f"\n  [{i:2d}] {title}")
        print(f"       Agency: {agency} | NAICS: {naics}")
        print(f"       Set-Aside: {set_aside} | State: {state}")
        print(f"       Deadline: {deadline} | Contact: {contact}")
        print(f"       {r['sam_gov_link']}")

    if len(records) > 15:
        print(f"\n  ... and {len(records) - 15} more in CSV.")


def main():
    parser = argparse.ArgumentParser(description="SAM.gov Federal Contract Opportunity Scraper")
    parser.add_argument("--keyword", default="", help="Search keyword (e.g. 'IT services', 'construction texas')")
    parser.add_argument("--state", default="TX", help="Filter by state (e.g. TX, CA, NY). Empty = all states")
    parser.add_argument("--max-results", type=int, default=50, help="Max opportunities to fetch (default: 50)")
    parser.add_argument("--enrich", action="store_true", default=True, help="Fetch detail for each result (NAICS, contacts)")
    parser.add_argument("--no-enrich", action="store_true", help="Skip detail fetching (faster but less data)")
    parser.add_argument("--output", default=OUTPUT_FILE, help="Output CSV path")
    parser.add_argument("--json-dump", action="store_true", help="Also dump raw JSON")

    args = parser.parse_args()
    do_enrich = not args.no_enrich

    print(f"\n{'='*75}")
    print("  PRINTMAXX Government Contract Intelligence System v2.0")
    print(f"{'='*75}")
    print(f"  Keyword: {args.keyword or '(all active)'}")
    print(f"  State filter: {args.state or 'ALL'}")
    print(f"  Max results: {args.max_results}")
    print(f"  Enrich details: {do_enrich}")
    print(f"{'='*75}")

    # --- SEARCH ---
    all_records = []
    page = 0
    page_size = 25

    while len(all_records) < args.max_results:
        remaining = args.max_results - len(all_records)
        fetch_size = min(page_size, remaining)

        # If state specified, include it in keyword for better results
        search_keyword = args.keyword
        if args.state and not args.keyword:
            # Search for state name to get relevant results
            state_names = {
                "TX": "texas", "CA": "california", "NY": "new york",
                "FL": "florida", "IL": "illinois", "VA": "virginia",
                "MD": "maryland", "DC": "washington dc", "GA": "georgia",
                "PA": "pennsylvania", "OH": "ohio", "NC": "north carolina",
                "CO": "colorado", "WA": "washington state", "AZ": "arizona",
                "MA": "massachusetts", "NJ": "new jersey", "MI": "michigan",
            }
            search_keyword = state_names.get(args.state.upper(), args.state)

        print(f"\n  Fetching page {page+1} (searching: '{search_keyword}')...")
        data = search_opportunities(keyword=search_keyword, page=page, size=fetch_size)

        if not data:
            print("  Failed to fetch search results.")
            break

        results = data.get("_embedded", {}).get("results", [])
        total = data.get("page", {}).get("totalElements", 0)

        if page == 0:
            print(f"  Total available: {total} opportunities")

        if not results:
            print("  No more results.")
            break

        for r in results:
            record = parse_search_result(r)
            all_records.append(record)

        print(f"  Fetched {len(results)} results (total collected: {len(all_records)})")

        if len(results) < fetch_size:
            break

        page += 1
        time.sleep(0.5)

    print(f"\n  Total search results: {len(all_records)}")

    # --- ENRICH ---
    if do_enrich and all_records:
        print(f"\n  Enriching {len(all_records)} opportunities with detail data...")
        enriched = 0
        for i, record in enumerate(all_records):
            opp_id = record["notice_id"]
            if not opp_id:
                continue

            detail = get_opportunity_detail(opp_id)
            if detail:
                enrich_with_detail(record, detail)
                enriched += 1

            # Progress
            if (i + 1) % 10 == 0 or i == len(all_records) - 1:
                print(f"    Enriched {i+1}/{len(all_records)}...")

            time.sleep(0.3)  # Rate limiting

        print(f"  Successfully enriched {enriched}/{len(all_records)} opportunities")

    # --- FILTER ---
    if args.state:
        pre = len(all_records)
        all_records = filter_by_state(all_records, args.state)
        print(f"\n  State filter ({args.state}): {pre} -> {len(all_records)}")

    # --- SORT by deadline ---
    def sort_key(r):
        d = r.get("response_deadline", "")
        if d:
            try:
                # ISO format
                return datetime.fromisoformat(d.replace("+00:00", "+0000").replace("Z", "+0000")[:19])
            except Exception:
                pass
        return datetime.max

    all_records.sort(key=sort_key)

    # --- OUTPUT ---
    write_csv(all_records, args.output)

    if args.json_dump:
        json_path = args.output.replace(".csv", ".json")
        with open(json_path, "w") as f:
            json.dump(all_records, f, indent=2, default=str)
        print(f"  JSON dump saved to: {json_path}")

    print_summary(all_records)

    return all_records


if __name__ == "__main__":
    records = main()
