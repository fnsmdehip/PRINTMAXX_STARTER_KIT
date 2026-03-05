#!/usr/bin/env python3
"""
PRINTMAXX Operations Web Dashboard
====================================
Zero-dependency Python web dashboard for monitoring and triggering operations.
Uses only stdlib (http.server + json). Dark theme, auto-refresh, trigger buttons.

Usage:
  python3 ops_web_dashboard.py                # Start on port 8080
  python3 ops_web_dashboard.py --port 9090    # Custom port
  python3 ops_web_dashboard.py --no-open      # Don't auto-open browser
"""

import json
import subprocess
import sys
import os
import csv
import html
from datetime import datetime
from pathlib import Path
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

# Import semantic search API
try:
    from semantic_memory_search import api_search, build_index as rebuild_search_index
    SEARCH_AVAILABLE = True
except ImportError:
    SEARCH_AVAILABLE = False

BASE = Path(__file__).resolve().parent.parent
AUTO = BASE / "AUTOMATIONS"
OPS = BASE / "OPS"
LEDGER = BASE / "LEDGER"
LOGS = AUTO / "logs"


def safe_text(val):
    """Escape text for safe insertion into HTML."""
    if val is None:
        return ""
    return html.escape(str(val))


def read_file_safe(path, max_lines=50):
    try:
        lines = Path(path).read_text(errors="replace").strip().split("\n")
        return lines[:max_lines]
    except Exception:
        return []


def read_csv_safe(path, max_rows=100):
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            reader = csv.DictReader(f)
            rows = []
            for i, row in enumerate(reader):
                if i >= max_rows:
                    break
                rows.append(row)
            return rows
    except Exception:
        return []


def read_json_safe(path):
    try:
        return json.loads(Path(path).read_text())
    except Exception:
        return None


def read_jsonl_tail(path, n=10):
    entries = []
    try:
        with open(path, "r") as f:
            for line in f:
                line = line.strip()
                if line:
                    try:
                        entries.append(json.loads(line))
                    except json.JSONDecodeError:
                        pass
    except Exception:
        pass
    return entries[-n:]


