# NPS Survey Template

Net Promoter Score measurement.

**When to use:** Monthly or quarterly for existing users
**Target responses:** 100+ for statistical significance
**Best timing:** After 30+ days of usage, not during onboarding

---

## The core NPS question

**Question 1 (Required):**
> On a scale of 0-10, how likely are you to recommend [product] to a friend or colleague?

| 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---|---|---|---|---|---|---|---|---|---|
| Not at all likely | | | | | Neutral | | | | | Extremely likely |

---

## Scoring

**Promoters (9-10):** Loyal enthusiasts who will refer others
**Passives (7-8):** Satisfied but not enthusiastic
**Detractors (0-6):** Unhappy users who can damage your brand

**NPS Formula:**
```
NPS = % Promoters - % Detractors
```

**Example:**
- 100 responses
- 40 Promoters (40%)
- 35 Passives (35%)
- 25 Detractors (25%)
- NPS = 40 - 25 = **+15**

---

## Benchmark interpretation

| NPS | Rating | What it means |
|-----|--------|---------------|
| 70+ | Excellent | World-class. Apple/Tesla territory |
| 50-69 | Great | Strong product-market fit |
| 30-49 | Good | Solid foundation, room to improve |
| 0-29 | Okay | Work to do on user satisfaction |
| Below 0 | Poor | More detractors than promoters. Urgent fix |

---

## Follow-up questions

**Question 2 (Always include):**
> What's the primary reason for your score?

_Open text field_

This is where you get actual insights.

---

**Question 3 (Optional - segment by score):**

**For Promoters (9-10):**
> What do you like most about [product]?

**For Passives (7-8):**
> What would it take to make you a 9 or 10?

**For Detractors (0-6):**
> What's the biggest problem we need to fix?

---

**Question 4 (Optional - feature feedback):**
> Which feature do you use most often?
- Feature A
- Feature B
- Feature C
- Feature D
- Other: _____

---

## Survey implementation

### Email template

**Subject:** Quick question about [product] (30 seconds)

**Body:**
> Hi [First Name],
>
> We're working to improve [product] and would love your quick feedback.
>
> **One question:** How likely are you to recommend [product] to a friend?
>
> [0] [1] [2] [3] [4] [5] [6] [7] [8] [9] [10]
>
> Click a number above to respond instantly.
>
> Thanks,
> [Your name]

---

### In-app implementation

Best practices:
- Trigger after meaningful engagement (not immediately after signup)
- Don't interrupt critical workflows
- Show once every 90 days max
- Allow dismissal
- Mobile-friendly tap targets

---

## Analysis template

### Raw data

| Date | Score | Category | Reason |
|------|-------|----------|--------|
|      |       |          |        |
|      |       |          |        |

### Summary metrics

**Survey period:** [Date range]
**Total responses:**
**Response rate:**

| Category | Count | Percentage |
|----------|-------|------------|
| Promoters (9-10) | | |
| Passives (7-8) | | |
| Detractors (0-6) | | |

**NPS Score:**

**Trend vs. last period:** +/- X points

---

### Theme analysis

Code open-ended responses into categories:

**Promoter themes:**
| Theme | Frequency | Example quote |
|-------|-----------|---------------|
|       |           |               |
|       |           |               |

**Detractor themes:**
| Theme | Frequency | Example quote |
|-------|-----------|---------------|
|       |           |               |
|       |           |               |

---

### Segment analysis

Break down NPS by user segments:

| Segment | NPS | n | Insight |
|---------|-----|---|---------|
| New users (<30 days) | | | |
| Established (30-90 days) | | | |
| Veterans (90+ days) | | | |
| Free tier | | | |
| Paid tier | | | |

---

## Action framework

### For Promoters
- Ask for referrals
- Request reviews/testimonials
- Invite to beta programs
- Feature their success stories

### For Passives
- Follow up with targeted improvements
- Ask what would make them a 10
- Monitor for churn risk

### For Detractors
- Personal outreach from support
- Understand specific issues
- Offer to make it right
- Track if they convert to promoter after fix

---

## NPS cadence

**Quarterly:** Best for most products
- Enough time between surveys
- Tracks trends over time
- Not annoying

**Monthly:** Only if:
- Shipping features rapidly
- Small user base needs faster signal
- Short subscription cycles

**After key moments:**
- Post-onboarding (day 7 or 14)
- After major feature launch
- After support interaction

---

## Common mistakes

1. **Surveying too often** - Once per quarter max
2. **Wrong timing** - Not during onboarding
3. **No follow-up** - Detractors need outreach
4. **Ignoring passives** - They're churn risks too
5. **Just tracking score** - Read the open text responses
6. **No segmentation** - Average NPS hides patterns
