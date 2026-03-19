#!/usr/bin/env python3
"""
PRINTMAXX UNIFIED CONTROL PANEL
=================================
Single Flask server that replaces all scattered dashboards.
Serves the control panel HTML and exposes API endpoints for:
- Agent throttle control (EFFICIENT/HIGH mode toggle, per-agent on/off)
- System status (health, revenue, cron, sites)
- Quick actions (run scripts, view logs)
- Slash command launcher
- System tree (hierarchy, data flow, cron schedule)
- Real-time metrics (agent invocations, alpha entries)
- Venture status
- Pipeline funnel

Port: 9999
Usage: python3 AUTOMATIONS/control_panel.py
"""

import csv
import json
import os
import re
import sqlite3
import subprocess
import sys
import threading
import time
import webbrowser
from datetime import datetime, timedelta
from pathlib import Path
from collections import Counter
from urllib.request import Request, urlopen
from urllib.error import URLError

try:
    from flask import Flask, jsonify, request, Response
except ImportError:
    print("ERROR: Flask not installed. Run: pip3 install flask")
    sys.exit(1)

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parent.parent
AUTOMATIONS = PROJECT_ROOT / "AUTOMATIONS"
OPS = PROJECT_ROOT / "OPS"
LEDGER = PROJECT_ROOT / "LEDGER"
FINANCIALS = PROJECT_ROOT / "FINANCIALS"
LOGS_DIR = AUTOMATIONS / "logs"
CLAUDE_LOGS = Path.home() / ".claude" / "logs"
LA_DIR = Path.home() / "Library" / "LaunchAgents"
HTML_PATH = AUTOMATIONS / "control_panel.html"

PORT = 9999
PYTHON = sys.executable

# Load N8N_API_KEY from .env
N8N_BASE = "http://localhost:5678"
N8N_API_KEY = ""
_env_path = PROJECT_ROOT / ".env"
if _env_path.exists():
    try:
        with open(_env_path, "r") as _ef:
            for _line in _ef:
                _line = _line.strip()
                if _line.startswith("N8N_API_KEY="):
                    N8N_API_KEY = _line.split("=", 1)[1].strip()
                    break
    except Exception:
        pass

# Sovrun paths
SOVRUN_SKILLS_DB = AUTOMATIONS / "agent" / "sovrun" / "skills.db"
SOVRUN_SKILLS_DB_ALT = AUTOMATIONS / "agent" / "swarm" / "sovrun" / "skills.db"
DAG_CHECKPOINT = AUTOMATIONS / "agent" / "morning_dag_checkpoint.json"
DAG_STATE = AUTOMATIONS / "agent" / "morning_dag_state.json"

app = Flask(__name__)
_lock = threading.Lock()


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def safe_read(filepath, max_lines=50):
    try:
        p = Path(filepath)
        if not p.exists():
            return ""
        with open(p, "r", encoding="utf-8", errors="replace") as f:
            lines = f.readlines()
        return "".join(lines[-max_lines:])
    except Exception:
        return ""


def safe_read_json(filepath):
    try:
        with open(filepath, "r") as f:
            return json.load(f)
    except Exception:
        return {}


def safe_read_csv(filepath, max_rows=100):
    try:
        p = Path(filepath)
        if not p.exists():
            return []
        rows = []
        with open(p, "r", encoding="utf-8", errors="replace") as f:
            reader = csv.DictReader(f)
            for i, row in enumerate(reader):
                if i >= max_rows:
                    break
                rows.append(dict(row))
        return rows
    except Exception:
        return []


def run_cmd(cmd, timeout=30):
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout, cwd=str(PROJECT_ROOT))
        return r.returncode, r.stdout.strip(), r.stderr.strip()
    except subprocess.TimeoutExpired:
        return -1, "", "timeout"
    except Exception as e:
        return -1, "", str(e)


def days_until_friday():
    today = datetime.now()
    days_ahead = (4 - today.weekday()) % 7
    if days_ahead == 0 and today.hour >= 12:
        days_ahead = 7
    return days_ahead


def relative_time(ts):
    if not ts:
        return "never"
    try:
        if isinstance(ts, (int, float)):
            dt = datetime.fromtimestamp(ts)
        else:
            dt = datetime.fromisoformat(str(ts))
        delta = datetime.now() - dt
        if delta.total_seconds() < 60:
            return f"{int(delta.total_seconds())}s ago"
        if delta.total_seconds() < 3600:
            return f"{int(delta.total_seconds() / 60)}m ago"
        if delta.total_seconds() < 86400:
            return f"{delta.total_seconds() / 3600:.1f}h ago"
        return f"{delta.days}d ago"
    except Exception:
        return "unknown"


# ---------------------------------------------------------------------------
# Throttle integration
# ---------------------------------------------------------------------------
def get_throttle_status():
    """Get full throttle status via throttle_toggle.py --json"""
    code, out, err = run_cmd([PYTHON, str(AUTOMATIONS / "throttle_toggle.py"), "--json"], timeout=15)
    if code == 0 and out:
        try:
            return json.loads(out)
        except json.JSONDecodeError:
            pass
    return {"mode": "unknown", "agents": {}, "summary": {}}


def set_throttle_mode(mode):
    with _lock:
        code, out, err = run_cmd([PYTHON, str(AUTOMATIONS / "throttle_toggle.py"), "--mode", mode], timeout=60)
    return {"success": code == 0, "output": out, "error": err}


def toggle_agent(agent_id, enabled):
    flag = "--on" if enabled else "--off"
    with _lock:
        code, out, err = run_cmd([PYTHON, str(AUTOMATIONS / "throttle_toggle.py"), "--agent", agent_id, flag], timeout=15)
    return {"success": code == 0, "output": out, "error": err}


def set_agent_interval(agent_id, hours):
    with _lock:
        code, out, err = run_cmd([PYTHON, str(AUTOMATIONS / "throttle_toggle.py"), "--agent", agent_id, "--interval", str(hours)], timeout=15)
    return {"success": code == 0, "output": out, "error": err}


# ---------------------------------------------------------------------------
# System status
# ---------------------------------------------------------------------------
def get_system_status():
    status = {
        "timestamp": datetime.now().isoformat(),
        "days_until_reset": days_until_friday(),
        "revenue": "$0",
        "day_number": 0,
    }

    # Revenue from financial tracker
    rev_path = FINANCIALS / "REVENUE_TRACKER.csv"
    if rev_path.exists():
        rows = safe_read_csv(rev_path, max_rows=1000)
        total = sum(float(r.get("amount", 0)) for r in rows if r.get("amount"))
        status["revenue"] = f"${total:,.0f}"

    # Day number from session briefing
    briefing = safe_read(OPS / "SESSION_BRIEFING.md", max_lines=20)
    for line in briefing.split("\n"):
        if "Day " in line and "at zero" in line.lower():
            try:
                day_num = int(line.split("Day ")[1].split(" ")[0])
                status["day_number"] = day_num
            except (IndexError, ValueError):
                pass

    # Alpha stats
    alpha_path = LEDGER / "ALPHA_STAGING.csv"
    if alpha_path.exists():
        rows = safe_read_csv(alpha_path, max_rows=50000)
        status["alpha_total"] = len(rows)
        status["alpha_pending"] = sum(1 for r in rows if r.get("status", "").upper() == "PENDING_REVIEW")
        status["alpha_approved"] = sum(1 for r in rows if r.get("status", "").upper() == "APPROVED")

    # Cron count
    code, out, _ = run_cmd(["crontab", "-l"], timeout=5)
    if code == 0:
        cron_lines = [l for l in out.split("\n") if l.strip() and not l.strip().startswith("#") and not l.strip().startswith("SHELL") and not l.strip().startswith("PATH") and not l.strip().startswith("BASE") and not l.strip().startswith("PYTHON")]
        status["cron_jobs"] = len(cron_lines)

    # Launchd agent count
    code, out, _ = run_cmd(["launchctl", "list"], timeout=5)
    if code == 0:
        pm_agents = [l for l in out.split("\n") if "printmaxx" in l.lower() or "com.claude.schedule" in l.lower()]
        status["launchd_agents"] = len(pm_agents)

    return status


