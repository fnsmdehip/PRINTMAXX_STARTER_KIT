"""
Resilience -- Shared module for crash-proof AI agents.

Provides:
- retry with exponential backoff + jitter
- file locking (fcntl advisory locks)
- circuit breaker (CLOSED > OPEN > HALF_OPEN > CLOSED)
- input sanitization for prompt injection defense
- trajectory logging (append-only JSONL audit trail)

Stdlib only. No external dependencies.

Import and use across all your agents to make them production-grade.

Usage:
    from sovrun.core.resilience import retry, locked_file, CircuitBreaker
    from sovrun.core.resilience import sanitize_for_prompt, TrajectoryLogger
"""
from __future__ import annotations

import fcntl
import functools
import json
import logging
import os
import random
import re
import time
from contextlib import contextmanager
from datetime import datetime, timezone
from io import TextIOWrapper
from pathlib import Path
from typing import Any, Callable, Generator, TypeVar

# ---------------------------------------------------------------------------
# Configurable paths
# ---------------------------------------------------------------------------
PROJECT_ROOT = Path(os.environ.get("SOVRUN_ROOT", Path.cwd()))
LOCKS_DIR = Path(os.environ.get("SOVRUN_LOCKS_DIR", PROJECT_ROOT / "state" / "locks"))
LOGS_DIR = Path(os.environ.get("SOVRUN_LOGS_DIR", PROJECT_ROOT / "logs"))
TRAJECTORY_DIR = LOGS_DIR / "trajectory"
CB_STATE_FILE = LOCKS_DIR / "circuit_breaker_state.json"

_T = TypeVar("_T")
logger = logging.getLogger("sovrun.resilience")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def safe_path(target: str | Path) -> Path:
    """Verify target resolves inside PROJECT_ROOT."""
    resolved = Path(target).resolve()
    root = PROJECT_ROOT.resolve()
    if not str(resolved).startswith(str(root)):
        raise ValueError(f"BLOCKED: {resolved} outside {root}")
    return resolved


def _ensure_dir(p: Path) -> None:
    p.mkdir(parents=True, exist_ok=True)


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="milliseconds")


def _ts() -> float:
    return time.time()


# ---------------------------------------------------------------------------
# 1. Retry with exponential backoff + jitter
# ---------------------------------------------------------------------------

def retry(max_attempts: int = 5, base_delay: float = 2.0,
          on_failure_return: Any = "") -> Callable[..., Any]:
    """Decorator: retry N times with exponential backoff.
    On final failure, logs error and returns on_failure_return."""
    def decorator(fn: Callable[..., _T]) -> Callable[..., _T | Any]:
        @functools.wraps(fn)
        def wrapper(*args: Any, **kwargs: Any) -> _T | Any:
            last_exc: BaseException | None = None
            for attempt in range(max_attempts):
                try:
                    return fn(*args, **kwargs)
                except Exception as exc:
                    last_exc = exc
                    if attempt < max_attempts - 1:
                        delay = (base_delay ** (attempt + 1)) + random.uniform(0, base_delay ** attempt)
                        logger.warning("retry %d/%d for %s: %s (wait %.2fs)",
                                       attempt + 1, max_attempts, fn.__name__, exc, delay)
                        time.sleep(delay)
            logger.error("FINAL FAILURE after %d attempts for %s: %s",
                         max_attempts, fn.__name__, last_exc)
            return on_failure_return
        return wrapper
    return decorator


# ---------------------------------------------------------------------------
# 2. File locking (fcntl advisory locks)
# ---------------------------------------------------------------------------

_LOCK_TIMEOUT: int = 30
_STALE_LOCK_AGE: int = 300  # 5 minutes


def _lock_path_for(target: str | Path) -> Path:
    _ensure_dir(LOCKS_DIR)
    return LOCKS_DIR / (Path(target).resolve().name + ".lock")


def _cleanup_stale_locks() -> None:
    if not LOCKS_DIR.exists():
        return
    cutoff = _ts() - _STALE_LOCK_AGE
    for lf in LOCKS_DIR.glob("*.lock"):
        try:
            if lf.stat().st_mtime < cutoff:
                lf.unlink(missing_ok=True)
                logger.info("cleaned stale lock %s", lf.name)
        except OSError:
            pass


