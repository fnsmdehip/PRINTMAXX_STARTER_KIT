#!/usr/bin/env python3
"""
PRINTMAXX Automation: Post-Deployment User Acquisition Pipeline

After each app ships to Surge/Vercel/Netlify, auto-drafts community posts for
Reddit (r/SideProject, r/IndieHackers, r/webdev), HN Show HN, and Product Hunt.
Pulls the latest deployed app URL from OPS/DEPLOYMENT_URLS.md, generates
niche-specific value-first posts with engagement hooks, and queues drafts to
CONTENT/social/posting_queue/ for human review before publishing.

Secondary: queries Firebase for demo viewers or early signups and triggers the
cold email sequence via existing outbound scripts in AUTOMATIONS/outbound/.

Usage:
    python saas_demo_to_user_pipeline.py --run
    python saas_demo_to_user_pipeline.py --dry-run
    python saas_demo_to_user_pipeline.py --status
"""

import argparse
import csv
import json
import logging
import re
import subprocess
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

try:
    from _common import PROJECT, safe_path, recall_skills_for_task, capture_skill_from_result
except ImportError:
    PROJECT = Path(__file__).resolve().parent.parent

    def safe_path(p):
        resolved = Path(p).resolve()
        if not str(resolved).startswith(str(PROJECT.resolve())):
            raise ValueError(f"Path '{resolved}' escapes PROJECT root '{PROJECT}'")
        return resolved

    def recall_skills_for_task(task):
        return []

    def capture_skill_from_result(result, task):
        pass


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

LOG_FILE = safe_path(PROJECT / "AUTOMATIONS" / "logs" / "saas_demo_to_user_pipeline.log")
DEPLOYMENT_URLS_FILE = safe_path(PROJECT / "OPS" / "DEPLOYMENT_URLS.md")
QUEUE_DIR = safe_path(PROJECT / "CONTENT" / "social" / "posting_queue")
STATUS_FILE = safe_path(PROJECT / "AUTOMATIONS" / "logs" / "saas_demo_to_user_pipeline_status.json")
OUTBOUND_SCRIPT = safe_path(PROJECT / "AUTOMATIONS" / "outbound" / "cold_email_sequence.py")
FIREBASE_EXPORT_SCRIPT = safe_path(PROJECT / "AUTOMATIONS" / "outbound" / "firebase_export_contacts.py")

PLATFORMS = ["reddit_sideproject", "reddit_indiehackers", "reddit_webdev", "hn_showhn", "producthunt"]

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------


def setup_logging():
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler(str(LOG_FILE), mode="a"),
            logging.StreamHandler(sys.stdout),
        ],
    )


log = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Deployment URL parsing
# ---------------------------------------------------------------------------


def parse_deployment_urls():
    """Parse OPS/DEPLOYMENT_URLS.md and return list of deployment dicts."""
    if not DEPLOYMENT_URLS_FILE.exists():
        log.warning("DEPLOYMENT_URLS.md not found at %s", DEPLOYMENT_URLS_FILE)
        return []

    deployments = []
    url_pattern = re.compile(r"https?://[^\s\)\"\']+")

    try:
        lines = DEPLOYMENT_URLS_FILE.read_text(encoding="utf-8").splitlines()
        for line in lines:
            urls = url_pattern.findall(line)
            for url in urls:
                app_name = _infer_app_name(url, line)
                platform = _infer_platform(url)
                deployments.append({"url": url, "app_name": app_name, "platform": platform, "line": line.strip()})
    except OSError as exc:
        log.error("Failed to read deployment URLs file: %s", exc)

    return deployments


def _infer_app_name(url, line):
    """Best-effort app name from URL or surrounding markdown."""
    # Try bold/header text before the URL on same line
    heading_match = re.search(r"[#*_]{1,3}([A-Za-z0-9 _\-]+)[#*_]{0,3}", line)
    if heading_match:
        return heading_match.group(1).strip()
    # Fall back to hostname slug
    host = re.sub(r"https?://", "", url).split("/")[0]
    slug = re.sub(r"\.(surge\.sh|vercel\.app|netlify\.app|web\.app|firebaseapp\.com)$", "", host)
    return slug.replace("-", " ").replace("_", " ").title()


def _infer_platform(url):
    for keyword in ("surge", "vercel", "netlify", "firebase", "web.app"):
        if keyword in url:
            return keyword
    return "unknown"


