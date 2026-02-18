#!/usr/bin/env python3
"""
PRINTMAXX Master Dashboard Generator
Reads all project data files and generates a Bloomberg-style HTML dashboard.
Run: python3 builds/master_dashboard/generate_dashboard.py
Output: builds/master_dashboard/index.html
"""

import csv
import json
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path
from collections import Counter

# --- Config ---
BASE = Path(__file__).resolve().parent.parent.parent
OUT = Path(__file__).resolve().parent / "index.html"

# --- Helpers ---

def safe_read_csv(path, max_rows=None):
    """Read CSV, return list of dicts. Gracefully handles missing/corrupt files."""
    rows = []
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            reader = csv.DictReader(f)
            for i, row in enumerate(reader):
                rows.append(row)
                if max_rows and i >= max_rows:
                    break
    except Exception as e:
        print(f"  WARN: Could not read {path}: {e}")
    return rows


def safe_read_json(path):
    try:
        with open(path, "r") as f:
            return json.load(f)
    except Exception as e:
        print(f"  WARN: Could not read {path}: {e}")
        return {}


def file_age_hours(path):
    """Return hours since file was last modified, or -1 if missing."""
    try:
        mtime = os.path.getmtime(path)
        delta = datetime.now() - datetime.fromtimestamp(mtime)
        return delta.total_seconds() / 3600
    except Exception:
        return -1


def file_mtime_str(path):
    try:
        mtime = os.path.getmtime(path)
        return datetime.fromtimestamp(mtime).strftime("%Y-%m-%d %H:%M")
    except Exception:
        return "N/A"


def count_lines(path):
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            return sum(1 for _ in f) - 1  # minus header
    except Exception:
        return 0


def count_files(directory, pattern="*"):
    try:
        return len(list(Path(directory).glob(pattern)))
    except Exception:
        return 0


def health_status(hours):
    if hours < 0:
        return ("MISSING", "#ef4444")
    if hours < 4:
        return ("LIVE", "#22c55e")
    if hours < 24:
        return ("STALE", "#f59e0b")
    return ("DEAD", "#ef4444")


# --- Data Collection ---

print("[PRINTMAXX] Generating master dashboard...")
print(f"  Base: {BASE}")
now = datetime.now()

# Panel 1: Pipeline Status
print("  Reading pipeline state...")
pipeline = safe_read_json(BASE / "AUTOMATIONS" / "research_pipeline_output" / "pipeline_state.json")
pipeline_last_run = pipeline.get("last_run", "Never")
pipeline_total_alpha = pipeline.get("total_alpha", 0)
pipeline_total_content = pipeline.get("total_content", 0)
pipeline_runs = pipeline.get("runs", [])
today_alpha = 0
today_content = 0
today_str = now.strftime("%Y-%m-%d")
for run in pipeline_runs:
    ts = run.get("timestamp", "")
    if ts.startswith(today_str):
        today_alpha += run.get("alpha_count", 0)
        today_content += run.get("content_count", 0)

# Panel 2: Alpha Funnel
print("  Reading alpha staging...")
alpha_rows = safe_read_csv(BASE / "LEDGER" / "ALPHA_STAGING.csv")
alpha_total = len(alpha_rows)
alpha_by_status = Counter()
alpha_by_category = Counter()
alpha_with_ops = 0
for r in alpha_rows:
    status = (r.get("status") or "UNKNOWN").strip()
    alpha_by_status[status] += 1
    cat = (r.get("category") or "UNKNOWN").strip()
    alpha_by_category[cat] += 1
    if r.get("ops_generated", "").strip().upper() == "TRUE":
        alpha_with_ops += 1

# Top categories (sorted)
top_categories = alpha_by_category.most_common(10)

# Panel 3: Auto-Ops Tracker
print("  Reading auto-ops tracker...")
ops_rows = safe_read_csv(BASE / "LEDGER" / "AUTO_OPS_TRACKER.csv")
ops_total = len(ops_rows)
ops_by_status = Counter()
ops_by_category = Counter()
ops_by_priority = Counter()
for r in ops_rows:
    ops_by_status[(r.get("status") or "UNKNOWN").strip()] += 1
    ops_by_category[(r.get("category") or "UNKNOWN").strip()] += 1
    ops_by_priority[(r.get("priority") or "UNKNOWN").strip()] += 1

