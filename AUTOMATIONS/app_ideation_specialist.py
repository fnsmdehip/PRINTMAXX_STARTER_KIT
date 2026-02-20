#!/usr/bin/env python3
"""
PRINTMAXX App Ideation Specialist
===================================
Discovers viral trends and matches them to simple app ideas that can be
vibe-coded in <24 hours. Fetches from free APIs, clusters trends, identifies
app gaps, scores ideas, and outputs actionable specs.

Sources:
  - YouTube Data API v3 (10K units/day free)
  - pytrends (Google Trends, free, no key)
  - TikTok Creative Center (public scrape)
  - Reddit JSON API (free, no auth)
  - iTunes Search API (free, app gap analysis)

Usage:
  python3 app_ideation_specialist.py --scan
  python3 app_ideation_specialist.py --trends-only
  python3 app_ideation_specialist.py --score-idea "AI-powered daily affirmation app for Muslim women"
  python3 app_ideation_specialist.py --status
  python3 app_ideation_specialist.py --top 5
"""

import argparse
import csv
import hashlib
import json
import os
import random
import re
import sys
import time
import traceback
import urllib.request
import urllib.parse
import urllib.error
from datetime import datetime, timedelta
from pathlib import Path

# ---------------------------------------------------------------------------
# Constants & paths
# ---------------------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent
LEDGER_DIR = PROJECT_ROOT / "LEDGER"
OPS_DIR = PROJECT_ROOT / "OPS"
AUTOMATIONS_DIR = PROJECT_ROOT / "AUTOMATIONS"
CACHE_DIR = AUTOMATIONS_DIR / "output" / "app_ideation_cache"
APP_DISCOVERY_MD = PROJECT_ROOT / "MONEY_METHODS" / "APP_FACTORY" / "APP_DISCOVERY_ENGINE.md"
CLONE_CSV = LEDGER_DIR / "APP_CLONE_OPPORTUNITIES.csv"
RESULTS_CSV = LEDGER_DIR / "APP_IDEATION_RESULTS.csv"
ALPHA_CSV = LEDGER_DIR / "ALPHA_STAGING.csv"

CACHE_TTL_HOURS = 6
SCORE_THRESHOLD = 16
TODAY = datetime.now().strftime("%Y-%m-%d")
TIMESTAMP = datetime.now().strftime("%Y-%m-%d_%H%M%S")

# Subreddits for app-related trend discovery
APP_SUBREDDITS = [
    "SideProject", "indiehackers", "startups", "AppIdeas",
    "androidapps", "iOSProgramming", "reactnative", "FlutterDev",
    "webdev", "selfhosted", "ProductHunt", "Entrepreneur",
]

# Google Trends seed keywords for app-related searches
TRENDS_SEEDS = [
    "app", "ai app", "productivity app", "fitness app", "habit tracker",
    "prayer app", "meditation app", "budget app", "sleep tracker",
    "meal planner", "workout app", "journaling app", "language learning",
    "fasting app", "calorie counter", "water tracker", "mood tracker",
]

# YouTube trending video categories relevant to apps
YT_CATEGORIES = {
    "28": "Science & Technology",
    "22": "People & Blogs",
    "26": "How-to & Style",
    "27": "Education",
}

# Insider-style name fragments for generating non-AI-slop names
NAME_FRAGMENTS = {
    "prefixes": [
        "lock", "max", "streak", "drift", "step", "pulse", "void",
        "hush", "glow", "reps", "mise", "dusk", "tack", "ruck",
        "slab", "zone", "hype", "monk", "grind", "stash", "batch",
    ],
    "suffixes": [
        "lab", "kit", "log", "den", "hub", "run", "tap", "box",
        "pal", "way", "flo", "ink", "arc", "vue", "ops", "ism",
    ],
}

TECH_STACKS = [
    "Next.js PWA (Vercel free tier, instant deploy)",
    "React Native + Expo (cross-platform, EAS build free tier)",
    "SvelteKit PWA (lightweight, Cloudflare Pages free)",
    "Remix PWA (Vercel/Netlify free tier)",
    "Flutter Web + Mobile (single codebase, Firebase free tier)",
    "Astro + Preact PWA (ultra-light, Netlify free)",
]

REVENUE_MODELS = [
    "Freemium + weekly subscription ($4.99/week)",
    "Free + in-app purchases (consumables)",
    "Free + ads (AdMob interstitial + rewarded)",
    "Freemium + monthly sub ($9.99/mo) via RevenueCat",
    "Free + affiliate product recommendations",
    "One-time purchase ($2.99) + tip jar",
    "Free tier + pro unlock ($19.99 lifetime)",
]


# ---------------------------------------------------------------------------
# Utility helpers
# ---------------------------------------------------------------------------

def safe_path(target: Path) -> Path:
    """Verify path is within project root."""
    resolved = Path(target).resolve()
    if not str(resolved).startswith(str(PROJECT_ROOT)):
        raise ValueError(f"BLOCKED: {resolved} is outside project root")
    return resolved


def ensure_dirs():
    """Create output directories if missing."""
    for d in [CACHE_DIR, LEDGER_DIR, OPS_DIR]:
        safe_path(d)
        d.mkdir(parents=True, exist_ok=True)


def fetch_url(url: str, headers: dict = None, retries: int = 3, timeout: int = 15) -> str:
    """Fetch URL content with retry and exponential backoff."""
    hdr = {"User-Agent": "PRINTMAXX-AppIdeation/1.0"}
    if headers:
        hdr.update(headers)
    req = urllib.request.Request(url, headers=hdr)
    for attempt in range(retries):
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                return resp.read().decode("utf-8", errors="replace")
        except (urllib.error.URLError, urllib.error.HTTPError, OSError) as e:
            if attempt == retries - 1:
                print(f"  [WARN] Failed to fetch {url}: {e}")
                return ""
            wait = (2 ** attempt) + random.uniform(0, 1)
            time.sleep(wait)
    return ""


