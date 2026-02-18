# Hybrid monetization

Combining multiple revenue streams to maximize lifetime value across user segments.

---

## Strategy overview

### Revenue stream combinations

| Primary model | Secondary model | Best for |
|---------------|-----------------|----------|
| Subscription | Ads (free tier) | Most apps |
| Subscription | Consumable IAP | Apps with variable usage |
| Freemium + Ads | Lifetime purchase | Apps with devoted users |
| Subscription | Tip jar | Creator/indie apps |
| Ads | Rewarded video upgrade | Casual apps |

### User segment revenue matrix

| Segment | % of users | Subscription | Ads | Consumables | Contribution |
|---------|------------|--------------|-----|-------------|--------------|
| Premium subscribers | 3-8% | Yes | No | Maybe | 60-80% |
| Free active users | 40-60% | No | Yes | Maybe | 15-30% |
| Occasional users | 30-40% | No | Limited | Rare | 5-15% |
| Churned users | N/A | No | No | No | 0% |

---

## Subscriptions + ads model

### Implementation framework

```typescript
interface HybridMonetization {
  subscription: {
    tiers: SubscriptionTier[];
    trialDays: number;
  };
  ads: {
    showToSubscribers: boolean;
    freeUserConfig: AdConfig;
    lapsedUserConfig: AdConfig;
  };
}

const hybridConfig: HybridMonetization = {
  subscription: {
    tiers: [
      { id: 'monthly', price: 7.99, features: ['unlimited', 'ad_free', 'premium_features'] },
      { id: 'annual', price: 47.99, features: ['unlimited', 'ad_free', 'premium_features'] },
    ],
    trialDays: 7,
  },
  ads: {
    showToSubscribers: false,
    freeUserConfig: {
      banner: true,
      interstitial: true,
      rewarded: true,
      interstitialFrequency: 300, // seconds
    },
    lapsedUserConfig: {
      banner: true,
      interstitial: false, // Less aggressive for win-back
      rewarded: true,
      interstitialFrequency: 600,
    },
  },
};
```

### Revenue impact modeling

**Scenario: 10,000 monthly active users**

Without ads:
```
Subscribers (5%): 500 users x $7.99 = $3,995/month
Total: $3,995/month
```

With hybrid (subscriptions + ads):
```
Subscribers (5%): 500 users x $7.99 = $3,995/month
Free users with ads: 9,500 users x $0.03 ARPDAU x 30 days = $8,550/month
Total: $12,545/month (+214%)
```

### Cannibalization risk

Question: Do ads reduce subscription conversion?

**Test framework:**
```
Experiment: Ads impact on subscription
Duration: 30 days

Variant A: No ads, subscription only
Variant B: Ads for free users, subscription available

Metrics:
- Subscription conversion rate
- Total revenue per user
- D30 retention
```

**Typical results:**
- Subscription conversion drops 10-20% with ads
- But total revenue increases 50-150%
- Net positive for most apps

---

## Consumable IAPs alongside subscriptions

### Use cases for consumables

| Consumable type | Example | Price point | Use alongside subscription |
|-----------------|---------|-------------|---------------------------|
| Credits/tokens | AI generation tokens | $0.99-4.99 | Yes (extra usage) |
| Virtual currency | In-app coins | $0.99-9.99 | Yes (premium content) |
| Boosts/power-ups | Time savers | $0.99-2.99 | Yes (convenience) |
| Content packs | Additional templates | $2.99-9.99 | Yes (one-time purchase) |

### Implementation example

```typescript
interface ConsumableProduct {
  id: string;
  name: string;
  price: number;
  quantity: number;
  availableTo: 'all' | 'free_only' | 'subscribers_only';
}

const consumables: ConsumableProduct[] = [
  {
    id: 'tokens_100',
    name: '100 AI Tokens',
    price: 2.99,
    quantity: 100,
    availableTo: 'all', // Even subscribers might want extra
  },
  {
    id: 'tokens_500',
    name: '500 AI Tokens',
    price: 9.99,
    quantity: 500,
    availableTo: 'all',
  },
  {
    id: 'template_pack',
    name: 'Premium Templates',
    price: 4.99,
    quantity: 1,
    availableTo: 'all', // One-time purchase
  },
];
```

