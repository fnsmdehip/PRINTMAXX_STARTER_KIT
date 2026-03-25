#!/usr/bin/env python3
"""
PRINTMAXX Automation: saasfly_scaffold
======================================
Scaffold new SaaS products using saasfly as base template.

DAG:
  1. clone repo         – clone nextify-limited/saasfly
  2. strip to core      – remove demo/example content
  3. inject features    – add niche-specific modules and pages
  4. wire payments      – configure Stripe + RevenueCat env vars and stubs
  5. deploy to vercel   – run vercel deploy via CLI
  6. update index       – append entry to app factory index CSV

Usage:
  python3 saasfly_scaffold.py --run --niche "invoice-generator" --slug "invoicemax"
  python3 saasfly_scaffold.py --status
  python3 saasfly_scaffold.py --dry-run --niche "hr-portal" --slug "hrmax"
"""

import argparse
import csv
import json
import logging
import os
import subprocess
import sys
import urllib.request
import urllib.error
from datetime import datetime, timezone
from pathlib import Path

# ---------------------------------------------------------------------------
# _common imports (provided by PRINTMAXX harness)
# ---------------------------------------------------------------------------
try:
    from _common import PROJECT, safe_path, recall_skills_for_task, capture_skill_from_result
except ImportError:
    # Fallback definitions so the script remains runnable standalone
    PROJECT = Path(__file__).resolve().parent.parent

    def safe_path(p: Path) -> Path:
        resolved = Path(p).resolve()
        if not str(resolved).startswith(str(PROJECT.resolve())):
            raise ValueError(f"Path escapes PROJECT root: {resolved}")
        return resolved

    def recall_skills_for_task(task_name: str) -> dict:
        return {}

    def capture_skill_from_result(task_name: str, result: dict) -> None:
        pass

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
AUTOMATIONS_DIR   = safe_path(PROJECT / "AUTOMATIONS")
LOG_DIR           = safe_path(AUTOMATIONS_DIR / "logs")
LOG_FILE          = safe_path(LOG_DIR / "saasfly_scaffold.log")
STATE_FILE        = safe_path(AUTOMATIONS_DIR / "saasfly_scaffold_state.json")
INDEX_CSV         = safe_path(AUTOMATIONS_DIR / "app_factory_index.csv")
BUILDS_DIR        = safe_path(AUTOMATIONS_DIR / "builds")

SAASFLY_REPO      = "https://github.com/nextify-limited/saasfly.git"
SAASFLY_REPO_API  = "https://api.github.com/repos/nextify-limited/saasfly"

INDEX_FIELDNAMES  = ["slug", "niche", "repo_path", "vercel_url", "status", "created_at"]

STRIP_PATTERNS = [
    "apps/web/src/app/(marketing)",
    "apps/web/public/screenshots",
    "apps/web/content",
    ".github/FUNDING.yml",
]

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------

def _setup_logging() -> logging.Logger:
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    logger = logging.getLogger("saasfly_scaffold")
    logger.setLevel(logging.DEBUG)
    if not logger.handlers:
        fh = logging.FileHandler(str(LOG_FILE), mode="a", encoding="utf-8")
        fh.setLevel(logging.DEBUG)
        fmt = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s",
                                datefmt="%Y-%m-%dT%H:%M:%SZ")
        fh.setFormatter(fmt)
        logger.addHandler(fh)
        sh = logging.StreamHandler(sys.stdout)
        sh.setLevel(logging.INFO)
        sh.setFormatter(fmt)
        logger.addHandler(sh)
    return logger

log = _setup_logging()

# ---------------------------------------------------------------------------
# State helpers
# ---------------------------------------------------------------------------