# Panel 4: System Health
print("  Checking system health...")
health_checks = [
    ("Twitter Scraper", BASE / "AUTOMATIONS" / "logs" / "twitter_alpha.log"),
    ("Reddit Scraper", BASE / "AUTOMATIONS" / "logs" / "reddit_alpha.log"),
    ("Research Pipeline", BASE / "AUTOMATIONS" / "research_pipeline_output" / "pipeline_state.json"),
    ("Alpha Screener", BASE / "AUTOMATIONS" / "logs" / "alpha_screen.log"),
    ("Ecom Arb Engine", BASE / "LEDGER" / "ECOM_ARB_OPPORTUNITIES.csv"),
    ("Freelance Scanner", BASE / "LEDGER" / "FREELANCE_DEMAND_SCAN.csv"),
    ("Trend Aggregator", BASE / "LEDGER" / "TREND_SIGNALS.csv"),
    ("Closed Loop", BASE / "AUTOMATIONS" / "logs" / "closed_loop.log"),
    ("Morning Brain", BASE / "AUTOMATIONS" / "logs" / "brain_morning.log"),
    ("Evening Brain", BASE / "AUTOMATIONS" / "logs" / "brain_evening.log"),
    ("Venture Tracker", BASE / "AUTOMATIONS" / "logs" / "cron_ventures.log"),
    ("Auto-Resume", BASE / "AUTOMATIONS" / "logs" / "auto_resume.log"),
    ("Overnight Cron", BASE / "AUTOMATIONS" / "logs" / "cron_overnight.log"),
    ("Algo Detection", BASE / "AUTOMATIONS" / "logs" / "algo_detection.log"),
]
health_data = []
for name, path in health_checks:
    hours = file_age_hours(path)
    status, color = health_status(hours)
    mtime = file_mtime_str(path)
    health_data.append({
        "name": name,
        "status": status,
        "color": color,
        "last_updated": mtime,
        "hours_ago": round(hours, 1) if hours >= 0 else -1
    })

# Panel 5: Live Sites
live_sites = [
    ("printmaxx-seo.surge.sh", "601 SEO Pages"),
    ("ramadan-tracker.surge.sh", "Ramadan PWA"),
    ("focuslock-app.surge.sh", "FocusLock App"),
    ("habitforge-app.surge.sh", "HabitForge App"),
    ("mealmaxx-app.surge.sh", "MealMaxx App"),
    ("sleepmaxx-app.surge.sh", "SleepMaxx App"),
    ("walktounlock-app.surge.sh", "WalkToUnlock App"),
    ("printmaxx-portfolio.surge.sh", "Portfolio"),
    ("printmaxx-analyzer.surge.sh", "Analyzer"),
    ("printmaxx-dashboard.surge.sh", "Dashboard"),
    ("dental-demo.surge.sh", "Dental Demo"),
    ("restaurant-site-demo.surge.sh", "Restaurant Demo"),
    ("fitness-demo.surge.sh", "Fitness Demo"),
    ("legal-demo.surge.sh", "Legal Demo"),
    ("plumber-demo.surge.sh", "Plumber Demo"),
    ("realtor-demo.surge.sh", "Realtor Demo"),
    ("dental-motion.surge.sh", "Dental Motion"),
    ("realtor-motion.surge.sh", "Realtor Motion"),
    ("restaurant-motion.surge.sh", "Restaurant Motion"),
]

# Panel 6: Content Pipeline
print("  Checking content pipeline...")
auto_content_dir = BASE / "CONTENT" / "social" / "auto_generated"
auto_content_count = count_files(auto_content_dir, "*.*")
auto_content_latest = file_mtime_str(auto_content_dir) if auto_content_dir.exists() else "N/A"
# Count all content dirs
content_social_files = count_files(BASE / "CONTENT" / "social", "**/*.*")
content_buffer_files = count_files(BASE / "AUTOMATIONS" / "content_posting", "*.csv")

# Panel 7: Lead Pipeline
print("  Reading lead pipeline...")
master_leads_count = count_lines(BASE / "AUTOMATIONS" / "leads" / "MASTER_LEADS.csv")
hot_leads_count = count_lines(BASE / "AUTOMATIONS" / "leads" / "HOT_LEADS.csv")
outreach_files = count_files(BASE / "AUTOMATIONS" / "outreach", "*.csv")
pipeline_rows = safe_read_csv(BASE / "AUTOMATIONS" / "outreach" / "PIPELINE_TRACKER.csv", max_rows=70000)
pipeline_by_status = Counter()
for r in pipeline_rows:
    pipeline_by_status[(r.get("status") or "UNKNOWN").strip()] += 1
pipeline_total = len(pipeline_rows)

# Panel 8: Revenue
print("  Reading revenue tracker...")
revenue_rows = safe_read_csv(BASE / "FINANCIALS" / "REVENUE_TRACKER.csv")
total_revenue = 0
total_expenses = 0
total_profit = 0
methods_revenue = Counter()
for r in revenue_rows:
    try:
        rev = float(r.get("revenue", 0) or 0)
        exp = float(r.get("expenses", 0) or 0)
        prof = float(r.get("profit", 0) or 0)
        total_revenue += rev
        total_expenses += exp
        total_profit += prof
        methods_revenue[r.get("method_name", "Unknown")] += prof
    except Exception:
        pass


# --- HTML Generation ---

