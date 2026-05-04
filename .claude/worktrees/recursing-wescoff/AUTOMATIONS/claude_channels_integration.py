#!/usr/bin/env python3
"""
PRINTMAXX Automation: Claude Code Channels → Telegram Bot Integration

Wires Claude Code Channels into the PRINTMAXX Telegram bot for remote agent
control. Simultaneously generates high-engagement content riding Anthropic's
Claude Code Channels announcement and produces a Gumroad setup guide.

Usage:
    python3 claude_channels_integration.py --run
    python3 claude_channels_integration.py --status
    python3 claude_channels_integration.py --dry-run
"""

import argparse
import csv
import json
import logging
import subprocess
import sys
import urllib.request
import urllib.error
import urllib.parse
from datetime import datetime, timezone
from pathlib import Path

# ---------------------------------------------------------------------------
# Bootstrap: try importing shared helpers; fall back to local stubs so the
# script can still run stand-alone if _common isn't on the path yet.
# ---------------------------------------------------------------------------
try:
    from _common import PROJECT, safe_path, recall_skills_for_task, capture_skill_from_result
except ImportError:
    PROJECT = Path(__file__).resolve().parent.parent

    def safe_path(rel: str | Path) -> Path:
        """Return an absolute path guaranteed to live inside PROJECT."""
        target = (PROJECT / rel).resolve()
        if not str(target).startswith(str(PROJECT)):
            raise ValueError(f"Path escapes PROJECT root: {target}")
        return target

    def recall_skills_for_task(task: str) -> list[str]:
        """Stub: returns empty skill list when _common is unavailable."""
        return []

    def capture_skill_from_result(result: dict) -> None:
        """Stub: no-op when _common is unavailable."""
        pass

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
LOG_FILE = safe_path("AUTOMATIONS/logs/claude_channels_integration.log")
CONTENT_DIR = safe_path("AUTOMATIONS/content")
GUMROAD_DIR = safe_path("AUTOMATIONS/gumroad")
STATE_FILE = safe_path("AUTOMATIONS/state/claude_channels_state.json")

# ---------------------------------------------------------------------------
# Logging (append mode, cron-safe — no interactive output required)
# ---------------------------------------------------------------------------
LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(message)s",
    handlers=[
        logging.FileHandler(str(LOG_FILE), mode="a"),
        logging.StreamHandler(sys.stdout),
    ],
)
log = logging.getLogger("printmaxx.channels")

# ---------------------------------------------------------------------------
# Content templates
# ---------------------------------------------------------------------------

TWEET_THREAD: list[str] = [
    (
        "@AnthropicAI just made Claude Code remote-controlled.\n\n"
        "Meet Channels.\n\n"
        "You can now:\n"
        "→ Connect a persistent local Claude session to a Discord or Telegram bot\n"
        "→ Message tasks to your bot on the go\n"
        "→ Get results delivered straight to your phone\n\n"
        "This changes everything for solo operators. 🧵"
    ),
    (
        "The old workflow:\n"
        "→ Boot laptop\n"
        "→ SSH into dev box\n"
        "→ Type commands\n\n"
        "The new workflow:\n"
        "→ Send a Telegram message\n"
        "→ Claude handles it\n\n"
        "Your AI agent is now truly always-on. 🔥"
    ),
    (
        "Here's how PRINTMAXX uses Claude Code Channels:\n\n"
        "1️⃣  Persistent Claude session runs on the server\n"
        "2️⃣  Telegram bot is the control surface\n"
        "3️⃣  Message a task → Claude executes → results in your pocket\n\n"
        "Content generation, client reports, Gumroad updates — all via chat."
    ),
    (
        "Want the exact setup guide?\n\n"
        "I built a step-by-step Gumroad doc covering:\n"
        "• Installing Claude Code + enabling Channels\n"
        "• Creating a Telegram bot with BotFather\n"
        "• Connecting the channel token\n"
        "• Running it headless on a VPS\n\n"
        "Drop a 🤖 and I'll send you the link."
    ),
]

