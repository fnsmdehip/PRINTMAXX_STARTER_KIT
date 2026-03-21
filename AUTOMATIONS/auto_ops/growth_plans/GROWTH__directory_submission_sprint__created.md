# Growth Plan: # DIRECTORY SUBMISSION SPRINT  **Created:** 2026-02-19 **Dea

**Created:** 2026-03-20 18:10
**Venture:** APP
**Budget Tier:** FREE
**Revenue Est:** $0-10/mo

---

## Tactics

1. Submit to 20+ PWA directories (PWA Store, AppScope, Progressive Web Apps list)
2. Cross-link from existing deployed landing pages to directory listings for backlink juice
3. Submit to niche-specific directories (Islamic app directories for Hilal/PrayerLock)

## Budget Tier Strategies

### FREE
Manual submission to free directories (PWA Store, AppScope, AlternativeTo, Product Hunt, SaaSHub). Cross-link from 47 deployed surge sites. Submit to Islamic/Muslim app directories for niche targeting.

### LOW
$10-30 for featured placement on 2-3 mid-tier directories that accept payment

### MID
$50-100 for Product Hunt launch boost + paid directory featured spots

## Daily Actions

- [ ] Read LEDGER/LAUNCH_DIRECTORY_TRACKER.csv and LEDGER/LAUNCH_DIRECTORIES.csv for existing directory list and submission status
- [ ] Cross-reference with deployed apps in OPS/DEPLOYMENT_URLS.md to build submission queue
- [ ] Generate submission payloads (title, description, URL, screenshots, category) for each app×directory pair
- [ ] For directories with open submission forms, use playwright MCP to auto-fill and submit
- [ ] Log submission status back to LAUNCH_DIRECTORY_TRACKER.csv with timestamp
- [ ] Prioritize Hilal/ramadan-tracker for Islamic-specific directories while Ramadan is still active (ends ~Mar 29)

## Tooling

```json
{
  "browser": "playwright for auto-form-fill submissions",
  "email": "none",
  "content": "none"
}
```
