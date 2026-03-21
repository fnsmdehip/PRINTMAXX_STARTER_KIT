#!/usr/bin/env python3

from __future__ import annotations
"""
PRINTMAXX Arb Listing Generator

Takes profitable products from ECOM_ARB_OPPORTUNITIES.csv and generates
ready-to-post listings for FB Marketplace, eBay, Mercari, Poshmark.

Also generates AliExpress/1688 sourcing links for procurement.

Usage:
    python3 AUTOMATIONS/arb_listing_generator.py --generate          # Generate listings for all profitable products
    python3 AUTOMATIONS/arb_listing_generator.py --platform fb       # FB Marketplace only
    python3 AUTOMATIONS/arb_listing_generator.py --platform ebay     # eBay only
    python3 AUTOMATIONS/arb_listing_generator.py --min-margin 30     # Only products with 30%+ margin
    python3 AUTOMATIONS/arb_listing_generator.py --source            # Generate sourcing/procurement links
"""

import csv
import os
import sys
import json
from datetime import datetime
from pathlib import Path

BASE = Path(__file__).parent.parent
ARB_CSV = BASE / "LEDGER" / "ECOM_ARB_OPPORTUNITIES.csv"
OUTPUT_DIR = BASE / "PRODUCTS" / "ARB_LISTINGS"
SOURCING_DIR = BASE / "PRODUCTS" / "ARB_SOURCING"

# Listing templates by platform
FB_TEMPLATE = """## {product_title}

**Price:** ${sell_price}
**Condition:** New
**Category:** {category}
**Location:** [Your City] (ship nationwide)

### Description
{description}

Free shipping! Brand new, sealed in original packaging.
Ships within 1-2 business days via USPS Priority.

### Tags
{tags}

---
**Source:** {source_url}
**Our cost:** ${total_cost:.2f}
**Net profit:** ${net_profit:.2f} ({margin_pct:.1f}% margin)
**Platform:** FB Marketplace (5% fee)
"""

EBAY_TEMPLATE = """## eBay Listing: {product_title}

**Title (80 char max):** {ebay_title}
**Starting Price:** ${sell_price}
**Buy It Now:** ${sell_price}
**Condition:** New
**Category:** {ebay_category}
**Shipping:** Free (USPS Priority)
**Returns:** 30-day free returns
**Item Specifics:** {item_specifics}

### Description (HTML)
<h2>{product_title}</h2>
<p>{description}</p>
<ul>
<li>Brand new, sealed packaging</li>
<li>Free shipping via USPS Priority Mail</li>
<li>30-day hassle-free returns</li>
<li>Ships within 1 business day</li>
</ul>

---
**Source:** {source_url}
**Our cost:** ${total_cost:.2f} (incl eBay 13.25% + shipping)
**Net profit:** ${net_profit_ebay:.2f} ({margin_pct_ebay:.1f}% margin)
"""

MERCARI_TEMPLATE = """## Mercari Listing: {product_title}

**Price:** ${sell_price}
**Condition:** New
**Category:** {category}
**Shipping:** Free (prepaid label)

### Description
{description}

Brand new! Ships fast.
{tags}

---
**Source:** {source_url}
**Our cost:** ${total_cost:.2f}
**Mercari fee:** 10% = ${mercari_fee:.2f}
**Net profit:** ${net_profit_mercari:.2f}
"""

