#!/usr/bin/env python3
"""
PRINTMAXX Automation: many_notes_niche_deployer

Forks the brufdev/many-notes PHP repo (MIT, 928 stars), strips it to core
functionality, wires Stripe paywall + multi-tenant isolation, and deploys
as niche-specific hosted note apps for legal, medical, and real estate
verticals.

DAG-based execution with idempotent task checkpointing, dry-run support,
CSV reporting, and cron-safe operation (no interactive input, clean exit).

Usage:
    python3 many_notes_niche_deployer.py --run
    python3 many_notes_niche_deployer.py --dry-run
    python3 many_notes_niche_deployer.py --status
"""

import argparse
import csv
import json
import logging
import subprocess
import sys
import urllib.request
import urllib.error
from datetime import datetime
from pathlib import Path

# ---------------------------------------------------------------------------
# Bootstrap: import from _common if available, else define locally
# ---------------------------------------------------------------------------
try:
    from _common import (
        PROJECT,
        safe_path,
        recall_skills_for_task,
        capture_skill_from_result,
    )
except ImportError:
    PROJECT = Path(__file__).resolve().parent.parent

    def safe_path(path: "Path | str") -> Path:
        """Validate that *path* resolves inside PROJECT, preventing traversal."""
        resolved = Path(path).resolve()
        try:
            resolved.relative_to(PROJECT)
        except ValueError:
            raise ValueError(
                f"Path {resolved} escapes PROJECT root {PROJECT}"
            )
        return resolved

    def recall_skills_for_task(task_name: str) -> list:
        return []

    def capture_skill_from_result(task_name: str, result: dict) -> None:
        pass

# ---------------------------------------------------------------------------
# Directory / file constants
# ---------------------------------------------------------------------------
AUTOMATIONS_DIR = PROJECT / "AUTOMATIONS"
LOG_DIR         = AUTOMATIONS_DIR / "logs"
LOG_FILE        = LOG_DIR / "many_notes_niche_deployer.log"
STATUS_FILE     = AUTOMATIONS_DIR / "many_notes_niche_deployer_status.json"
BUILD_DIR       = AUTOMATIONS_DIR / "build"  / "many_notes"
DEPLOY_DIR      = AUTOMATIONS_DIR / "deploy" / "many_notes"
CSV_REPORT      = AUTOMATIONS_DIR / "reports" / "many_notes_niche_deployer.csv"

UPSTREAM_REPO   = "https://github.com/brufdev/many-notes"

# ---------------------------------------------------------------------------
# Niche definitions
# ---------------------------------------------------------------------------
NICHES: dict = {
    "legal": {
        "app_name":         "LegalNotes",
        "description":      "Secure note-taking for legal professionals",
        "plan_price_cents": 2900,
        "plan_name":        "Legal Pro",
        "color_primary":    "#1a237e",
        "features":         ["case-tagging", "client-isolation", "export-pdf"],
    },
    "medical": {
        "app_name":         "MedNotes",
        "description":      "HIPAA-aligned clinical notes for healthcare providers",
        "plan_price_cents": 3900,
        "plan_name":        "Clinical Pro",
        "color_primary":    "#1b5e20",
        "features":         ["patient-tagging", "audit-log", "2fa-required"],
    },
    "real_estate": {
        "app_name":         "DealNotes",
        "description":      "Property and deal notes for real estate professionals",
        "plan_price_cents": 1900,
        "plan_name":        "Agent Pro",
        "color_primary":    "#bf360c",
        "features":         ["property-tagging", "client-crm", "map-pins"],
    },
}

# Directories / files to strip from the upstream clone (bloat / demo content)
STRIP_PATTERNS = [
    ".github",
    "tests",
    "docs",
    "README.md",
    "CHANGELOG.md",
    "screenshots",
]

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------

def setup_logging() -> logging.Logger:
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    logger = logging.getLogger("many_notes_niche_deployer")
    logger.setLevel(logging.DEBUG)
    if not logger.handlers:
        fh = logging.FileHandler(
            str(safe_path(LOG_FILE)), mode="a", encoding="utf-8"
        )
        fh.setLevel(logging.DEBUG)
        fmt = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
        fh.setFormatter(fmt)
        logger.addHandler(fh)

        sh = logging.StreamHandler(sys.stdout)
        sh.setLevel(logging.INFO)
        sh.setFormatter(fmt)
        logger.addHandler(sh)
    return logger

