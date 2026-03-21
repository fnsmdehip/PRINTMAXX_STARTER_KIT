# Growth Plan: source viral us products from aliexpress. list on nordic pla

**Created:** 2026-03-20 18:35
**Venture:** PRODUCT
**Budget Tier:** FREE
**Revenue Est:** $200-800/mo

---

## Tactics

1. List same products across ALL 4 Nordic platforms simultaneously for max surface area
2. Use local language SEO in titles — Nordic marketplaces have weak search, easy to rank
3. Price 10-15% below local competitors but 3x above AliExpress cost for healthy margin
4. Seasonal product rotation — Nordic winter gear Oct-Mar, outdoor May-Aug
5. Cross-list winners on Amazon.se (launched 2020, still low competition)

## Budget Tier Strategies

### FREE
Organic listings on finn.no (free tier), tori.fi (free), dba.dk (limited free). SEO-optimized titles in local language. Cross-post to Facebook Marketplace Nordic groups.

### LOW
$20-50/mo for promoted listings on CDON and finn.no boost. A/B test listing photos.

### MID
$100-200/mo for CDON seller subscription + finn.no premium seller account + small Facebook Ads budget targeting Nordic buyers for high-margin products.

## Daily Actions

- [ ] 1. Enhance existing chain_source_viral_us_products_from_aliexpress with Nordic-specific scanner
- [ ] 2. Build nordic_ecom_arbitrage_scanner.py: AliExpress trending → Nordic gap analysis → margin calc with IOSS VAT
- [ ] 3. Add Claude translation layer for NO/SV/DA/FI listing copy generation
- [ ] 4. Calculate landed cost: product + shipping + IOSS VAT (varies by country) + platform fees
- [ ] 5. Output ready-to-list product cards as JSON/CSV with localized titles, descriptions, prices in local currency
- [ ] 6. Cron twice/week (Mon+Thu 7AM) to catch new trending products
- [ ] 7. HUMAN BLOCKER: Create seller accounts on finn.no, cdon.com, dba.dk, tori.fi
- [ ] 8. HUMAN BLOCKER: Set up Klarna/Vipps business account for payment processing
- [ ] 9. HUMAN BLOCKER: Register for IOSS (Import One-Stop Shop) for EU VAT compliance
- [ ] 10. Phase 2 trigger: When 5+ products sell consistently, evaluate EU warehouse (3PL in Poland/Baltics for lowest cost)

## Tooling

```json
{
  "browser": "playwright for marketplace scraping",
  "email": "none",
  "content": "claude -p for translation and listing copy"
}
```
