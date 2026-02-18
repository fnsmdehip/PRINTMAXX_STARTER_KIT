# Competitor Design Aggregator

**Purpose:** Extract winning design patterns from top competitors before creating any asset.

---

## The Method

Before creating ANY visual asset (icon, screenshot, video), run this process:

### Step 1: Identify Top 5 Competitors

For each niche, find the apps making $100k+/mo with best ratings:

```
Search queries:
- "[niche] app" on App Store (sort by top grossing)
- "[niche] tracker" on Product Hunt
- "best [niche] apps 2026" on Google
- Sensor Tower / AppMagic for revenue estimates
```

### Step 2: Screenshot Everything

Capture for EACH competitor:
- App icon (full res from App Store)
- First 3 app store screenshots
- Onboarding screens (download and screenshot)
- Main dashboard/home screen
- Key feature screens
- Settings/profile screens

### Step 3: Extract Design DNA

Analyze and document:

**Colors:**
- Primary color (exact hex)
- Secondary color
- Background color
- Accent/CTA color
- Text colors (heading, body, muted)

**Typography:**
- Heading font (identify via WhatTheFont or similar)
- Body font
- Font weights used
- Line heights

**Iconography:**
- Icon style (outlined, filled, duotone)
- Icon weight (thin, regular, bold)
- Corner radius on elements
- Shadow style

**Layout patterns:**
- Card styles
- Spacing rhythm
- Navigation patterns
- CTA placement

### Step 4: Create Aggregate Style Guide

Combine the BEST elements from all competitors:
- Take the most common successful patterns
- Identify unique differentiators
- Note what to AVOID (dated patterns)

---

## Niche-Specific Competitor Analysis

### Biohacking/Longevity (BioMaxx)

**Top Competitors to Analyze:**
1. Zero (fasting) - $500k+/mo
2. Oura Ring app - Premium health tracking
3. Whoop - Performance optimization
4. InsideTracker - Biomarker tracking
5. Levels (CGM) - Glucose optimization

**Common Design Patterns:**
- Dark mode dominant (90%+ use dark)
- Green/teal as primary (health = green)
- Minimal, data-forward UI
- Circular progress indicators
- Card-based metrics display
- Sans-serif fonts (Inter, SF Pro)

**Icon Style:**
- Abstract/geometric health symbols
- Gradient fills (not flat)
- Subtle glow effects
- NO literal organs/body parts

**Differentiation Opportunities:**
- Most are cold/clinical - add warmth
- Few have gamification - add streaks/rewards
- Limited social features - add community

---

### Looksmaxxing (GlowMaxx)

**Top Competitors to Analyze:**
1. UMAX - $500k+/mo (AI face rating)
2. Mewing App - Jaw tracking
3. Skincare routine apps (various)
4. Face Yoga apps
5. Glow Recipe / skincare trackers

**Common Design Patterns:**
- Clean white or soft dark backgrounds
- Pink/coral accents for women's market
- Blue/neutral for men's market
- Before/after photo layouts
- Progress tracking with visual timelines
- Aspirational imagery

**Icon Style:**
- Face silhouettes or abstract beauty symbols
- Gradient from warm to cool tones
- Soft, approachable rounded shapes
- Mirror/reflection motifs

**Differentiation Opportunities:**
- Most focus single aspect - be comprehensive
- Few track multiple protocols together
- Limited education content

---

### Faith/Devotional (DevotionFlow, DailyAnchor, FocusPrayer)

**Top Competitors to Analyze:**
1. Hallow - $100M+ valuation
2. Pray.com - Major player
3. Abide - Sleep/meditation focus
4. Bible App (YouVersion) - 500M+ downloads
5. Glorify - Modern design leader

**Common Design Patterns:**
- Warm, peaceful color palettes
- Navy/gold is classic combo
- Soft gradients, no harsh contrasts
- Generous whitespace
- Scripture in beautiful typography
- Nature imagery (sunrises, water, mountains)

**Icon Style:**
- Doves, crosses, books, light rays
- Gold/amber accents on dark backgrounds
- Elegant, not cartoonish
- Subtle, reverent aesthetic

**Differentiation Opportunities:**
- Most are passive consumption - add active engagement
- Few have accountability features
- Limited customization

---

### Fitness/Steps (StepUnlock)

**Top Competitors to Analyze:**
1. Opal/OneSec - Screen blocking
2. StepsApp - Step tracking
3. Pedometer++ - Simple step counter
4. Pacer - Walking tracker
5. Sweatcoin - Rewards for walking

**Common Design Patterns:**
- Bright, energetic colors
- Green = go, achievement
- Large number displays
- Circular progress rings
- Achievement badges/celebrations
- Motivational messaging

**Icon Style:**
- Footprints, running figures, hearts
- Dynamic motion lines
- Bright gradients (green, blue, orange)
- Energetic, not static

**Differentiation Opportunities:**
- Unique lock mechanism angle
- Gamification of walking
- Social challenges

---

### Women's Health (PelvicPro)

**Top Competitors to Analyze:**
1. Kegel Trainer (various)
2. Elvie - Premium hardware+app
3. Perifit - Gamified kegels
4. Squeezy (NHS) - Medical credibility
5. Flo - Period tracker (UI reference)

**Common Design Patterns:**
- Soft pinks, purples, teals
- Empowering, not clinical
- Privacy-focused UI (discreet)
- Progress visualization
- Educational content heavy
- Supportive tone in copy

