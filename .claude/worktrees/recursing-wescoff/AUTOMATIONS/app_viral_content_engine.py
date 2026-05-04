#!/usr/bin/env python3
"""
PRINTMAXX Automation: App Viral Content Engine
===============================================
Generates viral 'builder story' short-form hooks for each live app in APP_FACTORY
using the Cal AI growth pattern: founders-building-for-pain-point narrative,
progress milestones, and raw behind-the-scenes content.

Feeds generated hooks into content_multiplier.py and posting_queue.
Tracks TikTok/IG Reels download velocity correlation.

TYPE: poster
PATTERN: Cal AI — "this story sounds fake but is inspirational" — teenagers
frustrated with calorie tracking build Cal AI using ChatGPT to learn to code,
lean into viral short-form content instead of traditional marketing.
"""

import argparse
import csv
import json
import logging
import subprocess
import sys
import urllib.request
import urllib.error
from datetime import datetime, timezone
from pathlib import Path

# ── Project root ──────────────────────────────────────────────────────────────
PROJECT = Path(__file__).resolve().parent.parent

# ── Import from _common (with local fallbacks) ────────────────────────────────
try:
    from _common import (
        PROJECT as _COMMON_PROJECT,
        safe_path,
        recall_skills_for_task,
        capture_skill_from_result,
    )
    PROJECT = _COMMON_PROJECT
except ImportError:
    def safe_path(path: Path) -> Path:
        """Validate that path is within PROJECT to prevent path traversal."""
        resolved = Path(path).resolve()
        if not str(resolved).startswith(str(PROJECT)):
            raise ValueError(f"Path {resolved} is outside PROJECT root {PROJECT}")
        return resolved

    def recall_skills_for_task(task: str) -> list:
        return []

    def capture_skill_from_result(task: str, result: dict) -> None:
        pass

# ── Canonical paths ───────────────────────────────────────────────────────────
AUTOMATIONS_DIR = PROJECT / "AUTOMATIONS"
LOG_FILE        = AUTOMATIONS_DIR / "logs" / "app_viral_content_engine.log"
APP_FACTORY_DIR = PROJECT / "APP_FACTORY"
OUTPUT_DIR      = AUTOMATIONS_DIR / "viral_content"
QUEUE_FILE      = AUTOMATIONS_DIR / "posting_queue" / "viral_hooks.json"
METRICS_FILE    = AUTOMATIONS_DIR / "logs" / "download_velocity.csv"

# ── Logging ───────────────────────────────────────────────────────────────────

def setup_logging() -> logging.Logger:
    safe_path(LOG_FILE.parent).mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler(safe_path(LOG_FILE), mode="a"),
            logging.StreamHandler(sys.stdout),
        ],
    )
    return logging.getLogger("app_viral_content_engine")

# ── Cal AI Narrative Templates ────────────────────────────────────────────────

_ORIGIN_HOOKS = [
    "we were just {founders} who couldn't stand {pain_point} — so we built an AI to fix it",
    "used chatgpt to learn to code. zero CS background. here's what happened 6 months later",
    "everyone said 'just use the existing apps' — we said 'hold on'",
    "this sounds fake: {founders}, one pain point, one app, millions of impressions",
    "we built the app we actually needed. that's the whole secret.",
    "day 1: idea in my notes app. day 47: 10k downloads. this is not a normal story",
    "i was terrible at code. chatgpt basically became my co-founder",
    "instead of giving up on {pain_point}, we shipped. here's what we learned",
]

_MILESTONE_TEMPLATES = [
    "day {day}: just hit {metric} — {reaction}",
    "{metric} in {timeframe}. still can't believe it.",
    "when we crossed {metric}, we cried. genuine tears.",
    "nobody believed we could hit {metric}. update: we hit it.",
    "{metric} users and none of them are our moms (we checked)",
]

