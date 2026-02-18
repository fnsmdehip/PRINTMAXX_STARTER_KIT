# YouTube Automation Deep Dive

Complete playbook for building and scaling faceless YouTube channels. Production workflows, AI tools, monetization strategies, and outsourcing systems.

---

## Executive Summary

YouTube remains the highest-paying platform for content creators in 2026. While TikTok and Instagram Reels offer reach, YouTube delivers 3-10x higher RPM for equivalent content. Faceless channels eliminate creator dependency, enabling portfolio strategies where 5-10 channels generate diversified income.

**Key findings:**
- Finance/investing niches: $15-50 CPM (highest on platform)
- YouTube Shorts: $0.40+ RPM baseline (still beats TikTok)
- Dan Koe reported $4,495 in 2 weeks from Shorts alone (Jan 2026)
- Multi-platform strategy: Same content, different monetization per platform
- Automation potential: 60-90% depending on niche

---

## Channel Type Comparison

### 1. Compilation Channels

**Examples:** FailArmy, Daily Dose of Internet, People Are Awesome

| Metric | Value |
|--------|-------|
| CPM Range | $1-4 |
| Competition | HIGH |
| Content Difficulty | LOW |
| Automation Level | HIGH (80%) |
| Time to $1K/mo | 8-14 months |
| Required Subs | 75K-150K |

**Content types:**
- Fail compilations
- Satisfying videos
- Amazing talent showcases
- Viral clip roundups
- Nature/animal compilations

**Production workflow:**
1. Source clips from Reddit, Twitter, TikTok (with permission or licensing)
2. Batch edit in DaVinci Resolve using templates
3. Add consistent intro/outro
4. AI voiceover for narration
5. Consistent thumbnail style

**Revenue at 100K subs:** $1,000-3,000/month

**Scaling advantage:** High volume production possible, low barrier to entry, but crowded market requires differentiation.

---

### 2. Educational/Explainer Channels

**Examples:** Kurzgesagt, Wendover Productions, How Money Works, Cold Fusion

| Metric | Value |
|--------|-------|
| CPM Range | $4-15 |
| Competition | MEDIUM |
| Content Difficulty | MEDIUM-HIGH |
| Automation Level | MEDIUM (50-60%) |
| Time to $1K/mo | 6-12 months |
| Required Subs | 40K-100K |

**Content types:**
- How things work
- History explainers
- Science breakdowns
- Economics/business analysis
- Technology deep dives

**Production workflow:**
1. Research with Perplexity + Claude
2. Script with AI assistance (Claude for drafts, human edit for voice)
3. Storyboard key visuals
4. ElevenLabs voiceover
5. Motion graphics in After Effects or Canva
6. B-roll from stock libraries

**Revenue at 100K subs:** $2,000-10,000/month

**Scaling advantage:** High CPMs, sponsorship-friendly, evergreen content compounds views over time.

---

### 3. Relaxation/Ambient Channels

**Examples:** Lofi Girl, Yellow Brick Cinema, Relaxing White Noise

| Metric | Value |
|--------|-------|
| CPM Range | $0.50-3 (meditation content higher: $5-8) |
| Competition | MEDIUM |
| Content Difficulty | LOW |
| Automation Level | HIGHEST (90%) |
| Time to $1K/mo | 12-18 months |
| Required Subs | 100K-200K |

**Content types:**
- Lofi music streams
- Nature sounds
- Rain/fireplace ambiance
- Sleep music compilations
- Guided meditation

**Production workflow:**
1. Source royalty-free music (Suno AI, Epidemic Sound)
2. Stock nature footage (Pexels, Artgrid)
3. FFmpeg scripts for looping 8-10 hour videos
4. 10+ mid-roll ads per 8-hour video
5. Thumbnail: dark/muted colors, moon/cozy imagery

**Revenue at 100K subs:** $500-2,000/month (but scales with long videos = more ad breaks)

**Scaling advantage:** Create once, earn forever. Evergreen demand. 8-hour videos = 8 hours watch time per viewer. Highest automation potential.

---

### 4. News/Commentary Channels

**Examples:** Philip DeFranco style (without face), The Infographics Show

| Metric | Value |
|--------|-------|
| CPM Range | $3-10 |
| Competition | HIGH |
| Content Difficulty | MEDIUM |
| Automation Level | LOW (40%) |
| Time to $1K/mo | 8-14 months |
| Required Subs | 50K-100K |

