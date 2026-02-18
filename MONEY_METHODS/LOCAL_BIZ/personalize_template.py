#!/usr/bin/env python3
"""
personalize_template.py - Personalize local business landing page templates.

Takes a template HTML file and business details, outputs a personalized version
ready to deploy as a demo for cold outreach.

Usage:
    python3 personalize_template.py \
        --template templates/plumber.html \
        --name "Joe's Plumbing" \
        --phone "(555) 123-4567" \
        --address "123 Main St" \
        --city "Austin" \
        --state "TX" \
        --zip "78701" \
        --email "joe@joesplumbing.com" \
        --output output/joes-plumbing.html

    # Batch mode from CSV:
    python3 personalize_template.py \
        --template templates/dental.html \
        --csv businesses.csv \
        --output-dir output/

CSV format (first row = headers):
    name,phone,address,city,state,zip,email,years_in_business,rating,review_count
"""

import argparse
import csv
import os
import re
import sys
from pathlib import Path


# Default placeholder values for fields not provided
DEFAULTS = {
    "BUSINESS_NAME": "Your Business Name",
    "PHONE": "(555) 000-0000",
    "ADDRESS": "123 Main Street",
    "CITY": "Your City",
    "STATE": "ST",
    "ZIP": "00000",
    "EMAIL": "info@yourbusiness.com",
    "YEARS_IN_BUSINESS": "10",
    "RATING_STARS": "4.9",
    "REVIEW_COUNT": "150",
    "LICENSE_NUMBER": "12345",
    "JOBS_COMPLETED": "5,000",
    "MAP_LAT": "30.2672",
    "MAP_LNG": "-97.7431",
    # Plumber-specific
    "SERVICE_AREA_1": "North Side",
    "SERVICE_AREA_2": "South Side",
    "SERVICE_AREA_3": "East Side",
    "SERVICE_AREA_4": "West Side",
    "SERVICE_AREA_5": "Downtown",
    # Realtor-specific
    "AGENT_FIRST_NAME": "Agent",
    "TOTAL_SOLD": "200",
    "VOLUME_SOLD": "85",
    "DAYS_ON_MARKET": "14",
    "SALE_TO_LIST": "99",
    "AVG_SALE_PRICE": "425,000",
    "YEARS_EXPERIENCE": "12",
    "BROKERAGE_NAME": "Brokerage Name",
    "SPECIALTIES": "Residential, First-time buyers",
    "NEIGHBORHOOD_1": "Downtown",
    "NEIGHBORHOOD_2": "Midtown",
    "NEIGHBORHOOD_3": "North End",
    "NEIGHBORHOOD_4": "West Hills",
    "NEIGHBORHOOD_5": "Riverside",
    "NEIGHBORHOOD_6": "Lakewood",
    "LISTING_1_PRICE": "425,000",
    "LISTING_1_ADDRESS": "123 Oak Lane",
    "LISTING_1_BEDS": "3",
    "LISTING_1_BATHS": "2",
    "LISTING_1_SQFT": "1,850",
    "LISTING_2_PRICE": "575,000",
    "LISTING_2_ADDRESS": "456 Maple Drive",
    "LISTING_2_BEDS": "4",
    "LISTING_2_BATHS": "3",
    "LISTING_2_SQFT": "2,400",
    "LISTING_3_PRICE": "350,000",
    "LISTING_3_ADDRESS": "789 Elm Street",
    "LISTING_3_BEDS": "2",
    "LISTING_3_BATHS": "2",
    "LISTING_3_SQFT": "1,200",
    # Dental-specific
    "DOCTOR_NAME": "Dr. Smith",
    "DOCTOR_TITLE": "DDS",
    # Restaurant-specific
    "CUISINE_TYPE": "American",
    "HOURS_WEEKDAY": "11am - 10pm",
    "HOURS_WEEKEND": "10am - 11pm",
    # Gym/Fitness-specific
    "MEMBERSHIP_PRICE": "49",
    "GYM_HOURS": "5am - 11pm",
}


