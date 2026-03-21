# Growth Plan:  organic affiliates are still so behind on this ai video stu

**Created:** 2026-03-20 23:12
**Venture:** CONTENT
**Budget Tier:** FREE
**Revenue Est:** $300-1200/mo affiliate commissions within 60 days at scale; $500-2000/mo if video template pack listed on Gumroad

---

## Tactics

1. Target affiliate offers with video-friendly products (supplements, software, physical goods) — these convert 2-4x better on video vs static
2. Use completion-rate optimization: hook must deliver payoff by second 3 per TikTok algo shift in priority stack
3. Cross-post every video to TikTok + IG Reels + YouTube Shorts simultaneously — triple surface area per asset
4. Add DM-share bait to video CTAs (IG now weights DM shares as top metric)
5. Repurpose video scripts into Twitter threads via content_repurposer.py — same research, 5x output
6. Build affiliate offer comparison videos (our product vs competitor) — high buyer intent, low competition from other affiliates

## Budget Tier Strategies

### FREE
Remotion for video rendering, claude -p for scripts, surge.sh for affiliate link redirect pages, posting_queue for scheduling. Zero cost per video produced.

### LOW
$0-50/mo — boost top 2 videos/week on TikTok ($5/day) to seed algo. Test which offer converts. Kill losers in 72h.

### MID
$50-200/mo — license video template pack to other affiliates on Gumroad ($49 one-time). The meta-play: sell the process to people who won't build it themselves.

## Daily Actions

- [ ] Run subagents to scan CREATOR_PROGRAMS.csv and WINNING_CONTENT_STRUCTURES.csv in parallel
- [ ] Create ai_affiliate_video_pipeline.py with DAG phases wired to video_factory and content_repurposer
- [ ] Add to AI_VIDEO_CONTENT_TRACKER.csv schema: offer_name, affiliate_link, video_path, platform, clicks, commissions
- [ ] Wire cron at 7 AM daily — output goes to posting_queue + tracker
- [ ] After 14 days of data, package the working video script templates as a Gumroad product ($49)

## Tooling

```json
{
  "browser": "playwright MCP for offer research",
  "email": "none",
  "content": "video_factory (Remotion) + content_repurposer.py + engagement_bait_converter.py"
}
```
