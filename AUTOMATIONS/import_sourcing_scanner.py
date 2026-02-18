#!/usr/bin/env python3
"""
PRINTMAXX Import Sourcing Scanner - US Customs Intelligence

Finds the exact factories competitors source from using public US customs/import data.
Primary source: ImportYeti (Playwright browser automation).
Fallback: Google cached pages + DuckDuckGo + direct Alibaba supplier search.

Every US shipment is logged publicly: company, factory, volumes, dates.
Search a competitor → see their Chinese factory → contact factory directly → your own branding.

Output: LEDGER/IMPORT_SOURCING_INTEL.csv + LEDGER/CONTACT_READY_FACTORIES.csv

Usage:
    python3 import_sourcing_scanner.py --scan                    # Scan all from ECOM_ARB_OPPORTUNITIES.csv
    python3 import_sourcing_scanner.py --search "CurrentBody"    # Search specific company
    python3 import_sourcing_scanner.py --product "led face mask"  # Search by product type
    python3 import_sourcing_scanner.py --top 10                   # Top 10 sourcing opportunities
    python3 import_sourcing_scanner.py --daily                    # Cron-friendly daily scan
    python3 import_sourcing_scanner.py --status                   # Show intel summary
    python3 import_sourcing_scanner.py --export                   # Export contact-ready CSV
    python3 import_sourcing_scanner.py --report                   # Generate markdown sourcing report
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
from datetime import datetime, timedelta
from pathlib import Path

# ============================================================
# DEPENDENCIES
# ============================================================

try:
    import requests
except ImportError:
    print("[!] requests not installed. Run: pip install requests")
    sys.exit(1)

HAS_PLAYWRIGHT = False
try:
    from playwright.sync_api import sync_playwright
    HAS_PLAYWRIGHT = True
except ImportError:
    pass

# ============================================================
# PATHS & CONSTANTS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent
LEDGER_DIR = PROJECT_ROOT / "LEDGER"
AUTOMATIONS_DIR = PROJECT_ROOT / "AUTOMATIONS"
LOGS_DIR = AUTOMATIONS_DIR / "logs"
LOCK_FILE = AUTOMATIONS_DIR / ".import_scanner.lock"

# Input
ECOM_ARB_CSV = LEDGER_DIR / "ECOM_ARB_OPPORTUNITIES.csv"

# Output
INTEL_CSV = LEDGER_DIR / "IMPORT_SOURCING_INTEL.csv"
CONTACT_CSV = LEDGER_DIR / "CONTACT_READY_FACTORIES.csv"
REPORT_MD = PROJECT_ROOT / "OPS" / "SOURCING_REPORT.md"
LOG_FILE = LOGS_DIR / f"import_scanner_{datetime.now().strftime('%Y-%m-%d')}.log"

# Settings
RATE_LIMIT_SECONDS = 2.5  # delay between requests
MAX_RESULTS_PER_SEARCH = 20
REQUEST_TIMEOUT = 20
STALE_DAYS = 30  # intel older than this gets flagged

INTEL_CSV_HEADERS = [
    "scan_id", "timestamp", "query", "query_type", "source",
    "us_importer", "us_importer_address", "factory_name", "factory_location",
    "factory_country", "shipment_count", "first_shipment", "last_shipment",
    "reorder_frequency_days", "product_description", "hs_code",
    "weight_kg", "volume_estimate", "confidence", "seasonal_pattern",
    "alibaba_url", "google_url", "importyeti_url",
    "arb_product_match", "arb_margin_pct", "priority_score"
]

CONTACT_CSV_HEADERS = [
    "factory_name", "factory_location", "factory_country", "products",
    "shipment_count", "last_shipment", "reorder_frequency_days",
    "confidence", "us_importers", "alibaba_search_url", "google_contact_url",
    "made_in_china_url", "estimated_moq", "priority_score", "status", "notes"
]

USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
)

# ============================================================
# PATH SAFETY
# ============================================================

def safe_path(path: Path) -> Path:
    """Ensure all file writes stay within PROJECT_ROOT."""
    resolved = path.resolve()
    if not str(resolved).startswith(str(PROJECT_ROOT)):
        raise ValueError(f"Path {resolved} is outside project root {PROJECT_ROOT}")
    return resolved


def ensure_dirs():
    """Create required directories."""
    for d in [LEDGER_DIR, LOGS_DIR, safe_path(REPORT_MD).parent]:
        d.mkdir(parents=True, exist_ok=True)

# ============================================================
# LOCK FILE (prevent double-runs)
# ============================================================

def acquire_lock() -> bool:
    lf = safe_path(LOCK_FILE)
    if lf.exists():
        try:
            pid = int(lf.read_text().strip())
            # Check if process is still running
            os.kill(pid, 0)
            return False  # still running
        except (ProcessLookupError, ValueError, PermissionError):
            pass  # stale lock
    lf.write_text(str(os.getpid()))
    return True


def release_lock():
    lf = safe_path(LOCK_FILE)
    if lf.exists():
        lf.unlink()

# ============================================================
# LOGGING
# ============================================================

def log(msg: str, level: str = "INFO"):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] [{level}] {msg}"
    print(line)
    try:
        with open(safe_path(LOG_FILE), "a") as f:
            f.write(line + "\n")
    except Exception:
        pass

# ============================================================
# ECOM ARB INTEGRATION
# ============================================================

def load_arb_opportunities() -> list:
    """Load products from ECOM_ARB_OPPORTUNITIES.csv that have positive margins."""
    if not ECOM_ARB_CSV.exists():
        log("ECOM_ARB_OPPORTUNITIES.csv not found", "WARN")
        return []

    products = {}
    with open(ECOM_ARB_CSV, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            product = row.get("product", "").strip()
            if not product:
                continue
            try:
                margin = float(row.get("margin_pct", 0))
                sell_price = float(row.get("sell_price", 0))
                source_price = float(row.get("source_price", 0))
            except (ValueError, TypeError):
                margin = 0
                sell_price = 0
                source_price = 0

            action = row.get("action", "SKIP")
            # Keep best margin for each product
            if product not in products or margin > products[product]["margin"]:
                products[product] = {
                    "product": product,
                    "margin": margin,
                    "sell_price": sell_price,
                    "source_price": source_price,
                    "action": action,
                    "category": row.get("category", ""),
                }

    # Sort by margin descending, only positive margin products
    result = sorted(
        [p for p in products.values() if p["margin"] > 0],
        key=lambda x: x["margin"],
        reverse=True,
    )
    log(f"Loaded {len(result)} profitable products from ecom arb data")
    return result

# ============================================================
# IMPORTYETI SCRAPER (Playwright)
# ============================================================

def scrape_importyeti_playwright(query: str, query_type: str = "product") -> list:
    """
    Use Playwright to scrape ImportYeti search results.
    ImportYeti blocks requests/curl but renders in real browsers.

    ImportYeti search page renders text blocks in this pattern:
        CompanyName
        Supplier (or Company)
        Address
        Total Shipments
        N
        Most recent shipment
        MM/DD/YYYY
        Top Customers
        Customer1, Customer2, ...

    Returns list of parsed supplier/company dicts.
    """
    if not HAS_PLAYWRIGHT:
        log("Playwright not available, skipping ImportYeti scrape", "WARN")
        return []

    results = []
    url = f"https://www.importyeti.com/search?q={urllib.parse.quote(query)}"
    log(f"ImportYeti Playwright scrape: {url}")

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            ctx = browser.new_context(
                user_agent=USER_AGENT,
                viewport={"width": 1280, "height": 800},
            )
            page = ctx.new_page()
            page.goto(url, timeout=30000, wait_until="networkidle")
            time.sleep(3)  # ImportYeti uses Cloudflare + JS rendering

            # Extract the visible text from the main content area
            main_el = page.query_selector("main") or page.query_selector("#__next") or page.query_selector("body")
            if not main_el:
                browser.close()
                return []

            page_text = main_el.inner_text()
            results = _parse_importyeti_text(page_text, query)

            # Also try to get company detail pages for top results
            # Extract any company links on the page
            company_links = page.query_selector_all('a[href*="/company/"]')
            detail_urls = []
            seen_urls = set()
            for el in company_links[:10]:
                try:
                    href = el.get_attribute("href") or ""
                    if href and href not in seen_urls and "/company/" in href:
                        seen_urls.add(href)
                        full_url = f"https://www.importyeti.com{href}" if href.startswith("/") else href
                        detail_urls.append(full_url)
                except Exception:
                    pass

            # Drill into top 3 company detail pages for richer data
            for i, detail_url in enumerate(detail_urls[:3]):
                time.sleep(RATE_LIMIT_SECONDS)
                try:
                    page.goto(detail_url, timeout=30000, wait_until="networkidle")
                    time.sleep(2)
                    detail_el = page.query_selector("main") or page.query_selector("#__next")
                    if detail_el:
                        detail_text = detail_el.inner_text()
                        detail_results = _parse_importyeti_company_page(detail_text, detail_url)
                        results.extend(detail_results)
                except Exception as e:
                    log(f"Error drilling into detail page: {e}", "WARN")

            browser.close()

    except Exception as e:
        log(f"Playwright ImportYeti error: {e}", "ERROR")

    log(f"ImportYeti returned {len(results)} results for '{query}'")
    return results


def _parse_importyeti_text(text: str, query: str) -> list:
    """
    Parse ImportYeti search results page text into structured records.

    ImportYeti renders each search result as a block of text lines:
        EntityName
        Supplier|Company
        AddressLine (may be multi-line)
        Total Shipments
        N
        Most recent shipment
        MM/DD/YYYY
        Top Customers
        Customer1, Customer2, ...

    Strategy: Find all "Total Shipments" markers, then extract the block
    between successive markers. Each block = one record.
    """
    results = []
    lines = [line.strip() for line in text.split("\n") if line.strip()]

    # Find indices of all "Total Shipments" markers
    ts_indices = []
    for i, line in enumerate(lines):
        if line.lower() == "total shipments":
            ts_indices.append(i)

    if not ts_indices:
        return []

    # For each "Total Shipments" marker, parse the full record
    # The record structure around each marker:
    #   [lines above]   <- entity name, type, address
    #   Total Shipments  <- marker (ts_indices[n])
    #   N               <- shipment count
    #   Most recent shipment
    #   date
    #   Top Customers
    #   customer list
    #   [next record starts]

    # First, determine the boundary before each record.
    # The boundary is either the "Top Customers" line + customer data of previous record,
    # or the start of page content (for first record).

    for idx, ts_pos in enumerate(ts_indices):
        try:
            # Parse shipment count (line after "Total Shipments")
            if ts_pos + 1 >= len(lines):
                continue
            shipment_str = lines[ts_pos + 1].replace(",", "").strip()
            try:
                shipment_count = int(shipment_str)
            except ValueError:
                continue

            # Parse forward: Most recent shipment + Top Customers
            last_shipment = ""
            top_customers = []
            record_end = ts_pos + 2  # where this record's data ends

            k = ts_pos + 2
            while k < len(lines) and k < ts_pos + 10:
                if lines[k].lower() == "most recent shipment" and k + 1 < len(lines):
                    last_shipment = lines[k + 1]
                    k += 2
                    continue
                if lines[k].lower() == "top customers" and k + 1 < len(lines):
                    top_customers = [c.strip() for c in lines[k + 1].split(",") if c.strip()]
                    record_end = k + 2
                    break
                k += 1

            # Parse backward: find entity name, type, address
            # The start of this record is just after the previous record ends
            # For the first record, find the header boundary
            if idx == 0:
                # Walk back from ts_pos to find where content starts
                # Stop at known header lines
                start = 0
                for j in range(ts_pos - 1, -1, -1):
                    if lines[j].lower() in ("advanced search", ">"):
                        start = j + 1
                        break
                    # Also stop at page-level navigation
                    if any(lines[j].lower().startswith(x) for x in
                           ["companies", "addresses", "product finder", "type", "industry"]):
                        start = j + 1
                        break
            else:
                # Start is the end of the previous record
                # Walk forward from previous Top Customers to find entity start
                prev_ts = ts_indices[idx - 1]
                # Find where previous record's "Top Customers" + data ends
                prev_end = prev_ts + 2
                pk = prev_ts + 2
                while pk < ts_pos and pk < prev_ts + 10:
                    if lines[pk].lower() == "top customers" and pk + 1 < len(lines):
                        prev_end = pk + 2
                        break
                    pk += 1
                start = prev_end

            # Extract the lines between start and ts_pos
            header_lines = lines[start:ts_pos]

            # Parse header lines into entity_name, entity_type, address
            entity_name = ""
            entity_type = ""
            address = ""

            if len(header_lines) >= 3:
                entity_name = header_lines[0]
                if header_lines[1].lower() in ("supplier", "company"):
                    entity_type = header_lines[1].lower()
                    address = " ".join(header_lines[2:])
                else:
                    # Might not have explicit type
                    entity_type = "unknown"
                    address = " ".join(header_lines[1:])
            elif len(header_lines) == 2:
                entity_name = header_lines[0]
                if header_lines[1].lower() in ("supplier", "company"):
                    entity_type = header_lines[1].lower()
                else:
                    address = header_lines[1]
            elif len(header_lines) == 1:
                entity_name = header_lines[0]

            # Determine location from address
            location = _extract_location_from_address(address)
            country = _detect_country(address)

            # Skip navigation/header junk entries
            skip_names = {"type", "industry", "advanced search", "", "<", ">", "..."}
            if entity_name.lower() in skip_names:
                continue
            if len(entity_name) < 2:
                continue
            # Skip single generic words that match search terms
            if entity_name.lower() in ("led", "mask", "face", "light"):
                continue

            results.append({
                "entity_name": entity_name,
                "entity_type": entity_type,
                "address": address,
                "factory_location": location,
                "factory_country": country,
                "shipment_count": shipment_count,
                "last_shipment": last_shipment,
                "top_customers": top_customers,
                "source": "importyeti_search",
                "importyeti_url": importyeti_company_url(entity_name),
            })

        except Exception as e:
            log(f"Error parsing ImportYeti record at line {ts_pos}: {e}", "WARN")
            continue

    return results


def _parse_importyeti_company_page(text: str, url: str) -> list:
    """Parse an ImportYeti company detail page for supplier data."""
    results = []
    lines = [line.strip() for line in text.split("\n") if line.strip()]

    # Company pages show the company's suppliers with similar patterns
    # Look for supplier sections
    company_name = ""
    for line in lines[:5]:
        if len(line) > 3 and line.lower() not in ("supplier", "company", "overview"):
            company_name = line
            break

    # Same pattern parsing as search page
    page_results = _parse_importyeti_text(text, company_name)
    for r in page_results:
        r["detail_page_url"] = url
        r["parent_company"] = company_name
    return page_results


def _extract_location_from_address(address: str) -> str:
    """Extract city/province from an address string."""
    china_cities = [
        "Shenzhen", "Guangzhou", "Dongguan", "Yiwu", "Shanghai", "Foshan",
        "Ningbo", "Hangzhou", "Xiamen", "Wenzhou", "Zhongshan", "Jiangmen",
        "Quanzhou", "Chengdu", "Wuhan", "Changsha", "Nanjing", "Suzhou",
        "Tianjin", "Qingdao", "Dalian", "Hefei", "Kunshan", "Zhangzhou",
        "Wuxi", "Zhejiang", "Jiangxi", "Fuzhou",
    ]
    china_provinces = [
        "Guangdong", "Zhejiang", "Fujian", "Jiangsu", "Shandong",
        "Hebei", "Anhui", "Hunan", "Hubei", "Sichuan",
    ]

    addr_lower = address.lower()
    found_city = ""
    found_province = ""
    for city in china_cities:
        if city.lower() in addr_lower:
            found_city = city
            break
    for prov in china_provinces:
        if prov.lower() in addr_lower:
            found_province = prov
            break

    if found_city and found_province:
        return f"{found_city}, {found_province}"
    elif found_city:
        return found_city
    elif found_province:
        return found_province
    elif "china" in addr_lower or " cn" in addr_lower:
        return "China"
    elif "india" in addr_lower:
        return "India"
    elif "hong kong" in addr_lower:
        return "Hong Kong"
    return address[:50] if address else "Unknown"


def _detect_country(address: str) -> str:
    """Detect country code from address."""
    addr_lower = address.lower()
    # Check for Chinese city/province names as strong signal
    cn_markers = [
        "china", " cn", "shenzhen", "guangzhou", "dongguan", "yiwu",
        "shanghai", "foshan", "ningbo", "hangzhou", "xiamen", "wenzhou",
        "guangdong", "zhejiang", "fujian", "jiangsu", "shandong",
        "wuxi", "suzhou", "nanjing", "chengdu", "qingdao",
    ]
    if any(m in addr_lower for m in cn_markers):
        return "CN"
    elif "india" in addr_lower or "gujarat" in addr_lower or "delhi" in addr_lower or "mumbai" in addr_lower:
        return "IN"
    elif "hong kong" in addr_lower:
        return "HK"
    elif "taiwan" in addr_lower:
        return "TW"
    elif "vietnam" in addr_lower:
        return "VN"
    elif "korea" in addr_lower:
        return "KR"
    elif "japan" in addr_lower:
        return "JP"
    elif "canada" in addr_lower:
        return "CA"
    elif "united states" in addr_lower or "usa" in addr_lower:
        return "US"
    return "UNKNOWN"

# ============================================================
# DUCKDUCKGO FALLBACK SCRAPER
# ============================================================

def search_duckduckgo(query: str, max_results: int = 10) -> list:
    """
    Search DuckDuckGo for ImportYeti/customs data about a product or company.
    Uses the HTML version (no API key needed).
    Returns list of search result dicts.
    """
    results = []
    search_queries = [
        f'site:importyeti.com "{query}"',
        f'"{query}" supplier factory china import customs',
        f'"{query}" manufacturer china alibaba supplier',
    ]

    for sq in search_queries:
        time.sleep(RATE_LIMIT_SECONDS)
        try:
            encoded = urllib.parse.quote_plus(sq)
            url = f"https://html.duckduckgo.com/html/?q={encoded}"
            headers = {"User-Agent": USER_AGENT}
            r = requests.get(url, headers=headers, timeout=REQUEST_TIMEOUT)
            if r.status_code != 200:
                continue

            # Extract result titles and snippets
            links = re.findall(
                r'<a[^>]+class="result__a"[^>]+href="([^"]+)"[^>]*>(.*?)</a>',
                r.text, re.DOTALL
            )
            snippets = re.findall(
                r'<a[^>]+class="result__snippet"[^>]*>(.*?)</a>',
                r.text, re.DOTALL
            )

            for j, (link, title) in enumerate(links[:max_results]):
                snippet = snippets[j] if j < len(snippets) else ""
                # Clean HTML tags
                clean_title = re.sub(r'<[^>]+>', '', title).strip()
                clean_snippet = re.sub(r'<[^>]+>', '', snippet).strip()
                # Decode URL from DDG redirect
                actual_url = link
                uddg = re.search(r'uddg=([^&]+)', link)
                if uddg:
                    actual_url = urllib.parse.unquote(uddg.group(1))

                results.append({
                    "title": clean_title,
                    "snippet": clean_snippet,
                    "url": actual_url,
                    "search_query": sq,
                })

        except Exception as e:
            log(f"DuckDuckGo search error for '{sq}': {e}", "WARN")

    log(f"DuckDuckGo returned {len(results)} results for '{query}'")
    return results

# ============================================================
# FACTORY INTELLIGENCE EXTRACTION
# ============================================================

def extract_factory_intel(search_results: list, query: str) -> list:
    """
    Parse search results to extract factory/supplier intelligence.
    Looks for Chinese factory names, locations, shipment counts, etc.
    """
    intel = []
    china_cities = [
        "Shenzhen", "Guangzhou", "Dongguan", "Yiwu", "Shanghai", "Foshan",
        "Ningbo", "Hangzhou", "Xiamen", "Wenzhou", "Zhongshan", "Jiangmen",
        "Quanzhou", "Chengdu", "Wuhan", "Changsha", "Nanjing", "Suzhou",
        "Tianjin", "Qingdao", "Dalian", "Hefei", "Kunshan", "Zhangzhou",
    ]
    china_provinces = [
        "Guangdong", "Zhejiang", "Fujian", "Jiangsu", "Shandong",
        "Hebei", "Anhui", "Hunan", "Hubei", "Sichuan", "Shanghai",
    ]

    for result in search_results:
        text = f"{result.get('title', '')} {result.get('snippet', '')}"

        # Extract factory names (Chinese company naming patterns)
        factory_patterns = [
            # Standard Chinese company names
            r'((?:' + '|'.join(china_cities) + r')\s+[A-Z][a-zA-Z\s&\.]+(?:Co\.?\s*,?\s*Ltd\.?|Technology|Trading|Electronics|Industrial|Manufacturing|Lighting|Beauty|Cosmetic)(?:\s+Co\.?\s*,?\s*Ltd\.?)?)',
            # "XX Factory" / "XX Manufacturing"
            r'([A-Z][a-zA-Z\s]{3,40}(?:Factory|Manufacturing|Industrial|Trading)\s*(?:Co\.?\s*,?\s*Ltd\.?)?)',
        ]

        factories_found = []
        for pattern in factory_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            factories_found.extend(matches)

        # Extract location
        location = ""
        for city in china_cities:
            if city.lower() in text.lower():
                location = city
                for prov in china_provinces:
                    if prov.lower() in text.lower():
                        location = f"{city}, {prov}"
                        break
                break

        # Extract shipment count
        shipment_count = 0
        sc_match = re.search(r'(\d[\d,]*)\s*(?:shipments?|records?)', text, re.IGNORECASE)
        if sc_match:
            shipment_count = int(sc_match.group(1).replace(",", ""))

        # Extract US importer name (for importyeti results)
        us_importer = ""
        if "importyeti.com/company/" in result.get("url", ""):
            slug = result["url"].split("/company/")[-1].split("/")[0].split("?")[0]
            us_importer = slug.replace("-", " ").title()

        # Extract product description
        product_desc = ""
        prod_match = re.search(
            r'(?:product|item|description|shipment)[:\s]+([^.]{10,120})',
            text, re.IGNORECASE
        )
        if prod_match:
            product_desc = prod_match.group(1).strip()

        # Build intel record for each factory found
        if factories_found:
            for factory in factories_found[:3]:
                factory_clean = re.sub(r'\s+', ' ', factory).strip()
                if len(factory_clean) < 5:
                    continue
                intel.append({
                    "factory_name": factory_clean,
                    "factory_location": location or "China",
                    "factory_country": "CN",
                    "us_importer": us_importer,
                    "shipment_count": shipment_count,
                    "product_description": product_desc or query,
                    "source_url": result.get("url", ""),
                    "source": result.get("search_query", "web_search"),
                    "confidence": _calc_confidence(shipment_count, location, factory_clean),
                })
        elif us_importer:
            # Even without factory name, importer name is valuable
            intel.append({
                "factory_name": "",
                "factory_location": location or "Unknown",
                "factory_country": "CN",
                "us_importer": us_importer,
                "shipment_count": shipment_count,
                "product_description": product_desc or query,
                "source_url": result.get("url", ""),
                "source": result.get("search_query", "web_search"),
                "confidence": "LOW",
            })

    # Deduplicate by factory name
    seen = set()
    unique_intel = []
    for item in intel:
        key = (item["factory_name"].lower(), item["us_importer"].lower())
        if key not in seen:
            seen.add(key)
            unique_intel.append(item)

    return unique_intel


def _calc_confidence(shipment_count: int, location: str, factory_name: str) -> str:
    """Score confidence: HIGH (5+ shipments, known city), MEDIUM, LOW."""
    score = 0
    if shipment_count >= 10:
        score += 3
    elif shipment_count >= 5:
        score += 2
    elif shipment_count >= 1:
        score += 1

    if any(city in location for city in ["Shenzhen", "Guangzhou", "Dongguan", "Yiwu"]):
        score += 1

    if re.search(r'(?:Co\.?\s*,?\s*Ltd|Technology|Trading|Manufacturing)', factory_name, re.IGNORECASE):
        score += 1

    if score >= 4:
        return "HIGH"
    elif score >= 2:
        return "MEDIUM"
    return "LOW"

# ============================================================
# URL GENERATORS
# ============================================================

def alibaba_search_url(factory_name: str) -> str:
    """Generate Alibaba search URL for a factory."""
    q = urllib.parse.quote_plus(factory_name)
    return f"https://www.alibaba.com/trade/search?SearchText={q}&tab=supplier"


def google_factory_url(factory_name: str) -> str:
    """Generate Google search URL for factory contact info."""
    q = urllib.parse.quote_plus(f'"{factory_name}" contact email alibaba')
    return f"https://www.google.com/search?q={q}"


def made_in_china_url(product: str) -> str:
    """Generate Made-in-China search URL."""
    q = urllib.parse.quote_plus(product)
    return f"https://www.made-in-china.com/products-search/hot-china-products/{q}.html"


def importyeti_company_url(company: str) -> str:
    """Generate ImportYeti company URL."""
    slug = re.sub(r'[^a-z0-9]+', '-', company.lower()).strip('-')
    return f"https://www.importyeti.com/company/{slug}"


def importyeti_search_url(query: str) -> str:
    """Generate ImportYeti search URL."""
    q = urllib.parse.quote_plus(query)
    return f"https://www.importyeti.com/search?q={q}"

# ============================================================
# FULL SCAN PIPELINE
# ============================================================

def scan_product(product: str, arb_data: dict = None) -> list:
    """
    Full scan pipeline for a product.
    1. ImportYeti via Playwright (if available)
    2. DuckDuckGo fallback for web results
    3. Extract factory intel
    4. Generate contact URLs
    5. Score and prioritize
    """
    all_intel = []

    # Layer 1: ImportYeti via Playwright
    iy_results = scrape_importyeti_playwright(product, "product")
    for r in iy_results:
        entity_type = r.get("entity_type", "unknown")
        entity_name = r.get("entity_name", "")

        # Determine if this is a supplier (factory) or importer (US company)
        # ImportYeti labels: "Supplier" = foreign factory, "Company" = US importer
        if entity_type == "supplier":
            factory_name = entity_name
            us_importer = ""
            # Top customers listed on supplier pages are the US importers
            if r.get("top_customers"):
                us_importer = ", ".join(r["top_customers"][:3])
        else:
            factory_name = ""
            us_importer = entity_name
            # For US companies, top customers might be sub-entities, not factories

        # Skip entries that are just generic single words matching search terms
        if entity_name.lower() in ("led", "mask", "face", "light", "beauty"):
            continue

        # Parse date into our format
        date_range = {}
        if r.get("last_shipment"):
            date_range["last"] = r["last_shipment"]

        all_intel.append({
            "factory_name": factory_name,
            "factory_location": r.get("factory_location", ""),
            "factory_country": r.get("factory_country", "UNKNOWN"),
            "us_importer": us_importer,
            "shipment_count": r.get("shipment_count", 0),
            "product_description": product,
            "source": "importyeti_playwright",
            "source_url": r.get("importyeti_url", ""),
            "confidence": _calc_confidence(
                r.get("shipment_count", 0),
                r.get("factory_location", ""),
                factory_name or entity_name,
            ),
            "date_range": date_range,
            "top_customers": r.get("top_customers", []),
            "address": r.get("address", ""),
        })

    time.sleep(RATE_LIMIT_SECONDS)

    # Layer 2: DuckDuckGo web search
    ddg_results = search_duckduckgo(product)
    ddg_intel = extract_factory_intel(ddg_results, product)
    all_intel.extend(ddg_intel)

    # Layer 3: Enrich with URLs and scores
    enriched = []
    seen_factories = set()
    for item in all_intel:
        factory = item.get("factory_name", "").lower().strip()
        importer = item.get("us_importer", "").lower().strip()
        dedup_key = f"{factory}|{importer}"
        if dedup_key in seen_factories:
            continue
        seen_factories.add(dedup_key)

        # Generate URLs
        if item.get("factory_name"):
            item["alibaba_url"] = alibaba_search_url(item["factory_name"])
            item["google_url"] = google_factory_url(item["factory_name"])
        else:
            item["alibaba_url"] = alibaba_search_url(product)
            item["google_url"] = ""

        if item.get("us_importer"):
            item["importyeti_url"] = importyeti_company_url(item["us_importer"])
        else:
            item["importyeti_url"] = importyeti_search_url(product)

        # Calculate priority score (0-100)
        priority = _calc_priority_score(item, arb_data)
        item["priority_score"] = priority
        item["arb_product_match"] = product
        item["arb_margin_pct"] = arb_data.get("margin", 0) if arb_data else 0

        # Estimate reorder frequency
        date_range = item.get("date_range", {})
        shipments = item.get("shipment_count", 0)
        item["reorder_frequency_days"] = _calc_reorder_freq(date_range, shipments)

        # Detect seasonal patterns
        item["seasonal_pattern"] = _detect_seasonality(date_range)

        enriched.append(item)

    # Sort by priority
    enriched.sort(key=lambda x: x.get("priority_score", 0), reverse=True)
    return enriched


def _calc_priority_score(item: dict, arb_data: dict = None) -> int:
    """Calculate priority score 0-100 for a sourcing lead."""
    score = 0

    # Factory name found = +20
    if item.get("factory_name"):
        score += 20

    # Shipment count scoring
    sc = item.get("shipment_count", 0)
    if sc >= 50:
        score += 25
    elif sc >= 20:
        score += 20
    elif sc >= 10:
        score += 15
    elif sc >= 5:
        score += 10
    elif sc >= 1:
        score += 5

    # Confidence level
    conf = item.get("confidence", "LOW")
    if conf == "HIGH":
        score += 15
    elif conf == "MEDIUM":
        score += 10
    else:
        score += 3

    # Known location (major manufacturing hub)
    loc = item.get("factory_location", "")
    if any(c in loc for c in ["Shenzhen", "Guangzhou", "Dongguan", "Yiwu"]):
        score += 10
    elif any(c in loc for c in ["Shanghai", "Ningbo", "Hangzhou"]):
        score += 7

    # Arb margin boost: if we have positive margin data from ecom arb
    if arb_data:
        margin = arb_data.get("margin", 0)
        if margin >= 50:
            score += 15
        elif margin >= 30:
            score += 10
        elif margin >= 15:
            score += 5

    # Recent activity boost
    date_range = item.get("date_range", {})
    if date_range.get("last"):
        try:
            last = datetime.strptime(date_range["last"][:10], "%Y-%m-%d")
            days_ago = (datetime.now() - last).days
            if days_ago <= 180:
                score += 10
            elif days_ago <= 365:
                score += 5
        except (ValueError, TypeError):
            pass

    return min(score, 100)


def _calc_reorder_freq(date_range: dict, shipment_count: int) -> int:
    """Estimate reorder frequency in days from date range and shipment count."""
    if not date_range or shipment_count <= 1:
        return 0
    try:
        first = date_range.get("first", "")[:10]
        last = date_range.get("last", "")[:10]
        if not first or not last:
            return 0
        d1 = datetime.strptime(first, "%Y-%m-%d")
        d2 = datetime.strptime(last, "%Y-%m-%d")
        span = (d2 - d1).days
        if span > 0 and shipment_count > 1:
            return round(span / (shipment_count - 1))
    except (ValueError, TypeError):
        pass
    return 0


def _detect_seasonality(date_range: dict) -> str:
    """Detect if shipments show seasonal pattern."""
    # Without individual shipment dates, we can only make basic observations
    if not date_range:
        return "UNKNOWN"
    try:
        last = date_range.get("last", "")[:10]
        first = date_range.get("first", "")[:10]
        if not last or not first:
            return "UNKNOWN"
        d1 = datetime.strptime(first, "%Y-%m-%d")
        d2 = datetime.strptime(last, "%Y-%m-%d")
        span = (d2 - d1).days
        if span < 180:
            return "SHORT_HISTORY"
        elif span > 730:
            return "YEAR_ROUND"
        else:
            # Check if dates cluster in specific months
            m1, m2 = d1.month, d2.month
            if m1 >= 8 and m2 <= 12:
                return "Q4_SEASONAL"
            return "MULTI_SEASON"
    except (ValueError, TypeError):
        return "UNKNOWN"

# ============================================================
# CSV I/O
# ============================================================

def save_intel(records: list):
    """Append intel records to IMPORT_SOURCING_INTEL.csv."""
    csv_path = safe_path(INTEL_CSV)
    file_exists = csv_path.exists()

    with open(csv_path, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=INTEL_CSV_HEADERS, extrasaction="ignore")
        if not file_exists:
            writer.writeheader()

        for rec in records:
            scan_id = hashlib.md5(
                f"{rec.get('factory_name','')}{rec.get('us_importer','')}{rec.get('arb_product_match','')}".encode()
            ).hexdigest()[:12]
            row = {
                "scan_id": scan_id,
                "timestamp": datetime.now().isoformat(),
                "query": rec.get("arb_product_match", ""),
                "query_type": "product",
                "source": rec.get("source", ""),
                "us_importer": rec.get("us_importer", ""),
                "us_importer_address": "",
                "factory_name": rec.get("factory_name", ""),
                "factory_location": rec.get("factory_location", ""),
                "factory_country": rec.get("factory_country", "CN"),
                "shipment_count": rec.get("shipment_count", 0),
                "first_shipment": rec.get("date_range", {}).get("first", ""),
                "last_shipment": rec.get("date_range", {}).get("last", ""),
                "reorder_frequency_days": rec.get("reorder_frequency_days", 0),
                "product_description": rec.get("product_description", ""),
                "hs_code": "",
                "weight_kg": "",
                "volume_estimate": "",
                "confidence": rec.get("confidence", "LOW"),
                "seasonal_pattern": rec.get("seasonal_pattern", "UNKNOWN"),
                "alibaba_url": rec.get("alibaba_url", ""),
                "google_url": rec.get("google_url", ""),
                "importyeti_url": rec.get("importyeti_url", ""),
                "arb_product_match": rec.get("arb_product_match", ""),
                "arb_margin_pct": rec.get("arb_margin_pct", 0),
                "priority_score": rec.get("priority_score", 0),
            }
            writer.writerow(row)

    log(f"Saved {len(records)} records to {csv_path}")


def load_intel() -> list:
    """Load existing intel from CSV."""
    csv_path = safe_path(INTEL_CSV)
    if not csv_path.exists():
        return []
    with open(csv_path, "r") as f:
        return list(csv.DictReader(f))


def export_contact_ready():
    """
    Generate CONTACT_READY_FACTORIES.csv from intel data.
    Aggregates by factory, ranks by priority.
    """
    intel = load_intel()
    if not intel:
        log("No intel data to export", "WARN")
        return []

    # Aggregate by factory
    factories = {}
    for row in intel:
        factory = row.get("factory_name", "").strip()
        if not factory:
            continue
        key = factory.lower()
        if key not in factories:
            factories[key] = {
                "factory_name": factory,
                "factory_location": row.get("factory_location", ""),
                "factory_country": row.get("factory_country", "CN"),
                "products": set(),
                "shipment_count": 0,
                "last_shipment": "",
                "reorder_frequency_days": 0,
                "confidence": row.get("confidence", "LOW"),
                "us_importers": set(),
                "priority_scores": [],
            }
        entry = factories[key]
        if row.get("arb_product_match"):
            entry["products"].add(row["arb_product_match"])
        if row.get("product_description"):
            entry["products"].add(row["product_description"])
        try:
            entry["shipment_count"] = max(
                entry["shipment_count"], int(row.get("shipment_count", 0))
            )
        except (ValueError, TypeError):
            pass
        if row.get("last_shipment") and row["last_shipment"] > entry["last_shipment"]:
            entry["last_shipment"] = row["last_shipment"]
        try:
            entry["reorder_frequency_days"] = max(
                entry["reorder_frequency_days"],
                int(row.get("reorder_frequency_days", 0)),
            )
        except (ValueError, TypeError):
            pass
        if row.get("us_importer"):
            entry["us_importers"].add(row["us_importer"])
        try:
            entry["priority_scores"].append(int(row.get("priority_score", 0)))
        except (ValueError, TypeError):
            pass
        # Upgrade confidence if any record is higher
        conf_rank = {"HIGH": 3, "MEDIUM": 2, "LOW": 1}
        if conf_rank.get(row.get("confidence", "LOW"), 0) > conf_rank.get(entry["confidence"], 0):
            entry["confidence"] = row["confidence"]

    # Build output rows
    output = []
    for entry in factories.values():
        products_str = "; ".join(sorted(entry["products"]))[:200]
        importers_str = "; ".join(sorted(entry["us_importers"]))[:200]
        avg_priority = (
            round(sum(entry["priority_scores"]) / len(entry["priority_scores"]))
            if entry["priority_scores"]
            else 0
        )
        # Estimate MOQ based on shipment count
        if entry["shipment_count"] >= 20:
            moq = "100-500 units"
        elif entry["shipment_count"] >= 5:
            moq = "200-1000 units"
        else:
            moq = "500-2000 units"

        output.append({
            "factory_name": entry["factory_name"],
            "factory_location": entry["factory_location"],
            "factory_country": entry["factory_country"],
            "products": products_str,
            "shipment_count": entry["shipment_count"],
            "last_shipment": entry["last_shipment"],
            "reorder_frequency_days": entry["reorder_frequency_days"],
            "confidence": entry["confidence"],
            "us_importers": importers_str,
            "alibaba_search_url": alibaba_search_url(entry["factory_name"]),
            "google_contact_url": google_factory_url(entry["factory_name"]),
            "made_in_china_url": made_in_china_url(products_str.split(";")[0].strip()),
            "estimated_moq": moq,
            "priority_score": avg_priority,
            "status": "NEW",
            "notes": "",
        })

    output.sort(key=lambda x: x["priority_score"], reverse=True)

    # Write CSV
    csv_path = safe_path(CONTACT_CSV)
    with open(csv_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=CONTACT_CSV_HEADERS)
        writer.writeheader()
        writer.writerows(output)

    log(f"Exported {len(output)} factories to {csv_path}")
    return output

# ============================================================
# REPORT GENERATOR
# ============================================================

def generate_report():
    """Generate markdown sourcing report with top opportunities."""
    intel = load_intel()
    if not intel:
        log("No intel data for report", "WARN")
        return

    # Group by product
    by_product = {}
    for row in intel:
        prod = row.get("arb_product_match", row.get("query", "unknown"))
        by_product.setdefault(prod, []).append(row)

    # Stats
    total_records = len(intel)
    total_factories = len(set(r.get("factory_name", "") for r in intel if r.get("factory_name")))
    total_importers = len(set(r.get("us_importer", "") for r in intel if r.get("us_importer")))
    high_conf = sum(1 for r in intel if r.get("confidence") == "HIGH")

    ts = datetime.now().strftime("%Y-%m-%d %H:%M")

    report = f"""# PRINTMAXX Sourcing Intelligence Report

