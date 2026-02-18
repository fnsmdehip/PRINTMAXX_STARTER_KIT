# DailyDevotion - Product Requirements Document

**App Name:** DailyDevotion
**Niche:** Faith (Christian focus)
**Method:** Fork of Loop Habit Tracker (MIT license)
**Monetization:** Freemium with Premium ($4.99/mo or $29.99/yr)
**Mascot:** Dove

---

## Overview

DailyDevotion is a faith-focused habit tracking app that helps Christians build spiritual disciplines. Forked from the open-source Loop Habit Tracker, it adds faith-specific templates, daily Bible verses, and a dove mascot for encouragement.

Core insight: Christians want to build spiritual habits but generic habit trackers feel secular. A faith-branded app with pre-built templates removes friction.

---

## Problem Statement

Christians struggle to maintain consistent spiritual disciplines because:

1. Generic habit apps lack faith context
2. No pre-built templates for common practices (prayer, scripture, fasting)
3. Secular motivation messages miss the mark
4. No integration with daily scripture
5. Church apps focus on content, not habit building

---

## Solution

A habit tracker designed for spiritual growth:

- Pre-built faith habit templates (10+ disciplines)
- Daily Bible verse integration
- Encouraging dove mascot with faith-based messages
- Calming spiritual UI (purple/gold palette)
- Streak tracking reframed as "faithfulness"
- Community features for accountability partners

---

## Target Audience

### Primary: Committed Christians (25-45)
- Regular church attendance
- Want to deepen spiritual life
- Already use productivity apps
- Value daily devotional time
- Willing to pay for faith tools

### Secondary: New Believers
- Recently converted
- Need structure for spiritual habits
- Benefit from templates and guidance
- High retention if habits stick

### Tertiary: Church Leaders
- Looking for tools to recommend
- Could drive word-of-mouth
- Potential for church licensing deals

---

## User Stories (MVP)

### US001: Faith Habit Templates
**As a** Christian user
**I want to** choose from pre-built spiritual discipline templates
**So that** I don't have to figure out what habits to track

**Acceptance Criteria:**
- Display 10+ faith-specific templates
- Templates include: Morning Prayer, Scripture Reading, Gratitude Journal, Church Attendance, Evening Prayer, Meditation, Fasting, Tithe/Giving, Sabbath Rest, Scripture Memorization
- One-tap to add template as habit
- Templates have appropriate icons, colors, frequencies

**Implementation Notes:**
- Leverage existing habit creation from Loop
- Add template picker screen before custom habit flow
- Store templates as constants

---

### US002: Daily Bible Verse
**As a** user
**I want to** see an encouraging Bible verse each day
**So that** I start my habit tracking with scripture

**Acceptance Criteria:**
- Display verse card on main screen
- New verse each day
- Show reference and translation
- Share button for social/messaging
- Cache verse for offline access

**Implementation Notes:**
- Integrate bible-api.com (free, public domain)
- Cache in SharedPreferences
- Fallback to local verse database if offline

---

### US003: Dove Mascot Messages
**As a** user
**I want to** receive encouraging faith-based messages
**So that** I feel supported in my spiritual journey

**Acceptance Criteria:**
- Dove appears on main screen
- Different messages for: greeting, streak celebration, encouragement after miss, habit completion
- Messages reference scripture or faith themes
- Animations for key moments (streak milestones)

**Implementation Notes:**
- Use Lottie for dove animations
- Message pools for variety
- Context-aware message selection

---

### US004: Faithfulness Streak Tracking
**As a** user
**I want to** see my streak reframed as "faithfulness"
**So that** the language resonates with my faith

**Acceptance Criteria:**
- "Faithfulness streak" instead of generic "streak"
- Milestone celebrations at 7, 30, 100, 365 days
- Dove celebration animation at milestones
- "Growth rate" instead of "completion rate"

**Implementation Notes:**
- Primarily string/UI changes
- Leverage existing streak logic from Loop
- Add celebration overlays

