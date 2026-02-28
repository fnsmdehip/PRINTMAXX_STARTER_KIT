# Content Factory Playbook

**Script:** `AUTOMATIONS/content_factory.py`
**Purpose:** Unified pipeline: content in -> adapted for every platform -> scheduled -> tracked -> recycled

---

## Quick Start

```bash
# See what you have
python3 AUTOMATIONS/content_factory.py --status

# Full daily cycle (ingest + adapt + schedule + recycle)
python3 AUTOMATIONS/content_factory.py --daily --dry-run

# Run it for real
python3 AUTOMATIONS/content_factory.py --daily

# Export Buffer CSVs for upload
python3 AUTOMATIONS/content_factory.py --export-buffer

# Factory mode: 1 post -> 50+ variants
python3 AUTOMATIONS/content_factory.py --factory "cold emailed 200 dentists. 27% open rate. 4 calls booked."
```

---

## Daily Workflow (5 minutes)

1. **Morning (auto via cron or manual):**
   ```bash
   python3 AUTOMATIONS/content_factory.py --daily
   ```
   This runs the full pipeline:
   - Scans `CONTENT/social/` for new .md and .csv files
   - Deduplicates against already-posted content
   - Adapts each piece for Twitter, LinkedIn, TikTok, Instagram, Reddit, YouTube
   - Schedules with optimal timing per platform (with natural jitter)
   - Checks for winners older than 30 days to recycle

2. **Export for scheduling:**
   ```bash
   python3 AUTOMATIONS/content_factory.py --export-buffer
   ```
   Generates one CSV per account+platform in `AUTOMATIONS/content_posting/buffer_exports/`. Upload to Buffer or Publer.

3. **After posting (tracked by auto_content_poster.py):**
   - Performance data flows into `LEDGER/CONTENT_PERFORMANCE.csv`
   - Winners flagged in `LEDGER/CONTENT_WINNERS.csv`
   - Factory automatically recycles winners after 30 days

---

## Content Adaptation Rules

### Twitter (X)
- **Limit:** 280 chars
- **Hashtags:** 0-2 max (hashtags hurt reach on X)
- **Tone:** lowercase, casual, consequence-first hooks
- **Avoid:** link previews in promotional posts (kills reach)
- **Best for:** hot takes, specific numbers, reply bait

### LinkedIn
- **Limit:** 3,000 chars
- **Hashtags:** 0-3 at bottom
- **Tone:** professional but direct. Capitalize sentences. Line breaks between paragraphs
- **Skip:** weekends (no Saturday/Sunday posts)
- **Best for:** case studies, process breakdowns, B2B insights

### TikTok
- **Limit:** 2,200 chars (caption)
- **Hashtags:** 3-7, always include #fyp
- **Tone:** short caption, casual, text as video script outline
- **Best for:** before/after, quick tips, controversial takes

### Instagram
- **Limit:** 2,200 chars
- **Hashtags:** 5-15 in block at bottom
- **Tone:** longer captions OK, line breaks for readability
- **Best for:** carousels, infographics, visual content

### Reddit
- **Limit:** 40,000 chars
- **Hashtags:** ZERO (instant credibility kill)
- **Tone:** conversational, no promotional CTAs, provide genuine value
- **Remove:** "link in bio", "reply X for", "DM me for" (Reddit hates self-promotion)
- **Best for:** detailed breakdowns, honest results, community value

### YouTube
- **Limit:** 5,000 chars (description)
- **Hashtags:** 3-8 in description
- **Tone:** description format, can include timestamps and links
- **Best for:** tutorials, deep dives, ambient/chill content

### Substack
- **Limit:** 100,000 chars
- **Hashtags:** ZERO
- **Tone:** newsletter format, expand into full paragraphs
- **Frequency:** 1 post/day max
- **Best for:** deep analysis, weekly roundups, exclusive content

---

## Best Posting Times (UTC)

Based on audience analysis across niches. All times include +/- 15 min jitter to avoid looking automated.

