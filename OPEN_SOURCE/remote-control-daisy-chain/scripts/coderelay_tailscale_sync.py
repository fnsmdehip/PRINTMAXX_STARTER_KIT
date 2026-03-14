#!/usr/bin/env python3
"""Keep CodeRelay aligned with a userspace Tailscale daemon.

Responsibilities:
- detect login-needed state and surface the auth URL in logs
- ensure the node comes up with stable preferences once authenticated
- configure `tailscale serve` for CodeRelay
- update CodeRelay publicOrigin to the MagicDNS URL and restart CodeRelay if needed
"""

from __future__ import annotations

import json
import os
import plistlib
import subprocess
import sys
from pathlib import Path


HOME = Path.home()
TAILSCALE_SOCKET = Path(
    os.environ.get(
        "CODERELAY_TAILSCALE_SOCKET",
        str(HOME / ".tailscale-coderelay" / "tailscaled.socket"),
    )
)
CODERELAY_CONFIG = Path(
    os.environ.get(
        "CODERELAY_CONFIG_PATH",
        str(HOME / ".coderelay" / "config.json"),
    )
)
CODERELAY_PLIST = Path(
    os.environ.get(
        "CODERELAY_PLIST_PATH",
        str(HOME / "Library" / "LaunchAgents" / "com.coderelay.plist"),
    )
)
STATE_FILE = Path(
    os.environ.get(
        "CODERELAY_REMOTE_STATE_FILE",
        str(HOME / ".remote_access_state.json"),
    )
)

TAILSCALE = os.environ.get("CODERELAY_TAILSCALE_BIN", "/opt/homebrew/bin/tailscale")
DESIRED_HOSTNAME = os.environ.get("CODERELAY_TAILSCALE_HOSTNAME", "control-node")
DESIRED_OPERATOR = os.environ.get("CODERELAY_TAILSCALE_OPERATOR", "macuser")
SERVE_TARGET = os.environ.get("CODERELAY_TAILSCALE_SERVE_TARGET", "http://127.0.0.1:8790")
LOCAL_URL = os.environ.get("CODERELAY_LOCAL_URL", SERVE_TARGET)
LAN_FALLBACK_URL = os.environ.get("CODERELAY_LAN_FALLBACK_URL", "")


def run(*args: str, check: bool = False) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        args,
        text=True,
        capture_output=True,
        check=check,
    )


def tailscale(*args: str, check: bool = False) -> subprocess.CompletedProcess[str]:
    return run(TAILSCALE, f"--socket={TAILSCALE_SOCKET}", *args, check=check)


def load_status() -> dict:
    result = tailscale("status", "--json")
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or result.stdout.strip() or "tailscale status failed")
    return json.loads(result.stdout)


def ensure_node_up() -> tuple[bool, str]:
    result = tailscale(
        "up",
        "--reset",
        f"--hostname={DESIRED_HOSTNAME}",
        f"--operator={DESIRED_OPERATOR}",
        "--ssh",
        "--timeout=20s",
    )
    detail = (result.stdout + result.stderr).strip()
    return result.returncode == 0, detail


def ensure_serve() -> tuple[bool, str]:
    status = tailscale("serve", "status")
    text = (status.stdout + status.stderr).strip()
    if SERVE_TARGET in text:
        return True, text or "serve already configured"
    result = tailscale("serve", "--bg", SERVE_TARGET)
    detail = (result.stdout + result.stderr).strip()
    if result.returncode != 0:
        return False, detail or "tailscale serve failed"
    confirm = tailscale("serve", "status")
    confirm_text = (confirm.stdout + confirm.stderr).strip()
    return SERVE_TARGET in confirm_text, confirm_text or detail or "serve configured"


