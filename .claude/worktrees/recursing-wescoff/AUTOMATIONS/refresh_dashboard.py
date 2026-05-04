#!/usr/bin/env python3

from __future__ import annotations
"""
PRINTMAXX Pipeline Dashboard Generator
========================================
Generates a Bloomberg-style HTML control panel for PRINTMAXX.

This is intentionally file-based (no server) so it can be refreshed from cron
and opened in a browser on demand.

Usage:
    python3 AUTOMATIONS/refresh_dashboard.py          # Generate + open
    python3 AUTOMATIONS/refresh_dashboard.py --no-open # Generate only
"""

import json
import csv
import argparse
import re
from pathlib import Path
from datetime import datetime
from collections import Counter, defaultdict

BASE = Path(__file__).resolve().parent.parent
OUTPUT_DIR = BASE / "output" / "dashboard"
OUTPUT_FILE = OUTPUT_DIR / "index.html"
OUTPUT_ROOT = BASE / "output"
SHIP_CRON_LOG = BASE / "logs" / "ship_cron.log"

SHIP_RUNS_CSV = BASE / "LEDGER" / "SHIP_CAPTAIN_RUNS.csv"
HUMAN_QUEUE_MD = BASE / "OPS" / "HUMAN_LOOP_QUEUE.md"
DEPLOYMENT_URLS_MD = BASE / "OPS" / "DEPLOYMENT_URLS.md"
STATIC_DEPLOYMENT_URLS_MD = BASE / "OPS" / "STATIC_DEPLOYMENT_URLS.md"
STACK_HEARTBEAT_MD = BASE / "OPS" / "STACK_HEARTBEAT.md"
RBI_TODO_MD = BASE / "OPS" / "RBI_PORTFOLIO_TODO.md"
COMPLIANCE_GLOB = "compliance_scan_*.json"
QA_DIR = BASE / "OPS" / "CONTENT_QA_QUEUE"
PUBLISH_MANIFEST = OUTPUT_ROOT / "publish_packs" / "manifest.json"
ECOM_MANIFEST = OUTPUT_ROOT / "ecom" / "manifest.json"
ECOM_AUTOLIST_MANIFEST = OUTPUT_ROOT / "ecom_autolist" / "manifest.json"
ECOM_AUTOPILOT_MANIFEST = OUTPUT_ROOT / "ecom_autopilot" / "manifest.json"
FREELANCE_MANIFEST = OUTPUT_ROOT / "freelance" / "manifest.json"
GOV_MANIFEST = OUTPUT_ROOT / "gov" / "manifest.json"
APPS_MANIFEST = OUTPUT_ROOT / "apps" / "manifest.json"
NATIVE_APPS_MANIFEST = OUTPUT_ROOT / "native_apps" / "manifest.json"
LAUNCH_MANIFEST = OUTPUT_ROOT / "launch" / "manifest.json"
CRON_FLEET_MANIFEST = OUTPUT_ROOT / "cron_fleet" / "manifest.json"
CLAWDBOT_MANIFEST = OUTPUT_ROOT / "clawdbot" / "manifest.json"

ALPHA_STAGING_CSV = BASE / "LEDGER" / "ALPHA_STAGING.csv"
AUTO_OPS_TRACKER_CSV = BASE / "LEDGER" / "AUTO_OPS_TRACKER.csv"
COPY_STYLE_CORPUS_CSV = BASE / "LEDGER" / "COPY_STYLE_CORPUS.csv"


def read_text(path: Path, default: str) -> str:
    try:
        if path.exists():
            return path.read_text(encoding="utf-8", errors="replace")
    except Exception:
        pass
    return default


def load_human_queue() -> list[dict]:
    items: list[dict] = []
    text = read_text(HUMAN_QUEUE_MD, "")
    for line in text.splitlines():
        s = line.strip()
        if not s.startswith("- ["):
            continue
        # - [ ] `KEY` - reason
        if "`" not in s:
            continue
        try:
            key = s.split("`", 2)[1].strip()
            reason = s.split(" - ", 1)[1].strip() if " - " in s else ""
            items.append({"key": key, "reason": reason})
        except Exception:
            continue
    return items