**Content types:**
- Current events breakdown
- News aggregation
- Trending topic analysis
- Industry updates

**Production workflow:**
1. TweetDeck + Google Alerts for monitoring
2. 15-30 minute window for breaking content
3. AI-assisted script writing
4. Quick turnaround editing
5. Consistent visual style

**Revenue at 100K subs:** $2,000-6,000/month

**Scaling advantage:** High engagement, binge-worthy series potential, but requires speed and consistency.

---

### 5. Top 10/Listicle Channels

**Examples:** WatchMojo, MostAmazingTop10, TheRichest

| Metric | Value |
|--------|-------|
| CPM Range | $3-10 |
| Competition | HIGH |
| Content Difficulty | LOW-MEDIUM |
| Automation Level | HIGH (70%) |
| Time to $1K/mo | 8-12 months |
| Required Subs | 50K-100K |

**Content types:**
- Top 10 lists (any topic)
- Ranking videos
- "Best of" compilations
- Comparison videos
- "X vs Y" content

**Production workflow:**
1. Keyword research for trending topics
2. AI research for list content
3. Template-based editing
4. Stock footage compilation
5. SEO-optimized titles

**Revenue at 100K subs:** $1,500-5,000/month

**Scaling advantage:** Formulaic production, fast turnaround, daily upload possible.

---

### 6. True Crime/Mystery Channels

**Examples:** Coffeehouse Crime, Lazy Masquerade, Mr. Nightmare

| Metric | Value |
|--------|-------|
| CPM Range | $4-12 |
| Competition | MEDIUM-HIGH |
| Content Difficulty | HIGH |
| Automation Level | LOW (30-40%) |
| Time to $1K/mo | 6-10 months |
| Required Subs | 30K-75K |

**Content types:**
- True crime cases
- Unsolved mysteries
- Internet mysteries
- Reddit story narrations
- Creepy compilations

**Production workflow:**
1. Deep research on cases
2. Atmospheric script writing
3. Professional voiceover (AI or human)
4. Dark, moody visuals
5. Sound design for tension

**Revenue at 100K subs:** $3,000-10,000/month

**Scaling advantage:** Highest engagement and retention, loyal audiences, but harder to automate due to research requirements.

---

### Channel Type Matrix

| Type | CPM | Competition | Difficulty | Evergreen | Automation | Scale Potential |
|------|-----|-------------|------------|-----------|------------|-----------------|
| Compilation | $1-4 | HIGH | LOW | MEDIUM | 80% | HIGH |
| Educational | $4-15 | MEDIUM | MED-HIGH | HIGH | 50-60% | MEDIUM |
| Relaxation | $0.50-8 | MEDIUM | LOW | HIGH | 90% | HIGH |
| News | $3-10 | HIGH | MEDIUM | LOW | 40% | MEDIUM |
| Top 10/Lists | $3-10 | HIGH | LOW-MED | HIGH | 70% | HIGH |
| True Crime | $4-12 | MED-HIGH | HIGH | HIGH | 30-40% | LOW |
| Finance | $10-30 | HIGH | HIGH | HIGH | 40-50% | MEDIUM |
| Tech | $6-15 | HIGH | MEDIUM | MEDIUM | 50-60% | MEDIUM |

---

## Production Workflow

### Phase 1: Research and Scripting

**Tools:**
- Perplexity Pro ($20/mo) - Topic research, fact-checking
- Claude Pro ($20/mo) - Script drafts, outlines
- TubeBuddy ($9/mo) - Keyword research, competition analysis
- vidIQ ($10/mo) - Trending topics, SEO optimization

**Script structure (8-15 min videos):**
```
Hook (0-30s): Pattern interrupt, question, or bold claim
Setup (30-60s): Why this matters, what viewer will learn
Body (60-80% of video): 3-7 main points, each with evidence
Payoff (conclusion): Key insight, surprising revelation
CTA (final 30s): Subscribe, watch next video, comment
```

**AI script workflow:**
1. Research topic with Perplexity (gather 5-10 sources)
2. Create outline: Hook + 5 main points + conclusion
3. Prompt Claude with outline, tone guidelines, and target length
4. Edit output for human voice (remove AI patterns)
5. Time check: 1,500 words = ~10 minutes

