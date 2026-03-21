# Growth Plan: 2k users, $800 with a Habit Tracker - I can't explain how go

**Created:** 2026-03-21 12:40
**Venture:** APP
**Budget Tier:** FREE
**Revenue Est:** $200-800/mo

---

## Tactics

1. Post 'I built this for myself' authentic stories NOT product launches — community love beats marketing tone
2. Warm up Reddit account: comment on 5 niche threads before posting own app each week
3. Reply to every comment in first 6h — engagement velocity signals boost Reddit algo ranking
4. Cross-post to r/SideProject and r/IndieHackers 48h after niche subreddit post performs well (50+ upvotes threshold)
5. Screenshot Reddit comment sections + install spikes → repost on Twitter as social proof loop
6. Stagger posts: 1 app per week, never same subreddit twice in 2 weeks from same account

## Budget Tier Strategies

### FREE
3 Reddit posts/week across rotating apps. Personal account with 100+ karma. Niche subreddits per app category. Reply to comments within 6h. Cross-post winners.

### LOW
$10-30 Reddit promoted posts on organic posts that hit 70+ upvotes. Test 1 app at $10 budget, measure install delta, scale winners only.

### MID
$50-100/mo Reddit ads targeting subreddits of competitor apps (r/habitica, r/streaksapp users). Lookalike by subreddit interest targeting.

## Daily Actions

- [ ] 1. Audit MONEY_METHODS/APP_FACTORY/builds/ — extract app name, niche, live URL, polish score for all 47+ apps
- [ ] 2. Run handoff chain: app_selector → post_generator → subreddit_mapper to produce posting_schedule.json
- [ ] 3. Create reddit_app_launch_poster.py: reads posting_schedule.json, submits to Reddit via Playwright MCP, logs post URLs to LEDGER/APP_REDDIT_INSTALLS.csv
- [ ] 4. Wire cron: every Monday 10am, auto-post next queued app to primary subreddit
- [ ] 5. After each post: monitor install delta in App Store Connect — log before/after 72h counts
- [ ] 6. After 5 posts: identify best-performing subreddit-niche pair → prioritize in future scheduling
- [ ] 7. Screenshot top-performing posts → route to engagement_bait_converter.py for Twitter content

## Tooling

```json
{
  "browser": "Playwright MCP for Reddit post submission",
  "email": "none",
  "content": "claude -p for personal-voice post generation"
}
```
