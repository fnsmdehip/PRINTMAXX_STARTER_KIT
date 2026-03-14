"""PRINTMAXX Blocking State Gates (T014 -- BEADS-style)

Deterministic state machine for pipeline quality control.
States persist in SQLite, surviving session restarts and /compact.

States: PENDING -> IMPLEMENTING -> VALIDATING -> REVIEWING -> APPROVED | REJECTED | HUMAN_REQUIRED
Rule: NO transition from REJECTED -> APPROVED without human_override=True logged.

Usage:
    from gates import GateManager
    gm = GateManager()
    gate = gm.create("content_post_123", "content", "CONTENT/social/posting_queue/post_123.txt")
    gate.transition("IMPLEMENTING", "content_compounder started generation", "content_compounder")
    gate.transition("REVIEWING", "evaluator scored 8.2/10", "evaluator_agent")
    gate.transition("APPROVED", "cross-model reviewer confirmed", "adversarial_reviewer")

    # Only APPROVED items proceed
    approved = gm.get_approved("content")

    # Block bad content
    gate.transition("REJECTED", "quality score 3.1/10 -- generic slop", "quality_gate")

    # Escalate to human
    gate.require_human("Revenue-affecting deployment needs manual approval")
"""
from __future__ import annotations

import argparse
import json
import sqlite3
import sys
from datetime import datetime, timezone
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
HUMAN_APPROVAL_PATH = safe_path(PROJECT / "OPS" / "PENDING_HUMAN_APPROVAL.jsonl")

VALID_STATES = frozenset({
    "PENDING",
    "IMPLEMENTING",
    "VALIDATING",
    "REVIEWING",
    "APPROVED",
    "REJECTED",
    "HUMAN_REQUIRED",
})

# Allowed transitions: source -> set of valid targets
ALLOWED_TRANSITIONS: dict[str, set[str]] = {
    "PENDING":          {"IMPLEMENTING", "REJECTED", "HUMAN_REQUIRED"},
    "IMPLEMENTING":     {"VALIDATING", "REJECTED", "HUMAN_REQUIRED"},
    "VALIDATING":       {"REVIEWING", "REJECTED", "HUMAN_REQUIRED"},
    "REVIEWING":        {"APPROVED", "REJECTED", "HUMAN_REQUIRED"},
    "REJECTED":         {"HUMAN_REQUIRED"},  # APPROVED only via human_override
    "HUMAN_REQUIRED":   {"APPROVED", "REJECTED", "IMPLEMENTING"},
    "APPROVED":         set(),  # terminal
}


