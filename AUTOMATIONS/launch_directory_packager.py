#!/usr/bin/env python3
"""Launch directory packager (no auto-submission).

Creates:
  1) A single tracker CSV for submissions across directories.
  2) Per-product "submission payloads" and checklists.

This is intentionally human-executable. It avoids automated form submission
and keeps Ship Captain compliant and low-blast-radius.

Inputs:
  - LEDGER/LAUNCH_DIRECTORIES_MASTER.csv
  - output/apps/manifest.json (optional; products derived from discovered apps)

Outputs:
  - LEDGER/LAUNCH_DIRECTORY_TRACKER.csv (created/updated)
  - output/launch/latest.md + latest.html + manifest.json
  - output/launch/items/<product_id>/submission_payload.json + checklist.md
"""

from __future__ import annotations

import argparse
import csv
import json
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


BASE = Path(__file__).resolve().parent.parent
LEDGER = BASE / "LEDGER"
OUT = BASE / "output" / "launch"
ITEMS_DIR = OUT / "items"

DIR_MASTER = LEDGER / "LAUNCH_DIRECTORIES_MASTER.csv"
TRACKER = LEDGER / "LAUNCH_DIRECTORY_TRACKER.csv"
APPS_MANIFEST = BASE / "output" / "apps" / "manifest.json"
NATIVE_APPS_MANIFEST = BASE / "output" / "native_apps" / "manifest.json"
DEPLOYMENT_URLS_MD = BASE / "OPS" / "DEPLOYMENT_URLS.md"

LATEST_MD = OUT / "latest.md"
LATEST_HTML = OUT / "latest.html"
MANIFEST = OUT / "manifest.json"


PRIORITY_RANK = {"HIGHEST": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3}


def now_iso() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def load_json(path: Path) -> dict:
    if not path.exists():
        return {}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
        return payload if isinstance(payload, dict) else {}
    except Exception:
        return {}


def read_csv_dicts(path: Path, max_rows: int = 20000) -> List[Dict[str, str]]:
    if not path.exists():
        return []
    out: List[Dict[str, str]] = []
    try:
        with open(path, "r", encoding="utf-8", newline="") as f:
            r = csv.DictReader(f)
            for i, row in enumerate(r):
                if i >= max_rows:
                    break
                if isinstance(row, dict):
                    out.append({k: (v or "").strip() for k, v in row.items()})
    except Exception:
        return []
    return out


