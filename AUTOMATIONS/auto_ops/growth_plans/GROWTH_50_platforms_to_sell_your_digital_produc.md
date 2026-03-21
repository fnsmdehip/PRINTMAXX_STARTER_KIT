# Growth Plan: 50 platforms to sell your digital product (and it's free)

**Created:** 2026-03-20 13:50
**Venture:** PRODUCT
**Budget Tier:** FREE
**Revenue Est:** $50-300/mo

---

## Tactics

1. Cross-list identical products with niche-specific titles per platform (Gumroad=indie, Payhip=creator, Sellfy=solopreneur)
2. SEO-optimize each listing differently to capture long-tail searches per marketplace
3. Use platform-native affiliate programs where available to get others promoting listings

## Budget Tier Strategies

### FREE
List on all free-tier platforms (Gumroad, Payhip, Sellfy, Ko-fi, Lemon Squeezy, Itch.io, Creative Market, Stan Store free tier). Optimize titles and descriptions per platform SEO. Cross-link between listings.

### LOW
$0-50/mo: Boost 1-2 top-performing listings with platform-native promoted placement (Gumroad Discover, Creative Market featured)

### MID
$50-200/mo: Run targeted ads to highest-converting platform listings. A/B test pricing across platforms to find optimal price point per audience.

## Daily Actions

- [ ] Build platform_db.json with 50 marketplaces: name, URL, fees, API availability, product categories, free tier limits
- [ ] Cross-reference with DIGITAL_PRODUCTS/ready_to_sell/ and PRODUCTS/listings/ to build coverage matrix
- [ ] Generate platform-specific listing copy for each product using claude -p (title, description, tags optimized per platform)
- [ ] Output prioritized signup queue sorted by: no-fee platforms first, largest audience second, API-listable third
- [ ] Weekly cron checks for new platforms and coverage gaps, appends to HUMAN action queue in PERSISTENT_TASK_TRACKER
- [ ] BLOCKER: Human must create accounts on each platform - script generates exact signup URLs and pre-filled listing text to minimize time

## Tooling

```json
{
  "browser": "none",
  "email": "none",
  "content": "claude -p for generating platform-specific listing copy variants"
}
```