print("  Generating HTML...")

def json_safe(obj):
    return json.dumps(obj)

html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>PRINTMAXX Command Center</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.7/dist/chart.umd.min.js"></script>
<style>
  @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;500;600;700&display=swap');

  * {{ margin: 0; padding: 0; box-sizing: border-box; }}

  :root {{
    --bg-primary: #0a0a0f;
    --bg-secondary: #12121a;
    --bg-panel: #161621;
    --bg-panel-header: #1a1a2e;
    --border: #2a2a3e;
    --border-glow: #3a3a5e;
    --text-primary: #e8e8f0;
    --text-secondary: #8888a8;
    --text-muted: #5a5a78;
    --green: #22c55e;
    --green-dim: rgba(34,197,94,0.15);
    --amber: #f59e0b;
    --amber-dim: rgba(245,158,11,0.15);
    --red: #ef4444;
    --red-dim: rgba(239,68,68,0.15);
    --blue: #3b82f6;
    --blue-dim: rgba(59,130,246,0.15);
    --purple: #a855f7;
    --purple-dim: rgba(168,85,247,0.15);
    --cyan: #06b6d4;
    --cyan-dim: rgba(6,182,212,0.15);
  }}

  body {{
    font-family: 'JetBrains Mono', 'Fira Code', 'Cascadia Code', monospace;
    background: var(--bg-primary);
    color: var(--text-primary);
    min-height: 100vh;
    line-height: 1.5;
  }}

  .header {{
    background: linear-gradient(180deg, #1a1a2e 0%, var(--bg-primary) 100%);
    border-bottom: 1px solid var(--border);
    padding: 16px 24px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    position: sticky;
    top: 0;
    z-index: 100;
    backdrop-filter: blur(12px);
  }}

  .header-left {{
    display: flex;
    align-items: center;
    gap: 16px;
  }}

  .logo {{
    font-size: 20px;
    font-weight: 700;
    letter-spacing: 2px;
    background: linear-gradient(135deg, var(--green), var(--cyan));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
  }}

  .logo-sub {{
    font-size: 11px;
    color: var(--text-muted);
    letter-spacing: 3px;
    text-transform: uppercase;
  }}

  .header-right {{
    display: flex;
    align-items: center;
    gap: 20px;
    font-size: 12px;
    color: var(--text-secondary);
  }}

  .pulse-dot {{
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: var(--green);
    animation: pulse 2s infinite;
    display: inline-block;
  }}

  @keyframes pulse {{
    0%, 100% {{ opacity: 1; box-shadow: 0 0 0 0 rgba(34,197,94,0.4); }}
    50% {{ opacity: 0.7; box-shadow: 0 0 0 6px rgba(34,197,94,0); }}
  }}

  .grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(420px, 1fr));
    gap: 16px;
    padding: 20px 24px;
    max-width: 1920px;
    margin: 0 auto;
  }}

  .panel {{
    background: var(--bg-panel);
    border: 1px solid var(--border);
    border-radius: 8px;
    overflow: hidden;
    transition: border-color 0.2s;
  }}

  .panel:hover {{
    border-color: var(--border-glow);
  }}

  .panel-header {{
    background: var(--bg-panel-header);
    padding: 12px 16px;
    border-bottom: 1px solid var(--border);
    display: flex;
    align-items: center;
    justify-content: space-between;
  }}

  .panel-title {{
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: var(--text-secondary);
  }}

  .panel-badge {{
    font-size: 10px;
    padding: 2px 8px;
    border-radius: 4px;
    font-weight: 500;
  }}

  .badge-green {{ background: var(--green-dim); color: var(--green); }}
  .badge-amber {{ background: var(--amber-dim); color: var(--amber); }}
  .badge-red {{ background: var(--red-dim); color: var(--red); }}
  .badge-blue {{ background: var(--blue-dim); color: var(--blue); }}
  .badge-purple {{ background: var(--purple-dim); color: var(--purple); }}

  .panel-body {{
    padding: 16px;
  }}

  .stat-grid {{
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 12px;
  }}

  .stat-box {{
    background: var(--bg-secondary);
    border: 1px solid var(--border);
    border-radius: 6px;
    padding: 12px;
    text-align: center;
  }}

  .stat-value {{
    font-size: 28px;
    font-weight: 700;
    color: var(--green);
    line-height: 1.2;
  }}

  .stat-value.amber {{ color: var(--amber); }}
  .stat-value.red {{ color: var(--red); }}
  .stat-value.blue {{ color: var(--blue); }}
  .stat-value.purple {{ color: var(--purple); }}
  .stat-value.cyan {{ color: var(--cyan); }}

  .stat-label {{
    font-size: 10px;
    color: var(--text-muted);
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-top: 4px;
  }}

  .health-row {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 6px 0;
    border-bottom: 1px solid rgba(42,42,62,0.5);
    font-size: 12px;
  }}

  .health-row:last-child {{ border-bottom: none; }}

  .health-name {{ color: var(--text-secondary); flex: 1; }}
  .health-time {{ color: var(--text-muted); font-size: 11px; margin-right: 12px; }}

  .health-dot {{
    width: 10px;
    height: 10px;
    border-radius: 50%;
    display: inline-block;
    margin-right: 8px;
    flex-shrink: 0;
  }}

  .health-status {{
    font-size: 10px;
    font-weight: 600;
    letter-spacing: 1px;
    min-width: 50px;
    text-align: right;
  }}

  .bar-row {{
    display: flex;
    align-items: center;
    margin-bottom: 8px;
    font-size: 12px;
  }}

  .bar-label {{
    width: 140px;
    color: var(--text-secondary);
    font-size: 11px;
    text-overflow: ellipsis;
    overflow: hidden;
    white-space: nowrap;
    flex-shrink: 0;
  }}

  .bar-track {{
    flex: 1;
    height: 18px;
    background: var(--bg-secondary);
    border-radius: 3px;
    overflow: hidden;
    margin: 0 8px;
  }}

  .bar-fill {{
    height: 100%;
    border-radius: 3px;
    transition: width 0.5s ease;
    min-width: 2px;
  }}

  .bar-count {{
    min-width: 40px;
    text-align: right;
    color: var(--text-primary);
    font-weight: 500;
    font-size: 12px;
  }}

  .sites-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
    gap: 8px;
  }}

  .site-card {{
    background: var(--bg-secondary);
    border: 1px solid var(--border);
    border-radius: 6px;
    padding: 8px 10px;
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 11px;
    cursor: pointer;
    transition: all 0.2s;
  }}

  .site-card:hover {{
    border-color: var(--green);
    background: var(--green-dim);
  }}

  .site-dot {{
    width: 8px;
    height: 8px;
    border-radius: 50%;
    flex-shrink: 0;
  }}

  .site-name {{
    color: var(--text-secondary);
    text-overflow: ellipsis;
    overflow: hidden;
    white-space: nowrap;
  }}

  .site-desc {{
    color: var(--text-muted);
    font-size: 10px;
  }}

  .chart-container {{
    position: relative;
    height: 200px;
    margin-top: 12px;
  }}

  .kpi-strip {{
    display: flex;
    gap: 12px;
    padding: 10px 24px;
    background: var(--bg-secondary);
    border-bottom: 1px solid var(--border);
    overflow-x: auto;
  }}

  .kpi-item {{
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 12px;
    white-space: nowrap;
  }}

  .kpi-label {{ color: var(--text-muted); }}
  .kpi-value {{ color: var(--text-primary); font-weight: 600; }}
  .kpi-value.up {{ color: var(--green); }}
  .kpi-value.down {{ color: var(--red); }}

  .divider {{ width: 1px; background: var(--border); margin: 0 4px; }}

  .panel-wide {{
    grid-column: span 2;
  }}

  .pipeline-stages {{
    display: flex;
    gap: 2px;
    margin-top: 12px;
    align-items: flex-end;
  }}

  .stage {{
    flex: 1;
    text-align: center;
  }}

  .stage-bar {{
    background: var(--green);
    border-radius: 3px 3px 0 0;
    margin: 0 4px;
    min-height: 4px;
    transition: height 0.5s;
  }}

  .stage-label {{
    font-size: 9px;
    color: var(--text-muted);
    margin-top: 4px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
  }}

  .stage-count {{
    font-size: 12px;
    font-weight: 600;
    color: var(--text-primary);
    margin-top: 2px;
  }}

  .mini-table {{
    width: 100%;
    font-size: 11px;
    margin-top: 8px;
  }}

  .mini-table td {{
    padding: 4px 6px;
    border-bottom: 1px solid rgba(42,42,62,0.3);
  }}

  .mini-table td:first-child {{ color: var(--text-secondary); }}
  .mini-table td:last-child {{ text-align: right; font-weight: 500; }}

  .footer {{
    text-align: center;
    padding: 20px;
    font-size: 10px;
    color: var(--text-muted);
    border-top: 1px solid var(--border);
    margin-top: 20px;
  }}

  @media (max-width: 900px) {{
    .grid {{
      grid-template-columns: 1fr;
    }}
    .panel-wide {{
      grid-column: span 1;
    }}
    .header {{
      flex-direction: column;
      gap: 8px;
    }}
    .kpi-strip {{
      flex-wrap: wrap;
    }}
  }}

  /* Scrollbar */
  ::-webkit-scrollbar {{ width: 6px; height: 6px; }}
  ::-webkit-scrollbar-track {{ background: var(--bg-primary); }}
  ::-webkit-scrollbar-thumb {{ background: var(--border); border-radius: 3px; }}
  ::-webkit-scrollbar-thumb:hover {{ background: var(--border-glow); }}
