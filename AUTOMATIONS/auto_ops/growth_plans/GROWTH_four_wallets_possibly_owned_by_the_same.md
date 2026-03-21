# Growth Plan: Four wallets (possibly owned by the same entity) sold 395 $W

**Created:** 2026-03-21 12:40
**Venture:** CONTENT
**Budget Tier:** FREE
**Revenue Est:** $0-50/mo

---

## Tactics

1. Frame whale loss stories as lessons — crypto audience engages hard with schadenfreude + 'what I would have done instead'
2. Use Arkham explorer links as receipts — verifiable on-chain data beats opinion content 3x on crypto Twitter
3. Reply to Lookonchain's original tweets with our commentary to capture their existing audience
4. Build a 'Whale Autopsy' content series — weekly breakdown of the biggest on-chain losses

## Budget Tier Strategies

### FREE
Scrape Lookonchain Twitter daily, pull top 3 whale movement stories, run through engagement_bait_converter.py, post to Twitter with Arkham receipt links. Reply to source tweets for reach.

### LOW
$0-50/mo — Boost 1 whale autopsy post/week via Twitter ads targeting crypto followers. $5-10/post.

### MID
$50-200/mo — Sponsor crypto newsletter placement with whale tracking content as lead magnet. Add Coinbase/Binance affiliate links to posts for passive referral revenue.

## Daily Actions

- [ ] Check existing chain_my_bot_scanned_400000_wallets_to_find_t — wire this entry as a parameterized input rather than new script if pattern matches
- [ ] Add Lookonchain as a daily scrape source in twitter_alpha_scraper.py (already deployed) — filter for tweets containing '$WBTC', '$ETH', 'lost', 'sold', 'entity' keywords
- [ ] Pipe filtered tweets into engagement_bait_converter.py with prompt template: 'whale loss story → 3 content angles: lesson, data breakdown, prediction'
- [ ] Output 3 posts per whale event to CONTENT/social/posting_queue/
- [ ] Add cron at 7 AM daily (after twitter scraper runs at 6 AM)

## Tooling

```json
{
  "browser": "none \u2014 Lookonchain via Twitter API or scraper, Arkham via public explorer URLs",
  "email": "none",
  "content": "engagement_bait_converter.py"
}
```
