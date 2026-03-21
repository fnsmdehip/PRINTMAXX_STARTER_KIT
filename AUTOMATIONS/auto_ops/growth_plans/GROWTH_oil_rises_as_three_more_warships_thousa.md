# Growth Plan: Oil Rises As Three More Warships, Thousands Of Marines Dispa

**Created:** 2026-03-20 23:36
**Venture:** CONTENT
**Budget Tier:** FREE
**Revenue Est:** $50-200/mo

---

## Tactics

1. Post geopolitical commentary within 15 min of breaking macro news — algo rewards timeliness
2. Reply to ZeroHedge tweets with 'what this means' takes — hijack their distribution
3. Tag oil/defense/macro finance accounts in threads to trigger reply chains
4. Use verified numbers (barrel price, % move) in first line — stops the scroll

## Budget Tier Strategies

### FREE
RSS feed polling ZeroHedge + Reuters energy desk → claude -p generates 3 takes per event → routes to content_multiplier.py → posting_queue/

### LOW
$0-20/mo: boost high-engagement geopolitical posts on X to finance audiences (CPM cheap in finance niche outside US hours)

### MID
$50-100/mo: sponsored placement in finance newsletters + ZeroHedge comment seeding with link to our commentary thread

## Daily Actions

- [ ] Add ZeroHedge RSS + Reuters energy RSS to geopolitical_signal_content_router.py
- [ ] Define trigger keywords: ['warships', 'military deployment', 'oil embargo', 'marines', 'Middle East escalation', 'sanctions oil']
- [ ] On trigger: extract event summary → pass to claude -p with finance commentary prompt → output 3 posts (thread opener, standalone take, reply bait)
- [ ] Route posts to CONTENT/social/posting_queue/ with tag #macro
- [ ] Wire cron at 7AM/1PM/7PM for feed polling
- [ ] Feed high-engagement posts back to content_repurposer.py for newsletter inclusion

## Tooling

```json
{
  "browser": "none",
  "email": "none",
  "content": "content_factory + engagement_bait_converter.py"
}
```
