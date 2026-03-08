# Generator Fix Report - 2026-03-08

## Problem

Two generators in `AUTOMATIONS/decision_engine.py` have been producing low-quality skeleton output for 5+ quality gate cycles:

1. **EcomArbPipeline._generate_listings** (was line 226-270): Output skeleton template with "Brand new, ships fast. Message me for bulk pricing." for ALL products. No real descriptions, no features, no product-specific copy. Title was just raw product name (e.g., "yoga mat"). Category was "[Auto-detect]".

2. **FreelancePipeline._generate_responses** (was line 140-186): Output unfilled `[placeholder]` brackets like `[Specific deliverable matching their ask]`, `[realistic estimate]`, `[link]`. Contained chatbot artifact "Happy to discuss scope and timeline." No service matching. Ignored CSV fields like `matched_services`, `budget`, `body_preview`.

Secondary issue: `AUTOMATIONS/auto_freelance_responder.py` line 209 contained chatbot artifact "happy to answer any questions about the process." and line 200/202 "happy to discuss pricing."

## Root Cause

Both generators used hardcoded f-string templates with zero product/service intelligence. The `EcomArbPipeline` had no product knowledge database despite `arb_listing_generator.py` having a `PRODUCT_DB` with real data. The `FreelancePipeline` had no service matching logic despite `auto_freelance_responder.py` having a complete `VIBE_CODE_SERVICES` dictionary and `match_services()` function.

The `analyze()` method for ecom also dropped the `category` field from the CSV, preventing even basic category-aware fallback copy.

## Fixes Applied

### 1. EcomArbPipeline (decision_engine.py)

- Added `PRODUCT_DB` with 17 products: led face mask, yoga mat, posture corrector, gua sha tool, scalp massager, wireless earbuds, cat water fountain, jump rope weighted, lash serum, phone projector, shower head filter, resistance bands set, ring light, pull up bar, cable organizer, ice roller face, neck stretcher, dermaplaning tool
- Each product has: category, fb_title, ebay_title, features list, fb_description (80-300 chars), ebay_description (60-250 chars)
- All copy follows copy-style.md: consequence-first hooks, specific numbers, no AI vocabulary, no em dashes
- Added `CATEGORY_COPY_HINTS` for fallback copy when product isn't in DB (7 categories: beauty, health, fitness, tech, pet, home, kitchen)
- Added `_get_product_data()` method that checks DB first, falls back to category-aware generation
- Fallback products get `_is_fallback: True` flag and `PENDING_REVIEW` status (vs `READY_TO_LIST` for DB products)
- Added quality self-check that rejects output containing skeleton markers ("Brand new, ships fast", "[Auto-detect]", etc.) or descriptions under 80 chars (FB) / 60 chars (eBay)
- Fixed `analyze()` to pass `category` field through from CSV

### 2. FreelancePipeline (decision_engine.py)

- Added `SERVICES` dictionary with 8 service types: website, automation, data_entry, logo, social_media, scraper, video_editing, cold_email
- Each service has: name, delivery time, price_floor, pitch line, portfolio links
- Added `_match_service()` method: checks `matched_services` CSV field first, then keyword matching against title + body_preview
- Added `_build_price_line()` method: undercuts stated budget by 15%, or shows price floor if no budget
- Fixed `analyze()` to extract and pass through: budget, matched_services, delivery_time, body_preview from CSV
- Response is now copy-paste ready with real pitch, real pricing, real portfolio links
- No brackets, no placeholders, no "Happy to help" or "I specialize in exactly"
- Added quality self-check that rejects responses containing `[placeholder]` brackets or chatbot artifacts
- Added follow-up DM template with service-specific delivery time

### 3. auto_freelance_responder.py

- Removed chatbot artifact "happy to answer any questions about the process." (line 209)
- Changed "happy to discuss pricing" to "pricing depends on scope" (lines 200, 202)

## Files Modified

- `AUTOMATIONS/decision_engine.py` - EcomArbPipeline and FreelancePipeline rewritten
- `AUTOMATIONS/auto_freelance_responder.py` - chatbot artifacts removed

## Verification

All changes compile successfully. Unit tests verify:
- Known products get real titles and descriptions (yoga mat: 284 char description)
- Unknown products get category-aware fallback copy, flagged as fallback
- No skeleton markers survive the quality self-check
- Service matching correctly maps "logo design" posts to logo service, "web scraper" posts to scraper service
- Generated responses contain zero `[placeholder]` brackets and zero chatbot artifacts
- Price lines correctly compute 85% of stated budget or show price floor

## Impact

- Ecom listings now have real product copy that could be posted to FB Marketplace / eBay without human rewriting
- Freelance responses are copy-paste ready with service-matched pitches and pricing
- Quality self-checks prevent regression to skeleton output
- Quality gate no longer needs to spend cycles rewriting every single output