</style>
</head>
<body>

<!-- HEADER -->
<div class="header">
  <div class="header-left">
    <div>
      <div class="logo">PRINTMAXX</div>
      <div class="logo-sub">command center</div>
    </div>
  </div>
  <div class="header-right">
    <span><span class="pulse-dot"></span> SYSTEMS ONLINE</span>
    <span id="clock">{now.strftime("%Y-%m-%d %H:%M:%S")}</span>
    <span style="color:var(--text-muted)">Generated: {now.strftime("%b %d %H:%M")}</span>
  </div>
</div>

<!-- KPI STRIP -->
<div class="kpi-strip">
  <div class="kpi-item">
    <span class="kpi-label">ALPHA</span>
    <span class="kpi-value up">{alpha_total:,}</span>
  </div>
  <div class="divider"></div>
  <div class="kpi-item">
    <span class="kpi-label">AUTO-OPS</span>
    <span class="kpi-value up">{ops_total:,}</span>
  </div>
  <div class="divider"></div>
  <div class="kpi-item">
    <span class="kpi-label">LEADS</span>
    <span class="kpi-value">{master_leads_count:,}</span>
  </div>
  <div class="divider"></div>
  <div class="kpi-item">
    <span class="kpi-label">HOT LEADS</span>
    <span class="kpi-value up">{hot_leads_count}</span>
  </div>
  <div class="divider"></div>
  <div class="kpi-item">
    <span class="kpi-label">PIPELINE</span>
    <span class="kpi-value">{pipeline_total:,}</span>
  </div>
  <div class="divider"></div>
  <div class="kpi-item">
    <span class="kpi-label">SITES LIVE</span>
    <span class="kpi-value up">{len(live_sites)}</span>
  </div>
  <div class="divider"></div>
  <div class="kpi-item">
    <span class="kpi-label">REVENUE</span>
    <span class="kpi-value {'up' if total_profit > 0 else 'down'}">${total_profit:,.0f}</span>
  </div>
  <div class="divider"></div>
  <div class="kpi-item">
    <span class="kpi-label">CONTENT</span>
    <span class="kpi-value">{pipeline_total_content}</span>
  </div>
