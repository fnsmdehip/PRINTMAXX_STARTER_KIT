#!/usr/bin/env python3
"""
PRINTMAXX Automation: RamadanTracker Africa Growth

Mine r/digitalnomad and r/islam subreddits for Africa-specific Ramadan/prayer
pain points, auto-generate targeted content for Muslim digital nomads in Africa,
surface top African cities missing from Hilal app coverage, and post
geo-targeted content driving app installs.

TYPE: scraper|poster
METHOD CONTEXT: [RamadanTracker] Reddit opportunity: DN experience around whole Africa
"""

import argparse
import base64
import csv
import json
import logging
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

# ---------------------------------------------------------------------------
# Bootstrap: import from _common or define local fallbacks
# ---------------------------------------------------------------------------
try:
    from _common import PROJECT, safe_path, recall_skills_for_task, capture_skill_from_result
except ImportError:
    PROJECT = Path(__file__).resolve().parent.parent

    def safe_path(target):
        """Validate that target resolves within PROJECT."""
        resolved = Path(target).resolve()
        try:
            resolved.relative_to(PROJECT)
        except ValueError:
            raise ValueError(
                f"Path escape detected: {resolved} is outside PROJECT root {PROJECT}"
            )
        return resolved

    def recall_skills_for_task(task_name: str) -> dict:
        return {}

    def capture_skill_from_result(task_name: str, result) -> None:
        pass

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
SCRIPT_NAME = "ramadan_tracker_africa_growth"
LOG_FILE = safe_path(PROJECT / "AUTOMATIONS" / "logs" / f"{SCRIPT_NAME}.log")
DATA_DIR = safe_path(PROJECT / "AUTOMATIONS" / "data" / SCRIPT_NAME)
OUTPUT_DIR = safe_path(PROJECT / "AUTOMATIONS" / "output" / SCRIPT_NAME)

SUBREDDITS = ["digitalnomad", "islam"]

SEARCH_QUERIES = [
    "africa ramadan",
    "africa prayer time",
    "muslim digital nomad africa",
    "hilal africa",
    "ramadan travel africa",
    "prayer app africa",
    "eid africa",
    "mosque africa nomad",
    "africa fasting",
    "halal africa nomad",
    "africa prayer schedule",
    "ramadan remote work",
]

AFRICAN_CITIES = [
    {"city": "Lagos",         "country": "Nigeria",       "lat":  6.52,  "lon":   3.38},
    {"city": "Nairobi",       "country": "Kenya",         "lat": -1.29,  "lon":  36.82},
    {"city": "Accra",         "country": "Ghana",         "lat":  5.56,  "lon":  -0.20},
    {"city": "Dar es Salaam", "country": "Tanzania",      "lat": -6.79,  "lon":  39.21},
    {"city": "Addis Ababa",   "country": "Ethiopia",      "lat":  9.03,  "lon":  38.74},
    {"city": "Casablanca",    "country": "Morocco",       "lat": 33.59,  "lon":  -7.62},
    {"city": "Cairo",         "country": "Egypt",         "lat": 30.06,  "lon":  31.25},
    {"city": "Dakar",         "country": "Senegal",       "lat": 14.72,  "lon": -17.47},
    {"city": "Kampala",       "country": "Uganda",        "lat":  0.32,  "lon":  32.58},
    {"city": "Khartoum",      "country": "Sudan",         "lat": 15.55,  "lon":  32.53},
    {"city": "Abidjan",       "country": "Ivory Coast",   "lat":  5.35,  "lon":  -4.00},
    {"city": "Tunis",         "country": "Tunisia",       "lat": 36.82,  "lon":  10.17},
    {"city": "Algiers",       "country": "Algeria",       "lat": 36.74,  "lon":   3.06},
    {"city": "Bamako",        "country": "Mali",          "lat": 12.65,  "lon":  -8.00},
    {"city": "Niamey",        "country": "Niger",         "lat": 13.51,  "lon":   2.11},
    {"city": "Conakry",       "country": "Guinea",        "lat":  9.54,  "lon": -13.68},
    {"city": "Mombasa",       "country": "Kenya",         "lat": -4.05,  "lon":  39.67},
    {"city": "Zanzibar",      "country": "Tanzania",      "lat": -6.16,  "lon":  39.20},
    {"city": "Marrakech",     "country": "Morocco",       "lat": 31.63,  "lon":  -8.00},
    {"city": "Rabat",         "country": "Morocco",       "lat": 33.99,  "lon":  -6.85},
    {"city": "Tripoli",       "country": "Libya",         "lat": 32.89,  "lon":  13.18},
    {"city": "Mogadishu",     "country": "Somalia",       "lat":  2.05,  "lon":  45.34},
    {"city": "Maputo",        "country": "Mozambique",    "lat": -25.97, "lon":  32.59},
    {"city": "Djibouti City", "country": "Djibouti",      "lat": 11.59,  "lon":  43.14},
    {"city": "Nouakchott",    "country": "Mauritania",    "lat": 18.08,  "lon": -15.97},
]

