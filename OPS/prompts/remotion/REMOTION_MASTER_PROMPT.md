# Remotion Master Prompt Library

Collection of prompts for generating professional Remotion videos. Use the appropriate prompt based on your use case.

---

## Prompt 1: Premium Cyberpunk/Tech (Full Production)

**Best for:** Crypto, SaaS, tech products, DeFi apps, high-energy promos
**Duration:** 45-55 seconds
**Style:** Dark/neon cyberpunk, phonk music sync

```
You are an expert Remotion video creator using the latest Agent Skills. Your goal is to build a complete, polished, production-ready Remotion video project in one go — clean code, best practices, modular compositions, smooth transitions, kinetic typography, and professional feel.

First, create or update the project structure if needed (src/Video.tsx as main Composition, helper components in src/components/, assets in public/).

Video specs:
- Duration: 45-55 seconds total
- Resolution: 1920x1080 (16:9), 30 fps
- Style: premium dark/neon cyberpunk/futuristic tech vibe — deep blacks, cyan/magenta/purple gradients, glow effects, subtle particles, glitch transitions where appropriate
- Font: Use Google Fonts import — something modern like "Inter" for body, "Orbitron" or "Rajdhani" for titles (bold + glowing)
- Pacing: fast but not chaotic — quick cuts (1-4s per scene), energetic but readable
- Transitions: smooth combinations — cross-dissolve, zoom blur, glitch wipe, slide with motion blur, scale + fade
- Animations: kinetic text (pop-in, slide, scale with spring), icons/elements flying in, counters animating up, subtle parallax on backgrounds

Music & Audio (updated for trendy TikTok phonk integration):
- First, recall/find the most trendy TikTok music as of January 2026: Focus on phonk variations like Brazilian Phonk/Funk (e.g., high-energy tracks such as GOZALO by Ariis, ACELERADA by sma$her & MXZI, MONTAGEM REBOLA by ATLXS & DJ FKU, LUNA BALA, or similar aggressive/gym phonk with heavy bass, chopped vocals, and drift vibes). Suggest 3-5 top examples based on viral playlists (e.g., from Spotify's TOP 50 PHONK 2026 or YouTube viral mixes).
- Then, find open-source/free-to-use versions: Do not use copyrighted originals. Instead, suggest royalty-free alternatives or remixes (e.g., similar no-copyright phonk tracks like "Boom Pop" by KXLLYXU from Tunetank, "Baile Rave" from ElevenLabs, or custom remixes from samples). Provide user instructions in code comments to download free MP3s from sites like:
  - Pixabay (https://pixabay.com/music/search/phonk%20music) - Search for "phonk" and download royalty-free tracks.
  - Uppbeat (https://uppbeat.io/music/category/phonk) - Free phonk downloads, no attribution needed for personal use.
  - FreeToUse (https://freetouse.com/music/category/phonk) - Direct free phonk MP3s like "Aylex".
  - Tunetank (https://tunetank.com/discover/genres/phonk) - Royalty-free phonk like "Tempest" by SLXSH.
  - SoundCloud/Spotify no-copyright phonk playlists (e.g., https://soundcloud.com/ncmfyt/sets/phonk-no-copyright-music or Spotify's PHONK NO COPYRIGHT MUSIC).
- For repos/samples: Suggest downloading open-source sample packs from GitHub to build custom phonk (e.g., drums, bass, synths for remixing). Key repos:
  - pumodi/open-samples (https://github.com/pumodi/open-samples) - Free samples (choral, keyboards, percussion, synths, etc.); download full library from Dropbox: https://www.dropbox.com/scl/fo/en9luu00sx7lxib0tz5a7/AFf_7TypGuKolljx3VP0HtM?rlkey=zuouxhghnlbyh72xmnvjs6hv4&st=e1d9fdkc&dl=0. License: Permissive for music use (royalty-free, no AI training).
  - bratpeki/sample-packs (https://github.com/bratpeki/sample-packs) - Links to various royalty-free packs (drums, loops, FX) that can be used for phonk; clone repo and follow source links.
- User should place downloaded MP3s or samples in public/music/ folder (e.g., trendy_phonk.mp3).
- Import via staticFile('music/trendy_phonk.mp3')
- Use <Audio> component: start at 0s, loop if needed, fade in 1-2s at beginning, fade out at end
- Intelligently integrate: Auto-pick the most fitting track based on video vibe (e.g., aggressive phonk for montage). Sync to scenes — e.g., time transitions/cuts to bass drops (assume ~140-150 BPM for phonk), animate text/elements to rhythm (use useCurrentFrame() to pulse on beats), duck volume to ~25-35% during narration/peaks, crossfade if multiple clips. Add comments in code on how to remix samples if needed (e.g., via external tools like Audacity).
- Add subtle whoosh/sfx on transitions if possible (placeholder comments OK)

Scenes structure (strict timings — make durations add up exactly):
0-8s:   Intro hook
   - Black fade to neon grid background
   - Big centered title "[Your Video Title / Product Name]" zooms in with glow + particle burst
   - Subtitle " [Short tagline]" slides up below
   - Logo (assume public/logo.png or describe) appears top-right with spin-in

8-22s: Problem / Setup
   - Show relatable scene: frustrated person at desk/phone (use descriptive placeholder or stock-like animation: "diverse young adult looking stressed at laptop with flat crypto chart")
   - Text overlays: "Tired of low yields?" "Scattered across protocols?" popping in sequentially
   - Quick cuts to icons of struggling wallets/protocols

22-38s: Solution / Features montage
   - Hero transition (glitch + whoosh)
   - Person now excited → smiling, typing → charts spiking up
   - Fast montage (1-2s each):
     - Deposit screen animate
     - "One click → 15+ protocols" icons flashing + connecting lines
     - Yield numbers counter up dramatically (use <Counter> or spring animation)
     - Text bursts: "Auto-optimized", "Max APY", "No gas waste"
   - Energetic beat-sync cuts

38-50s: Call to Action + Outro
   - Big bold CTA: "Start Earning Now" button pulse/glow + hover effect simulation
   - Website URL / app link zooms in
   - Social handles / QR if relevant
   - Fade to logo + tagline reprise
   - Music swells then fades out

Additional requirements:
- Use TransitionSeries or custom Transition components for scene changes
- Make everything responsive / type-safe
- Add <AbsoluteFill> backgrounds with gradient or subtle moving particles
- Include <Sequence> for precise timing
- Export-ready: default Composition named "Main" at 1920x1080
- Add comments in code explaining each section, including music suggestions/downloads
- If anything is unclear (e.g. logo, specific images), use placeholders like <Img src={staticFile('placeholder/person-trading.jpg')} /> and note in comments
- After generating, suggest 2-3 iteration prompts I can use next (e.g. "make cuts faster and sync tighter to phonk drops", "swap to a more aggressive phonk variant", "add custom sfx from open-samples repo")

Topic / Product: [FILL IN: Describe your video here in 2-4 sentences]

Show me the full code for src/Video.tsx (and any new components you create) — make it copy-paste ready.

Begin now — be creative but follow the structure exactly. This should feel like a high-end crypto/SaaS ad with trendy phonk energy.
```

