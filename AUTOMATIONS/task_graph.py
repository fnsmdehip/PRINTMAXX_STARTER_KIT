#!/usr/bin/env python3
"""
T016 — Native Task Dependency Graph

Replaces time-based cron with dependency-aware execution for pipeline agents.
Defines 4 dependency chains as a DAG, tracks task state in SQLite, and provides
a CLI for status inspection, readiness checks, and manual control.

Usage:
    python3 AUTOMATIONS/task_graph.py --status
    python3 AUTOMATIONS/task_graph.py --chain CHAIN_ALPHA_PIPELINE
    python3 AUTOMATIONS/task_graph.py --ready
    python3 AUTOMATIONS/task_graph.py --mark-done scraper
    python3 AUTOMATIONS/task_graph.py --mark-failed scraper --reason "timeout"
    python3 AUTOMATIONS/task_graph.py --stale
    python3 AUTOMATIONS/task_graph.py --reset scraper
    python3 AUTOMATIONS/task_graph.py --visualize

Stdlib only. No external dependencies.
"""
from __future__ import annotations

import argparse
import json
import sqlite3
import sys
import time
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any, Optional

# ---------------------------------------------------------------------------
# Imports from shared utilities
# ---------------------------------------------------------------------------
sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import PROJECT, safe_path, log, ts

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
DB_PATH = safe_path(PROJECT / "LEDGER" / "printmaxx_gates.db")
LEDGER_DIR = safe_path(PROJECT / "LEDGER")

# Ensure LEDGER dir exists
LEDGER_DIR.mkdir(parents=True, exist_ok=True)


class TaskStatus(str, Enum):
    WAITING = "WAITING"
    READY = "READY"
    RUNNING = "RUNNING"
    DONE = "DONE"
    FAILED = "FAILED"
    SKIPPED = "SKIPPED"


# ---------------------------------------------------------------------------
# Chain definitions — the 4 dependency DAGs
# ---------------------------------------------------------------------------
# Each chain is a list of (task_name, timeout_minutes) in dependency order.
# task N depends on task N-1 completing successfully.

CHAIN_ALPHA_PIPELINE = "CHAIN_ALPHA_PIPELINE"
CHAIN_CONTENT = "CHAIN_CONTENT"
CHAIN_LEAD = "CHAIN_LEAD"
CHAIN_ARB = "CHAIN_ARB"

CHAINS: dict[str, list[tuple[str, int]]] = {
    CHAIN_ALPHA_PIPELINE: [
        ("scraper", 20),
        ("alpha_auto_processor", 30),
        ("intelligence_router", 15),
        ("ceo_agent", 45),
    ],
    CHAIN_CONTENT: [
        ("shakespeare_agent", 30),
        ("evaluator_agent", 20),
        ("cross_model_reviewer", 20),
        ("social_poster", 15),
    ],
    CHAIN_LEAD: [
        ("observer_agent", 20),
        ("quinn_agent", 25),
        ("lead_machine", 30),
        ("compliance_scanner", 15),
        ("send", 10),
    ],
    CHAIN_ARB: [
        ("ecomm_arb_pipeline", 30),
        ("evaluator_agent_arb", 20),  # separate instance for arb chain
        ("HUMAN_GATE", 0),  # no timeout — waits for human
        ("asset_deployer", 30),
    ],
}

# Tasks that remain purely time-based (not in the DAG)
TIME_BASED_TASKS = [
    "morning_digest",          # 6:45 AM
    "daily_tactical_engine",   # 7:15 AM
    "system_health_monitor",   # */15 min
    "safety_commit",           # */2h
]


# ---------------------------------------------------------------------------
# TaskNode
# ---------------------------------------------------------------------------
@dataclass
class TaskNode:
    name: str
    chain: str
    upstream_deps: list[str] = field(default_factory=list)
    downstream: list[str] = field(default_factory=list)
    status: TaskStatus = TaskStatus.WAITING
    last_completed: Optional[str] = None   # ISO timestamp
    last_started: Optional[str] = None     # ISO timestamp
    timeout_minutes: int = 30
    fail_count: int = 0

    def is_ready(self, completed_tasks: set[str]) -> bool:
        """True if all upstream deps are in completed_tasks."""
        if self.status in (TaskStatus.RUNNING, TaskStatus.DONE, TaskStatus.SKIPPED):
            return False
        return all(dep in completed_tasks for dep in self.upstream_deps)


