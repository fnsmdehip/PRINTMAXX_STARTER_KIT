#!/usr/bin/env python3
"""
VENTURE AUTONOMY ENGINE — Universal OpenClaw-Level Autonomy for ALL Ventures
=============================================================================

Turns ANY venture into a fully autonomous find→build→pitch→close pipeline.
OpenClaw (local biz) was the example. This is the generalized framework.

Every venture type gets its own autonomy loop:
  OUTBOUND  → find prospects → qualify → build assets → send outreach → track
  CONTENT   → find topics → generate content → schedule posts → track engagement
  APP       → find gaps → build MVP → deploy → ASO optimize → track downloads
  LOCAL_BIZ → find businesses → grade sites → build previews → outreach → close
  RESEARCH  → scrape sources → analyze → score → route to actions → compound
  MONETIZE  → find offers → create funnels → deploy pages → track conversions
  PRODUCT   → find demand → build product → create listing → distribute → sell
  BROKERING → scrape targets → qualify leads → connect parties → earn fee → track revenue

The engine:
  1. Reads venture definitions (from CEO agent, xlsx, or manual)
  2. Matches venture type to autonomy template
  3. Executes the full pipeline per venture
  4. Generates scheduled task configs (launchd + Cowork prompts)
  5. Tracks results and feeds back into CEO loop

Usage:
  python3 venture_autonomy.py --status              # Show all autonomous ventures
  python3 venture_autonomy.py --run VENTURE_ID       # Run one venture's full cycle
  python3 venture_autonomy.py --run-all              # Run all active ventures
  python3 venture_autonomy.py --create TYPE NAME     # Create new autonomous venture
  python3 venture_autonomy.py --schedule             # Generate launchd + Cowork configs
  python3 venture_autonomy.py --list-types           # Show all venture types + templates
  python3 venture_autonomy.py --self-manage            # Run self-management cycle (auto-install/fix/adjust/prune)
  python3 venture_autonomy.py --daemon               # Run forever cycling all ventures
"""

from __future__ import annotations

import argparse
import csv
csv.field_size_limit(10 * 1024 * 1024)
import json
import os
import signal
import subprocess
import sys
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Optional

# Ensure sibling modules are importable when run from project root
sys.path.insert(0, str(Path(__file__).resolve().parent))

from agent_resilience import (
    sanitize_for_prompt, locked_file, TrajectoryLogger,
)

# Sovrun modules — procedural memory for venture skill recall
_SOVRUN_PATH = str(Path(__file__).resolve().parent.parent / "OPEN_SOURCE" / "agent-soul")
if _SOVRUN_PATH not in sys.path:
    sys.path.insert(0, _SOVRUN_PATH)

try:
    from core.procedural_memory import ProceduralMemory as _ProceduralMemory
    _SOVRUN_AVAILABLE = True
except ImportError:
    _SOVRUN_AVAILABLE = False

try:
    from master_ops_bridge import MasterOpsBridge
    _BRIDGE_AVAILABLE = True
except ImportError:
    _BRIDGE_AVAILABLE = False

_trajectory = TrajectoryLogger("venture_autonomy")


def _recall_venture_skills(venture_type: str, task: str = "") -> str:
    """Query sovrun procedural memory for skills relevant to this venture."""
    if not _SOVRUN_AVAILABLE:
        return ""
    try:
        db_path = AUTOMATIONS / "agent" / "sovrun" / "skills.db"
        db_path.parent.mkdir(parents=True, exist_ok=True)
        mem = _ProceduralMemory(db_path=db_path)
        query = f"{venture_type} {task}".strip()
        injection = mem.export_injection(query, max_chars=400)
        mem.close()
        return injection
    except Exception:
        return ""


def _capture_venture_skill(venture_type: str, task: str, result: str, success: bool = True) -> None:
    """Capture a venture execution as a procedural skill."""
    if not _SOVRUN_AVAILABLE or not success or len(task.strip()) < 10:
        return
    try:
        db_path = AUTOMATIONS / "agent" / "sovrun" / "skills.db"
        db_path.parent.mkdir(parents=True, exist_ok=True)
        mem = _ProceduralMemory(db_path=db_path)
        mem.capture(task=f"[{venture_type}] {task}", result=result[:1000], success=True)
        mem.close()
    except Exception:
        pass

# ── paths & guardrails ───────────────────────────────────────────────────
PROJECT = Path("/Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt")
AUTOMATIONS = PROJECT / "AUTOMATIONS"
VENTURES_DIR = AUTOMATIONS / "agent" / "ceo_agent" / "ventures"
AUTONOMY_DIR = AUTOMATIONS / "agent" / "autonomy"
SCHEDULES_DIR = AUTONOMY_DIR / "schedules"
RESULTS_DIR = AUTONOMY_DIR / "results"
STATE_FILE = AUTONOMY_DIR / "autonomy_state.json"
LOG_FILE = AUTOMATIONS / "logs" / "venture_autonomy.log"
MISSION_LOG = AUTOMATIONS / "agent" / "missions.jsonl"
MESSAGE_BUS = AUTOMATIONS / "agent" / "message_bus.jsonl"
AGENT_STATE = AUTOMATIONS / "agent" / "state.json"
PYTHON = sys.executable

_shutdown = False
def _sig(s: int, f: Any) -> None:
    global _shutdown
    _shutdown = True
    print("\n[!] Shutdown requested.")
signal.signal(signal.SIGINT, _sig)
signal.signal(signal.SIGTERM, _sig)


def safe_path(p: str | Path) -> Path:
    resolved = Path(p).resolve()
    if not str(resolved).startswith(str(PROJECT.resolve())):
        raise ValueError(f"BLOCKED: {resolved} outside {PROJECT}")
    return resolved


def ts() -> str:
    return datetime.now().strftime("%H:%M:%S")


def log(msg: str, level: str = "INFO") -> None:
    line = f"[{ts()}] [AUTONOMY] [{level}] {msg}"
    print(line)
    try:
        LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(LOG_FILE, "a") as f:
            f.write(line + "\n")
    except Exception:
        pass


def run_cmd(cmd: str, timeout_sec: int = 300, label: Optional[str] = None) -> tuple[bool, str]:
    """Run a command with guardrails. Returns (success, output)."""
    tag = label or cmd[:60]
    log(f"Running: {tag}")
    try:
        result = subprocess.run(
            cmd, shell=True, capture_output=True, text=True,
            timeout=timeout_sec, cwd=str(PROJECT)
        )
        output = (result.stdout or "") + (result.stderr or "")
        output = output[-3000:]
        if result.returncode == 0:
            log(f"  OK: {tag}")
            return True, output
        else:
            log(f"  FAIL (rc={result.returncode}): {tag}", "WARN")
            return False, output
    except subprocess.TimeoutExpired:
        log(f"  TIMEOUT ({timeout_sec}s): {tag}", "WARN")
        return False, f"Timed out after {timeout_sec}s"
    except Exception as e:
        log(f"  ERROR: {tag}: {e}", "ERROR")
        return False, str(e)[:500]


def run_script(script_name: str, args: str = "", timeout_sec: int = 300, label: Optional[str] = None) -> tuple[bool, str]:
    """Run a PRINTMAXX automation script."""
    script_path = AUTOMATIONS / script_name
    if not script_path.exists():
        log(f"Script not found: {script_path}", "WARN")
        return False, f"Script not found: {script_name}"
    cmd = f"{PYTHON} {script_path} {args}".strip()
    return run_cmd(cmd, timeout_sec, label or script_name)


def _hours_since(iso_ts: Optional[str]) -> float:
    if not iso_ts:
        return float('inf')
    try:
        return (datetime.now() - datetime.fromisoformat(str(iso_ts))).total_seconds() / 3600
    except Exception:
        return float('inf')


def log_mission(mission_name: str, result: str, duration_s: float, output: str = "") -> None:
    """Log to the shared agent mission log (same format as monitor.py expects)."""
    entry = {
        "ts": datetime.now().isoformat(),
        "mission": mission_name,
        "result": result,
        "duration_s": round(duration_s, 1),
        "output": str(output)[:200],
    }
    try:
        with locked_file(MISSION_LOG, mode="a") as f:
            f.write(json.dumps(entry) + "\n")
    except Exception:
        pass


def send_bus_message(body: str, to_agent: str = "ceo") -> None:
    """Send a message on the shared inter-agent bus."""
    msg = {
        "ts": datetime.now().isoformat(),
        "from": "autonomy_engine",
        "to": to_agent,
        "type": "status",
        "body": str(body)[:500],
        "read": False,
    }
    try:
        with locked_file(MESSAGE_BUS, mode="a") as f:
            f.write(json.dumps(msg) + "\n")
    except Exception:
        pass


# ══════════════════════════════════════════════════════════════════════════
# VENTURE TYPES — Each type defines its autonomy pipeline
# ══════════════════════════════════════════════════════════════════════════

# Smart model routing: right model for each task
# Opus = strategy/creativity/quality. Sonnet = solid execution. Haiku = routine/maintenance.
MODEL_OPUS = "claude-opus-4-6"
MODEL_SONNET = "claude-sonnet-4-6"
MODEL_HAIKU = "claude-haiku-4-5-20251001"

# ── Steps that require human action — never waste tokens on these ──────────
# Maps (venture_type, step) -> reason string.  Checked before _run_with_claude.
HUMAN_BLOCKED_STEPS: dict[tuple[str, str], str] = {
    # BROKERING — actual fee collection needs human agreements
    ("BROKERING", "earn_fee"): "Requires signed referral agreement + payment processor",
}

# ── Heuristic fallbacks for steps that can self-verify without LLM ─────────
# Each entry: (venture_type, step) -> callable(venture_id, venture, vtype) -> (ok: bool, detail: str)
# Used when _run_with_claude fails or as a cheaper first-pass check.


def _fallback_check_files_exist(glob_pattern: str, label: str):
    """Factory: returns a heuristic that checks if matching files exist."""
    def _check(venture_id: str, venture: dict, vtype: dict) -> tuple[bool, str]:
        import glob as _glob
        venture_dir = AUTONOMY_DIR / venture_id / "output"
        venture_dir.mkdir(parents=True, exist_ok=True)
        # Also check broader project paths
        patterns = [
            str(venture_dir / glob_pattern),
            str(RESULTS_DIR / f"*{venture_id}*{glob_pattern}"),
        ]
        found = []
        for p in patterns:
            found.extend(_glob.glob(p))
        if found:
            return True, f"{label}: {len(found)} files found"
        return False, f"{label}: no matching files"
    return _check


def _fallback_content_format(venture_id: str, venture: dict, vtype: dict) -> tuple[bool, str]:
    """Check if generated content exists in any format."""
    import glob as _glob
    search_dirs = [
        str(PROJECT / "CONTENT" / "social" / "generated" / "*.txt"),
        str(PROJECT / "CONTENT" / "social" / "generated" / "*.md"),
        str(PROJECT / "CONTENT" / "social" / "posting_queue" / "*.txt"),
        str(AUTONOMY_DIR / venture_id / "output" / "*content*"),
        str(AUTONOMY_DIR / venture_id / "output" / "*generate*"),
    ]
    total = 0
    for pattern in search_dirs:
        total += len(_glob.glob(pattern))
    if total > 0:
        return True, f"format: {total} content files exist across queues"
    return False, "format: no content files found to format"


def _fallback_content_schedule(venture_id: str, venture: dict, vtype: dict) -> tuple[bool, str]:
    """Check if posting queue has scheduled content."""
    import glob as _glob
    queue_files = _glob.glob(str(PROJECT / "CONTENT" / "social" / "posting_queue" / "*.txt"))
    if queue_files:
        return True, f"schedule: {len(queue_files)} posts in posting queue"
    return False, "schedule: posting queue empty"


def _fallback_track_results(venture_id: str, venture: dict, vtype: dict) -> tuple[bool, str]:
    """Check if there are recent result/report files (< 48h old)."""
    import glob as _glob
    output_dir = AUTONOMY_DIR / venture_id / "output"
    output_dir.mkdir(parents=True, exist_ok=True)
    results = _glob.glob(str(output_dir / "*report*")) + _glob.glob(str(output_dir / "*track*"))
    if results:
        # Check freshness — any file modified in last 48h counts
        cutoff = time.time() - 48 * 3600
        recent = [f for f in results if os.path.getmtime(f) > cutoff]
        if recent:
            return True, f"track: {len(recent)} recent tracking reports"
        return False, f"track: {len(results)} reports exist but all stale (>48h)"
    return False, "track: no tracking reports yet"