def get_log_tail(agent_id, lines=30):
    """Get last N lines of an agent's log."""
    # Try ~/.claude/logs/ first (swarm + venture agents)
    for prefix in ["swarm_", "auto_", ""]:
        log_path = CLAUDE_LOGS / f"{prefix}{agent_id}.log"
        if log_path.exists():
            return safe_read(log_path, max_lines=lines)

    # Try AUTOMATIONS/logs/
    for name in [f"{agent_id}.log", f"cron_{agent_id}.log"]:
        log_path = LOGS_DIR / name
        if log_path.exists():
            return safe_read(log_path, max_lines=lines)

    return f"No log found for {agent_id}"


def get_quick_actions():
    """List of available quick actions."""
    return [
        {"id": "decision_engine", "name": "Decision Engine Cycle", "cmd": f"{PYTHON} AUTOMATIONS/decision_engine.py --cycle", "category": "core"},
        {"id": "system_health", "name": "System Health Check", "cmd": f"{PYTHON} AUTOMATIONS/system_health_monitor.py --quick", "category": "core"},
        {"id": "alpha_process", "name": "Process New Alpha", "cmd": f"{PYTHON} AUTOMATIONS/alpha_auto_processor.py --process-new", "category": "alpha"},
        {"id": "loop_closer", "name": "Run Loop Closer", "cmd": f"{PYTHON} AUTOMATIONS/loop_closer.py --cycle", "category": "core"},
        {"id": "quality_gate", "name": "Quality Gate", "cmd": f"{PYTHON} AUTOMATIONS/quality_gate.py --gate", "category": "quality"},
        {"id": "daily_digest", "name": "Generate Daily Digest", "cmd": f"{PYTHON} AUTOMATIONS/daily_digest.py", "category": "reports"},
        {"id": "tactical_plan", "name": "Generate Tactical Plan", "cmd": f"{PYTHON} AUTOMATIONS/daily_tactical_engine.py --save", "category": "reports"},
        {"id": "intelligence_stats", "name": "Intelligence Stats", "cmd": f"{PYTHON} AUTOMATIONS/intelligence_router.py --stats", "category": "intel"},
        {"id": "alpha_stats", "name": "Alpha Query Stats", "cmd": f"{PYTHON} AUTOMATIONS/alpha_query.py --stats", "category": "alpha"},
        {"id": "venture_status", "name": "Venture Status", "cmd": f"{PYTHON} AUTOMATIONS/venture_autonomy.py --status", "category": "agents"},
        {"id": "swarm_status", "name": "Swarm Status", "cmd": f"{PYTHON} AUTOMATIONS/agent_swarm.py --status", "category": "agents"},
        {"id": "swarm_health", "name": "Swarm Health Check", "cmd": f"{PYTHON} AUTOMATIONS/agent_swarm.py --health", "category": "agents"},
        {"id": "throttle_status", "name": "Throttle Status", "cmd": f"{PYTHON} AUTOMATIONS/throttle_toggle.py --status", "category": "throttle"},
        {"id": "throttle_estimate", "name": "Token Burn Estimate", "cmd": f"{PYTHON} AUTOMATIONS/throttle_toggle.py --estimate", "category": "throttle"},
    ]


def get_slash_commands():
    """List available Claude Code slash commands."""
    cmd_dir = PROJECT_ROOT / ".claude" / "commands"
    commands = []
    if cmd_dir.exists():
        for f in sorted(cmd_dir.glob("*.md")):
            name = f.stem
            first_line = ""
            try:
                with open(f, "r") as fh:
                    first_line = fh.readline().strip().lstrip("#").strip()
            except Exception:
                pass
            commands.append({"name": f"/{name}", "description": first_line, "file": str(f.relative_to(PROJECT_ROOT))})
    return commands


def get_deployed_sites():
    """Read deployment URLs."""
    deploy_path = OPS / "DEPLOYMENT_URLS.md"
    sites = []
    if deploy_path.exists():
        content = safe_read(deploy_path, max_lines=100)
        for line in content.split("\n"):
            if "surge.sh" in line or "vercel.app" in line:
                urls = re.findall(r'https?://[^\s\)]+', line)
                for url in urls:
                    name = line.split("|")[1].strip() if "|" in line else url.split("//")[1].split(".")[0]
                    sites.append({"name": name, "url": url})
    return sites


