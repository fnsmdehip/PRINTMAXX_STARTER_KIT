#!/usr/bin/env python3
"""Cycle 56 scraper: RunningStreak verify + Fitness expansion (yoga, cycling, HIIT, pushup, plank, fasting)"""
import urllib.request
import urllib.parse
import json
import time
import os

BASE = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE, "data")

# P0: RunningStreak must be verified this cycle (4.19M unverified demand)
ITUNES_TERMS = {
    "running_streak": "running streak habit paid",
    "running_streak_alt": "run daily habit tracker paid",
    "yoga_streak": "yoga streak habit daily paid",
    "cycling_habit": "cycling habit streak tracker paid",
    "hiit_streak": "hiit workout streak habit paid",
    "pushup_streak": "pushup streak counter habit paid",
    "plank_habit": "plank habit streak counter paid",
    "intermittent_fasting": "intermittent fasting streak habit paid",
    "meditation_streak_recheck": "meditation streak daily habit paid",
    "language_streak_recheck": "language learning streak habit paid",
}

REDDIT_TARGETS = {
    "running": ["running streak app habit", "run daily habit tracker"],
    "yoga": ["yoga streak app habit", "yoga daily tracker"],
    "cycling": ["cycling habit app streak", "bike daily tracker"],
    "fasting": ["intermittent fasting app paid", "16:8 fasting tracker"],
    "bodyweightfitness": ["pushup streak app habit", "plank habit tracker"],
    "Meditation": ["meditation streak app paid", "daily meditation habit"],
    "languagelearning": ["streak app recommendation", "language habit tracker paid"],
    "indiehackers": ["lifetime deal launch revenue week 1", "89 lifetime deals 199"],
}

# Subreddits to size (get subscriber count for demand ranking)
SIZE_TARGETS = ["yoga", "cycling", "fasting", "bodyweightfitness"]


def itunes_scrape():
    results = {}
    for niche, term in ITUNES_TERMS.items():
        url = "https://itunes.apple.com/search?term=" + urllib.parse.quote(term) + "&entity=software&limit=10&country=us"
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=15) as r:
                data = json.loads(r.read())
            apps = data.get("results", [])
            paid = [a for a in apps if a.get("price", 0) > 0]
            paid_details = [
                {
                    "name": a.get("trackName", ""),
                    "price": a.get("price", 0),
                    "rating": round(a.get("averageUserRating", 0), 2),
                    "rating_count": a.get("userRatingCount", 0),
                    "developer": a.get("sellerName", ""),
                    "bundle_id": a.get("bundleId", ""),
                }
                for a in paid[:3]
            ]
            is_generic = any(
                a.get("trackName", "").lower() in ["streaks", "habitify", "way of life", "done"]
                for a in paid
            )
            results[niche] = {
                "search_term": term,
                "total_results": len(apps),
                "paid_count": len(paid),
                "free_count": len(apps) - len(paid),
                "paid_apps": paid_details,
                "gap_confirmed": len(paid) == 0 or (len(paid) <= 2 and is_generic),
                "only_generic": is_generic and len(paid) > 0,
            }
            print(f"iTunes {niche}: {len(paid)} paid apps | gap={results[niche]['gap_confirmed']}")
        except Exception as e:
            results[niche] = {
                "search_term": term,
                "error": str(e),
                "total_results": 0,
                "paid_count": 0,
                "free_count": 0,
                "paid_apps": [],
                "gap_confirmed": False,
            }
            print(f"iTunes {niche} ERROR: {e}")
        time.sleep(2.5)

    out = os.path.join(DATA_DIR, "itunes_scrape_cycle056.json")
    with open(out, "w") as f:
        json.dump(results, f, indent=2)
    print(f"iTunes saved -> {out}")
    return results


def reddit_scrape():
    results = {}
    headers = {
        "User-Agent": "Mozilla/5.0 PRINTMAXX/1.0 (competitive intel research)",
        "Accept": "application/json",
    }

    # Size new subreddits
    for sub in SIZE_TARGETS:
        url = f"https://www.reddit.com/r/{sub}/about.json"
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=10) as r:
                data = json.loads(r.read())
            sub_count = data.get("data", {}).get("subscribers", 0)
            results[f"{sub}_size"] = {"subreddit": sub, "subscribers": sub_count}
            print(f"r/{sub}: {sub_count:,} subscribers")
        except Exception as e:
            results[f"{sub}_size"] = {"subreddit": sub, "subscribers": 0, "error": str(e)}
            print(f"r/{sub} size ERROR: {e}")
        time.sleep(2.0)

    # Keyword searches per subreddit
    for sub, keywords in REDDIT_TARGETS.items():
        sub_results = []
        for kw in keywords[:1]:  # 1 keyword per sub to stay within rate limits
            url = f"https://www.reddit.com/r/{sub}/search.json?q={urllib.parse.quote(kw)}&restrict_sr=1&sort=relevance&limit=5&t=month"
            try:
                req = urllib.request.Request(url, headers=headers)
                with urllib.request.urlopen(req, timeout=10) as r:
                    data = json.loads(r.read())
                posts = data.get("data", {}).get("children", [])
                for p in posts:
                    pd = p.get("data", {})
                    sub_results.append({
                        "title": pd.get("title", ""),
                        "score": pd.get("score", 0),
                        "url": pd.get("url", ""),
                        "selftext": pd.get("selftext", "")[:300],
                        "num_comments": pd.get("num_comments", 0),
                    })
                print(f"r/{sub} '{kw}': {len(posts)} posts")
            except Exception as e:
                print(f"r/{sub} '{kw}' ERROR: {e}")
            time.sleep(2.0)
        results[sub] = sub_results

    out = os.path.join(DATA_DIR, "raw_scrape_cycle056.json")
    with open(out, "w") as f:
        json.dump(results, f, indent=2)
    print(f"Reddit saved -> {out}")
    return results


if __name__ == "__main__":
    print("=== CYCLE 056 SCRAPER ===")
    print("P0: RunningStreak iTunes verification")
    print("Expanding: yoga, cycling, HIIT, pushup, plank, fasting\n")

    print("--- iTunes API ---")
    itunes = itunes_scrape()

    print("\n--- Reddit JSON API ---")
    reddit = reddit_scrape()

    print("\n=== CYCLE 056 SCRAPE COMPLETE ===")
    gaps = [k for k, v in itunes.items() if v.get("gap_confirmed")]
    print(f"iTunes gaps found: {gaps}")
