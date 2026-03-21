# Growth Plan: client paid me $1800 for a project. my tool cost was $0.53. 

**Created:** 2026-03-21 12:40
**Venture:** EAS
**Budget Tier:** FREE
**Revenue Est:** $3000-8000/mo

---

## Tactics

1. Post case study on Reddit r/Entrepreneur r/Solopreneur with real numbers ($1800, 25 min) — hooks on effective hourly rate
2. Repurpose as Twitter thread: before/after tool stack (Webflow $42 + Typeform → $0.53/project)
3. Cold outreach to local businesses with Yelp 3-star-or-below reviews — frame as revenue-fix
4. Offer first project at $500 as portfolio anchor, then raise to $1500+ with social proof
5. Build Gumroad product: 'The $1800 Landing Page SOPs + Prompt Pack' — meta-sell the method

## Budget Tier Strategies

### FREE
Post case studies on Reddit/HN/IH with real numbers. DM 10 local biz owners/day via existing cold outbound scripts. Create thread content from project screenshots for Twitter.

### LOW
$20-30/mo LinkedIn Sales Nav trial to find SMB owners actively posting about needing web help. Boost best-performing Reddit post via targeted Reddit ads.

### MID
$50-100/mo on Google Ads targeting 'small business landing page [city]' — high-intent, low volume, $500+ LTV makes CPA math easy.

## Daily Actions

- [ ] Route to existing chain_client_paid_me_1800_for_a_project_my_t — already wired
- [ ] Add eas_landing_chatbot_proposal_gen.py: input=business URL, output=personalized proposal + price anchored at $1800
- [ ] Plug into local_biz_website_scraper.py (top SaaS candidate, score 95) to auto-source targets
- [ ] Wire Stripe Payment Link generation on proposal acceptance
- [ ] Cron: 9 AM weekdays — pull 5 fresh targets from scraper, generate proposals, add to cold outbound queue
- [ ] Subagent: generate 3 tweet variants + 1 Reddit post from this case study TODAY (Rule 9)

## Tooling

```json
{
  "browser": "playwright for local biz scraping",
  "email": "existing cold outbound scripts (AUTOMATIONS/cold_email_pipeline.py)",
  "content": "engagement_bait_converter.py for case study posts",
  "delivery": "Claude Code for page gen, Stripe Payment Link for invoicing"
}
```
