# PRINTMAXX Master Automation Plan

Tech stack, workflows, Ralph loops, and anti-ban strategies for all money methods.

**Status:** PLANNING - Awaiting greenlight before execution

---

## Executive Summary

**Goal:** Scale 29 money methods/sub-categories with maximum automation, minimum bans, budget-friendly.

**Core Strategy:**
1. **Repurpose > Create** - 80% repurposed content, 20% original (Pareto)
2. **Warm first, automate later** - Manual warmup, then gradual automation
3. **Ralph loops for content** - Overnight generation, morning review
4. **Mix repost + original** - Avoid algorithm flags by varying content sources
5. **Quote tweets + replies** - Engagement hacks before original posts

---

## Tech Stack (Budget: ~$200-400/mo at scale)

### Tier 1: Essential (Day 1)

| Tool | Cost | Purpose |
|------|------|---------|
| **Soax Residential** | $99/mo (~15GB) | Social automation proxies |
| **Instantly.ai** | $37/mo | Cold email sending + warmup |
| **Buffer** | $15/mo | Multi-platform scheduling |
| **Claude Max** | Already have | Ralph loops, content generation |

### Tier 2: Scale (Week 2+)

| Tool | Cost | Purpose |
|------|------|---------|
| **Decodo (Smartproxy)** | $75/5GB | Backup proxy pool |
| **Hypefury** | $29/mo | X-specific scheduling + threads |
| **Make.com** | Free tier | Workflow automation |
| **n8n (self-hosted)** | Free | Complex automation flows |

### Tier 3: Advanced (Month 2+)

| Tool | Cost | Purpose |
|------|------|---------|
| **Mobile Proxies** | $100-150/mo | Main monetized accounts |
| **Apollo.io** | $49/mo | Lead data for outbound |
| **Aged accounts** | One-time $200-500 | Pre-warmed accounts |

### Development Stack

| Tool | Purpose |
|------|---------|
| **Playwright** | Browser automation (posting, scraping) |
| **Selenium** | Backup browser automation |
| **Claude Chrome MCP** | Browser control from Claude |
| **yt-dlp** | Download videos for repurposing |
| **FFmpeg** | Video processing, clipping |
| **Whisper** | Transcription for clip analysis |
| **Remotion** | Video generation (already have) |

---

## Account Strategy

### Account Tiers

| Tier | Proxy | Automation | Purpose |
|------|-------|------------|---------|
| **Main** | Mobile proxy | Manual + light scheduling | Monetized, brand accounts |
| **Growth** | Residential rotating | Semi-automated | Building audience |
| **Burner** | Residential rotating | Full automation | Testing, volume |

### Accounts Per Method (Target)

| Method | Platform | Account Count | Tier Split |
|--------|----------|---------------|------------|
| MEME_CHANNELS | X, TikTok | 5-10 | 2 main, 3-5 growth, 2-3 burner |
| NEWS_SOCIALS | X | 3-5 | 1 main, 2-3 growth |
| RELAX_CHANNELS | YouTube, TikTok | 3-5 | 1 main, 2-3 growth |
| AI_INFLUENCER | X, IG, TikTok | 3-5 per persona | 1 main, 2 growth |
| WOMEN_APPRECIATION | X | 3-5 | All growth tier |
| CLIP_CHANNELS | TikTok, YT Shorts | 3-5 | 1 main, 2-3 growth |

### Account Warming Schedule

```
Week 1-2: Manual warming (no automation)
Week 3-4: Light scheduling via Buffer/Hypefury
Week 5+: Gradual Playwright automation
```

---

## Content Strategy: Repurpose First

### The 80/20 Rule

```
80% Repurposed Content:
- Download from target accounts
- Add own caption/insight
- Mix timing (not same time as original)
- Change format slightly (crop, caption style)

20% Original Content:
- AI-generated unique takes
- Remixed/edited clips
- Quote tweets with insight
- Engagement bait (polls, questions)
```

### Source Accounts (From comprehensive_results.csv)
/Users/macbookpro/Documents/PRINTMAXX_STARTER_KIT/OPS/MASTER_ACTION_PLAN.md
**MEME_CHANNELS sources:**
- @FearedBuck - Streamer clips, viral moments
- @kirawontmiss - Commentary, reactions
- @HumansNoContext / @NoContextHumans - Random viral content
- @AMAZlNGNATURE - Nature content (can cross-post)
- @Rainmaker1973 - Science/nature (fact-based)
- @AIWarper - AI slop content

