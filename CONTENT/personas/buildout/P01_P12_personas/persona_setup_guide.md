# Persona Setup Guide — Tools, Platforms, Compliance

## Overview

This guide covers the complete technical stack for launching and operating AI-powered SFW personas. All 12 personas (P01-P12) share the same infrastructure with persona-specific customization at the content layer.

---

## AI Image Generation (Persona Faces)

### Option A: Midjourney (recommended for photorealistic)
**Plan:** Basic $10/mo or Standard $30/mo

**Face generation workflow:**
1. Create initial character sheet (5-10 images of same "character" from different angles)
2. Save seed number from best result
3. Use `--sref` (style reference) and `--cref` (character reference) for consistency
4. Create a library of 50+ images before launch

**Prompt formulas by persona:**

Fitness persona:
```
athletic [ethnicity] woman, 28 years old, fit physique, professional headshot, athletic wear, natural lighting, bokeh background, Instagram-quality, photorealistic --ar 1:1 --v 6.1
```

Faith/lifestyle:
```
warm [ethnicity] woman, 30s, natural beauty, soft smile, cozy indoor setting, natural window light, authentic, photorealistic, lifestyle photography --ar 1:1 --v 6.1
```

Business/solopreneur:
```
confident [ethnicity] man/woman, 28-35, professional casual, laptop visible, clean minimal office background, natural light, LinkedIn-quality --ar 1:1 --v 6.1
```

**Consistency tips:**
- Lock in face shape, skin tone, hair with first approved image
- Always use same lighting descriptor
- Create a "reference sheet" post with 4-6 angles saved offline
- Never mix Midjourney versions for same persona (use v6.1 exclusively)

### Option B: This Person Does Not Exist / Generated Photos
- thispersondoesnotexist.com: free, truly random, no consistency across sessions
- generated.photos: $9.99/mo, searchable, adjustable parameters
- Use for throwaway accounts, not main persona that needs consistency

### Option C: Illustrated Avatar (zero AI detection risk)
- Canva avatar builder: free, customizable, clearly illustrated
- Anime/cartoon style: eliminates AI face detection entirely
- Works well for: BuildrBot (tech persona), StudyWithAI, financial personas
- Disadvantage: less human connection vs. photorealistic

### Option D: HeyGen Video Avatar
- Create a full talking avatar video for $29/mo
- Best for: YouTube channel faces, video content at scale
- Persona speaks your script in a realistic video format
- Requires script → HeyGen → upload pipeline

---

## Video Production Stack

### Short-form video (TikTok/Reels/Shorts)

**Minimal viable stack ($0 additional cost):**
1. Claude writes script
2. ElevenLabs generates voiceover ($11/mo Starter)
3. CapCut adds captions + B-roll (free)
4. Buffer schedules posting ($18/mo)

**Full production stack ($45/mo additional):**
- Invideo AI ($25/mo): text-to-video with stock footage
- Pictory ($19/mo): script-to-video with auto-captions
- HeyGen ($29/mo): talking avatar videos

**CapCut batch workflow:**
1. Import all audio files for the week
2. Use CapCut "auto caption" feature on each
3. Add text overlays for hook (first 3 seconds)
4. Export all at 1080x1920 (vertical) or 1080x1080 (square)
5. Total time: 90 min for 7 videos at full pace

### Long-form video (YouTube)
- Script: Claude Opus (highest quality for long-form)
- Voice: ElevenLabs Professional ($99/mo for quality) OR ElevenLabs Standard ($11/mo)
- Visuals: stock footage (Pexels/Pixabay free, Storyblocks $149/yr)
- Editing: CapCut desktop or DaVinci Resolve (free)
- Thumbnails: Canva (use template → update text + image each video)

---

## Written Content Stack

### Caption writing (batch mode)
Claude prompt template for batch generation:
```
You are the social media manager for [PERSONA NAME], a [NICHE] content account on [PLATFORM].

Voice: [2-3 sentences describing voice style]
Audience: [who follows this account]
Goal: [what we want followers to do]

Write [NUMBER] separate [POST TYPE] posts about the following topics:
[LIST TOPICS]

Rules:
- No em dashes
- No AI vocabulary (leverage, comprehensive, robust, seamless, innovative)
- Lead with consequence, not explanation
- Specific numbers where possible
- Max [CHARACTER LIMIT] per post
- End with a soft CTA or observation, not "follow for more" every time
```

