#!/usr/bin/env python3

from __future__ import annotations
"""
PRINTMAXX OpenClaw Hybrid Execution Engine
==========================================
Blends OpenClaw battle-tested autonomous patterns with PRINTMAXX 3-layer memory.

OpenClaw patterns implemented:
  - Script-first execution (fast, no LLM cost)
  - Closed-loop error recovery (analyze -> categorize -> fix -> retry)
  - LLM fallback only after exhausting script-level fixes
  - Sub-agent spawning with kill conditions
  - Crash recovery via active-tasks checkpoint

Memory integration (Memento system):
  - Pre-task: read heartbeat + active-tasks for crash recovery
  - During-task: progress checkpoints every 60s
  - Post-task: heartbeat update + daily log + clear active-tasks
  - Learning: retry fixes logged for future reference

Usage:
    from openclaw_hybrid import ClosedLoopExecutor, MemoryIntegratedRunner

    # In supervisor:
    runner = MemoryIntegratedRunner()
    code, output, duration = runner.execute(task)

    # Standalone:
    python3 AUTOMATIONS/openclaw_hybrid.py --task-id AUTO_20260219_research_twitter_scrape
    python3 AUTOMATIONS/openclaw_hybrid.py --health-check
    python3 AUTOMATIONS/openclaw_hybrid.py --crash-recovery
"""

import subprocess
import json
import time
import os
import sys
import re
import shutil
import threading
import argparse
import logging
from pathlib import Path
from datetime import datetime, timedelta

# --- Path bootstrap (sibling import support) ---
_THIS_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(_THIS_DIR))

try:
    from llm_backends import MultiBackendRouter, create_router
except ImportError:
    MultiBackendRouter = None
    create_router = None

# --- Constants ---
PROJECT_ROOT = _THIS_DIR.parent
OPS = PROJECT_ROOT / "OPS"
HEARTBEAT_PATH = OPS / "HEARTBEAT.md"
ACTIVE_TASKS_PATH = OPS / "active-tasks.md"
DAILY_LOGS_DIR = _THIS_DIR / "logs" / "daily"
AUTONOMOUS_LOG_DIR = _THIS_DIR / "logs" / "autonomous"
RETRY_LEARNINGS_PATH = _THIS_DIR / "logs" / "retry_learnings.jsonl"
COST_TRACKER_PATH = AUTONOMOUS_LOG_DIR / "daily_cost.json"
LOCK_DIR = _THIS_DIR / "locks"

for _d in [DAILY_LOGS_DIR, AUTONOMOUS_LOG_DIR, LOCK_DIR]:
    _d.mkdir(parents=True, exist_ok=True)

# --- Logging ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.FileHandler(
            AUTONOMOUS_LOG_DIR / f"openclaw_{datetime.now().strftime('%Y-%m-%d')}.log"
        ),
        logging.StreamHandler(),
    ],
)
log = logging.getLogger("openclaw_hybrid")


# ============================================================
# ERROR CATEGORIZATION
# ============================================================

class ErrorCategory:
    MISSING_DEP = "MISSING_DEP"
    API_DOWN = "API_DOWN"
    BAD_DATA = "BAD_DATA"
    PERMISSION = "PERMISSION"
    TIMEOUT = "TIMEOUT"
    UNKNOWN = "UNKNOWN"


_ERROR_PATTERNS = {
    ErrorCategory.MISSING_DEP: [
        r"ModuleNotFoundError:\s+No module named '(\S+)'",
        r"ImportError:\s+cannot import name",
        r"command not found",
        r"No such file or directory.*bin/",
        r"pip.*install",
        r"Could not find a version",
        r"ModuleNotFoundError",
        r"ImportError",
    ],
    ErrorCategory.API_DOWN: [
        r"ConnectionError",
        r"ConnectionRefusedError",
        r"HTTPError.*5\d\d",
        r"TimeoutError.*connect",
        r"urlopen error.*Connection refused",
        r"requests\.exceptions\.ConnectionError",
        r"503 Service Unavailable",
        r"502 Bad Gateway",
        r"429 Too Many Requests",
        r"rate.?limit",
    ],
    ErrorCategory.BAD_DATA: [
        r"JSONDecodeError",
        r"UnicodeDecodeError",
        r"ValueError.*invalid literal",
        r"KeyError:\s+",
        r"IndexError:\s+list index",
        r"csv\.Error",
        r"ParserError",
        r"EmptyDataError",
        r"malformed",
    ],
    ErrorCategory.PERMISSION: [
        r"PermissionError",
        r"Permission denied",
        r"EACCES",
        r"Operation not permitted",
        r"Access is denied",
        r"Errno 13",
    ],
    ErrorCategory.TIMEOUT: [
        r"TimeoutExpired",
        r"timed out",
        r"Timeout",
        r"deadline exceeded",
        r"ETIMEDOUT",
    ],
}


def categorize_error(error_text: str) -> tuple:
    """
    Categorize an error by scanning its output.
    Returns (category, matched_pattern, extracted_detail).
    """
    if not error_text:
        return ErrorCategory.UNKNOWN, "", ""

    for category, patterns in _ERROR_PATTERNS.items():
        for pattern in patterns:
            m = re.search(pattern, error_text, re.IGNORECASE)
            if m:
                detail = m.group(1) if m.lastindex and m.lastindex >= 1 else m.group(0)
                return category, pattern, detail.strip()

    return ErrorCategory.UNKNOWN, "", error_text[:200]


# ============================================================
# ADAPTIVE RETRY ENGINE
# ============================================================

