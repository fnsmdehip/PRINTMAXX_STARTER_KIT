# Growth Plan: linkedin automation tools that won't get you restricted - wh

**Created:** 2026-03-20 13:50
**Venture:** OUTBOUND
**Budget Tier:** FREE
**Revenue Est:** $200-800/mo

---

## Tactics

1. LinkedIn warmup protocol (30 actions/day week 1, scale 10%/week)
2. Engage with target posts before connecting (3 touches rule)
3. Use Sales Navigator free trial for initial list build then export

## Budget Tier Strategies

### FREE
Playwright browser automation with Brave cookies, manual warmup schedule, organic engagement before connect requests, profile optimization for inbound

### LOW
$0-50/mo: LinkedIn Sales Navigator monthly trial rotation, proxy rotation for multi-session safety

### MID
$50-200/mo: Dedicated residential proxy, PhantomBuster cheapest tier for enrichment only, rest handled by custom scripts

## Daily Actions

- [ ] Extract safe LinkedIn automation limits from Reddit thread into reference doc
- [ ] Add LinkedIn rate-limit constants to existing eas_lead_pipeline.py config
- [ ] Build lightweight Playwright script that respects daily/weekly caps
- [ ] Wire into existing OUTBOUND venture cron for weekday morning runs
- [ ] Track restriction events to auto-throttle if platform pushback detected

## Tooling

```json
{
  "browser": "playwright_mcp",
  "email": "custom cold email scripts",
  "content": "content_factory"
}
```
