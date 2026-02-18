# PRINTMAXX App Asset Generation Prompts

**Date:** 2026-02-10
**Platform:** Google ImageFX (powered by Imagen 3) / Gemini Image Generation
**Purpose:** Production-ready prompts for all visual assets across 6 PRINTMAXX apps

---

## ImageFX / Imagen 3 Prompt Engineering Notes

**Model:** Google Imagen 3 (latest as of Feb 2026), accessible via ImageFX at labs.google/fx/tools/image-fx or via Gemini.

**Key prompt tips for ImageFX:**
- ImageFX responds best to descriptive, natural language prompts. No need for comma-separated tag lists (that is Midjourney/SD style).
- Specify the medium/style explicitly: "3D render," "digital illustration," "vector graphic," "photorealistic," etc.
- ImageFX has strong understanding of lighting, materials, and camera angles. Be specific about these.
- For app icons specifically: say "app icon design" or "mobile app icon" to trigger the right proportions and style.
- ImageFX does not use a "negative prompt" field like Stable Diffusion. Instead, include avoidance language inline: "without text," "no words," "clean background with no clutter."
- For consistent style across a set, repeat the same style descriptors across all prompts.
- Aspect ratio: ImageFX defaults to 1:1. For other ratios, specify in the prompt or use Gemini's aspect ratio controls.
- ImageFX handles gradients, glass effects, and 3D depth particularly well.
- For the best results, generate 4 variants and pick the best. Iterate by tweaking adjectives, not restructuring the entire prompt.

**Prompt structure that works best with Imagen 3:**
```
[Subject description] + [Style/medium] + [Lighting] + [Color specification] + [Composition notes] + [Avoidance instructions]
```

---

## The 6 Apps

| # | App Name | Niche | Primary Colors | Icon Concept |
|---|----------|-------|----------------|--------------|
| 1 | PrayerLock | Faith/Prayer | Gold #E2B53F on deep blue-black #1A1A2E | Crescent + lock |
| 2 | Dusk | Sleep/Wellness | Gold #F5C542 on navy #0B1A2E | Crescent moon |
| 3 | Vault | Focus/Productivity | Blue #007AFF on matte black #1A1A1A | Abstract vault door |
| 4 | Streakr | Habit Tracking | Orange #FF9500 on white/dark | Flame/streak ring |
| 5 | Mise | Meal Planning | Warm amber on cream | Chef's knife / bowl |
| 6 | Steplock | Walking/Fitness | Coral #FF4757 on white/black | Footprint + lock |

---

## APP 1: PrayerLock

### A. App Icon (1024x1024)

**PrayerLock App Icon - Variant 1 (Crescent Lock)**
```
Platform: ImageFX / Imagen 3
Prompt: "A mobile app icon design featuring a crescent moon shape integrated with a minimalist padlock silhouette. The crescent is made of brushed gold with subtle metallic reflections, color #E2B53F. Set against a deep blue-black gradient background transitioning from #1A1A2E at the edges to #16213E at the center. Soft ambient golden glow radiating from the crescent. 3D render with top-left lighting creating subtle depth and shadow on the lock element. Clean minimal composition, single centered symbol, no text, no words, no letters. Square format with no rounded corners. Premium iOS app icon style."
Negative (inline): "no text, no words, no letters, no stars, no complex patterns, no busy details"
Style: 3D metallic render
Colors: Background #1A1A2E to #16213E gradient, Symbol #E2B53F gold
```

**PrayerLock App Icon - Variant 2 (Prayer Hands Silhouette)**
```
Platform: ImageFX / Imagen 3
Prompt: "A mobile app icon design showing two minimalist hands pressed together in prayer position, rendered as a geometric golden silhouette. The hands are a single flat gold shape, color #E2B53F, with subtle 3D beveling on the edges. Background is a smooth radial gradient from deep navy #16213E at center to near-black #1A1A2E at edges. A faint circular halo of warm light behind the hands at 15% opacity. Clean modern design, centered composition, single symbolic element. No text, no words, no letters, no ornate details. Square format, professional mobile app icon style with subtle 3D depth."
Negative (inline): "no text, no words, no calligraphy, no Arabic script, no cross, no religious symbols beyond hands"
Style: Flat geometric with 3D edge bevel
Colors: Background #1A1A2E/#16213E, Symbol #E2B53F
```

**PrayerLock App Icon - Variant 3 (Geometric Lock + Light)**
```
Platform: ImageFX / Imagen 3
Prompt: "A mobile app icon design of a stylized padlock shape where the lock's shackle forms an arch of warm golden light, color #E2B53F. The lock body is a rounded rectangle in dark teal #4ECCA3 with 30% opacity, creating a frosted glass effect against the deep navy background #1A1A2E. A single beam of soft light emanates upward from the lock's keyhole. 3D render, top-left directional lighting, matte surfaces with one specular highlight on the shackle. Minimal, modern, centered. No text, no words, no letters, no busy patterns. Square format, premium iOS app icon design."
Negative (inline): "no text, no words, no complex geometry, no religious iconography"
Style: 3D glass and metallic render
Colors: Background #1A1A2E, Lock body #4ECCA3 (30% opacity), Shackle #E2B53F
```

### B. App Store Screenshots (1290x2796 iPhone 15 Pro Max)

