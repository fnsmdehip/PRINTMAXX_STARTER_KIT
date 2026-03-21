# VIDEO AUTOPILOT — Full Pipeline Spec

generate > find templates > auto-edit > schedule > post > track > optimize

## the system

```
[1] TEMPLATE FINDER          [2] VIDEO GENERATOR         [3] AUTO-EDITOR
viral_content_scanner.py  →  ai_video_content_pipeline  →  claude dispatch
+ trending format scraper     + best tool per use case      + capcut/descript
+ reddit/tiktok trends        + parallel gen (3-5 tools)    + auto captions
                                                            + auto transitions
                                                            + hook optimization

[4] SCHEDULER                [5] POSTER                  [6] TRACKER
publer/buffer API         →  auto_content_poster.py     →  AI_VIDEO_CONTENT_TRACKER.csv
+ optimal time slots          + multi-platform              + views, clicks, conversions
+ A/B test scheduling         + format adaptation           + revenue attribution
                              + 9:16 / 16:9 / 1:1          + performance scoring
                                                            + feed back to [1]
```

## [1] template finder — what's working NOW

### sources
- **viral_content_scanner.py** (existing) — scrapes viral tweets, detects engagement patterns
- **tiktok creative center** — top performing ads, trending sounds, viral formats
- **instagram reels trending** — audio trends, format trends
- **youtube shorts analytics** — what's getting views in our niches

### template extraction
when a viral video is found, extract:
- hook structure (first 3 seconds pattern)
- visual format (split screen, green screen, POV, text overlay, etc.)
- audio pattern (trending sound, original, voice-over, ASMR)
- pacing (cuts per second, zoom timing)
- CTA placement (end, middle, overlay)
- caption style (all caps hook, emoji placement, hashtag strategy)

store in: `10_RESEARCH/VIDEO_RESEARCH/templates/VIRAL_FORMATS.md`

### implementation
extend `viral_content_scanner.py` to:
1. classify viral videos by format type
2. extract hook/CTA patterns
3. store template library that video generator can reference
4. auto-update weekly with new trending formats

## [2] video generator — tool selection matrix

### auto-select best tool per content type

| content type | primary tool | fallback | why |
|-------------|-------------|----------|-----|
| hero/ad quality | Veo 3.1 | Seedance 2.0 | highest realism |
| product demo | Seedance 2.0 | Kling | multimodal reference input |
| social shorts (volume) | Kling 2.6 | Pika | best value, 2min length |
| talking head/avatar | HeyGen / Seedance | D-ID | consistent face |
| artistic/stylized | Luma Ray 3 | Runway | unique aesthetic |
| faceless narration | Kling + ElevenLabs | Veo + ElevenLabs | voice + visuals |
| multilingual | Seedance 2.0 | HeyGen | 8+ language lip sync |

### the $0 stack (current phase)
```
daily capacity at $0:
  Seedance (Xiao Yunque free):  unlimited during promo
  Kling free:                   66 credits = 1-2 vids
  Pika free:                    ~3-5 clips
  Hailuo free:                  20-30 watermarked
  Veo free:                     ~5/month (save for hero)
  Luma free:                    ~1/day

  TOTAL: 25-35 videos/day at $0
```

### parallel generation
for each content piece, generate 2-3 versions across tools simultaneously:
- version A: primary tool (best quality)
- version B: fallback tool (backup)
- version C: different style (A/B test)

pick the best one. this is cheap at $0 tier.

## [3] auto-editor — claude dispatch system

### the problem
AI video tools output raw clips. they need:
- captions (auto-generated, styled)
- transitions between clips
- hook text overlay (first 3 sec)
- CTA overlay (last 3 sec)
- background music (if no native audio)
- aspect ratio adaptation (9:16, 16:9, 1:1)
- branding elements (watermark, logo)

### solution: claude-dispatched editing

