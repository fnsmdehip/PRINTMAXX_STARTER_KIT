# PrayerLock - Product Requirements Document

**App Name:** PrayerLock
**Niche:** Faith (Christian focus, expandable to multi-faith)
**Method:** AFM012 - Screen Time Blocker Variant
**Monetization:** Hard Paywall - $9.99/mo or $49.99/yr

---

## Overview

PrayerLock blocks distracting apps until the user completes their morning devotional routine. The phone stays locked until prayer time is fulfilled.

Core insight: Christians want to pray more but get distracted. Lock the distraction until the habit is done.

---

## Problem Statement

Christians report wanting to spend more time in prayer and scripture but consistently fail due to:
1. Phone notifications interrupt morning quiet time
2. Social media scroll replaces devotional time
3. No accountability mechanism for spiritual habits
4. Guilt cycle: miss prayer, feel bad, distract with phone, repeat

---

## Solution

Lock selected apps until user completes a configurable devotional routine:
- Timer-based prayer (5-30 min)
- Scripture reading (passage completion)
- Journaling (minimum word count)
- Audio devotional (completion tracking)

---

## User Stories (MVP - Single Context Window Implementable)

### US001: App Blocking Setup
**As a** user
**I want to** select which apps get blocked
**So that** only distracting apps are locked during devotional time

**Acceptance Criteria:**
- Display list of installed apps
- Allow multi-select for blocking
- Persist selection to local storage
- Common defaults pre-selected (social media, games)

**Implementation Notes:**
- Use device accessibility API
- Store config in AsyncStorage (RN) or SharedPreferences (Flutter)
- Single screen, checkbox list UI

---

### US002: Devotional Timer
**As a** user
**I want to** set a prayer timer duration
**So that** I know how long to pray before apps unlock

**Acceptance Criteria:**
- Slider or picker for 5-60 minutes
- Timer displays countdown
- Audio/haptic notification at completion
- Cannot be bypassed (no skip button)

**Implementation Notes:**
- Use native timer APIs
- Full-screen lock during timer
- Prevent app switching during active session

---

### US003: Scripture Reading Module
**As a** user
**I want to** read a Bible passage before unlocking
**So that** I engage with scripture daily

**Acceptance Criteria:**
- Display daily verse or passage
- Scroll to bottom required to complete
- Reading time tracked (minimum threshold)
- Mark as complete button appears after threshold

**Implementation Notes:**
- Integrate free Bible API (bible-api.com or similar)
- Track scroll position
- 60-second minimum engagement

---

### US004: Unlock Verification
**As a** user
**I want** the app to verify I completed my devotional
**So that** I can't cheat the system

**Acceptance Criteria:**
- Completion requires timer OR scripture reading
- Optional: both required in settings
- Unlock persists for configurable hours (default: until next morning)
- Reset happens at user-configured time (default: 5am)

**Implementation Notes:**
- Store completion timestamp
- Compare against daily reset time
- Accessibility service controls app blocking

---

### US005: Hard Paywall
**As a** new user
**I want to** see the value proposition before paying
**So that** I understand what I'm buying

**Acceptance Criteria:**
- 3-day free trial with full functionality
- Paywall screen shows pricing clearly
- Features locked after trial without subscription
- Restore purchases option

**Implementation Notes:**
- RevenueCat for subscription management
- Paywall appears on app launch post-trial
- Track trial start date in local storage

---

### US006: Streak Tracking
**As a** user
**I want to** see my prayer streak
**So that** I stay motivated

**Acceptance Criteria:**
- Display current streak (consecutive days)
- Show longest streak achieved
- Calendar view of completed days
- Streak break notification/warning

**Implementation Notes:**
- Simple counter in local storage
- Calendar component for history view
- Optional push notification for streak reminders

---

### US007: Emergency Unlock
**As a** user
**I want** an emergency unlock option
**So that** I can access my phone in genuine emergencies

**Acceptance Criteria:**
- Hidden in settings (not prominent)
- Requires typing "I am breaking my commitment" to unlock
- Logs the bypass (shown in history)
- Resets streak

