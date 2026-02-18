# Lock Apps Icon Generation Prompts V3

Production-ready prompts for generating app icons for the Lock Apps suite. All icons use modern 3D style with depth, gradients, and unique color schemes.

---

## Technical Specifications

**Required for ALL icons:**
- Primary size: 1024x1024 (App Store requirement)
- Additional sizes: 180x180 (iPhone), 167x167 (iPad Pro), 152x152 (iPad)
- Format: PNG
- Color space: sRGB
- NO transparency, NO alpha channel
- NO text in icon (Apple rejects text)
- NO rounded corners in source (iOS adds them automatically)
- Background: Solid color or gradient (no transparency)

---

## 1. PrayerLock

### Target Market
Faith niche (interfaith - Islamic, Christian, Hindu, Buddhist). Primary focus on daily prayer/meditation habits.

### Color Scheme
- Primary: Deep teal (#0d9488)
- Accent: Gold (#e0b87a)
- Background gradient: Dark teal to lighter teal

### AI Image Generation Prompt (Gemini/DALL-E/Midjourney)

```
Create a modern 3D app icon for a prayer/meditation app, 1024x1024 pixels, no text.

Style: Clean, modern 3D design with depth and soft shadows. Premium spiritual aesthetic.

Central element: Islamic geometric star pattern (8-pointed star) OR crescent moon, rendered in 3D with beveled edges and subtle metallic finish.

Color palette:
- Background: Gradient from deep teal (#0d9488) to lighter teal (#14b8a6)
- Star/crescent: Gold (#e0b87a) with subtle shine and highlights
- Shadows: Soft purple-tinted shadows for depth

Details:
- The geometric star should have clean, precise edges
- Add subtle ambient occlusion for depth
- Soft glow around the star/crescent (not harsh)
- Professional, premium feel
- No transparency, solid background
- No text or letters
- No rounded corners (iOS adds them)

Lighting: Soft top-left light source, creating gentle highlights and shadows.

Output: 1024x1024px PNG, sRGB color space, no alpha channel.
```

### Gemini API Prompt

```json
{
  "prompt": "Modern 3D app icon, 1024x1024, Islamic geometric 8-pointed star in metallic gold (#e0b87a) on gradient teal background (#0d9488 to #14b8a6), soft shadows, beveled edges, ambient occlusion, professional spiritual aesthetic, no text, no transparency, no rounded corners, soft glow, premium quality",
  "number_of_images": 4,
  "aspect_ratio": "1:1"
}
```

### Fallback: Figma/Canva Instructions

1. Create 1024x1024 canvas
2. Background: Linear gradient, deep teal (#0d9488) top to lighter teal (#14b8a6) bottom
3. Draw 8-pointed Islamic star using pen tool OR import free geometric star SVG
4. Color star: Gold (#e0b87a)
5. Add effects:
   - Inner shadow (soft, 5px blur, 20% opacity)
   - Drop shadow (10px offset, 15px blur, 30% opacity, dark purple #1e293b)
   - Slight outer glow (gold, 3px, 10% opacity)
6. Export as PNG, 1024x1024, sRGB, no transparency

---

## 2. WalkToUnlock

### Target Market
Fitness niche. Lock phone until daily step count achieved.

### Color Scheme
- Primary: Vibrant green (#22c55e)
- Accent: Blue (#3b82f6)
- Background gradient: Light blue to green

### AI Image Generation Prompt (Gemini/DALL-E/Midjourney)

```
Create a modern 3D app icon for a fitness walking app, 1024x1024 pixels, no text.

Style: Energetic, modern 3D design with motion and depth. Athletic aesthetic.

Central element: Stylized 3D footprint OR curved walking path/trail, rendered with depth and gradient.

Color palette:
- Background: Gradient from light blue (#60a5fa) to vibrant green (#22c55e), suggesting movement
- Footprint/path: Solid blue (#3b82f6) with white highlights
- Shadows: Soft green-tinted shadows

Details:
- If footprint: Single shoe print, angled slightly for dynamism, with tread texture
- If path: Curved trail/road with perspective depth, leading into distance
- Add subtle motion blur or speed lines (minimal)
- Clean, athletic, motivating feel
- No transparency, solid background
- No text or letters
- No rounded corners (iOS adds them)

Lighting: Bright, energetic lighting from top-right, creating sharp highlights.

Output: 1024x1024px PNG, sRGB color space, no alpha channel.
```

### Gemini API Prompt

```json
{
  "prompt": "Modern 3D app icon, 1024x1024, stylized blue footprint (#3b82f6) with white highlights on gradient background light blue (#60a5fa) to vibrant green (#22c55e), athletic aesthetic, motion energy, depth shadows, clean sporty design, no text, no transparency, no rounded corners, bright lighting",
  "number_of_images": 4,
  "aspect_ratio": "1:1"
}
```

### Fallback: Figma/Canva Instructions

1. Create 1024x1024 canvas
2. Background: Linear gradient, light blue (#60a5fa) top to vibrant green (#22c55e) bottom, 45-degree angle
3. Draw stylized footprint shape (use ellipse + rectangle for shoe sole, add tread lines)
4. Color footprint: Blue (#3b82f6)
5. Add effects:
   - White inner highlight (top-left, 40% opacity)
   - Drop shadow (8px offset, 12px blur, 25% opacity, dark green)
   - Slight outer glow (white, 2px, 15% opacity for energy)
6. Optional: Add 2-3 curved lines behind footprint for motion (subtle)
7. Export as PNG, 1024x1024, sRGB, no transparency

---

## 3. StudyLock

### Target Market
Students niche. Lock phone until study session complete.

### Color Scheme
- Primary: Purple (#8b5cf6)
- Accent: Indigo (#6366f1)
- Background gradient: Deep indigo to lighter purple

### AI Image Generation Prompt (Gemini/DALL-E/Midjourney)

```
Create a modern 3D app icon for a study/focus app, 1024x1024 pixels, no text.

Style: Smart, premium 3D design with depth and sophistication. Academic aesthetic.

Central element: Open book (3D, pages visible) OR stylized lightbulb, rendered with clean geometry and gradients.

Color palette:
- Background: Gradient from deep indigo (#4f46e5) to lighter purple (#a78bfa)
- Book/lightbulb: Bright purple (#8b5cf6) with white/gold highlights on pages or glass
- Shadows: Soft blue-purple shadows

Details:
- If book: Open book with visible pages, slight curl, depth between pages, bookmark ribbon (indigo)
- If lightbulb: Modern minimal bulb with glowing filament, clean glass surface
- Add subtle knowledge/insight symbolism (sparkles or light rays, minimal)
- Professional, academic, premium feel
- No transparency, solid background
- No text or letters
- No rounded corners (iOS adds them)

Lighting: Soft centered lighting, creating gentle highlights on central element.

Output: 1024x1024px PNG, sRGB color space, no alpha channel.
```

### Gemini API Prompt

```json
{
  "prompt": "Modern 3D app icon, 1024x1024, open book in bright purple (#8b5cf6) with white page highlights on gradient background deep indigo (#4f46e5) to light purple (#a78bfa), academic premium aesthetic, depth between pages, subtle sparkles, professional, no text, no transparency, no rounded corners, soft centered lighting",
  "number_of_images": 4,
  "aspect_ratio": "1:1"
}
```

### Fallback: Figma/Canva Instructions

1. Create 1024x1024 canvas
2. Background: Linear gradient, deep indigo (#4f46e5) top to lighter purple (#a78bfa) bottom
3. Draw open book:
   - Two rounded rectangles for pages, slightly angled outward
   - Thin rectangle in center for spine
4. Color book: Purple (#8b5cf6) for cover, white (#f8fafc) for pages
5. Add effects:
   - Pages: Inner shadow (soft, 3px blur, 15% opacity)
   - Book: Drop shadow (10px offset, 15px blur, 30% opacity, dark indigo)
   - Add thin indigo (#6366f1) bookmark ribbon coming from top
   - Optional: 2-3 small star sparkles above book (gold #fbbf24, 10% opacity)
6. Export as PNG, 1024x1024, sRGB, no transparency

---

## 4. FocusLock

### Target Market
Productivity niche. Lock phone until focus session (Pomodoro/deep work) complete.

### Color Scheme
- Primary: Orange (#f97316)
- Accent: Red (#ef4444)
- Background gradient: Deep red to bright orange

### AI Image Generation Prompt (Gemini/DALL-E/Midjourney)

```
Create a modern 3D app icon for a productivity focus app, 1024x1024 pixels, no text.

Style: Bold, energetic 3D design with sharp focus and intensity. Productivity aesthetic.

Central element: Bullseye target with concentric circles OR stylized flame, rendered in 3D with depth and gradients.

Color palette:
- Background: Gradient from deep red (#dc2626) to bright orange (#fb923c)
- Target/flame: Orange (#f97316) center with red (#ef4444) outer rings or flame base
- Shadows: Soft warm shadows

Details:
- If target: 3D concentric circles with depth, centered dot, precise geometry
- If flame: Modern geometric flame shape, layered, with inner glow
- Add subtle intensity/energy (minimal rays or subtle pulse effect)
- Bold, focused, motivating feel
- No transparency, solid background
- No text or letters
- No rounded corners (iOS adds them)

Lighting: Strong directional lighting from top, creating dramatic highlights and shadows.

Output: 1024x1024px PNG, sRGB color space, no alpha channel.
```

### Gemini API Prompt

```json
{
  "prompt": "Modern 3D app icon, 1024x1024, bullseye target in orange (#f97316) center with red (#ef4444) concentric rings on gradient background deep red (#dc2626) to bright orange (#fb923c), bold productivity aesthetic, depth between rings, geometric precision, intense focus, no text, no transparency, no rounded corners, strong top lighting",
  "number_of_images": 4,
  "aspect_ratio": "1:1"
}
```

### Fallback: Figma/Canva Instructions

1. Create 1024x1024 canvas
2. Background: Linear gradient, deep red (#dc2626) top to bright orange (#fb923c) bottom
3. Draw bullseye target:
   - 4 concentric circles (largest to smallest)
   - Colors alternate: red (#ef4444), orange (#f97316), red, orange (center)
4. Add 3D depth:
   - Each ring: Inner shadow (2px blur, 20% opacity, makes rings recede)
   - Center dot: Slight outer glow (white, 3px, 15% opacity)
5. Add effects:
   - Entire target: Drop shadow (12px offset, 18px blur, 35% opacity, dark red)
   - Optional: 4-6 subtle rays emanating from center (orange, 5% opacity, thin lines)
6. Export as PNG, 1024x1024, sRGB, no transparency

---

## Batch Generation Workflow

### Option 1: Gemini API (Recommended for consistency)

```bash
# Install Gemini SDK
pip install google-generativeai

# Python script to generate all 4 icons
python AUTOMATIONS/generate_lock_app_icons.py
```

Script should:
1. Loop through all 4 apps
2. Call Gemini API with each prompt
3. Generate 4 variations per app
4. Save to `MONEY_METHODS/APP_FACTORY/assets/icons/[app_name]/`
5. Pick best variation
6. Resize to all required sizes (1024, 180, 167, 152)

### Option 2: Midjourney Batch

```
/imagine [paste PrayerLock prompt] --ar 1:1 --v 6
/imagine [paste WalkToUnlock prompt] --ar 1:1 --v 6
/imagine [paste StudyLock prompt] --ar 1:1 --v 6
/imagine [paste FocusLock prompt] --ar 1:1 --v 6
```

Select best, upscale to 1024x1024, remove background if needed.

### Option 3: DALL-E 3 (ChatGPT Plus)

Paste each prompt into ChatGPT with DALL-E 3, generate 2-3 variations, pick best, download at highest resolution.

---

## Post-Generation Checklist

For EACH icon, verify:

- [ ] 1024x1024 primary size exists
- [ ] Additional sizes generated (180, 167, 152)
- [ ] PNG format, sRGB color space
- [ ] No transparency, no alpha channel
- [ ] No text in icon
- [ ] No rounded corners in source file
- [ ] Colors match specified palette
- [ ] Icon is recognizable at 40x40 (test by scaling down)
- [ ] Icon works on both light and dark backgrounds
- [ ] Passes Apple Human Interface Guidelines review

---

## Icon File Naming Convention

```
[app_name]_icon_1024.png   (App Store)
[app_name]_icon_180.png    (iPhone)
[app_name]_icon_167.png    (iPad Pro)
[app_name]_icon_152.png    (iPad)
```

Example:
```
PrayerLock_icon_1024.png
PrayerLock_icon_180.png
PrayerLock_icon_167.png
PrayerLock_icon_152.png
```

---

## A/B Testing Recommendations

Generate 2-3 variations per app for testing:

**PrayerLock:**
- Variation A: 8-pointed star
- Variation B: Crescent moon
- Variation C: Prayer beads (geometric)

**WalkToUnlock:**
- Variation A: Single footprint
- Variation B: Walking path/trail
- Variation C: Shoe outline

**StudyLock:**
- Variation A: Open book
- Variation B: Lightbulb
- Variation C: Graduation cap (minimal)

**FocusLock:**
- Variation A: Bullseye target
- Variation B: Flame
- Variation C: Clock/timer (minimal)

Test in App Store Connect with different audience segments.

---

## Tooling Reference

**AI Generation:**
- Gemini API: `google-generativeai` Python SDK
- Midjourney: Discord bot, `/imagine` command
- DALL-E 3: ChatGPT Plus or OpenAI API

**Manual Design:**
- Figma (free): figma.com
- Canva (free with limitations): canva.com
- Affinity Designer (one-time $70): affinity.serif.com

**Resizing/Optimization:**
- ImageMagick: `convert icon.png -resize 180x180 icon_180.png`
- Photoshop batch actions
- Online: squoosh.app (Google, lossless)

**Validation:**
- Apple Human Interface Guidelines: developer.apple.com/design/human-interface-guidelines/app-icons
- App Icon Generator (validation): appicon.co

---

## Notes

**biomaxx icon:** Already exists. Uses blue/cyan circadian rhythm theme with sun/moon gradient. Located at `MONEY_METHODS/APP_FACTORY/products/biomaxx/assets/icon_1024.png`.

**Color psychology:**
- Teal/gold (PrayerLock): Spiritual, calm, premium
- Green/blue (WalkToUnlock): Health, energy, movement
- Purple/indigo (StudyLock): Intelligence, focus, creativity
- Orange/red (FocusLock): Intensity, urgency, productivity

**Platform differences:**
- iOS adds rounded corners automatically (don't include in source)
- Android requires adaptive icons (separate foreground + background layers) - create later if needed
- macOS may require larger sizes (512x512, 1024x1024 @2x)

**Apple rejection risks:**
- Text in icon (even small) = rejection
- Emoji or Apple emoji style = rejection
- Looks too similar to Apple system icons = rejection
- Inappropriate content = rejection
- Misleading (e.g., fake notification badge) = rejection