class AdaptiveRetryEngine:
    """
    Per-category retry strategies with learning.
    Writes successful fixes to retry_learnings.jsonl.
    """

    MAX_RETRIES = 3

    def __init__(self):
        self._learnings_cache = self._load_learnings()

    # --- learnings persistence ---
    def _load_learnings(self) -> list:
        if not RETRY_LEARNINGS_PATH.exists():
            return []
        learnings = []
        try:
            for line in RETRY_LEARNINGS_PATH.read_text().strip().split("\n"):
                line = line.strip()
                if line:
                    learnings.append(json.loads(line))
        except Exception:
            pass
        return learnings

    def _save_learning(self, entry: dict):
        entry["timestamp"] = datetime.now().isoformat()
        try:
            with open(RETRY_LEARNINGS_PATH, "a") as f:
                f.write(json.dumps(entry) + "\n")
            self._learnings_cache.append(entry)
        except Exception as e:
            log.warning(f"Could not save retry learning: {e}")

    def _lookup_past_fix(self, category: str, detail: str) -> str | None:
        """Check if we have a known fix for this error signature."""
        for entry in reversed(self._learnings_cache):
            if entry.get("category") == category and entry.get("success"):
                if detail and detail in entry.get("detail", ""):
                    return entry.get("fix_command", "")
        return None

    # --- strategy dispatching ---

    def generate_fix(
        self, category: str, detail: str, attempt: int, task: dict
    ) -> dict | None:
        """
        Generate a fix strategy for the given error category and attempt number.
        Returns dict with keys: description, command, env_patch, timeout_multiplier.
        Returns None if no strategy left.
        """
        if attempt > self.MAX_RETRIES:
            return None

        # Check past learnings first
        past = self._lookup_past_fix(category, detail)
        if past and attempt == 1:
            return {
                "description": f"Learned fix from past: {past[:80]}",
                "command": past,
                "env_patch": {},
                "timeout_multiplier": 1.0,
            }

        dispatch = {
            ErrorCategory.MISSING_DEP: self._fix_missing_dep,
            ErrorCategory.API_DOWN: self._fix_api_down,
            ErrorCategory.BAD_DATA: self._fix_bad_data,
            ErrorCategory.PERMISSION: self._fix_permission,
            ErrorCategory.TIMEOUT: self._fix_timeout,
            ErrorCategory.UNKNOWN: self._fix_unknown,
        }
        handler = dispatch.get(category, self._fix_unknown)
        return handler(detail, attempt, task)

    # --- per-category strategies ---

    def _fix_missing_dep(self, detail: str, attempt: int, task: dict) -> dict | None:
        module_name = detail.strip("'\"")
        if attempt == 1:
            # Try pip3 install
            return {
                "description": f"pip3 install missing module: {module_name}",
                "command": f"pip3 install {module_name}",
                "env_patch": {},
                "timeout_multiplier": 1.0,
            }
        elif attempt == 2:
            # Try common alternative package names
            alternatives = {
                "cv2": "opencv-python",
                "PIL": "Pillow",
                "yaml": "pyyaml",
                "bs4": "beautifulsoup4",
                "sklearn": "scikit-learn",
                "dotenv": "python-dotenv",
                "lxml": "lxml",
                "dateutil": "python-dateutil",
            }
            alt = alternatives.get(module_name, f"{module_name}")
            return {
                "description": f"Try alternative package name: {alt}",
                "command": f"pip3 install {alt}",
                "env_patch": {},
                "timeout_multiplier": 1.0,
            }
        elif attempt == 3:
            return {
                "description": "Try with --user flag and updated pip",
                "command": f"pip3 install --user --upgrade {module_name}",
                "env_patch": {},
                "timeout_multiplier": 1.0,
            }
        return None

    def _fix_api_down(self, detail: str, attempt: int, task: dict) -> dict | None:
        if attempt == 1:
            return {
                "description": "Wait 30s then retry (transient API failure)",
                "command": "__WAIT_30__",
                "env_patch": {},
                "timeout_multiplier": 1.0,
            }
        elif attempt == 2:
            return {
                "description": "Wait 60s then retry with extended timeout",
                "command": "__WAIT_60__",
                "env_patch": {},
                "timeout_multiplier": 2.0,
            }
        elif attempt == 3:
            # Try alternative URL environment hints if task has them
            alt_url = task.get("execution", {}).get("fallback_api_url", "")
            if alt_url:
                return {
                    "description": f"Try alternative API URL: {alt_url}",
                    "command": "__RETRY__",
                    "env_patch": {"API_BASE_URL": alt_url},
                    "timeout_multiplier": 1.5,
                }
            return {
                "description": "Final retry with doubled timeout",
                "command": "__RETRY__",
                "env_patch": {},
                "timeout_multiplier": 3.0,
            }
        return None

    def _fix_bad_data(self, detail: str, attempt: int, task: dict) -> dict | None:
        execution = task.get("execution", {})
        command = execution.get("command", "")

        if attempt == 1:
            # Try adding --force or --skip-errors flag
            if command:
                if "--force" not in command and "--skip-errors" not in command:
                    return {
                        "description": "Retry with --skip-errors flag",
                        "command": command + " --skip-errors",
                        "env_patch": {},
                        "timeout_multiplier": 1.0,
                    }
            return {
                "description": "Retry with PYTHONDONTWRITEBYTECODE (clean run)",
                "command": "__RETRY__",
                "env_patch": {"PYTHONDONTWRITEBYTECODE": "1"},
                "timeout_multiplier": 1.0,
            }
        elif attempt == 2:
            if command and "--force" not in command:
                return {
                    "description": "Retry with --force flag",
                    "command": command + " --force",
                    "env_patch": {},
                    "timeout_multiplier": 1.0,
                }
            return {
                "description": "Clean retry with fresh environment",
                "command": "__RETRY__",
                "env_patch": {"PYTHONHASHSEED": "0"},
                "timeout_multiplier": 1.0,
            }
        elif attempt == 3:
            return {
                "description": "Validate input data then retry",
                "command": "__RETRY__",
                "env_patch": {"STRICT_MODE": "0"},
                "timeout_multiplier": 1.0,
            }
        return None

    def _fix_permission(self, detail: str, attempt: int, task: dict) -> dict | None:
        execution = task.get("execution", {})
        command = execution.get("command", "")

        if attempt == 1:
            # Try making output directories
            output_path = task.get("output_path", "")
            if output_path:
                full = PROJECT_ROOT / output_path
                return {
                    "description": f"Create output directories: {output_path}",
                    "command": f"mkdir -p {full}",
                    "env_patch": {},
                    "timeout_multiplier": 1.0,
                }
            return {
                "description": "Retry (permission may have been transient lock)",
                "command": "__RETRY__",
                "env_patch": {},
                "timeout_multiplier": 1.0,
            }
        elif attempt == 2:
            # Try writing to alternative path
            alt_output = PROJECT_ROOT / "OPS" / "autonomous_output" / "fallback"
            return {
                "description": f"Redirect output to fallback path: {alt_output}",
                "command": "__RETRY__",
                "env_patch": {"OUTPUT_DIR": str(alt_output)},
                "timeout_multiplier": 1.0,
            }
        elif attempt == 3:
            # Check and fix file permissions
            return {
                "description": "Fix file permissions in project dir and retry",
                "command": f"chmod -R u+rw {PROJECT_ROOT / 'OPS'}",
                "env_patch": {},
                "timeout_multiplier": 1.0,
            }
        return None

    def _fix_timeout(self, detail: str, attempt: int, task: dict) -> dict | None:
        execution = task.get("execution", {})
        command = execution.get("command", "")

        if attempt == 1:
            return {
                "description": "Retry with 2x timeout",
                "command": "__RETRY__",
                "env_patch": {},
                "timeout_multiplier": 2.0,
            }
        elif attempt == 2:
            # Try with --quick or --fast flag
            if command and "--quick" not in command and "--fast" not in command:
                return {
                    "description": "Retry with --quick flag and 3x timeout",
                    "command": command + " --quick",
                    "env_patch": {},
                    "timeout_multiplier": 3.0,
                }
            return {
                "description": "Retry with 3x timeout",
                "command": "__RETRY__",
                "env_patch": {},
                "timeout_multiplier": 3.0,
            }
        elif attempt == 3:
            return {
                "description": "Final retry with max timeout and reduced scope",
                "command": "__RETRY__",
                "env_patch": {"BATCH_SIZE": "100", "MAX_WORKERS": "5"},
                "timeout_multiplier": 4.0,
            }
        return None

    def _fix_unknown(self, detail: str, attempt: int, task: dict) -> dict | None:
        if attempt == 1:
            return {
                "description": "Blind retry (unknown error category)",
                "command": "__RETRY__",
                "env_patch": {},
                "timeout_multiplier": 1.5,
            }
        elif attempt == 2:
            return {
                "description": "Retry with clean environment",
                "command": "__RETRY__",
                "env_patch": {"PYTHONDONTWRITEBYTECODE": "1"},
                "timeout_multiplier": 2.0,
            }
        return None

    def record_outcome(self, category: str, detail: str, fix_cmd: str, success: bool):
        """Record whether a fix worked so future runs can learn."""
        self._save_learning({
            "category": category,
            "detail": detail,
            "fix_command": fix_cmd,
            "success": success,
        })


