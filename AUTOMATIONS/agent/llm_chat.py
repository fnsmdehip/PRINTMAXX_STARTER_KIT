#!/usr/bin/env python3
"""
PRINTMAXX LLM Chat — iMessage-style multi-agent chat
=====================================================
Real-time chat between Claude Code, ChatGPT Codex, and Local LLM.
Both agents read/write directly to the shared bus file.

http://localhost:7770

No copy-pasting. Each agent just reads the bus file:
  - Claude Code: "check the chat for new messages"
  - ChatGPT Codex: "read AUTOMATIONS/agent/llm_chat_bus.jsonl and respond to the latest"
"""

import argparse
import json
import html as html_mod
import urllib.parse
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path

PROJECT = Path("/Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt")
BUS_FILE = PROJECT / "AUTOMATIONS" / "agent" / "llm_chat_bus.jsonl"

AGENTS = {
    "claude": {"name": "Claude Code", "color": "#a78bfa", "align": "right", "avatar": "C"},
    "codex":  {"name": "ChatGPT Codex", "color": "#74aa9c", "align": "left", "avatar": "G"},
    "local":  {"name": "Local LLM", "color": "#fbbf24", "align": "left", "avatar": "L"},
    "user":   {"name": "You", "color": "#f87171", "align": "center", "avatar": "U"},
}


def post(sender, body, recipient="all", meta=None):
    msg = {"ts": datetime.now().isoformat(), "from": sender, "to": recipient, "body": body}
    if meta:
        msg["meta"] = meta
    BUS_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(BUS_FILE, "a") as f:
        f.write(json.dumps(msg) + "\n")
    return msg


def get_messages(n=200):
    if not BUS_FILE.exists():
        return []
    msgs = []
    for line in BUS_FILE.read_text().strip().split("\n")[-n:]:
        try:
            msgs.append(json.loads(line))
        except Exception:
            pass
    return msgs


def get_new_messages(after_ts, for_agent=None):
    msgs = get_messages(200)
    new = []
    for m in msgs:
        if m["ts"] > after_ts:
            if for_agent is None or m["to"] in (for_agent, "all"):
                new.append(m)
    return new


CSS = """
* { margin:0; padding:0; box-sizing:border-box; }
body { background:#0a0a0a; color:#e4e4e7; font-family:-apple-system,'SF Pro',system-ui,sans-serif; height:100vh; display:flex; flex-direction:column; }

.topbar { background:#111; border-bottom:1px solid #222; padding:10px 16px; display:flex; align-items:center; gap:12px; flex-shrink:0; }
.topbar h1 { font-size:15px; color:#fff; font-weight:600; }
.topbar .agents { display:flex; gap:10px; margin-left:auto; }
.topbar .agent-pill { display:flex; align-items:center; gap:5px; padding:3px 10px; border-radius:12px; font-size:11px; border:1px solid #333; }
.topbar .agent-pill .dot { width:7px; height:7px; border-radius:50%; }

.chat-area { flex:1; overflow-y:auto; padding:16px; display:flex; flex-direction:column; gap:6px; }

.bubble-wrap { display:flex; flex-direction:column; max-width:75%; }
.bubble-wrap.right { align-self:flex-end; align-items:flex-end; }
.bubble-wrap.left { align-self:flex-start; align-items:flex-start; }
.bubble-wrap.center { align-self:center; align-items:center; }

.sender-label { font-size:10px; color:#666; margin-bottom:2px; padding:0 8px; }

.bubble { padding:8px 14px; border-radius:18px; font-size:13px; line-height:1.5; word-break:break-word; white-space:pre-wrap; max-width:100%; }
.bubble.right { background:#5b21b6; color:#f3f4f6; border-bottom-right-radius:4px; }
.bubble.left-codex { background:#1a3a2a; color:#d1fae5; border-bottom-left-radius:4px; }
.bubble.left-local { background:#422006; color:#fef3c7; border-bottom-left-radius:4px; }
.bubble.center { background:#1c1c1e; color:#999; font-style:italic; border-radius:12px; font-size:12px; }

.bubble-time { font-size:9px; color:#555; margin-top:2px; padding:0 8px; }

.bubble code { background:rgba(0,0,0,0.3); padding:1px 5px; border-radius:3px; font-family:'SF Mono',monospace; font-size:12px; }
.bubble pre { background:rgba(0,0,0,0.3); padding:8px; border-radius:6px; margin:4px 0; overflow-x:auto; font-family:'SF Mono',monospace; font-size:11px; }

.compose-bar { background:#111; border-top:1px solid #222; padding:10px 16px; display:flex; gap:8px; align-items:flex-end; flex-shrink:0; }
.compose-bar select { background:#1c1c1e; border:1px solid #333; color:#e4e4e7; padding:8px; border-radius:8px; font-size:12px; font-family:inherit; }
.compose-bar textarea { flex:1; background:#1c1c1e; border:1px solid #333; color:#e4e4e7; padding:8px 12px; border-radius:18px; font-size:13px; font-family:inherit; resize:none; min-height:38px; max-height:120px; line-height:1.4; }
.compose-bar textarea:focus { outline:none; border-color:#5b21b6; }
.compose-bar button { background:#5b21b6; color:white; border:none; width:38px; height:38px; border-radius:50%; cursor:pointer; font-size:16px; display:flex; align-items:center; justify-content:center; flex-shrink:0; }
.compose-bar button:hover { background:#6d28d9; }

.typing { padding:4px 16px; font-size:11px; color:#555; min-height:20px; flex-shrink:0; }

.day-divider { text-align:center; color:#444; font-size:11px; padding:12px 0 6px; }
"""

