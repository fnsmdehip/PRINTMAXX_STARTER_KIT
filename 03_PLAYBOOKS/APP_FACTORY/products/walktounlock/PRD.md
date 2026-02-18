# WalkToUnlock - Product Requirements Document

**App Name:** WalkToUnlock
**Niche:** Fitness (Walking/Steps focus)
**Method:** AFM012 - Screen Time Blocker Variant
**Monetization:** Hard Paywall - $7.99/mo or $39.99/yr

---

## Overview

WalkToUnlock blocks distracting apps until the user hits their daily step goal. No steps, no scrolling.

Core insight: People know they should walk more. They also know they scroll too much. Tie the two together.

---

## Problem Statement

People want to be more active but:
1. Sedentary jobs make walking an afterthought
2. Phone addiction keeps them seated
3. Step goals feel arbitrary with no real consequence
4. Fitness apps track but don't enforce
5. Health data exists but doesn't change behavior

---

## Solution

Block selected apps until HealthKit/Google Fit confirms step goal reached:
- Set daily step target (3,000-15,000)
- Apps locked until steps verified
- Progress bar shows remaining steps
- Unlock happens automatically when goal hit

---

## User Stories (MVP - Single Context Window Implementable)

### US001: Health Data Permission
**As a** user
**I want to** connect my step data
**So that** the app can track my walking progress

**Acceptance Criteria:**
- Request HealthKit (iOS) / Google Fit (Android) permission
- Read step count data
- Display current step count on home screen
- Handle permission denied gracefully

**Implementation Notes:**
- Use react-native-health or expo-health
- Background refresh every 5 minutes
- Cache last known step count

---

### US002: Step Goal Setting
**As a** user
**I want to** set my daily step goal
**So that** I have a clear target to unlock my apps

**Acceptance Criteria:**
- Slider from 1,000 to 20,000 steps
- Preset options (3k, 5k, 8k, 10k)
- Show estimated walking time/distance
- Persist goal in settings

**Implementation Notes:**
- Sensible default: 5,000 steps
- Show "beginner/moderate/advanced" labels
- Calculate: ~2,000 steps per mile, ~15 min per 1,000 steps

---

### US003: App Blocking Setup
**As a** user
**I want to** select which apps get blocked
**So that** only distracting apps are locked

**Acceptance Criteria:**
- Display list of installed apps
- Allow multi-select for blocking
- Common defaults pre-selected (social media, games)
- Exclude essential apps (Phone, Messages, Maps)

**Implementation Notes:**
- Use same blocking approach as PrayerLock
- Platform-specific APIs
- Store config in local storage

---

### US004: Progress Display
**As a** user
**I want to** see how close I am to unlocking
**So that** I'm motivated to keep walking

**Acceptance Criteria:**
- Large progress ring/bar on home screen
- Current steps vs goal (e.g., "3,247 / 5,000")
- Remaining steps prominently displayed
- Estimated time to reach goal

**Implementation Notes:**
- Update every 5 minutes in background
- Pull-to-refresh for manual update
- Satisfying animation when goal reached

---

### US005: Automatic Unlock
**As a** user
**I want** apps to unlock automatically when I hit my goal
**So that** I don't have to manually check

**Acceptance Criteria:**
- Background check every 5 minutes
- Push notification when unlocked
- Celebratory animation on goal completion
- Apps become accessible immediately

**Implementation Notes:**
- Background fetch API
- Local notification on unlock
- Confetti/celebration UI
- Log completion timestamp

---

### US006: Hard Paywall
**As a** new user
**I want to** try the app before paying
**So that** I know it works for me

**Acceptance Criteria:**
- 3-day free trial with full functionality
- Paywall screen shows pricing clearly
- Features locked after trial
- Restore purchases option

**Implementation Notes:**
- RevenueCat integration
- Track trial start date
- Paywall appears post-trial

---

### US007: Streak Tracking
**As a** user
**I want to** see my step goal streak
**So that** I stay motivated

**Acceptance Criteria:**
- Display current streak
- Show longest streak
- Calendar view of completed days
- Streak break warning notification

**Implementation Notes:**
- Simple counter logic
- 8pm warning if goal not hit
- Streak resets at midnight

---

### US008: Emergency Unlock
**As a** user
**I want** emergency access option
**So that** I can use my phone in genuine emergencies

