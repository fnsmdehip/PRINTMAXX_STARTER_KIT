# Twitter/X Account Creation SOP

**Created:** 2026-02-12
**Purpose:** Step-by-step guide for creating and launching 5 priority Twitter/X accounts
**Status:** READY FOR HUMAN EXECUTION

---

## Pre-Creation Checklist (Have Ready Before Starting)

### Required for ALL accounts
- [ ] Email addresses (unique per account, ProtonMail recommended)
- [ ] Phone number (can reuse across 2-3 accounts max, then need new numbers)
- [ ] Profile photos generated (see image prompts per account below)
- [ ] Banner images generated (see image prompts per account below)
- [ ] Bio text copied from this doc (character-counted, ready to paste)
- [ ] VPN or clean IP (Twitter flags multiple account creation from same IP)
- [ ] Browser profile separation (use different Chrome profiles or anti-detect browser)

### Recommended
- [ ] Pre-written first 5 tweets per account (see "Day 1 Tweets" section)
- [ ] Buffer or Publer account for scheduling
- [ ] Content calendar loaded: `LEDGER/CONTENT_CALENDAR_30DAY.csv`

### Anti-Ban Precautions
- Create accounts 24-48 hours apart (NOT all same day)
- Use different IPs per account (VPN rotate or mobile data)
- Complete profile fully before tweeting (photo, banner, bio, pinned tweet)
- Do NOT follow accounts from other PRINTMAXX accounts immediately
- Do NOT like/RT between owned accounts in first 2 weeks
- Wait 48 hours after creation before posting

---

## Account 1: @PRINTMAXXER (Tech / Building in Public)

**Priority:** HIGHEST (flagship account, all other accounts cross-promote to this)
**Niche:** Solopreneur tech, AI tools, building in public, indie hacking
**Brand color:** Neon green #00FF41 on black #0D0D0D
**Email:** printmaxxer@protonmail.com

### Step 1: Sign up
1. Go to twitter.com/i/flow/signup
2. Use email: printmaxxer@protonmail.com
3. Set display name: PRINTMAXXER
4. Set handle: @PRINTMAXXER (if taken, try @printmaxxer_ or @PRINTMAXX3R)
5. Skip all "follow these accounts" and "turn on notifications" prompts
6. Verify email

### Step 2: Profile photo
Generate using one of these prompts:

**Midjourney v6:**
```
Minimalist terminal cursor icon, bright neon green (#00FF41) "PM>_" text on pure black (#0D0D0D) background, monospace font, slight CRT screen glow effect around the text, retro hacker terminal aesthetic, clean and sharp, no gradients except the subtle glow --ar 1:1 --v 6 --style raw
```

**DALL-E 3:**
```
A square minimalist logo on pure black (#0D0D0D) background. Bright neon green (#00FF41) text reading "PM>_" in a clean monospace font, centered. A very subtle green CRT-style glow surrounds the text. The style is retro terminal/hacker aesthetic but clean and modern. No other elements, no gradients, no busy details. Think classic green-on-black computer terminal.
```

**Style notes:** ACCEPT clean terminal aesthetic, monospace, hacker vibes. REJECT skulls, matrix rain, circuit boards, generic tech imagery.

### Step 3: Banner image
**Midjourney v6:**
```
Wide dark terminal screen aesthetic, black (#0D0D0D) background, scattered fragments of green (#00FF41) code or text across the canvas as if a terminal is actively running, some lines brighter than others, subtle red (#FF0040) accent on one line like an error or alert, the center area slightly darker and emptier for text overlay safe zone, no actual readable code --ar 3:1 --v 6 --style raw
```

### Step 4: Bio
Paste this exactly (155 chars):
```
building 11 revenue streams in public. $0 to $50K/mo arc. shipping apps, content, cold outbound, AI tools. everything documented. follow the build log.
```

**Alternate if primary feels wrong (152 chars):**
```
solopreneur running 11 money methods simultaneously. apps, newsletters, AI, cold email. $0 right now. documenting the entire climb. raw numbers only.
```

### Step 5: Pinned tweet
Write and pin immediately after first tweet:
```
building 11 revenue streams from $0.

apps, newsletters, cold email, AI tools, content, affiliate, local biz websites, digital products, freelance arb, clipping, POD.

documenting everything. real numbers. no guru shit.

follow along.
```