# ---------------------------------------------------------------------------
# Status helpers (JSON checkpoint file)
# ---------------------------------------------------------------------------

def load_status() -> dict:
    if STATUS_FILE.exists():
        try:
            with open(safe_path(STATUS_FILE), "r", encoding="utf-8") as fh:
                return json.load(fh)
        except (json.JSONDecodeError, OSError, ValueError):
            pass
    return {"tasks": {}, "last_run": None, "run_count": 0}


def save_status(status: dict) -> None:
    STATUS_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(safe_path(STATUS_FILE), "w", encoding="utf-8") as fh:
        json.dump(status, fh, indent=2, default=str)


def mark_task(status: dict, task: str, state: str, detail: str = "") -> None:
    status["tasks"][task] = {
        "state":   state,
        "updated": datetime.utcnow().isoformat(),
        "detail":  detail,
    }


def task_done(status: dict, task: str) -> bool:
    return status.get("tasks", {}).get(task, {}).get("state") == "done"

# ---------------------------------------------------------------------------
# CSV reporting
# ---------------------------------------------------------------------------

def append_csv_row(row: dict) -> None:
    CSV_REPORT.parent.mkdir(parents=True, exist_ok=True)
    file_exists = CSV_REPORT.exists()
    fieldnames = ["timestamp", "task", "niche", "state", "detail"]
    with open(safe_path(CSV_REPORT), "a", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames, extrasaction="ignore")
        if not file_exists:
            writer.writeheader()
        writer.writerow({**{"timestamp": datetime.utcnow().isoformat()}, **row})

# ---------------------------------------------------------------------------
# Shell helper
# ---------------------------------------------------------------------------

def run_cmd(
    cmd: list,
    *,
    cwd: "Path | None" = None,
    dry_run: bool = False,
    logger: "logging.Logger | None" = None,
) -> tuple:
    """Run *cmd*, return (returncode, stdout, stderr)."""
    if logger:
        logger.debug("CMD: %s  cwd=%s", " ".join(str(c) for c in cmd), cwd)
    if dry_run:
        if logger:
            logger.info("[DRY-RUN] would run: %s", " ".join(str(c) for c in cmd))
        return 0, "", ""
    try:
        result = subprocess.run(
            [str(c) for c in cmd],
            cwd=str(cwd) if cwd else None,
            capture_output=True,
            text=True,
            timeout=300,
        )
        return result.returncode, result.stdout.strip(), result.stderr.strip()
    except subprocess.TimeoutExpired:
        return 1, "", "command timed out after 300 s"
    except FileNotFoundError as exc:
        return 1, "", str(exc)

# ---------------------------------------------------------------------------
# File-generation helpers (each writes exactly one file via safe_path)
# ---------------------------------------------------------------------------

def _write_file(path: Path, content: str, dry_run: bool, logger: logging.Logger) -> bool:
    """Safely write *content* to *path*; respects dry_run."""
    if dry_run:
        logger.info("[DRY-RUN] would write: %s", path)
        return True
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(safe_path(path), "w", encoding="utf-8") as fh:
            fh.write(content)
        return True
    except (OSError, ValueError) as exc:
        logger.error("Failed to write %s: %s", path, exc)
        return False


def _stripe_paywall_middleware(dest: Path, niche: str, cfg: dict) -> tuple:
    """Return (path, content) for the Stripe paywall middleware."""
    path = dest / "app" / "Http" / "Middleware" / "StripePaywallMiddleware.php"
    content = f"""\
<?php
/**
 * StripePaywallMiddleware — generated by PRINTMAXX
 * Niche: {niche} | Plan: {cfg['plan_name']} ({cfg['plan_price_cents']} ¢/month)
 */
namespace App\\Http\\Middleware;

use Closure;
use Illuminate\\Http\\Request;
use Illuminate\\Support\\Facades\\Auth;

class StripePaywallMiddleware
{{
    public function handle(Request $request, Closure $next)
    {{
        if (!Auth::check()) {{
            return redirect()->route('login');
        }}

        $user = Auth::user();

        // stripe_subscribed is a boolean column kept current by webhook
        if (!$user->stripe_subscribed) {{
            return redirect()->route('billing.subscribe')->with(
                'info',
                'A {cfg["plan_name"]} subscription is required to access {cfg["app_name"]}.'
            );
        }}

        // Multi-tenant isolation: bind current tenant to the IoC container
        app()->instance('current_tenant_id', $user->id);

        return $next($request);
    }}
}}
"""
    return path, content