# ---------------------------------------------------------------------------
# NEW: System Tree API
# ---------------------------------------------------------------------------
def get_system_tree():
    """Parse PRINTMAXX_SYSTEM_MAP.md for hierarchy, data flow, agents, cron."""
    hierarchy = [
        {
            "level": "L0",
            "name": "ORCHESTRATOR",
            "color": "#ff3355",
            "scripts": [
                {"name": "ceo_agent.py", "desc": "16 phases. Scores all ops. PROMOTE/ENHANCE/CREATE/KILL.", "schedule": "Every 2h"}
            ]
        },
        {
            "level": "L1",
            "name": "ENGINES",
            "color": "#ff6b35",
            "scripts": [
                {"name": "venture_autonomy.py", "desc": "8 venture pipelines. Self-managing schedules.", "schedule": "Every 4h"},
                {"name": "agent_swarm.py", "desc": "25 agents via launchd. swarm_brain every 4h.", "schedule": "Continuous"},
                {"name": "decision_engine.py", "desc": "Closed-loop: pending data to scored actions.", "schedule": "Every 30min"}
            ]
        },
        {
            "level": "L2",
            "name": "INTELLIGENCE",
            "color": "#4488ff",
            "scripts": [
                {"name": "intelligence_router.py", "desc": "484 docs + 15K alpha entries into single brief.", "schedule": "On demand"},
                {"name": "alpha_query.py", "desc": "Venture-based alpha search with ROI normalization.", "schedule": "On demand"},
                {"name": "daily_digest.py", "desc": "What happened overnight summary.", "schedule": "6:45 AM"},
                {"name": "session_briefing.py", "desc": "Auto session-start: agent reports, changes.", "schedule": "On session start"},
                {"name": "prompt_meta_review.py", "desc": "Analyzes user prompts for lost threads.", "schedule": "Every 48h"}
            ]
        },
        {
            "level": "L3",
            "name": "EXECUTION",
            "color": "#00ff88",
            "scripts": [
                {"name": "daily_tactical_engine.py", "desc": "Unified 'do exactly this today' plan.", "schedule": "7:15 AM"},
                {"name": "daily_engagement_planner.py", "desc": "Warmup-aware Twitter action plan.", "schedule": "7:00 AM"},
                {"name": "growth_strategist.py", "desc": "Growth strategies per venture from intel.", "schedule": "5:00 AM"},
                {"name": "twitter_warmup_poster.py", "desc": "21-day warmup ramp. Advances at midnight.", "schedule": "Midnight"},
                {"name": "alpha_auto_processor.py", "desc": "Routes ALPHA_STAGING to ventures.", "schedule": "6:30 AM"},
                {"name": "actionable_aggregator.py", "desc": "Scans 6 sources into prioritized queue.", "schedule": "7:30 AM"}
            ]
        },
        {
            "level": "L4",
            "name": "COLLECTION",
            "color": "#8b5cf6",
            "scripts": [
                {"name": "twitter_alpha_scraper.py", "desc": "133 Twitter accounts via Brave cookies.", "schedule": "6:00 AM"},
                {"name": "background_reddit_scraper.py", "desc": "Reddit JSON API, no auth.", "schedule": "6:15 AM"}
            ]
        },
        {
            "level": "L5",
            "name": "QUALITY",
            "color": "#eab308",
            "scripts": [
                {"name": "quality_gate.py", "desc": "Hard gate. Blocks slop, rewrites bad content.", "schedule": "Every 2h"},
                {"name": "compliance_scanner.py", "desc": "FTC / platform compliance auditing.", "schedule": "On demand"},
                {"name": "system_health_monitor.py", "desc": "Health checks: agents, cron, disk.", "schedule": "Every 6h"}
            ]
        },
        {
            "level": "L6",
            "name": "MAINTENANCE",
            "color": "#888888",
            "scripts": [
                {"name": "loop_closer.py", "desc": "3 loops: decision, feedback, pipeline.", "schedule": "Every 2h"},
                {"name": "memory_manager.py", "desc": "Filesystem-based memory management.", "schedule": "5:00 AM"},
                {"name": "build_codebase_grammar.py", "desc": "118x compressed grammar for LLM context.", "schedule": "5:45 AM"},
                {"name": "wire_missed_intelligence.py", "desc": "Parses scan results to update catalog.", "schedule": "On demand"}
            ]
        }
    ]

    data_flow = [
        {"from": "Scrapers", "to": "ALPHA_STAGING.csv", "label": "Raw alpha intake"},
        {"from": "ALPHA_STAGING.csv", "to": "alpha_auto_processor", "label": "Route to ventures"},
        {"from": "Filesystem scan", "to": "wire_missed_intelligence", "label": "Find unindexed docs"},
        {"from": "wire_missed_intelligence", "to": "INTELLIGENCE_CATALOG.json", "label": "Update catalog"},
        {"from": "All sources", "to": "intelligence_router.py", "label": "484 docs + 15K alpha"},
        {"from": "intelligence_router.py", "to": "ceo_agent (Phase 3.5)", "label": "Enrichment"},
        {"from": "intelligence_router.py", "to": "venture_autonomy", "label": "Pre-execution brief"},
        {"from": "intelligence_router.py", "to": "agent_swarm", "label": "AGENT_VENTURE_MAP"},
        {"from": "decision_engine", "to": "DECISIONS.csv", "label": "Audit trail"},
        {"from": "loop_closer", "to": "Swarm adjustments", "label": "Feedback + execution"}
    ]

    cron_schedule = {
        "morning_chain": [
            {"time": "5:00", "script": "growth_strategist"},
            {"time": "5:30", "script": "venture self-manager"},
            {"time": "5:45", "script": "codebase grammar"},
            {"time": "6:00", "script": "twitter scraper + alpha review"},
            {"time": "6:15", "script": "reddit scraper"},
            {"time": "6:30", "script": "alpha auto-processor"},
            {"time": "6:45", "script": "daily digest"},
            {"time": "7:00", "script": "engagement planner"},
            {"time": "7:15", "script": "tactical engine"}
        ],
        "continuous": [
            {"interval": "15min", "script": "guardian pulse + keepalive"},
            {"interval": "30min", "script": "decision engine"},
            {"interval": "2h", "script": "CEO agent + loop closer + safety commit"},
            {"interval": "3h", "script": "signal aggregator + ops manager"},
            {"interval": "4h", "script": "venture autonomy + tracker"},
            {"interval": "6h", "script": "swarm health + memecoin + SAM.gov"}
        ],
        "daily": [
            {"time": "1 AM", "script": "ship engine layer1"},
            {"time": "2 AM", "script": "overnight master runner"},
            {"time": "3 AM", "script": "closed-loop pipeline"},
            {"time": "4 AM", "script": "lead enrichment + log rotation"},
            {"time": "9 PM", "script": "autonomous factory"},
            {"time": "11 PM", "script": "guardian improve"},
            {"time": "Midnight", "script": "warmup poster advance"}
        ],
        "weekly": [
            {"time": "Sun 2 AM", "script": "performance report"},
            {"time": "Sun 3 AM", "script": "full backup"},
            {"time": "Sun 4 AM", "script": "system clone"},
            {"time": "Mon", "script": "ASO, RPM, ecom"}
        ]
    }

    agent_topology = {
        "venture_agents": [
            {"name": "CONTENT", "type": "CONTENT", "interval": "4h"},
            {"name": "OUTBOUND", "type": "OUTBOUND", "interval": "4h"},
            {"name": "APP_FACTORY", "type": "APP_FACTORY", "interval": "4h"},
            {"name": "LOCAL_BIZ", "type": "LOCAL_BIZ", "interval": "4h"},
            {"name": "MONETIZATION", "type": "MONETIZATION", "interval": "4h"},
            {"name": "PRODUCT", "type": "PRODUCT", "interval": "4h"},
            {"name": "RESEARCH", "type": "RESEARCH", "interval": "4h"},
            {"name": "SCRAPING", "type": "SCRAPING", "interval": "4h"}
        ],
        "swarm_agents": {
            "META": ["swarm_brain (4h, Opus)", "meta_executor (4h, Opus)"],
            "DISCOVERY": ["gap_hunter", "opportunity_scanner", "competitor_stalker"],
            "ACTION": ["asset_deployer", "content_compounder", "lead_machine"],
            "MEDIA": ["video_factory", "image_factory"],
            "OPTIMIZE": ["seo_aso_optimizer", "conversion_optimizer", "quality_enforcer"],
            "QUALITY": ["quality_gate (2h, Opus)", "playwright_tester"],
            "INTELLIGENCE": ["trend_synthesizer", "cross_pollinator", "revenue_tracker"],
            "MAINTENANCE": ["system_healer", "data_janitor"],
            "GROWTH": ["distribution_engine", "inbound_maximizer", "social_poster", "growth_strategist (24h, Opus)"],
            "NOTIFICATION": ["alert_dispatcher"]
        }
    }

    # Try to get script statuses from log file mtimes
    script_statuses = {}
    for layer in hierarchy:
        for script in layer["scripts"]:
            sname = script["name"].replace(".py", "")
            status = "unknown"
            last_run = None
            # Check log files
            for log_dir in [LOGS_DIR, CLAUDE_LOGS]:
                for prefix in ["", "cron_", "swarm_", "auto_"]:
                    log_path = log_dir / f"{prefix}{sname}.log"
                    if log_path.exists():
                        try:
                            mtime = log_path.stat().st_mtime
                            last_run = datetime.fromtimestamp(mtime).isoformat()
                            age_hours = (datetime.now() - datetime.fromtimestamp(mtime)).total_seconds() / 3600
                            if age_hours < 6:
                                status = "active"
                            elif age_hours < 24:
                                status = "idle"
                            else:
                                status = "stale"
                        except Exception:
                            pass
                        break
                if last_run:
                    break
            script["status"] = status
            script["last_run"] = last_run

    # -----------------------------------------------------------------------
    # State files — check existence, size, mtime
    # -----------------------------------------------------------------------
    state_files_def = [
        {"name": "ceo_state.json", "desc": "CEO cycle count, decisions, timestamps", "path": "AUTOMATIONS/agent/ceo_agent/ceo_state.json"},
        {"name": "autonomy_state.json", "desc": "Venture pipelines, stages, results", "path": "AUTOMATIONS/agent/autonomy/autonomy_state.json"},
        {"name": "swarm_state.json", "desc": "Agent health, cycles, effectiveness scores", "path": "AUTOMATIONS/agent/swarm/swarm_state.json"},
        {"name": "twitter_warmup_state.json", "desc": "Warmup day, phase, post history", "path": "AUTOMATIONS/twitter_warmup_state.json"},
        {"name": "ALPHA_STAGING.csv", "desc": "Raw alpha intake (15,154 entries)", "path": "LEDGER/ALPHA_STAGING.csv"},
        {"name": "INTELLIGENCE_CATALOG.json", "desc": "487 docs, value scores, buried gold", "path": "OPS/INTELLIGENCE_CATALOG.json"},
        {"name": "decisions.jsonl", "desc": "CEO decision audit trail", "path": "AUTOMATIONS/agent/ceo_agent/decisions.jsonl"},
        {"name": "missions.jsonl", "desc": "Shared mission log", "path": "AUTOMATIONS/agent/missions.jsonl"},
        {"name": "message_bus.jsonl", "desc": "Inter-agent messages", "path": "AUTOMATIONS/agent/message_bus.jsonl"},
        {"name": "feedback_recommendations.json", "desc": "Loop closer to swarm adjustments", "path": "AUTOMATIONS/agent/swarm/feedback_recommendations.json"},
        {"name": "USER_PROMPTS.jsonl", "desc": "Every user prompt timestamped", "path": "LEDGER/USER_PROMPTS.jsonl"},
        {"name": "throttle_state.json", "desc": "Current throttle mode and overrides", "path": "AUTOMATIONS/throttle_state.json"}
    ]

    state_files = []
    for sf in state_files_def:
        full_path = PROJECT_ROOT / sf["path"]
        entry = dict(sf)
        if full_path.exists():
            try:
                stat = full_path.stat()
                entry["exists"] = True
                entry["size_kb"] = round(stat.st_size / 1024, 1)
                entry["last_modified"] = relative_time(stat.st_mtime)
            except Exception:
                entry["exists"] = True
                entry["size_kb"] = 0
                entry["last_modified"] = "unknown"
        else:
            entry["exists"] = False
            entry["size_kb"] = 0
            entry["last_modified"] = "never"
        state_files.append(entry)

    hooks = [
        {"event": "PreToolUse", "matcher": "Write|Edit", "desc": "Path validation — blocks writes outside project"},
        {"event": "PostToolUse", "matcher": "Edit|Write", "desc": "py_compile, secret detection, safe_path check, file handle leak check, type hints"},
        {"event": "SessionStart", "matcher": "*", "desc": "Cron check, subconscious injection, session briefing, control panel launch"},
        {"event": "UserPromptSubmit", "matcher": "*", "desc": "Log user prompts, sync memory"},
        {"event": "Stop", "matcher": "*", "desc": "Session end processing, memory sync"}
    ]

    directory_overview = [
        {"name": "AUTOMATIONS/", "desc": "THE BRAIN — 298 Python scripts, 5K files", "icon": "brain"},
        {"name": "LEDGER/", "desc": "DATA WAREHOUSE — 2,023 CSVs, 2.2K files", "icon": "database"},
        {"name": "OPS/", "desc": "OPERATIONS CENTER — 1.2K files", "icon": "settings"},
        {"name": "CONTENT/", "desc": "CONTENT ENGINE — 957 files", "icon": "pencil"},
        {"name": "MONEY_METHODS/", "desc": "REVENUE METHODS — 11.7K files", "icon": "coin"},
        {"name": "DIGITAL_PRODUCTS/", "desc": "13 products built, $0 listed", "icon": "package"},
        {"name": "MEDIA/", "desc": "MEDIA ASSETS — 11.5K files", "icon": "photo"},
        {"name": "FINANCIALS/", "desc": "MONEY TRACKING", "icon": "chart-bar"},
        {"name": "01_STRATEGY/", "desc": "Strategic planning docs", "icon": "target"},
        {"name": "03_PLAYBOOKS/", "desc": "19K files — agency, AI, local lead gen, ecom arb", "icon": "book"}
    ]

    revenue_status = {
        "current": "$0",
        "day": 35,
        "pipeline_ready": "13 digital products built. 40 posts queued. 1,110 leads. 16 live sites.",
        "human_time_to_unblock": "~85 min"
    }

    return {
        "hierarchy": hierarchy,
        "data_flow": data_flow,
        "cron_schedule": cron_schedule,
        "agent_topology": agent_topology,
        "state_files": state_files,
        "hooks": hooks,
        "directory_overview": directory_overview,
        "revenue_status": revenue_status
    }


