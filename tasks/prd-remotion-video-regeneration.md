# PRD: Remotion Video Regeneration

## Introduction

Regenerate all PRINTMAXX app marketing videos using proper branded icons and royalty-free music. Current videos are basic and missing music/proper branding.

## Alpha Stack Reference

**Remotion Master Prompts:** `OPS/prompts/remotion/REMOTION_MASTER_PROMPT.md`
- Prompt #4: Faith/Devotional (warm, peaceful, gold/amber)
- Prompt #5: Fitness/Health (energetic, vibrant greens/blues)
- Prompt #6: Women's Wellness (soft, empowering, pink/purple)
- Prompt #7: Biohacking/Longevity (scientific, premium, emerald/dark)

**Music Sources (Royalty-Free):**
- Pixabay: pixabay.com/music (phonk, ambient)
- Uppbeat: uppbeat.io (high quality)
- Tunetank: tunetank.com (phonk, EDM)
- FreeToUse: freetouse.com/music

**Video Plan:** `LANDING/printmaxx-site/src/remotion/VIDEO_REGENERATION_PLAN.md`

**Existing Icons:** `LANDING/printmaxx-site/public/icons/` (9 high-quality 3D icons)

**Reference Files:**
- `.claude/CLAUDE.md` → Remotion Video Production section
- `OPS/prompts/remotion/TIKTOK_MUSIC_TRENDS.md` - Music research

## Goals

- Regenerate videos with proper 3D branded icons (not generic letters)
- Add royalty-free music (phonk for energetic, ambient for faith)
- Use correct Remotion prompt template per app niche
- Output professional TikTok/Reels-ready videos (1080x1920)
- Videos stored in `LANDING/printmaxx-site/out/` and `builds/{app}/marketing/videos/`

## App-to-Template Mapping

| App | Niche | Prompt Template | Music Style |
|-----|-------|-----------------|-------------|
| BioMaxx | Biohacking | #7 | Ambient/Tech |
| GlowMaxx | Women's Wellness | #6 | Soft Pop |
| PrayerLock | Faith | #4 | Peaceful Ambient |
| StepUnlock | Fitness | #5 | Energetic Phonk |
| DevotionFlow | Faith | #4 | Peaceful Ambient |
| DailyAnchor | Faith | #4 | Peaceful Ambient |
| FocusPrayer | Faith | #4 | Peaceful Ambient |
| PelvicPro | Women's Health | #6 | Soft Ambient |
| LearnLock | Education | #2 (generic) | Upbeat |
| PromptVault | AI/Tech | #7 | Tech/Synth |

## User Stories

### US-001: Download Royalty-Free Music
**Description:** As a developer, I need royalty-free music files for video production.

**Acceptance Criteria:**
- [ ] Download phonk track from Pixabay to `public/music/phonk-energetic.mp3`
- [ ] Download ambient track from Pixabay to `public/music/ambient-peaceful.mp3`
- [ ] Download soft pop track to `public/music/soft-empowering.mp3`
- [ ] All tracks are royalty-free (no attribution required)
- [ ] Tracks are 60-90 seconds minimum

### US-002: Create BioMaxx Premium Video
**Description:** As a marketer, I need a premium biohacking video for BioMaxx.

**Acceptance Criteria:**
- [ ] Uses Prompt #7 (biohacking/scientific template)
- [ ] Features proper BioMaxx 3D icon from `public/icons/biomaxx-icon.png`
- [ ] Includes ambient/tech music track
- [ ] Duration: 10-15 seconds
- [ ] Resolution: 1080x1920 (vertical TikTok format)
- [ ] Output to `out/biomaxx-promo-v2.mp4`
- [ ] Typecheck passes

### US-003: Create Faith Apps Video Bundle
**Description:** As a marketer, I need videos for all faith apps (PrayerLock, DevotionFlow, DailyAnchor, FocusPrayer).

**Acceptance Criteria:**
- [ ] All use Prompt #4 (faith/devotional template)
- [ ] Features proper app icons
- [ ] Includes peaceful ambient music
- [ ] Duration: 10-15 seconds each
- [ ] Output to `out/{app}-promo-v2.mp4`
- [ ] Typecheck passes

### US-004: Create Fitness/Wellness Video Bundle
**Description:** As a marketer, I need videos for fitness/wellness apps (StepUnlock, GlowMaxx, PelvicPro).

**Acceptance Criteria:**
- [ ] StepUnlock uses Prompt #5 (fitness, energetic)
- [ ] GlowMaxx uses Prompt #6 (women's wellness)
- [ ] PelvicPro uses Prompt #6 (women's health)
- [ ] Features proper app icons
- [ ] Music matches energy level
- [ ] Output to `out/{app}-promo-v2.mp4`
- [ ] Typecheck passes

### US-005: Copy Videos to App Marketing Folders
**Description:** As a developer, I need videos in each app's marketing folder.

**Acceptance Criteria:**
- [ ] Copy each video to `builds/{app}/marketing/videos/`
- [ ] Create marketing folder if doesn't exist
- [ ] Videos named consistently: `{app}-promo.mp4`

## Technical Considerations

**Remotion Project Location:** `LANDING/printmaxx-site/`

**Render Command:**
```bash
cd LANDING/printmaxx-site
npx remotion render src/remotion/index.ts CompositionName out/video.mp4
```

**Music Import:**
```tsx
import { Audio, staticFile } from 'remotion';
<Audio src={staticFile('music/ambient-peaceful.mp3')} volume={0.3} />
```

## Non-Goals

- No full 45-55 second production videos (those are for later)
- No custom sound effects (just music)
- No AI-generated voiceover (keep text-only for now)

## Success Metrics

- All 10 apps have professional promo videos
- Videos include proper icons (not letters)
- Videos include royalty-free music
- Videos are TikTok/Reels ready (vertical 1080x1920)
- Videos render without errors
