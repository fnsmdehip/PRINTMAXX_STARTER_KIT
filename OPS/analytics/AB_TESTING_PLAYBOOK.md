# A/B Testing Playbook

Complete methodology for running statistically valid A/B tests across apps and marketing.

---

## Quick Reference

**Minimum sample sizes:**
- High-traffic tests: 1,000 per variant
- Medium-traffic: 500 per variant
- Low-traffic: 250 per variant (longer duration)

**Minimum test duration:** 7 days (capture weekly patterns)

**Required confidence:** 95% (p < 0.05)

**Stop conditions:**
- Hit sample size AND 7+ days
- 99% confidence reached early
- Critical bug discovered

---

## 1. What to Test

### App Tests (Priority Order)

**1. Paywall Copy (Highest Impact)**
- Emotional vs feature-based messaging
- Social proof integration
- Urgency/scarcity elements
- Value proposition framing

**2. Pricing**
- Price points ($7.99 vs $9.99 vs $12.99)
- Display format (monthly vs annual equivalent)
- Tier structure (2 vs 3 tiers)
- Anchoring with premium tier

**3. Onboarding**
- Flow length (3 vs 5 vs 7 screens)
- Personalization depth
- First action to complete
- Permission request timing

**4. CTAs**
- Copy (action verbs vs outcomes)
- Visual treatment (color, size, animation)
- Placement (sticky vs static)
- Urgency messaging

### Marketing Tests (Priority Order)

**1. Email**
- Subject lines (question vs statement vs curiosity)
- Personalization level
- Body length
- CTA placement and copy

**2. Paid Ads**
- Creative format (UGC vs polished vs carousel)
- Ad copy approach (story vs features vs social proof)
- Audience targeting
- Placement optimization

**3. Landing Pages**
- Headline approach
- Social proof type
- CTA position
- Form field count

---

## 2. Statistical Significance Calculator

### Manual Calculation

```
Z-score = (p1 - p2) / sqrt(p_pooled * (1 - p_pooled) * (1/n1 + 1/n2))

Where:
- p1 = conversion rate variant A
- p2 = conversion rate variant B
- p_pooled = (conversions_A + conversions_B) / (n1 + n2)
- n1, n2 = sample sizes
```

**Z-score thresholds:**
- 1.65 = 90% confidence
- 1.96 = 95% confidence (minimum for decisions)
- 2.58 = 99% confidence

### Quick Reference Table

| Baseline Conversion | Minimum Detectable Effect | Sample Size (per variant) |
|---------------------|---------------------------|---------------------------|
| 1% | 0.5% (50% lift) | 3,000 |
| 2% | 0.5% (25% lift) | 6,200 |
| 5% | 1% (20% lift) | 4,900 |
| 10% | 2% (20% lift) | 4,300 |
| 20% | 4% (20% lift) | 3,900 |

### Sample Size Formula

```
n = (Z_alpha + Z_beta)^2 * (p1(1-p1) + p2(1-p2)) / (p1 - p2)^2

For 95% confidence, 80% power:
n = 16 * p * (1-p) / (MDE)^2

Where:
- p = baseline conversion rate
- MDE = minimum detectable effect (absolute)
```

---

## 3. Sample Size Requirements

### By Test Type

| Test Type | Typical Baseline | Target MDE | Min Sample/Variant |
|-----------|------------------|------------|-------------------|
| Paywall conversion | 3-5% | 1% absolute | 1,500 |
| Trial to paid | 10-20% | 3% absolute | 1,200 |
| CTA tap rate | 5-15% | 2% absolute | 2,000 |
| Email open rate | 20-35% | 5% absolute | 800 |
| Ad CTR | 1-3% | 0.5% absolute | 3,000 |
| Landing page conversion | 2-5% | 1% absolute | 2,000 |

### Traffic Requirements

**App tests:**
- Need 3,000+ daily active users for weekly tests
- Need 10,000+ DAU for multiple concurrent tests
- Low-traffic apps: run one test at a time, longer duration

**Marketing tests:**
- Email: 5,000+ list size for single test
- Ads: $500+ budget per variant
- Landing pages: 1,000+ weekly visitors

---

## 4. Test Duration Guidelines

### Minimum Duration

| Scenario | Minimum Days |
|----------|--------------|
| High-traffic (10k+ DAU) | 7 days |
| Medium-traffic (1k-10k DAU) | 14 days |
| Low-traffic (<1k DAU) | 21-30 days |
| Email campaigns | Until send complete |
| Paid ads | 7 days (or $500 spend/variant) |

### Why 7+ Days?

1. **Weekly patterns:** User behavior varies by day
2. **Novelty effect:** New designs get temporary lifts
3. **Sample diversity:** Different user segments engage differently
4. **External factors:** Marketing, press, seasonality

