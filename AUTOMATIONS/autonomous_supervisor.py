#!/usr/bin/env python3
"""
PRINTMAXX Autonomous Supervisor Daemon

The 24/7 worker that spawns workers. Runs on the spare M2 MacBook.
Reads task queue, spawns LLM agent sessions, monitors agents,
enforces guardrails, logs everything, sends Telegram alerts.

LLM Backend Priority (NO Claude — Claude Max is interactive-only):
    1. Codex CLI (OAuth, free with ChatGPT Pro) — best available model, full agent
    2. Kimi 2.5 API (Moonshot AI) — wrapped in tool-use agent loop
    3. MiniMax API — wrapped in tool-use agent loop

Usage:
    # Run as daemon (foreground, with sleep prevention)
    caffeinate -s python3 AUTOMATIONS/autonomous_supervisor.py

    # Run single task from queue
    python3 AUTOMATIONS/autonomous_supervisor.py --once

    # Trigger self-planning (generate new tasks)
    python3 AUTOMATIONS/autonomous_supervisor.py --plan

    # Check status
    python3 AUTOMATIONS/autonomous_supervisor.py --status

    # Dry run (show what would happen, don't execute)
    python3 AUTOMATIONS/autonomous_supervisor.py --dry-run

    # Run specific scheduled pipeline
    python3 AUTOMATIONS/autonomous_supervisor.py --pipeline research

    # Check LLM backend status
    python3 AUTOMATIONS/autonomous_supervisor.py --backends
"""

import subprocess
import json
import time
import os
import sys
import signal
import hashlib
import argparse
from pathlib import Path
from datetime import datetime, timedelta
import logging
import re

# --- LLM Backend Import ---
try:
    from llm_backends import MultiBackendRouter, ToolUseAgent, create_router
except ImportError:
    # Add AUTOMATIONS to path for sibling import
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from llm_backends import MultiBackendRouter, ToolUseAgent, create_router

# --- OpenClaw Hybrid Engine Import ---
try:
    from openclaw_hybrid import MemoryIntegratedRunner
    _OPENCLAW_AVAILABLE = True
except ImportError:
    _OPENCLAW_AVAILABLE = False

_openclaw_runner = None

def get_openclaw_runner():
    """Lazy-initialize the OpenClaw hybrid runner (singleton)."""
    global _openclaw_runner
    if _openclaw_runner is None and _OPENCLAW_AVAILABLE:
        _openclaw_runner = MemoryIntegratedRunner()
    return _openclaw_runner

# --- Constants ---
PROJECT_ROOT = Path(__file__).resolve().parent.parent
QUEUE_PATH = PROJECT_ROOT / "OPS" / "AUTONOMOUS_TASK_QUEUE.jsonl"
CONFIG_PATH = PROJECT_ROOT / "OPS" / "AUTONOMOUS_WORKER_CONFIG.yaml"
LOG_DIR = PROJECT_ROOT / "AUTOMATIONS" / "logs" / "autonomous"
HEARTBEAT_PATH = PROJECT_ROOT / "OPS" / "HEARTBEAT.md"
ACTIVE_TASKS_PATH = PROJECT_ROOT / "OPS" / "active-tasks.md"
HUMAN_NEEDED_DIR = PROJECT_ROOT / "OPS" / "HUMAN_NEEDED"
OUTPUT_BASE = PROJECT_ROOT / "OPS" / "autonomous_output"
WORKER_PROMPT_PATH = PROJECT_ROOT / "OPS" / "WORKER_BASE_PROMPT.md"
SELF_PLAN_PROMPT_PATH = PROJECT_ROOT / "OPS" / "SELF_PLANNING_PROMPT.md"
LOCK_FILE = PROJECT_ROOT / "AUTOMATIONS" / ".autonomous_supervisor.lock"
COST_TRACKER = LOG_DIR / "daily_cost.json"

# --- Setup logging ---
LOG_DIR.mkdir(parents=True, exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_DIR / f"supervisor_{datetime.now().strftime('%Y-%m-%d')}.log"),
        logging.StreamHandler(),
    ],
)
log = logging.getLogger("supervisor")


# --- Config Loading ---
def load_config() -> dict:
    """Load config from YAML (simple parser, no pyyaml dependency)."""
    config = {
        "cost_cap_per_run": 5.00,
        "cost_cap_daily": 50.00,
        "time_cap_per_run_min": 120,
        "poll_interval_sec": 300,
        "self_plan_interval_hours": 6,
        "max_concurrent_runs": 1,
        "health_check_interval_min": 120,
        "daily_digest_hour": 22,
        # LLM Backend settings — NO Claude in autonomous chain
        "backend_order": "codex,kimi,minimax",
        "codex_model": "gpt-5.3-codex",  # GPT-5.3 via Codex CLI (ChatGPT Pro). ALWAYS best model.
        "codex_approval_mode": "full-auto",
        "claude_model": "sonnet",
        "kimi_api_key": "",
        "kimi_model": "kimi-k2-0711-chat",
        "minimax_api_key": "",
        "minimax_model": "MiniMax-Text-01",
    }

    if not CONFIG_PATH.exists():
        log.warning(f"Config not found at {CONFIG_PATH}, using defaults")
        return config

    try:
        text = CONFIG_PATH.read_text()
        for line in text.split("\n"):
            line = line.strip()
            if not line or line.startswith("#") or ":" not in line:
                continue
            # Simple top-level key:value parsing
            key, _, val = line.partition(":")
            key = key.strip()
            val = val.strip().strip('"').strip("'")
            if key in config:
                # Type coerce based on default type
                if isinstance(config[key], float):
                    try:
                        config[key] = float(val)
                    except ValueError:
                        pass
                elif isinstance(config[key], int):
                    try:
                        config[key] = int(val)
                    except ValueError:
                        pass
                else:
                    config[key] = val
            # Also capture backend-related keys not in defaults
            elif key.startswith(("backend_", "codex_", "claude_", "kimi_", "minimax_")):
                config[key] = val
    except Exception as e:
        log.warning(f"Config parse error: {e}, using defaults")

    return config


