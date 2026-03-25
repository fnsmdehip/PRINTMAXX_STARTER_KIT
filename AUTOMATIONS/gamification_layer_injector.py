#!/usr/bin/env python3
"""
gamification_layer_injector.py — PRINTMAXX Automation

Injects an RPG gamification layer into 7 non-religious streak apps in the
app factory. Adds XP system, four life areas (Body/Mind/Heart/Will), leveling
mechanics, and streak bonuses. Validated by first paying user on Habitum.

Usage:
    python gamification_layer_injector.py --status
    python gamification_layer_injector.py --dry-run
    python gamification_layer_injector.py --run
"""

import argparse
import csv
import json
import logging
import subprocess
import sys
import traceback
from datetime import datetime
from pathlib import Path

# ---------------------------------------------------------------------------
# Bootstrap: resolve PROJECT before importing _common so that the import
# works whether _common lives in AUTOMATIONS/ or the repo root.
# ---------------------------------------------------------------------------
PROJECT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))

try:
    from _common import (
        PROJECT as _COMMON_PROJECT,
        safe_path,
        recall_skills_for_task,
        capture_skill_from_result,
    )
    # Prefer the canonical PROJECT from _common if it exists
    PROJECT = _COMMON_PROJECT
except ImportError:
    # Fallback safe_path so the script can at least self-validate
    def safe_path(p: Path) -> Path:
        """Validate that *p* is inside PROJECT and return it."""
        resolved = Path(p).resolve()
        try:
            resolved.relative_to(PROJECT.resolve())
        except ValueError:
            raise ValueError(f"Path escapes PROJECT root: {resolved}")
        return resolved

    def recall_skills_for_task(task: str) -> list:
        return []

    def capture_skill_from_result(result: dict) -> None:
        pass

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------
LOG_DIR = safe_path(PROJECT / "AUTOMATIONS" / "logs")
LOG_DIR.mkdir(parents=True, exist_ok=True)
LOG_FILE = safe_path(LOG_DIR / "gamification_layer_injector.log")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE, mode="a"),
        logging.StreamHandler(sys.stdout),
    ],
)
log = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Constants — gamification design
# ---------------------------------------------------------------------------
LIFE_AREAS = ["Body", "Mind", "Heart", "Will"]

AREA_KEYWORDS: dict[str, list[str]] = {
    "Body":  ["fitness", "health", "sleep", "exercise", "nutrition", "workout", "steps"],
    "Mind":  ["learning", "reading", "study", "focus", "meditation", "productivity"],
    "Heart": ["journal", "gratitude", "social", "relationship", "kindness", "mood"],
    "Will":  ["discipline", "habit", "streak", "goal", "challenge", "consistency"],
}

XP_TABLE: dict[str, int] = {
    "streak_day":          10,   # base XP per day on a streak
    "streak_bonus_7":      25,   # bonus at 7-day milestone
    "streak_bonus_30":     100,
    "streak_bonus_90":     300,
    "streak_bonus_365":   1000,
    "perfect_week":        50,
    "area_level_up":      200,
    "all_areas_active":    30,   # daily bonus when all 4 areas have activity
}

LEVEL_THRESHOLDS: list[int] = [
    0, 100, 250, 500, 900, 1500, 2500, 4000, 6000, 9000, 13000,
]  # index = level (max level 10 shown; extend as needed)

# Template files that the injector writes / updates inside each app
GAMIFICATION_FILES = {
    "xp_config":      "config/gamification/xp_config.json",
    "level_config":   "config/gamification/level_config.json",
    "area_config":    "config/gamification/area_config.json",
    "streak_bonuses": "config/gamification/streak_bonuses.json",
    "manifest":       "config/gamification/manifest.json",
}

# ---------------------------------------------------------------------------
# App registry  (relative paths inside PROJECT)
# ---------------------------------------------------------------------------
APP_REGISTRY_PATH = safe_path(
    PROJECT / "AUTOMATIONS" / "data" / "app_registry.json"
)

FALLBACK_APPS: list[dict] = [
    {"id": "app_01", "name": "StreakForge",   "path": "apps/streak_forge",   "area_hints": ["Will", "Mind"]},
    {"id": "app_02", "name": "HabitPulse",    "path": "apps/habit_pulse",    "area_hints": ["Body", "Will"]},
    {"id": "app_03", "name": "DailyRise",     "path": "apps/daily_rise",     "area_hints": ["Mind", "Heart"]},
    {"id": "app_04", "name": "MomentumX",     "path": "apps/momentum_x",     "area_hints": ["Will", "Body"]},
    {"id": "app_05", "name": "ConsistencyPro","path": "apps/consistency_pro","area_hints": ["Mind", "Will"]},
    {"id": "app_06", "name": "FlowState",     "path": "apps/flow_state",     "area_hints": ["Heart", "Mind"]},
    {"id": "app_07", "name": "GritTracker",   "path": "apps/grit_tracker",   "area_hints": ["Body", "Will"]},
]


