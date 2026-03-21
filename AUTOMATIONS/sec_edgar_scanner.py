#!/usr/bin/env python3
"""
SEC EDGAR SCANNER — Daily scan of SEC filings for revenue opportunities.

Scans EDGAR EFTS (full-text search) and recent filings for:
  - 8-K filings (material events) → time-sensitive consulting/freelance opportunities
  - Executive departures → companies in transition needing contractors
  - New product/service launches → market signals for EAS venture
  - M&A activity → integration consulting opportunities
  - Companies with automation-heavy operations → EAS sales targets

Feeds into ALPHA_STAGING → auto_approve → autonomous_integrator V2 pipeline.

EDGAR API: No auth required, 10 req/sec rate limit, User-Agent required.
Docs: https://efts.sec.gov/LATEST/search-index?q=...

Cron: 15 5 * * * (5:15 AM daily, after method_discovery at 5 AM)

Usage:
  python3 AUTOMATIONS/sec_edgar_scanner.py --scan
  python3 AUTOMATIONS/sec_edgar_scanner.py --scan --form-type 8-K
  python3 AUTOMATIONS/sec_edgar_scanner.py --status
  python3 AUTOMATIONS/sec_edgar_scanner.py --dry-run

Stdlib only. Zero external dependencies.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

# Ensure sibling imports
sys.path.insert(0, str(Path(__file__).resolve().parent))

from _common import PROJECT, safe_path, recall_skills_for_task, capture_skill_from_result

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

AUTOMATIONS = PROJECT / "AUTOMATIONS"
LEDGER = PROJECT / "LEDGER"
OPS = PROJECT / "OPS"
LOG_FILE = AUTOMATIONS / "logs" / "sec_edgar_scanner.log"
EDGAR_CACHE = AUTOMATIONS / "auto_ops" / "edgar_cache"
ALPHA_STAGING = LEDGER / "ALPHA_STAGING.csv"
LOCK_FILE = AUTOMATIONS / "locks" / "sec_edgar.lock"

# SEC EDGAR endpoints (no auth, free, 10 req/sec)
EDGAR_EFTS_URL = "https://efts.sec.gov/LATEST/search-index"
EDGAR_FULL_TEXT = "https://efts.sec.gov/LATEST/search-index"
EDGAR_SUBMISSIONS = "https://data.sec.gov/submissions"
EDGAR_RECENT_URL = "https://www.sec.gov/cgi-bin/browse-edgar"

# REQUIRED: SEC blocks requests without proper User-Agent
USER_AGENT = "PRINTMAXX-Research research@printmaxx.io"

# Rate limiting
MIN_REQUEST_INTERVAL = 0.12  # 10 req/sec max

# Filing types to scan
SCAN_CONFIGS = [
    {
        "form_type": "8-K",
        "description": "Material events — leadership changes, M&A, material agreements",
        "opportunity_types": ["consulting", "freelance", "EAS_target"],
        "keywords": [
            "automation", "digital transformation", "AI", "machine learning",
            "operational efficiency", "cost reduction", "restructuring",
            "departure", "resignation", "appointed", "transition",
            "acquisition", "merger", "partnership",
        ],
    },
    {
        "form_type": "8-K",
        "description": "Companies announcing hiring or expansion",
        "opportunity_types": ["freelance", "EAS_target"],
        "keywords": [
            "hiring", "expansion", "new office", "headcount",
            "contractor", "outsource", "automate processes",
        ],
    },
    {
        "form_type": "S-1",
        "description": "IPO filings — companies with money to spend",
        "opportunity_types": ["EAS_target", "content"],
        "keywords": [
            "IPO", "initial public offering", "automation", "technology platform",
        ],
    },
]

# ALPHA_STAGING schema
ALPHA_FIELDS = [
    "alpha_id", "source", "source_url", "category", "tactic",
    "roi_potential", "priority", "status", "applicable_methods",
    "applicable_niches", "synergy_score", "cross_sell_products",
    "implementation_priority", "engagement_authenticity",
    "earnings_verified", "extracted_method", "compliance_notes",
    "reviewer_notes", "created_at", "ops_generated",
]


# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------

def log(msg: str, level: str = "INFO") -> None:
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] [EDGAR] [{level}] {msg}"
    print(line)
    safe_path(LOG_FILE).parent.mkdir(parents=True, exist_ok=True)
    with open(safe_path(LOG_FILE), "a") as f:
        f.write(line + "\n")


# ---------------------------------------------------------------------------
# EDGAR API
# ---------------------------------------------------------------------------

_last_request_time = 0.0


def edgar_request(url: str, params: dict | None = None) -> dict | None:
    """Make a rate-limited request to EDGAR API. Returns parsed JSON or None."""
    global _last_request_time

    # Rate limit
    elapsed = time.time() - _last_request_time
    if elapsed < MIN_REQUEST_INTERVAL:
        time.sleep(MIN_REQUEST_INTERVAL - elapsed)

    if params:
        url = f"{url}?{urllib.parse.urlencode(params)}"

    req = urllib.request.Request(url, headers={
        "User-Agent": USER_AGENT,
        "Accept": "application/json",
    })

    try:
        _last_request_time = time.time()
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        log(f"EDGAR HTTP {e.code}: {url[:100]}", "ERROR")
        if e.code == 429:
            time.sleep(2)  # Rate limited, back off
        return None
    except Exception as e:
        log(f"EDGAR request failed: {e}", "ERROR")
        return None


def search_edgar_filings(query: str, form_type: str = "8-K",
                          date_range: str = "", max_results: int = 50) -> list[dict]:
    """Search EDGAR full-text search API for filings matching query."""
    params: dict[str, Any] = {
        "q": query,
        "dateRange": date_range or "custom",
        "startdt": (datetime.now() - timedelta(days=3)).strftime("%Y-%m-%d"),
        "enddt": datetime.now().strftime("%Y-%m-%d"),
        "forms": form_type,
    }

    # EDGAR EFTS API
    url = "https://efts.sec.gov/LATEST/search-index"
    data = edgar_request(url, params)

    if not data:
        # Fallback: try the standard full-text search
        url = "https://efts.sec.gov/LATEST/search-index"
        params_alt = {
            "q": f'"{query}" AND formType:"{form_type}"',
            "dateRange": "custom",
            "startdt": params["startdt"],
            "enddt": params["enddt"],
        }
        data = edgar_request(url, params_alt)

    if not data:
        return []

    hits = data.get("hits", {}).get("hits", [])
    results = []
    for hit in hits[:max_results]:
        source = hit.get("_source", {})
        results.append({
            "company": source.get("display_names", [source.get("entity_name", "Unknown")])[0]
                        if source.get("display_names") else source.get("entity_name", "Unknown"),
            "cik": source.get("entity_id", ""),
            "form_type": source.get("form_type", form_type),
            "filed": source.get("file_date", ""),
            "description": source.get("display_description", "")[:500],
            "url": f"https://www.sec.gov/Archives/edgar/data/{source.get('entity_id', '')}/{source.get('file_num', '')}",
            "items": source.get("items", []),
        })

    return results


def get_recent_filings(form_type: str = "8-K", count: int = 40) -> list[dict]:
    """Get most recent filings of a given type via EDGAR RSS/JSON feed."""
    # Use EDGAR full-text search with broad query for recent filings
    params = {
        "q": "*",
        "forms": form_type,
        "dateRange": "custom",
        "startdt": (datetime.now() - timedelta(days=2)).strftime("%Y-%m-%d"),
        "enddt": datetime.now().strftime("%Y-%m-%d"),
    }

    url = "https://efts.sec.gov/LATEST/search-index"
    data = edgar_request(url, params)

    if not data:
        return []

    hits = data.get("hits", {}).get("hits", [])
    results = []
    for hit in hits[:count]:
        source = hit.get("_source", {})
        results.append({
            "company": (source.get("display_names", ["Unknown"])[0]
                        if source.get("display_names") else source.get("entity_name", "Unknown")),
            "cik": source.get("entity_id", ""),
            "form_type": source.get("form_type", form_type),
            "filed": source.get("file_date", ""),
            "description": source.get("display_description", "")[:500],
            "items": source.get("items", []),
        })

    return results


# ---------------------------------------------------------------------------
# Scoring
# ---------------------------------------------------------------------------

def score_filing(filing: dict, config: dict) -> dict:
    """Score a filing for opportunity potential. Returns enriched filing dict."""
    desc = (filing.get("description", "") + " " + " ".join(filing.get("items", []))).lower()
    company = filing.get("company", "")

    # Keyword match scoring
    keyword_hits = []
    for kw in config.get("keywords", []):
        if kw.lower() in desc:
            keyword_hits.append(kw)

    keyword_score = min(len(keyword_hits) * 15, 60)  # 0-60 from keywords

    # Form type bonus
    form_bonus = {"8-K": 20, "S-1": 15, "10-K": 10, "10-Q": 5}.get(
        filing.get("form_type", ""), 5)

    # Recency bonus (filed today = 20, yesterday = 10, older = 0)
    recency = 0
    filed = filing.get("filed", "")
    if filed:
        try:
            filed_date = datetime.strptime(filed, "%Y-%m-%d")
            days_ago = (datetime.now() - filed_date).days
            recency = max(0, 20 - (days_ago * 10))
        except ValueError:
            pass

    total_score = keyword_score + form_bonus + recency

    filing["score"] = total_score
    filing["keyword_hits"] = keyword_hits
    filing["opportunity_types"] = config.get("opportunity_types", [])
    filing["config_description"] = config.get("description", "")

    return filing


# ---------------------------------------------------------------------------
# Alpha staging integration
# ---------------------------------------------------------------------------

def get_existing_alpha_ids() -> set[str]:
    """Load existing alpha IDs to avoid duplicates."""
    ids: set[str] = set()
    if not ALPHA_STAGING.exists():
        return ids
    try:
        with open(ALPHA_STAGING) as f:
            for row in csv.DictReader(f):
                aid = row.get("alpha_id", "")
                if aid:
                    ids.add(aid)
    except Exception:
        pass
    return ids


def filing_to_alpha_id(filing: dict) -> str:
    """Generate a deterministic alpha ID for a filing."""
    key = f"EDGAR_{filing.get('cik', '')}_{filing.get('form_type', '')}_{filing.get('filed', '')}"
    return f"EDGAR{hashlib.md5(key.encode()).hexdigest()[:8].upper()}"


def write_to_alpha_staging(filings: list[dict], dry_run: bool = False) -> int:
    """Write scored filings to ALPHA_STAGING.csv. Returns count written."""
    if not filings:
        return 0

    existing_ids = get_existing_alpha_ids()
    new_entries = []

    for f in filings:
        alpha_id = filing_to_alpha_id(f)
        if alpha_id in existing_ids:
            continue

        # Map opportunity types to applicable methods
        opp_types = f.get("opportunity_types", [])
        methods = []
        if "EAS_target" in opp_types:
            methods.append("EAS outreach")
        if "consulting" in opp_types:
            methods.append("consulting pitch")
        if "freelance" in opp_types:
            methods.append("freelance proposal")
        if "content" in opp_types:
            methods.append("content opportunity")

        # Map score to priority
        score = f.get("score", 0)
        if score >= 60:
            priority, roi = "P0", "HIGH"
        elif score >= 40:
            priority, roi = "P1", "MEDIUM"
        else:
            priority, roi = "P2", "LOW"

        entry = {
            "alpha_id": alpha_id,
            "source": "SEC_EDGAR",
            "source_url": f.get("url", ""),
            "category": f.get("form_type", "FILING"),
            "tactic": f"{f.get('company', 'Unknown')} — {f.get('config_description', '')}",
            "roi_potential": roi,
            "priority": priority,
            "status": "PENDING_REVIEW",
            "applicable_methods": "|".join(methods),
            "applicable_niches": "|".join(f.get("opportunity_types", [])),
            "synergy_score": str(min(score, 100)),
            "cross_sell_products": "",
            "implementation_priority": priority,
            "engagement_authenticity": "N/A",
            "earnings_verified": "N/A",
            "extracted_method": (f"SEC {f.get('form_type', '')}: {f.get('company', '')} — "
                                 f"{f.get('description', '')[:200]}"),
            "compliance_notes": "SEC public filing — fully legal to use",
            "reviewer_notes": f"Score: {score}/100, Keywords: {', '.join(f.get('keyword_hits', []))}",
            "created_at": datetime.now().isoformat(),
            "ops_generated": "no",
        }
        new_entries.append(entry)

    if not new_entries:
        return 0

    if dry_run:
        log(f"[DRY-RUN] Would write {len(new_entries)} entries to ALPHA_STAGING")
        for e in new_entries[:5]:
            log(f"  - {e['alpha_id']}: {e['tactic'][:80]}")
        return len(new_entries)

    # Append to ALPHA_STAGING
    file_exists = ALPHA_STAGING.exists()
    with open(safe_path(ALPHA_STAGING), "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=ALPHA_FIELDS)
        if not file_exists:
            writer.writeheader()
        for entry in new_entries:
            writer.writerow(entry)

    return len(new_entries)


# ---------------------------------------------------------------------------
# Scanner pipeline
# ---------------------------------------------------------------------------

def run_scan(form_type_filter: str = "", dry_run: bool = False) -> dict:
    """Run the full EDGAR scan pipeline. Returns summary dict."""
    log("Starting SEC EDGAR scan...")

    all_filings: list[dict] = []
    scan_count = 0

    for config in SCAN_CONFIGS:
        ft = config["form_type"]
        if form_type_filter and ft != form_type_filter:
            continue

        log(f"Scanning {ft}: {config['description']}")

        # Search by keywords
        for kw in config["keywords"][:8]:  # Limit API calls
            filings = search_edgar_filings(kw, form_type=ft, max_results=20)
            scan_count += 1

            for filing in filings:
                scored = score_filing(filing, config)
                if scored["score"] >= 25:  # Minimum score threshold
                    all_filings.append(scored)

            time.sleep(0.15)  # Rate limit

    # Deduplicate by CIK + form + date
    seen: set[str] = set()
    unique_filings = []
    for f in all_filings:
        key = f"{f.get('cik')}_{f.get('form_type')}_{f.get('filed')}"
        if key not in seen:
            seen.add(key)
            unique_filings.append(f)

    # Sort by score descending
    unique_filings.sort(key=lambda x: x.get("score", 0), reverse=True)

    # Write to alpha staging
    written = write_to_alpha_staging(unique_filings, dry_run=dry_run)

    # Cache results
    safe_path(EDGAR_CACHE).mkdir(parents=True, exist_ok=True)
    cache_file = safe_path(EDGAR_CACHE / f"edgar_scan_{datetime.now().strftime('%Y%m%d')}.json")
    cache_data = {
        "timestamp": datetime.now().isoformat(),
        "api_calls": scan_count,
        "total_filings": len(all_filings),
        "unique_filings": len(unique_filings),
        "written_to_alpha": written,
        "top_results": [
            {
                "company": f.get("company", ""),
                "form": f.get("form_type", ""),
                "score": f.get("score", 0),
                "keywords": f.get("keyword_hits", []),
                "opportunities": f.get("opportunity_types", []),
            }
            for f in unique_filings[:20]
        ],
    }
    cache_file.write_text(json.dumps(cache_data, indent=2))

    summary = {
        "api_calls": scan_count,
        "total_found": len(all_filings),
        "unique": len(unique_filings),
        "written": written,
        "top_score": unique_filings[0].get("score", 0) if unique_filings else 0,
    }

    log(f"Scan complete: {scan_count} API calls, {len(unique_filings)} unique filings, "
        f"{written} new entries written to ALPHA_STAGING")

    # Capture skill for procedural memory
    if written > 0:
        capture_skill_from_result(
            task="SEC EDGAR daily scan for revenue opportunities",
            result=f"Scanned {scan_count} queries, found {len(unique_filings)} filings, "
                   f"wrote {written} to alpha staging. Top score: {summary['top_score']}",
            success=True,
        )

    return summary


# ---------------------------------------------------------------------------
# Status
# ---------------------------------------------------------------------------

def show_status() -> None:
    print("=" * 60)
    print("SEC EDGAR SCANNER — Status")
    print("=" * 60)

    # Check cache for last run
    if EDGAR_CACHE.exists():
        cache_files = sorted(EDGAR_CACHE.glob("edgar_scan_*.json"), reverse=True)
        if cache_files:
            try:
                last = json.loads(cache_files[0].read_text())
                print(f"\nLast scan: {last.get('timestamp', 'unknown')}")
                print(f"API calls: {last.get('api_calls', 0)}")
                print(f"Filings found: {last.get('unique_filings', 0)}")
                print(f"Written to alpha: {last.get('written_to_alpha', 0)}")
                print(f"\nTop results:")
                for r in last.get("top_results", [])[:5]:
                    print(f"  [{r.get('score', 0)}] {r.get('company', '')} "
                          f"({r.get('form', '')}) — {', '.join(r.get('keywords', []))}")
            except Exception:
                print("Last scan: cache corrupted")
        else:
            print("No scan history found")
    else:
        print("No scan history (first run)")

    # Check EDGAR in alpha staging
    edgar_count = 0
    if ALPHA_STAGING.exists():
        try:
            with open(ALPHA_STAGING) as f:
                for row in csv.DictReader(f):
                    if row.get("source") == "SEC_EDGAR":
                        edgar_count += 1
        except Exception:
            pass
    print(f"\nEDGAR entries in ALPHA_STAGING: {edgar_count}")

    # Cron status
    try:
        import subprocess
        result = subprocess.run(["crontab", "-l"], capture_output=True, text=True, timeout=5)
        if "sec_edgar" in result.stdout:
            print("Cron: INSTALLED")
        else:
            print("Cron: NOT INSTALLED (recommended: 15 5 * * *)")
    except Exception:
        print("Cron: unable to check")

    print("=" * 60)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(description="SEC EDGAR Scanner — daily filing analysis")
    parser.add_argument("--scan", action="store_true", help="Run full scan")
    parser.add_argument("--form-type", type=str, default="", help="Filter by form type (e.g. 8-K)")
    parser.add_argument("--dry-run", action="store_true", help="Preview without writing")
    parser.add_argument("--status", action="store_true", help="Show scan status")
    parser.add_argument("--run", action="store_true", help="Alias for --scan")

    args = parser.parse_args()

    if args.status:
        show_status()
        return

    if args.scan or args.run or args.dry_run:
        run_scan(form_type_filter=args.form_type, dry_run=args.dry_run)
        return

    parser.print_help()


if __name__ == "__main__":
    main()
