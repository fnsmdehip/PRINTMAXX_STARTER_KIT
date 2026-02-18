# Pain Point Finder

Extract pain points from reviews, forums, and communities. Outputs validated customer problems.

---

## System prompt

```
You are a customer research analyst. You extract pain points from raw customer feedback and identify patterns that reveal product and content opportunities.

Approach:
- Look for recurring complaints, not one-off issues
- Distinguish between symptoms and root causes
- Prioritize by frequency and intensity
- Connect pain points to opportunities

Output format:
- Categorized pain points with examples
- Frequency indicators
- Intensity assessment
- Opportunity mapping
- Validation recommendations
```

---

## User prompt template

```
Extract pain points from [SOURCE].

Source details:
- Source type: [TYPE - reviews, forum posts, social media, interviews]
- Platform: [PLATFORM - G2, Reddit, Twitter, etc.]
- Product/topic: [PRODUCT_OR_TOPIC]

Analysis goals:
- What problems are people facing?
- How frequently do these come up?
- How painful are they (intensity)?
- What solutions are they requesting?

My context:
- My product/service: [MY_PRODUCT]
- How I might help: [MY_SOLUTION]
- What I'm looking for: [GOAL - content ideas, feature ideas, positioning]

Data to analyze:
[DATA - paste reviews, posts, or describe what to analyze]
```

---

## Example output

**Input:**
```
Extract pain points from Calendly reviews.

Source details:
- Source type: reviews
- Platform: G2 and Capterra
- Product/topic: Calendly scheduling software

Analysis goals:
- What problems are people facing with Calendly?
- How frequently do these come up?
- How painful are they?
- What solutions are they requesting?

My context:
- My product/service: Building a simple scheduling tool
- How I might help: Simpler alternative with fewer features
- What I'm looking for: Feature gaps and positioning opportunities

Data to analyze:
[Sample of 50 negative reviews from G2 and Capterra]
```

**Output:**

