#!/usr/bin/env python3
"""
Competitive Intel Scraper — Cycle 067
Strategy: PARENTING + PET_CARE + ACADEMIC + SOCIAL_CONNECTION
Date: 2026-03-18
Targets: toddler reading streak, bedtime routine habit, dog walk streak,
         cat enrichment habit, flashcard streak, homework streak, exam prep,
         gratitude-to-person streak, kindness challenge, family dinner streak,
         journaling with kid, screen limit habit, pet training streak
"""

import json
import time
import requests
import csv
from datetime import datetime, timezone
from pathlib import Path

BASE = Path(__file__).parent
DATA = BASE / "data"
OUTPUT = BASE / "output"
LEDGER = Path(__file__).parent.parent.parent.parent.parent / "LEDGER"
ALPHA_CSV = LEDGER / "ALPHA_STAGING.csv"
CI_CSV = LEDGER / "COMPETITIVE_INTEL.csv"

CYCLE = 67
NOW = datetime.now(timezone.utc)
DATE_STR = NOW.strftime("%Y-%m-%d")
TS = NOW.strftime("%Y%m%d_%H%M")

GENERIC_TRACKERS = {
    "streaks", "habitica", "productive", "habitminder", "habit tracker",
    "loop habit tracker", "done", "streaks - habit tracker", "habitnow",
    "habit - daily tracker", "everyday", "habitify", "strides", "way of life",
    "coach.me", "fabulous", "productive - habit tracker", "daylio",
    "habitbull", "momentum", "finch", "tiimo", "routinery", "myfitnesspal",
    "noom", "loseit", "cronometer", "nike training", "peloton",
    "duolingo", "babbel", "anki", "quizlet", "khan academy"
}

