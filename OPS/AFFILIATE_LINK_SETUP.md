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



---

## Pending Enhancement (ALPHA9026, Score: 30)

**Source:** r/growthhacking (Reddit) | **URL:** https://old.reddit.com/r/GrowthHacking/comments/1rm94lz/how_id_use_openclaw_to_replace_a_15kmo_ops/
**Added:** 2026-03-08T04:05:02-04:00

How I’d use OpenClaw to replace a $15k/mo ops + marketing stack (real setup, not theory) [Score: 16]



---

## Pending Enhancement (ALPHA23874, Score: 62)

**Source:** swarm_opportunity_scanner | **URL:** https://www.upwork.com/freelance-jobs/apply/White-Label-Partner-Needed-for-Roofing-Automation-Agency_~022031841531673860891/
**Added:** 2026-03-13T15:45:01-04:00

White-label AI chatbot platforms now start at $70-99/mo (Trillet $99/mo 3 sub-accounts, BotSailor $70/mo). Build VERTICAL-SPECIFIC packages: RoofBot, DentalAssist AI, LegalIntake AI. Charge $199-499/mo per client + $499 setup. 50-85% margins. Live Upwork demand confirmed.



---

## Pending Enhancement (ALPHA25364, Score: 29)

**Source:** @mattpocockuk (high-signal-accounts) | **URL:** https://x.com/Salad_Chefs/status/2032135402052825312/analytics
**Added:** 2026-03-14T09:45:01-04:00

90% cheaper. 5 min setup. $0 token fees.
SaladCloud saves you lettuce.



---

## Pending Enhancement (ALPHA25266, Score: 23)

**Source:** @wesocialgrowth | **URL:** https://x.com/getzirrus/status/2023412710709616947/analytics
**Added:** 2026-03-14T12:48:46-04:00

Fewer bills. More savings. Bundle mobile with internet for just $25/month per line. Plus, free home delivery and setup.



---

## Pending Enhancement (ALPHA25307, Score: 29)

**Source:** producthunt | **URL:** https://www.producthunt.com/products/gstack
**Added:** 2026-03-14T12:48:46-04:00

GStack - Use Garry Tan exact Claude Code setup (YC president config as a product)



---

## Pending Enhancement (ALPHA98788, Score: 35)

**Source:** @seanb2b (high-signal-accounts) | **URL:** https://x.com/seanb2b/status/2032488883670168055
**Added:** 2026-03-14T18:45:01-04:00

Ashao 
→ Closed $3K setup + $300/meeting
→ 50% upfront, 50% after first call

$97 → $3K collected + recurring

Stop trying to figure it out yourself 

http://
closingclientsgroup.com