**Strategy per source:**
1. Download last 2-3 months of top performing posts
2. Store media + captions in database
3. Repost with modifications at random intervals
4. Mix in original content between reposts
5. Quote tweet sources occasionally (engagement hack)

### Content Pipeline

```
SCRAPE → STORE → MODIFY → SCHEDULE → POST → TRACK

1. SCRAPE: Playwright downloads media + captions
2. STORE: Database with metadata (engagement, timing)
3. MODIFY: Add own caption, crop, add watermark
4. SCHEDULE: Queue with random timing
5. POST: Via Buffer or Playwright
6. TRACK: Monitor engagement, adjust strategy
```

---

## Ralph Loop Architecture

### Updated Ralph Setup (snarktank/ralph style)

```
PRINTMAXX_STARTER_KIT/
├── .ralph/
│   ├── guardrails.md          # Learned constraints
│   ├── progress.md            # What's done
│   ├── errors.log             # Failures
│   └── activity.log           # Token tracking
├── ralph_tasks/
│   ├── 00_daily_alpha.md      # Research task
│   ├── 01_content_memes.md    # Meme content gen
│   ├── 02_content_news.md     # News content gen
│   ├── 03_content_relax.md    # Relax channel content
│   ├── 04_ai_influencer.md    # AI persona content
│   ├── 05_clip_analysis.md    # Streamer clip extraction
│   ├── 06_repurpose_queue.md  # Process repurpose queue
│   └── prd.json               # Structured task list
└── AGENTS.md                   # Patterns discovered
```

### Ralph Task Template

```markdown
---
task_id: MEME_CONTENT_GEN
test_command: "python scripts/validate_content.py"
max_iterations: 20
completion_signal: "BATCH_COMPLETE"
---

# Task: Generate 50 meme posts for X

## Context
- Read .claude/rules/copy-style.md
- Check .ralph/guardrails.md for constraints
- Output to CONTENT/social/memes/

## Success Criteria
1. [ ] 50 posts written
2. [ ] Each < 280 chars
3. [ ] No em dashes
4. [ ] No banned AI vocabulary
5. [ ] Mix of formats (text, question, hot take)
6. [ ] Each saved as individual file

## Sources for inspiration
- LEDGER/comprehensive_results.csv (engagement patterns)
- Top posts from target accounts

## When complete
Output: <promise>BATCH_COMPLETE</promise>
```

### Parallel Ralph Agents

Run these overnight simultaneously:

```bash
# Terminal 1: Meme content
while true; do claude --prompt ralph_tasks/01_content_memes.md; sleep 10; done

# Terminal 2: News content
while true; do claude --prompt ralph_tasks/02_content_news.md; sleep 10; done

# Terminal 3: AI influencer content
while true; do claude --prompt ralph_tasks/04_ai_influencer.md; sleep 10; done

# Terminal 4: Research
while true; do claude --prompt ralph_tasks/00_daily_alpha.md; sleep 10; done
```

---

## Automation Scripts (Priority Order)

### Phase 1: Scraping & Data (Week 1)

| Script | Purpose | Priority |
|--------|---------|----------|
| `scrape_twitter_account.py` | Download posts + media from target accounts | HIGH |
| `extract_engagement_data.py` | Get likes/RTs/views for content analysis | HIGH |
| `transcript_analyzer.py` | Analyze YouTube transcripts for clips | HIGH |
| `content_database.py` | Store scraped content with metadata | HIGH |

### Phase 2: Content Processing (Week 2)

| Script | Purpose | Priority |
|--------|---------|----------|
| `caption_modifier.py` | Add unique captions to repurposed content | HIGH |
| `video_clipper.py` | Extract clips from long-form video | HIGH |
| `caption_generator.py` | Auto-caption videos | MEDIUM |
| `thumbnail_generator.py` | Create thumbnails for YouTube | MEDIUM |

### Phase 3: Posting Automation (Week 3+)

| Script | Purpose | Priority |
|--------|---------|----------|
| `x_poster.py` | Post to X with proxy support | HIGH |
| `tiktok_uploader.py` | Upload to TikTok | HIGH |
| `youtube_shorts_uploader.py` | Upload Shorts | MEDIUM |
| `multi_account_scheduler.py` | Manage posting across accounts | HIGH |

### Phase 4: Engagement & Growth (Week 4+)

| Script | Purpose | Priority |
|--------|---------|----------|
| `reply_bot.py` | Auto-reply to trending posts | MEDIUM |
| `quote_tweet_bot.py` | Quote tweet with insight | MEDIUM |
| `engagement_tracker.py` | Track growth metrics | MEDIUM |

