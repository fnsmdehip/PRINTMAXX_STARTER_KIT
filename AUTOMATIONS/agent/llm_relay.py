#!/usr/bin/env python3
"""
PRINTMAXX LLM Relay — Multi-Subscription Agent Communication Hub
=================================================================
Bridges Claude Code <-> ChatGPT Codex (and any other LLM agent).

How it works:
  1. Each agent posts messages to a shared JSONL bus
  2. Web UI at localhost:7770 shows the conversation + lets you relay manually
  3. Agents can request reviews, critiques, task handoffs, or collaborative builds
  4. You can paste Codex output into the relay and Claude reads it (and vice versa)

Message types:
  - task:     "Here's a task for you"
  - result:   "Here's my output"
  - critique: "Review this and improve it"
  - question: "I need input on X"
  - context:  "FYI, here's relevant info"

Usage:
  python3 AUTOMATIONS/agent/llm_relay.py                    # Start web UI
  python3 AUTOMATIONS/agent/llm_relay.py --port 7770        # Custom port
  python3 AUTOMATIONS/agent/llm_relay.py send --from claude --to codex --type task --body "Review this code"
  python3 AUTOMATIONS/agent/llm_relay.py inbox --for claude
  python3 AUTOMATIONS/agent/llm_relay.py history
"""

import argparse
import json
import os
import sys
import html as html_mod
import urllib.parse
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path

PROJECT = Path("/Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt")
BUS_FILE = PROJECT / "AUTOMATIONS" / "agent" / "llm_relay_bus.jsonl"
AGENTS = {
    "claude": {"name": "Claude Code (Opus)", "color": "#a78bfa", "sub": "Anthropic Max"},
    "codex": {"name": "ChatGPT Codex", "color": "#74aa9c", "sub": "OpenAI Plus/Pro"},
    "local": {"name": "Local LLM (LM Studio)", "color": "#fbbf24", "sub": "Eva Qwen2.5 32B"},
}
MSG_TYPES = ["task", "result", "critique", "question", "context"]


def append_message(from_agent, to_agent, msg_type, body, metadata=None):
    msg = {
        "ts": datetime.now().isoformat(),
        "from": from_agent,
        "to": to_agent,
        "type": msg_type,
        "body": body,
    }
    if metadata:
        msg["meta"] = metadata
    BUS_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(BUS_FILE, "a") as f:
        f.write(json.dumps(msg) + "\n")
    return msg


def read_messages(n=100, for_agent=None, msg_type=None):
    if not BUS_FILE.exists():
        return []
    lines = BUS_FILE.read_text().strip().split("\n")
    msgs = []
    for line in lines[-500:]:
        try:
            m = json.loads(line)
            if for_agent and m.get("to") != for_agent:
                continue
            if msg_type and m.get("type") != msg_type:
                continue
            msgs.append(m)
        except Exception:
            pass
    return msgs[-n:]


