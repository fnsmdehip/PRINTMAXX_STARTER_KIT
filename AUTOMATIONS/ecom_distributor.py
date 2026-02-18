#!/usr/bin/env python3
"""
PRINTMAXX Ecom Multi-Platform Distributor — One product → 10+ platforms

Takes a product spec and generates platform-ready listings for:
  Gumroad, Etsy, Redbubble, Creative Market, Gumroad, eBay, Amazon KDP,
  Lemon Squeezy, Whop, Payhip, Ko-fi, Sellfy, Notion Marketplace

Usage:
    python3 AUTOMATIONS/ecom_distributor.py --list                      # Show ready products
    python3 AUTOMATIONS/ecom_distributor.py --distribute PRODUCT_ID     # Distribute one product
    python3 AUTOMATIONS/ecom_distributor.py --distribute-all            # Distribute everything
    python3 AUTOMATIONS/ecom_distributor.py --platforms                 # Show platform status
    python3 AUTOMATIONS/ecom_distributor.py --generate-csv PRODUCT_ID   # Generate upload CSVs
    python3 AUTOMATIONS/ecom_distributor.py --affiliate-networks        # Show affiliate networks
    python3 AUTOMATIONS/ecom_distributor.py --status                    # Distribution status
"""

import os
import sys
import csv
import json
from datetime import datetime
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
PRODUCTS_DIR = BASE / "PRODUCTS"
DIGITAL_DIR = BASE / "DIGITAL_PRODUCTS"
LEDGER = BASE / "LEDGER"
OUTPUT_DIR = BASE / "output" / "ecom_distribution"
LOG_DIR = BASE / "AUTOMATIONS" / "logs"


PLATFORMS = {
    "gumroad": {
        "name": "Gumroad", "type": "digital", "fee": "10%",
        "url": "https://gumroad.com", "signup": "https://gumroad.com/signup",
        "accepts": ["ebooks", "templates", "courses", "software", "art", "music"],
        "listing_fields": ["name", "price", "description", "cover_url", "tags", "category"],
        "notes": "Instant payout. Best for digital products. No monthly fee."
    },
    "etsy": {
        "name": "Etsy", "type": "digital+physical", "fee": "$0.20/listing + 6.5%",
        "url": "https://etsy.com", "signup": "https://www.etsy.com/sell",
        "accepts": ["templates", "printables", "art", "POD", "handmade", "vintage"],
        "listing_fields": ["title", "description", "price", "tags", "category", "images"],
        "notes": "High traffic. SEO matters. 13 tags per listing."
    },
    "redbubble": {
        "name": "Redbubble", "type": "POD", "fee": "artist sets margin",
        "url": "https://redbubble.com", "signup": "https://www.redbubble.com/signup",
        "accepts": ["art", "designs", "illustrations"],
        "listing_fields": ["title", "description", "tags", "design_image"],
        "notes": "Upload design, they handle printing/shipping. Set 20%+ margin."
    },
    "creative_market": {
        "name": "Creative Market", "type": "digital", "fee": "40% commission",
        "url": "https://creativemarket.com", "signup": "https://creativemarket.com/sell",
        "accepts": ["fonts", "templates", "graphics", "themes", "photos"],
        "listing_fields": ["name", "price", "description", "category", "tags", "preview_images"],
        "notes": "Premium marketplace. Higher prices ($15-50+). Apply to sell."
    },
    "lemon_squeezy": {
        "name": "Lemon Squeezy", "type": "digital", "fee": "5% + $0.50",
        "url": "https://lemonsqueezy.com", "signup": "https://app.lemonsqueezy.com/register",
        "accepts": ["software", "ebooks", "courses", "subscriptions"],
        "listing_fields": ["name", "price", "description", "category"],
        "notes": "Lower fees than Gumroad. Good for SaaS/subscriptions."
    },
    "whop": {
        "name": "Whop", "type": "digital+community", "fee": "3-5%",
        "url": "https://whop.com", "signup": "https://whop.com/sell",
        "accepts": ["courses", "communities", "software", "templates", "bots"],
        "listing_fields": ["name", "price", "description", "category", "access_type"],
        "notes": "Great for community/membership products. Growing marketplace."
    },
    "payhip": {
        "name": "Payhip", "type": "digital", "fee": "5% (free plan)",
        "url": "https://payhip.com", "signup": "https://payhip.com/auth/register",
        "accepts": ["ebooks", "courses", "software", "memberships", "coaching"],
        "listing_fields": ["name", "price", "description", "category"],
        "notes": "Free plan available. 0% fee on Plus plan ($99/mo)."
    },
    "ko_fi": {
        "name": "Ko-fi", "type": "digital+tips", "fee": "0% (Gold: $6/mo)",
        "url": "https://ko-fi.com", "signup": "https://ko-fi.com/account/register",
        "accepts": ["art", "templates", "commissions", "memberships"],
        "listing_fields": ["name", "price", "description", "category"],
        "notes": "0% fee is huge. Good for smaller products and memberships."
    },
    "sellfy": {
        "name": "Sellfy", "type": "digital+POD", "fee": "from $22/mo",
        "url": "https://sellfy.com", "signup": "https://sellfy.com/signup",
        "accepts": ["digital", "POD", "subscriptions", "physical"],
        "listing_fields": ["name", "price", "description", "category", "images"],
        "notes": "All-in-one store. POD integration built in."
    },
    "amazon_kdp": {
        "name": "Amazon KDP", "type": "books", "fee": "30-65% royalty",
        "url": "https://kdp.amazon.com", "signup": "https://kdp.amazon.com/signup",
        "accepts": ["ebooks", "paperbacks", "journals", "planners"],
        "listing_fields": ["title", "subtitle", "description", "keywords", "categories", "price", "manuscript", "cover"],
        "notes": "Massive audience. 70% royalty on $2.99-$9.99 ebooks."
    },
    "notion_marketplace": {
        "name": "Notion Marketplace", "type": "templates", "fee": "varies",
        "url": "https://notion.so/templates", "signup": "https://notion.so/become-a-creator",
        "accepts": ["notion_templates"],
        "listing_fields": ["name", "description", "price", "preview_url", "template_url"],
        "notes": "Growing marketplace. Apply to become a creator."
    },
}

