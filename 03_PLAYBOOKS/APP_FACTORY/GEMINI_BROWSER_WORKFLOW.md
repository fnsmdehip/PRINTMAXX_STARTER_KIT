# Gemini Browser Image Generation Workflow

**Purpose:** Generate high-quality app icons via Gemini browser UI with "Redo with Pro" for maximum quality.

**Why Browser vs API:** Gemini API has strict rate limits. Browser UI bypasses these and offers "Redo with Pro" for higher quality output.

---

## Quick Reference for Agents

### URLs
- Gemini: `https://gemini.google.com/app`
- AI Studio (alternative): `https://aistudio.google.com`

### Key DOM Selectors

```javascript
// Input text
const input = document.querySelector('[contenteditable="true"]');
input.textContent = prompt;
input.dispatchEvent(new InputEvent('input', { bubbles: true, data: prompt }));

// Send message
document.querySelector('button[aria-label="Send message"]').click();

// Click generated image to expand
document.querySelector('img.image.loaded').click();

// Open more options menu
document.querySelector('button[aria-label="Show more options"]').click();

// Download image (in lightbox)
document.querySelector('button[aria-label="Download full size image"]').click();

// Redo with Pro (from menu)
// Click button containing text "Redo with Pro"
const buttons = document.querySelectorAll('button');
for (const btn of buttons) {
    if (btn.textContent.includes('Redo with Pro')) {
        btn.click();
        break;
    }
}

// Close lightbox
document.querySelector('button[aria-label="Close"]').click();
```

---

## Full Workflow

### Step 1: Navigate to Gemini
```javascript
// Navigate to Gemini
mcp__Claude_in_Chrome__navigate({ url: "https://gemini.google.com/app", tabId: TAB_ID });
```

### Step 2: Enter Prompt
Use competitor-aggregated prompts from `COMPETITOR_DESIGN_AGGREGATOR.md`:

```javascript
const prompt = `Generate a professional 3D mobile app icon for "[APP_NAME]" - a [DESCRIPTION].
Design: [SYMBOL] with [EFFECTS], gradient from [COLOR1] (#HEX1) to [COLOR2] (#HEX2), [BACKGROUND], [STYLE].
Technical: 1024x1024, iOS rounded corners, no text, glossy finish, subtle glow.`;

const input = document.querySelector('[contenteditable="true"]');
input.textContent = prompt;
input.dispatchEvent(new InputEvent('input', { bubbles: true, data: prompt }));

// Wait then click send
document.querySelector('button[aria-label="Send message"]').click();
```

### Step 3: Wait for Generation
```javascript
// Wait 15-20 seconds for image generation
await new Promise(r => setTimeout(r, 15000));
```

### Step 4: Redo with Pro (CRITICAL)
```javascript
// Click more options
document.querySelector('button[aria-label="Show more options"]').click();

// Wait for menu
await new Promise(r => setTimeout(r, 500));

// Click Redo with Pro
const buttons = document.querySelectorAll('button');
for (const btn of buttons) {
    if (btn.textContent.includes('Redo with Pro')) {
        btn.click();
        break;
    }
}

// Wait for Pro regeneration (15-20 seconds)
await new Promise(r => setTimeout(r, 20000));
```

### Step 5: Download Image
```javascript
// Click image to expand lightbox
document.querySelector('img.image.loaded').click();

// Wait for lightbox
await new Promise(r => setTimeout(r, 1000));

// Click download button
document.querySelector('button[aria-label="Download full size image"]').click();
```

### Step 6: Copy to Assets
```bash
# Find newest download
NEWEST=$(ls -t ~/Downloads/Gemini_Generated_Image_*.png | head -1)

# Copy to icons folder
cp "$NEWEST" "/path/to/APP_FACTORY/assets/icons/[appname]-icon-1024.png"

# Verify size (should be 800KB-1.5MB for quality)
ls -la "/path/to/APP_FACTORY/assets/icons/[appname]-icon-1024.png"
```

---

## Troubleshooting

### Download Button Not Working
The download button click sometimes doesn't trigger via automation. Workarounds:
1. Click image to open in new tab, then use page save
2. Use the menu "Download image" option instead of toolbar button
3. Get image URL and attempt fetch with blob download

### Rate Limited
If Gemini shows rate limit:
1. Wait 5-10 minutes
2. Try AI Studio instead: `https://aistudio.google.com`
3. Use ChatGPT DALL-E as fallback

### Image Quality Check
- Minimum acceptable: 800KB
- Good quality: 1-1.5MB
- If under 500KB, regenerate with Pro

---

## Prompt Templates by Niche

### Biohacking (BioMaxx style)
```
Professional 3D mobile app icon for "[APP]" biohacking tracker.
Design: DNA helix intertwined with lightning bolt, gradient emerald green (#10B981) to teal (#14B8A6), dark slate background (#0F172A), scientific but energetic style.
Technical: 1024x1024, iOS corners, no text, glossy, subtle glow.
```

### Faith/Prayer (PrayerLock style)
```
Professional 3D mobile app icon for "[APP]" Christian prayer app.
Design: Praying hands with subtle light rays, gradient navy blue (#1E3A5F) to gold (#FFD700), warm amber glow, elegant reverent feel.
Technical: 1024x1024, iOS corners, no text, glossy finish.
```

### Fitness/Steps (StepUnlock style)
```
Professional 3D mobile app icon for "[APP]" fitness tracking app.
Design: Running figure or footprint with motion lines, gradient bright green (#22C55E) to blue (#3B82F6), energetic dynamic style.
Technical: 1024x1024, iOS corners, no text, glossy, motion blur effect.
```

### Women's Health (PelvicPro style)
```
Professional 3D mobile app icon for "[APP]" women's wellness app.
Design: Abstract lotus or feminine wave motif, gradient soft pink (#EC4899) to purple (#8B5CF6), elegant empowering feel.
Technical: 1024x1024, iOS corners, no text, soft glow, premium finish.
```

---

## Integration After Download

After icons are downloaded, integrate into apps:

```bash
# 1. Copy to app's assets folder
cp icons/[app]-icon-1024.png builds/[app]/assets/icon.png

# 2. Update app.json with icon path
# In app.json: "icon": "./assets/icon.png"

# 3. Launch in iOS Simulator to verify
cd builds/[app]
npx expo start --ios

# 4. Take screenshot for audit
# Use Simulator > File > Save Screen
```

---

## Quality Checklist

- [ ] Icon is 1024x1024 pixels
- [ ] File size 800KB-1.5MB (indicates good detail)
- [ ] No text in icon
- [ ] Has depth/3D effect
- [ ] Uses gradient (not flat)
- [ ] Includes relevant symbol for app purpose
- [ ] Passes squint test (recognizable when blurred)
- [ ] Stands out in App Store grid mockup

---

Created: 2026-01-21