# ---------------------------------------------------------------------------
# NEW: Master Ops API (parsed from xlsx)
# ---------------------------------------------------------------------------
_master_ops_cache = {"data": None, "timestamp": 0}


def get_master_ops():
    """Parse the latest PRINTMAXX_MASTER_OPS_ENHANCED xlsx and return structured JSON."""
    # 5-minute cache
    now = time.time()
    if _master_ops_cache["data"] and (now - _master_ops_cache["timestamp"]) < 300:
        return _master_ops_cache["data"]

    try:
        import openpyxl
    except ImportError:
        return {"error": "openpyxl not installed", "total_ops": 0}

    # Find latest xlsx
    xlsx_files = sorted(PROJECT_ROOT.glob("PRINTMAXX_MASTER_OPS_ENHANCED_*.xlsx"))
    if not xlsx_files:
        return {"error": "No PRINTMAXX_MASTER_OPS_ENHANCED_*.xlsx found", "total_ops": 0}

    xlsx_path = xlsx_files[-1]
    xlsx_name = xlsx_path.name
    # Extract date from filename: PRINTMAXX_MASTER_OPS_ENHANCED_2026-03-03.xlsx
    date_str = xlsx_name.replace("PRINTMAXX_MASTER_OPS_ENHANCED_", "").replace(".xlsx", "")

    try:
        wb = openpyxl.load_workbook(str(xlsx_path), read_only=True, data_only=True)
    except Exception as e:
        return {"error": f"Failed to open xlsx: {e}", "total_ops": 0}

    result = {
        "last_updated": date_str,
        "xlsx_file": xlsx_name,
        "total_ops": 0,
        "categories": [],
        "priority_launch": [],
        "synergy_stacks": [],
        "readiness": {"READY": 0, "BUILD": 0, "BLOCKED": 0},
        "venture_map": [],
        "alpha_thesis": [],
        "blocker_summary": [],
        "tool_stacks": {"video": [], "hosting": [], "lead_gen": []},
        "existing_infra": {"total": 0, "by_category": []}
    }

    try:
        # --- ALL OPS MASTER ---
        if "ALL OPS MASTER" in wb.sheetnames:
            ws = wb["ALL OPS MASTER"]
            headers = None
            ops_by_category = {}
            total_ops = 0
            for i, row in enumerate(ws.iter_rows(values_only=True)):
                if i == 0:
                    headers = [str(h).strip() if h else f"col_{j}" for j, h in enumerate(row)]
                    continue
                if not row or not row[0]:
                    continue
                total_ops += 1
                rd = {headers[j]: (row[j] if j < len(row) else None) for j in range(len(headers))}
                cat = str(rd.get("CATEGORY", "OTHER") or "OTHER")
                if cat not in ops_by_category:
                    ops_by_category[cat] = []
                ops_by_category[cat].append({
                    "op_id": str(rd.get("OP_ID", "") or ""),
                    "name": str(rd.get("OP_NAME", "") or ""),
                    "revenue": str(rd.get("REVENUE_RANGE", "") or ""),
                    "automation": str(rd.get("AUTOMATION_LEVEL", "") or ""),
                    "status": str(rd.get("STATUS", "") or ""),
                    "priority": str(rd.get("PRIORITY", "") or "")
                })
            result["total_ops"] = total_ops
            result["categories"] = [
                {"name": cat, "count": len(ops), "ops": ops}
                for cat, ops in sorted(ops_by_category.items())
            ]

        # --- PRIORITY LAUNCH ---
        if "PRIORITY LAUNCH" in wb.sheetnames:
            ws = wb["PRIORITY LAUNCH"]
            headers = None
            for i, row in enumerate(ws.iter_rows(values_only=True)):
                if i == 0:
                    headers = [str(h).strip() if h else f"col_{j}" for j, h in enumerate(row)]
                    continue
                if not row or row[0] is None:
                    continue
                rd = {headers[j]: (row[j] if j < len(row) else None) for j in range(len(headers))}
                result["priority_launch"].append({
                    "rank": rd.get("RANK", 0),
                    "op_id": str(rd.get("OP_ID", "") or ""),
                    "name": str(rd.get("OP_NAME", "") or ""),
                    "effort": str(rd.get("EFFORT", "") or ""),
                    "revenue": str(rd.get("REVENUE_POTENTIAL", "") or ""),
                    "first_step": str(rd.get("FIRST_STEP", "") or ""),
                    "time_to_first": str(rd.get("TIME_TO_FIRST_$", "") or "")
                })

        # --- SYNERGY STACKS ---
        if "SYNERGY STACKS" in wb.sheetnames:
            ws = wb["SYNERGY STACKS"]
            headers = None
            for i, row in enumerate(ws.iter_rows(values_only=True)):
                if i == 0:
                    headers = [str(h).strip() if h else f"col_{j}" for j, h in enumerate(row)]
                    continue
                if not row or not row[0]:
                    continue
                rd = {headers[j]: (row[j] if j < len(row) else None) for j in range(len(headers))}
                result["synergy_stacks"].append({
                    "id": str(rd.get("PACKAGE_ID", "") or ""),
                    "name": str(rd.get("NAME", "") or ""),
                    "score": rd.get("SYNERGY_SCORE", 0) or 0,
                    "multiplier": str(rd.get("REVENUE_MULTIPLIER", "") or ""),
                    "methods": str(rd.get("METHODS_COMBINED", "") or ""),
                    "description": str(rd.get("DESCRIPTION", "") or "")
                })

        # --- AUTO_STATUS_LIVE ---
        if "AUTO_STATUS_LIVE" in wb.sheetnames:
            ws = wb["AUTO_STATUS_LIVE"]
            headers = None
            readiness_counts = {"READY": 0, "BUILD": 0, "BLOCKED": 0}
            for i, row in enumerate(ws.iter_rows(values_only=True)):
                if i == 0:
                    headers = [str(h).strip() if h else f"col_{j}" for j, h in enumerate(row)]
                    continue
                if not row or not row[0]:
                    continue
                rd = {headers[j]: (row[j] if j < len(row) else None) for j in range(len(headers))}
                r_val = str(rd.get("READINESS", "") or "").upper()
                if r_val in readiness_counts:
                    readiness_counts[r_val] += 1
                elif r_val:
                    readiness_counts.setdefault(r_val, 0)
                    readiness_counts[r_val] += 1
            result["readiness"] = readiness_counts

        # --- VENTURE_AUTOMATION_MAP ---
        blocker_map = {}  # blocker_key -> list of venture_ids
        if "VENTURE_AUTOMATION_MAP" in wb.sheetnames:
            ws = wb["VENTURE_AUTOMATION_MAP"]
            headers = None
            for i, row in enumerate(ws.iter_rows(values_only=True)):
                if i == 0:
                    headers = [str(h).strip() if h else f"col_{j}" for j, h in enumerate(row)]
                    continue
                if not row or not row[0]:
                    continue
                rd = {headers[j]: (row[j] if j < len(row) else None) for j in range(len(headers))}
                vid = str(rd.get("VENTURE_ID", "") or "")
                blocker_key = str(rd.get("BLOCKER_KEY", "") or "")
                auto_score = rd.get("AUTOMATION_SCORE_100", 0) or 0
                signal_count = rd.get("SIGNAL_COUNT", 0) or 0
                result["venture_map"].append({
                    "venture_id": vid,
                    "name": str(rd.get("VENTURE_NAME", "") or ""),
                    "lane": str(rd.get("LANE", "") or ""),
                    "readiness": str(rd.get("READINESS", "") or ""),
                    "blocker": blocker_key,
                    "auto_score": auto_score,
                    "signal_count": signal_count
                })
                if blocker_key and blocker_key != "NONE":
                    if blocker_key not in blocker_map:
                        blocker_map[blocker_key] = []
                    blocker_map[blocker_key].append(vid)

        # Build blocker summary
        result["blocker_summary"] = [
            {"blocker": bk, "count": len(vids), "ventures_affected": vids}
            for bk, vids in sorted(blocker_map.items(), key=lambda x: -len(x[1]))
        ]

        # --- ALPHA_THESIS_INDEX ---
        if "ALPHA_THESIS_INDEX" in wb.sheetnames:
            ws = wb["ALPHA_THESIS_INDEX"]
            headers = None
            for i, row in enumerate(ws.iter_rows(values_only=True)):
                if i == 0:
                    headers = [str(h).strip() if h else f"col_{j}" for j, h in enumerate(row)]
                    continue
                if not row or not row[0]:
                    continue
                rd = {headers[j]: (row[j] if j < len(row) else None) for j in range(len(headers))}
                result["alpha_thesis"].append({
                    "id": str(rd.get("ALPHA_ID", "") or ""),
                    "opportunity": str(rd.get("OPPORTUNITY", "") or ""),
                    "lane": str(rd.get("LANE", "") or ""),
                    "edge_duration": str(rd.get("EDGE_DURATION", "") or ""),
                    "why_llm_edge": str(rd.get("WHY_LLM_EDGE", "") or "")
                })

        # --- VIDEO & MEDIA STACK ---
        if "VIDEO & MEDIA STACK" in wb.sheetnames:
            ws = wb["VIDEO & MEDIA STACK"]
            headers = None
            for i, row in enumerate(ws.iter_rows(values_only=True)):
                if i == 0:
                    headers = [str(h).strip() if h else f"col_{j}" for j, h in enumerate(row)]
                    continue
                if not row or not row[0]:
                    continue
                rd = {headers[j]: (row[j] if j < len(row) else None) for j in range(len(headers))}
                result["tool_stacks"]["video"].append({
                    "name": str(rd.get("TOOL", "") or ""),
                    "type": str(rd.get("TYPE", "") or ""),
                    "free_tier": str(rd.get("FREE_TIER", "") or ""),
                    "quality": str(rd.get("QUALITY", "") or "")
                })

        # --- HOSTING & DEPLOY ---
        if "HOSTING & DEPLOY" in wb.sheetnames:
            ws = wb["HOSTING & DEPLOY"]
            headers = None
            for i, row in enumerate(ws.iter_rows(values_only=True)):
                if i == 0:
                    headers = [str(h).strip() if h else f"col_{j}" for j, h in enumerate(row)]
                    continue
                if not row or not row[0]:
                    continue
                rd = {headers[j]: (row[j] if j < len(row) else None) for j in range(len(headers))}
                result["tool_stacks"]["hosting"].append({
                    "name": str(rd.get("PLATFORM", "") or ""),
                    "free_tier": str(rd.get("FREE_TIER", "") or ""),
                    "commercial": str(rd.get("COMMERCIAL_USE", "") or ""),
                    "best_for": str(rd.get("BEST_FOR", "") or "")
                })

        # --- LEAD GEN STACK ---
        if "LEAD GEN STACK" in wb.sheetnames:
            ws = wb["LEAD GEN STACK"]
            headers = None
            for i, row in enumerate(ws.iter_rows(values_only=True)):
                if i == 0:
                    headers = [str(h).strip() if h else f"col_{j}" for j, h in enumerate(row)]
                    continue
                if not row or not row[0]:
                    continue
                rd = {headers[j]: (row[j] if j < len(row) else None) for j in range(len(headers))}
                result["tool_stacks"]["lead_gen"].append({
                    "name": str(rd.get("TOOL", "") or ""),
                    "type": str(rd.get("TYPE", "") or ""),
                    "free_tier": str(rd.get("FREE_TIER", "") or ""),
                    "automation": str(rd.get("AUTOMATION_LEVEL", "") or "")
                })

        # --- EXISTING INFRA ---
        if "EXISTING INFRA" in wb.sheetnames:
            ws = wb["EXISTING INFRA"]
            headers = None
            infra_by_cat = {}
            infra_total = 0
            for i, row in enumerate(ws.iter_rows(values_only=True)):
                if i == 0:
                    headers = [str(h).strip() if h else f"col_{j}" for j, h in enumerate(row)]
                    continue
                if not row or not row[0]:
                    continue
                infra_total += 1
                rd = {headers[j]: (row[j] if j < len(row) else None) for j in range(len(headers))}
                cat = str(rd.get("CATEGORY", "OTHER") or "OTHER")
                if cat not in infra_by_cat:
                    infra_by_cat[cat] = []
                infra_by_cat[cat].append({
                    "name": str(rd.get("ITEM", "") or ""),
                    "status": str(rd.get("STATUS", "") or ""),
                    "notes": str(rd.get("NOTES", "") or "")
                })
            result["existing_infra"]["total"] = infra_total
            result["existing_infra"]["by_category"] = [
                {"category": cat, "count": len(items), "items": items}
                for cat, items in sorted(infra_by_cat.items())
            ]

    except Exception as e:
        result["parse_error"] = str(e)
    finally:
        try:
            wb.close()
        except Exception:
            pass

    _master_ops_cache["data"] = result
    _master_ops_cache["timestamp"] = now
    return result