def load_blocked_actions() -> list:
    """Load blocked action patterns from config."""
    blocked = [
        "git push", "npm publish", "pip publish",
        "payment", "stripe", "paypal",
        "account creation", "password", "credential",
        "ssh-keygen", "rm -rf /", "sudo rm", "diskutil", "mkfs",
    ]
    # Could parse from YAML blocked_actions list, but defaults are safe
    return blocked


# --- Task Queue ---
class TaskQueue:
    """JSONL-based task queue. Each line is a JSON task object."""

    def __init__(self, path: Path = QUEUE_PATH):
        self.path = path
        self.path.parent.mkdir(parents=True, exist_ok=True)
        if not self.path.exists():
            self.path.write_text("")

    def _read_all(self) -> list:
        """Read all tasks from queue."""
        tasks = []
        for line in self.path.read_text().strip().split("\n"):
            line = line.strip()
            if not line:
                continue
            try:
                tasks.append(json.loads(line))
            except json.JSONDecodeError:
                log.warning(f"Skipping malformed queue entry: {line[:100]}")
        return tasks

    def _write_all(self, tasks: list):
        """Write all tasks back to queue."""
        lines = [json.dumps(t) for t in tasks]
        self.path.write_text("\n".join(lines) + "\n" if lines else "")

    def get_pending(self) -> list:
        """Get all pending tasks, sorted by priority."""
        tasks = [t for t in self._read_all() if t.get("status") == "PENDING"]
        tasks.sort(key=lambda t: t.get("priority", 99))
        return tasks

    def get_next(self) -> dict | None:
        """Get next pending task (highest priority = lowest number)."""
        pending = self.get_pending()
        if not pending:
            return None
        # Check dependencies
        completed_ids = {t["id"] for t in self._read_all() if t.get("status") == "COMPLETED"}
        for task in pending:
            deps = task.get("dependencies", [])
            if all(d in completed_ids for d in deps):
                return task
        return None

    def update_status(self, task_id: str, status: str, result: str = ""):
        """Update task status."""
        tasks = self._read_all()
        for t in tasks:
            if t["id"] == task_id:
                t["status"] = status
                t["updated_at"] = datetime.now().isoformat()
                if result:
                    t["result"] = result[:500]
                if status == "IN_PROGRESS":
                    t["started_at"] = datetime.now().isoformat()
                elif status in ("COMPLETED", "FAILED"):
                    t["completed_at"] = datetime.now().isoformat()
                break
        self._write_all(tasks)

    def add_task(self, task: dict):
        """Add a new task to the queue."""
        task.setdefault("status", "PENDING")
        task.setdefault("created_at", datetime.now().isoformat())
        task.setdefault("priority", 5)
        task.setdefault("risk_level", "LOW")
        task.setdefault("dependencies", [])
        tasks = self._read_all()
        # Dedup by ID
        existing_ids = {t["id"] for t in tasks}
        if task["id"] not in existing_ids:
            tasks.append(task)
            self._write_all(tasks)
            log.info(f"Added task: {task['id']} — {task.get('description', '')[:80]}")
        else:
            log.info(f"Task {task['id']} already exists, skipping")

    def add_tasks(self, tasks: list):
        """Add multiple tasks."""
        for t in tasks:
            self.add_task(t)

    def stats(self) -> dict:
        """Get queue statistics."""
        tasks = self._read_all()
        return {
            "total": len(tasks),
            "pending": sum(1 for t in tasks if t.get("status") == "PENDING"),
            "in_progress": sum(1 for t in tasks if t.get("status") == "IN_PROGRESS"),
            "completed": sum(1 for t in tasks if t.get("status") == "COMPLETED"),
            "failed": sum(1 for t in tasks if t.get("status") == "FAILED"),
        }


# --- Cost Tracking ---
class CostTracker:
    """Track estimated daily API cost."""

    def __init__(self, path: Path = COST_TRACKER):
        self.path = path
        self._load()

    def _load(self):
        if self.path.exists():
            try:
                data = json.loads(self.path.read_text())
                if data.get("date") == datetime.now().strftime("%Y-%m-%d"):
                    self.today_cost = data.get("cost", 0.0)
                    self.runs_today = data.get("runs", 0)
                    return
            except (json.JSONDecodeError, KeyError):
                pass
        self.today_cost = 0.0
        self.runs_today = 0

    def _save(self):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(json.dumps({
            "date": datetime.now().strftime("%Y-%m-%d"),
            "cost": round(self.today_cost, 4),
            "runs": self.runs_today,
        }))

    def add_run(self, duration_min: float, model: str = "opus"):
        """Estimate cost based on runtime and model. Very rough."""
        # Claude Max plan = unlimited tokens, so "cost" is more about
        # rate limit consumption than dollars. Track runtime as proxy.
        # Rough estimate: $0.50 per 10 minutes of Opus runtime
        rate = {"opus": 0.05, "sonnet": 0.02, "haiku": 0.005}.get(model, 0.03)
        estimated = duration_min * rate
        self.today_cost += estimated
        self.runs_today += 1
        self._save()
        return estimated

    def get_daily_cost(self) -> float:
        self._load()
        return self.today_cost

    def is_over_cap(self, cap: float) -> bool:
        return self.get_daily_cost() >= cap


# --- Guardrails ---
def check_guardrails(task: dict) -> tuple[bool, str]:
    """Check if a task passes guardrails. Returns (ok, reason)."""
    # Risk level check
    if task.get("risk_level") == "CRITICAL":
        return False, "CRITICAL risk tasks require human approval"

    # Blocked action patterns
    desc = (task.get("description", "") + " " + task.get("success_criteria", "")).lower()
    for blocked in load_blocked_actions():
        if blocked.lower() in desc:
            return False, f"Task contains blocked action: '{blocked}'"

    return True, "passed"


def validate_output_path(path_str: str) -> bool:
    """Ensure output path is within project root."""
    try:
        resolved = Path(path_str).resolve()
        return str(resolved).startswith(str(PROJECT_ROOT))
    except Exception:
        return False