### Subscription vs consumable decision

```
IF user has predictable, consistent usage:
  Subscription makes sense

IF user has variable, bursty usage:
  Consumables might generate more revenue

IF user is price-sensitive:
  Consumables allow "pay as you go"
```

### Hybrid subscription + consumable model

**Subscription includes:**
- Base allocation (e.g., 100 AI generations/month)
- All premium features
- Ad-free experience

**Consumables add:**
- Extra tokens when base allocation runs out
- Special one-time purchases (templates, themes)
- Gifts to other users

---

## Tip jar / support options

### When tip jars work

- Indie developer with personal brand
- Community-loved app with devoted users
- Open source or freemium with generous free tier
- Apps serving specific communities (hobbyists, creators)

### Implementation

```typescript
const tipJarOptions = [
  { id: 'coffee', name: 'Buy me a coffee', price: 2.99, emoji: 'coffee' },
  { id: 'lunch', name: 'Buy me lunch', price: 9.99, emoji: 'sandwich' },
  { id: 'dinner', name: 'Buy me dinner', price: 24.99, emoji: 'steak' },
  { id: 'support', name: 'Monthly support', price: 4.99, recurring: true },
];
```

### Tip jar placement

**Effective locations:**
- Settings/About screen
- After major feature release (changelog)
- After user milestone ("You've completed 100 workouts!")
- In-app "Support development" section

**Avoid:**
- Main UI (feels begging)
- Blocking flows
- Too frequently

### Expected revenue

| App type | Tip conversion | Avg tip | Monthly (per 10K MAU) |
|----------|----------------|---------|----------------------|
| Indie with brand | 0.1-0.5% | $5 | $50-250 |
| Community-loved | 0.5-2% | $7 | $350-1,400 |
| Typical app | 0.01-0.1% | $3 | $3-30 |

---

## Lifetime purchase option

### When to offer lifetime

**Good candidates:**
- Apps with stable, finished feature set
- Apps with devoted power users
- Apps where churn is high but devotees are very devoted
- When you want to capture revenue from hesitant subscribers

**Poor candidates:**
- Apps with high ongoing costs (AI APIs, server)
- Apps expecting major feature additions
- Apps with very high churn (lifetime buyers might churn anyway)

### Pricing lifetime purchases

**Formula approaches:**

1. **Monthly multiple**
   ```
   Lifetime = Monthly x 24-36
   Example: $7.99/month -> $191.76 - $287.64 -> Round to $199
   ```

2. **Annual multiple**
   ```
   Lifetime = Annual x 2-3
   Example: $47.99/year -> $95.98 - $143.97 -> Round to $99 or $129
   ```

3. **LTV-based**
   ```
   Lifetime = Expected LTV x 1.5-2
   If average subscriber stays 8 months at $7.99 = $63.92 LTV
   Lifetime = $95.88 - $127.84 -> Round to $99
   ```

### Lifetime implementation

```typescript
interface LifetimePurchase {
  id: string;
  price: number;
  originalMonthlyEquivalent: number;
  features: string[];
  displaySavings: string;
}

const lifetimeOption: LifetimePurchase = {
  id: 'lifetime_pro',
  price: 99.99,
  originalMonthlyEquivalent: 7.99,
  features: [
    'All current features',
    'All future updates',
    'No recurring payments',
  ],
  displaySavings: 'Save vs 13+ months of subscription',
};
```

### Lifetime purchase placement

**Option A: Always visible**
- Show alongside monthly/annual on paywall
- Works for apps confident in LTV calculation

**Option B: Hidden/limited**
- Show only in settings
- Show only during promotions
- Show only to long-term users

**Option C: Win-back**
- Offer lifetime to users who cancelled subscription
- "Miss us? Come back forever for one price"

### Cannibalization concerns

