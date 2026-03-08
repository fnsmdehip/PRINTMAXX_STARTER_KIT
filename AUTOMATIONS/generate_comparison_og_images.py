#!/usr/bin/env python3
"""Generate OG images for comparison pages using Playwright screenshots."""

import os
import sys
import shutil

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE_PATH = os.path.join(PROJECT_ROOT, "MEDIA", "image_templates", "comparison_og.html")

COMPARISONS = [
    {
        "slug": "cursor-vs-claudecode",
        "product_a": "Cursor",
        "product_b": "Claude Code",
        "sub_a": "$20/mo AI IDE",
        "sub_b": "$20/mo CLI Agent",
        "tagline": "Same price, completely different workflows. Full 2026 comparison.",
        "color_a": "#3b82f6",
        "color_b": "#f97316",
    },
    {
        "slug": "coldmaxx-vs-instantly",
        "product_a": "ColdMaxx",
        "product_b": "Instantly",
        "sub_a": "Free forever",
        "sub_b": "$30-97/mo",
        "tagline": "$0/mo vs $30/mo. Same cold email features. Here's the real breakdown.",
        "color_a": "#06b6d4",
        "color_b": "#5046e4",
    },
    {
        "slug": "instantly-vs-lemlist",
        "product_a": "Instantly",
        "product_b": "Lemlist",
        "sub_a": "$30/mo volume",
        "sub_b": "$59/mo personalization",
        "tagline": "Volume vs personalization. Which cold email tool actually wins?",
        "color_a": "#5046e4",
        "color_b": "#ff6b6b",
    },
    {
        "slug": "pagescorer-vs-gtmetrix",
        "product_a": "PageScorer",
        "product_b": "GTmetrix",
        "sub_a": "Free, no signup",
        "sub_b": "Freemium",
        "tagline": "No signup vs account required. Which website speed test is better?",
        "color_a": "#3b82f6",
        "color_b": "#e87c2a",
    },
    {
        "slug": "sleepmaxx-vs-sleepcycle",
        "product_a": "SleepMaxx",
        "product_b": "Sleep Cycle",
        "sub_a": "Free, offline, private",
        "sub_b": "$40/year subscription",
        "tagline": "Your sleep data stays on your phone. No cloud, no subscription.",
        "color_a": "#8b5cf6",
        "color_b": "#f59e0b",
    },
]


def generate_og_html(comp):
    """Generate customized OG image HTML from template."""
    with open(TEMPLATE_PATH, "r") as f:
        html = f.read()

    html = html.replace("PRODUCTA", comp["product_a"])
    html = html.replace("PRODUCTB", comp["product_b"])
    html = html.replace("SUBA", comp["sub_a"])
    html = html.replace("SUBB", comp["sub_b"])
    html = html.replace("TAGLINE", comp["tagline"])
    html = html.replace("COLORA", comp["color_a"])
    html = html.replace("COLORB", comp["color_b"])

    return html


def main():
    """Generate OG images for all comparison pages."""
    output_dir = os.path.join(PROJECT_ROOT, "MEDIA", "generated_images", "og_comparisons")
    os.makedirs(output_dir, exist_ok=True)

    # Try Playwright first
    try:
        from playwright.sync_api import sync_playwright
        use_playwright = True
    except ImportError:
        print("Playwright not available. Generating HTML files only (screenshot manually).")
        use_playwright = False

    for comp in COMPARISONS:
        html = generate_og_html(comp)
        slug = comp["slug"]

        # Always save the HTML version
        html_path = os.path.join(output_dir, f"{slug}-og.html")
        with open(html_path, "w") as f:
            f.write(html)
        print(f"HTML: {html_path}")

        # Also save to the deployment directory
        deploy_dir = os.path.join(PROJECT_ROOT, "07_LANDING", slug)
        if os.path.isdir(deploy_dir):
            deploy_html_path = os.path.join(deploy_dir, "og-image.html")
            with open(deploy_html_path, "w") as f:
                f.write(html)
            print(f"  Deployed HTML OG to: {deploy_html_path}")

        if use_playwright:
            try:
                with sync_playwright() as p:
                    browser = p.chromium.launch(headless=True)
                    page = browser.new_page(viewport={"width": 1200, "height": 630})
                    page.set_content(html)
                    page.wait_for_timeout(500)

                    png_path = os.path.join(output_dir, f"{slug}-og.png")
                    page.screenshot(path=png_path)
                    print(f"  PNG: {png_path}")

                    # Copy to deployment dir
                    if os.path.isdir(deploy_dir):
                        deploy_png = os.path.join(deploy_dir, "og-image.png")
                        shutil.copy2(png_path, deploy_png)
                        print(f"  Deployed PNG OG to: {deploy_png}")

                    browser.close()
            except Exception as e:
                print(f"  Playwright screenshot failed for {slug}: {e}")

    print(f"\nDone. {len(COMPARISONS)} OG images generated in {output_dir}")


if __name__ == "__main__":
    main()
