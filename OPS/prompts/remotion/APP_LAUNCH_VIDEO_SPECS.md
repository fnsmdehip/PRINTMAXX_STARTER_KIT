# App Launch Video Specifications

**Purpose:** Production-ready Remotion video specs for PrayerLock, WalkToUnlock, and StudyLock launches
**Format:** Vertical (1080x1920) for TikTok/Reels
**FPS:** 30fps
**Output:** `/LANDING/printmaxx-site/out/` or app-specific `builds/{app}/marketing/videos/`

---

## Quick Reference

| App | Primary Color | Secondary Color | Mood | Music Style |
|-----|---------------|-----------------|------|-------------|
| PrayerLock | Gold #F5A623 | Deep Blue #1A237E | Peaceful, warm | Worship ambient, soft piano |
| WalkToUnlock | Electric Green #00FF88 | Charcoal #1A1A1A | Energetic, competitive | Brazilian phonk, aggressive trap |
| StudyLock | Electric Blue #0066FF | Clean White #FFFFFF | Focused, academic | Lo-fi beats, minimal electronic |

---

## 1. App Announcement Video (15-30 seconds)

### Structure (900 frames at 30fps = 30 seconds)

```
0-90 frames (3s):    HOOK - Bold claim + visual impact
90-270 frames (6s):   PROBLEM - Relatable struggle
270-540 frames (9s):  SOLUTION - App reveal + key features
540-750 frames (7s):  PROOF - Social proof or stats
750-900 frames (5s):  CTA - Download now
```

---

### PrayerLock Announcement

**Duration:** 25 seconds (750 frames)
**Tone:** Warm, inviting, not preachy

#### Scene Breakdown

| Frames | Duration | Scene | Visual | Text Overlay |
|--------|----------|-------|--------|--------------|
| 0-75 | 2.5s | Hook | Phone screen with social apps glowing, fade to peaceful sunrise | "What if you couldn't scroll until you prayed?" |
| 75-180 | 3.5s | Problem | Split screen: Left=doomscrolling in bed, Right=stressed person | "We reach for our phones before God." |
| 180-270 | 3s | Transition | Gold light rays wipe across screen | - |
| 270-450 | 6s | Solution | App icon animates in with dove particles, then 3 feature cards cascade | "PrayerLock: Pray First, Phone Second" |
| 450-600 | 5s | Features | Animated mockups showing: lock screen, verse display, streak counter | "Daily verse / Prayer timer / Streak tracking" |
| 600-675 | 2.5s | Proof | Counter animation: "10,000+ faithful users" | "Join the community" |
| 675-750 | 2.5s | CTA | App icon pulses, App Store badge appears | "Download free today" |

#### Typography

```
Headlines: Playfair Display Bold (elegant serif)
Body/Features: Inter Medium
Size: 64-80px for headlines, 48px for features
Line height: 1.1
```

#### Color Palette

```css
--primary: #F5A623 (warm gold)
--secondary: #1A237E (deep blue)
--background: linear-gradient(180deg, #1A237E 0%, #0D1642 100%)
--text: #F8FAFC (soft white)
--accent-glow: rgba(245, 166, 35, 0.5)
```

#### Animation Config

```tsx
// Gentle, peaceful animations
const faithSpring = {
  damping: 25,
  stiffness: 80,
  mass: 1
};

// Scene transitions
const sunriseWipe = {
  duration: 45, // 1.5s
  easing: 'easeInOut',
  direction: 'radial-center'
};
```

#### Music Recommendations

**Primary:** Worship ambient, peaceful piano
**Royalty-Free Sources:**
- Pixabay: "worship ambient", "inspirational piano"
- Uppbeat: "spiritual", "reflective"
- YouTube Audio Library: "cinematic emotional piano"

**Volume Mix:**
- 0-75 frames: -9dB (hook impact)
- 75-600 frames: -12dB (under content)
- 600-750 frames: Fade to -18dB (CTA clarity)

**BPM Target:** 60-80 BPM (slow, peaceful)

---

### WalkToUnlock Announcement

**Duration:** 25 seconds (750 frames)
**Tone:** High energy, motivating, competitive

#### Scene Breakdown

