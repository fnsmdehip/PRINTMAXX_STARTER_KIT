# AI UGC Tools Stack — Pricing Comparison + Recommended Setup

## The Core Stack (What You Actually Need)

### Tier 1: Must-Haves (Total: ~$55-85/mo)

| Tool | Purpose | Cost | Verdict |
|---|---|---|---|
| **ElevenLabs** | AI voiceover | $22/mo (Creator plan) | Best voice quality, 100K chars/mo |
| **D-ID** | AI avatar videos | $24/mo (Pro plan) | 100 credits/mo, clean results |
| **CapCut** | Editing + captions | $0 (free tier) | Best for mobile-first content |
| **Claude** | Script writing | $20/mo (Pro) or API | $0.003/1K tokens = ~$0.05/script |
| **Pexels/Pixabay** | B-roll footage | $0 | Free commercial use |

**Total Tier 1:** $46-66/mo
**Breakeven:** 1 video at $65 covers the month

---

### Tier 2: Upgrade When You Have Clients (Total: ~$100-160/mo additional)

| Tool | Purpose | Cost | When to Add |
|---|---|---|---|
| **HeyGen** | Premium AI avatar | $89/mo (Creator) | When D-ID quality isn't enough |
| **Descript** | Transcript + edit | $24/mo | When you need to edit by text |
| **Canva Pro** | Thumbnails + graphics | $13/mo | When branding assets are needed |
| **Repurpose.io** | Multi-platform publish | $25/mo | When you're distributing your own content |

---

### Tier 3: Agency-Scale (Total: ~$300-500/mo additional)

| Tool | Purpose | Cost | When to Add |
|---|---|---|---|
| **Synthesia** | Enterprise avatars | $89-330/mo | Enterprise clients only |
| **Runway ML** | AI video generation | $15-95/mo | When clients need B2B cinematic look |
| **Adobe Premiere** | Professional editing | $55/mo | Agency-grade deliverables |
| **Frame.io** | Client collaboration | $15/mo | Client review workflow |

---

## Head-to-Head Comparison: Avatar Tools

### D-ID vs HeyGen vs Synthesia

| Feature | D-ID | HeyGen | Synthesia |
|---|---|---|---|
| **Price (entry)** | $6/mo (Lite, 10 credits) | $29/mo (Essential) | $22/mo (Starter) |
| **Price (practical)** | $24/mo (Pro, 100 credits) | $89/mo (Creator) | $89/mo (Creator) |
| **Video quality** | Good | Very Good | Best |
| **Avatar selection** | 25+ stock | 100+ stock + custom | 230+ stock |
| **Custom avatar** | Yes (Pro+) | Yes ($29 one-time) | Yes (Enterprise) |
| **Lip sync accuracy** | Good | Excellent | Excellent |
| **Max resolution** | 1080p | 4K | 1080p |
| **API access** | Yes | Yes | Yes |
| **Turnaround** | Near instant | Near instant | Near instant |
| **Best for** | Starting out | Scaling | Enterprise clients |

**Recommended:** Start with D-ID → upgrade to HeyGen when you have 3+ regular clients.

---

## Head-to-Head Comparison: Voice Tools

### ElevenLabs vs PlayHT vs Murf

| Feature | ElevenLabs | PlayHT | Murf |
|---|---|---|---|
| **Price (entry)** | $5/mo (Starter) | $31/mo (Creator) | $29/mo (Basic) |
| **Price (practical)** | $22/mo (Creator) | $49/mo (Pro) | $39/mo (Pro) |
| **Voice quality** | Best in class | Very good | Good |
| **Custom voice clone** | Yes ($22+ plan) | Yes ($49+ plan) | Yes ($75+ plan) |
| **Voices available** | 900+ | 800+ | 120+ |
| **Languages** | 29 | 142 | 20 |
| **API** | Yes | Yes | Yes |
| **Emotion control** | Yes | Limited | Yes |
| **Best for** | Quality-first | Language diversity | Simple workflows |

**Recommended:** ElevenLabs exclusively unless you need multiple languages.

---

## Free Tools That Are Actually Good

| Tool | What It Does | Why It Works |
|---|---|---|
| **Pexels** | Stock video + photos | Commercial license, searchable |
| **Pixabay** | Stock video + music | Same as Pexels, different library |
| **CapCut** | Video editing | Designed for content creation, not filmmaking |
| **DaVinci Resolve** | Pro editing | Full free tier, desktop only |
| **OBS Studio** | Screen recording | Best free screen capture |
| **Audacity** | Audio editing | If you need to clean up audio |
| **Canva (free)** | Graphics + thumbnails | Good enough for most use cases |

