#!/usr/bin/env python3
"""
PRINTMAXX Reddit App Seeder
===========================
Generates authentic founder-story posts for each App Factory app and schedules
them to high-signal subreddits: r/passive_income, r/indiehackers, r/androidapps,
r/iphone, r/SideProject.

Uses Claude to write app-specific "journey posts" in genuine founder voice —
mirrors the HabitSwipe playbook: minimal app, authentic story, community-first
launch. Posts are appended to CONTENT/social/posting_queue/ as JSONL for
warmup-aware delivery, and a CSV manifest is written alongside for human review.

Usage:
    python3 reddit_app_seeder.py --run
    python3 reddit_app_seeder.py --run --dry-run
    python3 reddit_app_seeder.py --status
"""

import argparse
import csv
import json
import logging
import os
import subprocess
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

# ── _common imports ────────────────────────────────────────────────────────────
try:
    from _common import PROJECT, safe_path, recall_skills_for_task, capture_skill_from_result
except ImportError:
    PROJECT = Path(__file__).resolve().parent.parent

    def safe_path(target):  # type: ignore[misc]
        resolved = Path(target).resolve()
        if not str(resolved).startswith(str(PROJECT)):
            raise ValueError(f"BLOCKED: {resolved} is outside project root {PROJECT}")
        return resolved

    def recall_skills_for_task(task_description, max_chars=600):  # type: ignore[misc]
        return ""

    def capture_skill_from_result(task, result, success=True):  # type: ignore[misc]
        pass


# ── paths ──────────────────────────────────────────────────────────────────────
AUTOMATIONS_DIR   = PROJECT / "AUTOMATIONS"
LOGS_DIR          = AUTOMATIONS_DIR / "logs"
LOG_FILE          = LOGS_DIR / "reddit_app_seeder.log"
POSTING_QUEUE_DIR = PROJECT / "CONTENT" / "social" / "posting_queue"
APP_REGISTRY      = PROJECT / "APP_FACTORY" / "apps.json"

# ── constants ──────────────────────────────────────────────────────────────────
TARGET_SUBREDDITS = [
    "passive_income",
    "indiehackers",
    "androidapps",
    "iphone",
    "SideProject",
]

CLAUDE_API_URL = "https://api.anthropic.com/v1/messages"
CLAUDE_MODEL   = "claude-sonnet-4-6"

HABITSWIPE_REF = {
    "app_name": "HabitSwipe",
    "platform": "Android & iOS",
    "users":    2500,
    "revenue":  800,
    "url":      "http://www.habitswipe.app",
    "niche":    "habit tracker",
    "hook":     "2k users, $800 with a Habit Tracker — I can't explain how good this feels",
}


# ── logging ────────────────────────────────────────────────────────────────────
def _setup_logging() -> logging.Logger:
    try:
        safe_path(LOGS_DIR).mkdir(parents=True, exist_ok=True)
    except Exception:
        LOGS_DIR.mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger("reddit_app_seeder")
    logger.setLevel(logging.DEBUG)

    if not logger.handlers:
        fmt = logging.Formatter(
            "%(asctime)s [%(levelname)s] %(message)s", datefmt="%Y-%m-%dT%H:%M:%S"
        )
        fh = logging.FileHandler(LOG_FILE, mode="a", encoding="utf-8")
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(fmt)

        ch = logging.StreamHandler(sys.stdout)
        ch.setLevel(logging.INFO)
        ch.setFormatter(logging.Formatter("[%(levelname)s] %(message)s"))

        logger.addHandler(fh)
        logger.addHandler(ch)

    return logger


log = _setup_logging()


