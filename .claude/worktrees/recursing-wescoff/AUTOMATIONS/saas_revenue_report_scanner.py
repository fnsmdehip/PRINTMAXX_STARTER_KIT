#!/usr/bin/env python3
"""
PRINTMAXX Automation: SaaS Revenue Report Scanner
DUPLICATE ENHANCEMENT for chain_acquisition_i_analyzed_600_verified_s

Scrapes r/microsaas, r/SaaS, and IndieHackers for verified revenue reports,
extracts niche + revenue range + tech stack, scores against PRINTMAXX capabilities
(Claude Code + free infra), and feeds top candidates into app_factory_priority_queue.json.

Revenue comes from BUILDING the validated ideas, not from the research itself.

Cron: 0 6 * * 1 /usr/bin/python3 /path/to/AUTOMATIONS/saas_revenue_report_scanner.py --run
"""

import argparse
import csv
import json
import logging
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

# ---------------------------------------------------------------------------
# _common imports with fallback for standalone execution
# ---------------------------------------------------------------------------
try:
    from _common import PROJECT, safe_path, recall_skills_for_task, capture_skill_from_result
except ImportError:
    PROJECT = Path(__file__).resolve().parent.parent

    def safe_path(p: Path) -> Path:
        resolved = Path(p).resolve()
        if not str(resolved).startswith(str(PROJECT.resolve())):
            raise ValueError(f"Path escape attempt blocked: {resolved}")
        return resolved

    def recall_skills_for_task(task_name: str) -> dict:
        return {}

    def capture_skill_from_result(task_name: str, result: dict) -> None:
        pass

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
AUTOMATIONS_DIR = PROJECT / "AUTOMATIONS"
LOG_FILE = AUTOMATIONS_DIR / "logs" / "saas_revenue_report_scanner.log"
QUEUE_FILE = PROJECT / "app_factory_priority_queue.json"
CACHE_FILE = AUTOMATIONS_DIR / "data" / "saas_scanner_cache.json"
EXPORT_CSV = AUTOMATIONS_DIR / "data" / "saas_revenue_candidates.csv"

REDDIT_API = "https://www.reddit.com"
INDIEHACKERS_API = "https://www.indiehackers.com"

SUBREDDITS = ["microsaas", "SaaS", "EntrepreneurRideAlong"]

# Keywords that indicate a verified revenue report
REVENUE_KEYWORDS = [
    "mrr", "arr", "revenue", "making", "earning", "profit", "$/month",
    "k/month", "per month", "monthly revenue", "revenue report", "milestone",
    "crossed", "hit", "reached", "showcase"
]

# Niche capability scoring weights: higher = better fit for Claude Code + free infra
CAPABILITY_WEIGHTS = {
    "automation":        10,
    "report":            9,
    "pdf":               9,
    "email":             8,
    "invoice":           9,
    "scheduling":        8,
    "notification":      7,
    "analytics":         8,
    "dashboard":         7,
    "api":               8,
    "scraping":          9,
    "monitoring":        8,
    "audit":             8,
    "compliance":        7,
    "workflow":          9,
    "integration":       8,
    "sync":              8,
    "backup":            7,
    "converter":         9,
    "generator":         9,
    "template":          8,
    "form":              7,
    "onboarding":        6,
    "crm":               5,
    "billing":           6,
    "subscription":      6,
    "chatbot":           5,
    "ai":                9,
    "llm":               10,
    "parsing":           9,
    "extraction":        9,
    "validation":        8,
}

# Revenue range scoring: higher MRR floor = higher priority
REVENUE_FLOOR_SCORES = {
    (0,     1_000):  1,
    (1_000,  5_000): 3,
    (5_000, 10_000): 5,
    (10_000, 50_000): 7,
    (50_000, 200_000): 9,
    (200_000, 10_000_000): 10,
}

MIN_SCORE_FOR_QUEUE = 12  # combined score threshold to enter APP_FACTORY queue
MAX_QUEUE_ADDITIONS_PER_RUN = 5
REQUEST_DELAY = 1.5  # seconds between HTTP requests (be polite)

# ---------------------------------------------------------------------------
# Logging setup
# ---------------------------------------------------------------------------

