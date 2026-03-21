# Growth Plan: [PH LAUNCH] Contral: The agentic IDE which teaches while you

**Created:** 2026-03-21 12:40
**Venture:** OUTBOUND
**Budget Tier:** FREE
**Revenue Est:** $200-500/mo

---

## Tactics

1. Scrape PH maker profiles daily — founders who launch dev tools are highest-intent B2B leads
2. 48h outreach window: contact makers within 48h of launch while they are most engaged and responsive
3. Engage with Contral launch post (upvote + comment) for visibility to their dev-tool audience
4. Extract upvoter list from Contral PH page via Playwright — upvoters self-identify as agentic IDE buyers
5. Content angle: write SEO post on agentic IDEs (Contral, Cursor, etc.) — captures developer keyword traffic
6. Monitor agentic-IDE-adjacent PH launches weekly as standing intelligence source

## Budget Tier Strategies

### FREE
Daily PH scrape via requests/Playwright, maker cold email via custom script, engage with launch posts organically, SEO content on agentic IDE trend using existing content pipeline

### LOW
$0-50/mo — Hunter.io free tier to verify maker emails, schedule via existing twitter_warmup_poster.py for content distribution

### MID
$50-200/mo — Apollo or Clay enrichment on upvoter list, automated LinkedIn outreach sequence to PH makers in dev tools

## Daily Actions

- [ ] Route to existing chain_14_ph_launches_today__high_quality_b2b_ — same pattern already built
- [ ] Add 'agentic_ide' and 'dev_tool' as priority category filters in ph_launch_lead_scraper.py
- [ ] Extract Contral maker profile + top 50 upvoters via Playwright MCP as one-time lead batch
- [ ] Run leads through existing cold outreach qualification pipeline
- [ ] Feed agentic IDE trend signal to engagement_bait_converter.py for 3 content posts

## Tooling

```json
{
  "browser": "Playwright MCP for PH upvoter extraction",
  "email": "custom cold email scripts (existing)",
  "content": "engagement_bait_converter.py \u2014 convert agentic IDE trend into 3 posts"
}
```
