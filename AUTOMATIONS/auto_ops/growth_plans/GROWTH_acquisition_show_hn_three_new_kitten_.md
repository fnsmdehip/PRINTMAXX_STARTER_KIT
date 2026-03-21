# Growth Plan: [ACQUISITION] Show HN: Three new Kitten TTS models – smalles

**Created:** 2026-03-21 12:40
**Venture:** CONTENT
**Budget Tier:** FREE
**Revenue Est:** $0 direct / $50-300/mo indirect via increased faceless content output volume

---

## Tactics

1. Use zero-cost local TTS to produce faceless voiceover content at 10x volume — no per-minute API fees
2. Batch voiceover all 324 pending content queue items overnight via cron
3. Layer Kitten TTS voices across 3 niches (faith, fitness, tech) with distinct voices per brand to avoid detection
4. Build 'voice sample' lead magnet showing TTS quality — captures indie hacker / dev audience as content hook

## Budget Tier Strategies

### FREE
Run Kitten TTS locally via Python — model is <25MB, downloads once, zero marginal cost per voiceover. Batch all existing CONTENT/social/posting_queue scripts into audio files. Use ffmpeg to merge with stock video. Post faceless content across TikTok/YT/IG Reels.

### LOW
$0-50/mo — Buy a few Envato stock video clips ($20) as background for voiceover videos. Use generated content as top-of-funnel for streak app downloads.

### MID
$50-200/mo — Commission 5-10 UGC-style scripts per week, auto-voice them, distribute at scale. A/B test Kitten TTS voices vs ElevenLabs to validate quality parity.

## Daily Actions

- [ ] pip install kokoro-onnx or equivalent Kitten TTS Python binding (check HN thread for repo URL)
- [ ] Download smallest Kitten model (<25MB) to AUTOMATIONS/models/kitten_tts/
- [ ] Write kitten_tts_voiceover_pipeline.py: reads scripts from CONTENT/social/posting_queue/*.txt, generates .mp3 per script, writes to CONTENT/social/audio_queue/
- [ ] Test with 3 sample scripts — verify audio quality vs ElevenLabs
- [ ] Add cron entry: 0 7 * * * python3 AUTOMATIONS/kitten_tts_voiceover_pipeline.py --batch
- [ ] Wire audio paths back into posting_queue entries so distribution agents know audio is ready
- [ ] Check if existing real-time local TTS script can be ENHANCED with Kitten models instead of creating new script

## Tooling

```json
{
  "browser": "none",
  "email": "none",
  "content": "kitten_tts + ffmpeg + content_factory",
  "tts_model": "kitten-tts (huggingface or github, <25MB, local)",
  "audio_merge": "ffmpeg (already installed)",
  "queue": "CONTENT/social/posting_queue/"
}
```
