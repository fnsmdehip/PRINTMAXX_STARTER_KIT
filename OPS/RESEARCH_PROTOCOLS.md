# Research Protocols (Daily + Weekly + Comprehensive)
**Last updated:** 2026-02-05
**Extracted from:** CLAUDE.md for context savings

---

## Core principle

ONE SOURCE OF TRUTH: All research goes in LEDGER/*.csv files. Never create separate research docs.

## Where everything lives

| Data Type | File Location | What Goes Here |
|-----------|---------------|----------------|
| New findings | `LEDGER/ALPHA_STAGING.csv` | All new alpha, PENDING_REVIEW status |
| Emerging platforms | `LEDGER/ALPHA_WATCHLIST.csv` | ChatGPT ads, new tools to monitor |
| Sources to scan | `LEDGER/HIGH_SIGNAL_SOURCES.csv` | 140+ sources: X accounts, Reddit, BHW, Twitter communities |
| Subreddits | `LEDGER/RESEARCH_SUBREDDITS.csv` | 40 subreddits organized by category |
| Grey hat filtering | `06_OPERATIONS/research/GREY_HAT_SOURCE_FILTERING.md` | How to filter BHW/communities for legal tactics |
| Edge growth tactics | `06_OPERATIONS/growth/EDGE_GROWTH_TACTICS.md` | Automation limits, services, what's working |
| App playbooks | `LEDGER/APP_FACTORY_METHODS.csv` | Proven app building methods |
| App opportunities | `LEDGER/APP_CLONE_OPPORTUNITIES.csv` | Apps to clone |
| Cross-pollination | `LEDGER/CROSS_POLLINATION_MATRIX.csv` | Method synergies and stacks |
| GTM priorities | `LEDGER/GTM_OPTIMIZATION_PRIORITIES.csv` | ASO/SEO/GEO priority per method |

---

## Daily research (3 parallel tasks at session start)

```bash
# 1. Run the daily research skill (web search + subreddits)
/daily-research

# 2. Review and approve findings
/review-alpha
```

## Weekly edge tactics audit (every Monday)

1. **BlackHatWorld scan** (30 min) - Email Marketing + Social Media sections, last 7 days. Look for ban warnings, algorithm changes, limit changes.
2. **Reddit scan** (20 min) - r/coldemail, r/socialmediamarketing, r/Instagram. Sort by Top - This Week.
3. **Twitter scan** (20 min) - @pipelineabuser, @caiden_cole for email/deliverability updates. Platform announcement accounts.
4. **Update** `06_OPERATIONS/growth/EDGE_GROWTH_TACTICS.md` - Safe limits still accurate? Services stopped working? New methods?

---

## Twitter bookmark alpha extraction (daily)

**Primary method:** Automated Playwright scraper (preferred) or manual console extraction (fallback).

### Automated scraper

**Location:** `AUTOMATIONS/twitter_alpha_scraper.py`

```bash
# Close Chrome first (script needs exclusive access to profile)
# Scrape everything (bookmarks + high-signal accounts)
python3 AUTOMATIONS/twitter_alpha_scraper.py --all

# Just bookmarks
python3 AUTOMATIONS/twitter_alpha_scraper.py --bookmarks

# Just high-signal accounts (limit to top 20)
python3 AUTOMATIONS/twitter_alpha_scraper.py --accounts --limit 20
```

**What it does automatically:**
1. Uses your logged-in Chrome profile (no login needed)
2. Scrolls through Twitter bookmarks
3. Scrapes all auto_monitor=TRUE accounts from HIGH_SIGNAL_SOURCES.csv
4. Filters for business content only (skips memes/lifestyle)
5. Auto-categorizes entries (APP_FACTORY, COLD_OUTBOUND, etc.)
6. Deduplicates against existing ALPHA_STAGING.csv entries
7. Saves new entries with PENDING_REVIEW status
8. Creates JSON backup of raw data

**Accounts:** 89 Twitter accounts marked auto_monitor=TRUE in HIGH_SIGNAL_SOURCES.csv.

**Output:**
- New entries → `LEDGER/ALPHA_STAGING.csv` (status: PENDING_REVIEW)
- Raw JSON → `AUTOMATIONS/twitter_scraper_output/bookmarks_YYYYMMDD_HHMMSS.json`
- Raw JSON → `AUTOMATIONS/twitter_scraper_output/accounts_YYYYMMDD_HHMMSS.json`

### Manual console extraction (fallback)

**Guide:** `AUTOMATIONS/x_bookmarks/MANUAL_EXTRACTION_WORKFLOW.md`

1. Open `https://x.com/i/bookmarks` in browser
2. Open DevTools console (`Cmd+Option+I`)
3. Paste extraction script from MANUAL_EXTRACTION_WORKFLOW.md
4. Run `python3 extract_alpha_from_bookmarks.py --latest`
5. Update `BOOKMARK_EXTRACTION_LOG.md` with session details

---

## Reddit alpha extraction (daily) - 41 subreddits

**Full list:** `LEDGER/RESEARCH_SUBREDDITS.csv` (41 subreddits, all auto_monitor=TRUE)

### Subreddit categories

- **Core:** r/SideProject, r/EntrepreneurRideAlong, r/juststart, r/coldemail, r/indiehackers
- **App/SaaS:** r/AppBusiness, r/SaaS, r/MicroSaas, r/startups
- **Marketing:** r/growthhacking, r/affiliatemarketing, r/SEO, r/bigseo, r/socialmediamarketing
- **Community:** r/Entrepreneur, r/sweatystartup, r/passive_income
- **Platform-specific:** r/YouTube_startups, r/Instagram, r/TikTokCringe, r/newsletters
- **Technical:** r/iOSProgramming, r/reactnative, r/webdev
- **Monetization:** r/Flipping, r/FulfillmentByAmazon, r/ecommerce, r/Etsy
- Plus 14 more specialized subreddits

### Workflow

1. Use Chrome MCP or Python requests to access subreddits
2. Navigate to r/[name]/top/?t=week (top posts this week)
3. Scan top 10-20 posts per subreddit
4. Click into high-value posts (50+ upvotes or 20+ comments)
5. Read top comments for additional insights
6. Extract methodology, specific numbers, proof
7. Filter for business content only
8. Run bot detection + earnings skepticism checks
9. Deduplicate against existing ALPHA_STAGING.csv
10. Append new entries with status: PENDING_REVIEW

### Reddit-specific notes

- **Python requests works best** for Reddit (JSON API): `requests.get("https://www.reddit.com/r/SaaS/top.json?t=week", headers={'User-Agent': 'Mozilla/5.0'})`
- Reddit blocks Playwright/Selenium but requests works
- old.reddit.com works better than new Reddit for scraping
- DO NOT limit to 7-10 subreddits. Research ALL 41.

---

## Comprehensive research protocol (multi-agent)

When comprehensive research requested, launch 10 agents simultaneously:

1. APP_FACTORY opportunities (Product Hunt, GitHub MIT repos)
2. CONTENT_FARM updates (TikTok/YouTube/IG algorithm changes)
3. COLD_OUTBOUND deliverability (email warmup, LinkedIn limits)
4. AI_INFLUENCER monetization (personas, platforms, tools)
5. SEO/GEO/ASO updates (Google, AI citations, app stores)
6. TOOL_ALPHA discoveries (MCP servers, automation, breakthrough tools)
7. EMERGING_NICHES (new underserved markets with proof)
8. NEW_MONEY_METHODS (novel monetization models with revenue proof)
9. CROSS_POLLINATION (method/niche stacks with 85+ synergy)
10. BREAKTHROUGH_TOOLS (10x efficiency or unlock new capabilities)

### Post-research pipeline (automatic, no asking)

1. Deduplicate & consolidate (remove duplicate source_urls)
2. Categorize & organize (create files in `LEDGER/ALPHA_BY_CATEGORY/`)
3. Identify new methods (propose new IDs MM090+)
4. Update cross-pollination matrix
5. Generate content (Zero Waste Protocol - see `OPS/ZERO_WASTE_PROTOCOL.md`)
6. Create playbooks for highest-synergy stacks
7. Flag human review items

---

## Adding new alpha (the right way)

1. **Always append to ALPHA_STAGING.csv** - never create new files
2. **Follow existing format:**
   - `alpha_id`: ALPHA[NNN] (increment from last entry)
   - `source`: Where found (@handle, site name)
   - `category`: APP_FACTORY | CONTENT_FORMAT | OUTBOUND | GROWTH_HACK | TOOL_ALPHA | MONETIZATION
   - `status`: PENDING_REVIEW (human approves before integration)
3. **After approval, integrate into:**
   - APP_FACTORY_METHODS.csv for app building playbooks
   - MARKETING_CHANNELS_MASTER.csv for new channels
   - WINNING_CONTENT_STRUCTURES.csv for content formats

## DO NOT create these files

These should NOT exist (duplicates LEDGER data):
- DAILY_ALPHA_WORKFLOW.md
- APP_CONVERSION_ALPHA.md
- RESEARCH_FINDINGS.md
- Any standalone research docs outside LEDGER/

---

## Discovery engine (7 dimensions, always running)

1. **Geographic Arbitrage** - US apps → India/Indonesia/Brazil/Nigeria (clone + localize)
2. **Demographic Arbitrage** - General apps → women/men/Gen Z/boomer versions
3. **New Niche Discovery** - Reddit communities >100K with pain points + buying power
4. **New Money Method Discovery** - "I made $X" posts → extract method → stress test
5. **Sub-Ops Discovery** - Each method has 5-10 sub-methods (platforms, niches, pricing variants)
6. **Social Meta Discovery** - Platform algorithm changes → format arbitrage opportunities
7. **Emergent Opportunity Discovery** - Adjacent industries, tech changes, regulations, behavior shifts

**Full playbook:** `ralph/loops/mega/DISCOVERY_ENGINE.md`

---

## High-signal source monitoring

Every session, check at least 5 sources from `LEDGER/HIGH_SIGNAL_SOURCES.csv`:
- Prioritize sources marked `auto_monitor=TRUE`
- Extract actionable alpha
- Skip generic engagement bait
- Stage findings to ALPHA_STAGING.csv with proper categorization

---

## MIT/Open source repo strategy

When building apps/tools, ALWAYS search for MIT-licensed repos first:
```
GitHub search patterns:
- "{app name} clone" license:mit
- "{app name} alternative" license:mit
- "react native {category}" license:mit stars:>100
```

**Allowed licenses:** MIT, Apache 2.0, BSD (commercial use OK)
**Avoid:** GPL/AGPL (requires releasing your code)
