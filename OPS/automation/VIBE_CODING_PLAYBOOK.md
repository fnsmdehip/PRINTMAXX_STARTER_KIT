# Vibe Coding Playbook

**Source:** @karpathy (Feb 2, 2025) - 31K likes, 5.3M views
**Alpha ID:** ALPHA349
**Category:** TOOL_ALPHA
**ROI Potential:** HIGHEST
**Effort:** LOW
**Risk:** MEDIUM (code quality unknown)

---

## What is Vibe Coding?

**Karpathy's original definition:**

> "There's a new kind of coding I call 'vibe coding', where you fully give in to the vibes, embrace exponentials, and forget that the code even exists. It's possible because LLMs (e.g. Cursor Composer w Sonnet) are getting too good."

**Translation:** Describe what you want in plain English. Let the AI write all the code. Don't even look at it. Just test if it works.

---

## Why This Matters for PRINTMAXX

1. **Speed:** Build MVPs in hours, not days
2. **No-code ceiling removed:** Build actual apps, not Bubble/Webflow limitations
3. **Portfolio velocity:** Ship 2-3 apps per week instead of per month
4. **Iteration speed:** "This is broken" → fixed in seconds
5. **Lower barrier:** Focus on product, not syntax

---

## The Vibe Coding Stack

### Tier 1: Cursor + Claude (Primary)

**Setup:**
1. Install Cursor (cursor.sh)
2. Enable Claude Sonnet in settings
3. Open Composer (Cmd+K)
4. Describe your app

**Best for:**
- React/Next.js apps
- Python scripts
- Full-stack development
- Complex logic

**Example prompt:**
```
Build a screen time blocker app with React Native that:
- Locks the phone until user completes 5 minutes of prayer
- Has a peaceful UI with soft blues and whites
- Uses RevenueCat for subscriptions
- Tracks daily prayer streaks
```

### Tier 2: Windsurf (Alternative)

**When to use:**
- Cursor is buggy/slow
- Need different model options
- Prefer different UX

**Same workflow:** Natural language → code → test

### Tier 3: CodeXero (Instant Deploy)

**What it is:** Natural language to deployed app on Sei Network (Web3)

**@anjalisayswhat example:**
> "i vibe coded to solve the biggest problem of human history: DISCIPLINE"
> "all vibe coded in mins on @CodeXero_xyz"

**Best for:**
- Web3 apps
- Quick deploys without DevOps
- Token/blockchain features
- Rapid prototyping

### Tier 4: Replit Agent

**What it is:** Full autonomous agent that builds, deploys, hosts

**Best for:**
- Complete beginners
- Quick web apps
- No local setup needed
- Automatic hosting

---

## Vibe Coding Workflow

### Phase 1: Describe (2 min)

Write what you want in plain English. Be specific about:
- Core feature (ONE thing)
- Target user
- Platform (mobile/web)
- Key differentiator

**Example:**
```
I want a walking tracker app for Christians that:
- Counts steps using phone sensors
- Shows Bible verses during walks
- Has a minimalist dark green design
- Locks social media until 5000 steps reached
- Uses RevenueCat for $4.99/week subscription
```

### Phase 2: Generate (5 min)

Let the AI write everything:
- File structure
- Components
- Logic
- Styling
- API integrations

**Don't:**
- Read the code line by line
- Try to understand every function
- Optimize prematurely

**Do:**
- Accept suggestions
- Keep prompting until it works
- Trust the vibes

### Phase 3: Test (10 min)

Test functionality, not code quality:
- Does the core feature work?
- Is the UI acceptable?
- Can users complete the main flow?

**If broken:** Describe what's wrong → let AI fix

### Phase 4: Ship (5 min)

Deploy immediately:
- Expo for mobile → TestFlight
- Vercel for web → Live URL
- CodeXero for Web3 → On-chain

**Total time: 22 minutes for working MVP**

---

## Vibe Coding Best Practices

### DO

1. **One feature at a time**
   - "Add login" then "Add payment" then "Add tracking"
   - Not: "Build complete app with login, payment, tracking, analytics..."

2. **Describe outcomes, not implementation**
   - Good: "Make the button feel bouncy when pressed"
   - Bad: "Add spring animation with 0.3s duration and cubic-bezier..."

3. **Include constraints**
   - "Use only React Native, no Expo modules"
   - "Keep it under 500 lines"
   - "Use these specific colors: #1a1a2e, #16213e"

4. **Reference working examples**
   - "Make the paywall look like Calm's"
   - "Copy the animation style from Duolingo"

5. **Test frequently**
   - Every 2-3 prompts, run the app
   - Catch issues early before they compound