def _billing_controller(dest: Path, niche: str, cfg: dict) -> tuple:
    """Return (path, content) for the BillingController."""
    path = dest / "app" / "Http" / "Controllers" / "BillingController.php"
    content = f"""\
<?php
/**
 * BillingController — generated by PRINTMAXX
 * Niche: {niche} | App: {cfg['app_name']}
 */
namespace App\\Http\\Controllers;

use Illuminate\\Http\\Request;
use Illuminate\\Support\\Facades\\Auth;
use Stripe\\Stripe;
use Stripe\\Checkout\\Session as StripeCheckout;
use Stripe\\Webhook;
use Stripe\\Exception\\SignatureVerificationException;

class BillingController extends Controller
{{
    public function __construct()
    {{
        Stripe::setApiKey(config('services.stripe.secret'));
    }}

    public function subscribe()
    {{
        return view('billing.subscribe', [
            'app_name'    => '{cfg["app_name"]}',
            'plan_name'   => '{cfg["plan_name"]}',
            'price_cents' => {cfg["plan_price_cents"]},
            'pub_key'     => config('services.stripe.key'),
        ]);
    }}

    public function checkout(Request $request)
    {{
        $user    = Auth::user();
        $session = StripeCheckout::create([
            'payment_method_types' => ['card'],
            'line_items'           => [[
                'price'    => config('services.stripe.price_id'),
                'quantity' => 1,
            ]],
            'mode'                 => 'subscription',
            'client_reference_id' => (string) $user->id,
            'customer_email'      => $user->email,
            'success_url'         => route('billing.success') . '?session_id={{CHECKOUT_SESSION_ID}}',
            'cancel_url'          => route('billing.cancel'),
        ]);
        return redirect($session->url, 303);
    }}

    public function success()
    {{
        return view('billing.success', ['app_name' => '{cfg["app_name"]}']);
    }}

    public function cancel()
    {{
        return redirect()->route('billing.subscribe')
            ->with('warning', 'Subscription cancelled — you can resubscribe anytime.');
    }}

    public function webhook(Request $request)
    {{
        try {{
            $event = Webhook::constructEvent(
                $request->getContent(),
                $request->header('Stripe-Signature'),
                config('services.stripe.webhook_secret')
            );
        }} catch (SignatureVerificationException $e) {{
            return response('Invalid signature', 400);
        }}

        $sub = $event->data->object;
        $uid = $sub->client_reference_id
            ?? $sub->metadata->client_reference_id
            ?? null;

        if ($uid) {{
            $active = in_array($event->type, [
                'customer.subscription.created',
                'customer.subscription.updated',
            ]) && $sub->status === 'active';

            if ($event->type === 'customer.subscription.deleted') {{
                $active = false;
            }}

            \\App\\Models\\User::where('id', $uid)
                ->update(['stripe_subscribed' => $active]);
        }}

        return response('OK', 200);
    }}
}}
"""
    return path, content