Risk: Lifetime buyers would have paid more as subscribers

Mitigation:
- Price lifetime at 24-36x monthly
- Limit availability (promotions only)
- Track: What % of lifetime buyers were previous subscribers?

---

## Revenue optimization by segment

### Segment strategy matrix

| Segment | Primary revenue | Secondary | Optimization goal |
|---------|-----------------|-----------|-------------------|
| Power users | Subscription | Consumables | Maximize LTV |
| Regular users | Subscription | - | Convert to annual |
| Casual users | Ads | Rewarded video | Increase session frequency |
| Churned | Win-back offer | Lifetime | Recover revenue |
| Non-payers | Ads | Tip jar | Extract any value |

### Implementation

```typescript
function getMonetizationStrategy(user: User): MonetizationStrategy {
  const usage = user.sessionsLast30Days;
  const hasSubscribed = user.subscriptionHistory.length > 0;

  if (user.hasActiveSubscription) {
    return {
      showAds: false,
      showConsumables: usage > 50, // Heavy users might want extra
      showTipJar: false,
      showLifetime: false,
    };
  }

  if (hasSubscribed && !user.hasActiveSubscription) {
    // Churned subscriber
    return {
      showAds: true,
      showConsumables: false,
      showTipJar: false,
      showLifetime: true, // Win-back with lifetime
      winBackDiscount: 0.5,
    };
  }

  if (usage > 20) {
    // High-usage free user
    return {
      showAds: true,
      showConsumables: true,
      showTipJar: false,
      showLifetime: false,
      subscriptionEmphasis: 'high', // Push subscription hard
    };
  }

  // Casual user
  return {
    showAds: true,
    showConsumables: false,
    showTipJar: false,
    showLifetime: false,
    subscriptionEmphasis: 'low',
  };
}
```

---

## Revenue mix benchmarks

### Typical hybrid app revenue breakdown

| Revenue source | % of total | Notes |
|----------------|------------|-------|
| Subscriptions | 50-70% | Core revenue driver |
| Ads | 20-35% | Free tier monetization |
| Consumables | 5-15% | Variable usage top-up |
| Lifetime | 5-10% | One-time buyers |
| Tips | 0-3% | Nice-to-have |

### Revenue per user targets

| Model | ARPU (monthly) | Target |
|-------|----------------|--------|
| Subscription only | $0.30-0.60 | 5-8% conversion x $6-8 effective |
| Ads only | $0.05-0.15 | $0.002-0.005 x 30 days |
| Hybrid | $0.50-1.00 | Best of both |

---

## Hybrid monetization test framework

### Experiment 1: Add ads to subscription model

```
Baseline: Subscription only
Test: Subscription + ads for free users

Duration: 30 days
Sample: 5000+ users per variant

Metrics:
- Total revenue per install
- Subscription conversion rate
- D30 retention
- User rating (1-star reviews)
```

### Experiment 2: Add consumables

```
Baseline: Subscription only
Test: Subscription + consumable tokens

Duration: 30 days
Sample: 2000+ users per variant

Metrics:
- Revenue per paying user
- Consumable purchase rate
- Impact on subscription renewals
- Feature usage patterns
```

### Experiment 3: Lifetime option impact

```
Baseline: Monthly + Annual only
Test: Monthly + Annual + Lifetime

Duration: 60 days (need longer for lifetime data)
Sample: 5000+ users per variant

Metrics:
- Revenue per user (lifetime normalized)
- Subscription conversion rate
- Annual vs lifetime selection
- Long-term subscriber churn
```

---

## Implementation checklist

Before launching hybrid monetization:

- [ ] Subscription system working and tested
- [ ] Ad network integrated and configured
- [ ] Consumable IAPs set up in stores
- [ ] User segmentation logic implemented
- [ ] Ad suppression for subscribers working
- [ ] Revenue tracking for all streams
- [ ] A/B test infrastructure ready
- [ ] Privacy compliance for all monetization
- [ ] User experience tested for each segment
- [ ] Support documentation updated