# ---------------------------------------------------------------------------
# NEW: Real-time metrics API
# ---------------------------------------------------------------------------
def get_realtime_data():
    """Return time-series data for real-time charts."""
    now = datetime.now()
    data_points = []

    # Scan log files for modification times in last 24h to build activity timeline
    log_dirs = [LOGS_DIR, CLAUDE_LOGS]
    activity_counts = Counter()

    for log_dir in log_dirs:
        if not log_dir.exists():
            continue
        try:
            for log_file in log_dir.iterdir():
                if not log_file.is_file() or not log_file.name.endswith(".log"):
                    continue
                try:
                    mtime = datetime.fromtimestamp(log_file.stat().st_mtime)
                    if (now - mtime).total_seconds() < 86400:
                        # Bucket into hourly slots
                        hour_key = mtime.replace(minute=0, second=0, microsecond=0)
                        activity_counts[hour_key.isoformat()] += 1
                except Exception:
                    continue
        except Exception:
            continue

    # Build 24-hour timeline
    for i in range(24):
        t = (now - timedelta(hours=23 - i)).replace(minute=0, second=0, microsecond=0)
        key = t.isoformat()
        data_points.append({
            "timestamp": int(t.timestamp() * 1000),
            "invocations": activity_counts.get(key, 0)
        })

    # Alpha entries over time (from ALPHA_STAGING.csv timestamps)
    alpha_timeline = []
    alpha_path = LEDGER / "ALPHA_STAGING.csv"
    if alpha_path.exists():
        alpha_counts = Counter()
        try:
            with open(alpha_path, "r", encoding="utf-8", errors="replace") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    ts_str = row.get("timestamp", row.get("created_at", row.get("date", "")))
                    if ts_str:
                        try:
                            ts = datetime.fromisoformat(ts_str.replace("Z", "+00:00").split("+")[0])
                            day_key = ts.strftime("%Y-%m-%d")
                            alpha_counts[day_key] += 1
                        except Exception:
                            pass
        except Exception:
            pass

        # Last 7 days of alpha
        for i in range(7):
            day = (now - timedelta(days=6 - i)).strftime("%Y-%m-%d")
            alpha_timeline.append({
                "date": day,
                "count": alpha_counts.get(day, 0)
            })

    # System events from recent logs
    events = []
    if LOGS_DIR.exists():
        try:
            log_files = sorted(LOGS_DIR.iterdir(), key=lambda p: p.stat().st_mtime, reverse=True)
            for lf in log_files[:10]:
                if lf.is_file() and lf.name.endswith(".log"):
                    try:
                        mtime = datetime.fromtimestamp(lf.stat().st_mtime)
                        events.append({
                            "name": lf.stem,
                            "time": mtime.isoformat(),
                            "ago": relative_time(mtime)
                        })
                    except Exception:
                        pass
        except Exception:
            pass

    return {
        "agent_activity": data_points,
        "alpha_timeline": alpha_timeline,
        "recent_events": events
    }


