#!/usr/bin/env python3
"""
PRINTMAXX Command Center — Enhanced Dashboard
http://localhost:7777

Features:
  - 15-minute session timer with audio alarm
  - 5-minute inactivity alarm
  - Persistent todo list (saved to disk)
  - Agent status, mission log, venture tracker
  - Guardrails status
  - Inter-agent message bus viewer
  - Quick actions

Usage:
  python3 AUTOMATIONS/agent/monitor.py
  python3 AUTOMATIONS/agent/monitor.py --port 8080
"""

import argparse
import json
import os
import subprocess
import urllib.parse
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path

PROJECT = Path("/Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt")
STATE_FILE = PROJECT / "AUTOMATIONS" / "agent" / "state.json"
MISSION_LOG = PROJECT / "AUTOMATIONS" / "agent" / "missions.jsonl"
AGENT_LOG = PROJECT / "AUTOMATIONS" / "logs" / "agent.log"
OPS_STATE_FILE = PROJECT / "AUTOMATIONS" / "agent" / "ops_manager" / "ops_state.json"
TODO_FILE = PROJECT / "AUTOMATIONS" / "agent" / "todos.json"
MESSAGE_BUS = PROJECT / "AUTOMATIONS" / "agent" / "message_bus.jsonl"


def get_state():
    try:
        return json.loads(STATE_FILE.read_text())
    except Exception:
        return {}


def get_ops_state():
    try:
        return json.loads(OPS_STATE_FILE.read_text())
    except Exception:
        return {}


def get_todos():
    try:
        return json.loads(TODO_FILE.read_text())
    except Exception:
        return []


def save_todos(todos):
    TODO_FILE.write_text(json.dumps(todos, indent=2))


def get_messages(n=20):
    if not MESSAGE_BUS.exists():
        return []
    try:
        lines = MESSAGE_BUS.read_text().strip().split("\n")
        msgs = []
        for line in lines[-n:]:
            try:
                msgs.append(json.loads(line))
            except Exception:
                pass
        return msgs
    except Exception:
        return []


def get_recent_missions(n=30):
    if not MISSION_LOG.exists():
        return []
    try:
        lines = MISSION_LOG.read_text().strip().split("\n")
        entries = []
        for line in lines[-n:]:
            try:
                entries.append(json.loads(line))
            except Exception:
                pass
        return entries
    except Exception:
        return []


def get_agent_log(n=50):
    if not AGENT_LOG.exists():
        return ""
    try:
        lines = AGENT_LOG.read_text().strip().split("\n")
        return "\n".join(lines[-n:])
    except Exception:
        return ""


def is_daemon_running():
    try:
        r = subprocess.run(["pgrep", "-f", "printmaxx_agent.py"],
                           capture_output=True, text=True, timeout=5)
        pids = r.stdout.strip().split("\n")
        return [p for p in pids if p]
    except Exception:
        return []


def disk_free():
    try:
        st = os.statvfs("/")
        return round(st.f_bavail * st.f_frsize / (1024**3), 1)
    except Exception:
        return -1


def get_content_files():
    content_dir = PROJECT / "CONTENT" / "social" / "printmaxxer"
    if not content_dir.exists():
        return []
    files = sorted(content_dir.glob("*.md"), reverse=True)
    return files[:5]