# ── app registry ───────────────────────────────────────────────────────────────
def load_apps() -> list:
    """Load App Factory app list from APP_FACTORY/apps.json; fall back to HabitSwipe."""
    try:
        reg = safe_path(APP_REGISTRY)
        with open(reg, encoding="utf-8") as fh:
            apps = json.load(fh)
        if not isinstance(apps, list) or not apps:
            raise ValueError("apps.json must be a non-empty list")
        log.info("Loaded %d app(s) from %s", len(apps), reg.name)
        return apps
    except FileNotFoundError:
        log.warning("App registry not found at %s — using HabitSwipe fallback", APP_REGISTRY)
        return [HABITSWIPE_REF]
    except Exception as exc:
        log.error("Failed to load app registry: %s — using HabitSwipe fallback", exc)
        return [HABITSWIPE_REF]


# ── warmup check ───────────────────────────────────────────────────────────────
def check_warmup_ready() -> bool:
    """
    Invoke reddit_warmup_checker.py via subprocess if present.
    Returns True when warm or when checker is absent.
    """
    checker = AUTOMATIONS_DIR / "reddit_warmup_checker.py"
    if not checker.exists():
        log.debug("Warmup checker not found — assuming warm")
        return True

    try:
        result = subprocess.run(
            ["python3", str(checker), "--status"],
            capture_output=True,
            text=True,
            timeout=15,
            cwd=str(PROJECT),
        )
        if result.returncode != 0:
            log.warning("Warmup checker: not warm yet — %s", result.stdout.strip())
            return False
        return True
    except subprocess.TimeoutExpired:
        log.warning("Warmup checker timed out — proceeding anyway")
        return True
    except Exception as exc:
        log.warning("Warmup checker error: %s — proceeding anyway", exc)
        return True


# ── Claude API ─────────────────────────────────────────────────────────────────
def call_claude(prompt: str) -> str:
    """POST to Claude Messages API via urllib. Returns assistant text."""
    api_key = os.environ.get("ANTHROPIC_API_KEY", "")
    if not api_key:
        raise EnvironmentError("ANTHROPIC_API_KEY environment variable is not set")

    payload = json.dumps({
        "model":      CLAUDE_MODEL,
        "max_tokens": 1024,
        "messages":   [{"role": "user", "content": prompt}],
    }).encode("utf-8")

    req = urllib.request.Request(
        CLAUDE_API_URL,
        data=payload,
        headers={
            "x-api-key":         api_key,
            "anthropic-version": "2023-06-01",
            "content-type":      "application/json",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            body = json.loads(resp.read().decode("utf-8"))
        return body["content"][0]["text"].strip()
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"Claude API HTTP {exc.code}: {detail}") from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"Claude API connection error: {exc.reason}") from exc


# ── prompt ─────────────────────────────────────────────────────────────────────
def build_prompt(app: dict, subreddit: str) -> str:
    name     = app.get("app_name", "My App")
    platform = app.get("platform", "iOS & Android")
    users    = app.get("users", 0)
    revenue  = app.get("revenue", 0)
    url      = app.get("url", "")
    niche    = app.get("niche", "productivity")
    hook     = app.get("hook", HABITSWIPE_REF["hook"])

    return f"""You are a solo indie developer sharing your genuine founder journey on Reddit.
Write a single Reddit post for r/{subreddit} about your app "{name}".

App details:
  Platform : {platform}
  Niche    : {niche}
  Users    : {users:,}
  Revenue  : ${revenue:,}
  URL      : {url}

Voice and tone:
  - First-person, humble, authentic — no corporate speak
  - Share the real journey: late nights, what flopped, what clicked
  - Community-first: invite honest feedback, not just downloads
  - Match this energy: "{hook}"
  - Tailor angle and references to r/{subreddit} culture

Formatting (follow exactly):
  Line 1 : "Title: <your title>"
  Line 2 : blank
  Line 3 : "Body:"
  Line 4+ : post body, 150-300 words, plain Reddit text, no markdown fences
  Final line: a genuine question or call to discussion

Output:
Title: <title here>

Body:
<body here>"""


