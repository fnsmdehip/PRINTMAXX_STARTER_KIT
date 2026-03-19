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

    # Detailed daily plans — aggressive ops calendar
    # Week 1: FOUNDATION (accounts, first products, first content)
    # Week 2: VOLUME (3x content, 3x outreach, first paid experiments)
    # Week 3: OPTIMIZATION (kill losers, scale winners, add edge tactics)
    # Week 4: COMPOUND (recurring revenue, partnerships, scale what works)
    daily_plans = {
        # ===== WEEK 1: FOUNDATION =====
        1: {
            "theme": "DAY ZERO",
            "tasks": [
                "Create Gumroad account + list first 5 products (prompt packs, automation templates, notion kits)",
                "Authenticate Stripe MCP for payment processing",
                "Upload Twitter banner/pfp/bio (all assets ready in MEDIA/)",
                "Post 5 tweets from posting queue + 1 thread on what you're building",
                "Reply to 30 accounts in automation/AI niche (reply guy warmup)",
                "DM 5 high-follower accounts with genuine value (no pitch yet)",
                "Set up GoLogin profiles for secondary accounts",
                "Verify all 112 cron jobs ran overnight: check system_health_monitor output",
                "Review ALPHA_STAGING.csv for new opportunities (target: 50 entries)",
                "Read daily_tool_scout output + CAPITAL_GENESIS_PRIORITY_STACK.md"
            ],
            "revenue_target": "$0",
            "content": {"tweets": 5, "threads": 1, "tiktoks": 0, "youtube": 0, "newsletters": 0},
            "engagement": {"replies": 30, "dms": 5, "comments": 10, "follows": 25},
            "outreach": {"cold_emails": 0, "proposals": 0, "calls": 0},
            "automation_checks": ["cron health 112 jobs", "scraper outputs (twitter/reddit/alpha)", "soul drift score > 6"],
            "research": ["alpha_staging 50 entries", "daily_tool_scout output", "capital_genesis_priority_stack"]
        },
        2: {
            "theme": "PRODUCT BLITZ",
            "tasks": [
                "List remaining 8 products on Gumroad (total 13: prompt packs, templates, guides, code snippets, SOP bundles)",
                "Create Whop storefront + list top 8 products there too (5.7% fee vs Gumroad 10%)",
                "Generate product thumbnails using Playwright screenshot factory (batch all 13)",
                "Write 5 tweets showcasing products with hooks, not just 'check this out'",
                "Write 1 thread: 'I automated X and here is the exact prompt I used' (lead magnet for email)",
                "Reply to 40 accounts in AI/automation/freelance niches",
                "Comment on 5 viral tweets within 30 min of posting (set up alerts)",
                "DM 5 mid-tier accounts (2K-20K followers) offering free template in exchange for feedback",
                "Cross-post product links to LinkedIn with value-first framing",
                "Verify reddit scraper + twitter scraper ran, check agent_swarm health",
                "Review soul_drift_report.json — any agent below 6/10 gets prompt rewrite",
                "Read GREY_HAT_EDGE_GROWTH_MASTER.md warmup protocols section"
            ],
            "revenue_target": "$0-20",
            "content": {"tweets": 5, "threads": 1, "tiktoks": 0, "youtube": 0, "newsletters": 0},
            "engagement": {"replies": 40, "dms": 5, "comments": 15, "follows": 30},
            "outreach": {"cold_emails": 0, "proposals": 0, "calls": 0},
            "automation_checks": ["scraper outputs verified", "agent_swarm health", "soul drift scores"],
            "research": ["warmup protocols", "competitor product pricing on Gumroad", "top-selling automation templates"]
        },
        3: {
            "theme": "FREELANCE LAUNCH",
            "tasks": [
                "Create Fiverr account + post 5 gigs (AI automation, Claude Code dev, chatbot build, data pipeline, web scraping)",
                "Create Upwork profile + submit 10 proposals on AI/automation jobs posted today",
                "Draft 3 cold email templates (EAS intro, freelance pitch, local biz website redesign)",
                "Build email scraper target list: 100 local businesses with outdated websites",
                "Write 5 tweets + 1 thread: 'How I build apps in 2 hours that agencies quote $10K for'",
                "Reply to 40 accounts, prioritize anyone talking about needing automation",
                "DM 10 people who tweeted about manual processes or hiring developers",
                "Comment on 3 LinkedIn posts about business automation (non-spammy, value-add)",
                "Set up Fiverr gig SEO: research top keywords, competitor pricing, optimize descriptions",
                "Check n8n workflows status, verify daily_engagement_planner ran at 7 AM",
                "Process 75 alpha entries from ALPHA_STAGING.csv",
                "Read competitor Fiverr gigs in AI category — note pricing, delivery times, reviews"
            ],
            "revenue_target": "$0-30",
            "content": {"tweets": 5, "threads": 1, "tiktoks": 0, "youtube": 0, "newsletters": 0},
            "engagement": {"replies": 40, "dms": 10, "comments": 13, "follows": 35},
            "outreach": {"cold_emails": 0, "proposals": 10, "calls": 0},
            "automation_checks": ["n8n workflows", "engagement_planner", "fiverr gig indexing"],
            "research": ["competitor fiverr pricing", "alpha_staging 75 entries", "upwork trending skills"]
        },
        4: {
            "theme": "FIRST BLOOD",
            "tasks": [
                "Send first cold email batch: 50 emails to local biz with outdated websites",
                "Submit 10 more Upwork proposals (20 total active)",
                "Lower first Fiverr gig price to $25 to get first review fast",
                "Post 5 tweets + 1 thread: breakdown of a real automation you built",
                "Reply to 50 accounts (increase from 40 — push the warmup)",
                "DM 10 Fiverr buyers who posted AI jobs in last 24h with proactive pitch",
                "Set up engagement pod: find 5-10 accounts willing to mutually engage",
                "Comment on 10 Reddit posts in r/freelance, r/automation, r/smallbusiness (genuine help, link in profile)",
                "Create TikTok account + film first 3 videos (screen recordings of building with AI)",
                "Verify eas_lead_pipeline.py ran at 8 AM, review scored leads",
                "Review method_discovery_crawler output — any new P0 methods?",
                "Read DEFINITIVE_GROWTH_STACK.md engagement section for next escalation"
            ],
            "revenue_target": "$0-50",
            "content": {"tweets": 5, "threads": 1, "tiktoks": 3, "youtube": 0, "newsletters": 0},
            "engagement": {"replies": 50, "dms": 10, "comments": 20, "follows": 40},
            "outreach": {"cold_emails": 50, "proposals": 10, "calls": 0},
            "automation_checks": ["eas_lead_pipeline", "cold email delivery/bounce rates", "method_discovery_crawler"],
            "research": ["new P0 methods", "reddit niche conversations", "growth stack engagement tactics"]
        },
        5: {
            "theme": "OUTREACH MACHINE",
            "tasks": [
                "Send cold email batch 2: 50 more emails (100 total), A/B test subject lines",
                "Follow up on batch 1 non-openers with different subject line",
                "Submit 5 more Upwork proposals on high-budget jobs ($2K+)",
                "Post 5 tweets + 1 thread: 'I sent 100 cold emails, here is what happened' (real-time case study)",
                "Reply to 50 accounts + engage with any replies to your threads",
                "DM 15 people: 10 potential clients + 5 potential collaborators",
                "Post first 3 TikToks (cross-post to YouTube Shorts + Instagram Reels)",
                "Create Fanvue account for persona venture (P02)",
                "Write 2 Reddit posts with genuine value (r/Entrepreneur, r/SaaS)",
                "Check cold email analytics: open rates, reply rates, bounce rates",
                "Verify twitter_warmup_poster advanced correctly, check warmup day status",
                "Review capital_genesis_ranker output — reprioritize based on Day 1-4 data"
            ],
            "revenue_target": "$0-75",
            "content": {"tweets": 5, "threads": 1, "tiktoks": 3, "youtube": 0, "newsletters": 0},
            "engagement": {"replies": 50, "dms": 15, "comments": 12, "follows": 40},
            "outreach": {"cold_emails": 50, "proposals": 5, "calls": 0},
            "automation_checks": ["twitter_warmup_poster", "cold email analytics", "tiktok upload verification"],
            "research": ["cold email A/B results", "capital_genesis rerank", "fanvue competitor analysis"]
        },
        6: {
            "theme": "DATA WAR ROOM",
            "tasks": [
                "Full Week 1 analytics review: Twitter impressions, Gumroad views, Fiverr clicks, email open/reply rates",
                "Calculate revenue-per-hour for every channel touched this week",
                "Rank channels: which got most traction with least effort? 3x that one.",
                "Kill anything with literally 0 signal after 5 days of effort",
                "Post 5 tweets + 1 thread: 'Week 1 building in public — real numbers'",
                "Reply to 30 accounts (reduce volume, increase quality on Sat)",
                "DM 5 highest-engagement accounts from this week to build relationships",
                "Review all Fiverr/Upwork messages and respond within 1 hour",
                "Batch create 20 tweets + 5 threads for next week",
                "Verify all scrapers ran (twitter, reddit, alpha), fix any failures",
                "Run system_health_monitor --quick and fix any degraded services",
                "Read daily_digest output — identify 3 actions the system surfaced that you missed"
            ],
            "revenue_target": "$0-100",
            "content": {"tweets": 5, "threads": 1, "tiktoks": 0, "youtube": 0, "newsletters": 0},
            "engagement": {"replies": 30, "dms": 5, "comments": 5, "follows": 15},
            "outreach": {"cold_emails": 0, "proposals": 0, "calls": 0},
            "automation_checks": ["all scrapers", "system_health_monitor", "daily_digest"],
            "research": ["week 1 analytics deep dive", "channel ROI ranking", "daily_digest action items"]
        },
        7: {
            "theme": "CONTENT FACTORY",
            "tasks": [
                "Batch create 25 tweets + 7 threads for Week 2 (load Buffer/Typefully queue)",
                "Script 5 TikToks (screen recordings showing AI builds in real-time)",
                "Write first YouTube script: '10-minute tutorial on automating X with Claude'",
                "Create 5 Facebook posts targeting boomer demo (golf/fishing/health automation angles)",
                "Write first cold email follow-up sequence (3 emails, days 3/5/7 after initial)",
                "Optimize top 3 Gumroad listings: update titles, descriptions, pricing based on view data",
                "Reply to 30 accounts + respond to all accumulated DMs",
                "Set up YouTube channel: branding, about page, first thumbnail template",
                "Create CashApp/Venmo/crypto links on all bios (P11 passive income)",
                "Verify weekly backup ran (Sunday 3 AM), check backup integrity",
                "Review intelligence_router coverage — any gaps in venture mapping?",
                "Plan Week 2 escalation: 3x content volume, 3x outreach, first paid experiment"
            ],
            "revenue_target": "$0-150",
            "content": {"tweets": 5, "threads": 1, "tiktoks": 0, "youtube": 0, "newsletters": 0},
            "engagement": {"replies": 30, "dms": 5, "comments": 5, "follows": 15},
            "outreach": {"cold_emails": 0, "proposals": 0, "calls": 0},
            "automation_checks": ["weekly backup", "intelligence_router coverage", "buffer/typefully queues loaded"],
            "research": ["youtube competitor analysis", "boomer demo content angles", "week 2 escalation plan"]
        },
        # ===== WEEK 2: VOLUME (3x everything) =====
        8: {
            "theme": "TRIPLE DOWN",
            "tasks": [
                "Send cold email batch 3: 75 emails (175 total) with optimized subject lines from Week 1 A/B test",
                "Submit 15 Upwork proposals (35 total) — focus on $1K-5K project budgets",
                "Post 8 tweets + 2 threads (3x from Week 1 daily rate)",
                "Reply to 60 accounts — target people complaining about manual processes",
                "DM 15 people: 10 cold prospects from Twitter + 5 Upwork job posters who haven't hired yet",
                "Post 3 TikToks (batch from Sunday) + cross-post to Shorts and Reels",
                "Comment on 5 viral posts in your niche within 30 min of going viral (set alerts)",
                "Apply to 3 affiliate programs: ClickBank, ShareASale, and best vertical match",
                "Follow up on all Week 1 cold emails that got opens but no replies",
                "Check agent_swarm --status, verify 25 agents operational",
                "Review alpha_auto_processor output — process any PENDING_REVIEW entries",
                "Read AGENT_ECOSYSTEM_ANALYSIS.md — find tool to add to stack this week"
            ],
            "revenue_target": "$10-75",
            "content": {"tweets": 8, "threads": 2, "tiktoks": 3, "youtube": 0, "newsletters": 0},
            "engagement": {"replies": 60, "dms": 15, "comments": 20, "follows": 50},
            "outreach": {"cold_emails": 75, "proposals": 15, "calls": 0},
            "automation_checks": ["agent_swarm 25 agents", "alpha_auto_processor", "cold email bounce rates"],
            "research": ["agent_ecosystem_analysis", "affiliate program verticals", "upwork trending categories"]
        },
        9: {
            "theme": "VIDEO BLITZ",
            "tasks": [
                "Record + edit first YouTube video (10 min: 'I built X with AI in Y minutes')",
                "Generate voiceover with Edge TTS, source footage with AI video tools",
                "Create click-worthy thumbnail with Playwright screenshot factory",
                "Post 8 tweets + 1 thread promoting the video before upload",
                "Upload video + optimize: title/desc/tags for SEO, end screen, cards, pinned comment with CTA",
                "Reply to 60 accounts — prioritize anyone discussing topics from your video",
                "DM 10 mid-tier YouTubers in adjacent niches offering collab/cross-promotion",
                "Post 3 TikToks: 60-sec cuts from the YouTube video + trending hooks",
                "Submit 10 Upwork proposals on jobs matching your Fiverr gig categories",
                "Verify venture_autonomy --status shows all 8 venture types active",
                "Check twitter_alpha_scraper output — new accounts to follow/engage?",
                "Review OPEN_SOURCE_MONEY_TOOLS for any quick-deploy revenue tools"
            ],
            "revenue_target": "$10-100",
            "content": {"tweets": 8, "threads": 1, "tiktoks": 3, "youtube": 1, "newsletters": 0},
            "engagement": {"replies": 60, "dms": 10, "comments": 15, "follows": 45},
            "outreach": {"cold_emails": 0, "proposals": 10, "calls": 0},
            "automation_checks": ["venture_autonomy 8 types", "twitter_alpha_scraper", "youtube upload verification"],
            "research": ["open_source_money_tools", "youtube SEO best practices", "competitor video formats"]
        },
        10: {
            "theme": "EMAIL SCALE",
            "tasks": [
                "Send cold email batch 4: 100 emails (275 total) — split test 3 different value props",
                "Follow up sequence: Day 3 follow-ups on batch 2, Day 5 on batch 1",
                "Write case study from any wins (even small: 'got a reply', 'booked a call')",
                "Post 8 tweets + 2 threads (one case study thread, one tactical thread)",
                "Reply to 60 accounts + engage with every reply to your threads within 1 hour",
                "DM 15 people: 5 who engaged with your content + 10 cold prospects from email list",
                "Post in 5 Facebook Groups (boomer-targeted: golf automation, health tracking, fishing tech)",
                "Create 3 LinkedIn posts (repurpose best tweets with professional framing)",
                "Start secondary Twitter account for niche content (separate GoLogin profile)",
                "Verify n8n workflows, check daily_engagement_planner ran, verify edge_growth_engine status",
                "Process 100 alpha entries from ALPHA_STAGING.csv",
                "Read GITHUB_AUTOMATION_TOOLS_CATALOG.md — identify 2 tools rated GREEN to integrate"
            ],
            "revenue_target": "$20-100",
            "content": {"tweets": 8, "threads": 2, "tiktoks": 0, "youtube": 0, "newsletters": 0},
            "engagement": {"replies": 60, "dms": 15, "comments": 20, "follows": 50},
            "outreach": {"cold_emails": 100, "proposals": 0, "calls": 0},
            "automation_checks": ["n8n workflows", "engagement_planner", "edge_growth_engine"],
            "research": ["github_automation_tools_catalog", "cold email split test results", "alpha_staging 100 entries"]
        },
        11: {
            "theme": "MULTI-PLATFORM",
            "tasks": [
                "Post 3 TikToks + 3 YouTube Shorts + 3 Instagram Reels (repurpose same content across all 3)",
                "Upload YouTube video #2 (tutorial or reaction to trending AI topic)",
                "Post 8 tweets + 1 thread cross-promoting YouTube/TikTok content",
                "Reply to 60 accounts on Twitter + 20 comments on TikToks in your niche",
                "DM 10 TikTok creators in AI/tech niche for duet/stitch opportunities",
                "Submit 10 Upwork proposals (45 total) — increase budget targets to $2K-10K",
                "EAS: Research 15 local businesses with outdated websites using savvy_lead_scraper",
                "Create Pinterest account + pin 10 products/templates (SEO-optimized descriptions)",
                "Follow up on all Fiverr messages — offer rush delivery for premium price",
                "Check loop_closer --cycle output, verify all 4 loops ran",
                "Review soul_drift_report.json — rewrite prompts for any agent scoring < 7",
                "Read boomer affiliate alpha: BOOMER_MALE_55_70_AFFILIATE.md for content angles"
            ],
            "revenue_target": "$20-150",
            "content": {"tweets": 8, "threads": 1, "tiktoks": 3, "youtube": 1, "newsletters": 0},
            "engagement": {"replies": 80, "dms": 10, "comments": 20, "follows": 50},
            "outreach": {"cold_emails": 0, "proposals": 10, "calls": 0},
            "automation_checks": ["loop_closer 4 loops", "soul_drift scores", "pinterest account setup"],
            "research": ["boomer_affiliate_alpha", "tiktok trending sounds", "pinterest SEO keywords"]
        },
        12: {
            "theme": "EAS OFFENSIVE",
            "tasks": [
                "Send 20 personalized EAS outreach emails to scored leads from eas_lead_pipeline",
                "Cold call 5 highest-scored local business leads (use Bland AI if available)",
                "Send cold email batch 5: 75 emails (350 total) with best-performing subject lines",
                "Post 8 tweets + 1 thread: EAS case study or automation ROI breakdown",
                "Reply to 60 accounts + 10 LinkedIn comments on business automation posts",
                "DM 10 local business owners on Instagram/Facebook who posted about being 'overwhelmed'",
                "Post 3 TikToks showing real automation results (screen recordings)",
                "Set up Beehiiv newsletter + create lead magnet (free automation checklist PDF)",
                "Create first Facebook ad creative ($0 spend yet, just build the assets)",
                "Verify eas_lead_pipeline scored leads correctly, check scraper accuracy",
                "Run security_audit.py — review any findings",
                "Read EAS venture docs in MONEY_METHODS/EAS/ — refine pricing based on competitor research"
            ],
            "revenue_target": "$30-200",
            "content": {"tweets": 8, "threads": 1, "tiktoks": 3, "youtube": 0, "newsletters": 0},
            "engagement": {"replies": 60, "dms": 10, "comments": 20, "follows": 40},
            "outreach": {"cold_emails": 95, "proposals": 0, "calls": 5},
            "automation_checks": ["eas_lead_pipeline", "security_audit", "bland_ai availability"],
            "research": ["EAS competitor pricing", "local biz pain points", "bland AI call scripts"]
        },
        13: {
            "theme": "PAID EXPERIMENT",
            "tasks": [
                "If budget: launch $5/day Facebook ad targeting men 55-70 (boomer demo), golf/fishing/health interests",
                "If no budget: post in 10 Facebook Groups with boomer-targeted content (organic substitute)",
                "A/B test 2 ad creatives: one educational, one curiosity-hook",
                "Post 8 tweets + 2 threads (one growth update, one tactical lesson)",
                "Reply to 60 accounts + double-engage with anyone who replied to your last 3 days of threads",
                "DM 15 people: 5 newsletter subscribers (if any), 5 thread engagers, 5 cold prospects",
                "Submit 10 Upwork proposals on fresh jobs (55 total, close rate tracking starts now)",
                "Post YouTube Shorts cut from Video #2 + 3 new TikToks",
                "Write newsletter issue #1: recap of Week 2 learnings (builds trust + email list)",
                "Verify all cron jobs via crontab -l, check for any that silently failed",
                "Review method_discovery_crawler — any new methods discovered this week?",
                "Read competitor newsletters in AI/automation space — note their hooks and CTAs"
            ],
            "revenue_target": "$30-200",
            "content": {"tweets": 8, "threads": 2, "tiktoks": 3, "youtube": 0, "newsletters": 1},
            "engagement": {"replies": 60, "dms": 15, "comments": 15, "follows": 45},
            "outreach": {"cold_emails": 0, "proposals": 10, "calls": 0},
            "automation_checks": ["crontab full audit", "facebook ad delivery (if active)", "method_discovery_crawler"],
            "research": ["new revenue methods", "competitor newsletters", "facebook ad benchmarks"]
        },
        14: {
            "theme": "WEEK 2 WAR ROOM",
            "tasks": [
                "Full Week 2 analytics: compare all channels side-by-side in spreadsheet",
                "Calculate: total emails sent vs replies vs calls booked vs revenue (full funnel)",
                "Calculate: total proposals vs responses vs gigs won vs revenue per gig",
                "Calculate: content pieces vs impressions vs clicks vs conversions",
                "Rank every channel by revenue per hour — top 3 get 3x resources in Week 3",
                "Post 5 tweets + 1 thread: 'Week 2 numbers (transparent growth update)'",
                "Reply to 30 accounts + handle all DM conversations in progress",
                "Batch create 30 tweets + 7 threads for Week 3",
                "Script 5 TikToks + 1 YouTube video for next week",
                "Verify backup system ran, check agent resilience logs for any circuit breaker triggers",
                "Review ACTIONABLE_QUEUE.md — execute any queued items not yet done",
                "Deep dive CAPITAL_GENESIS_PRIORITY_STACK.md — rewrite Week 3 if priorities shifted"
            ],
            "revenue_target": "$50-250",
            "content": {"tweets": 5, "threads": 1, "tiktoks": 0, "youtube": 0, "newsletters": 0},
            "engagement": {"replies": 30, "dms": 5, "comments": 5, "follows": 15},
            "outreach": {"cold_emails": 0, "proposals": 0, "calls": 0},
            "automation_checks": ["backup system", "agent resilience logs", "circuit breaker status"],
            "research": ["full funnel analysis", "ACTIONABLE_QUEUE.md", "capital_genesis rerank"]
        },
        # ===== WEEK 3: OPTIMIZATION (kill losers, scale winners, edge tactics) =====
        15: {
            "theme": "KILL AND SCALE",
            "tasks": [
                "KILL: Any venture with 0 traction after 14 days of effort — document why, free up time",
                "SCALE: 3x resources on top 2 performing channels (more content, more outreach, more engagement)",
                "Deploy edge tactic #1: strategic follow/unfollow on secondary accounts (50 follows/day, unfollow after 3 days if no followback)",
                "Send cold email batch 6: 100 emails (450 total) — use only best-performing template",
                "Post 10 tweets + 2 threads on primary + 5 tweets on secondary account cross-promoting",
                "Reply to 75 accounts on primary + 20 on secondary (total 95 engagement actions)",
                "DM 20 people: mix of warm leads, cold prospects, and collaboration pitches",
                "Post 3 TikToks + 2 YouTube Shorts",
                "Launch newsletter lead magnet: tweet link, pin to profile, add to all bios",
                "Verify edge_growth_engine is tracking follow/unfollow ratios within platform limits",
                "Check competitive_cognition_audit output — any strategic blind spots?",
                "Review GREY_HAT_EDGE_GROWTH_MASTER.md Section 4 (Lead Gen Edge) for next tactic to deploy"
            ],
            "revenue_target": "$50-300",
            "content": {"tweets": 15, "threads": 2, "tiktoks": 3, "youtube": 0, "newsletters": 0},
            "engagement": {"replies": 95, "dms": 20, "comments": 20, "follows": 75},
            "outreach": {"cold_emails": 100, "proposals": 0, "calls": 0},
            "automation_checks": ["edge_growth_engine", "competitive_cognition_audit", "follow/unfollow ratios"],
            "research": ["lead gen edge tactics", "killed ventures post-mortem", "scaled channel playbook"]
        },
        16: {
            "theme": "NEWSLETTER ENGINE",
            "tasks": [
                "Write newsletter #2 with best content from Week 2 + exclusive alpha not posted publicly",
                "Set up 3-email welcome sequence in Beehiiv (value, value, soft sell)",
                "Add newsletter opt-in to: Gumroad checkout, YouTube desc, Twitter pinned tweet, TikTok bio, all landing pages",
                "Post 10 tweets + 2 threads promoting newsletter with specific value hooks (not 'subscribe to my newsletter')",
                "Reply to 75 accounts + engage heavily with anyone who subscribes",
                "DM 15 people who engaged with newsletter tweets offering exclusive bonus for subscribing",
                "Send cold email batch 7: 75 emails (525 total) — add newsletter CTA to email signature",
                "Submit 10 Upwork proposals (65 total, track win rate this week)",
                "Post 3 TikToks showing behind-the-scenes of your automation system",
                "Check daily_digest output — surface any missed opportunities from last 48 hours",
                "Verify prompt_meta_review ran — any lost threads or forgotten goals?",
                "Read competitor newsletters: how do they monetize? Sponsorships? Paid tier? Affiliate?"
            ],
            "revenue_target": "$50-300",
            "content": {"tweets": 10, "threads": 2, "tiktoks": 3, "youtube": 0, "newsletters": 1},
            "engagement": {"replies": 75, "dms": 15, "comments": 15, "follows": 50},
            "outreach": {"cold_emails": 75, "proposals": 10, "calls": 0},
            "automation_checks": ["daily_digest", "prompt_meta_review", "beehiiv delivery rates"],
            "research": ["competitor newsletter monetization", "welcome sequence benchmarks", "email list growth tactics"]
        },
        17: {
            "theme": "AFFILIATE LAUNCH",
            "tasks": [
                "Write 5 affiliate review posts/threads: boomer demo (health supplements, golf tech, fishing gear, financial tools, insurance comparison)",
                "Post affiliate content on: 3 Facebook Groups (boomer), 2 Reddit posts, 2 Pinterest pins, 1 YouTube Short",
                "Apply to 5 affiliate programs: health/supplement (10-15% commission), SaaS tools ($50-500/referral)",
                "Post 10 tweets + 1 thread: '5 tools I actually use for X' (affiliate links in thread)",
                "Reply to 75 accounts + target people asking 'what tool should I use for X?'",
                "DM 10 accounts who asked tool recommendation questions with genuine comparison + affiliate link",
                "Send 25 EAS follow-up emails to all previous outreach (Day 7/14 follow-ups)",
                "Cold call 5 warmest EAS leads (people who opened emails multiple times)",
                "Post 3 TikToks: product review format (hook: 'Stop paying for X when Y exists')",
                "Verify affiliate link tracking is working across all platforms",
                "Check compliance_scanner output — all affiliate content FTC compliant?",
                "Read BOOMER_MALE_55_70_AFFILIATE.md — refine content angles based on first engagement data"
            ],
            "revenue_target": "$75-350",
            "content": {"tweets": 10, "threads": 1, "tiktoks": 3, "youtube": 0, "newsletters": 0},
            "engagement": {"replies": 75, "dms": 10, "comments": 15, "follows": 50},
            "outreach": {"cold_emails": 25, "proposals": 0, "calls": 5},
            "automation_checks": ["affiliate link tracking", "compliance_scanner", "FTC disclosures"],
            "research": ["boomer affiliate performance data", "highest-commission programs", "affiliate content formats"]
        },
        18: {
            "theme": "EAS CLOSE PUSH",
            "tasks": [
                "Call/email top 5 warmest EAS leads — push for discovery call or proposal request",
                "Send 5 custom EAS proposals ($1,500-4,500 packages from MONEY_METHODS/EAS/)",
                "Create EAS case study draft: even if no paying client yet, document a system you built for yourself as proof",
                "Send cold email batch 8: 75 emails (600 total) — new list segment if current list exhausted",
                "Post 10 tweets + 2 threads (1 EAS value prop thread, 1 tactical content)",
                "Reply to 75 accounts + prioritize any business owners in replies",
                "DM 15 local business owners from Instagram/Facebook who posted about growth/operations",
                "Post YouTube video #3 (EAS-themed: 'How I automate a business in 48 hours')",
                "Upload 3 TikToks + cross-post to Shorts",
                "Verify eas_lead_pipeline scoring accuracy — are high-scored leads converting to replies?",
                "Check agent_swarm model routing — are Opus/Sonnet/Haiku assignments optimal?",
                "Read EAS legal docs — have MSA and SOW ready for any deal that closes"
            ],
            "revenue_target": "$100-500",
            "content": {"tweets": 10, "threads": 2, "tiktoks": 3, "youtube": 1, "newsletters": 0},
            "engagement": {"replies": 75, "dms": 15, "comments": 15, "follows": 45},
            "outreach": {"cold_emails": 75, "proposals": 5, "calls": 5},
            "automation_checks": ["eas_lead_pipeline accuracy", "agent_swarm model routing", "youtube analytics"],
            "research": ["EAS proposal refinement", "legal doc readiness", "competitor EAS pricing"]
        },
        19: {
            "theme": "CONTENT FLOOD",
            "tasks": [
                "Batch create 15 TikToks (3 per day for the rest of the week)",
                "Batch create 5 YouTube Shorts (cuts from existing content + new hooks)",
                "Batch 10 Facebook posts targeting boomer demo across 5 different groups",
                "Write newsletter #3 with Week 3 alpha + exclusive offer for subscribers",
                "Post 10 tweets + 2 threads (1 engagement-bait thread, 1 value thread)",
                "Reply to 75 accounts + comment on 10 viral posts within first hour of trending",
                "DM 20 people: 10 engaged followers + 5 potential clients + 5 potential partners",
                "Deploy secondary account strategy: 5 tweets from secondary promoting primary content",
                "Post 5 Pinterest pins with affiliate-linked products (boomer targeting)",
                "Verify all content was posted across platforms — check Buffer/Typefully/Publer queues",
                "Run system_visualizer — review SYSTEM_VISUAL.html for architecture gaps",
                "Read daily_tool_scout + method_discovery_crawler — any emergent tactics?"
            ],
            "revenue_target": "$100-500",
            "content": {"tweets": 15, "threads": 2, "tiktoks": 3, "youtube": 0, "newsletters": 1},
            "engagement": {"replies": 75, "dms": 20, "comments": 20, "follows": 50},
            "outreach": {"cold_emails": 0, "proposals": 0, "calls": 0},
            "automation_checks": ["content queue verification", "system_visualizer", "posting tool uptime"],
            "research": ["daily_tool_scout", "method_discovery_crawler", "emerging content formats"]
        },
        20: {
            "theme": "EDGE TACTICS",
            "tasks": [
                "Deploy edge tactic #2: Engagement pod activation — coordinate replies with 5-10 aligned accounts on each other's posts",
                "Deploy edge tactic #3: Quote-tweet viral posts with contrarian take within 15 min (sets up reply thread visibility)",
                "If FB ads running: review Day 7 data, kill losers, double budget on winner",
                "If no FB ads: deploy edge tactic #4 — create 2 more secondary accounts for cross-promotion network",
                "Send cold email batch 9: 50 emails (650 total) — only to highest-engagement segments",
                "Post 10 tweets + 1 thread from primary + 5 tweets from secondary accounts",
                "Reply to 80 accounts (push engagement ceiling higher)",
                "DM 15 people with highest interaction scores this week",
                "Post 3 TikToks + 2 YouTube Shorts (top-performing format from analytics)",
                "Review all edge tactic deployment: are they producing measurable lift?",
                "Verify sqlite_alpha_index is up to date, run FTS search for 'edge growth' tactics",
                "Read GREY_HAT_EDGE_GROWTH_MASTER.md Section 9 (Shadowban Detection) — proactive monitoring"
            ],
            "revenue_target": "$100-500",
            "content": {"tweets": 15, "threads": 1, "tiktoks": 3, "youtube": 0, "newsletters": 0},
            "engagement": {"replies": 80, "dms": 15, "comments": 15, "follows": 55},
            "outreach": {"cold_emails": 50, "proposals": 0, "calls": 0},
            "automation_checks": ["sqlite_alpha_index", "edge tactic lift measurement", "shadowban detection"],
            "research": ["shadowban detection protocols", "engagement pod effectiveness", "edge tactic ROI"]
        },
        21: {
            "theme": "WEEK 3 CALIBRATION",
            "tasks": [
                "Trajectory check: are we on track for $1K this month? If not, identify the 1 biggest bottleneck.",
                "Revenue gap analysis: what's the shortest path from current revenue to $1K? Double down there.",
                "Full engagement audit: which platform has highest engagement-to-revenue conversion?",
                "If any venture crossed $100 revenue this week: create SOP to replicate it 3x",
                "Post 5 tweets + 1 thread: transparent Week 3 update with real numbers",
                "Reply to 30 accounts + handle all pending DM conversations",
                "Batch create 30 tweets + 7 threads + 5 TikToks for Week 4",
                "Batch create 5 YouTube Shorts + 1 full YouTube script for Week 4",
                "Write cold email batch for Week 4: 100 emails pre-drafted with personalization tokens",
                "Verify backup system, run full system_health_monitor, review all logs for silent failures",
                "Run competitive_cognition_audit — identify strategic improvements",
                "Review CAPITAL_GENESIS_PRIORITY_STACK.md — are we working on the highest-ROI tasks?"
            ],
            "revenue_target": "$100-600",
            "content": {"tweets": 5, "threads": 1, "tiktoks": 0, "youtube": 0, "newsletters": 0},
            "engagement": {"replies": 30, "dms": 5, "comments": 5, "follows": 15},
            "outreach": {"cold_emails": 0, "proposals": 0, "calls": 0},
            "automation_checks": ["full system health", "backup verification", "competitive_cognition_audit"],
            "research": ["trajectory analysis", "bottleneck identification", "capital_genesis rerank"]
        },
        # ===== WEEK 4: COMPOUND (recurring revenue, partnerships, scale what works) =====
        22: {
            "theme": "REVENUE ENGINE",
            "tasks": [
                "Rank ALL channels by revenue/hour: top 3 get 80% of remaining effort this month",
                "Pitch retainer to best freelance client: $500-2K/month for ongoing automation support",
                "Set up subscription tier on Gumroad/Whop: monthly automation templates ($19/mo) or community ($49/mo)",
                "Send cold email batch 10: 100 emails (750 total) — only to hottest segments",
                "Post 10 tweets + 2 threads (1 revenue milestone thread, 1 tactical value thread)",
                "Reply to 80 accounts + 15 DMs targeting decision-makers",
                "Post 3 TikToks + 1 YouTube video (tutorial on your best-converting content topic)",
                "Follow up on ALL open proposals (Upwork, EAS, freelance) — create urgency",
                "Create upsell path: anyone who bought a $15 product gets email offering $50 product or $99 package",
                "Verify all revenue tracking is accurate: Gumroad dashboard, Fiverr earnings, Upwork, affiliate dashboards",
                "Check loop_closer pipeline_advancement — are deals moving through stages?",
                "Read DEFINITIVE_GROWTH_STACK.md Section on paid experiments for May planning"
            ],
            "revenue_target": "$150-600",
            "content": {"tweets": 10, "threads": 2, "tiktoks": 3, "youtube": 1, "newsletters": 0},
            "engagement": {"replies": 80, "dms": 15, "comments": 15, "follows": 50},
            "outreach": {"cold_emails": 100, "proposals": 5, "calls": 3},
            "automation_checks": ["revenue tracking accuracy", "loop_closer pipeline", "subscription setup verification"],
            "research": ["paid experiment planning", "retainer pricing research", "upsell funnel benchmarks"]
        },
        23: {
            "theme": "RECURRING REVENUE",
            "tasks": [
                "Convert any one-time buyers to subscribers: email all Gumroad buyers with subscription offer",
                "Launch Telegram VIP channel ($49-99/mo) with exclusive alpha/automation content",
                "Create 3 pieces of exclusive subscriber-only content (template, tutorial, or tool)",
                "Send cold email batch 11: 75 emails (825 total) — add testimonial/social proof to template",
                "Post 10 tweets + 2 threads (1 subscriber testimonial/value thread, 1 growth thread)",
                "Reply to 80 accounts + engage heavily with anyone discussing recurring revenue/subscriptions",
                "DM 20 people: 10 existing buyers/engagers + 10 cold prospects",
                "Post 3 TikToks showing 'day in the life of running automated business'",
                "Newsletter #4 with exclusive subscriber offer + referral incentive",
                "Verify Telegram VIP channel is set up with payment gateway working",
                "Check daily_engagement_planner — is the warmup schedule aligned with our volume?",
                "Read community venture docs (M01-M06) — what's the best community monetization path?"
            ],
            "revenue_target": "$150-700",
            "content": {"tweets": 10, "threads": 2, "tiktoks": 3, "youtube": 0, "newsletters": 1},
            "engagement": {"replies": 80, "dms": 20, "comments": 15, "follows": 50},
            "outreach": {"cold_emails": 75, "proposals": 0, "calls": 0},
            "automation_checks": ["telegram payment gateway", "engagement_planner alignment", "subscriber tracking"],
            "research": ["community monetization", "telegram channel benchmarks", "subscription pricing psychology"]
        },
        24: {
            "theme": "PRODUCT HUNT PREP",
            "tasks": [
                "Pick best product for Product Hunt launch: must have clear value prop and professional landing page",
                "Prepare launch assets: 5 screenshots, 60-sec demo video, tagline, description, first comment",
                "Recruit 10 hunters/upvoters: DM people who upvoted similar products recently",
                "Create pre-launch buzz: tweet about upcoming launch 3x today with teaser content",
                "Post 10 tweets + 2 threads (1 pre-launch hype, 1 building-in-public)",
                "Reply to 75 accounts + engage with anyone in the Product Hunt community",
                "DM 15 people who launched on Product Hunt recently — ask for tips and mutual upvote",
                "Post 3 TikToks about the product you're launching",
                "Submit 10 Upwork proposals (75 total) — track close rate at this point",
                "Verify product landing page loads fast, checkout works, all links functional",
                "Check system_health_monitor for any degraded services before launch",
                "Read Product Hunt launch playbooks — timing, first-hour strategy, comment engagement"
            ],
            "revenue_target": "$150-700",
            "content": {"tweets": 10, "threads": 2, "tiktoks": 3, "youtube": 0, "newsletters": 0},
            "engagement": {"replies": 75, "dms": 15, "comments": 15, "follows": 45},
            "outreach": {"cold_emails": 0, "proposals": 10, "calls": 0},
            "automation_checks": ["landing page performance", "checkout flow", "system health pre-launch"],
            "research": ["Product Hunt launch playbooks", "competitor PH launches", "upvote community strategy"]
        },
        25: {
            "theme": "LAUNCH DAY",
            "tasks": [
                "Execute Product Hunt launch at 12:01 AM PT (schedule it the night before)",
                "Post first comment immediately with the story + ask-me-anything",
                "DM all 10 recruited upvoters: 'We are live, link here'",
                "Monitor PH every 30 min: respond to EVERY comment within 15 minutes",
                "Post 15 tweets throughout the day promoting the launch + sharing milestones",
                "Write 1 launch thread: 'How I built X from zero — the story'",
                "Share launch link: Reddit (r/SaaS, r/SideProject), LinkedIn, Facebook Groups, Discord servers, Indie Hackers",
                "Send newsletter blast to all subscribers: 'We just launched on Product Hunt'",
                "Reply to 50 accounts minimum — today is all-engagement mode",
                "DM 20 people who upvoted or commented on PH page thanking them",
                "Verify PH analytics tracking: are upvotes/visits/conversions being counted?",
                "Document everything: PH position, upvote count, comments, traffic spike — this is content for next week"
            ],
            "revenue_target": "$200-1000",
            "content": {"tweets": 15, "threads": 1, "tiktoks": 0, "youtube": 0, "newsletters": 1},
            "engagement": {"replies": 50, "dms": 20, "comments": 30, "follows": 30},
            "outreach": {"cold_emails": 0, "proposals": 0, "calls": 0},
            "automation_checks": ["PH analytics", "traffic spike handling", "checkout under load"],
            "research": ["real-time PH ranking position", "competitor launches today", "conversion rate from PH traffic"]
        },
        26: {
            "theme": "EAS FINAL PUSH",
            "tasks": [
                "Push hardest EAS prospect to close: send final proposal with 48-hour expiry and 10% early-bird discount",
                "Call top 3 EAS leads — voice builds trust faster than email",
                "If deal closes: begin delivery within 24 hours, set scope expectations via MSA/SOW",
                "If no close: analyze objections, adjust pitch, add the learnings to EAS playbook",
                "Send cold email batch 12: 50 emails (875 total) with PH launch as social proof",
                "Post 10 tweets + 1 thread: PH results recap + lessons learned",
                "Reply to 75 accounts + thank everyone who supported the PH launch",
                "DM 15 people who engaged during launch but didn't convert — what's the objection?",
                "Post 3 TikToks recapping the launch (authentic, raw, no polish)",
                "Upload YouTube video #4: PH launch documentary or results video",
                "Verify all revenue from launch is tracked: PH referrals, direct sales, email signups",
                "Read EAS MSA/SOW templates — be ready to send contract same day if deal closes"
            ],
            "revenue_target": "$200-1000",
            "content": {"tweets": 10, "threads": 1, "tiktoks": 3, "youtube": 1, "newsletters": 0},
            "engagement": {"replies": 75, "dms": 15, "comments": 15, "follows": 40},
            "outreach": {"cold_emails": 50, "proposals": 3, "calls": 3},
            "automation_checks": ["revenue tracking post-launch", "EAS contract readiness", "delivery pipeline"],
            "research": ["EAS objection handling", "post-launch conversion tactics", "MSA/SOW templates"]
        },
        27: {
            "theme": "CONVERSION OPTIMIZATION",
            "tasks": [
                "A/B test: Gumroad product titles, descriptions, and prices for top 3 sellers",
                "A/B test: cold email subject lines, opening lines, and CTAs across segments",
                "Add upsells/cross-sells to all product checkout pages",
                "Create urgency: limited-time bundle offer combining 3 best products at discount",
                "Post 10 tweets + 1 thread: 'X things I learned from sending 875 cold emails'",
                "Reply to 60 accounts + focus on conversion-oriented engagement (people asking questions = answer with product links)",
                "DM 10 warmest leads with personalized offer based on their specific engagement history",
                "Optimize email sequences: rewrite any email with < 20% open rate or < 2% click rate",
                "Post 3 TikToks + 2 YouTube Shorts focused on top-converting topic",
                "Verify Gumroad analytics match expected revenue, check for payment failures",
                "Run full alpha_auto_processor batch — clear all PENDING_REVIEW entries",
                "Read conversion optimization research — landing page best practices, pricing psychology"
            ],
            "revenue_target": "$200-800",
            "content": {"tweets": 10, "threads": 1, "tiktoks": 3, "youtube": 0, "newsletters": 0},
            "engagement": {"replies": 60, "dms": 10, "comments": 10, "follows": 35},
            "outreach": {"cold_emails": 0, "proposals": 0, "calls": 0},
            "automation_checks": ["gumroad payment tracking", "alpha_auto_processor", "A/B test tracking"],
            "research": ["conversion optimization", "pricing psychology", "upsell funnel design"]
        },
        28: {
            "theme": "MAY WAR PLAN",
            "tasks": [
                "Full month review: actual revenue vs 3 scenarios (conservative/medium/aggressive)",
                "Per-channel breakdown: revenue, time invested, ROI per hour, growth trajectory",
                "Identify top 3 ventures for May: allocate 80% of effort to these three",
                "Kill list: finalize which ventures get cut in May (< $50 revenue after full month)",
                "Scale list: which ventures get 3x resources in May (> $200 revenue or > 5% engagement)",
                "Post 5 tweets + 1 thread: 'Month 1 retrospective — the honest numbers'",
                "Reply to 30 accounts + handle all open DM conversations",
                "Write May roadmap with adjusted targets based on April data",
                "Set May daily KPI targets based on actual conversion rates from April",
                "Verify all automated systems are stable for overnight/weekend operation",
                "Review all agent outputs from the month — any consistently underperforming?",
                "Document procedural memory: what worked, what didn't, what to never do again"
            ],
            "revenue_target": "$200-800",
            "content": {"tweets": 5, "threads": 1, "tiktoks": 0, "youtube": 0, "newsletters": 0},
            "engagement": {"replies": 30, "dms": 5, "comments": 5, "follows": 15},
            "outreach": {"cold_emails": 0, "proposals": 0, "calls": 0},
            "automation_checks": ["all systems stability check", "agent performance audit", "cron job health"],
            "research": ["month 1 retrospective analysis", "May target setting", "procedural memory capture"]
        },
        29: {
            "theme": "AUTOMATE EVERYTHING",
            "tasks": [
                "Automate any task you did manually more than 3 times this month: create script + add to cron",
                "Set up new cron jobs for any recurring workflow discovered during April",
                "Create automated reporting: daily revenue email, weekly channel performance, monthly summary",
                "Deploy any backlogged automation from ACTIONABLE_QUEUE.md",
                "Post 10 tweets + 1 thread: 'How I automated X (so I never have to do it again)'",
                "Reply to 60 accounts + engage with anyone discussing automation/efficiency",
                "DM 10 people: potential May collaboration partners",
                "Send cold email batch 13: 50 emails (925 total) — warm up May pipeline early",
                "Post 3 TikToks showing real automation workflows in action",
                "Update PRINTMAXX_SYSTEM_MAP.md with all April changes",
                "Clean up dead ventures: archive docs, remove orphan cron jobs, update intelligence catalog",
                "Read NOVEL_DISCOVERIES.md — any patterns worth extracting to sovrun?"
            ],
            "revenue_target": "$200-800",
            "content": {"tweets": 10, "threads": 1, "tiktoks": 3, "youtube": 0, "newsletters": 0},
            "engagement": {"replies": 60, "dms": 10, "comments": 10, "follows": 40},
            "outreach": {"cold_emails": 50, "proposals": 0, "calls": 0},
            "automation_checks": ["new cron jobs deployed", "ACTIONABLE_QUEUE cleared", "system_map updated"],
            "research": ["NOVEL_DISCOVERIES.md", "automation candidates", "May pipeline warmup"]
        },
        30: {
            "theme": "MONTH 1 CLOSE",
            "tasks": [
                "Final revenue count: total April earnings across ALL channels",
                "Update KPI_DASHBOARD.md with actual April numbers vs projections",
                "Revenue leaderboard: rank every venture by actual revenue generated",
                "Engagement leaderboard: total followers gained, engagement rate, growth trajectory",
                "Outreach leaderboard: total emails sent, reply rate, close rate, revenue per email",
                "Post 10 tweets + 1 thread: 'Month 1 complete — here are the real numbers (no cap)'",
                "Reply to 60 accounts + post retrospective on LinkedIn",
                "Send newsletter #5: month in review + what's coming in May (build anticipation)",
                "Update all bios/profiles with any new credentials or milestones from April",
                "Full system health audit: all 112 cron jobs, all 33 agents, all scrapers, all pipelines",
                "Run capital_genesis_ranker --rank --report — generate fresh May priority stack",
                "Set 3 stretch goals for May that would change everything if achieved"
            ],
            "revenue_target": "$250-1000",
            "content": {"tweets": 10, "threads": 1, "tiktoks": 0, "youtube": 0, "newsletters": 1},
            "engagement": {"replies": 60, "dms": 10, "comments": 10, "follows": 30},
            "outreach": {"cold_emails": 0, "proposals": 0, "calls": 0},
            "automation_checks": ["full system audit", "capital_genesis_ranker", "all 33 agents operational"],
            "research": ["month 1 data analysis", "May priority stack", "stretch goal feasibility"]
        },
    }

    default_plan = {
        "theme": "FLEX",
        "tasks": ["Continue top 3 priority ventures", "Post 5 tweets + engage 30 accounts", "Review daily_digest + alpha_staging",
                  "Follow up on all open proposals and DMs", "Monitor revenue dashboards", "Check cron job health",
                  "Process 50 alpha entries", "Post 2 TikToks from batch"],
        "revenue_target": "TBD",
        "content": {"tweets": 5, "threads": 0, "tiktoks": 2, "youtube": 0, "newsletters": 0},
        "engagement": {"replies": 30, "dms": 5, "comments": 5, "follows": 15},
        "outreach": {"cold_emails": 0, "proposals": 0, "calls": 0},
        "automation_checks": ["daily_digest", "cron health", "scraper outputs"],
        "research": ["alpha_staging", "capital_genesis_priority_stack"]
    }

    # Weekly phase labels
    week_phases = {1: "FOUNDATION", 2: "VOLUME", 3: "OPTIMIZATION", 4: "COMPOUND"}

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