| Frames | Duration | Scene | Visual | Text Overlay |
|--------|----------|-------|--------|--------------|
| 0-60 | 2s | Hook | Phone slams onto pillow, alarm buzzes, hand reaches | "You can't scroll yet." |
| 60-150 | 3s | Problem | Split: zombie scrolling vs stressed at work | "Phone addiction is killing your gains." |
| 150-210 | 2s | Transition | Green energy burst wipe with motion blur | - |
| 210-420 | 7s | Solution | Running shoe icon bounces in with speed lines, step counter animates 0->1000 | "WalkToUnlock: Walk Before You Scroll" |
| 420-540 | 4s | Features | Rapid-fire feature cards with bounce animations | "Step lock / Progress bar / Streaks" |
| 540-660 | 4s | Proof | Step counter races up: "5M+ steps unlocked" | "Join the movement" |
| 660-750 | 3s | CTA | Phone unlocks with confetti, App Store badge | "Download. Walk. Unlock." |

#### Typography

```
Headlines: Inter Black (impact)
Body/Features: Inter Bold
Size: 72-96px for headlines (bigger = energy)
Line height: 1.0
```

#### Color Palette

```css
--primary: #00FF88 (electric green)
--secondary: #1A1A1A (charcoal)
--background: linear-gradient(135deg, #1A1A1A 0%, #0F2818 100%)
--text: #FFFFFF
--accent-glow: rgba(0, 255, 136, 0.6)
--energy-pulse: #00FF88 with 0.3 opacity pulse
```

#### Animation Config

```tsx
// Bouncy, energetic animations
const fitnessSpring = {
  damping: 10,
  stiffness: 250,
  mass: 0.8
};

// Counter animation (dramatic climb)
const stepCounter = {
  from: 0,
  to: 10000,
  duration: 90, // 3s
  easing: 'easeOut'
};
```

#### Music Recommendations

**Primary:** Brazilian phonk (GOZALO, ACELERADA style)
**Royalty-Free Sources:**
- FreeToUse: extensive phonk library
- Pixabay: "phonk aggressive bass"
- Tunetank: "Tempest" by SLXSH, "Boom Pop" by KXLLYXU

**Volume Mix:**
- 0-60 frames: -6dB (hook slam)
- 60-540 frames: -9dB (energy maintain)
- 540-750 frames: Build to -6dB then fade

**BPM Target:** 140-150 BPM (sync cuts to beat)

**Beat Sync Points:**
- Frame 0: Bass hit on "You can't scroll"
- Frame 150: Drop on transition wipe
- Frame 210: Build into solution reveal
- Frame 540: Heavy bass under counter animation

---

### StudyLock Announcement

**Duration:** 25 seconds (750 frames)
**Tone:** Smart, focused, encouraging

#### Scene Breakdown

| Frames | Duration | Scene | Visual | Text Overlay |
|--------|----------|-------|--------|--------------|
| 0-75 | 2.5s | Hook | Student staring at phone, textbooks ignored | "Your phone is stealing your A's." |
| 75-180 | 3.5s | Problem | Split: TikTok scroll vs panicked studying before exam | "5 hours on social media. 0 hours studying." |
| 180-240 | 2s | Transition | Blue particles form timer shape | - |
| 240-450 | 7s | Solution | Graduation cap icon with study particles, timer animates | "StudyLock: Study First, Scroll Later" |
| 450-570 | 4s | Features | Clean cards slide in from sides | "Focus timer / Quiz checks / Study stats" |
| 570-660 | 3s | Proof | Report card animation: grades improve | "GPA +0.8 average improvement" |
| 660-750 | 3s | CTA | Lock icon transforms to open, App Store badge | "Ace your exams. Download now." |

#### Typography

```
Headlines: Inter Bold (clean, academic)
Body/Features: Inter Medium
Size: 64-80px for headlines
Line height: 1.15
```

#### Color Palette

```css
--primary: #0066FF (electric blue)
--secondary: #FFFFFF (clean white)
--background: linear-gradient(180deg, #FFFFFF 0%, #E8F0FF 100%)
--text-dark: #1A1A2E
--accent-glow: rgba(0, 102, 255, 0.4)
```

#### Animation Config

```tsx
// Clean, precise animations
const studySpring = {
  damping: 15,
  stiffness: 180,
  mass: 1
};

// Timer typewriter effect
const timerType = {
  characters: ['2', '5', ':', '0', '0'],
  stagger: 6, // frames between chars
};
```

#### Music Recommendations

