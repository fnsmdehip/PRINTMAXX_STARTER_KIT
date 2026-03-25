#!/usr/bin/env python3

from __future__ import annotations
"""
Government Contract Opportunity Scraper
========================================
Sources (in priority order):
  1. SAM.gov API (api.sam.gov) - Official US govt procurement portal, FREE public API
  2. USAspending.gov API - Federal spending data, FREE public API
  3. tendersinfo.com - Aggregator (browser-based, fallback)

Outputs: AUTOMATIONS/leads/gov_tenders_active.csv

Usage:
  python3 gov_tenders_scraper.py                    # Default: next 30 days, all categories
  python3 gov_tenders_scraper.py --days 14           # Next 14 days
  python3 gov_tenders_scraper.py --keyword "IT"      # Filter by keyword
  python3 gov_tenders_scraper.py --set-aside SBA     # Small business set-asides only
  python3 gov_tenders_scraper.py --naics 541512      # Specific NAICS code
  python3 gov_tenders_scraper.py --min-budget 50000  # Minimum budget $50K
"""

import csv
import json
import os
import sys
import time
import argparse
import re
from datetime import datetime, timedelta
from pathlib import Path
from urllib.parse import quote

try:
    import requests
except ImportError:
    print("ERROR: requests not installed. Run: pip3 install requests")
    sys.exit(1)

# ============================================================
# CONFIGURATION
# ============================================================

SCRIPT_DIR = Path(__file__).parent
PROJECT_DIR = SCRIPT_DIR.parent
OUTPUT_DIR = SCRIPT_DIR / "leads"
OUTPUT_FILE = OUTPUT_DIR / "gov_tenders_active.csv"

# SAM.gov public API - no key required for basic search
# Docs: https://open.gsa.gov/api/get-opportunities-public-api/
SAM_GOV_API_BASE = "https://api.sam.gov/opportunities/v2/search"

# SAM.gov API key (free, register at sam.gov)
# If you don't have one, the script uses the public endpoint with rate limits
SAM_GOV_API_KEY = os.environ.get("SAM_GOV_API_KEY", "")

# USAspending.gov API - completely free, no key needed
USASPENDING_API_BASE = "https://api.usaspending.gov/api/v2"

# Set-aside type mapping
SET_ASIDE_CODES = {
    "SBA": "Total Small Business Set-Aside",
    "SBP": "Partial Small Business Set-Aside",
    "8A": "8(a) Set-Aside",
    "8AN": "8(a) Sole Source",
    "HZC": "HUBZone Set-Aside",
    "HZS": "HUBZone Sole Source",
    "SDVOSBC": "Service-Disabled Veteran-Owned Small Business Set-Aside",
    "SDVOSBS": "Service-Disabled Veteran-Owned Small Business Sole Source",
    "WOSB": "Women-Owned Small Business",
    "WOSBSS": "Women-Owned Small Business Sole Source",
    "EDWOSB": "Economically Disadvantaged Women-Owned Small Business",
    "EDWOSBSS": "Economically Disadvantaged WOSB Sole Source",
    "LAS": "Local Area Set-Aside",
    "IEE": "Indian Economic Enterprise",
    "ISBEE": "Indian Small Business Economic Enterprise",
    "BICiv": "Buy Indian Civilian",
    "VSA": "Veteran-Owned Small Business Set-Aside",
    "VSS": "Veteran-Owned Small Business Sole Source",
}

# Notice types
NOTICE_TYPES = {
    "o": "Solicitation",
    "p": "Presolicitation",
    "k": "Combined Synopsis/Solicitation",
    "r": "Sources Sought",
    "s": "Special Notice",
    "g": "Sale of Surplus Property",
    "i": "Intent to Bundle",
    "a": "Award Notice",
}

CSV_HEADERS = [
    "opportunity_id",
    "title",
    "agency",
    "sub_agency",
    "category",
    "notice_type",
    "budget_low",
    "budget_high",
    "award_amount",
    "deadline",
    "posted_date",
    "description",
    "location",
    "naics_code",
    "naics_description",
    "set_aside_type",
    "set_aside_description",
    "classification_code",
    "url",
    "contact_name",
    "contact_email",
    "contact_phone",
    "source",
    "scraped_at",
]


# ============================================================
# SAM.GOV SCRAPER (PRIMARY)
# ============================================================

