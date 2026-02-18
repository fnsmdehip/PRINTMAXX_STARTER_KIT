# App store review strategy

When to ask, how to optimize, and how to prevent negative reviews.

---

## Why reviews matter

**App store ranking factors:**
- Review quantity (more is better)
- Review recency (recent reviews weighted higher)
- Average rating (4.0+ is table stakes, 4.5+ is competitive)
- Review velocity (consistent flow beats sporadic bursts)
- Review quality (detailed reviews may carry more weight)

**User behavior:**
- 79% of users check ratings before downloading
- 53% want 4+ stars minimum
- 1-star jump in rating can increase conversions 5-10%

---

## When to ask for reviews

### Best moments (high emotional state)

**Ask immediately after:**
- Completing a core action successfully
- Reaching a milestone (7 days, 10 uses, first achievement)
- Positive moment (goal met, task completed, progress visible)
- Feature they requested gets shipped
- Support issue gets resolved positively

**Specific triggers:**
```
// Productivity app
if (tasksCompletedToday >= 5) triggerReviewPrompt()

// Health app
if (streakDays >= 7) triggerReviewPrompt()

// Utility app
if (totalUses >= 10 && lastActionSuccessful) triggerReviewPrompt()
```

### When NOT to ask

**Never ask:**
- On first launch
- During onboarding
- After an error or crash
- When user is mid-task
- After a failed action
- If they opened a support ticket recently
- If they already dismissed a prompt
- If they already reviewed

---

## iOS vs Android timing

### iOS specifics

**Apple limits:**
- SKStoreReviewController: 3 prompts per 365 days (Apple enforces)
- System decides whether to actually show prompt
- No guarantee your request results in visible prompt
- Cannot customize the prompt UI

**iOS timing strategy:**
```
Day 7: First prompt (if engaged)
Day 30: Second prompt (if didn't review)
Day 90: Third prompt (power users only)
```

**iOS best practices:**
- Save prompts for best moments
- Don't waste prompts early in user journey
- Track when you've requested (even if not shown)
- Test prompt timing with A/B tests

### Android specifics

