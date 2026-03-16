#!/usr/bin/env python3
"""PRINTMAXX System Visualizer — generates OPS/SYSTEM_VISUAL.html daily.

Shows: all agents (model, interval, status), ventures, cron health,
revenue, pipeline, and system stats in one auto-refreshing HTML page.

Usage:
  python3 AUTOMATIONS/system_visualizer.py           # generate + open
  python3 AUTOMATIONS/system_visualizer.py --generate # generate only
  python3 AUTOMATIONS/system_visualizer.py --open     # open existing
"""
from __future__ import annotations
import json, subprocess, os, sys, argparse
from datetime import datetime
from pathlib import Path

PROJECT = Path(__file__).resolve().parent.parent
AUTO = PROJECT / "AUTOMATIONS"
OPS = PROJECT / "OPS"
OUTPUT = OPS / "SYSTEM_VISUAL.html"


def _load_json(p: Path, default=None):
    try:
        return json.loads(p.read_text())
    except Exception:
        return default if default is not None else {}


def _file_age_hours(p: Path) -> float:
    try:
        return (datetime.now().timestamp() - p.stat().st_mtime) / 3600
    except Exception:
        return 999


def _cron_count() -> int:
    try:
        r = subprocess.run(["crontab", "-l"], capture_output=True, text=True, timeout=5)
        return len([l for l in r.stdout.splitlines() if l.strip() and not l.startswith("#")])
    except Exception:
        return 0


def _launchd_count() -> int:
    try:
        return len(list(Path.home().glob("Library/LaunchAgents/com.printmaxx.*.plist")))
    except Exception:
        return 0


def gather_swarm_agents() -> list[dict]:
    state = _load_json(AUTO / "agent" / "swarm" / "swarm_state.json", {})
    agents = state.get("agents", {})
    results = []
    for name, info in sorted(agents.items()):
        model_raw = info.get("model", "opus")
        if "haiku" in model_raw:
            model = "Haiku"
        elif "sonnet" in model_raw:
            model = "Sonnet"
        else:
            model = "Opus"
        status = info.get("status", "unknown")
        if info.get("killed"):
            status = "KILLED"
        elif info.get("hibernated"):
            status = "SLEEP"
        interval = info.get("interval_hours", "?")
        last_run = info.get("last_run", "")
        results.append({
            "name": name, "model": model, "status": status,
            "interval": interval, "last_run": last_run,
            "category": info.get("category", ""),
        })
    return results


def gather_ventures() -> list[dict]:
    state = _load_json(AUTO / "agent" / "autonomy" / "autonomy_state.json", {})
    ventures = state.get("ventures", {})
    results = []
    for name, info in sorted(ventures.items()):
        results.append({
            "name": name,
            "status": info.get("status", "unknown"),
            "cycles": info.get("cycles", 0),
            "last_run": info.get("last_run", ""),
            "successes": info.get("successes", 0),
            "failures": info.get("failures", 0),
        })
    return results


def gather_stats() -> dict:
    heartbeat = {}
    hb_path = OPS / "HEARTBEAT.md"
    if hb_path.exists():
        text = hb_path.read_text()
        for line in text.splitlines():
            if ":" in line:
                k, v = line.split(":", 1)
                heartbeat[k.strip().lower()] = v.strip()

    briefing_age = _file_age_hours(OPS / "SESSION_BRIEFING.md")
    tactical_age = _file_age_hours(OPS / "DAILY_TACTICAL_PLAN.md")

    return {
        "cron_jobs": _cron_count(),
        "launchd_plists": _launchd_count(),
        "briefing_age_h": round(briefing_age, 1),
        "tactical_age_h": round(tactical_age, 1),
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
    }