def _acquire(lf: Any, timeout: int) -> bool:
    deadline = _ts() + timeout
    while _ts() < deadline:
        try:
            fcntl.flock(lf, fcntl.LOCK_EX | fcntl.LOCK_NB)
            return True
        except BlockingIOError:
            time.sleep(0.1)
    return False


@contextmanager
def locked_file(target: str | Path, mode: str = "r+",
                timeout: int = _LOCK_TIMEOUT) -> Generator[TextIOWrapper, None, None]:
    """Open target with an advisory flock. Auto-cleans stale locks > 5 min."""
    _cleanup_stale_locks()
    target_path = Path(target)
    lf = open(_lock_path_for(target_path), "w")
    acquired = False
    try:
        acquired = _acquire(lf, timeout)
        if not acquired:
            raise TimeoutError(f"Could not acquire lock for {target_path} within {timeout}s")
        if not target_path.exists():
            target_path.touch()
        with open(target_path, mode) as f:
            yield f  # type: ignore[misc]
    finally:
        if acquired:
            fcntl.flock(lf, fcntl.LOCK_UN)
        lf.close()


def file_lock(target: str | Path) -> Callable[..., Any]:
    """Decorator: wrap the function body with an advisory file lock."""
    def decorator(fn: Callable[..., _T]) -> Callable[..., _T]:
        @functools.wraps(fn)
        def wrapper(*args: Any, **kwargs: Any) -> _T:
            _cleanup_stale_locks()
            lf = open(_lock_path_for(target), "w")
            acquired = False
            try:
                acquired = _acquire(lf, _LOCK_TIMEOUT)
                if not acquired:
                    raise TimeoutError(f"Lock timeout for {target} ({_LOCK_TIMEOUT}s)")
                return fn(*args, **kwargs)
            finally:
                if acquired:
                    fcntl.flock(lf, fcntl.LOCK_UN)
                lf.close()
        return wrapper
    return decorator


# ---------------------------------------------------------------------------
# 3. Circuit breaker
# ---------------------------------------------------------------------------

class CircuitBreakerOpen(Exception):
    """Raised when the circuit breaker is OPEN."""


class CircuitBreaker:
    """CLOSED > OPEN (after N failures in window) > HALF_OPEN (probe) > CLOSED.
    State persisted to disk for crash recovery."""

    CLOSED: str = "CLOSED"
    OPEN: str = "OPEN"
    HALF_OPEN: str = "HALF_OPEN"

    def __init__(self, name: str = "default", failure_threshold: int = 3,
                 recovery_timeout: int = 60, window: int = 300) -> None:
        self.name = name
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.window = window
        self._state: str = self.CLOSED
        self._failures: list[float] = []
        self._opened_at: float = 0.0
        _ensure_dir(LOCKS_DIR)
        self._load()

    def _key(self) -> str:
        return f"cb_{self.name}"

    def _load(self) -> None:
        if not CB_STATE_FILE.exists():
            return
        try:
            mine = json.loads(CB_STATE_FILE.read_text()).get(self._key(), {})
            self._state = mine.get("state", self.CLOSED)
            self._failures = mine.get("failures", [])
            self._opened_at = mine.get("opened_at", 0.0)
        except (json.JSONDecodeError, OSError):
            pass

    def _save(self) -> None:
        data: dict[str, Any] = {}
        if CB_STATE_FILE.exists():
            try:
                data = json.loads(CB_STATE_FILE.read_text())
            except (json.JSONDecodeError, OSError):
                pass
        data[self._key()] = {"state": self._state, "failures": self._failures,
                             "opened_at": self._opened_at}
        CB_STATE_FILE.write_text(json.dumps(data, indent=2))

    def _maybe_transition(self) -> None:
        if self._state == self.OPEN and _ts() - self._opened_at >= self.recovery_timeout:
            self._state = self.HALF_OPEN
            self._save()

    @property
    def state(self) -> str:
        self._maybe_transition()
        return self._state

    def record_failure(self) -> None:
        now = _ts()
        self._failures = [t for t in self._failures if now - t < self.window]
        self._failures.append(now)
        if len(self._failures) >= self.failure_threshold:
            self._state, self._opened_at = self.OPEN, now
            logger.warning("circuit breaker '%s' OPEN after %d failures",
                           self.name, len(self._failures))
        self._save()

    def record_success(self) -> None:
        self._failures.clear()
        self._state = self.CLOSED
        self._save()

    def __enter__(self) -> CircuitBreaker:
        self._maybe_transition()
        if self._state == self.OPEN:
            logger.warning("circuit breaker '%s' open, skipping", self.name)
            raise CircuitBreakerOpen(self.name)
        return self

    def __exit__(self, exc_type: type | None, _exc_val: BaseException | None,
                 _exc_tb: Any) -> bool:
        if exc_type is not None and exc_type is not CircuitBreakerOpen:
            self.record_failure()
        elif exc_type is None:
            self.record_success()
        return False


