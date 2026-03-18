# YouTube Content Factory Playbook

**Created:** 2026-02-27
**Status:** READY TO EXECUTE
**Companion script:** `AUTOMATIONS/youtube_factory.py`
**Setup guide:** `OPS/LOCAL_VIDEO_GEN_SETUP.md`

---

## Strategy

Build faceless YouTube channels using local AI (Mac, $0 marginal cost). Long-form content clipped into shorts. Script → narration → B-roll → assembly → upload → cross-post. One video per day per channel.

---

## 1. Profitable Niches (Feb 2026)

| Niche | CPM Range | Difficulty | Competition | Time to $1K/mo |
|-------|-----------|-----------|-------------|----------------|
| Finance/Investing | $12-25 | High | High | 4-6 months |
| Horror/Mystery | $8-15 | Medium | Medium | 3-5 months |
| AI/Tech News | $6-12 | Medium | Medium-High | 3-4 months |
| Historical Docs | $6-12 | Medium | Low-Medium | 4-6 months |
| Comparison/Ranking | $5-10 | Low | Medium | 2-4 months |
| Reddit Stories | $4-8 | Low | Very High | 3-5 months |

### Recommended Starting Niches (pick 1-2)

**Tier 1 — Start Here:**
- **AI/Tech News:** You already track this. Repackage alpha research into videos. Low effort to repurpose existing content. $6-12 CPM.
- **Comparison/Ranking:** "Top 10 X vs Y" format. Easy to script. High search volume. $5-10 CPM.

**Tier 2 — Scale To:**
- **Horror/Mystery:** Highest engagement rates. AI-generated visuals work well. $8-15 CPM.
- **Finance/Investing:** Highest CPM but needs credibility signals.

**Tier 3 — Boomer Male 55-70 Demographic (HIGH CPM, LOW competition in faceless):**
- **Golf Tips/Reviews:** $15-30 CPM. "Best Putters Under $200" / "Fix Your Slice in 5 Minutes." 10-20 min calm authority format. Affiliate: golf gear $40-120.
- **Fishing Tutorials:** $8-15 CPM. "Best Bass Lures for Spring 2026" / "Kayak Fishing Setup Guide." Deep knowledge signals. Affiliate: fishing gear $30-100.
- **Health/Wellness for Men 50+:** $12-25 CPM. "Joint Pain Relief That Actually Works" / "Sleep Better After 55." Affiliate: supplements $30-80, pain relief devices.
- **Workshop/DIY/Tools:** $8-15 CPM. "Best Table Saw Under $500" / "Woodworking Basics for Beginners." Affiliate: power tools, workshop gear.
- **Retirement Planning Basics:** $20-35 CPM. "Social Security Timing Strategy" / "Medicare Explained Simply." Highest CPM of any niche. Affiliate: financial planning services.

**Boomer Content Format Rules:**
- 10-20 min longform (NOT shorts). This demographic watches full videos.
- Calm, authoritative narration. No hype. No zoomer energy. Think PBS documentary meets practical guide.
- Lower background music volume. Clear speech priority.
- Larger text overlays. High contrast. Simple thumbnails with clear text.
- CTA: "subscribe for more" at end, not mid-roll spam. Email newsletter capture in description.
- Upload schedule: 2-3x/week consistency beats daily churn for this audience.

---

## 2. Complete Pipeline

```
Script (Claude API) → TTS (local Qwen3-TTS/Bark) → B-Roll (local Wan2.1/SDXL)
→ Assembly (ffmpeg/moviepy) → Clip to Shorts → Upload (YouTube API)
→ Cross-post to TikTok/Reels
```

### Step-by-Step

**Step 1: Script Generation (5-10 min)**
```bash
python3 AUTOMATIONS/youtube_factory.py --generate-script --niche tech --topic "5 AI tools that replaced $200K jobs"
```
- Claude API generates 1500-2500 word script
- Includes: hook (first 15 seconds), body sections, CTA
- Output: `output/youtube/{niche}/{date}/script.md`

