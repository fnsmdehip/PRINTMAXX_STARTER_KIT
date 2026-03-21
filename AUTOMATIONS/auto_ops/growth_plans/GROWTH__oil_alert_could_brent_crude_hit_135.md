# Growth Plan:  OIL ALERT: COULD BRENT CRUDE HIT $135?

Rystad Energy warns

**Created:** 2026-03-21 12:40
**Venture:** CONTENT
**Budget Tier:** FREE
**Revenue Est:** $0/mo direct — engagement signal only

---

## Tactics

1. Post the two-scenario frame as a Twitter poll: '$110 or $135? Which Brent scenario do YOU think plays out?' — polls get 3x the impressions of statements
2. Thread format: Scenario A vs Scenario B with clear price targets and dates. Verifiable numbers = shares from finance accounts
3. Reply to @DeItaone original tweet with the scenario breakdown as a value-add comment — hijack existing engagement

## Budget Tier Strategies

### FREE
Post 2-scenario thread on Twitter with poll. Reply to oil/energy macro accounts. Cross-post to r/investing, r/wallstreetbets as discussion prompt. No original research needed — cite Rystad Energy directly.

### LOW
$0-50/mo — boost top-performing finance thread with $5-10 Twitter ad spend targeting investing/trading audiences.

### MID
$50-200/mo — sponsor a finance newsletter slot when oil story is hot. CPM is lowest during macro events when everyone wants context.

## Daily Actions

- [ ] python3 AUTOMATIONS/engagement_bait_converter.py --input 'Brent crude $135 Rystad 4-month Middle East disruption scenario' --niche finance --format poll,thread
- [ ] Review output in CONTENT/social/posting_queue/ — approve best hook
- [ ] Post via twitter_warmup_poster.py if account is warmed up

## Tooling

```json
{
  "browser": "none",
  "email": "none",
  "content": "engagement_bait_converter.py \u2192 CONTENT/social/posting_queue/"
}
```
