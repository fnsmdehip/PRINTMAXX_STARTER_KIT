#!/usr/bin/env python3
"""
PRINTMAXX Automation: ProductHunt Email Productivity Monitor

Monitors ProductHunt for email productivity tool launches as trend signals.
Extracts hook structures (cleaner inbox, focused writing, less noise) and
auto-generates engagement content routed to engagement_bait_converter.py
with the email-productivity niche tag.

TYPE: poster
METHOD CONTEXT: [PH LAUNCH] Joy for Gmail: A Gmail with clearer inbox, focused writing, less noise
"""

import argparse
import csv
import json
import logging
import subprocess
import sys
import urllib.request
import urllib.error
import urllib.parse
from datetime import datetime, timezone
from pathlib import Path

try:
    from _common import PROJECT, safe_path, recall_skills_for_task, capture_skill_from_result
except ImportError:
    PROJECT = Path(__file__).resolve().parent.parent

    def safe_path(path: Path) -> Path:
        resolved = Path(path).resolve()
        if not str(resolved).startswith(str(PROJECT.resolve())):
            raise ValueError(f"Path escape attempt blocked: {resolved}")
        return resolved

    def recall_skills_for_task(task_description: str) -> list:
        return []

    def capture_skill_from_result(result: dict, skill_name: str) -> None:
        pass


LOG_FILE = PROJECT / "AUTOMATIONS" / "logs" / "ph_email_productivity_monitor.log"
OUTPUT_DIR = PROJECT / "AUTOMATIONS" / "output" / "ph_email_productivity"
QUEUE_FILE = PROJECT / "AUTOMATIONS" / "queues" / "engagement_bait_queue.json"
CONVERTER_SCRIPT = PROJECT / "AUTOMATIONS" / "engagement_bait_converter.py"
STATUS_FILE = PROJECT / "AUTOMATIONS" / "status" / "ph_email_productivity_monitor.json"

NICHE_TAG = "email-productivity"

PH_GRAPHQL_URL = "https://api.producthunt.com/v2/api/graphql"

EMAIL_PRODUCTIVITY_KEYWORDS = [
    "gmail", "inbox", "email", "inbox zero", "email productivity",
    "email management", "email client", "mail", "unsubscribe",
    "email cleaner", "focused writing", "less noise", "cleaner inbox",
    "email triage", "email workflow", "email automation",
]

HOOK_TEMPLATES = {
    "cleaner_inbox": [
        "Your inbox is a warzone. Here's the framework that finally brought order.",
        "Inbox zero isn't a myth. It's a system. Here's the one that actually works.",
        "I cleaned 10,000 emails in 48 hours. Here's the exact process:",
        "The 'cleaner inbox' promise is real — but only if you do these 5 things first.",
    ],
    "focused_writing": [
        "Email is killing your deep work. Here's how top performers write fewer, better emails.",
        "Stop writing emails like you're texting. This framework changed everything.",
        "The best email writers I know all do this one counterintuitive thing.",
        "Writing emails that actually get responses: a thread on what I learned the hard way.",
    ],
    "less_noise": [
        "You're not overwhelmed by work. You're overwhelmed by email noise. Here's the fix.",
        "Every email newsletter, promo, and CC is stealing your focus. Here's the kill switch.",
        "Signal vs noise in your inbox: how to find what matters in under 5 minutes/day.",
        "The tools silently destroying your email productivity (and how to fight back):",
    ],
    "tools_killing_productivity": [
        "The email tools you think are helping you are actually making things worse. A thread:",
        "I tested 12 Gmail productivity tools. Here's what most people get wrong:",
        "Hot take: most email productivity apps solve the wrong problem. Here's what to look for instead.",
        "New [PH LAUNCH] just dropped in the Gmail space. Here's what it signals about where email is going:",
    ],
    "inbox_zero_framework": [
        "Inbox Zero in 2025: the framework nobody talks about (but everyone needs).",
        "The inbox zero system I've used for 3 years — and why it still works:",
        "A 5-step inbox zero framework that survives contact with real life:",
        "Inbox zero is not about empty inbox. It's about decision speed. Here's the method:",
    ],
}