def _tenant_scope_trait(dest: Path) -> tuple:
    """Return (path, content) for the TenantScoped Eloquent trait."""
    path = dest / "app" / "Models" / "Traits" / "TenantScoped.php"
    content = """\
<?php
/**
 * TenantScoped — generated by PRINTMAXX
 * Adds automatic per-user isolation to any Eloquent model.
 * Usage: add `use TenantScoped;` to your model class.
 */
namespace App\\Models\\Traits;

use Illuminate\\Database\\Eloquent\\Builder;
use Illuminate\\Support\\Facades\\App;

trait TenantScoped
{
    public static function bootTenantScoped(): void
    {
        static::addGlobalScope('tenant', function (Builder $builder) {
            $tid = App::bound('current_tenant_id') ? App::make('current_tenant_id') : null;
            if ($tid !== null) {
                $builder->where(static::getTenantColumn(), $tid);
            }
        });

        static::creating(function ($model) {
            $tid = App::bound('current_tenant_id') ? App::make('current_tenant_id') : null;
            if ($tid !== null) {
                $model->{static::getTenantColumn()} = $tid;
            }
        });
    }

    public static function getTenantColumn(): string
    {
        return defined('static::TENANT_COLUMN') ? static::TENANT_COLUMN : 'user_id';
    }
}
"""
    return path, content


def _niche_config(dest: Path, niche: str, cfg: dict) -> tuple:
    """Return (path, content) for config/niche.php."""
    path = dest / "config" / "niche.php"
    features_php = "[\n" + "".join(f"        '{f}',\n" for f in cfg["features"]) + "    ]"
    content = f"""\
<?php
/**
 * Niche configuration — generated by PRINTMAXX
 * Vertical: {niche}
 */
return [
    'niche'            => '{niche}',
    'app_name'         => '{cfg["app_name"]}',
    'description'      => '{cfg["description"]}',
    'color_primary'    => '{cfg["color_primary"]}',
    'plan_name'        => '{cfg["plan_name"]}',
    'plan_price_cents' => {cfg["plan_price_cents"]},
    'features'         => {features_php},
];
"""
    return path, content


def _env_example(dest: Path, niche: str, cfg: dict) -> tuple:
    """Return (path, content) for .env.example."""
    path = dest / ".env.example"
    slug = niche.replace("_", "-")
    content = f"""\
APP_NAME="{cfg['app_name']}"
APP_ENV=production
APP_KEY=
APP_DEBUG=false
APP_URL=https://{slug}-notes.example.com

DB_CONNECTION=mysql
DB_HOST=127.0.0.1
DB_PORT=3306
DB_DATABASE={niche}_notes
DB_USERNAME=
DB_PASSWORD=

STRIPE_KEY=pk_live_
STRIPE_SECRET=sk_live_
STRIPE_WEBHOOK_SECRET=whsec_
STRIPE_PRICE_ID=price_

MAIL_MAILER=smtp
MAIL_HOST=
MAIL_PORT=587
MAIL_USERNAME=
MAIL_PASSWORD=
MAIL_FROM_ADDRESS=noreply@{slug}-notes.example.com
MAIL_FROM_NAME="{cfg['app_name']}"
"""
    return path, content


def _patch_composer_json(dest: Path, dry_run: bool, logger: logging.Logger) -> bool:
    """Inject stripe/stripe-php into composer.json require block."""
    composer_path = dest / "composer.json"
    if dry_run:
        logger.info("[DRY-RUN] would patch: %s", composer_path)
        return True
    if not composer_path.exists():
        logger.warning("composer.json not found at %s — skipping Stripe injection", composer_path)
        return True
    try:
        with open(safe_path(composer_path), "r", encoding="utf-8") as fh:
            data = json.load(fh)
        data.setdefault("require", {})["stripe/stripe-php"] = "^15.0"
        with open(safe_path(composer_path), "w", encoding="utf-8") as fh:
            json.dump(data, fh, indent=4)
        return True
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        logger.error("Failed to patch composer.json at %s: %s", composer_path, exc)
        return False

# ---------------------------------------------------------------------------
# DAG tasks
# ---------------------------------------------------------------------------

def task_preflight(status: dict, logger: logging.Logger, dry_run: bool) -> bool:
    """T01 — verify required system tools are present."""
    task = "T01_preflight"
    if task_done(status, task):
        logger.info("[%s] already done, skipping", task)
        return True
    logger.info("[%s] checking required tools…", task)
    missing = [t for t in ("git", "php", "composer") if run_cmd(["which", t], dry_run=dry_run)[0] != 0]
    if missing and not dry_run:
        detail = f"missing tools: {', '.join(missing)}"
        logger.error("[%s] FAILED — %s", task, detail)
        mark_task(status, task, "failed", detail)
        append_csv_row({"task": task, "niche": "all", "state": "failed", "detail": detail})
        return False
    mark_task(status, task, "done", "all tools present")
    append_csv_row({"task": task, "niche": "all", "state": "done", "detail": "ok"})
    logger.info("[%s] OK", task)
    return True


