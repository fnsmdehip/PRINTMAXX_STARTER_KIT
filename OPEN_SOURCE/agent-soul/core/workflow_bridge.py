"""
Workflow Bridge -- Autonomous n8n workflow creation and management.

Programmatically creates, deploys, and manages n8n workflows via API.
No visual builder. No manual webhook registration. Agents detect when
a task needs a workflow and build it automatically.

Stdlib only (urllib). Auto-upgrades to httpx via deps.py if available.

Usage:
    from sovrun.core.workflow_bridge import (
        WorkflowBuilder, WorkflowManager, WorkflowDetector,
    )

    detector = WorkflowDetector()
    if detector.should_use_workflow("when new email arrives, extract data, add to sheet"):
        steps = detector.suggest_workflow("when new email arrives, extract data, add to sheet")
        builder = WorkflowBuilder()
        workflow_json = builder.build_workflow("email_to_sheet", "webhook", steps)
        manager = WorkflowManager()
        wf = manager.create(workflow_json)
        manager.activate(wf["id"])

CLI:
    python3 -m sovrun.core.workflow_bridge --detect "task description"
    python3 -m sovrun.core.workflow_bridge --build "when email, extract, add to sheet"
    python3 -m sovrun.core.workflow_bridge --create "name" --trigger webhook --steps "step1,step2"
    python3 -m sovrun.core.workflow_bridge --list
    python3 -m sovrun.core.workflow_bridge --status
    python3 -m sovrun.core.workflow_bridge --config URL API_KEY
"""
from __future__ import annotations

import argparse
import json
import logging
import os
import re
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Sequence

try:
    from .deps import get_http_client  # type: ignore[import-not-found]
except ImportError:
    from deps import get_http_client  # type: ignore[import-not-found, no-redef]

# ---------------------------------------------------------------------------
# Configurable paths
# ---------------------------------------------------------------------------
PROJECT_ROOT = Path(os.environ.get("SOVRUN_ROOT", Path.cwd()))
CONFIG_DIR = Path(os.environ.get("SOVRUN_CONFIG_DIR", PROJECT_ROOT / "config"))
LOGS_DIR = Path(os.environ.get("SOVRUN_LOGS_DIR", PROJECT_ROOT / "logs"))
WORKFLOW_LOG = LOGS_DIR / "workflows.jsonl"

logger = logging.getLogger("sovrun.workflow_bridge")


def _ensure_dir(p: Path) -> None:
    p.mkdir(parents=True, exist_ok=True)


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="milliseconds")


def _audit(event: str, **data: Any) -> None:
    """Append to JSONL audit trail."""
    _ensure_dir(WORKFLOW_LOG.parent)
    entry = {"ts": _now_iso(), "event": event, **data}
    try:
        with open(WORKFLOW_LOG, "a") as f:
            f.write(json.dumps(entry, default=str) + "\n")
    except OSError as exc:
        logger.warning("failed to write workflow audit: %s", exc)


# ---------------------------------------------------------------------------
# n8n config
# ---------------------------------------------------------------------------
N8N_CONFIG_FILE = CONFIG_DIR / "n8n.json"

_DEFAULT_CONFIG = {
    "base_url": "http://localhost:5678",
    "api_key": "",
}


def _load_config() -> dict[str, str]:
    if N8N_CONFIG_FILE.exists():
        try:
            return json.loads(N8N_CONFIG_FILE.read_text())
        except (json.JSONDecodeError, OSError):
            pass
    return dict(_DEFAULT_CONFIG)


def _save_config(cfg: dict[str, str]) -> None:
    _ensure_dir(N8N_CONFIG_FILE.parent)
    N8N_CONFIG_FILE.write_text(json.dumps(cfg, indent=2) + "\n")


# ---------------------------------------------------------------------------
# Node type registry -- maps step types to n8n node definitions
# ---------------------------------------------------------------------------

@dataclass
class StepDef:
    """Definition for a workflow step before it becomes an n8n node."""
    type: str
    name: str
    parameters: dict[str, Any] = field(default_factory=dict)


