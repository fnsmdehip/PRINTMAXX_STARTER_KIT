# RBI System Improvement Plan — Next 10 Upgrades

**RBI = Revenue-Based Intelligence**
**Current state:** Daily research pipeline with scrapers + alpha processor + staging/review flow
**Goal:** Double signal quality, halve processing time, automate 80% of human review decisions

---

## Current System Map

```
Twitter scraper → ALPHA_STAGING.csv → alpha_auto_processor.py → APPROVED/REJECTED/BAIT
Reddit scraper  →                   → manual review trigger    → ventures/OPS/content
Daily research pipeline             → BRAIN_LOG.jsonl          → BRAIN_STATE.json
```

**Bottlenecks identified:**
1. Manual review is 60% of time cost
2. Duplicate alpha across runs not caught
3. No scoring for "how new is this tactic"
4. No source credibility weighting
5. No feedback loop from outcomes to future scoring

---

## Upgrade 1: Automated Duplicate Detection

**Problem:** Same tactic appears multiple times across different scrape runs. Review wastes time on already-known intel.
**Fix:** Semantic similarity check before staging.

```python
# Add to alpha_auto_processor.py
from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer('all-MiniLM-L6-v2')

def is_duplicate(new_entry, existing_entries, threshold=0.85):
    new_embedding = model.encode(new_entry['summary'])
    for entry in existing_entries:
        existing_embedding = model.encode(entry['summary'])
        similarity = util.cos_sim(new_embedding, existing_embedding)
        if similarity > threshold:
            return True, entry['alpha_id']
    return False, None
```

**Time saved:** 20-30% of manual review volume
**Build time:** 2 hours
**Dependencies:** `pip install sentence-transformers`

---

## Upgrade 2: Source Credibility Scoring

**Problem:** Alpha from a 12-follower account is treated the same as alpha from @levelsio.
**Fix:** Weight scores by source metrics at time of scraping.

```python
SOURCE_WEIGHTS = {
    'verified': 1.5,
    'followers_100k_plus': 1.4,
    'followers_10k_100k': 1.2,
    'followers_1k_10k': 1.0,
    'followers_under_1k': 0.7,
    'engagement_rate_high': 1.3,  # >5% engagement
    'engagement_rate_low': 0.8,   # <1% engagement
    'known_alpha_source': 1.6,    # manually curated list
}

TRUSTED_ACCOUNTS = [
    'pipelineabuser', 'levelsio', 'tdinh_me', 'marc_louvion',
    'dannypostmaa', 'codyschneiderxx', '0xzak', 'eptwts',
    'tom777kruise', 'piratewires', 'seanb2b'
]
```

**Output:** Each alpha entry gets `source_credibility_score: 0.7-1.6`
**Downstream effect:** Auto-approve anything >1.3 with specific numbers; auto-reject anything <0.8 without numbers

---

## Upgrade 3: Novelty Score

**Problem:** Tactics become stale. Cold email advice from 2023 is not alpha.
**Fix:** Score each entry against how recently similar tactics were approved.

```python
def calculate_novelty(entry, ledger_history, days_window=90):
    """
    Returns 0-1 novelty score.
    1.0 = completely new tactic
    0.0 = exact tactic seen multiple times in last 90 days
    """
    recent = [e for e in ledger_history if e['days_ago'] <= days_window]
    matches = semantic_search(entry['summary'], recent, top_k=5)
    if not matches:
        return 1.0
    avg_similarity = sum(m['score'] for m in matches) / len(matches)
    return round(1.0 - avg_similarity, 2)
```

**Threshold rules:**
- Novelty > 0.7: auto-stage as PENDING_REVIEW
- Novelty 0.4-0.7: flag as "RELATED_TO: [alpha_id]" for quick comparison
- Novelty < 0.4: auto-categorize as DUPLICATE

---

## Upgrade 4: Auto-Approve Fast Path

**Problem:** High-confidence alpha still sits in PENDING_REVIEW for hours.
**Fix:** Define auto-approve criteria so obvious wins flow straight to integration.

