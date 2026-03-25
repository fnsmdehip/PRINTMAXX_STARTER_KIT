#!/usr/bin/env python3
"""
PRINTMAXX App Factory Scaffold Sync
=====================================
Wires dunky11/react-saas-template (MIT, JavaScript) into the App Factory base
template library. Clones the upstream repo, strips non-essentials, injects the
PRINTMAXX stack (Stripe payment integration, Firebase auth, RevenueCat stub),
and outputs a parameterized scaffold ready for SaaS variant forks.

Designed for weekly cron execution to pull upstream changes automatically so
every new App Factory SaaS variant starts from a working, styled base.

Usage:
    python3 app_factory_scaffold_sync.py --run
    python3 app_factory_scaffold_sync.py --dry-run
    python3 app_factory_scaffold_sync.py --status

Cron (weekly, Sundays 02:00):
    0 2 * * 0 /usr/bin/python3 /path/to/AUTOMATIONS/app_factory_scaffold_sync.py --run
"""

import argparse
import csv
import json
import logging
import os
import shutil
import subprocess
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

# ---------------------------------------------------------------------------
# Bootstrap: import from _common or fall back to local definitions
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

    def safe_path(path: Path) -> Path:  # type: ignore[misc]
        """Return *path* after asserting it resolves within PROJECT."""
        resolved = Path(path).resolve()
        try:
            resolved.relative_to(PROJECT.resolve())
        except ValueError:
            raise ValueError(
                f"Path escape detected: {resolved!r} is outside PROJECT {PROJECT!r}"
            )
        return resolved

    def recall_skills_for_task(task: str) -> list:  # type: ignore[misc]
        """Stub: return stored skill references for *task*."""
        return []

    def capture_skill_from_result(task: str, result: dict) -> None:  # type: ignore[misc]
        """Stub: persist a skill learned from *result*."""
        pass


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
REPO_URL = "https://github.com/dunky11/react-saas-template.git"

UPSTREAM_CACHE: Path = PROJECT / "AUTOMATIONS" / "cache" / "react-saas-template-upstream"
SCAFFOLD_DIR: Path = PROJECT / "OUTPUTS" / "app_factory" / "react-saas-scaffold"
LOG_PATH: Path = PROJECT / "AUTOMATIONS" / "logs" / "app_factory_scaffold_sync.log"
STATUS_PATH: Path = PROJECT / "AUTOMATIONS" / "logs" / "app_factory_scaffold_sync_status.json"
RUNS_CSV: Path = PROJECT / "AUTOMATIONS" / "logs" / "app_factory_scaffold_sync_runs.csv"

# Relative paths inside the upstream clone to remove before scaffolding
STRIP_PATHS: list = [
    "src/dummy",
    "src/images/logged_out",
    ".github",
    "CHANGELOG.md",
    "CODE_OF_CONDUCT.md",
    "CONTRIBUTING.md",
    "screenshots",
]

# PRINTMAXX environment variable templates
STRIPE_ENV_VARS: dict = {
    "REACT_APP_STRIPE_PUBLISHABLE_KEY": "pk_live_REPLACE_ME",
    "REACT_APP_STRIPE_PRICE_ID_MONTHLY": "price_REPLACE_ME_MONTHLY",
    "REACT_APP_STRIPE_PRICE_ID_ANNUAL": "price_REPLACE_ME_ANNUAL",
}

FIREBASE_ENV_VARS: dict = {
    "REACT_APP_FIREBASE_API_KEY": "REPLACE_ME",
    "REACT_APP_FIREBASE_AUTH_DOMAIN": "REPLACE_ME.firebaseapp.com",
    "REACT_APP_FIREBASE_PROJECT_ID": "REPLACE_ME",
    "REACT_APP_FIREBASE_STORAGE_BUCKET": "REPLACE_ME.appspot.com",
    "REACT_APP_FIREBASE_MESSAGING_SENDER_ID": "REPLACE_ME",
    "REACT_APP_FIREBASE_APP_ID": "REPLACE_ME",
}

