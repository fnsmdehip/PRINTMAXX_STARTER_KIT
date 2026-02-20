#!/usr/bin/env python3
"""Venture map execution health check.

Checks freshness and quality of venture-map execution runs and writes
health artifacts for dashboards/human review.
"""

from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List


BASE_DIR = Path(__file__).resolve().parent.parent
LEDGER_DIR = BASE_DIR / "LEDGER"
OUT_DIR = BASE_DIR / "output" / "venture_map_health"

RUNS_CSV = LEDGER_DIR / "VENTURE_MAP_EXEC_RUNS.csv"
HEALTH_CSV = LEDGER_DIR / "VENTURE_MAP_HEALTH.csv"
MANIFEST_JSON = OUT_DIR / "manifest.json"
LATEST_MD = OUT_DIR / "latest.md"

OK_STATUSES = {"OK"}
FAIL_STATUSES = {"FAILED", "TIMEOUT"}


def now_iso() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def parse_ts(value: str) -> datetime | None:
    s = (value or "").strip()
    if not s:
        return None
    for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%dT%H:%M:%S"):
        try:
            return datetime.strptime(s, fmt)
        except ValueError:
            continue
    return None


def age_hours(dt: datetime | None) -> float | None:
    if dt is None:
        return None
    delta = datetime.now() - dt
    return round(delta.total_seconds() / 3600.0, 3)


