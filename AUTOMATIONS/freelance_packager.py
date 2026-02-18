#!/usr/bin/env python3
"""Freelance execution pack (no posting).

Collects auto-generated response drafts (dry-run) and summarizes the best ones for quick human execution.

Inputs:
  - AUTOMATIONS/freelance_responses_auto/*.md
  - LEDGER/FREELANCE_DEMAND_SCAN.csv (optional; for counts)

Outputs (overwritten each run):
  - output/freelance/latest.md
  - output/freelance/latest.html
  - output/freelance/manifest.json
"""

from __future__ import annotations

import argparse
import csv
import json
import re
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


BASE = Path(__file__).resolve().parent.parent
LEDGER = BASE / "LEDGER"
RESP_DIR = BASE / "AUTOMATIONS" / "freelance_responses_auto"
SCAN_CSV = LEDGER / "FREELANCE_DEMAND_SCAN.csv"

OUT = BASE / "output" / "freelance"
LATEST_MD = OUT / "latest.md"
LATEST_HTML = OUT / "latest.html"
MANIFEST = OUT / "manifest.json"


def now_iso() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def parse_generated_ts(text: str) -> Optional[datetime]:
    m = re.search(r"^\*\*Generated:\*\*\s+([0-9T:\-\.]+)", text, flags=re.MULTILINE)
    if not m:
        return None
    raw = m.group(1).strip()
    try:
        # Handles ISO like 2026-02-14T03:43:49.572502
        return datetime.fromisoformat(raw.replace("Z", ""))
    except Exception:
        return None


def extract_field(text: str, label: str) -> str:
    # Matches "**Label:** value"
    pat = rf"^\*\*{re.escape(label)}:\*\*\s*(.+)$"
    m = re.search(pat, text, flags=re.MULTILINE)
    return (m.group(1).strip() if m else "")


def extract_response_block(text: str) -> str:
    lines = text.splitlines()
    start = None
    for i, line in enumerate(lines):
        if line.strip().lower().startswith("## response"):
            start = i + 1
            break
    if start is None:
        return ""

    # Skip blank lines
    while start < len(lines) and not lines[start].strip():
        start += 1

    out: List[str] = []
    for j in range(start, len(lines)):
        s = lines[j].rstrip("\n")
        if s.strip() == "---":
            break
        if s.strip().lower().startswith("## sample deliverable spec"):
            break
        if s.strip().lower().startswith("## follow-up"):
            break
        out.append(s)
    return "\n".join(out).strip()


def load_scan_count() -> int:
    if not SCAN_CSV.exists():
        return 0
    try:
        with open(SCAN_CSV, "r", encoding="utf-8", newline="") as f:
            return sum(1 for _ in csv.DictReader(f))
    except Exception:
        return 0


def load_response_drafts(max_age_hours: int = 72) -> List[Dict[str, Any]]:
    if not RESP_DIR.exists():
        return []

    cutoff = datetime.now() - timedelta(hours=max_age_hours)
    items: List[Dict[str, Any]] = []

    for p in sorted(RESP_DIR.glob("*.md")):
        try:
            text = p.read_text(encoding="utf-8", errors="replace")
        except Exception:
            continue

        gen_dt = parse_generated_ts(text)
        if gen_dt is None:
            try:
                gen_dt = datetime.fromtimestamp(p.stat().st_mtime)
            except Exception:
                gen_dt = datetime.now()

        if gen_dt < cutoff:
            continue

        score_raw = extract_field(text, "Score") or "0"
        try:
            score = int(float(re.sub(r"[^\d\.]", "", score_raw) or "0"))
        except Exception:
            score = 0

        item = {
            "path": str(p),
            "generated_at": gen_dt.isoformat(timespec="seconds"),
            "post": extract_field(text, "Post"),
            "source": extract_field(text, "Source"),
            "score": score,
            "budget": extract_field(text, "Budget"),
            "url": extract_field(text, "URL"),
            "services": extract_field(text, "Services"),
            "response": extract_response_block(text),
        }
        items.append(item)

    # Prefer higher score, then more recent.
    items.sort(key=lambda it: (-int(it.get("score") or 0), str(it.get("generated_at") or "")), reverse=False)
    return items


def render_markdown(items: List[Dict[str, Any]], scan_count: int, top_n: int = 5) -> str:
    lines: List[str] = []
    lines.append("# PRINTMAXX Freelance Pack (No Posting)")
    lines.append("")
    lines.append(f"Generated: {now_iso()}")
    lines.append("")
    lines.append(f"- Demand scan rows (latest CSV): {scan_count}")
    lines.append(f"- Response drafts found (last 72h): {len(items)}")
    lines.append("")

    lines.append("## Top Draft Responses (copy/paste ready)")
    lines.append("")
    if not items:
        lines.append("- None (run: python3 AUTOMATIONS/auto_freelance_responder.py --dry-run)")
        lines.append("")
        return "\n".join(lines).rstrip() + "\n"

    for idx, it in enumerate(items[: max(1, top_n)], start=1):
        title = (it.get("post") or "").strip() or "Untitled"
        url = (it.get("url") or "").strip()
        lines.append(f"### {idx}. {title}")
        lines.append("")
        lines.append(f"- Score: {it.get('score')}")
        if it.get("budget"):
            lines.append(f"- Budget: {it.get('budget')}")
        if it.get("source"):
            lines.append(f"- Source: {it.get('source')}")
        if it.get("services"):
            lines.append(f"- Services: {it.get('services')}")
        if url:
            lines.append(f"- URL: {url}")
        lines.append(f"- Draft file: {it.get('path')}")
        lines.append("")
        resp = (it.get("response") or "").strip()
        if resp:
            lines.append("```text")
            lines.append(resp)
            lines.append("```")
        lines.append("")

    lines.append("## More Drafts")
    lines.append("")
    for it in items[top_n : top_n + 15]:
        title = (it.get("post") or "").strip() or "Untitled"
        lines.append(f"- {title} (score={it.get('score')}) -> {it.get('path')}")

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
  <title>PRINTMAXX Freelance Pack</title>
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


def write_manifest(items: List[Dict[str, Any]], scan_count: int) -> None:
    payload = {
        "generated_at": now_iso(),
        "scan_csv": str(SCAN_CSV) if SCAN_CSV.exists() else "",
        "scan_count": scan_count,
        "draft_count": len(items),
        "drafts": items[:50],
    }
    MANIFEST.write_text(json.dumps(payload, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--top", type=int, default=5)
    ap.add_argument("--max-age-hours", type=int, default=72)
    args = ap.parse_args()

    if not args.write:
        ap.print_help()
        return 2

    OUT.mkdir(parents=True, exist_ok=True)

    scan_count = load_scan_count()
    items = load_response_drafts(max_age_hours=max(1, int(args.max_age_hours)))
    md = render_markdown(items, scan_count, top_n=max(1, int(args.top)))
    LATEST_MD.write_text(md, encoding="utf-8")
    write_html(md)
    write_manifest(items, scan_count)
    print(f"freelance_packager: wrote {LATEST_MD}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