def task_clone_upstream(status: dict, logger: logging.Logger, dry_run: bool) -> bool:
    """T02 — clone brufdev/many-notes into the build directory."""
    task = "T02_clone_upstream"
    if task_done(status, task):
        logger.info("[%s] already done, skipping", task)
        return True
    logger.info("[%s] cloning upstream…", task)
    target = BUILD_DIR / "upstream"
    if not dry_run:
        target.parent.mkdir(parents=True, exist_ok=True)
        safe_path(target.parent)
    if target.exists() and not dry_run:
        rc, _, err = run_cmd(["git", "pull", "--ff-only"], cwd=target, dry_run=dry_run, logger=logger)
    else:
        rc, _, err = run_cmd(
            ["git", "clone", "--depth=1", UPSTREAM_REPO, str(target)],
            dry_run=dry_run, logger=logger,
        )
    if rc != 0 and not dry_run:
        detail = f"git error: {err}"
        logger.error("[%s] FAILED — %s", task, detail)
        mark_task(status, task, "failed", detail)
        append_csv_row({"task": task, "niche": "all", "state": "failed", "detail": detail})
        return False
    mark_task(status, task, "done", str(target))
    append_csv_row({"task": task, "niche": "all", "state": "done", "detail": str(target)})
    logger.info("[%s] OK → %s", task, target)
    return True


def task_strip_to_core(status: dict, logger: logging.Logger, dry_run: bool) -> bool:
    """T03 — remove non-core dirs / files from the cloned upstream."""
    task = "T03_strip_to_core"
    if task_done(status, task):
        logger.info("[%s] already done, skipping", task)
        return True
    logger.info("[%s] stripping non-core files…", task)
    upstream = BUILD_DIR / "upstream"
    removed = []
    for pattern in STRIP_PATTERNS:
        target = upstream / pattern
        if dry_run:
            logger.info("[DRY-RUN] would remove: %s", target)
            continue
        if not target.exists():
            continue
        try:
            safe_path(target)
        except ValueError as exc:
            logger.error("[%s] path safety violation: %s", task, exc)
            mark_task(status, task, "failed", str(exc))
            return False
        rc, _, err = run_cmd(["rm", "-rf", str(target)], logger=logger)
        if rc == 0:
            removed.append(pattern)
        else:
            logger.warning("[%s] could not remove %s: %s", task, target, err)
    detail = f"removed: {', '.join(removed) or 'none (dry-run or nothing matched)'}"
    mark_task(status, task, "done", detail)
    append_csv_row({"task": task, "niche": "all", "state": "done", "detail": detail})
    logger.info("[%s] OK — %s", task, detail)
    return True


def task_fetch_stripe_sdk_info(status: dict, logger: logging.Logger, dry_run: bool) -> bool:
    """T04 — fetch latest stripe/stripe-php version from Packagist (informational)."""
    task = "T04_fetch_stripe_sdk"
    if task_done(status, task):
        logger.info("[%s] already done, skipping", task)
        return True
    logger.info("[%s] fetching Stripe PHP SDK version from Packagist…", task)
    url = "https://repo.packagist.org/p2/stripe/stripe-php.json"
    if dry_run:
        mark_task(status, task, "done", "dry-run")
        logger.info("[DRY-RUN] would fetch: %s", url)
        return True
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "PRINTMAXX-Automation/1.0"})
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        packages = data.get("packages", {}).get("stripe/stripe-php", [])
        latest = packages[0].get("version", "unknown") if packages else "unknown"
        detail = f"stripe/stripe-php latest={latest}"
        mark_task(status, task, "done", detail)
        append_csv_row({"task": task, "niche": "all", "state": "done", "detail": detail})
        logger.info("[%s] OK — %s", task, detail)
    except (urllib.error.URLError, json.JSONDecodeError, KeyError, IndexError) as exc:
        # Non-fatal: composer will resolve ^15.0 at install time
        detail = f"packagist fetch skipped ({exc}); composer will resolve version"
        logger.warning("[%s] WARNING: %s", task, detail)
        mark_task(status, task, "done", detail)
    return True