def read_rows(path: Path) -> List[Dict[str, str]]:
    if not path.exists():
        return []
    rows: List[Dict[str, str]] = []
    with open(path, "r", encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            rows.append({str(k): str(v or "") for k, v in row.items()})
    return rows


def ensure_health_csv() -> None:
    LEDGER_DIR.mkdir(parents=True, exist_ok=True)
    if HEALTH_CSV.exists():
        return
    with open(HEALTH_CSV, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(
            [
                "timestamp",
                "status",
                "reason",
                "max_age_hours",
                "critical_age_hours",
                "last_run_at",
                "last_ok_at",
                "last_ok_age_hours",
                "last_batch_status_counts",
                "last_batch_command_count",
            ]
        )


def evaluate(rows: List[Dict[str, str]], max_age_hours: float, critical_age_hours: float) -> Dict[str, Any]:
    if not rows:
        return {
            "status": "CRITICAL",
            "reason": "No venture map run history found",
            "counts": {"rows": 0},
            "last_run_at": "",
            "last_ok_at": "",
            "last_ok_age_hours": None,
            "last_batch": {"status_counts": {}, "command_count": 0},
        }

    parsed: List[Dict[str, Any]] = []
    for row in rows:
        ts = parse_ts(row.get("timestamp", ""))
        if ts is None:
            continue
        parsed.append(
            {
                "timestamp": ts,
                "status": (row.get("status") or "").strip().upper(),
                "command": (row.get("command") or "").strip(),
            }
        )

    if not parsed:
        return {
            "status": "CRITICAL",
            "reason": "Run history exists but timestamps are unreadable",
            "counts": {"rows": len(rows), "parsed_rows": 0},
            "last_run_at": "",
            "last_ok_at": "",
            "last_ok_age_hours": None,
            "last_batch": {"status_counts": {}, "command_count": 0},
        }

    parsed.sort(key=lambda x: x["timestamp"])
    last_run_at = parsed[-1]["timestamp"]
    ok_rows = [r for r in parsed if r["status"] in OK_STATUSES]
    last_ok_at = ok_rows[-1]["timestamp"] if ok_rows else None

    last_batch_rows = [r for r in parsed if r["timestamp"] == last_run_at]
    batch_status_counts = Counter(r["status"] or "UNKNOWN" for r in last_batch_rows)
    batch_fail_count = sum(batch_status_counts.get(s, 0) for s in FAIL_STATUSES)

    last_ok_age = age_hours(last_ok_at)
    if last_ok_at is None:
        status = "CRITICAL"
        reason = "No successful venture-map command bundles recorded yet"
    else:
        if last_ok_age is None:
            status = "CRITICAL"
            reason = "Could not calculate last successful run age"
        elif last_ok_age <= max_age_hours:
            status = "OK"
            reason = f"Last successful venture-map run is fresh ({last_ok_age:.2f}h)"
        elif last_ok_age <= critical_age_hours:
            status = "STALE"
            reason = f"Last successful venture-map run is stale ({last_ok_age:.2f}h > {max_age_hours}h)"
        else:
            status = "CRITICAL"
            reason = f"Last successful venture-map run is too old ({last_ok_age:.2f}h > {critical_age_hours}h)"

    # Degrade fresh status if the latest batch had hard failures.
    if status == "OK" and batch_fail_count > 0:
        status = "STALE"
        reason = f"Latest venture-map batch has failures ({batch_fail_count} failed/timeout)"

    return {
        "status": status,
        "reason": reason,
        "counts": {"rows": len(rows), "parsed_rows": len(parsed), "ok_rows": len(ok_rows)},
        "last_run_at": last_run_at.strftime("%Y-%m-%d %H:%M:%S"),
        "last_ok_at": last_ok_at.strftime("%Y-%m-%d %H:%M:%S") if last_ok_at else "",
        "last_ok_age_hours": last_ok_age,
        "last_batch": {
            "status_counts": {k: int(v) for k, v in sorted(batch_status_counts.items())},
            "command_count": len(last_batch_rows),
        },
    }


def write_outputs(payload: Dict[str, Any]) -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    MANIFEST_JSON.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    last_ok_age = payload.get("last_ok_age_hours")
    last_ok_age_str = "n/a" if last_ok_age is None else f"{float(last_ok_age):.2f}"
    lines = [
        "# Venture Map Health",
        "",
        f"Generated: {payload.get('generated_at', '')}",
        f"Status: {payload.get('status', 'UNKNOWN')}",
        f"Reason: {payload.get('reason', '')}",
        "",
        "## Freshness",
        "",
        f"- last_run_at={payload.get('last_run_at', '') or 'n/a'}",
        f"- last_ok_at={payload.get('last_ok_at', '') or 'n/a'}",
        f"- last_ok_age_hours={last_ok_age_str}",
        f"- max_age_hours={payload.get('max_age_hours', '')}",
        f"- critical_age_hours={payload.get('critical_age_hours', '')}",
        "",
        "## Latest Batch",
        "",
        f"- command_count={payload.get('last_batch', {}).get('command_count', 0)}",
        f"- status_counts={json.dumps(payload.get('last_batch', {}).get('status_counts', {}), sort_keys=True)}",
        "",
        "## History Counts",
        "",
        f"- rows={payload.get('counts', {}).get('rows', 0)}",
        f"- parsed_rows={payload.get('counts', {}).get('parsed_rows', 0)}",
        f"- ok_rows={payload.get('counts', {}).get('ok_rows', 0)}",
        "",
        f"- Manifest: `{MANIFEST_JSON.relative_to(BASE_DIR)}`",
    ]
    LATEST_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def append_health_csv(payload: Dict[str, Any]) -> None:
    ensure_health_csv()
    with open(HEALTH_CSV, "a", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(
            [
                now_iso(),
                payload.get("status", "UNKNOWN"),
                payload.get("reason", ""),
                payload.get("max_age_hours", 0),
                payload.get("critical_age_hours", 0),
                payload.get("last_run_at", ""),
                payload.get("last_ok_at", ""),
                payload.get("last_ok_age_hours", ""),
                json.dumps(payload.get("last_batch", {}).get("status_counts", {}), sort_keys=True),
                payload.get("last_batch", {}).get("command_count", 0),
            ]
        )


def parse_args() -> argparse.Namespace:
    ap = argparse.ArgumentParser(description="Venture map run health checker")
    ap.add_argument("--max-age-hours", type=float, default=12.0, help="Freshness threshold for healthy status")
    ap.add_argument("--critical-age-hours", type=float, default=24.0, help="Critical stale threshold")
    ap.add_argument("--no-fail", action="store_true", help="Always exit 0 even when stale/critical")
    return ap.parse_args()


def main() -> int:
    args = parse_args()
    rows = read_rows(RUNS_CSV)
    summary = evaluate(rows, max_age_hours=max(0.1, args.max_age_hours), critical_age_hours=max(0.2, args.critical_age_hours))

    payload: Dict[str, Any] = {
        "generated_at": now_iso(),
        "status": summary.get("status", "UNKNOWN"),
        "reason": summary.get("reason", ""),
        "max_age_hours": max(0.1, args.max_age_hours),
        "critical_age_hours": max(0.2, args.critical_age_hours),
        "last_run_at": summary.get("last_run_at", ""),
        "last_ok_at": summary.get("last_ok_at", ""),
        "last_ok_age_hours": summary.get("last_ok_age_hours"),
        "counts": summary.get("counts", {}),
        "last_batch": summary.get("last_batch", {}),
        "source_csv": str(RUNS_CSV),
    }
    write_outputs(payload)
    append_health_csv(payload)

    status = str(payload.get("status", "UNKNOWN")).upper()
    print(
        "venture_map_health_check: "
        f"status={status} "
        f"last_ok_age_h={payload.get('last_ok_age_hours')} "
        f"reason={payload.get('reason', '')}"
    )

    if args.no_fail:
        return 0
    if status == "OK":
        return 0
    if status == "STALE":
        return 1
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
