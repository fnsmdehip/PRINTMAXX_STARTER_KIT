#!/usr/bin/env python3
"""Generate PRINTMAXX Panel app icon and convert to .icns"""

import os
import subprocess
import shutil
from PIL import Image, ImageDraw, ImageFont, ImageFilter

BASE = "/Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt/AUTOMATIONS"
ICON_SIZE = 1024
OUTPUT_PNG = os.path.join(BASE, "PrintmaxxPanel_icon.png")
ICONSET_DIR = os.path.join(BASE, "AppIcon.iconset")
ICNS_OUTPUT = os.path.join(BASE, "PrintmaxxPanel.app", "Contents", "Resources", "AppIcon.icns")


def create_icon():
    """Generate 1024x1024 PRINTMAXX icon."""
    img = Image.new("RGBA", (ICON_SIZE, ICON_SIZE), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # --- Dark gradient background ---
    top_color = (10, 10, 15)       # #0a0a0f
    bottom_color = (17, 24, 39)    # #111827
    for y in range(ICON_SIZE):
        t = y / (ICON_SIZE - 1)
        r = int(top_color[0] + (bottom_color[0] - top_color[0]) * t)
        g = int(top_color[1] + (bottom_color[1] - top_color[1]) * t)
        b = int(top_color[2] + (bottom_color[2] - top_color[2]) * t)
        draw.line([(0, y), (ICON_SIZE - 1, y)], fill=(r, g, b, 255))

    # --- Rounded corner mask ---
    corner_radius = 180
    mask = Image.new("L", (ICON_SIZE, ICON_SIZE), 0)
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.rounded_rectangle(
        [(0, 0), (ICON_SIZE - 1, ICON_SIZE - 1)],
        radius=corner_radius,
        fill=255,
    )
    img.putalpha(mask)

    # --- Try to get a bold font ---
    font_p = None
    font_maxx = None
    # Preferred bold fonts on macOS
    bold_fonts = [
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
        "/System/Library/Fonts/Supplemental/Helvetica Bold.ttf",
        "/Library/Fonts/Arial Bold.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
        "/System/Library/Fonts/SFNSDisplay.ttf",
        "/System/Library/Fonts/SFNS.ttf",
    ]
    chosen_font = None
    for fp in bold_fonts:
        if os.path.exists(fp):
            chosen_font = fp
            break

    p_size = 620
    maxx_size = 100
    if chosen_font:
        try:
            font_p = ImageFont.truetype(chosen_font, p_size)
            font_maxx = ImageFont.truetype(chosen_font, maxx_size)
        except Exception:
            font_p = None
            font_maxx = None

    if font_p is None:
        # Fallback to default
        font_p = ImageFont.load_default()
        font_maxx = ImageFont.load_default()

    # --- Glow layer behind the P ---
    glow = Image.new("RGBA", (ICON_SIZE, ICON_SIZE), (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow)

    # Get bounding box for centering
    p_bbox = glow_draw.textbbox((0, 0), "P", font=font_p)
    p_w = p_bbox[2] - p_bbox[0]
    p_h = p_bbox[3] - p_bbox[1]
    p_x = (ICON_SIZE - p_w) // 2 - p_bbox[0]
    p_y = (ICON_SIZE - p_h) // 2 - p_bbox[1] - 40  # shift up to make room for MAXX

    # Draw the glow P (larger, blurred, semi-transparent green)
    glow_draw.text((p_x, p_y), "P", fill=(0, 255, 136, 120), font=font_p)
    glow = glow.filter(ImageFilter.GaussianBlur(radius=40))

    # Second glow pass — tighter
    glow2 = Image.new("RGBA", (ICON_SIZE, ICON_SIZE), (0, 0, 0, 0))
    glow2_draw = ImageDraw.Draw(glow2)
    glow2_draw.text((p_x, p_y), "P", fill=(0, 255, 136, 80), font=font_p)
    glow2 = glow2.filter(ImageFilter.GaussianBlur(radius=18))

    # Outer halo — very wide, dim
    halo = Image.new("RGBA", (ICON_SIZE, ICON_SIZE), (0, 0, 0, 0))
    halo_draw = ImageDraw.Draw(halo)
    halo_draw.text((p_x, p_y), "P", fill=(0, 255, 136, 40), font=font_p)
    halo = halo.filter(ImageFilter.GaussianBlur(radius=80))

    # Composite glows onto main image
    img = Image.alpha_composite(img, halo)
    img = Image.alpha_composite(img, glow)
    img = Image.alpha_composite(img, glow2)

    # --- Draw the main P ---
    main_layer = Image.new("RGBA", (ICON_SIZE, ICON_SIZE), (0, 0, 0, 0))
    main_draw = ImageDraw.Draw(main_layer)
    main_draw.text((p_x, p_y), "P", fill=(0, 255, 136, 255), font=font_p)  # #00ff88
    img = Image.alpha_composite(img, main_layer)

    # --- Draw "MAXX" text below ---
    maxx_layer = Image.new("RGBA", (ICON_SIZE, ICON_SIZE), (0, 0, 0, 0))
    maxx_draw = ImageDraw.Draw(maxx_layer)
    maxx_bbox = maxx_draw.textbbox((0, 0), "MAXX", font=font_maxx)
    maxx_w = maxx_bbox[2] - maxx_bbox[0]
    maxx_x = (ICON_SIZE - maxx_w) // 2 - maxx_bbox[0]
    maxx_y = p_y + p_h + 20
    # Subtle glow behind MAXX
    maxx_glow = Image.new("RGBA", (ICON_SIZE, ICON_SIZE), (0, 0, 0, 0))
    mg_draw = ImageDraw.Draw(maxx_glow)
    mg_draw.text((maxx_x, maxx_y), "MAXX", fill=(255, 255, 255, 60), font=font_maxx)
    maxx_glow = maxx_glow.filter(ImageFilter.GaussianBlur(radius=8))
    img = Image.alpha_composite(img, maxx_glow)

    maxx_draw.text((maxx_x, maxx_y), "MAXX", fill=(255, 255, 255, 230), font=font_maxx)
    img = Image.alpha_composite(img, maxx_layer)

    # --- Add subtle top highlight / shine ---
    shine = Image.new("RGBA", (ICON_SIZE, ICON_SIZE), (0, 0, 0, 0))
    shine_draw = ImageDraw.Draw(shine)
    for y in range(200):
        alpha = int(12 * (1 - y / 200))
        shine_draw.line([(100, y), (ICON_SIZE - 100, y)], fill=(255, 255, 255, alpha))
    img = Image.alpha_composite(img, shine)

    # Save
    img.save(OUTPUT_PNG, "PNG")
    print(f"Icon saved: {OUTPUT_PNG}")
    return img


def create_iconset(img):
    """Create .iconset directory with all required sizes."""
    if os.path.exists(ICONSET_DIR):
        shutil.rmtree(ICONSET_DIR)
    os.makedirs(ICONSET_DIR)

    # Required sizes for macOS iconset:
    # icon_16x16.png, icon_16x16@2x.png (32),
    # icon_32x32.png, icon_32x32@2x.png (64),
    # icon_128x128.png, icon_128x128@2x.png (256),
    # icon_256x256.png, icon_256x256@2x.png (512),
    # icon_512x512.png, icon_512x512@2x.png (1024)
    sizes = [
        ("icon_16x16.png", 16),
        ("icon_16x16@2x.png", 32),
        ("icon_32x32.png", 32),
        ("icon_32x32@2x.png", 64),
        ("icon_128x128.png", 128),
        ("icon_128x128@2x.png", 256),
        ("icon_256x256.png", 256),
        ("icon_256x256@2x.png", 512),
        ("icon_512x512.png", 512),
        ("icon_512x512@2x.png", 1024),
    ]

    for name, size in sizes:
        resized = img.resize((size, size), Image.LANCZOS)
        resized.save(os.path.join(ICONSET_DIR, name), "PNG")
        print(f"  Created {name} ({size}x{size})")


def convert_to_icns():
    """Use iconutil to convert .iconset to .icns"""
    result = subprocess.run(
        ["iconutil", "-c", "icns", ICONSET_DIR, "-o", ICNS_OUTPUT],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        print(f"iconutil error: {result.stderr}")
        raise RuntimeError(f"iconutil failed: {result.stderr}")
    print(f"ICNS created: {ICNS_OUTPUT}")

    # Clean up iconset directory
    shutil.rmtree(ICONSET_DIR)
    print("Cleaned up .iconset directory")


if __name__ == "__main__":
    print("Generating PRINTMAXX Panel icon...")
    icon_img = create_icon()
    print("Creating iconset...")
    create_iconset(icon_img)
    print("Converting to .icns...")
    convert_to_icns()
    print("Done!")