def task_generate_niche_variants(status: dict, logger: logging.Logger, dry_run: bool) -> bool:
    """T05 — for each niche, copy upstream + inject Stripe paywall + tenant isolation."""
    task = "T05_generate_niches"
    if task_done(status, task):
        logger.info("[%s] already done, skipping", task)
        return True
    logger.info("[%s] generating niche variants…", task)
    upstream = BUILD_DIR / "upstream"
    failed_niches = []

    for niche, cfg in NICHES.items():
        logger.info("[%s] → niche=%s (%s)", task, niche, cfg["app_name"])
        dest = DEPLOY_DIR / niche

        if not dry_run:
            dest.mkdir(parents=True, exist_ok=True)
            safe_path(dest)
            # Sync upstream into niche deploy dir
            rc, _, err = run_cmd(
                ["rsync", "-a", "--delete", str(upstream) + "/", str(dest) + "/"],
                logger=logger,
            )
            if rc != 0:
                # rsync may not be present; fall back to cp
                rc, _, err = run_cmd(
                    ["cp", "-r", str(upstream) + "/.", str(dest)],
                    logger=logger,
                )
            if rc != 0:
                logger.error("[%s] could not copy upstream to %s: %s", task, dest, err)
                failed_niches.append(niche)
                continue

        # Collect (path, content) pairs for each generated file
        generators = [
            _stripe_paywall_middleware(dest, niche, cfg),
            _billing_controller(dest, niche, cfg),
            _tenant_scope_trait(dest),
            _niche_config(dest, niche, cfg),
            _env_example(dest, niche, cfg),
        ]
        niche_ok = True
        for file_path, file_content in generators:
            if not _write_file(file_path, file_content, dry_run, logger):
                niche_ok = False
                break

        if niche_ok and not _patch_composer_json(dest, dry_run, logger):
            niche_ok = False

        if niche_ok:
            append_csv_row({"task": task, "niche": niche, "state": "done", "detail": str(dest)})
            logger.info("[%s] niche=%s OK → %s", task, niche, dest)
        else:
            failed_niches.append(niche)

    if failed_niches:
        detail = f"failed niches: {', '.join(failed_niches)}"
        logger.error("[%s] PARTIAL FAILURE — %s", task, detail)
        mark_task(status, task, "failed", detail)
        return False

    detail = f"generated: {', '.join(NICHES)}"
    mark_task(status, task, "done", detail)
    logger.info("[%s] OK — %s", task, detail)
    return True


def task_write_deploy_manifest(status: dict, logger: logging.Logger, dry_run: bool) -> bool:
    """T06 — write manifest.json summarising all niche build outputs."""
    task = "T06_deploy_manifest"
    if task_done(status, task):
        logger.info("[%s] already done, skipping", task)
        return True
    logger.info("[%s] writing deploy manifest…", task)
    manifest = {
        "generated_at": datetime.utcnow().isoformat(),
        "upstream_repo": UPSTREAM_REPO,
        "niches": {
            niche: {
                "app_name":         cfg["app_name"],
                "deploy_path":      str(DEPLOY_DIR / niche),
                "plan_name":        cfg["plan_name"],
                "plan_price_cents": cfg["plan_price_cents"],
                "features":         cfg["features"],
                "ready":            (DEPLOY_DIR / niche).exists() or dry_run,
            }
            for niche, cfg in NICHES.items()
        },
    }
    manifest_path = DEPLOY_DIR / "manifest.json"
    if dry_run:
        logger.info("[DRY-RUN] would write manifest → %s", manifest_path)
        mark_task(status, task, "done", "dry-run")
        return True
    try:
        manifest_path.parent.mkdir(parents=True, exist_ok=True)
        with open(safe_path(manifest_path), "w", encoding="utf-8") as fh:
            json.dump(manifest, fh, indent=2)
        mark_task(status, task, "done", str(manifest_path))
        append_csv_row({"task": task, "niche": "all", "state": "done", "detail": str(manifest_path)})
        logger.info("[%s] OK → %s", task, manifest_path)
        return True
    except (OSError, ValueError) as exc:
        detail = str(exc)
        logger.error("[%s] FAILED — %s", task, detail)
        mark_task(status, task, "failed", detail)
        return False