# Maps user-facing step type names to n8n node type strings and default params
_NODE_REGISTRY: dict[str, dict[str, Any]] = {
    "webhook": {
        "n8n_type": "n8n-nodes-base.webhook",
        "defaults": {
            "httpMethod": "POST",
            "path": "hook",
            "responseMode": "onReceived",
        },
    },
    "cron": {
        "n8n_type": "n8n-nodes-base.scheduleTrigger",
        "defaults": {
            "rule": {"interval": [{"field": "hours", "hoursInterval": 1}]},
        },
    },
    "http_request": {
        "n8n_type": "n8n-nodes-base.httpRequest",
        "defaults": {
            "method": "GET",
            "url": "",
            "responseFormat": "json",
        },
    },
    "code": {
        "n8n_type": "n8n-nodes-base.code",
        "defaults": {
            "language": "javaScript",
            "jsCode": "// process items\nreturn items;",
        },
    },
    "if": {
        "n8n_type": "n8n-nodes-base.if",
        "defaults": {
            "conditions": {
                "boolean": [{"value1": "={{$json.value}}", "value2": True}],
            },
        },
    },
    "switch": {
        "n8n_type": "n8n-nodes-base.switch",
        "defaults": {
            "rules": {"values": []},
        },
    },
    "set": {
        "n8n_type": "n8n-nodes-base.set",
        "defaults": {
            "mode": "manual",
            "duplicateItem": False,
            "assignments": {"assignments": []},
        },
    },
    "merge": {
        "n8n_type": "n8n-nodes-base.merge",
        "defaults": {
            "mode": "append",
        },
    },
    "email_send": {
        "n8n_type": "n8n-nodes-base.emailSend",
        "defaults": {
            "fromEmail": "",
            "toEmail": "",
            "subject": "",
            "text": "",
        },
    },
    "slack": {
        "n8n_type": "n8n-nodes-base.slack",
        "defaults": {
            "resource": "message",
            "operation": "post",
            "channel": "",
            "text": "",
        },
    },
    "spreadsheet": {
        "n8n_type": "n8n-nodes-base.spreadsheetFile",
        "defaults": {
            "operation": "append",
            "fileFormat": "csv",
        },
    },
    "google_sheets": {
        "n8n_type": "n8n-nodes-base.googleSheets",
        "defaults": {
            "operation": "appendOrUpdate",
            "documentId": "",
            "sheetName": "Sheet1",
        },
    },
    "llm_call": {
        "n8n_type": "n8n-nodes-base.executeCommand",
        "defaults": {
            "command": 'claude -p "{{prompt}}"',
        },
    },
    "llm_batch": {
        "n8n_type": "n8n-nodes-base.executeCommand",
        "defaults": {
            "command": 'echo \'{{prompt}}\' | claude --print',
        },
    },
}

# Trigger types (these can only be first node)
_TRIGGER_TYPES = {"webhook", "cron"}


# ---------------------------------------------------------------------------
# WorkflowBuilder
# ---------------------------------------------------------------------------

