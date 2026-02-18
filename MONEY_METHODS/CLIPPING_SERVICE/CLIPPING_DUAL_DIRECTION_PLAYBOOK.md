# Clipping: dual-direction playbook

**Method ID:** MM071 CLIPPING_SERVICE
**Revenue potential:** $2K-$50K/mo (service) + $5K-$54K/mo (clipper army distribution)
**Capital required:** $0-$500 to start
**Time to first dollar:** 3-7 days (service), 14-21 days (clipper army)

this is not one method. it's three.

1. **clip for others** = service revenue. you're the clipper. $25-150/clip.
2. **recruit clippers for your content** = scale distribution. you're the publisher. 50/50 rev share.
3. **clip-to-product pipeline** = turn clips into products. compilations, carousels, course promos, TikTok Shop demos.

most people only think about #2. you run all three simultaneously.

---

## existing infrastructure (already built)

before building anything new, here's what already exists in this codebase:

| asset | location | status |
|-------|----------|--------|
| auto_clip_pipeline.py | `AUTOMATIONS/auto_clip_pipeline.py` | PRODUCTION READY. 434 lines. yt-dlp + whisper + claude + ffmpeg. |
| clip_post_scheduler.py | `AUTOMATIONS/clip_post_scheduler.py` | PRODUCTION READY. 278 lines. optimal timing per platform. |
| install script | `AUTOMATIONS/install_clip_pipeline.sh` | READY. auto-installs all deps. |
| synergy playbook (SYN352) | `MONEY_METHODS/SYNERGY_PACKAGES/SYN352_CLIPPER_TIKTOK_DOUBLE_MONETIZATION.md` | 355 lines. full clipper network economics for TikTok Rewards + Shop double monetization. |
| clipper app portfolio | `MONEY_METHODS/SYNERGY_PACKAGES/SYNERGY_PACKAGE_CLIPPER_APP_PORTFOLIO.md` | 500-clipper model for app launches. |
| pipeline docs | `AUTOMATIONS/CLIP_PIPELINE_*.md` | 5 doc files, 1,500+ lines of documentation. |
| example files | `AUTOMATIONS/example_accounts.json`, `example_urls.txt` | templates ready. |

**the pipeline is built. now we monetize it in both directions.**

---

## DIRECTION 1: clip for others (service revenue)

### the play

you have a production-ready automated clip pipeline that turns a 2-hour video into 10-15 vertical clips with burned-in captions in under 20 minutes of actual work (rest is compute time). most freelancers charge $25-50/clip and spend 30-60 minutes MANUALLY editing each one.

your cost per clip: ~$0.01 in API calls + 2 minutes of QA review.
their cost per clip: 30-60 minutes of labor.
your margin: 95%+.

### pricing

| package | price | what they get | your time | your cost |
|---------|-------|---------------|-----------|-----------|
| basic | $25/clip | vertical crop, auto captions, 15-60s | 2 min QA | ~$0.01 |
| pro | $50/clip | + custom hooks, music, 3 caption styles | 10 min | ~$0.01 |
| bundle 5 | $150 ($30/clip) | 5 pro clips from one video | 30 min total | ~$0.05 |
| bundle 10 | $250 ($25/clip) | 10 pro clips from one video | 45 min total | ~$0.10 |
| monthly retainer | $500-2K/mo | 20-80 clips/month, priority queue | 2-8 hrs/mo | ~$1 |

**at $500/mo retainer with 4 clients:** $2K/mo for ~12 hours work. $166/hr effective rate.

**at $2K/mo retainer with 5 clients:** $10K/mo for ~40 hours work. $250/hr effective rate.

### target clients

ranked by willingness to pay and deal size:

1. **podcasters with 10K-100K audience** - they have content, no clips. they know clips drive discovery. sweet spot.
2. **course creators** - sitting on 50+ hours of video content. clips = student acquisition.
3. **coaches/consultants** - charge $5K+/client. $500/mo for clips is nothing.
4. **youtubers (50K-500K subs)** - too big to clip themselves, too small for a full-time editor.
5. **streamers (twitch/kick)** - 4-8 hour VODs daily. goldmine of clip-worthy moments.
6. **real estate agents** - video tours into property highlight reels.
7. **fitness trainers** - workout tutorials into 60s clips for reels/tiktok.

### client acquisition (the proof-first method)

do NOT cold DM saying "I can make clips for you." everyone says that.

**step 1: pick 5 creators.** find youtubers/podcasters with 10K-100K subs who don't post shorts/reels.

**step 2: clip their content for free.** run `auto_clip_pipeline.py` on their latest video. takes 20 minutes.

