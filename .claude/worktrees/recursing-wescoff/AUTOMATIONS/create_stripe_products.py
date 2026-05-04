#!/usr/bin/env python3
"""
create_stripe_products.py — Create Stripe products, prices, and payment links
for PRINTMAXX digital products that are missing them.

Usage:
    python3 AUTOMATIONS/create_stripe_products.py
    python3 AUTOMATIONS/create_stripe_products.py --dry-run
    python3 AUTOMATIONS/create_stripe_products.py --status
"""

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
LOG_DIR = PROJECT_ROOT / "AUTOMATIONS" / "logs"
STRIPE_PRODUCTS_MD = PROJECT_ROOT / "OPS" / "STRIPE_PRODUCTS.md"
RESULTS_JSON = PROJECT_ROOT / "AUTOMATIONS" / "agent" / "stripe_digital_products.json"


def safe_path(target: Path) -> Path:
    """Verify path is within project root. Raises ValueError if not."""
    resolved = Path(target).resolve()
    if not str(resolved).startswith(str(PROJECT_ROOT)):
        raise ValueError(f"BLOCKED: {resolved} is outside project root {PROJECT_ROOT}")
    return resolved


def load_env() -> str:
    """Load STRIPE_SECRET_KEY from .env file or environment."""
    env_file = PROJECT_ROOT / ".env"
    if env_file.exists():
        for line in env_file.read_text().splitlines():
            line = line.strip()
            if line.startswith("STRIPE_SECRET_KEY=") and not line.startswith("#"):
                key = line.split("=", 1)[1].strip().strip('"').strip("'")
                if key:
                    return key
    # Fall back to actual environment
    key = os.environ.get("STRIPE_SECRET_KEY", "")
    if key:
        return key
    return ""


# Product definitions: (name, description, price_cents, currency)
PRODUCTS = [
    {
        "name": "Funnel Teardown Pack",
        "description": (
            "Real funnel teardowns from 7-figure operators. "
            "Copy their structure, skip the trial and error."
        ),
        "price_cents": 3900,
        "currency": "usd",
    },
    {
        "name": "Reddit Money Machine",
        "description": (
            "Step-by-step system to turn Reddit communities into a consistent "
            "traffic and revenue source. No ads required."
        ),
        "price_cents": 2900,
        "currency": "usd",
    },
    {
        "name": "Prompt Engineering Vault",
        "description": (
            "300+ battle-tested prompts for solopreneurs: content creation, "
            "sales copy, customer research, and product development."
        ),
        "price_cents": 2700,
        "currency": "usd",
    },
    {
        "name": "Claude Code Mastery: Ship Apps in 48 Hours",
        "description": (
            "Build and deploy a working web app in 48 hours using Claude Code. "
            "No prior coding experience required."
        ),
        "price_cents": 4700,
        "currency": "usd",
    },
    {
        "name": "50 Viral Tweet Templates",
        "description": (
            "50 fill-in-the-blank tweet templates proven to drive engagement "
            "for solopreneurs, builders, and indie hackers."
        ),
        "price_cents": 1900,
        "currency": "usd",
    },
    {
        "name": "Solo Launch Checklist Pack",
        "description": (
            "The exact pre-launch, launch-day, and post-launch checklists "
            "used to ship 100+ digital products solo."
        ),
        "price_cents": 900,
        "currency": "usd",
    },
    {
        "name": "Cold Email Playbook: SaaS Edition",
        "description": (
            "Cold email sequences, subject line formulas, and follow-up cadences "
            "built specifically for SaaS founders doing outbound."
        ),
        "price_cents": 2900,
        "currency": "usd",
    },
]


def log(msg: str) -> None:
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{ts}] {msg}")