PAIN_POINT_KEYWORDS = [
    "prayer", "ramadan", "halal", "mosque", "fasting", "suhoor", "iftar",
    "qibla", "salah", "eid", "hijab", "muslim", "islamic", "prayer time",
    "athan", "adhan", "jummah", "friday prayer", "wifi mosque",
    "coworking halal", "prayer room", "wudu", "ablution", "masjid",
]

AFRICA_KEYWORDS = [
    "africa", "lagos", "nairobi", "accra", "cairo", "dakar", "kampala",
    "casablanca", "morocco", "kenya", "nigeria", "ghana", "tanzania",
    "ethiopia", "senegal", "ivory coast", "mali", "niger", "sudan",
    "algeria", "tunisia", "egypt", "uganda", "mombasa", "zanzibar",
    "marrakech", "rabat", "bamako", "niamey", "conakry", "djibouti",
    "mogadishu", "tripoli", "maputo", "khartoum", "abidjan",
]

REDDIT_USER_AGENT = "PRINTMAXX:RamadanTrackerBot:v1.0 (automated research tool)"
REDDIT_BASE = "https://www.reddit.com"
REDDIT_OAUTH_BASE = "https://oauth.reddit.com"

POST_TEMPLATES = [
    {
        "title": "Muslim DNs in {city}, {country} — how do you manage prayer times while coworking? [Genuine question]",
        "body": (
            "As a Muslim digital nomad spending time across Africa, I've been thinking about "
            "how we handle Ramadan and daily prayers while working remotely.\n\n"
            "**Pain points I've personally run into in {city}:**\n"
            "- Finding coworking spaces with a prayer room or nearby mosque\n"
            "- Reliable prayer time apps that actually cover {city} accurately\n"
            "- Locating halal food near workspaces during Ramadan\n\n"
            "I've been using the **Hilal app** for moon sighting news and prayer scheduling — "
            "it's been a game changer for DNs across Africa. Anyone else using it in {city} "
            "or nearby?\n\n"
            "Would love to hear from other Muslim DNs on the continent. Drop your city below!\n\n"
            "*[Hilal app available on iOS/Android — built for African Muslim communities]*"
        ),
        "subreddit": "digitalnomad",
    },
    {
        "title": "Ramadan 2026 as a digital nomad in Africa — resource thread for Muslim DNs",
        "body": (
            "Ramadan Mubarak to all Muslim DNs!\n\n"
            "Sharing resources specifically for those of us working remotely across Africa:\n\n"
            "**Prayer time accuracy:**\n"
            "Many popular prayer apps don't have precise coverage for African cities outside "
            "the major metros. The **Hilal app** has been the most reliable for cities like:\n"
            "{city_list}\n\n"
            "**What's working for me this Ramadan:**\n"
            "- Blocking prayer times in my calendar before my workday\n"
            "- Finding coworking spaces within walking distance of a mosque\n"
            "- Using Hilal app for local moon sighting announcements\n\n"
            "Anyone else have tips for Muslim DNs navigating Ramadan in Africa?"
        ),
        "subreddit": "digitalnomad",
    },
    {
        "title": "[{country}] Guide for Muslim digital nomads — prayer infrastructure & Ramadan tips",
        "body": (
            "After spending time across {country} as a Muslim DN, here's my honest take:\n\n"
            "**{city} specifically:**\n"
            "- Mosque density: solid options in the main areas\n"
            "- Prayer app coverage: Hilal app works well here and sources local data\n"
            "- Halal food: strong scene, especially around Ramadan\n"
            "- Coworking spaces with prayer rooms: growing but still limited\n\n"
            "For anyone planning Ramadan in {country}, download **Hilal** before you arrive — "
            "it's one of the few apps with accurate African city data and local moon "
            "sighting announcements.\n\n"
            "Happy to answer questions about the Muslim DN experience in {country}!"
        ),
        "subreddit": "digitalnomad",
    },
]

