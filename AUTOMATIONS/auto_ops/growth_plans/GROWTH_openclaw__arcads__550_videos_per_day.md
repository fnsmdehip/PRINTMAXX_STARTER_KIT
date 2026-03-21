# Growth Plan: OpenClaw + Arcads = 550 videos per day

Fully-realistic UGC 

**Created:** 2026-03-20 18:35
**Venture:** CONTENT
**Budget Tier:** FREE
**Revenue Est:** $100-400/mo

---

## Tactics

1. Cross-post UGC across all 3 niches (faith/fitness/tech) with niche-specific hooks
2. A/B test hook variants in first 2 seconds (IG DM shares = new priority metric per P0 stack)
3. Repurpose top-performing UGC into carousel stills and quote graphics
4. Use completion-rate optimization (TikTok algo shift per P0 stack) — keep videos under 30s
5. Multi-account cross-promotion: post same UGC with different hooks across niche accounts

## Budget Tier Strategies

### FREE
Remotion + Claude Max + free TTS (edge-tts/piper) + organic posting across accounts. 10-30 videos/day at $0. Hub-and-spoke repurposing (1 video → 20 platform-specific cuts).

### LOW
$0-50/mo: Upgrade to ElevenLabs starter for better voice quality. Boost top 3 performing UGC posts/week ($2-5 each).

### MID
$50-200/mo: ElevenLabs pro + stock footage library sub. Run UGC as paid ads on TikTok/IG ($5-10/day on winners only).

## Daily Actions

- [ ] 1. Build ai_ugc_video_factory.py using Remotion + Claude for script gen + edge-tts for voiceover
- [ ] 2. Wire into existing chain_openclaw__arcads__550_videos_per_day (enhance, don't duplicate)
- [ ] 3. Create 3 niche-specific UGC templates in MEDIA/video_templates/ (faith, fitness, tech)
- [ ] 4. DAG phase 1: Claude generates 10 scripts/niche from trending alpha + pain points
- [ ] 5. DAG phase 2: edge-tts renders voiceover, Remotion renders video with template
- [ ] 6. DAG phase 3: Queue to CONTENT/social/posting_queue/ with platform-specific cuts
- [ ] 7. Add cron 7:30 AM daily for batch generation
- [ ] 8. Track in AI_VIDEO_CONTENT_TRACKER.csv (already exists in LEDGER)
- [ ] 9. A/B test: UGC video posts vs static image posts — measure engagement delta
- [ ] 10. Skip OpenClaw entirely (security risk) — use native Claude + Remotion stack

## Tooling

```json
{
  "browser": "playwright_mcp_for_trend_scraping",
  "email": "none",
  "content": "remotion_video_factory+content_repurposer+engagement_bait_converter"
}
```
