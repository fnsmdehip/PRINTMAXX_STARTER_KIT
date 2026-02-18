# Push Notification Strategy Guide

Timing, copy, segmentation, and A/B testing for mobile push notifications.

---

## Notification Timing Matrix

### By User Behavior

| User Segment | Best Time | Frequency | Content Focus |
|--------------|-----------|-----------|---------------|
| Power users (daily) | Morning (7-9am) | 1x/day max | Feature discovery |
| Regular users (3-4x/week) | Evening (6-8pm) | 3x/week | Streak/progress |
| Casual users (1x/week) | Sunday evening | 1x/week | Re-engagement |
| Churning (14+ days inactive) | Variable (test) | 1x then wait | Win-back offer |

### By App Category

| Category | Primary Time | Secondary Time | Avoid |
|----------|--------------|----------------|-------|
| Fitness | 6-7am, 5-6pm | Weekends 8am | Late night |
| Productivity | 8-9am weekdays | Sunday 7pm | Weekends |
| Meditation/Prayer | 6am, 9pm | Lunch 12pm | Work hours |
| Finance | 7-8am | Market close 4pm | Weekends |
| Entertainment | 7-9pm | Weekends all day | Work hours |
| Learning | 7-8pm | Weekend mornings | Late night |

### Time Zone Handling

```
Strategy: Send at user's local time

Implementation:
1. Capture timezone on app install (device setting)
2. Store in user profile
3. Schedule based on local time
4. Fallback: Use IP geolocation

Never: Send at server time to all users
```

---

## Notification Copy Formulas

### The Proven Structures

**1. Progress Prompt**
```
[User Name], you're [X]% there!
Just [action] to [achieve goal].
```
Example: "Sarah, you're 80% there! Just 2 more sessions to complete your 7-day streak."

**2. Social Proof**
```
[X] people just [action]
Join them and [benefit].
```
Example: "1,247 people just completed their morning prayer. Join them and start your day right."

**3. Loss Aversion**
```
Your [progress/streak] expires in [time].
[Action] now to save it.
```
Example: "Your 14-day streak expires in 2 hours. Open now to save it."

**4. Personalized Insight**
```
Based on your [behavior],
try [recommendation].
```
Example: "Based on your sleep patterns, try our 10pm wind-down session."

**5. Simple Reminder**
```
Time for your [activity].
[Motivational phrase].
```
Example: "Time for your daily prayer. 5 minutes to peace."

**6. Achievement Unlock**
```
You just earned [achievement]!
Tap to see what's next.
```
Example: "You just earned the Early Bird badge! Tap to see what's next."

**7. Content Freshness**
```
New: [content description]
[Benefit/curiosity hook].
```
Example: "New: Gratitude meditation for stressful days. 8 minutes to calm."

---

## Segmentation Framework

### Behavioral Segments

| Segment | Criteria | Notification Strategy |
|---------|----------|----------------------|
| Champions | Daily use, 30+ day streak | Feature tips, premium upsell |
| Regulars | 3-4x/week, engaged | Streak maintenance, habit building |
| Casuals | 1x/week or less | Re-engagement, value reminders |
| At-Risk | No activity 7-14 days | Win-back, special offers |
| Dormant | No activity 14+ days | Final re-engagement, then remove |

### Lifecycle Segments

| Stage | Days Since Install | Priority Notifications |
|-------|-------------------|----------------------|
| Onboarding | 0-7 | Tutorial completion, first value |
| Activation | 7-30 | Habit formation, streak building |
| Retention | 30-90 | Feature discovery, upgrades |
| Loyalty | 90+ | Referrals, advanced features |

### Permission Strategy by Segment

```
New Users (Day 0-3):
- Delay permission request until after first value moment
- Show value preview before asking
- Use soft ask first ("Would you like reminders?")

Active Users (Day 7+):
- Can request for new features
- Contextual asks (e.g., "Get notified when X happens?")

Re-engaged Users:
- Careful with frequency
- Respect previous opt-out patterns
```

---

## A/B Testing Framework

### What to Test

| Element | Test Type | Sample Size Needed |
|---------|-----------|-------------------|
| Send time | Hour of day | 5,000+ per variant |
| Copy | Message text | 3,000+ per variant |
| Emoji | With vs without | 3,000+ per variant |
| Personalization | Name vs no name | 3,000+ per variant |
| Urgency | With vs without | 3,000+ per variant |
| Length | Short vs long | 3,000+ per variant |

### Testing Methodology

```
1. Define hypothesis
   "Including user name will increase open rate by 10%"

2. Set sample size
   Minimum 3,000 per variant for meaningful results

3. Run test for 7+ days
   Capture weekday and weekend behavior

4. Measure primary metric
   Open rate for engagement tests
   Retention for value tests

5. Statistical significance
   p < 0.05 before declaring winner

6. Document and implement
   Log results, roll out winner
```

### Sample Test Results Log

