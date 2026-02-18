#!/usr/bin/env python3
"""
Generate professional app icons using Gemini API.
Usage: python generate_icons.py --app biomaxx --style biohacking
"""

import os
import sys
import json
import base64
import requests
from pathlib import Path
from dotenv import load_dotenv

# Load env from project root
project_root = Path(__file__).parent.parent.parent.parent
load_dotenv(project_root / '.env')

GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
OUTPUT_DIR = Path(__file__).parent.parent / 'assets' / 'icons'

# App icon configurations with COMPETITOR-INFORMED design
# Each config includes competitor analysis for better prompts
APP_CONFIGS = {
    'biomaxx': {
        'name': 'BioMaxx',
        'niche': 'biohacking/longevity',
        'symbol': 'DNA helix intertwined with a lightning bolt, representing science meets optimization',
        'colors': 'emerald green (#10B981) to teal (#14B8A6)',
        'style': 'scientific, premium, futuristic',
        'background': 'dark slate (#0F172A)',
        'competitors': 'Zero (purple, minimal), Oura (silver ring), Whoop (red/black aggressive), Levels (green glucose)',
        'competitor_patterns': 'dark backgrounds, gradient fills, abstract symbols, single focal point',
        'differentiation': 'Vibrant emerald (not clinical blue/gray), combines science + energy, warmer than competitors',
        'avoid': 'clinical blue, literal organ imagery, flat design, cold/sterile feel',
    },
    'glowmaxx': {
        'name': 'GlowMaxx',
        'niche': 'looksmaxxing/self-improvement',
        'symbol': 'stylized face silhouette with radiant glow lines emanating outward',
        'colors': 'coral red (#FF6B6B) to warm pink (#FF8E8E)',
        'style': 'modern, aesthetic, aspirational beauty',
        'background': 'dark charcoal (#0F0F0F)',
        'competitors': 'UMAX (neon purple AI), Mewing apps (jaw focus), skincare trackers (clean white)',
        'competitor_patterns': 'face silhouettes, before/after motifs, progress indicators, aspirational imagery',
        'differentiation': 'Warm coral (stands out from cold purple/blue), glow effect suggests transformation',
        'avoid': 'harsh neon, clinical medical look, overly feminine pink, literal face photos',
    },
    'stepunlock': {
        'name': 'StepUnlock',
        'niche': 'fitness/walking/phone lock',
        'symbol': 'dynamic footprint with motion trails merging into an unlock/open padlock symbol',
        'colors': 'electric green (#4ADE80) to cyan (#22D3EE)',
        'style': 'energetic, achievement-focused, gamified',
        'background': 'deep blue (#1E3A5F)',
        'competitors': 'Opal (minimal purple), StepsApp (green circle), Sweatcoin (gold coin), Pedometer++ (red heart)',
        'competitor_patterns': 'circular progress rings, step counters, achievement badges, bright colors',
        'differentiation': 'Unique lock mechanism concept, motion trails suggest movement, gaming feel',
        'avoid': 'static imagery, plain step counter look, medical/health focus, boring circular gauge',
    },
    'devotionflow': {
        'name': 'DevotionFlow',
        'niche': 'faith/christian devotionals',
        'symbol': 'open book with elegant dove rising and soft light rays, suggesting scripture and spirit',
        'colors': 'warm gold (#E6B800) to amber (#F59E0B)',
        'style': 'peaceful, spiritual, elegant, reverent',
        'background': 'deep navy (#1A1A2E)',
        'competitors': 'Hallow (purple minimal), Glorify (modern gradient), Bible App (green book), Abide (soft blue)',
        'competitor_patterns': 'navy/gold combos, doves, books, light rays, generous whitespace, warm palettes',
        'differentiation': 'Combines book + dove (not just one), warmer gold than competitors silver/white',
        'avoid': 'cartoonish imagery, harsh colors, cluttered symbols, overly literal crosses',
    },
    'pelvicpro': {
        'name': 'PelvicPro',
        'niche': 'womens health/kegel training',
        'symbol': 'abstract lotus flower with subtle strength/core symbol, elegant and discreet',
        'colors': 'soft pink (#FF69B4) to purple (#A855F7)',
        'style': 'empowering, professional, discreet, supportive',
        'background': 'deep purple (#4A1942)',
        'competitors': 'Elvie (minimal teal), Perifit (playful pink), Squeezy NHS (medical blue), Kegel trainers (basic)',
        'competitor_patterns': 'abstract feminine shapes, lotus/flower motifs, soft gradients, professional not clinical',
        'differentiation': 'Elegant lotus suggests strength + femininity, premium purple gradient, empowering not medical',
        'avoid': 'anatomical imagery, clinical medical look, childish/cutesy design, obvious pelvic references',
    },
    'promptvault': {
        'name': 'PromptVault',
        'niche': 'AI/productivity/prompt management',
        'symbol': 'vault door with AI neural network circuit pattern integrated, secure knowledge storage',
        'colors': 'electric blue (#3B82F6) to purple (#8B5CF6)',
        'style': 'tech-forward, secure, intelligent, premium',
        'background': 'dark (#0F0F0F)',
        'competitors': 'Notion (minimal), ChatGPT (green), various AI tools (blue/purple gradients)',
        'competitor_patterns': 'neural networks, circuit patterns, brain imagery, blue/purple tech colors',
        'differentiation': 'Vault concept unique (security + storage), combines AI + security visually',
        'avoid': 'generic brain icon, plain robot face, too similar to ChatGPT green, cluttered circuits',
    },
    'focusprayer': {
        'name': 'FocusPrayer',
        'niche': 'faith/prayer timer/focus',
        'symbol': 'praying hands encircled by a subtle timer ring, focus meets faith',
        'colors': 'gold (#E6B800) to soft cream white (#FFF8E7)',
        'style': 'calm, focused, spiritual, meditative',
        'background': 'deep navy (#1A1A2E)',
        'competitors': 'Hallow, prayer apps (hands), focus apps (timers), meditation apps (circles)',
        'competitor_patterns': 'praying hands, timer elements, peaceful palettes, minimal designs',
        'differentiation': 'Merges prayer + focus timer concepts, warm gold glow, contemplative mood',
        'avoid': 'harsh timer graphics, clinical countdown look, overly ornate religious imagery',
    },
    'dailyanchor': {
        'name': 'DailyAnchor',
        'niche': 'faith/daily habits/grounding',
        'symbol': 'anchor with sunrise rays emerging behind it, grounding meets new beginnings',
        'colors': 'ocean blue (#0EA5E9) to sunrise gold (#F59E0B)',
        'style': 'grounding, hopeful, daily ritual, steadfast',
        'background': 'dark ocean blue (#0C4A6E)',
        'competitors': 'habit trackers (checkmarks), faith apps (religious symbols), morning routine apps',
        'competitor_patterns': 'nature imagery (sunrise, water), warm/cool color transitions, hopeful tones',
        'differentiation': 'Anchor = stability/grounding (unique in faith space), sunrise = daily renewal',
        'avoid': 'generic checkmark, plain anchor without context, overly nautical/sailor theme',
    },
    'learnlock': {
        'name': 'LearnLock',
        'niche': 'education/study focus/phone lock',
        'symbol': 'book with integrated lock mechanism and subtle graduation cap element',
        'colors': 'purple (#8B5CF6) to blue (#3B82F6)',
        'style': 'educational, achievement-focused, focused, smart',
        'background': 'dark (#1E1E2E)',
        'competitors': 'Forest (tree growing), Focus apps (timers), study apps (books), Opal (blocker)',
        'competitor_patterns': 'books, graduation caps, growth imagery, achievement badges, focus timers',
        'differentiation': 'Lock mechanism unique to study (earn access through learning), gamified education',
        'avoid': 'boring open book, generic graduation cap, childish school imagery, plain timer',
    },
}


