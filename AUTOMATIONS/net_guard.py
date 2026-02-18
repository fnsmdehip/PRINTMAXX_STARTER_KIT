#!/usr/bin/env python3
"""Network guard for cron-style automations.

Ship Captain runs frequently. Some steps require outbound network (SAM.gov, Reddit,
price checks). In sandboxed or offline environments those steps should SKIP cleanly
without creating noisy FAILED runs.

Usage:
  python3 AUTOMATIONS/net_guard.py --host api.sam.gov -- python3 AUTOMATIONS/sam_gov_monitor.py --limit 10
"""

from __future__ import annotations

import argparse
import json
import socket
import subprocess
import sys
import time
from typing import List


def can_connect(host: str, port: int, timeout_sec: float) -> bool:
    try:
        # DNS + TCP connect check. Works without HTTP libs and fails fast when offline.
        with socket.create_connection((host, port), timeout=timeout_sec):
            return True
    except OSError:
        return False


def parse_args() -> argparse.Namespace:
    ap = argparse.ArgumentParser(description="Run a command only if network is reachable.")
    ap.add_argument("--host", default="example.com", help="Host to probe (DNS+TCP). Default: example.com")
    ap.add_argument("--port", type=int, default=443, help="Port to probe. Default: 443")
    ap.add_argument("--timeout-sec", type=float, default=3.0, help="Probe timeout seconds. Default: 3.0")
    ap.add_argument("--key", default="", help="Optional throttle key (stored under OPS/_state).")
    ap.add_argument(
        "--min-interval-sec",
        type=int,
        default=0,
        help="If set with --key, skip if the key ran within this many seconds (best-effort).",
    )
    ap.add_argument("cmd", nargs=argparse.REMAINDER, help="Command to run after `--`")
    return ap.parse_args()


def load_state(path) -> dict:
    try:
        if path.exists():
            payload = json.loads(path.read_text(encoding="utf-8"))
            return payload if isinstance(payload, dict) else {}
    except Exception:
        return {}
    return {}


def save_state(path, payload: dict) -> None:
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(payload, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")
    except Exception:
        return


def main() -> int:
    args = parse_args()

    cmd: List[str] = args.cmd
    if cmd and cmd[0] == "--":
        cmd = cmd[1:]
    if not cmd:
        print("net_guard: missing command. Example: net_guard.py --host api.sam.gov -- python3 ...", file=sys.stderr)
        return 2

    key = (args.key or "").strip()
    min_interval = int(args.min_interval_sec or 0)
    state_path = None
    state = {}
    if key and min_interval > 0:
        # Keep state in the repo so cron runs and Codex runs share throttling.
        from pathlib import Path

        base = Path(__file__).resolve().parent.parent
        state_path = base / "OPS" / "_state" / "net_guard_state.json"
        state = load_state(state_path)
        last = state.get(key)
        try:
            last_ts = float(last) if last is not None else 0.0
        except Exception:
            last_ts = 0.0
        now_ts = time.time()
        if last_ts and (now_ts - last_ts) < float(min_interval):
            remaining = int(float(min_interval) - (now_ts - last_ts))
            print(f"net_guard: throttled key={key} remaining_sec={max(0, remaining)}. Skipping: {' '.join(cmd)}")
            return 0

    if not can_connect(args.host, args.port, args.timeout_sec):
        print(f"net_guard: no network to {args.host}:{args.port} (timeout={args.timeout_sec}s). Skipping: {' '.join(cmd)}")
        return 0

    proc = subprocess.run(cmd, check=False)
    if state_path is not None and key:
        state[key] = time.time()
        save_state(state_path, state)
    return int(proc.returncode)


if __name__ == "__main__":
    raise SystemExit(main())
