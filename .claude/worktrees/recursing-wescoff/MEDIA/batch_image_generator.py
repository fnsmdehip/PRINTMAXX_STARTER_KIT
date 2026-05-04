#!/usr/bin/env python3
"""
PRINTMAXX Image Factory — Batch Image Generator
Reads content files from CONTENT/social/posting_queue/,
creates HTML from templates, screenshots with Playwright.
Zero cost, pixel-perfect images.
"""

import json
import os
import re
import html
import sys
from pathlib import Path
from datetime import datetime

PROJECT_ROOT = Path(__file__).resolve().parent.parent
TEMPLATES_DIR = PROJECT_ROOT / "MEDIA" / "image_templates"
OUTPUT_DIR = PROJECT_ROOT / "MEDIA" / "generated_images"
CONTENT_DIR = PROJECT_ROOT / "CONTENT" / "social" / "posting_queue"
CATALOG_PATH = OUTPUT_DIR / "catalog.json"


def safe_path(target: Path) -> Path:
    resolved = Path(target).resolve()
    if not str(resolved).startswith(str(PROJECT_ROOT)):
        raise ValueError(f"BLOCKED: {resolved} is outside project root")
    return resolved


def load_catalog() -> list:
    if CATALOG_PATH.exists():
        return json.loads(CATALOG_PATH.read_text())
    return []


def save_catalog(catalog: list):
    safe_path(CATALOG_PATH)
    CATALOG_PATH.write_text(json.dumps(catalog, indent=2))


def extract_content(filepath: Path) -> dict:
    """Extract meaningful content from a posting queue file."""
    text = filepath.read_text().strip()
    lines = text.split("\n")

    # Parse metadata header if present
    HEADER_PREFIXES = ("PLATFORM:", "IMAGE:", "ACCOUNT:", "SCHEDULED:", "CHARACTER_COUNT:",
                       "THREAD:", "STATUS:", "SOURCE:", "QUALITY_GATE:")
    meta = {}
    body_start = 0
    has_header = any(line.strip().startswith(p) for line in lines[:10] for p in HEADER_PREFIXES)
    if has_header:
        for i, line in enumerate(lines):
            if line.strip() == "---":
                body_start = i + 1
                break
            if ":" in line and not line.strip().startswith("http"):
                key, val = line.split(":", 1)
                meta[key.strip().lower()] = val.strip()
        # If no --- found, skip all header lines
        if body_start == 0:
            body_start = next((i for i, l in enumerate(lines) if l.strip() and not any(l.strip().startswith(p) for p in HEADER_PREFIXES) and l.strip() != "---"), 0)

    body_lines = [l for l in lines[body_start:] if l.strip()]

    # Strip parenthetical labels like "(Durable price increase angle)"
    body_lines = [l for l in body_lines if not (l.strip().startswith("(") and l.strip().endswith(")"))]

    # For thread posts, get first tweet only
    tweet_lines = []
    in_tweet = False
    has_tweet_markers = any(line.startswith("[TWEET") for line in body_lines)
    for line in body_lines:
        if line.startswith("[TWEET 2") or line.startswith("[TWEET 3"):
            break
        if line.startswith("[TWEET 1"):
            in_tweet = True
            continue
        if in_tweet or not has_tweet_markers:
            tweet_lines.append(line)

    if not tweet_lines:
        tweet_lines = body_lines

    body = "\n".join(tweet_lines).strip()

    # Extract first strong line as hook
    hook = tweet_lines[0] if tweet_lines else ""
    subtitle = " ".join(tweet_lines[1:3]) if len(tweet_lines) > 1 else ""

    # Extract numbers — prefer the most impactful one (largest value, dollar amounts, percentages)
    numbers = re.findall(r'[\$]?[\d,]+\.?\d*[%KMBx]?', body)
    big_number = None
    best_score = 0
    for n in numbers:
        cleaned = n.replace(",", "").replace("$", "").replace("%", "").replace("K", "").replace("M", "").replace("B", "").replace("x", "")
        try:
            val = float(cleaned)
            if val <= 0:
                continue
            score = val
            if "$" in n:
                score *= 10  # Dollar amounts are more impactful
            if "M" in n:
                score *= 1000000
            elif "K" in n:
                score *= 1000
            elif "B" in n:
                score *= 1000000000
            if "%" in n:
                score *= 5  # Percentages are engaging
            if score > best_score:
                best_score = score
                big_number = n
        except ValueError:
            continue

    # Detect bullet points
    bullets = [l.strip().lstrip("- ").lstrip("* ") for l in tweet_lines if l.strip().startswith(("-", "*", "  -"))]

    return {
        "meta": meta,
        "body": body,
        "hook": hook,
        "subtitle": subtitle,
        "big_number": big_number,
        "bullets": bullets[:4],
        "source": meta.get("source", ""),
        "is_thread": meta.get("thread", "no").lower() == "yes" or len(bullets) >= 3,
    }


