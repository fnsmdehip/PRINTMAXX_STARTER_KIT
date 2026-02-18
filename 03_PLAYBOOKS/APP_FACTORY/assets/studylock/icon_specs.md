# StudyLock - App Icon Specifications

## Primary Icon Concept

**Design:** Open book or graduation cap combined with timer/clock element and lock

**Visual Description:**
- Simplified open book silhouette at center
- Clock/timer element integrated (quarter-filled circle or clock hands)
- Small lock keyhole incorporated subtly
- Gradient background from deep indigo to vibrant indigo
- Clean, academic yet modern aesthetic

---

## Color Palette

| Element | Color | Hex Code |
|---------|-------|----------|
| Background Top | Vibrant Indigo | #6366F1 |
| Background Bottom | Deep Indigo | #4F46E5 |
| Book/Timer | White | #FFFFFF |
| Timer Progress | Success Green | #22C55E |
| Accent Shadow | Dark Indigo | #312E81 |
| Lock Element | Light Indigo | #A5B4FC |

---

## Style Guidelines

### Do
- Keep elements simple and recognizable at 60x60px
- Use clean geometric shapes for book/timer
- Make timer element visible but not dominant
- Test on light and dark backgrounds
- Convey "focus" and "study" at a glance

### Don't
- Use detailed book pages or text
- Add literal pencils, notebooks, or school supplies
- Make the lock too prominent (it's not a security app)
- Use childish or cartoonish elements
- Include graduation caps (too literal)

---

## Size Requirements

### iOS App Store
| Size | Dimensions | Usage |
|------|------------|-------|
| 1024x1024 | 1024 x 1024 px | App Store listing |
| 180x180 | 180 x 180 px | iPhone @3x |
| 120x120 | 120 x 120 px | iPhone @2x |
| 167x167 | 167 x 167 px | iPad Pro @2x |
| 152x152 | 152 x 152 px | iPad @2x |
| 76x76 | 76 x 76 px | iPad @1x |
| 60x60 | 60 x 60 px | iPhone @1x |

### Google Play Store
| Size | Dimensions | Usage |
|------|------------|-------|
| 512x512 | 512 x 512 px | Play Store listing |
| 192x192 | 192 x 192 px | xxxhdpi |
| 144x144 | 144 x 144 px | xxhdpi |
| 96x96 | 96 x 96 px | xhdpi |
| 72x72 | 72 x 72 px | hdpi |
| 48x48 | 48 x 48 px | mdpi |

---

## Icon Variants

### Primary (Default)
- Full color gradient background
- Book + timer elements
- Use for App Store, home screen

### Notification Icon (Android)
- White silhouette only
- Book + timer simplified
- Transparent background

### Dark Mode Alternative
- Lighter background gradient for dark home screens
- Test visibility against iOS dark mode wallpapers

---

## File Specifications

### Format
- **iOS:** PNG with no transparency, sRGB color profile
- **Android:** PNG with transparency for adaptive icons

### Naming Convention
```
studylock_icon_1024.png
studylock_icon_512.png
studylock_icon_180@3x.png
studylock_icon_120@2x.png
studylock_icon_notification.png (Android)
```

### Compression
- Optimize all PNGs
- Target: < 100KB for 1024x1024

---

## Generation Prompts

### For AI Image Generation (Gemini/Midjourney)

**Primary Icon:**
```
A minimal app icon design for iOS. Centered composition showing a simplified open book silhouette in white, with a circular timer element integrated into the design showing partial progress in green (#22C55E). Background gradient from deep indigo (#4F46E5) at bottom to vibrant indigo (#6366F1) at top. Clean, modern, academic aesthetic. Rounded square format for app store. No text, no fine details that disappear when small.
```

**Alternative Prompt:**
```
Minimalist study app icon. White book silhouette combined with Pomodoro timer circle. Indigo gradient background. Green progress indicator. Modern flat design. 1024x1024 iOS format.
```

---

## Quality Checklist

- [ ] Recognizable at 60x60px
- [ ] Works on light home screen backgrounds
- [ ] Works on dark home screen backgrounds
- [ ] Study/focus concept clear at a glance
- [ ] Timer element visible but not dominant
- [ ] Differentiates from generic timer apps
- [ ] Appeals to student demographic (18-25)
- [ ] Passes squint test
- [ ] Color palette consistent with app branding
- [ ] No childish or cartoonish elements
