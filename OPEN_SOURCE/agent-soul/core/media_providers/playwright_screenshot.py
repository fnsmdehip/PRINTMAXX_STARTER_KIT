"""
Playwright Screenshot Provider -- zero-cost HTML-to-image via Playwright.

Renders HTML content in a headless browser and captures a screenshot.
Great for thumbnails, social cards, banners, data visualizations.
No API key needed. Just pip install playwright && playwright install chromium.
"""
from __future__ import annotations

import logging
import os
import tempfile
from pathlib import Path
from typing import Any

from .base import MediaProvider, ProviderResult, audit_media

logger = logging.getLogger("sovrun.media.playwright")


class PlaywrightScreenshotProvider(MediaProvider):
    """Zero-cost HTML-to-image via Playwright browser automation."""

    name = "playwright_screenshot"
    task_types = ["image"]
    budget_tier = "free"
    needs_gpu = False

    def is_available(self) -> bool:
        try:
            from playwright.sync_api import sync_playwright  # noqa: F401
            return True
        except ImportError:
            return False

    def get_cost(self, task_type: str, **kwargs: Any) -> float:
        return 0.0

    def generate(self, task_type: str, **kwargs: Any) -> ProviderResult:
        if task_type != "image":
            return ProviderResult(
                success=False, provider=self.name, task_type=task_type,
                error=f"unsupported task type: {task_type}",
            )

        html_content = kwargs.get("html_content", "")
        url = kwargs.get("url", "")
        if not html_content and not url:
            return ProviderResult(
                success=False, provider=self.name, task_type=task_type,
                error="html_content or url is required",
            )

        # Parse size
        size = kwargs.get("size", "1280x720")
        parts = size.split("x")
        width = int(parts[0]) if len(parts) >= 1 else 1280
        height = int(parts[1]) if len(parts) >= 2 else 720

        full_page = kwargs.get("full_page", False)
        selector = kwargs.get("selector")  # CSS selector for element screenshot

        output_path = str(self._output_path("image", "png"))

        try:
            self._capture(
                html_content=html_content,
                url=url,
                output_path=output_path,
                width=width,
                height=height,
                full_page=full_page,
                selector=selector,
            )
            audit_media(
                "screenshot_generated", provider=self.name,
                width=width, height=height, output=output_path,
            )
            return ProviderResult(
                success=True,
                output_path=output_path,
                provider=self.name,
                task_type="image",
                cost_usd=0.0,
                metadata={"width": width, "height": height, "full_page": full_page},
            )
        except Exception as exc:
            logger.error("playwright screenshot failed: %s", exc)
            return ProviderResult(
                success=False, provider=self.name, task_type=task_type,
                error=str(exc),
            )

    def _capture(
        self,
        html_content: str,
        url: str,
        output_path: str,
        width: int,
        height: int,
        full_page: bool,
        selector: str | None,
    ) -> None:
        from playwright.sync_api import sync_playwright

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page(viewport={"width": width, "height": height})

            if url:
                page.goto(url, wait_until="networkidle")
            elif html_content:
                # Write HTML to temp file, load it
                tmp = tempfile.NamedTemporaryFile(
                    suffix=".html", delete=False, mode="w",
                )
                try:
                    tmp.write(html_content)
                    tmp.close()
                    page.goto(f"file://{tmp.name}", wait_until="networkidle")
                finally:
                    os.unlink(tmp.name)

            if selector:
                element = page.query_selector(selector)
                if element:
                    element.screenshot(path=output_path)
                else:
                    page.screenshot(path=output_path, full_page=full_page)
            else:
                page.screenshot(path=output_path, full_page=full_page)

            browser.close()

    def generate_thumbnail(
        self, title: str, subtitle: str = "", template: str = "default",
        size: str = "1280x720",
    ) -> ProviderResult:
        """Generate a YouTube/social thumbnail from a title and optional subtitle."""
        html = self._thumbnail_html(title, subtitle, template)
        return self.generate("image", html_content=html, size=size)

    @staticmethod
    def _thumbnail_html(title: str, subtitle: str, template: str) -> str:
        bg_color = "#0a0a0a"
        accent = "#00ff88"
        if template == "dark_red":
            accent = "#ff4444"
        elif template == "blue":
            bg_color = "#0d1117"
            accent = "#58a6ff"

        subtitle_html = ""
        if subtitle:
            subtitle_html = f'<div style="color:#ccc;font-size:28px;margin-top:16px;">{subtitle}</div>'

        return f"""<!DOCTYPE html>
<html><head><style>
    body {{
        margin: 0; padding: 0;
        width: 1280px; height: 720px;
        background: {bg_color};
        display: flex; align-items: center; justify-content: center;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    }}
    .card {{
        text-align: center; padding: 60px;
        max-width: 1000px;
    }}
    .title {{
        color: {accent}; font-size: 56px; font-weight: 800;
        line-height: 1.2; letter-spacing: -1px;
    }}
</style></head><body>
    <div class="card">
        <div class="title">{title}</div>
        {subtitle_html}
    </div>
</body></html>"""
