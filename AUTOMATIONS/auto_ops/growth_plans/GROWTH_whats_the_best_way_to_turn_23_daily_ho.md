# Growth Plan: What's the best way to turn 2-3 daily hours into steady side

**Created:** 2026-03-21 12:40
**Venture:** CONTENT
**Budget Tier:** FREE
**Revenue Est:** $0-50/mo

---

## Tactics

1. Post '2-3 hours/day → $X/mo' content with specific tool names (prayerlock, soberstreak, streak apps) as proof-of-concept examples
2. Reply to r/passive_income threads matching this exact question — drop our app links as real examples
3. Create a 'time audit' thread: '2 hours on X = $Y/mo automated' format with our actual builds
4. Target the '9-5 + side hustle' identity angle — highest engagement on this subreddit

## Budget Tier Strategies

### FREE
Organic replies in r/passive_income, r/sidehustle, r/financialindependence threads matching '2-3 hours daily' intent. Repurpose as Twitter threads via content_repurposer.py. Cross-post to LinkedIn as founder story.

### LOW
$0-50/mo — Boost top-performing tweet variant on X. Use $10-20 on Reddit promoted posts targeting r/passive_income if one post gets organic traction first.

### MID
$50-200/mo — Retarget visitors from streak app landing pages with this angle as ad creative. A/B test '2 hours/day' vs 'set it and forget it' copy.

## Daily Actions

- [ ] python3 AUTOMATIONS/engagement_bait_converter.py --input 'What is the best way to turn 2-3 daily hours into steady side income' --source reddit/passive_income --angle time_constrained_earner
- [ ] Review generated posts in CONTENT/social/posting_queue/ — approve 3 best variants
- [ ] Route approved posts through content_repurposer.py for Twitter + LinkedIn + Reddit variants
- [ ] Add to posting queue — schedule over 1 week (not all at once)

## Tooling

```json
{
  "browser": "none",
  "email": "none",
  "content": "engagement_bait_converter.py + content_repurposer.py"
}
```