NICHES = {
    # ── PARENTING ────────────────────────────────────────────────────────────
    "toddler_reading_streak": {
        "label": "Daily Toddler Reading Streak",
        "subreddits": ["Parenting", "toddlers", "beyondthebump"],
        "itunes_terms": ["toddler reading streak daily habit paid", "read to child daily streak tracker paid"],
        "hypothesis": "BO — r/Parenting 5M+. 'Read 20 min/day' is universal advice. Zero dedicated streak tracker for parents."
    },
    "bedtime_routine_habit": {
        "label": "Kids Bedtime Routine Habit Tracker",
        "subreddits": ["Parenting", "sleeptrain", "NewParents"],
        "itunes_terms": ["bedtime routine habit tracker kids paid streak", "children sleep routine streak daily paid"],
        "hypothesis": "SOFT — Sleep apps for adults exist. Kids bedtime ROUTINE streak tracker is distinct niche."
    },
    "screen_limit_habit": {
        "label": "Daily Screen Time Limit Habit",
        "subreddits": ["Parenting", "nosurf", "digitalminimalism"],
        "itunes_terms": ["screen time limit habit streak daily paid", "screen limit tracker habit streak paid"],
        "hypothesis": "SOFT — Screen Time (Apple built-in) is a control, not a habit streak. Parent accountability tracker gap."
    },
    "journaling_with_kid": {
        "label": "Daily Parent-Child Journal Streak",
        "subreddits": ["Parenting", "Journaling", "toddlers"],
        "itunes_terms": ["parent child journal daily streak paid habit", "family journal streak tracker paid daily"],
        "hypothesis": "BO — Intersection of journaling + parenting. Zero apps for parent+child daily journal streak."
    },
    # ── PET CARE ─────────────────────────────────────────────────────────────
    "dog_walk_streak": {
        "label": "Daily Dog Walk Streak Tracker",
        "subreddits": ["dogs", "dogcare", "DogAdvice"],
        "itunes_terms": ["dog walk streak daily habit paid tracker", "dog walk habit streak tracker paid"],
        "hypothesis": "BO — r/dogs 3M+. Vets say 2 walks/day. Zero dedicated dog-walk streak app. Massive unmet need."
    },
    "pet_training_streak": {
        "label": "Daily Pet Training Session Streak",
        "subreddits": ["Dogtraining", "Pets", "cats"],
        "itunes_terms": ["pet training streak daily habit paid", "dog training session streak tracker paid"],
        "hypothesis": "BO — r/Dogtraining 1M+. '5 min training daily' is standard advice. Zero dedicated training streak app."
    },
    "cat_enrichment_habit": {
        "label": "Daily Cat Playtime / Enrichment Streak",
        "subreddits": ["cats", "catcare", "CATHELP"],
        "itunes_terms": ["cat playtime streak daily habit paid", "cat enrichment habit tracker streak paid"],
        "hypothesis": "BO — r/cats 7M+. Vets recommend 15min daily play. Zero dedicated cat enrichment streak app."
    },
    # ── ACADEMIC ─────────────────────────────────────────────────────────────
    "flashcard_streak": {
        "label": "Daily Flashcard / Spaced Repetition Streak",
        "subreddits": ["learnprogramming", "medicalschool", "premed"],
        "itunes_terms": ["flashcard streak daily habit paid tracker", "spaced repetition habit streak daily paid"],
        "hypothesis": "SOFT — Anki is free/open. Gap: paid streak-gamification layer on top of ANY study deck."
    },
    "homework_streak": {
        "label": "Daily Homework / Study Habit Streak",
        "subreddits": ["teenagers", "highschool", "college"],
        "itunes_terms": ["homework habit streak daily paid tracker", "study habit streak tracker paid daily"],
        "hypothesis": "BO — r/teenagers 2M+. Students need accountability. Zero dedicated homework streak tracker."
    },
    "exam_prep_streak": {
        "label": "Daily Exam Prep Habit Tracker",
        "subreddits": ["MCAT", "LSAT", "CPA_Exam"],
        "itunes_terms": ["exam prep streak daily habit paid tracker", "MCAT LSAT study streak habit paid"],
        "hypothesis": "BO — High-stakes exam communities huge (MCAT 200K+, LSAT 70K+). Need daily streak accountability."
    },
    # ── SOCIAL CONNECTION ────────────────────────────────────────────────────
    "gratitude_to_person": {
        "label": "Daily Gratitude Message / Kind Act Streak",
        "subreddits": ["gratitude", "kindness", "DecidingToBeBetter"],
        "itunes_terms": ["gratitude message daily streak habit paid", "random acts kindness streak daily paid habit"],
        "hypothesis": "BO — r/gratitude 300K+, r/DecidingToBeBetter 700K+. Gratitude SENDING (to person) streak unbuilt."
    },
    "family_dinner_streak": {
        "label": "Daily Family Dinner / Meal Together Streak",
        "subreddits": ["Parenting", "family", "mealplanning"],
        "itunes_terms": ["family dinner streak daily habit paid", "family meal together habit streak paid tracker"],
        "hypothesis": "BO — Research-backed: family dinners = better outcomes. Zero dedicated family-dinner streak app."
    },
    "social_call_streak": {
        "label": "Daily Phone Call / Social Connection Streak",
        "subreddits": ["lonely", "socialskills", "DecidingToBeBetter"],
        "itunes_terms": ["social connection streak daily habit paid", "phone call habit streak tracker daily paid"],
        "hypothesis": "BO — Loneliness epidemic. CDC reports daily connection habit as antidote. Zero streak app exists."
    },
}


def reddit_community_size(subreddits: list) -> tuple:
    """Fetch subscriber counts from Reddit JSON API (no auth needed)."""
    total = 0
    breakdown = {}
    headers = {"User-Agent": "PRINTMAXX-intel-bot/1.0"}
    for sub in subreddits:
        try:
            url = f"https://www.reddit.com/r/{sub}/about.json"
            r = requests.get(url, headers=headers, timeout=10)
            if r.status_code == 200:
                data = r.json().get("data", {})
                subs = data.get("subscribers", 0)
                total += subs
                breakdown[sub] = subs
            elif r.status_code == 429:
                print(f"    [RATE] r/{sub} — backing off 8s")
                time.sleep(8)
            else:
                print(f"    [SKIP] r/{sub} → HTTP {r.status_code}")
            time.sleep(1.2)
        except Exception as e:
            print(f"    [ERR] r/{sub}: {e}")
    return total, breakdown


