#!/usr/bin/env python3
"""PWA/App packaging pipeline (no deploy, no store submission).

Purpose:
  - Turn existing built apps (currently: ralph/loops/app_factory/output/*) into
    "launch-ready artifacts": metadata, screenshots, and a single latest pack.
  - Designed to run frequently under Ship Captain without thrashing: it only
    regenerates screenshots when an app's index.html changes.

Outputs:
  - output/apps/manifest.json
  - output/apps/latest.md
  - output/apps/latest.html
  - output/apps/items/<app_id>/{desktop.png,mobile.png,meta.json}

No network required. Safe to run on control node.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


BASE = Path(__file__).resolve().parent.parent
APPS_ROOT = BASE / "ralph" / "loops" / "app_factory" / "output"
OPS_STATE = BASE / "OPS" / "_state"
STATE_FILE = OPS_STATE / "app_packager.json"

OUT_DIR = BASE / "output" / "apps"
ITEMS_DIR = OUT_DIR / "items"
MANIFEST = OUT_DIR / "manifest.json"
LATEST_MD = OUT_DIR / "latest.md"
LATEST_HTML = OUT_DIR / "latest.html"


def now_iso() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def load_state() -> dict:
    if not STATE_FILE.exists():
        return {"version": 1, "apps": {}}
    try:
        payload = json.loads(STATE_FILE.read_text(encoding="utf-8"))
        if isinstance(payload, dict):
            payload.setdefault("version", 1)
            payload.setdefault("apps", {})
            if isinstance(payload.get("apps"), dict):
                return payload
    except Exception:
        pass
    return {"version": 1, "apps": {}}


def save_state(state: dict) -> None:
    OPS_STATE.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(json.dumps(state, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")


def extract_title_and_description(html: str) -> Tuple[str, str]:
    title = ""
    desc = ""
    m = re.search(r"<title>(.*?)</title>", html, flags=re.IGNORECASE | re.DOTALL)
    if m:
        title = re.sub(r"\s+", " ", m.group(1)).strip()
    m = re.search(
        r'<meta\s+name=["\']description["\']\s+content=["\'](.*?)["\']',
        html,
        flags=re.IGNORECASE | re.DOTALL,
    )
    if m:
        desc = re.sub(r"\s+", " ", m.group(1)).strip()
    return title, desc


def tagline_from_description(title: str, desc: str) -> str:
    # Aim for <= ~80 chars (PH has 60-ish, but we keep it short).
    base = (desc or "").strip()
    if base:
        # Use first sentence-ish chunk.
        s = re.split(r"[.!?]\s+", base, maxsplit=1)[0].strip()
        s = re.sub(r"\s+", " ", s)
        if len(s) <= 80:
            return s
        return s[:77].rstrip() + "..."
    # Fallback: compressed title.
    t = re.sub(r"\s+", " ", (title or "").strip())
    return t[:77].rstrip() + "..." if len(t) > 80 else t


def try_load_json(path: Path) -> dict:
    if not path.exists():
        return {}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
        return payload if isinstance(payload, dict) else {}
    except Exception:
        return {}


def discover_apps() -> List[Path]:
    if not APPS_ROOT.exists():
        return []
    apps = []
    for p in sorted(APPS_ROOT.iterdir()):
        if not p.is_dir():
            continue
        if (p / "index.html").exists():
            apps.append(p)
    return apps


def screenshot_app(index_path: Path, desktop_png: Path, mobile_png: Path) -> Tuple[bool, str]:
    try:
        from playwright.sync_api import sync_playwright  # type: ignore
    except Exception as e:
        return False, f"playwright not available: {e}"

    uri = index_path.resolve().as_uri()
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)

            def shot(viewport: dict, out_path: Path) -> None:
                page = browser.new_page(viewport=viewport)
                page.goto(uri, wait_until="domcontentloaded", timeout=30_000)
                # Stop motion/animation to avoid blurry screenshots.
                try:
                    page.add_style_tag(content="*{animation:none!important;transition:none!important;}")
                except Exception:
                    pass
                page.wait_for_timeout(800)
                out_path.parent.mkdir(parents=True, exist_ok=True)
                page.screenshot(path=str(out_path), full_page=False)
                page.close()

            shot({"width": 1280, "height": 720}, desktop_png)
            shot({"width": 390, "height": 844}, mobile_png)
            browser.close()
        return True, "ok"
    except Exception as e:
        return False, str(e)


def render_md(items: List[Dict[str, Any]]) -> str:
    lines: List[str] = []
    lines.append("# PRINTMAXX App Pack (No Deploy)")
    lines.append("")
    lines.append(f"Generated: {now_iso()}")
    lines.append("")
    lines.append(f"Discovered apps: {len(items)}")
    lines.append("")
    if not items:
        lines.append("- None found under ralph/loops/app_factory/output/")
        lines.append("")
        return "\n".join(lines)

    for it in items:
        app_id = it.get("app_id") or "unknown"
        title = it.get("title") or app_id
        desc = it.get("description") or ""
        lines.append(f"## {app_id}: {title}")
        lines.append("")
        if desc:
            lines.append(desc)
            lines.append("")
        lines.append(f"- Path: {it.get('app_dir')}")
        lines.append(f"- Index SHA: `{it.get('index_sha')}`")
        lines.append(f"- Tagline draft: {it.get('tagline')}")
        if it.get("manifest_path"):
            lines.append(f"- manifest.json: {it.get('manifest_path')}")
        if it.get("desktop_png"):
            lines.append(f"- desktop screenshot: {it.get('desktop_png')}")
        if it.get("mobile_png"):
            lines.append(f"- mobile screenshot: {it.get('mobile_png')}")
        if it.get("screenshot_status") and it.get("screenshot_status") != "OK":
            lines.append(f"- screenshot_status: {it.get('screenshot_status')}")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def write_html(md_text: str) -> None:
    escaped = md_text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    html = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>PRINTMAXX App Pack</title>
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
    ap.add_argument("--write", action="store_true", help="Write output/apps pack")
    ap.add_argument("--max-apps", type=int, default=12, help="Safety cap (default: 12)")
    args = ap.parse_args()

    if not args.write:
        ap.print_help()
        return 2

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    ITEMS_DIR.mkdir(parents=True, exist_ok=True)

    state = load_state()
    prev_apps = state.get("apps", {}) if isinstance(state.get("apps"), dict) else {}

    apps = discover_apps()[: max(0, int(args.max_apps))]
    items: List[Dict[str, Any]] = []

    for app_dir in apps:
        app_id = app_dir.name
        index_path = app_dir / "index.html"
        manifest_path = app_dir / "manifest.json"
        html = ""
        try:
            html = index_path.read_text(encoding="utf-8", errors="replace")
        except Exception:
            html = ""

        title, desc = extract_title_and_description(html)
        index_sha = sha256_file(index_path)
        tagline = tagline_from_description(title, desc)

        item_dir = ITEMS_DIR / app_id
        item_dir.mkdir(parents=True, exist_ok=True)
        desktop_png = item_dir / "desktop.png"
        mobile_png = item_dir / "mobile.png"
        meta_json = item_dir / "meta.json"

        prev = prev_apps.get(app_id, {}) if isinstance(prev_apps.get(app_id), dict) else {}
        prev_sha = str(prev.get("index_sha") or "")
        need_shots = (prev_sha != index_sha) or (not desktop_png.exists()) or (not mobile_png.exists())

        status = "OK"
        if need_shots:
            ok, msg = screenshot_app(index_path, desktop_png, mobile_png)
            status = "OK" if ok else f"FAIL: {msg[:180]}"

        manifest_payload = try_load_json(manifest_path)

        meta = {
            "app_id": app_id,
            "title": title,
            "description": desc,
            "tagline": tagline,
            "app_dir": str(app_dir),
            "index_path": str(index_path),
            "index_sha": index_sha,
            "manifest_path": str(manifest_path) if manifest_path.exists() else "",
            "manifest": {
                "name": str(manifest_payload.get("name") or ""),
                "short_name": str(manifest_payload.get("short_name") or ""),
                "start_url": str(manifest_payload.get("start_url") or ""),
                "display": str(manifest_payload.get("display") or ""),
            }
            if manifest_payload
            else {},
            "desktop_png": str(desktop_png) if desktop_png.exists() else "",
            "mobile_png": str(mobile_png) if mobile_png.exists() else "",
            "screenshot_status": status,
            "updated_at": now_iso(),
        }
        meta_json.write_text(json.dumps(meta, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")

        items.append(meta)
        prev_apps[app_id] = {"index_sha": index_sha, "updated_at": meta["updated_at"]}

    # Persist state + manifest.
    state["apps"] = prev_apps
    save_state(state)

    manifest = {
        "generated_at": now_iso(),
        "apps_root": str(APPS_ROOT),
        "count": len(items),
        "items": items,
    }
    MANIFEST.write_text(json.dumps(manifest, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")

    md = render_md(items)
    LATEST_MD.write_text(md, encoding="utf-8")
    write_html(md)
    print(f"app_packager: wrote {LATEST_MD}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
