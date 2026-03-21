# SoberStreak — Upgrade Spec (2026-03-21)
## Status: ITERATE_EXISTING_NOW | Score: 121 | Market: HIGH

## Source Intelligence
- r/NoFap: 1.24M subs, zero paid dedicated streak app
- Quittr privacy scandal: exposed millions of users' sensitive data
- HabitSwipe: $800 revenue, 2.5K users in 2 months (comparable app)
- Review prompt timing: +0.8 stars by firing after value moment (not onboarding)

## What Exists
- 693-line PWA at soberstreak.surge.sh
- Features: streak tracking, milestones, journal, heatmap, craving support
- Monetization: NONE
- Review prompt: NONE
- Multiple habits: NO (single habit only)

## Core Upgrades (in priority order)

### 1. Review Prompt Timing (score impact: +0.8 stars)
- Trigger: After 7-day milestone reached AND user checks in successfully
- NOT on: First open, second open, onboarding
- Prompt copy: "7 days clean. If SoberStreak helped, a quick rating keeps us going."
- iOS: SKStoreReviewRequest | Web: Show modal with App Store link
- Gate: Only fire once per 90 days max

### 2. Premium Tier (monetization)
- Free: Single habit tracking, 10 milestones, journal, heatmap
- Premium ($2.99/mo or $19.99/yr): Multiple habits (up to 5), pattern insights,
  custom milestone messages, data export, no upsell banners
- Paywall trigger: When user tries to add 2nd habit
- Payment: Stripe payment link (pre-built, no backend required)
- Annual-first display: show $19.99/yr first, $2.99/mo as secondary option

### 3. NoFap Community Targeting
- Update description to lead with NoFap/PMO angle
- Add "NoFap Mode" toggle with community-specific milestone messages
- Add r/NoFap milestone language: "hardmode", "easy mode", "PMO", "flatline"
- Privacy badge: "Unlike Quittr — zero data, zero servers, zero surveillance"

### 4. Multiple Habit Support (premium gate)
- Free: 1 habit (default: "Sobriety")
- Premium: alcohol, weed, smoking, NoFap, gambling, social media, porn
- Each habit gets its own streak, heatmap, and milestone track

## ASO Targets
- Primary: "nofap tracker", "sobriety streak app", "private sobriety tracker"
- New: "nofap app no data", "sobriety counter offline", "quit porn tracker"
- Price point: $1.99/mo soft launch → test $2.99/mo after 100 users

## Build Approach
- Upgrade existing PWA in-place (no framework switch)
- Add premium logic via localStorage flag + Stripe checkout redirect
- Review prompt via Web Share API + review link modal
- Target: 30-min build, then deploy same day

## Revenue Model
- Month 1 target: 50 premium users × $2.99 = $150/mo
- Month 3 target: 200 premium users × $2.99 = $600/mo
- Path to $1K/mo: 334 subs OR annual plan mix at $19.99/yr