---

### US005: Spiritual Discipline Categories
**As a** user
**I want to** organize habits by spiritual discipline type
**So that** I can see my growth in different areas

**Acceptance Criteria:**
- Categories: Prayer, Scripture, Worship, Service, Rest, Generosity
- Filter habits by category
- Stats per category
- Color coding by category

**Implementation Notes:**
- Add category field to Habit model
- Category picker in habit creation
- Filter UI in main list

---

### US006: Premium Features
**As a** user
**I want** access to advanced features
**So that** I can deepen my tracking practice

**Free Tier:**
- 5 habit limit
- Basic templates (3)
- Daily verse
- Basic streak tracking
- Standard notifications

**Premium Tier ($4.99/mo or $29.99/yr):**
- Unlimited habits
- All templates (10+)
- Verse of day widget
- Advanced statistics
- Multiple translations for verses
- Export/backup data
- No ads
- Priority support

**Implementation Notes:**
- RevenueCat for subscription
- Feature flags for gating
- Soft paywall (can use free tier indefinitely)

---

### US007: Prayer Time Reminders
**As a** user
**I want** contextual reminders with verse snippets
**So that** notifications feel meaningful

**Acceptance Criteria:**
- Include short scripture in notifications
- Different messages for different habits
- Respect quiet hours
- "Later" snooze option

**Implementation Notes:**
- Extend existing notification system
- Add verse fetching to reminder builder
- Optional toggle per habit

---

### US008: Widget with Verse
**As a** user
**I want** a home screen widget
**So that** I can see my verse and quick-complete habits

**Acceptance Criteria:**
- Display today's verse (abbreviated)
- Show top 3 habits with checkboxes
- Tap verse to open full verse
- Streak counter visible
- Multiple size options

**Implementation Notes:**
- Extend existing Loop widgets
- Add verse integration
- AppWidgetProvider update

---

## Future Features (Post-MVP)

### V1.1 - Community
- Accountability partner pairing
- Share progress with partner
- Group challenges

### V1.2 - Content Integration
- Guided devotional plans
- Audio prayers
- Worship music integration

### V1.3 - Church Features
- Church group challenges
- Pastor dashboard
- Bulk licensing

### V2.0 - Multi-Faith
- Muslim prayer time support
- Jewish prayer traditions
- Generic spiritual tracker mode

---

## MVP Feature Set

| Feature | Priority | Effort | In MVP |
|---------|----------|--------|--------|
| Rebrand (name, colors, icon) | P0 | Low | Yes |
| Faith templates (10) | P0 | Medium | Yes |
| Daily verse card | P0 | Medium | Yes |
| Dove mascot (static) | P1 | Low | Yes |
| Faithfulness reframing | P1 | Low | Yes |
| Premium paywall | P0 | Medium | Yes |
| Verse in notifications | P2 | Low | Yes |
| Dove animations | P2 | Medium | No (v1.1) |
| Widget with verse | P2 | Medium | No (v1.1) |
| Accountability partners | P3 | High | No |
| Audio content | P3 | High | No |

---

## Monetization Strategy

### Pricing (Soft Paywall)
- **Free:** Core features, 5 habit limit
- **Monthly:** $4.99/mo
- **Annual:** $29.99/yr (50% savings)
- **Lifetime:** $79.99 (optional, test later)

### Why Soft Paywall
Unlike PrayerLock (screen blocker = high urgency), habit trackers have:
- Lower immediate pain point
- Longer evaluation period needed
- Strong word-of-mouth when free tier works
- Premium converts through value demonstration

### Revenue Projections (Conservative)
| Month | Downloads | Free | Paid | MRR |
|-------|-----------|------|------|-----|
| 1 | 500 | 450 | 25 | $125 |
| 3 | 2,000 | 1,700 | 150 | $750 |
| 6 | 5,000 | 4,000 | 500 | $2,500 |
| 12 | 15,000 | 12,000 | 1,500 | $7,500 |