def setup_logging() -> logging.Logger:
    log_path = safe_path(LOG_FILE)
    log_path.parent.mkdir(parents=True, exist_ok=True)
    logger = logging.getLogger("saas_revenue_scanner")
    logger.setLevel(logging.INFO)
    if not logger.handlers:
        fh = logging.FileHandler(log_path, mode="a", encoding="utf-8")
        fh.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))
        logger.addHandler(fh)
        sh = logging.StreamHandler(sys.stdout)
        sh.setFormatter(logging.Formatter("[%(levelname)s] %(message)s"))
        logger.addHandler(sh)
    return logger

# ---------------------------------------------------------------------------
# HTTP helpers
# ---------------------------------------------------------------------------

def fetch_json(url: str, logger: logging.Logger, timeout: int = 15) -> dict | None:
    headers = {
        "User-Agent": "PRINTMAXX-SaaSScanner/1.0 (automation; research)",
        "Accept": "application/json",
    }
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            if resp.status != 200:
                logger.warning("HTTP %s for %s", resp.status, url)
                return None
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        logger.warning("HTTPError %s for %s: %s", exc.code, url, exc.reason)
    except urllib.error.URLError as exc:
        logger.warning("URLError for %s: %s", url, exc.reason)
    except Exception as exc:
        logger.warning("Unexpected fetch error for %s: %s", url, exc)
    return None

# ---------------------------------------------------------------------------
# Reddit scraping
# ---------------------------------------------------------------------------

def _is_revenue_post(title: str, selftext: str) -> bool:
    combined = (title + " " + selftext).lower()
    return any(kw in combined for kw in REVENUE_KEYWORDS)


def _extract_revenue_range(text: str) -> tuple[int, int]:
    """Return (floor, ceiling) MRR estimate in USD from free-text."""
    import re
    text_lower = text.lower()
    patterns = [
        r"\$\s*(\d[\d,]*)\s*(?:k)?(?:\s*[-–]\s*\$?\s*(\d[\d,]*)\s*(?:k)?)?\s*(?:/mo|per\s*month|mrr|monthly)",
        r"(\d[\d,]*)\s*(?:k)?\s*(?:dollars?|usd)?\s*/\s*mo",
    ]
    found_nums = []
    for pat in patterns:
        for m in re.finditer(pat, text_lower):
            for g in m.groups():
                if g:
                    num = int(g.replace(",", ""))
                    # If the match context has 'k' or the number looks like thousands
                    if "k" in text_lower[max(0, m.start()-2):m.end()+2]:
                        num *= 1000
                    found_nums.append(num)
    if not found_nums:
        # Fall back to bare dollar amounts: $10k $50k etc.
        for m in re.finditer(r"\$\s*(\d+)\s*k", text_lower):
            found_nums.append(int(m.group(1)) * 1000)
        for m in re.finditer(r"\$\s*([\d,]+)", text_lower):
            num = int(m.group(1).replace(",", ""))
            if num >= 100:
                found_nums.append(num)
    if not found_nums:
        return (0, 0)
    found_nums.sort()
    return (found_nums[0], found_nums[-1])


def _extract_niche_keywords(text: str) -> list[str]:
    text_lower = text.lower()
    return [kw for kw in CAPABILITY_WEIGHTS if kw in text_lower]


def _extract_tech_stack(text: str) -> list[str]:
    stacks = [
        "python", "node", "react", "nextjs", "rails", "django", "flask",
        "fastapi", "postgres", "sqlite", "supabase", "firebase", "stripe",
        "tailwind", "typescript", "golang", "rust", "php", "laravel",
        "vercel", "cloudflare", "aws", "gcp", "azure",
    ]
    text_lower = text.lower()
    return [s for s in stacks if s in text_lower]


