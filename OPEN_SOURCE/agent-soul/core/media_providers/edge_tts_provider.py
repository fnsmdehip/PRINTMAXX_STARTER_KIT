"""
Edge TTS Provider -- Microsoft Edge text-to-speech (free, no API key).

Uses the edge-tts Python package which connects to Microsoft's Edge
browser TTS service. Hundreds of voices, multiple languages, zero cost.

Install: pip install edge-tts
"""
from __future__ import annotations

import asyncio
import logging
import os
import shutil
from typing import Any

from .base import MediaProvider, ProviderResult, audit_media

logger = logging.getLogger("sovrun.media.edge_tts")

# Default voices by style
_DEFAULT_VOICES: dict[str, str] = {
    "male_us": "en-US-GuyNeural",
    "female_us": "en-US-JennyNeural",
    "male_uk": "en-GB-RyanNeural",
    "female_uk": "en-GB-SoniaNeural",
    "male_au": "en-AU-WilliamNeural",
    "female_au": "en-AU-NatashaNeural",
    "narrator": "en-US-DavisNeural",
    "casual": "en-US-AriaNeural",
    "daniel": "en-US-DavisNeural",
}


class EdgeTTSProvider(MediaProvider):
    """Microsoft Edge TTS -- free, high-quality, no API key needed."""

    name = "edge_tts"
    task_types = ["tts"]
    budget_tier = "free"
    needs_gpu = False

    def is_available(self) -> bool:
        try:
            import edge_tts  # noqa: F401
            return True
        except ImportError:
            return False

    def get_cost(self, task_type: str, **kwargs: Any) -> float:
        return 0.0

    def generate(self, task_type: str, **kwargs: Any) -> ProviderResult:
        if task_type != "tts":
            return ProviderResult(
                success=False, provider=self.name, task_type=task_type,
                error=f"unsupported task type: {task_type}",
            )

        text = kwargs.get("text", "")
        if not text:
            return ProviderResult(
                success=False, provider=self.name, task_type=task_type,
                error="text is required",
            )

        voice = kwargs.get("voice", "narrator")
        # Resolve voice alias to full name
        voice_id = _DEFAULT_VOICES.get(voice, voice)

        output_path = str(self._output_path("tts", "mp3"))

        try:
            result = asyncio.run(self._generate_async(text, voice_id, output_path))
            audit_media(
                "tts_generated", provider=self.name, voice=voice_id,
                chars=len(text), output=output_path,
            )
            return result
        except Exception as exc:
            logger.error("edge_tts generation failed: %s", exc)
            return ProviderResult(
                success=False, provider=self.name, task_type=task_type,
                error=str(exc),
            )

    async def _generate_async(
        self, text: str, voice: str, output_path: str
    ) -> ProviderResult:
        import edge_tts

        communicate = edge_tts.Communicate(text, voice)
        await communicate.save(output_path)

        return ProviderResult(
            success=True,
            output_path=output_path,
            provider=self.name,
            task_type="tts",
            cost_usd=0.0,
            metadata={"voice": voice, "chars": len(text)},
        )

    @staticmethod
    def list_voices() -> list[dict[str, str]]:
        """List available Edge TTS voices."""
        try:
            import edge_tts
            voices = asyncio.run(edge_tts.list_voices())
            return [
                {"name": v["ShortName"], "gender": v["Gender"], "locale": v["Locale"]}
                for v in voices
            ]
        except ImportError:
            return []
