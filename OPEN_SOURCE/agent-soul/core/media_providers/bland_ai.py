"""
Bland AI Provider -- voice agent calls (inbound + outbound).

Requires: BLAND_AI_API_KEY environment variable.
Pricing: 100 free calls/day, $0.09/min after.
"""
from __future__ import annotations

import json
import logging
import os
from typing import Any

from .base import MediaProvider, ProviderResult, audit_media

logger = logging.getLogger("sovrun.media.bland_ai")

_COST_PER_MINUTE = 0.09


class BlandAIProvider(MediaProvider):
    """Bland AI -- programmable voice agents for phone calls."""

    name = "bland_ai"
    task_types = ["voice_agent"]
    budget_tier = "low"
    needs_gpu = False

    def __init__(self) -> None:
        self._api_key = os.environ.get("BLAND_AI_API_KEY", "")

    def is_available(self) -> bool:
        return bool(self._api_key)

    def get_cost(self, task_type: str, **kwargs: Any) -> float:
        if task_type == "voice_agent":
            duration_min = kwargs.get("max_duration", 5)
            return duration_min * _COST_PER_MINUTE
        return 0.0

    def generate(self, task_type: str, **kwargs: Any) -> ProviderResult:
        if task_type != "voice_agent":
            return ProviderResult(
                success=False, provider=self.name, task_type=task_type,
                error=f"unsupported task type: {task_type}",
            )

        action = kwargs.get("action", "call")
        if action == "call":
            return self._make_call(**kwargs)
        if action == "setup":
            return self._setup_agent(**kwargs)
        return ProviderResult(
            success=False, provider=self.name, task_type=task_type,
            error=f"unknown action: {action}",
        )

    def _make_call(self, **kwargs: Any) -> ProviderResult:
        phone_number = kwargs.get("to_number", "")
        if not phone_number:
            return ProviderResult(
                success=False, provider=self.name, task_type="voice_agent",
                error="to_number is required",
            )

        script = kwargs.get("script", "")
        task = kwargs.get("task", script)
        voice = kwargs.get("voice", "maya")
        max_duration = kwargs.get("max_duration", 5)

        try:
            from ..deps import get_http_client
        except ImportError:
            from deps import get_http_client  # type: ignore[no-redef]

        client = get_http_client(
            base_url="https://api.bland.ai",
            headers={
                "Authorization": self._api_key,
                "Content-Type": "application/json",
            },
            timeout=30.0,
        )

        try:
            payload: dict[str, Any] = {
                "phone_number": phone_number,
                "task": task,
                "voice": voice,
                "max_duration": max_duration,
                "record": True,
            }
            if kwargs.get("from_number"):
                payload["from"] = kwargs["from_number"]
            if kwargs.get("first_sentence"):
                payload["first_sentence"] = kwargs["first_sentence"]
            if kwargs.get("model"):
                payload["model"] = kwargs["model"]

            resp = client.post("/v1/calls", json=payload)
            resp.raise_for_status()
            data = resp.json()

            call_id = data.get("call_id", "")
            audit_media(
                "call_initiated", provider=self.name,
                call_id=call_id, to=phone_number,
                cost_est=max_duration * _COST_PER_MINUTE,
            )

            return ProviderResult(
                success=True,
                provider=self.name,
                task_type="voice_agent",
                cost_usd=max_duration * _COST_PER_MINUTE,
                metadata={
                    "call_id": call_id,
                    "phone_number": phone_number,
                    "voice": voice,
                    "status": data.get("status", "queued"),
                },
            )
        except Exception as exc:
            logger.error("bland.ai call failed: %s", exc)
            return ProviderResult(
                success=False, provider=self.name, task_type="voice_agent",
                error=str(exc),
            )
        finally:
            client.close()

    def _setup_agent(self, **kwargs: Any) -> ProviderResult:
        """Configure an inbound voice agent on a phone number."""
        phone_number = kwargs.get("phone_number", "")
        script = kwargs.get("script", "")

        if not phone_number or not script:
            return ProviderResult(
                success=False, provider=self.name, task_type="voice_agent",
                error="phone_number and script are required for setup",
            )

        try:
            from ..deps import get_http_client
        except ImportError:
            from deps import get_http_client  # type: ignore[no-redef]

        client = get_http_client(
            base_url="https://api.bland.ai",
            headers={
                "Authorization": self._api_key,
                "Content-Type": "application/json",
            },
            timeout=30.0,
        )

        try:
            payload: dict[str, Any] = {
                "phone_number": phone_number,
                "prompt": script,
                "voice": kwargs.get("voice", "maya"),
            }
            if kwargs.get("webhook_url"):
                payload["webhook"] = kwargs["webhook_url"]

            resp = client.post("/v1/inbound", json=payload)
            resp.raise_for_status()
            data = resp.json()

            audit_media(
                "agent_configured", provider=self.name,
                phone_number=phone_number,
            )

            return ProviderResult(
                success=True,
                provider=self.name,
                task_type="voice_agent",
                cost_usd=0.0,
                metadata={
                    "phone_number": phone_number,
                    "status": "configured",
                    "response": data,
                },
            )
        except Exception as exc:
            logger.error("bland.ai setup failed: %s", exc)
            return ProviderResult(
                success=False, provider=self.name, task_type="voice_agent",
                error=str(exc),
            )
        finally:
            client.close()

    def get_call_status(self, call_id: str) -> dict[str, Any]:
        """Check status of an ongoing or completed call."""
        try:
            from ..deps import get_http_client
        except ImportError:
            from deps import get_http_client  # type: ignore[no-redef]

        client = get_http_client(
            base_url="https://api.bland.ai",
            headers={"Authorization": self._api_key},
            timeout=15.0,
        )
        try:
            resp = client.get(f"/v1/calls/{call_id}")
            resp.raise_for_status()
            return resp.json()
        except Exception as exc:
            return {"error": str(exc)}
        finally:
            client.close()
