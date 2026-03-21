#!/usr/bin/env python3

from __future__ import annotations
"""
PRINTMAXX Autonomous Worker — Telegram Alert Module

Sends notifications to Telegram for:
- Task completion/failure
- Human-needed escalations
- Daily digest summaries
- Cost cap warnings
- System health alerts

Setup:
1. Message @BotFather on Telegram, create a bot, get the token
2. Send a message to your bot, then get your chat_id from:
   https://api.telegram.org/bot<TOKEN>/getUpdates
3. Set in config:
   TELEGRAM_BOT_TOKEN=your_token
   TELEGRAM_CHAT_ID=your_chat_id
"""

import json
import os
import urllib.request
import urllib.parse
from datetime import datetime
from pathlib import Path

# Config paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent
CONFIG_PATH = PROJECT_ROOT / "OPS" / "AUTONOMOUS_WORKER_CONFIG.yaml"
ALERT_LOG = PROJECT_ROOT / "AUTOMATIONS" / "logs" / "alerts.jsonl"


def _load_telegram_config():
    """Load Telegram credentials from config or environment."""
    token = os.environ.get("TELEGRAM_BOT_TOKEN", "")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID", "")

    # Fallback: try reading from config file
    if not token or not chat_id:
        try:
            config_text = CONFIG_PATH.read_text()
            for line in config_text.split("\n"):
                line = line.strip()
                if line.startswith("telegram_bot_token:"):
                    token = token or line.split(":", 1)[1].strip().strip('"').strip("'")
                if line.startswith("telegram_chat_id:"):
                    chat_id = chat_id or line.split(":", 1)[1].strip().strip('"').strip("'")
        except FileNotFoundError:
            pass

    return token, chat_id


def _log_alert(alert_type: str, message: str, sent: bool):
    """Append alert to log file."""
    ALERT_LOG.parent.mkdir(parents=True, exist_ok=True)
    entry = {
        "timestamp": datetime.now().isoformat(),
        "type": alert_type,
        "message": message[:200],
        "sent": sent,
    }
    with open(ALERT_LOG, "a") as f:
        f.write(json.dumps(entry) + "\n")


def send_telegram(message: str, alert_type: str = "info") -> bool:
    """Send a message via Telegram bot. Returns True if sent successfully."""
    token, chat_id = _load_telegram_config()

    if not token or not chat_id:
        print(f"[ALERT] Telegram not configured. Message: {message[:100]}")
        _log_alert(alert_type, message, sent=False)
        return False

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    data = urllib.parse.urlencode({
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "Markdown",
        "disable_web_page_preview": "true",
    }).encode("utf-8")

    try:
        req = urllib.request.Request(url, data=data, method="POST")
        with urllib.request.urlopen(req, timeout=10) as resp:
            result = json.loads(resp.read())
            sent = result.get("ok", False)
            _log_alert(alert_type, message, sent=sent)
            return sent
    except Exception as e:
        print(f"[ALERT] Telegram send failed: {e}")
        _log_alert(alert_type, message, sent=False)
        return False


# --- Alert Templates ---

def alert_task_started(task_id: str, description: str):
    """Notify that an autonomous task has started."""
    msg = (
        f"🔄 *Task Started*\n"
        f"ID: `{task_id}`\n"
        f"{description[:200]}"
    )
    return send_telegram(msg, "task_started")


def alert_task_completed(task_id: str, description: str, duration_min: float, output_summary: str = ""):
    """Notify that a task completed successfully."""
    msg = (
        f"✅ *Task Completed*\n"
        f"ID: `{task_id}`\n"
        f"Duration: {duration_min:.1f} min\n"
        f"{description[:150]}"
    )
    if output_summary:
        msg += f"\n\nOutput: {output_summary[:200]}"
    return send_telegram(msg, "task_completed")


def alert_task_failed(task_id: str, description: str, error: str):
    """Notify that a task failed."""
    msg = (
        f"❌ *Task Failed*\n"
        f"ID: `{task_id}`\n"
        f"{description[:150]}\n"
        f"\nError: {error[:300]}"
    )
    return send_telegram(msg, "task_failed")


def alert_human_needed(task_id: str, reason: str):
    """Escalate to human — something needs manual intervention."""
    msg = (
        f"🚨 *HUMAN NEEDED*\n"
        f"Task: `{task_id}`\n"
        f"\n{reason[:400]}\n"
        f"\nCheck: `OPS/HUMAN_NEEDED/{task_id}.md`"
    )
    return send_telegram(msg, "human_needed")