REVENUECAT_ENV_VARS: dict = {
    "REACT_APP_REVENUECAT_API_KEY": "REPLACE_ME",
}


# ---------------------------------------------------------------------------
# Logging (file append + stdout; configured once at module load)
# ---------------------------------------------------------------------------

def _configure_logging() -> logging.Logger:
    log_dir = LOG_PATH.parent
    log_dir.mkdir(parents=True, exist_ok=True)
    logger = logging.getLogger("app_factory_scaffold_sync")
    logger.setLevel(logging.DEBUG)
    if not logger.handlers:
        file_handler = logging.FileHandler(
            safe_path(LOG_PATH), mode="a", encoding="utf-8"
        )
        file_handler.setFormatter(
            logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
        )
        logger.addHandler(file_handler)
        stream_handler = logging.StreamHandler(sys.stdout)
        stream_handler.setFormatter(logging.Formatter("[%(levelname)s] %(message)s"))
        logger.addHandler(stream_handler)
    return logger


log: logging.Logger = _configure_logging()


# ---------------------------------------------------------------------------
# Safe file I/O helpers
# ---------------------------------------------------------------------------

def _write_text(path: Path, content: str, dry_run: bool = False) -> None:
    if dry_run:
        log.info("[DRY-RUN] Would write text file: %s", path)
        return
    target = safe_path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content, encoding="utf-8")


def _write_json(path: Path, data: dict, dry_run: bool = False) -> None:
    if dry_run:
        log.info("[DRY-RUN] Would write JSON: %s", path)
        return
    target = safe_path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(data, indent=2), encoding="utf-8")