def gather_system_state():
    """Collect all system metrics for the dashboard."""
    state = {}

    # Heartbeat
    hb_lines = read_file_safe(OPS / "HEARTBEAT.md", 30)
    state["heartbeat"] = "\n".join(hb_lines) if hb_lines else "No heartbeat data"

    # Active tasks
    at_lines = read_file_safe(OPS / "active-tasks.md", 30)
    state["active_tasks"] = "\n".join(at_lines) if at_lines else "No active tasks"

    # Rebalancer latest
    rebal = read_json_safe(LOGS / "rebalance_latest.json")
    if rebal and isinstance(rebal, list):
        state["rebalancer"] = rebal[:15]
    else:
        state["rebalancer"] = []

    # Rebalance history (last 7)
    state["rebalance_history"] = read_jsonl_tail(LOGS / "rebalance_history.jsonl", 7)

    # Checkpoint pending
    cp_dir = OPS / "checkpoints" / "pending"
    pending = []
    if cp_dir.exists():
        for f in sorted(cp_dir.glob("*.md")):
            pending.append({"name": f.name, "size": f.stat().st_size})
    state["checkpoints_pending"] = pending

    # Session checkpoint (resume info)
    ckpt = read_json_safe(LOGS / "session_checkpoint.json")
    state["session_checkpoint"] = ckpt

    # Overnight logs (latest)
    today = datetime.now().strftime("%Y-%m-%d")
    overnight_log = LOGS / f"overnight_{today}.log"
    if overnight_log.exists():
        lines = read_file_safe(overnight_log, 20)
        state["overnight_log"] = "\n".join(lines)
    else:
        state["overnight_log"] = "No overnight log for today"

    # Lead pipeline
    hot_path = AUTO / "leads" / "qualified" / "HOT_LEADS_QUALIFIED.csv"
    if hot_path.exists():
        try:
            with open(hot_path, "r") as f:
                state["hot_leads_count"] = sum(1 for _ in f) - 1
        except Exception:
            state["hot_leads_count"] = 0
    else:
        state["hot_leads_count"] = 0

    # Pipeline metrics
    state["pipeline_metrics"] = read_jsonl_tail(
        AUTO / "leads" / "qualified" / "pipeline_metrics.jsonl", 5
    )

    # Cron status
    try:
        result = subprocess.run(
            ["crontab", "-l"], capture_output=True, text=True, timeout=5
        )
        cron_lines = [
            l for l in result.stdout.strip().split("\n")
            if l.strip() and not l.startswith("#")
        ]
        state["cron_jobs"] = len(cron_lines)
    except Exception:
        state["cron_jobs"] = 0

    # Disk usage
    try:
        result = subprocess.run(
            ["du", "-sh", str(BASE)], capture_output=True, text=True, timeout=10
        )
        state["disk_usage"] = result.stdout.strip().split("\t")[0] if result.stdout else "?"
    except Exception:
        state["disk_usage"] = "?"

    # Revenue
    rev_path = LEDGER / "REVENUE_TRACKER.csv"
    state["revenue"] = "$0"
    if rev_path.exists():
        rows = read_csv_safe(rev_path)
        total = 0
        for r in rows:
            try:
                total += float(r.get("amount", "0").replace("$", "").replace(",", ""))
            except (ValueError, TypeError):
                pass
        if total > 0:
            state["revenue"] = f"${total:,.2f}"

    # Alpha staging count
    alpha_path = LEDGER / "ALPHA_STAGING.csv"
    if alpha_path.exists():
        try:
            with open(alpha_path, "r") as f:
                state["alpha_count"] = sum(1 for _ in f) - 1
        except Exception:
            state["alpha_count"] = 0
    else:
        state["alpha_count"] = 0

    state["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return state


# Operations that can be triggered
OPS_COMMANDS = {
    "heartbeat": {
        "label": "Refresh Heartbeat",
        "cmd": [sys.executable, str(AUTO / "memory_manager.py"), "--heartbeat"],
    },
    "memory_full": {
        "label": "Full Memory Refresh",
        "cmd": [sys.executable, str(AUTO / "memory_manager.py"), "--full"],
    },
    "rebalancer": {
        "label": "Run Rebalancer",
        "cmd": [sys.executable, str(AUTO / "auto_rebalancer.py"), "--check"],
    },
    "orchestrator_status": {
        "label": "Orchestrator Status",
        "cmd": [sys.executable, str(AUTO / "autonomous_orchestrator.py"), "--status"],
    },
    "venture_scores": {
        "label": "Venture Scores",
        "cmd": [sys.executable, str(AUTO / "venture_performance_tracker.py"), "--recommend"],
    },
    "checkpoints": {
        "label": "Checkpoint Status",
        "cmd": [sys.executable, str(AUTO / "checkpoint_manager.py"), "--status"],
    },
    "saas_scan": {
        "label": "SaaS Scanner",
        "cmd": [sys.executable, str(AUTO / "saas_product_scanner.py"), "--scan"],
    },
    "system_health": {
        "label": "System Health",
        "cmd": [sys.executable, str(AUTO / "system_health_monitor.py"), "--quick"],
    },
    "plan_morning": {
        "label": "Plan Morning Session",
        "cmd": [sys.executable, str(AUTO / "autonomous_orchestrator.py"), "--plan", "morning"],
    },
    "plan_midday": {
        "label": "Plan Midday Session",
        "cmd": [sys.executable, str(AUTO / "autonomous_orchestrator.py"), "--plan", "midday"],
    },
    "plan_evening": {
        "label": "Plan Evening Session",
        "cmd": [sys.executable, str(AUTO / "autonomous_orchestrator.py"), "--plan", "evening"],
    },
    "rebuild_search_index": {
        "label": "Rebuild Search Index",
        "cmd": [sys.executable, str(AUTO / "semantic_memory_search.py"), "--index"],
    },
}


def build_html_page():
    """Build the dashboard HTML using safe string construction (no innerHTML)."""
    # All dynamic content is inserted via textContent in JS, not innerHTML
    return """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>PRINTMAXX Ops Dashboard</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{background:#0a0e17;color:#c8d6e5;font-family:'SF Mono','Fira Code',monospace;font-size:13px}
.header{background:#111827;border-bottom:1px solid #1e3a5f;padding:12px 20px;display:flex;justify-content:space-between;align-items:center}
.header h1{color:#00ff88;font-size:16px;letter-spacing:2px}
.header .ts{color:#6b7280;font-size:11px}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(340px,1fr));gap:12px;padding:12px}
.card{background:#111827;border:1px solid #1e3a5f;border-radius:6px;padding:14px;min-height:120px}
.card h2{color:#00ff88;font-size:12px;text-transform:uppercase;letter-spacing:1px;margin-bottom:10px;border-bottom:1px solid #1e3a5f;padding-bottom:6px}
.card pre{white-space:pre-wrap;word-break:break-word;font-size:11px;color:#9ca3af;max-height:300px;overflow-y:auto}
.btn-row{display:flex;flex-wrap:wrap;gap:6px;padding:12px 20px}
.btn{background:#1e3a5f;color:#00ff88;border:1px solid #00ff88;border-radius:4px;padding:6px 12px;cursor:pointer;font-family:inherit;font-size:11px;transition:background 0.15s}
.btn:hover{background:#00ff88;color:#0a0e17}
.btn:disabled{opacity:0.4;cursor:not-allowed}
.btn-plan{border-color:#60a5fa;color:#60a5fa}
.btn-plan:hover{background:#60a5fa;color:#0a0e17}
.btn-analysis{border-color:#f59e0b;color:#f59e0b}
.btn-analysis:hover{background:#f59e0b;color:#0a0e17}
.score-row{display:flex;justify-content:space-between;padding:2px 0;border-bottom:1px solid #1a2332}
.score-name{color:#c8d6e5;flex:1}
.score-val{width:40px;text-align:right;font-weight:bold}
.score-action{width:100px;text-align:right;font-size:10px}
.kill{color:#ef4444}.reduce{color:#f59e0b}.maintain{color:#6b7280}.double{color:#00ff88}
.stat{display:inline-block;background:#1a2332;border-radius:4px;padding:4px 8px;margin:2px;font-size:11px}
.stat .label{color:#6b7280}.stat .value{color:#00ff88;font-weight:bold}
.output-box{background:#0d1117;border:1px solid #1e3a5f;border-radius:4px;padding:10px;margin-top:8px;max-height:400px;overflow-y:auto;font-size:11px;color:#9ca3af;white-space:pre-wrap;display:none}
.checkpoint-item{background:#1a2332;border-radius:4px;padding:6px 8px;margin:4px 0;font-size:11px}
.checkpoint-item .name{color:#f59e0b}
.refreshing{animation:pulse 1s infinite}
@keyframes pulse{0%,100%{opacity:1}50%{opacity:0.5}}
</style>
</head>
<body>

<div class="header">
  <h1>PRINTMAXX OPS</h1>
  <span class="ts" id="timestamp">Loading...</span>
</div>

<div class="btn-row">
  <strong style="color:#6b7280;font-size:11px;padding:6px 4px">PLAN:</strong>
  <button class="btn btn-plan" onclick="runOp('plan_morning')">Morning</button>
  <button class="btn btn-plan" onclick="runOp('plan_midday')">Midday</button>
  <button class="btn btn-plan" onclick="runOp('plan_evening')">Evening</button>
  <strong style="color:#6b7280;font-size:11px;padding:6px 12px">EXECUTE:</strong>
  <button class="btn" onclick="runOp('heartbeat')">Heartbeat</button>
  <button class="btn" onclick="runOp('memory_full')">Memory Full</button>
  <button class="btn" onclick="runOp('checkpoints')">Checkpoints</button>
  <strong style="color:#6b7280;font-size:11px;padding:6px 12px">ANALYSIS:</strong>
  <button class="btn btn-analysis" onclick="runOp('rebalancer')">Rebalancer</button>
  <button class="btn btn-analysis" onclick="runOp('venture_scores')">Ventures</button>
  <button class="btn btn-analysis" onclick="runOp('saas_scan')">SaaS Scan</button>
  <button class="btn btn-analysis" onclick="runOp('system_health')">Health</button>
  <button class="btn btn-analysis" onclick="runOp('orchestrator_status')">Orchestrator</button>
  <button class="btn" onclick="runOp('rebuild_search_index')" style="margin-left:12px;border-color:#a78bfa;color:#a78bfa" onmouseover="this.style.background='#a78bfa';this.style.color='#0a0e17'" onmouseout="this.style.background='';this.style.color='#a78bfa'">Rebuild Index</button>
</div>

<div style="padding:4px 20px 8px;display:flex;gap:6px;align-items:center">
  <input id="search-input" type="text" placeholder="Search memory (learnings, orchestrator, signals, pipeline...)"
    style="flex:1;background:#111827;border:1px solid #1e3a5f;border-radius:4px;padding:6px 10px;color:#c8d6e5;font-family:inherit;font-size:12px;outline:none"
    onkeydown="if(event.key==='Enter')doSearch()">
  <select id="search-cat" style="background:#111827;border:1px solid #1e3a5f;border-radius:4px;padding:6px 8px;color:#a78bfa;font-family:inherit;font-size:11px">
    <option value="">All categories</option>
    <option value="learnings">Learnings</option>
    <option value="orchestrator">Orchestrator</option>
    <option value="signals">Signals</option>
    <option value="pipeline">Pipeline</option>
    <option value="brain">Brain</option>
    <option value="rebalancer">Rebalancer</option>
    <option value="tasks">Tasks</option>
    <option value="cold_email">Cold Email</option>
    <option value="scraper">Scraper</option>
    <option value="alerts">Alerts</option>
    <option value="heartbeat">Heartbeat</option>
  </select>
  <button class="btn" onclick="doSearch()" style="border-color:#a78bfa;color:#a78bfa" onmouseover="this.style.background='#a78bfa';this.style.color='#0a0e17'" onmouseout="this.style.background='';this.style.color='#a78bfa'">Search</button>
</div>

<div id="search-results" class="output-box" style="margin:0 20px;display:none"></div>
<div id="op-output" class="output-box" style="margin:0 20px"></div>

<div class="grid" id="dashboard-grid">
  <!-- Cards are built by JS using safe DOM methods -->
</div>

<script>
// Build a card element safely using DOM methods (no innerHTML)
function makeCard(title, contentFn) {
  var card = document.createElement('div');
  card.className = 'card';
  var h2 = document.createElement('h2');
  h2.textContent = title;
  card.appendChild(h2);
  contentFn(card);
  return card;
}

function addPre(parent, text) {
  var pre = document.createElement('pre');
  pre.textContent = text || 'No data';
  parent.appendChild(pre);
}

function addStat(parent, label, value) {
  var span = document.createElement('span');
  span.className = 'stat';
  var lb = document.createElement('span');
  lb.className = 'label';
  lb.textContent = label + ': ';
  var vl = document.createElement('span');
  vl.className = 'value';
  vl.textContent = value;
  span.appendChild(lb);
  span.appendChild(vl);
  parent.appendChild(span);
}

function addScoreRow(parent, name, score, action) {
  var row = document.createElement('div');
  row.className = 'score-row';

  var nameEl = document.createElement('span');
  nameEl.className = 'score-name';
  nameEl.textContent = name;

  var scoreEl = document.createElement('span');
  scoreEl.className = 'score-val';
  var cls = 'maintain';
  if (action === 'KILL') cls = 'kill';
  else if (action === 'REDUCE') cls = 'reduce';
  else if (action === 'DOUBLE_DOWN') cls = 'double';
  scoreEl.className = 'score-val ' + cls;
  scoreEl.textContent = score;

  var actEl = document.createElement('span');
  actEl.className = 'score-action ' + cls;
  actEl.textContent = action;

  row.appendChild(nameEl);
  row.appendChild(scoreEl);
  row.appendChild(actEl);
  parent.appendChild(row);
}

function renderDashboard(data) {
  var grid = document.getElementById('dashboard-grid');
  // Clear existing cards
  while (grid.firstChild) grid.removeChild(grid.firstChild);

  document.getElementById('timestamp').textContent = 'Updated: ' + data.timestamp;

  // System Overview
  grid.appendChild(makeCard('System Overview', function(card) {
    addStat(card, 'Revenue', data.revenue || '$0');
    addStat(card, 'Hot Leads', String(data.hot_leads_count || 0));
    addStat(card, 'Alpha Entries', String(data.alpha_count || 0));
    addStat(card, 'Cron Jobs', String(data.cron_jobs || 0));
    addStat(card, 'Disk', data.disk_usage || '?');
    addStat(card, 'Checkpoints', String((data.checkpoints_pending || []).length));
  }));

  // Heartbeat
  grid.appendChild(makeCard('Heartbeat', function(card) {
    addPre(card, data.heartbeat);
  }));

  // Active Tasks
  grid.appendChild(makeCard('Active Tasks', function(card) {
    addPre(card, data.active_tasks);
  }));

  // Rebalancer Scores
  grid.appendChild(makeCard('Rebalancer (Top 15)', function(card) {
    var items = data.rebalancer || [];
    if (items.length === 0) {
      addPre(card, 'No rebalancer data. Run --check first.');
      return;
    }
    for (var i = 0; i < items.length; i++) {
      var r = items[i];
      addScoreRow(card, r.method || '?', r.score || 0, r.action || 'MAINTAIN');
    }
  }));

  // Rebalance History
  grid.appendChild(makeCard('Rebalance History', function(card) {
    var hist = data.rebalance_history || [];
    if (hist.length === 0) {
      addPre(card, 'No history yet.');
      return;
    }
    for (var i = 0; i < hist.length; i++) {
      var e = hist[i];
      var line = (e.date || '?') + '  methods=' + (e.methods || 0) +
        '  doubles=' + (e.doubles || 0) + '  kills=' + (e.kills || 0);
      var p = document.createElement('div');
      p.style.cssText = 'padding:2px 0;font-size:11px;color:#9ca3af';
      p.textContent = line;
      card.appendChild(p);
    }
  }));

  // Pending Checkpoints
  grid.appendChild(makeCard('Pending Checkpoints', function(card) {
    var cps = data.checkpoints_pending || [];
    if (cps.length === 0) {
      var p = document.createElement('div');
      p.style.color = '#00ff88';
      p.textContent = 'No pending checkpoints. System clean.';
      card.appendChild(p);
      return;
    }
    for (var i = 0; i < cps.length; i++) {
      var item = document.createElement('div');
      item.className = 'checkpoint-item';
      var nameSpan = document.createElement('span');
      nameSpan.className = 'name';
      nameSpan.textContent = cps[i].name;
      item.appendChild(nameSpan);
      card.appendChild(item);
    }
  }));

  // Session Checkpoint (Resume)
  grid.appendChild(makeCard('Session Checkpoint', function(card) {
    var ckpt = data.session_checkpoint;
    if (!ckpt) {
      addPre(card, 'No active checkpoint. Clean state.');
      return;
    }
    addStat(card, 'Session', ckpt.session_type || '?');
    addStat(card, 'Task', String(ckpt.task_completed || 0));
    addStat(card, 'Time', ckpt.timestamp || '?');
    var note = document.createElement('div');
    note.style.cssText = 'margin-top:8px;color:#f59e0b;font-size:11px';
    note.textContent = 'Resume available. Run --auto to continue from checkpoint.';
    card.appendChild(note);
  }));

  // Pipeline Metrics
  grid.appendChild(makeCard('Pipeline Metrics (Last 5)', function(card) {
    var metrics = data.pipeline_metrics || [];
    if (metrics.length === 0) {
      addPre(card, 'No pipeline data yet.');
      return;
    }
    for (var i = 0; i < metrics.length; i++) {
      var m = metrics[i];
      var line = (m.date || '?') + '  analyzed=' + (m.analyzed || 0) +
        '  hot=' + (m.hot || 0) + '  rate=' + (m.hot_rate || 0) + '%';
      var p = document.createElement('div');
      p.style.cssText = 'padding:2px 0;font-size:11px;color:#9ca3af';
      p.textContent = line;
      card.appendChild(p);
    }
  }));

  // Overnight Log
  grid.appendChild(makeCard('Overnight Log (Today)', function(card) {
    addPre(card, data.overnight_log);
  }));
}

function fetchData() {
  var ts = document.getElementById('timestamp');
  ts.className = 'ts refreshing';
  fetch('/api/state')
    .then(function(r) { return r.json(); })
    .then(function(data) {
      renderDashboard(data);
      ts.className = 'ts';
    })
    .catch(function(err) {
      ts.textContent = 'Error: ' + err.message;
      ts.className = 'ts';
    });
}

function runOp(opName) {
  var box = document.getElementById('op-output');
  box.style.display = 'block';
  box.textContent = 'Running ' + opName + '...';
  // Disable all buttons temporarily
  var btns = document.querySelectorAll('.btn');
  for (var i = 0; i < btns.length; i++) btns[i].disabled = true;

  fetch('/api/run?op=' + encodeURIComponent(opName))
    .then(function(r) { return r.json(); })
    .then(function(data) {
      box.textContent = '=== ' + opName + ' ===\\n\\n' + (data.output || 'No output') +
        (data.error ? '\\n\\nSTDERR:\\n' + data.error : '');
      // Re-enable buttons
      for (var i = 0; i < btns.length; i++) btns[i].disabled = false;
      // Refresh dashboard data after operation
      setTimeout(fetchData, 1000);
    })
    .catch(function(err) {
      box.textContent = 'Error: ' + err.message;
      for (var i = 0; i < btns.length; i++) btns[i].disabled = false;
    });
}

function doSearch() {
  var q = document.getElementById('search-input').value.trim();
  if (!q) return;
  var cat = document.getElementById('search-cat').value;
  var box = document.getElementById('search-results');
  box.style.display = 'block';
  box.textContent = 'Searching: "' + q + '"...';
  var url = '/api/search?q=' + encodeURIComponent(q);
  if (cat) url += '&category=' + encodeURIComponent(cat);
  fetch(url)
    .then(function(r) { return r.json(); })
    .then(function(data) {
      if (data.error) { box.textContent = 'Error: ' + data.error; return; }
      var results = data.results || [];
      if (results.length === 0) { box.textContent = 'No results for: "' + q + '"'; return; }
      var lines = ['Search: "' + q + '" (' + results.length + ' results)', ''];
      for (var i = 0; i < results.length; i++) {
        var r = results[i];
        var ts = (r.timestamp || '').substring(0, 19);
        lines.push((i+1) + '. [' + r.category + '] score=' + r.score.toFixed(3) + '  (' + ts + ')');
        lines.push('   Match: ' + (r.matched_terms || []).join(', '));
        lines.push('   ' + (r.snippet || ''));
        lines.push('');
      }
      box.textContent = lines.join('\\n');
    })
    .catch(function(err) {
      box.textContent = 'Search error: ' + err.message;
    });
}

// Initial load + auto-refresh every 30s
fetchData();
setInterval(fetchData, 30000);
</script>
</body>
</html>"""


class DashboardHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        pass  # Suppress default logging

    def do_GET(self):
        parsed = urlparse(self.path)

        if parsed.path == "/" or parsed.path == "/index.html":
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(build_html_page().encode("utf-8"))

        elif parsed.path == "/api/state":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Cache-Control", "no-cache")
            self.end_headers()
            state = gather_system_state()
            self.wfile.write(json.dumps(state, default=str).encode("utf-8"))

        elif parsed.path == "/api/search":
            params = parse_qs(parsed.query)
            q = params.get("q", [""])[0]
            if not q:
                self.send_response(400)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"error": "Missing query parameter 'q'"}).encode())
                return
            if not SEARCH_AVAILABLE:
                self.send_response(503)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"error": "Search not available. semantic_memory_search.py not found."}).encode())
                return

            category = params.get("category", [None])[0]
            top_k = int(params.get("top", ["10"])[0])
            recent = params.get("recent", [None])[0]
            recent_days = int(recent) if recent else None

            results = api_search(q, top_k=top_k, category=category,
                                 recent_days=recent_days)
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Cache-Control", "no-cache")
            self.end_headers()
            self.wfile.write(json.dumps({"query": q, "results": results},
                                        default=str).encode("utf-8"))

        elif parsed.path == "/api/run":
            params = parse_qs(parsed.query)
            op = params.get("op", [""])[0]
            if op not in OPS_COMMANDS:
                self.send_response(400)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"error": f"Unknown op: {op}"}).encode())
                return

            cmd_info = OPS_COMMANDS[op]
            try:
                result = subprocess.run(
                    cmd_info["cmd"],
                    capture_output=True, text=True, timeout=60,
                    cwd=str(BASE)
                )
                resp = {
                    "op": op,
                    "output": result.stdout,
                    "error": result.stderr if result.returncode != 0 else "",
                    "code": result.returncode,
                }
            except subprocess.TimeoutExpired:
                resp = {"op": op, "output": "", "error": "Timeout (60s)", "code": -1}
            except Exception as e:
                resp = {"op": op, "output": "", "error": str(e), "code": -1}

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(resp).encode("utf-8"))

        else:
            self.send_response(404)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            self.wfile.write(b"Not found")


def main():
    import argparse
    p = argparse.ArgumentParser(description="PRINTMAXX Ops Web Dashboard")
    p.add_argument("--port", type=int, default=8080, help="Port (default 8080)")
    p.add_argument("--no-open", action="store_true", help="Don't auto-open browser")
    args = p.parse_args()

    server = HTTPServer(("127.0.0.1", args.port), DashboardHandler)
    url = f"http://127.0.0.1:{args.port}"
    print(f"PRINTMAXX Ops Dashboard running at {url}")
    print("Press Ctrl+C to stop")

    if not args.no_open:
        try:
            subprocess.Popen(["open", url])
        except Exception:
            pass

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down.")
        server.server_close()


if __name__ == "__main__":
    main()