# --- Direct Script Execution (OpenClaw Pattern) ---
def run_script_directly(task: dict, timeout_min: int = 30) -> tuple:
    """
    Execute a script directly via subprocess (no LLM needed).
    Used for tasks with execution.type == "script".

    Returns (return_code, output_text, duration_minutes).
    """
    execution = task.get("execution", {})
    command = execution.get("command", "")
    script = execution.get("script", "")

    if not command:
        return -2, "No command specified in execution config", 0.0

    # Validate the script path is within project
    script_path = PROJECT_ROOT / "AUTOMATIONS" / script
    if script and not str(script_path.resolve()).startswith(str(PROJECT_ROOT)):
        return -2, f"BLOCKED: script {script} resolves outside project root", 0.0

    log.info(f"Running script directly: {command}")
    start_time = time.time()

    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=timeout_min * 60,
            cwd=str(PROJECT_ROOT),
            env={**os.environ, "PYTHONPATH": str(PROJECT_ROOT / "AUTOMATIONS")},
        )

        duration = (time.time() - start_time) / 60.0
        output = result.stdout
        if result.stderr:
            output += f"\n\n--- STDERR ---\n{result.stderr}"

        log.info(f"Script finished (code {result.returncode}, {duration:.1f} min)")
        return result.returncode, output, duration

    except subprocess.TimeoutExpired:
        duration = (time.time() - start_time) / 60.0
        log.warning(f"Script timed out after {timeout_min} min: {command}")
        return -1, f"Script timed out after {timeout_min} min", duration
    except Exception as e:
        duration = (time.time() - start_time) / 60.0
        log.error(f"Script execution error: {e}")
        return -3, f"Execution error: {str(e)}", duration


def build_fallback_prompt(task: dict, error_output: str) -> str:
    """
    Build an LLM prompt for when a script fails.
    The LLM should analyze the error and try to achieve the task's
    meta-goal through alternative means within guardrails.

    This is the core OpenClaw pattern: scripts do heavy lifting,
    LLM loop handles failures intelligently.
    """
    execution = task.get("execution", {})
    pipeline = task.get("pipeline", "unknown")
    step = task.get("step", "unknown")

    prompt = f"""## SCRIPT FAILURE — AUTONOMOUS RECOVERY

A scheduled automation script has FAILED. Your job is to analyze the failure
and achieve the same goal through alternative means. Stay within guardrails.

### Failed Task
- **Task ID:** {task.get('id', 'unknown')}
- **Pipeline:** {pipeline}
- **Step:** {step}
- **Description:** {task.get('description', 'No description')}
- **Script:** {execution.get('script', 'unknown')}
- **Command:** {execution.get('command', 'unknown')}
- **Success Criteria:** {task.get('success_criteria', 'Complete the task goal')}

### Error Output (last 2000 chars)
```
{error_output[-2000:]}
```

### Your Mission
1. **Analyze** what went wrong (missing dependency? API down? bad data? permission error?)
2. **Try to fix** the immediate issue if it's simple (missing import, wrong path, etc.)
3. **If the script itself is broken**, try to achieve the SAME GOAL through alternative means:
   - Use different Python libraries or approaches
   - Use curl/wget for API calls if requests fails
   - Use alternative data sources if the primary is down
   - Write a quick inline script that accomplishes the same thing
4. **If nothing works**, write a clear diagnostic to OPS/HUMAN_NEEDED/ so the human can fix it

### Guardrails (NON-NEGOTIABLE)
- ALL file operations MUST stay within: {PROJECT_ROOT}
- Do NOT modify system files, dotfiles, or files outside the project
- Do NOT delete CLAUDE.md, LEDGER/, FINANCIALS/, SECRETS/
- Do NOT run destructive commands (rm -rf, dd, diskutil)
- Timeouts: you have {task.get('estimated_minutes', 30)} minutes max

### Output
Write your results to: OPS/autonomous_output/{datetime.now().strftime('%Y-%m-%d')}/{task.get('id', 'unknown')}/
Include: what failed, what you tried, whether you achieved the goal, and any recommendations.
"""
    return prompt


# --- LLM Router (initialized lazily) ---
_llm_router = None

def get_llm_router() -> MultiBackendRouter:
    """Get or create the LLM backend router."""
    global _llm_router
    if _llm_router is None:
        config = load_config()
        # Parse backend_order from comma-separated string to list
        raw_order = config.get("backend_order", "codex,kimi,minimax")
        if isinstance(raw_order, str):
            backend_order = [b.strip() for b in raw_order.split(",") if b.strip()]
        else:
            backend_order = raw_order
        backend_config = {
            "backend_order": backend_order,
            "codex_model": config.get("codex_model", "o3"),
            "codex_approval_mode": config.get("codex_approval_mode", "full-auto"),
            "claude_model": config.get("claude_model", "sonnet"),
            "kimi_api_key": config.get("kimi_api_key", os.environ.get("KIMI_API_KEY", "")),
            "kimi_model": config.get("kimi_model", "kimi-k2-0711-chat"),
            "minimax_api_key": config.get("minimax_api_key", os.environ.get("MINIMAX_API_KEY", "")),
            "minimax_model": config.get("minimax_model", "MiniMax-Text-01"),
        }
        _llm_router = create_router(backend_config)
        available = _llm_router.get_available_backends()
        log.info(f"LLM backend chain: {' -> '.join(available) if available else 'NONE'}")
    return _llm_router


# --- Worker Prompt Building ---
def build_worker_prompt(task: dict) -> str:
    """Build the full prompt for a worker session."""
    template = WORKER_PROMPT_PATH.read_text() if WORKER_PROMPT_PATH.exists() else ""

    # Substitute placeholders
    date_str = datetime.now().strftime("%Y-%m-%d")
    output_path = task.get("output_path", f"OPS/autonomous_output/{date_str}/{task['id']}/")

    prompt = template.replace("{TASK_DESCRIPTION}", task.get("description", ""))
    prompt = prompt.replace("{SUCCESS_CRITERIA}", task.get("success_criteria", "Complete the task"))
    prompt = prompt.replace("{OUTPUT_PATH}", output_path)
    prompt = prompt.replace("{TASK_ID}", task.get("id", "unknown"))
    prompt = prompt.replace("{TIME_LIMIT_MIN}", str(task.get("estimated_minutes", 30)))
    prompt = prompt.replace("{DATE}", date_str)

    return prompt