def _fallback_scraping_configure(venture_id: str, venture: dict, vtype: dict) -> tuple[bool, str]:
    """Check if scraper configs exist (they're static, rarely need LLM)."""
    config_paths = [
        AUTOMATIONS / "twitter_alpha_scraper.py",
        AUTOMATIONS / "background_reddit_scraper.py",
    ]
    found = [str(p) for p in config_paths if p.exists()]
    if found:
        return True, f"configure: {len(found)} scrapers configured"
    return False, "configure: no scraper scripts found"


def _fallback_scraping_clean(venture_id: str, venture: dict, vtype: dict) -> tuple[bool, str]:
    """Check if scraped data exists in staging (cleaning is a pipeline step)."""
    staging = PROJECT / "LEDGER" / "ALPHA_STAGING.csv"
    if staging.exists() and staging.stat().st_size > 100:
        return True, f"clean: ALPHA_STAGING.csv exists ({staging.stat().st_size // 1024}KB)"
    return False, "clean: no staging data to clean"


def _fallback_scraping_store(venture_id: str, venture: dict, vtype: dict) -> tuple[bool, str]:
    """Check if LEDGER CSVs have data."""
    import glob as _glob
    csvs = _glob.glob(str(PROJECT / "LEDGER" / "*.csv"))
    if csvs:
        total_size = sum(os.path.getsize(f) for f in csvs)
        return True, f"store: {len(csvs)} LEDGER CSVs ({total_size // 1024}KB)"
    return False, "store: no LEDGER CSVs found"


def _fallback_grade_sites(venture_id: str, venture: dict, vtype: dict) -> tuple[bool, str]:
    """Check if grading results exist from previous runs."""
    import glob as _glob
    grade_files = (
        _glob.glob(str(AUTONOMY_DIR / venture_id / "output" / "*grade*")) +
        _glob.glob(str(AUTOMATIONS / "leads" / venture_id / "*grade*")) +
        _glob.glob(str(AUTOMATIONS / "leads" / venture_id / "*score*"))
    )
    if grade_files:
        return True, f"grade: {len(grade_files)} grading result files"
    return False, "grade: no grading results — run discover step first"


def _fallback_research_score(venture_id: str, venture: dict, vtype: dict) -> tuple[bool, str]:
    """Check if alpha scoring has been done (alpha_auto_processor output)."""
    staging = PROJECT / "LEDGER" / "ALPHA_STAGING.csv"
    if not staging.exists():
        return False, "score: no ALPHA_STAGING.csv"
    try:
        with open(staging) as f:
            reader = csv.reader(f)
            header = next(reader, [])
            rows = list(reader)
        scored = [r for r in rows if len(r) > 3 and r[3].strip().upper() in ("HIGHEST", "HIGH", "MEDIUM", "LOW")]
        if scored:
            return True, f"score: {len(scored)}/{len(rows)} entries scored in ALPHA_STAGING"
        return False, f"score: {len(rows)} entries but none scored yet"
    except Exception:
        return False, "score: failed to read ALPHA_STAGING.csv"


def _fallback_build_page(venture_id: str, venture: dict, vtype: dict) -> tuple[bool, str]:
    """Check if landing pages exist in LANDING/ directory."""
    import glob as _glob
    pages = _glob.glob(str(PROJECT / "LANDING" / "**" / "index.html"), recursive=True)
    if pages:
        return True, f"build_page: {len(pages)} landing pages exist"
    return False, "build_page: no landing pages in LANDING/"


def _fallback_app_spec(venture_id: str, venture: dict, vtype: dict) -> tuple[bool, str]:
    """Check if app specs exist."""
    import glob as _glob
    specs = _glob.glob(str(AUTOMATIONS / "auto_ops" / "app_specs" / "*.json"))
    specs += _glob.glob(str(AUTOMATIONS / "auto_ops" / "app_specs" / "*.md"))
    if specs:
        return True, f"spec: {len(specs)} app specs in auto_ops/app_specs/"
    return False, "spec: no app specs found"


def _fallback_app_aso(venture_id: str, venture: dict, vtype: dict) -> tuple[bool, str]:
    """Check if ASO research exists."""
    aso_script = AUTOMATIONS / "aso_keyword_research.py"
    if aso_script.exists():
        # Run the ASO script instead of LLM
        ok, output = run_script("aso_keyword_research.py", timeout_sec=120, label=f"{venture_id}:aso")
        if ok:
            return True, f"aso: keyword research script completed"
        return False, f"aso: keyword research script failed"
    return False, "aso: aso_keyword_research.py not found"


# Registry: (venture_type, step_name) -> fallback function
FALLBACK_HEURISTICS: dict[tuple[str, str], Any] = {
    # CONTENT
    ("CONTENT", "format"): _fallback_content_format,
    ("CONTENT", "schedule"): _fallback_content_schedule,
    ("CONTENT", "track"): _fallback_track_results,
    # APP
    ("APP", "spec"): _fallback_app_spec,
    ("APP", "aso"): _fallback_app_aso,
    # LOCAL_BIZ
    ("LOCAL_BIZ", "grade"): _fallback_grade_sites,
    ("LOCAL_BIZ", "track"): _fallback_track_results,
    # MONETIZE
    ("MONETIZE", "build_page"): _fallback_build_page,
    # PRODUCT
    ("PRODUCT", "track"): _fallback_track_results,
    # RESEARCH
    ("RESEARCH", "score"): _fallback_research_score,
    # SCRAPING
    ("SCRAPING", "configure"): _fallback_scraping_configure,
    ("SCRAPING", "clean"): _fallback_scraping_clean,
    ("SCRAPING", "store"): _fallback_scraping_store,
    # OUTBOUND
    ("OUTBOUND", "followup"): _fallback_track_results,
    # BROKERING
    ("BROKERING", "connect_parties"): _fallback_track_results,
    ("BROKERING", "track_revenue"): _fallback_track_results,
}


