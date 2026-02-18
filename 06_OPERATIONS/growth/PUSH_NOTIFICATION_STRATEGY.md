# Push Notification Strategy for PRINTMAXX Apps

**Last Updated:** 2026-01-23
**Applies to:** PrayerLock, WalkToUnlock, StudyLock

---

## 1. Timing Optimization

### Best Times by App Type

| App | Primary Window | Secondary Window | Why |
|-----|----------------|------------------|-----|
| PrayerLock | 6:00-7:00 AM | 8:30-9:00 PM | Morning devotion, evening reflection |
| WalkToUnlock | 7:00-8:00 AM | 5:30-6:30 PM | Before work motivation, post-work movement |
| StudyLock | 3:00-4:00 PM | 7:00-8:00 PM | After school/work, evening study blocks |

### Day of Week Patterns

| Day | Engagement Level | Strategy |
|-----|------------------|----------|
| Monday | High | Fresh start messaging, goal setting |
| Tuesday-Thursday | Medium-High | Streak maintenance, progress updates |
| Friday | Medium | Weekend prep, achievement celebrations |
| Saturday | Lower | Lighter touch, lifestyle integration |
| Sunday | Variable by app | PrayerLock high, others moderate |

**PrayerLock Sunday Exception:** 7:00-8:00 AM is peak. Users expect spiritual content.

### Timezone Handling

```
Implementation:
1. Store user timezone on first app open (device settings)
2. Schedule all notifications in LOCAL time
3. Default to America/New_York if unknown
4. Re-detect timezone on app foreground (travel users)
```

**Code Example (React Native/Expo):**
```javascript
import * as Localization from 'expo-localization';

const getUserTimezone = () => {
  return Localization.timezone || 'America/New_York';
};
```

### Frequency Limits

| User Segment | Max Daily | Max Weekly | Notes |
|--------------|-----------|------------|-------|
| New users (days 1-3) | 2 | 10 | Higher touch for habit formation |
| New users (days 4-7) | 1-2 | 7 | Tapering to sustainable |
| Active users | 1 | 5-6 | Maintain engagement without fatigue |
| At-risk users | 1 | 3-4 | Quality over quantity |
| Premium users | 1-2 | 7 | More features to notify about |

**Hard Rule:** Never send more than 2 notifications in a 4-hour window.

---

## 2. Copy Formulas

### Title Patterns (Under 50 Characters)

**Formula 1: Direct Action**
```
[Verb] your [thing] [timeframe]
```
Examples:
- "Start your morning prayer" (24 chars)
- "Complete your daily steps" (25 chars)
- "Begin your study session" (24 chars)

**Formula 2: Streak Alert**
```
[Number]-day streak [status]
```
Examples:
- "7-day streak at risk" (20 chars)
- "14-day streak achieved" (22 chars)
- "Your 30-day streak awaits" (25 chars)

**Formula 3: Personal Progress**
```
You're [X]% to [goal]
```
Examples:
- "You're 80% to your goal" (23 chars)
- "You're 3 steps from 10K" (23 chars)
- "You're 1 session from level 5" (29 chars)

**Formula 4: Question Hook**
```
Ready for [activity]?
```
Examples:
- "Ready for morning prayer?" (25 chars)
- "Ready to hit 10K steps?" (23 chars)
- "Ready for a quick quiz?" (23 chars)

**Formula 5: Time-Based Urgency**
```
[Timeframe]: [action needed]
```
Examples:
- "2 hours left: complete your goal" (32 chars)
- "Tonight: finish your streak" (27 chars)
- "This morning: prayer time" (25 chars)

### Body Patterns (Under 100 Characters)

**Formula 1: Benefit + Action**
```
[Benefit statement]. Tap to [action].
```
Examples:
- "Start your day with peace. Tap to begin your morning devotion." (63 chars)
- "You're almost there. Tap to log your remaining 1,200 steps." (59 chars)
- "Ace your next exam. Tap to start a 25-minute focus session." (59 chars)

**Formula 2: Social Proof**
```
[Number] users [action] today. Join them.
```
Examples:
- "12,000 users prayed this morning. Join them." (44 chars)
- "8,500 users hit their step goal today. You're next." (51 chars)
- "3,200 students completed a session. Start yours." (48 chars)