**Generated:** {ts}
**Total Intel Records:** {total_records}
**Unique Factories:** {total_factories}
**Unique US Importers:** {total_importers}
**High Confidence Leads:** {high_conf}

---

## Top 10 Sourcing Opportunities

"""
    # Sort all intel by priority_score
    sorted_intel = sorted(intel, key=lambda x: int(x.get("priority_score", 0)), reverse=True)

    for i, row in enumerate(sorted_intel[:10], 1):
        factory = row.get("factory_name", "Unknown factory")
        importer = row.get("us_importer", "Unknown importer")
        product = row.get("arb_product_match", row.get("product_description", ""))
        score = row.get("priority_score", 0)
        confidence = row.get("confidence", "LOW")
        shipments = row.get("shipment_count", 0)
        location = row.get("factory_location", "Unknown")
        margin = row.get("arb_margin_pct", 0)
        alibaba = row.get("alibaba_url", "")
        importyeti = row.get("importyeti_url", "")

        report += f"""### {i}. {factory or importer}

| Field | Value |
|-------|-------|
| **Product** | {product} |
| **Factory** | {factory} |
| **Location** | {location} |
| **US Importer** | {importer} |
| **Shipments** | {shipments} |
| **Confidence** | {confidence} |
| **Priority Score** | {score}/100 |
| **Ecom Arb Margin** | {margin}% |
| **Alibaba** | [Search]({alibaba}) |
| **ImportYeti** | [View]({importyeti}) |

