#!/usr/bin/env python3
"""
PRINTMAXX Automation System — PH Launch Content Pipeline
ph_ai_devtools_content_pipeline.py

Generates dev-audience content for the GitAgent by Lyzr Product Hunt launch:
  - Tweet threads on repo-as-agent pattern
  - Reddit posts for r/devtools and r/MachineLearning
  - LinkedIn posts targeting engineering managers

Secondary objective: position PRINTMAXX EAS as the
'GitAgent setup + custom repo agent integration' service for dev teams.

Checks lyzr.ai for affiliate program details and embeds referral context
in all generated content assets.

Usage:
  python ph_ai_devtools_content_pipeline.py --run
  python ph_ai_devtools_content_pipeline.py --status
  python ph_ai_devtools_content_pipeline.py --dry-run
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

# ---------------------------------------------------------------------------
# Bootstrap: import from _common or define fallbacks
# ---------------------------------------------------------------------------
try:
    from _common import PROJECT, safe_path, recall_skills_for_task, capture_skill_from_result
except ImportError:
    PROJECT = Path(__file__).resolve().parent.parent

    def safe_path(target):
        """Resolve *target* and assert it lives inside PROJECT."""
        resolved = Path(target).resolve()
        try:
            resolved.relative_to(PROJECT)
        except ValueError:
            raise ValueError(
                f"Path '{resolved}' is outside PROJECT root '{PROJECT}'. "
                "Refusing to write."
            )
        return resolved

    def recall_skills_for_task(task_name: str) -> dict:
        return {}

    def capture_skill_from_result(task_name: str, result: dict) -> None:
        pass

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
AUTOMATIONS_DIR  = PROJECT / "AUTOMATIONS"
LOG_DIR          = AUTOMATIONS_DIR / "logs"
OUTPUT_DIR       = AUTOMATIONS_DIR / "output" / "ph_ai_devtools_content_pipeline"
STATUS_FILE      = OUTPUT_DIR / "status.json"
CONTENT_CSV      = OUTPUT_DIR / "content_assets.csv"
CONTENT_JSON     = OUTPUT_DIR / "content_assets.json"
AFFILIATE_CACHE  = OUTPUT_DIR / "lyzr_affiliate_cache.json"
LOG_FILE         = LOG_DIR / "ph_ai_devtools_content_pipeline.log"

LYZR_AFFILIATE_URL = "https://lyzr.ai/affiliate"

# ---------------------------------------------------------------------------
# Logging (append mode, cron-safe — no interactive output required)
# ---------------------------------------------------------------------------

def _setup_logging(dry_run: bool = False) -> logging.Logger:
    log_path = safe_path(LOG_FILE)
    log_path.parent.mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger("printmaxx.ph_pipeline")
    logger.setLevel(logging.DEBUG)

    fmt = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%dT%H:%M:%S%z",
    )

    fh = logging.FileHandler(str(log_path), mode="a", encoding="utf-8")
    fh.setFormatter(fmt)
    logger.addHandler(fh)

    sh = logging.StreamHandler(sys.stdout)
    sh.setFormatter(fmt)
    sh.setLevel(logging.INFO if not dry_run else logging.DEBUG)
    logger.addHandler(sh)

    return logger

# ---------------------------------------------------------------------------
# Affiliate program probe
# ---------------------------------------------------------------------------

def fetch_affiliate_info(logger: logging.Logger) -> dict:
    """
    Attempt to retrieve affiliate / partner details from lyzr.ai.
    Returns a dict with whatever metadata is available; never raises.
    """
    cached = safe_path(AFFILIATE_CACHE)
    if cached.exists():
        try:
            data = json.loads(cached.read_text(encoding="utf-8"))
            age_hours = (
                datetime.now(tz=timezone.utc).timestamp() - data.get("fetched_at_ts", 0)
            ) / 3600
            if age_hours < 24:
                logger.info("Using cached affiliate info (age: %.1f h).", age_hours)
                return data
        except Exception as exc:
            logger.warning("Affiliate cache unreadable: %s", exc)

    result = {
        "fetched_at_ts": datetime.now(tz=timezone.utc).timestamp(),
        "fetched_at": datetime.now(tz=timezone.utc).isoformat(),
        "affiliate_url": LYZR_AFFILIATE_URL,
        "program_found": False,
        "cta": "Visit lyzr.ai/affiliate for partnership details",
        "embed_line": "Partner with Lyzr → lyzr.ai/affiliate",
        "raw_snippet": "",
    }

    try:
        req = urllib.request.Request(
            LYZR_AFFILIATE_URL,
            headers={
                "User-Agent": (
                    "Mozilla/5.0 (compatible; PRINTMAXX-ContentBot/1.0; "
                    "+https://printmaxx.io)"
                )
            },
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            body = resp.read(4096).decode("utf-8", errors="replace")
            result["raw_snippet"] = body[:512]
            # Heuristic: look for affiliate / partner / referral signals
            lower = body.lower()
            if any(kw in lower for kw in ("affiliate", "referral", "partner program", "commission")):
                result["program_found"] = True
                result["cta"] = (
                    "Join the Lyzr affiliate program → lyzr.ai/affiliate"
                )
                result["embed_line"] = (
                    "💸 Earn commissions — Lyzr affiliate program: lyzr.ai/affiliate"
                )
                logger.info("Affiliate program signals detected on lyzr.ai.")
            else:
                logger.info(
                    "No affiliate program signals detected; using generic CTA."
                )
    except urllib.error.HTTPError as exc:
        logger.warning("HTTP %s fetching affiliate page: %s", exc.code, exc)
    except urllib.error.URLError as exc:
        logger.warning("Network error fetching affiliate page: %s", exc)
    except Exception as exc:
        logger.warning("Unexpected error fetching affiliate page: %s", exc)

    # Persist cache
    try:
        cached.parent.mkdir(parents=True, exist_ok=True)
        cached.write_text(json.dumps(result, indent=2), encoding="utf-8")
    except Exception as exc:
        logger.warning("Could not cache affiliate info: %s", exc)

    return result


# ---------------------------------------------------------------------------
# Content generation helpers
# ---------------------------------------------------------------------------

HASHTAGS_TWEET = "#GitAgent #Lyzr #DevTools #AI #RepoAsAgent #BuildInPublic"
HASHTAGS_LINKEDIN = "#DevTools #AI #EngineeringLeadership #GitAgent #Lyzr #SoftwareEngineering"
PRINTMAXX_EAS_TAGLINE = (
    "PRINTMAXX EAS — GitAgent setup + custom repo agent integration for dev teams. "
    "Get your repository reasoning about itself in 48 h."
)
PRINTMAXX_CTA = "Book a discovery call → printmaxx.io/eas-gitagent"


def _ts() -> str:
    return datetime.now(tz=timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def build_tweet_thread(affiliate: dict) -> list[dict]:
    """
    Returns a list of tweet dicts (1-indexed position + body).
    Covers: repo-as-agent concept, GitAgent mechanics, dev workflow impact,
    PRINTMAXX EAS CTA, affiliate embed.
    """
    affiliate_line = affiliate["embed_line"]
    tweets = [
        {
            "position": 1,
            "platform": "twitter",
            "asset_type": "tweet_thread_opener",
            "channel": "twitter",
            "body": (
                "🧵 Your repository is smarter than you think.\n\n"
                "GitAgent by @LyzrAI just launched on Product Hunt and it's "
                "genuinely changing how dev teams interact with their own codebases.\n\n"
                "Here's the repo-as-agent pattern and why it matters for every "
                "engineering team right now 👇\n\n"
                f"{HASHTAGS_TWEET}"
            ),
        },
        {
            "position": 2,
            "platform": "twitter",
            "asset_type": "tweet_thread_body",
            "channel": "twitter",
            "body": (
                "The idea: instead of your repo being a passive archive of code, "
                "GitAgent turns it into an *active reasoner*.\n\n"
                "Your commits, PRs, issues, and docs become the memory and context "
                "of an agent that can:\n"
                "→ Answer 'why was this designed this way?'\n"
                "→ Triage new issues against historical patterns\n"
                "→ Draft PRs with full context awareness"
            ),
        },
        {
            "position": 3,
            "platform": "twitter",
            "asset_type": "tweet_thread_body",
            "channel": "twitter",
            "body": (
                "The repo-as-agent pattern flips the script on 'AI coding assistants'.\n\n"
                "Old model: AI reads your code and suggests completions.\n"
                "New model: your repository *is* the agent — it reasons, remembers, "
                "and acts on your team's behalf.\n\n"
                "Lyzr's GitAgent is one of the first production implementations "
                "of this at scale."
            ),
        },
        {
            "position": 4,
            "platform": "twitter",
            "asset_type": "tweet_thread_body",
            "channel": "twitter",
            "body": (
                "For dev teams the practical wins are:\n\n"
                "✅ Onboarding: new hires interrogate the repo instead of senior engineers\n"
                "✅ Code review: agent flags decisions that contradict historical patterns\n"
                "✅ Incident response: trace 'what changed and why' in seconds\n"
                "✅ Architecture drift: detect when implementation diverges from intent"
            ),
        },
        {
            "position": 5,
            "platform": "twitter",
            "asset_type": "tweet_thread_body",
            "channel": "twitter",
            "body": (
                "How to get started with GitAgent:\n\n"
                "1️⃣ Connect your GitHub/GitLab org\n"
                "2️⃣ Lyzr indexes commits, PRs, issues, docs\n"
                "3️⃣ Configure agent persona + access scope\n"
                "4️⃣ Expose via Slack, API, or custom UI\n\n"
                "The hard part is step 3 — scoping the agent so it's useful "
                "without being noisy. That's where teams usually need help."
            ),
        },
        {
            "position": 6,
            "platform": "twitter",
            "asset_type": "tweet_thread_cta",
            "channel": "twitter",
            "body": (
                "If you want GitAgent set up for your team with a custom repo "
                "agent integration tuned to your stack:\n\n"
                f"{PRINTMAXX_EAS_TAGLINE}\n\n"
                f"{PRINTMAXX_CTA}\n\n"
                f"{affiliate_line}"
            ),
        },
        {
            "position": 7,
            "platform": "twitter",
            "asset_type": "tweet_thread_closer",
            "channel": "twitter",
            "body": (
                "tl;dr: the repo-as-agent pattern is real, it's here, and "
                "GitAgent by @LyzrAI is the cleanest implementation I've seen.\n\n"
                "Go upvote them on Product Hunt 🔼 and try it with your own repo.\n\n"
                "Questions? Reply or DM — happy to nerd out on implementation details."
            ),
        },
    ]
    return tweets


def build_reddit_post_devtools(affiliate: dict) -> dict:
    affiliate_line = affiliate["embed_line"]
    return {
        "platform": "reddit",
        "channel": "r/devtools",
        "asset_type": "reddit_post",
        "title": (
            "GitAgent by Lyzr (PH launch today) — repo-as-agent pattern: "
            "your codebase becomes an active reasoner, not just an archive"
        ),
        "body": (
            "I've been watching the 'AI dev tools' space closely and most of what "
            "ships is autocomplete with better marketing. GitAgent is different enough "
            "that I wanted to write it up properly.\n\n"
            "**What it actually does**\n\n"
            "GitAgent (Lyzr) indexes your entire repository — commits, PRs, issues, "
            "docs, code — and exposes it as an agent you can query, configure, and "
            "integrate into your workflow. The key insight is that the *history* of "
            "your repo is as important as its current state. Why was this module "
            "structured this way? What's the decision trail behind this API design? "
            "GitAgent knows because it's read everything.\n\n"
            "**The repo-as-agent pattern**\n\n"
            "This is the conceptual shift worth understanding:\n\n"
            "- Traditional: repo = passive store, AI = external tool that reads it\n"
            "- Repo-as-agent: repo = active entity that reasons about itself and acts\n\n"
            "Practical consequences:\n\n"
            "1. **Onboarding** — new engineers ask the repo questions instead of "
            "interrupting senior devs. The agent has read every PR, every issue, "
            "every architectural discussion.\n\n"
            "2. **Code review augmentation** — the agent flags when a proposed change "
            "contradicts decisions made six months ago (with citations).\n\n"
            "3. **Incident triage** — 'what changed in the last 72 hours that could "
            "cause this?' becomes a single query.\n\n"
            "4. **Architecture compliance** — detect drift between intent (ADRs, "
            "design docs) and implementation over time.\n\n"
            "**Setup notes for teams evaluating this**\n\n"
            "The indexing is straightforward. The harder work is configuring the "
            "agent's scope and persona so it's actually useful vs. hallucinatory. "
            "You want it to say 'I don't know' rather than confabulate when it "
            "hits gaps in the history.\n\n"
            "Lyzr provides the infrastructure; the configuration layer is where "
            "you'll spend time if you're doing a serious integration.\n\n"
            "**Upvote / check it out**\n\n"
            "They're live on PH today. Worth trying against a real repo with "
            "substantial history.\n\n"
            "---\n\n"
            "*Disclosure: we help dev teams with GitAgent setup and custom repo agent "
            f"integrations at PRINTMAXX EAS ({PRINTMAXX_CTA}). {affiliate_line}*"
        ),
    }


def build_reddit_post_machinelearning(affiliate: dict) -> dict:
    affiliate_line = affiliate["embed_line"]
    return {
        "platform": "reddit",
        "channel": "r/MachineLearning",
        "asset_type": "reddit_post",
        "title": (
            "[Project] GitAgent by Lyzr — repository-grounded agents using "
            "full VCS history as context: architecture and implications"
        ),
        "body": (
            "Sharing this because the architecture choices here are genuinely "
            "interesting from an applied ML / agent systems perspective.\n\n"
            "**GitAgent (Lyzr) — high-level architecture**\n\n"
            "GitAgent ingests the full artifact graph of a software repository: "
            "source code, commit messages, PR descriptions and review threads, "
            "issue histories, wikis, and CI/CD logs. These are chunked, embedded, "
            "and stored in a retrieval layer. At query time, a planner agent "
            "routes questions to appropriate sub-retrievers and synthesizes "
            "grounded answers with source citations.\n\n"
            "**What's technically interesting**\n\n"
            "1. **Temporal grounding** — the agent is aware of *when* artifacts "
            "were created, modified, and deprecated. It can answer questions "
            "about state at a point in time, not just current state.\n\n"
            "2. **Cross-artifact reasoning** — linking a code change to the PR "
            "discussion that motivated it, to the issue that preceded that, to "
            "the architectural decision record that framed it. This multi-hop "
            "retrieval over heterogeneous artifact types is the hard part.\n\n"
            "3. **Hallucination mitigation via provenance** — every answer cites "
            "specific commits, PRs, or issues. The agent is configured to "
            "express uncertainty rather than fabricate when citations are absent.\n\n"
            "**Repo-as-agent vs. RAG-over-code**\n\n"
            "A lot of 'AI codebase search' is basically RAG over the current "
            "state of the source files. The differentiator here is treating the "
            "full VCS history as first-class context. The *why* information lives "
            "in commits and PRs, not in the source files themselves. Most tools "
            "discard this.\n\n"
            "**Open questions / limitations**\n\n"
            "- How does retrieval quality degrade as repo history grows to millions "
            "of commits? (Curious if anyone has stress-tested this)\n"
            "- Handling monorepos with heterogeneous team contexts is non-trivial\n"
            "- The agent configuration surface is powerful but requires expertise "
            "to tune — not a zero-config experience for large enterprise repos\n\n"
            "**PH launch**\n\n"
            "They launched today. Worth a look if you're interested in applied "
            "agent systems grounded in structured external knowledge.\n\n"
            "---\n\n"
            "*Note: PRINTMAXX EAS offers GitAgent setup and custom repo agent "
            f"integration services for dev teams. {PRINTMAXX_CTA}. {affiliate_line}*"
        ),
    }


def build_linkedin_post(affiliate: dict) -> dict:
    affiliate_line = affiliate["embed_line"]
    return {
        "platform": "linkedin",
        "channel": "linkedin_feed",
        "asset_type": "linkedin_post",
        "target_audience": "engineering_managers",
        "body": (
            "Your senior engineers are still the primary source of institutional "
            "knowledge about your codebase. That's an organizational risk.\n\n"
            "When they're in meetings, on PTO, or eventually move on — that "
            "knowledge walks out the door with them.\n\n"
            "GitAgent by Lyzr (launching on Product Hunt today) is one of the "
            "most credible answers I've seen to this problem.\n\n"
            "The concept is called repo-as-agent: instead of your repository "
            "being a passive archive, it becomes an active entity that can "
            "reason about its own history and answer questions about why the "
            "system is built the way it is.\n\n"
            "For engineering managers, the value propositions are concrete:\n\n"
            "→ ONBOARDING VELOCITY: new engineers get answers from the repo "
            "directly rather than scheduling 1:1s with whoever 'knows the "
            "most about auth' or 'has been here the longest'\n\n"
            "→ DECISION ARCHAEOLOGY: when a stakeholder asks 'why did we build "
            "it this way?', the answer is a query, not a war story\n\n"
            "→ CONTEXT PRESERVATION: reorgs, team rotations, and departures "
            "stop being knowledge-destruction events\n\n"
            "→ REVIEW QUALITY: your team stops re-litigating decisions that "
            "were already made and documented in PR threads nobody reads\n\n"
            "The setup requires some configuration work — defining the agent's "
            "scope, persona, and access controls to match your team's actual "
            "needs. That's where teams usually get stuck.\n\n"
            f"At PRINTMAXX EAS, we handle the full GitAgent setup and custom "
            "repo agent integration for dev teams. Most teams are operational "
            f"within 48 hours. {PRINTMAXX_CTA}\n\n"
            f"{affiliate_line}\n\n"
            "Interested in how this works in practice? Drop a comment or DM me — "
            "happy to walk through the architecture.\n\n"
            f"{HASHTAGS_LINKEDIN}"
        ),
    }


# ---------------------------------------------------------------------------
# Pipeline orchestration
# ---------------------------------------------------------------------------

def _ensure_output_dirs(logger: logging.Logger) -> None:
    for d in (OUTPUT_DIR, LOG_DIR):
        try:
            safe_path(d).mkdir(parents=True, exist_ok=True)
            logger.debug("Ensured directory: %s", d)
        except Exception as exc:
            logger.error("Could not create directory %s: %s", d, exc)
            raise


def _write_json(path: Path, data, logger: logging.Logger) -> None:
    target = safe_path(path)
    try:
        target.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
        logger.info("Wrote JSON → %s", target)
    except Exception as exc:
        logger.error("Failed to write JSON %s: %s", target, exc)
        raise


def _write_csv(path: Path, rows: list[dict], logger: logging.Logger) -> None:
    if not rows:
        logger.warning("No rows to write to CSV %s.", path)
        return
    target = safe_path(path)
    try:
        fieldnames = list(rows[0].keys())
        with target.open("w", newline="", encoding="utf-8") as fh:
            writer = csv.DictWriter(fh, fieldnames=fieldnames, extrasaction="ignore")
            writer.writeheader()
            writer.writerows(rows)
        logger.info("Wrote CSV (%d rows) → %s", len(rows), target)
    except Exception as exc:
        logger.error("Failed to write CSV %s: %s", target, exc)
        raise


def run_pipeline(dry_run: bool, logger: logging.Logger) -> dict:
    logger.info("=== PRINTMAXX Content Pipeline — PH GitAgent Launch START ===")
    skills_context = recall_skills_for_task("ph_ai_devtools_content_pipeline")
    logger.debug("Skills context: %s", skills_context)

    _ensure_output_dirs(logger)

    # 1. Fetch affiliate info
    logger.info("Step 1/4 — Fetching Lyzr affiliate info.")
    affiliate = fetch_affiliate_info(logger)

    # 2. Generate all content assets
    logger.info("Step 2/4 — Generating content assets.")
    tweet_thread = build_tweet_thread(affiliate)
    reddit_devtools = build_reddit_post_devtools(affiliate)
    reddit_ml = build_reddit_post_machinelearning(affiliate)
    linkedin = build_linkedin_post(affiliate)

    all_assets = tweet_thread + [reddit_devtools, reddit_ml, linkedin]

    # Stamp each asset
    run_ts = _ts()
    for asset in all_assets:
        asset["generated_at"] = run_ts
        asset["affiliate_program_found"] = affiliate["program_found"]

    # 3. Persist assets
    logger.info("Step 3/4 — Persisting content assets.")
    if dry_run:
        logger.info("[DRY-RUN] Skipping file writes. Asset preview:")
        for asset in all_assets[:2]:
            logger.info(
                "  [%s / %s] %s",
                asset.get("platform", "?"),
                asset.get("channel", "?"),
                (asset.get("body", asset.get("title", ""))[:80] + "..."),
            )
    else:
        _write_json(CONTENT_JSON, all_assets, logger)
        _write_csv(CONTENT_CSV, all_assets, logger)

    # 4. Update status
    status = {
        "last_run": run_ts,
        "dry_run": dry_run,
        "assets_generated": len(all_assets),
        "affiliate_program_found": affiliate["program_found"],
        "affiliate_cta": affiliate["cta"],
        "asset_breakdown": {
            "tweet_thread_tweets": len(tweet_thread),
            "reddit_posts": 2,
            "linkedin_posts": 1,
        },
        "output_json": str(CONTENT_JSON),
        "output_csv": str(CONTENT_CSV),
        "status": "ok",
    }

    if not dry_run:
        _write_json(STATUS_FILE, status, logger)

    capture_skill_from_result("ph_ai_devtools_content_pipeline", status)

    logger.info(
        "=== Pipeline complete — %d assets generated. dry_run=%s ===",
        len(all_assets),
        dry_run,
    )
    return status


def print_status(logger: logging.Logger) -> None:
    status_path = safe_path(STATUS_FILE)
    if not status_path.exists():
        logger.info("No status file found at %s — pipeline has not run yet.", status_path)
        print("No status file found. Run with --run first.")
        return
    try:
        data = json.loads(status_path.read_text(encoding="utf-8"))
        print(json.dumps(data, indent=2))
        logger.info("Status displayed from %s.", status_path)
    except Exception as exc:
        logger.error("Could not read status file: %s", exc)
        print(f"Error reading status: {exc}")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="ph_ai_devtools_content_pipeline",
        description=(
            "PRINTMAXX Automation — PH GitAgent/Lyzr launch content generator. "
            "Produces tweet threads, Reddit posts, and LinkedIn posts for dev audiences."
        ),
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--run",
        action="store_true",
        help="Run the full content generation pipeline.",
    )
    group.add_argument(
        "--status",
        action="store_true",
        help="Print the status of the last pipeline run.",
    )
    group.add_argument(
        "--dry-run",
        action="store_true",
        dest="dry_run",
        help="Simulate pipeline execution without writing output files.",
    )
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    dry_run = args.dry_run
    logger = _setup_logging(dry_run=dry_run)

    try:
        if args.run or dry_run:
            result = run_pipeline(dry_run=dry_run, logger=logger)
            print(json.dumps(result, indent=2))
        elif args.status:
            print_status(logger)
    except KeyboardInterrupt:
        logger.info("Interrupted by user.")
        sys.exit(0)
    except Exception as exc:
        logger.exception("Unhandled exception in pipeline: %s", exc)
        sys.exit(1)

    sys.exit(0)


if __name__ == "__main__":
    main()