def scrape_sam_gov(days=30, keyword=None, set_aside=None, naics=None, min_budget=0, limit=1000):
    """
    Scrape opportunities from SAM.gov public API.

    SAM.gov is THE official US government procurement portal.
    $500B+ in federal spending flows through here every year.
    API is free. Most people don't know it exists.
    """
    print("\n[SAM.gov] Scraping federal contract opportunities...")

    today = datetime.now()
    deadline_start = today.strftime("%m/%d/%Y")
    deadline_end = (today + timedelta(days=days)).strftime("%m/%d/%Y")

    opportunities = []
    offset = 0
    page_size = 100  # Max per request
    total_fetched = 0

    while total_fetched < limit:
        params = {
            "postedFrom": (today - timedelta(days=365)).strftime("%m/%d/%Y"),
            "postedTo": today.strftime("%m/%d/%Y"),
            "rdlfrom": deadline_start,
            "rdlto": deadline_end,
            "limit": min(page_size, limit - total_fetched),
            "offset": offset,
            "ptype": "o,k,p,r",  # Solicitations, Combined, Presolicitations, Sources Sought
        }

        if SAM_GOV_API_KEY:
            params["api_key"] = SAM_GOV_API_KEY

        if keyword:
            params["title"] = keyword

        if set_aside:
            params["typeOfSetAside"] = set_aside

        if naics:
            params["ncode"] = naics

        headers = {
            "User-Agent": "PRINTMAXX-GovTenderScraper/1.0 (research tool)",
            "Accept": "application/json",
        }

        try:
            print(f"  Fetching page {offset // page_size + 1} (offset {offset})...")
            resp = requests.get(SAM_GOV_API_BASE, params=params, headers=headers, timeout=30)

            if resp.status_code == 429:
                print("  Rate limited. Waiting 60s...")
                time.sleep(60)
                continue

            if resp.status_code != 200:
                print(f"  API returned {resp.status_code}: {resp.text[:200]}")
                break

            data = resp.json()

            if "opportunitiesData" not in data:
                # Try alternate response structure
                if isinstance(data, list):
                    results = data
                else:
                    print(f"  Unexpected response structure: {list(data.keys())[:5]}")
                    break
            else:
                results = data.get("opportunitiesData", [])

            if not results:
                print(f"  No more results at offset {offset}")
                break

            total_count = data.get("totalRecords", len(results))
            print(f"  Got {len(results)} results (total available: {total_count})")

            for opp in results:
                try:
                    parsed = parse_sam_opportunity(opp, min_budget)
                    if parsed:
                        opportunities.append(parsed)
                except Exception as e:
                    print(f"  Error parsing opportunity: {e}")
                    continue

            total_fetched += len(results)
            offset += page_size

            if total_fetched >= total_count:
                break

            # Rate limit courtesy
            time.sleep(1)

        except requests.exceptions.Timeout:
            print("  Request timed out. Retrying...")
            time.sleep(5)
            continue
        except requests.exceptions.ConnectionError as e:
            print(f"  Connection error: {e}")
            break
        except json.JSONDecodeError:
            print(f"  Invalid JSON response. Status: {resp.status_code}")
            print(f"  Response preview: {resp.text[:300]}")
            break
        except Exception as e:
            print(f"  Unexpected error: {e}")
            break

    print(f"[SAM.gov] Total opportunities scraped: {len(opportunities)}")
    return opportunities


def parse_sam_opportunity(opp, min_budget=0):
    """Parse a single SAM.gov opportunity into our standard format."""

    # Extract budget/award info
    award = opp.get("award", {}) or {}
    budget_low = ""
    budget_high = ""
    award_amount = ""

    if isinstance(award, dict):
        award_amount = award.get("amount", "")
        if award_amount and min_budget and float(str(award_amount).replace(",", "").replace("$", "")) < min_budget:
            return None

    # Extract description (may be in different fields)
    description = opp.get("description", "") or ""
    if not description:
        description = opp.get("organizationType", "") or ""

    # Truncate long descriptions for CSV
    if len(description) > 500:
        description = description[:497] + "..."

    # Clean HTML from description
    description = re.sub(r'<[^>]+>', ' ', description)
    description = re.sub(r'\s+', ' ', description).strip()

    # Extract point of contact
    poc = opp.get("pointOfContact", []) or []
    contact_name = ""
    contact_email = ""
    contact_phone = ""
    if poc and isinstance(poc, list) and len(poc) > 0:
        primary = poc[0] if isinstance(poc[0], dict) else {}
        contact_name = primary.get("fullName", "") or f"{primary.get('firstName', '')} {primary.get('lastName', '')}".strip()
        contact_email = primary.get("email", "")
        contact_phone = primary.get("phone", "")

    # Build opportunity URL
    opp_id = opp.get("noticeId", "") or opp.get("solicitationNumber", "")
    url = f"https://sam.gov/opp/{opp.get('noticeId', '')}/view" if opp.get("noticeId") else ""

    # Set-aside info
    set_aside_code = opp.get("typeOfSetAsideDescription", "") or opp.get("typeOfSetAside", "")
    set_aside_desc = SET_ASIDE_CODES.get(set_aside_code, set_aside_code)

    # Notice type
    notice_type_code = opp.get("type", "") or ""
    notice_type = NOTICE_TYPES.get(notice_type_code, notice_type_code)

    # NAICS
    naics_code = opp.get("naicsCode", "")
    naics_desc = opp.get("naicsSolicitationDescription", "") or opp.get("classificationCode", "")

    # Location
    place = opp.get("placeOfPerformance", {}) or {}
    location_parts = []
    if isinstance(place, dict):
        city = place.get("city", {})
        if isinstance(city, dict):
            location_parts.append(city.get("name", ""))
        elif isinstance(city, str):
            location_parts.append(city)
        state = place.get("state", {})
        if isinstance(state, dict):
            location_parts.append(state.get("name", "") or state.get("code", ""))
        elif isinstance(state, str):
            location_parts.append(state)
        country = place.get("country", {})
        if isinstance(country, dict):
            location_parts.append(country.get("name", "") or country.get("code", ""))
    location = ", ".join([p for p in location_parts if p])

    if not location:
        office = opp.get("officeAddress", {}) or {}
        if isinstance(office, dict):
            location = f"{office.get('city', '')}, {office.get('state', '')}".strip(", ")

    return {
        "opportunity_id": opp_id,
        "title": (opp.get("title", "") or "").strip(),
        "agency": (opp.get("fullParentPathName", "") or opp.get("departmentName", "") or "").strip(),
        "sub_agency": (opp.get("subtierAgency", "") or opp.get("office", "") or "").strip(),
        "category": (opp.get("classificationCode", "") or ""),
        "notice_type": notice_type,
        "budget_low": budget_low,
        "budget_high": budget_high,
        "award_amount": award_amount,
        "deadline": (opp.get("responseDeadLine", "") or opp.get("archiveDate", "") or ""),
        "posted_date": (opp.get("postedDate", "") or ""),
        "description": description,
        "location": location,
        "naics_code": naics_code,
        "naics_description": naics_desc,
        "set_aside_type": set_aside_code,
        "set_aside_description": set_aside_desc,
        "classification_code": opp.get("classificationCode", ""),
        "url": url,
        "contact_name": contact_name,
        "contact_email": contact_email,
        "contact_phone": contact_phone,
        "source": "SAM.gov",
        "scraped_at": datetime.now().isoformat(),
    }


