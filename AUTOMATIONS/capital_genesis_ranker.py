#!/usr/bin/env python3
"""
CAPITAL GENESIS RANKER — Automated Priority Stack Generator
=============================================================

Scores ALL pending methods/ventures against the Capital Genesis framework
and outputs a daily priority stack.  CEO agent and daily engagement planner
read OPS/CAPITAL_GENESIS_PRIORITY_STACK.md to know WHAT to work on and in
WHAT ORDER.

Inputs:
  - LEDGER/ALPHA_STAGING.csv          (status=APPROVED or NEW_METHOD)
  - LEDGER/METHOD_DISCOVERY_LOG.csv   (newly discovered methods)
  - LEDGER/CAPITAL_GENESIS_LANE_STATUS.csv (existing lane statuses)
  - AUTOMATIONS/auto_ops/             (method stubs across subdirectories)
  - Master ops bridge cache           (182 ops)

Scoring Matrix (7 dimensions, weighted to 10-point composite):
  revenue_potential  x 0.25  (HIGHEST=10, HIGH=8, MEDIUM=5, LOW=2)
  speed_to_revenue   x 0.20  (1-10, higher = faster)
  downside_risk      x 0.15  (inverted: 1=high risk -> 1pt, 10=no risk -> 10pt)
  automation_potential x 0.15 (1-10, higher = more automatable)
  synergy_score      x 0.10  (1-10, cross-pollination with existing ventures)
  upfront_cost       x 0.10  (inverted: $0=10pt, $100=7pt, $500=4pt, $1000+=1pt)
  liability_risk     x 0.05  (inverted: 1=high risk -> 1pt, 10=no risk -> 10pt)

  Weights are PHASE-AWARE — auto-detected from LEDGER/FUNNEL_METRICS.csv:
    Phase 0 ($0):      speed 0.30, cost 0.20 (speed sprint, first dollar fast)
    Phase 1 ($1-1k):   balanced (default weights above)
    Phase 3 ($1k-5k):  automation 0.20, synergy 0.15 (scale what works)
    Phase 4 ($5k+):    risk 0.20, liability 0.10 (protect what you built)
  Override with --phase N.

Priority Assignment:
  P0 (DO NOW):  composite >= 7.5, upfront_cost <= $100, speed >= 6
  P1 (DO SOON): composite >= 6.0, upfront_cost <= $500
  P2 (QUEUE):   composite >= 4.5
  P3 (WATCH):   composite >= 3.0
  KILL:         composite < 3.0

Outputs:
  OPS/CAPITAL_GENESIS_PRIORITY_STACK.md   (human-readable, sorted by composite)
  LEDGER/CAPITAL_GENESIS_RANKINGS.csv     (machine-readable, all scores)

Usage:
  python3 AUTOMATIONS/capital_genesis_ranker.py --rank       # Full ranking cycle
  python3 AUTOMATIONS/capital_genesis_ranker.py --top 10     # Show top N methods
  python3 AUTOMATIONS/capital_genesis_ranker.py --p0          # Show P0 only
  python3 AUTOMATIONS/capital_genesis_ranker.py --new         # Rank only unranked methods
  python3 AUTOMATIONS/capital_genesis_ranker.py --report      # Executive summary
  python3 AUTOMATIONS/capital_genesis_ranker.py --export csv  # Export to CSV
  python3 AUTOMATIONS/capital_genesis_ranker.py --rank --phase 0  # Force pre-revenue weights

Cron:
  30 5 * * *  (5:30 AM daily, after method_discovery_crawler at 5 AM)
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any, Optional

# ---------------------------------------------------------------------------
# Bootstrap
# ---------------------------------------------------------------------------

sys.path.insert(0, str(Path(__file__).resolve().parent))

from agent_resilience import (  # noqa: E402
    TrajectoryLogger,
    safe_path,
    PROJECT_ROOT,
)
from _common import ts  # noqa: E402,F401

csv.field_size_limit(10 * 1024 * 1024)

_trajectory = TrajectoryLogger("capital_genesis_ranker")

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

PROJECT = PROJECT_ROOT
LEDGER = PROJECT / "LEDGER"
OPS = PROJECT / "OPS"
AUTOMATIONS = PROJECT / "AUTOMATIONS"
AUTO_OPS = AUTOMATIONS / "auto_ops"
LOG_DIR = AUTOMATIONS / "logs"
LOG_FILE = LOG_DIR / "capital_genesis_ranker.log"

ALPHA_CSV = LEDGER / "ALPHA_STAGING.csv"
METHOD_DISCOVERY_CSV = LEDGER / "METHOD_DISCOVERY_LOG.csv"
LANE_STATUS_CSV = LEDGER / "CAPITAL_GENESIS_LANE_STATUS.csv"
MASTER_OPS_CACHE = AUTOMATIONS / "master_ops_cache.json"

OUTPUT_MD = OPS / "CAPITAL_GENESIS_PRIORITY_STACK.md"
OUTPUT_CSV = LEDGER / "CAPITAL_GENESIS_RANKINGS.csv"

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

WEIGHTS = {
    "revenue_potential": 0.25,
    "speed_to_revenue": 0.20,
    "downside_risk": 0.15,
    "automation_potential": 0.15,
    "synergy_score": 0.10,
    "upfront_cost": 0.10,
    "liability_risk": 0.05,
}

# Phase-aware weight overrides: at $0 revenue, speed and low cost matter most.
# At scale, risk management and synergy matter more.
PHASE_WEIGHTS = {
    0: {  # $0 revenue -- speed sprint
        "revenue_potential": 0.20,
        "speed_to_revenue": 0.30,
        "downside_risk": 0.10,
        "automation_potential": 0.10,
        "synergy_score": 0.05,
        "upfront_cost": 0.20,
        "liability_risk": 0.05,
    },
    1: WEIGHTS,  # $1-1k/mo -- balanced (default)
    3: {  # $1k-5k/mo -- favor automation and synergy
        "revenue_potential": 0.25,
        "speed_to_revenue": 0.15,
        "downside_risk": 0.15,
        "automation_potential": 0.20,
        "synergy_score": 0.15,
        "upfront_cost": 0.05,
        "liability_risk": 0.05,
    },
    4: {  # $5k+/mo -- favor risk management and scaling
        "revenue_potential": 0.25,
        "speed_to_revenue": 0.10,
        "downside_risk": 0.20,
        "automation_potential": 0.15,
        "synergy_score": 0.15,
        "upfront_cost": 0.05,
        "liability_risk": 0.10,
    },
}

REVENUE_MAP = {
    "HIGHEST": 10,
    "HIGH": 8,
    "MEDIUM": 5,
    "LOW": 2,
    "NONE": 0,
}

# Ventures for synergy cross-pollination detection
VENTURES = [
    "CONTENT", "OUTBOUND", "APP_FACTORY", "LOCAL_BIZ",
    "MONETIZATION", "PRODUCT", "RESEARCH", "SCRAPING",
    "EAS", "FREELANCE", "BROKERING",
]

# Category to venture mapping for synergy computation
CATEGORY_VENTURE_MAP = {
    "CONTENT_FARM": ["CONTENT"],
    "CONTENT_FORMAT": ["CONTENT"],
    "AI_INFLUENCER": ["CONTENT", "MONETIZATION"],
    "APP_FACTORY": ["APP_FACTORY"],
    "TOOL_ALPHA": ["APP_FACTORY", "PRODUCT"],
    "OUTBOUND": ["OUTBOUND", "EAS"],
    "COLD_OUTBOUND": ["OUTBOUND", "EAS"],
    "MONETIZATION": ["MONETIZATION", "PRODUCT"],
    "ECOM": ["MONETIZATION", "PRODUCT"],
    "ECOM_ARB": ["MONETIZATION", "PRODUCT"],
    "SEO_GEO_ASO": ["CONTENT", "APP_FACTORY"],
    "GROWTH_HACK": ["CONTENT", "APP_FACTORY", "MONETIZATION"],
    "AI_ALPHA": ["RESEARCH", "APP_FACTORY"],
    "FREELANCE": ["FREELANCE", "OUTBOUND"],
    "LOCAL_BIZ": ["LOCAL_BIZ", "OUTBOUND", "EAS"],
    "NEWSLETTER": ["CONTENT", "MONETIZATION"],
    "COMMUNITY": ["CONTENT", "MONETIZATION"],
    "DIRECTORY": ["APP_FACTORY", "MONETIZATION"],
    "CHROME_EXT": ["APP_FACTORY", "PRODUCT"],
    "MCP_SERVER": ["APP_FACTORY", "PRODUCT"],
    "SAAS": ["APP_FACTORY", "PRODUCT"],
    "INFO_PRODUCTS": ["PRODUCT", "MONETIZATION"],
    "DIGITAL_PRODUCTS": ["PRODUCT", "MONETIZATION"],
    "RESEARCH": ["RESEARCH"],
    "SCRAPING": ["SCRAPING", "RESEARCH"],
    "AGENCY": ["OUTBOUND", "EAS", "FREELANCE"],
    "BROKERING": ["BROKERING", "OUTBOUND", "SCRAPING", "LOCAL_BIZ"],
    "REFERRAL": ["BROKERING", "OUTBOUND", "MONETIZATION"],
    "LEAD_GEN": ["BROKERING", "OUTBOUND", "SCRAPING", "EAS"],
    "DOMAIN_FLIPPING": ["BROKERING", "MONETIZATION"],
    "WHITE_LABEL": ["BROKERING", "PRODUCT", "CONTENT"],
    "API_ARBITRAGE": ["BROKERING", "APP_FACTORY", "MONETIZATION"],
}

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------

def rlog(msg: str, level: str = "INFO") -> None:
    """Append to ranker log + print."""
    line = f"[{ts()}] [RANKER] [{level}] {msg}"
    print(line, file=sys.stderr)
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    try:
        with open(LOG_FILE, "a") as f:
            f.write(line + "\n")
    except Exception:
        pass


# ---------------------------------------------------------------------------
# Data Ingest
# ---------------------------------------------------------------------------

def _read_csv(path: Path) -> list[dict]:
    """Read a CSV safely, return list of row dicts."""
    if not path.exists():
        return []
    rows = []
    try:
        with open(path, "r", newline="", errors="replace") as f:
            reader = csv.DictReader(f)
            for row in reader:
                rows.append(row)
    except Exception as exc:
        rlog(f"Failed to read {path.name}: {exc}", "WARN")
    return rows


def _read_master_ops_cache() -> list[dict]:
    """Read the master ops bridge JSON cache."""
    if not MASTER_OPS_CACHE.exists():
        rlog("Master ops cache not found, skipping", "WARN")
        return []
    try:
        data = json.loads(MASTER_OPS_CACHE.read_text())
        return data.get("sheets", {}).get("ALL OPS MASTER", [])
    except Exception as exc:
        rlog(f"Failed to read master ops cache: {exc}", "WARN")
        return []


def _scan_auto_ops_stubs() -> list[dict]:
    """Scan AUTOMATIONS/auto_ops/ subdirectories for method stub files."""
    stubs = []
    if not AUTO_OPS.exists():
        return stubs
    for subdir in AUTO_OPS.iterdir():
        if not subdir.is_dir():
            continue
        for f in subdir.iterdir():
            if f.suffix in (".md", ".txt") and f.is_file():
                try:
                    content = f.read_text(errors="replace")[:2000]
                    # Extract method name from filename or first heading
                    name = f.stem.replace("_", " ").replace("-", " ").title()
                    first_line = ""
                    for line in content.split("\n"):
                        stripped = line.strip().lstrip("#").strip()
                        if stripped:
                            first_line = stripped[:200]
                            break
                    stubs.append({
                        "method_id": f"STUB_{f.stem.upper()[:30]}",
                        "method_name": first_line or name,
                        "source": f"auto_ops/{subdir.name}/{f.name}",
                        "source_type": "auto_ops_stub",
                        "content": content[:500],
                        "category": subdir.name.upper(),
                    })
                except Exception:
                    pass
    return stubs


def ingest_all_methods() -> list[dict]:
    """Aggregate methods from all input sources into a unified list.

    Each method dict has at minimum:
      method_id, method_name, source, source_type, category,
      revenue_potential_raw, status
    """
    methods: list[dict] = []
    seen_ids: set[str] = set()

    # --- 1. ALPHA_STAGING.csv (APPROVED + NEW_METHOD entries) ---
    alpha_rows = _read_csv(ALPHA_CSV)
    approved_statuses = {
        "APPROVED", "ROUTED_TO_VENTURE", "QUEUED_FOR_REVIEW",
        "INTEGRATED", "NEW_METHOD", "PENDING_REVIEW", "NEW",
    }
    for row in alpha_rows:
        status = str(row.get("status", "")).strip().upper()
        if status not in approved_statuses:
            continue
        aid = str(row.get("alpha_id", "")).strip()
        if not aid or aid in seen_ids:
            continue
        seen_ids.add(aid)
        methods.append({
            "method_id": aid,
            "method_name": _extract_method_name(row),
            "source": str(row.get("source", "alpha_staging")),
            "source_type": "alpha_staging",
            "category": str(row.get("category", "GENERAL")).upper(),
            "revenue_potential_raw": str(row.get("roi_potential", "MEDIUM")).upper(),
            "status": status,
            "tactic": str(row.get("tactic", ""))[:500],
            "synergy_score_raw": str(row.get("synergy_score", "0")),
            "extracted_method": str(row.get("extracted_method", "")),
        })

    rlog(f"Ingested {len(methods)} methods from ALPHA_STAGING")

    # --- 2. METHOD_DISCOVERY_LOG.csv ---
    discovery_rows = _read_csv(METHOD_DISCOVERY_CSV)
    discovery_count = 0
    for row in discovery_rows:
        mid = str(row.get("method_id", "")).strip()
        if not mid or mid in seen_ids:
            continue
        seen_ids.add(mid)
        methods.append({
            "method_id": mid,
            "method_name": str(row.get("method_id", mid)).replace("_", " ").title(),
            "source": "method_discovery",
            "source_type": "method_discovery",
            "category": _guess_category_from_id(mid),
            "revenue_potential_raw": _map_roi_pct(row.get("roi_pct", "")),
            "status": str(row.get("decision", "NEW")).upper(),
            "tactic": str(row.get("method_id", "")),
            "revenue_per_hour_raw": str(row.get("revenue_per_hour", "0")),
            "lane_action": str(row.get("lane_action", "")),
        })
        discovery_count += 1
    rlog(f"Ingested {discovery_count} methods from METHOD_DISCOVERY_LOG")

    # --- 3. CAPITAL_GENESIS_LANE_STATUS.csv ---
    lane_rows = _read_csv(LANE_STATUS_CSV)
    lane_count = 0
    for row in lane_rows:
        mid = str(row.get("method_id", row.get("trade_id", ""))).strip()
        if not mid or mid in seen_ids:
            continue
        seen_ids.add(mid)
        methods.append({
            "method_id": mid,
            "method_name": mid.replace("_", " ").title(),
            "source": "lane_status",
            "source_type": "lane_status",
            "category": _guess_category_from_id(mid),
            "revenue_potential_raw": _map_roi_pct(row.get("roi_pct", "")),
            "status": str(row.get("decision", row.get("lane_action", "ACTIVE"))).upper(),
            "tactic": mid,
            "revenue_per_hour_raw": str(row.get("revenue_per_hour", "0")),
        })
        lane_count += 1
    rlog(f"Ingested {lane_count} methods from LANE_STATUS")

    # --- 4. Auto-ops stubs ---
    stubs = _scan_auto_ops_stubs()
    stub_count = 0
    for stub in stubs:
        sid = stub["method_id"]
        if sid in seen_ids:
            continue
        seen_ids.add(sid)
        stub.setdefault("revenue_potential_raw", "MEDIUM")
        stub.setdefault("status", "NEW")
        stub.setdefault("tactic", stub.get("content", ""))
        methods.append(stub)
        stub_count += 1
    rlog(f"Ingested {stub_count} method stubs from auto_ops/")

    # --- 5. Master ops bridge cache (ALL OPS MASTER) ---
    master_ops = _read_master_ops_cache()
    master_count = 0
    for op in master_ops:
        oid = str(op.get("OP_ID", "")).strip()
        if not oid or oid in seen_ids:
            continue
        seen_ids.add(oid)
        rev_range = str(op.get("REVENUE_RANGE", "$0"))
        methods.append({
            "method_id": oid,
            "method_name": str(op.get("OP_NAME", oid)),
            "source": "master_ops",
            "source_type": "master_ops",
            "category": str(op.get("CATEGORY", "GENERAL")).upper(),
            "revenue_potential_raw": _parse_revenue_level(rev_range),
            "status": str(op.get("STATUS", "ACTIVE")).upper(),
            "tactic": str(op.get("OP_NAME", "")),
            "revenue_range": rev_range,
            "automation_level": str(op.get("AUTOMATION_LEVEL", "")),
            "priority": str(op.get("PRIORITY", "")),
        })
        master_count += 1
    rlog(f"Ingested {master_count} ops from master ops cache")
    rlog(f"Total methods aggregated: {len(methods)}")

    return methods


# ---------------------------------------------------------------------------
# Scoring Helpers
# ---------------------------------------------------------------------------

def _extract_method_name(row: dict) -> str:
    """Pull best name from an alpha staging row."""
    extracted = str(row.get("extracted_method", "")).strip()
    if extracted and len(extracted) > 10:
        # Take first sentence
        first = extracted.split(".")[0].strip()
        if len(first) > 10:
            return first[:120]
    tactic = str(row.get("tactic", "")).strip()
    if tactic and len(tactic) > 10:
        return tactic[:120]
    return str(row.get("alpha_id", "Unknown Method"))


def _guess_category_from_id(method_id: str) -> str:
    """Guess category from a method ID string."""
    upper = method_id.upper()
    if "APP" in upper:
        return "APP_FACTORY"
    if "COLD" in upper or "OUTBOUND" in upper or "EMAIL" in upper:
        return "OUTBOUND"
    if "CONTENT" in upper or "SOCIAL" in upper or "TIKTOK" in upper:
        return "CONTENT_FARM"
    if "ECOM" in upper or "ARB" in upper or "DROP" in upper:
        return "ECOM_ARB"
    if "SEO" in upper or "ASO" in upper:
        return "SEO_GEO_ASO"
    if "AI" in upper and "AGENT" in upper:
        return "AI_ALPHA"
    if "INFLUENCER" in upper or "PERSONA" in upper:
        return "AI_INFLUENCER"
    if "NEWSLETTER" in upper:
        return "NEWSLETTER"
    if "EAS" in upper or "ENTERPRISE" in upper or "AUTOMATION_AGENCY" in upper:
        return "AGENCY"
    if "FREELANCE" in upper or "FIVERR" in upper:
        return "FREELANCE"
    if "TEMPLATE" in upper or "NOTION" in upper or "PRODUCT" in upper:
        return "DIGITAL_PRODUCTS"
    if "BROKER" in upper or "REFERRAL" in upper or "CONNECTOR" in upper:
        return "BROKERING"
    if "LEAD_GEN" in upper or "LEAD GEN" in upper:
        return "LEAD_GEN"
    if "DOMAIN" in upper and ("FLIP" in upper or "EXPIR" in upper):
        return "DOMAIN_FLIPPING"
    if "WHITE_LABEL" in upper or "WHITE LABEL" in upper:
        return "WHITE_LABEL"
    return "GENERAL"


def _map_roi_pct(val: Any) -> str:
    """Map a numeric ROI percentage to a text level."""
    try:
        pct = float(val)
        if pct >= 200:
            return "HIGHEST"
        if pct >= 100:
            return "HIGH"
        if pct >= 50:
            return "MEDIUM"
        return "LOW"
    except (ValueError, TypeError):
        return "MEDIUM"


def _parse_revenue_level(rev_range: str) -> str:
    """Parse a revenue range string like '$5k-50k/mo' into a level."""
    if not rev_range:
        return "LOW"
    upper_str = rev_range.upper()
    # Extract largest number
    numbers = re.findall(r'(\d+)', upper_str.replace(",", ""))
    has_k = "K" in upper_str
    if not numbers:
        return "MEDIUM"
    try:
        largest = max(int(n) for n in numbers)
        if has_k:
            largest = largest * 1000
        if largest >= 10000:
            return "HIGHEST"
        if largest >= 3000:
            return "HIGH"
        if largest >= 500:
            return "MEDIUM"
        return "LOW"
    except (ValueError, TypeError):
        return "MEDIUM"


# ---------------------------------------------------------------------------
# Core Scoring Engine
# ---------------------------------------------------------------------------

def score_revenue_potential(method: dict) -> float:
    """Score 0-10 based on revenue potential label."""
    raw = str(method.get("revenue_potential_raw", "MEDIUM")).upper().strip()
    return float(REVENUE_MAP.get(raw, 5))


def score_speed_to_revenue(method: dict) -> float:
    """Score 1-10 for how fast this method can generate revenue.

    Heuristics:
      - Digital products, templates, content farm: fast (7-9)
      - Apps, SaaS, directories: medium (4-6)
      - Agency, community, acquisitions: slow (2-4)
    """
    category = str(method.get("category", "")).upper()
    tactic = str(method.get("tactic", "")).lower()

    # Check for speed signals in tactic text
    fast_signals = ["immediate", "today", "hours", "24h", "72h", "quick", "instant",
                    "fast", "gumroad", "notion", "template", "content", "post"]
    slow_signals = ["months", "year", "build", "community", "acquisition",
                    "enterprise", "consulting", "course"]

    base = 5.0

    # Category-based baseline
    speed_map = {
        "DIGITAL_PRODUCTS": 8, "CONTENT_FARM": 8, "CONTENT_FORMAT": 7,
        "MONETIZATION": 7, "NEWSLETTER": 6, "AI_INFLUENCER": 6,
        "ECOM": 6, "ECOM_ARB": 7, "FREELANCE": 7,
        "OUTBOUND": 5, "COLD_OUTBOUND": 5, "GROWTH_HACK": 6,
        "APP_FACTORY": 4, "TOOL_ALPHA": 4, "AI_ALPHA": 4,
        "SEO_GEO_ASO": 3, "DIRECTORY": 4, "CHROME_EXT": 5,
        "MCP_SERVER": 5, "COMMUNITY": 3, "SAAS": 3,
        "LOCAL_BIZ": 4, "AGENCY": 4, "INFO_PRODUCTS": 6,
        "RESEARCH": 2, "SCRAPING": 3,
        "BROKERING": 5, "REFERRAL": 6, "LEAD_GEN": 6,
        "DOMAIN_FLIPPING": 5, "WHITE_LABEL": 5, "API_ARBITRAGE": 4,
    }
    base = float(speed_map.get(category, 5))

    # Adjust based on tactic text signals
    fast_hits = sum(1 for s in fast_signals if s in tactic)
    slow_hits = sum(1 for s in slow_signals if s in tactic)
    adjustment = min(fast_hits, 3) * 0.5 - min(slow_hits, 3) * 0.5

    # Revenue per hour adjustment
    try:
        rph = float(method.get("revenue_per_hour_raw", "0"))
        if rph >= 50:
            adjustment += 1.0
        elif rph >= 25:
            adjustment += 0.5
    except (ValueError, TypeError):
        pass

    return max(1.0, min(10.0, base + adjustment))


def score_downside_risk(method: dict) -> float:
    """Score 1-10 (inverted: 10 = no risk). Higher is safer."""
    category = str(method.get("category", "")).upper()
    tactic = str(method.get("tactic", "")).lower()

    # Base risk by category
    risk_map = {
        "DIGITAL_PRODUCTS": 9, "CONTENT_FARM": 8, "CONTENT_FORMAT": 8,
        "NEWSLETTER": 8, "MONETIZATION": 7, "FREELANCE": 8,
        "OUTBOUND": 7, "COLD_OUTBOUND": 7, "INFO_PRODUCTS": 8,
        "AI_INFLUENCER": 5, "APP_FACTORY": 6, "TOOL_ALPHA": 7,
        "GROWTH_HACK": 4, "ECOM": 5, "ECOM_ARB": 4,
        "SEO_GEO_ASO": 7, "AI_ALPHA": 6, "DIRECTORY": 7,
        "CHROME_EXT": 7, "MCP_SERVER": 7, "COMMUNITY": 7,
        "SAAS": 6, "LOCAL_BIZ": 6, "AGENCY": 6,
        "RESEARCH": 9, "SCRAPING": 5,
        "BROKERING": 7, "REFERRAL": 7, "LEAD_GEN": 7,
        "DOMAIN_FLIPPING": 7, "WHITE_LABEL": 8, "API_ARBITRAGE": 6,
    }
    base = float(risk_map.get(category, 6))

    # Risk signals in tactic text
    risk_signals = ["grey hat", "gray hat", "risk", "ban", "suspend",
                    "compliance", "legal", "violation", "tos"]
    safe_signals = ["proven", "legitimate", "organic", "white hat",
                    "low risk", "safe", "compliant"]

    risk_hits = sum(1 for s in risk_signals if s in tactic)
    safe_hits = sum(1 for s in safe_signals if s in tactic)

    return max(1.0, min(10.0, base - risk_hits + safe_hits * 0.5))


def score_automation_potential(method: dict) -> float:
    """Score 1-10 for how automatable this method is."""
    category = str(method.get("category", "")).upper()
    tactic = str(method.get("tactic", "")).lower()

    auto_map = {
        "CONTENT_FARM": 9, "CONTENT_FORMAT": 8, "SCRAPING": 9,
        "RESEARCH": 9, "SEO_GEO_ASO": 7, "APP_FACTORY": 6,
        "AI_ALPHA": 8, "TOOL_ALPHA": 7, "NEWSLETTER": 7,
        "DIGITAL_PRODUCTS": 5, "ECOM": 6, "ECOM_ARB": 7,
        "AI_INFLUENCER": 7, "MONETIZATION": 5, "GROWTH_HACK": 6,
        "OUTBOUND": 8, "COLD_OUTBOUND": 8, "DIRECTORY": 6,
        "CHROME_EXT": 5, "MCP_SERVER": 5, "COMMUNITY": 3,
        "SAAS": 5, "LOCAL_BIZ": 6, "AGENCY": 4,
        "FREELANCE": 4, "INFO_PRODUCTS": 4,
        "BROKERING": 8, "REFERRAL": 7, "LEAD_GEN": 9,
        "DOMAIN_FLIPPING": 8, "WHITE_LABEL": 8, "API_ARBITRAGE": 8,
    }
    base = float(auto_map.get(category, 5))

    # Check for automation level from master ops
    auto_level = str(method.get("automation_level", "")).upper()
    if "FULL" in auto_level:
        base = max(base, 8.0)
    elif "HIGH" in auto_level or "SEMI" in auto_level:
        base = max(base, 6.0)

    # Automation signals in text
    auto_signals = ["automate", "cron", "script", "bot", "scraper",
                    "pipeline", "api", "webhook", "n8n", "claude"]
    manual_signals = ["manual", "handmade", "custom", "bespoke",
                      "phone call", "in-person", "face to face"]

    auto_hits = sum(1 for s in auto_signals if s in tactic)
    manual_hits = sum(1 for s in manual_signals if s in tactic)

    return max(1.0, min(10.0, base + auto_hits * 0.3 - manual_hits * 0.5))


def score_synergy(method: dict) -> tuple[float, list[str]]:
    """Score 1-10 for cross-pollination potential. Returns (score, list of fed ventures)."""
    category = str(method.get("category", "")).upper()
    tactic = str(method.get("tactic", "")).lower()

    # Which ventures does this method feed?
    fed_ventures = list(CATEGORY_VENTURE_MAP.get(category, []))

    # Check tactic text for additional venture references
    venture_keywords = {
        "CONTENT": ["content", "post", "social", "tweet", "newsletter"],
        "OUTBOUND": ["email", "outbound", "cold", "outreach", "lead"],
        "APP_FACTORY": ["app", "mobile", "pwa", "chrome extension"],
        "LOCAL_BIZ": ["local", "smb", "small business"],
        "MONETIZATION": ["monetiz", "revenue", "gumroad", "stripe", "affiliate"],
        "PRODUCT": ["product", "template", "course", "ebook", "digital"],
        "RESEARCH": ["research", "alpha", "intelligence", "scrape", "monitor"],
        "EAS": ["enterprise", "automation", "consulting", "agency"],
        "FREELANCE": ["freelance", "fiverr", "upwork", "service"],
        "BROKERING": ["broker", "referral fee", "connector", "lead gen service", "white label", "domain flip"],
    }

    for venture, keywords in venture_keywords.items():
        if venture not in fed_ventures:
            for kw in keywords:
                if kw in tactic:
                    fed_ventures.append(venture)
                    break

    # Deduplicate
    fed_ventures = list(dict.fromkeys(fed_ventures))

    # Base synergy from raw synergy_score in alpha (0-100 scale -> 0-10)
    try:
        raw_syn = float(method.get("synergy_score_raw", "0"))
        if raw_syn > 10:
            # Raw is on 0-100 scale (e.g. "85" from Capital Genesis stacks)
            base = min(10.0, raw_syn / 10.0)
        elif raw_syn > 0:
            base = min(10.0, raw_syn)
        else:
            base = 3.0
    except (ValueError, TypeError):
        base = 3.0

    # Boost for cross-pollination breadth (additive, not override)
    venture_count = len(fed_ventures)
    breadth_bonus = min(venture_count * 0.8, 3.0)  # up to +3.0 for 4+ ventures
    if base < 7.0:
        base = min(10.0, base + breadth_bonus)
    else:
        base = min(10.0, base + breadth_bonus * 0.3)

    return max(1.0, min(10.0, base)), fed_ventures


def score_upfront_cost(method: dict) -> tuple[float, float]:
    """Score 1-10 (inverted: $0=10, $1000+=1). Returns (score, estimated_cost)."""
    tactic = str(method.get("tactic", "")).lower()
    category = str(method.get("category", "")).upper()

    # Try to extract dollar amounts from tactic
    cost_matches = re.findall(r'\$(\d[\d,]*)', tactic)
    estimated_cost = 0.0

    if cost_matches:
        try:
            costs = [float(c.replace(",", "")) for c in cost_matches]
            # Use the smallest mentioned cost as the upfront cost estimate
            # (larger numbers are usually revenue projections)
            estimated_cost = min(costs)
        except (ValueError, TypeError):
            pass

    # Category-based cost defaults if no explicit cost found
    if estimated_cost == 0.0:
        cost_defaults = {
            "DIGITAL_PRODUCTS": 0, "CONTENT_FARM": 0, "CONTENT_FORMAT": 0,
            "NEWSLETTER": 0, "RESEARCH": 0, "SCRAPING": 0,
            "SEO_GEO_ASO": 0, "AI_ALPHA": 0, "TOOL_ALPHA": 0,
            "GROWTH_HACK": 50, "FREELANCE": 0, "AI_INFLUENCER": 40,
            "OUTBOUND": 30, "COLD_OUTBOUND": 30, "MONETIZATION": 0,
            "APP_FACTORY": 100, "DIRECTORY": 100, "CHROME_EXT": 0,
            "MCP_SERVER": 0, "COMMUNITY": 100, "SAAS": 200,
            "ECOM": 200, "ECOM_ARB": 100, "LOCAL_BIZ": 50,
            "AGENCY": 50, "INFO_PRODUCTS": 0,
            "BROKERING": 0, "REFERRAL": 0, "LEAD_GEN": 0,
            "DOMAIN_FLIPPING": 30, "WHITE_LABEL": 0, "API_ARBITRAGE": 50,
        }
        estimated_cost = float(cost_defaults.get(category, 50))

    # Invert: $0=10, $100=7, $500=4, $1000+=1
    if estimated_cost <= 0:
        score = 10.0
    elif estimated_cost <= 50:
        score = 9.0
    elif estimated_cost <= 100:
        score = 7.0
    elif estimated_cost <= 250:
        score = 5.5
    elif estimated_cost <= 500:
        score = 4.0
    elif estimated_cost <= 750:
        score = 2.5
    elif estimated_cost <= 1000:
        score = 1.5
    else:
        score = 1.0

    return score, estimated_cost


def score_liability_risk(method: dict) -> float:
    """Score 1-10 (inverted: 10 = no liability risk). Covers legal, compliance, reputational."""
    category = str(method.get("category", "")).upper()
    tactic = str(method.get("tactic", "")).lower()

    liability_map = {
        "DIGITAL_PRODUCTS": 9, "CONTENT_FARM": 7, "CONTENT_FORMAT": 7,
        "NEWSLETTER": 8, "RESEARCH": 9, "SCRAPING": 5,
        "APP_FACTORY": 7, "TOOL_ALPHA": 8, "AI_ALPHA": 7,
        "OUTBOUND": 6, "COLD_OUTBOUND": 6, "MONETIZATION": 7,
        "AI_INFLUENCER": 4, "GROWTH_HACK": 4, "FREELANCE": 7,
        "ECOM": 6, "ECOM_ARB": 5, "SEO_GEO_ASO": 7,
        "DIRECTORY": 8, "CHROME_EXT": 7, "MCP_SERVER": 8,
        "COMMUNITY": 7, "SAAS": 6, "LOCAL_BIZ": 6,
        "AGENCY": 6, "INFO_PRODUCTS": 7,
        "BROKERING": 7, "REFERRAL": 7, "LEAD_GEN": 7,
        "DOMAIN_FLIPPING": 8, "WHITE_LABEL": 7, "API_ARBITRAGE": 6,
    }
    base = float(liability_map.get(category, 6))

    # Liability red flags
    red_flags = ["compliance", "ftc", "gdpr", "hipaa", "finra", "sec",
                 "income claim", "guarantee", "nsfw", "adult", "gambling",
                 "crypto", "securities", "medical", "health claim"]
    green_flags = ["open source", "mit license", "no liability",
                   "disclaimer", "transparent"]

    reds = sum(1 for s in red_flags if s in tactic)
    greens = sum(1 for s in green_flags if s in tactic)

    return max(1.0, min(10.0, base - reds * 0.5 + greens * 0.3))


def _detect_current_phase() -> int:
    """Detect current revenue phase from lane status or funnel metrics.

    Returns phase number (0-4). Defaults to 0 (pre-revenue) if no data found.
    """
    # Check funnel metrics for MRR
    funnel_path = LEDGER / "FUNNEL_METRICS.csv"
    if funnel_path.exists():
        try:
            rows = _read_csv(funnel_path)
            for row in reversed(rows):  # most recent last
                mrr = str(row.get("total_mrr", row.get("monthly_revenue", "0")))
                try:
                    val = float(mrr.replace("$", "").replace(",", ""))
                    if val >= 5000:
                        return 4
                    if val >= 1000:
                        return 3
                    if val >= 100:
                        return 1
                except (ValueError, TypeError):
                    pass
        except Exception:
            pass
    return 0  # pre-revenue default


def compute_composite(scores: dict[str, float], phase: int | None = None) -> float:
    """Weighted composite score on 0-10 scale, phase-aware."""
    if phase is None:
        phase = _detect_current_phase()
    weights = PHASE_WEIGHTS.get(phase, WEIGHTS)
    total = 0.0
    for dim, weight in weights.items():
        total += scores.get(dim, 0.0) * weight
    return round(total, 2)


def assign_priority(composite: float, upfront_cost: float, speed: float) -> str:
    """Assign P0/P1/P2/P3/KILL based on composite, cost, and speed.

    P0 threshold at 7.5 (not 8.0) because at $0 revenue, the system needs
    to surface enough actionable methods to hit first dollar fast.
    """
    if composite >= 7.5 and upfront_cost <= 100 and speed >= 6:
        return "P0"
    if composite >= 6.0 and upfront_cost <= 500:
        return "P1"
    if composite >= 4.5:
        return "P2"
    if composite >= 3.0:
        return "P3"
    return "KILL"


def recommend_action(priority: str, status: str, composite: float) -> str:
    """Recommended action based on priority and current status."""
    status_upper = status.upper()

    if priority == "KILL":
        return "KILL"

    # Already active methods -- thresholds from strategic-ethos.md:
    # Double-down: 20%+ growth at $500+ → SCALE
    # Kill: <$100 MRR/60d or <500 followers/90d → KILL
    active_statuses = {"ACTIVE", "SCALE", "SCALE_2X", "RUNNING", "LIVE"}
    if status_upper in active_statuses:
        if composite >= 7.5:
            return "SCALE"
        if composite >= 5.5:
            return "HOLD"
        if composite >= 4.0:
            return "PIVOT"
        return "KILL"

    # New or pending methods
    if priority == "P0":
        return "LAUNCH_NOW"
    if priority == "P1":
        return "LAUNCH"
    if priority == "P2":
        return "QUEUE"
    if priority == "P3":
        return "WATCH"

    return "WATCH"


# ---------------------------------------------------------------------------
# Full Ranking Pipeline
# ---------------------------------------------------------------------------

def rank_all(methods: Optional[list[dict]] = None, only_new: bool = False,
             phase_override: Optional[int] = None) -> list[dict]:
    """Score and rank all methods. Returns sorted list of ranked method dicts."""
    start = _trajectory.log_attempt("rank_all")

    if methods is None:
        methods = ingest_all_methods()

    if only_new:
        # Load previous rankings to filter
        prev_ids = set()
        if OUTPUT_CSV.exists():
            for row in _read_csv(OUTPUT_CSV):
                prev_ids.add(str(row.get("method_id", "")))
        methods = [m for m in methods if m.get("method_id") not in prev_ids]
        rlog(f"Ranking {len(methods)} new (unranked) methods")

    ranked: list[dict] = []
    phase = phase_override if phase_override is not None else _detect_current_phase()
    phase_labels = {0: "$0 (speed sprint)", 1: "$1-1k/mo", 3: "$1k-5k/mo", 4: "$5k+/mo"}
    rlog(f"Revenue phase: {phase} ({phase_labels.get(phase, 'unknown')}) — weights adjusted")

    for method in methods:
        rev_score = score_revenue_potential(method)
        speed_score = score_speed_to_revenue(method)
        risk_score = score_downside_risk(method)
        auto_score = score_automation_potential(method)
        syn_score, fed_ventures = score_synergy(method)
        cost_score, est_cost = score_upfront_cost(method)
        liab_score = score_liability_risk(method)

        scores = {
            "revenue_potential": rev_score,
            "speed_to_revenue": speed_score,
            "downside_risk": risk_score,
            "automation_potential": auto_score,
            "synergy_score": syn_score,
            "upfront_cost": cost_score,
            "liability_risk": liab_score,
        }
        composite = compute_composite(scores, phase)
        priority = assign_priority(composite, est_cost, speed_score)
        action = recommend_action(priority, method.get("status", "NEW"), composite)

        ranked.append({
            "method_id": method["method_id"],
            "method_name": method.get("method_name", "")[:120],
            "composite": composite,
            "priority": priority,
            "revenue_potential": rev_score,
            "speed_to_revenue": speed_score,
            "downside_risk": risk_score,
            "automation_potential": auto_score,
            "synergy": syn_score,
            "upfront_cost_score": cost_score,
            "liability_risk": liab_score,
            "estimated_cost": est_cost,
            "status": method.get("status", "NEW"),
            "recommended_action": action,
            "category": method.get("category", "GENERAL"),
            "source_type": method.get("source_type", "unknown"),
            "fed_ventures": ",".join(fed_ventures),
            "fed_venture_count": len(fed_ventures),
        })

    # Sort by composite descending
    ranked.sort(key=lambda x: x["composite"], reverse=True)

    # Assign rank numbers and phase metadata
    for i, entry in enumerate(ranked, 1):
        entry["rank"] = i
        entry["revenue_phase"] = phase

    _trajectory.log_success("rank_all", start, method_count=len(ranked))
    rlog(f"Ranked {len(ranked)} methods")

    return ranked


# ---------------------------------------------------------------------------
# Cross-Pollination Detection
# ---------------------------------------------------------------------------

def detect_cross_pollination(ranked: list[dict]) -> list[dict]:
    """Identify methods that feed 3+ ventures (high synergy priority boost)."""
    high_synergy = []
    for entry in ranked:
        if entry.get("fed_venture_count", 0) >= 3:
            high_synergy.append(entry)
    high_synergy.sort(key=lambda x: x.get("fed_venture_count", 0), reverse=True)
    return high_synergy


def build_synergy_map(ranked: list[dict]) -> dict[str, list[str]]:
    """Build venture -> list of methods that feed it."""
    vmap: dict[str, list[str]] = defaultdict(list)
    for entry in ranked:
        ventures = str(entry.get("fed_ventures", "")).split(",")
        for v in ventures:
            v = v.strip()
            if v:
                vmap[v].append(entry["method_id"])
    return dict(vmap)


# ---------------------------------------------------------------------------
# Output: Markdown Priority Stack
# ---------------------------------------------------------------------------

def write_priority_stack_md(ranked: list[dict]) -> None:
    """Write OPS/CAPITAL_GENESIS_PRIORITY_STACK.md."""
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    high_synergy = detect_cross_pollination(ranked)
    synergy_map = build_synergy_map(ranked)

    # Priority group counts
    pcounts = Counter(e["priority"] for e in ranked)

    lines: list[str] = []
    lines.append("# Capital Genesis Priority Stack")
    lines.append("")
    phase_labels = {0: "Phase 0 ($0 — speed sprint)", 1: "Phase 1 ($1-1k/mo)",
                    3: "Phase 3 ($1k-5k/mo)", 4: "Phase 4 ($5k+/mo)"}
    phase = ranked[0].get("revenue_phase", 0) if ranked else 0
    lines.append(f"**Generated:** {now}")
    lines.append(f"**Revenue phase:** {phase_labels.get(phase, f'Phase {phase}')}")
    lines.append(f"**Total methods ranked:** {len(ranked)}")
    lines.append(f"**P0 (DO NOW):** {pcounts.get('P0', 0)} | "
                 f"**P1 (DO SOON):** {pcounts.get('P1', 0)} | "
                 f"**P2 (QUEUE):** {pcounts.get('P2', 0)} | "
                 f"**P3 (WATCH):** {pcounts.get('P3', 0)} | "
                 f"**KILL:** {pcounts.get('KILL', 0)}")
    lines.append("")
    lines.append("---")
    lines.append("")

    # P0 Section
    p0_methods = [e for e in ranked if e["priority"] == "P0"]
    if p0_methods:
        lines.append("## P0: DO NOW (composite >= 7.5, cost <= $100, speed >= 6)")
        lines.append("")
        lines.append("| Rank | Method | Score | Action | Rev | Speed | Risk | Auto | Synergy | Cost | Category |")
        lines.append("|------|--------|-------|--------|-----|-------|------|------|---------|------|----------|")
        for e in p0_methods:
            lines.append(
                f"| {e['rank']} | {e['method_name'][:50]} | **{e['composite']}** | "
                f"{e['recommended_action']} | {e['revenue_potential']:.0f} | "
                f"{e['speed_to_revenue']:.1f} | {e['downside_risk']:.1f} | "
                f"{e['automation_potential']:.1f} | {e['synergy']:.1f} | "
                f"${e['estimated_cost']:.0f} | {e['category']} |"
            )
        lines.append("")

    # P1 Section
    p1_methods = [e for e in ranked if e["priority"] == "P1"]
    if p1_methods:
        lines.append("## P1: DO SOON (composite >= 6.0, cost <= $500)")
        lines.append("")
        lines.append("| Rank | Method | Score | Action | Rev | Speed | Risk | Auto | Synergy | Cost | Category |")
        lines.append("|------|--------|-------|--------|-----|-------|------|------|---------|------|----------|")
        for e in p1_methods:
            lines.append(
                f"| {e['rank']} | {e['method_name'][:50]} | **{e['composite']}** | "
                f"{e['recommended_action']} | {e['revenue_potential']:.0f} | "
                f"{e['speed_to_revenue']:.1f} | {e['downside_risk']:.1f} | "
                f"{e['automation_potential']:.1f} | {e['synergy']:.1f} | "
                f"${e['estimated_cost']:.0f} | {e['category']} |"
            )
        lines.append("")

    # P2 Section
    p2_methods = [e for e in ranked if e["priority"] == "P2"]
    if p2_methods:
        lines.append("## P2: QUEUE (composite >= 4.5)")
        lines.append("")
        lines.append("| Rank | Method | Score | Action | Rev | Speed | Auto | Category |")
        lines.append("|------|--------|-------|--------|-----|-------|------|----------|")
        for e in p2_methods[:50]:  # Cap display
            lines.append(
                f"| {e['rank']} | {e['method_name'][:50]} | {e['composite']} | "
                f"{e['recommended_action']} | {e['revenue_potential']:.0f} | "
                f"{e['speed_to_revenue']:.1f} | {e['automation_potential']:.1f} | "
                f"{e['category']} |"
            )
        if len(p2_methods) > 50:
            lines.append(f"| ... | +{len(p2_methods) - 50} more | | | | | | |")
        lines.append("")

    # P3 Section
    p3_methods = [e for e in ranked if e["priority"] == "P3"]
    if p3_methods:
        lines.append("## P3: WATCH (composite >= 3.0)")
        lines.append("")
        lines.append("| Rank | Method | Score | Action | Category |")
        lines.append("|------|--------|-------|--------|----------|")
        for e in p3_methods[:30]:
            lines.append(
                f"| {e['rank']} | {e['method_name'][:50]} | {e['composite']} | "
                f"{e['recommended_action']} | {e['category']} |"
            )
        if len(p3_methods) > 30:
            lines.append(f"| ... | +{len(p3_methods) - 30} more | | | |")
        lines.append("")

    # KILL Section
    kill_methods = [e for e in ranked if e["priority"] == "KILL"]
    if kill_methods:
        lines.append("## KILL (composite < 3.0)")
        lines.append("")
        lines.append(f"{len(kill_methods)} methods below threshold. Recommend reallocation of resources.")
        lines.append("")
        for e in kill_methods[:20]:
            lines.append(f"- {e['method_id']}: {e['method_name'][:60]} (score: {e['composite']})")
        if len(kill_methods) > 20:
            lines.append(f"- ... +{len(kill_methods) - 20} more")
        lines.append("")

    # Cross-Pollination Section
    lines.append("---")
    lines.append("")
    lines.append("## Cross-Pollination Map")
    lines.append("")

    if high_synergy:
        lines.append("### High Synergy Methods (feed 3+ ventures)")
        lines.append("")
        for e in high_synergy[:15]:
            ventures = e.get("fed_ventures", "")
            lines.append(
                f"- **{e['method_name'][:60]}** (score: {e['composite']}) "
                f"feeds: {ventures}"
            )
        lines.append("")

    lines.append("### Venture Feed Map")
    lines.append("")
    lines.append("| Venture | Methods Feeding It | Count |")
    lines.append("|---------|-------------------|-------|")
    for venture in sorted(synergy_map.keys()):
        method_ids = synergy_map[venture]
        display = ", ".join(method_ids[:5])
        if len(method_ids) > 5:
            display += f" +{len(method_ids) - 5} more"
        lines.append(f"| {venture} | {display} | {len(method_ids)} |")
    lines.append("")

    # Executive Summary
    lines.append("---")
    lines.append("")
    lines.append("## Executive Summary")
    lines.append("")
    if p0_methods:
        lines.append(f"**Immediate action:** {len(p0_methods)} P0 methods ready for launch. "
                     f"Top: {p0_methods[0]['method_name'][:60]} (score: {p0_methods[0]['composite']})")
    else:
        lines.append("**No P0 methods.** Review P1 pipeline for promotion candidates.")
    lines.append("")
    if high_synergy:
        lines.append(f"**High synergy alert:** {len(high_synergy)} methods feed 3+ ventures. "
                     f"Prioritize these for maximum cross-pollination.")
    lines.append("")
    total_p0_p1 = len(p0_methods) + len(p1_methods)
    lines.append(f"**Active pipeline:** {total_p0_p1} methods in P0+P1 (actionable now/soon)")
    lines.append(f"**Watch list:** {pcounts.get('P2', 0) + pcounts.get('P3', 0)} methods queued or under watch")
    lines.append(f"**Kill candidates:** {pcounts.get('KILL', 0)} methods below viability threshold")
    lines.append("")
    lines.append("---")
    lines.append(f"*Auto-generated by capital_genesis_ranker.py at {now}. "
                 f"Consumer: CEO agent, daily engagement planner.*")
    lines.append("")

    # Write
    output = safe_path(OUTPUT_MD)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(lines))
    rlog(f"Wrote priority stack to {OUTPUT_MD}")


# ---------------------------------------------------------------------------
# Output: CSV Rankings
# ---------------------------------------------------------------------------

CSV_COLUMNS = [
    "rank", "method_id", "method_name", "composite", "priority",
    "revenue_potential", "speed_to_revenue", "downside_risk",
    "automation_potential", "synergy", "upfront_cost_score",
    "liability_risk", "estimated_cost", "status", "recommended_action",
    "category", "source_type", "fed_ventures", "fed_venture_count",
    "revenue_phase",
]


def write_rankings_csv(ranked: list[dict]) -> None:
    """Write LEDGER/CAPITAL_GENESIS_RANKINGS.csv."""
    output = safe_path(OUTPUT_CSV)
    output.parent.mkdir(parents=True, exist_ok=True)
    with open(output, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_COLUMNS, extrasaction="ignore")
        writer.writeheader()
        for entry in ranked:
            writer.writerow(entry)
    rlog(f"Wrote {len(ranked)} rankings to {OUTPUT_CSV}")


# ---------------------------------------------------------------------------
# CLI Display
# ---------------------------------------------------------------------------

def display_top(ranked: list[dict], n: int = 10) -> None:
    """Display top N methods."""
    print(f"\n  Top {n} Capital Genesis Methods")
    print(f"  {'=' * 90}")
    print(f"  {'Rank':<5} {'Score':<7} {'Pri':<5} {'Action':<10} {'Method':<50} {'Category':<15}")
    print(f"  {'-' * 90}")
    for e in ranked[:n]:
        print(f"  {e['rank']:<5} {e['composite']:<7} {e['priority']:<5} "
              f"{e['recommended_action']:<10} {e['method_name'][:48]:<50} {e['category']:<15}")
    print()


def display_p0(ranked: list[dict]) -> None:
    """Display P0 methods only."""
    p0 = [e for e in ranked if e["priority"] == "P0"]
    if not p0:
        print("\n  No P0 methods found. Nothing at composite >= 7.5 with cost <= $100 and speed >= 6.\n")
        return
    print(f"\n  P0: DO NOW ({len(p0)} methods)")
    print(f"  {'=' * 100}")
    print(f"  {'Rank':<5} {'Score':<7} {'Action':<8} {'Rev':<5} {'Spd':<5} {'Risk':<5} "
          f"{'Auto':<5} {'Syn':<5} {'Cost':<7} {'Method':<40}")
    print(f"  {'-' * 100}")
    for e in p0:
        print(f"  {e['rank']:<5} {e['composite']:<7} {e['recommended_action']:<8} "
              f"{e['revenue_potential']:<5.0f} {e['speed_to_revenue']:<5.1f} "
              f"{e['downside_risk']:<5.1f} {e['automation_potential']:<5.1f} "
              f"{e['synergy']:<5.1f} ${e['estimated_cost']:<6.0f} "
              f"{e['method_name'][:38]:<40}")
    print()


def display_report(ranked: list[dict]) -> None:
    """Executive summary report."""
    pcounts = Counter(e["priority"] for e in ranked)
    action_counts = Counter(e["recommended_action"] for e in ranked)
    category_counts = Counter(e["category"] for e in ranked)
    high_synergy = detect_cross_pollination(ranked)

    # Score distribution
    avg_score = sum(e["composite"] for e in ranked) / max(len(ranked), 1)
    top_10_avg = sum(e["composite"] for e in ranked[:10]) / min(10, max(len(ranked), 1))

    phase = ranked[0].get("revenue_phase", 0) if ranked else 0
    phase_labels = {0: "$0 (speed sprint)", 1: "$1-1k/mo", 3: "$1k-5k/mo", 4: "$5k+/mo"}

    print(f"\n  Capital Genesis Ranker - Executive Report")
    print(f"  {'=' * 60}")
    print(f"  Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"  Revenue phase: {phase_labels.get(phase, f'Phase {phase}')}")
    print(f"  Total methods ranked: {len(ranked)}")
    print(f"  Average composite score: {avg_score:.2f}")
    print(f"  Top 10 average score: {top_10_avg:.2f}")
    print()

    print(f"  Priority Distribution:")
    for p in ["P0", "P1", "P2", "P3", "KILL"]:
        count = pcounts.get(p, 0)
        bar = "#" * min(count, 40)
        print(f"    {p:<6} {count:>4}  {bar}")
    print()

    print(f"  Action Breakdown:")
    for action in ["LAUNCH_NOW", "LAUNCH", "SCALE", "HOLD", "QUEUE", "WATCH", "PIVOT", "KILL"]:
        count = action_counts.get(action, 0)
        if count > 0:
            print(f"    {action:<10} {count:>4}")
    print()

    print(f"  Top Categories:")
    for cat, count in category_counts.most_common(10):
        print(f"    {cat:<25} {count:>4}")
    print()

    if high_synergy:
        print(f"  High Synergy Methods (3+ ventures):")
        for e in high_synergy[:5]:
            print(f"    {e['method_name'][:50]} -> {e['fed_ventures']}")
    print()

    if ranked:
        print(f"  Top 5 Methods:")
        for e in ranked[:5]:
            print(f"    #{e['rank']} {e['composite']:.2f} [{e['priority']}] "
                  f"{e['method_name'][:50]}")
    print()


# ---------------------------------------------------------------------------
# Main CLI
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Capital Genesis Ranker: score and prioritize all methods/ventures.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Examples:\n"
            "  python3 AUTOMATIONS/capital_genesis_ranker.py --rank\n"
            "  python3 AUTOMATIONS/capital_genesis_ranker.py --top 20\n"
            "  python3 AUTOMATIONS/capital_genesis_ranker.py --p0\n"
            "  python3 AUTOMATIONS/capital_genesis_ranker.py --new\n"
            "  python3 AUTOMATIONS/capital_genesis_ranker.py --report\n"
            "  python3 AUTOMATIONS/capital_genesis_ranker.py --export csv\n"
            "\n"
            "Cron: 30 5 * * * (5:30 AM daily)\n"
        ),
    )
    parser.add_argument("--rank", action="store_true",
                        help="Full ranking cycle: ingest, score, output MD + CSV")
    parser.add_argument("--top", type=int, metavar="N",
                        help="Show top N methods (runs ranking if needed)")
    parser.add_argument("--p0", action="store_true",
                        help="Show P0 (DO NOW) methods only")
    parser.add_argument("--new", action="store_true",
                        help="Rank only unranked/new methods")
    parser.add_argument("--report", action="store_true",
                        help="Executive summary report")
    parser.add_argument("--export", type=str, metavar="FORMAT",
                        help="Export format: 'csv' (writes to LEDGER/)")
    parser.add_argument("--phase", type=int, metavar="N", choices=[0, 1, 3, 4],
                        help="Override revenue phase (0=pre-revenue, 1=$1-1k, 3=$1k-5k, 4=$5k+)")

    args = parser.parse_args()

    # Default: show help if no args
    if not any([args.rank, args.top, args.p0, args.new, args.report, args.export, args.phase is not None]):
        parser.print_help()
        return

    rlog("=== Capital Genesis Ranker starting ===")

    # Run ranking
    ranked = rank_all(only_new=args.new, phase_override=args.phase)

    if args.rank or args.new:
        write_priority_stack_md(ranked)
        write_rankings_csv(ranked)
        rlog("Full ranking cycle complete")
        display_report(ranked)

    if args.top:
        display_top(ranked, args.top)

    if args.p0:
        display_p0(ranked)

    if args.report and not args.rank and not args.new:
        display_report(ranked)

    if args.export and args.export.lower() == "csv":
        write_rankings_csv(ranked)
        print(f"\n  Exported to {OUTPUT_CSV}\n")

    rlog("=== Capital Genesis Ranker complete ===")


if __name__ == "__main__":
    main()
