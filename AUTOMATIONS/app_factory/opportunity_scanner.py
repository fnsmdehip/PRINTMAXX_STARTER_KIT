#!/usr/bin/env python3
"""App Factory Opportunity Scanner.

Scans multiple sources for app opportunities, scores them, and outputs a ranked
CSV for the app factory pipeline to consume.

Sources:
  1. Apple App Store RSS feeds (top charts, trending)
  2. Reddit pain-point scraping (JSON API, no auth)
  3. App Store search suggestions (keyword gap analysis)
  4. Existing alpha pipeline (ALPHA_STAGING.csv)

Usage:
  python3 AUTOMATIONS/app_factory/opportunity_scanner.py --scan
  python3 AUTOMATIONS/app_factory/opportunity_scanner.py --scan --dry-run
  python3 AUTOMATIONS/app_factory/opportunity_scanner.py --report
  python3 AUTOMATIONS/app_factory/opportunity_scanner.py --help
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import sys
import time
import urllib.request
import urllib.error
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
PROJECT = Path(__file__).resolve().parent.parent.parent
AUTOMATIONS = PROJECT / "AUTOMATIONS"
LEDGER = PROJECT / "LEDGER"
OPS = PROJECT / "OPS"
LOG_DIR = AUTOMATIONS / "app_factory" / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

OPPORTUNITIES_CSV = LEDGER / "APP_FACTORY_OPPORTUNITIES.csv"
ALPHA_STAGING = LEDGER / "ALPHA_STAGING.csv"
LOGFILE = LOG_DIR / "opportunity_scanner.log"

# ---------------------------------------------------------------------------
# Guardrails
# ---------------------------------------------------------------------------
def safe_path(target: Path) -> Path:
    resolved = Path(target).resolve()
    if not str(resolved).startswith(str(PROJECT)):
        raise ValueError(f"BLOCKED: {resolved} is outside project root {PROJECT}")
    return resolved


def log(msg: str) -> None:
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] {msg}"
    print(line)
    with open(safe_path(LOGFILE), "a") as f:
        f.write(line + "\n")


# ---------------------------------------------------------------------------
# HTTP helper (no external deps)
# ---------------------------------------------------------------------------
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
}


def fetch_url(url: str, timeout: int = 20) -> str | None:
    """Fetch URL with retries. Returns text or None."""
    for attempt in range(3):
        try:
            req = urllib.request.Request(url, headers=HEADERS)
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                return resp.read().decode("utf-8", errors="replace")
        except (urllib.error.URLError, urllib.error.HTTPError, OSError) as e:
            log(f"  fetch attempt {attempt+1} failed for {url}: {e}")
            if attempt < 2:
                time.sleep(2 * (attempt + 1))
    return None


def fetch_json(url: str, timeout: int = 20) -> dict | list | None:
    """Fetch JSON from URL. Returns parsed JSON or None."""
    text = fetch_url(url, timeout)
    if text is None:
        return None
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return None


# ---------------------------------------------------------------------------
# Source 1: Apple App Store RSS Feeds
# ---------------------------------------------------------------------------
# Apple provides RSS feeds for top charts by genre
# Genre IDs: 6013=Health&Fitness, 6017=Education, 6023=Food&Drink,
#             6012=Lifestyle, 6015=Finance, 6007=Productivity
APP_STORE_GENRES = {
    "health_fitness": 6013,
    "education": 6017,
    "food_drink": 6023,
    "lifestyle": 6012,
    "finance": 6015,
    "productivity": 6007,
    "photo_video": 6008,
    "social_networking": 6005,
    "utilities": 6002,
    "entertainment": 6016,
}

# App categories we can build with our streak/habit template
TEMPLATE_FIT_CATEGORIES = {
    "health_fitness", "education", "lifestyle", "productivity",
    "food_drink", "social_networking",
}


def scan_app_store_rss() -> list[dict]:
    """Scrape App Store top free/paid/grossing charts via RSS for target genres."""
    results = []
    feed_types = ["topfreeapplications", "toppaidapplications", "topgrossingapplications"]

    for genre_name, genre_id in APP_STORE_GENRES.items():
        for feed_type in feed_types:
            url = (
                f"https://rss.applemarketingtools.com/api/v2/us/apps/{feed_type}/50/"
                f"genre={genre_id}/json"
            )
            data = fetch_json(url, timeout=15)
            if not data:
                # Fallback to iTunes RSS
                url_itunes = (
                    f"https://itunes.apple.com/us/rss/{feed_type}/limit=25/"
                    f"genre={genre_id}/json"
                )
                data = fetch_json(url_itunes, timeout=15)

            if not data:
                continue

            # Parse Apple Marketing Tools format
            if "feed" in data and "results" in data["feed"]:
                for i, app in enumerate(data["feed"]["results"][:25]):
                    results.append({
                        "source": "app_store_rss",
                        "genre": genre_name,
                        "chart": feed_type.replace("applications", ""),
                        "rank": i + 1,
                        "name": app.get("name", ""),
                        "artist": app.get("artistName", ""),
                        "app_id": app.get("id", ""),
                        "url": app.get("url", ""),
                    })
            # Parse iTunes RSS format
            elif "feed" in data and "entry" in data.get("feed", {}):
                entries = data["feed"]["entry"]
                if isinstance(entries, dict):
                    entries = [entries]
                for i, app in enumerate(entries[:25]):
                    name = ""
                    if "im:name" in app:
                        name = app["im:name"].get("label", "")
                    artist = ""
                    if "im:artist" in app:
                        artist = app["im:artist"].get("label", "")
                    app_id = ""
                    if "id" in app and "attributes" in app["id"]:
                        app_id = app["id"]["attributes"].get("im:id", "")
                    results.append({
                        "source": "app_store_rss",
                        "genre": genre_name,
                        "chart": feed_type.replace("applications", ""),
                        "rank": i + 1,
                        "name": name,
                        "artist": artist,
                        "app_id": app_id,
                        "url": "",
                    })

            time.sleep(0.5)  # Be polite

    log(f"App Store RSS: collected {len(results)} chart entries across {len(APP_STORE_GENRES)} genres")
    return results


def extract_app_store_opportunities(chart_data: list[dict]) -> list[dict]:
    """Analyze chart data to find gaps and patterns we can exploit."""
    opportunities = []

    # Count genres and find patterns
    genre_counts: dict[str, int] = {}
    name_patterns: list[str] = []
    for entry in chart_data:
        genre = entry.get("genre", "")
        genre_counts[genre] = genre_counts.get(genre, 0) + 1
        name_patterns.append(entry.get("name", "").lower())

    # Find trending keywords across chart names
    word_freq: dict[str, int] = {}
    stop_words = {"the", "a", "an", "and", "or", "for", "to", "of", "in", "my",
                  "your", "app", "pro", "free", "new", "best", "-", "&", "with"}
    for name in name_patterns:
        words = re.findall(r'[a-z]+', name)
        for w in words:
            if w not in stop_words and len(w) > 2:
                word_freq[w] = word_freq.get(w, 0) + 1

    # Top trending keywords (appear in 3+ chart apps)
    trending_kws = sorted(
        [(w, c) for w, c in word_freq.items() if c >= 3],
        key=lambda x: -x[1]
    )[:30]

    # Build opportunities from trending keywords that fit our template
    streak_fit_keywords = [
        "streak", "habit", "tracker", "daily", "focus", "meditation",
        "prayer", "workout", "fasting", "journal", "reading", "sleep",
        "water", "fitness", "yoga", "mood", "gratitude", "mindfulness",
        "bible", "quran", "study", "learning", "nutrition", "walk",
        "run", "breathe", "plank", "pushup", "stretch", "calm",
    ]

    for kw, count in trending_kws:
        # Check if this keyword suggests an app we can build
        fits_template = any(
            kw in sk or sk in kw for sk in streak_fit_keywords
        )
        if fits_template or count >= 5:
            opp_id = hashlib.md5(f"appstore_{kw}".encode()).hexdigest()[:12]
            opportunities.append({
                "id": f"OPP_{opp_id}",
                "source": "app_store_charts",
                "keyword": kw,
                "chart_frequency": count,
                "template_fit": "HIGH" if fits_template else "MEDIUM",
                "niche": _keyword_to_niche(kw),
                "opportunity_type": "trending_keyword",
            })

    # Identify underserved genres (few grossing apps but high demand)
    for genre in TEMPLATE_FIT_CATEGORIES:
        grossing_count = sum(
            1 for e in chart_data
            if e.get("genre") == genre and "grossing" in e.get("chart", "")
        )
        free_count = sum(
            1 for e in chart_data
            if e.get("genre") == genre and "free" in e.get("chart", "")
        )
        if free_count > 0 and grossing_count < free_count * 0.3:
            opp_id = hashlib.md5(f"genre_gap_{genre}".encode()).hexdigest()[:12]
            opportunities.append({
                "id": f"OPP_{opp_id}",
                "source": "app_store_genre_gap",
                "keyword": genre,
                "chart_frequency": free_count,
                "template_fit": "HIGH",
                "niche": genre.replace("_", " ").title(),
                "opportunity_type": "underserved_genre",
            })

    log(f"App Store analysis: found {len(opportunities)} opportunities from chart data")
    return opportunities


def _keyword_to_niche(kw: str) -> str:
    """Map a keyword to a niche category."""
    niche_map = {
        "fitness": "Health & Fitness", "workout": "Health & Fitness",
        "yoga": "Health & Fitness", "plank": "Health & Fitness",
        "pushup": "Health & Fitness", "run": "Health & Fitness",
        "walk": "Health & Fitness", "stretch": "Health & Fitness",
        "meditation": "Wellness", "mindfulness": "Wellness",
        "calm": "Wellness", "breathe": "Wellness", "sleep": "Wellness",
        "prayer": "Religious/Spiritual", "bible": "Religious/Spiritual",
        "quran": "Religious/Spiritual", "faith": "Religious/Spiritual",
        "fasting": "Religious/Spiritual",
        "journal": "Productivity", "focus": "Productivity",
        "habit": "Productivity", "streak": "Productivity",
        "study": "Education", "learning": "Education", "reading": "Education",
        "nutrition": "Food & Health", "water": "Food & Health",
        "mood": "Mental Health", "gratitude": "Mental Health",
        "tracker": "Utility",
    }
    return niche_map.get(kw, "General")


# ---------------------------------------------------------------------------
# Source 2: Reddit Pain Point Scraping
# ---------------------------------------------------------------------------
REDDIT_SUBREDDITS = [
    "androidapps", "iosapps", "AppIdeas", "SideProject",
    "Entrepreneur", "startups", "indiehackers",
    "selfimprovement", "getdisciplined", "productivity",
    "Fitness", "loseit", "intermittentfasting",
    "Meditation", "mentalhealth", "Christianity",
    "Islam", "Buddhism", "Judaism",
]

PAIN_POINT_SIGNALS = [
    r"i wish there was an app",
    r"looking for an app",
    r"is there an app",
    r"any app that",
    r"need an app",
    r"cant find.*app",
    r"no good app",
    r"why isnt there",
    r"would pay for",
    r"someone should build",
    r"idea for an app",
    r"app idea",
    r"app suggestion",
    r"daily habit",
    r"streak tracker",
    r"i need a way to track",
    r"accountability",
]


def scan_reddit_pain_points() -> list[dict]:
    """Scan Reddit for app pain points and opportunities via JSON API."""
    results = []

    for sub in REDDIT_SUBREDDITS:
        # Reddit JSON API (no auth needed, rate limited)
        url = f"https://www.reddit.com/r/{sub}/search.json?q=app+idea+OR+wish+app+OR+need+app+OR+habit+tracker&sort=new&t=month&limit=25"
        data = fetch_json(url, timeout=15)
        if not data or "data" not in data:
            time.sleep(2)
            continue

        posts = data.get("data", {}).get("children", [])
        for post_wrapper in posts:
            post = post_wrapper.get("data", {})
            title = post.get("title", "")
            selftext = post.get("selftext", "")[:500]
            score = post.get("score", 0)
            num_comments = post.get("num_comments", 0)
            permalink = post.get("permalink", "")

            combined = (title + " " + selftext).lower()

            # Check for pain point signals
            matched_signals = []
            for pattern in PAIN_POINT_SIGNALS:
                if re.search(pattern, combined, re.IGNORECASE):
                    matched_signals.append(pattern)

            if matched_signals and score >= 2:
                opp_id = hashlib.md5(
                    f"reddit_{sub}_{title[:30]}".encode()
                ).hexdigest()[:12]

                # Extract potential niche from content
                niche = _extract_niche_from_text(combined)

                results.append({
                    "id": f"OPP_{opp_id}",
                    "source": f"reddit_r/{sub}",
                    "title": title[:120],
                    "score": score,
                    "comments": num_comments,
                    "pain_signals": len(matched_signals),
                    "niche": niche,
                    "url": f"https://reddit.com{permalink}",
                    "opportunity_type": "pain_point",
                    "template_fit": "HIGH" if any(
                        kw in combined for kw in
                        ["habit", "streak", "daily", "track", "routine"]
                    ) else "MEDIUM",
                })

        time.sleep(2)  # Reddit rate limit: ~1 req/2s for unauthenticated

    log(f"Reddit scan: found {len(results)} pain points across {len(REDDIT_SUBREDDITS)} subreddits")
    return results


def _extract_niche_from_text(text: str) -> str:
    """Extract the most likely niche from text content."""
    niche_keywords = {
        "Health & Fitness": ["workout", "exercise", "gym", "weight", "fitness", "running", "steps"],
        "Wellness": ["meditation", "mindfulness", "breathing", "sleep", "calm", "stress"],
        "Religious/Spiritual": ["prayer", "bible", "quran", "church", "faith", "god", "spiritual"],
        "Productivity": ["habit", "routine", "focus", "productivity", "goal", "todo", "task"],
        "Education": ["study", "learn", "reading", "book", "language", "vocab"],
        "Food & Health": ["water", "diet", "nutrition", "meal", "calorie", "fasting"],
        "Mental Health": ["mood", "journal", "gratitude", "anxiety", "therapy", "mental"],
        "Finance": ["budget", "saving", "money", "invest", "expense"],
    }

    scores: dict[str, int] = {}
    for niche, keywords in niche_keywords.items():
        score = sum(1 for kw in keywords if kw in text)
        if score > 0:
            scores[niche] = score

    if scores:
        return max(scores, key=scores.get)  # type: ignore[arg-type]
    return "General"


# ---------------------------------------------------------------------------
# Source 3: App Store Search Suggestions (keyword gaps)
# ---------------------------------------------------------------------------
SEED_KEYWORDS = [
    "habit tracker", "streak tracker", "daily routine", "prayer app",
    "meditation timer", "water reminder", "mood journal", "gratitude journal",
    "bible study", "quran daily", "workout streak", "fasting tracker",
    "reading log", "study timer", "focus timer", "sleep tracker",
    "sobriety counter", "pushup challenge", "yoga daily", "breath work",
    "language practice", "coding streak", "fitness challenge", "walk tracker",
]


def scan_keyword_suggestions() -> list[dict]:
    """Use App Store search suggestions API to find keyword gaps."""
    results = []

    for seed in SEED_KEYWORDS:
        url = (
            f"https://search.itunes.apple.com/WebObjects/MZSearchHints.woa/wa/hints?"
            f"media=software&term={urllib.request.quote(seed)}"
        )
        data = fetch_url(url, timeout=10)
        if not data:
            time.sleep(1)
            continue

        # Parse the hints XML/plist
        try:
            root = ET.fromstring(data)
            hints = []
            # Apple returns a plist with an array of dicts
            for dict_elem in root.findall(".//dict"):
                strings = dict_elem.findall("string")
                for s in strings:
                    if s.text and len(s.text) > 3:
                        hints.append(s.text.strip())
        except ET.ParseError:
            # Try to parse as JSON if XML fails
            try:
                jdata = json.loads(data)
                if isinstance(jdata, dict) and "hints" in jdata:
                    hints = [h.get("term", "") for h in jdata["hints"] if h.get("term")]
                elif isinstance(jdata, list):
                    hints = [str(h) for h in jdata if isinstance(h, str)]
                else:
                    hints = []
            except (json.JSONDecodeError, TypeError):
                hints = []

        for hint in hints[:5]:
            # Check if this suggestion represents a gap we can fill
            opp_id = hashlib.md5(f"kw_{hint}".encode()).hexdigest()[:12]
            niche = _extract_niche_from_text(hint.lower())
            fits = any(
                kw in hint.lower()
                for kw in ["habit", "streak", "daily", "tracker", "timer", "journal", "challenge"]
            )
            results.append({
                "id": f"OPP_{opp_id}",
                "source": "keyword_suggestions",
                "keyword": hint,
                "seed": seed,
                "niche": niche,
                "opportunity_type": "keyword_gap",
                "template_fit": "HIGH" if fits else "LOW",
            })

        time.sleep(0.5)

    log(f"Keyword suggestions: collected {len(results)} keyword opportunities")
    return results


# ---------------------------------------------------------------------------
# Source 4: Existing Alpha Pipeline
# ---------------------------------------------------------------------------
def scan_alpha_staging() -> list[dict]:
    """Pull app-related alpha from ALPHA_STAGING.csv."""
    results = []
    if not ALPHA_STAGING.exists():
        log("ALPHA_STAGING.csv not found, skipping")
        return results

    app_keywords = [
        "app", "ios", "mobile", "subscription", "paywall",
        "habit", "streak", "revenuecat", "expo", "react native",
    ]

    try:
        with open(ALPHA_STAGING, "r", newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                status = row.get("status", "").upper()
                if status in ("ARCHIVED", "REJECTED"):
                    continue

                content = (
                    row.get("content", "") + " " +
                    row.get("title", "") + " " +
                    row.get("description", "")
                ).lower()

                if any(kw in content for kw in app_keywords):
                    opp_id = hashlib.md5(
                        f"alpha_{row.get('id', '')}_{row.get('title', '')[:20]}".encode()
                    ).hexdigest()[:12]

                    results.append({
                        "id": f"OPP_{opp_id}",
                        "source": "alpha_staging",
                        "title": row.get("title", "")[:120],
                        "alpha_status": status,
                        "roi_estimate": row.get("roi_estimate", "MEDIUM"),
                        "niche": _extract_niche_from_text(content),
                        "opportunity_type": "alpha_pipeline",
                        "template_fit": "HIGH" if any(
                            kw in content for kw in ["streak", "habit", "daily", "track"]
                        ) else "MEDIUM",
                    })
    except Exception as e:
        log(f"Error reading ALPHA_STAGING: {e}")

    log(f"Alpha staging: found {len(results)} app-related entries")
    return results


# ---------------------------------------------------------------------------
# Scoring Engine
# ---------------------------------------------------------------------------
def score_opportunity(opp: dict) -> float:
    """Score an opportunity on 0-100 scale across multiple dimensions."""
    score = 0.0

    # 1. Template fit (0-25)
    fit = opp.get("template_fit", "LOW")
    fit_scores = {"HIGH": 25, "MEDIUM": 15, "LOW": 5}
    score += fit_scores.get(fit, 5)

    # 2. Market signal strength (0-25)
    source = opp.get("source", "")
    if "app_store" in source:
        # Chart presence = validated demand
        rank = opp.get("rank", 50)
        freq = opp.get("chart_frequency", 1)
        score += min(25, 10 + freq * 2 + max(0, (50 - rank) * 0.3))
    elif "reddit" in source:
        post_score = opp.get("score", 0)
        comments = opp.get("comments", 0)
        pain_signals = opp.get("pain_signals", 0)
        score += min(25, post_score * 0.5 + comments * 0.3 + pain_signals * 5)
    elif source == "keyword_suggestions":
        score += 12  # Moderate signal -- Apple suggests it
    elif source == "alpha_staging":
        roi = opp.get("roi_estimate", "MEDIUM")
        roi_scores = {"HIGHEST": 25, "HIGH": 20, "MEDIUM": 12, "LOW": 5}
        score += roi_scores.get(roi, 10)

    # 3. Niche quality (0-25)
    niche = opp.get("niche", "General")
    # High-value niches based on our paywall research
    niche_scores = {
        "Health & Fitness": 25,  # Highest LTV ($46.1 annual)
        "Food & Health": 22,
        "Wellness": 22,
        "Religious/Spiritual": 20,  # Low competition, loyal users
        "Mental Health": 20,
        "Education": 18,
        "Productivity": 16,
        "Finance": 15,
        "General": 8,
    }
    score += niche_scores.get(niche, 8)

    # 4. Competition assessment (0-25)
    # Lower competition = higher score
    opp_type = opp.get("opportunity_type", "")
    if opp_type == "underserved_genre":
        score += 25  # Genre gap = low competition
    elif opp_type == "pain_point":
        score += 20  # Unmet need = potential gap
    elif opp_type == "keyword_gap":
        score += 15  # Suggestion gap = moderate opportunity
    elif opp_type == "trending_keyword":
        score += 10  # Trending = some competition
    else:
        score += 8

    return round(min(100, score), 1)


def deduplicate_opportunities(opps: list[dict]) -> list[dict]:
    """Deduplicate opportunities by niche+keyword similarity."""
    seen_keys: set[str] = set()
    deduped = []

    for opp in opps:
        # Create a dedup key from niche + primary keyword
        kw = opp.get("keyword", opp.get("title", "")).lower()[:30]
        niche = opp.get("niche", "").lower()
        key = f"{niche}_{kw}"

        # Simple dedup: skip if we've seen this niche+keyword combo
        if key not in seen_keys:
            seen_keys.add(key)
            deduped.append(opp)

    return deduped


# ---------------------------------------------------------------------------
# Output
# ---------------------------------------------------------------------------
CSV_FIELDS = [
    "id", "score", "source", "niche", "opportunity_type", "template_fit",
    "keyword", "title", "chart_frequency", "reddit_score", "comments",
    "pain_signals", "roi_estimate", "url", "scanned_at", "status",
]


def write_opportunities_csv(opps: list[dict], dry_run: bool = False) -> None:
    """Write scored opportunities to CSV."""
    output = safe_path(OPPORTUNITIES_CSV)

    # Load existing to merge
    existing: dict[str, dict] = {}
    if output.exists():
        try:
            with open(output, "r", newline="") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    existing[row.get("id", "")] = row
        except Exception:
            pass

    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new_count = 0
    updated_count = 0

    for opp in opps:
        opp_id = opp.get("id", "")
        if opp_id in existing:
            # Update score but keep status if manually set
            old = existing[opp_id]
            if old.get("status", "") not in ("BUILDING", "BUILT", "SUBMITTED", "REJECTED_MANUAL"):
                old["score"] = str(opp.get("score", 0))
                old["scanned_at"] = ts
                updated_count += 1
        else:
            row = {field: "" for field in CSV_FIELDS}
            row["id"] = opp_id
            row["score"] = str(opp.get("score", 0))
            row["source"] = opp.get("source", "")
            row["niche"] = opp.get("niche", "")
            row["opportunity_type"] = opp.get("opportunity_type", "")
            row["template_fit"] = opp.get("template_fit", "")
            row["keyword"] = opp.get("keyword", "")
            row["title"] = opp.get("title", "")
            row["chart_frequency"] = str(opp.get("chart_frequency", ""))
            row["reddit_score"] = str(opp.get("score_reddit", opp.get("score", "")))
            row["comments"] = str(opp.get("comments", ""))
            row["pain_signals"] = str(opp.get("pain_signals", ""))
            row["roi_estimate"] = opp.get("roi_estimate", "")
            row["url"] = opp.get("url", "")
            row["scanned_at"] = ts
            row["status"] = "NEW"
            existing[opp_id] = row
            new_count += 1

    if dry_run:
        log(f"DRY RUN: Would write {new_count} new, {updated_count} updated to {output}")
        return

    # Write all
    rows = sorted(existing.values(), key=lambda r: -float(r.get("score", 0)))
    with open(output, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_FIELDS, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)

    log(f"Wrote {len(rows)} opportunities ({new_count} new, {updated_count} updated) to {output}")


def stage_top_opportunities_to_alpha(opps: list[dict], top_n: int = 10, dry_run: bool = False) -> None:
    """Stage the top N opportunities into ALPHA_STAGING for pipeline integration."""
    if dry_run:
        log(f"DRY RUN: Would stage top {top_n} opportunities to ALPHA_STAGING")
        return

    top = sorted(opps, key=lambda o: -o.get("score", 0))[:top_n]
    if not top:
        return

    staging_path = safe_path(ALPHA_STAGING)

    # Read existing IDs to avoid duplicates
    existing_ids: set[str] = set()
    if staging_path.exists():
        try:
            with open(staging_path, "r", newline="") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    existing_ids.add(row.get("id", ""))
        except Exception:
            pass

    staged_count = 0
    with open(staging_path, "a", newline="") as f:
        writer = None
        for opp in top:
            opp_id = opp.get("id", "")
            if opp_id in existing_ids:
                continue

            alpha_row = {
                "id": opp_id,
                "timestamp": datetime.now().isoformat(),
                "source": f"app_factory_scanner_{opp.get('source', '')}",
                "title": f"App Opportunity: {opp.get('keyword', opp.get('title', 'Unknown'))}",
                "content": f"Niche: {opp.get('niche', 'Unknown')}. Type: {opp.get('opportunity_type', '')}. Template fit: {opp.get('template_fit', '')}. Score: {opp.get('score', 0)}",
                "status": "PENDING_REVIEW",
                "roi_estimate": "HIGH" if opp.get("score", 0) >= 70 else "MEDIUM",
                "venture_type": "APP_FACTORY",
                "priority": "THIS_WEEK" if opp.get("score", 0) >= 60 else "MEDIUM",
            }
            if writer is None:
                writer = csv.DictWriter(f, fieldnames=list(alpha_row.keys()))
                if f.tell() == 0:
                    writer.writeheader()
            writer.writerow(alpha_row)
            staged_count += 1

    log(f"Staged {staged_count} top opportunities to ALPHA_STAGING.csv")


# ---------------------------------------------------------------------------
# Report
# ---------------------------------------------------------------------------
def generate_report() -> str:
    """Generate a report of current opportunities."""
    if not OPPORTUNITIES_CSV.exists():
        return "No opportunities CSV found. Run --scan first."

    rows = []
    with open(OPPORTUNITIES_CSV, "r", newline="") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    if not rows:
        return "Opportunities CSV is empty. Run --scan first."

    # Sort by score descending
    rows.sort(key=lambda r: -float(r.get("score", 0)))

    lines = [
        "# App Factory Opportunity Report",
        f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"Total opportunities: {len(rows)}",
        "",
        "## Top 20 Opportunities",
        "",
        "| Rank | Score | Niche | Keyword/Title | Source | Template Fit | Status |",
        "|------|-------|-------|---------------|--------|-------------|--------|",
    ]

    for i, row in enumerate(rows[:20], 1):
        kw = row.get("keyword", "") or row.get("title", "")
        lines.append(
            f"| {i} | {row.get('score', '?')} | {row.get('niche', '?')} | "
            f"{kw[:40]} | {row.get('source', '?')[:20]} | "
            f"{row.get('template_fit', '?')} | {row.get('status', '?')} |"
        )

    # Stats by niche
    niche_counts: dict[str, int] = {}
    for row in rows:
        n = row.get("niche", "Unknown")
        niche_counts[n] = niche_counts.get(n, 0) + 1

    lines.extend([
        "",
        "## By Niche",
        "",
        "| Niche | Count | Avg Score |",
        "|-------|-------|-----------|",
    ])

    for niche, count in sorted(niche_counts.items(), key=lambda x: -x[1]):
        avg = sum(
            float(r.get("score", 0)) for r in rows if r.get("niche") == niche
        ) / max(count, 1)
        lines.append(f"| {niche} | {count} | {avg:.1f} |")

    # Stats by source
    source_counts: dict[str, int] = {}
    for row in rows:
        s = row.get("source", "unknown")
        source_counts[s] = source_counts.get(s, 0) + 1

    lines.extend([
        "",
        "## By Source",
        "",
        "| Source | Count |",
        "|--------|-------|",
    ])
    for source, count in sorted(source_counts.items(), key=lambda x: -x[1]):
        lines.append(f"| {source} | {count} |")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main() -> None:
    parser = argparse.ArgumentParser(
        description="App Factory Opportunity Scanner",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 AUTOMATIONS/app_factory/opportunity_scanner.py --scan
  python3 AUTOMATIONS/app_factory/opportunity_scanner.py --scan --dry-run
  python3 AUTOMATIONS/app_factory/opportunity_scanner.py --report
  python3 AUTOMATIONS/app_factory/opportunity_scanner.py --scan --sources appstore,reddit
        """,
    )
    parser.add_argument("--scan", action="store_true", help="Run full opportunity scan")
    parser.add_argument("--report", action="store_true", help="Generate opportunity report")
    parser.add_argument("--dry-run", action="store_true", help="Don't write files, just show what would happen")
    parser.add_argument("--sources", default="all", help="Comma-separated sources: appstore,reddit,keywords,alpha (default: all)")
    parser.add_argument("--stage-top", type=int, default=10, help="Stage top N opportunities to alpha pipeline (default: 10)")

    args = parser.parse_args()

    if not args.scan and not args.report:
        parser.print_help()
        return

    if args.report:
        report = generate_report()
        print(report)
        return

    if args.scan:
        log("=" * 60)
        log("App Factory Opportunity Scanner starting")
        log("=" * 60)

        all_opportunities: list[dict] = []
        sources = args.sources.split(",") if args.sources != "all" else ["appstore", "reddit", "keywords", "alpha"]

        if "appstore" in sources:
            log("Scanning App Store charts...")
            chart_data = scan_app_store_rss()
            appstore_opps = extract_app_store_opportunities(chart_data)
            all_opportunities.extend(appstore_opps)

        if "reddit" in sources:
            log("Scanning Reddit pain points...")
            reddit_opps = scan_reddit_pain_points()
            all_opportunities.extend(reddit_opps)

        if "keywords" in sources:
            log("Scanning keyword suggestions...")
            kw_opps = scan_keyword_suggestions()
            all_opportunities.extend(kw_opps)

        if "alpha" in sources:
            log("Scanning alpha staging...")
            alpha_opps = scan_alpha_staging()
            all_opportunities.extend(alpha_opps)

        # Deduplicate
        all_opportunities = deduplicate_opportunities(all_opportunities)

        # Score
        for opp in all_opportunities:
            opp["score"] = score_opportunity(opp)

        # Sort by score
        all_opportunities.sort(key=lambda o: -o.get("score", 0))

        log(f"Total unique opportunities: {len(all_opportunities)}")
        if all_opportunities:
            log(f"Top scored: {all_opportunities[0].get('keyword', all_opportunities[0].get('title', '?'))} ({all_opportunities[0].get('score', 0)})")

        # Write CSV
        write_opportunities_csv(all_opportunities, dry_run=args.dry_run)

        # Stage top to alpha pipeline
        stage_top_opportunities_to_alpha(
            all_opportunities,
            top_n=args.stage_top,
            dry_run=args.dry_run,
        )

        log("Scan complete.")


if __name__ == "__main__":
    main()