**Primary:** Lo-fi beats, minimal electronic
**Royalty-Free Sources:**
- Pixabay: "lofi study", "minimal electronic"
- Lo-fi Girl licensed tracks
- YouTube Audio Library: study/focus category

**Volume Mix:**
- Consistent -12dB throughout
- No major drops (maintain focus feeling)
- Fade to -18dB on CTA

**BPM Target:** 70-90 BPM (study pace)

---

## 2. Feature Highlight Video (10-15 seconds)

### Template Structure (450 frames at 30fps = 15 seconds)

```
0-45 frames (1.5s):   HOOK - Feature in action
45-270 frames (7.5s): DEMO - Feature showcase
270-390 frames (4s):  BENEFIT - What user gets
390-450 frames (2s):  CTA - Quick download prompt
```

### Format: Quick Hook + Demo + CTA

**Aspect Ratio:** 9:16 (1080x1920)
**Key Rule:** Show feature working in first 3 seconds

---

### PrayerLock Feature Videos

#### Feature 1: Morning Lock

| Frames | Visual | Text |
|--------|--------|------|
| 0-45 | Phone alarm rings, screen shows lock with praying hands | "Your phone knows you need to pray first" |
| 45-180 | User taps phone, prayer prompt appears with verse | "Daily verse. Guided prompts." |
| 180-270 | Timer starts, peaceful animation | "5 minutes with God" |
| 270-390 | Timer completes, phone unlocks with golden glow | "Then your phone unlocks" |
| 390-450 | App icon + "Link in bio" | "PrayerLock - free download" |

#### Feature 2: Streak Tracking

| Frames | Visual | Text |
|--------|--------|------|
| 0-45 | Calendar view with fire streak emoji | "47 days of morning prayer" |
| 45-180 | Streak counter animates up, calendar fills with checks | - |
| 180-270 | Close-up of streak number with glow | "Don't break the chain" |
| 270-390 | Share button appears, social preview | "Share your journey" |
| 390-450 | App icon + CTA | "Start your streak today" |

#### Feature 3: Daily Verse

| Frames | Visual | Text |
|--------|--------|------|
| 0-45 | Beautiful verse on screen, golden text | Scripture text |
| 45-180 | Verse animates word by word | - |
| 180-270 | Reflection prompt appears below | "What does this mean to you?" |
| 270-390 | User types response (blur), peace animation | "Start each day grounded" |
| 390-450 | App icon + CTA | "Get your daily verse" |

---

### WalkToUnlock Feature Videos

#### Feature 1: Step Lock

| Frames | Visual | Text |
|--------|--------|------|
| 0-45 | Phone locked, "1000 steps to unlock" | "Your phone is locked." |
| 45-180 | POV walking footage, step counter climbing rapidly | - |
| 180-270 | Counter hits target with explosion effect | "UNLOCKED" |
| 270-390 | Phone home screen appears with confetti | "Earned your scroll time" |
| 390-450 | App icon + CTA | "WalkToUnlock - free" |

#### Feature 2: Progress Bar

| Frames | Visual | Text |
|--------|--------|------|
| 0-45 | Lock screen with green progress bar at 20% | "Only 800 steps to go" |
| 45-180 | Progress bar fills with satisfying animation | - |
| 180-270 | Bar completes with pulse effect | "100% Complete" |
| 270-390 | Achievement badge pops up | "Morning Walker badge earned" |
| 390-450 | App icon + CTA | "Download and walk" |

#### Feature 3: Streaks & Achievements

| Frames | Visual | Text |
|--------|--------|------|
| 0-45 | Trophy case with badges | "31 day streak. 150k steps." |
| 45-180 | Badges animate in one by one | - |
| 180-270 | Personal record highlight | "New record: 15k steps in one day" |
| 270-390 | Leaderboard preview | "You're #3 this week" |
| 390-450 | App icon + CTA | "Join the leaderboard" |

---

### StudyLock Feature Videos

#### Feature 1: Pomodoro Lock

| Frames | Visual | Text |
|--------|--------|------|
| 0-45 | Phone shows "Phone locked for 25 min" | "No distractions allowed" |
| 45-180 | Timer countdown with study environment | - |
| 180-270 | Timer completes, phone unlocks | "5 min break earned" |
| 270-390 | Break timer starts, cycle visual | "Then back to focus" |
| 390-450 | App icon + CTA | "StudyLock - ace your exams" |

#### Feature 2: Quiz Checks

