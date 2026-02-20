#!/usr/bin/env python3
"""
PRINTMAXX Cron Fleet Report
===========================

This is a truth-first, file-based "what is actually running" report.

It does not assume network access. It only inspects:
  - log files under logs/ and AUTOMATIONS/logs/
  - key output artifacts under output/
  - key ledgers under LEDGER/

Outputs:
  output/cron_fleet/latest.md
  output/cron_fleet/latest.html
  output/cron_fleet/manifest.json
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable


BASE_DIR = Path(__file__).resolve().parent.parent
OUT_DIR = BASE_DIR / "output" / "cron_fleet"
MANIFEST = OUT_DIR / "manifest.json"
LATEST_MD = OUT_DIR / "latest.md"
LATEST_HTML = OUT_DIR / "latest.html"


def now_iso() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def _dt_from_ts(ts: float) -> datetime:
    return datetime.fromtimestamp(ts, tz=timezone.utc)


def _age_min(ts: float) -> int:
    delta = datetime.now(tz=timezone.utc) - _dt_from_ts(ts)
    return max(0, int(delta.total_seconds() // 60))


def _fmt_age(mins: int) -> str:
    if mins < 60:
        return f"{mins}m"
    hrs = mins // 60
    rem = mins % 60
    if hrs < 48:
        return f"{hrs}h{rem:02d}m"
    days = hrs // 24
    hr = hrs % 24
    return f"{days}d{hr:02d}h"


def _safe_rel(p: Path) -> str:
    try:
        return str(p.relative_to(BASE_DIR))
    except Exception:
        return str(p)


@dataclass(frozen=True)
class FileRow:
    relpath: str
    mtime_iso: str
    age_min: int
    size_bytes: int

    def to_dict(self) -> dict:
        return {
            "relpath": self.relpath,
            "mtime_iso": self.mtime_iso,
            "age_min": self.age_min,
            "size_bytes": self.size_bytes,
        }


def _file_row(p: Path) -> FileRow | None:
    try:
        st = p.stat()
    except Exception:
        return None
    return FileRow(
        relpath=_safe_rel(p),
        mtime_iso=datetime.fromtimestamp(st.st_mtime).strftime("%Y-%m-%d %H:%M:%S"),
        age_min=_age_min(st.st_mtime),
        size_bytes=int(st.st_size),
    )


def _collect_files(paths: Iterable[Path]) -> list[FileRow]:
    rows: list[FileRow] = []
    for p in paths:
        r = _file_row(p)
        if r:
            rows.append(r)
    rows.sort(key=lambda x: x.age_min)
    return rows


def _glob_many(root: Path, patterns: list[str]) -> list[Path]:
    out: list[Path] = []
    for pat in patterns:
        out.extend(sorted(root.glob(pat)))
    # Deduplicate while preserving order.
    seen: set[str] = set()
    uniq: list[Path] = []
    for p in out:
        s = str(p)
        if s in seen:
            continue
        seen.add(s)
        uniq.append(p)
    return uniq


def _render_table(rows: list[FileRow], *, max_rows: int = 25) -> str:
    if not rows:
        return "_No data._"
    lines = ["| file | age | mtime | size |", "|---|---:|---:|---:|"]
    for r in rows[:max_rows]:
        age = _fmt_age(r.age_min)
        size_kb = max(1, r.size_bytes // 1024) if r.size_bytes else 0
        lines.append(f"| `{r.relpath}` | {age} | {r.mtime_iso} | {size_kb} KB |")
    return "\n".join(lines)


def _escape_html(s: str) -> str:
    return (s or "").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def _render_html(rows: list[FileRow], *, title: str) -> str:
    if not rows:
        body = "<p class='muted'>No data.</p>"
    else:
        trs = []
        for r in rows[:60]:
            trs.append(
                "<tr>"
                f"<td><code>{_escape_html(r.relpath)}</code></td>"
                f"<td style='text-align:right'>{_escape_html(_fmt_age(r.age_min))}</td>"
                f"<td style='text-align:right'>{_escape_html(r.mtime_iso)}</td>"
                f"<td style='text-align:right'>{max(0, r.size_bytes // 1024)} KB</td>"
                "</tr>"
            )
        body = (
            "<table>"
            "<thead><tr><th>file</th><th>age</th><th>mtime</th><th>size</th></tr></thead>"
            "<tbody>"
            + "".join(trs)
            + "</tbody></table>"
        )

    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{_escape_html(title)}</title>
  <style>
    body {{ font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace; background:#0b0b0b; color:#eaeaea; margin:0; }}
    header {{ padding:14px 18px; border-bottom:1px solid #1f1f1f; background:#0f0f0f; }}
    h1 {{ font-size:14px; margin:0; letter-spacing:1px; color:#00ff88; }}
    .meta {{ color:#888; font-size:12px; margin-top:6px; }}
    main {{ padding:14px 18px 26px; }}
    table {{ width:100%; border-collapse:collapse; font-size:12px; }}
    th, td {{ border-bottom:1px solid #1f1f1f; padding:8px 8px; vertical-align:top; }}
    th {{ color:#aaa; font-weight:600; text-align:left; }}
    code {{ color:#9ad; }}
    .muted {{ color:#777; }}
  </style>
</head>
<body>
  <header>
    <h1>{_escape_html(title)}</h1>
    <div class="meta">Generated: {_escape_html(now_iso())}</div>
  </header>
  <main>
    {body}
  </main>
</body>
</html>
"""


