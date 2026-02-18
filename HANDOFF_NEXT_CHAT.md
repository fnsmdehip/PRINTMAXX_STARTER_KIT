# Handoff for Next Chat Session

**CRITICAL: Start every session by reading `.claude/CLAUDE.md` for full project context.**

**Updated:** 2026-01-21
**Session:** Alpha review, prompt organization, subagent launches

---

## FIRST THING TO DO

```bash
# Read the main project instructions
cat .claude/CLAUDE.md
```

This file contains:
- Project architecture
- Operating policies
- Daily research system
- Ralph loop patterns
- All file locations
- Model routing rules

---

## SESSION COMPLETED

### Alpha Review
- **50 entries approved**, 1 rejected (ALPHA050)
- Key high-priority alpha for immediate implementation:
  - ALPHA032: Animated paywalls = 2.9x conversion
  - ALPHA033: Paywall in onboarding = 50% of trials
  - ALPHA034: Annual plans = 2.6x retention
  - ALPHA038: Gamification = 55% 7-day retention
  - ALPHA042: Single push notification = 3x retention
  - ALPHA049: X launch hack (ask for comments)

### Prompt Organization
- Created `OPS/prompts/templates/landing_page_prompt.md` - Landing page generation
- Created `OPS/prompts/templates/engineering_modes.md` - Planner/Debugger modes + security checklist
- Original RTF files remain in project root for reference

### Remotion Video Pattern
- Fetched Remotion prompt pattern from JonnyBurger gist
- Key insight: Conversational workflow, not rigid prompts
- Request changes naturally: "make it bigger", "add typewriter animation"
- Claude Code understands Remotion API implicitly

---

## APPS STATUS

| App | Onboarding | Content | Monetization | Status |
|-----|------------|---------|--------------|--------|
| PromptVault | 5 screens | 1,055 prompts | Freemium + ads | Simulator running |
| PelvicPro | 4 screens | 50+ exercises | Trial + sub | Simulator running |
| LearnLock | None | N/A | Subscription | Needs iOS init |
| FocusPrayer | None | N/A | Subscription | Needs iOS init |
| StepUnlock | None | N/A | Subscription | Needs iOS init |
| DailyAnchor | None | N/A | Subscription | Needs iOS init |
| DevotionFlow | None | N/A | Subscription | Android only |

---

## KEY ALPHA TO IMPLEMENT NOW

From ALPHA_STAGING.csv, implement in all apps:

1. **Animated paywalls** (ALPHA032) - 2.9x conversion boost
2. **Paywall in onboarding** (ALPHA033) - 50% of trials start Day 0
3. **Default annual plans** (ALPHA034) - 2.6x higher retention
4. **User name on paywall** (ALPHA035) - +17% conversion
5. **Streak mechanics** (ALPHA038) - Duolingo pattern
6. **Day 1 push notification** (ALPHA042) - 3x retention
7. **Google Sign-In default** (ALPHA020b) - 90%+ pick Google
8. **Attribution question** (ALPHA022) - "How did you hear about us?"

---

## RALPH TASKS READY

Located in `ralph_tasks/`:

| Task | Description | Priority |
|------|-------------|----------|
| 00_daily_alpha_research.md | Scan sources for new alpha | Daily |
| 01_content_faith.md | Faith niche content | HIGH |
| 02_content_fitness.md | Fitness niche content | HIGH |
| 03_content_ai.md | AI niche content | HIGH |
| 04_email_sequences.md | Email sequence generation | MEDIUM |
| 05_playwright_scripts.md | Automation scripts | MEDIUM |
| 06_landing_components.md | Landing page components | HIGH |
| 07_app_clone_research.md | Find apps to clone | HIGH |
| 08_app_factory_build.md | Build apps autonomously | HIGH |
| 09_app_marketing_stack.md | Marketing materials | HIGH |
| 10_performance_monitor.md | Track and optimize | MEDIUM |

---

## MANUAL TASKS (Human Required)

### Priority 1: Accounts
- [ ] Apple Developer ($99/yr) - developer.apple.com
- [ ] Google Play Console ($25) - play.google.com/console
- [ ] RevenueCat (free) - revenuecat.com
- [ ] @PRINTMAXXER on X

### Priority 2: FamilyControls API
- [ ] Apply at developer.apple.com/contact/request/family-controls-distribution
- Required for: FocusPrayer, StepUnlock, LearnLock

---

## QUICK COMMANDS

```bash
# Project status
make status

# Run daily research
/daily-research

# Review alpha entries
/review-alpha

# Start landing site
cd LANDING/printmaxx-site && npm run dev

# Validation
make validate
```

---

## KEY FILES

```
.claude/CLAUDE.md              # START HERE - main instructions
.claude/rules/copy-style.md    # Writing guidelines
OPS/RALPH_LOOP_GUIDE.md        # Autonomous build pattern
ralph_tasks/                   # Ready-to-run ralph tasks
LEDGER/ALPHA_STAGING.csv       # 50 approved alpha entries
LEDGER/APP_FACTORY_METHODS.csv # 13 proven app building methods
OPS/prompts/templates/         # Reusable prompt templates
```

---

## NEXT SESSION PRIORITIES

1. **Launch ralph agents** for app builds (LearnLock, FocusPrayer, StepUnlock)
2. **Implement high-priority alpha** in PromptVault and PelvicPro
3. **Generate Remotion brand videos** for PRINTMAXX and apps
4. **Content generation** for all three niches
5. **Landing page creation** using new prompt template

---

**Remember: Read `.claude/CLAUDE.md` first. Everything is there.**