def slugify(text: str) -> str:
    """Convert text to URL-safe slug."""
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_-]+", "-", text)
    text = re.sub(r"^-+|-+$", "", text)
    return text


def personalize(template_content: str, replacements: dict) -> str:
    """Replace all {{PLACEHOLDER}} tokens with actual values."""
    result = template_content

    # Merge with defaults (provided values override defaults)
    merged = {**DEFAULTS, **replacements}

    # Replace all {{PLACEHOLDER}} patterns
    for key, value in merged.items():
        pattern = "{{" + key + "}}"
        result = result.replace(pattern, str(value))

    # Find any remaining unreplaced placeholders and warn
    remaining = re.findall(r"\{\{([A-Z_0-9]+)\}\}", result)
    if remaining:
        unique = sorted(set(remaining))
        print(f"  Warning: {len(unique)} unreplaced placeholders: {', '.join(unique[:10])}", file=sys.stderr)

    return result


def build_replacements_from_args(args) -> dict:
    """Build replacement dict from CLI arguments."""
    r = {}
    if args.name:
        r["BUSINESS_NAME"] = args.name
        # Auto-derive agent first name for realtor templates
        first = args.name.split()[0].rstrip("'s").rstrip("'s")
        r["AGENT_FIRST_NAME"] = first
    if args.phone:
        r["PHONE"] = args.phone
    if args.address:
        r["ADDRESS"] = args.address
    if args.city:
        r["CITY"] = args.city
    if args.state:
        r["STATE"] = args.state
    if args.zip:
        r["ZIP"] = args.zip
    if args.email:
        r["EMAIL"] = args.email
    if args.years:
        r["YEARS_IN_BUSINESS"] = args.years
        r["YEARS_EXPERIENCE"] = args.years
    if args.rating:
        r["RATING_STARS"] = args.rating
    if args.reviews:
        r["REVIEW_COUNT"] = args.reviews
    if args.license:
        r["LICENSE_NUMBER"] = args.license

    # Extra key=value pairs
    if args.extra:
        for pair in args.extra:
            if "=" in pair:
                k, v = pair.split("=", 1)
                r[k.strip().upper()] = v.strip()

    return r


def build_replacements_from_csv_row(row: dict) -> dict:
    """Build replacement dict from a CSV row."""
    # Map common CSV column names to template placeholders
    column_map = {
        "name": "BUSINESS_NAME",
        "business_name": "BUSINESS_NAME",
        "phone": "PHONE",
        "address": "ADDRESS",
        "city": "CITY",
        "state": "STATE",
        "zip": "ZIP",
        "zipcode": "ZIP",
        "zip_code": "ZIP",
        "email": "EMAIL",
        "years": "YEARS_IN_BUSINESS",
        "years_in_business": "YEARS_IN_BUSINESS",
        "rating": "RATING_STARS",
        "stars": "RATING_STARS",
        "reviews": "REVIEW_COUNT",
        "review_count": "REVIEW_COUNT",
        "license": "LICENSE_NUMBER",
        "license_number": "LICENSE_NUMBER",
    }

    r = {}
    for csv_col, value in row.items():
        csv_col_lower = csv_col.strip().lower()
        if csv_col_lower in column_map:
            r[column_map[csv_col_lower]] = value.strip()
        else:
            # Pass through as uppercase placeholder name
            r[csv_col.strip().upper()] = value.strip()

    # Auto-derive agent first name
    if "BUSINESS_NAME" in r:
        first = r["BUSINESS_NAME"].split()[0].rstrip("'s").rstrip("'s")
        if "AGENT_FIRST_NAME" not in r:
            r["AGENT_FIRST_NAME"] = first

    return r


def process_single(template_path: str, replacements: dict, output_path: str):
    """Process a single template with replacements and write output."""
    with open(template_path, "r", encoding="utf-8") as f:
        template = f.read()

    result = personalize(template, replacements)

    # Ensure output directory exists
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(result)

    print(f"  Created: {output_path}")


