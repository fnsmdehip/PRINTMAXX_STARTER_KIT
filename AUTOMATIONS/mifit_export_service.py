#!/usr/bin/env python3
"""
PRINTMAXX Automation System — Mi Fit & Zepp Workout Exporter Service

Wraps rolandsz/Mi-Fit-and-Zepp-workout-exporter as a micro-SaaS:
  - Accepts user credentials via built-in web form (--serve mode)
  - Runs the exporter on-demand (--run) or via cron
  - Outputs GPX / TCX / CSV files for download
  - Optionally auto-syncs workouts to Strava or Google Fit

Target users: Xiaomi Mi Band and Amazfit owners wanting data portability.

Usage:
    python3 mifit_export_service.py --run
    python3 mifit_export_service.py --run --user alice
    python3 mifit_export_service.py --status
    python3 mifit_export_service.py --dry-run
    python3 mifit_export_service.py --serve [--host 0.0.0.0 --port 8080]

Cron example (daily at 06:00):
    0 6 * * * /usr/bin/python3 /path/to/mifit_export_service.py --run
"""

from __future__ import annotations

import argparse
import csv
import json
import logging
import os
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

# ---------------------------------------------------------------------------
# Bootstrap: try _common, fall back to local definitions
# ---------------------------------------------------------------------------
try:
    from _common import (  # type: ignore[import]
        PROJECT,
        safe_path,
        recall_skills_for_task,
        capture_skill_from_result,
    )
except ImportError:
    PROJECT: Path = Path(__file__).resolve().parent.parent

    def safe_path(path: "Path | str", must_exist: bool = False) -> Path:
        """Return resolved Path only if it lives inside PROJECT.

        Raises ValueError on path-escape attempts, FileNotFoundError when
        *must_exist* is True and the target does not exist.
        """
        resolved = Path(path).resolve()
        try:
            resolved.relative_to(PROJECT)
        except ValueError as exc:
            raise ValueError(
                f"Path escape blocked: {path!r} resolves outside PROJECT ({PROJECT})"
            ) from exc
        if must_exist and not resolved.exists():
            raise FileNotFoundError(f"Required path not found: {resolved}")
        return resolved

    def recall_skills_for_task(task_description: str) -> list:  # noqa: D401
        """No-op stub used when _common is absent."""
        return []

    def capture_skill_from_result(result: object, task_description: str) -> None:
        """No-op stub used when _common is absent."""

# ---------------------------------------------------------------------------
# Directory / file layout
# ---------------------------------------------------------------------------
AUTOMATIONS_DIR = safe_path(PROJECT / "AUTOMATIONS")
LOGS_DIR        = safe_path(AUTOMATIONS_DIR / "logs")
DATA_DIR        = safe_path(AUTOMATIONS_DIR / "data" / "mifit_exports")
EXPORTER_DIR    = safe_path(AUTOMATIONS_DIR / "vendor" / "Mi-Fit-and-Zepp-workout-exporter")
CONFIG_FILE     = safe_path(AUTOMATIONS_DIR / "config" / "mifit_users.json")
STATUS_FILE     = safe_path(AUTOMATIONS_DIR / "status" / "mifit_export_service.json")
LOG_FILE        = safe_path(LOGS_DIR / "mifit_export_service.log")

EXPORTER_SCRIPT = EXPORTER_DIR / "export_workouts.py"

# ---------------------------------------------------------------------------
# Logging  (append mode as required)
# ---------------------------------------------------------------------------

def _setup_logging() -> logging.Logger:
    LOGS_DIR.mkdir(parents=True, exist_ok=True)
    logger = logging.getLogger("mifit_export_service")
    logger.setLevel(logging.DEBUG)
    if not logger.handlers:
        fmt = logging.Formatter(
            "%(asctime)s  %(levelname)-8s  %(name)s  %(message)s",
            datefmt="%Y-%m-%dT%H:%M:%S",
        )
        fh = logging.FileHandler(str(LOG_FILE), mode="a", encoding="utf-8")
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(fmt)
        logger.addHandler(fh)
        ch = logging.StreamHandler(sys.stdout)
        ch.setLevel(logging.INFO)
        ch.setFormatter(fmt)
        logger.addHandler(ch)
    return logger


log = _setup_logging()

