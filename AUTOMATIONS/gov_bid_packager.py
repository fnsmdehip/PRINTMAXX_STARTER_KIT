#!/usr/bin/env python3
"""Gov bid pack (no bidding).

Summarizes actionable, upcoming-deadline opportunities from LEDGER/GOV_OPPORTUNITIES.csv
into a single human-executable pack.

This intentionally does NOT submit bids, create accounts, or interact with portals.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path
from typing import Any, Dict, List, Optional


BASE = Path(__file__).resolve().parent.parent
LEDGER = BASE / "LEDGER"
OUT_DIR = BASE / "output" / "gov"

SRC = LEDGER / "GOV_OPPORTUNITIES.csv"
LATEST_MD = OUT_DIR / "latest.md"
LATEST_HTML = OUT_DIR / "latest.html"
MANIFEST = OUT_DIR / "manifest.json"


def now_iso() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def parse_deadline(raw: str) -> Optional[date]:
    s = (raw or "").strip()
    if not s:
        return None
    # Common formats seen in SAM/exports.
    fmts = [
        "%Y-%m-%d",
        "%m/%d/%Y",
        "%Y/%m/%d",
        "%Y-%m-%dT%H:%M:%S",
        "%Y-%m-%d %H:%M:%S",
    ]
    for fmt in fmts:
        try:
            return datetime.strptime(s, fmt).date()
        except Exception:
            continue
    # Last resort: pull YYYY-MM-DD from text.
    m = re.search(r"(\d{4}-\d{2}-\d{2})", s)
    if m:
        try:
            return datetime.strptime(m.group(1), "%Y-%m-%d").date()
        except Exception:
            return None
    return None


def safe_float(v: object, default: float = 0.0) -> float:
    try:
        return float(str(v).strip())
    except Exception:
        return default


def classify_lane(title: str, desc: str) -> str:
    t = (title or "").lower()
    d = (desc or "").lower()
    blob = f"{t}\n{d}"

    lanes = [
        ("web_dev", ["website", "web", "wordpress", "drupal", "cms", "ui/ux", "redesign", "frontend", "react"]),
        ("software_dev", ["software", "app", "api", "development", "programming", "system design", "integration"]),
        ("data_analysis", ["data", "analysis", "analytics", "dashboard", "reporting", "etl", "sql", "python"]),
        ("tech_writing", ["technical writing", "documentation", "manual", "sop", "instructional", "whitepaper"]),
        ("marketing", ["marketing", "social media", "seo", "content", "communications", "public relations"]),
        ("training", ["training", "curriculum", "course", "instructional design", "learning", "workshop"]),
    ]
    for lane, kws in lanes:
        if any(kw in blob for kw in kws):
            return lane
    return "other"


def load_rows(limit: int = 10000) -> List[Dict[str, str]]:
    if not SRC.exists():
        return []
    rows: List[Dict[str, str]] = []
    try:
        with open(SRC, "r", encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f)
            for i, row in enumerate(reader):
                if i >= limit:
                    break
                if isinstance(row, dict):
                    rows.append({k: (v or "").strip() for k, v in row.items()})
    except Exception:
        return []
    return rows


def select_needs_review(max_items: int = 25) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    seen: set[str] = set()
    for r in load_rows():
        oid = (r.get("opportunity_id") or "").strip()
        url = (r.get("url") or "").strip()
        key = oid or url
        if not key or key in seen:
            continue
        seen.add(key)

        deadline_raw = (r.get("response_deadline") or "").strip()
        if deadline_raw:
            continue  # handled by open opps section

        source = (r.get("source") or "").strip().lower()
        status = (r.get("status") or "").strip().upper()
        if "sam.gov html" not in source and not status.endswith("REVIEW") and not oid.startswith("SEARCH_"):
            continue

        title = (r.get("title") or "").strip() or "(untitled)"
        desc = (r.get("description") or "").strip()
        out.append(
            {
                "opportunity_id": oid,
                "title": title,
                "agency": (r.get("agency") or "").strip() or "Various",
                "url": url,
                "source": (r.get("source") or "").strip(),
                "status": status,
                "keyword_match": (r.get("keyword_match") or "").strip(),
                "lane": classify_lane(title, desc),
                "description": desc[:500],
            }
        )

    out.sort(key=lambda it: (str(it.get("keyword_match") or ""), str(it.get("title") or "")))
    return out[:max_items]


def select_open_opps(max_items: int = 25, max_days_out: int = 60) -> List[Dict[str, Any]]:
    today = date.today()
    out: List[Dict[str, Any]] = []
    seen: set[str] = set()

    for r in load_rows():
        oid = (r.get("opportunity_id") or "").strip()
        url = (r.get("url") or "").strip()
        key = oid or url
        if not key:
            continue
        if key in seen:
            continue
        seen.add(key)

        title = (r.get("title") or "").strip()
        agency = (r.get("agency") or "").strip()
        deadline_raw = (r.get("response_deadline") or "").strip()
        deadline = parse_deadline(deadline_raw)
        if deadline is None:
            continue

        days_left = (deadline - today).days
        if days_left < 0:
            continue
        if days_left > max_days_out:
            continue

        desc = (r.get("description") or "").strip()
        item = {
            "opportunity_id": oid,
            "title": title or "(untitled)",
            "agency": agency,
            "deadline": deadline.isoformat(),
            "days_left": days_left,
            "set_aside": (r.get("set_aside") or "").strip(),
            "naics": (r.get("naics") or "").strip(),
            "estimated_value": safe_float(r.get("estimated_value"), 0.0),
            "url": url,
            "source": (r.get("source") or "").strip(),
            "keyword_match": (r.get("keyword_match") or "").strip(),
            "lane": classify_lane(title, desc),
        }
        out.append(item)

    out.sort(key=lambda it: (int(it.get("days_left") or 9999), -float(it.get("estimated_value") or 0.0)))
    return out[:max_items]


def render_markdown(open_opps: List[Dict[str, Any]], needs_review: List[Dict[str, Any]]) -> str:
    lines: List[str] = []
    lines.append("# PRINTMAXX Gov Bid Pack (No Bidding)")
    lines.append("")
    lines.append(f"Generated: {now_iso()}")
    lines.append("")
    lines.append(f"Source ledger: {SRC}")
    lines.append("")
    lines.append("## Open Opportunities (upcoming deadlines)")
    lines.append("")

    if not open_opps:
        lines.append("- None (monitor may be offline or ledger contains only awards).")
    else:
        for it in open_opps:
            title = it.get("title") or "(untitled)"
            agency = it.get("agency") or "n/a"
            deadline = it.get("deadline") or "n/a"
            days_left = it.get("days_left")
            est = float(it.get("estimated_value") or 0.0)
            est_s = f"${est:,.0f}" if est else "n/a"
            lane = it.get("lane") or "other"
            url = it.get("url") or ""

            lines.append(f"- D-{days_left} | {deadline} | {agency} | {title}")
            lines.append(
                f"  - lane={lane} | naics={it.get('naics') or 'n/a'} | set_aside={it.get('set_aside') or 'n/a'} | est={est_s}"
            )
            if url:
                lines.append(f"  - url={url}")
            if it.get("opportunity_id"):
                lines.append(f"  - id={it.get('opportunity_id')}")
            if it.get("source"):
                lines.append(f"  - source={it.get('source')}")
            if it.get("keyword_match"):
                lines.append(f"  - keyword_match={it.get('keyword_match')}")

    lines.append("")
    lines.append("## SAM.gov Search Hits (Manual Review Needed)")
    lines.append("")
    if not needs_review:
        lines.append("- None.")
    else:
        for it in needs_review:
            title = it.get("title") or "(untitled)"
            agency = it.get("agency") or "Various"
            lane = it.get("lane") or "other"
            url = it.get("url") or ""
            lines.append(f"- {agency} | {title}")
            lines.append(f"  - lane={lane} | status={it.get('status') or 'n/a'} | keyword_match={it.get('keyword_match') or 'n/a'}")
            if url:
                lines.append(f"  - url={url}")

    lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def write_html(md_text: str) -> None:
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
  <title>PRINTMAXX Gov Bid Pack</title>
  <style>
    body {{ margin: 0; background: #0b0b0b; color: #eaeaea; font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace; }}
    .wrap {{ max-width: 1100px; margin: 0 auto; padding: 18px; }}
    pre {{ white-space: pre-wrap; line-height: 1.5; font-size: 13px; }}
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


def write_manifest(open_opps: List[Dict[str, Any]], needs_review: List[Dict[str, Any]]) -> None:
    payload = {
        "generated_at": now_iso(),
        "ledger": str(SRC) if SRC.exists() else "",
        "open_count": len(open_opps),
        "open": open_opps,
        "needs_review_count": len(needs_review),
        "needs_review": needs_review,
    }
    MANIFEST.write_text(json.dumps(payload, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--max-items", type=int, default=25)
    ap.add_argument("--max-days-out", type=int, default=60)
    args = ap.parse_args()

    if not args.write:
        ap.print_help()
        return 2

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    open_opps = select_open_opps(max_items=max(1, int(args.max_items)), max_days_out=max(1, int(args.max_days_out)))
    needs_review = select_needs_review(max_items=25)
    md = render_markdown(open_opps, needs_review)
    LATEST_MD.write_text(md, encoding="utf-8")
    write_html(md)
    write_manifest(open_opps, needs_review)
    print(f"gov_bid_packager: wrote {LATEST_MD}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