def classify_template(content: dict, filename: str) -> str:
    """Pick the best template for this content."""
    body = content["body"].lower()
    hook = content["hook"].lower()

    # Thread with bullets -> thread_card
    if content["is_thread"] and len(content["bullets"]) >= 3:
        return "thread_card"

    # Short quote/confession/hot take -> quote_card
    short_body = len(content["body"]) < 200
    is_quote = any(w in body for w in ["confession:", "hot take:", "the version of", "stop overthinking", "two types of"])
    if short_body and (is_quote or "quote" in filename or "confession" in filename or "bip_" in filename):
        return "quote_card"

    # Has a prominent number -> stat_highlight
    if content["big_number"] and any(w in body for w in ["%", "$", "days", "hours", "emails", "leads", "visitors", "month", "year", "cost", "revenue", "margin"]):
        return "stat_highlight"

    # App promos -> niche_card
    if "app_promo" in filename or "promo" in filename:
        return "niche_card"

    # Counter/competitor content -> social_card
    if "counter" in filename or "competitor" in filename:
        return "social_card"

    # Default: social_card for most tweet content
    return "social_card"


def escape(text: str) -> str:
    """HTML-escape text."""
    return html.escape(text)


def highlight_key_phrase(text: str) -> str:
    """Find a key phrase to highlight with gradient."""
    escaped = escape(text)

    # Patterns to highlight: numbers, dollar amounts, percentages, key phrases
    patterns = [
        (r'(\$[\d,]+\.?\d*[KMB]?(?:/(?:month|mo|year|yr))?)', r'<span class="highlight">\1</span>'),
        (r'(\d+[%])', r'<span class="highlight">\1</span>'),
        (r'(\d+(?:,\d+)*\+?\s*(?:agents?|products?|emails?|leads?|visitors?|customers?|pages?|websites?))', r'<span class="highlight">\1</span>'),
        (r'(\d+[xX]\s+\w+)', r'<span class="highlight">\1</span>'),
    ]

    for pattern, replacement in patterns:
        result = re.sub(pattern, replacement, escaped, count=1)
        if result != escaped:
            return result

    return escaped


