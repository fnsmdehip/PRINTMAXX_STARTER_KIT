# Growth Plan: I spent 4 hours a day on Reddit to get my first 50 customers

**Created:** 2026-03-20 13:50
**Venture:** CONTENT
**Budget Tier:** FREE
**Revenue Est:** $50-300/mo

---

## Tactics

1. Target high-intent subreddits: r/SaaS, r/indiehackers, r/Entrepreneur, r/sideproject, r/ClaudeAI, r/webdev for our products
2. Value-first posting: answer genuinely, product mention is secondary — builds karma and trust
3. Comment on rising posts within first hour for maximum visibility
4. Cross-reference Reddit threads with our existing content — link blog posts that answer questions
5. Track which subreddits convert best, double down on top 5
6. Build Reddit karma on account before any product mentions (warmup period)

## Budget Tier Strategies

### FREE
Organic Reddit engagement: value-first responses in target subreddits 3x/day, karma building, profile optimization with product links, AMA-style posts sharing build journey

### LOW
$0-50/mo: Reddit ads targeting specific subreddits for top-performing products, promoted posts in r/SaaS and r/indiehackers

### MID
$50-200/mo: Multiple Reddit accounts with residential proxies for wider coverage (GoLogin + SOAX), subreddit-specific landing pages for tracking

## Daily Actions

- [ ] Extend reddit_deep_scraper.py with keyword matching for our product categories (streak apps, prayer, focus, MCP, Claude Code)
- [ ] Build reddit_engagement_pipeline.py with DAG: scrape → qualify → draft → queue
- [ ] Keyword list: streak app, habit tracker, prayer app, focus app, Claude Code, MCP server, cold email tool, landing page builder
- [ ] Response templates: genuine answer + subtle mention pattern, pure value no mention pattern, build-in-public story pattern
- [ ] Anti-spam safeguards: max 3 posts/subreddit/day, 2h minimum between posts, karma threshold before product mentions, rotate subreddits
- [ ] Add cron at 7AM/1PM/7PM to catch peak Reddit activity windows
- [ ] Track conversions: UTM params on all product links posted, log to KPI dashboard
- [ ] Warmup: first 2 weeks pure value posting (no product mentions) to build karma and history

## Tooling

```json
{
  "browser": "none (Reddit JSON API via requests)",
  "email": "none",
  "content": "claude -p for response drafting, existing reddit_deep_scraper.py for monitoring"
}
```
