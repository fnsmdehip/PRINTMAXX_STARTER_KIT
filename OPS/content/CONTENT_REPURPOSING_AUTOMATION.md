# Content Repurposing Automation Guide

**Purpose:** Maximize content ROI by turning one piece into 20+ pieces across platforms with minimal manual effort.

**Core Insight:** Create once, distribute everywhere. The best creators spend 20% creating and 80% distributing.

---

## Quick Reference: Tool Matrix

| Tool | Primary Use | Price | Automation Level | Best For |
|------|-------------|-------|------------------|----------|
| **Opus Clip** | Long video to clips | $19-99/mo | Semi-auto | YouTube to TikTok/Reels |
| **Vizard** | Video repurposing | $20-60/mo | Semi-auto | Multi-platform video |
| **Repurpose.io** | Cross-posting | $25-99/mo | Full auto | Podcast distribution |
| **Descript** | Video/podcast editing | $15-44/mo | Manual | Pro editing + transcription |
| **Headliner** | Audiograms | $0-24/mo | Semi-auto | Podcast to social |
| **Typefully** | Twitter threads | $0-20/mo | Semi-auto | Blog to threads |
| **Buffer** | Scheduling | $0-120/mo | Full auto | Multi-platform posting |
| **Make.com** | Workflow automation | $0-29/mo | Full auto | Custom pipelines |
| **n8n** | Self-hosted automation | Free (hosting) | Full auto | Complex workflows |

---

## Workflow 1: Long Video to Short Clips

**Input:** YouTube/podcast video (10+ minutes)
**Output:** 5-15 vertical clips for TikTok, Reels, Shorts

```
Long Video
    |
    v
[AI Clip Detection]
    |
    +---> Opus Clip (best AI selection)
    +---> Vizard (multi-platform templates)
    +---> Descript (manual control)
    |
    v
[Auto-Format]
    |
    +---> 9:16 vertical
    +---> Captions added
    +---> Hook optimized
    |
    v
[Distribution]
    |
    +---> TikTok
    +---> Instagram Reels
    +---> YouTube Shorts
    +---> Facebook Reels
```

### Tool Comparison: AI Clipping

| Tool | AI Quality | Caption Style | Export Options | Price |
|------|------------|---------------|----------------|-------|
| **Opus Clip** | Best | Modern, viral-style | Direct to socials | $19/mo (3hrs), $99/mo (20hrs) |
| **Vizard** | Good | Clean, customizable | Multi-platform | $20/mo (5hrs), $60/mo (20hrs) |
| **Submagic** | Good | Trendy animations | Direct export | $15/mo (10 videos) |
| **Munch** | Medium | Basic | Multi-platform | $49/mo |
| **Vidyo.ai** | Medium | Basic | Download only | $15/mo |

### Opus Clip Workflow (Recommended)

1. Upload video to Opus Clip
2. AI detects 10-15 viral moments
3. Review clips (30 min for 1hr video)
4. Select 5-8 best clips
5. Apply branding template
6. Export to platforms directly

**Time:** 45 min per 1hr video
**Output:** 5-8 clips per video
**Cost:** $19-99/mo depending on volume

### Alternatives to Opus Clip

**Budget Option - CapCut (Free):**
- Manual clip selection
- Good captions and effects
- No AI selection
- Time: 2-3 hours per 1hr video

**Pro Option - Descript ($24/mo):**
- Full editing control
- AI transcription
- Filler word removal
- Time: 1-2 hours per 1hr video

**Self-Hosted Option - Whisper + FFmpeg:**
- Free (compute costs only)
- Full control
- Requires technical setup
- Best for high volume (100+ videos/mo)

---

## Workflow 2: Podcast to Multi-Format

**Input:** Podcast episode (30-60 min audio/video)
**Output:** Audiograms, blog, social posts, email, clips

