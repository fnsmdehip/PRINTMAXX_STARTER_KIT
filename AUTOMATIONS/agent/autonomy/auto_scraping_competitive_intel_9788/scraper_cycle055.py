#!/usr/bin/env python3
"""Cycle 55 scraper: iTunes API + Reddit JSON API"""
import urllib.request
import urllib.parse
import json
import time
import os

BASE = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE, "data")

ITUNES_TERMS = {
    "journaling_habit": "journal habit streak daily",
    "language_learning_streak": "language learning streak habit",
    "walking_habit_streak": "walking habit tracker streak",
    "sleep_habit_tracker": "sleep habit tracker paid",
    "writing_habit_streak": "writing habit streak daily",
    "nofap_streak": "nofap streak counter",
    "sobriety_streak_recheck": "sobriety counter streak",
    "gratitude_habit": "gratitude journal habit paid",
    "cold_shower_recheck": "cold shower habit streak",
    "mindfulness_streak": "mindfulness habit streak"
}

REDDIT_TARGETS = {
    "Journaling": ["journal app recommendation", "habit app streak"],
    "languagelearning": ["streak app language", "habit tracker language"],
    "sleep": ["sleep habit app", "tracker paid app"],
    "running": ["running streak app habit", "habit tracker runner"],
    "indiehackers": ["lifetime deal week 1", "indie app launch revenue"],
    "MicroSaas": ["lifetime deal results", "indie app sales week 1"],
}

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
                }
                for a in paid[:3]
            ]
            results[niche] = {
                "search_term": term,
                "total_results": len(apps),
                "paid_count": len(paid),
                "free_count": len(apps) - len(paid),
                "paid_apps": paid_details,
                "gap_confirmed": len(paid) == 0,
            }
            print(f"iTunes {niche}: {len(paid)} paid apps")
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
    out = os.path.join(DATA_DIR, "itunes_scrape_cycle055.json")
    with open(out, "w") as f:
        json.dump(results, f, indent=2)
    print(f"iTunes saved -> {out}")
    return results


def reddit_scrape():
    results = {}
    for sub, keywords in REDDIT_TARGETS.items():
        sub_results = {"subreddit": sub, "subscriber_count": None, "posts": []}
        # Get subreddit info (subscriber count)
        try:
            url = f"https://www.reddit.com/r/{sub}/about.json"
            req = urllib.request.Request(url, headers={"User-Agent": "printmaxx-intel/1.0"})
            with urllib.request.urlopen(req, timeout=10) as r:
                about = json.loads(r.read())
            sub_results["subscriber_count"] = about.get("data", {}).get("subscribers", 0)
            print(f"r/{sub}: {sub_results['subscriber_count']:,} subs")
        except Exception as e:
            print(f"r/{sub} about err: {e}")
        time.sleep(2.0)
        # Search for each keyword
        for kw in keywords:
            try:
                url = "https://www.reddit.com/r/" + sub + "/search.json?q=" + urllib.parse.quote(kw) + "&sort=top&t=month&limit=10"
                req = urllib.request.Request(url, headers={"User-Agent": "printmaxx-intel/1.0"})
                with urllib.request.urlopen(req, timeout=10) as r:
                    data = json.loads(r.read())
                posts = data.get("data", {}).get("children", [])
                for p in posts:
                    pd = p.get("data", {})
                    sub_results["posts"].append({
                        "id": pd.get("id", ""),
                        "title": pd.get("title", "")[:200],
                        "score": pd.get("score", 0),
                        "num_comments": pd.get("num_comments", 0),
                        "url": pd.get("url", ""),
                        "keyword": kw,
                    })
                print(f"  r/{sub} '{kw}': {len(posts)} posts")
            except Exception as e:
                print(f"  r/{sub} '{kw}' err: {e}")
            time.sleep(2.0)
        results[sub] = sub_results
    out = os.path.join(DATA_DIR, "raw_scrape_cycle055.json")
    with open(out, "w") as f:
        json.dump({"cycle": 55, "subreddits": results}, f, indent=2)
    print(f"Reddit saved -> {out}")
    return results


if __name__ == "__main__":
    print("=== CYCLE 55 SCRAPE ===")
    itunes = itunes_scrape()
    reddit = reddit_scrape()
    print("=== SCRAPE COMPLETE ===")