---

## Prompt 2: App Store Promo (Short-Form Vertical)

**Best for:** TikTok, Reels, app store preview videos
**Duration:** 8-15 seconds
**Style:** Clean, modern, vertical (1080x1920)

```
Create a professional Remotion app promo video for TikTok/Reels (1080x1920, 30fps, 8-15 seconds).

App Details:
- Name: [APP_NAME]
- Tagline: [TAGLINE]
- Features: [FEATURE_1], [FEATURE_2], [FEATURE_3], [FEATURE_4]
- Color Scheme: [PRIMARY_COLOR], [SECONDARY_COLOR], [BACKGROUND_COLOR]
- Niche: [NICHE - e.g., fitness, faith, productivity]

Design Requirements:
1. **Logo/Icon** (NOT a plain letter in a box):
   - 3D isometric or perspective effect
   - Gradient fills (multi-color, premium feel)
   - Glow/reflection effects
   - Entrance animation: scale + rotate + particle burst

2. **Background**:
   - Animated gradient orbs (slow rotation)
   - Floating particles or geometric shapes
   - Subtle grain/noise texture overlay

3. **Typography**:
   - App name: Bold, modern font (Inter Black or Montserrat Bold)
   - Tagline: Medium weight, slightly smaller
   - Features: Clean, readable, with checkmark icons
   - All text uses spring animations with stagger

4. **Structure** (8 seconds = 240 frames at 30fps):
   - 0-45 frames (1.5s): Logo entrance with effects
   - 45-90 frames (1.5s): Tagline kinetic reveal
   - 90-180 frames (3s): Features cascade in (15 frame stagger)
   - 180-240 frames (2s): CTA button pulse + end card

5. **Effects**:
   - Spring animations: { damping: 12, stiffness: 200 }
   - Text reveal: translateY with opacity
   - CTA: Scale pulse (1 → 1.05 → 1) with glow

Output: Full TypeScript/React code for Remotion composition.
```