### When to End Early

- 99% confidence reached AND 7+ days elapsed
- Critical bug affecting one variant
- 95%+ confidence after 14+ days (if time-constrained)

### Never End Early If

- One variant is "winning" before minimum duration
- Sample size not reached
- Business pressure (wait it out)

---

## 5. Test Setup Process

### Step 1: Document Hypothesis

```
Test ID: [APP-PAY-001]
Hypothesis: [Emotional copy converts better than feature-based]
Rationale: [Users make purchase decisions emotionally, not rationally]
Primary Metric: [conversion_rate]
Secondary Metrics: [revenue_per_user, trial_starts]
```

### Step 2: Calculate Sample Size

1. Determine baseline conversion rate (from last 30 days)
2. Set minimum detectable effect (10-20% relative lift minimum)
3. Calculate sample size using formula
4. Estimate test duration based on traffic

### Step 3: Configure Test

**RevenueCat A/B tests:**
```
1. Products > Experiments > Create Experiment
2. Select paywall/offering to test
3. Configure variants (50/50 split default)
4. Set start date
5. Document in LEDGER/AB_TESTS_MASTER.csv
```

**Firebase Remote Config:**
```
1. Remote Config > Create parameter
2. Add conditions (user percentile)
3. Publish changes
4. Track in analytics
```

**Optimizely/VWO (Landing pages):**
```
1. Create experiment
2. Define goals (conversion events)
3. Set targeting
4. Traffic allocation
5. Start experiment
```

### Step 4: QA Before Launch

- [ ] Both variants render correctly
- [ ] Analytics events firing properly
- [ ] No edge cases breaking experience
- [ ] Fallback behavior works
- [ ] Test on multiple devices/browsers

### Step 5: Monitor During Test

**Daily checks:**
- Sample ratio mismatch (should be ~50/50)
- Error rates by variant
- Unusual metric movements

**Do not:**
- Check statistical significance daily
- Share interim results widely
- Make decisions before test ends

---

## 6. Analyzing Results

### Required Data

```
Variant A: n1 conversions from N1 exposures
Variant B: n2 conversions from N2 exposures

Conversion rates:
p1 = n1 / N1
p2 = n2 / N2

Relative lift = (p2 - p1) / p1 * 100
```

### Statistical Test

1. Calculate Z-score (see formula above)
2. Look up p-value
3. Check confidence level

### Result Interpretation

| Confidence | Decision |
|------------|----------|
| 0-90% | No winner - test inconclusive |
| 90-95% | Directional signal - consider extending |
| 95-99% | Winner declared - implement |
| 99%+ | Strong winner - implement immediately |

### Common Pitfalls

**Simpson's paradox:** Overall results differ from segment results
- Always check by key segments (new vs returning, iOS vs Android)

**Multiple testing:** Running many tests inflates false positives
- Use Bonferroni correction for related tests
- Adjust alpha = 0.05 / number_of_comparisons

**Peeking:** Checking results repeatedly increases error rate
- Set analysis date upfront
- Use sequential testing if peeking needed

---

## 7. Winner Implementation Process

### Step 1: Document Results

Update LEDGER/AB_TESTS_MASTER.csv:
```
status: COMPLETED
result: WINNER_B
winner: variant_b
lift_percent: 15.2
confidence: 97.3
notes: "Emotional copy (B) beat feature list (A). 15.2% lift in conversion rate."
```

### Step 2: Create Implementation Ticket

```
Title: Implement A/B Test Winner - [Test ID]
Priority: High (revenue impact)
Description:
- Test: [APP-PAY-001]
- Winner: Variant B (Emotional copy)
- Lift: +15.2% conversion rate
- Confidence: 97.3%
- Expected annual revenue impact: $X
Action: Roll out variant B to 100% of users
```

### Step 3: Roll Out

**Gradual rollout (recommended):**
1. 50% traffic first (monitor for 2-3 days)
2. 75% traffic (monitor for 2-3 days)
3. 100% traffic

**Full rollout (urgent wins):**
1. Deploy to 100%
2. Monitor closely for 48 hours
3. Rollback plan ready

### Step 4: Validate Post-Implementation

- Check metrics match test results
- Monitor for unexpected effects
- Document learnings

---

## 8. Test Templates

### Paywall Copy Test

```
Test ID: APP-PAY-XXX
App: [App Name]
Test Type: paywall_copy
Hypothesis: [Statement]

Variants:
A (Control): [Current copy]
B: [New copy - emotional angle]
C: [New copy - social proof angle]

Primary Metric: conversion_rate
Secondary: revenue_per_user, trial_starts
Sample Size: 1,500 per variant
Duration: 14 days minimum
```

### Pricing Test