VENTURE_TYPES = {
    "OUTBOUND": {
        "description": "Cold outreach ventures — email, DM, LinkedIn, etc.",
        "pipeline": ["prospect", "qualify", "build_asset", "outreach", "followup", "track"],
        "interval_hours": 4,
        "model": MODEL_SONNET,  # outreach templates + prospecting
        "scripts": {
            "prospect": ("printmaxx_agent.py", "--mission outreach-prospect"),
            "qualify": ("printmaxx_agent.py", "--mission outreach-qualify"),
            "build_asset": ("printmaxx_agent.py", "--mission outreach-asset"),
            "outreach": ("printmaxx_agent.py", "--mission outreach-send"),
            "followup": ("printmaxx_agent.py", "--mission outreach-send"),
            "track": ("printmaxx_agent.py", "--mission outreach-track"),
        },
        "claude_prompt": (
            "You are the OUTBOUND autonomy agent for PRINTMAXX venture '{name}'.\n"
            "Working directory: {project}\n\n"
            "Your job runs every {interval}h. Each cycle:\n"
            "1. PROSPECT: Find 20+ new prospects matching the venture's ICP. "
            "Use web search, directory scraping, LinkedIn-style lookups. "
            "Save to AUTOMATIONS/leads/{venture_id}/prospects.csv\n"
            "2. QUALIFY: Score each prospect 1-10 on fit, budget signals, urgency. "
            "Move 8+ scores to qualified.csv\n"
            "3. BUILD ASSET: For each qualified prospect, generate a personalized "
            "cold email or DM using the 6-question framework. Save drafts.\n"
            "4. OUTREACH: Queue the top 10 emails/DMs for sending. "
            "Log to outreach_log.csv\n"
            "5. TRACK: Check previous outreach for replies. Update status.\n\n"
            "Rules:\n"
            "- All files stay in {project}\n"
            "- Log everything to AUTOMATIONS/logs/venture_{venture_id}.log\n"
            "- Use real data, not placeholders\n"
            "- If a step fails, skip to next step, don't stop the cycle"
        ),
    },

    "CONTENT": {
        "description": "Content creation ventures — social, blog, video scripts, newsletters.",
        "pipeline": ["find_topics", "generate", "format", "schedule", "distribute", "track"],
        "interval_hours": 6,
        "model": MODEL_SONNET,  # content gen + scheduling
        "scripts": {
            "find_topics": ("printmaxx_agent.py", "--mission content-topics"),
            "generate": ("printmaxx_agent.py", "--mission content"),
            "format": ("content_repurposer.py", ""),
            "schedule": ("clip_post_scheduler.py", "--input CONTENT/social/posting_queue --days 7"),
            "distribute": ("printmaxx_agent.py", "--mission content-distribute"),
            "track": ("printmaxx_agent.py", "--mission content-track"),
        },
        "demographic_variants": {
            "boomer_male_55_70": {
                "platforms": ["YouTube", "Facebook", "Email Newsletter"],
                "content_style": "calm, authoritative, educational. no zoomer energy. trustworthy voice. "
                    "10-20 min longform. specific verticals: golf, fishing, health/wellness, tools/DIY, "
                    "retirement planning, classic cars, woodworking.",
                "format": "longer paragraphs, no slang, clear structure. educational not entertaining. "
                    "problem-solution framing. credibility signals (years of experience, data, studies).",
                "cta_style": "direct, low-pressure. 'learn more' not 'smash subscribe'. email capture over social follows.",
                "product_categories": "health supplements ($30-80), pain relief, sleep aids, golf gear, "
                    "fishing equipment, workshop tools, financial planning guides.",
            },
        },
        "claude_prompt": (
            "You are the CONTENT autonomy agent for PRINTMAXX venture '{name}'.\n"
            "Working directory: {project}\n\n"
            "Your job runs every {interval}h. Each cycle:\n"
            "1. FIND TOPICS: Scan trending topics in the venture's niche. "
            "Check LEDGER/ALPHA_STAGING.csv for recent alpha. "
            "Check CONTENT/social/ for what's already been posted.\n"
            "2. GENERATE: Create 5 social posts (X/Twitter format), "
            "1 thread (5-7 tweets), 1 newsletter draft. "
            "Follow .claude/rules/copy-style.md voice guidelines.\n"
            "   BOOMER VARIANT: Also generate 2 Facebook posts + 1 YouTube longform script "
            "targeting males 55-70. Calm, authoritative tone. Health/golf/fishing/tools verticals. "
            "Save to CONTENT/social/boomer/.\n"
            "3. FORMAT: Adapt content for each platform "
            "(X, LinkedIn, newsletter, blog, Facebook Groups for 55+ demo).\n"
            "4. SCHEDULE: Save all content to CONTENT/social/generated/ "
            "as PENDING_REVIEW with timestamps.\n"
            "5. DISTRIBUTE: Move APPROVED content to posting queue.\n"
            "6. TRACK: Check engagement on previously posted content.\n\n"
            "Rules:\n"
            "- NEVER use AI slop vocabulary (see .claude/rules/copy-style.md)\n"
            "- Consequence-first hooks, specific numbers, lowercase energy\n"
            "- Boomer content: NO zoomer energy. Educational, trustworthy, calm authority.\n"
            "- All files stay in {project}"
        ),
    },

    "APP": {
        "description": "App factory ventures — PWAs, tools, micro-SaaS.",
        "pipeline": ["find_gap", "spec", "build", "deploy", "aso", "track"],
        "interval_hours": 12,
        "model": MODEL_SONNET,  # code generation — Sonnet handles well
        "scripts": {
            "find_gap": ("app_factory_autopilot.py", "--run --bookmarks-limit 60 --accounts-limit 12 --approval-max 80 --processor-batch 120 --queue-limit 40"),
            "spec": ("app_factory_command_center.py", "--refresh --top 8"),
            "build": ("printmaxx_agent.py", "--mission apps"),
            "deploy": ("printmaxx_agent.py", "--mission apps-deploy"),
            "aso": ("aso_keyword_research.py", ""),
            "track": ("printmaxx_agent.py", "--mission apps-track"),
        },
        "claude_prompt": (
            "You are the APP FACTORY autonomy agent for PRINTMAXX venture '{name}'.\n"
            "Working directory: {project}\n\n"
            "Your job runs every {interval}h. Each cycle:\n"
            "1. FIND GAP: Run "
            "python3 AUTOMATIONS/app_factory_autopilot.py --run "
            "to ingest bookmarks, scrape app alpha, auto-approve low-risk items, route them, generate specs, and rebuild the ranked queue. "
            "Use AUTOMATIONS/agent/autonomy/app_factory_priority_queue.json as the source of truth.\n"
            "2. SPEC: Pick the highest-scoring non-blocked item. "
            "If it maps to an existing app, spec an upgrade before greenfield work. "
            "Write or refine the app spec in AUTOMATIONS/auto_ops/app_specs/.\n"
            "3. BUILD: Build the narrowest version that creates a real first win fast. "
            "Use MONEY_METHODS/APP_FACTORY/ONBOARDING_PLAYBOOK.md and "
            "MONEY_METHODS/APP_FACTORY/APP_DISCOVERY_ENGINE.md.\n"
            "4. DEPLOY: Ship a testable build, then prepare the native-quality path. "
            "Do not confuse a quick PWA deploy with App Store readiness.\n"
            "5. ASO: Generate keywords, screenshots spec, review-prompt timing, "
            "and pricing tests for the exact niche.\n"
            "6. TRACK: Log what changed, what converted, and whether the next move is "
            "iterate-existing, build-new, or park.\n\n"
            "Rules:\n"
            "- Apps must match top 10 in category quality\n"
            "- Read OPS/APP_FACTORY_ALPHA_COMMAND_CENTER.md before spec or build work\n"
            "- No fake paywalls, no single-file HTML monoliths as the end state, no generic app ideas\n"
            "- Default to value-first onboarding, lower-priced annual-first tests, and post-value review prompts\n"
            "- Affiliate links are secondary. Retention and billing come first.\n"
            "- All files stay in {project}\n"
            "- Include monetization config, privacy policy, content"
        ),
    },

    "LOCAL_BIZ": {
        "description": "Local business outreach — find businesses, build sites, pitch.",
        "pipeline": ["discover", "grade", "build_preview", "deploy", "outreach", "track"],
        "interval_hours": 4,
        "model": MODEL_SONNET,  # local biz prospecting + site builds
        "scripts": {
            "discover": ("openclaw_local_biz.py", '--discover "{city}" {niche}'),
            "grade": ("playwright_site_tester.py", "--quick"),
            "build_preview": ("openclaw_local_biz.py", "--build"),
            "deploy": ("openclaw_local_biz.py", "--build"),
            "outreach": ("openclaw_local_biz.py", "--outreach"),
            "track": ("printmaxx_agent.py", "--mission health"),
        },
        "claude_prompt": (
            "You are the LOCAL BIZ autonomy agent for PRINTMAXX venture '{name}'.\n"
            "Working directory: {project}\n\n"
            "Your job runs every {interval}h. Each cycle:\n"
            "1. DISCOVER: Search for local businesses in rotating cities "
            "that have no website or terrible websites. "
            "Use DuckDuckGo search, Yelp scraping, Google Maps data.\n"
            "2. GRADE: Score each business website A-F based on "
            "mobile responsiveness, SSL, load time, design quality.\n"
            "3. BUILD PREVIEW: For F and D grade businesses, "
            "auto-generate a modern preview website.\n"
            "4. DEPLOY: Deploy preview to surge.sh with unique URL.\n"
            "5. OUTREACH: Generate cold email with preview link. "
            "Queue for sending.\n"
            "6. TRACK: Check outreach responses, follow up on warm leads.\n\n"
            "City rotation: cycle through US cities automatically.\n"
            "Can also target international markets.\n"
            "Rules: All files stay in {project}"
        ),
    },

    "RESEARCH": {
        "description": "Research & alpha — scrape, analyze, score, route to actions.",
        "pipeline": ["scrape", "analyze", "score", "route", "compound"],
        "interval_hours": 2,
        "model": MODEL_HAIKU,  # scraping + data processing
        "scripts": {
            "scrape": ("twitter_alpha_scraper.py", "--all"),
            "analyze": ("alpha_auto_processor.py", "--process-new"),
            "score": ("capital_genesis_ranker.py", "--rank"),
            "route": ("decision_engine.py", "--cycle"),
            "compound": ("engagement_bait_converter.py", "--limit 5"),
        },
        "claude_prompt": (
            "You are the RESEARCH autonomy agent for PRINTMAXX venture '{name}'.\n"
            "Working directory: {project}\n\n"
            "Your job runs every {interval}h. Each cycle:\n"
            "1. SCRAPE: Run twitter_alpha_scraper.py --all and "
            "background_reddit_scraper.py --scrape. "
            "Also check HackerNews, ProductHunt, IndieHackers.\n"
            "2. ANALYZE: Process raw scrapes through alpha_auto_processor.py. "
            "Score each finding on actionability, ROI, effort.\n"
            "3. SCORE: Rate findings HIGHEST/HIGH/MEDIUM/LOW. "
            "Apply bot detection and earnings skepticism (see alpha-review.md).\n"
            "4. ROUTE: Send APPROVED findings to correct target files "
            "(see LEDGER/ structure). Run decision_engine.py --cycle.\n"
            "5. COMPOUND: Take top findings and generate content from them. "
            "Every research finding = 3 tweets + 1 thread minimum.\n\n"
            "Rules: All files stay in {project}. Follow alpha-review.md guidelines."
        ),
    },

    "MONETIZE": {
        "description": "Monetization ventures — affiliate, digital products, funnels.",
        "pipeline": ["find_offers", "create_funnel", "build_page", "deploy", "distribute", "track"],
        "interval_hours": 8,
        "model": MODEL_SONNET,  # funnel builds + offer evaluation
        "scripts": {
            "find_offers": ("printmaxx_agent.py", "--mission monetize-research"),
            "create_funnel": ("printmaxx_agent.py", "--mission monetize"),
            "build_page": ("printmaxx_agent.py", "--mission factory"),
            "deploy": ("printmaxx_agent.py", "--mission monetize-deploy"),
            "distribute": ("content_repurposer.py", ""),
            "track": ("printmaxx_agent.py", "--mission monetize-track"),
        },
        "demographic_variants": {
            "boomer_male_55_70": {
                "affiliate_categories": "health supplements (joint support, sleep aids, prostate health $30-80), "
                    "pain relief devices, golf accessories ($40-120), fishing gear ($30-100), "
                    "workshop/power tools, financial planning services, Medicare supplement info.",
                "funnel_style": "longer-form landing pages. testimonials from age-appropriate people. "
                    "larger fonts, clear layouts, phone number visible. trust signals: BBB, guarantees, "
                    "free shipping. email-first not social-first.",
                "platforms": "Facebook Ads targeting 55-70 male, YouTube pre-roll on golf/fishing/DIY channels, "
                    "email newsletters (high open rates in this demo), Google Search (health keywords).",
            },
        },
        "claude_prompt": (
            "You are the MONETIZATION autonomy agent for PRINTMAXX venture '{name}'.\n"
            "Working directory: {project}\n\n"
            "Your job runs every {interval}h. Each cycle:\n"
            "1. FIND OFFERS: Scan affiliate networks, Gumroad trending, "
            "AppSumo deals. Find high-commission opportunities.\n"
            "   BOOMER VARIANT: Also scan ClickBank health/wellness category, "
            "Amazon Associates for golf/fishing/tools, and supplement affiliate programs. "
            "Target $30-80 price range products for males 55-70.\n"
            "2. CREATE FUNNEL: Design a conversion funnel for the top offer. "
            "Email sequence, landing page copy, social proof.\n"
            "   BOOMER VARIANT: Longer-form pages, larger fonts, trust signals, "
            "phone-friendly. Email-first distribution.\n"
            "3. BUILD PAGE: Create landing page in LANDING/ directory.\n"
            "4. DEPLOY: Deploy to surge.sh or Vercel.\n"
            "5. DISTRIBUTE: Create social posts, email blasts, "
            "community posts promoting the offer. "
            "BOOMER VARIANT: Facebook Groups for 55+ demographics, "
            "YouTube descriptions on longform content.\n"
            "6. TRACK: Check conversion rates, revenue, ROI.\n\n"
            "Rules:\n"
            "- FTC disclosure on all affiliate links\n"
            "- No fake testimonials\n"
            "- All files stay in {project}"
        ),
    },

    "PRODUCT": {
        "description": "Digital product ventures — ebooks, courses, templates, tools.",
        "pipeline": ["find_demand", "create", "listing", "launch", "distribute", "track"],
        "interval_hours": 24,
        "model": MODEL_SONNET,  # product builds + listing creation
        "scripts": {
            "find_demand": ("printmaxx_agent.py", "--mission product-research"),
            "create": ("printmaxx_agent.py", "--mission product-create"),
            "listing": ("printmaxx_agent.py", "--mission product-listing"),
            "launch": ("engagement_bait_converter.py", "--limit 5"),
            "distribute": ("printmaxx_agent.py", "--mission product-distribute"),
            "track": ("printmaxx_agent.py", "--mission health"),
        },
        "claude_prompt": (
            "You are the PRODUCT autonomy agent for PRINTMAXX venture '{name}'.\n"
            "Working directory: {project}\n\n"
            "Your job runs every {interval}h. Each cycle:\n"
            "1. FIND DEMAND: Analyze Reddit, Twitter, Gumroad trending "
            "to find what people are actively searching for.\n"
            "2. CREATE: Build the digital product (PDF, template, tool, "
            "Notion template, spreadsheet, etc.).\n"
            "3. LISTING: Create Gumroad/Lemon Squeezy listing with "
            "optimized title, description, pricing, preview images.\n"
            "4. LAUNCH: Deploy and create launch content (tweets, "
            "ProductHunt listing, Reddit posts).\n"
            "5. DISTRIBUTE: Cross-post to all channels.\n"
            "6. TRACK: Monitor sales, reviews, refund rate.\n\n"
            "Rules: All files in {project}. Quality > speed."
        ),
    },

    "SCRAPING": {
        "description": "Data scraping ventures — competitive intel, lead gen, market data.",
        "pipeline": ["configure", "scrape", "clean", "analyze", "store", "alert"],
        "interval_hours": 2,
        "model": MODEL_SONNET,  # scraping is execution, Sonnet handles it
        "scripts": {
            "configure": ("system_health_monitor.py", "--quick"),
            "scrape": ("twitter_alpha_scraper.py", "--all"),
            "clean": ("sqlite_alpha_index.py", "--rebuild"),
            "analyze": ("alpha_auto_processor.py", "--process-new"),
            "store": ("sqlite_alpha_index.py", "--rebuild"),
            "alert": ("decision_engine.py", "--cycle"),
        },
        "claude_prompt": (
            "You are the SCRAPING autonomy agent for PRINTMAXX venture '{name}'.\n"
            "Working directory: {project}\n\n"
            "Your job runs every {interval}h. Each cycle:\n"
            "1. CONFIGURE: Check scraper configs, update targets if needed.\n"
            "2. SCRAPE: Run all configured scrapers. Handle rate limits.\n"
            "3. CLEAN: Deduplicate, normalize, validate scraped data.\n"
            "4. ANALYZE: Score and categorize all new data points.\n"
            "5. STORE: Append to appropriate LEDGER/ CSV files.\n"
            "6. ALERT: Flag high-value findings for immediate action.\n\n"
            "Rules: All files in {project}. Respect rate limits. No TOS violations."
        ),
    },

    "BROKERING": {
        "description": "Connect businesses to services for referral fees. Same scraping + cold email pattern, different verticals.",
        "pipeline": ["scrape_targets", "qualify_leads", "connect_parties", "earn_fee", "track_revenue"],
        "interval_hours": 6,
        "model": MODEL_SONNET,  # prospecting + outreach execution
        "verticals": [
            "real_estate", "equipment_financing", "merchant_processing",
            "insurance", "sba_loans", "wholesale", "lead_gen_service",
            "white_label_reports",
        ],
        "scripts": {
            "scrape_targets": ("printmaxx_agent.py", "--mission brokering-scrape"),
            "qualify_leads": ("printmaxx_agent.py", "--mission brokering-qualify"),
            "connect_parties": ("printmaxx_agent.py", "--mission brokering-qualify"),
            "track_revenue": ("printmaxx_agent.py", "--mission brokering-track"),
        },
        "claude_prompt": (
            "You are the BROKERING autonomy agent for PRINTMAXX venture '{name}'.\n"
            "Working directory: {project}\n\n"
            "Reference: OPS/BROKERING_ARBITRAGE_OPPORTUNITIES.md for the full play list.\n\n"
            "Your job runs every {interval}h. Each cycle:\n"
            "1. SCRAPE TARGETS: Find businesses needing services in the active vertical. "
            "Use savvy_lead_scraper, nationwide_scraper, or SAM.gov monitor. "
            "Sources: Google Maps, LinkedIn, industry directories. "
            "Save to AUTOMATIONS/leads/{venture_id}/broker_targets.csv\n"
            "2. QUALIFY LEADS: Score each target on deal size, urgency, and fit. "
            "Enrich with Apollo/Clearbit data if available. "
            "Move qualified leads (score 7+) to qualified_broker_leads.csv\n"
            "3. CONNECT PARTIES: For qualified leads, identify the best service provider "
            "(lender, broker, vendor, agent) and draft a warm intro email for both sides. "
            "Use cold email templates from MONEY_METHODS/EAS/email_templates/ adapted for brokering.\n"
            "4. EARN FEE: Track introductions made. Follow up on connections. "
            "Send referral agreement when deal progresses. "
            "Fee structure: 1-5% of deal value or flat $50-5K per referral.\n"
            "5. TRACK REVENUE: Log all referral fees earned, pending, and pipeline. "
            "Update LEDGER/BROKERING_REVENUE.csv\n\n"
            "Verticals to rotate through: real estate referrals, equipment financing, "
            "merchant processing, insurance, SBA loans, wholesale connecting, "
            "lead gen as a service, white-label reports.\n\n"
            "Rules:\n"
            "- All files stay in {project}\n"
            "- CAN-SPAM compliant on all outreach\n"
            "- Disclose referral relationship where legally required\n"
            "- Track referral agreements in LEDGER/\n"
            "- Kill verticals with <2% conversion after 100 outreach attempts"
        ),
    },
}


