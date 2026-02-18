#!/usr/bin/env python3
"""
PRINTMAXX Status (truth-first)
=============================

One command to answer:
  - is anything actually running?
  - what is producing artifacts?
  - what is blocked, and why?

Reads only local files (no network).
"""

from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from datetime import datetime
from pathlib import Path


BASE = Path(__file__).resolve().parent.parent

RUNS_CSV = BASE / "LEDGER" / "SHIP_CAPTAIN_RUNS.csv"
QUEUE_MD = BASE / "OPS" / "HUMAN_LOOP_QUEUE.md"
NODE_ROLE_JSON = BASE / "OPS" / "NODE_ROLE.json"
CRON_FLEET_MANIFEST = BASE / "output" / "cron_fleet" / "manifest.json"


def now_iso() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def read_text(p: Path) -> str:
    try:
        return p.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return ""


def load_json(p: Path) -> dict:
    try:
        payload = json.loads(p.read_text(encoding="utf-8"))
        return payload if isinstance(payload, dict) else {}
    except Exception:
        return {}


def tail_runs(limit: int = 200) -> list[dict]:
    if not RUNS_CSV.exists():
        return []
    rows: list[dict] = []
    with open(RUNS_CSV, "r", newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            rows.append(row)
    return rows[-limit:]


def last_by_step(rows: list[dict]) -> dict[str, dict]:
    out: dict[str, dict] = {}
    for r in rows:
        sid = (r.get("step_id") or "").strip()
        if not sid:
            continue
        out[sid] = r
    return out


def parse_queue() -> list[dict]:
    text = read_text(QUEUE_MD)
    items: list[dict] = []
    for line in text.splitlines():
        s = line.strip()
        if not s.startswith("- ["):
            continue
        if "`" not in s:
            continue
        key = s.split("`", 2)[1].strip()
        reason = s.split(" - ", 1)[1].strip() if " - " in s else ""
        items.append({"key": key, "reason": reason})
    return items


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    rows = tail_runs(400)
    by_step = last_by_step(rows)
    statuses = Counter((r.get("status") or "").strip().upper() for r in rows if r.get("status"))

    node_role = (load_json(NODE_ROLE_JSON).get("role") or "control") if NODE_ROLE_JSON.exists() else "control"
    queue = parse_queue()

    cron = load_json(CRON_FLEET_MANIFEST) if CRON_FLEET_MANIFEST.exists() else {}
    recent_logs = cron.get("logs") if isinstance(cron.get("logs"), list) else []

    critical = {}
    for k in ("deploy_apps", "deploy_static", "live_send"):
        if k in by_step:
            critical[k] = {
                "status": by_step[k].get("status", ""),
                "notes": (by_step[k].get("notes", "") or "")[:220],
                "timestamp": by_step[k].get("timestamp", ""),
            }

    payload = {
        "generated_at": now_iso(),
        "node_role": node_role,
        "ship_captain": {
            "recent_rows": len(rows),
            "recent_status_counts": dict(statuses),
        },
        "human_queue": {"pending": len(queue), "items": queue[:20]},
        "critical_steps": critical,
        "cron_fleet": {
            "generated_at": cron.get("generated_at", ""),
            "tracked_logs": int(cron.get("counts", {}).get("logs", 0)) if isinstance(cron.get("counts"), dict) else 0,
            "recent_logs": recent_logs[:10],
        },
    }

    if args.json:
        print(json.dumps(payload, indent=2))
        return 0

    print(f"PRINTMAXX STATUS @ {payload['generated_at']}")
    print(f"- node_role: {payload['node_role']}")
    print(
        "- ship_recent: OK={ok} FAILED={failed} SKIPPED={skipped}".format(
            ok=statuses.get("OK", 0),
            failed=statuses.get("FAILED", 0),
            skipped=statuses.get("SKIPPED", 0),
        )
    )
    print(f"- human_queue_pending: {len(queue)}")
    if queue:
        for it in queue[:10]:
            print(f"  - {it['key']}: {it['reason']}")
        if len(queue) > 10:
            print(f"  - ... ({len(queue) - 10} more)")

    if critical:
        print("- critical_steps:")
        for k, v in critical.items():
            print(f"  - {k}: {v.get('status')} ({v.get('notes')})")

    if recent_logs:
        print("- recent_cron_logs:")
        for it in recent_logs[:10]:
            rp = (it.get("relpath") or "").strip()
            age = it.get("age_min")
            print(f"  - {rp} (age_min={age})")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