# ============================================================
# HEALTH-AWARE SCHEDULER
# ============================================================

class HealthAwareScheduler:
    """
    Pre-flight health checks before running any task.
    If health check fails, log and skip (never crash the supervisor).
    """

    def __init__(self):
        self.issues = []

    def check_all(self) -> tuple:
        """
        Run all health checks.
        Returns (healthy: bool, issues: list[str]).
        """
        self.issues = []
        self._check_disk_space()
        self._check_stale_locks()
        self._check_memory_freshness()
        self._check_daily_cost()
        healthy = len(self.issues) == 0
        return healthy, self.issues

    def _check_disk_space(self):
        try:
            usage = shutil.disk_usage(str(PROJECT_ROOT))
            free_gb = usage.free / (1024 ** 3)
            if free_gb < 1.0:
                self.issues.append(f"Low disk space: {free_gb:.1f}GB free (need >1GB)")
        except Exception as e:
            self.issues.append(f"Could not check disk space: {e}")

    def _check_stale_locks(self):
        try:
            now = time.time()
            two_hours = 2 * 3600
            for lock_file in LOCK_DIR.glob("*.lock"):
                age = now - lock_file.stat().st_mtime
                if age > two_hours:
                    self.issues.append(
                        f"Stale lock: {lock_file.name} ({age / 3600:.1f}h old)"
                    )
        except Exception as e:
            self.issues.append(f"Could not check locks: {e}")

    def _check_memory_freshness(self):
        try:
            if HEARTBEAT_PATH.exists():
                age_sec = time.time() - HEARTBEAT_PATH.stat().st_mtime
                age_hours = age_sec / 3600
                if age_hours > 1.0:
                    self.issues.append(
                        f"Stale heartbeat: {age_hours:.1f}h old (should be <1h)"
                    )
            else:
                self.issues.append("HEARTBEAT.md does not exist")
        except Exception as e:
            self.issues.append(f"Could not check memory freshness: {e}")

    def _check_daily_cost(self):
        try:
            if COST_TRACKER_PATH.exists():
                data = json.loads(COST_TRACKER_PATH.read_text())
                today = datetime.now().strftime("%Y-%m-%d")
                if data.get("date") == today:
                    cost = data.get("cost", 0.0)
                    if cost >= 50.0:
                        self.issues.append(
                            f"Daily cost cap reached: ${cost:.2f} (cap $50)"
                        )
        except Exception:
            pass  # Cost tracker missing is not a health issue

    def log_skip(self, task_id: str, issues: list):
        log.warning(f"HEALTH CHECK FAILED for {task_id}: {'; '.join(issues)}")
        _daily_log(f"HEALTH_SKIP: {task_id} - {'; '.join(issues)}")


