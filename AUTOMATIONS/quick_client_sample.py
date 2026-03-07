#!/usr/bin/env python3
"""
Quick Client Sample Builder — OP17 Nuclear Weapon
===================================================
Generates a custom live demo website for a prospect in <5 minutes.
Deploy to surge.sh, send the link, close the deal.

Usage:
  python3 AUTOMATIONS/quick_client_sample.py --type landing --name "Acme Corp" --industry dental
  python3 AUTOMATIONS/quick_client_sample.py --type dashboard --name "Client Inc" --industry fitness
  python3 AUTOMATIONS/quick_client_sample.py --type portfolio --name "John Doe" --industry photography
  python3 AUTOMATIONS/quick_client_sample.py --deploy client-preview  # deploy to surge.sh
  python3 AUTOMATIONS/quick_client_sample.py --list                   # list available templates

Templates: landing, dashboard, portfolio, restaurant, saas, agency
"""

import argparse
import os
import re
import subprocess
import sys
from pathlib import Path
from datetime import datetime

BASE = Path(__file__).resolve().parent.parent
OUTPUT_DIR = BASE / "builds" / "client-samples"


def slugify(text):
    return re.sub(r'[^a-z0-9]+', '-', text.lower()).strip('-')


TEMPLATES = {
    "landing": {
        "name": "SaaS Landing Page",
        "description": "Dark mode, gradient accents, pricing table, testimonials, CTA",
        "base_file": BASE / "builds" / "portfolio" / "landing-page" / "index.html",
    },
    "dashboard": {
        "name": "Analytics Dashboard",
        "description": "Charts, metrics cards, sidebar nav, data tables",
        "base_file": BASE / "builds" / "portfolio" / "dashboard" / "index.html",
    },
    "dental": {
        "name": "Dental Practice Site",
        "description": "Clean medical design, booking CTA, services, team section",
        "base_file": BASE / "MONEY_METHODS" / "LOCAL_BIZ" / "templates" / "dental.html",
    },
    "restaurant": {
        "name": "Restaurant Site",
        "description": "Menu showcase, reservations, gallery, location map",
        "base_file": BASE / "MONEY_METHODS" / "LOCAL_BIZ" / "templates" / "restaurant.html",
    },
    "fitness": {
        "name": "Fitness Studio Site",
        "description": "Class schedule, trainer profiles, membership pricing",
        "base_file": BASE / "MONEY_METHODS" / "LOCAL_BIZ" / "templates" / "fitness.html",
    },
    "legal": {
        "name": "Law Firm Site",
        "description": "Professional design, practice areas, attorney profiles",
        "base_file": BASE / "MONEY_METHODS" / "LOCAL_BIZ" / "templates" / "legal.html",
    },
    "realtor": {
        "name": "Real Estate Agent Site",
        "description": "Property listings, agent bio, market stats, contact form",
        "base_file": BASE / "MONEY_METHODS" / "LOCAL_BIZ" / "templates" / "realtor.html",
    },
    "plumber": {
        "name": "Plumbing Service Site",
        "description": "Emergency CTA, services, service area, reviews",
        "base_file": BASE / "MONEY_METHODS" / "LOCAL_BIZ" / "templates" / "plumber.html",
    },
}


def customize_html(html, client_name, industry):
    """Replace placeholder text with client-specific info."""
    replacements = {
        "Flowstack": client_name,
        "flowstack": slugify(client_name),
        "ShopMetrics": client_name,
        "{{BUSINESS_NAME}}": client_name,
        "{{PHONE}}": "(555) 123-4567",
        "{{EMAIL}}": f"hello@{slugify(client_name)}.com",
        "{{ADDRESS}}": "123 Main Street, Your City",
        "{{CITY}}": "Your City",
    }
    for old, new in replacements.items():
        html = html.replace(old, new)
    return html


