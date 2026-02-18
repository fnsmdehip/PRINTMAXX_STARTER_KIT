# DEEP BOOKMARK ALPHA EXTRACTION PLAN

## Problem
Current scrape only got tweet text snippets. Real alpha is in:
1. Images/infographics (129 bookmarks)
2. Full threads (22 long threads need complete text)
3. External articles (links that need fetching)
4. "Show more" collapsed text

## Solution: 2-Phase Deep Scrape

### Phase 1: Re-scrape with Vision (HIGH PRIORITY)
Use Playwright + Claude/GPT-4V to:
1. Visit each bookmark URL individually
2. Take screenshot of full thread
3. Extract text from images/infographics
4. Get full "Show more" expanded text
5. Save to structured JSON with vision analysis

**Output:** `x_bookmarks_deep_2026-01-19.json` with:
- Full thread text (not truncated)
- Image OCR / infographic extraction
- External link content (if present)

### Phase 2: Pattern Mining (ALPHA EXTRACTION)
Analyze deep data for:
1. **Playbook patterns** (step-by-step guides in images)
2. **Revenue screenshots** (proof/metrics in images)
3. **Tool stacks** (tech mentioned in threads/images)
4. **Funnel breakdowns** (conversion paths in infographics)
5. **Copywriting angles** (winning hooks/formats to repurpose)

## Expected Alpha Gains
- 129 images → likely 20-40 have tactical infographics
- 22 long threads → likely 10-15 have complete playbooks
- Full text → catch "read more" alpha we missed

## Execution
1. Run deep scraper tonight (Brave still has session)
2. Feed results to Claude for pattern extraction
3. Update master doc with any new playbooks
4. Build swipe file for niche account content
