# Growth Plan: Launched an Ad Free YouTube Transcript Tool

**Created:** 2026-03-21 12:40
**Venture:** APP
**Budget Tier:** FREE
**Revenue Est:** $50-200/mo

---

## Tactics

1. Submit to 8 free tool directories (Toolify, There's An AI, FuturePedia, AI Valley)
2. Post to r/MicroSaas and r/SideProject on launch day — title: 'I built a dead-simple ad-free YouTube transcript tool'
3. Target long-tail SEO: 'youtube transcript no ads', 'download youtube transcript free', 'youtube to text free'
4. Add to app factory builds index — cross-link from other tools for SEO juice
5. Affiliate sidebar: link to Descript (40% recurring), Otter.ai, Notion (for saving transcripts)

## Budget Tier Strategies

### FREE
Directory submissions, Reddit launch post, SEO via meta tags targeting transcript keywords, cross-link from existing app factory builds, submit to ProductHunt

### LOW
$0-50/mo: buy 2-3 backlinks from niche tool blogs, boost ProductHunt launch with indie hacker community upvote coordination

### MID
$50-200/mo: Google Ads on 'youtube transcript tool free' (low CPC ~$0.30), scale affiliate sidebar with A/B tested placements

## Daily Actions

- [ ] pip install youtube-transcript-api — no API key needed, pulls from YouTube's internal endpoint
- [ ] Build single-file HTML tool: input box, fetch via fetch() calling a lightweight /api?url= endpoint (Python Flask or Vercel serverless), render clean transcript with timestamps
- [ ] Wire affiliate sidebar: Descript ref link, Otter.ai ref link — passive click revenue
- [ ] Deploy to surge.sh as youtube-transcript.surge.sh (or similar)
- [ ] Submit to 8 tool directories same day
- [ ] Post r/MicroSaas launch thread — include 'built this in an afternoon' framing

## Tooling

```json
{
  "browser": "none",
  "email": "none",
  "content": "youtube-transcript-api (pip, free, no key needed)"
}
```
