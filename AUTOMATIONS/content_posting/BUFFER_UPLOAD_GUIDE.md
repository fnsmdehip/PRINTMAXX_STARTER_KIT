# buffer/publer bulk upload guide

**3 CSV files. 130 tweets. 3 accounts. here's exactly how to load them and start posting today.**

---

## what you have right now

| file | posts | account | niche |
|------|-------|---------|-------|
| `printmaxxer_tweets_50.csv` | 50 | @PRINTMAXXER | tech/solopreneur build-in-public |
| `findom_tweets_50.csv` | 50 | findom persona | AI adult content |
| `meme_engagement_tweets_30.csv` | 30 | meme account | engagement farming |

all 3 CSVs use the same format:

```
tweet_text,category,post_time_slot
```

`post_time_slot` values: `morning`, `midday`, `afternoon`, `evening`

additional content in `CONTENT/social/` subdirectories: `ai/`, `faith/`, `fitness/`, `findom/`, `launch_posts/`, `linkedin/`, `memes/`, `pinterest/`, `reddit/`, `threads/`

---

## step 1: convert CSVs to buffer format

buffer wants 2 columns: `Text` and `Date/Time` (or just `Text` if you're using buffer's queue slots).

### option A: queue-only upload (fastest, 5 minutes)

buffer's queue feature auto-schedules posts at your preset times. you only need to upload text, no date/time mapping needed.

**buffer CSV format for queue upload:**
```
Text
"day 4. 6 revenue streams live. content farm posted 312 pieces..."
"found a tool that scrapes every new product hunt launch..."
```

**convert with this script:**

```bash
python3 -c "
import csv, sys

input_file = sys.argv[1]
output_file = sys.argv[2]

with open(input_file) as f:
    reader = csv.DictReader(f)
    rows = list(reader)

with open(output_file, 'w', newline='') as f:
    w = csv.writer(f)
    w.writerow(['Text'])
    for r in rows:
        w.writerow([r['tweet_text']])
print(f'converted {len(rows)} posts -> {output_file}')
" AUTOMATIONS/content_posting/printmaxxer_tweets_50.csv AUTOMATIONS/content_posting/buffer_printmaxxer.csv
```

run 3 times, swapping filenames:

```bash
# @PRINTMAXXER
python3 -c "..." printmaxxer_tweets_50.csv buffer_printmaxxer.csv

# findom persona
python3 -c "..." findom_tweets_50.csv buffer_findom.csv

# meme account
python3 -c "..." meme_engagement_tweets_30.csv buffer_memes.csv
```

### option B: date/time upload (10 minutes)

if you want exact scheduling control. assign real dates and times based on `post_time_slot`.

```bash
python3 -c "
import csv, sys
from datetime import datetime, timedelta

input_file = sys.argv[1]
output_file = sys.argv[2]
start_date = '2026-02-07'  # change to your start date

time_map = {
    'morning': '08:30',
    'midday': '12:15',
    'afternoon': '15:30',
    'evening': '19:45'
}

with open(input_file) as f:
    reader = csv.DictReader(f)
    rows = list(reader)

# group by time slot for round-robin date assignment
slot_counts = {}
base = datetime.strptime(start_date, '%Y-%m-%d')

with open(output_file, 'w', newline='') as f:
    w = csv.writer(f)
    w.writerow(['Text', 'Date', 'Time'])
    for i, r in enumerate(rows):
        slot = r['post_time_slot']
        slot_counts[slot] = slot_counts.get(slot, 0)
        day_offset = slot_counts[slot]
        post_date = (base + timedelta(days=day_offset)).strftime('%Y-%m-%d')
        post_time = time_map.get(slot, '12:00')
        w.writerow([r['tweet_text'], post_date, post_time])
        slot_counts[slot] += 1

print(f'converted {len(rows)} posts -> {output_file}')
print(f'date range: {start_date} to {(base + timedelta(days=max(slot_counts.values()))).strftime(\"%Y-%m-%d\")}')
" AUTOMATIONS/content_posting/printmaxxer_tweets_50.csv AUTOMATIONS/content_posting/buffer_printmaxxer_dated.csv
```

