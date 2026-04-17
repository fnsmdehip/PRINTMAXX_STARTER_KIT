#!/usr/bin/env python3
"""
PRINTMAXX Telegram Control Bot
================================
Full two-way control of the PRINTMAXX system from your iPhone via Telegram.

Commands:
  /start      - Welcome message + command list
  /status     - System health summary (16-point check)
  /health     - Quick health check (fast)
  /cron       - List active cron jobs
  /revenue    - Revenue pipeline state
  /queue      - Actionable queue (top 10)
  /run <cmd>  - Run a whitelisted automation command
  /loops      - Loop closer status
  /sites      - Count live surge.sh sites
  /alpha      - Recent alpha entries count + last 3
  /morning    - Trigger morning DAG manually
  /decision   - Run decision engine cycle
  /logs       - Last 20 lines of latest log
  /help       - Show all commands

Setup (5 min):
  1. Message @BotFather on Telegram -> /newbot -> get token
  2. Send any message to your new bot
  3. Visit: https://api.telegram.org/bot<TOKEN>/getUpdates
     Copy your "id" from the "chat" object
  4. Add to .env:
       TELEGRAM_BOT_TOKEN=your_token_here
       TELEGRAM_CHAT_ID=your_chat_id_here
  5. Run: python3 AUTOMATIONS/telegram_control_bot.py
  6. Add to cron for auto-restart:
       */5 * * * * pgrep -f telegram_control_bot.py || python3 /path/to/AUTOMATIONS/telegram_control_bot.py &

Usage:
  python3 AUTOMATIONS/telegram_control_bot.py          # Start bot (blocking)
  python3 AUTOMATIONS/telegram_control_bot.py --test   # Send test message and exit
  python3 AUTOMATIONS/telegram_control_bot.py --daemon # Run in background
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
import urllib.parse
import urllib.request
from datetime import datetime
from pathlib import Path

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parent.parent
AUTOMATIONS = PROJECT_ROOT / "AUTOMATIONS"
OPS = PROJECT_ROOT / "OPS"
LEDGER = PROJECT_ROOT / "LEDGER"
LOGS = AUTOMATIONS / "logs"
ENV_PATH = PROJECT_ROOT / ".env"
OFFSET_FILE = AUTOMATIONS / "logs" / "telegram_bot_offset.txt"
PID_FILE = AUTOMATIONS / "logs" / "telegram_bot.pid"

PYTHON = sys.executable

# ---------------------------------------------------------------------------
# Whitelisted commands (safe to run from phone)
# Anything NOT in this list is blocked. No arbitrary shell execution.
# ---------------------------------------------------------------------------
ALLOWED_COMMANDS = {
    "health": f"{PYTHON} {AUTOMATIONS}/system_health_monitor.py --quick",
    "health_full": f"{PYTHON} {AUTOMATIONS}/system_health_monitor.py --check",
    "decision": f"{PYTHON} {AUTOMATIONS}/decision_engine.py --cycle",
    "morning": f"{PYTHON} {AUTOMATIONS}/morning_dag.py --run",
    "loops": f"{PYTHON} {AUTOMATIONS}/loop_closer.py --status",
    "scrape_twitter": f"{PYTHON} {AUTOMATIONS}/twitter_alpha_scraper.py --all",
    "scrape_reddit": f"{PYTHON} {AUTOMATIONS}/background_reddit_scraper.py --scrape",
    "alpha_process": f"{PYTHON} {AUTOMATIONS}/alpha_auto_processor.py --process-new",
    "capital_rank": f"{PYTHON} {AUTOMATIONS}/capital_genesis_ranker.py --rank --top 5",
    "venture_status": f"{PYTHON} {AUTOMATIONS}/venture_autonomy.py --status",
    "swarm_status": f"{PYTHON} {AUTOMATIONS}/agent_swarm.py --status",
    "ceo_status": f"{PYTHON} {AUTOMATIONS}/ceo_agent.py --status",
}


# ---------------------------------------------------------------------------
# Config loader
# ---------------------------------------------------------------------------
def _load_config() -> tuple[str, str]:
    token = os.environ.get("TELEGRAM_BOT_TOKEN", "")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID", "")

    if ENV_PATH.exists():
        for line in ENV_PATH.read_text().splitlines():
            line = line.strip()
            if line.startswith("TELEGRAM_BOT_TOKEN=") and not token:
                token = line.split("=", 1)[1].strip().strip('"').strip("'")
            elif line.startswith("TELEGRAM_CHAT_ID=") and not chat_id:
                chat_id = line.split("=", 1)[1].strip().strip('"').strip("'")

    return token, chat_id


TOKEN, CHAT_ID = _load_config()


# ---------------------------------------------------------------------------
# Telegram API helpers
# ---------------------------------------------------------------------------
def _api_call(method: str, params: dict) -> dict:
    if not TOKEN:
        return {"ok": False, "error": "TELEGRAM_BOT_TOKEN not set"}
    url = f"https://api.telegram.org/bot{TOKEN}/{method}"
    data = urllib.parse.urlencode(params).encode()
    try:
        req = urllib.request.Request(url, data=data, method="POST")
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.loads(resp.read().decode())
    except Exception as e:
        return {"ok": False, "error": str(e)}


def send(text: str, chat_id: str = "") -> bool:
    cid = chat_id or CHAT_ID
    if not cid:
        return False
    # Telegram max message length: 4096
    if len(text) > 4000:
        text = text[:3990] + "\n...(truncated)"
    result = _api_call("sendMessage", {"chat_id": cid, "text": text, "parse_mode": "HTML"})
    return result.get("ok", False)


def get_updates(offset: int = 0) -> list:
    result = _api_call("getUpdates", {"offset": offset, "timeout": 30, "limit": 10})
    if result.get("ok"):
        return result.get("result", [])
    return []


def load_offset() -> int:
    try:
        if OFFSET_FILE.exists():
            return int(OFFSET_FILE.read_text().strip())
    except Exception:
        pass
    return 0


def save_offset(offset: int):
    LOGS.mkdir(parents=True, exist_ok=True)
    OFFSET_FILE.write_text(str(offset))


# ---------------------------------------------------------------------------
# Command handlers
# ---------------------------------------------------------------------------
def _run_cmd(cmd: str, timeout: int = 60) -> str:
    try:
        result = subprocess.run(
            cmd, shell=True, capture_output=True, text=True, timeout=timeout
        )
        output = result.stdout + result.stderr
        return output.strip() or "(no output)"
    except subprocess.TimeoutExpired:
        return f"Timed out after {timeout}s"
    except Exception as e:
        return f"Error: {e}"


def cmd_status() -> str:
    lines = ["PRINTMAXX System Status", "=" * 30]

    # Cron count
    cron_out = _run_cmd("crontab -l 2>/dev/null | grep -c PRINTMAXX || echo 0")
    lines.append(f"Crons active: {cron_out.strip()}")

    # Alpha count
    alpha_path = LEDGER / "ALPHA_STAGING.csv"
    if alpha_path.exists():
        try:
            count = sum(1 for _ in open(alpha_path)) - 1
            lines.append(f"Alpha entries: {count}")
        except Exception:
            lines.append("Alpha: unreadable")

    # Latest log
    log_files = sorted(LOGS.glob("system_health_*.json"), reverse=True)
    if log_files:
        try:
            data = json.loads(log_files[0].read_text())
            score = data.get("health_score", "?")
            lines.append(f"Health score: {score}/100")
        except Exception:
            lines.append("Health log: unreadable")

    # Control panel
    cp_pid = _run_cmd("pgrep -f control_panel.py || echo 'DOWN'")
    lines.append(f"Control panel: {'UP (port 9999)' if cp_pid.strip() != 'DOWN' else 'DOWN'}")

    # Decision engine last run
    de_log = AUTOMATIONS / "logs" / "decision_engine.log"
    if de_log.exists():
        try:
            mtime = datetime.fromtimestamp(de_log.stat().st_mtime)
            age_h = (datetime.now() - mtime).total_seconds() / 3600
            lines.append(f"Decision engine: {age_h:.1f}h ago")
        except Exception:
            pass

    lines.append(f"\nTimestamp: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    return "\n".join(lines)


def cmd_health() -> str:
    output = _run_cmd(
        f"{PYTHON} {AUTOMATIONS}/system_health_monitor.py --quick", timeout=30
    )
    return f"Health Check:\n{output}"


def cmd_cron() -> str:
    output = _run_cmd("crontab -l 2>/dev/null | grep -v '^#' | grep -v '^$'")
    lines = [l for l in output.splitlines() if l.strip()]
    if not lines:
        return "No cron jobs found."
    summary = [f"Cron jobs ({len(lines)} total):"]
    for l in lines[:15]:
        parts = l.split(None, 5)
        if len(parts) >= 6:
            schedule = " ".join(parts[:5])
            script = Path(parts[5].split()[-1]).name if parts[5] else parts[5]
            summary.append(f"  {schedule} | {script}")
        else:
            summary.append(f"  {l[:80]}")
    if len(lines) > 15:
        summary.append(f"  ...and {len(lines)-15} more")
    return "\n".join(summary)


def cmd_revenue() -> str:
    rev_file = PROJECT_ROOT / "FINANCIALS" / "revenue_pipeline.json"
    lines = ["Revenue Pipeline:"]
    if rev_file.exists():
        try:
            data = json.loads(rev_file.read_text())
            for k, v in list(data.items())[:10]:
                lines.append(f"  {k}: {v}")
        except Exception:
            lines.append("  (could not parse)")
    else:
        lines.append("  No revenue_pipeline.json found")

    # Check Stripe balance file if exists
    stripe_file = OPS / "STRIPE_PRODUCTS.md"
    if stripe_file.exists():
        lines.append("\nStripe products: configured (see OPS/STRIPE_PRODUCTS.md)")

    lines.append(f"\nChecked: {datetime.now().strftime('%H:%M')}")
    return "\n".join(lines)


def cmd_queue() -> str:
    queue_file = OPS / "ACTIONABLE_QUEUE.md"
    if not queue_file.exists():
        return "OPS/ACTIONABLE_QUEUE.md not found."
    content = queue_file.read_text()
    lines = content.splitlines()
    # Show first 25 lines
    preview = "\n".join(lines[:25])
    if len(lines) > 25:
        preview += f"\n...({len(lines)-25} more lines)"
    return f"Actionable Queue:\n{preview}"


def cmd_loops() -> str:
    output = _run_cmd(
        f"{PYTHON} {AUTOMATIONS}/loop_closer.py --status", timeout=30
    )
    return f"Loop Status:\n{output}"


def cmd_sites() -> str:
    urls_file = OPS / "DEPLOYMENT_URLS.md"
    if urls_file.exists():
        content = urls_file.read_text()
        live = content.count("LIVE")
        total = content.count("surge.sh")
        return f"Deployed sites: {live} LIVE out of {total} total\n(OPS/DEPLOYMENT_URLS.md)"
    return "OPS/DEPLOYMENT_URLS.md not found"


def cmd_alpha() -> str:
    alpha_path = LEDGER / "ALPHA_STAGING.csv"
    if not alpha_path.exists():
        return "ALPHA_STAGING.csv not found"
    try:
        lines = alpha_path.read_text().splitlines()
        count = max(0, len(lines) - 1)
        result = [f"Alpha staging: {count} entries"]
        # Show last 3
        if len(lines) > 1:
            result.append("\nLast 3 entries:")
            for row in lines[-3:]:
                if row.strip():
                    parts = row.split(",")
                    title = parts[0][:60] if parts else row[:60]
                    result.append(f"  - {title}")
        return "\n".join(result)
    except Exception as e:
        return f"Error reading alpha: {e}"


def cmd_logs() -> str:
    log_files = sorted(LOGS.glob("*.log"), key=lambda p: p.stat().st_mtime, reverse=True)
    if not log_files:
        return "No log files found in AUTOMATIONS/logs/"
    latest = log_files[0]
    content = latest.read_text(errors="replace")
    lines = content.splitlines()
    last_20 = "\n".join(lines[-20:])
    return f"Last 20 lines of {latest.name}:\n{last_20}"


def cmd_run(arg: str) -> str:
    if not arg:
        available = "\n".join(f"  /run {k}" for k in sorted(ALLOWED_COMMANDS.keys()))
        return f"Available run targets:\n{available}"

    cmd_key = arg.strip().lower()
    if cmd_key not in ALLOWED_COMMANDS:
        return (
            f"Unknown command: {cmd_key}\n"
            f"Allowed: {', '.join(sorted(ALLOWED_COMMANDS.keys()))}"
        )

    send(f"Running: {cmd_key} ...")
    output = _run_cmd(ALLOWED_COMMANDS[cmd_key], timeout=120)
    # Trim output for Telegram
    if len(output) > 1500:
        output = output[:1490] + "\n...(truncated)"
    return f"Result of {cmd_key}:\n{output}"


def cmd_morning() -> str:
    send("Starting morning DAG. This may take 2-3 minutes...")
    output = _run_cmd(f"{PYTHON} {AUTOMATIONS}/morning_dag.py --run", timeout=300)
    if len(output) > 1500:
        output = output[:1490] + "\n...(truncated)"
    return f"Morning DAG:\n{output}"


def cmd_decision() -> str:
    send("Running decision engine cycle...")
    output = _run_cmd(f"{PYTHON} {AUTOMATIONS}/decision_engine.py --cycle", timeout=180)
    if len(output) > 1500:
        output = output[:1490] + "\n...(truncated)"
    return f"Decision Engine:\n{output}"


HELP_TEXT = """PRINTMAXX Mobile Control