**Screenshot 1: "Your prayer, protected"**
- Device mockup: iPhone 15 Pro Max, slightly angled 5 degrees right
- Screen shows: Lock screen with prayer countdown timer, gold accent ring at 60% completion
- Background: Deep navy #1A1A2E gradient
- Headline text at top: "Your prayer, protected" in white SF Pro Display, 48pt semibold
- Subtext: none
- Theme: Dark, reverent, gold accents

**Screenshot 2: "Never miss a prayer"**
- Device mockup: Straight-on iPhone
- Screen shows: 5 daily prayer times listed in cards, next prayer highlighted with gold border, countdown badge
- Background: #16213E solid
- Headline: "Never miss a prayer" in white, 48pt
- Theme: Functional, clean, informational

**Screenshot 3: "Build unbreakable streaks"**
- Device mockup: iPhone slightly angled left
- Screen shows: 30-day prayer streak calendar heat map, current streak "47 days" in gold, completion rings
- Background: Dark gradient
- Headline: "Build unbreakable streaks" in gold #E2B53F, 48pt
- Theme: Achievement, progression

**Screenshot 4: "Focus on what matters"**
- Device mockup: iPhone with screen showing active prayer session
- Screen shows: Phone locked during prayer, countdown timer, beautiful minimal interface with just the timer and a soft golden glow
- Background: Near-black
- Headline: "Focus on what matters" in white, 48pt
- Theme: Zen, focused, distraction-free

**Screenshot 5: "All faiths welcome"**
- Device mockup: Two iPhones side by side (one showing Islamic prayer times with Qibla, one showing Christian prayer with scripture)
- Background: #1A1A2E
- Headline: "All faiths welcome" in teal #4ECCA3, 48pt
- Theme: Inclusive, warm, universal

