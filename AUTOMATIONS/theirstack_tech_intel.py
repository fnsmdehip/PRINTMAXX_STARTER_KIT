#!/usr/bin/env python3
"""
Tech Stack Intelligence Scraper
Source: @pipelineabuser tweet - "theirstack.com / scrapes job postings and extracts the tech stack"

Extracts tech stacks from job postings to identify what companies actually use.
"Job posts reveal the stuff that's actually in use" - better signal than BuiltWith.

Usage:
    python3 theirstack_tech_intel.py                          # Run default
    python3 theirstack_tech_intel.py --company "Stripe"
    python3 theirstack_tech_intel.py --tech "snowflake" --find-companies
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
OUTPUT_CSV = BASE_DIR / "LEDGER" / "TECH_STACK_INTEL.csv"
LOG_FILE = BASE_DIR / "AUTOMATIONS" / "logs" / "tech_stack_intel.log"

# Tech keywords to look for in job postings
TECH_KEYWORDS = {
    "data_infra": ["snowflake", "databricks", "bigquery", "redshift", "firebolt", "clickhouse"],
    "data_tools": ["dbt", "airflow", "dagster", "prefect", "fivetran", "stitch", "airbyte"],
    "analytics": ["looker", "tableau", "power bi", "metabase", "mode", "sigma", "preset"],
    "crm": ["salesforce", "hubspot", "pipedrive", "close.com", "copper"],
    "marketing": ["klaviyo", "mailchimp", "braze", "iterable", "customer.io", "sendgrid"],
    "payments": ["stripe", "adyen", "braintree", "square", "paypal"],
    "infra": ["aws", "gcp", "azure", "vercel", "netlify", "railway", "render"],
    "monitoring": ["datadog", "new relic", "grafana", "sentry", "pagerduty"],
    "ai_ml": ["openai", "anthropic", "hugging face", "langchain", "llamaindex", "pinecone", "weaviate"],
}

# Target companies to analyze
DEFAULT_COMPANIES = [
    "Stripe", "Shopify", "HubSpot", "Notion", "Figma",
    "Vercel", "Supabase", "Linear", "Retool", "Zapier",
    "Webflow", "Canva", "Airtable", "Monday.com", "Asana",
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
        log(f"Fetch error: {url} - {e}")
        return None


def search_hn_jobs(company):
    """Search HN Who's Hiring for company job postings with tech details."""
    results = []
    url = f"https://hn.algolia.com/api/v1/search?query={quote(company)}&tags=comment&numericFilters=created_at_i>={int((datetime.now() - timedelta(days=90)).timestamp())}"
    data = fetch_url(url)
    if data:
        try:
            result = json.loads(data)
            for hit in result.get("hits", [])[:10]:
                text = hit.get("comment_text", "") or ""
                text_lower = text.lower()
                # Check if it's a job posting
                if any(kw in text_lower for kw in ["hiring", "looking for", "position", "role", "engineer", "developer"]):
                    # Extract tech keywords
                    found_tech = []
                    for category, keywords in TECH_KEYWORDS.items():
                        for kw in keywords:
                            if kw.lower() in text_lower:
                                found_tech.append(f"{category}:{kw}")
                    if found_tech:
                        results.append({
                            "company": company,
                            "source": "HN Who's Hiring",
                            "tech_found": ", ".join(found_tech),
                            "job_text": re.sub(r'<[^>]+>', '', text)[:500],
                            "url": f"https://news.ycombinator.com/item?id={hit.get('objectID', '')}",
                            "date": hit.get("created_at", "")[:10],
                        })
        except json.JSONDecodeError:
            pass
    return results