**Icon Style:**
- Abstract feminine shapes
- Lotus, flower, or wave motifs
- Soft gradients
- Elegant, professional
- NOT overtly anatomical

**Differentiation Opportunities:**
- Most are basic timers - add intelligence
- Few have proper progress tracking
- Limited personalization

---

## Icon Generation Process

### Before Generating ANY Icon:

1. **Research** (30 min)
   - Screenshot top 5 competitor icons
   - Identify common colors, shapes, styles
   - Note what stands out vs blends in

2. **Document** (15 min)
   - Create mood board (Figma, Pinterest)
   - List specific hex colors to use
   - Describe symbol/shape concept

3. **Differentiate** (15 min)
   - How will ours stand out in App Store grid?
   - What's our unique visual angle?
   - What do competitors NOT do that we should?

4. **Generate** (varies)
   - Use aggregated insights in prompt
   - Generate 4-6 variations
   - Test at multiple sizes (180px, 60px, 29px)

5. **Validate** (10 min)
   - Put icon next to competitor icons
   - Does it stand out? Look professional?
   - Is it recognizable at 60px?

---

## Prompt Template with Competitor Context

```
Create a professional mobile app icon for "[APP_NAME]" in the [NICHE] space.

COMPETITOR CONTEXT:
Top apps in this space use: [describe common patterns]
Our differentiation: [unique angle]

DESIGN REQUIREMENTS:
- Symbol: [specific symbol based on research]
- Primary color: [hex from competitor analysis]
- Gradient: [to color]
- Background: [hex]
- Style: [based on what works in niche]

MUST HAVE (from competitor analysis):
- [Pattern 1 that top apps use]
- [Pattern 2 that top apps use]
- [Pattern 3 that top apps use]

MUST AVOID:
- [What dated/failing apps do]
- [Overused clichés in niche]

DIFFERENTIATION:
- [What makes ours unique visually]

Technical: 3D/isometric, glossy, 1024x1024, iOS rounded corners, no text
```

---

## Quick Competitor Research Checklist

- [ ] Identified top 5 revenue-generating competitors
- [ ] Screenshot all their icons
- [ ] Documented color palettes (exact hex)
- [ ] Noted typography choices
- [ ] Identified common UI patterns
- [ ] Found differentiation opportunities
- [ ] Created mood board
- [ ] Wrote differentiated design brief

---

## Tools for Competitor Research

**App Store Research:**
- Sensor Tower (revenue estimates)
- AppMagic (market intelligence)
- App Store directly (reviews, screenshots)

**Design Extraction:**
- ColorZilla (extract colors from screenshots)
- WhatTheFont (identify fonts)
- Figma (create mood boards)

**Screenshot Capture:**
- App Store high-res icon download
- iOS Simulator (for in-app screenshots)
- Android Emulator

**Validation:**
- AppLaunchpad (mockup icon in context)
- IconKitchen (test at multiple sizes)

---

## Example: BioMaxx Icon Brief

**Competitor Analysis Summary:**
- Zero: Minimalist, purple gradient, abstract timer
- Oura: Silver/gray, ring shape, premium feel
- Whoop: Bold red/black, athletic, aggressive
- Levels: Green gradient, glucose chart motif
- InsideTracker: Blue/white, DNA helix element

**Common Patterns:**
- Dark backgrounds (4/5)
- Gradient fills (5/5)
- Abstract symbols not literal (5/5)
- Single focal point (5/5)

**Our Differentiation:**
- Combine DNA (science) + Lightning (energy/optimization)
- Emerald green (fresh, not clinical blue)
- More vibrant than clinical competitors

**Final Prompt:**
```
Professional 3D mobile app icon for "BioMaxx" biohacking tracker.

COMPETITOR CONTEXT: Top apps (Zero, Oura, Whoop, Levels) use dark backgrounds with gradient abstract symbols. Most are clinical blue/gray or aggressive red. None combine science + energy visuals.

DESIGN:
- Symbol: DNA double helix intertwined with lightning bolt
- Gradient: Emerald green (#10B981) to teal (#14B8A6)
- Background: Dark slate (#0F172A)
- Style: Scientific but energetic, premium futuristic

MUST HAVE: 3D depth, glossy finish, soft glow, single focal point
MUST AVOID: Clinical blue, literal organ imagery, flat design
DIFFERENTIATION: Vibrant green (stands out from gray/blue competitors)

Technical: Isometric perspective, 1024x1024, iOS corners, no text
```

---

## Design Hacks

### 1. The "Squint Test"
Blur your icon to 50% - can you still tell what it is? If not, simplify.

### 2. The "Grid Test"
Put your icon in a grid with 20 competitor icons. Does it stand out? Is it recognizable?

### 3. The "Dark Mode Test"
Test icon on both light and dark backgrounds. Many users have dark mode.

### 4. The "Notification Badge Test"
Add a red notification dot - does the icon still look good?

### 5. The "Folder Test"
Put icon in a folder with similar apps - can users find it quickly?

### 6. The "3-Second Rule"
Show someone the icon for 3 seconds. Can they describe what the app does?

### 7. The "Trend Surfing"
What visual trends are hot RIGHT NOW? (Currently: 3D, gradients, glassmorphism)

### 8. The "Inverse Research"
Look at FAILING apps in niche. What do their icons have in common? Avoid those patterns.

---

Created: 2026-01-21
