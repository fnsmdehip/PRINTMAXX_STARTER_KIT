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


@app.route("/api/kpi/calendar")
def api_kpi_calendar():
    """Return full month calendar with daily KPIs and tasks."""
    import calendar
    now = datetime.now()
    year, month = now.year, now.month + 1 if now.month < 12 else 1  # next month (April)
    if now.month == 12: year += 1
    _, days_in_month = calendar.monthrange(year, month)

    # ==========================================================================
    # PRINTMAXX DAILY OPS — 33-AGENT AUTONOMOUS SYSTEM KPIs
    # ==========================================================================
    # Week 1: INFRA + ACCOUNTS (multi-account stack, proxy setup, product listings, first outreach)
    # Week 2: VOLUME + PIPELINE (3x content across accounts, cold email at scale, gov contracts, freelance)
    # Week 3: EDGE + OPTIMIZE (growth engine tactics, kill/scale, arbitrage, secondary account amplification)
    # Week 4: COMPOUND + CLOSE (recurring revenue, retainers, community, full system audit)
    daily_plans = {
        # ===== WEEK 1: INFRA + ACCOUNTS =====
        1: {
            "theme": "MULTI-ACCOUNT GENESIS",
            "tasks": [
                # ACCOUNTS
                "Set up GoLogin with 6 browser profiles: @PRINTMAXXER (primary), 2 niche accounts (fitness/golf, finance), 2 content farm accounts, 1 findom persona",
                "Assign SOAX mobile proxy to each GoLogin profile (unique residential IP per account, geo-match to account location)",
                "Create 3 secondary X/Twitter accounts in GoLogin profiles — each gets its own niche, voice, and bio",
                "Subscribe X Premium Basic ($3/mo) on primary + 2 secondary accounts ($9 total) for 10x impression boost",
                # CONTENT
                "Post 8 tweets from primary @PRINTMAXXER queue + 1 thread: what you are building",
                "Run content_factory.py --batch-alpha 5 to generate cross-platform content from latest alpha",
                "Generate 3 faceless video scripts via ai_video_content_pipeline.py --generate golf --count 3 for boomer YouTube",
                # ENGAGEMENT
                "Reply to 40 accounts from primary within 15 min of target posting (reply guy = 150x a like in algo weight)",
                "Post 3 tweets per secondary account (warmup phase: quality over volume, first 100 tweets set algo foundation)",
                # REVENUE
                "Create Gumroad account + list all 13 products with price anchoring ($197 crossed out, $97 shown)",
                "Create Whop storefront + list top 8 products (5.7% fee vs Gumroad 10%)",
                # AUTOMATION
                "Verify 112 cron jobs ran: check system_health_monitor.py --quick output",
                "Verify twitter_alpha_scraper.py output at LEDGER/TWITTER_ALPHA_SCRAPES.csv (133 accounts scraped at 6AM)",
                "Verify background_reddit_scraper.py output at LEDGER/REDDIT_SCRAPES/ (ran at 6:15AM)",
                "Check soul_drift_report.json — any agent below 6/10 gets prompt rewrite immediately"
            ],
            "revenue_target": "$0",
            "content": {"tweets": 14, "threads": 1, "tiktoks": 0, "youtube": 3, "newsletters": 0},
            "engagement": {"replies": 40, "dms": 5, "comments": 10, "follows": 25},
            "outreach": {"cold_emails": 0, "proposals": 0, "calls": 0},
            "automation_checks": [
                "cron health: system_health_monitor.py --quick (112 jobs)",
                "twitter_alpha_scraper.py: 133 accounts, 6AM cron",
                "background_reddit_scraper.py: 6:15AM cron",
                "soul_drift_report.json: all agents > 6/10",
                "GoLogin profiles: 6 profiles with unique SOAX proxies"
            ],
            "research": [
                "CAPITAL_GENESIS_PRIORITY_STACK.md: daily ranked priorities",
                "daily_tool_scout.py output: new tools discovered",
                "ALPHA_STAGING.csv: process 50 PENDING_REVIEW entries"
            ]
        },
        2: {
            "theme": "FREELANCE + PRODUCT BLITZ",
            "tasks": [
                # ACCOUNTS
                "Warm up 3 secondary X accounts: 5 tweets each, 15 genuine replies each, follow 20 niche accounts each (stagger 30+ min between accounts)",
                "Create Fiverr account + post 5 gigs: AI automation ($150), Claude Code dev ($200), chatbot build ($100), data pipeline ($175), web scraping ($125)",
                "Create Upwork profile + submit 10 proposals on AI/automation jobs with $1K+ budgets",
                # CONTENT
                "Post 8 tweets + 1 thread from primary: 'I build apps in 2 hours that agencies quote $10K for'",
                "Generate product thumbnails for all 13 Gumroad products using Playwright screenshot factory",
                "Run auto_clip_pipeline.py --demo on 2 trending YouTube videos in AI niche to identify clip opportunities",
                # ENGAGEMENT
                "Reply to 50 accounts from primary (target: anyone tweeting about manual processes, hiring devs, or needing automation)",
                "DM 10 people who tweeted about manual work pain points with genuine value (no pitch)",
                "Post in 2 X Communities relevant to automation/AI before tweeting (30-min velocity window hack)",
                # REVENUE
                "Run fiverr_gig_scraper.py --category resume to analyze competitor pricing and delivery times",
                "Set Fiverr launch price at $25 for first gig to accelerate first review acquisition",
                # AUTOMATION
                "Verify agent_swarm.py --status: 25 agents operational (4 Opus, 5 Sonnet, 3 Haiku)",
                "Verify n8n workflow w01 (GMaps lead scraper) executed, check LEDGER for new leads",
                "Verify n8n workflow w04 (cold email SendGrid) is ready for Day 4 launch",
                "Check alpha_auto_processor.py output: process any PENDING_REVIEW entries"
            ],
            "revenue_target": "$0-20",
            "content": {"tweets": 23, "threads": 1, "tiktoks": 0, "youtube": 0, "newsletters": 0},
            "engagement": {"replies": 50, "dms": 10, "comments": 15, "follows": 60},
            "outreach": {"cold_emails": 0, "proposals": 10, "calls": 0},
            "automation_checks": [
                "agent_swarm.py --status: 25 agents, model routing check",
                "n8n w01 GMaps lead scraper execution",
                "n8n w04 cold email SendGrid readiness",
                "alpha_auto_processor.py: PENDING_REVIEW cleared",
                "fiverr_gig_scraper.py: competitor analysis complete"
            ],
            "research": [
                "Fiverr AI category: pricing, delivery times, top sellers",
                "Upwork trending skills: which AI jobs are paying $2K+",
                "GREY_HAT_EDGE_GROWTH_MASTER.md: warmup protocols (Section 11)"
            ]
        },
        3: {
            "theme": "GOV CONTRACTS + EAS PIPELINE",
            "tasks": [
                # ACCOUNTS
                "Continue secondary account warmup: 5 tweets + 20 replies per secondary account (unique content per account, never cross-post identical text)",
                "Set up GoLogin profile for LinkedIn automation (separate from Twitter profiles)",
                # CONTENT
                "Post 8 tweets + 2 threads from primary (1 freelance value thread, 1 build-in-public thread)",
                "Generate 5 TikTok scripts via ai_video_content_pipeline.py --generate fitness --count 5",
                "Create 3 LinkedIn posts repurposing best tweets with B2B framing for EAS",
                # ENGAGEMENT
                "Reply to 50 accounts from primary + 10 replies per secondary (80 total)",
                "Comment on 5 LinkedIn posts about business automation (value-add, link EAS site in profile)",
                # REVENUE
                "Run sam_gov_monitor.py to scan SAM.gov for IT/software/automation contracts matching NAICS 541511-541990",
                "Run uk_contracts_finder.py --categories IT consulting marketing to scan UK procurement opportunities",
                "Review LEDGER/GOV_OPPORTUNITIES.csv: identify top 3 contracts we can bid on with Claude Code capabilities",
                "Run eas_lead_pipeline.py: scrape + score 50 local businesses with outdated websites",
                "Draft 3 EAS cold email templates: Signal Map intro ($1,500), Phone Pilot pitch ($3,500), Ops Pilot value prop ($4,500)",
                # AUTOMATION
                "Verify venture_autonomy.py --status: all 8 venture types active (OUTBOUND, CONTENT, APP, LOCAL_BIZ, RESEARCH, MONETIZE, PRODUCT, SCRAPING)",
                "Verify daily_engagement_planner.py ran at 7AM, review today's engagement plan",
                "Check n8n w09 (content repurpose) execution status"
            ],
            "revenue_target": "$0-30",
            "content": {"tweets": 24, "threads": 2, "tiktoks": 5, "youtube": 0, "newsletters": 0},
            "engagement": {"replies": 80, "dms": 5, "comments": 15, "follows": 35},
            "outreach": {"cold_emails": 0, "proposals": 10, "calls": 0},
            "automation_checks": [
                "sam_gov_monitor.py: NAICS codes 541511-541990 scan",
                "uk_contracts_finder.py: IT/consulting/marketing scan",
                "eas_lead_pipeline.py: 50 leads scored (8AM cron)",
                "venture_autonomy.py --status: 8 venture types",
                "daily_engagement_planner.py: 7AM cron verified"
            ],
            "research": [
                "GOV_OPPORTUNITIES.csv: top 3 biddable contracts",
                "EAS competitor pricing: dental/legal/HVAC verticals",
                "BOOMER_MALE_55_70_AFFILIATE.md: content angles for faceless YouTube"
            ]
        },
        4: {
            "theme": "COLD OUTREACH IGNITION",
            "tasks": [
                # ACCOUNTS
                "Create TikTok account + post first 3 videos (screen recordings of AI builds, real phone, no VPN)",
                "Create Pinterest account + pin 10 affiliate-linked products with SEO-optimized descriptions",
                "Cross-promote: secondary accounts repost/quote-tweet primary content (stagger 2+ hours apart)",
                # CONTENT
                "Post 10 tweets + 1 thread from primary: breakdown of a real automation build",
                "Post 5 tweets per secondary account: niche-specific content (never identical to primary)",
                "Run content_factory.py --batch-alpha 10 to generate multi-platform content batch",
                "Post 3 TikToks (cross-post adapted versions to YouTube Shorts + Instagram Reels)",
                # ENGAGEMENT
                "Reply to 60 accounts from primary + 15 per secondary (90 total)",
                "DM 15 people: 5 who tweeted about hiring devs, 5 who need automation, 5 potential collaborators",
                "Comment on 10 Reddit posts: r/freelance, r/automation, r/smallbusiness, r/Entrepreneur (genuine value, link in profile)",
                # REVENUE
                "Launch cold email via n8n w04: 50 emails to local businesses with outdated websites from eas_lead_pipeline scored list",
                "Submit 10 more Upwork proposals (20 total active, target $2K+ projects)",
                "Check Fiverr for new buyer requests in AI/automation categories, respond to all within 1 hour",
                # AUTOMATION
                "Verify eas_lead_pipeline.py 8AM cron: check scored leads in LEDGER/",
                "Verify method_discovery_crawler.py 5AM cron: any new P0 methods in OPS/CAPITAL_GENESIS_PRIORITY_STACK.md?",
                "Verify edge_growth_engine.py is tracking engagement ratios per account within platform limits",
                "Check n8n w14 (Stripe product delivery) webhook readiness for first sale"
            ],
            "revenue_target": "$0-50",
            "content": {"tweets": 20, "threads": 1, "tiktoks": 3, "youtube": 0, "newsletters": 0},
            "engagement": {"replies": 90, "dms": 15, "comments": 20, "follows": 45},
            "outreach": {"cold_emails": 50, "proposals": 10, "calls": 0},
            "automation_checks": [
                "n8n w04 cold email: 50 emails sent, bounce rate < 5%",
                "eas_lead_pipeline.py: scored leads accuracy check",
                "method_discovery_crawler.py: 5AM cron output",
                "edge_growth_engine.py: per-account engagement ratios",
                "n8n w14 Stripe webhook: ready for first sale"
            ],
            "research": [
                "CAPITAL_GENESIS_PRIORITY_STACK.md: new P0 methods",
                "Reddit r/automation + r/freelance: hot job threads",
                "DEFINITIVE_GROWTH_STACK.md: engagement escalation section"
            ]
        },
        5: {
            "theme": "E-COMMERCE + ARBITRAGE SCAN",
            "tasks": [
                # ACCOUNTS
                "Set up Fanvue account for persona venture P02 (findom, separate GoLogin profile + SOAX proxy)",
                "Set up Beehiiv newsletter account + create lead magnet PDF (free automation checklist)",
                # CONTENT
                "Post 10 tweets + 1 thread from primary: 'I sent 50 cold emails, here is what happened' (real-time case study)",
                "Post 5 tweets per secondary (10 total), each adapted to its niche voice",
                "Generate 3 faceless YouTube scripts via ai_video_content_pipeline.py --generate health --count 3 (boomer targeting)",
                "Run auto_clip_pipeline.py --url [trending video] --max-clips 5 to batch-clip viral content",
                # ENGAGEMENT
                "Reply to 60 accounts from primary + 20 from secondaries (80 total)",
                "DM 10 mid-tier accounts (2K-20K followers) offering free template in exchange for feedback/testimonial",
                # REVENUE
                "Scan Facebook/TikTok ads libraries for winning products (TikTok Shop arbitrage E01)",
                "List top 3 winning products on TikTok Shop or appropriate e-commerce platform",
                "Send cold email batch 2: 50 more emails (100 total) via n8n w04, A/B test subject lines",
                "Follow up on batch 1 non-openers with different subject line (auto via SendGrid sequence)",
                "Run auto_freelance_responder.py --scan-and-respond to auto-generate proposals for hot Reddit/Upwork jobs",
                # AUTOMATION
                "Verify twitter_warmup_poster.py warmup day status + advancement",
                "Check cold email analytics: open rates (target >40%), reply rates (target >2%), bounce rates (target <5%)",
                "Verify capital_genesis_ranker.py 5:30AM cron: review updated priority stack",
                "Check n8n w13 (Reddit pain point miner) output: any EAS prospects identified?"
            ],
            "revenue_target": "$0-75",
            "content": {"tweets": 20, "threads": 1, "tiktoks": 0, "youtube": 3, "newsletters": 0},
            "engagement": {"replies": 80, "dms": 10, "comments": 10, "follows": 40},
            "outreach": {"cold_emails": 50, "proposals": 5, "calls": 0},
            "automation_checks": [
                "twitter_warmup_poster.py: warmup day advancement",
                "cold email analytics: open/reply/bounce rates",
                "capital_genesis_ranker.py: 5:30AM cron output",
                "n8n w13 Reddit pain miner: EAS prospect alerts",
                "auto_freelance_responder.py: proposals generated"
            ],
            "research": [
                "TikTok/Facebook ads library: winning product scan",
                "cold email A/B test results: best subject lines",
                "Fanvue competitor analysis: pricing, content strategy"
            ]
        },
        6: {
            "theme": "WEEK 1 WAR ROOM",
            "tasks": [
                # ACCOUNTS
                "Audit all GoLogin profiles: verify each has unique SOAX IP, no fingerprint overlap, no shared cookies",
                "Check shadowban status on all accounts: shadowban.eu for X, engagement rate drop for others",
                # CONTENT
                "Batch create 30 tweets + 7 threads for primary + 15 tweets per secondary for Week 2",
                "Script 5 TikToks from ai_video_content_pipeline.py --generate fitness --count 5",
                # ENGAGEMENT
                "Reply to 30 accounts (reduced volume Saturday, increase quality)",
                "Post 5 tweets + 1 thread from primary: 'Week 1 building in public -- real numbers'",
                # REVENUE
                "Full Week 1 analytics: Twitter impressions per account, Gumroad views, Fiverr clicks, email open/reply rates",
                "Calculate revenue-per-hour for every channel: freelance, products, email, engagement",
                "Rank all channels by ROI: top 3 get 3x resources in Week 2",
                # AUTOMATION
                "Run system_health_monitor.py --quick: fix any degraded services",
                "Verify all scrapers ran (twitter_alpha_scraper, background_reddit_scraper, alpha_auto_processor)",
                "Review daily_digest.py output (6:45AM cron): identify 3 actions the system surfaced that were missed",
                "Check ACTIONABLE_QUEUE.md for any queued items not yet executed",
                # GOV CONTRACTS
                "Run sam_gov_monitor.py: check for newly posted IT/software contracts this week",
                "Review GOV_OPPORTUNITIES.csv: shortlist contracts with response deadlines in next 14 days"
            ],
            "revenue_target": "$0-100",
            "content": {"tweets": 5, "threads": 1, "tiktoks": 0, "youtube": 0, "newsletters": 0},
            "engagement": {"replies": 30, "dms": 5, "comments": 5, "follows": 15},
            "outreach": {"cold_emails": 0, "proposals": 0, "calls": 0},
            "automation_checks": [
                "system_health_monitor.py --quick: all services green",
                "all scrapers: twitter/reddit/alpha verified",
                "daily_digest.py: 6:45AM cron output reviewed",
                "ACTIONABLE_QUEUE.md: queued items cleared",
                "shadowban check: all accounts clean"
            ],
            "research": [
                "Week 1 channel ROI ranking: revenue-per-hour analysis",
                "GOV_OPPORTUNITIES.csv: biddable contracts shortlist",
                "daily_digest.py: missed opportunities identified"
            ]
        },
        7: {
            "theme": "CONTENT FACTORY + BOOMER PIPELINE",
            "tasks": [
                # ACCOUNTS
                "Set up YouTube channel: branding, about page, thumbnail template, channel keywords for faceless boomer content",
                "Add CashApp/Venmo/crypto wallet links to ALL account bios (P11 passive tributes)",
                # CONTENT
                "Upload first 3 faceless YouTube videos (golf tips, fishing gear reviews, health for men 55+) from ai_video_content_pipeline.py output",
                "Create 5 Facebook posts for boomer demo Groups (golf automation, health tracking, fishing tech)",
                "Write first newsletter issue in Beehiiv: automation alpha + exclusive tool recommendation",
                "Run edge_growth_engine.py --repurpose [best_thread] to atomize top content across 6 platforms",
                # ENGAGEMENT
                "Reply to 30 accounts + respond to all accumulated DMs across all accounts",
                "Post 3 tweets per secondary account (maintain warmup cadence)",
                # REVENUE
                "Optimize top 3 Gumroad listings: update titles, descriptions, pricing based on Week 1 view data",
                "Write cold email follow-up sequence: 3 emails at days 3/5/7 after initial (load into n8n w04)",
                "Apply to 3 affiliate programs: health/supplement (10-15% commission), SaaS tools ($50-500/referral), hosting ($50-200/referral)",
                # AUTOMATION
                "Verify weekly backup ran (Sunday 3AM cron), check backup integrity in ~/PRINTMAXX_BACKUPS/",
                "Verify intelligence_router.py coverage: 484 docs mapped, 98.3% target",
                "Verify security_audit.py Sunday 4:30AM cron ran: review 6-category findings",
                "Plan Week 2 escalation: 3x content volume across all accounts, launch gov contract bids"
            ],
            "revenue_target": "$0-150",
            "content": {"tweets": 9, "threads": 0, "tiktoks": 0, "youtube": 3, "newsletters": 1},
            "engagement": {"replies": 30, "dms": 10, "comments": 5, "follows": 15},
            "outreach": {"cold_emails": 0, "proposals": 0, "calls": 0},
            "automation_checks": [
                "weekly backup: Sunday 3AM cron + integrity check",
                "intelligence_router.py: 484 docs, 98.3% coverage",
                "security_audit.py: Sunday 4:30AM 6-category scan",
                "edge_growth_engine.py --repurpose: content atomization",
                "n8n w04: follow-up sequence loaded and armed"
            ],
            "research": [
                "YouTube competitor analysis: faceless boomer channels RPM/CPM",
                "boomer Facebook Groups: top 10 groups by activity for golf/fishing/health",
                "affiliate program commissions: highest-paying verticals"
            ]
        },
        # ===== WEEK 2: VOLUME + PIPELINE =====
        8: {
            "theme": "TRIPLE-ACCOUNT VOLUME",
            "tasks": [
                # ACCOUNTS
                "Primary account: post 12 tweets + 2 threads (3x Week 1 volume)",
                "Secondary accounts: post 8 tweets each (total 16 across 2 accounts)",
                "Cross-account amplification: secondary accounts quote-tweet primary threads with unique takes (stagger 2+ hours)",
                # CONTENT
                "Run content_factory.py --batch-alpha 10: generate 10 multi-platform content pieces from alpha",
                "Generate 5 TikToks via ai_video_content_pipeline.py for fitness + golf niches",
                "Post 3 TikToks + cross-post adapted versions to YouTube Shorts + Instagram Reels",
                # ENGAGEMENT
                "Reply to 75 accounts from primary + 25 from secondaries (100 total)",
                "DM 15 people: 5 Upwork job posters who haven't hired, 5 thread engagers, 5 cold prospects",
                "Post to 3 X Communities before tweeting to trigger 30-min velocity window boost",
                # REVENUE
                "Send cold email batch 3: 75 emails (175 total) via n8n w04 with A/B winning subject line",
                "Submit 15 Upwork proposals (35 total) targeting $1K-5K project budgets",
                "Follow up on all Week 1 cold emails that got opens but no replies (auto via n8n w04 sequence)",
                # AUTOMATION
                "Verify agent_swarm.py --status: 25 agents operational, check model routing (Opus/Sonnet/Haiku)",
                "Check alpha_auto_processor.py: process all PENDING_REVIEW entries in ALPHA_STAGING.csv",
                "Verify n8n w01 (GMaps lead scraper): new leads enriched and scored"
            ],
            "revenue_target": "$10-75",
            "content": {"tweets": 28, "threads": 2, "tiktoks": 3, "youtube": 0, "newsletters": 0},
            "engagement": {"replies": 100, "dms": 15, "comments": 15, "follows": 50},
            "outreach": {"cold_emails": 75, "proposals": 15, "calls": 0},
            "automation_checks": [
                "agent_swarm.py: 25 agents, Opus/Sonnet/Haiku routing",
                "alpha_auto_processor.py: all PENDING_REVIEW cleared",
                "n8n w01 GMaps: lead enrichment pipeline",
                "n8n w04 cold email: bounce rate + sequence health",
                "X Communities: velocity window engagement strategy"
            ],
            "research": [
                "Upwork trending AI categories: $1K-5K job analysis",
                "cold email A/B results: winning subject lines",
                "AGENT_ECOSYSTEM_ANALYSIS.md: tool to integrate this week"
            ]
        },
        9: {
            "theme": "VIDEO + FACELESS SCALE",
            "tasks": [
                # ACCOUNTS
                "All secondary accounts: 8 tweets + 25 replies each (pushing past warmup into growth phase)",
                # CONTENT
                "Upload YouTube faceless video #4-5 (golf tips, health for 55+) via ai_video_content_pipeline.py",
                "Record 1 YouTube tutorial video: 'How I automate a business in 48 hours with Claude' (10 min)",
                "Run auto_clip_pipeline.py --urls-file batch.txt --max-clips 15 on 3 trending AI/tech videos",
                "Post clips as TikToks + Shorts + Reels (3 clips per platform = 9 posts)",
                "Post 10 tweets + 1 thread from primary promoting YouTube content",
                # ENGAGEMENT
                "Reply to 75 accounts from primary + 25 from secondaries (100 total)",
                "DM 10 mid-tier YouTubers in AI/automation niche offering cross-promotion",
                # REVENUE
                "Submit 10 Upwork proposals on jobs matching Fiverr gig categories (45 total)",
                "Run auto_freelance_responder.py --scan-and-respond: auto-bid on hot Reddit freelance threads",
                "Respond to all Fiverr buyer requests within 1 hour, offer rush delivery premium",
                # GOV CONTRACTS
                "Run sam_gov_monitor.py --limit 50: scan for new IT/software/digital marketing contracts",
                "Draft proposal outline for top-scoring SAM.gov opportunity matching our NAICS codes",
                # AUTOMATION
                "Verify venture_autonomy.py --status: all 8 venture types active",
                "Check twitter_alpha_scraper.py: new accounts to follow/engage from 133-account scan"
            ],
            "revenue_target": "$10-100",
            "content": {"tweets": 26, "threads": 1, "tiktoks": 3, "youtube": 3, "newsletters": 0},
            "engagement": {"replies": 100, "dms": 10, "comments": 15, "follows": 45},
            "outreach": {"cold_emails": 0, "proposals": 10, "calls": 0},
            "automation_checks": [
                "venture_autonomy.py: 8 venture types active",
                "twitter_alpha_scraper.py: 133-account scan output",
                "auto_clip_pipeline.py: 15 clips generated",
                "auto_freelance_responder.py: proposals auto-generated",
                "sam_gov_monitor.py: new opportunities identified"
            ],
            "research": [
                "SAM.gov: biddable contracts matching NAICS 541511-541990",
                "YouTube SEO: faceless channel optimization for RPM",
                "OPEN_SOURCE_MONEY_TOOLS: quick-deploy revenue tools"
            ]
        },
        10: {
            "theme": "EMAIL SCALE + MULTI-PLATFORM",
            "tasks": [
                # ACCOUNTS
                "Start 2 more secondary accounts in new niches (health/supplements, personal finance) with GoLogin + SOAX",
                "Each new account: bio, profile pic, 3 seed tweets, follow 20 niche accounts",
                # CONTENT
                "Post 12 tweets + 2 threads from primary (1 case study, 1 tactical value)",
                "Post 8 tweets per secondary (24 total across 3 secondaries)",
                "Post in 5 Facebook Groups with boomer-targeted content (golf, fishing, health tracking)",
                "Create 3 LinkedIn posts repurposing best tweets with EAS B2B framing",
                "Run edge_growth_engine.py --cross-post to distribute top content across all platforms",
                # ENGAGEMENT
                "Reply to 75 from primary + 30 from secondaries (105 total)",
                "DM 15 people: 5 who engaged with content + 10 cold prospects from email list",
                # REVENUE
                "Send cold email batch 4: 100 emails (275 total) via n8n w04, split test 3 value props",
                "Follow up sequence: Day 3 on batch 2, Day 5 on batch 1 (auto via SendGrid)",
                "Write case study from any wins (reply, call booked, gig landed)",
                # AUTOMATION
                "Verify n8n workflows w01/w04/w09/w14: all executing without errors",
                "Verify daily_engagement_planner.py 7AM cron + edge_growth_engine.py status",
                "Process 100 alpha entries via alpha_auto_processor.py --process-new",
                "Check n8n w16 error alerter: any silent workflow failures?"
            ],
            "revenue_target": "$20-100",
            "content": {"tweets": 36, "threads": 2, "tiktoks": 0, "youtube": 0, "newsletters": 0},
            "engagement": {"replies": 105, "dms": 15, "comments": 20, "follows": 60},
            "outreach": {"cold_emails": 100, "proposals": 0, "calls": 0},
            "automation_checks": [
                "n8n w01/w04/w09/w14: execution health check",
                "n8n w16 error alerter: silent failure detection",
                "daily_engagement_planner.py: 7AM cron verified",
                "edge_growth_engine.py: cross-post execution",
                "alpha_auto_processor.py: 100 entries processed"
            ],
            "research": [
                "cold email split test: 3 value props compared",
                "GITHUB_AUTOMATION_TOOLS_CATALOG.md: 2 GREEN-rated tools to integrate",
                "Facebook Group engagement: boomer demo response rates"
            ]
        },
        11: {
            "theme": "EAS OFFENSIVE + MULTI-PLATFORM",
            "tasks": [
                # ACCOUNTS
                "All 4 secondary accounts: 8 tweets + 25 replies each (32 tweets, 100 replies total across secondaries)",
                "Create Pinterest boards for each niche: automation tools, boomer health, golf tech, finance tips",
                # CONTENT
                "Post 12 tweets + 1 thread from primary cross-promoting YouTube/TikTok",
                "Upload YouTube faceless videos #6-7 in boomer niches (golf tips, health supplements)",
                "Post 3 TikToks + cross-post to Shorts + Reels (adapted per platform, never identical)",
                "Pin 10 affiliate products on Pinterest with SEO-optimized descriptions",
                # ENGAGEMENT
                "Reply to 75 from primary + 30 from secondaries + 20 TikTok comments (125 total)",
                "DM 10 TikTok creators in AI/tech niche for duet/stitch opportunities",
                # REVENUE
                "Run eas_lead_pipeline.py: research 20 local businesses with outdated websites using savvy_lead_scraper",
                "Send 20 personalized EAS outreach emails to highest-scored leads (dental, legal, HVAC verticals)",
                "Submit 10 Upwork proposals (55 total), increase budget targets to $2K-10K",
                "Follow up on all Fiverr messages, offer rush delivery at premium price",
                # AUTOMATION
                "Check loop_closer.py --cycle: verify all 4 loops ran (decisions, feedback, pipeline, soul drift)",
                "Review soul_drift_report.json: rewrite prompts for any agent scoring < 7/10",
                "Check uk_contracts_finder.py: any new UK IT/automation procurement opportunities?"
            ],
            "revenue_target": "$20-150",
            "content": {"tweets": 44, "threads": 1, "tiktoks": 3, "youtube": 2, "newsletters": 0},
            "engagement": {"replies": 125, "dms": 10, "comments": 20, "follows": 50},
            "outreach": {"cold_emails": 20, "proposals": 10, "calls": 0},
            "automation_checks": [
                "loop_closer.py --cycle: 4 loops verified",
                "soul_drift_report.json: all agents > 7/10",
                "eas_lead_pipeline.py: 20 leads scored",
                "uk_contracts_finder.py: UK procurement scan",
                "Pinterest: 10 affiliate pins indexed"
            ],
            "research": [
                "BOOMER_MALE_55_70_AFFILIATE.md: refine content angles from engagement data",
                "EAS verticals: dental/legal/HVAC pain points and pricing",
                "TikTok trending sounds + formats for AI niche"
            ]
        },
        12: {
            "theme": "EAS CLOSE + GOV BID PREP",
            "tasks": [
                # ACCOUNTS
                "Audit all account health: TweepCred proxy check (engagement rate vs follower count), warmup progress",
                # CONTENT
                "Post 12 tweets + 1 thread from primary: EAS case study or automation ROI breakdown",
                "Post 8 tweets per secondary (24 total), niche-specific value content",
                "Post 3 TikToks showing real automation results (screen recordings)",
                "Create first Facebook ad creative for boomer demo ($0 spend, build assets only)",
                # ENGAGEMENT
                "Reply to 75 from primary + 30 from secondaries + 10 LinkedIn (115 total)",
                "DM 10 local business owners on Instagram/Facebook who posted about being overwhelmed",
                # REVENUE
                "Cold call 5 highest-scored EAS leads (Bland AI if available, manual if not)",
                "Send cold email batch 5: 75 emails (350 total) with best-performing subject line",
                "Send 5 custom EAS proposals: Signal Map ($1,500), Phone Pilot ($3,500), Ops Pilot ($4,500)",
                "Draft SAM.gov proposal for highest-value matching contract from GOV_OPPORTUNITIES.csv",
                # AUTOMATION
                "Run security_audit.py: review 6-category findings (secrets, injection, permissions, network, agent safety)",
                "Verify eas_lead_pipeline.py scoring accuracy: are high-scored leads converting to email replies?",
                "Check n8n w02 (Apollo lead enrichment): B2B contacts matching EAS criteria"
            ],
            "revenue_target": "$30-200",
            "content": {"tweets": 36, "threads": 1, "tiktoks": 3, "youtube": 0, "newsletters": 0},
            "engagement": {"replies": 115, "dms": 10, "comments": 10, "follows": 40},
            "outreach": {"cold_emails": 75, "proposals": 5, "calls": 5},
            "automation_checks": [
                "security_audit.py: 6-category scan clean",
                "eas_lead_pipeline.py: lead-to-reply conversion check",
                "n8n w02 Apollo: B2B contact enrichment",
                "Bland AI: call script readiness + availability",
                "Account health: TweepCred engagement ratios"
            ],
            "research": [
                "SAM.gov proposal requirements: formatting + submission process",
                "EAS MSA/SOW templates: ready for same-day contract send",
                "Bland AI call scripts: EAS discovery call framework"
            ]
        },
        13: {
            "theme": "BOOMER BLITZ + NEWSLETTER",
            "tasks": [
                # ACCOUNTS
                "Subscribe X Premium on 2 more secondary accounts that have passed warmup threshold ($6 more = $15 total)",
                # CONTENT
                "Write newsletter #1 in Beehiiv: Week 2 automation alpha + exclusive tool recommendation",
                "Post 12 tweets + 2 threads from primary (1 growth update, 1 tactical lesson)",
                "Post 8 tweets per secondary (24 total)",
                "Post in 10 Facebook Groups with boomer-targeted content: golf tech reviews, health supplements, fishing gear",
                "Upload YouTube faceless videos #8-9 in boomer niches (supplement reviews, golf gadgets)",
                "Run ai_video_content_pipeline.py --generate golf --count 5 for next batch",
                # ENGAGEMENT
                "Reply to 75 from primary + 30 from secondaries (105 total)",
                "DM 15 people: 5 newsletter subscribers, 5 thread engagers, 5 cold prospects",
                # REVENUE
                "Submit 10 Upwork proposals on fresh $2K+ jobs (65 total, track win rate)",
                "If budget available: launch $5/day Facebook ad targeting men 55-70 (golf/fishing/health interests)",
                "If no budget: organic substitute -- post in 10 more boomer Facebook Groups",
                # AUTOMATION
                "Verify all cron jobs via crontab -l: identify any silently failed jobs",
                "Check method_discovery_crawler.py 5AM cron: any new revenue methods discovered?",
                "Verify n8n w09 (content repurpose) is processing new content pieces"
            ],
            "revenue_target": "$30-200",
            "content": {"tweets": 36, "threads": 2, "tiktoks": 0, "youtube": 2, "newsletters": 1},
            "engagement": {"replies": 105, "dms": 15, "comments": 15, "follows": 45},
            "outreach": {"cold_emails": 0, "proposals": 10, "calls": 0},
            "automation_checks": [
                "crontab full audit: all 112 jobs verified",
                "method_discovery_crawler.py: 5AM cron output",
                "n8n w09 content repurpose: execution check",
                "Beehiiv: newsletter delivery rate + open rate",
                "Facebook ads: creative assets ready (or organic substitute)"
            ],
            "research": [
                "new P0 revenue methods from crawler",
                "competitor newsletters in automation niche: monetization models",
                "Facebook ad benchmarks for men 55-70 demo"
            ]
        },
        14: {
            "theme": "WEEK 2 CALIBRATION",
            "tasks": [
                # ACCOUNTS
                "Full multi-account audit: engagement rate per account, follower growth, shadowban status check",
                # CONTENT
                "Batch create for Week 3: 35 tweets + 7 threads for primary, 20 tweets per secondary",
                "Script 5 TikToks + 1 YouTube tutorial for next week",
                "Post 8 tweets + 1 thread from primary: 'Week 2 numbers (transparent growth update)'",
                # ENGAGEMENT
                "Reply to 30 accounts (reduced volume, increase quality on analytics day)",
                "Handle all open DM conversations across all accounts",
                # REVENUE
                "Full funnel analysis: emails sent vs opens vs replies vs calls vs revenue",
                "Full proposal analysis: proposals sent vs responses vs gigs won vs revenue per gig",
                "Rank every channel by revenue-per-hour: top 3 get 3x resources in Week 3",
                "Kill any channel with literally 0 signal after 14 days of effort",
                # AUTOMATION
                "Verify backup system ran (auto-backup cron), check agent resilience logs for circuit breaker triggers",
                "Review ACTIONABLE_QUEUE.md (7:30AM cron): execute any queued items",
                "Deep dive CAPITAL_GENESIS_PRIORITY_STACK.md: rewrite Week 3 priorities if stack shifted",
                # GOV CONTRACTS
                "Review all SAM.gov + UK Contracts Finder results from the week: any approaching deadline?",
                "Submit proposal if any contract deadline is within 7 days"
            ],
            "revenue_target": "$50-250",
            "content": {"tweets": 8, "threads": 1, "tiktoks": 0, "youtube": 0, "newsletters": 0},
            "engagement": {"replies": 30, "dms": 10, "comments": 5, "follows": 15},
            "outreach": {"cold_emails": 0, "proposals": 0, "calls": 0},
            "automation_checks": [
                "backup system: integrity check + agent resilience logs",
                "ACTIONABLE_QUEUE.md: 7:30AM cron output cleared",
                "circuit breaker status: no triggers in last 48h",
                "multi-account audit: per-account engagement rates",
                "GOV proposals: deadline tracking"
            ],
            "research": [
                "full funnel analysis: email/proposal/content conversion rates",
                "channel ROI ranking: revenue-per-hour per channel",
                "CAPITAL_GENESIS_PRIORITY_STACK.md: Week 3 priority adjustment"
            ]
        },
        # ===== WEEK 3: EDGE + OPTIMIZE =====
        15: {
            "theme": "KILL AND SCALE",
            "tasks": [
                # ACCOUNTS
                "KILL: any account with <0.5% engagement after 14 days (algo suppression territory, rebuild or abandon)",
                "SCALE: 3x posting volume on top 2 performing accounts",
                "Deploy strategic follow/unfollow on secondary accounts: 50 follows/day per account, unfollow after 3 days if no followback",
                # CONTENT
                "Post 15 tweets + 2 threads from primary + 10 tweets per secondary (35 total)",
                "Deploy content atomization: 1 thread becomes 12 niche-specific angles via content_factory.py (unique per account, 40% penalty for duplicate detection)",
                "Post 3 TikToks + 2 YouTube Shorts from auto_clip_pipeline.py best clips",
                # ENGAGEMENT
                "Reply to 80 from primary + 40 from secondaries (120 total, push ceiling)",
                "DM 20 people: mix of warm leads, cold prospects, collaboration pitches",
                "Quote-tweet 5 viral posts within 15 min of posting (contrarian take = reply thread visibility)",
                # REVENUE
                "Send cold email batch 6: 100 emails (450 total) using only best-performing template from A/B tests",
                "Run auto_freelance_responder.py --scan-and-respond: batch bid on all matching Reddit/Upwork jobs",
                "Launch newsletter lead magnet: tweet link from primary, pin to profile, add to all bios",
                # AUTOMATION
                "Verify edge_growth_engine.py tracking: follow/unfollow ratios within platform limits per account",
                "Check competitive_cognition_audit.py (Sunday 5AM cron): any strategic blind spots?",
                "Verify sqlite_alpha_index.py FTS5 index is current (3:30AM daily cron)"
            ],
            "revenue_target": "$50-300",
            "content": {"tweets": 35, "threads": 2, "tiktoks": 3, "youtube": 0, "newsletters": 0},
            "engagement": {"replies": 120, "dms": 20, "comments": 15, "follows": 75},
            "outreach": {"cold_emails": 100, "proposals": 5, "calls": 0},
            "automation_checks": [
                "edge_growth_engine.py: follow/unfollow per-account ratios",
                "competitive_cognition_audit.py: strategic blind spots",
                "sqlite_alpha_index.py: FTS5 index currency (3:30AM cron)",
                "content atomization: duplicate detection avoidance",
                "killed accounts/ventures: documented + resources freed"
            ],
            "research": [
                "GREY_HAT_EDGE_GROWTH_MASTER.md Section 4: Lead Gen Edge tactics",
                "killed ventures: post-mortem analysis",
                "scaled channel playbook: what doubled engagement?"
            ]
        },
        16: {
            "theme": "AFFILIATE + NEWSLETTER ENGINE",
            "tasks": [
                # ACCOUNTS
                "All secondary accounts: increase to 10 tweets + 30 replies each (scaling past warmup)",
                # CONTENT
                "Write newsletter #2: best alpha from Week 2 + exclusive content not posted publicly",
                "Write 5 affiliate review threads: boomer targeting (health supplements, golf tech, fishing gear, financial tools, insurance)",
                "Post affiliate content: 3 Facebook Groups (boomer), 2 Reddit posts, 2 Pinterest pins, 1 YouTube Short",
                "Post 12 tweets + 2 threads from primary: newsletter promotion + affiliate value thread",
                # ENGAGEMENT
                "Reply to 80 from primary + 40 from secondaries (120 total)",
                "DM 15 people who engaged with newsletter/affiliate tweets -- offer exclusive bonus",
                "Target people asking 'what tool should I use for X?' and reply with genuine comparison + affiliate link in reply thread",
                # REVENUE
                "Apply to 5 affiliate programs: health/supplement (10-15%), SaaS tools ($50-500/ref), hosting ($50-200/ref)",
                "Send cold email batch 7: 75 emails (525 total) with newsletter CTA in email signature",
                "Submit 10 Upwork proposals (75 total, track win rate this week)",
                "Add newsletter opt-in to: Gumroad checkout, YouTube desc, all bios, all landing pages",
                # AUTOMATION
                "Check daily_digest.py: surface missed opportunities from last 48 hours",
                "Verify prompt_meta_review.py (48h cycle): any lost threads or forgotten goals?",
                "Verify compliance_scanner: all affiliate content FTC compliant?"
            ],
            "revenue_target": "$50-300",
            "content": {"tweets": 32, "threads": 2, "tiktoks": 0, "youtube": 0, "newsletters": 1},
            "engagement": {"replies": 120, "dms": 15, "comments": 15, "follows": 50},
            "outreach": {"cold_emails": 75, "proposals": 10, "calls": 0},
            "automation_checks": [
                "daily_digest.py: 6:45AM cron missed-opportunity scan",
                "prompt_meta_review.py: 48h cycle lost-thread detection",
                "compliance_scanner: FTC compliance on affiliate content",
                "Beehiiv: newsletter delivery + open rate tracking",
                "affiliate link tracking: click attribution working"
            ],
            "research": [
                "highest-commission affiliate programs by vertical",
                "competitor newsletter monetization models",
                "BOOMER_MALE_55_70_AFFILIATE.md: engagement data refinement"
            ]
        },
        17: {
            "theme": "EAS CLOSE PUSH + ARBITRAGE",
            "tasks": [
                # ACCOUNTS
                "Check all account TweepCred proxies: engagement-to-follower ratios healthy across all accounts",
                # CONTENT
                "Post 12 tweets + 2 threads from primary (1 EAS value prop, 1 tactical content)",
                "Post 10 tweets per secondary (30 total across 3 secondaries)",
                "Upload YouTube video (EAS-themed: 'How I automate a business in 48 hours')",
                "Post 3 TikToks: product review format (hook: 'Stop paying for X when Y exists')",
                # ENGAGEMENT
                "Reply to 80 from primary + 40 from secondaries (120 total)",
                "DM 15 local business owners from Instagram/Facebook who posted about growth/operations",
                # REVENUE
                "Call/email top 5 warmest EAS leads: push for discovery call or proposal request",
                "Send 5 custom EAS proposals ($1,500-4,500 packages) from MONEY_METHODS/EAS/",
                "Send 25 EAS follow-up emails to all previous outreach (Day 7/14 follow-ups)",
                "Scan TikTok/Facebook ads libraries for 3 new winning products for e-commerce arbitrage",
                "Run sam_gov_monitor.py: weekly government contract scan",
                # AUTOMATION
                "Verify eas_lead_pipeline.py accuracy: high-scored leads vs actual reply conversion",
                "Check agent_swarm model routing: Opus on swarm_brain/quality_gate, Sonnet on competitor_stalker/lead_machine, Haiku on system_healer/data_janitor",
                "Verify auto_freelance_responder.py: proposals sent in last 24h, response rate"
            ],
            "revenue_target": "$75-350",
            "content": {"tweets": 42, "threads": 2, "tiktoks": 3, "youtube": 1, "newsletters": 0},
            "engagement": {"replies": 120, "dms": 15, "comments": 15, "follows": 50},
            "outreach": {"cold_emails": 25, "proposals": 5, "calls": 5},
            "automation_checks": [
                "eas_lead_pipeline.py: lead-to-conversion accuracy",
                "agent_swarm model routing: Opus/Sonnet/Haiku assignments",
                "auto_freelance_responder.py: proposal send rate",
                "sam_gov_monitor.py: weekly scan results",
                "TweepCred health: all accounts above suppression threshold"
            ],
            "research": [
                "EAS proposal refinement from objection data",
                "e-commerce arbitrage: winning product identification",
                "SAM.gov: new contracts matching capabilities"
            ]
        },
        18: {
            "theme": "CONTENT FLOOD + CROSS-AMPLIFICATION",
            "tasks": [
                # ACCOUNTS
                "Cross-account amplification day: primary posts thread, secondary accounts reply with value-add takes (unique per account)",
                "Deploy X Communities strategy: post to 3 Communities before main tweet to trigger algo velocity window",
                # CONTENT
                "Batch create 15 TikToks via ai_video_content_pipeline.py across fitness, golf, health niches",
                "Batch create 5 YouTube Shorts from auto_clip_pipeline.py best clips",
                "Batch 10 Facebook posts for boomer Groups (5 different groups, 2 posts each)",
                "Write newsletter #3 with Week 3 alpha + exclusive subscriber offer",
                "Post 12 tweets + 2 threads from primary (1 engagement-bait, 1 value)",
                "Post 10 tweets per secondary (30 total)",
                # ENGAGEMENT
                "Reply to 80 from primary + 40 from secondaries + 10 viral post replies within 30 min (130 total)",
                "DM 20 people: 10 engaged followers + 5 potential clients + 5 potential partners",
                # REVENUE
                "Post 5 Pinterest pins with affiliate-linked boomer products (golf, health, fishing)",
                "Check all e-commerce listings performance: views, clicks, conversion rate",
                # AUTOMATION
                "Verify all content posted across platforms: check Buffer/Typefully/Publer queues",
                "Run system_visualizer.py: review SYSTEM_VISUAL.html for architecture gaps",
                "Check method_discovery_crawler.py + daily_tool_scout.py: emergent tactics?"
            ],
            "revenue_target": "$100-500",
            "content": {"tweets": 42, "threads": 2, "tiktoks": 3, "youtube": 0, "newsletters": 1},
            "engagement": {"replies": 130, "dms": 20, "comments": 20, "follows": 50},
            "outreach": {"cold_emails": 0, "proposals": 0, "calls": 0},
            "automation_checks": [
                "content queue verification: Buffer/Typefully/Publer",
                "system_visualizer.py: architecture gap analysis",
                "method_discovery_crawler.py: 5AM cron emergent tactics",
                "daily_tool_scout.py: new tool discoveries",
                "X Communities: velocity window engagement tracking"
            ],
            "research": [
                "emerging content formats from discovery crawler",
                "Pinterest SEO: affiliate pin indexing speed",
                "cross-amplification metrics: engagement lift measurement"
            ]
        },
        19: {
            "theme": "EDGE GROWTH DEPLOYMENT",
            "tasks": [
                # ACCOUNTS
                "Deploy bookmark scraping: monitor bookmarks of top 10 alpha accounts for content ideas and trend signals",
                "Check shadowban status on all accounts: run detection on shadowban.eu (X), engagement drop analysis (IG/TikTok)",
                # CONTENT
                "Post 12 tweets + 1 thread from primary + 10 per secondary (32 total)",
                "Run edge_growth_engine.py --squeeze: full edge tactic audit + actionable output",
                "Run edge_growth_engine.py --viral [top_product]: generate viral hooks for best-selling product",
                # ENGAGEMENT
                "Reply to 80 from primary + 40 from secondaries (120 total)",
                "Deploy reply guy at scale: reply within 15 min to 10 big accounts in niche (author-engaged reply = +75 algo weight)",
                "DM 15 people with highest interaction scores this week",
                # REVENUE
                "Send cold email batch 8: 50 emails (500 total) -- only to highest-engagement segments",
                "Run auto_freelance_responder.py --scan-and-respond: capture any new hot jobs",
                "Review all Fiverr/Upwork active proposals: respond to inquiries within 1 hour",
                # GOV CONTRACTS
                "Run uk_contracts_finder.py --keyword 'digital' --min-value 50000: scan high-value UK contracts",
                "Review GOV_OPPORTUNITIES.csv: any deadlines in next 7 days? Draft submission.",
                # AUTOMATION
                "Verify sqlite_alpha_index.py FTS5 search: run query for 'edge growth' + 'arbitrage' + 'government contract'",
                "Measure edge tactic lift: are follow/unfollow, cross-amplification, X Communities producing measurable engagement increase?"
            ],
            "revenue_target": "$100-500",
            "content": {"tweets": 32, "threads": 1, "tiktoks": 0, "youtube": 0, "newsletters": 0},
            "engagement": {"replies": 120, "dms": 15, "comments": 15, "follows": 55},
            "outreach": {"cold_emails": 50, "proposals": 5, "calls": 0},
            "automation_checks": [
                "edge_growth_engine.py --squeeze: full tactic audit",
                "sqlite_alpha_index.py: FTS5 edge/arbitrage/gov queries",
                "edge tactic lift measurement: cross-amplification ROI",
                "shadowban detection: all accounts clean",
                "uk_contracts_finder.py: high-value UK contract scan"
            ],
            "research": [
                "GREY_HAT_EDGE_GROWTH_MASTER.md Section 9: shadowban detection protocols",
                "edge tactic effectiveness: measured lift per tactic",
                "GOV deadlines: upcoming submission requirements"
            ]
        },
        20: {
            "theme": "PRODUCT HUNT PREP + PERSONA LAUNCH",
            "tasks": [
                # ACCOUNTS
                "Launch Fanvue persona: first 5 posts from separate GoLogin profile + SOAX proxy, findom niche",
                "Fanvue cross-promotion: hint content on X secondary account with teaser + Fanvue link in bio",
                # CONTENT
                "Pick best product for Product Hunt: clear value prop, professional landing page ready",
                "Prepare PH launch assets: 5 screenshots, 60-sec demo video, tagline, description, first comment draft",
                "Post 12 tweets + 2 threads from primary (1 pre-launch hype, 1 building-in-public)",
                "Post 10 per secondary (30 total)",
                # ENGAGEMENT
                "Reply to 80 from primary + 40 from secondaries (120 total)",
                "DM 15 people who launched on PH recently: ask for tips + mutual upvote exchange",
                "Recruit 10 hunters/upvoters: DM people who upvoted similar products recently",
                # REVENUE
                "Create urgency offer: limited-time bundle combining top 3 Gumroad products at 40% discount",
                "Set up CashApp/Venmo/crypto tribute page for Fanvue persona (P02/P11)",
                "Submit 10 Upwork proposals (85 total)",
                # AUTOMATION
                "Verify product landing page: load speed, checkout flow, all links functional",
                "Run system_health_monitor.py --quick: all services green before PH launch",
                "Check loop_closer.py --cycle: are deals moving through pipeline stages?"
            ],
            "revenue_target": "$100-500",
            "content": {"tweets": 42, "threads": 2, "tiktoks": 0, "youtube": 0, "newsletters": 0},
            "engagement": {"replies": 120, "dms": 15, "comments": 15, "follows": 45},
            "outreach": {"cold_emails": 0, "proposals": 10, "calls": 0},
            "automation_checks": [
                "landing page: load speed + checkout flow test",
                "system_health_monitor.py: pre-launch all-green check",
                "loop_closer.py --cycle: pipeline advancement status",
                "Fanvue: profile live + content indexed",
                "PH launch assets: complete and staged"
            ],
            "research": [
                "Product Hunt launch playbooks: timing + first-hour strategy",
                "Fanvue competitor analysis: pricing + content frequency",
                "bundle pricing psychology: anchoring + perceived discount"
            ]
        },
        21: {
            "theme": "WEEK 3 CALIBRATION",
            "tasks": [
                # ACCOUNTS
                "Full multi-account health audit: per-account engagement rate, follower growth, TweepCred score estimate, shadowban status",
                # CONTENT
                "Post 8 tweets + 1 thread from primary: transparent Week 3 numbers update",
                "Batch create for Week 4: 35 tweets + 7 threads (primary), 25 tweets per secondary",
                "Script 5 TikToks + 1 YouTube tutorial for Week 4",
                # ENGAGEMENT
                "Reply to 30 accounts (reduced volume, increase quality on calibration day)",
                # REVENUE
                "Trajectory check: on track for $1K this month? Identify the 1 biggest bottleneck.",
                "Revenue gap analysis: shortest path from current revenue to $1K = double down there",
                "Full engagement-to-revenue conversion audit: which platform converts best?",
                "If any venture crossed $100 this week: create SOP to replicate 3x",
                "Pre-draft 100 cold emails for Week 4 with personalization tokens (load into n8n w04)",
                # AUTOMATION
                "Run full system_health_monitor.py: check all services, review logs for silent failures",
                "Verify backup system integrity + agent resilience logs for circuit breaker triggers",
                "Run competitive_cognition_audit.py: identify strategic blind spots",
                "Review CAPITAL_GENESIS_PRIORITY_STACK.md: recalibrate Week 4 priorities"
            ],
            "revenue_target": "$100-600",
            "content": {"tweets": 8, "threads": 1, "tiktoks": 0, "youtube": 0, "newsletters": 0},
            "engagement": {"replies": 30, "dms": 5, "comments": 5, "follows": 15},
            "outreach": {"cold_emails": 0, "proposals": 0, "calls": 0},
            "automation_checks": [
                "full system_health_monitor.py: all services audit",
                "backup system + agent resilience logs: circuit breaker check",
                "competitive_cognition_audit.py: strategic blind spots",
                "multi-account health: engagement/growth/shadowban per account",
                "CAPITAL_GENESIS_PRIORITY_STACK.md: priority recalibration"
            ],
            "research": [
                "trajectory analysis: $1K gap identification",
                "bottleneck identification: single biggest block",
                "SOP creation: replicate $100+ ventures 3x"
            ]
        },
        # ===== WEEK 4: COMPOUND + CLOSE =====
        22: {
            "theme": "LAUNCH DAY + REVENUE ENGINE",
            "tasks": [
                # ACCOUNTS
                "All accounts on full blast: primary 15 tweets, secondaries 10 each (45 total), all promoting PH launch",
                # CONTENT
                "Execute Product Hunt launch at 12:01 AM PT",
                "Post first PH comment with story + ask-me-anything",
                "Write 1 launch thread: 'How I built X from zero'",
                "Share PH link: Reddit (r/SaaS, r/SideProject), LinkedIn, Facebook Groups, Discord, Indie Hackers",
                "Send newsletter blast: 'We just launched on Product Hunt'",
                "Post 3 TikToks: launch day behind-the-scenes",
                # ENGAGEMENT
                "Monitor PH every 30 min: respond to EVERY comment within 15 min",
                "Reply to 50+ accounts: all-engagement mode across all platforms",
                "DM 20 people who upvoted/commented on PH thanking them",
                "Secondary accounts amplify: quote-tweet launch with unique congratulatory takes",
                # REVENUE
                "Pitch retainer to best freelance client: $500-2K/mo for ongoing automation support",
                "Set up subscription tier on Gumroad/Whop: monthly templates ($19/mo) or community ($49/mo)",
                # AUTOMATION
                "Verify PH analytics tracking: upvotes, visits, conversions counted accurately",
                "Monitor checkout under PH traffic load: no failures",
                "Check n8n w14 Stripe webhook: all sales auto-fulfilled"
            ],
            "revenue_target": "$200-1000",
            "content": {"tweets": 45, "threads": 1, "tiktoks": 3, "youtube": 0, "newsletters": 1},
            "engagement": {"replies": 50, "dms": 20, "comments": 30, "follows": 30},
            "outreach": {"cold_emails": 0, "proposals": 0, "calls": 0},
            "automation_checks": [
                "PH analytics: upvotes/visits/conversions tracking",
                "checkout: no failures under traffic load",
                "n8n w14 Stripe: auto-fulfillment working",
                "cross-account amplification: PH launch boost",
                "subscription tier: payment flow verified"
            ],
            "research": [
                "real-time PH ranking position: hourly tracking",
                "conversion rate from PH traffic: optimize if below 2%",
                "competitor PH launches today: differentiation analysis"
            ]
        },
        23: {
            "theme": "RECURRING REVENUE + EAS FINAL PUSH",
            "tasks": [
                # ACCOUNTS
                "All accounts: resume normal posting cadence after PH day (12 primary + 10 per secondary)",
                # CONTENT
                "Post 12 tweets + 2 threads from primary (1 PH results recap, 1 subscriber value thread)",
                "Post 10 per secondary (30 total)",
                "Post 3 TikToks: 'day in the life running automated business'",
                "Write newsletter #4: exclusive subscriber offer + referral incentive",
                # ENGAGEMENT
                "Reply to 80 from primary + 40 from secondaries (120 total)",
                "DM 20 people: 10 existing buyers/engagers + 10 cold prospects",
                # REVENUE
                "Push hardest EAS prospect to close: final proposal with 48-hour expiry + 10% early-bird discount",
                "Call top 3 EAS leads: voice builds trust faster than email",
                "Convert one-time Gumroad buyers to subscribers: email all buyers with subscription offer",
                "Launch Telegram VIP channel ($49-99/mo) with exclusive alpha/automation content",
                "Send cold email batch 9: 75 emails (575 total) with PH launch as social proof + testimonials",
                # AUTOMATION
                "Verify Telegram VIP payment gateway working",
                "Check daily_engagement_planner.py: warmup schedule aligned with current volume?",
                "Verify all revenue tracking: Gumroad, Fiverr, Upwork, affiliate, Stripe dashboards accurate"
            ],
            "revenue_target": "$150-700",
            "content": {"tweets": 42, "threads": 2, "tiktoks": 3, "youtube": 0, "newsletters": 1},
            "engagement": {"replies": 120, "dms": 20, "comments": 15, "follows": 50},
            "outreach": {"cold_emails": 75, "proposals": 0, "calls": 3},
            "automation_checks": [
                "Telegram VIP: payment gateway test",
                "daily_engagement_planner.py: volume/warmup alignment",
                "revenue tracking: all dashboards accurate",
                "EAS proposal: delivery pipeline ready if close",
                "Gumroad/Whop: subscription tier conversion tracking"
            ],
            "research": [
                "community monetization models: M01-M06 docs",
                "Telegram channel benchmarks: subscriber-to-revenue",
                "EAS objection handling: update playbook from calls"
            ]
        },
        24: {
            "theme": "CONVERSION OPTIMIZATION + GOV BID",
            "tasks": [
                # ACCOUNTS
                "Audit all accounts: which to keep, which to pivot, which to kill based on 3-week data",
                # CONTENT
                "Post 12 tweets + 1 thread from primary: 'X things I learned from sending 500+ cold emails'",
                "Post 10 per secondary (30 total)",
                "Upload YouTube faceless videos #10-11 in boomer niches",
                "Post 3 TikToks + 2 YouTube Shorts: top-converting format from analytics",
                # ENGAGEMENT
                "Reply to 80 from primary + 40 from secondaries (120 total)",
                "DM 10 warmest leads with personalized offer based on engagement history",
                # REVENUE
                "A/B test: Gumroad product titles/descriptions/prices for top 3 sellers",
                "Add upsells/cross-sells to all product checkout pages",
                "Optimize email sequences: rewrite any email with <20% open rate or <2% click rate",
                "Create upsell path: $15 buyer gets email for $50 product, $50 buyer gets $99 package",
                # GOV CONTRACTS
                "Submit SAM.gov proposal for best-matching contract (if deadline this week)",
                "Run uk_contracts_finder.py --keyword 'automation' --min-value 25000: new opportunities",
                "Identify UK contracts we can bid on: IT/software/digital transformation",
                # AUTOMATION
                "Run full alpha_auto_processor.py batch: clear all PENDING_REVIEW entries",
                "Verify Gumroad analytics match expected revenue, check for payment failures",
                "Check n8n w16 error alerter: any workflow failures in last 7 days?"
            ],
            "revenue_target": "$200-800",
            "content": {"tweets": 42, "threads": 1, "tiktoks": 3, "youtube": 2, "newsletters": 0},
            "engagement": {"replies": 120, "dms": 10, "comments": 10, "follows": 35},
            "outreach": {"cold_emails": 0, "proposals": 0, "calls": 0},
            "automation_checks": [
                "alpha_auto_processor.py: all PENDING_REVIEW cleared",
                "Gumroad: analytics vs expected revenue match",
                "n8n w16: error alerter -- 7-day failure review",
                "uk_contracts_finder.py: automation contract scan",
                "A/B test tracking: product title/price variations"
            ],
            "research": [
                "conversion optimization: landing page best practices",
                "pricing psychology: anchoring + payment splitting",
                "SAM.gov proposal submission: requirements checklist"
            ]
        },
        25: {
            "theme": "SCALE WINNERS + AUTOMATE REPEATS",
            "tasks": [
                # ACCOUNTS
                "Top-performing accounts: increase posting 2x, add X Premium if not already subscribed",
                "Low-performing accounts: reduce to maintenance mode (3 tweets + 10 replies daily)",
                # CONTENT
                "Post 15 tweets + 2 threads from primary (revenue milestone + tactical value)",
                "Post 10 per secondary (30 total)",
                "Post 3 TikToks showing real automation workflows in action",
                "Run content_factory.py --batch-alpha 15: large batch for end-of-month content buffer",
                # ENGAGEMENT
                "Reply to 80 from primary + 40 from secondaries (120 total)",
                "DM 15 people: potential next-month collaboration partners",
                # REVENUE
                "Send cold email batch 10: 100 emails (675 total) -- only to hottest segments",
                "Follow up on ALL open proposals: Upwork, EAS, freelance -- create urgency with expiry dates",
                "Automate any task done manually 3+ times this month: script + cron",
                "Deploy any backlogged automation from ACTIONABLE_QUEUE.md",
                # AUTOMATION
                "Set up new cron jobs for recurring workflows discovered this month",
                "Create automated revenue reporting: daily Telegram summary via n8n w17",
                "Update PRINTMAXX_SYSTEM_MAP.md with all changes from this month",
                "Clean up dead ventures: archive docs, remove orphan cron jobs"
            ],
            "revenue_target": "$200-800",
            "content": {"tweets": 45, "threads": 2, "tiktoks": 3, "youtube": 0, "newsletters": 0},
            "engagement": {"replies": 120, "dms": 15, "comments": 10, "follows": 40},
            "outreach": {"cold_emails": 100, "proposals": 5, "calls": 0},
            "automation_checks": [
                "new cron jobs deployed for recurring workflows",
                "ACTIONABLE_QUEUE.md: all backlog cleared",
                "PRINTMAXX_SYSTEM_MAP.md: updated with month changes",
                "dead ventures: archived + orphan crons removed",
                "automated revenue reporting: n8n w17 configured"
            ],
            "research": [
                "NOVEL_DISCOVERIES.md: patterns worth extracting to sovrun",
                "automation candidates: manual tasks done 3+ times",
                "next-month pipeline warmup: pre-draft content + emails"
            ]
        },
        26: {
            "theme": "PARTNERSHIP + COMMUNITY",
            "tasks": [
                # ACCOUNTS
                "Evaluate: which secondary accounts are worth $3/mo X Premium upgrade based on engagement data?",
                # CONTENT
                "Post 12 tweets + 1 thread from primary: Month retrospective with real numbers",
                "Post 10 per secondary (30 total)",
                "Upload YouTube video: month retrospective or best tutorial content",
                "Post 3 TikToks: authentic behind-the-scenes, no polish",
                "Write newsletter #5: month in review + what is coming next month",
                # ENGAGEMENT
                "Reply to 75 from primary + 30 from secondaries (105 total)",
                "DM 10 top engagers: convert to community members / paid subscribers",
                # REVENUE
                "Send cold email batch 11: 50 emails (725 total) with best social proof from the month",
                "Push any open EAS deals to close: follow up with case study + limited-time pricing",
                "Review e-commerce listing performance: kill underperformers, double down on winners",
                # GOV CONTRACTS
                "Final SAM.gov + UK Contracts Finder weekly scan before month end",
                "If any contract won: begin delivery planning immediately",
                # AUTOMATION
                "Run capital_genesis_ranker.py --rank --report: generate fresh next-month priority stack",
                "Verify all 33 agents operational: agent_swarm (25) + venture_autonomy (8)",
                "Check intelligence_router.py --stats: doc coverage and alpha entry count"
            ],
            "revenue_target": "$200-800",
            "content": {"tweets": 42, "threads": 1, "tiktoks": 3, "youtube": 1, "newsletters": 1},
            "engagement": {"replies": 105, "dms": 10, "comments": 10, "follows": 35},
            "outreach": {"cold_emails": 50, "proposals": 0, "calls": 3},
            "automation_checks": [
                "capital_genesis_ranker.py: fresh priority stack generated",
                "all 33 agents: swarm (25) + ventures (8) operational",
                "intelligence_router.py --stats: coverage + alpha count",
                "SAM.gov + UK Contracts Finder: final monthly scan",
                "e-commerce listings: performance review complete"
            ],
            "research": [
                "next-month priority stack: adjusted from actual data",
                "partnership opportunities: collab partners identified",
                "community conversion: free follower to paid member pipeline"
            ]
        },
        27: {
            "theme": "NEXT MONTH WAR PLAN",
            "tasks": [
                # ACCOUNTS
                "Full account stack review: total accounts, total X Premium spend, engagement per account, ROI per account",
                "Plan account stack for next month: which to add, which to sunset, which niches to expand",
                # CONTENT
                "Post 8 tweets + 1 thread from primary: 'Month in review, honest numbers'",
                "Post 5 per secondary (15 total)",
                # ENGAGEMENT
                "Reply to 30 accounts + handle all open DM conversations",
                # REVENUE
                "Full month review: actual revenue vs conservative/medium/aggressive scenarios from KPI_DASHBOARD.md",
                "Per-channel breakdown: revenue, time invested, ROI per hour, growth trajectory",
                "Identify top 3 ventures for next month: allocate 80% of effort to these three",
                "Kill list: finalize ventures to cut next month (<$50 revenue after full month)",
                "Scale list: ventures getting 3x resources next month (>$200 revenue or >5% engagement)",
                "Set next-month daily KPI targets based on actual conversion rates",
                # AUTOMATION
                "Verify all automated systems stable for overnight/weekend operation",
                "Review all agent outputs: any consistently underperforming agents need prompt rewrites?",
                "Document procedural memory: what worked, what didn't, what to never repeat"
            ],
            "revenue_target": "$200-800",
            "content": {"tweets": 23, "threads": 1, "tiktoks": 0, "youtube": 0, "newsletters": 0},
            "engagement": {"replies": 30, "dms": 5, "comments": 5, "follows": 15},
            "outreach": {"cold_emails": 0, "proposals": 0, "calls": 0},
            "automation_checks": [
                "all systems stability: overnight/weekend readiness",
                "agent performance audit: underperforming agents identified",
                "procedural memory: lessons captured + stored",
                "account stack ROI: per-account revenue analysis",
                "next-month KPI targets: set from actual conversion data"
            ],
            "research": [
                "month retrospective: actual vs projected revenue",
                "next-month venture prioritization: top 3 + kill list",
                "conversion rate baselines: email/proposal/content per channel"
            ]
        },
        28: {
            "theme": "MONTH CLOSE + SYSTEM AUDIT",
            "tasks": [
                # ACCOUNTS
                "Update all bios/profiles with new credentials or milestones from the month",
                # CONTENT
                "Post 10 tweets + 1 thread from primary: 'Month complete, real numbers, no cap'",
                "Post 5 per secondary (15 total)",
                "Post LinkedIn retrospective for EAS credibility building",
                # ENGAGEMENT
                "Reply to 60 accounts across all platforms",
                # REVENUE
                "Final revenue count: total earnings across ALL channels (freelance, products, content, EAS, persona, affiliate, gov contracts)",
                "Revenue leaderboard: rank every venture by actual revenue generated",
                "Engagement leaderboard: followers gained per account, engagement rate, growth trajectory",
                "Outreach leaderboard: emails sent, reply rate, close rate, revenue per email",
                # AUTOMATION
                "Full system health audit: all 112 cron jobs, all 33 agents, all scrapers, all pipelines",
                "Run capital_genesis_ranker.py --rank --report: fresh next-month priority stack",
                "Verify all GoLogin profiles + SOAX proxies still functional and undetected",
                "Set 3 stretch goals for next month that would change the trajectory if achieved",
                # GOV CONTRACTS
                "Review all GOV_OPPORTUNITIES.csv outcomes: bids submitted, responses received, contracts won",
                "Update gov contract pipeline tracker with next month's target contracts"
            ],
            "revenue_target": "$250-1000",
            "content": {"tweets": 25, "threads": 1, "tiktoks": 0, "youtube": 0, "newsletters": 0},
            "engagement": {"replies": 60, "dms": 10, "comments": 10, "follows": 30},
            "outreach": {"cold_emails": 0, "proposals": 0, "calls": 0},
            "automation_checks": [
                "full system audit: 112 crons + 33 agents + all scrapers",
                "capital_genesis_ranker.py: next-month stack generated",
                "GoLogin + SOAX: all profiles functional + undetected",
                "GOV pipeline: bids/responses/wins tracked",
                "stretch goals: 3 trajectory-changing targets set"
            ],
            "research": [
                "month data analysis: what compounded, what didn't",
                "next-month priority stack: data-driven venture ranking",
                "stretch goal feasibility: resource requirements mapped"
            ]
        },
        29: {
            "theme": "PIPELINE PRELOAD",
            "tasks": [
                # ACCOUNTS
                "Pre-create any new accounts needed for next month expansions (new GoLogin profiles + SOAX assignments)",
                # CONTENT
                "Batch create next month Week 1 content: 35 tweets + 7 threads (primary), 25 per secondary",
                "Pre-generate 10 faceless YouTube videos via ai_video_content_pipeline.py for next month",
                "Post 10 tweets + 1 thread from primary: 'How I automated X so I never have to do it again'",
                # ENGAGEMENT
                "Reply to 60 accounts + engage with anyone discussing automation/efficiency",
                "DM 10 potential next-month collaboration partners",
                # REVENUE
                "Send cold email batch 12: 50 emails (775 total) -- warm up next month pipeline early",
                "Pre-draft 100 cold emails for next month Week 1 with personalization tokens",
                "Run auto_freelance_responder.py --scan-and-respond: capture any end-of-month hot jobs",
                # AUTOMATION
                "Set up any new cron jobs identified during the month",
                "Deploy any remaining items from ACTIONABLE_QUEUE.md",
                "Update OPS/PRINTMAXX_SYSTEM_MAP.md with all month's changes",
                "Clean up dead ventures: archive docs, remove orphan cron jobs, update intelligence catalog"
            ],
            "revenue_target": "$200-800",
            "content": {"tweets": 10, "threads": 1, "tiktoks": 0, "youtube": 0, "newsletters": 0},
            "engagement": {"replies": 60, "dms": 10, "comments": 10, "follows": 40},
            "outreach": {"cold_emails": 50, "proposals": 0, "calls": 0},
            "automation_checks": [
                "new cron jobs: all month's discoveries deployed",
                "ACTIONABLE_QUEUE.md: fully cleared",
                "PRINTMAXX_SYSTEM_MAP.md: end-of-month update",
                "dead ventures: cleaned + archived",
                "next-month content buffer: pre-loaded"
            ],
            "research": [
                "next-month pipeline warmup: pre-drafted emails/content",
                "automation candidates: month's manual tasks scripted",
                "NOVEL_DISCOVERIES.md: sovrun extraction candidates"
            ]
        },
        30: {
            "theme": "MONTH CLOSE FINAL",
            "tasks": [
                # ACCOUNTS
                "Final account health check: all accounts clean, all proxies working, all profiles updated",
                # CONTENT
                "Post 10 tweets + 1 thread from primary: end-of-month wrap-up",
                "Send newsletter: month recap + next month preview (build anticipation)",
                # ENGAGEMENT
                "Reply to 60 accounts + final DM batch to close open conversations",
                # REVENUE
                "Final revenue reconciliation: all channels, all platforms, all payment processors",
                "Update KPI_DASHBOARD.md with actual month numbers vs projections",
                "Close any remaining open proposals with urgency",
                # AUTOMATION
                "Verify all systems stable for overnight transition to next month",
                "Run capital_genesis_ranker.py --rank --export csv: export month-end state",
                "Verify all 33 agents operational for next month's Day 1",
                "Final backup: python3 AUTOMATIONS/backup_system.py --full"
            ],
            "revenue_target": "$250-1000",
            "content": {"tweets": 10, "threads": 1, "tiktoks": 0, "youtube": 0, "newsletters": 1},
            "engagement": {"replies": 60, "dms": 10, "comments": 10, "follows": 30},
            "outreach": {"cold_emails": 0, "proposals": 0, "calls": 0},
            "automation_checks": [
                "all 33 agents: operational for next month",
                "capital_genesis_ranker.py: month-end state exported",
                "backup_system.py --full: complete backup verified",
                "all accounts: clean health + working proxies",
                "next month Day 1: all systems ready"
            ],
            "research": [
                "month-end revenue reconciliation: actual vs target",
                "KPI_DASHBOARD.md: updated with real numbers",
                "next month Day 1 priorities: top 3 actions identified"
            ]
        },
    }

    default_plan = {
        "theme": "FLEX OPS",
        "tasks": [
            "Continue top 3 priority ventures from CAPITAL_GENESIS_PRIORITY_STACK.md",
            "Post 12 tweets from primary + 8 per secondary account (28 total)",
            "Reply to 60 accounts from primary + 20 from secondaries (80 total)",
            "Follow up on all open proposals (Upwork, EAS, freelance) and DM conversations",
            "Run auto_freelance_responder.py --scan-and-respond: capture hot jobs",
            "Send 25 cold emails from pipeline (continue n8n w04 sequence)",
            "Run sam_gov_monitor.py: check for new matching contracts",
            "Verify system_health_monitor.py --quick: all 112 cron jobs + 33 agents",
            "Check twitter_alpha_scraper.py + background_reddit_scraper.py outputs",
            "Check soul_drift_report.json: all agents > 6/10",
            "Process 50 alpha entries via alpha_auto_processor.py --process-new",
            "Review daily_digest.py output (6:45AM): surface missed opportunities",
            "Post 3 TikToks from ai_video_content_pipeline.py batch",
            "Check GoLogin profiles + SOAX proxies: all accounts clean and functional",
        ],
        "revenue_target": "TBD",
        "content": {"tweets": 28, "threads": 0, "tiktoks": 3, "youtube": 0, "newsletters": 0},
        "engagement": {"replies": 80, "dms": 10, "comments": 10, "follows": 25},
        "outreach": {"cold_emails": 25, "proposals": 5, "calls": 0},
        "automation_checks": [
            "system_health_monitor.py: 112 crons + 33 agents",
            "twitter_alpha_scraper.py + reddit scraper: output verified",
            "soul_drift_report.json: all agents > 6/10",
            "GoLogin + SOAX: all profiles functional",
            "daily_digest.py: 6:45AM cron reviewed"
        ],
        "research": [
            "CAPITAL_GENESIS_PRIORITY_STACK.md: daily priorities",
            "alpha_staging: 50 PENDING_REVIEW entries processed",
            "sam_gov_monitor.py: new contract opportunities"
        ]
    }

    # Weekly phase labels
    week_phases = {1: "INFRA + ACCOUNTS", 2: "VOLUME + PIPELINE", 3: "EDGE + OPTIMIZE", 4: "COMPOUND + CLOSE"}

    calendar_data = []
    for day in range(1, min(days_in_month + 1, 31)):
        plan = daily_plans.get(day, default_plan)
        is_today = (now.month == month and now.day == day) or (now.month == month - 1 and day == 1)
        week_num = (day - 1) // 7 + 1
        content = plan.get("content", {"tweets": 5, "threads": 0, "tiktoks": 0, "youtube": 0, "newsletters": 0})
        engagement = plan.get("engagement", {"replies": 0, "dms": 0, "comments": 0, "follows": 0})
        outreach = plan.get("outreach", {"cold_emails": 0, "proposals": 0, "calls": 0})
        # Compute daily scores
        engagement_score = engagement.get("replies", 0) + engagement.get("dms", 0) + engagement.get("comments", 0) + engagement.get("follows", 0)
        content_score = content.get("tweets", 0) + content.get("threads", 0) * 3 + content.get("tiktoks", 0) * 2 + content.get("youtube", 0) * 5 + content.get("newsletters", 0) * 4
        outreach_score = outreach.get("cold_emails", 0) + outreach.get("proposals", 0) * 5 + outreach.get("calls", 0) * 10
        calendar_data.append({
            "day": day,
            "weekday": calendar.day_abbr[calendar.weekday(year, month, day)],
            "theme": plan["theme"],
            "tasks": plan["tasks"],
            "revenue_target": plan["revenue_target"],
            "content": content,
            "engagement": engagement,
            "outreach": outreach,
            "automation_checks": plan.get("automation_checks", []),
            "research": plan.get("research", []),
            "is_today": is_today,
            "is_past": False,
            "week": week_num,
            "week_phase": week_phases.get(week_num, "SCALE"),
            "scores": {
                "engagement": engagement_score,
                "content": content_score,
                "outreach": outreach_score,
            },
        })

    return jsonify({"month": f"{calendar.month_name[month]} {year}", "days": calendar_data, "goal": "$1,000"})


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
