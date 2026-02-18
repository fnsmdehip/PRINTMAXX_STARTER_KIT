# Daily Alpha Research Skill

**Purpose:** Automatically scan high-signal sources for new tactics, tools, and strategies
**Frequency:** Daily (run at start of session or on demand with `/alpha-scan`)
**Output:** Staged findings in LEDGER/ALPHA_STAGING.csv for human review

---

## How This Skill Works

1. **Scan** - Check HIGH_SIGNAL_SOURCES.csv for accounts marked `auto_monitor=TRUE`
2. **Extract** - Pull latest posts/content from each source
3. **Filter** - Only surface actionable alpha (not noise)
4. **Stage** - Add to ALPHA_STAGING.csv with `status=PENDING_REVIEW`
5. **Wait** - Human reviews and marks as `APPROVED` or `REJECTED`
6. **Learn** - Track approval patterns to improve filtering over time

---

## Source Categories

### Tier 1: HIGHEST Signal (Always Scan)
- @levelsio, @tdinh_me, @caiden_cole, @pipelineabuser, @knoxtwts, @purpdevvv
- Ben's Bites newsletter
- IdeaBrowser community signals
- Product Hunt daily

### Tier 2: HIGH Signal (Daily Scan)
- All other Twitter accounts in HIGH_SIGNAL_SOURCES.csv
- Reddit: r/SideProject, r/indiehackers, r/coldemail, r/AppBusiness
- Fireship YouTube

### Tier 3: MEDIUM Signal (Weekly Scan)
- General newsletters
- Podcasts (scan show notes)
- Tools like algrow.online, appkittie

---

## Alpha Classification Schema

For each finding, classify into:

| Category | Description | Example |
|----------|-------------|---------|
| APP_FACTORY | Mobile app opportunity or tactic | "Take trending app X, make version for women" |
| CONTENT_FORMAT | Winning hook/structure/CTA | "This thumbnail format gets 10x CTR" |
| OUTBOUND | Email/LinkedIn/call tactic | "New subject line formula: 47% open rate" |
| GROWTH_HACK | Non-mainstream acquisition | "Reddit comment strategy for B2B" |
| TOOL_ALPHA | New tool or API worth testing | "This free tool replaces $50/mo subscription" |
| COMPLIANCE | FTC/legal edge case or safe practice | "How Cluely uses AI influencers legally" |
| NICHE_INSIGHT | Market gap or underserved segment | "Faith apps for Orthodox Christians" |
| MONETIZATION | Pricing, offer structure, upsell | "$500 offer structure that converts" |

---

## Filtering Rules (What Gets Staged)

**INCLUDE if:**
- Specific numbers or proof (revenue, conversion rates, etc.)
- Actionable step-by-step process
- New tool or method not in current stack
- Compliance insight that reduces risk
- Niche opportunity matching AI/Faith/Fitness

**EXCLUDE if:**
- Vague motivation content
- Already in LEDGER or MASTER_DOC
- Requires >$1000 upfront investment
- High risk without clear mitigation
- Only works for that specific person's situation

---

## Output Format (ALPHA_STAGING.csv)

```csv
alpha_id,source,source_url,category,title,description,actionable_steps,effort_level,roi_potential,risk_level,applies_to_niches,status,reviewed_date,reviewer_notes
```

**Status values:**
- `PENDING_REVIEW` - Awaiting human review
- `APPROVED` - Human approved, ready to add to main docs
- `REJECTED` - Not useful, logged for pattern learning
- `NEEDS_MORE_INFO` - Promising but need to investigate more

---

## Agent Prompt (For Claude Code Daily Run)

```
You are the PrintMaxx Alpha Research Agent.

TASK: Scan sources for new tactics and stage findings for human review.

INPUTS:
1. LEDGER/HIGH_SIGNAL_SOURCES.csv (accounts to monitor)
2. LEDGER/ALPHA_STAGING.csv (where to add findings)
3. LEDGER/GTM_REVENUE_INTELLIGENCE.md (existing knowledge - don't duplicate)

PROCESS:
1. For each source marked auto_monitor=TRUE:
   - Check for new content (last 24-48 hours)
   - Extract actionable insights
   - Classify using the schema above

2. For each finding:
   - Verify it's not already in existing docs
   - Assess effort/ROI/risk
   - Determine which niches it applies to

3. Add to ALPHA_STAGING.csv with status=PENDING_REVIEW

4. Output summary:
   - Total sources scanned
   - Findings staged for review
   - Categories breakdown

RULES:
- Never auto-approve. All findings go to staging.
- Prefer specific over vague. Numbers > claims.
- Cross-reference: if it works for info products, note if it could work for apps or services.
- Flag compliance-sensitive tactics for extra review.

OUTPUT: Updated ALPHA_STAGING.csv + summary report
```

---

## Learning Loop (Improve Over Time)

Track approval/rejection patterns:

```csv
pattern_id,pattern_type,pattern_description,outcome_bias,confidence
```

Example patterns to learn:
- "User approves @levelsio tactics at 90%+ rate" → weight higher
- "User rejects vague motivation content 100%" → filter out
- "User approves app factory niche plays" → surface more
- "User rejects anything requiring >$500 spend" → filter out

Update filtering based on 20+ data points per pattern.

---

## Manual Trigger

Run anytime with prompt:
```
Run the daily alpha research scan. Check HIGH_SIGNAL_SOURCES for new content and stage findings in ALPHA_STAGING.csv for my review.
```

---

## Integration with Browser

When Chrome extension is connected:
1. Navigate to each X account's profile
2. Scroll recent posts (last 7 days)
3. Extract: text, images, videos, engagement metrics, top replies
4. Screenshot high-signal posts for reference
5. Stage findings with source URLs

---

**Last Updated:** 2026-01-20
