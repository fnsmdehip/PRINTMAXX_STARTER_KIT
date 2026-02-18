#!/usr/bin/env python3
"""Ecom arbitrage execution pack (no posting).

This produces a single, always-up-to-date "what to list next" pack from existing ledgers
and generated listing drafts.

Inputs:
  - LEDGER/ECOM_ARB_OPPORTUNITIES.csv
  - PRODUCTS/ARB_LISTINGS/ (latest listing draft)

Outputs (overwritten each run):
  - output/ecom/latest.md
  - output/ecom/latest.html
  - output/ecom/manifest.json
"""

from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional


BASE = Path(__file__).resolve().parent.parent
LEDGER = BASE / "LEDGER"
PRODUCTS = BASE / "PRODUCTS"
OUT = BASE / "output" / "ecom"

ARB_LEDGER = LEDGER / "ECOM_ARB_OPPORTUNITIES.csv"
ARB_LISTINGS_DIR = PRODUCTS / "ARB_LISTINGS"
AUTOPILOT_MANIFEST = BASE / "output" / "ecom_autopilot" / "manifest.json"
AUTOPILOT_LATEST = BASE / "output" / "ecom_autopilot" / "latest.md"
LATEST_MD = OUT / "latest.md"
LATEST_HTML = OUT / "latest.html"
MANIFEST = OUT / "manifest.json"


def now_iso() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def safe_float(v: object, default: float = 0.0) -> float:
    try:
        return float(str(v).strip())
    except Exception:
        return default


def safe_int(v: object, default: int = 0) -> int:
    try:
        return int(float(str(v).strip()))
    except Exception:
        return default


def latest_file(dir_path: Path, glob_pat: str) -> Optional[Path]:
    try:
        files = sorted(dir_path.glob(glob_pat))
    except Exception:
        return None
    if not files:
        return None
    # Prefer mtime over lexicographic name for safety.
    return max(files, key=lambda p: p.stat().st_mtime)


def load_arb_rows(limit: int = 5000) -> List[Dict[str, str]]:
    if not ARB_LEDGER.exists():
        return []
    rows: List[Dict[str, str]] = []
    try:
        with open(ARB_LEDGER, "r", encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f)
            for i, row in enumerate(reader):
                if i >= limit:
                    break
                if isinstance(row, dict):
                    rows.append({k: (v or "").strip() for k, v in row.items()})
    except Exception:
        return []
    return rows


def top_arb_opportunities(max_items: int = 15) -> List[Dict[str, Any]]:
    rows = load_arb_rows()
    if not rows:
        return []

    best_by_product: Dict[str, Dict[str, Any]] = {}
    for r in rows:
        product = (r.get("product") or "").strip().lower()
        if not product:
            continue

        item = {
            "timestamp": (r.get("timestamp") or "").strip(),
            "product": product,
            "category": (r.get("category") or "").strip(),
            "sell_price": safe_float(r.get("sell_price"), 0.0),
            "source_price": safe_float(r.get("source_price"), 0.0),
            "best_platform": (r.get("best_platform") or "").strip(),
            "net_profit": safe_float(r.get("net_profit"), 0.0),
            "margin_pct": safe_float(r.get("margin_pct"), 0.0),
            "trend_score": safe_int(r.get("trend_score"), 0),
            "composite_score": safe_float(r.get("composite_score"), 0.0),
            "action": (r.get("action") or "").strip().upper(),
            "price_source": (r.get("price_source") or "").strip(),
            "weight_tier": (r.get("weight_tier") or "").strip(),
        }

        # Keep the highest composite score per product.
        prev = best_by_product.get(product)
        if prev is None or float(item["composite_score"]) > float(prev.get("composite_score") or 0.0):
            best_by_product[product] = item

    items = list(best_by_product.values())

    # Prefer actionable items first.
    def rank_key(it: Dict[str, Any]):
        action = (it.get("action") or "").upper()
        action_rank = 0 if action == "LIST" else (1 if action == "WATCH" else 2)
        return (
            action_rank,
            -float(it.get("composite_score") or 0.0),
            -float(it.get("margin_pct") or 0.0),
            -float(it.get("net_profit") or 0.0),
        )

    items.sort(key=rank_key)
    return items[:max_items]


def load_autopilot_summary() -> Dict[str, Any]:
    if not AUTOPILOT_MANIFEST.exists():
        return {"available": False}
    try:
        payload = json.loads(AUTOPILOT_MANIFEST.read_text(encoding="utf-8"))
    except Exception:
        return {"available": False}
    if not isinstance(payload, dict):
        return {"available": False}

    queue_stats = payload.get("queue_stats")
    if not isinstance(queue_stats, dict):
        queue_stats = {}
    return {
        "available": True,
        "manifest": str(AUTOPILOT_MANIFEST),
        "latest_md": str(AUTOPILOT_LATEST) if AUTOPILOT_LATEST.exists() else "",
        "winners_count": safe_int(payload.get("winners_count"), 0),
        "queue_stats": queue_stats,
    }


