# Growth Plan: Day 200. Just hit $12k in revenue. It still feels unreal. Ab

**Created:** 2026-03-21 12:40
**Venture:** OUTBOUND
**Budget Tier:** FREE
**Revenue Est:** $500-2000/mo

---

## Tactics

1. Target subreddits where our apps already have traction: r/sobriety, r/productivity, r/islam, r/GetMotivated, r/Accounting
2. Focus replies on posts <6h old (highest visibility window before thread dies)
3. Warm Reddit account first — 30 days karma farming on unrelated posts before product mentions
4. Use different accounts per niche to avoid cross-contamination / ban radius
5. Track which subreddits convert — double post frequency there, exit the rest
6. Reply to comments ON viral posts (not just top-level posts) — less competition, same traffic

## Budget Tier Strategies

### FREE
Use existing reddit_deep_scraper.py output as signal source. claude -p for reply generation. Manual posting from warmed account. Target 5-10 replies/day across top-converting subreddits.

### LOW
$20-50/mo for aged Reddit account with karma (buy from r/redditbay or similar) — skip 30-day warmup. Faster deployment, lower ban risk on first product mention.

### MID
$50-200/mo: Multiple aged accounts per niche. Rotate posting. Use SOAX residential proxies ($99/mo) to prevent IP-based ban clustering across accounts.

## Daily Actions

- [ ] 1. Wire reddit_intent_monitor.py to consume existing AUTOMATIONS/reddit_scraper_output/ files — no new scraping needed
- [ ] 2. Add intent keyword filter layer + product-niche matching dict (focuslock→productivity, soberstreak→sobriety, prayerlock→islam/christian, invoiceforge→freelancers)
- [ ] 3. Use claude -p to generate reply drafts: prompt includes subreddit context, original post, our app's value prop
- [ ] 4. Write output to CONTENT/social/posting_queue/reddit_replies_queue.json with post URL, reply draft, match score
- [ ] 5. Add cron: 0 */4 * * * — runs 6x daily on fresh scraper output
- [ ] 6. Human reviews queue daily, posts top 5-10 replies from warmed account
- [ ] 7. Track reply URLs in LEDGER — follow up weekly to see upvote/comment signal

## Tooling

```json
{
  "browser": "none \u2014 Reddit JSON API via requests, no browser needed",
  "email": "none",
  "content": "claude -p for reply generation, existing reddit_deep_scraper.py for signal ingestion"
}
```