| Frames | Visual | Text |
|--------|--------|------|
| 0-45 | Quiz question pops up during study | "Quick check: still focused?" |
| 45-180 | User answers correctly, checkmark animation | - |
| 180-270 | Wrong answer adds time (dramatic) | "+5 minutes if you're distracted" |
| 270-390 | Completion celebration | "Quiz passed. Keep going!" |
| 390-450 | App icon + CTA | "Study smarter" |

#### Feature 3: Study Stats

| Frames | Visual | Text |
|--------|--------|------|
| 0-45 | Dashboard with study hours | "42 hours this week" |
| 45-180 | Charts animate in, subjects breakdown | - |
| 180-270 | Focus score highlight | "Focus score: 94/100" |
| 270-390 | Compare to last week (improvement) | "Up 28% from last week" |
| 390-450 | App icon + CTA | "Track your focus" |

---

## 3. Testimonial Video Template (20-30 seconds)

### Structure (900 frames = 30 seconds)

```
0-120 frames (4s):    BEFORE - The struggle
120-180 frames (2s):  TRANSITION - Discovery moment
180-600 frames (14s): AFTER - Transformation + quote
600-780 frames (6s):  PROOF - Stats or visual evidence
780-900 frames (4s):  CTA - Join them
```

### Visual Style: Text-Based Testimonial

**No voiceover required.** All text overlay with stock/generated visuals.

---

### Template: Transformation Story

| Section | Frames | Visual | Text Pattern |
|---------|--------|--------|--------------|
| Before | 0-120 | Relatable struggle footage | "I used to [BAD HABIT]" |
| Transition | 120-180 | App discovery moment | "Then I found [APP]" |
| Quote | 180-420 | Happy user footage/aesthetic | "[TESTIMONIAL QUOTE]" |
| Stats | 420-600 | Achievement/numbers | "[SPECIFIC RESULT]" |
| Social Proof | 600-780 | Multiple testimonials cascade | "Join 10,000+ users" |
| CTA | 780-900 | App icon + download | "Link in bio" |

---

### PrayerLock Testimonials

#### Testimonial 1: "Morning Transformation"

| Frames | Visual | Text |
|--------|--------|------|
| 0-120 | Person doomscrolling in bed | "I used to waste my first hour on Instagram" |
| 120-180 | Golden sunrise fade | "Then I found PrayerLock" |
| 180-420 | Peaceful morning routine, journaling | "Now I start every day with God. My anxiety is down. My peace is up." |
| 420-600 | Counter: "90+ day streak" | "90 days of consistent morning prayer" |
| 600-780 | Multiple quote cards cascade | "Changed my life" / "Best app ever" / "So peaceful" |
| 780-900 | App icon pulse | "Start your morning right" |

#### Testimonial 2: "Family Accountability"

| Frames | Visual | Text |
|--------|--------|------|
| 0-120 | Family members on phones | "My family was always on our phones at breakfast" |
| 120-180 | App icon transition | "We all downloaded PrayerLock" |
| 180-420 | Family praying together, putting phones away | "Now we pray together before anyone scrolls. It's brought us closer." |
| 420-600 | "4 family members / 247 days / 988 prayers" | - |
| 600-780 | Heart reaction, family testimonials | - |
| 780-900 | App icon + "Family plan available" | - |

---

### WalkToUnlock Testimonials

#### Testimonial 1: "Step Challenge"

| Frames | Visual | Text |
|--------|--------|------|
| 0-120 | Sedentary person at desk | "I averaged 2,000 steps a day" |
| 120-180 | Running shoe animation | "WalkToUnlock changed that" |
| 180-420 | Person walking, hiking, active lifestyle | "Now I hit 10k before I even check my phone. Lost 15 lbs in 3 months." |
| 420-600 | Counter racing: "2k -> 10k daily average" | "5x more active" |
| 600-780 | Fitness photos before/after | - |
| 780-900 | App icon + energy burst | "Walk more. Scroll less." |

#### Testimonial 2: "Morning Energy"

| Frames | Visual | Text |
|--------|--------|------|
| 0-120 | Groggy morning, reaching for phone | "I used to scroll for 30 min before getting up" |
| 120-180 | Green energy transition | - |
| 180-420 | Energetic morning walk, sunrise | "Now I'm outside walking before my brain wakes up. Best decision ever." |
| 420-600 | "6am walks every day / 127 day streak" | - |
| 600-780 | Energy level comparison visual | - |
| 780-900 | App icon | "Try it free" |

