# Shared Toolstack: 3 AI Personas on $40/mo

**Purpose:** How to run 3 complete AI personas (Findom + Faith + Fitness) on a single $40/mo tool subscription.
**Created:** 2026-01-27

---

## Tool Stack Overview

| Tool | Monthly Cost | What It Does | Shared Across |
|------|-------------|--------------|---------------|
| Leonardo.ai | $12/mo (Apprentice) | AI image generation, character consistency | All 3 personas |
| ElevenLabs | $22/mo (Starter) | Voice synthesis, 3 voice profiles | All 3 personas |
| D-ID | $6/mo (Lite) | Talking head video from image + audio | All 3 personas |
| **Total** | **$40/mo** | | |

**Upgrade path:** When combined revenue hits $500/mo, upgrade D-ID to HeyGen ($24/mo) for better lip sync and more video minutes. New total: $58/mo.

---

## Leonardo.ai: Character Consistency for 3 Personas

### How to Maintain 3 Distinct Characters

**The problem:** AI image generators create different faces every time. You need the SAME face across hundreds of images per persona.

**The solution:** Seed locking + style reference + consistent prompting.

### Step 1: Generate Base Character (Do Once Per Persona)

For each persona, generate 20-30 images. Pick the best one that matches the character profile. Record:

| Persona | Seed Number | Model | Guidance | Resolution |
|---------|------------|-------|----------|------------|
| Findom (Luxury) | [record] | Phoenix | 7.5 | 1024x1024 |
| Grace (Faith) | [record] | Phoenix | 7.5 | 1024x1024 |
| Coach Max (Fitness) | [record] | Phoenix | 7.5 | 1024x1024 |

### Step 2: Lock the Seed

Once you find the perfect face:
1. Note the exact seed number from Leonardo.ai generation details
2. Use this seed number for ALL future generations of that persona
3. Keep the same model, guidance scale, and base prompt prefix
4. Only change: setting description, clothing, pose

### Step 3: Style Reference Images

Upload 3-5 of your best generations as "Image Reference" for future generations:
- Use Image2Image with 0.3-0.4 strength (keeps face, changes scene)
- Or use Character Reference feature (Leonardo Phoenix supports this)
- Save reference images in the asset folder for each persona

### Step 4: Prompt Engineering for Consistency

**Every prompt follows this structure:**
```
[Character base prefix] + [Setting/scene description] + [Clothing for this scene] + [Expression/pose] + [Lighting/camera]
```

**Character base prefixes are locked per persona** (see individual persona docs).

The base prefix contains: physical description, skin tone, hair, build, age appearance.
The scene changes, but the person stays the same.

### Monthly Quota Management

**Leonardo.ai Apprentice plan: 8,500 tokens/month**

Estimated usage per persona per month:
- 30 images for daily posts: ~3,000 tokens
- 5 video thumbnails: ~500 tokens
- 5 story/extra images: ~500 tokens
- Total per persona: ~4,000 tokens

**3 personas: ~12,000 tokens/month**

This exceeds the 8,500 limit. Solutions:
1. **Batch generation sessions** - Generate 2 weeks of content in one session for each persona
2. **Upscale selectively** - Only upscale hero images (saves tokens)
3. **Reuse settings** - Same image can work for multiple similar posts
4. **Upgrade if needed** - Artisan plan ($24/mo) gives 25,000 tokens

**Recommended approach:** Generate content in 2-week batches. Week 1: Generate all 3 personas. Week 3: Generate next batch. This gives buffer.

If consistently hitting limits, upgrade to Artisan ($24/mo). New total: $52/mo. Still ROI-positive at $200+/mo revenue.

---

## ElevenLabs: 3 Voice Profiles from 1 Account

### Account Setup

**ElevenLabs Starter plan: $22/mo**
- 30,000 characters/month (roughly 30 minutes of audio)
- Up to 10 custom voices
- We need 3 voices. Plenty of room.

### Voice Profile Configuration

**Voice 1: Findom Persona**
- Base voice: "Bella" or custom clone
- Stability: 0.50 (more expressive)
- Similarity Boost: 0.80
- Style: 0.60 (more dramatic)
- Tone: Commanding, elegant, measured
- Use for: LoyalFans content, X video captions, IG Reels

**Voice 2: Grace (Faith)**
- Base voice: "Rachel" or custom clone
- Stability: 0.65 (calm, steady)
- Similarity Boost: 0.75
- Style: 0.40 (gentle, natural)
- Tone: Warm, calm, comforting
- Use for: Devotional videos, prayer audio, TikTok narration

