# Revenue optimization playbook

Tactical strategies to increase lifetime value, reduce churn, and maximize revenue per user.

---

## LTV optimization strategies

### LTV formula

```
LTV = ARPU x Average Subscription Length (months)
    = (Monthly price x Conversion rate) x (1 / Monthly churn rate)
```

**Example calculation:**
```
Monthly price: $7.99
Conversion rate: 5%
Monthly churn: 8%

ARPU = $7.99 x 0.05 = $0.40
Avg subscription length = 1 / 0.08 = 12.5 months
LTV = $0.40 x 12.5 = $5.00

Or for paying users only:
LTV = $7.99 x 12.5 = $99.88
```

### LTV improvement levers

| Lever | Impact on LTV | Difficulty | Priority |
|-------|---------------|------------|----------|
| Reduce churn 8% -> 6% | +33% | High | 1 |
| Increase price $7.99 -> $9.99 | +25% (if conversion holds) | Medium | 2 |
| Increase conversion 5% -> 6% | +20% | Medium | 3 |
| Shift to annual 50% -> 70% | +15% (lower effective churn) | Medium | 4 |

### Churn reduction impact table

| Current churn | Improved churn | LTV multiplier |
|---------------|----------------|----------------|
| 10% | 8% | 1.25x |
| 10% | 6% | 1.67x |
| 8% | 6% | 1.33x |
| 8% | 5% | 1.60x |
| 6% | 4% | 1.50x |

Key insight: Reducing churn has outsized impact on LTV compared to other levers.

---

## Churn reduction tactics

### Churn prediction signals

| Signal | Churn risk | Action |
|--------|------------|--------|
| No app open in 7 days | High | Push notification campaign |
| Feature usage dropped 50% | Medium | Feature education email |
| Billing failed | Critical | Payment update prompt |
| Opened but no core action | Medium | Onboarding reminder |
| Support ticket unresolved | High | Prioritize resolution |

### Churn prevention system

```typescript
interface ChurnRiskUser {
  userId: string;
  riskScore: number; // 0-100
  riskFactors: string[];
  recommendedAction: string;
  daysSinceLastActive: number;
  subscriptionDaysRemaining: number;
}

function calculateChurnRisk(user: User): ChurnRiskUser {
  let score = 0;
  const factors: string[] = [];

  // Engagement signals
  if (user.daysSinceLastActive > 14) {
    score += 30;
    factors.push('inactive_14_days');
  } else if (user.daysSinceLastActive > 7) {
    score += 15;
    factors.push('inactive_7_days');
  }

  // Usage trend
  const usageTrend = user.sessionsThisWeek / user.sessionsLastWeek;
  if (usageTrend < 0.5) {
    score += 20;
    factors.push('usage_declined_50_percent');
  }

  // Feature adoption
  if (user.featuresUsed < 3) {
    score += 15;
    factors.push('low_feature_adoption');
  }

  // Billing issues
  if (user.hasFailedPayment) {
    score += 40;
    factors.push('payment_failed');
  }

  // Support issues
  if (user.hasOpenTicket && user.ticketAgeHours > 48) {
    score += 10;
    factors.push('unresolved_support_ticket');
  }

  return {
    userId: user.id,
    riskScore: Math.min(score, 100),
    riskFactors: factors,
    recommendedAction: getRecommendedAction(factors),
    daysSinceLastActive: user.daysSinceLastActive,
    subscriptionDaysRemaining: user.subscriptionDaysRemaining,
  };
}
```

### Intervention playbook

| Risk score | Timing | Intervention |
|------------|--------|--------------|
| 20-40 | Immediate | In-app tooltip highlighting unused features |
| 40-60 | Within 24h | Push notification with value reminder |
| 60-80 | Within 24h | Email with personalized usage tips |
| 80+ | Immediate | Personal outreach (if high-value) or win-back offer |

### Engagement campaigns

**7-day inactive campaign**
```
Day 7: Push notification
  "Your [feature] misses you. Quick 2-minute session?"

Day 10: Email
  Subject: "Did you know you can..."
  Body: Feature education based on unused features

Day 14: Push notification
  "We added [new feature]. Check it out?"

Day 21: Win-back email
  Subject: "Come back and get 30% off"
  Body: Discount offer if returning within 7 days
```

**Pre-renewal engagement**
```
7 days before renewal:
  In-app message: "Your subscription renews in 7 days"
  Show: Usage stats, value delivered

3 days before renewal:
  Push notification: "Don't forget - renewal coming up"
  For at-risk users: "Have questions? Chat with us"

1 day before renewal:
  Nothing (avoid prompting cancellation)
```

---

## Upgrade prompts timing

### Optimal prompt triggers

