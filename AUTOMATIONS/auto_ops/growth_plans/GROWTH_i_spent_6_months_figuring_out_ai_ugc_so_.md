# Growth Plan: I spent 6 months figuring out AI UGC so you don't have to.



**Created:** 2026-03-20 13:50
**Venture:** CONTENT
**Budget Tier:** FREE
**Revenue Est:** $500-3000/mo

---

## Tactics

1. Multi-account structure: 3-5 themed accounts per niche (not branded, topic-specific personas)
2. First 2 seconds = pattern interrupt (text overlay + movement + direct address)
3. Completion rate optimization: 15-30sec clips, open loop at start, payoff at end
4. Cross-post winners from TikTok to IG Reels within 4h (platform lag arbitrage)
5. DM share bait: end videos with 'send this to someone who...' CTA (IG algorithm priority signal)
6. Comment seeding: first comment is a controversial take or question to trigger engagement
7. Sound trend hijacking: use trending sounds within first 48h of viral detection
8. Engagement warming: 15min manual engagement before and after each post (like/comment in niche)

## Budget Tier Strategies

### FREE
OSS AI avatar pipeline (SadTalker+Bark+ffmpeg), multi-account organic posting, trending sound hijacking, engagement warming protocol, cross-platform repurposing, comment seeding from alt accounts

### LOW
$20-50/mo for proxy rotation (SOAX residential) to maintain multi-account without bans, basic analytics tooling

### MID
$100-200/mo for HeyGen/Synthesia API credits (higher quality avatars), GoLogin for account management, spark ads on top performers

## Daily Actions

- [ ] 1. Install OSS AI UGC stack: pip3 install TTS sadtalker wav2lip (or use Replicate free tier for GPU inference)
- [ ] 2. Create ai_ugc_content_farm.py with DAG phases: trend scan → script gen → video render → distribute → analyze
- [ ] 3. Build 10 UGC script templates optimized for completion rate (consequence-first hooks from procedural memory)
- [ ] 4. Set up 3 TikTok accounts per niche (productivity, faith, finance) with unique personas and posting schedules
- [ ] 5. Wire into existing content_factory chain: UGC clips feed engagement_bait_converter for text repurposing
- [ ] 6. Add cron 5 AM daily: generate batch of 3-5 clips, queue for optimal posting times
- [ ] 7. Wire analytics scraper to flag winners (>10K views/24h) for format replication in next cycle
- [ ] 8. Ralph loop for iterative improvement: each cycle analyzes what worked and adjusts script templates

## Tooling

```json
{
  "browser": "playwright for scraping + posting automation",
  "email": "none",
  "content": "claude -p for scripts, Bark/Coqui TTS, SadTalker/Wav2Lip for avatar, ffmpeg for assembly, whisper for captions"
}
```
