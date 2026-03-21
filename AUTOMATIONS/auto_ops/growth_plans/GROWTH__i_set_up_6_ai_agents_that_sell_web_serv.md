# Growth Plan:  i set up 6 ai agents that sell web services 24/7 (full brea

**Created:** 2026-03-20 18:09
**Venture:** OUTBOUND
**Budget Tier:** FREE
**Revenue Est:** $500-2000/mo

---

## Tactics

1. multi-niche targeting (restaurants, dentists, plumbers, realtors simultaneously)
2. free audit as lead magnet (builds trust, demonstrates value before ask)
3. portfolio snowball (each delivered site becomes a case study for next pitch)
4. reply-to-engage on local business subreddits and Facebook groups
5. Upwork/Fiverr profile with AI-speed delivery as differentiator

## Budget Tier Strategies

### FREE
Scrape GMB/Yelp for leads, cold email via custom scripts, free audits as hooks, post case studies on Reddit r/webdev r/smallbusiness, cross-pollinate with existing EAS and local_biz ventures

### LOW
$0-50/mo: Google Workspace for cold email sending domain ($6/mo), 2-3 warmup domains rotating, boost case study posts on local subreddits

### MID
$50-200/mo: Instantly or Smartlead for email at scale ($30-97/mo), Apollo.io for verified contact data ($49/mo), run 200+ emails/day across warmed domains

## Daily Actions

- [ ] 1. Extend local_biz_website_scraper.py to output qualified leads with contact info and site audit scores
- [ ] 2. Build ai_web_services_sales_agents.py with 6 HandoffRouter stages using existing handoff.py
- [ ] 3. Create email templates: initial audit hook, objection responses (4 types from procedural memory), followup sequence (3 touches)
- [ ] 4. Wire PageSpeed/Lighthouse audit into playwright MCP for automated site scoring
- [ ] 5. Create deliverable templates: SEO audit PDF, website mockup HTML, competitor comparison
- [ ] 6. Add cron: weekdays 7 AM scrape+qualify, 9 AM outreach, 2 PM followup check
- [ ] 7. Wire into existing EAS venture for deal tracking and revenue attribution
- [ ] 8. Add KPI row to dashboard: leads/emails/replies/deliveries/closes per day

## Tooling

```json
{
  "browser": "playwright MCP for site audits",
  "email": "custom cold email scripts + warmup rotation",
  "content": "claude -p for audit reports and website generation"
}
```