Based on 5% conversion, 8% monthly churn.

---

## Competitive Analysis

### Direct Competitors

| App | Price | Faith Focus | Strengths | Weaknesses |
|-----|-------|-------------|-----------|------------|
| Hallow | $8.99/mo | Catholic | Rich content, audio | Expensive, Catholic-specific |
| Glorify | $11.99/mo | Christian | Beautiful design | Focuses on content not habits |
| Echo Prayer | Free/$3.99 | Christian | Simple prayer list | No habit tracking |
| First 15 | Free | Christian | Devotional content | Not a habit tracker |

### Indirect Competitors

| App | Price | Habit Focus | Faith Gap |
|-----|-------|-------------|-----------|
| Loop (our base) | Free | General | No faith features |
| Streaks | $4.99 | General | Secular |
| Habitica | Freemium | Gamified | RPG theme |
| Strides | Freemium | Goals | Business-focused |

### Our Differentiation
1. **Fork advantage:** Battle-tested codebase, fast to market
2. **Templates:** Lower friction than competitors
3. **Price:** Cheaper than Hallow/Glorify
4. **Focus:** Habit building, not content consumption
5. **Mascot:** Memorable, shareable, builds affinity

---

## Technical Specifications

### Platform
- **Primary:** Android (from Loop fork)
- **Secondary:** iOS (React Native rebuild or Flutter)

### Stack (Android)
- **Language:** Kotlin
- **Architecture:** Clean Architecture + MVVM
- **Database:** Room (SQLite)
- **DI:** Dagger/Hilt
- **Async:** Coroutines + Flow
- **UI:** Material Design 3

### APIs
- **Bible:** bible-api.com (free) or api.scripture.api.bible
- **Subscriptions:** RevenueCat
- **Analytics:** Mixpanel or Amplitude
- **Crash:** Firebase Crashlytics
- **Push:** Firebase Cloud Messaging

### Data Model Extensions

```kotlin
// Extend existing Habit model
data class Habit(
    val id: Long,
    val name: String,
    val description: String,
    val frequency: Frequency,
    val targetValue: Int,
    val targetType: HabitType,
    val color: Int,
    val icon: Int,
    val reminderTime: String?,
    val createdAt: Long,
    // NEW FIELDS
    val category: DisciplineCategory,
    val templateId: String?,
    val verseReference: String?  // Optional verse for this habit
)

enum class DisciplineCategory {
    PRAYER,
    SCRIPTURE,
    WORSHIP,
    SERVICE,
    REST,
    GENEROSITY,
    CUSTOM
}

// New verse model
data class DailyVerse(
    val date: String,
    val reference: String,
    val text: String,
    val translation: String,
    val cachedAt: Long
)
```

---

## Success Metrics

| Metric | Target | Tool |
|--------|--------|------|
| Day 1 Retention | > 50% | Analytics |
| Day 7 Retention | > 30% | Analytics |
| Day 30 Retention | > 15% | Analytics |
| Trial to Paid | > 8% | RevenueCat |
| Monthly Churn | < 10% | RevenueCat |
| App Store Rating | > 4.5 | Store |
| Avg Habits/User | > 3 | Analytics |
| Avg Streak | > 5 days | Analytics |

---

## Launch Plan

### Pre-Launch (Week 1-2)
- [ ] Complete MVP features
- [ ] Create app store assets
- [ ] Write store description
- [ ] Set up RevenueCat
- [ ] Beta test with 20 faith users
- [ ] Fix critical bugs
- [ ] Prepare privacy policy

### Launch (Week 3)
- [ ] Submit to Google Play
- [ ] Create TikTok/Instagram accounts
- [ ] Record 5 launch videos
- [ ] Post in Christian Facebook groups
- [ ] Reach out to faith influencers
- [ ] Launch landing page

