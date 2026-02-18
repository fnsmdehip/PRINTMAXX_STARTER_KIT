# A/B Testing Infrastructure

Complete testing system for apps and marketing optimization.

---

## Directory Structure

```
ab_tests/
├── README.md                    # This file
├── PAYWALL_VARIATIONS.md        # App paywall copy and design tests
├── PRICING_VARIATIONS.md        # Price point and display tests
├── ONBOARDING_VARIATIONS.md     # User onboarding flow tests
├── CTA_VARIATIONS.md            # Call-to-action tests
├── EMAIL_SUBJECT_TESTS.md       # Email subject line tests
├── AD_CREATIVE_TESTS.md         # Paid ad creative tests
└── LANDING_PAGE_TESTS.md        # Landing page conversion tests
```

---

## Related Files

| File | Location | Purpose |
|------|----------|---------|
| AB_TESTS_MASTER.csv | LEDGER/ | Track all active and completed tests |
| AB_TESTING_PLAYBOOK.md | OPS/ | Methodology and best practices |
| ab_test_analyzer.py | AUTOMATIONS/ | Analyze test data and calculate significance |

---

## Quick Start

### 1. Choose a Test

Review the variation files to find a test template:
- App conversion tests: PAYWALL, PRICING, ONBOARDING, CTA
- Marketing tests: EMAIL, AD_CREATIVE, LANDING_PAGE

### 2. Document in LEDGER

Add the test to `LEDGER/AB_TESTS_MASTER.csv`:

```csv
test_id,app,test_type,hypothesis,variant_a,variant_b,...
APP-PAY-001,HeartSync,paywall_copy,"Emotional copy converts better",Current copy,New emotional copy,...
```

### 3. Implement Variants

Set up the test in your testing platform:
- **Apps:** RevenueCat, Firebase Remote Config
- **Email:** ConvertKit, Mailchimp, Beehiiv
- **Ads:** Meta Ads Manager, TikTok Ads
- **Landing pages:** Optimizely, VWO, Unbounce

### 4. Run the Test

Minimum requirements:
- 7 days duration
- Sample size per variant (see playbook)
- 95% confidence for decisions

### 5. Analyze Results

Use the analyzer script:

```bash
cd AUTOMATIONS
python ab_test_analyzer.py --test-id APP-PAY-001 --manual
```

### 6. Implement Winner

Update LEDGER with results and roll out winning variant.

---

## Test Categories

### App Tests

| Category | File | What to Test |
|----------|------|--------------|
| Paywall | PAYWALL_VARIATIONS.md | Copy, design, timing, social proof |
| Pricing | PRICING_VARIATIONS.md | Price points, display format, tiers, trials |
| Onboarding | ONBOARDING_VARIATIONS.md | Flow length, personalization, permissions |
| CTAs | CTA_VARIATIONS.md | Copy, color, placement, animation |

### Marketing Tests

| Category | File | What to Test |
|----------|------|--------------|
| Email | EMAIL_SUBJECT_TESTS.md | Subject lines, personalization, send time |
| Ads | AD_CREATIVE_TESTS.md | Format, creative, copy, targeting |
| Landing | LANDING_PAGE_TESTS.md | Headlines, layout, forms, social proof |

---

## Statistical Requirements

### Sample Size Guidelines

| Baseline Conversion | Min Detectable Effect | Sample Per Variant |
|---------------------|----------------------|-------------------|
| 1% | 0.5% lift | 3,000 |
| 5% | 1% lift | 4,900 |
| 10% | 2% lift | 4,300 |
| 20% | 4% lift | 3,900 |

### Confidence Levels

| Confidence | Decision |
|------------|----------|
| <90% | Inconclusive - extend or accept null |
| 90-95% | Directional signal - extend if possible |
| 95-99% | Winner - implement |
| 99%+ | Strong winner - implement immediately |

---

## Test Prioritization (ICE Framework)

**ICE Score = Impact x Confidence x Ease**

| Factor | 1-10 Scale |
|--------|-----------|
| Impact | Revenue potential of winning |
| Confidence | Likelihood of meaningful result |
| Ease | Implementation difficulty |

### Priority Matrix

| Impact | ICE Score | Action |
|--------|-----------|--------|
| High + High Confidence + Easy | 7-10 | Do now |
| High + Any + Hard | 4-6 | Schedule |
| Low + Any + Any | 1-3 | Skip or batch |

---

## Common Mistakes to Avoid

1. **Ending tests early** - Wait for minimum duration AND sample size
2. **Peeking** - Don't check daily; set analysis date upfront
3. **Testing too many things** - One variable per test
4. **Ignoring segments** - Check results by key segments
5. **No hypothesis** - Document why you think variant will win
6. **Not tracking** - Every test in LEDGER/AB_TESTS_MASTER.csv

---

## Testing Cadence

### Weekly
- Review active tests
- Launch 1-2 new tests
- Document completed tests

### Monthly
- Analyze all test learnings
- Update templates with insights
- Plan next month's tests

### Quarterly
- Meta-analysis across all tests
- Update playbook
- Share learnings team-wide

---

## Tools Integration

### RevenueCat (App Pricing/Paywalls)
```
Products > Experiments > Create
Configure variants
Set traffic split
Monitor in dashboard
```

### Firebase (Feature Flags)
```
Remote Config > Create parameter
Add user percentile conditions
Publish and track
```

### Meta Ads (Creative Testing)
```
Ads Manager > Create Campaign
Enable A/B test
Select variable
Set budget and duration
```

### Email Platforms
```
Create broadcast/campaign
Enable A/B testing
Enter variants
Set test size (20-30%)
Set winner criteria
```

---

## Resources

- Full methodology: `OPS/AB_TESTING_PLAYBOOK.md`
- Analyzer script: `AUTOMATIONS/ab_test_analyzer.py`
- Test tracking: `LEDGER/AB_TESTS_MASTER.csv`
- Sample size calculator: evanmiller.org/ab-testing/sample-size.html
- Significance calculator: abtestguide.com/calc/

---

*Last updated: 2026-01-21*
