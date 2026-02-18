# Brainstormer

Generate ideas across business areas. Outputs structured idea lists with evaluation.

---

## System prompt

```
You are a creative strategist helping solopreneurs generate ideas. You produce lots of ideas first (quantity), then help evaluate them (quality).

Approach:
- Generate many ideas before evaluating
- Mix obvious and non-obvious options
- Consider the solopreneur's constraints
- Provide evaluation criteria
- Highlight top picks with rationale

Output format:
- Many ideas organized by category
- Brief description of each
- Evaluation matrix
- Top recommendations
```

---

## User prompt template

```
Generate ideas for [TOPIC].

Context:
- Business: [BUSINESS]
- Goal: [GOAL]
- Constraints: [CONSTRAINTS - time, money, skills]

Parameters:
- Number of ideas: [COUNT - e.g., 20, 50]
- Types: [TYPES - e.g., content ideas, product ideas, growth tactics]
- Risk tolerance: [RISK - conservative, moderate, experimental]

What's worked before:
[PAST_WINS - if any]

What to avoid:
[AVOID - things you've tried that didn't work]
```

---

## Example output

**Input:**
```
Generate ideas for content to create this quarter.

Context:
- Business: SaaS tool for freelancers to track time
- Goal: Build audience and drive trial signups
- Constraints: 5 hours/week for content, no video equipment, can write

Parameters:
- Number of ideas: 30
- Types: Blog posts, social content, lead magnets
- Risk tolerance: Moderate (some experiments ok)

What's worked before:
- "How I landed my first freelance client" got good engagement
- Comparison posts drive trials
- Templates perform well as lead magnets

What to avoid:
- Generic productivity tips (too competitive)
- "Top 10 time tracking apps" (we'd rank ourselves, feels biased)
```

**Output:**

```
## Content brainstorm: Q1 content ideas

### Blog post ideas (15)

**How-to/Tutorial:**
1. How to set your freelance rates using time data
2. How to track time without it feeling like surveillance
3. How to calculate your true hourly rate (including admin)
4. How to use time tracking to identify your most profitable clients
5. How to track project time across multiple freelance gigs

**Story/Experience:**
6. What I learned tracking every hour for 30 days
7. How a freelancer doubled their effective rate with one change
8. The time tracking mistake that cost me $5,000
9. Why I stopped billing hourly (and what I do now)
10. How top-earning freelancers manage their time differently

**Data/Research:**
11. [Survey] How much do freelancers actually work per week?
12. Freelance income vs hours: What the data shows
13. The most undercharged services in freelancing (with data)

**Comparison/Alternatives:**
14. Spreadsheet vs dedicated time tracking: Which is better?
15. Manual vs automatic time tracking: Pros and cons

**Contrarian:**
16. Why some freelancers shouldn't track time
17. The productivity advice that backfires for freelancers

---

### Social content ideas (10)

**Threads:**
18. "I tracked my time for 90 days. Here's what I found." (data thread)
19. "How to go from $50/hour to $150/hour as a freelancer" (rate thread)
20. "The freelance time audit: A step-by-step process" (how-to thread)

**Single posts:**
21. Poll: "Do you track your freelance hours?" (engagement)
22. "Your effective hourly rate isn't what you charge" (insight)
23. Screenshot: Real time tracking data with lessons (transparency)
24. "The 30% rule for freelance admin time" (tip)
25. "What 100 freelancers told us about their biggest time wasters" (data)

**Carousels:**
26. "5 signs you're undercharging (according to your time data)"
27. "How to set up time tracking that doesn't suck"

---

### Lead magnet ideas (5)

28. **Freelance rate calculator spreadsheet**
    - Input hours and expenses, output true hourly rate
    - Low effort, high value

29. **30-day time tracking challenge template**
    - Notion or spreadsheet template
    - Daily prompts and weekly review

30. **"The Freelance Time Audit" PDF guide**
    - 5-page guide to analyzing where time goes
    - Includes worksheets

31. **Client profitability calculator**
    - Track time per client, calculate actual profit
    - Direct tie to product use case

32. **Weekly time review template**
    - Simple one-page review
    - Could be Notion, Google Doc, or PDF

---

### Evaluation criteria

| Criteria | Weight | Description |
|----------|--------|-------------|
| Effort | 25% | How much time to create? |
| SEO potential | 25% | Can this rank in search? |
| Conversion potential | 25% | Will this drive trials? |
| Differentiation | 15% | Is this unique to us? |
| Engagement potential | 10% | Will this get shares/discussion? |

---

### Evaluation matrix (top ideas)

| Idea | Effort | SEO | Conversion | Diff | Engagement | Score |
|------|--------|-----|------------|------|------------|-------|
| #1 Rate setting | 3/5 | 5/5 | 5/5 | 4/5 | 3/5 | 4.2 |
| #4 Profitable clients | 3/5 | 4/5 | 5/5 | 5/5 | 3/5 | 4.1 |
| #28 Rate calculator | 3/5 | 3/5 | 5/5 | 4/5 | 4/5 | 3.9 |
| #11 Survey data | 5/5 | 4/5 | 3/5 | 5/5 | 5/5 | 3.9 |
| #18 90-day thread | 2/5 | 2/5 | 4/5 | 4/5 | 5/5 | 3.4 |
| #31 Client profit calc | 2/5 | 2/5 | 5/5 | 5/5 | 3/5 | 3.4 |

(Lower effort = higher score, ratings are inverted for scoring)

---

### Top recommendations

**Priority 1: Create first**

1. **Blog: How to set your freelance rates using time data** (#1)
   - High SEO potential ("freelance rate calculator" searches)
   - Directly connects to product value prop
   - Can include embedded lead magnet
   - Est. effort: 4 hours

2. **Lead magnet: Freelance rate calculator spreadsheet** (#28)
   - Pairs with blog post above
   - High perceived value, moderate effort
   - Direct pathway to trial signup
   - Est. effort: 3 hours

**Priority 2: Create second**

3. **Blog: How to identify your most profitable clients** (#4)
   - Differentiating angle
   - Business case for time tracking
   - Can include case study/example
   - Est. effort: 4 hours

4. **Thread: 90-day time tracking results** (#18)
   - High engagement potential
   - Can use your own data
   - Drives traffic to blog/product
   - Est. effort: 1 hour

**Priority 3: Experiment**

5. **Survey: How much do freelancers actually work?** (#11)
   - High effort but high payoff
   - Creates original data for multiple pieces
   - Good for backlinks and PR
   - Est. effort: 8-10 hours total

---

### Content calendar suggestion

| Week | Content | Type |
|------|---------|------|
| 1 | Rate calculator lead magnet | Lead magnet |
| 2 | How to set freelance rates (blog) | Blog |
| 3 | 90-day tracking thread | Social |
| 4 | Profitable clients (blog) | Blog |
| 5-6 | Survey creation and promotion | Research |
| 7 | Survey results (blog) | Blog |
| 8 | Survey data thread | Social |

---

### Ideas saved for later

**Good but lower priority:**
- #6 (30 days tracking) - Similar to #18, do one first
- #29 (30-day challenge) - Good lead magnet for later
- #12 (income vs hours) - Needs survey data first

**Experimental:**
- #16 (why not to track) - Contrarian, risky but could work
- #9 (stopped billing hourly) - Only if you have a real story

**Skip for now:**
- #14, #15 (comparison) - Works but less differentiating
- #17 (productivity backfires) - Too generic
```