_MILESTONES = [
    {"day": 7,   "metric": "100 downloads",   "timeframe": "first week",   "reaction": "screamed into a pillow"},
    {"day": 30,  "metric": "1k users",        "timeframe": "one month",    "reaction": "couldn't sleep"},
    {"day": 60,  "metric": "10k downloads",   "timeframe": "two months",   "reaction": "quit our part-time jobs"},
    {"day": 90,  "metric": "50k users",       "timeframe": "three months", "reaction": "got our first press hit"},
    {"day": 180, "metric": "500k downloads",  "timeframe": "six months",   "reaction": "started getting acquisition offers"},
]

_BEHIND_THE_SCENES = [
    "the app crashed on launch day. we fixed it in 4 hours from a Starbucks",
    "our first 'viral' video got 200 views. we made 47 more anyway",
    "we DM'd every single early user and asked what sucked. most things sucked.",
    "the feature everyone loves? we almost cut it to ship faster",
    "our 'office' was a bedroom. two monitors, one dream, too much caffeine",
    "we used chatgpt to write code we didn't understand — then learned what it meant",
    "rejected from every accelerator we applied to. we shipped anyway.",
    "the version that went viral was version 11. versions 1–10 were disasters",
    "we gave it away free for 60 days. that's how we got word of mouth",
    "our growth hack was: make something people actually want and talk about it honestly",
]

_PAIN_POINT_NARRATIVES = [
    "existing apps made {pain_point} feel like a chore. we made it feel like a superpower.",
    "we were the target user. that made everything easier.",
    "the pain was real. the solution was scrappy. the growth was real.",
    "we built it because nothing else did exactly what we needed.",
    "founder-market fit isn't a buzzword when you live the problem every day",
]

_PLATFORM_HASHTAG_BASE = ["#buildinpublic", "#indiedev", "#startuplife", "#founderjourney"]

# ── Hook Generation ───────────────────────────────────────────────────────────

def _app_slug(name: str) -> str:
    return name.lower().replace(" ", "").replace("/", "")


def generate_builder_story_hooks(app: dict) -> list[dict]:
    """Generate a full Cal AI–pattern hook set for one live app."""
    name       = app.get("name", "App")
    pain_point = app.get("pain_point", "frustrating existing workflows")
    founders   = app.get("founders", "a small team of builders")
    launched   = app.get("launched_date", "recently")
    slug       = _app_slug(name)
    tag        = f"#{slug}"
    now        = datetime.now(timezone.utc).isoformat()
    hooks: list[dict] = []

    # ── Origin story ──────────────────────────────────────────────────────────
    for template in _ORIGIN_HOOKS[:4]:
        hooks.append({
            "app":       name,
            "type":      "origin_story",
            "platform":  ["tiktok", "ig_reels"],
            "hook":      template.format(founders=founders, pain_point=pain_point),
            "cta":       f"follow to watch us build {name} live",
            "hashtags":  _PLATFORM_HASHTAG_BASE + [tag],
            "generated": now,
        })

    # ── Milestone reveals ─────────────────────────────────────────────────────
    for i, ms in enumerate(_MILESTONES[:3]):
        template = _MILESTONE_TEMPLATES[i % len(_MILESTONE_TEMPLATES)]
        hooks.append({
            "app":       name,
            "type":      "milestone",
            "platform":  ["tiktok", "ig_reels", "twitter"],
            "hook":      template.format(**ms),
            "body":      f"here's exactly what we did to get {name} to {ms['metric']}",
            "cta":       "comment your questions — we answer every one",
            "hashtags":  ["#milestones", "#startupgrowth", "#buildinpublic", tag],
            "generated": now,
        })

    # ── Raw behind-the-scenes ─────────────────────────────────────────────────
    for bts in _BEHIND_THE_SCENES[:3]:
        hooks.append({
            "app":       name,
            "type":      "behind_the_scenes",
            "platform":  ["tiktok", "ig_reels"],
            "hook":      bts,
            "body":      f"nobody shows this part of building {name}. we're showing it.",
            "cta":       "save this if you're building something",
            "hashtags":  ["#rawfounder", "#buildinpublic", "#realtalk", tag],
            "generated": now,
        })

    # ── Pain-point narrative ──────────────────────────────────────────────────
    for pp in _PAIN_POINT_NARRATIVES[:2]:
        hooks.append({
            "app":       name,
            "type":      "pain_point_narrative",
            "platform":  ["tiktok", "ig_reels", "twitter"],
            "hook":      pp.format(pain_point=pain_point),
            "body":      f"so we built {name}. launched {launched}. here's what happened.",
            "cta":       "link in bio — try it free",
            "hashtags":  ["#productmarket", "#buildinpublic", tag],
            "generated": now,
        })

    return hooks