```
Podcast Episode
    |
    v
[Transcription]
    |
    +---> Descript (best)
    +---> Whisper API (cheap)
    +---> Otter.ai (accurate)
    |
    v
[Content Extraction]
    |
    +---> Key quotes (5-10)
    +---> Main topics (3-5)
    +---> Full transcript
    |
    v
[Multi-Format Output]
    |
    +---> Audiograms (Headliner)
    +---> Blog post (Claude)
    +---> Twitter thread (Typefully)
    +---> LinkedIn posts (Buffer)
    +---> Newsletter (ConvertKit)
    +---> YouTube clips (Opus Clip)
```

### Headliner Audiogram Workflow

**What it does:** Creates video from audio with waveforms, captions, and graphics.

1. Upload podcast audio + transcript
2. Select quote segments (30-60 sec each)
3. Choose template (square for feed, vertical for Stories)
4. Add captions and branding
5. Export and schedule

**Settings:**
- Square (1:1) for Twitter/LinkedIn feed
- Vertical (9:16) for Stories/Reels
- Landscape (16:9) for YouTube community

**Time:** 30 min for 5-10 audiograms
**Cost:** $14/mo (15 videos) or $24/mo (unlimited)

### Podcast to Blog Pipeline

```
Transcript
    |
    v
[Claude Processing]
    |
    Prompt: "Convert this podcast transcript to a 1500-word blog post.
    Structure: Hook intro, 3-5 main sections with H2 headers,
    actionable takeaways, conclusion with CTA.
    Maintain the speaker's voice. Add formatting for readability."
    |
    v
[SEO Optimization]
    |
    +---> Add target keyword
    +---> Write meta description
    +---> Add internal links
    +---> Add FAQ section
    |
    v
[Publish]
    |
    +---> Blog (primary)
    +---> Medium (syndication)
    +---> LinkedIn article
```

**Time:** 20 min with Claude assistance
**Cost:** Claude API costs (~$0.10-0.50 per blog)

---

## Workflow 3: Blog Post to Social

**Input:** Blog post (1500+ words)
**Output:** Twitter thread, LinkedIn posts, newsletter, carousel

```
Blog Post
    |
    v
[Content Analysis]
    |
    +---> Extract main points (5-7)
    +---> Pull quotes (3-5)
    +---> Identify data/stats
    |
    v
[Format Adaptation]
    |
    +---> Twitter thread (Typefully)
    +---> LinkedIn posts (3-5 angles)
    +---> Newsletter section
    +---> Carousel slides (10)
    +---> Video script
    |
    v
[Scheduling]
    |
    +---> Week 1: Thread + LinkedIn
    +---> Week 2: Carousel + Quotes
    +---> Week 3: Video + Newsletter
```

### Typefully for Twitter Threads

**Features:**
- Thread composer with preview
- Optimal time scheduling
- Analytics
- AI rewrite suggestions

**Workflow:**
1. Paste blog key points
2. Expand each point to tweet
3. Add hook as first tweet
4. Add CTA as last tweet
5. Schedule for optimal time

**Template:**
```
Tweet 1 (Hook): [Surprising claim or question]
Tweet 2-6: [One point per tweet with example]
Tweet 7: [Summary or key takeaway]
Tweet 8 (CTA): [Engagement ask or link]
```

**Time:** 15 min per thread
**Cost:** Free or $10-20/mo for teams

### LinkedIn Post Variations

From one blog, create 5 LinkedIn posts:

1. **Story Format:** Personal angle on the topic
2. **Listicle:** "5 things I learned about X"
3. **Hot Take:** Contrarian view from the blog
4. **How-To:** Actionable steps from the blog
5. **Quote Graphic:** Key quote as image + short text

**Scheduling:** 1 post every 2-3 days over 2 weeks

---

## Workflow 4: Tweet to Expanded Content

**Input:** Viral tweet or thread (high engagement)
**Output:** TikTok video, blog post, newsletter

