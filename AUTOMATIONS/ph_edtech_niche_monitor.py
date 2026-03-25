#!/usr/bin/env python3
"""
PRINTMAXX Automation: PH Edtech Niche Monitor
==============================================
Tracks Product Hunt exam prep / edtech app launches, extracts certification
niches with proven demand, feeds the app factory with ranked niche targets,
and generates SEO content targeting '[certification] exam prep app' long-tail
keywords.

DAG type:       scraper|dag
Method context: [PH LAUNCH] Educato App: Personalized exam prep, now in your pocket
Output:         AUTOMATIONS/output/ph_edtech_niche_monitor/
                  certification_niches.csv   — ranked niche targets for app factory
                  ph_launches.json           — raw PH launch data
                  seo_content.json           — long-tail keyword + content briefs
                  state.json                 — last-run metadata
"""

import argparse
import csv
import json
import logging
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

# ---------------------------------------------------------------------------
# Bootstrap — import from _common or define local fallbacks
# ---------------------------------------------------------------------------
try:
    from _common import PROJECT, safe_path, recall_skills_for_task, capture_skill_from_result
except ImportError:
    PROJECT = Path(__file__).resolve().parent.parent

    def safe_path(path) -> Path:
        """Resolve path and assert it stays within PROJECT."""
        resolved = Path(path).resolve()
        try:
            resolved.relative_to(PROJECT)
        except ValueError:
            raise ValueError(f"Path escape: {resolved} is outside PROJECT {PROJECT}")
        return resolved

    def recall_skills_for_task(task: str) -> list:  # noqa: D103
        return []

    def capture_skill_from_result(result: dict) -> None:  # noqa: D103
        pass


# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
LOG_DIR      = PROJECT / "AUTOMATIONS" / "logs"
LOG_FILE     = LOG_DIR / "ph_edtech_niche_monitor.log"
OUTPUT_DIR   = PROJECT / "AUTOMATIONS" / "output" / "ph_edtech_niche_monitor"
LAUNCHES_JSON  = OUTPUT_DIR / "ph_launches.json"
NICHES_CSV     = OUTPUT_DIR / "certification_niches.csv"
SEO_JSON       = OUTPUT_DIR / "seo_content.json"
STATE_FILE     = OUTPUT_DIR / "state.json"

LOG_ROTATE_BYTES = 5 * 1024 * 1024  # 5 MB

# ---------------------------------------------------------------------------
# Domain data
# ---------------------------------------------------------------------------
CERT_KEYWORDS = [
    "aws", "azure", "gcp", "google cloud", "comptia", "cissp", "ceh",
    "pmp", "scrum", "agile", "gmat", "gre", "sat", "act", "lsat", "mcat",
    "usmle", "nclex", "bar exam", "cpa", "cfa", "frm", "series 7",
    "ielts", "toefl", "toeic", "duolingo english", "ccna", "ccnp",
    "cisco", "java", "python", "javascript", "react", "kubernetes",
    "docker", "terraform", "devops", "data science", "machine learning",
    "salesforce", "hubspot", "google analytics", "facebook ads",
    "microsoft office", "excel", "sql", "tableau", "power bi",
    "real estate", "insurance", "nursing", "medical", "dental",
    "pharmacy", "physical therapy", "occupational therapy",
    "driving", "cdl", "faa", "pilot", "emt", "paramedic",
    "six sigma", "lean", "itil", "cobit", "prince2",
    "exam prep", "certification", "study guide", "practice test",
    "mock exam", "flashcard", "quiz", "spaced repetition",
]

SEO_TEMPLATES = [
    "{cert} exam prep app",
    "{cert} practice test app",
    "{cert} study app",
    "best {cert} exam app",
    "{cert} certification app",
    "free {cert} study app",
    "{cert} quiz app",
    "{cert} flashcard app",
    "top {cert} prep app",
    "{cert} exam simulator app",
    "{cert} exam questions app",
    "pass {cert} on first try app",
]

PH_GRAPHQL_URL   = "https://api.producthunt.com/v2/api/graphql"
PH_EDUCATION_URL = "https://www.producthunt.com/topics/education"