# ══════════════════════════════════════════════════════════════════════════
# AUTONOMY STATE — tracks all autonomous ventures
# ══════════════════════════════════════════════════════════════════════════

class AutonomyState:
    """Persistent state for all autonomous ventures."""

    def __init__(self) -> None:
        AUTONOMY_DIR.mkdir(parents=True, exist_ok=True)
        SCHEDULES_DIR.mkdir(parents=True, exist_ok=True)
        RESULTS_DIR.mkdir(parents=True, exist_ok=True)
        self.data: dict[str, Any] = self._load()

    def _load(self) -> dict[str, Any]:
        if STATE_FILE.exists():
            try:
                with locked_file(STATE_FILE, mode="r") as f:
                    return json.load(f)
            except Exception:
                pass
        return {
            "ventures": {},
            "total_cycles": 0,
            "total_pipeline_runs": 0,
            "created_at": datetime.now().isoformat(),
        }

    def save(self) -> None:
        safe_path(STATE_FILE)
        with locked_file(STATE_FILE, mode="w") as f:
            json.dump(self.data, f, indent=2, default=str)

    def get_venture(self, venture_id: str) -> Optional[dict[str, Any]]:
        return self.data["ventures"].get(venture_id)

    def add_venture(self, venture_id: str, venture_def: dict[str, Any]) -> None:
        self.data["ventures"][venture_id] = venture_def
        self.save()

    def update_venture(self, venture_id: str, updates: dict[str, Any]) -> None:
        if venture_id in self.data["ventures"]:
            self.data["ventures"][venture_id].update(updates)
            self.save()

    def get_active_ventures(self) -> dict[str, dict[str, Any]]:
        return {
            vid: v for vid, v in self.data["ventures"].items()
            if v.get("status") not in ("PAUSED", "KILLED")
        }


# ══════════════════════════════════════════════════════════════════════════
# VENTURE AUTONOMY ENGINE — runs the pipeline for any venture
# ══════════════════════════════════════════════════════════════════════════