# ---------------------------------------------------------------------------
# Config helpers
# ---------------------------------------------------------------------------
DEFAULT_CONFIG: dict = {
    "users": {},
    "strava": {"client_id": "", "client_secret": ""},
    "google_fit": {"client_id": "", "client_secret": ""},
    "web": {"host": "127.0.0.1", "port": 8080},
    "exporter": {
        "repo_url": "https://github.com/rolandsz/Mi-Fit-and-Zepp-workout-exporter",
        "python_bin": sys.executable,
        "formats": ["gpx", "tcx", "csv"],
    },
}


def _ensure_dirs() -> None:
    """Create all required directories under PROJECT."""
    for d in (LOGS_DIR, DATA_DIR, CONFIG_FILE.parent, STATUS_FILE.parent, EXPORTER_DIR):
        safe_path(d).mkdir(parents=True, exist_ok=True)


def load_config() -> dict:
    """Load config from disk, merging missing top-level keys with defaults."""
    _ensure_dirs()
    if not CONFIG_FILE.exists():
        save_config(DEFAULT_CONFIG)
        return dict(DEFAULT_CONFIG)
    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as fh:
            on_disk = json.load(fh)
        return {**DEFAULT_CONFIG, **on_disk}
    except (json.JSONDecodeError, OSError) as exc:
        log.error("Cannot load config %s: %s", CONFIG_FILE, exc)
        return dict(DEFAULT_CONFIG)


def save_config(config: dict) -> None:
    """Persist config atomically via safe_path."""
    target = safe_path(CONFIG_FILE)
    target.parent.mkdir(parents=True, exist_ok=True)
    tmp = safe_path(target.with_suffix(".tmp"))
    try:
        with open(tmp, "w", encoding="utf-8") as fh:
            json.dump(config, fh, indent=2)
        tmp.replace(target)
    except OSError as exc:
        log.error("Failed to save config: %s", exc)
        raise


def load_status() -> dict:
    """Return the last-run status dict, or empty dict on any error."""
    if not STATUS_FILE.exists():
        return {}
    try:
        with open(STATUS_FILE, "r", encoding="utf-8") as fh:
            return json.load(fh)
    except (json.JSONDecodeError, OSError):
        return {}


def save_status(status: dict) -> None:
    """Persist status atomically via safe_path."""
    target = safe_path(STATUS_FILE)
    target.parent.mkdir(parents=True, exist_ok=True)
    tmp = safe_path(target.with_suffix(".tmp"))
    try:
        with open(tmp, "w", encoding="utf-8") as fh:
            json.dump(status, fh, indent=2, default=str)
        tmp.replace(target)
    except OSError as exc:
        log.error("Failed to save status: %s", exc)


# ---------------------------------------------------------------------------
# Exporter bootstrap
# ---------------------------------------------------------------------------

def ensure_exporter(dry_run: bool = False) -> bool:
    """Clone the upstream exporter repo if it is not already present."""
    if EXPORTER_DIR.exists() and EXPORTER_SCRIPT.exists():
        log.debug("Exporter already present at %s", EXPORTER_DIR)
        return True
    log.info("Cloning Mi-Fit-and-Zepp-workout-exporter ...")
    if dry_run:
        log.info("[dry-run] Would clone exporter repo into %s", EXPORTER_DIR)
        return True
    try:
        safe_path(EXPORTER_DIR.parent).mkdir(parents=True, exist_ok=True)
        result = subprocess.run(
            [
                "git", "clone", "--depth", "1",
                "https://github.com/rolandsz/Mi-Fit-and-Zepp-workout-exporter",
                str(EXPORTER_DIR),
            ],
            capture_output=True,
            text=True,
            timeout=120,
        )
        if result.returncode != 0:
            log.error("git clone failed: %s", result.stderr.strip())
            return False
        log.info("Exporter cloned successfully")
        return True
    except (subprocess.TimeoutExpired, FileNotFoundError, OSError) as exc:
        log.error("Failed to clone exporter: %s", exc)
        return False


# ---------------------------------------------------------------------------
# Export logic
# ---------------------------------------------------------------------------

def _user_output_dir(user_id: str) -> Path:
    out = safe_path(DATA_DIR / user_id)
    out.mkdir(parents=True, exist_ok=True)
    return out


def _write_manifest_csv(path: Path, user_id: str, files: list, timestamp: str) -> None:
    """Write a CSV manifest of exported files via safe_path."""
    safe = safe_path(path)
    try:
        with open(safe, "w", newline="", encoding="utf-8") as fh:
            writer = csv.writer(fh)
            writer.writerow(["timestamp", "user_id", "filename", "size_bytes"])
            for f in files:
                fp = Path(f)
                size = fp.stat().st_size if fp.exists() else 0
                writer.writerow([timestamp, user_id, fp.name, size])
        log.debug("Manifest written: %s", safe)
    except OSError as exc:
        log.warning("Could not write manifest: %s", exc)


