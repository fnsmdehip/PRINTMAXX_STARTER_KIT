# Growth Plan: Worst and best SaaS tools you’ve ever used

**Created:** 2026-03-20 18:09
**Venture:** CONTENT
**Budget Tier:** FREE
**Revenue Est:** $0-25/mo

---

## Tactics

1. Post comparison content as replies in r/SaaS threads for organic reach
2. Repurpose top-voted pain points into Twitter threads tagging the tool accounts
3. SEO longtail pages: 'best alternative to [hated tool]'

## Budget Tier Strategies

### FREE
Mine Reddit threads weekly, publish comparison listicles to existing accounts, cross-post to dev.to/Medium, reply in original threads with value-add links

### LOW
$0-20/mo boost top-performing comparison posts on Twitter/LinkedIn

### MID
$50-100/mo programmatic SEO for '[tool] alternative' longtail pages with affiliate links

## Daily Actions

- [ ] Scrape r/SaaS for tool review threads using existing reddit_deep_scraper.py JSON API
- [ ] Extract tool names + sentiment (loved/hated) + specific pain points via claude -p
- [ ] Generate 1 comparison listicle per week for content pipeline
- [ ] Route high-pain-point tools to APP_FACTORY as clone/alternative candidates
- [ ] Publish via existing content distribution channels

## Tooling

```json
{
  "browser": "none",
  "email": "none",
  "content": "content_factory + engagement_bait_converter"
}
```