### Step 6: Log creation
```bash
python3 scripts/account_tracker.py add --platform twitter --username PRINTMAXXER --email printmaxxer@protonmail.com --status CREATED --niche tech
```

---

## Account 2: @daily_anchor_faith (Faith / Prayer)

**Priority:** HIGH (Ramadan starts Feb 28, time-sensitive content opportunity)
**Niche:** Faith, daily prayer, spiritual discipline, PrayerLock app promo
**Brand color:** Deep blue-gray #2C3E50, warm gold accent #E8B77D
**Email:** hello@dailyanchor.com or dailyanchor@protonmail.com

### Step 1: Sign up
1. Go to twitter.com/i/flow/signup
2. Use email: dailyanchor@protonmail.com
3. Set display name: DailyAnchor
4. Set handle: @daily_anchor_faith (if taken, try @dailyanchor_ or @thedailyanchor)
5. Skip all prompts, verify email

### Step 2: Profile photo
**Midjourney v6:**
```
Minimalist anchor icon in white (#FFFFFF) on deep blue-gray (#2C3E50) background, clean geometric line art style, a small warm gold (#E8B77D) circle at the top of the anchor suggesting a rising sun, simple elegant nautical design, no textures, no ropes, no ornate details, modern minimalist logo aesthetic --ar 1:1 --v 6 --style raw
```

**DALL-E 3:**
```
A minimalist square logo on a solid deep blue-gray (#2C3E50) background. A clean white geometric anchor shape is centered. At the top of the anchor, a small warm gold (#E8B77D) semicircle suggests a rising sun peeking above the anchor's crown. The style is flat, modern, no textures, no ropes, no ornate details. Think Apple-level simplicity. The anchor is geometric and clean, not illustrative or hand-drawn.
```

**Style notes:** ACCEPT clean geometry, flat color, generous whitespace, warm but restrained. REJECT stock photo sunsets, praying hands, crosses, ornate rope details, weathered textures, church imagery, doves.

### Step 3: Banner image
**Midjourney v6:**
```
Wide minimalist seascape at dawn, deep blue-gray (#2C3E50) ocean meeting a warm gold (#E8B77D) horizon line, very subtle calm water texture, clean and calm composition, the horizon sits at the lower third, vast sky in blue-gray tones, warm golden light just beginning at edge, no boats, no land, no text, meditative and serene --ar 3:1 --v 6 --style raw
```

### Step 4: Bio
Paste this exactly (148 chars):
```
127-day prayer streak. 5am anchor routine. documenting what consistency does to your life when you stop treating faith like a weekend hobby. PrayerLock
```

**Alternate (144 chars):**
```
daily prayer + scripture + gratitude. tracking streaks, sharing what works. 127 days in. faith isn't passive. app: PrayerLock. join the morning.
```

### Step 5: Pinned tweet
```
started a prayer streak 127 days ago.

5am. every day. scripture, gratitude list, 10 minutes of silence.

here's what changed:
- anxiety dropped noticeably by week 3
- actually look forward to mornings now
- decisions feel clearer

not selling anything. just documenting what consistency does.
```

### Step 6: Log creation
```bash
python3 scripts/account_tracker.py add --platform twitter --username daily_anchor_faith --email dailyanchor@protonmail.com --status CREATED --niche faith
```

---

## Account 3: @three_hour_physique (Fitness / Health)

**Priority:** HIGH (evergreen niche, strong affiliate potential)
**Niche:** Evidence-based minimal training, fitness, health
**Brand color:** Near black #1A1A1A, red-orange accent #FF4500
**Email:** threehourphysique@protonmail.com

### Step 1: Sign up
1. Go to twitter.com/i/flow/signup
2. Use email: threehourphysique@protonmail.com
3. Set display name: MinimalPhysique
4. Set handle: @three_hour_physique (if taken, try @minimalphysique or @3hrphysique)
5. Skip all prompts, verify email

### Step 2: Profile photo
**Midjourney v6:**
```
Ultra-minimalist logo, a geometric barbell shape made of two white circles connected by a thin white horizontal line, on near-black (#1A1A1A) background, one circle filled with red-orange (#FF4500), clean flat vector style, no gradients, no shadows, no 3D, stark and precise, centered with generous dark padding --ar 1:1 --v 6 --style raw
```