JS = """
let lastTs = "";
let pollInterval = null;

function scrollBottom() {
    const area = document.getElementById('chatArea');
    area.scrollTop = area.scrollHeight;
}

function poll() {
    fetch('/api/messages?after=' + encodeURIComponent(lastTs))
        .then(r => r.json())
        .then(msgs => {
            if (msgs.length > 0) {
                const area = document.getElementById('chatArea');
                const wasAtBottom = area.scrollHeight - area.scrollTop - area.clientHeight < 50;
                msgs.forEach(m => {
                    area.innerHTML += renderBubble(m);
                    lastTs = m.ts;
                });
                if (wasAtBottom) scrollBottom();
                updateTyping('');
            }
        })
        .catch(() => {});
}

function renderBubble(m) {
    const agents = {
        claude: {align:'right', cls:'right', label:'Claude Code'},
        codex: {align:'left', cls:'left-codex', label:'ChatGPT Codex'},
        local: {align:'left', cls:'left-local', label:'Local LLM'},
        user: {align:'center', cls:'center', label:'You'}
    };
    const a = agents[m.from] || agents.user;
    const time = m.ts ? m.ts.substring(11,16) : '';
    const body = escapeHtml(m.body);
    return `<div class="bubble-wrap ${a.align}">
        <div class="sender-label">${a.label}</div>
        <div class="bubble ${a.cls}">${body}</div>
        <div class="bubble-time">${time}</div>
    </div>`;
}

function escapeHtml(t) {
    const d = document.createElement('div');
    d.textContent = t;
    let s = d.innerHTML;
    // basic code block formatting
    s = s.replace(/```([\\s\\S]*?)```/g, '<pre>$1</pre>');
    s = s.replace(/`([^`]+)`/g, '<code>$1</code>');
    return s;
}

function sendMsg(e) {
    e.preventDefault();
    const body = document.getElementById('msgInput').value.trim();
    if (!body) return;
    const from = document.getElementById('fromSelect').value;
    fetch('/api/send', {
        method: 'POST',
        headers: {'Content-Type':'application/json'},
        body: JSON.stringify({from, to:'all', body})
    }).then(() => {
        document.getElementById('msgInput').value = '';
        document.getElementById('msgInput').style.height = '38px';
        poll();
    });
}

function updateTyping(text) {
    document.getElementById('typing').textContent = text;
}

function autoGrow(el) {
    el.style.height = '38px';
    el.style.height = Math.min(el.scrollHeight, 120) + 'px';
}

// handle enter to send, shift+enter for newline
document.addEventListener('DOMContentLoaded', () => {
    const input = document.getElementById('msgInput');
    input.addEventListener('keydown', e => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMsg(e);
        }
    });
    input.addEventListener('input', () => autoGrow(input));

    // init lastTs from existing messages
    const bubbles = document.querySelectorAll('.bubble-time');
    scrollBottom();

    // poll every 2s for new messages
    pollInterval = setInterval(poll, 2000);
});
"""