### Post-Launch (Week 4-8)
- [ ] Respond to all reviews
- [ ] Post 3 videos per day
- [ ] Collect testimonials
- [ ] A/B test paywall
- [ ] Add requested features
- [ ] Plan iOS version

---

## Content Strategy

### Social Media Handles
- @dailydevotion_app (Instagram)
- @dailydevotionapp (TikTok)
- @dailydevotionHQ (Twitter/X)

### Content Pillars
1. **Habit tips:** "3 ways to never miss morning prayer"
2. **Verses:** Share daily verses with branded graphics
3. **Testimonials:** User transformation stories
4. **Behind the scenes:** App development journey
5. **Faith humor:** Relatable Christian memes

### Launch Hooks
- "I built an app because I kept forgetting to pray"
- "This simple app helped me read the Bible every day for 30 days"
- "Why I quit [secular app] for a faith-based habit tracker"

---

## Risks and Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Low differentiation from Loop | Medium | High | Strong branding, unique features |
| Bible API reliability | Low | Medium | Local fallback database |
| Crowded faith app market | High | Medium | Focus on habits, not content |
| iOS version delays | High | Medium | Launch Android first, validate |
| Low conversion rate | Medium | High | Test pricing, add more premium value |

---

## Compliance & Safety

### Content Guidelines
- Use public domain translations (KJV, WEB) to avoid licensing
- No prosperity gospel or controversial theology
- Inclusive language ("Christians" not denomination-specific)
- Clear attribution for all scripture

### Privacy Policy Requirements
- Data collected (habits, verse preferences)
- No selling of user data
- Offline-first data storage
- Export/delete user data option

### App Store Compliance
- Accurate description of subscription terms
- Clear trial length and pricing
- Restore purchases functionality
- No misleading health claims

---

## Appendix: Complete Template List

| Template | Category | Frequency | Type | Default Target |
|----------|----------|-----------|------|----------------|
| Morning Prayer | Prayer | Daily | Boolean | - |
| Evening Prayer | Prayer | Daily | Boolean | - |
| Scripture Reading | Scripture | Daily | Numeric | 15 min |
| Scripture Memorization | Scripture | Weekly | Numeric | 1 verse |
| Gratitude Journal | Prayer | Daily | Numeric | 3 items |
| Christian Meditation | Prayer | Daily | Numeric | 10 min |
| Church Attendance | Worship | Weekly | Boolean | - |
| Sabbath Rest | Rest | Weekly | Boolean | - |
| Fasting | Rest | Custom | Boolean | - |
| Tithe/Giving | Generosity | Weekly | Boolean | - |

---

## Appendix: Store Listing Draft

### App Name
DailyDevotion: Faith Habit Tracker

### Short Description (80 chars)
Build spiritual disciplines with prayer, scripture & habit tracking

### Full Description
Build lasting spiritual habits with DailyDevotion, the habit tracker designed for your faith journey.

Track your prayer time, scripture reading, gratitude practice, and more with beautiful, faith-focused templates. Get daily Bible verses to inspire your walk. Celebrate your faithfulness streaks with our encouraging dove mascot.

FEATURES:
- 10 pre-built spiritual discipline templates
- Daily Bible verse on your home screen
- Track prayer, scripture, fasting, and more
- Faithfulness streak tracking
- Calming spiritual design
- Widgets for quick access
- Export and backup your data

Whether you want to pray more, read scripture daily, or build any spiritual discipline, DailyDevotion gives you the tools to grow in faith, one habit at a time.

FREE FEATURES:
- Up to 5 habits
- 3 basic templates
- Daily verse
- Streak tracking

PREMIUM ($4.99/mo or $29.99/yr):
- Unlimited habits
- All templates
- Advanced statistics
- Multiple verse translations
- Data export
- No ads

Built on the trusted Loop Habit Tracker, DailyDevotion combines proven habit tracking with faith-focused features.

---

Created: 2026-01-21
Status: PLANNING