# ---------------------------------------------------------------------------
# Database initialization
# ---------------------------------------------------------------------------
def _init_db(conn: sqlite3.Connection) -> None:
    """Create tables if they don't exist."""
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS gates (
            gate_id         TEXT PRIMARY KEY,
            asset_type      TEXT NOT NULL,
            asset_path      TEXT NOT NULL,
            state           TEXT NOT NULL DEFAULT 'PENDING',
            evidence        TEXT NOT NULL DEFAULT '',
            agent_name      TEXT NOT NULL DEFAULT '',
            model_used      TEXT NOT NULL DEFAULT '',
            created_at      TEXT NOT NULL,
            updated_at      TEXT NOT NULL,
            human_override  INTEGER NOT NULL DEFAULT 0
        );

        CREATE TABLE IF NOT EXISTS gate_transitions (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            gate_id         TEXT NOT NULL,
            from_state      TEXT NOT NULL,
            to_state        TEXT NOT NULL,
            evidence        TEXT NOT NULL DEFAULT '',
            agent_name      TEXT NOT NULL DEFAULT '',
            model_used      TEXT NOT NULL DEFAULT '',
            human_override  INTEGER NOT NULL DEFAULT 0,
            timestamp       TEXT NOT NULL,
            FOREIGN KEY (gate_id) REFERENCES gates(gate_id)
        );

        CREATE INDEX IF NOT EXISTS idx_gates_state ON gates(state);
        CREATE INDEX IF NOT EXISTS idx_gates_asset_type ON gates(asset_type);
        CREATE INDEX IF NOT EXISTS idx_transitions_gate ON gate_transitions(gate_id);
    """)


def _get_connection() -> sqlite3.Connection:
    """Return a connection with row_factory set."""
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(DB_PATH), timeout=10)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    _init_db(conn)
    return conn


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


# ---------------------------------------------------------------------------
# Gate class
# ---------------------------------------------------------------------------
class Gate:
    """Represents a single gate (one tracked asset)."""

    def __init__(self, row: sqlite3.Row, conn: sqlite3.Connection) -> None:
        self._conn = conn
        self.gate_id: str = row["gate_id"]
        self.asset_type: str = row["asset_type"]
        self.asset_path: str = row["asset_path"]
        self.state: str = row["state"]
        self.evidence: str = row["evidence"]
        self.agent_name: str = row["agent_name"]
        self.model_used: str = row["model_used"]
        self.created_at: str = row["created_at"]
        self.updated_at: str = row["updated_at"]
        self.human_override: bool = bool(row["human_override"])

    # -- core transition --------------------------------------------------

    def transition(
        self,
        new_state: str,
        evidence: str = "",
        agent_name: str = "",
        model_used: str = "",
        human_override: bool = False,
    ) -> None:
        """Move gate to *new_state* with full audit logging.

        Raises ValueError for invalid transitions.
        Raises PermissionError if REJECTED->APPROVED without human_override.
        """
        new_state = new_state.upper()
        if new_state not in VALID_STATES:
            raise ValueError(f"Invalid state: {new_state}. Must be one of {sorted(VALID_STATES)}")

        # Special rule: REJECTED -> APPROVED requires human_override
        if self.state == "REJECTED" and new_state == "APPROVED":
            if not human_override:
                raise PermissionError(
                    f"Gate {self.gate_id}: REJECTED -> APPROVED requires human_override=True. "
                    "Use gate.transition('APPROVED', evidence, human_override=True)."
                )
            # Allow the override -- skip normal transition check
        else:
            allowed = ALLOWED_TRANSITIONS.get(self.state, set())
            if new_state not in allowed:
                raise ValueError(
                    f"Gate {self.gate_id}: transition {self.state} -> {new_state} is not allowed. "
                    f"Valid targets from {self.state}: {sorted(allowed) if allowed else 'NONE (terminal state)'}"
                )

        now = _now_iso()
        old_state = self.state

        # Write transition record
        self._conn.execute(
            """INSERT INTO gate_transitions
               (gate_id, from_state, to_state, evidence, agent_name, model_used, human_override, timestamp)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (self.gate_id, old_state, new_state, evidence, agent_name, model_used,
             1 if human_override else 0, now),
        )

        # Update gate row
        self._conn.execute(
            """UPDATE gates
               SET state = ?, evidence = ?, agent_name = ?, model_used = ?,
                   updated_at = ?, human_override = ?
               WHERE gate_id = ?""",
            (new_state, evidence, agent_name, model_used, now,
             1 if human_override else 0, self.gate_id),
        )
        self._conn.commit()

        # Update local attrs
        self.state = new_state
        self.evidence = evidence
        self.agent_name = agent_name
        self.model_used = model_used
        self.updated_at = now
        self.human_override = human_override

        log(f"Gate {self.gate_id}: {old_state} -> {new_state} by {agent_name or 'unknown'}", tag="GATE")

        # If new state is HUMAN_REQUIRED, write to JSONL
        if new_state == "HUMAN_REQUIRED":
            self._write_human_required(evidence)

    # -- convenience methods -----------------------------------------------

    def is_blocked(self) -> bool:
        """Returns True if gate is in a blocking state (not APPROVED)."""
        return self.state != "APPROVED"

    def require_human(self, reason: str, agent_name: str = "", model_used: str = "") -> None:
        """Shortcut to transition to HUMAN_REQUIRED."""
        self.transition("HUMAN_REQUIRED", reason, agent_name, model_used)

    def history(self) -> list[dict[str, Any]]:
        """Return full transition history for this gate."""
        rows = self._conn.execute(
            """SELECT * FROM gate_transitions
               WHERE gate_id = ?
               ORDER BY timestamp ASC""",
            (self.gate_id,),
        ).fetchall()
        return [dict(r) for r in rows]

    # -- internal ----------------------------------------------------------

    def _write_human_required(self, reason: str) -> None:
        """Append to OPS/PENDING_HUMAN_APPROVAL.jsonl."""
        HUMAN_APPROVAL_PATH.parent.mkdir(parents=True, exist_ok=True)
        entry = {
            "gate_id": self.gate_id,
            "asset_type": self.asset_type,
            "asset_path": self.asset_path,
            "reason": reason,
            "agent_name": self.agent_name,
            "model_used": self.model_used,
            "timestamp": _now_iso(),
        }
        with open(HUMAN_APPROVAL_PATH, "a") as f:
            f.write(json.dumps(entry) + "\n")
        log(f"HUMAN_REQUIRED: {self.gate_id} -- {reason}", level="WARN", tag="GATE")

    def to_dict(self) -> dict[str, Any]:
        """Serialize gate to dict."""
        return {
            "gate_id": self.gate_id,
            "asset_type": self.asset_type,
            "asset_path": self.asset_path,
            "state": self.state,
            "evidence": self.evidence,
            "agent_name": self.agent_name,
            "model_used": self.model_used,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "human_override": self.human_override,
        }

    def __repr__(self) -> str:
        return f"<Gate {self.gate_id} state={self.state} type={self.asset_type}>"


