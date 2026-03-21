# Growth Plan: Backend developers charge $10k+ for this.

I built it in 2 h

**Created:** 2026-03-21 12:40
**Venture:** EAS
**Budget Tier:** FREE
**Revenue Est:** $1500-4000/mo

---

## Tactics

1. Reply to 'I need a developer' and 'dev costs too much' tweets with '2hr build' proof post
2. Post weekly demo: pick a common SaaS request, build live, show before/after time
3. Seed r/SaaS, r/entrepreneur with 'I stopped hiring devs, here's what I use instead' post
4. List boilerplate template on Gumroad as $97 product: 'Full SaaS in a box'

## Budget Tier Strategies

### FREE
Reply-bait on dev cost complaints. Post 2hr build demos. Cross-promote with APP factory builds as proof-of-concept. Submit to indie hacker Show HN.

### LOW
$0-50/mo — Boost top-performing demo post. Target 'hire developer' and 'build SaaS' keyword audiences on X. $10 promoted tweet with video demo.

### MID
$50-200/mo — Paid cold outreach to non-technical founders in email lists. Retarget visitors to EAS landing page with 'built in 2hrs' case study ad.

## Daily Actions

- [ ] Wire into chain_vibecoded_services_300800build_mic — no new chain needed
- [ ] Create eas_saas_boilerplate_generator.py: scaffolds OAuth+Stripe+customer portal+AI+DB from config JSON, deploys to Firebase or Vercel via CLI
- [ ] Add to APP factory base template so every app build auto-inherits this stack
- [ ] Generate 3 Twitter posts using 2hr-build hook format via engagement_bait_converter.py
- [ ] Add KPI entry: weekly cold DM to non-technical founders complaining about dev costs
- [ ] Create $97 Gumroad listing: 'Full SaaS Boilerplate — Google OAuth + Stripe + AI + DB, deploy in 2hrs' (pre-build, list when account exists)

## Tooling

```json
{
  "browser": "none",
  "email": "custom cold email scripts",
  "content": "engagement_bait_converter.py \u2014 feed this exact tweet format as template"
}
```
