# Escalation matrix

Who handles what, when to escalate, and SLA definitions.

---

## Escalation levels

### Level 1: Support (you)

**Handle directly:**
- Password resets
- How-to questions
- Billing inquiries (standard)
- Known bugs with documented workarounds
- Subscription changes (upgrade/downgrade/cancel)
- Feature explanations
- Basic troubleshooting (first 2 attempts)

**Time to resolve:** Same day for simple issues, 48 hours for moderate.

### Level 2: Senior support

**Escalate when:**
- Issue persists after 2 troubleshooting attempts
- Customer explicitly requests supervisor
- Account lifetime value >$500
- Potential data loss
- Complex billing disputes
- Multi-account issues

**How to escalate:** Tag @senior-support in ticket with summary.

**Time to resolve:** 24-48 hours.

### Level 3: Engineering

**Escalate when:**
- Confirmed bug with no workaround
- Data corruption or loss
- Security vulnerability reported
- Server errors visible in logs
- Integration failures on our end
- Performance issues affecting multiple users

**How to escalate:** Create ticket in [ENGINEERING BOARD] with:
- Steps to reproduce
- User ID and account details
- Error messages/logs
- Screenshots or video
- Number of users affected

**Time to resolve:** 24-72 hours depending on severity.

### Level 4: Founder/executive

**Escalate when:**
- Legal action threatened
- Refund request >$100 (disputed)
- PR risk (influencer, journalist, large following)
- Competitor mentioned as replacement
- Systemic issue affecting many users
- Security breach confirmed
- Regulatory/compliance issue

**How to escalate:** Direct message in Slack with one-paragraph summary. Don't wait.

**Time to resolve:** 4-24 hours.

---

## What to escalate

### Always escalate immediately

| Trigger | Escalate to |
|---------|-------------|
| "I'm going to post about this on Twitter/Reddit" | Founder |
| "I'm contacting my lawyer" | Founder |
| "I'm a journalist writing about your company" | Founder |
| Security breach or data exposure | Engineering + Founder |
| Complete service outage | Engineering |
| GDPR/CCPA data request | Senior Support |
| Account hacking suspected | Engineering |

### Escalate after troubleshooting fails

| Issue | Escalate to |
|-------|-------------|
| Bug with no workaround | Engineering |
| Payment stuck in limbo | Senior Support |
| Data not syncing after all fixes | Engineering |
| Account access issues (not password) | Engineering |
| Integration broken on our side | Engineering |

### Don't escalate (handle yourself)

- Customer is frustrated but issue is resolved
- Feature requests (log in backlog)
- General feedback
- Questions you can answer from documentation
- Price complaints (policy is policy)

---

## SLA definitions

### Response time SLAs

| Priority | First response | Target resolution |
|----------|----------------|-------------------|
| Critical | 2 hours | 24 hours |
| High | 8 hours | 48 hours |
| Medium | 24 hours | 72 hours |
| Low | 48 hours | 5 business days |

Business hours: 9am-6pm PST, Monday-Friday.

### Priority definitions

**Critical**
- Complete service outage
- Payment system down
- Security incident
- Data loss affecting multiple users
- Legal threat

**High**
- Feature completely broken
- Payment failed (customer trying to pay)
- Sync issues preventing work
- Account locked out

**Medium**
- Feature partially broken
- Minor bugs with workarounds
- How-to questions
- Billing questions (non-urgent)

**Low**
- Feature requests
- General feedback
- Documentation questions
- Cosmetic issues

---

## External escalations

### App Store / Google Play

Issues we escalate to Apple/Google:
- Review manipulation reports
- Fraudulent charge disputes they initiate
- App rejection appeals
- Rating/review removals

We cannot fix:
- Customer's payment method issues with them
- Their account restrictions
- Family sharing conflicts

### Payment processor (Stripe)

Escalate to Stripe when:
- Fraud dispute needs documentation
- Payout issues on our end
- Webhook failures from their side
- Account verification requirements

### Cloud provider

Escalate to [AWS/GCP/etc.] when:
- Infrastructure outage
- Security incident from their side
- Performance degradation at infrastructure level

---

## Escalation template

When escalating, include:

```
**Summary:** [One sentence description]

**Customer:** [Email, user ID, plan]

**Issue:** [What's happening]

**Impact:** [How many users, revenue at risk]

**Tried:** [What you already attempted]

**Evidence:** [Screenshots, logs, ticket link]

**Urgency:** [Critical/High/Medium/Low and why]
```

---

## Escalation tracking

Log all escalations in [ESCALATION LOG / SHEET].

Track:
- Date/time escalated
- Who escalated
- Who received
- Resolution time
- Outcome

Review escalation patterns monthly. Recurring escalations indicate systemic issues to fix.

---

## When in doubt

**Ask yourself:**
1. Can I solve this in the next 30 minutes?
2. Do I have the access/authority needed?
3. Is the customer getting more frustrated?
4. Is there any legal/PR risk?

If answers are no/no/yes/yes, escalate immediately.

Better to escalate unnecessarily than to make a frustrated customer wait.
