# @clipvault_ First Week Content Strategy

**Status:** PENDING_REVIEW
**Account type:** Faceless viral clip curation
**Voice:** No personality. No humor attempts. Short neutral captions. The clip IS the content. Let it speak.
**Goal:** 2 posts/day for 7 days across X, TikTok, IG Reels, YouTube Shorts, Facebook. Test caption formats, find what drives comments.

---

## 1. Caption Templates (14 total, 2 per day)

Captions are SHORT. 2-8 words max. No emojis. No hashtags in the caption itself (those go in comments or description field). The caption is a frame that makes people watch and react.

### Day 1 (Account Launch)

**Post 1:**
```
this shouldn't work but it does
```
Use with: skill clips, unusual solutions, unexpected engineering, trick shots.

**Post 2:**
```
wait for it
```
Use with: any clip with a delayed payoff, surprise ending, slow build to climax.

### Day 2

**Post 3:**
```
he really did that
```
Use with: athletic feats, bold moves, confrontations, clutch moments.

**Post 4:**
```
no way this is real
```
Use with: optical illusions, extreme talent, unbelievable timing, nature clips.

### Day 3

**Post 5:**
```
rate this 1-10
```
Use with: food plating, art, builds, transformations, skill displays.

**Post 6:**
```
which one are you
```
Use with: comparison clips, two-person reactions, group behavior, relatable scenarios.

### Day 4

**Post 7:**
```
the precision here
```
Use with: craftwork, surgery, cooking, engineering, calligraphy, machining.

**Post 8:**
```
someone explain this
```
Use with: confusing clips, weird physics, things that look wrong, glitches in real life.

### Day 5

**Post 9:**
```
bro was not expecting that
```
Use with: pranks, surprises, animal reactions, competition upsets.

**Post 10:**
```
name this in one word
```
Use with: any high-energy or visually striking clip. Forces comments.

### Day 6

**Post 11:**
```
watch this till the end
```
Use with: longer clips (30-60s) with a payoff in the final seconds.

**Post 12:**
```
is this a W or an L
```
Use with: risky decisions, unusual choices, debatable outcomes, relationship clips.

### Day 7

**Post 13:**
```
the level of detail here
```
Use with: miniatures, woodworking, digital art, model building, cooking plating.

**Post 14:**
```
you've never seen this before
```
Use with: rare footage, unusual animals, obscure skills, niche crafts, hidden places.

---

## 2. Engagement Post Formats (7 total, 1 per day)

These are standalone engagement posts. No clip required, or use a generic satisfying/interesting clip as the background. Purpose: drive comments, saves, shares. Algorithm fuel.

### Format 1: Rate This (Day 1)
```
rate this 1-10

[clip of food plating, art, or a build]
```
Why it works: single digit response is zero friction. Everyone replies. Comment count drives reach.

### Format 2: Which One? (Day 2)
```
left or right?

[split screen clip or two options side by side]
```
Why it works: binary choice = instant opinion. People pick a side. Debates start in comments.

### Format 3: Caption This (Day 3)
```
caption this

[funny or absurd still frame / short clip with no context]
```
Why it works: turns viewers into content creators. Best captions get engagement on their own replies.

### Format 4: One Word Only (Day 4)
```
describe this in one word

[visually dense or emotionally loaded clip]
```
Why it works: forces a response. Low barrier. People scroll back up to re-watch before answering.

### Format 5: Fill in the Blank (Day 5)
```
this is the most ______ thing i've ever seen

[extreme clip - extremely satisfying, extremely chaotic, extremely precise, etc.]
```
Why it works: mad-libs format. People fill in different words. Creates variety in comments.

### Format 6: Would You? (Day 6)
```
would you try this? yes or no

[risky activity, extreme food, unusual experience]
```
Why it works: yes/no poll without needing platform poll feature. Drives debate when clip is polarizing.

