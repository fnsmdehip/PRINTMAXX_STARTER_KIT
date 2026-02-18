# PRD: Twitter Bookmark Deep Extraction System

## Introduction

Extract maximum value from X/Twitter bookmarks with deep analysis of replies, profiles, and funnels. This is a daily alpha source that should run on first session of each day.

## Alpha Stack Reference

**Extraction Scripts:** `AUTOMATIONS/x_bookmarks/`
- `QUICK_START.md` - Basic extraction instructions
- `deep_bookmark_scraper.js` - Full post text, images, funnel detection
- `profile_scraper.js` - Bio, banner, profile pics
- `extract_alpha_from_bookmarks.py` - Process to ALPHA_STAGING.csv
- `DEEP_EXTRACTION_CHECKLIST.md` - Comprehensive extraction guide
- `BOOKMARK_EXTRACTION_LOG.md` - Track progress between runs

**Output Files:**
- `LEDGER/ALPHA_STAGING.csv` - New alpha (PENDING_REVIEW status)
- `LEDGER/HIGH_SIGNAL_SOURCES.csv` - Accounts to follow
- `LEDGER/PROFILE_ANALYSIS.csv` - Bio copy inspiration
- `LEDGER/CONTENT_ASSETS.csv` - Images for repurposing
- `LEDGER/FUNNEL_PATTERNS.csv` - Product/content pairings

**Reference Files:**
- `.claude/CLAUDE.md` → Twitter Bookmark Alpha Extraction section
- `.claude/CLAUDE.md` → DAILY RESEARCH SYSTEM section

## Goals

- Extract all new bookmarks since last run
- Capture full post text (expand "Show more")
- Analyze top replies for funnel patterns
- Capture author profile data (bio, links, banners)
- Dedupe against existing ALPHA_STAGING entries
- Add high-signal accounts to HIGH_SIGNAL_SOURCES.csv

## Data to Capture Per Bookmark

### Standard Data
- Post URL and status ID
- Author handle and display name
- Full post text
- Post date
- Engagement metrics (likes, retweets, replies)
- Images/media URLs
- Links in post

### Deep Data (High-Value Posts)
Revenue numbers, case studies, playbooks get extra analysis:
- Top 3-5 replies (especially author replies with links)
- Author bio text
- Author bio link (often the product URL)
- Author profile pic URL
- Author banner URL
- Author follower count

### Funnel Detection Patterns
Look for in replies and bio:
- "Link in bio"
- "DM me for..."
- Product/course/template mentions
- Waitlist/newsletter signups
- Booking links (calendly, etc.)
- Price mentions ($XX, $XXk)

## User Stories

### US-001: Check existing alpha entries
**Description:** As a researcher, I need to know what's already captured to avoid duplicates.

**Acceptance Criteria:**
- [ ] Read ALPHA_STAGING.csv source_url column
- [ ] Create list of already-captured URLs
- [ ] Note last extraction date from BOOKMARK_EXTRACTION_LOG.md
- [ ] Output: Set of existing URLs for deduplication

### US-002: Extract new bookmarks via browser
**Description:** As a researcher, I need to scrape new bookmarks from X.

**Acceptance Criteria:**
- [ ] Navigate to x.com/i/bookmarks
- [ ] Scroll through all bookmarks
- [ ] Capture standard data for each post
- [ ] Skip posts already in ALPHA_STAGING
- [ ] Export to JSON file

### US-003: Deep analyze high-value posts
**Description:** As a researcher, I need detailed analysis of posts with revenue/growth signals.

**Acceptance Criteria:**
- [ ] Identify posts with revenue keywords (mrr, $XXk, revenue)
- [ ] Click into each high-value post
- [ ] Capture top 5 replies
- [ ] Capture author profile data
- [ ] Detect funnel patterns in replies/bio

### US-004: Add alpha to ALPHA_STAGING.csv
**Description:** As a researcher, I need to add new findings to the ledger.

**Acceptance Criteria:**
- [ ] Format entries per ALPHA_STAGING.csv schema
- [ ] Assign alpha_id (increment from last ALPHAXXXX)
- [ ] Set status to PENDING_REVIEW
- [ ] Categorize: APP_FACTORY, CONTENT_FORMAT, OUTBOUND, GROWTH_HACK, TOOL_ALPHA, MONETIZATION
- [ ] Include actionable_steps extracted from content
- [ ] Append to ALPHA_STAGING.csv

### US-005: Update HIGH_SIGNAL_SOURCES.csv
**Description:** As a researcher, I need to add new accounts worth following.

**Acceptance Criteria:**
- [ ] Identify accounts with 3+ high-value bookmarks
- [ ] Check if account already in HIGH_SIGNAL_SOURCES.csv
- [ ] Add new accounts with SRC_ID, handle, focus area
- [ ] Update scan frequency based on posting velocity

### US-006: Update extraction log
**Description:** As a researcher, I need to log this run for future agents.

**Acceptance Criteria:**
- [ ] Update BOOKMARK_EXTRACTION_LOG.md with session details
- [ ] Note last status ID processed
- [ ] List new alpha entries added
- [ ] List new accounts discovered

## Technical Considerations

**Browser Automation:**
Chrome MCP can be unstable. Fallback options:
1. Manual extraction using console scripts from QUICK_START.md
2. Python + Playwright (requires logged-in session)

**Deduplication Check:**
```python
existing_urls = set(df['source_url'].dropna())
if post_url in existing_urls:
    skip_post()
```

**Content Filtering:**
Use keywords from deep_bookmark_scraper.js:
- INCLUDE: mrr, arr, revenue, shipped, launched, growth, seo, api, automation
- EXCLUDE: trump, biden, maga, woke, ratio, celebrity, sports

## Non-Goals

- No auto-posting or engagement (read-only)
- No scraping non-bookmarked content
- No bypassing rate limits aggressively

## Success Metrics

- 20+ new alpha entries per extraction run
- 5+ new HIGH_SIGNAL_SOURCES accounts per month
- Zero duplicate entries in ALPHA_STAGING
- PENDING_REVIEW entries contain actionable steps
- BOOKMARK_EXTRACTION_LOG allows seamless handoff between agents
