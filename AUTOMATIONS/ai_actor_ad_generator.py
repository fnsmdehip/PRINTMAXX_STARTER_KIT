#!/usr/bin/env python3
"""
PRINTMAXX Automation System — AI Actor Ad Generator

Scrapes AdsTurbo / similar AI-actor ad platforms for available free-tier
slots, auto-generates video ad creatives for 47+ live apps, and routes
completed job descriptors to the content_factory posting queue for
TikTok / Instagram paid and organic distribution.

Usage:
    python ai_actor_ad_generator.py --run
    python ai_actor_ad_generator.py --status
    python ai_actor_ad_generator.py --dry-run
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
# Bootstrap — prefer shared helpers, fall back to local definitions
# ---------------------------------------------------------------------------
try:
    from _common import (  # type: ignore[import]
        PROJECT,
        safe_path,
        recall_skills_for_task,
        capture_skill_from_result,
    )
except ImportError:
    PROJECT = Path(__file__).resolve().parent.parent

    def safe_path(path) -> Path:
        """Resolve *path* and assert it lives inside PROJECT."""
        resolved = Path(path).resolve()
        if not str(resolved).startswith(str(PROJECT.resolve())):
            raise ValueError(f"Path escapes project root: {path}")
        resolved.parent.mkdir(parents=True, exist_ok=True)
        return resolved

    def recall_skills_for_task(task: str) -> list:  # type: ignore[misc]
        return []

    def capture_skill_from_result(task: str, result: dict) -> None:  # type: ignore[misc]
        pass

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
AUTOMATIONS_DIR = PROJECT / "AUTOMATIONS"
LOG_FILE = AUTOMATIONS_DIR / "logs" / "ai_actor_ad_generator.log"
APPS_CATALOG = AUTOMATIONS_DIR / "data" / "apps_catalog.json"
PLATFORM_CACHE = AUTOMATIONS_DIR / "cache" / "ad_platforms.json"
CREATIVE_QUEUE = AUTOMATIONS_DIR / "queues" / "ad_creatives_pending.json"
CONTENT_FACTORY_QUEUE = PROJECT / "content_factory" / "queue" / "incoming.json"
STATE_FILE = AUTOMATIONS_DIR / "state" / "ai_actor_ad_generator_state.json"

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------
def _setup_logging() -> logging.Logger:
    log_path = safe_path(LOG_FILE)
    handler = logging.FileHandler(log_path, mode="a", encoding="utf-8")
    handler.setFormatter(
        logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
    )
    logger = logging.getLogger("ai_actor_ad_generator")
    logger.setLevel(logging.INFO)
    if not logger.handlers:
        logger.addHandler(handler)
        logger.addHandler(logging.StreamHandler(sys.stdout))
    return logger


LOG = _setup_logging()

# ---------------------------------------------------------------------------
# Ad-platform definitions
# ---------------------------------------------------------------------------
AD_PLATFORMS = [
    {
        "name": "AdsTurbo",
        "url": "https://adsturbo.com",
        "api_base": "https://api.adsturbo.com/v1",
        "free_tier_endpoint": "/plans/free",
        "generate_endpoint": "/ads/generate",
        "auth_env_var": "ADSTURBO_API_KEY",
    },
    {
        "name": "HeyGen",
        "url": "https://heygen.com",
        "api_base": "https://api.heygen.com/v1",
        "free_tier_endpoint": "/user/remaining_quota",
        "generate_endpoint": "/video.generate",
        "auth_env_var": "HEYGEN_API_KEY",
    },
    {
        "name": "Creatify",
        "url": "https://creatify.ai",
        "api_base": "https://api.creatify.ai/api",
        "free_tier_endpoint": "/credits/",
        "generate_endpoint": "/ai_ads/",
        "auth_env_var": "CREATIFY_API_KEY",
    },
]

# Distribution channels routed to content_factory
DISTRIBUTION_CHANNELS = [
    {"platform": "tiktok", "mode": "organic"},
    {"platform": "tiktok", "mode": "paid"},
    {"platform": "instagram_reels", "mode": "organic"},
    {"platform": "instagram_reels", "mode": "paid"},
]

# ---------------------------------------------------------------------------
# Utilities
# ---------------------------------------------------------------------------
def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _load_json(path: Path) -> dict | list:
    p = Path(path)
    if not p.exists():
        return {}
    with open(p, "r", encoding="utf-8") as fh:
        return json.load(fh)


def _write_json(path: Path, data) -> None:
    p = safe_path(path)
    with open(p, "w", encoding="utf-8") as fh:
        json.dump(data, fh, indent=2)


def _read_env_key(var: str) -> str | None:
    """Pull an API key from the environment via a subprocess env dump (no os module)."""
    try:
        result = subprocess.run(
            ["printenv", var],
            capture_output=True,
            text=True,
            timeout=5,
        )
        value = result.stdout.strip()
        return value if value else None
    except Exception:
        return None


def _http_get(url: str, headers: dict | None = None, timeout: int = 20) -> dict | None:
    req = urllib.request.Request(url, headers=headers or {})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            body = resp.read().decode("utf-8")
            return json.loads(body)
    except urllib.error.HTTPError as exc:
        LOG.warning("HTTP %s for %s: %s", exc.code, url, exc.reason)
        return None
    except urllib.error.URLError as exc:
        LOG.warning("URL error for %s: %s", url, exc.reason)
        return None
    except json.JSONDecodeError:
        LOG.warning("Non-JSON response from %s", url)
        return None


def _http_post(url: str, payload: dict, headers: dict | None = None, timeout: int = 60) -> dict | None:
    body = json.dumps(payload).encode("utf-8")
    hdrs = {"Content-Type": "application/json"}
    if headers:
        hdrs.update(headers)
    req = urllib.request.Request(url, data=body, headers=hdrs, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        LOG.warning("HTTP %s for POST %s: %s", exc.code, url, exc.reason)
        return None
    except urllib.error.URLError as exc:
        LOG.warning("URL error for POST %s: %s", url, exc.reason)
        return None
    except json.JSONDecodeError:
        LOG.warning("Non-JSON POST response from %s", url)
        return None

# ---------------------------------------------------------------------------
# Step 1 — Discover free-tier capacity across platforms
# ---------------------------------------------------------------------------
def scrape_platform_free_tiers(dry_run: bool = False) -> list[dict]:
    """
    Query each configured ad platform for its free-tier / remaining credit
    status. Returns a list of platform dicts annotated with 'available_credits'
    and 'can_generate' booleans.
    """
    LOG.info("Scanning %d AI-actor ad platforms for free-tier availability…", len(AD_PLATFORMS))
    results = []

    for platform in AD_PLATFORMS:
        name = platform["name"]
        api_key = _read_env_key(platform["auth_env_var"])
        entry = {**platform, "api_key_present": bool(api_key), "available_credits": 0, "can_generate": False}

        if dry_run:
            LOG.info("[DRY-RUN] Would probe %s free tier", name)
            entry["can_generate"] = True
            entry["available_credits"] = 99
            results.append(entry)
            continue

        if not api_key:
            LOG.warning("No API key for %s (%s) — skipping", name, platform["auth_env_var"])
            results.append(entry)
            continue

        url = platform["api_base"] + platform["free_tier_endpoint"]
        headers = {"Authorization": f"Bearer {api_key}"}
        data = _http_get(url, headers=headers)

        if data is None:
            LOG.warning("Could not reach free-tier endpoint for %s", name)
            results.append(entry)
            continue

        # Normalise credit keys across platforms
        credits = (
            data.get("remaining_credits")
            or data.get("credits")
            or data.get("quota_remaining")
            or data.get("free_generations")
            or 0
        )
        try:
            credits = int(credits)
        except (TypeError, ValueError):
            credits = 0

        entry["available_credits"] = credits
        entry["can_generate"] = credits > 0
        entry["raw_response"] = data
        LOG.info("%s — available credits: %d", name, credits)
        results.append(entry)

    if not dry_run:
        _write_json(PLATFORM_CACHE, {"fetched_at": _now_iso(), "platforms": results})

    return results


# ---------------------------------------------------------------------------
# Step 2 — Load the 47+ live-app catalog
# ---------------------------------------------------------------------------
def load_apps_catalog() -> list[dict]:
    """
    Load app metadata from AUTOMATIONS/data/apps_catalog.json.
    Falls back to a minimal stub so the workflow can always run.
    """
    catalog_path = safe_path(APPS_CATALOG)

    if catalog_path.exists():
        try:
            apps = json.loads(catalog_path.read_text(encoding="utf-8"))
            LOG.info("Loaded %d apps from catalog", len(apps))
            return apps
        except json.JSONDecodeError as exc:
            LOG.error("Malformed apps catalog: %s", exc)

    # Stub — write a seed catalog on first run
    LOG.warning("apps_catalog.json not found — writing seed catalog")
    stub = [
        {
            "app_id": f"app_{i:03d}",
            "name": f"PRINTMAXX App {i}",
            "category": "productivity",
            "store_url": "",
            "tagline": "Print smarter, not harder.",
            "cta": "Download free",
            "target_audience": "small business owners",
            "platforms": ["tiktok", "instagram_reels"],
        }
        for i in range(1, 48)
    ]
    _write_json(catalog_path, stub)
    return stub


# ---------------------------------------------------------------------------
# Step 3 — Generate ad-creative job descriptors
# ---------------------------------------------------------------------------
def build_creative_jobs(apps: list[dict], available_platforms: list[dict], dry_run: bool = False) -> list[dict]:
    """
    Pair each app with a capable platform and build job descriptors.
    Jobs are written to the creative pending queue.
    """
    capable = [p for p in available_platforms if p["can_generate"]]
    if not capable:
        LOG.warning("No platforms have available credits — no jobs created")
        return []

    jobs = []
    for idx, app in enumerate(apps):
        platform = capable[idx % len(capable)]  # round-robin
        job = {
            "job_id": f"job_{_now_iso().replace(':', '-').replace('.', '-')}_{idx:04d}",
            "created_at": _now_iso(),
            "status": "pending",
            "dry_run": dry_run,
            "app": app,
            "platform": platform["name"],
            "api_base": platform["api_base"],
            "generate_endpoint": platform["generate_endpoint"],
            "auth_env_var": platform["auth_env_var"],
            "creative_spec": {
                "actor_style": "casual_human",
                "duration_seconds": 30,
                "aspect_ratio": "9:16",
                "script": (
                    f"Hey! Discover {app['name']} — {app.get('tagline', '')} "
                    f"{app.get('cta', 'Download now')}!"
                ),
                "voice": "natural_en_us",
                "caption": True,
            },
            "distribution_channels": DISTRIBUTION_CHANNELS,
        }
        jobs.append(job)

    LOG.info("Built %d creative jobs across %d capable platforms", len(jobs), len(capable))
    _write_json(safe_path(CREATIVE_QUEUE), {"updated_at": _now_iso(), "jobs": jobs})
    return jobs


# ---------------------------------------------------------------------------
# Step 4 — Submit generation requests
# ---------------------------------------------------------------------------
def submit_generation_jobs(jobs: list[dict], dry_run: bool = False) -> list[dict]:
    """
    For each pending job, POST to the platform API to kick off generation.
    Updates job status in-place and returns the updated list.
    """
    for job in jobs:
        if dry_run:
            LOG.info("[DRY-RUN] Would submit job %s to %s", job["job_id"], job["platform"])
            job["status"] = "submitted_dry_run"
            job["platform_job_id"] = f"dry_{job['job_id']}"
            continue

        api_key = _read_env_key(job["auth_env_var"])
        if not api_key:
            LOG.warning("Skipping job %s — no API key", job["job_id"])
            job["status"] = "skipped_no_key"
            continue

        url = job["api_base"] + job["generate_endpoint"]
        headers = {"Authorization": f"Bearer {api_key}"}
        payload = {
            "app_id": job["app"]["app_id"],
            "creative_spec": job["creative_spec"],
            "webhook_url": "",  # populate if webhook endpoint is configured
        }

        LOG.info("Submitting job %s → %s", job["job_id"], job["platform"])
        response = _http_post(url, payload, headers=headers)

        if response:
            job["status"] = "submitted"
            job["platform_job_id"] = response.get("job_id") or response.get("id") or ""
            job["platform_response"] = response
            LOG.info("Submitted %s — platform job id: %s", job["job_id"], job["platform_job_id"])
        else:
            job["status"] = "submission_failed"
            LOG.error("Submission failed for job %s", job["job_id"])

    # Persist updated queue
    _write_json(safe_path(CREATIVE_QUEUE), {"updated_at": _now_iso(), "jobs": jobs})
    return jobs


# ---------------------------------------------------------------------------
# Step 5 — Route completed / submitted jobs to content_factory queue
# ---------------------------------------------------------------------------
def route_to_content_factory(jobs: list[dict], dry_run: bool = False) -> int:
    """
    Append submitted jobs to content_factory/queue/incoming.json.
    Returns the count of entries enqueued.
    """
    routable = [j for j in jobs if j["status"] in ("submitted", "submitted_dry_run")]
    if not routable:
        LOG.info("No routable jobs at this time")
        return 0

    queue_path = safe_path(CONTENT_FACTORY_QUEUE)
    existing: list = []
    if queue_path.exists():
        try:
            existing = json.loads(queue_path.read_text(encoding="utf-8"))
            if not isinstance(existing, list):
                existing = []
        except json.JSONDecodeError:
            existing = []

    new_entries = []
    for job in routable:
        for channel in job["distribution_channels"]:
            entry = {
                "source": "ai_actor_ad_generator",
                "enqueued_at": _now_iso(),
                "dry_run": dry_run,
                "job_id": job["job_id"],
                "platform_job_id": job.get("platform_job_id", ""),
                "ad_platform": job["platform"],
                "app_id": job["app"]["app_id"],
                "app_name": job["app"]["name"],
                "distribution_platform": channel["platform"],
                "distribution_mode": channel["mode"],
                "creative_spec": job["creative_spec"],
                "status": "queued",
            }
            new_entries.append(entry)

    combined = existing + new_entries
    if not dry_run:
        _write_json(queue_path, combined)
    LOG.info(
        "%sRouted %d distribution entries to content_factory queue",
        "[DRY-RUN] Would have " if dry_run else "",
        len(new_entries),
    )
    return len(new_entries)


# ---------------------------------------------------------------------------
# State helpers
# ---------------------------------------------------------------------------
def _load_state() -> dict:
    p = safe_path(STATE_FILE)
    if p.exists():
        try:
            return json.loads(p.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            pass
    return {}


def _save_state(state: dict) -> None:
    _write_json(safe_path(STATE_FILE), state)


# ---------------------------------------------------------------------------
# CSV reporting
# ---------------------------------------------------------------------------
def _write_run_report(jobs: list[dict], enqueued: int) -> None:
    report_path = safe_path(
        AUTOMATIONS_DIR / "reports" / f"ad_gen_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    )
    fieldnames = ["job_id", "app_id", "app_name", "platform", "status", "platform_job_id", "created_at"]
    with open(report_path, "w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for job in jobs:
            writer.writerow({
                "job_id": job["job_id"],
                "app_id": job["app"]["app_id"],
                "app_name": job["app"]["name"],
                "platform": job["platform"],
                "status": job["status"],
                "platform_job_id": job.get("platform_job_id", ""),
                "created_at": job["created_at"],
            })
    LOG.info("Run report written: %s", report_path)


# ---------------------------------------------------------------------------
# Workflow entry points
# ---------------------------------------------------------------------------
def run_workflow(dry_run: bool = False) -> None:
    LOG.info("=== AI Actor Ad Generator — %sRUN START ===", "DRY-" if dry_run else "")
    skills = recall_skills_for_task("ai_actor_ad_generation")
    if skills:
        LOG.info("Recalled %d skills for task", len(skills))

    try:
        platforms = scrape_platform_free_tiers(dry_run=dry_run)
        apps = load_apps_catalog()
        jobs = build_creative_jobs(apps, platforms, dry_run=dry_run)

        if not jobs:
            LOG.warning("No jobs to process — exiting cleanly")
            _save_state({"last_run": _now_iso(), "jobs_created": 0, "enqueued": 0})
            return

        jobs = submit_generation_jobs(jobs, dry_run=dry_run)
        enqueued = route_to_content_factory(jobs, dry_run=dry_run)
        _write_run_report(jobs, enqueued)

        state = {
            "last_run": _now_iso(),
            "dry_run": dry_run,
            "apps_processed": len(apps),
            "jobs_created": len(jobs),
            "jobs_submitted": sum(1 for j in jobs if "submitted" in j["status"]),
            "jobs_failed": sum(1 for j in jobs if j["status"] == "submission_failed"),
            "enqueued_for_distribution": enqueued,
        }
        _save_state(state)

        capture_skill_from_result("ai_actor_ad_generation", state)

        LOG.info(
            "Run complete — apps: %d | jobs submitted: %d | distribution entries: %d",
            len(apps),
            state["jobs_submitted"],
            enqueued,
        )

    except Exception as exc:
        LOG.exception("Unhandled error during workflow run: %s", exc)
        sys.exit(1)

    LOG.info("=== AI Actor Ad Generator — RUN END ===")


def show_status() -> None:
    state = _load_state()
    if not state:
        print("No previous run found.")
        return

    print("\n--- AI Actor Ad Generator — Status ---")
    for key, value in state.items():
        print(f"  {key}: {value}")

    queue_path = Path(CONTENT_FACTORY_QUEUE)
    if queue_path.exists():
        try:
            queue = json.loads(queue_path.read_text(encoding="utf-8"))
            queued = sum(1 for e in queue if e.get("source") == "ai_actor_ad_generator")
            print(f"  content_factory_queue_entries: {queued}")
        except (json.JSONDecodeError, TypeError):
            print("  content_factory_queue_entries: (unreadable)")

    platform_cache = Path(PLATFORM_CACHE)
    if platform_cache.exists():
        try:
            cache = json.loads(platform_cache.read_text(encoding="utf-8"))
            print(f"  platform_cache_fetched_at: {cache.get('fetched_at', 'unknown')}")
            for p in cache.get("platforms", []):
                print(f"    {p['name']}: credits={p['available_credits']} can_generate={p['can_generate']}")
        except (json.JSONDecodeError, TypeError):
            pass

    print()


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="ai_actor_ad_generator",
        description="PRINTMAXX — AI Actor Ad Generator for 47+ live apps",
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--run",
        action="store_true",
        help="Execute the full ad-generation and distribution-routing workflow",
    )
    group.add_argument(
        "--status",
        action="store_true",
        help="Print status of the last run and current queue depth",
    )
    group.add_argument(
        "--dry-run",
        action="store_true",
        dest="dry_run",
        help="Simulate the workflow without making API calls or writing to the content_factory queue",
    )
    return parser


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main() -> None:
    parser = _build_parser()
    args = parser.parse_args()

    if args.status:
        show_status()
    elif args.dry_run:
        run_workflow(dry_run=True)
    elif args.run:
        run_workflow(dry_run=False)


if __name__ == "__main__":
    main()