### Format 7: What Happened Next (Day 7)
```
what do you think happened next?

[clip cut right before the resolution]
```
Why it works: curiosity gap. Forces people to comment their guess. If you post the follow-up as a reply or next day, you get return visitors.

---

## 3. Content Sourcing Playbook

How to find 10-20 viral clips every single day with zero creative effort.

### Reddit (Best Source, No Auth Required for JSON API)

**Subreddits to scrape daily (top posts, past week):**

| Subreddit | Members | Content Type | Best For |
|-----------|---------|-------------|----------|
| r/nextfuckinglevel | 10M+ | Skills, talent, feats | "he really did that" captions |
| r/oddlysatisfying | 8M+ | Satisfying processes, precision | "the precision here" captions |
| r/Unexpected | 7M+ | Surprise endings | "wait for it" captions |
| r/MadeMeSmile | 9M+ | Wholesome moments | Warmth + shareability |
| r/Damnthatsinteresting | 8M+ | Facts, rare footage | "you've never seen this before" |
| r/BeAmazed | 4M+ | Impressive visuals | "no way this is real" |
| r/interestingasfuck | 12M+ | Broad interesting content | General clips |
| r/NatureIsFuckingLit | 6M+ | Animal/nature footage | Animal clips |
| r/toptalent | 2M+ | Extreme skill displays | "rate this 1-10" |
| r/therewasanattempt | 4M+ | Fails, attempts | "is this a W or an L" |
| r/blackmagicfuckery | 3M+ | Unexplainable clips | "someone explain this" |
| r/nonononoyes | 2M+ | Close calls, saves | "watch this till the end" |

**How to scrape (no API key needed):**
```bash
# Get top 25 posts from past week as JSON
curl -s "https://www.reddit.com/r/nextfuckinglevel/top/.json?t=week&limit=25" \
  -H "User-Agent: clipvault/1.0" | python3 -m json.tool

# Download video from reddit post
yt-dlp "https://www.reddit.com/r/nextfuckinglevel/comments/POSTID/" -o "raw/reddit/%(title)s.%(ext)s"
```

**Daily Reddit routine:**
1. Hit each subreddit's top/week JSON endpoint
2. Filter for video posts (is_video: true or media type)
3. Download top 5 from each sub
4. Dedup against hash database
5. Pick 10 best for the day

### TikTok

**Source accounts to monitor (clip aggregators):**
- @clips (10M+)
- @trendingclips (4M+)
- @failarmy (50M+)
- @satisfying (8M+)
- @oddlysatisfying (5M+)
- @nextlevel (3M+)

**How to find trending clips:**
1. TikTok Creative Center (ads.tiktok.com/business/creativecenter) -- shows trending content
2. Browse For You page (10 min daily, save clips)
3. Search trending sounds -- clips using popular audio get boosted

**How to download:**
```bash
# Download TikTok video (no watermark)
yt-dlp "https://www.tiktok.com/@user/video/1234567890" -o "raw/tiktok/%(title)s.%(ext)s"
```

### Twitter/X

**Viral video accounts to monitor daily:**
- @TheFigen_ (3M+, viral clips and facts)
- @NoContextHumans (3M+, absurd human behavior)
- @InternetH0F (2M+, hall of fame internet moments)
- @HoodPosts (1M+, reaction videos)
- @CringeTok2 (600K+, TikTok compilations)
- @fearedbuck (1.5M+, mixed viral clips)
- @baborelux (500K+, interesting clips)
- @WorldWideClips (800K+, global viral moments)

**How to download:**
```bash
# Download Twitter video
yt-dlp "https://twitter.com/user/status/1234567890" -o "raw/twitter/%(id)s.%(ext)s"
```

### YouTube (Compilation Channels to Clip From)

**Channels with clippable content:**
- Daily Dose of Internet (18M subs) -- 3-5 min compilations, each segment is a standalone clip
- FailArmy (15M subs) -- fail compilations
- People Are Awesome (9M subs) -- skill/talent compilations
- That's Amazing (8M subs) -- trick shots, stunts
- Bored Panda (6M subs) -- interesting/wholesome
- SmarterEveryDay (11M subs) -- science demos (clip the "aha" moment)