### Newsletter copy
- Platform: Beehiiv (free up to 2,500 subscribers, then $42/mo)
- Template: Welcome → educational → product mention → CTA → PS line
- Cadence: weekly, same day each week (algorithm + reader habit)

---

## Platform Setup by Account

### Instagram
**Username:** @[personahandle] — short, lowercase, no numbers
**Profile photo:** 2MB or less, 180x180px displayed, no text in photo
**Bio:** 150 characters. Format: what you do + who for + where to go
**Link in bio:** Beacons.ai (free tier) or Linktree
**Category:** Creator / Personal Blog / Education
**Professional Account:** switch to Creator Account immediately
**Contact:** set up dedicated email (persona@gmail.com) for brand deal inquiries

**First 9 posts strategy:** post 9 pieces in first week to fill grid. First impression is grid view.
**Stories:** post daily from day 1 — polls, Q&As, reposts of relevant content

### TikTok
**Username:** @[personahandle] — match Instagram handle exactly
**Profile:** same photo as Instagram (consistency)
**Bio:** 80 characters max + link (requires 1K followers for clickable link)
**Category:** Education / Lifestyle / Entertainment depending on niche
**Analytics:** switch to Creator Account → Business Account (to access TikTok Analytics)
**First post:** your best content. algorithm judges early velocity.

**TikTok Creator Program:**
- Requires: 10K followers + 100K views in last 30 days + 18+ years + US/UK/etc.
- Pays: $0.40-0.80 per 1,000 views (RPM)
- Better revenue path: affiliate links via video description

### YouTube
**Channel name:** [PersonaName] — exact handle match
**Description:** Include keywords. What the channel is about, who it's for, upload schedule.
**Trailer video:** 60-90 second intro video. Pin to channel. Explains value prop.
**Playlist:** create topic playlists immediately, even with 1 video each
**YouTube Partner Program:** 1,000 subscribers + 4,000 watch hours OR 10M Shorts views
**Shorts vs Long:** launch with Shorts for growth, long-form for revenue

### Pinterest
**Business account:** free, required for analytics and promoted pins
**Username:** @[personahandle]
**Boards:** 10-15 boards created at launch, SEO-optimized names
**Pinning cadence:** 5-10 pins/day (use Tailwind $19.99/mo or manual with Buffer)
**Profile photo:** same as other platforms
**Bio:** include niche keywords (Pinterest is a search engine)

### X/Twitter
**Handle:** @[personahandle]
**Bio:** 160 characters. Include keywords. Pinned post = your best content.
**Profile:** verified/subscribed gets better distribution (X Premium $8/mo)
**Content:** threads outperform single tweets 3:1 for engagement
**Scheduling:** Buffer or Hypefury ($49/mo for advanced analytics)

### LinkedIn
**For B2B personas only** (BuildrBot P04, CodeLane P07, WealthCraft P06)
**Profile setup:** complete every field (LinkedIn penalizes incomplete profiles)
**Creator Mode:** enable immediately (gets newsletter + follow button)
**Posting:** text-only posts with line breaks outperform links (algorithm suppresses external links)
**Newsletter:** LinkedIn Newsletter feature — free, goes to all followers

---

## Scheduling and Automation

### Buffer ($18/mo Essentials)
- 3 channels, unlimited posts
- Schedule 30 days in advance
- Best times feature (auto-optimizes posting windows)
- Use for: Instagram, Facebook, LinkedIn, Pinterest, X

### Later ($18/mo Starter)
- Visual content calendar
- Instagram-focused
- Auto-publish Reels + Stories
- Hashtag suggester built in

### TikTok TikTok Scheduler (free, native)
- Found in TikTok Studio
- Schedule up to 10 days ahead
- Only for verified creators with Business Account

### Zapier connections (useful automations)
- RSS → Buffer (auto-share content from relevant blogs)
- New YouTube video → post to Twitter/LinkedIn
- Beehiiv subscriber → Google Sheets (backup list)
- Stripe purchase → Beehiiv tag (segment buyers from free subscribers)

---

## Compliance and Legal

### FTC Disclosure Requirements (US)

**Affiliate links:** must disclose in every post with an affiliate link
- Acceptable: "#ad" "#affiliate" "Affiliate link" "I earn a commission"
- Must be visible without clicking "see more"
- Not acceptable: buried in hashtags, text too small to notice

