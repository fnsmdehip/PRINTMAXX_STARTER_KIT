#!/usr/bin/env python3
"""
PRINTMAXX Lead Enrichment Script
==================================
Takes a CSV of company names or domains and enriches with company and contact data
using free APIs (Hunter.io, Apollo.io free tier, Clearbit free).

Usage:
    python3 enrich_leads.py input.csv                    # Enrich from file
    python3 enrich_leads.py input.csv --output enriched.csv
    python3 enrich_leads.py input.csv --api hunter       # Use specific API
    python3 enrich_leads.py input.csv --rate-limit 2     # 2 seconds between requests

Environment Variables:
    HUNTER_API_KEY    - Hunter.io API key (50 free requests/month)
    APOLLO_API_KEY    - Apollo.io API key (free tier)
    CLEARBIT_API_KEY  - Clearbit API key (free tier, deprecated but may work)

Output columns:
    company_name, domain, industry, company_size, decision_maker_name,
    decision_maker_email, decision_maker_title, linkedin_url, source, enriched_at
"""

import csv
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime
from pathlib import Path
from typing import Optional

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
OUTREACH_PIPELINE = PROJECT_ROOT / "LEDGER" / "OUTREACH_PIPELINE.csv"

# API keys from environment
HUNTER_API_KEY = os.environ.get("HUNTER_API_KEY", "")
APOLLO_API_KEY = os.environ.get("APOLLO_API_KEY", "")
CLEARBIT_API_KEY = os.environ.get("CLEARBIT_API_KEY", "")

# Rate limiting
DEFAULT_RATE_LIMIT = 2  # seconds between API calls
MAX_RETRIES = 3
RETRY_DELAY = 5  # seconds


def log(msg: str) -> None:
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{ts}] {msg}")


def make_request(url: str, headers: Optional[dict] = None, retries: int = MAX_RETRIES) -> Optional[dict]:
    """Make HTTP request with retry logic."""
    if headers is None:
        headers = {}
    headers["User-Agent"] = "PRINTMAXX-Lead-Enrichment/1.0"

    req = urllib.request.Request(url, headers=headers)

    for attempt in range(retries):
        try:
            with urllib.request.urlopen(req, timeout=15) as response:
                if response.status == 200:
                    return json.loads(response.read().decode("utf-8"))
                elif response.status == 429:
                    log(f"Rate limited. Waiting {RETRY_DELAY * (attempt + 1)}s...")
                    time.sleep(RETRY_DELAY * (attempt + 1))
                    continue
                else:
                    log(f"HTTP {response.status} for {url}")
                    return None
        except urllib.error.HTTPError as e:
            if e.code == 429:
                log(f"Rate limited (429). Waiting {RETRY_DELAY * (attempt + 1)}s...")
                time.sleep(RETRY_DELAY * (attempt + 1))
                continue
            elif e.code in (401, 403):
                log(f"Auth error ({e.code}). Check API key.")
                return None
            elif e.code == 404:
                return None
            else:
                log(f"HTTP error {e.code} for {url}")
                if attempt < retries - 1:
                    time.sleep(RETRY_DELAY)
                continue
        except urllib.error.URLError as e:
            log(f"Network error: {e.reason}")
            if attempt < retries - 1:
                time.sleep(RETRY_DELAY)
            continue
        except Exception as e:
            log(f"Request error: {e}")
            if attempt < retries - 1:
                time.sleep(RETRY_DELAY)
            continue

    return None


def normalize_domain(domain_or_company: str) -> str:
    """Extract or guess domain from input."""
    text = domain_or_company.strip().lower()

    # Already a domain
    if "." in text and " " not in text:
        # Strip protocol
        text = text.replace("https://", "").replace("http://", "").replace("www.", "")
        return text.split("/")[0]

    # Company name -> guess domain
    clean = text.replace(" ", "").replace(",", "").replace(".", "").replace("inc", "").replace("llc", "")
    return f"{clean}.com"


