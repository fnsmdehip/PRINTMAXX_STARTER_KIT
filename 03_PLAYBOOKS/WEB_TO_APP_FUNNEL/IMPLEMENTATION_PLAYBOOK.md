# WEB_TO_APP_FUNNEL Implementation Playbook

**Method ID:** MM092
**ROI Rank:** #8 (Score: 85/100)
**Revenue model:** Direct web subscriptions (bypass 30% App Store fee)
**Time investment:** 5-8 hrs/week ongoing, 15-25 hrs initial build
**Capital required:** $0 (Stripe + Vercel free tiers)
**Difficulty:** 7/10
**Platform risk:** 3/10 (web payments are decentralized)
**Monthly potential:** $2,000-20,000
**First dollar timeline:** 2-3 weeks from launch

---

## Overview

Build web-based payment funnels that bypass the 30% Apple/Google App Store commission. Users discover your app, land on a web page, subscribe via Stripe, then unlock premium features in the app. 82% of top-grossing apps use web funnels. Some apps get 90% of revenue through web rather than in-app purchases.

This is the HIGHEST synergy method in PRINTMAXX (score: 98 with APP_FACTORY). Every app you build should have a web funnel.

Key insight: Apple allows linking to external payment pages in certain regions (US, EU, others). Even where restricted, you can drive web traffic through content marketing, social media, and email. The user subscribes on web, your app checks entitlement via RevenueCat or custom API.

Proof: Spotify gets majority of subs via web. Netflix entirely web-based. Duolingo, Headspace, Calm all have web funnels. Forest app ($100K/mo) uses web + app. PRINTMAXX has full 1,000+ line playbook ready.

FULL DETAILED PLAYBOOK: `WEB_TO_APP_FUNNEL_PLAYBOOK.md` (1,000+ lines, covers everything below in extreme detail)

---

## Prerequisites

### Accounts needed
- [ ] Stripe (free) - stripe.com
- [ ] Vercel (free tier) - vercel.com
- [ ] RevenueCat (free tier) - revenuecat.com
- [ ] Domain for landing page ($9-12/yr)

### Tools/software
- [ ] Next.js (PRINTMAXX stack) - for landing page
- [ ] Stripe Checkout or Stripe Payment Links - for payments
- [ ] RevenueCat Web SDK or Custom API - for entitlement sync

### Existing assets to use
- `WEB_TO_APP_FUNNEL_PLAYBOOK.md` - **FULL 1,000+ line playbook (START HERE)**
- `APP_MONETIZATION_STRATEGY.md` - Pricing strategy
- `PAYWALL_PSYCHOLOGY_AB_PLAYBOOK.md` - Paywall optimization
- `REVENUECAT_INTEGRATION_GUIDE.md` - RevenueCat implementation
- `LANDING/printmaxx-site/` - Next.js site (reuse infrastructure)

---

## Step-by-step implementation

### Day 1-3: Build landing page (8-12 hours)

**Task 1: Create app landing page**

Build a Next.js landing page for your app (reuse PRINTMAXX site infrastructure):

```bash
cd LANDING/printmaxx-site
# Create new route for app
mkdir -p app/apps/prayerlock
```

Landing page structure:
```
1. Hero: App name + tagline + screenshot + CTA button
2. Problem: What pain point does your app solve?
3. Solution: How your app solves it (3-4 features)
4. Social proof: Download count, ratings, testimonials
5. Pricing: Web pricing (show savings vs App Store)
6. FAQ: Common questions
7. Final CTA: Subscribe now + download app
```

**Task 2: Set up Stripe Checkout**

```bash
npm install stripe @stripe/stripe-js
```

Create Stripe products matching app subscriptions:
- Monthly: $6.99/mo (same as in-app, or slightly cheaper)
- Annual: $39.99/yr (show as "$3.33/mo - Save 52%")
- Lifetime: $79.99 (optional, lower than in-app $99.99 to incentivize web)

Web prices can be lower because you save 30% on fees:
```
In-app:  $49.99/yr - Apple takes $15.00 - You get $34.99
Web:     $39.99/yr - Stripe takes $1.46  - You get $38.53
Result:  10% cheaper for user, 10% MORE revenue for you
```

**Task 3: Connect Stripe to RevenueCat**

RevenueCat syncs web purchases with in-app entitlements:
1. In RevenueCat dashboard: Settings > Integrations > Stripe
2. Add Stripe API keys
3. Map Stripe products to RevenueCat offerings
4. User subscribes on web -> RevenueCat updates entitlement -> App checks entitlement

Reference: `REVENUECAT_INTEGRATION_GUIDE.md` for exact code.

### Day 3-5: Payment flow (4-6 hours)

**Task 4: Build checkout flow**

Stripe Checkout (hosted, fastest):
1. User clicks "Subscribe" on landing page
2. Redirect to Stripe Checkout (hosted by Stripe)
3. User enters payment
4. Redirect back to success page
5. Webhook fires -> Update RevenueCat entitlement

OR Stripe Payment Links (no-code):
1. Create Payment Link in Stripe dashboard
2. Add link to landing page button
3. Done. No code needed.

Start with Payment Links for speed. Migrate to custom Checkout for more control.

