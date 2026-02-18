#!/usr/bin/env python3
"""
image_generator.py - Generate social media images with text overlays

Creates platform-sized images with text captions for social media posts.
Uses PIL/Pillow for image generation. Supports multiple templates and sizes.

Usage:
    python3 image_generator.py --text "Your caption here" --platform X --template dark
    python3 image_generator.py --text "Big number stat" --platform Instagram --template stats
    python3 image_generator.py --file content.md --platform all --output-dir output/

Example:
    python3 image_generator.py --text "I made $47K in 30 days. here's the stack." --platform X --template dark
    python3 image_generator.py --text "Cold email reply rate: 12.3%" --platform Instagram --template stats --color "#1a1a2e"
"""

import argparse
import logging
import os
import sys
from datetime import datetime
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent.parent
AUTOMATIONS_DIR = PROJECT_DIR / "AUTOMATIONS"
LOG_DIR = AUTOMATIONS_DIR / "logs"
OUTPUT_DIR = AUTOMATIONS_DIR / "generated_images"

LOG_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_DIR / "image_generator.log"),
        logging.StreamHandler(sys.stdout),
    ],
)
logger = logging.getLogger(__name__)

# Platform image sizes
PLATFORM_SIZES = {
    "X": (1200, 675),          # 16:9
    "Twitter": (1200, 675),
    "Instagram": (1080, 1080),  # Square
    "Instagram_story": (1080, 1920),  # 9:16
    "LinkedIn": (1200, 627),   # ~1.91:1
    "TikTok": (1080, 1920),    # 9:16
    "YouTube": (1280, 720),    # 16:9
    "Pinterest": (1000, 1500),  # 2:3
    "Facebook": (1200, 630),   # ~1.91:1
    "carousel": (1080, 1350),  # 4:5
}

TEMPLATES = {
    "dark": {"bg": (26, 26, 46), "text": (255, 255, 255), "accent": (102, 126, 234)},
    "light": {"bg": (250, 250, 250), "text": (30, 30, 30), "accent": (59, 130, 246)},
    "gradient_blue": {"bg": (15, 23, 42), "text": (255, 255, 255), "accent": (56, 189, 248)},
    "gradient_purple": {"bg": (30, 10, 60), "text": (255, 255, 255), "accent": (168, 85, 247)},
    "stats": {"bg": (10, 10, 10), "text": (0, 255, 136), "accent": (255, 255, 255)},
    "faith": {"bg": (25, 25, 50), "text": (255, 215, 0), "accent": (255, 255, 255)},
    "fitness": {"bg": (20, 20, 20), "text": (255, 69, 0), "accent": (255, 255, 255)},
    "tech": {"bg": (0, 20, 40), "text": (0, 255, 65), "accent": (255, 255, 255)},
}


def hex_to_rgb(hex_color):
    """Convert hex color to RGB tuple."""
    hex_color = hex_color.lstrip("#")
    return tuple(int(hex_color[i : i + 2], 16) for i in (0, 2, 4))


