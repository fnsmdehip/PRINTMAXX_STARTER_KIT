#!/usr/bin/env python3
"""PRINTMAXX Ship Captain.

Runs non-critical execution automatically and gates critical actions behind
explicit human approvals (human-in-loop).
"""

from __future__ import annotations

import argparse
import concurrent.futures
import csv
import fcntl
import json
import os
import shlex
import subprocess
import threading
import time
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Dict, Iterable, List, Tuple, Optional


BASE_DIR = Path(__file__).resolve().parent.parent
LOG_DIR = BASE_DIR / "logs"
OPS_DIR = BASE_DIR / "OPS"
LEDGER_DIR = BASE_DIR / "LEDGER"
SECRETS_FILE = BASE_DIR / "SECRETS" / "PAYMENT_INFO.md"

RUNS_CSV = LEDGER_DIR / "SHIP_CAPTAIN_RUNS.csv"
QUEUE_MD = OPS_DIR / "HUMAN_LOOP_QUEUE.md"
APPROVALS_CSV = OPS_DIR / "HUMAN_APPROVALS.csv"
POLICY_JSON = OPS_DIR / "STACK_POLICY.json"
NODE_ROLE_JSON = OPS_DIR / "NODE_ROLE.json"
RUN_LOG = LOG_DIR / "ship_captain.log"
LOCK_FILE = LOG_DIR / "ship_captain.lock"

REQUIRED_REVENUE_ACCOUNTS = [
    "Gumroad",
    "eBay",
    "Etsy",
    "Redbubble",
    "Amazon",
]

ACTIVE_STATUSES = {"ACTIVE", "CREATED", "READY"}
ACCOUNT_SECRET_KEYS = {
    "stripe": ["STRIPE_ACCOUNT_ID"],
    "gumroad": ["GUMROAD_EMAIL", "GUMROAD_ACCESS_TOKEN"],
    # Email infra is checked separately (Gmail/Resend + CAN-SPAM address).
}

# Only export these secret keys into subprocess env (avoid spraying passwords).
EXPORT_SECRET_ENV_KEYS = {
    "VERCEL_TOKEN",
    "SURGE_TOKEN",
    "SURGE_LOGIN",
    "NETLIFY_AUTH_TOKEN",
    "GUMROAD_ACCESS_TOKEN",
}

_LOG_LOCK = threading.Lock()
_RUNS_LOCK = threading.Lock()


@dataclass
class Step:
    step_id: str
    name: str
    command: str
    timeout_sec: int = 600
    critical_key: str = ""
    inject_secrets_env: bool = False