def get_latest_deployment():
    """Return the most recently listed deployment entry, or None."""
    deployments = parse_deployment_urls()
    return deployments[-1] if deployments else None


# ---------------------------------------------------------------------------
# Post generation
# ---------------------------------------------------------------------------


def _timestamp_tag():
    return datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")


def generate_reddit_sideproject_post(app_name, url):
    title = f"I built {app_name} – here's the one workflow trick that made it actually useful"
    body = f"""Hey r/SideProject,

Shipped something this week that I've been heads-down on for a while: **{app_name}**.

**The problem it solves:** [describe the specific pain point in 1–2 sentences]

**Why I built it instead of using X:** Most tools I found required [friction point]. {app_name} does [key differentiator] without the setup overhead.

**What it does in 30 seconds:**
1. [Step 1]
2. [Step 2]
3. [Result]

Live at: {url}

Happy to answer any questions – and genuinely curious: how are others handling [related problem] right now? I keep hearing people mention [approach], does that actually work at scale?
"""
    return {"title": title, "body": body}


def generate_reddit_indiehackers_post(app_name, url):
    title = f"Show IH: {app_name} – launched today, here's the metrics so far"
    body = f"""Hey IH,

Just shipped **{app_name}** after [X weeks] of building: {url}

**The idea:** [One-line value prop]

**Traction so far (be honest):**
- Signups: [N]
- Demo sessions: [N]
- MRR: $0 (but here's my acquisition plan)

**What's working:** [early signal]
**What's not:** [honest struggle]

My current plan to get first 10 paying users is [strategy]. Would love feedback from anyone who's been through early distribution in this space.

What's the weirdest growth lever that worked for you early on?
"""
    return {"title": title, "body": body}


def generate_reddit_webdev_post(app_name, url):
    title = f"Show /r/webdev: {app_name} – built with [stack], open to feedback on the UX"
    body = f"""Hey webdev,

Shipped **{app_name}** this week and wanted to share it here since I borrowed heavily from discussions in this community.

**Stack:** [list your stack]
**Live demo:** {url}

**One technical decision I'm curious about:** [specific tradeoff, e.g. "I went with SSR over CSR for X because Y – was that the right call?"]

The frontend was the trickiest part – specifically [specific challenge]. Solved it by [approach].

If you have 2 minutes to poke at it and tell me the first thing that confused you, I'd genuinely appreciate it.
"""
    return {"title": title, "body": body}


def generate_hn_showhn_post(app_name, url):
    title = f"Show HN: {app_name} – [one-line description of what it does]"
    body = f"""Hi HN,

{app_name} ({url}) is a [brief description].

**The core insight:** [non-obvious observation about the problem space]

**Why now:** [market timing or technology unlock]

**What's different:** Unlike [existing approach], {app_name} [key differentiator] because [reason that's technically or operationally hard to replicate].

Built by [team size]. [Current state: alpha/beta/launched]. Looking for early feedback from people who deal with [target use case] regularly.

What am I missing?
"""
    return {"title": title, "body": body}


def generate_producthunt_post(app_name, url):
    tagline = f"{app_name} – [one punchy value prop under 60 chars]"
    description = f"""**What is {app_name}?**
[2–3 sentence elevator pitch]

**Who it's for:**
[specific persona description]

**How it works:**
→ [Step 1]
→ [Step 2]
→ [Outcome]

**Why we built it:**
[founder story in 2 sentences]

Try it free: {url}

We're the makers — ask us anything. Would especially love feedback on [specific aspect].
"""
    return {"tagline": tagline, "description": description, "url": url}


POST_GENERATORS = {
    "reddit_sideproject": generate_reddit_sideproject_post,
    "reddit_indiehackers": generate_reddit_indiehackers_post,
    "reddit_webdev": generate_reddit_webdev_post,
    "hn_showhn": generate_hn_showhn_post,
    "producthunt": generate_producthunt_post,
}


# ---------------------------------------------------------------------------
# Queue management
# ---------------------------------------------------------------------------