**Script prompt template:**
```
Write a YouTube script about [TOPIC].

Structure:
- Hook that creates curiosity in first 15 seconds
- 5 main points with specific examples and data
- Smooth transitions between sections
- Conclusion that ties back to hook
- Call to action

Tone: [Conversational/Authoritative/Entertaining]
Length: [1500/2000/2500] words
Include: Specific numbers, surprising facts, counterintuitive insights
Avoid: AI vocabulary (delve, journey, landscape), generic claims
```

---

### Phase 2: Voiceover Production

**AI Voiceover Tools:**

| Tool | Cost | Quality | Best For |
|------|------|---------|----------|
| ElevenLabs | $5-22/mo | HIGHEST | Any niche, most natural |
| Play.ht | $30/mo | HIGH | Professional corporate tone |
| Murf.ai | $23/mo | HIGH | Multiple voice variety |
| Amazon Polly | Pay-per-use | MEDIUM | Budget/high volume |
| Google Cloud TTS | Pay-per-use | MEDIUM | Budget alternative |

**ElevenLabs settings for natural sound:**
- Stability: 50-70% (lower = more expressive)
- Clarity: 70-85%
- Style exaggeration: 0-30% (niche dependent)
- Speaker boost: ON for voice clarity

**Human voiceover alternatives:**

| Source | Cost Per Video | Turnaround | Best For |
|--------|----------------|------------|----------|
| Fiverr | $20-100 | 2-5 days | Budget testing |
| Voices.com | $100-500 | 1-3 days | Professional quality |
| Upwork | $50-200 | 2-5 days | Ongoing relationship |

**Voiceover tips:**
- Record in 2-3 minute segments for editing flexibility
- Include pronunciation guides for complex terms
- Request raw files + processed version
- Build relationship with 2-3 reliable voice artists

---

### Phase 3: Video Editing

**Editing software by budget:**

| Budget | Tool | Cost | Learning Curve |
|--------|------|------|----------------|
| $0 | DaVinci Resolve | Free | Steep |
| $0 | CapCut Desktop | Free | Easy |
| $20/mo | Adobe Premiere Pro | $21/mo | Medium |
| $300 one-time | Final Cut Pro | $300 | Medium |

**Stock footage sources:**

| Source | Cost | License | Quality |
|--------|------|---------|---------|
| Pexels | Free | CC0 | Medium |
| Pixabay | Free | CC0 | Medium |
| Storyblocks | $20/mo | Commercial | High |
| Envato Elements | $17/mo | Commercial | High |
| Artgrid | $25/mo | Commercial | Premium |

**AI-generated footage:**
- Runway ML ($15/mo) - Generate custom clips, image-to-video
- Pika Labs (free tier) - Short generations
- Kling AI - High quality video generation
- Sora (when available) - Premium quality

**Editing workflow template:**
1. Import voiceover, create sequence
2. Add visual references at script timestamps
3. Drop in stock footage/graphics
4. Add text overlays for key points
5. Background music (subtle, 15-20% volume)
6. Color grade for consistency
7. Export: 1080p minimum, 4K preferred

---

### Phase 4: Thumbnail Creation

**Thumbnail formula:**
1. Bold text (3-4 words maximum)
2. Contrasting colors (yellow/black, red/white, blue/orange)
3. Interesting visual (face with expression, object, dramatic scene)
4. Numbers if list content ("Top 10", "$1M", "24 Hours")
5. Curiosity gap (incomplete information)

**Tools:**
- Canva Pro ($13/mo) - Templates, easy design
- Photoshop ($21/mo) - Advanced manipulation
- Figma (free) - Collaborative, component-based
- Midjourney ($10/mo) - AI background generation

**Thumbnail dimensions:** 1280x720 (16:9 ratio)

**Testing strategy:**
- Create 2-3 variants per video
- Use TubeBuddy A/B testing
- Track CTR over 48-72 hours
- Iterate on winning patterns

---

## AI Tool Stack

### Complete Production Stack

| Phase | Tool | Cost | Purpose |
|-------|------|------|---------|
| Research | Perplexity Pro | $20/mo | Topic research |
| Research | TubeBuddy | $9/mo | Keyword research |
| Scripting | Claude Pro | $20/mo | Script generation |
| Voiceover | ElevenLabs | $22/mo | AI voice |
| Stock | Storyblocks | $20/mo | B-roll footage |
| AI footage | Runway ML | $15/mo | Generated clips |
| Editing | DaVinci Resolve | Free | Video editing |
| Audio | Descript | $12/mo | Audio cleanup |
| Thumbnails | Canva Pro | $13/mo | Graphics |
| Analytics | vidIQ | $10/mo | Performance tracking |