**Formula 3: Streak Consequence**
```
[Streak status]. [Time remaining] to keep it alive.
```
Examples:
- "Your 21-day prayer streak is at risk. 4 hours to save it." (57 chars)
- "Don't lose your 14-day streak. 2 hours left today." (50 chars)
- "45-day study streak on the line. One session keeps it." (54 chars)

**Formula 4: Achievement Unlock**
```
[Achievement name] unlocked! Tap to see your [reward].
```
Examples:
- "Early Bird badge unlocked! Tap to see your new badge." (53 chars)
- "10K Club achieved! Tap to share your milestone." (47 chars)
- "Quiz Master unlocked! Tap to claim your reward." (47 chars)

**Formula 5: Personalized Insight**
```
[Name], [personal stat]. [Encouraging action].
```
Examples:
- "Sarah, you've prayed 47 days straight. Keep the faith." (54 chars)
- "Mike, 8,234 steps so far. 1,766 more unlocks your phone." (56 chars)
- "Alex, 3 hours studied this week. One more session hits your goal." (65 chars)

### Emoji Usage Guidelines

**Allowed Emojis by App:**

| App | Allowed | Never Use |
|-----|---------|-----------|
| PrayerLock | pray hands, dove, sun, heart, star, book | fire, money, party |
| WalkToUnlock | footprints, trophy, fire, muscle, check | pray, book, money |
| StudyLock | book, brain, lightbulb, star, check, trophy | pray, money, party |

**Emoji Rules:**
1. Max 1 emoji per notification
2. Place at start OR end, never middle
3. Test emoji vs no-emoji (some segments prefer clean)
4. iOS renders differently than Android (test both)

**Examples:**
```
Good: "Your 7-day streak is at risk"
Good: "Your 7-day streak is at risk" (with fire emoji at end)
Bad:  "Your (fire) 7-day streak (fire) is at risk (fire)"
```

### Personalization Tokens

| Token | Description | Fallback |
|-------|-------------|----------|
| `{{first_name}}` | User's first name | "there" |
| `{{streak_count}}` | Current streak number | "your" |
| `{{steps_remaining}}` | Steps left today | "your goal" |
| `{{study_minutes}}` | Minutes studied today | "your session" |
| `{{days_since_last}}` | Days since last session | (omit if 0) |
| `{{level}}` | User's current level | "your level" |

**Token Validation Rule:** Never send notification if required token is missing. Use fallback copy instead.

---

## 3. Notification Types by App

### PrayerLock Notifications

#### 3.1 Morning Prayer Reminders

**Trigger:** 6:30 AM local time (if no session logged today)

| ID | Title | Body | Deep Link |
|----|-------|------|-----------|
| PL-AM-001 | Good morning, {{first_name}} | Start your day with 5 minutes of peace. Tap to begin. | /prayer/start |
| PL-AM-002 | Your morning prayer awaits | 12,000 users started their day in prayer. Join them. | /prayer/start |
| PL-AM-003 | Rise and pray | {{streak_count}} days strong. Keep your streak alive. | /prayer/start |
| PL-AM-004 | A new day, a new prayer | Take 3 minutes to center yourself this morning. | /prayer/guided |
| PL-AM-005 | The world is quiet. Pray now. | Your prayer space is ready. Tap to enter. | /prayer/start |

#### 3.2 Streak Maintenance Alerts

**Trigger:** 8:00 PM local time (if no session today AND streak > 3 days)

| ID | Title | Body | Deep Link |
|----|-------|------|-----------|
| PL-STR-001 | {{streak_count}}-day streak at risk | 4 hours left. One prayer keeps your streak alive. | /prayer/quick |
| PL-STR-002 | Don't break the chain | You've prayed {{streak_count}} days straight. Continue tonight? | /prayer/start |
| PL-STR-003 | Tonight: save your streak | A 2-minute prayer protects {{streak_count}} days of progress. | /prayer/quick |
| PL-STR-004 | Your streak needs you | Just 3 minutes to keep {{streak_count}} days going. | /prayer/quick |
| PL-STR-005 | {{streak_count}} days of faith | Don't let it end tonight. One prayer is all it takes. | /prayer/start |