# ============================================================
# USASPENDING.GOV SCRAPER (SECONDARY - AWARDS DATA)
# ============================================================

def scrape_usaspending(days=30, keyword=None, limit=200):
    """
    Scrape from USAspending.gov API.

    This gives us AWARDED contracts (not opportunities) which is useful for:
    - Understanding what agencies are spending on
    - Finding agencies that regularly award in specific categories
    - Identifying subcontracting opportunities
    """
    print("\n[USAspending.gov] Scraping recent federal awards...")

    today = datetime.now()
    start_date = (today - timedelta(days=90)).strftime("%Y-%m-%d")
    end_date = today.strftime("%Y-%m-%d")

    opportunities = []
    page = 1

    payload = {
        "filters": {
            "time_period": [
                {
                    "start_date": start_date,
                    "end_date": end_date,
                }
            ],
            "award_type_codes": ["A", "B", "C", "D"],  # Contracts only
        },
        "fields": [
            "Award ID",
            "Recipient Name",
            "Award Amount",
            "Total Obligation",
            "Description",
            "Start Date",
            "End Date",
            "Awarding Agency",
            "Awarding Sub Agency",
            "Award Type",
            "recipient_id",
            "Place of Performance State Code",
            "Place of Performance City Name",
            "NAICS Code",
            "NAICS Description",
            "PSC Code",
            "PSC Description",
        ],
        "page": page,
        "limit": min(limit, 100),
        "sort": "Award Amount",
        "order": "desc",
    }

    if keyword:
        payload["filters"]["keywords"] = [keyword]

    headers = {
        "Content-Type": "application/json",
        "User-Agent": "PRINTMAXX-GovTenderScraper/1.0",
    }

    try:
        url = f"{USASPENDING_API_BASE}/search/spending_by_award/"
        print(f"  Fetching awards data...")
        resp = requests.post(url, json=payload, headers=headers, timeout=30)

        if resp.status_code != 200:
            print(f"  API returned {resp.status_code}: {resp.text[:200]}")
            return []

        data = resp.json()
        results = data.get("results", [])
        total = data.get("page_metadata", {}).get("total", 0)

        print(f"  Got {len(results)} awards (total available: {total})")

        for award in results:
            try:
                parsed = parse_usaspending_award(award)
                if parsed:
                    opportunities.append(parsed)
            except Exception as e:
                print(f"  Error parsing award: {e}")
                continue

    except Exception as e:
        print(f"  Error fetching USAspending data: {e}")

    print(f"[USAspending.gov] Total awards scraped: {len(opportunities)}")
    return opportunities


