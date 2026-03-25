#!/usr/bin/env python3
"""Cron watchdog — detects wiped crons and restores from backup. Runs via launchd."""
import subprocess
from datetime import datetime
from pathlib import Path

PROJECT = Path(__file__).resolve().parent.parent
LOG = PROJECT / "AUTOMATIONS" / "logs" / "cron_watchdog.log"
BACKUP = PROJECT / "AUTOMATIONS" / "agent" / "cron_backup.txt"

REQUIRED = [
    "method_discovery_crawler", "sec_edgar_scanner", "crunchbase_scanner",
    "morning_intelligence_dag", "venture_pipeline", "auto_approve",
    "autonomous_integrator", "orphan_doc_scanner", "alpha_backlog_scanner",
]

def log(msg):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] [WATCHDOG] {msg}"
    print(line)
    LOG.parent.mkdir(parents=True, exist_ok=True)
    with open(LOG, "a") as f:
        f.write(line + "\n")

def check():
    r = subprocess.run(["crontab", "-l"], capture_output=True, text=True, timeout=5)
    current = r.stdout if r.returncode == 0 else ""
    missing = [c for c in REQUIRED if c not in current]
    if not missing:
        log(f"OK — all {len(REQUIRED)} crons present")
        BACKUP.parent.mkdir(parents=True, exist_ok=True)
        BACKUP.write_text(current)
        return
    log(f"ALERT: {len(missing)} crons missing: {missing}")
    if BACKUP.exists():
        backup = BACKUP.read_text()
        lines = [l for l in backup.splitlines() if any(c in l for c in missing)]
        if lines:
            new = current.rstrip() + "\n" + "\n".join(lines) + "\n"
            p = subprocess.run(["crontab", "-"], input=new, capture_output=True, text=True, timeout=10)
            log(f"Restored {len(lines)} crons" if p.returncode == 0 else f"Restore failed: {p.stderr[:100]}")

if __name__ == "__main__":
    check()