def scrape_subreddit(subreddit: str, logger: logging.Logger, limit: int = 25) -> list[dict]:
    url = f"{REDDIT_API}/r/{subreddit}/search.json?q=revenue+mrr+making&sort=new&limit={limit}&t=month"
    logger.info("Scraping r/%s ...", subreddit)
    data = fetch_json(url, logger)
    if not data:
        return []
    posts = []
    try:
        children = data["data"]["children"]
    except (KeyError, TypeError):
        logger.warning("Unexpected Reddit response structure for r/%s", subreddit)
        return []
    for child in children:
        try:
            p = child["data"]
            title = p.get("title", "")
            selftext = p.get("selftext", "")
            if not _is_revenue_post(title, selftext):
                continue
            rev_floor, rev_ceil = _extract_revenue_range(title + " " + selftext)
            niches = _extract_niche_keywords(title + " " + selftext)
            stack = _extract_tech_stack(title + " " + selftext)
            posts.append({
                "source": f"reddit/r/{subreddit}",
                "title": title[:200],
                "url": "https://reddit.com" + p.get("permalink", ""),
                "score": p.get("score", 0),
                "created_utc": p.get("created_utc", 0),
                "rev_floor": rev_floor,
                "rev_ceil": rev_ceil,
                "niches": niches,
                "tech_stack": stack,
                "raw_text_snippet": (title + " " + selftext)[:500],
            })
        except Exception as exc:
            logger.debug("Post parse error: %s", exc)
            continue
    logger.info("r/%s: %d revenue posts found", subreddit, len(posts))
    time.sleep(REQUEST_DELAY)
    return posts


def scrape_indiehackers(logger: logging.Logger) -> list[dict]:
    """Fetch IndieHackers revenue stories via their public JSON feed."""
    url = "https://www.indiehackers.com/api/main/interviews?limit=20"
    logger.info("Scraping IndieHackers interviews ...")
    data = fetch_json(url, logger)
    posts = []
    if not data:
        logger.info("IndieHackers: no data returned (API may require auth)")
        return posts
    interviews = data if isinstance(data, list) else data.get("interviews", data.get("data", []))
    for item in interviews:
        try:
            title = item.get("title", item.get("name", ""))
            revenue_str = str(item.get("revenue", item.get("monthlyRevenue", "")))
            tags = item.get("tags", [])
            slug = item.get("slug", item.get("id", ""))
            rev_floor, rev_ceil = _extract_revenue_range(revenue_str + " " + title)
            niches = _extract_niche_keywords(title + " " + " ".join(tags))
            posts.append({
                "source": "indiehackers",
                "title": title[:200],
                "url": f"https://www.indiehackers.com/interview/{slug}",
                "score": item.get("upvoteCount", 0),
                "created_utc": 0,
                "rev_floor": rev_floor,
                "rev_ceil": rev_ceil,
                "niches": niches,
                "tech_stack": _extract_tech_stack(title),
                "raw_text_snippet": title[:500],
            })
        except Exception as exc:
            logger.debug("IH parse error: %s", exc)
            continue
    logger.info("IndieHackers: %d revenue posts found", len(posts))
    time.sleep(REQUEST_DELAY)
    return posts

# ---------------------------------------------------------------------------
# Scoring
# ---------------------------------------------------------------------------

def score_candidate(post: dict) -> int:
    """Score a post on capability fit + revenue potential."""
    capability_score = sum(CAPABILITY_WEIGHTS[n] for n in post.get("niches", []))
    rev_floor = post.get("rev_floor", 0)
    rev_score = 0
    for (lo, hi), pts in REVENUE_FLOOR_SCORES.items():
        if lo <= rev_floor < hi:
            rev_score = pts
            break
    # Upvote signal (capped)
    engagement_score = min(int(post.get("score", 0) / 100), 5)
    return capability_score + rev_score + engagement_score


def deduplicate(posts: list[dict], seen_urls: set) -> list[dict]:
    unique = []
    for p in posts:
        if p["url"] not in seen_urls:
            seen_urls.add(p["url"])
            unique.append(p)
    return unique

# ---------------------------------------------------------------------------
# Queue management
# ---------------------------------------------------------------------------