def render_markdown(top_items: List[Dict[str, Any]], arb_listings_latest: Optional[Path], autopilot: Dict[str, Any]) -> str:
    lines: List[str] = []
    lines.append("# PRINTMAXX Ecom Pack (No Posting)")
    lines.append("")
    lines.append(f"Generated: {now_iso()}")
    lines.append("")

    lines.append("## Top Arbitrage Opportunities (from LEDGER/ECOM_ARB_OPPORTUNITIES.csv)")
    lines.append("")
    if not top_items:
        lines.append("- None (arb ledger missing or empty).")
    else:
        for it in top_items:
            lines.append(
                f"- {it['product']} | sell=${it['sell_price']:.2f} src=${it['source_price']:.2f} "
                f"profit=${it['net_profit']:.2f} margin={it['margin_pct']:.1f}% "
                f"platform={it.get('best_platform') or 'n/a'} score={it.get('composite_score')}"
            )
            meta = []
            if it.get("category"):
                meta.append(f"cat={it['category']}")
            if it.get("weight_tier"):
                meta.append(f"weight={it['weight_tier']}")
            if it.get("price_source"):
                meta.append(f"price_source={it['price_source']}")
            if meta:
                lines.append(f"  - " + " | ".join(meta))

    lines.append("")
    lines.append("## Latest Arb Listing Drafts (copy/paste ready)")
    lines.append("")
    if arb_listings_latest and arb_listings_latest.exists():
        lines.append(f"- {arb_listings_latest}")
    else:
        lines.append("- None (run `python3 AUTOMATIONS/arb_listing_generator.py --generate`).")

    lines.append("")
    lines.append("## Ecom Autopilot")
    lines.append("")
    if not autopilot.get("available"):
        lines.append("- Not available yet (run `python3 AUTOMATIONS/ecom_autopilot.py --tick`).")
    else:
        lines.append(f"- Winners selected: {autopilot.get('winners_count', 0)}")
        if autopilot.get("latest_md"):
            lines.append(f"- Latest report: {autopilot.get('latest_md')}")
        qstats = autopilot.get("queue_stats") if isinstance(autopilot.get("queue_stats"), dict) else {}
        for plat, stat in qstats.items():
            if not isinstance(stat, dict):
                continue
            total = safe_int(stat.get("total"), 0)
            auto_ready = safe_int(stat.get("auto_ready"), 0)
            blocked = safe_int(stat.get("blocked"), 0)
            lines.append(f"  - {plat}: total={total} auto_ready={auto_ready} blocked={blocked}")

    return "\n".join(lines).rstrip() + "\n"


def write_html(md_text: str) -> None:
    # Keep it dead-simple and offline friendly.
    escaped = (
        md_text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )
    html = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>PRINTMAXX Ecom Pack</title>
  <style>
    body {{ margin: 0; background: #0b0b0b; color: #eaeaea; font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace; }}
    .wrap {{ max-width: 1100px; margin: 0 auto; padding: 18px; }}
    pre {{ white-space: pre-wrap; line-height: 1.5; font-size: 13px; }}
    a {{ color: #00aaff; }}
  </style>
</head>
<body>
  <div class="wrap">
    <pre>{escaped}</pre>
  </div>
</body>
</html>
"""
    LATEST_HTML.write_text(html, encoding="utf-8")


def write_manifest(top_items: List[Dict[str, Any]], arb_listings_latest: Optional[Path], autopilot: Dict[str, Any]) -> None:
    payload = {
        "generated_at": now_iso(),
        "arb_ledger": str(ARB_LEDGER),
        "top_arb": top_items,
        "arb_listings_latest": str(arb_listings_latest) if arb_listings_latest else "",
        "autopilot_manifest": str(AUTOPILOT_MANIFEST) if AUTOPILOT_MANIFEST.exists() else "",
        "autopilot_available": bool(autopilot.get("available")),
        "autopilot_winners_count": safe_int(autopilot.get("winners_count"), 0),
        "autopilot_queue_stats": autopilot.get("queue_stats") if isinstance(autopilot.get("queue_stats"), dict) else {},
    }
    MANIFEST.write_text(json.dumps(payload, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true", help="Write output/ecom/latest.{md,html} + manifest")
    ap.add_argument("--max-items", type=int, default=15)
    args = ap.parse_args()

    if not args.write:
        ap.print_help()
        return 2

    OUT.mkdir(parents=True, exist_ok=True)

    top_items = top_arb_opportunities(max_items=max(1, int(args.max_items)))
    arb_latest = latest_file(ARB_LISTINGS_DIR, "ARB_LISTINGS_*.md")
    autopilot = load_autopilot_summary()
    md = render_markdown(top_items, arb_latest, autopilot)

    LATEST_MD.write_text(md, encoding="utf-8")
    write_html(md)
    write_manifest(top_items, arb_latest, autopilot)
    print(f"ecom_packager: wrote {LATEST_MD}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
