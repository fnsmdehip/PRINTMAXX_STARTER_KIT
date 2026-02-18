#!/usr/bin/env python3
"""
PRINTMAXX Competitor Sourcing Pipeline - Factory-Direct Intelligence
# CRON: 0 5 * * 1  python3 AUTOMATIONS/competitor_sourcing_pipeline.py --scan >> AUTOMATIONS/logs/competitor_sourcing.log 2>&1

Maps ecom arb products -> top seller competitors -> their exact factory source -> factory-direct pricing.
Reads ECOM_ARB_OPPORTUNITIES.csv + CONTACT_READY_FACTORIES.csv + IMPORT_SOURCING_INTEL.csv.
Outputs COMPETITOR_FACTORY_MAP.csv with margin improvement calculations.

The thesis: US customs data is public. every shipment entering the country is logged.
Find a competitor doing $500k/mo. Search ImportYeti. See their factory in China.
Contact factory directly. Cut out AliExpress middleman. Margin goes from 25% to 60%+.

Usage:
    python3 competitor_sourcing_pipeline.py --scan              # Full pipeline scan
    python3 competitor_sourcing_pipeline.py --product "yoga mat" # Single product deep dive
    python3 competitor_sourcing_pipeline.py --status            # Show pipeline status
    python3 competitor_sourcing_pipeline.py --top 10            # Top 10 opportunities
    python3 competitor_sourcing_pipeline.py --enrich            # Enrich existing map with new intel
"""

import argparse
import csv
import hashlib
import json
import os
import re
import sys
import time
import urllib.parse
from datetime import datetime
from pathlib import Path

# ============================================================
# PATHS & CONSTANTS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent
LEDGER_DIR = PROJECT_ROOT / "LEDGER"
AUTOMATIONS_DIR = PROJECT_ROOT / "AUTOMATIONS"
LOGS_DIR = AUTOMATIONS_DIR / "logs"
OPS_DIR = PROJECT_ROOT / "OPS"
LOCK_FILE = AUTOMATIONS_DIR / ".competitor_sourcing.lock"

# Input files
ECOM_ARB_CSV = LEDGER_DIR / "ECOM_ARB_OPPORTUNITIES.csv"
CONTACT_FACTORIES_CSV = LEDGER_DIR / "CONTACT_READY_FACTORIES.csv"
INTEL_CSV = LEDGER_DIR / "IMPORT_SOURCING_INTEL.csv"

# Output
COMPETITOR_MAP_CSV = LEDGER_DIR / "COMPETITOR_FACTORY_MAP.csv"
LOG_FILE = LOGS_DIR / f"competitor_sourcing_{datetime.now().strftime('%Y-%m-%d')}.log"