</div>

<!-- GRID -->
<div class="grid">

  <!-- Panel 1: Pipeline Status -->
  <div class="panel">
    <div class="panel-header">
      <span class="panel-title">Research Pipeline</span>
      <span class="panel-badge badge-green">ACTIVE</span>
    </div>
    <div class="panel-body">
      <div class="stat-grid">
        <div class="stat-box">
          <div class="stat-value">{pipeline_total_alpha:,}</div>
          <div class="stat-label">Total Alpha (Lifetime)</div>
        </div>
        <div class="stat-box">
          <div class="stat-value cyan">{pipeline_total_content}</div>
          <div class="stat-label">Content Generated</div>
        </div>
        <div class="stat-box">
          <div class="stat-value amber">{today_alpha:,}</div>
          <div class="stat-label">Alpha Today</div>
        </div>
        <div class="stat-box">
          <div class="stat-value purple">{today_content}</div>
          <div class="stat-label">Content Today</div>
        </div>
      </div>
      <table class="mini-table" style="margin-top:12px">
        <tr><td>Last Run</td><td>{pipeline_last_run[:19] if len(pipeline_last_run) > 10 else pipeline_last_run}</td></tr>
        <tr><td>Pipeline Runs (Session)</td><td>{len(pipeline_runs)}</td></tr>
        <tr><td>Avg Alpha/Run</td><td>{round(pipeline_total_alpha/max(len(pipeline_runs),1)):,}</td></tr>
      </table>
    </div>
  </div>

  <!-- Panel 2: Alpha Funnel -->
  <div class="panel">
    <div class="panel-header">
      <span class="panel-title">Alpha Funnel</span>
      <span class="panel-badge badge-purple">{alpha_total:,} ENTRIES</span>
    </div>
    <div class="panel-body">
      <div class="stat-grid">
        <div class="stat-box">
          <div class="stat-value">{alpha_by_status.get('APPROVED', 0):,}</div>
          <div class="stat-label">Approved</div>
        </div>
        <div class="stat-box">
          <div class="stat-value amber">{alpha_by_status.get('PENDING_REVIEW', 0):,}</div>
          <div class="stat-label">Pending Review</div>
        </div>
        <div class="stat-box">
          <div class="stat-value blue">{alpha_by_status.get('ENGAGEMENT_BAIT', 0):,}</div>
          <div class="stat-label">Engagement Bait</div>
        </div>
        <div class="stat-box">
          <div class="stat-value red">{alpha_by_status.get('REJECTED', 0):,}</div>
          <div class="stat-label">Rejected</div>
        </div>
      </div>
      <div style="margin-top:12px;font-size:11px;color:var(--text-muted);margin-bottom:6px;">TOP CATEGORIES</div>
      {"".join(f'''<div class="bar-row">
        <div class="bar-label">{cat}</div>
        <div class="bar-track"><div class="bar-fill" style="width:{min(count/max(top_categories[0][1],1)*100,100):.0f}%;background:var(--green);opacity:{0.4 + 0.6*(1 - i/max(len(top_categories),1))};"></div></div>
        <div class="bar-count">{count:,}</div>
      </div>''' for i, (cat, count) in enumerate(top_categories[:8]))}
    </div>
  </div>

  <!-- Panel 3: Auto-Ops Tracker -->
  <div class="panel">
    <div class="panel-header">
      <span class="panel-title">Auto-Ops Tracker</span>
      <span class="panel-badge badge-blue">{ops_total:,} OPS</span>
    </div>
    <div class="panel-body">
      <div class="stat-grid">
        <div class="stat-box">
          <div class="stat-value">{ops_total:,}</div>
          <div class="stat-label">Total Generated</div>
        </div>
        <div class="stat-box">
          <div class="stat-value cyan">{alpha_with_ops:,}</div>
          <div class="stat-label">Alpha w/ Ops</div>
        </div>
      </div>
      <div style="margin-top:14px;font-size:11px;color:var(--text-muted);margin-bottom:6px;">BY STATUS</div>
      {"".join(f'''<div class="bar-row">
        <div class="bar-label">{s}</div>
        <div class="bar-track"><div class="bar-fill" style="width:{min(c/max(ops_total,1)*100,100):.0f}%;background:{'var(--green)' if s=='DEPLOYED' else 'var(--amber)' if s=='GENERATED' else 'var(--blue)' if s=='REVIEWED' else 'var(--red)'};"></div></div>
        <div class="bar-count">{c:,}</div>
      </div>''' for s, c in ops_by_status.most_common(6))}
      <div style="margin-top:10px;font-size:11px;color:var(--text-muted);margin-bottom:6px;">BY PRIORITY</div>
      {"".join(f'''<div class="bar-row">
        <div class="bar-label">{p}</div>
        <div class="bar-track"><div class="bar-fill" style="width:{min(c/max(ops_total,1)*100,100):.0f}%;background:{'var(--red)' if p=='HIGH' else 'var(--amber)' if p=='MEDIUM' else 'var(--green)'};"></div></div>
        <div class="bar-count">{c:,}</div>
      </div>''' for p, c in ops_by_priority.most_common(5))}
    </div>
  </div>

  <!-- Panel 4: System Health -->
  <div class="panel">
    <div class="panel-header">
      <span class="panel-title">System Health</span>
      <span class="panel-badge {'badge-green' if sum(1 for h in health_data if h['status']=='LIVE') > len(health_data)//2 else 'badge-amber'}">{sum(1 for h in health_data if h['status']=='LIVE')}/{len(health_data)} LIVE</span>
    </div>
    <div class="panel-body">
      {"".join(f'''<div class="health-row">
        <span class="health-dot" style="background:{h['color']}"></span>
        <span class="health-name">{h['name']}</span>
        <span class="health-time">{h['last_updated']}</span>
        <span class="health-status" style="color:{h['color']}">{h['status']}</span>
      </div>''' for h in health_data)}
    </div>
  </div>

  <!-- Panel 5: Live Sites -->
  <div class="panel panel-wide">
    <div class="panel-header">
      <span class="panel-title">Live Sites</span>
      <span class="panel-badge badge-green">{len(live_sites)} DEPLOYED</span>
    </div>
    <div class="panel-body">
      <div class="sites-grid">
        {"".join(f'''<a href="https://{domain}" target="_blank" style="text-decoration:none;">
          <div class="site-card" id="site-{i}">
            <span class="site-dot" id="dot-{i}" style="background:var(--text-muted)"></span>
            <div>
              <div class="site-name">{domain.replace('.surge.sh','')}</div>
              <div class="site-desc">{desc}</div>
            </div>
          </div>
        </a>''' for i, (domain, desc) in enumerate(live_sites))}
      </div>
    </div>
  </div>

  <!-- Panel 6: Content Pipeline -->
  <div class="panel">
    <div class="panel-header">
      <span class="panel-title">Content Pipeline</span>
      <span class="panel-badge badge-cyan" style="background:var(--cyan-dim);color:var(--cyan);">GENERATING</span>
    </div>
    <div class="panel-body">
      <div class="stat-grid">
        <div class="stat-box">
          <div class="stat-value cyan">{auto_content_count}</div>
          <div class="stat-label">Auto-Generated</div>
        </div>
        <div class="stat-box">
          <div class="stat-value">{content_buffer_files}</div>
          <div class="stat-label">Buffer CSVs</div>
        </div>
        <div class="stat-box">
          <div class="stat-value purple">{content_social_files}</div>
          <div class="stat-label">Social Content Files</div>
        </div>
        <div class="stat-box">
          <div class="stat-value amber">{pipeline_total_content}</div>
          <div class="stat-label">Pipeline Content</div>
        </div>
      </div>
      <table class="mini-table" style="margin-top:12px">
        <tr><td>Auto-Gen Latest</td><td>{auto_content_latest}</td></tr>
        <tr><td>Ops Content Deployed</td><td>{ops_by_status.get('DEPLOYED', 0):,}</td></tr>
        <tr><td>Ops Content Generated</td><td>{ops_by_status.get('GENERATED', 0):,}</td></tr>
      </table>
    </div>
  </div>

  <!-- Panel 7: Lead Pipeline -->
  <div class="panel">
    <div class="panel-header">
      <span class="panel-title">Lead Pipeline</span>
      <span class="panel-badge badge-amber">{pipeline_total:,} IN PIPE</span>
    </div>
    <div class="panel-body">
      <div class="stat-grid">
        <div class="stat-box">
          <div class="stat-value">{master_leads_count:,}</div>
          <div class="stat-label">Total Leads</div>
        </div>
        <div class="stat-box">
          <div class="stat-value amber">{hot_leads_count}</div>
          <div class="stat-label">Hot Leads</div>
        </div>
        <div class="stat-box">
          <div class="stat-value blue">{outreach_files}</div>
          <div class="stat-label">Outreach Files</div>
        </div>
        <div class="stat-box">
          <div class="stat-value purple">{pipeline_total:,}</div>
          <div class="stat-label">Pipeline Total</div>
        </div>
      </div>
      <div style="margin-top:14px;font-size:11px;color:var(--text-muted);margin-bottom:6px;">PIPELINE BY STATUS</div>
      {"".join(f'''<div class="bar-row">
        <div class="bar-label">{s}</div>
        <div class="bar-track"><div class="bar-fill" style="width:{min(c/max(pipeline_total,1)*100,100):.0f}%;background:{'var(--green)' if s in ('SENT','REPLIED','CLOSED') else 'var(--amber)' if s=='READY' else 'var(--blue)'};"></div></div>
        <div class="bar-count">{c:,}</div>
      </div>''' for s, c in pipeline_by_status.most_common(6))}
    </div>
  </div>

  <!-- Panel 8: Revenue & Ventures -->
  <div class="panel">
    <div class="panel-header">
      <span class="panel-title">Revenue & Ventures</span>
      <span class="panel-badge {'badge-green' if total_profit > 0 else 'badge-red'}">${total_profit:,.0f} P&L</span>
    </div>
    <div class="panel-body">
      <div class="stat-grid">
        <div class="stat-box">
          <div class="stat-value {'up' if total_revenue > 0 else ''}" style="color:var(--green)">${total_revenue:,.0f}</div>
          <div class="stat-label">Total Revenue</div>
        </div>
        <div class="stat-box">
          <div class="stat-value red">${total_expenses:,.0f}</div>
          <div class="stat-label">Total Expenses</div>
        </div>
        <div class="stat-box">
          <div class="stat-value" style="color:{'var(--green)' if total_profit >= 0 else 'var(--red)'}">${total_profit:,.0f}</div>
          <div class="stat-label">Net Profit</div>
        </div>
        <div class="stat-box">
          <div class="stat-value blue">{len(revenue_rows)}</div>
          <div class="stat-label">Tracked Methods</div>
        </div>
      </div>
      <div style="margin-top:14px;font-size:11px;color:var(--text-muted);margin-bottom:6px;">TOP METHODS BY PROFIT</div>
      {"".join(f'''<div class="bar-row">
        <div class="bar-label">{m[:18]}</div>
        <div class="bar-track"><div class="bar-fill" style="width:{min(abs(p)/max(abs(methods_revenue.most_common(1)[0][1]) if methods_revenue else 1, 1)*100,100):.0f}%;background:{'var(--green)' if p >= 0 else 'var(--red)'};"></div></div>
        <div class="bar-count" style="color:{'var(--green)' if p >= 0 else 'var(--red)'}">${p:,.0f}</div>
      </div>''' for m, p in methods_revenue.most_common(5))}
      <table class="mini-table" style="margin-top:8px">
        <tr><td>Paper Trades Active</td><td>{len(revenue_rows)}</td></tr>
        <tr><td>Revenue Sources</td><td>{len(set(r.get('source','') for r in revenue_rows))}</td></tr>
      </table>
    </div>
  </div>

  <!-- Panel 9: Alpha Category Breakdown (Chart) -->
  <div class="panel">
    <div class="panel-header">
      <span class="panel-title">Alpha by Category</span>
      <span class="panel-badge badge-purple">{len(alpha_by_category)} CATEGORIES</span>
    </div>
    <div class="panel-body">
      <div class="chart-container">
        <canvas id="alphaCategoryChart"></canvas>
      </div>
    </div>
  </div>

  <!-- Panel 10: Ops Category Breakdown (Chart) -->
  <div class="panel">
    <div class="panel-header">
      <span class="panel-title">Auto-Ops by Category</span>
      <span class="panel-badge badge-blue">{len(ops_by_category)} TYPES</span>
    </div>
    <div class="panel-body">
      <div class="chart-container">
        <canvas id="opsCategoryChart"></canvas>
      </div>
    </div>
  </div>