def task_composer_install(status: dict, logger: logging.Logger, dry_run: bool) -> bool:
    """T07 — run `composer install --no-dev` in each niche deploy directory."""
    task = "T07_composer_install"
    if task_done(status, task):
        logger.info("[%s] already done, skipping", task)
        return True
    logger.info("[%s] running composer install for each niche…", task)
    failed = []
    for niche in NICHES:
        dest = DEPLOY_DIR / niche
        if not dest.exists() and not dry_run:
            logger.warning("[%s] deploy dir missing for %s, skipping", task, niche)
            continue
        rc, _, err = run_cmd(
            ["composer", "install", "--no-dev", "--optimize-autoloader", "--no-interaction"],
            cwd=dest, dry_run=dry_run, logger=logger,
        )
        if rc != 0 and not dry_run:
            logger.error("[%s] composer failed for %s: %s", task, niche, err)
            failed.append(niche)
        else:
            append_csv_row({"task": task, "niche": niche, "state": "done", "detail": "composer ok"})
            logger.info("[%s] composer OK for niche=%s", task, niche)
    if failed:
        detail = f"composer failed for: {', '.join(failed)}"
        mark_task(status, task, "failed", detail)
        return False
    mark_task(status, task, "done", "composer install complete for all niches")
    return True


def task_stripe_products_script(status: dict, logger: logging.Logger, dry_run: bool) -> bool:
    """T08 — write a helper shell script that creates Stripe products via the CLI."""
    task = "T08_stripe_products_script"
    if task_done(status, task):
        logger.info("[%s] already done, skipping", task)
        return True
    logger.info("[%s] writing Stripe product-creation helper script…", task)

    lines = [
        "#!/usr/bin/env bash",
        "# Auto-generated by PRINTMAXX — creates Stripe products/prices for all niches",
        "# Requires: stripe CLI (https://stripe.com/docs/stripe-cli), jq",
        "set -euo pipefail",
        "",
    ]
    for niche, cfg in NICHES.items():
        slug = niche.replace("_", "-")
        lines += [
            f"echo '--- creating Stripe product for niche={niche} ---'",
            f"PRODUCT_{niche.upper()}=$(stripe products create \\",
            f"  --name='{cfg['app_name']}' \\",
            f"  --description='{cfg['description']}' \\",
            f"  --metadata[niche]={niche} \\",
            f"  --format=json | jq -r '.id')",
            f'echo "  product_id: ${{{f"PRODUCT_{niche.upper()}"}}}"',
            "",
            f"PRICE_{niche.upper()}=$(stripe prices create \\",
            f"  --product=${{{f'PRODUCT_{niche.upper()}'}}} \\",
            f"  --unit-amount={cfg['plan_price_cents']} \\",
            f"  --currency=usd \\",
            f"  --recurring[interval]=month \\",
            f"  --nickname='{cfg['plan_name']}' \\",
            f"  --format=json | jq -r '.id')",
            f'echo "  STRIPE_PRICE_ID ({niche}): ${{{f"PRICE_{niche.upper()}"}}}"',
            "",
        ]
    lines.append("echo 'Done. Copy each STRIPE_PRICE_ID into the matching niche .env file.'")

    script_content = "\n".join(lines) + "\n"
    script_path = DEPLOY_DIR / "create_stripe_products.sh"

    if dry_run:
        logger.info("[DRY-RUN] would write → %s", script_path)
        mark_task(status, task, "done", "dry-run")
        return True
    try:
        script_path.parent.mkdir(parents=True, exist_ok=True)
        with open(safe_path(script_path), "w", encoding="utf-8") as fh:
            fh.write(script_content)
        script_path.chmod(0o755)
        mark_task(status, task, "done", str(script_path))
        append_csv_row({"task": task, "niche": "all", "state": "done", "detail": str(script_path)})
        logger.info("[%s] OK → %s", task, script_path)
        return True
    except (OSError, ValueError) as exc:
        detail = str(exc)
        logger.error("[%s] FAILED — %s", task, detail)
        mark_task(status, task, "failed", detail)
        return False