| Platform  | Slot 1 | Slot 2 | Slot 3 | Slot 4 |
|-----------|--------|--------|--------|--------|
| Twitter   | 13:00  | 17:00  | 22:00  | 01:00  |
| LinkedIn  | 12:00  | 16:00  | 21:00  | -      |
| TikTok    | 11:00  | 17:00  | 02:00  | -      |
| Instagram | 14:00  | 19:00  | 00:00  | -      |
| Reddit    | 13:00  | 18:00  | 23:00  | -      |
| YouTube   | 15:00  | 20:00  | -      | -      |

**EST equivalents:** Subtract 5 hours. Twitter Slot 1 = 8 AM EST.

**Niche-specific adjustments (from auto_content_poster.py):**
- Faith (@selahmoments): early morning (5:30 AM) + evening (8 PM)
- Fitness (@repscheme): pre-gym (7 AM) + post-work (6:30 PM)
- Esoteric (@voidpilled): late night (10 PM + 2 AM)
- Ambient (@drifthour): night (11 PM + 6 AM)

---

## Factory Mode

Transform a single post into 50+ platform-ready variants:

```bash
python3 AUTOMATIONS/content_factory.py --factory "text here" --niche tech
```

**What it generates:**
1. **Platform adaptations (6):** One per platform (Twitter, LinkedIn, TikTok, IG, Reddit, YouTube)
2. **Hook variations (24):** 8 different opening hooks x 3 platforms each
3. **Question formats (8):** 4 engagement questions x 2 platforms
4. **Thread openers (1):** Twitter thread starter
5. **Cross-niche adaptations (12+):** Same content reframed for faith, fitness, tech, memes

**Total: 50+ variants from 1 input.**

Use after every build session, every alpha discovery, every win. One piece of content should touch 4+ channels minimum.

---

## Recycling Rules

Posts that performed well get re-queued after 30 days with subtle modifications.

**Eligible for recycling:**
- Winner score >= 50 (from CONTENT_PERFORMANCE.csv)
- Posted 30+ days ago
- Not already recycled in last 30 days

**Modifications applied:**
- Hook swap ("i " -> "update: ", "still works: ", etc.)
- Suffix additions ("still works.", "nothing has changed.")
- Phrasing swaps to avoid exact duplicate detection

**Why this works:**
- Twitter shows posts to ~5% of followers. Recycling reaches the other 95%.
- LinkedIn algorithm resets after 30 days.
- Top performers are proven. Re-posting them has higher expected value than new untested content.

---

## Cross-Promotion Strategy

### Account Network (13 accounts)

```
@PRINTMAXXER (hub)
  |
  +-- @toolstwts (tools)
  +-- @growthpilled (growth)
  +-- @outboundtwts (outreach)
  +-- @shiplog (building)
  |
  +-- @selahmoments (faith)
  +-- @repscheme (fitness)
  +-- @voidpilled (esoteric)
  |
  +-- @clipvault_ (clips)
  +-- @silentframes (aesthetic)
  +-- @velvetframes (beauty)
  +-- @drifthour (ambient)
```

### Cross-Promo Rules

1. **Tech cluster** (@PRINTMAXXER, @toolstwts, @growthpilled, @outboundtwts, @shiplog):
   - Share each other's best threads with added context
   - Quote tweet with "related:" or "this is what I use too:"
   - Max 1 cross-promo per account per day

2. **Lifestyle cluster** (@selahmoments, @repscheme, @voidpilled):
   - Occasional cross-references when content overlaps (discipline, habits, mindset)
   - Never forced. Only when genuine connection exists.

3. **Visual cluster** (@clipvault_, @silentframes, @velvetframes, @drifthour):
   - Can share aesthetic content across accounts
   - Different angles: clips vs photos vs curated vs ambient

4. **Hub promotion:** @PRINTMAXXER can reference any account naturally
   - "built a prayer tracking app" -> mention @selahmoments
   - "automated my content posting" -> mention @toolstwts

5. **Never:** Obvious shill behavior. No "check out my other account". Always provide standalone value.

---

## Content Sources (Auto-Scanned)

The factory scans these directories automatically:

