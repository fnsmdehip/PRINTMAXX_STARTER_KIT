# PrayerLock - App Icon Specifications

## Primary Icon Concept

**Design:** Hands clasped in prayer with a subtle lock element integrated

**Visual Description:**
- Simplified hands in prayer position (side view silhouette)
- Small lock icon embedded at the base of hands
- Soft golden glow emanating from above the hands
- Clean, minimal style with no fine details
- Gradient background from deep navy to soft gold at top

---

## Color Palette

| Element | Color | Hex Code |
|---------|-------|----------|
| Background Top | Soft Gold | #D4AF37 |
| Background Bottom | Deep Navy | #1a1a2e |
| Hands | Off-White | #F5F5F5 |
| Hands Shadow | Light Gold | #C4A030 |
| Lock Element | White | #FFFFFF |
| Glow Effect | Warm Gold | #FFD700 at 30% opacity |

---

## Style Guidelines

### Do
- Keep silhouette simple and recognizable at 60x60px
- Use soft gradients, not harsh color transitions
- Maintain strong contrast between hands and background
- Round all corners generously (iOS default)
- Test visibility on both light and dark home screens

### Don't
- Include text or letters in the icon
- Use detailed realistic hand illustrations
- Add multiple competing elements
- Use thin lines that disappear when small
- Include religious symbols that could limit audience (no crosses)

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
- Use for App Store, home screen, most contexts

### Notification Icon (Android)
- Single color silhouette only
- White (#FFFFFF) hands on transparent background
- No background gradient
- Required for Android push notifications

### Spotlight/Search (iOS)
- Same as primary but optimized for smaller display
- May simplify lock element if not visible at small sizes

---

## File Specifications

### Format
- **iOS:** PNG with no transparency, sRGB color profile
- **Android:** PNG with transparency for adaptive icons

### Naming Convention
```
prayerlock_icon_1024.png
prayerlock_icon_512.png
prayerlock_icon_180@3x.png
prayerlock_icon_120@2x.png
prayerlock_icon_notification.png (Android)
```

### Compression
- Optimize all PNGs (TinyPNG or similar)
- Target: < 100KB for 1024x1024

---

## Generation Prompts

### For AI Image Generation (Gemini/Midjourney)

**Primary Icon:**
```
A minimal app icon design for iOS. Centered composition showing simplified hands clasped in prayer position, side view silhouette in off-white color. Small lock icon integrated at the base of hands. Background gradient from deep navy blue (#1a1a2e) at bottom to soft gold (#D4AF37) at top. Soft golden glow emanating from above hands. Clean flat design with subtle shadows. Rounded square format for app store. Professional, calming, spiritual aesthetic. No text, no crosses, no fine details.
```

**Alternative Style:**
```
Minimalist app icon. Praying hands silhouette, white on navy-to-gold gradient background. Modern flat design. Lock symbol subtly incorporated. Peaceful, professional. 1024x1024 iOS app icon format.
```

---

## Quality Checklist

- [ ] Recognizable at 60x60px (smallest home screen size)
- [ ] Works on light home screen backgrounds
- [ ] Works on dark home screen backgrounds
- [ ] No fine details that disappear when scaled down
- [ ] Unique enough to not confuse with other apps
- [ ] Matches app's peaceful, faith-focused personality
- [ ] Does not look like existing prayer/faith apps
- [ ] Passes squint test (blur eyes, still recognizable)
- [ ] Lock element visible but not dominant
- [ ] Color palette consistent with app branding