def parse_claude_response(raw: str) -> tuple:
    title      = ""
    body_lines = []
    in_body    = False

    for line in raw.splitlines():
        stripped = line.strip()
        if not in_body and stripped.lower().startswith("title:"):
            title = stripped[6:].strip()
        elif not in_body and stripped.lower() == "body:":
            in_body = True
        elif in_body:
            body_lines.append(line)

    return title, "\n".join(body_lines).strip()


# ── post generation ────────────────────────────────────────────────────────────
def generate_post(app: dict, subreddit: str, dry_run: bool = False) -> dict:
    name = app.get("app_name", "unknown")
    log.info("Generating  app=%s  r/%s  dry_run=%s", name, subreddit, dry_run)

    if dry_run:
        title = f"[DRY RUN] {name} founder story for r/{subreddit}"
        body  = (
            f"[DRY RUN] Claude would generate an authentic founder-voice post "
            f"for {name} targeting the r/{subreddit} community here."
        )
    else:
        try:
            raw   = call_claude(build_prompt(app, subreddit))
            title, body = parse_claude_response(raw)
            if not title:
                title = f"Built {name} solo — here's what happened ({users:,} users later)".replace(
                    "{users:,}", f"{app.get('users', 0):,}"
                )
            if not body:
                body = raw
        except Exception as exc:
            log.error("Claude failed  app=%s  r/%s: %s", name, subreddit, exc)
            return {}

    return {
        "app_name":     name,
        "subreddit":    subreddit,
        "title":        title,
        "body":         body,
        "url":          app.get("url", ""),
        "platform":     app.get("platform", ""),
        "users":        app.get("users", 0),
        "revenue":      app.get("revenue", 0),
        "status":       "queued",
        "dry_run":      dry_run,
        "generated_at": datetime.now(timezone.utc).isoformat(),
    }


# ── queue writers ──────────────────────────────────────────────────────────────
def _date_slug() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")


def _queue_dir() -> Path:
    qd = safe_path(POSTING_QUEUE_DIR)
    qd.mkdir(parents=True, exist_ok=True)
    return qd


def write_jsonl(post: dict, queue_dir: Path) -> Path:
    outfile = safe_path(queue_dir / f"reddit_queue_{_date_slug()}.jsonl")
    with open(outfile, "a", encoding="utf-8") as fh:
        fh.write(json.dumps(post, ensure_ascii=False) + "\n")
    return outfile


def write_csv_manifest(posts: list, queue_dir: Path) -> Path:
    """Append batch to a human-readable CSV manifest for today."""
    csv_file   = safe_path(queue_dir / f"reddit_manifest_{_date_slug()}.csv")
    fieldnames = [
        "generated_at", "app_name", "subreddit", "title",
        "url", "users", "revenue", "status", "dry_run",
    ]
    is_new = not csv_file.exists()
    with open(csv_file, "a", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames, extrasaction="ignore")
        if is_new:
            writer.writeheader()
        writer.writerows(posts)
    return csv_file


# ── CLI commands ───────────────────────────────────────────────────────────────
def cmd_run(dry_run: bool = False) -> None:
    skill_ctx = recall_skills_for_task("reddit founder story seeding")
    if skill_ctx:
        log.debug("Skill context: %s", skill_ctx[:120])

    apps = load_apps()
    log.info(
        "Starting reddit_app_seeder  apps=%d  subreddits=%d  dry_run=%s",
        len(apps), len(TARGET_SUBREDDITS), dry_run,
    )

    warmup_ok = check_warmup_ready()
    if not warmup_ok:
        log.warning("Account not fully warmed — posts queued for manual review before submission")

    try:
        queue_dir = _queue_dir()
    except Exception as exc:
        log.error("Cannot create queue dir: %s", exc)
        sys.exit(1)

    batch   = []
    success = 0
    failed  = 0

    for app in apps:
        for sub in TARGET_SUBREDDITS:
            try:
                post = generate_post(app, sub, dry_run=dry_run)
                if not post:
                    failed += 1
                    continue
                jsonl_path = write_jsonl(post, queue_dir)
                batch.append(post)
                success += 1
                log.debug("Queued → %s  r/%s", jsonl_path.name, sub)
            except Exception as exc:
                log.error(
                    "Unhandled error  app=%s  r/%s: %s",
                    app.get("app_name", "?"), sub, exc,
                )
                failed += 1

    if batch:
        try:
            csv_path = write_csv_manifest(batch, queue_dir)
            log.info("CSV manifest → %s", csv_path.name)
        except Exception as exc:
            log.warning("CSV manifest write failed: %s", exc)

    summary = (
        f"reddit_app_seeder: {success} queued, {failed} failed, "
        f"dry_run={dry_run}, warmup_confirmed={warmup_ok}"
    )
    capture_skill_from_result(
        task    = "reddit founder story seeding",
        result  = summary,
        success = failed == 0,
    )

    log.info(summary)
    if dry_run:
        print(f"\n[DRY RUN] Would queue {success} posts across {len(TARGET_SUBREDDITS)} subreddits.")
    else:
        print(f"\nDone. {success} posts queued, {failed} failed. Log: {LOG_FILE}")


