#!/usr/bin/env python3
"""
PRINTMAXX Automation: ProductHunt Mac Utility Launch Monitor
TYPE: poster

Monitors ProductHunt daily for Mac utility / menu-bar / edge-UI app launches.
Extracts UI pattern and core value prop, feeds into engagement_bait_converter.py
to generate 3 tweets + 1 thread per launch (hooks: 'Mac apps nobody knows about',
'Hidden Mac features devs are building now', comparison hooks), then routes output
to the posting_queue.

Existing chain: chain_ph_launch_kickfolder_turn_your_macs_ handles the seed entry.
This automation catches FUTURE similar launches automatically.
"""

import argparse
import csv
import json
import logging
import subprocess
import sys
import urllib.request
import urllib.error
from datetime import date, datetime, timezone
from pathlib import Path

# ---------------------------------------------------------------------------
# Bootstrap PROJECT path before importing _common
# ---------------------------------------------------------------------------
PROJECT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT))

try:
    from _common import PROJECT as _PROJECT_COMMON, safe_path, recall_skills_for_task, capture_skill_from_result
    PROJECT = _PROJECT_COMMON
except ImportError:
    # Fallback definitions so the script remains runnable without _common
    def safe_path(p: Path) -> Path:
        resolved = Path(p).resolve()
        if not str(resolved).startswith(str(PROJECT.resolve())):
            raise ValueError(f"Path escape detected: {resolved} is outside {PROJECT}")
        return resolved

    def recall_skills_for_task(task: str):
        return []

    def capture_skill_from_result(skill: str, result: str):
        pass

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
AUTOMATIONS_DIR = PROJECT / "AUTOMATIONS"
LOG_PATH = AUTOMATIONS_DIR / "logs" / "ph_mac_utility_launch_monitor.log"
SEEN_PATH = AUTOMATIONS_DIR / "data" / "ph_mac_utility_seen.json"
QUEUE_PATH = AUTOMATIONS_DIR / "posting_queue" / "ph_mac_utility_posts.csv"
CONVERTER = AUTOMATIONS_DIR / "engagement_bait_converter.py"

PH_API_URL = "https://api.producthunt.com/v2/api/graphql"
PH_TOKEN_FILE = PROJECT / "secrets" / "ph_token.json"

MAC_KEYWORDS = [
    "mac", "macos", "menu bar", "menubar", "menu-bar", "status bar",
    "edge", "toolbar", "dock", "spotlight", "alfred", "raycast",
    "command center", "shortcut", "launcher", "utility", "tray",
    "notification center", "widget", "automator", "workflow",
    "top edge", "hidden", "swipe", "gesture", "quicklook",
    "quick look", "finder", "app switcher", "window manager",
]

TWEET_HOOKS = [
    "Mac apps nobody knows about",
    "Hidden Mac features devs are building now",
    "comparison",
]

# ---------------------------------------------------------------------------
# Logging setup (append mode, cron-friendly)
# ---------------------------------------------------------------------------

def setup_logging() -> logging.Logger:
    try:
        safe_path(LOG_PATH.parent).mkdir(parents=True, exist_ok=True)
    except Exception:
        LOG_PATH.parent.mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger("ph_mac_utility_monitor")
    logger.setLevel(logging.DEBUG)

    if not logger.handlers:
        fh = logging.FileHandler(str(LOG_PATH), mode="a", encoding="utf-8")
        fh.setLevel(logging.DEBUG)
        fmt = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s", datefmt="%Y-%m-%dT%H:%M:%S")
        fh.setFormatter(fmt)
        logger.addHandler(fh)

        sh = logging.StreamHandler(sys.stdout)
        sh.setLevel(logging.INFO)
        sh.setFormatter(fmt)
        logger.addHandler(sh)

    return logger


log = setup_logging()

# ---------------------------------------------------------------------------
# Token loading
# ---------------------------------------------------------------------------

def load_ph_token() -> str:
    """Load ProductHunt API bearer token from secrets file."""
    try:
        token_path = safe_path(PH_TOKEN_FILE)
        with open(token_path, "r", encoding="utf-8") as fh:
            data = json.load(fh)
        token = data.get("token") or data.get("access_token") or ""
        if not token:
            raise ValueError("No token found in ph_token.json")
        return token
    except Exception as exc:
        log.error("Failed to load PH token: %s", exc)
        raise