def spawn_agent_session(prompt: str, timeout_min: int = 120) -> tuple:
    """
    Spawn an LLM agent session using the multi-backend router.
    Tries backends in priority order: codex -> kimi -> minimax (NO Claude).

    For CLI backends (codex, claude): spawns subprocess directly.
    For API backends (kimi, minimax): wraps in tool-use agent loop.

    Returns (return_code, output_text, duration_minutes).
    """
    router = get_llm_router()

    # Write prompt to log
    prompt_file = LOG_DIR / f"prompt_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    prompt_file.write_text(prompt)

    log.info(f"Spawning agent session (timeout: {timeout_min} min)")
    log.info(f"Available backends: {router.get_available_backends()}")

    code, output, duration = router.generate(prompt, timeout_min=timeout_min)

    # Clean up prompt file on success
    if code == 0:
        try:
            prompt_file.unlink()
        except Exception:
            pass

    return code, output, duration


# Legacy alias for backward compatibility
spawn_claude_session = spawn_agent_session


# --- Self-Planning ---
def run_self_planning(queue: TaskQueue) -> int:
    """Spawn a self-planning session to generate new tasks."""
    log.info("Running self-planning agent (queue is empty)")

    if not SELF_PLAN_PROMPT_PATH.exists():
        log.error(f"Self-planning prompt not found at {SELF_PLAN_PROMPT_PATH}")
        return 0

    prompt = SELF_PLAN_PROMPT_PATH.read_text()

    code, output, duration = spawn_claude_session(prompt, timeout_min=30)

    if code != 0:
        log.warning(f"Self-planning failed (code {code})")
        return 0

    # Parse task list from output
    # Look for JSON array in the output
    tasks_added = 0
    try:
        # Find JSON array in output (between [ and ])
        json_match = re.search(r'\[[\s\S]*?\]', output)
        if json_match:
            tasks = json.loads(json_match.group())
            if isinstance(tasks, list):
                for task in tasks:
                    if isinstance(task, dict) and "id" in task and "description" in task:
                        task["status"] = "PENDING"
                        task["source"] = "self_planning"
                        task["created_at"] = datetime.now().isoformat()
                        queue.add_task(task)
                        tasks_added += 1
    except (json.JSONDecodeError, AttributeError) as e:
        log.warning(f"Could not parse tasks from planner output: {e}")

    log.info(f"Self-planning generated {tasks_added} new tasks")
    return tasks_added


# --- Run Logging ---
def log_run(task: dict, code: int, output: str, duration: float):
    """Log a run result to daily JSONL log."""
    date_str = datetime.now().strftime("%Y-%m-%d")
    log_file = LOG_DIR / f"runs_{date_str}.jsonl"

    entry = {
        "timestamp": datetime.now().isoformat(),
        "task_id": task.get("id"),
        "category": task.get("category"),
        "description": task.get("description", "")[:200],
        "return_code": code,
        "duration_min": round(duration, 2),
        "output_length": len(output),
        "output_summary": output[:500] if output else "",
        "success": code == 0,
    }

    with open(log_file, "a") as f:
        f.write(json.dumps(entry) + "\n")


def save_output(task: dict, output: str):
    """Save task output to designated path."""
    date_str = datetime.now().strftime("%Y-%m-%d")
    output_path = task.get("output_path", f"OPS/autonomous_output/{date_str}/{task['id']}/")

    full_path = PROJECT_ROOT / output_path
    full_path.mkdir(parents=True, exist_ok=True)

    output_file = full_path / "output.md"
    output_file.write_text(f"# Task Output: {task.get('id')}\n\n"
                            f"**Description:** {task.get('description', '')}\n"
                            f"**Completed:** {datetime.now().isoformat()}\n\n"
                            f"---\n\n{output}")


# --- Lock File ---
def acquire_lock() -> bool:
    """Prevent multiple supervisor instances."""
    if LOCK_FILE.exists():
        # Check if PID is still running
        try:
            pid = int(LOCK_FILE.read_text().strip())
            os.kill(pid, 0)  # Check if process exists
            return False  # Process still running
        except (ProcessLookupError, ValueError):
            pass  # Stale lock, overwrite

    LOCK_FILE.write_text(str(os.getpid()))
    return True


def release_lock():
    """Release the supervisor lock."""
    try:
        LOCK_FILE.unlink()
    except FileNotFoundError:
        pass


# --- Active Tasks Tracking ---
def update_active_tasks(task: dict, status: str):
    """Update OPS/active-tasks.md for crash recovery."""
    ACTIVE_TASKS_PATH.parent.mkdir(parents=True, exist_ok=True)

    if status == "started":
        content = (
            f"# Active Tasks (Autonomous Worker)\n\n"
            f"**Last updated:** {datetime.now().isoformat()}\n\n"
            f"## Currently Running\n\n"
            f"- **Task:** {task.get('id')}\n"
            f"- **Description:** {task.get('description', '')}\n"
            f"- **Category:** {task.get('category', 'unknown')}\n"
            f"- **Started:** {datetime.now().strftime('%H:%M')}\n"
            f"- **Time cap:** {task.get('estimated_minutes', 30)} min\n"
        )
        ACTIVE_TASKS_PATH.write_text(content)
    elif status == "completed":
        content = (
            f"# Active Tasks (Autonomous Worker)\n\n"
            f"**Last updated:** {datetime.now().isoformat()}\n\n"
            f"## No Active Tasks\n\n"
            f"Last completed: {task.get('id')} at {datetime.now().strftime('%H:%M')}\n"
        )
        ACTIVE_TASKS_PATH.write_text(content)


