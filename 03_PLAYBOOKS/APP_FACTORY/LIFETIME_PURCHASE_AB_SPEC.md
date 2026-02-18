# Lifetime purchase A/B testing spec for Lock Apps

**Created:** 2026-02-02 (MEGA_094 CG-03)
**Alpha Sources:** ALPHA972912, ALPHA972913, ALPHA972919, ALPHA465, SYN034
**Applies to:** PrayerLock, WalkToUnlock, StudyLock, biomaxx
**Prerequisite:** RevenueCat Experiments SDK integrated

---

## the problem

43% of consumers now prefer hybrid monetization over pure subscription. subscription fatigue is real. the average American has 6.7 active subscriptions and 42% say they have "too many."

meanwhile lifetime purchases are making a comeback. Calm sold 1M+ lifetime memberships at $299. Headspace tested $399 lifetime. multiple Lock App competitors offer lifetime as their premium tier.

the question: for a $39.99-$59.99/yr screen blocker app, does adding a lifetime option increase or cannibalize revenue?

---

## hypothesis

adding a lifetime purchase option at 3x annual price will:
1. increase overall conversion rate by 8-15% (captures subscription-averse users)
2. NOT significantly cannibalize annual subscriptions (different buyer psychology)
3. generate 20-30% higher first-month revenue from cash-forward buyers
4. reduce perceived risk ("I own this forever" vs "another subscription")

the risk: if >40% of new subscribers choose lifetime over annual, LTV drops. need kill switch.

---

## test design

### variant A: current (subscription only)

```
PAYWALL SCREEN:
┌─────────────────────────────┐
│   Annual (BEST VALUE)       │
│   $4.17/mo billed at $49.99 │
│   Save 48%                  │
│   ☑ (pre-selected)         │
├─────────────────────────────┤
│   Monthly                   │
│   $7.99/mo                  │
│                             │
└─────────────────────────────┘
    [ Start Free Trial ]
```

### variant B: subscription + lifetime (3-option)

```
PAYWALL SCREEN:
┌─────────────────────────────┐
│   Lifetime (OWN FOREVER)    │
│   $149.99 one-time          │
│   Never pay again           │
├─────────────────────────────┤
│   Annual (MOST POPULAR)     │
│   $4.17/mo billed at $49.99 │
│   Save 48%                  │
│   ☑ (pre-selected)         │
├─────────────────────────────┤
│   Monthly                   │
│   $7.99/mo                  │
│                             │
└─────────────────────────────┘
    [ Start Free Trial ]
```

### variant C: lifetime-first (reverse anchor)

```
PAYWALL SCREEN:
┌─────────────────────────────┐
│   Lifetime (BEST VALUE)     │
│   $149.99 one-time          │
│   = 2.5 years then FREE     │
│   ☑ (pre-selected)         │
├─────────────────────────────┤
│   Annual                    │
│   $59.99/year               │
│   $5.00/month               │
├─────────────────────────────┤
│   Monthly                   │
│   $9.99/mo                  │
│                             │
└─────────────────────────────┘
    [ Get Lifetime Access ]
```

note: variant C uses higher monthly/annual prices to make lifetime look better. the psychology is different. instead of annual as target, lifetime is the target with subscriptions as decoy.

---

## pricing per app

| App | Monthly | Annual | Lifetime | Lifetime / Annual Ratio |
|-----|---------|--------|----------|------------------------|
| PrayerLock | $5.99 | $39.99 | $99.99 | 2.5x |
| WalkToUnlock | $7.99 | $49.99 | $149.99 | 3.0x |
| StudyLock | $6.99 | $49.99 | $129.99 | 2.6x |
| biomaxx | $7.99 | $59.99 | $179.99 | 3.0x |

**Why these ratios:**
- below 2x: cannibalization risk (too cheap to not choose lifetime)
- 2.5-3x: sweet spot (attractive for committed users, most still choose annual)
- above 4x: nobody picks lifetime (defeats the purpose)

PrayerLock at 2.5x because faith audience has higher commitment/lower churn (pray every day = strong habit). biomaxx at 3.0x because supplement tracking is less habitual.

---

## RevenueCat experiment config

```json
{
  "experiment_name": "lifetime_purchase_test",
  "variants": [
    {
      "name": "control_subscription_only",
      "weight": 34,
      "offerings": ["monthly", "annual"]
    },
    {
      "name": "subscription_plus_lifetime",
      "weight": 33,
      "offerings": ["monthly", "annual", "lifetime"]
    },
    {
      "name": "lifetime_first_reverse_anchor",
      "weight": 33,
      "offerings": ["monthly_premium", "annual_premium", "lifetime"],
      "default_selection": "lifetime"
    }
  ],
  "minimum_sample_size": 500,
  "primary_metric": "revenue_per_install",
  "secondary_metrics": [
    "conversion_rate",
    "avg_revenue_per_paying_user",
    "lifetime_selection_rate",
    "day_7_retention",
    "day_30_churn"
  ],
  "kill_criteria": {
    "lifetime_selection_rate_above": 0.45,
    "conversion_rate_drop_below": 0.02,
    "revenue_per_install_drop_below_control": 0.15
  }
}
```

---

## metrics to track

### primary (determines winner)

**Revenue per install (RPI).** Not conversion rate. Not ARPU. RPI captures both conversion AND value in one number.