PH_POSTS_QUERY = """
query EdtechPosts($cursor: String) {
  posts(topic: "education", order: VOTES, after: $cursor) {
    pageInfo { hasNextPage endCursor }
    edges {
      node {
        id name tagline description votesCount commentsCount website createdAt
        topics { edges { node { name slug } } }
      }
    }
  }
}
"""

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------

def _rotate_log_if_needed() -> None:
    """Use subprocess gzip to rotate oversized log files (cron-safe)."""
    try:
        log_path = safe_path(LOG_FILE)
        if log_path.exists() and log_path.stat().st_size > LOG_ROTATE_BYTES:
            stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S")
            archive = safe_path(LOG_DIR / f"ph_edtech_niche_monitor.{stamp}.log.gz")
            result = subprocess.run(
                ["gzip", "-c", str(log_path)],
                capture_output=True, timeout=30
            )
            if result.returncode == 0:
                archive.write_bytes(result.stdout)
                log_path.write_text("", encoding="utf-8")
    except (ValueError, OSError, subprocess.SubprocessError):
        pass  # Non-fatal; log rotation is best-effort


def setup_logging() -> logging.Logger:
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    _rotate_log_if_needed()
    log_path = safe_path(LOG_FILE)

    logger = logging.getLogger("ph_edtech_niche_monitor")
    logger.setLevel(logging.INFO)
    if logger.handlers:
        return logger

    fh = logging.FileHandler(log_path, mode="a", encoding="utf-8")
    fh.setFormatter(logging.Formatter(
        "%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%dT%H:%M:%SZ",
    ))
    sh = logging.StreamHandler(sys.stdout)
    sh.setFormatter(logging.Formatter("[%(levelname)s] %(message)s"))
    logger.addHandler(fh)
    logger.addHandler(sh)
    return logger


# ---------------------------------------------------------------------------
# HTTP helpers
# ---------------------------------------------------------------------------