def run_exporter_for_user(
    user_id: str,
    user_cfg: dict,
    formats: list,
    dry_run: bool = False,
) -> dict:
    """
    Invoke the upstream exporter for a single user.

    Returns a result dict: success (bool), files (list[str]),
    manifest (str), error (str|None), run_dir (str), timestamp (str).
    """
    email    = user_cfg.get("email", "")
    password = user_cfg.get("password", "")
    if not email or not password:
        return {"success": False, "files": [], "error": "Missing credentials"}

    out_dir   = _user_output_dir(user_id)
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    run_dir   = safe_path(out_dir / timestamp)

    if dry_run:
        log.info(
            "[dry-run] Would export %s for user %r -> %s",
            formats, user_id, run_dir,
        )
        return {"success": True, "files": [], "dry_run": True, "timestamp": timestamp}

    run_dir.mkdir(parents=True, exist_ok=True)

    produced_files: list = []
    errors: list = []

    for fmt in formats:
        log.info("Exporting %s for user %r ...", fmt.upper(), user_id)
        try:
            cmd = [
                sys.executable,
                str(EXPORTER_SCRIPT),
                "--email",    email,
                "--password", password,
                "--format",   fmt,
                "--output",   str(run_dir),
            ]
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=300,
                cwd=str(EXPORTER_DIR),
            )
            if result.returncode == 0:
                log.info("Export %s complete for %r", fmt.upper(), user_id)
                for f in run_dir.iterdir():
                    if f.suffix.lstrip(".").lower() == fmt.lower():
                        produced_files.append(safe_path(f))
            else:
                err_msg = (result.stderr.strip() or result.stdout.strip())[:400]
                log.error("Export %s failed for %r: %s", fmt.upper(), user_id, err_msg)
                errors.append(f"{fmt}: {err_msg}")
        except subprocess.TimeoutExpired:
            log.error("Export %s timed out for user %r", fmt.upper(), user_id)
            errors.append(f"{fmt}: timeout after 300 s")
        except (OSError, subprocess.SubprocessError) as exc:
            log.error("Subprocess error (%s, user=%r): %s", fmt, user_id, exc)
            errors.append(f"{fmt}: {exc}")

    manifest_path = safe_path(run_dir / "manifest.csv")
    _write_manifest_csv(manifest_path, user_id, produced_files, timestamp)

    return {
        "success":   len(errors) == 0,
        "files":     [str(f) for f in produced_files],
        "manifest":  str(manifest_path),
        "error":     "; ".join(errors) if errors else None,
        "run_dir":   str(run_dir),
        "timestamp": timestamp,
    }


# ---------------------------------------------------------------------------
# Strava sync
# ---------------------------------------------------------------------------
_STRAVA_UPLOAD_URL = "https://www.strava.com/api/v3/uploads"
_STRAVA_TOKEN_URL  = "https://www.strava.com/oauth/token"


def _strava_refresh_token(config: dict, user_id: str) -> "str | None":
    """Return a valid Strava access token, refreshing via OAuth2 if needed."""
    user_cfg   = config.get("users", {}).get(user_id, {})
    strava     = user_cfg.get("strava_tokens", {})
    access     = strava.get("access_token", "")
    expires_at = strava.get("expires_at", 0)

    if access and time.time() < expires_at - 60:
        return access

    refresh = strava.get("refresh_token", "")
    if not refresh:
        return None

    global_strava = config.get("strava", {})
    data = urllib.parse.urlencode({
        "client_id":     global_strava.get("client_id", ""),
        "client_secret": global_strava.get("client_secret", ""),
        "grant_type":    "refresh_token",
        "refresh_token": refresh,
    }).encode()
    try:
        req = urllib.request.Request(_STRAVA_TOKEN_URL, data=data, method="POST")
        with urllib.request.urlopen(req, timeout=30) as resp:
            body = json.loads(resp.read())
        strava["access_token"]  = body["access_token"]
        strava["expires_at"]    = body["expires_at"]
        strava["refresh_token"] = body.get("refresh_token", refresh)
        config["users"][user_id]["strava_tokens"] = strava
        save_config(config)
        return strava["access_token"]
    except (urllib.error.URLError, KeyError, json.JSONDecodeError) as exc:
        log.error("Strava token refresh failed for %r: %s", user_id, exc)
        return None


