#!/usr/bin/env python3
"""
SAM.gov Government Contract Monitor
Source: @pipelineabuser tweet - "tendersinfo.com / government contracts before they close"
Also: ALPHA015, Government Contracts Method MM071

Searches SAM.gov public API for small business opportunities matching our capabilities.
Outputs to LEDGER/GOV_OPPORTUNITIES.csv and prints summary.

Usage:
    python3 sam_gov_monitor.py                    # Run with defaults
    python3 sam_gov_monitor.py --keywords "web development,data analysis"
    python3 sam_gov_monitor.py --state CA --limit 50
"""

import argparse
import csv
import json
import os
import re
import sys
from datetime import datetime, timedelta
from pathlib import Path
from urllib.request import urlopen, Request
from urllib.parse import urlencode, quote
from urllib.error import URLError, HTTPError

BASE_DIR = Path(__file__).parent.parent
OUTPUT_CSV = BASE_DIR / "LEDGER" / "GOV_OPPORTUNITIES.csv"
LOG_FILE = BASE_DIR / "AUTOMATIONS" / "logs" / "sam_gov_monitor.log"

# SAM.gov search endpoint (public search API used by sam.gov web app).
SAM_SEARCH_API_BASE = "https://sam.gov/api/prod/sgs/v1/search/"

# NAICS codes we can fulfill with Claude Code
NAICS_CODES = [
    "541511",  # Custom Computer Programming
    "541512",  # Computer Systems Design
    "541519",  # Other Computer Related Services
    "541611",  # Administrative Management Consulting
    "541613",  # Marketing Consulting
    "541810",  # Advertising Agencies
    "541820",  # Public Relations
    "541910",  # Marketing Research
    "541990",  # Other Professional Services
    "561410",  # Document Preparation Services
    "611430",  # Professional Development Training
]

KEYWORDS = [
    "technical writing",
    "web development",
    "website redesign",
    "data analysis",
    "content development",
    "content creation",
    "training development",
    "software development",
    "digital marketing",
    "social media",
    "research report",
    "documentation",
]

SET_ASIDE_CODES = {
    "SBA": "Total Small Business",
    "SBP": "Partial Small Business",
    "8A": "8(a) Set-Aside",
    "8AN": "8(a) Sole Source",
    "HZC": "HUBZone",
    "HZS": "HUBZone Sole Source",
    "SDVOSBC": "Service-Disabled Veteran-Owned",
    "SDVOSBS": "SDVO Sole Source",
    "WOSB": "Women-Owned Small Business",
    "WOSBSS": "WOSB Sole Source",
}


def log(msg):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_msg = f"[{timestamp}] {msg}"
    print(log_msg)
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(LOG_FILE, "a") as f:
        f.write(log_msg + "\n")


def strip_html(text):
    """Remove basic HTML tags from API snippets."""
    if not text:
        return ""
    text = re.sub(r"<[^>]+>", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def parse_iso_date(date_str):
    if not date_str:
        return ""
    return date_str[:10]


def extract_agency(organization_hierarchy):
    """Pick the most specific org name available."""
    if not isinstance(organization_hierarchy, list):
        return ""
    for org in reversed(organization_hierarchy):
        name = org.get("name", "")
        if name:
            return name
    return ""


def search_sam_gov(keyword, limit=25, posted_from=None, api_key=None):
    """Search SAM.gov active opportunities using the public search API."""

    params = {
        "index": "opp",
        "page": "0",
        "sort": "-modifiedDate",
        "size": str(limit),
        "mode": "search",
        "is_active": "true",
        "q": keyword,
    }

    url = f"{SAM_SEARCH_API_BASE}?{urlencode(params)}"
    headers = {
        "Accept": "application/json, text/plain, */*",
        "User-Agent": "PRINTMAXX-Monitor/1.0",
        "Origin": "https://sam.gov",
        "Referer": "https://sam.gov/search/",
    }

    try:
        req = Request(url, headers=headers)
        with urlopen(req, timeout=30) as response:
            data = json.loads(response.read().decode())
            return data
    except HTTPError as e:
        if e.code == 429:
            log(f"SAM.gov rate-limited for keyword: {keyword}")
            return None
        if e.code in (403, 404):
            log(f"SAM.gov search API unavailable (HTTP {e.code}) for keyword: {keyword}")
            return None
        log(f"HTTP error {e.code} for keyword: {keyword}")
        return None
    except (URLError, Exception) as e:
        log(f"Error searching SAM.gov for '{keyword}': {e}")
        return None


def search_sam_gov_html(keyword, state=None):
    """Fallback: scrape SAM.gov search results page."""
    search_url = f"https://sam.gov/search/?index=opp&q={quote(keyword)}&sort=-relevance&page=1&pageSize=25"
    if state:
        search_url += f"&sfm%5Bstatus%5D%5Bis_active%5D=true&sfm%5BsimpleSearch%5D%5BkeywordRadio%5D=ALL"

    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
        "Accept": "text/html,application/xhtml+xml",
    }

    try:
        req = Request(search_url, headers=headers)
        with urlopen(req, timeout=30) as response:
            html = response.read().decode("utf-8", errors="replace")
            # Extract opportunity count from page
            import re
            count_match = re.search(r'"totalCount":(\d+)', html)
            total = int(count_match.group(1)) if count_match else 0
            return {"url": search_url, "total": total, "keyword": keyword}
    except Exception as e:
        log(f"HTML fallback error for '{keyword}': {e}")
        return {"url": search_url, "total": 0, "keyword": keyword, "error": str(e)}


