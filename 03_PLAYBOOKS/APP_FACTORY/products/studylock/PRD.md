# StudyLock - Product Requirements Document

**App Name:** StudyLock
**Niche:** Students (High school, college, grad school)
**Method:** AFM012 - Screen Time Blocker Variant
**Monetization:** Hard Paywall - $6.99/mo or $34.99/yr

---

## Overview

StudyLock blocks distracting apps until the user completes a study session. Pomodoro-style timer enforces focus. No study time, no scrolling.

Core insight: Students know they should study more. They also know they scroll too much. Tie the two together.

---

## Problem Statement

Students want better grades but:
1. Phone notifications interrupt study sessions
2. Social media scroll replaces homework time
3. Pomodoro timers lack enforcement (easy to ignore)
4. No accountability for study habits
5. Procrastination cycle: plan to study, scroll instead, feel guilty, repeat

---

## Solution

Block selected apps until user completes a Pomodoro study session:
- Set session length (25 min default, customizable 5-60 min)
- Apps locked until timer completes
- Built-in break timer (5 min default)
- Streak tracking gamifies consistency
- Daily/weekly study time stats show progress

---

## User Stories (MVP - Single Context Window Implementable)

### US001: App Blocking Setup
**As a** student
**I want to** select which apps get blocked
**So that** only distracting apps are locked during study time

**Acceptance Criteria:**
- Display list of installed apps
- Allow multi-select for blocking
- Persist selection to local storage
- Common defaults pre-selected (social media, games, YouTube)

**Implementation Notes:**
- Use device accessibility API
- Store config in AsyncStorage
- Single screen, checkbox list UI
- Pre-select: TikTok, Instagram, Twitter, YouTube, Snapchat, Discord

---

### US002: Pomodoro Timer
**As a** student
**I want to** set a study timer duration
**So that** I study for a focused period before apps unlock

**Acceptance Criteria:**
- Default: 25 min work, 5 min break
- Customizable: 5-60 min work, 1-15 min break
- Timer displays countdown (large, prominent)
- Audio/haptic notification at completion
- Cannot be bypassed (no skip button)
- Break timer optional but encouraged

**Implementation Notes:**
- Full-screen lock during active session
- Prevent app switching during timer
- Background timer continues if user minimizes
- Session ends = apps unlock for break duration

---

### US003: Study Session Flow
**As a** student
**I want to** start a study session easily
**So that** I can get into focus mode quickly

**Acceptance Criteria:**
- One-tap "Start Session" button
- Pre-session: show blocked apps reminder
- During session: countdown, motivational quote
- End of session: celebration, break prompt
- Break ends: prompt for another session

**Implementation Notes:**
- State machine: idle, studying, break, complete
- Track completed sessions per day
- Log session data (duration, timestamp)

---

### US004: Streak Tracking
**As a** student
**I want to** see my study streak
**So that** I stay motivated to study daily

**Acceptance Criteria:**
- Display current streak (consecutive days with at least 1 session)
- Show longest streak achieved
- Calendar view of completed days
- Streak break warning notification at 8pm

**Implementation Notes:**
- Simple counter in local storage
- Day counts if at least 25 min studied
- Calendar component for history view
- Push notification for streak reminders

---

### US005: Study Stats
**As a** student
**I want to** see my study time statistics
**So that** I can track my progress

**Acceptance Criteria:**
- Today's total study time
- This week's total study time
- Daily average for the week
- Sessions completed today
- Total lifetime study hours

**Implementation Notes:**
- Store each session with timestamp and duration
- Calculate aggregates on-the-fly
- Charts for visual representation (optional MVP+)

---

### US006: Hard Paywall
**As a** new user
**I want to** try the app before paying
**So that** I know it works for me

**Acceptance Criteria:**
- 7-day free trial with full functionality
- Paywall screen shows pricing clearly
- Features locked after trial without subscription
- Restore purchases option
- Student discount messaging (psychological, not actual discount)

**Implementation Notes:**
- RevenueCat for subscription management
- Paywall appears on app launch post-trial
- Track trial start date in local storage

---

### US007: Emergency Unlock
**As a** student
**I want** an emergency unlock option
**So that** I can access my phone in genuine emergencies

**Acceptance Criteria:**
- Hidden in settings (not prominent)
- Requires typing "I am quitting my study session" to unlock
- Logs the bypass (shown in history)
- Resets today's streak progress

**Implementation Notes:**
- Intentionally friction-heavy
- Text input validation (exact match)
- Logged to discourage overuse

---

## Future Features (Post-MVP)

- **Focus music:** Lo-fi beats during study sessions
- **Study groups:** Share streaks with classmates
- **Subject tracking:** Tag sessions by subject
- **Goal setting:** Weekly study hour targets
- **GPA correlation:** Track grades vs study time (self-reported)
- **Parent dashboard:** Share progress with parents
- **Teacher integration:** Class-wide study challenges
- **Widget:** Lock screen timer widget
- **Apple Watch:** Companion app for timer

---

## MVP Feature Set