**DALL-E 3:**
```
A minimalist square logo on a near-black (#1A1A1A) background. A geometric barbell shape: two circles connected by a thin horizontal line. The left circle is white outline only. The right circle is filled with red-orange (#FF4500). The design is ultra-flat, clean, no gradients, no shadows, no 3D effects. It looks like a high-end fitness brand mark, not a gym logo. Geometric precision, centered with ample dark space around it.
```

**Style notes:** ACCEPT clean geometry, flat design, stark contrast, minimal. REJECT shirtless bodies, protein shakers, dumbbells with detail, sweat drops, flames, tribal patterns, muscle illustrations.

### Step 3: Banner image
**Midjourney v6:**
```
Wide minimalist composition on near-black (#1A1A1A), a single bold red-orange (#FF4500) horizontal line cutting across the center, white geometric shapes suggesting simplified workout movements (circles, angles) arranged along the line, stark contrast, flat design, no people, no equipment photos, abstract fitness typography aesthetic --ar 3:1 --v 6 --style raw
```

### Step 4: Bio
Paste this exactly (142 chars):
```
3 hours per week in the gym. better results than most 6-day splits. evidence-based minimal training. real numbers. no supplements to sell you.
```

**Alternate (131 chars):**
```
minimal effective dose training. 3 sessions/week, 60 min each. posting real weights, reps, progress photos. no bro science allowed.
```

### Step 5: Pinned tweet
```
you spend 8 hours per week in the gym and i get better results in 3.

not because i'm gifted. because most people do 3x more volume than the research says they need.

this account: real weights, real reps, real progress photos. 3 sessions/week. 60 min each.

no coaching to sell. just the training log.
```

### Step 6: Log creation
```bash
python3 scripts/account_tracker.py add --platform twitter --username three_hour_physique --email threehourphysique@protonmail.com --status CREATED --niche fitness
```

---

## Account 4: @SleepMaxx (Sleep / Wellness)

**Priority:** MEDIUM (strong niche, good affiliate potential for mattress/supplement)
**Niche:** Sleep science, sleep optimization, wellness
**Brand color:** Deep navy #0A1628, soft blue accent #4A90D9, lavender #B8A9C9
**Email:** hello@sleepmaxx.com or sleepmaxx@protonmail.com

### Step 1: Sign up
1. Go to twitter.com/i/flow/signup
2. Use email: sleepmaxx@protonmail.com
3. Set display name: SleepMaxx
4. Set handle: @SleepMaxx (if taken, try @sleepmaxx_ or @thesleepmaxx)
5. Skip all prompts, verify email

### Step 2: Profile photo
**Midjourney v6:**
```
Minimalist crescent moon icon in white (#FFFFFF) on deep navy (#0A1628) background, the moon is a clean geometric crescent shape, two or three small dots as simplified stars near the moon, one star in soft blue (#4A90D9) and one in lavender (#B8A9C9), flat design, no gradients, no face on the moon, no cartoonish elements, elegant and calm --ar 1:1 --v 6 --style raw
```

**DALL-E 3:**
```
A minimalist square logo on deep navy (#0A1628) background. A clean geometric white crescent moon is centered. Two small dots representing stars sit near the moon: one in soft blue (#4A90D9), one in lavender (#B8A9C9). The design is flat, modern, no gradients, no textures, no cartoon face on the moon. It reads as a premium wellness brand mark, sophisticated and calm. Ample navy space surrounds the icon.
```

**Style notes:** ACCEPT clean geometric shapes, flat color, premium feel, calm energy. REJECT cartoon sheep, ZZZ letters, sleeping faces, pillows, generic wellness stock imagery, cute/childish moon faces.

### Step 3: Banner image
**Midjourney v6:**
```
Wide minimalist nightscape on deep navy (#0A1628), a gentle sine wave pattern in soft blue (#4A90D9) running horizontally through the center suggesting sleep cycles, small scattered dots in white and lavender (#B8A9C9) above the wave like stars, calm and meditative, no landscape features, abstract data visualization of sleep, clean and serene --ar 3:1 --v 6 --style raw
```

### Step 4: Bio
Paste this exactly (141 chars):
```
8pm screen cutoff. 65F room. 10pm lights out. went from 5.5 hrs of broken sleep to 7.5 hrs of deep sleep in 3 weeks. posting the protocol.
```

