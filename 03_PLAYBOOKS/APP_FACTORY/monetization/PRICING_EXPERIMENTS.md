# Pricing experiments

Systematic approach to finding optimal price points through controlled testing.

---

## Price point matrix

### Tested price tiers

| Tier | Monthly | Annual | Annual savings | Target conversion |
|------|---------|--------|----------------|-------------------|
| Budget | $4.99 | $29.99 | 50% | 8-12% |
| Standard | $7.99 | $49.99 | 48% | 5-8% |
| Premium | $9.99 | $59.99 | 50% | 3-5% |
| Pro | $14.99 | $99.99 | 44% | 2-4% |

### Price elasticity benchmarks

**Utility apps (calculators, timers, productivity)**
- Sweet spot: $4.99-7.99/month
- Annual conversion: 40-60% of subscribers
- Price sensitivity: High

**Lifestyle apps (fitness, meditation, habits)**
- Sweet spot: $7.99-12.99/month
- Annual conversion: 50-70% of subscribers
- Price sensitivity: Medium

**Niche professional tools**
- Sweet spot: $14.99-29.99/month
- Annual conversion: 60-80% of subscribers
- Price sensitivity: Low

---

## Annual vs monthly ratio tests

### Standard ratios to test

| Ratio | Monthly example | Annual equivalent | Effective monthly | Savings message |
|-------|-----------------|-------------------|-------------------|-----------------|
| 12:8 | $7.99 | $63.92 | $5.33 | Save 33% |
| 12:6 | $7.99 | $47.94 | $4.00 | Save 50% |
| 12:5 | $7.99 | $39.95 | $3.33 | Save 58% |
| 12:4 | $7.99 | $31.96 | $2.66 | Save 67% |

### Test results template

```
Experiment: Annual ratio test
App: [App name]
Duration: 14 days minimum
Traffic: 500+ users per variant

Variant A: 12:6 ratio (50% savings)
Variant B: 12:8 ratio (33% savings)

Metrics:
- Annual subscription rate
- Total revenue per user
- Refund rate
- 30-day retention of annual subscribers
```

### Benchmark data

Industry averages for annual vs monthly split:
- 12:8 ratio: 45% choose annual
- 12:6 ratio: 55% choose annual
- 12:5 ratio: 65% choose annual

Revenue optimization insight: 12:6 ratio typically maximizes total revenue. Going lower increases annual conversion but reduces per-user revenue.

---

## Free trial length tests

### Trial configurations

| Trial length | Pros | Cons | Best for |
|--------------|------|------|----------|
| 3 days | Lower CAC, faster feedback | Less time to show value | Simple apps, clear value prop |
| 7 days | Balance of urgency + time | Standard, no differentiation | Most apps |
| 14 days | Full habit formation | Higher support cost, forget to cancel complaints | Complex apps, habit-based |

### Test framework

**3-day trial test**
```
Hypothesis: Shorter trial creates urgency without sacrificing conversion
Primary metric: Trial-to-paid conversion rate
Secondary metrics:
- Day 1 activation rate
- Feature usage depth
- Support tickets about trial length

Success criteria: Conversion rate within 80% of 7-day trial
```

**7-day trial test (control)**
```
Baseline conversion: X%
Baseline activation: Y%
```

**14-day trial test**
```
Hypothesis: Longer trial allows habit formation, higher retention post-conversion
Primary metric: Trial-to-paid conversion rate
Secondary metrics:
- Day 30 retention of converted users
- Lifetime value (90-day projection)
- Feature adoption depth

Success criteria: LTV increase offsets lower conversion rate
```

### Trial length benchmarks

| Trial length | Avg conversion | 30-day retention | Typical LTV multiplier |
|--------------|----------------|------------------|------------------------|
| 3 days | 4-6% | 70-75% | 0.9x |
| 7 days | 5-8% | 72-78% | 1.0x (baseline) |
| 14 days | 4-7% | 78-85% | 1.15x |

---

## Discount testing framework

### Discount scenarios

**Onboarding discount**
- Timing: Shown at end of onboarding
- Typical offer: 50% off first year
- Duration: 24-48 hour countdown
- Expected lift: 40-60% increase in immediate conversion

**Paywall rejection discount**
- Timing: User dismisses paywall
- Typical offer: 30-40% off
- Duration: One-time offer
- Expected lift: 15-25% of rejectors convert

**Win-back discount**
- Timing: 3-7 days after trial expires
- Typical offer: 50-60% off first period
- Duration: 7 days
- Expected lift: 5-10% of expired trials convert