def _append_csv_row(
    path: Path,
    row: dict,
    fieldnames: list,
    dry_run: bool = False,
) -> None:
    if dry_run:
        log.info("[DRY-RUN] Would append CSV row to %s: %s", path, row)
        return
    target = safe_path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    write_header = not target.exists()
    with target.open("a", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        if write_header:
            writer.writeheader()
        writer.writerow(row)


# ---------------------------------------------------------------------------
# Subprocess helper
# ---------------------------------------------------------------------------

def _run(
    cmd: list,
    cwd: Optional[Path] = None,
    dry_run: bool = False,
) -> subprocess.CompletedProcess:
    label = " ".join(str(c) for c in cmd)
    if dry_run:
        log.info("[DRY-RUN] Would execute: %s", label)
        return subprocess.CompletedProcess(cmd, returncode=0, stdout="", stderr="")
    log.debug("Executing: %s", label)
    result = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    if result.returncode != 0:
        log.warning("stderr: %s", result.stderr.strip())
    return result


# ---------------------------------------------------------------------------
# Preflight checks
# ---------------------------------------------------------------------------

def _git_available() -> bool:
    try:
        return subprocess.run(["git", "--version"], capture_output=True).returncode == 0
    except FileNotFoundError:
        return False


def _github_reachable() -> bool:
    try:
        urllib.request.urlopen("https://github.com", timeout=10)
        return True
    except urllib.error.URLError:
        return False


# ---------------------------------------------------------------------------
# Upstream management
# ---------------------------------------------------------------------------

def clone_or_update_upstream(dry_run: bool = False) -> bool:
    """Clone the upstream repo or pull latest changes. Returns True on success."""
    UPSTREAM_CACHE.parent.mkdir(parents=True, exist_ok=True)

    if UPSTREAM_CACHE.exists():
        log.info("Upstream cache found — pulling latest ...")
        result = _run(
            ["git", "pull", "--ff-only", "origin", "main"],
            cwd=UPSTREAM_CACHE,
            dry_run=dry_run,
        )
        if result.returncode != 0:
            log.warning("git pull failed — attempting fresh clone.")
            if not dry_run:
                shutil.rmtree(UPSTREAM_CACHE, ignore_errors=True)
            return _fresh_clone(dry_run=dry_run)
    else:
        return _fresh_clone(dry_run=dry_run)

    log.info("Upstream cache is current.")
    return True


def _fresh_clone(dry_run: bool = False) -> bool:
    log.info("Cloning %s ...", REPO_URL)
    result = _run(
        ["git", "clone", "--depth", "1", REPO_URL, str(UPSTREAM_CACHE)],
        dry_run=dry_run,
    )
    if result.returncode != 0:
        log.error("git clone failed: %s", result.stderr.strip())
        return False
    log.info("Clone complete.")
    return True


def get_upstream_sha(dry_run: bool = False) -> str:
    if dry_run or not UPSTREAM_CACHE.exists():
        return "dry-run-sha"
    result = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=UPSTREAM_CACHE,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip() if result.returncode == 0 else "unknown"


# ---------------------------------------------------------------------------
# Strip non-essentials
# ---------------------------------------------------------------------------

def strip_non_essentials(dry_run: bool = False) -> None:
    """Copy upstream cache to scaffold dir and remove non-essential paths."""
    if not dry_run:
        if SCAFFOLD_DIR.exists():
            shutil.rmtree(SCAFFOLD_DIR)
        target = safe_path(SCAFFOLD_DIR)
        shutil.copytree(UPSTREAM_CACHE, target, ignore=shutil.ignore_patterns(".git"))
        log.info("Copied upstream to %s", SCAFFOLD_DIR)
    else:
        log.info("[DRY-RUN] Would copy %s → %s", UPSTREAM_CACHE, SCAFFOLD_DIR)

    for rel in STRIP_PATHS:
        target_path = SCAFFOLD_DIR / rel
        if dry_run:
            log.info("[DRY-RUN] Would strip: %s", rel)
            continue
        if target_path.exists():
            if target_path.is_dir():
                shutil.rmtree(target_path)
            else:
                target_path.unlink()
            log.info("Stripped: %s", rel)
        else:
            log.debug("Strip target not present (skipping): %s", rel)


# ---------------------------------------------------------------------------
# PRINTMAXX stack injection
# ---------------------------------------------------------------------------

def inject_stripe(dry_run: bool = False) -> None:
    """Write Stripe client stub into the scaffold."""
    log.info("Injecting Stripe payment integration ...")
    content = """\
// PRINTMAXX — Stripe payment integration
// Populate REACT_APP_STRIPE_* vars in .env.local before deploying.
// Install: npm install @stripe/stripe-js @stripe/react-stripe-js

import { loadStripe } from '@stripe/stripe-js';

const stripePromise = loadStripe(process.env.REACT_APP_STRIPE_PUBLISHABLE_KEY);

/**
 * Redirect to Stripe Checkout for the given price ID.
 * Wire to a backend endpoint that creates a Checkout Session.
 *
 * @param {string} priceId - Stripe price ID (monthly or annual)
 * @param {string} customerId - Optional existing Stripe customer ID
 */
export async function redirectToCheckout(priceId, customerId) {
  const stripe = await stripePromise;
  // const { sessionId } = await fetch('/api/stripe/create-checkout-session', {
  //   method: 'POST',
  //   headers: { 'Content-Type': 'application/json' },
  //   body: JSON.stringify({ priceId, customerId }),
  // }).then((r) => r.json());
  // await stripe.redirectToCheckout({ sessionId });
  console.warn('[PRINTMAXX] Stripe checkout stub — wire to your backend.');
}

/**
 * Open Stripe Customer Portal so the user can manage their subscription.
 */
export async function openCustomerPortal() {
  // const { url } = await fetch('/api/stripe/customer-portal', {
  //   method: 'POST',
  // }).then((r) => r.json());
  // window.location.href = url;
  console.warn('[PRINTMAXX] Stripe customer portal stub — wire to your backend.');
}

export default stripePromise;
"""
    dest = SCAFFOLD_DIR / "src" / "printmaxx" / "stripe" / "stripeClient.js"
    _write_text(dest, content, dry_run=dry_run)
    log.info("Stripe stub → %s", dest.relative_to(PROJECT))


def inject_firebase_auth(dry_run: bool = False) -> None:
    """Write Firebase auth configuration stub into the scaffold."""
    log.info("Injecting Firebase auth ...")
    content = """\
// PRINTMAXX — Firebase Authentication
// Populate REACT_APP_FIREBASE_* vars in .env.local before deploying.
// Install: npm install firebase

import { initializeApp, getApps } from 'firebase/app';
import { getAuth, GoogleAuthProvider, signInWithPopup, signOut } from 'firebase/auth';

const firebaseConfig = {
  apiKey: process.env.REACT_APP_FIREBASE_API_KEY,
  authDomain: process.env.REACT_APP_FIREBASE_AUTH_DOMAIN,
  projectId: process.env.REACT_APP_FIREBASE_PROJECT_ID,
  storageBucket: process.env.REACT_APP_FIREBASE_STORAGE_BUCKET,
  messagingSenderId: process.env.REACT_APP_FIREBASE_MESSAGING_SENDER_ID,
  appId: process.env.REACT_APP_FIREBASE_APP_ID,
};

// Prevent duplicate app initialisation during hot-reload
const app = getApps().length === 0 ? initializeApp(firebaseConfig) : getApps()[0];
export const auth = getAuth(app);
export const googleProvider = new GoogleAuthProvider();

export async function signInWithGoogle() {
  return signInWithPopup(auth, googleProvider);
}

export async function signOutUser() {
  return signOut(auth);
}

export default app;
"""
    dest = SCAFFOLD_DIR / "src" / "printmaxx" / "firebase" / "firebaseClient.js"
    _write_text(dest, content, dry_run=dry_run)
    log.info("Firebase auth stub → %s", dest.relative_to(PROJECT))


def inject_revenuecat_stub(dry_run: bool = False) -> None:
    """Write RevenueCat web SDK stub into the scaffold."""
    log.info("Injecting RevenueCat stub ...")
    content = """\
// PRINTMAXX — RevenueCat subscription management stub
// Populate REACT_APP_REVENUECAT_API_KEY in .env.local before deploying.
// Install: npm install @revenuecat/purchases-js

// import Purchases from '@revenuecat/purchases-js';

let _purchases = null;

/**
 * Initialise (or return cached) RevenueCat Purchases instance.
 *
 * @param {string} userId - Authenticated user ID
 * @returns {Promise<Purchases|null>}
 */
export async function configureRevenueCat(userId) {
  if (_purchases) return _purchases;
  // _purchases = new Purchases(process.env.REACT_APP_REVENUECAT_API_KEY);
  // await _purchases.logIn(userId);
  // return _purchases;
  console.warn('[PRINTMAXX] RevenueCat stub — install SDK and uncomment above.');
  return null;
}

/**
 * Fetch available subscription offerings.
 *
 * @returns {Promise<Object>} RevenueCat Offerings object
 */
export async function getOfferings() {
  // const purchases = await configureRevenueCat(currentUserId);
  // return purchases.getOfferings();
  console.warn('[PRINTMAXX] RevenueCat getOfferings stub.');
  return { current: null, all: {} };
}

/**
 * Purchase a specific package from an offering.
 *
 * @param {Object} pkg - RevenueCat Package object
 * @returns {Promise<Object|null>}
 */
export async function purchasePackage(pkg) {
  // const purchases = await configureRevenueCat(currentUserId);
  // return purchases.purchasePackage(pkg);
  console.warn('[PRINTMAXX] RevenueCat purchasePackage stub.');
  return null;
}

/**
 * Restore previous purchases for the current user.
 *
 * @returns {Promise<Object|null>}
 */
export async function restorePurchases() {
  // const purchases = await configureRevenueCat(currentUserId);
  // return purchases.restorePurchases();
  console.warn('[PRINTMAXX] RevenueCat restorePurchases stub.');
  return null;
}
"""
    dest = SCAFFOLD_DIR / "src" / "printmaxx" / "revenuecat" / "revenueCatClient.js"
    _write_text(dest, content, dry_run=dry_run)
    log.info("RevenueCat stub → %s", dest.relative_to(PROJECT))


def inject_printmaxx_index(dry_run: bool = False) -> None:
    """Write a barrel export so consumers import from a single entry point."""
    content = """\
// PRINTMAXX stack — barrel export
// import { redirectToCheckout, auth, configureRevenueCat } from '../printmaxx';

export { default as stripePromise, redirectToCheckout, openCustomerPortal } from './stripe/stripeClient';
export { default as firebaseApp, auth, googleProvider, signInWithGoogle, signOutUser } from './firebase/firebaseClient';
export { configureRevenueCat, getOfferings, purchasePackage, restorePurchases } from './revenuecat/revenueCatClient';
"""
    dest = SCAFFOLD_DIR / "src" / "printmaxx" / "index.js"
    _write_text(dest, content, dry_run=dry_run)
    log.info("Printmaxx barrel index → %s", dest.relative_to(PROJECT))


# ---------------------------------------------------------------------------
# Scaffold support files
# ---------------------------------------------------------------------------

def write_env_example(dry_run: bool = False) -> None:
    """Write a combined .env.example with all PRINTMAXX environment variables."""
    log.info("Writing .env.example ...")
    lines = [
        "# PRINTMAXX App Factory — environment variable template",
        "# Copy to .env.local and fill in real values before running.\n",
        "# ── Stripe ─────────────────────────────────────────────────────────",
    ]
    for k, v in STRIPE_ENV_VARS.items():
        lines.append(f"{k}={v}")
    lines += [
        "",
        "# ── Firebase ────────────────────────────────────────────────────────",
    ]
    for k, v in FIREBASE_ENV_VARS.items():
        lines.append(f"{k}={v}")
    lines += [
        "",
        "# ── RevenueCat ──────────────────────────────────────────────────────",
    ]
    for k, v in REVENUECAT_ENV_VARS.items():
        lines.append(f"{k}={v}")
    lines.append("")
    _write_text(SCAFFOLD_DIR / ".env.example", "\n".join(lines), dry_run=dry_run)


def write_scaffold_manifest(sha: str, dry_run: bool = False) -> None:
    """Write printmaxx_scaffold.json metadata into the scaffold root."""
    manifest = {
        "printmaxx_scaffold": True,
        "upstream_repo": REPO_URL,
        "upstream_sha": sha,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "stack": {
            "payment": "stripe",
            "auth": "firebase",
            "subscriptions": "revenuecat",
        },
        "stripped_paths": STRIP_PATHS,
        "injected_modules": [
            "src/printmaxx/stripe/stripeClient.js",
            "src/printmaxx/firebase/firebaseClient.js",
            "src/printmaxx/revenuecat/revenueCatClient.js",
            "src/printmaxx/index.js",
        ],
        "env_vars_required": list(STRIPE_ENV_VARS)
        + list(FIREBASE_ENV_VARS)
        + list(REVENUECAT_ENV_VARS),
    }
    _write_json(SCAFFOLD_DIR / "printmaxx_scaffold.json", manifest, dry_run=dry_run)
    log.info("Scaffold manifest written.")


# ---------------------------------------------------------------------------
# Audit helpers
# ---------------------------------------------------------------------------

def _record_run(status: str, sha: str, dry_run: bool = False) -> None:
    row = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "status": status,
        "upstream_sha": sha,
        "dry_run": str(dry_run),
        "scaffold_path": str(SCAFFOLD_DIR),
    }
    _append_csv_row(
        RUNS_CSV,
        row,
        fieldnames=["timestamp", "status", "upstream_sha", "dry_run", "scaffold_path"],
        dry_run=dry_run,
    )