def build_relay_html():
    messages = read_messages(50)
    now = datetime.now().strftime("%H:%M:%S")

    msg_html = ""
    for m in messages:
        ts = m.get("ts", "?")[11:19]
        frm = m.get("from", "?")
        to = m.get("to", "?")
        mtype = m.get("type", "?")
        body = html_mod.escape(m.get("body", ""))
        frm_info = AGENTS.get(frm, {"name": frm, "color": "#888"})
        to_info = AGENTS.get(to, {"name": to, "color": "#888"})

        type_badge = {
            "task": "#f87171", "result": "#4ade80", "critique": "#fbbf24",
            "question": "#60a5fa", "context": "#a1a1aa"
        }.get(mtype, "#71717a")

        msg_html += f'''<div class="msg">
            <div class="msg-header">
                <span class="agent" style="color:{frm_info['color']}">{frm_info['name']}</span>
                <span class="arrow">-></span>
                <span class="agent" style="color:{to_info['color']}">{to_info['name']}</span>
                <span class="badge" style="background:{type_badge}">{mtype}</span>
                <span class="ts">{ts}</span>
            </div>
            <div class="msg-body">{body.replace(chr(10), "<br>")}</div>
        </div>'''

    agent_options = "".join(
        f'<option value="{k}">{v["name"]}</option>' for k, v in AGENTS.items()
    )
    type_options = "".join(
        f'<option value="{t}">{t}</option>' for t in MSG_TYPES
    )

    return f"""<!DOCTYPE html>
<html><head>
<meta charset="utf-8">
<title>PRINTMAXX LLM Relay</title>
<style>
  * {{ margin:0; padding:0; box-sizing:border-box; }}
  body {{ background:#0a0a0a; color:#e4e4e7; font-family:'SF Mono','Fira Code',monospace; font-size:13px; padding:16px; }}
  h1 {{ font-size:18px; color:#fff; margin-bottom:4px; }}
  .subtitle {{ color:#71717a; font-size:12px; margin-bottom:16px; }}
  .agents-bar {{ display:flex; gap:16px; margin-bottom:16px; padding:10px; background:#18181b; border:1px solid #27272a; border-radius:8px; }}
  .agent-card {{ display:flex; align-items:center; gap:8px; }}
  .agent-dot {{ width:10px; height:10px; border-radius:50%; }}
  .agent-name {{ font-size:12px; font-weight:bold; }}
  .agent-sub {{ font-size:10px; color:#71717a; }}

  .compose {{ background:#18181b; border:1px solid #27272a; border-radius:8px; padding:14px; margin-bottom:16px; }}
  .compose-row {{ display:flex; gap:8px; margin-bottom:8px; align-items:center; }}
  .compose select, .compose textarea, .compose button {{
    background:#0f0f12; border:1px solid #27272a; color:#e4e4e7; font-family:inherit; font-size:12px; border-radius:4px; padding:6px 10px;
  }}
  .compose textarea {{ width:100%; min-height:80px; resize:vertical; }}
  .compose button {{ background:#27272a; cursor:pointer; padding:8px 20px; }}
  .compose button:hover {{ background:#3f3f46; }}
  .compose label {{ font-size:11px; color:#71717a; min-width:40px; }}

  .messages {{ display:flex; flex-direction:column; gap:8px; max-height:60vh; overflow-y:auto; }}
  .msg {{ background:#18181b; border:1px solid #27272a; border-radius:8px; padding:10px 14px; }}
  .msg-header {{ display:flex; align-items:center; gap:8px; margin-bottom:6px; font-size:12px; }}
  .arrow {{ color:#52525b; }}
  .badge {{ padding:2px 8px; border-radius:3px; font-size:10px; color:#000; font-weight:bold; }}
  .ts {{ margin-left:auto; color:#52525b; font-size:11px; }}
  .msg-body {{ font-size:12px; line-height:1.6; color:#d4d4d8; white-space:pre-wrap; word-break:break-word; }}

  .quick-actions {{ display:flex; gap:6px; margin-bottom:16px; flex-wrap:wrap; }}
  .quick-actions button {{ background:#27272a; color:#e4e4e7; border:1px solid #3f3f46; padding:5px 12px; border-radius:4px; cursor:pointer; font-family:inherit; font-size:11px; }}
  .quick-actions button:hover {{ background:#3f3f46; }}

  .help {{ background:#18181b; border:1px solid #27272a; border-radius:8px; padding:12px; margin-top:16px; font-size:11px; color:#71717a; line-height:1.6; }}
</style>
</head><body>

<h1>PRINTMAXX LLM Relay</h1>
<div class="subtitle">Multi-subscription agent communication hub | {now} | {len(messages)} messages</div>

<div class="agents-bar">
    {"".join(f'<div class="agent-card"><div class="agent-dot" style="background:{v["color"]}"></div><div><div class="agent-name" style="color:{v["color"]}">{v["name"]}</div><div class="agent-sub">{v["sub"]}</div></div></div>' for v in AGENTS.values())}
</div>

<div class="compose">
    <form method="POST" action="/send">
        <div class="compose-row">
            <label>From:</label>
            <select name="from">{agent_options}</select>
            <label>To:</label>
            <select name="to">{"".join(f'<option value="{k}" {"selected" if k=="codex" else ""}>{v["name"]}</option>' for k,v in AGENTS.items())}</select>
            <label>Type:</label>
            <select name="type">{type_options}</select>
        </div>
        <textarea name="body" placeholder="Paste output, write a task, request a critique..."></textarea>
        <div class="compose-row" style="justify-content:flex-end;margin-top:8px">
            <button type="submit">Send Message</button>
        </div>
    </form>
</div>

<div class="quick-actions">
    <button onclick="quickSend('claude','codex','task','Review and improve the latest code I wrote. Check AUTOMATIONS/ for recent changes.')">Claude -> Codex: Review my code</button>
    <button onclick="quickSend('codex','claude','result','[PASTE CODEX OUTPUT HERE]')">Codex -> Claude: Paste result</button>
    <button onclick="quickSend('claude','codex','critique','Look at this approach and tell me what could be better. Be specific.')">Claude -> Codex: Critique request</button>
    <button onclick="quickSend('codex','claude','task','[PASTE CODEX TASK HERE]')">Codex -> Claude: Send task</button>
    <button onclick="quickSend('claude','local','task','Generate content for the findom venture. Check CONTENT/_LOCAL_LLM_QUARANTINE/ for format.')">Claude -> Local LLM: Content gen</button>
</div>

<div class="messages">
    {msg_html if msg_html else '<div style="color:#52525b;text-align:center;padding:40px">No messages yet. Send one above or use the CLI.</div>'}
</div>

<div class="help">
    <strong>How to use this:</strong><br>
    1. Give Claude Code a task. It produces output.<br>
    2. Copy the interesting parts, paste into relay as "claude -> codex: result"<br>
    3. Open ChatGPT Codex. Tell it: "Read the latest message in AUTOMATIONS/agent/llm_relay_bus.jsonl and respond"<br>
    4. Codex produces output. Paste back here as "codex -> claude: result"<br>
    5. Tell Claude Code: "Read the latest codex message in AUTOMATIONS/agent/llm_relay_bus.jsonl"<br>
    <br>
    <strong>CLI:</strong><br>
    python3 AUTOMATIONS/agent/llm_relay.py send --from claude --to codex --type task --body "..."<br>
    python3 AUTOMATIONS/agent/llm_relay.py inbox --for claude<br>
    python3 AUTOMATIONS/agent/llm_relay.py history<br>
    <br>
    <strong>For Claude Code to auto-read:</strong> Just say "check the relay for new messages from codex"<br>
    <strong>For Codex to auto-read:</strong> Tell it to read llm_relay_bus.jsonl in the project
</div>

<script>
function quickSend(from, to, type, body) {{
    const form = document.querySelector('form');
    form.querySelector('[name=from]').value = from;
    form.querySelector('[name=to]').value = to;
    form.querySelector('[name=type]').value = type;
    form.querySelector('textarea').value = body;
    form.querySelector('textarea').focus();
}}
</script>

</body></html>"""


class RelayHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/" or self.path.startswith("/relay"):
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(build_relay_html().encode())
        elif self.path == "/api/messages":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps(read_messages(50), indent=2).encode())
        elif self.path.startswith("/api/inbox"):
            query = urllib.parse.urlparse(self.path).query
            params = urllib.parse.parse_qs(query)
            agent = params.get("for", ["claude"])[0]
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(read_messages(20, for_agent=agent), indent=2).encode())
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        if self.path == "/send":
            content_length = int(self.headers.get("Content-Length", 0))
            raw = self.rfile.read(content_length).decode()
            params = urllib.parse.parse_qs(raw)
            frm = params.get("from", ["claude"])[0]
            to = params.get("to", ["codex"])[0]
            mtype = params.get("type", ["task"])[0]
            body = params.get("body", [""])[0]
            if body.strip():
                append_message(frm, to, mtype, body.strip())
            self.send_response(302)
            self.send_header("Location", "/")
            self.end_headers()
        elif self.path == "/api/send":
            content_length = int(self.headers.get("Content-Length", 0))
            raw = self.rfile.read(content_length).decode()
            try:
                data = json.loads(raw)
                msg = append_message(
                    data.get("from", "unknown"),
                    data.get("to", "unknown"),
                    data.get("type", "context"),
                    data.get("body", ""),
                    data.get("meta")
                )
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"ok": True, "msg": msg}).encode())
            except Exception as e:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(str(e).encode())
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, fmt, *args):
        pass


def cli_send(args):
    msg = append_message(args.from_agent, args.to, args.type, args.body)
    print(f"Sent: {msg['from']} -> {msg['to']} [{msg['type']}]: {msg['body'][:80]}")


def cli_inbox(args):
    msgs = read_messages(20, for_agent=args.for_agent)
    if not msgs:
        print(f"No messages for {args.for_agent}")
        return
    for m in msgs:
        ts = m["ts"][11:19]
        print(f"[{ts}] {m['from']} [{m['type']}]: {m['body'][:120]}")


def cli_history(args):
    msgs = read_messages(args.n)
    for m in msgs:
        ts = m["ts"][11:19]
        print(f"[{ts}] {m['from']} -> {m['to']} [{m['type']}]: {m['body'][:120]}")


def main():
    parser = argparse.ArgumentParser(description="PRINTMAXX LLM Relay")
    sub = parser.add_subparsers(dest="command")

    # Web server (default)
    parser.add_argument("--port", type=int, default=7770)

    # Send
    send_p = sub.add_parser("send")
    send_p.add_argument("--from", dest="from_agent", required=True)
    send_p.add_argument("--to", required=True)
    send_p.add_argument("--type", default="task", choices=MSG_TYPES)
    send_p.add_argument("--body", required=True)

    # Inbox
    inbox_p = sub.add_parser("inbox")
    inbox_p.add_argument("--for", dest="for_agent", required=True)

    # History
    hist_p = sub.add_parser("history")
    hist_p.add_argument("-n", type=int, default=30)

    args = parser.parse_args()

    if args.command == "send":
        cli_send(args)
    elif args.command == "inbox":
        cli_inbox(args)
    elif args.command == "history":
        cli_history(args)
    else:
        # Start web UI
        BUS_FILE.parent.mkdir(parents=True, exist_ok=True)
        if not BUS_FILE.exists():
            BUS_FILE.touch()
        server = HTTPServer(("127.0.0.1", args.port), RelayHandler)
        print(f"LLM Relay running at http://localhost:{args.port}")
        print("Ctrl+C to stop")
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            print("\nRelay stopped.")


if __name__ == "__main__":
    main()