def alert_cost_warning(daily_cost: float, daily_cap: float):
    """Warn that daily cost is approaching or exceeding cap."""
    pct = (daily_cost / daily_cap * 100) if daily_cap > 0 else 0
    msg = (
        f"💰 *Cost Warning*\n"
        f"Daily spend: ${daily_cost:.2f} / ${daily_cap:.2f} ({pct:.0f}%)\n"
    )
    if daily_cost >= daily_cap:
        msg += "\n⛔ *DAILY CAP HIT. Supervisor paused until midnight.*"
    return send_telegram(msg, "cost_warning")


def alert_agent_timeout(task_id: str, timeout_min: float):
    """Notify that an agent was killed due to timeout."""
    msg = (
        f"⏰ *Agent Timeout*\n"
        f"Task: `{task_id}`\n"
        f"Killed after {timeout_min:.0f} min (exceeded time cap)\n"
        f"Task returned to queue."
    )
    return send_telegram(msg, "agent_timeout")


def alert_daily_digest(stats: dict):
    """Send end-of-day summary."""
    msg = (
        f"📊 *Daily Digest — {datetime.now().strftime('%Y-%m-%d')}*\n"
        f"\n"
        f"Tasks completed: {stats.get('completed', 0)}\n"
        f"Tasks failed: {stats.get('failed', 0)}\n"
        f"Tasks pending: {stats.get('pending', 0)}\n"
        f"Total runtime: {stats.get('total_runtime_min', 0):.0f} min\n"
        f"Estimated cost: ${stats.get('estimated_cost', 0):.2f}\n"
    )
    if stats.get("content_generated", 0) > 0:
        msg += f"Content generated: {stats['content_generated']} pieces\n"
    if stats.get("alpha_found", 0) > 0:
        msg += f"Alpha found: {stats['alpha_found']} entries\n"
    if stats.get("errors"):
        msg += f"\nTop errors:\n"
        for err in stats["errors"][:3]:
            msg += f"  - {err[:100]}\n"
    return send_telegram(msg, "daily_digest")


def alert_system_health(status: str, details: str = ""):
    """Send system health check result."""
    icon = "🟢" if status == "HEALTHY" else "🟡" if status == "DEGRADED" else "🔴"
    msg = f"{icon} *System Health: {status}*"
    if details:
        msg += f"\n{details[:400]}"
    return send_telegram(msg, "system_health")


def alert_supervisor_started():
    """Notify that the supervisor daemon has started."""
    msg = (
        f"🚀 *Autonomous Supervisor Started*\n"
        f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
        f"Host: {os.uname().nodename}\n"
        f"Ready to process tasks."
    )
    return send_telegram(msg, "supervisor_started")


def alert_supervisor_stopped(reason: str = "manual"):
    """Notify that the supervisor daemon has stopped."""
    msg = (
        f"🛑 *Autonomous Supervisor Stopped*\n"
        f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
        f"Reason: {reason}"
    )
    return send_telegram(msg, "supervisor_stopped")


def alert_queue_empty():
    """Notify that the task queue is empty and self-planning will begin."""
    msg = (
        f"📋 *Task Queue Empty*\n"
        f"Spawning self-planning agent to generate new tasks.\n"
        f"Next check in 5 minutes."
    )
    return send_telegram(msg, "queue_empty")


# --- CLI for testing ---

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        print("Testing Telegram connection...")
        result = send_telegram("🧪 PRINTMAXX Autonomous Worker — test alert. If you see this, Telegram is configured correctly.")
        if result:
            print("✅ Telegram alert sent successfully!")
        else:
            print("❌ Telegram not configured or send failed.")
            print("Set TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID in environment or config.")
    elif len(sys.argv) > 1 and sys.argv[1] == "--status":
        token, chat_id = _load_telegram_config()
        print(f"Token configured: {'yes' if token else 'NO'}")
        print(f"Chat ID configured: {'yes' if chat_id else 'NO'}")
        if ALERT_LOG.exists():
            lines = ALERT_LOG.read_text().strip().split("\n")
            print(f"Alert log entries: {len(lines)}")
            if lines:
                last = json.loads(lines[-1])
                print(f"Last alert: {last['type']} at {last['timestamp']} (sent: {last['sent']})")
    else:
        print("Usage: python3 autonomous_alerts.py --test | --status")