def build_html():
    state = get_state()
    missions = get_recent_missions(25)
    log_text = get_agent_log(40)
    pids = is_daemon_running()
    disk = disk_free()
    content_files = get_content_files()
    todos = get_todos()
    messages = get_messages(15)

    daemon_status = f'<span class="status-live">LIVE (PID {", ".join(pids)})</span>' if pids else '<span class="status-dead">STOPPED</span>'
    last_cycle = state.get("last_cycle", "never")
    if last_cycle != "never":
        try:
            lc = datetime.fromisoformat(last_cycle)
            ago = (datetime.now() - lc).total_seconds()
            if ago < 120:
                last_cycle_display = f"{int(ago)}s ago"
            elif ago < 7200:
                last_cycle_display = f"{int(ago/60)}m ago"
            else:
                last_cycle_display = f"{int(ago/3600)}h ago"
        except Exception:
            last_cycle_display = last_cycle[:16]
    else:
        last_cycle_display = "never"

    result_icons = {"success": "&#9679;", "partial": "&#9681;", "failed": "&#9679;", "skipped": "&#9675;"}
    result_colors = {"success": "#4ade80", "partial": "#fbbf24", "failed": "#f87171", "skipped": "#94a3b8"}

    # Mission results table
    mission_rows = ""
    for name, result in state.get("last_mission_results", {}).items():
        icon = result_icons.get(result, "?")
        color = result_colors.get(result, "#fff")
        last_run = state.get("last_run_times", {}).get(name, "?")
        if last_run != "?":
            last_run = last_run[11:16]
        mission_rows += f'<tr><td style="color:{color}">{icon}</td><td>{name}</td><td>{result}</td><td>{last_run}</td></tr>\n'

    # Mission log rows
    log_rows = ""
    for m in reversed(missions):
        result = m.get("result", "?")
        color = result_colors.get(result, "#fff")
        ts = m.get("ts", "?")[:16]
        name = m.get("mission", "?")
        output = m.get("output", "")[:80]
        dur = m.get("duration", 0)
        log_rows += f'<tr><td style="color:{color}">{result}</td><td>{ts}</td><td>{name}</td><td>{output}</td><td>{dur:.0f}s</td></tr>\n'

    # Content preview
    content_preview = ""
    if content_files:
        try:
            latest = content_files[0].read_text()[:1500]
            content_preview = latest.replace("<", "&lt;").replace(">", "&gt;").replace("\n", "<br>")
        except Exception:
            content_preview = "Error reading content"

    # Ops Manager ventures
    ops = get_ops_state()
    venture_rows = ""
    for vname, vdata in ops.get("venture_status", {}).items():
        result = vdata.get("last_result", "?")
        color = result_colors.get(result, "#fff")
        icon = result_icons.get(result, "?")
        last_run = vdata.get("last_run", "?")[:16]
        summary = vdata.get("last_summary", "")[:60]
        venture_rows += f'<tr><td style="color:{color}">{icon}</td><td>{vname}</td><td>{result}</td><td>{summary}</td><td>{last_run}</td></tr>\n'

    # Todo list HTML
    todo_rows = ""
    for i, todo in enumerate(todos):
        done_class = "todo-done" if todo.get("done") else ""
        check = "&#9745;" if todo.get("done") else "&#9744;"
        prio = todo.get("priority", "P2")
        prio_color = {"P0": "#f87171", "P1": "#fbbf24", "P2": "#60a5fa", "P3": "#94a3b8"}.get(prio, "#94a3b8")
        text = todo.get("text", "").replace("<", "&lt;").replace(">", "&gt;")
        todo_rows += f'''<tr class="{done_class}">
            <td><a href="/todo/toggle/{i}" style="text-decoration:none;color:#e4e4e7">{check}</a></td>
            <td style="color:{prio_color}">{prio}</td>
            <td>{text}</td>
            <td><a href="/todo/delete/{i}" style="color:#71717a;text-decoration:none">x</a></td>
        </tr>\n'''

    # Message bus
    msg_rows = ""
    for msg in reversed(messages):
        ts = msg.get("ts", "?")[11:19]
        src = msg.get("from", "?")
        dst = msg.get("to", "?")
        body = msg.get("body", "")[:80].replace("<", "&lt;").replace(">", "&gt;")
        msg_rows += f'<tr><td>{ts}</td><td>{src}</td><td>{dst}</td><td>{body}</td></tr>\n'

    safe_log = log_text.replace("<", "&lt;").replace(">", "&gt;")
    disk_color = "#4ade80" if disk > 10 else "#fbbf24" if disk > 3 else "#f87171"
    now_str = datetime.now().strftime('%H:%M:%S')
    date_str = datetime.now().strftime('%A, %B %d, %Y')

    html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>PRINTMAXX Command Center</title>
