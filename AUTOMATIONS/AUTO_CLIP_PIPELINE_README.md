# Automated Clip Pipeline

**Turn long-form content (streams, podcasts, YouTube videos) into viral short clips automatically.**

## Quick Start

```bash
# Demo mode (see what it would do)
python3 auto_clip_pipeline.py --demo

# Process single video
python3 auto_clip_pipeline.py --url "https://youtube.com/watch?v=xxx"

# Batch process
python3 auto_clip_pipeline.py --urls-file urls.txt --max-clips 15

# Generate posting schedule
python3 clip_post_scheduler.py --input clips/clips_metadata.csv --days 14
```

## Installation

### Required Dependencies

```bash
# Core tools
pip install yt-dlp
brew install ffmpeg  # or apt-get install ffmpeg on Linux

# Python packages
pip install openai-whisper anthropic

# Optional: for better performance
pip install faster-whisper
```

### API Key Setup

```bash
# Set Anthropic API key for viral moment analysis
export ANTHROPIC_API_KEY="sk-ant-..."

# Or pass directly
python3 auto_clip_pipeline.py --url "..." --api-key "sk-ant-..."
```

## Pipeline Stages

### 1. Download (yt-dlp)
- Downloads video from URL (YouTube, Twitch, etc.)
- Saves to `clips/downloads/`
- Supports resume capability

### 2. Transcribe (Whisper)
- Transcribes audio with word-level timestamps
- Uses OpenAI Whisper base model
- Cached to `clips/transcripts/`

### 3. Analyze (Claude)
- AI-powered viral moment detection
- Identifies: funny moments, controversial statements, emotional peaks, quotable insights
- Scores each moment 1-10 for viral potential
- Generates caption/hook for each clip

### 4. Clip (FFmpeg)
- Extracts video segments
- Crops to vertical 9:16 (TikTok/Reels/Shorts)
- Burns in captions from transcript
- Center crop by default: maintains face in frame

### 5. Output
- MP4 clips ready to post
- Metadata CSV with all details
- SRT subtitle files

## Output Structure

```
clips/
├── downloads/          # Downloaded source videos
├── transcripts/        # Whisper transcripts (JSON)
├── clips/             # Final clips (MP4)
├── metadata/          # Working files
├── clips_metadata.csv # Master metadata CSV
└── processed_urls.log # Resume tracking
```

## Metadata CSV Format

| Column | Description |
|--------|-------------|
| clip_id | Unique identifier (video_id_clip01) |
| source_url | Original video URL |
| timestamp_start | Start time in source video (seconds) |
| timestamp_end | End time in source video (seconds) |
| duration | Clip duration (seconds) |
| transcript_snippet | Text from transcript |
| viral_score | AI score 1-10 |
| viral_reason | Why it would go viral |
| caption_text | Suggested caption/hook |
| output_path | Path to MP4 file |
| created_at | ISO timestamp |

## Usage Examples

### Single Video

```bash
python3 auto_clip_pipeline.py \
  --url "https://youtube.com/watch?v=dQw4w9WgXcQ" \
  --max-clips 10 \
  --min-duration 15 \
  --max-duration 60
```

### Batch Processing

Create `urls.txt`:
```
https://youtube.com/watch?v=xxx
https://youtube.com/watch?v=yyy
https://youtube.com/watch?v=zzz
```

Run:
```bash
python3 auto_clip_pipeline.py --urls-file urls.txt
```

### Skip Already Downloaded

```bash
python3 auto_clip_pipeline.py \
  --urls-file urls.txt \
  --skip-download
```

### Custom Output Directory

```bash
python3 auto_clip_pipeline.py \
  --url "..." \
  --output /path/to/output/
```

## Posting Scheduler

Generate optimal posting schedule for Buffer/Publer:

```bash
# Generate 7-day schedule
python3 clip_post_scheduler.py \
  --input clips/clips_metadata.csv \
  --output posting_schedule.csv \
  --days 7

# Multi-platform with custom start date
python3 clip_post_scheduler.py \
  --input clips/clips_metadata.csv \
  --platforms tiktok twitter instagram youtube \
  --days 14 \
  --start-date 2026-02-10

# Custom accounts
python3 clip_post_scheduler.py \
  --input clips/clips_metadata.csv \
  --accounts accounts.json
```

### Accounts JSON Format

```json
{
  "tiktok": ["@faithaccount", "@fitnessaccount"],
  "twitter": ["@printmaxxer"],
  "instagram": ["@printmaxxer"],
  "youtube": ["@printmaxxer"]
}
```

### Posting Schedule CSV

Output format for Buffer/Publer bulk upload:

| Column | Description |
|--------|-------------|
| clip_id | Reference to source clip |
| post_text | Caption with platform-specific formatting |
| media_path | Path to video file |
| platform | tiktok, twitter, instagram, youtube |
| account | Account handle |
| scheduled_time | ISO timestamp |
| viral_score | Reference score |
| caption | Original caption |

### Optimal Posting Times

**TikTok:** 9am, 12pm, 5pm, 7pm
**Twitter:** 8am, 12pm, 5pm, 9pm
**Instagram:** 9am, 12pm, 5pm, 7pm
**YouTube Shorts:** 2pm, 5pm, 8pm

## Claude Analysis Prompt

The pipeline uses this prompt for viral moment detection:

