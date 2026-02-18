#!/usr/bin/env python3
"""PRINTMAXX Ecom Autopilot.

Purpose:
  - Convert arbitrage scan output into a persistent winner list.
  - Build platform queue CSVs for multi-platform listing execution.
  - Mark what is auto-executable now vs what is blocked by account auth.

This script is non-interactive and safe for Ship Captain cron runs.
It does not submit listings directly; it prepares and prioritizes execution.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Iterable, List, Tuple


BASE = Path(__file__).resolve().parent.parent
LEDGER = BASE / "LEDGER"
OUTPUT = BASE / "output" / "ecom_autopilot"
QUEUE_DIR = OUTPUT / "queues"

ARB_LEDGER = LEDGER / "ECOM_ARB_OPPORTUNITIES.csv"
ACCOUNTS_CSV = LEDGER / "ACCOUNTS.csv"
WINNERS_CSV = LEDGER / "ECOM_WINNERS.csv"

LATEST_MD = OUTPUT / "latest.md"
LATEST_HTML = OUTPUT / "latest.html"
MANIFEST = OUTPUT / "manifest.json"

PLATFORMS = [
    "ebay",
    "etsy",
    "redbubble",
    "facebook_marketplace",
    "amazon",
]

# Platforms where this repo has browser automation support today.
AUTOMATABLE_PLATFORMS = {"ebay", "etsy", "redbubble"}

PLATFORM_ALIASES = {
    "ebay": {"ebay", "e-bay"},
    "etsy": {"etsy"},
    "redbubble": {"redbubble"},
    "facebook_marketplace": {"facebook", "fb", "fb marketplace", "facebook marketplace"},
    "amazon": {"amazon", "amazon seller", "amazon seller central", "amazon kdp"},
}


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


def slugify(text: str, max_len: int = 64) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", (text or "").lower()).strip("-")
    if not s:
        return "item"
    return s[:max_len].strip("-")


def read_csv_rows(path: Path, max_rows: int = 200000) -> List[Dict[str, str]]:
    if not path.exists():
        return []
    out: List[Dict[str, str]] = []
    try:
        with open(path, "r", encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f)
            for i, row in enumerate(reader):
                if i >= max_rows:
                    break
                out.append({k: (v or "").strip() for k, v in row.items()})
    except Exception:
        return []
    return out


def write_csv_rows(path: Path, fieldnames: Iterable[str], rows: List[Dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(fieldnames))
        writer.writeheader()
        for row in rows:
            writer.writerow({k: row.get(k, "") for k in writer.fieldnames})


def normalize_platform_name(name: str) -> str:
    n = (name or "").strip().lower()
    for plat, aliases in PLATFORM_ALIASES.items():
        if n in aliases:
            return plat
    return n


def load_account_readiness() -> Dict[str, bool]:
    rows = read_csv_rows(ACCOUNTS_CSV, max_rows=5000)
    readiness = {p: False for p in PLATFORMS}
    active_status = {"ACTIVE", "CREATED", "READY", "WARMUP"}

    for row in rows:
        platform = normalize_platform_name(row.get("Platform") or row.get("platform") or "")
        status = (row.get("Status") or row.get("status") or "").strip().upper()
        if platform in readiness and status in active_status:
            readiness[platform] = True
    return readiness


def dedupe_best_opportunities(rows: List[Dict[str, str]]) -> List[Dict[str, Any]]:
    best: Dict[str, Dict[str, Any]] = {}
    for r in rows:
        product = (r.get("product") or "").strip().lower()
        if not product:
            continue

        item = {
            "timestamp": r.get("timestamp", ""),
            "product": product,
            "category": r.get("category", ""),
            "sell_price": safe_float(r.get("sell_price"), 0.0),
            "source_price": safe_float(r.get("source_price"), 0.0),
            "best_platform": (r.get("best_platform") or "").strip(),
            "net_profit": safe_float(r.get("net_profit"), 0.0),
            "margin_pct": safe_float(r.get("margin_pct"), 0.0),
            "trend_score": safe_int(r.get("trend_score"), 0),
            "composite_score": safe_float(r.get("composite_score"), 0.0),
            "action": (r.get("action") or "").strip().upper(),
            "price_source": r.get("price_source", ""),
            "weight_tier": r.get("weight_tier", ""),
        }

        prev = best.get(product)
        if prev is None or float(item["composite_score"]) > float(prev.get("composite_score") or 0.0):
            best[product] = item

    return list(best.values())


def score_winner(item: Dict[str, Any]) -> float:
    # Quant-style blended score for listing priority.
    return round(
        float(item.get("composite_score") or 0.0) * 1.0
        + float(item.get("net_profit") or 0.0) * 1.8
        + float(item.get("margin_pct") or 0.0) * 0.35
        + float(item.get("trend_score") or 0.0) * 0.15,
        2,
    )


def stage_for(item: Dict[str, Any], winner_score: float) -> str:
    margin = float(item.get("margin_pct") or 0.0)
    profit = float(item.get("net_profit") or 0.0)
    if winner_score >= 95 and margin >= 50 and profit >= 15:
        return "SCALE"
    if winner_score >= 75 and margin >= 35 and profit >= 8:
        return "TEST"
    return "PROBE"


def platforms_for(stage: str) -> List[str]:
    if stage == "SCALE":
        return ["ebay", "etsy", "redbubble", "facebook_marketplace", "amazon"]
    if stage == "TEST":
        return ["ebay", "etsy", "redbubble", "facebook_marketplace"]
    return ["ebay", "etsy", "redbubble"]


def title_for(product: str, category: str, platform: str) -> str:
    base = " ".join(w.capitalize() for w in product.split())
    if platform == "etsy":
        return f"{base} | Trending {category.title()} Find | 2026"
    if platform == "redbubble":
        return f"{base} Trend Design"
    if platform == "amazon":
        return f"{base} - Practical {category.title()} Pick"
    if platform == "facebook_marketplace":
        return f"{base} - New in Box"
    return f"{base} - Fast Shipping"


def description_for(item: Dict[str, Any], platform: str) -> str:
    product = str(item.get("product") or "").strip()
    category = str(item.get("category") or "").strip()
    margin = float(item.get("margin_pct") or 0.0)
    best_platform = str(item.get("best_platform") or "").strip() or "n/a"
    return (
        f"Trending {category} product: {product}. "
        f"Optimized from PRINTMAXX arb engine. Margin profile {margin:.1f}%. "
        f"Primary signal from {best_platform}. "
        f"Platform-targeted listing copy for {platform}."
    )


def tags_for(product: str, category: str) -> str:
    words = [w for w in re.findall(r"[a-z0-9]+", product.lower()) if len(w) >= 3]
    tags = []
    for w in words:
        if w not in tags:
            tags.append(w)
    if category:
        c = category.lower()
        if c not in tags:
            tags.append(c)
    for extra in ["trending", "2026", "best-seller"]:
        if extra not in tags:
            tags.append(extra)
    return ",".join(tags[:13])


def build_winners(
    opportunities: List[Dict[str, Any]],
    *,
    top: int,
    min_margin: float,
    min_profit: float,
    include_watch: bool = False,
) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    for item in opportunities:
        action = str(item.get("action") or "").upper()
        margin = float(item.get("margin_pct") or 0.0)
        profit = float(item.get("net_profit") or 0.0)
        if not include_watch and action != "LIST":
            continue
        if margin < min_margin or profit < min_profit:
            continue

        ws = score_winner(item)
        stage = stage_for(item, ws)
        pid = slugify(f"{item.get('product')}-{item.get('category')}")
        out.append(
            {
                **item,
                "winner_score": ws,
                "stage": stage,
                "product_id": pid,
                "distribution_vector": "|".join(platforms_for(stage)),
            }
        )

    out.sort(key=lambda x: float(x.get("winner_score") or 0.0), reverse=True)
    return out[: max(1, int(top))]


def build_platform_queues(winners: List[Dict[str, Any]], account_ready: Dict[str, bool]) -> Dict[str, List[Dict[str, Any]]]:
    queues: Dict[str, List[Dict[str, Any]]] = {p: [] for p in PLATFORMS}
    ts = now_iso()

    for w in winners:
        product = str(w.get("product") or "")
        category = str(w.get("category") or "")
        price = round(float(w.get("sell_price") or 0.0), 2)
        source_price = round(float(w.get("source_price") or 0.0), 2)
        profit = round(float(w.get("net_profit") or 0.0), 2)
        margin = round(float(w.get("margin_pct") or 0.0), 1)
        score = round(float(w.get("winner_score") or 0.0), 2)

        for platform in platforms_for(str(w.get("stage") or "PROBE")):
            is_ready = bool(account_ready.get(platform, False))
            auto_capable = platform in AUTOMATABLE_PLATFORMS
            if is_ready and auto_capable:
                queue_status = "AUTO_READY"
            elif is_ready:
                queue_status = "ACCOUNT_READY_NO_AUTOMATION"
            else:
                queue_status = "HUMAN_LOGIN_REQUIRED"

            row = {
                "generated_at": ts,
                "platform": platform,
                "queue_status": queue_status,
                "auto_capable": "YES" if auto_capable else "NO",
                "account_ready": "YES" if is_ready else "NO",
                "product_id": w.get("product_id", ""),
                "product": product,
                "category": category,
                "stage": w.get("stage", ""),
                "winner_score": f"{score:.2f}",
                "sell_price": f"{price:.2f}",
                "source_price": f"{source_price:.2f}",
                "net_profit": f"{profit:.2f}",
                "margin_pct": f"{margin:.1f}",
                "best_platform": w.get("best_platform", ""),
                "title": title_for(product, category, platform),
                "description": description_for(w, platform),
                "tags": tags_for(product, category),
                "organic_budget_usd": "0",
                "paid_test_budget_usd": "0" if str(w.get("stage")) == "PROBE" else ("5" if str(w.get("stage")) == "TEST" else "15"),
                "next_action": (
                    "run auto_list_products"
                    if queue_status == "AUTO_READY"
                    else ("manual list with queue row" if is_ready else "create/login account")
                ),
            }
            queues[platform].append(row)

    return queues


def write_winners_ledger(winners: List[Dict[str, Any]]) -> None:
    prev_rows = read_csv_rows(WINNERS_CSV, max_rows=5000)
    prev_by_id: Dict[str, Dict[str, str]] = {}
    for row in prev_rows:
        pid = (row.get("product_id") or "").strip()
        if pid:
            prev_by_id[pid] = row

    out_rows: List[Dict[str, Any]] = []
    ts = now_iso()
    for w in winners:
        pid = str(w.get("product_id") or "")
        prev = prev_by_id.get(pid, {})
        out_rows.append(
            {
                "timestamp": ts,
                "product_id": pid,
                "product": w.get("product", ""),
                "category": w.get("category", ""),
                "stage": w.get("stage", ""),
                "winner_score": f"{float(w.get('winner_score') or 0.0):.2f}",
                "sell_price": f"{float(w.get('sell_price') or 0.0):.2f}",
                "source_price": f"{float(w.get('source_price') or 0.0):.2f}",
                "net_profit": f"{float(w.get('net_profit') or 0.0):.2f}",
                "margin_pct": f"{float(w.get('margin_pct') or 0.0):.1f}",
                "trend_score": int(float(w.get("trend_score") or 0)),
                "best_platform": w.get("best_platform", ""),
                "distribution_vector": w.get("distribution_vector", ""),
                "organic_status": prev.get("organic_status", "NOT_STARTED"),
                "paid_status": prev.get("paid_status", "HOLD"),
                "notes": prev.get("notes", ""),
            }
        )

    fieldnames = [
        "timestamp",
        "product_id",
        "product",
        "category",
        "stage",
        "winner_score",
        "sell_price",
        "source_price",
        "net_profit",
        "margin_pct",
        "trend_score",
        "best_platform",
        "distribution_vector",
        "organic_status",
        "paid_status",
        "notes",
    ]
    write_csv_rows(WINNERS_CSV, fieldnames, out_rows)


def render_latest_md(
    winners: List[Dict[str, Any]],
    queues: Dict[str, List[Dict[str, Any]]],
    account_ready: Dict[str, bool],
) -> str:
    lines: List[str] = []
    lines.append("# PRINTMAXX Ecom Autopilot")
    lines.append("")
    lines.append(f"Generated: {now_iso()}")
    lines.append("")

    stage_counts: Dict[str, int] = defaultdict(int)
    for w in winners:
        stage_counts[str(w.get("stage") or "PROBE")] += 1

    lines.append("## Winner Summary")
    lines.append("")
    lines.append(f"- Winners selected: {len(winners)}")
    lines.append(f"- Stage SCALE: {stage_counts.get('SCALE', 0)}")
    lines.append(f"- Stage TEST: {stage_counts.get('TEST', 0)}")
    lines.append(f"- Stage PROBE: {stage_counts.get('PROBE', 0)}")
    lines.append("")

    lines.append("## Account Readiness")
    lines.append("")
    for p in PLATFORMS:
        lines.append(f"- {p}: {'READY' if account_ready.get(p, False) else 'MISSING'}")
    lines.append("")

    lines.append("## Top Winners")
    lines.append("")
    for w in winners[:20]:
        lines.append(
            "- "
            + f"{w.get('product')} | score={float(w.get('winner_score') or 0.0):.2f} "
            + f"| profit=${float(w.get('net_profit') or 0.0):.2f} "
            + f"| margin={float(w.get('margin_pct') or 0.0):.1f}% "
            + f"| stage={w.get('stage')} "
            + f"| routes={w.get('distribution_vector')}"
        )
    lines.append("")

    lines.append("## Queue Counts")
    lines.append("")
    for p in PLATFORMS:
        rows = queues.get(p, [])
        auto_ready = sum(1 for r in rows if (r.get("queue_status") or "") == "AUTO_READY")
        blocked = len(rows) - auto_ready
        lines.append(f"- {p}: total={len(rows)} auto_ready={auto_ready} blocked={blocked}")
    lines.append("")

    lines.append("## Auto Listing Commands")
    lines.append("")
    lines.append("- eBay: `python3 AUTOMATIONS/auto_list_products.py --platform ebay`")
    lines.append("- Etsy: `python3 AUTOMATIONS/auto_list_products.py --platform etsy`")
    lines.append("- Redbubble: `python3 AUTOMATIONS/auto_list_products.py --platform redbubble`")
    lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def write_latest_html(md_text: str) -> None:
    esc = (
        md_text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )
    html = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>PRINTMAXX Ecom Autopilot</title>
  <style>
    body {{ margin: 0; background: #0b0b0b; color: #eaeaea; font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace; }}
    .wrap {{ max-width: 1120px; margin: 0 auto; padding: 20px; }}
    pre {{ white-space: pre-wrap; line-height: 1.45; font-size: 13px; }}
  </style>
</head>
<body>
  <div class="wrap"><pre>{esc}</pre></div>
</body>
</html>
"""
    LATEST_HTML.write_text(html, encoding="utf-8")