AFFILIATE_NETWORKS = {
    "shareasale": {"name": "ShareASale", "url": "https://shareasale.com", "type": "general",
                   "signup": "https://www.shareasale.com/newsignup.cfm", "min_payout": "$50"},
    "cj": {"name": "CJ Affiliate", "url": "https://cj.com", "type": "general",
            "signup": "https://signup.cj.com/member/signup/publisher/", "min_payout": "$50"},
    "impact": {"name": "Impact", "url": "https://impact.com", "type": "general",
               "signup": "https://app.impact.com/signup", "min_payout": "$25"},
    "amazon_associates": {"name": "Amazon Associates", "url": "https://affiliate-program.amazon.com",
                          "type": "ecom", "signup": "https://affiliate-program.amazon.com/signup",
                          "min_payout": "$10"},
    "rakuten": {"name": "Rakuten", "url": "https://rakutenadvertising.com", "type": "general",
                "signup": "https://rakutenadvertising.com/publisher-sign-up/", "min_payout": "$50"},
    "awin": {"name": "Awin", "url": "https://awin.com", "type": "general",
             "signup": "https://www.awin.com/us/publishers/sign-up", "min_payout": "$20"},
    "partnerstack": {"name": "PartnerStack", "url": "https://partnerstack.com", "type": "saas",
                     "signup": "https://partnerstack.com/partners", "min_payout": "$5"},
    "flexoffers": {"name": "FlexOffers", "url": "https://flexoffers.com", "type": "general",
                   "signup": "https://publisherpro.flexoffers.com/signup", "min_payout": "$25"},
}


def read_csv(path, max_rows=500):
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            return [row for i, row in enumerate(csv.DictReader(f)) if i < max_rows]
    except Exception:
        return []


def get_products():
    """Gather all ready-to-distribute products."""
    products = []

    # Gumroad listings
    gumroad_file = PRODUCTS_DIR / "GUMROAD_READY_LISTINGS.md"
    if gumroad_file.exists():
        products.append({
            "id": "PROD_GUMROAD_BUNDLE", "name": "Gumroad Digital Products (10)",
            "type": "digital", "source": str(gumroad_file),
            "platforms": ["gumroad", "lemon_squeezy", "payhip", "whop", "ko_fi", "sellfy"],
            "count": 10, "status": "READY"
        })

    # Etsy listings
    etsy_file = PRODUCTS_DIR / "ECOM_LISTINGS_READY" / "ETSY_LISTINGS_COMPLETE.md"
    if etsy_file.exists():
        products.append({
            "id": "PROD_ETSY_BUNDLE", "name": "Etsy Listings (Complete)",
            "type": "digital+physical", "source": str(etsy_file),
            "platforms": ["etsy", "redbubble", "creative_market"],
            "count": 20, "status": "READY"
        })

    # POD designs
    pod_file = PRODUCTS_DIR / "POD_DESIGNS_50.md"
    if pod_file.exists():
        products.append({
            "id": "PROD_POD_50", "name": "POD Designs (50)",
            "type": "POD", "source": str(pod_file),
            "platforms": ["redbubble", "etsy", "sellfy"],
            "count": 50, "status": "READY"
        })

    # KDP journals
    kdp_file = PRODUCTS_DIR / "KDP_JOURNALS_10.md"
    if kdp_file.exists():
        products.append({
            "id": "PROD_KDP_10", "name": "KDP Journals/Planners (10)",
            "type": "books", "source": str(kdp_file),
            "platforms": ["amazon_kdp"],
            "count": 10, "status": "READY"
        })

    # Digital products directory
    if DIGITAL_DIR.exists():
        for f in DIGITAL_DIR.glob("*.md"):
            products.append({
                "id": f"PROD_{f.stem.upper()}", "name": f.stem.replace("_", " ").title(),
                "type": "digital", "source": str(f),
                "platforms": ["gumroad", "lemon_squeezy", "payhip", "ko_fi"],
                "count": 1, "status": "READY"
            })

    # Fiverr gigs (services)
    fiverr_file = PRODUCTS_DIR / "FREELANCE_LISTINGS_READY" / "FIVERR_GIGS_10.md"
    if fiverr_file.exists():
        products.append({
            "id": "PROD_FIVERR_10", "name": "Fiverr Gigs (10 services)",
            "type": "service", "source": str(fiverr_file),
            "platforms": ["fiverr"],
            "count": 10, "status": "READY"
        })

    # Upwork profiles
    upwork_file = PRODUCTS_DIR / "FREELANCE_LISTINGS_READY" / "UPWORK_PROFILES_5.md"
    if upwork_file.exists():
        products.append({
            "id": "PROD_UPWORK_5", "name": "Upwork Profiles (5)",
            "type": "service", "source": str(upwork_file),
            "platforms": ["upwork"],
            "count": 5, "status": "READY"
        })

    return products


