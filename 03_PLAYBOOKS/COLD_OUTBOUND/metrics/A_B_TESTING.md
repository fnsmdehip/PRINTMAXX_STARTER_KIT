# A/B testing for cold outbound

What to test, how to test, and how to interpret results.

## Why A/B test

Small improvements compound:
- Improve open rate from 45% to 55% = 22% more people reading
- Improve reply rate from 3% to 4% = 33% more conversations
- Combined = 63% more replies from same volume

## What to test (in priority order)

### 1. Subject lines (highest impact on opens)

**Test elements:**
- Length (short vs medium)
- Personalization (with vs without name/company)
- Question vs statement
- Specific vs vague
- With vs without numbers

**Example tests:**
- A: "{{company}} + growth"
- B: "Quick question for {{firstName}}"

- A: "Your website"
- B: "{{company}}'s website conversion"

- A: "15 min call?"
- B: "Idea for {{company}}"

### 2. Opening line (impacts reply rate)

**Test elements:**
- Personalization depth
- Problem statement vs observation
- Question vs statement
- Compliment vs direct

**Example tests:**
- A: "Noticed {{company}} is growing fast..."
- B: "Quick question about your marketing..."

- A: "I help companies like {{company}} with..."
- B: "Most [their role]s I talk to struggle with..."

### 3. Call-to-action (impacts meeting rate)

**Test elements:**
- Calendar link vs "reply to this email"
- Specific time ask vs open-ended
- Low-commitment vs direct ask
- Question CTA vs statement CTA

**Example tests:**
- A: "Worth a 15-min call? Here's my calendar: [link]"
- B: "Worth a quick chat? Just reply and I'll send times."

- A: "Can you do Thursday at 2pm?"
- B: "What's your availability next week?"

### 4. Email length (impacts reply rate)

**Test elements:**
- Ultra-short (3-4 sentences)
- Short (5-7 sentences)
- Medium (8-10 sentences)
- Long (10+ sentences)

**Note:** Shorter almost always wins in cold email.

### 5. Offer/value proposition (impacts quality of replies)

**Test elements:**
- Different pain points emphasized
- Different outcomes promised
- Different proof points
- Free value vs direct pitch

### 6. Timing (send time)

**Test elements:**
- Morning vs afternoon
- Tuesday vs Thursday
- Early in sequence vs later

### 7. Sequence structure

**Test elements:**
- 3-email vs 5-email sequence
- Follow-up timing (2 days vs 4 days)
- Breakup email vs no breakup

## How to A/B test properly

### Sample size requirements

**Minimum for meaningful results:**
- Subject line test: 200+ sends per variant (400 total)
- Body copy test: 300+ sends per variant (600 total)
- CTA test: 300+ sends per variant

**Rule of thumb:**
Wait until you have 20+ of the desired action (opens for subject line, replies for copy) before drawing conclusions.

### Test one variable at a time

**Bad approach:**
- Variant A: Short subject + long email + calendar link CTA
- Variant B: Long subject + short email + "reply" CTA

You won't know what caused the difference.

**Good approach:**
- Variant A: "Quick question for {{firstName}}"
- Variant B: "{{company}} + [topic]"

Everything else identical.

### Random split

**How to split:**
- 50/50 split (most common)
- Or 80/20 if testing against proven winner
- Random assignment (not sequential)

**In Instantly/Smartlead:**
- Create two versions in sequence builder
- Tool automatically splits 50/50
- Sends randomly assigned

### Run test to completion

**Don't:**
- Check results after 1 day and declare winner
- Stop early because one looks better
- Change the test mid-stream

**Do:**
- Decide sample size beforehand
- Run until you hit that sample
- Then analyze results

## Statistical significance

### The problem with small samples

| Variant | Sent | Opens | Open Rate |
|---------|------|-------|-----------|
| A | 50 | 25 | 50% |
| B | 50 | 22 | 44% |

Is A really better? Maybe. Or maybe random chance.

### Simple significance check

**Quick rule:** Difference should be > 2x the noise level.

**Better check:** Use a significance calculator.

**Tools:**
- ABTestGuide.com/calc
- NeilPatel.com/ab-testing-calculator

Enter:
- Sample size A and B
- Conversions A and B
- Get significance percentage

**Aim for:** 95% confidence (p < 0.05)

### When you can skip statistics

If the difference is huge (50% vs 30%), you don't need stats. It's obviously significant.

If the difference is small (50% vs 48%), you need more data or accept you can't tell.