```
## Pain point analysis: Calendly reviews

### Analysis summary

Analyzed 50 negative/mixed reviews from G2 and Capterra. Most users rate Calendly positively overall, but consistent pain points emerge in negative reviews.

**Key finding:** Most complaints aren't about core scheduling. They're about complexity, pricing, and integration friction.

---

### Pain point category 1: Pricing and value

**Frequency:** Very high (mentioned in 28/50 reviews)
**Intensity:** High (users express frustration, consider switching)

**Specific pain points:**

| Pain Point | Frequency | Example Quote |
|------------|-----------|---------------|
| Free tier limitations | 15 mentions | "The free version is basically a demo. Can't do anything useful." |
| Price jump from free to paid | 12 mentions | "Goes from $0 to $10/month with nothing in between." |
| Features locked behind higher tiers | 8 mentions | "Need the $15 plan just to remove branding." |
| Per-user pricing for teams | 6 mentions | "Gets expensive fast when you have 5+ people." |

**Root cause:** Calendly's freemium model is optimized for upsell, not user satisfaction.

**Opportunity:**
- Position on transparent, fair pricing
- Offer a meaningful free tier or low-cost paid tier ($5/mo)
- No per-seat pricing for small teams

---

### Pain point category 2: Complexity and feature bloat

**Frequency:** High (mentioned in 18/50 reviews)
**Intensity:** Medium (users work around it but complain)

**Specific pain points:**

| Pain Point | Frequency | Example Quote |
|------------|-----------|---------------|
| Too many settings/options | 10 mentions | "Spent an hour just trying to set up my first event type." |
| Confusing workflows | 8 mentions | "The routing logic makes my head hurt." |
| Features I'll never use | 6 mentions | "I just want a booking link. Don't need analytics." |
| Admin panel overwhelming | 5 mentions | "Dashboard looks like a cockpit." |

**Root cause:** Calendly has grown to serve enterprise, leaving simple use cases behind.

**Opportunity:**
- "One screen setup" positioning
- Fewer features, done well
- Target users who just need "schedule a call"

---

### Pain point category 3: Integration issues

**Frequency:** Medium-high (mentioned in 14/50 reviews)
**Intensity:** High (blocks workflow, causes missed meetings)

**Specific pain points:**

| Pain Point | Frequency | Example Quote |
|------------|-----------|---------------|
| Calendar sync delays | 7 mentions | "Double booked because sync took 5 minutes." |
| Zoom integration issues | 5 mentions | "Meeting links don't always get added." |
| Limited native integrations | 4 mentions | "Need Zapier for everything, which costs more." |
| Breaking after updates | 3 mentions | "Google Calendar integration broke twice this year." |

**Root cause:** Complex integration architecture creates reliability issues.

**Opportunity:**
- Focus on 2-3 integrations done perfectly
- Real-time sync as differentiator
- Built-in integrations vs Zapier dependency

---

### Pain point category 4: Branding and customization

**Frequency:** Medium (mentioned in 10/50 reviews)
**Intensity:** Medium (annoying but not dealbreaker)

**Specific pain points:**

| Pain Point | Frequency | Example Quote |
|------------|-----------|---------------|
| Can't remove Calendly branding (free) | 6 mentions | "Looks unprofessional with their logo on my page." |
| Limited design customization | 4 mentions | "Colors don't match my brand at all." |
| Booking page looks generic | 3 mentions | "Every consultant has the same looking page." |

**Root cause:** Calendly uses branding removal as upsell mechanism.

**Opportunity:**
- No branding on free tier (or minimal)
- Better default designs
- Easy customization without premium

---

### Pain point category 5: Customer support

**Frequency:** Lower but intense (mentioned in 8/50 reviews)
**Intensity:** High when it occurs

**Specific pain points:**

| Pain Point | Frequency | Example Quote |
|------------|-----------|---------------|
| Slow response times | 4 mentions | "Waited 3 days for a response to a billing issue." |
| No phone support | 3 mentions | "Couldn't get anyone on the phone." |
| Unhelpful responses | 2 mentions | "Just sent me a link to docs I'd already read." |

**Root cause:** Calendly scaled support down as they grew.

**Opportunity:**
- Responsive support as differentiator
- Personal touch (solopreneur advantage)

---

### Pain point by user segment

**Solopreneurs/freelancers:**
- Price sensitivity (highest concern)
- Branding on free tier
- Just need basic scheduling

**Small teams (2-10):**
- Per-user pricing adds up
- Admin overhead for setup
- Integration reliability

**Power users:**
- Not enough customization
- Workflow limitations
- Want more control

**Opportunity:** Target solopreneurs specifically. They're underserved and price-sensitive.

---

### Requested features not addressed

| Request | Frequency | Notes |
|---------|-----------|-------|
| Cheaper paid tier | 8 mentions | Gap between $0 and $10 |
| Better mobile experience | 5 mentions | Admin app is clunky |
| Offline booking capability | 3 mentions | For areas with poor connection |
| SMS reminders on all plans | 4 mentions | Currently premium only |
| Simple group scheduling | 4 mentions | Current solution is complicated |

---

### Opportunity mapping

**Content opportunities:**
- "Best Calendly alternatives for freelancers" (target pricing pain)
- "Simple scheduling tools that just work" (target complexity)
- "How to set up scheduling in 5 minutes" (position vs Calendly's complexity)

**Product opportunities:**
- Simple scheduling tool with 1 event type focus
- Flat pricing ($5/mo unlimited)
- No branding removal upsell
- Real-time calendar sync as core feature

**Positioning opportunities:**
- "The scheduling tool that doesn't nickel and dime you"
- "One link. One purpose. Zero confusion."
- "Built for people who just want to schedule calls"

---

### Validation recommendations

**Before building, validate:**
1. Interview 5-10 freelancers who've tried Calendly
   - Confirm pricing is the real blocker
   - Understand what "simple" means to them
   - Ask about switching triggers

2. Test positioning with landing page
   - "Simple scheduling for freelancers"
   - Measure signup intent before building

3. Check competitor moves
   - Is anyone else targeting this gap?
   - Cal.com, SavvyCal, TidyCal positioning

**Red flag signals:**
- If users say "Calendly is fine, just wish it was cheaper" = price objection
- If users say "I hate using Calendly" = experience problem (better opportunity)

---

### Summary: Top 3 actionable insights

1. **Pricing gap exists:** Users want something between free and $10/mo
   - Action: Consider $5/mo positioning

2. **Complexity is a real problem:** Users feel overwhelmed
   - Action: Position as radically simple

3. **Solopreneurs are underserved:** They don't need team features
   - Action: Build specifically for one-person use case
```

---

## Variations

### Reddit pain point extraction
```
Extract pain points from [SUBREDDIT] about [TOPIC].

Search for:
- Complaint posts
- "Wish there was..." requests
- "I hate when..." statements
- Comparison/alternative requests

Output: Categorized pain points with post examples and opportunity assessment
```

### Interview synthesis
```
Synthesize pain points from [N] customer interviews.

For each pain point:
- How many people mentioned it?
- Exact quotes
- Severity (nice-to-fix vs must-fix)
- Current workarounds

Output: Prioritized pain point list with validation status
```

### Twitter complaint mining
```
Find pain points from Twitter about [PRODUCT/TOPIC].

Look for:
- Direct complaints and frustrations
- Sarcastic comments about the experience
- "Does anyone else..." questions
- Requests for alternatives

Output: Tweet examples categorized by pain point theme
```

---

## Quality checklist

- [ ] Pain points categorized clearly
- [ ] Frequency indicated for each
- [ ] Intensity/severity assessed
- [ ] Direct quotes included
- [ ] Root causes identified
- [ ] Opportunities mapped
- [ ] Validation steps recommended
- [ ] Would this help prioritize what to build or write about?