# ---------------------------------------------------------------------------
# ProductHunt GraphQL fetch
# ---------------------------------------------------------------------------

GRAPHQL_QUERY = """
query TodayPosts($after: String) {
  posts(order: VOTES, after: $after, first: 50, postedBefore: null) {
    pageInfo { endCursor hasNextPage }
    edges {
      node {
        id
        name
        tagline
        description
        url
        votesCount
        website
        createdAt
        topics { edges { node { name } } }
        makers { edges { node { name } } }
      }
    }
  }
}
"""


def fetch_today_posts(token: str, dry_run: bool = False) -> list:
    """Fetch today's ProductHunt posts via GraphQL. Returns list of post dicts."""
    if dry_run:
        log.info("[dry-run] Skipping PH API fetch; returning mock data.")
        return _mock_posts()

    all_posts = []
    after = None
    page = 0

    while True:
        variables = {}
        if after:
            variables["after"] = after

        payload = json.dumps({"query": GRAPHQL_QUERY, "variables": variables}).encode("utf-8")

        req = urllib.request.Request(
            PH_API_URL,
            data=payload,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}",
                "Accept": "application/json",
            },
            method="POST",
        )

        try:
            with urllib.request.urlopen(req, timeout=20) as resp:
                raw = resp.read().decode("utf-8")
                data = json.loads(raw)
        except urllib.error.HTTPError as exc:
            log.error("PH API HTTP error %s: %s", exc.code, exc.read().decode("utf-8", errors="replace"))
            break
        except urllib.error.URLError as exc:
            log.error("PH API URL error: %s", exc.reason)
            break
        except json.JSONDecodeError as exc:
            log.error("PH API JSON decode error: %s", exc)
            break

        edges = data.get("data", {}).get("posts", {}).get("edges", [])
        page_info = data.get("data", {}).get("posts", {}).get("pageInfo", {})

        for edge in edges:
            node = edge.get("node", {})
            topics = [t["node"]["name"] for t in node.get("topics", {}).get("edges", [])]
            makers = [m["node"]["name"] for m in node.get("makers", {}).get("edges", [])]
            all_posts.append({
                "id": node.get("id"),
                "name": node.get("name", ""),
                "tagline": node.get("tagline", ""),
                "description": node.get("description", ""),
                "url": node.get("url", ""),
                "website": node.get("website", ""),
                "votesCount": node.get("votesCount", 0),
                "createdAt": node.get("createdAt", ""),
                "topics": topics,
                "makers": makers,
            })

        page += 1
        if not page_info.get("hasNextPage") or page >= 5:
            break
        after = page_info.get("endCursor")

    log.info("Fetched %d total posts from PH.", len(all_posts))
    return all_posts


def _mock_posts() -> list:
    """Return minimal mock data for --dry-run testing."""
    return [
        {
            "id": "mock-001",
            "name": "EdgeBar Pro",
            "tagline": "Turn your Mac's top edge into a hidden command center",
            "description": "A menu-bar utility that exposes a hidden panel along the top edge of your Mac screen.",
            "url": "https://www.producthunt.com/posts/edgebar-pro",
            "website": "https://edgebarpro.example.com",
            "votesCount": 312,
            "createdAt": datetime.now(timezone.utc).isoformat(),
            "topics": ["Mac", "Productivity", "Developer Tools"],
            "makers": ["Jane Dev"],
        },
        {
            "id": "mock-002",
            "name": "SwiftLaunch",
            "tagline": "Instant launcher hidden in your Mac menu bar",
            "description": "One-key launcher that lives invisibly in your status bar.",
            "url": "https://www.producthunt.com/posts/swiftlaunch",
            "website": "https://swiftlaunch.example.com",
            "votesCount": 198,
            "createdAt": datetime.now(timezone.utc).isoformat(),
            "topics": ["Mac", "Utilities"],
            "makers": ["Alex Maker"],
        },
    ]


# ---------------------------------------------------------------------------
# Filtering
# ---------------------------------------------------------------------------

def is_mac_utility(post: dict) -> bool:
    """Return True if post looks like a Mac utility / menu-bar / edge-UI app."""
    text = " ".join([
        post.get("name", ""),
        post.get("tagline", ""),
        post.get("description", ""),
        " ".join(post.get("topics", [])),
    ]).lower()

    for kw in MAC_KEYWORDS:
        if kw in text:
            return True
    return False