def enrich_with_hunter(domain: str) -> dict:
    """Enrich using Hunter.io API."""
    result = {
        "company_name": "",
        "domain": domain,
        "industry": "",
        "company_size": "",
        "decision_maker_name": "",
        "decision_maker_email": "",
        "decision_maker_title": "",
        "linkedin_url": "",
        "source": "hunter.io",
    }

    if not HUNTER_API_KEY:
        log("HUNTER_API_KEY not set. Skipping Hunter enrichment.")
        return result

    # Domain search - find emails at company
    url = f"https://api.hunter.io/v2/domain-search?domain={domain}&api_key={HUNTER_API_KEY}&limit=5"
    data = make_request(url)

    if data and "data" in data:
        d = data["data"]
        result["company_name"] = d.get("organization", "")
        result["industry"] = d.get("industry", "")
        result["company_size"] = str(d.get("company_size", ""))

        # Get first decision maker (prefer C-level, VP, Director)
        emails = d.get("emails", [])
        priority_titles = ["ceo", "cto", "coo", "founder", "owner", "vp", "director", "head"]

        best_contact = None
        for email_entry in emails:
            title = (email_entry.get("position") or "").lower()
            if any(pt in title for pt in priority_titles):
                best_contact = email_entry
                break

        if not best_contact and emails:
            best_contact = emails[0]

        if best_contact:
            first = best_contact.get("first_name", "")
            last = best_contact.get("last_name", "")
            result["decision_maker_name"] = f"{first} {last}".strip()
            result["decision_maker_email"] = best_contact.get("value", "")
            result["decision_maker_title"] = best_contact.get("position", "")
            result["linkedin_url"] = best_contact.get("linkedin", "")

    return result


def enrich_with_apollo(domain: str) -> dict:
    """Enrich using Apollo.io API."""
    result = {
        "company_name": "",
        "domain": domain,
        "industry": "",
        "company_size": "",
        "decision_maker_name": "",
        "decision_maker_email": "",
        "decision_maker_title": "",
        "linkedin_url": "",
        "source": "apollo.io",
    }

    if not APOLLO_API_KEY:
        log("APOLLO_API_KEY not set. Skipping Apollo enrichment.")
        return result

    # Organization enrichment
    url = "https://api.apollo.io/v1/organizations/enrich"
    params = urllib.parse.urlencode({"api_key": APOLLO_API_KEY, "domain": domain})
    data = make_request(f"{url}?{params}")

    if data and "organization" in data:
        org = data["organization"]
        result["company_name"] = org.get("name", "")
        result["industry"] = org.get("industry", "")

        # Apollo uses ranges for employee count
        emp_range = org.get("estimated_num_employees")
        if emp_range:
            result["company_size"] = str(emp_range)

    # People search at company
    people_url = "https://api.apollo.io/v1/mixed_people/search"
    people_params = urllib.parse.urlencode({
        "api_key": APOLLO_API_KEY,
        "q_organization_domains": domain,
        "per_page": 5,
        "person_seniorities[]": "c_suite,founder,owner,vp,director",
    })
    people_data = make_request(f"{people_url}?{people_params}")

    if people_data and "people" in people_data:
        people = people_data["people"]
        if people:
            person = people[0]
            result["decision_maker_name"] = person.get("name", "")
            result["decision_maker_email"] = person.get("email", "")
            result["decision_maker_title"] = person.get("title", "")
            result["linkedin_url"] = person.get("linkedin_url", "")

    return result


def enrich_with_clearbit(domain: str) -> dict:
    """Enrich using Clearbit API (free tier)."""
    result = {
        "company_name": "",
        "domain": domain,
        "industry": "",
        "company_size": "",
        "decision_maker_name": "",
        "decision_maker_email": "",
        "decision_maker_title": "",
        "linkedin_url": "",
        "source": "clearbit",
    }

    if not CLEARBIT_API_KEY:
        log("CLEARBIT_API_KEY not set. Skipping Clearbit enrichment.")
        return result

    # Company enrichment
    url = f"https://company.clearbit.com/v2/companies/find?domain={domain}"
    headers = {"Authorization": f"Bearer {CLEARBIT_API_KEY}"}
    data = make_request(url, headers=headers)

    if data:
        result["company_name"] = data.get("name", "")
        result["industry"] = data.get("category", {}).get("industry", "")
        metrics = data.get("metrics", {})
        if metrics:
            emp_range = metrics.get("employeesRange", "")
            result["company_size"] = emp_range if emp_range else str(metrics.get("employees", ""))

    return result


def merge_results(*results: dict) -> dict:
    """Merge enrichment results, preferring non-empty values from earlier sources."""
    merged = {
        "company_name": "",
        "domain": "",
        "industry": "",
        "company_size": "",
        "decision_maker_name": "",
        "decision_maker_email": "",
        "decision_maker_title": "",
        "linkedin_url": "",
        "source": "",
    }

    sources = []
    for result in results:
        for key, value in result.items():
            if key == "source":
                if value:
                    sources.append(value)
                continue
            if value and not merged[key]:
                merged[key] = value

    merged["source"] = " + ".join(sources) if sources else "none"
    return merged


