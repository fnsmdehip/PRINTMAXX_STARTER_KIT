#!/usr/bin/env python3
"""
PRINTMAXX Niche Trend Scanner
Monitors Google Trends, Gumroad discover, and App Store top charts for PrintMaxx niche keywords.

Distinct from trend_aggregator.py which focuses on ecom/product trends.
This script focuses on APP and NICHE keyword trends relevant to the 7 PrintMaxx apps:
  - Prayer app, faith app, devotional app
  - Screen time blocker, digital wellbeing, phone addiction
  - Study lock, focus timer, student productivity
  - Fitness tracker, walk tracker, step counter
  - AI productivity, AI tools, AI assistant
  - Sleep tracker, sleep improvement
  - Habit tracker, habit builder

Sources:
  1. Google Trends via pytrends (or fallback to RSS)
  2. Gumroad discover/trending pages (relevant categories)
  3. App Store top charts via iTunes RSS feeds (free)
  4. Reddit niche subreddit pulse check

Output: AUTOMATIONS/logs/trend_report_YYYY-MM-DD.md

Cron entry (weekly, Monday 6:00 AM):
  0 6 * * 1 cd /Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt && /usr/bin/python3 AUTOMATIONS/trend_scanner.py --full >> AUTOMATIONS/logs/trend_scanner.log 2>&1

Usage:
    python3 trend_scanner.py --full             # Full weekly scan (all sources)
    python3 trend_scanner.py --google-trends     # Google Trends only
    python3 trend_scanner.py --appstore          # App Store top charts only
    python3 trend_scanner.py --gumroad           # Gumroad trending only
    python3 trend_scanner.py --reddit            # Reddit niche pulse only
    python3 trend_scanner.py --report            # Show latest report
"""

import argparse
import json
import os
import re
import sys
import time
from datetime import datetime
from pathlib import Path
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError

PROJECT_ROOT = Path(__file__).resolve().parent.parent
LOGS_DIR = PROJECT_ROOT / "AUTOMATIONS" / "logs"
LOG_FILE = LOGS_DIR / "trend_scanner.log"

try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False

try:
    from pytrends.request import TrendReq
    HAS_PYTRENDS = True
except ImportError:
    HAS_PYTRENDS = False


# PrintMaxx niche keyword groups (aligned with 7 PWA apps + alpha findings)
NICHE_KEYWORDS = {
    "faith": {
        "keywords": ["prayer app", "bible app", "devotional app", "christian meditation", "ramadan app"],
        "subreddits": ["r/Christianity", "r/islam", "r/prayer"],
        "app_store_genre": "6017",  # Religion / Spirituality (Reference)
    },
    "screen_time": {
        "keywords": ["screen time blocker", "phone addiction", "digital wellbeing", "dopamine detox", "phone detox app"],
        "subreddits": ["r/nosurf", "r/digitalminimalism"],
        "app_store_genre": "6024",  # Productivity
    },
    "study": {
        "keywords": ["study app", "focus timer", "study lock", "pomodoro app", "student productivity"],
        "subreddits": ["r/GetStudying", "r/productivity"],
        "app_store_genre": "6017",  # Education
    },
    "fitness": {
        "keywords": ["fitness tracker app", "walk tracker", "step counter app", "workout app", "gym app"],
        "subreddits": ["r/fitness", "r/loseit", "r/walking"],
        "app_store_genre": "6013",  # Health & Fitness
    },
    "ai_productivity": {
        "keywords": ["AI productivity app", "AI assistant app", "AI tools", "AI writing app", "chatgpt app"],
        "subreddits": ["r/ChatGPT", "r/ClaudeAI", "r/artificial"],
        "app_store_genre": "6024",  # Productivity
    },
    "sleep": {
        "keywords": ["sleep tracker app", "sleep improvement", "sleep sounds app", "insomnia app", "sleep quality"],
        "subreddits": ["r/sleep", "r/insomnia"],
        "app_store_genre": "6013",  # Health & Fitness
    },
    "habit": {
        "keywords": ["habit tracker app", "habit builder", "daily routine app", "self improvement app", "discipline app"],
        "subreddits": ["r/getdisciplined", "r/DecidingToBeBetter", "r/selfimprovement"],
        "app_store_genre": "6013",  # Health & Fitness
    },
}