def write_csv_dicts(path: Path, rows: List[Dict[str, str]], fieldnames: List[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for row in rows:
            w.writerow({k: (row.get(k, "") or "") for k in fieldnames})


def load_deployed_urls() -> Dict[str, str]:
    """Best-effort parse OPS/DEPLOYMENT_URLS.md into {app_id: url} for LIVE apps."""
    if not DEPLOYMENT_URLS_MD.exists():
        return {}
    try:
        lines = DEPLOYMENT_URLS_MD.read_text(encoding="utf-8", errors="replace").splitlines()
    except Exception:
        return {}

    mapping: Dict[str, str] = {}
    in_table = False
    for raw in lines:
        line = raw.strip()
        if not line:
            if in_table:
                break
            continue
        if line.lower().startswith("| app | url | status |"):
            in_table = True
            continue
        if not in_table:
            continue
        if line.startswith("|-----"):
            continue
        if not line.startswith("|") or line.count("|") < 4:
            continue
        cols = [c.strip() for c in line.strip("|").split("|")]
        if len(cols) < 3:
            continue
        app_id = cols[0]
        url = cols[1]
        status = cols[2].upper()
        if status != "LIVE":
            continue
        if url.startswith("http://") or url.startswith("https://"):
            mapping[app_id] = url
        elif url:
            mapping[app_id] = "https://" + url.lstrip("/")
    return mapping


def load_directories() -> List[Dict[str, str]]:
    if not DIR_MASTER.exists():
        return []
    dirs = read_csv_dicts(DIR_MASTER)
    # Only ACTIVE entries
    active = [d for d in dirs if (d.get("status") or "").strip().upper() == "ACTIVE"]

    def key(d: Dict[str, str]):
        pri = (d.get("priority") or "").strip().upper()
        return (PRIORITY_RANK.get(pri, 9), d.get("directory_name", ""))

    active.sort(key=key)
    return active


def derive_products() -> List[Dict[str, Any]]:
    products: List[Dict[str, Any]] = []
    deployed = load_deployed_urls()
    apps = load_json(APPS_MANIFEST)
    items = apps.get("items") if isinstance(apps.get("items"), list) else []
    for it in items:
        if not isinstance(it, dict):
            continue
        pid = (it.get("app_id") or "").strip()
        if not pid:
            continue
        products.append(
            {
                "product_id": pid,
                "product_type": "app",
                "name": (it.get("title") or pid).strip() or pid,
                "tagline": (it.get("tagline") or "").strip(),
                "description": (it.get("description") or "").strip(),
                # No live URLs until deploy step succeeds.
                "website_url": deployed.get(pid, ""),
                "desktop_png": (it.get("desktop_png") or "").strip(),
                "mobile_png": (it.get("mobile_png") or "").strip(),
            }
            )
    # Also include native app projects as launchable products (no auto-submission).
    native = load_json(NATIVE_APPS_MANIFEST)
    nitems = native.get("items") if isinstance(native.get("items"), list) else []
    for it in nitems:
        if not isinstance(it, dict):
            continue
        key = (it.get("key") or "").strip()
        app_id = (it.get("app_id") or "").strip()
        if not app_id:
            continue
        # Ensure uniqueness even when templates share the same folder name.
        pid = f"native-{(key.replace('__','-') if key else app_id)}"
        app_path = (it.get("path") or "").strip()
        screenshots_dir = ""
        mobile_png = ""
        if app_path:
            try:
                p = Path(app_path)
                sdir = p / "screenshots"
                if sdir.exists() and sdir.is_dir():
                    screenshots_dir = str(sdir)
                    # Best-effort pick a representative screenshot.
                    for cand in sorted(sdir.iterdir()):
                        if not cand.is_file():
                            continue
                        if cand.suffix.lower() in {".png", ".jpg", ".jpeg", ".webp"}:
                            mobile_png = str(cand)
                            break
            except Exception:
                pass

        expo = it.get("expo") if isinstance(it.get("expo"), dict) else {}
        name = (expo.get("name") or "").strip() if expo else ""
        products.append(
            {
                "product_id": pid,
                "product_type": "native_app",
                "name": name or app_id,
                "tagline": "",
                "description": "",
                "website_url": "",
                "desktop_png": screenshots_dir,  # directory path for humans
                "mobile_png": mobile_png,
            }
        )
    return products


def ensure_tracker(directories: List[Dict[str, str]], products: List[Dict[str, Any]]) -> None:
    fieldnames = [
        "product_id",
        "directory_id",
        "directory_name",
        "directory_url",
        "priority",
        "status",
        "submitted_date",
        "approved_date",
        "traffic_generated",
        "notes",
    ]

    existing = read_csv_dicts(TRACKER)
    by_key: Dict[Tuple[str, str], Dict[str, str]] = {}
    for row in existing:
        pid = (row.get("product_id") or "").strip()
        did = (row.get("directory_id") or "").strip()
        if pid and did:
            by_key[(pid, did)] = row

    out_rows: List[Dict[str, str]] = []
    for prod in products:
        pid = str(prod.get("product_id") or "").strip()
        if not pid:
            continue
        for d in directories:
            did = (d.get("directory_id") or "").strip()
            if not did:
                continue
            key = (pid, did)
            prev = by_key.get(key, {})
            out_rows.append(
                {
                    "product_id": pid,
                    "directory_id": did,
                    "directory_name": d.get("directory_name", ""),
                    "directory_url": d.get("url", ""),
                    "priority": (d.get("priority") or "").strip().upper(),
                    "status": (prev.get("status") or "PENDING").strip().upper(),
                    "submitted_date": prev.get("submitted_date", ""),
                    "approved_date": prev.get("approved_date", ""),
                    "traffic_generated": prev.get("traffic_generated", ""),
                    "notes": prev.get("notes", ""),
                }
            )

    # Stable ordering for diffing.
    out_rows.sort(key=lambda r: (r.get("product_id", ""), PRIORITY_RANK.get(r.get("priority", ""), 9), r.get("directory_id", "")))
    write_csv_dicts(TRACKER, out_rows, fieldnames)


def best_directories_for_product(directories: List[Dict[str, str]], max_items: int = 12) -> List[Dict[str, str]]:
    # Currently: simple priority ordering. Later: filter by target_products.
    return directories[: max(1, int(max_items))]


def write_product_pack(prod: Dict[str, Any], directories: List[Dict[str, str]]) -> Dict[str, Any]:
    pid = str(prod.get("product_id") or "").strip() or "product"
    pdir = ITEMS_DIR / pid
    pdir.mkdir(parents=True, exist_ok=True)

    chosen = best_directories_for_product(directories, max_items=12)

    payload = {
        "product_id": pid,
        "name": prod.get("name") or pid,
        "product_type": prod.get("product_type") or "unknown",
        "website_url": prod.get("website_url") or "",
        "tagline": prod.get("tagline") or "",
        "description": prod.get("description") or "",
        "assets": {
            "desktop_png": prod.get("desktop_png") or "",
            "mobile_png": prod.get("mobile_png") or "",
        },
        "directories_top": [
            {
                "directory_id": d.get("directory_id", ""),
                "directory_name": d.get("directory_name", ""),
                "url": d.get("url", ""),
                "priority": (d.get("priority") or "").strip().upper(),
                "category": d.get("category", ""),
                "submission_fee": d.get("submission_fee", ""),
                "approval_time": d.get("approval_time", ""),
                "notes": d.get("notes", ""),
            }
            for d in chosen
        ],
        "generated_at": now_iso(),
    }

    (pdir / "submission_payload.json").write_text(json.dumps(payload, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")

    # Human checklist (kept short; no step-by-step platform bypass guidance).
    lines: List[str] = []
    lines.append(f"# Launch Checklist: {pid}")
    lines.append("")
    lines.append(f"Generated: {now_iso()}")
    lines.append("")
    lines.append("## Payload")
    lines.append("")
    lines.append(f"- Name: {payload['name']}")
    lines.append(f"- Tagline: {payload['tagline']}")
    if payload.get("website_url"):
        lines.append(f"- URL: {payload['website_url']}")
    else:
        lines.append("- URL: (deploy pending)")
    lines.append("")
    lines.append("## Assets")
    lines.append("")
    lines.append(f"- Desktop screenshot: {payload['assets'].get('desktop_png') or 'n/a'}")
    lines.append(f"- Mobile screenshot: {payload['assets'].get('mobile_png') or 'n/a'}")
    lines.append("")
    lines.append("## Directory Targets (Top)")
    lines.append("")
    for d in payload["directories_top"]:
        lines.append(f"- {d['priority']} {d['directory_name']} ({d['url']})")
    lines.append("")

    (pdir / "checklist.md").write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")

    return {
        "product_id": pid,
        "pack_dir": str(pdir),
        "checklist": str((pdir / "checklist.md")),
        "payload": str((pdir / "submission_payload.json")),
        "top_count": len(chosen),
    }


def render_latest_md(products: List[Dict[str, Any]], packs: List[Dict[str, Any]]) -> str:
    lines: List[str] = []
    lines.append("# PRINTMAXX Launch Pack (No Auto-Submission)")
    lines.append("")
    lines.append(f"Generated: {now_iso()}")
    lines.append("")
    lines.append(f"- Products: {len(products)}")
    lines.append(f"- Tracker: {TRACKER}")
    lines.append("")
    if not packs:
        lines.append("- No products found (expected output/apps/manifest.json).")
        lines.append("")
        return "\n".join(lines)

    for p in packs:
        lines.append(f"## {p.get('product_id')}")
        lines.append("")
        lines.append(f"- Checklist: {p.get('checklist')}")
        lines.append(f"- Payload: {p.get('payload')}")
        lines.append(f"- Top dirs: {p.get('top_count')}")
        lines.append("")

    lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def write_html(md_text: str) -> None:
    escaped = md_text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    html = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>PRINTMAXX Launch Pack</title>
  <style>
    body {{ margin: 0; background: #0b0b0b; color: #eaeaea; font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace; }}
    .wrap {{ max-width: 1100px; margin: 0 auto; padding: 18px; }}
    pre {{ white-space: pre-wrap; line-height: 1.5; font-size: 13px; }}
  </style>
</head>
<body>
  <div class="wrap"><pre>{escaped}</pre></div>
</body>
</html>
"""
    LATEST_HTML.write_text(html, encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true")
    # Keep a cap, but default high enough to include the current app/native fleet.
    ap.add_argument("--max-products", type=int, default=80)
    args = ap.parse_args()

    if not args.write:
        ap.print_help()
        return 2

    OUT.mkdir(parents=True, exist_ok=True)
    ITEMS_DIR.mkdir(parents=True, exist_ok=True)

    directories = load_directories()
    products = derive_products()[: max(0, int(args.max_products))]

    ensure_tracker(directories, products)

    packs = [write_product_pack(prod, directories) for prod in products]

    md = render_latest_md(products, packs)
    LATEST_MD.write_text(md, encoding="utf-8")
    write_html(md)

    manifest = {"generated_at": now_iso(), "products": products, "packs": packs, "directories_count": len(directories)}
    MANIFEST.write_text(json.dumps(manifest, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")

    print(f"launch_directory_packager: wrote {LATEST_MD}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