def load_app_registry() -> list[dict]:
    """Load app list from registry file; fall back to hard-coded list."""
    if APP_REGISTRY_PATH.exists():
        try:
            with open(APP_REGISTRY_PATH) as fh:
                apps = json.load(fh)
            log.info("Loaded %d apps from registry.", len(apps))
            return apps
        except Exception as exc:
            log.warning("Could not read registry (%s). Using fallback list.", exc)
    return FALLBACK_APPS


# ---------------------------------------------------------------------------
# Gamification config builders
# ---------------------------------------------------------------------------

def build_xp_config(app: dict) -> dict:
    return {
        "schema_version": "1.0",
        "app_id": app["id"],
        "xp_events": XP_TABLE,
        "generated_at": datetime.utcnow().isoformat() + "Z",
    }


def build_level_config(app: dict) -> dict:
    levels = []
    for lvl, threshold in enumerate(LEVEL_THRESHOLDS):
        next_threshold = LEVEL_THRESHOLDS[lvl + 1] if lvl + 1 < len(LEVEL_THRESHOLDS) else None
        levels.append({
            "level": lvl,
            "xp_required": threshold,
            "xp_for_next": next_threshold,
            "title": _level_title(lvl),
        })
    return {
        "schema_version": "1.0",
        "app_id": app["id"],
        "levels": levels,
        "generated_at": datetime.utcnow().isoformat() + "Z",
    }


def _level_title(lvl: int) -> str:
    titles = [
        "Novice", "Apprentice", "Adept", "Journeyman", "Veteran",
        "Expert", "Master", "Grandmaster", "Champion", "Legend", "Ascendant",
    ]
    return titles[lvl] if lvl < len(titles) else f"Level {lvl}"


def build_area_config(app: dict) -> dict:
    hints = set(app.get("area_hints", LIFE_AREAS))
    areas = []
    for area in LIFE_AREAS:
        areas.append({
            "id": area.lower(),
            "name": area,
            "keywords": AREA_KEYWORDS[area],
            "active": area in hints,
            "color": _area_color(area),
            "icon": _area_icon(area),
        })
    return {
        "schema_version": "1.0",
        "app_id": app["id"],
        "life_areas": areas,
        "bonus_all_areas_active_xp": XP_TABLE["all_areas_active"],
        "generated_at": datetime.utcnow().isoformat() + "Z",
    }


def _area_color(area: str) -> str:
    return {"Body": "#FF6B35", "Mind": "#4ECDC4", "Heart": "#FF6B9D", "Will": "#C77DFF"}.get(area, "#888888")


def _area_icon(area: str) -> str:
    return {"Body": "flame", "Mind": "brain", "Heart": "heart", "Will": "shield"}.get(area, "star")


def build_streak_bonuses(app: dict) -> dict:
    milestones = [
        {"days": 3,   "xp": 15,   "badge": "Hat Trick"},
        {"days": 7,   "xp": XP_TABLE["streak_bonus_7"],  "badge": "Week Warrior"},
        {"days": 14,  "xp": 50,   "badge": "Fortnight"},
        {"days": 21,  "xp": 75,   "badge": "Three Weeks"},
        {"days": 30,  "xp": XP_TABLE["streak_bonus_30"], "badge": "Monthly Master"},
        {"days": 60,  "xp": 200,  "badge": "Two Months"},
        {"days": 90,  "xp": XP_TABLE["streak_bonus_90"], "badge": "Quarter Champion"},
        {"days": 180, "xp": 500,  "badge": "Half Year Hero"},
        {"days": 365, "xp": XP_TABLE["streak_bonus_365"],"badge": "Year Ascendant"},
    ]
    return {
        "schema_version": "1.0",
        "app_id": app["id"],
        "base_xp_per_day": XP_TABLE["streak_day"],
        "milestones": milestones,
        "perfect_week_xp": XP_TABLE["perfect_week"],
        "generated_at": datetime.utcnow().isoformat() + "Z",
    }


def build_manifest(app: dict, files_written: list[str]) -> dict:
    return {
        "schema_version": "1.0",
        "app_id": app["id"],
        "app_name": app["name"],
        "gamification_enabled": True,
        "life_areas": LIFE_AREAS,
        "files": files_written,
        "injected_at": datetime.utcnow().isoformat() + "Z",
        "injector_version": "1.0.0",
    }


# ---------------------------------------------------------------------------
# Core injection logic
# ---------------------------------------------------------------------------

