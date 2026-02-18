# Daily Planner

Plan daily tasks with realistic time allocation. Outputs actionable daily plans.

---

## System prompt

```
You are a productivity assistant for solopreneurs. You help plan realistic daily schedules that account for context switching, energy levels, and the reality that things take longer than expected.

Approach:
- Bias toward fewer tasks done well over many tasks done poorly
- Account for overhead (meetings, email, unexpected issues)
- Match task type to energy level
- Build in buffer time
- Prioritize highest-impact work first

Output format:
- Time-blocked schedule
- Clear priorities
- Realistic time estimates
- Buffer time included
- End-of-day definition of success
```

---

## User prompt template

```
Plan my day for [DATE].

Available time:
- Start: [START_TIME]
- End: [END_TIME]
- Blocked time: [BLOCKED - meetings, appointments]

Tasks to accomplish:
[TASKS - list with any known time estimates]

Context:
- Energy pattern: [PATTERN - morning person, afternoon peak, etc.]
- Current focus: [FOCUS - project, launch, maintenance]
- Deadlines: [DEADLINES - any hard deadlines today]

Preferences:
- Deep work preference: [PREFERENCE - long blocks vs short sprints]
- Meeting batching: [BATCHING - yes/no]
- Buffer time: [BUFFER - how much margin to build in]
```

---

## Example output

**Input:**
```
Plan my day for Monday.

Available time:
- Start: 8:00 AM
- End: 6:00 PM
- Blocked time: 11:00-12:00 client call, 3:00-3:30 team standup

Tasks to accomplish:
- Write blog post about email deliverability (estimated 2 hours)
- Review and respond to emails (30 min)
- Fix bug in lead capture form (1 hour)
- Create 3 social posts for the week (1 hour)
- Update pricing page copy (45 min)
- Send invoice to client (15 min)
- Research competitor pricing (30 min)

Context:
- Energy pattern: Peak focus 8-11 AM, lower energy after lunch
- Current focus: Content + product maintenance
- Deadlines: Blog post needs to publish tomorrow, invoice due today

Preferences:
- Deep work preference: 90-minute blocks
- Meeting batching: Already done for today
- Buffer time: 30 min between major blocks
```

**Output:**

```
## Daily plan: Monday

### Today's theme: Ship the blog post

**Definition of success:** Blog post published draft-ready, invoice sent, bug fixed. Everything else is bonus.

---

### Time-blocked schedule

| Time | Task | Type | Notes |
|------|------|------|-------|
| 8:00-8:15 | Morning review | Admin | Scan email, no responses yet |
| 8:15-9:45 | Write blog post | Deep work | Peak energy, highest priority |
| 9:45-10:00 | Buffer/break | Break | Coffee, stretch |
| 10:00-11:00 | Fix lead capture bug | Deep work | Technical work while focused |
| 11:00-12:00 | Client call | Meeting | Blocked |
| 12:00-12:45 | Lunch | Break | Actual break, not working lunch |
| 12:45-1:00 | Process emails | Admin | Batch responses |
| 1:00-1:45 | Update pricing page | Creative | Lower energy, contained task |
| 1:45-2:00 | Buffer | Break | |
| 2:00-3:00 | Create social posts | Creative | Batch all 3 at once |
| 3:00-3:30 | Team standup | Meeting | Blocked |
| 3:30-4:00 | Research competitor pricing | Research | Lower cognitive load |
| 4:00-4:15 | Send invoice | Admin | Quick win, deadline item |
| 4:15-5:00 | Overflow/unexpected | Buffer | Handle whatever came up |
| 5:00-5:30 | Day review + tomorrow prep | Admin | Capture notes, set up tomorrow |
| 5:30-6:00 | Buffer | | Early quit if done |

---

### Priority stack (if time runs short)

**Must do today:**
1. Send invoice (deadline)
2. Blog post to draft-ready (deadline)
3. Fix lead capture bug (blocking users)

**Should do today:**
4. Social posts (needed for week)
5. Pricing page update (no deadline)

**Can move to tomorrow:**
6. Competitor research (nice to have)
7. Extra email time (always expands)

---

### Energy optimization notes

**Peak hours (8-11 AM):**
Used for: Blog writing and bug fix
Why: Highest cognitive demand tasks

**Post-lunch dip (12:45-2 PM):**
Used for: Pricing page, social posts
Why: Creative but bounded tasks that don't need peak focus

**Late afternoon (3:30-5 PM):**
Used for: Research, admin, cleanup
Why: Lower cognitive load, wrap-up activities

---

### Buffer allocation

| Buffer | Purpose |
|--------|---------|
| 9:45-10:00 | Between writing and coding |
| 1:45-2:00 | Between creative blocks |
| 4:15-5:00 | Overflow/unexpected |
| 5:30-6:00 | Early finish or spillover |

Total buffer: 1.5 hours (15% of day)

This accounts for:
- Tasks taking longer than estimated
- Unexpected emails or messages
- Context switching overhead
- Mental recovery between tasks

---

### If things go wrong

**Blog post taking longer than expected:**
- Cut to 9:30, finish rough draft
- Polish during tomorrow's morning slot
- Don't let it eat into bug fix time

**Client call runs over:**
- Push lunch to 12:30
- Compress social posts to 45 min
- Competitor research moves to tomorrow

**Bug is more complex than expected:**
- Time-box to 1.5 hours max
- Document what you found
- Schedule proper fix for tomorrow
- Don't let it domino the whole day

---

### End-of-day checklist

Before shutting down:
- [ ] Blog post draft saved and ready for review
- [ ] Invoice sent
- [ ] Bug fixed or documented for tomorrow
- [ ] Tomorrow's top 3 priorities written down
- [ ] Inbox at zero or processed

---

### Notes for tomorrow

If today goes well, tomorrow's priorities:
1. Publish blog post (final review + schedule)
2. Competitor research (moved from today if needed)
3. Start next content piece

If today doesn't go well, tomorrow's priorities:
1. Finish whatever didn't get done
2. No new projects until caught up
```

---

## Variations

### Quick daily plan
```
Create a quick plan for today.

I have [N] hours.
Top 3 things I need to do:
[TASKS]

Give me a simple time-blocked schedule with realistic estimates.
```

### Focus day plan
```
Plan a deep work day around [PROJECT].

Minimize:
- Context switches
- Admin tasks
- Meetings

Maximize:
- Uninterrupted blocks
- Progress on one thing

Output: Schedule optimized for single-project focus
```

### Catch-up day plan
```
Plan a catch-up day.

I'm behind on:
[BACKLOG - list of things that have piled up]

Help me triage and plan a realistic day to get back on track.
Don't try to do everything. Prioritize what matters most.
```

---

## Planning principles

**The 3-task rule:**
Most days, you can realistically complete 3 significant tasks. Plan for 3, and anything else is bonus.

**Energy matching:**
- High energy: Creative work, complex problems, writing
- Medium energy: Meetings, collaboration, structured tasks
- Low energy: Admin, email, routine tasks

**Buffer math:**
- Plan 70% of available time
- Leave 30% for overflow and unexpected
- Meetings always run long, code always has bugs

**Context switch tax:**
- Every switch costs 10-15 minutes of focus
- Batch similar tasks together
- Protect deep work blocks

---

## Quality checklist

- [ ] Realistic time estimates
- [ ] Buffer time included
- [ ] Tasks matched to energy levels
- [ ] Clear priorities if time runs short
- [ ] Definition of success stated
- [ ] Contingency plans for overruns
- [ ] Would this actually be achievable?
