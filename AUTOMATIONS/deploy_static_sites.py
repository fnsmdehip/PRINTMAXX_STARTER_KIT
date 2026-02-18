#!/usr/bin/env python3
"""
Deploy PRINTMAXX static build directories to Surge.

This is intentionally a *single-purpose* deployer used by Ship Captain as a
human-approved critical step.
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import List, Tuple


BASE_DIR = Path(__file__).resolve().parent.parent
OPS_DIR = BASE_DIR / "OPS"
STATIC_URLS_MD = OPS_DIR / "STATIC_DEPLOYMENT_URLS.md"


@dataclass(frozen=True)
class DeployItem:
    name: str
    project_dir: Path
    domain: str


ITEMS: Tuple[DeployItem, ...] = (
    DeployItem("PRINTMAXX SEO (programmatic)", BASE_DIR / "builds" / "programmatic_seo", "printmaxx-seo.surge.sh"),
    DeployItem("SiteScore (app)", BASE_DIR / "builds" / "site-scorer", "sitescore-app.surge.sh"),
    DeployItem("SiteScore Pro (analyzer)", BASE_DIR / "builds" / "seo-analyzer-web", "sitescore-analyzer.surge.sh"),
    DeployItem("PRINTMAXX Dashboard", BASE_DIR / "builds" / "master_dashboard", "printmaxx-dashboard.surge.sh"),
    DeployItem("Flowstack Demo", BASE_DIR / "builds" / "portfolio" / "landing-page", "flowstack-demo.surge.sh"),
    DeployItem("ShopMetrics Demo", BASE_DIR / "builds" / "portfolio" / "dashboard", "shopmetrics-dashboard.surge.sh"),
)


def _runner() -> List[str]:
    # Prefer installed surge CLI; fall back to npx for portability.
    if shutil.which("surge"):
        return ["surge"]
    return ["npx", "surge"]


def _deploy_one(item: DeployItem, *, timeout_sec: int, dry_run: bool) -> Tuple[bool, str]:
    if not item.project_dir.exists():
        return False, f"missing dir: {item.project_dir}"

    runner = _runner()
    cmd = runner + ["--project", str(item.project_dir), "--domain", item.domain]
    if dry_run:
        return True, "DRY_RUN: " + " ".join(cmd)

    try:
        proc = subprocess.run(
            cmd,
            cwd=BASE_DIR,
            capture_output=True,
            text=True,
            timeout=timeout_sec,
            check=False,
        )
    except subprocess.TimeoutExpired:
        return False, f"TIMEOUT after {timeout_sec}s"
    except Exception as e:
        return False, f"ERROR: {e}"

    out = (proc.stdout or "") + "\n" + (proc.stderr or "")
    out = out.strip()
    if proc.returncode != 0:
        return False, out[-1200:] if out else f"exit={proc.returncode}"
    return True, out[-1200:] if out else "ok"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--timeout-sec", type=int, default=420)
    args = ap.parse_args()

    ok_all = True
    results: List[Tuple[str, str, str]] = []  # (name, domain, status)
    for item in ITEMS:
        ok, msg = _deploy_one(item, timeout_sec=args.timeout_sec, dry_run=args.dry_run)
        status = "OK" if ok else "FAIL"
        print(f"[{status}] {item.name} -> https://{item.domain}")
        if msg:
            print(msg)
        print("")
        ok_all = ok_all and ok
        results.append((item.name, f"https://{item.domain}", "LIVE" if ok and not args.dry_run else ("DRY_RUN" if args.dry_run else "FAILED")))

    # Write a simple truth file for dashboards/launch packs (no secrets).
    OPS_DIR.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    lines = []
    lines.append("# PRINTMAXX Static Deployment URLs")
    lines.append("")
    lines.append(f"**Last updated:** {ts}")
    lines.append("")
    lines.append("| Site | URL | Status |")
    lines.append("|---|---|---|")
    for name, url, st in results:
        lines.append(f"| {name} | {url} | {st} |")
    lines.append("")
    STATIC_URLS_MD.write_text("\n".join(lines), encoding="utf-8")

    return 0 if ok_all else 1


if __name__ == "__main__":
    raise SystemExit(main())