```bash
python3 AUTOMATIONS/auto_clip_pipeline.py \
  --url "https://youtube.com/watch?v=THEIR_VIDEO" \
  --max-clips 5 \
  --output clips/portfolio/CLIENT_NAME/
```

**step 3: DM with the finished clips.**

> hey [name], been watching your stuff. clipped 5 moments from your latest episode. they're ready to post on tiktok/reels.
>
> [link to unlisted google drive folder with 5 clips]
>
> no strings. if you want more, I do this full-time. $30/clip or $500/mo unlimited.

**conversion rate on proof-first outreach:** 15-25% (vs 1-3% for generic cold DMs).

**step 4: get reviews.** first 3 clients: offer 50% off for 30 days in exchange for a Fiverr review + testimonial.

### fiverr gig (see FIVERR_GIG_LISTING.md)

full listing copy is in `MONEY_METHODS/CLIPPING_SERVICE/FIVERR_GIG_LISTING.md`. optimized for fiverr search.

### upwork proposal template

> Hi [name],
>
> I clip long-form content into vertical short-form for [platform]. My pipeline:
>
> 1. AI-powered moment detection (finds the "wait what?" moments, not random 30s chunks)
> 2. Vertical crop with burned-in captions (styled, not default subs)
> 3. Hook optimization (first 3 seconds tested across formats)
>
> Recent results:
> - [Creator X]: clips averaged 45K views on TikTok (parent video had 8K views on YouTube)
> - [Creator Y]: 3 clips hit 100K+ in first week
>
> I deliver 5-10 clips per video within 48 hours. $30/clip or $500/mo retainer for unlimited clips.
>
> Happy to do a free test clip from your latest video as proof of quality.
>
> [name]

### direct outreach (youtube comment scraping)

find creators who should be clipping but aren't:

1. go to youtube. search "[your niche] podcast" or "[niche] interview"
2. filter by upload date (last month), view count (10K-500K)
3. check if they have shorts. most don't.
4. check their tiktok/instagram. if empty or dead = perfect prospect.
5. clip one video, DM on twitter/instagram with the finished product.

**target: 5 outreach messages per day.** 25/week. at 15% conversion = 3-4 new clients/week.

### scaling to agency model

once you hit 20+ clients:

1. **hire clippers at $5/clip** on Fiverr/Upwork (Philippines, Eastern Europe). your pipeline handles the hard part (moment detection, transcription). they handle manual polish (music selection, thumbnail, platform-specific tweaks).
2. **charge $25-50/clip.** margin: $20-45/clip.
3. **at 100 clips/week:** $2K-4.5K/week revenue, $500-1K/week cost = **$6K-14K/mo profit.**
4. **QA review:** you review 20% randomly. reject anything below 7/10 quality.

---

## DIRECTION 2: recruit clippers for our content (scale distribution)

### the play

you publish long-form content (youtube, podcasts, streams). you recruit 5-50 clippers to cut your content and post on THEIR accounts. they earn money from creator funds + affiliate commissions. you get distribution across 5-50 accounts simultaneously.

this is how MrBeast, Clavicular, and every serious creator scales. 500 clippers = 500 simultaneous A/B tests of your content across the algorithm.

### revenue share models

| model | split | best for | risk |
|-------|-------|----------|------|
| flat rate | $1/1K views | high-volume content | you pay regardless of revenue |
| rev share | 50/50 on all revenue | partnership feel | clippers want upside |
| hybrid | $0.50/1K + 25% rev share | balanced | moderate for both sides |
| performance bonus | base + 2x if >50K, 3x if >100K | incentivizes viral | unpredictable costs |

**recommended: hybrid model.** $0.50/1K views base + 25% of any affiliate/shop revenue the clip generates.

### recruitment channels

1. **r/forhire** - post job listing (see CLIPPER_RECRUITMENT.md)
2. **fiverr buyer requests** - post a request for "TikTok clip editors"
3. **twitter/X** - post: "looking for 5 clippers. $1/1K views. DM portfolio." tag #clippingjobs #tiktokjobs
4. **upwork** - post job: "ongoing TikTok clip editor, performance-based pay"
5. **discord communities** - Creator Clips Community (SRC132 in LEDGER)
6. **whop** - create free community, recruit from within
7. **telegram** - clipper group chat for announcements + coordination
8. **direct DM** - find small TikTok creators (1K-10K followers) who clip other people's content. offer them your content instead.

### clipper army structure

**minimum viable army: 5 clippers across 5 niches.**

