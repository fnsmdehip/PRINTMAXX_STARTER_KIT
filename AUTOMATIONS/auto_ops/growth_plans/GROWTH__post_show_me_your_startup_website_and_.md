# Growth Plan:  post: show me your startup website and i'll give you action

**Created:** 2026-03-20 18:35
**Venture:** EAS
**Budget Tier:** FREE
**Revenue Est:** $500-1500/mo

---

## Tactics

1. authority_building_via_free_audits
2. reddit_value_first_outbound
3. content_repurpose_audit_into_thread

## Budget Tier Strategies

### FREE
Post genuine feedback on r/startups, r/SideProject, r/indiehackers, IH forums. Repurpose best audits into Twitter threads showing common mistakes. CTA: 'DM for full audit'

### LOW
$0-50/mo: Boost top-performing audit threads on Twitter. Run targeted Reddit ads on startup subs

### MID
$50-200/mo: Sponsor IH newsletter placement offering free audits. Cold email Product Hunt launchers with mini-audit attached

## Daily Actions

- [ ] Wire into existing chain__post_show_me_your_startup_website_and_ for dedup
- [ ] Build website_roast_lead_gen.py with Reddit JSON API scraper for review-my-site posts
- [ ] Add Playwright-based Lighthouse + meta tag audit module
- [ ] Claude generates 3-paragraph actionable feedback per site (no fluff, specific fixes)
- [ ] Post replies to original threads with audit summary + soft CTA
- [ ] Log warm responders to LEDGER/INBOUND_LEADS.csv tagged source=website_roast
- [ ] Cron 7:30 AM daily, feed qualified leads into EAS outbound pipeline

## Tooling

```json
{
  "browser": "playwright_mcp",
  "email": "custom_cold_email",
  "content": "claude_p_feedback_gen"
}
```
