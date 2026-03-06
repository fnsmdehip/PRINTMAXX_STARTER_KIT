#!/usr/bin/env python3
"""
PRINTMAXX Agent Monitor — Live Dashboard
Open http://localhost:7777 in your browser.
Auto-refreshes every 30 seconds.

Usage:
  python3 AUTOMATIONS/agent/monitor.py          # Start on port 7777
  python3 AUTOMATIONS/agent/monitor.py --port 8080  # Custom port
"""

import argparse
import json
import os
import subprocess
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path

PROJECT = Path("/Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt")
STATE_FILE = PROJECT / "AUTOMATIONS" / "agent" / "state.json"
MISSION_LOG = PROJECT / "AUTOMATIONS" / "agent" / "missions.jsonl"
AGENT_LOG = PROJECT / "AUTOMATIONS" / "logs" / "agent.log"


def get_state():
    try:
        return json.loads(STATE_FILE.read_text())
    except Exception:
        return {}


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
    files = sorted(content_dir.glob("AGENT_CONTENT_*.md"), reverse=True)
    return files[:5]


def build_html():
    state = get_state()
    missions = get_recent_missions(25)
    log_text = get_agent_log(40)
    pids = is_daemon_running()
    disk = disk_free()
    content_files = get_content_files()

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

    # Mission results table
    mission_rows = ""
    result_icons = {"success": "&#9679;", "partial": "&#9681;", "failed": "&#9679;", "skipped": "&#9675;"}
    result_colors = {"success": "#4ade80", "partial": "#fbbf24", "failed": "#f87171", "skipped": "#94a3b8"}
    for name, result in state.get("last_mission_results", {}).items():
        icon = result_icons.get(result, "?")
        color = result_colors.get(result, "#fff")
        last_run = state.get("last_run_times", {}).get(name, "?")
        if last_run != "?":
            last_run = last_run[11:16]  # Just HH:MM
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

    # Latest content preview
    content_preview = ""
    if content_files:
        try:
            latest = content_files[0].read_text()[:1500]
            content_preview = latest.replace("<", "&lt;").replace(">", "&gt;").replace("\n", "<br>")
        except Exception:
            content_preview = "Error reading content"

    # Guardrails status
    guardrails_html = """
    <div class="card">
      <h2>Guardrails</h2>
      <table>
        <tr><td style="color:#4ade80">&#9679;</td><td>File ops locked to PRINTMAXX folder</td></tr>
        <tr><td style="color:#4ade80">&#9679;</td><td>Desktop, Downloads, Library BLOCKED</td></tr>
        <tr><td style="color:#4ade80">&#9679;</td><td>System dirs (/usr, /bin, /etc) BLOCKED</td></tr>
        <tr><td style="color:#4ade80">&#9679;</td><td>Dangerous commands (rm -rf /, dd, fork) BLOCKED</td></tr>
        <tr><td style="color:#4ade80">&#9679;</td><td>Scripts must be in AUTOMATIONS/ only</td></tr>
        <tr><td style="color:#4ade80">&#9679;</td><td>All subprocess timeouts enforced (max 5min)</td></tr>
        <tr><td style="color:#4ade80">&#9679;</td><td>Disk < 2GB = write missions paused</td></tr>
      </table>
    </div>
    """

    # Escaped log text
    safe_log = log_text.replace("<", "&lt;").replace(">", "&gt;")

    disk_color = "#4ade80" if disk > 10 else "#fbbf24" if disk > 3 else "#f87171"

    html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<meta http-equiv="refresh" content="30">