def search_github_jobs(company):
    """Search GitHub for company engineering posts that reveal tech stack."""
    results = []
    # Search GitHub repos for company engineering blogs
    url = f"https://api.github.com/search/repositories?q={quote(company)}+in:name+language:python+language:typescript&sort=stars&per_page=5"
    data = fetch_url(url, headers={"Accept": "application/vnd.github.v3+json"})
    if data:
        try:
            result = json.loads(data)
            for repo in result.get("items", [])[:5]:
                lang = repo.get("language", "")
                topics = repo.get("topics", [])
                results.append({
                    "company": company,
                    "source": "GitHub",
                    "tech_found": f"language:{lang}, topics:{','.join(topics[:5])}",
                    "job_text": repo.get("description", "")[:500],
                    "url": repo.get("html_url", ""),
                    "date": repo.get("updated_at", "")[:10],
                })
        except json.JSONDecodeError:
            pass
    return results


def search_job_boards_free(company):
    """Search free job board APIs for tech stack intel."""
    results = []

    # Arbeitnow API (free, no key)
    url = f"https://www.arbeitnow.com/api/job-board-api?search={quote(company)}"
    data = fetch_url(url)
    if data:
        try:
            result = json.loads(data)
            for job in result.get("data", [])[:10]:
                description = (job.get("description", "") or "").lower()
                found_tech = []
                for category, keywords in TECH_KEYWORDS.items():
                    for kw in keywords:
                        if kw.lower() in description:
                            found_tech.append(f"{category}:{kw}")

                if found_tech:
                    results.append({
                        "company": job.get("company_name", company),
                        "source": "Arbeitnow",
                        "tech_found": ", ".join(found_tech),
                        "job_text": f"{job.get('title', '')} - {job.get('description', '')[:300]}",
                        "url": job.get("url", ""),
                        "date": job.get("created_at", "")[:10],
                    })
        except json.JSONDecodeError:
            pass

    # Remotive API (free, no key)
    url2 = f"https://remotive.com/api/remote-jobs?search={quote(company)}&limit=10"
    data2 = fetch_url(url2)
    if data2:
        try:
            result = json.loads(data2)
            for job in result.get("jobs", [])[:10]:
                description = (job.get("description", "") or "").lower()
                found_tech = []
                for category, keywords in TECH_KEYWORDS.items():
                    for kw in keywords:
                        if kw.lower() in description:
                            found_tech.append(f"{category}:{kw}")
                if found_tech:
                    results.append({
                        "company": job.get("company_name", company),
                        "source": "Remotive",
                        "tech_found": ", ".join(found_tech),
                        "job_text": f"{job.get('title', '')} - {re.sub(r'<[^>]+>', '', job.get('description', ''))[:300]}",
                        "url": job.get("url", ""),
                        "date": job.get("publication_date", "")[:10],
                    })
        except json.JSONDecodeError:
            pass

    return results


def find_companies_using_tech(tech_name):
    """Reverse lookup: find companies using a specific technology."""
    results = []
    log(f"Finding companies using: {tech_name}")

    # Search HN for mentions
    url = f"https://hn.algolia.com/api/v1/search?query={quote(tech_name)}&tags=comment&numericFilters=created_at_i>={int((datetime.now() - timedelta(days=90)).timestamp())}"
    data = fetch_url(url)
    if data:
        try:
            result = json.loads(data)
            for hit in result.get("hits", [])[:20]:
                text = hit.get("comment_text", "") or ""
                text_lower = text.lower()
                if any(kw in text_lower for kw in ["we use", "we're using", "switched to", "migrated to", "we run"]):
                    results.append({
                        "tech": tech_name,
                        "source": "HN Comment",
                        "text": re.sub(r'<[^>]+>', '', text)[:300],
                        "url": f"https://news.ycombinator.com/item?id={hit.get('objectID', '')}",
                    })
        except json.JSONDecodeError:
            pass

    return results