formula: total revenue / total installs

why: a variant could have lower conversion but higher RPI because lifetime buyers pay more upfront. RPI is the only metric that captures the full picture.

### secondary (context)

| Metric | Why It Matters | Kill Threshold |
|--------|---------------|----------------|
| Conversion rate | Overall paywall effectiveness | < 2% = investigate |
| Lifetime selection rate | Cannibalization signal | > 45% = too much cannibalization |
| Annual selection rate | Core metric health | < 30% of subscribers = concern |
| ARPU (avg revenue per paying user) | Revenue quality | Down > 20% from control = concern |
| Day 7 retention | Early engagement | Down > 15% from control |
| Day 30 churn | Subscription health | Up > 10% from control |
| Refund rate (lifetime) | Buyer's remorse | > 8% = price too high |

### calculated (post-experiment)

| Metric | Formula |
|--------|---------|
| Projected 12-month revenue per user | (% monthly x 12 x monthly price) + (% annual x annual price) + (% lifetime x lifetime price) |
| Breakeven month for lifetime | lifetime price / annual price x 12 |
| Cannibalization rate | (control annual % - variant annual %) / control annual % |
| Net revenue impact | variant RPI / control RPI |

---

## minimum sample size

**Per variant: 500 installs minimum.**

Based on:
- Expected conversion rate: 3-5% (hard paywall Lock Apps)
- Minimum detectable effect: 20% (we need to see a meaningful difference)
- Statistical power: 80%
- Confidence level: 95%

**At 50 installs/day per app: 10 days per variant = 30 days total.**
**At 100 installs/day: 5 days per variant = 15 days total.**

don't call the experiment early. subscription fatigue is real but so is anchoring bias. early movers to lifetime may not represent the population.

---

## kill criteria (stop experiment if)

| Trigger | Action | Why |
|---------|--------|-----|
| Lifetime selection > 45% | Stop variant C | Too much cannibalization, long-term revenue at risk |
| Conversion < 2% (any variant) | Investigate immediately | Something fundamentally broken |
| Revenue per install < 85% of control | Stop underperforming variant | Clear loser |
| Refund rate > 8% on lifetime | Reduce lifetime price by 20% | Price too high for perceived value |

---

## implementation order

**Phase 1: RevenueCat product setup (before experiment)**
1. Create lifetime entitlement in RevenueCat for each app
2. Configure lifetime as non-renewing purchase (NOT subscription)
3. Set up offerings: control (monthly + annual), variant B (monthly + annual + lifetime), variant C (premium monthly + premium annual + lifetime)
4. Create experiment with 34/33/33 split
5. Test purchase flow in sandbox

**Phase 2: paywall UI (code changes)**
1. Update paywall component to accept 2 or 3 pricing options
2. Add "OWN FOREVER" or "BEST VALUE" badge for lifetime
3. Add "= X years then FREE" calculation below lifetime price
4. Ensure pre-selection works correctly per variant (annual for B, lifetime for C)
5. Add "never pay again" subtext for lifetime option

**Phase 3: launch + monitor**
1. Enable experiment in RevenueCat dashboard
2. Monitor daily: conversion rate, selection rate, revenue per install
3. Check kill criteria daily for first 7 days
4. Weekly review after day 7
5. Call experiment at 500+ installs per variant OR 30 days (whichever first)

---

## expected outcomes

| Scenario | Probability | Impact |
|----------|------------|--------|
| Variant B wins (sub + lifetime) | 45% | 8-15% RPI increase. Lifetime captures subscription-averse users without cannibalizing annual. |
| Variant A wins (sub only) | 30% | Lifetime confuses users or cannibalizes annual too much. Keep current pricing. |
| Variant C wins (lifetime-first) | 15% | Big surprise. Lock Apps may be better as one-time purchase products (strong habit = less need for recurring motivation). |
| Inconclusive | 10% | Need more data. Extend to 1000 installs per variant. |

**Most likely winner: Variant B.** Adding lifetime as a third option typically increases overall conversion 8-15% without significant cannibalization, because the type of person who buys lifetime was NOT going to buy annual. They were going to leave. Lifetime captures the "I don't want another subscription" segment.

---

## cross-pollination

| Product | How This Applies |
|---------|-----------------|
| Gumroad PDFs | Already have one-time pricing. Test subscription (monthly updates) vs one-time. |
| Cold email service | Test project-based ($1000 setup) vs monthly retainer ($500/mo) vs hybrid ($750 setup + $300/mo) |
| Newsletter (Beehiiv) | Test paid tier: monthly vs annual vs lifetime archive access |
| Notion templates | Already one-time. Test adding annual "template club" subscription alongside individual purchases. |

the same subscription fatigue insight applies across all revenue channels. test everywhere.

---

## references

- ALPHA972912: Subscription fatigue 43% hybrid monetization. Lifetime purchase revival.
- ALPHA972913: Digital products $124B -> $416B by 2030. One-time purchase remains dominant format.
- ALPHA465: Hard paywalls 8x revenue. 80% conversions during onboarding.
- SYN034: Hybrid Monetization Subscription+Lifetime (synergy score 93)
- PAYWALL_PSYCHOLOGY_AB_PLAYBOOK.md: Existing pricing psychology + onboarding flow research
- Calm: 1M+ lifetime at $299. Headspace $399 lifetime test.
