#!/usr/bin/env python3
"""Native app packaging pipeline (no submit, no deploy).

Goal:
  - Discover Expo/React Native app projects that are already in-repo (e.g. the
    `app factory/app-factory/*` collection).
  - Produce a single "what exists + what's risky + what's ready" pack so the
    human can submit to app stores when ready.

This script is intentionally:
  - local-only (no network)
  - non-destructive (does not modify app projects)
  - blast-radius safe (no credentials uploads, no store submissions)

Outputs:
  - output/native_apps/manifest.json
  - output/native_apps/latest.md
  - output/native_apps/latest.html
  - output/native_apps/items/<key>/meta.json
"""

from __future__ import annotations

import argparse
import json
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


BASE = Path(__file__).resolve().parent.parent

# Source roots (existing app-factory collection outside ralph loops).
APP_FACTORY_ROOT = BASE / "app factory" / "app-factory"
RELIGIOUS_ROOT = APP_FACTORY_ROOT / "religious-apps"
NON_RELIGIOUS_ROOT = APP_FACTORY_ROOT / "non-religious-apps"
CORE_SCRIPTURE_STREAK = BASE / "app factory" / "scripture-streak"
BASE_TEMPLATE_SCRIPTURE_STREAK = APP_FACTORY_ROOT / "base-template" / "scripture-streak"

OUT_DIR = BASE / "output" / "native_apps"
ITEMS_DIR = OUT_DIR / "items"
MANIFEST = OUT_DIR / "manifest.json"
LATEST_MD = OUT_DIR / "latest.md"
LATEST_HTML = OUT_DIR / "latest.html"


def now_iso() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def _read_json(path: Path) -> dict:
    try:
        if path.exists():
            payload = json.loads(path.read_text(encoding="utf-8", errors="replace"))
            return payload if isinstance(payload, dict) else {}
    except Exception:
        return {}
    return {}


def _safe_rel(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(BASE))
    except Exception:
        return str(path.resolve())


def discover_apps(max_apps: int) -> List[Tuple[str, Path]]:
    """Return list of (category, app_dir)."""
    found: List[Tuple[str, Path]] = []

    roots = [
        ("religious", RELIGIOUS_ROOT),
        ("non_religious", NON_RELIGIOUS_ROOT),
        ("core", CORE_SCRIPTURE_STREAK),
        ("template", BASE_TEMPLATE_SCRIPTURE_STREAK),
    ]

    for category, root in roots:
        if not root.exists():
            continue
        # Some roots point directly at an app directory (not a parent folder of apps).
        if (root / "package.json").exists() and (
            (root / "app.json").exists()
            or (root / "app.config.js").exists()
            or (root / "app").exists()
            or (root / "src").exists()
        ):
            found.append((category, root))
            continue

        for p in sorted(root.iterdir()):
            if not p.is_dir():
                continue
            # Treat as app root if it looks like an RN/Expo project.
            if (p / "package.json").exists() and (
                (p / "app.json").exists()
                or (p / "app.config.js").exists()
                or (p / "app").exists()
                or (p / "src").exists()
            ):
                found.append((category, p))

    # Stable ordering by category then name.
    found.sort(key=lambda t: (t[0], t[1].name))
    return found[: max(0, int(max_apps))]


def count_images(dir_path: Path, limit: int = 5000) -> int:
    if not dir_path.exists() or not dir_path.is_dir():
        return 0
    exts = {".png", ".jpg", ".jpeg", ".webp"}
    n = 0
    try:
        for p in dir_path.iterdir():
            if n >= limit:
                break
            if p.is_file() and p.suffix.lower() in exts:
                n += 1
    except Exception:
        return n
    return n


def sensitive_files(app_dir: Path) -> List[str]:
    """Top-level secret-ish artifacts to flag (do not read contents)."""
    globs = [
        "*.p8",
        "*.p12",
        "*.pem",
        "*.key",
        "*.mobileprovision",
        "*.jks",
        "*keystore*",
        "google-services.json",
        "GoogleService-Info.plist",
        "credentials*.json",
        "serviceAccount*.json",
        ".env",
        ".env.*",
    ]

    hits: List[str] = []
    for pat in globs:
        try:
            for p in sorted(app_dir.glob(pat)):
                if p.is_file():
                    hits.append(p.name)
        except Exception:
            continue

    # Dedup while preserving order
    out: List[str] = []
    seen = set()
    for h in hits:
        if h in seen:
            continue
        seen.add(h)
        out.append(h)
    return out