**Implementation Notes:**
- Intentionally friction-heavy
- Text input validation
- Logged to shame user into not using

---

## Future Features (Post-MVP)

- **Prayer journal:** Written reflection with prompts
- **Audio devotionals:** Partner with ministries for content
- **Community:** Share streaks with accountability partners
- **Church integration:** Church-wide challenges
- **Multi-faith:** Muslim prayer times, Jewish morning prayers
- **Widget:** Lock screen widget showing progress
- **Apple Watch:** Companion app for quick logging

---

## MVP Feature Set

| Feature | Priority | Effort | Included in MVP |
|---------|----------|--------|-----------------|
| App blocking | P0 | Medium | Yes |
| Prayer timer | P0 | Low | Yes |
| Scripture reading | P0 | Medium | Yes |
| Streak tracking | P1 | Low | Yes |
| Hard paywall | P0 | Low | Yes |
| Emergency unlock | P1 | Low | Yes |
| Prayer journal | P2 | Medium | No |
| Community | P3 | High | No |
| Audio devotionals | P2 | Medium | No |

---

## Monetization Structure

### Pricing
- **Monthly:** $9.99/mo
- **Annual:** $49.99/yr (save 58%)
- **Lifetime:** $99.99 (optional, test later)

### Why Hard Paywall
Reference: Opal ($600k MRR), BePresent ($300k MRR) both use hard paywall. Screen blockers convert well with paywalls because:
1. Clear value proposition (block = result)
2. Low refund rate (users see it working)
3. No free tier dilutes urgency

### Trial Strategy
- 3-day free trial
- Full functionality during trial
- Paywall after trial expiration
- No feature-gating (all or nothing)

---

## Success Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| Trial to Paid | >15% | RevenueCat dashboard |
| Day 7 Retention | >40% | Analytics |
| Average Streak | >7 days | In-app tracking |
| Monthly Churn | <8% | RevenueCat |
| App Store Rating | >4.5 | Store reviews |

---

## Launch Checklist

### Pre-Launch
- [ ] Core features complete and tested
- [ ] RevenueCat integration working
- [ ] App Store screenshots designed
- [ ] App Store description written (SEO optimized)
- [ ] Privacy policy created
- [ ] Terms of service created
- [ ] TestFlight beta with 20+ users
- [ ] Bug fixes from beta feedback

### Launch
- [ ] Submit to App Store
- [ ] Submit to Google Play
- [ ] Create TikTok account (@prayerlock)
- [ ] Record 5 launch TikToks
- [ ] Post in Christian Facebook groups
- [ ] Reach out to faith influencers
- [ ] Set up basic landing page

### Post-Launch (Week 1-4)
- [ ] Monitor reviews, respond to all
- [ ] Post 3 TikToks per day
- [ ] Collect user testimonials
- [ ] A/B test paywall copy
- [ ] Add requested features from feedback
- [ ] Reach $1k MRR milestone

---

## Risks and Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Apple rejects accessibility usage | Medium | High | Follow Apple guidelines exactly, appeal if needed |
| Users find bypass workarounds | Medium | Medium | Make bypass shameful, track and display it |
| Low trial conversion | Medium | High | Optimize paywall, add urgency |
| Copycat apps | High | Low | Move fast, build community moat |
| Content licensing issues | Low | Medium | Use public domain Bible APIs |

---

## Technical Requirements Summary

- **Platform:** iOS (primary), Android (secondary)
- **Framework:** React Native or Flutter
- **Subscription:** RevenueCat
- **Bible API:** bible-api.com (free) or API.Bible
- **Analytics:** Mixpanel or Amplitude (free tier)
- **Backend:** None for MVP (all local storage)
- **Push notifications:** Firebase

---

## Appendix: Competitor Pricing Reference

| App | Monthly | Annual | Model |
|-----|---------|--------|-------|
| Opal | $9.99 | $49.99 | Hard paywall |
| BePresent | $7.99 | $39.99 | Hard paywall |
| one sec | $4.99 | $29.99 | Soft paywall |
| Freedom | $8.99 | $39.99 | Hard paywall |

PrayerLock pricing aligns with market leaders.