def generate_social_card_html(content: dict) -> tuple:
    """Generate social_card HTML. Returns (html_string, width, height)."""
    hook = highlight_key_phrase(content["hook"])
    subtitle = escape(content["subtitle"][:120]) if content["subtitle"] else ""

    return (f"""<!DOCTYPE html>
<html><head><meta charset="utf-8">
<style>
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  body {{
    width: 1200px; height: 675px;
    background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 50%, #16213e 100%);
    font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', 'Inter', sans-serif;
    color: #ffffff; display: flex; flex-direction: column;
    justify-content: center; padding: 80px; overflow: hidden;
  }}
  .hook {{ font-size: 48px; font-weight: 800; line-height: 1.15; letter-spacing: -1px; margin-bottom: 24px; max-width: 900px; }}
  .hook .highlight {{ background: linear-gradient(90deg, #667eea, #764ba2); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }}
  .subtitle {{ font-size: 22px; font-weight: 400; color: rgba(255,255,255,0.55); max-width: 700px; line-height: 1.5; }}
  .brand {{ position: absolute; bottom: 40px; right: 60px; font-size: 18px; font-weight: 700; color: rgba(255,255,255,0.3); letter-spacing: 4px; text-transform: uppercase; }}
  .accent-bar {{ width: 60px; height: 4px; background: linear-gradient(90deg, #667eea, #764ba2); border-radius: 2px; margin-bottom: 32px; }}
</style></head>
<body>
  <div class="accent-bar"></div>
  <div class="hook">{hook}</div>
  <div class="subtitle">{subtitle}</div>
  <div class="brand">PRINTMAXX</div>
</body></html>""", 1200, 675)


def generate_quote_card_html(content: dict) -> tuple:
    """Generate quote_card HTML. Returns (html_string, width, height)."""
    # Use full body as quote, capped at reasonable length
    quote = escape(content["body"][:280])

    return (f"""<!DOCTYPE html>
<html><head><meta charset="utf-8">
<style>
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  body {{
    width: 1080px; height: 1080px; background: #0a0a0a;
    font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', 'Inter', sans-serif;
    color: #ffffff; display: flex; flex-direction: column;
    justify-content: center; align-items: center; padding: 100px; overflow: hidden;
  }}
  .quote-mark {{ font-size: 120px; font-weight: 900; background: linear-gradient(135deg, #667eea, #764ba2); -webkit-background-clip: text; -webkit-text-fill-color: transparent; line-height: 0.6; margin-bottom: 40px; }}
  .quote {{ font-size: 34px; font-weight: 600; line-height: 1.4; text-align: center; max-width: 800px; margin-bottom: 48px; }}
  .attribution {{ font-size: 20px; font-weight: 400; color: rgba(255,255,255,0.4); letter-spacing: 2px; text-transform: uppercase; }}
  .border-glow {{ position: absolute; top: 30px; left: 30px; right: 30px; bottom: 30px; border: 1px solid rgba(102, 126, 234, 0.2); border-radius: 8px; }}
</style></head>
<body>
  <div class="border-glow"></div>
  <div class="quote-mark">&ldquo;</div>
  <div class="quote">{quote}</div>
  <div class="attribution">@PRINTMAXXER</div>
</body></html>""", 1080, 1080)


def generate_stat_highlight_html(content: dict) -> tuple:
    """Generate stat_highlight HTML. Returns (html_string, width, height)."""
    big_num = escape(content["big_number"] or "0")
    context = escape(content["hook"][:120])
    detail = escape(content["subtitle"][:160]) if content["subtitle"] else ""

    return (f"""<!DOCTYPE html>
<html><head><meta charset="utf-8">
<style>
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  body {{
    width: 1200px; height: 675px;
    background: linear-gradient(135deg, #0a0a0a 0%, #0f0f1a 50%, #0a0a0a 100%);
    font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', 'Inter', sans-serif;
    color: #ffffff; display: flex; flex-direction: column;
    justify-content: center; padding: 80px; overflow: hidden; position: relative;
  }}
  .grid-overlay {{ position: absolute; top: 0; left: 0; right: 0; bottom: 0; background-image: linear-gradient(rgba(102,126,234,0.03) 1px, transparent 1px), linear-gradient(90deg, rgba(102,126,234,0.03) 1px, transparent 1px); background-size: 40px 40px; }}
  .big-number {{ font-size: 120px; font-weight: 900; background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #667eea 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; line-height: 1; letter-spacing: -4px; margin-bottom: 16px; position: relative; z-index: 1; }}
  .context {{ font-size: 34px; font-weight: 700; line-height: 1.3; max-width: 900px; margin-bottom: 20px; position: relative; z-index: 1; }}
  .detail {{ font-size: 20px; font-weight: 400; color: rgba(255,255,255,0.4); max-width: 700px; line-height: 1.5; position: relative; z-index: 1; }}
  .brand {{ position: absolute; bottom: 35px; right: 55px; font-size: 16px; font-weight: 700; color: rgba(255,255,255,0.15); letter-spacing: 4px; text-transform: uppercase; z-index: 1; }}
  .glow {{ position: absolute; top: 50%; left: -80px; transform: translateY(-50%); width: 300px; height: 300px; background: radial-gradient(circle, rgba(102,126,234,0.08) 0%, transparent 70%); border-radius: 50%; }}
</style></head>
<body>
  <div class="grid-overlay"></div>
  <div class="glow"></div>
  <div class="big-number">{big_num}</div>
  <div class="context">{context}</div>
  <div class="detail">{detail}</div>
  <div class="brand">PRINTMAXX</div>
</body></html>""", 1200, 675)


