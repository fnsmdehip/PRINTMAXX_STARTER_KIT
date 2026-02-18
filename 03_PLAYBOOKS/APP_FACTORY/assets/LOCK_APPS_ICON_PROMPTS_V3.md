# Lock Apps Icon Generation Prompts (V3 - Competitor-Informed)

**Created:** 2026-02-03
**MEGA_RALPH:** EX-05 Day 4 Iteration 15
**Priority:** 9.0 (blocking App Store submission)

These are the highest priority icons. PrayerLock, WalkToUnlock, StudyLock, and BioMaxx are the 4 launch-ready apps. Icons must be generated before TestFlight/App Store submission.

**Generation tools (pick any):**
1. Ideogram (https://ideogram.ai) - 25 free/day, best text rendering
2. Google AI Studio (https://aistudio.google.com) - Gemini 2.0 Flash, free
3. ChatGPT/DALL-E - Reliable 1024x1024 output
4. Leonardo.ai (https://leonardo.ai) - 150 free tokens/day
5. Midjourney - If subscribed

**Design system (all icons share):**
- 3D depth with isometric or perspective view
- Glossy/glass finish with subtle reflections
- Soft glow effect around main symbol
- Single clear focal point
- iOS rounded square format
- Recognizable at 60x60px
- NO text, NO letters, pure iconography
- Must look like a $10M funded app

---

## 1. PrayerLock (Multi-Faith Version)

**Position:** "The phone lock that makes you pray." Zero direct competitors do behavior enforcement for prayer.

### Competitor Context

| Competitor | Icon Style | Our Differentiation |
|-----------|-----------|---------------------|
| Hallow | Minimal "H" on purple gradient | We lock the phone, they play audio |
| Muslim Pro | Green crescent on white | We enforce prayer, they remind |
| Pray.com | Soft watercolor cross | We work across faiths |
| Bible App | Green book icon | We're a lock, not a reader |
| Athan | Green mosque dome | We're multi-faith |

**Key insight:** No competitor uses a LOCK symbol. Every prayer app uses religious symbols (crosses, crescents, books). Our lock mechanism IS the brand.

### V3 Prompt (Multi-Faith - PREFERRED)

```
Create a professional mobile app icon for "PrayerLock" - an app that locks your phone until you pray.

DESIGN: A golden 3D padlock in the center, partially open, with soft divine light rays emanating from the opening. The light suggests spiritual awakening through the act of unlocking through prayer. The lock should be elegant, not industrial - think premium jewelry-quality metal with warm gold reflections.

COLOR PALETTE:
- Lock: warm gold (#D4AF37) to amber (#B8860B) gradient with metallic reflections
- Light rays: soft white-gold (#FFE4B5) to pure white, emanating upward
- Background: deep midnight blue (#0D1B3E) to dark navy (#1a1a2e) gradient
- Subtle warm glow behind the lock

STYLE: Spiritual, premium, universal (NOT tied to one religion). The lock IS the brand. No crosses, no crescents, no specific religious symbols. The golden light represents prayer itself, universal across all faiths.

MUST INCLUDE:
- 3D depth with realistic metallic gold textures
- Glossy finish with clear reflections on the lock body
- Soft divine glow from the partially open lock
- Single focal point (the lock)
- Professional gradient execution
- Rounded corners (iOS app icon style)
- Particle/light effects around the opening

MUST AVOID:
- Praying hands (too generic, used by 50+ apps)
- Crosses, crescents, or any faith-specific symbols
- Flat design without dimension
- Text or letters
- Industrial/harsh lock look
- Cold blue tones (must feel warm and spiritual)

TECHNICAL: 1024x1024 pixels. Must be recognizable at 60px. Must work on light and dark backgrounds.

This icon should make someone think "beautiful, premium, spiritual" not "phone restriction." The gold lock with divine light says: "prayer unlocks something valuable."
```

### V3 Prompt (Alternative - Cross + Crescent Combined)

```
Create a professional mobile app icon for a multi-faith prayer app.

DESIGN: A refined 3D padlock with the keyhole shaped as a subtle universal spiritual symbol - a radiating light burst (not a cross or crescent specifically, but suggesting divine light). The lock is partially open with warm golden light spilling out.

COLOR PALETTE:
- Lock body: brushed gold (#C5A55A) to deep amber (#8B6914)
- Light emission: warm white (#FFF8DC) to gold (#FFD700)
- Background: gradient from deep sapphire (#0C1445) to midnight navy (#161A30)

STYLE: Premium, warm, inviting. App Store flagship quality. The lock is the hero element.

TECHNICAL: 1024x1024, 3D depth, glossy metallic finish, soft glow effects, iOS rounded square. No text.
```

### Copy Commands After Generation

```bash
# Copy to app builds
cp ~/Downloads/prayerlock-icon.png /Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt/MONEY_METHODS/APP_FACTORY/assets/icons/prayerlock-icon-1024-v3.png
cp ~/Downloads/prayerlock-icon.png /Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt/MONEY_METHODS/APP_FACTORY/builds/prayerlock/assets/icon.png
cp ~/Downloads/prayerlock-icon.png /Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt/MONEY_METHODS/APP_FACTORY/builds/prayerlock-sdk54/assets/icon.png
```

---

## 2. WalkToUnlock

**Position:** "No steps, no scrolling." Blocks apps until you hit your step goal. The only app that makes phone addiction drive fitness.

### Competitor Context

| Competitor | Icon Style | Our Differentiation |
|-----------|-----------|---------------------|
| Opal | Minimal gem on purple/white | We're fitness-focused, they're general blocker |
| StepsApp | Green circular progress | We BLOCK apps, they just count |
| Sweatcoin | Gold coin icon | We lock phone, they reward with crypto |
| Pedometer++ | Red heart in circle | We enforce behavior, they track |
| Forest | Growing tree | We use real step data, they use timer |

**Key insight:** No fitness app LOCKS your phone based on steps. Step counters passively track. We actively block. The icon needs to communicate "locked until you walk."

### V3 Prompt (PREFERRED)

```
Create a professional mobile app icon for "WalkToUnlock" - an app that blocks your phone apps until you hit your daily step goal.

DESIGN: A stylized running shoe footprint in motion, with a circular activity ring around it (like Apple Watch rings). The ring is 70% filled with vibrant lime green, 30% empty. The footprint has dynamic motion trails suggesting movement and energy. A small subtle lock icon is integrated where the ring gap is (the unfilled portion) - suggesting "walk more to close the ring and unlock."

COLOR PALETTE:
- Footprint: crisp white (#FFFFFF) with subtle shadow
- Activity ring filled: lime green (#A5E887) to electric green (#4ADE80) gradient
- Activity ring empty: dark muted green (#1A3A1A) at 50% opacity
- Motion trails: light green (#BBF7D0) with transparency fade
- Background: deep dark green (#052E16) to forest green (#064E3B) gradient
- Lock element: white or light green, small and subtle

STYLE: Energetic, achievement-focused, gamified fitness. Should feel like closing your Apple Watch rings but with real stakes (your apps are locked). The circular progress ring is the hero element - it communicates "progress toward unlocking."

MUST INCLUDE:
- 3D depth with the ring feeling like it pops off the background
- Glossy finish on the activity ring segments
- Motion blur/trails on the footprint
- Single clear composition (ring + footprint)
- Professional gradient from dark to electric green
- iOS rounded square format
- Subtle particle effects or energy dots along the ring

MUST AVOID:
- Plain shoe or sneaker illustration
- Heart rate or health monitoring imagery
- Red or orange (too aggressive for walking)
- Flat progress bar (must be circular ring)
- Timer or clock elements
- Text or numbers
- Cluttered multiple symbols

TECHNICAL: 1024x1024 pixels. Recognizable at 60px. Works on light and dark backgrounds. High contrast between green ring and dark background.

This icon should make fitness-conscious people think "I need to close that ring." The incomplete ring is intentional - it creates desire to complete it.
```

### V3 Prompt (Alternative - Lock Focus)

```
Create a professional mobile app icon for a fitness phone-locking app.

DESIGN: A 3D padlock made of green energy/light, with a shoe footprint as the keyhole shape. The lock is surrounded by a glowing activity ring at 70% progress. Energy particles flow along the ring path.

COLOR PALETTE:
- Lock: translucent lime green (#A5E887) with glow
- Ring: electric green (#4ADE80) gradient
- Background: deep forest (#052E16) to dark (#0A0A0A)

STYLE: Fitness gamification meets phone security. Premium but energetic.

TECHNICAL: 1024x1024, 3D depth, glossy finish, glow effects, iOS rounded square. No text.
```

### Copy Commands After Generation

```bash
cp ~/Downloads/walktounlock-icon.png /Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt/MONEY_METHODS/APP_FACTORY/assets/icons/walktounlock-icon-1024-v3.png
cp ~/Downloads/walktounlock-icon.png /Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt/MONEY_METHODS/APP_FACTORY/builds/walktounlock/assets/icon.png
```

---

## 3. StudyLock

**Position:** "No study, no scrolling." The Pomodoro timer that actually enforces focus by blocking distracting apps. Average GPA increase: 0.8 points.

### Competitor Context

| Competitor | Icon Style | Our Differentiation |
|-----------|-----------|---------------------|
| Forest | Green tree growing | We block apps, they plant fake trees |
| Opal | Purple gem | We're study-specific, they're general |
| Focus Bear | Bear character | We use Pomodoro, they use habits |
| Flora | Flower growing | We enforce timer, they gamify growing |
| Flipd | Blue minimal | We track GPA impact, they just lock |

**Key insight:** Study/focus apps use growth metaphors (trees, flowers, bears). None use the BOOK + LOCK concept. The timer ring is our differentiator from generic blockers.

### V3 Prompt (PREFERRED)

```
Create a professional mobile app icon for "StudyLock" - an app that blocks TikTok, Instagram, and games until you complete your study session using a Pomodoro timer.

DESIGN: A stylized open book viewed from slightly above (3/4 angle), with a glowing Pomodoro timer circle emerging from the book's pages. The timer circle is 75% filled with vibrant indigo, showing active study progress. A subtle padlock shape is integrated into the book's spine or the unfilled timer segment. Pages of the book have a subtle glow suggesting knowledge.

COLOR PALETTE:
- Book: clean white (#F8FAFC) pages with subtle paper texture, slight shadow
- Timer ring filled: electric indigo (#6366F1) to vibrant purple (#8B5CF6) gradient
- Timer ring empty: dark muted purple (#1E1B4B) at 40% opacity
- Book spine/edges: soft indigo (#A5B4FC)
- Background: deep midnight indigo (#1E1B4B) to dark purple (#0F0B2A) gradient
- Glow from book: soft lavender (#E0E7FF) emanating upward

STYLE: Academic but modern. Should appeal to Gen Z students (18-25) not children. The combination of book + active timer says "you're studying RIGHT NOW and making progress." Premium, not cutesy.

MUST INCLUDE:
- 3D depth with the book having realistic page thickness
- Glossy finish on the timer ring
- Soft glow from the book pages (knowledge radiating)
- Single clear composition (book + timer ring)
- Professional indigo-to-purple gradient
- iOS rounded square format
- Timer ring should feel like it's actively counting down

MUST AVOID:
- Graduation caps (too literal, too young)
- Pencils, notebooks, school supplies (cluttered)
- Trees or flowers (that's Forest app's identity)
- Cartoonish or childish elements
- Red timer (too aggressive/stressful)
- Generic book without the timer element
- Light/pastel background (must be dark and focused)
- Text, numbers, or clock hands

TECHNICAL: 1024x1024 pixels. Recognizable at 60px. Works on light and dark backgrounds. The indigo-purple palette should feel focused and calm, not anxious.

This icon should make students think "productive focus time" not "restriction." The glowing book with active timer says: "you're building something right now."
```

### V3 Prompt (Alternative - Minimal)

```
Create a professional mobile app icon for a student focus app.

DESIGN: A 3D book with a circular Pomodoro timer ring rising from its open pages. The ring glows indigo-purple at 75% progress. Soft knowledge-light emanates from the book. A tiny lock keyhole is integrated into the timer gap.

COLOR PALETTE:
- Book: white with subtle shadows
- Timer: indigo (#6366F1) to purple (#8B5CF6) gradient
- Background: deep midnight (#0F0B2A) to indigo (#1E1B4B)

STYLE: Academic, modern, focused. Gen Z aesthetic. Premium but approachable.

TECHNICAL: 1024x1024, 3D depth, glossy finish, glow effects, iOS rounded square. No text.
```

### Copy Commands After Generation

```bash
cp ~/Downloads/studylock-icon.png /Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt/MONEY_METHODS/APP_FACTORY/assets/icons/studylock-icon-1024-v3.png
cp ~/Downloads/studylock-icon.png /Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt/MONEY_METHODS/APP_FACTORY/builds/studylock/assets/icon.png
```

---

## 4. BioMaxx (Reference - V2 Already Exists)

BioMaxx already has a V2 prompt in `ICON_PROMPTS_V2.txt` and a generated icon at `assets/icons/biomaxx-icon-1024.png`. Included here for completeness.

**If regenerating:** Use the V2 prompt from ICON_PROMPTS_V2.txt (DNA helix + lightning bolt, emerald green to teal, dark slate background).

```bash
# Copy existing icon to build
cp /Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt/MONEY_METHODS/APP_FACTORY/assets/icons/biomaxx-icon-1024.png /Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt/MONEY_METHODS/APP_FACTORY/builds/biomaxx-sdk54/assets/icon.png
```

---

## Design System: The "Lock App" Family

All 4 Lock Apps share a visual DNA for brand recognition:

| App | Primary Color | Symbol | Lock Element |
|-----|--------------|--------|-------------|
| PrayerLock | Gold (#D4AF37) | Padlock with divine light | Lock IS the symbol |
| WalkToUnlock | Lime Green (#A5E887) | Activity ring + footprint | Lock in ring gap |
| StudyLock | Indigo (#6366F1) | Book + timer ring | Lock in timer gap |
| BioMaxx | Emerald (#10B981) | DNA helix + lightning | N/A (different brand) |

**Shared traits across Lock Apps:**
- Dark backgrounds (midnight blue, forest green, deep indigo)
- Circular progress/ring elements
- Warm glow effects suggesting achievement
- 3D depth with glossy finish
- Lock symbolism integrated subtly (not dominant)

**What makes them a FAMILY without being identical:**
- Each has a unique color identity
- Each has a niche-specific hero element (prayer light, step ring, study book)
- The lock concept ties them together
- Dark-to-vibrant gradient pattern is consistent
- Same quality level signals "same publisher"

---

## Generation Workflow

### Step 1: Generate (Human Task)

Pick your tool and generate each icon:
1. Open Ideogram/DALL-E/AI Studio
2. Paste the PREFERRED prompt for each app
3. Generate 4 variations per app
4. Pick the best one
5. Download as PNG (1024x1024)

### Step 2: Copy to Builds

```bash
# Create directories if needed
mkdir -p /Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt/MONEY_METHODS/APP_FACTORY/builds/prayerlock/assets
mkdir -p /Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt/MONEY_METHODS/APP_FACTORY/builds/prayerlock-sdk54/assets
mkdir -p /Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt/MONEY_METHODS/APP_FACTORY/builds/walktounlock/assets
mkdir -p /Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt/MONEY_METHODS/APP_FACTORY/builds/studylock/assets

# After downloading icons from AI tool:
cp ~/Downloads/prayerlock-icon.png builds/prayerlock/assets/icon.png
cp ~/Downloads/prayerlock-icon.png builds/prayerlock-sdk54/assets/icon.png
cp ~/Downloads/walktounlock-icon.png builds/walktounlock/assets/icon.png
cp ~/Downloads/studylock-icon.png builds/studylock/assets/icon.png

# Also save to central icons directory
cp ~/Downloads/prayerlock-icon.png assets/icons/prayerlock-icon-1024-v3.png
cp ~/Downloads/walktounlock-icon.png assets/icons/walktounlock-icon-1024-v3.png
cp ~/Downloads/studylock-icon.png assets/icons/studylock-icon-1024-v3.png
```

### Step 3: Verify

```bash
# Check all icons exist
ls -la assets/icons/*-v3.png
ls -la builds/prayerlock*/assets/icon.png
ls -la builds/walktounlock/assets/icon.png
ls -la builds/studylock/assets/icon.png
```

### Step 4: Quality Check

For each generated icon:
- [ ] Recognizable at 60x60px (zoom browser to see)
- [ ] Works on both light and dark backgrounds
- [ ] No fine details that disappear small
- [ ] Unique from competitor icons
- [ ] Has 3D depth (not flat)
- [ ] Has glow/reflection effects
- [ ] No text or letters visible
- [ ] Matches the app's color identity
- [ ] Feels premium ("$10M funded app" test)

---

## Checkpoint: Human Action Required

- [ ] Generate PrayerLock icon using V3 prompt above
- [ ] Generate WalkToUnlock icon using V3 prompt above
- [ ] Generate StudyLock icon using V3 prompt above
- [ ] Copy BioMaxx existing icon to build directory
- [ ] Copy all icons to respective build directories
- [ ] Verify all icons pass quality checklist
- [ ] Launch in iOS Simulator to see icons on home screen
