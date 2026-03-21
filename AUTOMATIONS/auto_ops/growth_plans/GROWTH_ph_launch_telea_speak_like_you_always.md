# Growth Plan: [PH LAUNCH] Telea: Speak like you always know what to say

**Created:** 2026-03-21 12:40
**Venture:** OUTBOUND
**Budget Tier:** FREE
**Revenue Est:** $200-600/mo

---

## Tactics

1. Target PH launches with 50-300 upvotes — high-signal founders, low outreach competition vs top-100
2. Personalize openers with specific product detail ('saw Telea hit PH today — communication AI is exploding right now')
3. Monitor PH maker comments for pain points — use as cold email hook
4. Cross-reference PH founders with LinkedIn for direct email via apollo/hunter free tier
5. Flag 'communication AI' category launches for app clone opportunity queue (validated niche)

## Budget Tier Strategies

### FREE
Daily PH scrape via Playwright, founder enrichment via free LinkedIn + Twitter search, personalized cold emails via custom smtp script, route qualified leads into existing chain_14_ph_launches chain

### LOW
$0-50/mo — Hunter.io free tier (50/mo) for email verification, schedule 3 follow-up sequences per lead via custom cold email script

### MID
$50-200/mo — Apollo.io starter for enrichment at scale, Instantly warm sender rotation for improved deliverability

## Daily Actions

- [ ] Check if ph_launch_outbound_monitor.py exists in AUTOMATIONS/ — if yes, add communication/AI category filter and wire into existing chain_14_ph_launches chain
- [ ] If not, create ph_launch_outbound_monitor.py: Playwright scrape producthunt.com/posts?category=all&order=votes, extract maker profiles, score leads, append to LEDGER/INBOUND_LEADS.csv
- [ ] Wire output into existing handoff chain_14_ph_launches_today__high_quality_b2b_ — no new chain needed
- [ ] Add cron: 0 9 * * * runs scraper daily, catches same-day launches within 48h outreach window
- [ ] Flag 'communication AI' / 'speech' / 'presentation' PH categories to APP_FACTORY clone queue as validated niches

## Tooling

```json
{
  "browser": "Playwright MCP for PH scraping",
  "email": "custom cold email scripts (Instantly fallback)",
  "content": "none"
}
```
