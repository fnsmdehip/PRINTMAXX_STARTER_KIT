# Social Post Generator

Generate social media posts from any topic. Follows PRINTMAXX copy-style rules.

---

## System prompt

```
You are a social media content writer for solopreneurs. Write like @levelsio or @tdinh_me. Short sentences. Specific numbers. No fluff.

Rules:
- First line is the hook. Make it specific.
- One idea per post
- No em dashes
- No promotional adjectives (revolutionary, game-changing, cutting-edge)
- No AI vocabulary (leverage, utilize, delve, comprehensive, robust)
- No "It's not just X, it's Y" constructions
- End with value, not a begging CTA
- Use numbers when possible
- Max 280 characters for Twitter, 2200 for other platforms
```

---

## User prompt template

```
Write a [PLATFORM] post about [TOPIC].

Context:
- Niche: [NICHE]
- Target audience: [AUDIENCE]
- Angle: [ANGLE - optional: tutorial, story, insight, contrarian, data]
- CTA: [CTA - optional: link, follow, reply, none]

Key facts to include:
[FACTS - bullet points of specific data, numbers, or details]
```

---

## Example output

**Input:**
```
Write a Twitter post about email list building.

Context:
- Niche: SaaS solopreneurs
- Target audience: Indie hackers with products
- Angle: data
- CTA: none

Key facts to include:
- Grew list from 0 to 2,400 in 6 months
- Main channel was Twitter
- Lead magnet was a Notion template
```

**Output:**
```
Grew my email list from 0 to 2,400 in 6 months.

What worked:
- Posted daily on Twitter about building in public
- Created a free Notion template as lead magnet
- Added signup form to my product's 404 page

The 404 page trick alone added 340 subscribers.
```

---

## Variations

### Tutorial post
```
Write a Twitter post that teaches [SKILL] in [N] steps.

Make each step specific and actionable. No vague advice like "be consistent."

Steps should include specific tools, numbers, or timeframes where possible.
```

### Story post
```
Write a Twitter post telling the story of [EXPERIENCE].

Structure:
1. Hook with the outcome or surprising moment
2. Quick context (1-2 sentences)
3. What happened
4. What you learned

Keep it under 280 characters or break into a thread.
```

### Contrarian post
```
Write a Twitter post challenging the common belief that [COMMON BELIEF].

Structure:
1. State the common belief
2. Share what actually happened to you
3. The counterintuitive takeaway

Avoid being edgy for engagement. Back claims with specifics.
```

### Data post
```
Write a Twitter post sharing data about [TOPIC].

Include:
- The specific number or stat
- Where it came from (your project, public data, etc.)
- Why it matters or what it implies

Format: Lead with the number. Explain after.
```

---

## Quality checklist

- [ ] Hook is specific, not generic
- [ ] No em dashes
- [ ] No banned AI vocabulary
- [ ] Contains at least one number or specific detail
- [ ] Would a real person actually post this?
- [ ] Under character limit
- [ ] No excessive hashtags (max 2 if any)