CONTENT_TYPES = [
    "gmail_productivity_thread",
    "inbox_zero_framework",
    "tools_killing_email_productivity",
]


def setup_logging(dry_run: bool = False) -> logging.Logger:
    logger = logging.getLogger("ph_email_productivity_monitor")
    logger.setLevel(logging.DEBUG)

    if not logger.handlers:
        try:
            log_path = safe_path(LOG_FILE)
            log_path.parent.mkdir(parents=True, exist_ok=True)
            fh = logging.FileHandler(str(log_path), mode="a", encoding="utf-8")
            fh.setLevel(logging.DEBUG)
            formatter = logging.Formatter(
                "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
                datefmt="%Y-%m-%dT%H:%M:%S"
            )
            fh.setFormatter(formatter)
            logger.addHandler(fh)
        except Exception as e:
            print(f"[WARN] Could not set up file logging: {e}", file=sys.stderr)

        ch = logging.StreamHandler(sys.stdout)
        ch.setLevel(logging.INFO)
        ch.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s", datefmt="%H:%M:%S"))
        logger.addHandler(ch)

    if dry_run:
        logger.info("[DRY-RUN] No files will be written, no scripts will be called.")

    return logger


def fetch_ph_launches(logger: logging.Logger, limit: int = 20) -> list:
    """
    Fetch recent ProductHunt launches via public GraphQL API (no auth for top posts).
    Falls back to a curated seed payload when the API is unavailable.
    """
    query = """
    {
      posts(order: NEWEST, first: %d) {
        edges {
          node {
            id
            name
            tagline
            description
            url
            votesCount
            createdAt
            topics {
              edges {
                node {
                  name
                  slug
                }
              }
            }
          }
        }
      }
    }
    """ % limit

    payload = json.dumps({"query": query}).encode("utf-8")
    req = urllib.request.Request(
        PH_GRAPHQL_URL,
        data=payload,
        headers={
            "Content-Type": "application/json",
            "User-Agent": "PRINTMAXX-PHMonitor/1.0",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            raw = resp.read().decode("utf-8")
            data = json.loads(raw)
            edges = data.get("data", {}).get("posts", {}).get("edges", [])
            launches = [e["node"] for e in edges if "node" in e]
            logger.info(f"Fetched {len(launches)} launches from ProductHunt API.")
            return launches
    except urllib.error.HTTPError as e:
        logger.warning(f"PH API HTTP error {e.code}: {e.reason}. Using seed data.")
    except urllib.error.URLError as e:
        logger.warning(f"PH API URL error: {e.reason}. Using seed data.")
    except json.JSONDecodeError as e:
        logger.warning(f"PH API JSON parse error: {e}. Using seed data.")
    except Exception as e:
        logger.warning(f"PH API unexpected error: {e}. Using seed data.")

    return _seed_launches()


def _seed_launches() -> list:
    """Curated seed data based on the known method context signal."""
    return [
        {
            "id": "seed-joy-gmail",
            "name": "Joy for Gmail",
            "tagline": "A Gmail with clearer inbox, focused writing, less noise",
            "description": (
                "Joy transforms your Gmail experience with intelligent inbox organization, "
                "distraction-free writing mode, and noise reduction filters so you can "
                "focus on what actually matters."
            ),
            "url": "https://www.producthunt.com/posts/joy-for-gmail",
            "votesCount": 0,
            "createdAt": datetime.now(timezone.utc).isoformat(),
            "topics": {
                "edges": [
                    {"node": {"name": "Productivity", "slug": "productivity"}},
                    {"node": {"name": "Gmail", "slug": "gmail"}},
                    {"node": {"name": "Email", "slug": "email"}},
                ]
            },
        }
    ]


def is_email_productivity_launch(launch: dict) -> bool:
    """Return True if a launch matches email productivity signal keywords."""
    text = " ".join([
        launch.get("name", ""),
        launch.get("tagline", ""),
        launch.get("description", "") or "",
    ]).lower()

    topics = [
        e["node"]["slug"]
        for e in launch.get("topics", {}).get("edges", [])
        if "node" in e
    ]
    topic_text = " ".join(topics).lower()
    combined = text + " " + topic_text

    return any(kw in combined for kw in EMAIL_PRODUCTIVITY_KEYWORDS)


def extract_hooks(launch: dict) -> dict:
    """
    Extract hook signal categories from a launch's tagline/description.
    Returns a dict mapping hook_category -> True/False.
    """
    text = " ".join([
        launch.get("name", ""),
        launch.get("tagline", ""),
        launch.get("description", "") or "",
    ]).lower()

    hooks_detected = {
        "cleaner_inbox": any(kw in text for kw in ["cleaner inbox", "clean inbox", "inbox organization", "inbox management", "inbox zero", "unclutter"]),
        "focused_writing": any(kw in text for kw in ["focused writing", "distraction-free", "focus mode", "writing mode", "compose", "draft"]),
        "less_noise": any(kw in text for kw in ["less noise", "noise reduction", "signal", "filter", "unsubscribe", "quiet", "silence", "calm"]),
        "tools_killing_productivity": any(kw in text for kw in ["productivity", "workflow", "efficient", "effective", "performance"]),
        "inbox_zero_framework": any(kw in text for kw in ["inbox zero", "empty inbox", "triage", "archive", "process email"]),
    }

    if not any(hooks_detected.values()):
        hooks_detected["tools_killing_productivity"] = True

    return hooks_detected


def generate_content_batch(launch: dict, hooks: dict) -> list:
    """
    Generate engagement content items based on detected hooks.
    Returns a list of content dicts ready for engagement_bait_converter.
    """
    import random

    launch_name = launch.get("name", "Unknown Tool")
    launch_tagline = launch.get("tagline", "")
    launch_url = launch.get("url", "")
    timestamp = datetime.now(timezone.utc).isoformat()

    content_items = []

    for hook_category, detected in hooks.items():
        if not detected:
            continue

        templates = HOOK_TEMPLATES.get(hook_category, [])
        if not templates:
            continue

        hook_text = random.choice(templates)
        hook_text = hook_text.replace("[PH LAUNCH]", f"[PH LAUNCH] {launch_name}")

        content_type = _hook_to_content_type(hook_category)

        item = {
            "source": "producthunt",
            "source_launch_id": launch.get("id", ""),
            "source_launch_name": launch_name,
            "source_launch_tagline": launch_tagline,
            "source_launch_url": launch_url,
            "hook_category": hook_category,
            "hook_text": hook_text,
            "content_type": content_type,
            "niche_tag": NICHE_TAG,
            "generated_at": timestamp,
            "votes": launch.get("votesCount", 0),
            "status": "pending",
        }

        content_items.append(item)

    return content_items


def _hook_to_content_type(hook_category: str) -> str:
    mapping = {
        "cleaner_inbox": "inbox_zero_framework",
        "focused_writing": "gmail_productivity_thread",
        "less_noise": "tools_killing_email_productivity",
        "tools_killing_productivity": "tools_killing_email_productivity",
        "inbox_zero_framework": "inbox_zero_framework",
    }
    return mapping.get(hook_category, "gmail_productivity_thread")


def write_content_to_csv(content_items: list, logger: logging.Logger, dry_run: bool = False) -> Path:
    """Write generated content items to a timestamped CSV file."""
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    filename = f"ph_email_productivity_{timestamp}.csv"

    try:
        out_dir = safe_path(OUTPUT_DIR)
        out_dir.mkdir(parents=True, exist_ok=True)
        out_file = safe_path(out_dir / filename)
    except ValueError as e:
        logger.error(f"Path validation failed: {e}")
        raise

    if dry_run:
        logger.info(f"[DRY-RUN] Would write {len(content_items)} items to {out_file}")
        return out_file

    try:
        fieldnames = [
            "source", "source_launch_id", "source_launch_name", "source_launch_tagline",
            "source_launch_url", "hook_category", "hook_text", "content_type",
            "niche_tag", "generated_at", "votes", "status",
        ]
        with open(str(out_file), "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(content_items)
        logger.info(f"Wrote {len(content_items)} content items to {out_file}")
    except OSError as e:
        logger.error(f"Failed to write CSV: {e}")
        raise

    return out_file


def enqueue_for_converter(content_items: list, logger: logging.Logger, dry_run: bool = False) -> None:
    """Append content items to the shared engagement bait queue JSON file."""
    try:
        queue_path = safe_path(QUEUE_FILE)
        queue_path.parent.mkdir(parents=True, exist_ok=True)
    except ValueError as e:
        logger.error(f"Queue path validation failed: {e}")
        return

    if dry_run:
        logger.info(f"[DRY-RUN] Would enqueue {len(content_items)} items to {queue_path}")
        return

    existing = []
    if queue_path.exists():
        try:
            with open(str(queue_path), "r", encoding="utf-8") as f:
                existing = json.load(f)
            if not isinstance(existing, list):
                existing = []
        except (json.JSONDecodeError, OSError):
            existing = []

    existing.extend(content_items)

    try:
        with open(str(queue_path), "w", encoding="utf-8") as f:
            json.dump(existing, f, indent=2, ensure_ascii=False)
        logger.info(f"Enqueued {len(content_items)} items. Queue total: {len(existing)}")
    except OSError as e:
        logger.error(f"Failed to write queue file: {e}")


def invoke_converter(csv_path: Path, logger: logging.Logger, dry_run: bool = False) -> None:
    """Call engagement_bait_converter.py with the generated CSV and niche tag."""
    try:
        converter_path = safe_path(CONVERTER_SCRIPT)
    except ValueError as e:
        logger.error(f"Converter script path validation failed: {e}")
        return

    if not converter_path.exists():
        logger.warning(f"Converter script not found at {converter_path}. Skipping invocation.")
        return

    cmd = [
        sys.executable,
        str(converter_path),
        "--input", str(csv_path),
        "--niche", NICHE_TAG,
        "--run",
    ]

    if dry_run:
        logger.info(f"[DRY-RUN] Would invoke: {' '.join(cmd)}")
        return

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=120,
        )
        if result.returncode == 0:
            logger.info(f"Converter exited cleanly. stdout: {result.stdout.strip()[:200]}")
        else:
            logger.error(
                f"Converter exited {result.returncode}. "
                f"stderr: {result.stderr.strip()[:400]}"
            )
    except subprocess.TimeoutExpired:
        logger.error("Converter timed out after 120 seconds.")
    except OSError as e:
        logger.error(f"Failed to invoke converter: {e}")


def write_status(status_data: dict, logger: logging.Logger, dry_run: bool = False) -> None:
    """Persist run status to the status JSON file."""
    try:
        status_path = safe_path(STATUS_FILE)
        status_path.parent.mkdir(parents=True, exist_ok=True)
    except ValueError as e:
        logger.error(f"Status path validation failed: {e}")
        return

    if dry_run:
        logger.info(f"[DRY-RUN] Would write status to {status_path}")
        return

    try:
        with open(str(status_path), "w", encoding="utf-8") as f:
            json.dump(status_data, f, indent=2, ensure_ascii=False)
    except OSError as e:
        logger.error(f"Failed to write status file: {e}")


def read_status(logger: logging.Logger) -> dict:
    """Read the last run status from the status JSON file."""
    try:
        status_path = safe_path(STATUS_FILE)
    except ValueError as e:
        logger.error(f"Status path validation failed: {e}")
        return {}

    if not status_path.exists():
        return {"message": "No previous run found.", "status_file": str(status_path)}

    try:
        with open(str(status_path), "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError) as e:
        logger.error(f"Could not read status file: {e}")
        return {"error": str(e)}


def run_monitor(dry_run: bool = False) -> None:
    logger = setup_logging(dry_run=dry_run)
    logger.info("=== PH Email Productivity Monitor START ===")

    skills = recall_skills_for_task("monitor producthunt email productivity launches")
    if skills:
        logger.debug(f"Recalled {len(skills)} skill(s) for task.")

    run_start = datetime.now(timezone.utc).isoformat()
    matched_launches = []
    total_content_items = []

    try:
        launches = fetch_ph_launches(logger=logger, limit=30)
    except Exception as e:
        logger.error(f"Failed to fetch launches: {e}")
        launches = []

    for launch in launches:
        try:
            if not is_email_productivity_launch(launch):
                continue

            logger.info(
                f"Matched launch: {launch.get('name', '?')} — "
                f"{launch.get('tagline', '')[:80]}"
            )
            matched_launches.append(launch.get("name", "unknown"))

            hooks = extract_hooks(launch)
            active_hooks = [k for k, v in hooks.items() if v]
            logger.info(f"  Hooks detected: {active_hooks}")

            content_items = generate_content_batch(launch, hooks)
            logger.info(f"  Generated {len(content_items)} content items.")
            total_content_items.extend(content_items)

        except Exception as e:
            logger.error(f"Error processing launch '{launch.get('name', '?')}': {e}")
            continue

    csv_path = None
    if total_content_items:
        try:
            csv_path = write_content_to_csv(total_content_items, logger=logger, dry_run=dry_run)
            enqueue_for_converter(total_content_items, logger=logger, dry_run=dry_run)
            invoke_converter(csv_path, logger=logger, dry_run=dry_run)
        except Exception as e:
            logger.error(f"Output/routing step failed: {e}")
    else:
        logger.info("No email productivity launches matched. Nothing to write.")

    status_data = {
        "last_run": run_start,
        "completed_at": datetime.now(timezone.utc).isoformat(),
        "dry_run": dry_run,
        "launches_fetched": len(launches),
        "launches_matched": len(matched_launches),
        "matched_names": matched_launches,
        "content_items_generated": len(total_content_items),
        "output_csv": str(csv_path) if csv_path else None,
        "niche_tag": NICHE_TAG,
        "status": "ok",
    }

    write_status(status_data, logger=logger, dry_run=dry_run)

    result = {
        "task": "ph_email_productivity_monitor",
        "items_generated": len(total_content_items),
        "niche_tag": NICHE_TAG,
    }
    capture_skill_from_result(result, "ph_email_productivity_monitor")

    logger.info(
        f"=== DONE: {len(matched_launches)} matched, "
        f"{len(total_content_items)} items generated ==="
    )


def print_status() -> None:
    logger = setup_logging()
    status = read_status(logger)
    print(json.dumps(status, indent=2))


def main() -> None:
    parser = argparse.ArgumentParser(
        description="PRINTMAXX: ProductHunt Email Productivity Monitor",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Examples:\n"
            "  python ph_email_productivity_monitor.py --run\n"
            "  python ph_email_productivity_monitor.py --dry-run\n"
            "  python ph_email_productivity_monitor.py --status\n"
        ),
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--run", action="store_true", help="Run the monitor pipeline.")
    group.add_argument("--dry-run", action="store_true", help="Simulate run without writing files.")
    group.add_argument("--status", action="store_true", help="Print last run status and exit.")

    args = parser.parse_args()

    if args.status:
        print_status()
        sys.exit(0)

    if args.run or args.dry_run:
        run_monitor(dry_run=args.dry_run)
        sys.exit(0)


if __name__ == "__main__":
    main()