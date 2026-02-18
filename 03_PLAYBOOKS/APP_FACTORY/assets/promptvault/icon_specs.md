# PromptVault - App Icon Specifications

## Primary Icon Concept

**Design:** Vault or safe door combined with document/prompt symbol

**Visual Description:**
- Circular vault door shape as base
- Document or text snippet icon at center
- Sparkle or AI glow accent
- Gradient background from deep purple to violet
- Modern, tech-forward aesthetic

---

## Color Palette

| Element | Color | Hex Code |
|---------|-------|----------|
| Background Top | Violet | #8B5CF6 |
| Background Bottom | Deep Purple | #1E1B4B |
| Vault/Document | White | #FFFFFF |
| AI Sparkle | Gold | #EAB308 |
| Accent Glow | Light Purple | #C4B5FD at 50% opacity |

---

## Style Guidelines

### Do
- Keep vault/document concept simple and iconic
- Use modern gradients (purple to violet)
- Include subtle AI sparkle to suggest intelligence
- Make it recognizable at small sizes
- Test on both light and dark backgrounds

### Don't
- Make vault look like a safe/security app
- Include literal text or letters
- Use complex vault mechanics (dial, handle)
- Make the AI element too dominant
- Use dated skeuomorphic designs

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

### Web (if applicable)
| Size | Dimensions | Usage |
|------|------------|-------|
| 512x512 | 512 x 512 px | PWA icon |
| 192x192 | 192 x 192 px | Touch icon |
| 32x32 | 32 x 32 px | Favicon |
| 16x16 | 16 x 16 px | Favicon small |

---

## Icon Variants

### Primary (Default)
- Full gradient background
- Vault + document + sparkle
- Use for App Store, home screen

### Notification Icon (Android)
- White silhouette only
- Document/prompt shape
- Transparent background

### Favicon (Web)
- Simplified: just document with sparkle
- Works at 16x16px
- No gradient (solid purple background)

---

## File Specifications

### Format
- **iOS:** PNG with no transparency, sRGB
- **Android:** PNG with transparency
- **Web:** PNG and ICO

### Naming Convention
```
promptvault_icon_1024.png
promptvault_icon_512.png
promptvault_icon_180@3x.png
promptvault_icon_120@2x.png
promptvault_icon_notification.png
promptvault_favicon.ico
```

### Compression
- Optimize all PNGs
- Target: < 100KB for 1024x1024

---

## Generation Prompts

### For AI Image Generation (Gemini/Midjourney)

**Primary Icon:**
```
A minimal app icon design for iOS. Centered composition showing a stylized vault or safe door shape in white, with a document/text snippet symbol at center. Small gold sparkle accents suggesting AI. Background gradient from deep purple (#1E1B4B) at bottom to violet (#8B5CF6) at top. Modern flat design with subtle depth. Rounded square format for app store. Tech-forward, professional aesthetic.
```

**Alternative Prompt:**
```
Minimalist AI tool app icon. White document icon with subtle vault door circular frame. Purple-to-violet gradient background. Gold sparkle accent. Modern flat design. No text. 1024x1024 iOS format.
```

---

## Quality Checklist

- [ ] Recognizable at 60x60px
- [ ] Works on light home screen backgrounds
- [ ] Works on dark home screen backgrounds
- [ ] Vault/document concept clear at a glance
- [ ] Differentiates from notes apps and password managers
- [ ] Suggests AI/prompts without being literal
- [ ] Appeals to tech-savvy demographic
- [ ] Passes squint test
- [ ] Color palette consistent with app branding
- [ ] Gold sparkle visible but subtle