def generate_thread_card_html(content: dict) -> tuple:
    """Generate thread_card HTML. Returns (html_string, width, height)."""
    hook = highlight_key_phrase(content["hook"])
    bullets_html = "\n".join(f'    <div class="bullet">{escape(b[:80])}</div>' for b in content["bullets"][:4])

    return (f"""<!DOCTYPE html>
<html><head><meta charset="utf-8">
<style>
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  body {{
    width: 1200px; height: 675px;
    background: linear-gradient(160deg, #0a0a0a 0%, #0f0f23 40%, #1a1a2e 100%);
    font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', 'Inter', sans-serif;
    color: #ffffff; display: flex; flex-direction: column;
    justify-content: center; padding: 70px 80px; overflow: hidden; position: relative;
  }}
  .thread-indicator {{ display: flex; align-items: center; gap: 10px; margin-bottom: 28px; }}
  .thread-dot {{ width: 8px; height: 8px; border-radius: 50%; background: #667eea; }}
  .thread-line {{ width: 40px; height: 2px; background: rgba(102,126,234,0.3); }}
  .thread-label {{ font-size: 14px; font-weight: 600; color: rgba(102,126,234,0.7); letter-spacing: 2px; text-transform: uppercase; }}
  .hook {{ font-size: 44px; font-weight: 800; line-height: 1.15; letter-spacing: -1px; margin-bottom: 28px; max-width: 950px; }}
  .hook .highlight {{ background: linear-gradient(90deg, #667eea, #764ba2); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }}
  .bullets {{ display: flex; flex-direction: column; gap: 12px; }}
  .bullet {{ font-size: 20px; font-weight: 500; color: rgba(255,255,255,0.55); display: flex; align-items: center; gap: 12px; }}
  .bullet::before {{ content: ''; width: 6px; height: 6px; border-radius: 50%; background: linear-gradient(135deg, #667eea, #764ba2); flex-shrink: 0; }}
  .handle {{ position: absolute; bottom: 35px; right: 55px; font-size: 18px; font-weight: 600; color: rgba(255,255,255,0.2); }}
  .corner-glow {{ position: absolute; top: -100px; right: -100px; width: 350px; height: 350px; background: radial-gradient(circle, rgba(102,126,234,0.1) 0%, transparent 70%); border-radius: 50%; }}
</style></head>
<body>
  <div class="corner-glow"></div>
  <div class="thread-indicator">
    <div class="thread-dot"></div><div class="thread-line"></div>
    <div class="thread-label">THREAD</div>
  </div>
  <div class="hook">{hook}</div>
  <div class="bullets">
{bullets_html}
  </div>
  <div class="handle">@printmaxxer</div>
</body></html>""", 1200, 675)