def update_coderelay_public_origin(origin: str) -> bool:
    changed = False

    cfg = json.loads(CODERELAY_CONFIG.read_text())
    if cfg.get("publicOrigin") != origin:
        cfg["publicOrigin"] = origin
        CODERELAY_CONFIG.write_text(json.dumps(cfg, indent=2) + "\n")
        changed = True

    with CODERELAY_PLIST.open("rb") as f:
        plist = plistlib.load(f)
    env = plist.setdefault("EnvironmentVariables", {})
    if env.get("CODERELAY_LOCAL_PUBLIC_ORIGIN") != origin:
        env["CODERELAY_LOCAL_PUBLIC_ORIGIN"] = origin
        with CODERELAY_PLIST.open("wb") as f:
            plistlib.dump(plist, f)
        changed = True

    return changed


def restart_coderelay() -> tuple[bool, str]:
    unload = run("launchctl", "unload", str(CODERELAY_PLIST))
    load = run("launchctl", "load", str(CODERELAY_PLIST))
    ok = load.returncode == 0
    detail = (unload.stdout + unload.stderr + load.stdout + load.stderr).strip()
    return ok, detail


def load_existing_state() -> dict:
    if not STATE_FILE.exists():
        return {}
    try:
        return json.loads(STATE_FILE.read_text())
    except Exception:
        return {}


def update_remote_state(status: dict, public_origin: str, serve_ok: bool, serve_detail: str) -> None:
    existing = load_existing_state()
    self_status = status.get("Self") or {}
    coderelay = existing.get("coderelay") or {}

    next_state = {
        "tailscale": {
            "backend_state": status.get("BackendState"),
            "dns_name": (self_status.get("DNSName") or "").rstrip("."),
            "tailscale_ips": self_status.get("TailscaleIPs") or [],
            "serve_status": "live" if serve_ok else "pending_or_failed",
            "serve_detail": serve_detail,
        },
        "coderelay": {
            "local_url": LOCAL_URL,
            "same_wifi_url": LAN_FALLBACK_URL or coderelay.get("same_wifi_url", ""),
            "tailnet_url": public_origin,
            "public_origin": public_origin,
        },
        "rustdesk": existing.get("rustdesk") or {},
    }
    STATE_FILE.write_text(json.dumps(next_state, indent=2) + "\n")


def main() -> int:
    try:
        status = load_status()
    except Exception as exc:
        print(json.dumps({"ok": False, "stage": "status", "error": str(exc)}))
        return 1

    backend_state = status.get("BackendState")
    if backend_state == "NeedsLogin":
        print(
            json.dumps(
                {
                    "ok": False,
                    "stage": "needs_login",
                    "auth_url": status.get("AuthURL", ""),
                }
            )
        )
        return 10

    up_ok = True
    up_detail = ""
    if backend_state != "Running":
        up_ok, up_detail = ensure_node_up()
        try:
            status = load_status()
        except Exception as exc:
            print(json.dumps({"ok": False, "stage": "post_up_status", "error": str(exc), "detail": up_detail}))
            return 2

    backend_state = status.get("BackendState")
    dns_name = ((status.get("Self") or {}).get("DNSName") or "").rstrip(".")
    if backend_state != "Running" or not dns_name:
        print(
            json.dumps(
                {
                    "ok": False,
                    "stage": "not_running",
                    "backend_state": backend_state,
                    "dns_name": dns_name,
                    "up_detail": up_detail,
                }
            )
        )
        return 3

    serve_ok, serve_detail = ensure_serve()
    public_origin = f"https://{dns_name}"
    changed = update_coderelay_public_origin(public_origin)
    restart_ok = True
    restart_detail = ""
    if changed:
        restart_ok, restart_detail = restart_coderelay()

    update_remote_state(status, public_origin, serve_ok, serve_detail)

    print(
        json.dumps(
            {
                "ok": up_ok and serve_ok and restart_ok,
                "backend_state": backend_state,
                "dns_name": dns_name,
                "public_origin": public_origin,
                "serve_ok": serve_ok,
                "serve_detail": serve_detail,
                "coderelay_updated": changed,
                "coderelay_restart_ok": restart_ok,
                "coderelay_restart_detail": restart_detail,
            }
        )
    )
    return 0 if (up_ok and serve_ok and restart_ok) else 4


if __name__ == "__main__":
    sys.exit(main())
