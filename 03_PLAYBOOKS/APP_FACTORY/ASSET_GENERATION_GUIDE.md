# Asset Generation Guide

Open source libraries for icons/illustrations + AI generation with Gemini/Nano Banana for custom assets.

---

## Quick Start: Automated Icon Generation

**API Key:** `/.env` → `GEMINI_API_KEY`
**Script:** `scripts/generate_icons.py`
**Output:** `assets/icons/`

```bash
# List available apps
python scripts/generate_icons.py --list

# Generate single icon
python scripts/generate_icons.py --app biomaxx

# Generate all icons
python scripts/generate_icons.py --all

# Just see the prompt (for use in other tools)
python scripts/generate_icons.py --app biomaxx --prompt-only
```

**Note:** Gemini API requires billing enabled for image generation. If you hit rate limits:
1. Enable billing at https://console.cloud.google.com/billing
2. Or use the `--prompt-only` flag and paste into Midjourney/DALL-E

---

## Open source icon libraries (free commercial use)

### Large collections

| Library | Icons | License | Best for |
|---------|-------|---------|----------|
| [Iconoir](https://iconoir.com/) | 1,500+ | MIT | Clean, minimal UI icons |
| [Remix Icon](https://remixicon.com/) | 2,700+ | Apache 2.0 | System icons, neutral style |
| [Lucide](https://lucide.dev/) | 1,400+ | ISC | Feather-style, React/Vue support |
| [Tabler Icons](https://tabler-icons.io/) | 5,900+ | MIT | Comprehensive, 24x24 grid |
| [Heroicons](https://heroicons.com/) | 450+ | MIT | Tailwind CSS integration |
| [Phosphor Icons](https://phosphoricons.com/) | 6,000+ | MIT | 6 weights per icon |
| [SVG Repo](https://www.svgrepo.com/) | 500,000+ | Various | Massive collection, check license per icon |

### When to use open source

Use open source for:
- UI elements (navigation, buttons, indicators)
- System icons (settings, profile, menu)
- Generic placeholders
- Rapid prototyping

Don't use open source for:
- App store icon (needs to be unique)
- Brand identity (mascots, logos)
- Marketing materials (screenshots, promo)

---

## Free illustration libraries

| Library | Style | Count | License |
|---------|-------|-------|---------|
| [unDraw](https://undraw.co/) | Flat vector | 500+ | MIT |
| [Open Peeps](https://www.openpeeps.com/) | Hand-drawn people | Modular | CC0 |
| [Illustrations.co](https://illlustrations.co/) | Flat colorful | 120+ | MIT |
| [Khagwal 3D](https://www.khagwal.com/) | 3D Blender | 45+ | CC0 |
| [Pixels Market](https://pixels.market/) | Flat to isometric | 15,000+ | Free commercial |
| [Thiings](https://thiings.co/) | AI 3D isometric | 1,900+ | Free commercial |

### Style consistency

Pick one library and stick with it per app. Mixing styles looks amateur.

```
PrayerLock: unDraw (clean, professional, faith-appropriate)
WalkToUnlock: Open Peeps (human, friendly, fitness vibe)
AI tools: Khagwal 3D (tech, modern)
```

---

## AI asset generation (Gemini/Nano Banana)

### What is Nano Banana?

Nano Banana is the community nickname for Gemini's image generation:
- **Nano Banana (Fast):** Gemini 2.5 Flash Image, quick generations
- **Nano Banana Pro (Thinking):** Gemini 3 Pro Image, best quality

Key advantages:
- Perfect text rendering (logos, UI mockups)
- Up to 14 reference images for style consistency
- Search grounding for accurate real-world elements
- Natural language prompts (no "4k, masterpiece" spam needed)

### Prompt structure

```
[Subject + Adjectives] doing [Action] in [Location/Context].
[Composition/Camera Angle].
[Lighting/Atmosphere].
[Style/Media].
```

### App icon prompts (copy-paste ready)

**Faith app icon (PrayerLock):**
```
A minimal app icon design. Centered composition showing hands clasped in prayer, soft golden glow emanating from above. Clean flat design with subtle gradient. Rounded square format suitable for iOS app store. Calming blue and gold color palette. Professional app icon style.
```

**Fitness app icon (WalkToUnlock):**
```
A minimal app icon design. Centered composition showing a running shoe footprint with motion lines. Energetic but clean style. Rounded square format for iOS app store. Vibrant green and white color palette. Modern flat design with subtle shadows.
```

**Habit tracker icon:**
```
A minimal app icon design. Centered checkmark inside a circle, with subtle streak lines suggesting progress. Clean geometric style. Rounded square format for iOS. Purple and white color palette. Modern flat design.
```

**AI tool icon:**
```
A minimal app icon design. Abstract brain or neural network pattern, geometric and modern. Gradient from electric blue to purple. Clean lines, no detail clutter. Rounded square format for iOS app store. Tech startup aesthetic.
```

### Mascot prompts

**Faith mascot (praying angel character):**
```
A cute cartoon mascot character. Simple chibi-style angel with tiny wings, hands together in prayer, peaceful expression. Soft pastel colors, primarily white and gold. Clean vector illustration style suitable for mobile app. Front-facing, minimal details, friendly and approachable.
```

**Fitness mascot (running dog):**
```
A cute cartoon mascot character. Happy golden retriever puppy running, tongue out, wearing a small sweatband. Energetic pose with one paw forward. Simple flat illustration style, bright colors. Suitable for mobile app branding. Side profile view.
```

**AI mascot (friendly robot):**
```
A cute cartoon mascot character. Small friendly robot with rounded features, glowing blue eyes, simple geometric body. Waving one hand. Clean minimal design, tech-friendly but approachable. Light gray and blue color scheme. Suitable for mobile app icon and branding.
```

### App store screenshot mockups

**Feature highlight:**
```
Professional app store screenshot mockup. iPhone 15 Pro displaying [app screen description]. Clean background gradient from [color] to [color]. Bold headline text above phone: "[Feature headline]". Subtext below: "[Supporting text]". Marketing style, polished.
```

**Lifestyle shot:**
```
Lifestyle photography mockup. Person holding iPhone naturally, screen showing [app name] interface. Morning light, cozy home setting. Warm, inviting atmosphere. Focus on phone screen with blurred background. Professional stock photo style.
```

### Browser automation for bulk generation

Use Playwright to automate Gemini for batch asset creation.

```python
from playwright.sync_api import sync_playwright
import time

def generate_asset(prompt, output_path):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        # Navigate to Gemini
        page.goto("https://gemini.google.com/app")

        # Wait for login if needed
        time.sleep(3)

        # Find prompt input
        prompt_input = page.locator('textarea[placeholder*="Enter"]')
        prompt_input.fill(prompt)

        # Submit
        page.keyboard.press('Enter')

        # Wait for generation
        time.sleep(30)  # Adjust based on complexity

        # Download generated image
        # (Implementation depends on Gemini's UI structure)

        browser.close()

# Batch generation
prompts = [
    "Faith app icon: hands in prayer, golden glow, flat design...",
    "Fitness app icon: running shoe, green gradient, minimal...",
    "AI app icon: neural network, blue-purple gradient, geometric...",
]

for i, prompt in enumerate(prompts):
    generate_asset(prompt, f"assets/icon_{i}.png")
```

---

## Asset workflow

### Phase 1: MVP (speed priority)

1. Use open source icons for all UI elements
2. Generate 1 app icon with Gemini
3. Use unDraw illustrations for onboarding
4. Screenshot real app for app store images

Time: 2-4 hours

### Phase 2: Polish (quality priority)

1. Generate custom mascot with Gemini
2. Create consistent illustration set (5-10 images)
3. Professional app store screenshots
4. Marketing assets (social media, ads)

Time: 1-2 days

### Phase 3: Brand (scale priority)

1. Full mascot character sheet
2. Animation frames for mascot
3. Multiple icon variants (light/dark mode)
4. Complete marketing asset library

Time: 1 week

---

## Don't overproduce

User quote: "dont wannt be basic bitch look same as every other app"

Balance:
- App icon: Custom (unique = recognizable in app drawer)
- UI icons: Open source (no one notices, save time)
- Onboarding: 3-5 custom illustrations (first impression matters)
- Marketing: Batch generate as needed

**MVP rule:** Ship with 80% open source, 20% custom. Iterate based on user feedback.

---

## Quality checklist

### App icon
- [ ] Recognizable at 60x60px
- [ ] Works on light and dark backgrounds
- [ ] No fine details that disappear when small
- [ ] Unique, not generic template look
- [ ] Matches app's personality

### Illustrations
- [ ] Consistent style across all images
- [ ] Colors match brand palette
- [ ] Appropriate for target audience
- [ ] Not offensive or exclusionary
- [ ] Loads fast (optimized file size)

### Screenshots
- [ ] Shows actual app (not mockups of different app)
- [ ] Text is readable
- [ ] Follows Apple/Google guidelines
- [ ] Highlights key features
- [ ] Has clear call to action

---

## Tools

### Generation
- [Gemini](https://gemini.google.com/) - Image generation (Nano Banana)
- [Midjourney](https://midjourney.com/) - Alternative for style variety
- [DALL-E 3](https://openai.com/dall-e-3) - Good for realistic images

### Editing
- [Figma](https://figma.com/) - Vector editing, mockups
- [Canva](https://canva.com/) - Quick marketing assets
- [Remove.bg](https://remove.bg/) - Background removal
- [Squoosh](https://squoosh.app/) - Image compression

### Conversion
- [CloudConvert](https://cloudconvert.com/) - Format conversion
- [TinyPNG](https://tinypng.com/) - PNG/JPEG compression
- [SVGOMG](https://jakearchibald.github.io/svgomg/) - SVG optimization

---

## File organization

```
APP_FACTORY/assets/
├── icons/
│   ├── prayerlock/
│   │   ├── app_icon_1024.png
│   │   ├── app_icon_512.png
│   │   └── app_icon_180.png
│   └── walktounlock/
│       └── ...
├── mascots/
│   ├── prayerlock_angel.png
│   └── walktounlock_dog.png
├── illustrations/
│   ├── onboarding_1.png
│   ├── onboarding_2.png
│   └── onboarding_3.png
├── screenshots/
│   ├── ios/
│   └── android/
└── marketing/
    ├── social/
    └── ads/
```

---

## Sources

- [Toools.design - 50+ Free Icon Libraries](https://www.toools.design/free-open-source-icon-libraries)
- [Lineicons - Best Open Source Icon Libraries 2026](https://lineicons.com/blog/best-open-source-icon-libraries)
- [Toolfolio - 25+ Free Illustration Libraries](https://toolfolio.io/productive-value/free-open-source-illustrations-library)
- [Atlabs - Nano Banana Pro Prompting Guide](https://www.atlabs.ai/blog/the-ultimate-nano-banana-pro-prompting-guide-mastering-gemini-3-pro-image)
- [GitHub - awesome-nanobanana-pro](https://github.com/ZeroLu/awesome-nanobanana-pro)

---

Created: 2026-01-21