def cmd_build(template_type, client_name, industry):
    """Build a customized client sample."""
    if template_type not in TEMPLATES:
        print(f"Unknown template: {template_type}")
        print(f"Available: {', '.join(TEMPLATES.keys())}")
        return None

    tmpl = TEMPLATES[template_type]
    base_file = tmpl["base_file"]

    if not base_file.exists():
        print(f"Template file not found: {base_file}")
        print("Run the template builder first or choose a different template.")
        return None

    # Read base template
    html = base_file.read_text()

    # Customize
    html = customize_html(html, client_name, industry)

    # Output
    slug = slugify(client_name)
    out_dir = OUTPUT_DIR / slug
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / "index.html"
    out_file.write_text(html)

    # Copy any sibling files (CSS, JS)
    for sibling in base_file.parent.iterdir():
        if sibling != base_file and sibling.is_file():
            content = sibling.read_text()
            content = customize_html(content, client_name, industry)
            (out_dir / sibling.name).write_text(content)

    print(f"\nSample built: {out_dir}")
    print(f"  Template: {tmpl['name']}")
    print(f"  Client: {client_name}")
    print(f"  Files: {len(list(out_dir.iterdir()))}")
    print(f"\nDeploy: python3 {__file__} --deploy {slug}")
    print(f"  This will publish to: https://{slug}-preview.surge.sh")

    return out_dir


def cmd_deploy(slug):
    """Deploy a client sample to surge.sh."""
    sample_dir = OUTPUT_DIR / slug
    if not sample_dir.exists():
        print(f"Sample not found: {sample_dir}")
        print(f"Build first: python3 {__file__} --type landing --name 'Client Name'")
        return

    domain = f"{slug}-preview.surge.sh"
    print(f"Deploying {slug} to {domain}...")
    result = subprocess.run(["npx", "surge", ".", domain], cwd=str(sample_dir)).returncode

    if result == 0:
        print(f"\nLIVE: https://{domain}")
        print(f"\nSend this link to the client:")
        print(f"  'hey, built you a live preview. check it out: https://{domain}'")
        print(f"  'if you like the direction, I can customize it fully for $[PRICE].'")
    else:
        print("Deploy failed. Check surge.sh login.")


def cmd_list():
    """List available templates."""
    print("=" * 60)
    print("AVAILABLE TEMPLATES")
    print("=" * 60)

    for tid, tmpl in TEMPLATES.items():
        exists = "YES" if tmpl["base_file"].exists() else "NO"
        print(f"\n  {tid}")
        print(f"    Name:    {tmpl['name']}")
        print(f"    Desc:    {tmpl['description']}")
        print(f"    Ready:   {exists}")

    # Show existing samples
    if OUTPUT_DIR.exists():
        samples = list(OUTPUT_DIR.iterdir())
        if samples:
            print(f"\n{'─' * 60}")
            print(f"BUILT SAMPLES ({len(samples)}):")
            for s in samples:
                if s.is_dir():
                    files = len(list(s.iterdir()))
                    print(f"  {s.name} ({files} files)")


def main():
    parser = argparse.ArgumentParser(description="Quick Client Sample Builder — OP17")
    parser.add_argument("--type", type=str, help="Template type (landing, dashboard, dental, etc.)")
    parser.add_argument("--name", type=str, help="Client/business name")
    parser.add_argument("--industry", type=str, default="general", help="Industry for customization")
    parser.add_argument("--deploy", type=str, help="Deploy a built sample (slug)")
    parser.add_argument("--list", action="store_true", help="List available templates")

    args = parser.parse_args()

    if args.list:
        cmd_list()
    elif args.deploy:
        cmd_deploy(args.deploy)
    elif args.type and args.name:
        cmd_build(args.type, args.name, args.industry)
    else:
        parser.print_help()
        print("\nExamples:")
        print(f"  python3 {__file__} --type landing --name 'Acme Corp'")
        print(f"  python3 {__file__} --type dental --name 'Bright Smiles Dental'")
        print(f"  python3 {__file__} --deploy acme-corp")
        print(f"  python3 {__file__} --list")


if __name__ == "__main__":
    main()
