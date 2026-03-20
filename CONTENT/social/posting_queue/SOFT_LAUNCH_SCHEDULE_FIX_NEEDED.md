# SOFT_LAUNCH SCHEDULE CONFLICT, Needs Fix Before Mar 17

**Issue:** Mar 17-26 has 4 slots/day scheduled (0730, 1100, 1430, 1800) but SOFT_LAUNCH phase only allows 1-2 posts/day max.

**Current state:** 40 tweets scheduled across Mar 17-26 (4/day x 10 days). Need to reduce to 20 max (2/day x 10 days).

**Recommended fix:**
1. **KEEP:** 0730 and 1800 slots (morning + evening = 2/day, well spaced)
2. **HOLD:** 1100 and 1430 slots, move to FULL_GROWTH (Mar 27+) or create new Apr 16+ dates
3. This frees 20 high-quality tweets for later without losing them

**Why this matters:** Posting 4x/day during warmup risks getting flagged as automation by Twitter's algorithm. The whole point of the 21-day warmup is to build trust signals gradually.

**Action needed:** Next social_poster cycle should:
1. Rename Mar 17-26 _1100 and _1430 files with HOLD_ prefix
2. Reschedule them for Apr 16+ or later FULL_GROWTH slots
3. Update post_schedule.json and post_log.json

**Priority:** P1, must be done before Mar 17 (9 days away)

---
CREATED: 2026-03-08T15:56:00
SOURCE: social_poster quality gate cycle
STATUS: OPEN