def parse_usaspending_award(award):
    """Parse a USAspending award into our standard format."""

    description = (award.get("Description", "") or "")[:500]
    description = re.sub(r'<[^>]+>', ' ', description)
    description = re.sub(r'\s+', ' ', description).strip()

    amount = award.get("Award Amount", 0) or award.get("Total Obligation", 0)

    location_parts = []
    city = award.get("Place of Performance City Name", "")
    state = award.get("Place of Performance State Code", "")
    if city:
        location_parts.append(city)
    if state:
        location_parts.append(state)
    location = ", ".join(location_parts)

    return {
        "opportunity_id": award.get("Award ID", ""),
        "title": f"[AWARDED] {description[:100]}..." if len(description) > 100 else f"[AWARDED] {description}",
        "agency": award.get("Awarding Agency", ""),
        "sub_agency": award.get("Awarding Sub Agency", ""),
        "category": award.get("PSC Code", ""),
        "notice_type": f"Award - {award.get('Award Type', '')}",
        "budget_low": "",
        "budget_high": "",
        "award_amount": amount,
        "deadline": award.get("End Date", ""),
        "posted_date": award.get("Start Date", ""),
        "description": description,
        "location": location,
        "naics_code": award.get("NAICS Code", ""),
        "naics_description": award.get("NAICS Description", "") or award.get("PSC Description", ""),
        "set_aside_type": "",
        "set_aside_description": "",
        "classification_code": award.get("PSC Code", ""),
        "url": f"https://www.usaspending.gov/award/{award.get('internal_id', '')}" if award.get('internal_id') else "",
        "contact_name": "",
        "contact_email": "",
        "contact_phone": "",
        "source": "USAspending.gov",
        "scraped_at": datetime.now().isoformat(),
    }


# ============================================================
# GRANTS.GOV SCRAPER (FREE, NO KEY, WORKING)
# ============================================================

def scrape_grants_gov(days=30, keyword=None, limit=200):
    """
    Scrape open grant and contract opportunities from Grants.gov.

    Grants.gov is free, no API key, and has real open opportunities.
    This is federal grant funding - agencies giving money to orgs.
    """
    print("\n[Grants.gov] Scraping open federal opportunities...")

    url = "https://apply07.grants.gov/grantsws/rest/opportunities/search"
    opportunities = []
    start_record = 0
    page_size = 25  # Max per request

    while start_record < limit:
        payload = {
            "oppStatuses": "posted",
            "sortBy": "openDate|desc",
            "rows": min(page_size, limit - start_record),
            "startRecord": start_record,
        }

        if keyword:
            payload["keyword"] = keyword

        headers = {
            "Content-Type": "application/json",
            "User-Agent": "PRINTMAXX-GovTenderScraper/1.0",
        }

        try:
            print(f"  Fetching page {start_record // page_size + 1} (offset {start_record})...")
            resp = requests.post(url, json=payload, headers=headers, timeout=30)

            if resp.status_code != 200:
                print(f"  API returned {resp.status_code}: {resp.text[:200]}")
                break

            data = resp.json()
            results = data.get("oppHits", [])
            total = data.get("hitCount", 0)

            if not results:
                break

            print(f"  Got {len(results)} opportunities (total available: {total})")

            for opp in results:
                try:
                    parsed = parse_grants_gov_opportunity(opp, days)
                    if parsed:
                        opportunities.append(parsed)
                except Exception as e:
                    print(f"  Error parsing grant: {e}")
                    continue

            start_record += len(results)

            if start_record >= total:
                break

            time.sleep(0.5)

        except Exception as e:
            print(f"  Error: {e}")
            break

    print(f"[Grants.gov] Total opportunities scraped: {len(opportunities)}")
    return opportunities


def parse_grants_gov_opportunity(opp, days=30):
    """Parse a Grants.gov opportunity."""

    close_date_str = opp.get("closeDate", "")
    open_date_str = opp.get("openDate", "")

    # Filter by deadline within our window
    if close_date_str:
        try:
            close_date = datetime.strptime(close_date_str, "%m/%d/%Y")
            if close_date < datetime.now():
                return None  # Already closed
            if close_date > datetime.now() + timedelta(days=days):
                pass  # Still include - might be useful
        except ValueError:
            pass

    opp_number = opp.get("number", "")
    opp_id = opp.get("id", "")

    return {
        "opportunity_id": f"GRANTS-{opp_id}" if opp_id else opp_number,
        "title": opp.get("title", "").strip(),
        "agency": opp.get("agency", ""),
        "sub_agency": "",
        "category": opp.get("docType", ""),
        "notice_type": f"Grant - {opp.get('docType', 'synopsis')}",
        "budget_low": "",
        "budget_high": "",
        "award_amount": "",
        "deadline": close_date_str,
        "posted_date": open_date_str,
        "description": f"Opportunity {opp_number} - {opp.get('title', '')}",
        "location": "USA (Federal)",
        "naics_code": "",
        "naics_description": "",
        "set_aside_type": "",
        "set_aside_description": "",
        "classification_code": ", ".join(opp.get("cfdaList", [])),
        "url": f"https://www.grants.gov/search-results-detail/{opp_id}" if opp_id else "",
        "contact_name": "",
        "contact_email": "",
        "contact_phone": "",
        "source": "Grants.gov",
        "scraped_at": datetime.now().isoformat(),
    }


# ============================================================
# USASPENDING - SMALL BUSINESS IT CONTRACTS (TARGETED)
# ============================================================

