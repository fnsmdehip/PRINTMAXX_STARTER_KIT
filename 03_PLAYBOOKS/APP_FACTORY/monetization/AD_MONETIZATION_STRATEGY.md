# Ad monetization strategy

Framework for implementing non-intrusive ad monetization alongside or instead of subscriptions.

---

## When to show ads

### User segmentation

| User type | Ad strategy | Reasoning |
|-----------|-------------|-----------|
| Free tier (never subscribed) | Show ads | Monetize non-payers |
| Trial users | No ads | Don't disrupt conversion funnel |
| Lapsed subscribers | Limited ads | Incentive to re-subscribe |
| Active subscribers | Never show ads | This is what they're paying to avoid |

### Implementation logic

```typescript
function shouldShowAd(user: User): boolean {
  // Never show ads to paying subscribers
  if (user.hasActiveSubscription) return false;

  // Never show ads during trial
  if (user.isInTrial) return false;

  // Show ads to free users
  if (user.subscriptionStatus === 'none') return true;

  // Limited ads for lapsed subscribers (incentive to return)
  if (user.subscriptionStatus === 'lapsed') {
    return user.daysSinceLapse > 7; // Grace period
  }

  return false;
}
```

---

## Ad placement optimization

### Placement hierarchy (least to most intrusive)

1. **Banner ads** - Always visible, lowest impact, lowest revenue
2. **Native ads** - Blended into content, medium impact
3. **Interstitial ads** - Full screen between actions, high impact
4. **Rewarded video** - User-initiated, highest value exchange

### Placement rules

**Banner ads**
```
Position: Bottom of screen (not top - thumb zone)
Size: 320x50 (standard) or 320x100 (large)
Refresh: Every 30-60 seconds
Revenue: $0.10-0.50 eCPM
```

**Native ads**
```
Position: Within content feed (every 5-8 items)
Design: Match app aesthetic, clear "Ad" label
Refresh: On scroll/new content load
Revenue: $0.50-2.00 eCPM
```

**Interstitial ads**
```
Position: Between natural breaks (level complete, session end)
Frequency: Max 1 per 3-5 minutes
Timing: After user action, not interrupting
Revenue: $2-10 eCPM
```

**Rewarded video**
```
Position: Clearly labeled opt-in button
Reward: Extra feature use, virtual currency, premium content preview
Duration: 15-30 seconds
Revenue: $10-30 eCPM
```

### Placement test framework

```
Experiment: Ad placement optimization
Duration: 14 days
Sample: 5000+ ad impressions per variant

Variant A: Banner only
Variant B: Banner + interstitial after session
Variant C: Banner + rewarded video option
Variant D: All three ad types

Metrics:
- Revenue per daily active user (ARPDAU)
- Session length
- D1/D7 retention
- User complaints/reviews mentioning ads
```

---

## Rewarded video strategy

### Reward types

| Reward | Example | User value | Implementation |
|--------|---------|------------|----------------|
| Extra usage | +3 free generations | High | Temporary limit increase |
| Premium preview | Try AI feature once | High | Feature unlock for single use |
| Virtual currency | +100 coins | Medium | In-app economy boost |
| Ad-free period | 1 hour no ads | Medium | Suppress ad display |
| Content unlock | Access bonus content | High | Temporary content access |

### Rewarded video placement

**Optimal triggers**
1. User hits free tier limit ("Watch ad for +3 uses")
2. User completes challenging task ("Bonus reward available")
3. Between content sections ("Watch to continue")
4. Daily login bonus ("Double your reward")

### Implementation example

