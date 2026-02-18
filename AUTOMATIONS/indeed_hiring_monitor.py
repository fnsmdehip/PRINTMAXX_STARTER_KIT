#!/usr/bin/env python3
"""
Indeed Hiring Monitor - SDR/BDR Job Posting Scraper
====================================================
Companies hiring SDRs/BDRs have broken or scaling outbound.
Both scenarios = they need help. High intent leads.

Uses DuckDuckGo to find Indeed job postings for sales development roles.
Extracts company names, job details, and signals.

Usage:
    python3 indeed_hiring_monitor.py
    python3 indeed_hiring_monitor.py --roles "SDR" "Account Executive" "Sales Manager"
    python3 indeed_hiring_monitor.py --cities "New York" "San Francisco" "Austin"
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
OUTPUT_FILE = OUTPUT_DIR / "indeed_hiring_leads.csv"
RATE_LIMIT_DELAY = 2.0

# Sales/SDR roles that signal broken outbound
DEFAULT_ROLES = [
    "SDR",
    "Sales Development Representative",
    "BDR",
    "Business Development Representative",
    "Inside Sales Representative",
    "Outbound Sales",
    "Lead Generation Specialist",
    "Sales Development Manager",
    "Head of Sales Development",
    "VP Sales Development",
]

# Major US cities + tech hubs
DEFAULT_CITIES = [
    "New York, NY",
    "San Francisco, CA",
    "Austin, TX",
    "Boston, MA",
    "Chicago, IL",
    "Denver, CO",
    "Seattle, WA",
    "Los Angeles, CA",
    "Atlanta, GA",
    "Miami, FL",
    "Dallas, TX",
    "Nashville, TN",
    "Remote",
]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
}


def search_google(query, max_results=25):
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

    # Fallback to DuckDuckGo if Google returned nothing
    if not results:
        return search_duckduckgo_html(query, max_results)

    return results


def search_duckduckgo_html(query, max_results=25):
    """Search DuckDuckGo HTML version (fallback)."""
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


def scrape_indeed_rss(role, city, max_results=15):
    """
    Use Indeed's RSS feed for job search results.
    RSS feeds are often less protected than the main site.
    """
    jobs = []
    city_encoded = quote_plus(city)
    role_encoded = quote_plus(role)

    # Indeed RSS feed URL
    rss_url = f"https://www.indeed.com/rss?q={role_encoded}&l={city_encoded}&sort=date&fromage=7"

    try:
        resp = requests.get(rss_url, headers={
            **HEADERS,
            "Accept": "application/rss+xml, application/xml, text/xml",
        }, timeout=15)

        if resp.status_code in (403, 429):
            return None

        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "xml")
        if not soup:
            soup = BeautifulSoup(resp.text, "html.parser")

        for item in soup.find_all("item"):
            job = {}

            title_el = item.find("title")
            if title_el:
                full_title = title_el.get_text(strip=True)
                # Format: "Job Title - Company - City, ST"
                parts = full_title.split(" - ")
                if len(parts) >= 2:
                    job["job_title"] = parts[0].strip()
                    job["company_name"] = parts[1].strip()
                    if len(parts) >= 3:
                        job["location"] = parts[2].strip()
                else:
                    job["job_title"] = full_title

            link_el = item.find("link")
            if link_el:
                job["job_url"] = link_el.get_text(strip=True) or link_el.string or ""

            desc_el = item.find("description")
            if desc_el:
                desc_text = desc_el.get_text(strip=True)
                # Clean HTML from description
                desc_soup = BeautifulSoup(desc_text, "html.parser")
                job["job_snippet"] = desc_soup.get_text(strip=True)[:300]

            pub_date = item.find("pubDate")
            if pub_date:
                job["posted_date"] = pub_date.get_text(strip=True)

            if job.get("company_name") or job.get("job_title"):
                jobs.append(job)

            if len(jobs) >= max_results:
                break

        return jobs if jobs else None

    except Exception as e:
        print(f"    RSS feed error: {e}")
        return None


def scrape_indeed_search(role, city, max_results=15):
    """
    Scrape Indeed search results directly via their web interface.
    Falls back to search engine if blocked.
    """
    jobs = []

    # URL-encode for Indeed
    city_encoded = quote_plus(city)
    role_encoded = quote_plus(role)

    url = f"https://www.indeed.com/jobs?q={role_encoded}&l={city_encoded}&sort=date&fromage=7"

    try:
        resp = requests.get(url, headers={
            **HEADERS,
            "Referer": "https://www.indeed.com/",
        }, timeout=15)

        if resp.status_code in (403, 429):
            return None  # Blocked, use search fallback

        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")

        # Try to find job cards
        job_cards = soup.select('.job_seen_beacon, .jobsearch-ResultsList .result, [data-jk]')

        for card in job_cards[:max_results]:
            job = {}

            # Job title
            title_el = card.select_one('.jobTitle a, .jcs-JobTitle, h2 a')
            if title_el:
                job["job_title"] = title_el.get_text(strip=True)
                href = title_el.get("href", "")
                if href.startswith("/"):
                    href = f"https://www.indeed.com{href}"
                job["job_url"] = href

            # Company name
            company_el = card.select_one('.companyName, [data-testid="company-name"], .company')
            if company_el:
                job["company_name"] = company_el.get_text(strip=True)

            # Location
            location_el = card.select_one('.companyLocation, [data-testid="text-location"], .location')
            if location_el:
                job["location"] = location_el.get_text(strip=True)

            # Salary
            salary_el = card.select_one('.salary-snippet-container, [data-testid="attribute_snippet_testid"]')
            if salary_el:
                job["salary_range"] = salary_el.get_text(strip=True)

            # Date posted
            date_el = card.select_one('.date, [data-testid="myJobsStateDate"]')
            if date_el:
                job["posted_date"] = date_el.get_text(strip=True)

            # Job snippet
            desc_el = card.select_one('.job-snippet, [class*="job-snippet"]')
            if desc_el:
                job["job_snippet"] = desc_el.get_text(strip=True)[:300]

            if job.get("company_name") or job.get("job_title"):
                jobs.append(job)

        return jobs if jobs else None

    except requests.exceptions.RequestException as e:
        print(f"    Indeed direct scrape failed: {e}")
        return None


def extract_job_from_search(result, search_role, search_city):
    """
    Extract job posting data from a search engine result.
    """
    url = result.get("url", "")
    title = result.get("title", "")
    snippet = result.get("snippet", "")

    # Filter for actual job posting sites
    job_sites = ["indeed.com", "linkedin.com/jobs", "glassdoor.com", "ziprecruiter.com",
                 "lever.co", "greenhouse.io", "builtin.com", "wellfound.com"]

    is_job_site = any(site in url.lower() for site in job_sites)
    if not is_job_site:
        return None

    job = {
        "job_url": url,
        "search_role": search_role,
        "search_city": search_city,
    }

    # Extract company name from title
    # Common patterns: "Job Title - Company Name | Indeed.com"
    title_parts = re.split(r'\s*[-|]\s*', title)
    if len(title_parts) >= 2:
        job["job_title"] = title_parts[0].strip()
        # Company is usually second part (before site name)
        company = title_parts[1].strip()
        # Remove site suffixes
        company = re.sub(r'\s*(Indeed|LinkedIn|Glassdoor|ZipRecruiter|Lever|Greenhouse|BuiltIn|Wellfound).*$', '', company, flags=re.IGNORECASE).strip()
        if company and len(company) < 80:
            job["company_name"] = company
    else:
        job["job_title"] = title.strip()

    # Extract location from snippet
    location_match = re.search(r'(?:in|Location:)\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*,?\s*[A-Z]{2})', snippet)
    if location_match:
        job["location"] = location_match.group(1).strip()
    else:
        job["location"] = search_city

    # Extract salary from snippet
    salary_match = re.search(r'\$[\d,]+(?:\s*[-to]\s*\$[\d,]+)?(?:\s*(?:per|a)\s*(?:year|month|hour))?', snippet, re.IGNORECASE)
    if salary_match:
        job["salary_range"] = salary_match.group(0)

    # Extract posting date
    date_patterns = [
        r'(\d+)\s*(?:days?|hours?)\s*ago',
        r'Posted\s+(\w+\s+\d{1,2},?\s*\d{4})',
        r'(Just posted|Today|Yesterday)',
    ]
    for pattern in date_patterns:
        match = re.search(pattern, snippet, re.IGNORECASE)
        if match:
            job["posted_date"] = match.group(0)
            break

    job["job_snippet"] = snippet[:300]

    return job


def classify_hiring_signal(job):
    """
    Classify the hiring signal to determine lead quality.
    """
    title = (job.get("job_title", "") + " " + job.get("job_snippet", "")).lower()

    signals = []
    lead_quality = "MEDIUM"

    # Multiple SDR roles = scaling outbound (high intent)
    if any(word in title for word in ["multiple", "several", "team", "3+", "5+", "10+"]):
        signals.append("SCALING_TEAM")
        lead_quality = "HIGHEST"

    # Senior/Head/VP = building outbound from scratch (high intent)
    if any(word in title for word in ["head of", "vp ", "vice president", "director of"]):
        signals.append("LEADERSHIP_HIRE")
        lead_quality = "HIGH"

    # Manager role = they have a team and need management
    if "manager" in title:
        signals.append("TEAM_MANAGEMENT")
        lead_quality = "HIGH"

    # Entry level = they're building basic outbound
    if any(word in title for word in ["entry level", "junior", "associate"]):
        signals.append("BUILDING_BASICS")

    # Remote = wider company, possibly more budget
    if "remote" in title or "remote" in job.get("location", "").lower():
        signals.append("REMOTE_OK")

    # Urgency signals
    if any(word in title for word in ["asap", "immediate", "urgent", "start immediately"]):
        signals.append("URGENT_HIRE")
        lead_quality = "HIGHEST"

    # Tech stack mentions
    tech_mentions = []
    for tech in ["salesforce", "hubspot", "outreach", "salesloft", "apollo", "zoominfo", "linkedin"]:
        if tech in title:
            tech_mentions.append(tech)
    if tech_mentions:
        job["tech_stack_mentioned"] = ", ".join(tech_mentions)

    job["hiring_signals"] = "; ".join(signals) if signals else "STANDARD"
    job["lead_quality"] = lead_quality

    return job


def search_jobs(role, city, max_results=15):
    """
    Search for job postings - first try Indeed directly, then fallback to search.
    """
    # Try Indeed first
    print(f"    Trying Indeed direct for '{role}' in {city}...")
    direct_jobs = scrape_indeed_search(role, city, max_results)

    if direct_jobs:
        for j in direct_jobs:
            j["search_role"] = role
            j["search_city"] = city
            j["source"] = "indeed_direct"
        return direct_jobs

    # Fallback 1: Indeed RSS feed
    print(f"    Trying Indeed RSS feed...")
    rss_jobs = scrape_indeed_rss(role, city, max_results)
    if rss_jobs:
        for j in rss_jobs:
            j["search_role"] = role
            j["search_city"] = city
            j["source"] = "indeed_rss"
        return rss_jobs

    # Fallback 2: Search engine
    print(f"    Using search engine fallback...")
    queries = [
        f'site:indeed.com "{role}" "{city}" jobs',
        f'"{role}" "{city}" hiring site:indeed.com OR site:linkedin.com/jobs OR site:builtin.com',
        f'"{role}" hiring "{city}" 2026',
    ]

    all_jobs = []
    for query in queries:
        results = search_google(query, max_results=max_results)
        for result in results:
            job = extract_job_from_search(result, role, city)
            if job:
                job["source"] = "search"
                all_jobs.append(job)
        time.sleep(RATE_LIMIT_DELAY)

    return all_jobs


def write_csv(jobs, output_path):
    """Write jobs to CSV."""
    if not jobs:
        print("No jobs to write.")
        return

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    columns = [
        "company_name", "job_title", "location", "salary_range",
        "posted_date", "lead_quality", "hiring_signals",
        "tech_stack_mentioned", "search_role", "search_city",
        "job_snippet", "job_url", "source", "scraped_at"
    ]

    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=columns, extrasaction="ignore")
        writer.writeheader()
        for job in jobs:
            job["scraped_at"] = datetime.now().isoformat()
            writer.writerow(job)

    print(f"\nWrote {len(jobs)} job leads to {output_path}")


def print_summary(jobs):
    """Print summary."""
    if not jobs:
        print("No jobs found.")
        return

    print("\n" + "=" * 70)
    print("INDEED HIRING MONITOR SUMMARY")
    print("=" * 70)
    print(f"Total job postings found: {len(jobs)}")

    # Unique companies
    companies = set(j.get("company_name", "Unknown") for j in jobs if j.get("company_name"))
    print(f"Unique companies hiring: {len(companies)}")

    # By city
    by_city = {}
    for j in jobs:
        city = j.get("search_city", j.get("location", "Unknown"))
        by_city[city] = by_city.get(city, 0) + 1

    print(f"\nBy city:")
    for city, count in sorted(by_city.items(), key=lambda x: x[1], reverse=True)[:10]:
        print(f"  {city}: {count} postings")

    # By lead quality
    by_quality = {}
    for j in jobs:
        q = j.get("lead_quality", "Unknown")
        by_quality[q] = by_quality.get(q, 0) + 1

    print(f"\nBy lead quality:")
    for q, count in sorted(by_quality.items(), key=lambda x: x[1], reverse=True):
        print(f"  {q}: {count} leads")

    # Top signals
    all_signals = []
    for j in jobs:
        sigs = j.get("hiring_signals", "")
        if sigs and sigs != "STANDARD":
            all_signals.extend(sigs.split("; "))

    if all_signals:
        from collections import Counter
        signal_counts = Counter(all_signals)
        print(f"\nTop hiring signals:")
        for sig, count in signal_counts.most_common(10):
            print(f"  {sig}: {count}")

    # Top companies by posting count
    company_counts = {}
    for j in jobs:
        comp = j.get("company_name", "")
        if comp:
            company_counts[comp] = company_counts.get(comp, 0) + 1

    if company_counts:
        print(f"\nTop companies (most SDR postings = most broken outbound):")
        for comp, count in sorted(company_counts.items(), key=lambda x: x[1], reverse=True)[:15]:
            print(f"  {comp}: {count} postings")

    print("=" * 70)


def main():
    parser = argparse.ArgumentParser(description="Indeed Hiring Monitor - SDR/BDR Job Scraper")
    parser.add_argument("--roles", nargs="+", help="Job roles to search")
    parser.add_argument("--cities", nargs="+", help="Cities to search")
    parser.add_argument("--output", type=str, default=str(OUTPUT_FILE))
    parser.add_argument("--max-per-search", type=int, default=15)
    parser.add_argument("--quick", action="store_true", help="Quick mode: 3 roles, 5 cities")

    args = parser.parse_args()

    print("=" * 70)
    print("INDEED HIRING MONITOR - SDR/BDR JOB POSTINGS")
    print("=" * 70)
    print("Strategy: Company hiring 5 SDRs? Their outbound is broken or scaling.")
    print("Both scenarios = they need help.\n")

    roles = args.roles or DEFAULT_ROLES
    cities = args.cities or DEFAULT_CITIES

    if args.quick:
        roles = roles[:3]
        cities = cities[:5]

    # Use a focused subset to avoid too many queries
    # Prioritize the most specific role terms
    priority_roles = ["SDR", "Sales Development Representative", "BDR", "Outbound Sales"]
    search_roles = [r for r in priority_roles if r in roles] or roles[:4]

    total = len(search_roles) * len(cities)
    print(f"Searching {len(search_roles)} roles x {len(cities)} cities = {total} searches\n")

    all_jobs = []
    search_count = 0

    for role in search_roles:
        print(f"\n--- Role: {role} ---")
        for city in cities:
            search_count += 1
            print(f"  [{search_count}/{total}] {city}...")

            jobs = search_jobs(role, city, max_results=args.max_per_search)

            # Classify each job
            for job in jobs:
                job = classify_hiring_signal(job)

            print(f"    Found {len(jobs)} postings")
            all_jobs.extend(jobs)

    # Deduplicate by company + job_title
    seen = set()
    deduped = []
    for j in all_jobs:
        key = f"{j.get('company_name','')}-{j.get('job_title','')}-{j.get('location','')}"
        if key not in seen:
            seen.add(key)
            deduped.append(j)

    all_jobs = deduped
    print(f"\n{len(all_jobs)} unique job leads after deduplication")

    print_summary(all_jobs)
    write_csv(all_jobs, args.output)

    print(f"\nNext steps:")
    print(f"  1. Sort by lead_quality (HIGHEST first)")
    print(f"  2. Companies with 3+ SDR postings = highest priority targets")
    print(f"  3. Find hiring manager on LinkedIn (VP Sales, Head of Revenue)")
    print(f"  4. Cold email: 'I saw you're hiring [X] SDRs. We help companies like [similar co] book 40% more meetings.'")
    print(f"  5. Time-sensitive: reach out within 7 days of posting")


if __name__ == "__main__":
    main()
