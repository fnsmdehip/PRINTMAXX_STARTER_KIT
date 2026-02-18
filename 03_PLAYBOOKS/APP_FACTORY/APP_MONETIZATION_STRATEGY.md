# App Monetization Strategy

Complete guide for monetizing mobile apps. Covers subscriptions, IAP, ads, and affiliate integration.

---

## Monetization models comparison

| Model | Pros | Cons | Best for |
|-------|------|------|----------|
| Hard paywall | Highest ARPU, clear value | Lower installs | Utility apps (screen blockers, habit trackers) |
| Soft paywall | More installs, builds habit | Lower conversion | Content apps, games |
| Freemium + IAP | Wide funnel, upsell opportunities | Needs many users | Games, productivity tools |
| Subscription | Predictable revenue, LTV | Churn management | Premium tools, content |
| Ads | Passive, no friction | Low CPM, hurts UX | Free tools, casual games |
| Affiliate | High margins, aligned incentives | Needs relevant products | Health, finance, lifestyle |

---

## Subscriptions (RevenueCat)

You already have RevenueCat. Here's how to maximize it.

### Pricing tiers

**Utility apps (screen blockers, trackers):**
- Monthly: $7.99-$12.99
- Annual: $39.99-$69.99 (50-60% discount)
- Lifetime: $99.99-$149.99 (optional, test)

**Content apps (devotionals, guides):**
- Monthly: $4.99-$9.99
- Annual: $29.99-$49.99

**Premium tools (AI features, advanced):**
- Monthly: $14.99-$24.99
- Annual: $99.99-$149.99

### RevenueCat implementation

```swift
// iOS - Configure offerings
Purchases.shared.getOfferings { offerings, error in
    if let package = offerings?.current?.monthly {
        // Show paywall with package
    }
}

// Track trial conversion
Purchases.shared.customerInfo { customerInfo, error in
    if customerInfo?.entitlements["premium"]?.isActive == true {
        // User is subscribed
    }
}
```

```kotlin
// Android - Configure offerings
Purchases.sharedInstance.getOfferingsWith({ offerings ->
    offerings.current?.monthly?.let { package ->
        // Show paywall with package
    }
})
```

### Paywall optimization

**High-converting elements:**
1. Social proof (X users, Y reviews)
2. Feature comparison (free vs premium)
3. Risk reversal (7-day trial, cancel anytime)
4. Urgency (limited offer, countdown)
5. Before/after results

**A/B test these:**
- Price points ($7.99 vs $9.99)
- Trial length (3 vs 7 days)
- Annual vs monthly emphasis
- Copy variations
- Button colors and placement

### Trial strategy

| App type | Trial length | Why |
|----------|--------------|-----|
| Screen blockers | 3 days | Quick value demonstration |
| Habit trackers | 7 days | Needs time to form habit |
| Content apps | 7-14 days | Sample content library |
| Productivity | 7 days | Standard |

---

## In-app purchases (IAP)

### Consumable IAP

One-time purchases that can be rebought.

**Examples:**
- Credits/tokens for AI features
- Unlock specific content pieces
- Remove ads (one-time)

**Implementation:**
```swift
// iOS StoreKit 2
let product = try await Product.products(for: ["credits_100"])
let result = try await product.first?.purchase()
```

### Non-consumable IAP

One-time purchases that persist forever.

**Examples:**
- Premium themes/icons
- Lifetime access
- Feature unlocks

### IAP pricing psychology

| Price point | Conversion | Use case |
|-------------|------------|----------|
| $0.99 | Highest | Low-value unlocks |
| $2.99-$4.99 | Good | Standard features |
| $9.99-$14.99 | Medium | Premium features |
| $29.99+ | Lower | Power users only |

---

## Ads (for free tiers)

### Ad networks for apps

| Network | CPM | Best for |
|---------|-----|----------|
| AdMob (Google) | $1-10 | General apps |
| Unity Ads | $5-20 | Games |
| AppLovin | $3-15 | Games, utilities |
| Meta Audience Network | $2-8 | Social-adjacent apps |
| IronSource | $4-12 | Games (mediation) |

### Ad formats

**Banner ads:**
- Low CPM ($0.50-$2)
- Non-intrusive
- Good for free tiers

**Interstitial ads:**
- Higher CPM ($2-10)
- Show between screens
- Don't interrupt core actions

**Rewarded video:**
- Highest CPM ($5-20)
- User-initiated
- Best UX (opt-in)

### Implementation strategy

```
Free tier: Banner + occasional interstitial
Premium tier: No ads (selling point)
```

**Rewarded video for in-app currency:**
- Watch ad = earn 10 credits
- Users self-select (engaged users watch more)
- Doesn't feel like ads (feels like earning)

---

## Affiliate links in apps (iOS StoreKit External Purchase Link)

As of 2024, iOS allows linking to external payment methods in certain regions. This enables affiliate strategies.

### How it works

1. User browses app content
2. App recommends relevant product (supplement, book, service)
3. User taps affiliate link
4. Opens Safari/external browser
5. You earn commission on purchase

