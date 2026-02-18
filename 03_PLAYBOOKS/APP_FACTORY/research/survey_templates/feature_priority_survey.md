# Feature Priority Survey Template

Let users vote on what to build next.

**When to use:** Quarterly planning, roadmap prioritization
**Target responses:** 50+
**Best timing:** Before major planning cycles

---

## Survey structure

### Introduction

> We're planning what to build next and want your input. This takes about 3 minutes.
>
> Your feedback directly influences our roadmap.

---

### Question 1: Current satisfaction

> How satisfied are you with [product] today?

- Very satisfied
- Somewhat satisfied
- Neutral
- Somewhat dissatisfied
- Very dissatisfied

---

### Question 2: Feature importance (Max-Diff or ranking)

**Option A: Forced ranking (for 5-8 features)**

> Rank these potential features from most to least important to you:

Drag to reorder:
- [ ] Feature A description
- [ ] Feature B description
- [ ] Feature C description
- [ ] Feature D description
- [ ] Feature E description

**Option B: Max-Diff (for 8+ features)**

Show sets of 4 features at a time:

> Of these four features, which is MOST important and which is LEAST important to you?

| Feature | Most important | Least important |
|---------|----------------|-----------------|
| Feature A | O | O |
| Feature B | O | O |
| Feature C | O | O |
| Feature D | O | O |

Repeat with different sets until all features covered.

**Option C: Simple rating (easiest but less accurate)**

> How important is each feature to you?

| Feature | Not important | Slightly | Moderately | Very | Critical |
|---------|---------------|----------|------------|------|----------|
| Feature A | O | O | O | O | O |
| Feature B | O | O | O | O | O |
| Feature C | O | O | O | O | O |

---

### Question 3: Kano model questions (optional but powerful)

For each potential feature, ask two questions:

**Functional question:**
> If [feature] were added, how would you feel?

- I would like it
- I expect it
- I'm neutral
- I can tolerate it
- I dislike it

**Dysfunctional question:**
> If [feature] were NOT added, how would you feel?

- I would like it
- I expect it
- I'm neutral
- I can tolerate it
- I dislike it

**Kano categorization:**
| | Like | Expect | Neutral | Tolerate | Dislike |
|---|---|---|---|---|---|
| **If has: Like** | Q | A | A | A | O |
| **If has: Expect** | R | I | I | I | M |
| **If has: Neutral** | R | I | I | I | M |
| **If has: Tolerate** | R | I | I | I | M |
| **If has: Dislike** | R | R | R | R | Q |

- **M** = Must-have (expected, no satisfaction if missing)
- **O** = One-dimensional (more = better)
- **A** = Attractive (delighter, not expected)
- **I** = Indifferent (don't care)
- **R** = Reverse (actively don't want)
- **Q** = Questionable (confused response)

---

### Question 4: Willingness to pay

> Would you pay more for any of these features?

- Yes, I'd pay $X/month more for [feature]
- No, I wouldn't pay more
- I'd pay more but only if [open text]

---

### Question 5: Missing features

> Is there a feature we didn't mention that you really want?

_Open text field_

---

### Question 6: Segment identification

> Which best describes you?

(Include relevant segments for your product)

- Segment A
- Segment B
- Segment C

---

## Analysis template

### Response summary

**Survey period:**
**Total responses:**
**Completion rate:**

### Feature ranking results

| Rank | Feature | Score | % chose as top 3 |
|------|---------|-------|------------------|
| 1 | | | |
| 2 | | | |
| 3 | | | |
| 4 | | | |
| 5 | | | |

### Segment comparison

| Feature | Segment A rank | Segment B rank | Difference |
|---------|----------------|----------------|------------|
| | | | |
| | | | |

### Kano classification summary

| Feature | Category | Priority implication |
|---------|----------|---------------------|
| | Must-have | Ship before everything else |
| | One-dimensional | Include in roadmap |
| | Attractive | Delighter, lower priority |
| | Indifferent | Don't build |

### Open-ended themes

| Requested feature | Frequency | Notes |
|-------------------|-----------|-------|
| | | |
| | | |

---

## Prioritization framework

After survey results, use this matrix:

### Impact vs. Effort

|  | Low effort | High effort |
|--|------------|-------------|
| **High impact** | DO FIRST | PLAN CAREFULLY |
| **Low impact** | QUICK WIN | DON'T DO |

### Priority score formula

```
Priority = (User demand score x User segment weight) / Effort estimate
```

**User demand score:** From survey ranking (1-10)
**Segment weight:** How important is this segment? (1-3)
**Effort estimate:** T-shirt size converted (S=1, M=2, L=4, XL=8)

---

## Presenting results to stakeholders

### Summary slide

**Users want (top 3):**
1. Feature X - 67% ranked in top 3
2. Feature Y - 54% ranked in top 3
3. Feature Z - 48% ranked in top 3

**Users don't want:**
- Feature W - 72% ranked last

**Segment differences:**
- Power users prioritize [X]
- New users prioritize [Y]

### Recommendation

Based on user input and effort estimates:

| Q1 | Q2 | Q3 |
|----|----|----|
| Feature X | Feature Y | Feature Z |

---

## Survey best practices

### Feature descriptions

**Bad:** "Improved dashboard"
**Good:** "See your weekly progress with charts showing trends over time"

Be specific. Users can't prioritize vague concepts.

### Number of features

- Too few (under 5): Not useful
- Sweet spot: 6-10 features
- Too many (15+): Survey fatigue

### Avoid bias

- Randomize feature order
- Don't "sell" features in descriptions
- Include some features you know users want (calibration)
- Include some you expect low interest in

### Response incentive

- Small thank you (discount code, free month)
- Early access to winning feature
- "You helped shape our roadmap" recognition