| Feature | Priority | Effort | Included in MVP |
|---------|----------|--------|-----------------|
| App blocking | P0 | Medium | Yes |
| Pomodoro timer | P0 | Medium | Yes |
| Study session flow | P0 | Low | Yes |
| Streak tracking | P1 | Low | Yes |
| Study stats | P1 | Low | Yes |
| Hard paywall | P0 | Low | Yes |
| Emergency unlock | P1 | Low | Yes |
| Focus music | P2 | Medium | No |
| Study groups | P3 | High | No |
| Subject tracking | P2 | Low | No |

---

## Monetization Structure

### Pricing
- **Monthly:** $6.99/mo
- **Annual:** $34.99/yr (save 58%)
- **Lifetime:** $69.99 (optional, test later)

### Why Hard Paywall
Reference: Opal ($600k MRR), BePresent ($300k MRR) both use hard paywall. Screen blockers convert well with paywalls because:
1. Clear value proposition (block = result)
2. Low refund rate (users see it working)
3. No free tier dilutes urgency

### Why Lower Price Than PrayerLock
- Student market is price-sensitive
- Parents often pay (lower friction)
- Competing with free Pomodoro apps
- Volume play: more users, lower price

### Trial Strategy
- 7-day free trial (longer for students to see value)
- Full functionality during trial
- Paywall after trial expiration
- Target: trial starts during midterms/finals for max urgency

---

## Success Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| Trial to Paid | >10% | RevenueCat dashboard |
| Day 7 Retention | >35% | Analytics |
| Average Streak | >5 days | In-app tracking |
| Weekly Study Time | >5 hours | In-app stats |
| Monthly Churn | <12% | RevenueCat |
| App Store Rating | >4.3 | Store reviews |

---

## Launch Checklist

### Pre-Launch
- [ ] Core features complete and tested
- [ ] RevenueCat integration working
- [ ] App Store screenshots designed (student-focused)
- [ ] App Store description written (SEO: study app, focus app, student productivity)
- [ ] Privacy policy created
- [ ] Terms of service created
- [ ] TestFlight beta with 20+ students
- [ ] Bug fixes from beta feedback

### Launch
- [ ] Submit to App Store
- [ ] Submit to Google Play
- [ ] Create TikTok account (@studylock)
- [ ] Record 5 launch TikToks (study tips genre)
- [ ] Post in student Facebook groups, Reddit (r/college, r/GetStudying)
- [ ] Reach out to study influencers (studytok, studygram)
- [ ] Set up basic landing page

### Post-Launch (Week 1-4)
- [ ] Monitor reviews, respond to all
- [ ] Post 3 TikToks per day
- [ ] Collect study improvement testimonials
- [ ] A/B test paywall copy
- [ ] Time marketing around midterms/finals
- [ ] Reach $1k MRR milestone

---

## Risks and Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Apple rejects accessibility usage | Medium | High | Follow Apple guidelines exactly, appeal if needed |
| Students find bypass workarounds | Medium | Medium | Make bypass shameful, track and display it |
| Low trial conversion | Medium | High | Optimize paywall, add urgency (exam season) |
| Competing with free Pomodoro apps | High | Medium | Blocking is the differentiator, not timer |
| Seasonal demand (school year only) | High | Medium | Target summer school, test prep, lifelong learners |

---

## Technical Requirements Summary

- **Platform:** iOS (primary), Android (secondary)
- **Framework:** React Native
- **State Management:** Zustand
- **Subscription:** RevenueCat
- **Analytics:** Mixpanel (free tier)
- **Backend:** None for MVP (all local storage)
- **Push notifications:** Firebase

---

## Guilt-Driven Marketing Angles

Target students' guilt about:
1. Not studying enough
2. Scrolling during class
3. Bad grades
4. Disappointing parents
5. Falling behind classmates
6. Wasting tuition money

**Hook Examples:**
- "POV: You planned to study but opened TikTok instead"
- "That 5 minute break that turned into 3 hours"
- "Warning: Your GPA is watching you scroll"
- "The app that made me go from C's to A's"
- "My screen time went from 8 hours to 2 hours"

---

## Appendix: Pomodoro Time Presets

| Preset | Work | Break | Total Cycle | Sessions/Hour |
|--------|------|-------|-------------|---------------|
| Quick Focus | 15 min | 3 min | 18 min | 3+ |
| Classic | 25 min | 5 min | 30 min | 2 |
| Deep Work | 45 min | 10 min | 55 min | 1 |
| Marathon | 60 min | 15 min | 75 min | <1 |

Default recommendation: Classic (25/5) - proven effective.

---

## Appendix: Competitor Analysis

| App | Monthly | Annual | Model | Weakness |
|-----|---------|--------|-------|----------|
| Forest | Free/$3.99 | - | One-time | No app blocking |
| Focus Plant | Free | $9.99/yr | Soft paywall | Gamey, not serious |
| Flora | Free | $11.99/yr | Soft paywall | Social features only |
| Opal | $9.99 | $49.99 | Hard paywall | Not student-focused |
| one sec | $4.99 | $29.99 | Soft paywall | Delays, not blocks |

**StudyLock Differentiator:** Hard blocking (not just delay) + Pomodoro structure + student-specific messaging.