def generate() -> dict:
    logs_root = BASE_DIR / "logs"
    auto_logs_root = BASE_DIR / "AUTOMATIONS" / "logs"

    log_files = []
    if logs_root.exists():
        log_files.extend(_glob_many(logs_root, ["*.log", "*.txt", "*.jsonl"]))
    if auto_logs_root.exists():
        log_files.extend(_glob_many(auto_logs_root, ["*.log", "*.txt", "*.jsonl"]))

    # Key deliverables (truth-first: these are the things you should see updating).
    key_artifacts = [
        BASE_DIR / "output" / "dashboard" / "index.html",
        BASE_DIR / "OPS" / "HUMAN_LOOP_QUEUE.md",
        BASE_DIR / "OPS" / "HUMAN_EXECUTION_BRIEF.md",
        BASE_DIR / "output" / "ecom" / "latest.md",
        BASE_DIR / "output" / "freelance" / "latest.md",
        BASE_DIR / "output" / "gov" / "latest.md",
        BASE_DIR / "output" / "apps" / "latest.md",
        BASE_DIR / "output" / "native_apps" / "latest.md",
        BASE_DIR / "output" / "launch" / "latest.md",
        BASE_DIR / "output" / "clawwork_sidecar" / "latest.md",
        BASE_DIR / "output" / "clawwork_sidecar" / "manifest.json",
        BASE_DIR / "output" / "venture_map_exec" / "latest.md",
        BASE_DIR / "output" / "venture_map_exec" / "manifest.json",
        BASE_DIR / "output" / "venture_map_health" / "latest.md",
        BASE_DIR / "output" / "venture_map_health" / "manifest.json",
        BASE_DIR / "LEDGER" / "SHIP_CAPTAIN_RUNS.csv",
        BASE_DIR / "LEDGER" / "CLAWWORK_SIDECAR_RUNS.csv",
        BASE_DIR / "LEDGER" / "VENTURE_MAP_EXEC_RUNS.csv",
        BASE_DIR / "LEDGER" / "VENTURE_MAP_HEALTH.csv",
        BASE_DIR / "LEDGER" / "FREELANCE_DEMAND_SCAN.csv",
        BASE_DIR / "LEDGER" / "LAUNCH_DIRECTORY_TRACKER.csv",
    ]

    logs = _collect_files(log_files)
    artifacts = _collect_files([p for p in key_artifacts if p.exists()])

    payload = {
        "generated_at": now_iso(),
        "counts": {"logs": len(logs), "artifacts": len(artifacts)},
        "logs": [r.to_dict() for r in logs[:200]],
        "artifacts": [r.to_dict() for r in artifacts],
    }
    return payload


def write(payload: dict) -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    MANIFEST.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    logs = [FileRow(**r) for r in payload.get("logs", []) if isinstance(r, dict)]
    artifacts = [FileRow(**r) for r in payload.get("artifacts", []) if isinstance(r, dict)]

    md = [
        "# PRINTMAXX Cron Fleet (Truth-First)",
        "",
        f"Generated: {payload.get('generated_at','')}",
        "",
        "## Key Artifacts",
        "",
        _render_table(artifacts, max_rows=25),
        "",
        "## Recent Log Updates",
        "",
        _render_table(logs, max_rows=40),
        "",
        f"- Manifest: `{_safe_rel(MANIFEST)}`",
    ]
    LATEST_MD.write_text("\n".join(md) + "\n", encoding="utf-8")

    # HTML view: show logs (that is the main "is it running" proof).
    LATEST_HTML.write_text(_render_html(logs, title="PRINTMAXX Cron Fleet"), encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true", help="Write output/cron_fleet artifacts.")
    args = ap.parse_args()

    payload = generate()
    if args.write:
        write(payload)
        print("cron_fleet_report: ok")
        print(f"- manifest: {MANIFEST}")
        print(f"- latest: {LATEST_MD}")
        return 0

    print(json.dumps(payload, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
