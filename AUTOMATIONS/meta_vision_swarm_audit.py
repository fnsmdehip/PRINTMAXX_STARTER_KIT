#!/usr/bin/env python3
"""Generate a full-context META_VISION audit snapshot.

Swarm model:
  - Collector phase: build full-file inventory.
  - Parallel audit teams: runtime, pipeline, directory metrics, largest files.
  - Output phase: timestamped META_VISION markdown + raw CSV artifacts.
"""

from __future__ import annotations

import argparse
import csv
import json
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Iterable, List, Tuple


BASE_DIR = Path(__file__).resolve().parent.parent
AUDIT_DIR = BASE_DIR / "AUDIT"
OPS_DIR = BASE_DIR / "OPS"
LEDGER_DIR = BASE_DIR / "LEDGER"
OUTPUT_DIR = BASE_DIR / "output"

SKIP_DIRS = {".git", ".idea", ".vscode", "__pycache__", ".pytest_cache"}
KEY_DIRS = [
    "AUTOMATIONS",
    "OPS",
    "LEDGER",
    "output",
    "AUDIT",
    "MONEY_METHODS",
    "CONTENT",
    "PRODUCTS",
    "scripts",
]


@dataclass(frozen=True)
class FileRec:
    relpath: str
    top_level: str
    size_bytes: int
    mtime_iso: str
    extension: str


def now_iso() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def safe_int(v: object, default: int = 0) -> int:
    try:
        return int(float(str(v).strip()))
    except Exception:
        return default


def safe_float(v: object, default: float = 0.0) -> float:
    try:
        return float(str(v).strip())
    except Exception:
        return default


def fmt_bytes(n: int) -> str:
    value = float(max(0, n))
    units = ["B", "KB", "MB", "GB", "TB"]
    i = 0
    while value >= 1024 and i < len(units) - 1:
        value /= 1024.0
        i += 1
    if i == 0:
        return f"{int(value)} {units[i]}"
    return f"{value:.2f} {units[i]}"


def load_json(path: Path) -> Dict[str, Any]:
    if not path.exists():
        return {}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
        return payload if isinstance(payload, dict) else {}
    except Exception:
        return {}


def count_csv_rows(path: Path) -> int:
    if not path.exists():
        return 0
    try:
        with open(path, "r", encoding="utf-8", errors="replace", newline="") as f:
            reader = csv.reader(f)
            count = -1
            for _ in reader:
                count += 1
        return max(0, count)
    except Exception:
        return 0


def inventory_files(root: Path) -> List[FileRec]:
    out: List[FileRec] = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        dpath = Path(dirpath)
        for name in filenames:
            path = dpath / name
            try:
                st = path.stat()
            except Exception:
                continue
            try:
                rel = path.relative_to(root).as_posix()
            except Exception:
                rel = str(path)
            top = rel.split("/", 1)[0] if "/" in rel else "(root)"
            out.append(
                FileRec(
                    relpath=rel,
                    top_level=top,
                    size_bytes=int(st.st_size),
                    mtime_iso=datetime.fromtimestamp(st.st_mtime).strftime("%Y-%m-%d %H:%M:%S"),
                    extension=path.suffix.lower(),
                )
            )
    out.sort(key=lambda r: r.relpath)
    return out


def top_level_metrics(inventory: List[FileRec]) -> List[Dict[str, Any]]:
    buckets: Dict[str, Dict[str, Any]] = {}
    for rec in inventory:
        b = buckets.setdefault(
            rec.top_level,
            {
                "top_level": rec.top_level,
                "file_count": 0,
                "total_bytes": 0,
                "py_files": 0,
                "csv_files": 0,
                "md_files": 0,
            },
        )
        b["file_count"] += 1
        b["total_bytes"] += rec.size_bytes
        if rec.extension == ".py":
            b["py_files"] += 1
        if rec.extension == ".csv":
            b["csv_files"] += 1
        if rec.extension == ".md":
            b["md_files"] += 1
    rows = list(buckets.values())
    rows.sort(key=lambda r: int(r.get("file_count", 0)), reverse=True)
    return rows


