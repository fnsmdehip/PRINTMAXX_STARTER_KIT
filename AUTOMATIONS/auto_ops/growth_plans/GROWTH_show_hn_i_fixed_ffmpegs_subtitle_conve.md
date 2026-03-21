# Growth Plan: Show HN: I fixed FFmpeg's subtitle conversion (the bug from 

**Created:** 2026-03-21 12:41
**Venture:** APP
**Budget Tier:** FREE
**Revenue Est:** $300-900/mo

---

## Tactics

1. SEO: target 'convert SRT to PGS online', 'SRT to SUP converter', 'Blu-ray subtitle converter free' — near-zero competition, high buyer intent
2. Post in r/PleX, r/DataHoarder, r/Jellyfin, r/ffmpeg — these users hit the bitmap subtitle wall constantly
3. Dev content: 'How Claude Code fixed a 12-year-old open source bug' — submit to HN Show HN + IH for organic traffic and credibility
4. List on ProductHunt as 'the subtitle converter that actually handles PGS/bitmap formats'
5. API tier pitched to streaming pipeline builders — one Zapier/n8n integration node drives recurring B2B revenue
6. Engage directly under the original HN thread to capture warm traffic already validated by upvotes

## Budget Tier Strategies

### FREE
SEO landing pages per format pair (30+ pages auto-generated), HN/IH dev blog post, r/PleX and r/DataHoarder organic posts, engage in original HN thread, submit to free directories (It's FOSS, AlternativeTo)

### LOW
$20-30/mo ProductHunt boost on launch day; Reddit promoted post in r/VideoEditing or r/PleX targeting subtitle pain point

### MID
$50-100/mo Google Ads on 'subtitle format converter' and PGS/SRT niche terms — low CPC, high intent, converts directly

## Daily Actions

- [ ] 1. Find and star the GitHub repo; document all supported input/output format pairs
- [ ] 2. Generate webapp from app factory base template — drag-drop subtitle file, select output format, convert
- [ ] 3. Wire Stripe: free tier = 10 files/day; Pro = $9/mo unlimited + API key
- [ ] 4. Run keyword subagent: extract all 'convert X to Y subtitle' search queries
- [ ] 5. Run landing page subagent: generate one SEO page per format pair (SRT→PGS, ASS→SRT, VTT→PGS, etc.)
- [ ] 6. Deploy to surge.sh (subtitleconverter.surge.sh or subtitlemaxx.surge.sh)
- [ ] 7. Write and post 'Claude Code fixed a 12-year FFmpeg bug' story to HN + Indie Hackers
- [ ] 8. Post in Plex/Jellyfin Discord servers and relevant subreddits with genuine helpful framing
- [ ] 9. Submit sitemap; add to AlternativeTo under 'Subtitle Edit' and 'Handbrake'
- [ ] 10. Add weekly cron to monitor Search Console impressions for conversion keyword set

## Tooling

```json
{
  "browser": "none",
  "email": "none",
  "content": "content_factory for SEO page generation + engagement_bait_converter for tweet/thread output"
}
```