**Sponsored content:** must disclose paid partnership
- Platform-native tools: Instagram "Paid Partnership" label, TikTok "Paid Partnership" sticker
- These are legally sufficient AND preferred by FTC
- Supplement with caption disclosure: "partnered with [brand] to share this"

**Income/results claims:**
- "I made $X" requires substantiation
- Use: "users report" / "clients typically see" / "up to X results"
- Add disclaimer: "results not typical" for any specific outcome claim

### AI Persona Disclosure
- US law (as of 2026): no requirement to disclose AI-generated personas
- EU AI Act: disclosure required for synthetic media that could deceive
- Best practice: if asked directly "are you AI?", answer honestly
- For synthetic video personas (HeyGen): disclose in description on YouTube, TikTok
- Platform rules vary: TikTok requires AI-generated label on realistic synthetic media

### Platform-specific policies
- **Instagram:** Branded Content Policies — must tag brand partner for paid posts
- **TikTok:** prohibits AI-generated images in ads without disclosure
- **YouTube:** requires disclosure in description for sponsored content
- **Pinterest:** prohibits deceptive content, requires ad labels for paid promotions

### Account Safety
- Never share login credentials
- Use different email per persona (personas@yourdomain.com vs selah@yourdomain.com)
- Enable 2FA on all accounts
- Store recovery codes offline
- Don't use the same IP for all accounts (use different networks or residential proxies if managing 5+ accounts)

---

## Analytics Tracking

### What to track per platform (weekly)

| Metric | Why It Matters | Target |
|--------|---------------|--------|
| Follower growth rate | Account velocity | 5-10%/week early stage |
| Average views per post | Distribution health | Rising trend |
| Engagement rate | Audience quality | 3-5% Instagram, 5-10% TikTok |
| Click-through rate (bio link) | Traffic conversion | 2-5% |
| Email sign-ups | Owned audience building | 1-2% of followers |
| Affiliate link clicks | Revenue potential | Track via affiliate dashboard |
| Sales/conversions | Revenue | Track via Gumroad/Stripe |

### Tools
- **Metricool** (free tier): cross-platform analytics
- **Iconosquare** ($49/mo): deep Instagram analytics
- **Native TikTok Analytics**: good enough for most metrics
- **Google Analytics 4**: for bio link click-throughs
- **Beehiiv analytics**: email open/click rates

---

## Account Warmup Protocol (New Accounts)

**Week 1-2:**
- Post every day (even if low quality)
- Engage with 20-30 accounts in your niche daily (genuine comments)
- Follow 10-20 accounts per day (follow back culture in some niches)
- Don't post affiliate links yet

**Week 3-4:**
- Increase content quality, maintain frequency
- Start adding affiliate links (1 per 5 posts max)
- Begin DM outreach to potential collaborators (similar-size accounts)
- Monitor which content formats perform best

**Month 2+:**
- Test different hooks, formats, and topics
- Kill what doesn't work after 2-3 attempts
- Double down on what works
- Start pitching brands for paid deals (even micro at 1K followers)

---

## Red Flags: What Gets Accounts Banned

- Buying followers (platform detection has improved significantly in 2025-2026)
- Mass following/unfollowing (follow > 100/day on Instagram = risk)
- Posting the same exact content on 2 accounts simultaneously (duplicate content detection)
- Using banned hashtags (look up updated ban lists for your niche)
- Automated likes/comments via bots (Jarvee, ManyChat for Instagram is fine, Instabot-style = ban)
- Repeatedly posting content that gets reported (check what triggers reports in your niche)
- Links to prohibited sites in bio (check each platform's restricted categories)
- Switching niches dramatically (confuses algorithm, drops distribution)

---

## Launch Sequence (Day by Day)

**Day -7 (before launch):** create all accounts, set up profiles, generate 30+ posts in content bank

**Day -3:** create teaser story: "launching something new [date]" — builds initial curiosity

**Day 1 (launch day):** post 3 pieces of best content across the day. Engage with every comment within 2 hours.

**Day 2-7:** post 1-2x/day. Engage 30 min/day minimum. Follow 10 accounts/day in niche.

**Day 8-30:** maintain cadence. Test hooks. Note which posts get saves (highest-value signal).

**Day 31:** review analytics. Kill worst-performing formats. Double best-performing formats. Plan month 2.