# ── APP_FACTORY Loader ────────────────────────────────────────────────────────

def load_live_apps(log: logging.Logger) -> list[dict]:
    """Discover live apps from APP_FACTORY. Falls back to demo app."""
    apps: list[dict] = []
    try:
        factory = safe_path(APP_FACTORY_DIR)
        if not factory.exists():
            log.warning("APP_FACTORY not found: %s", factory)
            return _demo_apps()

        # Prefer a top-level apps.json index
        index = factory / "apps.json"
        if index.exists():
            with open(safe_path(index)) as f:
                data = json.load(f)
            apps = [a for a in data if a.get("status") == "live"]
            log.info("Loaded %d live app(s) from apps.json", len(apps))
            return apps

        # Fall back: scan sub-directories for app.json manifests
        for subdir in sorted(factory.iterdir()):
            if not subdir.is_dir():
                continue
            manifest = subdir / "app.json"
            if not manifest.exists():
                continue
            try:
                with open(safe_path(manifest)) as f:
                    meta = json.load(f)
                if meta.get("status") == "live":
                    apps.append(meta)
                    log.info("Found live app: %s", meta.get("name", subdir.name))
            except (json.JSONDecodeError, OSError) as exc:
                log.warning("Skipping bad manifest %s: %s", manifest, exc)

    except (OSError, ValueError) as exc:
        log.error("Failed scanning APP_FACTORY: %s", exc)

    return apps if apps else _demo_apps()


def _demo_apps() -> list[dict]:
    return [{
        "name":          "Cal AI",
        "description":   "AI-powered calorie tracker",
        "pain_point":    "tedious manual calorie logging",
        "founders":      "two frustrated teenagers",
        "launched_date": "6 months ago",
        "analytics_api_url": "",
        "status":        "live",
    }]

# ── Download Velocity ─────────────────────────────────────────────────────────

def fetch_velocity(app: dict, log: logging.Logger) -> dict[str, int]:
    """Fetch download counts from app analytics API (stub-safe)."""
    velocity = {"tiktok": 0, "ig_reels": 0}
    api_url  = app.get("analytics_api_url", "")
    if not api_url:
        return velocity
    try:
        req = urllib.request.Request(api_url, headers={"User-Agent": "PRINTMAXX/1.0"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode())
        velocity["tiktok"]   = int(data.get("tiktok_downloads", 0))
        velocity["ig_reels"] = int(data.get("ig_reels_downloads", 0))
    except (urllib.error.URLError, json.JSONDecodeError, OSError, ValueError) as exc:
        log.warning("Velocity API failed for %s: %s", app.get("name"), exc)
    return velocity


def record_velocity(app_name: str, platform: str, downloads: int,
                    log: logging.Logger, dry_run: bool = False) -> None:
    """Append one velocity row to the CSV metrics log."""
    try:
        safe_path(METRICS_FILE.parent).mkdir(parents=True, exist_ok=True)
        row = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "app":       app_name,
            "platform":  platform,
            "downloads": downloads,
            "hook_posted": True,
        }
        if dry_run:
            log.info("[DRY-RUN] velocity row: %s", row)
            return
        write_header = not METRICS_FILE.exists()
        with open(safe_path(METRICS_FILE), "a", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=list(row.keys()))
            if write_header:
                writer.writeheader()
            writer.writerow(row)
        log.info("Velocity recorded: %s / %s = %d", app_name, platform, downloads)
    except (OSError, ValueError) as exc:
        log.error("Failed to record velocity (%s/%s): %s", app_name, platform, exc)

