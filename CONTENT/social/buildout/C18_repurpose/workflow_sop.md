# C18 Viral Content Repurposer, Workflow SOP
# One Piece of Content → 10 Platforms

## The Math

1 original piece → 10 distribution points
- 3 long-form posts (YouTube video, newsletter issue, blog article)
- 4 short-form clips (TikTok, IG Reels, YouTube Shorts, FB Reels)
- 2 static posts (X/Twitter thread, LinkedIn post)
- 1 audio (podcast episode or voiceover clip)

Cost to create: 2-4 hours
Cost to distribute: 45 minutes
Effective cost per platform: 17 minutes

---

## Source Content Hierarchy (what to repurpose first)

| Tier | Source | Repurpose Potential | Time to Process |
|------|--------|--------------------|--------------------|
| S | YouTube long-form (8-15 min) | Highest, video, clips, audio, transcript | 90 min |
| A | Podcast episode (20-30 min) | High, audio, transcript, clips, blog | 75 min |
| B | Twitter thread (10+ tweets) | Medium, carousel, blog, short video | 45 min |
| C | Newsletter issue (800-1,200 words) | Medium, blog, thread, carousel, audio | 45 min |
| D | Short-form clip (60 sec) | Low, crosspost only, no derivatives | 15 min |

---

## Master Workflow: YouTube Video → 10 Platforms

### Step 0: Pre-production (do before filming)
- Write transcript first (Claude prompt: "Write a 10-minute video script on [topic] for a faceless YouTube channel targeting solopreneurs. Structure: Hook 0-30s, Problem 30-90s, Solution 2-7min, CTA 7-10min.")
- From transcript, extract: thread hook, newsletter intro, 5 clip timestamps
- Record video with transcript in hand, clean, natural pacing

### Step 1: Upload source (5 min)
1. Export video at 1920x1080, H.264, AAC audio
2. Upload raw to Google Drive / CapCut web
3. Generate AI transcript (YouTube auto-captions or Descript)
4. Save transcript as .txt in content library

### Step 2: Clip extraction (20 min)
Cut 4-6 clips from the long-form:
- Clip 1: Hook moment (0:15–0:45), highest-energy 30 seconds
- Clip 2: Core insight reveal, 45-60 seconds
- Clip 3: Step-by-step snippet, 45 seconds
- Clip 4: Proof point or result, 30 seconds
- Clip 5 (optional): Contrarian take, 30 seconds
- Clip 6 (optional): CTA clip, 20 seconds

Tool: CapCut (free, batch export), OpusClip ($29/mo auto-clips), or manual Descript

### Step 3: Format clips per platform (15 min)
In CapCut:
- Export each clip at 9:16 (1080x1920) for TikTok, IG Reels, YouTube Shorts, FB Reels
- Add captions (CapCut auto-caption, style: bold white text, black outline)
- Remove watermark: export at 1080p, re-import, burn captions

### Step 4: Long-form YouTube upload (10 min)
- Title formula: [Number] [Outcome] (No [Common Belief]) | e.g., "7 Side Hustles That Actually Pay in 2025 (No Experience Needed)"
- Description: 150-word summary + timestamps + 5 affiliate links + subscribe CTA
- Tags: 10-15 tags (main keyword + variants + channel topic)
- Thumbnail: bright background, bold text overlay, emotional face/graphic
- Schedule: Tuesday or Thursday, 2pm EST

### Step 5: Short-form uploads (10 min)
Upload all 4 clips to each platform simultaneously:
- TikTok: paste caption from clipboard, add 3-5 hashtags, schedule 9pm EST
- IG Reels: paste caption, add location tag, schedule 11am EST
- YouTube Shorts: add #Shorts to title, paste description
- FB Reels: crosspost from IG (Meta Business Suite, 1 click)

### Step 6: Blog/SEO article (15 min)
Prompt: "Convert this transcript into a 1,500-word SEO article targeting the keyword [keyword]. Add H2 headers every 300 words, include a comparison table, add affiliate links for [tool list]. Maintain human, direct tone."
- Publish on own site or Medium
- Add internal links to 3 other articles
- Include email opt-in CTA in conclusion

### Step 7: Newsletter issue (10 min)
Prompt: "Convert this transcript into a 900-word newsletter issue. Lead with the most interesting insight. Include 1 tool recommendation with affiliate link. End with 1 actionable takeaway. No fluff."
- Upload to Beehiiv as draft
- Add sponsor placement (if applicable)
- Schedule for Tuesday 8am