| Trigger | Conversion lift | Notes |
|---------|-----------------|-------|
| Usage limit reached | 25-40% | Highest intent moment |
| Feature attempt blocked | 20-35% | Clear value demonstration |
| Milestone achieved | 15-25% | Positive emotional state |
| After value delivery | 10-20% | User satisfied with product |
| Session end | 5-10% | Natural break point |

### Prompt timing rules

```typescript
interface UpgradePromptConfig {
  trigger: string;
  minSessionsBeforePrompt: number;
  minDaysSinceLastPrompt: number;
  maxPromptsPerDay: number;
  showAfterValueMoment: boolean;
}

const upgradePromptRules: UpgradePromptConfig[] = [
  {
    trigger: 'usage_limit',
    minSessionsBeforePrompt: 0, // Show immediately when hit
    minDaysSinceLastPrompt: 0,
    maxPromptsPerDay: 3,
    showAfterValueMoment: true,
  },
  {
    trigger: 'feature_gate',
    minSessionsBeforePrompt: 2,
    minDaysSinceLastPrompt: 1,
    maxPromptsPerDay: 2,
    showAfterValueMoment: true,
  },
  {
    trigger: 'session_end',
    minSessionsBeforePrompt: 5,
    minDaysSinceLastPrompt: 3,
    maxPromptsPerDay: 1,
    showAfterValueMoment: false,
  },
  {
    trigger: 'milestone',
    minSessionsBeforePrompt: 0,
    minDaysSinceLastPrompt: 7,
    maxPromptsPerDay: 1,
    showAfterValueMoment: true,
  },
];
```

### Prompt fatigue prevention

- Max 3 upgrade prompts per day (all types combined)
- Min 1 day between "unprompted" upgrade suggestions
- Never show prompt immediately after dismissal
- Track prompt-to-conversion ratio; back off if declining

### Prompt effectiveness tracking

```typescript
interface PromptMetrics {
  promptType: string;
  impressions: number;
  conversions: number;
  dismissals: number;
  conversionRate: number;
  dismissRateToChurn: number; // Do dismissed users churn more?
}

// Track and optimize based on these metrics
// Kill prompts with <1% conversion and high dismiss-to-churn correlation
```

---

## Win-back pricing strategies

### Win-back timing

| Days since churn | Win-back offer | Expected recovery |
|------------------|----------------|-------------------|
| 1-3 | Payment recovery (if billing failed) | 60-80% |
| 3-7 | 30% discount | 5-10% |
| 7-14 | 40% discount | 3-7% |
| 14-30 | 50% discount | 2-5% |
| 30-90 | 60% discount or lifetime offer | 1-3% |
| 90+ | Rarely worth pursuing | <1% |

### Win-back campaign sequence

**Billing failure recovery**
```
Hour 1: In-app prompt + push notification
  "We couldn't process your payment. Update card to continue?"

Hour 24: Email
  Subject: "Your subscription is paused"
  Body: Update payment link, grace period reminder

Day 3: Push notification
  "Last chance to update payment before losing access"

Day 7: Access revoked, downgrade to free
```

**Voluntary cancellation recovery**
```
At cancellation: Exit survey + retention offer
  "Before you go, tell us why?"
  [Too expensive | Not using enough | Missing feature | Other]

  Based on response:
  - Too expensive: "Get 40% off your next month"
  - Not using enough: "Pause subscription for 1 month instead?"
  - Missing feature: "This is coming in [X]. Want to try free for a month?"

Day 3: Email
  Subject: "We miss you"
  Body: Usage stats showing value delivered, soft return CTA

Day 7: Push notification
  "Your data is still here. Come back anytime."

Day 14: Email with discount
  Subject: "50% off to come back"
  Body: Time-limited offer

Day 30: Final email
  Subject: "Last chance: 60% off forever"
  Body: Lifetime or annual at major discount
```

### Win-back offer matrix

| Cancel reason | Offer type | Discount | Duration |
|---------------|------------|----------|----------|
| Too expensive | Price discount | 40-50% | 3 months |
| Not using enough | Usage extension | 30 days free | One-time |
| Missing feature | Feature preview | Beta access | Until launch |
| Competitor | Competitive match | Up to 50% | 6 months |
| Temporary | Pause option | Free pause | 1-3 months |

---

## Annual upgrade strategies

### Why annual matters

| Metric | Monthly | Annual |
|--------|---------|--------|
| Effective churn rate | 8-12%/month | 2-4%/month |
| Payment friction | 12x/year | 1x/year |
| Revenue predictability | Low | High |
| Refund window impact | Small | Larger |

### Annual upgrade prompts

**At subscription start**
```
"Start with annual and save 50%"
Show: Monthly vs annual comparison
Highlight: Total savings amount
```

**After 3 months on monthly**
```
"You've been with us 3 months!"
"Upgrade to annual and save $X over your next year"
Show: Personalized savings calculation
```