def _update_status(status: str, sha: str, dry_run: bool = False) -> None:
    data = {
        "last_run": datetime.now(timezone.utc).isoformat(),
        "status": status,
        "upstream_sha": sha,
        "scaffold_path": str(SCAFFOLD_DIR),
        "dry_run": dry_run,
    }
    _write_json(STATUS_PATH, data, dry_run=dry_run)


# ---------------------------------------------------------------------------
# CLI command implementations
# ---------------------------------------------------------------------------

def cmd_status() -> int:
    """Print last sync status from the status JSON file."""
    if not STATUS_PATH.exists():
        print("No status file found. Run with --run to generate the scaffold.")
        return 0
    try:
        data = json.loads(STATUS_PATH.read_text(encoding="utf-8"))
        scaffold_present = Path(data.get("scaffold_path", "")).exists()
        print(f"Last run        : {data.get('last_run', 'unknown')}")
        print(f"Status          : {data.get('status', 'unknown')}")
        print(f"Upstream SHA    : {data.get('upstream_sha', 'unknown')}")
        print(f"Scaffold path   : {data.get('scaffold_path', 'unknown')}")
        print(f"Scaffold present: {scaffold_present}")
        print(f"Dry run         : {data.get('dry_run', False)}")
    except (json.JSONDecodeError, OSError) as exc:
        log.error("Failed to read status file: %s", exc)
        return 1
    return 0