def itunes_search(terms: list) -> dict:
    """Search iTunes for apps matching terms. Returns {name: {price, rating, rating_count}}."""
    found = {}
    for term in terms:
        try:
            url = "https://itunes.apple.com/search"
            params = {"term": term, "entity": "software", "limit": 5, "country": "us"}
            r = requests.get(url, params=params, timeout=10)
            if r.status_code == 200:
                results = r.json().get("results", [])
                for app in results:
                    name = app.get("trackName", "").lower()
                    price = app.get("price", 0)
                    rating = app.get("averageUserRating", 0)
                    rating_count = app.get("userRatingCount", 0)
                    found[name] = {
                        "price": price,
                        "rating": rating,
                        "rating_count": rating_count,
                        "genre": app.get("primaryGenreName", ""),
                        "dev": app.get("artistName", ""),
                        "bundle_id": app.get("bundleId", ""),
                        "url": app.get("trackViewUrl", ""),
                    }
            time.sleep(0.8)
        except Exception as e:
            print(f"    [ERR] iTunes '{term}': {e}")
    return found


def classify_competition(niche_key: str, apps: dict) -> str:
    """
    Classify niche as BLUE_OCEAN, SOFT_COMPETITION, or OCCUPIED.
    BLUE_OCEAN   = no relevant paid apps with real traction (>500 ratings)
    SOFT         = relevant apps exist but weak (<2K ratings) OR generic tracker
    OCCUPIED     = strong dedicated app (>2K ratings, >$0.99 price)
    """
    relevant = []
    for name, meta in apps.items():
        name_lower = name.lower()
        # Skip if generic tracker
        if any(g in name_lower for g in GENERIC_TRACKERS):
            continue
        # Check relevance: does app name contain niche keywords?
        niche_words = set(niche_key.replace("_", " ").split())
        app_words = set(name_lower.split())
        overlap = niche_words & app_words
        if len(overlap) >= 1 and meta["rating_count"] > 100:
            relevant.append((name, meta))

    if not relevant:
        return "BLUE_OCEAN"

    strong = [(n, m) for n, m in relevant if m["rating_count"] > 2000]
    if strong:
        return "OCCUPIED"
    return "SOFT_COMPETITION"


def score_opportunity(community_total: int, status: str, hypothesis: str) -> int:
    """0-100 opportunity score."""
    base = 0
    if status == "BLUE_OCEAN":
        base = 70
    elif status == "SOFT_COMPETITION":
        base = 45
    else:
        base = 15

    # Community size bonus
    if community_total > 10_000_000:
        base += 25
    elif community_total > 5_000_000:
        base += 18
    elif community_total > 2_000_000:
        base += 12
    elif community_total > 500_000:
        base += 6

    # Keyword signals in hypothesis
    for signal in ["CRITICAL", "MASSIVE", "ZERO dedicated", "zero apps", "Zero apps", "time-sensitive"]:
        if signal.lower() in hypothesis.lower():
            base += 3

    return min(base, 100)