# Product descriptions and metadata
PRODUCT_DB = {
    "led face mask": {
        "title": "LED Light Therapy Face Mask - 7 Color Red Blue Skin Care Anti-Aging",
        "ebay_title": "LED Light Therapy Face Mask 7 Color Red Blue Anti-Aging Skin Rejuvenation NEW",
        "description": "Professional LED light therapy mask with 7 colors for different skin concerns. Red light for anti-aging and collagen production. Blue light for acne treatment. Green for pigmentation. Use 15-20 minutes daily for visible results in 4-6 weeks.",
        "category": "Beauty & Personal Care",
        "ebay_category": "Health & Beauty > Skin Care > Anti-Aging Products",
        "tags": "led face mask, light therapy, anti-aging, skincare, red light therapy, acne treatment",
        "item_specifics": "Type: LED Mask | Colors: 7 | Power: USB Rechargeable | Material: ABS Plastic",
        "aliexpress_search": "https://www.aliexpress.com/w/wholesale-led-face-mask-7-color.html?sortType=total_tranpro_desc",
        "alibaba_search": "https://www.alibaba.com/trade/search?SearchText=led+face+mask+7+color",
    },
    "yoga mat": {
        "title": "Extra Thick Yoga Mat Non-Slip Exercise Fitness Pilates Workout Pad",
        "ebay_title": "Extra Thick Non-Slip Yoga Mat Exercise Fitness Pilates Gym Workout Pad 72x24 NEW",
        "description": "High-density NBR yoga mat, extra thick for joint protection. Non-slip surface on both sides. Perfect for yoga, pilates, stretching, and floor exercises. Includes carrying strap. 72x24 inches.",
        "category": "Sports & Outdoors",
        "ebay_category": "Sporting Goods > Fitness > Yoga & Pilates > Yoga Mats",
        "tags": "yoga mat, exercise mat, fitness, pilates, gym, non-slip, extra thick",
        "item_specifics": "Type: Yoga Mat | Material: NBR | Thickness: 10mm | Size: 72x24 in",
        "aliexpress_search": "https://www.aliexpress.com/w/wholesale-yoga-mat-thick-nbr.html?sortType=total_tranpro_desc",
        "alibaba_search": "https://www.alibaba.com/trade/search?SearchText=yoga+mat+nbr+thick",
    },
    "pull up bar": {
        "title": "Doorway Pull Up Bar No Screw Installation Home Gym Chin Up",
        "ebay_title": "Doorway Pull Up Bar No Screw Home Gym Chin Up Exercise Fitness Training Bar NEW",
        "description": "Heavy-duty doorway pull up bar, no drilling required. Fits standard door frames 24-36 inches. Padded grips for comfort. Supports up to 300 lbs. Multiple grip positions for pull ups, chin ups, and hanging exercises.",
        "category": "Sports & Outdoors",
        "ebay_category": "Sporting Goods > Fitness > Strength Training > Pull Up Bars",
        "tags": "pull up bar, doorway, home gym, chin up, fitness, no drill",
        "item_specifics": "Type: Pull Up Bar | Installation: Doorway | Max Weight: 300 lbs | Grip: Foam Padded",
        "aliexpress_search": "https://www.aliexpress.com/w/wholesale-doorway-pull-up-bar.html?sortType=total_tranpro_desc",
        "alibaba_search": "https://www.alibaba.com/trade/search?SearchText=doorway+pull+up+bar",
    },
    "ring light": {
        "title": "10 Inch LED Ring Light with Tripod Stand Phone Holder for Video",
        "ebay_title": "10\" LED Ring Light Tripod Stand Phone Holder Video TikTok YouTube Streaming NEW",
        "description": "10-inch LED ring light with adjustable tripod stand and phone holder. 3 color modes (warm/cool/daylight) with 10 brightness levels. USB powered. Perfect for TikTok, YouTube, video calls, and selfies.",
        "category": "Electronics",
        "ebay_category": "Cameras & Photo > Lighting & Studio > Ring Lights",
        "tags": "ring light, LED, tripod, TikTok, YouTube, video, streaming, selfie",
        "item_specifics": "Type: Ring Light | Size: 10 inch | Power: USB | Modes: 3 Color x 10 Brightness",
        "aliexpress_search": "https://www.aliexpress.com/w/wholesale-10-inch-ring-light-tripod.html?sortType=total_tranpro_desc",
        "alibaba_search": "https://www.alibaba.com/trade/search?SearchText=10+inch+ring+light+tripod",
    },
    "resistance bands": {
        "title": "Resistance Bands Set 5 Pack Exercise Bands with Handles for Home Gym",
        "ebay_title": "Resistance Bands Set 5 Pack Exercise Workout Bands Handles Home Gym Fitness NEW",
        "description": "Complete resistance bands set with 5 different resistance levels. Includes 2 handles, 2 ankle straps, door anchor, and carrying bag. Perfect for home workouts, physical therapy, and strength training.",
        "category": "Sports & Outdoors",
        "ebay_category": "Sporting Goods > Fitness > Resistance Bands",
        "tags": "resistance bands, exercise bands, home gym, workout, fitness, strength training",
        "item_specifics": "Type: Resistance Bands | Set Size: 5 Pack | Material: Natural Latex",
        "aliexpress_search": "https://www.aliexpress.com/w/wholesale-resistance-bands-set-5.html?sortType=total_tranpro_desc",
        "alibaba_search": "https://www.alibaba.com/trade/search?SearchText=resistance+bands+set+5",
    },
    "microcurrent device": {
        "title": "Microcurrent Facial Toning Device Anti-Aging Face Lift Skin Tightening",
        "ebay_title": "Microcurrent Facial Device Face Lift Anti-Aging Skin Tightening Toning Tool NEW",
        "description": "Professional microcurrent facial toning device. Uses low-level electrical currents to stimulate facial muscles, improve skin elasticity, and reduce fine lines. USB rechargeable. Use 5 minutes per day.",
        "category": "Beauty & Personal Care",
        "ebay_category": "Health & Beauty > Skin Care > Anti-Aging Products",
        "tags": "microcurrent, facial toning, anti-aging, face lift, skin tightening, beauty device",
        "item_specifics": "Type: Microcurrent Device | Power: USB Rechargeable | Use: 5 min/day",
        "aliexpress_search": "https://www.aliexpress.com/w/wholesale-microcurrent-facial-device.html?sortType=total_tranpro_desc",
        "alibaba_search": "https://www.alibaba.com/trade/search?SearchText=microcurrent+facial+device",
    },
}