def queue_post(platform, app_name, content, deployment_url, dry_run=False):
    """Write a draft post to the posting queue directory."""
    QUEUE_DIR.mkdir(parents=True, exist_ok=True)
    tag = _timestamp_tag()
    filename = f"{tag}_{platform}_{re.sub(r'[^a-z0-9]', '_', app_name.lower())}.json"
    dest = safe_path(QUEUE_DIR / filename)

    payload = {
        "queued_at": datetime.now(timezone.utc).isoformat(),
        "platform": platform,
        "app_name": app_name,
        "deployment_url": deployment_url,
        "status": "pending_review",
        "content": content,
    }

    if dry_run:
        log.info("[DRY-RUN] Would write %s:\n%s", dest, json.dumps(payload, indent=2))
        return None

    try:
        dest.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        log.info("Queued post: %s", dest)
        return str(dest)
    except OSError as exc:
        log.error("Failed to write post queue file %s: %s", dest, exc)
        return None


# ---------------------------------------------------------------------------
# Firebase contact extraction
# ---------------------------------------------------------------------------


def extract_firebase_contacts(dry_run=False):
    """
    Run firebase_export_contacts.py if present, parse its CSV output.
    Returns list of dicts with at least {email, name, source}.
    """
    contacts = []

    if not FIREBASE_EXPORT_SCRIPT.exists():
        log.warning("Firebase export script not found at %s – skipping contact extraction", FIREBASE_EXPORT_SCRIPT)
        return contacts

    csv_output_path = safe_path(PROJECT / "AUTOMATIONS" / "logs" / "firebase_contacts_latest.csv")

    cmd = [sys.executable, str(FIREBASE_EXPORT_SCRIPT), "--output", str(csv_output_path)]
    log.info("Running Firebase export: %s", " ".join(cmd))

    if dry_run:
        log.info("[DRY-RUN] Would run: %s", " ".join(cmd))
        return []

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        if result.returncode != 0:
            log.error("Firebase export failed (rc=%d): %s", result.returncode, result.stderr[:500])
            return contacts
        log.info("Firebase export stdout: %s", result.stdout[:500])
    except subprocess.TimeoutExpired:
        log.error("Firebase export timed out")
        return contacts
    except OSError as exc:
        log.error("Failed to launch Firebase export script: %s", exc)
        return contacts

    if not csv_output_path.exists():
        log.warning("Firebase export ran but produced no CSV at %s", csv_output_path)
        return contacts

    try:
        with csv_output_path.open(newline="", encoding="utf-8") as fh:
            reader = csv.DictReader(fh)
            for row in reader:
                contacts.append(dict(row))
        log.info("Extracted %d contacts from Firebase", len(contacts))
    except (OSError, csv.Error) as exc:
        log.error("Failed to read Firebase contacts CSV: %s", exc)

    return contacts


# ---------------------------------------------------------------------------
# Cold email trigger
# ---------------------------------------------------------------------------


def trigger_cold_email_sequence(contacts, deployment_url, app_name, dry_run=False):
    """Pass contacts to the existing cold_email_sequence.py outbound script."""
    if not contacts:
        log.info("No contacts to enqueue for cold email")
        return

    if not OUTBOUND_SCRIPT.exists():
        log.warning("Cold email script not found at %s – skipping", OUTBOUND_SCRIPT)
        return

    contacts_json_path = safe_path(PROJECT / "AUTOMATIONS" / "logs" / "cold_email_contacts_latest.json")

    try:
        contacts_json_path.write_text(
            json.dumps({"app_name": app_name, "deployment_url": deployment_url, "contacts": contacts}, indent=2),
            encoding="utf-8",
        )
    except OSError as exc:
        log.error("Failed to write contacts JSON for cold email: %s", exc)
        return

    cmd = [
        sys.executable,
        str(OUTBOUND_SCRIPT),
        "--contacts",
        str(contacts_json_path),
        "--app",
        app_name,
        "--url",
        deployment_url,
    ]

    if dry_run:
        log.info("[DRY-RUN] Would trigger cold email: %s", " ".join(cmd))
        return

    log.info("Triggering cold email sequence for %d contact(s): %s", len(contacts), " ".join(cmd))
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        if result.returncode != 0:
            log.error("Cold email sequence failed (rc=%d): %s", result.returncode, result.stderr[:500])
        else:
            log.info("Cold email sequence completed: %s", result.stdout[:300])
    except subprocess.TimeoutExpired:
        log.error("Cold email sequence timed out")
    except OSError as exc:
        log.error("Failed to launch cold email script: %s", exc)


# ---------------------------------------------------------------------------
# Status reporting
# ---------------------------------------------------------------------------


def load_status():
    if not STATUS_FILE.exists():
        return {}
    try:
        return json.loads(STATUS_FILE.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}


