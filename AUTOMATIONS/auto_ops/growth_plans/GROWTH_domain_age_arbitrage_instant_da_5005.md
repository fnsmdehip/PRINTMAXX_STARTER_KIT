# Growth Plan: domain age arbitrage. instant da. $500-5000 investment.  

**Created:** 2026-03-20 18:09
**Venture:** BROKERING
**Budget Tier:** FREE
**Revenue Est:** $0/mo now (scanner phase), $200-800/mo when brokering active, $1000-3000/mo if buying domains at Phase 2+

---

## Tactics

1. Post weekly 'expired domain deals' thread on Twitter to build SEO audience
2. Cross-post domain finds to r/juststart r/SEO r/Domains for inbound broker leads
3. Build email list of domain buyers from SEO communities — becomes distribution for brokering

## Budget Tier Strategies

### FREE
Organic Twitter threads showing domain finds with DA scores, Reddit posts in SEO subs, build scanner as open-source tool for backlinks + credibility

### LOW
$0-50/mo: Register 1-2 high-DA domains under $50 as proof-of-concept, flip for 3-5x on Flippa/Odys

### MID
$50-200/mo: Buy 2-3 aged domains monthly, build thin affiliate sites on them, 301 redirect link juice to money sites

## Daily Actions

- [ ] Build domain_age_arbitrage_scanner.py using Playwright to scrape expireddomains.net daily drops
- [ ] Score each domain: DA estimate (Moz free API or scrape), spam ratio, niche classification, archive.org page count
- [ ] Output top 20 daily to LEDGER/DOMAIN_OPPORTUNITIES.csv with columns: domain, da, dr, backlinks, spam_pct, niche, est_price, flip_value
- [ ] Add cron at 5 AM daily
- [ ] When brokering venture has leads: match domain opportunities to buyer requests
- [ ] At Phase 2+ ($1K+ capital): buy top-scored domains, build affiliate content on aged DA, or 301 to existing PRINTMAXX sites for SEO boost

## Tooling

```json
{
  "browser": "playwright for expireddomains.net scraping",
  "email": "none",
  "content": "content_factory for SEO community posts"
}
```