class WorkflowBuilder:
    """Programmatically generates n8n workflow JSON definitions.

    Takes a list of StepDef objects or simplified dicts and produces
    a complete n8n workflow JSON ready to POST to the API.
    """

    # n8n canvas layout constants
    _X_START = 250
    _X_SPACING = 200
    _Y_CENTER = 300

    def build_workflow(
        self,
        name: str,
        trigger_type: str,
        steps: Sequence[StepDef | dict[str, Any]],
    ) -> dict[str, Any]:
        """Create a valid n8n workflow JSON.

        Args:
            name: workflow name
            trigger_type: 'webhook' or 'cron'
            steps: list of StepDef or dicts with keys:
                   type (str), name (str), parameters (dict, optional)

        Returns:
            Complete n8n workflow JSON dict.
        """
        if trigger_type not in _TRIGGER_TYPES:
            raise ValueError(
                f"trigger_type must be one of {_TRIGGER_TYPES}, got '{trigger_type}'"
            )

        # Normalize steps to StepDef
        normalized: list[StepDef] = []
        for s in steps:
            if isinstance(s, StepDef):
                normalized.append(s)
            elif isinstance(s, dict):
                normalized.append(StepDef(
                    type=s.get("type", "code"),
                    name=s.get("name", f"step_{len(normalized)}"),
                    parameters=s.get("parameters", {}),
                ))
            else:
                raise TypeError(f"step must be StepDef or dict, got {type(s)}")

        # Build trigger node
        trigger_node = self._make_node(
            StepDef(type=trigger_type, name=f"{trigger_type}_trigger"),
            position_index=0,
        )

        # Build step nodes
        nodes = [trigger_node]
        for i, step_def in enumerate(normalized):
            if step_def.type in _TRIGGER_TYPES:
                raise ValueError(
                    f"Step '{step_def.name}' has trigger type '{step_def.type}'. "
                    "Triggers can only be the first node. Use trigger_type parameter."
                )
            node = self._make_node(step_def, position_index=i + 1)
            nodes.append(node)

        # Build connections: linear chain trigger -> step0 -> step1 -> ...
        connections: dict[str, Any] = {}
        for i in range(len(nodes) - 1):
            src_name = nodes[i]["name"]
            dst_name = nodes[i + 1]["name"]
            connections[src_name] = {
                "main": [[{"node": dst_name, "type": "main", "index": 0}]],
            }

        workflow = {
            "name": name,
            "nodes": nodes,
            "connections": connections,
            "active": False,
            "settings": {
                "executionOrder": "v1",
            },
        }

        _audit("workflow_built", name=name, trigger=trigger_type,
               step_count=len(normalized))

        return workflow

    def _make_node(self, step: StepDef, position_index: int) -> dict[str, Any]:
        """Convert a StepDef into an n8n node dict."""
        registry_entry = _NODE_REGISTRY.get(step.type)
        if registry_entry is None:
            raise ValueError(
                f"Unknown step type '{step.type}'. "
                f"Available: {sorted(_NODE_REGISTRY.keys())}"
            )

        # Merge defaults with user-provided parameters
        params = {**registry_entry["defaults"], **step.parameters}

        return {
            "name": step.name,
            "type": registry_entry["n8n_type"],
            "typeVersion": 1,
            "position": [
                self._X_START + (position_index * self._X_SPACING),
                self._Y_CENTER,
            ],
            "parameters": params,
        }


# ---------------------------------------------------------------------------
# WorkflowManager
# ---------------------------------------------------------------------------