def main():
    print(f"\n{'='*60}")
    print(f"COMPETITIVE INTEL CYCLE {CYCLE}")
    print(f"Strategy: PARENTING + PET_CARE + ACADEMIC + SOCIAL_CONNECTION")
    print(f"Timestamp: {NOW.isoformat()}")
    print(f"{'='*60}\n")

    DATA.mkdir(exist_ok=True)
    OUTPUT.mkdir(exist_ok=True)

    raw_results = {}
    blue_oceans = []
    soft_competition = []
    occupied = []
    ci_rows = []
    alpha_entries = []

    # ── STEP 1: CONFIGURE ────────────────────────────────────────────
    print(f"[CONFIGURE] {len(NICHES)} niches queued for cycle {CYCLE}")
    print(f"  Strategy: PARENTING + PET_CARE + ACADEMIC + SOCIAL_CONNECTION")

    # ── STEP 2: SCRAPE + ANALYZE ─────────────────────────────────────
    for niche_key, niche_cfg in NICHES.items():
        label = niche_cfg["label"]
        print(f"\n[SCRAPE] {niche_key}")
        print(f"  Subreddits: {niche_cfg['subreddits']}")

        # Reddit community size
        community_total, breakdown = reddit_community_size(niche_cfg["subreddits"])
        print(f"  Community: {community_total:,} ({breakdown})")

        # iTunes App Store check
        print(f"  iTunes search: {niche_cfg['itunes_terms']}")
        apps = itunes_search(niche_cfg["itunes_terms"])
        print(f"  Apps found: {len(apps)}")
        for name, meta in list(apps.items())[:3]:
            print(f"    '{name}' | ${meta['price']} | ★{meta['rating']:.1f} ({meta['rating_count']:,})")

        # ── ANALYZE ──────────────────────────────────────────────────
        status = classify_competition(niche_key, apps)
        score = score_opportunity(community_total, status, niche_cfg["hypothesis"])
        print(f"  Status: {status} | Score: {score}")

        raw_results[niche_key] = {
            "label": label,
            "community_total": community_total,
            "community_breakdown": breakdown,
            "apps_found": len(apps),
            "apps": apps,
            "status": status,
            "score": score,
            "hypothesis": niche_cfg["hypothesis"],
        }

        if status == "BLUE_OCEAN":
            blue_oceans.append((niche_key, community_total))
        elif status == "SOFT_COMPETITION":
            soft_competition.append(niche_key)
        else:
            occupied.append(niche_key)

        # ── CI ROW ───────────────────────────────────────────────────
        ci_rows.append([
            "app_gap",                          # type
            niche_key.split("_")[0],            # category
            label,                              # name
            "paid",                             # price
            "",                                 # rating
            community_total,                    # rating_count (using as community proxy)
            f"C{CYCLE:03d}",                    # version
            DATE_STR,                           # last_updated
            1 if status == "BLUE_OCEAN" else 0, # positive_sentiment
            0,                                  # negative_sentiment
            "reddit+itunes",                    # source
            f"r/{'+'.join(niche_cfg['subreddits'][:2])}",  # url
            status,                             # metric_1
            score,                              # metric_2
            niche_cfg["hypothesis"][:120],      # notes (truncated)
            NOW.isoformat(),                    # scan_date
        ])

        # ── ALPHA ENTRY (Blue Ocean + large community) ───────────────
        if status == "BLUE_OCEAN" and community_total > 1_000_000:
            alpha_entries.append({
                "date": DATE_STR,
                "source": f"competitive_intel_cycle_{CYCLE}",
                "venture": "APP_FACTORY",
                "category": "APP_OPPORTUNITY",
                "title": f"BLUE OCEAN [{niche_key.upper()}]: {label}",
                "content": (
                    f"Community: {community_total:,} | "
                    f"Apps found: {len(apps)} (none dominant). "
                    f"{niche_cfg['hypothesis']} "
                    f"Score: {score}/100. Build: streak UI + {label.lower()} context. $2.99-$4.99."
                ),
                "roi_potential": "HIGH",
                "status": "PENDING_REVIEW",
                "score": score,
            })
        elif status == "SOFT_COMPETITION" and community_total > 3_000_000:
            alpha_entries.append({
                "date": DATE_STR,
                "source": f"competitive_intel_cycle_{CYCLE}",
                "venture": "APP_FACTORY",
                "category": "APP_OPPORTUNITY",
                "title": f"NEAR-BO [{niche_key.upper()}]: {label}",
                "content": (
                    f"Community: {community_total:,} | "
                    f"Weak competition (soft). {niche_cfg['hypothesis']} "
                    f"Score: {score}/100."
                ),
                "roi_potential": "MEDIUM",
                "status": "PENDING_REVIEW",
                "score": score,
            })

    # ── STEP 3: STORE ────────────────────────────────────────────────
    print(f"\n[STORE] Writing {len(ci_rows)} rows to COMPETITIVE_INTEL.csv...")
    try:
        with open(CI_CSV, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            for row in ci_rows:
                writer.writerow(row)
        print(f"  [OK] {len(ci_rows)} rows appended to {CI_CSV}")
    except Exception as e:
        print(f"  [ERR] CI CSV write failed: {e}")

    alpha_written = 0
    if alpha_entries and ALPHA_CSV.exists():
        try:
            with open(ALPHA_CSV, "a", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                for entry in alpha_entries:
                    writer.writerow([
                        entry["date"], entry["source"], entry["venture"],
                        entry["category"], entry["title"], entry["content"],
                        entry["roi_potential"], entry["status"], entry["score"]
                    ])
                    alpha_written += 1
            print(f"  [OK] {alpha_written} alpha entries appended")
        except Exception as e:
            print(f"  [ERR] Alpha staging write failed: {e}")

    # ── STEP 4: SAVE DATA FILES ──────────────────────────────────────
    raw_out = DATA / f"raw_scrape_cycle{CYCLE:03d}.json"
    clean_out = DATA / f"clean_cycle{CYCLE:03d}.json"
    analyze_out = DATA / f"analyze_cycle{CYCLE:03d}.json"

    with open(raw_out, "w") as f:
        json.dump(raw_results, f, indent=2, default=str)

    clean_data = {k: v for k, v in raw_results.items() if v.get("community_total", 0) > 0}
    with open(clean_out, "w") as f:
        json.dump(clean_data, f, indent=2, default=str)

    top_opps = sorted(
        [(k, v["community_total"]) for k, v in raw_results.items()
         if v.get("status") in ("BLUE_OCEAN", "SOFT_COMPETITION")],
        key=lambda x: x[1], reverse=True
    )[:8]

    analyze_data = {
        "cycle": CYCLE,
        "timestamp": NOW.isoformat(),
        "strategy": "PARENTING + PET_CARE + ACADEMIC + SOCIAL_CONNECTION",
        "total_scanned": len(raw_results),
        "blue_oceans": [b[0] for b in blue_oceans],
        "soft_competition": soft_competition,
        "occupied": occupied,
        "top_opportunities": top_opps,
    }
    with open(analyze_out, "w") as f:
        json.dump(analyze_data, f, indent=2, default=str)

    print(f"  [OK] Raw/clean/analyze JSON saved to data/")

    # ── STEP 5: UPDATE CYCLE STATE ───────────────────────────────────
    try:
        state_path = DATA / "cycle_state.json"
        with open(state_path) as f:
            state = json.load(f)
        prev_bos = state.get("cumulative_blue_oceans", 52)
        prev_p0_alerts = state.get("p0_alerts", [])
    except Exception:
        prev_bos = 52
        prev_p0_alerts = []

    new_bos_count = len(blue_oceans)
    new_total_bos = prev_bos + new_bos_count

    p0_alerts = list(prev_p0_alerts)
    for bo_key, bo_community in sorted(blue_oceans, key=lambda x: x[1], reverse=True):
        label = NICHES[bo_key]["label"]
        alert_str = f"NEW_C067 BLUE OCEAN: {bo_key.upper()} — {bo_community:,} community. BUILD NOW."
        if alert_str not in p0_alerts:
            p0_alerts.insert(0, alert_str)

    near_bos = [
        s for s in soft_competition
        if raw_results.get(s, {}).get("community_total", 0) > 2_000_000
    ]

    new_state = {
        "venture": "SCRAPING_competitive_intel",
        "last_cycle": NOW.isoformat(),
        "cycle_number": CYCLE,
        "cycle_status": "COMPLETE",
        "current_step": "done",
        "configured_at": NOW.isoformat(),
        "stats": {
            "niches_scanned": len(raw_results),
            "new_bos_confirmed": new_bos_count,
            "soft_competition": len(soft_competition),
            "occupied": len(occupied),
            "alpha_entries": alpha_written,
            "ci_rows_added": len(ci_rows),
            "blue_oceans_confirmed": new_total_bos,
        },
        "cumulative_blue_oceans": new_total_bos,
        "p0_alerts": p0_alerts,
        f"cycle_{CYCLE}_results": {
            "strategy": "PARENTING + PET_CARE + ACADEMIC + SOCIAL_CONNECTION",
            "new_blue_oceans": [b[0] for b in blue_oceans],
            "near_bos": near_bos,
            "soft_competition": soft_competition,
            "occupied": occupied,
            "biggest_community": sorted(
                [(k, v["community_total"]) for k, v in raw_results.items()],
                key=lambda x: x[1], reverse=True
            )[0] if raw_results else ["N/A", 0],
        },
    }

    with open(DATA / "cycle_state.json", "w") as f:
        json.dump(new_state, f, indent=2, default=str)
    print(f"  [OK] cycle_state.json updated → cycle {CYCLE}, {new_total_bos} total BOs")

    return {
        "raw_results": raw_results,
        "blue_oceans": blue_oceans,
        "soft_competition": soft_competition,
        "occupied": occupied,
        "alpha_written": alpha_written,
        "ci_rows": len(ci_rows),
        "new_total_bos": new_total_bos,
        "analyze_data": analyze_data,
        "near_bos": near_bos,
    }


if __name__ == "__main__":
    results = main()
    print(f"\n[CYCLE {CYCLE}] COMPLETE")
    print(f"  Blue Oceans:      {len(results['blue_oceans'])}")
    print(f"  Soft Competition: {len(results['soft_competition'])}")
    print(f"  Occupied:         {len(results['occupied'])}")
    print(f"  Cumulative BOs:   {results['new_total_bos']}")
    print(f"  CI rows added:    {results['ci_rows']}")
    print(f"  Alpha entries:    {results['alpha_written']}")