**Acceptance Criteria:**
- Hidden in settings
- Requires typing confirmation phrase
- Logs the bypass
- Resets streak

**Implementation Notes:**
- High friction by design
- "I am skipping my walk" confirmation
- Displayed in history as "skipped"

---

## Future Features (Post-MVP)

- **Walk challenges:** Compete with friends
- **Walking routes:** Suggest nearby walking paths
- **Weather integration:** Adjust goals for bad weather
- **Treadmill mode:** Manual step entry for indoor walking
- **Walking podcast:** Partner content during walks
- **Apple Watch:** Companion app with progress ring
- **Widget:** Lock screen step progress
- **Gamification:** Badges, achievements, levels

---

## MVP Feature Set

| Feature | Priority | Effort | Included in MVP |
|---------|----------|--------|-----------------|
| Health data integration | P0 | Medium | Yes |
| Step goal setting | P0 | Low | Yes |
| App blocking | P0 | Medium | Yes |
| Progress display | P0 | Low | Yes |
| Auto-unlock | P0 | Medium | Yes |
| Hard paywall | P0 | Low | Yes |
| Streak tracking | P1 | Low | Yes |
| Emergency unlock | P1 | Low | Yes |
| Walk challenges | P2 | High | No |
| Weather integration | P3 | Low | No |

---

## Monetization Structure

### Pricing
- **Monthly:** $7.99/mo
- **Annual:** $39.99/yr (save 58%)
- **Lifetime:** $79.99 (optional, test later)

### Why Hard Paywall
Same rationale as PrayerLock: screen blockers convert well with hard paywalls. Clear value proposition, low refund rate.

### Why Slightly Lower Price Than PrayerLock
- Fitness market more price-sensitive
- Competing with free fitness apps
- Step tracking is commoditized
- Differentiation is in blocking, not content

### Trial Strategy
- 3-day free trial
- Full functionality
- Paywall after expiration

---

## Success Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| Trial to Paid | >12% | RevenueCat |
| Day 7 Retention | >35% | Analytics |
| Average Streak | >5 days | In-app |
| Steps Increase | >20% vs baseline | Health data |
| Monthly Churn | <10% | RevenueCat |
| App Store Rating | >4.3 | Reviews |

---

## Launch Checklist

### Pre-Launch
- [ ] Core features complete
- [ ] HealthKit/Google Fit tested on real devices
- [ ] RevenueCat integration working
- [ ] App Store screenshots
- [ ] Privacy policy (health data specific)
- [ ] TestFlight beta with 20+ users
- [ ] Step tracking accuracy validated

### Launch
- [ ] Submit to App Store
- [ ] Submit to Google Play
- [ ] Create TikTok account (@walktounlock)
- [ ] Record 5 launch TikToks
- [ ] Post in fitness Facebook groups
- [ ] Reach out to fitness influencers

### Post-Launch (Week 1-4)
- [ ] Monitor reviews
- [ ] Post 3 TikToks per day
- [ ] Collect step increase testimonials
- [ ] A/B test paywall
- [ ] Reach $500 MRR milestone

---

## Risks and Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Health permission denied | Medium | High | Clear permission explanation, fallback manual entry |
| Inaccurate step data | Medium | Medium | Use official APIs, don't trust third-party |
| Users game with fake steps | Low | Low | Accept some gaming, focus on habit change |
| Weather prevents walking | Medium | Medium | Add weather-adjusted goals post-MVP |
| Competing with free fitness apps | High | Medium | Blocking is the differentiator, not tracking |

---

## Technical Requirements Summary

- **Platform:** iOS (primary), Android (secondary)
- **Framework:** React Native
- **Health Data:** HealthKit (iOS), Google Fit (Android)
- **Subscription:** RevenueCat
- **Analytics:** Mixpanel
- **Backend:** None for MVP
- **Push notifications:** Firebase

---

## Appendix: Step Goal Benchmarks

| Level | Steps | Time | Distance |
|-------|-------|------|----------|
| Sedentary | <3,000 | - | - |
| Light | 3,000 | ~30 min | ~1.5 mi |
| Moderate | 5,000 | ~50 min | ~2.5 mi |
| Active | 8,000 | ~80 min | ~4 mi |
| Very Active | 10,000 | ~100 min | ~5 mi |
| Athletic | 15,000+ | ~150 min | ~7.5 mi |

Default recommendation: 5,000 steps (achievable for most).
