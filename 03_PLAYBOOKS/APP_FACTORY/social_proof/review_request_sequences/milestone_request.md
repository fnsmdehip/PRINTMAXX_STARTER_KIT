# Milestone-based review requests

Triggered at specific user milestones: Day 7, Day 30, Day 90.

---

## Day 7: First week complete

**Trigger:** User has been active for 7 days AND completed at least one core action.

**In-app message:**

```
You've been using [App Name] for a week now.

If it's been helpful, a quick review helps others find it.

[Leave a Review] [Maybe Later] [Never Ask Again]
```

**Email version:**

Subject: One week with [App Name]

Hey [First Name],

You've used [App Name] for a week. [Specific stat if available: "You've logged 12 entries" or "You've saved approximately 45 minutes."]

If the app is working for you, a review helps other people find it:
[Review link]

If something's frustrating, reply here. I fix things fast.

[Your Name]

---

## Day 30: Established user

**Trigger:** User active for 30+ days AND engaged in last 7 days.

**In-app message:**

```
You've been using [App Name] for a month.

Your feedback helps shape what I build next. Would you share your experience?

[Write a Review] [Send Feedback Instead] [Not Now]
```

**Email version:**

Subject: 30 days in - quick favor?

Hey [First Name],

You've been using [App Name] for a month now. That puts you in the top 20% of active users.

If you have 30 seconds, a review would help a lot:
[Review link]

Or if you'd rather share feedback privately, reply to this email. I read everything and it directly influences what I build.

Thanks,
[Your Name]

---

## Day 90: Power user / Loyal customer

**Trigger:** User active for 90+ days AND engaged in last 14 days.

**In-app message:**

```
You've been with [App Name] for 3 months.

You're one of our longest-active users. Would you share what's kept you using the app?

[Share Your Story] [Leave a Review] [Not Now]
```

**Email version:**

Subject: You've been here since [month they joined]

Hey [First Name],

You joined [App Name] back in [Month]. You're one of the earliest users still actively using the app.

I'd love to feature your experience - whether that's:
- A quick review (30 seconds): [link]
- A short case study (I'll write it, you just answer 3 questions)
- A testimonial quote I can use on the website

If you're interested in any of those, reply and let me know which works best.

Either way, thanks for sticking around.

[Your Name]

---

## Milestone tracking logic

```
Day 7:
- Condition: days_since_signup >= 7
- Condition: core_actions_completed >= 1
- Condition: review_request_count == 0
- Action: Show in-app prompt OR send email

Day 30:
- Condition: days_since_signup >= 30
- Condition: last_active_days <= 7
- Condition: review_request_count <= 1
- Condition: has_not_reviewed == true
- Action: Show in-app prompt OR send email

Day 90:
- Condition: days_since_signup >= 90
- Condition: last_active_days <= 14
- Condition: has_not_reviewed == true
- Action: Send personalized email (higher touch)
```

---

## Suppression rules

Do NOT trigger milestone requests if:
- User has open support ticket
- User rated app negatively (1-3 stars) in-app
- User clicked "Never Ask Again"
- User unsubscribed from marketing emails
- User churned and returned (different sequence)

---

## FTC compliance

- No incentives for reviews
- Equal treatment regardless of likely rating
- Private feedback option always available
- Respect "don't ask again" preferences
