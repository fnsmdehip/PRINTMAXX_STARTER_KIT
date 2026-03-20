"""
Replicate Provider -- Flux, Stable Diffusion, video models via Replicate API.

Requires: REPLICATE_API_TOKEN environment variable.
Supports: image (Flux, SDXL), video (Wan2.1, various), music (MusicGen).
"""
from __future__ import annotations

import json
import logging
import os
import time
from typing import Any

from .base import MediaProvider, ProviderResult, audit_media

logger = logging.getLogger("sovrun.media.replicate")

# Model registry: task_type -> list of (model_id, friendly_name, cost_estimate)
_MODELS: dict[str, list[tuple[str, str, float]]] = {
    "image": [
        ("black-forest-labs/flux-schnell", "flux-schnell", 0.003),
        ("black-forest-labs/flux-1.1-pro", "flux-pro", 0.04),
        ("stability-ai/sdxl:latest", "sdxl", 0.005),
    ],
    "video": [
        ("wan-ai/wan-2.1-t2v-480p", "wan2.1-480p", 0.05),
        ("minimax/video-01-live", "minimax-video", 0.10),
    ],
    "music": [
        ("meta/musicgen:latest", "musicgen", 0.03),
    ],
}

_POLL_INTERVAL = 2.0
_MAX_POLL_TIME = 300.0  # 5 minutes


class ReplicateProvider(MediaProvider):
    """Replicate API -- run open-source models in the cloud."""

    name = "replicate"
    task_types = ["image", "video", "music"]
    budget_tier = "low"
    needs_gpu = False

    def __init__(self) -> None:
        self._api_token = os.environ.get("REPLICATE_API_TOKEN", "")

    def is_available(self) -> bool:
        return bool(self._api_token)

    def get_cost(self, task_type: str, **kwargs: Any) -> float:
        models = _MODELS.get(task_type, [])
        model_name = kwargs.get("model")
        if model_name:
            for model_id, name, cost in models:
                if name == model_name or model_id == model_name:
                    return cost
        # Return cheapest option
        return models[0][2] if models else 0.0

    def generate(self, task_type: str, **kwargs: Any) -> ProviderResult:
        models = _MODELS.get(task_type)
        if not models:
            return ProviderResult(
                success=False, provider=self.name, task_type=task_type,
                error=f"unsupported task type: {task_type}",
            )

        # Select model
        model_name = kwargs.get("model")
        model_id = models[0][0]  # default to first (cheapest)
        cost_est = models[0][2]
        if model_name:
            for mid, name, cost in models:
                if name == model_name or mid == model_name:
                    model_id = mid
                    cost_est = cost
                    break

        # Build input based on task type
        model_input = self._build_input(task_type, **kwargs)

        try:
            from ..deps import get_http_client
        except ImportError:
            from deps import get_http_client  # type: ignore[no-redef]

        client = get_http_client(
            base_url="https://api.replicate.com",
            headers={
                "Authorization": f"Bearer {self._api_token}",
                "Content-Type": "application/json",
                "Prefer": "wait",
            },
            timeout=_MAX_POLL_TIME,
        )

        try:
            # Create prediction
            resp = client.post("/v1/predictions", json={
                "version": model_id.split(":")[-1] if ":" in model_id else None,
                "model": model_id if ":" not in model_id else None,
                "input": model_input,
            })
            resp.raise_for_status()
            prediction = resp.json()

            # Poll until complete
            pred_url = prediction.get("urls", {}).get("get", "")
            if not pred_url:
                pred_url = f"/v1/predictions/{prediction['id']}"

            output_url = self._poll_prediction(client, pred_url)
            if not output_url:
                return ProviderResult(
                    success=False, provider=self.name, task_type=task_type,
                    error="prediction timed out or failed",
                )

            # Download output
            ext = self._ext_for_task(task_type)
            output_path = self._output_path(task_type, ext)
            dl_resp = client.get(output_url)
            dl_resp.raise_for_status()
            output_path.write_bytes(dl_resp.text.encode("latin-1"))

            audit_media(
                f"{task_type}_generated", provider=self.name,
                model=model_id, cost=cost_est, output=str(output_path),
            )

            return ProviderResult(
                success=True,
                output_path=str(output_path),
                provider=self.name,
                task_type=task_type,
                cost_usd=cost_est,
                metadata={"model": model_id, "input": model_input},
            )
        except Exception as exc:
            logger.error("replicate generation failed: %s", exc)
            return ProviderResult(
                success=False, provider=self.name, task_type=task_type,
                error=str(exc),
            )
        finally:
            client.close()

    def _build_input(self, task_type: str, **kwargs: Any) -> dict[str, Any]:
        if task_type == "image":
            inp: dict[str, Any] = {"prompt": kwargs.get("prompt", "")}
            if kwargs.get("size"):
                parts = kwargs["size"].split("x")
                if len(parts) == 2:
                    inp["width"] = int(parts[0])
                    inp["height"] = int(parts[1])
            if kwargs.get("negative_prompt"):
                inp["negative_prompt"] = kwargs["negative_prompt"]
            return inp

        if task_type == "video":
            inp = {"prompt": kwargs.get("prompt", "")}
            if kwargs.get("duration"):
                inp["duration"] = kwargs["duration"]
            return inp

        if task_type == "music":
            inp = {"prompt": kwargs.get("prompt", "")}
            if kwargs.get("duration"):
                inp["duration"] = kwargs["duration"]
            return inp

        return {"prompt": kwargs.get("prompt", "")}

    def _poll_prediction(self, client: Any, pred_url: str) -> str | None:
        """Poll a prediction until complete, return output URL."""
        elapsed = 0.0
        while elapsed < _MAX_POLL_TIME:
            resp = client.get(pred_url)
            if resp.status_code != 200:
                return None
            data = resp.json()
            status = data.get("status", "")

            if status == "succeeded":
                output = data.get("output")
                if isinstance(output, list) and output:
                    return output[0]
                if isinstance(output, str):
                    return output
                return None

            if status in ("failed", "canceled"):
                logger.error("replicate prediction %s: %s", status,
                             data.get("error", ""))
                return None

            time.sleep(_POLL_INTERVAL)
            elapsed += _POLL_INTERVAL

        return None

    @staticmethod
    def _ext_for_task(task_type: str) -> str:
        return {"image": "png", "video": "mp4", "music": "wav"}.get(task_type, "bin")