def sync_to_strava(
    config: dict,
    user_id: str,
    files: list,
    dry_run: bool = False,
) -> dict:
    """Upload GPX / TCX workout files to Strava for *user_id*."""
    token = _strava_refresh_token(config, user_id)
    if not token:
        return {"synced": 0, "error": "No Strava token available"}

    synced = 0
    errors: list = []

    for fpath in files:
        fp = Path(fpath)
        if fp.suffix.lower() not in (".gpx", ".tcx"):
            continue
        data_type = fp.suffix.lstrip(".")
        log.info("Uploading %s to Strava for user %r", fp.name, user_id)

        if dry_run:
            log.info("[dry-run] Would upload %s to Strava", fp.name)
            synced += 1
            continue

        try:
            file_bytes  = fp.read_bytes()
            boundary    = "----PrintmaxxBoundary"
            header_part = (
                f"--{boundary}\r\n"
                f"Content-Disposition: form-data; name=\"data_type\"\r\n\r\n"
                f"{data_type}\r\n"
                f"--{boundary}\r\n"
                f"Content-Disposition: form-data; name=\"file\"; filename=\"{fp.name}\"\r\n"
                f"Content-Type: application/octet-stream\r\n\r\n"
            ).encode()
            footer_part = f"\r\n--{boundary}--\r\n".encode()
            body        = header_part + file_bytes + footer_part

            req = urllib.request.Request(
                _STRAVA_UPLOAD_URL,
                data=body,
                headers={
                    "Authorization": f"Bearer {token}",
                    "Content-Type":  f"multipart/form-data; boundary={boundary}",
                },
                method="POST",
            )
            with urllib.request.urlopen(req, timeout=60) as resp:
                resp_body = json.loads(resp.read())
            log.info(
                "Strava upload queued: id=%s status=%s",
                resp_body.get("id"), resp_body.get("status"),
            )
            synced += 1
        except (urllib.error.URLError, OSError, json.JSONDecodeError) as exc:
            log.error("Strava upload failed for %s: %s", fp.name, exc)
            errors.append(str(exc))

    return {"synced": synced, "error": "; ".join(errors) if errors else None}


# ---------------------------------------------------------------------------
# Google Fit sync
# ---------------------------------------------------------------------------
_GFIT_SESSION_URL = "https://www.googleapis.com/fitness/v1/users/me/sessions"

_ACTIVITY_MAP = {
    "running":    8,
    "walking":    90,
    "cycling":    1,
    "swimming":   82,
    "hiking":     32,
    "treadmill":  97,
    "elliptical": 3,
    "strength":   80,
    "yoga":       100,
}


def _to_epoch_ms(value: str) -> "int | None":
    """Convert ISO-8601 or Unix-timestamp string to milliseconds since epoch."""
    if not value:
        return None
    try:
        return int(float(value) * 1000)
    except ValueError:
        pass
    for fmt in ("%Y-%m-%dT%H:%M:%SZ", "%Y-%m-%d %H:%M:%S", "%Y-%m-%d"):
        try:
            dt = datetime.strptime(value, fmt).replace(tzinfo=timezone.utc)
            return int(dt.timestamp() * 1000)
        except ValueError:
            pass
    return None


def _csv_to_gfit_sessions(csv_path: Path) -> list:
    """Convert a CSV workout file into minimal Google Fit session payloads."""
    sessions: list = []
    try:
        with open(csv_path, "r", encoding="utf-8", newline="") as fh:
            reader = csv.DictReader(fh)
            for row in reader:
                start_ms = _to_epoch_ms(row.get("start_time", ""))
                end_ms   = _to_epoch_ms(row.get("end_time", ""))
                if not start_ms or not end_ms:
                    continue
                activity = row.get("activity_type", "other").lower().strip()
                sessions.append({
                    "id":              f"mifit-{start_ms}",
                    "name":            row.get("activity_type", "Workout"),
                    "description":     "Imported from Mi Fit via PRINTMAXX",
                    "startTimeMillis": str(start_ms),
                    "endTimeMillis":   str(end_ms),
                    "application": {
                        "name":    "PRINTMAXX MiFit Exporter",
                        "version": "1.0",
                    },
                    "activityType": _ACTIVITY_MAP.get(activity, 4),
                })
    except (OSError, csv.Error) as exc:
        log.warning("Could not parse CSV %s: %s", csv_path, exc)
    return sessions


