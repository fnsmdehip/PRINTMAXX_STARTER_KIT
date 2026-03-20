"""
Base classes for all media providers.
"""
from __future__ import annotations

import json
import logging
import os
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

logger = logging.getLogger("sovrun.media")

MEDIA_DIR = Path(os.environ.get("SOVRUN_MEDIA_DIR", Path.cwd() / "media_output"))
AUDIT_LOG = Path(os.environ.get("SOVRUN_LOGS_DIR", Path.cwd() / "logs")) / "media.jsonl"


@dataclass
class ProviderResult:
    """Result from a media generation call."""
    success: bool
    output_path: str | None = None
    provider: str = ""
    task_type: str = ""
    cost_usd: float = 0.0
    metadata: dict[str, Any] = field(default_factory=dict)
    error: str | None = None

    def to_dict(self) -> dict[str, Any]:
        d: dict[str, Any] = {
            "success": self.success,
            "provider": self.provider,
            "task_type": self.task_type,
            "cost_usd": self.cost_usd,
        }
        if self.output_path:
            d["output_path"] = self.output_path
        if self.error:
            d["error"] = self.error
        if self.metadata:
            d["metadata"] = self.metadata
        return d


def audit_media(event: str, **data: Any) -> None:
    """Append to media JSONL audit trail."""
    AUDIT_LOG.parent.mkdir(parents=True, exist_ok=True)
    entry = {
        "ts": datetime.now(timezone.utc).isoformat(timespec="milliseconds"),
        "event": event,
        **data,
    }
    try:
        with open(AUDIT_LOG, "a") as f:
            f.write(json.dumps(entry, default=str) + "\n")
    except OSError as exc:
        logger.warning("failed to write media audit: %s", exc)


class MediaProvider:
    """Base class for all media providers.

    Subclasses must implement:
        name        - provider identifier string
        task_types  - list of supported task types (image, video, tts, voice_agent, music)
        budget_tier - minimum budget tier required (free, low, mid, high)
        needs_gpu   - whether local GPU is required

        generate(task_type, **kwargs) -> ProviderResult
        get_cost(task_type, **kwargs) -> float
        is_available() -> bool
    """

    name: str = "base"
    task_types: list[str] = []
    budget_tier: str = "free"  # free, low, mid, high
    needs_gpu: bool = False

    def generate(self, task_type: str, **kwargs: Any) -> ProviderResult:
        raise NotImplementedError

    def get_cost(self, task_type: str, **kwargs: Any) -> float:
        return 0.0

    def is_available(self) -> bool:
        return False

    def _output_dir(self, task_type: str) -> Path:
        """Get or create output directory for this task type."""
        d = MEDIA_DIR / task_type / self.name
        d.mkdir(parents=True, exist_ok=True)
        return d

    def _output_path(self, task_type: str, ext: str) -> Path:
        """Generate a unique output file path."""
        ts = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S_%f")
        return self._output_dir(task_type) / f"{ts}.{ext}"