<title>PRINTMAXX Agent Monitor</title>
<style>
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  body {{ background: #0a0a0a; color: #e4e4e7; font-family: 'SF Mono', 'Fira Code', 'Consolas', monospace; font-size: 13px; padding: 20px; }}
  h1 {{ font-size: 20px; color: #fff; margin-bottom: 4px; }}
  h2 {{ font-size: 14px; color: #a1a1aa; margin-bottom: 10px; text-transform: uppercase; letter-spacing: 1px; }}
  .header {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; border-bottom: 1px solid #27272a; padding-bottom: 12px; }}
  .header-right {{ text-align: right; font-size: 12px; color: #71717a; }}
  .grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-bottom: 16px; }}
  .grid-3 {{ display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 16px; margin-bottom: 16px; }}
  .card {{ background: #18181b; border: 1px solid #27272a; border-radius: 8px; padding: 16px; }}
  .stat {{ text-align: center; }}
  .stat .value {{ font-size: 28px; font-weight: bold; color: #fff; }}
  .stat .label {{ font-size: 11px; color: #71717a; margin-top: 4px; text-transform: uppercase; }}
  .status-live {{ color: #4ade80; font-weight: bold; }}
  .status-dead {{ color: #f87171; font-weight: bold; animation: blink 1s infinite; }}
  @keyframes blink {{ 50% {{ opacity: 0.3; }} }}
  table {{ width: 100%; border-collapse: collapse; }}
  th {{ text-align: left; color: #71717a; font-size: 11px; text-transform: uppercase; padding: 6px 8px; border-bottom: 1px solid #27272a; }}
  td {{ padding: 5px 8px; border-bottom: 1px solid #1e1e21; font-size: 12px; }}
  tr:hover {{ background: #1e1e24; }}
  .log-box {{ background: #0f0f12; border: 1px solid #27272a; border-radius: 6px; padding: 12px; max-height: 300px; overflow-y: auto; white-space: pre-wrap; font-size: 11px; color: #a1a1aa; line-height: 1.6; }}
  .content-preview {{ background: #0f0f12; border: 1px solid #27272a; border-radius: 6px; padding: 12px; max-height: 400px; overflow-y: auto; font-size: 12px; color: #d4d4d8; line-height: 1.7; }}
  .controls {{ margin-bottom: 16px; }}
  .controls a {{ display: inline-block; background: #27272a; color: #e4e4e7; padding: 6px 14px; border-radius: 4px; text-decoration: none; margin-right: 8px; font-size: 12px; }}
  .controls a:hover {{ background: #3f3f46; }}
  .controls a.danger {{ background: #7f1d1d; }}
  .controls a.danger:hover {{ background: #991b1b; }}
</style>
</head>
<body>
  <div class="header">
    <div>
      <h1>PRINTMAXX Agent Monitor</h1>
      <span style="color:#71717a">autonomous business system</span>
    </div>
    <div class="header-right">
      {daemon_status}<br>
      Last refresh: {datetime.now().strftime('%H:%M:%S')}<br>
      Auto-refresh: 30s
    </div>
  </div>

  <div class="controls">
    <a href="/action/status">Refresh Status</a>
    <a href="/action/run-once">Run Cycle Now</a>
    <a href="/action/stop" class="danger">Stop Daemon</a>
  </div>

  <div class="grid-3">
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
  </div>

  <div class="grid-3">
    <div class="card stat">
      <div class="value">{state.get('missions_failed', 0)}</div>
      <div class="label">Missions Failed</div>
    </div>
    <div class="card stat">
      <div class="value">{last_cycle_display}</div>
      <div class="label">Last Cycle</div>
    </div>
    <div class="card stat">
      <div class="value">$0</div>
      <div class="label">Revenue</div>
    </div>
  </div>

  <div class="grid">
    <div class="card">
      <h2>Mission Status</h2>
      <table>
        <tr><th></th><th>Mission</th><th>Result</th><th>Last Run</th></tr>
        {mission_rows}
      </table>
    </div>
    {guardrails_html}
  </div>

  <div class="card" style="margin-bottom:16px">
    <h2>Mission Log (Recent)</h2>
    <table>
      <tr><th>Result</th><th>Time</th><th>Mission</th><th>Output</th><th>Dur</th></tr>
      {log_rows}
    </table>
  </div>

  <div class="grid">
    <div class="card">
      <h2>Agent Log (Last 40 Lines)</h2>
      <div class="log-box">{safe_log}</div>
    </div>
    <div class="card">
      <h2>Latest Content Generated</h2>
      <div class="content-preview">{content_preview if content_preview else '<em>No content generated yet</em>'}</div>
    </div>
  </div>

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
                    os.kill(int(pid), 15)  # SIGTERM
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

        elif self.path == "/api/state":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(get_state(), indent=2).encode())

        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, format, *args):
        pass  # Suppress HTTP logs


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=7777)
    args = parser.parse_args()

    server = HTTPServer(("127.0.0.1", args.port), MonitorHandler)
    print(f"PRINTMAXX Agent Monitor running at http://localhost:{args.port}")
    print("Press Ctrl+C to stop")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nMonitor stopped.")


if __name__ == "__main__":
    main()
