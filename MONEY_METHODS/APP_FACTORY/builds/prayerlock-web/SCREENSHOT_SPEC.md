# PrayerLock — Screenshot Capture Spec

## Required Dimensions
- **iOS:** 1290 x 2796px (iPhone 15 Pro Max)
- **Android:** 1080 x 1920px minimum

## Screenshot List (6 recommended)

### Screenshot 1: Prayer Timer — HERO SHOT
**Screen:** Timer tab, active countdown
**State:**
- Timer running: 14:23 remaining (out of 20 min)
- Circular progress ring: ~28% complete
- Teal glow effect active (timer-active CSS class)
- Sound selector showing: 🌧 Rain (active)
- "In Prayer" status indicator
- Dark background with Islamic geometric pattern subtle
**Caption overlay:** "Focus. Pray. Repeat."
**Notes:** This is the hero screenshot — most visually impressive

### Screenshot 2: Streak Tracker
**Screen:** Streak tab
**State:**
- Contribution graph showing 34 consecutive days filled (teal squares)
- Current streak counter: 🔥 34 days
- Best streak: 34 days (in progress)
- "30 Day Milestone" badge visible and unlocked
- Last 4 weeks completely filled (green squares), then tapering off 2 months back
**Caption:** "Don't break the chain"
**Notes:** Full streak is emotionally compelling. Make it look aspirational.

### Screenshot 3: Qibla Compass
**Screen:** Qibla tab
**State:**
- Compass face showing
- Needle pointing ~45° (northeast, as if user is in North America)
- "Direction to Mecca" label
- Coordinates shown: 40.7128° N, 74.0060° W
- Bearing: 58.3°
- "Accurate to ±2°" note visible
**Caption:** "Find Mecca from anywhere"

### Screenshot 4: Tasbih Counter
**Screen:** Tasbih tab
**State:**
- Large counter showing: 66 / 99
- Progress ring: 66% complete
- Session target: SubhanAllah (99x)
- Haptic feedback indicator (pulse ring)
- Previous sessions: 33/33 ✓ completed
**Caption:** "Tap. Count. Complete."

### Screenshot 5: Daily Verse
**Screen:** Verse/Dua tab
**State:**
- Arabic text displayed in large, beautiful Arabic typography (RTL)
- English translation below: "And whoever relies upon Allah — then He is sufficient for him. Indeed, Allah will accomplish His purpose." (Quran 65:3)
- Share button visible
- Date: Today's date
- Category badge: Quran
**Caption:** "One verse. Every day."

### Screenshot 6: App Overview / Home
**Screen:** Home screen / dashboard
**State:**
- All 5 tab icons visible at bottom: Timer, Streak, Qibla, Tasbih, Verse
- Today's prayer summary card:
  - "Today's Goal: 20 min"
  - Progress: "14 min logged"
  - Streak: 34 days
- Clean, professional layout showing full capability
**Caption:** "Everything in one place"

## Capture via Playwright
```python
from playwright.sync_api import sync_playwright

screens = [
    ("timer", "timer_tab_button"),
    ("streak", "streak_tab_button"),
    ("qibla", "qibla_tab_button"),
    ("tasbih", "tasbih_tab_button"),
    ("verse", "verse_tab_button"),
]

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 390, "height": 844})  # iPhone 14
    page.goto("https://prayerlock.surge.sh")
    page.wait_for_load_state("networkidle")

    for name, selector in screens:
        page.click(f"[data-tab='{name}']")
        page.wait_for_timeout(500)
        page.screenshot(path=f"prayerlock_ios_{name}.png")
    browser.close()
```

## File Naming
```
prayerlock_ios_01_timer_active.png          ← HERO
prayerlock_ios_02_streak_34day.png
prayerlock_ios_03_qibla_compass.png
prayerlock_ios_04_tasbih_counter.png
prayerlock_ios_05_daily_verse.png
prayerlock_ios_06_home_overview.png
```

## Design Notes for Screenshots
- Add device frame using shots.so or mockuphone.com
- Use deep teal (#0d9488) as the accent color in any marketing frames
- The Islamic geometric pattern background sells the aesthetic immediately
- Streak screenshot is highest-converting — put it second (after timer hero)
- For Play Store feature graphic: use the streak tab with flame emoji prominent