# App Store Top Charts RSS genre IDs (free, no auth)
APPSTORE_CHART_GENRES = {
    "Health & Fitness": "6013",
    "Productivity": "6024",
    "Education": "6017",
    "Lifestyle": "6012",
}


def log(msg):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] {msg}"
    print(line)
    try:
        LOGS_DIR.mkdir(parents=True, exist_ok=True)
        with open(LOG_FILE, "a") as f:
            f.write(line + "\n")
    except Exception:
        pass


def fetch_url(url, timeout=15):
    """Fetch URL content as string."""
    req = Request(url, headers={
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
    })
    try:
        with urlopen(req, timeout=timeout) as resp:
            return resp.read().decode("utf-8", errors="replace")
    except (URLError, HTTPError) as e:
        log(f"  ERROR fetching {url}: {e}")
        return None


def scan_google_trends():
    """Scan Google Trends for all niche keywords. Returns dict of niche -> trend data."""
    results = {}

    if HAS_PYTRENDS:
        log("Scanning Google Trends via pytrends...")
        try:
            pytrends = TrendReq(hl="en-US", tz=360)
        except Exception as e:
            log(f"  pytrends init failed: {e}")
            return _scan_google_trends_rss()

        for niche, config in NICHE_KEYWORDS.items():
            kws = config["keywords"][:5]  # pytrends max 5 per request
            log(f"  {niche}: {kws}")
            try:
                pytrends.build_payload(kws, cat=0, timeframe="now 7-d", geo="US")
                interest = pytrends.interest_over_time()
                if not interest.empty:
                    # Get average interest per keyword
                    avgs = {}
                    for kw in kws:
                        if kw in interest.columns:
                            avgs[kw] = round(interest[kw].mean(), 1)
                    results[niche] = {
                        "source": "pytrends",
                        "period": "last 7 days",
                        "keyword_interest": avgs,
                        "top_keyword": max(avgs, key=avgs.get) if avgs else None,
                    }
                else:
                    results[niche] = {"source": "pytrends", "keyword_interest": {}, "note": "No data returned"}
                time.sleep(2)  # Rate limit
            except Exception as e:
                log(f"  pytrends error for {niche}: {e}")
                results[niche] = {"source": "pytrends", "error": str(e)}
                time.sleep(5)
    else:
        log("pytrends not installed, using RSS fallback...")
        results = _scan_google_trends_rss()

    return results


def _scan_google_trends_rss():
    """Fallback: check Google Trends daily trends RSS for relevant keywords."""
    results = {}
    url = "https://trends.google.com/trending/rss?geo=US"
    log(f"  Fetching Google Trends RSS: {url}")
    content = fetch_url(url)
    if not content:
        log("  Could not fetch Google Trends RSS")
        return results

    # Extract trending topics
    titles = re.findall(r"<title><!\[CDATA\[(.*?)\]\]></title>", content)
    traffic = re.findall(r"ht:approx_traffic>(.*?)</ht:approx_traffic", content)

    trending_items = []
    for i, title in enumerate(titles):
        vol = traffic[i] if i < len(traffic) else "?"
        trending_items.append({"title": title, "traffic": vol})

    # Check if any trending topic matches our niche keywords
    for niche, config in NICHE_KEYWORDS.items():
        matches = []
        for item in trending_items:
            t_lower = item["title"].lower()
            for kw in config["keywords"]:
                if any(word in t_lower for word in kw.lower().split()):
                    matches.append(item)
                    break
        results[niche] = {
            "source": "google_trends_rss",
            "matches": matches,
            "match_count": len(matches),
            "total_trending": len(trending_items),
        }

    return results


