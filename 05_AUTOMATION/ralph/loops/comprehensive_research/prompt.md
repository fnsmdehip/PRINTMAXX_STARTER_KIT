# Comprehensive Multi-Method Research Loop

**Mission:** Find actionable opportunities across ALL money methods, niches, tools, and cross-pollination stacks.

---

## State Files (DO NOT MODIFY THESE DIRECTLY)

Read these files for current state:
- `.ralph/progress.md` - What research categories are complete
- `.ralph/guardrails.md` - Learned constraints
- `LEDGER/LEDGER_INDEX.md` - All LEDGER files and their purpose

---

## Your Task Each Iteration

1. **Read progress.md** - See which categories are incomplete
2. **Pick ONE category** - The highest priority incomplete category
3. **Execute research** - Follow the category-specific instructions below
4. **Write results to disk** - Update appropriate LEDGER/*.csv files
5. **Update progress.md** - Mark category complete with findings summary
6. **Exit** - Let next iteration pick next category

---

## Research Categories (Priority Order)

### 1. EMERGING_NICHES
**Goal:** Find 3+ new underserved niches with monetization proof

**Sources:**
- Web search: "[demographic] struggling with [problem]" high engagement tweets
- Reddit: New subreddits 50k+ members formed last year
- Product Hunt: Apps serving niche audiences
- Search "underserved market 2026" "niche business ideas"

**Output:** Add to `LEDGER/NICHES.csv`
- Columns: niche_id (N021+), niche_name, target_demo, core_pain_points, existing_products, monetization_proof, applicable_methods
- Must have: Real revenue proof, cross-pollination with existing methods

### 2. NEW_MONEY_METHODS
**Goal:** Find 2+ novel monetization models not in our 39 methods

**Sources:**
- Twitter: "How I made $X in 2026" with actual numbers
- r/Entrepreneur, r/SideProject success stories (last 30 days)
- Indie Hackers new revenue models
- @levelsio, @tdinh_me recent posts

**Output:** Add to `LEDGER/MONEY_METHODS_TRACKER.csv`
- Columns: method_id (MM017+), method_name, revenue_model, startup_cost, proof_url, applicable_niches
- Must have: $1k+/mo revenue proof, replicable with our stack

### 3. CROSS_POLLINATION
**Goal:** Find 5+ high-synergy stacks (score 85+)

**Sources:**
- Read existing `LEDGER/CROSS_POLLINATION_MATRIX.csv`
- Search "I use X to grow Y" posts
- Case studies stacking multiple revenue streams
- @gregisenberg community strategies

**Output:** Update `LEDGER/CROSS_POLLINATION_MATRIX.csv`
- Add new combinations with synergy_score, mechanism, asset_sharing, implementation_sequence
- Must have: Specific synergy mechanism, not just "works well together"

### 4. BREAKTHROUGH_TOOLS
**Goal:** Find 3+ tools that enable NEW capabilities (not just faster)

**Sources:**
- GitHub trending (last 30 days, AI/automation)
- Product Hunt Developer Tools
- Search "replaced my developer with [tool]"
- New MCP servers

**Output:** Add to `LEDGER/ALPHA_STAGING.csv`
- Category: TOOL_ALPHA, ROI: HIGHEST if enables new method
- Must have: Novel capability unlocked, not incremental improvement

### 5. APP_FACTORY_OPPORTUNITIES
**Goal:** Find 10+ high-revenue apps to clone

**Sources:**
- appkittie.com "New big hits"
- Product Hunt Mobile apps
- r/AppBusiness revenue posts
- GitHub MIT-licensed React Native apps

**Output:** Add to `LEDGER/APP_CLONE_OPPORTUNITIES.csv`
- Must have: Revenue estimate, niche adaptation, MIT repo if exists

### 6. CONTENT_FARM_UPDATES
**Goal:** Find 10+ current platform tactics

**Sources:**
- Search "TikTok algorithm 2026" "YouTube Shorts"
- r/NewTubers, r/TikTokHelp (last 30 days)
- @maverickecom, @Jonnyvandel posts
- "faceless YouTube channel" case studies

**Output:** Add to `LEDGER/ALPHA_STAGING.csv` (category: CONTENT_FARM)
**And:** Update `LEDGER/WINNING_CONTENT_STRUCTURES.csv`

### 7. COLD_OUTBOUND_UPDATES
**Goal:** Find 10+ deliverability/automation tactics

**Sources:**
- @pipelineabuser, @caiden_cole recent tweets
- r/coldemail top posts (last 30 days)
- Search "cold email deliverability 2026"
- BHW Email Marketing section (legal tactics only)

**Output:** Add to `LEDGER/ALPHA_STAGING.csv` (category: OUTBOUND)
**And:** Update `OPS/EDGE_GROWTH_TACTICS.md` if limits changed

### 8. AI_INFLUENCER_MONETIZATION
**Goal:** Find 5+ monetizable personas/tactics

**Sources:**
- Search "AI influencer" "synthetic content creator"
- r/ArtificialIntelligence monetization threads
- @maverickecom AI UGC updates
- "AI ASMR" "AI fitness coach" revenue

**Output:** Add to `LEDGER/ALPHA_STAGING.csv` (category: AI_INFLUENCER)

### 9. SEO_GEO_ASO_UPDATES
**Goal:** Find 10+ current optimization tactics

**Sources:**
- Search "Google algorithm update 2026"
- @lilyraynyc, @JohnMu tweets
- r/SEO, r/bigseo (last 30 days)
- "ChatGPT citations" "Perplexity SEO"

**Output:** Add to `LEDGER/ALPHA_STAGING.csv` (category: SEO_GEO_ASO)
**And:** Update `OPS/GTM_OPTIMIZATION_CHECKLIST.md` with new tactics

### 10. MONETIZATION_TACTICS
**Goal:** Find 8+ pricing/upsell/conversion tactics

**Sources:**
- Search "pricing psychology 2026"
- @yegormethod sales posts
- r/SaaS monetization threads
- Successful paywall case studies

**Output:** Add to `LEDGER/ALPHA_STAGING.csv` (category: MONETIZATION)

---

## Critical Rules

1. **Write to disk immediately** - Don't accumulate findings in memory
2. **One category per iteration** - Don't try to do multiple
3. **Append to CSV files** - Never overwrite existing entries
4. **Use WebSearch extensively** - This is a research task
5. **Require proof** - Revenue numbers, engagement proof, GitHub stars
6. **Check for duplicates** - grep existing files before adding
7. **Update progress.md** - Mark complete with 2-3 sentence summary
8. **No human approval needed** - These are research findings, not actions

---

## File Write Safety

Before appending to any CSV:
```bash
# Check if entry already exists
grep "search_term" LEDGER/FILE.csv
# If not found, append
echo "new_row" >> LEDGER/FILE.csv
```

---

## Success Criteria

Loop completes when ALL 10 categories marked complete in progress.md.

Each category complete means:
- Minimum findings count met
- All findings written to appropriate LEDGER files
- Progress.md updated with summary
- No errors in .ralph/errors.log

---

## On Errors

If category fails:
1. Log error to `.ralph/errors.log`
2. Add constraint to `.ralph/guardrails.md`
3. Mark category as BLOCKED in progress.md
4. Move to next category

Don't retry failed categories in same loop run.

---

**Remember:** Each iteration starts fresh. Read state from files. Write findings to disk. Update progress. Exit.