```
Viral Tweet
    |
    v
[Engagement Analysis]
    |
    +---> What resonated? (comments)
    +---> What questions? (replies)
    +---> What objections? (quote tweets)
    |
    v
[Content Expansion]
    |
    +---> TikTok script (30-60 sec)
    +---> Blog post (1500 words)
    +---> Newsletter deep dive
    +---> Follow-up thread
    |
    v
[Distribution]
    |
    +---> TikTok (same day)
    +---> Blog (within 48 hrs)
    +---> Newsletter (weekly)
```

### Tweet to TikTok Script Template

```
[Hook - 3 sec]
"I tweeted this and it got [X] likes..."
OR
"[Restate the tweet as hook]"

[Context - 5 sec]
"Here's what I mean..."

[Main Points - 20-40 sec]
- Point 1 with example
- Point 2 with example
- Point 3 with example

[CTA - 3 sec]
"Follow for more [topic] tips"
OR
"Comment if you [relevant question]"
```

**Time:** 10 min scripting + 15 min recording/editing
**Cost:** Free (just your time)

---

## Workflow 5: Newsletter to Social Posts

**Input:** Weekly newsletter (1000+ words)
**Output:** 10-15 social posts across platforms

```
Newsletter
    |
    v
[Content Extraction]
    |
    +---> Main insight (1 thread)
    +---> Supporting points (5 posts)
    +---> Curated links (3 posts)
    +---> Personal update (2 posts)
    +---> CTA variations (2 posts)
    |
    v
[Platform Adaptation]
    |
    +---> X: Thread + 3 standalone
    +---> LinkedIn: 4 posts
    +---> TikTok: 2 scripts
    +---> Instagram: 3 carousels
    |
    v
[2-Week Schedule]
    |
    Week 1: Launch thread + LinkedIn
    Week 2: TikTok + carousels + quotes
```

### Extraction Template (Claude Prompt)

```
From this newsletter, extract:
1. The main insight (2-3 sentences)
2. 5 supporting points (1 sentence each)
3. 3 quotable moments (under 280 chars)
4. 2 controversial/hot takes
5. 1 actionable tip
6. 3 questions to ask the audience

Format each for: Twitter, LinkedIn, TikTok script
```

---

## Automation Platforms

### n8n (Self-Hosted)

**Best for:** Complex multi-step workflows, high volume, custom integrations

**Setup:**
1. Deploy on Hetzner (5/mo) or Railway
2. Connect social platforms via OAuth
3. Build workflows with visual editor

**Example Workflow: Blog to Multi-Platform**
```
Trigger: New blog post (RSS/Webhook)
    |
    v
Step 1: Extract content via HTTP
    |
    v
Step 2: Claude API - Generate thread
    |
    v
Step 3: Claude API - Generate LinkedIn
    |
    v
Step 4: Post to X via API
    |
    v
Step 5: Post to LinkedIn via API
    |
    v
Step 6: Log to Google Sheets
```

**Estimated Cost:**
- Hosting: $5-10/mo
- Claude API: $5-20/mo
- Time: 2-4 hours initial setup

**Templates to Build:**
1. RSS to social posts
2. YouTube upload to clip queue
3. Podcast to blog pipeline
4. Tweet to newsletter digest

### Make.com (Zapier Alternative)

**Best for:** Non-technical users, quick setup, reliable triggers

**Pricing:**
- Free: 1,000 ops/mo
- Core: $9/mo (10,000 ops)
- Pro: $16/mo (10,000 ops + priority)

**Key Templates:**
1. "New YouTube Video to Social Media Posts"
2. "Podcast Episode to Blog and Social"
3. "RSS Feed to Social Distribution"
4. "Form Submission to Content Queue"

**Limitations:**
- Social posting requires third-party (Buffer/Publer)
- AI steps cost extra operations
- Rate limits on free tier

### Repurpose.io

**Best for:** Podcast/video creators who want hands-off distribution

**How it works:**
1. Connect source (YouTube, podcast host, etc.)
2. Set destination templates
3. New content auto-distributes