# ---------------------------------------------------------------------------
# NEW: Venture status API
# ---------------------------------------------------------------------------
def get_venture_status():
    """Return venture status from autonomy_state.json."""
    state_path = AUTOMATIONS / "agent" / "autonomy" / "autonomy_state.json"
    state = safe_read_json(state_path)
    ventures = state.get("ventures", {})

    result = []
    for vid, v in ventures.items():
        last_run = v.get("last_run", "")
        result.append({
            "id": vid,
            "name": v.get("name", vid),
            "type": v.get("type", "UNKNOWN"),
            "status": v.get("status", "UNKNOWN"),
            "interval_hours": v.get("interval_hours", 0),
            "cycles_run": v.get("cycles_run", 0),
            "last_run": last_run,
            "last_run_ago": relative_time(last_run) if last_run else "never",
            "pipeline": v.get("pipeline", []),
            "latest_result": v.get("results", [{}])[-1] if v.get("results") else {}
        })

    return {"ventures": result}


# ---------------------------------------------------------------------------
# NEW: Pipeline funnel API
# ---------------------------------------------------------------------------
def get_pipeline():
    """Return pipeline stages: alpha pending -> approved -> routed -> deployed -> revenue."""
    alpha_path = LEDGER / "ALPHA_STAGING.csv"
    stages = {
        "pending": 0,
        "approved": 0,
        "routed": 0,
        "deployed": 0,
        "revenue": 0
    }

    if alpha_path.exists():
        rows = safe_read_csv(alpha_path, max_rows=50000)
        for r in rows:
            status = r.get("status", "").upper()
            if status == "PENDING_REVIEW":
                stages["pending"] += 1
            elif status == "APPROVED":
                stages["approved"] += 1
            elif status in ("ROUTED", "INTEGRATED", "PROCESSED"):
                stages["routed"] += 1
            elif status in ("DEPLOYED", "LIVE", "PUBLISHED"):
                stages["deployed"] += 1
            elif status in ("REVENUE", "MONETIZED"):
                stages["revenue"] += 1

    # Check revenue tracker
    rev_path = FINANCIALS / "REVENUE_TRACKER.csv"
    if rev_path.exists():
        rev_rows = safe_read_csv(rev_path, max_rows=1000)
        total_rev = sum(float(r.get("amount", 0)) for r in rev_rows if r.get("amount"))
        stages["total_revenue"] = f"${total_rev:,.0f}"
    else:
        stages["total_revenue"] = "$0"

    # Add total alpha count
    stages["total_alpha"] = stages["pending"] + stages["approved"] + stages["routed"] + stages["deployed"] + stages["revenue"]

    return stages


