# Affiliate Link Setup Guide

## STATUS: ACTION REQUIRED
Your landing pages are live but affiliate links have **placeholder IDs**. Sign up for each program below and replace the placeholders.

---

## Live Funnel Pages

| Page | URL | Status |
|------|-----|--------|
| AI Stack 2026 | https://ai-stack-2026.surge.sh | LIVE, needs real affiliate IDs |
| ConvertKit vs Beehiiv | https://convertkit-vs-beehiiv.surge.sh | LIVE, needs real affiliate IDs |

---

## Programs to Sign Up For (by commission priority)

### 1. ConvertKit (30% recurring lifetime) - HIGHEST PRIORITY
- **Sign up:** https://convertkit.com/affiliate
- **Commission:** 30% recurring on all payments, lifetime
- **Cookie:** 30 days
- **Payout:** Monthly via PayPal or Stripe
- **Your ref link format:** `https://convertkit.com?lmref=YOUR_REF_ID`
- **Replace in files:** Search for `REPLACE_CONVERTKIT_REF_ID` in:
  - `LANDING/app-marketing-pages/ai-stack-2026/index.html`
  - `LANDING/app-marketing-pages/convertkit-vs-beehiiv/index.html`
- **Math:** 10 referrals at $29/mo = $87/mo passive income. Compounds monthly.

### 2. Beehiiv (20% recurring)
- **Sign up:** https://www.beehiiv.com/partners
- **Commission:** 20% recurring
- **Cookie:** 30 days
- **Payout:** Monthly
- **Your ref link format:** `https://www.beehiiv.com/?via=YOUR_USERNAME`
- **Replace in files:** Search for `REPLACE_BEEHIIV_REF_ID` in:
  - `LANDING/app-marketing-pages/ai-stack-2026/index.html`
  - `LANDING/app-marketing-pages/convertkit-vs-beehiiv/index.html`
- **Math:** 10 referrals at $49/mo = $98/mo passive income.

### 3. Gumroad (varies)
- **Sign up:** https://gumroad.com/affiliates
- **Commission:** Set by each product creator (typically 10-30%)
- **Your ref link format:** `https://gumroad.com/a/YOUR_AFFILIATE_ID`
- **Replace in files:** Search for `REPLACE_GUMROAD_AFF_ID` in:
  - `LANDING/app-marketing-pages/ai-stack-2026/index.html`

---

## How to Replace IDs

After signing up, run this in terminal from project root:

```bash
# ConvertKit
sed -i '' 's/REPLACE_CONVERTKIT_REF_ID/your_actual_ref_id/g' LANDING/app-marketing-pages/ai-stack-2026/index.html
sed -i '' 's/REPLACE_CONVERTKIT_REF_ID/your_actual_ref_id/g' LANDING/app-marketing-pages/convertkit-vs-beehiiv/index.html

# Beehiiv
sed -i '' 's/REPLACE_BEEHIIV_REF_ID/your_actual_username/g' LANDING/app-marketing-pages/ai-stack-2026/index.html
sed -i '' 's/REPLACE_BEEHIIV_REF_ID/your_actual_username/g' LANDING/app-marketing-pages/convertkit-vs-beehiiv/index.html

# Gumroad
sed -i '' 's/REPLACE_GUMROAD_AFF_ID/your_actual_gumroad_id/g' LANDING/app-marketing-pages/ai-stack-2026/index.html
```

Then redeploy:
```bash
cd LANDING/app-marketing-pages/ai-stack-2026 && npx surge . ai-stack-2026.surge.sh
cd LANDING/app-marketing-pages/convertkit-vs-beehiiv && npx surge . convertkit-vs-beehiiv.surge.sh
```

---

## Click Tracking

All affiliate links fire GoatCounter events on click. Check:
- https://printmaxx.goatcounter.com
- Events named: `aff-click-convertkit`, `aff-click-beehiiv`, `aff-click-cursor`, etc.

This tells you which tools get the most clicks before you even have affiliate accounts set up.

---

## Revenue Projection (Conservative)

| Month | Traffic/page | Clicks (5%) | Conversions (10%) | Monthly Commission |
|-------|-------------|-------------|-------------------|-------------------|
| 1 | 200 | 10 | 1 | $8.70 |
| 3 | 500 | 25 | 2-3 | $20-26 |
| 6 | 1,500 | 75 | 7-8 | $60-70 |
| 12 | 3,000 | 150 | 15 | $130+ (recurring) |

Note: These compound. By month 12, your month-1 referrals are still paying. Recurring commissions stack.

---

## Next Actions

1. Sign up for ConvertKit affiliate program (5 min)
2. Sign up for Beehiiv partner program (5 min)
3. Replace placeholder IDs (2 min)
4. Redeploy pages (1 min)
5. Post distribution content from `CONTENT/social/affiliate_funnel_posts_mar7.md`
6. Monitor GoatCounter for click data


---

## Pending Enhancement (ALPHA18110, Score: 24)

**Source:** @whale_alert (high-signal-accounts) | **URL:** https://x.com/TradeZella/status/2023081699437867471/analytics
**Added:** 2026-03-08T01:09:41-05:00

If I could restart trading, I’d follow these:

This alone would’ve saved me $14K and 2 years of pain:

1. Pick one setup and trade it 100 times before judging it.

2. Risk so small that losses feel like nothing. Size up after proof, not confidence.

3. Grade every trade A, B, or