def scrape_usaspending_it_smallbiz(days=90, limit=100):
    """
    Targeted USAspending query for IT/consulting contracts.
    NAICS codes: 541511-541519 (Computer Services), 541611-541690 (Consulting),
    518210 (Data Processing/Hosting), 541810-541910 (Marketing/PR).
    """
    print("\n[USAspending.gov] Scraping IT/consulting awards for market intel...")

    today = datetime.now()
    start_date = (today - timedelta(days=days)).strftime("%Y-%m-%d")
    end_date = today.strftime("%Y-%m-%d")

    url = f"{USASPENDING_API_BASE}/search/spending_by_award/"

    # IT and consulting NAICS codes
    naics_codes = [
        "541511", "541512", "541519",  # Computer services
        "541611", "541613", "541618", "541690",  # Management/consulting
        "518210",  # Data processing/hosting
        "541810", "541820", "541910",  # Marketing/PR
        "561110", "561210",  # Administrative/facilities
        "511210",  # Software publishers
        "517311", "517312",  # Telecommunications
    ]

    payload = {
        "filters": {
            "time_period": [{"start_date": start_date, "end_date": end_date}],
            "award_type_codes": ["A", "B", "C", "D"],
            "naics_codes": {"require": naics_codes},
        },
        "fields": [
            "Award ID", "Recipient Name", "Award Amount", "Total Obligation",
            "Description", "Start Date", "End Date", "Awarding Agency",
            "Awarding Sub Agency", "Award Type", "Place of Performance State Code",
            "Place of Performance City Name", "NAICS Code", "NAICS Description",
            "PSC Code", "PSC Description",
        ],
        "page": 1,
        "limit": min(limit, 100),
        "sort": "Award Amount",
        "order": "desc",
    }

    headers = {
        "Content-Type": "application/json",
        "User-Agent": "PRINTMAXX-GovTenderScraper/1.0",
    }

    opportunities = []

    try:
        resp = requests.post(url, json=payload, headers=headers, timeout=30)
        if resp.status_code == 200:
            data = resp.json()
            results = data.get("results", [])
            total = data.get("page_metadata", {}).get("total", 0)
            print(f"  Got {len(results)} IT/consulting awards (total: {total})")

            for award in results:
                try:
                    parsed = parse_usaspending_award(award)
                    if parsed:
                        parsed["title"] = parsed["title"].replace("[AWARDED]", "[IT/CONSULTING AWARD]")
                        opportunities.append(parsed)
                except Exception as e:
                    print(f"  Error: {e}")
        else:
            print(f"  API returned {resp.status_code}")

    except Exception as e:
        print(f"  Error: {e}")

    print(f"[USAspending.gov IT] Total IT/consulting awards: {len(opportunities)}")
    return opportunities


# ============================================================
# SAM.GOV ENTITY/CONTRACT SEARCH (BONUS - FIND CONTRACTORS)
# ============================================================

def search_sam_entities(keyword=None, naics=None, set_aside=None, limit=50):
    """
    Search SAM.gov for registered entities (contractors).
    Useful for finding small businesses to partner with or sell intel to.
    """
    print("\n[SAM.gov Entities] Searching registered contractors...")

    # This endpoint requires an API key
    if not SAM_GOV_API_KEY:
        print("  SAM.gov Entity Search requires API key. Set SAM_GOV_API_KEY env var.")
        print("  Register free at: https://sam.gov/content/entity-registration")
        return []

    url = "https://api.sam.gov/entity-information/v3/entities"
    params = {
        "api_key": SAM_GOV_API_KEY,
        "registrationStatus": "A",  # Active registrations
        "purposeOfRegistrationCode": "Z2",  # Federal contracts
        "includeSections": "entityRegistration,coreData",
        "page": 0,
        "size": min(limit, 100),
    }

    if keyword:
        params["q"] = keyword
    if naics:
        params["naicsCode"] = naics
    if set_aside:
        params["sbaBusinessTypeCode"] = set_aside

    try:
        resp = requests.get(url, params=params, timeout=30)
        if resp.status_code == 200:
            data = resp.json()
            entities = data.get("entityData", [])
            print(f"  Found {len(entities)} registered entities")
            return entities
        else:
            print(f"  Entity search returned {resp.status_code}")
            return []
    except Exception as e:
        print(f"  Error: {e}")
        return []


# ============================================================
# TENDERSINFO.COM SCRAPER (FALLBACK - WEB SCRAPING)
# ============================================================