# ---------------------------------------------------------------------------
# Seen-list (deduplication)
# ---------------------------------------------------------------------------

def load_seen() -> set:
    try:
        seen_path = safe_path(SEEN_PATH)
        if seen_path.exists():
            with open(seen_path, "r", encoding="utf-8") as fh:
                data = json.load(fh)
            return set(data.get("seen", []))
    except Exception as exc:
        log.warning("Could not load seen list: %s", exc)
    return set()


def save_seen(seen: set, dry_run: bool = False) -> None:
    if dry_run:
        log.info("[dry-run] Would save seen list (%d entries).", len(seen))
        return
    try:
        seen_path = safe_path(SEEN_PATH)
        seen_path.parent.mkdir(parents=True, exist_ok=True)
        with open(seen_path, "w", encoding="utf-8") as fh:
            json.dump({"seen": sorted(seen), "updated": datetime.now(timezone.utc).isoformat()}, fh, indent=2)
        log.debug("Saved seen list to %s", seen_path)
    except Exception as exc:
        log.error("Failed to save seen list: %s", exc)


# ---------------------------------------------------------------------------
# UI pattern + value prop extractor
# ---------------------------------------------------------------------------

UI_PATTERNS = {
    "menu bar": "Menu-bar hidden panel",
    "menubar": "Menu-bar hidden panel",
    "menu-bar": "Menu-bar hidden panel",
    "status bar": "Status-bar widget",
    "top edge": "Top-edge hidden drawer",
    "edge": "Edge-anchored overlay",
    "dock": "Dock-integrated launcher",
    "toolbar": "Toolbar quick-action strip",
    "launcher": "Keyboard-driven launcher",
    "widget": "Notification-center widget",
    "spotlight": "Spotlight-style command palette",
    "gesture": "Gesture-activated panel",
    "swipe": "Swipe-triggered overlay",
    "window manager": "Window-management overlay",
    "workflow": "Automation workflow UI",
}

VALUE_KEYWORDS = {
    "hidden": "reveals invisible functionality",
    "instant": "zero-friction access",
    "keyboard": "keyboard-first workflow",
    "shortcut": "shortcut-driven UX",
    "command center": "centralises Mac controls",
    "productivity": "productivity multiplier",
    "launcher": "app/command launcher",
    "automat": "workflow automation",
    "quick": "speed-optimised access",
    "seamless": "frictionless integration",
}


def extract_ui_pattern(post: dict) -> str:
    text = " ".join([post.get("name", ""), post.get("tagline", ""), post.get("description", "")]).lower()
    for kw, pattern in UI_PATTERNS.items():
        if kw in text:
            return pattern
    return "Mac utility panel"


def extract_value_prop(post: dict) -> str:
    text = " ".join([post.get("tagline", ""), post.get("description", "")]).lower()
    found = []
    for kw, prop in VALUE_KEYWORDS.items():
        if kw in text:
            found.append(prop)
    if found:
        return "; ".join(found[:2])
    tagline = post.get("tagline", "").strip()
    return tagline[:120] if tagline else "streamlines Mac workflow"


# ---------------------------------------------------------------------------
# engagement_bait_converter.py invocation
# ---------------------------------------------------------------------------

def run_converter(post: dict, ui_pattern: str, value_prop: str, dry_run: bool = False) -> dict:
    """
    Call engagement_bait_converter.py as subprocess, passing launch context.
    Returns dict with tweet_1, tweet_2, tweet_3, thread keys.
    Falls back to inline generation if converter not found.
    """
    name = post.get("name", "Unknown App")
    tagline = post.get("tagline", "")
    ph_url = post.get("url", "")

    if CONVERTER.exists() and not dry_run:
        payload = json.dumps({
            "source": "producthunt",
            "app_name": name,
            "tagline": tagline,
            "ui_pattern": ui_pattern,
            "value_prop": value_prop,
            "ph_url": ph_url,
            "hooks": TWEET_HOOKS,
        })
        try:
            result = subprocess.run(
                [sys.executable, str(CONVERTER), "--json-input", payload],
                capture_output=True,
                text=True,
                timeout=60,
            )
            if result.returncode == 0 and result.stdout.strip():
                try:
                    return json.loads(result.stdout.strip())
                except json.JSONDecodeError:
                    log.warning("Converter returned non-JSON; falling back to inline generation.")
            else:
                log.warning("Converter exited %d: %s", result.returncode, result.stderr[:200])
        except subprocess.TimeoutExpired:
            log.error("Converter timed out for post %s", name)
        except Exception as exc:
            log.error("Converter subprocess error: %s", exc)
    else:
        if dry_run:
            log.info("[dry-run] Would invoke engagement_bait_converter.py for '%s'.", name)
        elif not CONVERTER.exists():
            log.warning("engagement_bait_converter.py not found at %s; using inline fallback.", CONVERTER)

    # Inline fallback generation
    return _generate_tweets_inline(name, tagline, ui_pattern, value_prop, ph_url)


