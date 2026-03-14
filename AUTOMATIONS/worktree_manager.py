#!/usr/bin/env python3
"""Git worktree isolation manager for parallel agent execution.

Prevents file-level conflicts when multiple agents (e.g. content_compounder +
social_poster) write to overlapping paths.  Each agent operates in its own
git worktree; changes are reconciled back to main on a schedule.

CLI:
    python3 AUTOMATIONS/worktree_manager.py --setup NAME
    python3 AUTOMATIONS/worktree_manager.py --merge NAME [--strategy last-write-wins|human-review]
    python3 AUTOMATIONS/worktree_manager.py --cleanup NAME
    python3 AUTOMATIONS/worktree_manager.py --list
    python3 AUTOMATIONS/worktree_manager.py --conflicts NAME
    python3 AUTOMATIONS/worktree_manager.py --reconcile
    python3 AUTOMATIONS/worktree_manager.py --status
"""
from __future__ import annotations

import argparse
import json
import logging
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

# ---------------------------------------------------------------------------
# Shared utilities
# ---------------------------------------------------------------------------
from _common import PROJECT, safe_path, load_json, log as _clog, ts  # noqa: F401

TAG = "WORKTREE"
LOGS_DIR = PROJECT / "AUTOMATIONS" / "logs"
STATE_FILE = PROJECT / "AUTOMATIONS" / "agent" / "worktree_state.json"
PENDING_FILE = PROJECT / "LEDGER" / "PENDING_HUMAN_APPROVAL.jsonl"
WORKTREE_ROOT = PROJECT.parent  # one level up; worktrees live beside project

# Revenue-affecting paths — always require human-review merge strategy
REVENUE_PATHS: list[str] = [
    "LEDGER/LIVE_ARB_PRODUCTS.csv",
    "AUTOMATIONS/agent/ceo_agent/decisions.jsonl",
    "FINANCIALS/",
]

# Known conflict pairs (agents that write to overlapping dirs)
CONFLICT_PAIRS: list[dict[str, Any]] = [
    {
        "agents": ["content_compounder", "social_poster"],
        "paths": ["CONTENT/social/posting_queue/"],
        "default_strategy": "last-write-wins",
    },
    {
        "agents": ["asset_deployer", "app_factory_autopilot"],
        "paths": ["OPS/"],
        "default_strategy": "last-write-wins",
    },
]

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------

def _setup_logger() -> logging.Logger:
    LOGS_DIR.mkdir(parents=True, exist_ok=True)
    logger = logging.getLogger("worktree_manager")
    logger.setLevel(logging.DEBUG)
    if not logger.handlers:
        fh = logging.FileHandler(LOGS_DIR / "worktree_manager.log", encoding="utf-8")
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))
        logger.addHandler(fh)
        sh = logging.StreamHandler()
        sh.setLevel(logging.INFO)
        sh.setFormatter(logging.Formatter("[%(asctime)s] [WORKTREE] [%(levelname)s] %(message)s",
                                          datefmt="%H:%M:%S"))
        logger.addHandler(sh)
    return logger

logger = _setup_logger()

# ---------------------------------------------------------------------------
# Low-level git helpers
# ---------------------------------------------------------------------------

def _run_git(args: list[str], cwd: str | Path | None = None,
             timeout: int = 60) -> tuple[bool, str]:
    """Run a git command.  Returns (success, stdout_or_stderr)."""
    cmd = ["git"] + args
    try:
        r = subprocess.run(
            cmd, capture_output=True, text=True,
            timeout=timeout, cwd=str(cwd or PROJECT),
        )
        output = (r.stdout.strip() or r.stderr.strip())
        return r.returncode == 0, output
    except FileNotFoundError:
        return False, "git not found on PATH"
    except subprocess.TimeoutExpired:
        return False, f"git timeout after {timeout}s"
    except Exception as exc:
        return False, str(exc)