# ---------------------------------------------------------------------------
# GateManager class
# ---------------------------------------------------------------------------
class GateManager:
    """Central manager for all gates. Thread-safe via SQLite WAL mode."""

    def __init__(self, db_path: Optional[str | Path] = None) -> None:
        if db_path is not None:
            self._db_path = Path(db_path)
        else:
            self._db_path = DB_PATH
        self._db_path.parent.mkdir(parents=True, exist_ok=True)
        self._conn = _get_connection()

    def close(self) -> None:
        self._conn.close()

    # -- create & get ------------------------------------------------------

    def create(
        self,
        gate_id: str,
        asset_type: str,
        asset_path: str,
        agent_name: str = "",
        model_used: str = "",
    ) -> Gate:
        """Create a new gate in PENDING state. Raises if gate_id already exists."""
        now = _now_iso()
        try:
            self._conn.execute(
                """INSERT INTO gates
                   (gate_id, asset_type, asset_path, state, evidence, agent_name,
                    model_used, created_at, updated_at, human_override)
                   VALUES (?, ?, ?, 'PENDING', '', ?, ?, ?, ?, 0)""",
                (gate_id, asset_type, asset_path, agent_name, model_used, now, now),
            )
            self._conn.commit()
        except sqlite3.IntegrityError:
            raise ValueError(f"Gate {gate_id} already exists. Use get() to retrieve it.")

        log(f"Gate created: {gate_id} (type={asset_type})", tag="GATE")

        # Record initial transition
        self._conn.execute(
            """INSERT INTO gate_transitions
               (gate_id, from_state, to_state, evidence, agent_name, model_used,
                human_override, timestamp)
               VALUES (?, '', 'PENDING', 'Gate created', ?, ?, 0, ?)""",
            (gate_id, agent_name, model_used, now),
        )
        self._conn.commit()

        return self.get(gate_id)

    def get(self, gate_id: str) -> Gate:
        """Retrieve a gate by ID. Raises KeyError if not found."""
        row = self._conn.execute(
            "SELECT * FROM gates WHERE gate_id = ?", (gate_id,)
        ).fetchone()
        if row is None:
            raise KeyError(f"Gate not found: {gate_id}")
        return Gate(row, self._conn)

    def get_or_create(
        self,
        gate_id: str,
        asset_type: str = "",
        asset_path: str = "",
        agent_name: str = "",
        model_used: str = "",
    ) -> Gate:
        """Get existing gate or create a new one."""
        try:
            return self.get(gate_id)
        except KeyError:
            return self.create(gate_id, asset_type, asset_path, agent_name, model_used)

    # -- query methods -----------------------------------------------------

    def get_by_state(self, state: str, asset_type: Optional[str] = None) -> list[Gate]:
        """Return all gates in a given state, optionally filtered by asset_type."""
        state = state.upper()
        if asset_type:
            rows = self._conn.execute(
                "SELECT * FROM gates WHERE state = ? AND asset_type = ? ORDER BY updated_at DESC",
                (state, asset_type),
            ).fetchall()
        else:
            rows = self._conn.execute(
                "SELECT * FROM gates WHERE state = ? ORDER BY updated_at DESC",
                (state,),
            ).fetchall()
        return [Gate(r, self._conn) for r in rows]

    def get_approved(self, asset_type: Optional[str] = None) -> list[Gate]:
        """Return all APPROVED gates."""
        return self.get_by_state("APPROVED", asset_type)

    def get_rejected(self, asset_type: Optional[str] = None) -> list[Gate]:
        """Return all REJECTED gates."""
        return self.get_by_state("REJECTED", asset_type)

    def get_human_required(self, asset_type: Optional[str] = None) -> list[Gate]:
        """Return all HUMAN_REQUIRED gates."""
        return self.get_by_state("HUMAN_REQUIRED", asset_type)

    def get_pending(self, asset_type: Optional[str] = None) -> list[Gate]:
        """Return all PENDING gates."""
        return self.get_by_state("PENDING", asset_type)

    def get_all(self, asset_type: Optional[str] = None) -> list[Gate]:
        """Return all gates, optionally filtered by asset_type."""
        if asset_type:
            rows = self._conn.execute(
                "SELECT * FROM gates WHERE asset_type = ? ORDER BY updated_at DESC",
                (asset_type,),
            ).fetchall()
        else:
            rows = self._conn.execute(
                "SELECT * FROM gates ORDER BY updated_at DESC"
            ).fetchall()
        return [Gate(r, self._conn) for r in rows]

    # -- stats -------------------------------------------------------------

    def stats(self) -> dict[str, Any]:
        """Return aggregate statistics about all gates."""
        total_row = self._conn.execute("SELECT COUNT(*) as cnt FROM gates").fetchone()
        total = total_row["cnt"] if total_row else 0

        state_counts: dict[str, int] = {}
        for state in sorted(VALID_STATES):
            row = self._conn.execute(
                "SELECT COUNT(*) as cnt FROM gates WHERE state = ?", (state,)
            ).fetchone()
            state_counts[state] = row["cnt"] if row else 0

        type_rows = self._conn.execute(
            "SELECT asset_type, COUNT(*) as cnt FROM gates GROUP BY asset_type ORDER BY cnt DESC"
        ).fetchall()
        type_counts = {r["asset_type"]: r["cnt"] for r in type_rows}

        transition_row = self._conn.execute(
            "SELECT COUNT(*) as cnt FROM gate_transitions"
        ).fetchone()
        total_transitions = transition_row["cnt"] if transition_row else 0

        override_row = self._conn.execute(
            "SELECT COUNT(*) as cnt FROM gate_transitions WHERE human_override = 1"
        ).fetchone()
        human_overrides = override_row["cnt"] if override_row else 0

        return {
            "total_gates": total,
            "by_state": state_counts,
            "by_type": type_counts,
            "total_transitions": total_transitions,
            "human_overrides": human_overrides,
            "db_path": str(self._db_path),
        }


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def _format_gate_table(gates: list[Gate]) -> str:
    """Format gates as a readable table."""
    if not gates:
        return "  (none)"
    lines = []
    header = f"  {'GATE ID':<35} {'STATE':<17} {'TYPE':<15} {'AGENT':<25} {'UPDATED':<25}"
    lines.append(header)
    lines.append("  " + "-" * (len(header) - 2))
    for g in gates:
        updated = g.updated_at[:19] if g.updated_at else ""
        lines.append(
            f"  {g.gate_id:<35} {g.state:<17} {g.asset_type:<15} "
            f"{g.agent_name:<25} {updated:<25}"
        )
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="PRINTMAXX Blocking State Gates (T014)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--stats", action="store_true", help="Show gate statistics")
    parser.add_argument("--pending", action="store_true", help="List PENDING gates")
    parser.add_argument("--approved", action="store_true", help="List APPROVED gates")
    parser.add_argument("--rejected", action="store_true", help="List REJECTED gates")
    parser.add_argument("--human-required", action="store_true", help="List HUMAN_REQUIRED gates")
    parser.add_argument("--all", action="store_true", help="List all gates")
    parser.add_argument(
        "--transition", nargs=3, metavar=("GATE_ID", "NEW_STATE", "EVIDENCE"),
        help="Transition a gate: --transition GATE_ID NEW_STATE 'reason text'",
    )
    parser.add_argument(
        "--human-override", action="store_true",
        help="Set human_override=True on --transition (required for REJECTED->APPROVED)",
    )
    parser.add_argument("--type", type=str, default=None, help="Filter by asset_type")
    parser.add_argument(
        "--history", type=str, metavar="GATE_ID",
        help="Show full transition history for a gate",
    )
    parser.add_argument(
        "--create", nargs=3, metavar=("GATE_ID", "ASSET_TYPE", "ASSET_PATH"),
        help="Create a new gate: --create GATE_ID ASSET_TYPE ASSET_PATH",
    )
    parser.add_argument("--json", action="store_true", help="Output as JSON")

    args = parser.parse_args()
    gm = GateManager()

    try:
        if args.stats:
            s = gm.stats()
            if args.json:
                print(json.dumps(s, indent=2))
            else:
                print("\n=== PRINTMAXX Gate Statistics ===")
                print(f"  Total gates:       {s['total_gates']}")
                print(f"  Total transitions: {s['total_transitions']}")
                print(f"  Human overrides:   {s['human_overrides']}")
                print(f"  DB path:           {s['db_path']}")
                print("\n  By state:")
                for state, count in sorted(s["by_state"].items()):
                    marker = " *" if count > 0 else ""
                    print(f"    {state:<17} {count}{marker}")
                if s["by_type"]:
                    print("\n  By asset type:")
                    for atype, count in s["by_type"].items():
                        print(f"    {atype:<20} {count}")
                print()

        elif args.pending:
            gates = gm.get_pending(args.type)
            if args.json:
                print(json.dumps([g.to_dict() for g in gates], indent=2))
            else:
                print(f"\n=== PENDING Gates ({len(gates)}) ===")
                print(_format_gate_table(gates))
                print()

        elif args.approved:
            gates = gm.get_approved(args.type)
            if args.json:
                print(json.dumps([g.to_dict() for g in gates], indent=2))
            else:
                print(f"\n=== APPROVED Gates ({len(gates)}) ===")
                print(_format_gate_table(gates))
                print()

        elif args.rejected:
            gates = gm.get_rejected(args.type)
            if args.json:
                print(json.dumps([g.to_dict() for g in gates], indent=2))
            else:
                print(f"\n=== REJECTED Gates ({len(gates)}) ===")
                print(_format_gate_table(gates))
                print()

        elif args.human_required:
            gates = gm.get_human_required(args.type)
            if args.json:
                print(json.dumps([g.to_dict() for g in gates], indent=2))
            else:
                print(f"\n=== HUMAN_REQUIRED Gates ({len(gates)}) ===")
                print(_format_gate_table(gates))
                print()

        elif args.all:
            gates = gm.get_all(args.type)
            if args.json:
                print(json.dumps([g.to_dict() for g in gates], indent=2))
            else:
                print(f"\n=== All Gates ({len(gates)}) ===")
                print(_format_gate_table(gates))
                print()

        elif args.transition:
            gate_id, new_state, evidence = args.transition
            try:
                gate = gm.get(gate_id)
            except KeyError:
                print(f"ERROR: Gate '{gate_id}' not found.")
                sys.exit(1)
            try:
                gate.transition(
                    new_state, evidence,
                    agent_name="cli_user",
                    human_override=args.human_override,
                )
                print(f"OK: {gate_id} -> {new_state}")
                if args.json:
                    print(json.dumps(gate.to_dict(), indent=2))
            except (ValueError, PermissionError) as e:
                print(f"ERROR: {e}")
                sys.exit(1)

        elif args.history:
            try:
                gate = gm.get(args.history)
            except KeyError:
                print(f"ERROR: Gate '{args.history}' not found.")
                sys.exit(1)
            hist = gate.history()
            if args.json:
                print(json.dumps(hist, indent=2))
            else:
                print(f"\n=== Transition History: {args.history} ===")
                print(f"  Current state: {gate.state}")
                print(f"  Asset: {gate.asset_path} (type={gate.asset_type})")
                print()
                for h in hist:
                    ts_str = h["timestamp"][:19] if h["timestamp"] else ""
                    override = " [HUMAN_OVERRIDE]" if h["human_override"] else ""
                    from_s = h["from_state"] or "(created)"
                    print(f"  {ts_str}  {from_s} -> {h['to_state']}  "
                          f"by {h['agent_name'] or 'unknown'}{override}")
                    if h["evidence"]:
                        print(f"              {h['evidence']}")
                print()

        elif args.create:
            gate_id, asset_type, asset_path = args.create
            try:
                gate = gm.create(gate_id, asset_type, asset_path, agent_name="cli_user")
                print(f"OK: Created gate '{gate_id}' (type={asset_type}, state=PENDING)")
                if args.json:
                    print(json.dumps(gate.to_dict(), indent=2))
            except ValueError as e:
                print(f"ERROR: {e}")
                sys.exit(1)

        else:
            # Default: show stats
            s = gm.stats()
            if s["total_gates"] == 0:
                print("\n=== PRINTMAXX Gates ===")
                print("  No gates created yet.")
                print("  Create one: python3 gates.py --create GATE_ID ASSET_TYPE ASSET_PATH")
                print("  Full help:  python3 gates.py --help")
                print()
            else:
                # Show stats as default
                print("\n=== PRINTMAXX Gate Statistics ===")
                print(f"  Total gates:       {s['total_gates']}")
                print(f"  Total transitions: {s['total_transitions']}")
                print(f"  Human overrides:   {s['human_overrides']}")
                active = s["by_state"].get("PENDING", 0) + s["by_state"].get("IMPLEMENTING", 0) + \
                         s["by_state"].get("VALIDATING", 0) + s["by_state"].get("REVIEWING", 0)
                print(f"  Active (in-flight): {active}")
                print(f"  Approved:          {s['by_state'].get('APPROVED', 0)}")
                print(f"  Rejected:          {s['by_state'].get('REJECTED', 0)}")
                print(f"  Human required:    {s['by_state'].get('HUMAN_REQUIRED', 0)}")
                print()
                print("  Commands: --stats | --pending | --approved | --rejected | --human-required")
                print("            --all | --history GATE_ID | --create ID TYPE PATH")
                print("            --transition GATE_ID STATE 'evidence' [--human-override]")
                print()
    finally:
        gm.close()


if __name__ == "__main__":
    main()