# Known top sellers per product category (real US ecom competitors)
# Format: product_keyword -> list of {company, est_revenue_mo, platform}
TOP_SELLERS = {
    "led face mask": [
        {"company": "CurrentBody", "est_revenue_mo": 2000000, "platform": "DTC"},
        {"company": "Omnilux", "est_revenue_mo": 1500000, "platform": "DTC"},
        {"company": "Solawave", "est_revenue_mo": 800000, "platform": "Amazon+DTC"},
        {"company": "Project E Beauty", "est_revenue_mo": 500000, "platform": "Amazon"},
        {"company": "Dennis Gross", "est_revenue_mo": 400000, "platform": "Sephora+DTC"},
    ],
    "yoga mat": [
        {"company": "Manduka", "est_revenue_mo": 3000000, "platform": "DTC+Amazon"},
        {"company": "Liforme", "est_revenue_mo": 1200000, "platform": "DTC"},
        {"company": "Jade Yoga", "est_revenue_mo": 800000, "platform": "DTC+Amazon"},
        {"company": "Gaiam", "est_revenue_mo": 2000000, "platform": "Amazon+Retail"},
        {"company": "Lululemon", "est_revenue_mo": 5000000, "platform": "DTC+Retail"},
    ],
    "phone projector": [
        {"company": "Nebula Anker", "est_revenue_mo": 4000000, "platform": "Amazon+DTC"},
        {"company": "Vankyo", "est_revenue_mo": 1500000, "platform": "Amazon"},
        {"company": "Yaber", "est_revenue_mo": 2000000, "platform": "Amazon"},
    ],
    "wireless earbuds": [
        {"company": "JLab", "est_revenue_mo": 5000000, "platform": "Amazon+Retail"},
        {"company": "Tozo", "est_revenue_mo": 3000000, "platform": "Amazon"},
        {"company": "SoundPeats", "est_revenue_mo": 2000000, "platform": "Amazon"},
        {"company": "Skullcandy", "est_revenue_mo": 4000000, "platform": "Retail+Amazon"},
    ],
    "ring light": [
        {"company": "Neewer", "est_revenue_mo": 2000000, "platform": "Amazon"},
        {"company": "Lume Cube", "est_revenue_mo": 800000, "platform": "DTC+Amazon"},
        {"company": "Elgato", "est_revenue_mo": 1500000, "platform": "Amazon+DTC"},
    ],
    "pull up bar": [
        {"company": "Iron Age", "est_revenue_mo": 500000, "platform": "Amazon"},
        {"company": "Rogue Fitness", "est_revenue_mo": 3000000, "platform": "DTC"},
        {"company": "Perfect Fitness", "est_revenue_mo": 1000000, "platform": "Amazon+Retail"},
    ],
    "portable blender": [
        {"company": "BlendJet", "est_revenue_mo": 8000000, "platform": "DTC+Amazon"},
        {"company": "PopBabies", "est_revenue_mo": 500000, "platform": "Amazon"},
        {"company": "Zulay Kitchen", "est_revenue_mo": 600000, "platform": "Amazon"},
    ],
    "resistance bands set": [
        {"company": "Fit Simplify", "est_revenue_mo": 1000000, "platform": "Amazon"},
        {"company": "WODFitters", "est_revenue_mo": 400000, "platform": "Amazon+DTC"},
        {"company": "Bodylastics", "est_revenue_mo": 300000, "platform": "Amazon+DTC"},
    ],
    "cable organizer": [
        {"company": "Anker", "est_revenue_mo": 1000000, "platform": "Amazon"},
        {"company": "JOTO", "est_revenue_mo": 500000, "platform": "Amazon"},
    ],
    "posture corrector": [
        {"company": "Upright Go", "est_revenue_mo": 800000, "platform": "DTC+Amazon"},
        {"company": "ComfyBrace", "est_revenue_mo": 400000, "platform": "Amazon"},
    ],
    "lash serum": [
        {"company": "Grande Cosmetics", "est_revenue_mo": 2000000, "platform": "Sephora+DTC"},
        {"company": "Revitalash", "est_revenue_mo": 1500000, "platform": "DTC"},
        {"company": "Babe Lash", "est_revenue_mo": 600000, "platform": "Amazon+DTC"},
    ],
    "neck stretcher": [
        {"company": "Neck Hammock", "est_revenue_mo": 300000, "platform": "DTC"},
        {"company": "Restcloud", "est_revenue_mo": 400000, "platform": "Amazon"},
    ],
    "knife sharpener": [
        {"company": "Work Sharp", "est_revenue_mo": 1000000, "platform": "Amazon+DTC"},
        {"company": "Lansky", "est_revenue_mo": 500000, "platform": "Amazon+Retail"},
    ],
    "microcurrent device": [
        {"company": "NuFACE", "est_revenue_mo": 3000000, "platform": "Sephora+DTC"},
        {"company": "ZIIP Beauty", "est_revenue_mo": 1000000, "platform": "DTC"},
        {"company": "Foreo Bear", "est_revenue_mo": 1500000, "platform": "DTC+Sephora"},
    ],
    "air fryer liner": [
        {"company": "Numola", "est_revenue_mo": 200000, "platform": "Amazon"},
    ],
    "dermaplaning tool": [
        {"company": "Dermaflash", "est_revenue_mo": 500000, "platform": "Sephora+DTC"},
        {"company": "Schick Hydro Silk", "est_revenue_mo": 800000, "platform": "Retail"},
    ],
    "jump rope weighted": [
        {"company": "Crossrope", "est_revenue_mo": 1000000, "platform": "DTC"},
        {"company": "WOD Nation", "est_revenue_mo": 300000, "platform": "Amazon"},
    ],
    "grip strength trainer": [
        {"company": "Captains of Crush", "est_revenue_mo": 400000, "platform": "Amazon+DTC"},
        {"company": "GD Iron Grip", "est_revenue_mo": 200000, "platform": "Amazon"},
    ],
    "dog puzzle toy": [
        {"company": "Nina Ottosson", "est_revenue_mo": 500000, "platform": "Amazon+PetSmart"},
        {"company": "Outward Hound", "est_revenue_mo": 800000, "platform": "Amazon+Retail"},
    ],
}