# ---------------------------------------------------------------------------
# DAG definition — ordered list; each task must pass before the next runs
# ---------------------------------------------------------------------------
DAG: list = [
    ("T01_preflight",              task_preflight),
    ("T02_clone_upstream",         task_clone_upstream),
    ("T03_strip_to_core",          task_strip_to_core),
    ("T04_fetch_stripe_sdk",       task_fetch_stripe_sdk_info),
    ("T05_generate_niches",        task_generate_niche_variants),
    ("T06_deploy_manifest",        task_write_deploy_manifest),
    ("T07_composer_install",       task_composer_install),
    ("T08_stripe_products_script", task_stripe_products_script),
]


def run_dag(dry_run: bool = False) -> int:
    logger  = setup_logging()
    status  = load_status()
    status["last_run"]  = datetime.utcnow().isoformat()
    status["run_count"] = status.get("run_count", 0) + 1

    run_label = f"run #{status['run_count']}" + (" [DRY-RUN]" if dry_run else "")
    logger.info("=== PRINTMAXX many_notes_niche_deployer START (%s) ===", run_label)

    skills = recall_skills_for_task("many_notes_niche_deployer")
    if skills:
        logger.debug("recalled skills: %s", skills)

    exit_code = 0
    for task_name, task_fn in DAG:
        try:
            ok = task_fn(status, logger, dry_run)
        except Exception as exc:
            logger.exception("unhandled exception in %s: %s", task_name, exc)
            mark_task(status, task_name, "failed", str(exc))
            ok = False
        finally:
            save_status(status)
        if not ok:
            logger.error("DAG halted at %s", task_name)
            exit_code = 1
            break

    overall = "FAILED" if exit_code else "COMPLETE"
    capture_skill_from_result("many_notes_niche_deployer", {"status": overall, "tasks": status["tasks"]})
    logger.info("=== PRINTMAXX many_notes_niche_deployer END — %s ===", overall)
    return exit_code

# ---------------------------------------------------------------------------
# Status printer
# ---------------------------------------------------------------------------

def print_status() -> int:
    setup_logging()
    status = load_status()
    if not status["tasks"]:
        print("No runs recorded yet. Use --run or --dry-run to start.")
        return 0
    print(f"Last run : {status.get('last_run', 'never')}")
    print(f"Run count: {status.get('run_count', 0)}")
    print()
    header = f"{'Task':<38} {'State':<10} {'Updated':<26} Detail"
    print(header)
    print("-" * len(header))
    all_done = True
    for name, info in status["tasks"].items():
        state   = info.get("state", "?")
        updated = info.get("updated", "")
        detail  = info.get("detail", "")[:55]
        marker  = "" if state == "done" else ("! " if state == "failed" else "~ ")
        if state != "done":
            all_done = False
        print(f"{marker}{name:<36} {state:<10} {updated:<26} {detail}")
    print()
    print("Overall:", "COMPLETE" if all_done else "INCOMPLETE / FAILED")
    return 0

# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="many_notes_niche_deployer",
        description=(
            "PRINTMAXX — fork brufdev/many-notes, strip to core, "
            "add Stripe paywall + multi-tenant isolation, "
            "deploy as legal / medical / real-estate note apps."
        ),
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--run",
        action="store_true",
        help="Execute the full deployment DAG",
    )
    group.add_argument(
        "--status",
        action="store_true",
        help="Print current task status and exit",
    )
    group.add_argument(
        "--dry-run",
        dest="dry_run",
        action="store_true",
        help="Simulate the DAG without writing files or running commands",
    )
    return parser


def main() -> None:
    args = build_parser().parse_args()
    if args.status:
        sys.exit(print_status())
    elif args.run:
        sys.exit(run_dag(dry_run=False))
    else:  # --dry-run
        sys.exit(run_dag(dry_run=True))


if __name__ == "__main__":
    main()