### Step 8: Twitter/X thread (5 min)
Prompt: "Convert this into a 7-tweet thread. Tweet 1: consequence-first hook with specific number. Tweets 2-6: one insight per tweet, no fluff. Tweet 7: CTA pointing to full video. No em dashes."
- Post Tweet 1, add remaining as thread
- Reply to Tweet 1 with thread link after 15 minutes (algorithm signal)
- Schedule 8am or 12pm EST weekdays

### Step 9: LinkedIn post (5 min)
Prompt: "Write a 200-word LinkedIn post based on this content. Open with a bold claim. Use short paragraphs (1-2 sentences). Include 1 specific number. End with a question to drive comments. Professional but direct tone."
- Post natively (no links in body, put link in comments)
- First comment: "Full video here: [link]" within 5 minutes of posting

### Step 10: Podcast episode (5 min)
Option A: Use video audio track directly
- Export audio-only from video editor
- Upload to Buzzsprout as new episode
- Add transcript as show notes
- Auto-distributes to Spotify, Apple, Google

Option B: Record 5-min condensed version as standalone episode

---

## Weekly Content Calendar (Repurpose Schedule)

| Day | Action |
|-----|--------|
| Monday | Film/write source content |
| Tuesday | YouTube long-form goes live + newsletter |
| Wednesday | TikTok clips 1 + 2 |
| Thursday | IG Reels clips 1 + 2 + LinkedIn post |
| Friday | YouTube Shorts all 4 clips |
| Saturday | Twitter thread + blog article |
| Sunday | FB Reels (auto-crosspost) + podcast episode |

---

## Podcast/Newsletter → 10 Platforms (Condensed)

Same logic, different source:
1. Podcast → transcribe via Descript or Whisper → blog article
2. Blog → extract 5 key sentences → Twitter thread
3. Twitter thread → screenshot + design → LinkedIn carousel
4. Newsletter → pull 3 best lines → 3 standalone tweets
5. Any audio → clip 60-sec soundbite → Reels/Shorts/TikTok

---

## Twitter Thread → 5 Platforms

Short-form source can still be stretched:
1. Thread → LinkedIn post (top insight)
2. Thread → carousel script (one slide per tweet)
3. Thread → YouTube Short script (read the thread as video)
4. Thread → newsletter section (expand on each tweet)
5. Thread → Reddit post (reframe as value-first post, no promotion)

---

## Content Library Structure

```
content_library/
├── originals/           # Raw source files (.mp4, .txt, .md)
├── clips/               # Cut clips ready for each platform
├── captions/            # Platform-formatted captions
├── articles/            # Blog drafts
├── newsletters/         # Newsletter drafts
├── threads/             # Twitter threads
├── linkedin/            # LinkedIn posts
└── tracker.csv          # Status per piece: source | platforms | links | dates
```

tracker.csv columns:
`piece_id, source_title, source_type, youtube_link, tiktok_link, ig_reels_link, shorts_link, fb_link, blog_link, newsletter_link, thread_link, linkedin_link, podcast_link, created_date, status`

---

## Automation Add-ons (When Stack Allows)

- **Zapier/Make:** Auto-detect new YouTube video → trigger Descript transcription → send transcript to Claude API → post outputs to Buffer queue
- **Buffer:** Schedule all platform posts 1 week ahead from dashboard
- **Repurpose.io:** Auto-crosspost TikTok → IG Reels → FB Reels → YouTube Shorts (removes watermark)
- **Notion content calendar:** Track every piece, status, links, performance

---

## Quality Checklist (Before Publishing Each Derivative)

- [ ] Platform-specific caption written (not copy-pasted from another platform)
- [ ] Correct aspect ratio for each clip
- [ ] Captions burned in (for video clips)
- [ ] Affiliate links present where relevant
- [ ] CTA directs back to primary platform (YouTube, newsletter, or DMs)
- [ ] No watermarks from TikTok on crossposted clips
- [ ] First comment posted on LinkedIn (with link)
- [ ] Tweet 1 of thread is consequence-first hook (no "Thread:" prefix)
- [ ] Blog article has internal links + email opt-in CTA
- [ ] Newsletter has clear subject line with specific number/outcome
