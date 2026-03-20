"""
OpenAI Media Provider -- DALL-E 3 image generation + TTS.

Requires: OPENAI_API_KEY environment variable.
Costs: DALL-E 3 ~$0.04/image (1024x1024), TTS ~$0.015/1K chars.
"""
from __future__ import annotations

import json
import logging
import os
from typing import Any

from .base import MediaProvider, ProviderResult, audit_media

logger = logging.getLogger("sovrun.media.openai")

_DALLE_SIZES = {"256x256", "512x512", "1024x1024", "1024x1792", "1792x1024"}
_TTS_VOICES = {"alloy", "echo", "fable", "onyx", "nova", "shimmer"}

# Cost estimates
_DALLE_COST = {
    "256x256": 0.016,
    "512x512": 0.018,
    "1024x1024": 0.04,
    "1024x1792": 0.08,
    "1792x1024": 0.08,
}
_TTS_COST_PER_CHAR = 0.000015  # $0.015 per 1K chars


class OpenAIMediaProvider(MediaProvider):
    """OpenAI DALL-E 3 + TTS via REST API."""

    name = "openai"
    task_types = ["image", "tts"]
    budget_tier = "low"
    needs_gpu = False

    def __init__(self) -> None:
        self._api_key = os.environ.get("OPENAI_API_KEY", "")

    def is_available(self) -> bool:
        return bool(self._api_key)

    def get_cost(self, task_type: str, **kwargs: Any) -> float:
        if task_type == "image":
            size = kwargs.get("size", "1024x1024")
            return _DALLE_COST.get(size, 0.04)
        if task_type == "tts":
            text = kwargs.get("text", "")
            return len(text) * _TTS_COST_PER_CHAR
        return 0.0

    def generate(self, task_type: str, **kwargs: Any) -> ProviderResult:
        if task_type == "image":
            return self._generate_image(**kwargs)
        if task_type == "tts":
            return self._generate_tts(**kwargs)
        return ProviderResult(
            success=False, provider=self.name, task_type=task_type,
            error=f"unsupported task type: {task_type}",
        )

    def _generate_image(self, **kwargs: Any) -> ProviderResult:
        prompt = kwargs.get("prompt", "")
        if not prompt:
            return ProviderResult(
                success=False, provider=self.name, task_type="image",
                error="prompt is required",
            )

        size = kwargs.get("size", "1024x1024")
        if size not in _DALLE_SIZES:
            size = "1024x1024"

        style = kwargs.get("style", "vivid")  # vivid or natural
        quality = kwargs.get("quality", "standard")  # standard or hd

        try:
            from ..deps import get_http_client
        except ImportError:
            from deps import get_http_client  # type: ignore[no-redef]

        client = get_http_client(
            base_url="https://api.openai.com",
            headers={
                "Authorization": f"Bearer {self._api_key}",
                "Content-Type": "application/json",
            },
            timeout=120.0,
        )

        try:
            resp = client.post("/v1/images/generations", json={
                "model": "dall-e-3",
                "prompt": prompt,
                "n": 1,
                "size": size,
                "style": style,
                "quality": quality,
                "response_format": "url",
            })
            resp.raise_for_status()
            data = resp.json()

            image_url = data["data"][0]["url"]
            revised_prompt = data["data"][0].get("revised_prompt", prompt)

            # Download image
            output_path = self._output_path("image", "png")
            img_resp = client.get(image_url)
            img_resp.raise_for_status()
            output_path.write_bytes(img_resp.text.encode("latin-1"))

            cost = _DALLE_COST.get(size, 0.04)
            audit_media(
                "image_generated", provider=self.name, prompt=prompt[:100],
                size=size, cost=cost, output=str(output_path),
            )

            return ProviderResult(
                success=True,
                output_path=str(output_path),
                provider=self.name,
                task_type="image",
                cost_usd=cost,
                metadata={
                    "size": size, "style": style, "quality": quality,
                    "revised_prompt": revised_prompt,
                },
            )
        except Exception as exc:
            logger.error("openai image generation failed: %s", exc)
            return ProviderResult(
                success=False, provider=self.name, task_type="image",
                error=str(exc),
            )
        finally:
            client.close()

    def _generate_tts(self, **kwargs: Any) -> ProviderResult:
        text = kwargs.get("text", "")
        if not text:
            return ProviderResult(
                success=False, provider=self.name, task_type="tts",
                error="text is required",
            )

        voice = kwargs.get("voice", "onyx")
        if voice not in _TTS_VOICES:
            voice = "onyx"

        model = kwargs.get("model", "tts-1")  # tts-1 or tts-1-hd

        try:
            from ..deps import get_http_client
        except ImportError:
            from deps import get_http_client  # type: ignore[no-redef]

        client = get_http_client(
            base_url="https://api.openai.com",
            headers={
                "Authorization": f"Bearer {self._api_key}",
                "Content-Type": "application/json",
            },
            timeout=120.0,
        )

        try:
            resp = client.post("/v1/audio/speech", json={
                "model": model,
                "input": text,
                "voice": voice,
                "response_format": "mp3",
            })
            resp.raise_for_status()

            output_path = self._output_path("tts", "mp3")
            output_path.write_bytes(resp.text.encode("latin-1"))

            cost = len(text) * _TTS_COST_PER_CHAR
            audit_media(
                "tts_generated", provider=self.name, voice=voice,
                chars=len(text), cost=cost, output=str(output_path),
            )

            return ProviderResult(
                success=True,
                output_path=str(output_path),
                provider=self.name,
                task_type="tts",
                cost_usd=cost,
                metadata={"voice": voice, "model": model, "chars": len(text)},
            )
        except Exception as exc:
            logger.error("openai tts failed: %s", exc)
            return ProviderResult(
                success=False, provider=self.name, task_type="tts",
                error=str(exc),
            )
        finally:
            client.close()
