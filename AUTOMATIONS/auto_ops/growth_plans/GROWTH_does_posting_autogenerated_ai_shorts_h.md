# Growth Plan: Does posting auto-generated AI Shorts (history, scary storie

**Created:** 2026-03-20 13:50
**Venture:** CONTENT
**Budget Tier:** FREE
**Revenue Est:** $50-300/mo

---

## Tactics

1. Completion rate optimization: front-load hook in first 1.5s (TikTok algo rewards >80% watch-through)
2. 1-to-20 repurpose: same script → vertical short + horizontal mid-form + carousel + thread
3. Niche rotation: scary at night, history AM, fun facts midday — match audience active hours
4. Comment bait CTAs: end every video with polarizing question to boost engagement signals
5. Cross-post to 3+ platforms from single render — marginal cost zero

## Budget Tier Strategies

### FREE
Organic posting 3x/day, engagement farming via comment bait CTAs, cross-platform repurposing, hashtag rotation, duet/stitch trending sounds

### LOW
$10-30/mo boost top-performing shorts on TikTok Promote for initial traction

### MID
$50-100/mo TikTok ads on proven winners, micro-influencer collabs for channel shoutouts

## Daily Actions

- [ ] Wire into existing CONTENT venture — no new venture needed
- [ ] Build ai_shorts_content_pipeline.py using existing video_factory + Remotion + edge-tts
- [ ] Configure niche rotation: history, scary stories, paranormal, fun facts (4 content buckets)
- [ ] Add cron 7 AM daily to generate 3 shorts and queue for posting
- [ ] Route output to content_multiplier for cross-platform repurposing (TikTok + YT Shorts + IG Reels)
- [ ] Track KPIs: videos/day, views, completion rate, subscriber growth in KPI_DASHBOARD

## Tooling

```json
{
  "browser": "none",
  "email": "none",
  "content": "content_factory + video_factory (Remotion) + edge-tts (free) + existing auto-clip pipeline"
}
```
