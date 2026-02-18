#!/usr/bin/env python3
"""
PRINTMAXX Bulk Lead Downloader
================================
Downloads millions of US business leads from Overture Maps (free, open data).
Replaces the slow city-by-city scraper approach.

Overture Maps: Backed by Meta, Microsoft, Amazon, TomTom.
License: CDLA Permissive 2.0 (free for commercial use).
Data: 15-25M US POIs with name, phone, email, website, address, category.

USAGE:
  python3 download_bulk_leads.py --categories dentist,restaurant,plumber,lawyer
  python3 download_bulk_leads.py --all-categories
  python3 download_bulk_leads.py --state TX --categories dentist
  python3 download_bulk_leads.py --status
  python3 download_bulk_leads.py --count

OUTPUT:
  AUTOMATIONS/leads/bulk/US_LEADS_{category}.csv  (per-category files)
  AUTOMATIONS/leads/bulk/US_LEADS_MASTER.csv      (all combined)
"""

import os
import sys
import json
import csv
import argparse
from datetime import datetime
from pathlib import Path

PROJECT_ROOT = "/Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt"
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "AUTOMATIONS", "leads", "bulk")
PYTHON = "/Library/Frameworks/Python.framework/Versions/3.12/bin/python3"

# Target business categories (Overture Maps category names)
TARGET_CATEGORIES = {
    "dentist": ["dentist", "dental_clinic", "dental_hygienist", "orthodontist", "oral_surgeon"],
    "restaurant": ["restaurant", "fast_food_restaurant", "pizza_restaurant", "cafe"],
    "plumber": ["plumbing", "plumber"],
    "lawyer": ["lawyer", "law_firm", "attorney", "legal_services"],
    "doctor": ["doctor", "medical_clinic", "physician", "family_medicine"],
    "chiropractor": ["chiropractor", "chiropractic"],
    "realtor": ["real_estate_agent", "real_estate_agency", "realtor"],
    "gym": ["gym", "fitness_center", "health_club"],
    "salon": ["beauty_salon", "hair_salon", "nail_salon", "barber_shop"],
    "auto_repair": ["automotive_repair", "auto_body_shop", "automotive_services_and_repair", "auto_repair"],
    "accountant": ["accountant", "accounting_firm", "tax_preparation"],
    "veterinarian": ["veterinarian", "animal_hospital", "pet_clinic"],
    "hvac": ["hvac_services", "hvac", "heating_contractor", "air_conditioning"],
    "roofing": ["roofing", "roofing_contractor", "roofing_service"],
    "electrician": ["electrician", "electrical_contractor"],
}

# US bounding box (continental US)
US_BBOX = {
    "min_lon": -125.0,
    "min_lat": 24.0,
    "max_lon": -66.0,
    "max_lat": 50.0,
}

# State bounding boxes (approximate) for filtering
STATE_BBOXES = {
    "TX": (-106.65, 25.84, -93.51, 36.50),
    "CA": (-124.48, 32.53, -114.13, 42.01),
    "FL": (-87.63, 24.52, -80.03, 31.00),
    "NY": (-79.76, 40.50, -71.86, 45.01),
    "IL": (-91.51, 36.97, -87.02, 42.51),
    "PA": (-80.52, 39.72, -74.69, 42.27),
    "OH": (-84.82, 38.40, -80.52, 42.32),
    "GA": (-85.61, 30.36, -80.84, 35.00),
    "NC": (-84.32, 33.84, -75.46, 36.59),
    "MI": (-90.42, 41.70, -82.12, 48.30),
    "AZ": (-114.82, 31.33, -109.04, 37.00),
    "WA": (-124.85, 45.54, -116.92, 49.00),
    "CO": (-109.06, 36.99, -102.04, 41.00),
}