**Total premium stack:** ~$140/month

### Budget Stack (Under $50/month)

| Phase | Tool | Cost |
|-------|------|------|
| Research | Perplexity (free tier) | $0 |
| Research | TubeBuddy (free) | $0 |
| Scripting | Claude (free tier) | $0 |
| Voiceover | ElevenLabs ($5 tier) | $5 |
| Stock | Pexels | $0 |
| Editing | DaVinci Resolve | $0 |
| Editing | CapCut | $0 |
| Thumbnails | Canva (free) | $0 |
| Analytics | TubeBuddy (free) | $0 |

**Total budget stack:** $5-20/month

### Automation Stack

| Task | Tool | Cost | Automation Level |
|------|------|------|------------------|
| Clip generation | Opus Clip Pro | $29/mo | 90% |
| Scheduling | Buffer/Hootsuite | $0-99/mo | 100% |
| Repurposing | Descript | $12/mo | 70% |
| Captions | CapCut | $0 | 95% |
| Thumbnails | Canva templates | $13/mo | 60% |
| Cross-posting | Zapier | $20/mo | 100% |

---

## YouTube Shorts Strategy

### Shorts Monetization Requirements

- 1,000 subscribers
- 10 million Shorts views in 90 days
- OR 4,000 watch hours (long-form)

### Shorts RPM Reality (Jan 2026 Data)

| Platform | RPM Range | Notes |
|----------|-----------|-------|
| YouTube Shorts | $0.40-1.50 | Most reliable |
| TikTok | Declining/unreliable | Use for testing only |
| Facebook Reels | $1-5 | Highest for some niches |
| Instagram Reels | $0.50-2 | Good for brand building |

**Strategy:** Post same short-form content to all platforms. Track RPM by platform by niche. Double down on highest-paying platform.

### Shorts Production Workflow

**From long-form:**
1. Upload to Opus Clip Pro ($29/mo)
2. AI identifies viral moments (virality score 0-100)
3. Auto-generates 5-10 clips per video
4. Add captions (CapCut style)
5. Auto-post to YouTube Shorts, TikTok, Reels

**Native Shorts:**
1. Hook in first second (no intro)
2. 30-58 seconds optimal length
3. Vertical format (9:16)
4. Bold text overlays
5. Trending audio optional (original audio often better in 2026)

### Shorts to Long-form Funnel

1. Post 3-5 Shorts daily
2. Track which topics perform best
3. Expand winning Shorts into 8-15 min long-form
4. End card: "Full video on this topic"
5. Cross-pollinate audiences

---

## Monetization Timeline

### YouTube Partner Program Requirements

- 1,000 subscribers
- 4,000 watch hours in past 12 months
- OR 10 million Shorts views in 90 days

### Timeline to Monetization

| Niche | Time to YPP | Time to $1K/mo | Required Subs |
|-------|-------------|----------------|---------------|
| Finance | 4-8 months | 4-8 months | 20K-50K |
| Tech | 6-10 months | 6-10 months | 30K-75K |
| Educational | 6-12 months | 6-12 months | 40K-100K |
| Compilation | 8-14 months | 8-14 months | 75K-150K |
| Top 10 | 8-12 months | 8-12 months | 50K-100K |
| Relaxation | 12-18 months | 12-18 months | 100K-200K |
| True crime | 4-8 months | 6-10 months | 30K-75K |

### Triple Monetization Model

**Never rely on AdSense alone.** Best channels stack three revenue streams:

1. **Primary: YouTube AdSense**
   - Baseline revenue
   - Scales with views
   - CPM varies by niche

2. **Secondary: Affiliate Links**
   - Add 2-3 relevant links per video description
   - Pin comment with top recommendation
   - Amazon Associates (1-10%)
   - Niche programs (5-30%)

3. **Tertiary: Digital Product**
   - Simple product: $7-27 price point
   - Templates, checklists, mini-courses
   - Mentioned in video, linked in description

