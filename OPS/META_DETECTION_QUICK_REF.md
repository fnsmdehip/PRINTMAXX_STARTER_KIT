# Meta Detection System - Quick Reference Card

**Script:** `AUTOMATIONS/niche_meta_detector.py`
**Docs:** `OPS/META_DETECTION_SYSTEM_GUIDE.md`

---

## Run Detection

```bash
python3 AUTOMATIONS/niche_meta_detector.py
```

---

## 6 Historical Patterns

| Pattern | Description | Coin | Product | Content |
|---------|-------------|------|---------|---------|
| **GHIBLI** | Character aesthetic → coin | 9 | 6 | 10 |
| **SARATOGA** | Quick pump meme | 10 | 2 | 7 |
| **ROUTINE** | Lifestyle → app | 3 | 10 | 9 |
| **MOLT** | AI agent → coin | 8 | 7 | 8 |
| **FITNESS** | Transformation → product | 2 | 10 | 10 |
| **SPIRITUAL** | Wellness → course | 3 | 9 | 9 |

---

## Quick Queries

**Top 10 opportunities:**
```bash
head -11 LEDGER/NICHE_META_OPPORTUNITIES.csv | column -t -s,
```

**Faith niche opportunities:**
```bash
grep "N001" LEDGER/NICHE_META_OPPORTUNITIES.csv
```

**High velocity meta (≥8):**
```bash
awk -F',' '$4 >= 8' LEDGER/META_TRACKER.csv
```

**App opportunities only:**
```bash
grep "APP" LEDGER/NICHE_META_OPPORTUNITIES.csv
```

**Content opportunities only:**
```bash
grep "CONTENT" LEDGER/NICHE_META_OPPORTUNITIES.csv
```

**Memecoin opportunities only:**
```bash
grep "MEMECOIN" LEDGER/NICHE_META_OPPORTUNITIES.csv
```

---

## Current Top 5 Opportunities

1. **Cozy AI Companions** (Tech) - Content - Priority 147 - MM006, CF013
2. **Sleep Soundscape Coins** (Sleep) - Content - Priority 131 - MM006, CF013
3. **Sleep Soundscape Coins** (Memes) - Content - Priority 131 - MM006, CF013
4. **Cozy AI Companions** (Tech) - Memecoin - Priority 117 - MM034
5. **GenZ Stock Memes** (GenZ Finance) - Content - Priority 108 - MM006, CF013

---

## Velocity Scale

| Score | Mentions/Hour | Alert Level |
|-------|---------------|-------------|
| 10 | ≥10 | EXPLOSIVE |
| 9 | ≥5 | VERY HIGH |
| 8 | ≥3 | HIGH |
| 7 | ≥2 | MEDIUM-HIGH |
| 6 | ≥1 | MEDIUM |
| 5 | ≥0.5 | MEDIUM-LOW |
| 4 | ≥0.25 | LOW-MEDIUM |
| 3 | <0.25 | LOW |

---

## Files

| File | Rows | Purpose |
|------|------|---------|
| `LEDGER/META_TRACKER.csv` | 8 | All detected meta |
| `LEDGER/NICHE_META_OPPORTUNITIES.csv` | 34 | Specific opportunities |
| `LEDGER/NEW_NICHES_DISCOVERED.csv` | 2 | Emerging niches |

---

## Pattern Distribution (Current)

- NOVEL_PATTERN: 3 trends (37.5%)
- GHIBLI_PATTERN: 2 trends (25%)
- ROUTINE_PATTERN: 2 trends (25%)
- MOLT_PATTERN: 1 trend (12.5%)

---

## Next Actions

1. Build content for Cozy AI Companions (Tech niche)
2. Build content for Sleep Soundscape Coins (Sleep + Memes niches)
3. Build content for GenZ Stock Memes (4 niches)
4. Consider memecoin launch for Cozy AI Companions (coin potential 9/10)
5. Run script daily to track velocity changes

---

## Niche IDs Quick Reference

| ID | Niche | ID | Niche | ID | Niche |
|----|-------|----|-------|----|-------|
| N001 | Faith | N012 | Gaming | N023 | Investing |
| N002 | Fitness | N013 | Crypto | N024 | Productivity |
| N003 | Tech | N014 | Stocks | N025 | Meditation |
| N004 | Pet | N015 | Motivation | N026 | Language |
| N005 | Senior | N016 | Music | N027 | Art |
| N006 | ADHD | N017 | Fashion | N028 | Photography |
| N007 | GenZ Finance | N018 | Food | N029 | Anime |
| N008 | Couples | N019 | Travel | N030 | Sports |
| N009 | Women Wellness | N020 | Parenting | N031 | Environment |
| N010 | Students | N021 | Mental Health | N032 | DIY |
| N011 | Sleep | N022 | Career | N033 | Memes |

---

## Method IDs Quick Reference

| ID | Method | ID | Method |
|----|--------|----|--------|
| MM001 | APP_FACTORY | MM006 | CONTENT_FARM |
| MM002 | INFO_PRODUCTS | MM025 | DIGITAL_PRODUCTS |
| MM034 | MEMECOIN_TRADING | MM046 | NOTION_TEMPLATES |
| CF013 | YOUTUBE_SHORTS | MM019 | PORTFOLIO_APP_BUILDER |

---

**Run detection daily. Prioritize by priority_score. Ship the highest opportunities first.**
