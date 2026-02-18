# Comprehensive Alpha Research Ralph Loop

**Task:** Deep research across ALL high-signal sources for actionable alpha

**Reference Files:**
- `LEDGER/HIGH_SIGNAL_SOURCES.csv` - 81+ accounts, subreddits, sources
- `LEDGER/RESEARCH_SUBREDDITS.csv` - 40 research + launch subreddits
- `AUTOMATIONS/NICHE_META_DETECTOR.md` - Meta detection framework
- `LEDGER/ALPHA_STAGING.csv` - Where findings go

## Research Sources (Prioritized)

### S-Tier Sources (Scan Every Iteration)
- @pipelineabuser - Cold email mastery, outbound tactics
- @levelsio - Indie hacking, real numbers
- @tdinh_me - Technical builds, honest results
- @codyschneiderxx - SaaS growth, LinkedIn hacks
- @paborns - ASO optimization, app store tactics
- r/SideProject - 430K members, product launches
- r/Entrepreneur - 4.8M members, broad entrepreneurship

### A-Tier Sources (Scan 50% of iterations)
- @dannypostmaa, @marc_louvion - Structured how-tos
- @gregisenberg - Startup ideas
- @tatealax - Growth hacking
- r/juststart, r/SEO - Content site arbitrage
- r/coldemail - Email deliverability
- r/indiehackers - Method validation

### B-Tier Sources (Scan 25% of iterations)
- @yegormethod - Sales psychology
- @Jonnyvandel - Mass content automation
- appkittie.com - App store movers
- Product Hunt - New launches
- r/AppBusiness - App monetization

## Research Categories

For each source, extract alpha in these categories:

1. **APP_FACTORY** - App building, monetization, ASO
2. **CONTENT_FARM** - Content formats, platform algorithms
3. **COLD_OUTBOUND** - Email/LinkedIn tactics, deliverability
4. **AI_INFLUENCER** - Persona monetization, platforms
5. **SEO_GEO_ASO** - Search optimization, AI citations
6. **TOOL_ALPHA** - New tools, breakthrough capabilities
7. **EMERGING_NICHES** - New underserved markets
8. **NEW_MONEY_METHODS** - Novel monetization models
9. **CROSS_POLLINATION** - Method/niche stacks
10. **PLATFORM_ARBITRAGE** - RPM/conversion arbitrage

## Alpha Quality Criteria

Only extract if it has:
- Specific numbers (revenue, conversion rates, timeframes)
- Replicable framework or method
- Proof (case study, views, revenue screenshot, GitHub stars)
- Actionable within our current stack

## Bot Detection (MANDATORY)

Before trusting metrics, check:
- Engagement ratio normal? (10K likes with 3 comments = botted)
- Comments substantive or just "🔥🔥🔥"?
- Account age vs follower count reasonable?
- Mark suspicious: `engagement_authenticity: SUSPICIOUS`

## Earnings Skepticism (MANDATORY)

Default stance: Assume claims are inflated until proven otherwise.

- Round numbers ($50K vs $47,382) = likely inflated
- Selling to people who want to make money = skeptical
- Screenshot provided? (still fakeable)
- Mark unverified: `earnings_verified: FALSE`

**STILL extract the method even if numbers are BS.**

## Output Format

Append to `LEDGER/ALPHA_STAGING.csv`:
```
alpha_id,source,source_url,category,status,roi_potential,tactic_summary,specific_numbers,proof_provided,engagement_authenticity,earnings_verified,applicable_methods,cross_niche_adaptations,created_date
```

## Deduplication

Before adding any entry:
1. Check if `source_url` already exists in ALPHA_STAGING.csv
2. If exact duplicate, skip
3. If similar but different angle, add with note

## Progress Tracking

Use `.ralph/progress.md` to track:
- Sources scanned this iteration
- Alpha entries added
- Duplicates skipped
- Categories covered
- Next source to scan

## Workflow Per Iteration

1. Check progress.md for next source to scan
2. Scan that source (WebSearch for recent posts/content)
3. Extract alpha using quality criteria
4. Run bot detection + earnings skepticism checks
5. Check for duplicates
6. Append to ALPHA_STAGING.csv
7. Update progress.md
8. Exit (next iteration starts fresh)

## Rotation Strategy

- Iteration 1: S-tier source 1
- Iteration 2: S-tier source 2
- Iteration 3: S-tier source 3
- Iteration 4: A-tier source
- Iteration 5: S-tier source 4
- Iteration 6: B-tier source
- Repeat pattern

## Safety Rules

- Read only, no bash commands
- Append to CSV, don't overwrite
- Check for duplicates before adding
- All file writes within project directory only
- WebSearch and WebFetch allowed

## Success Criteria

- Scan 30+ high-signal sources
- Extract 50+ alpha entries
- Cover all 10 categories
- Flag 10+ cross-pollination opportunities
- Identify 3+ new money methods