**Alternate (137 chars):**
```
fixed my sleep in 3 weeks with 4 changes. no supplements, no gadgets, no mattress affiliate links. just the science. daily sleep tips.
```

### Step 5: Pinned tweet
```
slept terribly for years. 5.5 hours of broken, light sleep.

made 4 changes:
1. 8pm screen cutoff (or orange glasses)
2. 65F bedroom temperature
3. 10pm lights out, same time every night
4. morning sunlight within 30 minutes of waking

3 weeks later: 7.5 hours of deep sleep. consistent. no supplements.

posting the full protocol here. one tip per day.
```

### Step 6: Log creation
```bash
python3 scripts/account_tracker.py add --platform twitter --username SleepMaxx --email sleepmaxx@protonmail.com --status CREATED --niche sleep
```

---

## Account 5: @ai_workflows_daily (AI/Tech Workflows)

**Priority:** MEDIUM (supports @PRINTMAXXER, different angle on same audience)
**Niche:** AI tool workflows, automation, no-code/low-code
**Brand color:** Black #000000, electric blue accent #0066FF
**Email:** aiworkflows@protonmail.com

### Step 1: Sign up
1. Go to twitter.com/i/flow/signup
2. Use email: aiworkflows@protonmail.com
3. Set display name: StackFlow
4. Set handle: @ai_workflows_daily (if taken, try @stackflow_ai or @aiworkflowsdaily)
5. Skip all prompts, verify email

### Step 2: Profile photo
**Midjourney v6:**
```
Minimalist abstract logo, a white equilateral triangle made of 3 small circles (nodes) connected by thin white lines, on pure black background, one node filled with electric blue (#0066FF), flat clean design, no gradients, no shadows, mathematical precision, like a simplified network graph or molecule --ar 1:1 --v 6 --style raw
```

**DALL-E 3:**
```
A minimalist square logo on pure black background. Three small white circles arranged in an equilateral triangle, connected by thin white lines. One circle is filled with electric blue (#0066FF). The design looks like a simplified network node or tech workflow graph. Ultra-flat, no gradients, no shadows, mathematical precision. Modern tech brand aesthetic.
```

**Style notes:** ACCEPT clean geometry, flat color, tech/network feel. REJECT robot faces, AI brain imagery, gears, lightbulbs, generic tech stock.

### Step 3: Banner image
**Midjourney v6:**
```
Wide minimalist design on black (#000000), a simplified neural network visualization, white dots and thin connecting lines, key pathways lit in electric blue (#0066FF), flat clean vector aesthetic, no 3D, no gradients, center zone kept minimal for text safe area, circuit board meets data flow diagram --ar 3:1 --v 6 --style raw
```

### Step 4: Bio
Paste this exactly (140 chars):
```
12 AI tools wired together in 4 minutes. daily workflow breakdowns. what to use, how to connect them, what it replaces. no hype, just stacks.
```

**Alternate (144 chars):**
```
daily AI workflow breakdowns. 12 tools connected in 4 minutes. no tutorials, no courses. just the stack, the setup, and what it replaces. free.
```

### Step 5: Pinned tweet
```
12 AI tools. 4 minutes to set up. replaces what used to take 3 hours.

this account: one workflow per day.
- what tools
- how they connect
- what it replaces
- exact setup steps

no courses to sell. no "AI is the future" fluff. just the stacks.
```

### Step 6: Log creation
```bash
python3 scripts/account_tracker.py add --platform twitter --username ai_workflows_daily --email aiworkflows@protonmail.com --status CREATED --niche ai_tools
```

---

## Post-Creation Warmup Protocol (ALL Accounts)

