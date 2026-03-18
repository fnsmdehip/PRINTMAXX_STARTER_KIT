#!/usr/bin/env python3
"""
Competitive Intel Scraper — Cycle 064
Strategy: CREATIVE_ARTS + SKILL_BUILDING + SPIRITUAL_SPECIFICS + PROFESSIONAL_HABITS
Date: 2026-03-17
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

CYCLE = 64
NOW = datetime.now(timezone.utc)
DATE_STR = NOW.strftime("%Y-%m-%d")
TS = NOW.strftime("%Y%m%d_%H%M")

# Generic tracker exclusion list (false positive filter)
GENERIC_TRACKERS = {
    "streaks", "habitica", "productive", "habitminder", "habit tracker",
    "loop habit tracker", "done", "streaks - habit tracker", "habitnow",
    "habit - daily tracker", "everyday", "habitify", "strides", "way of life",
    "coach.me", "fabulous", "productive - habit tracker", "daylio",
    "habitbull", "momentum", "finch", "tiimo", "routinery"
}

# Cycle 64 targets: unexplored niches
NICHES = {
    "guitar_practice_streak": {
        "label": "Daily Guitar Practice Streak",
        "subreddits": ["guitarlessons", "Guitar", "learnguitar"],
        "itunes_terms": ["guitar practice streak daily habit", "guitar daily habit tracker paid"],
        "hypothesis": "BO — no dedicated guitar practice tracker, 2M+ guitarist community"
    },
    "piano_practice_habit": {
        "label": "Daily Piano Practice Habit Tracker",
        "subreddits": ["pianolearning", "piano", "learnpiano"],
        "itunes_terms": ["piano practice streak daily habit", "piano habit tracker paid daily"],
        "hypothesis": "BO — piano learning community growing via TikTok trend, no dedicated app"
    },
    "chess_daily_streak": {
        "label": "Daily Chess Puzzle / Study Streak",
        "subreddits": ["chess", "chessbeginners", "ChessOpenings"],
        "itunes_terms": ["chess daily puzzle streak habit paid", "chess study habit tracker paid"],
        "hypothesis": "OCCUPIED — Chess.com has app but no dedicated streak-only habit tool"
    },
    "writing_daily_streak": {
        "label": "Daily Writing / 1000 Words Streak",
        "subreddits": ["writing", "worldbuilding", "nanowrimo"],
        "itunes_terms": ["daily writing streak habit 1000 words paid", "writing habit tracker paid streak"],
        "hypothesis": "BO — large writing community, NaNoWriMo proves demand, no dedicated streak app"
    },
    "poetry_streak": {
        "label": "Daily Poetry Writing Streak",
        "subreddits": ["Poetry", "poetryworkshop", "worldbuilding"],
        "itunes_terms": ["poetry writing streak daily habit paid", "poem a day habit tracker paid"],
        "hypothesis": "BO — niche but loyal community, no dedicated poetry streak app found"
    },
    "devotional_reading_streak": {
        "label": "Daily Devotional Reading Streak (non-Quran/Bible specific)",
        "subreddits": ["Christianity", "Reformed", "spirituality"],
        "itunes_terms": ["devotional reading streak daily habit paid", "daily devotional habit tracker paid"],
        "hypothesis": "SOFT — Hallow exists but is Catholic-focused, gap for Protestant/generic devotional"
    },
    "rosary_streak": {
        "label": "Daily Rosary Prayer Streak",
        "subreddits": ["Catholicism", "OrthodoxChristianity", "Christianity"],
        "itunes_terms": ["rosary streak daily habit paid", "rosary prayer habit tracker paid"],
        "hypothesis": "BO — Hallow is meditation-first, no dedicated rosary streak tracker"
    },
    "posture_habit": {
        "label": "Daily Posture Check / Posture Habit Streak",
        "subreddits": ["Posture", "Posturecheck", "bodyweightfitness"],
        "itunes_terms": ["posture habit streak daily paid", "posture reminder habit tracker paid"],
        "hypothesis": "BO — WFH posture epidemic, r/Posture community active, no dedicated habit app"
    },
    "stretching_streak": {
        "label": "Daily Stretching / Flexibility Streak",
        "subreddits": ["flexibility", "yoga", "Stretching"],
        "itunes_terms": ["stretching streak daily habit paid", "flexibility habit tracker paid daily"],
        "hypothesis": "SOFT — Some yoga apps include stretching but no dedicated stretch-streak app"
    },
    "typing_speed_habit": {
        "label": "Daily Typing Speed Practice Streak",
        "subreddits": ["learntyping", "MechanicalKeyboards", "productivity"],
        "itunes_terms": ["typing speed streak habit paid", "typing practice daily habit tracker paid"],
        "hypothesis": "BO — WFH remote work typing skill demand, no dedicated habit tracker found"
    },
    "networking_habit": {
        "label": "Daily Networking / Professional Outreach Streak",
        "subreddits": ["networking", "careerguidance", "LinkedInLunatics"],
        "itunes_terms": ["networking habit streak daily paid", "professional outreach habit tracker paid"],
        "hypothesis": "BO — job market anxiety driving networking behavior, no streak app found"
    },
    "reading_pages_streak": {
        "label": "Daily Reading Pages Goal Streak (10 pages/day)",
        "subreddits": ["books", "52book", "booksuggestions"],
        "itunes_terms": ["reading pages streak daily habit paid", "daily reading habit pages tracker paid"],
        "hypothesis": "BO supplement to READING_STREAK — pages-focused vs time-focused, different UX"
    }
}

def get_reddit_community_size(subreddits: list[str]) -> tuple[int, dict]:
    """Get subscriber count via Reddit JSON API (no browser needed)."""
    headers = {"User-Agent": "Mozilla/5.0 (compatible; research-bot/1.0)"}
    sizes = {}
    total = 0
    for sub in subreddits:
        try:
            url = f"https://www.reddit.com/r/{sub}/about.json"
            r = requests.get(url, headers=headers, timeout=10)
            if r.status_code == 200:
                data = r.json()
                count = data.get("data", {}).get("subscribers", 0)
                sizes[sub] = count
                total += count
            else:
                sizes[sub] = 0
            time.sleep(2.0)
        except Exception as e:
            sizes[sub] = 0
    return total, sizes


def search_itunes(term: str, limit: int = 15) -> list[dict]:
    """Search iTunes App Store for competing apps."""
    url = "https://itunes.apple.com/search"
    params = {
        "term": term,
        "entity": "software",
        "country": "us",
        "limit": limit,
        "explicit": "no"
    }
    try:
        r = requests.get(url, params=params, timeout=15)
        if r.status_code == 200:
            return r.json().get("results", [])
    except Exception:
        pass
    return []


def is_generic_tracker(app_name: str) -> bool:
    """Filter out generic habit trackers that appear in all niche searches."""
    name_lower = app_name.lower()
    for generic in GENERIC_TRACKERS:
        if generic in name_lower:
            return True
    return False


def find_dedicated_competitor(apps: list[dict], niche_keywords: list[str]) -> dict | None:
    """Find the top dedicated niche competitor (not generic)."""
    dedicated = []
    for app in apps:
        name = app.get("trackName", "")
        desc = app.get("description", "").lower()[:200]
        ratings = app.get("userRatingCount", 0)
        if is_generic_tracker(name):
            continue
        # Check if niche keyword appears in name or desc
        for kw in niche_keywords:
            if kw.lower() in name.lower() or kw.lower() in desc:
                dedicated.append({"name": name, "ratings": ratings, "app": app})
                break
    if dedicated:
        dedicated.sort(key=lambda x: x["ratings"], reverse=True)
        return dedicated[0]
    return None


def classify_competition(total_community: int, top_app_ratings: int, generic_count: int) -> str:
    """Classify niche as BLUE_OCEAN, SOFT_COMPETITION, or OCCUPIED."""
    if top_app_ratings == 0:
        return "BLUE_OCEAN"
    elif top_app_ratings < 10_000:
        return "SOFT_COMPETITION"
    else:
        return "OCCUPIED"


def score_opportunity(status: str, community_size: int, top_app_ratings: int) -> int:
    """Score 1-10 based on demand vs competition gap."""
    if status == "BLUE_OCEAN":
        base = 8
        if community_size > 5_000_000:
            base = 10
        elif community_size > 2_000_000:
            base = 9
        return base
    elif status == "SOFT_COMPETITION":
        base = 6
        if community_size > 3_000_000:
            base = 7
        return base
    else:  # OCCUPIED
        if top_app_ratings > 100_000:
            return 2
        elif top_app_ratings > 50_000:
            return 3
        return 4


def main():
    print(f"[CYCLE {CYCLE}] Starting Competitive Intel Scraper")
    print(f"[CYCLE {CYCLE}] Strategy: CREATIVE_ARTS + SKILL_BUILDING + SPIRITUAL_SPECIFICS + PROFESSIONAL_HABITS")
    print(f"[CYCLE {CYCLE}] Niches to scan: {len(NICHES)}")

    raw_results = {}
    ci_rows = []
    blue_oceans = []
    soft_competition = []
    occupied = []
    alpha_entries = []

    # ── STEP 1: SCRAPE ──────────────────────────────────────────────
    print(f"\n[SCRAPE] Phase starting...")
    for niche_key, niche_data in NICHES.items():
        print(f"  Scanning: {niche_key}")
        result = {"niche": niche_key, "label": niche_data["label"], "hypothesis": niche_data["hypothesis"]}

        # Reddit community sizing
        total_community, sub_breakdown = get_reddit_community_size(niche_data["subreddits"])
        result["community_total"] = total_community
        result["subreddit_breakdown"] = sub_breakdown
        print(f"    Reddit community: {total_community:,}")

        # iTunes competition scan
        all_apps = []
        for term in niche_data["itunes_terms"]:
            apps = search_itunes(term)
            all_apps.extend(apps)
            time.sleep(2.5)

        # Deduplicate apps by trackId
        seen_ids = set()
        unique_apps = []
        for app in all_apps:
            tid = app.get("trackId")
            if tid and tid not in seen_ids:
                seen_ids.add(tid)
                unique_apps.append(app)

        total_apps = len(unique_apps)
        generics_filtered = sum(1 for a in unique_apps if is_generic_tracker(a.get("trackName", "")))
        real_apps = [a for a in unique_apps if not is_generic_tracker(a.get("trackName", ""))]

        # Find keywords for niche matching
        niche_words = niche_key.replace("_", " ").split()

        top_competitor = find_dedicated_competitor(real_apps, niche_words)
        top_app_name = top_competitor["name"] if top_competitor else ""
        top_app_ratings = top_competitor["ratings"] if top_competitor else 0

        result["total_apps_found"] = total_apps
        result["generics_filtered"] = generics_filtered
        result["real_competitors"] = len(real_apps)
        result["top_competitor"] = top_app_name
        result["top_competitor_ratings"] = top_app_ratings

        print(f"    iTunes: {total_apps} apps found, {generics_filtered} generics filtered, top: {top_app_name} ({top_app_ratings:,} ratings)")

        raw_results[niche_key] = result

    # ── STEP 2: CLEAN + ANALYZE ─────────────────────────────────────
    print(f"\n[CLEAN+ANALYZE] Classifying {len(raw_results)} niches...")
    for niche_key, result in raw_results.items():
        status = classify_competition(
            result["community_total"],
            result["top_competitor_ratings"],
            result.get("generics_filtered", 0)
        )
        score = score_opportunity(status, result["community_total"], result["top_competitor_ratings"])
        result["status"] = status
        result["score"] = score

        if status == "BLUE_OCEAN":
            blue_oceans.append((niche_key, result["community_total"]))
        elif status == "SOFT_COMPETITION":
            soft_competition.append(niche_key)
        else:
            occupied.append(niche_key)

        # Build CI row
        notes_parts = []
        if result["top_competitor"]:
            notes_parts.append(f"{len([a for a in raw_results[niche_key].get('subreddit_breakdown', {})])} competitors. Top: '{result['top_competitor']}' ({result['top_competitor_ratings']:,} ratings).")
        else:
            notes_parts.append(f"No dedicated niche app found. {result['generics_filtered']} generic trackers filtered out.")
        notes_parts.append(f"Community: {result['community_total']:,}.")

        ci_row = [
            DATE_STR,
            CYCLE,
            niche_key,
            result["label"],
            status,
            result["community_total"],
            ",".join(NICHES[niche_key]["subreddits"]),
            result["top_competitor_ratings"],
            result["generics_filtered"],
            result["top_competitor"],
            result["top_competitor_ratings"],
            " ".join(notes_parts),
            False,
            json.dumps(result["subreddit_breakdown"])
        ]
        ci_rows.append(ci_row)

        # Generate alpha entries for BOs and soft competition
        if status in ("BLUE_OCEAN", "SOFT_COMPETITION") and result["community_total"] > 500_000:
            alpha_entries.append({
                "date": DATE_STR,
                "source": f"auto_scraper_cycle064_{niche_key}",
                "venture": "APP_FACTORY",
                "category": "APP_FACTORY",
                "title": f"{'BLUE OCEAN' if status == 'BLUE_OCEAN' else 'SOFT'}: {result['label']} — {result['community_total']:,} community",
                "content": f"Niche: {niche_key}. Status: {status}. Community: {result['community_total']:,}. Top app: {result['top_competitor'] or 'NONE'} ({result['top_competitor_ratings']:,} ratings). {NICHES[niche_key]['hypothesis']}",
                "roi_potential": "HIGH" if status == "BLUE_OCEAN" else "MEDIUM",
                "status": "PENDING_REVIEW",
                "score": score
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

    # Write alpha entries to ALPHA_STAGING.csv
    alpha_written = 0
    if alpha_entries and ALPHA_CSV.exists():
        try:
            with open(ALPHA_CSV, "r", encoding="utf-8") as f:
                existing_content = f.read()
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

    # ── STEP 4: SAVE DATA FILES ─────────────────────────────────────
    raw_out = DATA / f"raw_scrape_cycle{CYCLE:03d}.json"
    clean_out = DATA / f"clean_cycle{CYCLE:03d}.json"
    analyze_out = DATA / f"analyze_cycle{CYCLE:03d}.json"

    with open(raw_out, "w") as f:
        json.dump(raw_results, f, indent=2)

    clean_data = {k: v for k, v in raw_results.items() if v.get("community_total", 0) > 0}
    with open(clean_out, "w") as f:
        json.dump(clean_data, f, indent=2)

    analyze_data = {
        "cycle": CYCLE,
        "timestamp": NOW.isoformat(),
        "strategy": "CREATIVE_ARTS + SKILL_BUILDING + SPIRITUAL_SPECIFICS + PROFESSIONAL_HABITS",
        "total_scanned": len(raw_results),
        "blue_oceans": [b[0] for b in blue_oceans],
        "soft_competition": soft_competition,
        "occupied": occupied,
        "top_opportunities": sorted(
            [(k, v["community_total"]) for k, v in raw_results.items() if v.get("status") in ("BLUE_OCEAN", "SOFT_COMPETITION")],
            key=lambda x: x[1], reverse=True
        )[:8]
    }
    with open(analyze_out, "w") as f:
        json.dump(analyze_data, f, indent=2)

    print(f"  [OK] Raw/clean/analyze JSON saved to data/")

    # ── STEP 5: UPDATE CYCLE STATE ───────────────────────────────────
    # Load current BO count
    try:
        state_path = DATA / "cycle_state.json"
        with open(state_path) as f:
            state = json.load(f)
        prev_bos = state.get("cumulative_blue_oceans", 46)
    except Exception:
        prev_bos = 46

    new_bos_count = len(blue_oceans)
    new_total_bos = prev_bos + new_bos_count

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
            "blue_oceans_confirmed": new_total_bos
        },
        "cumulative_blue_oceans": new_total_bos,
        "p0_alerts": [
            "CLEAN_EATING_STREAK: 11.4M community. LARGEST BO. BUILD NOW.",
            "READING_STREAK: 23M r/books. BUILD NOW.",
            "CODING_STREAK: 4.7M r/learnprogramming. BUILD NOW.",
            "MEDITATION_STREAK: 3.52M. BUILD NOW.",
            "RUNNING_STREAK: 4.19M VERIFIED. BUILD NOW.",
            "SAVINGS_STREAK: 30.9M personalfinance. BUILD NOW.",
            "PRAYERLOCK: Ramadan time-critical. CRITICAL.",
        ],
        f"cycle_{CYCLE}_results": {
            "strategy": "CREATIVE_ARTS + SKILL_BUILDING + SPIRITUAL_SPECIFICS + PROFESSIONAL_HABITS",
            "new_blue_oceans": [b[0] for b in blue_oceans],
            "soft_competition": soft_competition,
            "occupied": occupied,
            "biggest_community": sorted(
                [(k, v["community_total"]) for k, v in raw_results.items()],
                key=lambda x: x[1], reverse=True
            )[0] if raw_results else ["N/A", 0]
        }
    }

    with open(DATA / "cycle_state.json", "w") as f:
        json.dump(new_state, f, indent=2)
    print(f"  [OK] cycle_state.json updated → cycle {CYCLE}, {new_total_bos} total BOs")

    # Return results for alert generation
    return {
        "raw_results": raw_results,
        "blue_oceans": blue_oceans,
        "soft_competition": soft_competition,
        "occupied": occupied,
        "alpha_written": alpha_written,
        "ci_rows": len(ci_rows),
        "new_total_bos": new_total_bos,
        "analyze_data": analyze_data
    }


if __name__ == "__main__":
    results = main()
    print(f"\n[CYCLE {CYCLE}] COMPLETE")
    print(f"  Blue Oceans: {len(results['blue_oceans'])}")
    print(f"  Soft Competition: {len(results['soft_competition'])}")
    print(f"  Occupied: {len(results['occupied'])}")
    print(f"  Cumulative BOs: {results['new_total_bos']}")
    print(f"  CI rows added: {results['ci_rows']}")
    print(f"  Alpha entries: {results['alpha_written']}")
