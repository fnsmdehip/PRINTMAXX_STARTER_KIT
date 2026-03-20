# C19 ASMR, Production Guide (AI-First, Zero Human Required)

## Stack Overview

Total monthly tool cost: $62-97/month
Human time required: 2-4 hours/week for 3 uploads

| Tool | Purpose | Cost | Tier |
|------|---------|------|------|
| ElevenLabs (Creator) | AI voice narration | $22/mo | Required for narrated |
| Freesound.org | Sound effects library | Free | Always |
| Audacity | Sound mixing (desktop) | Free | Always |
| DaVinci Resolve | Video assembly | Free | Always |
| ChatGPT / Claude | Script writing | $20/mo | Required for narrated |
| Stable Diffusion (local) or Midjourney | Thumbnail + static visuals | $0-10/mo | Optional |
| YouTube Studio | Upload + scheduling | Free | Always |
| Patreon | Membership platform | 8% of revenue | Revenue |
| Gumroad | Digital product sales | 10% fee | Revenue |

**All-in tool cost: $42-52/month** (or $62/mo with Midjourney for better thumbnails)

---

## Part 1: AI Voice Setup (ElevenLabs)

### Voice selection for ASMR
Not all ElevenLabs voices work for ASMR. These do:

| Voice | Type | Best for | Why |
|-------|------|---------|-----|
| Charlotte | British female | Philosophy, ambient narration | Naturally slow, warm |
| Alice | American female | Finance, educational | Calm, measured |
| Rachel | American female | Roleplay, coaching | Slightly warmer |
| Fin | Irish male | Tech content | Distinctive, calm |
| Custom clone | Your design | Branded channel | Consistency |

**Settings for ASMR output:**
- Stability: 0.80 (higher = more consistent, less breathy)
- Similarity: 0.75
- Style: 0.15 (LOWER = more natural, less theatrical)
- Speaker boost: OFF (adds sharpness, wrong for ASMR)

**ASMR-specific generation trick:**
Insert `[pause]` tags between sentences. ElevenLabs v3 honors them.
Example script: "This is the letter A. [pause] Dot dash. [pause] Listen closely. [pause]"

### Delivery speed
- Standard narration: 0.85x speed in ElevenLabs settings
- Reading content (books, summaries): 0.80x
- Roleplay content: 0.90x (slightly faster = more conversational)
- Educational slow-down: Add explicit pauses in script rather than changing speed

---

## Part 2: Sound Layer System

### The 3-Layer Mix

Every ASMR video uses 3 audio layers mixed at specific volumes:

```
Layer 1, BASE (ambient/drone): 100% volume in mix
Layer 2, ACTION SOUNDS (triggers): 60-80% of base
Layer 3, NARRATION (voice): 90-110% of base (voice sits on top)
```

**Never fight layers.** If the base is loud, the triggers get lost. EQ the base to remove 2kHz-4kHz frequencies, that's where most ASMR trigger sounds live.

### Freesound.org sourcing guide
All sounds royalty-free. Search terms that work:

| Sound Category | Freesound search query | License needed |
|----------------|----------------------|----------------|
| Rain on window | "rain window interior medium" | CC0 |
| Library ambience | "library quiet footsteps" | CC0 or CC-BY |
| Fireplace | "fireplace crackling soft" | CC0 |
| Page turn | "book page turn single" | CC0 |
| Keyboard typing | "mechanical keyboard typing slow" | CC0 |
| Coffee shop | "coffee shop ambience quiet" | CC0 |
| Ocean cave | "cave ocean echo water drip" | CC0 |
| Airport | "airport terminal ambience" | CC0 |

**Filter: Always filter for CC0 (no attribution required)**
**Duration: Get 2-5 min clips minimum, loop them in Audacity**

### Looping technique (Audacity)
1. Import base sound file
2. Effect → Fade Out on last 5 seconds
3. Effect → Fade In on first 5 seconds
4. Export as 60-min loop: Tracks → Generate → Silence for remainder, then chain together
5. For 8-hour videos: generate 8 copies of the base, join in timeline

### Mixing levels (Audacity / DaVinci)
- Base ambient: -18 dB
- Action triggers: -24 dB
- Voice narration: -12 dB
- Master output target: -14 LUFS (YouTube standard, prevents normalization destruction)
- Peak ceiling: -1 dBFS

---

## Part 3: Visual Production

### Static image videos (ambient/soundscape content)
Easiest. Single static image, 60-90 min, rendered once.

**Process:**
1. Find/generate image (see sources below)
2. Import to DaVinci Resolve as 3840x2160 (4K) still
3. Set project frame rate: 24fps
4. Drag to timeline, extend to full video length
5. Import audio tracks to timeline
6. Color grade: warm tones → Offset lift warm, Contrast slight increase
7. Export: H.264, YouTube preset, target bitrate 8-12 Mbps

**Image sources (free):**
- Unsplash.com, search "cozy library", "rainy window", "airport night"
- Pexels.com, same searches
- Midjourney, "$0 per image" with basic plan if <200 images/mo
- Stable Diffusion local, completely free, needs decent GPU

**Midjourney prompts for key concepts:**
- Library: `cozy library interior night, warm candlelight, wooden shelves, fog window, rain, photorealistic, soft shadows --ar 16:9`
- Konbini: `japanese convenience store interior 2am, fluorescent lights, rain outside, empty aisles, neon reflections --ar 16:9`
- Cave/ocean: `sea cave entrance sunset, ocean waves, golden hour, cinematic, photorealistic --ar 16:9`

### Thumbnail production

**Formula:** Background image + large readable text + subtle ASMR visual indicator