def key_dir_metrics(inventory: List[FileRec]) -> List[Dict[str, Any]]:
    by_top = {row["top_level"]: row for row in top_level_metrics(inventory)}
    rows: List[Dict[str, Any]] = []
    for key in KEY_DIRS:
        row = by_top.get(key, None)
        if row is None:
            rows.append(
                {
                    "dir": key,
                    "file_count": 0,
                    "total_bytes": 0,
                    "py_files": 0,
                    "csv_files": 0,
                    "md_files": 0,
                    "exists": False,
                }
            )
        else:
            rows.append(
                {
                    "dir": key,
                    "file_count": int(row.get("file_count", 0)),
                    "total_bytes": int(row.get("total_bytes", 0)),
                    "py_files": int(row.get("py_files", 0)),
                    "csv_files": int(row.get("csv_files", 0)),
                    "md_files": int(row.get("md_files", 0)),
                    "exists": True,
                }
            )
    return rows


def largest_files(inventory: List[FileRec], max_rows: int) -> List[Dict[str, Any]]:
    rows = sorted(inventory, key=lambda r: r.size_bytes, reverse=True)[:max_rows]
    return [
        {
            "relpath": r.relpath,
            "size_bytes": r.size_bytes,
            "size_human": fmt_bytes(r.size_bytes),
            "mtime_iso": r.mtime_iso,
        }
        for r in rows
    ]


def audit_runtime_state() -> Dict[str, Any]:
    queue_path = OPS_DIR / "HUMAN_LOOP_QUEUE.md"
    approvals_path = OPS_DIR / "HUMAN_APPROVALS.csv"
    node_role_path = OPS_DIR / "NODE_ROLE.json"
    heartbeat_path = OPS_DIR / "HEARTBEAT.md"

    pending: List[str] = []
    if queue_path.exists():
        for raw in queue_path.read_text(encoding="utf-8", errors="replace").splitlines():
            s = raw.strip()
            if s.startswith("- [ ]"):
                pending.append(s)

    approved: List[str] = []
    if approvals_path.exists():
        with open(approvals_path, "r", encoding="utf-8", newline="") as f:
            for row in csv.DictReader(f):
                key = (row.get("key") or "").strip().upper()
                status = (row.get("status") or "").strip().upper()
                if key and status in {"APPROVED", "YES", "TRUE", "ACTIVE"}:
                    approved.append(key)

    node_role = load_json(node_role_path).get("role", "unknown")
    return {
        "node_role": str(node_role),
        "queue_file_exists": queue_path.exists(),
        "pending_approvals_count": len(pending),
        "pending_approvals": pending,
        "approved_keys_count": len(approved),
        "approved_keys": sorted(set(approved)),
        "heartbeat_exists": heartbeat_path.exists(),
    }


