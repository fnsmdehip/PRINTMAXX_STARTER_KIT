#!/usr/bin/env python3
"""
PRINTMAXX Automation: ph_launch_mindspend_content.py

Routes Mindspend PH launch angle through engagement_bait_converter.py to generate
emotional-spending content (threads, Reddit posts, Twitter hooks). Simultaneously
queues an emotional-finance PWA spec into the App Factory pipeline as a 1-day
vibe-code competitor build.

TYPE: poster
METHOD CONTEXT: [PH LAUNCH] Mindspend: Track how you feel about spending, not just the numbers
"""

import argparse
import csv
import json
import subprocess
import sys
import urllib.request
import urllib.error
from datetime import datetime
from pathlib import Path

try:
    from _common import PROJECT, safe_path, recall_skills_for_task, capture_skill_from_result
except ImportError:
    PROJECT = Path(__file__).resolve().parent.parent

    def safe_path(p):
        resolved = Path(p).resolve()
        if not str(resolved).startswith(str(PROJECT)):
            raise ValueError(f"Path escape attempt blocked: {resolved} is outside {PROJECT}")
        return resolved

    def recall_skills_for_task(task_name):
        return []

    def capture_skill_from_result(result, skill_name):
        return result


LOG_PATH = PROJECT / "AUTOMATIONS" / "logs" / "ph_launch_mindspend_content.log"

PH_LAUNCH_ANGLE = (
    "[PH LAUNCH] Mindspend: Track how you feel about spending, not just the numbers"
)

CONTENT_OUTPUT_DIR = PROJECT / "AUTOMATIONS" / "output" / "mindspend_ph_launch"
APP_FACTORY_QUEUE = PROJECT / "AUTOMATIONS" / "app_factory" / "queue"
ENGAGEMENT_CONVERTER = PROJECT / "AUTOMATIONS" / "engagement_bait_converter.py"

CONTENT_TEMPLATES = {
    "twitter_hook": [
        "Most budgeting apps track dollars. Mindspend tracks your feelings. "
        "Because guilt and joy are what actually drive your spending. 🧵",
        "You already know how much you spent. But do you know WHY you felt okay spending it? "
        "Mindspend just launched on Product Hunt 🚀",
        "Every purchase has an emotion behind it. Mindspend makes that visible — "
        "and it just launched on Product Hunt today.",
        "Broke again at the end of the month? It's not a math problem. It's an emotional pattern. "
        "Mindspend shows you both. Launching on PH now 👇",
    ],
    "reddit_post": [
        {
            "subreddit": "r/personalfinance",
            "title": "I built a spending tracker that logs your emotional state at purchase time — PH launch today",
            "body": (
                "Most budgeting tools show you the numbers. Mindspend adds an emotional layer: "
                "you rate how you felt before and after each purchase — stressed, bored, happy, anxious.\n\n"
                "Over time it surfaces patterns: 'You spend $200+ when stressed at work.' "
                "'Retail therapy spikes every Sunday evening.'\n\n"
                "Would love feedback from this community. Launching on Product Hunt today:\n"
                "https://producthunt.com/posts/mindspend\n\n"
                "Happy to answer any questions about the build or the concept."
            ),
        },
        {
            "subreddit": "r/Entrepreneur",
            "title": "Launched Mindspend today: emotional-finance tracker — here's the 30-day build story",
            "body": (
                "30 days ago I had a simple thesis: people don't overspend because they lack information, "
                "they overspend because of how they feel.\n\n"
                "So I built Mindspend — a PWA that layers emotional check-ins onto every transaction. "
                "You log a mood, it builds a pattern.\n\n"
                "Today it's live on Product Hunt. Would appreciate your support and brutal feedback.\n"
                "https://producthunt.com/posts/mindspend"
            ),
        },
    ],
    "thread": [
        "1/ Your budget app is lying to you. Not about the numbers — those are fine. "
        "It's lying about WHY you're spending. Thread 🧵",
        "2/ Every financial decision is emotionally driven. Stress purchases. Boredom scrolling Amazon. "
        "Celebratory splurges. Your spreadsheet doesn't capture any of that.",
        "3/ Mindspend does. It's a spending tracker that asks: 'How do you feel right now?' "
        "before logging a purchase. Just launched on Product Hunt.",
        "4/ After 30 days you get a map. Not just 'I spent $400 on food' but "
        "'I spent $400 on food, 60% of it when I was stressed or lonely.'",
        "5/ That's the lever. Not willpower. Pattern recognition. "
        "Check it out → https://producthunt.com/posts/mindspend",
    ],
}

