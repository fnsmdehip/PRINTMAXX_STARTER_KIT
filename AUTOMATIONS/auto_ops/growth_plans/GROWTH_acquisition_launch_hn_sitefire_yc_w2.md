# Growth Plan: [ACQUISITION] Launch HN: Sitefire (YC W26) – Automating acti

**Created:** 2026-03-21 12:40
**Venture:** EAS
**Budget Tier:** FREE
**Revenue Est:** $500-3000/mo (3-6 EAS clients at $500-1000/mo GEO retainer, or resell audits to agencies at $200/audit)

---

## Tactics

1. Post GEO audit results as Twitter content — 'We checked 50 SaaS brands in AI search. Only 6% appeared. Here's who won and why.'
2. Create HN comment thread engagement around Sitefire launch — position as having done this manually before their tool existed
3. LinkedIn cold DM to agency owners: 'Your clients are invisible to ChatGPT. I built a free audit. Want to see your score?'
4. Reddit posts in r/marketing r/SEO r/ChatGPT about GEO — drive inbound to free audit page
5. Build free GEO audit landing page (surge.sh, 1 hour) — collects email, runs audit, gates full report behind email capture

## Budget Tier Strategies

### FREE
Perplexity free tier for citation checks, claude -p for report gen, surge.sh landing page, manual cold email via Gmail. Target 5 outreaches/day. Repurpose every audit as Twitter thread content.

### LOW
$30/mo Perplexity Pro API for bulk queries + $20 Apollo for lead emails = $50/mo. Scale to 50 audits/day. Automate email send via SMTP script.

### MID
$100 Instantly for warmed inboxes + $50 Perplexity API = $150/mo. 200 audits/day. A/B test subject lines. Target marketing agencies as resellers ($500-1500/mo retainer).

## Daily Actions

- [ ] 1. Build geo_audit_pipeline.py: accepts business name + category → queries Perplexity for 10 category terms → checks if domain appears in AI answers → returns citation rate %
- [ ] 2. Build prospect list: scrape 200 local/SMB businesses from existing leads pipeline (191K hot leads already exist in LEDGER) — filter for ones with websites but no GEO presence
- [ ] 3. Generate audit reports for top 50 prospects using claude -p in parallel (5 subagents, 10 each)
- [ ] 4. Cold email via chain_cold_outbound hook — subject: 'AI search doesn't know [Business] exists — here's proof' — attach 1-page audit
- [ ] 5. Build free audit landing page at geo-audit.surge.sh — captures email, runs auto-audit, gates full report (email nurture → upsell to $500/mo GEO retainer)
- [ ] 6. Wire cron: daily 7 AM → 20 new audits → 10 cold emails → report results to KPI dashboard
- [ ] 7. Generate 3 Twitter posts from audit data: stat-based posts about AI citation gaps in specific niches

## Tooling

```json
{
  "browser": "playwright (Perplexity scraping) + requests (DuckDuckGo AI fallback)",
  "email": "custom SMTP script (free) \u2192 Instantly at LOW tier",
  "content": "engagement_bait_converter.py \u2192 GEO angle posts",
  "ai_query": "Perplexity API free tier + direct HTTP to ChatGPT search endpoint"
}
```
