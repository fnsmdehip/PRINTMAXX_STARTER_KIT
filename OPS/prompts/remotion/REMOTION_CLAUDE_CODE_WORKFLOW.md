# Remotion + Claude Code Video Production Workflow

**Source:** @Shpigford (Josh Pigford, Baremetrics founder) - Jan 24, 2026
**Validated by:** @DrewAutomates, @Remotion official

---

## Overview

Generate complete product demo videos entirely within Claude Code using the Remotion Agent Skills and ElevenLabs MCP integration. No video team required. No screen recording. The app literally renders itself.

**Stack:**
- Claude Code with Opus 4.5
- Remotion Agent Skills (`/remotion` skill)
- ElevenLabs API via MCP (voiceover)
- Existing codebase React components

**What Josh Built:**
- Full product demo video for Presscut
- Generated entirely within Claude Code
- Used existing React components from the app
- Added AI-generated voiceover via ElevenLabs
- Total time: ~1 hour of iteration

---

## Technical Setup

### 1. Install Remotion Agent Skills

```bash
npx skills add remotion-dev/skills
```

This adds the `/remotion` skill to Claude Code, enabling:
- Video composition generation
- Scene timing and transitions
- Text and graphics animation
- Audio synchronization
- Video rendering

### 2. Configure ElevenLabs MCP

