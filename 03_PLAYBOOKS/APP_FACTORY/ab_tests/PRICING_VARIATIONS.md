# Pricing A/B Test Variations

Ready-to-test pricing strategies and display formats.

---

## Price Point Tests

### Test 1: Weekly Subscription Price Points

**Hypothesis:** Higher price with stronger value prop converts similarly with better LTV.

| Variant | Price | Positioning |
|---------|-------|-------------|
| A | $7.99/week | "Most affordable" |
| B | $9.99/week | Standard |
| C | $12.99/week | "Premium experience" |

**Expected outcomes:**
- A: Highest conversion, lowest LTV
- B: Balanced conversion and LTV
- C: Lowest conversion, highest LTV

**Winner criteria:** Highest total revenue per 1000 users

---

### Test 2: Monthly Subscription Price Points

**Hypothesis:** $9.99 is the psychological sweet spot.

| Variant | Price | Annual Equivalent |
|---------|-------|-------------------|
| A | $7.99/month | $95.88/year |
| B | $9.99/month | $119.88/year |
| C | $12.99/month | $155.88/year |

---

### Test 3: Annual Subscription Price Points

**Hypothesis:** Perceived savings drives annual upgrades.

| Variant | Price | Monthly Equivalent | Savings vs Monthly |
|---------|-------|-------------------|-------------------|
| A | $59.99/year | $5.00/mo | 50% |
| B | $79.99/year | $6.67/mo | 33% |
| C | $99.99/year | $8.33/mo | 17% |

---

## Price Display Format Tests

### Test 4: Monthly vs Annual Framing

**Hypothesis:** Showing monthly equivalent increases annual plan uptake.

**Variant A: Simple Annual**
```
Annual Plan: $79.99/year
```

**Variant B: Monthly Equivalent**
```
Annual Plan: $79.99/year
(Just $6.67/month)
```

**Variant C: Savings Highlight**
```
Annual Plan: $79.99/year
Save $40 vs monthly!
```

**Variant D: Daily Framing**
```
Annual Plan: $79.99/year
Less than $0.22/day
```

---

### Test 5: Crossed Out Pricing

**Hypothesis:** Anchor pricing increases perceived value.

**Variant A: No Anchor**
```
Pro Plan: $9.99/month
```

**Variant B: Higher Anchor**
```
Pro Plan: ~~$19.99~~ $9.99/month
(50% OFF - Limited Time)
```

**Variant C: Competitor Anchor**
```
Pro Plan: $9.99/month
(Similar apps charge $20+)
```

---

## Tier Structure Tests

### Test 6: Two vs Three Tiers

**Hypothesis:** Middle tier becomes anchor, increases Pro uptake.

**Variant A: Two Tiers**
```
FREE           PRO
$0             $9.99/mo
Basic access   Everything
```

**Variant B: Three Tiers**
```
FREE      PRO        ELITE
$0        $9.99/mo   $19.99/mo
Basic     Premium    Everything+
```

**Variant C: Three Tiers (Recommended Highlight)**
```
FREE      PRO ★BEST VALUE    ELITE
$0        $9.99/mo            $19.99/mo
Basic     Premium             Everything+
```

---

### Test 7: Feature Differentiation

**Hypothesis:** Clear feature gates increase upgrade motivation.

**Variant A: Soft Limits**
```
FREE: 10 actions/day
PRO: Unlimited actions
```

**Variant B: Hard Feature Gates**
```
FREE: Basic features only
PRO: Advanced features unlocked
```

**Variant C: Usage + Features**
```
FREE: 10 actions/day, basic features
PRO: Unlimited actions, all features, priority support
```

---

## Lifetime Pricing Tests

### Test 8: Lifetime Option Impact

**Hypothesis:** Lifetime option increases immediate revenue without cannibalizing subscriptions.

**Variant A: No Lifetime**
```
Monthly: $9.99/mo
Annual: $79.99/year
```

**Variant B: With Lifetime**
```
Monthly: $9.99/mo
Annual: $79.99/year
Lifetime: $199.99 (one-time)
```

**Variant C: Limited Lifetime**
```
Monthly: $9.99/mo
Annual: $79.99/year
Lifetime: $149.99 (FOUNDERS PRICE - 47 left)
```

---

### Test 9: Lifetime Pricing Level

**Hypothesis:** 2x annual is optimal lifetime price point.

| Variant | Lifetime Price | Multiple of Annual |
|---------|---------------|-------------------|
| A | $149.99 | 1.9x |
| B | $199.99 | 2.5x |
| C | $299.99 | 3.7x |

---

## Bundle Pricing Tests

### Test 10: App Bundle Discount

**Hypothesis:** Bundles increase average order value.

**Variant A: Single App**
```
AIWriter Pro: $9.99/month
```