def sync_to_google_fit(
    config: dict,
    user_id: str,
    files: list,
    dry_run: bool = False,
) -> dict:
    """Upload workout CSV sessions to Google Fit for *user_id*."""
    user_cfg = config.get("users", {}).get(user_id, {})
    access   = user_cfg.get("google_fit_tokens", {}).get("access_token", "")
    if not access:
        log.warning("No Google Fit token for user %r; skipping sync", user_id)
        return {"synced": 0, "error": "No Google Fit access token"}

    synced = 0
    errors: list = []

    for fpath in files:
        fp = Path(fpath)
        if fp.suffix.lower() != ".csv":
            continue
        log.info("Syncing %s to Google Fit for user %r", fp.name, user_id)

        if dry_run:
            log.info("[dry-run] Would sync %s to Google Fit", fp.name)
            synced += 1
            continue

        try:
            for session in _csv_to_gfit_sessions(fp):
                payload = json.dumps(session).encode()
                req = urllib.request.Request(
                    _GFIT_SESSION_URL,
                    data=payload,
                    headers={
                        "Authorization": f"Bearer {access}",
                        "Content-Type":  "application/json",
                    },
                    method="POST",
                )
                with urllib.request.urlopen(req, timeout=30) as resp:
                    json.loads(resp.read())
                synced += 1
        except (urllib.error.URLError, OSError, json.JSONDecodeError) as exc:
            log.error("Google Fit sync failed for %s: %s", fp.name, exc)
            errors.append(str(exc))

    return {"synced": synced, "error": "; ".join(errors) if errors else None}


# ---------------------------------------------------------------------------
# Core run orchestration
# ---------------------------------------------------------------------------

def run_all_users(
    config: dict,
    dry_run: bool = False,
    user_filter: "str | None" = None,
) -> dict:
    """Export workouts for all (or one) configured users and persist status."""
    recall_skills_for_task("run mifit export for all users")
    users        = config.get("users", {})
    global_fmts  = config.get("exporter", {}).get("formats", ["gpx", "tcx", "csv"])
    status       = load_status()
    results: dict = {}

    for user_id, user_cfg in users.items():
        if user_filter and user_id != user_filter:
            continue
        if not user_cfg.get("enabled", True):
            log.info("User %r is disabled; skipping", user_id)
            continue

        log.info("=== Processing user: %r ===", user_id)
        user_formats = user_cfg.get("export_formats", global_fmts)
        result = run_exporter_for_user(user_id, user_cfg, user_formats, dry_run=dry_run)

        if result.get("success") and result.get("files"):
            sync_cfg = user_cfg.get("sync", {})
            if sync_cfg.get("strava"):
                result["strava"] = sync_to_strava(
                    config, user_id, result["files"], dry_run=dry_run
                )
            if sync_cfg.get("google_fit"):
                result["google_fit"] = sync_to_google_fit(
                    config, user_id, result["files"], dry_run=dry_run
                )

        status[user_id] = {
            "last_run":    datetime.now(timezone.utc).isoformat(),
            "last_result": result,
        }
        results[user_id] = result
        capture_skill_from_result(result, f"mifit export for user {user_id}")

    save_status(status)
    return results


# ---------------------------------------------------------------------------
# Status command
# ---------------------------------------------------------------------------

def print_status(config: dict) -> None:
    """Print a human-readable service status summary to stdout."""
    status = load_status()
    users  = config.get("users", {})
    width  = 60

    print(f"\n{'=' * width}")
    print(" PRINTMAXX -- Mi Fit Export Service  STATUS")
    print(f"{'=' * width}")
    print(f"  PROJECT  : {PROJECT}")
    print(f"  Log file : {LOG_FILE}")
    print(f"  Config   : {CONFIG_FILE}")
    exporter_ok = "present" if EXPORTER_SCRIPT.exists() else "NOT FOUND"
    print(f"  Exporter : {EXPORTER_DIR}  [{exporter_ok}]")
    print(f"  Users    : {len(users)} configured")
    print()

    if not users:
        print("  No users configured.")
        print("  Run --serve and add credentials via the web UI, or edit config directly.")
    else:
        for uid, ucfg in users.items():
            last        = status.get(uid, {})
            last_run    = last.get("last_run", "never")
            last_result = last.get("last_result", {})
            if not last_result:
                state = "----"
            elif last_result.get("success"):
                state = "OK  "
            else:
                state = "FAIL"
            fmt_list   = ", ".join(ucfg.get("export_formats", ["gpx", "tcx", "csv"]))
            sync_parts = [k for k, v in ucfg.get("sync", {}).items() if v]
            sync_str   = ", ".join(sync_parts) or "none"
            print(f"  [{state}] {uid}")
            print(f"         email   : {ucfg.get('email', '--')}")
            print(f"         formats : {fmt_list}")
            print(f"         sync    : {sync_str}")
            print(f"         last run: {last_run}")
            if last_result.get("error"):
                print(f"         error   : {last_result['error']}")
            if last_result.get("files"):
                print(f"         files   : {len(last_result['files'])} produced")
            print()

    print(f"{'=' * width}\n")