def audit_pipeline_state() -> Dict[str, Any]:
    freelance_manifest = load_json(OUTPUT_DIR / "freelance" / "manifest.json")
    ecom_manifest = load_json(OUTPUT_DIR / "ecom" / "manifest.json")
    ecom_autolist_manifest = load_json(OUTPUT_DIR / "ecom_autolist" / "manifest.json")
    clawdbot_manifest = load_json(OUTPUT_DIR / "clawdbot" / "manifest.json")
    sidecar_manifest = load_json(OUTPUT_DIR / "clawwork_sidecar" / "manifest.json")

    accounts_csv = LEDGER_DIR / "ACCOUNTS.csv"
    account_rows = count_csv_rows(accounts_csv)
    active_accounts = 0
    if accounts_csv.exists():
        with open(accounts_csv, "r", encoding="utf-8", newline="") as f:
            for row in csv.DictReader(f):
                status = (row.get("Status") or "").strip().upper()
                if status in {"ACTIVE", "CREATED", "READY"}:
                    active_accounts += 1

    claw_counts = clawdbot_manifest.get("counts", {}) if isinstance(clawdbot_manifest.get("counts"), dict) else {}
    sidecar_budget = sidecar_manifest.get("budget", {}) if isinstance(sidecar_manifest.get("budget"), dict) else {}
    sidecar_totals = sidecar_manifest.get("totals", {}) if isinstance(sidecar_manifest.get("totals"), dict) else {}

    return {
        "freelance_scan_count": safe_int(freelance_manifest.get("scan_count"), 0),
        "freelance_draft_count": safe_int(freelance_manifest.get("draft_count"), 0),
        "ecom_top_arb_count": len(ecom_manifest.get("top_arb", [])) if isinstance(ecom_manifest.get("top_arb"), list) else 0,
        "gumroad_pending_count": safe_int(ecom_autolist_manifest.get("pending_count"), 0),
        "gumroad_live_count": safe_int(ecom_autolist_manifest.get("live_count"), 0),
        "clawdbot_intent_rows": safe_int(claw_counts.get("intent_rows"), 0),
        "clawdbot_syndication_rows": safe_int(claw_counts.get("syndication_rows"), 0),
        "clawdbot_directory_rows": safe_int(claw_counts.get("directory_rows"), 0),
        "accounts_total_rows": account_rows,
        "accounts_active_rows": active_accounts,
        "sidecar_budget_state": str(sidecar_budget.get("budget_state", "unknown")),
        "sidecar_estimated_cost_usd": safe_float(sidecar_totals.get("estimated_eval_cost_usd"), 0.0),
        "sidecar_expected_profit_usd": safe_float(sidecar_totals.get("expected_profit_usd"), 0.0),
    }


def latest_full_context_state() -> Dict[str, Any]:
    candidates = sorted(AUDIT_DIR.glob("FULL_CONTEXT_*"))
    if not candidates:
        return {
            "exists": False,
            "summary_path": "",
            "manifest_path": "",
            "chunks_path": "",
            "summary": {},
        }
    latest = candidates[-1]
    summary_path = latest / "summary.json"
    manifest_path = latest / "file_manifest.csv"
    chunks_path = latest / "chunks"
    summary = load_json(summary_path) if summary_path.exists() else {}
    return {
        "exists": True,
        "summary_path": str(summary_path.relative_to(BASE_DIR)) if summary_path.exists() else "",
        "manifest_path": str(manifest_path.relative_to(BASE_DIR)) if manifest_path.exists() else "",
        "chunks_path": str(chunks_path.relative_to(BASE_DIR)) if chunks_path.exists() else "",
        "summary": summary,
    }


