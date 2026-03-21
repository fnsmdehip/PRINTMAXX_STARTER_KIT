# Growth Plan: [PH LAUNCH] optimo: effortless media optimizer for the web

**Created:** 2026-03-21 12:40
**Venture:** OUTBOUND
**Budget Tier:** FREE
**Revenue Est:** $200-600/mo

---

## Tactics

1. 48h launch window: contact founders within 48h of PH launch when they're in maximum hustle/receptive mode
2. Reference their specific product (optimo-style tools = web performance niche) — offer performance audit or content strategy
3. Target MEDIUM+ upvote launches (50-300 range) — big enough to be real, small enough that founder still personally responds
4. Cross-reference PH founder Twitter handles with our existing scraped accounts for warm signal before cold outreach
5. Build PH category watchlist: developer-tools, productivity, saas, marketing — these founders have budget and technical sophistication

## Budget Tier Strategies

### FREE
Daily PH scrape via Playwright MCP → filter → Claude-generated personalized DMs/emails → manual send queue. Zero cost, 5-15 qualified leads/day.

### LOW
$0-50/mo — Instantly or Smartlead free tier for automated send sequencing. Add Twitter DM automation for founders with open DMs.

### MID
$50-200/mo — Apollo.io enrichment to find verified founder emails from PH profiles. Combine email + Twitter touchpoints for 2x reply rate.

## Daily Actions

- [ ] Extend existing chain_14_ph_launches_today chain — add category filter for web/media/SaaS tools
- [ ] Deploy ph_launch_outbound_monitor.py with Playwright MCP: scrape ph.com/posts?order=ranked daily at 8 AM
- [ ] Qualifier filters by upvotes (50-500 sweet spot) + extracts maker Twitter/email from PH profile
- [ ] Route qualified founders to existing cold_outbound pipeline with PH-specific opening line template
- [ ] Add cron: 0 8 * * * — daily scrape feeds LEDGER/INBOUND_LEADS.csv with source=ProductHunt
- [ ] KPI track: weekly reply rate on PH-sourced outreach vs baseline cold

## Tooling

```json
{
  "browser": "Playwright MCP (ph.com has no auth wall for public launches)",
  "email": "custom cold_email_pipeline.py (existing)",
  "content": "claude -p for personalized outreach copy per founder"
}
```