class WorkflowManager:
    """Manages workflows on a running n8n instance via its REST API.

    All calls go through deps.get_http_client() which auto-upgrades
    to httpx when available, else falls back to urllib.
    """

    def __init__(self, base_url: str | None = None,
                 api_key: str | None = None) -> None:
        cfg = _load_config()
        self._base_url = (base_url or cfg.get("base_url", "")).rstrip("/")
        self._api_key = api_key or cfg.get("api_key", "")

        headers: dict[str, str] = {"Accept": "application/json"}
        if self._api_key:
            headers["X-N8N-API-KEY"] = self._api_key

        self._client = get_http_client(
            base_url=self._base_url,
            headers=headers,
            timeout=30.0,
        )

    def close(self) -> None:
        self._client.close()

    def __enter__(self) -> WorkflowManager:
        return self

    def __exit__(self, *args: Any) -> None:
        self.close()

    # -- API calls ---------------------------------------------------------

    def ping(self) -> dict[str, Any]:
        """Check n8n connectivity. Returns version info or error."""
        try:
            resp = self._client.get("/api/v1/workflows?limit=1")
            if resp.status_code == 200:
                return {"connected": True, "base_url": self._base_url}
            return {"connected": False, "status": resp.status_code,
                    "body": resp.text[:200]}
        except Exception as exc:
            return {"connected": False, "error": str(exc)}

    def create(self, workflow_json: dict[str, Any]) -> dict[str, Any]:
        """POST /api/v1/workflows -- create a new workflow.

        Returns the created workflow dict (includes 'id').
        """
        resp = self._client.post("/api/v1/workflows", json=workflow_json)
        resp.raise_for_status()
        result = resp.json()
        _audit("workflow_created", id=result.get("id"),
               name=workflow_json.get("name"))
        return result

    def activate(self, workflow_id: str) -> dict[str, Any]:
        """PATCH /api/v1/workflows/{id} -- set active=True."""
        resp = self._client.patch(
            f"/api/v1/workflows/{workflow_id}",
            json={"active": True},
        )
        resp.raise_for_status()
        _audit("workflow_activated", id=workflow_id)
        return resp.json()

    def deactivate(self, workflow_id: str) -> dict[str, Any]:
        """PATCH /api/v1/workflows/{id} -- set active=False."""
        resp = self._client.patch(
            f"/api/v1/workflows/{workflow_id}",
            json={"active": False},
        )
        resp.raise_for_status()
        _audit("workflow_deactivated", id=workflow_id)
        return resp.json()

    def trigger(self, workflow_id: str,
                payload: dict[str, Any] | None = None) -> dict[str, Any]:
        """POST to trigger a workflow via its webhook (test endpoint).

        Uses n8n's test webhook URL pattern. For production webhooks,
        use the webhook path directly.
        """
        resp = self._client.post(
            f"/api/v1/workflows/{workflow_id}/run",
            json=payload or {},
        )
        resp.raise_for_status()
        _audit("workflow_triggered", id=workflow_id)
        return resp.json()

    def list_workflows(self, limit: int = 100) -> list[dict[str, Any]]:
        """GET /api/v1/workflows -- list all workflows."""
        resp = self._client.get(f"/api/v1/workflows?limit={limit}")
        resp.raise_for_status()
        data = resp.json()
        # n8n wraps in {"data": [...]} or returns list directly
        if isinstance(data, dict) and "data" in data:
            return data["data"]
        if isinstance(data, list):
            return data
        return []

    def get_workflow(self, workflow_id: str) -> dict[str, Any]:
        """GET /api/v1/workflows/{id} -- get workflow details."""
        resp = self._client.get(f"/api/v1/workflows/{workflow_id}")
        resp.raise_for_status()
        return resp.json()

    def delete(self, workflow_id: str) -> bool:
        """DELETE /api/v1/workflows/{id}. Returns True on success."""
        resp = self._client.delete(f"/api/v1/workflows/{workflow_id}")
        resp.raise_for_status()
        _audit("workflow_deleted", id=workflow_id)
        return True

    def get_executions(self, workflow_id: str,
                       limit: int = 20) -> list[dict[str, Any]]:
        """GET /api/v1/executions -- execution history for a workflow."""
        resp = self._client.get(
            f"/api/v1/executions?workflowId={workflow_id}&limit={limit}",
        )
        resp.raise_for_status()
        data = resp.json()
        if isinstance(data, dict) and "data" in data:
            return data["data"]
        if isinstance(data, list):
            return data
        return []


# ---------------------------------------------------------------------------
# WorkflowDetector
# ---------------------------------------------------------------------------

# Pattern categories that indicate a task should be a workflow
_WORKFLOW_INDICATORS: list[tuple[str, list[str]]] = [
    ("trigger_response", [
        r"when\s+.+\s+(happens?|occurs?|arrives?|comes?\s+in)",
        r"on\s+(new|every|each)\s+",
        r"if\s+.+\s+then\s+",
        r"trigger\s+on\s+",
    ]),
    ("scheduled", [
        r"every\s+(hour|day|minute|week|morning|evening|night)",
        r"daily\s+at\s+",
        r"at\s+\d{1,2}(:\d{2})?\s*(am|pm)",
        r"cron\b",
        r"scheduled?\b",
        r"recurring\b",
        r"periodic(ally)?\b",
    ]),
    ("webhook", [
        r"webhook\b",
        r"listen\s+for\s+",
        r"receive\s+(data|payload|event)",
        r"incoming\s+(request|data|event)",
    ]),
    ("integration", [
        r"connect\s+.+\s+to\s+",
        r"pipe\s+(data\s+)?from\s+.+\s+to\s+",
        r"send\s+.+\s+to\s+(slack|email|sheet|discord)",
        r"sync\s+.+\s+(with|between)\s+",
        r"forward\s+.+\s+to\s+",
    ]),
    ("multi_step", [
        r"then\s+(do|send|check|process|add|update|create|post)",
        r"extract\s+.+\s+(and|then)\s+",
        r"transform\s+.+\s+(and|then)\s+",
        r"step\s+\d+",
        r"first\s+.+\s+then\s+",
    ]),
]

# Compiled patterns for performance
_COMPILED_INDICATORS: list[tuple[str, list[re.Pattern[str]]]] = [
    (cat, [re.compile(p, re.IGNORECASE) for p in patterns])
    for cat, patterns in _WORKFLOW_INDICATORS
]