**Auto-approve when ALL are true:**
- source_credibility_score > 1.3
- novelty_score > 0.6
- Contains at least 2 of: [specific dollar amount, specific time period, specific tool name, specific percentage]
- engagement_authenticity: AUTHENTIC (not SUSPICIOUS)
- Category is in: [OUTBOUND, CONTENT_FORMAT, TOOL_ALPHA, MONETIZATION]

```python
def should_auto_approve(entry):
    specificity_count = count_specifics(entry['summary'])
    return (
        entry['source_credibility'] > 1.3 and
        entry['novelty_score'] > 0.6 and
        specificity_count >= 2 and
        entry['engagement_authenticity'] != 'SUSPICIOUS' and
        entry['category'] in AUTO_APPROVE_CATEGORIES
    )
```

**Expected auto-approve rate:** 15-25% of incoming alpha
**Human review reduction:** 20% less queue per run

---

## Upgrade 5: Outcome Feedback Loop

**Problem:** We never close the loop. Did APPROVED alpha actually produce results?
**Fix:** Track which alpha we acted on and what happened.

New CSV: `LEDGER/ALPHA_OUTCOMES.csv`

```
alpha_id, approved_date, action_taken, action_date, outcome, revenue_attributed, notes
ALPHA185, 2026-01-15, "set up ralph loops", 2026-01-16, "POSITIVE - 5 tasks completed", 0, ""
ALPHA201, 2026-01-20, "cold email sequence", 2026-01-21, "NEUTRAL - 2% reply rate", 180, "below benchmark"
```

**Monthly review process:**
- Pull all APPROVED alpha from last 90 days
- For each: was action taken? If yes, what was the outcome?
- Calculate: approval-to-action rate, action-to-positive-outcome rate
- Use to calibrate auto-approve thresholds quarterly

**Target metrics:**
- Approval-to-action rate: >60% (currently estimated ~30%)
- Action-to-positive-outcome: >40%

---

## Upgrade 6: Category-Specific Routing Automation

**Problem:** APPROVED entries still require manual routing to the right master file.
**Fix:** Auto-route based on category + keywords.

```python
ROUTING_MAP = {
    'OUTBOUND': 'LEDGER/MARKETING_CHANNELS_MASTER.csv',
    'CONTENT_FORMAT': 'LEDGER/WINNING_CONTENT_STRUCTURES.csv',
    'TOOL_ALPHA': 'OPS/TOOL_STACK.md',
    'MONETIZATION': 'OPS/MONETIZATION_PLAYBOOKS.md',
    'SEO_GEO_ASO': 'OPS/GTM_OPTIMIZATION_CHECKLIST.md',
    'APP_FACTORY': 'LEDGER/APP_FACTORY_METHODS.csv',
    'GROWTH_HACK': 'LEDGER/MARKETING_CHANNELS_MASTER.csv',
    'ENGAGEMENT_BAIT': 'OPS/NICHE_POSTING_STRATEGY.md',
}

def auto_route(entry):
    target_file = ROUTING_MAP.get(entry['category'])
    if target_file:
        append_to_file(entry, target_file)
        entry['routing_status'] = 'AUTO_ROUTED'
        entry['routed_to'] = target_file
    return entry
```

**Time saved:** 5-10 minutes per review session

---

## Upgrade 7: Engagement Authenticity Auto-Check

**Problem:** Bot detection is currently manual.
**Fix:** Automated heuristics at scrape time.

```python
def check_engagement_authenticity(post_data):
    likes = post_data.get('likes', 0)
    comments = post_data.get('comments', 0)
    followers = post_data.get('author_followers', 0)
    account_age_days = post_data.get('account_age_days', 365)

    flags = []

    # Engagement ratio check
    if likes > 0 and comments > 0:
        ratio = likes / comments
        if ratio > 200:  # 200+ likes per comment = suspicious
            flags.append('LOW_COMMENT_RATIO')

    # Follower/like ratio
    if followers > 0 and likes > 0:
        if likes > followers * 3:  # getting 3x their followers in likes = suspicious
            flags.append('LIKES_EXCEED_FOLLOWERS')

    # New account with large following
    if account_age_days < 90 and followers > 10000:
        flags.append('NEW_LARGE_ACCOUNT')

    if len(flags) == 0:
        return 'AUTHENTIC'
    elif len(flags) == 1:
        return 'SUSPICIOUS'
    else:
        return 'LIKELY_BOTTED'
```

