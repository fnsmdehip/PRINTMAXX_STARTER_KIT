# WalkToUnlock - App Icon Specifications

## Primary Icon Concept

**Design:** Footstep or shoe print with circular progress ring and subtle lock element

**Visual Description:**
- Stylized footstep/shoe print silhouette at center
- Circular progress ring around the footstep (70% filled)
- Small lock icon or keyhole integrated into design
- Motion lines suggesting movement
- Gradient background from dark teal to vibrant teal

---

## Color Palette

| Element | Color | Hex Code |
|---------|-------|----------|
| Background Top | Vibrant Teal | #0D9488 |
| Background Bottom | Dark Teal | #134E4A |
| Footstep | White | #FFFFFF |
| Progress Ring Filled | Green | #22C55E |
| Progress Ring Empty | Muted Teal | #1F3D3A |
| Motion Lines | Light Teal | #5EEAD4 at 60% opacity |

---

## Style Guidelines

### Do
- Keep footstep silhouette simple and recognizable at small sizes
- Use clean, energetic aesthetic that suggests movement
- Make progress ring visible but not dominant
- Test visibility on light and dark home screens
- Ensure green progress section contrasts well

### Don't
- Use realistic shoe details
- Add text or numbers in the icon
- Make the lock element too prominent
- Use thin lines that disappear when scaled down
- Include arrows or other complex directional elements

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
- Complete progress ring visible
- Use for App Store, home screen

### Notification Icon (Android)
- White footstep silhouette only
- Transparent background
- No progress ring or lock
- Required for Android notifications

### Alternative (Activity Ring Focus)
- Progress ring more prominent
- Footstep smaller, centered
- For contexts emphasizing fitness tracking

---

## File Specifications

### Format
- **iOS:** PNG with no transparency, sRGB color profile
- **Android:** PNG with transparency for adaptive icons

### Naming Convention
```
walktounlock_icon_1024.png
walktounlock_icon_512.png
walktounlock_icon_180@3x.png
walktounlock_icon_120@2x.png
walktounlock_icon_notification.png (Android)
```

### Compression
- Optimize all PNGs
- Target: < 100KB for 1024x1024

---

## Generation Prompts

### For AI Image Generation (Gemini/Midjourney)

**Primary Icon:**
```
A minimal app icon design for iOS. Centered composition showing a white stylized footstep or shoe print silhouette. Circular progress ring around the footstep, 70% filled in green (#22C55E), remaining portion in muted teal (#1F3D3A). Background gradient from dark teal (#134E4A) at bottom to vibrant teal (#0D9488) at top. Subtle motion lines suggesting movement. Clean flat design. Rounded square format for app store. Energetic fitness aesthetic.
```

**Alternative Prompt:**
```
Minimalist fitness app icon. Running shoe footprint in white, surrounded by activity ring progress indicator. Teal gradient background. Green progress fill. Modern flat design. 1024x1024 iOS app icon format.
```

---

## Quality Checklist

- [ ] Recognizable at 60x60px
- [ ] Works on light home screen backgrounds
- [ ] Works on dark home screen backgrounds
- [ ] Footstep silhouette clearly visible
- [ ] Progress ring readable but not overwhelming
- [ ] Unique enough to not confuse with other fitness apps
- [ ] Conveys movement/activity at a glance
- [ ] Passes squint test (blur eyes, still recognizable)
- [ ] Color palette consistent with app branding
- [ ] Green progress element visible at all sizes