class VentureAutonomyEngine:
    """Runs the full autonomy pipeline for any venture type."""

    def __init__(self, state: AutonomyState) -> None:
        self.state = state

    def create_venture(self, venture_type: str, name: str, config: Optional[dict[str, Any]] = None) -> Optional[str]:
        """Create a new autonomous venture."""
        if venture_type not in VENTURE_TYPES:
            log(f"Unknown venture type: {venture_type}. Available: {list(VENTURE_TYPES.keys())}", "ERROR")
            return None

        vtype = VENTURE_TYPES[venture_type]
        venture_id = f"auto_{venture_type.lower()}_{name.lower().replace(' ', '_')[:20]}_{int(time.time()) % 10000}"

        venture_def = {
            "id": venture_id,
            "name": name,
            "type": venture_type,
            "status": "ACTIVE",
            "pipeline": vtype["pipeline"],
            "interval_hours": vtype["interval_hours"],
            "config": config or {},
            "created_at": datetime.now().isoformat(),
            "last_run": None,
            "cycles_run": 0,
            "results": [],
            "pipeline_stats": {step: {"runs": 0, "successes": 0, "last_run": None} for step in vtype["pipeline"]},
        }

        # Create venture-specific directories
        venture_dir = AUTONOMY_DIR / venture_id
        venture_dir.mkdir(parents=True, exist_ok=True)
        (venture_dir / "data").mkdir(exist_ok=True)
        (venture_dir / "output").mkdir(exist_ok=True)
        (venture_dir / "logs").mkdir(exist_ok=True)

        # Also create leads directory if outbound/local_biz/brokering
        if venture_type in ("OUTBOUND", "LOCAL_BIZ", "BROKERING"):
            leads_dir = AUTOMATIONS / "leads" / venture_id
            leads_dir.mkdir(parents=True, exist_ok=True)

        self.state.add_venture(venture_id, venture_def)
        log(f"Created autonomous venture: {venture_id} (type={venture_type}, interval={vtype['interval_hours']}h)")

        # Generate scheduled task configs
        self._generate_schedule_configs(venture_id, venture_def)

        return venture_id

    def run_venture(self, venture_id: str) -> bool:
        """Run the full autonomy pipeline for a venture."""
        venture = self.state.get_venture(venture_id)
        if not venture:
            log(f"Venture not found: {venture_id}", "ERROR")
            return False

        if venture.get("status") in ("PAUSED", "KILLED"):
            log(f"Venture {venture_id} is {venture['status']} — skipping")
            return False

        # Check interval
        hours_since = _hours_since(venture.get("last_run"))
        interval = venture.get("interval_hours", 4)
        if hours_since < interval:
            log(f"Venture {venture_id}: {hours_since:.1f}h since last run < {interval}h interval — skipping")
            return False

        vtype_key = venture.get("type", "")
        vtype = VENTURE_TYPES.get(vtype_key)
        if not vtype:
            log(f"Unknown type {vtype_key} for venture {venture_id}", "ERROR")
            return False

        log(f"{'='*60}")
        log(f"VENTURE CYCLE: {venture['name']} ({venture_id})")
        log(f"Type: {vtype_key} | Pipeline: {' → '.join(venture['pipeline'])}")
        log(f"{'='*60}")

        # INTELLIGENCE-FIRST: Query intelligence for this venture type
        intel_brief = ""
        try:
            import subprocess as _sp
            _intel_cmd = [
                "python3", str(PROJECT / "AUTOMATIONS" / "intelligence_router.py"),
                "--venture", vtype_key, "--json"
            ]
            _intel_result = _sp.run(_intel_cmd, capture_output=True, text=True, timeout=30)
            if _intel_result.returncode == 0 and _intel_result.stdout.strip():
                intel_brief = _intel_result.stdout.strip()[:1000]
                log(f"  Intelligence loaded: {len(intel_brief)} chars for {vtype_key}")
        except Exception as _ie:
            log(f"  Intelligence query failed (non-fatal): {_ie}", "WARN")

        # SOVRUN PROCEDURAL MEMORY: Recall relevant skills
        skills_brief = _recall_venture_skills(vtype_key, venture.get("name", ""))
        if skills_brief:
            log(f"  Procedural memory: {len(skills_brief)} chars of learned skills")

        # XLSX INTELLIGENCE: Get Master Ops context for this venture
        xlsx_ctx = self._get_venture_xlsx_context(vtype_key)
        if xlsx_ctx:
            log(f"  xlsx context: {xlsx_ctx.get('total_ops', 0)} ops, "
                f"{xlsx_ctx.get('ready_count', 0)} ready, "
                f"{len(xlsx_ctx.get('synergies', []))} synergies, "
                f"{len(xlsx_ctx.get('blockers', []))} blockers")

        cycle_results = {}
        scripts = vtype.get("scripts", {})
        config = venture.get("config", {})

        for step in venture["pipeline"]:
            if _shutdown:
                log("Shutdown requested — stopping venture cycle")
                break

            log(f"  Step: {step}...")

            # 1. Check HUMAN_BLOCKED — never waste tokens on these
            blocked_key = (vtype_key, step)
            if blocked_key in HUMAN_BLOCKED_STEPS:
                reason = HUMAN_BLOCKED_STEPS[blocked_key]
                log(f"    HUMAN_BLOCKED: {step} — {reason}")
                cycle_results[step] = "human_blocked"
                self._save_step_result(venture_id, step, False,
                                       f"HUMAN_BLOCKED: {reason}")
                continue

            # 2. Check if there's a script mapping for this step
            if step in scripts:
                script_name, script_args = scripts[step]

                # Substitute config values into args
                try:
                    args = script_args.format(
                        city=config.get("city", "Austin TX"),
                        niche=config.get("niche", "dentist"),
                        venture_id=venture_id,
                        name=venture["name"],
                        **config
                    )
                except KeyError:
                    args = script_args  # use raw args if format fails

                script_path = AUTOMATIONS / script_name
                if script_path.exists():
                    ok, output = run_script(script_name, args, timeout_sec=300,
                                            label=f"{venture_id}:{step}")
                    cycle_results[step] = "ok" if ok else "failed"

                    # Save step output
                    self._save_step_result(venture_id, step, ok, output)
                else:
                    log(f"    Script not found: {script_name}", "WARN")
                    # 3a. Try heuristic fallback before LLM
                    fallback_fn = FALLBACK_HEURISTICS.get(blocked_key)
                    if fallback_fn:
                        try:
                            fb_ok, fb_detail = fallback_fn(venture_id, venture, vtype)
                            log(f"    Fallback: {fb_detail}")
                            cycle_results[step] = "ok" if fb_ok else "failed"
                            self._save_step_result(venture_id, step, fb_ok, fb_detail)
                        except Exception as fb_err:
                            log(f"    Fallback error: {fb_err}", "WARN")
                            cycle_results[step] = self._run_with_claude(
                                venture_id, venture, step, vtype)
                    else:
                        cycle_results[step] = self._run_with_claude(
                            venture_id, venture, step, vtype)
            else:
                # No script mapping — try heuristic fallback, then LLM
                fallback_fn = FALLBACK_HEURISTICS.get(blocked_key)
                if fallback_fn:
                    try:
                        fb_ok, fb_detail = fallback_fn(venture_id, venture, vtype)
                        log(f"    Fallback: {fb_detail}")
                        cycle_results[step] = "ok" if fb_ok else "failed"
                        self._save_step_result(venture_id, step, fb_ok, fb_detail)
                    except Exception as fb_err:
                        log(f"    Fallback error: {fb_err}", "WARN")
                        cycle_results[step] = self._run_with_claude(
                            venture_id, venture, step, vtype)
                else:
                    cycle_results[step] = self._run_with_claude(
                        venture_id, venture, step, vtype)

            # Update pipeline stats
            stats = venture.get("pipeline_stats", {}).get(step, {"runs": 0, "successes": 0})
            stats["runs"] = stats.get("runs", 0) + 1
            if cycle_results.get(step) == "ok":
                stats["successes"] = stats.get("successes", 0) + 1
            stats["last_run"] = datetime.now().isoformat()
            venture.setdefault("pipeline_stats", {})[step] = stats

        # Update venture state
        successes = sum(1 for v in cycle_results.values() if v == "ok")
        blocked = sum(1 for v in cycle_results.values() if v == "human_blocked")
        failed = sum(1 for v in cycle_results.values() if v == "failed")
        total = len(cycle_results)
        runnable = total - blocked  # steps that were actually attempted

        venture["last_run"] = datetime.now().isoformat()
        venture["cycles_run"] = venture.get("cycles_run", 0) + 1
        venture["results"] = venture.get("results", [])[-19:]  # keep last 20
        venture["results"].append({
            "ts": datetime.now().isoformat(),
            "steps": cycle_results,
            "success_rate": f"{successes}/{total}",
        })

        self.state.update_venture(venture_id, venture)
        self.state.data["total_cycles"] = self.state.data.get("total_cycles", 0) + 1
        self.state.data["total_pipeline_runs"] = self.state.data.get("total_pipeline_runs", 0) + total
        self.state.save()

        # Log mission to shared agent infrastructure
        mission_name = f"autonomy:{venture_id[:30]}"
        if successes == runnable and runnable > 0:
            result_str = "success"
        elif successes > 0:
            result_str = "partial"
        else:
            result_str = "failed"
        duration = sum(1 for _ in cycle_results)  # approximate
        log_mission(mission_name, result_str, duration,
                    f"{venture['name']}: {successes}/{total} OK, {blocked} blocked, {failed} failed")

        def _step_label(v: str) -> str:
            if v == "ok":
                return "OK"
            if v == "human_blocked":
                return "BLOCKED"
            return "FAIL"

        send_bus_message(
            f"Venture '{venture['name']}' cycle complete: {successes}/{total} steps. "
            f"Pipeline: {' -> '.join(f'{_step_label(v)}:{k}' for k, v in cycle_results.items())}"
        )

        blocked_note = f", {blocked} human-blocked" if blocked else ""
        log(f"Venture cycle complete: {venture['name']} — {successes}/{total} steps succeeded{blocked_note}")

        # Capture as procedural skill on success
        if successes > 0:
            steps_summary = ", ".join(f"{k}:{v}" for k, v in cycle_results.items())
            _capture_venture_skill(
                vtype_key, venture.get("name", venture_id),
                f"Pipeline: {steps_summary}. {successes}/{total} steps succeeded.",
                success=(successes == total),
            )

        return True

    def run_all_active(self) -> None:
        """Run all active ventures that are due."""
        active = self.state.get_active_ventures()
        if not active:
            log("No active autonomous ventures")
            return

        log(f"Running {len(active)} active autonomous ventures...")
        ran = 0
        for vid, venture in active.items():
            if _shutdown:
                break
            if self.run_venture(vid):
                ran += 1

        log(f"Ran {ran}/{len(active)} ventures this cycle")

    def _get_venture_xlsx_context(self, venture_type: str) -> dict:
        """Get xlsx intelligence for a specific venture's execution."""
        if not _BRIDGE_AVAILABLE:
            return {}
        try:
            bridge = MasterOpsBridge()

            # Get venture automation map entries
            vmap = bridge.get_ventures_by_lane(venture_type.lower())
            if not vmap:
                # Try category match
                ops = bridge.get_ops_by_category(venture_type)
            else:
                ops = bridge.get_ops_by_category(vmap[0].get("VENTURE_NAME", venture_type) if vmap else venture_type)

            # Get readiness info
            ready_ops = [op for op in bridge.get_ready_ops() if any(
                op.get("OP_ID") == o.get("OP_ID") for o in ops
            )]

            # Get relevant synergies
            op_ids = {o.get("OP_ID") for o in ops}
            synergies = [s for s in bridge.get_synergy_stacks()
                         if any(oid in s.get("METHODS_COMBINED", "") for oid in op_ids)]

            # Get blockers
            blockers = [b for b in bridge.get_blocker_summary()
                        if any(oid in b.get("ventures_affected", []) for oid in op_ids)]

            # Get alpha theses
            theses = bridge.get_alpha_by_lane(venture_type.lower())

            return {
                "total_ops": len(ops),
                "ready_count": len(ready_ops),
                "ready_ops": [{"id": o.get("OP_ID"), "name": o.get("OP_NAME"), "auto_score": o.get("AUTOMATION_SCORE_100")} for o in ready_ops[:5]],
                "synergies": [{"name": s.get("NAME"), "multiplier": s.get("REVENUE_MULTIPLIER")} for s in synergies[:3]],
                "blockers": [b.get("blocker") for b in blockers],
                "alpha_edges": [{"opp": t.get("OPPORTUNITY"), "duration": t.get("EDGE_DURATION")} for t in theses[:3]],
                "has_playbooks": any(bridge.get_playbook_for_op(o.get("OP_ID", "")) for o in ops[:10]),
            }
        except Exception:
            return {}

    def _get_venture_intelligence(self, venture_type: str, step: Optional[str] = None) -> str:
        """Query intelligence router for venture-specific context."""
        cmd = [sys.executable, str(AUTOMATIONS / "intelligence_router.py"),
               "--venture", venture_type, "--brief"]
        if step:
            cmd.extend(["--task", step])
        try:
            result = subprocess.run(cmd, capture_output=True, text=True,
                                    timeout=30, cwd=str(PROJECT))
            if result.returncode == 0 and result.stdout.strip():
                return sanitize_for_prompt(
                    result.stdout.strip(), field_name=f"venture_intel_{venture_type}_{step or 'general'}"
                )
        except Exception:
            pass
        return ""

    def _run_with_claude(self, venture_id: str, venture: dict[str, Any], step: str, vtype: dict[str, Any]) -> str:
        """Use Claude CLI to execute a pipeline step that has no script.

        Fixed: uses --api-key when ANTHROPIC_API_KEY is set (avoids OAuth errors).
        Falls back to heuristic checks if claude -p fails entirely.
        """
        # Get intelligence briefing for this venture + step
        intel = self._get_venture_intelligence(venture.get("type", ""), step)
        intel_block = f"\n\nINTELLIGENCE BRIEFING:\n{intel}\n\n" if intel else ""
        try:
            venture_context = vtype.get("claude_prompt", "").format(
                name=venture.get("name", venture_id),
                project=str(PROJECT),
                interval=venture.get("interval_hours", vtype.get("interval_hours", 4)),
                venture_id=venture_id,
            )
        except Exception:
            venture_context = vtype.get("claude_prompt", "")
        venture_context_block = (
            f"VENTURE OPERATING CONTEXT:\n{venture_context}\n\n" if venture_context else ""
        )

        # Build a focused prompt for this specific step
        # Resilient pipeline handling: if pipeline is a dict (corrupted), use its keys
        pipeline = venture.get('pipeline', [])
        if isinstance(pipeline, dict):
            pipeline = list(pipeline.keys())
            venture['pipeline'] = pipeline  # auto-repair
        step_num = (pipeline.index(step) + 1) if step in pipeline else "?"
        prompt = (
            f"{venture_context_block}"
            f"Execute step '{step}' for venture '{venture['name']}' "
            f"(type: {venture['type']}). "
            f"Working directory: {PROJECT}. "
            f"Venture data directory: {AUTONOMY_DIR / venture_id}/. "
            f"Save all outputs there. "
            f"This is step {step_num} of "
            f"{len(pipeline)} in the pipeline: "
            f"{' -> '.join(pipeline)}. "
            f"{intel_block}"
            f"Use the intelligence briefing above to inform your decisions. "
            f"Use the venture operating context above as standing instructions. "
            f"Do the minimum viable version of this step and save results.\n\n"
            f"AGENTIC EXECUTION:\n"
            f"Do NOT stop after one step. Keep going until the task is COMPLETE or you hit a blocker.\n"
            f"- Read state -> Plan -> Execute -> Verify -> If more work needed, CONTINUE\n"
            f"- If you find sub-tasks while working, do them now, don't defer\n"
            f"- Only stop when: (a) task fully complete, (b) human action required, (c) 15+ tool calls made (safety limit)\n"
            f"- Write completion status to AUTOMATIONS/agent/autonomy/{venture_id}/output/{step}_report.md"
        )

        model = vtype.get("model", MODEL_SONNET)

        # Build claude command — use --api-key if ANTHROPIC_API_KEY is set
        api_key = os.environ.get("ANTHROPIC_API_KEY", "")
        api_key_flag = f"--api-key {api_key} " if api_key else ""
        # Escape prompt for shell: write to temp file to avoid quoting issues
        import tempfile
        prompt_file = Path(tempfile.mktemp(suffix=".txt", prefix="venture_prompt_"))
        try:
            prompt_file.write_text(prompt)
            cmd = (
                f'unset CLAUDECODE && cat "{prompt_file}" | claude -p --dangerously-skip-permissions '
                f'{api_key_flag}'
                f'--model {model}'
            )

            import time as _time
            _start = _time.time()
            ok, output = run_cmd(cmd, timeout_sec=180, label=f"claude:{venture_id}:{step}")
        finally:
            # Clean up temp file
            try:
                prompt_file.unlink(missing_ok=True)
            except Exception:
                pass

        if ok:
            _trajectory.log_success(f"claude:{venture_id}:{step}", _start)
            return "ok"

        # Claude failed — try heuristic fallback before reporting failure
        _trajectory.log_failure(f"claude:{venture_id}:{step}", error=output[:200], start=_start)
        vtype_key = venture.get("type", "")
        fallback_fn = FALLBACK_HEURISTICS.get((vtype_key, step))
        if fallback_fn:
            try:
                fb_ok, fb_detail = fallback_fn(venture_id, venture, vtype)
                log(f"    Claude failed, fallback: {fb_detail}")
                self._save_step_result(venture_id, step, fb_ok, f"claude_failed_fallback: {fb_detail}")
                return "ok" if fb_ok else "failed"
            except Exception as fb_err:
                log(f"    Fallback also failed: {fb_err}", "WARN")

        return "failed"

    def _save_step_result(self, venture_id: str, step: str, success: bool, output: str) -> None:
        """Save step results to venture results directory."""
        result_dir = AUTONOMY_DIR / venture_id / "output"
        result_dir.mkdir(parents=True, exist_ok=True)
        result_file = result_dir / f"{step}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        try:
            safe_path(result_file)
            result_file.write_text(
                f"Step: {step}\n"
                f"Status: {'SUCCESS' if success else 'FAILED'}\n"
                f"Timestamp: {datetime.now().isoformat()}\n"
                f"{'='*60}\n"
                f"{output[-2000:]}\n"
            )
        except Exception as e:
            log(f"Failed to save step result: {e}", "WARN")

    def _generate_schedule_configs(self, venture_id: str, venture_def: dict[str, Any]) -> None:
        """Generate launchd plist and Cowork prompt for a venture."""
        vtype = VENTURE_TYPES.get(venture_def["type"], {})
        interval = venture_def.get("interval_hours", 4)

        # 1. Generate LLM-powered launchd plist (claude -p with venture prompt)
        plist_content = self._generate_llm_launchd_plist(venture_id, venture_def, vtype, interval)
        plist_path = SCHEDULES_DIR / f"com.claude.schedule.{venture_id}.plist"
        safe_path(plist_path)
        plist_path.write_text(plist_content)

        # 2. Generate script-only launchd plist (Python script, no LLM)
        plist_script = self._generate_script_launchd_plist(venture_id, venture_def, interval)
        plist_script_path = SCHEDULES_DIR / f"com.printmaxx.script.{venture_id}.plist"
        safe_path(plist_script_path)
        plist_script_path.write_text(plist_script)

        # 3. Generate Cowork scheduled task prompt
        cowork_prompt = self._generate_cowork_prompt(venture_id, venture_def, vtype)
        prompt_path = SCHEDULES_DIR / f"cowork_{venture_id}.md"
        safe_path(prompt_path)
        prompt_path.write_text(cowork_prompt)

        # 4. Generate cron entry (script-based)
        cron_entry = self._generate_cron_entry(venture_id, interval)
        cron_path = SCHEDULES_DIR / f"cron_{venture_id}.txt"
        safe_path(cron_path)
        cron_path.write_text(cron_entry)

        # 5. Generate ralph loop prompt
        ralph_prompt = self._generate_ralph_prompt(venture_id, venture_def, vtype)
        ralph_path = SCHEDULES_DIR / f"ralph_{venture_id}.md"
        safe_path(ralph_path)
        ralph_path.write_text(ralph_prompt)

        log(f"Generated schedule configs: llm-launchd + script-launchd + cowork + cron + ralph for {venture_id}")

    def _generate_llm_launchd_plist(self, venture_id: str, venture_def: dict[str, Any], vtype: dict[str, Any], interval_hours: int) -> str:
        """Generate launchd plist that runs Claude's brain (claude -p) on a schedule.

        This is the KEY differentiator — each scheduled task gets Claude's full
        intelligence planning and executing, not just a Python script.
        Uses the same format as the claude-code-scheduler plugin.
        """
        interval_seconds = interval_hours * 3600
        name = venture_def.get("name", venture_id)
        template = vtype.get("claude_prompt", "Run the venture pipeline.")
        prompt = template.format(
            name=name,
            project=str(PROJECT),
            interval=interval_hours,
            venture_id=venture_id,
        )
        # Append agentic loop directive
        prompt += (
            "\n\nAGENTIC EXECUTION:\n"
            "Do NOT stop after one step. Keep going until the task is COMPLETE or you hit a blocker.\n"
            "- Read state -> Plan -> Execute -> Verify -> If more work needed, CONTINUE\n"
            "- If you find sub-tasks while working, do them now, don't defer\n"
            "- Only stop when: (a) task fully complete, (b) human action required, (c) 15+ tool calls made (safety limit)\n"
            f"- Write completion status to AUTOMATIONS/agent/autonomy/{venture_id}/output/report_{datetime.now().strftime('%Y%m%d')}.md"
        )
        # Escape for XML/bash: replace quotes and ampersands
        prompt_escaped = (prompt
                          .replace("&", "&amp;")
                          .replace('"', '\\"')
                          .replace("'", "'\\''")
                          .replace("\n", " "))

        model = vtype.get("model", MODEL_SONNET)
        home = str(Path.home())
        log_path = f"{home}/.claude/logs/{venture_id}.log"

        # Include --api-key flag if ANTHROPIC_API_KEY is available
        api_key = os.environ.get("ANTHROPIC_API_KEY", "")
        api_key_flag = f"--api-key $ANTHROPIC_API_KEY " if api_key else ""
        # Include ANTHROPIC_API_KEY in plist env vars for scheduled runs
        api_key_plist_entry = ""
        if api_key:
            api_key_plist_entry = (
                f"        <key>ANTHROPIC_API_KEY</key>\n"
                f"        <string>{api_key}</string>"
            )

        return f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.claude.schedule.{venture_id}</string>
    <key>ProgramArguments</key>
    <array>
        <string>/bin/bash</string>
        <string>-c</string>
        <string>cd "{PROJECT}" &amp;&amp; claude -p "{prompt_escaped}" --dangerously-skip-permissions {api_key_flag}--model {model} >> "{log_path}" 2>&amp;1</string>
    </array>
    <key>EnvironmentVariables</key>
    <dict>
        <key>PATH</key>
        <string>/usr/local/bin:/usr/bin:/bin:/opt/homebrew/bin:{home}/.local/bin</string>
{api_key_plist_entry}
    </dict>
    <key>StartInterval</key>
    <integer>{interval_seconds}</integer>
    <key>StandardOutPath</key>
    <string>{log_path}</string>
    <key>StandardErrorPath</key>
    <string>{home}/.claude/logs/{venture_id}.error.log</string>
    <key>RunAtLoad</key>
    <false/>