# AliExpress to factory-direct price multiplier (typically 40-70% cheaper)
FACTORY_DIRECT_DISCOUNT_LOW = 0.35   # best case: factory price = 35% of AliExpress
FACTORY_DIRECT_DISCOUNT_HIGH = 0.60  # worst case: factory price = 60% of AliExpress
FACTORY_DIRECT_DISCOUNT_MID = 0.45   # typical case

COMPETITOR_MAP_HEADERS = [
    "entry_id", "timestamp", "product", "competitor", "competitor_revenue_est",
    "competitor_platform", "factory_name", "factory_location", "shipment_count",
    "aliexpress_price", "factory_direct_low", "factory_direct_mid", "factory_direct_high",
    "sell_price", "margin_current_pct", "margin_factory_direct_pct",
    "margin_improvement_pct", "alibaba_url", "importyeti_url",
    "contact_status", "priority_score", "notes"
]

# ============================================================
# PATH SAFETY & UTILS
# ============================================================

def safe_path(path: Path) -> Path:
    resolved = path.resolve()
    if not str(resolved).startswith(str(PROJECT_ROOT)):
        raise ValueError(f"Path {resolved} outside project root")
    return resolved


def ensure_dirs():
    for d in [LEDGER_DIR, LOGS_DIR]:
        d.mkdir(parents=True, exist_ok=True)


def log(msg: str, level: str = "INFO"):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] [{level}] {msg}"
    print(line)
    try:
        with open(safe_path(LOG_FILE), "a") as f:
            f.write(line + "\n")
    except Exception:
        pass


def acquire_lock() -> bool:
    lf = safe_path(LOCK_FILE)
    if lf.exists():
        try:
            pid = int(lf.read_text().strip())
            os.kill(pid, 0)
            return False
        except (ProcessLookupError, ValueError, PermissionError):
            pass
    lf.write_text(str(os.getpid()))
    return True


def release_lock():
    lf = safe_path(LOCK_FILE)
    if lf.exists():
        lf.unlink()

# ============================================================
# DATA LOADERS
# ============================================================