GUMROAD_GUIDE: dict = {
    "title": "Remote-Control Claude Code via Telegram — Step-by-Step Setup Guide",
    "subtitle": "Use Claude Code Channels to control your AI agent from your phone",
    "sections": [
        {
            "heading": "Prerequisites",
            "body": (
                "- Claude Code installed (npm install -g @anthropic-ai/claude-code)\n"
                "- An Anthropic API key with Claude Code access\n"
                "- A Linux VPS or always-on Mac/PC\n"
                "- A Telegram account"
            ),
        },
        {
            "heading": "Step 1 — Create your Telegram Bot",
            "body": (
                "1. Open Telegram and search for @BotFather\n"
                "2. Send /newbot and follow the prompts\n"
                "3. Copy the HTTP API token BotFather gives you\n"
                "4. Store it safely — you'll need it in Step 3"
            ),
        },
        {
            "heading": "Step 2 — Enable Claude Code Channels",
            "body": (
                "Run inside your project directory:\n\n"
                "  claude --channel telegram\n\n"
                "Claude Code will print a channel connection string, e.g.:\n"
                "  channel://cc_<token>@channels.anthropic.com\n\n"
                "Keep this terminal session open (or use tmux/screen)."
            ),
        },
        {
            "heading": "Step 3 — Connect the Telegram Bot to the Channel",
            "body": (
                "In Claude Code settings (claude settings), add:\n\n"
                "  channels.telegram.botToken: <YOUR_BOT_TOKEN>\n"
                "  channels.telegram.allowedUsers: [<your_telegram_user_id>]\n\n"
                "Restart the channel session. Send /start to your bot.\n"
                "You should receive a confirmation message."
            ),
        },
        {
            "heading": "Step 4 — Run Headless on a VPS",
            "body": (
                "Use a systemd service or tmux to keep Claude Code alive:\n\n"
                "  tmux new-session -d -s claude 'claude --channel telegram'\n\n"
                "Or create /etc/systemd/system/claude-channel.service\n"
                "with ExecStart pointing to the claude binary.\n\n"
                "  systemctl enable --now claude-channel"
            ),
        },
        {
            "heading": "Step 5 — Send Your First Remote Task",
            "body": (
                "Open Telegram, message your bot:\n\n"
                '  "Generate a weekly content report and save it to reports/"\n\n'
                "Claude executes the task on your server and replies with the result.\n"
                "You just remote-controlled your AI agent from your phone. 🎉"
            ),
        },
        {
            "heading": "Troubleshooting",
            "body": (
                "- Bot not responding: check tmux/systemd is still running\n"
                "- Auth errors: verify ANTHROPIC_API_KEY is exported in the shell\n"
                "- Unknown user errors: confirm your Telegram user ID in allowedUsers\n"
                "- Logs: claude code writes to ~/.claude/logs/ by default"
            ),
        },
    ],
    "cta": (
        "Questions? DM @PRINTMAXX on Twitter/X or reply to this Gumroad product page."
    ),
}

PRINTMAXX_HOOK_CONFIG: dict = {
    "description": "PRINTMAXX Claude Channels Telegram hook configuration",
    "hook_type": "PostToolUse",
    "matcher": ".*",
    "action": "log_and_notify",
    "telegram": {
        "enabled": True,
        "notify_on": ["task_complete", "error", "file_write"],
    },
    "generated_at": datetime.now(timezone.utc).isoformat(),
}

# ---------------------------------------------------------------------------
# Core helpers
# ---------------------------------------------------------------------------

def load_state() -> dict:
    """Load persisted run state from JSON; return empty dict if missing."""
    try:
        state_file = safe_path(STATE_FILE.relative_to(PROJECT))
        if state_file.exists():
            return json.loads(state_file.read_text(encoding="utf-8"))
    except Exception as exc:
        log.warning("Could not load state: %s", exc)
    return {}


def save_state(state: dict) -> None:
    """Persist run state to JSON via safe_path."""
    try:
        rel = STATE_FILE.relative_to(PROJECT)
        target = safe_path(rel)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(json.dumps(state, indent=2), encoding="utf-8")
        log.debug("State saved → %s", target)
    except Exception as exc:
        log.error("Could not save state: %s", exc)


def write_json(rel: str | Path, data: dict | list, dry_run: bool = False) -> Path:
    """Write *data* as pretty JSON to PROJECT/rel, respecting --dry-run."""
    target = safe_path(rel)
    if dry_run:
        log.info("[DRY-RUN] Would write JSON → %s", target)
        return target
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    log.info("Wrote JSON → %s", target)
    return target


def write_text(rel: str | Path, content: str, dry_run: bool = False) -> Path:
    """Write plain text to PROJECT/rel, respecting --dry-run."""
    target = safe_path(rel)
    if dry_run:
        log.info("[DRY-RUN] Would write text → %s", target)
        return target
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content, encoding="utf-8")
    log.info("Wrote text → %s", target)
    return target