</dict>
</plist>"""

    def _generate_script_launchd_plist(self, venture_id: str, venture_def: dict[str, Any], interval_hours: int) -> str:
        """Generate launchd plist that runs the Python script (no LLM, lighter weight)."""
        interval_seconds = interval_hours * 3600
        return f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.printmaxx.script.{venture_id}</string>
    <key>ProgramArguments</key>
    <array>
        <string>/bin/bash</string>
        <string>-c</string>
        <string>cd "{PROJECT}" &amp;&amp; {PYTHON} {AUTOMATIONS / 'venture_autonomy.py'} --run {venture_id} >> "{AUTOMATIONS / 'logs' / f'{venture_id}.log'}" 2>&amp;1</string>
    </array>
    <key>EnvironmentVariables</key>
    <dict>
        <key>PATH</key>
        <string>/usr/local/bin:/usr/bin:/bin:/opt/homebrew/bin</string>
    </dict>
    <key>StartInterval</key>
    <integer>{interval_seconds}</integer>
    <key>StandardOutPath</key>
    <string>{AUTOMATIONS / 'logs' / f'{venture_id}.log'}</string>
    <key>StandardErrorPath</key>
    <string>{AUTOMATIONS / 'logs' / f'{venture_id}_err.log'}</string>
    <key>RunAtLoad</key>
    <false/>
</dict>
</plist>"""

    def _generate_cowork_prompt(self, venture_id: str, venture_def: dict[str, Any], vtype: dict[str, Any]) -> str:
        """Generate a Cowork scheduled task prompt."""
        name = venture_def.get("name", venture_id)
        interval = venture_def.get("interval_hours", 4)
        template = vtype.get("claude_prompt", "Run the venture pipeline.")

        prompt = template.format(
            name=name,
            project=str(PROJECT),
            interval=interval,
            venture_id=venture_id,
        )

        return f"""# Cowork Scheduled Task: {name}

## Setup
1. Open Claude Desktop > Cowork
2. Click "Scheduled" in left sidebar > "+ New task"
3. Name: {name}
4. Frequency: Every {interval} hours
5. Working folder: {PROJECT}
6. Paste the prompt below

## Prompt

{prompt}

## Notes
- This runs with Claude's full intelligence (not just scripts)
- Requires Claude Desktop to be open
- For 24/7 execution, use the launchd plist or cron entry instead
- Generated by venture_autonomy.py on {datetime.now().strftime('%Y-%m-%d')}
"""

    def _generate_cron_entry(self, venture_id: str, interval_hours: int) -> str:
        """Generate a cron entry for this venture."""
        # Convert interval to cron schedule
        if interval_hours <= 1:
            schedule = "0 * * * *"  # every hour
        elif interval_hours <= 2:
            schedule = "0 */2 * * *"  # every 2 hours
        elif interval_hours <= 4:
            schedule = "0 */4 * * *"  # every 4 hours
        elif interval_hours <= 6:
            schedule = "0 */6 * * *"  # every 6 hours
        elif interval_hours <= 8:
            schedule = "0 */8 * * *"  # every 8 hours
        elif interval_hours <= 12:
            schedule = "0 */12 * * *"  # every 12 hours
        else:
            schedule = "0 9 * * *"  # daily at 9am

        cmd = f"cd {PROJECT} && {PYTHON} {AUTOMATIONS / 'venture_autonomy.py'} --run {venture_id}"
        log_path = AUTOMATIONS / "logs" / f"{venture_id}_cron.log"

        return f"""# PRINTMAXX Autonomous Venture: {venture_id}
# Generated by venture_autonomy.py
# Install: crontab -l | cat - this_file | crontab -
{schedule} {cmd} >> {log_path} 2>&1
"""

    def _generate_ralph_prompt(self, venture_id: str, venture_def: dict[str, Any], vtype: dict[str, Any]) -> str:
        """Generate a ralph loop PROMPT.md for this venture."""
        name = venture_def.get("name", venture_id)
        pipeline = venture_def.get("pipeline", [])
        interval = venture_def.get("interval_hours", 4)
        extra = ""
        if venture_def.get("type") == "APP":
            extra = (
                "\nBefore choosing the next step:\n"
                "1. Run `python3 AUTOMATIONS/app_factory_autopilot.py --run`\n"
                "2. Read `OPS/APP_FACTORY_ALPHA_COMMAND_CENTER.md`\n"
                "3. Use `AUTOMATIONS/agent/autonomy/app_factory_priority_queue.json` as the ranking source of truth\n"
                "4. If the top item maps to an existing app, iterate that app before greenfield work\n"
                "5. Enforce hard gates: real billing path, native-feeling UX, privacy URL, post-value review prompt timing\n"
            )

        return f"""# Ralph Loop: {name} ({venture_id})

Read state from AUTOMATIONS/agent/autonomy/{venture_id}/
Execute the next step in the pipeline: {' → '.join(pipeline)}

Check which step was last completed (read output/ directory).
Execute the NEXT step. If all steps done, start over from step 1.

After completing the step:
1. Save output to AUTOMATIONS/agent/autonomy/{venture_id}/output/
2. Update state in AUTOMATIONS/agent/autonomy/autonomy_state.json
3. Log to AUTOMATIONS/logs/venture_{venture_id}.log
4. Exit cleanly so the next loop iteration gets fresh context
{extra}

Type: {venture_def.get('type', 'UNKNOWN')}
Interval: {interval}h
Working dir: {PROJECT}
"""

    def import_from_ceo_ventures(self) -> int:
        """Import existing CEO-created ventures into the autonomy engine."""
        if not VENTURES_DIR.exists():
            log("No CEO ventures directory found")
            return 0

        imported = 0
        for vf in sorted(VENTURES_DIR.glob("venture_*.json")):
            try:
                vdef = json.loads(vf.read_text())
                op_id = vdef.get("op_id", "")
                name = vdef.get("name", "")
                category = str(vdef.get("category", "")).upper()
                lane = str(vdef.get("lane", "")).upper()
                status = vdef.get("status", "CREATED")

                if status in ("KILLED", "PAUSED"):
                    continue

                # Map category/lane to venture type
                type_map = {
                    "CONTENT": "CONTENT",
                    "OUTBOUND": "OUTBOUND",
                    "APP_FACTORY": "APP",
                    "SCRAPING": "SCRAPING",
                    "MONETIZATION": "MONETIZE",
                    "SEO": "CONTENT",
                    "SOCIAL": "CONTENT",
                    "RESEARCH": "RESEARCH",
                }
                venture_type = type_map.get(category, type_map.get(lane, "RESEARCH"))

                venture_id = f"ceo_{op_id.lower()}"
                if venture_id in self.state.data["ventures"]:
                    continue  # already imported

                self.create_venture(venture_type, name, config={"op_id": op_id, "source": "ceo_agent"})
                imported += 1
            except Exception as e:
                log(f"Failed to import {vf.name}: {e}", "WARN")

        log(f"Imported {imported} ventures from CEO agent")
        return imported


# ══════════════════════════════════════════════════════════════════════════
# SCHEDULER MANAGER — install/manage launchd + cron
# ══════════════════════════════════════════════════════════════════════════