def scan_appstore_charts():
    """Scan App Store top free/paid charts for relevant categories via RSS."""
    results = {}
    log("Scanning App Store top charts via RSS...")

    for category_name, genre_id in APPSTORE_CHART_GENRES.items():
        for chart_type, chart_name in [("topfreeapplications", "Top Free"), ("toppaidapplications", "Top Paid")]:
            url = f"https://itunes.apple.com/us/rss/{chart_type}/limit=50/genre={genre_id}/json"
            log(f"  {category_name} - {chart_name}")

            content = fetch_url(url)
            if not content:
                continue

            try:
                data = json.loads(content)
                entries = data.get("feed", {}).get("entry", [])
            except (json.JSONDecodeError, KeyError):
                log(f"    Failed to parse JSON for {category_name} {chart_name}")
                continue

            apps = []
            for entry in entries[:25]:
                app_name = ""
                if "im:name" in entry:
                    app_name = entry["im:name"].get("label", "")

                price = "Free"
                if "im:price" in entry:
                    price_data = entry["im:price"].get("attributes", {})
                    amount = price_data.get("amount", "0")
                    if float(amount) > 0:
                        price = f"${amount}"

                category = ""
                if "category" in entry:
                    category = entry["category"].get("attributes", {}).get("label", "")

                developer = ""
                if "im:artist" in entry:
                    developer = entry["im:artist"].get("label", "")

                apps.append({
                    "name": app_name,
                    "price": price,
                    "category": category,
                    "developer": developer,
                })

            key = f"{category_name}_{chart_name.replace(' ', '_').lower()}"
            results[key] = {
                "category": category_name,
                "chart": chart_name,
                "genre_id": genre_id,
                "app_count": len(apps),
                "apps": apps,
            }
            time.sleep(1)

    return results


def scan_gumroad_trending():
    """Scan Gumroad discover page for trending products in relevant categories."""
    results = {}
    log("Scanning Gumroad discover for relevant categories...")

    if not HAS_REQUESTS:
        log("  requests library not installed. Skipping Gumroad scan.")
        return {"error": "requests not installed"}

    categories = [
        ("software-development", "Software & Dev"),
        ("self-improvement", "Self Improvement"),
        ("design", "Design"),
        ("fitness-health", "Fitness & Health"),
        ("education", "Education"),
    ]

    for slug, label in categories:
        url = f"https://gumroad.com/discover?query={slug}"
        log(f"  Gumroad: {label}")

        try:
            resp = requests.get(url, headers={
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
                "Accept": "text/html",
            }, timeout=15)
            html = resp.text
        except Exception as e:
            log(f"    Error: {e}")
            results[slug] = {"category": label, "error": str(e)}
            time.sleep(2)
            continue

        # Extract product names and prices from HTML (basic parsing)
        product_names = re.findall(r'class="[^"]*product-card[^"]*"[^>]*>.*?<h3[^>]*>(.*?)</h3>', html, re.DOTALL)
        prices = re.findall(r'\$[\d,.]+', html)

        # Clean
        products = []
        for i, name in enumerate(product_names[:15]):
            clean_name = re.sub(r'<[^>]+>', '', name).strip()
            if clean_name:
                price = prices[i] if i < len(prices) else "?"
                products.append({"name": clean_name, "price": price})

        results[slug] = {
            "category": label,
            "product_count": len(products),
            "products": products,
        }
        time.sleep(2)

    return results