def _git_is_repo() -> bool:
    """Return True if PROJECT is inside a git working tree."""
    ok, _ = _run_git(["rev-parse", "--is-inside-work-tree"])
    return ok


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")

# ---------------------------------------------------------------------------
# State persistence
# ---------------------------------------------------------------------------

def _load_state() -> dict[str, Any]:
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    return load_json(STATE_FILE, {
        "worktrees": {},
        "last_reconciliation": None,
        "conflict_history": [],
    })


def _save_state(state: dict[str, Any]) -> None:
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    tmp = STATE_FILE.with_suffix(".tmp")
    tmp.write_text(json.dumps(state, indent=2, default=str))
    tmp.replace(STATE_FILE)


def _worktree_path(name: str) -> Path:
    """Path for worktree named *name*: PROJECT.parent / printmaxx-{name}/"""
    return WORKTREE_ROOT / f"printmaxx-{name}"


def _is_revenue_path(rel: str) -> bool:
    """Return True if *rel* (relative to project root) is revenue-affecting."""
    for rp in REVENUE_PATHS:
        if rp.endswith("/"):
            if rel.startswith(rp):
                return True
        elif rel == rp:
            return True
    return False

# ---------------------------------------------------------------------------
# WorktreeManager
# ---------------------------------------------------------------------------