AUTO_STEPS: List[Step] = [
    Step("stack_health", "Runtime stack heartbeat", "python3 AUTOMATIONS/stack_governor.py --heartbeat", 120),
    Step("preflight_status", "Account status snapshot", "python3 scripts/account_tracker.py status", 120),
    Step("preflight_blockers", "Revenue blockers snapshot", "python3 scripts/account_tracker.py blockers", 120),

    # Research ingest -> alpha -> ops (runs continuously but throttled).
    Step("alpha_staging_migrate", "Normalize ALPHA_STAGING schema (if needed)", "python3 AUTOMATIONS/alpha_staging_migrate.py", 180),
    Step(
        "x_ingest_copy_style",
        "X ingest (copy-style handles, last 30 days)",
        "python3 AUTOMATIONS/net_guard.py --key x_ingest_copy_style --min-interval-sec 86400 --host x.com -- python3 AUTOMATIONS/twitter_copy_style_ingest.py --days 30 --max-scrolls 25",
        1800,
    ),
    Step(
        "alpha_monitor",
        "Alpha monitor (Reddit + RSS) (best effort)",
        "python3 AUTOMATIONS/net_guard.py --key alpha_monitor --min-interval-sec 21600 --host www.reddit.com -- python3 AUTOMATIONS/alpha_monitor.py --cron",
        900,
    ),
    Step(
        "unified_alpha_monitor",
        "Unified alpha monitor (best effort)",
        "python3 AUTOMATIONS/net_guard.py --key unified_alpha_monitor --min-interval-sec 86400 --host github.com -- python3 AUTOMATIONS/unified_alpha_monitor.py --full",
        1800,
    ),
    Step("alpha_autoapprove", "Auto-approve safe alpha (whitelist sources)", "python3 AUTOMATIONS/alpha_auto_approver.py --tick --max 50", 240),
    Step("alpha_to_ops", "Alpha -> ops generator", "python3 AUTOMATIONS/alpha_to_ops.py --process", 1800),
    Step(
        "triggering_events",
        "Triggering events monitor (hiring/filing/news) (best effort)",
        "python3 AUTOMATIONS/net_guard.py --key triggering_events --min-interval-sec 21600 --host efts.sec.gov -- python3 AUTOMATIONS/triggering_events_monitor.py",
        1200,
    ),
    Step(
        "clawdbot_rbi",
        "Clawdbot-style RBI growth queues (safe draft mode)",
        "python3 AUTOMATIONS/clawdbot_rbi_engine.py --tick --max-intents 180 --max-syndication 420 --max-directories 900 --max-jobs 200 --max-keywords 260 --max-community 180",
        600,
    ),

    # Revenue engines that do not require social accounts (no posting/bidding/sending).
    Step(
        "ecom_arb_scan",
        "Ecom arb scan (best effort)",
        "python3 AUTOMATIONS/net_guard.py --key ecom_arb_scan --min-interval-sec 21600 --host www.amazon.com -- python3 AUTOMATIONS/ecom_arb_engine.py --hourly --top 2",
        900,
    ),
    Step(
        "arb_listings",
        "Generate arb listing drafts (copy/paste)",
        "python3 AUTOMATIONS/arb_listing_generator.py --generate --min-margin 30 --action LIST --top 5 --platform ebay",
        240,
    ),
    Step(
        "ecom_autopilot",
        "Ecom winner selection + platform queue build",
        "python3 AUTOMATIONS/ecom_autopilot.py --tick --top 12 --min-margin 20 --min-profit 3",
        240,
    ),
    Step(
        "ecom_distribution",
        "Ecom multi-platform distribution matrix",
        "python3 AUTOMATIONS/ecom_distributor.py --distribute-all",
        240,
    ),
    Step("ecom_pack", "Write ecom execution pack", "python3 AUTOMATIONS/ecom_packager.py --write", 120),
    Step("gumroad_autolist_pack", "Write Gumroad auto-list status pack", "python3 AUTOMATIONS/gumroad_autolist_packager.py --write", 120),

    Step(
        "freelance_scan",
        "Freelance demand scan (best effort)",
        "python3 AUTOMATIONS/net_guard.py --key freelance_scan --min-interval-sec 7200 --host reddit.com -- python3 AUTOMATIONS/freelance_demand_scanner.py --hourly",
        900,
    ),
    Step(
        "freelance_drafts",
        "Freelance response drafts (dry run)",
        "python3 AUTOMATIONS/auto_freelance_responder.py --dry-run",
        300,
    ),
    Step("freelance_pack", "Write freelance execution pack", "python3 AUTOMATIONS/freelance_packager.py --write", 120),
    Step(
        "clawwork_sidecar",
        "ClawWork economic sidecar benchmark (budget-guarded)",
        "python3 AUTOMATIONS/clawwork_sidecar.py --tick",
        180,
    ),
    Step(
        "master_ops_enhance",
        "Refresh enhanced Master Ops workbook from live runtime signals",
        "python3 AUTOMATIONS/master_ops_enhancer.py",
        240,
    ),
    Step(
        "master_ops_exec_plan",
        "Plan Master Ops execution queue (safe dry run)",
        "python3 AUTOMATIONS/master_ops_executor.py --top 12 --max-per-lane 3",
        240,
    ),

    Step(
        "gov_monitor",
        "Gov contract monitor (SAM.gov) (best effort)",
        "python3 AUTOMATIONS/net_guard.py --key gov_monitor --min-interval-sec 21600 --host api.sam.gov -- python3 AUTOMATIONS/sam_gov_monitor.py --limit 10",
        900,
    ),
    Step("gov_pack", "Write gov bid pack", "python3 AUTOMATIONS/gov_bid_packager.py --write", 120),

    Step("carousel_factory", "Generate daily carousels (AI influencer)", "python3 AUTOMATIONS/carousel_factory.py --tick", 240),
    Step("calendar", "Generate 30-day calendar", "python3 scripts/generate_30day_calendar.py", 180),
    Step("buffer_csv", "Generate Buffer CSVs", "python3 scripts/generate_buffer_csvs.py", 240),
    Step("qa_router", "Route content to QA queue", "python3 scripts/content_to_qa_router.py", 180),
    Step("qa_autoapprove", "Auto-approve low-risk QA items", "python3 AUTOMATIONS/qa_auto_approver.py --tick --max 10", 240),
    Step("publish_pack", "Generate publish packs from approved QA", "python3 AUTOMATIONS/publish_pack.py --tick --max 20", 240),

    Step("app_pack", "Package apps (screenshots + launch meta)", "python3 AUTOMATIONS/app_packager.py --write", 900),
    Step("native_apps_pack", "Package native apps (no submit)", "python3 AUTOMATIONS/native_app_packager.py --write", 900),
    Step(
        "deploy_guard",
        "Auto-deploy (no-cost) if artifacts changed",
        "python3 AUTOMATIONS/deploy_guard.py --tick",
        1800,
        inject_secrets_env=True,
    ),
    Step("launch_pack", "Package launch directories + tracker", "python3 AUTOMATIONS/launch_directory_packager.py --write", 240),

    Step("human_brief", "Write human execution brief", "python3 AUTOMATIONS/human_brief.py --write", 120),
    Step("rbi_daily", "Run RBI daily audit", "python3 scripts/rbi_audit.py daily", 300),
    Step("rbi_portfolio", "Run RBI portfolio optimizer", "python3 AUTOMATIONS/rbi_portfolio_optimizer.py --tick", 240),
    Step("compliance", "Run compliance scan", "python3 AUTOMATIONS/compliance_scanner.py --audit-all --save --no-fail", 900),
    Step("cluely_pack", "Generate disclosure + legal pages for builds", "python3 AUTOMATIONS/cluely_compliance_pack.py --apply", 240),
    Step("cron_fleet", "Cron fleet truth report", "python3 AUTOMATIONS/cron_fleet_report.py --write", 120),
    Step("dashboard", "Refresh dashboard", "python3 AUTOMATIONS/refresh_dashboard.py --no-open", 300),
    Step("memory", "Refresh memory layers", "python3 AUTOMATIONS/memory_manager.py --full", 300),
    Step("cron_status", "Orchestrator status snapshot", "bash ./printmaxx_cron.sh status", 300),
    Step(
        "email_preview",
        "Cold email preview batch (dry run)",
        "python3 AUTOMATIONS/email_sender.py --preview --outreach AUTOMATIONS/outreach/HOT_BATCH_FEB13_COMPLIANT.csv --max-sends 25",
        300,
    ),
]

