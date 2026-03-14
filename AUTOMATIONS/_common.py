"""Shared utilities for PRINTMAXX automation scripts."""
from __future__ import annotations
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Optional
import json

PROJECT = Path(__file__).resolve().parent.parent

def safe_path(target: str | Path) -> Path:
    """Verify path is within project root. Raises ValueError if not."""
    resolved = Path(target).resolve()
    if not str(resolved).startswith(str(PROJECT)):
        raise ValueError(f"BLOCKED: {resolved} is outside project root {PROJECT}")
    return resolved

def ts() -> str:
    """Timestamp string for logging."""
    return datetime.now().strftime("%H:%M:%S")

def log(msg: str, level: str = "INFO", tag: str = "SYSTEM") -> None:
    """Prefixed log line."""
    print(f"[{ts()}] [{tag}] [{level}] {msg}")

def load_json(path: str | Path, default: Any = None) -> Any:
    """Load JSON file safely. Returns default (or {}) on any error."""
    if default is None:
        default = {}
    try:
        return json.loads(Path(path).read_text())
    except Exception:
        return default

def hours_since(iso_timestamp: str) -> float:
    """Hours elapsed since an ISO timestamp. Returns inf on parse failure."""
    try:
        dt = datetime.fromisoformat(iso_timestamp.replace("Z", "+00:00"))
        if dt.tzinfo:
            dt = dt.replace(tzinfo=None)
        return (datetime.now() - dt).total_seconds() / 3600
    except Exception:
        return float("inf")

def run_script(script_name: str, args: list[str] | None = None, timeout: int = 60) -> tuple[bool, str]:
    """Run an AUTOMATIONS script via subprocess. Returns (success, output)."""
    import subprocess
    cmd = ["python3", str(PROJECT / "AUTOMATIONS" / script_name)]
    if args:
        cmd.extend(args)
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout, cwd=str(PROJECT))
        return r.returncode == 0, r.stdout.strip()
    except subprocess.TimeoutExpired:
        return False, f"TIMEOUT after {timeout}s"
    except Exception as e:
        return False, str(e)

SOUL_PATH = PROJECT / "AUTOMATIONS" / "SOUL.md"

def get_soul(max_chars: int = 2000) -> str:
    """Read SOUL.md behavioral directives. Returns empty string if missing."""
    try:
        return SOUL_PATH.read_text(encoding="utf-8")[:max_chars]
    except Exception:
        return ""

VENTURES = ["CONTENT", "OUTBOUND", "APP_FACTORY", "LOCAL_BIZ", "MONETIZATION", "PRODUCT", "RESEARCH", "SCRAPING"]

VENTURE_NAMES = {
    "CONTENT": "Content Farm & Distribution",
    "OUTBOUND": "Cold Email & Outbound",
    "APP_FACTORY": "App Factory (PWAs & Mobile)",
    "LOCAL_BIZ": "Local Business Pipeline",
    "MONETIZATION": "Revenue & Monetization",
    "PRODUCT": "Digital Products",
    "RESEARCH": "Alpha Research & Intelligence",
    "SCRAPING": "Competitive Intel Scrapers",
}