**How to clip:**
```bash
# Download full video
yt-dlp "https://youtube.com/watch?v=VIDEO_ID" -o "raw/youtube/%(title)s.%(ext)s"

# Clip specific section (start at 1:30, duration 45 seconds)
ffmpeg -ss 00:01:30 -i "raw/youtube/video.mp4" -t 00:00:45 -c copy "processed/clip_001.mp4"
```

### Tools Summary

| Tool | Install | Purpose |
|------|---------|---------|
| yt-dlp | `pip install yt-dlp` | Download video from any platform |
| ffmpeg | `brew install ffmpeg` | Clip, trim, resize, reformat video |
| curl + python json | built-in | Reddit JSON API scraping |
| gallery-dl | `pip install gallery-dl` | Batch download images/videos |

---

## 4. Platform-Specific Reformatting Guide

Every clip gets reformatted per platform. One source clip becomes 5 platform-optimized versions.

### TikTok
- **Aspect ratio:** 9:16 vertical (1080x1920)
- **Duration:** 15-60 seconds (sweet spot: 20-35s for completion rate)
- **Audio:** Add trending sound as overlay OR keep original audio if it's interesting
- **Caption:** Short (under 100 chars). Place in text overlay too for silent viewers.
- **Hashtags:** In description, not caption. 3-5 relevant tags.
- **Key:** First frame must hook. First 1 second determines scroll-or-watch.

```bash
# Convert horizontal video to vertical (crop center)
ffmpeg -i input.mp4 -vf "crop=ih*9/16:ih,scale=1080:1920" -c:a copy tiktok_output.mp4

# Add black bars if you want to preserve full frame
ffmpeg -i input.mp4 -vf "scale=1080:-1,pad=1080:1920:(ow-iw)/2:(oh-ih)/2:black" -c:a copy tiktok_padded.mp4
```