# Step type inference from natural language
_STEP_PATTERNS: list[tuple[str, str, dict[str, Any]]] = [
    # pattern, step_type, default_params
    (r"(send|post)\s+(to\s+)?slack\b", "slack", {}),
    (r"(send|write)\s+(an?\s+)?email\b", "email_send", {}),
    (r"(add|append|write)\s+to\s+(spread)?sheet\b", "google_sheets", {}),
    (r"(add|append|write)\s+to\s+(csv|file)\b", "spreadsheet", {}),
    (r"(fetch|get|request|call|hit)\s+(url|api|endpoint|http)\b", "http_request", {}),
    (r"http\s+(get|post|put|patch|delete)\b", "http_request", {}),
    (r"(transform|process|convert|parse|calculate|compute|run\s+code)\b", "code", {}),
    (r"(extract|scrape|pull)\s+(data|info|text)\b", "code", {}),
    (r"(filter|check|validate|if|condition)\b", "if", {}),
    (r"(switch|route|branch)\b", "switch", {}),
    (r"(set|assign|define)\s+(data|field|value|variable)\b", "set", {}),
    (r"(combine|merge|join)\b", "merge", {}),
    (r"(llm|ai|claude|gpt|gemini|language\s+model|ask\s+ai|generate\s+text|summarize|analyze\s+with)\b", "llm_call", {}),
]

_COMPILED_STEP_PATTERNS: list[tuple[re.Pattern[str], str, dict[str, Any]]] = [
    (re.compile(p, re.IGNORECASE), step_type, defaults)
    for p, step_type, defaults in _STEP_PATTERNS
]


class WorkflowDetector:
    """Detects whether a task description should become an n8n workflow
    and suggests the step structure for it.
    """

    def __init__(self, threshold: int = 2) -> None:
        """
        Args:
            threshold: minimum number of indicator category matches
                       required to recommend a workflow. Default 2.
        """
        self.threshold = threshold

    def should_use_workflow(self, task_description: str) -> bool:
        """Return True if the task matches enough workflow indicator patterns.

        Checks across 5 categories: trigger/response, scheduled, webhook,
        integration, multi-step. A match in 2+ categories suggests a workflow.
        """
        matched_categories = self._match_categories(task_description)
        return len(matched_categories) >= self.threshold

    def analyze(self, task_description: str) -> dict[str, Any]:
        """Return detailed analysis of why a task should/shouldn't be a workflow."""
        matched = self._match_categories(task_description)
        should = len(matched) >= self.threshold
        steps = self.suggest_workflow(task_description) if should else []

        return {
            "task": task_description,
            "should_use_workflow": should,
            "matched_categories": list(matched),
            "category_count": len(matched),
            "threshold": self.threshold,
            "suggested_steps": [
                {"type": s.type, "name": s.name, "parameters": s.parameters}
                for s in steps
            ],
        }

    def suggest_workflow(self, task_description: str) -> list[StepDef]:
        """Parse a task description into a list of StepDef objects.

        Splits on common delimiters (comma, 'then', 'and then', semicolons)
        and matches each fragment against known step patterns.
        """
        # Split task into fragments
        fragments = re.split(
            r"\s*(?:,\s*(?:and\s+)?(?:then\s+)?|;\s*|\s+then\s+|\s+and\s+then\s+)\s*",
            task_description.strip(),
        )
        fragments = [f.strip() for f in fragments if f.strip()]

        steps: list[StepDef] = []
        for i, fragment in enumerate(fragments):
            step = self._classify_fragment(fragment, i)
            if step:
                steps.append(step)

        if not steps:
            # Fallback: single code step for unrecognized tasks
            steps.append(StepDef(
                type="code",
                name="process",
                parameters={"jsCode": f"// TODO: implement '{task_description}'\nreturn items;"},
            ))

        return steps

    def _match_categories(self, text: str) -> set[str]:
        matched: set[str] = set()
        for category, patterns in _COMPILED_INDICATORS:
            for pattern in patterns:
                if pattern.search(text):
                    matched.add(category)
                    break
        return matched

    def _classify_fragment(self, fragment: str, index: int) -> StepDef | None:
        """Classify a text fragment into a StepDef."""
        # Clean up fragment
        clean = fragment.strip().rstrip(".")

        for pattern, step_type, defaults in _COMPILED_STEP_PATTERNS:
            if pattern.search(clean):
                # Generate a readable name from the fragment
                name = self._fragment_to_name(clean, index)
                return StepDef(
                    type=step_type,
                    name=name,
                    parameters=dict(defaults),
                )

        # Unmatched fragments become code steps
        if clean and len(clean) > 3:
            return StepDef(
                type="code",
                name=self._fragment_to_name(clean, index),
                parameters={
                    "jsCode": f"// {clean}\nreturn items;",
                },
            )
        return None

    @staticmethod
    def _fragment_to_name(fragment: str, index: int) -> str:
        """Convert a natural language fragment to a valid node name."""
        # Take first few meaningful words
        words = re.findall(r"[a-zA-Z]+", fragment.lower())
        words = [w for w in words if w not in {
            "the", "a", "an", "to", "from", "in", "on", "at", "for",
            "and", "or", "of", "is", "it", "do", "if", "by", "with",
        }]
        name_words = words[:3] if words else [f"step"]
        name = "_".join(name_words)
        # Ensure uniqueness via index suffix
        return f"{name}_{index}"