**Workflow Example:**
```
New YouTube Video
    |
    v
[Auto-Create]
    |
    +---> TikTok (vertical clip)
    +---> Instagram Reel
    +---> LinkedIn video
    +---> Facebook video
    +---> Twitter video
```

**Pricing:**
- Podcaster: $25/mo (1 show, 10 destinations)
- Creator: $75/mo (3 shows, unlimited destinations)
- Agency: $99/mo (unlimited)

**Limitations:**
- No AI clipping (just reformats)
- Limited customization per platform
- Best for podcast-first creators

---

## Cost Breakdown by Volume

### Low Volume (1-4 pieces/week)

| Tool | Purpose | Monthly Cost |
|------|---------|--------------|
| Opus Clip Starter | Video clipping | $19 |
| Headliner Free | Audiograms | $0 |
| Buffer Free | Scheduling | $0 |
| Typefully Free | Threads | $0 |
| **Total** | | **$19/mo** |

### Medium Volume (5-10 pieces/week)

| Tool | Purpose | Monthly Cost |
|------|---------|--------------|
| Opus Clip Pro | Video clipping | $49 |
| Headliner Basic | Audiograms | $14 |
| Buffer Essentials | Scheduling | $6 |
| Typefully Pro | Threads | $10 |
| Descript Creator | Editing | $24 |
| **Total** | | **$103/mo** |

### High Volume (10+ pieces/week)

| Tool | Purpose | Monthly Cost |
|------|---------|--------------|
| Opus Clip Unlimited | Video clipping | $99 |
| Repurpose.io Creator | Auto-distribution | $75 |
| n8n self-hosted | Custom automation | $10 |
| Claude API | Content generation | $20 |
| Buffer Team | Scheduling | $12 |
| **Total** | | **$216/mo** |

---

## Implementation Priority

### Week 1: Foundation

1. **Set up Opus Clip** - Start turning long videos into clips
2. **Set up Buffer** - Centralize scheduling
3. **Create templates** - Blog-to-social prompts for Claude

### Week 2: Automation

1. **Set up n8n or Make.com** - Build first automated workflow
2. **Connect RSS triggers** - Auto-detect new content
3. **Build distribution queue** - Google Sheets tracking

### Week 3: Scale

1. **Add Repurpose.io** - Hands-off video distribution
2. **Add Headliner** - Audiograms for podcast
3. **Refine workflows** - Optimize based on results

### Week 4: Optimize

1. **Track performance** - Which repurposed content performs best
2. **A/B test formats** - Thread vs single post, square vs vertical
3. **Document SOPs** - Repeatable processes for each workflow

---

## n8n Workflow Templates

### Template 1: Blog to X Thread

```json
{
  "name": "Blog to X Thread",
  "nodes": [
    {
      "type": "RSS Feed",
      "config": {
        "url": "[YOUR_BLOG_RSS]",
        "poll_interval": "1h"
      }
    },
    {
      "type": "HTTP Request",
      "config": {
        "method": "POST",
        "url": "https://api.anthropic.com/v1/messages",
        "headers": {
          "x-api-key": "[CLAUDE_API_KEY]"
        },
        "body": {
          "model": "claude-3-haiku-20240307",
          "max_tokens": 1024,
          "messages": [{
            "role": "user",
            "content": "Convert this blog post to a Twitter thread (7-10 tweets). First tweet should be a hook. Last tweet should be a CTA. Blog: {{$node.RSS.json.content}}"
          }]
        }
      }
    },
    {
      "type": "X (Twitter)",
      "config": {
        "operation": "createThread",
        "tweets": "{{$node.HTTP.json.content}}"
      }
    }
  ]
}
```

### Template 2: YouTube to Multi-Platform