def _load_state() -> dict:
    if STATE_FILE.exists():
        try:
            with STATE_FILE.open("r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError) as exc:
            log.warning("Could not load state file: %s", exc)
    return {"runs": []}


def _save_state(state: dict) -> None:
    safe_path(STATE_FILE.parent).mkdir(parents=True, exist_ok=True)
    with safe_path(STATE_FILE).open("w", encoding="utf-8") as f:
        json.dump(state, f, indent=2)


def _record_run(state: dict, slug: str, niche: str, status: str,
                vercel_url: str = "", notes: str = "") -> None:
    state.setdefault("runs", []).append({
        "slug":       slug,
        "niche":      niche,
        "status":     status,
        "vercel_url": vercel_url,
        "notes":      notes,
        "timestamp":  datetime.now(timezone.utc).isoformat(),
    })

# ---------------------------------------------------------------------------
# Utility
# ---------------------------------------------------------------------------

def _run_cmd(cmd: list[str], cwd: Path | None = None, dry_run: bool = False,
             check: bool = True) -> subprocess.CompletedProcess:
    """Run a shell command, honouring dry-run mode."""
    cwd_str = str(cwd) if cwd else None
    log.debug("CMD%s: %s (cwd=%s)", " [DRY]" if dry_run else "", " ".join(cmd), cwd_str)
    if dry_run:
        return subprocess.CompletedProcess(cmd, returncode=0, stdout=b"", stderr=b"")
    result = subprocess.run(cmd, cwd=cwd_str, capture_output=True, text=True)
    if result.stdout:
        log.debug("STDOUT: %s", result.stdout.strip())
    if result.stderr:
        log.debug("STDERR: %s", result.stderr.strip())
    if check and result.returncode != 0:
        raise subprocess.CalledProcessError(result.returncode, cmd,
                                            result.stdout, result.stderr)
    return result


def _fetch_json(url: str) -> dict:
    req = urllib.request.Request(url, headers={"User-Agent": "PRINTMAXX/1.0"})
    with urllib.request.urlopen(req, timeout=15) as resp:
        return json.loads(resp.read().decode("utf-8"))


def _write_file(path: Path, content: str, dry_run: bool = False) -> None:
    validated = safe_path(path)
    log.debug("WRITE%s: %s", " [DRY]" if dry_run else "", validated)
    if dry_run:
        return
    validated.parent.mkdir(parents=True, exist_ok=True)
    with validated.open("w", encoding="utf-8") as f:
        f.write(content)

# ---------------------------------------------------------------------------
# DAG steps
# ---------------------------------------------------------------------------

def step_clone(slug: str, build_dir: Path, dry_run: bool) -> Path:
    """Step 1 – Clone saasfly into builds/<slug>."""
    log.info("[1/6] Cloning saasfly → %s", build_dir)
    if build_dir.exists() and not dry_run:
        log.warning("Build dir already exists, skipping clone: %s", build_dir)
        return build_dir
    BUILDS_DIR.mkdir(parents=True, exist_ok=True)
    _run_cmd(["git", "clone", "--depth=1", SAASFLY_REPO, str(build_dir)], dry_run=dry_run)
    log.info("[1/6] Clone complete.")
    return build_dir


def step_strip_to_core(build_dir: Path, dry_run: bool) -> None:
    """Step 2 – Remove demo/marketing content from the clone."""
    log.info("[2/6] Stripping demo content from %s", build_dir)
    for pattern in STRIP_PATTERNS:
        target = build_dir / pattern
        log.debug("Removing (if exists): %s", target)
        if not dry_run and target.exists():
            _run_cmd(["rm", "-rf", str(target)], dry_run=False)
    log.info("[2/6] Strip complete.")


def step_inject_features(build_dir: Path, slug: str, niche: str,
                         dry_run: bool) -> None:
    """Step 3 – Inject niche-specific feature stubs."""
    log.info("[3/6] Injecting niche features for '%s' (%s)", niche, slug)

    feature_dir = build_dir / "apps" / "web" / "src" / "features" / slug
    index_content = f"""\
// Auto-generated by PRINTMAXX saasfly_scaffold
// Niche: {niche}  |  Slug: {slug}

export const NICHE = "{niche}";
export const SLUG  = "{slug}";

export async function coreWorkflow() {{
  // TODO: implement {niche} core workflow
  throw new Error("coreWorkflow() not yet implemented for {niche}");
}}
"""
    _write_file(safe_path(feature_dir / "index.ts"), index_content, dry_run)

    page_content = f"""\
import {{ coreWorkflow }} from "@/features/{slug}";

export default function {slug.replace("-", "_").capitalize()}Page() {{
  return (
    <main>
      <h1>{niche}</h1>
      {{/* TODO: build {niche} UI */}}
    </main>
  );
}}
"""
    _write_file(
        safe_path(build_dir / "apps" / "web" / "src" / "app" / "(dashboard)" / slug / "page.tsx"),
        page_content,
        dry_run,
    )
    log.info("[3/6] Feature injection complete.")


def step_wire_payments(build_dir: Path, slug: str, dry_run: bool) -> None:
    """Step 4 – Wire Stripe + RevenueCat env var stubs and config."""
    log.info("[4/6] Wiring Stripe + RevenueCat for %s", slug)

    env_example = safe_path(build_dir / ".env.example")
    additions = f"""
# ---- PRINTMAXX: {slug} payment config ----
STRIPE_SECRET_KEY=sk_test_REPLACE_ME
STRIPE_WEBHOOK_SECRET=whsec_REPLACE_ME
STRIPE_PRICE_ID_MONTHLY=price_REPLACE_ME
STRIPE_PRICE_ID_ANNUAL=price_REPLACE_ME
REVENUECAT_API_KEY=REPLACE_ME
REVENUECAT_ENTITLEMENT_ID=pro
# ---- end PRINTMAXX ----
"""
    if not dry_run:
        current = env_example.read_text(encoding="utf-8") if env_example.exists() else ""
        if "PRINTMAXX" not in current:
            with safe_path(env_example).open("a", encoding="utf-8") as f:
                f.write(additions)
    else:
        log.debug("DRY: would append payment env vars to %s", env_example)

    payments_content = """\
// Auto-generated by PRINTMAXX saasfly_scaffold
import Stripe from "stripe";

export const stripe = new Stripe(process.env.STRIPE_SECRET_KEY!, {
  apiVersion: "2024-06-20",
});

export async function createCheckoutSession(priceId: string, userId: string) {
  return stripe.checkout.sessions.create({
    mode: "subscription",
    line_items: [{ price: priceId, quantity: 1 }],
    success_url: `${process.env.NEXT_PUBLIC_APP_URL}/dashboard?session_id={CHECKOUT_SESSION_ID}`,
    cancel_url:  `${process.env.NEXT_PUBLIC_APP_URL}/pricing`,
    metadata: { userId },
  });
}

export async function getRevenueCatEntitlement(userId: string): Promise<boolean> {
  const apiKey = process.env.REVENUECAT_API_KEY!;
  const res = await fetch(`https://api.revenuecat.com/v1/subscribers/${userId}`, {
    headers: { Authorization: `Bearer ${apiKey}` },
  });
  if (!res.ok) return false;
  const data = await res.json();
  const entitlement = process.env.REVENUECAT_ENTITLEMENT_ID ?? "pro";
  return !!data?.subscriber?.entitlements?.[entitlement]?.expires_date;
}
"""
    _write_file(
        safe_path(build_dir / "apps" / "web" / "src" / "lib" / "payments.ts"),
        payments_content,
        dry_run,
    )
    log.info("[4/6] Payment wiring complete.")


def step_deploy_vercel(build_dir: Path, slug: str,
                       dry_run: bool) -> str:
    """Step 5 – Deploy to Vercel and return the deployment URL."""
    log.info("[5/6] Deploying %s to Vercel", slug)
    result = _run_cmd(
        ["npx", "vercel", "--prod", "--yes", "--name", slug],
        cwd=build_dir / "apps" / "web",
        dry_run=dry_run,
    )
    if dry_run:
        vercel_url = f"https://{slug}.vercel.app (dry-run)"
    else:
        # Vercel CLI prints the URL on the last non-empty line of stdout
        lines = [ln.strip() for ln in result.stdout.splitlines() if ln.strip()]
        vercel_url = lines[-1] if lines else f"https://{slug}.vercel.app"
    log.info("[5/6] Deployed: %s", vercel_url)
    return vercel_url


def step_update_index(slug: str, niche: str, build_dir: Path,
                      vercel_url: str, dry_run: bool) -> None:
    """Step 6 – Append a row to the app factory index CSV."""
    log.info("[6/6] Updating app factory index at %s", INDEX_CSV)
    row = {
        "slug":       slug,
        "niche":      niche,
        "repo_path":  str(build_dir),
        "vercel_url": vercel_url,
        "status":     "deployed" if not dry_run else "dry-run",
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    if dry_run:
        log.debug("DRY: would append to index: %s", row)
        return
    write_header = not INDEX_CSV.exists()
    INDEX_CSV.parent.mkdir(parents=True, exist_ok=True)
    with safe_path(INDEX_CSV).open("a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=INDEX_FIELDNAMES)
        if write_header:
            writer.writeheader()
        writer.writerow(row)
    log.info("[6/6] Index updated.")

# ---------------------------------------------------------------------------
# High-level run / status
# ---------------------------------------------------------------------------

def run_dag(slug: str, niche: str, dry_run: bool) -> None:
    """Execute the full saasfly scaffold DAG."""
    log.info("=== saasfly_scaffold START  slug=%s  niche=%s  dry=%s ===",
             slug, niche, dry_run)

    skills = recall_skills_for_task("saasfly_scaffold")
    if skills:
        log.debug("Recalled skills: %s", skills)

    state = _load_state()
    build_dir = safe_path(BUILDS_DIR / slug)

    try:
        step_clone(slug, build_dir, dry_run)
        step_strip_to_core(build_dir, dry_run)
        step_inject_features(build_dir, slug, niche, dry_run)
        step_wire_payments(build_dir, slug, dry_run)
        vercel_url = step_deploy_vercel(build_dir, slug, dry_run)
        step_update_index(slug, niche, build_dir, vercel_url, dry_run)

        _record_run(state, slug, niche, "success", vercel_url)
        _save_state(state)

        result = {"slug": slug, "niche": niche, "vercel_url": vercel_url, "status": "success"}
        capture_skill_from_result("saasfly_scaffold", result)

        log.info("=== saasfly_scaffold COMPLETE  url=%s ===", vercel_url)

    except subprocess.CalledProcessError as exc:
        msg = f"Subprocess failed (rc={exc.returncode}): {exc.cmd}"
        log.error(msg)
        _record_run(state, slug, niche, "error", notes=msg)
        _save_state(state)
        sys.exit(1)
    except ValueError as exc:
        log.error("Path safety violation: %s", exc)
        _record_run(state, slug, niche, "error", notes=str(exc))
        _save_state(state)
        sys.exit(1)
    except urllib.error.URLError as exc:
        log.error("Network error: %s", exc)
        _record_run(state, slug, niche, "error", notes=str(exc))
        _save_state(state)
        sys.exit(1)
    except Exception as exc:  # noqa: BLE001
        log.error("Unexpected error: %s", exc, exc_info=True)
        _record_run(state, slug, niche, "error", notes=str(exc))
        _save_state(state)
        sys.exit(1)


def show_status() -> None:
    """Print a summary of all previous runs."""
    state = _load_state()
    runs = state.get("runs", [])
    if not runs:
        print("No runs recorded yet.")
        return
    print(f"{'TIMESTAMP':<28} {'SLUG':<24} {'NICHE':<30} {'STATUS':<12} URL")
    print("-" * 110)
    for r in runs:
        print(f"{r.get('timestamp',''):<28} {r.get('slug',''):<24} "
              f"{r.get('niche',''):<30} {r.get('status',''):<12} "
              f"{r.get('vercel_url','')}")

    if INDEX_CSV.exists():
        print(f"\nApp factory index: {INDEX_CSV}")
        with INDEX_CSV.open("r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            rows = list(reader)
        print(f"  {len(rows)} product(s) indexed.")

# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="PRINTMAXX: scaffold a SaaS product from saasfly template",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--run",     action="store_true", help="Execute the scaffold DAG")
    mode.add_argument("--status",  action="store_true", help="Show status of previous runs")
    mode.add_argument("--dry-run", action="store_true", dest="dry_run",
                      help="Simulate without writing files or deploying")

    parser.add_argument("--slug",  default="",
                        help="URL-safe product identifier, e.g. invoicemax")
    parser.add_argument("--niche", default="",
                        help="Human-readable niche, e.g. 'invoice-generator'")
    return parser


def main() -> None:
    parser = _build_parser()
    args = parser.parse_args()

    if args.status:
        show_status()
        sys.exit(0)

    if args.run or args.dry_run:
        if not args.slug:
            parser.error("--slug is required with --run / --dry-run")
        if not args.niche:
            parser.error("--niche is required with --run / --dry-run")
        slug  = args.slug.strip().lower().replace(" ", "-")
        niche = args.niche.strip()
        run_dag(slug, niche, dry_run=args.dry_run)


if __name__ == "__main__":
    main()