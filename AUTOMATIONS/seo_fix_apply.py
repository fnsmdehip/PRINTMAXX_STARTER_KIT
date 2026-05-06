#!/usr/bin/env python3
"""Apply all SEO fixes: replace data:URI OG images, update dateModified, fix sitemaps."""

import re
import os
from pathlib import Path
from datetime import date

BASE = Path("/Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt/LANDING")
TODAY = date.today().isoformat()  # 2026-05-05

# ── 1. Fix data:image OG URLs ────────────────────────────────────────────────

OG_FIXES = {
    "cnsnt": "https://cnsnt.surge.sh/og.png",
    "cnsnt-downloads": "https://cnsnt-downloads.surge.sh/og.png",
    "research-blog": "https://fnsmdehip-research.surge.sh/og.png",
    "builders-ledger": "https://builders-ledger.surge.sh/og.png",
}

DATA_URI_PATTERN = re.compile(r'data:image/svg\+xml,[^"]+')


def fix_og_images(html: str, new_url: str) -> str:
    """Replace all data:image/svg+xml occurrences with the real hosted URL."""
    return DATA_URI_PATTERN.sub(new_url, html)


# ── 2. Update dateModified in JSON-LD ────────────────────────────────────────

DATE_MOD_PATTERN = re.compile(r'"dateModified"\s*:\s*"[0-9]{4}-[0-9]{2}-[0-9]{2}"')


def update_date_modified(html: str) -> str:
    return DATE_MOD_PATTERN.sub(f'"dateModified": "{TODAY}"', html)


# ── 3. Update sitemap lastmod dates ──────────────────────────────────────────

LASTMOD_PATTERN = re.compile(r'<lastmod>[^<]+</lastmod>')


def update_sitemap_lastmod(xml: str) -> str:
    return LASTMOD_PATTERN.sub(f'<lastmod>{TODAY}</lastmod>', xml)


# ── Apply all fixes ───────────────────────────────────────────────────────────

def process_html(path: Path, og_url: str | None = None):
    html = path.read_text(encoding="utf-8")
    original = html

    if og_url:
        html = fix_og_images(html, og_url)

    html = update_date_modified(html)

    if html != original:
        path.write_text(html, encoding="utf-8")
        print(f"  UPDATED: {path.relative_to(BASE.parent)}")
    else:
        print(f"  no changes: {path.name}")


def process_sitemap(path: Path):
    if not path.exists():
        return
    xml = path.read_text(encoding="utf-8")
    updated = update_sitemap_lastmod(xml)
    if updated != xml:
        path.write_text(updated, encoding="utf-8")
        print(f"  UPDATED sitemap: {path.relative_to(BASE.parent)}")


def main():
    print("=== SEO Fix Run ===")
    print(f"Date: {TODAY}\n")

    # Fix OG images + dateModified in affected HTML files
    print("-- OG Image + dateModified fixes --")
    for dirname, og_url in OG_FIXES.items():
        html_path = BASE / dirname / "index.html"
        if html_path.exists():
            process_html(html_path, og_url)
        else:
            print(f"  SKIP (not found): {html_path}")

    # Update dateModified in all other key landing pages (no OG fix needed)
    print("\n-- dateModified updates (other sites) --")
    other_sites = ["truthscope", "androx", "cnsnt"]
    for dirname in other_sites:
        html_path = BASE / dirname / "index.html"
        if html_path.exists():
            process_html(html_path, og_url=None)

    # Update all sitemaps
    print("\n-- Sitemap lastmod updates --")
    for sitemap in BASE.rglob("sitemap.xml"):
        process_sitemap(sitemap)

    print("\nAll SEO fixes applied.")


if __name__ == "__main__":
    main()
