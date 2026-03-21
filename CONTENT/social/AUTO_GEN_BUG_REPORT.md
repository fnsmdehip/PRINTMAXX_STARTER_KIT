# Auto-Generated Tweet Bug Report
**Date:** 2026-03-21
**Script:** `AUTOMATIONS/tweet_auto_drafter.py`
**Severity:** HIGH -- producing garbage content that would flag accounts as bots

## Problem

The auto-drafter reads ALL alpha entries from ALPHA_STAGING.csv and templates them across ALL 5 accounts without niche filtering. This produces tweets like:

- `"faith without works... CHUCK NORRIS DIES AT 86. put the effort in."` (@selahmoments)
- `"grind doesn't care about your feelings. canadian Core Retail Sales MoM Actual 0.8%. just show up."` (@repscheme)
- `"the matrix has a backdoor. canadian Core Retail Sales MoM Actual 0.8%."` (@voidpilled)
- `"super Micro $SMCI stock is down by almost 30% so far today. the math works out to 30%/mo if you execute."` (@PRINTMAXXER)

Every single auto-generated tweet from the 013110 batch is incoherent bot-looking slop.

## Root Cause (line 120-220 of tweet_auto_drafter.py)

1. **No niche filtering.** All alpha entries go to all accounts. The `_default` template bucket on repscheme/drifthour/voidpilled/selahmoments catches EVERYTHING.
2. **Raw alpha text used as `{tactic_short}`.** Financial data headlines, celebrity death notices, and economic indicators are not tactics. The `extract_tactic_short()` function (line 261) just grabs raw text from `extracted_method`, `tactic`, or `reviewer_notes` fields without checking if it's actionable content.
3. **No coherence gate.** The template + tactic output is never checked for readability. "faith without works... CHUCK NORRIS DIES" passes because there's no validation.

## Fix Required

1. **Add niche-relevance filter** (before template selection):
   - @PRINTMAXXER: tech, tools, AI, automation, revenue, building, coding
   - @selahmoments: faith, prayer, spiritual, church, scripture, ramadan
   - @repscheme: fitness, exercise, discipline, health, training, body
   - @voidpilled: tech, information, systems, esoteric, contrarian, markets
   - @drifthour: aesthetic, process, building, late-night, curated

2. **Add tactic quality gate** (in extract_tactic_short):
   - Reject entries that are pure news headlines (no actionable method)
   - Reject financial data blurbs (match pattern: "Actual X% Forecast Y%")
   - Reject celebrity/death news
   - Require minimum actionability: must contain a verb and a method

3. **Add output coherence check**:
   - After template.format(), check that the tweet reads as a coherent sentence
   - Reject if tactic_short is >60% of tweet length (means template barely wraps it)

## Workaround (NOW)

Use the `_compound.csv` files instead of `_013110.csv` files. The compound content was hand-crafted from real compound analysis and is high quality.

**Files to use:**
- `tweets_printmaxxer_20260321_compound.csv` (10 tweets, HIGH quality)
- `tweets_selahmoments_20260321_compound.csv` (6 tweets, HIGH quality)
- `tweets_repscheme_20260321_compound.csv` (6 tweets, HIGH quality)
- `tweets_voidpilled_20260321_compound.csv` (7 tweets, HIGH quality)
- `tweets_drifthour_20260321_compound.csv` (6 tweets, HIGH quality)

**Files to REJECT:**
- All `tweets_*_20260321_013110.csv` files (garbage, do not post)