def generate_icon_prompt(app_key: str) -> str:
    """Generate the Gemini prompt for an app icon with competitor-informed design."""
    config = APP_CONFIGS[app_key]

    prompt = f"""Create a professional mobile app icon for "{config['name']}" in the {config['niche']} space.

COMPETITOR CONTEXT:
Top competitors: {config['competitors']}
Common patterns in this niche: {config['competitor_patterns']}
Our differentiation strategy: {config['differentiation']}

DESIGN REQUIREMENTS:
- Symbol/Icon: {config['symbol']}
- Color Gradient: {config['colors']}
- Background: {config['background']}
- Style: {config['style']}

MUST INCLUDE (proven patterns from top apps):
- 3D depth with isometric or perspective view
- Glossy/glass finish with subtle reflections
- Soft glow effect around the main symbol
- Single clear focal point (not cluttered)
- Professional gradient execution
- Rounded corners (iOS app icon style)

MUST AVOID (based on competitor analysis):
- {config['avoid']}
- Plain flat design without dimension
- Text or letters in the icon
- Cluttered multiple symbols
- Generic stock icon look

DIFFERENTIATION (what makes us stand out):
{config['differentiation']}

TECHNICAL SPECS:
- Size: 1024x1024 pixels
- Must be recognizable at 60x60px (app drawer size)
- Must work on both light and dark backgrounds
- High contrast for visibility

Generate a single, stunning app icon that stands out in the App Store grid while fitting the {config['niche']} aesthetic. This should look like a $10M+ funded app, not a weekend project."""

    return prompt