---

## Anti-Ban Strategy

### Platform-Specific Rules

#### X (Twitter)

**DO:**
- Mix post types (text, media, quote, reply)
- Human-like timing (irregular intervals)
- Engage before posting (likes, replies)
- Use official API via Hypefury when possible
- Quote tweet instead of just repost
- Reply to own tweets (engagement hack)

**DON'T:**
- Post same content across accounts
- Use exact same captions
- Post at exact intervals (every hour on the hour)
- Mass follow/unfollow
- Use datacenter proxies

**Detection Avoidance:**
```python
# Random delay between actions
delay = random.uniform(30, 180)  # 30 sec to 3 min

# Vary posting times
hour_variance = random.randint(-2, 2)
minute_variance = random.randint(0, 59)

# Different captions for same media
captions = [variation_1, variation_2, variation_3]
caption = random.choice(captions)
```

#### TikTok

**DO:**
- Use official app for critical actions
- Enable location services
- Complete watch sessions before posting
- Engage authentically first
- Use trending sounds
- Post duets/stitches (counts as original)

**DON'T:**
- Use VPN (heavy detection)
- Mass like/follow
- Post identical content across accounts
- Use web version for posting
- Spam comments

**Mobile Proxy Required:**
- TikTok fingerprints heavily
- Always use mobile proxy for important accounts
- Residential OK for burner accounts

#### YouTube

**DO:**
- Complete metadata (title, description, tags)
- Custom thumbnails
- Consistent upload schedule
- Engage with comments
- Use Shorts + long-form

**DON'T:**
- Upload copyrighted music (ContentID)
- Clickbait without delivery (retention drop)
- Mass upload (looks bot-like)

#### Instagram

**DO:**
- Use all features (Stories, Reels, Posts)
- Respond to DMs/comments
- Consistent aesthetic
- Use hashtags (but not banned ones)

**DON'T:**
- Follow/unfollow rapidly (50 max/day)
- Use automation for DMs
- Comment spam
- Use third-party apps that require login

### Rate Limits (Safe Defaults)

| Platform | Action | Safe Limit |
|----------|--------|------------|
| X | Posts | 10-15/day |
| X | Likes | 50-100/day |
| X | Follows | 20-30/day |
| TikTok | Posts | 3-5/day |
| TikTok | Likes | 100-200/day |
| Instagram | Posts | 1-3/day |
| Instagram | Stories | 5-10/day |
| Instagram | Follows | 50/day |

### Recovery Protocol

```
IF account flagged:
1. STOP all automation immediately
2. Switch to manual only
3. Wait 48-72 hours
4. Check shadowban status
5. Resume slowly (50% of previous rate)
6. If persists, consider fresh account
```

---

## Content Repurposing Workflow

### Meme Channel Workflow

```
1. DAILY: Scrape top posts from source accounts
   - @FearedBuck, @kirawontmiss, @HumansNoContext, etc.
   - Store: media URL, caption, engagement metrics
   - Filter: >1000 likes in last 24h

2. PROCESS: Modify for reposting
   - Download media
   - Generate 3 caption variations
   - Add subtle watermark if video
   - Store in queue

3. SCHEDULE: Mix repost + original
   - 4 reposts : 1 original ratio
   - Random timing (not predictable)
   - Different accounts get different content

4. ENGAGE: Amplify posts
   - Quote tweet from other accounts
   - Reply with related content
   - Engage with replies
```

### News Socials Workflow

```
1. MONITOR: News sources
   - Twitter trending
   - Google News
   - Reddit front page
   - NewsAPI

2. FILTER: Newsworthy + viral potential
   - Breaking news
   - Controversial takes
   - Numbers/data
   - Visual content

3. PACKAGE: Viral format
   - "BREAKING: [headline]"
   - Key bullet points
   - Source link

4. POST: Speed matters
   - First to post wins
   - Cross-platform immediately
   - Follow up with analysis thread
```

### Clip Channel Workflow (STREAMER_CLIPS)

```
1. IDENTIFY: Top streamers with re-uploaded VODs
   - Search: "[streamer name] stream" on YouTube
   - Pull VOD URLs

2. TRANSCRIBE: Extract transcript
   - YouTube API or yt-dlp + Whisper
   - Save full transcript

3. ANALYZE: Find clippable moments
   - AI prompt: "Find high-engagement moments"
   - Criteria: emotion, skill, drama, funny
   - Output: timestamps

4. CLIP: Extract segments
   - FFmpeg: extract 30-60 sec clips
   - Auto-caption with Whisper

5. DISTRIBUTE: Post across accounts
   - TikTok, YouTube Shorts, X
   - Vary captions per platform
   - Tag/mention streamer (exposure)
```