# --- Scheduled Pipelines ---
PIPELINE_PROMPTS = {
    "research": (
        "Run the full PRINTMAXX research pipeline:\n"
        "1. Run: python3 AUTOMATIONS/daily_research_orchestrator.py --full\n"
        "2. Run: python3 AUTOMATIONS/twitter_alpha_scraper.py --all\n"
        "3. Run: python3 AUTOMATIONS/background_reddit_scraper.py --scrape\n"
        "4. Run: python3 AUTOMATIONS/competitor_monitor.py --scan\n"
        "5. Run: python3 AUTOMATIONS/alpha_auto_processor.py --process-new\n"
        "6. Update HEARTBEAT.md with results count\n"
        "Write summary to OPS/autonomous_output/{date}/research_pipeline/output.md"
    ),
    "content": (
        "Generate content from today's high-scoring alpha:\n"
        "1. Read LEDGER/ALPHA_STAGING.csv for APPROVED entries with score >= 80\n"
        "2. For each high-scoring entry, generate 3-5 tweets following .claude/rules/copy-style.md\n"
        "3. Generate 1 tweet thread (5-7 tweets) from best entry\n"
        "4. Save all content to CONTENT/social/auto_generated/ with PENDING_REVIEW status\n"
        "5. Update HEARTBEAT.md with content count\n"
        "Write summary to OPS/autonomous_output/{date}/content_pipeline/output.md"
    ),
    "midday": (
        "Run midday pulse check:\n"
        "1. Quick scan of trending topics (python3 AUTOMATIONS/trend_aggregator.py --scan)\n"
        "2. Check for new high-signal alpha since morning\n"
        "3. If new high-signal found (score >= 85), generate mini content batch\n"
        "4. Check system health (python3 AUTOMATIONS/system_health_monitor.py --quick)\n"
        "Write summary to OPS/autonomous_output/{date}/midday_pulse/output.md"
    ),
    "overnight": (
        "Run overnight builder tasks:\n"
        "1. Read OPS/PERSISTENT_TASK_TRACKER.md for building tasks\n"
        "2. Pick the highest-priority buildable task that doesn't require human\n"
        "3. Execute it fully (build + test + save output)\n"
        "4. Run retrospective: what worked, what didn't, write to AUTOMATIONS/logs/autonomous/retrospective.jsonl\n"
        "5. Generate task proposals for tomorrow's morning run\n"
        "Write results to OPS/autonomous_output/{date}/overnight_builder/output.md"
    ),
    "health": (
        "Run system health check:\n"
        "1. python3 AUTOMATIONS/system_health_monitor.py --check\n"
        "2. Verify cron jobs are firing (check log timestamps)\n"
        "3. Check disk space\n"
        "4. Check for failed runs in AUTOMATIONS/logs/autonomous/\n"
        "5. Auto-recover any stalled processes\n"
        "Write report to OPS/autonomous_output/{date}/health_check/output.md"
    ),
}


def run_scheduled_pipeline(pipeline_name: str) -> bool:
    """Run a pre-defined pipeline by name."""
    if pipeline_name not in PIPELINE_PROMPTS:
        log.error(f"Unknown pipeline: {pipeline_name}")
        return False

    date_str = datetime.now().strftime("%Y-%m-%d")
    prompt_body = PIPELINE_PROMPTS[pipeline_name].replace("{date}", date_str)

    task = {
        "id": f"PIPELINE_{pipeline_name}_{date_str}",
        "category": pipeline_name,
        "description": f"Scheduled {pipeline_name} pipeline",
        "risk_level": "LOW",
        "estimated_minutes": 60,
        "output_path": f"OPS/autonomous_output/{date_str}/{pipeline_name}_pipeline/",
    }

    # Build full prompt
    worker_base = WORKER_PROMPT_PATH.read_text() if WORKER_PROMPT_PATH.exists() else ""
    full_prompt = worker_base.replace("{TASK_DESCRIPTION}", prompt_body)
    full_prompt = full_prompt.replace("{SUCCESS_CRITERIA}", f"Complete the {pipeline_name} pipeline")
    full_prompt = full_prompt.replace("{OUTPUT_PATH}", task["output_path"])
    full_prompt = full_prompt.replace("{TASK_ID}", task["id"])
    full_prompt = full_prompt.replace("{TIME_LIMIT_MIN}", "60")
    full_prompt = full_prompt.replace("{DATE}", date_str)

    config = load_config()
    update_active_tasks(task, "started")

    code, output, duration = spawn_claude_session(full_prompt, timeout_min=int(config["time_cap_per_run_min"]))

    update_active_tasks(task, "completed")
    log_run(task, code, output, duration)
    save_output(task, output)

    # Cost tracking
    cost_tracker = CostTracker()
    cost_tracker.add_run(duration)

    # Alerts
    try:
        from autonomous_alerts import alert_task_completed, alert_task_failed
        if code == 0:
            alert_task_completed(task["id"], task["description"], duration, output[:200])
        else:
            alert_task_failed(task["id"], task["description"], output[:300])
    except ImportError:
        pass

    return code == 0