def generate_niche_card_html(content: dict) -> tuple:
    """Generate niche_card HTML. Returns (html_string, width, height)."""
    hook = highlight_key_phrase(content["hook"])
    subtitle = escape(content["subtitle"][:120]) if content["subtitle"] else ""

    return (f"""<!DOCTYPE html>
<html><head><meta charset="utf-8">
<style>
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  body {{
    width: 1200px; height: 675px;
    background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 50%, #16213e 100%);
    font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', 'Inter', sans-serif;
    color: #ffffff; display: flex; flex-direction: column;
    justify-content: center; padding: 80px; overflow: hidden; position: relative;
  }}
  .accent-bar {{ width: 50px; height: 3px; background: linear-gradient(90deg, #667eea, #764ba2); border-radius: 2px; margin-bottom: 28px; }}
  .hook {{ font-size: 48px; font-weight: 800; line-height: 1.15; letter-spacing: -1px; margin-bottom: 24px; max-width: 900px; }}
  .highlight {{ background: linear-gradient(90deg, #667eea, #764ba2); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }}
  .subtitle {{ font-size: 22px; font-weight: 400; color: rgba(255,255,255,0.5); max-width: 700px; line-height: 1.5; }}
  .handle {{ position: absolute; bottom: 40px; right: 60px; font-size: 18px; font-weight: 600; color: rgba(255,255,255,0.25); }}
</style></head>
<body>
  <div class="accent-bar"></div>
  <div class="hook">{hook}</div>
  <div class="subtitle">{subtitle}</div>
  <div class="handle">@printmaxxer</div>
</body></html>""", 1200, 675)


GENERATORS = {
    "social_card": generate_social_card_html,
    "quote_card": generate_quote_card_html,
    "stat_highlight": generate_stat_highlight_html,
    "thread_card": generate_thread_card_html,
    "niche_card": generate_niche_card_html,
}

TEMPLATE_CATEGORIES = {
    "social_card": "Social Cards (1200x675)",
    "quote_card": "Quote Cards (1080x1080)",
    "stat_highlight": "Stat Highlights (1200x675)",
    "thread_card": "Thread Cards (1200x675)",
    "niche_card": "Niche Cards (1200x675)",
}


def make_image_id(filename: str) -> str:
    """Convert filename to image ID."""
    base = Path(filename).stem
    # Clean up for ID
    clean = re.sub(r'[^a-z0-9_]', '_', base.lower())
    clean = re.sub(r'_+', '_', clean).strip('_')
    return clean


def find_items_needing_images() -> list:
    """Find all content files in posting_queue that don't have matching images."""
    catalog = load_catalog()
    existing_ids = {entry["id"] for entry in catalog}
    existing_files = {f.stem for f in OUTPUT_DIR.glob("*.png")}

    needs = []
    for f in sorted(CONTENT_DIR.glob("*.txt")):
        img_id = make_image_id(f.name)
        if img_id not in existing_ids and img_id not in existing_files:
            needs.append(f)

    return needs


def generate_all():
    """Main generation loop."""
    from playwright.sync_api import sync_playwright

    items = find_items_needing_images()
    if not items:
        print("All content already has images. Nothing to generate.")
        return

    print(f"Found {len(items)} items needing images.")
    catalog = load_catalog()
    generated = 0
    errors = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)

        for filepath in items:
            try:
                content = extract_content(filepath)
                if not content["body"].strip():
                    continue

                template_type = classify_template(content, filepath.name)
                generator = GENERATORS.get(template_type, generate_social_card_html)
                html_str, width, height = generator(content)

                img_id = make_image_id(filepath.name)
                html_path = safe_path(OUTPUT_DIR / f"_temp_{img_id}.html")
                png_path = safe_path(OUTPUT_DIR / f"{img_id}.png")

                html_path.write_text(html_str)

                page = browser.new_page(viewport={"width": width, "height": height})
                page.goto(f"file://{html_path}")
                page.wait_for_timeout(200)
                page.screenshot(path=str(png_path), type="png")
                page.close()

                html_path.unlink()

                file_size = png_path.stat().st_size
                catalog.append({
                    "id": img_id,
                    "path": str(png_path),
                    "size": file_size,
                    "width": width,
                    "height": height,
                    "category": TEMPLATE_CATEGORIES.get(template_type, "Social Cards (1200x675)"),
                    "template": f"{template_type}.html",
                    "generated_at": datetime.now().isoformat(),
                    "paired_with": filepath.name,
                })

                generated += 1
                if generated % 10 == 0:
                    print(f"  Generated {generated}/{len(items)}...")

            except Exception as e:
                errors.append((filepath.name, str(e)))

        browser.close()

    save_catalog(catalog)
    print(f"\nDone: {generated} images generated, {len(errors)} errors.")
    if errors:
        print("Errors:")
        for name, err in errors[:10]:
            print(f"  {name}: {err}")


