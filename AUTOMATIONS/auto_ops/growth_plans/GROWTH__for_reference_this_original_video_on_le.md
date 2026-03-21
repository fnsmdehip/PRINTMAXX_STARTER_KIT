# Growth Plan:  for reference this original video on left has 525.1k views 

**Created:** 2026-03-20 18:09
**Venture:** CONTENT
**Budget Tier:** FREE
**Revenue Est:** $200-800/mo

---

## Tactics

1. Clone ONLY videos with 100K+ views (proven format = lower risk)
2. A/B test hook variants: keep proven structure, swap first 2 seconds
3. Cross-post each clone to 3+ platforms with native aspect ratios
4. Ride existing trends by cloning UGC that uses trending audio
5. Stack monetization: same video promotes app + affiliate link in bio
6. Engagement warm: seed initial comments from alt accounts within 15 min of posting

## Budget Tier Strategies

### FREE
yt-dlp + whisper + Claude script gen + ffmpeg/Remotion assembly. Post organically to warmed accounts. Target 2 videos/week across TikTok, IG Reels, X. Use trending audio from royalty-free sources.

### LOW
$20-40/mo for HeyGen or D-ID credits for AI avatar UGC (more authentic than text-overlay). Boost top performer $5-10 per video on TikTok Promote.

### MID
$100-150/mo for Spark Ads on TikTok using organic UGC clones as ad creatives. Retarget viewers who watched 75%+ with app install CTA.

## Daily Actions

- [ ] 1. Build ugc_clone_pipeline.py with 5-phase DAG (discover→analyze→clone→produce→distribute)
- [ ] 2. Phase 1 scraper: use yt-dlp to download top UGC ads from TikTok/IG (filter 100K+ views, app/SaaS niche)
- [ ] 3. Phase 2 analyzer: whisper transcribe → Claude extracts {hook_type, pain_point, demo_moment, cta_style, duration, pacing}
- [ ] 4. Phase 3 cloner: Claude rewrites script substituting our product (PrayerLock, FocusLock, Scripture Streak) while preserving proven structure
- [ ] 5. Phase 4 producer: Remotion renders video with text overlays + captions, or ffmpeg assembles from screen recordings + voiceover
- [ ] 6. Phase 5 distributor: output to CONTENT/social/posting_queue/ with platform variants (9:16 TikTok, 9:16 Reels, 16:9 X)
- [ ] 7. Wire into existing chain_i_spent_6_months_figuring_out_ai_ugc_so_ for UGC best practices
- [ ] 8. Cron Mon+Thu 7AM to refresh viral UGC library and generate new clones
- [ ] 9. Track: views per clone, CTR to app, installs attributed. Kill format if <1K views avg after 5 posts

## Tooling

```json
{
  "browser": "playwright for scraping viral examples",
  "email": "none",
  "content": "whisper + claude_script_gen + remotion/ffmpeg + existing auto_clip_service.py"
}
```
