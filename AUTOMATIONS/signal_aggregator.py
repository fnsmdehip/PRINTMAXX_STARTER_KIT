#!/usr/bin/env python3

from __future__ import annotations
"""
PRINTMAXX Signal Aggregator - Fuse intelligence from ALL scanners into ranked opportunities.

Reads from: FREELANCE_DEMAND_SCAN, ECOM_ARB_OPPORTUNITIES, TREND_SIGNALS, ALPHA_STAGING,
overnight logs, and scraper outputs. Applies time-decay, source weighting, multi-source
fusion, and confidence boosting to produce a single ranked list of opportunities.

Usage:
    python3 AUTOMATIONS/signal_aggregator.py --scan           # Full signal aggregation
    python3 AUTOMATIONS/signal_aggregator.py --top 10         # Top 10 opportunities
    python3 AUTOMATIONS/signal_aggregator.py --alerts         # High-confidence alerts only
    python3 AUTOMATIONS/signal_aggregator.py --history        # Signal trend over time
    python3 AUTOMATIONS/signal_aggregator.py --source freelance  # Filter by source
    python3 AUTOMATIONS/signal_aggregator.py --category CONTENT  # Filter by op category
"""

import os
import sys
import csv
import json
import math
import argparse
import glob as glob_mod
from datetime import datetime, timedelta
from pathlib import Path
from collections import defaultdict

BASE = Path(__file__).resolve().parent.parent
LEDGER = BASE / "LEDGER"
AUTOMATIONS = BASE / "AUTOMATIONS"
OPS = BASE / "OPS"

FUSED_OUTPUT = LEDGER / "FUSED_SIGNALS.csv"
HISTORY_OUTPUT = LEDGER / "SIGNAL_HISTORY.jsonl"

# ============================================================================
# SOURCE CONFIGURATION
# ============================================================================

SOURCE_CONFIG = {
    "freelance_demand": {
        "path": LEDGER / "FREELANCE_DEMAND_SCAN.csv",
        "reliability": 0.85,
        "description": "Reddit hiring posts matched to our services",
        "signal_type": "demand",
    },
    "ecom_arb": {
        "path": LEDGER / "ECOM_ARB_OPPORTUNITIES.csv",
        "reliability": 0.75,
        "description": "Product arbitrage opportunities with margin calculation",
        "signal_type": "opportunity",
    },
    "trend_signals": {
        "path": LEDGER / "TREND_SIGNALS.csv",
        "reliability": 0.70,
        "description": "Multi-source trend detection (Google Trends + Reddit + PH)",
        "signal_type": "trend",
    },
    "alpha_staging": {
        "path": LEDGER / "ALPHA_STAGING.csv",
        "reliability": 0.90,
        "description": "Curated alpha intelligence entries",
        "signal_type": "alpha",
    },
}

# Category mapping for signals
SIGNAL_TO_CATEGORY = {
    # Freelance demand keywords -> op categories
    "website": "SERVICE",
    "automation": "SERVICE",
    "cold_email": "OUTBOUND",
    "video_editing": "CONTENT",
    "social_media": "CONTENT",
    "logo": "SERVICE",
    "data_entry": "SERVICE",
    "ai": "SERVICE",
    # Ecom product categories -> op categories
    "beauty": "ECOM",
    "fitness": "ECOM",
    "tech": "ECOM",
    "health": "ECOM",
    "home": "ECOM",
    "kitchen": "ECOM",
    "pet": "ECOM",
    # Alpha categories -> op categories
    "APP_FACTORY": "APP",
    "CONTENT_FARM": "CONTENT",
    "CONTENT_FORMAT": "CONTENT",
    "OUTBOUND": "OUTBOUND",
    "TOOL_ALPHA": "GROWTH",
    "MONETIZATION": "ECOM",
    "GROWTH_HACK": "GROWTH",
    "ENGAGEMENT_BAIT": "CONTENT",
    "SEO_GEO_ASO": "AFFILIATE",
    # Trend signal types -> op categories
    "rising_query": "CONTENT",
    "quality_product": "ECOM",
    "educational": "CONTENT",
    "service_opportunity": "SERVICE",
}


# ============================================================================
# TIME DECAY FUNCTION
# ============================================================================