PWA_SPEC = {
    "project_name": "Mindspend",
    "type": "PWA",
    "build_timeline": "1-day vibe-code",
    "stack": ["React", "TypeScript", "IndexedDB", "Service Worker", "Tailwind CSS"],
    "core_features": [
        "Transaction logging with pre/post emotional state rating (1–5 scale + tag)",
        "Emotion categories: stressed, bored, happy, anxious, celebratory, guilty, neutral",
        "Spending pattern analytics: emotion vs. spend amount over time",
        "Weekly emotional-spend digest (push notification via Service Worker)",
        "Offline-first via IndexedDB sync",
        "CSV export of transactions + emotion log",
        "Simple onboarding: connect bank via Plaid (optional) or manual entry",
    ],
    "differentiator": (
        "Competitor trackers (YNAB, Copilot, Monarch) track dollars. "
        "Mindspend tracks the emotional trigger behind every dollar."
    ),
    "target_user": "Millennials/Gen Z who understand their overspending is emotional, not informational",
    "ph_launch_hook": PH_LAUNCH_ANGLE,
    "app_factory_priority": "high",
    "queued_at": datetime.utcnow().isoformat(),
}


def log(message: str, dry_run: bool = False) -> None:
    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    prefix = "[DRY-RUN] " if dry_run else ""
    line = f"[{timestamp}] {prefix}{message}"
    print(line, flush=True)
    try:
        log_file = safe_path(LOG_PATH)
        log_file.parent.mkdir(parents=True, exist_ok=True)
        with log_file.open("a", encoding="utf-8") as f:
            f.write(line + "\n")
    except Exception as e:
        print(f"[WARN] Could not write to log: {e}", file=sys.stderr)


def write_json(path: Path, data: dict, dry_run: bool = False) -> bool:
    try:
        safe = safe_path(path)
        if dry_run:
            log(f"DRY-RUN: would write JSON to {safe}", dry_run=True)
            return True
        safe.parent.mkdir(parents=True, exist_ok=True)
        with safe.open("w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        log(f"Wrote JSON: {safe}")
        return True
    except Exception as e:
        log(f"ERROR writing JSON to {path}: {e}")
        return False


def write_csv(path: Path, rows: list, fieldnames: list, dry_run: bool = False) -> bool:
    try:
        safe = safe_path(path)
        if dry_run:
            log(f"DRY-RUN: would write CSV ({len(rows)} rows) to {safe}", dry_run=True)
            return True
        safe.parent.mkdir(parents=True, exist_ok=True)
        with safe.open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)
        log(f"Wrote CSV: {safe}")
        return True
    except Exception as e:
        log(f"ERROR writing CSV to {path}: {e}")
        return False


def run_engagement_converter(angle: str, output_dir: Path, dry_run: bool = False) -> dict:
    """Pass the PH launch angle to engagement_bait_converter.py if it exists."""
    result = {"status": "skipped", "output": None, "error": None}
    try:
        converter = safe_path(ENGAGEMENT_CONVERTER)
        if not converter.exists():
            log(f"engagement_bait_converter.py not found at {converter} — generating content directly")
            result["status"] = "converter_missing"
            return result

        safe_out = safe_path(output_dir)
        cmd = [
            sys.executable,
            str(converter),
            "--angle", angle,
            "--output-dir", str(safe_out),
            "--format", "json",
        ]
        if dry_run:
            log(f"DRY-RUN: would run: {' '.join(cmd)}", dry_run=True)
            result["status"] = "dry_run"
            return result

        log(f"Running engagement_bait_converter: {' '.join(cmd)}")
        proc = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=60,
        )
        if proc.returncode == 0:
            result["status"] = "success"
            result["output"] = proc.stdout.strip()
            log(f"engagement_bait_converter succeeded: {result['output'][:200]}")
        else:
            result["status"] = "error"
            result["error"] = proc.stderr.strip()
            log(f"engagement_bait_converter failed (rc={proc.returncode}): {result['error']}")
    except subprocess.TimeoutExpired:
        result["status"] = "timeout"
        result["error"] = "engagement_bait_converter timed out after 60s"
        log(f"ERROR: {result['error']}")
    except Exception as e:
        result["status"] = "exception"
        result["error"] = str(e)
        log(f"ERROR running engagement_bait_converter: {e}")
    return result


