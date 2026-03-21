#!/usr/bin/env python3

from __future__ import annotations
"""
nationwide_scraper.py - Mass nationwide local business lead scraper

Wraps savvy_lead_scraper.py to iterate across 200+ US cities.
Built-in city list (top 200 by population) or load from CSV.

Usage:
    python3 nationwide_scraper.py --category "dental" --max-cities 50
    python3 nationwide_scraper.py --categories "dental,legal,plumbing,hvac" --max-cities 200
    python3 nationwide_scraper.py --categories "dental" --max-cities 10 --resume
    python3 nationwide_scraper.py --help

Output:
    Per-city:  AUTOMATIONS/leads/[category]_[city]_leads.csv
    Aggregate: AUTOMATIONS/leads/MASTER_LEADS.csv

Dependencies:
    pip install requests beautifulsoup4
"""

import argparse
import csv
import json
import os
import random
import re
import signal
import sys
import time
from datetime import datetime
from pathlib import Path

# Import the single-city scraper
SCRIPT_DIR = Path(__file__).parent.resolve()
sys.path.insert(0, str(SCRIPT_DIR))

try:
    from savvy_lead_scraper import run_scraper, CSV_HEADERS
except ImportError:
    print("ERROR: savvy_lead_scraper.py must be in the same directory.")
    print("       Make sure AUTOMATIONS/savvy_lead_scraper.py exists.")
    sys.exit(1)


# ============================================================================
# BUILT-IN TOP 200 US CITIES
# ============================================================================