**Step 2: TTS Narration (2-5 min)**
```bash
python3 AUTOMATIONS/youtube_factory.py --narrate --niche tech --topic "5 AI tools"
```
- Uses local Qwen3-TTS (already set up per LOCAL_VIDEO_GEN_SETUP.md)
- Generates natural-sounding narration
- Output: `output/youtube/{niche}/{date}/narration.wav`

**Step 3: B-Roll Generation (10-30 min depending on model)**
```bash
python3 AUTOMATIONS/youtube_factory.py --generate-broll --niche tech --topic "5 AI tools"
```
- Uses Wan2.1 or SDXL for visual segments
- Generates 5-10 clips per video
- Can also use stock footage (Pexels API, free)
- Output: `output/youtube/{niche}/{date}/broll/`

**Step 4: Assembly (2-5 min)**
```bash
python3 AUTOMATIONS/youtube_factory.py --assemble --niche tech --topic "5 AI tools"
```
- ffmpeg combines narration + B-roll + text overlays
- Adds background music (royalty-free)
- Adds subtitles (auto-generated via Whisper)
- Output: `output/youtube/{niche}/{date}/final.mp4`

**Step 5: Auto-Clip to Shorts (1-2 min)**
```bash
python3 AUTOMATIONS/youtube_factory.py --clip --niche tech --topic "5 AI tools"
```
- Detects key moments via audio energy analysis
- Creates 30-60 second vertical clips
- Output: `output/youtube/{niche}/{date}/shorts/`

**Step 6: Upload (1 min)**
```bash
python3 AUTOMATIONS/youtube_factory.py --upload --niche tech --topic "5 AI tools"
```
- YouTube Data API v3 upload
- Auto-sets title, description, tags, thumbnail
- Schedules for optimal time
- Output: Upload confirmation + video URL

**Step 7: Cross-Post**
- Shorts → TikTok (manual or via TikTok API)
- Shorts → Instagram Reels (manual or via Meta API)
- Full video description → blog post (optional SEO play)

### Full Pipeline (One Command)**
```bash
python3 AUTOMATIONS/youtube_factory.py --full-pipeline --niche tech --topic "5 AI tools that replaced $200K jobs" --dry-run
```

---

## 3. Revenue Projections (Realistic)

Based on 1 video/day, building over 6 months:

| Month | Videos | Views/Video | Total Views | Revenue (at niche CPM) |
|-------|--------|-------------|-------------|----------------------|
| 1 | 30 | 100-500 | 5K-15K | $0 (not monetized) |
| 2 | 60 | 500-2K | 30K-120K | $0 (building to 1K subs) |
| 3 | 90 | 1K-5K | 90K-450K | $50-200 (monetized) |
| 4 | 120 | 2K-10K | 240K-1.2M | $200-800 |
| 5 | 150 | 5K-20K | 750K-3M | $500-2K |
| 6 | 180 | 10K-50K | 1.8M-9M | $1K-5K |

**Monetization requirements:** 1,000 subscribers + 4,000 watch hours (long-form) or 10M shorts views in 90 days.

**Note:** These are conservative estimates. One viral video (500K+ views) accelerates everything by months.

---

## 4. Content Calendar (First 30 Days — AI/Tech Niche)

### Week 1: Foundation
| Day | Topic | Type |
|-----|-------|------|
| 1 | "5 AI tools that do the work of a $200K employee" | Listicle |
| 2 | "Claude vs GPT-5 vs Gemini: honest comparison" | Comparison |
| 3 | "I automated my entire job with AI — here's how" | Story |
| 4 | "The AI tools nobody talks about" | Hidden gems |
| 5 | "How to use Claude Code to build apps in minutes" | Tutorial |
| 6 | "AI is replacing these 10 jobs RIGHT NOW" | Listicle |
| 7 | "The dark side of AI agents nobody warns you about" | Controversy |

### Week 2: Engagement Hooks
| Day | Topic | Type |
|-----|-------|------|
| 8 | "I built a $10K/mo business using only AI" | Case study |
| 9 | "Best free AI tools in 2026 — complete tier list" | Ranking |
| 10 | "AI coding: is it actually good?" | Review |
| 11 | "5 ways to make money with AI (that actually work)" | Listicle |
| 12 | "The AI bubble: are we in trouble?" | Analysis |
| 13 | "How I use AI to work 2 hours a day" | Story |
| 14 | "AI vs humans: who wins at [specific task]?" | Comparison |