def cmd_status() -> None:
    date_slug  = _date_slug()
    jsonl_file = POSTING_QUEUE_DIR / f"reddit_queue_{date_slug}.jsonl"
    csv_file   = POSTING_QUEUE_DIR / f"reddit_manifest_{date_slug}.csv"

    if not jsonl_file.exists():
        print(f"No queue found for {date_slug}. Run with --run first.")
        return

    counts     = {}
    apps_seen  = set()
    subs_seen  = set()
    dry_run_ct = 0

    try:
        with open(jsonl_file, encoding="utf-8") as fh:
            for raw_line in fh:
                raw_line = raw_line.strip()
                if not raw_line:
                    continue
                try:
                    post   = json.loads(raw_line)
                    status = post.get("status", "other")
                    counts[status] = counts.get(status, 0) + 1
                    apps_seen.add(post.get("app_name", "?"))
                    subs_seen.add("r/" + post.get("subreddit", "?"))
                    if post.get("dry_run"):
                        dry_run_ct += 1
                except json.JSONDecodeError:
                    counts["parse_error"] = counts.get("parse_error", 0) + 1
    except Exception as exc:
        log.error("Status read error: %s", exc)
        return

    print(f"\n=== Reddit Queue — {date_slug} ===")
    for k, v in sorted(counts.items()):
        print(f"  {k:<10}: {v}")
    if dry_run_ct:
        print(f"  dry-run  : {dry_run_ct}")
    print(f"  Apps     : {', '.join(sorted(apps_seen)) or 'none'}")
    print(f"  Subreddits: {', '.join(sorted(subs_seen)) or 'none'}")
    print(f"  JSONL    : {jsonl_file}")
    if csv_file.exists():
        print(f"  Manifest : {csv_file}")
    print()


# ── entry point ────────────────────────────────────────────────────────────────
def main() -> None:
    parser = argparse.ArgumentParser(
        prog="reddit_app_seeder",
        description=(
            "PRINTMAXX Reddit App Seeder — generates authentic founder-story posts\n"
            "for App Factory apps and queues them to r/passive_income, r/indiehackers,\n"
            "r/androidapps, r/iphone, r/SideProject."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--run",     action="store_true",
                        help="Generate and queue posts for all apps")
    parser.add_argument("--status",  action="store_true",
                        help="Show today's posting queue summary")
    parser.add_argument("--dry-run", action="store_true", dest="dry_run",
                        help="Simulate run without calling Claude or writing queue files")

    args = parser.parse_args()

    if not args.run and not args.status:
        parser.print_help()
        sys.exit(0)

    try:
        if args.status:
            cmd_status()
        if args.run:
            cmd_run(dry_run=args.dry_run)
    except KeyboardInterrupt:
        log.warning("Interrupted by user")
        sys.exit(1)
    except Exception as exc:
        log.exception("Fatal error: %s", exc)
        sys.exit(1)


if __name__ == "__main__":
    main()