# ---------------------------------------------------------------------------
# Web UI
# ---------------------------------------------------------------------------
_HTML_TEMPLATE = (
    "<!DOCTYPE html>\n"
    "<html lang=\"en\">\n"
    "<head>\n"
    "  <meta charset=\"UTF-8\">\n"
    "  <title>PRINTMAXX -- Mi Fit Export</title>\n"
    "  <style>\n"
    "    body  { font-family: system-ui, sans-serif; max-width: 720px;\n"
    "             margin: 40px auto; background: #f5f5f5; padding: 0 16px; }\n"
    "    h1    { color: #0072C6; }\n"
    "    form  { background: #fff; padding: 24px; border-radius: 8px;\n"
    "             box-shadow: 0 1px 4px rgba(0,0,0,.1); }\n"
    "    label { display: block; margin: 12px 0 4px; font-weight: 600; }\n"
    "    input[type=text], input[type=email], input[type=password], select\n"
    "          { width: 100%; padding: 8px; box-sizing: border-box;\n"
    "             border: 1px solid #ccc; border-radius: 4px; }\n"
    "    button { margin-top: 16px; padding: 10px 28px; background: #0072C6;\n"
    "              color: #fff; border: none; border-radius: 4px;\n"
    "              cursor: pointer; font-size: 1em; }\n"
    "    button:hover { background: #005a9e; }\n"
    "    .msg  { margin: 12px 0; padding: 12px; border-radius: 4px; }\n"
    "    .ok   { background: #d4edda; color: #155724; }\n"
    "    .err  { background: #f8d7da; color: #721c24; }\n"
    "    table { width: 100%; border-collapse: collapse;\n"
    "             background: #fff; margin-top: 16px;\n"
    "             box-shadow: 0 1px 4px rgba(0,0,0,.1); }\n"
    "    th, td { padding: 10px; border: 1px solid #ddd; text-align: left; }\n"
    "    th    { background: #0072C6; color: #fff; }\n"
    "    a     { color: #0072C6; }\n"
    "  </style>\n"
    "</head>\n"
    "<body>\n"
    "<h1>PRINTMAXX -- Mi Fit / Zepp Export</h1>\n"
    "{message}\n"
    "<h2>Add / Update User</h2>\n"
    "<form method=\"POST\" action=\"/save_user\">\n"
    "  <label>User ID <small>(alphanumeric, e.g. alice)</small></label>\n"
    "  <input type=\"text\" name=\"user_id\" required"
    " pattern=\"[A-Za-z0-9_-]{1,64}\" maxlength=\"64\">\n"
    "  <label>Mi Fit / Zepp Email</label>\n"
    "  <input type=\"email\" name=\"email\" required>\n"
    "  <label>Password</label>\n"
    "  <input type=\"password\" name=\"password\" required>\n"
    "  <label>Export Formats (hold Ctrl/Cmd to select multiple)</label>\n"
    "  <select name=\"formats\" multiple size=\"3\">\n"
    "    <option value=\"gpx\" selected>GPX</option>\n"
    "    <option value=\"tcx\" selected>TCX</option>\n"
    "    <option value=\"csv\" selected>CSV</option>\n"
    "  </select>\n"
    "  <label><input type=\"checkbox\" name=\"sync_strava\" value=\"1\">"
    "&nbsp; Sync to Strava</label>\n"
    "  <label><input type=\"checkbox\" name=\"sync_gfit\" value=\"1\">"
    "&nbsp; Sync to Google Fit</label>\n"
    "  <button type=\"submit\">Save &amp; Export Now</button>\n"
    "</form>\n"
    "<h2>Registered Users</h2>\n"
    "{user_table}\n"
    "</body>\n"
    "</html>\n"
)

