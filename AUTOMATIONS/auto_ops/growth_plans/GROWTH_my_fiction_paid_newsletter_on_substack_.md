# Growth Plan: My fiction paid newsletter on Substack, Commercial Fiction C

**Created:** 2026-03-20 13:50
**Venture:** CONTENT
**Budget Tier:** FREE
**Revenue Est:** $200-800/mo by month 3, $1500-3000/mo by month 6 (assuming 5-10% free-to-paid conversion at $8/mo, need 200-400 paid subs)

---

## Tactics

1. Cross-promote newsletter in every tweet thread CTA (already generating 3+ tweets/session)
2. Repurpose top-performing CONTENT/social posts as newsletter deep-dives
3. Free tier first 8 weeks to build subscriber base before paywall flip
4. Guest-post swaps with other small Substack writers in adjacent niches
5. Embed newsletter signup in all 47 deployed landing pages as exit-intent or footer CTA
6. Use engagement_bait_converter.py to turn each newsletter into 3 social posts driving signups

## Budget Tier Strategies

### FREE
Cross-promote via existing 47 landing pages + social channels. Repurpose ALPHA_STAGING insights as newsletter content. Reply-bait on Twitter linking to free issues. Substack recommendation network (free cross-promo with other writers).

### LOW
$10-30/mo: Substack boost feature to get recommended to other readers. Small Twitter ad spend on best-performing teaser tweets.

### MID
$50-150/mo: Paid Substack promotion slots. Sponsor small podcasts in niche. LinkedIn newsletter ads targeting solopreneurs.

## Daily Actions

- [ ] 1. Create Substack account in strongest PRINTMAXX niche (Claude Code / AI solopreneur tools — highest existing content volume)
- [ ] 2. Build substack_newsletter_pipeline.py: pulls week's best alpha + content → Claude drafts → formats for Substack API
- [ ] 3. Generate first 4 issues as backlog before launch (subagent task)
- [ ] 4. Add newsletter CTA to all 47 deployed landing pages (footer + exit intent)
- [ ] 5. Wire into content_factory chain: every social post batch includes 1 newsletter teaser
- [ ] 6. Cron Mon+Thu 5AM: auto-draft, human review queue, publish
- [ ] 7. Week 8: flip to paid tier ($8/mo or $70/yr), keep 1 free post per month as funnel
- [ ] 8. Add KPI tracking to KPI_DASHBOARD.md

## Tooling

```json
{
  "browser": "none",
  "email": "substack native (free)",
  "content": "claude -p content generation + content_repurposer.py"
}
```