| Test | Variant A | Variant B | Winner | Lift |
|------|-----------|-----------|--------|------|
| Time: 7am vs 9am | 12% open | 18% open | 9am | +50% |
| Name personalization | 14% open | 19% open | With name | +36% |
| Emoji: With vs without | 15% open | 17% open | With emoji | +13% |
| Length: Short vs long | 16% open | 13% open | Short | +23% |

---

## Notification Categories

### Transactional (Always Send)
- Account security alerts
- Payment confirmations
- Password reset
- Subscription status changes

### Critical Feature
- Streak about to break
- Goal deadline approaching
- Content they requested

### Engagement (User Controlled)
- Daily reminders
- New content alerts
- Community updates
- Progress celebrations

### Marketing (Careful)
- Feature announcements
- Upgrade prompts
- Special offers

---

## Frequency Caps

### Recommended Limits

| User Type | Max per Day | Max per Week | Quiet Hours |
|-----------|-------------|--------------|-------------|
| New (0-7 days) | 1 | 4 | 10pm-7am |
| Active | 2 | 7 | 10pm-7am |
| Casual | 1 | 2 | 10pm-7am |
| At-Risk | 1 | 1 | 10pm-7am |

### Fatigue Prevention

```
Rules:
1. No more than 1 notification per 4-hour window
2. Skip day after high-frequency period
3. Reduce frequency if open rate drops below 5%
4. Stop completely if user ignores 5 in a row
```

---

## Copy Templates by Use Case

### Streak Maintenance

```
[User], your [X]-day streak is alive!
Open now to keep it going.

---

Don't lose your [X]-day streak.
Just [action] to continue.

---

Your streak ends at midnight.
2 minutes to save it.
```

### Re-engagement (7-14 days inactive)

```
We miss you, [User].
Your [goal/progress] is waiting.

---

[User], [X] people completed [action] this week.
Ready to join them?

---

Quick win waiting inside.
[Specific feature/content] takes 3 minutes.
```

### Feature Announcement

```
New: [Feature name]
[One-line benefit].

---

You asked, we built.
[Feature] is now live.

---

Try this: [Feature name]
[Specific use case benefit].
```

### Celebration/Achievement

```
You did it!
[Achievement name] unlocked.

---

[X] [actions] this month!
New personal best.

---

Milestone: [X] total [actions].
See your progress →
```

### Win-back (14+ days)

```
We saved your progress.
[X] [actions] waiting for you.

---

[User], it's been a while.
Start fresh with [quick win offer].

---

Your [goal] is still achievable.
Just [X] minutes to get back on track.
```

---

## Platform-Specific Guidelines

### iOS

```
Limits:
- Title: 50 characters visible
- Body: 4 lines visible (collapsed)
- Rich notifications: Images, buttons

Best Practices:
- Request permission after value shown
- Use provisional authorization first (silent)
- Support notification grouping
- Implement notification service extension for rich content
```

### Android

```
Limits:
- Title: No strict limit, but keep short
- Body: 2 lines visible (collapsed)
- Big text style: Can show more

Best Practices:
- Channel categories for user control
- Priority levels (high for time-sensitive)
- Heads-up display sparingly
- Direct reply actions where appropriate
```

---

## Metrics to Track

### Primary Metrics

| Metric | Formula | Healthy Range |
|--------|---------|---------------|
| Opt-in Rate | Opted In / Asked | 40-60% |
| Delivery Rate | Delivered / Sent | >95% |
| Open Rate | Opens / Delivered | 5-15% |
| Conversion Rate | Actions / Opens | 10-30% |
| Opt-out Rate | Unsubscribed / Sent | <0.5% |

### Tracking Dashboard

```
Weekly Report Structure:

1. Volume
   - Notifications sent
   - Unique users reached
   - By category breakdown

2. Engagement
   - Open rate by segment
   - Open rate by category
   - Time-to-open distribution

3. Quality
   - Opt-out rate
   - Disabled notification rate
   - Complaint signals

4. Impact
   - Session starts from push
   - Conversion to key action
   - Revenue attributed
```

---

## Common Mistakes to Avoid

1. **Sending too early in onboarding**
   - Wait for first value moment
   - Ask contextually, not at install

2. **Same message to everyone**
   - Segment by behavior
   - Personalize content

3. **Too many notifications**
   - Respect frequency caps
   - Quality over quantity

4. **Ignoring timezone**
   - Always send at local time
   - Respect quiet hours

5. **No A/B testing**
   - Test everything
   - Document results

6. **Ignoring opt-outs**
   - Track why users disable
   - Adjust strategy accordingly

7. **Generic copy**
   - Be specific
   - Reference user's activity

---

## Quick Reference Checklist

**Before Sending:**
- [ ] Is this the right time for this user's timezone?
- [ ] Have we sent too many already today/this week?
- [ ] Is the copy personalized?
- [ ] Is the CTA clear?
- [ ] Will this notification be useful to the user?
- [ ] Are we respecting quiet hours?

**Monthly Audit:**
- [ ] Review opt-out rates by category
- [ ] Check open rate trends
- [ ] Analyze best-performing copy
- [ ] Update segments based on behavior
- [ ] Remove or modify underperforming notifications

---

Last updated: 2026-01-23
