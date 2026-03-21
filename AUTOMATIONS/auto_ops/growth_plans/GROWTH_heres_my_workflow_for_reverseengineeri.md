# Growth Plan: Here's my workflow for reverse-engineering any creator's sty

**Created:** 2026-03-20 13:50
**Venture:** CONTENT
**Budget Tier:** FREE
**Revenue Est:** $100-400/mo indirect via higher engagement content

---

## Tactics

1. Clone styles of creators with 50K-500K followers (big enough to validate, small enough the style isnt saturated)
2. A/B test cloned-style posts vs generic posts to measure engagement lift
3. Build style library indexed by niche so any new content task pulls from proven patterns
4. Cross-pollinate styles across niches (fitness hook structure applied to productivity content)

## Budget Tier Strategies

### FREE
Use yt-dlp for video download, Whisper for transcription, Claude for style analysis. Scrape public creator pages. Store playbooks as markdown in CONTENT/style_library/

### LOW
$0-20/mo for proxy rotation if scraping at scale. Optional Descript free tier for faster transcription

### MID
$50-100/mo for video API access or TikTok research tools to identify trending creators faster

## Daily Actions

- [ ] Create CONTENT/style_library/ directory for storing creator style playbooks
- [ ] Build creator_style_reverser.py: accepts video URL or transcript, outputs structured style playbook (hooks, pacing, vocabulary, CTA patterns, visual style notes)
- [ ] Wire yt-dlp download + whisper transcription as Phase 1 input
- [ ] Claude analysis prompt: break down hook type, script structure, emotional arc, CTA pattern, vocabulary fingerprint, pacing rhythm
- [ ] Output playbook as structured JSON + human-readable markdown
- [ ] Feed playbooks into content_multiplier.py as style templates for bulk generation
- [ ] Add weekly cron (Monday 7 AM) to scrape 5 new top creators and refresh style library
- [ ] Track engagement metrics on styled vs unstyled posts in KPI dashboard

## Tooling

```json
{
  "browser": "playwright_mcp",
  "email": "none",
  "content": "content_multiplier + engagement_bait_converter + style_library"
}
```
