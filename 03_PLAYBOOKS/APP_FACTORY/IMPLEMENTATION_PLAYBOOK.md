# APP_FACTORY Implementation Playbook

**Method ID:** MM001
**ROI Rank:** #1 (Score: 94/100)
**Revenue model:** IAP + Subscriptions + Affiliate
**Time investment:** 10-15 hrs/week ongoing, 40-80 hrs first app
**Capital required:** $124 one-time (Apple $99 + Google $25)
**Difficulty:** 6/10
**Platform risk:** 4/10 (Apple review process is main risk)
**Monthly potential:** $1,000-50,000
**First dollar timeline:** 4-8 weeks from start

---

## Overview

Build mobile apps using React Native/Expo, monetize with hard paywalls and subscriptions via RevenueCat, distribute through content farm accounts and AI personas. The Lock App pattern (lock phone until positive behavior completed) is the PRINTMAXX competitive moat. Same infrastructure reuses across PrayerLock, WalkToUnlock, StudyLock, and future apps.

Proof: Connor Burd $185k/mo from app portfolio. Max Artemov $22k/mo from 30 apps in under 1 year. Forest app $100k/mo from focus timer with 44M downloads.

---

## Prerequisites

### Accounts needed
- [ ] Apple Developer ($99/yr) - developer.apple.com/programs/enroll
- [ ] Google Play Console ($25 one-time) - play.google.com/console/signup
- [ ] RevenueCat (free tier) - app.revenuecat.com/signup
- [ ] Stripe (free) - dashboard.stripe.com/register
- [ ] Mixpanel (free tier) - mixpanel.com/register

### Tools/software
- [ ] Node.js 18+ installed
- [ ] Expo CLI: `npm install -g expo-cli`
- [ ] Xcode (Mac only, required for iOS)
- [ ] Android Studio (optional, for Android testing)
- [ ] Claude Code for AI-assisted development

### Existing assets to use
- `builds/` - 14+ app builds ready (biomaxx READY, PrayerLock 85%)
- `APP_MONETIZATION_STRATEGY.md` - Full monetization guide
- `PAYWALL_PSYCHOLOGY_AB_PLAYBOOK.md` - Paywall optimization (8-part system)
- `APP_LAUNCH_FULL_STACK.md` - Launch checklist
- `APP_STORE_REJECTION_GUIDE.md` - Avoid rejections
- `REVENUECAT_INTEGRATION_GUIDE.md` - RevenueCat code
- `ASSET_GENERATION_GUIDE.md` - Icon/visual generation with Gemini
- `LEDGER/APP_CLONE_OPPORTUNITIES.csv` - Apps to clone

---

## Step-by-step implementation

### Day 1: Environment setup (2-3 hours)

**Task 1: Install development tools**
```bash
brew install node
npm install -g expo-cli @expo/ngrok
node --version  # Should be 18+
```

**Task 2: Create developer accounts**
- Apple Developer: developer.apple.com/programs/enroll ($99/yr, 24-48hr approval)
- Google Play: play.google.com/console/signup ($25 one-time, immediate)

**Task 3: Set up RevenueCat**
1. Sign up at app.revenuecat.com
2. Create project, add iOS + Android apps
3. Configure offerings: Monthly $6.99-7.99, Annual $39.99-49.99 (show as $3.33-4.17/mo), Lifetime $99.99 optional
4. Create "premium" entitlement
5. Reference: `REVENUECAT_INTEGRATION_GUIDE.md`

### Day 2-7: Build your first app (15-30 hours)

**Task 4: Pick app**

| App | Status | Market Validation | Build Time |
|-----|--------|-------------------|------------|
| biomaxx | READY to ship | Looksmaxxing trend | 0 days |
| PrayerLock | 85% done | Hallow $51.4M/yr, ZERO competitors | 3-5 days |
| WalkToUnlock | 35-40% | Sweatcoin refugees 170M users | 7-10 days |
| StudyLock | 40% | Forest $100k/mo validates | 7-10 days |

**Task 5: Run existing build**
```bash
cd MONEY_METHODS/APP_FACTORY/builds/biomaxx-sdk54
npm install
npx expo start --ios
```

**Task 6: Implement hard paywall (CRITICAL for revenue)**

Onboarding flow (this order matters):
1. Welcome screen (app name + tagline)
2. Personalization quiz (3-5 questions, builds investment)
3. Value preview (show what they get)
4. Social proof ("10,000+ users improved their habits")
5. HARD PAYWALL (annual-first display, save X% badge)
6. App opens only after subscription or trial start

Hard paywalls = 10x better conversion than soft. 80% of conversions happen during onboarding.