def write_csv(path: Path, headers: Iterable[str], rows: Iterable[Dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(headers))
        writer.writeheader()
        for row in rows:
            writer.writerow({k: row.get(k, "") for k in writer.fieldnames})


def md_table(headers: List[str], rows: List[List[str]]) -> List[str]:
    out = ["| " + " | ".join(headers) + " |", "| " + " | ".join(["---"] * len(headers)) + " |"]
    for row in rows:
        out.append("| " + " | ".join(row) + " |")
    return out


def render_meta_markdown(
    *,
    generated_at: str,
    inventory: List[FileRec],
    top_rows: List[Dict[str, Any]],
    key_rows: List[Dict[str, Any]],
    largest_rows: List[Dict[str, Any]],
    runtime: Dict[str, Any],
    pipeline: Dict[str, Any],
    full_context: Dict[str, Any],
    artifacts: Dict[str, str],
) -> str:
    total_files = len(inventory)
    total_bytes = sum(r.size_bytes for r in inventory)
    total_dirs = 0
    for _, dirnames, _ in os.walk(BASE_DIR):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        total_dirs += len(dirnames)

    lines: List[str] = []
    lines.append("# META VISION: PRINTMAXX System Synthesis (v3 -- Swarm Full Context)")
    lines.append("")
    lines.append(f"**Date:** {generated_at}")
    lines.append("**Method:** Parallel swarm audit teams (inventory, runtime, pipeline, metrics)")
    lines.append("**Scope:** Full repository context with raw inventory artifacts")
    lines.append("")
    lines.append("## 1. Global Scale Snapshot")
    lines.append("")
    lines.append(f"- Total files: **{total_files:,}**")
    lines.append(f"- Total directories: **{total_dirs:,}**")
    lines.append(f"- Total bytes on disk (files only): **{fmt_bytes(total_bytes)}**")
    lines.append(f"- Python files: **{sum(1 for r in inventory if r.extension == '.py'):,}**")
    lines.append(f"- CSV files: **{sum(1 for r in inventory if r.extension == '.csv'):,}**")
    lines.append(f"- Markdown files: **{sum(1 for r in inventory if r.extension == '.md'):,}**")
    lines.append("")
    lines.append("## 2. Top-Level Directory Metrics (Full Surface)")
    lines.append("")
    top_table_rows: List[List[str]] = []
    for r in top_rows:
        top_table_rows.append(
            [
                str(r.get("top_level", "")),
                f"{safe_int(r.get('file_count'), 0):,}",
                fmt_bytes(safe_int(r.get("total_bytes"), 0)),
                f"{safe_int(r.get('py_files'), 0):,}",
                f"{safe_int(r.get('csv_files'), 0):,}",
                f"{safe_int(r.get('md_files'), 0):,}",
            ]
        )
    lines.extend(md_table(["top_level", "files", "bytes", "py", "csv", "md"], top_table_rows))
    lines.append("")
    lines.append("## 3. Core System Directories (Agent Navigation)")
    lines.append("")
    key_table_rows: List[List[str]] = []
    for r in key_rows:
        key_table_rows.append(
            [
                str(r.get("dir", "")),
                "yes" if bool(r.get("exists")) else "no",
                f"{safe_int(r.get('file_count'), 0):,}",
                fmt_bytes(safe_int(r.get("total_bytes"), 0)),
                f"{safe_int(r.get('py_files'), 0):,}",
                f"{safe_int(r.get('csv_files'), 0):,}",
                f"{safe_int(r.get('md_files'), 0):,}",
            ]
        )
    lines.extend(md_table(["dir", "exists", "files", "bytes", "py", "csv", "md"], key_table_rows))
    lines.append("")
    lines.append("## 4. Runtime and Approval Gates")
    lines.append("")
    lines.append(f"- Node role: `{runtime.get('node_role', 'unknown')}`")
    lines.append(f"- Pending approvals: **{safe_int(runtime.get('pending_approvals_count'), 0)}**")
    lines.append(f"- Approved keys: **{safe_int(runtime.get('approved_keys_count'), 0)}**")
    lines.append(f"- HEARTBEAT.md present: **{'yes' if runtime.get('heartbeat_exists') else 'no'}**")
    lines.append("")
    pending = runtime.get("pending_approvals", [])
    if isinstance(pending, list) and pending:
        lines.append("### Pending Approval Items")
        lines.append("")
        for item in pending:
            lines.append(f"- {item}")
        lines.append("")
    lines.append("## 5. Revenue Pipeline State (Current Artifacts)")
    lines.append("")
    lines.append(f"- Freelance scan rows: **{safe_int(pipeline.get('freelance_scan_count'), 0):,}**")
    lines.append(f"- Freelance draft rows: **{safe_int(pipeline.get('freelance_draft_count'), 0):,}**")
    lines.append(f"- Ecom top arb items: **{safe_int(pipeline.get('ecom_top_arb_count'), 0):,}**")
    lines.append(f"- Gumroad pending listings: **{safe_int(pipeline.get('gumroad_pending_count'), 0):,}**")
    lines.append(f"- Gumroad live listings: **{safe_int(pipeline.get('gumroad_live_count'), 0):,}**")
    lines.append(f"- Clawdbot intent queue rows: **{safe_int(pipeline.get('clawdbot_intent_rows'), 0):,}**")
    lines.append(f"- Clawdbot syndication rows: **{safe_int(pipeline.get('clawdbot_syndication_rows'), 0):,}**")
    lines.append(f"- Clawdbot directory rows: **{safe_int(pipeline.get('clawdbot_directory_rows'), 0):,}**")
    lines.append(f"- Accounts tracked: **{safe_int(pipeline.get('accounts_total_rows'), 0):,}**")
    lines.append(f"- Accounts active/ready: **{safe_int(pipeline.get('accounts_active_rows'), 0):,}**")
    lines.append("")
    lines.append("### ClawWork Sidecar State")
    lines.append("")
    lines.append(f"- Budget state: `{pipeline.get('sidecar_budget_state', 'unknown')}`")
    lines.append(f"- Estimated eval cost: **${safe_float(pipeline.get('sidecar_estimated_cost_usd'), 0.0):.2f}**")
    lines.append(f"- Expected sampled profit: **${safe_float(pipeline.get('sidecar_expected_profit_usd'), 0.0):.2f}**")
    lines.append("")
    lines.append("## 6. Full-Content Corpus (No-Summary Context)")
    lines.append("")
    if bool(full_context.get("exists")):
        summary = full_context.get("summary", {}) if isinstance(full_context.get("summary"), dict) else {}
        lines.append(f"- Summary file: `{full_context.get('summary_path', '')}`")
        lines.append(f"- File manifest: `{full_context.get('manifest_path', '')}`")
        lines.append(f"- Raw chunk shards: `{full_context.get('chunks_path', '')}`")
        lines.append(f"- Files captured: **{safe_int(summary.get('files_total'), 0):,}**")
        lines.append(f"- Text files captured: **{safe_int(summary.get('text_files'), 0):,}**")
        lines.append(f"- Binary files captured: **{safe_int(summary.get('binary_files'), 0):,}**")
        lines.append(f"- Total chunks: **{safe_int(summary.get('total_chunks'), 0):,}**")
        lines.append(f"- Total bytes captured: **{fmt_bytes(safe_int(summary.get('total_bytes'), 0))}**")
    else:
        lines.append("- No FULL_CONTEXT_* artifact found.")
    lines.append("")
    lines.append("## 7. Largest Files (Storage + Review Hotspots)")
    lines.append("")
    largest_table_rows: List[List[str]] = []
    for r in largest_rows:
        largest_table_rows.append(
            [
                str(r.get("relpath", "")),
                str(r.get("size_human", "")),
                str(r.get("mtime_iso", "")),
            ]
        )
    lines.extend(md_table(["file", "size", "mtime"], largest_table_rows))
    lines.append("")
    lines.append("## 8. Full-Context Raw Artifacts")
    lines.append("")
    lines.append(f"- Full file inventory CSV: `{artifacts.get('inventory_csv', '')}`")
    lines.append(f"- Top-level metrics CSV: `{artifacts.get('top_metrics_csv', '')}`")
    lines.append(f"- Core directory metrics CSV: `{artifacts.get('key_metrics_csv', '')}`")
    lines.append(f"- Largest files CSV: `{artifacts.get('largest_csv', '')}`")
    lines.append("")
    lines.append("## 9. Re-run Command")
    lines.append("")
    lines.append("```bash")
    lines.append("python3 AUTOMATIONS/meta_vision_swarm_audit.py --write")
    lines.append("```")
    lines.append("")
    return "\n".join(lines) + "\n"


def parse_args() -> argparse.Namespace:
    ap = argparse.ArgumentParser(description="Generate timestamped META_VISION full-context audit")
    ap.add_argument("--write", action="store_true", help="Generate audit artifacts")
    ap.add_argument("--tag", default="", help="Optional tag (default: YYYY_MM_DD)")
    ap.add_argument("--max-largest", type=int, default=120, help="Rows to keep in largest-files list")
    return ap.parse_args()


def main() -> int:
    args = parse_args()
    if not args.write:
        print("meta_vision_swarm_audit: pass --write")
        return 2

    tag = args.tag.strip() or datetime.now().strftime("%Y_%m_%d")
    generated_at = now_iso()

    # Collector phase.
    inventory = inventory_files(BASE_DIR)

    # Parallel audit teams.
    results: Dict[str, Any] = {}
    with ThreadPoolExecutor(max_workers=6) as ex:
        future_map = {
            ex.submit(top_level_metrics, inventory): "top_metrics",
            ex.submit(key_dir_metrics, inventory): "key_metrics",
            ex.submit(largest_files, inventory, max(20, args.max_largest)): "largest",
            ex.submit(audit_runtime_state): "runtime",
            ex.submit(audit_pipeline_state): "pipeline",
        }
        for fut in as_completed(future_map):
            key = future_map[fut]
            results[key] = fut.result()

    full_context = latest_full_context_state()

    AUDIT_DIR.mkdir(parents=True, exist_ok=True)

    meta_md = AUDIT_DIR / f"META_VISION_{tag}.md"
    inventory_csv = AUDIT_DIR / f"META_VISION_{tag}_FILE_INVENTORY.csv"
    top_metrics_csv = AUDIT_DIR / f"META_VISION_{tag}_TOP_LEVEL_METRICS.csv"
    key_metrics_csv = AUDIT_DIR / f"META_VISION_{tag}_CORE_DIR_METRICS.csv"
    largest_csv = AUDIT_DIR / f"META_VISION_{tag}_LARGEST_FILES.csv"

    write_csv(
        inventory_csv,
        ["relpath", "top_level", "size_bytes", "mtime_iso", "extension"],
        [
            {
                "relpath": r.relpath,
                "top_level": r.top_level,
                "size_bytes": r.size_bytes,
                "mtime_iso": r.mtime_iso,
                "extension": r.extension,
            }
            for r in inventory
        ],
    )
    write_csv(
        top_metrics_csv,
        ["top_level", "file_count", "total_bytes", "py_files", "csv_files", "md_files"],
        results.get("top_metrics", []),
    )
    write_csv(
        key_metrics_csv,
        ["dir", "exists", "file_count", "total_bytes", "py_files", "csv_files", "md_files"],
        results.get("key_metrics", []),
    )
    write_csv(
        largest_csv,
        ["relpath", "size_bytes", "size_human", "mtime_iso"],
        results.get("largest", []),
    )

    md = render_meta_markdown(
        generated_at=generated_at,
        inventory=inventory,
        top_rows=results.get("top_metrics", []),
        key_rows=results.get("key_metrics", []),
        largest_rows=results.get("largest", []),
        runtime=results.get("runtime", {}),
        pipeline=results.get("pipeline", {}),
        full_context=full_context,
        artifacts={
            "inventory_csv": str(inventory_csv.relative_to(BASE_DIR)),
            "top_metrics_csv": str(top_metrics_csv.relative_to(BASE_DIR)),
            "key_metrics_csv": str(key_metrics_csv.relative_to(BASE_DIR)),
            "largest_csv": str(largest_csv.relative_to(BASE_DIR)),
        },
    )
    meta_md.write_text(md, encoding="utf-8")

    print("meta_vision_swarm_audit: wrote")
    print(f"- {meta_md}")
    print(f"- {inventory_csv}")
    print(f"- {top_metrics_csv}")
    print(f"- {key_metrics_csv}")
    print(f"- {largest_csv}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