# ---------------------------------------------------------------------------
# SQLite persistence
# ---------------------------------------------------------------------------
def _connect() -> sqlite3.Connection:
    conn = sqlite3.connect(str(DB_PATH))
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA synchronous=NORMAL")
    conn.row_factory = sqlite3.Row
    return conn


def _init_table(conn: sqlite3.Connection) -> None:
    conn.execute("""
        CREATE TABLE IF NOT EXISTS task_graph (
            task_name       TEXT NOT NULL,
            chain           TEXT NOT NULL,
            status          TEXT NOT NULL DEFAULT 'WAITING',
            last_completed  TEXT,
            last_started    TEXT,
            timeout_minutes INTEGER NOT NULL DEFAULT 30,
            fail_count      INTEGER NOT NULL DEFAULT 0,
            PRIMARY KEY (task_name, chain)
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS task_graph_log (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            task_name   TEXT NOT NULL,
            chain       TEXT NOT NULL,
            action      TEXT NOT NULL,
            detail      TEXT,
            ts          TEXT NOT NULL
        )
    """)
    conn.commit()


def _log_action(conn: sqlite3.Connection, task_name: str, chain: str, action: str, detail: str = "") -> None:
    conn.execute(
        "INSERT INTO task_graph_log (task_name, chain, action, detail, ts) VALUES (?, ?, ?, ?, ?)",
        (task_name, chain, action, detail, _now_iso()),
    )


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