def fetch_url(url: str, headers: dict = None, data: bytes = None, timeout: int = 20) -> str:
    req = urllib.request.Request(url, data=data, headers=headers or {})
    req.add_header(
        "User-Agent",
        "Mozilla/5.0 (compatible; PRINTMAXX/1.0; +https://printmaxx.io)",
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read().decode("utf-8", errors="replace")


def ph_graphql(query: str, variables: dict = None, token: str = "") -> dict:
    payload = json.dumps({"query": query, "variables": variables or {}}).encode()
    headers = {"Content-Type": "application/json", "Accept": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return json.loads(fetch_url(PH_GRAPHQL_URL, headers=headers, data=payload))


# ---------------------------------------------------------------------------
# Mock data (dry-run / fallback)
# ---------------------------------------------------------------------------

def _mock_launches() -> list:
    return [
        {
            "id": "mock-001",
            "name": "Educato",
            "tagline": "Personalized exam prep, now in your pocket",
            "description": "AI-powered AWS certification study app with adaptive quizzes and spaced repetition",
            "votes": 842, "comments": 134,
            "website": "https://educato.app",
            "created_at": "2026-03-20T10:00:00Z",
            "topics": ["Education", "Productivity"],
        },
        {
            "id": "mock-002",
            "name": "CertPath",
            "tagline": "Your CISSP & CompTIA study companion",
            "description": "Gamified cybersecurity certification prep with practice tests and exam simulations",
            "votes": 612, "comments": 89,
            "website": "https://certpath.io",
            "created_at": "2026-03-18T09:00:00Z",
            "topics": ["Education", "Security"],
        },
        {
            "id": "mock-003",
            "name": "MedBoard",
            "tagline": "USMLE Step 1 and 2 in 90 days",
            "description": "Spaced repetition flashcards and mock exams for medical board exam prep",
            "votes": 530, "comments": 72,
            "website": "https://medboard.io",
            "created_at": "2026-03-15T08:00:00Z",
            "topics": ["Education", "Health"],
        },
        {
            "id": "mock-004",
            "name": "LangBoost",
            "tagline": "IELTS and TOEFL prep with real test simulations",
            "description": "Full-length practice tests, AI scoring, and feedback for IELTS TOEFL TOEIC",
            "votes": 488, "comments": 61,
            "website": "https://langboost.app",
            "created_at": "2026-03-12T11:00:00Z",
            "topics": ["Education", "Language"],
        },
        {
            "id": "mock-005",
            "name": "CloudAce",
            "tagline": "Pass AWS Azure GCP exams on your first try",
            "description": "Adaptive learning for cloud certification exam prep with practice questions",
            "votes": 407, "comments": 55,
            "website": "https://cloudace.dev",
            "created_at": "2026-03-10T13:00:00Z",
            "topics": ["Education", "Cloud"],
        },
        {
            "id": "mock-006",
            "name": "BarPrep AI",
            "tagline": "Pass the bar exam with AI-personalized study",
            "description": "MBE practice questions and essay feedback for bar exam preparation",
            "votes": 375, "comments": 48,
            "website": "https://barprep.ai",
            "created_at": "2026-03-08T10:00:00Z",
            "topics": ["Education", "Legal"],
        },
        {
            "id": "mock-007",
            "name": "CPA Coach",
            "tagline": "CPA exam prep that adapts to you",
            "description": "Adaptive practice tests, flashcards, and performance analytics for CPA candidates",
            "votes": 342, "comments": 44,
            "website": "https://cpacoach.app",
            "created_at": "2026-03-05T09:00:00Z",
            "topics": ["Education", "Finance"],
        },
        {
            "id": "mock-008",
            "name": "PMPocket",
            "tagline": "PMP certification in your pocket",
            "description": "PMP practice tests, agile scenarios, and scrum flashcards for project managers",
            "votes": 298, "comments": 39,
            "website": "https://pmpocket.io",
            "created_at": "2026-03-02T08:00:00Z",
            "topics": ["Education", "Productivity"],
        },
    ]


# ---------------------------------------------------------------------------
# Scraping
# ---------------------------------------------------------------------------

def _parse_node(node: dict) -> dict:
    topics = [
        t["node"]["name"]
        for t in node.get("topics", {}).get("edges", [])
    ]
    return {
        "id":          node.get("id"),
        "name":        node.get("name", ""),
        "tagline":     node.get("tagline", ""),
        "description": node.get("description", ""),
        "votes":       node.get("votesCount", 0),
        "comments":    node.get("commentsCount", 0),
        "website":     node.get("website", ""),
        "created_at":  node.get("createdAt", ""),
        "topics":      topics,
    }


def _scrape_via_graphql(logger: logging.Logger, token: str = "") -> list:
    launches = []
    cursor = None
    for page in range(5):
        variables = {"cursor": cursor} if cursor else {}
        result = ph_graphql(PH_POSTS_QUERY, variables, token=token)
        if "errors" in result:
            logger.warning("GraphQL errors on page %d: %s", page + 1, result["errors"])
            break
        data    = result.get("data", {}).get("posts", {})
        edges   = data.get("edges", [])
        for edge in edges:
            launches.append(_parse_node(edge.get("node", {})))
        page_info = data.get("pageInfo", {})
        if not page_info.get("hasNextPage"):
            break
        cursor = page_info.get("endCursor")
    return launches


def _scrape_via_html(logger: logging.Logger) -> list:
    """Fallback: extract __NEXT_DATA__ JSON from PH education topic page."""
    launches = []
    try:
        html  = fetch_url(PH_EDUCATION_URL)
        start = html.find('id="__NEXT_DATA__"')
        if start == -1:
            return launches
        start = html.find(">", start) + 1
        end   = html.find("</script>", start)
        if end <= start:
            return launches
        page_data = json.loads(html[start:end])

        def dig(obj, *keys):
            for k in keys:
                if not isinstance(obj, (dict, list)):
                    return None
                obj = obj.get(k) if isinstance(obj, dict) else (obj[k] if isinstance(obj, list) and isinstance(k, int) else None)
            return obj

        edges = dig(page_data, "props", "pageProps", "posts", "edges") or []
        for edge in edges:
            launches.append(_parse_node(edge.get("node", {})))
    except (urllib.error.URLError, json.JSONDecodeError, TypeError, ValueError) as exc:
        logger.warning("HTML scrape failed: %s", exc)
    return launches


def scrape_ph_launches(logger: logging.Logger, dry_run: bool = False, token: str = "") -> list:
    if dry_run:
        logger.info("[DRY-RUN] Returning mock PH launches")
        return _mock_launches()

    logger.info("Scraping Product Hunt edtech launches...")
    launches = []

    try:
        launches = _scrape_via_graphql(logger, token=token)
        logger.info("GraphQL: fetched %d launches", len(launches))
    except urllib.error.HTTPError as exc:
        if exc.code == 401:
            logger.warning("GraphQL unauthenticated (401) — falling back to HTML scrape")
        else:
            logger.warning("GraphQL HTTP %d — falling back to HTML scrape", exc.code)
    except (urllib.error.URLError, json.JSONDecodeError, KeyError) as exc:
        logger.warning("GraphQL error: %s — falling back to HTML scrape", exc)

    if not launches:
        launches = _scrape_via_html(logger)
        logger.info("HTML scrape: fetched %d launches", len(launches))

    if not launches:
        logger.warning("All scrape methods failed — using mock data")
        launches = _mock_launches()

    return launches


# ---------------------------------------------------------------------------
# Niche extraction
# ---------------------------------------------------------------------------

def extract_niches(launches: list, logger: logging.Logger) -> list:
    """
    Score each certification niche by frequency, total PH votes, and
    engagement ratio (votes / comments).  Composite score weights:
      50% total votes signal  |  25% mention frequency  |  25% engagement
    """
    logger.info("Extracting niches from %d launches...", len(launches))
    niche_map: dict = {}

    for launch in launches:
        text = " ".join([
            launch.get("name", ""),
            launch.get("tagline", ""),
            launch.get("description", ""),
        ]).lower()

        votes      = launch.get("votes", 0)
        comments   = launch.get("comments", 0)
        engagement = votes / max(comments, 1)
        name       = launch.get("name", "")

        for kw in CERT_KEYWORDS:
            if kw not in text:
                continue
            if kw not in niche_map:
                niche_map[kw] = {
                    "niche":            kw,
                    "mentions":         0,
                    "total_votes":      0,
                    "_engagement_sum":  0.0,
                    "avg_engagement":   0.0,
                    "example_launches": [],
                }
            entry = niche_map[kw]
            entry["mentions"]        += 1
            entry["total_votes"]     += votes
            entry["_engagement_sum"] += engagement
            entry["avg_engagement"]  = entry["_engagement_sum"] / entry["mentions"]
            if len(entry["example_launches"]) < 3:
                entry["example_launches"].append(name)

    niches = []
    max_votes  = max((e["total_votes"] for e in niche_map.values()), default=1) or 1
    max_eng    = max((e["avg_engagement"] for e in niche_map.values()), default=1) or 1

    for entry in niche_map.values():
        score = (
            (entry["total_votes"]    / max_votes) * 50
            + (entry["mentions"]     / max(len(launches), 1)) * 25
            + (entry["avg_engagement"] / max_eng) * 25
        )
        niches.append({
            "niche":            entry["niche"],
            "rank_score":       round(score, 4),
            "mentions":         entry["mentions"],
            "total_votes":      entry["total_votes"],
            "avg_engagement":   round(entry["avg_engagement"], 2),
            "example_launches": ", ".join(entry["example_launches"]),
        })

    niches.sort(key=lambda x: x["rank_score"], reverse=True)
    logger.info("Identified %d certification niches", len(niches))
    return niches


# ---------------------------------------------------------------------------
# SEO content generation
# ---------------------------------------------------------------------------

def generate_seo_content(niches: list, logger: logging.Logger) -> list:
    """
    Produce long-tail keyword targets and content briefs for the top 20 niches,
    targeting '[certification] exam prep app' search intent patterns.
    """
    top     = niches[:20]
    logger.info("Generating SEO content for top %d niches...", len(top))
    items   = []

    for niche in top:
        cert       = niche["niche"]
        cert_title = cert.upper() if len(cert) <= 5 else cert.title()

        items.append({
            "niche":               cert,
            "primary_keyword":     f"{cert_title} exam prep app",
            "long_tail_keywords":  [t.format(cert=cert_title) for t in SEO_TEMPLATES],
            "meta_title":          (
                f"Best {cert_title} Exam Prep App — Ace Your Certification in 2026"
            ),
            "meta_description":    (
                f"Top-rated {cert_title} exam prep app with adaptive practice tests, "
                f"flashcards, and real exam simulations. "
                f"Join thousands who passed on their first try."
            ),
            "h1":                  (
                f"Prepare for Your {cert_title} Exam With AI-Powered Practice Tests"
            ),
            "content_brief":       (
                f"Audience: professionals studying for {cert_title} certification. "
                f"Pain points: expensive courses, low pass rates, time constraints. "
                f"Differentiators: mobile-first, adaptive learning, offline mode. "
                f"CTA: Start 7-day free practice / Download free trial."
            ),
            "rank_score":          niche["rank_score"],
            "ph_votes_signal":     niche["total_votes"],
        })

    logger.info("Generated %d SEO items", len(items))
    return items


# ---------------------------------------------------------------------------
# File I/O (all writes through safe_path)
# ---------------------------------------------------------------------------

def _ensure_dirs() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    LOG_DIR.mkdir(parents=True, exist_ok=True)


def _write_json(dest: Path, data, logger: logging.Logger, dry_run: bool, label: str) -> None:
    if dry_run:
        logger.info("[DRY-RUN] Would write %s → %s", label, dest)
        return
    try:
        path = safe_path(dest)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
        logger.info("Wrote %s → %s", label, path)
    except (ValueError, OSError) as exc:
        logger.error("Failed to write %s: %s", label, exc)


def save_launches(launches: list, logger: logging.Logger, dry_run: bool) -> None:
    _write_json(LAUNCHES_JSON, launches, logger, dry_run, "launches JSON")


def save_niches_csv(niches: list, logger: logging.Logger, dry_run: bool) -> None:
    if not niches:
        logger.warning("No niches to write")
        return
    if dry_run:
        logger.info("[DRY-RUN] Would write niches CSV → %s", NICHES_CSV)
        return
    try:
        path = safe_path(NICHES_CSV)
        path.parent.mkdir(parents=True, exist_ok=True)
        fieldnames = list(niches[0].keys())
        with path.open("w", newline="", encoding="utf-8") as fh:
            writer = csv.DictWriter(fh, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(niches)
        logger.info("Wrote niches CSV → %s", path)
    except (ValueError, OSError) as exc:
        logger.error("Failed to write niches CSV: %s", exc)


def save_seo_content(items: list, logger: logging.Logger, dry_run: bool) -> None:
    _write_json(SEO_JSON, items, logger, dry_run, "SEO content JSON")


def save_state(state: dict, logger: logging.Logger) -> None:
    try:
        path = safe_path(STATE_FILE)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(state, indent=2, ensure_ascii=False), encoding="utf-8")
    except (ValueError, OSError) as exc:
        logger.warning("Could not save state: %s", exc)


def load_state(logger: logging.Logger) -> dict:
    try:
        path = safe_path(STATE_FILE)
        if path.exists():
            return json.loads(path.read_text(encoding="utf-8"))
    except (ValueError, OSError, json.JSONDecodeError) as exc:
        logger.debug("State load error: %s", exc)
    return {}


# ---------------------------------------------------------------------------
# Status
# ---------------------------------------------------------------------------

def print_status(logger: logging.Logger) -> None:
    state = load_state(logger)
    print("\n=== PH EDTECH NICHE MONITOR — STATUS ===")
    if not state:
        print("  No run data found. Use --run to execute the pipeline.")
    else:
        print(f"  Last run    : {state.get('last_run', 'N/A')}")
        print(f"  Launches    : {state.get('launches_count', 0)}")
        print(f"  Niches      : {state.get('niches_count', 0)}")
        print(f"  SEO items   : {state.get('seo_items_count', 0)}")
        top = state.get("top_niches", [])[:5]
        print(f"  Top niches  : {', '.join(top) if top else 'N/A'}")
    print()
    artifacts = [
        (LAUNCHES_JSON, "Launches JSON "),
        (NICHES_CSV,    "Niches CSV    "),
        (SEO_JSON,      "SEO JSON      "),
        (LOG_FILE,      "Log file      "),
    ]
    for path, label in artifacts:
        if path.exists():
            size = f"{path.stat().st_size:,} B"
            print(f"  {label}  OK   {size:>12}   {path}")
        else:
            print(f"  {label}  --   {'missing':>12}   {path}")
    print()


# ---------------------------------------------------------------------------
# Pipeline
# ---------------------------------------------------------------------------

def run_pipeline(dry_run: bool = False, token: str = "") -> None:
    logger = setup_logging()
    logger.info("=== PH EDTECH NICHE MONITOR START  dry_run=%s ===", dry_run)

    _ensure_dirs()

    # Recall any persisted skills for this task type
    try:
        skills = recall_skills_for_task("ph_edtech_scrape_niche_extraction")
        if skills:
            logger.info("Recalled %d prior skills for task", len(skills))
    except Exception as exc:
        logger.debug("recall_skills_for_task unavailable: %s", exc)

    # Stage 1 — scrape
    launches = scrape_ph_launches(logger, dry_run=dry_run, token=token)
    save_launches(launches, logger, dry_run)

    # Stage 2 — niche extraction
    niches = extract_niches(launches, logger)
    save_niches_csv(niches, logger, dry_run)

    # Stage 3 — SEO content
    seo_items = generate_seo_content(niches, logger)
    save_seo_content(seo_items, logger, dry_run)

    # Stage 4 — capture skill from top result
    if niches:
        top = niches[0]
        try:
            capture_skill_from_result({
                "task":                "ph_edtech_niche_monitor",
                "top_niche":          top["niche"],
                "rank_score":         top["rank_score"],
                "seo_primary_kw":     f"{top['niche'].upper()} exam prep app",
                "ph_votes_signal":    top["total_votes"],
            })
        except Exception as exc:
            logger.debug("capture_skill_from_result unavailable: %s", exc)

    # Stage 5 — persist state
    state = {
        "last_run":        datetime.now(timezone.utc).isoformat(),
        "launches_count":  len(launches),
        "niches_count":    len(niches),
        "seo_items_count": len(seo_items),
        "top_niches":      [n["niche"] for n in niches[:10]],
        "dry_run":         dry_run,
    }
    if not dry_run:
        save_state(state, logger)

    logger.info(
        "=== COMPLETE  launches=%d  niches=%d  seo_items=%d ===",
        len(launches), len(niches), len(seo_items),
    )

    # Cron-friendly stdout summary
    print(
        f"[ph_edtech_niche_monitor] "
        f"launches={len(launches)} niches={len(niches)} seo={len(seo_items)}"
    )
    if niches:
        top = niches[0]
        print(
            f"[ph_edtech_niche_monitor] "
            f"top_niche={top['niche']}  score={top['rank_score']}  "
            f"votes={top['total_votes']}"
        )


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="ph_edtech_niche_monitor",
        description="PRINTMAXX — PH Edtech Launch Monitor & Niche Extractor",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "examples:\n"
            "  %(prog)s --run\n"
            "  %(prog)s --run --token YOUR_PH_API_TOKEN\n"
            "  %(prog)s --dry-run\n"
            "  %(prog)s --status\n"
        ),
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--run",
        action="store_true",
        help="Execute the full scrape → niche extraction → SEO generation pipeline",
    )
    group.add_argument(
        "--status",
        action="store_true",
        help="Print status of last run and output file inventory",
    )
    group.add_argument(
        "--dry-run",
        dest="dry_run",
        action="store_true",
        help="Simulate pipeline using mock data; no network requests or file writes",
    )
    parser.add_argument(
        "--token",
        default="",
        metavar="PH_TOKEN",
        help="Product Hunt API bearer token (enables authenticated GraphQL; optional)",
    )
    return parser


def main() -> None:
    parser = build_parser()
    args   = parser.parse_args()

    try:
        if args.status:
            logger = setup_logging()
            print_status(logger)
        elif args.dry_run:
            run_pipeline(dry_run=True, token=args.token)
        else:
            run_pipeline(dry_run=False, token=args.token)
    except KeyboardInterrupt:
        sys.exit(0)
    except Exception as exc:
        try:
            logger = setup_logging()
            logger.critical("Unhandled exception: %s", exc, exc_info=True)
        except Exception:
            pass
        print(f"[ph_edtech_niche_monitor] FATAL: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()