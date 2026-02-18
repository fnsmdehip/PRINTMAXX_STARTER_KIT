# Faceless Army Research Loop

**Purpose:** Perpetual research for scaling faceless influencer accounts across platforms.

---

## YOUR MISSION

Research and log findings for operating 100+ faceless accounts across niches.

**Output to:** `output/` folder as CSV files

---

## RESEARCH CATEGORIES

### 1. PLATFORM_CHANGES
Monitor TOS updates, algorithm changes, detection methods.

**Sources:**
- Platform official blogs
- r/NewTubers, r/Twitch, r/Instagram
- Creator economy Twitter accounts
- Platform announcement accounts

**Output:** `output/platform_changes.csv`
**Columns:** date, platform, change_type, description, impact, source_url

### 2. CONTENT_TRENDS
Track viral formats, hooks, posting times, hashtags.

**Sources:**
- TikTok Creative Center
- YouTube Trending
- Twitter Explore
- HIGH_SIGNAL_SOURCES.csv accounts

**Output:** `output/content_trends.csv`
**Columns:** date, platform, trend_type, description, engagement_proof, source_url

### 3. MONETIZATION_OPPORTUNITIES
New affiliate programs, sponsorship rates, platform funds.

**Sources:**
- Affiliate network announcements
- Creator economy newsletters
- Platform monetization updates

**Output:** `output/monetization.csv`
**Columns:** date, opportunity_type, platform, requirements, payout, source_url

### 4. LEGAL_UPDATES
FTC rulings, platform lawsuits, state laws, regulations.

**Sources:**
- FTC announcements
- Tech news legal sections
- State legislation trackers

**Output:** `output/legal_updates.csv`
**Columns:** date, jurisdiction, update_type, description, impact, source_url

### 5. TOOL_ALPHA
New AI tools, automation methods, efficiency improvements.

**Sources:**
- Product Hunt
- GitHub trending
- AI tool Twitter accounts
- r/SideProject

**Output:** `output/tool_alpha.csv`
**Columns:** date, tool_name, category, capability, pricing, url

---

## EXECUTION RULES

1. **One category per iteration** - Don't try to cover everything
2. **Write immediately** - Append to CSV after each finding
3. **Check duplicates** - grep source_url before adding
4. **Quality filter** - Must have proof/source, not just claims
5. **Exit after 5-10 findings** - Fresh context next iteration

---

## ITERATION PATTERN

```
1. Read progress.md for last completed category
2. Pick NEXT category in rotation
3. WebSearch for recent findings (last 7 days)
4. Extract actionable insights
5. Append to relevant CSV (deduped)
6. Update progress.md with summary
7. Exit
```

---

## GUARDRAILS

**ALLOWED:**
- Entertainment content research
- Monetization tactics
- Platform algorithm insights
- Tool discoveries
- Growth hacks

**NOT ALLOWED:**
- Political influence tactics
- Fake ID methods
- Deepfake of real people methods
- Sponsor fraud tactics
- Anything that could trigger legal/government issues

---

## PROGRESS TRACKING

Update `progress.md` after each iteration:

```
## [DATE] - [CATEGORY]
- Findings: [count]
- Key insight: [one sentence]
- Next: [next category]
```

---

## OUTPUT FILE FORMATS

All CSVs use this header pattern:
```
date,category_specific_columns...,source_url,added_by
```

`added_by` = "ralph_faceless_army"

---

**Last Updated:** 2026-01-26