**Voice 3: Coach Max (Fitness)**
- Base voice: "Josh" or "Adam" or custom clone
- Stability: 0.55 (energetic variation)
- Similarity Boost: 0.80
- Style: 0.50 (confident, coaching)
- Tone: Energetic, clear, motivational
- Use for: Workout instruction videos, supplement reviews, TikTok content

### Monthly Audio Budget

**30,000 characters = approximately 30 minutes total**

Allocation per persona:
| Persona | Minutes/mo | Content Type |
|---------|-----------|--------------|
| Findom | 8 min | 4 videos (2 min each) |
| Grace | 12 min | 6 devotional videos (2 min each) |
| Coach Max | 10 min | 5 workout/tip videos (2 min each) |
| **Total** | **30 min** | **15 videos/month** |

**Optimization tips:**
- Write scripts BEFORE generating audio (don't waste characters on retakes)
- Keep videos 30-60 seconds when possible (stretches the budget)
- Use text-on-screen for TikTok where voice isn't needed
- Save character budget for videos where voice is critical (devotionals, coaching)

**If hitting limits:** Upgrade to Creator plan ($99/mo) for 100 min. Do this when revenue exceeds $500/mo combined.

### Voice Cloning (Advanced, Month 2+)

For ultimate consistency:
1. Record 3-5 minutes of sample audio per persona (use a voice actor from Fiverr, $20-50)
2. Upload to ElevenLabs Instant Voice Clone
3. This locks the voice permanently - no drift between sessions
4. Better than stock voices for long-term persona building

---

## D-ID: Video Generation for All 3 Personas

### Account Setup

**D-ID Lite plan: $6/mo**
- 10 minutes of video/month
- Supports image + audio input
- Lip sync to uploaded audio

### Video Generation Workflow

**Per video:**
1. Select best Leonardo.ai image for the scene
2. Generate audio with ElevenLabs (correct voice profile)
3. Upload image + audio to D-ID
4. Generate talking head video
5. Download and add to content pipeline

### Monthly Video Budget

**10 minutes/month total across 3 personas:**

| Persona | Videos/mo | Length | Total |
|---------|-----------|--------|-------|
| Findom | 2 | 60s each | 2 min |
| Grace | 4 | 60s each | 4 min |
| Coach Max | 3 | 60s each | 3 min |
| Buffer | - | - | 1 min |
| **Total** | **9** | | **10 min** |

**Optimization:**
- Keep all D-ID videos under 60 seconds
- Use D-ID for "talking to camera" content only
- Use static images + audio overlay for content where lip sync isn't needed
- This stretches the budget significantly

### HeyGen Upgrade Path (Month 3+)

When revenue hits $500/mo combined:
- Upgrade to HeyGen Creator ($24/mo)
- 15 minutes of video/month
- Better lip sync quality
- More natural head movement
- Avatar customization options
- New total tool cost: $58/mo

---

## Content Batch Workflow: One Session, Three Personas

### Weekly Batch Session (3-4 hours, Sunday evening)

**Hour 1: Image Generation (Leonardo.ai)**

```
1. Open Leonardo.ai
2. Load Findom base prompt + seed
   - Generate 7 images (one per day) across different settings
   - Download all, organize in findom/week_XX/ folder
3. Load Grace base prompt + seed
   - Generate 7 images across devotional settings
   - Download all, organize in faith/week_XX/ folder
4. Load Coach Max base prompt + seed
   - Generate 7 images across gym/fitness settings
   - Download all, organize in fitness/week_XX/ folder
```

**Hour 2: Script Writing + Audio (ElevenLabs)**

```
1. Write all video scripts for the week:
   - Findom: 1 video script (60s)
   - Grace: 2 devotional scripts (60s each)
   - Coach Max: 2 workout tip scripts (60s each)
2. Open ElevenLabs
3. Select Findom voice profile → generate audio → download
4. Select Grace voice profile → generate audio → download
5. Select Coach Max voice profile → generate audio → download
```

**Hour 3: Video Generation (D-ID)**

```
1. Open D-ID
2. Upload Findom image + audio → generate → download
3. Upload Grace images + audio (x2) → generate → download
4. Upload Coach Max images + audio (x2) → generate → download
5. Total: 5 videos generated for the week
```

**Hour 4: Post Scheduling**

```
1. Open scheduling tool (Buffer, Hypefury, or platform native)
2. Schedule all 3 personas:
   - Findom: 3-5 posts/day for 7 days
   - Grace: 4 posts/day for 7 days
   - Coach Max: 4 posts/day for 7 days
3. Queue Reels/TikToks for each persona
4. Prepare story templates for the week
```

### Batch Efficiency Tips

1. **Write all scripts first** - Don't switch between writing and generating
2. **Generate all images in one Leonardo session** - Switching between seeds/prompts is fast
3. **Generate all audio in one ElevenLabs session** - Just switch voice profile between clips
4. **Generate all videos in one D-ID session** - Upload pairs of image + audio sequentially
5. **Schedule everything at once** - Don't post manually during the week

### Content Reuse Across Personas

Some content can be adapted across personas with different framing:

| Universal Theme | Findom Version | Grace Version | Coach Max Version |
|----------------|----------------|---------------|-------------------|
| Discipline | "Standards require discipline" | "Faith requires daily practice" | "Results require showing up" |
| Morning routine | "My luxury morning ritual" | "My 5 AM devotional routine" | "My 5 AM training routine" |
| Consistency | "Consistency builds wealth" | "Consistency deepens faith" | "Consistency builds muscle" |
| Community | "My loyal community" | "Our prayer community" | "The 5AM Gains crew" |

---

## Asset Organization: Folder Structure

```
AI_INFLUENCER/
├── FINDOM/
│   ├── prd.json
│   ├── assets/
│   │   ├── reference_images/     # 5 seed-locked reference faces
│   │   ├── weekly_content/
│   │   │   ├── week_01/
│   │   │   ├── week_02/
│   │   │   └── ...
│   │   ├── videos/
│   │   └── audio/
│   ├── scripts/                  # Video scripts
│   └── scheduling/               # Scheduled post drafts
│
├── SFW_PERSONAS/
│   ├── FAITH_PERSONA.md
│   ├── FITNESS_PERSONA.md
│   ├── SHARED_TOOLSTACK.md       # This file
│   ├── CROSS_PROMOTION_MAP.md
│   │
│   ├── faith/
│   │   ├── reference_images/     # 5 seed-locked Grace faces
│   │   ├── weekly_content/
│   │   │   ├── week_01/
│   │   │   ├── week_02/
│   │   │   └── ...
│   │   ├── videos/
│   │   ├── audio/
│   │   ├── scripts/
│   │   └── scheduling/
│   │
│   └── fitness/
│       ├── reference_images/     # 5 seed-locked Coach Max faces
│       ├── weekly_content/
│       │   ├── week_01/
│       │   ├── week_02/
│       │   └── ...
│       ├── videos/
│       ├── audio/
│       ├── scripts/
│       └── scheduling/
```

### File Naming Convention

**Images:** `{persona}_{setting}_{date}_v{version}.png`
- `grace_garden_20260127_v1.png`
- `max_gym_20260127_v2.png`

**Audio:** `{persona}_{content_type}_{date}.mp3`
- `grace_devotional_20260127.mp3`
- `max_supplement_review_20260127.mp3`

**Video:** `{persona}_{platform}_{content_type}_{date}.mp4`
- `grace_tiktok_devotional_20260127.mp4`
- `max_ig_reel_form_check_20260127.mp4`

---

## Cost Scaling Path

| Combined Revenue | Tool Budget | Changes |
|-----------------|-------------|---------|
| $0-500/mo | $40/mo | Base stack (Leonardo Apprentice + ElevenLabs Starter + D-ID Lite) |
| $500-1,500/mo | $58/mo | Upgrade D-ID to HeyGen ($24/mo) |
| $1,500-3,000/mo | $82/mo | Upgrade Leonardo to Artisan ($24/mo) for more tokens |
| $3,000-5,000/mo | $145/mo | Upgrade ElevenLabs to Creator ($99/mo) for more audio |
| $5,000+/mo | $247/mo | Add HeyGen Business ($48/mo), premium everything |

**Rule:** Tool spending should never exceed 10% of revenue. Scale tools as revenue grows.

---

## Quick Reference: Daily Operations

### Minimum Viable Daily Effort (30 min total)

| Task | Time | Tool |
|------|------|------|
| Post pre-scheduled content | 5 min | Buffer/native scheduling |
| Engage as each persona (replies, likes) | 15 min | Manual on phone |
| Check analytics/adjust | 5 min | Platform analytics |
| Respond to DMs/comments | 5 min | Manual |

### Weekly Batch Session (4 hours, Sunday)

| Task | Time | Tool |
|------|------|------|
| Generate all images | 60 min | Leonardo.ai |
| Write all scripts | 30 min | Manual |
| Generate all audio | 30 min | ElevenLabs |
| Generate all videos | 30 min | D-ID/HeyGen |
| Schedule all posts | 60 min | Buffer/native |
| Plan next week content | 30 min | Manual |

**Total weekly time investment: ~7.5 hours (30 min/day + 4 hr batch)**
**Total monthly cost: $40**
**Break-even: ~$10/hour of work at $300/mo revenue. Scales infinitely from there.**
