#!/usr/bin/env python3
"""
PRINTMAXX Personalized Demo Generator
======================================
Generates personalized landing pages for hot leads by injecting their
business name, phone, city, and address into industry-specific templates.

Usage:
    python3 AUTOMATIONS/personalize_demos.py --top 50
    python3 AUTOMATIONS/personalize_demos.py --top 10 --category dentist --dry-run
    python3 AUTOMATIONS/personalize_demos.py --all --deploy
"""

import csv
import re
import argparse
import shutil
from pathlib import Path
from datetime import datetime

BASE = Path(__file__).resolve().parent.parent
HOT_LEADS = BASE / "AUTOMATIONS" / "leads" / "qualified" / "HOT_LEADS_QUALIFIED.csv"
TEMPLATES_DIR = BASE / "MONEY_METHODS" / "LOCAL_BIZ" / "templates"
OUTPUT_DIR = BASE / "output" / "personalized_demos"

# Category → template mapping
CATEGORY_MAP = {
    "dentist": "dental.html",
    "cosmetic_dentist": "dental.html",
    "orthodontist": "dental.html",
    "general_dentistry": "dental.html",
    "pediatric_dentist": "dental.html",
    "real_estate_agent": "realtor.html",
    "lawyer": "legal.html",
    "civil_rights_lawyers": "legal.html",
    "legal_services": "legal.html",
    "spanish_restaurant": "restaurant.html",
    "restaurant": "restaurant.html",
    "fast_food_restaurant": "restaurant.html",
    "pizza_restaurant": "restaurant.html",
    "mexican_restaurant": "restaurant.html",
    "american_restaurant": "restaurant.html",
    "italian_restaurant": "restaurant.html",
    "chinese_restaurant": "restaurant.html",
    "seafood_restaurant": "restaurant.html",
    "barbecue_restaurant": "restaurant.html",
    "bar_and_grill_restaurant": "restaurant.html",
    "chicken_restaurant": "restaurant.html",
    "breakfast_and_brunch_restaurant": "restaurant.html",
    "burger_restaurant": "restaurant.html",
    "cafe": "restaurant.html",
    "gym": "fitness.html",
    "chiropractor": "fitness.html",
    "veterinarian": "dental.html",  # closest match (care practice)
    "plumbing": "plumber.html",
    "plumber": "plumber.html",
    "beauty_salon": "fitness.html",
    "hair_salon": "fitness.html",
    "nail_salon": "fitness.html",
    "accountant": "legal.html",
}

# Placeholder values in each template to replace
TEMPLATE_PLACEHOLDERS = {
    "dental.html": {
        "business_name": "Bright Smile Family Dental",
        "phone": "(512) 555-0142",
        "address": "2847 Lakewood Dr, Austin, TX 78704",
        "city_state": "Austin, TX",
        "title_suffix": "Family & Cosmetic Dentistry",
    },
    "realtor.html": {
        "business_name": "Sarah Martinez Real Estate",
        "phone": "(512) 555-0456",
        "address": "1200 S Lamar Blvd, Austin, TX 78704",
        "city_state": "Austin, TX",
        "city_only": "Austin",
        "title_suffix": "Austin Real Estate Agent",
    },
    "legal.html": {
        "business_name": "Morrison & Associates",
        "phone": "(512) 555-0315",
        "address": "600 Congress Ave Ste 1400, Austin, TX 78701",
        "city_state": "Austin, TX",
        "title_suffix": "Attorneys at Law",
    },
    "restaurant.html": {
        "business_name": "Casa Luna Kitchen & Bar",
        "phone": "(512) 555-0198",
        "address": "415 Congress Ave, Austin, TX 78701",
        "city_state": "Austin, TX",
        "title_suffix": "Restaurant",
    },
    "fitness.html": {
        "business_name": "Iron Temple Fitness",
        "phone": "(512) 555-0267",
        "address": "3200 S Congress Ave, Austin, TX 78704",
        "city_state": "Austin, TX",
        "title_suffix": "Fitness & Wellness",
    },
    "plumber.html": {
        "business_name": "FlowRight Plumbing",
        "phone": "(512) 555-0389",
        "address": "8900 N Lamar Blvd, Austin, TX 78753",
        "city_state": "Austin, TX",
        "title_suffix": "Plumbing Services",
    },
}


def slugify(text: str) -> str:
    """Convert text to URL-safe slug."""
    text = text.lower().strip()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[\s_]+', '-', text)
    text = re.sub(r'-+', '-', text)
    return text[:60].rstrip('-')


