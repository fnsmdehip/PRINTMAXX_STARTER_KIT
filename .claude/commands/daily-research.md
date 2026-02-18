---
name: daily-research
description: Run daily alpha research scan. Stages findings for human greenlight before integration.
model: haiku
---

# Daily Alpha Research Run

Scan high-signal sources for new tactics, tools, and methods. Stage findings for human approval before integrating into LEDGER.

## Process

### Step 1: Scan Sources
Read LEDGER/HIGH_SIGNAL_SOURCES.csv and check recent content from:
- X accounts (56+ high-signal follows including @Hightrafficsite, @iamgdsa, @jasoncfox, @wesocialgrowth)
- Reddit communities (6 subreddits)
- YouTube channels (4 channels)
- Tools/websites (4 sources)

**Priority X accounts for tools/tactics/repurposing:**
- @iamgdsa - Creator marketing, FindMeCreators/Shortimize alpha, micro-influencer tactics
- @Hightrafficsite - SEO arbitrage, high-traffic content strategies
- @jasoncfox - Marketing funnels, agency tactics, growth hacks
- @wesocialgrowth - Platform-specific growth, content format ideas

### Step 2: Extract Alpha
For each potential finding, evaluate:
- Is it actionable within $200-500 budget?
- Does it have proof of working (numbers, results)?
- Is it new (not already in our LEDGER files)?
- Does it align with 3 niches or meta-brand?

### Step 3: Stage for Review
Write findings to LEDGER/ALPHA_STAGING.csv with:
- alpha_id: ALPHA[NNN]
- source: Where found
- category: APP_FACTORY | CONTENT_FORMAT | OUTBOUND | GROWTH_HACK | TOOL_ALPHA | CHANNEL | MONETIZATION
- summary: 1-2 sentence description
- proof: Numbers/results that validate it
- actionable_steps: How to implement
- status: PENDING_REVIEW

### Step 4: Report Summary
Output:
- Sources scanned
- New findings staged (count)
- Categories breakdown
- Recommendation for priority review

## Human Greenlight Flow

After running `/daily-research`:
1. Review ALPHA_STAGING.csv entries marked PENDING_REVIEW
2. For each entry, decide: APPROVED or REJECTED
3. Run `/review-alpha` to integrate approved entries into:
   - APP_FACTORY_METHODS.csv
   - MARKETING_CHANNELS_MASTER.csv
   - WINNING_CONTENT_STRUCTURES.csv
   - TOOLS_SERVICES_MASTER.csv

## Arguments

- `--platform [X|Reddit|YouTube|Web]` - Filter by platform
- `--tier [HIGHEST|HIGH|MEDIUM]` - Filter by signal tier
- `--dry-run` - Preview without writing to staging

Example: `/daily-research --platform X --tier HIGHEST`

## Output

Creates/updates:
- LEDGER/ALPHA_STAGING.csv (new entries)
- OPS/logs/RESEARCH_[date].md (run log)