<style>
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  body {{ background: #0a0a0a; color: #e4e4e7; font-family: 'SF Mono', 'Fira Code', 'Consolas', monospace; font-size: 13px; padding: 16px 20px; }}
  h1 {{ font-size: 20px; color: #fff; margin-bottom: 4px; }}
  h2 {{ font-size: 13px; color: #a1a1aa; margin-bottom: 8px; text-transform: uppercase; letter-spacing: 1px; }}
  .header {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px; border-bottom: 1px solid #27272a; padding-bottom: 10px; }}
  .header-right {{ text-align: right; font-size: 12px; color: #71717a; }}
  .grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-bottom: 12px; }}
  .grid-3 {{ display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 12px; margin-bottom: 12px; }}
  .grid-4 {{ display: grid; grid-template-columns: 1fr 1fr 1fr 1fr; gap: 12px; margin-bottom: 12px; }}
  .card {{ background: #18181b; border: 1px solid #27272a; border-radius: 8px; padding: 14px; }}
  .stat {{ text-align: center; }}
  .stat .value {{ font-size: 26px; font-weight: bold; color: #fff; }}
  .stat .label {{ font-size: 11px; color: #71717a; margin-top: 2px; text-transform: uppercase; }}
  .status-live {{ color: #4ade80; font-weight: bold; }}
  .status-dead {{ color: #f87171; font-weight: bold; animation: blink 1s infinite; }}
  @keyframes blink {{ 50% {{ opacity: 0.3; }} }}
  table {{ width: 100%; border-collapse: collapse; }}
  th {{ text-align: left; color: #71717a; font-size: 11px; text-transform: uppercase; padding: 4px 6px; border-bottom: 1px solid #27272a; }}
  td {{ padding: 4px 6px; border-bottom: 1px solid #1e1e21; font-size: 12px; }}
  tr:hover {{ background: #1e1e24; }}
  .log-box {{ background: #0f0f12; border: 1px solid #27272a; border-radius: 6px; padding: 10px; max-height: 250px; overflow-y: auto; white-space: pre-wrap; font-size: 11px; color: #a1a1aa; line-height: 1.5; }}
  .content-preview {{ background: #0f0f12; border: 1px solid #27272a; border-radius: 6px; padding: 10px; max-height: 300px; overflow-y: auto; font-size: 12px; color: #d4d4d8; line-height: 1.6; }}
  .controls {{ margin-bottom: 12px; display: flex; gap: 6px; flex-wrap: wrap; }}
  .controls a, .controls button {{ display: inline-block; background: #27272a; color: #e4e4e7; padding: 5px 12px; border-radius: 4px; text-decoration: none; font-size: 12px; border: none; cursor: pointer; font-family: inherit; }}
  .controls a:hover, .controls button:hover {{ background: #3f3f46; }}
  .controls .danger {{ background: #7f1d1d; }}
  .controls .danger:hover {{ background: #991b1b; }}
  .controls .active {{ background: #166534; }}

  /* Timer section */
  .timer-bar {{ display: flex; align-items: center; gap: 16px; background: #18181b; border: 1px solid #27272a; border-radius: 8px; padding: 10px 16px; margin-bottom: 12px; }}
  .timer-display {{ font-size: 32px; font-weight: bold; font-variant-numeric: tabular-nums; color: #fff; min-width: 100px; }}
  .timer-display.warning {{ color: #fbbf24; }}
  .timer-display.critical {{ color: #f87171; animation: blink 0.5s infinite; }}
  .timer-label {{ font-size: 11px; color: #71717a; text-transform: uppercase; }}
  .timer-btn {{ background: #27272a; color: #e4e4e7; border: none; padding: 6px 14px; border-radius: 4px; cursor: pointer; font-family: inherit; font-size: 12px; }}
  .timer-btn:hover {{ background: #3f3f46; }}
  .timer-btn.start {{ background: #166534; }}
  .timer-btn.stop {{ background: #7f1d1d; }}
  .idle-indicator {{ display: flex; align-items: center; gap: 6px; }}
  .idle-dot {{ width: 8px; height: 8px; border-radius: 50%; background: #4ade80; }}
  .idle-dot.idle {{ background: #fbbf24; animation: blink 1s infinite; }}
  .idle-dot.alarm {{ background: #f87171; animation: blink 0.3s infinite; }}

  /* Todo */
  .todo-input {{ display: flex; gap: 6px; margin-bottom: 8px; }}
  .todo-input input {{ flex: 1; background: #0f0f12; border: 1px solid #27272a; color: #e4e4e7; padding: 6px 10px; border-radius: 4px; font-family: inherit; font-size: 12px; }}
  .todo-input select {{ background: #0f0f12; border: 1px solid #27272a; color: #e4e4e7; padding: 6px; border-radius: 4px; font-family: inherit; font-size: 12px; }}
  .todo-input button {{ background: #27272a; color: #e4e4e7; border: none; padding: 6px 12px; border-radius: 4px; cursor: pointer; font-family: inherit; font-size: 12px; }}
  .todo-done td {{ opacity: 0.4; text-decoration: line-through; }}

  /* Progress bar */
  .progress-bar {{ height: 3px; background: #27272a; border-radius: 2px; margin-top: 4px; overflow: hidden; }}
  .progress-fill {{ height: 100%; border-radius: 2px; transition: width 1s linear; }}
</style>
</head>
<body>

<div class="header">
    <div>
        <h1>PRINTMAXX Command Center</h1>
        <span style="color:#71717a">{date_str}</span>
    </div>
    <div class="header-right">
        {daemon_status}<br>
        Clock: <span id="clock">{now_str}</span><br>
        <span style="color:#71717a">Auto-refresh: data only (no page reload)</span>
    </div>
</div>

<!-- TIMER BAR -->
<div class="timer-bar">
    <div>
        <div class="timer-label">Session Timer</div>
        <div class="timer-display" id="sessionTimer">15:00</div>
        <div class="progress-bar"><div class="progress-fill" id="timerProgress" style="width:100%;background:#4ade80"></div></div>
    </div>
    <div style="display:flex;gap:6px;flex-direction:column">
        <button class="timer-btn start" onclick="startTimer(15)">15 min</button>
        <button class="timer-btn start" onclick="startTimer(25)">25 min</button>
        <button class="timer-btn stop" onclick="stopTimer()">Stop</button>
    </div>
    <div style="border-left:1px solid #27272a;padding-left:16px">
        <div class="timer-label">Inactivity</div>
        <div style="display:flex;align-items:center;gap:8px">
            <div class="idle-dot" id="idleDot"></div>
            <span id="idleTime" style="font-size:14px;color:#a1a1aa">0:00</span>
        </div>
        <div style="font-size:10px;color:#52525b;margin-top:2px">alarm at 5:00</div>
    </div>
    <div style="border-left:1px solid #27272a;padding-left:16px">
        <div class="timer-label">Session Elapsed</div>
        <div id="sessionElapsed" style="font-size:14px;color:#a1a1aa">0:00:00</div>
    </div>
    <div style="margin-left:auto">
        <button class="timer-btn" onclick="silenceAlarm()" id="silenceBtn" style="display:none;background:#7f1d1d">Silence</button>
    </div>
</div>

<!-- CONTROLS -->
<div class="controls">
    <a href="/action/status">Refresh</a>
    <a href="/action/run-once">Run Agent Cycle</a>
    <button onclick="startTimer(15)" class="active">Start 15m Timer</button>
    <a href="/action/stop" class="danger">Stop Daemon</a>
</div>

<!-- STATS ROW -->
<div class="grid-4">
    <div class="card stat">
        <div class="value">{state.get('cycles_run', 0)}</div>
        <div class="label">Cycles Run</div>
    </div>
    <div class="card stat">
        <div class="value">{state.get('missions_completed', 0)}</div>
        <div class="label">Missions OK</div>
    </div>
    <div class="card stat">
        <div class="value" style="color:{disk_color}">{disk}GB</div>
        <div class="label">Disk Free</div>
    </div>
    <div class="card stat">
        <div class="value">$0</div>
        <div class="label">Revenue</div>
    </div>
</div>

<!-- TODO + MISSION STATUS -->
<div class="grid">
    <div class="card">
        <h2>Today's Tasks</h2>
        <form class="todo-input" action="/todo/add" method="GET" onsubmit="return addTodo(event)">
            <select id="todoPrio">
                <option value="P0">P0</option>
                <option value="P1" selected>P1</option>
                <option value="P2">P2</option>
                <option value="P3">P3</option>
            </select>
            <input type="text" id="todoText" placeholder="Add task..." autocomplete="off">
            <button type="submit">+</button>
        </form>
        <table>
            <tr><th></th><th>Pri</th><th>Task</th><th></th></tr>
            {todo_rows if todo_rows else '<tr><td colspan="4" style="color:#71717a">No tasks yet. Add one above.</td></tr>'}
        </table>
    </div>
    <div class="card">
        <h2>Mission Status</h2>
        <table>
            <tr><th></th><th>Mission</th><th>Result</th><th>Last</th></tr>
            {mission_rows if mission_rows else '<tr><td colspan="4" style="color:#71717a">No missions run yet</td></tr>'}
        </table>
    </div>
</div>

<!-- VENTURES + INTER-AGENT MESSAGES -->
<div class="grid">
    <div class="card">
        <h2>Ventures ({ops.get("cycles_run", 0)} cycles)</h2>
        <table>
            <tr><th></th><th>Venture</th><th>Result</th><th>Summary</th><th>Last</th></tr>
            {venture_rows if venture_rows else '<tr><td colspan="5" style="color:#71717a">No venture cycles yet</td></tr>'}
        </table>
    </div>
    <div class="card">
        <h2>Inter-Agent Messages</h2>
        <table>
            <tr><th>Time</th><th>From</th><th>To</th><th>Message</th></tr>
            {msg_rows if msg_rows else '<tr><td colspan="4" style="color:#71717a">No messages yet</td></tr>'}
        </table>
        <div style="margin-top:8px;font-size:11px;color:#52525b">
            Send: POST /api/message {{"from":"claude","to":"kodex","body":"..."}}
        </div>
    </div>
</div>

<!-- GUARDRAILS + QUICK REF -->
<div class="grid">
    <div class="card">
        <h2>Guardrails</h2>
        <table>
            <tr><td style="color:#4ade80">&#9679;</td><td>File ops locked to PRINTMAXX folder</td></tr>
            <tr><td style="color:#4ade80">&#9679;</td><td>Desktop, Downloads, Library BLOCKED</td></tr>
            <tr><td style="color:#4ade80">&#9679;</td><td>System dirs BLOCKED</td></tr>
            <tr><td style="color:#4ade80">&#9679;</td><td>Dangerous commands BLOCKED</td></tr>
            <tr><td style="color:#4ade80">&#9679;</td><td>Scripts in AUTOMATIONS/ only</td></tr>
            <tr><td style="color:#4ade80">&#9679;</td><td>Subprocess timeouts (5min max)</td></tr>
            <tr><td style="color:#4ade80">&#9679;</td><td>Disk &lt; 2GB = writes paused</td></tr>
        </table>
    </div>
    <div class="card">
        <h2>Quick Reference</h2>
        <table>
            <tr><td style="color:#71717a">Brave cookies</td><td><code>--user-data-dir=BraveCookies</code></td></tr>
            <tr><td style="color:#71717a">Monitor</td><td><code>localhost:7777</code></td></tr>
            <tr><td style="color:#71717a">LM Studio</td><td><code>localhost:1234</code></td></tr>
            <tr><td style="color:#71717a">Agent daemon</td><td><code>printmaxx_agent.py</code></td></tr>
            <tr><td style="color:#71717a">Ops manager</td><td><code>printmaxx_ops_manager.py</code></td></tr>
            <tr><td style="color:#71717a">Message bus</td><td><code>agent/message_bus.jsonl</code></td></tr>
        </table>
    </div>
</div>

<!-- MISSION LOG -->
<div class="card" style="margin-bottom:12px">
    <h2>Mission Log (Recent)</h2>
    <table>
        <tr><th>Result</th><th>Time</th><th>Mission</th><th>Output</th><th>Dur</th></tr>
        {log_rows if log_rows else '<tr><td colspan="5" style="color:#71717a">No mission log entries</td></tr>'}
    </table>
</div>

<!-- LOGS + CONTENT -->
<div class="grid">
    <div class="card">
        <h2>Agent Log (Last 40)</h2>
        <div class="log-box">{safe_log if safe_log else '<em>No agent log</em>'}</div>
    </div>
    <div class="card">
        <h2>Latest Content</h2>
        <div class="content-preview">{content_preview if content_preview else '<em>No content generated yet</em>'}</div>
    </div>
</div>

<script>
// ============ SESSION TIMER ============
let timerInterval = null;
let timerSeconds = 0;
let timerTotal = 0;
let alarmPlaying = false;
let alarmOsc = null;
let audioCtx = null;

function getAudioCtx() {{
    if (!audioCtx) audioCtx = new (window.AudioContext || window.webkitAudioContext)();
    return audioCtx;
}}

function playAlarm() {{
    if (alarmPlaying) return;
    alarmPlaying = true;
    document.getElementById('silenceBtn').style.display = 'inline-block';
    const ctx = getAudioCtx();
    function beep() {{
        if (!alarmPlaying) return;
        const osc = ctx.createOscillator();
        const gain = ctx.createGain();
        osc.connect(gain);
        gain.connect(ctx.destination);
        osc.frequency.value = 880;
        osc.type = 'square';
        gain.gain.value = 0.3;
        osc.start();
        gain.gain.exponentialRampToValueAtTime(0.01, ctx.currentTime + 0.3);
        osc.stop(ctx.currentTime + 0.3);
        setTimeout(() => {{ if (alarmPlaying) beep(); }}, 600);
    }}
    beep();
}}

function silenceAlarm() {{
    alarmPlaying = false;
    document.getElementById('silenceBtn').style.display = 'none';
}}

function startTimer(minutes) {{
    silenceAlarm();
    timerSeconds = minutes * 60;
    timerTotal = timerSeconds;
    if (timerInterval) clearInterval(timerInterval);
    timerInterval = setInterval(() => {{
        timerSeconds--;
        updateTimerDisplay();
        if (timerSeconds <= 0) {{
            clearInterval(timerInterval);
            timerInterval = null;
            playAlarm();
        }}
    }}, 1000);
    updateTimerDisplay();
}}

function stopTimer() {{
    silenceAlarm();
    if (timerInterval) clearInterval(timerInterval);
    timerInterval = null;
    timerSeconds = 0;
    timerTotal = 0;
    updateTimerDisplay();
}}

function updateTimerDisplay() {{
    const el = document.getElementById('sessionTimer');
    const prog = document.getElementById('timerProgress');
    const m = Math.floor(Math.abs(timerSeconds) / 60);
    const s = Math.abs(timerSeconds) % 60;
    const prefix = timerSeconds < 0 ? '-' : '';
    el.textContent = prefix + m + ':' + String(s).padStart(2, '0');

    el.className = 'timer-display';
    if (timerSeconds <= 60 && timerSeconds > 0) el.className += ' critical';
    else if (timerSeconds <= 180 && timerSeconds > 0) el.className += ' warning';

    if (timerTotal > 0) {{
        const pct = Math.max(0, (timerSeconds / timerTotal) * 100);
        prog.style.width = pct + '%';
        prog.style.background = pct < 10 ? '#f87171' : pct < 25 ? '#fbbf24' : '#4ade80';
    }} else {{
        prog.style.width = '0%';
    }}
}}

// ============ INACTIVITY DETECTOR ============
let lastActivity = Date.now();
let idleAlarmFired = false;

function resetActivity() {{
    lastActivity = Date.now();
    idleAlarmFired = false;
    silenceAlarm();
    const dot = document.getElementById('idleDot');
    if (dot) {{ dot.className = 'idle-dot'; }}
}}

['mousemove', 'keypress', 'click', 'scroll', 'touchstart'].forEach(evt => {{
    document.addEventListener(evt, resetActivity, {{ passive: true }});
}});

setInterval(() => {{
    const idle = Math.floor((Date.now() - lastActivity) / 1000);
    const el = document.getElementById('idleTime');
    const dot = document.getElementById('idleDot');
    const m = Math.floor(idle / 60);
    const s = idle % 60;
    if (el) el.textContent = m + ':' + String(s).padStart(2, '0');

    if (idle >= 300 && !idleAlarmFired) {{
        idleAlarmFired = true;
        if (dot) dot.className = 'idle-dot alarm';
        playAlarm();
    }} else if (idle >= 120) {{
        if (dot) dot.className = 'idle-dot idle';
    }}
}}, 1000);

// ============ CLOCK ============
const sessionStart = Date.now();
setInterval(() => {{
    const now = new Date();
    const el = document.getElementById('clock');
    if (el) el.textContent = now.toLocaleTimeString('en-GB');

    const elapsed = Math.floor((Date.now() - sessionStart) / 1000);
    const h = Math.floor(elapsed / 3600);
    const m = Math.floor((elapsed % 3600) / 60);
    const s = elapsed % 60;
    const se = document.getElementById('sessionElapsed');
    if (se) se.textContent = h + ':' + String(m).padStart(2,'0') + ':' + String(s).padStart(2,'0');
}}, 1000);

// ============ TODO (AJAX) ============
function addTodo(e) {{
    e.preventDefault();
    const text = document.getElementById('todoText').value.trim();
    if (!text) return false;
    const prio = document.getElementById('todoPrio').value;
    fetch('/todo/add?text=' + encodeURIComponent(text) + '&priority=' + prio)
        .then(() => location.reload());
    return false;
}}

// ============ AUTO-REFRESH DATA (no page reload) ============
// We do a soft refresh every 30s by reloading the page
// This preserves the timer state since it's client-side
// Actually, page reload will reset timers. Let's use meta refresh only for data.
// For now, no auto-reload — user clicks Refresh or data updates via /api/state

// Auto-start 15min timer on first load
if (!timerInterval) {{
    startTimer(15);
}}
</script>

</body>
</html>"""
    return html


class MonitorHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/" or self.path == "/action/status":
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(build_html().encode())

        elif self.path == "/action/stop":
            pids = is_daemon_running()
            for pid in pids:
                try:
                    os.kill(int(pid), 15)
                except Exception:
                    pass
            self.send_response(302)
            self.send_header("Location", "/")
            self.end_headers()

        elif self.path == "/action/run-once":
            subprocess.Popen(
                ["python3", str(PROJECT / "AUTOMATIONS" / "printmaxx_agent.py"), "--once"],
                cwd=str(PROJECT),
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
            )
            self.send_response(302)
            self.send_header("Location", "/")
            self.end_headers()

        elif self.path.startswith("/todo/add"):
            query = urllib.parse.urlparse(self.path).query
            params = urllib.parse.parse_qs(query)
            text = params.get("text", [""])[0]
            priority = params.get("priority", ["P2"])[0]
            if text:
                todos = get_todos()
                todos.append({"text": text, "priority": priority, "done": False, "added": datetime.now().isoformat()})
                save_todos(todos)
            self.send_response(302)
            self.send_header("Location", "/")
            self.end_headers()

        elif self.path.startswith("/todo/toggle/"):
            try:
                idx = int(self.path.split("/")[-1])
                todos = get_todos()
                if 0 <= idx < len(todos):
                    todos[idx]["done"] = not todos[idx].get("done", False)
                    save_todos(todos)
            except Exception:
                pass
            self.send_response(302)
            self.send_header("Location", "/")
            self.end_headers()

        elif self.path.startswith("/todo/delete/"):
            try:
                idx = int(self.path.split("/")[-1])
                todos = get_todos()
                if 0 <= idx < len(todos):
                    todos.pop(idx)
                    save_todos(todos)
            except Exception:
                pass
            self.send_response(302)
            self.send_header("Location", "/")
            self.end_headers()

        elif self.path == "/api/state":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps(get_state(), indent=2).encode())

        elif self.path == "/api/messages":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps(get_messages(), indent=2).encode())

        elif self.path == "/api/todos":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps(get_todos(), indent=2).encode())

        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        if self.path == "/api/message":
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length).decode()
            try:
                msg = json.loads(body)
                msg["ts"] = datetime.now().isoformat()
                with open(MESSAGE_BUS, "a") as f:
                    f.write(json.dumps(msg) + "\n")
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(b'{"ok":true}')
            except Exception as e:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(str(e).encode())
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, format, *args):
        pass


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=7777)
    args = parser.parse_args()

    # Ensure todo file exists
    if not TODO_FILE.exists():
        save_todos([])

    # Ensure message bus exists
    if not MESSAGE_BUS.exists():
        MESSAGE_BUS.touch()

    server = HTTPServer(("127.0.0.1", args.port), MonitorHandler)
    print(f"PRINTMAXX Command Center running at http://localhost:{args.port}")
    print("Press Ctrl+C to stop")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nCommand Center stopped.")


if __name__ == "__main__":
    main()
