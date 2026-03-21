# Growth Plan: # Faceless/AI YouTube Channel Due Diligence Report  **Date:*

**Created:** 2026-03-20 18:10
**Venture:** CONTENT
**Budget Tier:** FREE
**Revenue Est:** $100-400/mo per channel after 3-6 months consistent posting (discounted from typical $500-2K claims due to YouTube crackdown risk and CPM variance)

---

## Tactics

1. Target high-CPM niches first (finance $15-30, tech $8-15, health $6-12) to maximize early revenue per view
2. Cross-post Shorts to TikTok and IG Reels for discovery funnel back to YouTube long-form
3. Use comment engagement warming on competitor videos in same niche (not spam, genuine value-add comments)
4. Playlist SEO stacking — group videos into keyword-rich playlists for suggested video algorithm boost
5. Vary posting times, video lengths, and intro styles to avoid YouTube inauthentic content detection patterns

## Budget Tier Strategies

### FREE
Organic SEO titles, cross-post Shorts to TikTok/IG, comment engagement on competitor videos, playlist stacking, community posts for retention signals

### LOW
$20-50/mo for premium stock footage subscription (Storyblocks) to differentiate from pure AI slop; $10/mo for better TTS voices

### MID
$100-150/mo for thumbnail A/B testing tools + small YouTube ad spend on best-performing videos to seed initial views and trigger algorithm recommendation

## Daily Actions

- [ ] 1. Research top 5 high-CPM faceless niches using existing alpha + YouTube API data
- [ ] 2. Build script template library in Claude — 10 proven structures per niche (listicle, explainer, comparison, story)
- [ ] 3. Wire edge-tts (free Microsoft TTS, pip install edge-tts) for natural voiceover generation with speed/pitch variation
- [ ] 4. Build Remotion video template with: voiceover track + stock footage + text overlays + transitions
- [ ] 5. Create thumbnail generator using existing image_factory (Playwright HTML-to-image)
- [ ] 6. Wire YouTube Data API v3 for automated upload (free quota: 10K units/day, ~6 uploads)
- [ ] 7. Schedule cron MWF 8AM: generate batch of 3 videos, queue uploads
- [ ] 8. Add crackdown mitigation: randomize intro styles, vary video length ±15%, mix human-edited clips every 5th video
- [ ] 9. Cross-post Shorts extraction to TikTok/IG via existing content_repurposer.py
- [ ] 10. Track CPM, views, subs weekly — kill channel if <$50/mo after 90 days, double down if >$200/mo

## Tooling

```json
{
  "browser": "playwright for upload automation",
  "email": "none",
  "content": "claude -p for scripts, edge-tts for voiceover, remotion for assembly, ffmpeg for post-processing"
}
```
