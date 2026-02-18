# Satisfaction survey email templates

Templates for collecting feedback after support interactions.

---

## Simple CSAT survey

**Use when:** Standard post-resolution survey. Send automatically or manually after closing.

---

Subject: Quick question about your support experience

Hi [NAME],

Your recent support request is resolved.

**How was your experience?**

[SATISFIED BUTTON] | [UNSATISFIED BUTTON]

One click. No account needed.

Thanks,
[COMPANY NAME] Support

---

## CSAT with comment option

**Use when:** Want qualitative feedback along with rating.

---

Subject: 30 seconds: How did we do?

Hi [NAME],

We just resolved your support request about [BRIEF TOPIC].

**Rate your experience:**

[SATISFIED] | [NEUTRAL] | [UNSATISFIED]

**Optional: What could we have done better?**
[Reply to this email with feedback]

Your input helps us improve.

- [COMPANY NAME] Support

---

## NPS survey (quarterly)

**Use when:** Measuring overall satisfaction, not tied to specific ticket.

---

Subject: One question for you

Hi [NAME],

Quick question:

**How likely are you to recommend [PRODUCT] to a friend or colleague?**

0 [Not likely] -------- 5 -------- 10 [Very likely]

[RATING BUTTONS 0-10]

Why that score? (optional)
[Reply with your thoughts]

Takes 10 seconds. Helps us a lot.

- [COMPANY NAME]

---

## Follow-up on negative rating

**Use when:** Customer submitted negative CSAT. Reach out personally.

---

Subject: Re: Your feedback

Hi [NAME],

I saw your support rating and wanted to reach out personally.

Sorry we didn't meet expectations. Can you tell me what went wrong? I want to make sure we do better.

No sales pitch, just trying to learn.

- [AGENT]
[Personal signature, not generic support]

---

## Thank you for positive feedback

**Use when:** Customer left great rating or comment. Acknowledge it.

---

Subject: Thanks for the kind words

Hi [NAME],

Saw your feedback. Thanks for taking the time - it means a lot to the team.

If you ever have a minute, a review on [APP STORE / G2 / CAPTERRA] helps other people find us. No pressure though.

[REVIEW LINK]

- [AGENT]

---

## Request for testimonial

**Use when:** Customer gave exceptional feedback, good candidate for testimonial.

---

Subject: Would you share your experience?

Hi [NAME],

You mentioned [SPECIFIC POSITIVE THING THEY SAID].

Would you be open to sharing that as a testimonial? Just a sentence or two about your experience. We'd feature it on our website with your name (or anonymously if you prefer).

Totally optional. Just thought I'd ask since your feedback was so specific and helpful.

Either way, thanks for being a customer.

- [AGENT]

---

## Survey reminder (if no response)

**Use when:** Sent survey 3 days ago, no response, want another try.

---

Subject: Re: Quick question about your support experience

Hi [NAME],

Following up on my earlier note. Did you have a chance to rate your support experience?

[SATISFIED] | [UNSATISFIED]

One click, takes 2 seconds.

No worries if not - just helps us improve.

- [COMPANY NAME] Support

---

## Implementation notes

**Survey timing:**
- Send within 1 hour of resolution (while experience is fresh)
- Don't send if ticket took more than 2 weeks (too much time passed)
- Don't send for tickets closed as spam/duplicate

**Survey frequency:**
- Max 1 survey per customer per week
- Don't survey same customer for minor follow-up tickets

**Response handling:**
- Route negative ratings to senior support for follow-up
- Aggregate positive feedback in team channel weekly
- Track CSAT trends in support_metrics dashboard

**Button implementation:**
- Use one-click rating if possible (no login required)
- Store rating with ticket ID for correlation
- Allow optional comment after rating click
