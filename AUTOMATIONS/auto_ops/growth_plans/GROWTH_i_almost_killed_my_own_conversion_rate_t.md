# Growth Plan: I almost killed my own conversion rate to save $400/mo on su

**Created:** 2026-03-20 18:09
**Venture:** APP
**Budget Tier:** FREE
**Revenue Est:** $0-100/mo indirect (conversion lift across existing app portfolio, compounding as apps get traffic)

---

## Tactics

1. Add FAQ schema markup for SEO rich snippets on all app pages
2. Use support chat transcripts as content seeds for social posts
3. A/B test pages with vs without FAQ to prove conversion lift

## Budget Tier Strategies

### FREE
Claude-powered FAQ generation, static HTML chat widget with pre-built answers, schema markup for search visibility, in-page help tooltips

### LOW
$0-50/mo: Crisp.chat free tier (2 seats) or Tawk.to (fully free) for live chat fallback on highest-traffic apps

### MID
$50-200/mo: Intercom starter or Zendesk for multi-app support hub with shared inbox if volume warrants

## Daily Actions

- [ ] 1. Run playwright crawl of all 47 deployed URLs from OPS/DEPLOYMENT_URLS.md to audit for FAQ, help, and onboarding presence
- [ ] 2. Generate niche-specific FAQ content for each app using claude -p (batch all 47 in parallel subagents)
- [ ] 3. Create a lightweight static chat widget (HTML/JS, no backend) with pre-built Q&A per app category
- [ ] 4. Inject FAQ sections and chat widget into landing pages via template modification
- [ ] 5. Add FAQ schema markup (FAQPage JSON-LD) for SEO rich snippet eligibility
- [ ] 6. Redeploy updated pages via surge
- [ ] 7. Set weekly cron to re-audit new deployments and auto-generate support content

## Tooling

```json
{
  "browser": "playwright for audit crawl",
  "email": "none",
  "content": "claude -p for FAQ and help content generation"
}
```