Commands:
  /status   - Full system overview
  /health   - Quick health check
  /cron     - Active cron jobs
  /revenue  - Revenue pipeline
  /queue    - Actionable queue (top items)
  /loops    - Loop closer status
  /sites    - Live site count
  /alpha    - Alpha staging stats
  /logs     - Recent log output
  /morning  - Trigger morning DAG
  /decision - Run decision engine
  /run      - Run automation (see /run for list)
  /help     - This message

Running on: """ + str(PROJECT_ROOT.name)


# ---------------------------------------------------------------------------
# Message dispatcher
# ---------------------------------------------------------------------------
def handle_message(text: str, chat_id: str) -> str:
    text = text.strip()
    if not text.startswith("/"):
        return "Send a command starting with /. Try /help"

    parts = text.split(None, 1)
    command = parts[0].lower().lstrip("/")
    # Strip @botname suffix if present
    if "@" in command:
        command = command.split("@")[0]
    arg = parts[1] if len(parts) > 1 else ""

    handlers = {
        "start": lambda: HELP_TEXT,
        "help": lambda: HELP_TEXT,
        "status": cmd_status,
        "health": cmd_health,
        "cron": cmd_cron,
        "revenue": cmd_revenue,
        "queue": cmd_queue,
        "loops": cmd_loops,
        "sites": cmd_sites,
        "alpha": cmd_alpha,
        "logs": cmd_logs,
        "morning": cmd_morning,
        "decision": cmd_decision,
        "run": lambda: cmd_run(arg),
    }

    handler = handlers.get(command)
    if handler is None:
        return f"Unknown command: /{command}\nTry /help"

    try:
        return handler()
    except Exception as e:
        return f"Error in /{command}: {e}"


# ---------------------------------------------------------------------------
# Security: only allow messages from configured CHAT_ID
# ---------------------------------------------------------------------------
def is_authorized(chat_id: str) -> bool:
    if not CHAT_ID:
        return True  # No restriction if not configured
    return str(chat_id) == str(CHAT_ID)


# ---------------------------------------------------------------------------
# Main polling loop
# ---------------------------------------------------------------------------
def run_bot():
    if not TOKEN:
        print("ERROR: TELEGRAM_BOT_TOKEN not set. Add to .env or environment.")
        print("  TELEGRAM_BOT_TOKEN=your_token_here")
        print("  TELEGRAM_CHAT_ID=your_chat_id_here")
        sys.exit(1)

    # Write PID
    LOGS.mkdir(parents=True, exist_ok=True)
    PID_FILE.write_text(str(os.getpid()))

    print(f"[telegram_control_bot] Started. PID: {os.getpid()}")
    print(f"[telegram_control_bot] Authorized chat_id: {CHAT_ID or 'ANY (not restricted)'}")

    send(
        f"PRINTMAXX bot online. {datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
        "Type /help for commands."
    )

    offset = load_offset()

    while True:
        try:
            updates = get_updates(offset)
            for update in updates:
                update_id = update.get("update_id", 0)
                offset = update_id + 1
                save_offset(offset)

                msg = update.get("message") or update.get("edited_message")
                if not msg:
                    continue

                chat_id = str(msg.get("chat", {}).get("id", ""))
                text = msg.get("text", "")

                if not text:
                    continue

                if not is_authorized(chat_id):
                    send("Unauthorized.", chat_id)
                    print(f"[telegram_control_bot] Blocked unauthorized chat_id: {chat_id}")
                    continue

                print(
                    f"[telegram_control_bot] {datetime.now().strftime('%H:%M:%S')} "
                    f"From {chat_id}: {text[:80]}"
                )

                response = handle_message(text, chat_id)
                send(response, chat_id)

        except KeyboardInterrupt:
            print("[telegram_control_bot] Stopped by user.")
            if PID_FILE.exists():
                PID_FILE.unlink()
            break
        except Exception as e:
            print(f"[telegram_control_bot] Error in main loop: {e}")
            time.sleep(5)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(description="PRINTMAXX Telegram Control Bot")
    parser.add_argument("--test", action="store_true", help="Send test message and exit")
    parser.add_argument("--daemon", action="store_true", help="Print background start command")
    parser.add_argument("--status", action="store_true", help="Check if bot is running")
    args = parser.parse_args()

    if args.status:
        if PID_FILE.exists():
            pid = PID_FILE.read_text().strip()
            # Check if process is actually running
            result = subprocess.run(["kill", "-0", pid], capture_output=True)
            if result.returncode == 0:
                print(f"Bot is RUNNING (PID {pid})")
            else:
                print(f"Bot is STOPPED (stale PID {pid})")
                PID_FILE.unlink()
        else:
            print("Bot is STOPPED")
        return

    if args.test:
        token, chat_id = _load_config()
        if not token:
            print("ERROR: TELEGRAM_BOT_TOKEN not set")
            sys.exit(1)
        ok = send(
            f"PRINTMAXX test message. {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
            "If you see this, the bot is configured correctly!"
        )
        print("Test message sent successfully!" if ok else "FAILED to send test message")
        return

    if args.daemon:
        script = Path(__file__).resolve()
        print(f"To run in background:")
        print(f"  nohup {PYTHON} {script} > {LOGS}/telegram_bot.log 2>&1 &")
        print(f"\nTo add keepalive cron (restarts every 5 min if dead):")
        print(f"  */5 * * * * pgrep -f telegram_control_bot.py || nohup {PYTHON} {script} >> {LOGS}/telegram_bot.log 2>&1 &")
        return

    run_bot()


if __name__ == "__main__":
    main()
