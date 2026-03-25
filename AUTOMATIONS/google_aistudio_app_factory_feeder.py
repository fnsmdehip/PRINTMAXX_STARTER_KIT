#!/usr/bin/env python3
"""
PRINTMAXX Automation: Google AI Studio App Factory Feeder

Monitors Google AI Studio 2.0 feature releases and Antigravity/Firebase
changelogs; auto-generates app scaffolds using the vibe-coding stack;
pipes new feature announcements into the App Factory priority queue as
build-ready opportunities.

[PH LAUNCH] Google AI Studio 2.0: Full-stack vibe coding powered by
Antigravity + Firebase
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

# ---------------------------------------------------------------------------
# Bootstrap: resolve PROJECT before _common import so safe_path is available
# ---------------------------------------------------------------------------
_SCRIPT_PROJECT = Path(__file__).resolve().parent.parent

try:
    sys.path.insert(0, str(_SCRIPT_PROJECT / "AUTOMATIONS"))
    from _common import PROJECT, safe_path, recall_skills_for_task, capture_skill_from_result
except ImportError:
    # Fallback stubs so the script remains runnable without _common installed
    PROJECT = _SCRIPT_PROJECT

    def safe_path(path: Path) -> Path:
        """Validate that *path* resolves inside PROJECT."""
        resolved = Path(path).resolve()
        try:
            resolved.relative_to(PROJECT.resolve())
        except ValueError as exc:
            raise ValueError(
                f"Path escape attempt blocked: {resolved} is outside {PROJECT}"
            ) from exc
        return resolved

    def recall_skills_for_task(task: str) -> list:
        return []

    def capture_skill_from_result(result: dict, task: str) -> None:
        pass


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
AUTOMATIONS_DIR  = PROJECT / "AUTOMATIONS"
LOG_PATH         = AUTOMATIONS_DIR / "logs" / "google_aistudio_app_factory_feeder.log"
QUEUE_PATH       = AUTOMATIONS_DIR / "data" / "app_factory_queue.json"
SEEN_PATH        = AUTOMATIONS_DIR / "data" / "aistudio_seen_entries.csv"
SCAFFOLDS_DIR    = AUTOMATIONS_DIR / "scaffolds" / "aistudio"

FEED_SOURCES = {
    "google_aistudio_blog": "https://developers.googleblog.com/feeds/posts/default?alt=json",
    "firebase_release_notes": "https://firebase.google.com/support/release-notes/js.json",
}

VIBE_STACK_TEMPLATE = {
    "runtime":    "nodejs20",
    "ai_backend": "google-ai-studio-2.0",
    "infra":      ["firebase-app-hosting", "cloud-run", "antigravity"],
    "db":         "firestore",
    "auth":       "firebase-auth",
    "storage":    "firebase-storage",
    "deploy":     "firebase-deploy",
}

PRIORITY_KEYWORDS = [
    "gemini", "ai studio", "antigravity", "firebase", "vibe coding",
    "app hosting", "cloud run", "full-stack", "scaffold", "2.0",
    "gemini 2", "function calling", "grounding", "code execution",
]

# ---------------------------------------------------------------------------
# Logging setup
# ---------------------------------------------------------------------------

def setup_logging() -> logging.Logger:
    log_file = safe_path(LOG_PATH)
    log_file.parent.mkdir(parents=True, exist_ok=True)
    logger = logging.getLogger("aistudio_app_factory_feeder")
    logger.setLevel(logging.DEBUG)
    if not logger.handlers:
        fh = logging.FileHandler(str(log_file), mode="a", encoding="utf-8")
        fh.setFormatter(logging.Formatter(
            "%(asctime)s  %(levelname)-8s  %(message)s",
            datefmt="%Y-%m-%dT%H:%M:%SZ",
        ))
        logger.addHandler(fh)
        sh = logging.StreamHandler(sys.stdout)
        sh.setFormatter(logging.Formatter("%(levelname)-8s %(message)s"))
        logger.addHandler(sh)
    return logger


log = setup_logging()

# ---------------------------------------------------------------------------
# Persistence helpers
# ---------------------------------------------------------------------------

def _load_seen_ids() -> set:
    path = safe_path(SEEN_PATH)
    if not path.exists():
        return set()
    seen = set()
    try:
        with open(path, newline="", encoding="utf-8") as fh:
            for row in csv.DictReader(fh):
                seen.add(row.get("entry_id", "").strip())
    except Exception as exc:
        log.warning("Could not read seen-IDs file: %s", exc)
    return seen


def _save_seen_id(entry_id: str, title: str, source: str) -> None:
    path = safe_path(SEEN_PATH)
    path.parent.mkdir(parents=True, exist_ok=True)
    write_header = not path.exists()
    try:
        with open(path, "a", newline="", encoding="utf-8") as fh:
            writer = csv.DictWriter(fh, fieldnames=["entry_id", "title", "source", "seen_at"])
            if write_header:
                writer.writeheader()
            writer.writerow({
                "entry_id": entry_id,
                "title":    title,
                "source":   source,
                "seen_at":  datetime.now(timezone.utc).isoformat(),
            })
    except Exception as exc:
        log.error("Failed to persist seen entry %s: %s", entry_id, exc)


def _load_queue() -> list:
    path = safe_path(QUEUE_PATH)
    if not path.exists():
        return []
    try:
        with open(path, encoding="utf-8") as fh:
            return json.load(fh)
    except Exception as exc:
        log.warning("Could not load queue: %s", exc)
        return []


def _save_queue(queue: list) -> None:
    path = safe_path(QUEUE_PATH)
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        with open(path, "w", encoding="utf-8") as fh:
            json.dump(queue, fh, indent=2, ensure_ascii=False)
    except Exception as exc:
        log.error("Failed to save queue: %s", exc)

# ---------------------------------------------------------------------------
# Feed fetching
# ---------------------------------------------------------------------------

def _fetch_url(url: str, timeout: int = 20) -> bytes:
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "PRINTMAXX-AppFactoryFeeder/1.0 (automation bot)"},
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read()


def _parse_blogger_feed(raw: bytes, source_key: str) -> list:
    """Parse Google Blogger/Atom JSON feed."""
    entries = []
    try:
        data = json.loads(raw)
        for item in data.get("feed", {}).get("entry", []):
            title  = item.get("title", {}).get("$t", "")
            link   = next(
                (l["href"] for l in item.get("link", []) if l.get("rel") == "alternate"),
                "",
            )
            entry_id = item.get("id", {}).get("$t", link or title)
            summary  = item.get("summary", {}).get("$t", "")
            published = item.get("published", {}).get("$t", "")
            entries.append({
                "id":        entry_id,
                "title":     title,
                "link":      link,
                "summary":   summary,
                "published": published,
                "source":    source_key,
            })
    except Exception as exc:
        log.warning("Blogger feed parse error (%s): %s", source_key, exc)
    return entries


def _parse_firebase_release_json(raw: bytes, source_key: str) -> list:
    """Parse Firebase JS SDK release notes JSON (list of version objects)."""
    entries = []
    try:
        data = json.loads(raw)
        releases = data if isinstance(data, list) else data.get("releases", [])
        for rel in releases[:20]:  # cap to 20 most-recent
            version = rel.get("version", "unknown")
            entry_id = f"firebase-js-{version}"
            title    = f"Firebase JS SDK {version}"
            summary  = " | ".join(rel.get("changes", []))
            entries.append({
                "id":        entry_id,
                "title":     title,
                "link":      "https://firebase.google.com/support/release-notes/js",
                "summary":   summary,
                "published": rel.get("date", ""),
                "source":    source_key,
            })
    except Exception as exc:
        log.warning("Firebase release notes parse error (%s): %s", source_key, exc)
    return entries


def fetch_all_entries() -> list:
    all_entries = []
    for key, url in FEED_SOURCES.items():
        log.info("Fetching feed: %s", key)
        try:
            raw = _fetch_url(url)
            if key == "google_aistudio_blog":
                entries = _parse_blogger_feed(raw, key)
            elif key == "firebase_release_notes":
                entries = _parse_firebase_release_json(raw, key)
            else:
                entries = []
            log.info("  -> %d entries from %s", len(entries), key)
            all_entries.extend(entries)
        except urllib.error.URLError as exc:
            log.error("Network error fetching %s: %s", key, exc)
        except Exception as exc:
            log.error("Unexpected error fetching %s: %s", key, exc)
    return all_entries

# ---------------------------------------------------------------------------
# Priority scoring & filtering
# ---------------------------------------------------------------------------

def _score_entry(entry: dict) -> int:
    text = (entry.get("title", "") + " " + entry.get("summary", "")).lower()
    return sum(1 for kw in PRIORITY_KEYWORDS if kw in text)


def filter_relevant(entries: list) -> list:
    scored = [(e, _score_entry(e)) for e in entries]
    relevant = [(e, s) for e, s in scored if s > 0]
    relevant.sort(key=lambda x: x[1], reverse=True)
    return [e for e, _ in relevant]

# ---------------------------------------------------------------------------
# Scaffold generation
# ---------------------------------------------------------------------------

def _scaffold_name(title: str) -> str:
    slug = "".join(c if c.isalnum() or c in "-_" else "_" for c in title.lower())
    slug = slug.strip("_")[:48]
    ts   = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    return f"{ts}_{slug}"


def generate_scaffold(entry: dict, dry_run: bool = False) -> Path:
    name    = _scaffold_name(entry["title"])
    out_dir = safe_path(SCAFFOLDS_DIR / name)

    manifest = {
        "scaffold_name":  name,
        "generated_at":   datetime.now(timezone.utc).isoformat(),
        "source_entry":   entry,
        "vibe_stack":     VIBE_STACK_TEMPLATE,
        "build_status":   "queued",
        "opportunity":    {
            "title":   entry["title"],
            "link":    entry.get("link", ""),
            "summary": entry.get("summary", "")[:500],
        },
    }

    readme_lines = [
        f"# {entry['title']}",
        "",
        f"> Auto-generated by PRINTMAXX App Factory Feeder on "
        f"{datetime.now(timezone.utc).strftime('%Y-%m-%d')}",
        "",
        "## Opportunity",
        entry.get("summary", "")[:800],
        "",
        "## Stack",
        *[f"- **{k}**: {v}" for k, v in VIBE_STACK_TEMPLATE.items()],
        "",
        "## Next Steps",
        "1. Review opportunity summary above",
        "2. Confirm stack selections in manifest.json",
        "3. Run `firebase init` to bootstrap project",
        "4. Implement core feature using Gemini API",
        "5. Deploy via `firebase deploy`",
        "",
        f"Source: {entry.get('link', 'n/a')}",
    ]

    firebase_json = {
        "hosting": {
            "public":  "public",
            "ignore":  ["firebase.json", "**/.*", "**/node_modules/**"],
            "rewrites": [{"source": "**", "destination": "/index.html"}],
        },
        "functions": {
            "source":  "functions",
            "runtime": VIBE_STACK_TEMPLATE["runtime"],
        },
    }

    package_json = {
        "name":    name.replace("_", "-"),
        "version": "0.1.0",
        "private": True,
        "scripts": {
            "dev":    "vite",
            "build":  "vite build",
            "deploy": "firebase deploy",
        },
        "dependencies": {
            "firebase":                 "^10.0.0",
            "@google/generative-ai":    "^0.21.0",
        },
        "devDependencies": {
            "vite": "^5.0.0",
        },
    }

    if dry_run:
        log.info("[DRY-RUN] Would create scaffold: %s", out_dir)
        return out_dir

    out_dir.mkdir(parents=True, exist_ok=True)

    def _write(rel: str, content: str) -> None:
        target = safe_path(out_dir / rel)
        target.parent.mkdir(parents=True, exist_ok=True)
        with open(target, "w", encoding="utf-8") as fh:
            fh.write(content)

    _write("manifest.json",   json.dumps(manifest, indent=2, ensure_ascii=False))
    _write("README.md",       "\n".join(readme_lines))
    _write("firebase.json",   json.dumps(firebase_json, indent=2))
    _write("package.json",    json.dumps(package_json, indent=2))
    _write("src/.gitkeep",    "")
    _write("functions/index.js", (
        "// Cloud Functions entry point\n"
        "const { onRequest } = require('firebase-functions/v2/https');\n"
        "exports.api = onRequest(async (req, res) => {\n"
        "  res.json({ status: 'ok' });\n"
        "});\n"
    ))

    log.info("Scaffold created: %s", out_dir)
    return out_dir

# ---------------------------------------------------------------------------
# App Factory queue
# ---------------------------------------------------------------------------

def enqueue_opportunity(entry: dict, scaffold_path: Path, dry_run: bool = False) -> None:
    queue = _load_queue()
    opp = {
        "queued_at":     datetime.now(timezone.utc).isoformat(),
        "priority_score": _score_entry(entry),
        "title":         entry["title"],
        "link":          entry.get("link", ""),
        "source":        entry.get("source", ""),
        "published":     entry.get("published", ""),
        "scaffold_path": str(scaffold_path),
        "build_status":  "queued",
        "tags":          [kw for kw in PRIORITY_KEYWORDS
                          if kw in (entry["title"] + entry.get("summary", "")).lower()],
    }
    if dry_run:
        log.info("[DRY-RUN] Would enqueue: %s", entry["title"])
        return
    queue.append(opp)
    queue.sort(key=lambda x: x.get("priority_score", 0), reverse=True)
    _save_queue(queue)
    log.info("Enqueued opportunity: %s (score=%d)", entry["title"], opp["priority_score"])

# ---------------------------------------------------------------------------
# Optional: emit a shell hook for downstream processes
# ---------------------------------------------------------------------------

def _notify_queue_update(count: int) -> None:
    hook = PROJECT / "AUTOMATIONS" / "hooks" / "on_queue_update.sh"
    try:
        hook_path = safe_path(hook)
        if hook_path.exists():
            subprocess.run(
                [str(hook_path), str(count)],
                timeout=15,
                check=False,
                capture_output=True,
            )
    except Exception as exc:
        log.debug("Hook notification skipped: %s", exc)

# ---------------------------------------------------------------------------
# CLI actions
# ---------------------------------------------------------------------------

def action_run(dry_run: bool = False) -> int:
    log.info("=== App Factory Feeder RUN (dry_run=%s) ===", dry_run)
    skills = recall_skills_for_task("monitor google ai studio and firebase for new features")
    if skills:
        log.debug("Recalled skills: %s", skills)

    entries     = fetch_all_entries()
    relevant    = filter_relevant(entries)
    seen_ids    = _load_seen_ids()
    new_entries = [e for e in relevant if e["id"] not in seen_ids]

    log.info("Total fetched: %d | Relevant: %d | New: %d",
             len(entries), len(relevant), len(new_entries))

    enqueued = 0
    for entry in new_entries:
        try:
            scaffold = generate_scaffold(entry, dry_run=dry_run)
            enqueue_opportunity(entry, scaffold, dry_run=dry_run)
            if not dry_run:
                _save_seen_id(entry["id"], entry["title"], entry["source"])
            enqueued += 1
        except Exception as exc:
            log.error("Failed to process entry '%s': %s", entry.get("title"), exc)

    if enqueued:
        _notify_queue_update(enqueued)

    result = {"new_entries": enqueued, "total_fetched": len(entries), "relevant": len(relevant)}
    capture_skill_from_result(result, "aistudio_app_factory_feeder")
    log.info("Run complete. Enqueued %d new opportunities.", enqueued)
    return 0


def action_status() -> int:
    queue = _load_queue()
    seen_ids = _load_seen_ids()
    print(json.dumps({
        "queue_length":   len(queue),
        "seen_entries":   len(seen_ids),
        "queue_path":     str(QUEUE_PATH),
        "log_path":       str(LOG_PATH),
        "scaffolds_dir":  str(SCAFFOLDS_DIR),
        "top_queued": [
            {"title": q["title"], "score": q["priority_score"], "status": q["build_status"]}
            for q in queue[:5]
        ],
    }, indent=2))
    return 0

# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="PRINTMAXX: Google AI Studio App Factory Feeder",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--run",     action="store_true", help="Fetch feeds and process new entries")
    group.add_argument("--status",  action="store_true", help="Print queue and state summary")
    group.add_argument("--dry-run", action="store_true", dest="dry_run",
                       help="Simulate run without writing files or updating queue")
    args = parser.parse_args()

    try:
        if args.run:
            sys.exit(action_run(dry_run=False))
        elif args.dry_run:
            sys.exit(action_run(dry_run=True))
        elif args.status:
            sys.exit(action_status())
    except KeyboardInterrupt:
        log.info("Interrupted.")
        sys.exit(130)
    except Exception as exc:
        log.exception("Fatal error: %s", exc)
        sys.exit(1)


if __name__ == "__main__":
    main()