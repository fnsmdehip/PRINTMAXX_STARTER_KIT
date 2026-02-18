# Notification strategy

Push notifications are the highest-impact retention tool. Done right, they 2-3x retention. Done wrong, they get your app uninstalled.

---

## Optimal timing research

### Best times by category

**Faith apps**
- Morning reminder: 6:30-7:00 AM (before day starts)
- Streak risk: 8:00-9:00 PM (end of day, still time to act)
- New content: 10:00 AM Saturday (weekend engagement)

**Fitness apps**
- Daily reminder: 7:00 AM or user's workout time
- Inactivity nudge: 12:00 PM (lunch break opportunity)
- Goal achieved: immediate
- Streak celebration: immediate

**Productivity apps**
- Focus reminder: 5 min before scheduled session
- Session complete: immediate
- Daily summary: 8:00-9:00 PM
- Feature discovery: 10:00 AM or 2:00 PM (low-focus times)

### Time zone handling

1. Store user's timezone on registration
2. Update timezone if device reports different one
3. All notifications scheduled in local time
4. Recalculate schedules when timezone changes

### Weekend vs weekday

- Weekends: delay morning notifications by 1 hour
- Fridays: reduce afternoon notifications (people winding down)
- Mondays: good for "fresh start" messaging
- Sundays: weekly summary time

---

## Frequency limits

### Per notification type

| Type | Max per day | Max per week |
|------|-------------|--------------|
| Morning reminder | 1 | 7 |
| Streak at risk | 2 | 14 |
| Goal achieved | 1 | 7 |
| New content | 0 | 2 |
| Feature discovery | 0 | 1 |
| Community | 5 | 20 |

### Global limits

- Max 3 notifications per day total
- Max 15 notifications per week total
- No notifications between 10 PM - 6 AM (quiet hours)
- If user ignores 5 in a row, reduce frequency by 50%

### Escalation rules

Day 1-7: Normal frequency
Day 8-14 (no opens): Reduce to 1/day max
Day 15-30 (no opens): Weekly digest only
Day 31+ (no opens): Re-engagement campaign, then stop

---

## Personalization rules

### Behavior-based

1. **Completion time**: If user typically completes at 6 PM, remind at 5:30 PM
2. **Skip patterns**: If user skips Sundays, don't notify on Sundays
3. **Session length**: Adjust break suggestions based on typical session length
4. **Response time**: If user opens within 5 min, current timing works

### Engagement-based

1. **High engagers** (open 80%+): Can receive more notifications
2. **Medium engagers** (40-80%): Standard frequency
3. **Low engagers** (<40%): Reduce to essentials only
4. **Dormant** (7+ days inactive): Re-engagement sequence

### Content-based

1. Track which notification types get opened
2. Increase types that work, reduce types that don't
3. A/B test copy variants, promote winners
4. Personalize based on user's in-app activity

---

## A/B test ideas

### Copy tests

1. **Length**: Short (3 words) vs medium (8 words) titles
2. **Tone**: Direct vs question vs supportive
3. **Numbers**: With streak count vs without
4. **Personalization**: With name vs without
5. **Urgency**: "Now" vs "When ready"

### Timing tests

1. Morning: 6:30 AM vs 7:00 AM vs 7:30 AM
2. Evening: 6 PM vs 8 PM vs 9 PM
3. Advance notice: 5 min vs 15 min vs 30 min
4. Day of week for weekly content

### Format tests

1. Rich notification (image) vs text only
2. Action buttons vs no buttons
3. Sound vs silent
4. Grouped vs individual

### Measurement

- Primary metric: open rate
- Secondary: conversion to target action
- Track by: user segment, notification type, variant
- Statistical significance: wait for 1000+ samples per variant

---

## Opt-out handling

### Granular preferences

Let users control:
- All notifications on/off
- Morning reminders on/off
- Streak alerts on/off
- New content on/off
- Community notifications on/off
- Quiet hours (custom start/end)

### Soft opt-out

Before full opt-out:
1. Reduce frequency (weekly digest only)
2. Offer time-based pause (1 week, 1 month)
3. Ask which types they want to keep

### Re-engagement after opt-out

If user opted out but is still active:
- In-app prompt after 30 days: "Want notifications back?"
- Highlight what they missed
- One-tap re-enable

### Hard opt-out

If user disables at OS level:
- Detect on next app open
- Don't nag to re-enable
- Use in-app notifications instead
- Track for analytics (might indicate app issues)

---

## Implementation checklist

### Before launch

- [ ] Notification service integrated
- [ ] All templates have 2+ variants
- [ ] Quiet hours implemented
- [ ] Timezone handling tested
- [ ] Preference screen built
- [ ] Analytics events defined
- [ ] A/B test infrastructure ready

### After launch

- [ ] Monitor open rates daily for first week
- [ ] Check uninstall correlation
- [ ] Run first A/B test within 2 weeks
- [ ] Review feedback/reviews mentioning notifications
- [ ] Adjust frequency based on data

### Monthly review

- [ ] Open rate by notification type
- [ ] Conversion rate by notification type
- [ ] Uninstall rate correlation
- [ ] Top performing copy variants
- [ ] Underperforming notifications to cut

---

## Anti-patterns to avoid

### Never do

1. Send more than 3 notifications per day
2. Notify during quiet hours
3. Use clickbait titles that don't match content
4. Send notifications that don't require action
5. Notify about features user already uses
6. Send "miss you" messages before 7 days inactive
7. Use guilt or shame in copy
8. Include promotional content in utility notifications

### Red flags

- Open rate below 5%: something is wrong
- Uninstall spike after notification: too aggressive
- User complaints in reviews: public damage
- Permission revocation: you've lost trust

---

## Platform-specific notes

### iOS

- Rich notifications need extension
- Provisional authorization available (try before asking)
- Critical alerts for truly important apps only
- Focus modes may suppress notifications

### Android

- Notification channels required (group by type)
- Heads-up notifications for high priority only
- Notification dots show unread count
- Power saver may delay notifications

### Both

- Deep links to specific screens
- Action buttons for quick responses
- Images supported (use sparingly)
- Badge count management