**option A: CapCut automation (primary)**
- CapCut has no public API
- BUT: CapCut desktop can be automated via Playwright browser control
- workflow: claude generates edit instructions > playwright drives CapCut > exports
- CapCut auto-captions are industry-best and FREE
- limitations: fragile (UI changes break it), needs desktop app running

**option B: FFmpeg pipeline (reliable fallback)**
- fully scriptable, zero cost, runs on cron
- can do: captions (via whisper + ffmpeg burn-in), transitions, overlays, resize
- claude generates the ffmpeg command chain based on template
- limitations: less polished than CapCut, no fancy effects

**option C: Descript API (when budget allows)**
- text-based editing API
- auto-remove filler words, auto-captions, multi-track
- $24/mo but very powerful for automation
- best for: podcast clips, talking head edits, long-form to short

**option D: Opus Clip (auto short clips)**
- $19/mo, specialized for: take long video > auto-detect viral moments > export shorts
- has API for automation
- best for: repurposing YouTube long-form into shorts

### recommended stack (phase 0, $0)
```
PRIMARY:  FFmpeg pipeline (100% free, fully automated)
  - whisper for transcription > caption burn-in
  - ffmpeg for transitions, overlays, resize
  - claude generates the edit script per template

SECONDARY: Remotion (free, already deployed at MEDIA/remotion/)
  - 40+ videos already generated
  - React-based = claude writes the template code, remotion renders
  - perfect for: branded series, app promos, recurring formats, data-driven videos
  - can accept dynamic data (stats, prices, rankings) and render video automatically
  - use for: any video with consistent branding/template that repeats

TERTIARY: CapCut MCP (free, semi-automated)
  - use for: fancy animated caption styles, trending effects
  - CapCut MCP server lets claude control it programmatically
  - export to posting queue

FUTURE ($50+/mo): Opus Clip + Descript
  - opus clip for auto-viral-moment detection
  - descript for text-based editing at scale
```

### ffmpeg auto-edit pipeline (buildable NOW)

```python
# claude generates this per video based on template:
ffmpeg_commands = [
    # 1. Add auto-captions (whisper transcription burned in)
    "whisper input.mp4 --model small --output_format srt",
    "ffmpeg -i input.mp4 -vf subtitles=input.srt:force_style='FontSize=24,Bold=1,Alignment=2' captioned.mp4",

    # 2. Add hook text overlay (first 3 seconds)
    "ffmpeg -i captioned.mp4 -vf \"drawtext=text='THE ONE THING NOBODY TELLS YOU':fontsize=48:fontcolor=white:x=(w-tw)/2:y=h/4:enable='between(t,0,3)'\" hooked.mp4",

    # 3. Resize for platform
    "ffmpeg -i hooked.mp4 -vf 'scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2' tiktok_ready.mp4",

    # 4. Add background music (low volume)
    "ffmpeg -i tiktok_ready.mp4 -i bgmusic.mp3 -filter_complex '[1:a]volume=0.15[bg];[0:a][bg]amix=inputs=2:duration=first' final.mp4",
]
```

## [4] scheduler — optimal posting

### tool: Publer (recommended over Buffer)
- 5 free accounts
- visual calendar
- auto-posting to TikTok, Instagram, YouTube, Twitter, LinkedIn, Pinterest
- AI assistant built in
- $12/mo unlocks unlimited scheduling

### posting schedule (per niche)

| time slot | platform | content type | why |
|-----------|----------|-------------|-----|
| 7-9 AM | TikTok + Reels | motivation/fitness | morning scroll |
| 12-1 PM | Twitter + LinkedIn | tech/build-in-public | lunch break |
| 5-7 PM | TikTok + Reels + Shorts | entertainment/memes | commute scroll |
| 9-11 PM | TikTok + Reels | sleep/relaxation/faith | bedtime content |

### A/B testing
for each video, schedule 2 versions:
- same video, different hook text
- same video, different thumbnail
- same video, different posting time
track which performs better, feed back to template finder.