def cmd_run(dry_run: bool = False) -> int:
    """Full scaffold sync: clone/pull → strip → inject → manifest."""
    log.info("=== App Factory Scaffold Sync START (dry_run=%s) ===", dry_run)

    skills = recall_skills_for_task("app_factory_scaffold_sync")
    if skills:
        log.info("Recalled %d skill(s) for this task.", len(skills))

    sha = "unknown"

    try:
        # 1. Preflight
        if not _git_available():
            log.error("git not found on PATH — aborting.")
            return 1

        if not dry_run and not _github_reachable():
            log.error("GitHub is unreachable — aborting network operations.")
            return 1

        # 2. Refresh upstream cache
        if not clone_or_update_upstream(dry_run=dry_run):
            log.error("Failed to refresh upstream cache.")
            _record_run("FAILED_CLONE", sha, dry_run=dry_run)
            _update_status("FAILED_CLONE", sha, dry_run=dry_run)
            return 1

        sha = get_upstream_sha(dry_run=dry_run)
        log.info("Upstream HEAD SHA: %s", sha)

        # 3. Strip non-essentials → scaffold dir
        strip_non_essentials(dry_run=dry_run)

        # 4. Inject PRINTMAXX stack
        inject_stripe(dry_run=dry_run)
        inject_firebase_auth(dry_run=dry_run)
        inject_revenuecat_stub(dry_run=dry_run)
        inject_printmaxx_index(dry_run=dry_run)

        # 5. Support files
        write_env_example(dry_run=dry_run)
        write_scaffold_manifest(sha, dry_run=dry_run)

        # 6. Audit
        _record_run("SUCCESS", sha, dry_run=dry_run)
        _update_status("SUCCESS", sha, dry_run=dry_run)

        capture_skill_from_result(
            "app_factory_scaffold_sync",
            {"status": "SUCCESS", "sha": sha, "dry_run": dry_run},
        )

        log.info("=== App Factory Scaffold Sync COMPLETE ===")
        return 0

    except Exception as exc:
        log.exception("Unhandled error during scaffold sync: %s", exc)
        _record_run("ERROR", sha, dry_run=dry_run)
        _update_status("ERROR", sha, dry_run=dry_run)
        return 1


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "PRINTMAXX App Factory Scaffold Sync — wires dunky11/react-saas-template "
            "into the App Factory base template library with Stripe, Firebase, and RevenueCat."
        )
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--run",
        action="store_true",
        help="Run the full scaffold sync (clone/pull, strip, inject, write).",
    )
    group.add_argument(
        "--status",
        action="store_true",
        help="Print the last sync status without performing any sync.",
    )
    group.add_argument(
        "--dry-run",
        action="store_true",
        help="Simulate the full sync without writing any files.",
    )

    args = parser.parse_args()

    if args.status:
        sys.exit(cmd_status())
    elif args.run:
        sys.exit(cmd_run(dry_run=False))
    elif args.dry_run:
        sys.exit(cmd_run(dry_run=True))


if __name__ == "__main__":
    main()