---

### StudyLock Testimonials

#### Testimonial 1: "GPA Boost"

| Frames | Visual | Text |
|--------|--------|------|
| 0-120 | Student distracted by phone | "I couldn't focus. My GPA was 2.7." |
| 120-180 | Blue particles transition | "I downloaded StudyLock" |
| 180-420 | Focused studying, library scene | "Forced myself to study before scrolling. Pulled my GPA to 3.5 in one semester." |
| 420-600 | Report card animation: 2.7 -> 3.5 | "+0.8 GPA improvement" |
| 600-780 | College acceptance letter visual | - |
| 780-900 | App icon | "Your grades matter" |

#### Testimonial 2: "Finals Prep"

| Frames | Visual | Text |
|--------|--------|------|
| 0-120 | Panicked cramming | "I always crammed the night before" |
| 120-180 | Timer lock visual | - |
| 180-420 | Organized study sessions | "StudyLock helped me study consistently. First time I wasn't stressed for finals." |
| 420-600 | "142 hours studied / 12 exams / All A's" | - |
| 600-780 | Celebration confetti | - |
| 780-900 | App icon | "Finals season ready?" |

---

## 4. Tutorial/How-To Video (30-60 seconds)

### Structure (1800 frames at 30fps = 60 seconds)

```
0-90 frames (3s):     HOOK - Result preview
90-180 frames (3s):   INTRO - What we're doing
180-1440 frames (42s): STEPS - 4-6 numbered steps
1440-1620 frames (6s): RESULT - Final outcome
1620-1800 frames (6s): CTA - Download
```

### Style: Screen Recording + Annotations

**Visual:** Actual app screens with cursor/finger indicators
**Text:** Large numbered steps, clear labels
**Audio:** Lo-fi background, no voiceover (text-based)

---

### PrayerLock Tutorial: "Setup Your Morning Prayer Lock"

| Step | Frames | Screen | Text Overlay |
|------|--------|--------|--------------|
| Hook | 0-90 | Lock screen with verse | "Set up morning prayer in 60 seconds" |
| Step 1 | 180-420 | Download from App Store | "Step 1: Download PrayerLock (free)" |
| Step 2 | 420-660 | Onboarding: select wake time | "Step 2: Set your wake-up time" |
| Step 3 | 660-900 | Choose prayer duration | "Step 3: Pick prayer length (start with 5 min)" |
| Step 4 | 900-1140 | Enable notifications | "Step 4: Allow notifications for reminders" |
| Step 5 | 1140-1380 | First prayer screen | "Step 5: Pray and unlock" |
| Result | 1440-1620 | Streak counter at day 1 | "Day 1 complete. See you tomorrow." |
| CTA | 1620-1800 | App icon + badge | "Link in bio" |

---

### WalkToUnlock Tutorial: "Lock Your Phone Until You Walk"

| Step | Frames | Screen | Text Overlay |
|------|--------|--------|--------------|
| Hook | 0-90 | Phone unlocking after step counter hits target | "Your phone. Locked until you walk." |
| Step 1 | 180-420 | App Store download | "Step 1: Download WalkToUnlock" |
| Step 2 | 420-660 | Health permissions | "Step 2: Allow step tracking" |
| Step 3 | 660-900 | Set step goal (1000) | "Step 3: Set your step goal" |
| Step 4 | 900-1140 | Choose lock time | "Step 4: Set when to lock (try 7am)" |
| Step 5 | 1140-1380 | Lock activates, walking begins | "Step 5: Walk and watch the counter rise" |
| Result | 1440-1620 | Phone unlocks with animation | "Unlocked. Now you've earned your phone time." |
| CTA | 1620-1800 | App icon with footsteps | "Start walking tomorrow" |

---

### StudyLock Tutorial: "Force Yourself to Study"

| Step | Frames | Screen | Text Overlay |
|------|--------|--------|--------------|
| Hook | 0-90 | Lock screen during study session | "Your phone can't distract you anymore" |
| Step 1 | 180-420 | Download screen | "Step 1: Download StudyLock" |
| Step 2 | 420-660 | Choose mode (Pomodoro) | "Step 2: Pick focus mode" |
| Step 3 | 660-900 | Set study duration | "Step 3: Set your session (25 min)" |
| Step 4 | 900-1140 | Start session, phone locks | "Step 4: Tap start. Phone locks." |
| Step 5 | 1140-1260 | Quiz question appears | "Step 5: Answer check-ins to stay focused" |
| Step 6 | 1260-1380 | Timer completes | "Step 6: Complete timer to unlock" |
| Result | 1440-1620 | Study stats dashboard | "Track your focus. Ace your exams." |
| CTA | 1620-1800 | App icon | "Finals start now" |

