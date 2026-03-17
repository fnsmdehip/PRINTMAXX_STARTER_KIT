# Content posting guide: 30-day calendar deployment

**File:** `LEDGER/CONTENT_CALENDAR_30DAY.csv`
**Posts:** 1,008 total (LinkedIn skips weekends)
**Period:** February 3 - March 4, 2026
**Generated:** 2026-02-02

---

## Quick stats

| Metric | Count |
|--------|-------|
| Total posts | 1,008 |
| Faith posts | 336 |
| Fitness posts | 336 |
| Tech/AI posts | 336 |
| Twitter posts | 270 |
| TikTok posts | 270 |
| Instagram posts | 270 |
| LinkedIn posts | 198 (weekdays only) |
| Value posts | 471 (47%) |
| Engagement posts | 303 (30%) |
| Promotion posts | 168 (17%) |
| Personality posts | 66 (6%) |

---

## Accounts

| Niche | Twitter | TikTok | Instagram | LinkedIn |
|-------|---------|--------|-----------|----------|
| Faith | @daily_anchor_faith | @dailyanchorfaith | @dailyanchorfaith | Daily Anchor Faith |
| Fitness | @three_hour_physique | @threehourphysique | @threehourphysique | 3-Hour Physique |
| Tech/AI | @ai_workflows_daily | @aiworkflowsdaily | @aiworkflowsdaily | AI Workflows Daily |

---

## Posting times (EST)

| Platform | Post 1 | Post 2 | Post 3 |
|----------|--------|--------|--------|
| Twitter | 8:00 AM | 12:00 PM | 5:00 PM |
| TikTok | 6:00 AM | 12:00 PM | 9:00 PM |
| Instagram | 9:00 AM | 2:00 PM | 7:00 PM |
| LinkedIn | 7:00 AM | 12:00 PM | 5:00 PM |

---

## Deployment options (fastest to slowest)

### Option 1: Buffer bulk import (10 minutes)

1. Export CSV columns: `date`, `time`, `post_text`, `hashtags`
2. Go to buffer.com > Publishing > Bulk Create
3. Filter CSV by platform (one upload per platform per account)
4. Map columns: Date, Time, Text
5. Append hashtags to post text for each platform
6. Review and schedule

**Buffer CSV format needed:**
```
Date,Time,Text
2026-02-03,08:00,"i prayed for 5 minutes every morning for 90 days... #faith"
```

**Quick filter command:**
```bash
python3 -c "
import csv
platform = 'twitter'  # change per upload
niche = 'faith'       # change per upload
with open('LEDGER/CONTENT_CALENDAR_30DAY.csv') as f:
    reader = csv.DictReader(f)
    rows = [r for r in reader if r['platform'] == platform and r['niche'] == niche]
with open(f'LEDGER/buffer_import_{niche}_{platform}.csv', 'w', newline='') as f:
    w = csv.writer(f)
    w.writerow(['Date', 'Time', 'Text'])
    for r in rows:
        text = r['post_text']
        if r['hashtags']:
            text += '\n\n' + r['hashtags'].replace(',', ' ')
        w.writerow([r['date'], r['time'], text])
print(f'Exported {len(rows)} posts')
"
```

Run 12 times (3 niches x 4 platforms) to get all import files.

### Option 2: Publer bulk upload (15 minutes)

1. Go to publer.io > Bulk Scheduling
2. Upload CSV directly
3. Map columns to Publer fields
4. Set timezone to EST
5. Review calendar view
6. Approve batch

**Publer supports:** Twitter, Instagram, Facebook, LinkedIn, TikTok, Pinterest, Google Business

### Option 3: n8n automated posting (30 minutes setup, then automatic)

If you have n8n running (see `AUTOMATIONS/N8N_SETUP_AND_WORKFLOWS.md`):

1. Import the content calendar workflow
2. Connect platform APIs (X, TikTok, IG, LinkedIn)
3. Workflow reads CSV, posts at scheduled times
4. Set and forget

### Option 4: Manual posting (15-20 min/day)

1. Open CSV in Google Sheets
2. Filter by today's date
3. Sort by time
4. Copy/paste each post to the correct platform at the correct time
5. Mark status as "posted" in the sheet

---

## Content type breakdown

### Value posts (47% of calendar)

Education and alpha insights. Specific numbers, tools, tactics. This is what builds followers.

**Faith examples:** prayer routines with specific stats, bible reading plans, accountability frameworks
**Fitness examples:** training programs, nutrition protocols, supplement stacks with costs
**Tech examples:** AI tool comparisons, platform arbitrage data, automation workflows

### Engagement posts (30% of calendar)

Questions, polls, hot takes, either/or choices. This is what drives algorithm reach.

**Formats used:**
- Binary choices ("A or B?")
- Hot takes ("unpopular opinion:")
- Open questions ("what's your...")
- Confession/vulnerability
- Tag someone

### Promotion posts (17% of calendar)

Products, apps, lead magnets, Gumroad listings. Always value-first, then CTA.

**Products promoted:**
- PrayerLock (faith niche)
- WalkToUnlock (fitness niche)
- PRINTMAXX playbooks (tech niche)
- Gumroad digital products (all niches)
- Newsletters and free resources (all niches)
- Reply-bait lead magnets (all niches)

### Personality posts (6% of calendar)

Build-in-public, behind the scenes, honest updates. This is what builds trust and loyalty.

---

## Platform-specific adaptations

### Twitter
- Posts kept under 280 chars where possible
- 0-1 hashtags (hashtags hurt engagement on X)
- Reply bait CTAs ("reply KEYWORD for...")
- No link previews in promotional posts (kills reach)

### TikTok
- Caption text with #fyp always included
- 3-5 hashtags maximum
- Text posts designed as video script outlines
- Media description column provides visual guidance

### Instagram
- 5-15 hashtags (mix of large/medium/small/niche)
- Niche-specific hashtag bundles auto-appended
- Caption optimized for carousel/image posts
- CTA in caption, not just bio link

### LinkedIn
- Weekdays only (no Saturday/Sunday posts)
- Professional tone maintained
- Minimal hashtags (0-1)
- No casual abbreviations in adapted copy

---

## Reply bait keywords used

These keywords trigger DM funnels or lead magnet delivery:

| Keyword | What they get | Niche |
|---------|---------------|-------|
| PROVERBS | 7-day reading plan | Faith |
| FAST | Beginner fasting guide | Faith |
| JOURNAL | Prayer journal template | Faith |
| CHAIN | Scripture text chain setup | Faith |
| GROUP | Men's community group guide | Faith |
| CHALLENGE | 7-day prayer challenge | Faith |
| MARRIAGE | Couples devotional | Faith |
| EMAIL | Daily Anchor newsletter | Faith |
| SPLIT | 3-day training program | Fitness |
| 5 | 5-exercise full program | Fitness |
| PREP | Weekly meal prep plan | Fitness |
| STRETCH | Post-workout stretching routine | Fitness |
| STACK | Supplement stack guide | Fitness/Tech |
| BODYWEIGHT | 30-day bodyweight program | Fitness |
| TRACKER | Progress tracker spreadsheet | Fitness |
| AUTO | n8n automation workflow | Tech |
| COLD | Cold email setup guide | Tech |
| SEO | SEO/GEO playbook | Tech |
| FUNNEL | Web-to-app funnel playbook | Tech |
| N8N | n8n workflow library | Tech |
| LAUNCH | App launch checklist | Tech |
| ARBITRAGE | Platform arbitrage spreadsheet | Tech |
| ALPHA | Research system guide | Tech |
| NEWSLETTER | AI Workflows newsletter | Tech |
| SYSTEM | PRINTMAXX early access | Tech |

---

## Content rotation logic

10-day repeating cycle, 3 posts per day:

| Day | Post 1 | Post 2 | Post 3 |
|-----|--------|--------|--------|
| 1 | Value | Engagement | Value |
| 2 | Value | Promotion | Engagement |
| 3 | Engagement | Value | Value |
| 4 | Value | Engagement | Promotion |
| 5 | Personality | Value | Engagement |
| 6 | Value | Promotion | Value |
| 7 | Engagement | Value | Engagement |
| 8 | Value | Promotion | Value |
| 9 | Engagement | Value | Personality |
| 10 | Value | Engagement | Promotion |

This achieves approximately 40/30/20/10 split across value/engagement/promotion/personality.

---

## Quality assurance checklist

Before deploying, verify:

- [ ] No em dashes in any post
- [ ] No banned AI vocabulary (leverage, utilize, comprehensive, robust, etc.)
- [ ] All numbers are specific, not vague
- [ ] Lowercase energy maintained (twitter/tiktok)
- [ ] Reply bait keywords are consistent with DM automation setup
- [ ] Product links are live and correct
- [ ] Hashtags are platform-appropriate (not too many for twitter, enough for instagram)
- [ ] LinkedIn posts only on weekdays
- [ ] No duplicate posts on same platform same day

---

## Metrics to track after deployment

| Metric | Target | Tool |
|--------|--------|------|
| Impressions per post | 500+ (week 1), 2K+ (week 4) | Platform analytics |
| Engagement rate | 2%+ (twitter), 5%+ (tiktok) | Platform analytics |
| Reply bait conversion | 3%+ of impressions | Manual count |
| Follower growth | 100+/week per account | Platform analytics |
| Link clicks | 50+/week per account | Bit.ly or UTM tracking |
| Newsletter signups | 10+/week per niche | Beehiiv dashboard |

---

## Regeneration

To regenerate with updated content:

```bash
python3 scripts/generate_30day_calendar.py
```

Edit the content banks in `scripts/generate_30day_calendar.py` to add new posts, update alpha references, or adjust the content mix ratios.


    ---

    ## Pending Enhancement (ALPHA1233, Score: 20)

    **Source:** 2026-02-13 | **URL:** @maverickecom
    **Added:** 2026-02-18T06:49:18-05:00

    How I made $34k gmv in just 5 minutes: 