def search_usaspending(naics_code, limit=10):
    """Search USAspending.gov for recent contract awards (expiring contracts = opportunity)."""
    url = "https://api.usaspending.gov/api/v2/search/spending_by_award/"
    payload = json.dumps({
        "filters": {
            "naics_codes": [naics_code],
            "time_period": [
                {
                    "start_date": (datetime.now() - timedelta(days=365)).strftime("%Y-%m-%d"),
                    "end_date": datetime.now().strftime("%Y-%m-%d"),
                }
            ],
            "award_type_codes": ["A", "B", "C", "D"],  # Contracts
        },
        "fields": [
            "Award ID",
            "Recipient Name",
            "Total Obligation",
            "Period of Performance Start Date",
            "Period of Performance Current End Date",
            "Awarding Agency",
            "Description",
        ],
        "limit": limit,
        "page": 1,
        "sort": "Period of Performance Current End Date",
        "order": "asc",
    }).encode()

    headers = {
        "Content-Type": "application/json",
        "User-Agent": "PRINTMAXX-Monitor/1.0",
    }

    try:
        req = Request(url, data=payload, headers=headers, method="POST")
        with urlopen(req, timeout=30) as response:
            data = json.loads(response.read().decode())
            return data
    except Exception as e:
        log(f"USAspending error for NAICS {naics_code}: {e}")
        return None