def create_all_products(dry_run: bool = False) -> list[dict]:
    import stripe  # noqa: PLC0415

    key = load_env()
    if not key:
        log("ERROR: STRIPE_SECRET_KEY not found in .env or environment")
        sys.exit(1)

    stripe.api_key = key
    mode_label = "[DRY-RUN] " if dry_run else ""

    results = []
    log(f"{mode_label}Creating {len(PRODUCTS)} Stripe products...")

    for prod_def in PRODUCTS:
        name = prod_def["name"]
        desc = prod_def["description"]
        price_cents = prod_def["price_cents"]
        currency = prod_def["currency"]
        price_display = f"${price_cents // 100}"

        log(f"  {mode_label}Processing: {name} ({price_display})")

        if dry_run:
            results.append(
                {
                    "name": name,
                    "description": desc,
                    "price_cents": price_cents,
                    "product_id": "prod_DRY_RUN",
                    "price_id": "price_DRY_RUN",
                    "payment_link": "https://buy.stripe.com/DRY_RUN",
                    "dry_run": True,
                }
            )
            log(f"    [DRY-RUN] Would create product + price + payment link")
            continue

        try:
            # 1. Create product
            product = stripe.Product.create(
                name=name,
                description=desc,
                metadata={"source": "printmaxx", "type": "digital_product"},
            )
            product_id = product["id"]
            log(f"    Product created: {product_id}")

            # 2. Create price
            price = stripe.Price.create(
                product=product_id,
                unit_amount=price_cents,
                currency=currency,
            )
            price_id = price["id"]
            log(f"    Price created: {price_id}")

            # 3. Create payment link
            payment_link = stripe.PaymentLink.create(
                line_items=[{"price": price_id, "quantity": 1}],
            )
            link_url = payment_link["url"]
            log(f"    Payment link: {link_url}")

            results.append(
                {
                    "name": name,
                    "description": desc,
                    "price_cents": price_cents,
                    "price_display": price_display,
                    "product_id": product_id,
                    "price_id": price_id,
                    "payment_link": link_url,
                    "created_at": datetime.now().isoformat(),
                }
            )

        except Exception as exc:
            log(f"    ERROR creating {name}: {exc}")
            results.append(
                {
                    "name": name,
                    "error": str(exc),
                    "price_cents": price_cents,
                }
            )

    return results


def save_results(results: list[dict]) -> None:
    """Persist JSON results and append to OPS/STRIPE_PRODUCTS.md."""
    LOG_DIR.mkdir(parents=True, exist_ok=True)

    # Save JSON
    json_path = safe_path(RESULTS_JSON)
    json_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(results, indent=2))
    log(f"JSON saved: {json_path}")

    # Append to STRIPE_PRODUCTS.md
    md_path = safe_path(STRIPE_PRODUCTS_MD)
    successful = [r for r in results if "payment_link" in r and not r.get("dry_run")]
    if not successful:
        log("No successful products to append to STRIPE_PRODUCTS.md")
        return

    today = datetime.now().strftime("%Y-%m-%d")
    lines = [
        f"\n## Digital Products Batch — {today}",
        "| Product | Price | Stripe Product ID | Stripe Price ID | Payment Link |",
        "|---------|-------|-------------------|-----------------|--------------|",
    ]
    for r in successful:
        price_display = r.get("price_display", f"${r['price_cents'] // 100}")
        lines.append(
            f"| {r['name']} | {price_display} | {r['product_id']} "
            f"| {r['price_id']} | {r['payment_link']} |"
        )

    current = md_path.read_text()
    # Update "Last updated" date in header
    updated_content = "\n".join(
        line if not line.startswith("Last updated:") else f"Last updated: {today}"
        for line in current.splitlines()
    )
    updated_content += "\n" + "\n".join(lines) + "\n"
    md_path.write_text(updated_content)
    log(f"Appended {len(successful)} products to {md_path}")


def print_summary(results: list[dict]) -> None:
    ok = [r for r in results if "payment_link" in r and not r.get("error")]
    errors = [r for r in results if "error" in r]

    print("\n" + "=" * 60)
    print("RESULTS SUMMARY")
    print("=" * 60)
    for r in ok:
        dry = " [DRY-RUN]" if r.get("dry_run") else ""
        price = r.get("price_display", f"${r['price_cents'] // 100}")
        print(f"\n{r['name']} ({price}){dry}")
        print(f"  Product ID:   {r['product_id']}")
        print(f"  Price ID:     {r['price_id']}")
        print(f"  Payment Link: {r['payment_link']}")

    if errors:
        print(f"\nFAILED ({len(errors)}):")
        for e in errors:
            print(f"  {e['name']}: {e.get('error', 'unknown')}")

    print(f"\nTotal: {len(ok)} created, {len(errors)} failed")
    print("=" * 60)


def status_check() -> None:
    """Show what products are already in STRIPE_PRODUCTS.md."""
    md_path = safe_path(STRIPE_PRODUCTS_MD)
    if not md_path.exists():
        print("OPS/STRIPE_PRODUCTS.md not found")
        return

    content = md_path.read_text()
    target_names = [p["name"].lower() for p in PRODUCTS]

    print("\nStatus check — target products vs existing records:")
    for prod in PRODUCTS:
        found = prod["name"].lower() in content.lower()
        status = "FOUND" if found else "MISSING"
        price = f"${prod['price_cents'] // 100}"
        print(f"  [{status:7s}] {prod['name']} ({price})")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Create Stripe products/prices/payment links for PRINTMAXX digital products"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Simulate without making API calls",
    )
    parser.add_argument(
        "--status",
        action="store_true",
        help="Show which target products already exist in STRIPE_PRODUCTS.md",
    )
    args = parser.parse_args()

    if args.status:
        status_check()
        return

    results = create_all_products(dry_run=args.dry_run)
    print_summary(results)

    if not args.dry_run:
        save_results(results)


if __name__ == "__main__":
    main()