Add to your Claude MCP config (`~/.claude/claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "elevenlabs": {
      "command": "npx",
      "args": ["-y", "@anthropic/mcp-server-elevenlabs"],
      "env": {
        "ELEVENLABS_API_KEY": "your-api-key-here"
      }
    }
  }
}
```

**Get API Key:** https://elevenlabs.io/app/settings/api-keys

**Voice Selection:**
- For product demos: Professional, clear voices (Rachel, Adam, Antoni)
- For casual content: Conversational voices (Josh, Bella)
- For tutorials: Calm, instructive voices (Elli, Sam)

### 3. Project Structure

Remotion expects this structure:

```
project/
├── remotion/
│   ├── index.ts              # Entry point
│   ├── Root.tsx              # Root composition
│   ├── Video.tsx             # Main video composition
│   └── components/
│       ├── scenes/           # Individual scene components
│       ├── transitions/      # Transition effects
│       └── ui/               # Reusable UI elements
├── public/
│   ├── music/                # Background audio
│   ├── voiceover/            # Generated VO clips
│   └── assets/               # Images, logos, icons
└── package.json
```

---

## The Shpigford Workflow

### Step 1: Start in Your Codebase

Open Claude Code in your product's codebase directory. This is critical because Claude can then:
- Read your existing React components
- Understand your app's UI patterns
- Replicate your design system
- Pull real data structures

### Step 2: Use the Discovery Prompt

Josh's actual prompt:

```
Create a demo video of the [APP_NAME] app/product using remotion. Use react components to replicate UI elements and replicate the UI of the app as closely as possible. The app has a LOT of features/functionality, so take guidance from the marketing home page/index for what to highlight, while keeping language simple and to-the-point.

Really grill me with questions to nail down exactly how the final video should look/feel and what content should be there.

The ultimate goal of this is to replicate what me, the founder, would be showing/doing with a product demo with a customer.
```

**Key elements:**
- References existing codebase
- Points to marketing page for priorities
- Asks Claude to ask questions (interactive refinement)
- Sets goal: founder demo quality

### Step 3: Let Claude Plan

Claude will generate:
1. **Scene breakdown** with exact timings
2. **Content outline** for each scene
3. **Visual elements** to include
4. **Transition styles** between scenes
5. **Questions** to clarify your vision

Answer Claude's questions thoroughly. This iteration is where the magic happens.

### Step 4: Generate Video Code

Claude generates:
- Complete Remotion composition
- Scene components using your existing React components
- Animation and transition code
- Timing synchronization

**No new art assets needed** - Claude uses what's already in your codebase.

### Step 5: Add Voiceover (ElevenLabs)

Josh's insight on voice timing:

> "what's great is claude already knew the exact length of each scene and could customize the text for elevenlabs to generate. there's no way to do 'timing' with the voice generation so you have to generate separate audio clips and then have claude line them up for you (which works really well)."

**Workflow:**
1. Claude knows scene durations (e.g., Scene 1 = 5.2 seconds)
2. Claude writes VO script for each scene matching duration
3. Claude generates separate audio clips via ElevenLabs MCP
4. Claude places clips at correct timestamps in composition

**Example prompt for VO:**
```
Now add professional voiceover using ElevenLabs. Generate separate audio clips for each scene, keeping each clip within the scene duration. Use the "Rachel" voice for a professional product demo feel.
```

### Step 6: Render and Export

```bash
npx remotion render src/index.ts Main out/demo.mp4
```

Or use the Remotion Studio for preview:
```bash
npx remotion studio
```

---

## PRINTMAXX Integration

### Existing Infrastructure

We already have:
- `OPS/prompts/remotion/REMOTION_MASTER_PROMPT.md` - Full prompts for different video styles
- `OPS/prompts/remotion/REMOTION_VIDEO_PROMPT.md` - Technical animation guidelines
- `OPS/prompts/remotion/SOUND_DESIGN_GUIDE.md` - Audio selection by niche
- `OPS/prompts/remotion/TIKTOK_MUSIC_TRENDS.md` - Current trending sounds
- `/remotion-video` skill configured

### Enhancement: Add ElevenLabs MCP

**Setup:**
1. Get ElevenLabs API key (free tier: 10K chars/month)
2. Add to MCP config as shown above
3. Test with simple generation

**Cost estimates:**
- Free tier: 10,000 characters/month
- Starter ($5/mo): 30,000 characters
- Creator ($22/mo): 100,000 characters
- ~1000 characters = 1 minute of audio

### Use Cases for PRINTMAXX Apps

| App | Video Type | Duration | VO Needed |
|-----|------------|----------|-----------|
| PrayerLock | App demo | 30-45s | Yes - calm, reverent |
| WalkToUnlock | Feature showcase | 15-30s | Yes - energetic |
| StudyLock | Tutorial | 45-60s | Yes - instructive |
| biomaxx | Product demo | 30-45s | Yes - scientific |

### Prompt Templates by App Type

**Faith App (PrayerLock):**
```
Create a demo video of PrayerLock using remotion. The video should feel peaceful and reverent, not salesy. Highlight:
1. The lock screen prayer prompt
2. Simple unlock after prayer time
3. Prayer streak tracking
4. Community prayer wall

Use soft transitions, warm gold/navy colors, and worship-adjacent background music. Duration: 30-45 seconds. Add professional voiceover using ElevenLabs with a calm, warm voice (Elli or Adam).
```

**Fitness App (WalkToUnlock):**
```
Create an energetic demo video of WalkToUnlock using remotion. Show:
1. Phone locked until steps hit
2. Real-time step counter
3. Achievement unlocks
4. Friend challenges

Use fast cuts, green/blue gradients, and Brazilian phonk-style energy. Duration: 15-30 seconds. Add voiceover using ElevenLabs with an energetic, motivating voice (Josh or Antoni).
```

**Productivity App (StudyLock):**
```
Create a tutorial-style demo of StudyLock using remotion. Walk through:
1. Setting study goals
2. App blocking activation
3. Focus session countdown
4. Progress tracking

Use clean transitions, purple/dark theme, and lo-fi background. Duration: 45-60 seconds. Add instructive voiceover using ElevenLabs with a clear, calm voice (Rachel or Sam).
```

---

## Video Templates to Create

### 1. App Demo Template

**Purpose:** Product Hunt launches, App Store preview
**Duration:** 30-45 seconds
**Structure:**
- 0-5s: Hook + logo animation
- 5-15s: Problem statement
- 15-35s: Feature showcase (3-4 features)
- 35-45s: CTA + app store badges

### 2. Feature Announcement Template

**Purpose:** Twitter/TikTok feature drops
**Duration:** 15-20 seconds
**Structure:**
- 0-3s: "NEW:" hook
- 3-15s: Feature demo
- 15-20s: "Update now" CTA

### 3. Testimonial Video Template

**Purpose:** Social proof, ads
**Duration:** 30-60 seconds
**Structure:**
- 0-5s: Quote hook
- 5-25s: User story + app footage
- 25-55s: Results/benefits
- 55-60s: CTA

### 4. Tutorial Video Template

**Purpose:** Onboarding, support
**Duration:** 60-90 seconds
**Structure:**
- 0-10s: "How to [action]"
- 10-70s: Step-by-step walkthrough
- 70-90s: Summary + next steps

### 5. Social Proof Compilation Template

**Purpose:** Trust building, ads
**Duration:** 30-45 seconds
**Structure:**
- Rapid-fire testimonial snippets (3-5 seconds each)
- Interspersed with app footage
- Counter animations (downloads, ratings)
- CTA

---

## ElevenLabs Voice Guide

### Voice Selection by Niche

| Niche | Recommended Voice | Backup Voice | Characteristics |
|-------|-------------------|--------------|-----------------|
| Faith/Prayer | Elli | Adam | Calm, warm, reverent |
| Fitness/Gym | Josh | Antoni | Energetic, motivating |
| Women's Wellness | Rachel | Bella | Empowering, professional |
| Biohacking/Tech | Adam | Sam | Scientific, clear |
| Productivity | Rachel | Elli | Instructive, calm |
| Finance/Crypto | Adam | Josh | Confident, authoritative |

### Script Writing for VO

**Timing rules:**
- Average speaking rate: 150 words/minute
- 5-second scene = ~12-15 words
- 10-second scene = ~25 words
- Leave 0.5s buffer at scene boundaries

**Example script breakdown:**
```
Scene 1 (5s): "Tired of mindless scrolling? PrayerLock changes that." (8 words)
Scene 2 (8s): "Set your prayer time. Your phone stays locked until you've prayed." (12 words)
Scene 3 (10s): "Track your prayer streak. Connect with a community of believers." (10 words)
Scene 4 (7s): "Download PrayerLock. Transform your phone time into prayer time." (9 words)
```

### MCP Commands

**Generate single VO clip:**
```
Generate voiceover audio for: "[SCRIPT TEXT]" using the [VOICE_NAME] voice. Save to public/voiceover/scene_1.mp3
```

**Generate all clips:**
```
Generate voiceover clips for each scene using the Rachel voice:
Scene 1 (5s): "[TEXT]"
Scene 2 (8s): "[TEXT]"
Scene 3 (10s): "[TEXT]"
Scene 4 (7s): "[TEXT]"

Save each to public/voiceover/scene_[N].mp3
```

---

## Advanced Techniques

### 1. Pull Data via MCP

Like @DrewAutomates: Connect Supabase MCP to pull real product data:
- User counts
- Feature lists
- Pricing
- Testimonials

The video renders with live data, not hardcoded.

### 2. A/B Test Video Variants

Generate multiple versions with different:
- Hook lines
- Feature order
- CTA copy
- Voice selection

Test on TikTok to find winners.

### 3. Localization

Generate VO in multiple languages via ElevenLabs:
- Spanish, French, German, Japanese
- Same video structure, different audio
- Expand to international markets

### 4. Batch Generation

For 10 apps, generate all demo videos in one session:
```
Generate demo videos for each app in my portfolio:
1. PrayerLock - faith niche, 30s
2. WalkToUnlock - fitness niche, 20s
3. StudyLock - productivity niche, 45s
...

Use the appropriate niche prompt template for each.
```

---

## Workflow Checklist

Before starting video generation:

- [ ] Claude Code open in product codebase
- [ ] Remotion skills installed (`npx skills add remotion-dev/skills`)
- [ ] ElevenLabs MCP configured with API key
- [ ] Marketing page/feature list available for reference
- [ ] Color scheme and design tokens accessible
- [ ] Background music selected (royalty-free)
- [ ] Voice selection decided based on niche

During generation:

- [ ] Answer all Claude's clarifying questions
- [ ] Review scene breakdown before code generation
- [ ] Test each scene in Remotion Studio
- [ ] Generate and review VO clips
- [ ] Verify audio timing with scene durations
- [ ] Add music with proper ducking

After generation:

- [ ] Render full video
- [ ] Review for quality issues
- [ ] Export in required formats (MP4, vertical, horizontal)
- [ ] Create thumbnail from key frame
- [ ] Upload to appropriate platforms

---

## Troubleshooting

### "Voice doesn't match scene duration"

ElevenLabs generates audio at speaking rate, not exact duration. Solutions:
1. Adjust script word count
2. Use Claude to add/remove silence
3. Adjust scene duration to match audio

### "React components not rendering"

Ensure your components are:
1. Pure React (no Next.js server components)
2. Don't rely on browser APIs unavailable in Node
3. Export as default or named exports

### "Video renders black"

Check:
1. AbsoluteFill backgrounds are set
2. Assets paths are correct (use `staticFile()`)
3. Compositions have correct width/height

### "Audio sync issues"

- Generate shorter VO clips
- Add 0.3s buffer between clips
- Use `startFrom` prop precisely

---

## Cost Analysis

**For 10 app demo videos (30s each):**

| Item | Cost |
|------|------|
| Claude Code | $0 (included in Max subscription) |
| Remotion | $0 (open source) |
| ElevenLabs (5000 chars) | $0 (free tier) |
| Background music | $0 (royalty-free) |
| **Total** | **$0** |

**Compare to traditional:**
- Video team: $500-2000 per video
- Freelancer: $100-500 per video
- This workflow: $0

---

## Related Files

- `REMOTION_MASTER_PROMPT.md` - Niche-specific video prompts
- `REMOTION_VIDEO_PROMPT.md` - Technical animation guidelines
- `SOUND_DESIGN_GUIDE.md` - Audio selection by niche
- `TIKTOK_MUSIC_TRENDS.md` - Current trending sounds
- `APP_LAUNCH_VIDEO_SPECS.md` - Launch video specifications

---

## Sources

- @Shpigford: https://x.com/Shpigford (Jan 24, 2026 thread)
- @DrewAutomates: https://x.com/DrewAutomates (Claude + Remotion + Supabase workflow)
- @Remotion: https://x.com/Remotion (Official Agent Skills announcement)
- Remotion Docs: https://www.remotion.dev/docs
- ElevenLabs API: https://elevenlabs.io/docs

---

*Last Updated: January 26, 2026*