def cache_key(label: str) -> Path:
    """Generate a cache file path for a given label."""
    h = hashlib.md5(label.encode()).hexdigest()[:10]
    return CACHE_DIR / f"{label}_{h}.json"


def read_cache(label: str):
    """Read cached data if still fresh (within CACHE_TTL_HOURS)."""
    path = cache_key(label)
    if not path.exists():
        return None
    mtime = datetime.fromtimestamp(path.stat().st_mtime)
    if datetime.now() - mtime > timedelta(hours=CACHE_TTL_HOURS):
        return None
    try:
        with open(path, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return None


def write_cache(label: str, data):
    """Write data to cache."""
    path = cache_key(label)
    safe_path(path)
    with open(path, "w") as f:
        json.dump(data, f, indent=2, default=str)


def load_existing_clones() -> list:
    """Load existing clone opportunities for gap cross-reference."""
    if not CLONE_CSV.exists():
        return []
    rows = []
    try:
        with open(CLONE_CSV, "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                rows.append(row)
    except Exception:
        pass
    return rows


def load_discovery_context() -> str:
    """Read APP_DISCOVERY_ENGINE.md for context signals."""
    if not APP_DISCOVERY_MD.exists():
        return ""
    try:
        with open(APP_DISCOVERY_MD, "r") as f:
            return f.read()[:3000]
    except Exception:
        return ""


def next_alpha_id() -> str:
    """Get the next ALPHA ID from ALPHA_STAGING.csv."""
    max_id = 0
    if ALPHA_CSV.exists():
        try:
            with open(ALPHA_CSV, "r") as f:
                for line in f:
                    m = re.match(r"ALPHA(\d+)", line)
                    if m:
                        max_id = max(max_id, int(m.group(1)))
        except Exception:
            pass
    return f"ALPHA{max_id + 1}"


# ---------------------------------------------------------------------------
# 1. Trend Discovery
# ---------------------------------------------------------------------------

def fetch_google_trends() -> list:
    """Fetch trending searches via pytrends (Google Trends)."""
    cached = read_cache("google_trends")
    if cached:
        print("  [CACHE] Google Trends data from cache")
        return cached

    trends = []
    try:
        from pytrends.request import TrendReq
        pytrends = TrendReq(hl="en-US", tz=360, timeout=(10, 25))

        # Trending searches (real-time)
        try:
            df = pytrends.trending_searches(pn="united_states")
            for _, row in df.iterrows():
                trends.append({
                    "source": "google_trends_realtime",
                    "term": str(row[0]),
                    "score": 100,
                    "category": "trending_search",
                })
        except Exception as e:
            print(f"  [WARN] Trending searches failed: {e}")

        # Related queries for app-related seeds
        for seed in TRENDS_SEEDS[:6]:
            try:
                pytrends.build_payload([seed], timeframe="now 7-d", geo="US")
                related = pytrends.related_queries()
                if seed in related and related[seed].get("rising") is not None:
                    df_rising = related[seed]["rising"]
                    if df_rising is not None and not df_rising.empty:
                        for _, row in df_rising.head(5).iterrows():
                            trends.append({
                                "source": "google_trends_related",
                                "term": str(row.get("query", "")),
                                "score": int(row.get("value", 50)),
                                "category": f"related_to_{seed.replace(' ', '_')}",
                            })
                time.sleep(1)  # rate limit courtesy
            except Exception:
                continue

    except ImportError:
        print("  [INFO] pytrends not installed. Run: pip3 install pytrends")
        print("  [INFO] Falling back to manual trend seeds")
        for seed in TRENDS_SEEDS:
            trends.append({
                "source": "seed_keyword",
                "term": seed,
                "score": 50,
                "category": "seed",
            })
    except Exception as e:
        print(f"  [WARN] Google Trends fetch error: {e}")

    write_cache("google_trends", trends)
    return trends


def fetch_reddit_trends() -> list:
    """Fetch hot posts from app-related subreddits via Reddit JSON API."""
    cached = read_cache("reddit_trends")
    if cached:
        print("  [CACHE] Reddit trends from cache")
        return cached

    trends = []
    for sub in APP_SUBREDDITS:
        url = f"https://www.reddit.com/r/{sub}/hot.json?limit=10"
        raw = fetch_url(url)
        if not raw:
            continue
        try:
            data = json.loads(raw)
            children = data.get("data", {}).get("children", [])
            for post in children:
                pd = post.get("data", {})
                title = pd.get("title", "")
                ups = pd.get("ups", 0)
                comments = pd.get("num_comments", 0)
                created = pd.get("created_utc", 0)
                age_hours = (time.time() - created) / 3600 if created else 999
                velocity = (ups + comments * 2) / max(age_hours, 1)
                trends.append({
                    "source": f"reddit_r/{sub}",
                    "term": title,
                    "score": min(int(velocity), 999),
                    "category": "reddit_hot",
                    "upvotes": ups,
                    "comments": comments,
                    "url": f"https://reddit.com{pd.get('permalink', '')}",
                    "velocity": round(velocity, 1),
                })
        except (json.JSONDecodeError, KeyError):
            continue
        time.sleep(0.5)  # be nice to Reddit

    write_cache("reddit_trends", trends)
    return trends


def fetch_youtube_trending() -> list:
    """Fetch YouTube trending videos. Uses API key if available, else scrapes."""
    cached = read_cache("youtube_trends")
    if cached:
        print("  [CACHE] YouTube trends from cache")
        return cached

    trends = []
    yt_key = os.environ.get("YOUTUBE_API_KEY", "")

    if yt_key:
        for cat_id, cat_name in YT_CATEGORIES.items():
            url = (
                f"https://www.googleapis.com/youtube/v3/videos"
                f"?part=snippet,statistics&chart=mostPopular&regionCode=US"
                f"&videoCategoryId={cat_id}&maxResults=10&key={yt_key}"
            )
            raw = fetch_url(url)
            if not raw:
                continue
            try:
                data = json.loads(raw)
                for item in data.get("items", []):
                    snippet = item.get("snippet", {})
                    stats = item.get("statistics", {})
                    trends.append({
                        "source": f"youtube_{cat_name.replace(' ', '_')}",
                        "term": snippet.get("title", ""),
                        "score": int(stats.get("viewCount", 0)) // 1000,
                        "category": f"yt_{cat_name.lower().replace(' ', '_')}",
                        "views": int(stats.get("viewCount", 0)),
                        "likes": int(stats.get("likeCount", 0)),
                        "channel": snippet.get("channelTitle", ""),
                    })
            except (json.JSONDecodeError, KeyError, ValueError):
                continue
    else:
        print("  [INFO] No YOUTUBE_API_KEY set. Skipping YouTube trending (set env var to enable)")

    write_cache("youtube_trends", trends)
    return trends


def fetch_tiktok_trends() -> list:
    """Scrape TikTok Creative Center for trending hashtags."""
    cached = read_cache("tiktok_trends")
    if cached:
        print("  [CACHE] TikTok trends from cache")
        return cached

    trends = []
    # TikTok Creative Center trending hashtags page (public)
    url = "https://ads.tiktok.com/business/creativecenter/inspiration/popular/hashtag/pc/en"
    raw = fetch_url(url, timeout=20)
    if raw:
        # Extract hashtag names from the page HTML
        hashtag_pattern = re.findall(r'\"hashtag_name\":\s*\"([^\"]+)\"', raw)
        if not hashtag_pattern:
            # Fallback: try to extract from visible text patterns
            hashtag_pattern = re.findall(r'#(\w{3,30})', raw)

        seen = set()
        for tag in hashtag_pattern[:30]:
            tag_lower = tag.lower()
            if tag_lower not in seen:
                seen.add(tag_lower)
                trends.append({
                    "source": "tiktok_creative_center",
                    "term": f"#{tag}",
                    "score": 80,
                    "category": "tiktok_hashtag",
                })
    else:
        print("  [INFO] TikTok Creative Center scrape returned empty. Rate-limited or blocked.")

    # Also try the trending sounds/music endpoint
    sounds_url = "https://ads.tiktok.com/business/creativecenter/inspiration/popular/music/pc/en"
    raw_sounds = fetch_url(sounds_url, timeout=20)
    if raw_sounds:
        sound_pattern = re.findall(r'\"music_name\":\s*\"([^\"]+)\"', raw_sounds)
        for sound in sound_pattern[:10]:
            trends.append({
                "source": "tiktok_sounds",
                "term": sound,
                "score": 70,
                "category": "tiktok_sound",
            })

    write_cache("tiktok_trends", trends)
    return trends


def discover_all_trends() -> list:
    """Run all trend discovery sources and merge results."""
    print("\n[1/5] TREND DISCOVERY")
    print("=" * 50)

    all_trends = []

    print("  Fetching Google Trends...")
    gt = fetch_google_trends()
    print(f"    -> {len(gt)} signals")
    all_trends.extend(gt)

    print("  Fetching Reddit hot posts...")
    rd = fetch_reddit_trends()
    print(f"    -> {len(rd)} signals")
    all_trends.extend(rd)

    print("  Fetching YouTube trending...")
    yt = fetch_youtube_trending()
    print(f"    -> {len(yt)} signals")
    all_trends.extend(yt)

    print("  Fetching TikTok trends...")
    tt = fetch_tiktok_trends()
    print(f"    -> {len(tt)} signals")
    all_trends.extend(tt)

    print(f"\n  TOTAL TREND SIGNALS: {len(all_trends)}")
    return all_trends


# ---------------------------------------------------------------------------
# 2. Trend Clustering
# ---------------------------------------------------------------------------

def cluster_trends(trends: list) -> list:
    """Group related trends into clusters, rank by engagement velocity."""
    print("\n[2/5] TREND CLUSTERING")
    print("=" * 50)

    # Simple keyword-based clustering
    clusters = {}
    app_keywords = [
        "ai", "app", "fitness", "health", "sleep", "habit", "prayer",
        "meditation", "budget", "money", "crypto", "tracker", "journal",
        "workout", "diet", "fasting", "calm", "focus", "productivity",
        "learn", "language", "quiz", "game", "photo", "video", "music",
        "cook", "meal", "recipe", "water", "mood", "mental", "anxiety",
        "dating", "social", "chat", "voice", "timer", "alarm", "reminder",
        "clean", "organize", "declutter", "pet", "plant", "garden",
        "travel", "weather", "news", "read", "book", "podcast",
        "draw", "art", "design", "code", "build", "ship",
    ]

    for trend in trends:
        term = trend.get("term", "").lower()
        matched_kw = None
        for kw in app_keywords:
            if kw in term:
                matched_kw = kw
                break

        if not matched_kw:
            # Use first significant word as cluster key
            words = re.findall(r'[a-z]{3,}', term)
            matched_kw = words[0] if words else "misc"

        if matched_kw not in clusters:
            clusters[matched_kw] = {
                "keyword": matched_kw,
                "trends": [],
                "total_score": 0,
                "total_velocity": 0,
                "sources": set(),
            }

        clusters[matched_kw]["trends"].append(trend)
        clusters[matched_kw]["total_score"] += trend.get("score", 0)
        clusters[matched_kw]["total_velocity"] += trend.get("velocity", trend.get("score", 0))
        clusters[matched_kw]["sources"].add(trend.get("source", "unknown").split("_")[0])

    # Convert sets to lists for serialization and sort by velocity
    result = []
    for key, cluster in clusters.items():
        cluster["sources"] = list(cluster["sources"])
        cluster["trend_count"] = len(cluster["trends"])
        cluster["avg_score"] = cluster["total_score"] / max(cluster["trend_count"], 1)
        cluster["multi_source"] = len(cluster["sources"]) > 1
        result.append(cluster)

    result.sort(key=lambda c: (c["multi_source"], c["total_velocity"]), reverse=True)

    print(f"  Formed {len(result)} clusters from {len(trends)} signals")
    for c in result[:10]:
        src_str = ", ".join(c["sources"][:3])
        print(f"    [{c['keyword']:15s}] {c['trend_count']:3d} signals | vel={c['total_velocity']:6.0f} | sources: {src_str}")

    return result[:25]  # top 25 clusters


# ---------------------------------------------------------------------------
# 3. App Gap Identification (iTunes Search API)
# ---------------------------------------------------------------------------

def search_app_store(query: str, limit: int = 10) -> list:
    """Search App Store via iTunes Search API (free, no auth)."""
    encoded = urllib.parse.quote(query)
    url = f"https://itunes.apple.com/search?term={encoded}&entity=software&limit={limit}&country=us"
    raw = fetch_url(url)
    if not raw:
        return []
    try:
        data = json.loads(raw)
        results = []
        for app in data.get("results", []):
            results.append({
                "name": app.get("trackName", ""),
                "developer": app.get("artistName", ""),
                "rating": app.get("averageUserRating", 0),
                "reviews": app.get("userRatingCount", 0),
                "price": app.get("price", 0),
                "category": app.get("primaryGenreName", ""),
                "url": app.get("trackViewUrl", ""),
            })
        return results
    except (json.JSONDecodeError, KeyError):
        return []


def identify_gaps(clusters: list) -> list:
    """For each trend cluster, search App Store and flag gaps."""
    print("\n[3/5] APP GAP IDENTIFICATION")
    print("=" * 50)

    gap_results = []
    for cluster in clusters[:15]:
        kw = cluster["keyword"]
        query = f"{kw} app"
        apps = search_app_store(query, limit=10)

        high_review_apps = [a for a in apps if a.get("reviews", 0) >= 1000]
        low_review_apps = [a for a in apps if a.get("reviews", 0) < 1000]
        avg_rating = sum(a.get("rating", 0) for a in apps) / max(len(apps), 1)

        has_gap = len(high_review_apps) < 3  # fewer than 3 strong competitors
        opportunity_score = 0
        if has_gap:
            opportunity_score += 40
        if cluster["multi_source"]:
            opportunity_score += 20
        if cluster["total_velocity"] > 50:
            opportunity_score += 20
        if avg_rating < 4.0 and apps:
            opportunity_score += 20  # room for improvement

        gap_results.append({
            "cluster": kw,
            "trend_count": cluster["trend_count"],
            "velocity": cluster["total_velocity"],
            "multi_source": cluster["multi_source"],
            "existing_apps": len(apps),
            "strong_competitors": len(high_review_apps),
            "weak_competitors": len(low_review_apps),
            "avg_rating": round(avg_rating, 1),
            "has_gap": has_gap,
            "opportunity_score": opportunity_score,
            "top_apps": [a["name"] for a in apps[:3]],
        })

        status = "GAP FOUND" if has_gap else "saturated"
        print(f"  [{kw:15s}] {len(apps):2d} apps | {len(high_review_apps)} strong | rating={avg_rating:.1f} | {status} | opp={opportunity_score}")
        time.sleep(0.3)  # rate limit

    gap_results.sort(key=lambda g: g["opportunity_score"], reverse=True)
    return gap_results


# ---------------------------------------------------------------------------
# 4. App Idea Generation & Scoring
# ---------------------------------------------------------------------------

def generate_app_name(keyword: str) -> str:
    """Generate an insider-sounding app name (not AI-slop)."""
    # Method: combine keyword-derived fragment with a suffix
    # Goal: sounds like it came from within the niche community
    prefix_pool = NAME_FRAGMENTS["prefixes"]
    suffix_pool = NAME_FRAGMENTS["suffixes"]

    # Try to use the keyword itself as part of the name
    kw_short = keyword[:4].lower()
    options = [
        f"{kw_short}{random.choice(suffix_pool)}",
        f"{random.choice(prefix_pool)}{kw_short}",
        f"{kw_short}.{random.choice(suffix_pool)}",
        f"{random.choice(prefix_pool)}{random.choice(suffix_pool)}",
        f"{kw_short}rr",
        f"the{kw_short}",
    ]

    name = random.choice(options)
    # Capitalize first letter only (insider style, not CamelCase)
    return name[0].upper() + name[1:]


def score_idea(description: str, gap_data: dict = None) -> dict:
    """Score an app idea on 4 dimensions (1-5 each). Total threshold: 16/20."""
    desc_lower = description.lower()

    # --- vibe_codeability (can it be built in <24h with AI tools?) ---
    vibe = 3  # baseline
    simple_signals = ["tracker", "timer", "counter", "list", "log", "journal",
                      "calculator", "quiz", "reminder", "habit", "mood",
                      "water", "fasting", "prayer", "step", "streak"]
    complex_signals = ["social network", "marketplace", "real-time multiplayer",
                       "video editing", "ar/vr", "blockchain", "hardware"]
    if any(s in desc_lower for s in simple_signals):
        vibe += 1
    if "pwa" in desc_lower or "web app" in desc_lower:
        vibe += 1
    if any(s in desc_lower for s in complex_signals):
        vibe -= 2
    vibe = max(1, min(5, vibe))

    # --- trend_fit (how well does it match trending topics?) ---
    trend = 3  # baseline
    hot_topics = ["ai", "ramadan", "fitness", "sleep", "fasting", "meditation",
                  "budget", "mental health", "prayer", "productivity", "focus",
                  "habit", "gratitude", "journaling", "walking", "reading"]
    matches = sum(1 for t in hot_topics if t in desc_lower)
    trend = min(5, 2 + matches)
    if gap_data and gap_data.get("multi_source"):
        trend = min(5, trend + 1)

    # --- monetization (clear revenue model?) ---
    money = 3  # baseline
    money_signals = ["subscription", "premium", "pro", "affiliate", "ads",
                     "in-app", "purchase", "freemium", "paywall"]
    health_signals = ["fitness", "health", "sleep", "diet", "workout",
                      "meditation", "fasting", "prayer", "wellness"]
    if any(s in desc_lower for s in money_signals):
        money += 1
    if any(s in desc_lower for s in health_signals):
        money += 1  # health/wellness = proven subscription market
    money = max(1, min(5, money))

    # --- virality (would someone share this on TikTok?) ---
    viral = 2  # baseline (most apps are not inherently viral)
    viral_signals = ["streak", "challenge", "share", "leaderboard", "social",
                     "photo", "before after", "progress", "transformation",
                     "daily", "100 days", "screenshot", "widget"]
    visual_signals = ["beautiful", "aesthetic", "minimal", "dark mode",
                      "animation", "chart", "graph", "visual"]
    viral_matches = sum(1 for v in viral_signals if v in desc_lower)
    visual_matches = sum(1 for v in visual_signals if v in desc_lower)
    viral = min(5, 2 + viral_matches + visual_matches)

    if gap_data:
        opp = gap_data.get("opportunity_score", 0)
        if opp >= 60:
            trend = min(5, trend + 1)
        if gap_data.get("has_gap"):
            money = min(5, money + 1)

    total = vibe + trend + money + viral
    passes = total >= SCORE_THRESHOLD

    return {
        "vibe_codeability": vibe,
        "trend_fit": trend,
        "monetization": money,
        "virality": viral,
        "total": total,
        "passes_threshold": passes,
    }


def generate_ideas(gaps: list, clusters: list) -> list:
    """Generate app ideas from gap analysis and trend clusters."""
    print("\n[4/5] APP IDEA GENERATION & SCORING")
    print("=" * 50)

    ideas = []

    # Generate ideas from top gaps
    for gap in gaps[:12]:
        kw = gap["cluster"]
        name = generate_app_name(kw)
        description = f"{kw} tracker and daily companion app with streak system and progress visualization"

        # Build a more specific description based on keyword
        feature_map = {
            "fitness": "Daily workout logger with rep counting and progress photos",
            "sleep": "Sleep quality tracker with smart alarm and wind-down routines",
            "habit": "Streak-based habit tracker with accountability partner matching",
            "prayer": "Prayer time tracker with Qibla compass and community streaks",
            "meditation": "Guided breathwork timer with session streaks and mood logging",
            "budget": "Daily expense tracker with spending challenges and visual breakdowns",
            "fasting": "Intermittent fasting timer with streak tracking and body metrics",
            "mood": "Daily mood check-in with pattern detection and journal prompts",
            "water": "Hydration tracker with plant-growing gamification",
            "focus": "Pomodoro timer with app-blocking and deep work streaks",
            "meal": "Meal prep planner with grocery list generation and macro tracking",
            "learn": "Micro-learning quiz app with spaced repetition and daily streaks",
            "journal": "Daily journaling app with AI prompts and mood correlation",
            "workout": "Gym workout tracker with progressive overload calculator",
        }

        core_feature = feature_map.get(kw, f"{kw.title()} tracking with streaks and progress visualization")
        pitch = f"the {kw} app that actually sticks. streaks, not willpower."

        scores = score_idea(description + " " + core_feature, gap)

        tech_stack = random.choice(TECH_STACKS)
        revenue_model = random.choice(REVENUE_MODELS[:4])  # prefer subscription models
        build_time = "8-16 hours" if scores["vibe_codeability"] >= 4 else "16-24 hours"

        tiktok_hooks = [
            f"I built a {kw} app in one day. here's what happened.",
            f"this {kw} app was made by someone who actually {kw}s. you can tell.",
            f"day 1 of using my own {kw} app. the streak starts now.",
            f"POV: you built the {kw} app you always wanted",
            f"I asked 100 people what they hate about {kw} apps. then I fixed it.",
        ]

        idea = {
            "app_name": name,
            "pitch": pitch,
            "core_feature": core_feature,
            "tech_stack": tech_stack,
            "tiktok_hook": random.choice(tiktok_hooks),
            "build_time": build_time,
            "revenue_model": revenue_model,
            "cluster_keyword": kw,
            "opportunity_score": gap["opportunity_score"],
            "existing_competitors": gap["strong_competitors"],
            "avg_competitor_rating": gap["avg_rating"],
            "top_existing_apps": gap.get("top_apps", []),
            **scores,
        }
        ideas.append(idea)

    # Sort by total score descending
    ideas.sort(key=lambda i: (i["total"], i["opportunity_score"]), reverse=True)

    passing = [i for i in ideas if i["passes_threshold"]]
    print(f"\n  Generated {len(ideas)} ideas | {len(passing)} pass threshold ({SCORE_THRESHOLD}/20)")

    for i, idea in enumerate(ideas[:10], 1):
        status = "PASS" if idea["passes_threshold"] else "FAIL"
        print(f"  {i:2d}. [{status}] {idea['app_name']:15s} | "
              f"V={idea['vibe_codeability']} T={idea['trend_fit']} "
              f"M={idea['monetization']} R={idea['virality']} "
              f"| total={idea['total']}/20 | opp={idea['opportunity_score']}")

    return ideas


# ---------------------------------------------------------------------------
# 5. Output Generation
# ---------------------------------------------------------------------------

def write_results_csv(ideas: list):
    """Write ideas to LEDGER/APP_IDEATION_RESULTS.csv."""
    path = safe_path(RESULTS_CSV)
    fieldnames = [
        "scan_date", "app_name", "pitch", "core_feature", "tech_stack",
        "tiktok_hook", "build_time", "revenue_model", "cluster_keyword",
        "vibe_codeability", "trend_fit", "monetization", "virality",
        "total_score", "passes_threshold", "opportunity_score",
        "existing_competitors", "avg_competitor_rating",
    ]

    file_exists = path.exists()
    with open(path, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        for idea in ideas:
            writer.writerow({
                "scan_date": TODAY,
                "app_name": idea["app_name"],
                "pitch": idea["pitch"],
                "core_feature": idea["core_feature"],
                "tech_stack": idea["tech_stack"],
                "tiktok_hook": idea["tiktok_hook"],
                "build_time": idea["build_time"],
                "revenue_model": idea["revenue_model"],
                "cluster_keyword": idea["cluster_keyword"],
                "vibe_codeability": idea["vibe_codeability"],
                "trend_fit": idea["trend_fit"],
                "monetization": idea["monetization"],
                "virality": idea["virality"],
                "total_score": idea["total"],
                "passes_threshold": idea["passes_threshold"],
                "opportunity_score": idea["opportunity_score"],
                "existing_competitors": idea["existing_competitors"],
                "avg_competitor_rating": idea["avg_competitor_rating"],
            })

    print(f"  -> Wrote {len(ideas)} ideas to {path}")


def write_alpha_staging(ideas: list):
    """Append high-scoring ideas to ALPHA_STAGING.csv as APP_FACTORY category."""
    passing = [i for i in ideas if i["passes_threshold"]]
    if not passing:
        print("  -> No ideas passed threshold for ALPHA_STAGING")
        return

    path = safe_path(ALPHA_CSV)
    if not path.exists():
        print(f"  [WARN] ALPHA_STAGING.csv not found at {path}. Skipping alpha append.")
        return

    # Read header to match format
    with open(path, "r") as f:
        reader = csv.reader(f)
        header = next(reader, None)

    if not header:
        print("  [WARN] ALPHA_STAGING.csv has no header. Skipping.")
        return

    with open(path, "a", newline="") as f:
        writer = csv.writer(f)
        for idea in passing[:5]:  # top 5 only
            alpha_id = next_alpha_id()
            row = [""] * len(header)
            # Map fields to known column positions by name
            col_map = {h: i for i, h in enumerate(header)}
            if "alpha_id" in col_map:
                row[col_map["alpha_id"]] = alpha_id
            if "source" in col_map:
                row[col_map["source"]] = "App Ideation Specialist"
            if "category" in col_map:
                row[col_map["category"]] = "APP_FACTORY"
            if "tactic" in col_map:
                row[col_map["tactic"]] = f"{idea['app_name']}: {idea['pitch']}"
            if "roi_potential" in col_map:
                row[col_map["roi_potential"]] = "HIGH" if idea["total"] >= 18 else "MEDIUM"
            if "priority" in col_map:
                row[col_map["priority"]] = "HIGH"
            if "status" in col_map:
                row[col_map["status"]] = "PENDING_REVIEW"
            if "created_at" in col_map:
                row[col_map["created_at"]] = TODAY
            if "reviewer_notes" in col_map:
                row[col_map["reviewer_notes"]] = (
                    f"Auto-generated by app_ideation_specialist.py. "
                    f"Score: {idea['total']}/20. Opp: {idea['opportunity_score']}. "
                    f"Stack: {idea['tech_stack'][:40]}. Build: {idea['build_time']}."
                )
            writer.writerow(row)

    print(f"  -> Appended {min(len(passing), 5)} ideas to ALPHA_STAGING.csv")


def generate_markdown_report(ideas: list, trends: list, clusters: list, gaps: list) -> str:
    """Generate a full markdown report."""
    passing = [i for i in ideas if i["passes_threshold"]]
    report_path = safe_path(OPS_DIR / f"APP_IDEATION_REPORT_{TODAY}.md")

    lines = [
        f"# App Ideation Report - {TODAY}",
        "",
        f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"**Trend signals:** {len(trends)}",
        f"**Clusters formed:** {len(clusters)}",
        f"**Gaps analyzed:** {len(gaps)}",
        f"**Ideas generated:** {len(ideas)}",
        f"**Ideas passing threshold ({SCORE_THRESHOLD}/20):** {len(passing)}",
        "",
        "---",
        "",
        "## Top Passing Ideas",
        "",
    ]

    for i, idea in enumerate(passing[:10], 1):
        lines.extend([
            f"### {i}. {idea['app_name']}",
            "",
            f"**Pitch:** {idea['pitch']}",
            f"**Core feature:** {idea['core_feature']}",
            f"**Tech stack:** {idea['tech_stack']}",
            f"**Build time:** {idea['build_time']}",
            f"**Revenue model:** {idea['revenue_model']}",
            f"**TikTok hook:** \"{idea['tiktok_hook']}\"",
            "",
            f"| Dimension | Score |",
            f"|-----------|-------|",
            f"| Vibe-codeability | {idea['vibe_codeability']}/5 |",
            f"| Trend fit | {idea['trend_fit']}/5 |",
            f"| Monetization | {idea['monetization']}/5 |",
            f"| Virality | {idea['virality']}/5 |",
            f"| **Total** | **{idea['total']}/20** |",
            "",
            f"**Market context:** {idea['existing_competitors']} strong competitors, "
            f"avg rating {idea['avg_competitor_rating']}/5. "
            f"Opportunity score: {idea['opportunity_score']}/100.",
            "",
            f"**Existing apps:** {', '.join(idea.get('top_existing_apps', [])[:3]) or 'none found'}",
            "",
        ])

    # Trend clusters summary
    lines.extend([
        "---",
        "",
        "## Trend Cluster Summary",
        "",
        "| Cluster | Signals | Velocity | Multi-source | Sources |",
        "|---------|---------|----------|-------------|---------|",
    ])
    for c in clusters[:15]:
        ms = "yes" if c.get("multi_source") else "no"
        src = ", ".join(c.get("sources", [])[:3])
        lines.append(
            f"| {c['keyword']} | {c['trend_count']} | {c['total_velocity']:.0f} | {ms} | {src} |"
        )

    # Gap analysis summary
    lines.extend([
        "",
        "## Gap Analysis",
        "",
        "| Keyword | Apps Found | Strong | Gap? | Opp Score | Avg Rating |",
        "|---------|-----------|--------|------|-----------|------------|",
    ])
    for g in gaps[:15]:
        gap_str = "YES" if g["has_gap"] else "no"
        lines.append(
            f"| {g['cluster']} | {g['existing_apps']} | {g['strong_competitors']} "
            f"| {gap_str} | {g['opportunity_score']} | {g['avg_rating']} |"
        )

    # Ideas that didn't pass
    failing = [i for i in ideas if not i["passes_threshold"]]
    if failing:
        lines.extend([
            "",
            "## Ideas Below Threshold (for reference)",
            "",
        ])
        for idea in failing[:5]:
            lines.append(
                f"- **{idea['app_name']}** ({idea['cluster_keyword']}): "
                f"{idea['total']}/20 "
                f"(V={idea['vibe_codeability']} T={idea['trend_fit']} "
                f"M={idea['monetization']} R={idea['virality']})"
            )

    lines.extend([
        "",
        "---",
        "",
        f"*Generated by `app_ideation_specialist.py` on {datetime.now().isoformat()}*",
    ])

    report_content = "\n".join(lines)
    with open(report_path, "w") as f:
        f.write(report_content)

    print(f"  -> Report written to {report_path}")
    return str(report_path)


# ---------------------------------------------------------------------------
# CLI commands
# ---------------------------------------------------------------------------

def cmd_scan():
    """Full scan: trends + gaps + scoring + output."""
    print("\nPRINTMAXX APP IDEATION SPECIALIST")
    print("=" * 60)
    print(f"Date: {TODAY}")
    print(f"Threshold: {SCORE_THRESHOLD}/20")
    ensure_dirs()

    # Load context
    clones = load_existing_clones()
    context = load_discovery_context()
    if clones:
        print(f"\n  Loaded {len(clones)} existing clone opportunities for cross-reference")
    if context:
        print(f"  Loaded APP_DISCOVERY_ENGINE.md context ({len(context)} chars)")

    # 1. Discover trends
    trends = discover_all_trends()

    # 2. Cluster
    clusters = cluster_trends(trends)

    # 3. Identify gaps
    gaps = identify_gaps(clusters)

    # 4. Generate and score ideas
    ideas = generate_ideas(gaps, clusters)

    # 5. Output
    print("\n[5/5] OUTPUT GENERATION")
    print("=" * 50)
    write_results_csv(ideas)
    write_alpha_staging(ideas)
    report_path = generate_markdown_report(ideas, trends, clusters, gaps)

    passing = [i for i in ideas if i["passes_threshold"]]
    print(f"\n{'=' * 60}")
    print(f"SCAN COMPLETE")
    print(f"  Total ideas: {len(ideas)}")
    print(f"  Passing ideas: {len(passing)}")
    print(f"  Results CSV: {RESULTS_CSV}")
    print(f"  Report: {report_path}")
    print(f"  Alpha staging: {len(min(passing, key=lambda x: 1) and passing[:5])} entries appended" if passing else "  No ideas passed threshold")
    print(f"{'=' * 60}\n")

    # Save scan state for --status
    state = {
        "last_scan": TODAY,
        "last_scan_time": datetime.now().isoformat(),
        "trends_count": len(trends),
        "clusters_count": len(clusters),
        "gaps_count": len(gaps),
        "ideas_count": len(ideas),
        "passing_count": len(passing),
        "report_path": report_path,
    }
    write_cache("last_scan_state", state)


def cmd_trends_only():
    """Fetch and display trends without scoring."""
    print("\nPRINTMAXX TREND SCANNER (trends only)")
    print("=" * 60)
    ensure_dirs()

    trends = discover_all_trends()
    clusters = cluster_trends(trends)

    print("\n\nTOP TREND CLUSTERS:")
    print("-" * 60)
    for i, c in enumerate(clusters[:20], 1):
        ms = " [MULTI-SOURCE]" if c.get("multi_source") else ""
        print(f"  {i:2d}. {c['keyword']:15s} | {c['trend_count']:3d} signals | "
              f"vel={c['total_velocity']:6.0f}{ms}")
        # Show sample trends
        for t in c["trends"][:2]:
            term = t["term"][:60]
            print(f"      -> {term}")


def cmd_score_idea(description: str):
    """Score a manually provided idea."""
    print(f"\nSCORING IDEA: \"{description}\"")
    print("=" * 60)

    scores = score_idea(description)
    print(f"\n  Vibe-codeability: {scores['vibe_codeability']}/5")
    print(f"  Trend fit:        {scores['trend_fit']}/5")
    print(f"  Monetization:     {scores['monetization']}/5")
    print(f"  Virality:         {scores['virality']}/5")
    print(f"  -------------------------")
    print(f"  TOTAL:            {scores['total']}/20")
    print(f"  Threshold:        {SCORE_THRESHOLD}/20")
    print(f"  Status:           {'PASS' if scores['passes_threshold'] else 'FAIL'}")

    if scores["passes_threshold"]:
        name = generate_app_name(description.split()[0] if description.split() else "app")
        print(f"\n  Suggested name:   {name}")
        print(f"  Tech stack:       {random.choice(TECH_STACKS)}")
        print(f"  Revenue model:    {random.choice(REVENUE_MODELS[:4])}")
        build = "8-16 hours" if scores["vibe_codeability"] >= 4 else "16-24 hours"
        print(f"  Est. build time:  {build}")


def cmd_status():
    """Show last scan results."""
    ensure_dirs()
    state = read_cache("last_scan_state")

    print("\nAPP IDEATION SPECIALIST - STATUS")
    print("=" * 60)

    if not state:
        print("  No scan data found. Run --scan first.")
        print(f"  Cache dir: {CACHE_DIR}")
        print(f"  Results CSV: {RESULTS_CSV} ({'exists' if RESULTS_CSV.exists() else 'not found'})")
        return

    print(f"  Last scan:       {state.get('last_scan', 'unknown')}")
    print(f"  Scan time:       {state.get('last_scan_time', 'unknown')}")
    print(f"  Trends found:    {state.get('trends_count', 0)}")
    print(f"  Clusters formed: {state.get('clusters_count', 0)}")
    print(f"  Gaps analyzed:   {state.get('gaps_count', 0)}")
    print(f"  Ideas generated: {state.get('ideas_count', 0)}")
    print(f"  Passing ideas:   {state.get('passing_count', 0)}")
    print(f"  Report:          {state.get('report_path', 'n/a')}")
    print(f"  Results CSV:     {RESULTS_CSV} ({'exists' if RESULTS_CSV.exists() else 'not found'})")

    # Show recent results if available
    if RESULTS_CSV.exists():
        print(f"\n  Latest entries in {RESULTS_CSV.name}:")
        try:
            with open(RESULTS_CSV, "r") as f:
                reader = csv.DictReader(f)
                rows = list(reader)
                for row in rows[-5:]:
                    status = "PASS" if row.get("passes_threshold") == "True" else "FAIL"
                    print(f"    [{status}] {row.get('app_name', '?'):15s} | "
                          f"score={row.get('total_score', '?')}/20 | "
                          f"{row.get('scan_date', '?')}")
        except Exception:
            pass


def cmd_top(n: int):
    """Show top N ideas from last scan."""
    print(f"\nTOP {n} APP IDEAS")
    print("=" * 60)

    if not RESULTS_CSV.exists():
        print("  No results found. Run --scan first.")
        return

    try:
        with open(RESULTS_CSV, "r") as f:
            reader = csv.DictReader(f)
            rows = list(reader)
    except Exception as e:
        print(f"  Error reading results: {e}")
        return

    if not rows:
        print("  Results file is empty. Run --scan first.")
        return

    # Sort by total score descending, take top N
    rows.sort(key=lambda r: int(r.get("total_score", 0)), reverse=True)

    for i, row in enumerate(rows[:n], 1):
        passes = "PASS" if row.get("passes_threshold") == "True" else "FAIL"
        print(f"\n  {i}. [{passes}] {row.get('app_name', '?')}")
        print(f"     Pitch:    {row.get('pitch', '?')}")
        print(f"     Feature:  {row.get('core_feature', '?')}")
        print(f"     Stack:    {row.get('tech_stack', '?')}")
        print(f"     Revenue:  {row.get('revenue_model', '?')}")
        print(f"     Build:    {row.get('build_time', '?')}")
        print(f"     TikTok:   \"{row.get('tiktok_hook', '?')}\"")
        print(f"     Score:    {row.get('total_score', '?')}/20 "
              f"(V={row.get('vibe_codeability', '?')} "
              f"T={row.get('trend_fit', '?')} "
              f"M={row.get('monetization', '?')} "
              f"R={row.get('virality', '?')})")
        print(f"     Market:   {row.get('existing_competitors', '?')} strong competitors, "
              f"avg rating {row.get('avg_competitor_rating', '?')}/5")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="PRINTMAXX App Ideation Specialist - discover viral trends, match to vibe-codeable app ideas",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --scan                  Full scan (trends + gaps + scoring)
  %(prog)s --trends-only           Just fetch and display trends
  %(prog)s --score-idea "habit tracker with social accountability"
  %(prog)s --status                Show last scan results
  %(prog)s --top 5                 Show top 5 ideas from last scan
        """,
    )

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--scan", action="store_true", help="Full scan: trends + gaps + scoring + output")
    group.add_argument("--trends-only", action="store_true", help="Just fetch and display trends")
    group.add_argument("--score-idea", type=str, metavar="DESC", help="Score a manually provided app idea")
    group.add_argument("--status", action="store_true", help="Show last scan results")
    group.add_argument("--top", type=int, metavar="N", help="Show top N ideas from last scan")

    args = parser.parse_args()

    try:
        if args.scan:
            cmd_scan()
        elif args.trends_only:
            cmd_trends_only()
        elif args.score_idea:
            cmd_score_idea(args.score_idea)
        elif args.status:
            cmd_status()
        elif args.top:
            cmd_top(args.top)
    except KeyboardInterrupt:
        print("\n\nInterrupted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n[ERROR] {e}")
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