---

## Prompt 3: Hook Video (Ultra Short)

**Best for:** TikTok hooks, scroll stoppers, attention grabbers
**Duration:** 3-6 seconds
**Style:** Bold text, high contrast, kinetic typography

```
Create a Remotion hook video (1080x1920, 30fps, 5 seconds = 150 frames).

Hook Lines (display sequentially):
1. "[LINE_1]"
2. "[LINE_2]"
3. "[LINE_3]"

Style:
- Background: Dark (#0F0F0F) or deep blue (#0F172A)
- Text: White with colored highlight word
- Highlight color: [COLOR - e.g., #FF6B6B, #10B981]

Animation Pattern:
- Each line:
  - Spring entrance from bottom (translateY: 100 → 0)
  - 0.8s hold time
  - Slight scale pulse on key word
  - Fade/slide out before next line

Typography:
- Font: Inter or SF Pro (bold/black weight)
- Size: Large (64-80px), fills most of screen width
- Line height: 1.1
- Text align: center

Timing (150 frames total):
- Line 1: frames 0-45 (1.5s)
- Line 2: frames 45-95 (1.67s)
- Line 3: frames 95-150 (1.83s)

Output: Complete Remotion component with spring animations and proper sequencing.
```

---

## Prompt 4: Faith/Devotional App (Warm & Inviting)

**Best for:** Christian apps, meditation, prayer, devotional content
**Duration:** 8-12 seconds
**Style:** Warm, peaceful, gold/amber accents

```
Create a Remotion promo for a faith-based app (1080x1920, 30fps, 10 seconds).

App: [APP_NAME]
Tagline: [TAGLINE]
Features: [FEATURES]

Design Language:
- Colors: Deep navy (#1A1A2E), warm gold (#E6B800), soft white (#F8FAFC)
- Mood: Peaceful, welcoming, trustworthy
- NO harsh neon or cyberpunk elements

Logo Requirements:
- Symbol related to faith (dove, cross, praying hands, sunrise)
- Elegant, not cartoonish
- Subtle gold glow effect
- Graceful entrance (slow fade + gentle scale)

Background:
- Soft radial gradient (navy to darker navy)
- Gentle light rays or sunrise effect
- NO particles (keep it calm)

Typography:
- Elegant serif for app name (Playfair Display)
- Clean sans-serif for features (Inter)
- Slower animations (damping: 25, stiffness: 80)

Structure (300 frames):
- 0-60: Peaceful fade in, logo appears gently
- 60-120: Tagline reveals (word by word, soft)
- 120-240: Features slide in (slow stagger, 25 frames apart)
- 240-300: CTA with warm glow + end card

Tone: This should feel like a moment of peace, not a sales pitch.
```

---

## Prompt 5: Fitness/Health App (Energetic)

**Best for:** Workout apps, step trackers, health tracking
**Duration:** 8-12 seconds
**Style:** High energy, vibrant greens/blues

```
Create an energetic Remotion promo for a fitness app (1080x1920, 30fps, 10 seconds).

App: [APP_NAME]
Tagline: [TAGLINE]
Features: [FEATURES]

Design Language:
- Colors: Electric green (#4ADE80), deep blue (#1E3A5F), white
- Mood: Energetic, motivating, achievement-focused
- Dynamic, movement-focused design

Logo Requirements:
- Motion-related icon (running figure, footsteps, heart rate)
- Gradient fill (green to teal)
- Energetic entrance (bouncy spring, slight overshoot)
- Motion trails or speed lines

Background:
- Dark blue base with green gradient accents
- Animated diagonal lines or geometric shapes
- Subtle pulse effect synced to imaginary beat

Typography:
- Bold impact font for app name
- Achievement-style text animations (slide from left/right)
- Faster animations (damping: 10, stiffness: 250)

Structure (300 frames):
- 0-45: Dynamic intro, logo bounces in
- 45-90: Tagline punches in (bold, fast)
- 90-200: Features rapid-fire (10 frame stagger)
- 200-260: Counter animation (steps, calories, etc.)
- 260-300: CTA with energy pulse

Include: Animated counter component that counts up dramatically (0 → 10,000 steps)
```

