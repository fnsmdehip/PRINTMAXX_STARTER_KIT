"""Shared utilities for PRINTMAXX automation scripts."""
from __future__ import annotations
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Optional
import json
import sys

PROJECT = Path(__file__).resolve().parent.parent

# Sovrun modules (our open-source agent OS)
_SOVRUN_PATH = str(PROJECT / "OPEN_SOURCE" / "agent-soul")
if _SOVRUN_PATH not in sys.path:
    sys.path.insert(0, _SOVRUN_PATH)

# Lazy sovrun imports — graceful fallback if not available
_SOVRUN_AVAILABLE = False
try:
    from core.handoff import HandoffRouter, HandoffRequest, HandoffResult, GuardrailScope
    from core.procedural_memory import ProceduralMemory
    from core.orchestration import DAGOrchestrator, AgentStep, StepStatus, step as sovrun_step
    from core.workflow_bridge import WorkflowDetector, WorkflowBuilder, WorkflowManager
    from core.conversation_index import ConversationIndex
    from core.tracing import Tracer, TraceEvent
    _SOVRUN_AVAILABLE = True
except ImportError:
    HandoffRouter = None  # type: ignore[assignment, misc]
    HandoffRequest = None  # type: ignore[assignment, misc]
    HandoffResult = None  # type: ignore[assignment, misc]
    GuardrailScope = None  # type: ignore[assignment, misc]
    ProceduralMemory = None  # type: ignore[assignment, misc]
    DAGOrchestrator = None  # type: ignore[assignment, misc]
    AgentStep = None  # type: ignore[assignment, misc]
    StepStatus = None  # type: ignore[assignment, misc]
    sovrun_step = None  # type: ignore[assignment, misc]
    WorkflowDetector = None  # type: ignore[assignment, misc]
    WorkflowBuilder = None  # type: ignore[assignment, misc]
    WorkflowManager = None  # type: ignore[assignment, misc]
    ConversationIndex = None  # type: ignore[assignment, misc]
    Tracer = None  # type: ignore[assignment, misc]
    TraceEvent = None  # type: ignore[assignment, misc]


def sovrun_available() -> bool:
    """Check if sovrun modules are importable."""
    return _SOVRUN_AVAILABLE


def get_procedural_memory() -> Any:
    """Get a ProceduralMemory instance pointed at PRINTMAXX data dir.

    Returns None if sovrun is not available.
    """
    if not _SOVRUN_AVAILABLE or ProceduralMemory is None:
        return None
    import os
    os.environ.setdefault("SOVRUN_ROOT", str(PROJECT))
    db_path = PROJECT / "AUTOMATIONS" / "agent" / "sovrun" / "skills.db"
    db_path.parent.mkdir(parents=True, exist_ok=True)
    return ProceduralMemory(db_path=db_path)


def get_handoff_router() -> Any:
    """Get a HandoffRouter instance for PRINTMAXX.

    Returns None if sovrun is not available.
    """
    if not _SOVRUN_AVAILABLE or HandoffRouter is None:
        return None
    import os
    os.environ.setdefault("SOVRUN_ROOT", str(PROJECT))
    log_path = PROJECT / "AUTOMATIONS" / "agent" / "sovrun" / "handoffs.jsonl"
    log_path.parent.mkdir(parents=True, exist_ok=True)
    return HandoffRouter(log_path=log_path)


def recall_skills_for_task(task_description: str, max_chars: int = 600) -> str:
    """Query procedural memory for relevant skills before an agent runs.

    Returns injection string or empty string if unavailable.
    """
    mem = get_procedural_memory()
    if mem is None:
        return ""
    try:
        return mem.export_injection(task_description, max_chars=max_chars)
    except Exception:
        return ""
    finally:
        mem.close()


def capture_skill_from_result(task: str, result: str, success: bool = True) -> None:
    """Capture a completed task as a skill document in procedural memory."""
    mem = get_procedural_memory()
    if mem is None:
        return
    try:
        mem.capture(task=task, result=result, success=success)
    except Exception:
        pass
    finally:
        mem.close()

def get_workflow_detector() -> Any:
    """Get a WorkflowDetector instance.

    Returns None if sovrun is not available.
    """
    if not _SOVRUN_AVAILABLE or WorkflowDetector is None:
        return None
    return WorkflowDetector()


def get_conversation_index() -> Any:
    """Get a ConversationIndex pointed at PRINTMAXX conversation data.

    Returns None if sovrun is not available.
    """
    if not _SOVRUN_AVAILABLE or ConversationIndex is None:
        return None
    import os
    os.environ.setdefault("SOVRUN_ROOT", str(PROJECT))
    db_path = PROJECT / "AUTOMATIONS" / "agent" / "sovrun" / "conversations.db"
    conv_file = PROJECT / "LEDGER" / "CONVERSATION_HISTORY.jsonl"
    db_path.parent.mkdir(parents=True, exist_ok=True)
    return ConversationIndex(db_path=db_path, conversation_file=conv_file)


