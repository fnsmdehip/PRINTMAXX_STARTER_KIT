# Ralph Task: Daily Alpha Research

Run this task daily to scan for new opportunities and update watchlist.

**INTEGRATES WITH EXISTING INFRASTRUCTURE:**
- Read: `LEDGER/HIGH_SIGNAL_SOURCES.csv` (81+ high-signal X accounts, Reddit, YouTube, SEO/ASO blogs)
- Write: `LEDGER/ALPHA_STAGING.csv` (new findings for human review)
- Run: `/daily-research` skill for full scan
- See: `.claude/commands/daily-research.md` for full spec
- Reference: `OPS/GTM_OPTIMIZATION_CHECKLIST.md` for ASO/SEO/GEO standards

---

## Context
- Read `LEDGER/HIGH_SIGNAL_SOURCES.csv` for source list
- Read `LEDGER/ALPHA_STAGING.csv` for existing staged findings
- Read `LEDGER/ALPHA_WATCHLIST.csv` for current tracking
- Output findings to `LEDGER/ALPHA_STAGING.csv` and `OPS/alpha_research/`

## Success Criteria

### Step 1: Scan High-Signal Sources (from existing LEDGER)
1. [ ] Scan priority X accounts (@iamgdsa, @Hightrafficsite, @jasoncfox, @wesocialgrowth)
2. [ ] Check for ChatGPT ads updates (OpenAI blog, X, news)
3. [ ] Check for new AI tools relevant to content automation
4. [ ] Check competitor movements (levelsio, tdinh, dannypostmaa)
5. [ ] Check proxy/automation tool updates

### Step 1B: SEO/ASO/GEO Research (WEEKLY PRIORITY)
6. [ ] Scan SEO accounts (@lilyraynyc, @JohnMu, @aleyda, @iPullRank)
7. [ ] Scan ASO accounts (@paborns, @thomasbcn)
8. [ ] Scan GEO/AI search accounts (@gaborcselle)
9. [ ] Check r/SEO, r/bigseo for algorithm updates
10. [ ] Check r/AppBusiness for ASO tactics
11. [ ] Scan Ahrefs blog, Search Engine Journal for studies
12. [ ] Check AppTweak blog for ASO research

### Step 2: Alpha Assessment
6. [ ] For each finding, assess: Hype vs Real Alpha
7. [ ] Evaluate: Actionable within $200-500 budget?
8. [ ] Check: Has proof of working (numbers, results)?
9. [ ] Verify: New (not already in LEDGER files)?
10. [ ] Confirm: Aligns with 3 niches or meta-brand?

### Step 3: Stage for Human Review
11. [ ] Write new findings to `LEDGER/ALPHA_STAGING.csv` with:
    - alpha_id: ALPHA[NNN]
    - source: Where found
    - category: APP_FACTORY | CONTENT_FORMAT | OUTBOUND | GROWTH_HACK | TOOL_ALPHA | CHANNEL | MONETIZATION | SEO_GEO_ASO
    - summary: 1-2 sentence description
    - proof: Numbers/results that validate it
    - actionable_steps: How to implement
    - status: PENDING_REVIEW

### Step 4: Update Watchlist
12. [ ] Add new items to `LEDGER/ALPHA_WATCHLIST.csv`
13. [ ] Update status of existing items
14. [ ] Create daily report in `OPS/alpha_research/[DATE].md`

## ChatGPT Ads Specific Research (HIGH PRIORITY)

When checking ChatGPT ads:
- [ ] Check OpenAI announcements
- [ ] Search X for "ChatGPT ads" or "OpenAI advertising"
- [ ] Look for beta tester reports
- [ ] Note any CPM/CPC data shared
- [ ] Check if API access available
- [ ] Monitor approval process requirements

**Key Question:** Is there early mover advantage like TikTok ads 2019?
**Context:** Friends made 8 figures on TikTok ads early due to low CPMs.

## Output Format

```markdown
# Alpha Research - [DATE]

## Sources Scanned
- X accounts: [count]
- Reddit: [count]
- Other: [count]

## New Findings Staged
[count] new entries added to ALPHA_STAGING.csv

## Category Breakdown
- TOOL_ALPHA: [count]
- GROWTH_HACK: [count]
- CHANNEL: [count]
- etc.

## Priority for Human Review
1. [highest priority item]
2. [second priority item]

## ChatGPT Ads Update
[current status of ChatGPT ads - any new info?]

## Watchlist Changes
- [item]: [status change]
```

## After Completion
- Update `.ralph/progress.md`
- Update `LEDGER/ALPHA_STAGING.csv` (PENDING_REVIEW entries)
- Update `LEDGER/ALPHA_WATCHLIST.csv`
- Create daily report in `OPS/alpha_research/[DATE].md`

## Human Follow-Up Required
After this task completes, human should:
1. Review ALPHA_STAGING.csv entries marked PENDING_REVIEW
2. Mark each as APPROVED or REJECTED
3. Run `/review-alpha` to integrate approved entries

---

test_command: "ls OPS/alpha_research/*.md | wc -l"
