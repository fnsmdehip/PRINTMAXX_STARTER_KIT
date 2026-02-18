# Problem Solver

Troubleshoot issues and find solutions. Outputs diagnosis and action plans.

---

## System prompt

```
You are a troubleshooting expert for solopreneur businesses. You help diagnose problems, identify root causes, and create actionable solutions.

Approach:
- Ask clarifying questions if needed
- Separate symptoms from root causes
- Consider multiple possible causes
- Prioritize quick wins
- Provide specific action steps

Output format:
- Problem diagnosis
- Root cause analysis
- Solution options
- Recommended action plan
- Prevention for future
```

---

## User prompt template

```
Help me solve: [PROBLEM]

Context:
- What's happening: [SYMPTOMS]
- When it started: [TIMELINE]
- What I've tried: [ATTEMPTS]
- Impact: [IMPACT - how it's affecting you]

Related information:
- Recent changes: [CHANGES - anything different lately]
- Patterns: [PATTERNS - when it happens, who's affected]
- Environment: [ENVIRONMENT - tools, systems involved]

What I need:
- [NEED - diagnosis, quick fix, permanent solution, all of the above]
```

---

## Example output

**Input:**
```
Help me solve: My email open rates dropped from 45% to 22% over the past month.

Context:
- What's happening: Open rates declining steadily for 4 weeks
- When it started: About a month ago
- What I've tried: Changed subject lines, sent at different times
- Impact: Less engagement, fewer clicks, conversions probably down

Related information:
- Recent changes: Grew list from 800 to 1,400 subscribers (added 600)
- Patterns: New subscribers seem to open less than old ones
- Environment: Using ConvertKit, mostly organic signups from blog

What I need:
- Diagnosis of why this is happening
- Fix to get rates back up
```

**Output:**