def inject_app(app: dict, dry_run: bool = False) -> dict:
    """
    Write all gamification config files for *app*.
    Returns a result dict with keys: app_id, success, files_written, error.
    """
    app_path = PROJECT / app["path"]
    files_written: list[str] = []
    result = {"app_id": app["id"], "app_name": app["name"], "success": False,
              "files_written": [], "error": None}

    builders = {
        "xp_config":      build_xp_config,
        "level_config":   build_level_config,
        "area_config":    build_area_config,
        "streak_bonuses": build_streak_bonuses,
    }

    try:
        for key, rel_path in GAMIFICATION_FILES.items():
            if key == "manifest":
                continue  # written last
            target = safe_path(app_path / rel_path)
            payload = builders[key](app)
            if dry_run:
                log.info("[DRY-RUN] Would write %s", target)
            else:
                target.parent.mkdir(parents=True, exist_ok=True)
                with open(target, "w") as fh:
                    json.dump(payload, fh, indent=2)
                log.info("Wrote %s", target.relative_to(PROJECT))
            files_written.append(str(target.relative_to(PROJECT)))

        # manifest references the other files
        manifest_path = safe_path(app_path / GAMIFICATION_FILES["manifest"])
        manifest_payload = build_manifest(app, files_written)
        if dry_run:
            log.info("[DRY-RUN] Would write %s", manifest_path)
        else:
            manifest_path.parent.mkdir(parents=True, exist_ok=True)
            with open(manifest_path, "w") as fh:
                json.dump(manifest_payload, fh, indent=2)
            log.info("Wrote manifest %s", manifest_path.relative_to(PROJECT))
        files_written.append(str(manifest_path.relative_to(PROJECT)))

        result["success"] = True
        result["files_written"] = files_written

    except Exception as exc:
        result["error"] = traceback.format_exc()
        log.error("Failed to inject %s: %s", app["id"], exc)

    return result


def run_all(apps: list[dict], dry_run: bool = False) -> list[dict]:
    results = []
    for app in apps:
        log.info("==> Injecting gamification into %s (%s)", app["name"], app["id"])
        result = inject_app(app, dry_run=dry_run)
        results.append(result)
        capture_skill_from_result(result)
    return results


# ---------------------------------------------------------------------------
# Status check
# ---------------------------------------------------------------------------

def check_status(apps: list[dict]) -> None:
    log.info("--- Gamification Injection Status ---")
    for app in apps:
        app_path = PROJECT / app["path"]
        manifest = app_path / GAMIFICATION_FILES["manifest"]
        if manifest.exists():
            try:
                with open(manifest) as fh:
                    data = json.load(fh)
                log.info(
                    "[OK] %-20s  injected_at=%s  files=%d",
                    app["name"],
                    data.get("injected_at", "?"),
                    len(data.get("files", [])),
                )
            except Exception as exc:
                log.warning("[CORRUPT] %-20s  error=%s", app["name"], exc)
        else:
            log.info("[MISSING] %-20s  manifest not found", app["name"])


# ---------------------------------------------------------------------------
# Results report
# ---------------------------------------------------------------------------

def write_report(results: list[dict], dry_run: bool) -> None:
    report_dir = safe_path(PROJECT / "AUTOMATIONS" / "reports")
    report_dir.mkdir(parents=True, exist_ok=True)
    ts = datetime.utcnow().strftime("%Y%m%dT%H%M%S")
    prefix = "dry_run_" if dry_run else ""
    report_path = safe_path(report_dir / f"{prefix}gamification_injection_{ts}.csv")

    fieldnames = ["app_id", "app_name", "success", "files_written_count", "error"]
    try:
        with open(report_path, "w", newline="") as fh:
            writer = csv.DictWriter(fh, fieldnames=fieldnames)
            writer.writeheader()
            for r in results:
                writer.writerow({
                    "app_id": r["app_id"],
                    "app_name": r["app_name"],
                    "success": r["success"],
                    "files_written_count": len(r.get("files_written", [])),
                    "error": (r.get("error") or "").replace("\n", " ")[:200],
                })
        log.info("Report written to %s", report_path.relative_to(PROJECT))
    except Exception as exc:
        log.error("Could not write report: %s", exc)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Inject RPG gamification layer into streak app factory.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--run",     action="store_true", help="Inject gamification configs into all apps.")
    group.add_argument("--status",  action="store_true", help="Show injection status for each app.")
    group.add_argument("--dry-run", action="store_true", dest="dry_run",
                       help="Simulate injection without writing files.")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    log.info("gamification_layer_injector started — mode=%s",
             "run" if args.run else ("dry_run" if args.dry_run else "status"))

    try:
        recall_skills_for_task("inject_gamification_layer")
    except Exception:
        pass  # non-fatal

    try:
        apps = load_app_registry()

        if args.status:
            check_status(apps)
            return 0

        # --run or --dry-run
        results = run_all(apps, dry_run=args.dry_run)
        write_report(results, dry_run=args.dry_run)

        successes = sum(1 for r in results if r["success"])
        failures  = len(results) - successes
        log.info("Done. %d succeeded, %d failed.", successes, failures)
        return 0 if failures == 0 else 1

    except Exception as exc:
        log.error("Fatal error: %s", exc)
        log.debug(traceback.format_exc())
        return 2


if __name__ == "__main__":
    sys.exit(main())