Existing paywall code:
- `builds/biomaxx-sdk54/subscriptionService.ts` - RevenueCat wrapper
- `builds/biomaxx-sdk54/paywall.tsx` - Paywall screen
- `builds/biomaxx-sdk54/usePremiumGate.ts` - Premium gate hook

### Day 7-14: App Store submission

**Task 7: Generate app icon**
Prompt for Gemini/Leonardo: "3D app icon for [APP_NAME], [NICHE] theme, gradient [COLORS], glossy finish, modern design, isometric perspective, 1024x1024"
See: `assets/LOCK_APPS_ICON_PROMPTS_V3.md`
Requirements: 1024x1024 PNG, no transparency, 3D/gradient, NOT a plain letter.

**Task 8: Create screenshots**
6 screenshots at 1290x2796 (6.5" iPhone). Show app in use with text overlay.

**Task 9: Write listing**
Title (30 chars): "[App Name] - [Key Benefit]"
Subtitle (30 chars): "[Secondary benefit]"
Keywords (100 chars, comma-separated)
Full ASO checklist: `OPS/GTM_OPTIMIZATION_CHECKLIST.md`

**Task 10: Submit**
```bash
npx eas build --platform ios --profile production
npx eas submit --platform ios
```
Review: 24-48 hours. Common issues: `APP_STORE_REJECTION_GUIDE.md`

### Week 3-4: Launch and optimize

**Task 11: Create 3 social accounts per app** (TikTok, IG, X)
Post 3x/day. Content: feature demos, reply bait, build-in-public updates.

**Task 12: Set up web-to-app funnel (MM092)**
Landing page with Stripe checkout. Saves 30% vs App Store.
See: `WEB_TO_APP_FUNNEL/WEB_TO_APP_FUNNEL_PLAYBOOK.md`

**Task 13: A/B test paywall with RevenueCat experiments**
Test A: Annual-first vs monthly-first
Test B: $49.99/yr vs $39.99/yr
Test C: 3-day trial vs 7-day trial

---

## Revenue mechanics

### How money flows
User discovers app -> Downloads -> Onboarding (3-5 screens) -> Hard paywall -> Trial/Subscribe -> RevenueCat -> Apple/Google takes 15-30% -> Your Stripe

### Pricing (annual-first display)
Annual (DEFAULT): $49.99/yr displayed as "$4.17/mo, Save 48%"
Monthly: $7.99/mo (shown as expensive alternative)
Lifetime: $99.99 (optional aspirational anchor)

### First dollar timeline
Day 0-7: Build and submit. Day 7-14: Review. Day 14-21: First installs. Day 28-56: First revenue.

---

## Scaling path

### $0-1K/mo (Month 1-3)
1-2 apps live. 100-500 downloads/mo. 1.7% conversion. Focus: paywall optimization, ASO.

### $1-10K/mo (Month 3-6)
3-5 apps. 500-5,000 downloads/mo. 3-4% conversion. Add: content promotion, web funnel (+34.5% revenue/user).

### $10K+/mo (Month 6-12)
10+ apps (portfolio). Clipper network launches (MM017). Paid ads. Cross-sell between apps. Kill bottom 50%, 2x winners.

---

## Risk management

- **Apple rejection:** Follow APP_STORE_REJECTION_GUIDE.md
- **Revenue share changes:** Web-to-app funnel hedges
- **Competitive:** Lock mechanism is unique, no competitor locks phone for prayer/walking/studying
- **Failure modes:** Ship MVP in 14 days max. Hard paywall not soft. Annual-first not monthly. No generic icons. Always have analytics.

---

## Success metrics

| Metric | Good | Great | Kill |
|--------|------|-------|------|
| Trial start rate | 30% | 50%+ | <15% |
| Trial-to-paid | 40% | 60%+ | <25% |
| Day 1 retention | 30% | 50%+ | <15% |
| Monthly churn | 8% | 5% | >15% |
| ARPU | $2 | $5+ | <$0.50 |

Kill: 90 days with <$100 MRR and declining downloads.
Scale: MRR > $500 with positive MoM growth -> add paid ads.

---

## Cross-pollination

| Method | Synergy | How it stacks |
|--------|---------|---------------|
| MM092 WEB_TO_APP_FUNNEL | 98 | Bypass 30% store fee |
| MM019 PORTFOLIO_APP_BUILDER | 95 | 30-app portfolio strategy |
| MM017 CLIPPER_NETWORK | 95 | $0.14/download launches |
| AI005 FITNESS_COACHES | 95 | AI persona promotes app |
| MM006 CONTENT_FARM | 95 | Content accounts drive downloads |
| MM002 INFO_PRODUCTS | 90 | Course from app experience |
| MM015 NEWSLETTER | 90 | Newsletter promotes apps |