### DON'T

1. **Don't read all the code**
   - You'll slow down
   - The AI can explain if needed
   - Focus on outcomes

2. **Don't optimize early**
   - Ship first
   - Optimize only if users complain
   - "Premature optimization is the root of all evil"

3. **Don't fight the AI**
   - If it wants to use a library, let it
   - If it structures code differently, accept it
   - Your preferences don't matter if it works

4. **Don't vibe code production backends**
   - Auth systems need review
   - Payment logic needs review
   - Data handling needs review

---

## Risk Mitigation

### Code Quality Risks

| Risk | Mitigation |
|------|------------|
| Security holes | Manual review of auth/payment code |
| Performance issues | Load test before scale |
| Tech debt | Accept it for MVPs, refactor winners |
| Breaking changes | Git commits after each working state |

### When NOT to Vibe Code

1. **Payment processing** - Review manually
2. **User authentication** - Review manually
3. **Data encryption** - Review manually
4. **API keys/secrets** - Review manually
5. **Production databases** - Review manually

### Safe Vibe Coding Zones

1. **UI/UX** - Let AI go wild
2. **Animations** - Full vibes
3. **Static content** - Full vibes
4. **Prototypes** - Full vibes
5. **Internal tools** - Full vibes

---

## PRINTMAXX Integration

### APP_FACTORY Acceleration

Use vibe coding for:
- PrayerLock MVP iterations
- WalkToUnlock core features
- StudyLock blocking logic
- New app prototypes

**Workflow:**
1. Get app idea from LEDGER/APP_CLONE_OPPORTUNITIES.csv
2. Vibe code MVP in Cursor
3. Test in iOS Simulator
4. If promising, add to build queue
5. Production code review before App Store

### Content Automation Scripts

Use vibe coding for:
- Playwright automation scripts
- Content generation pipelines
- Data processing tools
- CSV manipulation scripts

### Ralph Loop Tools

Build ralph loop utilities via vibe coding:
- Progress file parsers
- Output aggregators
- Quality checkers
- Deduplication tools

---

## Tool Comparison

| Tool | Speed | Quality | Deploy | Cost | Best For |
|------|-------|---------|--------|------|----------|
| Cursor + Claude | Fast | High | Manual | $20/mo | Production apps |
| Windsurf | Fast | High | Manual | $15/mo | Alternative to Cursor |
| CodeXero | Fastest | Medium | Auto | Free? | Web3 prototypes |
| Replit Agent | Medium | Medium | Auto | $25/mo | Beginners |

---

## Quick Start Checklist

- [ ] Install Cursor (cursor.sh)
- [ ] Enable Claude Sonnet model
- [ ] Create new project folder
- [ ] Open Composer (Cmd+K)
- [ ] Describe your app in 2-3 sentences
- [ ] Accept all suggestions
- [ ] Run and test
- [ ] Iterate with "fix this: [problem]"
- [ ] Ship when core feature works

---

## Example Prompts

### Screen Time App
```
Build a React Native app that blocks Instagram until user completes 10 minutes of prayer.
Use a peaceful purple gradient UI. Add a timer with calming animations.
Track prayer streaks with AsyncStorage. Include RevenueCat paywall at $6.99/week.
```

### Content Automation
```
Build a Python script that:
- Reads URLs from a CSV file
- Scrapes the main content from each URL
- Saves to individual markdown files
- Logs progress to a JSON file
- Handles errors gracefully
```

### Data Processing
```
Build a Python script that:
- Reads ALPHA_STAGING.csv
- Filters for PENDING_REVIEW status
- Groups by category
- Outputs summary statistics
- Exports approved entries to separate file
```

---

## Metrics to Track

1. **Build time:** Minutes from idea to working MVP
2. **Iteration speed:** Time to fix reported issues
3. **Ship rate:** Apps deployed per week
4. **Winner rate:** Apps that hit $1k MRR
5. **Code review time:** Hours spent on manual review

**Target:**
- 3 MVPs per week
- 30 min average build time
- 1 winner per 10 ships

---

## Updates

| Date | Update |
|------|--------|
| 2026-01-26 | Initial playbook created from @karpathy tweet |

---

## Related Files

- `LEDGER/APP_CLONE_OPPORTUNITIES.csv` - App ideas to vibe code
- `MONEY_METHODS/APP_FACTORY/APP_DISCOVERY_PROCESS.md` - Finding apps to build
- `ralph/loops/app_factory/` - Overnight app building loops
- `LEDGER/ALPHA_STAGING.csv` - ALPHA349 entry