---

## Manual Setup Required (Human Tasks)

### Day 1 (Before Automation)

- [ ] Create social accounts (manual, no shortcuts)
- [ ] Set up 2FA on all accounts
- [ ] Purchase Soax proxy subscription
- [ ] Create proxy assignments per account
- [ ] Complete profile setup on all accounts
- [ ] Start manual engagement (no posting)

### Week 1 (Warming Period)

- [ ] Daily 15-30 min manual engagement per account
- [ ] First posts Day 3-5 (manual)
- [ ] Monitor for any flags
- [ ] Set up Buffer/Hypefury accounts

### Week 2 (Light Automation)

- [ ] Connect accounts to Buffer/Hypefury
- [ ] Schedule first automated posts
- [ ] Continue manual engagement
- [ ] Review scraped content for quality

### Week 3+ (Scale)

- [ ] Deploy Playwright scripts
- [ ] Start Ralph loops overnight
- [ ] Monitor automation for issues
- [ ] Adjust rate limits as needed

---

## Automated Out the Gate

These can run immediately (no account warmup needed):

### Research & Scraping
- [x] Scrape source accounts for content
- [x] Download media from target accounts
- [x] Extract engagement data
- [x] Build content database
- [x] Analyze transcripts for clips

### Content Generation (Ralph Loops)
- [x] Generate meme captions
- [x] Generate news posts
- [x] Generate AI influencer content
- [x] Create caption variations
- [x] Build content queues

### Processing
- [x] Process videos (clip, caption)
- [x] Generate thumbnails
- [x] Modify repurposed content
- [x] Build posting schedules

---

## Budget Breakdown

### Minimum Viable ($150/mo)

```
Soax 5GB: $33
Instantly: $37
Buffer: $15
Claude Max: (already have)
-----------
Total: ~$85/mo

Plus one-time:
- Aged accounts: $100-200
```

### Standard Scale ($250/mo)

```
Soax 10GB: $66
Instantly: $37
Hypefury: $29
Buffer: $15
Make.com: Free
-----------
Total: ~$147/mo
```

### Full Scale ($400/mo)

```
Decodo 10GB: $100
Mobile proxies (2): $180
Instantly: $37
Hypefury: $29
Apollo: $49
-----------
Total: ~$395/mo
```

---

## Pareto Shortcuts (80/20 Wins)

### Biggest Leverage Points

1. **Repurpose top-performing content** - Already proven to work
2. **Quote tweet strategy** - Engagement without original content
3. **Reply-guy accounts** - Build audience via replies
4. **News first-mover** - Speed beats quality for breaking news
5. **AI influencer + Info product** - Build audience, sell course

### Time Investment vs Return

| Activity | Time | Return | Priority |
|----------|------|--------|----------|
| Scrape + repost | 1hr setup | High | Do first |
| Quote tweet strategy | 30min/day | High | Do first |
| Ralph content gen | Overnight | Medium | Week 2 |
| Original content | 2-4hr/batch | Medium | Week 3 |
| Engagement automation | 2hr setup | Medium | Week 4 |

### What to Skip Initially

- Complex video editing (use raw clips)
- Perfect thumbnails (iterate later)
- Multiple platforms (focus on X + TikTok first)
- Engagement pods (risky, diminishing returns)
- Buying followers (waste of money)

---

## Greenlight Checklist

**Before execution, confirm:**

- [ ] Soax proxy account created
- [ ] Social accounts created (manual)
- [ ] 2FA enabled on all accounts
- [ ] Buffer or Hypefury connected
- [ ] Content database structure approved
- [ ] Ralph task files reviewed
- [ ] Anti-ban rules understood
- [ ] Manual warmup commitment (2 weeks)

**Ready to execute?** Reply "GREENLIGHT" and specify which phase to start.

---

## Phase Execution Order

### Phase 1: Foundation (Days 1-14)
- Manual account warming
- Scraping scripts running
- Content database building
- Ralph loops for content generation

### Phase 2: Light Automation (Days 15-28)
- Buffer/Hypefury scheduling
- Repurpose pipeline active
- News monitoring live
- Continue manual engagement

### Phase 3: Scale (Days 29+)
- Playwright posting scripts
- Multi-account management
- Full Ralph loop operation
- Engagement automation (careful)

---

Last updated: 2026-01-22