def get_tracer(agent_name: str = "printmaxx") -> Any:
    """Get a Tracer instance for agent observability.

    Returns None if sovrun is not available.
    """
    if not _SOVRUN_AVAILABLE or Tracer is None:
        return None
    import os
    os.environ.setdefault("SOVRUN_ROOT", str(PROJECT))
    traces_dir = PROJECT / "AUTOMATIONS" / "logs" / "traces"
    traces_dir.mkdir(parents=True, exist_ok=True)
    os.environ.setdefault("SOVRUN_TRACES_DIR", str(traces_dir))
    return Tracer()


def search_conversations(query: str, top_k: int = 10) -> list:
    """Search conversation history via FTS5 index.

    Returns list of matching entries or empty list if unavailable.
    """
    idx = get_conversation_index()
    if idx is None:
        return []
    try:
        return idx.search(query, top_k=top_k)
    except Exception:
        return []


def should_use_workflow(task_description: str) -> bool:
    """Check if a task should be routed to an n8n workflow.

    Returns False if sovrun is not available or detection fails.
    """
    detector = get_workflow_detector()
    if detector is None:
        return False
    try:
        return detector.should_use_workflow(task_description)
    except Exception:
        return False


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

VOICE_MODEL_PATH = PROJECT / "OPS" / "USER_VOICE_MODEL.json"

def get_voice_model(max_chars: int = 500) -> str:
    """Get compact user voice model for agent injection.

    Reads OPS/USER_VOICE_MODEL.json and returns a structured injection string
    with style summary, banned patterns, and recurring instructions. Agents
    prepend this to prompts so their output matches the user's voice.
    """
    try:
        model = json.loads(VOICE_MODEL_PATH.read_text(encoding="utf-8"))
        summary = model.get("style_summary", "")
        if not summary:
            return ""
        parts = [f"VOICE: {summary}"]
        banned = model.get("banned_patterns", [])[:8]
        if banned:
            parts.append(f"NEVER SAY: {', '.join(banned[:8])}")
        instructions = model.get("recurring_instructions", [])[:3]
        if instructions:
            parts.append(f"RULES: {'; '.join(instructions[:3])}")
        injection = " | ".join(parts)
        return injection[:max_chars]
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

# --- Media generation (sovrun) ---
try:
    from core.media import MediaRouter  # type: ignore
    _MEDIA_ROUTER = MediaRouter(budget_tier="low")
except ImportError:
    _MEDIA_ROUTER = None

def get_media_router():
    return _MEDIA_ROUTER

def generate_image(prompt, **kwargs):
    if _MEDIA_ROUTER:
        return _MEDIA_ROUTER.generate_image(prompt, **kwargs)
    return None

def generate_thumbnail(title, **kwargs):
    if _MEDIA_ROUTER:
        return _MEDIA_ROUTER.generate_thumbnail(title, **kwargs)
    return None

def text_to_speech(text, **kwargs):
    if _MEDIA_ROUTER:
        return _MEDIA_ROUTER.text_to_speech(text, **kwargs)
    return None

# --- External tool integrations (sovrun connector registry) ---
# These tools are available via connectors/registry.json
# Install with: python3 OPEN_SOURCE/agent-soul/connectors/setup.py --connect TOOL_NAME

AVAILABLE_TOOLS = {
    "crawl4ai": {"pip": "crawl4ai", "use_for": "LLM-friendly web crawling for generic URLs", "ventures": "intelligence pipeline, alpha scraping"},
    "postiz": {"docker": "ghcr.io/gitroomhq/postiz-app", "use_for": "30+ platform post scheduling", "ventures": "C01-C18 content"},
    "polar": {"pip": "polar-sdk", "use_for": "self-hosted payments (replaces Gumroad)", "ventures": "D01-D12 digital products"},
    "listmonk": {"docker": "listmonk/listmonk", "use_for": "self-hosted newsletter", "ventures": "N12 newsletter, C05 pipeline"},
    "freqtrade": {"docker": "freqtradeorg/freqtrade", "use_for": "crypto trading backtesting", "ventures": "I01-I05 investment"},
    "mautic": {"docker": "mautic/mautic", "use_for": "marketing automation + CRM for EAS clients", "ventures": "S02 EAS"},
}

def get_available_tools():
    """Return dict of available external tools and what they're for."""
    return AVAILABLE_TOOLS

def suggest_tools_for_task(task_description):
    """Suggest which external tools could help with a task."""
    task_lower = task_description.lower()
    suggestions = []
    keywords = {
        "crawl4ai": ["crawl", "scrape", "website", "extract", "url"],
        "postiz": ["post", "schedule", "social", "publish", "distribute"],
        "polar": ["payment", "sell", "product", "gumroad", "checkout", "subscription"],
        "listmonk": ["newsletter", "email list", "subscriber", "email campaign"],
        "freqtrade": ["trade", "crypto", "backtest", "exchange", "bitcoin"],
        "mautic": ["crm", "lead nurture", "marketing automation", "contact"],
    }
    for tool, kws in keywords.items():
        if any(kw in task_lower for kw in kws):
            suggestions.append({"tool": tool, **AVAILABLE_TOOLS[tool]})
    return suggestions