Tiktok Shop is actually easy if brands are using my system.

It’s literally plug and play once brands are working with the proper fit creators 

High GMV creators with product in hand are getting insane results

Best part is brands aren’t



    ---

    ## Pending Enhancement (ALPHA1335, Score: 28)

    **Source:** 2026-02-13 | **URL:** @alexcooldev
    **Added:** 2026-02-18T06:49:18-05:00

    It took me 2 months to hit my first $100 MRR.

Nobody cared. It felt slow, painful, I almost quit.

Then suddenly…
It only took a few days to reach $1,000 MRR (after one video went viral)

Early stages aren’t about making $$
They’re about learning, iterating, and finding the



    ---

    ## Pending Enhancement (ALPHA1421, Score: 32)

    **Source:** 2026-02-13 | **URL:** r/EntrepreneurRideAlong
    **Added:** 2026-02-18T06:49:18-05:00

    We really are living in a strange golden age of technology I’m an indie dev and one of my small side projects (simple calorie + habit tracking mobile app) just crossed $850 MRR. That number isn’t impressive by startup-Twitter standards, but it covers my devops costs, AI tools, and about half of my car payment. More importantly, it’s stable and still growing month over month.   

What surprised m



    ---

    ## Pending Enhancement (ALPHA1428, Score: 30)

    **Source:** 2026-02-13 | **URL:** r/EntrepreneurRideAlong
    **Added:** 2026-02-18T06:49:18-05:00

    Made $1300 with my SaaS in 28 days. Here's what worked and what didn't First UP, I didn't went from idea to $1300 in 28 days.

For the first three months I didn't knew that you have to market your product too.

I just kept building.

Then when I had 0 users after having a brutally failed PH launch.

I just went down on researching on how apps really grow from "0"

Watched endless starter story vid



    ---

    ## Pending Enhancement (ALPHA1460, Score: 26)

    **Source:** 2026-02-13 | **URL:** r/AppBusiness
    **Added:** 2026-02-18T06:49:18-05:00

    Built a fitness app that converts videos into workout routines. Made $300 in first month. This started as a personal frustration.

I save tons of workout reels on Instagram/TikTok but when I’m at the gym, they’re basically useless — buried in a messy “Saved” folder and impossible to find again.

I wanted a way to turn those short clips into actual workouts I can follow.

So I built an app:

	•	Pas



    ---

    ## Pending Enhancement (ALPHA1553, Score: 20)

    **Source:** 2026-02-13 | **URL:** r/affiliatemarketing
    **Added:** 2026-02-18T06:49:18-05:00

    Help, looking for advice Hey everyone, I’m writing this honestly looking for some guidance, but also to get things off my chest.

I’ve been doing affiliate marketing for about two years, in the fragrance niche. I’m a content creator on Instagram and over time I built an audience there. That audience helped me land a strong affiliate partnership with a Canadian site.

For a period of time, that inc



---

## Pending Enhancement (ALPHA1648, Score: 20)

**Source:** 2026-02-13 | **URL:** r/micro_saas
**Added:** 2026-02-18T07:12:19-05:00

I built a tool that allows you to find your next customer on Reddit in seconds here's how it works:

1. describe your ideal customer profile

2. analyzes thousands of reddit posts instantly

3. get a list of people ready to buy your product right now with buying intent 

the result is leads with metrics like activity score, comments and posts relating to your problem, engagement rate, and a bunch 



---

## Pending Enhancement (ALPHA1725, Score: 20)

**Source:** 2026-02-13 | **URL:** r/SaaS
**Added:** 2026-02-18T07:12:19-05:00

How to actually use programmatic SEO Let me clear up one big misunderstanding about programmatic SEO. It's not about churning out lots and lots of poorly written content. It's about creating content that can answer almost all questions a person could have about a topic at a very high scale.

For every search query, Google has to judge millions of pages.  
But if a few sites have worked out the top



---

## Pending Enhancement (ALPHA1737, Score: 34)

**Source:** 2026-02-13 | **URL:** r/growthhacking
**Added:** 2026-02-18T07:12:19-05:00

Growth hack that's not sexy but works 
Everyone wants the viral growth hack that 10x's their traffic overnight. Tried all the sexy tactics first. Product Hunt launch, viral Twitter threads, Reddit posting, influencer outreach. Got some spikes but nothing sustainable. The problem with sexy growth hacks is they produce one-time results. You get a spike, then you're back to grinding for the next spik



---

## Pending Enhancement (ALPHA1760, Score: 46)

**Source:** 2026-02-13 | **URL:** r/passive_income
**Added:** 2026-02-18T07:12:19-05:00

My Facebook Page Stats for this month 🎥 I have 116K followers so far. I create random funny, cute, and shocking content using Sora and Kling.

I have been earning an extra $1000+ a month for 3 months now.

I have a VA to make it more passive but I enjoy the video creation process.

You can turn AI slop into gold 💛

Edit Update: Wow! Got a lot of engagement. My AI playbooks used to be $27 but now i



---

## Pending Enhancement (ALPHA1762, Score: 24)

**Source:** 2026-02-13 | **URL:** r/passive_income
**Added:** 2026-02-18T07:12:19-05:00

Facebook content monetization (day 2) It’s about 6pm on day 2 of being content monetized on facebook for a page that posts ai videos and it looks like by midnight I’ll be at like $1000 for the day. That’s $30,000 a month just to spend a hour a day making ai videos it’s amazing if you’re not doing this your crazy 

Don’t sleep on making ai videos the platforms are paying



---

## Pending Enhancement (ALPHA6552, Score: 32)

