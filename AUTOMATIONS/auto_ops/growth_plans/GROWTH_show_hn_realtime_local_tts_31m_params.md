# Growth Plan: Show HN: Real-time local TTS (31M params, 5.6x CPU, voice cl

**Created:** 2026-03-20 18:09
**Venture:** CONTENT
**Budget Tier:** FREE
**Revenue Est:** $50-300/mo

---

## Tactics

1. Post Show-HN-style thread on Twitter showing before/after (text vs narrated video) to attract dev audience
2. List voiceover gig on Fiverr using AI-generated samples as portfolio
3. Cross-post narrated content across TikTok/YouTube Shorts/IG Reels simultaneously
4. Contribute improvements upstream to the OSS repo for backlink + credibility

## Budget Tier Strategies

### FREE
Narrate existing content queue with local TTS, post faceless narrated shorts on all platforms, list Fiverr voiceover gig with AI samples, repurpose into podcast-style clips

### LOW
$10-30/mo for better voice samples via Resemble.ai free tier or ElevenLabs starter if local quality insufficient for premium gigs

### MID
$50-100/mo for Fiverr Seller Plus visibility boost + promoted TikTok narrated clips

## Daily Actions

- [ ] Clone the VITS-ONNX repo and install onnxruntime (CPU only, no GPU needed)
- [ ] Download pretrained 31M param model weights + Resemblyzer speaker embeddings
- [ ] Build local_tts_pipeline.py wrapping model inference with CLI: --text, --voice, --output
- [ ] Extract 3-5 speaker embeddings from sample voices for variety
- [ ] Wire into video_factory.py: content script → TTS audio → Remotion render → narrated short
- [ ] Add cron job: daily at 5 AM pull top 3 scripts from CONTENT/social/posting_queue/ and narrate
- [ ] Create Fiverr gig listing using generated samples as portfolio (PRODUCTS/listings/)
- [ ] Track output quality and render success rate in LEDGER/AI_VIDEO_CONTENT_TRACKER.csv

## Tooling

```json
{
  "browser": "none",
  "email": "none",
  "content": "content_factory + video_factory (Remotion) + local ONNX TTS"
}
```