class SchedulerManager:
    """Manages launchd and cron installations for ventures."""

    @staticmethod
    def install_launchd(venture_id: str, mode: str = "llm") -> bool:
        """Install a launchd plist for a venture (macOS only).

        mode='llm' — Claude's brain runs on schedule (claude -p)
        mode='script' — Python script runs on schedule (lighter weight)
        """
        if mode == "llm":
            plist_src = SCHEDULES_DIR / f"com.claude.schedule.{venture_id}.plist"
            plist_name = f"com.claude.schedule.{venture_id}.plist"
        else:
            plist_src = SCHEDULES_DIR / f"com.printmaxx.script.{venture_id}.plist"
            plist_name = f"com.printmaxx.script.{venture_id}.plist"

        if not plist_src.exists():
            log(f"No plist found: {plist_src}", "ERROR")
            return False

        la_dir = Path.home() / "Library" / "LaunchAgents"
        la_dir.mkdir(parents=True, exist_ok=True)
        plist_dst = la_dir / plist_name

        try:
            import shutil

            # Unload if already exists
            if plist_dst.exists():
                subprocess.run(
                    ["launchctl", "unload", str(plist_dst)],
                    capture_output=True, timeout=10
                )

            shutil.copy2(str(plist_src), str(plist_dst))

            # Create log directory
            log_dir = Path.home() / ".claude" / "logs"
            log_dir.mkdir(parents=True, exist_ok=True)

            # Load it
            result = subprocess.run(
                ["launchctl", "load", str(plist_dst)],
                capture_output=True, text=True, timeout=10
            )
            if result.returncode == 0:
                log(f"Installed launchd ({mode}): {venture_id}")
                return True
            else:
                log(f"launchctl load failed: {result.stderr}", "WARN")
                return False
        except Exception as e:
            log(f"Failed to install launchd: {e}", "ERROR")
            return False

    @staticmethod
    def uninstall_launchd(venture_id: str) -> bool:
        """Uninstall all launchd plists for a venture."""
        la_dir = Path.home() / "Library" / "LaunchAgents"
        removed = 0
        for prefix in ["com.claude.schedule.", "com.printmaxx.script.", "com.printmaxx."]:
            plist_path = la_dir / f"{prefix}{venture_id}.plist"
            if plist_path.exists():
                try:
                    subprocess.run(
                        ["launchctl", "unload", str(plist_path)],
                        capture_output=True, timeout=10
                    )
                    plist_path.unlink()
                    removed += 1
                except Exception as e:
                    log(f"Failed to uninstall {plist_path.name}: {e}", "WARN")
        if removed:
            log(f"Uninstalled {removed} launchd agent(s) for {venture_id}")
        return removed > 0

    @staticmethod
    def install_all_llm() -> int:
        """Install LLM-powered launchd agents for ALL active ventures."""
        state = AutonomyState()
        active = state.get_active_ventures()
        installed = 0
        for vid in active:
            if SchedulerManager.install_launchd(vid, mode="llm"):
                installed += 1
        log(f"Installed {installed}/{len(active)} LLM launchd agents")
        send_bus_message(f"Installed {installed} LLM-powered scheduled tasks via launchd")
        return installed

    @staticmethod
    def install_cron(venture_id: str) -> bool:
        """Add cron entry for a venture."""
        cron_src = SCHEDULES_DIR / f"cron_{venture_id}.txt"
        if not cron_src.exists():
            log(f"No cron config found for {venture_id}", "ERROR")
            return False

        new_entry = ""
        for line in cron_src.read_text().split("\n"):
            line = line.strip()
            if line and not line.startswith("#"):
                new_entry = line
                break

        if not new_entry:
            log("No valid cron entry found", "ERROR")
            return False

        try:
            # Get current crontab
            result = subprocess.run(["crontab", "-l"], capture_output=True, text=True, timeout=10)
            current = result.stdout if result.returncode == 0 else ""

            # Check if already installed
            if venture_id in current:
                log(f"Cron already installed for {venture_id}")
                return True

            # Append
            new_crontab = current.rstrip() + f"\n# PRINTMAXX: {venture_id}\n{new_entry}\n"
            proc = subprocess.run(
                ["crontab", "-"], input=new_crontab,
                capture_output=True, text=True, timeout=10
            )
            if proc.returncode == 0:
                log(f"Installed cron for {venture_id}")
                return True
            else:
                log(f"Cron install failed: {proc.stderr}", "WARN")
                return False
        except Exception as e:
            log(f"Failed to install cron: {e}", "ERROR")
            return False

    @staticmethod
    def list_installed() -> dict[str, list[str]]:
        """List all installed PRINTMAXX scheduled tasks."""
        installed = {"launchd_llm": [], "launchd_script": [], "cron": []}

        # Check launchd
        la_dir = Path.home() / "Library" / "LaunchAgents"
        if la_dir.exists():
            for plist in la_dir.glob("com.claude.schedule.*.plist"):
                installed["launchd_llm"].append(plist.stem.replace("com.claude.schedule.", ""))
            for plist in la_dir.glob("com.printmaxx.script.*.plist"):
                installed["launchd_script"].append(plist.stem.replace("com.printmaxx.script.", ""))
            for plist in la_dir.glob("com.printmaxx.auto_*.plist"):
                vid = plist.stem.replace("com.printmaxx.", "")
                if vid not in installed["launchd_script"]:
                    installed["launchd_script"].append(vid)

        # Check cron
        try:
            result = subprocess.run(["crontab", "-l"], capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                for line in result.stdout.split("\n"):
                    if "PRINTMAXX" in line and "venture_autonomy" in line:
                        # Extract venture ID from the line
                        parts = line.split("--run")
                        if len(parts) > 1:
                            vid = parts[1].strip().split()[0] if parts[1].strip() else ""
                            if vid:
                                installed["cron"].append(vid)
        except Exception:
            pass

        return installed


# ══════════════════════════════════════════════════════════════════════════
# SELF-MANAGING AUTONOMY — creates, fixes, evolves schedules on its own
# ══════════════════════════════════════════════════════════════════════════

class SelfManager:
    """The meta-agent that manages the autonomy system itself.

    Capabilities:
    - Detect ventures with no active schedule and auto-install them
    - Detect failing ventures and restart/fix their schedules
    - Create new ventures when CEO agent discovers opportunities
    - Kill underperforming ventures (score < threshold)
    - Adjust intervals based on performance (fast for winners, slow for losers)
    - Ensure all schedules are running and healthy
    """

    def __init__(self, state: AutonomyState, engine: VentureAutonomyEngine) -> None:
        self.state = state
        self.engine = engine

    def run_self_management_cycle(self) -> list[str]:
        """Full self-management cycle — call this from CEO agent or cron."""
        log("=" * 60)
        log("SELF-MANAGEMENT CYCLE")
        log("=" * 60)

        actions = []
        actions += self._ensure_all_scheduled()
        actions += self._fix_broken_schedules()
        actions += self._adjust_intervals()
        actions += self._create_from_opportunities()
        actions += self._prune_dead_ventures()

        if actions:
            log(f"Self-management: {len(actions)} actions taken")
            send_bus_message(f"Self-management: {', '.join(actions[:5])}")
        else:
            log("Self-management: all systems nominal")

        return actions

    def _ensure_all_scheduled(self) -> list[str]:
        """Auto-install launchd for any active venture missing a schedule."""
        actions = []
        installed = SchedulerManager.list_installed()
        all_installed = set(installed["launchd_llm"] + installed["launchd_script"] + installed["cron"])

        for vid, venture in self.state.get_active_ventures().items():
            if vid not in all_installed:
                log(f"  Auto-installing LLM schedule for unscheduled venture: {vid}")
                if SchedulerManager.install_launchd(vid, mode="llm"):
                    actions.append(f"installed:{vid}")
                else:
                    # Fallback to script mode
                    log(f"  LLM install failed, trying script mode for {vid}")
                    if SchedulerManager.install_launchd(vid, mode="script"):
                        actions.append(f"installed-script:{vid}")

        return actions

    def _fix_broken_schedules(self) -> list[str]:
        """Detect and fix broken scheduled tasks."""
        actions = []
        la_dir = Path.home() / "Library" / "LaunchAgents"

        for vid, venture in self.state.get_active_ventures().items():
            # Check if venture has been running (has results)
            last_run = venture.get("last_run")
            if not last_run:
                continue  # never ran, might just be new

            hours_since = _hours_since(last_run)
            expected_interval = venture.get("interval_hours", 4)

            # If it hasn't run in 3x the expected interval, something is broken
            if hours_since > expected_interval * 3:
                log(f"  Venture {vid} overdue: {hours_since:.1f}h since last run "
                    f"(expected every {expected_interval}h)", "WARN")

                # Try to reinstall the schedule
                SchedulerManager.uninstall_launchd(vid)
                self.engine._generate_schedule_configs(vid, venture)
                if SchedulerManager.install_launchd(vid, mode="llm"):
                    actions.append(f"fixed:{vid}")
                    log(f"  Reinstalled schedule for {vid}")

            # Check last cycle results for failures
            results = venture.get("results", [])
            if len(results) >= 3:
                recent_3 = results[-3:]
                all_failed = all(
                    all(v != "ok" for v in r.get("steps", {}).values())
                    for r in recent_3
                )
                if all_failed:
                    log(f"  Venture {vid} has 3 consecutive full failures", "WARN")
                    # Regenerate configs (prompt might need updating)
                    self.engine._generate_schedule_configs(vid, venture)
                    actions.append(f"regen-config:{vid}")

        return actions

    def _adjust_intervals(self) -> list[str]:
        """Speed up winners, slow down losers."""
        actions = []

        for vid, venture in self.state.get_active_ventures().items():
            results = venture.get("results", [])
            if len(results) < 5:
                continue  # not enough data

            recent_5 = results[-5:]
            success_rates = []
            for r in recent_5:
                steps = r.get("steps", {})
                if steps:
                    ok_count = sum(1 for v in steps.values() if v == "ok")
                    success_rates.append(ok_count / len(steps))

            if not success_rates:
                continue

            avg_success = sum(success_rates) / len(success_rates)
            current_interval = venture.get("interval_hours", 4)
            venture_type = venture.get("type", "")

            # xlsx-aware adjustment factors
            boost_factor = 1.0
            slow_factor = 1.0
            if _BRIDGE_AVAILABLE:
                try:
                    xlsx_ctx = self.engine._get_venture_xlsx_context(venture_type)
                    # If venture has READY ops with high automation scores, speed up
                    if xlsx_ctx.get("ready_count", 0) > 3:
                        boost_factor = 1.2
                    # If all ops are blocked, slow down
                    if xlsx_ctx.get("ready_count", 0) == 0 and xlsx_ctx.get("blockers"):
                        slow_factor = 0.5  # Run less often if everything's blocked
                except Exception:
                    pass

            # Winners: if >80% success, halve the interval (min 1h)
            if avg_success > 0.8 and current_interval > 1:
                new_interval = max(1, int(current_interval // 2 / boost_factor))
                new_interval = max(1, new_interval)
                venture["interval_hours"] = new_interval
                self.state.update_venture(vid, venture)
                self.engine._generate_schedule_configs(vid, venture)
                SchedulerManager.install_launchd(vid, mode="llm")
                actions.append(f"speedup:{vid}:{current_interval}h→{new_interval}h")
                log(f"  Speeding up {vid}: {current_interval}h → {new_interval}h (avg success {avg_success:.0%})")

            # Losers: if <20% success, double the interval (max 48h)
            elif avg_success < 0.2 and current_interval < 48:
                new_interval = min(48, int(current_interval * 2 / slow_factor))
                venture["interval_hours"] = new_interval
                self.state.update_venture(vid, venture)
                self.engine._generate_schedule_configs(vid, venture)
                SchedulerManager.install_launchd(vid, mode="llm")
                actions.append(f"slowdown:{vid}:{current_interval}h→{new_interval}h")
                log(f"  Slowing down {vid}: {current_interval}h → {new_interval}h (avg success {avg_success:.0%})")

        return actions

    def _create_from_opportunities(self) -> list[str]:
        """Check CEO agent discoveries and alpha staging for new venture opportunities."""
        actions = []

        # Check CEO discoveries directory
        discover_dir = PROJECT / "AUTOMATIONS" / "agent" / "ceo_agent" / "discoveries"
        if discover_dir.exists():
            for f in sorted(discover_dir.glob("discover_*.md")):
                # Check if already imported
                op_id = f.stem.split("_")[1] if "_" in f.stem else ""
                existing = [v for v in self.state.data["ventures"].values()
                            if v.get("config", {}).get("op_id") == op_id]
                if existing:
                    continue

                # Read the discovery and create a venture
                try:
                    content = f.read_text()
                    # Try to determine the type from the content
                    content_lower = content.lower()
                    if any(w in content_lower for w in ["outreach", "cold email", "dm", "prospecting"]):
                        vtype = "OUTBOUND"
                    elif any(w in content_lower for w in ["content", "social", "post", "tweet", "video"]):
                        vtype = "CONTENT"
                    elif any(w in content_lower for w in ["app", "saas", "tool", "pwa"]):
                        vtype = "APP"
                    elif any(w in content_lower for w in ["local", "business", "website", "redesign"]):
                        vtype = "LOCAL_BIZ"
                    elif any(w in content_lower for w in ["product", "ebook", "template", "course"]):
                        vtype = "PRODUCT"
                    elif any(w in content_lower for w in ["affiliate", "funnel", "monetiz"]):
                        vtype = "MONETIZE"
                    else:
                        vtype = "RESEARCH"

                    # Extract name from first heading
                    name = "Discovery " + op_id
                    for line in content.split("\n"):
                        if line.startswith("# "):
                            name = line.replace("# ", "").replace("DISCOVERED: ", "")[:40]
                            break

                    vid = self.engine.create_venture(vtype, name, config={"op_id": op_id, "source": "ceo_discovery"})
                    if vid:
                        SchedulerManager.install_launchd(vid, mode="llm")
                        actions.append(f"created-from-discovery:{vid}")
                except Exception as e:
                    log(f"  Failed to create venture from {f.name}: {e}", "WARN")

        return actions

    def _prune_dead_ventures(self) -> list[str]:
        """Pause ventures that have been consistently failing for 10+ cycles."""
        actions = []

        for vid, venture in list(self.state.get_active_ventures().items()):
            cycles = venture.get("cycles_run", 0)
            results = venture.get("results", [])

            if cycles < 10 or len(results) < 10:
                continue

            # Check last 10 results
            recent_10 = results[-10:]
            total_failures = 0
            for r in recent_10:
                steps = r.get("steps", {})
                if steps:
                    ok_count = sum(1 for v in steps.values() if v == "ok")
                    if ok_count == 0:
                        total_failures += 1

            # If 8+ out of 10 cycles fully failed, pause it
            if total_failures >= 8:
                venture["status"] = "PAUSED"
                venture["paused_reason"] = f"{total_failures}/10 cycles fully failed"
                venture["paused_at"] = datetime.now().isoformat()
                self.state.update_venture(vid, venture)
                SchedulerManager.uninstall_launchd(vid)
                actions.append(f"paused:{vid}")
                log(f"  Paused {vid}: {total_failures}/10 cycles failed")

        return actions


# ══════════════════════════════════════════════════════════════════════════
# STATUS DISPLAY
# ══════════════════════════════════════════════════════════════════════════

def show_status() -> None:
    state = AutonomyState()
    ventures = state.data.get("ventures", {})
    installed = SchedulerManager.list_installed()

    print("=" * 70)
    print("VENTURE AUTONOMY ENGINE — STATUS")
    print("=" * 70)
    print(f"Total ventures:     {len(ventures)}")
    print(f"Active:             {len([v for v in ventures.values() if v.get('status') == 'ACTIVE'])}")
    print(f"Total cycles:       {state.data.get('total_cycles', 0)}")
    print(f"Pipeline runs:      {state.data.get('total_pipeline_runs', 0)}")
    print(f"LLM scheduled:      {len(installed['launchd_llm'])} (claude -p via launchd)")
    print(f"Script scheduled:   {len(installed['launchd_script'])} (python via launchd)")
    print(f"Cron installed:     {len(installed['cron'])}")
    print()

    if not ventures:
        print("No autonomous ventures yet. Create one with:")
        print("  python3 venture_autonomy.py --create TYPE NAME")
        print(f"\nAvailable types: {', '.join(VENTURE_TYPES.keys())}")
        return

    print(f"{'ID':<35} {'TYPE':<10} {'NAME':<25} {'STATUS':<8} {'CYCLES':>6} {'LAST RUN':<20} {'SCHED'}")
    print("-" * 120)

    for vid, v in sorted(ventures.items()):
        vtype = v.get("type", "?")[:9]
        name = v.get("name", "?")[:24]
        status = v.get("status", "?")[:7]
        cycles = v.get("cycles_run", 0)
        last = v.get("last_run") or "never"
        if last != "never":
            last = str(last)[:19]

        sched = []
        if vid in installed["launchd_llm"]:
            sched.append("LLM")
        if vid in installed["launchd_script"]:
            sched.append("script")
        if vid in installed["cron"]:
            sched.append("cron")
        sched_str = "+".join(sched) if sched else "none"

        print(f"{vid:<35} {vtype:<10} {name:<25} {status:<8} {cycles:>6} {last:<20} {sched_str}")

    # Show pipeline stats for recent ventures
    print("\nPIPELINE HEALTH (last cycle):")
    for vid, v in sorted(ventures.items()):
        if v.get("status") != "ACTIVE":
            continue
        results = v.get("results", [])
        if results:
            latest = results[-1]
            steps = latest.get("steps", {})

            def _label(s: str) -> str:
                if s == "ok":
                    return "OK"
                if s == "human_blocked":
                    return "BLOCKED"
                return "FAIL"

            step_str = " -> ".join(
                f"{_label(s)}:{k}"
                for k, s in steps.items()
            )
            print(f"  {v.get('name', vid)[:30]}: {step_str}")


def list_types() -> None:
    print("=" * 70)
    print("VENTURE TYPES — Available Autonomy Templates")
    print("=" * 70)
    for vtype, info in VENTURE_TYPES.items():
        pipeline = " → ".join(info["pipeline"])
        print(f"\n{vtype}:")
        print(f"  {info['description']}")
        print(f"  Pipeline: {pipeline}")
        print(f"  Default interval: {info['interval_hours']}h")
        print(f"  Scripts: {len(info.get('scripts', {}))} mapped")


# ══════════════════════════════════════════════════════════════════════════
# DAEMON MODE — run forever cycling all ventures
# ══════════════════════════════════════════════════════════════════════════

def run_daemon() -> None:
    """Run the autonomy engine forever, cycling all active ventures."""
    log("VENTURE AUTONOMY DAEMON STARTING")
    state = AutonomyState()
    engine = VentureAutonomyEngine(state)
    self_mgr = SelfManager(state, engine)

    cycle = 0
    while not _shutdown:
        cycle += 1
        log(f"Daemon cycle #{cycle}")

        try:
            engine.run_all_active()
        except Exception as e:
            log(f"Daemon cycle error: {e}", "ERROR")

        # Self-management every 3rd cycle (auto-install, fix, adjust, prune)
        if cycle % 3 == 0:
            try:
                self_mgr.run_self_management_cycle()
            except Exception as e:
                log(f"Self-management error: {e}", "ERROR")

        # Sleep 30 minutes between cycles (ventures have their own intervals)
        for _ in range(1800):
            if _shutdown:
                break
            time.sleep(1)

    log("VENTURE AUTONOMY DAEMON STOPPED")


# ══════════════════════════════════════════════════════════════════════════
# CLI
# ══════════════════════════════════════════════════════════════════════════

def main() -> None:
    parser = argparse.ArgumentParser(description="PRINTMAXX Venture Autonomy Engine")
    parser.add_argument("--status", action="store_true", help="Show status dashboard")
    parser.add_argument("--run", type=str, help="Run a specific venture by ID")
    parser.add_argument("--run-all", action="store_true", help="Run all active ventures")
    parser.add_argument("--create", nargs=2, metavar=("TYPE", "NAME"), help="Create new autonomous venture")
    parser.add_argument("--list-types", action="store_true", help="List venture types")
    parser.add_argument("--schedule", action="store_true", help="Regenerate all schedule configs")
    parser.add_argument("--install-launchd", type=str, help="Install LLM launchd for a venture")
    parser.add_argument("--install-script-launchd", type=str, help="Install script-only launchd for a venture")
    parser.add_argument("--install-cron", type=str, help="Install cron for a venture")
    parser.add_argument("--install-all", action="store_true",
                        help="Install LLM-powered launchd agents for ALL active ventures")
    parser.add_argument("--import-ceo", action="store_true", help="Import CEO-created ventures")
    parser.add_argument("--daemon", action="store_true", help="Run daemon mode")
    parser.add_argument("--pause", type=str, help="Pause a venture")
    parser.add_argument("--resume-venture", type=str, help="Resume a paused venture")
    parser.add_argument("--bootstrap", action="store_true",
                        help="Create all core autonomous ventures from PRINTMAXX strategy")
    parser.add_argument("--self-manage", action="store_true",
                        help="Run self-management cycle: auto-install, fix broken, adjust intervals, create from opportunities, prune dead")

    args = parser.parse_args()
    state = AutonomyState()
    engine = VentureAutonomyEngine(state)

    if args.status:
        show_status()

    elif args.list_types:
        list_types()

    elif args.run:
        engine.run_venture(args.run)

    elif args.run_all:
        engine.run_all_active()

    elif args.create:
        vtype, name = args.create
        vid = engine.create_venture(vtype.upper(), name)
        if vid:
            print(f"\nCreated: {vid}")
            print(f"\nSchedule configs generated in: {SCHEDULES_DIR}/")
            print(f"  - Cowork prompt: cowork_{vid}.md")
            print(f"  - LaunchD plist: com.printmaxx.{vid}.plist")
            print(f"  - Cron entry: cron_{vid}.txt")
            print(f"  - Ralph prompt: ralph_{vid}.md")
            print(f"\nTo install background execution:")
            print(f"  python3 venture_autonomy.py --install-launchd {vid}")
            print(f"  python3 venture_autonomy.py --install-cron {vid}")

    elif args.schedule:
        log("Regenerating all schedule configs...")
        for vid, v in state.get_active_ventures().items():
            engine._generate_schedule_configs(vid, v)
        log("Done.")

    elif args.install_launchd:
        SchedulerManager.install_launchd(args.install_launchd, mode="llm")

    elif args.install_script_launchd:
        SchedulerManager.install_launchd(args.install_script_launchd, mode="script")

    elif args.install_all:
        SchedulerManager.install_all_llm()

    elif args.install_cron:
        SchedulerManager.install_cron(args.install_cron)

    elif args.import_ceo:
        engine.import_from_ceo_ventures()

    elif args.pause:
        state.update_venture(args.pause, {"status": "PAUSED"})
        log(f"Paused venture: {args.pause}")

    elif args.resume_venture:
        state.update_venture(args.resume_venture, {"status": "ACTIVE"})
        log(f"Resumed venture: {args.resume_venture}")

    elif args.bootstrap:
        log("BOOTSTRAPPING all core autonomous ventures...")
        # Core ventures that every PRINTMAXX instance needs
        core_ventures = [
            ("RESEARCH", "Alpha Intelligence", {"sources": "twitter,reddit,hackernews"}),
            ("CONTENT", "Niche Content Farm", {"platforms": "twitter,linkedin,newsletter"}),
            ("OUTBOUND", "Cold Outreach Engine", {"channels": "email,dm,linkedin"}),
            ("LOCAL_BIZ", "OpenClaw Nationwide", {"city": "Austin TX", "niche": "dentist"}),
            ("MONETIZE", "Affiliate Funnels", {"networks": "gumroad,lemon_squeezy"}),
            ("APP", "App Factory", {"stack": "nextjs,pwa"}),
            ("PRODUCT", "Digital Products", {"types": "templates,ebooks,tools"}),
            ("SCRAPING", "Competitive Intel", {"targets": "competitors,trends,pricing"}),
            ("BROKERING", "Broker Connector Plays", {"verticals": "real_estate,equipment_financing,merchant_processing,lead_gen_service"}),
        ]
        created = 0
        for vtype, name, config in core_ventures:
            # Check if a venture of this type already exists
            existing = [v for v in state.data.get("ventures", {}).values()
                        if v.get("type") == vtype]
            if existing:
                log(f"  {vtype} venture already exists: {existing[0]['name']} — skipping")
                continue
            vid = engine.create_venture(vtype, name, config)
            if vid:
                created += 1
        log(f"Bootstrap complete: {created} new ventures created")
        send_bus_message(f"Autonomy engine bootstrapped {created} core ventures")
        show_status()

    elif args.self_manage:
        sm = SelfManager(state, engine)
        actions = sm.run_self_management_cycle()
        if actions:
            print(f"\nSelf-management: {len(actions)} actions taken")
            for a in actions:
                print(f"  - {a}")
        else:
            print("\nSelf-management: all systems nominal")

    elif args.daemon:
        run_daemon()

    else:
        show_status()


if __name__ == "__main__":
    main()