---

## Technical Specifications Summary

### Export Settings

```javascript
const config = {
  width: 1080,
  height: 1920,
  fps: 30,
  codec: 'h264',
  crf: 18, // High quality
  audioCodec: 'aac',
  audioBitrate: '192k',
};
```

### Font Stack

```css
/* Faith Apps */
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Inter:wght@400;500;700&display=swap');

/* Fitness Apps */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@700;900&display=swap');

/* Study Apps */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@500;700&display=swap');
```

### Shared Components

```tsx
// Reusable across all app videos

// App icon entrance with particles
const AppIconReveal = ({ icon, color, particleCount = 15 }) => {...};

// Feature card cascade
const FeatureCards = ({ features, stagger = 15 }) => {...};

// Counter animation
const AnimatedCounter = ({ from, to, duration, suffix }) => {...};

// Progress bar
const ProgressBar = ({ progress, color, height = 12 }) => {...};

// CTA button pulse
const CTAButton = ({ text, color, pulse = true }) => {...};

// Streak fire
const StreakFire = ({ count }) => {...};
```

---

## Asset Checklist Per App

### Before Creating Videos

- [ ] App icon generated (1024x1024)
- [ ] Color palette defined in CSS vars
- [ ] Font files available
- [ ] Music track selected and licensed
- [ ] Stock footage identified (if needed)
- [ ] Screenshot mockups ready

### Output Files

```
builds/{app}/marketing/videos/
├── announcement_v1.mp4
├── feature_lock_v1.mp4
├── feature_streak_v1.mp4
├── feature_tracking_v1.mp4
├── testimonial_transform_v1.mp4
├── tutorial_setup_v1.mp4
└── thumbnails/
    ├── announcement_thumb.png
    └── tutorial_thumb.png
```

---

## Quick Generation Commands

```bash
# Generate all videos for an app
npx remotion render src/Video.tsx --props='{"app":"prayerlock","type":"announcement"}'
npx remotion render src/Video.tsx --props='{"app":"prayerlock","type":"feature-lock"}'
npx remotion render src/Video.tsx --props='{"app":"prayerlock","type":"testimonial"}'
npx remotion render src/Video.tsx --props='{"app":"prayerlock","type":"tutorial"}'

# Preview before render
npx remotion preview src/Video.tsx --props='{"app":"walktounlock","type":"announcement"}'

# Batch render all apps
for app in prayerlock walktounlock studylock; do
  for type in announcement feature-lock testimonial tutorial; do
    npx remotion render src/Video.tsx --props="{\"app\":\"$app\",\"type\":\"$type\"}" -o "out/$app-$type.mp4"
  done
done
```

---

## Sound Design Quick Reference

| App | Primary Music | BPM | Volume | Beat Sync |
|-----|---------------|-----|--------|-----------|
| PrayerLock | Worship ambient | 60-80 | -12dB constant | Slow, gentle cuts |
| WalkToUnlock | Brazilian phonk | 140-150 | -6 to -9dB | Every 2 beats |
| StudyLock | Lo-fi beats | 70-90 | -12dB constant | Every 4 beats |

**Royalty-Free Sources:**
- Pixabay: pixabay.com/music
- FreeToUse: freetouse.com/music (best for phonk)
- Uppbeat: uppbeat.io
- Mixkit: mixkit.co/free-stock-music

**Full sound design guide:** `SOUND_DESIGN_GUIDE.md`

---

## Related Files

- `REMOTION_MASTER_PROMPT.md` - Full production prompts by style
- `REMOTION_VIDEO_PROMPT.md` - Animation guidelines and component patterns
- `SOUND_DESIGN_GUIDE.md` - Comprehensive audio selection
- `TIKTOK_MUSIC_TRENDS.md` - Current trending sounds
- `ASSET_GENERATION_GUIDE.md` - Icon and illustration generation

---

**Created:** 2026-01-24
**Last Updated:** 2026-01-24