**Seasonal discounts**
- Timing: Black Friday, New Year, back-to-school
- Typical offer: 40-50% off annual
- Duration: 3-7 days
- Expected lift: 2-3x normal conversion

### Discount percentages to test

| Discount | Perceived value | Revenue impact | Best use case |
|----------|-----------------|----------------|---------------|
| 20% | Low urgency | Minimal revenue loss | Retention offers |
| 30% | Moderate urgency | Acceptable loss | Standard promotions |
| 40% | Strong urgency | Significant loss | Seasonal sales |
| 50% | High urgency | Major loss, high volume | Launch, win-back |
| 60%+ | Devalues product | Use sparingly | Last-resort win-back |

---

## Price testing implementation

### RevenueCat offering structure

```typescript
// offerings configuration
const pricingOfferings = {
  control: {
    monthly: '$7.99',
    annual: '$47.99',
    trial: 7,
  },
  variant_a: {
    monthly: '$9.99',
    annual: '$59.99',
    trial: 7,
  },
  variant_b: {
    monthly: '$4.99',
    annual: '$29.99',
    trial: 7,
  },
};
```

### Test assignment logic

```typescript
function assignPricingVariant(userId: string): string {
  // Consistent assignment based on user ID
  const hash = simpleHash(userId);
  const bucket = hash % 100;

  if (bucket < 33) return 'control';
  if (bucket < 66) return 'variant_a';
  return 'variant_b';
}

function simpleHash(str: string): number {
  let hash = 0;
  for (let i = 0; i < str.length; i++) {
    const char = str.charCodeAt(i);
    hash = ((hash << 5) - hash) + char;
    hash = hash & hash;
  }
  return Math.abs(hash);
}
```

### Statistical significance calculator

```typescript
interface TestResult {
  visitors: number;
  conversions: number;
  revenue: number;
}

function calculateSignificance(
  control: TestResult,
  variant: TestResult
): { significant: boolean; confidence: number; lift: number } {
  const controlRate = control.conversions / control.visitors;
  const variantRate = variant.conversions / variant.visitors;

  const pooledRate = (control.conversions + variant.conversions) /
                     (control.visitors + variant.visitors);

  const standardError = Math.sqrt(
    pooledRate * (1 - pooledRate) *
    (1/control.visitors + 1/variant.visitors)
  );

  const zScore = (variantRate - controlRate) / standardError;
  const confidence = normalCDF(Math.abs(zScore));

  return {
    significant: confidence >= 0.95,
    confidence: confidence,
    lift: ((variantRate - controlRate) / controlRate) * 100,
  };
}
```

---

## Experiment schedule template

### Week 1-2: Baseline measurement
- Track current conversion rates
- Segment by acquisition source
- Establish statistical baseline

### Week 3-4: Price point test
- Run A/B test on monthly price
- Minimum 500 users per variant
- Track conversion + revenue + refunds

### Week 5-6: Annual ratio test
- Test annual savings percentage
- Same traffic requirements
- Track annual vs monthly split

### Week 7-8: Trial length test
- Test 3-day vs 7-day vs 14-day
- Track activation + conversion + retention
- Calculate LTV impact

### Week 9+: Implement winners
- Roll out winning variants
- Monitor for degradation
- Plan next experiment cycle

---

## Key metrics to track

### Primary metrics
- Trial start rate (% of users who start trial)
- Trial-to-paid conversion rate
- Revenue per user (RPU)
- Average revenue per paying user (ARPPU)

### Secondary metrics
- Annual vs monthly subscription ratio
- Refund rate by price point
- Time to conversion (days in trial before converting)
- Feature usage correlation with conversion

### Long-term metrics
- 30/60/90 day retention by price point
- Lifetime value by acquisition variant
- Churn rate by price tier

---

## Common pricing mistakes

1. **Testing too many variables at once**
   - Fix: Change one variable per experiment

2. **Insufficient sample size**
   - Fix: Run until 500+ users per variant minimum

3. **Ending tests too early**
   - Fix: Wait for statistical significance (95%+ confidence)

4. **Ignoring LTV**
   - Fix: Track 90-day revenue, not just immediate conversion

5. **Forgetting currency localization**
   - Fix: Test pricing in top 5 markets separately

6. **Racing to the bottom**
   - Fix: Test higher prices too. $14.99 might convert at 3% but generate more revenue than $4.99 at 8%
