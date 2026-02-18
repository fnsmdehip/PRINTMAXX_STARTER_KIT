# Clip Pipeline Quick Start

**Get viral clips from long-form content in 5 minutes.**

## 1. Install Dependencies (One Time)

```bash
# Install yt-dlp
pip install yt-dlp

# Install ffmpeg
brew install ffmpeg  # macOS
# or: apt-get install ffmpeg  # Linux

# Install Whisper (optional but recommended)
pip install openai-whisper

# Install Anthropic (for AI analysis)
pip install anthropic

# Set API key
export ANTHROPIC_API_KEY="sk-ant-api03-..."
# Add to ~/.zshrc or ~/.bashrc to persist
```

## 2. Test Installation

```bash
cd AUTOMATIONS
python3 auto_clip_pipeline.py --demo
```

You should see:
```
✅ yt-dlp: installed
✅ ffmpeg: installed
✅ whisper: installed
✅ anthropic: installed
✅ API key: set
```

## 3. Process Your First Video

### Option A: Single Video

```bash
python3 auto_clip_pipeline.py \
  --url "https://youtube.com/watch?v=YOUR_VIDEO_ID"
```

### Option B: Batch Processing

Edit `example_urls.txt` with your URLs, then:

```bash
python3 auto_clip_pipeline.py --urls-file example_urls.txt
```

## 4. Check Output

```bash
# View clips
open clips/clips/

# View metadata
cat clips/clips_metadata.csv
```

## 5. Generate Posting Schedule

```bash
python3 clip_post_scheduler.py \
  --input clips/clips_metadata.csv \
  --output posting_schedule.csv \
  --days 7 \
  --platforms tiktok twitter
```

## 6. Import to Buffer/Publer

1. Open Buffer/Publer
2. Go to bulk upload
3. Import `posting_schedule.csv`
4. Review and approve

## That's It!

You now have:
- ✅ Viral clips extracted
- ✅ Vertical format (9:16)
- ✅ Captions burned in
- ✅ Posting schedule optimized
- ✅ Ready for distribution

## Common Use Cases

### Daily Streamer Clips

```bash
# Add to crontab for daily execution
0 2 * * * cd /path/to/AUTOMATIONS && python3 auto_clip_pipeline.py --urls-file daily_streams.txt
```

### Podcast Repurposing

```bash
# Process all episodes
python3 auto_clip_pipeline.py \
  --urls-file podcast_episodes.txt \
  --max-clips 5 \
  --min-duration 30 \
  --max-duration 90
```

### Multi-Account Distribution

```bash
# Use custom accounts
python3 clip_post_scheduler.py \
  --input clips/clips_metadata.csv \
  --accounts example_accounts.json \
  --days 14
```

## Troubleshooting

### "yt-dlp not installed"
```bash
pip install yt-dlp
```

### "ffmpeg not installed"
```bash
brew install ffmpeg  # macOS
sudo apt-get install ffmpeg  # Linux
```

### "Whisper not installed"
```bash
pip install openai-whisper
# Or skip: pipeline works without it (less intelligent clip selection)
```

### "No API key"
```bash
export ANTHROPIC_API_KEY="sk-ant-..."
# Or pass directly: --api-key "sk-ant-..."
```

### Download Fails

Some platforms require authentication:
```bash
# Add cookies
yt-dlp --cookies-from-browser chrome [URL]

# Then use in pipeline (modify code to add --cookies flag)
```

## Next Steps

- Read full docs: `AUTO_CLIP_PIPELINE_README.md`
- Integrate with content farm strategy
- Set up automated daily runs
- Monitor which clips go viral
- Double down on winning formats

## Performance Tips

- Use `faster-whisper` for 3x faster transcription
- Run multiple instances in parallel for batch jobs
- Cache downloads to skip re-downloading

## Legal Note

- Ensure you have rights to source content
- Add transformative elements where required
- Respect platform terms of service
- FTC disclosure for sponsored content
