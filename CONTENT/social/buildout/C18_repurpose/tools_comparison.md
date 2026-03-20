# C18 Viral Content Repurposer, Tools Comparison
# Repurpose.io vs Manual vs Custom Scripts

## Decision Framework

| Situation | Best Option |
|-----------|------------|
| Budget under $30/mo | Manual workflow |
| 5-20 videos/month | Repurpose.io Starter |
| 20+ pieces/month | Repurpose.io Pro or custom scripts |
| Want full control + no subscriptions | Custom Python scripts |
| Non-technical, needs UI | Repurpose.io |
| Technical, wants API integration | Custom scripts |

---

## Option 1: Repurpose.io

**Pricing:**
- Starter: $25/mo, 5 channels, 100 posts/mo
- Professional: $49/mo, unlimited channels, unlimited posts
- Business: $99/mo, white-label, multiple workspaces

**What it does:**
- Watches a source channel (TikTok, YouTube, RSS)
- Auto-downloads new content when published
- Removes watermarks (TikTok → other platforms)
- Uploads to connected destination platforms
- Adds preset captions

**Supported workflows:**
- TikTok → IG Reels (watermark removed) ✓
- TikTok → YouTube Shorts ✓
- TikTok → Facebook Reels ✓
- TikTok → Twitter/X ✓
- TikTok → Pinterest ✓
- YouTube → Podcast (audio extraction) ✓
- Podcast → YouTube (static image video) ✓
- Podcast → YouTube Shorts (auto-clips from long audio), limited
- Twitter → LinkedIn ✓

**Limitations:**
- Does NOT generate captions per-platform (you set one preset)
- No AI caption rewriting, same caption everywhere
- Does NOT clip long-form into shorts (just crosspost)
- No blog/newsletter automation
- Limited to supported platforms

**Best for:** Crossposting the exact same video to 4 short-form platforms automatically. Set-and-forget for TikTok → everywhere else.

**Monthly output at Starter ($25/mo):**
- 4 short-form clips × 4 platforms = 16 posts/week → 64/month
- Well within 100 post limit

**ROI math:**
- Save 1 hour/week on manual uploads = 4 hours/month
- At $25/hr effective rate = $100/mo value
- Net: $75/mo positive ROI at Starter tier

---

## Option 2: Manual Workflow (Free)

**Stack:**
- CapCut (free, desktop or web), clip editing + captions
- Buffer (free, 3 channels, 10 posts each), scheduling
- Later (free, 1 platform), IG Reels scheduling
- TikTok mobile, native upload with duplication to others
- Beehiiv (free), newsletter scheduling
- YouTube Studio, video upload

**Workflow time per piece:**
- Edit 4 clips in CapCut: 20 min
- Write 4 captions: 10 min
- Upload to TikTok: 5 min
- Upload to IG Reels: 5 min
- Upload to YouTube Shorts: 5 min
- Upload to FB Reels (Business Suite crosspost from IG): 2 min
- Schedule thread on X: 5 min
- Schedule LinkedIn: 3 min
- Total per piece: ~55 min/week

**Limitation:** Fully manual. No automation. Error-prone at scale. TikTok watermark requires manual removal before crossposting (re-export without watermark).

**TikTok watermark removal (free):**
- Save TikTok to camera roll WITHOUT posting first, no watermark added yet
- OR use SnapTik.app / SSSTik.io to download and strip watermark
- OR just don't post to TikTok first, post elsewhere, then TikTok last

**Best for:** Starting out. Under 5 videos/month. Zero budget.

---

## Option 3: Custom Python Scripts

**Stack:**
- `yt-dlp`, download from YouTube, TikTok, any platform
- `ffmpeg`, clip cutting, format conversion, watermark removal
- `whisper`, transcription (OpenAI Whisper, local)
- `anthropic` SDK, Claude API for caption generation per platform
- `tiktok-uploader`, `instagrapi`, `pytube`, `google-api-python-client`, platform APIs

**Example pipeline script (conceptual):**