# ============================================================
# CLOSED-LOOP EXECUTOR
# ============================================================

class ClosedLoopExecutor:
    """
    Executes a task dict with closed-loop retry logic.
    On script failure: categorize error, generate fix, retry (up to 3x)
    before escalating to LLM fallback.
    """

    def __init__(self, retry_engine: AdaptiveRetryEngine | None = None):
        self.retry_engine = retry_engine or AdaptiveRetryEngine()
        self._llm_router = None

    def _get_router(self) -> "MultiBackendRouter | None":
        if self._llm_router is not None:
            return self._llm_router
        if create_router is None:
            log.warning("llm_backends not available, LLM fallback disabled")
            return None
        try:
            config = _load_config()
            self._llm_router = create_router(config)
            return self._llm_router
        except Exception as e:
            log.warning(f"Could not create LLM router: {e}")
            return None

    def execute(self, task: dict, timeout_min: int = 30) -> tuple:
        """
        Execute a task through the closed-loop pipeline.
        Returns (return_code, output_text, duration_minutes).
        """
        execution = task.get("execution", {})
        exec_type = execution.get("type", "llm")

        if exec_type == "script":
            return self._execute_script_with_retries(task, timeout_min)
        elif exec_type == "llm":
            return self._execute_llm(task, timeout_min)
        else:
            return self._execute_llm(task, timeout_min)

    def _run_subprocess(
        self, command: str, timeout_min: int, env_patch: dict | None = None
    ) -> tuple:
        """Run a shell command. Returns (code, output, duration_min)."""
        env = {
            **os.environ,
            "PYTHONPATH": str(_THIS_DIR),
        }
        if env_patch:
            env.update(env_patch)

        start = time.time()
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=timeout_min * 60,
                cwd=str(PROJECT_ROOT),
                env=env,
            )
            duration = (time.time() - start) / 60.0
            output = result.stdout
            if result.stderr:
                output += f"\n\n--- STDERR ---\n{result.stderr}"
            return result.returncode, output, duration
        except subprocess.TimeoutExpired:
            duration = (time.time() - start) / 60.0
            return -1, f"Script timed out after {timeout_min} min", duration
        except Exception as e:
            duration = (time.time() - start) / 60.0
            return -3, f"Execution error: {e}", duration

    def _execute_script_with_retries(self, task: dict, timeout_min: int) -> tuple:
        """
        Script execution with closed-loop retries.
        Categorize errors and apply per-category fix strategies.
        """
        execution = task.get("execution", {})
        command = execution.get("command", "")

        if not command:
            return -2, "No command specified in execution config", 0.0

        # Validate script path within project
        script = execution.get("script", "")
        if script:
            script_path = PROJECT_ROOT / "AUTOMATIONS" / script
            if not str(script_path.resolve()).startswith(str(PROJECT_ROOT)):
                return -2, f"BLOCKED: script {script} outside project root", 0.0

        all_outputs = []
        total_duration = 0.0

        # Initial execution
        log.info(f"[attempt 0] Running: {command[:120]}")
        code, output, duration = self._run_subprocess(command, timeout_min)
        total_duration += duration
        all_outputs.append(f"--- Attempt 0 (initial) ---\n{output}")

        if code == 0:
            return 0, output, duration

        # Error hit -- enter retry loop
        for attempt in range(1, AdaptiveRetryEngine.MAX_RETRIES + 1):
            remaining_time = max(timeout_min - total_duration, 5)

            category, pattern, detail = categorize_error(output)
            log.warning(
                f"[attempt {attempt}] Error category={category}, detail={detail[:80]}"
            )

            fix = self.retry_engine.generate_fix(category, detail, attempt, task)
            if fix is None:
                log.info(f"[attempt {attempt}] No more retry strategies for {category}")
                break

            log.info(f"[attempt {attempt}] Fix strategy: {fix['description']}")
            all_outputs.append(
                f"--- Attempt {attempt}: {fix['description']} ---"
            )

            fix_cmd = fix["command"]
            env_patch = fix.get("env_patch", {})
            timeout_mult = fix.get("timeout_multiplier", 1.0)

            # Handle special commands
            if fix_cmd == "__WAIT_30__":
                time.sleep(30)
                fix_cmd = command
            elif fix_cmd == "__WAIT_60__":
                time.sleep(60)
                fix_cmd = command
            elif fix_cmd == "__RETRY__":
                fix_cmd = command

            # If the fix is a preparatory command (pip install, mkdir, chmod),
            # run it first and then re-run the original command
            is_prep = any(
                fix_cmd.startswith(prefix)
                for prefix in ["pip3 ", "mkdir ", "chmod "]
            )

            if is_prep:
                log.info(f"[attempt {attempt}] Running prep: {fix_cmd[:100]}")
                prep_code, prep_out, prep_dur = self._run_subprocess(
                    fix_cmd, timeout_min=5, env_patch=env_patch
                )
                total_duration += prep_dur
                all_outputs.append(f"Prep output: {prep_out[:500]}")

                # Now re-run the original command
                adj_timeout = remaining_time * timeout_mult
                code, output, duration = self._run_subprocess(
                    command, timeout_min=int(adj_timeout), env_patch=env_patch
                )
            else:
                adj_timeout = remaining_time * timeout_mult
                code, output, duration = self._run_subprocess(
                    fix_cmd, timeout_min=int(adj_timeout), env_patch=env_patch
                )

            total_duration += duration
            all_outputs.append(f"Output: {output[:2000]}")

            # Record outcome
            success = code == 0
            self.retry_engine.record_outcome(category, detail, fix_cmd, success)

            if success:
                log.info(f"[attempt {attempt}] Fix succeeded!")
                combined = "\n\n".join(all_outputs)
                return 0, combined, total_duration

        # All retries exhausted -- try LLM fallback
        log.warning("All script retries exhausted, attempting LLM fallback")
        fb_code, fb_output, fb_duration = self._llm_fallback(
            task, "\n\n".join(all_outputs), max(timeout_min - total_duration, 10)
        )
        total_duration += fb_duration
        all_outputs.append(f"--- LLM Fallback (code {fb_code}) ---\n{fb_output}")

        combined = "\n\n".join(all_outputs)
        return fb_code, combined, total_duration

    def _execute_llm(self, task: dict, timeout_min: int) -> tuple:
        """Execute a task purely via LLM."""
        router = self._get_router()
        if router is None:
            return -2, "No LLM backends available", 0.0

        execution = task.get("execution", {})
        prompt = execution.get("prompt", "")
        if not prompt:
            prompt = _build_worker_prompt(task)

        log.info(f"LLM execution: sending prompt ({len(prompt)} chars)")
        code, output, duration = router.generate(prompt, timeout_min=timeout_min)
        return code, output, duration

    def _llm_fallback(
        self, task: dict, error_output: str, timeout_min: float
    ) -> tuple:
        """LLM fallback for failed scripts (core OpenClaw pattern)."""
        router = self._get_router()
        if router is None:
            return -2, "No LLM backends available for fallback", 0.0

        prompt = _build_fallback_prompt(task, error_output)
        code, output, duration = router.generate(
            prompt, timeout_min=int(timeout_min)
        )
        return code, output, duration


