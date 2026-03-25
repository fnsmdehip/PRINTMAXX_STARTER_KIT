#!/usr/bin/env python3
"""
PRINTMAXX Automation: AI Policy Engagement Converter
TYPE: poster

Converts AI policy/government news into high-engagement posts for the AI
entrepreneur audience. Specializes in extracting irony and tension angles
from bureaucratic contradictions — e.g., Trump publicly kills
Pentagon-Anthropic deal while Pentagon privately tells Anthropic they're
nearly aligned. That gap between public narrative and private reality is
engagement gold.
"""

import argparse
import csv
import json
import logging
import sys
import urllib.request
import urllib.error
from datetime import datetime
from pathlib import Path

# ---------------------------------------------------------------------------
# Bootstrap: resolve _common from sibling AUTOMATIONS structure
# ---------------------------------------------------------------------------
PROJECT = Path(__file__).resolve().parent.parent
_common_path = PROJECT / "AUTOMATIONS" / "_common"
if str(_common_path) not in sys.path:
    sys.path.insert(0, str(_common_path))

try:
    from _common import (  # noqa: E402  (imported after path manipulation)
        PROJECT as _COMMON_PROJECT,
        safe_path,
        recall_skills_for_task,
        capture_skill_from_result,
    )
    # Trust the canonical PROJECT from _common if available
    PROJECT = _COMMON_PROJECT
except ImportError:
    # Fallback: define locally so the script still runs standalone
    def safe_path(base: Path, *parts: str) -> Path:
        """Return resolved path, raising ValueError if outside *base*."""
        resolved = base.joinpath(*parts).resolve()
        if not str(resolved).startswith(str(base.resolve())):
            raise ValueError(
                f"Path escape attempt: {resolved} is outside {base}"
            )
        return resolved

    def recall_skills_for_task(task_name: str) -> dict:  # type: ignore[misc]
        return {}

    def capture_skill_from_result(result: dict, skill_name: str) -> None:  # type: ignore[misc]
        pass


# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
AUTOMATIONS_DIR = safe_path(PROJECT, "AUTOMATIONS")
LOG_DIR = safe_path(AUTOMATIONS_DIR, "logs")
LOG_FILE = safe_path(LOG_DIR, "ai_policy_engagement_converter.log")
OUTPUT_DIR = safe_path(AUTOMATIONS_DIR, "output", "ai_policy_engagement_converter")
STATUS_FILE = safe_path(OUTPUT_DIR, "status.json")
POSTS_CSV = safe_path(OUTPUT_DIR, "posts.csv")

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------
LOG_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE, mode="a", encoding="utf-8"),
        logging.StreamHandler(sys.stdout),
    ],
)
log = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Content engine
# ---------------------------------------------------------------------------

# Seed story that drove this automation instance
SEED_STORY = {
    "headline": (
        "New court filing reveals Pentagon told Anthropic the two sides were "
        "nearly aligned — a week after Trump declared the relationship kaput."
    ),
    "actors": ["Pentagon", "Anthropic", "Trump administration"],
    "irony": (
        "Trump kills deal publicly; Pentagon privately says they're almost there."
    ),
    "audience": "AI entrepreneurs",
    "signal_type": "controversy",
    "engagement_hook": "gap between public narrative and private reality",
}

POST_TEMPLATES = [
    # Template 0 — pure irony drop
    (
        "The gap between the public story and the private story in "
        "AI policy right now is staggering.\n\n"
        "Trump declares the Pentagon-Anthropic relationship dead.\n\n"
        "Meanwhile a court filing shows Pentagon told Anthropic they were "
        "NEARLY ALIGNED — one week later.\n\n"
        "This isn't just drama. It's a signal about how AI deals actually "
        "get done in DC: publicly killed, privately negotiated.\n\n"
        "If you're building in the AI space, understand this dynamic. "
        "The headline is never the whole story.\n\n"
        "What does this tell you about where enterprise AI is headed? "
        "Drop your read below."
    ),
    # Template 1 — founder lens
    (
        "Founder take on the Pentagon-Anthropic situation nobody's saying:\n\n"
        "The real lesson isn't 'government is chaotic.'\n\n"
        "It's that in high-stakes AI procurement, the DEAL and the "
        "ANNOUNCEMENT are two completely different processes.\n\n"
        "Trump publicly kills it. Pentagon privately says 'we're basically "
        "aligned.' Court filing makes it official.\n\n"
        "Translation for AI founders:\n"
        "→ Public statements from politicians ≠ operational reality\n"
        "→ The bureaucracy has its own momentum\n"
        "→ Never let a press release end your pipeline conversation\n\n"
        "The irony angle here is engagement gold — but the strategic signal "
        "is even more valuable.\n\n"
        "Thoughts?"
    ),
    # Template 2 — short punchy hook
    (
        "Hot take: the most interesting AI policy story right now isn't "
        "the ban or the executive order.\n\n"
        "It's the Pentagon-Anthropic gap.\n\n"
        "Public: Trump kills the deal.\n"
        "Private (per court filing): Pentagon says they were nearly aligned "
        "— a week after.\n\n"
        "That contradiction IS the story.\n\n"
        "AI entrepreneurs: this is how DC works. "
        "Learn to read the private signal, not the public noise.\n\n"
        "Agree or disagree?"
    ),
    # Template 3 — data/timeline frame
    (
        "Timeline that every AI founder should screenshot:\n\n"
        "Week 0 → Trump administration publicly declares Pentagon-Anthropic "
        "relationship over.\n\n"
        "Week 1 → Court filing surfaces. Pentagon told Anthropic the two "
        "sides were nearly aligned.\n\n"
        "The delta between those two data points is the entire story of how "
        "AI policy actually works in 2024.\n\n"
        "Public performance vs private negotiation.\n"
        "Political optics vs operational reality.\n\n"
        "If you're navigating government AI contracts — or watching this "
        "space for investment signals — the private channel is where the "
        "truth lives.\n\n"
        "What's your read on where this lands?"
    ),
    # Template 4 — engagement bait / question-first
    (
        "Genuine question for the AI entrepreneur community:\n\n"
        "How do you interpret the Pentagon-Anthropic reversal?\n\n"
        "Trump says deal is dead. Court filing says Pentagon privately told "
        "Anthropic they were nearly aligned — same week.\n\n"
        "Option A: Classic DC chaos, nothing to read into it.\n"
        "Option B: The public kill was political cover; the deal moves "
        "forward through back channels.\n"
        "Option C: This exposes exactly why AI companies should be cautious "
        "about government dependency.\n\n"
        "I'm leaning B, but genuinely curious where this community lands.\n\n"
        "Vote / comment below."
    ),
]