#### 3.3 Verse of the Day

**Trigger:** 7:00 AM local time (opt-in users only)

| ID | Title | Body | Deep Link |
|----|-------|------|-----------|
| PL-VOD-001 | Today's verse is ready | Tap to read and reflect on today's scripture. | /verse/today |
| PL-VOD-002 | Your daily verse | New wisdom waiting. Tap to start your morning. | /verse/today |
| PL-VOD-003 | Scripture for today | A verse selected for you. Tap to read. | /verse/today |
| PL-VOD-004 | Morning wisdom | Today's verse speaks to patience. Tap to read. | /verse/today |
| PL-VOD-005 | God's word for today | Your daily scripture is ready. Tap to reflect. | /verse/today |

**Note:** Do not include actual verse text in notification (copyright concerns).

#### 3.4 Weekly Progress Summaries

**Trigger:** Sunday 10:00 AM local time

| ID | Title | Body | Deep Link |
|----|-------|------|-----------|
| PL-WK-001 | Your week in prayer | {{weekly_sessions}} sessions, {{weekly_minutes}} minutes with God. See your summary. | /stats/weekly |
| PL-WK-002 | Weekly reflection ready | Review your prayer journey this week. Tap to see insights. | /stats/weekly |
| PL-WK-003 | 7 days of faith complete | You prayed {{weekly_sessions}} times. See how you grew. | /stats/weekly |
| PL-WK-004 | Week {{week_number}} complete | Your prayer stats are in. Tap to review your progress. | /stats/weekly |
| PL-WK-005 | Sunday summary | This week: {{weekly_sessions}} prayers, {{streak_count}}-day streak. Keep going. | /stats/weekly |

---

### WalkToUnlock Notifications

#### 3.5 Step Goal Reminders

**Trigger:** 6:00 PM local time (if < 50% of daily goal)

| ID | Title | Body | Deep Link |
|----|-------|------|-----------|
| WU-SG-001 | {{steps_remaining}} steps to go | You're halfway there. A 15-minute walk finishes it. | /dashboard |
| WU-SG-002 | Unlock your phone tonight | {{steps_remaining}} more steps unlocks everything. Get moving. | /dashboard |
| WU-SG-003 | Evening walk time | You're at {{steps_percent}}%. A short walk completes your goal. | /dashboard |
| WU-SG-004 | Almost there | {{steps_remaining}} steps left. You've got this. | /dashboard |
| WU-SG-005 | Phone still locked? | {{steps_remaining}} more steps and you're free. Walk it out. | /dashboard |

#### 3.6 Achievement Unlocked

**Trigger:** Immediately when achievement earned

| ID | Title | Body | Deep Link |
|----|-------|------|-----------|
| WU-ACH-001 | 10K Club unlocked! | You hit 10,000 steps. Welcome to the club. | /achievements |
| WU-ACH-002 | New badge: {{badge_name}} | Your dedication paid off. Tap to see your achievement. | /achievements |
| WU-ACH-003 | Achievement unlocked | {{badge_name}} is yours. Share your milestone? | /achievements/share |
| WU-ACH-004 | You earned {{badge_name}} | Another badge in your collection. Tap to view. | /achievements |
| WU-ACH-005 | Milestone reached | {{badge_name}} unlocked. You're in the top {{percentile}}% of walkers. | /achievements |

#### 3.7 Streak Warnings

**Trigger:** 7:00 PM local time (if streak > 7 days AND < 80% of goal)

| ID | Title | Body | Deep Link |
|----|-------|------|-----------|
| WU-STW-001 | {{streak_count}}-day streak needs you | {{steps_remaining}} steps in 5 hours. You've got this. | /dashboard |
| WU-STW-002 | Protect your streak | {{streak_count}} days of walking. Don't stop tonight. | /dashboard |
| WU-STW-003 | Streak alert | {{streak_count}} days at risk. {{steps_remaining}} steps to save it. | /dashboard |
| WU-STW-004 | Don't lose {{streak_count}} days | A 20-minute walk keeps your streak alive. | /dashboard |
| WU-STW-005 | Your streak is calling | {{steps_remaining}} steps. One walk. Keep the chain going. | /dashboard |

