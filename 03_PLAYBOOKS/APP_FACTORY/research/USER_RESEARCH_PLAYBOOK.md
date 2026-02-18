# User Research Playbook

Research methods for building apps people actually want.

---

## Research methods overview

| Method | Best for | Time | Participants |
|--------|----------|------|--------------|
| Discovery interviews | Finding problems worth solving | 30-60 min each | 5-8 |
| Usability tests | Testing if features work | 15-30 min each | 5 |
| Surveys | Quantifying opinions at scale | 5-10 min | 30+ |
| Churn interviews | Understanding why users leave | 20-30 min each | 5-10 |
| Power user interviews | Understanding retention | 30-45 min each | 3-5 |
| A/B tests | Validating feature impact | 1-2 weeks | 100+ per variant |

---

## When to use each method

### Discovery interviews
**Use when:** Starting a new product or feature area
**Goal:** Understand problems, workflows, and pain points
**Output:** Problem statements, opportunity areas

**Sample questions:**
- Walk me through your typical day doing [activity]
- What's the most frustrating part of [task]?
- What have you tried to solve this problem?

### Usability tests
**Use when:** Testing a prototype or live feature
**Goal:** Find usability issues before launch
**Output:** List of friction points ranked by severity

**Best practices:**
- Test with 5 users to find 80% of issues
- Use think-aloud protocol
- Don't lead or help

### Surveys
**Use when:** Need quantitative validation
**Goal:** Measure opinions at scale
**Output:** Percentages, rankings, segments

**Best practices:**
- Keep under 10 questions
- Use 5-point scales
- Include one open-ended question
- Incentivize completion

### Churn interviews
**Use when:** Users are leaving
**Goal:** Understand the moment they decided to leave
**Output:** Churn reasons ranked by frequency

**Key questions:**
- When did you stop using [product]?
- What were you trying to accomplish?
- What are you using instead?

### Power user interviews
**Use when:** Want to understand retention
**Goal:** Find what keeps your best users engaged
**Output:** Feature usage patterns, value props

**Key questions:**
- What made you stick with [product]?
- How has your usage changed over time?
- What would make you recommend this to a friend?

---

## Sample sizes

| Research type | Minimum | Ideal | Notes |
|---------------|---------|-------|-------|
| Discovery interviews | 5 | 8-12 | Stop when themes repeat |
| Usability tests | 5 | 5 | Diminishing returns after 5 |
| Surveys | 30 | 100+ | Need statistical significance |
| A/B tests | 100/variant | 1000/variant | Depends on effect size |
| Churn interviews | 5 | 10-15 | Focus on recent churners |

### When to stop interviewing
You've reached saturation when:
- Same themes appear 3x in a row
- No new insights in last 2 interviews
- You can predict answers before they speak

---

## Analysis frameworks

### Jobs to be done (JTBD)
**When someone [situation], they want to [motivation], so they can [outcome].**

Example: When a busy professional feels spiritually disconnected, they want quick daily guidance, so they can stay grounded without major time commitment.

### Problem stack ranking
After interviews, rank problems by:
1. **Frequency** - How many users mentioned it?
2. **Intensity** - How painful is it?
3. **Willingness to pay** - Would they pay to solve it?

Priority = Frequency x Intensity x Willingness

### Affinity mapping
1. Write each insight on a sticky note
2. Group similar insights
3. Name each group
4. Prioritize groups

### User journey mapping
Document each stage:
1. **Trigger** - What prompted them to act?
2. **Search** - How did they find solutions?
3. **Evaluation** - How did they compare options?
4. **Use** - What was onboarding like?
5. **Retention** - What keeps them engaged?
6. **Advocacy** - Would they recommend?

---

## Research timeline templates

### Pre-launch research (2-3 weeks)
- Week 1: 6-8 discovery interviews
- Week 2: Synthesize findings, create personas
- Week 3: Validate with survey (50+ responses)

### Feature validation (1 week)
- Day 1-2: Create prototype
- Day 3-4: 5 usability tests
- Day 5: Synthesize and iterate

### Ongoing research cadence
- Monthly: 2-3 user interviews
- Quarterly: NPS survey
- After churn: Exit interview within 48 hours

---

## Tools

### Free
- Google Forms (surveys)
- Loom (recording usability tests)
- Notion/Sheets (tracking)
- Calendly (scheduling)

### Paid (when you have budget)
- Typeform ($25/mo) - better survey UX
- Hotjar ($39/mo) - session recordings
- UserTesting ($49/test) - recruited participants
- Dovetail ($29/mo) - research repository

---

## Common mistakes

1. **Leading questions** - "Don't you think this feature is useful?"
2. **Building for yourself** - Your problems are not universal
3. **Small sample sizes** - 2 interviews is not research
4. **No recording** - Memory is unreliable
5. **Asking about future behavior** - People predict poorly
6. **Not synthesizing** - Raw notes are not insights

---

## Templates in this folder

**Interview guides:**
- `interview_guides/discovery_interview.md`
- `interview_guides/usability_test.md`
- `interview_guides/churn_interview.md`
- `interview_guides/power_user_interview.md`

**Survey templates:**
- `survey_templates/nps_survey.md`
- `survey_templates/feature_priority_survey.md`
- `survey_templates/pricing_survey.md`
- `survey_templates/onboarding_feedback.md`

**Personas:**
- `user_personas/` - 6 personas across niches

**Recruitment:**
- `recruitment_templates/screener_survey.md`
- `recruitment_templates/recruitment_email.md`
- `recruitment_templates/incentive_structure.md`

**Analysis:**
- `analysis_templates/interview_synthesis.md`
- `analysis_templates/survey_analysis.md`
- `analysis_templates/usability_findings.md`

**Tracking:**
- `RESEARCH_TRACKER.csv` - All studies
- `insight_repository.md` - Findings database