# If cities_top200.csv exists, we use it. Otherwise, use this built-in list.
BUILTIN_CITIES = [
    ("New York", "NY"), ("Los Angeles", "CA"), ("Chicago", "IL"), ("Houston", "TX"),
    ("Phoenix", "AZ"), ("Philadelphia", "PA"), ("San Antonio", "TX"), ("San Diego", "CA"),
    ("Dallas", "TX"), ("San Jose", "CA"), ("Austin", "TX"), ("Jacksonville", "FL"),
    ("Fort Worth", "TX"), ("Columbus", "OH"), ("Charlotte", "NC"), ("Indianapolis", "IN"),
    ("San Francisco", "CA"), ("Seattle", "WA"), ("Denver", "CO"), ("Nashville", "TN"),
    ("Oklahoma City", "OK"), ("El Paso", "TX"), ("Washington", "DC"), ("Boston", "MA"),
    ("Las Vegas", "NV"), ("Portland", "OR"), ("Memphis", "TN"), ("Louisville", "KY"),
    ("Baltimore", "MD"), ("Milwaukee", "WI"), ("Albuquerque", "NM"), ("Tucson", "AZ"),
    ("Fresno", "CA"), ("Mesa", "AZ"), ("Sacramento", "CA"), ("Atlanta", "GA"),
    ("Kansas City", "MO"), ("Colorado Springs", "CO"), ("Omaha", "NE"), ("Raleigh", "NC"),
    ("Virginia Beach", "VA"), ("Long Beach", "CA"), ("Miami", "FL"), ("Oakland", "CA"),
    ("Minneapolis", "MN"), ("Tulsa", "OK"), ("Tampa", "FL"), ("Arlington", "TX"),
    ("New Orleans", "LA"), ("Wichita", "KS"), ("Cleveland", "OH"), ("Bakersfield", "CA"),
    ("Aurora", "CO"), ("Anaheim", "CA"), ("Honolulu", "HI"), ("Santa Ana", "CA"),
    ("Riverside", "CA"), ("Corpus Christi", "TX"), ("Lexington", "KY"), ("Henderson", "NV"),
    ("Stockton", "CA"), ("Saint Paul", "MN"), ("Cincinnati", "OH"), ("St. Louis", "MO"),
    ("Pittsburgh", "PA"), ("Greensboro", "NC"), ("Lincoln", "NE"), ("Anchorage", "AK"),
    ("Plano", "TX"), ("Orlando", "FL"), ("Irvine", "CA"), ("Newark", "NJ"),
    ("Durham", "NC"), ("Chula Vista", "CA"), ("Toledo", "OH"), ("Fort Wayne", "IN"),
    ("St. Petersburg", "FL"), ("Laredo", "TX"), ("Jersey City", "NJ"), ("Chandler", "AZ"),
    ("Madison", "WI"), ("Lubbock", "TX"), ("Scottsdale", "AZ"), ("Reno", "NV"),
    ("Buffalo", "NY"), ("Gilbert", "AZ"), ("Glendale", "AZ"), ("North Las Vegas", "NV"),
    ("Winston-Salem", "NC"), ("Chesapeake", "VA"), ("Norfolk", "VA"), ("Fremont", "CA"),
    ("Garland", "TX"), ("Irving", "TX"), ("Hialeah", "FL"), ("Richmond", "VA"),
    ("Boise", "ID"), ("Spokane", "WA"), ("Baton Rouge", "LA"), ("Tacoma", "WA"),
    ("San Bernardino", "CA"), ("Modesto", "CA"), ("Fontana", "CA"), ("Des Moines", "IA"),
    ("Moreno Valley", "CA"), ("Santa Clarita", "CA"), ("Fayetteville", "NC"),
    ("Birmingham", "AL"), ("Oxnard", "CA"), ("Rochester", "NY"), ("Port St. Lucie", "FL"),
    ("Grand Rapids", "MI"), ("Huntsville", "AL"), ("Salt Lake City", "UT"),
    ("Frisco", "TX"), ("Yonkers", "NY"), ("Amarillo", "TX"), ("Glendale", "CA"),
    ("Huntington Beach", "CA"), ("McKinney", "TX"), ("Montgomery", "AL"),
    ("Augusta", "GA"), ("Aurora", "IL"), ("Akron", "OH"), ("Little Rock", "AR"),
    ("Tempe", "AZ"), ("Columbus", "GA"), ("Overland Park", "KS"), ("Grand Prairie", "TX"),
    ("Tallahassee", "FL"), ("Cape Coral", "FL"), ("Mobile", "AL"), ("Knoxville", "TN"),
    ("Shreveport", "LA"), ("Worcester", "MA"), ("Ontario", "CA"), ("Vancouver", "WA"),
    ("Sioux Falls", "SD"), ("Chattanooga", "TN"), ("Brownsville", "TX"),
    ("Fort Lauderdale", "FL"), ("Providence", "RI"), ("Newport News", "VA"),
    ("Rancho Cucamonga", "CA"), ("Santa Rosa", "CA"), ("Peoria", "AZ"),
    ("Oceanside", "CA"), ("Elk Grove", "CA"), ("Salem", "OR"), ("Pembroke Pines", "FL"),
    ("Eugene", "OR"), ("Garden Grove", "CA"), ("Cary", "NC"), ("Corona", "CA"),
    ("Springfield", "MO"), ("Fort Collins", "CO"), ("Jackson", "MS"),
    ("Alexandria", "VA"), ("Hayward", "CA"), ("Lancaster", "CA"), ("Salinas", "CA"),
    ("Palmdale", "CA"), ("Hollywood", "FL"), ("Springfield", "MA"), ("Macon", "GA"),
    ("Kansas City", "KS"), ("Sunnyvale", "CA"), ("Pomona", "CA"), ("Killeen", "TX"),
    ("Escondido", "CA"), ("Pasadena", "TX"), ("Joliet", "IL"), ("Savannah", "GA"),
    ("Naperville", "IL"), ("Bellevue", "WA"), ("Rockford", "IL"), ("Bridgeport", "CT"),
    ("Paterson", "NJ"), ("Miramar", "FL"), ("Murfreesboro", "TN"), ("Mesquite", "TX"),
    ("Dayton", "OH"), ("Roseville", "CA"), ("Thornton", "CO"), ("Sterling Heights", "MI"),
    ("Olathe", "KS"), ("Gainesville", "FL"), ("Surprise", "AZ"), ("Denton", "TX"),
    ("Waco", "TX"), ("McAllen", "TX"), ("Charleston", "SC"), ("Carrollton", "TX"),
    ("Midland", "TX"), ("Columbia", "SC"), ("Visalia", "CA"), ("New Haven", "CT"),
    ("West Valley City", "UT"), ("Cedar Rapids", "IA"), ("Topeka", "KS"),
    ("Elizabeth", "NJ"), ("Hartford", "CT"), ("Concord", "CA"),
]


# Graceful shutdown
_shutdown = False
def _sig(s, f):
    global _shutdown
    _shutdown = True
    print("\n[!] Shutdown requested. Saving progress...")
signal.signal(signal.SIGINT, _sig)
signal.signal(signal.SIGTERM, _sig)


# ============================================================================
# STATE MANAGEMENT
# ============================================================================

STATE_FILE = SCRIPT_DIR / "leads" / ".nationwide_state.json"


def load_state():
    if STATE_FILE.exists():
        try:
            return json.loads(STATE_FILE.read_text())
        except Exception:
            pass
    return {"completed": [], "started_at": datetime.now().isoformat()}