def read_input_csv(filepath: Path) -> list:
    """Read input CSV. Accepts columns: company, domain, name, url, or company_name."""
    rows = []
    with open(filepath, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Try to find domain or company name
            domain = ""
            company = ""
            for key in row:
                k = key.lower().strip()
                if k in ("domain", "url", "website"):
                    domain = row[key].strip()
                elif k in ("company", "company_name", "name", "organization"):
                    company = row[key].strip()

            if domain:
                rows.append({"domain": normalize_domain(domain), "company_input": company or domain})
            elif company:
                rows.append({"domain": normalize_domain(company), "company_input": company})
    return rows


def write_output_csv(results: list, output_path: Path) -> None:
    """Write enriched results to CSV."""
    fieldnames = [
        "company_name", "domain", "industry", "company_size",
        "decision_maker_name", "decision_maker_email", "decision_maker_title",
        "linkedin_url", "source", "enriched_at",
    ]

    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)

    log(f"Output written to {output_path} ({len(results)} rows)")


def main():
    import argparse

    parser = argparse.ArgumentParser(description="PRINTMAXX Lead Enrichment")
    parser.add_argument("input", help="Input CSV file with company names or domains")
    parser.add_argument("--output", default=None, help="Output CSV file path")
    parser.add_argument("--api", choices=["hunter", "apollo", "clearbit", "all"], default="all",
                        help="Which API to use (default: all)")
    parser.add_argument("--rate-limit", type=float, default=DEFAULT_RATE_LIMIT,
                        help=f"Seconds between API calls (default: {DEFAULT_RATE_LIMIT})")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be processed")
    args = parser.parse_args()

    log("PRINTMAXX Lead Enrichment starting")

    input_path = Path(args.input)
    if not input_path.exists():
        log(f"Input file not found: {input_path}")
        sys.exit(1)

    output_path = Path(args.output) if args.output else input_path.with_name(
        input_path.stem + "_enriched.csv"
    )

    # Read input
    leads = read_input_csv(input_path)
    log(f"Loaded {len(leads)} leads from {input_path}")

    if not leads:
        log("No leads to process.")
        sys.exit(1)

    if args.dry_run:
        log("Dry run. Domains to enrich:")
        for lead in leads:
            log(f"  {lead['company_input']} -> {lead['domain']}")
        return

    # Check API keys
    apis_available = []
    if args.api in ("hunter", "all") and HUNTER_API_KEY:
        apis_available.append("hunter")
    if args.api in ("apollo", "all") and APOLLO_API_KEY:
        apis_available.append("apollo")
    if args.api in ("clearbit", "all") and CLEARBIT_API_KEY:
        apis_available.append("clearbit")

    if not apis_available:
        log("WARNING: No API keys configured. Set HUNTER_API_KEY, APOLLO_API_KEY, or CLEARBIT_API_KEY.")
        log("Running in demo mode - will output template with domains only.")

    log(f"Active APIs: {apis_available if apis_available else 'NONE (demo mode)'}")

    # Process each lead
    results = []
    for i, lead in enumerate(leads):
        domain = lead["domain"]
        log(f"[{i+1}/{len(leads)}] Enriching: {domain}")

        enrichments = []

        if "hunter" in apis_available:
            enrichments.append(enrich_with_hunter(domain))
            time.sleep(args.rate_limit)

        if "apollo" in apis_available:
            enrichments.append(enrich_with_apollo(domain))
            time.sleep(args.rate_limit)

        if "clearbit" in apis_available:
            enrichments.append(enrich_with_clearbit(domain))
            time.sleep(args.rate_limit)

        if enrichments:
            merged = merge_results(*enrichments)
        else:
            # Demo mode: output domain only
            merged = {
                "company_name": lead["company_input"],
                "domain": domain,
                "industry": "",
                "company_size": "",
                "decision_maker_name": "",
                "decision_maker_email": "",
                "decision_maker_title": "",
                "linkedin_url": "",
                "source": "input_only",
            }

        merged["enriched_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Use original company name if enrichment didn't find one
        if not merged["company_name"]:
            merged["company_name"] = lead["company_input"]

        results.append(merged)

    # Write output
    write_output_csv(results, output_path)

    # Summary stats
    with_email = sum(1 for r in results if r["decision_maker_email"])
    with_linkedin = sum(1 for r in results if r["linkedin_url"])
    with_industry = sum(1 for r in results if r["industry"])

    log("--- ENRICHMENT SUMMARY ---")
    log(f"Total leads: {len(results)}")
    log(f"With email: {with_email} ({100*with_email//max(len(results),1)}%)")
    log(f"With LinkedIn: {with_linkedin} ({100*with_linkedin//max(len(results),1)}%)")
    log(f"With industry: {with_industry} ({100*with_industry//max(len(results),1)}%)")
    log(f"Output: {output_path}")
    log("Done.")


if __name__ == "__main__":
    main()