### Week 3-4: Double Down on Winners
- Check analytics from weeks 1-2
- Make more of whatever got the highest CTR and watch time
- Test different thumbnail styles
- A/B test video lengths (8 min vs 15 min vs 20 min)

---

## 5. Channel Branding

### Channel Name Ideas (AI/Tech)
- AIBreakdown, TechPilled, CodeAndConquer, AutomateEverything
- Pick something memorable, searchable, not taken

### Visual Identity
- Thumbnail template: bold text + face/reaction image + topic visual
- Color scheme: 2-3 colors max, consistent across all thumbnails
- Font: Heavy/bold sans-serif (Impact, Bebas Neue, or similar)
- Intro: 2-3 second branded intro (or skip entirely — YouTube penalizes long intros)

### Description Template
```
[Hook — what viewer will learn]

In this video, I break down [topic]. We cover:
- Point 1
- Point 2
- Point 3

[timestamps if 10+ min]

Tools mentioned:
- [Tool 1]: [link]
- [Tool 2]: [link]

---
Subscribe for daily AI/tech breakdowns.
```

---

## 6. Monetization Timeline

| Milestone | When | Revenue |
|-----------|------|---------|
| First upload | Day 1 | $0 |
| 100 subscribers | Week 2-4 | $0 |
| 1,000 subscribers | Month 2-3 | $0 (apply for YPP) |
| Monetization approved | Month 3-4 | First ad revenue |
| 5,000 subscribers | Month 4-6 | $200-1K/mo |
| 10,000 subscribers | Month 6-9 | $500-3K/mo |
| 50,000 subscribers | Month 9-18 | $2K-10K/mo |

### Revenue Streams Beyond Ads
1. **Affiliate links** in descriptions ($100-500/mo at 10K subs)
2. **Sponsored segments** ($200-2K/video at 50K subs)
3. **Digital products** linked from videos (courses, templates)
4. **Channel memberships** ($2-10/mo per member)
5. **Cross-platform** (TikTok Creator Fund, Instagram bonuses)

---

## 7. Failure Modes and Fixes

| Problem | Likely Cause | Fix |
|---------|-------------|-----|
| Low views | Bad thumbnails/titles | Study top-performing videos in niche, copy their thumbnail style |
| Low watch time | Boring intro | Hook in first 5 seconds, cut fluff |
| No subscriber growth | No CTA | Add subscribe CTA at peak engagement moment |
| Demonetization | Controversial content | Stay educational, avoid claims without proof |
| Copyright strike | Using copyrighted footage | Use only AI-generated + royalty-free content |
| TTS sounds robotic | Wrong TTS model | Try Bark or XTTS instead of basic TTS |
| Video quality too low | Poor B-roll | Mix AI-generated with Pexels stock footage |

---

## 8. Cross-Posting Strategy

### Long-form → Shorts Pipeline
- Every 10+ min video produces 3-5 shorts
- Shorts go to: YouTube Shorts, TikTok, Instagram Reels
- Different hook for each platform (TikTok = fast, YouTube = value-first)

### Platform-Specific Adaptations
| Platform | Length | Aspect Ratio | Style |
|----------|--------|-------------|-------|
| YouTube Long | 8-20 min | 16:9 | Educational, detailed |
| YouTube Shorts | 30-60 sec | 9:16 | Hook + key insight |
| TikTok | 15-60 sec | 9:16 | Casual, hook heavy |
| Instagram Reels | 30-90 sec | 9:16 | Polished, text overlays |

---

## Quick Start

```bash
# Full pipeline (dry run first)
python3 AUTOMATIONS/youtube_factory.py --full-pipeline --niche tech --topic "5 AI tools replacing jobs" --dry-run

# Then for real
python3 AUTOMATIONS/youtube_factory.py --full-pipeline --niche tech --topic "5 AI tools replacing jobs"
```

**Prerequisites:**
1. YouTube API credentials (get from Google Cloud Console)
2. Claude API key for script generation
3. Local TTS model installed (see LOCAL_VIDEO_GEN_SETUP.md)
4. ffmpeg installed (`brew install ffmpeg` — already done)