def generate_icon_with_gemini(app_key: str, model: str = "gemini-2.0-flash-exp-image-generation") -> dict:
    """Call Gemini API to generate an icon using Gemini image generation."""
    if not GEMINI_API_KEY:
        return {'error': 'GEMINI_API_KEY not found in .env'}

    prompt = generate_icon_prompt(app_key)

    # Try multiple models in case one is rate limited
    models_to_try = [
        model,
        "imagen-3.0-generate-002",  # Google's Imagen model
        "gemini-2.0-flash-preview-image-generation",
    ]

    for model_name in models_to_try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={GEMINI_API_KEY}"

        payload = {
            "contents": [{
                "parts": [{
                    "text": prompt
                }]
            }],
            "generationConfig": {
                "responseModalities": ["image", "text"]
            }
        }

        try:
            response = requests.post(url, json=payload, timeout=120)
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 429:
                print(f"  Rate limited on {model_name}, trying next...")
                continue
            else:
                print(f"  {model_name}: {response.status_code}")
                continue
        except Exception as e:
            print(f"  {model_name}: {e}")
            continue

    return {'error': 'All models rate limited or failed'}


def save_icon(app_key: str, image_data: bytes) -> str:
    """Save the generated icon to file."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output_path = OUTPUT_DIR / f"{app_key}_icon.png"

    with open(output_path, 'wb') as f:
        f.write(image_data)

    return str(output_path)


def main():
    import argparse
    parser = argparse.ArgumentParser(description='Generate app icons with Gemini')
    parser.add_argument('--app', type=str, help='App key (e.g., biomaxx, glowmaxx)')
    parser.add_argument('--all', action='store_true', help='Generate all app icons')
    parser.add_argument('--list', action='store_true', help='List available apps')
    parser.add_argument('--prompt-only', action='store_true', help='Just print the prompt')

    args = parser.parse_args()

    if args.list:
        print("Available apps:")
        for key, config in APP_CONFIGS.items():
            print(f"  {key}: {config['name']} - {config['style']}")
        return

    if args.prompt_only and args.app:
        print(generate_icon_prompt(args.app))
        return

    apps_to_generate = list(APP_CONFIGS.keys()) if args.all else [args.app] if args.app else []

    if not apps_to_generate:
        parser.print_help()
        return

    for app_key in apps_to_generate:
        if app_key not in APP_CONFIGS:
            print(f"Unknown app: {app_key}")
            continue

        print(f"Generating icon for {APP_CONFIGS[app_key]['name']}...")
        result = generate_icon_with_gemini(app_key)

        if 'error' in result:
            print(f"  Error: {result['error']}")
        else:
            # Parse response and save image
            try:
                # Gemini returns image in candidates[0].content.parts
                parts = result.get('candidates', [{}])[0].get('content', {}).get('parts', [])
                for part in parts:
                    if 'inlineData' in part:
                        image_data = base64.b64decode(part['inlineData']['data'])
                        path = save_icon(app_key, image_data)
                        print(f"  Saved: {path}")
                        break
                else:
                    print(f"  No image in response")
                    print(f"  Response: {json.dumps(result, indent=2)[:500]}")
            except Exception as e:
                print(f"  Error parsing response: {e}")


if __name__ == '__main__':
    main()
