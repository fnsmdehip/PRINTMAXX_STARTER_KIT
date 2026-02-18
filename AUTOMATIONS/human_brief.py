#!/usr/bin/env python3
"""
PRINTMAXX Human Execution Brief
==============================

Writes a single "what to do next" brief for the human/VA.
No account automation. No posting. Just surfaces the current state.
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path


BASE = Path(__file__).resolve().parent.parent
OPS = BASE / "OPS"
OUT = BASE / "output"

HUMAN_QUEUE = OPS / "HUMAN_LOOP_QUEUE.md"
MANIFEST = OUT / "publish_packs" / "manifest.json"
BRIEF = OPS / "HUMAN_EXECUTION_BRIEF.md"

ECOM_MANIFEST = OUT / "ecom" / "manifest.json"
ECOM_PACK = OUT / "ecom" / "latest.md"
FREELANCE_MANIFEST = OUT / "freelance" / "manifest.json"
FREELANCE_PACK = OUT / "freelance" / "latest.md"
GOV_MANIFEST = OUT / "gov" / "manifest.json"
GOV_PACK = OUT / "gov" / "latest.md"
APPS_MANIFEST = OUT / "apps" / "manifest.json"
APPS_PACK = OUT / "apps" / "latest.md"
NATIVE_APPS_MANIFEST = OUT / "native_apps" / "manifest.json"
NATIVE_APPS_PACK = OUT / "native_apps" / "latest.md"
LAUNCH_MANIFEST = OUT / "launch" / "manifest.json"
LAUNCH_PACK = OUT / "launch" / "latest.md"
CLAWDBOT_MANIFEST = OUT / "clawdbot" / "manifest.json"
CLAWDBOT_PACK = OUT / "clawdbot" / "latest.md"
CLAWWORK_MANIFEST = OUT / "clawwork_sidecar" / "manifest.json"
CLAWWORK_PACK = OUT / "clawwork_sidecar" / "latest.md"


def now_iso() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def read_text(p: Path) -> str:
    try:
        return p.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return ""


def load_manifest() -> dict:
    if not MANIFEST.exists():
        return {"items": []}
    try:
        payload = json.loads(MANIFEST.read_text(encoding="utf-8"))
        if isinstance(payload, dict):
            payload.setdefault("items", [])
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


def as_float(value: object, default: float = 0.0) -> float:
    try:
        return float(str(value).strip())
    except Exception:
        return default


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true")
    args = ap.parse_args()

    if not args.write:
        ap.print_help()
        return 2

    queue_text = read_text(HUMAN_QUEUE)
    manifest = load_manifest()
    items = manifest.get("items", [])
    if not isinstance(items, list):
        items = []

    buffer_dir = OUT / "publish_packs" / "buffer"
    buffer_files = sorted(buffer_dir.glob("*.csv")) if buffer_dir.exists() else []

    ecom = load_json(ECOM_MANIFEST)
    freelance = load_json(FREELANCE_MANIFEST)
    gov = load_json(GOV_MANIFEST)
    apps = load_json(APPS_MANIFEST)
    native_apps = load_json(NATIVE_APPS_MANIFEST)
    launch = load_json(LAUNCH_MANIFEST)
    clawdbot = load_json(CLAWDBOT_MANIFEST)
    clawwork = load_json(CLAWWORK_MANIFEST)

    # Latest 5 items (newest last in manifest right now).
    latest = [it for it in items[-5:] if isinstance(it, dict)]

    lines = []
    lines.append("# Human Execution Brief")
    lines.append("")
    lines.append(f"Generated: {now_iso()}")
    lines.append("")

    lines.append("## Publish Packs (Ready)")
    lines.append("")
    lines.append(f"- Total items: {len(items)}")
    if not latest:
        lines.append("- Latest: none")
    else:
        for it in reversed(latest):
            pid = (it.get("persona_id") or "").strip()
            plat = (it.get("platform") or "").strip()
            ctype = (it.get("content_type") or "").strip()
            sched = it.get("scheduled") if isinstance(it.get("scheduled"), dict) else {}
            d = (sched.get("date") or "").strip()
            t = (sched.get("time") or "").strip()
            preview = (it.get("preview_output_rel") or "").strip()
            preview_path = (OUT / preview).resolve() if preview else None
            preview_str = str(preview_path) if preview_path and preview_path.exists() else ""
            buf = (it.get("buffer_csv") or "").strip()
            lines.append(f"- {plat}/{ctype} persona={pid or 'n/a'} scheduled={d} {t}")
            if preview_str:
                lines.append(f"  - preview: {preview_str}")
            if buf:
                lines.append(f"  - buffer_csv: {buf}")

    lines.append("")
    lines.append("## Buffer CSVs (Upload Targets)")
    lines.append("")
    if not buffer_files:
        lines.append("- None")
    else:
        for p in buffer_files:
            lines.append(f"- {p}")

    lines.append("")
    lines.append("## Ecom Pack (No Posting)")
    lines.append("")
    if ECOM_PACK.exists():
        lines.append(f"- Pack: {ECOM_PACK}")
    else:
        lines.append("- Pack: none yet (expected: output/ecom/latest.md)")
    top_arb = ecom.get("top_arb") if isinstance(ecom.get("top_arb"), list) else []
    if top_arb:
        lines.append(f"- Top arb items: {len(top_arb)}")
        for it in top_arb[:5]:
            if not isinstance(it, dict):
                continue
            product = (it.get("product") or "").strip()
            profit = it.get("net_profit")
            margin = it.get("margin_pct")
            platform = (it.get("best_platform") or "").strip()
            lines.append(f"  - {product} profit={profit} margin={margin} platform={platform}")
    else:
        lines.append("- Top arb items: none")
    lines.append("")

    lines.append("## Freelance Pack (No Posting)")
    lines.append("")
    if FREELANCE_PACK.exists():
        lines.append(f"- Pack: {FREELANCE_PACK}")
    else:
        lines.append("- Pack: none yet (expected: output/freelance/latest.md)")
    draft_count = freelance.get("draft_count")
    if isinstance(draft_count, int):
        lines.append(f"- Draft responses (last 72h): {draft_count}")
    lines.append("")

    lines.append("## Gov Bid Pack (No Bidding)")
    lines.append("")
    if GOV_PACK.exists():
        lines.append(f"- Pack: {GOV_PACK}")
    else:
        lines.append("- Pack: none yet (expected: output/gov/latest.md)")
    open_count = gov.get("open_count")
    if isinstance(open_count, int):
        lines.append(f"- Open opportunities (deadline <= 60d): {open_count}")
    lines.append("")

    lines.append("## App Pack (No Deploy)")
    lines.append("")
    if APPS_PACK.exists():
        lines.append(f"- Pack: {APPS_PACK}")
    else:
        lines.append("- Pack: none yet (expected: output/apps/latest.md)")
    app_count = apps.get("count")
    if isinstance(app_count, int):
        lines.append(f"- Apps discovered: {app_count}")
    lines.append("")

    lines.append("## Native App Pack (No Submit)")
    lines.append("")
    if NATIVE_APPS_PACK.exists():
        lines.append(f"- Pack: {NATIVE_APPS_PACK}")
    else:
        lines.append("- Pack: none yet (expected: output/native_apps/latest.md)")
    native_count = native_apps.get("count")
    if isinstance(native_count, int):
        lines.append(f"- Native apps discovered: {native_count}")
    lines.append("")

    lines.append("## Launch Pack (No Auto-Submission)")
    lines.append("")
    if LAUNCH_PACK.exists():
        lines.append(f"- Pack: {LAUNCH_PACK}")
    else:
        lines.append("- Pack: none yet (expected: output/launch/latest.md)")
    dirs_count = launch.get("directories_count")
    if isinstance(dirs_count, int):
        lines.append(f"- Directories active: {dirs_count}")
    packs = launch.get("packs") if isinstance(launch.get("packs"), list) else []
    if packs:
        lines.append(f"- Product packs: {len(packs)}")
    lines.append("")

    lines.append("## Clawdbot RBI Pack (Draft Queues)")
    lines.append("")
    if CLAWDBOT_PACK.exists():
        lines.append(f"- Pack: {CLAWDBOT_PACK}")
    else:
        lines.append("- Pack: none yet (expected: output/clawdbot/latest.md)")
    c = clawdbot.get("counts") if isinstance(clawdbot.get("counts"), dict) else {}
    lines.append(f"- Intent queue rows: {int(c.get('intent_rows') or 0)}")
    lines.append(f"- Syndication rows: {int(c.get('syndication_rows') or 0)}")
    lines.append(f"- Directory wave rows: {int(c.get('directory_rows') or 0)}")
    lines.append(f"- Job-sniper rows: {int(c.get('job_rows') or 0)}")
    lines.append(f"- Keyword-gap rows: {int(c.get('keyword_rows') or 0)}")
    lines.append(f"- Community rows: {int(c.get('community_rows') or 0)}")
    lines.append("")

    lines.append("## ClawWork Sidecar (Economic Benchmark)")
    lines.append("")
    if CLAWWORK_PACK.exists():
        lines.append(f"- Pack: {CLAWWORK_PACK}")
    else:
        lines.append("- Pack: none yet (expected: output/clawwork_sidecar/latest.md)")
    cw_budget = clawwork.get("budget") if isinstance(clawwork.get("budget"), dict) else {}
    cw_totals = clawwork.get("totals") if isinstance(clawwork.get("totals"), dict) else {}
    cw_top = clawwork.get("top_lanes") if isinstance(clawwork.get("top_lanes"), list) else []
    lines.append(f"- Budget state: {cw_budget.get('budget_state', 'UNKNOWN')}")
    lines.append(f"- Estimated eval cost (this run): ${as_float(cw_totals.get('estimated_eval_cost_usd')):.2f}")
    lines.append(f"- Expected sampled profit: ${as_float(cw_totals.get('expected_profit_usd')):.2f}")
    if cw_top:
        top_lane = cw_top[0] if isinstance(cw_top[0], dict) else {}
        lines.append(f"- Top lane: {top_lane.get('lane', 'n/a')} (profit=${as_float(top_lane.get('expected_profit_usd')):.2f})")
    else:
        lines.append("- Top lane: n/a")
    lines.append("")

    lines.append("")
    lines.append("## Human Loop Queue (Blockers / Approvals)")
    lines.append("")
    if queue_text.strip():
        # Include as-is so the checklist stays the single source of truth.
        lines.append(queue_text.strip())
    else:
        lines.append("- HUMAN_LOOP_QUEUE.md missing or empty.")
    lines.append("")

    BRIEF.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"human_brief: wrote {BRIEF}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