CRITICAL_STEPS: List[Step] = [
    Step(
        "auto_list_ecom",
        "Auto-list seed ecom products (Gumroad API)",
        "python3 AUTOMATIONS/gumroad_auto_list.py --apply --max 10",
        timeout_sec=1800,
        critical_key="AUTO_LIST_ECOM",
        inject_secrets_env=True,
    ),
    Step(
        "live_send",
        "Live cold email send batch",
        "python3 AUTOMATIONS/email_sender.py --outreach AUTOMATIONS/outreach/HOT_BATCH_FEB13_COMPLIANT.csv --max-sends 100",
        timeout_sec=3600,
        critical_key="LIVE_EMAIL_SEND",
        inject_secrets_env=True,
    ),
]

POST_CRITICAL_STEPS: List[Step] = [
    Step("post_gumroad_autolist_pack", "Post: refresh Gumroad auto-list status", "python3 AUTOMATIONS/gumroad_autolist_packager.py --write", 120),
    Step("post_launch_pack", "Post: refresh launch packs", "python3 AUTOMATIONS/launch_directory_packager.py --write", 240),
    Step("post_dashboard", "Post: refresh dashboard", "python3 AUTOMATIONS/refresh_dashboard.py --no-open", 300),
    Step("post_memory", "Post: refresh memory layers", "python3 AUTOMATIONS/memory_manager.py --full", 300),
]


def ensure_dirs() -> None:
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    OPS_DIR.mkdir(parents=True, exist_ok=True)
    LEDGER_DIR.mkdir(parents=True, exist_ok=True)


def now_iso() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def append_log(line: str) -> None:
    stamped = f"[{now_iso()}] {line}"
    # Multiple lanes may log concurrently in swarm mode.
    with _LOG_LOCK:
        with open(RUN_LOG, "a", encoding="utf-8") as f:
            f.write(stamped + "\n")
        # Also emit to stdout so cron output isn't empty and can be tailed live.
        try:
            print(stamped, flush=True)
        except Exception:
            pass