def scan_reddit_pulse():
    """Quick pulse check on niche subreddits for trending topics."""
    results = {}
    log("Scanning Reddit niche subreddits for trending topics...")

    for niche, config in NICHE_KEYWORDS.items():
        niche_posts = []
        for sub in config.get("subreddits", []):
            sub_name = sub.replace("r/", "")
            url = f"https://www.reddit.com/r/{sub_name}/hot.json?limit=10"
            log(f"  {sub}")

            try:
                req = Request(url, headers={
                    "User-Agent": "PrintMaxx-TrendScanner/1.0 (research bot)",
                })
                with urlopen(req, timeout=15) as resp:
                    data = json.loads(resp.read().decode("utf-8"))

                posts = data.get("data", {}).get("children", [])
                for p in posts:
                    pd = p.get("data", {})
                    title = pd.get("title", "")
                    score = pd.get("score", 0)
                    comments = pd.get("num_comments", 0)
                    created = pd.get("created_utc", 0)
                    niche_posts.append({
                        "subreddit": sub_name,
                        "title": title[:200],
                        "score": score,
                        "comments": comments,
                        "created_utc": created,
                    })
            except Exception as e:
                log(f"    Error fetching {sub}: {e}")

            time.sleep(2)  # Respect rate limits

        # Sort by score and take top 5
        niche_posts.sort(key=lambda x: x.get("score", 0), reverse=True)
        results[niche] = {
            "subreddits": config.get("subreddits", []),
            "top_posts": niche_posts[:5],
            "total_scanned": len(niche_posts),
        }

    return results