def save_intel(results):
    """Save tech stack intel to CSV."""
    OUTPUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    file_exists = OUTPUT_CSV.exists()

    fieldnames = [
        "intel_id",
        "company",
        "source",
        "tech_found",
        "job_text",
        "url",
        "date",
        "found_date",
        "cold_email_angle",
    ]

    with open(OUTPUT_CSV, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()

        for i, result in enumerate(results):
            result["intel_id"] = f"TECH_{datetime.now().strftime('%Y%m%d')}_{i:04d}"
            result["found_date"] = datetime.now().strftime("%Y-%m-%d")
            # Generate cold email angle based on tech found
            tech = result.get("tech_found", "")
            if "data_infra" in tech or "data_tools" in tech:
                result["cold_email_angle"] = f"Noticed {result['company']} uses {tech.split(':')[-1]} - we help data teams ship 3x faster"
            elif "ai_ml" in tech:
                result["cold_email_angle"] = f"{result['company']} is investing in AI - we build custom AI tools at 1/10th agency cost"
            elif "marketing" in tech:
                result["cold_email_angle"] = f"Saw {result['company']} uses {tech.split(':')[-1]} - we help optimize email/marketing automation"
            else:
                result["cold_email_angle"] = f"Tech intel on {result['company']} - tailor outreach to their stack"

            clean = {k: result.get(k, "") for k in fieldnames}
            writer.writerow(clean)


def main():
    parser = argparse.ArgumentParser(description="Tech Stack Intelligence (@pipelineabuser)")
    parser.add_argument("--company", type=str, help="Specific company to analyze")
    parser.add_argument("--tech", type=str, help="Find companies using this tech")
    parser.add_argument("--find-companies", action="store_true", help="Reverse lookup mode")
    parser.add_argument("--summary", action="store_true", help="Show summary")
    args = parser.parse_args()

    if args.summary:
        if OUTPUT_CSV.exists():
            with open(OUTPUT_CSV, "r") as f:
                reader = list(csv.DictReader(f))
                print(f"\n{'='*60}")
                print(f"TECH STACK INTEL SUMMARY")
                print(f"{'='*60}")
                print(f"Total intel entries: {len(reader)}")
                companies = {}
                for row in reader:
                    c = row.get("company", "unknown")
                    companies[c] = companies.get(c, 0) + 1
                for company, count in sorted(companies.items(), key=lambda x: -x[1])[:20]:
                    print(f"  {company}: {count} entries")
        else:
            print("No intel yet. Run search first.")
        return

    if args.tech and args.find_companies:
        results = find_companies_using_tech(args.tech)
        print(f"\nCompanies using {args.tech}:")
        for r in results:
            print(f"  [{r['source']}] {r['text'][:100]}")
            print(f"    URL: {r['url']}")
        return

    companies = [args.company] if args.company else DEFAULT_COMPANIES

    print(f"\n{'='*60}")
    print(f"TECH STACK INTELLIGENCE SCRAPER")
    print(f"Source: @pipelineabuser - 'theirstack.com / job posts reveal tech in use'")
    print(f"{'='*60}")
    print(f"Analyzing {len(companies)} companies...")
    print()

    all_results = []
    for company in companies:
        log(f"Analyzing: {company}...")
        hn_results = search_hn_jobs(company)
        job_results = search_job_boards_free(company)
        gh_results = search_github_jobs(company)

        company_results = hn_results + job_results + gh_results
        all_results.extend(company_results)
        log(f"  {company}: {len(company_results)} tech signals (HN:{len(hn_results)} Jobs:{len(job_results)} GH:{len(gh_results)})")

    save_intel(all_results)

    print(f"\n{'='*60}")
    print(f"RESULTS")
    print(f"{'='*60}")
    print(f"Total tech signals: {len(all_results)}")
    print(f"Output: {OUTPUT_CSV}")

    # Print top findings
    if all_results:
        print(f"\nTop findings:")
        for r in all_results[:10]:
            print(f"  [{r['source']}] {r['company']}: {r['tech_found']}")

    print(f"\nNext steps:")
    print(f"  1. Review tech intel in {OUTPUT_CSV}")
    print(f"  2. Use cold_email_angle column for personalized outreach")
    print(f"  3. For full data, try theirstack.com")


if __name__ == "__main__":
    main()
