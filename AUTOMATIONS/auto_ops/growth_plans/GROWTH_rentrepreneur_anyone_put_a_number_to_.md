# Growth Plan: [r/entrepreneur] Anyone put a number to how much they've tur

**Created:** 2026-03-21 12:41
**Venture:** CONTENT
**Budget Tier:** FREE
**Revenue Est:** $0-30/mo indirect (content engagement → audience growth → downstream affiliate/product revenue)

---

## Tactics

1. Post 'founders who turned down $X from investors' stories as engagement bait — contrarian angle drives shares
2. Use extracted founder profiles as warm outbound leads (they have revenue, no VC overhead, likely open to tools/services)
3. Thread format: 'X founders who said no to investors — what they built instead'

## Budget Tier Strategies

### FREE
Route 3-5 best stories weekly to engagement_bait_converter.py, schedule via twitter_warmup_poster.py, cross-post to LinkedIn

### LOW
$0-50/mo — boost top-performing post with $10-20 to seed algorithmic reach

### MID
$50-200/mo — sponsor a bootstrapper newsletter placement referencing these stories

## Daily Actions

- [ ] Add keyword filters ('turned down', 'said no to investors', 'rejected VC', 'bootstrapped instead') to background_reddit_scraper.py's existing subreddit list
- [ ] Route matched posts/top comments through engagement_bait_converter.py with template: contrarian founder story
- [ ] Output to CONTENT/social/posting_queue/ for weekly review
- [ ] Do NOT create new venture — this is content seed only, no direct revenue path

## Tooling

```json
{
  "browser": "none",
  "email": "none",
  "content": "engagement_bait_converter.py"
}
```