"""

    # Product breakdown
    report += "\n---\n\n## Products Scanned\n\n"
    report += "| Product | Records | Factories | Best Margin | Top Priority |\n"
    report += "|---------|---------|-----------|-------------|-------------|\n"

    for prod, records in sorted(by_product.items(), key=lambda x: len(x[1]), reverse=True):
        n_factories = len(set(r.get("factory_name") for r in records if r.get("factory_name")))
        best_margin = max((float(r.get("arb_margin_pct", 0)) for r in records), default=0)
        top_priority = max((int(r.get("priority_score", 0)) for r in records), default=0)
        report += f"| {prod} | {len(records)} | {n_factories} | {best_margin:.1f}% | {top_priority}/100 |\n"

    # Action items
    report += f"""

---

## Next Actions

1. **Contact top 5 HIGH confidence factories** via Alibaba message or email
2. **Request samples** for top 3 products with highest arb margin
3. **Verify ImportYeti data** by opening the ImportYeti URLs in a browser (requires manual check)
4. **Cross-reference** factory names on Made-in-China and GlobalSources for contact info
5. **Calculate landed cost** including: factory price + shipping + customs duty + inspection

---

## How to Use This Data

1. Open the Alibaba search URL for each factory
2. Find their storefront and message them directly
3. Request: product catalog, price list, MOQ, sample pricing
4. Compare factory-direct price vs AliExpress source price from our ecom arb data
5. If factory price is 30%+ cheaper than AliExpress: order samples
6. Private label with your branding: logo, packaging, inserts