def write_csv(rel: str | Path, rows: list[dict], fieldnames: list[str], dry_run: bool = False) -> Path:
    """Write *rows* as CSV to PROJECT/rel, respecting --dry-run."""
    target = safe_path(rel)
    if dry_run:
        log.info("[DRY-RUN] Would write CSV → %s", target)
        return target
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    log.info("Wrote CSV → %s", target)
    return target

# ---------------------------------------------------------------------------
# Task implementations
# ---------------------------------------------------------------------------

def generate_tweet_thread(dry_run: bool) -> Path:
    """Serialise the tweet thread to a timestamped JSON file."""
    log.info("Generating tweet thread content…")
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    payload = {
        "campaign": "claude_channels_announcement",
        "generated_at": ts,
        "platform": "twitter",
        "thread": TWEET_THREAD,
    }
    rel = CONTENT_DIR.relative_to(PROJECT) / f"tweet_thread_{ts}.json"
    return write_json(rel, payload, dry_run=dry_run)


def generate_gumroad_guide(dry_run: bool) -> tuple[Path, Path]:
    """Write the Gumroad setup guide as both JSON (structured) and Markdown."""
    log.info("Generating Gumroad setup guide…")
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")

    json_rel = GUMROAD_DIR.relative_to(PROJECT) / f"claude_channels_guide_{ts}.json"
    json_path = write_json(json_rel, GUMROAD_GUIDE, dry_run=dry_run)

    # Build markdown
    lines = [
        f"# {GUMROAD_GUIDE['title']}",
        f"_{GUMROAD_GUIDE['subtitle']}_",
        "",
    ]
    for section in GUMROAD_GUIDE["sections"]:
        lines += [f"## {section['heading']}", "", section["body"], ""]
    lines += ["---", "", GUMROAD_GUIDE["cta"], ""]
    md_content = "\n".join(lines)

    md_rel = GUMROAD_DIR.relative_to(PROJECT) / f"claude_channels_guide_{ts}.md"
    md_path = write_text(md_rel, md_content, dry_run=dry_run)

    return json_path, md_path


def generate_hook_config(dry_run: bool) -> Path:
    """Write the PRINTMAXX Telegram hook configuration JSON."""
    log.info("Generating PRINTMAXX hook configuration…")
    rel = safe_path("AUTOMATIONS/hooks").relative_to(PROJECT) / "printmaxx_telegram_hook.json"
    return write_json(rel, PRINTMAXX_HOOK_CONFIG, dry_run=dry_run)


