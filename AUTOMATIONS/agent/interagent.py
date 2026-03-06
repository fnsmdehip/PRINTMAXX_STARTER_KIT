#!/usr/bin/env python3
"""
PRINTMAXX Inter-Agent Communication Bus

Enables Claude Code <-> Kodex (and any other agent) to pass messages,
share context, and coordinate work through a shared JSONL message bus.

Usage:
  # Send a message
  python3 AUTOMATIONS/agent/interagent.py send --from claude --to kodex --body "Check PR #42"

  # Read messages for an agent
  python3 AUTOMATIONS/agent/interagent.py read --for kodex

  # Read all recent messages
  python3 AUTOMATIONS/agent/interagent.py read --all

  # Post task handoff
  python3 AUTOMATIONS/agent/interagent.py handoff --from claude --to kodex --task "Review security" --context "See AUTOMATIONS/nsfw_safety_system.py"

  # Check inbox
  python3 AUTOMATIONS/agent/interagent.py inbox --for claude

API (via monitor at localhost:7777):
  POST /api/message  {"from":"claude","to":"kodex","body":"message"}
  GET  /api/messages  (returns last 20 messages)
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

PROJECT = Path("/Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt")
MESSAGE_BUS = PROJECT / "AUTOMATIONS" / "agent" / "message_bus.jsonl"
HANDOFF_DIR = PROJECT / "AUTOMATIONS" / "agent" / "handoffs"


def send_message(from_agent: str, to_agent: str, body: str, msg_type: str = "message"):
    """Append a message to the shared bus."""
    msg = {
        "ts": datetime.now().isoformat(),
        "from": from_agent,
        "to": to_agent,
        "type": msg_type,
        "body": body,
        "read": False
    }
    with open(MESSAGE_BUS, "a") as f:
        f.write(json.dumps(msg) + "\n")
    print(f"[{msg['ts'][:19]}] {from_agent} -> {to_agent}: {body[:80]}")
    return msg


def read_messages(for_agent: str = None, n: int = 20):
    """Read recent messages, optionally filtered by recipient."""
    if not MESSAGE_BUS.exists():
        return []
    lines = MESSAGE_BUS.read_text().strip().split("\n")
    msgs = []
    for line in lines[-200:]:
        try:
            m = json.loads(line)
            if for_agent and m.get("to") != for_agent:
                continue
            msgs.append(m)
        except Exception:
            pass
    return msgs[-n:]


def create_handoff(from_agent: str, to_agent: str, task: str, context: str = ""):
    """Create a structured task handoff between agents."""
    HANDOFF_DIR.mkdir(parents=True, exist_ok=True)

    handoff = {
        "ts": datetime.now().isoformat(),
        "from": from_agent,
        "to": to_agent,
        "task": task,
        "context": context,
        "status": "pending"
    }

    filename = f"handoff_{from_agent}_to_{to_agent}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    path = HANDOFF_DIR / filename
    path.write_text(json.dumps(handoff, indent=2))

    # Also post to message bus
    send_message(from_agent, to_agent, f"[HANDOFF] {task}", msg_type="handoff")

    print(f"Handoff created: {path.name}")
    return handoff


def get_inbox(for_agent: str):
    """Get unread messages and pending handoffs for an agent."""
    msgs = read_messages(for_agent=for_agent)
    unread = [m for m in msgs if not m.get("read")]

    # Check handoffs
    handoffs = []
    if HANDOFF_DIR.exists():
        for f in sorted(HANDOFF_DIR.glob(f"handoff_*_to_{for_agent}_*.json")):
            try:
                h = json.loads(f.read_text())
                if h.get("status") == "pending":
                    handoffs.append(h)
            except Exception:
                pass

    return {"unread_messages": unread, "pending_handoffs": handoffs}


def main():
    parser = argparse.ArgumentParser(description="PRINTMAXX Inter-Agent Comms")
    sub = parser.add_subparsers(dest="command")

    send_p = sub.add_parser("send")
    send_p.add_argument("--from", dest="from_agent", required=True)
    send_p.add_argument("--to", required=True)
    send_p.add_argument("--body", required=True)

    read_p = sub.add_parser("read")
    read_p.add_argument("--for", dest="for_agent", default=None)
    read_p.add_argument("--all", action="store_true")
    read_p.add_argument("-n", type=int, default=20)

    handoff_p = sub.add_parser("handoff")
    handoff_p.add_argument("--from", dest="from_agent", required=True)
    handoff_p.add_argument("--to", required=True)
    handoff_p.add_argument("--task", required=True)
    handoff_p.add_argument("--context", default="")

    inbox_p = sub.add_parser("inbox")
    inbox_p.add_argument("--for", dest="for_agent", required=True)

    args = parser.parse_args()

    if args.command == "send":
        send_message(args.from_agent, args.to, args.body)

    elif args.command == "read":
        agent = None if getattr(args, 'all', False) else args.for_agent
        msgs = read_messages(for_agent=agent, n=args.n)
        for m in msgs:
            ts = m.get("ts", "?")[:19]
            print(f"[{ts}] {m.get('from','?')} -> {m.get('to','?')}: {m.get('body','')}")
        if not msgs:
            print("No messages found.")

    elif args.command == "handoff":
        create_handoff(args.from_agent, args.to, args.task, args.context)

    elif args.command == "inbox":
        inbox = get_inbox(args.for_agent)
        print(f"\n=== INBOX for {args.for_agent} ===")
        print(f"Unread messages: {len(inbox['unread_messages'])}")
        for m in inbox['unread_messages']:
            print(f"  [{m.get('ts','?')[:19]}] {m.get('from','?')}: {m.get('body','')}")
        print(f"Pending handoffs: {len(inbox['pending_handoffs'])}")
        for h in inbox['pending_handoffs']:
            print(f"  [{h.get('ts','?')[:19]}] from {h.get('from','?')}: {h.get('task','')}")

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