def process_batch(template_path: str, csv_path: str, output_dir: str):
    """Process a template for each row in a CSV file."""
    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    if not rows:
        print("Error: CSV file is empty or has no data rows.", file=sys.stderr)
        sys.exit(1)

    os.makedirs(output_dir, exist_ok=True)
    template_name = Path(template_path).stem

    print(f"Processing {len(rows)} businesses from {csv_path}...")
    for i, row in enumerate(rows, 1):
        replacements = build_replacements_from_csv_row(row)
        biz_name = replacements.get("BUSINESS_NAME", f"business-{i}")
        slug = slugify(biz_name)
        output_path = os.path.join(output_dir, f"{template_name}-{slug}.html")
        print(f"  [{i}/{len(rows)}] {biz_name}")
        process_single(template_path, replacements, output_path)

    print(f"\nDone. {len(rows)} files created in {output_dir}/")


def main():
    parser = argparse.ArgumentParser(
        description="Personalize local business landing page templates.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Single business:
  python3 personalize_template.py \\
      --template templates/plumber.html \\
      --name "Joe's Plumbing" \\
      --phone "(555) 123-4567" \\
      --city "Austin" --state "TX" \\
      --output output/joes-plumbing.html

  # Batch from CSV:
  python3 personalize_template.py \\
      --template templates/dental.html \\
      --csv businesses.csv \\
      --output-dir output/

  # With extra custom fields:
  python3 personalize_template.py \\
      --template templates/realtor.html \\
      --name "Sarah Johnson Realty" \\
      --phone "(555) 987-6543" \\
      --city "Denver" --state "CO" \\
      --extra "BROKERAGE_NAME=Keller Williams" "TOTAL_SOLD=340" \\
      --output output/sarah-johnson.html
        """,
    )

    parser.add_argument("--template", "-t", required=True, help="Path to template HTML file")
    parser.add_argument("--name", "-n", help="Business name")
    parser.add_argument("--phone", "-p", help="Business phone number")
    parser.add_argument("--address", "-a", help="Street address")
    parser.add_argument("--city", "-c", help="City")
    parser.add_argument("--state", "-s", help="State (2-letter code)")
    parser.add_argument("--zip", "-z", help="ZIP code")
    parser.add_argument("--email", "-e", help="Business email")
    parser.add_argument("--years", help="Years in business")
    parser.add_argument("--rating", help="Google rating (e.g., 4.9)")
    parser.add_argument("--reviews", help="Number of Google reviews")
    parser.add_argument("--license", help="License number")
    parser.add_argument("--extra", nargs="*", help="Extra key=value pairs (e.g., BROKERAGE_NAME='Keller Williams')")
    parser.add_argument("--output", "-o", help="Output file path (single mode)")
    parser.add_argument("--csv", help="CSV file with business data (batch mode)")
    parser.add_argument("--output-dir", help="Output directory (batch mode)")

    args = parser.parse_args()

    # Validate template exists
    if not os.path.isfile(args.template):
        print(f"Error: Template not found: {args.template}", file=sys.stderr)
        sys.exit(1)

    # Batch mode
    if args.csv:
        if not os.path.isfile(args.csv):
            print(f"Error: CSV file not found: {args.csv}", file=sys.stderr)
            sys.exit(1)
        output_dir = args.output_dir or "output"
        process_batch(args.template, args.csv, output_dir)
        return

    # Single mode
    if not args.output:
        # Auto-generate output path
        if args.name:
            slug = slugify(args.name)
            template_name = Path(args.template).stem
            args.output = f"output/{template_name}-{slug}.html"
        else:
            print("Error: Provide --output path or --name for auto-naming.", file=sys.stderr)
            sys.exit(1)

    replacements = build_replacements_from_args(args)
    process_single(args.template, replacements, args.output)
    print(f"\nDone. Open in browser: file://{os.path.abspath(args.output)}")


if __name__ == "__main__":
    main()