---

## Production Workflow

### Single Video Workflow (Target: 30 min per video)

```
Step 1: Script (5 min)
→ Use Claude with this prompt:
  "Write a [30/45/60]-second UGC [format] script for [PRODUCT].
   Audience: [TARGET]. Hook: consequence-first. Body: specific numbers.
   CTA: direct. No em dashes. No AI vocabulary."

Step 2: Voice (5 min)
→ Paste script into ElevenLabs
→ Select voice matching the avatar
→ Export as MP3

Step 3: Avatar (10 min)
→ Upload MP3 to D-ID or HeyGen
→ Select avatar
→ Generate video

Step 4: Edit (7 min)
→ Import into CapCut
→ Add captions (auto-generate, then verify)
→ Add b-roll if needed (overlay)
→ Add background music at -20dB

Step 5: Export (3 min)
→ Export per platform specs
→ 9:16 for TikTok/Reels
→ 1:1 for Twitter/Facebook feed
→ 16:9 for YouTube if needed
```

### Batch Production (10 videos in 4 hours)

```
Hour 1: Scripts
→ Write all 10 scripts with Claude
→ Review and refine all 10
→ 6 min per script = 60 min

Hour 2: Voice generation
→ Queue all 10 in ElevenLabs
→ Download all audio files
→ Label: [video_name]_voice.mp3

Hour 3: Avatar generation
→ Upload all 10 audio files to D-ID/HeyGen
→ Start all renders simultaneously
→ Download completed videos as they render

Hour 4: Edit + export
→ CapCut batch import
→ Add captions to all (auto-generate, spot-check)
→ Add music, trim, export
→ 15 min per video = 150 min → batch saves time
```

---

## Cost Per Video at Scale

**Single video (no volume efficiency):**
- Script: $0.05 (Claude API)
- Voice: $0.30 (ElevenLabs per 1K chars)
- Avatar: $0.24 (D-ID Pro = $24/100 credits)
- Editing: $0 (CapCut)
- **Total COGS: $0.59**

**Monthly subscription amortized across 20 videos:**
- ElevenLabs: $22 / 20 = $1.10/video
- D-ID: $24 / 20 = $1.20/video
- **Total COGS at 20 videos/mo: $2.30/video**

**Margin at $65/video with 20 videos:** Revenue $1,300 — COGS $46 = $1,254 gross margin (96.5%)

---

## Tools to Skip

| Tool | Reason to Skip |
|---|---|
| **Pictory** | Overpriced for what it does, limited avatars |
| **InVideo AI** | Stock footage quality is poor, not UGC-looking |
| **Lumen5** | Text-to-video but not UGC-style at all |
| **Colossyan** | Enterprise pricing, not worth it unless $10K/mo |
| **Veed.io** | Good for captions but overpriced as full solution |
| **Hour One** | Expensive, limited use case |

---

## Upgrade Decision Tree

```
Monthly revenue from UGC service?

< $500 → Stay Tier 1 (D-ID + ElevenLabs + CapCut)
$500-2K → Add HeyGen ($89/mo) for quality upgrade
$2K-5K → Add Descript ($24) for faster editing
$5K+ → Add Adobe CC ($55) + Frame.io ($15) for agency workflow
$10K+ → Consider custom avatar training ($500-1K one-time)
```

---

## API vs Manual Workflow

At low volume (< 30 videos/month): Manual workflow is fine.
At 30-100 videos/month: Semi-automated (batch scripts, templated prompts).
At 100+ videos/month: Full API pipeline worth building.

**API endpoints that matter:**
- ElevenLabs: `POST /v1/text-to-speech/{voice_id}` — $0.30/1K chars
- D-ID: `POST /talks` — $0.0015/second of video
- Claude API: `POST /v1/messages` — $0.003/1K input tokens

**At 100 videos/month via API:**
- ElevenLabs: ~$15/mo
- D-ID: ~$12/mo (at avg 60s per video)
- Claude: ~$3/mo
- Total API COGS: $30/mo

Compare to: $22 + $24 + $20 subscription = $66/mo for same volume.
**API is cheaper at 30+ videos/month.**
