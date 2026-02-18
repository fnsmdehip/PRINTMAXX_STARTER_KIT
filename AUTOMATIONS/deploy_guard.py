#!/usr/bin/env python3
"""Deploy Guard (no-cost, non-interactive).

Goal: auto-deploy only when artifacts changed, without requiring manual CLI login.

This script is designed to be called from Ship Captain as a non-critical step.
It will:
  - compute fingerprints for PWA and static build artifacts
  - skip if unchanged
  - skip if no non-interactive deploy auth tokens exist
  - run deployers for changed sets:
      - PWAs: `python3 deploy_apps.py` (writes OPS/DEPLOYMENT_URLS.md)
      - Static: `python3 AUTOMATIONS/deploy_static_sites.py` (writes OPS/STATIC_DEPLOYMENT_URLS.md)
  - write a local report: output/deploy_guard/latest.{md,html} + manifest.json

Auth (non-interactive):
  - Vercel: VERCEL_TOKEN
  - Surge: SURGE_LOGIN + SURGE_TOKEN
  - Netlify: NETLIFY_AUTH_TOKEN
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple


BASE = Path(__file__).resolve().parent.parent

PWA_ROOT = BASE / "ralph" / "loops" / "app_factory" / "output"
STATIC_ROOTS = [
    BASE / "builds" / "programmatic_seo",
    BASE / "builds" / "site-scorer",
    BASE / "builds" / "seo-analyzer-web",
    BASE / "builds" / "master_dashboard",
    BASE / "builds" / "portfolio" / "landing-page",
    BASE / "builds" / "portfolio" / "dashboard",
]

STATE = BASE / "OPS" / "_state" / "deploy_guard_state.json"
OUT = BASE / "output" / "deploy_guard"
OUT_MD = OUT / "latest.md"
OUT_HTML = OUT / "latest.html"
OUT_MANIFEST = OUT / "manifest.json"


def now_iso() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def has_noninteractive_deploy_auth() -> bool:
    if (os.environ.get("VERCEL_TOKEN") or "").strip():
        return True
    if (os.environ.get("NETLIFY_AUTH_TOKEN") or "").strip():
        return True
    if (os.environ.get("SURGE_LOGIN") or "").strip() and (os.environ.get("SURGE_TOKEN") or "").strip():
        return True
    # Fallback: already-authenticated CLIs (non-interactive once logged in).
    checks = [
        "vercel whoami",
        "surge whoami",
        "netlify status",
    ]
    for cmd in checks:
        try:
            proc = subprocess.run(
                ["bash", "-lc", cmd],
                cwd=BASE,
                capture_output=True,
                text=True,
                timeout=12,
                check=False,
            )
            if proc.returncode == 0:
                return True
        except Exception:
            continue
    return False


def dir_summary(root: Path) -> Dict[str, object]:
    """Cheap signature for a directory tree."""
    if not root.exists():
        return {"exists": False, "count": 0, "sum_size": 0, "max_mtime": 0}
    count = 0
    sum_size = 0
    max_mtime = 0
    try:
        for p in root.rglob("*"):
            if not p.is_file():
                continue
            # Only count deploy-relevant artifacts.
            if p.suffix.lower() not in {".html", ".js", ".css", ".json", ".txt", ".xml"} and p.name not in {"robots.txt"}:
                continue
            st = p.stat()
            count += 1
            sum_size += int(st.st_size)
            mt = int(st.st_mtime)
            if mt > max_mtime:
                max_mtime = mt
    except Exception:
        pass
    return {"exists": True, "count": count, "sum_size": sum_size, "max_mtime": max_mtime}


def fingerprint(payload: Dict[str, object]) -> str:
    raw = json.dumps(payload, sort_keys=True, ensure_ascii=True).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def load_state() -> Dict[str, object]:
    if not STATE.exists():
        return {}
    try:
        return json.loads(STATE.read_text(encoding="utf-8"))
    except Exception:
        return {}


def save_state(state: Dict[str, object]) -> None:
    STATE.parent.mkdir(parents=True, exist_ok=True)
    STATE.write_text(json.dumps(state, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")


def run(cmd: str, *, timeout_sec: int) -> Tuple[int, str]:
    try:
        proc = subprocess.run(
            ["bash", "-lc", cmd],
            cwd=BASE,
            capture_output=True,
            text=True,
            timeout=timeout_sec,
            check=False,
        )
        out = (proc.stdout or "") + ("\n" + proc.stderr if proc.stderr else "")
        return int(proc.returncode), out.strip()
    except subprocess.TimeoutExpired:
        return 124, f"TIMEOUT after {timeout_sec}s"
    except Exception as e:
        return 1, str(e)


def write_report(lines: List[str], manifest: Dict[str, object]) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    md = "\n".join(lines).rstrip() + "\n"
    OUT_MD.write_text(md, encoding="utf-8")
    escaped = md.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    html = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>PRINTMAXX Deploy Guard</title>
  <style>
    body {{ margin: 0; background: #0b0b0b; color: #eaeaea; font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace; }}
    .wrap {{ max-width: 1100px; margin: 0 auto; padding: 18px; }}
    pre {{ white-space: pre-wrap; line-height: 1.5; font-size: 13px; }}
  </style>
</head>
<body>
  <div class="wrap"><pre>{escaped}</pre></div>
</body>
</html>
"""
    OUT_HTML.write_text(html, encoding="utf-8")
    OUT_MANIFEST.write_text(json.dumps(manifest, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--tick", action="store_true")
    ap.add_argument("--force", action="store_true")
    args = ap.parse_args()
    if not args.tick:
        ap.print_help()
        return 2

    prev = load_state()
    pwa_sig = dir_summary(PWA_ROOT)
    static_sig = {str(p): dir_summary(p) for p in STATIC_ROOTS}

    pwa_fp = fingerprint({"pwa": pwa_sig})
    static_fp = fingerprint({"static": static_sig})

    prev_pwa = str(prev.get("pwa_fp") or "")
    prev_static = str(prev.get("static_fp") or "")
    pwa_changed = args.force or (pwa_fp != prev_pwa)
    static_changed = args.force or (static_fp != prev_static)

    lines: List[str] = []
    lines.append("# Deploy Guard")
    lines.append("")
    lines.append(f"Generated: {now_iso()}")
    lines.append("")
    lines.append(f"- PWA changed: {pwa_changed}")
    lines.append(f"- Static changed: {static_changed}")
    lines.append("")

    manifest: Dict[str, object] = {
        "generated_at": now_iso(),
        "pwa_changed": bool(pwa_changed),
        "static_changed": bool(static_changed),
        "pwa_fp": pwa_fp,
        "static_fp": static_fp,
        "pwa_root": str(PWA_ROOT),
        "static_roots": [str(p) for p in STATIC_ROOTS],
        "results": [],
    }

    if not (pwa_changed or static_changed):
        lines.append("Result: SKIPPED (unchanged)")
        save_state(
            {
                **(prev if isinstance(prev, dict) else {}),
                "updated_at": now_iso(),
                "pwa_fp": pwa_fp,
                "static_fp": static_fp,
                "last_action": "SKIPPED_UNCHANGED",
            }
        )
        write_report(lines, manifest)
        print("deploy_guard: SKIPPED unchanged")
        return 0

    if not has_noninteractive_deploy_auth():
        lines.append("Result: SKIPPED (missing deploy tokens)")
        lines.append("")
        lines.append("Missing non-interactive auth. Set one of:")
        lines.append("- VERCEL_TOKEN")
        lines.append("- NETLIFY_AUTH_TOKEN")
        lines.append("- SURGE_LOGIN + SURGE_TOKEN")
        save_state(
            {
                **(prev if isinstance(prev, dict) else {}),
                "updated_at": now_iso(),
                "pwa_fp": prev_pwa or "",
                "static_fp": prev_static or "",
                "last_action": "SKIPPED_NO_AUTH",
            }
        )
        write_report(lines, manifest)
        print("deploy_guard: SKIPPED missing deploy tokens")
        return 0

    # Deploy changed sets.
    any_fail = False
    if pwa_changed:
        code, out = run("python3 deploy_apps.py", timeout_sec=1800)
        ok = code == 0
        any_fail = any_fail or (not ok)
        manifest["results"].append({"target": "pwa", "ok": ok, "exit_code": code, "tail": out[-1200:]})
        lines.append("## PWA Deploy")
        lines.append("")
        lines.append(f"- exit_code: {code}")
        lines.append(f"- ok: {ok}")
        if out:
            lines.append("")
            lines.append("```")
            lines.append(out[-1200:])
            lines.append("```")
        lines.append("")

    if static_changed:
        code, out = run("python3 AUTOMATIONS/deploy_static_sites.py", timeout_sec=1800)
        ok = code == 0
        any_fail = any_fail or (not ok)
        manifest["results"].append({"target": "static", "ok": ok, "exit_code": code, "tail": out[-1200:]})
        lines.append("## Static Deploy")
        lines.append("")
        lines.append(f"- exit_code: {code}")
        lines.append(f"- ok: {ok}")
        if out:
            lines.append("")
            lines.append("```")
            lines.append(out[-1200:])
            lines.append("```")
        lines.append("")

    # Only advance fingerprints when deploy succeeded for that target.
    new_state = dict(prev) if isinstance(prev, dict) else {}
    new_state["updated_at"] = now_iso()
    if pwa_changed and not any_fail:
        new_state["pwa_fp"] = pwa_fp
    else:
        new_state["pwa_fp"] = prev_pwa
    if static_changed and not any_fail:
        new_state["static_fp"] = static_fp
    else:
        new_state["static_fp"] = prev_static
    new_state["last_action"] = "DEPLOY" if not any_fail else "DEPLOY_FAILED"
    save_state(new_state)

    write_report(lines, manifest)
    print("deploy_guard: OK" if not any_fail else "deploy_guard: FAIL")
    return 0 if not any_fail else 1


if __name__ == "__main__":
    raise SystemExit(main())