## [5] poster — auto_content_poster.py integration

existing `auto_content_poster.py` handles multi-platform posting.
extend to:
1. read from video posting queue (not just text content)
2. upload video to platform-specific endpoints
3. adapt captions per platform (hashtags for TikTok, alt text for Twitter, etc.)
4. handle video format requirements per platform
5. track post URLs for performance monitoring

## [6] tracker + feedback loop

### metrics tracked per video
```csv
video_id, tool_used, template_type, niche, platform, hook_text,
posted_at, views_1h, views_24h, views_7d,
likes, comments, shares, saves,
clicks, conversions, revenue,
engagement_rate, viral_score
```

### feedback loop
```
high performers (>10K views OR >5% engagement):
  → extract template → add to VIRAL_FORMATS.md
  → note which tool produced it
  → increase frequency of that template + tool combo

low performers (<100 views after 24h):
  → flag template as stale
  → try different tool for same content type
  → adjust posting time

revenue performers (any conversion):
  → DOUBLE DOWN immediately
  → create 5 variations of the same template
  → spread across all platforms
  → alert CEO agent for Capital Genesis re-ranking
```

## capital genesis integration

### how this feeds the KPI decision engine

1. **tool cost tracking** → `perpetual_tool_researcher.py` scores tools → feeds venture cost calculations
2. **content ROI** → revenue per video / tool cost = ROI → Capital Genesis ranks content ventures
3. **tool switching signals** → when a cheaper tool matches quality → auto-switch → reduce venture costs
4. **new tool discoveries** → staged as alpha → ranked by Capital Genesis → integrated if P0/P1
5. **performance data** → views/engagement/revenue per niche → Capital Genesis kill/double-down decisions

### auto-decisions the system can make
- tool X quality dropped → switch to tool Y (auto, no human needed)
- new free tier discovered → re-score all content ventures (auto)
- template format going viral → increase production volume (auto)
- niche saturating (declining engagement) → reduce frequency, try new angle (auto)
- revenue per video > $X → alert human to invest in paid tier for more volume

## n8n integration

full pipeline orchestrated via n8n at localhost:5678.
see: `pipeline/N8N_VIDEO_WORKFLOW.md` for the deployable workflow.

key pattern: n8n handles orchestration + API calls.
when a step needs LLM intelligence, n8n calls `claude -p` via
Execute Command node, gets structured JSON back, continues workflow.

```
n8n cron trigger (every 6h)
  → trend check (HTTP node → Reddit/TikTok)
  → script generation (Execute Command → claude -p)
  → tool selection (Execute Command → ai_video_content_pipeline.py, reads tracker)
  → video generation (HTTP node → Kling/Hailuo/Veo API)
  → auto-edit (Execute Command → ffmpeg/whisper OR remotion)
  → caption gen (Execute Command → claude -p)
  → schedule (HTTP node → Publer API)
  → track (Execute Command → append to tracker CSV)
```

## implementation priority

1. **NOW**: FFmpeg auto-edit pipeline (free, scriptable) ✅ SPEC DONE
2. **NOW**: Wire perpetual_tool_researcher.py to cron ✅ DONE (8AM + 8PM)
3. **NOW**: Auto tool selection wired into video pipeline ✅ DONE (reads tracker)
4. **NOW**: Capital Genesis reads tool costs for venture scoring ✅ DONE
5. **NEXT**: Deploy n8n VIDEO_AUTOPILOT workflow (needs API keys for Kling/Publer)
6. **NEXT**: Extend viral_content_scanner.py for template extraction
7. **WEEK 1**: Video posting queue integration with auto_content_poster.py
8. **WEEK 2**: CapCut MCP for animated captions
9. **WHEN $50/mo**: Add Opus Clip for auto-viral-moment detection
10. **WHEN $100/mo**: Add Descript for text-based editing at scale