**Example for meditation channel:**
- AdSense: $2,000/mo at 100K subs
- Affiliate (sleep products, apps): $500/mo
- Digital product (guided meditation pack $17): $1,000/mo
- **Total: $3,500/mo vs $2,000 AdSense-only**

### Sponsorship Rates

| Subscribers | Integration (30-60s) | Dedicated Video |
|-------------|----------------------|-----------------|
| 10K-50K | $100-500 | $500-2,000 |
| 50K-100K | $500-1,500 | $2,000-5,000 |
| 100K-500K | $1,500-5,000 | $5,000-20,000 |
| 500K-1M | $5,000-15,000 | $20,000-50,000 |

**Getting sponsors:**
1. Join platforms: Grin, AspireIQ, Collabstr
2. Add "Business inquiries" to channel About
3. Create media kit with demographics and metrics
4. Reach out to brands already mentioned in videos
5. Response rate improves dramatically above 50K subs

---

## Outsourcing Guide

### Phase 1: Solo (0-10K subs)

Do everything yourself to:
- Learn every part of the process
- Build SOPs as you work
- Identify bottlenecks
- Understand what quality looks like

**Time investment:** 15-20 hours/week

### Phase 2: First Hire (10K-50K subs)

**Option A: Video Editor**
- Cost: $15-25/hour or $500-1,000/mo full-time
- Source: Upwork, OnlineJobs.ph
- Saves: 10-15 hours/week

**Option B: Research VA**
- Cost: $5-10/hour or $300-600/mo
- Source: OnlineJobs.ph, Fiverr
- Saves: 5-10 hours/week

**SOP requirements:**
- Style guide with example videos
- Step-by-step editing workflow
- Quality checklist
- Feedback process

### Phase 3: Small Team (50K-100K subs)

| Role | Cost/mo | Hours/week | Responsibility |
|------|---------|------------|----------------|
| Full-time editor | $1,000-2,000 | 40 | Editing, thumbnails |
| Part-time researcher | $300-600 | 15-20 | Script research |
| Thumbnail designer | $200-400 | Per-project | Thumbnail variants |

**You focus on:** Scripts, quality control, strategy

### Phase 4: Full Operation (100K+ subs)

| Role | Cost/mo | Responsibility |
|------|---------|----------------|
| Dedicated editor (per channel) | $1,500-3,000 | Full production |
| Research team lead | $800-1,500 | Script outlines |
| Thumbnail specialist | $500-1,000 | All thumbnails |
| Analytics manager | $500-1,000 | Performance tracking |

**You focus on:** Strategy, growth, new channels

### Where to Hire

| Platform | Best For | Cost Level |
|----------|----------|------------|
| Upwork | General talent, editors | Medium |
| OnlineJobs.ph | Filipino VAs, best value | Low |
| Fiverr | Project-based, testing | Low-Medium |
| Contra | Freelance specialists | Medium-High |
| Belay | Executive assistants | High |

### Hiring Process

1. **Post job with specific requirements**
   - Include example videos
   - Specify turnaround time
   - State pay rate upfront

2. **Test with paid trial**
   - 1-2 videos before commitment
   - Pay fair rate for trial
   - Evaluate against checklist

3. **Onboard with documentation**
   - Loom walkthrough of process
   - Written SOP
   - Style guide with examples
   - Regular check-in schedule

4. **Scale with systems**
   - Notion/Asana for project management
   - Slack for communication
   - Loom for feedback
   - Monthly performance reviews

---

## Multi-Channel Portfolio Strategy

### Why Multiple Channels

- Diversifies algorithm risk
- Tests different niches
- Compounds learning
- Multiple income streams
- Exit value multiplication

### Recommended Portfolio

| Channel | Purpose | Time Investment |
|---------|---------|-----------------|
| High CPM (finance/tech) | Revenue maximization | 30% |
| High automation (relaxation) | Passive income | 20% |
| Fast production (lists) | Volume, testing | 30% |
| Passion project | Creative satisfaction | 20% |

### Portfolio Revenue Targets

| Month | Channels | Combined Revenue |
|-------|----------|------------------|
| 6 | 2 | $500-1,500 |
| 12 | 3-4 | $2,000-5,000 |
| 18 | 5-6 | $5,000-15,000 |
| 24 | 6-10 | $10,000-30,000 |

### Exit Strategy

YouTube channels sell for 2-4x annual revenue:
- $5K/mo channel = $120-240K sale price
- Portfolio of 5 channels at $3K each = $15K/mo = $360-720K exit