def save_state(state):
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    state["updated_at"] = datetime.now().isoformat()
    STATE_FILE.write_text(json.dumps(state, indent=2))


# ============================================================================
# CITY LOADING
# ============================================================================

def load_cities_csv(path):
    """Load cities from a CSV file with columns: city, state_abbr or state."""
    cities = []
    with open(path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            city = row.get("city", "").strip()
            state = row.get("state_abbr", row.get("state", "")).strip()
            if city and state:
                cities.append((city, state))
    return cities


def get_cities(csv_path=None, max_cities=0):
    """Get city list from CSV or built-in, limited to max_cities."""
    if csv_path and Path(csv_path).exists():
        cities = load_cities_csv(csv_path)
        print(f"[*] Loaded {len(cities)} cities from {csv_path}")
    else:
        # Try the default CSV alongside this script
        default_csv = SCRIPT_DIR / "cities_top200.csv"
        if default_csv.exists():
            cities = load_cities_csv(str(default_csv))
            print(f"[*] Loaded {len(cities)} cities from {default_csv}")
        else:
            cities = BUILTIN_CITIES
            print(f"[*] Using built-in list of {len(cities)} cities")

    if max_cities > 0:
        cities = cities[:max_cities]
    return cities


# ============================================================================
# PROGRESS BAR (no tqdm dependency)
# ============================================================================

def progress_bar(current, total, prefix="", width=40, start_time=None):
    """Simple ASCII progress bar with ETA."""
    pct = current / total if total > 0 else 0
    filled = int(width * pct)
    bar = "#" * filled + "-" * (width - filled)
    eta_str = ""
    if start_time and current > 0:
        elapsed = time.time() - start_time
        per_item = elapsed / current
        remaining = per_item * (total - current)
        if remaining > 3600:
            eta_str = f" | ETA: {remaining/3600:.1f}h"
        elif remaining > 60:
            eta_str = f" | ETA: {remaining/60:.0f}m"
        else:
            eta_str = f" | ETA: {remaining:.0f}s"
    print(f"\r  {prefix} [{bar}] {current}/{total} ({pct*100:.0f}%){eta_str}    ", end="", flush=True)


# ============================================================================
# MASTER CSV AGGREGATION
# ============================================================================

def aggregate_master_csv(leads_dir):
    """Combine all per-city CSVs into MASTER_LEADS.csv."""
    master_path = leads_dir / "MASTER_LEADS.csv"
    all_rows = []

    for csv_file in leads_dir.glob("*_leads.csv"):
        if csv_file.name == "MASTER_LEADS.csv":
            continue
        try:
            with open(csv_file, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    all_rows.append(row)
        except Exception:
            continue

    if not all_rows:
        return 0

    # Sort by website_score ascending (hottest leads first)
    all_rows.sort(key=lambda x: int(x.get("website_score", "100") or "100"))

    # Deduplicate by business name + city
    seen = set()
    unique = []
    for row in all_rows:
        key = f"{row.get('business_name', '').lower().strip()}|{row.get('city', '').lower().strip()}"
        if key not in seen:
            seen.add(key)
            unique.append(row)

    with open(master_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_HEADERS, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(unique)

    return len(unique)


# ============================================================================
# MAIN PIPELINE
# ============================================================================

def run_nationwide(categories, max_cities=200, limit_per_city=30,
                   resume=False, cities_csv=None):
    """Run the scraper across multiple cities and categories."""
    leads_dir = SCRIPT_DIR / "leads"
    leads_dir.mkdir(parents=True, exist_ok=True)

    cities = get_cities(csv_path=cities_csv, max_cities=max_cities)
    if not cities:
        print("[!] No cities to scrape.")
        return

    # Build work queue: (category, city, state)
    work = []
    for cat in categories:
        for city_name, state in cities:
            work.append((cat, f"{city_name} {state}"))

    # Load resume state
    state = load_state() if resume else {"completed": [], "started_at": datetime.now().isoformat()}
    completed = set(state.get("completed", []))

    pending = [(cat, city) for cat, city in work if f"{cat}|{city}" not in completed]

    total = len(work)
    done_count = total - len(pending)

    print(f"\n{'='*60}")
    print(f"  NATIONWIDE LEAD SCRAPER")
    print(f"{'='*60}")
    print(f"  Categories:  {', '.join(categories)}")
    print(f"  Cities:      {len(cities)}")
    print(f"  Total runs:  {total} ({len(categories)} x {len(cities)})")
    print(f"  Limit/city:  {limit_per_city} businesses")
    if resume and done_count > 0:
        print(f"  Resuming:    {done_count} already done, {len(pending)} remaining")
    print(f"  Output:      {leads_dir}/[category]_[city]_leads.csv")
    print(f"  Master CSV:  {leads_dir}/MASTER_LEADS.csv")
    print(f"{'='*60}\n")

    if not pending:
        print("[*] All city+category combinations already completed.")
        count = aggregate_master_csv(leads_dir)
        print(f"[+] Master CSV: {count} leads in {leads_dir / 'MASTER_LEADS.csv'}")
        return

    start_time = time.time()
    total_leads = 0

    for idx, (cat, city) in enumerate(pending):
        if _shutdown:
            break

        run_num = done_count + idx + 1
        progress_bar(run_num - 1, total, prefix="Overall", start_time=start_time)
        print()
        print(f"\n[{run_num}/{total}] {cat.upper()} in {city.upper()}")

        try:
            results = run_scraper(category=cat, city=city, limit=limit_per_city, resume=False)
            total_leads += len(results) if results else 0
        except Exception as e:
            print(f"  [!] Error: {str(e)[:80]}")
            results = []

        # Mark as done
        key = f"{cat}|{city}"
        completed.add(key)
        state["completed"] = list(completed)
        save_state(state)

        # Rate limit between cities
        if idx < len(pending) - 1 and not _shutdown:
            delay = random.uniform(5.0, 10.0)
            print(f"  [*] Pausing {delay:.0f}s before next city...")
            time.sleep(delay)

    progress_bar(total, total, prefix="Overall", start_time=start_time)
    print()

    # Aggregate master CSV
    count = aggregate_master_csv(leads_dir)

    # Summary
    elapsed = time.time() - start_time
    elapsed_str = f"{elapsed/3600:.1f}h" if elapsed > 3600 else f"{elapsed/60:.0f}m"

    print(f"\n{'='*60}")
    print(f"  NATIONWIDE SCRAPING COMPLETE")
    print(f"{'='*60}")
    print(f"  Cities scraped:   {len(completed)}")
    print(f"  Total leads:      {total_leads}")
    print(f"  Master CSV:       {count} unique leads")
    print(f"  Time elapsed:     {elapsed_str}")
    print(f"  Output dir:       {leads_dir}/")
    print(f"  Master file:      {leads_dir / 'MASTER_LEADS.csv'}")

    # Count hot leads
    master = leads_dir / "MASTER_LEADS.csv"
    if master.exists():
        hot = 0
        with open(master, "r") as f:
            for row in csv.DictReader(f):
                try:
                    if int(row.get("website_score", "100")) <= 30:
                        hot += 1
                except (ValueError, KeyError): pass
        print(f"  HOT leads (0-30): {hot}")

    print(f"\n  Next: python3 mass_outreach.py --input {leads_dir / 'MASTER_LEADS.csv'} --template dental")
    print(f"{'='*60}\n")


# ============================================================================
# CLI
# ============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="Nationwide local business lead scraper (wraps savvy_lead_scraper.py)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 nationwide_scraper.py --category "dental" --max-cities 50
  python3 nationwide_scraper.py --categories "dental,legal,plumbing,hvac" --max-cities 200
  python3 nationwide_scraper.py --categories "dental" --max-cities 10 --resume
  python3 nationwide_scraper.py --categories "restaurant,salon" --max-cities 20 --limit 30

Output:
  Per-city CSV: AUTOMATIONS/leads/[category]_[city]_leads.csv
  Master CSV:   AUTOMATIONS/leads/MASTER_LEADS.csv
""")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--category", help="Single category to scrape")
    group.add_argument("--categories", help="Comma-separated categories (dental,legal,plumbing,hvac)")

    parser.add_argument("--max-cities", type=int, default=200,
                        help="Max cities to scrape (default: 200)")
    parser.add_argument("--limit", type=int, default=30,
                        help="Max businesses per city (default: 30)")
    parser.add_argument("--resume", action="store_true",
                        help="Resume from where you left off")
    parser.add_argument("--cities-csv", help="Custom cities CSV (default: built-in 200)")

    args = parser.parse_args()

    if args.category:
        categories = [args.category.strip()]
    else:
        categories = [c.strip() for c in args.categories.split(",") if c.strip()]

    if not categories:
        print("[!] No categories specified.")
        sys.exit(1)

    run_nationwide(
        categories=categories,
        max_cities=args.max_cities,
        limit_per_city=args.limit,
        resume=args.resume,
        cities_csv=args.cities_csv,
    )


if __name__ == "__main__":
    main()