**Play Store allows:**
- In-App Review API: More flexibility than iOS
- Can request more frequently
- Still has quotas (Google doesn't publish exact limits)
- User can dismiss without reviewing

**Android timing strategy:**
```
Day 3: Light prompt (satisfaction check only)
Day 7: First real prompt
Day 21: Second prompt if engaged
Day 45+: Additional prompts for power users
```

**Android best practices:**
- Pre-qualify with satisfaction question
- Route unhappy users to feedback form
- Monitor review-to-prompt ratio
- Adjust frequency based on results

---

## Review velocity optimization

### Consistent flow vs. burst

**Bad:** 100 reviews in Week 1, then 2 reviews per month
**Good:** 8-10 reviews per week, sustained

### Velocity tactics

**1. Stagger prompt timing**
Don't prompt all users at the same trigger. Randomize:
```
// Instead of prompting all Day 7 users at once
const promptDelay = Math.random() * 3 // 0-3 days
schedulePrompt(user, day7 + promptDelay)
```

**2. Segment by engagement**
- Power users: Prompt earlier (Day 5)
- Regular users: Standard timing (Day 7-10)
- Light users: Prompt later (Day 14+)

**3. Feature release reviews**
After shipping new feature:
- Notify users who requested it
- Prompt for review in that notification
- "You asked, we built it. Mind sharing your updated experience?"

**4. Support resolution reviews**
When closing positive support ticket:
- Wait 24-48 hours
- Send follow-up: "Glad we could help. If you have a moment, a review helps us keep improving."

---

## Negative review prevention

### Pre-emptive feedback collection

**The two-step flow:**
```
Step 1: "How's [App Name] working for you?"
        [Great!] [Could be better]

If "Could be better":
Step 2: "What could we improve?"
        [Text field]
        [Submit feedback]

If "Great!":
Step 2: "Would you share that on the App Store?"
        [Leave review] [Maybe later]
```

This routes frustrated users to feedback instead of 1-star reviews.

### Common complaint prevention

**Identify patterns:**
- Track feedback themes
- Monitor support tickets
- Watch negative review keywords
- Survey churned users

**Address proactively:**
- Fix recurring bugs before they cause reviews
- Improve confusing UX before users complain
- Add help content for common questions
- Onboard users to prevent early frustration

### In-app help before they leave

**Detect frustration signals:**
- Multiple failed attempts at same action
- Rage tapping
- Extended time on error screens
- Navigating in circles

**Intervene:**
```
Looks like you might be stuck. Need help with [task]?

[Get help] [I'm fine]
```

### Recovery after negative experience

**If crash or error occurs:**
1. Log it immediately
2. Show empathetic error message
3. Follow up within 24 hours if possible
4. Don't prompt for review for at least 14 days

**Recovery email:**
```
Subject: Sorry about that

Hey [Name],

We noticed [App Name] crashed/had an issue yesterday. Sorry about that.

We've already pushed a fix in version [X.X].

If you're still seeing problems, reply to this email. I'll personally help.

[Your Name]
```

---

## Responding to negative reviews

### Response speed

- Respond within 24 hours
- Faster response = higher chance they update review
- Shows other users you're responsive

### Response framework

1. **Acknowledge** the problem
2. **Apologize** (without admitting fault if not your bug)
3. **Offer solution** (contact email, troubleshooting, timeline for fix)
4. **Invite follow-up** (not asking them to change review)

**Example:**
```
Sorry about this, [Name]. That shouldn't happen. We're looking into it now.

Can you email support@[app].com with details? We'll get this sorted for you.
```

### After you've fixed the issue

Update your response:
```
Update: We fixed this in version [X.X]. Hope it's working better now. Thanks for the feedback that helped us catch it.
```

Some users will update their rating. Most won't. That's fine.

---

## Review monitoring

### Metrics to track

| Metric | Target | Action if below |
|--------|--------|-----------------|
| Average rating | 4.5+ | Investigate negative trends |
| Weekly review count | 5-10+ | Increase prompt frequency |
| 1-star percentage | <5% | Focus on prevention |
| Response rate | 100% | Set up alerts |
| Rating trend | Stable/up | Address if declining |

### Tools

**Free:**
- App Store Connect (iOS)
- Google Play Console (Android)
- RSS feeds for new reviews

**Paid:**
- AppFollow
- Appbot
- ReviewBot
- Sensor Tower

### Alert setup

Set up alerts for:
- Any 1-star review (respond immediately)
- Any 2-star review (respond within 24h)
- Keyword mentions (bugs, crash, broken, etc.)
- Rating drops below threshold
- Review velocity changes

---

## What NOT to do

### Apple/Google violations

**Prohibited:**
- Incentivizing reviews (free features, discounts for reviews)
- Buying reviews
- Review manipulation services
- Asking specifically for 5-star reviews
- Gating content behind reviews
- Spamming review requests

**Consequences:**
- App removal
- Account suspension
- Loss of all reviews
- Permanent ban

### Gray areas to avoid

- Prompting only users likely to leave positive reviews (technically risky)
- A/B testing that segments by predicted satisfaction (borderline)
- "We'll give you X if you rate us" (clear violation)
- "Rate us 5 stars to unlock..." (clear violation)

### What you CAN do

- Ask all users (not selectively) at good moments
- Route unhappy users to feedback (before review prompt)
- Respond to reviews publicly
- Ask users to update reviews after fixing issues (in response, not demand)
- Thank users who leave reviews

---

## Review audit checklist

Weekly:
- [ ] Check average rating trend
- [ ] Respond to all new negative reviews
- [ ] Review feedback themes
- [ ] Check review velocity

Monthly:
- [ ] Analyze prompt conversion rate
- [ ] Compare iOS vs Android performance
- [ ] Review competitor ratings
- [ ] Update response templates if needed

Quarterly:
- [ ] Audit prompt timing and triggers
- [ ] Review A/B test results
- [ ] Update strategy based on data
- [ ] Check for policy changes (Apple/Google)
