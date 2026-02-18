# PRD: App Icon Generation System

## Introduction

Generate professional 3D app icons for all PRINTMAXX apps using AI image generation tools. Icons must follow brand guidelines and be 1024x1024 PNG format for App Store submission.

## Alpha Stack Reference

**Best Icon Generation Tool (per ALPHA057):** ChatGPT/DALL-E generates 1024x1024 PNG icons directly usable for iOS. Better than Gemini API for icons.

**Icon Quality Requirements (per ASSET_GENERATION_GUIDE.md):**
- Must have depth/dimension (3D, isometric, or layered)
- Use gradients (not flat colors)
- Include relevant symbol/icon (not just a letter)
- Add glow, reflection, or particle effects
- Generate at 1024x1024, then resize

**Reference Files:**
- `MONEY_METHODS/APP_FACTORY/ASSET_GENERATION_GUIDE.md` - Full guide
- `MONEY_METHODS/APP_FACTORY/builds/ICON_GENERATION_PROMPTS.md` - Ready prompts
- `.claude/CLAUDE.md` → Gemini API & Image Generation section

## Goals

- Generate premium 3D icons for all 10 SDK 54 apps
- Icons match app niche/branding (faith=warm gold, fitness=energetic green, etc.)
- All icons are 1024x1024 PNG format
- Icons are saved to correct assets folder per app

## Apps Needing Icons

Based on QA report (SDK54_QA_REPORT.md):
1. DailyAnchor (faith) - `builds/dailyanchor-sdk54/assets/icon.png`
2. DevotionFlow (faith) - `builds/devotionflow-sdk54/assets/images/icon.png`
3. FocusPrayer (faith) - `builds/focusprayer-sdk54/assets/icon.png`
4. GlowMaxx (women's skincare) - `builds/glowmaxx-sdk54/assets/icon.png`
5. LearnLock (education) - `builds/learnlock-sdk54/assets/icon.png`
6. PromptVault (AI/productivity) - `builds/promptvault-sdk54/assets/icon.png`

## User Stories

### US-001: Create DailyAnchor Icon
**Description:** As a developer, I need a 3D app icon for DailyAnchor (faith/devotional app).

**Acceptance Criteria:**
- [ ] Icon features golden anchor symbol with glowing light
- [ ] Background is deep ocean blue to navy gradient (#1E3A5F to #0A1929)
- [ ] Icon is 1024x1024 PNG
- [ ] Icon saved to `builds/dailyanchor-sdk54/assets/icon.png`
- [ ] Also create splash.png with same branding

### US-002: Create DevotionFlow Icon
**Description:** As a developer, I need a 3D app icon for DevotionFlow (daily devotional app).

**Acceptance Criteria:**
- [ ] Icon features flowing water/river with subtle cross/dove
- [ ] Colors: warm cream to gold (#F5F0E8 to #E8D5B7) on burgundy (#722F37)
- [ ] Icon is 1024x1024 PNG
- [ ] Icon saved to `builds/devotionflow-sdk54/assets/images/icon.png`

### US-003: Create FocusPrayer Icon
**Description:** As a developer, I need a 3D app icon for FocusPrayer (prayer focus app).

**Acceptance Criteria:**
- [ ] Icon features praying hands with focus/target ring element
- [ ] Background is slate blue to deep indigo (#4A5568 to #2D3748)
- [ ] Icon is 1024x1024 PNG
- [ ] Icon saved to `builds/focusprayer-sdk54/assets/icon.png`

### US-004: Create GlowMaxx Icon
**Description:** As a developer, I need a 3D app icon for GlowMaxx (women's skincare app).

**Acceptance Criteria:**
- [ ] Icon features glowing face silhouette or sparkle burst
- [ ] Colors: coral pink to rose gold (#FF6B9D to #FFB6C1)
- [ ] Add subtle sparkle/shimmer effects
- [ ] Icon is 1024x1024 PNG
- [ ] Icon saved to `builds/glowmaxx-sdk54/assets/icon.png`

### US-005: Create LearnLock Icon
**Description:** As a developer, I need a 3D app icon for LearnLock (education screen lock app).

**Acceptance Criteria:**
- [ ] Icon features padlock integrated with book/graduation cap
- [ ] Colors: indigo to purple gradient (#4F46E5 to #7C3AED)
- [ ] Lock appears partially open (unlocking through learning)
- [ ] Icon is 1024x1024 PNG
- [ ] Icon saved to `builds/learnlock-sdk54/assets/icon.png`

### US-006: Create PromptVault Icon
**Description:** As a developer, I need a 3D app icon for PromptVault (AI prompt library).

**Acceptance Criteria:**
- [ ] Icon features vault door with AI/chat bubble elements
- [ ] Colors: electric cyan to purple (#00D9FF to #7C3AED) on dark (#1a1a2e)
- [ ] Add subtle circuit board patterns or digital glow
- [ ] Icon is 1024x1024 PNG
- [ ] Icon saved to `builds/promptvault-sdk54/assets/icon.png`

## Technical Considerations

**Generation Methods:**
1. **ChatGPT DALL-E (Preferred):** Navigate to chatgpt.com, paste prompt, download PNG
2. **Gemini AI Studio (Backup):** aistudio.google.com browser UI
3. **Manual prompt file:** `builds/ICON_GENERATION_PROMPTS.md` has ready prompts

**Directory Setup:**
```bash
# Create missing assets directories
mkdir -p builds/dailyanchor-sdk54/assets
mkdir -p builds/focusprayer-sdk54/assets
```

## Success Metrics

- All 6 apps have proper 3D icons (not placeholder letters)
- Icons are >100KB (indicates proper quality, not placeholder)
- Icons render well at small sizes (rounded corners)
- Apps can be submitted to App Store

## Open Questions

- Should we generate multiple variants per app for A/B testing?
- Do we need dark mode icon variants?