def get_account_status():
    """Check which platform accounts are created."""
    rows = read_csv(LEDGER / "ACCOUNTS.csv")
    active = {}
    for r in rows:
        platform = (r.get("Platform") or r.get("platform") or "").strip().lower()
        status = (r.get("Status") or r.get("status") or "").strip().upper()
        if platform:
            active[platform] = status in ("CREATED", "ACTIVE", "WARMED")
    return active


def print_products():
    """List all ready products with distribution targets."""
    products = get_products()
    accounts = get_account_status()

    print(f"\n{'='*70}")
    print(f"  READY-TO-DISTRIBUTE PRODUCTS — {datetime.now().strftime('%Y-%m-%d')}")
    print(f"{'='*70}\n")

    total_listings = 0
    for p in products:
        ready_platforms = []
        blocked_platforms = []
        for plat in p.get("platforms", []):
            if accounts.get(plat, False) or accounts.get(PLATFORMS.get(plat, {}).get("name", "").lower(), False):
                ready_platforms.append(plat)
            else:
                blocked_platforms.append(plat)

        status = "READY" if ready_platforms else "BLOCKED"
        total = p["count"] * len(p.get("platforms", []))
        total_listings += total

        print(f"  {p['id']}: {p['name']}")
        print(f"    Type: {p['type']} | Items: {p['count']} | Total listings: {total}")
        print(f"    Platforms: {', '.join(p.get('platforms', []))}")
        if blocked_platforms:
            print(f"    BLOCKED (no account): {', '.join(blocked_platforms)}")
        print(f"    Source: {os.path.relpath(p['source'], BASE)}")
        print()

    print(f"{'─'*70}")
    print(f"  TOTAL: {len(products)} product bundles → {total_listings} potential listings")
    print(f"{'='*70}\n")


def print_platforms():
    """Show all platforms with status."""
    accounts = get_account_status()

    print(f"\n{'='*70}")
    print(f"  DISTRIBUTION PLATFORMS")
    print(f"{'='*70}\n")

    for pid, p in PLATFORMS.items():
        has_account = accounts.get(pid, False) or accounts.get(p["name"].lower(), False)
        status = "ACTIVE" if has_account else "NEEDS ACCOUNT"
        marker = "+" if has_account else "x"

        print(f"  [{marker}] {p['name']:<20} Fee: {p['fee']:<20} Status: {status}")
        print(f"      Accepts: {', '.join(p['accepts'][:4])}")
        print(f"      Signup: {p['signup']}")
        print()

    print(f"{'='*70}\n")


def print_affiliate_networks():
    """Show affiliate networks for product distribution."""
    print(f"\n{'='*70}")
    print(f"  AFFILIATE NETWORKS FOR DISTRIBUTION")
    print(f"{'='*70}\n")

    for nid, n in AFFILIATE_NETWORKS.items():
        print(f"  {n['name']:<20} Type: {n['type']:<10} Min payout: {n['min_payout']}")
        print(f"      Signup: {n['signup']}")
        print()

    print(f"  STRATEGY: Sign up for ALL networks. List products as affiliate offers.")
    print(f"  Others promote YOUR products. You pay commission only on sales.")
    print(f"{'='*70}\n")