# ---------------------------------------------------------------------------
# Convenience: auto-create
# ---------------------------------------------------------------------------

def auto_create_workflow(
    task_description: str,
    name: str | None = None,
    activate: bool = True,
    trigger_type: str = "webhook",
) -> dict[str, Any] | None:
    """One-call workflow creation from a task description.

    Returns the created workflow dict from n8n, or None if the task
    doesn't warrant a workflow.

    Args:
        task_description: natural language description of the automation
        name: workflow name (auto-generated from task if omitted)
        activate: whether to activate after creation
        trigger_type: 'webhook' or 'cron'
    """
    detector = WorkflowDetector()
    if not detector.should_use_workflow(task_description):
        return None

    steps = detector.suggest_workflow(task_description)
    if not steps:
        return None

    # Auto-generate name from task
    if not name:
        words = re.findall(r"[a-zA-Z]+", task_description.lower())
        meaningful = [w for w in words if len(w) > 2 and w not in {
            "the", "and", "then", "when", "from", "that", "this", "with",
        }]
        name = "_".join(meaningful[:4]) or "auto_workflow"

    builder = WorkflowBuilder()
    workflow_json = builder.build_workflow(name, trigger_type, steps)

    try:
        with WorkflowManager() as manager:
            created = manager.create(workflow_json)
            wf_id = created.get("id", "")
            if activate and wf_id:
                manager.activate(wf_id)
            _audit("auto_create_complete", id=wf_id, name=name,
                   task=task_description, activated=activate)
            return created
    except Exception as exc:
        _audit("auto_create_failed", name=name, task=task_description,
               error=str(exc))
        logger.error("auto_create_workflow failed: %s", exc)
        return None


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def _cli_detect(task: str) -> None:
    detector = WorkflowDetector()
    analysis = detector.analyze(task)

    print(f"\n=== Workflow Detection ===\n")
    print(f"  Task: {task}")
    print(f"  Should use workflow: {'YES' if analysis['should_use_workflow'] else 'NO'}")
    print(f"  Matched categories: {analysis['category_count']}/{detector.threshold} needed")
    if analysis["matched_categories"]:
        for cat in analysis["matched_categories"]:
            print(f"    - {cat}")
    if analysis["suggested_steps"]:
        print(f"\n  Suggested steps ({len(analysis['suggested_steps'])}):")
        for s in analysis["suggested_steps"]:
            print(f"    [{s['type']:15s}] {s['name']}")
    print()


def _cli_build(task: str) -> None:
    detector = WorkflowDetector()
    steps = detector.suggest_workflow(task)

    # Infer trigger type
    trigger = "cron" if re.search(r"every\s+(hour|day|minute|week)", task, re.I) else "webhook"

    # Auto name
    words = re.findall(r"[a-zA-Z]+", task.lower())
    meaningful = [w for w in words if len(w) > 2]
    name = "_".join(meaningful[:4]) or "workflow"

    builder = WorkflowBuilder()
    workflow_json = builder.build_workflow(name, trigger, steps)

    print(json.dumps(workflow_json, indent=2))