_USER_ROW_TMPL = (
    "<tr><td>{uid}</td><td>{email}</td><td>{fmts}</td>"
    "<td>{sync}</td>"
    "<td><a href='/run?user={uid}'>Run now</a></td></tr>"
)


def _render_index(config: dict, message: str = "") -> bytes:
    users = config.get("users", {})
    rows  = "".join(
        _USER_ROW_TMPL.format(
            uid   = uid,
            email = ucfg.get("email", ""),
            fmts  = ", ".join(ucfg.get("export_formats", [])),
            sync  = ", ".join(k for k, v in ucfg.get("sync", {}).items() if v) or "none",
        )
        for uid, ucfg in users.items()
    )
    table = (
        "<table>"
        "<tr><th>ID</th><th>Email</th><th>Formats</th><th>Sync</th><th>Action</th></tr>"
        f"{rows}</table>"
        if rows
        else "<p>No users registered yet.</p>"
    )
    return _HTML_TEMPLATE.format(message=message, user_table=table).encode("utf-8")


class _MifitHandler(BaseHTTPRequestHandler):
    """Minimal HTTP handler: credential form, on-demand trigger, file download."""

    config: dict  # injected by serve()

    def log_message(self, fmt: str, *args: object) -> None:
        log.debug("HTTP %s", fmt % args)

    def _send(
        self,
        code: int,
        body: bytes,
        content_type: str = "text/html; charset=utf-8",
    ) -> None:
        self.send_response(code)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:  # noqa: N802
        parsed = urllib.parse.urlparse(self.path)
        qs     = urllib.parse.parse_qs(parsed.query)

        if parsed.path in ("/", "/index.html"):
            self._send(200, _render_index(self.config))

        elif parsed.path == "/run":
            user_id = qs.get("user", [None])[0]
            try:
                results = run_all_users(self.config, dry_run=False, user_filter=user_id)
                ok      = all(r.get("success") for r in results.values())
                cls     = "ok" if ok else "err"
                label   = "succeeded" if ok else "had errors"
                names   = ", ".join(results) or "(no users matched)"
                msg = f'<div class="msg {cls}">Export {label} for: {names}</div>'
            except Exception as exc:  # noqa: BLE001
                log.error("Web-triggered run failed: %s", exc)
                msg = f'<div class="msg err">Export error: {exc}</div>'
            self._send(200, _render_index(self.config, msg))

        elif parsed.path.startswith("/download/"):
            self._serve_download(parsed.path[len("/download/"):])

        elif parsed.path == "/status.json":
            body = json.dumps(load_status(), indent=2, default=str).encode()
            self._send(200, body, "application/json")

        else:
            self._send(404, b"404 Not Found")

    def do_POST(self) -> None:  # noqa: N802
        parsed = urllib.parse.urlparse(self.path)
        if parsed.path != "/save_user":
            self._send(404, b"404 Not Found")
            return

        length = int(self.headers.get("Content-Length", 0))
        raw    = self.rfile.read(length).decode("utf-8", errors="replace")
        fields = urllib.parse.parse_qs(raw, keep_blank_values=True)

        def _f(key: str) -> str:
            return fields.get(key, [""])[0].strip()

        user_id  = _f("user_id")
        email    = _f("email")
        password = _f("password")

        if not user_id or not email or not password:
            msg = '<div class="msg err">All fields (user_id, email, password) are required.</div>'
            self._send(400, _render_index(self.config, msg))
            return

        safe_uid = "".join(c for c in user_id if c.isalnum() or c in "-_")[:64]
        fmts     = fields.get("formats", ["gpx", "tcx", "csv"])

        self.config.setdefault("users", {})[safe_uid] = {
            "email":          email,
            "password":       password,
            "export_formats": fmts,
            "enabled":        True,
            "sync": {
                "strava":     bool(_f("sync_strava")),
                "google_fit": bool(_f("sync_gfit")),
            },
        }
        try:
            save_config(self.config)
            log.info("User %r saved via web UI", safe_uid)
        except OSError as exc:
            msg = f'<div class="msg err">Failed to save config: {exc}</div>'
            self._send(500, _render_index(self.config, msg))
            return

        try:
            subprocess.Popen(
                [sys.executable, str(Path(__file__).resolve()), "--run", "--user", safe_uid],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
        except OSError as exc:
            log.warning("Could not launch background export: %s", exc)

        msg = (
            f'<div class="msg ok">User <b>{safe_uid}</b> saved.'
            " Export running in background.</div>"
        )
        self._send(200, _render_index(self.config, msg))

    def _serve_download(self, rel_path: str) -> None:
        """Stream a file from DATA_DIR; blocks path-escape attempts."""
        try:
            target = safe_path(DATA_DIR / rel_path, must_exist=True)
            data   = target.read_bytes()
            self.send_response(200)
            self.send_header("Content-Type", "application/octet-stream")
            self.send_header(
                "Content-Disposition", f'attachment; filename="{target.name}"'
            )
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)
        except (ValueError, FileNotFoundError, OSError) as exc:
            log.warning("File download failed (%r): %s", rel_path, exc)
            self._send(404, b"File not found or access denied")