# ---------------------------------------------------------------------------
# API Routes
# ---------------------------------------------------------------------------
@app.route("/")
def index():
    if HTML_PATH.exists():
        with open(HTML_PATH, "r") as f:
            return Response(f.read(), mimetype="text/html")
    return "<h1>Control panel HTML not found</h1>", 404


@app.route("/api/status")
def api_status():
    throttle = get_throttle_status()
    system = get_system_status()
    return jsonify({
        "throttle": throttle,
        "system": system,
        "days_until_reset": days_until_friday(),
    })


@app.route("/api/agents")
def api_agents():
    return jsonify(get_throttle_status())


@app.route("/api/mode", methods=["POST"])
def api_mode():
    data = request.get_json(force=True)
    mode = data.get("mode", "efficient")
    if mode not in ("efficient", "high"):
        return jsonify({"error": "mode must be 'efficient' or 'high'"}), 400
    result = set_throttle_mode(mode)
    return jsonify(result)


@app.route("/api/agent/<agent_id>/toggle", methods=["POST"])
def api_toggle_agent(agent_id):
    data = request.get_json(force=True)
    enabled = data.get("enabled", True)
    result = toggle_agent(agent_id, enabled)
    return jsonify(result)


@app.route("/api/agent/<agent_id>/interval", methods=["POST"])
def api_set_interval(agent_id):
    data = request.get_json(force=True)
    hours = data.get("hours", 24)
    if hours <= 0:
        return jsonify({"error": "hours must be > 0"}), 400
    result = set_agent_interval(agent_id, hours)
    return jsonify(result)


@app.route("/api/logs/<agent_id>")
def api_logs(agent_id):
    lines = int(request.args.get("lines", 30))
    return jsonify({"agent_id": agent_id, "log": get_log_tail(agent_id, lines)})


@app.route("/api/actions")
def api_actions():
    return jsonify({"actions": get_quick_actions()})


@app.route("/api/action/<action_id>", methods=["POST"])
def api_run_action(action_id):
    actions = {a["id"]: a for a in get_quick_actions()}
    if action_id not in actions:
        return jsonify({"error": f"unknown action: {action_id}"}), 404
    action = actions[action_id]
    cmd_parts = action["cmd"].split()
    code, out, err = run_cmd(cmd_parts, timeout=120)
    return jsonify({"success": code == 0, "output": out[-3000:], "error": err[-1000:]})


@app.route("/api/commands")
def api_commands():
    return jsonify({"commands": get_slash_commands()})


@app.route("/api/sites")
def api_sites():
    return jsonify({"sites": get_deployed_sites()})


@app.route("/api/blockers")
def api_blockers():
    """Read P0 blockers from task tracker."""
    tracker_path = OPS / "PERSISTENT_TASK_TRACKER.md"
    blockers = []
    if tracker_path.exists():
        content = safe_read(tracker_path, max_lines=200)
        in_p0 = False
        for line in content.split("\n"):
            if "[P0]" in line:
                in_p0 = True
                continue
            if line.startswith("## [P") and "[P0]" not in line:
                in_p0 = False
            if in_p0 and line.strip().startswith("- ["):
                blockers.append(line.strip())
    return jsonify({"blockers": blockers})


# --- NEW API ENDPOINTS ---

@app.route("/api/system-tree")
def api_system_tree():
    return jsonify(get_system_tree())


@app.route("/api/realtime")
def api_realtime():
    return jsonify(get_realtime_data())


@app.route("/api/ventures")
def api_ventures():
    return jsonify(get_venture_status())


@app.route("/api/pipeline")
def api_pipeline():
    return jsonify(get_pipeline())


@app.route("/api/master-ops")
def api_master_ops():
    return jsonify(get_master_ops())


# ---------------------------------------------------------------------------
# Sovrun + n8n helpers
# ---------------------------------------------------------------------------
def _n8n_request(path, method="GET"):
    """Make a request to the n8n API. Returns parsed JSON or error dict."""
    if not N8N_API_KEY:
        return {"error": "N8N_API_KEY not configured in .env"}
    url = f"{N8N_BASE}/api/v1{path}"
    headers = {"X-N8N-API-KEY": N8N_API_KEY, "Accept": "application/json"}
    try:
        req = Request(url, headers=headers, method=method)
        with urlopen(req, timeout=10) as resp:
            return json.loads(resp.read().decode())
    except URLError as e:
        return {"error": f"n8n unreachable: {e.reason}"}
    except Exception as e:
        return {"error": str(e)}


def _get_skills_db():
    """Return path to the skills.db that exists, or None."""
    for p in [SOVRUN_SKILLS_DB, SOVRUN_SKILLS_DB_ALT]:
        if p.exists():
            return p
    return None


def get_sovrun_skills(query=""):
    """Query procedural memory FTS5 for skill docs."""
    db_path = _get_skills_db()
    if not db_path:
        return {"error": "skills.db not found", "skills": []}
    try:
        conn = sqlite3.connect(str(db_path))
        conn.row_factory = sqlite3.Row
        if query:
            # Try FTS5 first
            try:
                rows = conn.execute(
                    "SELECT * FROM skills_fts WHERE skills_fts MATCH ? ORDER BY rank LIMIT 50",
                    (query,)
                ).fetchall()
            except Exception:
                # Fallback to LIKE
                rows = conn.execute(
                    "SELECT * FROM skills WHERE name LIKE ? OR description LIKE ? LIMIT 50",
                    (f"%{query}%", f"%{query}%")
                ).fetchall()
        else:
            rows = conn.execute("SELECT * FROM skills ORDER BY rowid DESC LIMIT 50").fetchall()
        skills = [dict(r) for r in rows]
        conn.close()
        return {"skills": skills, "count": len(skills), "query": query}
    except Exception as e:
        return {"error": str(e), "skills": []}


