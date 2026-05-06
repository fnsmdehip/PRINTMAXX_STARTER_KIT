#!/usr/bin/env python3
"""Generate OG preview PNG images for landing pages that have broken data:URI og images."""

from PIL import Image, ImageDraw, ImageFont
import os

BASE = "/Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt/LANDING"

CONFIGS = [
    {
        "dir": "cnsnt",
        "bg": (10, 10, 26),          # #0a0a1a
        "accent": (108, 92, 231),     # #6c5ce7
        "accent2": (0, 184, 148),     # #00b894
        "title": "cnsnt",
        "subtitle": "Video Consent. AES-256 Encrypted.",
        "tagline": "GPS Timestamp  ·  Legal Templates  ·  Local-First",
    },
    {
        "dir": "cnsnt-downloads",
        "bg": (10, 10, 26),
        "accent": (108, 92, 231),
        "accent2": (0, 184, 148),
        "title": "cnsnt Desktop",
        "subtitle": "Download for Mac & Windows",
        "tagline": "AES-256 Encrypted  ·  No Account Required  ·  Local-First",
    },
    {
        "dir": "research-blog",
        "bg": (26, 30, 46),           # #1a1e2e
        "accent": (74, 158, 255),     # #4a9eff
        "accent2": (148, 163, 184),   # #94a3b8
        "title": "fnsmdehip research",
        "subtitle": "PEMF Therapy  ·  WiFi Sensing  ·  Cross-Domain Theory",
        "tagline": "Falsifiable claims. Published data. Kill switches on every idea.",
    },
    {
        "dir": "builders-ledger",
        "bg": (245, 240, 232),        # #f5f0e8 (light parchment)
        "accent": (139, 0, 0),        # #8b0000
        "accent2": (51, 51, 51),      # #333
        "title": "The Builder's Ledger",
        "subtitle": "Weekly Engineering & Revenue Report",
        "tagline": "Real numbers. Shipped products. No fluff.",
    },
]

def find_font(size):
    """Return best available font at given size."""
    candidates = [
        "/System/Library/Fonts/Helvetica.ttc",
        "/System/Library/Fonts/HelveticaNeue.ttc",
        "/System/Library/Fonts/SFNSDisplay.ttf",
        "/System/Library/Fonts/SFCompactDisplay.ttf",
        "/System/Library/Fonts/Arial.ttf",
        "/Library/Fonts/Arial.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    ]
    for path in candidates:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except Exception:
                continue
    return ImageFont.load_default()


def draw_rounded_rect(draw, x1, y1, x2, y2, radius, fill):
    draw.rounded_rectangle([x1, y1, x2, y2], radius=radius, fill=fill)


def generate_og(cfg, output_path):
    W, H = 1200, 630
    img = Image.new("RGB", (W, H), cfg["bg"])
    draw = ImageDraw.Draw(img)

    is_light = sum(cfg["bg"]) > 380

    # Subtle gradient overlay (top strip accent)
    for i in range(8):
        alpha = int(60 - i * 7)
        r, g, b = cfg["accent"]
        strip_color = (r, g, b)
        draw.rectangle([0, i, W, i + 1], fill=strip_color)

    # Left accent bar
    draw.rectangle([0, 0, 6, H], fill=cfg["accent"])

    # Title
    title_font = find_font(88)
    title_color = cfg["accent"] if not is_light else cfg["accent"]
    # Measure title
    bbox = draw.textbbox((0, 0), cfg["title"], font=title_font)
    tw = bbox[2] - bbox[0]
    tx = max(80, (W - tw) // 2)
    ty = 160
    draw.text((tx, ty), cfg["title"], font=title_font, fill=title_color)

    # Subtitle
    sub_font = find_font(38)
    sub_color = cfg["accent2"] if not is_light else cfg["accent2"]
    sbbox = draw.textbbox((0, 0), cfg["subtitle"], font=sub_font)
    sw = sbbox[2] - sbbox[0]
    sx = max(80, (W - sw) // 2)
    draw.text((sx, ty + 110), cfg["subtitle"], font=sub_font, fill=sub_color)

    # Tagline
    tag_font = find_font(26)
    tag_color = (140, 140, 160) if not is_light else (100, 100, 100)
    tbbox = draw.textbbox((0, 0), cfg["tagline"], font=tag_font)
    tgw = tbbox[2] - tbbox[0]
    tgx = max(80, (W - tgw) // 2)
    draw.text((tgx, ty + 180), cfg["tagline"], font=tag_font, fill=tag_color)

    # Bottom brand watermark
    brand_font = find_font(20)
    brand_color = (80, 80, 100) if not is_light else (160, 140, 120)
    draw.text((80, H - 50), "printmaxx.surge.sh", font=brand_font, fill=brand_color)

    img.save(output_path, "PNG", optimize=True)
    print(f"  Generated: {output_path}")


def main():
    for cfg in CONFIGS:
        out_dir = os.path.join(BASE, cfg["dir"])
        if not os.path.isdir(out_dir):
            print(f"  SKIP (dir not found): {out_dir}")
            continue
        out_path = os.path.join(out_dir, "og.png")
        try:
            generate_og(cfg, out_path)
        except Exception as e:
            print(f"  ERROR {cfg['dir']}: {e}")

    print("\nDone generating OG images.")


if __name__ == "__main__":
    main()