def serve(config: dict, host: str = "127.0.0.1", port: int = 8080) -> None:
    """Start the credential / export web UI server (blocking)."""
    _MifitHandler.config = config
    httpd = HTTPServer((host, port), _MifitHandler)
    log.info("Web UI -> http://%s:%s/", host, port)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        log.info("Web server stopped by user")
    finally:
        httpd.server_close()


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def _build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="mifit_export_service",
        description="PRINTMAXX -- Mi Fit & Zepp workout export micro-SaaS",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Examples:\n"
            "  %(prog)s --run                   # export all users\n"
            "  %(prog)s --run --user alice      # export one user\n"
            "  %(prog)s --dry-run               # simulate without I/O\n"
            "  %(prog)s --status                # show service status\n"
            "  %(prog)s --serve --port 8080     # start web UI\n"
        ),
    )
    p.add_argument(
        "--run",
        action="store_true",
        help="Run exports for all configured users (or --user only)",
    )
    p.add_argument(
        "--status",
        action="store_true",
        help="Print service status and last-run results",
    )
    p.add_argument(
        "--dry-run",
        action="store_true",
        help="Simulate actions without writing files or calling external APIs",
    )
    p.add_argument(
        "--serve",
        action="store_true",
        help="Start the built-in web UI for credential management",
    )
    p.add_argument(
        "--user",
        metavar="USER_ID",
        help="Limit --run to a single user ID",
    )
    p.add_argument(
        "--host",
        metavar="ADDR",
        default=None,
        help="Bind address for --serve (overrides config; default 127.0.0.1)",
    )
    p.add_argument(
        "--port",
        type=int,
        default=None,
        help="TCP port for --serve (overrides config; default 8080)",
    )
    return p


def main() -> None:
    """Parse CLI arguments, dispatch the requested action, and exit cleanly."""
    parser = _build_parser()
    args   = parser.parse_args()

    if not any([args.run, args.status, args.dry_run, args.serve]):
        parser.print_help()
        sys.exit(0)

    log.info("PRINTMAXX mifit_export_service starting (pid=%s)", os.getpid())

    try:
        _ensure_dirs()
        config = load_config()
    except Exception as exc:  # noqa: BLE001
        log.critical("Initialisation failed: %s", exc)
        sys.exit(1)

    exit_code = 0

    try:
        if args.status:
            print_status(config)

        if args.dry_run and not args.run:
            log.info("[dry-run] Checking exporter availability ...")
            ensure_exporter(dry_run=True)
            users = config.get("users", {})
            log.info("[dry-run] %d user(s) configured: %s", len(users), list(users))
            sys.exit(0)

        if args.run or args.dry_run:
            if not ensure_exporter(dry_run=args.dry_run):
                log.critical("Exporter not available; aborting")
                sys.exit(1)
            results = run_all_users(config, dry_run=args.dry_run, user_filter=args.user)
            if any(not r.get("success") for r in results.values()):
                log.warning("One or more exports failed -- check the log for details")
                exit_code = 2
            else:
                log.info("All exports completed successfully")

        if args.serve:
            web_cfg = config.get("web", {})
            host    = args.host or web_cfg.get("host", "127.0.0.1")
            port    = args.port or web_cfg.get("port", 8080)
            serve(config, host=host, port=port)

    except Exception as exc:  # noqa: BLE001
        log.error("Unhandled error: %s", exc, exc_info=True)
        exit_code = 1

    log.info("mifit_export_service done (exit=%s)", exit_code)
    sys.exit(exit_code)


if __name__ == "__main__":
    main()