def load_arb_data():
    """Load profitable products from CSV"""
    if not ARB_CSV.exists():
        print(f"[!] No arb data found at {ARB_CSV}")
        print("    Run: python3 AUTOMATIONS/ecom_arb_engine.py --scan")
        return []

    products = []
    seen = set()
    with open(ARB_CSV, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            key = row.get('product', '').strip().lower()
            if not key or key in seen:
                continue
            seen.add(key)

            try:
                margin = float(row.get('margin_pct', 0))
                profit = float(row.get('net_profit', 0))
                sell = float(row.get('sell_price', 0))
                source = float(row.get('source_price', 0))
                composite = float(row.get('composite_score', 0) or 0)
            except (ValueError, TypeError):
                continue

            if profit > 0:
                products.append({
                    'product': key,
                    'sell_price': sell,
                    'source_price': source,
                    'net_profit': profit,
                    'margin_pct': margin,
                    'composite_score': composite,
                    'total_cost': sell - profit,
                    'category': row.get('category', 'general'),
                    'best_platform': row.get('best_platform', 'FB Marketplace'),
                    'action': row.get('action', 'WATCH'),
                })

    # Rank by composite score first (if available), then margin and profit.
    products.sort(key=lambda x: (x.get('composite_score', 0), x['margin_pct'], x['net_profit']), reverse=True)
    return products


def calc_platform_fees(sell_price):
    """Calculate fees for each platform"""
    return {
        'fb': sell_price * 0.05,  # FB Marketplace 5%
        'ebay': sell_price * 0.1325 + 0.30,  # eBay 13.25% + $0.30
        'mercari': sell_price * 0.10,  # Mercari 10%
        'poshmark': sell_price * 0.20 if sell_price >= 15 else 2.95,  # Poshmark 20% or flat $2.95
    }


def generate_listings(products, platform_filter=None, min_margin=0, *, top_n=0, action_filter=""):
    """Generate ready-to-post listings"""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    filtered = [p for p in products if p['margin_pct'] >= min_margin]
    if action_filter:
        want = action_filter.strip().upper()
        filtered = [p for p in filtered if str(p.get('action', '')).strip().upper() == want]
    if top_n and top_n > 0:
        filtered = filtered[: int(top_n)]

    if not filtered:
        print(f"[!] No products with margin >= {min_margin}%")
        return

    all_listings = []

    for p in filtered:
        db = PRODUCT_DB.get(p['product'], {})
        if not db:
            # Generate basic listing for unknown products
            db = {
                'title': p['product'].title(),
                'ebay_title': p['product'].title() + ' NEW',
                'description': f"Brand new {p['product']}. Ships fast, free shipping.",
                'category': p['category'].title(),
                'ebay_category': p['category'].title(),
                'tags': p['product'].replace(' ', ', '),
                'item_specifics': f"Type: {p['product'].title()} | Condition: New",
                'aliexpress_search': f"https://www.aliexpress.com/w/wholesale-{p['product'].replace(' ', '-')}.html",
                'alibaba_search': f"https://www.alibaba.com/trade/search?SearchText={p['product'].replace(' ', '+')}",
            }

        fees = calc_platform_fees(p['sell_price'])
        source_url = db.get('aliexpress_search', '')

        listing = {
            'product': p['product'],
            'sell_price': p['sell_price'],
            'source_price': p['source_price'],
        }

        # FB Marketplace listing
        if not platform_filter or platform_filter == 'fb':
            fb = FB_TEMPLATE.format(
                product_title=db['title'],
                sell_price=p['sell_price'],
                category=db['category'],
                description=db['description'],
                tags=db['tags'],
                source_url=source_url,
                total_cost=p['total_cost'],
                net_profit=p['net_profit'],
                margin_pct=p['margin_pct'],
            )
            listing['fb'] = fb

        # eBay listing
        if not platform_filter or platform_filter == 'ebay':
            ebay_cost = p['source_price'] + fees['ebay'] + 4.50  # source + fees + shipping
            ebay_profit = p['sell_price'] - ebay_cost
            ebay_margin = (ebay_profit / p['sell_price'] * 100) if p['sell_price'] > 0 else 0

            ebay = EBAY_TEMPLATE.format(
                product_title=db['title'],
                ebay_title=db['ebay_title'],
                sell_price=p['sell_price'],
                ebay_category=db['ebay_category'],
                description=db['description'],
                item_specifics=db['item_specifics'],
                source_url=source_url,
                total_cost=ebay_cost,
                net_profit_ebay=ebay_profit,
                margin_pct_ebay=ebay_margin,
            )
            listing['ebay'] = ebay

        # Mercari listing
        if not platform_filter or platform_filter == 'mercari':
            mercari_fee = fees['mercari']
            mercari_cost = p['source_price'] + mercari_fee + 4.50
            mercari_profit = p['sell_price'] - mercari_cost

            mercari = MERCARI_TEMPLATE.format(
                product_title=db['title'],
                sell_price=p['sell_price'],
                category=db['category'],
                description=db['description'],
                tags=db['tags'],
                source_url=source_url,
                total_cost=mercari_cost,
                mercari_fee=mercari_fee,
                net_profit_mercari=mercari_profit,
            )
            listing['mercari'] = mercari

        all_listings.append(listing)

    # Write combined output
    ts = datetime.now().strftime('%Y_%m_%d')
    out_file = OUTPUT_DIR / f"ARB_LISTINGS_{ts}.md"

    with open(out_file, 'w') as f:
        f.write(f"# PRINTMAXX Arb Listings — {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n")
        f.write(f"**{len(all_listings)} profitable products** | Min margin: {min_margin}%\n\n")
        f.write("Copy-paste these listings to each platform. Source links included.\n\n")
        f.write("---\n\n")

        for i, l in enumerate(all_listings, 1):
            f.write(f"# Product {i}: {l['product'].title()}\n\n")
            f.write(f"**Sell:** ${l['sell_price']:.2f} | **Source:** ${l['source_price']:.2f}\n\n")

            if 'fb' in l:
                f.write("### FB Marketplace Listing\n\n")
                f.write(l['fb'])
                f.write("\n\n")

            if 'ebay' in l:
                f.write("### eBay Listing\n\n")
                f.write(l['ebay'])
                f.write("\n\n")

            if 'mercari' in l:
                f.write("### Mercari Listing\n\n")
                f.write(l['mercari'])
                f.write("\n\n")

            f.write("---\n\n")

    print(f"\n{'='*60}")
    print(f"  LISTINGS GENERATED: {len(all_listings)} products")
    print(f"  Output: {out_file}")
    print(f"{'='*60}\n")

    for l in all_listings:
        print(f"  {l['product'].title():30s} sell: ${l['sell_price']:.2f}  source: ${l['source_price']:.2f}")

    return out_file


def generate_sourcing(products):
    """Generate AliExpress/Alibaba sourcing links and procurement guide"""
    SOURCING_DIR.mkdir(parents=True, exist_ok=True)

    ts = datetime.now().strftime('%Y_%m_%d')
    out_file = SOURCING_DIR / f"SOURCING_GUIDE_{ts}.md"

    with open(out_file, 'w') as f:
        f.write(f"# PRINTMAXX Sourcing Guide — {datetime.now().strftime('%Y-%m-%d')}\n\n")
        f.write("## How to Source (Dropship Model)\n\n")
        f.write("1. **AliExpress** - Best for testing (no MOQ, ships direct to customer)\n")
        f.write("2. **Alibaba/1688** - Best for bulk (MOQ 50-500, 40-60% cheaper)\n")
        f.write("3. **CJ Dropshipping** - Best for automation (API, US warehouse, 3-7 day ship)\n\n")
        f.write("## Sourcing Links\n\n")

        for p in products:
            if p['net_profit'] <= 0:
                continue
            db = PRODUCT_DB.get(p['product'], {})
            f.write(f"### {p['product'].title()}\n\n")
            f.write(f"- **Sell at:** ${p['sell_price']:.2f}\n")
            f.write(f"- **Source est:** ${p['source_price']:.2f}\n")
            f.write(f"- **Profit:** ${p['net_profit']:.2f} ({p['margin_pct']:.1f}%)\n")
            if db.get('aliexpress_search'):
                f.write(f"- **AliExpress:** {db['aliexpress_search']}\n")
            if db.get('alibaba_search'):
                f.write(f"- **Alibaba:** {db['alibaba_search']}\n")
            f.write(f"- **CJ Dropshipping:** https://cjdropshipping.com/search?q={p['product'].replace(' ', '+')}\n")
            f.write("\n")

        f.write("\n## Automation (CJ Dropshipping API)\n\n")
        f.write("```\n")
        f.write("1. Sign up: https://cjdropshipping.com (free)\n")
        f.write("2. Connect to eBay/Shopify via API\n")
        f.write("3. When order comes in → auto-fulfills from US warehouse\n")
        f.write("4. Customer gets package in 3-7 days\n")
        f.write("5. You never touch inventory\n")
        f.write("```\n")

    print(f"  Sourcing guide: {out_file}")
    return out_file


def main():
    import argparse
    parser = argparse.ArgumentParser(description='Generate arb listings from scan data')
    parser.add_argument('--generate', action='store_true', help='Generate all listings')
    parser.add_argument('--platform', choices=['fb', 'ebay', 'mercari'], help='Platform filter')
    parser.add_argument('--min-margin', type=float, default=20, help='Minimum margin %% (default 20)')
    parser.add_argument('--top', type=int, default=0, help='Only generate top N items (after filters)')
    parser.add_argument('--action', default='', help='Only include items matching action (e.g. LIST)')
    parser.add_argument('--source', action='store_true', help='Generate sourcing links')
    parser.add_argument('--all', action='store_true', help='Generate everything')
    args = parser.parse_args()

    products = load_arb_data()
    if not products:
        return

    print(f"\n  Loaded {len(products)} profitable products from arb scan\n")

    if args.all or args.generate or args.platform:
        generate_listings(products, args.platform, args.min_margin, top_n=args.top, action_filter=args.action)

    if args.all or args.source:
        generate_sourcing(products)

    if not any([args.all, args.generate, args.platform, args.source]):
        # Default: show summary
        print(f"  {'Product':<25s} {'Sell':>8s} {'Source':>8s} {'Profit':>8s} {'Margin':>8s}")
        print(f"  {'-'*25} {'-'*8} {'-'*8} {'-'*8} {'-'*8}")
        for p in products[:10]:
            print(f"  {p['product']:<25s} ${p['sell_price']:>6.2f} ${p['source_price']:>6.2f} ${p['net_profit']:>6.2f} {p['margin_pct']:>6.1f}%")
        print(f"\n  Run with --generate to create copy-paste listings")
        print(f"  Run with --source to get AliExpress/Alibaba links")
        print(f"  Run with --all to generate everything")


if __name__ == '__main__':
    main()