def time_decay(hours_old: float, lambda_param: float = 0.03) -> float:
    """
    Exponential time decay for signal freshness.
    Fresh (<6h): ~1.0x, Recent (<24h): ~0.5x, Aging (<72h): ~0.11x
    Old (<7d): ~0.005x, Stale (>7d): ~0.0
    """
    return math.exp(-lambda_param * hours_old)


def hours_since(timestamp_str: str) -> float:
    """Parse timestamp and return hours since then."""
    if not timestamp_str:
        return 999
    for fmt in [
        "%Y-%m-%dT%H:%M:%S.%f",
        "%Y-%m-%dT%H:%M:%S",
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%d",
    ]:
        try:
            dt = datetime.strptime(timestamp_str.strip(), fmt)
            delta = datetime.now() - dt
            return max(0, delta.total_seconds() / 3600)
        except ValueError:
            continue
    return 999


# ============================================================================
# SIGNAL INGESTION
# ============================================================================

def read_csv_safe(path: Path, max_rows: int = 1000) -> list:
    """Read CSV safely with encoding fallback."""
    if not path.exists():
        return []
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            reader = csv.DictReader(f)
            return [row for i, row in enumerate(reader) if i < max_rows]
    except Exception:
        return []


def ingest_freelance_demand() -> list:
    """Ingest freelance demand signals."""
    rows = read_csv_safe(SOURCE_CONFIG["freelance_demand"]["path"])
    signals = []
    for row in rows:
        score = float(row.get("score", 0) or 0)
        budget = float(row.get("budget", 0) or 0)
        age_h = float(row.get("age_hours", 999) or 999)
        title = row.get("title", "")
        matched = row.get("matched_services", "")
        url = row.get("url", "")

        # Map matched services to categories
        categories = set()
        for svc in matched.split(","):
            svc = svc.strip().lower()
            cat = SIGNAL_TO_CATEGORY.get(svc, "SERVICE")
            categories.add(cat)

        signals.append({
            "source": "freelance_demand",
            "title": title[:120],
            "raw_score": score,
            "budget": budget,
            "age_hours": age_h,
            "url": url,
            "categories": list(categories) or ["SERVICE"],
            "matched_services": matched,
            "signal_type": "demand",
        })
    return signals


def ingest_ecom_arb() -> list:
    """Ingest ecom arbitrage signals."""
    rows = read_csv_safe(SOURCE_CONFIG["ecom_arb"]["path"])
    signals = []
    for row in rows:
        action = row.get("action", "").upper()
        if action == "SKIP":
            continue  # only include LIST and WATCH
        product = row.get("product", "")
        margin_pct = float(row.get("margin_pct", 0) or 0)
        composite = float(row.get("composite_score", 0) or 0)
        trend = float(row.get("trend_score", 0) or 0)
        net_profit = float(row.get("net_profit", 0) or 0)
        ts = row.get("timestamp", "")
        age_h = hours_since(ts)

        category_key = row.get("category", "general").lower()
        cat = SIGNAL_TO_CATEGORY.get(category_key, "ECOM")

        signals.append({
            "source": "ecom_arb",
            "title": f"Arb: {product} ({margin_pct:.0f}% margin, ${net_profit:.2f} profit)",
            "raw_score": composite,
            "budget": net_profit,
            "age_hours": age_h,
            "url": "",
            "categories": [cat],
            "matched_services": product,
            "signal_type": "opportunity",
            "extra": {"margin_pct": margin_pct, "trend_score": trend, "action": action},
        })
    return signals


def ingest_trend_signals() -> list:
    """Ingest trend detection signals."""
    rows = read_csv_safe(SOURCE_CONFIG["trend_signals"]["path"])
    signals = []
    for row in rows:
        score = float(row.get("score", 0) or 0)
        signal_text = row.get("signal", "")
        strength = float(row.get("strength", 0) or 0)
        signal_type = row.get("signal_type", "")
        product_matches = row.get("product_matches", "")
        url = row.get("url", "")
        age_h = float(row.get("age_hours", 999) or 999)

        categories = set()
        for pm in product_matches.split(","):
            pm = pm.strip().lower()
            cat = SIGNAL_TO_CATEGORY.get(pm, "CONTENT")
            categories.add(cat)
        st_cat = SIGNAL_TO_CATEGORY.get(signal_type.lower(), None)
        if st_cat:
            categories.add(st_cat)

        signals.append({
            "source": "trend_signals",
            "title": signal_text[:120],
            "raw_score": score,
            "budget": 0,
            "age_hours": age_h,
            "url": url,
            "categories": list(categories) or ["CONTENT"],
            "matched_services": product_matches,
            "signal_type": "trend",
            "extra": {"strength": strength, "original_type": signal_type},
        })
    return signals


