# App Store Screenshot Layout Guide — PRINTMAXX

---

## Required Screenshot Sizes

### iPhone 6.5" Display (iPhone 15 Pro Max, 14 Plus, etc.)
- **Size:** 1290 x 2796 px (portrait) or 2796 x 1290 px (landscape)
- **Required:** Yes — primary display size in App Store
- **Count:** 3-10 screenshots per localization

### iPhone 5.5" Display (iPhone 8 Plus, legacy)
- **Size:** 1242 x 2208 px (portrait) or 2208 x 1242 px (landscape)
- **Required:** Yes — required for older device support
- **Count:** 3-10 screenshots

### iPad 12.9" (if applicable)
- **Size:** 2048 x 2732 px (portrait) or 2732 x 2048 px (landscape)

---

## Screenshot Layout System

Each app should follow this 6-screenshot sequence:

### Screenshot 1: Hero / Value Proposition
```
+---------------------------+
|      [App Icon - small]   |
|                           |
|   ONE-LINE HEADLINE       |
|   that captures value     |
|                           |
|  +---------------------+  |
|  |                     |  |
|  |   DEVICE MOCKUP     |  |
|  |   showing main      |  |
|  |   screen of app     |  |
|  |                     |  |
|  +---------------------+  |
|                           |
|   Brief tagline here      |
+---------------------------+
```

### Screenshot 2: Key Feature A
```
+---------------------------+
|                           |
|   FEATURE HEADLINE        |
|   e.g. "Lock In Your      |
|   Focus"                  |
|                           |
|  +---------------------+  |
|  |                     |  |
|  |   FEATURE SCREEN    |  |
|  |   with UI visible   |  |
|  |                     |  |
|  +---------------------+  |
|                           |
|   Supporting text          |
+---------------------------+
```

### Screenshot 3: Key Feature B
Same layout as Screenshot 2, different feature.

### Screenshot 4: Social Proof / Stats
```
+---------------------------+
|                           |
|   "Trusted by X users"    |
|   or key metric           |
|                           |
|  +-----+  +-----+        |
|  |     |  |     |        |
|  | Stat|  | Stat|        |
|  |     |  |     |        |
|  +-----+  +-----+        |
|                           |
|  +---------------------+  |
|  |   APP SCREEN        |  |
|  +---------------------+  |
+---------------------------+
```

### Screenshot 5: Customization / Settings
```
+---------------------------+
|                           |
|   "Make It Yours"          |
|                           |
|  +---------------------+  |
|  |   Settings or       |  |
|  |   customization     |  |
|  |   screen            |  |
|  +---------------------+  |
|                           |
|   Highlight key options    |
+---------------------------+
```

### Screenshot 6: CTA / Closing
```
+---------------------------+
|                           |
|                           |
|   DOWNLOAD NOW             |
|   [App Icon - large]      |
|                           |
|   "Your [value] starts    |
|    today"                 |
|                           |
|   Key bullet points:      |
|   - Feature 1             |
|   - Feature 2             |
|   - Feature 3             |
|                           |
+---------------------------+
```

---

## Design Rules

### Typography on Screenshots
- **Headline:** 64-80px, bold (use brand heading font)
- **Subtext:** 32-40px, regular weight
- **Maximum 6 words per headline** — users scan fast

### Device Frame
- Use iPhone 15 Pro frame (titanium finish) for premium feel
- Frame should be approximately 65% of screenshot height
- Slightly rotated (5-8 degrees) for dynamic feel on Screenshot 1

### Background Treatment by App

| App        | Background Style                                    |
|------------|-----------------------------------------------------|
| PrayerLock | Deep navy gradient `#1A237E` to `#0D1442`           |
| Hilal      | Emerald gradient `#1B5E20` to `#0A2E10`             |
| FocusLock  | Orange gradient `#E65100` to `#BF360C`              |
| Dusk       | Purple gradient `#4A148C` to `#1A0A3E`              |
| Mise       | Red gradient `#BF360C` to `#7F1D0E`                 |
| StepLock   | Blue gradient `#0D47A1` to `#01579B`                |
| Streakr    | Amber gradient `#FF6F00` to `#E65100`               |

### Spacing
- **Top/bottom safe area:** 80px minimum
- **Side padding:** 60px minimum
- **Between text and device:** 40px

### Status Bar
- Always show a clean status bar: 9:41 AM, full battery, full signal
- Use white status bar on dark backgrounds, black on light

---

## Google Play Feature Graphic

- **Size:** 1024 x 500 px
- Landscape, no device frame
- App name + tagline + key visual
- Separate HTML templates provided in this directory

---

## File Naming Convention

```
[app_name]_screenshot_[number]_[size].png

Examples:
prayerlock_screenshot_01_6.5.png
prayerlock_screenshot_01_5.5.png
hilal_screenshot_02_6.5.png
```

## Export Settings
- Format: PNG (no JPEG)
- Color space: sRGB
- No alpha channel
- No rounded corners (App Store applies them automatically)
