# Growth Plan: Want to make a post

**Created:** 2026-03-20 23:12
**Venture:** CONTENT
**Budget Tier:** FREE
**Revenue Est:** $0-200/mo indirect (traffic → funnel → app/product conversions)

---

## Tactics

1. Monitor r/digitalnomad top posts daily — reply with genuine value + soft link to relevant app/landing page
2. Extract recurring pain points (visa, tools, income) → generate targeted posts that pre-sell PRINTMAXX products
3. Cross-post winning threads to Twitter/X + LinkedIn via content_repurposer.py
4. Add profile bio link to highest-traffic landing page

## Budget Tier Strategies

### FREE
Manual or scripted posting 3x/week, reply engagement on top 10 weekly posts, profile funnel to landing page

### LOW
$0-50/mo — promote winning posts via Reddit ads ($5/post boost on 2 top performers)

### MID
$50-200/mo — sponsor relevant weekly threads, test Reddit lead gen ads to email capture

## Daily Actions

- [ ] Wire reddit_digitalnomad_poster.py to pull top 10 weekly posts from r/digitalnomad via JSON API (no browser)
- [ ] Pass titles + top comments to claude -p to generate 3 value-add posts + 5 replies per cycle
- [ ] Queue output to CONTENT/social/posting_queue/ for human review before posting
- [ ] Add cron 0 9 * * 1,3,5 to run generation cycle
- [ ] Track profile link clicks and thread upvotes in ENGAGEMENT_METRICS_DAILY.csv

## Tooling

```json
{
  "browser": "none",
  "email": "none",
  "content": "claude -p + content_repurposer.py"
}
```