```
Test ID: APP-PRICE-XXX
App: [App Name]
Test Type: pricing
Hypothesis: [Statement]

Variants:
A (Control): $X.99/month
B: $Y.99/month
C: $Z.99/month

Primary Metric: revenue_per_user
Secondary: conversion_rate, LTV
Sample Size: 500 per variant
Duration: 21 days minimum (capture full billing cycles)
```

### Email Subject Line Test

```
Test ID: MKT-EMAIL-XXX
Campaign: [Campaign Name]
Test Type: email_subject
Hypothesis: [Statement]

Variants:
A: [Subject line A]
B: [Subject line B]
C: [Subject line C]

Primary Metric: open_rate
Secondary: click_rate, conversion_rate
Sample Size: 1,000 per variant
List Segment: [Segment criteria]
```

### Ad Creative Test

```
Test ID: MKT-AD-XXX
Platform: [Facebook/TikTok/etc]
Test Type: ad_creative
Hypothesis: [Statement]

Variants:
A (Control): [Description]
B: [Description]

Primary Metric: CTR
Secondary: CPA, ROAS
Budget: $500 per variant
Duration: 7 days minimum
Audience: [Targeting criteria]
```

---

## 9. Test Prioritization Framework

### ICE Score

```
ICE = Impact * Confidence * Ease

Impact (1-10): Potential revenue/metric improvement
Confidence (1-10): Certainty test will produce results
Ease (1-10): How easy to implement and run

Prioritize tests with highest ICE scores.
```

### Priority Matrix

| Impact | Confidence | Ease | Priority |
|--------|------------|------|----------|
| High | High | High | DO NOW |
| High | High | Low | Schedule |
| High | Low | High | Worth testing |
| High | Low | Low | Maybe later |
| Low | * | * | Skip or batch |

### Suggested Test Cadence

**Weekly:**
- Review active tests
- Launch new tests as capacity allows
- Document completed tests

**Monthly:**
- Analyze all test learnings
- Update best practices
- Plan next month's tests

**Quarterly:**
- Meta-analysis of all tests
- Update playbook with learnings
- Share with team

---

## 10. Tools and Resources

### A/B Testing Platforms

**App:**
- RevenueCat (paywall/pricing tests)
- Firebase Remote Config (feature flags)
- Optimizely Mobile (full testing suite)
- Statsig (analytics + testing)

**Web:**
- Optimizely
- VWO
- Google Optimize (deprecated, use alternatives)
- Unbounce (landing pages)

**Email:**
- Native platform testing (ConvertKit, Mailchimp)
- Litmus (advanced testing)

**Ads:**
- Native platform A/B testing
- AdEspresso (Facebook optimization)

### Calculators

**Sample size:**
- Evan Miller: https://www.evanmiller.org/ab-testing/sample-size.html
- Optimizely: https://www.optimizely.com/sample-size-calculator/

**Significance:**
- AB Test Guide: https://abtestguide.com/calc/
- Neil Patel: https://neilpatel.com/ab-testing-calculator/

### Books and Resources

- "Trustworthy Online Controlled Experiments" (Kohavi)
- "Statistical Methods in Online A/B Testing" (Georgi)
- Optimizely Academy
- CXL Institute courses

---

## 11. Common Mistakes to Avoid

1. **Not running tests long enough**
   - Minimum 7 days, preferably 14+

2. **Peeking at results**
   - Set analysis date upfront, stick to it

3. **Testing too many things**
   - One variable per test

4. **Ignoring sample size**
   - Calculate before starting, not after

5. **Ending at 95% confidence on day 2**
   - Could be noise, wait for minimum duration

6. **Not segmenting results**
   - Check new vs returning, platforms, geos

7. **Implementing without validation**
   - Monitor post-rollout metrics

8. **No hypothesis documentation**
   - Can't learn from undocumented tests

9. **Testing low-impact changes**
   - Button color rarely matters, copy does

10. **Not sharing learnings**
    - Document everything in LEDGER

---

## Appendix: Quick Formulas

### Conversion Rate
```
CR = conversions / visitors
```

### Standard Error
```
SE = sqrt(p * (1-p) / n)
```

### Confidence Interval
```
CI = p +/- Z * SE
(95% CI uses Z = 1.96)
```

### Z-Score for Two Proportions
```
Z = (p1 - p2) / sqrt(p * (1-p) * (1/n1 + 1/n2))
where p = (x1 + x2) / (n1 + n2)
```

### Sample Size (simplified)
```
n = 16 * p * (1-p) / MDE^2
(for 80% power, 95% confidence)
```

### Minimum Detectable Effect
```
MDE = sqrt(16 * p * (1-p) / n)
```

---

*Last updated: 2026-01-21*
*Owner: PRINTMAXX Operations*
