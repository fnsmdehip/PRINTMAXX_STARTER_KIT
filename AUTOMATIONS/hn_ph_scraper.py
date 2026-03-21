#!/usr/bin/env python3

from __future__ import annotations
"""
HackerNews + ProductHunt alpha scraper for PRINTMAXX.
Appends PENDING_REVIEW rows to LEDGER/ALPHA_STAGING.csv.
"""

import csv
import sys
import time
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

csv.field_size_limit(sys.maxsize)

import requests

# ── Paths ─────────────────────────────────────────────────────────────────────
PROJECT_ROOT = Path(__file__).resolve().parent.parent
ALPHA_CSV    = PROJECT_ROOT / "LEDGER" / "ALPHA_STAGING.csv"
LOG_PATH     = PROJECT_ROOT / "AUTOMATIONS" / "hn_ph_scraper.log"

# ── HN API base ───────────────────────────────────────────────────────────────
HN_BASE      = "https://hacker-news.firebaseio.com/v0"
HN_TOP_URL   = f"{HN_BASE}/topstories.json"
HN_SHOW_URL  = f"{HN_BASE}/showstories.json"
HN_ITEM_URL  = f"{HN_BASE}/item/{{id}}.json"

# Limit how many stories we fetch per feed to keep runtime sane
TOP_LIMIT    = 60
SHOW_LIMIT   = 40

# ProductHunt ΗΣEO-friendly public feed (no auth required)
PH_API_URL   = "https://www.producthunt.com/frontend/graphql"

# ── Category + scoring helpers ────────────────────────────────────────────────
CATEGORY_KEYWORDS = {
    "APP_FACTORY": [
        "saas", "app", "ios", "android", "mobile", "subscription", "waitlist",
        "launch", "side project", "indie", "micro-saas", "no-code", "no code",
        "low code", "pwa", "chrome extension", "browser extension",
    ],
    "TOOL_ALPHA": [
        "tool", "library", "framework", "sdk", "api", "open source", "github",
        "developer tool", "cli", "workflow", "automation", "playwright",
        "llm", "model", "embedding", "vector", "rag",
    ],
    "MONETIZATION": [
        "revenue", "mrr", "arr", "profit", "monetize", "monetisation",
        "pricing", "stripe", "gumroad", "payment", "subscription pricing",
        "i made", "we made", "earn", "selling", "sale", "$",
    ],
    "GROWTH_HACK": [
        "growth", "viral", "marketing", "seo", "acquisition", "funnel",
        "conversion", "retention", "churn", "email list", "cold email",
        "outreach", "b2b", "lead gen", "traffic",
    ],
    "CONTENT_FORMAT": [
        "content", "newsletter", "blog", "youtube", "podcast", "video",
        "twitter thread", "copywriting", "writing", "creator",
    ],
    "OUTBOUND": [
        "cold email", "cold outreach", "sales", "outbound", "prospect",
        "crm", "pipeline", "demo",
    ],
    "SEO_GEO_ASO": [
        "seo", "aso", "keyword", "backlink", "search ranking", "google",
        "bing", "serp", "organic traffic",
    ],
}

SKIP_KEYWORDS = [
    "ukraine", "russia", "war", "trump", "biden", "election", "politics",
    "climate change", "nuclear", "covid", "pandemic", "physics", "quantum",
    "mathematics", "academia", "research paper", "arxiv", "journal",
    "obituary", "died", "death",
]

ROI_MAP = {
    "HIGHEST": [
        "revenue", "mrr", "arr", "i made", "we made", "$",
        "profit", "monetize", "subscription", "saas",
    ],
    "HIGH": [
        "launch", "side project", "growth", "viral",
        "tool", "automation", "open source",
    ],
    "MEDIUM": [
        "tutorial", "guide", "tips", "how to", "learn",
        "framework", "library",
    ],
}


def log(msg: str) -> None:
    ts = datetime.now(timezone.utc).isoformat()
    line = f"[{ts}] {msg}"
    print(line)
    with open(LOG_PATH, "a") as f:
        f.write(line + "\n")


