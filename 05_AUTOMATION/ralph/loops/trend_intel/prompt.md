# Trend Intelligence Research Loop

**Mission:** Identify rising creators, trending niches, and emerging monetization models. Reverse-engineer their funnels. Extract replicable frameworks for PRINTMAXX deployment.

**Why this matters:** The fastest path to revenue is cloning what's already working. Find who's blowing up, figure out exactly how they make money, and adapt their playbook to our niches and methods.

---

## State Files (READ FIRST EVERY ITERATION)

- `.ralph/progress.md` - Which research categories are complete
- `.ralph/guardrails.md` - Learned constraints and quality rules
- `.ralph/errors.log` - What failed (don't retry same iteration)
- `LEDGER/LEDGER_INDEX.md` - All LEDGER files and their purpose
- `LEDGER/TREND_INTEL_TRACKER.csv` - Main output file

---

## Your Task Each Iteration

1. **Read progress.md** - See which categories are incomplete
2. **Pick ONE category** - Highest priority incomplete category
3. **PHASE 1: Scan** - Search for rising creators/trends in that category
4. **PHASE 2: Reverse-engineer** - Map funnels, monetization, distribution for each find
5. **PHASE 3: Extract** - Pull replicable frameworks and gap analysis
6. **PHASE 4: Log** - Write findings to LEDGER/TREND_INTEL_TRACKER.csv
7. **Update progress.md** - Mark category complete with findings summary
8. **Create analysis docs** - For any find with replication_score >= 7, write a brief analysis to `OPS/TREND_INTEL/analyses/`
9. **Exit** - Let next iteration pick next category

---

## PHASE 1: TREND SCANNING

For each research category, use these search patterns to find rising creators and trends.

### Search Query Templates

**Twitter/X:**
- "[niche] blowing up 2026"
- "[niche] creator making money 2026"
- "fastest growing [niche] account"
- "went from 0 to [X]k followers [niche]"
- "@[handle] revenue" for specific creators spotted

**Reddit:**
- r/Entrepreneur "success story" last 30 days, sort by Top
- r/SideProject "[niche] launched" last 30 days
- r/juststart "traffic report" or "income report" last 60 days
- r/passive_income "[method] per month" last 30 days

**Product Hunt:**
- Education/community products launched last 30 days
- Trending products in self-improvement, coaching, fitness
- Products with 500+ upvotes in relevant categories

**TikTok/YouTube (search via web):**
- "trending [niche] creator 2026"
- "[niche] funnel breakdown" on YouTube
- "how [creator name] makes money"
- "[niche] skool community review"

**Skool/Community:**
- "fastest growing Skool communities 2026"
- "Skool community [niche] members"
- "paid community [niche] making money"
- skool.com/discovery for trending groups

**SimilarWeb/Traffic:**
- "trending education sites 2026"
- "fastest growing coaching websites"
- "[niche] site traffic growing"

### What to Look For

- **Follower velocity** - Growing 10K+/month = signal
- **Revenue proof** - Screenshots, mentions of income, lifestyle indicators
- **Engagement ratio** - High engagement relative to follower count
- **Content consistency** - Regular posting cadence means business not hobby
- **Monetization stack** - Multiple revenue streams = sophisticated operator
- **Unique mechanism** - Proprietary frameworks, branded methods
- **Distribution innovation** - Novel acquisition strategies

---

## PHASE 2: FUNNEL REVERSE-ENGINEERING

For each creator/trend identified, map these elements:

### Traffic Source Analysis
- Which platforms are they most active on?
- What's their primary platform vs. distribution platforms?
- Approximate follower/subscriber counts across platforms
- Content frequency and format patterns
- Are they running ads? (check Facebook Ad Library, TikTok Ad Library)
- Do they have a clipping army or affiliate network?

### Monetization Stack Mapping
Map their full revenue stack in order of likely revenue contribution:

| Revenue Stream | Price Point | Estimated Monthly Revenue |
|----------------|-------------|--------------------------|
| Community (Skool, Discord, etc.) | $X/mo | $X |
| Course/Info Product | $X one-time | $X |
| 1:1 Coaching | $X/session | $X |
| Affiliate deals | Various | $X |
| Sponsorships | $X/post | $X |
| Digital products | $X each | $X |
| Physical products | $X each | $X |
| Ad revenue | CPM-based | $X |
| Other | | $X |

### VSSL/Sales Page Analysis
If they have a visible sales funnel:
- What's the hook/headline?
- What's the unique mechanism name? (e.g., "The 5AM Method", "The Creator Flywheel")
- What objections do they address?
- What social proof do they use?
- What's the CTA structure?
- What's the urgency/scarcity play?
- Price anchoring strategy?

### Distribution Strategy
- Organic vs. paid split (estimate)
- Content-to-offer pipeline (how do free followers become customers?)
- Lead magnet or free offer?
- Email/SMS capture mechanism?
- Referral or affiliate program?
- Cross-platform syndication strategy?
- Collaboration/podcast/guest strategy?

### Tech Stack Identification
Note any visible tools:
- Website builder (Framer, Webflow, WordPress, Carrd)
- Community (Skool, Circle, Discord, Heartbeat)
- Course platform (Kajabi, Teachable, Podia, Thinkific)
- Email (ConvertKit, Beehiiv, Mailchimp)
- Payment (Stripe, Gumroad, Whop, Stan.store)
- Video (YouTube, Wistia, Vimeo)
- Scheduling (Calendly, Cal.com)
- CRM (HubSpot, GoHighLevel)

---

## PHASE 3: PATTERN EXTRACTION

After analyzing each creator/trend, extract:

### Replicable Frameworks
- What specific method or framework can we adapt?
- What content format is driving their growth?
- What pricing model is working?
- What distribution hack are they using?

### Underserved Niches
- Is this niche being served well or is there room?
- What adjacent niches are completely empty?
- What demographic within the niche is ignored?

### Distribution Tactics
- What acquisition channel is overperforming?
- What content format gets disproportionate reach?
- What platform feature are they exploiting?

### Monetization Models
- What monetization model is proving out?
- What price points are working?
- What upsell/downsell structure converts?

### Gap Analysis for PRINTMAXX
- What could we do better/differently?
- Which PRINTMAXX methods (MM001-MM069) could we apply here?
- What's the fastest path to replicate the revenue model?
- What infrastructure do we already have that applies?

---

## PHASE 4: LOGGING

### Primary Output: LEDGER/TREND_INTEL_TRACKER.csv

**Columns (must match existing CSV header exactly):**
```
trend_id,date_identified,influencer_name,handle,niche,platform,followers,monetization_model,est_mrr,unique_mechanism,distribution_strategy,tech_stack,replication_score,printmaxx_methods,funnel_type,analysis_doc,status,notes
```

**Column definitions:**
- `trend_id`: TREND[NNN] - increment from last entry (currently at TREND001)
- `date_identified`: YYYY-MM-DD
- `influencer_name`: Real name or brand name
- `handle`: @handle or URL
- `niche`: Primary niche (fitness, faith, finance, self-improvement, etc.)
- `platform`: Primary platform with follower counts if multi-platform (e.g., "TikTok (700K) | Instagram (237K)")
- `followers`: Total approximate follower count across platforms
- `monetization_model`: Full monetization stack description (community, course, coaching, affiliate, etc.)
- `est_mrr`: Estimated monthly recurring revenue (numeric or range: $1K-5K, $5K-20K, $20K-100K, $100K+)
- `unique_mechanism`: Their branded method/framework name if any
- `distribution_strategy`: Primary acquisition strategy (organic social, ads, affiliates, clipping army, etc.)
- `tech_stack`: Key tools identified (Skool + Framer + ConvertKit, etc.)
- `replication_score`: 1-10 how replicable is this for PRINTMAXX (10 = copy tomorrow)
- `printmaxx_methods`: Which MM/CF/AI methods apply, pipe-separated (e.g., "AI001|AI005|CF001-CF013")
- `funnel_type`: Funnel structure summary (e.g., "Content -> Clipping Army -> VSSL -> Community -> High-Ticket")
- `analysis_doc`: Path to analysis doc if created (e.g., "OPS/TREND_INTEL/analyses/NAME.md"), empty if none
- `status`: PENDING_REVIEW (human approves integration) or ANALYZED (human has reviewed)
- `notes`: Key insight or why this matters

### Deduplication Check

Before appending any entry:
1. Read LEDGER/TREND_INTEL_TRACKER.csv
2. Check if `handle` already exists
3. If exists, only add if significantly new information (update notes)
4. If new, append row

### High-Value Analysis Docs

For any finding with `replication_score >= 7`, create a brief analysis document:

**Location:** `OPS/TREND_INTEL/analyses/TREND[NNN]_[handle].md`

**Template:**
```markdown
# TREND[NNN]: [Influencer/Brand Name]

**Handle:** @[handle]
**Niche:** [niche]
**Platform:** [primary platform]
**Est. MRR:** $[X]
**Replication Score:** [X]/10
**Date Analyzed:** [YYYY-MM-DD]

## What They're Doing
[2-3 sentences on their model]

## Funnel Map
[Traffic source] -> [Lead capture] -> [Nurture] -> [Offer] -> [Upsell]

## Monetization Stack
1. [Revenue stream 1] - $[X]/mo
2. [Revenue stream 2] - $[X]/mo
3. [Revenue stream 3] - $[X]/mo

## Unique Mechanism
[What do they call their method? What makes it "theirs"?]

## Replicable Frameworks
1. [Framework 1]
2. [Framework 2]

## PRINTMAXX Application
- **Methods:** [Which MM/CF/AI codes apply]
- **Niche adaptation:** [How we'd adapt to our niches]
- **Timeline:** [How fast could we replicate]
- **Missing infrastructure:** [What we'd need to build/buy]

## Gap/Weakness
[What are they doing poorly that we could exploit?]
```

---

## Research Categories (Rotate Through)

### 1. SKOOL_COMMUNITIES
**Goal:** Find 3+ trending/growing Skool communities with identifiable revenue

**Search patterns:**
- "fastest growing Skool communities 2026"
- "Skool community making money"
- "Skool leaderboard" + "[niche]"
- "joined [X] Skool community review"
- Check skool.com/discovery for trending groups

**What to extract:**
- Community name and creator
- Member count and growth rate
- Price point ($29/mo, $49/mo, $99/mo, etc.)
- Niche and target demographic
- Content/value proposition inside the community
- Creator's external platforms and follower counts
- How they drive members (organic, ads, affiliates)

**Quality bar:** 100+ paid members OR creator has 50K+ followers

### 2. TIKTOK_CREATORS
**Goal:** Find 3+ rising TikTok creators with clear monetization in relevant niches

**Search patterns:**
- "TikTok creator [niche] blowing up 2026"
- "TikTok [niche] making money"
- "[niche] TikTok Shop" success stories
- "viral TikTok [self-improvement/fitness/faith/productivity]"
- r/TikTokHelp success stories

**Niches to prioritize:**
- Self-improvement / looksmaxxing / productivity
- Faith / spirituality / manifestation
- Fitness / supplements / biohacking
- Finance / side hustles / crypto
- AI tools / tech tutorials

**What to extract:**
- Handle, follower count, avg views per video
- Content format (talking head, voiceover, POV, duets, etc.)
- Posting frequency
- Monetization (TikTok Shop, bio link, course, community, etc.)
- What hook patterns work for them
- Whether they use clippers/reposters

**Quality bar:** 50K+ followers OR $1K+/month estimated

### 3. YOUTUBE_EDUCATORS
**Goal:** Find 3+ YouTube education/coaching channels growing fast

**Search patterns:**
- "YouTube channel [niche] growing fast 2026"
- "how [creator] makes money YouTube"
- "[niche] course creator YouTube"
- YouTube channels under 100K subs with high view counts
- "YouTube educator [niche] income report"

**Niches to prioritize:**
- Business/entrepreneur education
- AI/tech tutorials
- Self-improvement/productivity
- Faith-based content
- Fitness/health optimization

**What to extract:**
- Channel name, subscriber count, avg views
- Content format and length
- Upload frequency
- Monetization beyond AdSense (courses, community, consulting)
- Funnel from YouTube to paid products
- Whether they run YouTube Shorts as distribution

**Quality bar:** 10K+ subscribers OR visible course/community business

### 4. TWITTER_BUILDERS
**Goal:** Find 3+ Twitter/X accounts building in public with revenue proof

**Search patterns:**
- "building in public [niche] revenue" on Twitter
- "MRR update" or "revenue update" tweets with numbers
- "#buildinpublic" recent high-engagement posts
- "[niche] solopreneur making money 2026"
- Accounts growing 5K+ followers/month

**What to extract:**
- Handle, follower count, follower growth rate
- What they're building (SaaS, community, products, etc.)
- Revenue numbers (MRR, one-time sales, etc.)
- Content style and frequency
- Distribution (threads, tips, behind-the-scenes)
- How they convert followers to customers

**Quality bar:** $1K+/month revenue proof OR 20K+ followers with clear monetization

### 5. NICHE_MOVEMENTS
**Goal:** Find 2+ emerging niche movements (like looksmaxxing, biohacking were)

**Search patterns:**
- "[new term]maxxing" trending on social media
- New subreddits with 10K+ members in last 6 months
- "new trend [self-improvement/health/productivity]"
- "movement [niche] growing"
- Google Trends for rising search terms in relevant categories
- TikTok hashtag views spiking

**What to extract:**
- Movement name and origin
- Core demographic
- Key influencers/founders
- How it's being monetized (or not yet = opportunity)
- Adjacent movements and crossover potential
- Products/services being created around it
- Content formats dominating the space

**Quality bar:** 10K+ social media mentions OR dedicated subreddit with 5K+ members

### 6. FUNNEL_INNOVATIONS
**Goal:** Find 3+ novel funnel structures, pricing models, or tech stack innovations

**Search patterns:**
- "funnel that converts [niche]"
- "new pricing model [SaaS/course/community]"
- "sales page structure that works 2026"
- "VSSL funnel" or "video sales letter [niche]"
- "reverse trial" or "freemium conversion" case studies
- Product Hunt for new funnel/marketing tools

**What to extract:**
- Funnel structure (awareness -> lead -> nurture -> close -> upsell)
- Specific conversion rates if available
- Tech stack powering the funnel
- Pricing strategy (free trial, reverse trial, money-back, etc.)
- Copy/messaging frameworks used
- What makes it different from standard funnels

**Quality bar:** Documented conversion rates OR novel structure not in our playbooks

### 7. CLIPPING_NETWORKS
**Goal:** Find 2+ creator clipping/distribution networks and their economics

**Search patterns:**
- "clipping army [creator name]"
- "short form content agency"
- "clip and repost [niche] making money"
- "faceless channel network"
- "content distribution network creators"
- r/YouTubers "clipping" discussions

**What to extract:**
- Network/operator name
- Number of channels/accounts managed
- Content sources (which creators are they clipping)
- Revenue model (rev share, flat fee, ad revenue split)
- Tech stack for clipping (Opus.pro, Gling, manual, etc.)
- Distribution platforms (TikTok, YouTube Shorts, Reels, etc.)
- Economics: cost per clip, revenue per clip, margin

**Quality bar:** 5+ channels managed OR $2K+/month revenue

### 8. COMMUNITY_MODELS
**Goal:** Find 3+ paid community models with innovative pricing or structure

**Search patterns:**
- "paid community model 2026"
- "community pricing strategy"
- "Skool vs Circle vs Discord" comparisons
- "community-led growth [niche]"
- "how to monetize a community"
- "community flywheel" case studies

**What to extract:**
- Community name and platform (Skool, Circle, Discord, custom)
- Pricing tiers and what's included at each
- Member count and growth trajectory
- Retention rate indicators (how long do members stay)
- Value delivery method (calls, content library, networking, challenges)
- Community-to-product pipeline (do they upsell to courses, coaching, etc.)
- Unique engagement mechanics (gamification, challenges, accountability)

**Quality bar:** 50+ paid members OR documented retention/revenue data

---

## Critical Rules

1. **Write to disk immediately** - Don't accumulate findings in memory
2. **One category per iteration** - Don't try to do all 8 at once
3. **Append to CSV files** - Never overwrite existing entries (use >> not >)
4. **Read before writing** - Check existing entries to avoid duplicates
5. **Use WebSearch extensively** - This is a research-first loop
6. **Require proof** - Revenue numbers, follower counts, engagement data, or credible estimates
7. **Update progress.md** - Mark complete with 2-3 sentence summary after each category
8. **No human approval needed for research** - These are findings, not actions. Status = PENDING_REVIEW for human integration decisions
9. **Create analysis docs for high-value finds** - replication_score >= 7 gets a full doc in OPS/TREND_INTEL/analyses/
10. **Cross-reference PRINTMAXX methods** - Every finding must map to at least 1 method from LEDGER/MONEY_METHODS_TRACKER.csv

---

## Quality Bar (Must Pass ALL)

Only log a finding if:
- Creator has **10K+ followers** on their primary platform OR **$1K+/month estimated revenue**
- There's an **identifiable funnel or monetization model** (not just "posts content")
- We can extract at **least 2 replicable frameworks** (content format, pricing, distribution, etc.)
- Relevant to at **least 1 PRINTMAXX method** (MM001-MM069, CF001-CF013, AI001-AI008)
- **Not already in LEDGER/TREND_INTEL_TRACKER.csv** (check handle column)

---

## Replication Score Guide

| Score | Meaning | Criteria |
|-------|---------|----------|
| 10 | Copy tomorrow | We have all infrastructure, just need to execute |
| 9 | Copy this week | Minor setup needed (1-2 hours) |
| 8 | Copy in 2 weeks | Need some new tools or accounts |
| 7 | Copy in 1 month | Need significant new infrastructure |
| 6 | Adapt in 1-2 months | Need to modify approach for our niches |
| 5 | Partial replication | Some elements applicable, not full model |
| 4 | Inspiration only | Interesting but different context |
| 3 | Long-term reference | May be relevant in 3-6 months |
| 2 | Tangentially related | Different market/model but interesting pattern |
| 1 | Archive only | Novel but not applicable to PRINTMAXX |

---

## File Write Safety

Before appending to TREND_INTEL_TRACKER.csv:
1. Read the file to check current entries and last trend_id
2. Check if handle/influencer already exists
3. If new, increment trend_id from last entry
4. Append new row with all columns filled
5. Verify write by reading back the last line

Before creating analysis docs:
1. Check if OPS/TREND_INTEL/analyses/TREND[NNN]_[handle].md already exists
2. If exists, only update if significantly new info
3. If new, create from template above

---

## On Errors

If a category fails:
1. Log error to `.ralph/errors.log` with timestamp and category
2. Add constraint to `.ralph/guardrails.md` if it's a repeatable issue
3. Mark category as BLOCKED in progress.md with reason
4. Move to next category (don't retry in same loop run)

---

## Success Criteria

Loop completes when ALL 8 categories are marked complete in progress.md.

Each category complete means:
- Minimum findings count met (see per-category goals)
- All findings written to LEDGER/TREND_INTEL_TRACKER.csv
- High-value finds (replication_score >= 7) have analysis docs
- Progress.md updated with summary
- No unlogged errors

When all 8 categories complete, output: `<promise>COMPLETE</promise>`

---

## Cross-Reference Files

When evaluating findings, check these existing LEDGER files for overlap:
- `LEDGER/MONEY_METHODS_TRACKER.csv` - All 88 tracked methods
- `LEDGER/ALPHA_STAGING.csv` - Recent alpha discoveries
- `LEDGER/CROSS_POLLINATION_MATRIX.csv` - Method synergies
- `LEDGER/HIGH_SIGNAL_SOURCES.csv` - Already-tracked accounts
- `LEDGER/NICHES.csv` - Existing niche definitions

If a trend finding overlaps with existing alpha, note it in the `notes` column and cross-reference the alpha_id.

---

**Remember:** Each iteration starts fresh. Read state from files. Write findings to disk. Update progress. Exit. The next iteration picks up where you left off.