def load_arb_opportunities() -> dict:
    """Load best margin per product from ECOM_ARB_OPPORTUNITIES.csv."""
    if not ECOM_ARB_CSV.exists():
        log("ECOM_ARB_OPPORTUNITIES.csv not found", "WARN")
        return {}

    products = {}
    with open(ECOM_ARB_CSV, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            product = row.get("product", "").strip().lower()
            if not product:
                continue
            try:
                margin = float(row.get("margin_pct", 0))
                sell_price = float(row.get("sell_price", 0))
                source_price = float(row.get("source_price", 0))
            except (ValueError, TypeError):
                continue

            if product not in products or margin > products[product]["margin_pct"]:
                products[product] = {
                    "product": row.get("product", "").strip(),
                    "margin_pct": margin,
                    "sell_price": sell_price,
                    "source_price": source_price,
                    "category": row.get("category", ""),
                    "action": row.get("action", "SKIP"),
                }
    return products


def load_factory_intel() -> dict:
    """Load factory intel indexed by product keyword."""
    by_product = {}
    for csv_path in [INTEL_CSV, CONTACT_FACTORIES_CSV]:
        if not csv_path.exists():
            continue
        with open(csv_path, "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                factory = row.get("factory_name", "").strip()
                if not factory:
                    continue
                # Match to product
                products_field = row.get("products", row.get("arb_product_match", row.get("query", "")))
                for prod_key in products_field.lower().split(";"):
                    prod_key = prod_key.strip()
                    if prod_key:
                        by_product.setdefault(prod_key, []).append({
                            "factory_name": factory,
                            "factory_location": row.get("factory_location", ""),
                            "factory_country": row.get("factory_country", "CN"),
                            "shipment_count": _safe_int(row.get("shipment_count", 0)),
                            "confidence": row.get("confidence", "LOW"),
                            "priority_score": _safe_int(row.get("priority_score", 0)),
                            "alibaba_url": row.get("alibaba_search_url", row.get("alibaba_url", "")),
                            "us_importers": row.get("us_importers", ""),
                            "last_shipment": row.get("last_shipment", ""),
                        })
    return by_product


def load_existing_map() -> dict:
    """Load existing competitor map entries for dedup."""
    if not COMPETITOR_MAP_CSV.exists():
        return {}
    entries = {}
    with open(COMPETITOR_MAP_CSV, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            key = f"{row.get('product', '').lower()}|{row.get('competitor', '').lower()}|{row.get('factory_name', '').lower()}"
            entries[key] = row
    return entries


def _safe_int(val) -> int:
    try:
        return int(float(val))
    except (ValueError, TypeError):
        return 0

# ============================================================
# PIPELINE CORE
# ============================================================

def map_competitor_to_factory(product: str, arb_data: dict, factory_intel: list, competitor: dict) -> list:
    """
    Map a competitor to their likely factory source.
    Cross-references ImportYeti intel with competitor company name.
    Returns list of mapping entries.
    """
    results = []
    aliexpress_price = arb_data.get("source_price", 0)
    sell_price = arb_data.get("sell_price", 0)
    current_margin = arb_data.get("margin_pct", 0)
    competitor_name = competitor.get("company", "")

    # Find factories that match this product
    matched_factories = []
    for fi in factory_intel:
        # Check if competitor is listed as US importer
        importers = fi.get("us_importers", "").lower()
        factory_name = fi.get("factory_name", "")

        # Direct importer match = highest confidence
        if competitor_name.lower() in importers:
            matched_factories.append({**fi, "match_type": "DIRECT_IMPORTER", "match_score": 100})
        # Same product category = indirect match
        elif fi.get("shipment_count", 0) >= 5:
            matched_factories.append({**fi, "match_type": "CATEGORY_MATCH", "match_score": 60})
        elif fi.get("shipment_count", 0) >= 1:
            matched_factories.append({**fi, "match_type": "CATEGORY_MATCH", "match_score": 40})

    # Sort by match score then shipment count
    matched_factories.sort(key=lambda x: (x.get("match_score", 0), x.get("shipment_count", 0)), reverse=True)

    # Take top 3 factory matches per competitor
    for factory in matched_factories[:3]:
        factory_direct_low = round(aliexpress_price * FACTORY_DIRECT_DISCOUNT_LOW, 2)
        factory_direct_mid = round(aliexpress_price * FACTORY_DIRECT_DISCOUNT_MID, 2)
        factory_direct_high = round(aliexpress_price * FACTORY_DIRECT_DISCOUNT_HIGH, 2)

        # Calculate margin improvement with factory-direct pricing
        if sell_price > 0 and factory_direct_mid > 0:
            # Estimate total cost with factory-direct (keep same fees/shipping)
            # Original margin = (sell - total_cost) / sell
            # Factory-direct margin = (sell - (total_cost - source_price + factory_direct_mid)) / sell
            cost_reduction = aliexpress_price - factory_direct_mid
            new_margin = current_margin + (cost_reduction / sell_price * 100) if sell_price else 0
            margin_improvement = new_margin - current_margin
        else:
            new_margin = 0
            margin_improvement = 0

        # Priority score
        priority = _calc_priority(factory, arb_data, margin_improvement)

        # ImportYeti URL for the competitor
        comp_slug = re.sub(r'[^a-z0-9]+', '-', competitor_name.lower()).strip('-')
        importyeti_url = f"https://www.importyeti.com/company/{comp_slug}"

        entry_id = hashlib.md5(
            f"{product}{competitor_name}{factory.get('factory_name', '')}".encode()
        ).hexdigest()[:12]

        results.append({
            "entry_id": entry_id,
            "timestamp": datetime.now().isoformat(),
            "product": product,
            "competitor": competitor_name,
            "competitor_revenue_est": f"${competitor.get('est_revenue_mo', 0):,.0f}/mo",
            "competitor_platform": competitor.get("platform", ""),
            "factory_name": factory.get("factory_name", ""),
            "factory_location": factory.get("factory_location", ""),
            "shipment_count": factory.get("shipment_count", 0),
            "aliexpress_price": f"${aliexpress_price:.2f}",
            "factory_direct_low": f"${factory_direct_low:.2f}",
            "factory_direct_mid": f"${factory_direct_mid:.2f}",
            "factory_direct_high": f"${factory_direct_high:.2f}",
            "sell_price": f"${sell_price:.2f}",
            "margin_current_pct": f"{current_margin:.1f}%",
            "margin_factory_direct_pct": f"{new_margin:.1f}%",
            "margin_improvement_pct": f"+{margin_improvement:.1f}%",
            "alibaba_url": factory.get("alibaba_url", ""),
            "importyeti_url": importyeti_url,
            "contact_status": "NOT_CONTACTED",
            "priority_score": priority,
            "notes": f"Match type: {factory.get('match_type', 'UNKNOWN')}. "
                     f"Factory confidence: {factory.get('confidence', 'LOW')}.",
        })

    return results


def _calc_priority(factory: dict, arb_data: dict, margin_improvement: float) -> int:
    """Calculate priority score 0-100."""
    score = 0

    # Margin improvement (biggest factor)
    if margin_improvement >= 30:
        score += 30
    elif margin_improvement >= 20:
        score += 25
    elif margin_improvement >= 10:
        score += 15
    elif margin_improvement > 0:
        score += 5

    # Factory shipment volume
    sc = factory.get("shipment_count", 0)
    if sc >= 100:
        score += 20
    elif sc >= 50:
        score += 15
    elif sc >= 10:
        score += 10
    elif sc >= 1:
        score += 5

    # Match type
    match_type = factory.get("match_type", "")
    if match_type == "DIRECT_IMPORTER":
        score += 25
    elif match_type == "CATEGORY_MATCH":
        score += 10

    # Factory confidence
    conf = factory.get("confidence", "LOW")
    if conf == "HIGH":
        score += 15
    elif conf == "MEDIUM":
        score += 10
    else:
        score += 3

    # Sell price (higher price = more room for margin)
    sell = arb_data.get("sell_price", 0)
    if sell >= 30:
        score += 10
    elif sell >= 15:
        score += 5

    return min(score, 100)

# ============================================================
# SCAN PIPELINE
# ============================================================

def run_full_scan(product_filter: str = None, top_n: int = 0) -> list:
    """
    Full pipeline: arb products -> competitors -> factory mapping.
    """
    arb_data = load_arb_opportunities()
    factory_intel = load_factory_intel()
    existing = load_existing_map()

    if not arb_data:
        log("No arb data found. Run ecom_arb_engine.py first.")
        return []

    # Filter to profitable products
    profitable = {k: v for k, v in arb_data.items() if v["margin_pct"] > 0}
    log(f"Found {len(profitable)} profitable products in arb data")

    if product_filter:
        profitable = {k: v for k, v in profitable.items() if product_filter.lower() in k.lower()}
        log(f"Filtered to {len(profitable)} products matching '{product_filter}'")

    # Sort by margin
    sorted_products = sorted(profitable.items(), key=lambda x: x[1]["margin_pct"], reverse=True)
    if top_n > 0:
        sorted_products = sorted_products[:top_n]

    all_entries = []
    products_scanned = 0
    competitors_mapped = 0
    factories_found = 0

    for prod_key, arb in sorted_products:
        product_display = arb["product"]

        # Get competitors for this product
        competitors = TOP_SELLERS.get(prod_key, [])
        if not competitors:
            # Try partial match
            for ts_key, ts_list in TOP_SELLERS.items():
                if ts_key in prod_key or prod_key in ts_key:
                    competitors = ts_list
                    break

        if not competitors:
            log(f"No known competitors for '{product_display}', skipping")
            continue

        # Get factory intel for this product
        prod_factories = factory_intel.get(prod_key, [])
        # Also try the display name
        prod_factories += factory_intel.get(product_display.lower(), [])
        # Dedup factories by name
        seen_factories = set()
        unique_factories = []
        for fi in prod_factories:
            fn = fi.get("factory_name", "").lower()
            if fn and fn not in seen_factories:
                seen_factories.add(fn)
                unique_factories.append(fi)

        if not unique_factories:
            log(f"No factory intel for '{product_display}'. Run import_sourcing_scanner.py --product '{product_display}' first.")
            # Still create entries with placeholder
            for comp in competitors[:3]:
                entry_id = hashlib.md5(
                    f"{product_display}{comp['company']}NO_FACTORY".encode()
                ).hexdigest()[:12]

                comp_slug = re.sub(r'[^a-z0-9]+', '-', comp['company'].lower()).strip('-')
                all_entries.append({
                    "entry_id": entry_id,
                    "timestamp": datetime.now().isoformat(),
                    "product": product_display,
                    "competitor": comp["company"],
                    "competitor_revenue_est": f"${comp.get('est_revenue_mo', 0):,.0f}/mo",
                    "competitor_platform": comp.get("platform", ""),
                    "factory_name": "NEEDS_SCAN",
                    "factory_location": "",
                    "shipment_count": 0,
                    "aliexpress_price": f"${arb['source_price']:.2f}",
                    "factory_direct_low": f"${arb['source_price'] * FACTORY_DIRECT_DISCOUNT_LOW:.2f}",
                    "factory_direct_mid": f"${arb['source_price'] * FACTORY_DIRECT_DISCOUNT_MID:.2f}",
                    "factory_direct_high": f"${arb['source_price'] * FACTORY_DIRECT_DISCOUNT_HIGH:.2f}",
                    "sell_price": f"${arb['sell_price']:.2f}",
                    "margin_current_pct": f"{arb['margin_pct']:.1f}%",
                    "margin_factory_direct_pct": "N/A",
                    "margin_improvement_pct": "N/A",
                    "alibaba_url": f"https://www.alibaba.com/trade/search?SearchText={urllib.parse.quote_plus(product_display)}&tab=supplier",
                    "importyeti_url": f"https://www.importyeti.com/company/{comp_slug}",
                    "contact_status": "NEEDS_SCAN",
                    "priority_score": 20,
                    "notes": "No factory intel yet. Run import_sourcing_scanner.py first.",
                })
                competitors_mapped += 1
            products_scanned += 1
            continue

        log(f"Mapping '{product_display}': {len(competitors)} competitors x {len(unique_factories)} factories")

        for comp in competitors:
            entries = map_competitor_to_factory(
                product_display, arb, unique_factories, comp
            )
            # Dedup against existing
            for entry in entries:
                dedup_key = f"{entry['product'].lower()}|{entry['competitor'].lower()}|{entry['factory_name'].lower()}"
                if dedup_key not in existing:
                    all_entries.append(entry)
                    existing[dedup_key] = entry
                    factories_found += 1
            competitors_mapped += 1

        products_scanned += 1

    # Sort by priority
    all_entries.sort(key=lambda x: x.get("priority_score", 0), reverse=True)

    # Save
    if all_entries:
        save_competitor_map(all_entries)

    log(f"Pipeline complete: {products_scanned} products, {competitors_mapped} competitors, {factories_found} factory mappings")
    return all_entries


def save_competitor_map(entries: list):
    """Append entries to COMPETITOR_FACTORY_MAP.csv."""
    csv_path = safe_path(COMPETITOR_MAP_CSV)
    file_exists = csv_path.exists() and csv_path.stat().st_size > 0

    with open(csv_path, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=COMPETITOR_MAP_HEADERS, extrasaction="ignore")
        if not file_exists:
            writer.writeheader()
        writer.writerows(entries)

    log(f"Saved {len(entries)} entries to {csv_path}")

# ============================================================
# STATUS & DISPLAY
# ============================================================

def show_status():
    """Show full pipeline status."""
    print("\n" + "=" * 72)
    print("  PRINTMAXX COMPETITOR SOURCING PIPELINE")
    print("=" * 72)

    # Check input files
    arb_data = load_arb_opportunities()
    factory_intel = load_factory_intel()

    profitable = {k: v for k, v in arb_data.items() if v["margin_pct"] > 0}
    total_factories = sum(len(v) for v in factory_intel.values())
    products_with_intel = len(factory_intel)

    print(f"\n  INPUT DATA:")
    print(f"    Profitable arb products:  {len(profitable)}")
    print(f"    Known competitors:        {sum(len(v) for v in TOP_SELLERS.values())} across {len(TOP_SELLERS)} products")
    print(f"    Factory intel records:    {total_factories} across {products_with_intel} products")

    # Check existing contact factories
    if CONTACT_FACTORIES_CSV.exists():
        with open(CONTACT_FACTORIES_CSV, "r") as f:
            contacts = list(csv.DictReader(f))
        high_conf = sum(1 for c in contacts if c.get("confidence") == "HIGH")
        print(f"    Contact-ready factories:  {len(contacts)} ({high_conf} HIGH confidence)")

    # Check output
    if COMPETITOR_MAP_CSV.exists():
        with open(COMPETITOR_MAP_CSV, "r") as f:
            map_entries = list(csv.DictReader(f))

        print(f"\n  COMPETITOR MAP:")
        print(f"    Total entries:           {len(map_entries)}")
        products_mapped = len(set(e.get("product", "") for e in map_entries))
        competitors_mapped = len(set(e.get("competitor", "") for e in map_entries))
        factories_mapped = len(set(e.get("factory_name", "") for e in map_entries if e.get("factory_name") != "NEEDS_SCAN"))
        needs_scan = sum(1 for e in map_entries if e.get("factory_name") == "NEEDS_SCAN")
        not_contacted = sum(1 for e in map_entries if e.get("contact_status") == "NOT_CONTACTED")

        print(f"    Products mapped:         {products_mapped}")
        print(f"    Competitors mapped:      {competitors_mapped}")
        print(f"    Factories found:         {factories_mapped}")
        print(f"    Needs factory scan:      {needs_scan}")
        print(f"    Not yet contacted:       {not_contacted}")

        # Top opportunities
        scored = sorted(map_entries, key=lambda x: _safe_int(x.get("priority_score", 0)), reverse=True)
        actionable = [e for e in scored if e.get("factory_name") != "NEEDS_SCAN"]

        if actionable:
            print(f"\n  TOP 10 OPPORTUNITIES (factory-direct margin improvement):")
            print(f"  {'#':>3} {'Product':<18} {'Competitor':<18} {'Factory':<22} {'Margin+':>8} {'Score':>5}")
            print(f"  {'---':>3} {'-'*18} {'-'*18} {'-'*22} {'-'*8} {'-'*5}")
            for i, e in enumerate(actionable[:10], 1):
                prod = e.get("product", "")[:17]
                comp = e.get("competitor", "")[:17]
                factory = e.get("factory_name", "")[:21]
                margin_imp = e.get("margin_improvement_pct", "N/A")
                score = e.get("priority_score", 0)
                print(f"  {i:>3} {prod:<18} {comp:<18} {factory:<22} {margin_imp:>8} {score:>5}")

        # Products needing factory scan
        if needs_scan > 0:
            needs_scan_products = set(e.get("product", "") for e in map_entries if e.get("factory_name") == "NEEDS_SCAN")
            print(f"\n  PRODUCTS NEEDING FACTORY SCAN ({len(needs_scan_products)}):")
            for prod in sorted(needs_scan_products):
                print(f"    python3 AUTOMATIONS/import_sourcing_scanner.py --product '{prod}'")

    else:
        print(f"\n  COMPETITOR MAP: Not yet generated. Run --scan")

    # Coverage analysis
    print(f"\n  COVERAGE ANALYSIS:")
    covered = 0
    uncovered = []
    for prod_key in profitable:
        has_competitors = prod_key in TOP_SELLERS or any(
            ts_key in prod_key or prod_key in ts_key for ts_key in TOP_SELLERS
        )
        has_factory_intel = prod_key in factory_intel or prod_key.lower() in factory_intel
        if has_competitors and has_factory_intel:
            covered += 1
        elif not has_competitors:
            uncovered.append(f"  {prod_key}: no known competitors")
        elif not has_factory_intel:
            uncovered.append(f"  {prod_key}: no factory intel")

    print(f"    Fully covered:           {covered}/{len(profitable)}")
    if uncovered[:5]:
        print(f"    Gaps (first 5):")
        for gap in uncovered[:5]:
            print(f"      {gap}")

    print(f"\n  FILES:")
    print(f"    Competitor map:  {COMPETITOR_MAP_CSV}")
    print(f"    Intel CSV:       {INTEL_CSV}")
    print(f"    Contacts CSV:    {CONTACT_FACTORIES_CSV}")
    print(f"    Arb data:        {ECOM_ARB_CSV}")
    print("=" * 72 + "\n")


def show_top(n: int = 10):
    """Show top N opportunities from the map."""
    if not COMPETITOR_MAP_CSV.exists():
        print("No competitor map yet. Run --scan first.")
        return

    with open(COMPETITOR_MAP_CSV, "r") as f:
        entries = list(csv.DictReader(f))

    actionable = [e for e in entries if e.get("factory_name") != "NEEDS_SCAN"]
    actionable.sort(key=lambda x: _safe_int(x.get("priority_score", 0)), reverse=True)

    print(f"\n  TOP {n} COMPETITOR SOURCING OPPORTUNITIES")
    print(f"  {'='*70}")

    for i, e in enumerate(actionable[:n], 1):
        print(f"\n  #{i} — {e.get('product', '')} via {e.get('competitor', '')}")
        print(f"    Factory:          {e.get('factory_name', '')}")
        print(f"    Location:         {e.get('factory_location', '')}")
        print(f"    Shipments:        {e.get('shipment_count', 0)}")
        print(f"    Competitor Rev:   {e.get('competitor_revenue_est', '')}")
        print(f"    AliExpress:       {e.get('aliexpress_price', '')}")
        print(f"    Factory Direct:   {e.get('factory_direct_mid', '')} (range: {e.get('factory_direct_low', '')} - {e.get('factory_direct_high', '')})")
        print(f"    Sell Price:       {e.get('sell_price', '')}")
        print(f"    Current Margin:   {e.get('margin_current_pct', '')}")
        print(f"    w/ Factory:       {e.get('margin_factory_direct_pct', '')}")
        print(f"    Margin Boost:     {e.get('margin_improvement_pct', '')}")
        print(f"    Priority Score:   {e.get('priority_score', '')}/100")
        print(f"    Alibaba:          {e.get('alibaba_url', '')}")
        print(f"    ImportYeti:       {e.get('importyeti_url', '')}")
        print(f"    Contact Status:   {e.get('contact_status', '')}")

# ============================================================
# CLI
# ============================================================

def main():
    parser = argparse.ArgumentParser(
        description="PRINTMAXX Competitor Sourcing Pipeline",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 competitor_sourcing_pipeline.py --scan                # Full pipeline
  python3 competitor_sourcing_pipeline.py --product "yoga mat"  # Single product
  python3 competitor_sourcing_pipeline.py --status              # Pipeline status
  python3 competitor_sourcing_pipeline.py --top 10              # Top 10 opportunities
  python3 competitor_sourcing_pipeline.py --enrich              # Re-enrich with new intel
        """,
    )
    parser.add_argument("--scan", action="store_true", help="Full pipeline scan")
    parser.add_argument("--product", type=str, help="Scan single product")
    parser.add_argument("--status", action="store_true", help="Show pipeline status")
    parser.add_argument("--top", type=int, default=0, help="Show top N opportunities")
    parser.add_argument("--enrich", action="store_true", help="Re-enrich map with new factory intel")

    args = parser.parse_args()
    ensure_dirs()

    if not any([args.scan, args.product, args.status, args.top, args.enrich]):
        args.status = True

    if args.status:
        show_status()
    elif args.top:
        show_top(args.top)
    elif args.scan or args.product or args.enrich:
        if not acquire_lock():
            log("Another instance running. Exiting.", "WARN")
            sys.exit(1)
        try:
            entries = run_full_scan(
                product_filter=args.product,
                top_n=0,
            )
            if entries:
                print(f"\nGenerated {len(entries)} competitor-factory mappings.")
                print(f"Run --status to see full summary.")
                print(f"Run --top 10 to see best opportunities.")
            else:
                print("\nNo new mappings generated. Check input data.")
        finally:
            release_lock()


if __name__ == "__main__":
    main()
