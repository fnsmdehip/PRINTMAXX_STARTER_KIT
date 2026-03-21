#!/usr/bin/env python3
"""
CRUNCHBASE SCANNER — Daily scan of startup funding/hiring for revenue opportunities.

Scans Crunchbase news RSS and free web data for:
  - Companies that just raised funding → EAS sales targets (they're spending)
  - Companies hiring automation/AI roles → freelance opportunities
  - Companies launching new products → competitor intel or content opportunities
  - Companies in transition → consulting opportunities

Feeds into ALPHA_STAGING → auto_approve → autonomous_integrator V2 pipeline.

Sources (no API key needed):
  - news.crunchbase.com RSS feeds
  - TechCrunch funding articles
  - Google News "startup funding" queries

Cron: 20 5 * * * (5:20 AM daily, after EDGAR scanner at 5:15 AM)

Usage:
  python3 AUTOMATIONS/crunchbase_scanner.py --scan
  python3 AUTOMATIONS/crunchbase_scanner.py --scan --focus EAS
  python3 AUTOMATIONS/crunchbase_scanner.py --status
  python3 AUTOMATIONS/crunchbase_scanner.py --dry-run

Stdlib only. Zero external dependencies.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
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
LOG_FILE = AUTOMATIONS / "logs" / "crunchbase_scanner.log"
CB_CACHE = AUTOMATIONS / "auto_ops" / "crunchbase_cache"
ALPHA_STAGING = LEDGER / "ALPHA_STAGING.csv"
LOCK_FILE = AUTOMATIONS / "locks" / "crunchbase.lock"

# No API key needed — these are public RSS/web sources
RSS_FEEDS = [
    {
        "name": "crunchbase_daily",
        "url": "https://news.crunchbase.com/feed/",
        "type": "rss",
    },
    {
        "name": "techcrunch_startups",
        "url": "https://techcrunch.com/category/startups/feed/",
        "type": "rss",
    },
    {
        "name": "techcrunch_fundings",
        "url": "https://techcrunch.com/tag/funding/feed/",
        "type": "rss",
    },
]

# Keywords that signal opportunities
OPPORTUNITY_KEYWORDS = {
    "eas_target": [
        "raised", "funding", "series a", "series b", "series c", "seed round",
        "million", "billion", "investment", "venture capital", "backed by",
        "growth stage", "expansion", "scaling", "new office",
    ],
    "automation_need": [
        "automation", "automate", "ai-powered", "machine learning",
        "digital transformation", "operational efficiency", "workflow",
        "streamline", "productivity", "saas", "platform",
    ],
    "hiring_signal": [
        "hiring", "headcount", "growing team", "new roles",
        "engineering team", "operations team", "looking for",
    ],
    "transition_signal": [
        "pivot", "restructuring", "new leadership", "ceo appointed",
        "acquisition", "acquired", "merger", "layoff", "transition",
    ],
    "freelance_signal": [
        "contractor", "freelance", "outsource", "agency",
        "consultant", "interim", "project-based",
    ],
}

# Revenue size indicators (larger = better EAS target)
REVENUE_INDICATORS = {
    "seed": ("$500K-$5M", 30),
    "series a": ("$5M-$20M", 50),
    "series b": ("$20M-$100M", 70),
    "series c": ("$100M+", 80),
    "pre-seed": ("$100K-$500K", 15),
    "ipo": ("$100M+", 75),
    "growth": ("$50M+", 65),
}

ALPHA_FIELDS = [
    "alpha_id", "source", "source_url", "category", "tactic",
    "roi_potential", "priority", "status", "applicable_methods",
    "applicable_niches", "synergy_score", "cross_sell_products",
    "implementation_priority", "engagement_authenticity",
    "earnings_verified", "extracted_method", "compliance_notes",
    "reviewer_notes", "created_at", "ops_generated",
]

USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
MIN_REQUEST_INTERVAL = 1.0  # Be polite to RSS feeds


# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------

def log(msg: str, level: str = "INFO") -> None:
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] [CRUNCHBASE] [{level}] {msg}"
    print(line)
    safe_path(LOG_FILE).parent.mkdir(parents=True, exist_ok=True)
    with open(safe_path(LOG_FILE), "a") as f:
        f.write(line + "\n")


# ---------------------------------------------------------------------------
# RSS Fetching
# ---------------------------------------------------------------------------

_last_request_time = 0.0


def fetch_rss(url: str) -> list[dict]:
    """Fetch and parse an RSS feed. Returns list of item dicts."""
    global _last_request_time

    elapsed = time.time() - _last_request_time
    if elapsed < MIN_REQUEST_INTERVAL:
        time.sleep(MIN_REQUEST_INTERVAL - elapsed)

    req = urllib.request.Request(url, headers={
        "User-Agent": USER_AGENT,
        "Accept": "application/rss+xml, application/xml, text/xml",
    })

    try:
        _last_request_time = time.time()
        with urllib.request.urlopen(req, timeout=30) as resp:
            xml_data = resp.read().decode("utf-8", errors="replace")
    except Exception as e:
        log(f"RSS fetch failed for {url[:60]}: {e}", "ERROR")
        return []

    items = []
    try:
        root = ET.fromstring(xml_data)
        # Handle both RSS 2.0 and Atom feeds
        ns = {"atom": "http://www.w3.org/2005/Atom"}

        # RSS 2.0
        for item in root.findall(".//item"):
            title = (item.findtext("title") or "").strip()
            link = (item.findtext("link") or "").strip()
            desc = (item.findtext("description") or "").strip()
            pub_date = (item.findtext("pubDate") or "").strip()
            items.append({
                "title": title,
                "link": link,
                "description": _strip_html(desc)[:1000],
                "pub_date": pub_date,
            })

        # Atom fallback
        if not items:
            for entry in root.findall(".//atom:entry", ns):
                title = (entry.findtext("atom:title", "", ns) or "").strip()
                link_el = entry.find("atom:link", ns)
                link = link_el.get("href", "") if link_el is not None else ""
                summary = (entry.findtext("atom:summary", "", ns) or "").strip()
                updated = (entry.findtext("atom:updated", "", ns) or "").strip()
                items.append({
                    "title": title,
                    "link": link,
                    "description": _strip_html(summary)[:1000],
                    "pub_date": updated,
                })
    except ET.ParseError as e:
        log(f"XML parse error: {e}", "ERROR")

    return items


def _strip_html(text: str) -> str:
    """Remove HTML tags from text."""
    return re.sub(r"<[^>]+>", "", text).strip()


# ---------------------------------------------------------------------------
# Scoring
# ---------------------------------------------------------------------------

def score_item(item: dict) -> dict:
    """Score an RSS item for opportunity potential."""
    text = f"{item.get('title', '')} {item.get('description', '')}".lower()

    # Keyword matching across categories
    category_scores: dict[str, int] = {}
    all_hits: list[str] = []

    for category, keywords in OPPORTUNITY_KEYWORDS.items():
        hits = [kw for kw in keywords if kw in text]
        if hits:
            category_scores[category] = len(hits) * 10
            all_hits.extend(hits)

    # Revenue size detection
    funding_score = 0
    funding_stage = ""
    for stage, (_, bonus) in REVENUE_INDICATORS.items():
        if stage in text:
            funding_score = max(funding_score, bonus)
            funding_stage = stage

    # Extract dollar amounts
    dollar_amounts = re.findall(r'\$(\d+(?:\.\d+)?)\s*(million|billion|m|b)', text, re.IGNORECASE)
    if dollar_amounts:
        for amount, unit in dollar_amounts:
            val = float(amount)
            if unit.lower() in ("billion", "b"):
                val *= 1000
            if val >= 100:
                funding_score = max(funding_score, 80)
            elif val >= 20:
                funding_score = max(funding_score, 60)
            elif val >= 5:
                funding_score = max(funding_score, 40)

    # Recency bonus
    recency = 10  # Default
    pub = item.get("pub_date", "")
    if pub:
        try:
            # Try common RSS date formats
            for fmt in ("%a, %d %b %Y %H:%M:%S %z", "%Y-%m-%dT%H:%M:%S%z", "%Y-%m-%d"):
                try:
                    dt = datetime.strptime(pub.strip(), fmt)
                    if dt.tzinfo:
                        dt = dt.replace(tzinfo=None)
                    days_ago = (datetime.now() - dt).days
                    recency = max(0, 20 - (days_ago * 5))
                    break
                except ValueError:
                    continue
        except Exception:
            pass

    total_score = sum(category_scores.values()) + funding_score + recency

    item["score"] = total_score
    item["keyword_hits"] = list(set(all_hits))
    item["category_scores"] = category_scores
    item["funding_stage"] = funding_stage
    item["funding_score"] = funding_score
    item["opportunity_types"] = list(category_scores.keys())

    return item


# ---------------------------------------------------------------------------
# Company name extraction
# ---------------------------------------------------------------------------

def extract_company_name(title: str) -> str:
    """Extract company name from a funding headline."""
    # Common patterns: "CompanyName Raises $XM", "CompanyName Secures Funding"
    patterns = [
        r"^(.+?)\s+(?:raises?|secures?|closes?|lands?|gets?|announces?|nabs?)\s",
        r"^(.+?)\s+(?:series\s+[a-z]|seed\s+round|funding|investment)",
        r"^(.+?)\s+(?:valued at|worth|valuation)",
    ]
    for pat in patterns:
        match = re.match(pat, title, re.IGNORECASE)
        if match:
            name = match.group(1).strip()
            # Clean up common prefixes
            name = re.sub(r"^(exclusive|breaking|update):\s*", "", name, flags=re.IGNORECASE)
            if len(name) < 50:
                return name
    # Fallback: first few words
    words = title.split()
    return " ".join(words[:3]) if words else "Unknown"


# ---------------------------------------------------------------------------
# Alpha staging integration
# ---------------------------------------------------------------------------

def get_existing_alpha_ids() -> set[str]:
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


def item_to_alpha_id(item: dict) -> str:
    key = f"CB_{item.get('link', '')}_{item.get('title', '')[:50]}"
    return f"CB{hashlib.md5(key.encode()).hexdigest()[:8].upper()}"


def write_to_alpha_staging(items: list[dict], dry_run: bool = False) -> int:
    if not items:
        return 0

    existing_ids = get_existing_alpha_ids()
    new_entries = []

    for item in items:
        alpha_id = item_to_alpha_id(item)
        if alpha_id in existing_ids:
            continue

        opp_types = item.get("opportunity_types", [])
        methods = []
        if "eas_target" in opp_types:
            methods.append("EAS outreach")
        if "automation_need" in opp_types:
            methods.append("automation consulting")
        if "hiring_signal" in opp_types:
            methods.append("freelance proposal")
        if "transition_signal" in opp_types:
            methods.append("consulting pitch")
        if "freelance_signal" in opp_types:
            methods.append("freelance bid")

        score = item.get("score", 0)
        if score >= 60:
            priority, roi = "P0", "HIGH"
        elif score >= 35:
            priority, roi = "P1", "MEDIUM"
        else:
            priority, roi = "P2", "LOW"

        company = extract_company_name(item.get("title", "Unknown"))
        funding = item.get("funding_stage", "")

        entry = {
            "alpha_id": alpha_id,
            "source": "CRUNCHBASE",
            "source_url": item.get("link", ""),
            "category": "FUNDING" if funding else "STARTUP_NEWS",
            "tactic": f"{company} — {item.get('title', '')[:80]}",
            "roi_potential": roi,
            "priority": priority,
            "status": "PENDING_REVIEW",
            "applicable_methods": "|".join(methods),
            "applicable_niches": "|".join(opp_types),
            "synergy_score": str(min(score, 100)),
            "cross_sell_products": "",
            "implementation_priority": priority,
            "engagement_authenticity": "N/A",
            "earnings_verified": "N/A",
            "extracted_method": (f"{'Funding: ' if funding else ''}{company} "
                                 f"({funding or 'news'}) — {item.get('description', '')[:200]}"),
            "compliance_notes": "Public news — fully legal",
            "reviewer_notes": (f"Score: {score}/100, Stage: {funding or 'N/A'}, "
                               f"Keywords: {', '.join(item.get('keyword_hits', [])[:5])}"),
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

def run_scan(focus: str = "", dry_run: bool = False) -> dict:
    """Run the full Crunchbase/funding scan pipeline."""
    log("Starting Crunchbase/funding scan...")

    all_items: list[dict] = []

    for feed in RSS_FEEDS:
        log(f"Fetching RSS: {feed['name']}")
        items = fetch_rss(feed["url"])
        log(f"  Got {len(items)} items from {feed['name']}")

        for item in items:
            item["feed_source"] = feed["name"]
            scored = score_item(item)
            if scored["score"] >= 20:  # Minimum threshold
                all_items.append(scored)

    # Filter by focus if specified
    if focus:
        focus_lower = focus.lower()
        all_items = [i for i in all_items
                     if focus_lower in " ".join(i.get("opportunity_types", []))]
        log(f"Filtered to {len(all_items)} items matching focus '{focus}'")

    # Deduplicate by link
    seen: set[str] = set()
    unique = []
    for item in all_items:
        link = item.get("link", "")
        if link and link not in seen:
            seen.add(link)
            unique.append(item)

    unique.sort(key=lambda x: x.get("score", 0), reverse=True)

    # Write to alpha staging
    written = write_to_alpha_staging(unique, dry_run=dry_run)

    # Cache results
    safe_path(CB_CACHE).mkdir(parents=True, exist_ok=True)
    cache_file = safe_path(CB_CACHE / f"cb_scan_{datetime.now().strftime('%Y%m%d')}.json")
    cache_data = {
        "timestamp": datetime.now().isoformat(),
        "feeds_scanned": len(RSS_FEEDS),
        "total_items": len(all_items),
        "unique_items": len(unique),
        "written_to_alpha": written,
        "top_results": [
            {
                "title": i.get("title", "")[:80],
                "company": extract_company_name(i.get("title", "")),
                "score": i.get("score", 0),
                "stage": i.get("funding_stage", ""),
                "keywords": i.get("keyword_hits", [])[:5],
                "opportunities": i.get("opportunity_types", []),
            }
            for i in unique[:20]
        ],
    }
    cache_file.write_text(json.dumps(cache_data, indent=2))

    summary = {
        "feeds": len(RSS_FEEDS),
        "total": len(all_items),
        "unique": len(unique),
        "written": written,
        "top_score": unique[0].get("score", 0) if unique else 0,
    }

    log(f"Scan complete: {len(RSS_FEEDS)} feeds, {len(unique)} unique items, "
        f"{written} new entries to ALPHA_STAGING")

    if written > 0:
        capture_skill_from_result(
            task="Crunchbase/funding daily scan for revenue opportunities",
            result=f"Scanned {len(RSS_FEEDS)} feeds, found {len(unique)} items, "
                   f"wrote {written} to alpha staging. Top score: {summary['top_score']}",
            success=True,
        )

    return summary


# ---------------------------------------------------------------------------
# Status
# ---------------------------------------------------------------------------

def show_status() -> None:
    print("=" * 60)
    print("CRUNCHBASE SCANNER — Status")
    print("=" * 60)

    if CB_CACHE.exists():
        cache_files = sorted(CB_CACHE.glob("cb_scan_*.json"), reverse=True)
        if cache_files:
            try:
                last = json.loads(cache_files[0].read_text())
                print(f"\nLast scan: {last.get('timestamp', 'unknown')}")
                print(f"Feeds scanned: {last.get('feeds_scanned', 0)}")
                print(f"Items found: {last.get('unique_items', 0)}")
                print(f"Written to alpha: {last.get('written_to_alpha', 0)}")
                print(f"\nTop results:")
                for r in last.get("top_results", [])[:5]:
                    print(f"  [{r.get('score', 0)}] {r.get('company', '')} "
                          f"({r.get('stage', 'news')}) — {', '.join(r.get('keywords', []))}")
            except Exception:
                print("Last scan: cache corrupted")
        else:
            print("No scan history")
    else:
        print("No scan history (first run)")

    cb_count = 0
    if ALPHA_STAGING.exists():
        try:
            with open(ALPHA_STAGING) as f:
                for row in csv.DictReader(f):
                    if row.get("source") == "CRUNCHBASE":
                        cb_count += 1
        except Exception:
            pass
    print(f"\nCrunchbase entries in ALPHA_STAGING: {cb_count}")

    try:
        import subprocess
        result = subprocess.run(["crontab", "-l"], capture_output=True, text=True, timeout=5)
        if "crunchbase_scanner" in result.stdout:
            print("Cron: INSTALLED")
        else:
            print("Cron: NOT INSTALLED (recommended: 20 5 * * *)")
    except Exception:
        print("Cron: unable to check")

    print("=" * 60)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(description="Crunchbase/Funding Scanner")
    parser.add_argument("--scan", action="store_true", help="Run full scan")
    parser.add_argument("--focus", type=str, default="", help="Focus on opportunity type (e.g. EAS)")
    parser.add_argument("--dry-run", action="store_true", help="Preview without writing")
    parser.add_argument("--status", action="store_true", help="Show status")
    parser.add_argument("--run", action="store_true", help="Alias for --scan")

    args = parser.parse_args()

    if args.status:
        show_status()
        return

    if args.scan or args.run or args.dry_run:
        run_scan(focus=args.focus, dry_run=args.dry_run)
        return

    parser.print_help()


if __name__ == "__main__":
    main()