---

## Upgrade 8: Weekly Digest Auto-Generation

**Problem:** Alpha sits in CSVs and doesn't get actioned.
**Fix:** Auto-generate Monday morning digest from last 7 days of approved alpha.

```python
# Run via cron: every Monday 8 AM
# python3 AUTOMATIONS/alpha_weekly_digest.py

def generate_weekly_digest():
    approved = load_recent_approved(days=7)
    by_category = group_by_category(approved)

    digest = f"""
# Alpha Digest — Week of {monday_date}

## Top Picks This Week
{format_top_picks(approved[:5])}

## By Category
{format_by_category(by_category)}

## Actions to Take This Week
{generate_action_items(approved)}
    """

    save_to_file(digest, f'LEDGER/DIGESTS/digest_{monday_date}.md')
    print(f"Digest saved. {len(approved)} entries reviewed.")
```

**Cron entry:** `0 8 * * 1 python3 /path/to/alpha_weekly_digest.py`

---

## Upgrade 9: Trend Velocity Tracking

**Problem:** We miss when a tactic is going viral in real-time — we only see it after it's mainstream.
**Fix:** Track mention frequency per tactic over rolling 7-day windows.

New field on ALPHA_STAGING: `trend_velocity: RISING|STABLE|DECLINING|EMERGING`

```python
VELOCITY_RULES = {
    'EMERGING': 'first sighting in 30 days, <3 mentions total',
    'RISING': 'mentioned 3-10x in last 7 days, up from <3 previous 7 days',
    'STABLE': 'consistent 3-10 mentions per week for 4+ weeks',
    'DECLINING': 'was RISING/STABLE, now <3 mentions in last 7 days',
}
```

**Priority:** EMERGING and RISING entries get bumped to top of review queue.

---

## Upgrade 10: Cross-Pollination Auto-Tagger

**Problem:** A tactic discovered for solopreneur niche often applies to faith, fitness, ecom — but we don't make that connection.
**Fix:** Auto-suggest cross-niche applications at staging time.

```python
NICHE_KEYWORDS = {
    'solopreneur': ['saas', 'cold email', 'indiehacker', 'b2b', 'automation'],
    'faith': ['prayer', 'ramadan', 'bible', 'church', 'devotional', 'christian'],
    'fitness': ['workout', 'supplement', 'training', 'macro', 'gym'],
    'ecom': ['dropship', 'tiktok shop', 'print on demand', 'amazon', 'etsy'],
}

def suggest_cross_pollination(entry):
    detected_niches = []
    for niche, keywords in NICHE_KEYWORDS.items():
        if any(kw in entry['summary'].lower() for kw in keywords):
            detected_niches.append(niche)

    all_niches = list(NICHE_KEYWORDS.keys())
    cross_niches = [n for n in all_niches if n not in detected_niches]

    return {
        'primary_niche': detected_niches,
        'cross_pollination_opportunities': cross_niches,
        'cross_pollination_note': f"Adapt for: {', '.join(cross_niches)}"
    }
```

---

## Implementation Priority

| Upgrade | Build Time | Impact | Priority |
|---------|-----------|--------|----------|
| 4. Auto-Approve Fast Path | 1 hour | High | P1 |
| 1. Duplicate Detection | 2 hours | High | P1 |
| 6. Auto-Route | 1 hour | High | P1 |
| 7. Bot Detection | 2 hours | Medium | P2 |
| 8. Weekly Digest | 2 hours | Medium | P2 |
| 2. Source Credibility | 3 hours | High | P2 |
| 3. Novelty Score | 3 hours | Medium | P3 |
| 9. Trend Velocity | 3 hours | Medium | P3 |
| 5. Outcome Feedback | 4 hours | High | P3 |
| 10. Cross-Pollination | 2 hours | Medium | P3 |

**30-day target:** P1 + P2 upgrades live. 50% reduction in manual review time.
**90-day target:** Full system. 80% of low-risk alpha auto-processed end-to-end.