def _generate_tweets_inline(name: str, tagline: str, ui_pattern: str, value_prop: str, ph_url: str) -> dict:
    """Generate engagement tweets without external converter."""
    tweet_1 = (
        f"Mac apps nobody knows about:\n\n"
        f"{name} — {tagline}\n\n"
        f"UI pattern: {ui_pattern}\n"
        f"Why it matters: {value_prop}\n\n"
        f"{ph_url}"
    )[:280]

    tweet_2 = (
        f"Hidden Mac features devs are building right now:\n\n"
        f"{name} turns your Mac into something new.\n"
        f"→ {ui_pattern}\n"
        f"→ {value_prop}\n\n"
        f"Built by indie devs. Shipping on Product Hunt.\n{ph_url}"
    )[:280]

    tweet_3 = (
        f"Alfred vs Raycast vs {name}?\n\n"
        f"{name} does something neither does:\n"
        f"{ui_pattern} — {value_prop}\n\n"
        f"Worth knowing: {ph_url}"
    )[:280]

    thread = (
        f"🧵 {name}: {tagline}\n\n"
        f"1/ Most Mac users don't know this category of tool exists.\n\n"
        f"2/ UI Pattern: {ui_pattern}\n"
        f"   That means: {value_prop}\n\n"
        f"3/ Why devs keep building in this space:\n"
        f"   - macOS exposes just enough API surface\n"
        f"   - Power users actively seek hidden-UI tools\n"
        f"   - Menu-bar real estate is underutilised\n\n"
        f"4/ {name} on Product Hunt → {ph_url}\n\n"
        f"Follow for more Mac utility launches as they happen."
    )

    return {
        "tweet_1": tweet_1,
        "tweet_2": tweet_2,
        "tweet_3": tweet_3,
        "thread": thread,
    }


# ---------------------------------------------------------------------------
# posting_queue writer
# ---------------------------------------------------------------------------

QUEUE_FIELDS = [
    "queued_at", "source", "post_id", "app_name", "ph_url",
    "ui_pattern", "value_prop", "hook_type", "content", "status",
]


def append_to_queue(post: dict, tweets: dict, ui_pattern: str, value_prop: str, dry_run: bool = False) -> None:
    """Write generated content rows to the posting_queue CSV."""
    if dry_run:
        log.info("[dry-run] Would append %d rows to posting queue for '%s'.", 4, post.get("name"))
        for key, content in tweets.items():
            log.debug("  [%s] %s", key, content[:80])
        return

    try:
        queue_path = safe_path(QUEUE_PATH)
        queue_path.parent.mkdir(parents=True, exist_ok=True)
        write_header = not queue_path.exists()

        with open(queue_path, "a", newline="", encoding="utf-8") as fh:
            writer = csv.DictWriter(fh, fieldnames=QUEUE_FIELDS)
            if write_header:
                writer.writeheader()

            now = datetime.now(timezone.utc).isoformat()
            hook_map = {
                "tweet_1": TWEET_HOOKS[0],
                "tweet_2": TWEET_HOOKS[1],
                "tweet_3": TWEET_HOOKS[2],
                "thread": "thread",
            }

            for key, content in tweets.items():
                writer.writerow({
                    "queued_at": now,
                    "source": "producthunt",
                    "post_id": post.get("id", ""),
                    "app_name": post.get("name", ""),
                    "ph_url": post.get("url", ""),
                    "ui_pattern": ui_pattern,
                    "value_prop": value_prop,
                    "hook_type": hook_map.get(key, key),
                    "content": content,
                    "status": "pending",
                })

        log.info("Queued 4 posts for '%s'.", post.get("name"))
    except Exception as exc:
        log.error("Failed to write to posting queue: %s", exc)


# ---------------------------------------------------------------------------
# Core run logic
# ---------------------------------------------------------------------------