def get_handoff_chains():
    """Return the 5 handoff chains and basic status."""
    chains_def = {
        "local_biz": [
            "savvy_lead_scraper", "lead_enrichment", "eas_lead_pipeline",
            "cold_email_generator", "follow_up_tracker",
        ],
        "content_factory": [
            "alpha_scanner", "topic_selector", "content_generator",
            "voice_injector", "platform_formatter",
        ],
        "product_launch": [
            "demand_scanner", "product_builder", "listing_creator",
            "distribution_engine", "sales_tracker",
        ],
        "freelance": [
            "job_scanner", "proposal_writer", "submission_tracker",
            "delivery_manager", "review_collector",
        ],
        "alpha_to_revenue": [
            "scraper_fleet", "alpha_processor", "intelligence_router",
            "capital_genesis_ranker", "venture_autonomy",
        ],
    }
    result = []
    for name, steps in chains_def.items():
        result.append({
            "name": name,
            "steps": steps,
            "step_count": len(steps),
        })
    return {"chains": result}


def get_dag_status():
    """Read morning intelligence DAG checkpoint/state."""
    data = {"checkpoint": None, "state": None}
    if DAG_CHECKPOINT.exists():
        data["checkpoint"] = safe_read_json(DAG_CHECKPOINT)
    if DAG_STATE.exists():
        data["state"] = safe_read_json(DAG_STATE)

    # Build the DAG structure for visualization
    dag_steps = [
        {"name": "scrape_twitter", "depends_on": [], "layer": 1, "desc": "Twitter (133 accounts)"},
        {"name": "scrape_reddit", "depends_on": [], "layer": 1, "desc": "Reddit (18 subreddits)"},
        {"name": "scrape_hn", "depends_on": [], "layer": 1, "desc": "HN + ProductHunt"},
        {"name": "merge_results", "depends_on": ["scrape_twitter", "scrape_reddit", "scrape_hn"], "layer": 2, "desc": "Merge scraper results"},
        {"name": "alpha_processor", "depends_on": ["merge_results"], "layer": 3, "desc": "Process new alpha"},
        {"name": "intelligence_router", "depends_on": ["alpha_processor"], "layer": 4, "desc": "Route through intel"},
        {"name": "capital_genesis_ranker", "depends_on": ["intelligence_router"], "layer": 5, "desc": "Rank by Capital Genesis"},
    ]

    # Enrich with status from checkpoint
    cp = data.get("checkpoint") or {}
    step_statuses = cp.get("step_statuses", cp.get("steps", {}))
    for step in dag_steps:
        sname = step["name"]
        if isinstance(step_statuses, dict) and sname in step_statuses:
            ss = step_statuses[sname]
            if isinstance(ss, dict):
                step["status"] = ss.get("status", "pending")
                step["duration"] = ss.get("duration_seconds", ss.get("duration", None))
            else:
                step["status"] = str(ss)
        else:
            step["status"] = "pending"

    data["dag_steps"] = dag_steps
    return data


# --- Sovrun + n8n API routes ---

@app.route("/api/n8n/workflows")
def api_n8n_workflows():
    data = _n8n_request("/workflows")
    return jsonify(data)


@app.route("/api/n8n/executions")
def api_n8n_executions():
    limit = request.args.get("limit", "20")
    data = _n8n_request(f"/executions?limit={limit}")
    return jsonify(data)


@app.route("/api/sovrun/skills")
def api_sovrun_skills():
    query = request.args.get("q", "")
    return jsonify(get_sovrun_skills(query))


@app.route("/api/sovrun/chains")
def api_sovrun_chains():
    return jsonify(get_handoff_chains())


@app.route("/api/sovrun/chains/<chain_name>/run", methods=["POST"])
def api_run_chain(chain_name):
    code, out, err = run_cmd(
        [PYTHON, str(AUTOMATIONS / "agent_swarm.py"), "--chain", chain_name],
        timeout=120
    )
    return jsonify({"success": code == 0, "output": out[-3000:], "error": err[-1000:]})


@app.route("/api/sovrun/dag")
def api_sovrun_dag():
    return jsonify(get_dag_status())


@app.route("/api/kpi")
def api_kpi():
    """Return KPI data: revenue, blockers, daily targets, week progress."""
    kpi = {"revenue": 0, "by_source": {}, "blockers": [], "daily_targets": [], "week": 0, "month_target": 1000}

    # Revenue from available sources
    for csv_name, source_key in [("GUMROAD_SALES.csv", "gumroad"), ("FREELANCE_EARNINGS.csv", "freelance"), ("STRIPE_SALES.csv", "stripe")]:
        csv_path = LEDGER / csv_name
        if csv_path.exists():
            try:
                with open(csv_path) as f:
                    for row in csv.DictReader(f):
                        amt = float((row.get("amount", row.get("price", "0")) or "0").replace("$", "").replace(",", ""))
                        kpi["revenue"] += amt
                        kpi["by_source"][source_key] = kpi["by_source"].get(source_key, 0) + amt
            except Exception:
                pass

    # Human blockers
    roadmap = OPS / "MONTHLY_ROADMAP_2026_04.md"
    if roadmap.exists():
        in_blockers = False
        with open(roadmap) as f:
            for line in f:
                if "HUMAN BLOCKERS" in line:
                    in_blockers = True
                elif in_blockers and line.startswith("- ["):
                    done = line.startswith("- [x]")
                    text = line[5:].strip() if done else line[5:].strip()
                    kpi["blockers"].append({"text": text, "done": done})
                elif in_blockers and not line.strip():
                    break

    # Week number
    import calendar
    day = datetime.now().day
    kpi["week"] = min((day - 1) // 7 + 1, 4)

    # Weekly check-in data
    checkin = OPS / "KPI_WEEKLY_CHECKIN.md"
    if checkin.exists():
        kpi["has_weekly_checkin"] = True
        kpi["checkin_date"] = datetime.fromtimestamp(checkin.stat().st_mtime).strftime("%Y-%m-%d")

    return jsonify(kpi)


@app.route("/api/kpi/complete", methods=["POST"])
def api_kpi_complete():
    """Mark a blocker as complete."""
    data = request.get_json() or {}
    blocker_text = data.get("text", "")
    roadmap = OPS / "MONTHLY_ROADMAP_2026_04.md"
    if roadmap.exists() and blocker_text:
        content = roadmap.read_text()
        old = f"- [ ] {blocker_text}"
        new = f"- [x] {blocker_text}"
        if old in content:
            roadmap.write_text(content.replace(old, new))
            return jsonify({"success": True})
    return jsonify({"success": False})


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    print(f"\n  PRINTMAXX CONTROL PANEL")
    print(f"  http://localhost:{PORT}")
    print(f"  Press Ctrl+C to stop\n")

    # Auto-open browser after short delay
    def open_browser():
        time.sleep(1.5)
        webbrowser.open(f"http://localhost:{PORT}")

    threading.Thread(target=open_browser, daemon=True).start()

    try:
        app.run(host="0.0.0.0", port=PORT, debug=False)
    except KeyboardInterrupt:
        print("\n  Shutting down.")


if __name__ == "__main__":
    main()