| clipper # | niche | content source | clips/week | platform |
|-----------|-------|----------------|------------|----------|
| 1 | tech/building | @PRINTMAXXER content | 3-5 | TikTok |
| 2 | faith | PrayerLock content, sermons | 3-5 | YouTube Shorts |
| 3 | fitness | workout content, WalkToUnlock | 3-5 | Instagram Reels |
| 4 | finance/hustle | podcast clips, alpha drops | 3-5 | TikTok + Twitter |
| 5 | gaming/memes | stream highlights, compilations | 3-5 | TikTok + YouTube Shorts |

**what we provide each clipper:**
- source content (raw video files or youtube links)
- brand guidelines (fonts, colors, caption style)
- hook templates (5-10 proven hooks per niche)
- posting account credentials OR they post on their own account
- content brief with suggested timestamps (from auto_clip_pipeline.py viral moment detection)

**what they provide:**
- edited clips (vertical, captioned, hooked)
- posting on schedule
- engagement in first 30 minutes (comment replies, respond to duets)
- weekly performance report (views, likes, comments, shares)

### clipper performance tracking

| metric | minimum threshold | good | great |
|--------|-------------------|------|-------|
| clips delivered/week | 3 | 5 | 8+ |
| avg views/clip | 5K | 20K | 50K+ |
| engagement rate | 3% | 6% | 10%+ |
| completion rate (assigned vs delivered) | 80% | 90% | 100% |
| revenue generated/month | $50 | $200 | $500+ |

**cut bottom 20% monthly.** replace with new recruits. keep top performers. give top 3 clippers bonus + first access to new content.

### revenue per clipper

conservative estimate at hybrid rate ($0.50/1K + 25% rev share):

- clipper posts 4 clips/week = 16/month
- average 20K views/clip = 320K views/month
- TikTok Rewards: 320K x $0.002 = $640
- affiliate commissions: $100 (if product links in bio)
- total revenue: $740/month
- clipper payment: (320K/1K x $0.50) + (25% x $740) = $160 + $185 = $345
- **your net per clipper: $395/month**

**at 10 clippers: ~$3,950/month**
**at 50 clippers: ~$19,750/month**

### using auto_clip_pipeline.py for clipper briefs

run the pipeline on your source content first. the viral moment detection gives you timestamps and viral scores. send these to clippers as starting points:

```bash
# generate content briefs for clippers
python3 AUTOMATIONS/auto_clip_pipeline.py \
  --url "https://youtube.com/watch?v=YOUR_VIDEO" \
  --max-clips 20 \
  --output clips/briefs/

# the clips_metadata.csv now has timestamps, viral scores, and suggested captions
# send relevant rows to each clipper as their assignment
```

the clipper gets: "clip from 4:32 to 5:15, viral score 9/10, suggested hook: 'nobody talks about this part...', transcript snippet included."

they add their editing style, music, and post. you skip the worst part (finding the moments). they skip the worst part (watching the full video).

---

## DIRECTION 3: clip-to-product pipeline (content to products)

### clip compilation -> youtube -> AdSense

take your best-performing clips (by views). compile 10-15 into a themed 10-minute youtube video. titles like "most viral [niche] moments of the month" or "best [topic] clips compilation."

- 10-minute video = mid-roll ads eligible
- compilation channels make $2-8 RPM
- at 100K views/month: $200-800/month passive AdSense
- cost: 30 minutes to compile with ffmpeg

```bash
# simple compilation with ffmpeg (concatenate top clips)
ffmpeg -f concat -safe 0 -i clips_list.txt -c copy compilation_feb2026.mp4
```

### best clips -> carousel posts -> instagram growth

take the transcript from your best clips. turn each into a 10-slide carousel:

