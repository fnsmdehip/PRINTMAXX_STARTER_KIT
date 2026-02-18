#!/usr/bin/env python3
"""PRINTMAXX Runtime Stack Governor.

Budget-first model routing + runtime availability checks.
Designed to run continuously from Ship Captain.
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple


BASE_DIR = Path(__file__).resolve().parent.parent
OPS_DIR = BASE_DIR / "OPS"
LEDGER_DIR = BASE_DIR / "LEDGER"
SECRETS_FILE = BASE_DIR / "SECRETS" / "PAYMENT_INFO.md"

POLICY_JSON = OPS_DIR / "STACK_POLICY.json"
NODE_ROLE_JSON = OPS_DIR / "NODE_ROLE.json"
HEARTBEAT_MD = OPS_DIR / "STACK_HEARTBEAT.md"
LEDGER_CSV = LEDGER_DIR / "STACK_HEALTH.csv"


def now_iso() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def _default_policy() -> Dict[str, object]:
    return {
        "version": "unknown",
        "budget": {
            "monthly_cap_usd": 200,
            "soft_cap_usd": 150,
            "hard_pause_cap_usd": 190,
            "daily_target_usd": 6.5,
            "premium_token_share_max_percent": 15,
        },
        "model_defaults": {
            "local_preferred": ["qwen2.5:7b", "llama3.1:8b", "phi4"],
            "openrouter_cheap": "moonshotai/kimi-k2-0905",
            "openai_mini": "gpt-5-mini",
            "anthropic_fast": "claude-sonnet-4-5",
            "premium_code": "gpt-5.2",
        },
        "task_routes": {
            "low_risk_bulk": ["local", "openrouter_cheap", "openai_mini"],
            "medium_risk_content": ["openrouter_cheap", "openai_mini", "anthropic_fast", "local"],
            "high_risk_reasoning": ["anthropic_fast", "premium_code", "openai_mini", "local"],
            "code_generation": ["premium_code", "anthropic_fast", "openai_mini", "local"],
        },
    }


def load_policy() -> Dict[str, object]:
    policy = _default_policy()
    if not POLICY_JSON.exists():
        return policy
    try:
        with open(POLICY_JSON, "r", encoding="utf-8") as f:
            loaded = json.load(f)
        if isinstance(loaded, dict):
            for key in ("version", "budget", "model_defaults", "task_routes", "risk", "objective"):
                if key in loaded:
                    policy[key] = loaded[key]
    except Exception:
        pass
    return policy


def load_node_role() -> str:
    default_role = "control"
    if not NODE_ROLE_JSON.exists():
        return default_role
    try:
        payload = json.loads(NODE_ROLE_JSON.read_text(encoding="utf-8"))
    except Exception:
        return default_role
    role = str(payload.get("role", default_role)).strip().lower()
    if role in {"control", "worker"}:
        return role
    return default_role


def load_secret_keys() -> Dict[str, str]:
    keys: Dict[str, str] = {}
    if not SECRETS_FILE.exists():
        return keys
    try:
        for line in SECRETS_FILE.read_text(encoding="utf-8").splitlines():
            s = line.strip()
            if not s or s.startswith("#") or "=" not in s:
                continue
            k, v = s.split("=", 1)
            k = k.strip()
            v = v.strip()
            if k and v:
                keys[k] = v
    except Exception:
        return keys
    return keys


def _run(cmd: str, timeout_sec: int = 8) -> Tuple[int, str, str]:
    try:
        proc = subprocess.run(
            ["bash", "-lc", cmd],
            cwd=BASE_DIR,
            capture_output=True,
            text=True,
            timeout=timeout_sec,
            check=False,
        )
        return proc.returncode, (proc.stdout or "").strip(), (proc.stderr or "").strip()
    except Exception as exc:
        return 1, "", str(exc)


def detect_ollama(local_preferred: List[str]) -> Dict[str, object]:
    installed = _run("command -v ollama >/dev/null && echo yes || echo no", 3)[1].strip() == "yes"
    result: Dict[str, object] = {"installed": installed, "daemon_ready": False, "models": []}
    if not installed:
        return result

    rc, out, _err = _run("ollama list", 8)
    if rc != 0:
        return result

    models: List[str] = []
    for line in out.splitlines():
        s = line.strip()
        if not s or s.upper().startswith("NAME"):
            continue
        # NAME column is first token
        name = s.split()[0].strip()
        if name:
            models.append(name)
    result["daemon_ready"] = True
    result["models"] = models

    # Preserve preferred order when possible
    preferred = [m for m in local_preferred if m in models]
    if preferred:
        ordered = preferred + [m for m in models if m not in preferred]
        result["models"] = ordered
    return result


def provider_readiness(secret_keys: Dict[str, str]) -> Dict[str, bool]:
    def has_key(env_key: str, secret_key: str) -> bool:
        return bool(os.environ.get(env_key)) or bool(secret_keys.get(secret_key))

    return {
        "openrouter": has_key("OPENROUTER_API_KEY", "OPENROUTER_API_KEY"),
        "anthropic": has_key("ANTHROPIC_API_KEY", "ANTHROPIC_API_KEY"),
        "openai": has_key("OPENAI_API_KEY", "OPENAI_API_KEY"),
    }


def choose_model(task_class: str, policy: Dict[str, object], providers: Dict[str, bool], ollama: Dict[str, object]) -> Dict[str, str]:
    routes = policy.get("task_routes", {})
    defaults = policy.get("model_defaults", {})
    route_chain = routes.get(task_class, ["openai_mini"])

    for route in route_chain:
        if route == "local":
            models = ollama.get("models", [])
            if ollama.get("daemon_ready") and models:
                return {"route": "local", "provider": "ollama", "model": str(models[0])}
        elif route == "openrouter_cheap":
            if providers.get("openrouter"):
                return {"route": "openrouter_cheap", "provider": "openrouter", "model": str(defaults.get("openrouter_cheap", "moonshotai/kimi-k2-0905"))}
        elif route == "openai_mini":
            if providers.get("openai"):
                return {"route": "openai_mini", "provider": "openai", "model": str(defaults.get("openai_mini", "gpt-5-mini"))}
        elif route == "anthropic_fast":
            if providers.get("anthropic"):
                return {"route": "anthropic_fast", "provider": "anthropic", "model": str(defaults.get("anthropic_fast", "claude-sonnet-4-5"))}
        elif route == "premium_code":
            if providers.get("openai"):
                return {"route": "premium_code", "provider": "openai", "model": str(defaults.get("premium_code", "gpt-5.2"))}
            if providers.get("anthropic"):
                return {"route": "premium_code_fallback", "provider": "anthropic", "model": str(defaults.get("anthropic_fast", "claude-sonnet-4-5"))}

    return {"route": "unavailable", "provider": "none", "model": "none"}


def ensure_ledger_csv() -> None:
    LEDGER_DIR.mkdir(parents=True, exist_ok=True)
    if LEDGER_CSV.exists():
        return
    with open(LEDGER_CSV, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(
            [
                "timestamp",
                "policy_version",
                "local_ready",
                "local_models",
                "openrouter_ready",
                "anthropic_ready",
                "openai_ready",
                "low_risk_route",
                "high_risk_route",
                "notes",
            ]
        )


def append_ledger(policy: Dict[str, object], providers: Dict[str, bool], ollama: Dict[str, object], low: Dict[str, str], high: Dict[str, str]) -> None:
    ensure_ledger_csv()
    with open(LEDGER_CSV, "a", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(
            [
                now_iso(),
                policy.get("version", "unknown"),
                "yes" if ollama.get("daemon_ready") else "no",
                "|".join(ollama.get("models", [])[:5]),
                "yes" if providers.get("openrouter") else "no",
                "yes" if providers.get("anthropic") else "no",
                "yes" if providers.get("openai") else "no",
                f"{low.get('provider')}:{low.get('model')}",
                f"{high.get('provider')}:{high.get('model')}",
                f"budget-first routing active node_role={load_node_role()}",
            ]
        )


def write_heartbeat(policy: Dict[str, object], providers: Dict[str, bool], ollama: Dict[str, object], decisions: Dict[str, Dict[str, str]]) -> None:
    OPS_DIR.mkdir(parents=True, exist_ok=True)
    budget = policy.get("budget", {})
    lines = [
        "# Runtime Stack Heartbeat",
        "",
        f"Generated: {now_iso()}",
        "",
        f"Node role: `{load_node_role()}`",
        "",
        f"Policy version: {policy.get('version', 'unknown')}",
        "",
        "## Budget Guard",
        "",
        f"- Monthly cap: ${budget.get('monthly_cap_usd', 200)}",
        f"- Soft cap: ${budget.get('soft_cap_usd', 150)}",
        f"- Hard pause cap: ${budget.get('hard_pause_cap_usd', 190)}",
        f"- Daily target: ${budget.get('daily_target_usd', 6.5)}",
        f"- Premium share max: {budget.get('premium_token_share_max_percent', 15)}%",
        "",
        "## Provider Readiness",
        "",
        f"- Ollama installed: {'yes' if ollama.get('installed') else 'no'}",
        f"- Ollama daemon ready: {'yes' if ollama.get('daemon_ready') else 'no'}",
        f"- Local models: {', '.join(ollama.get('models', [])[:8]) or 'none'}",
        f"- OpenRouter key ready: {'yes' if providers.get('openrouter') else 'no'}",
        f"- Anthropic key ready: {'yes' if providers.get('anthropic') else 'no'}",
        f"- OpenAI key ready: {'yes' if providers.get('openai') else 'no'}",
        "",
        "## Active Routes",
        "",
    ]
    for task_class, decision in decisions.items():
        lines.append(
            f"- {task_class}: {decision.get('provider')} / {decision.get('model')} ({decision.get('route')})"
        )

    with open(HEARTBEAT_MD, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")


def do_heartbeat(as_json: bool = False) -> int:
    policy = load_policy()
    defaults = policy.get("model_defaults", {})
    local_pref = defaults.get("local_preferred", ["qwen2.5:7b"])
    if not isinstance(local_pref, list):
        local_pref = ["qwen2.5:7b"]

    secret_keys = load_secret_keys()
    providers = provider_readiness(secret_keys)
    ollama = detect_ollama([str(x) for x in local_pref])

    decisions: Dict[str, Dict[str, str]] = {}
    task_routes = policy.get("task_routes", {})
    if isinstance(task_routes, dict):
        for task_class in task_routes:
            decisions[str(task_class)] = choose_model(str(task_class), policy, providers, ollama)

    if "low_risk_bulk" not in decisions:
        decisions["low_risk_bulk"] = choose_model("low_risk_bulk", policy, providers, ollama)
    if "high_risk_reasoning" not in decisions:
        decisions["high_risk_reasoning"] = choose_model("high_risk_reasoning", policy, providers, ollama)

    write_heartbeat(policy, providers, ollama, decisions)
    append_ledger(
        policy,
        providers,
        ollama,
        decisions.get("low_risk_bulk", {"provider": "none", "model": "none"}),
        decisions.get("high_risk_reasoning", {"provider": "none", "model": "none"}),
    )

    payload = {
        "timestamp": now_iso(),
        "node_role": load_node_role(),
        "policy_version": policy.get("version", "unknown"),
        "providers": providers,
        "ollama": ollama,
        "decisions": decisions,
    }
    if as_json:
        print(json.dumps(payload, indent=2))
    else:
        print(
            f"[STACK] low_risk={decisions.get('low_risk_bulk', {}).get('provider')}:{decisions.get('low_risk_bulk', {}).get('model')} "
            f"high_risk={decisions.get('high_risk_reasoning', {}).get('provider')}:{decisions.get('high_risk_reasoning', {}).get('model')}"
        )
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="PRINTMAXX runtime stack governor")
    parser.add_argument("--heartbeat", action="store_true", help="Write runtime heartbeat and ledger row (default)")
    parser.add_argument("--select-model", help="Return selected model for a task class")
    parser.add_argument("--json", action="store_true", help="Emit JSON")
    args = parser.parse_args()

    policy = load_policy()
    defaults = policy.get("model_defaults", {})
    local_pref = defaults.get("local_preferred", ["qwen2.5:7b"])
    if not isinstance(local_pref, list):
        local_pref = ["qwen2.5:7b"]

    secret_keys = load_secret_keys()
    providers = provider_readiness(secret_keys)
    ollama = detect_ollama([str(x) for x in local_pref])

    if args.select_model:
        decision = choose_model(args.select_model.strip(), policy, providers, ollama)
        if args.json:
            print(json.dumps(decision, indent=2))
        else:
            print(f"{decision.get('provider')}:{decision.get('model')}")
        return 0

    return do_heartbeat(as_json=args.json)


if __name__ == "__main__":
    raise SystemExit(main())