**Thumbnail text rules:**
- Max 5 words
- Font: Heavy sans-serif (Montserrat Bold, Inter Black)
- Color: White or cream text on dark background
- No emoji
- Lowercase preferred for calm aesthetic

**Thumbnail specs:**
- Size: 1280x720px (YouTube requirement)
- Format: JPG (not PNG, smaller file, loads faster)
- Text size: Minimum 80px, must be readable on mobile thumbnail

**Canva thumbnail template elements:**
1. Dark-gradient overlay on background image (30% opacity black gradient, bottom-heavy)
2. Channel name small text top-left (12px, 40% opacity white)
3. Main hook text center-left (80px, white, bold)
4. Optional: small "ASMR" label badge top-right (pill shape, dark bg)

---

## Part 4: Production Workflow (3 uploads/week)

### Weekly schedule
- **Monday:** Script 2 narrated videos (Claude-assisted, 30 min total)
- **Tuesday:** Generate audio tracks (ElevenLabs + Freesound mixing, 90 min)
- **Wednesday:** Assemble + export Video 1, upload + schedule (45 min)
- **Thursday:** Assemble + export Video 2, upload + schedule (45 min)
- **Friday:** Record/generate pure ambient video (30 min production, 20 min upload)
- **Weekend:** Batch script writing for next week (60 min)

**Total time: ~5.5 hours/week**

### Claude script prompt template
```
Write an ASMR narration script for a YouTube video.

Topic: [TOPIC]
Runtime: [X] minutes
Format: Whispered, slow delivery, educational

Requirements:
- Start with 30 seconds of ambient description ("settle in, get comfortable...")
- Deliver [X] key points at 90 seconds each
- Insert [pause] tags between sentences
- Use only real data and specific numbers (no vague claims)
- End with soft CTA: "if you want the no-ads version, Patreon link is below"
- Total word count: approximately [X × 90 × 2.5] words at 0.80x ElevenLabs speed

Voice style: calm, measured, no excitement. Like an audiobook narrator at 80wpm.
```

### ElevenLabs batch workflow
1. Split script into 500-character chunks (API limit optimization)
2. Generate each chunk, download MP3
3. Join in Audacity with 0.5-second silence between each
4. Apply full processing pipeline (see mixing levels above)
5. Final file: WAV for DaVinci import

### DaVinci Resolve project template
Save a base .drp file with:
- YouTube 1080p 24fps timeline pre-configured
- Color grade node saved (warm preset)
- Delivery settings saved (YouTube H.264 preset)
- Channel intro/outro pre-loaded (5-second fade in, 5-second fade out)

**Batch render command (once template is set):**
Just drag new audio to existing timeline, swap background image, render.
Time per video after template: 20-25 minutes.

---

## Part 5: Upload Optimization

### Title formula
`[primary keyword] ASMR | [hook/setting] [optional runtime]`

Examples:
- `sleep ASMR | cozy library rain sounds 1 hour`
- `study ASMR | japanese convenience store midnight`
- `finance ASMR | she explains investing while you sleep`

### Description template
```
fall asleep to [hook]. [one sentence setting description.]

no ads version + extended archive → [Patreon link]

--- SLEEP BETTER ---
Calm app (7-day free trial): [affiliate link]
BetterSleep app: [affiliate link]
Sleep mask recommendation: [Amazon Associates link]
White noise machine: [Amazon Associates link]

--- MORE FROM THIS CHANNEL ---
[playlist link 1]
[playlist link 2]

#ASMR #SleepSounds #[niche keyword]

This video is not intended to diagnose or treat any sleep disorders. If you have persistent sleep issues, consult a healthcare professional.
```

### Tags (copy-paste set)
```
ASMR, sleep sounds, ASMR sleep, relaxing sounds, ambient sounds, white noise, [topic] ASMR, ASMR [topic], sleep music, study ASMR, focus sounds, fall asleep fast, sleep aid, rain sounds, relaxation
```

### Scheduling
- Best upload times: Thursday 2pm-4pm EST, Saturday 10am-12pm EST
- Use YouTube Studio scheduled publishing
- Set first comment (pinned) = Patreon link + top affiliate link immediately on publish

### Playlist architecture
Create these playlists immediately:
1. "Sleep Sounds 1-3 Hours" (ambient, no narration)
2. "Study with Me ASMR" (keyboard, coding, productivity)
3. "Finance ASMR" (money content series)
4. "Philosophy for Insomniacs" (readings series)
5. "8+ Hour Sleep Ambients" (long-form, algorithm juice)

---

## Part 6: Channel Growth Acceleration

### Algorithm hacks for sleep content
- **CTR:** Test thumbnail text A/B (YouTube allows 3 thumbnails, tracks CTR automatically)
- **Watch time:** Long videos (60-90 min) with high completion = algorithm signals "people watch this to end" = recommendation fuel
- **Return viewers:** Sleep content = people come back every night. 7-day retention metric is unusually high = YouTube rewards this with more impressions
- **Shorts crossover:** Clip first 60 seconds of any narrated video as a Short. Use it to funnel to long-form. Shorts at 10K views = meaningful long-form discovery

### Cross-promotion
- Post ambient clips to Reddit: r/ASMR, r/sleepsounds, r/ambientmusic, r/Nootropics
- Twitter/X: "what sounds do you fall asleep to?" engagement bait → reply with video link
- Pinterest: pin thumbnail with sleep keyword boards
- Spotify (audio only): Use Anchor/Buzzsprout to distribute ambient audio as podcast episodes, free additional distribution

### Community tab usage (once unlocked at 500 subs)
- Monthly: "What's your favorite sleep sound?" poll
- Weekly: Behind-the-scenes snippet of upcoming video
- Patreon teaser: preview 30-second clip of exclusive