def scrape_tendersinfo(keyword=None, country="USA", limit=50):
    """
    Attempt to scrape tendersinfo.com.
    This is a web scraper fallback - may break if they change their site.
    """
    print("\n[tendersinfo.com] Attempting web scrape (fallback)...")

    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Referer": "https://www.tendersinfo.com",
    }

    search_url = "https://www.tendersinfo.com/global-tenders.php"
    params = {}
    if keyword:
        params["keyword"] = keyword
    if country:
        params["country"] = country

    try:
        resp = requests.get(search_url, params=params, headers=headers, timeout=15)
        if resp.status_code == 200:
            # Basic parsing - tendersinfo uses dynamic content, this is best-effort
            print(f"  Got response ({len(resp.text)} bytes)")
            # If it returns HTML with tender data, parse it
            # This is a basic extractor - may need updating
            opportunities = parse_tendersinfo_html(resp.text)
            print(f"  Extracted {len(opportunities)} opportunities")
            return opportunities
        elif resp.status_code == 403:
            print("  Access blocked (403). tendersinfo.com requires browser/account.")
            print("  Use SAM.gov data instead (same opportunities, free API).")
            return []
        else:
            print(f"  HTTP {resp.status_code}")
            return []
    except Exception as e:
        print(f"  Error: {e}")
        return []


def parse_tendersinfo_html(html):
    """Basic HTML parser for tendersinfo.com results."""
    opportunities = []

    # Simple regex-based extraction (no beautifulsoup dependency)
    # Look for tender listing patterns
    tender_blocks = re.findall(
        r'<div[^>]*class="[^"]*tender[^"]*"[^>]*>(.*?)</div>',
        html, re.DOTALL | re.IGNORECASE
    )

    if not tender_blocks:
        # Try alternate patterns
        tender_blocks = re.findall(
            r'<tr[^>]*>(.*?)</tr>',
            html, re.DOTALL | re.IGNORECASE
        )

    for block in tender_blocks[:50]:
        # Extract what we can
        title_match = re.search(r'<a[^>]*>(.*?)</a>', block, re.DOTALL)
        title = re.sub(r'<[^>]+>', '', title_match.group(1)).strip() if title_match else ""

        if not title or len(title) < 10:
            continue

        url_match = re.search(r'href="([^"]+)"', block)
        url = url_match.group(1) if url_match else ""
        if url and not url.startswith("http"):
            url = f"https://www.tendersinfo.com{url}"

        opportunities.append({
            "opportunity_id": "",
            "title": title,
            "agency": "",
            "sub_agency": "",
            "category": "",
            "notice_type": "",
            "budget_low": "",
            "budget_high": "",
            "award_amount": "",
            "deadline": "",
            "posted_date": "",
            "description": "",
            "location": "USA",
            "naics_code": "",
            "naics_description": "",
            "set_aside_type": "",
            "set_aside_description": "",
            "classification_code": "",
            "url": url,
            "contact_name": "",
            "contact_email": "",
            "contact_phone": "",
            "source": "tendersinfo.com",
            "scraped_at": datetime.now().isoformat(),
        })

    return opportunities


# ============================================================
# OUTPUT & REPORTING
# ============================================================