**Variant B: Bundle Offer**
```
AIWriter Pro: $9.99/month
OR
All 3 Apps Bundle: $19.99/month (Save 33%)
- AIWriter Pro
- FitTracker Pro
- HeartSync Premium
```

**Variant C: Bundle Default**
```
Complete Suite: $19.99/month
- AIWriter Pro
- FitTracker Pro
- HeartSync Premium

Or single app: $9.99/month
```

---

## Trial Structure Tests

### Test 11: Trial Length

**Hypothesis:** 7-day trial converts better than 3-day.

| Variant | Trial Length | Conversion Window |
|---------|--------------|-------------------|
| A | 3-day trial | Faster decision |
| B | 7-day trial | More value seen |
| C | 14-day trial | Maximum exposure |
| D | No trial (direct purchase) | Committed buyers only |

---

### Test 12: Trial Type

**Hypothesis:** Payment upfront trials convert higher.

**Variant A: Free Trial (No Card)**
```
Start 7-Day Free Trial
No credit card required
```

**Variant B: Free Trial (Card Required)**
```
Start 7-Day Free Trial
Card required, cancel anytime
```

**Variant C: Paid Trial**
```
Try 7 Days for $0.99
Then $9.99/month
```

---

## Currency/Regional Tests

### Test 13: Local Currency Display

**Hypothesis:** Local currency increases trust and conversion.

**Variant A: USD Only**
```
$9.99/month (all regions)
```

**Variant B: Local Currency**
```
UK: £7.99/month
EU: €8.99/month
AU: $14.99 AUD/month
```

**Variant C: Local + USD Equivalent**
```
UK: £7.99/month (~$9.99 USD)
```

---

### Test 14: Regional Pricing

**Hypothesis:** Lower prices in emerging markets increases overall revenue.

| Region | Standard | Test Price |
|--------|----------|------------|
| US/UK/EU | $9.99 | $9.99 |
| LATAM | $9.99 | $4.99 |
| India | $9.99 | $2.99 |
| SEA | $9.99 | $3.99 |

---

## Psychological Pricing Tests

### Test 15: Odd vs Round Pricing

**Hypothesis:** Charm pricing ($X.99) outperforms round numbers.

| Variant | Price | Psychology |
|---------|-------|------------|
| A | $9.99 | Charm pricing |
| B | $10.00 | Round number |
| C | $9.97 | Precise (seems calculated) |
| D | $9 | Minimal friction |

---

### Test 16: Price Ending

**Hypothesis:** Different endings signal different value.

| Variant | Annual Price | Signal |
|---------|--------------|--------|
| A | $79.99 | Value/deal |
| B | $80.00 | Premium/quality |
| C | $77.00 | Calculated/fair |

---

## Implementation Templates

### RevenueCat Offering Structure

```json
{
  "offerings": {
    "default": {
      "identifier": "default",
      "packages": [
        {
          "identifier": "weekly",
          "product_id": "pro_weekly_999"
        },
        {
          "identifier": "monthly",
          "product_id": "pro_monthly_999"
        },
        {
          "identifier": "annual",
          "product_id": "pro_annual_7999"
        }
      ]
    },
    "experiment_higher_price": {
      "identifier": "higher_price",
      "packages": [
        {
          "identifier": "weekly",
          "product_id": "pro_weekly_1299"
        },
        {
          "identifier": "monthly",
          "product_id": "pro_monthly_1299"
        },
        {
          "identifier": "annual",
          "product_id": "pro_annual_9999"
        }
      ]
    }
  }
}
```

### App Store Product IDs

Create products for each price point:
```
com.app.pro_weekly_799
com.app.pro_weekly_999
com.app.pro_weekly_1299
com.app.pro_monthly_799
com.app.pro_monthly_999
com.app.pro_monthly_1299
com.app.pro_annual_5999
com.app.pro_annual_7999
com.app.pro_annual_9999
com.app.pro_lifetime_14999
com.app.pro_lifetime_19999
com.app.pro_lifetime_29999
```

---

## Measurement Framework

### Primary Metrics
- Conversion rate (paywall views to purchase)
- Revenue per user (RPU)
- Average revenue per paying user (ARPPU)

### Secondary Metrics
- Plan distribution (weekly/monthly/annual/lifetime)
- Refund rate by price point
- 30-day LTV by price point
- Churn rate by price point

### Analysis Requirements
- Minimum 500 conversions per variant
- 14+ day test duration (capture billing cycles)
- Segment by acquisition source (paid users less price sensitive)

---

## Quick Reference: What to Test First

### New App Launch
1. Price point test (find optimal price)
2. Trial vs no trial
3. Two vs three tiers

### Established App (Optimizing)
1. Price display format
2. Annual vs monthly default
3. Lifetime option

### Revenue Plateau
1. Higher price point
2. Premium tier addition
3. Bundle offers

---

*Remember: Price tests require longer duration (14-21 days) to capture full billing cycles and refund patterns.*