```
Analyze this transcript and identify the most viral-worthy moments. For each moment:
1. Exact timestamp range (start - end in seconds)
2. Why it would go viral (emotion, controversy, humor, insight, surprise)
3. Suggested caption/hook for the clip
4. Viral score 1-10

Look for: unexpected statements, emotional reactions, controversial takes,
genuinely funny moments, profound insights, audience interaction moments,
dramatic pauses followed by reveals, "wait what?" moments.

Prioritize moments that work as standalone clips (don't need context to understand).
```

## Fallback Mode

If Whisper or Anthropic unavailable, pipeline uses fallback:
- Evenly spaced clips across video
- 30-second duration
- Generic captions
- Still functional but less intelligent

## FFmpeg Vertical Crop

Center crop formula: `crop=ih*9/16:ih:(iw-ih*9/16)/2:0`

This:
- Calculates 9:16 aspect ratio based on input height
- Centers the crop horizontally
- Preserves face in frame for talking head content

## Caption Burning

Subtitles style:
- Font size: 24px
- Color: White with black outline
- Position: Bottom margin 20px
- Outline: 2px for readability
- No shadow (cleaner look)

## Rate Limiting

- 1 second between Claude API calls
- Prevents rate limit errors
- Configurable in code

## Resume Capability

Pipeline tracks processed URLs in `processed_urls.log`:
- Automatically skips already-processed videos
- Safe to re-run on same URL list
- Useful for batch jobs that get interrupted

## Performance Tips

### Speed Up Transcription

Use faster-whisper (optional):
```bash
pip install faster-whisper
```

Modify code to use `faster_whisper.WhisperModel` instead of `whisper.load_model`.

### Parallel Processing

For batch jobs, run multiple instances:
```bash
# Split urls.txt into chunks
split -l 10 urls.txt batch_

# Run in parallel (4 instances)
for file in batch_*; do
  python3 auto_clip_pipeline.py --urls-file $file --output clips_$file &
done
wait
```

### Disk Space

Estimate: `(video_length_hours * 2GB) + (clips * 50MB)`

Example: 2-hour podcast
- Download: 4GB
- Clips (10): 500MB
- Total: ~4.5GB

## Troubleshooting

### "yt-dlp not installed"
```bash
pip install yt-dlp
```

### "ffmpeg not installed"
```bash
brew install ffmpeg  # macOS
apt-get install ffmpeg  # Ubuntu
```

### "Whisper not installed"
```bash
pip install openai-whisper
```

### "Anthropic not installed"
```bash
pip install anthropic
export ANTHROPIC_API_KEY="sk-ant-..."
```

### "Download failed"
- Check URL is valid
- Try: `yt-dlp --list-formats [URL]` to see available formats
- Some platforms require cookies/auth

### "Transcription too slow"
- Use smaller Whisper model: `whisper.load_model("tiny")`
- Or use faster-whisper
- Or skip transcription: clips will be evenly spaced

### "Claude analysis failed"
- Check API key: `echo $ANTHROPIC_API_KEY`
- Check rate limits
- Pipeline will fallback to evenly-spaced clips

## Real-World Workflow

### Daily Streamer Clips

```bash
# 1. Download yesterday's stream
python3 auto_clip_pipeline.py \
  --url "https://youtube.com/watch?v=xxx" \
  --max-clips 20 \
  --output clips/daily/

# 2. Generate posting schedule
python3 clip_post_scheduler.py \
  --input clips/daily/clips_metadata.csv \
  --days 7 \
  --platforms tiktok twitter

# 3. Review clips (manual QA)
open clips/daily/clips/

# 4. Import posting_schedule.csv to Buffer

# 5. Repeat daily
```

### Podcast Repurposing

```bash
# Process all podcast episodes
python3 auto_clip_pipeline.py \
  --urls-file podcast_episodes.txt \
  --max-clips 5 \
  --min-duration 30 \
  --max-duration 90

# Focus on high viral scores
python3 clip_post_scheduler.py \
  --input clips/clips_metadata.csv \
  --days 30 \
  --platforms tiktok twitter instagram youtube
```

### YouTube Compilation Channel

```bash
# Scrape competitor videos
# Extract clips from multiple sources
python3 auto_clip_pipeline.py --urls-file competitors.txt

# Re-upload as compilations
# (Add transformative elements per fair use)
```

## Next Steps

1. **Run demo:** `python3 auto_clip_pipeline.py --demo`
2. **Test single video:** Pick a YouTube URL you have rights to
3. **Review output:** Check clips quality
4. **Generate schedule:** Run scheduler on metadata CSV
5. **Import to Buffer:** Bulk upload CSV
6. **Monitor performance:** Track which clips go viral

## Integration with PRINTMAXX

This pipeline integrates with:
- **Content farm methods** - Auto-generate viral clips
- **AI influencer personas** - Content for faceless accounts
- **Streamer clip monetization** - Daily clip factory
- **YouTube automation** - Compilation channel content
- **TikTok/Reels strategy** - Vertical short-form content

See `MONEY_METHODS/CONTENT_FARM/` for full strategy.

## License & Usage

- For personal/commercial use
- Respect platform terms of service
- Ensure you have rights to source content
- Add transformative elements where required
- FTC compliance: disclose if sponsored

## Support

Issues? Check:
1. This README troubleshooting section
2. `AUTOMATIONS/AUTO_CLIP_PIPELINE_README.md`
3. Run with `--demo` to diagnose