def render_chat():
    messages = get_messages(100)
    agent_pills = "".join(
        f'<div class="agent-pill"><div class="dot" style="background:{a["color"]}"></div>{a["name"]}</div>'
        for a in AGENTS.values()
    )
    agent_options = "".join(
        f'<option value="{k}">{v["name"]}</option>' for k, v in AGENTS.items()
    )

    bubble_html = ""
    last_ts = ""
    for m in messages:
        sender = m.get("from", "user")
        body = html_mod.escape(m.get("body", ""))
        ts = m.get("ts", "")
        time_str = ts[11:16] if len(ts) > 16 else ""
        last_ts = ts

        align_map = {"claude": "right", "codex": "left", "local": "left", "user": "center"}
        cls_map = {"claude": "right", "codex": "left-codex", "local": "left-local", "user": "center"}
        label_map = {"claude": "Claude Code", "codex": "ChatGPT Codex", "local": "Local LLM", "user": "You"}

        align = align_map.get(sender, "left")
        cls = cls_map.get(sender, "center")
        label = label_map.get(sender, sender)

        bubble_html += f'''<div class="bubble-wrap {align}">
            <div class="sender-label">{label}</div>
            <div class="bubble {cls}">{body}</div>
            <div class="bubble-time">{time_str}</div>
        </div>\n'''

    return f"""<!DOCTYPE html>
<html><head>
<meta charset="utf-8">
<title>LLM Chat</title>
<style>{CSS}</style>
</head><body>

<div class="topbar">
    <h1>LLM Chat</h1>
    <div class="agents">{agent_pills}</div>
</div>

<div class="chat-area" id="chatArea">
    {bubble_html}
</div>

<div class="typing" id="typing"></div>

<form class="compose-bar" onsubmit="sendMsg(event)">
    <select id="fromSelect">{agent_options}</select>
    <textarea id="msgInput" placeholder="Type a message..." rows="1"></textarea>
    <button type="submit">&#9654;</button>
</form>

<script>
let lastTs = "{last_ts}";
{JS}
</script>

</body></html>"""


class ChatHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            self._html(render_chat())
        elif self.path.startswith("/api/messages"):
            query = urllib.parse.urlparse(self.path).query
            params = urllib.parse.parse_qs(query)
            after = params.get("after", [""])[0]
            if after:
                msgs = get_new_messages(after)
            else:
                msgs = get_messages(100)
            self._json(msgs)
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        if self.path == "/api/send":
            length = int(self.headers.get("Content-Length", 0))
            data = json.loads(self.rfile.read(length).decode())
            msg = post(data.get("from", "user"), data.get("body", ""), data.get("to", "all"))
            self._json({"ok": True, "msg": msg})
        else:
            self.send_response(404)
            self.end_headers()

    def _html(self, content):
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(content.encode())

    def _json(self, data):
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

    def log_message(self, fmt, *args):
        pass


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=7770)
    args = parser.parse_args()

    BUS_FILE.parent.mkdir(parents=True, exist_ok=True)
    if not BUS_FILE.exists():
        BUS_FILE.touch()

    server = HTTPServer(("127.0.0.1", args.port), ChatHandler)
    print(f"LLM Chat at http://localhost:{args.port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped.")


if __name__ == "__main__":
    main()
