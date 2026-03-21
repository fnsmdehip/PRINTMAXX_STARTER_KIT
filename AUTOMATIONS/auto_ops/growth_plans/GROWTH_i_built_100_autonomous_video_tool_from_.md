# Growth Plan: I built 100% autonomous video tool from idea to publishing o

**Created:** 2026-03-21 12:40
**Venture:** CONTENT
**Budget Tier:** FREE
**Revenue Est:** $50-200/mo

---

## Tactics

1. Batch 10 concepts per niche per run via claude -p — amortize ideation cost across all niches
2. Inject trending topics from content_trend_pipeline.py before scripting — algorithm-aware hooks
3. Route all scripts through engagement_bait_converter.py hook optimizer before production
4. Cross-post TikTok + YT Shorts + IG Reels in parallel via Playwright — 3x reach zero extra cost
5. Pin best-performing video captions to WINNING_CONTENT_STRUCTURES.csv for self-reinforcing loop
6. Niche rotation: faith, fitness, tech — 1 video per niche per day via config param

## Budget Tier Strategies

### FREE
Claude Max for scripting, ffmpeg + Pillow for assembly, Playwright for posting, content_trend_pipeline for trending topics — complete pipeline at $0/mo

### LOW
$5-15/mo: ElevenLabs Starter for natural TTS voiceover instead of gTTS; upgrades retention significantly

### MID
$50-100/mo: HeyGen or Synthesia for AI presenter face-cam style — higher trust, higher CPM niche targeting

## Daily Actions

- [ ] Audit auto_clip_service.py — check if ideation + multi-platform posting gaps exist
- [ ] If gaps: add ideation phase calling claude -p with niche + trend injection as params
- [ ] Implement ffmpeg text-on-video shorts renderer (fastest format, no face required)
- [ ] Wire Playwright MCP for TikTok + YT Shorts posting — reuse existing browser auth
- [ ] Add niche config array (faith/fitness/tech) so single script covers all CONTENT ventures
- [ ] Schedule cron 7 AM daily — generate and post 3 videos across niches
- [ ] Wire published video metadata into CONTENT_PERFORMANCE_LOG.csv for feedback loop
- [ ] Add KPI entry: videos_published_today + platform_views_7d rolling average

## Tooling

```json
{
  "browser": "playwright",
  "email": "none",
  "content": "claude -p + ffmpeg + content_trend_pipeline.py + engagement_bait_converter.py"
}
```