### Day 1-3: Silent Phase
- Complete profile fully (photo, banner, bio, location, website link if applicable)
- Follow 10-15 accounts in niche (real accounts you'd actually follow)
- Like 5-10 tweets (genuine engagement, not spam)
- Do NOT tweet yet
- Do NOT follow other PRINTMAXX accounts

### Day 4-7: Soft Launch
- Post first tweet (NOT the pinned tweet yet)
- 1-2 tweets per day max
- Reply to 3-5 tweets in niche (add real value, not "great post!")
- Follow 5-10 more relevant accounts
- Pin your intro tweet on day 5

### Day 8-14: Ramp Up
- 2-3 tweets per day
- 5-10 replies per day (quality replies that add context or data)
- Start following relevant accounts more aggressively (20-30/day max)
- Begin cross-promoting between accounts subtly (RT one thing from another account, max 1/day)

### Day 15+: Full Schedule
- Load content calendar into Buffer/Publer
- 3-5 tweets per day per account
- Consistent reply game (10+ per day)
- Cross-promote strategically (not spam)
- Begin outbound DMs to potential collaborators (after 100+ followers)

### Warmup Schedule Reference
Full warmup details in: `ralph/loops/social_setup/output/T5_warmup_schedules.md`

---

## A/B Testing Notes

For each account, test two approaches in the first 30 days:

| Test | Variable A | Variable B | Metric |
|------|-----------|-----------|--------|
| Bio | Primary bio | Alternate bio | Profile visit to follow ratio |
| Tweet style | Thread-heavy (2-3 threads/week) | Single tweets only | Engagement rate |
| Posting time | Morning (7-9am ET) | Evening (6-8pm ET) | Impressions |
| Reply strategy | Value-add replies | Question-based replies | Follow-backs |

Track results in: `python3 scripts/experiment_runner.py start --name "twitter_bio_test_PRINTMAXXER" --hypothesis "Primary bio converts better" --metric "follow_rate"`

---

## Creation Order and Timing

| Day | Account | Reason |
|-----|---------|--------|
| Day 1 | @PRINTMAXXER | Flagship, everything links back here |
| Day 3 | @daily_anchor_faith | Ramadan starts Feb 28, need warmup time |
| Day 5 | @three_hour_physique | Evergreen, strong affiliate potential |
| Day 7 | @SleepMaxx | Evergreen, good content-to-product pipeline |
| Day 9 | @ai_workflows_daily | Supports PRINTMAXXER, same audience different angle |

### Why 2-day gaps
- Twitter flags batch account creation from similar devices/IPs
- Gives time to generate proper images for next account
- Each account gets focused initial engagement before moving to next
- Reduces risk of all accounts being flagged/suspended simultaneously

---

## Quick Reference: All Account Details

| # | Handle | Display | Email | Niche | Colors |
|---|--------|---------|-------|-------|--------|
| 1 | @PRINTMAXXER | PRINTMAXXER | printmaxxer@protonmail.com | Tech/Build | #00FF41 on #0D0D0D |
| 2 | @daily_anchor_faith | DailyAnchor | dailyanchor@protonmail.com | Faith | #2C3E50 + #E8B77D |
| 3 | @three_hour_physique | MinimalPhysique | threehourphysique@protonmail.com | Fitness | #1A1A1A + #FF4500 |
| 4 | @SleepMaxx | SleepMaxx | sleepmaxx@protonmail.com | Sleep | #0A1628 + #4A90D9 |
| 5 | @ai_workflows_daily | StackFlow | aiworkflows@protonmail.com | AI Tools | #000000 + #0066FF |

---

## After ALL 5 Accounts Created

Run this to verify tracking:
```bash
python3 scripts/account_tracker.py status --platform twitter
```

Update master accounts file:
```bash
# Verify LEDGER/ACCOUNTS.csv has all 5 new Twitter entries
```

Load content into Buffer:
```bash
# Buffer CSVs ready at AUTOMATIONS/content_posting/
# Upload per-niche CSV to Buffer for each account
```

Cross-reference with content calendar:
- `LEDGER/CONTENT_CALENDAR_30DAY.csv` (1,278+ posts mapped)
- `OPS/CONTENT_POSTING_GUIDE.md` (platform-specific timing)

---

## Troubleshooting

**"Phone number already used"** - Use Google Voice, TextNow, or a prepaid SIM for additional numbers. Max 2-3 accounts per phone number.

**"Suspicious activity detected"** - Wait 24 hours. Do not retry immediately. Switch IP/browser profile.

**"Account suspended"** - Appeal immediately via help.twitter.com. Common for new accounts that tweet too fast. This is why warmup protocol matters.

**Handle taken** - Check alternatives listed per account above. Or use underscore prefix/suffix variations.

**Image generation issues** - Try all 3 AI tools (Midjourney, Leonardo, DALL-E). Midjourney v6 with --style raw gives cleanest results for logos. DALL-E 3 tends to add detail; add "minimalist, flat, simple" to counter.