def distribute_product(product_id):
    """Generate platform-specific listings for a product."""
    products = get_products()
    product = next((p for p in products if p["id"] == product_id), None)

    if not product:
        print(f"Product not found: {product_id}")
        print(f"Available: {', '.join(p['id'] for p in products)}")
        return

    accounts = get_account_status()
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    print(f"\n{'='*60}")
    print(f"  DISTRIBUTING: {product['name']}")
    print(f"{'='*60}\n")

    for plat_id in product.get("platforms", []):
        plat = PLATFORMS.get(plat_id, {})
        has_account = accounts.get(plat_id, False) or accounts.get(plat.get("name", "").lower(), False)

        if has_account:
            print(f"  [{plat.get('name', plat_id)}] READY — account active")
            print(f"    → Copy listings from: {os.path.relpath(product['source'], BASE)}")
            print(f"    → Fields needed: {', '.join(plat.get('listing_fields', []))}")
        else:
            print(f"  [{plat.get('name', plat_id)}] BLOCKED — create account first")
            print(f"    → Signup: {plat.get('signup', 'N/A')}")
        print()

    # Generate upload CSV
    csv_path = OUTPUT_DIR / f"{product_id}_distribution.csv"
    with open(csv_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["platform", "product_name", "source_file", "status", "account_ready", "signup_url"])
        for plat_id in product.get("platforms", []):
            plat = PLATFORMS.get(plat_id, {})
            has_account = accounts.get(plat_id, False) or accounts.get(plat.get("name", "").lower(), False)
            writer.writerow([
                plat.get("name", plat_id),
                product["name"],
                os.path.relpath(product["source"], BASE),
                "READY" if has_account else "NEEDS_ACCOUNT",
                "YES" if has_account else "NO",
                plat.get("signup", ""),
            ])

    print(f"  Distribution CSV: {csv_path}")
    print(f"{'='*60}\n")


def distribute_all():
    """Distribute all ready products."""
    products = get_products()
    print(f"Distributing {len(products)} product bundles...\n")
    for p in products:
        distribute_product(p["id"])


def print_status():
    """Print overall distribution status."""
    products = get_products()
    accounts = get_account_status()

    total_products = len(products)
    total_items = sum(p["count"] for p in products)
    total_platforms = len(PLATFORMS)
    active_platforms = sum(1 for pid in PLATFORMS if accounts.get(pid, False))

    total_possible_listings = sum(p["count"] * len(p.get("platforms", [])) for p in products)
    active_listings = sum(
        p["count"] * sum(1 for plat in p.get("platforms", []) if accounts.get(plat, False))
        for p in products
    )

    print(f"\n{'='*60}")
    print(f"  ECOM DISTRIBUTION STATUS — {datetime.now().strftime('%Y-%m-%d')}")
    print(f"{'='*60}")
    print(f"  Products ready: {total_products} bundles ({total_items} items)")
    print(f"  Platforms: {active_platforms}/{total_platforms} active")
    print(f"  Possible listings: {total_possible_listings}")
    print(f"  Listable now: {active_listings} (have accounts)")
    print(f"  Blocked: {total_possible_listings - active_listings} (need accounts)")
    print(f"  Affiliate networks: {len(AFFILIATE_NETWORKS)} available")

    if active_platforms == 0:
        print(f"\n  BOTTLENECK: No platform accounts created yet!")
        print(f"  → Follow OPS/ACCOUNT_CREATION_NOW.md")
        print(f"  → Priority: Stripe → Gumroad → Etsy → Fiverr")

    print(f"{'='*60}\n")


def main():
    args = sys.argv[1:]

    if not args or "--status" in args:
        print_status()
    elif "--list" in args:
        print_products()
    elif "--platforms" in args:
        print_platforms()
    elif "--affiliate-networks" in args:
        print_affiliate_networks()
    elif "--distribute" in args:
        idx = args.index("--distribute")
        if idx + 1 < len(args):
            distribute_product(args[idx + 1])
        else:
            print("Usage: --distribute PRODUCT_ID")
    elif "--distribute-all" in args:
        distribute_all()
    elif "--generate-csv" in args:
        idx = args.index("--generate-csv")
        if idx + 1 < len(args):
            distribute_product(args[idx + 1])
        else:
            print("Usage: --generate-csv PRODUCT_ID")
    else:
        print("""
PRINTMAXX Ecom Multi-Platform Distributor

Usage:
    python3 ecom_distributor.py --list                      # Show ready products
    python3 ecom_distributor.py --distribute PRODUCT_ID     # Distribute one product
    python3 ecom_distributor.py --distribute-all            # Distribute everything
    python3 ecom_distributor.py --platforms                 # Show platform status
    python3 ecom_distributor.py --generate-csv PRODUCT_ID   # Generate upload CSVs
    python3 ecom_distributor.py --affiliate-networks        # Show affiliate networks
    python3 ecom_distributor.py --status                    # Distribution status
""")


if __name__ == "__main__":
    main()
