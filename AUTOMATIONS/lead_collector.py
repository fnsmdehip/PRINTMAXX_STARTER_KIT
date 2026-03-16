#!/usr/bin/env python3
"""
PRINTMAXX Lead Collector
=========================
Lightweight HTTP server that accepts POST requests from any deployed surge.sh
page running lead-capture-universal.js and appends leads to LEDGER/leads.csv.

Features:
  - Email format validation
  - Deduplication (same email never added twice)
  - Captures source, page_url, UTM params, timestamp
  - CORS headers so browser POSTs work cross-origin
  - JSON success/error responses

Usage:
    python3 AUTOMATIONS/lead_collector.py              # start on :8888
    python3 AUTOMATIONS/lead_collector.py --port 9090  # custom port
    python3 AUTOMATIONS/lead_collector.py --status     # show lead count + recent
    python3 AUTOMATIONS/lead_collector.py --dry-run    # parse + validate, no write
    python3 AUTOMATIONS/lead_collector.py --list       # print all leads to stdout

Cron (keep it running, restart if dead):
    */5 * * * * pgrep -f "lead_collector.py" || cd $BASE && $PYTHON AUTOMATIONS/lead_collector.py >> AUTOMATIONS/logs/lead_collector.log 2>&1 &
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import re
import sys
from datetime import datetime
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parent.parent
LEADS_CSV    = PROJECT_ROOT / "LEDGER" / "leads.csv"
LOG_DIR      = PROJECT_ROOT / "AUTOMATIONS" / "logs"
LOG_FILE     = LOG_DIR / "lead_collector.log"

# CSV columns
CSV_FIELDS = [
    "timestamp", "email", "source", "page_url", "referrer",
    "utm_source", "utm_medium", "utm_campaign", "utm_content", "utm_term",
    "ip"
]


def safe_path(target: Path) -> Path:
    resolved = Path(target).resolve()
    if not str(resolved).startswith(str(PROJECT_ROOT)):
        raise ValueError(f"BLOCKED: {resolved} is outside project root {PROJECT_ROOT}")
    return resolved


def log(msg: str) -> None:
    ts  = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] {msg}"
    print(line, flush=True)
    try:
        safe_path(LOG_DIR).mkdir(parents=True, exist_ok=True)
        with open(safe_path(LOG_FILE), "a") as f:
            f.write(line + "\n")
    except Exception:
        pass


# ---------------------------------------------------------------------------
# CSV helpers
# ---------------------------------------------------------------------------

def ensure_csv() -> None:
    p = safe_path(LEADS_CSV)
    if not p.exists() or p.stat().st_size == 0:
        p.parent.mkdir(parents=True, exist_ok=True)
        with open(p, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=CSV_FIELDS)
            writer.writeheader()


def load_existing_emails() -> set[str]:
    p = safe_path(LEADS_CSV)
    if not p.exists():
        return set()
    emails: set[str] = set()
    try:
        with open(p, newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row.get("email"):
                    emails.add(row["email"].strip().lower())
    except Exception:
        pass
    return emails


def append_lead(data: dict, dry_run: bool = False) -> tuple[bool, str]:
    """
    Returns (success, message).
    Validates email, deduplicates, then appends to CSV.
    """
    email = (data.get("email") or "").strip().lower()

    # Validate
    if not email:
        return False, "email required"
    if not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email):
        return False, f"invalid email: {email}"

    # Deduplicate
    existing = load_existing_emails()
    if email in existing:
        return False, f"duplicate: {email}"

    if dry_run:
        return True, f"dry-run OK: would add {email}"

    row = {
        "timestamp":    datetime.now().isoformat(),
        "email":        email,
        "source":       (data.get("source") or "").strip()[:200],
        "page_url":     (data.get("page_url") or "").strip()[:500],
        "referrer":     (data.get("referrer") or "").strip()[:500],
        "utm_source":   (data.get("utm_source") or "").strip()[:100],
        "utm_medium":   (data.get("utm_medium") or "").strip()[:100],
        "utm_campaign": (data.get("utm_campaign") or "").strip()[:100],
        "utm_content":  (data.get("utm_content") or "").strip()[:100],
        "utm_term":     (data.get("utm_term") or "").strip()[:100],
        "ip":           (data.get("ip") or "").strip()[:45],
    }

    ensure_csv()
    with open(safe_path(LEADS_CSV), "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_FIELDS)
        writer.writerow(row)

    return True, f"saved: {email}"


# ---------------------------------------------------------------------------
# HTTP handler
# ---------------------------------------------------------------------------

class LeadHandler(BaseHTTPRequestHandler):

    def log_message(self, fmt: str, *args) -> None:
        # Suppress default noisy access log; we write our own
        pass

    def _cors_headers(self) -> None:
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")

    def do_OPTIONS(self) -> None:
        # Pre-flight CORS request from browser
        self.send_response(204)
        self._cors_headers()
        self.end_headers()

    def do_POST(self) -> None:
        if self.path.rstrip("/") not in ("/lead", "/leads"):
            self._respond(404, {"error": "not found"})
            return

        content_len = int(self.headers.get("Content-Length", 0))
        if content_len > 8192:
            self._respond(400, {"error": "payload too large"})
            return

        raw = self.rfile.read(content_len)
        try:
            data = json.loads(raw.decode("utf-8", errors="replace"))
        except Exception:
            self._respond(400, {"error": "invalid JSON"})
            return

        # Attach client IP for light abuse detection
        data["ip"] = self.client_address[0]

        ok, msg = append_lead(data)
        if ok:
            log(f"LEAD  {msg}")
            self._respond(200, {"success": True, "message": msg})
        else:
            if "duplicate" in msg:
                # Still 200 so the frontend shows the thank-you modal
                log(f"DUP   {msg}")
                self._respond(200, {"success": True, "message": "already subscribed"})
            else:
                log(f"ERR   {msg}")
                self._respond(400, {"error": msg})

    def do_GET(self) -> None:
        if self.path.rstrip("/") == "/health":
            count = len(load_existing_emails())
            self._respond(200, {"status": "ok", "leads": count})
        else:
            self._respond(404, {"error": "not found"})

    def _respond(self, status: int, body: dict) -> None:
        payload = json.dumps(body).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(payload)))
        self._cors_headers()
        self.end_headers()
        self.wfile.write(payload)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def cmd_status() -> None:
    ensure_csv()
    rows: list[dict] = []
    with open(safe_path(LEADS_CSV), newline="") as f:
        rows = list(csv.DictReader(f))

    total = len(rows)
    today = datetime.now().strftime("%Y-%m-%d")

    today_rows  = [r for r in rows if (r.get("timestamp") or "").startswith(today)]

    from collections import Counter
    sources = Counter(r.get("source", "unknown") for r in rows)
    top_sources = sources.most_common(5)

    print(f"\n=== Lead Collector Status ===")
    print(f"Total leads : {total}")
    print(f"Today       : {len(today_rows)}")
    print(f"\nTop sources:")
    for src, cnt in top_sources:
        print(f"  {cnt:>4}  {src}")

    print(f"\nLast 5 leads:")
    for r in rows[-5:]:
        print(f"  {r.get('timestamp','')[:16]}  {r.get('email',''):<35}  {r.get('source','')}")

    print()


def cmd_list() -> None:
    ensure_csv()
    with open(safe_path(LEADS_CSV), newline="") as f:
        for row in csv.DictReader(f):
            print(f"{row.get('timestamp','')[:16]}  {row.get('email',''):<35}  {row.get('source','')}")


def cmd_serve(port: int) -> None:
    ensure_csv()
    server = HTTPServer(("0.0.0.0", port), LeadHandler)
    log(f"Lead collector listening on port {port}")
    log(f"Endpoint : http://localhost:{port}/lead")
    log(f"Health   : http://localhost:{port}/health")
    log(f"CSV      : {LEADS_CSV}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        log("Shutting down")
        server.server_close()


def main() -> None:
    parser = argparse.ArgumentParser(
        description="PRINTMAXX lead collector server"
    )
    parser.add_argument("--port",    type=int, default=8888, help="Port to listen on (default 8888)")
    parser.add_argument("--status",  action="store_true",   help="Show lead stats and exit")
    parser.add_argument("--list",    action="store_true",   help="Print all leads and exit")
    parser.add_argument("--dry-run", action="store_true",   help="Test mode — validate but do not write")
    args = parser.parse_args()

    if args.status:
        cmd_status()
        return

    if args.list:
        cmd_list()
        return

    if args.dry_run:
        test = {"email": "test@example.com", "source": "dry-run"}
        ok, msg = append_lead(test, dry_run=True)
        print(f"dry-run result: {msg}")
        return

    cmd_serve(args.port)


if __name__ == "__main__":
    main()