#### 3.8 Weekly Challenge Invites

**Trigger:** Monday 8:00 AM local time

| ID | Title | Body | Deep Link |
|----|-------|------|-----------|
| WU-CH-001 | New weekly challenge | This week: 70,000 steps. Beat last week's {{last_week_steps}}? | /challenges |
| WU-CH-002 | Challenge yourself | Join 5,000 users in this week's step challenge. | /challenges |
| WU-CH-003 | Week {{week_number}} challenge | 70K steps, 7 days. Are you in? | /challenges/join |
| WU-CH-004 | Ready for a challenge? | This week's goal: 10K steps daily. Join the challenge. | /challenges |
| WU-CH-005 | Monday motivation | New challenge unlocked. Can you hit 70K this week? | /challenges |

---

### StudyLock Notifications

#### 3.9 Study Session Reminders

**Trigger:** User-set time OR 3:00 PM default (if no session today)

| ID | Title | Body | Deep Link |
|----|-------|------|-----------|
| SL-SR-001 | Time to focus | 25 minutes of distraction-free study. Tap to start. | /session/start |
| SL-SR-002 | Your study session awaits | Lock your phone. Unlock your potential. | /session/start |
| SL-SR-003 | Ready for a focus block? | {{streak_count}} days of studying. Keep the momentum. | /session/start |
| SL-SR-004 | Study time | One focused session. Zero distractions. Tap to begin. | /session/start |
| SL-SR-005 | {{first_name}}, time to study | Your brain is ready. Start a 25-minute session. | /session/start |

#### 3.10 Streak Alerts

**Trigger:** 8:00 PM local time (if no session AND streak > 5 days)

| ID | Title | Body | Deep Link |
|----|-------|------|-----------|
| SL-STR-001 | {{streak_count}}-day study streak at risk | One 15-minute session saves it. Tap to start. | /session/quick |
| SL-STR-002 | Don't break your streak | You've studied {{streak_count}} days straight. Continue? | /session/start |
| SL-STR-003 | Protect your progress | {{streak_count}} days of focus. Don't stop now. | /session/start |
| SL-STR-004 | Streak warning | 4 hours to save {{streak_count}} days of studying. | /session/quick |
| SL-STR-005 | One session to save it | Your {{streak_count}}-day streak needs 15 minutes. | /session/quick |

#### 3.11 Quiz Challenges

**Trigger:** After 3+ study sessions (engagement boost)

| ID | Title | Body | Deep Link |
|----|-------|------|-----------|
| SL-QZ-001 | Quick quiz ready | Test what you learned. 5 questions, 2 minutes. | /quiz/start |
| SL-QZ-002 | Challenge yourself | See how much you retained. Tap for a quick quiz. | /quiz/start |
| SL-QZ-003 | Quiz time | 5 questions based on your recent sessions. Ready? | /quiz/start |
| SL-QZ-004 | Test your knowledge | A quick quiz to reinforce what you've studied. | /quiz/start |
| SL-QZ-005 | Brain check | How much did you retain? Take a 2-minute quiz. | /quiz/start |

#### 3.12 Exam Prep Countdowns

**Trigger:** Daily at 7:00 PM (if exam date set, starting 14 days before)

| ID | Title | Body | Deep Link |
|----|-------|------|-----------|
| SL-EX-001 | {{days_until_exam}} days until {{exam_name}} | You've studied {{total_hours}} hours. Keep going. | /exam/{{exam_id}} |
| SL-EX-002 | Exam countdown: {{days_until_exam}} days | One more session tonight? Every minute counts. | /session/start |
| SL-EX-003 | {{exam_name}} in {{days_until_exam}} days | You're {{preparation_percent}}% prepared. Stay focused. | /exam/{{exam_id}} |
| SL-EX-004 | {{days_until_exam}} days left | Review your weak areas. Tap to see study recommendations. | /exam/{{exam_id}}/weak |
| SL-EX-005 | Final stretch: {{days_until_exam}} days | You've got this. One session closer to ready. | /session/start |

---

## 4. Segmentation Strategy