def app_meta(category: str, app_dir: Path) -> Dict[str, Any]:
    pkg = _read_json(app_dir / "package.json")
    appj = _read_json(app_dir / "app.json")

    expo = appj.get("expo") if isinstance(appj.get("expo"), dict) else {}
    expo_name = str(expo.get("name") or "").strip()
    expo_slug = str(expo.get("slug") or "").strip()

    has_ios = (app_dir / "ios").exists()
    has_android = (app_dir / "android").exists()
    screenshots = count_images(app_dir / "screenshots")

    item_key = f"{category}__{app_dir.name}"
    return {
        "key": item_key,
        "category": category,
        "app_id": app_dir.name,
        "path": str(app_dir.resolve()),
        "path_rel": _safe_rel(app_dir),
        "package": {
            "name": str(pkg.get("name") or "").strip(),
            "version": str(pkg.get("version") or "").strip(),
        },
        "expo": {
            "name": expo_name,
            "slug": expo_slug,
        }
        if expo
        else {},
        "has_ios": bool(has_ios),
        "has_android": bool(has_android),
        "screenshots_count": int(screenshots),
        "sensitive_files_top_level": sensitive_files(app_dir),
        "updated_at": now_iso(),
    }


def render_md(items: List[Dict[str, Any]]) -> str:
    lines: List[str] = []
    lines.append("# PRINTMAXX Native App Pack (No Submit)")
    lines.append("")
    lines.append(f"Generated: {now_iso()}")
    lines.append("")

    if not items:
        lines.append("- No app projects discovered.")
        lines.append("")
        lines.append("Expected roots:")
        lines.append(f"- {RELIGIOUS_ROOT}")
        lines.append(f"- {NON_RELIGIOUS_ROOT}")
        lines.append("")
        return "\n".join(lines)

    counts = Counter(str(it.get("category") or "unknown") for it in items)
    lines.append(f"Discovered apps: {len(items)}")
    lines.append(f"- religious: {counts.get('religious', 0)}")
    lines.append(f"- non_religious: {counts.get('non_religious', 0)}")
    lines.append("")

    # Surface the most actionable first: apps that have iOS + screenshots.
    def score(it: Dict[str, Any]) -> Tuple[int, int, int]:
        return (
            1 if it.get("has_ios") else 0,
            1 if it.get("has_android") else 0,
            int(it.get("screenshots_count") or 0),
        )

    ranked = sorted(items, key=score, reverse=True)

    for it in ranked[:50]:
        key = it.get("key") or ""
        app_id = it.get("app_id") or key
        expo = it.get("expo") if isinstance(it.get("expo"), dict) else {}
        expo_name = (expo.get("name") or "").strip()
        expo_slug = (expo.get("slug") or "").strip()
        pkg = it.get("package") if isinstance(it.get("package"), dict) else {}
        pkg_name = (pkg.get("name") or "").strip()
        pkg_ver = (pkg.get("version") or "").strip()
        sens = it.get("sensitive_files_top_level") if isinstance(it.get("sensitive_files_top_level"), list) else []

        title = expo_name or app_id
        lines.append(f"## {app_id}: {title}")
        lines.append("")
        lines.append(f"- Key: {key}")
        lines.append(f"- Path: {it.get('path')}")
        if pkg_name or pkg_ver:
            lines.append(f"- package.json: {pkg_name or 'n/a'} {('v'+pkg_ver) if pkg_ver else ''}".strip())
        if expo_slug:
            lines.append(f"- Expo slug: {expo_slug}")
        lines.append(f"- iOS project: {'yes' if it.get('has_ios') else 'no'}")
        lines.append(f"- Android project: {'yes' if it.get('has_android') else 'no'}")
        lines.append(f"- Screenshots: {int(it.get('screenshots_count') or 0)}")
        if sens:
            # Flag only; do not expose contents.
            lines.append(f"- Sensitive files (top-level): {', '.join(str(x) for x in sens[:12])}{' ...' if len(sens) > 12 else ''}")
        lines.append("")

    if len(items) > 50:
        lines.append(f"(Showing 50/{len(items)}.)")
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def write_html(md_text: str) -> None:
    escaped = md_text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    html = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>PRINTMAXX Native App Pack</title>
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
    ap.add_argument("--write", action="store_true", help="Write output/native_apps pack")
    ap.add_argument("--max-apps", type=int, default=60, help="Safety cap (default: 60)")
    args = ap.parse_args()

    if not args.write:
        ap.print_help()
        return 2

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    ITEMS_DIR.mkdir(parents=True, exist_ok=True)

    discovered = discover_apps(max_apps=int(args.max_apps))
    items: List[Dict[str, Any]] = []

    for category, app_dir in discovered:
        meta = app_meta(category, app_dir)
        items.append(meta)

        item_dir = ITEMS_DIR / str(meta["key"])
        item_dir.mkdir(parents=True, exist_ok=True)
        (item_dir / "meta.json").write_text(json.dumps(meta, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")

    manifest = {
        "generated_at": now_iso(),
        "source_roots": [str(RELIGIOUS_ROOT), str(NON_RELIGIOUS_ROOT)],
        "count": len(items),
        "items": items,
    }
    MANIFEST.write_text(json.dumps(manifest, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")

    md = render_md(items)
    LATEST_MD.write_text(md, encoding="utf-8")
    write_html(md)
    print(f"native_app_packager: wrote {LATEST_MD}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