def wrap_text(text, max_width, font_size_approx=40):
    """Wrap text to fit within width (approximate character-based)."""
    chars_per_line = max(10, max_width // (font_size_approx * 0.55))
    words = text.split()
    lines = []
    current = ""

    for word in words:
        if len(current) + len(word) + 1 <= chars_per_line:
            current = f"{current} {word}" if current else word
        else:
            if current:
                lines.append(current)
            current = word

    if current:
        lines.append(current)

    return lines


def generate_image_pillow(text, size, template_name, output_path, branding="PRINTMAXX"):
    """Generate image using Pillow."""
    try:
        from PIL import Image, ImageDraw, ImageFont
    except ImportError:
        logger.error("Pillow not installed. Run: pip install Pillow")
        logger.info("Generating placeholder spec instead...")
        return generate_spec_fallback(text, size, template_name, output_path)

    template = TEMPLATES.get(template_name, TEMPLATES["dark"])
    width, height = size

    # Create image
    img = Image.new("RGB", (width, height), template["bg"])
    draw = ImageDraw.Draw(img)

    # Try to use a nice font, fall back to default
    font_size = min(width, height) // 15
    small_font_size = font_size // 2

    try:
        font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", font_size)
        small_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", small_font_size)
    except (IOError, OSError):
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", font_size)
            small_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", small_font_size)
        except (IOError, OSError):
            font = ImageFont.load_default()
            small_font = font

    # Wrap text
    lines = wrap_text(text, width - 120, font_size)

    # Calculate vertical position (center)
    line_height = font_size * 1.4
    total_height = len(lines) * line_height
    start_y = (height - total_height) / 2

    # Draw accent bar
    bar_y = start_y - 30
    draw.rectangle(
        [60, bar_y, 60 + 80, bar_y + 4],
        fill=template["accent"],
    )

    # Draw text lines
    for i, line in enumerate(lines):
        y = start_y + i * line_height
        draw.text((80, y), line, fill=template["text"], font=font)

    # Draw branding
    if branding:
        draw.text(
            (80, height - 60),
            branding,
            fill=(*template["accent"], 180) if len(template["accent"]) == 3 else template["accent"],
            font=small_font,
        )

    # Save
    img.save(output_path, quality=95)
    logger.info(f"Generated image: {output_path} ({width}x{height})")
    return output_path


def generate_spec_fallback(text, size, template_name, output_path):
    """Generate a text spec file when Pillow is not available."""
    spec_path = str(output_path).replace(".png", "_spec.md")
    template = TEMPLATES.get(template_name, TEMPLATES["dark"])

    spec = f"# Image Spec\n\n"
    spec += f"**Size:** {size[0]}x{size[1]}\n"
    spec += f"**Template:** {template_name}\n"
    spec += f"**Background:** rgb{template['bg']}\n"
    spec += f"**Text Color:** rgb{template['text']}\n"
    spec += f"**Accent:** rgb{template['accent']}\n\n"
    spec += f"## Text Content:\n\n"
    spec += f"{text}\n\n"
    spec += f"## Layout:\n"
    spec += f"- Text centered vertically\n"
    spec += f"- Left-aligned at 80px margin\n"
    spec += f"- Accent bar above text\n"
    spec += f"- PRINTMAXX branding bottom-left\n"

    with open(spec_path, "w") as f:
        f.write(spec)

    logger.info(f"Generated spec (Pillow not available): {spec_path}")
    return spec_path


def main():
    parser = argparse.ArgumentParser(
        description="Generate social media images with text overlays"
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--text", type=str, help="Text to put on image")
    group.add_argument("--file", type=str, help="Read text from file")
    parser.add_argument(
        "--platform",
        type=str,
        default="X",
        help="Platform size or 'all' (default: X)",
    )
    parser.add_argument(
        "--template",
        choices=list(TEMPLATES.keys()),
        default="dark",
        help="Visual template (default: dark)",
    )
    parser.add_argument("--color", type=str, default=None, help="Override background color (hex)")
    parser.add_argument("--output-dir", type=str, default=None, help="Output directory")
    parser.add_argument("--branding", type=str, default="PRINTMAXX", help="Branding text")
    args = parser.parse_args()

    if args.file:
        path = Path(args.file)
        if not path.is_absolute():
            path = PROJECT_DIR / args.file
        with open(path) as f:
            text = f.read().strip()
        # Use first paragraph or first 200 chars
        paragraphs = text.split("\n\n")
        text = paragraphs[0][:200] if paragraphs else text[:200]
    else:
        text = args.text

    out_dir = Path(args.output_dir) if args.output_dir else OUTPUT_DIR
    out_dir.mkdir(parents=True, exist_ok=True)

    if args.platform.lower() == "all":
        platforms = list(PLATFORM_SIZES.keys())
    else:
        platforms = [args.platform]

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    for platform in platforms:
        size = PLATFORM_SIZES.get(platform, PLATFORM_SIZES["X"])
        filename = f"{platform}_{args.template}_{timestamp}.png"
        output_path = out_dir / filename

        if args.color:
            # Override template bg color
            TEMPLATES[args.template]["bg"] = hex_to_rgb(args.color)

        generate_image_pillow(text, size, args.template, output_path, args.branding)

    logger.info(f"Generated {len(platforms)} image(s)")


if __name__ == "__main__":
    main()