def status():
    """Show image factory status."""
    catalog = load_catalog()
    items_needing = find_items_needing_images()

    by_category = {}
    for entry in catalog:
        cat = entry.get("category", "Unknown")
        by_category[cat] = by_category.get(cat, 0) + 1

    print("IMAGE FACTORY STATUS")
    print(f"  Total images: {len(catalog)}")
    print(f"  Items needing images: {len(items_needing)}")
    print(f"  Categories:")
    for cat, count in sorted(by_category.items()):
        print(f"    {cat}: {count}")

    if items_needing:
        print(f"\n  Next 10 to generate:")
        for f in items_needing[:10]:
            content = extract_content(f)
            template = classify_template(content, f.name)
            print(f"    {f.name} -> {template}")


def regenerate_ids(ids: list):
    """Re-generate specific image IDs."""
    from playwright.sync_api import sync_playwright

    catalog = load_catalog()
    # Remove old entries for these IDs
    catalog = [e for e in catalog if e["id"] not in ids]
    # Remove old PNGs
    for img_id in ids:
        png = OUTPUT_DIR / f"{img_id}.png"
        if png.exists():
            png.unlink()

    # Find matching content files
    regen_files = []
    for f in CONTENT_DIR.glob("*.txt"):
        if make_image_id(f.name) in ids:
            regen_files.append(f)

    if not regen_files:
        print(f"No content files found matching IDs: {ids}")
        return

    print(f"Regenerating {len(regen_files)} images...")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        for filepath in regen_files:
            content = extract_content(filepath)
            if not content["body"].strip():
                continue
            template_type = classify_template(content, filepath.name)
            generator = GENERATORS.get(template_type, generate_social_card_html)
            html_str, width, height = generator(content)
            img_id = make_image_id(filepath.name)
            html_path = safe_path(OUTPUT_DIR / f"_temp_{img_id}.html")
            png_path = safe_path(OUTPUT_DIR / f"{img_id}.png")
            html_path.write_text(html_str)
            page = browser.new_page(viewport={"width": width, "height": height})
            page.goto(f"file://{html_path}")
            page.wait_for_timeout(200)
            page.screenshot(path=str(png_path), type="png")
            page.close()
            html_path.unlink()
            file_size = png_path.stat().st_size
            catalog.append({
                "id": img_id,
                "path": str(png_path),
                "size": file_size,
                "width": width,
                "height": height,
                "category": TEMPLATE_CATEGORIES.get(template_type, "Social Cards (1200x675)"),
                "template": f"{template_type}.html",
                "generated_at": datetime.now().isoformat(),
                "paired_with": filepath.name,
            })
            print(f"  Regenerated: {img_id} ({template_type})")
        browser.close()
    save_catalog(catalog)
    print("Done.")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--status":
        status()
    elif len(sys.argv) > 2 and sys.argv[1] == "--regenerate":
        regenerate_ids(sys.argv[2:])
    else:
        generate_all()
