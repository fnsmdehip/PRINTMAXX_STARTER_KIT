# Support Playbook

Last updated: 2026-01-21

---

## Response time targets

| Priority | First response | Resolution |
|----------|----------------|------------|
| Critical (app down, payment failed) | 2 hours | 24 hours |
| High (feature broken, sync issues) | 8 hours | 48 hours |
| Medium (how-to questions, minor bugs) | 24 hours | 72 hours |
| Low (feature requests, feedback) | 48 hours | Acknowledge only |

Business hours: 9am-6pm PST, Monday-Friday.
Weekend coverage: Critical issues only, 4-hour response.

---

## Escalation paths

### Level 1 - Support (you)
- Password resets
- Billing questions
- How-to guidance
- Known bug workarounds
- Subscription changes

### Level 2 - Senior support
Escalate when:
- Issue persists after 2 troubleshooting attempts
- Customer requests manager
- Account has >$500 lifetime value
- Legal or compliance mentions

### Level 3 - Engineering
Escalate when:
- Bug confirmed but no workaround exists
- Data loss reported
- Security concern
- Server-side error logs needed

### Level 4 - Founder
Escalate when:
- Threat of public complaint/review
- Refund >$100 disputed
- Legal action mentioned
- Press/influencer account

---

## Common issue categories

### Billing (35% of tickets)
- Charge not recognized
- Subscription not active after payment
- Refund request
- Upgrade/downgrade questions
- Failed payment retry

### Technical (40% of tickets)
- App crashes on launch
- Sync not working
- Features missing after update
- Slow performance
- Login issues

### Product (15% of tickets)
- How do I do X?
- Feature requests
- Integration questions
- Comparison to competitors

### Account (10% of tickets)
- Password reset
- Email change
- Account deletion
- Data export request

---

## Refund policy

### Automatic approval
- Within 7 days of purchase
- No previous refund on account
- Amount under $50

### Manual review required
- 8-30 days since purchase
- Previous refund on account
- Amount $50-$100

### Founder approval required
- Over 30 days since purchase
- Multiple previous refunds
- Amount over $100

### Always deny
- Obvious abuse pattern (buy-use-refund)
- Third refund request
- After explicit warning about refund limits

When denying: Be direct, explain why, offer alternative (credit, downgrade).

---

## Tone guidelines

### Do
- Get to the point in the first sentence
- Use "you" and "your" (not "the user" or "one")
- Admit when we messed up
- Give specific next steps
- Match their energy (casual = casual, frustrated = calm and direct)

### Don't
- Say "I hope this helps!"
- Say "Please let me know if you have any questions"
- Use "we apologize for any inconvenience"
- Use corporate jargon (leverage, utilize, per se)
- Over-explain obvious things

### Template structure
1. Acknowledge what they said (1 sentence max)
2. Answer or fix the problem
3. One clear next step
4. Sign off

### Example

Bad:
> Thank you so much for reaching out to us today! I hope this message finds you well. I completely understand how frustrating this must be for you, and I want you to know that we truly value your feedback. I've gone ahead and escalated this to our engineering team who will delve into the issue further. Please don't hesitate to reach out if you have any other questions!

Good:
> Got it. Your subscription should be active now - I manually synced it on our end. If it's still not showing, log out and back in. That usually fixes it.
>
> - Alex

---

## Response priority rules

1. Angry customers first
2. Paying customers before trial users
3. Simple fixes before complex investigations
4. Reply-all threads last (usually noise)

---

## Tools access

- Stripe dashboard: Billing issues, refunds
- Database admin: Account lookups, manual fixes
- Error logs: Server-side debugging
- Intercom/Zendesk: Ticket management
- Slack #support: Internal escalation

---

## When in doubt

Ask in #support-internal before responding if:
- Customer mentions lawyer/legal
- You're about to promise something we can't deliver
- The issue involves another customer's data
- You're not sure if a refund is appropriate

Better to delay 30 minutes than send a wrong answer.