class WorktreeManager:
    """Manages git worktrees for parallel agent isolation."""

    def __init__(self) -> None:
        self._is_git = _git_is_repo()
        if not self._is_git:
            logger.warning("Project is NOT a git repo — worktree ops will be skipped")

    # -- public API ----------------------------------------------------------

    def setup_worktree(self, name: str, base_branch: str = "main") -> Path | None:
        """Create a worktree at PROJECT.parent/printmaxx-{name}/.

        Returns the worktree Path on success, None on failure.
        """
        if not self._is_git:
            logger.warning("setup_worktree(%s) skipped — not a git repo", name)
            return None

        wt_path = _worktree_path(name)
        branch_name = f"worktree/{name}"

        if wt_path.exists():
            logger.info("Worktree already exists at %s", wt_path)
            return wt_path

        # Ensure base branch exists
        ok, _ = _run_git(["rev-parse", "--verify", base_branch])
        if not ok:
            logger.error("Base branch '%s' does not exist", base_branch)
            return None

        # Create worktree with new branch
        ok, out = _run_git(["worktree", "add", "-b", branch_name, str(wt_path), base_branch])
        if not ok:
            # Branch might already exist — try without -b
            ok, out = _run_git(["worktree", "add", str(wt_path), branch_name])
            if not ok:
                logger.error("Failed to create worktree '%s': %s", name, out)
                return None

        logger.info("Created worktree '%s' at %s (branch: %s)", name, wt_path, branch_name)

        # Update state
        state = _load_state()
        state["worktrees"][name] = {
            "path": str(wt_path),
            "branch": branch_name,
            "base_branch": base_branch,
            "created_at": _now_iso(),
            "status": "active",
            "merge_count": 0,
        }
        _save_state(state)
        return wt_path

    def merge_worktree(self, name: str, strategy: str = "last-write-wins") -> bool:
        """Merge worktree changes back into its base branch.

        Strategies:
            last-write-wins — auto-resolve conflicts by accepting worktree changes
            human-review    — write conflicts to PENDING_HUMAN_APPROVAL.jsonl
        """
        if not self._is_git:
            logger.warning("merge_worktree(%s) skipped — not a git repo", name)
            return False

        state = _load_state()
        wt_info = state.get("worktrees", {}).get(name)
        if not wt_info:
            logger.error("No tracked worktree named '%s'", name)
            return False

        wt_path = Path(wt_info["path"])
        branch = wt_info["branch"]
        base = wt_info.get("base_branch", "main")

        if not wt_path.exists():
            logger.error("Worktree path %s does not exist", wt_path)
            return False

        # Auto-commit any uncommitted changes in the worktree
        self._auto_commit(wt_path, name)

        # Check for conflicts before merging
        conflicts = self.get_conflicts(name)

        # Check if any conflicting files are revenue-affecting
        revenue_conflicts = [f for f in conflicts if _is_revenue_path(f)]
        if revenue_conflicts and strategy != "human-review":
            logger.warning(
                "Revenue-affecting files in conflict: %s — forcing human-review strategy",
                revenue_conflicts,
            )
            strategy = "human-review"

        # Switch to base branch in main project and merge
        current_branch_ok, current_branch = _run_git(["rev-parse", "--abbrev-ref", "HEAD"])

        ok, out = _run_git(["checkout", base])
        if not ok:
            logger.error("Failed to checkout base branch '%s': %s", base, out)
            return False

        if strategy == "last-write-wins":
            ok, out = _run_git(["merge", branch, "-X", "theirs",
                                "-m", f"worktree merge: {name} (last-write-wins)"])
        elif strategy == "human-review":
            ok, out = _run_git(["merge", branch, "--no-commit", "--no-ff"])
        else:
            logger.error("Unknown strategy: %s", strategy)
            if current_branch_ok:
                _run_git(["checkout", current_branch])
            return False

        if not ok and strategy == "last-write-wins":
            # Force resolve with theirs
            _run_git(["checkout", "--theirs", "."])
            _run_git(["add", "-A"])
            _run_git(["commit", "-m", f"worktree merge: {name} (forced last-write-wins)"])
            logger.info("Forced merge for '%s' using last-write-wins", name)
            ok = True

        if not ok and strategy == "human-review":
            self._write_pending_approval(name, conflicts)
            _run_git(["merge", "--abort"])
            logger.info("Merge for '%s' requires human review — written to PENDING_HUMAN_APPROVAL.jsonl", name)
            if current_branch_ok:
                _run_git(["checkout", current_branch])
            return False

        if ok and strategy == "human-review":
            # Check for pending conflicts after --no-commit merge
            pending = self.get_conflicts(name)
            if pending:
                self._write_pending_approval(name, pending)
                _run_git(["merge", "--abort"])
                logger.info("Merge for '%s' has conflicts — written to PENDING_HUMAN_APPROVAL.jsonl", name)
                if current_branch_ok:
                    _run_git(["checkout", current_branch])
                return False
            # No conflicts: commit
            _run_git(["commit", "-m", f"worktree merge: {name} (human-review, clean)"])

        # Update state
        wt_info["merge_count"] = wt_info.get("merge_count", 0) + 1
        wt_info["last_merged"] = _now_iso()
        wt_info["status"] = "merged"
        _save_state(state)

        # Restore original branch
        if current_branch_ok and current_branch != base:
            _run_git(["checkout", current_branch])

        logger.info("Successfully merged worktree '%s' using %s strategy", name, strategy)
        return True

    def cleanup_worktree(self, name: str) -> bool:
        """Remove a worktree after successful merge.  Never removes main."""
        if not self._is_git:
            logger.warning("cleanup_worktree(%s) skipped — not a git repo", name)
            return False

        if name == "main":
            logger.error("BLOCKED: cannot cleanup main worktree")
            return False

        state = _load_state()
        wt_info = state.get("worktrees", {}).get(name)
        if not wt_info:
            logger.error("No tracked worktree named '%s'", name)
            return False

        wt_path = Path(wt_info["path"])
        branch = wt_info.get("branch", f"worktree/{name}")

        # Remove the worktree
        if wt_path.exists():
            ok, out = _run_git(["worktree", "remove", str(wt_path), "--force"])
            if not ok:
                logger.error("Failed to remove worktree at %s: %s", wt_path, out)
                return False
        else:
            # Prune stale worktrees
            _run_git(["worktree", "prune"])

        # Delete the branch
        _run_git(["branch", "-D", branch])

        # Remove from state
        del state["worktrees"][name]
        _save_state(state)

        logger.info("Cleaned up worktree '%s' (path: %s, branch: %s)", name, wt_path, branch)
        return True

    def list_worktrees(self) -> list[dict[str, Any]]:
        """Return tracked worktrees with name, path, branch, created_at."""
        state = _load_state()
        results: list[dict[str, Any]] = []
        for name, info in state.get("worktrees", {}).items():
            results.append({
                "name": name,
                "path": info.get("path", ""),
                "branch": info.get("branch", ""),
                "created_at": info.get("created_at", ""),
                "status": info.get("status", "unknown"),
                "base_branch": info.get("base_branch", "main"),
                "merge_count": info.get("merge_count", 0),
                "last_merged": info.get("last_merged"),
            })
        return results

    def get_conflicts(self, name: str) -> list[str]:
        """Return list of file paths with conflicts between worktree and main."""
        if not self._is_git:
            return []

        state = _load_state()
        wt_info = state.get("worktrees", {}).get(name)
        if not wt_info:
            logger.warning("No tracked worktree '%s'", name)
            return []

        branch = wt_info.get("branch", f"worktree/{name}")
        base = wt_info.get("base_branch", "main")

        # Find merge-base and then diff both sides against it
        ok, merge_base = _run_git(["merge-base", base, branch])
        if not ok:
            logger.warning("Could not find merge-base for %s..%s", base, branch)
            return []

        # Files changed in base since merge-base
        _, base_diff = _run_git(["diff", "--name-only", merge_base, base])
        base_files = set(base_diff.splitlines()) if base_diff else set()

        # Files changed in branch since merge-base
        _, branch_diff = _run_git(["diff", "--name-only", merge_base, branch])
        branch_files = set(branch_diff.splitlines()) if branch_diff else set()

        # Conflicts = files changed on both sides
        conflicts = sorted(base_files & branch_files)
        if conflicts:
            logger.info("Found %d conflict(s) for worktree '%s': %s", len(conflicts), name, conflicts)
            # Record to conflict history
            self._record_conflict(name, conflicts)
        return conflicts

    def reconcile_all(self) -> dict[str, bool]:
        """Merge all active worktrees back to main.  Returns {name: success}."""
        if not self._is_git:
            logger.warning("reconcile_all skipped — not a git repo")
            return {}

        state = _load_state()
        results: dict[str, bool] = {}

        for name, info in list(state.get("worktrees", {}).items()):
            if info.get("status") == "cleaned":
                continue

            # Determine strategy
            strategy = self._strategy_for(name)
            logger.info("Reconciling worktree '%s' with strategy '%s'", name, strategy)
            results[name] = self.merge_worktree(name, strategy=strategy)

        # Update reconciliation timestamp
        state = _load_state()  # re-read after merges
        state["last_reconciliation"] = _now_iso()
        _save_state(state)

        logger.info("Reconciliation complete: %s", results)
        return results

    def status(self) -> dict[str, Any]:
        """Full status report: worktrees, git state, conflict pairs, last reconcile."""
        state = _load_state()
        worktrees = self.list_worktrees()

        # Check each worktree for conflicts
        conflict_report: dict[str, list[str]] = {}
        for wt in worktrees:
            if wt.get("status") != "cleaned":
                conflicts = self.get_conflicts(wt["name"])
                if conflicts:
                    conflict_report[wt["name"]] = conflicts

        return {
            "is_git_repo": self._is_git,
            "worktrees": worktrees,
            "active_count": sum(1 for w in worktrees if w.get("status") == "active"),
            "conflict_pairs_configured": len(CONFLICT_PAIRS),
            "current_conflicts": conflict_report,
            "last_reconciliation": state.get("last_reconciliation"),
            "conflict_history_count": len(state.get("conflict_history", [])),
            "state_file": str(STATE_FILE),
        }

    # -- private helpers -----------------------------------------------------

    def _auto_commit(self, wt_path: Path, name: str) -> None:
        """Commit any uncommitted work in the worktree."""
        _, status_out = _run_git(["status", "--porcelain"], cwd=wt_path)
        if not status_out:
            return  # nothing to commit
        _run_git(["add", "-A"], cwd=wt_path)
        _run_git(["commit", "-m", f"auto-commit: worktree {name} at {_now_iso()}"], cwd=wt_path)
        logger.info("Auto-committed changes in worktree '%s'", name)

    def _strategy_for(self, name: str) -> str:
        """Determine merge strategy for a worktree based on conflict pairs and
        revenue-affecting files."""
        # Check conflict pairs for explicit default strategies
        for pair in CONFLICT_PAIRS:
            if name in pair["agents"]:
                return pair.get("default_strategy", "last-write-wins")

        # Check if the worktree touches revenue-affecting paths
        state = _load_state()
        wt_info = state.get("worktrees", {}).get(name, {})
        branch = wt_info.get("branch", f"worktree/{name}")
        base = wt_info.get("base_branch", "main")

        ok, merge_base = _run_git(["merge-base", base, branch])
        if ok:
            _, diff_out = _run_git(["diff", "--name-only", merge_base, branch])
            if diff_out:
                for f in diff_out.splitlines():
                    if _is_revenue_path(f):
                        logger.info("Revenue path '%s' touched by '%s' — using human-review", f, name)
                        return "human-review"

        return "last-write-wins"

    def _write_pending_approval(self, name: str, conflicts: list[str]) -> None:
        """Append conflict info to PENDING_HUMAN_APPROVAL.jsonl for human review."""
        PENDING_FILE.parent.mkdir(parents=True, exist_ok=True)
        entry = {
            "ts": _now_iso(),
            "type": "worktree_merge_conflict",
            "worktree": name,
            "conflicts": conflicts,
            "revenue_affected": [f for f in conflicts if _is_revenue_path(f)],
            "action_required": "Manually resolve conflicts and merge",
            "command": f"python3 AUTOMATIONS/worktree_manager.py --merge {name} --strategy last-write-wins",
        }
        with open(PENDING_FILE, "a", encoding="utf-8") as fh:
            fh.write(json.dumps(entry) + "\n")
        logger.info("Written pending approval for worktree '%s' (%d conflicts)", name, len(conflicts))

    def _record_conflict(self, name: str, conflicts: list[str]) -> None:
        """Record conflict event in state history."""
        state = _load_state()
        history = state.setdefault("conflict_history", [])
        history.append({
            "ts": _now_iso(),
            "worktree": name,
            "files": conflicts,
        })
        # Keep last 200 entries
        if len(history) > 200:
            state["conflict_history"] = history[-200:]
        _save_state(state)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def _print_table(rows: list[dict[str, Any]], columns: list[str]) -> None:
    """Simple table printer."""
    if not rows:
        print("  (none)")
        return
    widths = {c: max(len(c), *(len(str(r.get(c, ""))) for r in rows)) for c in columns}
    header = "  ".join(c.ljust(widths[c]) for c in columns)
    print(header)
    print("-" * len(header))
    for row in rows:
        print("  ".join(str(row.get(c, "")).ljust(widths[c]) for c in columns))


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Git worktree isolation manager for parallel agent execution",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Examples:\n"
            "  %(prog)s --setup content_compounder\n"
            "  %(prog)s --merge content_compounder --strategy last-write-wins\n"
            "  %(prog)s --cleanup content_compounder\n"
            "  %(prog)s --list\n"
            "  %(prog)s --conflicts content_compounder\n"
            "  %(prog)s --reconcile\n"
            "  %(prog)s --status\n"
        ),
    )

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--setup", metavar="NAME", help="Create a worktree for agent NAME")
    group.add_argument("--merge", metavar="NAME", help="Merge worktree NAME back to base")
    group.add_argument("--cleanup", metavar="NAME", help="Remove worktree NAME after merge")
    group.add_argument("--list", action="store_true", help="List all tracked worktrees")
    group.add_argument("--conflicts", metavar="NAME", help="Show conflicts for worktree NAME")
    group.add_argument("--reconcile", action="store_true", help="Merge all active worktrees")
    group.add_argument("--status", action="store_true", help="Full status report")

    parser.add_argument("--strategy", choices=["last-write-wins", "human-review"],
                        default="last-write-wins",
                        help="Merge strategy (default: last-write-wins)")
    parser.add_argument("--base-branch", default="main",
                        help="Base branch for setup (default: main)")

    args = parser.parse_args()
    mgr = WorktreeManager()

    if args.setup:
        result = mgr.setup_worktree(args.setup, base_branch=args.base_branch)
        if result:
            print(f"Worktree ready: {result}")
        else:
            print("Failed to create worktree")
            sys.exit(1)

    elif args.merge:
        ok = mgr.merge_worktree(args.merge, strategy=args.strategy)
        if ok:
            print(f"Merged worktree '{args.merge}' successfully")
        else:
            print(f"Merge failed for '{args.merge}' — check logs")
            sys.exit(1)

    elif args.cleanup:
        ok = mgr.cleanup_worktree(args.cleanup)
        if ok:
            print(f"Cleaned up worktree '{args.cleanup}'")
        else:
            print(f"Cleanup failed for '{args.cleanup}'")
            sys.exit(1)

    elif args.list:
        worktrees = mgr.list_worktrees()
        print(f"\nTracked worktrees ({len(worktrees)}):\n")
        _print_table(worktrees, ["name", "status", "branch", "path", "created_at", "merge_count"])

    elif args.conflicts:
        conflicts = mgr.get_conflicts(args.conflicts)
        if conflicts:
            print(f"\nConflicts for '{args.conflicts}' ({len(conflicts)} files):\n")
            for f in conflicts:
                rev_tag = " [REVENUE]" if _is_revenue_path(f) else ""
                print(f"  - {f}{rev_tag}")
        else:
            print(f"No conflicts for '{args.conflicts}'")

    elif args.reconcile:
        print("Reconciling all active worktrees...\n")
        results = mgr.reconcile_all()
        if results:
            for name, ok in results.items():
                status_str = "OK" if ok else "FAILED"
                print(f"  {name}: {status_str}")
        else:
            print("  No active worktrees to reconcile")

    elif args.status:
        s = mgr.status()
        print(f"\n=== Worktree Manager Status ===")
        print(f"Git repo: {'yes' if s['is_git_repo'] else 'NO — ops disabled'}")
        print(f"Active worktrees: {s['active_count']}")
        print(f"Conflict pairs configured: {s['conflict_pairs_configured']}")
        print(f"Last reconciliation: {s['last_reconciliation'] or 'never'}")
        print(f"Conflict history entries: {s['conflict_history_count']}")
        print(f"State file: {s['state_file']}")
        print()

        if s["worktrees"]:
            print("Worktrees:")
            _print_table(s["worktrees"], ["name", "status", "branch", "merge_count", "last_merged"])
            print()

        if s["current_conflicts"]:
            print("Current conflicts:")
            for wt_name, files in s["current_conflicts"].items():
                print(f"  {wt_name}:")
                for f in files:
                    rev_tag = " [REVENUE]" if _is_revenue_path(f) else ""
                    print(f"    - {f}{rev_tag}")
            print()

        # Show known conflict pairs
        print("Configured conflict pairs:")
        for pair in CONFLICT_PAIRS:
            print(f"  {' + '.join(pair['agents'])} -> {', '.join(pair['paths'])} (strategy: {pair['default_strategy']})")


if __name__ == "__main__":
    main()