COMMENT_TEMPLATES = [
    (
        "This is such a real struggle! I've been using the Hilal app for prayer times across "
        "Africa and it's the most accurate I've found — especially in cities like {city} "
        "where other apps tend to be off. Might be worth checking out if you haven't already."
    ),
    (
        "Ramadan Mubarak! For prayer times specifically in {city}, the Hilal app has worked "
        "best for me. It sources local moon sighting data which really matters across "
        "different African regions. Free download too."
    ),
    (
        "As a Muslim DN who's worked in {city_list}, the prayer time accuracy issue is real. "
        "Most apps use generic calculation methods that don't account for African geography "
        "or local madhab preferences. The Hilal app resolved this for me."
    ),
]

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------

def setup_logging() -> None:
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler(str(LOG_FILE), mode="a", encoding="utf-8"),
            logging.StreamHandler(sys.stdout),
        ],
    )


log = logging.getLogger(SCRIPT_NAME)

# ---------------------------------------------------------------------------
# Utilities
# ---------------------------------------------------------------------------

def ensure_dirs() -> None:
    for d in [DATA_DIR, OUTPUT_DIR]:
        d.mkdir(parents=True, exist_ok=True)


def reddit_get(endpoint: str, params: dict = None) -> dict:
    """GET from Reddit public JSON API."""
    url = f"{REDDIT_BASE}{endpoint}.json"
    if params:
        url += "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent": REDDIT_USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        log.warning("HTTP %s for %s", exc.code, url)
        return {}
    except urllib.error.URLError as exc:
        log.warning("URL error for %s: %s", url, exc.reason)
        return {}
    except Exception as exc:
        log.warning("Unexpected error fetching %s: %s", url, exc)
        return {}


def load_reddit_config() -> dict:
    """Load Reddit OAuth credentials from config file."""
    config_path = safe_path(
        PROJECT / "AUTOMATIONS" / "config" / "reddit_credentials.json"
    )
    if config_path.exists():
        try:
            with open(config_path, "r", encoding="utf-8") as fh:
                return json.load(fh)
        except Exception as exc:
            log.warning("Could not load Reddit config: %s", exc)
    return {}