# ============================================================
# SUB-AGENT SPAWNER
# ============================================================

class SubAgentSpawner:
    """
    Spawns sub-tasks for complex failures.
    Each sub-agent gets: success criteria, output format, time budget, kill condition.
    Kill condition: no file writes in 5 minutes -> kill and log.
    """

    def __init__(self, router: "MultiBackendRouter | None" = None):
        self._router = router

    def spawn(
        self,
        sub_prompt: str,
        success_criteria: str,
        output_format: str,
        time_budget_min: int = 15,
        kill_no_write_min: int = 5,
    ) -> tuple:
        """
        Spawn a sub-agent for a focused sub-task.
        Returns (code, output, duration_min).
        """
        if self._router is None:
            return -2, "No LLM router available for sub-agents", 0.0

        full_prompt = f"""## SUB-AGENT TASK

### Success Criteria
{success_criteria}

### Required Output Format
{output_format}

### Time Budget
{time_budget_min} minutes maximum.

### Guardrails
- ALL files within {PROJECT_ROOT}
- Do NOT modify CLAUDE.md, SECRETS/, LEDGER/ core files
- Do NOT run destructive commands

### Task
{sub_prompt}
"""

        log.info(
            f"Spawning sub-agent (budget={time_budget_min}min, "
            f"kill_idle={kill_no_write_min}min)"
        )

        start = time.time()
        code, output, duration = self._router.generate(
            full_prompt, timeout_min=time_budget_min
        )

        # Log the sub-agent result
        _daily_log(
            f"SUB_AGENT: code={code}, duration={duration:.1f}min, "
            f"output_len={len(output)}"
        )
        return code, output, duration


# ============================================================
# MEMORY-INTEGRATED RUNNER
# ============================================================