**Color theme for set:** Dark backgrounds (#1A1A2E base), gold #E2B53F accents, white text, teal #4ECCA3 secondary

### C. Feature Graphic (Google Play, 1024x500)

```
Platform: ImageFX / Imagen 3
Prompt: "A wide banner design for a mobile app. Left side shows a golden crescent-lock icon glowing softly against a deep navy background #1A1A2E. Right side has large clean white text reading 'PrayerLock' in a modern sans-serif font, with smaller text below reading 'Protect your prayer time.' The entire composition has a horizontal gradient from #1A1A2E on the left to #16213E on the right. Subtle golden particle effects floating in the background. Professional app marketing banner, 1024x500 pixel wide format, landscape orientation."
Style: Marketing banner, wide format
Colors: #1A1A2E to #16213E gradient, #E2B53F gold, white text
```

### D. Social Media Kit

**Instagram Post (1080x1080):**
```
Platform: ImageFX / Imagen 3
Prompt: "A square social media post design with a centered golden crescent-lock icon on a deep navy background #1A1A2E. Below the icon, bold white text reads 'Lock your phone. Unlock your prayer.' in a clean modern sans-serif. Bottom of image has a subtle golden divider line. Minimal, premium app marketing style. No clutter, maximum three visual elements. Square format 1:1 ratio."
Style: Social media marketing graphic
Colors: #1A1A2E, #E2B53F, white
```

**Twitter/X Header (1500x500):**
```
Platform: ImageFX / Imagen 3
Prompt: "A wide header banner with a deep navy to dark teal gradient background, from #1A1A2E on the left to #16213E center to #1A1A2E on the right. A small golden crescent-lock icon on the far left at 20% from edge. Clean white text 'PrayerLock' in the center. Very minimal, lots of negative space. Wide landscape banner format. No busy patterns, no stars, clean modern aesthetic."
Style: Social media header banner
Colors: #1A1A2E, #16213E, #E2B53F, white
```

**Product Hunt Thumbnail (240x240):**
```
Platform: ImageFX / Imagen 3
Prompt: "A small square thumbnail showing a golden crescent moon integrated with a padlock on a dark navy background #1A1A2E. The icon fills 70% of the frame. Very simple, bold, recognizable at small sizes. No text, no details smaller than the lock's keyhole. 3D render with soft golden glow. Square format, icon-style."
Style: Small icon thumbnail
Colors: #1A1A2E, #E2B53F
```

### E. PWA Splash Screen

```
Platform: ImageFX / Imagen 3
Prompt: "A vertical splash screen design for a mobile app. Centered golden crescent-lock icon at 30% from top, below it the word 'PrayerLock' in clean white sans-serif text. Background is a smooth vertical gradient from #1A1A2E at top to #16213E at bottom. A very subtle radial golden glow behind the icon. Minimal, elegant, loading screen aesthetic. Portrait orientation, tall format."
Style: App splash/loading screen
Colors: #1A1A2E to #16213E vertical gradient, #E2B53F icon, white text
```

---

## APP 2: Dusk (Sleep/Wellness)

### A. App Icon (1024x1024)

**Dusk App Icon - Variant 1 (Flowing Crescent)**
```
Platform: ImageFX / Imagen 3
Prompt: "A mobile app icon design featuring a crescent moon made of flowing gradient lines, transitioning from deep navy #0B1A2E to warm gold #F5C542. The crescent is formed by 5-7 parallel curved lines that flow like silk ribbons, creating an elegant layered effect. Set against a matte black #0D0D0D background. 3D lighting from the top-left creates a soft ambient glow around the moon shape. The overall feel is serene, nocturnal, premium. Minimal style, single centered element, no text, no words, no letters, no stars. Square format, modern iOS app icon design."
Negative (inline): "no text, no words, no stars, no clouds, no face on the moon, no complex patterns"
Style: 3D layered line art
Colors: Background #0D0D0D, Lines gradient #0B1A2E to #F5C542
```

**Dusk App Icon - Variant 2 (Gradient Orb)**
```
Platform: ImageFX / Imagen 3
Prompt: "A mobile app icon design of a perfect sphere that is half-illuminated, representing the transition from day to night. The lit half glows with a warm gradient from golden amber #F5C542 to soft coral #FF6B35. The dark half fades into deep navy #0B1A2E. The sphere sits centered on a near-black background #0D0D0D. Soft ambient light spills from the illuminated side. 3D render with smooth matte surface and one subtle specular highlight. The terminator line between light and dark is slightly diffused. No text, no words, no letters. Square format, premium app icon."
Negative (inline): "no text, no words, no face, no eyes, no surface details, no craters"
Style: 3D photorealistic sphere render
Colors: Light half #F5C542 to #FF6B35, Dark half #0B1A2E, Background #0D0D0D
```

**Dusk App Icon - Variant 3 (Abstract Horizon)**
```
Platform: ImageFX / Imagen 3
Prompt: "A mobile app icon design showing an abstract horizon line at the lower third of the frame. Below the horizon is deep navy #0B1A2E. Above the horizon, a gradient transitions from warm gold #F5C542 at the horizon to deep indigo #3A1078 at the top, suggesting the moment after sunset. The horizon line itself has a soft golden glow. Two or three faint horizontal bands of color create a layered sunset-to-night effect. 3D render with volumetric lighting along the horizon. Minimal, abstract, no literal sun or moon shapes. No text, no words, no letters. Square format, modern app icon design."
Negative (inline): "no text, no words, no sun shape, no literal clouds, no trees, no landscape details"
Style: Abstract gradient landscape
Colors: Bottom #0B1A2E, Horizon glow #F5C542, Upper gradient #3A1078 to #6C63FF
```

### B. App Store Screenshots (1290x2796 iPhone 15 Pro Max)

**Screenshot 1: "Sleep score, simplified"**
- Device mockup: iPhone, centered
- Screen shows: Large "87" sleep score in thin gold text, centered, with a circular progress ring at 87% fill in gold-to-teal gradient
- Background: Deep navy #0B1A2E
- Headline: "Sleep score, simplified" in gold #F5C542, 44pt
- Theme: Premium, dark, minimal

**Screenshot 2: "Track every phase"**
- Device: iPhone slightly angled
- Screen: Sleep stage timeline bar (horizontal, color-coded: deep blue for deep sleep, teal for light, purple for REM, amber for awake)
- Background: #0B1A2E
- Headline: "Track every phase" in white, 44pt
- Theme: Scientific, data-rich

**Screenshot 3: "Wake at the right moment"**
- Device: iPhone centered
- Screen: Smart alarm interface showing optimal wake window, sunrise gradient animation at top
- Background: Very dark with hint of sunrise gradient at top
- Headline: "Wake at the right moment" in warm gold, 44pt
- Theme: Optimistic, morning energy

**Screenshot 4: "7-day sleep trends"**
- Device: iPhone
- Screen: Bar chart showing 7 nights of sleep data, gradient fills, trend line
- Background: #0B1A2E
- Headline: "See your patterns" in teal #4ECDC4, 44pt
- Theme: Analytics, insight

**Screenshot 5: "Sounds that help you drift"**
- Device: iPhone
- Screen: Grid of ambient sound options (rain, ocean, white noise, brown noise) with waveform visualizations
- Background: Deep indigo #3A1078 gradient
- Headline: "Sounds that help you drift" in white, 44pt
- Theme: Ambient, dreamy

**Color theme for set:** Navy #0B1A2E base, gold #F5C542 primary accent, teal #4ECDC4 secondary, white text

### C. Feature Graphic (Google Play, 1024x500)

```
Platform: ImageFX / Imagen 3
Prompt: "A wide banner design for a sleep tracking app. Left third shows a glowing crescent moon icon made of flowing gold gradient lines on a dark navy background. Center-right has clean white text 'Dusk' in a thin modern sans-serif font, with smaller text 'sleep tracking, simplified' below. Background is a horizontal gradient from near-black #0D0D0D on the left to deep navy #0B1A2E in the center to deep indigo #3A1078 on the right. Subtle star-like particles scattered at 10% opacity. Wide landscape format, 1024x500, premium app marketing banner."
Style: App marketing banner
Colors: #0D0D0D to #0B1A2E to #3A1078, #F5C542 gold, white text
```

### D. Social Media Kit

**Instagram Post (1080x1080):**
```
Prompt: "Square social media graphic. A glowing crescent moon made of golden gradient lines centered on a deep navy #0B1A2E background. Below: bold thin white text 'Better sleep starts at Dusk.' Clean minimal design, premium feel. 1:1 square format."
Colors: #0B1A2E, #F5C542, white
```

**Twitter/X Header (1500x500):**
```
Prompt: "Wide landscape header banner. Deep navy #0B1A2E to indigo #3A1078 gradient background. Small golden crescent icon on the left. 'Dusk' in thin white text center-right. Very minimal, lots of breathing room. Wide format, app header aesthetic."
Colors: #0B1A2E, #3A1078, #F5C542, white
```

**Product Hunt Thumbnail (240x240):**
```
Prompt: "Small square icon: flowing golden crescent moon on near-black background. Bold, simple, readable at 48px. No text. No stars. Just the crescent. Golden glow. Square format."
Colors: #0D0D0D, #F5C542
```

### E. PWA Splash Screen

```
Prompt: "Vertical splash screen. Deep navy #0B1A2E background. Centered golden crescent icon at upper third. Below it, 'Dusk' in thin white sans-serif text, 'Sleep tracking' in smaller muted grey text beneath. Faint radial glow behind the crescent in warm gold. Portrait tall format, loading screen aesthetic."
Colors: #0B1A2E, #F5C542, white, grey #8898AA
```

---

## APP 3: Vault (Focus/Productivity)

### A. App Icon (1024x1024)

**Vault App Icon - Variant 1 (Vault Door)**
```
Platform: ImageFX / Imagen 3
Prompt: "A mobile app icon design featuring an abstract vault door viewed from the front. A circular shape with a minimal cross-hair or plus-sign handle in the center, rendered in electric blue #007AFF with a subtle metallic sheen. The vault door sits on a matte black #1A1A1A background. The circular door has a thin bright blue border with soft blue glow along the edges, suggesting it is sealed and active. 3D render with top-left lighting creating depth on the circular form. Ultra-minimal, no text, no words, no letters, no decorative elements. Just the vault circle and handle. Square format, premium iOS app icon."
Negative (inline): "no text, no words, no gears, no combination dial, no complex machinery"
Style: 3D minimal metallic render
Colors: Background #1A1A1A, Vault door #2D2D2D, Accent #007AFF
```

**Vault App Icon - Variant 2 (Shield)**
```
Platform: ImageFX / Imagen 3
Prompt: "A mobile app icon design showing a minimal geometric shield shape, rendered as a frosted glass effect with a subtle blue tint. The shield has a faint electric blue #007AFF border glow. Inside the shield, a single vertical line (like a keyhole slit) in bright blue. Background is matte black #1A1A1A. 3D render with soft directional lighting from the top creating a subtle gradient across the glass shield surface. Clean, minimal, modern. No text, no words, no letters, no checkmarks, no complex symbols. Square format, app icon style."
Negative (inline): "no text, no words, no padlock, no chains, no ornate details"
Style: 3D frosted glass
Colors: Background #1A1A1A, Shield border #007AFF, Glass tint #4A90D9 at 20%
```

**Vault App Icon - Variant 3 (Concentric Rings)**
```
Platform: ImageFX / Imagen 3
Prompt: "A mobile app icon design of three concentric circles on a matte black #1A1A1A background. The outermost ring is dark grey #2D2D2D. The middle ring is electric blue #007AFF at 60% opacity. The innermost circle is solid electric blue #007AFF, glowing softly. The rings create a target/focus effect that draws the eye to the center. 3D render with subtle depth between each ring layer, creating a recessed tunnel effect. Minimal, geometric, precise. No text, no words, no letters. Square format, premium app icon design."
Negative (inline): "no text, no words, no crosshair, no target symbol"
Style: 3D geometric concentric rings
Colors: Background #1A1A1A, Outer #2D2D2D, Middle #007AFF 60%, Center #007AFF 100%
```

### B. App Store Screenshots (1290x2796 iPhone 15 Pro Max)

**Screenshot 1: "Lock in. Go deep."**
- Device: iPhone centered, slight shadow
- Screen: Full-screen focus timer showing "25:00" in large monospace white text, electric blue progress ring at 100%, matte black background
- Background: #1A1A1A
- Headline: "Lock in. Go deep." in electric blue #007AFF, 48pt bold
- Theme: Dark, intense, focused

**Screenshot 2: "Your phone, sealed"**
- Device: iPhone
- Screen: Lock screen showing "Vault Active" with countdown, blocked app list greyed out
- Background: #1A1A1A
- Headline: "Your phone, sealed" in white, 44pt
- Theme: Security, discipline

**Screenshot 3: "Track your deep work"**
- Device: iPhone angled
- Screen: Weekly bar chart of focus hours, each day color-coded by intensity, total "14h 23m this week"
- Background: #2D2D2D
- Headline: "Track your deep work" in blue #4A90D9, 44pt
- Theme: Data, progress

**Screenshot 4: "Set your intention"**
- Device: iPhone
- Screen: Pre-session intention picker with 4 tags: "Deep Work" "Study" "Creative" "Reading"
- Background: #1A1A1A
- Headline: "Set your intention" in white, 44pt
- Theme: Mindful, purposeful

**Screenshot 5: "Widgets keep you honest"**
- Full-bleed image: iPhone home screen with Vault widget showing today's focus time, next session, and streak
- Background: Blurred dark wallpaper
- Headline: "Widgets keep you honest" in blue #007AFF, 44pt
- Theme: Integration, daily use

**Color theme for set:** Matte black #1A1A1A base, electric blue #007AFF primary, softer blue #4A90D9 secondary, white text

### C. Feature Graphic (Google Play, 1024x500)

```
Prompt: "Wide banner for a focus timer app. Left: three concentric glowing blue circles on matte black. Center-right: 'Vault' in bold clean white text, subtitle 'deep work, protected' in grey #888888 below. Background: solid matte black #1A1A1A with a faint electric blue vignette glow from the left circles. Landscape 1024x500, minimal professional app banner."
Colors: #1A1A1A, #007AFF, white, #888888
```

### D. Social Media Kit

**Instagram Post (1080x1080):**
```
Prompt: "Square graphic. Matte black #1A1A1A background. Centered: a glowing electric blue vault door circle icon. Below: 'Your attention is the asset. Protect it.' in clean white text. Minimal, dark, premium. 1:1 square."
Colors: #1A1A1A, #007AFF, white
```

**Twitter/X Header (1500x500):**
```
Prompt: "Wide banner. Matte black background. Three faint concentric blue rings on the far left at 30% opacity. 'Vault' in white text at center. Ultra minimal. Wide landscape format."
Colors: #1A1A1A, #007AFF at 30%, white
```

**Product Hunt Thumbnail (240x240):**
```
Prompt: "Small square: three concentric circles, inner one glowing electric blue, on matte black background. Bold, simple, recognizable at tiny sizes. No text. Square format."
Colors: #1A1A1A, #007AFF
```

### E. PWA Splash Screen

```
Prompt: "Vertical splash screen. Matte black #1A1A1A background. Centered vault door circle icon in electric blue #007AFF at upper third. 'Vault' in bold white text below. 'Deep work, protected' in grey #888888 smaller text. Minimal, dark, serious. Portrait format."
Colors: #1A1A1A, #007AFF, white, #888888
```

---

## APP 4: Streakr (Habit Tracking)

### A. App Icon (1024x1024)

**Streakr App Icon - Variant 1 (Flame Streak)**
```
Platform: ImageFX / Imagen 3
Prompt: "A mobile app icon design featuring an abstract flame shape made of a warm gradient from deep orange #FF9500 at the base to bright golden yellow #FFD93D at the tip. The flame is stylized and geometric, not realistic, with smooth curves and 3-4 layered color bands. Set against a clean white #FFFFFF background. The flame is centered and fills about 60% of the icon area. 3D render with soft lighting creating a subtle shadow beneath the flame. Modern, playful, energetic. No text, no words, no letters. Square format, iOS app icon style."
Negative (inline): "no text, no words, no realistic fire, no smoke, no sparks, no dark background"
Style: 3D geometric gradient flame
Colors: Background #FFFFFF, Flame #FF9500 to #FFD93D gradient
```

**Streakr App Icon - Variant 2 (Streak Ring)**
```
Platform: ImageFX / Imagen 3
Prompt: "A mobile app icon design showing a circular progress ring that is 75% filled. The filled portion is a warm gradient from orange #FF9500 to coral #FF6B6B. The unfilled portion is light grey #D1D5DB. Inside the ring, a bold orange checkmark. Background is clean white #FFFFFF. The ring has subtle 3D depth with a thin shadow on the outer edge. Inspired by Apple Watch activity rings but with one ring and a checkmark. Bright, motivating, clean. No text, no words, no letters. Square format."
Negative (inline): "no text, no words, no numbers inside the ring, no multiple rings"
Style: 3D progress ring
Colors: Background white, Ring filled #FF9500 to #FF6B6B, Ring empty #D1D5DB, Check #FF9500
```

**Streakr App Icon - Variant 3 (Rising Bars)**
```
Platform: ImageFX / Imagen 3
Prompt: "A mobile app icon design showing 5 vertical bars in ascending height from left to right, like a streak chart going up. Each bar is a slightly different warm color: first bar coral #FF6B6B, second orange #FF9F43, third golden #FFD93D, fourth teal #4ECDC4, fifth green #6BCB77. The bars have rounded tops and subtle 3D depth. Background is clean white #FFFFFF. A thin grey baseline at the bottom. Playful, colorful, data-inspired. No text, no words, no letters, no axis labels. Square format, app icon."
Negative (inline): "no text, no words, no grid lines, no numbers"
Style: 3D colorful bar chart
Colors: Background white, Bars #FF6B6B, #FF9F43, #FFD93D, #4ECDC4, #6BCB77
```

### B. App Store Screenshots (1290x2796 iPhone 15 Pro Max)

**Screenshot 1: "Your streaks. Your power."**
- Device: iPhone centered
- Screen: Today view with 6 habits shown as colorful completion rings (Apple Watch ring style), "4/6 completed" prominent
- Background: White
- Headline: "Your streaks. Your power." in orange #FF9500, 48pt bold
- Theme: Bright, energetic, motivating

**Screenshot 2: "Track anything that matters"**
- Device: iPhone angled
- Screen: Habit list with various icons and colors, mix of completed (green checks) and pending habits
- Background: Light grey #F8F9FA
- Headline: "Track anything that matters" in dark text #1A1A1A, 44pt
- Theme: Flexible, personal

**Screenshot 3: "Streaks build momentum"**
- Device: iPhone
- Screen: Streak calendar heat map (GitHub-style), showing 3 months of data, streak counter "47 days" in bold orange
- Background: White
- Headline: "Streaks build momentum" in orange #FF9500, 44pt
- Theme: Progress, achievement

**Screenshot 4: "Celebrate every win"**
- Device: iPhone
- Screen: Confetti animation moment, large checkmark in center, "30-day streak!" badge in gold
- Background: White with colorful confetti particles
- Headline: "Celebrate every win" in green #6BCB77, 44pt
- Theme: Joy, reward, dopamine

**Screenshot 5: "See what's working"**
- Device: iPhone
- Screen: Analytics view with completion rate charts, best streak, weekly/monthly trends
- Background: White
- Headline: "See what's working" in teal #4ECDC4, 44pt
- Theme: Insight, data

**Color theme for set:** White base, orange #FF9500 primary, multi-color habit accents, dark text

### C. Feature Graphic (Google Play, 1024x500)

```
Prompt: "Wide banner for a habit tracking app. Left: colorful flame icon in orange-to-yellow gradient. Center: 'Streakr' in bold dark text on white background. Right: a mini heat map calendar with colored squares. Bright, energetic, clean white background. Landscape 1024x500 format. Playful professional app marketing banner."
Colors: White base, #FF9500 orange, #FFD93D yellow, #4ECDC4 teal, dark text
```

### D. Social Media Kit

**Instagram Post (1080x1080):**
```
Prompt: "Square social media graphic. White background. Large orange flame icon centered. Below: 'Every day counts. Track it.' in bold dark text. Small colorful heat map squares scattered decoratively at the bottom. Clean, bright, motivating. 1:1 square."
Colors: White, #FF9500, #1A1A1A text
```

**Twitter/X Header (1500x500):**
```
Prompt: "Wide banner. White background. Small orange flame icon on the left. 'Streakr' in bold dark text at center. A row of colorful small squares (representing streak days) running along the bottom edge. Bright, clean, minimal. Wide landscape format."
Colors: White, #FF9500, multi-color squares, dark text
```

**Product Hunt Thumbnail (240x240):**
```
Prompt: "Small square: geometric orange-to-yellow gradient flame on white background. Bold, simple, fills the frame. No text. Recognizable at tiny sizes. Square format."
Colors: White, #FF9500 to #FFD93D
```

### E. PWA Splash Screen

```
Prompt: "Vertical splash screen. White background. Orange gradient flame icon centered at upper third. 'Streakr' in bold dark text below. 'Build habits that stick' in lighter grey text beneath. Bright, clean, motivating energy. Portrait tall format."
Colors: White, #FF9500, #1A1A1A, #6B7280
```

---

## APP 5: Mise (Meal Planning)

### A. App Icon (1024x1024)

**Mise App Icon - Variant 1 (Chef's Knife)**
```
Platform: ImageFX / Imagen 3
Prompt: "A mobile app icon design featuring a minimal chef's knife viewed from above at a 45-degree angle. The blade is a clean geometric triangle in warm silver-grey #C0C0C0 with a subtle metallic sheen. The handle is warm walnut brown #8B6914. The knife sits on a warm cream #FFF8E1 background. A thin shadow beneath the knife creates depth. One small herb leaf in muted green #6BCB77 next to the blade tip as a subtle accent. 3D render with soft top-down lighting. Clean, culinary, premium. No text, no words, no letters. Square format, app icon design."
Negative (inline): "no text, no words, no cutting board, no food items, no complex scene"
Style: 3D minimal culinary still life
Colors: Background #FFF8E1, Blade silver, Handle #8B6914, Leaf #6BCB77
```

**Mise App Icon - Variant 2 (Bowl)**
```
Platform: ImageFX / Imagen 3
Prompt: "A mobile app icon design showing a minimal ceramic bowl viewed from a slight top-down angle, about 30 degrees. The bowl is white porcelain with a thin warm amber #F0883E rim line. Inside the bowl, a small stylized steam wisp rises in a single elegant curve, rendered in warm amber gradient. Background is a matte warm cream #FFF8E1. The bowl casts a soft circular shadow. 3D render, soft diffused lighting, food photography aesthetic. Simple, warm, appetizing. No text, no words, no letters, no food inside the bowl. Square format, app icon."
Negative (inline): "no text, no words, no food, no spoon, no chopsticks, no complex elements"
Style: 3D ceramic still life
Colors: Background #FFF8E1, Bowl white, Rim/steam #F0883E
```

**Mise App Icon - Variant 3 (Mise en Place Circles)**
```
Platform: ImageFX / Imagen 3
Prompt: "A mobile app icon design inspired by 'mise en place' - the chef's practice of organizing ingredients in small bowls. Show 4 small circles arranged in a loose diamond pattern, each filled with a different color: warm amber #F0883E, sage green #6BCB77, soft coral #FF6B6B, and golden yellow #FFD93D. The circles represent small prep bowls viewed from above. They sit on a warm cream #FFF8E1 background. Each circle has a subtle 3D depth with soft shadows. Clean, geometric, culinary. No text, no words, no letters. Square format, modern app icon."
Negative (inline): "no text, no words, no actual food textures, no complex patterns, no more than 4 circles"
Style: 3D flat color circles
Colors: Background #FFF8E1, Circles #F0883E, #6BCB77, #FF6B6B, #FFD93D
```

### B. App Store Screenshots (1290x2796 iPhone 15 Pro Max)

**Screenshot 1: "Meal prep, mastered"**
- Device: iPhone centered
- Screen: Weekly meal plan view with 7 days, each showing 3 meals as small color-coded cards
- Background: Warm cream #FFF8E1
- Headline: "Meal prep, mastered" in warm brown #5D4037, 48pt semibold
- Theme: Warm, organized, kitchen-friendly

**Screenshot 2: "Recipes that fit your week"**
- Device: iPhone angled
- Screen: Recipe card view showing a recipe with estimated prep time, macros, and a placeholder food image
- Background: White
- Headline: "Recipes that fit your week" in amber #F0883E, 44pt
- Theme: Practical, efficient

**Screenshot 3: "One tap grocery list"**
- Device: iPhone
- Screen: Auto-generated grocery list organized by aisle, with checkboxes and quantities
- Background: Cream #FFF8E1
- Headline: "One tap grocery list" in dark text, 44pt
- Theme: Convenience, utility

**Screenshot 4: "Know your macros"**
- Device: iPhone
- Screen: Daily nutrition dashboard with circular macro rings (protein blue, carbs green, fat amber), calorie total
- Background: White
- Headline: "Know your macros" in sage green #6BCB77, 44pt
- Theme: Health-conscious, data-driven

**Screenshot 5: "Prep like a chef"**
- Device: iPhone
- Screen: Step-by-step meal prep instructions with timer integration, organized by prep order
- Background: Warm cream
- Headline: "Prep like a chef" in amber #F0883E, 44pt
- Theme: Professional, aspirational

**Color theme for set:** Warm cream #FFF8E1 and white bases, amber #F0883E primary, sage #6BCB77 secondary, warm brown text

### C. Feature Graphic (Google Play, 1024x500)

```
Prompt: "Wide banner for a meal planning app. Left: four small colorful circles representing mise en place prep bowls (amber, green, coral, yellow) arranged in a diamond on a cream background. Center-right: 'Mise' in elegant warm brown text, subtitle 'meal prep, simplified' below. Warm cream #FFF8E1 background throughout. Soft, inviting, culinary. Wide landscape 1024x500 format."
Colors: #FFF8E1, #F0883E, #6BCB77, #FF6B6B, #FFD93D, warm brown text
```

### D. Social Media Kit

**Instagram Post (1080x1080):**
```
Prompt: "Square social graphic. Warm cream #FFF8E1 background. Four small colorful prep bowl circles arranged in a diamond pattern at center. Below: 'Prep once. Eat well all week.' in warm brown text. Clean, warm, kitchen-inspired. 1:1 square."
Colors: #FFF8E1, #F0883E, #6BCB77, warm brown text
```

**Twitter/X Header (1500x500):**
```
Prompt: "Wide banner. Warm cream background. Small prep bowl icon cluster on the left. 'Mise' in elegant brown text at center. Clean, warm, minimal. Wide landscape format."
Colors: #FFF8E1, multi-color circles, warm brown text
```

**Product Hunt Thumbnail (240x240):**
```
Prompt: "Small square: four colored circles in a diamond pattern (amber, green, coral, yellow) on warm cream background. Simple, bold, food-themed. No text. Square format."
Colors: #FFF8E1, #F0883E, #6BCB77, #FF6B6B, #FFD93D
```

### E. PWA Splash Screen

```
Prompt: "Vertical splash screen. Warm cream #FFF8E1 background. Centered prep bowl circles icon at upper third. 'Mise' in elegant warm brown text below. 'Meal prep, simplified' in lighter text beneath. Warm, inviting, portrait tall format."
Colors: #FFF8E1, multi-color circles, warm brown text, lighter brown subtext
```

---

## APP 6: Steplock (Walking/Fitness)

### A. App Icon (1024x1024)

**Steplock App Icon - Variant 1 (Footprint Lock)**
```
Platform: ImageFX / Imagen 3
Prompt: "A mobile app icon design featuring a single stylized footprint combined with a lock shape. The footprint is formed by an oval toe area and a rounded heel connected by an arch, rendered in vibrant coral red #FF4757. The heel of the footprint seamlessly transitions into the body of a small padlock shape. Set on a clean white #FFFFFF background. 3D render with subtle depth and a soft coral shadow beneath. Bold, energetic, immediately readable. No text, no words, no letters, no shoe tread patterns. Square format, modern iOS app icon."
Negative (inline): "no text, no words, no shoe, no sneaker, no complex details, no multiple footprints"
Style: 3D flat icon with depth
Colors: Background white, Footprint/lock #FF4757
```

**Steplock App Icon - Variant 2 (Step Ring)**
```
Platform: ImageFX / Imagen 3
Prompt: "A mobile app icon design showing a bold circular progress ring filled 70% in a gradient from coral red #FF4757 to vibrant green #2ED573. The ring is thick, about 15% of the icon width, like an Apple Watch activity ring. Inside the ring, a small minimal padlock icon in coral red #FF4757. The unfilled 30% of the ring is light grey #DFE4EA. Background is clean white #FFFFFF. 3D render with the ring having slight thickness and shadow. Energetic, fitness-coded, goal-oriented. No text, no words, no numbers. Square format, app icon style."
Negative (inline): "no text, no words, no numbers, no step count, no percentage"
Style: 3D activity ring
Colors: Background white, Ring filled #FF4757 to #2ED573 gradient, Ring empty #DFE4EA, Lock #FF4757
```

**Steplock App Icon - Variant 3 (Abstract Path)**
```
Platform: ImageFX / Imagen 3
Prompt: "A mobile app icon design showing an abstract winding path or trail rendered as a thick line that curves upward from bottom-left to top-right. The path is a gradient from coral red #FF4757 at the bottom to vibrant gold #FFD700 at the top. At the end of the path, a small circular badge or dot in green #2ED573, suggesting a goal reached. The path line has rounded caps and subtle 3D thickness. Background is clean white #FFFFFF. Dynamic, upward motion, achievement-coded. No text, no words, no letters, no footprints. Square format, modern app icon."
Negative (inline): "no text, no words, no footprints, no arrows, no dotted lines"
Style: 3D gradient path
Colors: Background white, Path #FF4757 to #FFD700 gradient, Goal dot #2ED573
```

### B. App Store Screenshots (1290x2796 iPhone 15 Pro Max)

**Screenshot 1: "Walk to unlock your day"**
- Device: iPhone centered
- Screen: Lock screen showing step count "4,217 / 10,000" with a large coral progress ring, "58% to unlock" text
- Background: White with subtle coral gradient at top
- Headline: "Walk to unlock your day" in coral #FF4757, 48pt bold
- Theme: Energetic, motivating, gamified

**Screenshot 2: "Your phone stays locked"**
- Device: iPhone
- Screen: Locked phone interface showing "Walk 5,783 more steps to unlock social media" with app icons greyed out
- Background: White
- Headline: "Your phone stays locked" in dark text #1A1A1A, 44pt
- Theme: Discipline, accountability

**Screenshot 3: "Hit your goals. Every day."**
- Device: iPhone angled
- Screen: Weekly step chart with daily bars, completed days in green, current day in coral with progress
- Background: Light grey #F5F5F7
- Headline: "Hit your goals. Every day." in green #2ED573, 44pt
- Theme: Consistency, streaks

**Screenshot 4: "Earn your screen time"**
- Device: iPhone
- Screen: Rewards screen showing unlocked apps after hitting step goal, celebratory animation
- Background: White
- Headline: "Earn your screen time" in coral #FF4757, 44pt
- Theme: Reward, achievement

**Screenshot 5: "Join the challenge"**
- Device: Two iPhones side by side showing leaderboard with friends
- Background: White
- Headline: "Join the challenge" in gold #FFD700, 44pt
- Theme: Social, competitive

**Color theme for set:** White base, coral #FF4757 primary, green #2ED573 for success, gold #FFD700 for achievement

### C. Feature Graphic (Google Play, 1024x500)

```
Prompt: "Wide banner for a fitness walking app. Left: bold coral-red footprint-lock icon on white. Center-right: 'Steplock' in bold dark text, subtitle 'walk to unlock your day' below. White background with a subtle gradient of coral #FF4757 at bottom edge. Energetic, clean, fitness-coded. Wide landscape 1024x500 format."
Colors: White, #FF4757, dark text, #2ED573 green accent
```

### D. Social Media Kit

**Instagram Post (1080x1080):**
```
Prompt: "Square social graphic. White background. Large coral-red footprint-lock icon centered. Below: 'Your phone is locked until you walk.' in bold dark text. Bottom edge: green progress bar at 60%. Energetic, fitness, gamified. 1:1 square."
Colors: White, #FF4757, dark text, #2ED573
```

**Twitter/X Header (1500x500):**
```
Prompt: "Wide banner. White background. Small coral footprint-lock icon on the left. 'Steplock' in bold dark text at center. A thin green-to-coral gradient progress bar running along the very bottom edge of the banner. Clean, energetic. Wide landscape format."
Colors: White, #FF4757, #2ED573, dark text
```

**Product Hunt Thumbnail (240x240):**
```
Prompt: "Small square: coral red footprint-lock icon on white background. Bold, simple, fills frame. No text. Recognizable at tiny sizes. Square format."
Colors: White, #FF4757
```

### E. PWA Splash Screen

```
Prompt: "Vertical splash screen. White background. Centered coral footprint-lock icon at upper third. 'Steplock' in bold dark text below. 'Walk to unlock your day' in lighter grey text beneath. Energetic, clean, fitness energy. Portrait tall format."
Colors: White, #FF4757, #1A1A1A, #6B7280
```

---

## Production Checklist

### Icon Generation Workflow
1. Open ImageFX at labs.google/fx/tools/image-fx (or use Gemini)
2. Paste prompt exactly as written above
3. Generate 4 variants per prompt (ImageFX default)
4. Select best variant
5. Download at highest resolution
6. Resize to 1024x1024 if needed
7. Do NOT add rounded corners (iOS/Android add these automatically)
8. Export as PNG with no transparency (App Store requirement)

### Required Icon Sizes (iOS)
```
1024x1024  - App Store listing (required)
180x180    - iPhone (60pt @3x)
120x120    - iPhone (60pt @2x)
167x167    - iPad Pro
152x152    - iPad
87x87      - iPhone Spotlight (29pt @3x)
80x80      - iPhone Spotlight (40pt @2x)
76x76      - iPad
58x58      - iPhone Settings (29pt @2x)
40x40      - iPhone Settings (20pt @2x)
```

### Required Icon Sizes (Android)
```
512x512    - Google Play listing
192x192    - xxxhdpi
144x144    - xxhdpi
96x96      - xhdpi
72x72      - hdpi
48x48      - mdpi
```

### Screenshot Dimensions
```
iPhone 15 Pro Max:   1290 x 2796 (6.7" required)
iPhone 14 Plus:      1284 x 2778 (6.5" accepted)
iPhone SE:           1242 x 2208 (5.5" accepted)
iPad Pro 12.9":      2048 x 2732
Google Play:         1080-1440 width, 16:9 or 9:16 ratio
```

### File Naming Convention
```
[app_name]_icon_v[1-3]_1024x1024.png
[app_name]_screenshot_[1-5]_1290x2796.png
[app_name]_feature_graphic_1024x500.png
[app_name]_ig_post_1080x1080.png
[app_name]_twitter_header_1500x500.png
[app_name]_ph_thumb_240x240.png
[app_name]_splash_portrait.png
```

---

*Asset generation prompts compiled from reverse-engineering 24 top App Store apps, using color palettes from AGGREGATE_DESIGN_SYSTEM.md and icon patterns from TOP_APP_AUDIT.md. All prompts optimized for Google ImageFX / Imagen 3.*
