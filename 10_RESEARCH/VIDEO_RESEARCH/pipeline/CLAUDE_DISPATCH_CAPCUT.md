# CLAUDE DISPATCH AUTO-EDITING

how claude orchestrates video editing without human intervention.

## the concept

claude receives raw AI-generated video clips and:
1. selects the right editing approach (ffmpeg vs CapCut vs Descript)
2. generates the edit instructions based on the viral template
3. executes the edit pipeline
4. outputs platform-ready video
5. queues for scheduling

## architecture

```
ai_video_content_pipeline.py generates script
  → tool selector picks best AI video tool
  → raw clip generated (15-60s)
  → claude_video_editor.py receives clip
    → analyzes content (whisper transcription, scene detection)
    → matches to viral template from VIRAL_FORMATS.md
    → generates ffmpeg command chain OR CapCut automation script
    → executes edit
    → outputs: 9:16 (TikTok/Reels/Shorts) + 16:9 (YouTube) + 1:1 (IG feed)
  → auto_content_poster.py queues for posting
  → AI_VIDEO_CONTENT_TRACKER.csv tracks performance
```

## editing approaches

### approach 1: FFmpeg Pipeline (primary, $0, fully automated)

advantages:
- 100% free, runs on cron, no GUI needed
- scriptable: claude generates the command chain
- fast: processes in seconds
- reliable: no UI changes to break automation

capabilities:
- auto-captions via whisper + burn-in
- text overlays (hooks, CTAs) with positioning/timing
- transitions (crossfade, fade to black)
- aspect ratio conversion (letterbox, crop, scale)
- background music mixing with volume control
- speed ramping (slow-mo, timelapse)
- color grading (basic LUTs)
- concatenation of multiple clips

limitations:
- no fancy animated text effects
- no AI-powered visual effects
- captions are basic styled (no animated word-by-word)

### approach 2: CapCut Browser Automation (secondary, $0, semi-automated)

advantages:
- industry-best auto-captions (animated, word-by-word highlight)
- trending effects and transitions
- template matching (apply viral templates)
- free at desktop tier

how it works:
1. playwright opens CapCut desktop app
2. imports raw video
3. applies auto-captions
4. applies template (if matching one exists)
5. adds text overlays per claude instructions
6. exports at target resolution/aspect ratio

limitations:
- needs CapCut desktop running on macOS
- fragile: UI changes break automation
- slower than ffmpeg (GUI rendering)
- can't run headless (needs display)

### approach 3: Remotion (existing, React-based video)

already set up in MEDIA/remotion/ — used for product videos.
good for: template-based branded content, consistent style.
not ideal for: raw AI clip editing.

### approach 4: Opus Clip API ($19/mo, when budget allows)

for: automatically extracting viral moments from longer content.
API available. send long video > get back short clips with scores.
best use case: YouTube long-form > auto-create shorts/reels.

## recommended implementation order

### phase 0 ($0): FFmpeg Auto-Editor
build `AUTOMATIONS/claude_video_editor.py` that:
1. takes input: raw clip path + niche + template type
2. runs whisper for transcription
3. generates ffmpeg commands based on template
4. outputs platform-ready files in 3 aspect ratios
5. moves to posting queue

### phase 1 ($0): CapCut Semi-Automation
add optional CapCut path for when animated captions are needed:
1. playwright imports to CapCut
2. applies auto-captions
3. exports
4. falls back to ffmpeg if CapCut is not available

### phase 2 ($19/mo): Opus Clip Integration
add Opus Clip API for:
1. long-form content auto-clipping
2. viral moment detection
3. score-based clip ranking

### phase 3 ($24/mo): Descript Integration
add Descript for:
1. text-based editing (edit transcript = edit video)
2. auto filler word removal
3. multi-track editing

## integration with existing systems

| system | integration point |
|--------|------------------|
| `ai_video_content_pipeline.py` | calls editor after generation |
| `perpetual_tool_researcher.py` | tracks editing tool rankings |
| `viral_content_scanner.py` | provides templates to editor |
| `auto_content_poster.py` | receives edited video for posting |
| `AI_VIDEO_CONTENT_TRACKER.csv` | tracks per-video performance |
| Capital Genesis | tool costs feed venture scoring |