---

## step 2: upload to buffer

### buffer bulk upload (free plan: 3 channels, 10 posts/channel queue)

1. go to [buffer.com](https://buffer.com) > log in
2. connect your X/Twitter account (do this per account - @PRINTMAXXER, findom, meme)
3. click **Publishing** in left sidebar
4. click **Queue** tab
5. click the **Bulk Create** button (top right, looks like a stack icon)
6. choose **Upload CSV**
7. select your converted CSV file (`buffer_printmaxxer.csv`)
8. buffer will show a preview of all posts
9. review the preview. check for:
   - no broken formatting
   - no cut-off text
   - hashtags display correctly
10. click **Add to Queue**
11. posts are now queued at your preset posting times

**buffer free plan limit: 10 posts per channel in queue.** if you have 50 posts, you'll need buffer paid ($6/mo per channel) or upload in batches of 10.

### buffer posting schedule setup

before uploading, set your queue times:

1. go to **Publishing** > **Settings** (gear icon)
2. select your X/Twitter channel
3. under **Posting Schedule**, add these time slots:

**@PRINTMAXXER (4-6 posts/day):**

| slot | time (ET) | why |
|------|-----------|-----|
| 1 | 8:30 AM | early morning tech twitter is active |
| 2 | 10:15 AM | second morning wave |
| 3 | 12:15 PM | lunch scroll |
| 4 | 3:30 PM | afternoon slump = phone checking |
| 5 | 5:45 PM | commute scroll |
| 6 | 7:45 PM | evening wind-down |

**findom persona (3-5 posts/day):**

| slot | time (ET) | why |
|------|-----------|-----|
| 1 | 9:00 AM | morning tribute ask timing |
| 2 | 1:00 PM | midday engagement |
| 3 | 5:00 PM | after-work payday energy |
| 4 | 9:00 PM | late night highest findom engagement |
| 5 | 11:30 PM | insomnia scroll (high conversion window) |

**meme account (5-8 posts/day):**

| slot | time (ET) | why |
|------|-----------|-----|
| 1 | 7:00 AM | early morning meme check |
| 2 | 9:30 AM | work avoidance scroll |
| 3 | 11:00 AM | pre-lunch |
| 4 | 12:30 PM | lunch scroll peak |
| 5 | 2:30 PM | afternoon slump peak |
| 6 | 5:00 PM | end of workday |
| 7 | 7:30 PM | evening entertainment |
| 8 | 10:00 PM | late night engagement peak |

---

## step 3: upload to publer (alternative)

publer is better than buffer for multi-account management. free plan: 3 social accounts, 10 scheduled posts. paid: $12/mo unlimited.

### publer CSV format

publer accepts a slightly different format:

```
Text,Date,Time,Social Account
"your tweet text here",2026-02-07,08:30,@PRINTMAXXER
```

**convert script for publer:**

```bash
python3 -c "
import csv, sys
from datetime import datetime, timedelta

input_file = sys.argv[1]
output_file = sys.argv[2]
account_name = sys.argv[3]
start_date = '2026-02-07'

time_map = {
    'morning': '08:30',
    'midday': '12:15',
    'afternoon': '15:30',
    'evening': '19:45'
}

with open(input_file) as f:
    reader = csv.DictReader(f)
    rows = list(reader)

slot_counts = {}
base = datetime.strptime(start_date, '%Y-%m-%d')

with open(output_file, 'w', newline='') as f:
    w = csv.writer(f)
    w.writerow(['Text', 'Date', 'Time', 'Social Account'])
    for r in rows:
        slot = r['post_time_slot']
        slot_counts[slot] = slot_counts.get(slot, 0)
        day_offset = slot_counts[slot]
        post_date = (base + timedelta(days=day_offset)).strftime('%Y-%m-%d')
        post_time = time_map.get(slot, '12:00')
        w.writerow([r['tweet_text'], post_date, post_time, account_name])
        slot_counts[slot] += 1

print(f'converted {len(rows)} posts -> {output_file}')
" AUTOMATIONS/content_posting/printmaxxer_tweets_50.csv AUTOMATIONS/content_posting/publer_printmaxxer.csv @PRINTMAXXER
```

### publer upload steps

1. go to [publer.io](https://publer.io) > log in
2. click **Create Post** > **Bulk Schedule**
3. select **Import from CSV**
4. upload your converted CSV
5. map columns:
   - Text -> Content
   - Date -> Date
   - Time -> Time
   - Social Account -> Account (or select manually)
6. set timezone: **Eastern Time (ET)**
7. click **Preview All** - scan for formatting issues
8. click **Schedule All**
9. check calendar view to verify spread looks right

### publer vs buffer: which to use

| feature | buffer (free) | buffer ($6/ch/mo) | publer (free) | publer ($12/mo) |
|---------|---------------|-------------------|---------------|-----------------|
| channels | 3 | unlimited | 3 | 10 |
| queue size | 10/channel | unlimited | 10 | 500 |
| CSV upload | yes | yes | yes | yes |
| auto-hashtags | no | no | yes | yes |
| AI writing | no | yes | no | yes |
| best for | testing | single brand | testing | multi-account |

**recommendation:** publer paid ($12/mo) if running 3+ accounts. buffer paid ($6/mo x 3 = $18/mo) if you want simpler UI but only for X/Twitter.

---

## step 4: manual fallback (if tools fail or free tier hits limits)

no scheduler needed. just discipline and a spreadsheet.

### daily posting workflow (15-20 min/day)

1. open the CSV in google sheets or numbers
2. filter by today's `post_time_slot`
3. set 4 phone alarms: 8:30am, 12:15pm, 3:30pm, 7:45pm ET
4. when alarm fires:
   - open CSV
   - find next unposted row for that time slot
   - copy `tweet_text`
   - paste into X/Twitter compose
   - post
   - mark row as "posted" (add a column, type "Y")
5. repeat until all CSVs are empty

### batch manual posting (for same-day queue)

if you want to post them all in one sitting using X/Twitter's native scheduler:

1. go to x.com > compose tweet
2. paste tweet text
3. click the calendar icon (bottom of compose box)
4. set date and time
5. click **Schedule**
6. repeat for all posts

this takes about 45-60 minutes for 50 posts but gives you full control.

---

## content rotation strategy

### category distribution per account

**@PRINTMAXXER categories:**

| category | % of posts | purpose |
|----------|-----------|---------|
| BUILD_UPDATE | 20% | day-by-day progress, real numbers |
| TOOL_SHARE | 15% | specific tools with costs and results |
| TACTIC_DROP | 15% | exact playbooks with numbers |
| NUMBER_FLEX | 10% | revenue/metrics dashboards |
| MINDSET | 15% | philosophy, anti-planning energy |
| HOW_TO | 15% | step-by-step breakdowns |
| CONTRARIAN | 10% | hot takes that drive engagement |

**findom persona categories:**

| category | % of posts | purpose |
|----------|-----------|---------|
| TRIBUTE_ASK | 20% | direct money asks |
| DEGRADATION_LITE | 15% | light humiliation (keeps it legal/platform-safe) |
| LUXURY_FLEX | 15% | lifestyle photos + "you paid for this" |
| ENGAGEMENT_GAME | 15% | spin wheels, salary reveals, interactive |
| COMMUNITY | 15% | RT chains, shoutouts, welcome posts |
| TEASE | 10% | fanvue/fansly previews |
| LIFESTYLE | 10% | aspirational content |

**meme account categories:**

| category | % of posts | purpose |
|----------|-----------|---------|
| HOT_TAKE | 20% | spicy opinions that drive quote tweets |
| ENGAGEMENT_BAIT | 20% | questions, polls, "wrong answers only" |
| MEME_FORMAT | 20% | relatable humor formats |
| RATIO_BAIT | 20% | controversial enough to quote-tweet |
| VIRAL_FORMAT | 20% | "unpopular opinion" pattern |

### rotation rules (non-negotiable)

1. **never post same category back-to-back.** if morning was BUILD_UPDATE, midday must be different.
2. **max 2 of same category per day.** even on 6-post days.
3. **promotional content (TRIBUTE_ASK, NUMBER_FLEX) never opens the day.** lead with value or engagement.
4. **end-of-day slot is highest engagement.** save your best content for evening.

### how to enforce rotation in buffer/publer

when uploading, sort your CSV by alternating categories:

```bash
python3 -c "
import csv
from itertools import cycle

with open('AUTOMATIONS/content_posting/printmaxxer_tweets_50.csv') as f:
    rows = list(csv.DictReader(f))

# group by category
cats = {}
for r in rows:
    cats.setdefault(r['category'], []).append(r)

# interleave categories
cat_iters = {k: iter(v) for k, v in cats.items()}
cat_cycle = cycle(cats.keys())
rotated = []

while len(rotated) < len(rows):
    cat = next(cat_cycle)
    try:
        rotated.append(next(cat_iters[cat]))
    except StopIteration:
        cat_iters.pop(cat)
        if not cat_iters:
            break
        remaining_cats = list(cat_iters.keys())
        cat_cycle = cycle(remaining_cats)

with open('AUTOMATIONS/content_posting/buffer_printmaxxer_rotated.csv', 'w', newline='') as f:
    w = csv.writer(f)
    w.writerow(['Text'])
    for r in rotated:
        w.writerow([r['tweet_text']])
print(f'rotated {len(rotated)} posts with category interleaving')
"
```

upload the rotated CSV to buffer's queue. queue posts in order = automatic rotation.

---

## cross-platform repurposing

### twitter -> threads

1. copy tweet text
2. add 1-2 sentences of context (threads users expect slightly longer posts)
3. add "follow for more [niche] content" at the end
4. post to threads

**example:**
```
twitter: "cold emailed 200 dentists with a mockup of a website i already built for them. 27% open rate. 4 calls booked."

threads: "cold emailed 200 dentists with a mockup of a website i already built for them. personalized screenshot in every email. 27% open rate. 4 calls booked. closing at $1,500 each.

the trick? build the product before you reach out. they see it's real and respond. follow for more cold outreach tactics."
```

### twitter -> linkedin

1. copy tweet text
2. expand to 3-5 sentences (linkedin rewards longer posts in 2026)
3. add a line break after the hook (linkedin algo loves the "see more" click)
4. remove slang, keep specific numbers
5. add a question at the end (drives comments)
6. no hashtags or 1 max

**example:**
```
twitter: "found a tool that scrapes every new product hunt launch and emails me the founder's contact info. 14% reply rate. $0 tool cost"

linkedin: "I found a tool that scrapes every new Product Hunt launch and emails me the founder's contact details.

I've been reaching out to offer growth services. 14% reply rate from cold emails. The tool costs $0.

Most people wait for clients to find them. I go find the clients the day they launch, when they need help the most.

What's your approach to finding new clients?"
```

### twitter -> instagram caption

1. copy tweet text as the first line (hook)
2. expand into 3-5 short paragraphs
3. add 5-15 hashtags at the bottom
4. pair with a canva visual (screenshot, quote card, or carousel)
5. save visual ideas to `CONTENT/social/pinterest/` for reuse

**canva template approach:**
- text-on-gradient for quotes and hot takes
- screenshot mockup for tool shares and number flexes
- carousel for how-to posts (1 step per slide)
- before/after for build updates

### twitter -> pinterest

1. create a canva pin (1000x1500px)
2. put tweet text as overlay on branded background
3. add your handle at the bottom
4. title: rephrase tweet as a "how to" or question
5. description: expand with 2-3 sentences + relevant keywords
6. link: to your gumroad, newsletter signup, or landing page

### repurposing schedule

| day | original platform | repurpose to | posts |
|-----|-------------------|--------------|-------|
| same day | X/Twitter | Threads | top 2-3 tweets |
| next day | X/Twitter | LinkedIn | top 1-2 (professionalized) |
| 2 days later | X/Twitter | Instagram | top 1 (with canva visual) |
| weekly batch | all top performers | Pinterest | 5-10 pins from best tweets |

### batch repurposing workflow (1 hour/week)

1. export your top 10 tweets from X analytics (by engagement rate)
2. convert top 5 to linkedin posts (save to `CONTENT/social/linkedin/`)
3. convert top 3 to instagram captions + create canva visuals
4. convert top 5 to pinterest pins
5. convert all 10 to threads posts
6. schedule everything in buffer/publer for the following week

---

## engagement protocol after posting

this is where most people fail. posting without engaging is like opening a store and hiding in the back room.

### 30-minute engagement window (every post)

1. **set a timer for 30 minutes after each post goes live**
2. reply to the first 3 comments within that window
3. like every comment within the first hour
4. if someone asks a question, reply with a value-add (not just "thanks!")
5. if engagement is high (10+ replies in 30 min), stay in thread and keep replying

### self-reply strategy (the real growth hack)

buffer/publer post your main tweet. then you manually add self-replies.

**self-reply rules:**
- never put a CTA in the main tweet. put it in the first self-reply.
- first self-reply within 2-3 minutes of posting
- format: additional value, then soft CTA

**example self-reply chain:**
```
main tweet: "cold emailed 200 dentists with a mockup of a website i already built for them. 27% open rate. 4 calls booked."

self-reply 1: "the template is 4 lines. subject line: 'built this for [practice name]'. body: screenshot + 3 bullet points of what I'd fix. link to the mockup. that's it."

self-reply 2: "tools used: apollo for leads ($0 free tier). instantly for warmup ($30/mo). canva for mockup screenshots. total cost: $30/mo."

self-reply 3: "i put together the exact cold email template + mockup workflow. reply 'COLD' and i'll send it over."
```

the CTA is in reply 3, not the main post. this is critical. algorithm hates links in main tweets. loves engagement in threads.

### quote-tweet recycling (24-48 hours later)

1. check which tweets got the most engagement
2. quote-tweet your own best performers with added context
3. timing: 24-48 hours after original post
4. add new angle, not just "this did well"

**example:**
```
quote tweet of your own post:
"update on this - closed 2 of the 4 calls. $3,000 from 200 cold emails. the ROI math: $30 tool cost. $3,000 revenue. 100x return. still think cold email is dead?"
```

### engagement time budget per account

| account | daily engagement time | what to do |
|---------|----------------------|------------|
| @PRINTMAXXER | 30 min | reply to comments, engage in solopreneur threads, self-replies |
| findom persona | 20 min | reply to tributes, run engagement games, RT chain participation |
| meme account | 15 min | reply to top comments, engage in tech/startup threads |

total: 65 min/day. front-load to first 30 min after each post goes live.

---

## metrics tracking

### what to track weekly

| metric | target (week 1-2) | target (week 4+) | where to check |
|--------|-------------------|-------------------|----------------|
| impressions/post | 200+ | 1,000+ | X analytics |
| engagement rate | 2%+ | 4%+ | X analytics (engagements / impressions) |
| link clicks | 5+/post | 25+/post | bit.ly or buffer analytics |
| follower growth | 50+/week | 200+/week | X profile |
| reply rate | 3+ replies/post | 10+/post | X analytics |
| self-reply CTA conversion | 1%+ of impressions | 3%+ | manual count |
| profile visits | 100+/week | 500+/week | X analytics |

### weekly review process (every sunday, 30 min)

1. pull X analytics for all 3 accounts
2. sort posts by engagement rate (descending)
3. identify top 5 and bottom 5 posts
4. check which **categories** appear in top 5 vs bottom 5
5. update this tracker:

```
AUTOMATIONS/content_posting/weekly_metrics.csv

week,account,category,avg_impressions,avg_engagement_rate,avg_replies,top_post_text
```

### kill/scale rules

| signal | action |
|--------|--------|
| category avg engagement < 1.5% for 2 weeks | kill that category. replace with more of what works |
| category avg engagement > 5% for 2 weeks | double posts in that category |
| specific post gets 10x avg impressions | turn it into a thread. turn it into a carousel. repurpose to every platform |
| follower growth < 20/week after week 2 | audit posting times, add 2 more daily posts, increase engagement time |
| link clicks < 5/week | move CTAs from main posts to self-replies. add more value-first posts |

### performance log template

save to `AUTOMATIONS/content_posting/performance_log.md` after each weekly review:

```
## week of [date]

### @PRINTMAXXER
- total impressions: X
- avg engagement rate: X%
- followers gained: X
- top category: X (X% eng rate)
- worst category: X (X% eng rate)
- revenue attributed: $X
- action: [kill/scale/maintain for each category]

### findom persona
- [same metrics]

### meme account
- [same metrics]

### changes for next week
- [specific adjustments]
```

---

## content from CONTENT/social/ directories

the CSV files are your primary queue. but there's additional content in `CONTENT/social/` subdirectories.

### how to use each directory

| directory | content type | upload to |
|-----------|-------------|-----------|
| `ai/` | tech AI posts (10 PRINTMAXXER launch posts) | @PRINTMAXXER X queue |
| `faith/` | PrayerLock posts | faith niche accounts |
| `fitness/` | WalkToUnlock posts | fitness niche accounts |
| `findom/` | findom content | findom persona X queue |
| `launch_posts/` | product launch announcements | all relevant accounts on launch day |
| `linkedin/` | professionalized content | linkedin accounts |
| `memes/` | meme content | meme account X queue |
| `pinterest/` | pin descriptions + text overlays | pinterest account |
| `reddit/` | GEO-optimized posts (6 posts) | relevant subreddits (manual only, don't automate reddit) |
| `threads/` | threads-adapted content | threads accounts |

### loading CONTENT/social/ into buffer

these files are markdown, not CSV. convert manually:

1. open the markdown file
2. copy each post block
3. paste into buffer compose (one post at a time)
4. add to queue

or batch convert:

```bash
# example: convert all .md files in a directory to a buffer CSV
python3 -c "
import os, csv, re

dir_path = 'CONTENT/social/ai/'
output = 'AUTOMATIONS/content_posting/buffer_ai_posts.csv'

posts = []
for f in sorted(os.listdir(dir_path)):
    if f.endswith('.md'):
        with open(os.path.join(dir_path, f)) as fh:
            content = fh.read()
            # extract individual posts (split by --- or ## or numbered list)
            blocks = re.split(r'\n---\n|\n## ', content)
            for b in blocks:
                b = b.strip()
                if len(b) > 10 and len(b) < 280:
                    posts.append(b)

with open(output, 'w', newline='') as f:
    w = csv.writer(f)
    w.writerow(['Text'])
    for p in posts:
        w.writerow([p])
print(f'extracted {len(posts)} posts -> {output}')
"
```

---

## complete launch sequence (do this today)

### phase 1: account setup (30 min)

1. create buffer account at buffer.com (or publer at publer.io)
2. connect @PRINTMAXXER X/Twitter account
3. connect findom persona X/Twitter account
4. connect meme X/Twitter account
5. set posting schedules per the time slots above

### phase 2: CSV conversion (10 min)

```bash
cd /Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt

# convert all 3 CSVs for buffer queue upload
for pair in "printmaxxer_tweets_50.csv buffer_printmaxxer.csv" "findom_tweets_50.csv buffer_findom.csv" "meme_engagement_tweets_30.csv buffer_memes.csv"; do
    set -- $pair
    python3 -c "
import csv, sys
with open('AUTOMATIONS/content_posting/$1') as f:
    rows = list(csv.DictReader(f))
with open('AUTOMATIONS/content_posting/$2', 'w', newline='') as f:
    w = csv.writer(f)
    w.writerow(['Text'])
    for r in rows:
        w.writerow([r['tweet_text']])
print(f'converted {len(rows)} -> $2')
"
done
```

### phase 3: upload (15 min)

1. buffer > @PRINTMAXXER channel > bulk create > upload `buffer_printmaxxer.csv` > add to queue
2. buffer > findom channel > bulk create > upload `buffer_findom.csv` > add to queue
3. buffer > meme channel > bulk create > upload `buffer_memes.csv` > add to queue

### phase 4: verify (5 min)

1. check buffer calendar view. posts should be spread across your time slots.
2. verify no duplicate posts on same day
3. check the queue order - categories should alternate (if you ran the rotation script)
4. confirm timezone is set to ET

### phase 5: engage (daily, 65 min)

1. when each post goes live, open X
2. add self-reply within 2-3 minutes (value + CTA in reply 3)
3. reply to first 3 comments within 30 min
4. like all comments within first hour
5. quote-tweet best performers 24-48 hours later

---

## troubleshooting

| problem | fix |
|---------|-----|
| buffer free tier limit (10 posts) | upgrade to $6/mo or upload in batches of 10, refill queue daily |
| CSV upload fails | check for unescaped quotes in tweet text. wrap all text in double quotes. escape internal quotes with \" |
| posts look wrong after upload | preview every post before confirming. check for line breaks mid-tweet |
| wrong timezone | buffer settings > timezone > set to Eastern (ET/EST/EDT) |
| duplicate posts | run dedup before upload: `sort -u buffer_printmaxxer.csv > deduped.csv` |
| hashtags getting cut off | X has 280 char limit. if tweet + hashtags > 280, move hashtags to self-reply |
| buffer doesn't support threads/self-replies | buffer only posts main tweets. self-replies are manual (set phone alerts) |
| publer CSV won't import | publer is strict on column names. use exact headers: Text, Date, Time |

---

## cost summary

| tool | free tier | paid tier | recommendation |
|------|-----------|-----------|----------------|
| buffer | 3 channels, 10 queued/each | $6/channel/mo unlimited | start free, upgrade when queue limit hurts |
| publer | 3 accounts, 10 scheduled | $12/mo, 10 accounts, 500 scheduled | better value for 3+ accounts |
| canva | 5 free designs/mo | $13/mo unlimited | get paid when doing cross-platform visuals |
| bit.ly | 10 links/mo | $8/mo unlimited | free tier enough to start |
| **total to start** | **$0** | | |
| **total when scaling** | **$12-25/mo** | | publer + canva |

---

## reference files

| what | where |
|------|-------|
| general content posting guide | `OPS/CONTENT_POSTING_GUIDE.md` |
| 30-day content calendar (1,008 posts) | `LEDGER/CONTENT_CALENDAR_30DAY.csv` |
| copy style rules | `.claude/rules/copy-style.md` |
| reply bait keywords + DM funnels | `OPS/CONTENT_POSTING_GUIDE.md` (reply bait section) |
| social content files | `CONTENT/social/` (12 subdirectories) |
| CSV source files | `AUTOMATIONS/content_posting/` (3 CSVs) |

---

the content is written. the CSVs exist. the schedule is mapped. the rotation is defined. the engagement protocol is clear. the only thing left is uploading and pressing go. stop reading this guide and go do it.

---

*Disclaimer: Results not typical. Individual results vary based on effort, market conditions, and other factors.*