### 4.1 New Users (First 7 Days)

**Goal:** Form the habit, prevent early churn

**Day 1 (2 hours after install):**
| App | Title | Body |
|-----|-------|------|
| PrayerLock | Welcome to PrayerLock | Your first prayer session is waiting. Just 3 minutes to start. |
| WalkToUnlock | Let's get moving | Set your first step goal and unlock your phone by walking. |
| StudyLock | Ready to focus? | Your first study session takes just 15 minutes. Let's go. |

**Day 2 (if completed Day 1):**
| App | Title | Body |
|-----|-------|------|
| PrayerLock | Day 2: Building your habit | You prayed yesterday. Do it again and you're 2 days strong. |
| WalkToUnlock | Day 2: You're doing great | Yesterday was solid. Let's hit another goal today. |
| StudyLock | Day 2: Momentum building | One session down. Another today and you're on a roll. |

**Day 2 (if missed Day 1):**
| App | Title | Body |
|-----|-------|------|
| PrayerLock | Still here for you | Your first prayer takes just 3 minutes. Give it a try? |
| WalkToUnlock | Ready when you are | Set a small goal today. Even 2,000 steps is a win. |
| StudyLock | No pressure | Start with 10 minutes. That's all it takes to begin. |

**Day 3-5 (streak building):**
| Trigger | Title | Body |
|---------|-------|------|
| 3-day streak | 3 days in a row | You're building a habit. Don't stop now. |
| 4-day streak | Almost a week | Day 4 complete. 3 more days and you've done a full week. |
| 5-day streak | 5 days strong | Halfway to a week. You're crushing this. |

**Day 6-7 (milestone approaching):**
| Trigger | Title | Body |
|---------|-------|------|
| Day 6 | Tomorrow is day 7 | One more day and you've completed your first week. |
| Day 7 | One week complete | 7 days of building a new habit. You made it. |

### 4.2 Active Users (Weekly Active)

**Goal:** Maintain engagement, celebrate progress, upsell premium

**Weekly Summary (Sunday):**
- Title: "Your week in review"
- Body: "{{weekly_sessions}} sessions, {{total_time}} minutes. See your stats."

**Monthly Milestone (1st of month):**
- Title: "{{month_name}} recap"
- Body: "You {{verb}} {{monthly_count}} times last month. That's top {{percentile}}%."

**Premium Upsell (free users, after 14-day streak):**
- Title: "Unlock advanced insights"
- Body: "See detailed analytics with Premium. You've earned a free trial."

### 4.3 At-Risk Churn Users

**Definition:** No session in 3+ days (was previously active 3+ days/week)

**Re-engagement Sequence:**

| Day | Title | Body |
|-----|-------|------|
| Day 3 | We miss you, {{first_name}} | Your streak ended, but you can start fresh today. |
| Day 5 | Quick check-in | Life gets busy. Even 5 minutes keeps your progress alive. |
| Day 7 | Your progress is saved | Jump back in anytime. We're here when you're ready. |
| Day 14 | One last thing | We'll be quiet for a while. Tap when you want to restart. |

**After Day 14:** Suppress notifications for 30 days. Re-engage only for major updates.

### 4.4 Premium vs Free Users

**Free Users:**
- Include occasional premium feature teasers (max 1 per week)
- Example: "Premium users get detailed analytics. Curious?"
- Never upsell in streak/reminder notifications (feels pushy)

**Premium Users:**
- Never send upsell notifications
- Exclusive feature announcements
- "New Premium feature: {{feature_name}}"
- Priority access to new challenges
- More personalized insights

---

## 5. A/B Testing Framework

### 5.1 What to Test

| Priority | Element | Variants | Expected Impact |
|----------|---------|----------|-----------------|
| High | Send time | 2-3 time slots | 10-30% open rate change |
| High | Title copy | 2-3 variations | 15-40% open rate change |
| Medium | Emoji usage | With vs without | 5-15% open rate change |
| Medium | Personalization | Name vs no name | 5-20% open rate change |
| Low | Body copy | 2-3 variations | 5-10% CTR change |
| Low | CTA wording | Tap vs Open vs Start | 3-8% CTR change |

### 5.2 Sample Sizes Needed