# ── Posting Queue ─────────────────────────────────────────────────────────────

def write_posting_queue(hooks: list[dict], log: logging.Logger, dry_run: bool = False) -> None:
    """Merge hooks into the persistent posting queue JSON."""
    try:
        safe_path(QUEUE_FILE.parent).mkdir(parents=True, exist_ok=True)
        existing: list[dict] = []
        if QUEUE_FILE.exists():
            with open(safe_path(QUEUE_FILE)) as f:
                try:
                    existing = json.load(f)
                except json.JSONDecodeError:
                    existing = []
        combined = existing + hooks
        if dry_run:
            log.info("[DRY-RUN] Would write %d hooks to posting queue", len(combined))
            return
        with open(safe_path(QUEUE_FILE), "w") as f:
            json.dump(combined, f, indent=2)
        log.info("Posting queue updated: %d total hooks → %s", len(combined), QUEUE_FILE)
    except (OSError, ValueError) as exc:
        log.error("Failed to write posting queue: %s", exc)


def write_app_hooks_file(app_name: str, hooks: list[dict],
                         log: logging.Logger, dry_run: bool = False) -> Path | None:
    """Write per-app hooks file to OUTPUT_DIR. Returns path on success."""
    try:
        safe_path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)
        slug  = app_name.lower().replace(" ", "_").replace("/", "_")
        ts    = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        path  = OUTPUT_DIR / f"{slug}_hooks_{ts}.json"
        if dry_run:
            log.info("[DRY-RUN] Would write %d hooks → %s", len(hooks), path)
            return None
        with open(safe_path(path), "w") as f:
            json.dump(hooks, f, indent=2)
        log.info("Wrote %d hooks for '%s' → %s", len(hooks), app_name, path)
        return path
    except (OSError, ValueError) as exc:
        log.error("Failed to write hooks file for %s: %s", app_name, exc)
        return None

# ── content_multiplier.py Integration ────────────────────────────────────────

def invoke_content_multiplier(hooks_file: Path, log: logging.Logger, dry_run: bool = False) -> None:
    """Subprocess-call content_multiplier.py with the latest hooks file."""
    multiplier = AUTOMATIONS_DIR / "content_multiplier.py"
    if not multiplier.exists():
        log.warning("content_multiplier.py not found at %s — skipping", multiplier)
        return
    cmd = [sys.executable, str(safe_path(multiplier)), "--input", str(safe_path(hooks_file)), "--run"]
    if dry_run:
        log.info("[DRY-RUN] Would invoke: %s", " ".join(cmd))
        return
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        if result.returncode == 0:
            log.info("content_multiplier.py succeeded")
        else:
            log.error("content_multiplier.py exited %d: %s", result.returncode, result.stderr.strip())
    except subprocess.TimeoutExpired:
        log.error("content_multiplier.py timed out")
    except OSError as exc:
        log.error("Failed to invoke content_multiplier.py: %s", exc)

# ── Status Report ─────────────────────────────────────────────────────────────

