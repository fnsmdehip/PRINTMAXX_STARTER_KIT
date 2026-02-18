#!/usr/bin/env python3
"""OpenRouter runtime key budget guard.

Purpose:
- Enforce hard daily limits on automation API keys so a monthly budget
  cannot be burned in a single day.
- Keep key policy declarative in OPS/OPENROUTER_BUDGET_POLICY.json.

This script never edits account-level billing; it only manages API keys.
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import urllib.error
import urllib.request
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Tuple


BASE_DIR = Path(__file__).resolve().parent.parent
OPS_DIR = BASE_DIR / "OPS"
LEDGER_DIR = BASE_DIR / "LEDGER"
OUT_DIR = BASE_DIR / "output" / "openrouter_budget_guard"
SECRETS_FILE = BASE_DIR / "SECRETS" / "PAYMENT_INFO.md"

POLICY_JSON = OPS_DIR / "OPENROUTER_BUDGET_POLICY.json"
RUNS_CSV = LEDGER_DIR / "OPENROUTER_BUDGET_GUARD.csv"
LATEST_JSON = OUT_DIR / "latest.json"
LATEST_MD = OUT_DIR / "latest.md"


def now_iso() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def _safe_float(v: object, default: float = 0.0) -> float:
    try:
        return float(str(v).strip())
    except Exception:
        return default


def _safe_bool(v: object, default: bool = False) -> bool:
    if isinstance(v, bool):
        return v
    if v is None:
        return default
    s = str(v).strip().lower()
    if s in {"1", "true", "yes", "y", "on"}:
        return True
    if s in {"0", "false", "no", "n", "off"}:
        return False
    return default


def load_policy() -> Dict[str, Any]:
    default = {
        "version": "2026-02-18",
        "base_url": "https://openrouter.ai/api/v1",
        "admin_key_env": "OPENROUTER_ADMIN_API_KEY",
        "monthly_budget_usd": 100.0,
        "daily_divisor_days": 30,
        "keys": [
            {
                "name": "printmaxx-worker-runtime",
                "label": "PRINTMAXX Worker Runtime",
                "create_if_missing": True,
                "limit_mode": "daily_from_monthly",
                "budget_share": 1.0,
                "limit_reset": "daily",
                "disabled": False,
                "tags": ["worker", "openclaw", "ship-captain"],
            }
        ],
    }
    if not POLICY_JSON.exists():
        return default
    try:
        payload = json.loads(POLICY_JSON.read_text(encoding="utf-8"))
    except Exception:
        return default
    if not isinstance(payload, dict):
        return default
    for key in ("version", "base_url", "admin_key_env", "monthly_budget_usd", "daily_divisor_days", "keys"):
        if key in payload:
            default[key] = payload[key]
    return default


def load_secret_map() -> Dict[str, str]:
    out: Dict[str, str] = {}
    if not SECRETS_FILE.exists():
        return out
    try:
        for line in SECRETS_FILE.read_text(encoding="utf-8").splitlines():
            s = line.strip()
            if not s or s.startswith("#") or "=" not in s:
                continue
            k, v = s.split("=", 1)
            k = k.strip()
            v = v.strip()
            if k and v:
                out[k] = v
    except Exception:
        return out
    return out


def resolve_admin_key(policy: Dict[str, Any]) -> str:
    env_name = str(policy.get("admin_key_env", "OPENROUTER_ADMIN_API_KEY")).strip() or "OPENROUTER_ADMIN_API_KEY"
    candidates = [
        env_name,
        "OPENROUTER_ADMIN_API_KEY",
        "OPENROUTER_API_KEY_ADMIN",
        "OPENROUTER_API_KEY",
    ]

    for name in candidates:
        v = (os.environ.get(name) or "").strip()
        if v:
            return v

    secrets = load_secret_map()
    for name in candidates:
        v = (secrets.get(name) or "").strip()
        if v:
            return v

    return ""


def _http_json(
    method: str,
    url: str,
    api_key: str,
    payload: Dict[str, Any] | None = None,
    timeout_sec: int = 20,
) -> Tuple[int, Dict[str, Any], str]:
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Accept": "application/json",
    }
    data: bytes | None = None
    if payload is not None:
        headers["Content-Type"] = "application/json"
        data = json.dumps(payload).encode("utf-8")

    req = urllib.request.Request(url=url, method=method.upper(), headers=headers, data=data)
    try:
        with urllib.request.urlopen(req, timeout=timeout_sec) as resp:
            raw = resp.read().decode("utf-8", errors="replace")
            body: Dict[str, Any] = {}
            if raw:
                try:
                    parsed = json.loads(raw)
                    if isinstance(parsed, dict):
                        body = parsed
                    else:
                        body = {"data": parsed}
                except Exception:
                    body = {"raw": raw}
            return int(resp.status), body, ""
    except urllib.error.HTTPError as exc:
        raw = exc.read().decode("utf-8", errors="replace") if exc.fp else ""
        body: Dict[str, Any] = {}
        if raw:
            try:
                parsed = json.loads(raw)
                if isinstance(parsed, dict):
                    body = parsed
                else:
                    body = {"data": parsed}
            except Exception:
                body = {"raw": raw}
        msg = str(body.get("error") or body.get("message") or raw or str(exc))
        return int(exc.code), body, msg
    except Exception as exc:
        return 0, {}, str(exc)


def _extract_key_list(body: Dict[str, Any]) -> List[Dict[str, Any]]:
    candidates: List[Any] = []
    if isinstance(body.get("data"), list):
        candidates = body.get("data", [])
    elif isinstance(body.get("keys"), list):
        candidates = body.get("keys", [])
    elif isinstance(body.get("data"), dict) and isinstance(body.get("data", {}).get("keys"), list):
        candidates = body.get("data", {}).get("keys", [])
    else:
        candidates = []

    out: List[Dict[str, Any]] = []
    for item in candidates:
        if isinstance(item, dict):
            out.append(item)
    return out


def desired_limit_usd(policy: Dict[str, Any], key_cfg: Dict[str, Any]) -> float:
    explicit = key_cfg.get("limit_usd")
    if explicit is not None:
        return max(0.0, round(_safe_float(explicit, 0.0), 2))

    mode = str(key_cfg.get("limit_mode", "daily_from_monthly")).strip().lower()
    if mode != "daily_from_monthly":
        return 0.0

    monthly = max(0.0, _safe_float(policy.get("monthly_budget_usd"), 100.0))
    divisor = max(1.0, _safe_float(policy.get("daily_divisor_days"), 30.0))
    share = max(0.0, _safe_float(key_cfg.get("budget_share"), 1.0))
    return round((monthly * share) / divisor, 2)


def _normalize_reset(raw: object) -> str:
    s = str(raw or "").strip().lower()
    if s in {"daily", "monthly"}:
        return s
    return "daily"


def _mask(v: str) -> str:
    s = v.strip()
    if len(s) <= 8:
        return "***"
    return f"{s[:4]}...{s[-4:]}"


def ensure_csv() -> None:
    LEDGER_DIR.mkdir(parents=True, exist_ok=True)
    if RUNS_CSV.exists():
        return
    with open(RUNS_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(
            [
                "timestamp",
                "mode",
                "success",
                "keys_checked",
                "keys_changed",
                "created",
                "updated",
                "notes",
            ]
        )


def append_csv(mode: str, success: bool, checked: int, changed: int, created: int, updated: int, notes: str) -> None:
    ensure_csv()
    with open(RUNS_CSV, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(
            [
                now_iso(),
                mode,
                "yes" if success else "no",
                checked,
                changed,
                created,
                updated,
                notes,
            ]
        )


def write_outputs(payload: Dict[str, Any]) -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    LATEST_JSON.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    lines: List[str] = []
    lines.append("# OpenRouter Budget Guard")
    lines.append("")
    lines.append(f"Generated: {payload.get('generated_at', '')}")
    lines.append(f"Mode: `{payload.get('mode', '')}`")
    lines.append(f"Success: `{payload.get('success', False)}`")
    lines.append("")
    lines.append("## Summary")
    lines.append("")
    lines.append(f"- Keys checked: {payload.get('keys_checked', 0)}")
    lines.append(f"- Keys changed: {payload.get('keys_changed', 0)}")
    lines.append(f"- Created: {payload.get('created_count', 0)}")
    lines.append(f"- Updated: {payload.get('updated_count', 0)}")
    lines.append("")
    lines.append("## Keys")
    lines.append("")
    lines.append("| name | hash | limit | reset | disabled | action |")
    lines.append("|---|---|---:|---|---|---|")
    for row in payload.get("rows", []):
        if not isinstance(row, dict):
            continue
        lines.append(
            "| {name} | `{hash}` | ${limit:.2f} | {reset} | {disabled} | {action} |".format(
                name=str(row.get("name", "")),
                hash=str(row.get("hash", "") or "n/a"),
                limit=_safe_float(row.get("desired_limit_usd"), 0.0),
                reset=str(row.get("desired_limit_reset", "daily")),
                disabled="yes" if _safe_bool(row.get("desired_disabled"), False) else "no",
                action=str(row.get("action", "none")),
            )
        )

    if payload.get("created_keys"):
        lines.append("")
        lines.append("## Newly Created Keys")
        lines.append("")
        lines.append("Raw key strings are only shown in CLI output for immediate copy.")
        for item in payload.get("created_keys", []):
            if not isinstance(item, dict):
                continue
            lines.append(f"- `{item.get('name', 'unknown')}` -> {item.get('masked_key', '***')}")

    notes = str(payload.get("notes", "")).strip()
    if notes:
        lines.append("")
        lines.append("## Notes")
        lines.append("")
        lines.append(f"- {notes}")

    lines.append("")
    LATEST_MD.write_text("\n".join(lines), encoding="utf-8")


def enforce(policy: Dict[str, Any], dry_run: bool, quiet: bool) -> Tuple[bool, Dict[str, Any]]:
    api_key = resolve_admin_key(policy)
    created_raw_keys: List[Tuple[str, str]] = []
    payload: Dict[str, Any] = {
        "generated_at": now_iso(),
        "mode": "enforce_dry_run" if dry_run else "enforce",
        "success": False,
        "keys_checked": 0,
        "keys_changed": 0,
        "created_count": 0,
        "updated_count": 0,
        "rows": [],
        "created_keys": [],
        "notes": "",
    }

    if not api_key:
        payload["success"] = True
        payload["notes"] = "Skipped: missing admin API key. Set OPENROUTER_ADMIN_API_KEY (or policy admin_key_env)."
        write_outputs(payload)
        append_csv(payload["mode"], True, 0, 0, 0, 0, str(payload["notes"]))
        if not quiet:
            print(f"openrouter_budget_guard: {payload['notes']}")
        return True, payload

    base_url = str(policy.get("base_url", "https://openrouter.ai/api/v1")).rstrip("/")
    list_status, list_body, list_err = _http_json("GET", f"{base_url}/keys", api_key)
    if list_status < 200 or list_status >= 300:
        payload["notes"] = f"Failed to list keys: status={list_status} err={list_err}"
        write_outputs(payload)
        append_csv(payload["mode"], False, 0, 0, 0, 0, str(payload["notes"]))
        if not quiet:
            print(f"openrouter_budget_guard: {payload['notes']}")
        return False, payload

    existing = _extract_key_list(list_body)
    by_name: Dict[str, Dict[str, Any]] = {}
    for key in existing:
        name = str(key.get("name", "")).strip()
        if name:
            by_name[name] = key

    key_cfgs = policy.get("keys", [])
    if not isinstance(key_cfgs, list):
        key_cfgs = []

    checked = 0
    changed = 0
    created_count = 0
    updated_count = 0

    for cfg in key_cfgs:
        if not isinstance(cfg, dict):
            continue

        name = str(cfg.get("name", "")).strip()
        if not name:
            continue

        checked += 1
        desired_limit = desired_limit_usd(policy, cfg)
        desired_reset = _normalize_reset(cfg.get("limit_reset", "daily"))
        desired_disabled = _safe_bool(cfg.get("disabled"), False)
        desired_label = str(cfg.get("label", "")).strip()
        create_if_missing = _safe_bool(cfg.get("create_if_missing"), True)

        row: Dict[str, Any] = {
            "name": name,
            "hash": "",
            "desired_limit_usd": desired_limit,
            "desired_limit_reset": desired_reset,
            "desired_disabled": desired_disabled,
            "action": "none",
            "details": "",
        }

        current = by_name.get(name)
        if current is None:
            if not create_if_missing:
                row["action"] = "skipped_missing"
                row["details"] = "create_if_missing=false"
                payload["rows"].append(row)
                continue

            create_body: Dict[str, Any] = {
                "name": name,
                "limit": desired_limit,
                "limit_reset": desired_reset,
            }
            if desired_label:
                create_body["label"] = desired_label
            if desired_disabled:
                create_body["disabled"] = True

            if dry_run:
                row["action"] = "would_create"
                row["details"] = "dry_run"
                changed += 1
                created_count += 1
                payload["rows"].append(row)
                continue

            status, body, err = _http_json("POST", f"{base_url}/keys", api_key, payload=create_body)
            if status >= 200 and status < 300:
                key_info = body.get("data") if isinstance(body.get("data"), dict) else body
                if not isinstance(key_info, dict):
                    key_info = {}
                row["action"] = "created"
                row["hash"] = str(key_info.get("hash", ""))
                row["details"] = "ok"
                changed += 1
                created_count += 1

                raw_key = str(key_info.get("key", "")).strip()
                if raw_key:
                    created_raw_keys.append((name, raw_key))
                    payload["created_keys"].append(
                        {
                            "name": name,
                            "masked_key": _mask(raw_key),
                        }
                    )
            else:
                row["action"] = "create_failed"
                row["details"] = f"status={status} err={err}"
            payload["rows"].append(row)
            continue

        # Existing key -> patch if drift.
        cur_hash = str(current.get("hash", "")).strip()
        cur_limit = _safe_float(current.get("limit"), -1.0)
        cur_reset = _normalize_reset(current.get("limit_reset"))
        cur_disabled = _safe_bool(current.get("disabled"), False)
        cur_label = str(current.get("label", "")).strip()

        row["hash"] = cur_hash

        patch_body: Dict[str, Any] = {}
        if round(cur_limit, 2) != round(desired_limit, 2):
            patch_body["limit"] = desired_limit
        if cur_reset != desired_reset:
            patch_body["limit_reset"] = desired_reset
        if cur_disabled != desired_disabled:
            patch_body["disabled"] = desired_disabled
        if desired_label and cur_label != desired_label:
            patch_body["label"] = desired_label

        if not patch_body:
            row["action"] = "no_change"
            row["details"] = "already_compliant"
            payload["rows"].append(row)
            continue

        if not cur_hash:
            row["action"] = "update_failed"
            row["details"] = "missing_hash"
            payload["rows"].append(row)
            continue

        if dry_run:
            row["action"] = "would_update"
            row["details"] = json.dumps(patch_body, sort_keys=True)
            changed += 1
            updated_count += 1
            payload["rows"].append(row)
            continue

        status, _body, err = _http_json("PATCH", f"{base_url}/keys/{cur_hash}", api_key, payload=patch_body)
        if status >= 200 and status < 300:
            row["action"] = "updated"
            row["details"] = "ok"
            changed += 1
            updated_count += 1
        else:
            row["action"] = "update_failed"
            row["details"] = f"status={status} err={err}"

        payload["rows"].append(row)

    payload["keys_checked"] = checked
    payload["keys_changed"] = changed
    payload["created_count"] = created_count
    payload["updated_count"] = updated_count
    payload["success"] = True
    payload["notes"] = f"policy_version={policy.get('version', 'unknown')}"

    write_outputs(payload)
    append_csv(
        payload["mode"],
        True,
        checked,
        changed,
        created_count,
        updated_count,
        str(payload["notes"]),
    )

    if not quiet:
        print(
            "openrouter_budget_guard: "
            f"checked={checked} changed={changed} created={created_count} updated={updated_count}"
        )
        for name, raw_key in created_raw_keys:
            # Print once so operator can copy to worker secrets.
            print(f"new_key name={name} key={raw_key}")

    return True, payload


def status(policy: Dict[str, Any], quiet: bool) -> Tuple[bool, Dict[str, Any]]:
    api_key = resolve_admin_key(policy)
    payload: Dict[str, Any] = {
        "generated_at": now_iso(),
        "mode": "status",
        "success": False,
        "rows": [],
        "notes": "",
    }

    if not api_key:
        payload["notes"] = "Missing admin API key. Set OPENROUTER_ADMIN_API_KEY (or policy admin_key_env)."
        write_outputs(payload)
        if not quiet:
            print(f"openrouter_budget_guard: {payload['notes']}")
        return False, payload

    base_url = str(policy.get("base_url", "https://openrouter.ai/api/v1")).rstrip("/")
    list_status, list_body, list_err = _http_json("GET", f"{base_url}/keys", api_key)
    if list_status < 200 or list_status >= 300:
        payload["notes"] = f"Failed to list keys: status={list_status} err={list_err}"
        write_outputs(payload)
        if not quiet:
            print(f"openrouter_budget_guard: {payload['notes']}")
        return False, payload

    rows: List[Dict[str, Any]] = []
    for key in _extract_key_list(list_body):
        rows.append(
            {
                "name": str(key.get("name", "")),
                "label": str(key.get("label", "")),
                "hash": str(key.get("hash", "")),
                "limit": _safe_float(key.get("limit"), 0.0),
                "limit_reset": _normalize_reset(key.get("limit_reset")),
                "disabled": _safe_bool(key.get("disabled"), False),
            }
        )

    payload["rows"] = sorted(rows, key=lambda x: str(x.get("name", "")))
    payload["success"] = True
    payload["notes"] = f"keys={len(rows)}"
    write_outputs(payload)

    if not quiet:
        print(f"openrouter_budget_guard: keys={len(rows)}")
    return True, payload


def parse_args() -> argparse.Namespace:
    ap = argparse.ArgumentParser(description="OpenRouter key budget guard")
    mode = ap.add_mutually_exclusive_group(required=False)
    mode.add_argument("--enforce", action="store_true", help="Enforce policy on API keys")
    mode.add_argument("--status", action="store_true", help="Read-only key status")
    ap.add_argument("--dry-run", action="store_true", help="Show what would change without API writes")
    ap.add_argument("--quiet", action="store_true", help="Minimal stdout")
    return ap.parse_args()


def main() -> int:
    args = parse_args()
    policy = load_policy()

    if args.status:
        ok, _ = status(policy=policy, quiet=bool(args.quiet))
        return 0 if ok else 1

    # Default mode is enforce.
    ok, _ = enforce(policy=policy, dry_run=bool(args.dry_run), quiet=bool(args.quiet))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
