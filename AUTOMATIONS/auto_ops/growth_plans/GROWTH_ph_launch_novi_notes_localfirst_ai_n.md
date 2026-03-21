# Growth Plan: [PH LAUNCH] Novi Notes: Local-first AI note app for Mac zero

**Created:** 2026-03-21 12:40
**Venture:** OUTBOUND
**Budget Tier:** FREE
**Revenue Est:** $150-600/mo

---

## Tactics

1. 48h outreach window post-PH launch — founders are maximally receptive during launch week
2. Offer launch growth services: cold email setup, SEO landing page, affiliate program setup
3. Clone the local-first + MCP app niche for APP_FACTORY (Novi Notes proves demand exists)
4. Post 'tools we're watching' content using PH launch signal to drive PRINTMAXX Twitter engagement
5. Monitor Novi Notes reviews/complaints on PH for unmet needs our apps can fill

## Budget Tier Strategies

### FREE
Scrape PH daily for local-first/MCP launches, queue outbound via existing chain, feed niche signal to app_factory_command_center.py, generate 1 tweet about the launch trend

### LOW
$0-50/mo: Sponsor PH comment on similar launches to get maker attention; use PH ad targeting for makers in productivity niche

### MID
$50-200/mo: Sponsor a future PH launch in similar niche to build credibility with maker community

## Daily Actions

- [ ] Wire ph_mcp_app_trend_extractor.py to pull PH launches tagged with 'MCP', 'local-first', 'AI notes', 'Mac app' daily at 7 AM
- [ ] Append founder contact + launch URL to existing chain_14_ph_launches input queue (reuse, don't rebuild)
- [ ] Extract niche signal (local-first + MCP = validated demand) → append to LEDGER/APP_CLONE_OPPORTUNITIES.csv
- [ ] Run engagement_bait_converter.py on this launch to generate 1 tweet about the local-first AI tool trend
- [ ] Add cron entry for daily 7 AM execution

## Tooling

```json
{
  "browser": "playwright (PH scrape if API fails)",
  "email": "existing cold email scripts",
  "content": "engagement_bait_converter.py"
}
```