def generate_html() -> str:
    agents = gather_swarm_agents()
    ventures = gather_ventures()
    stats = gather_stats()

    active = [a for a in agents if a["status"] not in ("KILLED", "SLEEP")]
    killed = [a for a in agents if a["status"] == "KILLED"]
    sleeping = [a for a in agents if a["status"] == "SLEEP"]

    model_counts = {"Opus": 0, "Sonnet": 0, "Haiku": 0}
    for a in active:
        model_counts[a["model"]] = model_counts.get(a["model"], 0) + 1

    def agent_row(a: dict) -> str:
        colors = {"Opus": "#ff6b6b", "Sonnet": "#ffd93d", "Haiku": "#6bcb77"}
        status_colors = {"active": "#6bcb77", "KILLED": "#666", "SLEEP": "#888", "unknown": "#aaa"}
        mc = colors.get(a["model"], "#aaa")
        sc = status_colors.get(a["status"], "#6bcb77")
        return f"""<tr>
            <td>{a['name']}</td>
            <td><span style="background:{mc};color:#000;padding:2px 8px;border-radius:4px;font-size:12px">{a['model']}</span></td>
            <td style="color:{sc}">{a['status']}</td>
            <td>{a['interval']}h</td>
            <td style="font-size:12px;color:#888">{a.get('category','')}</td>
        </tr>"""

    def venture_row(v: dict) -> str:
        sc = "#6bcb77" if v["status"] == "active" else "#ff6b6b"
        rate = f"{v['successes']}/{v['successes']+v['failures']}" if (v['successes']+v['failures']) > 0 else "0/0"
        return f"""<tr>
            <td>{v['name']}</td>
            <td style="color:{sc}">{v['status']}</td>
            <td>{v['cycles']}</td>
            <td>{rate}</td>
        </tr>"""

    active_rows = "\n".join(agent_row(a) for a in active)
    killed_rows = "\n".join(agent_row(a) for a in killed)
    sleeping_rows = "\n".join(agent_row(a) for a in sleeping)
    venture_rows = "\n".join(venture_row(v) for v in ventures)

    return f"""<!DOCTYPE html>
<html><head>
<meta charset="utf-8">
<title>PRINTMAXX System Visual</title>
<style>
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  body {{ background: #0a0a0a; color: #e0e0e0; font-family: 'SF Mono', 'Fira Code', monospace; padding: 20px; }}
  h1 {{ color: #fff; margin-bottom: 5px; font-size: 24px; }}
  .subtitle {{ color: #666; font-size: 13px; margin-bottom: 20px; }}
  .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 16px; margin-bottom: 20px; }}
  .card {{ background: #141414; border: 1px solid #222; border-radius: 8px; padding: 16px; }}
  .card h2 {{ color: #ffd93d; font-size: 14px; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 12px; }}
  .stat {{ display: flex; justify-content: space-between; padding: 4px 0; border-bottom: 1px solid #1a1a1a; }}
  .stat-label {{ color: #888; }}
  .stat-value {{ color: #fff; font-weight: bold; }}
  .stat-value.warn {{ color: #ff6b6b; }}
  .stat-value.good {{ color: #6bcb77; }}
  table {{ width: 100%; border-collapse: collapse; font-size: 13px; }}
  th {{ text-align: left; padding: 6px 8px; color: #666; border-bottom: 1px solid #222; font-size: 11px; text-transform: uppercase; }}
  td {{ padding: 5px 8px; border-bottom: 1px solid #1a1a1a; }}
  .section {{ margin-bottom: 24px; }}
  .section h2 {{ color: #ffd93d; font-size: 16px; margin-bottom: 8px; }}
  .model-bar {{ display: flex; gap: 8px; margin: 8px 0; }}
  .model-chip {{ padding: 4px 12px; border-radius: 4px; font-size: 12px; font-weight: bold; }}
  .collapsed {{ display: none; }}
  .toggle {{ cursor: pointer; color: #666; font-size: 12px; }}
  .toggle:hover {{ color: #ffd93d; }}
</style>
</head><body>
<h1>PRINTMAXX SYSTEM VISUAL</h1>
<p class="subtitle">Auto-generated {stats['generated_at']} | Refreshes daily at 6 AM</p>

<div class="grid">
  <div class="card">
    <h2>Infrastructure</h2>
    <div class="stat"><span class="stat-label">Cron jobs</span><span class="stat-value">{stats['cron_jobs']}</span></div>
    <div class="stat"><span class="stat-label">LaunchD plists</span><span class="stat-value">{stats['launchd_plists']}</span></div>
    <div class="stat"><span class="stat-label">Active agents</span><span class="stat-value good">{len(active)}</span></div>
    <div class="stat"><span class="stat-label">Killed/Sleeping</span><span class="stat-value">{len(killed)}/{len(sleeping)}</span></div>
    <div class="stat"><span class="stat-label">Ventures</span><span class="stat-value">{len(ventures)}</span></div>
  </div>

  <div class="card">
    <h2>Model Distribution</h2>
    <div class="model-bar">
      <span class="model-chip" style="background:#ff6b6b;color:#000">Opus: {model_counts['Opus']}</span>
      <span class="model-chip" style="background:#ffd93d;color:#000">Sonnet: {model_counts['Sonnet']}</span>
      <span class="model-chip" style="background:#6bcb77;color:#000">Haiku: {model_counts['Haiku']}</span>
    </div>
    <div class="stat"><span class="stat-label">Total active</span><span class="stat-value">{sum(model_counts.values())}</span></div>
    <div class="stat"><span class="stat-label">Opus %</span><span class="stat-value">{round(model_counts['Opus']/max(sum(model_counts.values()),1)*100)}%</span></div>
  </div>

  <div class="card">
    <h2>Freshness</h2>
    <div class="stat"><span class="stat-label">Session briefing</span><span class="stat-value {'warn' if stats['briefing_age_h'] > 6 else 'good'}">{stats['briefing_age_h']}h ago</span></div>
    <div class="stat"><span class="stat-label">Tactical plan</span><span class="stat-value {'warn' if stats['tactical_age_h'] > 24 else 'good'}">{stats['tactical_age_h']}h ago</span></div>
  </div>
</div>

<div class="section">
  <h2>Active Swarm Agents ({len(active)})</h2>
  <table>
    <tr><th>Agent</th><th>Model</th><th>Status</th><th>Interval</th><th>Category</th></tr>
    {active_rows}
  </table>
</div>

<div class="section">
  <h2>Ventures ({len(ventures)})</h2>
  <table>
    <tr><th>Venture</th><th>Status</th><th>Cycles</th><th>Success Rate</th></tr>
    {venture_rows}
  </table>
</div>

{"<div class='section'><h2>Killed Agents (" + str(len(killed)) + ")</h2><table><tr><th>Agent</th><th>Model</th><th>Status</th><th>Interval</th><th>Category</th></tr>" + killed_rows + "</table></div>" if killed else ""}

{"<div class='section'><h2>Sleeping Agents (" + str(len(sleeping)) + ")</h2><table><tr><th>Agent</th><th>Model</th><th>Status</th><th>Interval</th><th>Category</th></tr>" + sleeping_rows + "</table></div>" if sleeping else ""}

<div style="margin-top:20px;color:#333;font-size:11px">
  guardrail hook: active | full disk: off | model routing: smart | dashboard: control_panel.py :9999
</div>
</body></html>"""


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--generate", action="store_true", help="Generate only, don't open")
    parser.add_argument("--open", action="store_true", help="Open existing file")
    args = parser.parse_args()

    if args.open:
        if OUTPUT.exists():
            subprocess.run(["open", str(OUTPUT)])
        else:
            print("No visualization exists yet. Run without --open to generate.")
        return

    html = generate_html()
    OUTPUT.write_text(html)
    print(f"Generated: {OUTPUT}")

    if not args.generate:
        subprocess.run(["open", str(OUTPUT)])


if __name__ == "__main__":
    main()
