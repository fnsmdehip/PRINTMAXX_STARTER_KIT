# WalkToUnlock PRD

**App Name:** WalkToUnlock
**Tagline:** Walk Before You Scroll
**Category:** Screen Time Blocker (Fitness Niche)
**Target:** Fitness-minded people who want to reduce phone addiction

---

## Problem

- Phone addiction reduces physical activity
- Morning doomscrolling kills motivation
- Existing fitness apps don't address phone use
- No app connects phone access to movement

## Solution

Lock phone until user walks a set number of steps. Gamified fitness meets digital wellness.

---

## Core Features (MVP)

### 1. Step-Gated Lock
- Activates at user-set time or all-day mode
- Shows step counter instead of home screen
- Requires X steps to unlock (100/500/1000/custom)
- Health app integration for step tracking

### 2. Progress Display
- Real-time step count
- Progress bar to unlock
- Motivational messages at milestones

### 3. Gamification
- Daily streak counter
- Weekly step totals
- Achievements/badges
- Personal records

### 4. Customization
- Step goal by time of day
- Weekend vs weekday settings
- App whitelist (emergency calls always)

---

## Monetization

### Free Tier
- Basic step lock (100 steps max)
- Morning lock only
- Limited achievements

### Premium ($4.99/mo or $29.99/year)
- Unlimited step goals
- All-day lock mode
- Full achievement system
- Workout integration (gym check-in unlocks)
- Friends leaderboard
- Remove ads
- Streak freeze

### Affiliate Links
- Fitness trackers (Whoop, Oura)
- Running shoes (Amazon)
- Gym memberships
- Fitness apps (Fitbod, Strong)
- Protein/supplements

---

## Technical Stack

- **Framework:** React Native + Expo
- **Health Data:** expo-sensors + HealthKit/Google Fit
- **Backend:** Supabase
- **Payments:** RevenueCat
- **Analytics:** Mixpanel

---

## Competitive Analysis

| App | Monthly Revenue | Gap |
|-----|-----------------|-----|
| Opal | $600k/mo | No fitness component |
| BePresent | $300k/mo | No step tracking |
| Brainrot | $100k/mo | No fitness component |
| Step trackers | Various | No phone lock |

**Our angle:** First fitness-gated screen time blocker.

---

## Success Criteria

1. Ship to TestFlight within 2 weeks
2. 500 downloads in first month
3. 8% free-to-paid conversion
4. $2k MRR within 90 days

---

## MVP Checklist

- [ ] Expo project initialized
- [ ] Step counter integration
- [ ] Lock screen UI with progress
- [ ] Local storage for streak/stats
- [ ] RevenueCat paywall
- [ ] App Store assets
- [ ] TestFlight submission

---

## Design Notes

- **Colors:** Electric green (#00FF88) + charcoal (#1A1A1A)
- **Mascot:** Running shoe or footstep icon
- **Tone:** Energetic, challenging, competitive
- **UI:** Bold, fitness aesthetic, dark mode default

---

## Launch Checklist

- [ ] ASO keywords: step counter lock, fitness screen time, walk to unlock phone, exercise phone block
- [ ] Landing page with email capture
- [ ] TikTok content (before/after, step challenge)
- [ ] Fitness influencer outreach
- [ ] Reddit: r/fitness, r/running, r/digitalminimalism, r/nosurf
