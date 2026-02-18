# Day 1 Follow-up Email

Send 24 hours after launch (T+24h).

---

## Email details

**From:** [Your name] <hello@yourdomain.com>
**To:**
- Segment A: People who opened launch email but didn't click
- Segment B: People who didn't open launch email
**Subject options:**
- "Quick update on [App Name]"
- "Did you get a chance to try it?"
- "Day 1 numbers (surprised me)"
- "Still free for [X] more days"

---

## Email body

### Version A (For openers who didn't click)

```
Subject: Quick update on [App Name]

[First name],

Yesterday I launched [App Name]. You opened my email (thanks!) but I noticed you didn't download it yet.

Totally get it. New apps are a commitment.

Here's the quick version:

[App Name] = [main benefit in 5 words or less]

Takes 2 minutes to try. No account required.

[Single call-to-action button: "Try [App Name]"]

If you tried it and had issues, reply to this email. I'm personally fixing everything this week.

[Your name]
```

### Version B (For non-openers)

```
Subject: Did you see this?

[First name],

Yesterday I launched [App Name].

In case you missed it: [one-sentence description]

[X] people downloaded it on day 1.

Here's what they're saying:
- "[Quick testimonial]" - [Name]

Try it free: [link]

No spam from me, just wanted to make sure you saw it.

[Your name]
```

### Version C (Results-focused)

```
Subject: Day 1 numbers

[First name],

Yesterday [App Name] launched.

Day 1 results:
- [X] downloads
- [Y] positive reviews
- [Z] feature requests (already working on them)

The feedback surprised me. People actually [unexpected insight].

Haven't tried it yet? Here's your link: [link]

Free for [X] more days.

[Your name]

P.S. If you downloaded yesterday, how's it going? Reply and let me know.
```

---

## Email settings

- **Send time:** Same time as launch email (24h later)
- **Segment:** Split by engagement with launch email
- **Exclude:** People who already clicked/downloaded
- **Track:** Opens, clicks, replies

---

## Segmentation logic

```
IF opened_launch_email = true AND clicked_link = false
  THEN send Version A

IF opened_launch_email = false
  THEN send Version B

IF clicked_link = true
  THEN skip this email (they already engaged)
```

---

## Pre-send checklist

- [ ] Correct segment selected
- [ ] Excludes people who already downloaded
- [ ] Links updated if changed since launch
- [ ] Real testimonials used (no fake ones)
- [ ] Numbers are accurate
- [ ] Reply-to goes to monitored inbox

---

Created: 2026-01-21