def load_existing_opportunities():
    """Load existing opportunities to avoid duplicates."""
    existing = set()
    if OUTPUT_CSV.exists():
        with open(OUTPUT_CSV, "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                existing.add(row.get("opportunity_id", "") or row.get("title", ""))
    return existing


def save_opportunities(opportunities):
    """Save opportunities to CSV."""
    OUTPUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    file_exists = OUTPUT_CSV.exists()

    fieldnames = [
        "opportunity_id",
        "title",
        "agency",
        "posted_date",
        "response_deadline",
        "set_aside",
        "naics",
        "estimated_value",
        "description",
        "url",
        "source",
        "keyword_match",
        "found_date",
        "status",
        "notes",
    ]

    with open(OUTPUT_CSV, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        for opp in opportunities:
            writer.writerow(opp)


def run_sam_search(keywords=None, state=None, limit=25, api_key=None):
    """Run full SAM.gov search across all keywords."""
    if keywords is None:
        keywords = KEYWORDS

    existing = load_existing_opportunities()
    all_opportunities = []
    total_found = 0

    log(f"Starting SAM.gov search with {len(keywords)} keywords...")

    for keyword in keywords:
        log(f"Searching: '{keyword}'...")

        # Try SAM.gov search API first
        result = search_sam_gov(keyword, limit=limit, api_key=api_key)

        if result and "_embedded" in result and "results" in result["_embedded"]:
            opps = result["_embedded"]["results"]
            log(f"  Found {len(opps)} opportunities via SAM search API")
            for opp in opps:
                opp_id = opp.get("_id", "")
                if opp_id in existing:
                    continue

                desc_raw = ""
                descs = opp.get("descriptions", [])
                if isinstance(descs, list) and descs:
                    desc_raw = descs[0].get("content", "")

                opportunity = {
                    "opportunity_id": opp_id,
                    "title": opp.get("title", ""),
                    "agency": extract_agency(opp.get("organizationHierarchy", [])),
                    "posted_date": parse_iso_date(opp.get("publishDate", "")),
                    "response_deadline": parse_iso_date(opp.get("responseDate", "")),
                    "set_aside": "",
                    "naics": "",
                    "estimated_value": "",
                    "description": strip_html(desc_raw)[:500],
                    "url": f"https://sam.gov/opp/{opp_id}/view",
                    "source": "SAM.gov Search API",
                    "keyword_match": keyword,
                    "found_date": datetime.now().strftime("%Y-%m-%d"),
                    "status": "NEW",
                    "notes": "",
                }
                all_opportunities.append(opportunity)
                existing.add(opp_id)
                total_found += 1
        elif result and "opportunitiesData" in result:
            opps = result["opportunitiesData"]
            log(f"  Found {len(opps)} opportunities via legacy API")
            for opp in opps:
                opp_id = opp.get("noticeId", "")
                if opp_id in existing:
                    continue
                opportunity = {
                    "opportunity_id": opp_id,
                    "title": opp.get("title", ""),
                    "agency": opp.get("department", "") or opp.get("subtier", ""),
                    "posted_date": opp.get("postedDate", ""),
                    "response_deadline": opp.get("responseDeadLine", ""),
                    "set_aside": opp.get("typeOfSetAside", ""),
                    "naics": opp.get("naicsCode", ""),
                    "estimated_value": "",
                    "description": (opp.get("description", "") or "")[:500],
                    "url": f"https://sam.gov/opp/{opp_id}/view",
                    "source": "SAM.gov Legacy API",
                    "keyword_match": keyword,
                    "found_date": datetime.now().strftime("%Y-%m-%d"),
                    "status": "NEW",
                    "notes": "",
                }
                all_opportunities.append(opportunity)
                existing.add(opp_id)
                total_found += 1
        else:
            # Fallback to HTML search for count
            html_result = search_sam_gov_html(keyword, state)
            total_count = html_result.get("total", 0)
            log(f"  HTML search: ~{total_count} results for '{keyword}' (manual review needed)")
            if total_count > 0:
                opportunity = {
                    "opportunity_id": f"SEARCH_{keyword.replace(' ', '_').upper()}",
                    "title": f"[SEARCH RESULT] {keyword} - {total_count} opportunities found",
                    "agency": "Various",
                    "posted_date": datetime.now().strftime("%Y-%m-%d"),
                    "response_deadline": "",
                    "set_aside": "",
                    "naics": "",
                    "estimated_value": "",
                    "description": f"Search '{keyword}' returned {total_count} results. Manual review at: {html_result['url']}",
                    "url": html_result["url"],
                    "source": "SAM.gov HTML",
                    "keyword_match": keyword,
                    "found_date": datetime.now().strftime("%Y-%m-%d"),
                    "status": "NEEDS_REVIEW",
                    "notes": f"API may require key. Review manually at URL.",
                }
                all_opportunities.append(opportunity)
                total_found += 1

    return all_opportunities, total_found


def run_usaspending_search():
    """Search USAspending for expiring contracts we could bid on."""
    log("Searching USAspending.gov for expiring contracts...")
    expiring_contracts = []

    for naics in NAICS_CODES[:5]:  # Top 5 NAICS codes
        result = search_usaspending(naics, limit=5)
        if result and "results" in result:
            for contract in result["results"]:
                end_date_str = contract.get("Period of Performance Current End Date", "")
                if end_date_str:
                    try:
                        end_date = datetime.strptime(end_date_str, "%Y-%m-%d")
                        days_until_expiry = (end_date - datetime.now()).days
                        if 0 < days_until_expiry < 180:  # Expiring within 6 months
                            expiring_contracts.append({
                                "opportunity_id": contract.get("Award ID", ""),
                                "title": f"[EXPIRING] {contract.get('Description', '')[:200]}",
                                "agency": contract.get("Awarding Agency", ""),
                                "posted_date": contract.get("Period of Performance Start Date", ""),
                                "response_deadline": end_date_str,
                                "set_aside": "",
                                "naics": naics,
                                "estimated_value": str(contract.get("Total Obligation", "")),
                                "description": f"Current holder: {contract.get('Recipient Name', '')}. Expires in {days_until_expiry} days. Potential rebid opportunity.",
                                "url": f"https://www.usaspending.gov/award/{contract.get('Award ID', '')}",
                                "source": "USAspending.gov",
                                "keyword_match": f"NAICS {naics}",
                                "found_date": datetime.now().strftime("%Y-%m-%d"),
                                "status": "EXPIRING",
                                "notes": f"Days until expiry: {days_until_expiry}. File FOIA for winning proposal details.",
                            })
                    except ValueError:
                        pass
            log(f"  NAICS {naics}: found {len(result.get('results', []))} contracts")

    return expiring_contracts


def generate_foia_request(contract_id, agency_name=""):
    """Generate a FOIA request letter for competitive intel on a contract."""
    return f"""Subject: FOIA Request - Contract {contract_id}

Dear FOIA Officer,

Under the Freedom of Information Act (5 U.S.C. 552), I request access to the
following records related to contract {contract_id}:

1. The winning proposal (technical and pricing volumes)
2. Source selection evaluation documentation
3. Names of all offerors (winning and losing)
4. Award amount and period of performance
5. Performance evaluation reports (if available)

I am willing to pay reasonable duplication fees up to $25. Please contact me
if costs will exceed this amount.

I request a fee waiver as this information will contribute to public understanding
of government operations.

Thank you,
[YOUR NAME]
[YOUR EMAIL]
[YOUR PHONE]

Agency: {agency_name}
Contract: {contract_id}
Date: {datetime.now().strftime('%Y-%m-%d')}
"""


def main():
    parser = argparse.ArgumentParser(description="SAM.gov Government Contract Monitor")
    parser.add_argument("--keywords", type=str, help="Comma-separated keywords to search")
    parser.add_argument("--state", type=str, help="State abbreviation (e.g., CA, TX)")
    parser.add_argument("--limit", type=int, default=25, help="Results per keyword (default: 25)")
    parser.add_argument("--api-key", type=str, help="SAM.gov API key (optional, get free at api.data.gov)")
    parser.add_argument("--usaspending", action="store_true", help="Also search USAspending for expiring contracts")
    parser.add_argument("--foia", type=str, help="Generate FOIA request for a contract ID")
    parser.add_argument("--summary", action="store_true", help="Just show summary of saved opportunities")
    args = parser.parse_args()

    # Check for API key in env
    api_key = args.api_key or os.environ.get("SAM_GOV_API_KEY", "")

    if args.foia:
        print(generate_foia_request(args.foia))
        return

    if args.summary:
        if OUTPUT_CSV.exists():
            with open(OUTPUT_CSV, "r") as f:
                reader = list(csv.DictReader(f))
                print(f"\n{'='*60}")
                print(f"GOV CONTRACT OPPORTUNITIES SUMMARY")
                print(f"{'='*60}")
                print(f"Total opportunities tracked: {len(reader)}")
                statuses = {}
                for row in reader:
                    s = row.get("status", "UNKNOWN")
                    statuses[s] = statuses.get(s, 0) + 1
                for status, count in sorted(statuses.items()):
                    print(f"  {status}: {count}")
                print(f"\nFile: {OUTPUT_CSV}")
        else:
            print("No opportunities tracked yet. Run without --summary to search.")
        return

    keywords = args.keywords.split(",") if args.keywords else KEYWORDS

    print(f"\n{'='*60}")
    print(f"SAM.gov GOVERNMENT CONTRACT MONITOR")
    print(f"Source: @pipelineabuser + ALPHA015 + MM071")
    print(f"{'='*60}")
    print(f"Searching {len(keywords)} keywords...")
    print(f"API key (legacy endpoint only): {'SET' if api_key else 'NOT SET'}")
    print()

    # Search SAM.gov
    opportunities, total = run_sam_search(keywords, args.state, args.limit, api_key)

    # Search USAspending if requested
    if args.usaspending:
        expiring = run_usaspending_search()
        opportunities.extend(expiring)
        total += len(expiring)

    # Save results
    if opportunities:
        save_opportunities(opportunities)
        log(f"Saved {len(opportunities)} new opportunities to {OUTPUT_CSV}")

    # Print summary
    print(f"\n{'='*60}")
    print(f"RESULTS SUMMARY")
    print(f"{'='*60}")
    print(f"New opportunities found: {total}")
    print(f"Output: {OUTPUT_CSV}")
    print(f"\nNext steps:")
    print(f"  1. Review opportunities in {OUTPUT_CSV}")
    print(f"  2. Register on SAM.gov (https://sam.gov) if not done")
    print(f"  3. Generate FOIA for interesting contracts: python3 sam_gov_monitor.py --foia CONTRACT_ID")
    print(f"  4. Run daily: add to crontab or ralph loop")


if __name__ == "__main__":
    main()