def ingest_alpha_staging() -> list:
    """Ingest alpha intelligence signals."""
    rows = read_csv_safe(SOURCE_CONFIG["alpha_staging"]["path"])
    signals = []
    for row in rows:
        status = row.get("status", "").upper()
        if status not in ("APPROVED", "PENDING_REVIEW", ""):
            continue

        alpha_id = row.get("alpha_id", "")
        category = row.get("category", "")
        tactic = row.get("tactic", "")
        roi = row.get("roi_potential", "MEDIUM")
        source = row.get("source", "")
        url = row.get("source_url", "")
        created = row.get("created_at", "")
        age_h = hours_since(created) if created else 999

        # ROI to score
        roi_scores = {"HIGHEST": 95, "HIGH": 80, "MEDIUM": 60, "LOW": 40}
        raw_score = roi_scores.get(roi.upper(), 50)

        # Map alpha category to our categories
        cat = SIGNAL_TO_CATEGORY.get(category, "GROWTH")

        title = tactic[:120] if tactic else f"Alpha: {alpha_id} from {source}"

        signals.append({
            "source": "alpha_staging",
            "title": title,
            "raw_score": raw_score,
            "budget": 0,
            "age_hours": age_h,
            "url": url,
            "categories": [cat],
            "matched_services": category,
            "signal_type": "alpha",
            "extra": {"alpha_id": alpha_id, "roi": roi, "alpha_status": status},
        })
    return signals


def ingest_overnight_logs() -> list:
    """Ingest signals from overnight automation logs."""
    log_dir = AUTOMATIONS / "logs"
    signals = []
    if not log_dir.exists():
        return signals

    # Find recent overnight status files
    status_files = sorted(log_dir.glob("overnight_status_*.json"), reverse=True)[:3]
    for sf in status_files:
        try:
            data = json.loads(sf.read_text())
            age_h = hours_since(data.get("timestamp", ""))

            # Extract actionable findings
            for finding in data.get("findings", []):
                signals.append({
                    "source": "overnight_logs",
                    "title": finding.get("title", "Overnight finding")[:120],
                    "raw_score": float(finding.get("score", 50)),
                    "budget": 0,
                    "age_hours": age_h,
                    "url": "",
                    "categories": [finding.get("category", "GROWTH")],
                    "matched_services": "",
                    "signal_type": "system",
                })
        except Exception:
            continue

    return signals


# ============================================================================
# SIGNAL PROCESSING PIPELINE
# ============================================================================

def normalize_score(raw: float, source: str) -> float:
    """Normalize raw scores to 0-100 scale per source."""
    ranges = {
        "freelance_demand": (0, 100),
        "ecom_arb": (-200, 100),
        "trend_signals": (0, 100),
        "alpha_staging": (0, 100),
        "overnight_logs": (0, 100),
    }
    lo, hi = ranges.get(source, (0, 100))
    if hi == lo:
        return 50.0
    normalized = (raw - lo) / (hi - lo) * 100
    return max(0, min(100, normalized))


def apply_weights(signals: list) -> list:
    """Apply source reliability weights and time decay."""
    for sig in signals:
        source = sig["source"]
        reliability = SOURCE_CONFIG.get(source, {}).get("reliability", 0.5)

        # Normalize score
        norm_score = normalize_score(sig["raw_score"], source)

        # Apply time decay
        decay = time_decay(sig["age_hours"])

        # Budget bonus (signals with real money are more valuable)
        budget_bonus = 0
        if sig["budget"] > 0:
            budget_bonus = min(15, math.log2(sig["budget"] + 1) * 2)

        # Weighted score
        sig["normalized_score"] = norm_score
        sig["decay_factor"] = decay
        sig["reliability"] = reliability
        sig["budget_bonus"] = budget_bonus
        sig["weighted_score"] = (norm_score * reliability * decay) + budget_bonus

    return signals


