# PrayerLock PRD

**App Name:** PrayerLock
**Tagline:** Pray First, Phone Second
**Category:** Screen Time Blocker (Faith Niche)
**Target:** Christians who want to start their day with prayer before phone

---

## Problem

- People reach for phone immediately upon waking
- Doomscrolling replaces morning devotion time
- Existing screen time apps are secular and shame-based
- No app connects phone access to spiritual practice

## Solution

Lock phone until user completes morning prayer/devotion. Positive framing (reward, not punishment).

---

## Core Features (MVP)

### 1. Morning Lock
- Activates at user-set time (default 6am)
- Shows prayer prompt instead of lock screen
- Timer for prayer duration (5/10/15/30 min options)
- Must complete timer to unlock phone

### 2. Prayer Content
- Daily verse (API: Bible Gateway or static list)
- Simple prayer prompts ("Thank God for...", "Pray for...")
- Optional: Audio prayers from library

### 3. Progress Tracking
- Streak counter (consecutive days)
- Monthly calendar view
- Total prayer time logged

### 4. Unlock Mechanism
- Timer completion unlocks phone
- Emergency bypass with 24hr shame counter
- Optional: 3 wrong attempts = longer prayer time

---

## Monetization

### Free Tier
- Basic morning lock
- 5-minute prayer timer
- Limited verse library

### Premium ($4.99/mo or $29.99/year)
- Extended prayer times (30/60 min)
- Full devotional library
- Family accountability (see family members' streaks)
- Custom prayer prompts
- Remove ads
- Streak freeze (1 per week)

### Affiliate Links
- Bible apps
- Christian books (Amazon)
- Prayer journals
- Church apps

---

## Technical Stack

- **Framework:** React Native + Expo
- **Backend:** Supabase (auth + data)
- **Payments:** RevenueCat
- **Analytics:** Mixpanel or Amplitude
- **Push:** Expo Push Notifications

---

## Competitive Analysis

| App | Monthly Revenue | Gap |
|-----|-----------------|-----|
| Hallow | $2M+/mo | Catholic focus, no screen lock |
| Glorify | $500k/mo | No phone restriction |
| Opal | $600k/mo | Secular, no faith content |
| BePresent | $300k/mo | Secular, no faith content |

**Our angle:** First faith-based screen time blocker.

---

## Success Criteria

1. Ship to TestFlight within 2 weeks
2. 100 downloads in first month
3. 10% free-to-paid conversion
4. $1k MRR within 90 days

---

## MVP Checklist

- [ ] Expo project initialized
- [ ] Lock screen UI
- [ ] Timer functionality
- [ ] Basic verse display (static JSON)
- [ ] Local storage for streak
- [ ] RevenueCat paywall
- [ ] App Store assets (icon, screenshots)
- [ ] Submit to TestFlight

---

## Design Notes

- **Colors:** Gold/amber (#F5A623) + deep blue (#1A237E)
- **Mascot:** Praying hands or dove icon
- **Tone:** Warm, encouraging, not judgmental
- **UI:** Minimal, calm, focus on content

---

## Launch Checklist

- [ ] ASO keywords: prayer app, morning devotion, christian screen time, phone detox faith
- [ ] Landing page with email capture
- [ ] TikTok content (day-in-life, transformation)
- [ ] Christian influencer outreach
- [ ] Reddit: r/Christianity, r/TrueChristian, r/digitalminimalism