**Where to sell:**
- Empire Flippers (larger channels)
- Flippa (smaller channels)
- FE International (premium)
- Private sales (best multiples)

---

## Platform Comparison (Jan 2026)

### Revenue per Platform

| Platform | RPM/CPM Range | Reliability | Best Strategy |
|----------|---------------|-------------|---------------|
| YouTube Long-form | $4-30 CPM | HIGH | Primary revenue |
| YouTube Shorts | $0.40-1.50 RPM | HIGH | Volume + funnel |
| Facebook Reels | $1-5 RPM | MEDIUM | Test for niche fit |
| Instagram Reels | $0.50-2 RPM | MEDIUM | Brand building |
| TikTok | Declining/unstable | LOW | Traffic source only |

### Multi-Platform Strategy

**Post same content, track RPM per platform:**

1. Create video once
2. Export in all formats (16:9, 9:16)
3. Post to YouTube (long + Shorts), Facebook, Instagram, TikTok
4. Track RPM/CPM by platform for YOUR niche
5. Double down on highest-paying platforms
6. Use low-paying platforms for audience building only

**Content multiplication formula:**
1 long-form video becomes:
- 5-10 YouTube Shorts
- 5-10 TikToks
- 5-10 Instagram Reels
- 5-10 Facebook Reels
- 10 text posts (Twitter/X, LinkedIn)
- 10 quote cards (Instagram feed)

**Total: 1 video = 50+ pieces of content**

---

## Quick Start Checklist

### Week 1: Setup

- [ ] Choose primary niche from matrix above
- [ ] Create YouTube channel with optimized branding
- [ ] Set up AI tool stack (ElevenLabs, Perplexity, Claude)
- [ ] Create thumbnail templates in Canva
- [ ] Source 100+ stock clips for your niche

### Week 2: First Videos

- [ ] Research and script 3 videos
- [ ] Produce first video (full workflow)
- [ ] Create 3 thumbnail variants
- [ ] Upload and optimize metadata
- [ ] Extract 5+ Shorts from first video

### Week 3-4: Consistency

- [ ] Upload 2-3 long-form videos
- [ ] Post 3-5 Shorts daily
- [ ] Analyze performance data
- [ ] Iterate on thumbnails and hooks
- [ ] Document SOPs for outsourcing

### Month 2-3: Scale

- [ ] Increase to 2-3 videos per week
- [ ] Hire first VA or editor
- [ ] Launch second channel (different niche)
- [ ] Add affiliate links to all videos
- [ ] Create simple digital product

### Month 4-6: Optimize

- [ ] A/B test thumbnails systematically
- [ ] Optimize for watch time (retention analysis)
- [ ] Build sponsorship relationships
- [ ] Expand team as revenue allows
- [ ] Launch third channel

---

## Key Success Factors

1. **Consistency** - Upload on schedule, no exceptions
2. **Quality** - Better than 80% of competitors
3. **SEO** - Titles and descriptions optimized for search
4. **Thumbnails** - High CTR is the growth lever
5. **Retention** - Hook in first 30 seconds or die
6. **Patience** - Most channels take 6-12 months to monetize
7. **Diversification** - Multiple channels, multiple revenue streams

---

## Common Mistakes to Avoid

1. Inconsistent upload schedule
2. No niche focus (too broad)
3. Poor audio quality (viewers tolerate bad video, not bad audio)
4. Generic thumbnails that don't stand out
5. No SEO optimization (titles, descriptions, tags)
6. Giving up before 6 months
7. Copying exact videos (copyright issues)
8. No differentiation from competitors
9. Relying on AdSense alone
10. Not building email list from day 1

---

## Resources

### Related Files
- `MONEY_METHODS/CONTENT_FARM/FACELESS_YOUTUBE_GUIDE.md` - Detailed niche breakdowns
- `MONEY_METHODS/CONTENT_FARM/WINNING_FORMATS_RESEARCH.md` - Content format analysis
- `LEDGER/CONTENT_FARM_ALPHA_2026-01-24.csv` - Latest platform research

### External Resources
- TubeBuddy: Keyword research, A/B testing
- vidIQ: Analytics, trending topics
- Social Blade: Competitor analysis
- Opus Clip: Automated clip generation

---

**Last updated:** 2026-01-25