**Factory-direct vs AliExpress price difference is typically 40-70% cheaper.**
That turns a 25% margin product into a 60%+ margin product.

---

*Generated by PRINTMAXX Import Sourcing Scanner*
*Data sources: ImportYeti (US Customs), DuckDuckGo, Alibaba*
"""

    report_path = safe_path(REPORT_MD)
    report_path.write_text(report)
    log(f"Report saved to {report_path}")
    return report

# ============================================================
# STATUS / SUMMARY
# ============================================================

def show_status():
    """Print current intel summary."""
    intel = load_intel()

    print("\n" + "=" * 60)
    print("  PRINTMAXX IMPORT SOURCING INTELLIGENCE")
    print("=" * 60)

    if not intel:
        print("\n  No intel data yet. Run --scan or --product to start.\n")
        return

    total = len(intel)
    factories = set(r.get("factory_name") for r in intel if r.get("factory_name"))
    importers = set(r.get("us_importer") for r in intel if r.get("us_importer"))
    products = set(r.get("arb_product_match", r.get("query", "")) for r in intel)
    high = sum(1 for r in intel if r.get("confidence") == "HIGH")
    medium = sum(1 for r in intel if r.get("confidence") == "MEDIUM")

    print(f"\n  Total Records:        {total}")
    print(f"  Unique Factories:     {len(factories)}")
    print(f"  Unique US Importers:  {len(importers)}")
    print(f"  Products Scanned:     {len(products)}")
    print(f"  HIGH Confidence:      {high}")
    print(f"  MEDIUM Confidence:    {medium}")

    # Top 5 by priority
    sorted_intel = sorted(intel, key=lambda x: int(x.get("priority_score", 0)), reverse=True)
    print(f"\n  Top 5 Leads:")
    print(f"  {'Factory':<35} {'Product':<20} {'Score':>5} {'Conf':>6}")
    print(f"  {'-'*35} {'-'*20} {'-'*5} {'-'*6}")
    for row in sorted_intel[:5]:
        factory = (row.get("factory_name") or row.get("us_importer", "???"))[:34]
        product = row.get("arb_product_match", "")[:19]
        score = row.get("priority_score", 0)
        conf = row.get("confidence", "LOW")
        print(f"  {factory:<35} {product:<20} {score:>5} {conf:>6}")

    # Check for stale data
    stale = 0
    for row in intel:
        ts = row.get("timestamp", "")
        if ts:
            try:
                scan_date = datetime.fromisoformat(ts)
                if (datetime.now() - scan_date).days > STALE_DAYS:
                    stale += 1
            except (ValueError, TypeError):
                pass
    if stale > 0:
        print(f"\n  WARNING: {stale} records older than {STALE_DAYS} days (run --scan to refresh)")

    print(f"\n  Files:")
    print(f"    Intel CSV:     {INTEL_CSV}")
    print(f"    Contact CSV:   {CONTACT_CSV}")
    print(f"    Report:        {REPORT_MD}")
    print("=" * 60 + "\n")

# ============================================================
# CLI COMMANDS
# ============================================================

def cmd_scan(args):
    """Scan all products from ECOM_ARB_OPPORTUNITIES.csv."""
    arb_products = load_arb_opportunities()
    if not arb_products:
        log("No arb products found. Add products to ECOM_ARB_OPPORTUNITIES.csv first.")
        return

    limit = args.top if args.top else len(arb_products)
    products_to_scan = arb_products[:limit]
    log(f"Scanning {len(products_to_scan)} products from ecom arb data...")

    all_results = []
    for i, arb in enumerate(products_to_scan, 1):
        product = arb["product"]
        log(f"[{i}/{len(products_to_scan)}] Scanning: {product} (margin: {arb['margin']:.1f}%)")
        results = scan_product(product, arb)
        all_results.extend(results)
        if i < len(products_to_scan):
            time.sleep(RATE_LIMIT_SECONDS)

    if all_results:
        save_intel(all_results)
        print(f"\nSaved {len(all_results)} sourcing intel records.")
        print(f"Run --export to generate contact-ready CSV.")
        print(f"Run --report to generate full sourcing report.")
    else:
        print("\nNo results found. ImportYeti may require browser access.")
        print("Try: python3 import_sourcing_scanner.py --product 'led face mask'")


def cmd_search(args):
    """Search for a specific company."""
    company = args.search
    log(f"Searching company: {company}")

    # Search ImportYeti for this specific company
    results = scrape_importyeti_playwright(company, "company")

    # Also search via DuckDuckGo
    ddg = search_duckduckgo(f"{company} importyeti supplier factory china")
    ddg_intel = extract_factory_intel(ddg, company)

    # Merge
    all_results = []
    for r in results:
        suppliers = r.get("suppliers", [])
        for s in suppliers:
            all_results.append({
                "factory_name": s,
                "factory_location": "China",
                "factory_country": "CN",
                "us_importer": company,
                "shipment_count": r.get("shipment_count", 0),
                "product_description": "",
                "source": "importyeti_playwright",
                "source_url": r.get("importyeti_url", ""),
                "confidence": "MEDIUM",
                "date_range": r.get("date_range", {}),
                "arb_product_match": company,
                "arb_margin_pct": 0,
                "alibaba_url": alibaba_search_url(s),
                "google_url": google_factory_url(s),
                "importyeti_url": importyeti_company_url(company),
                "priority_score": 50,
                "reorder_frequency_days": 0,
                "seasonal_pattern": "UNKNOWN",
            })
    all_results.extend(ddg_intel)
    for item in ddg_intel:
        item["arb_product_match"] = company
        item["alibaba_url"] = alibaba_search_url(item.get("factory_name", company))
        item["google_url"] = google_factory_url(item.get("factory_name", company))
        item["importyeti_url"] = importyeti_company_url(company)
        item["priority_score"] = _calc_priority_score(item)

    if all_results:
        save_intel(all_results)
        print(f"\nFound {len(all_results)} sourcing records for '{company}'")
        _print_results_table(all_results)
    else:
        print(f"\nNo results for '{company}'. Try:")
        print(f"  1. Open ImportYeti manually: {importyeti_search_url(company)}")
        print(f"  2. Try a product search: --product 'led face mask'")


def cmd_product(args):
    """Search by product type."""
    product = args.product
    log(f"Searching product: {product}")

    # Check if we have arb data for this product
    arb_products = load_arb_opportunities()
    arb_data = None
    for ap in arb_products:
        if ap["product"].lower() == product.lower():
            arb_data = ap
            break

    results = scan_product(product, arb_data)

    if results:
        save_intel(results)
        print(f"\nFound {len(results)} sourcing records for '{product}'")
        if arb_data:
            print(f"  Ecom arb margin: {arb_data['margin']:.1f}%")
            print(f"  Sell price: ${arb_data['sell_price']:.2f}")
            print(f"  Source price: ${arb_data['source_price']:.2f}")
            print(f"  Factory-direct estimate: ${arb_data['source_price'] * 0.4:.2f}-${arb_data['source_price'] * 0.6:.2f}")
            print(f"  Potential margin with factory-direct: {((arb_data['sell_price'] - arb_data['source_price']*0.5) / arb_data['sell_price'] * 100):.1f}%")
        _print_results_table(results)
    else:
        print(f"\nNo results for '{product}'.")
        print(f"  ImportYeti search: {importyeti_search_url(product)}")
        print(f"  Alibaba search: {alibaba_search_url(product)}")
        print(f"  Made-in-China: {made_in_china_url(product)}")


def cmd_daily(args):
    """Cron-friendly daily scan mode."""
    log("Starting daily scan...")
    arb_products = load_arb_opportunities()
    if not arb_products:
        log("No arb products for daily scan")
        return

    # Only scan top 5 highest margin products daily
    top_products = arb_products[:5]
    all_results = []
    for arb in top_products:
        results = scan_product(arb["product"], arb)
        all_results.extend(results)
        time.sleep(RATE_LIMIT_SECONDS)

    if all_results:
        save_intel(all_results)
        export_contact_ready()
        log(f"Daily scan complete: {len(all_results)} records, {len(top_products)} products")


def cmd_export(args):
    """Export contact-ready CSV."""
    contacts = export_contact_ready()
    if contacts:
        print(f"\nExported {len(contacts)} factories to {CONTACT_CSV}")
        print("\nTop factories ready for outreach:")
        print(f"  {'Factory':<40} {'Products':<25} {'Score':>5} {'Shipments':>9}")
        print(f"  {'-'*40} {'-'*25} {'-'*5} {'-'*9}")
        for c in contacts[:10]:
            name = c["factory_name"][:39]
            prods = c["products"][:24]
            score = c["priority_score"]
            ships = c["shipment_count"]
            print(f"  {name:<40} {prods:<25} {score:>5} {ships:>9}")


def cmd_report(args):
    """Generate sourcing report."""
    report = generate_report()
    if report:
        print(f"\nReport saved to {REPORT_MD}")
        print("First 50 lines:\n")
        for line in report.split("\n")[:50]:
            print(line)


def cmd_status(args):
    """Show current intel status."""
    show_status()


def _print_results_table(results: list):
    """Print results as formatted table."""
    print(f"\n  {'#':>3} {'Type':<8} {'Name':<35} {'Location':<18} {'Ship#':>6} {'Score':>5} {'Conf':>6}")
    print(f"  {'---':>3} {'--------'} {'-'*35} {'-'*18} {'------':>6} {'-----':>5} {'------':>6}")
    for i, r in enumerate(results[:20], 1):
        factory = r.get("factory_name", "")
        importer = r.get("us_importer", "")
        if factory:
            rtype = "FACTORY"
            name = factory[:34]
        elif importer:
            rtype = "IMPORT"
            name = importer[:34]
        else:
            rtype = "?"
            name = "???"
        loc = r.get("factory_location", "?")[:17]
        ships = r.get("shipment_count", 0)
        score = r.get("priority_score", 0)
        conf = r.get("confidence", "LOW")
        print(f"  {i:>3} {rtype:<8} {name:<35} {loc:<18} {ships:>6} {score:>5} {conf:>6}")

        # Show US importers (customers) for factories
        customers = r.get("top_customers", [])
        if customers and factory:
            cust_str = ", ".join(customers[:3])
            if len(cust_str) > 70:
                cust_str = cust_str[:67] + "..."
            print(f"  {'':>3} {'':8} US Buyers: {cust_str}")

    if len(results) > 20:
        print(f"\n  ... and {len(results) - 20} more. Run --export for full CSV.")

    # Print action URLs for top factory result
    top_factory = None
    for r in results:
        if r.get("factory_name"):
            top_factory = r
            break
    if top_factory:
        print(f"\n  Quick actions for top factory: {top_factory['factory_name']}")
        if top_factory.get("alibaba_url"):
            print(f"    Alibaba:    {top_factory['alibaba_url']}")
        if top_factory.get("google_url"):
            print(f"    Google:     {top_factory['google_url']}")
        if top_factory.get("importyeti_url"):
            print(f"    ImportYeti: {top_factory['importyeti_url']}")
    elif results:
        top = results[0]
        print(f"\n  Quick actions for top result:")
        if top.get("alibaba_url"):
            print(f"    Alibaba:    {top['alibaba_url']}")
        if top.get("importyeti_url"):
            print(f"    ImportYeti: {top['importyeti_url']}")

# ============================================================
# MAIN
# ============================================================

def main():
    parser = argparse.ArgumentParser(
        description="PRINTMAXX Import Sourcing Scanner - US Customs Intelligence",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 import_sourcing_scanner.py --scan              # Scan all ecom arb products
  python3 import_sourcing_scanner.py --search "COSRX"    # Search specific company
  python3 import_sourcing_scanner.py --product "led face mask"  # Search by product
  python3 import_sourcing_scanner.py --top 5             # Top 5 products only
  python3 import_sourcing_scanner.py --daily             # Cron-friendly daily scan
  python3 import_sourcing_scanner.py --status            # Show intel summary
  python3 import_sourcing_scanner.py --export            # Export contact CSV
  python3 import_sourcing_scanner.py --report            # Full sourcing report
        """,
    )
    parser.add_argument("--scan", action="store_true", help="Scan all from ECOM_ARB_OPPORTUNITIES.csv")
    parser.add_argument("--search", type=str, help="Search specific company name")
    parser.add_argument("--product", type=str, help="Search by product type")
    parser.add_argument("--top", type=int, default=0, help="Limit to top N products")
    parser.add_argument("--daily", action="store_true", help="Cron-friendly daily scan")
    parser.add_argument("--status", action="store_true", help="Show current intel summary")
    parser.add_argument("--export", action="store_true", help="Export contact-ready CSV")
    parser.add_argument("--report", action="store_true", help="Generate sourcing report")

    args = parser.parse_args()

    ensure_dirs()

    # Default to --status if no args
    if not any([args.scan, args.search, args.product, args.daily, args.status, args.export, args.report]):
        args.status = True

    # Acquire lock for scan operations
    needs_lock = args.scan or args.daily or args.search or args.product
    if needs_lock:
        if not acquire_lock():
            log("Another scanner instance is running. Exiting.", "WARN")
            sys.exit(1)

    try:
        if args.status:
            cmd_status(args)
        elif args.export:
            cmd_export(args)
        elif args.report:
            cmd_report(args)
        elif args.scan:
            cmd_scan(args)
        elif args.search:
            cmd_search(args)
        elif args.product:
            cmd_product(args)
        elif args.daily:
            cmd_daily(args)
    except KeyboardInterrupt:
        log("Interrupted by user", "WARN")
    except Exception as e:
        log(f"Fatal error: {e}", "ERROR")
        raise
    finally:
        if needs_lock:
            release_lock()


if __name__ == "__main__":
    main()