</div>

<!-- FOOTER -->
<div class="footer">
  PRINTMAXX COMMAND CENTER v1.0 | Generated {now.strftime("%Y-%m-%d %H:%M:%S")} |
  Regenerate: <code style="color:var(--cyan)">python3 builds/master_dashboard/generate_dashboard.py</code> |
  Auto-refresh: 60s
</div>

<script>
// Live clock
setInterval(() => {{
  const el = document.getElementById('clock');
  if (el) el.textContent = new Date().toLocaleString('sv-SE').replace(',','');
}}, 1000);

// Auto-refresh every 60s (reloads page)
setTimeout(() => location.reload(), 60000);

// Site health checks (ping via Image trick - not perfect but gives visual feedback)
const sites = {json.dumps([s[0] for s in live_sites])};
sites.forEach((site, i) => {{
  const dot = document.getElementById('dot-' + i);
  fetch('https://' + site, {{ mode: 'no-cors', cache: 'no-cache' }})
    .then(() => {{
      if (dot) dot.style.background = 'var(--green)';
    }})
    .catch(() => {{
      if (dot) dot.style.background = 'var(--red)';
    }});
}});

// Charts
const chartColors = [
  '#22c55e', '#3b82f6', '#a855f7', '#f59e0b', '#ef4444',
  '#06b6d4', '#ec4899', '#14b8a6', '#f97316', '#8b5cf6',
  '#10b981', '#6366f1', '#e11d48'
];

