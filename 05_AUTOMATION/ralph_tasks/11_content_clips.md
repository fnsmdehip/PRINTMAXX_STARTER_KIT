---
task_id: CONTENT-005
test_command: "python3 -c \"import os; files = os.listdir('CONTENT/social/clips/'); assert len(files) >= 20, f'Only {len(files)} files'\""
max_iterations: 15
completion_signal: "CLIPS_BATCH_COMPLETE"
---

# Task: Generate clip channel content templates

## Context
- Read .claude/rules/copy-style.md for voice
- Read .ralph/guardrails.md for constraints
- Check LEDGER/CROSS_POLLINATION_MATRIX.csv - synergizes with MM010 (streamer clips), CF004 (memes)
- Output to CONTENT/social/clips/
- Create directory: `mkdir -p CONTENT/social/clips/`

## Content Types

### 1. Caption Templates (10 pieces)
Reusable captions for streamer clip accounts:

**Hook Patterns:**
- "[Streamer] just did WHAT?!"
- "This [game] moment is INSANE"
- "Nobody expected this from [streamer]"
- "The chat went CRAZY when this happened"
- "[Streamer] actually broke"

**Engagement Patterns:**
- "Would you have done the same thing?"
- "Rate this play 1-10"
- "Who's the better [game] player? [A] or [B]"

### 2. Bio Templates (3 pieces)
For different clip channel personas:
- Gaming clips general
- Specific game focus (Valorant, Fortnite, etc.)
- Streamer highlights

### 3. Trending Sound Pairings (7 pieces)
Match clip types with trending TikTok sounds:
- Skill clips → hype music
- Fail clips → comedic sounds
- Rage clips → dramatic sounds
- Wholesome clips → soft sounds

## File Format

### Caption Templates
```markdown
---
type: caption_template
niche: clips
platform: x | tiktok | youtube_shorts
clip_type: skill | fail | rage | wholesome | drama | funny
synergy_methods: [MM010, CF006, CF004]
generated_date: 2026-01-22
---

**Template:** [caption with [PLACEHOLDER] markers]

**Use When:** [description of when to use this template]

**Example Filled:** [example with real values]

**Hashtags:** [relevant hashtags]
```

### Bio Templates
```markdown
---
type: bio_template
niche: clips
platform: x | tiktok
focus: general | game_specific | streamer_focused
generated_date: 2026-01-22
char_count: [number]
---

**Bio:**
[bio text]

**Link Placeholder:** [what to link - discord, youtube, etc.]
```

### Sound Pairings
```markdown
---
type: sound_pairing
niche: clips
platform: tiktok | reels
clip_type: skill | fail | rage | wholesome | drama | funny
generated_date: 2026-01-22
---

**Clip Type:** [type]

**Sound Category:** [music style]

**Example Sounds:**
- [sound name 1]
- [sound name 2]
- [sound name 3]

**Timing Tips:** [when to cut, beat drops, etc.]

**Why It Works:** [psychology behind pairing]
```

## Clip Categories
- **Skill clips:** Insane plays, clutches, world records
- **Fail clips:** Funny deaths, mistakes, bugs
- **Rage clips:** Streamer reactions, keyboard smashes
- **Wholesome clips:** Donations, fan interactions
- **Drama clips:** Arguments, hot takes, controversies
- **Funny clips:** Comedy moments, jokes, impressions

## Cross-Pollination
- Tag streamers for exposure → they RT/duet
- Cross-post to meme accounts (CF004)
- Build following → sell shoutouts to smaller streamers

## Success Criteria
1. [ ] 10 caption templates covering all clip types
2. [ ] 3 bio templates for different personas
3. [ ] 7 sound pairing guides
4. [ ] Templates are actually reusable (placeholders work)
5. [ ] No em dashes or banned vocabulary
6. [ ] Hashtag suggestions included

## When complete
After all 20 files created:
Output: <promise>CLIPS_BATCH_COMPLETE</promise>