def print_status(log: logging.Logger) -> None:
    log.info("=== APP VIRAL CONTENT ENGINE — STATUS ===")

    if QUEUE_FILE.exists():
        try:
            with open(safe_path(QUEUE_FILE)) as f:
                queued = json.load(f)
            log.info("Posting queue: %d hooks pending", len(queued))
            by_type: dict[str, int] = {}
            for h in queued:
                t = h.get("type", "unknown")
                by_type[t] = by_type.get(t, 0) + 1
            for htype, count in sorted(by_type.items()):
                log.info("  %-32s %d", htype, count)
        except (json.JSONDecodeError, OSError) as exc:
            log.warning("Could not read queue: %s", exc)
    else:
        log.info("Posting queue: not yet created")

    if METRICS_FILE.exists():
        try:
            with open(safe_path(METRICS_FILE)) as f:
                rows = list(csv.DictReader(f))
            apps_seen = sorted({r.get("app", "") for r in rows})
            log.info("Velocity log: %d records | apps: %s", len(rows), ", ".join(apps_seen))
        except (OSError, csv.Error) as exc:
            log.warning("Could not read velocity log: %s", exc)
    else:
        log.info("Velocity log: not yet created")

    if OUTPUT_DIR.exists():
        recent = sorted(OUTPUT_DIR.glob("*_hooks_*.json"), reverse=True)[:5]
        log.info("Recent output files (%d):", len(recent))
        for p in recent:
            log.info("  %s", p.name)
    else:
        log.info("Output directory: not yet created")

# ── CLI ───────────────────────────────────────────────────────────────────────

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="PRINTMAXX: App Viral Content Engine — Cal AI–pattern builder story hooks"
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--run",     action="store_true",
                       help="Generate and queue viral hooks for all live apps")
    group.add_argument("--status",  action="store_true",
                       help="Show status of queued hooks and velocity metrics")
    group.add_argument("--dry-run", action="store_true", dest="dry_run",
                       help="Simulate run without writing any files")
    return parser.parse_args()

# ── Entry point ───────────────────────────────────────────────────────────────

def main() -> None:
    args = parse_args()
    log  = setup_logging()
    mode = "dry-run" if args.dry_run else ("status" if args.status else "run")
    log.info("PRINTMAXX App Viral Content Engine starting — mode: %s", mode)

    try:
        skills = recall_skills_for_task("generate viral short-form builder story hooks")
        if skills:
            log.info("Recalled %d skill(s) for task", len(skills))
    except Exception as exc:
        log.debug("recall_skills_for_task unavailable: %s", exc)

    if args.status:
        print_status(log)
        return

    dry_run = args.dry_run
    apps    = load_live_apps(log)

    if not apps:
        log.error("No apps resolved — exiting")
        sys.exit(1)

    all_hooks:       list[dict]  = []
    latest_out_file: Path | None = None

    for app in apps:
        name = app.get("name", "Unknown")
        log.info("Processing app: %s", name)
        try:
            hooks = generate_builder_story_hooks(app)
            log.info("  Generated %d hooks", len(hooks))
            all_hooks.extend(hooks)

            out = write_app_hooks_file(name, hooks, log, dry_run=dry_run)
            if out:
                latest_out_file = out

            velocity = fetch_velocity(app, log)
            for platform, count in velocity.items():
                record_velocity(name, platform, count, log, dry_run=dry_run)

            try:
                capture_skill_from_result(
                    "generate viral short-form builder story hooks",
                    {"app": name, "hook_count": len(hooks),
                     "types": sorted({h["type"] for h in hooks})},
                )
            except Exception as exc:
                log.debug("capture_skill_from_result unavailable: %s", exc)

        except Exception as exc:
            log.error("Error processing '%s': %s", name, exc)
            continue

    if all_hooks:
        write_posting_queue(all_hooks, log, dry_run=dry_run)

    if latest_out_file:
        invoke_content_multiplier(latest_out_file, log, dry_run=dry_run)
    elif dry_run and all_hooks:
        invoke_content_multiplier(OUTPUT_DIR / "dry_run_hooks.json", log, dry_run=True)

    log.info(
        "Complete — %d hook(s) generated across %d app(s)",
        len(all_hooks), len(apps),
    )


if __name__ == "__main__":
    main()