### Implementation

```swift
// iOS External Purchase Links (check regional availability)
if let url = URL(string: "https://affiliate-link.com?ref=yourapp") {
    UIApplication.shared.open(url)
}
```

### Affiliate opportunities by niche

**Faith apps:**
- Christian books (Amazon Associates: 4-8%)
- Devotional subscriptions (direct deals)
- Church management software (SaaS referrals: $50-200/signup)
- Faith-based journals and planners

**Fitness apps:**
- Supplements (brands pay 10-30% commissions)
- Workout equipment (Amazon: 3-8%)
- Online coaching programs (20-50% commissions)
- Fitness apps cross-promotion

**AI/Productivity apps:**
- SaaS tools (recurring commissions)
- Online courses (10-50%)
- Books and ebooks

### Supplement affiliate strategy (fitness/health apps)

This is high-margin opportunity. Supplement brands pay 15-30% commissions.

**How to implement:**
1. App asks user goals (lose weight, build muscle, sleep better)
2. AI suggests supplement stack for goals
3. User taps to view recommendation
4. Opens affiliate link to trusted retailer

**Affiliate programs:**
| Program | Commission | Cookie |
|---------|------------|--------|
| Amazon Associates | 3-8% | 24 hours |
| iHerb | 5-10% | 30 days |
| Bodybuilding.com | 5-15% | 30 days |
| Thorne (direct) | 15-25% | 90 days |
| Athletic Greens | $25 per sale | 30 days |

**Compliance:**
- Disclose affiliate relationship
- Don't make medical claims
- Use "consult your doctor" disclaimers
- Recommend based on goals, not diagnose

### Example user flow

```
User opens FitLock app
-> Completes workout
-> App: "Nice workout! Based on your muscle-building goals, here's a recovery stack:"
-> Shows: Protein powder + Creatine + Magnesium
-> "View on iHerb" (affiliate link)
-> User purchases = you earn 10%
```

---

## Monetization by app type

### Screen blockers (PrayerLock, WalkToUnlock)

**Primary:** Hard paywall subscription
- $9.99/mo or $49.99/yr
- 3-day free trial
- No free tier

**Secondary:** None needed. Subscription covers it.

### Habit trackers

**Primary:** Freemium + subscription
- Free: Basic tracking (3 habits)
- Premium: Unlimited habits, analytics, themes

**Secondary:** Themed icon packs (IAP $2.99 each)

### Faith apps

**Primary:** Subscription
- $4.99/mo or $29.99/yr
- Daily devotional content

**Secondary:**
- Affiliate links to Christian books
- Partner with churches for bulk licensing

### Fitness apps

**Primary:** Freemium subscription
- Free: Basic features
- Premium: AI coaching, analytics

**Secondary:**
- Supplement affiliate recommendations
- Equipment affiliate links
- Partner program with gyms

---

## Hybrid monetization example

PrayerLock monetization stack:

```
Revenue stream 1: Subscriptions (80% of revenue)
- $9.99/mo or $49.99/yr
- Hard paywall, 3-day trial

Revenue stream 2: Affiliate (15% of revenue)
- Christian book recommendations after devotionals
- Faith-based journal/planner affiliate
- Partner with YouVersion or similar

Revenue stream 3: Premium add-ons (5% of revenue)
- Custom icon packs ($2.99)
- Additional devotional content packs ($4.99)
```

---

## RevenueCat dashboard metrics to track

| Metric | Target | Action if below |
|--------|--------|-----------------|
| Trial start rate | >25% | Improve onboarding |
| Trial conversion | >15% | Optimize paywall |
| Monthly churn | <8% | Improve engagement |
| MRR growth | >10%/mo | Scale acquisition |
| Realized LTV | >$30 | Reduce churn, raise prices |

---

## Pricing A/B test framework

**Test 1:** Monthly vs annual emphasis
- Control: Monthly highlighted
- Variant: Annual highlighted with savings

**Test 2:** Price points
- Control: $9.99/mo
- Variant: $12.99/mo (test price elasticity)

**Test 3:** Trial length
- Control: 3-day trial
- Variant: 7-day trial

**Test 4:** Discount messaging
- Control: "$49.99/yr"
- Variant: "$49.99/yr (save 58%)"

Run each test for 2 weeks minimum, 1000+ users per variant.

---

## Legal/compliance checklist

- [ ] Apple/Google IAP rules followed
- [ ] External purchase links only in allowed regions
- [ ] Affiliate relationships disclosed
- [ ] No medical/health claims without disclaimer
- [ ] Subscription terms clearly stated
- [ ] Easy cancellation process documented
- [ ] Privacy policy covers monetization data

---

## Quick start

1. **Week 1:** Implement RevenueCat subscription
2. **Week 2:** Add paywall with 3-day trial
3. **Week 3:** A/B test paywall copy
4. **Week 4:** Add affiliate recommendations
5. **Month 2:** Analyze data, optimize pricing

Start with subscriptions. Add affiliate once you have users.

---

Created: 2026-01-21