def load_existing_urls() -> set:
    """Return set of already-indexed source_urls."""
    urls = set()
    if not ALPHA_CSV.exists():
        return urls
    with open(ALPHA_CSV, newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            url = row.get("source_url", "").strip()
            if url:
                urls.add(url)
    return urls


def next_alpha_id() -> str:
    """Generate next sequential ALPHA ID based on timestamp."""
    ts = datetime.now(timezone.utc).strftime("%y%m%d%H%M%S")
    return f"ALPHA_HN_{ts}"


def classify(text: str) -> tuple[Optional[str], Optional[str]]:
    """
    Return (category, roi_potential) for a piece of text.
    Scans lowercased text against keyword maps.
    """
    lower = text.lower()

    # Skip check
    for kw in SKIP_KEYWORDS:
        if kw in lower:
            return None, None

    category = "TOOL_ALPHA"  # default
    for cat, keywords in CATEGORY_KEYWORDS.items():
        if any(kw in lower for kw in keywords):
            category = cat
            break

    roi = "MEDIUM"
    for level in ("HIGHEST", "HIGH", "MEDIUM"):
        if any(kw in lower for kw in ROI_MAP.get(level, [])):
            roi = level
            break

    return category, roi


def fetch_json(url: str, timeout: int = 10) -> dict | list | None:
    try:
        r = requests.get(url, timeout=timeout, headers={"User-Agent": "PRINTMAXX-scraper/1.0"})
        r.raise_for_status()
        return r.json()
    except Exception as e:
        log(f"WARN fetch_json failed {url}: {e}")
        return None


# ── HackerNews ────────────────────────────────────────────────────────────────

def hn_fetch_stories(feed_url: str, limit: int) -> list[dict]:
    ids = fetch_json(feed_url)
    if not ids or not isinstance(ids, list):
        return []
    results = []
    for story_id in ids[:limit]:
        item = fetch_json(HN_ITEM_URL.format(id=story_id))
        if not item or not isinstance(item, dict):
            continue
        if item.get("type") not in ("story",):
            continue
        results.append(item)
        time.sleep(0.05)   # polite
    return results


def hn_to_alpha(item: dict, feed_label: str, existing_urls: set) -> dict | None:
    title = (item.get("title") or "").strip()
    url   = (item.get("url") or f"https://news.ycombinator.com/item?id={item['id']}").strip()
    score = item.get("score", 0)
    comments = item.get("descendants", 0)
    text  = (item.get("text") or "").strip()

    if url in existing_urls:
        return None

    # Show HN marker
    is_show = title.lower().startswith("show hn")
    combined = f"{title} {text}"

    category, roi = classify(combined)
    if category is None:
        return None  # skipped

    # Boost roi for high-score Show HN posts
    if is_show and score > 100:
        roi = "HIGH" if roi == "MEDIUM" else roi

    # Boost roi for money/revenue signals
    if any(kw in combined.lower() for kw in ["$", "revenue", "mrr", "i made"]):
        roi = "HIGHEST" if roi in ("HIGH", "MEDIUM") else roi

    description = title
    if text:
        # Strip HTML tags, truncate
        clean = re.sub(r"<[^>]+>", " ", text)
        clean = re.sub(r"\s+", " ", clean).strip()
        description = f"{title}. {clean[:300]}"

    reviewer_notes = (
        f"HN score={score} comments={comments} feed={feed_label}"
    )

    ts = datetime.now(timezone.utc).isoformat()
    return {
        "alpha_id":                f"ALPHA_HN_{item['id']}",
        "source":                  f"HackerNews ({feed_label})",
        "source_url":              url,
        "category":                category,
        "tactic":                  description[:500],
        "roi_potential":           roi,
        "priority":                "SOON",
        "status":                  "PENDING_REVIEW",
        "applicable_methods":      "",
        "applicable_niches":       "",
        "synergy_score":           "",
        "cross_sell_products":     "",
        "implementation_priority": "",
        "engagement_authenticity": "AUTHENTIC",
        "earnings_verified":       "N/A",
        "extracted_method":        "",
        "compliance_notes":        "",
        "reviewer_notes":          reviewer_notes,
        "created_at":              ts,
        "ops_generated":           "FALSE",
        "quality_issues":          "",
        "date_added":              ts[:10],
    }


# ── ProductHunt ───────────────────────────────────────────────────────────────

PH_GRAPHQL_QUERY = """
query FrontPage($cursor: String) {
  posts(order: RANKING, after: $cursor, first: 40) {
    edges {
      node {
        id
        name
        tagline
        description
        url
        votesCount
        commentsCount
        createdAt
        topics {
          edges {
            node {
              name
            }
          }
        }
      }
    }
    pageInfo {
      hasNextPage
      endCursor
    }
  }
}
"""


def fetch_ph_posts() -> list[dict]:
    """Fetch ProductHunt posts via their GraphQL API (no auth for public data)."""
    headers = {
        "Content-Type":  "application/json",
        "User-Agent":    "PRINTMAXX-scraper/1.0",
        "Accept":        "application/json",
    }
    payload = {
        "query":     PH_GRAPHQL_QUERY,
        "variables": {},
    }
    try:
        r = requests.post(PH_API_URL, json=payload, headers=headers, timeout=15)
        if r.status_code != 200:
            log(f"WARN PH GraphQL returned {r.status_code}")
            return []
        data = r.json()
        edges = data.get("data", {}).get("posts", {}).get("edges", [])
        return [e["node"] for e in edges if "node" in e]
    except Exception as e:
        log(f"WARN PH fetch failed: {e}. Falling back to public RSS.")
        return fetch_ph_rss()


def fetch_ph_rss() -> list[dict]:
    """Fallback: parse ProductHunt's public RSS feed."""
    rss_url = "https://www.producthunt.com/feed"
    try:
        r = requests.get(rss_url, timeout=15, headers={"User-Agent": "PRINTMAXX-scraper/1.0"})
        r.raise_for_status()
        # Very simple RSS parse — no lxml dependency
        items = []
        entries = re.findall(r"<item>(.*?)</item>", r.text, re.DOTALL)
        for entry in entries[:40]:
            title_m       = re.search(r"<title><!\[CDATA\[(.*?)]]></title>", entry)
            link_m        = re.search(r"<link>(.*?)</link>", entry)
            desc_m        = re.search(r"<description><!\[CDATA\[(.*?)]]></description>", entry, re.DOTALL)
            title         = (title_m.group(1) if title_m else "").strip()
            link          = (link_m.group(1)  if link_m  else "").strip()
            description   = (desc_m.group(1)  if desc_m  else "").strip()
            clean_desc    = re.sub(r"<[^>]+>", " ", description)
            clean_desc    = re.sub(r"\s+", " ", clean_desc).strip()[:300]
            if title and link:
                items.append({
                    "name":          title,
                    "tagline":       clean_desc[:200],
                    "description":   clean_desc,
                    "url":           link,
                    "votesCount":    0,
                    "commentsCount": 0,
                    "createdAt":     "",
                    "topics":        {"edges": []},
                })
        return items
    except Exception as e:
        log(f"ERR PH RSS fetch failed: {e}")
        return []


def ph_to_alpha(post: dict, existing_urls: set) -> dict | None:
    name        = (post.get("name") or "").strip()
    tagline     = (post.get("tagline") or "").strip()
    description = (post.get("description") or "").strip()
    url         = (post.get("url") or "").strip()
    votes       = post.get("votesCount", 0)
    comments    = post.get("commentsCount", 0)
    topics_raw  = [
        e["node"]["name"]
        for e in post.get("topics", {}).get("edges", [])
        if "node" in e
    ]
    topics_str  = ", ".join(topics_raw)

    if not url or url in existing_urls:
        return None

    combined = f"{name} {tagline} {description} {topics_str}"
    category, roi = classify(combined)
    if category is None:
        return None

    # PH upvotes as signal
    if votes > 300:
        roi = "HIGHEST"
    elif votes > 100:
        roi = "HIGH" if roi == "MEDIUM" else roi

    tactic = f"{name}: {tagline}"
    if description:
        tactic += f". {description[:300]}"

    reviewer_notes = f"PH votes={votes} comments={comments} topics={topics_str}"

    ts = datetime.now(timezone.utc).isoformat()
    return {
        "alpha_id":                f"ALPHA_PH_{re.sub(r'[^a-z0-9]', '_', name.lower())[:40]}",
        "source":                  "ProductHunt",
        "source_url":              url,
        "category":                category,
        "tactic":                  tactic[:500],
        "roi_potential":           roi,
        "priority":                "SOON",
        "status":                  "PENDING_REVIEW",
        "applicable_methods":      "",
        "applicable_niches":       "",
        "synergy_score":           "",
        "cross_sell_products":     "",
        "implementation_priority": "",
        "engagement_authenticity": "AUTHENTIC",
        "earnings_verified":       "N/A",
        "extracted_method":        "",
        "compliance_notes":        "",
        "reviewer_notes":          reviewer_notes,
        "created_at":              ts,
        "ops_generated":           "FALSE",
        "quality_issues":          "",
        "date_added":              ts[:10],
    }


# ── CSV writer ────────────────────────────────────────────────────────────────

FIELDNAMES = [
    "alpha_id", "source", "source_url", "category", "tactic",
    "roi_potential", "priority", "status",
    "applicable_methods", "applicable_niches", "synergy_score",
    "cross_sell_products", "implementation_priority",
    "engagement_authenticity", "earnings_verified",
    "extracted_method", "compliance_notes", "reviewer_notes",
    "created_at", "ops_generated", "quality_issues", "date_added",
]


def append_rows(rows: list[dict]) -> int:
    if not rows:
        return 0
    written = 0
    with open(ALPHA_CSV, "a", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=FIELDNAMES, extrasaction="ignore")
        for row in rows:
            writer.writerow(row)
            written += 1
    return written


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    log("=== HN + PH scraper starting ===")
    existing_urls = load_existing_urls()
    log(f"Loaded {len(existing_urls)} existing URLs for dedup.")

    all_rows = []

    # 1. HN front page
    log(f"Fetching HN top stories (limit={TOP_LIMIT})...")
    top_stories = hn_fetch_stories(HN_TOP_URL, TOP_LIMIT)
    log(f"  Got {len(top_stories)} top stories.")
    for item in top_stories:
        row = hn_to_alpha(item, "top", existing_urls)
        if row:
            all_rows.append(row)
            existing_urls.add(row["source_url"])

    # 2. HN Show HN
    log(f"Fetching HN Show HN stories (limit={SHOW_LIMIT})...")
    show_stories = hn_fetch_stories(HN_SHOW_URL, SHOW_LIMIT)
    log(f"  Got {len(show_stories)} Show HN stories.")
    for item in show_stories:
        row = hn_to_alpha(item, "showhn", existing_urls)
        if row:
            all_rows.append(row)
            existing_urls.add(row["source_url"])

    # 3. ProductHunt
    log("Fetching ProductHunt posts...")
    ph_posts = fetch_ph_posts()
    log(f"  Got {len(ph_posts)} PH posts.")
    for post in ph_posts:
        row = ph_to_alpha(post, existing_urls)
        if row:
            all_rows.append(row)
            existing_urls.add(row["source_url"])

    log(f"Total qualifying rows before dedup: {len(all_rows)}")

    # Final dedup by alpha_id within batch
    seen_ids = set()
    deduped = []
    for r in all_rows:
        if r["alpha_id"] not in seen_ids:
            seen_ids.add(r["alpha_id"])
            deduped.append(r)

    written = append_rows(deduped)
    log(f"Wrote {written} new rows to {ALPHA_CSV}")
    log("=== Done ===")

    # Summary for stdout
    print(f"\nSCRAPER SUMMARY")
    print(f"  HN top stories fetched : {len(top_stories)}")
    print(f"  HN Show HN fetched     : {len(show_stories)}")
    print(f"  ProductHunt fetched    : {len(ph_posts)}")
    print(f"  New rows written       : {written}")
    print(f"  Output: {ALPHA_CSV}")

    # Breakdown by category
    from collections import Counter
    cats = Counter(r["category"] for r in deduped)
    rois = Counter(r["roi_potential"] for r in deduped)
    print(f"\n  By category: {dict(cats)}")
    print(f"  By ROI:      {dict(rois)}")

    return written


if __name__ == "__main__":
    main()