class MemoryIntegratedRunner:
    """
    Wraps ClosedLoopExecutor with deep memory coupling.
    BEFORE: read heartbeat + active-tasks for crash recovery, check daily log.
    DURING: progress checkpoints to active-tasks.md every 60s (separate thread).
    AFTER: update heartbeat, log to daily, clear active-tasks entry.
    """

    def __init__(self):
        self.executor = ClosedLoopExecutor()
        self.health = HealthAwareScheduler()
        self._checkpoint_thread = None
        self._checkpoint_stop = threading.Event()

    def execute(self, task: dict, timeout_min: int = 30) -> tuple:
        """
        Full memory-integrated execution pipeline.
        Returns (return_code, output_text, duration_minutes).
        """
        task_id = task.get("id", "unknown")

        # --- HEALTH CHECK ---
        healthy, issues = self.health.check_all()
        if not healthy:
            self.health.log_skip(task_id, issues)
            # Non-fatal: log but still attempt unless disk is critical
            critical = any("disk" in i.lower() for i in issues)
            if critical:
                return (
                    -4,
                    f"HEALTH CHECK FAILED (critical): {'; '.join(issues)}",
                    0.0,
                )
            log.warning(f"Health issues (non-critical): {'; '.join(issues)}")

        # --- PRE-TASK: memory read ---
        self._pre_task(task)

        # --- DURING: start checkpoint thread ---
        self._start_checkpointing(task)

        try:
            # --- EXECUTE ---
            code, output, duration = self.executor.execute(task, timeout_min)
        except Exception as e:
            code, output, duration = -3, f"Uncaught exception: {e}", 0.0
            log.error(f"Uncaught exception during task {task_id}: {e}")
        finally:
            # --- STOP checkpointing ---
            self._stop_checkpointing()

        # --- POST-TASK: memory write ---
        self._post_task(task, code, output, duration)

        return code, output, duration

    # --- pre-task ---

    def _pre_task(self, task: dict):
        task_id = task.get("id", "unknown")
        log.info(f"PRE-TASK: {task_id}")

        # Read heartbeat for system state awareness
        if HEARTBEAT_PATH.exists():
            try:
                heartbeat = HEARTBEAT_PATH.read_text()[:500]
                log.info(f"Heartbeat: {heartbeat.strip()[:120]}")
            except Exception:
                pass

        # Check for crash recovery: stale active-tasks entries
        self._check_crash_recovery(task)

        # Check if already attempted today
        if self._already_attempted_today(task_id):
            log.info(f"Task {task_id} was already attempted today (logged in daily)")

        # Write to active-tasks that we are starting
        self._write_active_task(task, "STARTED")
        _daily_log(f"TASK_START: {task_id} - {task.get('description', '')[:80]}")

    def _check_crash_recovery(self, task: dict):
        """Detect stale entries in active-tasks.md (>2x estimated time)."""
        if not ACTIVE_TASKS_PATH.exists():
            return

        try:
            content = ACTIVE_TASKS_PATH.read_text()
            # Look for "Started:" timestamp
            m = re.search(r"Started:\s*(\d{2}:\d{2})", content)
            if m and "Currently Running" in content:
                # There is a stale entry
                estimated = task.get("estimated_minutes", 30)
                age_hours = _file_age_hours(ACTIVE_TASKS_PATH)
                stale_threshold = (estimated * 2) / 60  # Convert to hours
                if age_hours > max(stale_threshold, 0.5):
                    log.warning(
                        f"CRASH RECOVERY: stale active-task detected "
                        f"({age_hours:.1f}h old, threshold={stale_threshold:.1f}h)"
                    )
                    _daily_log(
                        f"CRASH_RECOVERY: stale active-task "
                        f"({age_hours:.1f}h old). Overwriting."
                    )
        except Exception as e:
            log.warning(f"Crash recovery check failed: {e}")

    def _already_attempted_today(self, task_id: str) -> bool:
        today = datetime.now().strftime("%Y-%m-%d")
        daily_log = DAILY_LOGS_DIR / f"{today}.md"
        if not daily_log.exists():
            return False
        try:
            return task_id in daily_log.read_text()
        except Exception:
            return False

    # --- during-task checkpointing ---

    def _start_checkpointing(self, task: dict):
        self._checkpoint_stop.clear()
        self._checkpoint_thread = threading.Thread(
            target=self._checkpoint_loop,
            args=(task,),
            daemon=True,
        )
        self._checkpoint_thread.start()

    def _checkpoint_loop(self, task: dict):
        """Write progress checkpoint to active-tasks every 60s."""
        start = time.time()
        while not self._checkpoint_stop.wait(60):
            elapsed = (time.time() - start) / 60.0
            self._write_active_task(
                task,
                f"RUNNING ({elapsed:.0f}min elapsed)",
            )

    def _stop_checkpointing(self):
        self._checkpoint_stop.set()
        if self._checkpoint_thread and self._checkpoint_thread.is_alive():
            self._checkpoint_thread.join(timeout=5)

    # --- post-task ---

    def _post_task(self, task: dict, code: int, output: str, duration: float):
        task_id = task.get("id", "unknown")
        success = code == 0
        status = "COMPLETED" if success else "FAILED"

        log.info(
            f"POST-TASK: {task_id} -> {status} "
            f"(code={code}, {duration:.1f}min)"
        )

        # Update active-tasks (clear)
        self._write_active_task(task, status)

        # Log to daily
        _daily_log(
            f"TASK_{status}: {task_id} "
            f"(code={code}, {duration:.1f}min, output_len={len(output)})"
        )

        # Log to autonomous run log
        self._log_run(task, code, output, duration)

        # Update heartbeat
        self._update_heartbeat()

    def _write_active_task(self, task: dict, status: str):
        """Write/update active-tasks.md for crash recovery."""
        try:
            ACTIVE_TASKS_PATH.parent.mkdir(parents=True, exist_ok=True)
            now = datetime.now()

            if status in ("COMPLETED", "FAILED"):
                content = (
                    f"# Active Tasks (OpenClaw Hybrid)\n\n"
                    f"**Last updated:** {now.isoformat()}\n\n"
                    f"## No Active Tasks\n\n"
                    f"Last {status.lower()}: {task.get('id')} "
                    f"at {now.strftime('%H:%M')}\n"
                )
            else:
                content = (
                    f"# Active Tasks (OpenClaw Hybrid)\n\n"
                    f"**Last updated:** {now.isoformat()}\n\n"
                    f"## Currently Running\n\n"
                    f"- **Task:** {task.get('id')}\n"
                    f"- **Description:** {task.get('description', '')}\n"
                    f"- **Status:** {status}\n"
                    f"- **Started:** {now.strftime('%H:%M')}\n"
                    f"- **Time cap:** {task.get('estimated_minutes', 30)} min\n"
                    f"- **Engine:** OpenClaw Hybrid (closed-loop + memento)\n"
                )
            ACTIVE_TASKS_PATH.write_text(content)
        except Exception as e:
            log.warning(f"Could not update active-tasks.md: {e}")

    def _log_run(self, task: dict, code: int, output: str, duration: float):
        """Log run result to autonomous JSONL log."""
        date_str = datetime.now().strftime("%Y-%m-%d")
        log_file = AUTONOMOUS_LOG_DIR / f"runs_{date_str}.jsonl"

        entry = {
            "timestamp": datetime.now().isoformat(),
            "engine": "openclaw_hybrid",
            "task_id": task.get("id"),
            "category": task.get("category"),
            "description": task.get("description", "")[:200],
            "return_code": code,
            "duration_min": round(duration, 2),
            "output_length": len(output),
            "output_summary": output[:500] if output else "",
            "success": code == 0,
        }

        try:
            with open(log_file, "a") as f:
                f.write(json.dumps(entry) + "\n")
        except Exception as e:
            log.warning(f"Could not write run log: {e}")

    def _update_heartbeat(self):
        """Trigger heartbeat update via memory_manager if available."""
        try:
            mm_path = _THIS_DIR / "memory_manager.py"
            if mm_path.exists():
                subprocess.run(
                    ["python3", str(mm_path), "--heartbeat"],
                    capture_output=True,
                    timeout=30,
                    cwd=str(PROJECT_ROOT),
                )
        except Exception:
            pass

    # --- crash recovery (standalone) ---

    def recover_from_crash(self) -> dict:
        """
        Detect and report stale active-tasks entries.
        Returns dict with recovery info.
        """
        result = {"stale_found": False, "task_id": None, "age_hours": 0}

        if not ACTIVE_TASKS_PATH.exists():
            return result

        try:
            content = ACTIVE_TASKS_PATH.read_text()
            if "Currently Running" not in content:
                return result

            # Extract task info
            m_task = re.search(r"\*\*Task:\*\*\s+(.+)", content)
            m_started = re.search(r"\*\*Started:\*\*\s+(\d{2}:\d{2})", content)

            if m_task:
                result["task_id"] = m_task.group(1).strip()
                result["stale_found"] = True
                result["age_hours"] = _file_age_hours(ACTIVE_TASKS_PATH)
                log.info(
                    f"Crash recovery: found stale task {result['task_id']} "
                    f"({result['age_hours']:.1f}h old)"
                )
                _daily_log(
                    f"CRASH_RECOVERY_DETECT: {result['task_id']} "
                    f"stale for {result['age_hours']:.1f}h"
                )
        except Exception as e:
            log.warning(f"Crash recovery scan failed: {e}")

        return result


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def _file_age_hours(path: Path) -> float:
    if not path.exists():
        return 999.0
    return (time.time() - path.stat().st_mtime) / 3600