```typescript
interface RewardedAdConfig {
  placement: string;
  reward: {
    type: 'usage' | 'feature' | 'currency' | 'ad_free';
    amount: number;
    duration?: number; // For time-based rewards
  };
  cooldown: number; // Seconds between watches
  dailyLimit: number;
}

const rewardedAdPlacements: RewardedAdConfig[] = [
  {
    placement: 'usage_limit',
    reward: { type: 'usage', amount: 3 },
    cooldown: 300, // 5 minutes
    dailyLimit: 5,
  },
  {
    placement: 'premium_preview',
    reward: { type: 'feature', amount: 1 },
    cooldown: 3600, // 1 hour
    dailyLimit: 3,
  },
  {
    placement: 'ad_free_hour',
    reward: { type: 'ad_free', amount: 1, duration: 3600 },
    cooldown: 7200, // 2 hours
    dailyLimit: 2,
  },
];
```

### Rewarded video benchmarks

| Metric | Good | Great | Excellent |
|--------|------|-------|-----------|
| Opt-in rate | 10% | 20% | 30%+ |
| Completion rate | 85% | 92% | 97%+ |
| eCPM | $10 | $20 | $30+ |
| Revenue per DAU | $0.02 | $0.05 | $0.10+ |

---

## Banner vs interstitial decision matrix

### Banner ads

**Pros:**
- Always earning (constant impressions)
- Non-intrusive
- User can ignore

**Cons:**
- Low eCPM ($0.10-0.50)
- Takes screen real estate
- Can look cheap/spammy

**Best for:**
- High-engagement apps (many sessions)
- Apps where users spend extended time
- When subscription conversion is low priority

### Interstitial ads

**Pros:**
- High eCPM ($2-10)
- Full attention
- Higher CTR

**Cons:**
- Interrupts experience
- Can cause churn if overused
- Users develop "ad blindness"

**Best for:**
- Apps with natural breaks (games, quizzes)
- Session-based usage patterns
- When user tolerance is tested and acceptable

### Decision framework

```
IF session length > 5 minutes AND natural break points exist:
  Use interstitials at break points + optional banner

ELSE IF session length > 2 minutes:
  Use banner + rewarded video

ELSE (short sessions):
  Use rewarded video only (no interruption)
```

---

## Ad frequency caps

### Recommended caps

| Ad type | Frequency cap | Reasoning |
|---------|---------------|-----------|
| Banner | Refresh every 30-60s | Balance revenue vs battery/data |
| Interstitial | Max 1 per 5 minutes | Prevent user frustration |
| Rewarded | Max 5 per day | Maintain reward value |
| Native | 1 per 5-8 content items | Keep feed mostly organic |

### Session-based caps

```typescript
interface AdFrequencyCaps {
  interstitial: {
    minSecondsBetween: number;
    maxPerSession: number;
    maxPerDay: number;
  };
  rewarded: {
    minSecondsBetween: number;
    maxPerDay: number;
  };
  banner: {
    refreshRateSeconds: number;
  };
}

const adCaps: AdFrequencyCaps = {
  interstitial: {
    minSecondsBetween: 300, // 5 minutes
    maxPerSession: 3,
    maxPerDay: 10,
  },
  rewarded: {
    minSecondsBetween: 300,
    maxPerDay: 5,
  },
  banner: {
    refreshRateSeconds: 45,
  },
};
```

### Frequency test framework

```
Experiment: Interstitial frequency
Duration: 14 days
Sample: 1000+ users per variant

Variant A: 1 per 5 minutes (conservative)
Variant B: 1 per 3 minutes (moderate)
Variant C: 1 per 2 minutes (aggressive)

Metrics:
- ARPDAU
- D7 retention
- Session length
- Sessions per day
- 1-star reviews mentioning ads
```

---

## Ad network selection

### Primary networks

| Network | Strengths | Weaknesses | eCPM range |
|---------|-----------|------------|------------|
| AdMob | Easy integration, reliable fill | Lower eCPM | $0.50-5 |
| AppLovin MAX | High eCPM, good mediation | Complex setup | $1-15 |
| Unity Ads | Great for rewarded video | Gaming focused | $5-30 |
| ironSource | Strong mediation | Resource heavy | $2-20 |
| Meta Audience Network | High eCPM for some regions | Inconsistent fill | $1-20 |

### Mediation strategy

