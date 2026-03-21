# Growth Plan: The real AI gold rush isn’t in building. It’s in babysitting

**Created:** 2026-03-20 18:35
**Venture:** OUTBOUND
**Budget Tier:** FREE
**Revenue Est:** $800-2500/mo

---

## Tactics

1. Reply to Reddit threads about broken vibe-coded apps with genuine help + soft CTA
2. Post 'AI babysitter' thread on Twitter with real case study data from our builds
3. Create content showing common vibe-code failure modes (engagement bait that doubles as lead gen)
4. Monitor r/SaaS r/startups r/webdev for 'my AI-built app broke' posts

## Budget Tier Strategies

### FREE
Reddit reply strategy on r/SaaS r/startups r/webdev targeting broken-vibe-code posts. Twitter threads showing AI maintenance value. Cross-post to IndieHackers.

### LOW
$20-40/mo on targeted X ads to founders who follow Cursor/Replit/v0 accounts

### MID
$100-150/mo on LinkedIn InMail to non-technical founders who recently launched AI-built products

## Daily Actions

- [ ] Add subreddit keywords ('vibe code broke', 'AI built app issues', 'Claude code maintenance') to reddit_deep_scraper filter list
- [ ] Create DAG script scraping 3 sources in parallel for founders needing AI tool maintenance
- [ ] Score leads by: mentions specific broken tool (high), asks for help (high), just venting (low)
- [ ] Generate cold email template: 'I maintain AI-built tools so founders can focus on growth' positioning
- [ ] Wire qualified leads into existing cold outbound pipeline (chain_vibecoded_services)
- [ ] Add to content queue: 3 tweets on AI babysitting angle + 1 thread with real data
- [ ] Cron at 7:30 AM daily to refresh lead pipeline

## Tooling

```json
{
  "browser": "none",
  "email": "custom cold email scripts",
  "content": "content_factory + engagement_bait_converter"
}
```