def fuse_signals(signals: list) -> list:
    """
    Fuse signals that point to the same opportunity.
    Multi-source corroboration multiplies confidence:
    - 1 source: base confidence
    - 2 sources: 2.5x boost
    - 3+ sources: 4x boost
    """
    # Group by similarity (category + keyword overlap)
    groups = defaultdict(list)
    for sig in signals:
        # Create grouping key from categories and key words
        cats = tuple(sorted(sig["categories"]))
        # Extract key terms from title for matching
        title_words = set(sig["title"].lower().split())
        # Simple grouping by first category
        primary_cat = cats[0] if cats else "UNKNOWN"
        groups[primary_cat].append(sig)

    fused = []
    for cat, cat_signals in groups.items():
        # Sort by weighted score within category
        cat_signals.sort(key=lambda s: s["weighted_score"], reverse=True)

        # Find unique sources
        sources = set(s["source"] for s in cat_signals)
        num_sources = len(sources)

        # Confidence boost based on source count
        if num_sources >= 3:
            confidence_boost = 4.0
        elif num_sources >= 2:
            confidence_boost = 2.5
        else:
            confidence_boost = 1.0

        # Take top signals from this category, apply boost
        seen_titles = set()
        for sig in cat_signals:
            # Simple dedup by title similarity
            title_key = sig["title"][:40].lower()
            if title_key in seen_titles:
                continue
            seen_titles.add(title_key)

            sig["source_count"] = num_sources
            sig["confidence_boost"] = confidence_boost
            sig["fused_score"] = min(100, sig["weighted_score"] * confidence_boost)
            sig["primary_category"] = cat
            fused.append(sig)

    # Final sort by fused score
    fused.sort(key=lambda s: s["fused_score"], reverse=True)
    return fused


def categorize_action(sig: dict) -> str:
    """Determine recommended action based on fused score."""
    score = sig["fused_score"]
    if score >= 85:
        return "IMMEDIATE_ACTION"
    elif score >= 70:
        return "HIGH_PRIORITY"
    elif score >= 50:
        return "MONITOR"
    elif score >= 30:
        return "BACKLOG"
    else:
        return "IGNORE"


# ============================================================================
# OUTPUT
# ============================================================================

def save_fused_csv(fused: list):
    """Save fused signals to CSV."""
    FUSED_OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    fields = [
        "rank", "fused_score", "action", "primary_category", "source",
        "source_count", "confidence_boost", "title", "url",
        "weighted_score", "normalized_score", "decay_factor",
        "reliability", "budget", "age_hours", "matched_services",
        "signal_type", "timestamp"
    ]

    tmp = FUSED_OUTPUT.with_suffix(".csv.tmp")
    try:
        with open(tmp, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
            writer.writeheader()
            for i, sig in enumerate(fused):
                sig["rank"] = i + 1
                sig["action"] = categorize_action(sig)
                sig["timestamp"] = datetime.now().isoformat()
                sig["fused_score"] = round(sig["fused_score"], 1)
                sig["weighted_score"] = round(sig.get("weighted_score", 0), 1)
                sig["normalized_score"] = round(sig.get("normalized_score", 0), 1)
                sig["decay_factor"] = round(sig.get("decay_factor", 0), 3)
                sig["reliability"] = round(sig.get("reliability", 0), 2)
                sig["budget"] = round(sig.get("budget", 0), 2)
                sig["age_hours"] = round(sig.get("age_hours", 0), 1)
                writer.writerow(sig)
        tmp.rename(FUSED_OUTPUT)
    except OSError as e:
        print(f"[SIGNAL_AGG] WARNING: Failed to write fused signals: {e}")
        try:
            tmp.unlink(missing_ok=True)
        except Exception:
            pass


def append_history(fused: list):
    """Append to signal history (append-only JSONL)."""
    HISTORY_OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().isoformat()
    entry = {
        "timestamp": timestamp,
        "total_signals": len(fused),
        "immediate_action": sum(1 for s in fused if categorize_action(s) == "IMMEDIATE_ACTION"),
        "high_priority": sum(1 for s in fused if categorize_action(s) == "HIGH_PRIORITY"),
        "top_5": [
            {"title": s["title"][:80], "score": round(s["fused_score"], 1), "source": s["source"]}
            for s in fused[:5]
        ],
        "by_category": {},
    }
    cat_counts = defaultdict(int)
    for s in fused:
        cat_counts[s["primary_category"]] += 1
    entry["by_category"] = dict(cat_counts)

    try:
        with open(HISTORY_OUTPUT, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry) + "\n")
    except OSError as e:
        print(f"[SIGNAL_AGG] WARNING: Failed to append history: {e}")