```typescript
// Waterfall configuration (highest to lowest eCPM)
const adMediationWaterfall = [
  { network: 'applovin', eCPMFloor: 15 },
  { network: 'unity', eCPMFloor: 10 },
  { network: 'ironsource', eCPMFloor: 5 },
  { network: 'meta', eCPMFloor: 2 },
  { network: 'admob', eCPMFloor: 0 }, // Fallback
];
```

### Fill rate targets

| Region | Target fill rate | Action if below |
|--------|------------------|-----------------|
| US/UK/CA/AU | 98%+ | Add backup networks |
| Western Europe | 95%+ | Add regional networks |
| Rest of world | 85%+ | Accept lower fill, optimize eCPM |

---

## Ad revenue benchmarks

### By app category

| Category | ARPDAU (ads) | Monthly revenue per 10K DAU |
|----------|--------------|----------------------------|
| Casual games | $0.05-0.15 | $1,500-4,500 |
| Utility apps | $0.02-0.05 | $600-1,500 |
| Productivity | $0.01-0.03 | $300-900 |
| Social/Lifestyle | $0.03-0.08 | $900-2,400 |
| Education | $0.02-0.06 | $600-1,800 |

### Revenue per ad type

| Ad type | Avg eCPM | Impressions/user/day | Daily revenue per 1K users |
|---------|----------|---------------------|---------------------------|
| Banner | $0.30 | 20 | $6 |
| Interstitial | $5.00 | 3 | $15 |
| Rewarded | $20.00 | 1 | $20 |
| Native | $1.50 | 5 | $7.50 |

---

## Ad quality and user experience

### Ad quality settings

```typescript
const adContentFilters = {
  // Block categories
  blockedCategories: [
    'gambling',
    'alcohol',
    'dating',
    'political',
    'cryptocurrency',
  ],

  // Require advertiser verification
  requireVerifiedAdvertisers: true,

  // Content rating
  maxContentRating: 'teen', // 'everyone', 'teen', 'mature'
};
```

### User experience guidelines

**Do:**
- Show ads only at natural break points
- Provide clear "X" to close interstitials
- Label ads clearly
- Respect system ad preferences

**Never:**
- Show ads during critical user flows
- Use fake close buttons
- Autoplay audio without user action
- Show ads immediately on app launch

### Monitoring ad quality

Track these signals:
- User reports of inappropriate ads
- 1-star reviews mentioning ads
- Support tickets about ads
- Unusual click-through rates (may indicate misleading ads)

---

## A/B testing ads

### Test framework

```
Experiment: Ad implementation impact
Duration: 21 days
Sample: 5000+ users per variant

Variant A (Control): No ads
Variant B: Banner only
Variant C: Banner + rewarded
Variant D: Banner + rewarded + interstitial

Metrics:
- Revenue per user (ads + subscriptions)
- Subscription conversion rate
- D7/D30 retention
- Session length and frequency
- User ratings
```

### What to test

1. **Ad presence impact on subscription conversion**
   - Does showing ads increase or decrease subscription conversion?
   - Some users subscribe to remove ads (lift)
   - Some users get annoyed and churn (loss)

2. **Optimal ad load**
   - More ads = more ad revenue, less engagement
   - Find the revenue-retention sweet spot

3. **Rewarded vs forced ads**
   - Compare ARPDAU and retention
   - Rewarded usually wins on retention

4. **Ad network performance**
   - A/B test mediation configurations
   - Optimize for ARPDAU, not just eCPM

---

## Compliance and privacy

### Required disclosures

- Privacy policy must mention ad networks used
- GDPR consent required for EU users
- CCPA opt-out required for California users
- COPPA compliance for apps targeting children (usually means no personalized ads)

### Implementation checklist

- [ ] ATT (App Tracking Transparency) prompt implemented (iOS)
- [ ] GDPR consent flow for EU users
- [ ] CCPA opt-out mechanism
- [ ] Privacy policy updated with ad network list
- [ ] Age verification if required by ad networks
- [ ] Ad content filtering configured
