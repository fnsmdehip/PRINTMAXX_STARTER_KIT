# Growth Plan: My entire sales funnel is Reddit comments

**Created:** 2026-03-20 13:50
**Venture:** CONTENT
**Budget Tier:** FREE
**Revenue Est:** $100-400/mo

---

## Tactics

1. subreddit keyword monitoring for high-intent threads
2. profile bio optimization with landing page links
3. helpful-first commenting (value ratio 10:1 before any self-promo)
4. target threads that rank in Google for longtail queries
5. cross-reference trending subreddit topics with our existing products

## Budget Tier Strategies

### FREE
Organic Reddit commenting on 5-10 target subreddits, profile link to landing pages, monitor via existing reddit_deep_scraper.py, comment drafts via claude -p

### LOW
$0-20/mo for Reddit Premium (no ads, access to r/lounge for networking), aged Reddit accounts for multi-subreddit coverage

### MID
$50-100/mo for multiple aged accounts + proxy rotation to scale comment volume across 20+ subreddits without triggering rate limits

## Daily Actions

- [ ] Extend reddit_deep_scraper.py to flag high-intent threads (questions, recommendations, pain-point posts) in target subreddits
- [ ] Build reddit_comment_funnel.py: takes flagged threads + our product catalog, generates helpful comment drafts using claude -p
- [ ] Comment drafts stored in CONTENT/social/posting_queue/reddit_comments_YYYYMMDD.txt for human review and posting
- [ ] Cron at 7 AM daily to surface new opportunities
- [ ] Track posted comments and engagement in LEDGER/reddit_comment_funnel.csv
- [ ] Profile bio updated with links to highest-converting landing pages

## Tooling

```json
{
  "browser": "none",
  "email": "none",
  "content": "claude -p for comment drafts + existing reddit_deep_scraper.py for thread discovery"
}
```
