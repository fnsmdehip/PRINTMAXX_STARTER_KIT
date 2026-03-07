#!/usr/bin/env python3
"""
Render Gumroad product cover images from HTML using Playwright.
Usage: python3 MEDIA/render_gumroad_covers.py
"""

import json
from pathlib import Path
from datetime import datetime
from playwright.sync_api import sync_playwright

BASE_DIR = Path(__file__).parent
HTML_DIR = BASE_DIR / "generated_images"
OUTPUT_DIR = BASE_DIR / "generated_images"

COVERS = [
    {
        "id": "gumroad_cover_1",
        "html": "gumroad_cover_1.html",
        "width": 1600,
        "height": 900,
        "product": "5 AI Prompts That Save 2 Hours Per Week",
        "price": "FREE",
    },
    {
        "id": "gumroad_cover_2",
        "html": "gumroad_cover_2.html",
        "width": 1600,
        "height": 900,
        "product": "Funnel Teardown Guide",
        "price": "$7",
    },
    {
        "id": "gumroad_cover_3",
        "html": "gumroad_cover_3.html",
        "width": 1600,
        "height": 900,
        "product": "73 Cold Email Subject Lines That Actually Get Opens",
        "price": "$29",
    },
    {
        "id": "gumroad_cover_4",
        "html": "gumroad_cover_4.html",
        "width": 1600,
        "height": 900,
        "product": "Cold Email Playbook",
        "price": "$27",
    },
    {
        "id": "gumroad_cover_5",
        "html": "gumroad_cover_5.html",
        "width": 1600,
        "height": 900,
        "product": "Local Biz Client Machine",
        "price": "$97",
    },
]


def render_cover(page, cover: dict) -> dict:
    html_path = HTML_DIR / cover["html"]
    html_content = html_path.read_text()

    page.set_viewport_size({"width": cover["width"], "height": cover["height"]})
    page.set_content(html_content, wait_until="networkidle")

    output_path = OUTPUT_DIR / f'{cover["id"]}.png'
    page.screenshot(path=str(output_path), type="png", full_page=False)

    size = output_path.stat().st_size
    print(f'  [OK] {cover["id"]}.png ({size // 1024}KB) — {cover["product"]} {cover["price"]}')

    return {
        "id": cover["id"],
        "path": str(output_path),
        "product": cover["product"],
        "price": cover["price"],
        "size_bytes": size,
        "width": cover["width"],
        "height": cover["height"],
        "category": "Gumroad Product Cover",
        "generated_at": datetime.now().isoformat(),
    }


def main():
    print("PRINTMAXX Gumroad Cover Generator")
    print("=" * 50)
    print(f"Rendering {len(COVERS)} covers at 1600x900")
    print()

    results = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        for cover in COVERS:
            try:
                result = render_cover(page, cover)
                results.append(result)
            except Exception as e:
                print(f'  [FAIL] {cover["id"]}: {e}')

        browser.close()

    # Update catalog
    catalog_path = OUTPUT_DIR / "catalog.json"
    existing: list = []
    if catalog_path.exists():
        try:
            existing = json.loads(catalog_path.read_text())
        except Exception:
            existing = []

    catalog_map = {e["id"]: e for e in existing}
    for entry in results:
        catalog_map[entry["id"]] = entry
    merged = list(catalog_map.values())
    catalog_path.write_text(json.dumps(merged, indent=2))

    print()
    print("=" * 50)
    print(f"Done: {len(results)}/{len(COVERS)} covers rendered")
    print(f"Catalog updated: {len(merged)} total entries")
    print(f"Output: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