def load_ship_runs_tail(limit: int = 40) -> list[dict]:
    if not SHIP_RUNS_CSV.exists():
        return []
    rows: list[dict] = []
    try:
        with open(SHIP_RUNS_CSV, "r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                rows.append(row)
    except Exception:
        return []
    return rows[-limit:]


def load_last_status_by_step() -> dict[str, dict]:
    # Best-effort: last row per step_id.
    by_step: dict[str, dict] = {}
    for row in load_ship_runs_tail(400):
        step_id = (row.get("step_id") or "").strip()
        if not step_id:
            continue
        by_step[step_id] = row
    return by_step


def latest_compliance_counts() -> dict:
    files = sorted((BASE / "LEDGER").glob(COMPLIANCE_GLOB))
    result = {"file": "", "critical": 0, "warning": 0, "info": 0, "total": 0}
    if not files:
        return result
    path = files[-1]
    result["file"] = str(path.relative_to(BASE))
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
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


def deploy_stats() -> dict:
    """Parse OPS/DEPLOYMENT_URLS.md (PWA deployer output) for quick status."""
    text = read_text(DEPLOYMENT_URLS_MD, "")
    total = live = failed = 0
    last_updated = ""
    for line in text.splitlines():
        s = line.strip()
        if s.lower().startswith("**last updated:**"):
            last_updated = s.split(":", 1)[1].strip().strip("*").strip()
            break

    in_table = False
    for raw in text.splitlines():
        s = raw.strip()
        if s.lower().startswith("| app | url | status |"):
            in_table = True
            continue
        if not in_table:
            continue
        if not s:
            break
        if s.startswith("|-----"):
            continue
        if not s.startswith("|"):
            continue
        cols = [c.strip() for c in s.strip("|").split("|")]
        if len(cols) < 3:
            continue
        status = cols[2].strip().upper()
        total += 1
        if status == "LIVE":
            live += 1
        elif status == "FAILED":
            failed += 1
    return {"total": total, "live": live, "failed": failed, "last_updated": last_updated}


def static_deploy_stats() -> dict:
    """Parse OPS/STATIC_DEPLOYMENT_URLS.md (static deployer output)."""
    text = read_text(STATIC_DEPLOYMENT_URLS_MD, "")
    total = live = failed = 0
    last_updated = ""
    for line in text.splitlines():
        s = line.strip()
        if s.lower().startswith("**last updated:**"):
            last_updated = s.split(":", 1)[1].strip().strip("*").strip()
            break

    in_table = False
    for raw in text.splitlines():
        s = raw.strip()
        if s.lower().startswith("| site | url | status |"):
            in_table = True
            continue
        if not in_table:
            continue
        if not s:
            break
        if s.startswith("|---"):
            continue
        if not s.startswith("|"):
            continue
        cols = [c.strip() for c in s.strip("|").split("|")]
        if len(cols) < 3:
            continue
        status = cols[2].strip().upper()
        total += 1
        if status == "LIVE":
            live += 1
        elif status in {"FAILED", "FAIL"}:
            failed += 1
    return {"total": total, "live": live, "failed": failed, "last_updated": last_updated}


def qa_queue_counts() -> dict:
    QA_DIR.mkdir(parents=True, exist_ok=True)
    counts = Counter()
    total = 0

    for p in QA_DIR.glob("*.md"):
        try:
            text = p.read_text(encoding="utf-8", errors="replace")
        except Exception:
            continue
        # Front matter: status: XYZ
        status = ""
        if text.startswith("---"):
            for line in text.splitlines():
                if line.strip() == "---":
                    continue
                if line.lower().startswith("status:"):
                    status = line.split(":", 1)[1].strip()
                    break
        status = (status or "UNKNOWN").strip().upper()
        counts[status] += 1
        total += 1

    return {"total": total, "by_status": dict(counts)}


def load_publish_manifest() -> dict:
    if not PUBLISH_MANIFEST.exists():
        return {"items": []}
    try:
        payload = json.loads(PUBLISH_MANIFEST.read_text(encoding="utf-8"))
        if isinstance(payload, dict) and isinstance(payload.get("items"), list):
            return payload
    except Exception:
        pass
    return {"items": []}


def load_json(path: Path) -> dict:
    if not path.exists():
        return {}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
        return payload if isinstance(payload, dict) else {}
    except Exception:
        return {}


def ecom_stats() -> dict:
    payload = load_json(ECOM_MANIFEST)
    top_arb = payload.get("top_arb") if isinstance(payload.get("top_arb"), list) else []
    return {
        "generated_at": payload.get("generated_at") or "",
        "top_arb_count": len(top_arb),
        "top_arb": top_arb[:5],
        "latest_href": "../ecom/latest.html" if (OUTPUT_ROOT / "ecom" / "latest.html").exists() else "",
    }

def ecom_autolist_stats() -> dict:
    payload = load_json(ECOM_AUTOLIST_MANIFEST)
    latest_href = "../ecom_autolist/latest.html" if (OUTPUT_ROOT / "ecom_autolist" / "latest.html").exists() else ""
    return {
        "generated_at": payload.get("generated_at") or "",
        "catalog_count": int(payload.get("catalog_count") or 0),
        "live_count": int(payload.get("live_count") or 0),
        "created_count": int(payload.get("created_count") or 0),
        "failed_count": int(payload.get("failed_count") or 0),
        "pending_count": int(payload.get("pending_count") or 0),
        "ledger_last_event": payload.get("ledger_last_event") or "",
        "latest_href": latest_href,
    }


def ecom_autopilot_stats() -> dict:
    payload = load_json(ECOM_AUTOPILOT_MANIFEST)
    qstats = payload.get("queue_stats") if isinstance(payload.get("queue_stats"), dict) else {}
    latest_href = "../ecom_autopilot/latest.html" if (OUTPUT_ROOT / "ecom_autopilot" / "latest.html").exists() else ""

    total_queue = 0
    auto_ready = 0
    blocked = 0
    for stat in qstats.values():
        if not isinstance(stat, dict):
            continue
        total_queue += int(stat.get("total") or 0)
        auto_ready += int(stat.get("auto_ready") or 0)
        blocked += int(stat.get("blocked") or 0)

    return {
        "generated_at": payload.get("generated_at") or "",
        "winners_count": int(payload.get("winners_count") or 0),
        "total_queue": total_queue,
        "auto_ready": auto_ready,
        "blocked": blocked,
        "queue_stats": qstats,
        "latest_href": latest_href,
    }


def clawdbot_stats() -> dict:
    payload = load_json(CLAWDBOT_MANIFEST)
    counts = payload.get("counts") if isinstance(payload.get("counts"), dict) else {}
    latest_href = "../clawdbot/latest.html" if (OUTPUT_ROOT / "clawdbot" / "latest.html").exists() else ""
    return {
        "generated_at": payload.get("generated_at") or "",
        "intent_rows": int(counts.get("intent_rows") or 0),
        "syndication_rows": int(counts.get("syndication_rows") or 0),
        "directory_rows": int(counts.get("directory_rows") or 0),
        "job_rows": int(counts.get("job_rows") or 0),
        "keyword_rows": int(counts.get("keyword_rows") or 0),
        "community_rows": int(counts.get("community_rows") or 0),
        "latest_href": latest_href,
    }


def freelance_stats() -> dict:
    payload = load_json(FREELANCE_MANIFEST)
    return {
        "generated_at": payload.get("generated_at") or "",
        "draft_count": int(payload.get("draft_count") or 0),
        "scan_count": int(payload.get("scan_count") or 0),
        "latest_href": "../freelance/latest.html" if (OUTPUT_ROOT / "freelance" / "latest.html").exists() else "",
    }


def gov_stats() -> dict:
    payload = load_json(GOV_MANIFEST)
    open_items = payload.get("open") if isinstance(payload.get("open"), list) else []
    soonest = None
    for it in open_items:
        if not isinstance(it, dict):
            continue
        d = it.get("deadline")
        if not isinstance(d, str) or not d:
            continue
        if soonest is None or d < soonest:
            soonest = d
    return {
        "generated_at": payload.get("generated_at") or "",
        "open_count": int(payload.get("open_count") or 0),
        "soonest_deadline": soonest or "",
        "latest_href": "../gov/latest.html" if (OUTPUT_ROOT / "gov" / "latest.html").exists() else "",
    }


def apps_stats() -> dict:
    payload = load_json(APPS_MANIFEST)
    items = payload.get("items") if isinstance(payload.get("items"), list) else []
    latest_href = "../apps/latest.html" if (OUTPUT_ROOT / "apps" / "latest.html").exists() else ""
    return {
        "generated_at": payload.get("generated_at") or "",
        "count": int(payload.get("count") or len(items)),
        "latest_href": latest_href,
    }


def launch_stats() -> dict:
    payload = load_json(LAUNCH_MANIFEST)
    packs = payload.get("packs") if isinstance(payload.get("packs"), list) else []
    latest_href = "../launch/latest.html" if (OUTPUT_ROOT / "launch" / "latest.html").exists() else ""
    return {
        "generated_at": payload.get("generated_at") or "",
        "directories_count": int(payload.get("directories_count") or 0),
        "packs_count": len(packs),
        "latest_href": latest_href,
    }

def native_apps_stats() -> dict:
    payload = load_json(NATIVE_APPS_MANIFEST)
    items = payload.get("items") if isinstance(payload.get("items"), list) else []
    latest_href = "../native_apps/latest.html" if (OUTPUT_ROOT / "native_apps" / "latest.html").exists() else ""
    return {
        "generated_at": payload.get("generated_at") or "",
        "count": int(payload.get("count") or len(items)),
        "latest_href": latest_href,
    }

def cron_fleet_stats() -> dict:
    payload = load_json(CRON_FLEET_MANIFEST)
    logs = payload.get("logs") if isinstance(payload.get("logs"), list) else []
    artifacts = payload.get("artifacts") if isinstance(payload.get("artifacts"), list) else []
    latest_href = "../cron_fleet/latest.html" if (OUTPUT_ROOT / "cron_fleet" / "latest.html").exists() else ""
    return {
        "generated_at": payload.get("generated_at") or payload.get("generated_at") or "",
        "logs_count": len(logs),
        "artifacts_count": len(artifacts),
        "logs": logs[:10],
        "latest_href": latest_href,
    }


def publish_pack_stats() -> dict:
    payload = load_publish_manifest()
    items = payload.get("items", [])
    if not isinstance(items, list):
        items = []

    by_platform = Counter()
    latest = None
    for it in items:
        if not isinstance(it, dict):
            continue
        by_platform[(it.get("platform") or "unknown").strip().lower()] += 1
        latest = it

    return {
        "total": sum(by_platform.values()),
        "by_platform": dict(by_platform),
        "latest": latest if isinstance(latest, dict) else None,
    }

def alpha_stats() -> dict:
    """Quick alpha pipeline status from LEDGER/ALPHA_STAGING.csv."""
    if not ALPHA_STAGING_CSV.exists():
        return {
            "total": 0,
            "by_status": {},
            "ops_generated_true": 0,
            "ops_backlog": 0,
            "latest_created_at": "",
        }
    by_status = Counter()
    total = 0
    ops_true = 0
    latest_created = ""
    try:
        with open(ALPHA_STAGING_CSV, "r", newline="", encoding="utf-8", errors="replace") as f:
            reader = csv.DictReader(f)
            for row in reader:
                total += 1
                st = (row.get("status") or "UNKNOWN").strip().upper()
                by_status[st] += 1
                if (row.get("ops_generated") or "").strip().upper() == "TRUE":
                    ops_true += 1
                ca = (row.get("created_at") or "").strip()
                if ca and (not latest_created or ca > latest_created):
                    latest_created = ca
    except Exception:
        return {
            "total": 0,
            "by_status": {},
            "ops_generated_true": 0,
            "ops_backlog": 0,
            "latest_created_at": "",
        }
    # Backlog = approved/auto_approved but not ops_generated.
    backlog = 0
    for st in ("APPROVED", "AUTO_APPROVED"):
        backlog += int(by_status.get(st, 0))
    backlog = max(0, backlog - ops_true)
    return {
        "total": total,
        "by_status": dict(by_status),
        "ops_generated_true": ops_true,
        "ops_backlog": backlog,
        "latest_created_at": latest_created,
    }


def auto_ops_stats() -> dict:
    """Quick ops generator status from LEDGER/AUTO_OPS_TRACKER.csv."""
    if not AUTO_OPS_TRACKER_CSV.exists():
        return {"total": 0, "by_status": {}, "by_category": {}, "latest": None}
    by_status = Counter()
    by_category = Counter()
    total = 0
    latest = None
    try:
        with open(AUTO_OPS_TRACKER_CSV, "r", newline="", encoding="utf-8", errors="replace") as f:
            reader = csv.DictReader(f)
            for row in reader:
                total += 1
                st = (row.get("status") or "UNKNOWN").strip().upper()
                by_status[st] += 1
                cat = (row.get("category") or "UNKNOWN").strip().upper()
                by_category[cat] += 1
                latest = row
    except Exception:
        return {"total": 0, "by_status": {}, "by_category": {}, "latest": None}
    top_cats = dict(by_category.most_common(8))
    return {"total": total, "by_status": dict(by_status), "by_category": top_cats, "latest": latest}


def copy_style_stats() -> dict:
    """Counts + latest scrape timestamp from LEDGER/COPY_STYLE_CORPUS.csv."""
    if not COPY_STYLE_CORPUS_CSV.exists():
        return {"rows": 0, "latest_scraped_at": ""}
    rows = 0
    latest = ""
    try:
        with open(COPY_STYLE_CORPUS_CSV, "r", newline="", encoding="utf-8", errors="replace") as f:
            reader = csv.DictReader(f)
            for row in reader:
                rows += 1
                ts = (row.get("scraped_at") or "").strip()
                if ts and (not latest or ts > latest):
                    latest = ts
    except Exception:
        return {"rows": 0, "latest_scraped_at": ""}
    return {"rows": rows, "latest_scraped_at": latest}


def escape_html(s: str) -> str:
    return (s or "").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

def _fmt_throttle_notes(notes: str) -> str:
    """Make net_guard throttle notes human-scannable."""
    n = (notes or "").strip()
    m = re.search(r"remaining_sec=(\d+)", n)
    if not m:
        return n
    try:
        sec = int(m.group(1))
    except Exception:
        return n
    mins = sec // 60
    hrs = mins // 60
    rem = mins % 60
    pretty = f"{hrs}h{rem:02d}m" if hrs else f"{rem}m"
    n = re.sub(r"remaining_sec=\d+", f"next_in={pretty}", n)
    return n

def tail_text(path: Path, *, max_lines: int = 120, max_bytes: int = 96_000) -> str:
    if not path.exists():
        return ""
    try:
        data = b""
        with open(path, "rb") as f:
            f.seek(0, 2)
            end = f.tell()
            size = min(end, max_bytes)
            f.seek(max(0, end - size))
            data = f.read(size)
        text = data.decode("utf-8", errors="replace")
        lines = text.splitlines()[-max_lines:]
        return "\n".join(lines)
    except Exception:
        return ""


def generate_dashboard():
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    queue = load_human_queue()
    runs_tail = load_ship_runs_tail(50)
    last_by_step = load_last_status_by_step()
    compliance = latest_compliance_counts()
    deploy = deploy_stats()
    static_deploy = static_deploy_stats()
    qa_stats = qa_queue_counts()
    pack_stats = publish_pack_stats()
    alpha = alpha_stats()
    ops = auto_ops_stats()
    copy_style = copy_style_stats()
    ecom = ecom_stats()
    ecom_autolist = ecom_autolist_stats()
    ecom_autopilot = ecom_autopilot_stats()
    clawdbot = clawdbot_stats()
    freelance = freelance_stats()
    gov = gov_stats()
    apps = apps_stats()
    native_apps = native_apps_stats()
    launch = launch_stats()
    cron_fleet = cron_fleet_stats()
    stack_heartbeat = read_text(STACK_HEARTBEAT_MD, "No stack heartbeat yet.")
    rbi_todo = read_text(RBI_TODO_MD, "No RBI portfolio todo yet.")
    ship_tail = tail_text(SHIP_CRON_LOG, max_lines=120)

    # Summary counters from last N rows (not perfect run grouping, but good enough for pulse)
    status_counts = Counter((r.get("status") or "").strip().upper() for r in runs_tail if r.get("status"))
    last_ts = runs_tail[-1].get("timestamp", "") if runs_tail else ""

    # Content stats
    qa_by = qa_stats.get("by_status", {}) if isinstance(qa_stats.get("by_status"), dict) else {}
    qa_pending = int(qa_by.get("PENDING_REVIEW", 0))
    qa_needs_style = int(qa_by.get("NEEDS_STYLE_FIX", 0))
    qa_approved = 0
    for k, v in qa_by.items():
        if str(k).upper().startswith("APPROVED"):
            try:
                qa_approved += int(v)
            except Exception:
                pass

    latest_pack = pack_stats.get("latest") if isinstance(pack_stats.get("latest"), dict) else None
    latest_preview_href = ""
    if latest_pack:
        rel = (latest_pack.get("preview_output_rel") or "").strip()
        if rel:
            # Dashboard is output/dashboard/index.html; output root is output/
            latest_preview_href = "../" + rel.replace("\\", "/")

    ecom_preview_text = "\n".join(
        [
            f"- {(it.get('product') or '')} (margin={it.get('margin_pct')}, profit={it.get('net_profit')})"
            for it in (ecom.get("top_arb") or [])
            if isinstance(it, dict)
        ]
    ) or "No arb items yet."
    ecom_preview = escape_html(ecom_preview_text)
    ecom_autolist_preview_text = (
        f"catalog={ecom_autolist.get('catalog_count', 0)} live={ecom_autolist.get('live_count', 0)} "
        f"created={ecom_autolist.get('created_count', 0)} pending={ecom_autolist.get('pending_count', 0)} "
        f"failed={ecom_autolist.get('failed_count', 0)} last={ecom_autolist.get('ledger_last_event') or 'n/a'}"
    )
    ecom_autolist_preview = escape_html(ecom_autolist_preview_text)
    ecom_autopilot_queue_stats = ecom_autopilot.get("queue_stats") if isinstance(ecom_autopilot.get("queue_stats"), dict) else {}
    ecom_autopilot_preview_text = "\n".join(
        [f"{k}: total={int((v or {}).get('total', 0))} auto={int((v or {}).get('auto_ready', 0))} blocked={int((v or {}).get('blocked', 0))}" for k, v in ecom_autopilot_queue_stats.items() if isinstance(v, dict)]
    ) or "No platform queues yet."
    ecom_autopilot_preview = escape_html(ecom_autopilot_preview_text)
    clawdbot_preview_text = (
        f"intent={clawdbot.get('intent_rows', 0)} "
        f"syndication={clawdbot.get('syndication_rows', 0)} "
        f"directories={clawdbot.get('directory_rows', 0)} "
        f"jobs={clawdbot.get('job_rows', 0)} "
        f"keywords={clawdbot.get('keyword_rows', 0)} "
        f"community={clawdbot.get('community_rows', 0)}"
    )
    clawdbot_preview = escape_html(clawdbot_preview_text)

    deploy_total = int(deploy.get("total", 0) or 0)
    deploy_live = int(deploy.get("live", 0) or 0)
    deploy_label = f"{deploy_live}/{deploy_total}" if deploy_total else "n/a"
    deploy_class = "green" if (deploy_total and deploy_live == deploy_total) else ("amber" if deploy_live else ("red" if deploy_total else "amber"))

    static_total = int(static_deploy.get("total", 0) or 0)
    static_live = int(static_deploy.get("live", 0) or 0)
    static_label = f"{static_live}/{static_total}" if static_total else "n/a"
    static_class = "green" if (static_total and static_live == static_total) else ("amber" if static_live else ("red" if static_total else "amber"))

    alpha_by = alpha.get("by_status", {}) if isinstance(alpha.get("by_status"), dict) else {}
    alpha_pending = int(alpha_by.get("PENDING_REVIEW", 0))
    alpha_auto = int(alpha_by.get("AUTO_APPROVED", 0))
    alpha_approved = int(alpha_by.get("APPROVED", 0))
    alpha_total = int(alpha.get("total", 0) or 0)
    alpha_ops_true = int(alpha.get("ops_generated_true", 0) or 0)

    ops_by = ops.get("by_status", {}) if isinstance(ops.get("by_status"), dict) else {}
    ops_total = int(ops.get("total", 0) or 0)
    ops_generated = int(ops_by.get("GENERATED", 0))
    ops_ready = int(ops_by.get("READY_TO_DEPLOY", 0))
    ops_cat_preview_text = "\n".join([f"{k}: {v}" for k, v in (ops.get("by_category", {}) or {}).items()]) or "No ops yet."
    ops_cat_preview = escape_html(ops_cat_preview_text)

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta http-equiv="refresh" content="60">
<title>PRINTMAXX Control Panel</title>
<style>
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{ background: #0a0a0a; color: #e0e0e0; font-family: 'SF Mono', 'Fira Code', 'Consolas', monospace; font-size: 13px; }}
.header {{ background: #111; border-bottom: 1px solid #222; padding: 12px 20px; display: flex; justify-content: space-between; align-items: center; }}
.header h1 {{ font-size: 16px; color: #00ff88; letter-spacing: 2px; }}
.header .ts {{ color: #666; font-size: 11px; }}
.grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 1px; background: #222; padding: 1px; }}
.panel {{ background: #0f0f0f; padding: 16px; min-height: 200px; }}
.panel h2 {{ color: #00ff88; font-size: 12px; letter-spacing: 1px; margin-bottom: 12px; text-transform: uppercase; }}
.big-number {{ font-size: 36px; font-weight: bold; color: #fff; }}
.big-number .unit {{ font-size: 14px; color: #666; }}
.stat-row {{ display: flex; justify-content: space-between; padding: 6px 0; border-bottom: 1px solid #1a1a1a; }}
.stat-label {{ color: #888; }}
.stat-value {{ color: #fff; font-weight: bold; }}
.stat-value.green {{ color: #00ff88; }}
.stat-value.amber {{ color: #ffaa00; }}
.stat-value.red {{ color: #ff4444; }}
.mono {{ white-space: pre-wrap; font-size: 11px; line-height: 1.6; color: #aaa; }}
.queue-item {{ padding: 6px 0; border-bottom: 1px solid #1a1a1a; }}
.queue-key {{ color: #00aaff; font-weight: bold; }}
.queue-reason {{ color: #aaa; }}
.link {{ color: #00aaff; text-decoration: none; }}
.link:hover {{ text-decoration: underline; }}
.table {{ width: 100%; border-collapse: collapse; }}
.table th, .table td {{ border-bottom: 1px solid #1a1a1a; padding: 6px 6px; font-size: 11px; text-align: left; vertical-align: top; }}
.pill {{ display:inline-block; padding: 2px 8px; border-radius: 999px; font-size: 10px; font-weight: bold; }}
.ok {{ background:#123; color:#00ff88; border:1px solid #1a1a1a; }}
.failed {{ background:#231; color:#ff4444; border:1px solid #1a1a1a; }}
.skipped {{ background:#221; color:#ffaa00; border:1px solid #1a1a1a; }}
@media (max-width: 900px) {{ .grid {{ grid-template-columns: 1fr; }} }}
</style>
</head>
<body>
<div class="header">
  <h1>PRINTMAXX CONTROL</h1>
  <div class="ts">Updated: {now} | Auto-refresh: 60s | Last row: {last_ts or "n/a"}</div>
</div>

<div class="grid">
  <!-- Panel 1: System Summary -->
  <div class="panel">
    <h2>System Summary</h2>
    <div class="stat-row"><span class="stat-label">Compliance (latest)</span><span class="stat-value {'red' if compliance['critical'] else ('amber' if compliance['warning'] else 'green')}">C{compliance['critical']} W{compliance['warning']} I{compliance['info']}</span></div>
    <div class="stat-row"><span class="stat-label">Queue pending</span><span class="stat-value {'amber' if queue else 'green'}">{len(queue)}</span></div>
    <div class="stat-row"><span class="stat-label">Deploy (PWA)</span><span class="stat-value {deploy_class}">{deploy_label}</span></div>
    <div class="stat-row"><span class="stat-label">Deploy (Static)</span><span class="stat-value {static_class}">{static_label}</span></div>
    <div class="stat-row"><span class="stat-label">Recent OK</span><span class="stat-value green">{status_counts.get('OK', 0)}</span></div>
    <div class="stat-row"><span class="stat-label">Recent FAILED</span><span class="stat-value red">{status_counts.get('FAILED', 0)}</span></div>
    <div class="stat-row"><span class="stat-label">Recent SKIPPED</span><span class="stat-value amber">{status_counts.get('SKIPPED', 0)}</span></div>
  </div>

  <!-- Panel 2: Human Loop Queue -->
  <div class="panel">
    <h2>Human Loop Queue</h2>
    {''.join([f"<div class='queue-item'><span class='queue-key'>{i['key']}</span><div class='queue-reason'>{i['reason']}</div></div>" for i in queue]) if queue else "<div class='mono'>No pending approvals.</div>"}
  </div>

  <!-- Panel 3: Last Steps (per step_id) -->
  <div class="panel">
    <h2>Last Step Status</h2>
    <table class="table">
      <thead><tr><th>step</th><th>status</th><th>dur</th><th>ts</th><th>notes</th></tr></thead>
      <tbody>
        {''.join([f"<tr><td>{sid}</td><td><span class='pill {('ok' if (row.get('status','').upper()=='OK') else ('failed' if (row.get('status','').upper()=='FAILED') else 'skipped'))}'>{row.get('status','')}</span></td><td>{row.get('duration_sec','')}</td><td>{row.get('timestamp','')}</td><td>{escape_html(_fmt_throttle_notes((row.get('notes','') or ''))[:160])}</td></tr>" for sid, row in sorted(last_by_step.items())])}
      </tbody>
    </table>
  </div>

  <!-- Panel 4: Live Ship Log Tail -->
  <div class="panel">
    <h2>Ship Captain Log (Tail)</h2>
    <div class="stat-row"><span class="stat-label">File</span><span class="stat-value">{escape_html(str(SHIP_CRON_LOG))}</span></div>
    <div class="mono">{escape_html(ship_tail) if ship_tail else "No log output yet."}</div>
  </div>

  <!-- Panel 5: Alpha Pipeline -->
  <div class="panel">
    <h2>Alpha Pipeline</h2>
    <div class="stat-row"><span class="stat-label">Alpha total</span><span class="stat-value">{alpha_total}</span></div>
    <div class="stat-row"><span class="stat-label">Pending review</span><span class="stat-value {'amber' if alpha_pending else 'green'}">{alpha_pending}</span></div>
    <div class="stat-row"><span class="stat-label">Auto-approved</span><span class="stat-value green">{alpha_auto}</span></div>
    <div class="stat-row"><span class="stat-label">Approved</span><span class="stat-value green">{alpha_approved}</span></div>
    <div class="stat-row"><span class="stat-label">Ops generated</span><span class="stat-value {'green' if alpha_ops_true else 'amber'}">{alpha_ops_true}</span></div>
    <div class="stat-row"><span class="stat-label">Copy-style corpus</span><span class="stat-value">{int(copy_style.get('rows', 0) or 0)}</span></div>
    <div class="stat-row"><span class="stat-label">Last corpus ingest</span><span class="stat-value">{escape_html(str(copy_style.get('latest_scraped_at') or 'n/a')[:19])}</span></div>
  </div>

  <!-- Panel 6: Auto Ops -->
  <div class="panel">
    <h2>Auto Ops</h2>
    <div class="stat-row"><span class="stat-label">Tracker total</span><span class="stat-value">{ops_total}</span></div>
    <div class="stat-row"><span class="stat-label">GENERATED</span><span class="stat-value">{ops_generated}</span></div>
    <div class="stat-row"><span class="stat-label">READY_TO_DEPLOY</span><span class="stat-value {'green' if ops_ready else 'amber'}">{ops_ready}</span></div>
    <div class="mono">{ops_cat_preview}</div>
  </div>

  <!-- Panel 5: Recent Run Ledger -->
  <div class="panel">
    <h2>Recent Run Ledger</h2>
    <table class="table">
      <thead><tr><th>ts</th><th>step</th><th>status</th><th>dur</th></tr></thead>
      <tbody>
        {''.join([f"<tr><td>{r.get('timestamp','')}</td><td>{r.get('step_id','')}</td><td>{r.get('status','')}</td><td>{r.get('duration_sec','')}</td></tr>" for r in reversed(runs_tail)])}
      </tbody>
    </table>
  </div>

  <!-- Panel 6: Runtime Stack -->
  <div class="panel">
    <h2>Runtime Stack</h2>
    <div class="mono">{stack_heartbeat}</div>
  </div>

  <!-- Panel 7: RBI Portfolio -->
  <div class="panel">
    <h2>RBI Portfolio</h2>
    <div class="mono">{rbi_todo}</div>
  </div>

  <!-- Panel 8: Content QA -->
  <div class="panel">
    <h2>Content QA</h2>
    <div class="stat-row"><span class="stat-label">QA total</span><span class="stat-value">{qa_stats.get('total', 0)}</span></div>
    <div class="stat-row"><span class="stat-label">PENDING_REVIEW</span><span class="stat-value {'amber' if qa_pending else 'green'}">{qa_pending}</span></div>
    <div class="stat-row"><span class="stat-label">NEEDS_STYLE_FIX</span><span class="stat-value {'amber' if qa_needs_style else 'green'}">{qa_needs_style}</span></div>
    <div class="stat-row"><span class="stat-label">APPROVED*</span><span class="stat-value green">{qa_approved}</span></div>
    <div class="mono">Auto-approval scope: IG carousels only (AI-disclosed).</div>
  </div>

  <!-- Panel 9: Publish Packs -->
  <div class="panel">
    <h2>Publish Packs</h2>
    <div class="stat-row"><span class="stat-label">Pack items</span><span class="stat-value {'amber' if pack_stats.get('total', 0) else 'green'}">{pack_stats.get('total', 0)}</span></div>
    <div class="stat-row"><span class="stat-label">By platform</span><span class="stat-value">{', '.join([f"{k}:{v}" for k, v in (pack_stats.get('by_platform', {}) or {}).items()]) or 'n/a'}</span></div>
    <div class="stat-row"><span class="stat-label">Latest preview</span><span class="stat-value">{(f"<a class='link' href='{latest_preview_href}'>open</a>" if latest_preview_href else 'n/a')}</span></div>
    <div class="mono">Manifest: output/publish_packs/manifest.json</div>
  </div>

  <!-- Panel 10: Ecom -->
  <div class="panel">
    <h2>Ecom</h2>
    <div class="stat-row"><span class="stat-label">Top arb items</span><span class="stat-value {'amber' if ecom.get('top_arb_count', 0) else 'green'}">{ecom.get('top_arb_count', 0)}</span></div>
    <div class="stat-row"><span class="stat-label">Latest pack</span><span class="stat-value">{(f"<a class='link' href='{ecom.get('latest_href')}'>open</a>" if ecom.get('latest_href') else 'n/a')}</span></div>
    <div class="mono">{ecom_preview}</div>
  </div>

  <!-- Panel 10B: Ecom Auto-List -->
  <div class="panel">
    <h2>Ecom Auto-List</h2>
    <div class="stat-row"><span class="stat-label">Catalog</span><span class="stat-value">{ecom_autolist.get('catalog_count', 0)}</span></div>
    <div class="stat-row"><span class="stat-label">LIVE</span><span class="stat-value {'amber' if (ecom_autolist.get('live_count', 0) == 0) else 'green'}">{ecom_autolist.get('live_count', 0)}</span></div>
    <div class="stat-row"><span class="stat-label">Pending</span><span class="stat-value {'amber' if ecom_autolist.get('pending_count', 0) else 'green'}">{ecom_autolist.get('pending_count', 0)}</span></div>
    <div class="stat-row"><span class="stat-label">Latest report</span><span class="stat-value">{(f"<a class='link' href='{ecom_autolist.get('latest_href')}'>open</a>" if ecom_autolist.get('latest_href') else 'n/a')}</span></div>
    <div class="mono">{ecom_autolist_preview}</div>
  </div>

  <!-- Panel 10C: Ecom Autopilot -->
  <div class="panel">
    <h2>Ecom Autopilot</h2>
    <div class="stat-row"><span class="stat-label">Winners</span><span class="stat-value {'amber' if (ecom_autopilot.get('winners_count', 0) == 0) else 'green'}">{ecom_autopilot.get('winners_count', 0)}</span></div>
    <div class="stat-row"><span class="stat-label">Queue rows</span><span class="stat-value">{ecom_autopilot.get('total_queue', 0)}</span></div>
    <div class="stat-row"><span class="stat-label">Auto-ready</span><span class="stat-value {'green' if ecom_autopilot.get('auto_ready', 0) else 'amber'}">{ecom_autopilot.get('auto_ready', 0)}</span></div>
    <div class="stat-row"><span class="stat-label">Blocked</span><span class="stat-value {'amber' if ecom_autopilot.get('blocked', 0) else 'green'}">{ecom_autopilot.get('blocked', 0)}</span></div>
    <div class="stat-row"><span class="stat-label">Latest report</span><span class="stat-value">{(f"<a class='link' href='{ecom_autopilot.get('latest_href')}'>open</a>" if ecom_autopilot.get('latest_href') else 'n/a')}</span></div>
    <div class="mono">{ecom_autopilot_preview}</div>
  </div>

  <!-- Panel 11: Freelance -->
  <div class="panel">
    <h2>Freelance</h2>
    <div class="stat-row"><span class="stat-label">Draft responses</span><span class="stat-value {'amber' if freelance.get('draft_count', 0) else 'green'}">{freelance.get('draft_count', 0)}</span></div>
    <div class="stat-row"><span class="stat-label">Scan rows</span><span class="stat-value">{freelance.get('scan_count', 0)}</span></div>
    <div class="stat-row"><span class="stat-label">Latest pack</span><span class="stat-value">{(f"<a class='link' href='{freelance.get('latest_href')}'>open</a>" if freelance.get('latest_href') else 'n/a')}</span></div>
    <div class="mono">No posting: generates copy/paste-ready drafts only.</div>
  </div>

  <!-- Panel 12: Gov -->
  <div class="panel">
    <h2>Gov</h2>
    <div class="stat-row"><span class="stat-label">Open opps (<=60d)</span><span class="stat-value {'amber' if gov.get('open_count', 0) else 'green'}">{gov.get('open_count', 0)}</span></div>
    <div class="stat-row"><span class="stat-label">Soonest deadline</span><span class="stat-value">{gov.get('soonest_deadline') or 'n/a'}</span></div>
    <div class="stat-row"><span class="stat-label">Latest pack</span><span class="stat-value">{(f"<a class='link' href='{gov.get('latest_href')}'>open</a>" if gov.get('latest_href') else 'n/a')}</span></div>
    <div class="mono">No bidding: summarizes opportunities only.</div>
  </div>

  <!-- Panel 13: Apps -->
  <div class="panel">
    <h2>Apps</h2>
    <div class="stat-row"><span class="stat-label">Discovered</span><span class="stat-value {'amber' if apps.get('count', 0) else 'green'}">{apps.get('count', 0)}</span></div>
    <div class="stat-row"><span class="stat-label">Latest pack</span><span class="stat-value">{(f"<a class='link' href='{apps.get('latest_href')}'>open</a>" if apps.get('latest_href') else 'n/a')}</span></div>
    <div class="mono">Screenshots + metadata from ralph/loops/app_factory/output/.</div>
  </div>

  <!-- Panel 14: Native Apps -->
  <div class="panel">
    <h2>Native Apps</h2>
    <div class="stat-row"><span class="stat-label">Discovered</span><span class="stat-value {'amber' if native_apps.get('count', 0) else 'green'}">{native_apps.get('count', 0)}</span></div>
    <div class="stat-row"><span class="stat-label">Latest pack</span><span class="stat-value">{(f"<a class='link' href='{native_apps.get('latest_href')}'>open</a>" if native_apps.get('latest_href') else 'n/a')}</span></div>
    <div class="mono">Expo/RN projects discovered under app factory/app-factory/* (no submit).</div>
  </div>

  <!-- Panel 15: Launch -->
  <div class="panel">
    <h2>Launch</h2>
    <div class="stat-row"><span class="stat-label">Directories</span><span class="stat-value">{launch.get('directories_count', 0)}</span></div>
    <div class="stat-row"><span class="stat-label">Product packs</span><span class="stat-value {'amber' if launch.get('packs_count', 0) else 'green'}">{launch.get('packs_count', 0)}</span></div>
    <div class="stat-row"><span class="stat-label">Latest pack</span><span class="stat-value">{(f"<a class='link' href='{launch.get('latest_href')}'>open</a>" if launch.get('latest_href') else 'n/a')}</span></div>
    <div class="mono">Creates/updates LEDGER/LAUNCH_DIRECTORY_TRACKER.csv (no auto-submission).</div>
  </div>

  <!-- Panel 16: Clawdbot RBI -->
  <div class="panel">
    <h2>Clawdbot RBI</h2>
    <div class="stat-row"><span class="stat-label">Intent queue</span><span class="stat-value {'amber' if clawdbot.get('intent_rows', 0) else 'green'}">{clawdbot.get('intent_rows', 0)}</span></div>
    <div class="stat-row"><span class="stat-label">Syndication rows</span><span class="stat-value">{clawdbot.get('syndication_rows', 0)}</span></div>
    <div class="stat-row"><span class="stat-label">Directory wave</span><span class="stat-value">{clawdbot.get('directory_rows', 0)}</span></div>
    <div class="stat-row"><span class="stat-label">Job sniper</span><span class="stat-value">{clawdbot.get('job_rows', 0)}</span></div>
    <div class="stat-row"><span class="stat-label">Keyword gap</span><span class="stat-value">{clawdbot.get('keyword_rows', 0)}</span></div>
    <div class="stat-row"><span class="stat-label">Community queue</span><span class="stat-value">{clawdbot.get('community_rows', 0)}</span></div>
    <div class="stat-row"><span class="stat-label">Latest report</span><span class="stat-value">{(f"<a class='link' href='{clawdbot.get('latest_href')}'>open</a>" if clawdbot.get('latest_href') else 'n/a')}</span></div>
    <div class="mono">{clawdbot_preview}</div>
  </div>

  <!-- Panel 17: Cron Fleet -->
  <div class="panel">
    <h2>Cron Fleet</h2>
    <div class="stat-row"><span class="stat-label">Tracked logs</span><span class="stat-value">{cron_fleet.get('logs_count', 0)}</span></div>
    <div class="stat-row"><span class="stat-label">Key artifacts</span><span class="stat-value">{cron_fleet.get('artifacts_count', 0)}</span></div>
    <div class="stat-row"><span class="stat-label">Latest report</span><span class="stat-value">{(f"<a class='link' href='{cron_fleet.get('latest_href')}'>open</a>" if cron_fleet.get('latest_href') else 'n/a')}</span></div>
    <div class="mono">{escape_html('\\n'.join([f"- {it.get('relpath','')} ({it.get('age_min','')}m)" for it in (cron_fleet.get('logs') or []) if isinstance(it, dict)]) or 'No cron fleet data yet.')}</div>
  </div>
</div>
</body>
</html>"""

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    tmp = OUTPUT_FILE.with_suffix(".html.tmp")
    try:
        tmp.write_text(html, encoding='utf-8')
        tmp.rename(OUTPUT_FILE)
    except OSError as e:
        print(f"[DASHBOARD] WARNING: Failed to write dashboard: {e}")
        try:
            tmp.unlink(missing_ok=True)
        except Exception:
            pass
    return OUTPUT_FILE


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--no-open', action='store_true')
    args = parser.parse_args()

    path = generate_dashboard()
    print(f"Dashboard generated: {path}")
    print(f"  Human queue: {len(load_human_queue())}")

    if not args.no_open:
        import subprocess
        subprocess.run(["open", str(path)])
        print("  Opened in browser")


if __name__ == "__main__":
    main()