def ensure_runs_csv() -> None:
    if RUNS_CSV.exists():
        return
    with open(RUNS_CSV, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["timestamp", "step_id", "step_name", "status", "duration_sec", "notes"])


def ensure_approvals_csv() -> None:
    if APPROVALS_CSV.exists():
        return
    with open(APPROVALS_CSV, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["key", "status", "updated_at", "notes"])


def load_policy() -> Dict[str, object]:
    default_policy: Dict[str, object] = {
        "risk": {
            "high_compliance_critical_threshold": 1,
            "required_approval_key": "COMPLIANCE_HIGH_RISK",
        }
    }
    if not POLICY_JSON.exists():
        return default_policy
    try:
        with open(POLICY_JSON, "r", encoding="utf-8") as f:
            data = json.load(f)
        if not isinstance(data, dict):
            return default_policy
        risk = data.get("risk")
        if isinstance(risk, dict):
            merged = default_policy["risk"].copy()
            merged.update(risk)
            data["risk"] = merged
        else:
            data["risk"] = default_policy["risk"]
        return data
    except Exception:
        return default_policy


def load_node_role() -> str:
    default_role = "control"
    if not NODE_ROLE_JSON.exists():
        return default_role
    try:
        with open(NODE_ROLE_JSON, "r", encoding="utf-8") as f:
            payload = json.load(f)
        role = str(payload.get("role", default_role)).strip().lower()
        if role in {"control", "worker"}:
            return role
    except Exception:
        return default_role
    return default_role


def latest_compliance_counts() -> Dict[str, object]:
    files = sorted(LEDGER_DIR.glob("compliance_scan_*.json"))
    result: Dict[str, object] = {
        "file": "",
        "critical": 0,
        "warning": 0,
        "info": 0,
        "total": 0,
    }
    if not files:
        return result

    path = files[-1]
    result["file"] = str(path.relative_to(BASE_DIR))
    try:
        with open(path, "r", encoding="utf-8") as f:
            payload = json.load(f)
    except Exception:
        return result

    issues = payload if isinstance(payload, list) else payload.get("issues", [])
    if not isinstance(issues, list):
        return result

    for item in issues:
        if not isinstance(item, dict):
            continue
        sev = str(item.get("severity", "")).strip().upper()
        if sev == "CRITICAL":
            result["critical"] += 1
        elif sev == "WARNING":
            result["warning"] += 1
        else:
            result["info"] += 1
    result["total"] = result["critical"] + result["warning"] + result["info"]
    return result