def generate_content_files(output_dir: Path, dry_run: bool = False) -> dict:
    """Write all content types (tweets, threads, Reddit posts) to output directory."""
    results = {}

    # Twitter hooks JSON
    hooks_path = output_dir / "twitter_hooks.json"
    hooks_data = {
        "generated_at": datetime.utcnow().isoformat(),
        "source_angle": PH_LAUNCH_ANGLE,
        "hooks": CONTENT_TEMPLATES["twitter_hook"],
    }
    results["twitter_hooks"] = write_json(hooks_path, hooks_data, dry_run=dry_run)

    # Thread JSON
    thread_path = output_dir / "twitter_thread.json"
    thread_data = {
        "generated_at": datetime.utcnow().isoformat(),
        "source_angle": PH_LAUNCH_ANGLE,
        "thread": CONTENT_TEMPLATES["thread"],
    }
    results["twitter_thread"] = write_json(thread_path, thread_data, dry_run=dry_run)

    # Reddit posts JSON
    reddit_path = output_dir / "reddit_posts.json"
    reddit_data = {
        "generated_at": datetime.utcnow().isoformat(),
        "source_angle": PH_LAUNCH_ANGLE,
        "posts": CONTENT_TEMPLATES["reddit_post"],
    }
    results["reddit_posts"] = write_json(reddit_path, reddit_data, dry_run=dry_run)

    # CSV summary of all content pieces
    csv_rows = []
    for hook in CONTENT_TEMPLATES["twitter_hook"]:
        csv_rows.append({
            "type": "twitter_hook",
            "platform": "twitter",
            "content_preview": hook[:80],
            "generated_at": datetime.utcnow().isoformat(),
        })
    for i, tweet in enumerate(CONTENT_TEMPLATES["thread"], 1):
        csv_rows.append({
            "type": f"thread_tweet_{i}",
            "platform": "twitter",
            "content_preview": tweet[:80],
            "generated_at": datetime.utcnow().isoformat(),
        })
    for post in CONTENT_TEMPLATES["reddit_post"]:
        csv_rows.append({
            "type": "reddit_post",
            "platform": post["subreddit"],
            "content_preview": post["title"][:80],
            "generated_at": datetime.utcnow().isoformat(),
        })

    csv_path = output_dir / "content_summary.csv"
    results["csv_summary"] = write_csv(
        csv_path,
        csv_rows,
        fieldnames=["type", "platform", "content_preview", "generated_at"],
        dry_run=dry_run,
    )

    return results


def queue_app_factory_spec(dry_run: bool = False) -> bool:
    """Write the PWA spec into the App Factory queue."""
    try:
        queue_dir = safe_path(APP_FACTORY_QUEUE)
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        spec_path = queue_dir / f"mindspend_pwa_{timestamp}.json"
        return write_json(spec_path, PWA_SPEC, dry_run=dry_run)
    except Exception as e:
        log(f"ERROR queuing App Factory spec: {e}")
        return False