---

## Variations

### Product ideas
```
Generate product ideas for [NICHE/AUDIENCE].

Context:
- Skills: [YOUR SKILLS]
- Audience: [WHO YOU CAN REACH]
- Budget: [WHAT YOU CAN INVEST]

Generate [N] ideas across:
- Digital products
- Services
- Tools
- Templates
- Courses

Evaluate for: Effort, demand, competition, margin
```

### Growth tactics
```
Generate growth ideas for [PRODUCT].

Current state:
- Users/customers: [COUNT]
- Channels working: [CHANNELS]
- Budget: [BUDGET]

Generate [N] ideas for:
- Organic growth
- Paid acquisition
- Partnerships
- Viral loops
- Content

Rank by: Cost, scalability, timeline
```

### Monetization ideas
```
Generate monetization ideas for [AUDIENCE/ASSET].

What you have:
- Audience: [SIZE AND TYPE]
- Content: [WHAT YOU'VE CREATED]
- Skills: [WHAT YOU CAN DO]

Generate ideas for:
- Products to sell
- Services to offer
- Affiliate opportunities
- Sponsorships
- Licensing

Evaluate for: Revenue potential, effort, fit
```

### Problem-solving ideas
```
Generate solutions for [PROBLEM].

Constraints:
- Time: [AVAILABLE TIME]
- Money: [BUDGET]
- Other: [OTHER CONSTRAINTS]

Generate [N] ideas from:
- Quick fixes
- Medium-term solutions
- Long-term systems
- Unconventional approaches

Rank by: Speed, effectiveness, sustainability
```

---

## Brainstorming principles

**Quantity first:**
- Generate many ideas before judging
- Bad ideas lead to good ideas
- Don't self-censor early

**Diverse perspectives:**
- What would [competitor] do?
- What would a beginner try?
- What's the opposite approach?

**Constraints as prompts:**
- What if you had half the time?
- What if you had no budget?
- What if you could only do one thing?

**Build on ideas:**
- Combine two mediocre ideas
- Take a good idea further
- Apply an idea from another industry

---

## Quality checklist

- [ ] Generated requested number of ideas
- [ ] Ideas are diverse (not variations of same thing)
- [ ] Each idea has brief description
- [ ] Evaluation criteria clear
- [ ] Top recommendations highlighted
- [ ] Rationale for recommendations provided
- [ ] Implementation considerations noted
- [ ] Would this give someone enough to work with?
