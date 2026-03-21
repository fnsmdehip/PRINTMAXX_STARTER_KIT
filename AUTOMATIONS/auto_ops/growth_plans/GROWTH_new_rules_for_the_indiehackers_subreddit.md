# Growth Plan: NEW RULES for the IndieHackers subreddit

**Created:** 2026-03-20 13:50
**Venture:** CONTENT
**Budget Tier:** FREE
**Revenue Est:** $0-50/mo indirect via traffic and leads

---

## Tactics

1. Craft posts as value-first case studies per new rules
2. Use allowed self-promo windows strategically
3. Engage in comments to build karma before posting links
4. Cross-post compliant content to r/SideProject and r/microsaas

## Budget Tier Strategies

### FREE
Organic r/indiehackers posting 2-3x/week with rule-compliant templates, comment engagement warming, cross-post to adjacent subs

### LOW
$0-20/mo for Reddit premium to reduce post cooldowns and access analytics

### MID
$50-100/mo for promoted posts on adjacent subreddits driving to our content

## Daily Actions

- [ ] Scrape current r/indiehackers rules via reddit JSON API
- [ ] Build rule-compliance checker that validates post title, body, link format against new rules
- [ ] Update CONTENT/social/distribution/ reddit templates to match new allowed formats
- [ ] Wire compliance checker as pre-distribution hook for any reddit content going to r/indiehackers
- [ ] Weekly cron rescrapes rules to catch future changes automatically
- [ ] Track post removal rate as KPI - target <5% removal

## Tooling

```json
{
  "browser": "none",
  "email": "none",
  "content": "content_factory + reddit_deep_scraper.py"
}
```