CSV_FIELDNAMES = [
    "generated_at",
    "template_index",
    "platform_hint",
    "character_count",
    "post_text",
]


# ---------------------------------------------------------------------------
# Core functions
# ---------------------------------------------------------------------------

def _write_status(state: str, detail: str, dry_run: bool = False) -> None:
    payload = {
        "script": "ai_policy_engagement_converter",
        "state": state,
        "detail": detail,
        "dry_run": dry_run,
        "timestamp": datetime.utcnow().isoformat() + "Z",
    }
    if not dry_run:
        try:
            target = safe_path(OUTPUT_DIR, "status.json")
            target.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        except Exception as exc:  # noqa: BLE001
            log.warning("Could not write status file: %s", exc)
    else:
        log.info("[DRY-RUN] Would write status: %s", json.dumps(payload))


def generate_posts() -> list[dict]:
    """Build the list of post dicts from templates + seed story."""
    posts = []
    now = datetime.utcnow().isoformat() + "Z"
    for idx, template in enumerate(POST_TEMPLATES):
        post_text = template.strip()
        posts.append(
            {
                "generated_at": now,
                "template_index": idx,
                "platform_hint": "LinkedIn / Twitter / Threads",
                "character_count": len(post_text),
                "post_text": post_text,
            }
        )
    return posts


def write_posts_csv(posts: list[dict], dry_run: bool = False) -> None:
    if dry_run:
        log.info("[DRY-RUN] Would write %d posts to %s", len(posts), POSTS_CSV)
        for p in posts:
            log.info(
                "[DRY-RUN] Template %d (%d chars): %s…",
                p["template_index"],
                p["character_count"],
                p["post_text"][:80].replace("\n", " "),
            )
        return

    target = safe_path(OUTPUT_DIR, "posts.csv")
    try:
        with target.open("w", newline="", encoding="utf-8") as fh:
            writer = csv.DictWriter(fh, fieldnames=CSV_FIELDNAMES)
            writer.writeheader()
            writer.writerows(posts)
        log.info("Wrote %d posts to %s", len(posts), target)
    except OSError as exc:
        log.error("Failed to write posts CSV: %s", exc)
        raise


def run(dry_run: bool = False) -> None:
    """Main execution: generate posts, persist, update status."""
    log.info("=== ai_policy_engagement_converter START (dry_run=%s) ===", dry_run)
    _write_status("running", "generating posts", dry_run=dry_run)

    try:
        # Optional: pull skill context if _common is available
        try:
            skills = recall_skills_for_task("ai_policy_engagement_converter")
            if skills:
                log.info("Recalled %d skills from _common", len(skills))
        except Exception:  # noqa: BLE001
            pass

        posts = generate_posts()
        log.info("Generated %d post variants", len(posts))

        write_posts_csv(posts, dry_run=dry_run)

        # Capture skill result back into _common if available
        try:
            capture_skill_from_result(
                {"posts_generated": len(posts), "seed_story": SEED_STORY},
                "ai_policy_engagement_converter",
            )
        except Exception:  # noqa: BLE001
            pass

        _write_status(
            "success",
            f"Generated {len(posts)} posts",
            dry_run=dry_run,
        )
        log.info("=== ai_policy_engagement_converter DONE ===")

    except Exception as exc:  # noqa: BLE001
        log.exception("Fatal error during run: %s", exc)
        _write_status("error", str(exc), dry_run=dry_run)
        sys.exit(1)


def show_status() -> None:
    """Print current status.json to stdout."""
    try:
        target = safe_path(OUTPUT_DIR, "status.json")
        if target.exists():
            print(target.read_text(encoding="utf-8"))
        else:
            print(json.dumps({"state": "never_run", "detail": "No status file found."}))
    except Exception as exc:  # noqa: BLE001
        log.error("Could not read status: %s", exc)
        sys.exit(1)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "PRINTMAXX: AI Policy Engagement Converter — "
            "turns AI policy/government news into engagement bait posts "
            "for the AI entrepreneur audience."
        )
    )
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument(
        "--run",
        action="store_true",
        help="Generate posts and write output files.",
    )
    mode.add_argument(
        "--status",
        action="store_true",
        help="Print the current status.json and exit.",
    )
    mode.add_argument(
        "--dry-run",
        action="store_true",
        help="Simulate a run without writing any files.",
    )
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if args.status:
        show_status()
    elif args.dry_run:
        run(dry_run=True)
    elif args.run:
        run(dry_run=False)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()