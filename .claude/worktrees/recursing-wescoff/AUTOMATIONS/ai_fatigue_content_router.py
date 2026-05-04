#!/usr/bin/env python3
"""
ai_fatigue_content_router.py — PRINTMAXX Automation System

Monitors HN and Reddit for AI fatigue sentiment signals, then routes
those signals to engagement_bait_converter.py to produce contrarian
'anti-AI-overwhelm' content that positions PRINTMAXX tools as the
simple/human alternative.

Cron-safe: no interactive input, exits cleanly with integer status codes.

Usage:
    python ai_fatigue_content_router.py --run
    python ai_fatigue_content_router.py --dry-run
    python ai_fatigue_content_router.py --status
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
# Project root — must appear before _common import
# ---------------------------------------------------------------------------
PROJECT = Path(__file__).resolve().parent.parent

# ---------------------------------------------------------------------------
# _common bootstrap — graceful fallback for standalone / first-run
# ---------------------------------------------------------------------------
try:
    sys.path.insert(0, str(PROJECT))
    from _common import (  # type: ignore[import]
        PROJECT as _COMMON_PROJECT,
        safe_path,
        recall_skills_for_task,
        capture_skill_from_result,
    )
    PROJECT = _COMMON_PROJECT
except ImportError:

    def safe_path(path: Path) -> Path:  # type: ignore[misc]
        """Ensure *path* resolves inside PROJECT; raise ValueError otherwise."""
        resolved = Path(path).resolve()
        if not str(resolved).startswith(str(PROJECT.resolve())):
            raise ValueError(f"Path escape blocked: {resolved!r} is outside {PROJECT!r}")
        return resolved

    def recall_skills_for_task(task: str) -> list:  # type: ignore[misc]
        return []

    def capture_skill_from_result(result: dict) -> None:  # type: ignore[misc]
        pass


# ---------------------------------------------------------------------------
# Canonical paths
# ---------------------------------------------------------------------------
AUTOMATIONS_DIR    = PROJECT / "AUTOMATIONS"
LOG_DIR            = AUTOMATIONS_DIR / "logs"
LOG_FILE           = LOG_DIR / "ai_fatigue_content_router.log"
OUTPUT_DIR         = AUTOMATIONS_DIR / "ai_fatigue_content"
SIGNALS_CSV        = OUTPUT_DIR / "signals.csv"
CONTENT_QUEUE_JSON = OUTPUT_DIR / "content_queue.json"
STATUS_JSON        = OUTPUT_DIR / "status.json"
CONVERTER_SCRIPT   = AUTOMATIONS_DIR / "engagement_bait_converter.py"

# ---------------------------------------------------------------------------
# Logging — append-mode, cron-friendly dual handler
# ---------------------------------------------------------------------------
def _setup_logging() -> logging.Logger:
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    logger = logging.getLogger("ai_fatigue_content_router")
    logger.setLevel(logging.DEBUG)
    if logger.handlers:
        return logger
    fmt = logging.Formatter(
        "%(asctime)s [%(levelname)-8s] %(message)s",
        datefmt="%Y-%m-%dT%H:%M:%SZ",
    )
    fh = logging.FileHandler(safe_path(LOG_FILE), mode="a", encoding="utf-8")
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(fmt)
    logger.addHandler(fh)

    sh = logging.StreamHandler(sys.stdout)
    sh.setLevel(logging.INFO)
    sh.setFormatter(fmt)
    logger.addHandler(sh)
    return logger


log = _setup_logging()

# ---------------------------------------------------------------------------
# Configuration constants
# ---------------------------------------------------------------------------
HN_SEARCH_URL     = "https://hn.algolia.com/api/v1/search"
REDDIT_SEARCH_URL = "https://www.reddit.com/search.json"
REQUEST_TIMEOUT   = 15  # seconds
FATIGUE_THRESHOLD = 0.15

AI_FATIGUE_KEYWORDS = [
    "AI fatigue",
    "AI overwhelm",
    "too many AI tools",
    "AI tool overload",
    "quit AI tools",
    "AI burnout",
    "done with AI",
    "AI exhaustion",
    "AI hype tired",
    "digital minimalism AI",
    "back to basics productivity",
    "AI simplicity",
]

CONTRARIAN_HOOKS = [
    "I quit {n} AI tools and made more money",
    "Why I deleted every AI tool (and what I use instead)",
    "The one tool that replaced my entire AI stack",
    "How going low-tech doubled my output",
    "Stop using AI for {task} — do this instead",
    "The $0 method that outperformed my whole AI setup",
    "I'm done chasing AI tools — here's what actually works",
    "AI fatigue is real: how I simplified everything in a weekend",
]

_FATIGUE_TERMS = frozenset({
    "fatigue", "overwhelm", "overwhelmed", "tired", "exhausted", "burnout",
    "overload", "quit", "delete", "deleted", "simplify", "simpler", "simple",
    "done", "enough", "stop", "hate", "hype", "toxic", "distraction",
    "minimalism", "minimal", "basics", "basic",
})


# ---------------------------------------------------------------------------
# HTTP helper
# ---------------------------------------------------------------------------
def _fetch_json(url: str, params: dict = None) -> dict:
    """GET *url* with optional query *params*; return parsed JSON or None."""
    if params:
        url = f"{url}?{urllib.parse.urlencode(params)}"
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "PRINTMAXX-ContentRouter/1.0 (cron automation)"},
    )
    try:
        with urllib.request.urlopen(req, timeout=REQUEST_TIMEOUT) as resp:
            raw = resp.read().decode("utf-8")
            return json.loads(raw)
    except urllib.error.HTTPError as exc:
        log.warning("HTTP %s for %s: %s", exc.code, url, exc.reason)
    except urllib.error.URLError as exc:
        log.warning("URL error for %s: %s", url, exc.reason)
    except (json.JSONDecodeError, TimeoutError, OSError) as exc:
        log.warning("Fetch failed for %s: %s", url, exc)
    return None


# ---------------------------------------------------------------------------
# Signal collectors
# ---------------------------------------------------------------------------
def _fetch_hn_signals(keyword: str) -> list:
    data = _fetch_json(HN_SEARCH_URL, {
        "query": keyword,
        "tags": "story,comment",
        "hitsPerPage": 10,
    })
    if not data:
        return []
    signals = []
    for hit in data.get("hits", []):
        title = hit.get("title") or (hit.get("comment_text") or "")[:120]
        if not title:
            continue
        signals.append({
            "source":     "hackernews",
            "id":         str(hit.get("objectID", "")),
            "title":      title,
            "url":        hit.get("url") or f"https://news.ycombinator.com/item?id={hit.get('objectID')}",
            "score":      int(hit.get("points") or 0),
            "comments":   int(hit.get("num_comments") or 0),
            "keyword":    keyword,
            "fetched_at": datetime.now(timezone.utc).isoformat(),
        })
    return signals


def _fetch_reddit_signals(keyword: str) -> list:
    data = _fetch_json(REDDIT_SEARCH_URL, {
        "q":     keyword,
        "sort":  "hot",
        "limit": 10,
        "t":     "week",
    })
    if not data:
        return []
    signals = []
    for child in data.get("data", {}).get("children", []):
        post = child.get("data", {})
        title = (post.get("title") or "")[:200]
        if not title:
            continue
        signals.append({
            "source":     "reddit",
            "id":         str(post.get("id", "")),
            "title":      title,
            "url":        f"https://www.reddit.com{post.get('permalink', '')}",
            "score":      int(post.get("score") or 0),
            "comments":   int(post.get("num_comments") or 0),
            "keyword":    keyword,
            "fetched_at": datetime.now(timezone.utc).isoformat(),
        })
    return signals


def collect_signals() -> list:
    """Collect AI-fatigue signals from HN and Reddit across all keywords."""
    log.info("Collecting signals for %d keywords…", len(AI_FATIGUE_KEYWORDS))
    all_signals = []
    seen = set()
    for keyword in AI_FATIGUE_KEYWORDS:
        for sig in _fetch_hn_signals(keyword) + _fetch_reddit_signals(keyword):
            uid = f"{sig['source']}:{sig['id']}"
            if uid not in seen and sig["id"]:
                seen.add(uid)
                all_signals.append(sig)
    log.info("Collected %d unique signals.", len(all_signals))
    return all_signals


# ---------------------------------------------------------------------------
# Sentiment scoring
# ---------------------------------------------------------------------------
def score_fatigue(signal: dict) -> float:
    """Return 0–1 fatigue score based on keyword overlap and engagement."""
    text   = (signal.get("title") or "").lower()
    tokens = set(text.split())
    hits   = tokens & _FATIGUE_TERMS
    base   = len(hits) / len(_FATIGUE_TERMS)
    engagement_bonus = min(
        (signal.get("score", 0) + signal.get("comments", 0)) / 1000.0,
        0.30,
    )
    return round(min(base + engagement_bonus, 1.0), 4)


# ---------------------------------------------------------------------------
# Content brief builder
# ---------------------------------------------------------------------------
def build_content_brief(signal: dict) -> dict:
    """Produce a structured content brief from a scored signal."""
    # Deterministic hook selection keyed on signal id
    idx  = sum(ord(c) for c in signal["id"]) % len(CONTRARIAN_HOOKS)
    hook = CONTRARIAN_HOOKS[idx].format(n=12, task="writing")
    return {
        "source_id":     f"{signal['source']}:{signal['id']}",
        "source_title":  signal["title"],
        "source_url":    signal["url"],
        "hook":          hook,
        "angle":         "contrarian-anti-ai-overwhelm",
        "cta":           "PRINTMAXX — the one tool that replaces your whole stack",
        "fatigue_score": signal.get("fatigue_score", 0.0),
        "created_at":    datetime.now(timezone.utc).isoformat(),
        "status":        "queued",
    }


# ---------------------------------------------------------------------------
# Persistence
# ---------------------------------------------------------------------------
def _ensure_dirs() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    LOG_DIR.mkdir(parents=True, exist_ok=True)


def save_signals_csv(signals: list, dry_run: bool = False) -> None:
    _ensure_dirs()
    target = safe_path(SIGNALS_CSV)
    write_header = not target.exists()
    if dry_run:
        log.info("[dry-run] Would append %d signals → %s", len(signals), target)
        return
    fields = ["source", "id", "title", "url", "score", "comments",
              "keyword", "fetched_at", "fatigue_score"]
    try:
        with target.open("a", newline="", encoding="utf-8") as fh:
            writer = csv.DictWriter(fh, fieldnames=fields, extrasaction="ignore")
            if write_header:
                writer.writeheader()
            writer.writerows(signals)
        log.info("Appended %d signals → %s", len(signals), target)
    except OSError as exc:
        log.error("Failed writing signals CSV: %s", exc)


def save_content_queue(briefs: list, dry_run: bool = False) -> None:
    _ensure_dirs()
    target = safe_path(CONTENT_QUEUE_JSON)
    existing = []
    if target.exists():
        try:
            with target.open("r", encoding="utf-8") as fh:
                existing = json.load(fh)
        except (json.JSONDecodeError, OSError):
            existing = []
    existing_ids = {b["source_id"] for b in existing}
    new_briefs   = [b for b in briefs if b["source_id"] not in existing_ids]
    if dry_run:
        log.info("[dry-run] Would add %d new briefs → %s", len(new_briefs), target)
        return
    combined = existing + new_briefs
    try:
        with target.open("w", encoding="utf-8") as fh:
            json.dump(combined, fh, indent=2, ensure_ascii=False)
        log.info("Content queue: %d total (%d new) → %s", len(combined), len(new_briefs), target)
    except OSError as exc:
        log.error("Failed writing content queue: %s", exc)


def update_status(stats: dict, dry_run: bool = False) -> None:
    _ensure_dirs()
    target = safe_path(STATUS_JSON)
    if dry_run:
        log.info("[dry-run] Would write status → %s", target)
        return
    payload = {**stats, "last_run": datetime.now(timezone.utc).isoformat()}
    try:
        with target.open("w", encoding="utf-8") as fh:
            json.dump(payload, fh, indent=2)
    except OSError as exc:
        log.error("Failed writing status: %s", exc)


# ---------------------------------------------------------------------------
# Converter subprocess
# ---------------------------------------------------------------------------
def invoke_converter(briefs: list, dry_run: bool = False) -> list:
    """
    Pass briefs to engagement_bait_converter.py via subprocess (--stdin-json).
    Returns list of converted result dicts; empty list on skip/error.
    """
    if not briefs:
        log.info("No briefs to convert — skipping converter.")
        return []

    try:
        converter = safe_path(CONVERTER_SCRIPT)
    except ValueError as exc:
        log.error("Converter path unsafe: %s", exc)
        return []

    if not converter.exists():
        log.warning("Converter not found at %s — skipping.", converter)
        return []

    cmd = [sys.executable, str(converter), "--stdin-json"]
    if dry_run:
        log.info("[dry-run] Would invoke: %s  (%d brief(s))", " ".join(cmd), len(briefs))
        return []

    log.info("Invoking converter for %d brief(s)…", len(briefs))
    try:
        result = subprocess.run(
            cmd,
            input=json.dumps(briefs),
            capture_output=True,
            text=True,
            timeout=120,
        )
        if result.returncode != 0:
            log.error("Converter exited %d: %s", result.returncode, result.stderr[:400])
            return []
        try:
            converted = json.loads(result.stdout)
            log.info("Converter returned %d result(s).", len(converted))
            capture_skill_from_result({"converted": converted, "input_briefs": briefs})
            return converted
        except json.JSONDecodeError:
            log.error("Converter output not valid JSON: %.300s", result.stdout)
            return []
    except subprocess.TimeoutExpired:
        log.error("Converter timed out (120 s).")
        return []
    except OSError as exc:
        log.error("Failed to launch converter: %s", exc)
        return []


# ---------------------------------------------------------------------------
# CLI commands
# ---------------------------------------------------------------------------
def cmd_run(dry_run: bool = False) -> int:
    """Execute the full pipeline: collect → score → brief → convert → persist."""
    log.info("=== ai_fatigue_content_router RUN  dry_run=%s ===", dry_run)

    try:
        skills = recall_skills_for_task("ai_fatigue_content_routing")
        if skills:
            log.debug("Recalled %d skill(s).", len(skills))
    except Exception as exc:
        log.debug("recall_skills_for_task failed (non-fatal): %s", exc)

    # 1. Collect raw signals
    signals = collect_signals()
    if not signals:
        log.warning("No signals collected — nothing to do.")
        return 0

    # 2. Score each signal
    for sig in signals:
        sig["fatigue_score"] = score_fatigue(sig)

    high_value = [s for s in signals if s["fatigue_score"] >= FATIGUE_THRESHOLD]
    log.info(
        "%d / %d signals exceed fatigue threshold (%.2f).",
        len(high_value), len(signals), FATIGUE_THRESHOLD,
    )

    # 3. Persist signals to CSV
    save_signals_csv(signals, dry_run=dry_run)

    # 4. Build content briefs for high-value signals
    briefs = [build_content_brief(s) for s in high_value]

    # 5. Route briefs through engagement_bait_converter
    converted = invoke_converter(briefs, dry_run=dry_run)

    # 6. Persist content queue
    save_content_queue(briefs, dry_run=dry_run)

    # 7. Record run stats
    stats = {
        "signals_collected":  len(signals),
        "high_value_signals": len(high_value),
        "briefs_generated":   len(briefs),
        "content_converted":  len(converted),
        "dry_run":            dry_run,
    }
    update_status(stats, dry_run=dry_run)
    log.info("Run complete: %s", stats)
    return 0


def cmd_status() -> int:
    """Print the most recent run status to stdout."""
    try:
        target = safe_path(STATUS_JSON)
    except ValueError as exc:
        log.error("Status path unsafe: %s", exc)
        return 1

    if not target.exists():
        print("No status file found — has the router been run yet?")
        return 1

    try:
        with target.open("r", encoding="utf-8") as fh:
            data = json.load(fh)
        print(json.dumps(data, indent=2))
        return 0
    except (json.JSONDecodeError, OSError) as exc:
        log.error("Could not read status file: %s", exc)
        return 1


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------
def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "PRINTMAXX AI-fatigue content router. "
            "Collects HN/Reddit signals and routes them to engagement_bait_converter.py."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--run",
        action="store_true",
        help="Run the full collect → convert → persist pipeline.",
    )
    group.add_argument(
        "--status",
        action="store_true",
        help="Print the last run status and exit.",
    )
    group.add_argument(
        "--dry-run",
        dest="dry_run",
        action="store_true",
        help="Run the pipeline without writing any files (preview mode).",
    )

    args = parser.parse_args()

    try:
        if args.status:
            sys.exit(cmd_status())
        elif args.run:
            sys.exit(cmd_run(dry_run=False))
        elif args.dry_run:
            sys.exit(cmd_run(dry_run=True))
    except KeyboardInterrupt:
        log.info("Interrupted.")
        sys.exit(130)
    except Exception as exc:
        log.exception("Unhandled exception: %s", exc)
        sys.exit(1)


if __name__ == "__main__":
    main()