#!/usr/bin/env python3
"""PRINTMAXX RBI Portfolio Optimizer.

Exploration/exploitation allocator for money methods.
Outputs ranked decisions and an execution todo for the next cycle.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple


BASE = Path(__file__).resolve().parent.parent
LEDGER = BASE / "LEDGER"
OPS = BASE / "OPS"
FINANCIALS = BASE / "FINANCIALS"

METHODS_MASTER = LEDGER / "MEGA_SHEET" / "TAB1_MONEY_METHODS_MASTER.csv"
METHODS_TRACKER = LEDGER / "MONEY_METHODS_TRACKER.csv"
ACCOUNTS_CSV = LEDGER / "ACCOUNTS.csv"
REVENUE_CSV = FINANCIALS / "REVENUE_TRACKER.csv"

STATE_JSON = LEDGER / "RBI_PORTFOLIO_STATE.json"
DECISIONS_CSV = LEDGER / "RBI_PORTFOLIO_DECISIONS.csv"
TODO_MD = OPS / "RBI_PORTFOLIO_TODO.md"


def now_iso() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def read_csv(path: Path) -> List[Dict[str, str]]:
    if not path.exists():
        return []
    rows: List[Dict[str, str]] = []
    with open(path, "r", encoding="utf-8", errors="replace", newline="") as f:
        for row in csv.DictReader(f):
            rows.append({k: (v or "").strip() for k, v in row.items()})
    return rows


def parse_money(raw: str) -> float:
    s = (raw or "").strip().lower().replace("$", "").replace(",", "")
    if not s:
        return 0.0
    mult = 1.0
    if s.endswith("k"):
        mult = 1000.0
        s = s[:-1]
    try:
        return float(s) * mult
    except Exception:
        return 0.0


def parse_monthly_potential(row: Dict[str, str]) -> float:
    low = parse_money(row.get("monthly_potential_low", ""))
    high = parse_money(row.get("monthly_potential_high", ""))
    if low == 0 and high == 0:
        # fallback to textual monthly_potential e.g. "$1k-50k"
        raw = row.get("monthly_potential", "")
        if "-" in raw:
            a, b = raw.split("-", 1)
            low = parse_money(a)
            high = parse_money(b)
        else:
            low = parse_money(raw)
            high = low
    if low == 0 and high == 0:
        return 0.0
    return (low + max(low, high)) / 2.0


def load_state() -> Dict[str, Dict[str, object]]:
    if not STATE_JSON.exists():
        return {}
    try:
        payload = json.loads(STATE_JSON.read_text(encoding="utf-8"))
        if isinstance(payload, dict):
            return payload
    except Exception:
        pass
    return {}


def save_state(state: Dict[str, Dict[str, object]]) -> None:
    STATE_JSON.parent.mkdir(parents=True, exist_ok=True)
    with open(STATE_JSON, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2)
        f.write("\n")


def accounts_ready_ratio() -> float:
    rows = read_csv(ACCOUNTS_CSV)
    if not rows:
        return 0.0
    required = {"Stripe", "Gumroad", "Instantly.ai", "Fiverr", "Upwork"}
    active = {"ACTIVE", "CREATED", "READY"}
    have = 0
    for r in rows:
        platform = r.get("Platform", "")
        status = r.get("Status", "").upper()
        if platform in required and status in active:
            have += 1
    return have / max(len(required), 1)


def method_revenue_signal(method_id: str, revenue_rows: List[Dict[str, str]]) -> float:
    m = (method_id or "").upper()
    total = 0.0
    for row in revenue_rows:
        rid = row.get("method_id", "").upper()
        if m and m in rid:
            total += parse_money(row.get("profit", "")) or parse_money(row.get("revenue", ""))
    return total


def decision_label(score: float) -> str:
    if score >= 75:
        return "DOUBLE_DOWN"
    if score >= 45:
        return "MAINTAIN"
    return "BACKLOG"


def merge_methods() -> List[Dict[str, str]]:
    master = read_csv(METHODS_MASTER)
    tracker = read_csv(METHODS_TRACKER)

    by_id: Dict[str, Dict[str, str]] = {}
    for row in master + tracker:
        mid = (row.get("method_id", "") or "").strip().upper()
        if not mid:
            continue
        if mid not in by_id:
            by_id[mid] = {}
        by_id[mid].update(row)
    return [by_id[k] for k in sorted(by_id)]


def score_method(
    row: Dict[str, str],
    revenue_rows: List[Dict[str, str]],
    account_ratio: float,
    state: Dict[str, Dict[str, object]],
) -> Tuple[float, Dict[str, float]]:
    mid = (row.get("method_id", "") or "").upper()
    potential = parse_monthly_potential(row)
    synergy = float((row.get("synergy_score") or "0").replace("%", "") or 0.0)
    status = (row.get("status") or "").lower()
    priority = (row.get("priority") or "").lower()

    rev = method_revenue_signal(mid, revenue_rows)
    # compress revenue to 0-100-like signal
    rev_signal = min(100.0, math.log10(max(rev, 1.0)) * 22.0)

    potential_signal = 0.0
    if potential > 0:
        # 500/mo -> ~18, 50k/mo -> ~88
        potential_signal = min(100.0, max(0.0, math.log10(potential) * 20.0))

    status_bonus = 0.0
    if status == "active":
        status_bonus = 12.0
    elif status in {"planning", "new"}:
        status_bonus = 6.0

    priority_bonus = 0.0
    if "phase1" in priority or priority in {"p0", "p1"}:
        priority_bonus = 8.0
    elif "phase2" in priority or priority == "p2":
        priority_bonus = 4.0

    exploration = 0.0
    node = state.get(mid, {})
    picks = int(node.get("picks", 0) or 0)
    exploration = min(18.0, 18.0 / math.sqrt(max(picks, 1)))

    account_gate = account_ratio * 15.0
    synergy_signal = min(20.0, synergy * 0.2)

    score = (
        rev_signal * 0.32
        + potential_signal * 0.28
        + synergy_signal
        + status_bonus
        + priority_bonus
        + exploration
        + account_gate
    )
    score = max(0.0, min(100.0, score))
    details = {
        "rev_signal": round(rev_signal, 2),
        "potential_signal": round(potential_signal, 2),
        "synergy_signal": round(synergy_signal, 2),
        "status_bonus": round(status_bonus, 2),
        "priority_bonus": round(priority_bonus, 2),
        "exploration_bonus": round(exploration, 2),
        "account_gate": round(account_gate, 2),
    }
    return score, details


def write_decisions(rows: List[Dict[str, object]]) -> None:
    DECISIONS_CSV.parent.mkdir(parents=True, exist_ok=True)
    with open(DECISIONS_CSV, "w", newline="", encoding="utf-8") as f:
        fields = [
            "timestamp",
            "rank",
            "method_id",
            "method_name",
            "status",
            "priority",
            "score",
            "decision",
            "expected_monthly_usd",
            "rev_signal",
            "potential_signal",
            "synergy_signal",
            "exploration_bonus",
            "notes",
        ]
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for row in rows:
            w.writerow(row)


def write_todo(rows: List[Dict[str, object]]) -> None:
    top = rows[:5]
    OPS.mkdir(parents=True, exist_ok=True)
    lines = [
        "# RBI Portfolio Todo",
        "",
        f"Generated: {now_iso()}",
        "",
        "## Top 5 Active Focus (Exploit + Explore)",
        "",
    ]
    if not top:
        lines.append("- no eligible methods")
    for i, row in enumerate(top, 1):
        lines.append(
            f"{i}. `{row['method_id']}` {row['method_name']} -> {row['decision']} "
            f"(score {row['score']}, est ${row['expected_monthly_usd']}/mo)"
        )
    lines.extend(
        [
            "",
            "## Rule",
            "",
            "- Keep 3 methods in DOUBLE_DOWN/MAINTAIN and 2 methods as exploration slots.",
            "- Re-score each cycle using realized data and reallocate attention automatically.",
            "",
        ]
    )
    with open(TODO_MD, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")


def tick(top_k: int = 10, json_out: bool = False) -> int:
    methods = merge_methods()
    if not methods:
        print("no_methods_loaded")
        return 1

    revenue_rows = read_csv(REVENUE_CSV)
    account_ratio = accounts_ready_ratio()
    state = load_state()
    ts = now_iso()

    scored: List[Tuple[float, Dict[str, str], Dict[str, float]]] = []
    for method in methods:
        score, details = score_method(method, revenue_rows, account_ratio, state)
        scored.append((score, method, details))

    scored.sort(key=lambda x: x[0], reverse=True)
    out_rows: List[Dict[str, object]] = []
    for idx, (score, method, details) in enumerate(scored, 1):
        mid = (method.get("method_id", "") or "").upper()
        mname = method.get("method_name", "")
        expected = int(parse_monthly_potential(method))
        decision = decision_label(score)
        out_rows.append(
            {
                "timestamp": ts,
                "rank": idx,
                "method_id": mid,
                "method_name": mname,
                "status": method.get("status", ""),
                "priority": method.get("priority", ""),
                "score": round(score, 2),
                "decision": decision,
                "expected_monthly_usd": expected,
                "rev_signal": details["rev_signal"],
                "potential_signal": details["potential_signal"],
                "synergy_signal": details["synergy_signal"],
                "exploration_bonus": details["exploration_bonus"],
                "notes": method.get("notes", "")[:180],
            }
        )

    # update state for top-k selected methods
    for row in out_rows[: max(top_k, 1)]:
        mid = str(row["method_id"])
        node = state.get(mid, {})
        node["picks"] = int(node.get("picks", 0) or 0) + 1
        node["last_selected_at"] = ts
        node["last_score"] = row["score"]
        node["last_decision"] = row["decision"]
        state[mid] = node

    save_state(state)
    write_decisions(out_rows)
    write_todo(out_rows)

    summary = {
        "timestamp": ts,
        "methods_total": len(out_rows),
        "top_focus": [f"{r['method_id']}:{r['decision']}:{r['score']}" for r in out_rows[:5]],
        "account_readiness_ratio": round(account_ratio, 3),
        "decisions_csv": str(DECISIONS_CSV.relative_to(BASE)),
        "todo_file": str(TODO_MD.relative_to(BASE)),
    }
    if json_out:
        print(json.dumps(summary, indent=2))
    else:
        print(
            f"rbi_tick methods={summary['methods_total']} "
            f"acct_ready={summary['account_readiness_ratio']} top5={';'.join(summary['top_focus'])}"
        )
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="PRINTMAXX RBI portfolio optimizer")
    parser.add_argument("--tick", action="store_true", help="Run one optimize cycle (default)")
    parser.add_argument("--top-k", type=int, default=10, help="Track exploration picks for top K methods")
    parser.add_argument("--json", action="store_true", help="Emit JSON summary")
    args = parser.parse_args()
    return tick(top_k=args.top_k, json_out=args.json)


if __name__ == "__main__":
    raise SystemExit(main())