**Task 5: Build success page**

After payment:
```
"You're subscribed! Here's what to do next:

1. Download [App Name] from the App Store [link]
2. Open the app and sign in with [email used to pay]
3. Premium features are now unlocked!

Having trouble? Email support@yourapp.com"
```

### Day 5-7: Drive traffic (4-6 hours)

**Task 6: Set up traffic sources**

Traffic to web funnel (where the 30% savings magic happens):

1. **Social media bio links** - All content accounts link to web page, not App Store
2. **Email/newsletter** - "Subscribe on our site for 10% off" (pass savings to user)
3. **Blog/SEO content** - Landing page ranks for "[app name] pricing"
4. **Content farm accounts** - Bio links point to web funnel
5. **Cold outreach** - Share web link in affiliate recruitment
6. **Reddit/forums** - Link to web page in relevant discussions

**Task 7: A/B test pricing**

Test with Stripe experiments or simple page variants:
- Test A: Show web-only discount ("Save 20% by subscribing here")
- Test B: Same price as in-app, position as "easier checkout"
- Test C: Annual-only on web (push highest LTV plan)

Track: Conversion rate, average revenue per visitor, refund rate.

### Week 2-4: Optimize and scale

**Task 8: Add email capture for non-buyers**

Not everyone will buy immediately. Capture emails:
```
Landing page → Email popup (5% discount for subscribing to newsletter)
→ 5-email nurture sequence → Re-pitch subscription
```

Expected: 3-5% of visitors give email, 10-20% of those convert within 30 days.

**Task 9: Build for every app**

Replicate this funnel for each PRINTMAXX app:
- PrayerLock: prayerlock.app or printmaxx.com/apps/prayerlock
- WalkToUnlock: walktounlock.app
- StudyLock: studylock.app
- BioMaxx: biomaxx.app

Same infrastructure, different landing pages. Copy the pattern.

---

## Revenue mechanics

### How money flows
User finds app (social, search, content) -> Lands on web page -> Subscribes via Stripe -> Stripe takes 2.9% + $0.30 -> You get 97%+ of revenue -> RevenueCat syncs entitlement -> User opens app with premium unlocked

### Savings vs App Store

| Scenario | Annual Sub | Platform Cut | You Keep |
|----------|-----------|--------------|----------|
| In-app purchase | $49.99 | 30% ($15.00) | $34.99 |
| Web purchase (Stripe) | $49.99 | 2.9%+$0.30 ($1.75) | $48.24 |
| Web discounted | $39.99 | 2.9%+$0.30 ($1.46) | $38.53 |

Web at $39.99 gives you MORE revenue ($38.53) than in-app at $49.99 ($34.99). User pays less, you earn more.

### First dollar timeline
Day 0-5: Build funnel. Day 5-7: Drive traffic. Day 7-21: First web subscription.

---

## Scaling path

### $0-2K/mo (Month 1-2)
1 app funnel live. Organic traffic only. 10-50 web subs. Focus: conversion rate optimization.

### $2K-10K/mo (Month 2-4)
3-5 app funnels live. Email capture + nurture. 50-200 web subs. Focus: traffic volume, email sequences.

### $10K-20K+/mo (Month 4-8)
All apps have web funnels. Paid traffic to web pages. 200-500+ web subs. Focus: paid acquisition with positive ROAS.

---

## Risk management

- **Apple guidelines:** Apple allows linking to external payment in US/EU under DMA. Other regions may restrict. Always offer in-app purchase as fallback.
- **Stripe disputes:** Keep dispute rate under 0.5%. Send confirmation emails. Offer easy cancellation.
- **RevenueCat sync issues:** Test entitlement sync thoroughly before launch. Handle edge cases (user buys web, installs on different device).
- **Low conversion:** Optimize landing page (hero image, pricing display, social proof). Test pricing. Add urgency (limited-time discount).
- **Technical complexity:** Start with Stripe Payment Links (no code). Graduate to Checkout for custom flows.

---

## Success metrics

| Metric | Good | Great | Kill |
|--------|------|-------|------|
| Landing page conversion | 3% | 8%+ | <1% |
| Web vs in-app revenue split | 20% | 50%+ | <5% |
| Revenue per visitor | $0.50 | $2.00+ | <$0.10 |
| Stripe dispute rate | <0.5% | <0.1% | >1% |
| Email capture rate | 3% | 8%+ | <1% |

Kill: 60 days with <$100 web revenue and <1% conversion.
Scale: Web revenue >$500/mo -> add paid traffic, build funnels for all apps.

---

## Cross-pollination

| Method | Synergy | How it stacks |
|--------|---------|---------------|
| MM001 APP_FACTORY | 98 | Every app needs a web funnel |
| MM019 PORTFOLIO_APPS | 95 | Portfolio of apps = portfolio of funnels |
| MM015 NEWSLETTER | 90 | Newsletter drives web funnel traffic |
| MM006 CONTENT_FARM | 85 | Content accounts link to web funnel |
| MM007 COLD_OUTBOUND | 80 | Cold outreach shares web links |
| MM009 AI_INFLUENCER | 85 | Personas promote web signup |