- slide 1: hook (the clip's best quote as text)
- slides 2-8: key points from transcript
- slide 9: summary
- slide 10: CTA (follow for more, link in bio)

carousels get 1.4x more reach than single images on instagram. they get saved and shared more.

**cost:** $0 if you use canva free tier. 15 minutes per carousel.

### clips with product demos -> TikTok Shop

if the clip shows a product (fitness gear, tech gadget, skincare): add TikTok Shop affiliate tag.

per SYN352 economics:
- $7.40/1K views (TikTok Rewards + Shop combined)
- vs $0.30-1/1K from creator fund alone
- 7-25x revenue multiplier per video

**product selection:** see `MONEY_METHODS/SYNERGY_PACKAGES/SYN352_CLIPPER_TIKTOK_DOUBLE_MONETIZATION.md` for the top 20 products list with commission rates.

### tutorial clips -> course promos -> gumroad/whop sales

if you clip educational content:

1. best clip becomes the "free sample" on TikTok/Reels
2. caption: "full breakdown in the course. link in bio."
3. bio links to Whop/Gumroad product page
4. conversion rate on education clips: 0.5-2% of viewers click, 3-8% of clicks buy

at 50K views on a tutorial clip:
- 50K x 1% click = 500 clicks
- 500 x 5% conversion = 25 sales
- 25 x $27 product = $675 from one clip

### the full clip-to-revenue map

```
source video (1-2 hours)
  |
  |-- auto_clip_pipeline.py --> 10-15 clips
  |     |
  |     |-- post on TikTok --> TikTok Rewards ($0.40-6/1K views)
  |     |-- post on YouTube Shorts --> Shorts ad revenue
  |     |-- post on Instagram Reels --> Reels bonus program
  |     |-- post on Twitter/X --> engagement + follower growth
  |     |
  |     |-- add TikTok Shop tag --> affiliate commissions ($5-7/1K views)
  |     |-- add amazon affiliate link in bio --> commission per sale
  |     |
  |     |-- best clips --> carousel posts --> instagram growth
  |     |-- best clips --> youtube compilation --> AdSense
  |     |-- tutorial clips --> course CTA --> Whop/Gumroad sales
  |     |-- behind-the-scenes clips --> newsletter CTA --> Beehiiv subs
  |     |
  |     |-- send to clipper army --> 5-50 accounts amplify
  |     |
  |     |-- sell clipping as service --> $25-150/clip
```

every single source video generates revenue from 5-10 streams. that's the dual-direction model.

---

## week 1 execution plan

### day 1 (2 hours)
- [ ] run `./AUTOMATIONS/install_clip_pipeline.sh` to verify all deps
- [ ] test pipeline: `python3 AUTOMATIONS/auto_clip_pipeline.py --demo`
- [ ] process 1 test video from your own content
- [ ] review output quality in `clips/clips/`

### day 2 (3 hours)
- [ ] find 5 creators who don't clip (youtube search, check their tiktok)
- [ ] run pipeline on their latest videos (5 videos, 5 clips each = 25 clips)
- [ ] upload to google drive folders (1 per creator)
- [ ] DM each creator with proof-first pitch

### day 3 (2 hours)
- [ ] post Fiverr gig (see FIVERR_GIG_LISTING.md)
- [ ] post Upwork profile with clipping as core service
- [ ] post on r/forhire offering clipping service
- [ ] post on twitter: portfolio + pricing

### day 4 (2 hours)
- [ ] post clipper recruitment ad on r/forhire (see CLIPPER_RECRUITMENT.md)
- [ ] DM 10 small TikTok creators offering clipper deal
- [ ] set up telegram group for clipper coordination
- [ ] create content brief template in notion/google docs

### day 5-7 (ongoing)
- [ ] follow up with 5 proof-first prospects
- [ ] onboard first 2-3 clippers with test assignments
- [ ] deliver first paid client clips
- [ ] track everything in LEDGER

---

## financial tracking

all clipping revenue tracks to:
- `FINANCIALS/REVENUE_TRACKER.csv` (service revenue + clipper army revenue)
- `FINANCIALS/EXPENSE_TRACKER.csv` (clipper payments, tool costs)

**cost breakdown:**
- Anthropic API: ~$0.01/video (viral moment detection)
- yt-dlp: free
- ffmpeg: free
- whisper: free (local)
- fiverr fees: 20% of service revenue
- clipper payments: $0.50-1/1K views

**break-even:** 1 client at $500/mo covers 6+ months of API costs.

---

## cross-references

| related file | what it covers |
|-------------|----------------|
| `AUTOMATIONS/auto_clip_pipeline.py` | the actual pipeline code (434 lines) |
| `AUTOMATIONS/clip_post_scheduler.py` | posting schedule generator (278 lines) |
| `AUTOMATIONS/CLIP_PIPELINE_QUICKSTART.md` | 5-minute setup |
| `MONEY_METHODS/SYNERGY_PACKAGES/SYN352_CLIPPER_TIKTOK_DOUBLE_MONETIZATION.md` | TikTok Rewards + Shop double monetization (355 lines) |
| `MONEY_METHODS/SYNERGY_PACKAGES/SYNERGY_PACKAGE_CLIPPER_APP_PORTFOLIO.md` | 500-clipper model for app launches |
| `MONEY_METHODS/CLIPPING_SERVICE/FIVERR_GIG_LISTING.md` | exact fiverr listing copy |
| `MONEY_METHODS/CLIPPING_SERVICE/CLIPPER_RECRUITMENT.md` | job posting + contract + onboarding |

---

## the bottom line

manual clipping: 30-60 minutes per clip. $25-50 revenue.
automated clipping: 2 minutes QA per clip. $25-50 revenue. 95% margin.

selling clips as a service = immediate revenue from day 3.
recruiting clippers = distribution at scale from week 3.
clip-to-product = compound revenue from every piece of content.

run all three. the pipeline is built. go.
