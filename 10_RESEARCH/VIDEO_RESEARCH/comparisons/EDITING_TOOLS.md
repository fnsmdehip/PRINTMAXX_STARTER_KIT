# Video Editing & Post-Production Tools Comparison

last updated: 2026-03-21

## the problem

AI video tools output raw clips. to go viral, you need:
- auto-captions (animated, word-by-word highlight)
- hook text overlay (first 3 seconds)
- transitions between clips
- aspect ratio adaptation (9:16, 16:9, 1:1)
- background music mixing
- CTA overlays
- branding elements

## tool comparison

| tool | price | API | auto-captions | auto-splice | batch process | best for |
|------|-------|-----|---------------|-------------|---------------|----------|
| **FFmpeg** | FREE | CLI | via whisper | yes (scripted) | yes | automated pipelines, $0 budget |
| **CapCut** | FREE / $7.99 Pro | NO | best in class | yes (manual) | no | fancy captions, trending effects |
| **Descript** | $24/mo | partial | good | text-based | yes | podcast clips, talking head |
| **Opus Clip** | $19/mo | YES | good | auto-viral-detect | yes | long-form to shorts |
| **InShot** | FREE / $3.99 Pro | NO | basic | manual | no | quick mobile edits |
| **Remotion** | FREE (self-hosted) | React API | manual | programmatic | yes | template-based branded content |
| **Shotcut** | FREE | NO | no | manual | no | desktop editing, fallback |
| **DaVinci Resolve** | FREE | scripted | no | manual | yes (Fusion) | pro-grade, complex edits |

## recommended stack by budget

### $0/mo (current phase)
```
PRIMARY: FFmpeg + Whisper
  - whisper for transcription → .srt file
  - ffmpeg burns in captions, adds overlays, resizes
  - 100% scriptable, runs on cron
  - claude generates the ffmpeg command chain

SECONDARY: Remotion (ALREADY DEPLOYED at MEDIA/remotion/)
  - 40+ videos already generated, React-based
  - claude writes React template code → remotion renders MP4
  - best for: branded series, app promos, recurring formats, data-driven videos
  - can pull in dynamic data (stats, prices, rankings) and render automatically
  - example: "top 5 tools this week" → remotion template → video every week on cron

TERTIARY: CapCut MCP (free, for animated captions)
  - use for: animated word-by-word captions that ffmpeg can't do
  - CapCut MCP server lets claude control it programmatically
```

### $19/mo
```
ADD: Opus Clip
  - auto-detects viral moments in longer content
  - scores clips by virality potential
  - API available for automation
  - best ROI for repurposing YouTube → shorts
```

### $43/mo
```
ADD: Descript ($24/mo)
  - text-based editing (edit transcript = edit video)
  - auto-remove filler words
  - multi-track editing
  - great for podcast → clip pipelines
```

## automation capability matrix

| capability | FFmpeg | CapCut | Descript | Opus Clip |
|-----------|--------|--------|----------|-----------|
| run headless (cron) | YES | NO (GUI) | partial | YES (API) |
| batch processing | YES | NO | YES | YES |
| API/CLI control | YES (CLI) | NO | partial | YES |
| claude can generate commands | YES | playwright only | partial | YES |
| caption quality | basic styled | best (animated) | good | good |
| transition effects | basic | extensive | basic | auto-selected |
| template system | scripted | built-in | no | no |
| cost per video | $0 | $0 | ~$0.50 | ~$0.40 |

## ffmpeg auto-edit recipes

### recipe 1: add auto-captions
```bash
# transcribe with whisper
whisper input.mp4 --model small --output_format srt --output_dir .

# burn captions into video
ffmpeg -i input.mp4 -vf "subtitles=input.srt:force_style='FontName=Arial,FontSize=22,Bold=1,PrimaryColour=&H00FFFFFF,OutlineColour=&H00000000,Outline=2,Alignment=2,MarginV=40'" output.mp4
```

### recipe 2: add hook text overlay
```bash
ffmpeg -i input.mp4 -vf "drawtext=text='THE SECRET NOBODY TELLS YOU':fontfile=/System/Library/Fonts/Helvetica.ttc:fontsize=48:fontcolor=white:borderw=3:bordercolor=black:x=(w-tw)/2:y=h/4:enable='between(t,0,3)'" output.mp4
```

### recipe 3: resize for TikTok (9:16)
```bash
ffmpeg -i input.mp4 -vf "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2:black" -c:a copy output_tiktok.mp4
```

### recipe 4: add background music
```bash
ffmpeg -i video.mp4 -i music.mp3 -filter_complex "[1:a]volume=0.15[bg];[0:a][bg]amix=inputs=2:duration=first:dropout_transition=2[out]" -map 0:v -map "[out]" output.mp4
```

### recipe 5: full pipeline (captions + hook + resize + music)
```bash
# step 1: transcribe
whisper input.mp4 --model small --output_format srt

# step 2: burn captions + hook text
ffmpeg -i input.mp4 -vf "subtitles=input.srt:force_style='FontSize=22,Bold=1,Alignment=2,MarginV=40',drawtext=text='WATCH THIS':fontsize=48:fontcolor=white:borderw=3:bordercolor=black:x=(w-tw)/2:y=h/4:enable='between(t,0,3)'" captioned.mp4

# step 3: resize for tiktok
ffmpeg -i captioned.mp4 -vf "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2" tiktok.mp4

# step 4: add background music
ffmpeg -i tiktok.mp4 -i bg_music.mp3 -filter_complex "[1:a]volume=0.12[bg];[0:a][bg]amix=inputs=2:duration=first[out]" -map 0:v -map "[out]" final.mp4
```

## capcut browser automation (playwright)

```python
# concept — needs CapCut desktop running
from playwright.sync_api import sync_playwright

def capcut_auto_edit(video_path, caption_style="trending"):
    with sync_playwright() as p:
        # connect to running CapCut via CDP or launch
        # 1. import video
        # 2. apply auto-captions (CapCut's are best)
        # 3. select caption style
        # 4. export at target resolution
        pass  # implementation depends on CapCut UI version
```

note: CapCut automation is fragile. UI changes break it. always have ffmpeg as fallback.
