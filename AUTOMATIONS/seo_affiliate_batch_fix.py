#!/usr/bin/env python3
"""
Batch SEO fix for affiliate pages:
  1. Replace data:image/svg+xml OG images with Pollinations.ai URLs
  2. Add missing og:image tags
  3. Add Article JSON-LD to pages missing structured data
  4. Update dateModified / datePublished to today
"""

import re
import os
import json
from pathlib import Path
from datetime import date
from urllib.parse import quote

BASE = Path("/Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt/LANDING/affiliate-pages")
TODAY = date.today().isoformat()

DATA_URI_PATTERN = re.compile(r'data:image/svg\+xml,[^"]+')
TITLE_PATTERN = re.compile(r'<title>([^<]+)</title>', re.IGNORECASE)
DESC_PATTERN = re.compile(r'<meta[^>]+name=["\']description["\'][^>]+content=["\']([^"\']+)["\']', re.IGNORECASE)
OG_IMAGE_PATTERN = re.compile(r'<meta\s+property=["\']og:image["\'][^>]+>', re.IGNORECASE)
CANONICAL_PATTERN = re.compile(r'<link[^>]+rel=["\']canonical["\'][^>]+href=["\']([^"\']+)["\']', re.IGNORECASE)
LASTMOD_PATTERN = re.compile(r'"dateModified"\s*:\s*"[0-9]{4}-[0-9]{2}-[0-9]{2}"')
DATEPUB_PATTERN = re.compile(r'"datePublished"\s*:\s*"[0-9]{4}-[0-9]{2}-[0-9]{2}"')
LDTYPE_PATTERN = re.compile(r'"@type"\s*:\s*"(Article|BlogPosting|NewsArticle)"')


def pollinations_url(title: str, seed: int = 42) -> str:
    """Generate a Pollinations.ai OG image URL from a title string."""
    # Clean title for prompt: remove year, symbols, make descriptive
    prompt = title.strip()
    prompt = re.sub(r'\s*\([^)]+\)', '', prompt)  # Remove parenthetical
    prompt = re.sub(r'\s*-\s*.*$', '', prompt)     # Remove everything after dash
    prompt = prompt.strip()
    prompt = f"{prompt}, professional comparison guide, dark blue minimal clean"
    encoded = quote(prompt[:200])
    return f"https://image.pollinations.ai/prompt/{encoded}?width=1200&height=630&nologo=true&seed={seed}"


def extract_title(html: str) -> str:
    m = TITLE_PATTERN.search(html)
    return m.group(1).strip() if m else "Best Comparison Guide 2026"


def extract_description(html: str) -> str:
    m = DESC_PATTERN.search(html)
    return m.group(1).strip() if m else ""


def extract_canonical(html: str) -> str:
    m = CANONICAL_PATTERN.search(html)
    return m.group(1).strip() if m else ""


def has_json_ld(html: str) -> bool:
    return 'application/ld+json' in html


def has_og_image(html: str) -> bool:
    return bool(OG_IMAGE_PATTERN.search(html))


def fix_data_uri_og(html: str, title: str, seed: int) -> str:
    """Replace data:URI in og:image and twitter:image with real Pollinations URL."""
    new_url = pollinations_url(title, seed)
    return DATA_URI_PATTERN.sub(new_url, html)


def add_og_image_tags(html: str, title: str, canonical: str, seed: int) -> str:
    """Insert og:image and twitter:image tags after the last og: meta tag."""
    new_url = pollinations_url(title, seed)
    og_tags = f"""<meta property="og:image" content="{new_url}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:image" content="{new_url}">"""

    # Insert after og:url or og:description, whichever is last in head
    og_url_match = re.search(r'(<meta[^>]+og:url[^>]+>)', html, re.IGNORECASE)
    og_desc_match = re.search(r'(<meta[^>]+og:description[^>]+>)', html, re.IGNORECASE)
    insert_after = og_url_match or og_desc_match
    if insert_after:
        pos = insert_after.end()
        return html[:pos] + "\n" + og_tags + html[pos:]
    # Fallback: insert before </head>
    return html.replace('</head>', og_tags + '\n</head>', 1)


def build_article_jsonld(title: str, description: str, canonical: str) -> str:
    """Build a minimal Article JSON-LD block."""
    data = {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": title[:110],
        "description": description[:300] if description else title,
        "url": canonical,
        "datePublished": "2026-03-01",
        "dateModified": TODAY,
        "author": {"@type": "Organization", "name": "PRINTMAXX"},
        "publisher": {"@type": "Organization", "name": "PRINTMAXX", "url": "https://printmaxx.surge.sh/"}
    }
    return f'<script type="application/ld+json">\n{json.dumps(data, indent=2)}\n</script>'


def add_json_ld(html: str, title: str, description: str, canonical: str) -> str:
    """Insert Article JSON-LD before </head>."""
    block = build_article_jsonld(title, description, canonical)
    return html.replace('</head>', block + '\n</head>', 1)


def update_date_modified(html: str) -> str:
    html = LASTMOD_PATTERN.sub(f'"dateModified": "{TODAY}"', html)
    return html


def process_file(html_path: Path, index: int) -> dict:
    html = html_path.read_text(encoding='utf-8')
    original = html
    changes = []
    seed = (index * 7 + 13) % 97 + 1  # Deterministic seed per page

    title = extract_title(html)
    description = extract_description(html)
    canonical = extract_canonical(html)

    # Fix data:URI OG images
    if DATA_URI_PATTERN.search(html):
        html = fix_data_uri_og(html, title, seed)
        changes.append("fix_data_uri_og")

    # Add OG image if missing entirely
    if not has_og_image(html):
        html = add_og_image_tags(html, title, canonical, seed)
        changes.append("add_og_image")

    # Add JSON-LD if missing
    if not has_json_ld(html):
        html = add_json_ld(html, title, description, canonical)
        changes.append("add_json_ld")

    # Update dateModified
    updated = update_date_modified(html)
    if updated != html:
        html = updated
        changes.append("update_date_modified")

    if html != original:
        html_path.write_text(html, encoding='utf-8')

    return {"path": html_path.parent.name, "changes": changes}


def main():
    print("=== Affiliate Pages Batch SEO Fix ===")
    print(f"Date: {TODAY}\n")

    # Get all affiliate page index.html files (including seo-articles subdirs)
    html_files = sorted(BASE.rglob("index.html"))
    print(f"Found {len(html_files)} pages to process\n")

    stats = {"fix_data_uri_og": 0, "add_og_image": 0, "add_json_ld": 0, "update_date_modified": 0, "unchanged": 0}

    for i, path in enumerate(html_files):
        result = process_file(path, i)
        if result["changes"]:
            print(f"  UPDATED [{', '.join(result['changes'])}]: {result['path']}")
            for c in result["changes"]:
                stats[c] = stats.get(c, 0) + 1
        else:
            stats["unchanged"] += 1

    print(f"\n=== Summary ===")
    print(f"data:URI OG images fixed:   {stats['fix_data_uri_og']}")
    print(f"OG images added:            {stats['add_og_image']}")
    print(f"JSON-LD added:              {stats['add_json_ld']}")
    print(f"dateModified updated:       {stats['update_date_modified']}")
    print(f"Unchanged:                  {stats['unchanged']}")
    print(f"Total processed:            {len(html_files)}")


if __name__ == "__main__":
    main()