def generate_report(trends_data, appstore_data, gumroad_data, reddit_data):
    """Generate a markdown trend report."""
    today = datetime.now().strftime("%Y-%m-%d")
    lines = []

    lines.append(f"# PRINTMAXX Trend Report - {today}")
    lines.append(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    lines.append(f"**Sources:** Google Trends, App Store Top Charts, Gumroad Discover, Reddit Pulse")
    lines.append("")
    lines.append("---")
    lines.append("")

    # Google Trends section
    lines.append("## 1. Google Trends (Niche Keywords)")
    lines.append("")
    if trends_data:
        for niche, data in trends_data.items():
            lines.append(f"### {niche.replace('_', ' ').title()}")
            if "keyword_interest" in data and data["keyword_interest"]:
                lines.append("| Keyword | Interest (avg 7d) |")
                lines.append("|---------|-------------------|")
                for kw, val in sorted(data["keyword_interest"].items(), key=lambda x: x[1], reverse=True):
                    bar = "#" * int(val / 5) if val else ""
                    lines.append(f"| {kw} | {val} {bar} |")
                if data.get("top_keyword"):
                    lines.append(f"\n**Top keyword:** {data['top_keyword']}")
            elif "matches" in data:
                if data["matches"]:
                    lines.append(f"**{data['match_count']} matches found in daily trends:**")
                    for m in data["matches"]:
                        lines.append(f"- {m['title']} (traffic: {m.get('traffic', '?')})")
                else:
                    lines.append("No niche keywords appeared in daily trending topics.")
            elif "error" in data:
                lines.append(f"Error: {data['error']}")
            else:
                lines.append("No data available.")
            lines.append("")
    else:
        lines.append("No Google Trends data collected.")
        lines.append("")

    # App Store section
    lines.append("## 2. App Store Top Charts")
    lines.append("")
    if appstore_data:
        for key, data in appstore_data.items():
            category = data.get("category", key)
            chart = data.get("chart", "?")
            apps = data.get("apps", [])
            lines.append(f"### {category} - {chart} (Top 10)")
            if apps:
                lines.append("| # | App | Price | Developer |")
                lines.append("|---|-----|-------|-----------|")
                for i, app in enumerate(apps[:10], 1):
                    lines.append(f"| {i} | {app['name']} | {app['price']} | {app['developer']} |")
            else:
                lines.append("No data available.")
            lines.append("")
    else:
        lines.append("No App Store data collected.")
        lines.append("")

    # Gumroad section
    lines.append("## 3. Gumroad Trending Products")
    lines.append("")
    if gumroad_data:
        for slug, data in gumroad_data.items():
            if "error" in data:
                lines.append(f"### {data.get('category', slug)}: Error - {data['error']}")
                continue
            cat = data.get("category", slug)
            products = data.get("products", [])
            lines.append(f"### {cat} ({data.get('product_count', 0)} products)")
            if products:
                for p in products[:10]:
                    lines.append(f"- {p['name']} ({p.get('price', '?')})")
            else:
                lines.append("No products extracted (page may require JS rendering).")
            lines.append("")
    else:
        lines.append("No Gumroad data collected.")
        lines.append("")

    # Reddit section
    lines.append("## 4. Reddit Niche Pulse")
    lines.append("")
    if reddit_data:
        for niche, data in reddit_data.items():
            subs = ", ".join(data.get("subreddits", []))
            lines.append(f"### {niche.replace('_', ' ').title()} ({subs})")
            posts = data.get("top_posts", [])
            if posts:
                lines.append("| Score | Comments | Subreddit | Title |")
                lines.append("|-------|----------|-----------|-------|")
                for p in posts:
                    title = p["title"][:80]
                    lines.append(f"| {p['score']:,} | {p['comments']:,} | r/{p['subreddit']} | {title} |")
            else:
                lines.append("No posts found.")
            lines.append("")
    else:
        lines.append("No Reddit data collected.")
        lines.append("")

    # Action items
    lines.append("## 5. Action Items")
    lines.append("")
    lines.append("Based on this scan, consider:")
    lines.append("- [ ] Check if any rising keywords should be added to ASO for our 7 apps")
    lines.append("- [ ] Identify new competitors that appeared in top charts")
    lines.append("- [ ] Look for Gumroad product ideas that align with our niches")
    lines.append("- [ ] Check Reddit pain points for feature ideas")
    lines.append("- [ ] Update LEDGER/TREND_SIGNALS.csv with any actionable signals")
    lines.append("")
    lines.append("---")
    lines.append(f"*Generated by AUTOMATIONS/trend_scanner.py at {datetime.now().isoformat()}*")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="PrintMaxx Niche Trend Scanner")
    parser.add_argument("--full", action="store_true", help="Full weekly scan (all sources)")
    parser.add_argument("--google-trends", action="store_true", help="Google Trends only")
    parser.add_argument("--appstore", action="store_true", help="App Store top charts only")
    parser.add_argument("--gumroad", action="store_true", help="Gumroad trending only")
    parser.add_argument("--reddit", action="store_true", help="Reddit niche pulse only")
    parser.add_argument("--report", action="store_true", help="Show latest report path")
    args = parser.parse_args()

    if not any([args.full, args.google_trends, args.appstore, args.gumroad, args.reddit, args.report]):
        parser.print_help()
        return

    if args.report:
        # Find latest report
        reports = sorted(LOGS_DIR.glob("trend_report_*.md"))
        if reports:
            latest = reports[-1]
            print(f"Latest report: {latest}")
            print(f"Open with: cat {latest}")
        else:
            print("No reports found. Run --full first.")
        return

    log("=" * 60)
    log("PRINTMAXX TREND SCANNER")
    log("=" * 60)

    trends_data = {}
    appstore_data = {}
    gumroad_data = {}
    reddit_data = {}

    if args.full or args.google_trends:
        trends_data = scan_google_trends()

    if args.full or args.appstore:
        appstore_data = scan_appstore_charts()

    if args.full or args.gumroad:
        gumroad_data = scan_gumroad_trending()

    if args.full or args.reddit:
        reddit_data = scan_reddit_pulse()

    # Generate and save report
    report = generate_report(trends_data, appstore_data, gumroad_data, reddit_data)
    today = datetime.now().strftime("%Y-%m-%d")
    report_path = LOGS_DIR / f"trend_report_{today}.md"
    LOGS_DIR.mkdir(parents=True, exist_ok=True)
    with open(report_path, "w") as f:
        f.write(report)

    log(f"Report saved to: {report_path}")
    print(f"\nReport saved: {report_path}")

    # Also save raw data as JSON for programmatic access
    raw_data = {
        "scan_date": today,
        "google_trends": trends_data,
        "appstore_charts": appstore_data,
        "gumroad": gumroad_data,
        "reddit_pulse": reddit_data,
    }
    json_path = LOGS_DIR / f"trend_raw_{today}.json"
    with open(json_path, "w") as f:
        json.dump(raw_data, f, indent=2, default=str)

    log(f"Raw data saved to: {json_path}")
    log("Scan complete.")


if __name__ == "__main__":
    main()