| Directory | Niche | File Types |
|-----------|-------|------------|
| `CONTENT/social/printmaxxer/` | tech | .md |
| `CONTENT/social/ai/` | tech | .md |
| `CONTENT/social/growthpilled/` | tech | .md |
| `CONTENT/social/outboundtwts/` | tech | .md |
| `CONTENT/social/toolstwts/` | tech | .md |
| `CONTENT/social/shiplog/` | tech | .md |
| `CONTENT/social/faith/` | faith | .md |
| `CONTENT/social/selahmoments/` | faith | .md |
| `CONTENT/social/ramadan/` | faith | .md |
| `CONTENT/social/fitness/` | fitness | .md |
| `CONTENT/social/repscheme/` | fitness | .md |
| `CONTENT/social/memes/` | memes | .md |
| `CONTENT/social/clipvault/` | memes | .md |
| `CONTENT/social/esoteric/` | esoteric | .md |
| `CONTENT/social/aesthetic/` | aesthetic | .md |
| `CONTENT/social/beauty_curated/` | beauty | .md |
| `CONTENT/social/drifthour/` | ambient | .md |
| `AUTOMATIONS/content_posting/` | mixed | .csv |

---

## Queue States

```
  [new content file] -> INGEST -> "queued"
                                      |
                              ADAPT -> "adapted" (platform-specific versions)
                                      |
                            SCHEDULE -> "scheduled" (date + time assigned)
                                      |
                         EXPORT/POST -> "posted"
                                      |
                      TRACK (30 days) -> "recyclable" (if winner_score >= 50)
                                      |
                             RECYCLE -> "queued" (modified, re-enters pipeline)
```

---

## Cron Integration

Add to crontab for fully automated content pipeline:

```bash
# 4:00 AM - Daily content factory cycle
0 4 * * * cd /Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt && python3 AUTOMATIONS/content_factory.py --daily >> AUTOMATIONS/logs/content_factory.log 2>&1

# 4:30 AM - Export Buffer CSVs
30 4 * * * cd /Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt && python3 AUTOMATIONS/content_factory.py --export-buffer >> AUTOMATIONS/logs/content_factory.log 2>&1

# Weekly - Recycle winners (Sunday midnight)
0 0 * * 0 cd /Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt && python3 AUTOMATIONS/content_factory.py --recycle-winners >> AUTOMATIONS/logs/content_factory.log 2>&1
```

---

## Integration Points

| System | How It Connects |
|--------|----------------|
| `auto_content_poster.py` | Posts content from queue, tracks performance |
| `LEDGER/CONTENT_PERFORMANCE.csv` | Performance data feeds recycling decisions |
| `LEDGER/CONTENT_WINNERS.csv` | Winners get recycled after 30 days |
| `LEDGER/CONTENT_POSTED.csv` | Dedup: never post same content twice |
| `LEDGER/CONTENT_CALENDAR_30DAY.csv` | Existing 1,008 posts (compatible format) |
| Buffer/Publer | Import exported CSVs for scheduled posting |
| `compliance_scanner.py` | Scan adapted content before posting |

---

## Metrics

Track these after deploying the factory:

| Metric | Target | How to Check |
|--------|--------|-------------|
| Content pieces ingested/day | 10+ | `--status` queue count |
| Platform variants created | 50+ per source | `--factory` output count |
| Posts scheduled/day | 3-4 per account | Buffer calendar view |
| Recycle rate | 10-20% of queue | `--status` recycling count |
| Duplicate detection | 0 duplicates posted | `CONTENT_POSTED.csv` hash check |
| Buffer CSV accuracy | 100% importable | Manual spot check after export |

---

## Troubleshooting

**"Found 0 new content pieces"**
- All existing content already in queue or posted. Create new content in `CONTENT/social/` directories.
- Check `LEDGER/CONTENT_FACTORY_QUEUE.csv` for existing entries.

**"No scheduled content to export"**
- Run `--daily` first to populate the schedule, then `--export-buffer`.

**Duplicate content across accounts**
- Normal. The factory creates per-account adaptations. Each is platform-specific.
- True duplicates (same hash) are automatically skipped.

**Buffer import rejects CSV**
- Ensure date format is YYYY-MM-DD and time is HH:MM.
- Check for unescaped quotes in post text.
- Try importing one file at a time.