---

## Prompt 6: Women's Wellness (Soft & Empowering)

**Best for:** Women's health apps, self-care, wellness
**Duration:** 8-12 seconds
**Style:** Soft, empowering, pink/purple gradients

```
Create a Remotion promo for a women's wellness app (1080x1920, 30fps, 10 seconds).

App: [APP_NAME]
Tagline: [TAGLINE]
Features: [FEATURES]

Design Language:
- Colors: Soft pink (#FF69B4), deep purple (#4A1942), cream white
- Mood: Empowering, supportive, private, professional
- Elegant but not overly feminine

Logo Requirements:
- Abstract feminine symbol (flower, figure, abstract shape)
- Gradient from pink to purple
- Elegant entrance (soft bloom effect)
- Subtle shimmer or sparkle

Background:
- Deep purple base with soft pink radial gradients
- Organic flowing shapes (like silk or water)
- Gentle animation (slow, calming movement)

Typography:
- Modern elegant font (Poppins or Quicksand)
- Soft reveal animations
- Medium speed (damping: 18, stiffness: 120)

Structure (300 frames):
- 0-60: Elegant fade, logo blooms into view
- 60-120: Tagline appears gracefully
- 120-220: Features slide in with soft timing
- 220-300: Supportive CTA + end card

Tone: Empowering and professional, not cutesy or patronizing.
```

---

## Prompt 7: Biohacking/Longevity (Scientific & Premium)

**Best for:** Biohacking, longevity, health optimization apps
**Duration:** 8-12 seconds
**Style:** Scientific, premium, emerald/dark

```
Create a Remotion promo for a biohacking/longevity app (1080x1920, 30fps, 10 seconds).

App: [APP_NAME]
Tagline: [TAGLINE]
Features: [FEATURES]

Design Language:
- Colors: Emerald green (#10B981), dark slate (#0F172A), ice white (#F8FAFC)
- Mood: Scientific, premium, optimized, data-driven
- Clean, minimal, sophisticated

Logo Requirements:
- DNA helix, molecule, or optimization symbol
- Gradient (emerald to teal)
- Tech-inspired entrance (scan line effect or data visualization)
- Subtle data particles around logo

Background:
- Deep slate with emerald accent gradients
- Subtle grid or data visualization pattern
- Floating data points or molecule structures

Typography:
- Clean modern font (Inter, system-ui)
- Data-like animations (typewriter for numbers)
- Precise timing (damping: 15, stiffness: 180)

Structure (300 frames):
- 0-50: Tech intro, logo materializes with data effect
- 50-100: Tagline types in (scientific feel)
- 100-200: Features appear with data visualization style
- 200-260: Metrics counter (HRV, sleep score, etc.)
- 260-300: Premium CTA + end card

Include: Animated metrics display (like a health dashboard)
```

---

## Usage Notes

### Quick Selection Guide

| Niche | Use Prompt # | Key Adjustments |
|-------|--------------|-----------------|
| Crypto/DeFi | 1 | Full cyberpunk treatment |
| Mobile App (general) | 2 | Adjust colors for brand |
| TikTok Hook | 3 | Just change the lines |
| Faith/Christian | 4 | Warm, peaceful |
| Fitness/Steps | 5 | High energy |
| Women's Health | 6 | Soft, empowering |
| Biohacking | 7 | Scientific, premium |

### Asset Generation

For app icons and logos, use Gemini API:
- Location: `/.env` → `GEMINI_API_KEY`
- Prompt style: "3D app icon, [app name], [style], gradient, glossy, modern, 1024x1024"
- See: `MONEY_METHODS/APP_FACTORY/ASSET_GENERATION_GUIDE.md`

### Music Sources (Royalty-Free)

| Source | Best For | URL |
|--------|----------|-----|
| Pixabay | General, phonk | pixabay.com/music |
| Uppbeat | High quality | uppbeat.io |
| Tunetank | Phonk, EDM | tunetank.com |
| FreeToUse | Quick grabs | freetouse.com/music |

### Iteration Prompts

After generating, use these follow-ups:
- "Make cuts 30% faster and sync to 145 BPM"
- "Add more particle effects and glow"
- "Make the logo entrance more dramatic with 3D rotation"
- "Add beat-synced text pulses"
- "Create a 5-second vertical cut for TikTok"