**Source:** r/SaaS (https://reddit.com/r/SaaS/comments/1r692k3/built_my_saas_to_132k_arr_and_i_didnt_write_a/) | **URL:** 
**Added:** 2026-02-18T07:12:19-05:00

Built my SaaS to $132K ARR and I didn't write a single line of code. I built a SaaS that hit $132K ARR. The whole thing was built by offshore developers I hired and managed myself

I want to break down what actually worked for growth, what didn't, and the one decision



---

## Pending Enhancement (ALPHA6555, Score: 24)

**Source:** r/Entrepreneur (https://reddit.com/r/Entrepreneur/comments/1r68krd/what_i_learned_going_from_0_to_350k_in_2025_with/) | **URL:** 
**Added:** 2026-02-18T07:12:19-05:00

what i learned going from $0 to $350k+ in 2025 with a side project (and already $50k+ in jan 2026). Hello! been lurking here forever and recently decided to get more active. figured i'd actually contribute something instead of just absorbing everyone else's post-mortems at 2am.

I run my own sort of



---

## Pending Enhancement (ALPHA6615, Score: 36)

**Source:** r/Entrepreneur (https://reddit.com/r/Entrepreneur/comments/1r6t3nt/should_i_monetize_at_35_usersday_or_wait_until/) | **URL:** 
**Added:** 2026-02-18T07:12:19-05:00

Should I monetize at 35 users/day or wait until 1k/day?. Built a free web tool (video downloader). Day 5.



Every competitor monetizes immediately with ads. I'm holding off.



Current situation:

\- 35 users/day organic

\- $0 revenue

\- Could add ads →



---

## Pending Enhancement (ALPHA6616, Score: 30)

**Source:** r/EntrepreneurRideAlong (https://reddit.com/r/EntrepreneurRideAlong/comments/1r6non3/week_1_of_building_a_multiplatform_content/) | **URL:** 
**Added:** 2026-02-18T07:12:19-05:00

Week 1 of building a multi-platform content business with AI — $30 spent, 0 revenue, but infrastructure is done. Sharing my ride along since I'm documenting everything as I go.

The hypothesis: AI tools have gotten cheap enough that one person can run a multi-channel content operation that used to require a smal



---

## Pending Enhancement (ALPHA7844, Score: 24)

**Source:** r/SideProject (https://reddit.com/r/SideProject/comments/1r73vcr/unpopular_opinion_most_side_projects_fail_because/) | **URL:** 
**Added:** 2026-02-18T07:12:19-05:00

unpopular opinion: most side projects fail because founders build what's interesting, not what's painful. scroll this sub on any day. 10+ launches following the same path: founder has cool idea → builds for 2-4 weeks → posts "i built X" → 15 upvotes → dies in 3 months.

meanwhile the boring stuff — invoic



---

## Pending Enhancement (ALPHA7851, Score: 32)

**Source:** r/SaaS (https://reddit.com/r/SaaS/comments/1r75ag8/built_marketplace_9_months_got_8_users_rebuilt/) | **URL:** 
**Added:** 2026-02-18T07:12:19-05:00

Built marketplace 9 months. Got 8 users. Rebuilt simple tool. 8K MRR in 5 months.. Started two-sided marketplace April 2025 connecting freelance developers with small agencies. Validated through fifty-three interviews. Everyone said they would use it. Spent nine months building matc



---

## Pending Enhancement (ALPHA7951, Score: 30)

**Source:** r/EntrepreneurRideAlong (https://reddit.com/r/EntrepreneurRideAlong/comments/1r7l7f8/the_most_profitable_automation_ive_built_was/) | **URL:** 
**Added:** 2026-02-18T07:12:19-05:00

The most profitable automation I’ve built was embarrassingly simple ($10k+). So, I was working with this small clinic recently. They were drowning in paperwork and endless email threads. Every. Single. Day. They spent hours copying and pasting patient information into document



---

## Pending Enhancement (ALPHA8070, Score: 24)

**Source:** r/Affiliatemarketing (https://reddit.com/r/Affiliatemarketing/comments/1r7wsiu/31kmo_with_affiliate_after_6_years_of_failing/) | **URL:** 
**Added:** 2026-02-18T07:12:19-05:00

$3.1K/mo with affiliate after 6 years of failing. Ok fellas heres everything I know about affiliate marketing after failing for 6y and now making over $3k recurring doing this in spare time after work

First rule.

The early bird gets the worm. If an



---

## Pending Enhancement (ALPHA8076, Score: 26)

**Source:** r/webdev (https://reddit.com/r/webdev/comments/1r7m5mu/over_260k_people_installed_fake_ai_assistant/) | **URL:** 
**Added:** 2026-02-18T07:12:19-05:00

Over 260k people installed fake AI assistant Chrome extensions that steal your data. saw research on 30 Chrome extensions posing as ChatGPT, Claude, Gemini helpers that actually exfiltrate your data.

They use remote iframes to bypass Web Store reviews and can silently update behavior



---

## Pending Enhancement (ALPHA8375, Score: 31)

**Source:** @unknown (bookmark) | **URL:** https://x.com/unknown/status/2021220354459566594
**Added:** 2026-02-18T08:39:34-05:00

you can become a MILLIONAIRE in under 50 days

- make such a website 
- start creating content around it
- go viral, and collect dollars 

website in this video; edugames dot uz https://t.co/ke3fwFOtPr



---

## Pending Enhancement (ALPHA8385, Score: 55)

**Source:** @unknown (bookmark) | **URL:** https://x.com/unknown/status/2021282530826113422
**Added:** 2026-02-18T08:39:34-05:00

LINKEDIN DOESN'T WANT YOU KNOWING THIS

but you can legally scrape your competitor's entire audience

client showed me his setup:

METHOD 1: viral post scraping
- finds competitor post (2,400 comments)
- scrapes all commenters
- filters VP+ at $20M+ companies (680 qualified)
-



---

## Pending Enhancement (ALPHA8397, Score: 36)

**Source:** @unknown (bookmark) | **URL:** https://x.com/unknown/status/2020973482314485991
**Added:** 2026-02-18T08:39:34-05:00

21 million views across the first three posts

this is how you dominate with ai content in 2026 https://t.co/hMS7qvZ0mV



---

## Pending Enhancement (ALPHA8400, Score: 52)

**Source:** @unknown (bookmark) | **URL:** https://x.com/unknown/status/2020950338006597700
**Added:** 2026-02-18T08:39:34-05:00

Why successful apps run hundreds of Facebook ads:

CalAI: 500 active ads
Learna: 700 active ads
Lazy Fit: 640 active ads

They're not running this content because it's unprofitable.

They've maximized their LTV by pushing yearly plans.

CalAI collects $30 upfront after 3 days.



---

## Pending Enhancement (ALPHA8416, Score: 26)

**Source:** r/webdev | **URL:** https://reddit.com/r/webdev/comments/1r7m5mu/over_260k_people_installed_fake_ai_assistant/
**Added:** 2026-02-18T08:45:14-05:00

[r/webdev] Over 260k people installed fake AI assistant Chrome extensions that steal your data



---

## Pending Enhancement (ALPHA8644, Score: 30)

**Source:** r/passive_income | **URL:** https://reddit.com/r/passive_income/comments/1r7ukdd/so_hyped_my_life_simulation_app_brought_in_1k_in/
**Added:** 2026-02-18T08:45:14-05:00

[r/passive_income] So hyped! My life simulation app brought in $1k in it's first month 📈📈



---

## Pending Enhancement (ALPHA8650, Score: 20)

**Source:** r/NewTubers | **URL:** https://reddit.com/r/NewTubers/comments/1r7z22d/earn_my_first_1000_subs_in_only_one_month/
**Added:** 2026-02-18T08:45:15-05:00

[r/NewTubers] Earn My First 1000 Subs In Only One Month



---

## Pending Enhancement (ALPHA8700, Score: 26)

**Source:** r/Affiliatemarketing | **URL:** https://reddit.com/r/Affiliatemarketing/comments/1r77ljz/how_we_dropped_bounce_rate_by_5_and_lifted/
**Added:** 2026-02-18T08:45:21-05:00

[r/Affiliatemarketing] How We Dropped Bounce Rate by 5% and Lifted Engagement by 6%



---

## Pending Enhancement (ALPHA8727, Score: 22)

**Source:** r/socialmedia | **URL:** https://reddit.com/r/socialmedia/comments/1r6ynsl/what_most_people_get_wrong_about_the_linkedin/
**Added:** 2026-02-18T08:45:21-05:00

[r/socialmedia] What Most People Get Wrong About the LinkedIn Algorithm



---

## Pending Enhancement (ALPHA8121, Score: 32)

**Source:** @knoxtwts (high-signal-accounts) | **URL:** https://x.com/knoxtwts/status/2024093805331226733
**Added:** 2026-02-18T08:54:05-05:00

scrape 100 pages in your niche. calculate views divided by account median on every post. 

anything hitting 100x that number is your template. extract the hook. make it more extreme. 

post across 30 accounts. find the next outlier. repeat. 

this is how the faceless pages with



---

## Pending Enhancement (ALPHA8222, Score: 22)

**Source:** @WatcherGuru (high-signal-accounts) | **URL:** https://x.com/WatcherGuru/status/2023209835181834666
**Added:** 2026-02-18T08:54:13-05:00

YouTuber Logan Paul purchased this NFT for $635,000 in 2021. 

Today, it's worth $155.



---

## Pending Enhancement (ALPHA8396, Score: 20)

**Source:** @yegormethod (high-signal-accounts) | **URL:** https://x.com/yegormethod/status/2022736958770848087
**Added:** 2026-02-18T08:54:24-05:00

A 48 year old man who injects his son's plasma just got 1,566 millionaires to apply for a $1,000,000/yr health subscription

The same health advice he literally gives away for free on YouTube....

I thought it was the dumbest business model I'd ever seen until I mapped what's



---

## Pending Enhancement (ALPHA8409, Score: 22)

**Source:** @KCodes7777 (high-signal-accounts) | **URL:** https://x.com/KCodes7777/status/2023556926655594764
**Added:** 2026-02-18T08:54:24-05:00

As promised.
Built a focus timer app in under 60 minutes.

Target audience?

→ StudyTok
→ “study with me” accounts
→ Productivity addicts

There are thousands of these accounts on TikTok + IG.

One example video (below) got 900K+ views.

Video structure:

→ Sound: “control



---

## Pending Enhancement (ALPHA12318, Score: 24)

**Source:** r/EntrepreneurRideAlong (https://reddit.com/r/EntrepreneurRideAlong/comments/1rcp3hf/would_you_pay_20mo_to_stop_hunting_for_leads_and/) | **URL:** 
**Added:** 2026-02-24T06:00:02-05:00

Would you pay $20/mo to stop "hunting" for leads and just have them delivered to your inbox?. Hey everyone,

Like most devs here, I love building but absolutely loathe "sales." Specifically, I hate spending hours on Reddit and HN trying to find that one person asking for a tool like mine, only



---

## Pending Enhancement (ALPHA12340, Score: 24)

**Source:** r/ecommerce (https://reddit.com/r/ecommerce/comments/1rczz24/those_of_you_making_product_videos_what_are_you/) | **URL:** 
**Added:** 2026-02-24T06:00:02-05:00

Those of you making product videos - what are you spending per video and is it worth it?. I run a small DTC brand with about 40 SKUs. Last year I was paying freelance videographers $300-500 per product video for social media and listings. It added up to over $4K for the year.

This year I



---

## Pending Enhancement (ALPHA13172, Score: 30)

**Source:** r/EntrepreneurRideAlong (https://reddit.com/r/EntrepreneurRideAlong/comments/1rdeqiw/how_to_negotiate_when_youve_never_sold_a_business/) | **URL:** 
**Added:** 2026-02-27T19:47:25-05:00

how to negotiate when you've never sold a business before. a guy lost probably $180k on the table because he didn't google the buyer

at this point I keep seeing that first time sellers don't research who they're selling to.

Like at all. They'll spend months



---

## Pending Enhancement (ALPHA13299, Score: 24)

**Source:** r/ecommerce (https://reddit.com/r/ecommerce/comments/1reb0k4/my_gf_is_launching_a_beauty_brand_with_50k_am_i/) | **URL:** 
**Added:** 2026-02-27T19:47:26-05:00

My GF is launching a beauty brand with $50k. Am I being supportive or letting her walk into a trap?. She wants to focus on mid-to-low priced beauty products targeting women 18–40 in Southeast Asia. She’s always been into beauty, follows TikTok trends, ingredient breakdowns, that kind of stuff. This i



---

## Pending Enhancement (ALPHA13305, Score: 30)

**Source:** r/SaaS (https://reddit.com/r/SaaS/comments/1re3ynv/how_do_you_actually_grow_your_early_saas_business/) | **URL:** 
**Added:** 2026-02-27T19:47:26-05:00

How do you actually grow your early SaaS business without paying $500+ on ads?. I'm 18 inexperienced launching my first SaaS (Leben AI) and trying to figure out how to actually get conversions because I don't want to be spending hundreds of dollars on ad spend right away and want



---

## Pending Enhancement (ALPHA13369, Score: 24)

**Source:** ProductHunt | **URL:** https://www.producthunt.com/products/fellow-app
**Added:** 2026-02-27T19:47:26-05:00

[PH LAUNCH] Ask Fellow: Automate post-meeting actions from documentation to emails



---

## Pending Enhancement (ALPHA13416, Score: 24)

**Source:** r/indiehackers (https://reddit.com/r/indiehackers/comments/1ren341/launched_a_pet_sitter_marketplace_that_doesnt/) | **URL:** 
**Added:** 2026-02-27T19:47:26-05:00

Launched a pet sitter marketplace that doesnt take a cut from bookings. Sitter Rank launched on PH today. Its a platform where pet sitters keep 100% of their booking income instead of losing 20-40% to Rover/Wag.

Revenue model is SaaS subscriptions from sitters (free tier



---

## Pending Enhancement (ALPHA13453, Score: 26)

**Source:** r/SideProject (https://reddit.com/r/SideProject/comments/1rfczi7/10_users_in_10_days_honest_breakdown/) | **URL:** 
**Added:** 2026-02-27T19:47:26-05:00

10 users in 10 days - honest breakdown. Launched FluoTest 10 days ago. Free quiz tool for lead qualification.

Had a post hit #1 on r/SaaS. Felt amazing.

But viral posts ≠ users. Direct outreach does.

What surprised me:

	∙	People don’t w



---

## Pending Enhancement (ALPHA13615, Score: 36)

**Source:** r/SaaS (https://reddit.com/r/SaaS/comments/1rfzxpq/earlystage_saas_teams_are_you_paying_for_postman/) | **URL:** 
**Added:** 2026-02-27T19:47:26-05:00

Early-stage SaaS teams - are you paying for Postman now?. We’re pre-revenue and the new pricing change (1-user Free limit) makes it hard to justify $20/month per developer.

I understand monetization, but API testing tools used to be easy to collaborate with

---

## Alpha Insights (Auto-Appended)

_Insights auto-appended by playbook_enhancer.py. Review and integrate as needed._

### Alpha Insight: ALPHA543 — 2026-02-28
**Source:** Buffer / TokChart ([link](https://buffer.com/resources/trending-songs-tiktok/))
**Category:** CONTENT_FORMAT
**Method:** No-talking trends perfect for faceless accounts. Bridgerton for product showcases. Check tokchart.com daily.
**Insight:** Feb 2026 TikTok sounds: ZOMB (IG-vs-reality). No-talking: No Hands + Euphoria glam + Group Consensus + Thermostat Game. Bridgerton for products.
**Potential:** ROI: HIGH | Synergy: 75



---

## Pending Enhancement (ALPHA13743, Score: 24)

**Source:** @marryevan999 (bookmarks) | **URL:** https://x.com/marryevan999/status/2025966737037152679
**Added:** 2026-02-28T06:00:01-05:00

Faceless Instagram pages will be the biggest side hustle in 2026:

• Can be made with AI in 1 day
• Only requires 1-2 hours a week
• Can rinse & repeat as many times

If you want to make $10k/month in passive income…

Follow these 7 simple steps:

### Alpha Insight: ALPHA1351 — 2026-03-01
**Source:** 2026-02-13
**Category:** CONTENT_FORMAT
**Insight:** the top 2 TikTok shop affiliates made $810k in 35 days, COMMISSION orangeshoppin & cakedfinds i built an agent to clone their videos with AI and pump out 300+ per day should not give this away for free, but f*k it Like, rt & comment “CLONE” i’ll send you the template i built
**Potential:** ROI: https://x.com/Jonnyvandel/status/2014436022621282486 | Synergy: 385



---

## Pending Enhancement (ALPHA14232, Score: 46)

**Source:** @dansugcmodels (daily scraper) | **URL:** https://x.com/dansugcmodels/status/1986470873096986958
**Added:** 2026-03-02T19:45:22-05:00

I analyzed 10,000 Jenni AI tiktok viral videos and found top 5 emotions that generate 80% of the views:

> confused
> frustrated
> struggling
> “whaaaat?”
> tired in bed

They’re easy to capture: 5–7 seconds, a clear hook, filmed on your phone, no script needed.

The real bottleneck is finding reliable UGC creators at scale. its costly, inconsistent, and slow to deliver.

I’ve bundled 100 human UG



---

## Pending Enhancement (ALPHA14252, Score: 30)

**Source:** @knoxtwts (daily scraper) | **URL:** https://x.com/knoxtwts/status/1984628980335480979
**Added:** 2026-03-02T19:45:22-05:00

most evil info product i've seen this year:

a “21-day confidence bootcamp to make her chase you”

tiktok ads targeting men with 0 dating experience

landing page opens with:

“she’s not ignoring you because she’s busy - she just doesn’t respect you.”

“you can fix that in 3 weeks.”

they scroll in silence questioning their whole existence

offer: $67 bootcamp + $49/mo “alpha group chat”

every li



---

## Pending Enhancement (ALPHA14254, Score: 54)

**Source:** @knoxtwts (daily scraper) | **URL:** https://x.com/knoxtwts/status/1989356178992664976
**Added:** 2026-03-02T19:45:22-05:00

most genius b2b info product hack i've seen this year: 

guy was stuck at $2k/month selling $97 community access 

everyone told him he needed more content, bigger audience, better marketing, viral growth 

he ignored all of it 

just: repositioned same product as infrastructure, not education, changed from "learn" to "install working infrastructure", raised price to $1997 

multiple 5-figs first 



---

## Pending Enhancement (ALPHA14305, Score: 30)

**Source:** @Hightrafficsite (daily scraper) | **URL:** https://x.com/Hightrafficsite/status/1664517988274561025
**Added:** 2026-03-02T19:45:22-05:00

This Simple DR 6 site earned more than $4000 in 7 months with just 70 articles.

Niche - Food - Cake
Monetization - Adthrive
What They Did - Listed cake prices from several food outlets and Left it and dint update content for Years 

Some Interesting Facts



---

## Pending Enhancement (ALPHA14309, Score: 36)

**Source:** @Hightrafficsite (daily scraper) | **URL:** https://x.com/Hightrafficsite/status/1722219052444356815
**Added:** 2026-03-02T19:45:22-05:00

 This is Big 

 This single page website earns $5000 to $7000 a month from affiliates 

How about creating a  website similar to the look of Google Sheets as a homepage and listing 100s of product info and linking to affiliates?

It is as simple as this.
Niche - Computer Parts
Monetisation  - Amazon Affiliates
Traffic - 86.5k (Similar Web Data)
Gets traffic from forums, social media etc
No Blog
No



---

## Pending Enhancement (ALPHA14312, Score: 44)

**Source:** @iamgdsa (daily scraper) | **URL:** https://x.com/iamgdsa/status/1907068912308719644
**Added:** 2026-03-02T19:45:22-05:00

POV Camera does $150k mrr.

11 TikTok accounts. 67M views. 3 hooks.

Repeating the exact same format scheme (full AI avatars).

Never seen anything like this:



---

## Pending Enhancement (ALPHA14321, Score: 24)

**Source:** @jasoncfox (daily scraper) | **URL:** https://x.com/jasoncfox/status/1975175468757197156
**Added:** 2026-03-02T19:45:28-05:00

My first 5 clients came from the simplest DM

My first $500k came from a simple DM and content

My first $1m came from a simple DM, Content and Sales process

Nothing complicated and nothing over the top

I just filmed a training breaking down 7 of my best DMs that worked through all of these stages

If you want it drop 'DM' below and I'll shoot it over (Must be following)



---

## Pending Enhancement (ALPHA14352, Score: 24)

**Source:** @yegormethod (daily scraper) | **URL:** https://x.com/yegormethod/status/1965430067208544467
**Added:** 2026-03-02T19:45:28-05:00

There’s a guy in your city who woke up at 4am, hit the gym for two hours, and will make $30,000 before you finish your first cup of coffee.

You've never met him. You've never seen his posts.
He doesn't have a "personal brand."

He's not tweeting "rise and grind" from his iPhone.
He's on a burner phone closing a deal that would change your family's life.

He's not making a vision board.
He's revie



---

## Pending Enhancement (ALPHA14770, Score: 24)

**Source:** r/SaaS (https://reddit.com/r/SaaS/comments/1ri0b9m/i_made_176_in_my_first_month_as_a_solo_founder/) | **URL:** 
**Added:** 2026-03-02T19:47:14-05:00

I made $176 in my first month as a solo founder. Here's every channel I tried and what actually converted.. I set a goal to make 1 sale by end of February. Got 4. $176 total across 2 products ($39 distribution framework + $59 Nuxt boilerplate).

I'm a software engineer building on the side after my 9-5 in R

### Alpha Insight: ALPHA1578 — 2026-03-05
**Source:** 2026-02-13
**Category:** CONTENT_FORMAT
**Insight:** I audited 500+ Instagram accounts in late 2025. Here is what is actually working vs what isn't. Everyone keeps screaming "just post more Reels," but after auditing over 500 accounts in the last 3 months (mix of E-com, Personal Brands, and Local Biz), the data is painting a slightly different picture. I wanted to share the raw trends we’re seeing across our client accounts so you can stop guessing. 1. Carousels are the new "Save" magnets For accounts under 10k followers, Carousels are currently
**Potential:** ROI: https://reddit.com/r/SocialMediaMarketing/comments/1qypdu1/i_audited_500_instagram_accounts_in_late_2025/ | Synergy: 140



---

## Pending Enhancement (ALPHA14930, Score: 24)

**Source:** @affprinter (explicit-handles) | **URL:** https://x.com/affprinter/status/2028375214476890620
**Added:** 2026-03-05T05:36:13-05:00

Tiktok organic + affiliate sweep offers = easiest way to make $7k/week

its so simple but people just dont have the right guidance

so I made a free guide for you guys so you can print $20k/months

Just comment "sweeps" and retweet and ill send it over (must follow for auto dm)



---

## Pending Enhancement (ALPHA14934, Score: 24)

**Source:** @StevenCravotta (explicit-handles) | **URL:** https://x.com/StevenCravotta/status/2028560487219163469
**Added:** 2026-03-05T05:36:13-05:00

The only time you are allowed to hard sell on TikTok:

Reply videos.

I'm stealing the traffic from my own viral video.

One reply video got 6,000 likes and 100,000 views with a hard sales pitch.



---

## Pending Enhancement (ALPHA15135, Score: 20)

**Source:** @SimonasDip (explicit-handles) | **URL:** https://x.com/SimonasDip/status/2028467439084687734
**Added:** 2026-03-05T06:24:45-05:00

scaled 300+ tiktok accounts to hit us audiences without getting banned

the secret isn't content

it's making tiktok think your account is real before you post anything

here are 3 automated methods that actually work

method 1: native auto scroll

some accounts get this by



---

## Pending Enhancement (ALPHA15460, Score: 22)

**Source:** @wesocialgrowth (high-signal-accounts) | **URL:** https://x.com/wesocialgrowth/status/2029240572855435375
**Added:** 2026-03-05T21:57:27-05:00

Here's how to turn your views into leads:

22 engagement farming hacks for TikTok/ Reels



---

## Pending Enhancement (ALPHA15848, Score: 56)

**Source:** @alexxgrowth (daily scraper) | **URL:** https://x.com/alexxgrowth/status/1970847940823400467
**Added:** 2026-03-06T23:00:01-05:00

autistic content hack:

sharing YOUR LOSSES makes more money than sharing wins

i told my clippers to post two identical product launches:

version A:
"made $100k this month!"

version B:
"lost $30k but learned this..."

version A:
123k views, 13 sales

version B:
5.4M views, 1450 sales

losing stories convert 49x better

here's the psychology:

winners create distance

but



---

## Pending Enhancement (ALPHA15857, Score: 30)

**Source:** @fromzerotomill (daily scraper) | **URL:** https://x.com/fromzerotomill/status/1921895790206730369
**Added:** 2026-03-06T23:00:01-05:00

There’s a guy in Romania

Runs a faceless AI +18 disney IG profiles

Auto-generates content with Midjourney + GPT

Voice with ElevenLabs

$300K/month

Zero human contact

Just ChatGPT, Stripe, and a MacBook

Reply w/'AI' and ill send you guide on how to do it



---

## Pending Enhancement (ALPHA15906, Score: 37)

**Source:** @mikey_starts (bookmarks) | **URL:** https://x.com/mikey_starts/status/2028516389590368583
**Added:** 2026-03-06T23:00:01-05:00

2026 guide to >$100M exit

> target niche dominated by slow incumbents
> rebuild core feature AI-first
> hire 100s of gen z students to run ambassador accounts
> copy most viral formats every single week
> cross-post to Tiktok, IG, YT & Facebook
> pay based on performance and not



---

## Pending Enhancement (ALPHA16293, Score: 26)

**Source:** @espindeezy (daily scraper) | **URL:** https://x.com/espindeezy/status/1846270665529467248
**Added:** 2026-03-07T00:25:43-05:00

I made 39k in the last 7 days with TikTok Shop

How?

By not reinventing the wheel.

My video took inspiration from another creator inside 
@creatorscorner0
 who went mega viral with the same product

And guess what? HIS video had taken inspiration from one of MY viral videos 

And you guessed it… that video was inspired by another creator inside our group. 

You’ll get 10x better re



---

## Pending Enhancement (ALPHA16300, Score: 32)

**Source:** @SimonasDip (daily scraper) | **URL:** https://x.com/SimonasDip/status/1974156805379969399
**Added:** 2026-03-07T00:25:44-05:00

All methods to target US audience on TikTok (ranked from least to most reliable)

1. VPN + US SIM card + restored phone + proxies
Basically pretend you’re in the US by wiping a phone, inserting a US SIM, running VPN/proxy.

 Pros: Cheapest DIY hack if you’re techy.
 Cons: VPNs get flagged, proxies break, SIMs cost money. Accounts often stop hitting the US feed after a while.

Reliability s



---

## Pending Enhancement (ALPHA16401, Score: 38)

**Source:** IndieHackers | **URL:** https://www.indiehackers.com/product/sumoclip
**Added:** 2026-03-07T00:41:17-05:00

Turn long videos into viral clips in minutes. $3.5k/mo March 2026. Repurposing workflow tool for content creators. Growing category.



---

## Pending Enhancement (ALPHA16409, Score: 35)

**Source:** IndieHackers | **URL:** https://www.indiehackers.com/product/wordy
**Added:** 2026-03-07T00:41:17-05:00

Learn languages by watching movies and TV shows. $20k/mo 2026. Entertainment-education crossover niche. Works on existing Netflix/streaming behavior.



---

## Pending Enhancement (ALPHA16369, Score: 36)

**Source:** @maverickecom (high-signal-accounts) | **URL:** https://x.com/maverickecom/status/2030054690969321752
**Added:** 2026-03-07T02:16:23-05:00

We launched a 7 figure Amazon brand on tiktok shop and did $20k with human UGC creators this week

Good team and good systems >

Takeaway:

- launch with human UGC. We use plug and play method to connect brands to high GMV creators in a mix of low retainers and commission only

-



---

## Pending Enhancement (ALPHA16383, Score: 24)

**Source:** @wesocialgrowth (high-signal-accounts) | **URL:** https://x.com/themariaines/status/2029865730016170449
**Added:** 2026-03-07T02:16:23-05:00

This crazy TikTok trend from December is soooo back

> 113.8 MILLION views
> 19.4 million likes
> 1.5 million bookmarks
> 238,400 comments



---

## Pending Enhancement (ALPHA16967, Score: 26)

**Source:** @wannercashcow (high-signal-accounts) | **URL:** https://x.com/wannercashcow/status/2029376379155018201
**Added:** 2026-03-07T07:18:48-05:00

I went from $0 to $522K in a single month with faceless YouTube

Over $8 million total generated across all my channels

Here's the full story (wins, losses, and lessons) 



---

## Pending Enhancement (ALPHA16981, Score: 24)

**Source:** @Jahjiren (high-signal-accounts) | **URL:** https://x.com/Jahjiren/status/2029711455273025755
**Added:** 2026-03-07T07:18:48-05:00

Seasonal apps could be a huge money grab
but only if done correctly 

Some UV Index apps make $10k+/mo

Spring break and summer are 
around the corner

Building this in 3 days then mass distributing 
could be the method

4 TikTok’s & reels a day
across 6 TikTok/IG accounts
using



---

## Pending Enhancement (ALPHA16991, Score: 29)

**Source:** @yegormethod (high-signal-accounts) | **URL:** https://x.com/yegormethod/status/2030015816637313114
**Added:** 2026-03-07T07:18:48-05:00

I'm going to drop some crazy sauce for anyone selling an offer over $1000:

Every B2B founder wants predictable client acquisition...

but they spend 99% of their time and budget advertising on tiktok & instagram

The person who can authorize 10k-50k has never once in their life



---

## Pending Enhancement (ALPHA17139, Score: 20)

**Source:** @franci__ugc (high-signal-accounts) | **URL:** https://x.com/franci__ugc/status/2018342418886590717
**Added:** 2026-03-07T09:48:10-05:00

tiktok's 2026 algorithm change nobody's talking about:

"comment part 2" replies now get 4x the initial push of fresh posts.

why? it signals conversation. algorithm sees engagement loop.

your workflow should be:
1. post video
2. wait for comments
3. reply to best comment with



---

## Pending Enhancement (ALPHA17164, Score: 24)

**Source:** @simonecanciello (high-signal-accounts) | **URL:** https://x.com/simonecanciello/status/2029997643858903132
**Added:** 2026-03-07T10:14:56-05:00

you can just build a $39.99/year alarm app and post this faceless format in bulk.

i’d build a niche one, still untapped.



---

## Pending Enhancement (ALPHA17171, Score: 24)

**Source:** @simonecanciello (high-signal-accounts) | **URL:** https://x.com/simonecanciello/status/2029230665212834264
**Added:** 2026-03-07T10:14:56-05:00

you can create a $59.99/year tanning app and post these shorts in bulk.

summer is coming, don’t miss this.



---

## Pending Enhancement (ALPHA17250, Score: 23)

**Source:** @wannercashcow (high-signal-accounts) | **URL:** https://x.com/wannercashcow/status/2030267221876846957
**Added:** 2026-03-07T10:14:56-05:00

Check out this valuable interview with our student Eric where we leaked his channel that made him $17K+ in ONE month

And if you want to scale your own faceless channel to $10K+/month, then book a free discovery call here: 
http://
join.wannercashcow.com/74807ae3



---

## Pending Enhancement (ALPHA17294, Score: 22)

**Source:** @wesocialgrowth (high-signal-accounts) | **URL:** https://x.com/wesocialgrowth/status/2030282350169629072
**Added:** 2026-03-07T10:44:04-05:00

We looked at the all-time best content from 40+ consumer apps.

The videos that measurably drove downloads and revenue.

Then, we compile the top 3 and turned into The TikTok Hall of Fame.

> 120+ viral videos
> formats
> hook structures

Complete with engagement data and revenue



---

## Pending Enhancement (ALPHA17479, Score: 26)

**Source:** @alexcooldev (high-signal-accounts) | **URL:** https://x.com/alexcooldev/status/2030300530506145989
**Added:** 2026-03-07T17:37:12-05:00

Bro 
@ErnestoSOFTWARE
 was right.

AI fitness influencers are working insanely well on TikTok and Instagram.

Today I randomly got a recommended video from an AI influencer account only a few videos posted and it’s already very viral.

They’re selling simple products for $22.99.



---

## Pending Enhancement (ALPHA17676, Score: 43)

**Source:** 2026-03-07 | **URL:** @gregisenberg
**Added:** 2026-03-07T21:45:20-05:00

this is one of those stories that sounds fake but is inspirational 

teenagers frustrated with calorie tracking build cal ai, use chatgpt to teach them code, lean into viral short-form content instead of fundraising, grow to ~15m downloads and $30m+ in revenue, and sell to



---

## Pending Enhancement (ALPHA17786, Score: 36)

**Source:** 2026-03-07 | **URL:** @maverickecom
**Added:** 2026-03-07T21:45:20-05:00

We launched a 7 figure Amazon brand on tiktok shop and did $20k with human UGC creators this week

Good team and good systems >

Takeaway:

- launch with human UGC. We use plug and play method to connect brands to high GMV creators in a mix of low retainers and commission only

-



---

## Pending Enhancement (ALPHA17836, Score: 42)

**Source:** 2026-03-07 | **URL:** @affprinter
**Added:** 2026-03-07T21:45:20-05:00

I Made $4,884 today

no product, no face, no prior audience
just making viral TikTok slideshows

if you won't pull at least $1K in the first 7 days there is literally 0 hope for you man

Retweet & Comment “TikTok” (must be following) and ill send you a free guide on how to do it



---

## Pending Enhancement (ALPHA17919, Score: 26)

**Source:** 2026-03-07 | **URL:** @affprinter
**Added:** 2026-03-07T21:45:21-05:00

Tiktok organic + affiliate sweep offers = easiest way to make $7k/week

its so simple but people just dont have the right guidance

so I made a free guide for you guys so you can print $20k/months

Just comment "sweeps" and retweet and ill send it over (must follow for auto dm)



---

## Pending Enhancement (ALPHA17920, Score: 20)

**Source:** 2026-03-07 | **URL:** @affprinter
**Added:** 2026-03-07T21:45:21-05:00

I made $2342 today from ai TikTok slideshows

This is the easiest way to make money in 2026

All organic, 0 Ads

want the breakdown?

Deleting in 24 hours....

Retweet & Comment “Slides” and I’ll dm you a free guide on how to start. (Must be following for auto dm)



---

## Pending Enhancement (ALPHA17967, Score: 41)

**Source:** 2026-03-07 | **URL:** @alexxgrowth
**Added:** 2026-03-07T21:45:21-05:00

how to make get rich off of ROBLOX:  

1/ find a brainrotted niche 
2/ ask chatgpt for enjoyable gameplay loops
3/ hire and fire a dev to do it for $10-$20 
4/ use content rewards to market it 
5/ add pay to win gamepasses for 99-999 robux 
6/ profit $100k/mo minimum



---

## Pending Enhancement (HN_008, Score: 20)

**Source:** HackerNews | **URL:** https://news.ycombinator.com/item?id=47291513
**Added:** 2026-03-08T00:10:14-05:00

LLM Writing Tropes.md — 129pts crowdsourced list of LLM writing tells. High engagement signal: everyone hates AI slop. Content angle: tweet thread on avoiding LLM tropes = guaranteed engagement.



---

## Pending Enhancement (HN_010, Score: 20)

**Source:** HackerNews | **URL:** https://news.ycombinator.com/item?id=47292485
**Added:** 2026-03-08T00:10:14-05:00

Put the zip code first — 385pts UX micro-optimization. Single-page site about one UX insight that went viral. Model for solopreneur content: one specific insight, sharp domain, instant share.



---

## Pending Enhancement (ALPHA18305, Score: 28)

**Source:** @wesocialgrowth (high-signal-accounts) | **URL:** https://x.com/wesocialgrowth/status/2030644732951703580
**Added:** 2026-03-08T11:32:51-04:00

- 2009 Meditation App Giant Suddenly Enters TikTok
- From Vent Now to Stateshift: The Anxiety Format Is Evolving
- Will This New AI Therapy App Hit 1 Million Views?
- The “UMAX for Body” App Pulling 40M Views
- This App Creates Your Virtual (Monetized) Twin
- AI Quran Tutor Hits



---

## Pending Enhancement (ALPHA18489, Score: 24)

**Source:** @HamptonAc_ (high-signal-accounts) | **URL:** https://x.com/HamptonAc_/status/2030704587988996228
**Added:** 2026-03-08T18:45:00-04:00

If I had to start over with $500 and 90 days to make $10K, here's exactly what I'd do:

Day 1-3: Pick a niche with desperate buyers (health, wealth, relationships). Not "cool" products. Problems people lose sleep over.

Day 4-7: Find 3 products already selling on TikTok with 1M+



---

## Pending Enhancement (ALPHA_HN_47299009, Score: 26)

**Source:** hackernews | **URL:** https://mlumiste.com/general/openai-charter/
**Added:** 2026-03-08T19:02:44-04:00

AGI goalposts debate: 315 HN pts + 208 comments. OpenAI charter analysis. Massive engagement on AI skepticism content. Content farming angle: contrarian AI takes drive huge engagement. Write anti-hype AI content for niche accounts.



---

## Pending Enhancement (ALPHA19327, Score: 24)

**Source:** @SimonasDip (high-signal-accounts) | **URL:** https://x.com/SimonasDip/status/2031004284544844139
**Added:** 2026-03-09T12:00:09-04:00

another viral podcast page printing MILLIONS of views

i actually think some videos are real (if they're not, insane job well done)

my guess is they're promoting their real podcast, which is the same name as the tiktok page

P.s. the reason all these videos have B&W filters is



---

## Pending Enhancement (ALPHA19473, Score: 43)

**Source:** 2026-03-09 | **URL:** @gregisenberg
**Added:** 2026-03-09T12:20:03-04:00

this is one of those stories that sounds fake but is inspirational 

teenagers frustrated with calorie tracking build cal ai, use chatgpt to teach them code, lean into viral short-form content instead of fundraising, grow to ~15m downloads and $30m+ in revenue, and sell to



---

## Pending Enhancement (ALPHA19583, Score: 36)

**Source:** 2026-03-09 | **URL:** @maverickecom
**Added:** 2026-03-09T12:20:03-04:00

We launched a 7 figure Amazon brand on tiktok shop and did $20k with human UGC creators this week

Good team and good systems >

Takeaway:

- launch with human UGC. We use plug and play method to connect brands to high GMV creators in a mix of low retainers and commission only

-



---

## Pending Enhancement (ALPHA19633, Score: 42)

**Source:** 2026-03-09 | **URL:** @affprinter
**Added:** 2026-03-09T12:20:03-04:00

I Made $4,884 today

no product, no face, no prior audience
just making viral TikTok slideshows

if you won't pull at least $1K in the first 7 days there is literally 0 hope for you man

Retweet & Comment “TikTok” (must be following) and ill send you a free guide on how to do it



---

## Pending Enhancement (ALPHA19716, Score: 26)

**Source:** 2026-03-09 | **URL:** @affprinter
**Added:** 2026-03-09T12:20:03-04:00

Tiktok organic + affiliate sweep offers = easiest way to make $7k/week

its so simple but people just dont have the right guidance

so I made a free guide for you guys so you can print $20k/months

Just comment "sweeps" and retweet and ill send it over (must follow for auto dm)



---

## Pending Enhancement (ALPHA19717, Score: 20)

**Source:** 2026-03-09 | **URL:** @affprinter
**Added:** 2026-03-09T12:20:03-04:00

I made $2342 today from ai TikTok slideshows

This is the easiest way to make money in 2026

All organic, 0 Ads

want the breakdown?

Deleting in 24 hours....

Retweet & Comment “Slides” and I’ll dm you a free guide on how to start. (Must be following for auto dm)



---

## Pending Enhancement (ALPHA19764, Score: 41)

**Source:** 2026-03-09 | **URL:** @alexxgrowth
**Added:** 2026-03-09T12:20:03-04:00

how to make get rich off of ROBLOX:  

1/ find a brainrotted niche 
2/ ask chatgpt for enjoyable gameplay loops
3/ hire and fire a dev to do it for $10-$20 
4/ use content rewards to market it 
5/ add pay to win gamepasses for 99-999 robux 
6/ profit $100k/mo minimum



---

## Pending Enhancement (ALPHA19790, Score: 24)

**Source:** 2026-03-09 | **URL:** r/startups
**Added:** 2026-03-09T12:20:03-04:00

$20k MRR to $191K MRR for supplement brand (I will not promote) heres every step of how we took a wellness brand from $20K MRR to $191K MRR in 7 months. It wasn’t all sunshine and rainbows but right now with AI you can get serious productivity gains. Hope this helps.

Tbh smaller DTC brands have an insane advantage compared to legacy companies now and it’s not even close.

My advice: take this and



---

## Pending Enhancement (ALPHA19941, Score: 29)

**Source:** @maverickecom (high-signal-accounts) | **URL:** https://x.com/maverickecom/status/2031033313729630550
**Added:** 2026-03-09T15:25:24-04:00

I just launched a brand on tiktok shop and added $45K GMV in under 2 months 

Here’s how:

- insider creating method
- plug and play method 

If you want to see my full playbook to scale brands on tiktok shop:

Comment SCALE and I’ll send it over 

(Must be following for me to



---

## Pending Enhancement (ALPHA_SCRAPE_20260309_1626_8114, Score: 39)

**Source:** reddit_r/SideProject_scrape | **URL:** https://reddit.com/r/SideProject
**Added:** 2026-03-09T16:26:45-04:00

Anti-AI positioning thread gets 610+ upvotes and 1518 comments on r/SideProject (vs typical 50-100). Contrarian angle "Not-AI" + physical product = massive engagement. Hardware startup with iF Design Award. Shows market fatigue with AI-only products.



---

## Pending Enhancement (ALPHA20153, Score: 24)

**Source:** @maverickecom (high-signal-accounts) | **URL:** https://x.com/maverickecom/status/2031124127700893862
**Added:** 2026-03-09T19:57:42-04:00

Here’s the full breakdown of how my agency added $45k GMV in 7 weeks for an Ecom brand

Every TikTok shop brand should be stealing my exact strategies lol



---

## Pending Enhancement (ALPHA20200, Score: 24)

**Source:** @wannercashcow (high-signal-accounts) | **URL:** https://x.com/wannercashcow/status/2031136331171295278
**Added:** 2026-03-09T19:57:42-04:00

Student Phiri just got the $50K role added

And he started last year..

But he already made more than $57,000 from faceless YouTube

He's just a normal guy who's willing to put in the work and DOESN'T give up

How would $10K+/month change YOUR life?

If you want to build your own



---

## Pending Enhancement (ALPHA20585, Score: 26)

**Source:** r/NewTubers | **URL:** https://reddit.com/r/NewTubers/comments/1rpjv1r/youtube_is_using_bots_when_you_use_advertising/
**Added:** 2026-03-10T06:45:01-04:00

[r/NewTubers] Youtube is using Bots when you use advertising with them!! This is So illegal!!!



---

## Pending Enhancement (ALPHA20597, Score: 26)

**Source:** r/NewTubers | **URL:** https://reddit.com/r/NewTubers/comments/1rprcef/results_one_week_of_posting_shorts_about_history/
**Added:** 2026-03-10T06:45:01-04:00

[r/NewTubers] Results: One week of posting shorts about history.



---

## Pending Enhancement (ALPHA20599, Score: 22)

**Source:** r/SaaS | **URL:** https://reddit.com/r/SaaS/comments/1rplpyh/tested_6_marketing_channels_to_scale_a_b2c_saas/
**Added:** 2026-03-10T06:45:01-04:00

[r/SaaS] Tested 6 marketing channels to scale a B2C SaaS to 6-figure MRR. One channel hit 500M+ views. One was a complete waste of money. Full breakdown w resources below



---

## Pending Enhancement (ALPHA20677, Score: 24)

**Source:** @maverickecom (high-signal-accounts) | **URL:** https://x.com/maverickecom/status/2031349689472205081
**Added:** 2026-03-10T14:23:33-04:00

anyone could have a tiktok shop brand that adds $100k/mo easily

Sadly, most think it takes years to build 

Here’s how you can do it in the next 6 weeks:



---

## Pending Enhancement (ALPHA21631, Score: 24)

**Source:** @adriamatz (bookmarks) | **URL:** https://x.com/adriamatz/status/2031273051598311788
**Added:** 2026-03-11T00:15:01-04:00

A fake AI app makes $50K/mo from dog owners

→ 60K downloads/mo
→ Just plays random sounds at your dog

The "AI translation" is fake.

Picks a random emotion and displays it.

They film their dog's reaction for TikTok.

The pet niche never dies.

700M dogs as potential users.



---

## Pending Enhancement (ALPHA22498, Score: 24)

**Source:** @knoxtwts (high-signal-accounts) | **URL:** https://x.com/knoxtwts/status/2031728918122889439
**Added:** 2026-03-12T02:14:17-04:00

actual ways people are making money with ai content right now:

- ugc ads for companies (retainers, $2k/mo+)
- faceless channels (low ticket, affiliates)
- ai slideshow accounts on tiktok (affiliate network + brand links)
- white label production for other agencies (they mark up



---

## Pending Enhancement (ALPHA22682, Score: 38)

**Source:** r/passive_income | **URL:** https://reddit.com/r/passive_income/comments/1rqsrdo/accidentally_built_a_following_of_40_year_old/
**Added:** 2026-03-12T06:15:01-04:00

[r/passive_income] Accidentally built a following of 40+ year old women on Facebook. I'm a 26M. First brand deal just paid $320 for one post.



---

## Pending Enhancement (ALPHA22837, Score: 20)

**Source:** r/Affiliatemarketing | **URL:** https://reddit.com/r/Affiliatemarketing/comments/1rqf1iv/why_do_most_creators_fail_at_affiliate_marketing/
**Added:** 2026-03-12T06:15:02-04:00

[r/Affiliatemarketing] Why do most creators fail at affiliate marketing even with thousands of views?



---

## Pending Enhancement (ALPHA22656, Score: 26)

**Source:** @alexcooldev (high-signal-accounts) | **URL:** https://x.com/kritarthmittal/status/2031715676847817031
**Added:** 2026-03-12T06:45:02-04:00

Sora 2 just got a massive upgrade.

I partnered with Arcads to build a custom n8n workflow that

> scrapes Reddit
> analyzes competitors' ads
> recreates viral AI ugc videos
> puts it all on a Google sheet / Airtable
> schedules it on X, TikTok, Li

Like + comment "SEND" to get



---

## Pending Enhancement (ALPHA23006, Score: 30)

**Source:** @unknown (bookmark) | **URL:** https://x.com/unknown/status/2008643433897066927
**Added:** 2026-03-12T08:18:27-04:00

🚀 Turn podcasts into viral clips in minutes. Virality Score finds your best moments, AI B-Roll adds flair, Speaker Detection keeps faces framed, and removes filler words like “um” &amp; “uh.”

Don't sleep on this. Try OpusClip today and get 25 free clips/month.



---

## Pending Enhancement (ALPHA23031, Score: 30)

**Source:** @unknown (bookmark) | **URL:** https://x.com/unknown/status/2030639096322748789
**Added:** 2026-03-12T08:18:27-04:00

ReelClaw revolution is here

you can scale to 1000 tiktok accounts if you have:
&gt; viral hook
&gt; demos
&gt; warmed up accounts

and its all within reach.

connecting the dots now. https://t.co/O3Vo8gWrTA



---

## Pending Enhancement (ALPHA23038, Score: 28)

**Source:** @unknown (bookmark) | **URL:** https://x.com/unknown/status/2029790710451654938
**Added:** 2026-03-12T08:18:27-04:00

this article tells you exactly why you're not making good money on Youtube 🔗



---

## Pending Enhancement (ALPHA23052, Score: 30)

**Source:** @unknown (bookmark) | **URL:** https://x.com/unknown/status/2029179443302785362
**Added:** 2026-03-12T08:18:27-04:00

This is genuinely 1 of the weirdest apps I’ve ever seen💀

They are going viral on TT
1,000,000 views with this hook 

The app exposes if your partner is a Gooner by telling you when they visit a corn website. https://t.co/CyEgpJJZIR



---

## Pending Enhancement (ALPHA23933, Score: 30)

**Source:** @levikov (bookmarks) | **URL:** https://x.com/levikov/status/2032033939653869853
**Added:** 2026-03-13T14:26:20-04:00

Instagram theme pages with AI characters are the most slept-on money printer on the internet right now and the people running them are earning $5-40k/month from a single page while everyone else fights over TikTok…

I'm going to explain exactly how this works because the people



---

## Pending Enhancement (ALPHA23956, Score: 30)

**Source:** @maverickecom (high-signal-accounts) | **URL:** https://x.com/maverickecom/status/2032469101126324349
**Added:** 2026-03-13T16:50:42-04:00

$70k added revenue for a client we launched on tiktok shop less than 2 months ago.



---

## Pending Enhancement (ALPHA24145, Score: 32)

**Source:** @affprinter (high-signal-accounts) | **URL:** https://x.com/affprinter/status/2031999796504883586
**Added:** 2026-03-13T16:50:49-04:00

I make $100K+ per month with TikTok slideshows
 
Here's how in 10 steps:
 
1. create TikTok accounts (5 min)
2. pick your offer: Walmart, Sephora, Amazon, Target, etc (1 min)
3. scroll TikTok, find viral slideshows in your niche (10 min)
4. screenshot the best frames, add your



---

## Pending Enhancement (ALPHA24167, Score: 30)

**Source:** @alexxgrowth (high-signal-accounts) | **URL:** https://x.com/alexxgrowth/status/2032093755730264164
**Added:** 2026-03-13T16:50:56-04:00

tiktok is now paying people to clip their content and post it on youtube

let me say that again

a platform worth $50 BILLION is using the exact same model that 16 year olds on Content Rewards use to make rent

they're not running ads. they're not doing influencer deals

they're



---

## Pending Enhancement (ALPHA24174, Score: 49)

**Source:** @fromzerotomill (high-signal-accounts) | **URL:** https://x.com/fromzerotomill/status/2032330778173219144
**Added:** 2026-03-13T16:50:56-04:00

Phantom Profits is live

the complete system for building faceless pages that print $10k-30k/month

12 beta operators averaged $18,400 in first 60 days
everything included:

1. niche selection framework
2. offer architecture
3. viral content engine
4. dm conversion scripts
5.



---

## Pending Enhancement (ALPHA25174, Score: 20)

**Source:** @pounddz (high-signal-accounts) | **URL:** https://x.com/pounddz/status/2032736197403939262
**Added:** 2026-03-14T06:15:03-04:00

I know a kid that’s been making 15k a month pretty consistently with TikTok slideshows 

He just uses Clawdbot + Nano banana to make the slides and promotes content rewards offers 

he said he works max 2 hours a day and has a system to go viral super consistently 

here's



---

## Pending Enhancement (ALPHA16762, Score: 20)

**Source:** r/AppBusiness | **URL:** https://reddit.com/r/AppBusiness/comments/1rm9qt8/reached_10k_users/
**Added:** 2026-03-14T12:48:45-04:00

Reached 10k users! | 10k in 4 months! Here are some tips for growth



---

## Pending Enhancement (ALPHA16792, Score: 23)

**Source:** r/SaaS | **URL:** https://reddit.com/r/SaaS/comments/1rn2s49/stop_playing_founder_and_start_building_a_business/
**Added:** 2026-03-14T12:48:45-04:00

Stop playing 'Founder' and start building a business. | I’m so sick of seeing founders bragging about their $1.8M seed rounds, winning pitch competitions, or being "Visionaries."



---

## Pending Enhancement (ALPHA16810, Score: 22)

**Source:** r/MicroSaas | **URL:** https://reddit.com/r/microsaas/comments/1rmzcwp/im_21_i_just_failed_my_dream_job_exam_by_15/
**Added:** 2026-03-14T12:48:45-04:00

I’m 21, I just failed my dream job exam by 15 seconds, and I’ve spent 4 months building an AI to save my family. Please hear me out. 🥺 | ​I’m a 21-year-old Mathematics graduate from India, and I’m writing this because I’m at a breaking point.



---

## Pending Enhancement (ALPHA16813, Score: 23)

**Source:** r/affiliatemarketing | **URL:** https://reddit.com/r/Affiliatemarketing/comments/1rmg4tu/curious_on_what_the_best_methods_of_earnings/
**Added:** 2026-03-14T12:48:45-04:00

Curious on what the best methods of earnings affiliate income is in this day and age from digital products? | I really want to take my affiliate income to the next level, and I am curious if anyone would be open to sharing a bit about which methods worked well for them.



---

## Pending Enhancement (ALPHA98738, Score: 43)

**Source:** indiehackers | **URL:** https://www.indiehackers.com/post/creators/from-simple-newsletter-to-4-5m-yr-media-company-RgQf0f1CJEO8KzTFjExN
**Added:** 2026-03-15T04:25:18-04:00

Newsletter to $4.5M/yr media company (Tangle). Isaac Saul: nonpartisan political newsletter. 500K+ readers in 60+ countries. Started on Substack with 13 readers then moved to Ghost (avoiding 10% revenue cut). $4M ARR + $500K+ ad revenue. Key: wrote while working full-time for first year. Reader feedback shaped product.



---

## Pending Enhancement (ALPHA100019, Score: 26)

**Source:** @leojrr (bookmarks) | **URL:** https://x.com/leojrr/status/2032560486638838071
**Added:** 2026-03-15T06:15:02-04:00

biggest mistake i made with openclaw
automating TikTok without data

it was just a bot guessing what to post about

now it:
1. analyzes trending topics in my niche
2. finds which slides are performing best
3. learns and adjusts automatically

here's exactly how to set it up

---



---

## Pending Enhancement (ALPHA100174, Score: 28)

**Source:** r/NewTubers | **URL:** https://reddit.com/r/NewTubers/comments/1rtjzei/went_viral_but_i_wont_get_paid_since_yt/
**Added:** 2026-03-15T06:20:04-04:00

[r/NewTubers] Went Viral - But I Won't Get Paid Since YT Monetization Takes So Long



---

## Pending Enhancement (ALPHA100312, Score: 20)

**Source:** r/beermoney | **URL:** https://reddit.com/r/beermoney/comments/1rsl3xv/trying_to_monetise_my_ig_page_42k_organic/
**Added:** 2026-03-15T06:20:04-04:00

[r/beermoney] Trying to monetise my IG page (42k+ organic followers)



---

## Pending Enhancement (ALPHA100317, Score: 22)

**Source:** r/NewTubers | **URL:** https://reddit.com/r/NewTubers/comments/1rtlotr/what_were_your_stats_after_your_first_year_on/
**Added:** 2026-03-15T06:20:04-04:00

[r/NewTubers] What were your stats after your first year on YouTube



---

## Pending Enhancement (ALPHA100498, Score: 24)

**Source:** ProductHunt | **URL:** https://www.producthunt.com/products/sitsense
**Added:** 2026-03-15T08:15:02-04:00

[PH LAUNCH] SitSense: Use your webcam to fix your posture



---

## Pending Enhancement (ALPHA100531, Score: 28)

**Source:** r/NewTubers | **URL:** https://reddit.com/r/NewTubers/comments/1rucfg6/after_years_on_youtube_i_realise_subscribers_are/
**Added:** 2026-03-15T08:55:30-04:00

[r/NewTubers] After years on YouTube, I realise subscribers are just not that important, THIS IS !



---

## Pending Enhancement (ALPHA100722, Score: 20)

**Source:** @lottsnomad (high-signal-accounts) | **URL:** https://x.com/lottsnomad/status/2033291438377632219
**Added:** 2026-03-16T00:24:29-04:00

ever wonder how much those annoying games on tiktok make?

here’s one

$80 million a month

only 1 year old btw



---

## Pending Enhancement (ALPHA100858, Score: 26)

**Source:** r/NewTubers | **URL:** https://reddit.com/r/NewTubers/comments/1rur8qk/finally_monetized_one_of_my_channels_yesterday/
**Added:** 2026-03-16T00:25:19-04:00

[r/NewTubers] Finally monetized one of my channels yesterday!



---

## Pending Enhancement (ALPHA100859, Score: 20)

**Source:** r/NewTubers | **URL:** https://reddit.com/r/NewTubers/comments/1ruwae7/national_park_channel_over_4_months/
**Added:** 2026-03-16T00:25:19-04:00

[r/NewTubers] National Park channel over 4 months



---

## Pending Enhancement (ALPHA100645, Score: 35)

**Source:** @maverickecom (high-signal-accounts) | **URL:** https://x.com/maverickecom/status/2033294085797077247
**Added:** 2026-03-16T00:41:06-04:00

I made $100K for an brand in under 2 months on TikTok Shop

- no wasted samples
- no lost time 
- no bs 
- no fluff

I put together a brand new comprehensive playbook I used to scale this brand with UGC and AI creators. 

It covers: 

- how to find good creators
- making content



---

## Pending Enhancement (ALPHA100649, Score: 26)

**Source:** @maverickecom (high-signal-accounts) | **URL:** https://x.com/maverickecom/status/2033200284848009312
**Added:** 2026-03-16T00:41:06-04:00

I just did $100k in added sales for a client, my agency took them live on tiktok shop 5 weeks ago at 0

Here’s how we do this:

1 - choosing my inner circle high quality creators 

2 - giving them training on viral content ideas with the product 

3 - keeping content quality high



---

## Pending Enhancement (ALPHA101136, Score: 26)

**Source:** ProductHunt | **URL:** https://www.producthunt.com/products/glam-ai
**Added:** 2026-03-16T04:16:41-04:00

[PH LAUNCH] Glam AI: Pick a trend, add your photo, and create viral content



---

## Pending Enhancement (ALPHA102626, Score: 24)

**Source:** @maverickecom (high-signal-accounts) | **URL:** https://x.com/maverickecom/status/2033614608347341005
**Added:** 2026-03-16T15:45:00-04:00

AI + UGC = GOLDMINE 

One can easily scale to $100K+/ Mo. with this strategy 

Tiktok has billions of users actively searching, learning, and comparing.

And compared to Meta or Amazon?

It's still way less saturated.

While most brands are stuck fighting rising CPMs on



---

## Pending Enhancement (ALPHA102628, Score: 28)

**Source:** @maverickecom (high-signal-accounts) | **URL:** https://x.com/maverickecom/status/2033570316883005863
**Added:** 2026-03-16T15:45:00-04:00

this AI tiktok page has 34k followers and thousands of views 
you probably wouldn't even tell it's AI

i built a workflow to recreate these videos easily

reply "SOURCE" and i'll send you access + a full guide

(must be following so i can dm)



---

## Pending Enhancement (ALPHA102693, Score: 30)

**Source:** @franci__ugc (high-signal-accounts) | **URL:** https://x.com/franci__ugc/status/2033565889530913092
**Added:** 2026-03-16T15:45:01-04:00

brands that ran UGC campaigns saw up to 460% engagement growth  

one campaign generated 1.5 million pieces of content across tiktok, instagram and x  

the brands that win aren't making better ads 

they're making content with real people, that viewers want to engage with



---

## Pending Enhancement (ALPHA102838, Score: 54)

**Source:** r/passive_income | **URL:** https://reddit.com/r/passive_income/comments/1rvkdew/day_6_0_10k_with_ai_influencers/
**Added:** 2026-03-16T16:19:22-04:00

[r/passive_income] Day 6 $0 - $10k With AI Influencers



---

## Pending Enhancement (ALPHA102857, Score: 20)

**Source:** r/NewTubers | **URL:** https://reddit.com/r/NewTubers/comments/1rvkmuq/shorts_stop_growing_after_1k/
**Added:** 2026-03-16T16:19:22-04:00

[r/NewTubers] Shorts stop growing after 1k



---

## Pending Enhancement (ALPHA103020, Score: 20)

**Source:** @affprinter (high-signal-accounts) | **URL:** https://x.com/affprinter/status/2033649987309993986
**Added:** 2026-03-16T18:15:01-04:00

I made $3424 Today from a viral tiktok slideshow
which i made with nano banana pro

I swear to god this is the easiest business model ever

Kids are LITERALLY making thousands a day

want the breakdown?

Deleting in 24 hours....

Retweet & Comment “Slideshow” and I’ll dm you a



---

## Pending Enhancement (ALPHA103084, Score: 26)

**Source:** r/socialmedia | **URL:** https://reddit.com/r/socialmedia/comments/1rvlhrt/should_i_pivot_my_100k_follower_social_media/
**Added:** 2026-03-16T18:21:03-04:00

[r/socialmedia] Should I pivot my 100k+ follower social media pages from documentary content to a product visualization page, or start fresh?



---

## Pending Enhancement (ALPHA103098, Score: 22)

**Source:** r/NewTubers | **URL:** https://reddit.com/r/NewTubers/comments/1rvghwj/do_your_videos_take_a_long_time_to_get_traction/
**Added:** 2026-03-16T18:21:03-04:00

[r/NewTubers] Do your videos take a long time to get traction?



---

## Pending Enhancement (ALPHA103498, Score: 24)

**Source:** @levelsio (high-signal-accounts) | **URL:** https://x.com/levelsio/status/2033717610844459108
**Added:** 2026-03-17T11:13:22-04:00

Kinda, in 2014 I made $5K/mo with Nomad List, 2015 was $10K/mo with Remote OK added

Before that 2008-2013, I was making anywhere from $2K to $8K/mo with my YouTube channel

And then before 2008 I was making maybe $500 - $1K/mo with my AdSense blogs

And then around 2003 I was

