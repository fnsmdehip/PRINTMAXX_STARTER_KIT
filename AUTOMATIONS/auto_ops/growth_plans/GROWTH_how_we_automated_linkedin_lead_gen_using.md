# Growth Plan: How we automated LinkedIn lead gen using keyword triggers (w

**Created:** 2026-03-20 18:35
**Venture:** OUTBOUND
**Budget Tier:** FREE
**Revenue Est:** $300-1500/mo

---

## Tactics

1. Comment warming: engage genuinely on 5 posts before any outreach comments daily to build profile credibility
2. Profile optimization: headline as value prop not job title, featured section with case studies
3. Multi-account rotation: separate account per niche (tech/faith/fitness) to avoid pattern detection
4. Reply bait: post own polls/questions in same groups to attract inbound signals
5. Cross-platform signal stacking: same keyword monitoring on Reddit/Twitter to identify people also active on LinkedIn

## Budget Tier Strategies

### FREE
Manual keyword searches via LinkedIn search URL scraping, Playwright automation with existing Brave login, Claude-generated comments, organic profile building through daily engagement

### LOW
$0-50/mo: LinkedIn Sales Navigator basic ($0 trial), residential proxy for multi-account stability, GoLogin for browser fingerprint separation

### MID
$50-200/mo: LinkedIn Sales Navigator Core ($99/mo), SOAX proxies for reliable scraping, Phantombuster credits for backup automation

## Daily Actions

- [ ] 1. Build buying-signal keyword list per niche (20+ trigger phrases per vertical)
- [ ] 2. Create linkedin_keyword_trigger_outreach.py with Playwright + Brave cookie auth
- [ ] 3. Implement LinkedIn search scraper for keyword monitoring (search URL pattern: linkedin.com/search/results/content/?keywords=...)
- [ ] 4. Build qualifier scoring: direct ask=10, pain=8, competitor complaint=7, filter >= 6
- [ ] 5. Wire Claude comment generator with tone-matching and soft CTA templates
- [ ] 6. Add rate limiting: max 10 comments/day, 5min gaps, weekday-only schedule
- [ ] 7. Build engagement tracker: check replies 24h after comment, generate warm DM drafts
- [ ] 8. Add to cron: 3x daily (7am, noon, 5pm) on weekdays
- [ ] 9. Wire into existing chain_how_we_automated_linkedin_lead_gen_using
- [ ] 10. Add KPI tracking: signals found, comments posted, reply rate, DMs sent, meetings booked

## Tooling

```json
{
  "browser": "Playwright with Brave cookie injection",
  "email": "none \u2014 comment-first strategy bypasses email",
  "content": "claude -p for comment generation"
}
```