def check_status() -> dict:
    """Return current status of outputs and queue."""
    status = {
        "timestamp": datetime.utcnow().isoformat(),
        "content_output_dir": str(CONTENT_OUTPUT_DIR),
        "content_files": [],
        "app_factory_queue": str(APP_FACTORY_QUEUE),
        "queued_specs": [],
        "log_exists": False,
    }
    try:
        out_dir = safe_path(CONTENT_OUTPUT_DIR)
        if out_dir.exists():
            status["content_files"] = [f.name for f in out_dir.iterdir() if f.is_file()]
    except Exception as e:
        status["content_output_error"] = str(e)

    try:
        queue_dir = safe_path(APP_FACTORY_QUEUE)
        if queue_dir.exists():
            status["queued_specs"] = [
                f.name for f in queue_dir.glob("mindspend_pwa_*.json")
            ]
    except Exception as e:
        status["queue_error"] = str(e)

    try:
        log_file = safe_path(LOG_PATH)
        status["log_exists"] = log_file.exists()
        if log_file.exists():
            status["log_size_bytes"] = log_file.stat().st_size
    except Exception as e:
        status["log_error"] = str(e)

    return status


def run(dry_run: bool = False) -> int:
    log(f"Starting ph_launch_mindspend_content run (dry_run={dry_run})")

    try:
        skills = recall_skills_for_task("ph_launch_content_generation")
        log(f"Recalled {len(skills)} skills for task")
    except Exception as e:
        log(f"WARN: recall_skills_for_task failed: {e}")
        skills = []

    # Step 1: Route PH angle through engagement_bait_converter
    log("Step 1: Running engagement_bait_converter")
    converter_result = run_engagement_converter(
        angle=PH_LAUNCH_ANGLE,
        output_dir=CONTENT_OUTPUT_DIR,
        dry_run=dry_run,
    )
    log(f"Converter result: {converter_result['status']}")

    try:
        capture_skill_from_result(converter_result, "engagement_bait_converter")
    except Exception as e:
        log(f"WARN: capture_skill_from_result failed: {e}")

    # Step 2: Generate content files directly (fallback or supplement to converter)
    log("Step 2: Generating content files")
    try:
        out_dir = safe_path(CONTENT_OUTPUT_DIR)
    except Exception as e:
        log(f"ERROR resolving output dir: {e}")
        return 1

    content_results = generate_content_files(out_dir, dry_run=dry_run)
    success_count = sum(1 for v in content_results.values() if v)
    log(f"Content generation: {success_count}/{len(content_results)} files succeeded")

    # Step 3: Queue PWA spec into App Factory
    log("Step 3: Queuing emotional-finance PWA spec to App Factory")
    queued = queue_app_factory_spec(dry_run=dry_run)
    log(f"App Factory queue: {'success' if queued else 'FAILED'}")

    # Step 4: Write run manifest
    manifest = {
        "run_at": datetime.utcnow().isoformat(),
        "dry_run": dry_run,
        "source_angle": PH_LAUNCH_ANGLE,
        "converter_result": converter_result,
        "content_results": content_results,
        "app_factory_queued": queued,
        "recalled_skills": [str(s) for s in skills],
    }
    manifest_path = out_dir / "run_manifest.json"
    write_json(manifest_path, manifest, dry_run=dry_run)

    all_ok = queued and (success_count == len(content_results))
    log(f"Run complete. Overall status: {'OK' if all_ok else 'PARTIAL_FAILURE'}")
    return 0 if all_ok else 2


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "PRINTMAXX: Route Mindspend PH launch angle through engagement_bait_converter "
            "and queue PWA spec into App Factory pipeline."
        )
    )
    parser.add_argument(
        "--run",
        action="store_true",
        help="Execute the full content generation and App Factory queue pipeline.",
    )
    parser.add_argument(
        "--status",
        action="store_true",
        help="Print current status of outputs and queue without running.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        dest="dry_run",
        help="Simulate all actions without writing files or invoking subprocesses.",
    )
    args = parser.parse_args()

    if args.status:
        status = check_status()
        print(json.dumps(status, indent=2))
        sys.exit(0)

    if args.run or args.dry_run:
        exit_code = run(dry_run=args.dry_run)
        sys.exit(exit_code)

    parser.print_help()
    sys.exit(0)


if __name__ == "__main__":
    main()