# --- Main Supervisor Loop ---
def run_supervisor(one_shot: bool = False, dry_run: bool = False):
    """Main supervisor daemon loop."""
    if not acquire_lock():
        log.error("Another supervisor instance is running. Exiting.")
        sys.exit(1)

    config = load_config()
    queue = TaskQueue()
    cost_tracker = CostTracker()
    last_self_plan = datetime.now()
    last_health_check = datetime.now()
    last_digest_date = ""

    # Send startup alert
    try:
        from autonomous_alerts import alert_supervisor_started
        alert_supervisor_started()
    except ImportError:
        pass

    log.info("=" * 60)
    log.info("PRINTMAXX Autonomous Supervisor — STARTED")
    log.info(f"Poll interval: {config['poll_interval_sec']}s")
    log.info(f"Cost cap: ${config['cost_cap_daily']}/day, ${config['cost_cap_per_run']}/run")
    log.info(f"Time cap: {config['time_cap_per_run_min']} min/run")
    log.info(f"Queue: {queue.stats()}")
    log.info("=" * 60)

    # Refresh memory layers on supervisor start
    try:
        subprocess.run(
            ["python3", str(PROJECT_ROOT / "AUTOMATIONS" / "memory_manager.py"), "--full"],
            capture_output=True, timeout=60, cwd=str(PROJECT_ROOT)
        )
        log.info("Memory layers refreshed (heartbeat + active-tasks + daily log)")
    except Exception as e:
        log.warning(f"Memory refresh failed: {e}")

    def graceful_shutdown(signum, frame):
        log.info("Received shutdown signal. Cleaning up...")
        release_lock()
        try:
            from autonomous_alerts import alert_supervisor_stopped
            alert_supervisor_stopped("signal received")
        except ImportError:
            pass
        sys.exit(0)

    signal.signal(signal.SIGTERM, graceful_shutdown)
    signal.signal(signal.SIGINT, graceful_shutdown)

    try:
        while True:
            now = datetime.now()

            # --- Daily cost cap check ---
            if cost_tracker.is_over_cap(config["cost_cap_daily"]):
                log.warning(f"Daily cost cap exceeded (${cost_tracker.get_daily_cost():.2f})")
                try:
                    from autonomous_alerts import alert_cost_warning
                    alert_cost_warning(cost_tracker.get_daily_cost(), config["cost_cap_daily"])
                except ImportError:
                    pass

                if one_shot:
                    break
                # Sleep until midnight
                midnight = now.replace(hour=0, minute=0, second=0) + timedelta(days=1)
                sleep_sec = (midnight - now).total_seconds()
                log.info(f"Sleeping {sleep_sec / 3600:.1f} hours until midnight")
                time.sleep(min(sleep_sec, 3600))  # Check every hour
                continue

            # --- Health check ---
            if (now - last_health_check).total_seconds() > config["health_check_interval_min"] * 60:
                log.info("Running periodic health check")
                if not dry_run:
                    run_scheduled_pipeline("health")
                last_health_check = now

            # --- Daily digest ---
            today_str = now.strftime("%Y-%m-%d")
            if now.hour >= config["daily_digest_hour"] and last_digest_date != today_str:
                log.info("Sending daily digest")
                try:
                    from autonomous_alerts import alert_daily_digest
                    stats = queue.stats()
                    stats["estimated_cost"] = cost_tracker.get_daily_cost()
                    stats["total_runtime_min"] = 0  # Could track this
                    alert_daily_digest(stats)
                    last_digest_date = today_str
                except ImportError:
                    pass

                # Generate daily memory summary
                try:
                    subprocess.run(
                        ["python3", str(PROJECT_ROOT / "AUTOMATIONS" / "memory_manager.py"), "--daily-summary"],
                        capture_output=True, timeout=60, cwd=str(PROJECT_ROOT)
                    )
                except Exception:
                    pass

            # --- Get next task ---
            task = queue.get_next()

            if task:
                task_id = task["id"]
                log.info(f"Processing task: {task_id} — {task.get('description', '')[:80]}")

                # Guardrail check
                ok, reason = check_guardrails(task)
                if not ok:
                    log.warning(f"Task {task_id} blocked by guardrails: {reason}")
                    queue.update_status(task_id, "BLOCKED", reason)
                    try:
                        from autonomous_alerts import alert_human_needed
                        alert_human_needed(task_id, f"Blocked by guardrails: {reason}")
                    except ImportError:
                        pass
                    continue

                if dry_run:
                    execution = task.get("execution", {})
                    exec_type = execution.get("type", "llm")
                    if exec_type == "script":
                        log.info(f"[DRY RUN] Would run script: {execution.get('command', '?')} (fallback: LLM)")
                    elif exec_type == "llm":
                        log.info(f"[DRY RUN] Would run LLM task: {task.get('description', '')[:60]}")
                    else:
                        log.info(f"[DRY RUN] Would execute task: {task_id}")
                    if one_shot:
                        break
                    time.sleep(config["poll_interval_sec"])
                    continue

                # Mark as in progress
                queue.update_status(task_id, "IN_PROGRESS")
                update_active_tasks(task, "started")

                try:
                    from autonomous_alerts import alert_task_started
                    alert_task_started(task_id, task.get("description", ""))
                except ImportError:
                    pass

                # --- OpenClaw Hybrid Execution Engine ---
                # Handles: health checks, crash recovery, script retries,
                # error categorization, LLM fallback, memory integration.
                execution = task.get("execution", {})
                exec_type = execution.get("type", "llm")

                timeout = min(
                    task.get("estimated_minutes", 30) * 2,  # 2x estimated time
                    int(config["time_cap_per_run_min"]),
                )

                runner = get_openclaw_runner()
                if runner is not None:
                    # Full OpenClaw hybrid path (preferred)
                    log.info(f"OpenClaw execution: type={exec_type}, timeout={timeout}min")
                    code, output, duration = runner.execute(task, timeout_min=timeout)
                    used_fallback = "LLM FALLBACK" in (output or "")
                else:
                    # Fallback: direct execution if openclaw_hybrid not available
                    log.warning("OpenClaw runner unavailable, using direct execution")
                    code = -99
                    output = ""
                    duration = 0.0
                    used_fallback = False

                    if exec_type == "script":
                        log.info(f"Script execution: {execution.get('command', '?')}")
                        code, output, duration = run_script_directly(task, timeout_min=timeout)
                        if code != 0:
                            log.warning(f"Script failed (code {code}), attempting LLM fallback...")
                            used_fallback = True
                            fallback_prompt = build_fallback_prompt(task, output)
                            fallback_timeout = max(timeout - int(duration), 10)
                            fb_code, fb_output, fb_duration = spawn_agent_session(
                                fallback_prompt, timeout_min=fallback_timeout
                            )
                            output = (
                                f"--- SCRIPT OUTPUT (FAILED, code {code}) ---\n"
                                f"{output[:1000]}\n\n"
                                f"--- LLM FALLBACK (code {fb_code}) ---\n"
                                f"{fb_output}"
                            )
                            code = fb_code
                            duration += fb_duration
                    elif exec_type == "llm":
                        llm_prompt = execution.get("prompt", "")
                        if not llm_prompt:
                            llm_prompt = build_worker_prompt(task)
                        log.info(f"LLM execution: sending prompt ({len(llm_prompt)} chars)")
                        code, output, duration = spawn_agent_session(llm_prompt, timeout_min=timeout)
                    else:
                        prompt = build_worker_prompt(task)
                        log.info(f"Legacy execution: building worker prompt")
                        code, output, duration = spawn_agent_session(prompt, timeout_min=timeout)

                # Track cost (only counts LLM time, script execution is free)
                estimated_cost = cost_tracker.add_run(duration if exec_type != "script" or used_fallback else 0)

                # Log the run
                log_run(task, code, output, duration)

                if code == 0:
                    # Success
                    status_note = output[:200]
                    if used_fallback:
                        status_note = f"[LLM FALLBACK] {status_note}"
                    queue.update_status(task_id, "COMPLETED", status_note)
                    save_output(task, output)
                    update_active_tasks(task, "completed")
                    fb_tag = " (via LLM fallback)" if used_fallback else ""
                    log.info(f"Task {task_id} completed{fb_tag} in {duration:.1f} min (est cost: ${estimated_cost:.2f})")
                    try:
                        from autonomous_alerts import alert_task_completed
                        alert_task_completed(task_id, task.get("description", ""), duration, status_note)
                    except ImportError:
                        pass

                    # Heartbeat + daily log handled by OpenClaw runner._post_task()
                    # Only call memory_manager directly if runner was unavailable
                    if runner is None:
                        try:
                            subprocess.run(
                                ["python3", str(PROJECT_ROOT / "AUTOMATIONS" / "memory_manager.py"), "--heartbeat"],
                                capture_output=True, timeout=30, cwd=str(PROJECT_ROOT)
                            )
                        except Exception:
                            pass

                elif code == -1:
                    # Timeout
                    queue.update_status(task_id, "FAILED", f"Timeout after {timeout} min")
                    update_active_tasks(task, "completed")
                    log.warning(f"Task {task_id} timed out after {timeout} min")
                    try:
                        from autonomous_alerts import alert_agent_timeout
                        alert_agent_timeout(task_id, timeout)
                    except ImportError:
                        pass

                    # Failure logging handled by OpenClaw runner._post_task()
                    if runner is None:
                        try:
                            subprocess.run(
                                ["python3", str(PROJECT_ROOT / "AUTOMATIONS" / "memory_manager.py"),
                                 "--log", f"TASK FAILED: {task_id} - Timeout after {timeout} min"],
                                capture_output=True, timeout=30, cwd=str(PROJECT_ROOT)
                            )
                        except Exception:
                            pass

                else:
                    # Other failure (script + fallback both failed, or LLM failed)
                    fail_note = output[:200]
                    if used_fallback:
                        fail_note = f"[SCRIPT+FALLBACK FAILED] {fail_note}"
                    queue.update_status(task_id, "FAILED", fail_note)
                    update_active_tasks(task, "completed")
                    log.error(f"Task {task_id} failed (code {code}){' after LLM fallback' if used_fallback else ''}")
                    try:
                        from autonomous_alerts import alert_task_failed
                        alert_task_failed(task_id, task.get("description", ""), output[:300])
                    except ImportError:
                        pass

                    # Failure logging handled by OpenClaw runner._post_task()
                    if runner is None:
                        try:
                            subprocess.run(
                                ["python3", str(PROJECT_ROOT / "AUTOMATIONS" / "memory_manager.py"),
                                 "--log", f"TASK FAILED: {task_id} - {task.get('description', '')[:100]}"],
                                capture_output=True, timeout=30, cwd=str(PROJECT_ROOT)
                            )
                        except Exception:
                            pass

                if one_shot:
                    break

            else:
                # Queue empty — try self-planning
                hours_since_plan = (now - last_self_plan).total_seconds() / 3600
                if hours_since_plan >= config["self_plan_interval_hours"]:
                    log.info("Queue empty and self-plan interval reached")
                    if not dry_run:
                        try:
                            from autonomous_alerts import alert_queue_empty
                            alert_queue_empty()
                        except ImportError:
                            pass
                        tasks_added = run_self_planning(queue)
                        if tasks_added > 0:
                            log.info(f"Self-planning added {tasks_added} tasks")
                    last_self_plan = now
                else:
                    log.debug(f"Queue empty, next self-plan in {config['self_plan_interval_hours'] - hours_since_plan:.1f} hours")

                if one_shot:
                    log.info("No tasks in queue (one-shot mode)")
                    break

            # Sleep before next poll
            time.sleep(config["poll_interval_sec"])

    except KeyboardInterrupt:
        log.info("Supervisor stopped by user")
    finally:
        release_lock()
        try:
            from autonomous_alerts import alert_supervisor_stopped
            alert_supervisor_stopped("clean shutdown")
        except ImportError:
            pass
        log.info("Supervisor shutdown complete")