```json
{
  "name": "YouTube to Social",
  "trigger": {
    "type": "YouTube",
    "event": "newVideo",
    "channelId": "[YOUR_CHANNEL_ID]"
  },
  "steps": [
    {
      "name": "Create Announcement",
      "type": "Claude API",
      "prompt": "Write a social media announcement for this video. Title: {{title}}. Description: {{description}}. Create: 1) Twitter post (280 chars), 2) LinkedIn post (500 chars), 3) Short hook for TikTok"
    },
    {
      "name": "Post to X",
      "type": "Twitter API",
      "content": "{{twitter_post}}"
    },
    {
      "name": "Post to LinkedIn",
      "type": "LinkedIn API",
      "content": "{{linkedin_post}}"
    },
    {
      "name": "Queue for Opus Clip",
      "type": "Google Sheets",
      "append": {
        "url": "{{video_url}}",
        "status": "pending_clips"
      }
    }
  ]
}
```

### Template 3: Podcast Episode Pipeline

```json
{
  "name": "Podcast to All Formats",
  "trigger": {
    "type": "RSS",
    "url": "[PODCAST_RSS]"
  },
  "steps": [
    {
      "name": "Download Audio",
      "type": "HTTP Download"
    },
    {
      "name": "Transcribe",
      "type": "Whisper API"
    },
    {
      "name": "Generate Blog",
      "type": "Claude API",
      "prompt": "Convert this transcript to a 1500 word blog post with SEO structure..."
    },
    {
      "name": "Generate Social",
      "type": "Claude API",
      "prompt": "Create 5 social posts from this transcript..."
    },
    {
      "name": "Publish Blog",
      "type": "WordPress/Ghost API"
    },
    {
      "name": "Schedule Social",
      "type": "Buffer API"
    }
  ]
}
```

---

## Platform-Specific Formatting

### TikTok / Reels / Shorts
- Aspect: 9:16 vertical
- Duration: 15-60 seconds (sweet spot: 30-45s)
- Captions: Required (85% watch without sound)
- Hook: First 3 seconds critical
- CTA: "Follow for more" or "Comment X"

### X (Twitter)
- Single posts: Under 280 chars
- Threads: 5-10 tweets max
- Images: 1200x675 or 1:1 square
- Video: Under 2:20, but 30-60s optimal
- Best times: 8-9am, 12-1pm, 5-6pm

### LinkedIn
- Post length: 150-300 words optimal
- Images: 1200x627 or 1080x1080
- Video: Under 10 min, 30-90s optimal
- Best times: Tue-Thu, 7-8am, 12pm, 5-6pm

### Instagram
- Feed: 1:1 (1080x1080) or 4:5 (1080x1350)
- Reels: 9:16 (1080x1920)
- Stories: 9:16 (1080x1920)
- Carousels: Up to 10 slides

---

## Metrics to Track

### Content Performance
- Views/impressions per repurposed piece
- Engagement rate by platform
- Click-through to original content
- Follower growth attribution

### Efficiency Metrics
- Time spent per piece (target: <30 min total)
- Cost per distributed piece
- Original:repurposed ratio (target: 1:10+)

### ROI Tracking
Track in `LEDGER/CONTENT_REPURPOSING_METRICS.csv`:
```csv
date,original_piece,repurposed_format,platform,views,engagement,clicks,time_spent_min,cost
```

---

## Common Pitfalls

1. **Over-automation** - Fully automated content often feels robotic. Add human touch to 1 in 5 posts.

2. **Same content everywhere** - Adapt format and tone per platform. LinkedIn is professional, TikTok is casual.

3. **Ignoring analytics** - Track what repurposed formats perform best. Double down on winners.

4. **No original content** - Repurposing amplifies original content. Still need to create 1-2 original pieces per week.

5. **Inconsistent branding** - Use templates to maintain visual consistency across platforms.

---

## Related Documents

- `OPS/ADDITIONAL_OPS_PLAYBOOK.md` - Content Multiplication Ops section
- `LEDGER/WINNING_CONTENT_STRUCTURES.csv` - Proven content formats
- `OPS/NICHE_ACCOUNT_CONTENT_CALENDAR.md` - Posting schedules
- `.claude/rules/copy-style.md` - Writing guidelines
- `MASTER_DOC/` - Original n8n setup instructions

---

Last updated: 2026-01-25