def save_to_csv(opportunities, output_file):
    """Save opportunities to CSV."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Deduplicate by opportunity_id
    seen_ids = set()
    unique_opps = []
    for opp in opportunities:
        oid = opp.get("opportunity_id", "")
        if oid and oid in seen_ids:
            continue
        if oid:
            seen_ids.add(oid)
        unique_opps.append(opp)

    with open(output_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_HEADERS, extrasaction="ignore")
        writer.writeheader()
        for opp in unique_opps:
            writer.writerow(opp)

    print(f"\nSaved {len(unique_opps)} opportunities to {output_file}")
    return unique_opps


def print_summary(opportunities):
    """Print a summary of scraped opportunities."""
    if not opportunities:
        print("\nNo opportunities found.")
        return

    print("\n" + "=" * 70)
    print("GOVERNMENT CONTRACT OPPORTUNITIES SUMMARY")
    print("=" * 70)

    # Source breakdown
    sources = {}
    for opp in opportunities:
        src = opp.get("source", "Unknown")
        sources[src] = sources.get(src, 0) + 1

    print(f"\nTotal opportunities: {len(opportunities)}")
    for src, count in sorted(sources.items()):
        print(f"  {src}: {count}")

    # Set-aside breakdown
    set_asides = {}
    for opp in opportunities:
        sa = opp.get("set_aside_description", "") or opp.get("set_aside_type", "")
        if sa:
            set_asides[sa] = set_asides.get(sa, 0) + 1

    if set_asides:
        print(f"\nSet-aside types:")
        for sa, count in sorted(set_asides.items(), key=lambda x: -x[1])[:10]:
            print(f"  {sa}: {count}")

    # Agency breakdown
    agencies = {}
    for opp in opportunities:
        agency = opp.get("agency", "")
        if agency:
            # Shorten long agency paths
            short = agency.split(".")[-1].strip() if "." in agency else agency
            agencies[short] = agencies.get(short, 0) + 1

    if agencies:
        print(f"\nTop agencies:")
        for agency, count in sorted(agencies.items(), key=lambda x: -x[1])[:10]:
            print(f"  {agency}: {count}")

    # NAICS breakdown
    naics = {}
    for opp in opportunities:
        code = opp.get("naics_code", "")
        desc = opp.get("naics_description", "")
        if code:
            label = f"{code} - {desc}" if desc else code
            naics[label] = naics.get(label, 0) + 1

    if naics:
        print(f"\nTop NAICS codes:")
        for code, count in sorted(naics.items(), key=lambda x: -x[1])[:10]:
            print(f"  {code}: {count}")

    # Show top 10 by title
    print(f"\nTop 10 opportunities (by recency):")
    for i, opp in enumerate(opportunities[:10], 1):
        title = opp.get("title", "Untitled")[:80]
        agency = opp.get("agency", "")[:30]
        deadline = opp.get("deadline", "N/A")
        amount = opp.get("award_amount", "")
        set_aside = opp.get("set_aside_type", "")

        amount_str = f" | ${amount:,.0f}" if amount and isinstance(amount, (int, float)) else ""
        sa_str = f" | {set_aside}" if set_aside else ""

        print(f"\n  {i}. {title}")
        print(f"     Agency: {agency} | Deadline: {deadline}{amount_str}{sa_str}")


def print_top_opportunities(opportunities, n=5):
    """Print detailed view of top N opportunities for cold email drafting."""
    print(f"\n{'=' * 70}")
    print(f"TOP {n} OPPORTUNITIES - DETAILED VIEW")
    print(f"{'=' * 70}")

    # Sort by: has set-aside (small biz friendly) > has deadline > has contact info
    def score_opp(opp):
        s = 0
        if opp.get("set_aside_type"):
            s += 100
        if opp.get("deadline"):
            s += 50
        if opp.get("contact_email"):
            s += 25
        if opp.get("award_amount"):
            try:
                s += min(float(str(opp["award_amount"]).replace(",", "")), 1000000) / 10000
            except Exception:
                pass  # Non-numeric award_amount; skip bonus
        return s

    sorted_opps = sorted(opportunities, key=score_opp, reverse=True)

    for i, opp in enumerate(sorted_opps[:n], 1):
        print(f"\n{'─' * 60}")
        print(f"#{i}: {opp.get('title', 'Untitled')}")
        print(f"{'─' * 60}")
        print(f"  ID:         {opp.get('opportunity_id', 'N/A')}")
        print(f"  Agency:     {opp.get('agency', 'N/A')}")
        print(f"  Sub-Agency: {opp.get('sub_agency', 'N/A')}")
        print(f"  Type:       {opp.get('notice_type', 'N/A')}")
        print(f"  Deadline:   {opp.get('deadline', 'N/A')}")
        print(f"  Posted:     {opp.get('posted_date', 'N/A')}")
        print(f"  Location:   {opp.get('location', 'N/A')}")
        print(f"  NAICS:      {opp.get('naics_code', 'N/A')} - {opp.get('naics_description', 'N/A')}")
        print(f"  Set-Aside:  {opp.get('set_aside_description', 'None')}")
        print(f"  Amount:     {opp.get('award_amount', 'Not specified')}")
        print(f"  Contact:    {opp.get('contact_name', 'N/A')} | {opp.get('contact_email', 'N/A')} | {opp.get('contact_phone', 'N/A')}")
        print(f"  URL:        {opp.get('url', 'N/A')}")
        desc = opp.get('description', 'No description available')
        if desc:
            print(f"  Description: {desc[:300]}")

    return sorted_opps[:n]


# ============================================================
# MAIN
# ============================================================

def main():
    parser = argparse.ArgumentParser(
        description="Government Contract Opportunity Scraper - SAM.gov + USAspending.gov",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 gov_tenders_scraper.py                      # All opportunities, next 30 days
  python3 gov_tenders_scraper.py --keyword "IT"        # IT-related contracts
  python3 gov_tenders_scraper.py --set-aside SBA       # Small business only
  python3 gov_tenders_scraper.py --naics 541512        # Computer systems design
  python3 gov_tenders_scraper.py --naics 541511        # Custom computer programming
  python3 gov_tenders_scraper.py --days 14             # Closing in 14 days
  python3 gov_tenders_scraper.py --min-budget 100000   # $100K+ contracts
  python3 gov_tenders_scraper.py --include-awards      # Also pull recent awards
  python3 gov_tenders_scraper.py --try-tendersinfo     # Try tendersinfo.com too

Set SAM_GOV_API_KEY env var for higher rate limits (free registration at sam.gov).
        """,
    )

    parser.add_argument("--days", type=int, default=30, help="Look ahead N days for deadlines (default: 30)")
    parser.add_argument("--keyword", type=str, default=None, help="Filter by keyword in title")
    parser.add_argument("--set-aside", type=str, default=None, help="Filter by set-aside type (SBA, 8A, HZC, SDVOSBC, WOSB, EDWOSB)")
    parser.add_argument("--naics", type=str, default=None, help="Filter by NAICS code")
    parser.add_argument("--min-budget", type=float, default=0, help="Minimum contract value")
    parser.add_argument("--limit", type=int, default=500, help="Max opportunities to fetch (default: 500)")
    parser.add_argument("--include-awards", action="store_true", help="Include recent awards from USAspending.gov")
    parser.add_argument("--try-tendersinfo", action="store_true", help="Also try tendersinfo.com (may be blocked)")
    parser.add_argument("--include-grants", action="store_true", help="Include Grants.gov federal grant opportunities")
    parser.add_argument("--include-it", action="store_true", help="Include IT/consulting awards from USAspending")
    parser.add_argument("--all-sources", action="store_true", help="Pull from ALL available sources")
    parser.add_argument("--output", type=str, default=None, help="Custom output file path")
    parser.add_argument("--top", type=int, default=5, help="Number of top opportunities to detail (default: 5)")

    args = parser.parse_args()

    output_file = Path(args.output) if args.output else OUTPUT_FILE

    print("=" * 70)
    print("GOVERNMENT CONTRACT OPPORTUNITY SCRAPER")
    print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Parameters: days={args.days}, keyword={args.keyword}, set_aside={args.set_aside}")
    print(f"            naics={args.naics}, min_budget=${args.min_budget:,.0f}, limit={args.limit}")
    print(f"Output: {output_file}")
    print("=" * 70)

    all_opportunities = []

    # 1. SAM.gov (primary - always run)
    sam_opps = scrape_sam_gov(
        days=args.days,
        keyword=args.keyword,
        set_aside=args.set_aside,
        naics=args.naics,
        min_budget=args.min_budget,
        limit=args.limit,
    )
    all_opportunities.extend(sam_opps)

    # 2. USAspending.gov (secondary - recent awards for intel)
    if args.include_awards or args.all_sources:
        usa_opps = scrape_usaspending(
            days=args.days,
            keyword=args.keyword,
            limit=min(args.limit, 200),
        )
        all_opportunities.extend(usa_opps)

    # 3. Grants.gov (federal grants - free, no key)
    if args.include_grants or args.all_sources:
        grants_opps = scrape_grants_gov(
            days=args.days,
            keyword=args.keyword,
            limit=min(args.limit, 200),
        )
        all_opportunities.extend(grants_opps)

    # 4. USAspending IT/consulting targeted
    if args.include_it or args.all_sources:
        it_opps = scrape_usaspending_it_smallbiz(
            days=90,
            limit=min(args.limit, 100),
        )
        all_opportunities.extend(it_opps)

    # 5. tendersinfo.com (fallback)
    if args.try_tendersinfo or args.all_sources:
        tender_opps = scrape_tendersinfo(
            keyword=args.keyword,
        )
        all_opportunities.extend(tender_opps)

    # Save results
    unique_opps = save_to_csv(all_opportunities, output_file)

    # --- Feed high-value findings into ALPHA_STAGING for Capital Genesis scoring ---
    if unique_opps:
        try:
            sys.path.insert(0, str(SCRIPT_DIR))
            from _alpha_staging_writer import stage_findings_batch
            findings = []
            for opp in unique_opps[:30]:
                title = opp.get("title", "")[:150]
                agency = opp.get("agency", "")[:50]
                set_aside = opp.get("set_aside_description", "") or opp.get("set_aside_type", "")
                deadline = opp.get("deadline", "N/A")
                naics = opp.get("naics_code", "")
                findings.append({
                    "content": (
                        f"Gov tender: {title} | Agency: {agency} | "
                        f"Set-aside: {set_aside or 'Full & Open'} | Deadline: {deadline} | "
                        f"NAICS: {naics or 'N/A'}"
                    ),
                    "source": "gov_tenders_scraper",
                    "source_url": opp.get("url", ""),
                    "category": "BROKERING",
                    "roi_potential": "HIGH" if set_aside else "MEDIUM",
                    "applicable_methods": "GOV_CONTRACTS",
                    "reviewer_notes": f"Auto-staged from gov_tenders_scraper.",
                })
            if findings:
                staged = stage_findings_batch(findings)
                print(f"\n  Staged {staged} gov tenders to ALPHA_STAGING.csv")
        except ImportError:
            pass

    # Print summary
    print_summary(unique_opps)

    # Print top opportunities
    top = print_top_opportunities(unique_opps, n=args.top)

    # Stats
    print(f"\n{'=' * 70}")
    print("ACTIONABLE INTELLIGENCE")
    print(f"{'=' * 70}")

    small_biz = [o for o in unique_opps if o.get("set_aside_type")]
    print(f"\nSmall business set-asides: {len(small_biz)} ({len(small_biz)*100//max(len(unique_opps),1)}% of total)")

    with_contacts = [o for o in unique_opps if o.get("contact_email")]
    print(f"Opportunities with contact emails: {len(with_contacts)}")

    print(f"\nFiles saved:")
    print(f"  {output_file}")
    print(f"\nNext steps:")
    print(f"  1. Review top {args.top} opportunities above")
    print(f"  2. Cross-reference NAICS codes with your capabilities")
    print(f"  3. Draft capability statements for matching set-asides")
    print(f"  4. Cold email small businesses in matching NAICS codes")
    print(f"  5. Register at SAM.gov if not already (free)")

    return unique_opps


if __name__ == "__main__":
    main()