def load_persistent_approvals() -> set[str]:
    if not APPROVALS_CSV.exists():
        return set()
    approved: set[str] = set()
    with open(APPROVALS_CSV, "r", newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            key = (row.get("key") or "").strip().upper()
            status = (row.get("status") or "").strip().upper()
            if key and status in {"APPROVED", "YES", "TRUE", "ACTIVE"}:
                approved.add(key)
    return approved


def upsert_persistent_approvals(approve: set[str], revoke: set[str]) -> None:
    ensure_approvals_csv()
    rows: Dict[str, Dict[str, str]] = {}

    with open(APPROVALS_CSV, "r", newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            key = (row.get("key") or "").strip().upper()
            if key:
                rows[key] = {
                    "key": key,
                    "status": (row.get("status") or "").strip() or "PENDING",
                    "updated_at": (row.get("updated_at") or "").strip(),
                    "notes": (row.get("notes") or "").strip(),
                }

    for key in sorted(approve):
        if not key:
            continue
        rows[key] = {
            "key": key,
            "status": "APPROVED",
            "updated_at": now_iso(),
            "notes": "approved via CLI",
        }

    for key in sorted(revoke):
        if not key:
            continue
        rows[key] = {
            "key": key,
            "status": "REVOKED",
            "updated_at": now_iso(),
            "notes": "revoked via CLI",
        }

    with open(APPROVALS_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["key", "status", "updated_at", "notes"])
        writer.writeheader()
        for key in sorted(rows):
            writer.writerow(rows[key])


def acquire_run_lock():
    lock_handle = open(LOCK_FILE, "w", encoding="utf-8")
    try:
        fcntl.flock(lock_handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError:
        lock_handle.close()
        return None
    lock_handle.write(f"pid={os.getpid()} started_at={now_iso()}\n")
    lock_handle.flush()
    return lock_handle


def sanitize_notes(notes: str, limit: int = 500) -> str:
    # Keep CSV one-line-per-record even when subprocess output has newlines.
    s = (notes or "").replace("\r\n", "\n").replace("\r", "\n").replace("\x00", "")
    s = s.replace("\n", "\\n")
    return s[:limit]


def record_run(step: Step, status: str, duration_sec: float, notes: str = "") -> None:
    # Multiple lanes may record concurrently in swarm mode.
    with _RUNS_LOCK:
        with open(RUNS_CSV, "a", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow([now_iso(), step.step_id, step.name, status, int(duration_sec), sanitize_notes(notes, 500)])


def run_step(step: Step) -> Tuple[str, str, float]:
    append_log(f"RUN {step.step_id}: {step.command}")
    start = time.time()
    try:
        env = build_env_for_step(step)
        proc = subprocess.run(
            ["bash", "-lc", step.command],
            cwd=BASE_DIR,
            capture_output=True,
            text=True,
            timeout=step.timeout_sec,
            check=False,
            env=env,
        )
        duration = time.time() - start
        out = (proc.stdout or "") + ("\n" + proc.stderr if proc.stderr else "")
        status = "OK" if proc.returncode == 0 else "FAILED"
        # net_guard intentionally returns 0 on skip so cron runs don't look broken.
        # Detect that case and surface it as SKIPPED for dashboards/ledgers.
        if status == "OK":
            o = out.strip()
            if o.startswith("net_guard:") and "Skipping:" in o:
                status = "SKIPPED"
        append_log(f"DONE {step.step_id}: {status} ({int(duration)}s)")
        return status, out.strip(), duration
    except subprocess.TimeoutExpired:
        duration = time.time() - start
        append_log(f"TIMEOUT {step.step_id} ({int(duration)}s)")
        return "TIMEOUT", f"Timed out after {step.timeout_sec}s", duration


def load_accounts() -> Dict[str, str]:
    path = LEDGER_DIR / "ACCOUNTS.csv"
    if not path.exists():
        return {}
    accounts: Dict[str, str] = {}
    with open(path, "r", encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            platform = (row.get("Platform") or "").strip()
            status = (row.get("Status") or "").strip().upper()
            if platform:
                accounts[platform.lower()] = status
    return accounts


def load_secret_presence() -> Dict[str, bool]:
    values: Dict[str, bool] = {}
    if not SECRETS_FILE.exists():
        return values
    try:
        with open(SECRETS_FILE, "r", encoding="utf-8") as f:
            for raw in f:
                line = raw.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                key, value = line.split("=", 1)
                k = key.strip().upper()
                v = value.strip()
                if k:
                    values[k] = bool(v)
    except Exception:
        return values
    return values


def load_secrets_kv() -> Dict[str, str]:
    if not SECRETS_FILE.exists():
        return {}
    kv: Dict[str, str] = {}
    try:
        with open(SECRETS_FILE, "r", encoding="utf-8") as f:
            for raw in f:
                line = raw.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                key, value = line.split("=", 1)
                k = key.strip().upper()
                v = value.strip()
                if k:
                    kv[k] = v
    except Exception:
        return {}
    return kv


def build_env_for_step(step: Step) -> Optional[Dict[str, str]]:
    if not step.inject_secrets_env:
        return None
    kv = load_secrets_kv()
    env = os.environ.copy()
    for k in EXPORT_SECRET_ENV_KEYS:
        v = (kv.get(k) or "").strip()
        if v:
            env[k] = v
    return env


def email_infra_ready(secrets: Dict[str, bool]) -> bool:
    # CAN-SPAM: require a physical address for any live sends.
    has_phys = bool(secrets.get("PHYSICAL_ADDRESS"))
    gmail_ok = bool(secrets.get("GMAIL_ADDRESS")) and bool(secrets.get("GMAIL_APP_PASSWORD"))
    resend_ok = bool(secrets.get("RESEND_API_KEY")) and bool(secrets.get("RESEND_FROM_EMAIL"))
    return has_phys and (gmail_ok or resend_ok)


def account_ready(platform: str, accounts: Dict[str, str], secrets: Dict[str, bool]) -> bool:
    status = accounts.get(platform.lower(), "")
    if is_active(status):
        return True
    required = ACCOUNT_SECRET_KEYS.get(platform.lower(), [])
    return any(secrets.get(k, False) for k in required)


def is_active(status: str) -> bool:
    return status.strip().upper() in ACTIVE_STATUSES


def has_deploy_auth() -> bool:
    if os.environ.get("VERCEL_TOKEN") or os.environ.get("SURGE_TOKEN") or os.environ.get("NETLIFY_AUTH_TOKEN"):
        return True
    secrets = load_secret_presence()
    if secrets.get("VERCEL_TOKEN") or secrets.get("SURGE_TOKEN") or secrets.get("NETLIFY_AUTH_TOKEN"):
        return True
    checks = [
        ("vercel whoami", "Vercel"),
        ("surge whoami", "Surge"),
        ("netlify status", "Netlify"),
    ]
    for command, _name in checks:
        try:
            proc = subprocess.run(
                ["bash", "-lc", command],
                cwd=BASE_DIR,
                capture_output=True,
                text=True,
                timeout=20,
                check=False,
            )
            if proc.returncode == 0:
                return True
        except Exception:
            continue
    return False


def build_human_queue(approvals_needed: Iterable[Tuple[str, str]], approved: set[str], node_role: str) -> None:
    lines = [
        "# Human Loop Queue",
        "",
        f"Generated: {now_iso()}",
        "",
        f"Node role: `{node_role}`",
        "",
        "Critical actions are blocked until explicitly approved.",
        "",
        "## Pending Approvals",
        "",
    ]

    pending = list(approvals_needed)
    if not pending:
        lines.append("- None")
    else:
        for key, reason in pending:
            lines.append(f"- [ ] `{key}` - {reason}")

    lines.extend(
        [
            "",
            "## Approved (Persistent)",
            "",
        ]
    )
    if approved:
        for key in sorted(approved):
            lines.append(f"- [x] `{key}`")
    else:
        lines.append("- None")

    lines.extend(
        [
            "",
            "## Resume Command",
            "",
            "Run Ship Captain again after approvals are done.",
            "",
        ]
    )

    with open(QUEUE_MD, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")


def resolve_critical_gates(approved: set[str]) -> List[Tuple[str, str]]:
    approvals_needed: List[Tuple[str, str]] = []
    accounts = load_accounts()
    secrets = load_secret_presence()
    node_role = load_node_role()

    for platform in REQUIRED_REVENUE_ACCOUNTS:
        if not account_ready(platform, accounts, secrets):
            approvals_needed.append((f"ACCOUNT_{platform.upper().replace('.', '_')}", f"Activate {platform} account"))

    if not email_infra_ready(secrets):
        approvals_needed.append(
            (
                "EMAIL_INFRA",
                "Configure Gmail/Resend + PHYSICAL_ADDRESS in SECRETS/PAYMENT_INFO.md (required for LIVE_EMAIL_SEND).",
            )
        )

    if not secrets.get("GUMROAD_ACCESS_TOKEN"):
        approvals_needed.append(("GUMROAD_API_TOKEN", "Add GUMROAD_ACCESS_TOKEN to SECRETS/PAYMENT_INFO.md for AUTO_LIST_ECOM."))

    if node_role != "worker":
        approvals_needed.append(
            (
                "RUN_ON_WORKER",
                "Critical revenue actions are disabled on non-worker node. Run worker node for auto-listing and live sending.",
            )
        )

    # Approval keys for critical ops
    if "AUTO_LIST_ECOM" not in approved:
        approvals_needed.append(("AUTO_LIST_ECOM", "Approve automated Gumroad product listing run"))
    if "LIVE_EMAIL_SEND" not in approved:
        approvals_needed.append(("LIVE_EMAIL_SEND", "Approve live cold-email send (100 max)"))

    policy = load_policy()
    risk_cfg = policy.get("risk", {})
    threshold = int(risk_cfg.get("high_compliance_critical_threshold", 1))
    compliance_key = str(risk_cfg.get("required_approval_key", "COMPLIANCE_HIGH_RISK")).strip().upper()
    counts = latest_compliance_counts()
    critical_count = int(counts.get("critical", 0))
    latest_file = str(counts.get("file", ""))
    if critical_count >= threshold and compliance_key not in approved:
        approvals_needed.append(
            (
                compliance_key,
                f"High compliance risk: {critical_count} CRITICAL issues in {latest_file}. "
                "Required for live high-upside execution.",
            )
        )

    return approvals_needed


def run_step_and_record(step: Step) -> Tuple[str, str, float]:
    status, output, duration = run_step(step)
    record_run(step, status, duration, output[-400:])
    return status, output, duration


def run_once(approved: set[str], *, swarm: bool = False, max_parallel: int = 4) -> int:
    ensure_dirs()
    ensure_runs_csv()
    lock_handle = acquire_run_lock()
    if lock_handle is None:
        append_log("SKIP run: another Ship Captain run is already in progress")
        return 0

    append_log("=== SHIP CAPTAIN RUN START ===")
    try:
        # Always run non-critical stack.
        if not swarm:
            for step in AUTO_STEPS:
                run_step_and_record(step)
        else:
            max_parallel = int(max_parallel or 0)
            if max_parallel < 1:
                max_parallel = 1
            if max_parallel > 12:
                max_parallel = 12

            by_id: Dict[str, Step] = {s.step_id: s for s in AUTO_STEPS}

            preflight = [
                "stack_health",
                "preflight_status",
                "preflight_blockers",
            ]
            alpha_lane = [
                "alpha_staging_migrate",
                "x_ingest_copy_style",
                "alpha_monitor",
                "unified_alpha_monitor",
                "alpha_autoapprove",
                "alpha_to_ops",
            ]

            swarm_lanes: Dict[str, List[str]] = {
                "growth": ["triggering_events", "clawdbot_rbi"],
                "ecom": ["ecom_arb_scan", "arb_listings", "ecom_autopilot", "ecom_distribution", "ecom_pack", "gumroad_autolist_pack"],
                "freelance": ["freelance_scan", "freelance_drafts", "freelance_pack"],
                "gov": ["gov_monitor", "gov_pack"],
                "content": ["carousel_factory", "calendar", "buffer_csv", "qa_router", "qa_autoapprove", "publish_pack"],
                "deploy": ["app_pack", "native_apps_pack", "deploy_guard", "launch_pack"],
            }

            # Finalization runs last so the dashboard/memory reflect the whole run.
            finalize = [
                "clawwork_sidecar",
                "master_ops_enhance",
                "master_ops_exec_plan",
                "human_brief",
                "rbi_daily",
                "rbi_portfolio",
                "compliance",
                "cluely_pack",
                "cron_fleet",
                "dashboard",
                "memory",
                "cron_status",
                "email_preview",
            ]

            def run_step_id(step_id: str) -> None:
                s = by_id.get(step_id)
                if s is None:
                    append_log(f"SWARM: unknown step_id={step_id}. Skipping.")
                    return
                run_step_and_record(s)

            # Phase 1: ordered preflight + alpha lane (single-writer to ALPHA_STAGING).
            for sid in preflight + alpha_lane:
                run_step_id(sid)

            # Phase 2: run the rest as lanes (sequential in-lane, parallel across lanes).
            def lane_worker(lane_name: str, step_ids: List[str]) -> None:
                append_log(f"LANE_START {lane_name}")
                for sid in step_ids:
                    run_step_id(sid)
                append_log(f"LANE_END {lane_name}")

            futures: Dict[concurrent.futures.Future, str] = {}
            with concurrent.futures.ThreadPoolExecutor(max_workers=max_parallel) as ex:
                for lane_name, step_ids in swarm_lanes.items():
                    futures[ex.submit(lane_worker, lane_name, step_ids)] = lane_name
                for fut in concurrent.futures.as_completed(futures):
                    lane_name = futures.get(fut, "unknown")
                    try:
                        fut.result()
                    except Exception as e:
                        append_log(f"LANE_CRASH {lane_name}: {e}")

            # Phase 3: finalization sequential.
            for sid in finalize:
                run_step_id(sid)

            # Safety: if AUTO_STEPS changes, still execute anything not covered above.
            covered: set[str] = set(preflight + alpha_lane + finalize)
            for ids in swarm_lanes.values():
                covered.update(ids)
            all_defined: set[str] = set(by_id.keys())
            uncovered = sorted(all_defined - covered)
            if uncovered:
                append_log(f"SWARM: uncovered steps detected ({len(uncovered)}). Running serially: {', '.join(uncovered)}")
                for sid in uncovered:
                    run_step_id(sid)

        # Evaluate critical gates
        pending = resolve_critical_gates(approved)
        node_role = load_node_role()
        build_human_queue(pending, approved, node_role)

        # Run critical steps only when approved + no prerequisite blockers remain.
        secrets = load_secret_presence()
        email_ready = email_infra_ready(secrets)
        policy = load_policy()
        risk_cfg = policy.get("risk", {})
        threshold = int(risk_cfg.get("high_compliance_critical_threshold", 1))
        compliance_key = str(risk_cfg.get("required_approval_key", "COMPLIANCE_HIGH_RISK")).strip().upper()
        counts = latest_compliance_counts()
        critical_count = int(counts.get("critical", 0))
        latest_file = str(counts.get("file", ""))
        critical_executed = False

        for step in CRITICAL_STEPS:
            if node_role != "worker":
                record_run(step, "SKIPPED", 0, f"Node role '{node_role}' cannot run critical actions")
                continue
            if step.critical_key not in approved:
                record_run(step, "SKIPPED", 0, f"Missing approval: {step.critical_key}")
                continue
            if step.critical_key == "AUTO_LIST_ECOM" and not secrets.get("GUMROAD_ACCESS_TOKEN"):
                record_run(step, "SKIPPED", 0, "Missing GUMROAD_ACCESS_TOKEN in SECRETS/PAYMENT_INFO.md")
                continue
            if step.critical_key == "LIVE_EMAIL_SEND" and not email_ready:
                record_run(step, "SKIPPED", 0, "Email infra not configured (GMAIL/RESEND + PHYSICAL_ADDRESS)")
                continue
            if step.critical_key == "LIVE_EMAIL_SEND" and critical_count >= threshold and compliance_key not in approved:
                record_run(
                    step,
                    "SKIPPED",
                    0,
                    f"Missing approval: {compliance_key} (critical={critical_count}, source={latest_file})",
                )
                continue
            status, output, duration = run_step(step)
            record_run(step, status, duration, output[-400:])

            # If we actually executed a critical step, run post-refresh steps to reflect
            # new deploy/listing state immediately (avoid waiting for next cron tick).
            critical_executed = True

        if critical_executed:
            for step in POST_CRITICAL_STEPS:
                status, output, duration = run_step(step)
                record_run(step, status, duration, output[-400:])

        return 0
    finally:
        append_log("=== SHIP CAPTAIN RUN END ===")
        try:
            fcntl.flock(lock_handle.fileno(), fcntl.LOCK_UN)
        finally:
            lock_handle.close()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="PRINTMAXX Ship Captain")
    parser.add_argument("--run", action="store_true", help="Run once (default)")
    parser.add_argument("--loop", action="store_true", help="Run continuously")
    parser.add_argument("--interval-sec", type=int, default=1800, help="Loop interval seconds (default: 1800)")
    parser.add_argument(
        "--swarm",
        action="store_true",
        help="Run auto steps as parallel lanes (safe swarm mode).",
    )
    parser.add_argument(
        "--max-parallel",
        type=int,
        default=4,
        help="Max parallel lanes in --swarm mode (default: 4).",
    )
    parser.add_argument(
        "--approve",
        action="append",
        default=[],
        help="Critical approval key (repeatable), e.g. --approve AUTO_LIST_ECOM --approve LIVE_EMAIL_SEND",
    )
    parser.add_argument(
        "--revoke",
        action="append",
        default=[],
        help="Revoke/pause a persistent approval key (repeatable), e.g. --revoke LIVE_EMAIL_SEND",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    ensure_dirs()
    ensure_approvals_csv()

    approve_cli = {k.strip().upper() for k in args.approve if k and k.strip()}
    revoke_cli = {k.strip().upper() for k in args.revoke if k and k.strip()}
    if approve_cli or revoke_cli:
        upsert_persistent_approvals(approve_cli, revoke_cli)

    approved = load_persistent_approvals()
    approved |= approve_cli
    approved -= revoke_cli

    if args.loop:
        while True:
            run_once(approved, swarm=args.swarm, max_parallel=args.max_parallel)
            time.sleep(max(30, args.interval_sec))
    return run_once(approved, swarm=args.swarm, max_parallel=args.max_parallel)


if __name__ == "__main__":
    raise SystemExit(main())