**At monthly renewal**
```
"Your subscription renews tomorrow"
"Switch to annual now and lock in $X savings"
One-click upgrade option
```

### Annual conversion benchmarks

| Prompt timing | Conversion rate |
|---------------|-----------------|
| At initial purchase | 40-60% choose annual |
| After 3 months monthly | 10-15% upgrade |
| At renewal with prompt | 5-10% upgrade |
| Win-back (churned monthly) | 20-30% choose annual when returning |

---

## Price increase strategies

### When to raise prices

- New significant features added
- Market rates have increased
- Current price undervalues product
- Testing shows conversion holds at higher price

### Price increase implementation

**Grandfather existing subscribers**
```
Existing subscribers: Keep old price
New subscribers only: New price
Communicate: "Locked-in rate for loyal users"
```

**Phase in increase**
```
Month 1: New subscribers pay new price
Month 3: Trial users see new price
Month 6: Offer existing users annual at old rate
Month 12: Full transition to new pricing
```

**Communicate value, not cost**
```
BAD: "We're raising prices from $7.99 to $9.99"

GOOD: "We've added [X, Y, Z features] this year.
      Starting [date], new subscribers pay $9.99/month.
      As a current subscriber, your rate stays at $7.99."
```

### Price increase impact modeling

```typescript
interface PriceIncreaseModel {
  currentPrice: number;
  newPrice: number;
  currentConversion: number;
  estimatedNewConversion: number;
  currentUsers: number;
  churnFromIncrease: number;
}

function modelPriceIncrease(model: PriceIncreaseModel): {
  revenueChange: number;
  breakEvenConversion: number;
} {
  const currentRevenue = model.currentPrice * model.currentConversion * model.currentUsers;
  const newRevenue = model.newPrice * model.estimatedNewConversion * model.currentUsers * (1 - model.churnFromIncrease);

  const breakEvenConversion = currentRevenue / (model.newPrice * model.currentUsers);

  return {
    revenueChange: ((newRevenue - currentRevenue) / currentRevenue) * 100,
    breakEvenConversion: breakEvenConversion,
  };
}

// Example:
// $7.99 -> $9.99 (25% increase)
// If conversion drops less than 20%, still profitable
```

---

## Revenue optimization metrics dashboard

### Daily metrics

| Metric | Target | Alert threshold |
|--------|--------|-----------------|
| Trial starts | 100/day | <70 |
| Trial conversions | 30/day | <20 |
| Subscription revenue | $X | <0.8x avg |
| Churn rate | <8% | >10% |
| ARPDAU | $0.05 | <$0.03 |

### Weekly metrics

| Metric | Target | Action if missed |
|--------|--------|------------------|
| LTV trend | Stable/up | Investigate churn |
| Annual ratio | 55%+ | Improve annual prompts |
| Trial-to-paid | 25%+ | Review onboarding |
| D7 retention | 40%+ | Engagement campaigns |

### Monthly metrics

| Metric | Benchmark | Note |
|--------|-----------|------|
| MRR growth | 5-10% | Healthy growth |
| Net revenue retention | 90%+ | Expansion - churn |
| Payback period | <12 months | CAC / monthly ARPU |
| LTV:CAC ratio | >3:1 | Healthy unit economics |

---

## Revenue optimization experiments to run

### High-impact experiments

1. **Annual ratio optimization**
   - Test annual savings percentage (33% vs 50%)
   - Test annual pre-selection on paywall
   - Test annual upgrade prompts at month 3

2. **Churn reduction**
   - Test engagement campaigns for at-risk users
   - Test pause option vs cancellation
   - Test win-back offer timing and discounts

3. **Price optimization**
   - Test higher price point with same features
   - Test lower price with limited features
   - Test regional pricing

4. **Upgrade prompt optimization**
   - Test prompt timing and triggers
   - Test prompt copy and design
   - Test prompt frequency limits

### Experiment priority framework

```
Priority = (Expected revenue impact) x (Confidence) / (Effort)

High priority: High impact, high confidence, low effort
Example: Testing annual pre-selection

Medium priority: High impact, medium confidence, medium effort
Example: Churn prediction and intervention system

Low priority: Low impact or high effort
Example: Complete paywall redesign
```

---

## Revenue optimization checklist

Weekly review:
- [ ] Check trial-to-paid conversion trend
- [ ] Review churn by subscription type
- [ ] Analyze upgrade prompt performance
- [ ] Review win-back campaign results

Monthly review:
- [ ] Calculate and track LTV by cohort
- [ ] Review pricing experiment results
- [ ] Analyze annual vs monthly trends
- [ ] Plan next month's experiments

Quarterly review:
- [ ] Full pricing strategy review
- [ ] Competitive pricing analysis
- [ ] LTV:CAC health check
- [ ] Feature vs pricing alignment