def download_with_duckdb(categories: list, state: str = None, limit: int = None):
    """
    Use DuckDB to query Overture Maps data directly from S3.
    This is faster and more flexible than the CLI tool.
    """
    try:
        import duckdb
    except ImportError:
        print("ERROR: duckdb not installed. Run: pip3 install duckdb")
        sys.exit(1)

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Build bounding box
    if state and state.upper() in STATE_BBOXES:
        bbox = STATE_BBOXES[state.upper()]
        bbox_filter = f"""
            AND bbox.xmin >= {bbox[0]} AND bbox.ymin >= {bbox[1]}
            AND bbox.xmax <= {bbox[2]} AND bbox.ymax <= {bbox[3]}
        """
        print(f"Filtering to state: {state.upper()}")
    else:
        bbox_filter = f"""
            AND bbox.xmin >= {US_BBOX['min_lon']} AND bbox.ymin >= {US_BBOX['min_lat']}
            AND bbox.xmax <= {US_BBOX['max_lon']} AND bbox.ymax <= {US_BBOX['max_lat']}
        """

    limit_clause = f"LIMIT {limit}" if limit else ""

    con = duckdb.connect()

    # Install and load required extensions
    con.execute("INSTALL httpfs;")
    con.execute("LOAD httpfs;")
    con.execute("SET s3_region='us-west-2';")

    # Overture Maps S3 path (latest release)
    overture_path = "s3://overturemaps-us-west-2/release/2025-12-17.0/theme=places/type=place/*"

    total_records = 0
    all_rows = []

    for cat_name in categories:
        if cat_name not in TARGET_CATEGORIES:
            print(f"WARNING: Unknown category '{cat_name}'. Skipping.")
            continue

        subcategories = TARGET_CATEGORIES[cat_name]
        cat_filter_parts = []
        for subcat in subcategories:
            cat_filter_parts.append(f"LOWER(categories.primary) LIKE '%{subcat}%'")
        cat_filter = " OR ".join(cat_filter_parts)

        print(f"\nDownloading: {cat_name} ({len(subcategories)} subcategories)...")

        query = f"""
        SELECT
            id,
            names.primary AS name,
            categories.primary AS category,
            COALESCE(phones[1], '') AS phone,
            COALESCE(emails[1], '') AS email,
            COALESCE(websites[1], '') AS website,
            COALESCE(addresses[1].freeform, '') AS address,
            COALESCE(addresses[1].locality, '') AS city,
            COALESCE(addresses[1].region, '') AS state,
            COALESCE(addresses[1].postcode, '') AS zip,
            COALESCE(addresses[1].country, '') AS country,
            ROUND(bbox.ymin + (bbox.ymax - bbox.ymin) / 2, 6) AS lat,
            ROUND(bbox.xmin + (bbox.xmax - bbox.xmin) / 2, 6) AS lon,
            confidence AS confidence_score
        FROM read_parquet('{overture_path}', filename=true, hive_partitioning=true)
        WHERE ({cat_filter})
            {bbox_filter}
            AND COALESCE(addresses[1].country, '') IN ('US', 'USA', 'United States')
        {limit_clause}
        """

        try:
            result = con.execute(query).fetchall()
            columns = [
                "id", "name", "category", "phone", "email", "website",
                "address", "city", "state", "zip", "country", "lat", "lon",
                "confidence_score"
            ]

            # Save per-category CSV
            cat_file = os.path.join(OUTPUT_DIR, f"US_LEADS_{cat_name.upper()}.csv")
            with open(cat_file, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(columns)
                writer.writerows(result)

            print(f"  {cat_name}: {len(result):,} records -> {cat_file}")
            total_records += len(result)

            for row in result:
                all_rows.append(list(row) + [cat_name])

        except Exception as e:
            print(f"  ERROR on {cat_name}: {e}")
            # Try simpler query without spatial functions
            try:
                simple_query = f"""
                SELECT
                    id,
                    names.primary AS name,
                    categories.primary AS category,
                    COALESCE(phones[1], '') AS phone,
                    COALESCE(emails[1], '') AS email,
                    COALESCE(websites[1], '') AS website,
                    COALESCE(addresses[1].freeform, '') AS address,
                    COALESCE(addresses[1].locality, '') AS city,
                    COALESCE(addresses[1].region, '') AS state,
                    COALESCE(addresses[1].postcode, '') AS zip,
                    COALESCE(addresses[1].country, '') AS country,
                    bbox.xmin AS lon,
                    bbox.ymin AS lat,
                    confidence AS confidence_score
                FROM read_parquet('{overture_path}', filename=true, hive_partitioning=true)
                WHERE ({cat_filter})
                    {bbox_filter}
                    AND COALESCE(addresses[1].country, '') IN ('US', 'USA', 'United States')
                {limit_clause}
                """
                result = con.execute(simple_query).fetchall()
                columns = [
                    "id", "name", "category", "phone", "email", "website",
                    "address", "city", "state", "zip", "country", "lon", "lat",
                    "confidence_score"
                ]

                cat_file = os.path.join(OUTPUT_DIR, f"US_LEADS_{cat_name.upper()}.csv")
                with open(cat_file, 'w', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow(columns)
                    writer.writerows(result)

                print(f"  {cat_name}: {len(result):,} records (fallback query) -> {cat_file}")
                total_records += len(result)

                for row in result:
                    all_rows.append(list(row) + [cat_name])

            except Exception as e2:
                print(f"  FATAL ERROR on {cat_name}: {e2}")
                continue

    # Save combined master file
    if all_rows:
        master_file = os.path.join(OUTPUT_DIR, "US_LEADS_MASTER.csv")
        master_columns = [
            "id", "name", "category", "phone", "email", "website",
            "address", "city", "state", "zip", "country", "lat", "lon",
            "confidence_score", "lead_category"
        ]
        with open(master_file, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(master_columns)
            writer.writerows(all_rows)

        # Stats
        has_phone = sum(1 for r in all_rows if r[3])
        has_email = sum(1 for r in all_rows if r[4])
        has_website = sum(1 for r in all_rows if r[5])

        print(f"\n{'='*60}")
        print(f"DOWNLOAD COMPLETE")
        print(f"{'='*60}")
        print(f"Total records: {total_records:,}")
        print(f"With phone:    {has_phone:,} ({has_phone/max(total_records,1)*100:.1f}%)")
        print(f"With email:    {has_email:,} ({has_email/max(total_records,1)*100:.1f}%)")
        print(f"With website:  {has_website:,} ({has_website/max(total_records,1)*100:.1f}%)")
        print(f"Master file:   {master_file}")
        print(f"Per-category:  {OUTPUT_DIR}/US_LEADS_*.csv")
    else:
        print("\nNo records downloaded.")

    con.close()
    return total_records


def download_with_cli(categories: list, state: str = None):
    """
    Fallback: Use overturemaps CLI to download as GeoJSON then convert.
    Slower but simpler if DuckDB has issues.
    """
    import subprocess

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    bbox = f"{US_BBOX['min_lon']},{US_BBOX['min_lat']},{US_BBOX['max_lon']},{US_BBOX['max_lat']}"

    for cat_name in categories:
        output_file = os.path.join(OUTPUT_DIR, f"US_PLACES_{cat_name.upper()}.geojson")
        print(f"Downloading {cat_name} via CLI...")

        cmd = [
            PYTHON, "-m", "overturemaps", "download",
            "--bbox", bbox,
            "-f", "geojson",
            "--type", "place",
            "-o", output_file,
        ]

        try:
            subprocess.run(cmd, check=True, timeout=600)
            print(f"  Saved: {output_file}")
        except subprocess.TimeoutExpired:
            print(f"  TIMEOUT on {cat_name}")
        except subprocess.CalledProcessError as e:
            print(f"  ERROR: {e}")


def show_status():
    """Show current bulk lead data status."""
    if not os.path.exists(OUTPUT_DIR):
        print("No bulk leads downloaded yet.")
        print(f"Run: python3 {__file__} --categories dentist,restaurant,plumber,lawyer")
        return

    print(f"\n{'Category':<20} {'Records':>10} {'Phone':>10} {'Email':>10} {'Website':>10} {'File Size':>12}")
    print("-" * 80)

    total = 0
    for f in sorted(os.listdir(OUTPUT_DIR)):
        if f.startswith("US_LEADS_") and f.endswith(".csv") and f != "US_LEADS_MASTER.csv":
            filepath = os.path.join(OUTPUT_DIR, f)
            cat = f.replace("US_LEADS_", "").replace(".csv", "")
            size = os.path.getsize(filepath)

            records = phone = email = website = 0
            with open(filepath, 'r') as csvf:
                reader = csv.DictReader(csvf)
                for row in reader:
                    records += 1
                    if row.get("phone"): phone += 1
                    if row.get("email"): email += 1
                    if row.get("website"): website += 1
            total += records

            size_str = f"{size/1024/1024:.1f} MB" if size > 1024*1024 else f"{size/1024:.0f} KB"
            print(f"{cat:<20} {records:>10,} {phone:>10,} {email:>10,} {website:>10,} {size_str:>12}")

    # Master file
    master = os.path.join(OUTPUT_DIR, "US_LEADS_MASTER.csv")
    if os.path.exists(master):
        size = os.path.getsize(master)
        size_str = f"{size/1024/1024:.1f} MB" if size > 1024*1024 else f"{size/1024:.0f} KB"
        print("-" * 80)
        print(f"{'MASTER TOTAL':<20} {total:>10,} {'':>10} {'':>10} {'':>10} {size_str:>12}")


def count_available():
    """Quick count of how many records we could download per category."""
    print("Estimating available records per category from Overture Maps...")
    print("(This queries S3 directly — may take 30-60 seconds per category)")
    print()

    try:
        import duckdb
        con = duckdb.connect()
        con.execute("INSTALL httpfs; LOAD httpfs; SET s3_region='us-west-2';")

        overture_path = "s3://overturemaps-us-west-2/release/2025-12-17.0/theme=places/type=place/*"

        for cat_name, subcats in TARGET_CATEGORIES.items():
            cat_filter_parts = [f"LOWER(categories.primary) LIKE '%{s}%'" for s in subcats]
            cat_filter = " OR ".join(cat_filter_parts)

            query = f"""
            SELECT COUNT(*) FROM read_parquet('{overture_path}', filename=true, hive_partitioning=true)
            WHERE ({cat_filter})
                AND bbox.xmin >= -125 AND bbox.ymin >= 24
                AND bbox.xmax <= -66 AND bbox.ymax <= 50
            """

            try:
                count = con.execute(query).fetchone()[0]
                print(f"  {cat_name:<20} ~{count:>10,} records")
            except Exception as e:
                print(f"  {cat_name:<20} ERROR: {e}")

        con.close()
    except ImportError:
        print("Need duckdb: pip3 install duckdb")


def main():
    parser = argparse.ArgumentParser(description="PRINTMAXX Bulk Lead Downloader (Overture Maps)")
    parser.add_argument("--categories", type=str, help="Comma-separated categories (dentist,restaurant,plumber,lawyer)")
    parser.add_argument("--all-categories", action="store_true", help="Download ALL 15 target categories")
    parser.add_argument("--state", type=str, help="Filter to a specific state (e.g., TX, CA, FL)")
    parser.add_argument("--limit", type=int, help="Limit records per category (for testing)")
    parser.add_argument("--status", action="store_true", help="Show current bulk lead data status")
    parser.add_argument("--count", action="store_true", help="Estimate available records per category")
    parser.add_argument("--method", choices=["duckdb", "cli"], default="duckdb", help="Download method")

    args = parser.parse_args()

    if args.status:
        show_status()
    elif args.count:
        count_available()
    elif args.all_categories:
        categories = list(TARGET_CATEGORIES.keys())
        print(f"Downloading ALL {len(categories)} categories: {', '.join(categories)}")
        download_with_duckdb(categories, state=args.state, limit=args.limit)
    elif args.categories:
        categories = [c.strip() for c in args.categories.split(",")]
        download_with_duckdb(categories, state=args.state, limit=args.limit)
    else:
        parser.print_help()
        print(f"\nAvailable categories: {', '.join(TARGET_CATEGORIES.keys())}")


if __name__ == "__main__":
    main()