For 95% confidence, 80% power:

| Expected Lift | Sample per Variant |
|---------------|-------------------|
| 5% | 31,000 |
| 10% | 8,000 |
| 15% | 3,600 |
| 20% | 2,000 |
| 30% | 900 |

**Practical Guidance:**
- Small user base (<5K DAU): Test 20%+ expected differences only
- Medium (10K+ DAU): Can test 10% differences
- Large (100K+ DAU): Can test 5% differences

### 5.3 Statistical Significance

**Minimum Test Duration:** 7 days (captures all day-of-week variation)

**Stop Test When:**
1. Reached sample size AND
2. p-value < 0.05 AND
3. Test ran at least 7 days

**Don't Stop Early:** Even if one variant looks better on day 2, run full 7 days.

**Tools:**
- Evan Miller's A/B Test Calculator: https://www.evanmiller.org/ab-testing/
- Firebase A/B Testing (built-in)
- OneSignal A/B Testing (built-in)

### 5.4 Iteration Cadence

| Phase | Duration | Focus |
|-------|----------|-------|
| Week 1-2 | Foundation | Test timing (2 variants) |
| Week 3-4 | Title optimization | Test 3 title formulas |
| Week 5-6 | Personalization | Name vs no name, tokens |
| Week 7-8 | Body copy | Test 2-3 body variants |
| Week 9+ | Refinement | Test winning elements in new contexts |

**Document Results:** Log all test results in `LEDGER/PUSH_NOTIFICATION_TESTS.csv`

**CSV Format:**
```csv
test_id,app,notification_type,variant_a,variant_b,metric,result_a,result_b,winner,start_date,end_date,sample_size
```

---

## 6. Metrics to Track

### 6.1 Open Rate Benchmarks

| App | Poor | Good | Great | Exceptional |
|-----|------|------|-------|-------------|
| PrayerLock | <15% | 20-30% | 30-40% | 40%+ |
| WalkToUnlock | <12% | 15-25% | 25-35% | 35%+ |
| StudyLock | <15% | 18-28% | 28-38% | 38%+ |

**Factors Affecting Open Rates:**
- Time since install (new users open more)
- Frequency (less is more)
- Quality of copy
- User engagement tier

### 6.2 Click-Through Rates

**CTR = (Taps on Notification) / (Notifications Delivered)**

| Rating | CTR |
|--------|-----|
| Poor | <5% |
| Good | 5-10% |
| Great | 10-15% |
| Exceptional | 15%+ |

**Improving CTR:**
- Use deep links to relevant screens (not home)
- Make action clear in body text
- Test different calls-to-action

### 6.3 Opt-Out Rates

| Rate | Status | Action |
|------|--------|--------|
| <0.1% | Excellent | Maintain current strategy |
| 0.1-0.3% | Good | Monitor weekly |
| 0.3-0.5% | Warning | Reduce frequency, improve copy |
| 0.5-1% | Critical | Pause non-essential notifications |
| >1% | Emergency | Stop all notifications, diagnose |

**Reducing Opt-Outs:**
- Add notification preferences in-app
- Respect quiet hours (10 PM - 7 AM)
- Make every notification valuable

### 6.4 Revenue Per Notification

| Metric | Formula | Benchmark |
|--------|---------|-----------|
| Revenue per Send | Total Revenue / Notifications Sent | $0.001-0.01 |
| Revenue per Open | Total Revenue / Opens | $0.01-0.05 |
| Revenue per Click | Total Revenue / Clicks | $0.05-0.20 |

**Attribution Window:** 24 hours from notification open

**Track:**
- Direct conversions (notification -> paywall -> purchase)
- Assisted conversions (notification -> session -> later purchase)
- LTV lift (notified users vs control group)

### 6.5 Dashboard Metrics (Track Weekly)

**Core Metrics:**
```
| Metric | This Week | Last Week | Change |
|--------|-----------|-----------|--------|
| Total Sent | | | |
| Open Rate | | | |
| CTR | | | |
| Opt-Out Rate | | | |
| Revenue Attributed | | | |
```

**Segment Breakdowns:**
- By user tier (new, active, at-risk)
- By notification type (reminder, achievement, streak)
- By app (PrayerLock, WalkToUnlock, StudyLock)

