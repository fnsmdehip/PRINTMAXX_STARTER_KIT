# Growth Plan: [PH LAUNCH] Assembly 2.0: Build modern client portals for se

**Created:** 2026-03-21 12:40
**Venture:** EAS
**Budget Tier:** FREE
**Revenue Est:** $300-900/mo

---

## Tactics

1. Post Assembly 2.0 PH comments: 'Built my own in 2h with Claude Code — DM me if you want the template'
2. Reddit: r/freelance, r/agencies — post 'I cloned Assembly for free, here's the template'
3. Cold DM Assembly 2.0 upvoters on PH — they're pre-qualified buyers
4. Surge.sh deploy a demo portal at client-portal-demo.surge.sh — use as proof of concept in outreach
5. Content: '5 service businesses losing clients because they have no client portal' thread

## Budget Tier Strategies

### FREE
PH comment engagement on Assembly launch, Reddit threads in r/freelance and r/agencies, cold DM upvoters, post demo portal URL in freelancer communities, engage Assembly 2.0 negative reviews with 'here's a cheaper alternative'

### LOW
$20-50 on targeted LinkedIn outreach to agency owners (100 connection requests/week limit), $0-30 on Reddit ads in r/entrepreneur targeting 'client portal' keyword

### MID
$50-150/mo cold email infrastructure (10 domains, 30 inboxes) targeting 500 service businesses/week with portal pain point angle

## Daily Actions

- [ ] 1. Use app factory to build 1 client portal template (file sharing, invoice view, project updates, messaging) — static HTML, deploy to surge.sh as demo
- [ ] 2. Scrape Assembly 2.0 PH upvoters via Playwright — these are self-qualified buyers
- [ ] 3. Build service biz lead list from LinkedIn (agencies/consultants) + Reddit freelancers who mention Google Drive / Notion for client delivery
- [ ] 4. Run client_portal_outreach_pipeline.py: qualify → cold email with demo link → close at $297-497/portal setup
- [ ] 5. Deliver customized template (30 min per client using app factory), deploy to their domain or subdomain
- [ ] 6. Wire cron Mon/Wed/Fri 7am for ongoing lead scrape + email drip
- [ ] 7. Post Assembly 2.0 PH comment thread + Reddit content via engagement_bait_converter.py

## Tooling

```json
{
  "browser": "playwright (scrape PH upvoters + LinkedIn)",
  "email": "existing cold email scripts (custom, not Instantly)",
  "content": "engagement_bait_converter.py for PH/Reddit posts",
  "portal_build": "app_factory + surge.sh deploy"
}
```