def save_status(data):
    STATUS_FILE.parent.mkdir(parents=True, exist_ok=True)
    try:
        dest = safe_path(STATUS_FILE)
        dest.write_text(json.dumps(data, indent=2), encoding="utf-8")
    except (OSError, ValueError) as exc:
        log.error("Failed to save status: %s", exc)


def show_status():
    status = load_status()
    if not status:
        print("No pipeline runs recorded yet.")
        return

    print(f"\n=== PRINTMAXX User Acquisition Pipeline – Status ===")
    print(f"Last run : {status.get('last_run', 'never')}")
    print(f"App      : {status.get('app_name', 'unknown')} ({status.get('deployment_url', '')})")
    print(f"Posts queued  : {status.get('posts_queued', 0)}")
    print(f"Contacts found: {status.get('contacts_found', 0)}")
    print(f"Email triggered: {status.get('email_triggered', False)}")

    queue_files = sorted(QUEUE_DIR.glob("*.json")) if QUEUE_DIR.exists() else []
    print(f"\nPosting queue ({len(queue_files)} files):")
    for f in queue_files[-10:]:
        print(f"  {f.name}")

    print(f"\nFull log: {LOG_FILE}")


# ---------------------------------------------------------------------------
# Pipeline entry point
# ---------------------------------------------------------------------------


def run_pipeline(dry_run=False):
    skills = recall_skills_for_task("post-deployment user acquisition")
    log.info("Skills recalled: %s", skills)

    log.info("=== Starting PRINTMAXX User Acquisition Pipeline (dry_run=%s) ===", dry_run)

    # 1. Get latest deployment
    deployment = get_latest_deployment()
    if not deployment:
        log.error("No deployment found in %s – aborting", DEPLOYMENT_URLS_FILE)
        sys.exit(1)

    app_name = deployment["app_name"]
    url = deployment["url"]
    log.info("Target deployment: %s @ %s", app_name, url)

    # 2. Generate and queue posts for all platforms
    posts_queued = 0
    queued_files = []
    for platform in PLATFORMS:
        generator = POST_GENERATORS.get(platform)
        if not generator:
            log.warning("No generator for platform '%s' – skipping", platform)
            continue
        try:
            content = generator(app_name, url)
            path = queue_post(platform, app_name, content, url, dry_run=dry_run)
            if path or dry_run:
                posts_queued += 1
                if path:
                    queued_files.append(path)
        except Exception as exc:
            log.error("Error generating post for %s: %s", platform, exc)

    log.info("Posts queued: %d / %d", posts_queued, len(PLATFORMS))

    # 3. Extract Firebase contacts
    contacts = extract_firebase_contacts(dry_run=dry_run)

    # 4. Trigger cold email sequence
    email_triggered = False
    if contacts:
        try:
            trigger_cold_email_sequence(contacts, url, app_name, dry_run=dry_run)
            email_triggered = True
        except Exception as exc:
            log.error("Cold email trigger failed: %s", exc)
    else:
        log.info("No Firebase contacts found – skipping cold email")

    # 5. Save status
    status = {
        "last_run": datetime.now(timezone.utc).isoformat(),
        "app_name": app_name,
        "deployment_url": url,
        "posts_queued": posts_queued,
        "queued_files": queued_files,
        "contacts_found": len(contacts),
        "email_triggered": email_triggered,
        "dry_run": dry_run,
    }
    if not dry_run:
        save_status(status)

    result_summary = json.dumps(status, indent=2)
    capture_skill_from_result(result_summary, "post-deployment user acquisition")

    log.info("Pipeline complete: %s", result_summary)
    return status


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def main():
    setup_logging()

    parser = argparse.ArgumentParser(
        description="PRINTMAXX post-deployment user acquisition pipeline",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--run", action="store_true", help="Execute the full pipeline")
    group.add_argument("--dry-run", action="store_true", help="Simulate the pipeline without writing posts or sending email")
    group.add_argument("--status", action="store_true", help="Show status of last run and pending queue")

    args = parser.parse_args()

    try:
        if args.status:
            show_status()
        elif args.dry_run:
            run_pipeline(dry_run=True)
        elif args.run:
            run_pipeline(dry_run=False)
    except KeyboardInterrupt:
        log.warning("Pipeline interrupted by user")
        sys.exit(130)
    except Exception as exc:
        log.exception("Unhandled pipeline error: %s", exc)
        sys.exit(1)


if __name__ == "__main__":
    main()