def print_table(fused: list, limit: int = 20):
    """Print formatted table of fused signals."""
    print(f"{'#':>3}  {'SCORE':>6}  {'ACTION':>18}  {'CAT':>8}  {'SRC':>16}  {'SRCS':>4}  {'AGE':>6}  {'TITLE':<60}")
    print("-" * 130)
    for i, sig in enumerate(fused[:limit]):
        action = categorize_action(sig)
        age_str = f"{sig['age_hours']:.0f}h" if sig["age_hours"] < 999 else "old"
        print(
            f"{i+1:>3}  "
            f"{sig['fused_score']:>6.1f}  "
            f"{action:>18}  "
            f"{sig['primary_category']:>8}  "
            f"{sig['source']:>16}  "
            f"{sig['source_count']:>4}  "
            f"{age_str:>6}  "
            f"{sig['title'][:60]:<60}"
        )


# ============================================================================
# MAIN COMMANDS
# ============================================================================

def cmd_scan():
    """Full signal aggregation pipeline."""
    print("=" * 80)
    print("PRINTMAXX SIGNAL AGGREGATOR")
    print(f"Timestamp: {datetime.now().isoformat()}")
    print("=" * 80)
    print()

    # 1. INGEST
    print("Phase 1: INGEST signals from all sources...")
    all_signals = []

    freelance = ingest_freelance_demand()
    print(f"  Freelance demand: {len(freelance)} signals")
    all_signals.extend(freelance)

    ecom = ingest_ecom_arb()
    print(f"  Ecom arbitrage:   {len(ecom)} signals")
    all_signals.extend(ecom)

    trends = ingest_trend_signals()
    print(f"  Trend signals:    {len(trends)} signals")
    all_signals.extend(trends)

    alpha = ingest_alpha_staging()
    print(f"  Alpha staging:    {len(alpha)} signals")
    all_signals.extend(alpha)

    overnight = ingest_overnight_logs()
    print(f"  Overnight logs:   {len(overnight)} signals")
    all_signals.extend(overnight)

    print(f"  TOTAL ingested:   {len(all_signals)} signals")
    print()

    # 2. WEIGHT
    print("Phase 2: WEIGHT signals (reliability + time decay + budget bonus)...")
    all_signals = apply_weights(all_signals)
    avg_decay = sum(s["decay_factor"] for s in all_signals) / max(1, len(all_signals))
    print(f"  Average decay factor: {avg_decay:.3f}")
    print()

    # 3. FUSE
    print("Phase 3: FUSE multi-source signals (confidence multiplier)...")
    fused = fuse_signals(all_signals)
    print(f"  Fused signals:    {len(fused)}")
    print()

    # 4. RANK + ALERT
    immediate = [s for s in fused if categorize_action(s) == "IMMEDIATE_ACTION"]
    high_pri = [s for s in fused if categorize_action(s) == "HIGH_PRIORITY"]
    monitor = [s for s in fused if categorize_action(s) == "MONITOR"]

    print("Phase 4: RANK and categorize...")
    print(f"  IMMEDIATE_ACTION (>=85): {len(immediate)}")
    print(f"  HIGH_PRIORITY    (>=70): {len(high_pri)}")
    print(f"  MONITOR          (>=50): {len(monitor)}")
    print(f"  BACKLOG/IGNORE   (<50):  {len(fused) - len(immediate) - len(high_pri) - len(monitor)}")
    print()

    # 5. OUTPUT
    save_fused_csv(fused)
    append_history(fused)
    print(f"Saved: {FUSED_OUTPUT}")
    print(f"Appended: {HISTORY_OUTPUT}")
    print()

    # Category breakdown
    print("--- Category Breakdown ---")
    cat_counts = defaultdict(lambda: {"count": 0, "avg_score": 0, "top_score": 0})
    for s in fused:
        cat = s["primary_category"]
        cat_counts[cat]["count"] += 1
        cat_counts[cat]["avg_score"] += s["fused_score"]
        cat_counts[cat]["top_score"] = max(cat_counts[cat]["top_score"], s["fused_score"])
    for cat in sorted(cat_counts, key=lambda c: cat_counts[c]["top_score"], reverse=True):
        d = cat_counts[cat]
        avg = d["avg_score"] / d["count"]
        print(f"  {cat:>10}: {d['count']:>4} signals  |  avg {avg:>5.1f}  |  top {d['top_score']:>5.1f}")
    print()

    # Source breakdown
    print("--- Source Breakdown ---")
    src_counts = defaultdict(int)
    for s in fused:
        src_counts[s["source"]] += 1
    for src, count in sorted(src_counts.items(), key=lambda x: x[1], reverse=True):
        rel = SOURCE_CONFIG.get(src, {}).get("reliability", 0.5)
        print(f"  {src:>20}: {count:>4} signals  (reliability: {rel:.2f})")
    print()

    # Top signals
    if fused:
        print("--- Top 20 Fused Signals ---")
        print_table(fused, 20)

    # Alerts
    if immediate:
        print()
        print("=" * 80)
        print(f"!!! {len(immediate)} IMMEDIATE ACTION ALERTS (score >= 85) !!!")
        print("=" * 80)
        for i, s in enumerate(immediate):
            print(f"  {i+1}. [{s['fused_score']:.1f}] {s['title'][:70]}")
            if s.get("url"):
                print(f"     URL: {s['url']}")
            print(f"     Source: {s['source']} | Category: {s['primary_category']} | {s['source_count']} sources corroborate")

    return fused


