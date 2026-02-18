---
task_id: CONTENT-004
test_command: "python3 -c \"import os; files = os.listdir('CONTENT/social/relax/'); assert len(files) >= 30, f'Only {len(files)} files'\""
max_iterations: 15
completion_signal: "RELAX_BATCH_COMPLETE"
---

# Task: Generate relax/sleep content for YouTube + socials

## Context
- Read .claude/rules/copy-style.md for voice
- Read .ralph/guardrails.md for constraints
- Check LEDGER/CROSS_POLLINATION_MATRIX.csv - synergizes with CF002 (sleep), AI004 (ASMR)
- Output to CONTENT/social/relax/
- Create directory: `mkdir -p CONTENT/social/relax/`

## Content Types to Create

### 1. Video Titles + Descriptions (15 pieces)
For YouTube ambient/relax videos:
- Title (50-70 chars, keyword-rich)
- Description (150-200 chars)
- Tags (comma-separated)
- Thumbnail text suggestion

**Title Patterns:**
- "[Time] Hours of [Sound] for [Purpose] | [Qualifier]"
- "[Adjective] [Sound] | Perfect for [Activity]"
- "Fall Asleep in [Time] | [Sound Type] for Deep Sleep"

**Examples:**
- "10 Hours of Gentle Rain for Deep Sleep | No Thunder"
- "Cozy Fireplace Crackling | Perfect for Winter Nights"
- "Forest Stream Sounds | Natural White Noise for Focus"

### 2. Community Posts (10 pieces)
Short posts for YouTube community tab + X:
- Sleep tips
- Relaxation quotes
- Poll questions about sleep habits
- "New video dropping" teasers

### 3. Shorts Scripts (5 pieces)
60-second scripts for sleep/relax Shorts:
- "3 sounds that help you sleep instantly"
- "Why [sound] is the best for relaxation"
- "Sleep hack most people don't know"

## File Format

### Video Metadata Files
```markdown
---
type: video_metadata
niche: relax
sub_niche: rain | fireplace | nature | white_noise | ambient
platform: youtube
synergy_methods: [CF001, CF002, AI004]
generated_date: 2026-01-22
---

**Title:** [title here]

**Description:**
[description]

**Tags:** [comma-separated tags]

**Thumbnail Text:** [text overlay for thumbnail]

**Sound Type:** [rain, fire, forest, ocean, etc.]

**Duration Suggestion:** [4h, 8h, 10h, 12h]

**Monetization Angle:** [affiliate link opportunity]
```

### Community/Social Posts
```markdown
---
type: community_post
niche: relax
platform: youtube | x
post_type: tip | quote | poll | teaser
synergy_methods: [CF001, CF002]
generated_date: 2026-01-22
char_count: [number]
---

[Post content]
```

### Shorts Scripts
```markdown
---
type: shorts_script
niche: relax
platform: youtube_shorts | tiktok | reels
duration: 60
synergy_methods: [CF001, CF002, AI004]
generated_date: 2026-01-22
---

**Hook (0-3s):** [attention grabber]

**Body (3-50s):**
[script content]

**CTA (50-60s):** [subscribe, comment, etc.]
```

## Sound Categories to Cover
- Rain (gentle, heavy, on roof, on window)
- Fireplace (crackling, with rain, with wind)
- Nature (forest, stream, birds, ocean)
- White noise (fan, static, brown noise)
- Ambient (cafe, train, thunderstorm)

## Cross-Pollination Hooks
- "For the best sleep tracking, I use [sleep app]" (CF002)
- "Pair this with ASMR for ultimate relaxation" (AI004)
- "My favorite sleep supplement: [affiliate]"

## Success Criteria
1. [ ] 15 video metadata files
2. [ ] 10 community/social posts
3. [ ] 5 shorts scripts
4. [ ] Each covers different sound type
5. [ ] No em dashes or banned vocabulary
6. [ ] Synergy hooks embedded naturally
7. [ ] SEO-optimized titles and descriptions

## When complete
After all 30 files created:
Output: <promise>RELAX_BATCH_COMPLETE</promise>