# --- Status Display ---
def show_status():
    """Show current supervisor and queue status."""
    queue = TaskQueue()
    stats = queue.stats()
    cost_tracker = CostTracker()

    print("\n" + "=" * 50)
    print("  PRINTMAXX AUTONOMOUS SUPERVISOR STATUS")
    print("=" * 50)

    # Lock status
    if LOCK_FILE.exists():
        try:
            pid = int(LOCK_FILE.read_text().strip())
            try:
                os.kill(pid, 0)
                print(f"\n  Supervisor: RUNNING (PID {pid})")
            except ProcessLookupError:
                print(f"\n  Supervisor: STALE LOCK (PID {pid} not running)")
        except ValueError:
            print(f"\n  Supervisor: UNKNOWN LOCK STATE")
    else:
        print(f"\n  Supervisor: NOT RUNNING")

    # Queue stats
    print(f"\n  Task Queue:")
    print(f"    Total:       {stats['total']}")
    print(f"    Pending:     {stats['pending']}")
    print(f"    In Progress: {stats['in_progress']}")
    print(f"    Completed:   {stats['completed']}")
    print(f"    Failed:      {stats['failed']}")

    # Cost
    print(f"\n  Today's Cost:  ${cost_tracker.get_daily_cost():.2f}")
    print(f"  Runs Today:    {cost_tracker.runs_today}")

    # Recent logs
    today_log = LOG_DIR / f"runs_{datetime.now().strftime('%Y-%m-%d')}.jsonl"
    if today_log.exists():
        lines = today_log.read_text().strip().split("\n")
        print(f"\n  Today's Runs:  {len(lines)}")
        if lines:
            last = json.loads(lines[-1])
            print(f"  Last Run:      {last.get('task_id', 'unknown')} at {last.get('timestamp', '')[:19]}")
            print(f"  Last Duration: {last.get('duration_min', 0):.1f} min")
            print(f"  Last Status:   {'SUCCESS' if last.get('success') else 'FAILED'}")

    # LLM Backend status
    try:
        router = get_llm_router()
        available = router.get_available_backends()
        print(f"\n  LLM Backends: {' -> '.join(available) if available else 'NONE'}")
    except Exception:
        print(f"\n  LLM Backends: error loading")

    # Pending tasks preview
    pending = queue.get_pending()[:5]
    if pending:
        print(f"\n  Next Tasks:")
        for t in pending:
            exec_info = t.get("execution", {})
            exec_type = exec_info.get("type", "llm")
            type_tag = "SCR" if exec_type == "script" else "LLM"
            print(f"    [{t.get('priority', '?')}] [{type_tag}] {t['id']}: {t.get('description', '')[:55]}")

    print("\n" + "=" * 50 + "\n")


