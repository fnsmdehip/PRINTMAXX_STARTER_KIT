#!/usr/bin/env python3
"""PRINTMAXX ClawWork minimal sidecar.

Purpose:
  - Add an economic benchmark layer on top of existing PRINTMAXX queues.
  - Keep runs safe-by-default: score and recommend, never live-send.
  - Enforce strict budget caps so evaluation never breaks the $200/mo stack.

This does not replace Ship Captain. It acts as a budgeted shadow evaluator.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List


BASE_DIR = Path(__file__).resolve().parent.parent
OPS_DIR = BASE_DIR / "OPS"
LEDGER_DIR = BASE_DIR / "LEDGER"
OUT_DIR = BASE_DIR / "output" / "clawwork_sidecar"

POLICY_JSON = OPS_DIR / "CLAWWORK_SIDECAR_POLICY.json"
MANIFEST_JSON = OUT_DIR / "manifest.json"
LATEST_MD = OUT_DIR / "latest.md"
RUNS_CSV = LEDGER_DIR / "CLAWWORK_SIDECAR_RUNS.csv"


def now_iso() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def _safe_float(v: object, default: float = 0.0) -> float:
    try:
        return float(str(v).strip())
    except Exception:
        return default


def _safe_int(v: object, default: int = 0) -> int:
    try:
        return int(float(str(v).strip()))
    except Exception:
        return default


def _default_policy() -> Dict[str, Any]:
    return {
        "version": "2026-02-16",
        "enabled": True,
        "budget": {
            "monthly_cap_usd": 20.0,
            "soft_cap_usd": 15.0,
            "hard_stop_usd": 18.0,
            "per_run_cap_usd": 1.0,
            "cost_per_eval_usd": 0.012,
        },
        "sampling": {
            "max_total_tasks_per_run": 30,
            "max_tasks_per_lane": 12,
        },
        "lanes": {
            "freelance_arbitrage": {
                "priority": 100,
                "source": "output/freelance/manifest.json",
                "queue_field": "draft_count",
                "win_rate": 0.08,
                "value_per_win_usd": 225.0,
                "quality_factor": 0.75,
                "human_blocker": "FIVERR_UPWORK_ACCOUNT",
            },
            "gumroad_listings": {
                "priority": 95,
                "source": "output/ecom_autolist/manifest.json",
                "queue_field": "pending_count",
                "win_rate": 0.22,
                "value_per_win_usd": 19.0,
                "quality_factor": 0.90,
                "human_blocker": "GUMROAD_ACCOUNT",
            },
            "cold_outreach_warmup": {
                "priority": 90,
                "source": "output/cold_emails/cold_emails_ready.csv",
                "queue_field": "csv_rows",
                "win_rate": 0.02,
                "value_per_win_usd": 300.0,
                "quality_factor": 0.70,
                "human_blocker": "EMAIL_INFRA",
            },
            "rbi_intent_sniping": {
                "priority": 80,
                "source": "output/clawdbot/manifest.json",
                "queue_field": "counts.intent_rows",
                "win_rate": 0.03,
                "value_per_win_usd": 180.0,
                "quality_factor": 0.70,
                "human_blocker": "X_MULTI_ACCOUNT_STACK",
            },
        },
        "external_runner": {
            "enabled": False,
            "clawwork_home": "",
            "command": "bash run_test_agent.sh",
            "timeout_sec": 1800,
            "estimated_cost_usd": 0.5,
        },
    }


def load_policy() -> Dict[str, Any]:
    policy = _default_policy()
    if not POLICY_JSON.exists():
        return policy
    try:
        loaded = json.loads(POLICY_JSON.read_text(encoding="utf-8"))
    except Exception:
        return policy
    if not isinstance(loaded, dict):
        return policy
    # Keep defaults for missing keys.
    for key in ("version", "enabled", "budget", "sampling", "lanes", "external_runner"):
        if key in loaded:
            policy[key] = loaded[key]
    return policy


def load_json(path: Path) -> Dict[str, Any]:
    if not path.exists():
        return {}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
        return payload if isinstance(payload, dict) else {}
    except Exception:
        return {}


def get_nested(payload: Dict[str, Any], dotted_key: str) -> Any:
    cur: Any = payload
    for part in dotted_key.split("."):
        if isinstance(cur, dict):
            cur = cur.get(part)
        else:
            return None
    return cur


def count_csv_rows(path: Path) -> int:
    if not path.exists():
        return 0
    try:
        with open(path, "r", encoding="utf-8", errors="replace", newline="") as f:
            reader = csv.reader(f)
            # Subtract header if present.
            count = -1
            for _ in reader:
                count += 1
            return max(0, count)
    except Exception:
        return 0


def ensure_runs_csv() -> None:
    LEDGER_DIR.mkdir(parents=True, exist_ok=True)
    if RUNS_CSV.exists():
        return
    with open(RUNS_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(
            [
                "timestamp",
                "budget_state",
                "sampled_tasks",
                "estimated_cost_usd",
                "expected_revenue_usd",
                "expected_profit_usd",
                "external_status",
                "notes",
            ]
        )


def month_spend_usd() -> float:
    ensure_runs_csv()
    month_prefix = datetime.now().strftime("%Y-%m")
    total = 0.0
    with open(RUNS_CSV, "r", encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            ts = (row.get("timestamp") or "").strip()
            if not ts.startswith(month_prefix):
                continue
            total += _safe_float(row.get("estimated_cost_usd"), 0.0)
    return round(total, 6)


def queue_count_for_lane(source_rel: str, queue_field: str) -> Dict[str, Any]:
    source_path = Path(source_rel)
    if not source_path.is_absolute():
        source_path = BASE_DIR / source_path
    source_path = source_path.resolve()
    exists = source_path.exists()

    queue_count = 0
    if exists and source_path.suffix.lower() == ".csv":
        if queue_field == "csv_rows":
            queue_count = count_csv_rows(source_path)
    elif exists and source_path.suffix.lower() == ".json":
        payload = load_json(source_path)
        raw = get_nested(payload, queue_field)
        queue_count = max(0, _safe_int(raw, 0))

    return {
        "source": str(source_path),
        "exists": exists,
        "queue_count": queue_count,
    }


def run_external_runner(policy: Dict[str, Any], invoke_external: bool) -> Dict[str, Any]:
    result: Dict[str, Any] = {
        "attempted": False,
        "status": "SKIPPED",
        "exit_code": 0,
        "notes": "External run disabled.",
        "output_tail": "",
    }
    if not invoke_external:
        return result

    cfg = policy.get("external_runner", {})
    if not isinstance(cfg, dict) or not bool(cfg.get("enabled", False)):
        result["notes"] = "Policy external_runner.enabled is false."
        return result

    home = str(cfg.get("clawwork_home", "")).strip()
    command = str(cfg.get("command", "")).strip()
    timeout_sec = max(30, _safe_int(cfg.get("timeout_sec"), 1800))
    if not home or not command:
        result["notes"] = "Missing clawwork_home or command in policy."
        return result

    home_path = Path(home).expanduser().resolve()
    if not home_path.exists():
        result["notes"] = f"clawwork_home not found: {home_path}"
        return result

    result["attempted"] = True
    try:
        proc = subprocess.run(
            ["bash", "-lc", command],
            cwd=home_path,
            capture_output=True,
            text=True,
            timeout=timeout_sec,
            check=False,
        )
        merged = ((proc.stdout or "") + ("\n" + proc.stderr if proc.stderr else "")).strip()
        result["status"] = "OK" if proc.returncode == 0 else "FAILED"
        result["exit_code"] = int(proc.returncode)
        result["notes"] = f"Ran in {home_path}"
        result["output_tail"] = merged[-600:]
        return result
    except subprocess.TimeoutExpired:
        result["status"] = "TIMEOUT"
        result["exit_code"] = 124
        result["notes"] = f"Timed out after {timeout_sec}s"
        return result
    except Exception as exc:
        result["status"] = "FAILED"
        result["exit_code"] = 1
        result["notes"] = str(exc)
        return result


def build_assessment(policy: Dict[str, Any], max_total_override: int, invoke_external: bool) -> Dict[str, Any]:
    budget_cfg = policy.get("budget", {}) if isinstance(policy.get("budget"), dict) else {}
    sampling_cfg = policy.get("sampling", {}) if isinstance(policy.get("sampling"), dict) else {}
    lanes_cfg = policy.get("lanes", {}) if isinstance(policy.get("lanes"), dict) else {}

    monthly_cap = max(0.0, _safe_float(budget_cfg.get("monthly_cap_usd"), 20.0))
    soft_cap = max(0.0, _safe_float(budget_cfg.get("soft_cap_usd"), 15.0))
    hard_stop = max(0.0, _safe_float(budget_cfg.get("hard_stop_usd"), 18.0))
    per_run_cap = max(0.0, _safe_float(budget_cfg.get("per_run_cap_usd"), 1.0))
    cost_per_eval = max(0.0, _safe_float(budget_cfg.get("cost_per_eval_usd"), 0.012))

    # Keep hard stop no higher than monthly cap.
    hard_ceiling = min(monthly_cap, hard_stop) if monthly_cap > 0 else hard_stop
    month_spend_before = month_spend_usd()
    remaining_month = max(0.0, hard_ceiling - month_spend_before)
    run_budget_remaining = min(per_run_cap, remaining_month)

    if remaining_month <= 0.0:
        budget_state = "HARD_STOP"
    elif month_spend_before >= soft_cap:
        budget_state = "SOFT_CAP"
    else:
        budget_state = "NORMAL"

    max_total = _safe_int(sampling_cfg.get("max_total_tasks_per_run"), 30)
    if max_total_override > 0:
        max_total = max_total_override
    max_lane = max(1, _safe_int(sampling_cfg.get("max_tasks_per_lane"), 12))
    tasks_left = max(0, max_total)

    lane_items: List[Dict[str, Any]] = []
    blockers: List[str] = []
    lane_list: List[tuple[str, Dict[str, Any]]] = [
        (name, cfg) for name, cfg in lanes_cfg.items() if isinstance(cfg, dict)
    ]
    lane_list.sort(key=lambda it: _safe_int(it[1].get("priority"), 0), reverse=True)

    for lane_name, cfg in lane_list:
        source_rel = str(cfg.get("source", "")).strip()
        queue_field = str(cfg.get("queue_field", "csv_rows")).strip()
        stats = queue_count_for_lane(source_rel, queue_field)
        queue_count = max(0, _safe_int(stats.get("queue_count"), 0))
        target_sample = min(queue_count, max_lane, tasks_left)

        if budget_state == "HARD_STOP" or cost_per_eval <= 0:
            sample_count = 0
        else:
            max_affordable = int(math.floor(run_budget_remaining / cost_per_eval)) if cost_per_eval > 0 else 0
            sample_count = min(target_sample, max_affordable)

        win_rate = max(0.0, _safe_float(cfg.get("win_rate"), 0.0))
        value_per_win = max(0.0, _safe_float(cfg.get("value_per_win_usd"), 0.0))
        quality_factor = min(1.0, max(0.0, _safe_float(cfg.get("quality_factor"), 0.75)))

        eval_cost = round(sample_count * cost_per_eval, 6)
        expected_revenue = round(sample_count * win_rate * value_per_win * quality_factor, 6)
        expected_profit = round(expected_revenue - eval_cost, 6)
        roi = round((expected_profit / eval_cost), 4) if eval_cost > 0 else 0.0

        run_budget_remaining = max(0.0, run_budget_remaining - eval_cost)
        tasks_left = max(0, tasks_left - sample_count)

        blocker = str(cfg.get("human_blocker", "")).strip().upper()
        if blocker and queue_count > 0:
            blockers.append(blocker)

        lane_items.append(
            {
                "lane": lane_name,
                "priority": _safe_int(cfg.get("priority"), 0),
                "source": stats.get("source", ""),
                "source_exists": bool(stats.get("exists")),
                "queue_count": queue_count,
                "sample_count": sample_count,
                "win_rate": win_rate,
                "value_per_win_usd": value_per_win,
                "quality_factor": quality_factor,
                "estimated_eval_cost_usd": eval_cost,
                "expected_revenue_usd": expected_revenue,
                "expected_profit_usd": expected_profit,
                "roi": roi,
                "human_blocker": blocker,
            }
        )

    external = run_external_runner(policy, invoke_external)

    total_queue = sum(_safe_int(x.get("queue_count"), 0) for x in lane_items)
    total_samples = sum(_safe_int(x.get("sample_count"), 0) for x in lane_items)
    total_eval_cost = round(sum(_safe_float(x.get("estimated_eval_cost_usd"), 0.0) for x in lane_items), 6)
    total_revenue = round(sum(_safe_float(x.get("expected_revenue_usd"), 0.0) for x in lane_items), 6)
    total_profit = round(total_revenue - total_eval_cost, 6)
    if external.get("attempted") and external.get("status") == "OK":
        extra_cost = _safe_float(policy.get("external_runner", {}).get("estimated_cost_usd"), 0.0)
        total_eval_cost = round(total_eval_cost + max(0.0, extra_cost), 6)
        total_profit = round(total_revenue - total_eval_cost, 6)

    top_lanes = sorted(
        lane_items,
        key=lambda x: _safe_float(x.get("expected_profit_usd"), 0.0),
        reverse=True,
    )[:3]

    payload: Dict[str, Any] = {
        "generated_at": now_iso(),
        "policy_version": str(policy.get("version", "unknown")),
        "enabled": bool(policy.get("enabled", True)),
        "budget": {
            "monthly_cap_usd": monthly_cap,
            "soft_cap_usd": soft_cap,
            "hard_stop_usd": hard_ceiling,
            "per_run_cap_usd": per_run_cap,
            "cost_per_eval_usd": cost_per_eval,
            "month_spend_before_usd": round(month_spend_before, 6),
            "month_spend_after_usd": round(month_spend_before + total_eval_cost, 6),
            "month_remaining_usd": round(max(0.0, hard_ceiling - (month_spend_before + total_eval_cost)), 6),
            "budget_state": budget_state,
        },
        "totals": {
            "queue_tasks": total_queue,
            "sampled_tasks": total_samples,
            "estimated_eval_cost_usd": total_eval_cost,
            "expected_revenue_usd": total_revenue,
            "expected_profit_usd": total_profit,
        },
        "lanes": lane_items,
        "top_lanes": [
            {
                "lane": x.get("lane", ""),
                "expected_profit_usd": x.get("expected_profit_usd", 0.0),
                "sample_count": x.get("sample_count", 0),
            }
            for x in top_lanes
        ],
        "blockers": sorted(set([b for b in blockers if b])),
        "external_runner": external,
        "notes": {
            "mode": "sidecar_only",
            "live_actions": "disabled",
            "approval_required_for_account_or_payment_actions": True,
        },
    }
    return payload


def write_outputs(payload: Dict[str, Any]) -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    MANIFEST_JSON.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    budget = payload.get("budget", {}) if isinstance(payload.get("budget"), dict) else {}
    totals = payload.get("totals", {}) if isinstance(payload.get("totals"), dict) else {}
    lanes = payload.get("lanes", []) if isinstance(payload.get("lanes"), list) else []
    blockers = payload.get("blockers", []) if isinstance(payload.get("blockers"), list) else []
    external = payload.get("external_runner", {}) if isinstance(payload.get("external_runner"), dict) else {}

    lines: List[str] = []
    lines.append("# ClawWork Sidecar (Economic Benchmark)")
    lines.append("")
    lines.append(f"Generated: {payload.get('generated_at', '')}")
    lines.append(f"Policy version: {payload.get('policy_version', 'unknown')}")
    lines.append("")
    lines.append("## Budget Guard")
    lines.append("")
    lines.append(f"- Budget state: `{budget.get('budget_state', 'UNKNOWN')}`")
    lines.append(f"- Monthly cap: ${_safe_float(budget.get('monthly_cap_usd')):.2f}")
    lines.append(f"- Hard stop: ${_safe_float(budget.get('hard_stop_usd')):.2f}")
    lines.append(f"- Month spend (before run): ${_safe_float(budget.get('month_spend_before_usd')):.2f}")
    lines.append(f"- Month spend (after run): ${_safe_float(budget.get('month_spend_after_usd')):.2f}")
    lines.append(f"- Month remaining: ${_safe_float(budget.get('month_remaining_usd')):.2f}")
    lines.append("")
    lines.append("## Economic Snapshot")
    lines.append("")
    lines.append(f"- Queue tasks observed: {int(_safe_int(totals.get('queue_tasks')))}")
    lines.append(f"- Tasks sampled this run: {int(_safe_int(totals.get('sampled_tasks')))}")
    lines.append(f"- Estimated eval cost: ${_safe_float(totals.get('estimated_eval_cost_usd')):.2f}")
    lines.append(f"- Expected revenue from sampled tasks: ${_safe_float(totals.get('expected_revenue_usd')):.2f}")
    lines.append(f"- Expected profit from sampled tasks: ${_safe_float(totals.get('expected_profit_usd')):.2f}")
    lines.append("")
    lines.append("## Lane Scores")
    lines.append("")
    lines.append("| lane | queue | sampled | eval_cost | exp_revenue | exp_profit | blocker |")
    lines.append("|---|---:|---:|---:|---:|---:|---|")
    for lane in lanes:
        lines.append(
            "| {lane} | {queue} | {sampled} | ${cost:.2f} | ${rev:.2f} | ${profit:.2f} | `{blocker}` |".format(
                lane=str(lane.get("lane", "")),
                queue=int(_safe_int(lane.get("queue_count"))),
                sampled=int(_safe_int(lane.get("sample_count"))),
                cost=_safe_float(lane.get("estimated_eval_cost_usd")),
                rev=_safe_float(lane.get("expected_revenue_usd")),
                profit=_safe_float(lane.get("expected_profit_usd")),
                blocker=str(lane.get("human_blocker", "") or "NONE"),
            )
        )
    lines.append("")
    lines.append("## First 3 Revenue Triggers")
    lines.append("")
    lines.append("1. Freelance arbitrage warm run: `python3 AUTOMATIONS/freelance_demand_scanner.py --hourly` then `python3 AUTOMATIONS/auto_freelance_responder.py --dry-run`.")
    lines.append("2. Gumroad listing prep run: `python3 AUTOMATIONS/gumroad_autolist_packager.py --write` and keep `AUTO_LIST_ECOM` approval gated.")
    lines.append("3. Cold outreach warmup run: `python3 AUTOMATIONS/email_sender.py --preview --outreach AUTOMATIONS/outreach/HOT_BATCH_FEB13_COMPLIANT.csv --max-sends 25`.")
    lines.append("")
    lines.append("## Human Blockers")
    lines.append("")
    if blockers:
        for blocker in blockers:
            lines.append(f"- `{blocker}`")
    else:
        lines.append("- None")
    lines.append("")
    lines.append("## External ClawWork Runner")
    lines.append("")
    lines.append(f"- Attempted: {'yes' if external.get('attempted') else 'no'}")
    lines.append(f"- Status: {external.get('status', 'SKIPPED')}")
    lines.append(f"- Notes: {external.get('notes', '')}")
    output_tail = str(external.get("output_tail", "")).strip()
    if output_tail:
        lines.append("")
        lines.append("```text")
        lines.append(output_tail)
        lines.append("```")
    lines.append("")

    LATEST_MD.write_text("\n".join(lines), encoding="utf-8")


def append_run_ledger(payload: Dict[str, Any]) -> None:
    ensure_runs_csv()
    budget = payload.get("budget", {}) if isinstance(payload.get("budget"), dict) else {}
    totals = payload.get("totals", {}) if isinstance(payload.get("totals"), dict) else {}
    top = payload.get("top_lanes", []) if isinstance(payload.get("top_lanes"), list) else []
    external = payload.get("external_runner", {}) if isinstance(payload.get("external_runner"), dict) else {}
    top_names = ",".join([str(x.get("lane", "")).strip() for x in top if isinstance(x, dict) and x.get("lane")])
    with open(RUNS_CSV, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(
            [
                now_iso(),
                str(budget.get("budget_state", "UNKNOWN")),
                int(_safe_int(totals.get("sampled_tasks"))),
                round(_safe_float(totals.get("estimated_eval_cost_usd")), 6),
                round(_safe_float(totals.get("expected_revenue_usd")), 6),
                round(_safe_float(totals.get("expected_profit_usd")), 6),
                str(external.get("status", "SKIPPED")),
                top_names,
            ]
        )


def parse_args() -> argparse.Namespace:
    ap = argparse.ArgumentParser(description="PRINTMAXX ClawWork sidecar")
    ap.add_argument("--tick", action="store_true", help="Run one sidecar evaluation tick")
    ap.add_argument("--write", action="store_true", help="Alias for --tick")
    ap.add_argument("--dry-run", action="store_true", help="Write outputs but do not append run ledger")
    ap.add_argument("--max-total", type=int, default=0, help="Override max sampled tasks per run")
    ap.add_argument(
        "--invoke-external",
        action="store_true",
        help="Attempt external ClawWork runner defined in OPS/CLAWWORK_SIDECAR_POLICY.json",
    )
    return ap.parse_args()


def main() -> int:
    args = parse_args()
    if not args.tick and not args.write:
        print("clawwork_sidecar: pass --tick (or --write)")
        return 2

    policy = load_policy()
    if not bool(policy.get("enabled", True)):
        print("clawwork_sidecar: disabled by policy")
        return 0

    payload = build_assessment(
        policy=policy,
        max_total_override=max(0, args.max_total),
        invoke_external=bool(args.invoke_external),
    )
    write_outputs(payload)
    if not args.dry_run:
        append_run_ledger(payload)
    print(f"clawwork_sidecar: wrote {MANIFEST_JSON} and {LATEST_MD}")
    if args.dry_run:
        print("clawwork_sidecar: dry run mode (ledger unchanged)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