def _cli_create(name: str, trigger: str, steps_csv: str) -> None:
    # Parse comma-separated step descriptions into StepDefs
    detector = WorkflowDetector()
    step_fragments = [s.strip() for s in steps_csv.split(",") if s.strip()]

    step_defs: list[StepDef] = []
    for i, frag in enumerate(step_fragments):
        classified = detector._classify_fragment(frag, i)
        if classified:
            step_defs.append(classified)
        else:
            step_defs.append(StepDef(type="code", name=f"step_{i}"))

    builder = WorkflowBuilder()
    workflow_json = builder.build_workflow(name, trigger, step_defs)

    try:
        with WorkflowManager() as manager:
            result = manager.create(workflow_json)
            wf_id = result.get("id", "?")
            manager.activate(wf_id)
            print(f"\nCreated and activated workflow: {name} (id={wf_id})\n")
    except Exception as exc:
        print(f"\nFailed to create workflow on n8n: {exc}")
        print("Workflow JSON (use with n8n import):")
        print(json.dumps(workflow_json, indent=2))


def _cli_list() -> None:
    try:
        with WorkflowManager() as manager:
            workflows = manager.list_workflows()
    except Exception as exc:
        print(f"\nFailed to connect to n8n: {exc}\n")
        return

    print(f"\n=== n8n Workflows ({len(workflows)}) ===\n")
    if not workflows:
        print("  (none)")
    for wf in workflows:
        active = "ACTIVE" if wf.get("active") else "INACTIVE"
        wf_id = wf.get("id", "?")
        name = wf.get("name", "untitled")
        nodes = len(wf.get("nodes", []))
        print(f"  [{active:8s}] id={wf_id:6s}  {name} ({nodes} nodes)")
    print()


def _cli_status() -> None:
    cfg = _load_config()
    print(f"\n=== n8n Connection Status ===\n")
    print(f"  Base URL: {cfg.get('base_url', '(not set)')}")
    print(f"  API Key:  {'****' + cfg.get('api_key', '')[-4:] if cfg.get('api_key') else '(not set)'}")

    try:
        with WorkflowManager() as manager:
            ping = manager.ping()
        if ping.get("connected"):
            print(f"  Status:   CONNECTED")
        else:
            err = ping.get("error") or ping.get("body", "unknown error")
            print(f"  Status:   DISCONNECTED ({err})")
    except Exception as exc:
        print(f"  Status:   DISCONNECTED ({exc})")
    print()


def _cli_config(url: str, api_key: str) -> None:
    cfg = {"base_url": url, "api_key": api_key}
    _save_config(cfg)
    print(f"\nSaved n8n config to {N8N_CONFIG_FILE}")
    print(f"  Base URL: {url}")
    print(f"  API Key:  {'****' + api_key[-4:] if api_key else '(not set)'}\n")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Workflow Bridge -- autonomous n8n workflow creation",
    )
    parser.add_argument("--detect", metavar="TASK",
                        help="Check if a task should be a workflow")
    parser.add_argument("--build", metavar="TASK",
                        help="Generate workflow JSON from task description")
    parser.add_argument("--create", metavar="NAME",
                        help="Create workflow on n8n (use with --trigger, --steps)")
    parser.add_argument("--trigger", default="webhook",
                        choices=["webhook", "cron"],
                        help="Trigger type for --create (default: webhook)")
    parser.add_argument("--steps", metavar="CSV",
                        help="Comma-separated step descriptions for --create")
    parser.add_argument("--list", action="store_true",
                        help="List workflows on n8n instance")
    parser.add_argument("--status", action="store_true",
                        help="Show n8n connection status")
    parser.add_argument("--config", nargs=2, metavar=("URL", "API_KEY"),
                        help="Set n8n connection config")
    args = parser.parse_args()

    has_action = any([
        args.detect, args.build, args.create,
        args.list, args.status, args.config,
    ])
    if not has_action:
        parser.print_help()
        return

    if args.config:
        _cli_config(args.config[0], args.config[1])

    if args.detect:
        _cli_detect(args.detect)

    if args.build:
        _cli_build(args.build)

    if args.create:
        if not args.steps:
            print("--create requires --steps (comma-separated step descriptions)")
            return
        _cli_create(args.create, args.trigger, args.steps)

    if args.list:
        _cli_list()

    if args.status:
        _cli_status()


if __name__ == "__main__":
    main()
