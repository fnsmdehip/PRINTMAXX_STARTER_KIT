# Growth Plan: # Sleep YouTube Video Descriptions  Pre-written titles, desc

**Created:** 2026-03-20 18:10
**Venture:** CONTENT
**Budget Tier:** FREE
**Revenue Est:** $50-300/mo after 10-20 videos indexed (sleep niche CPM $5-15, long watch sessions)

---

## Tactics

1. Cross-post audio snippets as TikTok/Shorts to funnel viewers to full 8hr YouTube videos
2. SEO-stack descriptions with long-tail sleep keywords (rain sounds for baby, brown noise for studying)
3. Playlist optimization: group by duration (1hr, 4hr, 8hr) and sound type for session-based watch time
4. Community tab polls asking what sounds to make next — drives engagement signal
5. Pin comment with affiliate link to sleep products (weighted blankets, white noise machines)

## Budget Tier Strategies

### FREE
Programmatic metadata generation via claude -p, cross-post 60s clips to TikTok/Shorts, optimize titles with free TubeBuddy tier, engage in sleep/ASMR subreddits with value-first posts linking channel

### LOW
$10-30/mo for stock ambient audio packs or Epidemic Sound subscription to avoid copyright strikes on monetized videos

### MID
$50-100/mo for TubeBuddy paid tier (A/B title testing, keyword explorer) + small ad spend promoting best-performing shorts

## Daily Actions

- [ ] Wire orphan doc content into CONTENT/youtube/sleep_metadata_templates/ as structured data
- [ ] Build youtube_metadata_generator.py that takes niche + video_count and outputs title/desc/tags per video
- [ ] Seed with existing 10 sleep video templates from the orphan doc
- [ ] Add keyword research phase: scrape top 50 sleep YouTube titles via requests, extract patterns
- [ ] Schedule weekly cron (Monday 7 AM) to generate fresh metadata batches for next upload cycle
- [ ] Add to content calendar with BLOCKER: YouTube channel creation (human action)
- [ ] Create audio generation pipeline: ffmpeg brown/pink/white noise + rain overlay = royalty-free 8hr videos at $0 cost

## Tooling

```json
{
  "browser": "none",
  "email": "none",
  "content": "content_factory + claude -p for metadata generation"
}
```