# ---------------------------------------------------------------------------
# TaskGraph — the core engine
# ---------------------------------------------------------------------------
class TaskGraph:
    """Dependency-aware task execution graph with SQLite persistence."""

    def __init__(self) -> None:
        self.nodes: dict[str, TaskNode] = {}
        self.conn = _connect()
        _init_table(self.conn)
        self.load_chains()
        self._sync_from_db()

    # -- build ---------------------------------------------------------------

    def load_chains(self) -> None:
        """Build all 4 chains as linked TaskNode objects."""
        self.nodes.clear()
        for chain_name, tasks in CHAINS.items():
            prev_name: Optional[str] = None
            for task_name, timeout in tasks:
                # Handle duplicate task names across chains by qualifying
                node_key = task_name if task_name not in self.nodes else f"{task_name}"
                node = TaskNode(
                    name=task_name,
                    chain=chain_name,
                    timeout_minutes=timeout,
                    upstream_deps=[prev_name] if prev_name else [],
                )
                self.nodes[f"{chain_name}::{task_name}"] = node
                # Wire downstream on previous node
                if prev_name:
                    prev_key = f"{chain_name}::{prev_name}"
                    if prev_key in self.nodes:
                        self.nodes[prev_key].downstream.append(task_name)
                prev_name = task_name

    def _sync_from_db(self) -> None:
        """Load persisted state into in-memory nodes."""
        rows = self.conn.execute("SELECT * FROM task_graph").fetchall()
        for row in rows:
            key = f"{row['chain']}::{row['task_name']}"
            if key in self.nodes:
                node = self.nodes[key]
                node.status = TaskStatus(row["status"])
                node.last_completed = row["last_completed"]
                node.last_started = row["last_started"]
                node.fail_count = row["fail_count"]

    def _persist_node(self, node: TaskNode) -> None:
        """Upsert a node's state to SQLite."""
        self.conn.execute("""
            INSERT INTO task_graph (task_name, chain, status, last_completed, last_started, timeout_minutes, fail_count)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(task_name, chain) DO UPDATE SET
                status=excluded.status,
                last_completed=excluded.last_completed,
                last_started=excluded.last_started,
                timeout_minutes=excluded.timeout_minutes,
                fail_count=excluded.fail_count
        """, (node.name, node.chain, node.status.value, node.last_completed,
              node.last_started, node.timeout_minutes, node.fail_count))
        self.conn.commit()

    # -- readiness -----------------------------------------------------------

    def _completed_in_chain(self, chain_name: str) -> set[str]:
        """Return set of task names that are DONE in the given chain."""
        done = set()
        for key, node in self.nodes.items():
            if node.chain == chain_name and node.status == TaskStatus.DONE:
                done.add(node.name)
        return done

    def check_ready(self) -> list[TaskNode]:
        """Return list of tasks whose upstream deps are all DONE."""
        ready = []
        for key, node in self.nodes.items():
            if node.status in (TaskStatus.WAITING, TaskStatus.READY, TaskStatus.FAILED):
                completed = self._completed_in_chain(node.chain)
                if node.is_ready(completed):
                    node.status = TaskStatus.READY
                    self._persist_node(node)
                    ready.append(node)
        return ready

    # -- state transitions ---------------------------------------------------

    def _find_node(self, task_name: str, chain_name: Optional[str] = None) -> Optional[TaskNode]:
        """Find a node by task name, optionally scoped to a chain."""
        if chain_name:
            key = f"{chain_name}::{task_name}"
            return self.nodes.get(key)
        # Search all chains, return first match
        for key, node in self.nodes.items():
            if node.name == task_name:
                return node
        return None

    def mark_started(self, task_name: str, chain_name: Optional[str] = None) -> bool:
        """Mark a task as RUNNING. Returns True on success."""
        node = self._find_node(task_name, chain_name)
        if not node:
            log(f"Task '{task_name}' not found in graph", level="ERROR", tag="TASK_GRAPH")
            return False
        node.status = TaskStatus.RUNNING
        node.last_started = _now_iso()
        self._persist_node(node)
        _log_action(self.conn, node.name, node.chain, "STARTED")
        self.conn.commit()
        log(f"[{node.chain}] {node.name} -> RUNNING", tag="TASK_GRAPH")
        return True

    def mark_done(self, task_name: str, chain_name: Optional[str] = None) -> bool:
        """Mark a task as DONE, trigger downstream readiness check."""
        node = self._find_node(task_name, chain_name)
        if not node:
            log(f"Task '{task_name}' not found in graph", level="ERROR", tag="TASK_GRAPH")
            return False
        node.status = TaskStatus.DONE
        node.last_completed = _now_iso()
        self._persist_node(node)
        _log_action(self.conn, node.name, node.chain, "DONE")
        self.conn.commit()
        log(f"[{node.chain}] {node.name} -> DONE", tag="TASK_GRAPH")

        # Trigger downstream readiness check
        self._propagate_readiness(node)
        return True

    def mark_failed(self, task_name: str, reason: str = "", skip_downstream: bool = False,
                    chain_name: Optional[str] = None) -> bool:
        """Mark a task as FAILED. Optionally skip all downstream tasks."""
        node = self._find_node(task_name, chain_name)
        if not node:
            log(f"Task '{task_name}' not found in graph", level="ERROR", tag="TASK_GRAPH")
            return False
        node.status = TaskStatus.FAILED
        node.fail_count += 1
        self._persist_node(node)
        _log_action(self.conn, node.name, node.chain, "FAILED", reason)
        self.conn.commit()
        log(f"[{node.chain}] {node.name} -> FAILED (x{node.fail_count}): {reason}", level="WARN", tag="TASK_GRAPH")

        if skip_downstream:
            self._skip_downstream(node)
        return True

    def reset_task(self, task_name: str, chain_name: Optional[str] = None) -> bool:
        """Reset a task to WAITING."""
        node = self._find_node(task_name, chain_name)
        if not node:
            log(f"Task '{task_name}' not found in graph", level="ERROR", tag="TASK_GRAPH")
            return False
        node.status = TaskStatus.WAITING
        node.last_started = None
        self._persist_node(node)
        _log_action(self.conn, node.name, node.chain, "RESET")
        self.conn.commit()
        log(f"[{node.chain}] {node.name} -> RESET to WAITING", tag="TASK_GRAPH")
        return True

    def reset_chain(self, chain_name: str) -> int:
        """Reset all tasks in a chain to WAITING. Returns count reset."""
        count = 0
        for key, node in self.nodes.items():
            if node.chain == chain_name:
                node.status = TaskStatus.WAITING
                node.last_started = None
                self._persist_node(node)
                count += 1
        _log_action(self.conn, "*", chain_name, "CHAIN_RESET")
        self.conn.commit()
        log(f"[{chain_name}] Reset {count} tasks to WAITING", tag="TASK_GRAPH")
        return count

    # -- propagation ---------------------------------------------------------

    def _propagate_readiness(self, completed_node: TaskNode) -> None:
        """After a node completes, check if downstream tasks become READY."""
        completed = self._completed_in_chain(completed_node.chain)
        for ds_name in completed_node.downstream:
            ds_key = f"{completed_node.chain}::{ds_name}"
            ds_node = self.nodes.get(ds_key)
            if ds_node and ds_node.status in (TaskStatus.WAITING, TaskStatus.FAILED):
                if ds_node.is_ready(completed):
                    ds_node.status = TaskStatus.READY
                    self._persist_node(ds_node)
                    log(f"[{ds_node.chain}] {ds_node.name} -> READY (upstream {completed_node.name} done)", tag="TASK_GRAPH")

    def _skip_downstream(self, failed_node: TaskNode) -> None:
        """Recursively skip all downstream tasks in the chain."""
        for ds_name in failed_node.downstream:
            ds_key = f"{failed_node.chain}::{ds_name}"
            ds_node = self.nodes.get(ds_key)
            if ds_node and ds_node.status not in (TaskStatus.DONE, TaskStatus.SKIPPED):
                ds_node.status = TaskStatus.SKIPPED
                self._persist_node(ds_node)
                _log_action(self.conn, ds_node.name, ds_node.chain, "SKIPPED",
                            f"upstream {failed_node.name} failed")
                log(f"[{ds_node.chain}] {ds_node.name} -> SKIPPED (upstream {failed_node.name} failed)",
                    level="WARN", tag="TASK_GRAPH")
                self._skip_downstream(ds_node)
        self.conn.commit()

    # -- queries -------------------------------------------------------------

    def stale_check(self) -> list[TaskNode]:
        """Find tasks that have been RUNNING longer than their timeout_minutes."""
        stale = []
        now = datetime.now(timezone.utc)
        for key, node in self.nodes.items():
            if node.status == TaskStatus.RUNNING and node.last_started and node.timeout_minutes > 0:
                try:
                    started = datetime.fromisoformat(node.last_started)
                    if started.tzinfo is None:
                        started = started.replace(tzinfo=timezone.utc)
                    elapsed_min = (now - started).total_seconds() / 60
                    if elapsed_min > node.timeout_minutes:
                        stale.append(node)
                except (ValueError, TypeError):
                    stale.append(node)  # can't parse start time, flag as stale
        return stale

    def get_status(self) -> dict[str, list[dict]]:
        """Return full graph state organized by chain."""
        result: dict[str, list[dict]] = {}
        for key, node in self.nodes.items():
            chain = node.chain
            if chain not in result:
                result[chain] = []
            result[chain].append({
                "name": node.name,
                "status": node.status.value,
                "upstream": node.upstream_deps,
                "downstream": node.downstream,
                "last_completed": node.last_completed,
                "last_started": node.last_started,
                "timeout_min": node.timeout_minutes,
                "fail_count": node.fail_count,
            })
        return result

    def get_chain_status(self, chain_name: str) -> list[dict]:
        """Return specific chain state."""
        full = self.get_status()
        return full.get(chain_name, [])

    def close(self) -> None:
        self.conn.close()

    # -- ASCII visualization -------------------------------------------------

    def visualize(self, chain_name: Optional[str] = None) -> str:
        """Generate ASCII art DAG visualization."""
        lines: list[str] = []
        status_icons = {
            TaskStatus.WAITING: "[ ]",
            TaskStatus.READY: "[>]",
            TaskStatus.RUNNING: "[~]",
            TaskStatus.DONE: "[x]",
            TaskStatus.FAILED: "[!]",
            TaskStatus.SKIPPED: "[-]",
        }
        status_colors = {
            TaskStatus.WAITING: "",
            TaskStatus.READY: " << READY",
            TaskStatus.RUNNING: " << RUNNING",
            TaskStatus.DONE: "",
            TaskStatus.FAILED: " << FAILED",
            TaskStatus.SKIPPED: " (skipped)",
        }

        chains_to_show = [chain_name] if chain_name else list(CHAINS.keys())

        for cn in chains_to_show:
            if cn not in CHAINS:
                lines.append(f"Unknown chain: {cn}")
                continue

            lines.append("")
            lines.append(f"=== {cn} ===")
            lines.append("")

            tasks_in_chain = [(k, n) for k, n in self.nodes.items() if n.chain == cn]
            # Sort by dependency order (matching the CHAINS definition order)
            chain_order = [t[0] for t in CHAINS[cn]]
            tasks_in_chain.sort(key=lambda x: chain_order.index(x[1].name) if x[1].name in chain_order else 999)

            for i, (key, node) in enumerate(tasks_in_chain):
                icon = status_icons.get(node.status, "[ ]")
                suffix = status_colors.get(node.status, "")
                name_padded = node.name.ljust(25)
                timeout_str = f"({node.timeout_minutes}min)" if node.timeout_minutes > 0 else "(no timeout)"
                fail_str = f" [fails: {node.fail_count}]" if node.fail_count > 0 else ""

                lines.append(f"  {icon} {name_padded} {timeout_str}{fail_str}{suffix}")

                # Draw arrow to next task
                if i < len(tasks_in_chain) - 1:
                    lines.append("       |")
                    lines.append("       v")

        lines.append("")
        lines.append("Legend: [ ] WAITING  [>] READY  [~] RUNNING  [x] DONE  [!] FAILED  [-] SKIPPED")
        lines.append("")

        # Time-based tasks not in the DAG
        lines.append("=== TIME-BASED (not in DAG) ===")
        lines.append("")
        for t in TIME_BASED_TASKS:
            lines.append(f"  [T] {t}")
        lines.append("")

        return "\n".join(lines)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def main() -> None:
    parser = argparse.ArgumentParser(
        description="T016 — Native Task Dependency Graph",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --status                        Full graph status (JSON)
  %(prog)s --chain CHAIN_ALPHA_PIPELINE    Single chain status
  %(prog)s --ready                         List tasks ready to run
  %(prog)s --mark-done scraper             Mark task as completed
  %(prog)s --mark-failed scraper --reason "API down"
  %(prog)s --stale                         Find stale RUNNING tasks
  %(prog)s --reset scraper                 Reset a task to WAITING
  %(prog)s --reset-chain CHAIN_CONTENT     Reset entire chain
  %(prog)s --visualize                     ASCII art DAG
  %(prog)s --visualize --chain CHAIN_ARB   Single chain ASCII art
        """,
    )

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--status", action="store_true", help="Full graph status (JSON)")
    group.add_argument("--chain", type=str, metavar="CHAIN_NAME", help="Show specific chain status")
    group.add_argument("--ready", action="store_true", help="List tasks ready to run")
    group.add_argument("--mark-done", type=str, metavar="TASK_NAME", help="Mark task as DONE")
    group.add_argument("--mark-started", type=str, metavar="TASK_NAME", help="Mark task as RUNNING")
    group.add_argument("--mark-failed", type=str, metavar="TASK_NAME", help="Mark task as FAILED")
    group.add_argument("--stale", action="store_true", help="Find stale RUNNING tasks")
    group.add_argument("--reset", type=str, metavar="TASK_NAME", help="Reset task to WAITING")
    group.add_argument("--reset-chain", type=str, metavar="CHAIN_NAME", help="Reset entire chain to WAITING")
    group.add_argument("--visualize", action="store_true", help="ASCII art DAG visualization")

    parser.add_argument("--reason", type=str, default="", help="Failure reason (with --mark-failed)")
    parser.add_argument("--skip-downstream", action="store_true", help="Skip downstream on failure")
    parser.add_argument("--chain-filter", type=str, metavar="CHAIN_NAME",
                        help="Scope task lookup to specific chain (for tasks that appear in multiple chains)")
    parser.add_argument("--json", action="store_true", help="Output as JSON (for agent consumption)")

    args = parser.parse_args()

    try:
        graph = TaskGraph()
    except Exception as e:
        log(f"Failed to initialize TaskGraph: {e}", level="ERROR", tag="TASK_GRAPH")
        sys.exit(1)

    try:
        if args.status:
            status = graph.get_status()
            if args.json:
                print(json.dumps(status, indent=2))
            else:
                for chain_name, tasks in status.items():
                    print(f"\n{'='*60}")
                    print(f"  {chain_name}")
                    print(f"{'='*60}")
                    for t in tasks:
                        status_str = t["status"].ljust(8)
                        fail_str = f" [fails: {t['fail_count']}]" if t["fail_count"] > 0 else ""
                        done_str = f" last_done: {t['last_completed']}" if t["last_completed"] else ""
                        print(f"  {status_str} {t['name']}{fail_str}{done_str}")
                print()

        elif args.chain:
            chain_status = graph.get_chain_status(args.chain)
            if not chain_status:
                print(f"Unknown chain: {args.chain}")
                print(f"Available chains: {', '.join(CHAINS.keys())}")
                sys.exit(1)
            if args.json:
                print(json.dumps(chain_status, indent=2))
            else:
                print(f"\n  {args.chain}")
                print(f"  {'='*50}")
                for t in chain_status:
                    status_str = t["status"].ljust(8)
                    fail_str = f" [fails: {t['fail_count']}]" if t["fail_count"] > 0 else ""
                    print(f"  {status_str} {t['name']}{fail_str}")
                print()

        elif args.ready:
            ready = graph.check_ready()
            if args.json:
                print(json.dumps([{"name": n.name, "chain": n.chain} for n in ready], indent=2))
            else:
                if ready:
                    print(f"\n  {len(ready)} task(s) READY to run:")
                    for node in ready:
                        print(f"    [{node.chain}] {node.name}")
                    print()
                else:
                    print("\n  No tasks are ready. Check --status for current state.\n")

        elif args.mark_done:
            ok = graph.mark_done(args.mark_done, chain_name=args.chain_filter)
            if ok:
                # Show what became ready
                ready = graph.check_ready()
                newly_ready = [n for n in ready if n.status == TaskStatus.READY]
                if newly_ready:
                    print(f"Newly ready: {', '.join(n.name for n in newly_ready)}")
            else:
                sys.exit(1)

        elif args.mark_started:
            ok = graph.mark_started(args.mark_started, chain_name=args.chain_filter)
            if not ok:
                sys.exit(1)

        elif args.mark_failed:
            ok = graph.mark_failed(
                args.mark_failed,
                reason=args.reason,
                skip_downstream=args.skip_downstream,
                chain_name=args.chain_filter,
            )
            if not ok:
                sys.exit(1)

        elif args.stale:
            stale = graph.stale_check()
            if args.json:
                print(json.dumps([{
                    "name": n.name, "chain": n.chain,
                    "started": n.last_started, "timeout_min": n.timeout_minutes,
                } for n in stale], indent=2))
            else:
                if stale:
                    print(f"\n  {len(stale)} STALE task(s) (exceeded timeout):")
                    for node in stale:
                        print(f"    [{node.chain}] {node.name} started={node.last_started} timeout={node.timeout_minutes}min")
                    print()
                else:
                    print("\n  No stale tasks.\n")

        elif args.reset:
            ok = graph.reset_task(args.reset, chain_name=args.chain_filter)
            if not ok:
                sys.exit(1)

        elif args.reset_chain:
            if args.reset_chain not in CHAINS:
                print(f"Unknown chain: {args.reset_chain}")
                print(f"Available chains: {', '.join(CHAINS.keys())}")
                sys.exit(1)
            count = graph.reset_chain(args.reset_chain)
            print(f"Reset {count} tasks in {args.reset_chain}")

        elif args.visualize:
            chain_filter = args.chain_filter
            print(graph.visualize(chain_name=chain_filter))

    except Exception as e:
        log(f"TaskGraph error: {e}", level="ERROR", tag="TASK_GRAPH")
        sys.exit(1)
    finally:
        graph.close()


if __name__ == "__main__":
    main()
