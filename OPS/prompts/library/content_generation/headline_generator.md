# Headline Generator

Generate A/B test headlines for any content. Follows PRINTMAXX copy-style rules.

---

## System prompt

```
You are a headline specialist. You write headlines that get clicks without being clickbait.

Principles:
- Specific beats vague
- Numbers work
- Questions engage
- How-to converts
- Curiosity gaps drive clicks (but deliver on the promise)

Rules:
- No em dashes
- No AI vocabulary
- No promotional adjectives (revolutionary, ultimate, definitive)
- Under 60 characters for SEO (or specify limit)
- Sentence case, not Title Case
- Must be testable (clear differences between variations)
```

---

## User prompt template

```
Generate [N] headline variations for [CONTENT_TYPE].

Topic: [TOPIC]
Target audience: [AUDIENCE]
Goal: [GOAL - clicks, shares, conversions, SEO]

Context:
- Platform: [PLATFORM - blog, email, landing page, ad]
- Character limit: [LIMIT - optional]
- Primary keyword: [KEYWORD - for SEO, optional]

Angles to explore:
[ANGLES - benefit, curiosity, how-to, number, question, negative]

Current headline (if rewriting):
[CURRENT - optional]
```

---

## Example output

**Input:**
```
Generate 10 headline variations for a blog post.

Topic: Building a profitable side project
Target audience: Developers who want passive income
Goal: SEO and clicks

Context:
- Platform: blog
- Character limit: 60
- Primary keyword: side project

Angles to explore:
- benefit, how-to, number, story, negative
```

**Output:**

```
---
HOW-TO ANGLE
---

1. How to build a side project that makes money
   (50 chars | Keyword: side project | Direct promise)

2. How I built a $500/month side project in 3 months
   (51 chars | Story hook with specific numbers)

---
NUMBER ANGLE
---

3. 7 side projects that actually make money in 2024
   (49 chars | List format, recency, "actually" adds skeptic appeal)

4. The $127/month side project I built in 2 weekends
   (52 chars | Specific revenue, specific timeframe)

5. 5 side project ideas for developers with full-time jobs
   (57 chars | Addresses time constraint)

---
BENEFIT ANGLE
---

6. Build a side project that pays your rent
   (42 chars | Concrete benefit, relatable)

7. Turn your coding skills into passive income
   (45 chars | Transformation, specific to audience)

---
CURIOSITY ANGLE
---

8. Why most side projects fail (and what to do instead)
   (55 chars | Negative hook with solution promise)

9. The side project strategy nobody talks about
   (47 chars | Curiosity gap)

---
NEGATIVE/CONTRARIAN ANGLE
---

10. Stop building side projects that don't make money
    (51 chars | Direct challenge, implies solution)

---
TESTING PAIRS
---

Test A vs B:
- #1 vs #2: Generic how-to vs specific story
- #3 vs #10: List vs challenge
- #4 vs #6: Revenue focus vs lifestyle benefit

Winner criteria:
- CTR for engagement
- Time on page for relevance
- Bounce rate for headline/content match
```

---

## Variations

### Email subject lines
```
Generate [N] email subject line variations.

Topic: [TOPIC]
Email type: [TYPE - newsletter, promo, announcement]
Goal: [GOAL - open rate, clicks, replies]

Include:
- Character count (aim for 30-50)
- Preview text suggestion
- Personalization token placement if applicable

Test framework: 20% of list, 2-hour window, promote winner
```

### Landing page headlines
```
Generate [N] landing page headline variations.

Product: [PRODUCT]
Target: [AUDIENCE]
Goal: [GOAL - signups, purchases, demos]

For each headline provide:
- Main headline (H1)
- Supporting subheadline
- Why this angle might work

Prioritize clarity over cleverness. Visitor should know what this is in 3 seconds.
```

### Social post hooks
```
Generate [N] first-line hooks for social posts.

Topic: [TOPIC]
Platform: [PLATFORM]
Content type: [TYPE - thread, single post, carousel]

Requirements:
- Under 100 characters
- Must work standalone
- Should create curiosity or state a surprising fact

Include:
- The hook line
- What the rest of the post delivers
```

### Ad headlines
```
Generate [N] ad headline variations.

Product: [PRODUCT]
Platform: [PLATFORM]
Character limit: [LIMIT]

For each variation:
- Headline text
- Supporting text (25 chars)
- Angle used
- When to use (audience segment or test scenario)

Follow platform character limits exactly.
```

---

## Headline formulas

**How-to:**
- How to [achieve result]
- How I [achieved result] in [timeframe]
- How to [achieve result] without [common obstacle]

**Number:**
- [N] ways to [achieve result]
- [N] [things] that [benefit]
- The [N]-step [process] for [result]

**Question:**
- Want to [achieve result]?
- Why do [people] [struggle with X]?
- What if you could [achieve result]?

**Negative:**
- Why [common approach] doesn't work
- Stop [doing this] if you want [result]
- [N] mistakes that kill your [thing]

**Curiosity:**
- The [thing] nobody talks about
- What [successful people] know about [topic]
- The real reason [something happens]

**Specificity:**
- How [person] [achieved specific result]
- The [exact/specific] [thing] I use to [result]
- [Specific number] [thing] in [specific time]

---

## Testing framework

**What to test:**
- Angle (benefit vs curiosity vs how-to)
- Specificity (numbers vs vague)
- Length (short vs medium)
- Format (question vs statement)

**Sample size:**
- Email: 20% of list minimum, or 1,000 per variation
- Ads: $50-100 per variation minimum
- Blog: 1,000 pageviews per variation

**Metrics:**
- Email: Open rate (subject), click rate (body headline)
- Ads: CTR, then conversion rate
- Blog: CTR from search, time on page, bounce rate

---

## Quality checklist

- [ ] Under character limit
- [ ] Contains keyword (if SEO)
- [ ] No em dashes
- [ ] No banned AI vocabulary
- [ ] No promotional fluff
- [ ] Sentence case (not Title Case)
- [ ] Specific over vague
- [ ] Clear differences between variations
- [ ] Would you click this?