def write_manifest(
    winners: List[Dict[str, Any]],
    queues: Dict[str, List[Dict[str, Any]]],
    account_ready: Dict[str, bool],
) -> None:
    queue_stats: Dict[str, Dict[str, int]] = {}
    for p, rows in queues.items():
        queue_stats[p] = {
            "total": len(rows),
            "auto_ready": sum(1 for r in rows if (r.get("queue_status") or "") == "AUTO_READY"),
            "blocked": sum(1 for r in rows if (r.get("queue_status") or "") != "AUTO_READY"),
        }

    payload = {
        "generated_at": now_iso(),
        "arb_ledger": str(ARB_LEDGER),
        "winners_count": len(winners),
        "winners": winners,
        "queues": {p: str((QUEUE_DIR / f"{p}_queue.csv")) for p in PLATFORMS},
        "queue_stats": queue_stats,
        "account_ready": account_ready,
    }
    MANIFEST.write_text(json.dumps(payload, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")


def run_tick(top: int, min_margin: float, min_profit: float, include_watch: bool) -> Dict[str, Any]:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    QUEUE_DIR.mkdir(parents=True, exist_ok=True)

    arb_rows = read_csv_rows(ARB_LEDGER, max_rows=200000)
    opportunities = dedupe_best_opportunities(arb_rows)
    winners = build_winners(
        opportunities,
        top=top,
        min_margin=min_margin,
        min_profit=min_profit,
        include_watch=include_watch,
    )
    account_ready = load_account_readiness()
    queues = build_platform_queues(winners, account_ready)

    write_winners_ledger(winners)

    queue_fields = [
        "generated_at",
        "platform",
        "queue_status",
        "auto_capable",
        "account_ready",
        "product_id",
        "product",
        "category",
        "stage",
        "winner_score",
        "sell_price",
        "source_price",
        "net_profit",
        "margin_pct",
        "best_platform",
        "title",
        "description",
        "tags",
        "organic_budget_usd",
        "paid_test_budget_usd",
        "next_action",
    ]
    for platform, rows in queues.items():
        write_csv_rows(QUEUE_DIR / f"{platform}_queue.csv", queue_fields, rows)

    md = render_latest_md(winners, queues, account_ready)
    LATEST_MD.write_text(md, encoding="utf-8")
    write_latest_html(md)
    write_manifest(winners, queues, account_ready)

    return {
        "winners": winners,
        "queues": queues,
        "account_ready": account_ready,
    }


def parse_args() -> argparse.Namespace:
    ap = argparse.ArgumentParser(description="PRINTMAXX ecom autopilot")
    ap.add_argument("--tick", action="store_true", help="Run one non-interactive generation tick")
    ap.add_argument("--top", type=int, default=12, help="Top winners to keep active (default: 12)")
    ap.add_argument("--min-margin", type=float, default=20.0, help="Minimum margin percent (default: 20)")
    ap.add_argument("--min-profit", type=float, default=3.0, help="Minimum net profit USD (default: 3)")
    ap.add_argument("--include-watch", action="store_true", help="Include WATCH actions in winner pool")
    return ap.parse_args()


def main() -> int:
    args = parse_args()
    if not args.tick:
        print("Use --tick to run autopilot generation.")
        return 2

    res = run_tick(
        top=max(1, int(args.top)),
        min_margin=float(args.min_margin),
        min_profit=float(args.min_profit),
        include_watch=bool(args.include_watch),
    )
    winners = res["winners"]
    queues = res["queues"]
    auto_ready_total = sum(
        1 for rows in queues.values() for r in rows if (r.get("queue_status") or "") == "AUTO_READY"
    )
    print(
        "ecom_autopilot: "
        + f"winners={len(winners)} "
        + f"queue_rows={sum(len(v) for v in queues.values())} "
        + f"auto_ready={auto_ready_total} "
        + f"manifest={MANIFEST}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
