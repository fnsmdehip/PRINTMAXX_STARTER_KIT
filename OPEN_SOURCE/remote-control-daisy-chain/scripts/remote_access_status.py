#!/usr/bin/env python3
"""Inspect the remote-control stack and optionally persist a snapshot."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tomllib
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path


HOME = Path.home()
TAILSCALE_BIN = Path("/opt/homebrew/bin/tailscale")
TAILSCALE_SOCKET = HOME / ".tailscale-coderelay" / "tailscaled.socket"
CODERELAY_BIN = HOME / ".coderelay" / "bin" / "coderelay"
CODERELAY_CONFIG = HOME / ".coderelay" / "config.json"
RUSTDESK_BIN = HOME / "Applications" / "RustDesk.app" / "Contents" / "MacOS" / "RustDesk"
RUSTDESK_CONFIG = HOME / "Library" / "Preferences" / "com.carriez.RustDesk" / "RustDesk.toml"
DEFAULT_STATE_PATH = HOME / ".remote_access_state.json"


def run_command(*args: str) -> tuple[bool, str]:
    try:
        result = subprocess.run(args, text=True, capture_output=True, check=False)
    except FileNotFoundError:
        return False, ""
    output = (result.stdout or "") + (result.stderr or "")
    return result.returncode == 0, output.strip()


def fetch_json(url: str) -> tuple[bool, dict | str]:
    try:
        with urllib.request.urlopen(url, timeout=3) as response:
            payload = response.read().decode("utf-8")
        return True, json.loads(payload)
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, json.JSONDecodeError) as exc:
        return False, str(exc)


def tailscale_state() -> dict:
    state = {
        "installed": TAILSCALE_BIN.exists(),
        "socket_exists": TAILSCALE_SOCKET.exists(),
    }
    if not state["installed"] or not state["socket_exists"]:
        return state

    ok, output = run_command(str(TAILSCALE_BIN), f"--socket={TAILSCALE_SOCKET}", "status", "--json")
    if ok and output:
        status = json.loads(output)
        self_status = status.get("Self") or {}
        state.update(
            {
                "backend_state": status.get("BackendState"),
                "dns_name": (self_status.get("DNSName") or "").rstrip("."),
                "tailscale_ips": self_status.get("TailscaleIPs") or [],
                "tailnet_url": f"https://{(self_status.get('DNSName') or '').rstrip('.')}"
                if self_status.get("DNSName")
                else "",
            }
        )
    else:
        state["status_error"] = output

    serve_ok, serve_output = run_command(str(TAILSCALE_BIN), f"--socket={TAILSCALE_SOCKET}", "serve", "status")
    state["serve_status"] = "live" if serve_ok and "proxy" in serve_output else "missing_or_failed"
    state["serve_detail"] = serve_output
    return state


def coderelay_state() -> dict:
    state = {
        "installed": CODERELAY_BIN.exists(),
        "config_exists": CODERELAY_CONFIG.exists(),
        "local_url": "http://127.0.0.1:8790",
    }
    if CODERELAY_CONFIG.exists():
        try:
            cfg = json.loads(CODERELAY_CONFIG.read_text())
            state.update(
                {
                    "config_public_origin": cfg.get("publicOrigin", ""),
                    "server_host": cfg.get("host", ""),
                    "server_port": cfg.get("port", ""),
                }
            )
        except json.JSONDecodeError as exc:
            state["config_error"] = str(exc)

    if CODERELAY_BIN.exists():
        ok, output = run_command(str(CODERELAY_BIN), "status")
        if ok and output:
            try:
                status = json.loads(output)
            except json.JSONDecodeError:
                state["status_error"] = output
            else:
                state["anchor_running"] = ((status.get("anchor") or {}).get("running")) is True
                state["codex_provider"] = ((status.get("providers") or {}).get("codex") or {}).get("status", "")
        else:
            state["status_error"] = output

    health_ok, health_payload = fetch_json("http://127.0.0.1:8790/health")
    state["health_ok"] = health_ok
    state["health"] = health_payload
    return state


def rustdesk_state() -> dict:
    state = {
        "installed": RUSTDESK_BIN.exists(),
        "config_exists": RUSTDESK_CONFIG.exists(),
    }
    if RUSTDESK_CONFIG.exists():
        try:
            cfg = tomllib.loads(RUSTDESK_CONFIG.read_text())
            state["config_has_password"] = bool(cfg.get("password"))
            state["enc_id"] = cfg.get("enc_id", "")
        except tomllib.TOMLDecodeError as exc:
            state["config_error"] = str(exc)

    if RUSTDESK_BIN.exists():
        ok, output = run_command(str(RUSTDESK_BIN), "--get-id")
        if ok:
            state["id"] = output.strip()
        elif output:
            state["id_error"] = output

    return state


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n")


def main() -> int:
    parser = argparse.ArgumentParser(description="Inspect the PRINTMAXX remote-control stack.")
    parser.add_argument("--write", type=Path, help="Write the snapshot to a path.")
    parser.add_argument(
        "--write-home-state",
        action="store_true",
        help="Also write the snapshot to ~/.printmaxx_remote_access.json",
    )
    args = parser.parse_args()

    snapshot = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "tailscale": tailscale_state(),
        "coderelay": coderelay_state(),
        "rustdesk": rustdesk_state(),
    }

    if args.write:
        write_json(args.write, snapshot)
    if args.write_home_state:
        write_json(DEFAULT_STATE_PATH, snapshot)

    print(json.dumps(snapshot, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