def get_reddit_token(config: dict) -> str:
    """Obtain Reddit OAuth bearer token via script-app password flow."""
    if not config.get("client_id") or not config.get("client_secret"):
        log.warning("Reddit credentials missing — posting disabled")
        return ""
    data = urllib.parse.urlencode(
        {
            "grant_type": "password",
            "username": config.get("username", ""),
            "password": config.get("password", ""),
        }
    ).encode()
    creds = f"{config['client_id']}:{config['client_secret']}".encode()
    auth_header = "Basic " + base64.b64encode(creds).decode()
    req = urllib.request.Request(
        "https://www.reddit.com/api/v1/access_token",
        data=data,
        headers={
            "User-Agent": REDDIT_USER_AGENT,
            "Authorization": auth_header,
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            result = json.loads(resp.read().decode("utf-8"))
            return result.get("access_token", "")
    except Exception as exc:
        log.warning("Failed to obtain Reddit token: %s", exc)
        return ""


def reddit_oauth_post(endpoint: str, data: dict, token: str) -> dict:
    """POST to Reddit OAuth API."""
    url = f"{REDDIT_OAUTH_BASE}{endpoint}"
    encoded = urllib.parse.urlencode(data).encode()
    req = urllib.request.Request(
        url,
        data=encoded,
        headers={
            "User-Agent": REDDIT_USER_AGENT,
            "Authorization": f"bearer {token}",
            "Content-Type": "application/x-www-form-urlencoded",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except Exception as exc:
        log.warning("Reddit POST failed for %s: %s", endpoint, exc)
        return {}


def is_africa_relevant(text: str) -> bool:
    lower = text.lower()
    return any(kw in lower for kw in AFRICA_KEYWORDS)


def is_prayer_relevant(text: str) -> bool:
    lower = text.lower()
    return any(kw in lower for kw in PAIN_POINT_KEYWORDS)


def relevance_score(title: str, body: str) -> int:
    combined = f"{title} {body}".lower()
    score = sum(2 for kw in AFRICA_KEYWORDS if kw in combined)
    score += sum(1 for kw in PAIN_POINT_KEYWORDS if kw in combined)
    return score


def write_json(path: Path, data) -> None:
    resolved = safe_path(path)
    try:
        with open(resolved, "w", encoding="utf-8") as fh:
            json.dump(data, fh, indent=2, ensure_ascii=False)
        log.info("Saved JSON: %s", resolved)
    except Exception as exc:
        log.error("JSON write failed for %s: %s", resolved, exc)


def write_csv(path: Path, rows: list, fieldnames: list) -> None:
    resolved = safe_path(path)
    try:
        with open(resolved, "w", newline="", encoding="utf-8") as fh:
            writer = csv.DictWriter(fh, fieldnames=fieldnames, extrasaction="ignore")
            writer.writeheader()
            writer.writerows(rows)
        log.info("Saved CSV: %s", resolved)
    except Exception as exc:
        log.error("CSV write failed for %s: %s", resolved, exc)

# ---------------------------------------------------------------------------
# Phase 1 — Scrape
# ---------------------------------------------------------------------------

def scrape_subreddit(subreddit: str, query: str, limit: int = 25) -> list:
    """Search a subreddit and return Africa/prayer-relevant posts."""
    params = {
        "q": query,
        "restrict_sr": "1",
        "sort": "new",
        "limit": limit,
        "t": "year",
    }
    data = reddit_get(f"/r/{subreddit}/search", params)
    posts = []
    for child in data.get("data", {}).get("children", []):
        p = child.get("data", {})
        title = p.get("title", "")
        body = p.get("selftext", "")
        combined = f"{title} {body}"
        if not (is_africa_relevant(combined) or is_prayer_relevant(combined)):
            continue
        posts.append(
            {
                "id": p.get("id", ""),
                "subreddit": subreddit,
                "title": title,
                "body": body[:500],
                "url": p.get("url", ""),
                "permalink": f"https://reddit.com{p.get('permalink', '')}",
                "upvotes": p.get("score", 0),
                "num_comments": p.get("num_comments", 0),
                "created_utc": p.get("created_utc", 0),
                "relevance": relevance_score(title, body),
                "query": query,
            }
        )
    return posts


def run_scrape(dry_run: bool = False) -> list:
    """Scrape both subreddits across all queries, dedup by post ID."""
    log.info("=== SCRAPE PHASE START ===")
    all_posts = []
    seen_ids: set = set()

    for subreddit in SUBREDDITS:
        for query in SEARCH_QUERIES:
            log.info("Searching r/%s: '%s'", subreddit, query)
            if dry_run:
                log.info("  [DRY RUN] Skipping actual request")
                continue
            try:
                posts = scrape_subreddit(subreddit, query)
                new = [p for p in posts if p["id"] not in seen_ids]
                for p in new:
                    seen_ids.add(p["id"])
                all_posts.extend(new)
                log.info("  +%d relevant posts (%d total unique)", len(new), len(all_posts))
                time.sleep(2)
            except Exception as exc:
                log.error("Scrape error r/%s '%s': %s", subreddit, query, exc)

    log.info("=== SCRAPE COMPLETE: %d unique posts ===", len(all_posts))

    if all_posts and not dry_run:
        stamp = datetime.now().strftime("%Y%m%d")
        write_csv(
            OUTPUT_DIR / f"scraped_posts_{stamp}.csv",
            all_posts,
            ["id", "subreddit", "title", "upvotes", "num_comments",
             "relevance", "query", "permalink", "created_utc"],
        )
        write_json(OUTPUT_DIR / f"scraped_posts_{stamp}.json", all_posts)

    return all_posts

# ---------------------------------------------------------------------------
# Phase 2 — Pain Point Analysis
# ---------------------------------------------------------------------------

CATEGORY_KEYWORDS = {
    "prayer_accuracy":   ["prayer time", "athan", "adhan", "calculation", "accurate", "off by", "wrong time", "inaccurate"],
    "halal_food":        ["halal", "food", "restaurant", "eat", "iftar", "suhoor", "meal", "hungry"],
    "prayer_space":      ["mosque", "prayer room", "musalla", "masjid", "coworking", "wudu", "space"],
    "community":         ["community", "muslim", "brothers", "sisters", "ummah", "jummah", "friday prayer"],
    "app_coverage":      ["app", "coverage", "city", "location", "hilal", "not available", "missing", "doesn't cover"],
    "ramadan_logistics": ["ramadan", "fasting", "schedule", "productivity", "remote work", "energy", "timing"],
}


def analyze_pain_points(posts: list) -> dict:
    """Categorize posts by pain type and surface the top hits."""
    buckets: dict = {k: [] for k in CATEGORY_KEYWORDS}

    for post in posts:
        text = f"{post['title']} {post['body']}".lower()
        for category, keywords in CATEGORY_KEYWORDS.items():
            if any(kw in text for kw in keywords):
                buckets[category].append(
                    {
                        "id": post["id"],
                        "title": post["title"],
                        "relevance": post["relevance"],
                        "permalink": post["permalink"],
                    }
                )

    summary = {
        "total_posts_analyzed": len(posts),
        "category_counts": {k: len(v) for k, v in buckets.items()},
        "top_posts": sorted(posts, key=lambda x: x["relevance"], reverse=True)[:10],
        "detail": buckets,
    }

    stamp = datetime.now().strftime("%Y%m%d")
    write_json(OUTPUT_DIR / f"pain_point_analysis_{stamp}.json", summary)

    for cat, count in summary["category_counts"].items():
        log.info("  Pain bucket '%s': %d posts", cat, count)

    return summary

# ---------------------------------------------------------------------------
# Phase 3 — Hilal Coverage Gap Analysis
# ---------------------------------------------------------------------------

def check_hilal_coverage() -> list:
    """
    Probe Hilal app's public city search for each African city.
    Marks cities as covered/uncovered to surface gaps.
    """
    log.info("=== HILAL COVERAGE CHECK ===")
    results = []

    for city_info in AFRICAN_CITIES:
        city = city_info["city"]
        country = city_info["country"]
        row = {
            "city": city,
            "country": country,
            "lat": city_info["lat"],
            "lon": city_info["lon"],
            "hilal_covered": False,
            "gap_priority": "unknown",
        }
        params = urllib.parse.urlencode({"q": city, "country": country})
        url = f"https://www.hilalapp.com/api/v1/cities?{params}"
        req = urllib.request.Request(url, headers={"User-Agent": REDDIT_USER_AGENT})
        try:
            with urllib.request.urlopen(req, timeout=10) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                city_list = data.get("cities", data.get("results", []))
                matched = any(city.lower() in str(c).lower() for c in city_list)
                row["hilal_covered"] = matched
                row["gap_priority"] = "covered" if matched else "high"
        except urllib.error.HTTPError as exc:
            log.debug("Hilal API HTTP %s for %s", exc.code, city)
            row["gap_priority"] = "check_manually"
        except Exception:
            row["gap_priority"] = "check_manually"

        results.append(row)
        log.info(
            "  %s, %s → %s",
            city,
            country,
            "covered" if row["hilal_covered"] else row["gap_priority"],
        )
        time.sleep(1)

    # Uncovered first
    results.sort(key=lambda x: (x["hilal_covered"], x["gap_priority"] == "covered"))

    stamp = datetime.now().strftime("%Y%m%d")
    write_json(OUTPUT_DIR / f"hilal_coverage_gaps_{stamp}.json", results)
    write_csv(
        OUTPUT_DIR / f"hilal_coverage_gaps_{stamp}.csv",
        results,
        ["city", "country", "lat", "lon", "hilal_covered", "gap_priority"],
    )

    uncovered = [r for r in results if not r["hilal_covered"]]
    log.info(
        "Coverage summary: %d/%d cities lack Hilal coverage",
        len(uncovered),
        len(results),
    )
    return results

# ---------------------------------------------------------------------------
# Phase 4 — Content Generation
# ---------------------------------------------------------------------------

def generate_content(pain_analysis: dict, coverage_gaps: list, dry_run: bool = False) -> list:
    """Build geo-targeted Reddit posts and reply comments."""
    log.info("=== CONTENT GENERATION PHASE ===")
    generated = []

    gap_cities = [c for c in coverage_gaps if not c.get("hilal_covered", True)][:5]
    gap_city_labels = [f"{c['city']}, {c['country']}" for c in gap_cities]
    city_list_str = (
        "\n".join(f"  - {label}" for label in gap_city_labels)
        if gap_city_labels
        else "  - Lagos, Nigeria\n  - Nairobi, Kenya\n  - Accra, Ghana"
    )

    target_cities = gap_cities if gap_cities else AFRICAN_CITIES[:4]

    for city_info in target_cities:
        city = city_info["city"]
        country = city_info["country"]
        for template in POST_TEMPLATES:
            generated.append(
                {
                    "type": "post",
                    "city": city,
                    "country": country,
                    "title": template["title"].format(city=city, country=country),
                    "body": template["body"].format(
                        city=city,
                        country=country,
                        city_list=city_list_str,
                    ),
                    "target_subreddit": template["subreddit"],
                    "generated_at": datetime.now(timezone.utc).isoformat(),
                }
            )

    top_posts = pain_analysis.get("top_posts", [])[:5]
    for post in top_posts:
        template = COMMENT_TEMPLATES[0]
        generated.append(
            {
                "type": "comment",
                "target_post_id": post.get("id", ""),
                "target_permalink": post.get("permalink", ""),
                "body": template.format(
                    city=gap_city_labels[0] if gap_city_labels else "Nairobi, Kenya",
                    city_list=(
                        ", ".join(gap_city_labels[:3])
                        if gap_city_labels
                        else "Lagos, Nairobi, Accra"
                    ),
                ),
                "generated_at": datetime.now(timezone.utc).isoformat(),
            }
        )

    stamp = datetime.now().strftime("%Y%m%d")
    write_json(OUTPUT_DIR / f"generated_content_{stamp}.json", generated)
    log.info("Generated %d content items", len(generated))

    if dry_run:
        log.info("[DRY RUN] Sample content (first 3 items):")
        for item in generated[:3]:
            preview = item.get("title") or item["body"][:80]
            log.info("  [%s] %s", item["type"], preview)

    return generated

# ---------------------------------------------------------------------------
# Phase 5 — Posting
# ---------------------------------------------------------------------------

def post_content(generated: list, dry_run: bool = False) -> dict:
    """Submit generated posts and comments to Reddit."""
    log.info("=== POSTING PHASE ===")
    results: dict = {"posted": [], "failed": [], "skipped": []}

    if dry_run:
        for item in generated:
            preview = item.get("title") or item["body"][:60]
            log.info("[DRY RUN] Would %s: %s…", item["type"], preview)
            results["skipped"].append(item)
        return results

    config = load_reddit_config()
    token = get_reddit_token(config) if config else ""
    if not token:
        log.warning("No Reddit token — skipping all posts")
        results["skipped"] = generated
        return results

    post_limit = int(config.get("daily_post_limit", 3))
    comment_limit = int(config.get("daily_comment_limit", 5))
    posts_made = 0
    comments_made = 0

    for item in generated:
        try:
            if item["type"] == "post" and posts_made < post_limit:
                resp = reddit_oauth_post(
                    "/api/submit",
                    {
                        "sr": item["target_subreddit"],
                        "kind": "self",
                        "title": item["title"],
                        "text": item["body"],
                    },
                    token,
                )
                if resp.get("success") or resp.get("json", {}).get("data", {}).get("name"):
                    log.info("Posted: %s", item["title"][:70])
                    results["posted"].append(item)
                    posts_made += 1
                else:
                    log.warning("Post rejected: %s", resp)
                    results["failed"].append(item)
                time.sleep(6)

            elif item["type"] == "comment" and comments_made < comment_limit:
                post_id = item.get("target_post_id")
                if not post_id:
                    results["skipped"].append(item)
                    continue
                resp = reddit_oauth_post(
                    "/api/comment",
                    {"thing_id": f"t3_{post_id}", "text": item["body"]},
                    token,
                )
                if resp.get("success") or resp.get("json", {}).get("data"):
                    log.info("Commented on t3_%s", post_id)
                    results["posted"].append(item)
                    comments_made += 1
                else:
                    log.warning("Comment rejected: %s", resp)
                    results["failed"].append(item)
                time.sleep(6)

            else:
                results["skipped"].append(item)

        except Exception as exc:
            log.error("Post/comment error: %s", exc)
            results["failed"].append(item)

    log.info(
        "Posting done — posted: %d | failed: %d | skipped: %d",
        len(results["posted"]),
        len(results["failed"]),
        len(results["skipped"]),
    )

    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    write_json(OUTPUT_DIR / f"posting_results_{stamp}.json", results)
    return results

# ---------------------------------------------------------------------------
# Status Report
# ---------------------------------------------------------------------------

def run_status() -> None:
    sep = "=" * 62
    print(f"\n{sep}")
    print("  PRINTMAXX — RamadanTracker Africa Growth  STATUS")
    print(sep)
    print(f"  Project root : {PROJECT}")
    print(f"  Log file     : {LOG_FILE}")
    print(f"  Output dir   : {OUTPUT_DIR}")
    print()

    if OUTPUT_DIR.exists():
        files = sorted(OUTPUT_DIR.glob("*"), key=lambda f: f.stat().st_mtime, reverse=True)
        files = [f for f in files if f.is_file()][:12]
        if files:
            print("  Recent output files:")
            for fpath in files:
                mtime = datetime.fromtimestamp(fpath.stat().st_mtime).strftime("%Y-%m-%d %H:%M")
                size = fpath.stat().st_size
                print(f"    {mtime}  {fpath.name:<52s}  {size:>8,} B")
        else:
            print("  No output files yet.")
    else:
        print("  Output directory not yet created.")

    print()
    if LOG_FILE.exists():
        print("  Last 5 log entries:")
        try:
            result = subprocess.run(
                ["tail", "-5", str(LOG_FILE)],
                capture_output=True,
                text=True,
                timeout=5,
            )
            for line in result.stdout.strip().splitlines():
                print(f"    {line}")
        except Exception as exc:
            print(f"    (could not read log: {exc})")
    print()

# ---------------------------------------------------------------------------
# Entry Point
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        prog="ramadan_tracker_africa_growth",
        description=(
            "PRINTMAXX: RamadanTracker Africa Growth — "
            "Reddit scraper and content poster for Muslim DNs in Africa."
        ),
    )
    parser.add_argument(
        "--run",
        action="store_true",
        help="Execute full pipeline: scrape → analyze → coverage → generate → post",
    )
    parser.add_argument(
        "--status",
        action="store_true",
        help="Show status of recent runs and output files",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Run pipeline end-to-end without posting; log all planned actions",
    )
    args = parser.parse_args()

    if not (args.run or args.status or args.dry_run):
        parser.print_help()
        sys.exit(0)

    setup_logging()
    ensure_dirs()

    if args.status:
        run_status()
        sys.exit(0)

    dry_run = args.dry_run
    if dry_run:
        log.info("=== DRY RUN MODE — no posts will be submitted ===")

    log.info("Starting %s | dry_run=%s", SCRIPT_NAME, dry_run)

    skills = recall_skills_for_task(SCRIPT_NAME)
    if skills:
        log.info("Recalled skills: %s", list(skills.keys()))

    try:
        # 1. Scrape subreddits
        posts = run_scrape(dry_run=dry_run)

        # 2. Analyse pain points
        pain_analysis = (
            analyze_pain_points(posts)
            if posts
            else {
                "total_posts_analyzed": 0,
                "category_counts": {},
                "top_posts": [],
                "detail": {},
            }
        )

        # 3. Hilal coverage gap check
        coverage_gaps = check_hilal_coverage()

        # 4. Generate targeted content
        generated = generate_content(pain_analysis, coverage_gaps, dry_run=dry_run)

        # 5. Post content
        post_results = post_content(generated, dry_run=dry_run)

        # Capture learnings for future sessions
        summary = {
            "posts_scraped": len(posts),
            "cities_checked": len(coverage_gaps),
            "uncovered_cities": sum(1 for c in coverage_gaps if not c.get("hilal_covered")),
            "content_generated": len(generated),
            "content_posted": len(post_results.get("posted", [])),
            "run_at": datetime.now(timezone.utc).isoformat(),
            "dry_run": dry_run,
        }
        capture_skill_from_result(SCRIPT_NAME, summary)
        log.info("Run complete: %s", summary)

    except KeyboardInterrupt:
        log.info("Interrupted — exiting cleanly")
        sys.exit(0)
    except Exception as exc:
        log.error("Fatal error: %s", exc, exc_info=True)
        sys.exit(1)

    sys.exit(0)


if __name__ == "__main__":
    main()