# ---------------------------------------------------------------------------
# 4. Input sanitization (prompt injection defense)
# ---------------------------------------------------------------------------

_INJECTION_PATTERNS: list[re.Pattern[str]] = [re.compile(p, re.I | re.M) for p in [
    r"ignore\s+(all\s+)?previous\s+instructions",
    r"ignore\s+(all\s+)?prior\s+instructions",
    r"disregard\s+(all\s+)?(previous|prior|above)\s+instructions",
    r"you\s+are\s+now\s+", r"new\s+instructions?:",
    r"override\s+(all\s+)?instructions",
    r"^\s*system\s*:", r"^\s*assistant\s*:", r"^\s*user\s*:",
    r"<\s*/?\s*(system|instructions?|prompt|context|rules?)\s*>",
    r"\[INST\]", r"<<\s*SYS\s*>>",
]]
_MAX_FIELD_LEN: int = 10_000


def sanitize_for_prompt(text: str | Any, field_name: str = "input") -> str:
    """Strip prompt-injection patterns from external content before using in prompts.
    Removes injection phrases, XML-like breakout tags, truncates to 10K chars."""
    if not isinstance(text, str):
        return ""
    original_len, cleaned = len(text), text
    for pat in _INJECTION_PATTERNS:
        m = pat.search(cleaned)
        if m:
            logger.warning("sanitize[%s]: stripped %r", field_name, m.group())
            cleaned = pat.sub("", cleaned)
    if len(cleaned) > _MAX_FIELD_LEN:
        logger.warning("sanitize[%s]: truncated %d -> %d chars",
                        field_name, original_len, _MAX_FIELD_LEN)
        cleaned = cleaned[:_MAX_FIELD_LEN]
    return cleaned


# ---------------------------------------------------------------------------
# 5. Trajectory logger
# ---------------------------------------------------------------------------

class TrajectoryLogger:
    """Append-only JSONL trajectory log per agent.
    Writes to logs/trajectory/{agent_name}.jsonl."""

    def __init__(self, agent_name: str) -> None:
        self.agent_name = agent_name
        _ensure_dir(TRAJECTORY_DIR)
        self._path: Path = TRAJECTORY_DIR / f"{agent_name}.jsonl"

    def _write(self, entry: dict[str, Any]) -> None:
        entry.setdefault("timestamp", _now_iso())
        entry.setdefault("agent", self.agent_name)
        with open(self._path, "a") as f:
            f.write(json.dumps(entry, default=str) + "\n")

    def log_attempt(self, action: str, **extra: Any) -> float:
        """Log an attempt; returns start timestamp for duration tracking."""
        start = _ts()
        self._write({"action": action, "result": "attempt", **extra})
        return start

    def log_success(self, action: str, start: float = 0.0, **extra: Any) -> None:
        dur = int((_ts() - start) * 1000) if start else 0
        self._write({"action": action, "result": "success", "duration_ms": dur, **extra})

    def log_failure(self, action: str, error: str = "",
                    start: float = 0.0, **extra: Any) -> None:
        dur = int((_ts() - start) * 1000) if start else 0
        self._write({"action": action, "result": "failure",
                     "error": error, "duration_ms": dur, **extra})


# ---------------------------------------------------------------------------
# Exports
# ---------------------------------------------------------------------------
__all__ = ["retry", "file_lock", "locked_file", "CircuitBreaker",
           "CircuitBreakerOpen", "sanitize_for_prompt", "TrajectoryLogger",
           "safe_path", "PROJECT_ROOT"]