def cmd_top(n: int):
    """Show top N opportunities."""
    # Quick scan
    all_signals = []
    all_signals.extend(ingest_freelance_demand())
    all_signals.extend(ingest_ecom_arb())
    all_signals.extend(ingest_trend_signals())
    all_signals.extend(ingest_alpha_staging())
    all_signals.extend(ingest_overnight_logs())
    all_signals = apply_weights(all_signals)
    fused = fuse_signals(all_signals)

    print(f"=== Top {n} Opportunities ===")
    print()
    print_table(fused, n)
    print()
    for i, s in enumerate(fused[:n]):
        action = categorize_action(s)
        print(f"{i+1}. [{s['fused_score']:.1f}] {s['title']}")
        print(f"   Source: {s['source']} | Category: {s['primary_category']} | Action: {action}")
        if s.get("url"):
            print(f"   URL: {s['url']}")
        if s.get("matched_services"):
            print(f"   Services: {s['matched_services']}")
        print()


def cmd_alerts():
    """Show only high-confidence alerts (>=85)."""
    all_signals = []
    all_signals.extend(ingest_freelance_demand())
    all_signals.extend(ingest_ecom_arb())
    all_signals.extend(ingest_trend_signals())
    all_signals.extend(ingest_alpha_staging())
    all_signals = apply_weights(all_signals)
    fused = fuse_signals(all_signals)

    immediate = [s for s in fused if categorize_action(s) == "IMMEDIATE_ACTION"]

    if not immediate:
        print("No IMMEDIATE_ACTION alerts right now.")
        print(f"Highest signal: {fused[0]['fused_score']:.1f} - {fused[0]['title'][:60]}" if fused else "No signals.")
        return

    print(f"=== {len(immediate)} IMMEDIATE ACTION ALERTS ===")
    print()
    for i, s in enumerate(immediate):
        print(f"{i+1}. SCORE: {s['fused_score']:.1f}")
        print(f"   {s['title']}")
        print(f"   Source: {s['source']} | Category: {s['primary_category']}")
        print(f"   Sources corroborating: {s['source_count']}")
        print(f"   Confidence boost: {s['confidence_boost']:.1f}x")
        if s.get("url"):
            print(f"   URL: {s['url']}")
        print()