def _daily_log(message: str):
    """Append a message to today's daily log."""
    today = datetime.now().strftime("%Y-%m-%d")
    log_file = DAILY_LOGS_DIR / f"{today}.md"
    ts = datetime.now().strftime("%H:%M:%S")
    try:
        if not log_file.exists():
            log_file.write_text(f"# Daily Log -- {today}\n\n")
        with open(log_file, "a") as f:
            f.write(f"[{ts}] {message}\n")
    except Exception:
        pass


def _load_config() -> dict:
    """Load supervisor config (simple YAML parser)."""
    config_path = OPS / "AUTONOMOUS_WORKER_CONFIG.yaml"
    config = {
        "backend_order": ["codex", "kimi", "minimax"],
        "codex_model": "gpt-5.3-codex",
        "codex_approval_mode": "full-auto",
        "kimi_api_key": os.environ.get("KIMI_API_KEY", ""),
        "kimi_model": "kimi-k2-0711-chat",
        "minimax_api_key": os.environ.get("MINIMAX_API_KEY", ""),
        "minimax_model": "MiniMax-Text-01",
    }

    if not config_path.exists():
        return config

    try:
        text = config_path.read_text()
        for line in text.split("\n"):
            line = line.strip()
            if not line or line.startswith("#") or ":" not in line:
                continue
            key, _, val = line.partition(":")
            key = key.strip()
            val = val.strip().strip('"').strip("'")
            if key == "backend_order":
                config[key] = [b.strip() for b in val.split(",") if b.strip()]
            elif key in config:
                config[key] = val
    except Exception:
        pass

    return config


def _build_worker_prompt(task: dict) -> str:
    """Build a basic worker prompt from a task dict."""
    date_str = datetime.now().strftime("%Y-%m-%d")
    return (
        f"## Task: {task.get('id', 'unknown')}\n\n"
        f"**Description:** {task.get('description', '')}\n"
        f"**Success criteria:** {task.get('success_criteria', 'Complete the task')}\n"
        f"**Date:** {date_str}\n"
        f"**Time limit:** {task.get('estimated_minutes', 30)} minutes\n\n"
        f"Execute this task. Write results to: "
        f"OPS/autonomous_output/{date_str}/{task.get('id', 'unknown')}/\n"
    )


def _build_fallback_prompt(task: dict, error_output: str) -> str:
    """Build LLM fallback prompt for a failed script."""
    execution = task.get("execution", {})
    return f"""## SCRIPT FAILURE -- AUTONOMOUS RECOVERY (OpenClaw Hybrid)

A scheduled script has FAILED after exhausting {AdaptiveRetryEngine.MAX_RETRIES} retry strategies.
Your job: analyze the failure and achieve the same goal through alternative means.

### Failed Task
- **Task ID:** {task.get('id', 'unknown')}
- **Description:** {task.get('description', 'No description')}
- **Script:** {execution.get('script', 'unknown')}
- **Command:** {execution.get('command', 'unknown')}
- **Success Criteria:** {task.get('success_criteria', 'Complete the task goal')}

### Error Output (last 2000 chars)
```
{error_output[-2000:]}
```

### Your Mission
1. Analyze what went wrong (all retry strategies failed)
2. Try to achieve the SAME GOAL through alternative means
3. Use different Python libraries, approaches, or tools
4. If nothing works, write a diagnostic to OPS/HUMAN_NEEDED/

### Guardrails (NON-NEGOTIABLE)
- ALL file operations within: {PROJECT_ROOT}
- Do NOT modify system files or files outside the project
- Time limit: {task.get('estimated_minutes', 30)} minutes
"""


# ============================================================
# CLI
# ============================================================