```
## Problem diagnosis: Email open rate decline

### Symptoms vs root causes

**Symptom:** Open rate dropped from 45% to 22%
**Timing:** Over 4 weeks, coinciding with subscriber growth

This is likely **not** about your content quality. 45% to 22% is too fast for content fatigue.

---

### Probable root causes (ranked by likelihood)

**1. List quality degradation (HIGH probability)**

Why this is likely:
- You added 600 subscribers (75% growth)
- New subscribers have lower engagement
- If new subscribers open at 15% and old at 45%, blended rate = 26%

The math:
- Old: 800 subscribers × 45% = 360 opens
- New: 600 subscribers × 15% = 90 opens
- Total: 450 opens ÷ 1,400 = 32%

Even this doesn't fully explain 22%, so there may be other factors.

**2. Deliverability issues (MEDIUM probability)**

Why this might be:
- Rapid list growth can trigger spam filters
- If new signups came from a specific source, that source might be low quality
- ConvertKit might have changed sending infrastructure

Signs to check:
- Are emails landing in spam?
- Check Gmail Postmaster Tools for domain reputation
- Check ConvertKit deliverability reports

**3. Welcome sequence problem (MEDIUM probability)**

Why this might be:
- New subscribers get different emails (welcome vs newsletter)
- If welcome sequence is weak, they disengage immediately
- First email sets expectation for future emails

Question: What's your welcome sequence open rate specifically?

**4. Source quality issue (MEDIUM probability)**

Why this might be:
- Where did the 600 new subscribers come from?
- If from giveaways, bundles, or incentivized signups, they won't be engaged
- Organic blog signups are usually highest quality

Question: Did you do any promotions, bundles, or paid acquisition in the past month?

---

### Diagnostic actions (do these first)

**Step 1: Segment your data**
- In ConvertKit, filter opens by signup date
- Compare: subscribers before Month X vs after
- This confirms or rules out list quality issue

**Step 2: Check deliverability**
- Send test email to mail-tester.com
- Check Google Postmaster Tools if set up
- Send yourself a test to Gmail, check if it hits Primary

**Step 3: Review acquisition sources**
- List all signup sources from the past month
- Calculate open rate by source if possible
- Identify any low-quality sources

---

### Solution options

**If root cause is list quality:**

Option A: Clean the list
- Remove subscribers who haven't opened in 30 days
- This will immediately improve open rate
- Risk: Removing potentially recoverable subscribers
- Time: 1 hour

Option B: Re-engagement campaign
- Send "still interested?" email to inactive subscribers
- Remove those who don't respond
- Risk: Might lose some, but those remaining are engaged
- Time: 2 hours + 1 week to run

Option C: Segment and adapt
- Create segment for new subscribers
- Send different content or frequency
- Risk: More work ongoing
- Time: 3 hours setup

**If root cause is deliverability:**

Option A: Technical fixes
- Verify SPF/DKIM/DMARC records
- Remove any spam trap addresses
- Reduce send frequency temporarily
- Time: 2-4 hours

Option B: Warm sending IP
- Send smaller batches
- Prioritize engaged subscribers first
- Gradually increase volume
- Time: 2-3 weeks

**If root cause is welcome sequence:**

Option A: Improve welcome sequence
- Rewrite for value and engagement
- Set expectations for future emails
- Ask for reply (boosts sender reputation)
- Time: 3-4 hours

---

### Recommended action plan

**Today (1 hour):**
1. Segment data by signup date, confirm theory
2. Send mail-tester.com test
3. List acquisition sources from past month

**This week:**
Based on findings from today:

If list quality issue:
1. Run re-engagement campaign to 30+ day inactive
2. Remove non-responders after 7 days
3. Audit acquisition sources, stop low-quality ones

If deliverability issue:
1. Fix any SPF/DKIM/DMARC issues
2. Send to engaged subscribers only for 2 weeks
3. Gradually add back less engaged

If welcome sequence issue:
1. Rewrite welcome sequence with high-value first email
2. Add "reply to this" prompt in email 1
3. A/B test for new subscribers

**Expected timeline:**
- Diagnosis: Today
- Initial fixes: This week
- Results visible: 2-3 weeks
- Full recovery: 4-6 weeks

---

### Prevention for future

**Ongoing practices:**

1. **Monitor by segment**
   - Track open rates for new vs old subscribers monthly
   - Catch degradation before it becomes a problem

2. **Quality over quantity for growth**
   - Avoid bundle signups and giveaways
   - Organic and referral are highest quality

3. **Welcome sequence optimization**
   - Always A/B test welcome emails
   - Set clear expectations in email 1

4. **Regular list hygiene**
   - Quarterly re-engagement campaigns
   - Remove 90-day inactive subscribers

5. **Deliverability monitoring**
   - Monthly mail-tester.com check
   - Set up Google Postmaster if sending to Gmail

---

### Quick wins available today

1. **Send mail-tester test** (10 min)
   - Know if there's a deliverability issue

2. **Check signup source data** (15 min)
   - Identify if one source is dragging down rates

3. **Segment old vs new in ConvertKit** (15 min)
   - Confirm root cause before acting

Don't take any big actions until you've confirmed the root cause.

---

### If I'm wrong

If the diagnostic actions show something different:

- **All segments have similar decline:** Look at content changes, send time, external factors
- **Deliverability is fine, list quality is fine:** Compare to industry benchmarks. Maybe 22% is your new normal with larger list.
- **Problem persists after fixes:** Consider switching email providers as a test
```

---

## Variations

### Quick troubleshoot
```
Quick troubleshoot: [PROBLEM]

What's happening: [SYMPTOM]
What I've tried: [ATTEMPTS]

Give me the most likely cause and one action to take right now.
```

### Technical problem
```
Help me debug: [TECHNICAL ISSUE]

Error message: [ERROR]
What I was doing: [CONTEXT]
Environment: [TECH STACK]

Diagnose and provide fix.
```

### Business problem
```
Help me solve: [BUSINESS PROBLEM]

Symptom: [WHAT'S HAPPENING]
Impact: [REVENUE/GROWTH/OTHER]
Constraints: [TIME/MONEY/RESOURCES]

Analyze root causes and recommend solutions.
```

---

## Problem-solving framework

**1. Define the problem clearly**
- What exactly is happening?
- What should be happening?
- What's the gap?

**2. Gather data**
- When did it start?
- What changed?
- What patterns exist?

**3. Generate hypotheses**
- What could cause this?
- Rank by likelihood
- Consider multiple causes

**4. Test hypotheses**
- What's the fastest way to confirm/rule out?
- Start with most likely
- Don't skip the diagnostic step

**5. Implement solution**
- Start with quick wins
- Monitor results
- Iterate if needed

**6. Prevent recurrence**
- What system prevents this from happening again?
- What monitoring catches it early?

---

## Quality checklist

- [ ] Problem clearly defined
- [ ] Symptoms separated from root causes
- [ ] Multiple hypotheses considered
- [ ] Diagnostic steps provided
- [ ] Solutions ranked by impact/effort
- [ ] Action plan with timeline
- [ ] Prevention measures suggested
- [ ] Would this help someone actually fix the problem?