# --- Backend Status ---
def show_backend_status():
    """Show LLM backend status."""
    router = get_llm_router()
    status = router.get_status()
    available = router.get_available_backends()

    print("\n" + "=" * 50)
    print("  LLM BACKEND STATUS")
    print("=" * 50)

    for name, info in status.items():
        avail = "READY" if info["available"] else "NOT AVAILABLE"
        print(f"\n  {name}: {avail}")
        for k, v in info["info"].items():
            print(f"    {k}: {v}")

    print(f"\n  Active chain: {' -> '.join(available) if available else 'NONE (all backends unavailable!)'}")

    if not available:
        print("\n  To fix:")
        print("    1. Install codex: npm i -g @openai/codex")
        print("    2. Or set KIMI_API_KEY env var for Kimi 2.5 fallback")
        print("    3. Or set MINIMAX_API_KEY env var for MiniMax fallback")
        print("    4. Or ensure 'claude' CLI is installed and authenticated")

    print("\n" + "=" * 50 + "\n")


# --- CLI ---
def main():
    parser = argparse.ArgumentParser(description="PRINTMAXX Autonomous Supervisor")
    parser.add_argument("--once", action="store_true", help="Run one task then exit")
    parser.add_argument("--plan", action="store_true", help="Run self-planning only")
    parser.add_argument("--status", action="store_true", help="Show status")
    parser.add_argument("--dry-run", action="store_true", help="Show what would happen")
    parser.add_argument("--pipeline", type=str, help="Run specific pipeline (research|content|midday|overnight|health)")
    parser.add_argument("--add-task", type=str, help="Add task from JSON string")
    parser.add_argument("--seed", action="store_true", help="Seed queue with initial tasks")
    parser.add_argument("--backends", action="store_true", help="Show LLM backend status")

    args = parser.parse_args()

    if args.backends:
        show_backend_status()
    elif args.status:
        show_status()
    elif args.plan:
        queue = TaskQueue()
        run_self_planning(queue)
    elif args.pipeline:
        run_scheduled_pipeline(args.pipeline)
    elif args.add_task:
        queue = TaskQueue()
        try:
            task = json.loads(args.add_task)
            queue.add_task(task)
            print(f"Added task: {task.get('id', 'unknown')}")
        except json.JSONDecodeError as e:
            print(f"Invalid JSON: {e}")
    elif args.seed:
        seed_initial_tasks()
    else:
        run_supervisor(one_shot=args.once, dry_run=args.dry_run)


def seed_initial_tasks():
    """Seed the queue with initial research and maintenance tasks."""
    queue = TaskQueue()
    date_str = datetime.now().strftime("%Y%m%d")

    tasks = [
        {
            "id": f"TASK_{date_str}_001",
            "category": "research",
            "priority": 1,
            "description": "Run full research pipeline: scrape Twitter (116 accounts), Reddit (41 subs), process new alpha, score and route to categories",
            "risk_level": "LOW",
            "estimated_minutes": 60,
            "success_criteria": "New alpha entries added to ALPHA_STAGING.csv, alpha auto-processor run, digest generated",
            "output_path": f"OPS/autonomous_output/{datetime.now().strftime('%Y-%m-%d')}/research/",
        },
        {
            "id": f"TASK_{date_str}_002",
            "category": "content",
            "priority": 2,
            "description": "Generate content from approved alpha (score >= 80). Create 5 tweets per niche (tech, faith, fitness) plus 1 thread from best alpha entry. Follow copy-style.md voice.",
            "risk_level": "LOW",
            "estimated_minutes": 45,
            "dependencies": [f"TASK_{date_str}_001"],
            "success_criteria": "15+ tweets saved to CONTENT/social/auto_generated/ with PENDING_REVIEW status, 1 thread saved",
            "output_path": f"OPS/autonomous_output/{datetime.now().strftime('%Y-%m-%d')}/content/",
        },
        {
            "id": f"TASK_{date_str}_003",
            "category": "analysis",
            "priority": 3,
            "description": "Run competitor monitoring: scan 19 apps across 6 niches via iTunes API, check for price/rating/version changes. Run App Store tracker for 36 apps.",
            "risk_level": "LOW",
            "estimated_minutes": 30,
            "success_criteria": "Competitor data updated, any significant changes flagged in daily log",
            "output_path": f"OPS/autonomous_output/{datetime.now().strftime('%Y-%m-%d')}/competitor/",
        },
        {
            "id": f"TASK_{date_str}_004",
            "category": "maintenance",
            "priority": 5,
            "description": "System health check: verify cron jobs fired, check disk space, validate log files, check for stale data (alpha entries > 30 days old)",
            "risk_level": "LOW",
            "estimated_minutes": 15,
            "success_criteria": "Health report generated with GREEN/AMBER/RED status for all 14 checkpoints",
            "output_path": f"OPS/autonomous_output/{datetime.now().strftime('%Y-%m-%d')}/health/",
        },
        {
            "id": f"TASK_{date_str}_005",
            "category": "self_improvement",
            "priority": 6,
            "description": "Run retrospective on recent autonomous runs. Review logs in AUTOMATIONS/logs/autonomous/. Identify: what took longer than expected, what failed, what patterns emerge. Write learnings to LEARNINGS.jsonl.",
            "risk_level": "LOW",
            "estimated_minutes": 30,
            "success_criteria": "Retrospective written with 3+ learnings, appended to LEARNINGS.jsonl",
            "output_path": f"OPS/autonomous_output/{datetime.now().strftime('%Y-%m-%d')}/retrospective/",
        },
    ]

    queue.add_tasks(tasks)
    print(f"Seeded {len(tasks)} initial tasks to queue")
    print(f"Queue now has {queue.stats()['pending']} pending tasks")


if __name__ == "__main__":
    main()