// Alpha category pie chart
const alphaCtx = document.getElementById('alphaCategoryChart');
if (alphaCtx) {{
  const alphaData = {json.dumps([{"label": c, "value": v} for c, v in top_categories[:10]])};
  new Chart(alphaCtx, {{
    type: 'doughnut',
    data: {{
      labels: alphaData.map(d => d.label),
      datasets: [{{
        data: alphaData.map(d => d.value),
        backgroundColor: chartColors.slice(0, alphaData.length),
        borderColor: '#161621',
        borderWidth: 2
      }}]
    }},
    options: {{
      responsive: true,
      maintainAspectRatio: false,
      plugins: {{
        legend: {{
          position: 'right',
          labels: {{
            color: '#8888a8',
            font: {{ family: "'JetBrains Mono', monospace", size: 10 }},
            boxWidth: 12,
            padding: 8
          }}
        }}
      }}
    }}
  }});
}}

// Ops category pie chart
const opsCtx = document.getElementById('opsCategoryChart');
if (opsCtx) {{
  const opsData = {json.dumps([{"label": c, "value": v} for c, v in ops_by_category.most_common(10)])};
  new Chart(opsCtx, {{
    type: 'doughnut',
    data: {{
      labels: opsData.map(d => d.label),
      datasets: [{{
        data: opsData.map(d => d.value),
        backgroundColor: chartColors.slice(0, opsData.length),
        borderColor: '#161621',
        borderWidth: 2
      }}]
    }},
    options: {{
      responsive: true,
      maintainAspectRatio: false,
      plugins: {{
        legend: {{
          position: 'right',
          labels: {{
            color: '#8888a8',
            font: {{ family: "'JetBrains Mono', monospace", size: 10 }},
            boxWidth: 12,
            padding: 8
          }}
        }}
      }}
    }}
  }});
}}
</script>

</body>
</html>
"""

with open(OUT, "w", encoding="utf-8") as f:
    f.write(html)

print(f"\n  Dashboard generated: {OUT}")
print(f"  File size: {os.path.getsize(OUT):,} bytes")
print(f"  Open: open {OUT}")
print(f"\n  Stats embedded:")
print(f"    Alpha entries:     {alpha_total:,}")
print(f"    Auto-ops:          {ops_total:,}")
print(f"    Pipeline alpha:    {pipeline_total_alpha:,}")
print(f"    Pipeline content:  {pipeline_total_content}")
print(f"    Master leads:      {master_leads_count:,}")
print(f"    Hot leads:         {hot_leads_count}")
print(f"    Pipeline entries:  {pipeline_total:,}")
print(f"    Revenue tracked:   ${total_revenue:,.0f}")
print(f"    Live sites:        {len(live_sites)}")
print(f"    Health checks:     {len(health_data)}")
print(f"    Content files:     {content_social_files}")
print(f"\n  Done.")