def cmd_history():
    """Show signal trend over time."""
    if not HISTORY_OUTPUT.exists():
        print("No history yet. Run --scan first.")
        return

    print("=== Signal History ===")
    print()

    entries = []
    with open(HISTORY_OUTPUT, "r") as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    entries.append(json.loads(line))
                except json.JSONDecodeError:
                    continue

    if not entries:
        print("No history entries found.")
        return

    print(f"{'TIMESTAMP':<22}  {'TOTAL':>6}  {'IMMED':>6}  {'HIGH':>6}  {'TOP SIGNAL':<50}")
    print("-" * 100)

    for e in entries[-20:]:  # last 20 entries
        ts = e.get("timestamp", "?")[:19]
        total = e.get("total_signals", 0)
        imm = e.get("immediate_action", 0)
        high = e.get("high_priority", 0)
        top_sig = ""
        if e.get("top_5"):
            top_sig = f"[{e['top_5'][0]['score']}] {e['top_5'][0]['title'][:40]}"
        print(f"{ts:<22}  {total:>6}  {imm:>6}  {high:>6}  {top_sig:<50}")

    print()
    print("Category distribution (latest):")
    if entries:
        latest = entries[-1]
        for cat, count in sorted(latest.get("by_category", {}).items(), key=lambda x: x[1], reverse=True):
            print(f"  {cat:>10}: {count}")


def cmd_filter_source(source: str):
    """Filter signals by source."""
    all_signals = []
    all_signals.extend(ingest_freelance_demand())
    all_signals.extend(ingest_ecom_arb())
    all_signals.extend(ingest_trend_signals())
    all_signals.extend(ingest_alpha_staging())
    all_signals = apply_weights(all_signals)
    fused = fuse_signals(all_signals)

    # Match source name loosely
    source_lower = source.lower()
    filtered = [s for s in fused if source_lower in s["source"].lower()]

    if not filtered:
        print(f"No signals from source matching '{source}'.")
        print(f"Available sources: {', '.join(set(s['source'] for s in fused))}")
        return

    print(f"=== Signals from '{source}' ({len(filtered)} found) ===")
    print()
    print_table(filtered, 30)


def cmd_filter_category(category: str):
    """Filter signals by op category."""
    all_signals = []
    all_signals.extend(ingest_freelance_demand())
    all_signals.extend(ingest_ecom_arb())
    all_signals.extend(ingest_trend_signals())
    all_signals.extend(ingest_alpha_staging())
    all_signals = apply_weights(all_signals)
    fused = fuse_signals(all_signals)

    cat_upper = category.upper()
    filtered = [s for s in fused if s["primary_category"] == cat_upper]

    if not filtered:
        print(f"No signals for category '{cat_upper}'.")
        cats = set(s["primary_category"] for s in fused)
        print(f"Available categories: {', '.join(sorted(cats))}")
        return

    print(f"=== Signals for category '{cat_upper}' ({len(filtered)} found) ===")
    print()
    print_table(filtered, 30)


# ============================================================================
# CLI
# ============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="PRINTMAXX Signal Aggregator - Fuse intelligence from all scanners"
    )
    parser.add_argument("--scan", action="store_true", help="Full signal aggregation pipeline")
    parser.add_argument("--top", type=int, metavar="N", help="Show top N opportunities")
    parser.add_argument("--alerts", action="store_true", help="Show high-confidence alerts only")
    parser.add_argument("--history", action="store_true", help="Show signal trend over time")
    parser.add_argument("--source", metavar="NAME", help="Filter by source (freelance, ecom, trend, alpha)")
    parser.add_argument("--category", metavar="CAT", help="Filter by category (CONTENT, SERVICE, APP, ECOM, etc)")

    args = parser.parse_args()

    if args.scan:
        cmd_scan()
    elif args.top:
        cmd_top(args.top)
    elif args.alerts:
        cmd_alerts()
    elif args.history:
        cmd_history()
    elif args.source:
        cmd_filter_source(args.source)
    elif args.category:
        cmd_filter_category(args.category)
    else:
        parser.print_help()
        print("\nQuick Start:")
        print("  python3 AUTOMATIONS/signal_aggregator.py --scan      # Full pipeline")
        print("  python3 AUTOMATIONS/signal_aggregator.py --top 5     # Top 5 opportunities")
        print("  python3 AUTOMATIONS/signal_aggregator.py --alerts    # High-confidence only")


if __name__ == "__main__":
    main()