def load_queue(logger: logging.Logger) -> dict:
    q_path = safe_path(QUEUE_FILE)
    if q_path.exists():
        try:
            with q_path.open("r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as exc:
            logger.warning("Could not load queue file: %s", exc)
    return {"generated_at": "", "queue": []}


def save_queue(queue_data: dict, logger: logging.Logger) -> None:
    q_path = safe_path(QUEUE_FILE)
    q_path.parent.mkdir(parents=True, exist_ok=True)
    tmp = q_path.with_suffix(".tmp")
    try:
        with tmp.open("w", encoding="utf-8") as f:
            json.dump(queue_data, f, indent=2)
        tmp.replace(q_path)
        logger.info("Queue saved to %s (%d items)", q_path, len(queue_data["queue"]))
    except Exception as exc:
        logger.error("Failed to save queue: %s", exc)
        if tmp.exists():
            tmp.unlink()
        raise


def build_queue_entry(post: dict, total_score: int) -> dict:
    return {
        "id": urllib.parse.quote(post["url"], safe=""),
        "source_url": post["url"],
        "source": post["source"],
        "title": post["title"],
        "niche_keywords": post["niches"],
        "tech_stack": post["tech_stack"],
        "estimated_mrr_floor": post["rev_floor"],
        "estimated_mrr_ceil": post["rev_ceil"],
        "capability_score": total_score,
        "status": "pending",
        "added_at": datetime.now(timezone.utc).isoformat(),
        "notes": f"Auto-added by saas_revenue_report_scanner. Rev: ${post['rev_floor']:,}-${post['rev_ceil']:,}/mo",
    }

# ---------------------------------------------------------------------------
# Cache helpers
# ---------------------------------------------------------------------------

def load_cache(logger: logging.Logger) -> dict:
    c_path = safe_path(CACHE_FILE)
    if c_path.exists():
        try:
            with c_path.open("r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as exc:
            logger.warning("Cache load error: %s", exc)
    return {"seen_urls": [], "last_run": ""}


def save_cache(cache: dict, logger: logging.Logger) -> None:
    c_path = safe_path(CACHE_FILE)
    c_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        with c_path.open("w", encoding="utf-8") as f:
            json.dump(cache, f, indent=2)
    except Exception as exc:
        logger.warning("Cache save error: %s", exc)

# ---------------------------------------------------------------------------
# CSV export
# ---------------------------------------------------------------------------

def export_csv(candidates: list[dict], logger: logging.Logger) -> None:
    csv_path = safe_path(EXPORT_CSV)
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "source", "title", "url", "rev_floor", "rev_ceil",
        "niches", "tech_stack", "score",
    ]
    try:
        with csv_path.open("a", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
            if csv_path.stat().st_size == 0:
                writer.writeheader()
            for c in candidates:
                row = {
                    "source": c["source"],
                    "title": c["title"],
                    "url": c["url"],
                    "rev_floor": c["rev_floor"],
                    "rev_ceil": c["rev_ceil"],
                    "niches": "|".join(c.get("niches", [])),
                    "tech_stack": "|".join(c.get("tech_stack", [])),
                    "score": c.get("_score", 0),
                }
                writer.writerow(row)
        logger.info("CSV export appended: %s", csv_path)
    except Exception as exc:
        logger.warning("CSV export failed: %s", exc)

# ---------------------------------------------------------------------------
# Core run logic
# ---------------------------------------------------------------------------

def run(dry_run: bool, logger: logging.Logger) -> int:
    """
    Full pipeline:
      1. Recall any relevant skills
      2. Scrape sources
      3. Deduplicate against cache
      4. Score all candidates
      5. Filter by MIN_SCORE_FOR_QUEUE
      6. Inject top candidates into app_factory_priority_queue.json
      7. Export CSV audit trail
      8. Capture skill from result
    Returns number of items added to queue.
    """
    # Step 1: Recall skills context
    skills_ctx = recall_skills_for_task("saas_niche_intelligence")
    logger.info("Skills context: %s", list(skills_ctx.keys()) if skills_ctx else "none")

    # Step 2: Scrape
    all_posts: list[dict] = []
    for sub in SUBREDDITS:
        all_posts.extend(scrape_subreddit(sub, logger))
    all_posts.extend(scrape_indiehackers(logger))
    logger.info("Total raw posts collected: %d", len(all_posts))

    # Step 3: Deduplicate
    cache = load_cache(logger)
    seen_urls: set = set(cache.get("seen_urls", []))
    unique_posts = deduplicate(all_posts, seen_urls)
    logger.info("Unique new posts after dedup: %d", len(unique_posts))

    # Step 4: Score
    scored: list[tuple[int, dict]] = []
    for post in unique_posts:
        s = score_candidate(post)
        post["_score"] = s
        scored.append((s, post))
    scored.sort(key=lambda x: x[0], reverse=True)

    # Step 5: Filter
    qualified = [(s, p) for s, p in scored if s >= MIN_SCORE_FOR_QUEUE]
    logger.info("Qualified candidates (score >= %d): %d", MIN_SCORE_FOR_QUEUE, len(qualified))

    # Step 6: Inject into queue
    added = 0
    if not dry_run:
        queue_data = load_queue(logger)
        existing_ids = {entry.get("id") for entry in queue_data.get("queue", [])}
        for score_val, post in qualified[:MAX_QUEUE_ADDITIONS_PER_RUN]:
            entry = build_queue_entry(post, score_val)
            if entry["id"] not in existing_ids:
                queue_data["queue"].append(entry)
                existing_ids.add(entry["id"])
                added += 1
                logger.info(
                    "QUEUED [score=%d mrr=$%d-$%d] %s",
                    score_val, post["rev_floor"], post["rev_ceil"], post["title"][:80]
                )
        queue_data["generated_at"] = datetime.now(timezone.utc).isoformat()
        if added:
            save_queue(queue_data, logger)
    else:
        logger.info("[DRY-RUN] Would add up to %d items to queue:", MAX_QUEUE_ADDITIONS_PER_RUN)
        for score_val, post in qualified[:MAX_QUEUE_ADDITIONS_PER_RUN]:
            logger.info(
                "  [score=%d mrr=$%d-$%d niches=%s] %s",
                score_val, post["rev_floor"], post["rev_ceil"],
                ",".join(post["niches"][:3]), post["title"][:80]
            )

    # Step 7: CSV audit trail (all qualified, even in dry-run for visibility)
    export_csv([p for _, p in qualified], logger)

    # Step 8: Capture skill
    result_summary = {
        "posts_collected": len(all_posts),
        "unique_new": len(unique_posts),
        "qualified": len(qualified),
        "added_to_queue": added,
        "top_candidates": [
            {
                "title": p["title"],
                "score": s,
                "niches": p["niches"],
                "mrr_range": [p["rev_floor"], p["rev_ceil"]],
            }
            for s, p in qualified[:5]
        ],
    }
    capture_skill_from_result("saas_niche_intelligence", result_summary)

    # Update cache
    if not dry_run:
        cache["seen_urls"] = list(seen_urls)
        cache["last_run"] = datetime.now(timezone.utc).isoformat()
        save_cache(cache, logger)

    logger.info(
        "Run complete. Posts=%d Unique=%d Qualified=%d Added=%d",
        len(all_posts), len(unique_posts), len(qualified), added
    )
    return added


def status(logger: logging.Logger) -> None:
    """Print current queue and cache state."""
    try:
        queue_data = load_queue(logger)
        q = queue_data.get("queue", [])
        pending = [e for e in q if e.get("status") == "pending"]
        print(f"Queue file:       {safe_path(QUEUE_FILE)}")
        print(f"Total in queue:   {len(q)}")
        print(f"Pending builds:   {len(pending)}")
        print(f"Queue updated:    {queue_data.get('generated_at', 'never')}")

        cache = load_cache(logger)
        print(f"Last scanner run: {cache.get('last_run', 'never')}")
        print(f"URLs seen so far: {len(cache.get('seen_urls', []))}")

        if pending:
            print("\nTop pending items:")
            for entry in sorted(pending, key=lambda x: x.get("capability_score", 0), reverse=True)[:5]:
                print(
                    f"  [score={entry.get('capability_score',0)} "
                    f"mrr=${entry.get('estimated_mrr_floor',0):,}-${entry.get('estimated_mrr_ceil',0):,}] "
                    f"{entry['title'][:70]}"
                )
    except Exception as exc:
        logger.error("Status error: %s", exc)
        sys.exit(1)

# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="PRINTMAXX: SaaS Revenue Report Scanner → APP_FACTORY queue feeder"
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--run", action="store_true", help="Scrape, score, and update queue")
    group.add_argument("--status", action="store_true", help="Show queue and cache state")
    group.add_argument("--dry-run", action="store_true", help="Scrape and score without writing to queue")
    args = parser.parse_args()

    logger = setup_logging()
    logger.info("=== saas_revenue_report_scanner starting (dry_run=%s) ===", args.dry_run)

    try:
        if args.status:
            status(logger)
        elif args.run:
            run(dry_run=False, logger=logger)
        elif args.dry_run:
            run(dry_run=True, logger=logger)
    except KeyboardInterrupt:
        logger.info("Interrupted.")
        sys.exit(0)
    except Exception as exc:
        logger.error("Fatal error: %s", exc, exc_info=True)
        sys.exit(1)

    logger.info("=== saas_revenue_report_scanner done ===")
    sys.exit(0)


if __name__ == "__main__":
    main()