### Instagram Reels
- **Aspect ratio:** 9:16 vertical (1080x1920) -- same as TikTok
- **Duration:** 15-90 seconds (sweet spot: 15-30s)
- **Audio:** IG has its own trending audio library. Swap to trending IG audio when possible.
- **Caption:** Under 125 chars for preview (full caption can be longer). First line = hook.
- **Hashtags:** 5-10 in caption or first comment. Mix broad (#viral #fyp) with niche (#oddlysatisfying #skills).
- **Cover image:** Pick the most visually striking frame. This shows on your grid.

### YouTube Shorts
- **Aspect ratio:** 9:16 vertical (1080x1920) -- same format
- **Duration:** Under 60 seconds (hard limit)
- **Title:** Descriptive, searchable. YouTube Shorts titles work like regular YouTube SEO. Example: "Woodworker builds miniature house in 30 seconds" not just "wait for it"
- **Audio:** Original audio usually fine. YouTube doesn't have a trending audio push like TikTok.
- **Description:** 2-3 sentences + hashtags. #Shorts tag helps discovery.
- **Key:** YouTube favors watch time and re-watches. Clips people watch twice perform best.

### Facebook
- **Aspect ratio:** 1:1 square (1080x1080) works best for feed. 9:16 for Reels.
- **Duration:** 15-60 seconds. Facebook auto-plays muted, so visual hook is everything.
- **Captions:** Burn subtitles into video (80%+ watch muted on FB). Use ffmpeg + .srt file.
- **Text:** Longer captions OK on FB. 1-3 sentences. Ask a question to drive comments.
- **Key:** Facebook rewards shares above all else. Wholesome + impressive clips get shared to family/friends.

```bash
# Convert to square (crop center)
ffmpeg -i input.mp4 -vf "crop=min(iw\,ih):min(iw\,ih),scale=1080:1080" -c:a copy fb_square.mp4

# Burn subtitles into video
ffmpeg -i input.mp4 -vf "subtitles=captions.srt:force_style='FontSize=24,PrimaryColour=&Hffffff&,OutlineColour=&H000000&,BorderStyle=3'" output_subtitled.mp4
```

### X/Twitter
- **Aspect ratio:** 16:9 horizontal (1920x1080) or 1:1 square. Native upload only.
- **Duration:** Under 2 minutes 20 seconds (hard limit).
- **Upload:** Native upload (not links). Twitter buries linked videos from other platforms.
- **Caption:** Above the video. Keep it under 280 chars. Caption IS the hook.
- **Key:** Quote tweets and replies drive virality on X. Post clip, then reply to yourself with "follow @clipvault_ for more" -- never put it in the main caption.

---

## 5. Hashtag Sets (30 sets, 5 hashtags each)

Use one set per post. Rotate across content types. Platform-specific notes: TikTok (use all 5), IG (use all 5 + add 3-5 broad ones), YouTube Shorts (use 3 in description), X (use 0-2 max, tags hurt reach on X), Facebook (use 0-3).

### Funny / Comedy
```
Set 1:  #funny #comedy #trynottolaugh #hilarious #lol
Set 2:  #funnyvideos #humor #laughing #comedia #jokes
Set 3:  #funnymoments #funnyclips #viral #haha #memes
```

### Satisfying / ASMR
```
Set 4:  #satisfying #oddlysatisfying #asmr #relaxing #soothing
Set 5:  #satisfyingvideos #cleaningasmr #organize #perfectfit #smooth
Set 6:  #mostsatisfying #slime #crunchy #peeling #cutting
```

### Wholesome / Feel Good
```
Set 7:  #wholesome #feelgood #mademyday #heartwarming #kindness
Set 8:  #faith #blessed #goodvibes #positivity #smile
Set 9:  #humanity #restored #love #beautiful #emotional
```

### Skills / Talent
```
Set 10: #skills #talent #nextlevel #insane #impressive
Set 11: #trickshot #parkour #athlete #gifted #practice
Set 12: #art #artist #creative #masterpiece #handmade
```

### Fails / Instant Regret
```
Set 13: #fail #fails #epicfail #instantregret #oops
Set 14: #failarmy #wipeout #faceplant #nailed #gone
Set 15: #whatcouldgowrong #holdmybeer #ouch #karma #timing
```

### Animals
```
Set 16: #animals #cute #pets #dogsoftiktok #catsoftiktok
Set 17: #puppy #kitten #wildlife #nature #adorable
Set 18: #animalsoftiktok #funnyanimals #dog #cat #birdsoftiktok
```

### Food / Cooking
```
Set 19: #food #cooking #recipe #foodporn #chef
Set 20: #foodtiktok #yummy #delicious #homemade #baking
Set 21: #streetfood #asmrfood #mukbang #foodie #tasty
```

### Tech / Science
```
Set 22: #tech #science #engineering #invention #future
Set 23: #technology #gadgets #innovation #robotics #ai
Set 24: #diy #howto #lifehack #smarttech #cool
```

### Sports / Fitness
```
Set 25: #sports #fitness #gym #basketball #football
Set 26: #workout #athlete #training #goals #motivation
Set 27: #soccer #mma #boxing #extreme #highlights
```

### Nature / Travel
```
Set 28: #nature #travel #beautiful #earth #explore
Set 29: #adventure #landscape #ocean #mountains #sunset
Set 30: #drone #aerial #paradise #wanderlust #planet
```

---

## 6. Posting Schedule

Optimal times based on clip/meme account research. All times EST. Adjust for your timezone.

### Daily Schedule (2 posts/day minimum during Week 1)

| Day | Post 1 Time | Post 1 Platform Priority | Post 2 Time | Post 2 Platform Priority |
|-----|-------------|--------------------------|-------------|--------------------------|
| Mon | 12:00 PM | TikTok, IG Reels, X | 7:00 PM | YouTube Shorts, FB, X |
| Tue | 8:00 AM | X, TikTok | 6:00 PM | IG Reels, YouTube Shorts, FB |
| Wed | 11:00 AM | TikTok, IG Reels | 9:00 PM | X, YouTube Shorts, FB |
| Thu | 9:00 AM | X, TikTok | 7:00 PM | IG Reels, YouTube Shorts, FB |
| Fri | 12:00 PM | TikTok, IG Reels, X | 8:00 PM | YouTube Shorts, FB, X |
| Sat | 10:00 AM | TikTok, IG Reels | 5:00 PM | X, YouTube Shorts, FB |
| Sun | 11:00 AM | X, TikTok, IG Reels | 6:00 PM | YouTube Shorts, FB |

### Platform-Specific Optimal Windows

**TikTok:**
- Best: 10 AM - 12 PM, 7 PM - 9 PM
- Good: 2 PM - 4 PM
- Avoid: 1 AM - 6 AM

**Instagram Reels:**
- Best: 9 AM - 11 AM, 6 PM - 8 PM
- Good: 12 PM - 2 PM
- Avoid: 12 AM - 5 AM

**YouTube Shorts:**
- Best: 12 PM - 3 PM, 5 PM - 7 PM
- Good: 8 AM - 10 AM
- Avoid: 11 PM - 6 AM (Shorts perform better during daytime browsing)

**X/Twitter:**
- Best: 8 AM - 10 AM, 12 PM - 1 PM, 5 PM - 7 PM
- Good: 9 PM - 11 PM
- Avoid: 2 AM - 6 AM

**Facebook:**
- Best: 1 PM - 4 PM (office workers on break/afternoon scroll)
- Good: 9 AM - 11 AM
- Avoid: 11 PM - 7 AM

### Week 1 Content Calendar (Fully Mapped)

| Day | Time | Caption | Content Type | Engagement Format | Hashtag Set |
|-----|------|---------|-------------|-------------------|-------------|
| Mon AM | 12 PM | "this shouldn't work but it does" | Skill/engineering clip | -- | Set 10 |
| Mon PM | 7 PM | "wait for it" | Surprise ending clip | Rate This (Format 1) | Set 1 |
| Tue AM | 8 AM | "he really did that" | Athletic/bold move clip | -- | Set 25 |
| Tue PM | 6 PM | "no way this is real" | Optical illusion / nature clip | Which One? (Format 2) | Set 28 |
| Wed AM | 11 AM | "rate this 1-10" | Food/art/build clip | -- | Set 19 |
| Wed PM | 9 PM | "which one are you" | Comparison/reaction clip | Caption This (Format 3) | Set 1 |
| Thu AM | 9 AM | "the precision here" | Craft/machining clip | -- | Set 4 |
| Thu PM | 7 PM | "someone explain this" | Physics/weird clip | One Word Only (Format 4) | Set 22 |
| Fri AM | 12 PM | "bro was not expecting that" | Prank/surprise clip | -- | Set 13 |
| Fri PM | 8 PM | "name this in one word" | High-energy clip | Fill in Blank (Format 5) | Set 10 |
| Sat AM | 10 AM | "watch this till the end" | Long payoff clip | -- | Set 4 |
| Sat PM | 5 PM | "is this a W or an L" | Debatable outcome clip | Would You? (Format 6) | Set 13 |
| Sun AM | 11 AM | "the level of detail here" | Miniature/craft clip | -- | Set 12 |
| Sun PM | 6 PM | "you've never seen this before" | Rare footage clip | What Happened Next (Format 7) | Set 28 |

---

## 7. Week 1 Execution Checklist

```
BEFORE DAY 1:
[ ] Create @clipvault_ on X/Twitter
[ ] Create @clipvault_ on TikTok
[ ] Create @clipvault_ on Instagram
[ ] Create clipvault channel on YouTube
[ ] Create clipvault page on Facebook
[ ] Set up Buffer free tier (connect 3 accounts)
[ ] Install yt-dlp: pip install yt-dlp
[ ] Install ffmpeg: brew install ffmpeg
[ ] Create folder structure: raw/, processed/, posted/
[ ] Source first 14 clips (see sourcing playbook above)
[ ] Process clips for each platform (see reformatting guide)

DAY 1 (Monday):
[ ] Post clip 1 at 12 PM: "this shouldn't work but it does"
[ ] Post clip 2 at 7 PM: "wait for it" + Rate This engagement in caption
[ ] Reply to 5 viral clips on X with "follow for more"
[ ] Source tomorrow's 2 clips from Reddit/TikTok

DAY 2 (Tuesday):
[ ] Post clip 3 at 8 AM: "he really did that"
[ ] Post clip 4 at 6 PM: "no way this is real" + Which One? engagement
[ ] Source tomorrow's clips
[ ] Check Day 1 analytics: which caption got more engagement?

DAY 3 (Wednesday):
[ ] Post clip 5 at 11 AM: "rate this 1-10"
[ ] Post clip 6 at 9 PM: "which one are you" + Caption This engagement
[ ] Source tomorrow's clips
[ ] Double down on whichever caption format is winning

DAY 4 (Thursday):
[ ] Post clip 7 at 9 AM: "the precision here"
[ ] Post clip 8 at 7 PM: "someone explain this" + One Word Only engagement
[ ] Source tomorrow's clips

DAY 5 (Friday):
[ ] Post clip 9 at 12 PM: "bro was not expecting that"
[ ] Post clip 10 at 8 PM: "name this in one word" + Fill in Blank engagement
[ ] Source weekend clips (batch 4 clips for Sat+Sun)

DAY 6 (Saturday):
[ ] Post clip 11 at 10 AM: "watch this till the end"
[ ] Post clip 12 at 5 PM: "is this a W or an L" + Would You? engagement

DAY 7 (Sunday):
[ ] Post clip 13 at 11 AM: "the level of detail here"
[ ] Post clip 14 at 6 PM: "you've never seen this before" + What Happened Next engagement
[ ] Full Week 1 analytics review:
    - Which captions drove most comments?
    - Which clip types got most views?
    - Which platform performed best?
    - Which posting time worked best?
[ ] Plan Week 2: double down on top 3 caption formats, cut bottom 3
```

---

## 8. Key Rules for @clipvault_

1. Never claim content as original. You are a curator.
2. No personal voice. No "I think" or "lol." Neutral framing only.
3. Caption is a frame, not commentary. 2-8 words. Let the clip do the work.
4. Source content that is 30+ days old. Never rip something posted today.
5. Never use the exact same caption as the original post.
6. Upload natively to every platform. Never post links.
7. If DMCA'd, remove immediately. No argument. Move on.
8. Post consistently. 2/day minimum, every day, no breaks during Week 1.
9. Engage in replies on viral posts from other accounts to get seen.
10. Track everything. Which caption, which clip type, which time, which platform.

---

## 9. Scaling After Week 1

**Week 2:** Increase to 3 posts/day. Add engagement replies (reply to your own posts with "follow for more clips"). Start "series" format ("satisfying clips vol. 1, 2, 3...").

**Week 3:** Increase to 4 posts/day. Start compilations (3-5 clips in one video, 60-90 seconds). Cross-promote with other clip accounts (mutual shoutouts).

**Week 4:** Full cadence: 4-6 posts/day. Set up Buffer paid if needed. Analyze top 10 posts of the month, replicate those formats. Set bio link to Beehiiv or Gumroad for eventual monetization.

**Month 2+:** Start accepting shoutout trades. Add bio link. Test affiliate links. Redirect traffic to monetized niche accounts (@PRINTMAXXER, faith, fitness).

---

**Status:** PENDING_REVIEW
**Created:** 2026-02-13
**Account:** @clipvault_
**Next action:** Create accounts on all 5 platforms, source first 14 clips, process and schedule.

---

*Affiliate Disclosure: Some links may be affiliate links. We may earn a commission at no extra cost to you.*