def run(dry_run: bool = False) -> int:
    """Main execution: fetch, filter, deduplicate, generate, queue. Returns exit code."""
    log.info("=== ph_mac_utility_launch_monitor START (dry_run=%s) ===", dry_run)

    try:
        recall_skills_for_task("producthunt mac utility monitor")
    except Exception:
        pass

    # Load token
    try:
        if not dry_run:
            token = load_ph_token()
        else:
            token = "dry-run-token"
    except Exception as exc:
        log.error("Aborting: cannot load PH token: %s", exc)
        return 1

    # Fetch posts
    try:
        posts = fetch_today_posts(token, dry_run=dry_run)
    except Exception as exc:
        log.error("Aborting: fetch failed: %s", exc)
        return 1

    # Filter to Mac utilities
    mac_posts = [p for p in posts if is_mac_utility(p)]
    log.info("Mac utility posts found: %d / %d total.", len(mac_posts), len(posts))

    # Deduplicate against seen list
    seen = load_seen()
    new_posts = [p for p in mac_posts if p.get("id") not in seen]
    log.info("New (unseen) Mac utility posts: %d", len(new_posts))

    if not new_posts:
        log.info("No new Mac utility launches today. Nothing to queue.")
        return 0

    processed = 0
    for post in new_posts:
        post_id = post.get("id", "")
        name = post.get("name", "")
        log.info("Processing: %s (id=%s, votes=%s)", name, post_id, post.get("votesCount"))

        try:
            ui_pattern = extract_ui_pattern(post)
            value_prop = extract_value_prop(post)
            log.debug("  UI pattern : %s", ui_pattern)
            log.debug("  Value prop : %s", value_prop)

            tweets = run_converter(post, ui_pattern, value_prop, dry_run=dry_run)
            append_to_queue(post, tweets, ui_pattern, value_prop, dry_run=dry_run)

            try:
                capture_skill_from_result("ph_mac_launch", f"{name}: {ui_pattern} / {value_prop}")
            except Exception:
                pass

            seen.add(post_id)
            processed += 1

        except Exception as exc:
            log.error("Failed to process post %s (%s): %s", post_id, name, exc)
            continue

    save_seen(seen, dry_run=dry_run)
    log.info("Done. Processed %d new Mac utility launch(es).", processed)
    log.info("=== ph_mac_utility_launch_monitor END ===")
    return 0


# ---------------------------------------------------------------------------
# Status reporting
# ---------------------------------------------------------------------------

def status() -> int:
    """Print current queue and seen-list stats."""
    try:
        seen = load_seen()
        print(f"Seen post IDs    : {len(seen)}")
    except Exception as exc:
        print(f"Seen list error  : {exc}")

    try:
        queue_path = safe_path(QUEUE_PATH)
        if queue_path.exists():
            with open(queue_path, "r", encoding="utf-8") as fh:
                rows = list(csv.DictReader(fh))
            pending = sum(1 for r in rows if r.get("status") == "pending")
            print(f"Queue total rows : {len(rows)}")
            print(f"Queue pending    : {pending}")
        else:
            print("Queue file       : not found")
    except Exception as exc:
        print(f"Queue error      : {exc}")

    try:
        log_path = safe_path(LOG_PATH)
        if log_path.exists():
            size = log_path.stat().st_size
            print(f"Log file         : {log_path} ({size:,} bytes)")
        else:
            print("Log file         : not yet created")
    except Exception as exc:
        print(f"Log error        : {exc}")

    return 0


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="PRINTMAXX: ProductHunt Mac utility launch monitor and tweet generator.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--run",
        action="store_true",
        help="Fetch today's PH posts, filter Mac utilities, generate and queue tweets.",
    )
    group.add_argument(
        "--status",
        action="store_true",
        help="Print queue and seen-list statistics.",
    )
    group.add_argument(
        "--dry-run",
        action="store_true",
        dest="dry_run",
        help="Simulate a full run with mock data; no files written, no API calls.",
    )
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    try:
        if args.status:
            sys.exit(status())
        elif args.dry_run:
            sys.exit(run(dry_run=True))
        else:
            sys.exit(run(dry_run=False))
    except KeyboardInterrupt:
        log.info("Interrupted by user.")
        sys.exit(130)
    except Exception as exc:
        log.critical("Unhandled exception: %s", exc, exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()