## A/B testing process

### Step 1: Choose what to test
Pick highest-impact variable (usually subject line first).

### Step 2: Create hypothesis
"I believe [change] will improve [metric] because [reason]."

Example: "I believe shorter subject lines will improve open rate because they display fully on mobile."

### Step 3: Create variants
- Control (current best performer or baseline)
- Treatment (the change you're testing)

### Step 4: Determine sample size
- Minimum 200 per variant for subject lines
- Minimum 300 per variant for body copy
- More is always better

### Step 5: Run the test
- Set up in email tool
- Start campaign
- Don't peek daily (wait for completion)

### Step 6: Analyze results
- Calculate rates for each variant
- Check statistical significance
- Determine winner

### Step 7: Implement and document
- Roll out winner to future campaigns
- Document what you learned
- Plan next test

## Test documentation template

```
Test name: Subject line - short vs long
Date: Jan 15-22, 2025
Hypothesis: Short subject lines will increase open rate

Variant A (Control): "{{company}} marketing question"
Variant B (Treatment): "Quick q"

Results:
- A: 450 sent, 215 opens, 47.8% open rate
- B: 450 sent, 255 opens, 56.7% open rate
- Difference: +8.9 percentage points
- Significance: 98%

Winner: Variant B

Learnings: Shorter subject lines perform better. Will test even shorter next.

Next test: Ultra-short subject (2-3 words) vs short (4-6 words)
```

## Common A/B tests to run

### Subject line tests

1. Company name personalization:
   - "{{company}}" vs "{{firstName}}"

2. Length:
   - "Quick q" vs "Question about {{company}}'s growth"

3. Format:
   - Question: "Quick question?" vs Statement: "Idea for {{company}}"

4. Specificity:
   - Vague: "Your marketing" vs Specific: "Your LinkedIn ads"

### Body copy tests

1. Opening line:
   - Observation: "Noticed you..." vs Question: "How are you handling..."

2. Proof point:
   - Specific: "[Client] saw 40% lift" vs General: "Our clients see great results"

3. Length:
   - 3 sentences vs 6 sentences

4. Tone:
   - Formal: "I would be happy to..." vs Casual: "Happy to..."

### CTA tests

1. Meeting ask:
   - Calendar link vs "Reply with availability"

2. Commitment level:
   - "15-minute call" vs "Quick chat"

3. Question vs statement:
   - "Worth a call?" vs "Let's connect."

### Sequence tests

1. Number of emails:
   - 3-email vs 5-email sequence

2. Timing:
   - 2-day gaps vs 4-day gaps

3. Follow-up approach:
   - Same value prop vs different angle each email

## Test velocity

### How fast to test

**Minimum:** 1 test per month
**Good:** 2-4 tests per month
**Great:** Weekly testing

### Parallel vs sequential

**Sequential (recommended for small volume):**
- Run one test at a time
- Wait for results before next test
- Clear learnings

**Parallel (for high volume):**
- Run multiple tests simultaneously
- Different segments
- Faster learning but more complex

## When not to A/B test

1. **Volume too low:** Under 100 emails/week = not enough data
2. **Too many variables:** Can't isolate cause
3. **Wrong metric:** Testing click rate when reply rate matters
4. **Already at peak:** 70% open rate is probably good enough

## Optimization roadmap

### Phase 1: Baseline (Week 1-2)
- Send 200-500 emails
- Establish baseline metrics
- No changes yet

### Phase 2: Subject lines (Week 3-6)
- Test 3-4 subject line variants
- Find winning pattern
- Usually 2-4 tests

### Phase 3: Opening lines (Week 7-10)
- Test different openers
- Personalization approaches
- 2-3 tests

### Phase 4: CTA (Week 11-14)
- Test different asks
- Calendar link vs reply
- 2-3 tests

### Phase 5: Sequence structure (Week 15-18)
- Test email count
- Timing between emails
- 2-3 tests

### Phase 6: Continuous (ongoing)
- Monthly tests
- Refine based on learnings
- Test new ideas as they come

## Quick reference

**Test priority:**
1. Subject lines (impact opens)
2. Opening line (impact replies)
3. CTA (impact meetings)
4. Sequence structure (impact overall)

**Sample size minimums:**
- Subject line: 200+ per variant
- Body copy: 300+ per variant
- Wait for 20+ actions before judging

**Process:**
1. Hypothesis
2. Create variants
3. Determine sample
4. Run to completion
5. Analyze with significance check
6. Implement winner
7. Document and repeat