---

## 7. Implementation Checklist

### Phase 1: Foundation (Week 1)

- [ ] Set up OneSignal account (recommended free tier)
- [ ] Implement SDK in all apps
- [ ] Configure notification permission request (after first value moment)
- [ ] Set up timezone detection
- [ ] Create user segments in OneSignal

### Phase 2: Core Notifications (Week 2)

- [ ] Implement morning reminder for each app
- [ ] Implement streak warning notifications
- [ ] Implement achievement notifications
- [ ] Set up frequency capping (2/day max)
- [ ] Test on both iOS and Android

### Phase 3: Segmentation (Week 3)

- [ ] Build new user onboarding sequence
- [ ] Create active user engagement flows
- [ ] Set up churn prevention sequences
- [ ] Differentiate premium vs free messaging

### Phase 4: Optimization (Week 4+)

- [ ] Launch first A/B test (timing)
- [ ] Build notification performance dashboard
- [ ] Create `LEDGER/PUSH_NOTIFICATION_TESTS.csv`
- [ ] Document winning patterns

---

## 8. Quick Reference: Copy Bank

### High-Performing Titles (Proven Patterns)

**Streak-based:**
```
- "{{streak_count}} days and counting"
- "Don't break the chain"
- "Your streak needs you"
```

**Progress-based:**
```
- "You're {{percent}}% there"
- "Almost done for today"
- "{{remaining}} to go"
```

**Question hooks:**
```
- "Ready for today?"
- "Got 5 minutes?"
- "Continue where you left off?"
```

**Time-sensitive:**
```
- "2 hours left today"
- "Morning routine time"
- "End your day right"
```

### High-Performing Bodies (Proven Patterns)

**Social proof:**
```
- "Join {{number}} users who {{action}} today"
- "You're in the top {{percent}}% this week"
```

**Consequence:**
```
- "{{streak_count}} days of progress on the line"
- "One {{action}} keeps your streak alive"
```

**Ease:**
```
- "Just {{minutes}} minutes. That's it."
- "Quick {{action}}. Tap to start."
```

**Personalized:**
```
- "{{name}}, you've {{achievement}}. Keep going."
- "Your {{metric}} is waiting."
```

---

## 9. Platform-Specific Notes

### iOS

- Request permission after user experiences value (not on first open)
- Provisional notifications available (silent delivery to Notification Center)
- Rich notifications support images (use for achievements)
- Time-sensitive notifications can break through Focus Mode (use sparingly)

### Android

- Notification channels required (create per type: reminders, achievements, etc.)
- Users can disable specific channels
- Heads-up notifications for high priority only
- Action buttons allow "Start Session" without opening app

### Expo/React Native Implementation

```javascript
import * as Notifications from 'expo-notifications';

// Schedule streak warning
await Notifications.scheduleNotificationAsync({
  content: {
    title: "Your 7-day streak is at risk",
    body: "4 hours left. One prayer keeps your streak alive.",
    data: {
      type: 'streak_warning',
      streakCount: 7,
      deepLink: '/prayer/quick'
    },
  },
  trigger: {
    hour: 20, // 8 PM local time
    minute: 0,
    repeats: false,
  },
});

// Cancel if user completes session
await Notifications.cancelScheduledNotificationAsync(notificationId);
```

---

## 10. Common Mistakes to Avoid

1. **Asking for permission too early** - Wait until after first value moment
2. **Sending too frequently** - Max 2/day, usually 1/day is better
3. **Generic copy** - "Come back" is lazy. Be specific.
4. **Ignoring timezones** - Never send at 3 AM local time
5. **No deep linking** - Open to relevant screen, not home
6. **No A/B testing** - Always be testing something
7. **Forgetting opt-out tracking** - Monitor weekly
8. **Same message forever** - Rotate copy, test new variants

---

**Owner:** PRINTMAXX Product Team
**Related Docs:**
- `APP_MONETIZATION_STRATEGY.md`
- `APP_LAUNCH_FULL_STACK.md`
- `LEDGER/PUSH_NOTIFICATION_TESTS.csv` (create for tracking)