```python
# repurpose_pipeline.py
import subprocess
import anthropic
import json
from pathlib import Path

def process_video(source_url: str, topic: str):
    # 1. Download source
    subprocess.run(["yt-dlp", "-o", "originals/%(title)s.%(ext)s", source_url])

    # 2. Transcribe
    subprocess.run(["whisper", "originals/video.mp4", "--output_format", "txt"])

    transcript = Path("originals/video.txt").read_text()

    client = anthropic.Anthropic()

    # 3. Generate platform-specific captions
    captions = {}
    platforms = ["tiktok", "instagram", "twitter", "linkedin", "newsletter"]

    for platform in platforms:
        response = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=500,
            messages=[{
                "role": "user",
                "content": f"Write a {platform} caption for this content. Topic: {topic}. Transcript: {transcript[:2000]}. Platform rules: {get_platform_rules(platform)}"
            }]
        )
        captions[platform] = response.content[0].text

    # 4. Cut clips with ffmpeg
    timestamps = [(0, 30), (90, 150), (180, 240), (300, 360)]
    for i, (start, end) in enumerate(timestamps):
        subprocess.run([
            "ffmpeg", "-i", "originals/video.mp4",
            "-ss", str(start), "-to", str(end),
            "-vf", "scale=1080:1920,setsar=1",  # 9:16 crop
            f"clips/clip_{i+1}.mp4"
        ])

    # 5. Add captions (burn-in with ffmpeg)
    for i in range(len(timestamps)):
        subprocess.run([
            "ffmpeg", "-i", f"clips/clip_{i+1}.mp4",
            "-vf", f"drawtext=text='{captions['tiktok'][:50]}':fontsize=48:fontcolor=white:box=1:boxcolor=black",
            f"clips/clip_{i+1}_captioned.mp4"
        ])

    return captions

def get_platform_rules(platform: str) -> str:
    rules = {
        "tiktok": "150 chars max, 3-5 hashtags, hook in first line",
        "instagram": "200 chars, 5-8 hashtags, call to action, no links",
        "twitter": "280 chars, no hashtags except 1, consequence-first hook",
        "linkedin": "200 chars in body, put link in comments, ask a question",
        "newsletter": "subject line: 6-8 words with number, body: 150 word summary"
    }
    return rules.get(platform, "")
```

**What custom scripts can do that tools cannot:**
- Generate unique captions per platform using Claude API
- Auto-clip based on transcript analysis (find natural breakpoints)
- Integrate with existing PRINTMAXX automation stack
- Batch process 50 videos overnight
- Log everything to LEDGER/ CSVs
- Trigger on new YouTube upload via RSS feed watcher

**Cost:**
- Server: $5-15/mo (DigitalOcean droplet)
- Claude API: ~$0.03 per video processed (Haiku)
- whisper: free (local) or $0.006/min (OpenAI API)
- Total: ~$10-20/mo for 20 videos + unlimited clips

**Time investment:** 8-12 hours initial build, then 0 manual time

**Best for:** Technical founder who already has automation pipeline running. Makes sense when processing 20+ pieces/month.

---

## Full Tool Stack Comparison Table

| Tool | Cost | Clip Cutting | Watermark Remove | Caption AI | Auto-Upload | Scheduling |
|------|------|-------------|-----------------|------------|-------------|-----------|
| Repurpose.io Starter | $25/mo | No | Yes | No | Yes (4 platforms) | Yes |
| Repurpose.io Pro | $49/mo | No | Yes | No | Unlimited | Yes |
| OpusClip | $29/mo | Yes (AI) | Yes | Basic | No | Yes |
| Descript | $24/mo | Yes | No | Transcription | No | No |
| CapCut + Buffer | $0-15/mo | Manual | Manual | No | No | Yes (Buffer) |
| Custom Python stack | $10-20/mo | ffmpeg | ffmpeg | Claude API | Limited | Cron |
| MindStudio workflow | $29/mo | No | No | Yes | No | No |

---

## Caption AI Tools

| Tool | Cost | Quality | Speed |
|------|------|---------|-------|
| Claude API (Haiku) | $0.003/1K tokens | Best, matches voice | Fast |
| ChatGPT API | $0.002/1K tokens | Good | Fast |
| Opus.pro | $29/mo | Okay, preset prompts | Fast |
| Repurpose.io built-in | Included | Basic, repetitive | Auto |

**Recommendation:** Use Claude Haiku via API for all caption generation. At $0.003/1K tokens, processing 20 captions per video costs under $0.05. Full video repurpose costs under $0.10 total in API fees.

---

## Recommended Stack by Budget

### $0/mo (manual)
- CapCut free (clips + captions)
- Buffer free (3 platforms, 10 posts each)
- Manual TikTok upload first, then crosspost via meta business suite
- Time cost: 55 min/piece

### $25/mo (semi-automated)
- Repurpose.io Starter (TikTok → 4 platforms auto)
- CapCut for manual clip cutting
- Claude.ai chat for caption writing
- Time cost: 20 min/piece

### $50/mo (mostly automated)
- Repurpose.io Pro ($49), unlimited crossposting
- OpusClip ($29), auto-clip extraction from long-form
- Claude API ($5 cap), per-platform captions
- Time cost: 10 min/piece

### $15/mo (custom scripts)
- VPS ($10/mo)
- Claude API ($5/mo cap)
- yt-dlp + ffmpeg + whisper (free, local)
- Custom Python pipeline
- Time cost: 0 min/piece after build