def load_hot_leads(category: str = None, top: int = None) -> list:
    """Load hot leads sorted by total_score descending (worst sites first)."""
    leads = []
    with open(HOT_LEADS, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            cat = row.get('category', '')
            if category and cat != category:
                continue
            if cat not in CATEGORY_MAP:
                continue
            leads.append(row)

    # Sort by total_score descending (highest score = worst website = best prospect)
    leads.sort(key=lambda r: int(r.get('total_score', 0)), reverse=True)

    if top:
        leads = leads[:top]
    return leads


def personalize_template(template_html: str, template_name: str, lead: dict) -> str:
    """Replace placeholder values with lead's real business data."""
    placeholders = TEMPLATE_PLACEHOLDERS.get(template_name, {})
    if not placeholders:
        return template_html

    biz_name = lead.get('name', 'Local Business')
    phone = lead.get('phone', '')
    address = lead.get('address', '')
    city = lead.get('city', '')
    state = lead.get('state', '')
    zip_code = lead.get('zip', '')

    city_state = f"{city}, {state}" if city and state else city or state
    city_state_zip = f"{city}, {state} {zip_code}".strip() if city else ""
    full_address = f"{address}, {city_state_zip}" if address else city_state_zip

    html = template_html

    # Replace business name (all occurrences)
    if placeholders.get("business_name"):
        html = html.replace(placeholders["business_name"], biz_name)

    # Replace phone
    if placeholders.get("phone") and phone:
        html = html.replace(placeholders["phone"], phone)

    # Replace full address
    if placeholders.get("address") and full_address:
        html = html.replace(placeholders["address"], full_address)

    # Replace city, state
    if placeholders.get("city_state") and city_state:
        html = html.replace(placeholders["city_state"], city_state)

    # Replace city only (for realtor template)
    if placeholders.get("city_only") and city:
        html = html.replace(placeholders["city_only"], city)

    # Update demo banner
    old_banner_pattern = r'DEMO — Custom design for \w+ practices?\.'
    new_banner = f'Custom preview for {biz_name}. Interested? Reply to the email that brought you here.'
    html = re.sub(old_banner_pattern, new_banner, html)

    # Also catch other demo banner patterns
    html = html.replace(
        'DEMO — Custom design for dental practices.',
        f'Custom preview for {biz_name}. Interested? Reply to the email that brought you here.'
    )
    html = html.replace(
        'DEMO — Custom design for',
        f'Custom preview for {biz_name}. Reply to'
    )

    # Update title tag
    if placeholders.get("title_suffix"):
        old_title = f'{placeholders["business_name"]} — {placeholders["title_suffix"]}'
        cat_label = lead.get('category', '').replace('_', ' ').title()
        new_title = f'{biz_name} — {cat_label} in {city_state}'
        html = html.replace(old_title, new_title)

    return html


def generate_demos(leads: list, dry_run: bool = False) -> list:
    """Generate personalized demos for leads. Returns manifest entries."""
    manifest = []
    templates_cache = {}

    for lead in leads:
        cat = lead.get('category', '')
        template_name = CATEGORY_MAP.get(cat)
        if not template_name:
            continue

        template_path = TEMPLATES_DIR / template_name
        if not template_path.exists():
            continue

        # Cache templates
        if template_name not in templates_cache:
            templates_cache[template_name] = template_path.read_text(encoding='utf-8')

        biz_name = lead.get('name', 'Unknown')
        city = lead.get('city', '')
        slug = slugify(f"{biz_name}-{city}")

        if not slug:
            continue

        entry = {
            "slug": slug,
            "business_name": biz_name,
            "category": cat,
            "template": template_name,
            "city": city,
            "state": lead.get('state', ''),
            "phone": lead.get('phone', ''),
            "total_score": lead.get('total_score', ''),
            "demo_path": f"{slug}/index.html",
        }
        manifest.append(entry)

        if dry_run:
            continue

        # Generate personalized HTML
        html = personalize_template(templates_cache[template_name], template_name, lead)

        # Write to output directory
        out_dir = OUTPUT_DIR / slug
        out_dir.mkdir(parents=True, exist_ok=True)
        (out_dir / "index.html").write_text(html, encoding='utf-8')

    return manifest


def write_manifest(manifest: list):
    """Write manifest CSV."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    manifest_path = OUTPUT_DIR / "MANIFEST.csv"
    fieldnames = ["slug", "business_name", "category", "template", "city", "state", "phone", "total_score", "demo_path"]
    with open(manifest_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(manifest)
    return manifest_path


def main():
    parser = argparse.ArgumentParser(description="Generate personalized demo sites for hot leads")
    parser.add_argument('--top', type=int, default=200, help='Generate for top N leads (default: 200)')
    parser.add_argument('--category', type=str, help='Only generate for specific category')
    parser.add_argument('--dry-run', action='store_true', help='Show what would be generated')
    parser.add_argument('--all', action='store_true', help='Generate for ALL hot leads')
    parser.add_argument('--deploy', action='store_true', help='Deploy to surge.sh after generating')
    parser.add_argument('--clean', action='store_true', help='Remove existing demos before generating')
    args = parser.parse_args()

    top = None if args.all else args.top

    print(f"Loading hot leads...")
    leads = load_hot_leads(category=args.category, top=top)
    print(f"  {len(leads)} leads to process")

    if args.clean and OUTPUT_DIR.exists():
        shutil.rmtree(OUTPUT_DIR)
        print(f"  Cleaned {OUTPUT_DIR}")

    print(f"Generating personalized demos{'(dry-run)' if args.dry_run else ''}...")
    manifest = generate_demos(leads, dry_run=args.dry_run)

    if not args.dry_run:
        manifest_path = write_manifest(manifest)
        print(f"\n  {len(manifest)} personalized demos generated")
        print(f"  Output: {OUTPUT_DIR}")
        print(f"  Manifest: {manifest_path}")

        # Show category breakdown
        from collections import Counter
        cats = Counter(e['category'] for e in manifest)
        print(f"\n  By category:")
        for cat, count in cats.most_common():
            print(f"    {count:>5}  {cat}")
    else:
        print(f"\n  Would generate {len(manifest)} personalized demos")
        for entry in manifest[:10]:
            print(f"    {entry['slug']} ({entry['category']}, {entry['city']} {entry['state']})")
        if len(manifest) > 10:
            print(f"    ... and {len(manifest) - 10} more")

    if args.deploy and not args.dry_run:
        import subprocess
        print(f"\nDeploying to surge.sh...")
        result = subprocess.run(
            ["npx", "surge", str(OUTPUT_DIR), "printmaxx-demos.surge.sh"],
            capture_output=True, text=True, timeout=120
        )
        if result.returncode == 0:
            print(f"  Deployed to https://printmaxx-demos.surge.sh")
        else:
            print(f"  Deploy failed: {result.stderr[:200]}")


if __name__ == "__main__":
    main()