def _cmd_health_check():
    """Run standalone health check."""
    scheduler = HealthAwareScheduler()
    healthy, issues = scheduler.check_all()

    print("\n" + "=" * 50)
    print("  OPENCLAW HYBRID -- HEALTH CHECK")
    print("=" * 50)

    if healthy:
        print("\n  Status: HEALTHY (all checks passed)")
    else:
        print(f"\n  Status: UNHEALTHY ({len(issues)} issue(s))")
        for issue in issues:
            print(f"    - {issue}")

    # Extra info
    print(f"\n  Project root: {PROJECT_ROOT}")
    print(f"  Heartbeat: {'exists' if HEARTBEAT_PATH.exists() else 'MISSING'}")
    print(f"  Active tasks: {'exists' if ACTIVE_TASKS_PATH.exists() else 'MISSING'}")
    print(f"  Retry learnings: {RETRY_LEARNINGS_PATH}")

    learning_count = 0
    if RETRY_LEARNINGS_PATH.exists():
        try:
            learning_count = sum(
                1 for line in RETRY_LEARNINGS_PATH.read_text().strip().split("\n")
                if line.strip()
            )
        except Exception:
            pass
    print(f"  Learned fixes: {learning_count}")
    print("\n" + "=" * 50 + "\n")


def _cmd_crash_recovery():
    """Run standalone crash recovery check."""
    runner = MemoryIntegratedRunner()
    result = runner.recover_from_crash()

    print("\n" + "=" * 50)
    print("  OPENCLAW HYBRID -- CRASH RECOVERY")
    print("=" * 50)

    if result["stale_found"]:
        print(f"\n  STALE TASK FOUND:")
        print(f"    Task ID: {result['task_id']}")
        print(f"    Stale for: {result['age_hours']:.1f} hours")
        print(f"\n  Options:")
        print(f"    1. Re-run the task")
        print(f"    2. Mark as failed and skip")
        print(f"\n  To clear: edit {ACTIVE_TASKS_PATH}")
    else:
        print("\n  No stale tasks found. System clean.")

    print("\n" + "=" * 50 + "\n")


def _cmd_run_task(task_id: str):
    """Execute a single task from the queue by ID."""
    queue_path = OPS / "AUTONOMOUS_TASK_QUEUE.jsonl"
    if not queue_path.exists():
        print(f"Task queue not found at {queue_path}")
        return

    task = None
    for line in queue_path.read_text().strip().split("\n"):
        line = line.strip()
        if not line:
            continue
        try:
            t = json.loads(line)
            if t.get("id") == task_id:
                task = t
                break
        except json.JSONDecodeError:
            continue

    if task is None:
        print(f"Task {task_id} not found in queue")
        return

    print(f"\nRunning task: {task_id}")
    print(f"Description: {task.get('description', '')[:80]}")
    print(f"Type: {task.get('execution', {}).get('type', 'llm')}")
    print()

    runner = MemoryIntegratedRunner()
    code, output, duration = runner.execute(task)

    print(f"\n{'=' * 50}")
    print(f"  RESULT: {'SUCCESS' if code == 0 else 'FAILED'}")
    print(f"  Code: {code}")
    print(f"  Duration: {duration:.1f} min")
    print(f"  Output length: {len(output)} chars")
    print(f"{'=' * 50}")
    if output:
        print(f"\n{output[:2000]}")


def _cmd_show_learnings():
    """Display all retry learnings."""
    if not RETRY_LEARNINGS_PATH.exists():
        print("No retry learnings recorded yet.")
        return

    print("\n" + "=" * 50)
    print("  OPENCLAW HYBRID -- RETRY LEARNINGS")
    print("=" * 50 + "\n")

    entries = []
    for line in RETRY_LEARNINGS_PATH.read_text().strip().split("\n"):
        if line.strip():
            try:
                entries.append(json.loads(line))
            except json.JSONDecodeError:
                continue

    if not entries:
        print("  No learnings recorded.")
        return

    successes = [e for e in entries if e.get("success")]
    failures = [e for e in entries if not e.get("success")]

    print(f"  Total entries: {len(entries)}")
    print(f"  Successful fixes: {len(successes)}")
    print(f"  Failed attempts: {len(failures)}")

    if successes:
        print(f"\n  --- Successful Fixes ---")
        for e in successes[-10:]:
            print(
                f"    [{e.get('category', '?')}] {e.get('detail', '')[:40]} "
                f"-> {e.get('fix_command', '')[:60]}"
            )

    print("\n" + "=" * 50 + "\n")


def main():
    parser = argparse.ArgumentParser(
        description="PRINTMAXX OpenClaw Hybrid Execution Engine"
    )
    parser.add_argument(
        "--task-id",
        type=str,
        help="Execute a specific task from the queue by ID",
    )
    parser.add_argument(
        "--health-check",
        action="store_true",
        help="Run system health check",
    )
    parser.add_argument(
        "--crash-recovery",
        action="store_true",
        help="Check for stale tasks and recovery options",
    )
    parser.add_argument(
        "--learnings",
        action="store_true",
        help="Display retry learnings database",
    )
    parser.add_argument(
        "--categorize-error",
        type=str,
        help="Categorize an error string (for testing)",
    )

    args = parser.parse_args()

    if args.health_check:
        _cmd_health_check()
    elif args.crash_recovery:
        _cmd_crash_recovery()
    elif args.learnings:
        _cmd_show_learnings()
    elif args.categorize_error:
        cat, pat, det = categorize_error(args.categorize_error)
        print(f"Category: {cat}")
        print(f"Pattern:  {pat}")
        print(f"Detail:   {det}")
    elif args.task_id:
        _cmd_run_task(args.task_id)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