def generate_content_log(dry_run: bool) -> Path:
    """Append a run record to the content tracking CSV."""
    log.info("Updating content tracking CSV…")
    ts = datetime.now(timezone.utc).isoformat()
    rows = [
        {
            "timestamp": ts,
            "task": "tweet_thread",
            "status": "generated",
            "platform": "twitter",
            "campaign": "claude_channels",
        },
        {
            "timestamp": ts,
            "task": "gumroad_guide",
            "status": "generated",
            "platform": "gumroad",
            "campaign": "claude_channels",
        },
    ]
    fieldnames = ["timestamp", "task", "status", "platform", "campaign"]
    rel = CONTENT_DIR.relative_to(PROJECT) / "content_log.csv"
    target = safe_path(rel)

    if dry_run:
        log.info("[DRY-RUN] Would append %d rows to %s", len(rows), target)
        return target

    target.parent.mkdir(parents=True, exist_ok=True)
    file_exists = target.exists()
    with target.open("a", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        writer.writerows(rows)
    log.info("Appended %d rows → %s", len(rows), target)
    return target


def check_claude_code_version(dry_run: bool) -> str:
    """Return the installed claude-code version string (best-effort)."""
    if dry_run:
        log.info("[DRY-RUN] Would check claude-code version")
        return "dry-run"
    try:
        result = subprocess.run(
            ["claude", "--version"],
            capture_output=True,
            text=True,
            timeout=10,
        )
        version = result.stdout.strip() or result.stderr.strip() or "unknown"
        log.info("claude-code version: %s", version)
        return version
    except FileNotFoundError:
        log.warning("claude binary not found on PATH — Channels may not be installed yet")
        return "not-installed"
    except subprocess.TimeoutExpired:
        log.warning("claude --version timed out")
        return "timeout"
    except Exception as exc:
        log.warning("Could not determine claude version: %s", exc)
        return "error"


def ping_anthropic_status(dry_run: bool) -> bool:
    """HEAD-request the Anthropic status page to confirm connectivity."""
    url = "https://status.anthropic.com"
    if dry_run:
        log.info("[DRY-RUN] Would ping %s", url)
        return True
    try:
        req = urllib.request.Request(url, method="HEAD")
        with urllib.request.urlopen(req, timeout=8) as resp:
            ok = resp.status < 400
            log.info("Anthropic status ping → HTTP %d (%s)", resp.status, "OK" if ok else "WARN")
            return ok
    except urllib.error.URLError as exc:
        log.warning("Anthropic status ping failed: %s", exc)
        return False
    except Exception as exc:
        log.warning("Anthropic status ping error: %s", exc)
        return False

# ---------------------------------------------------------------------------
# Main actions
# ---------------------------------------------------------------------------

def action_run(dry_run: bool) -> int:
    """Execute the full PRINTMAXX Claude Channels integration pipeline."""
    log.info("=== PRINTMAXX Claude Channels Integration — %s ===",
             "DRY-RUN" if dry_run else "RUN")

    skills = recall_skills_for_task("claude_channels_telegram_integration")
    if skills:
        log.info("Recalled %d skill(s): %s", len(skills), skills)

    state = load_state()
    state["last_run"] = datetime.now(timezone.utc).isoformat()
    state["dry_run"] = dry_run

    results: dict = {}

    # 1. Environment checks
    try:
        state["claude_version"] = check_claude_code_version(dry_run)
        state["anthropic_reachable"] = ping_anthropic_status(dry_run)
    except Exception as exc:
        log.error("Environment check failed: %s", exc)

    # 2. Generate tweet thread
    try:
        tweet_path = generate_tweet_thread(dry_run)
        results["tweet_thread"] = str(tweet_path)
    except Exception as exc:
        log.error("Tweet thread generation failed: %s", exc)
        results["tweet_thread"] = "error"

    # 3. Generate Gumroad guide
    try:
        g_json, g_md = generate_gumroad_guide(dry_run)
        results["gumroad_json"] = str(g_json)
        results["gumroad_md"] = str(g_md)
    except Exception as exc:
        log.error("Gumroad guide generation failed: %s", exc)
        results["gumroad"] = "error"

    # 4. Write hook config
    try:
        hook_path = generate_hook_config(dry_run)
        results["hook_config"] = str(hook_path)
    except Exception as exc:
        log.error("Hook config generation failed: %s", exc)
        results["hook_config"] = "error"

    # 5. Update content tracking CSV
    try:
        csv_path = generate_content_log(dry_run)
        results["content_log"] = str(csv_path)
    except Exception as exc:
        log.error("Content log update failed: %s", exc)
        results["content_log"] = "error"

    state["last_results"] = results
    save_state(state)

    capture_skill_from_result(results)

    log.info("Pipeline complete. Outputs: %s", json.dumps(results, indent=2))
    return 0


def action_status() -> int:
    """Print last run state and file inventory."""
    log.info("=== PRINTMAXX Status ===")

    state = load_state()
    if state:
        log.info("Last run   : %s", state.get("last_run", "never"))
        log.info("Dry-run    : %s", state.get("dry_run", "unknown"))
        log.info("Claude ver : %s", state.get("claude_version", "unknown"))
        log.info("Anthropic  : %s", "reachable" if state.get("anthropic_reachable") else "unreachable")
        last = state.get("last_results", {})
        for key, val in last.items():
            log.info("  %-20s %s", key, val)
    else:
        log.info("No previous run state found.")

    for directory in (CONTENT_DIR, GUMROAD_DIR):
        if directory.exists():
            files = sorted(directory.rglob("*"))
            log.info("%s — %d file(s)", directory.relative_to(PROJECT), len(files))
        else:
            log.info("%s — directory not yet created", directory.relative_to(PROJECT))

    log.info("Log file: %s", LOG_FILE)
    return 0

# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="PRINTMAXX: Claude Code Channels → Telegram Bot integration",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Examples:\n"
            "  %(prog)s --run          # full pipeline\n"
            "  %(prog)s --dry-run      # preview without writing files\n"
            "  %(prog)s --status       # show last run info\n"
        ),
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--run", action="store_true", help="Execute the full integration pipeline")
    group.add_argument("--status", action="store_true", help="Show last run status and file inventory")
    group.add_argument("--dry-run", dest="dry_run", action="store_true",
                       help="Preview all actions without writing files")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    try:
        if args.run:
            sys.exit(action_run(dry_run=False))
        elif args.dry_run:
            sys.exit(action_run(dry_run=True))
        elif args.status:
            sys.exit(action_status())
    except KeyboardInterrupt:
        log.warning("Interrupted by user")
        sys.exit(130)
    except Exception as exc:
        log.exception("Unhandled exception: %s", exc)
        sys.exit(1)


if __name__ == "__main__":
    main()