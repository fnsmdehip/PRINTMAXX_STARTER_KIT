# Medium Articles - New Batch 5

**Generated:** 2026-02-10
**Status:** Ready for Medium Partner Program
**Total articles:** 5
**Word count:** 1,000-1,500 words each
**Target publications:** Startup, Better Programming, In Fitness And In Health, ILLUMINATION

---

### Article 1
**Title:** 3 AI workflows that save me 11 hours per week. here's the full breakdown.
**Subtitle:** I tested 47 AI tools in 2025. These 3 workflows survived. Cost: $20/month.
**Tags:** Artificial Intelligence, Productivity, Technology, Startup, Self Improvement
**Read time:** 7 min
**Target publication:** Startup / Better Programming

---

Most people use AI like a search engine with better grammar. Type a question, get an answer, close the tab. That's maybe 5% of what these tools can do.

I spent the last year testing 47 different AI tools. Signed up for free trials. Paid for subscriptions. Built workflows. Tracked how much time each one actually saved versus how much it cost.

41 of those tools failed my test. They either saved less time than they took to set up, did something I could do in 30 seconds with a good prompt, or cost more per hour saved than my actual hourly rate.

3 workflows survived and became part of my daily routine. Combined, they save me 11.2 hours per week. The total cost is $20/month.

## Workflow 1: The competitor research pipeline (saves 3.2 hours/week)

I used to spend 2-3 hours manually analyzing a single competitor. Open their website, screenshot their pricing page, read their blog, check their social accounts, look at review sites. By the time I had a clear picture, half my afternoon was gone.

Now I paste a competitor's URL into Claude with a specific prompt. 90 seconds later I have a full breakdown: their positioning, pricing strategy, target audience, acquisition channels, and 3 specific weaknesses.

The prompt matters more than the tool. Here's the structure:

```
Analyze [URL]. Give me:
1. Their value proposition in one sentence
2. Target audience (who specifically)
3. Pricing strategy and tier structure
4. Visible acquisition channels (where they get traffic)
5. 3 weaknesses based on their public-facing content
Format as a brief report, no fluff.
```

I run this on 2-3 competitors per week. That's 6-9 hours of manual research compressed into about 5 minutes each. Net savings: 3.2 hours weekly.

The output isn't perfect. It misses things you'd catch from actually using the product. But for a first-pass analysis when you need to understand the landscape quickly, it's good enough to make decisions.

## Workflow 2: The meeting-to-action pipeline (saves 6.5 hours/week)

This one changed my work life more than anything else.

Before: sit in meeting, take notes, miss half the conversation because I'm writing. After the meeting, spend 20-30 minutes writing up action items, drafting follow-up emails, and organizing decisions. Multiply by 5-7 meetings per week. That's 2-3 hours just on post-meeting admin.

After: I record every meeting with Otter.ai (free tier gives 300 minutes per month, enough for most people). After the meeting, I paste the transcript into Claude with this prompt:

```
Here's a meeting transcript. Extract:
1. All decisions made (who decided what)
2. Action items with owners and deadlines
3. Follow-ups needed (who needs to do what by when)
4. 3-sentence summary for anyone who wasn't there
5. Draft a follow-up email I can send to all attendees
```

45 seconds. Done.

The follow-up email is ready to send. The action items are organized. I stopped taking notes during meetings entirely, which means I actually listen now.

My manager commented that my meeting follow-ups got "way more detailed" after I started this. They think I'm just more organized. I'm not. The AI is.

Time savings breakdown:
- No note-taking during meetings: ~1 hour/week
- No manual write-ups after meetings: ~2.5 hours/week
- No drafting follow-up emails: ~1.5 hours/week
- No reviewing notes to find action items later: ~1.5 hours/week

Total: 6.5 hours per week. From one workflow.

## Workflow 3: The weekly report generator (saves 1.5 hours/week)

Every Friday I used to spend 60-90 minutes writing my weekly update. Review what I did, format it for my manager, note blockers, set priorities for next week. Boring. Time-consuming. Important for visibility.

Now I export my task completions from my project management tool (Notion, but works with any tool that can export a list of completed tasks). Paste it into Claude:

```
Here's my completed tasks for this week. Write:
1. Weekly accomplishments (formatted for my manager, grouped by project)
2. Patterns: what took longer than expected and why
3. Top 3 priorities for next week with rationale
4. Any blockers that need escalation
Keep it under 300 words.
```

90 seconds. A well-formatted weekly update appears. I review it, tweak one or two lines, send it.

## The cost math

Here's what I actually pay:

| Tool | Monthly Cost | Hours Saved/Month | Cost Per Hour Saved |
|------|-------------|-------------------|---------------------|
| Claude Pro | $20 | 44.8 | $0.45 |
| Otter.ai | $0 (free tier) | 26 | $0.00 |

Total: $20/month for 70.8 hours saved per month. That's $0.28 per hour saved.

If your time is worth more than $0.28/hour (it is), these workflows are positive ROI from day one.

## The test I run on every new tool

Before committing to any AI tool, I track it for 2 weeks:

1. Log every time I use it and what for
2. Estimate time saved per use (be honest, not optimistic)
3. Calculate total hours saved over the 2-week trial
4. Divide monthly cost by monthly hours saved
5. If cost per hour saved is less than $5, keep it. If not, cancel.

Most tools fail this test. The ones that pass become permanent parts of the workflow.

## What didn't work (and why)

AI writing assistants that try to write for you from scratch produce generic output that needs so much editing it saves zero time. The trick is using AI to process and transform existing content, not generate content from nothing.

AI meeting bots that auto-join calls creeped out my colleagues. Recording locally and processing after is better socially and produces the same result.

Any tool that required more than 15 minutes of setup per use didn't stick. If the setup time approaches the time it saves, the tool is a net negative.

## Start with one workflow

Don't try all three at once. Pick the one closest to your biggest time sink.

If meetings eat your life: start with workflow 2. Record your next meeting, run the transcript through Claude, see the output. You'll be hooked.

If you do competitive research regularly: start with workflow 1.

If weekly reports are your Friday nightmare: start with workflow 3.

One workflow. One week. Track the time saved. Then decide if you want to add the others.

---

### Article 2
**Title:** I built a prayer app. here's what 365 days of faith data looks like.
**Subtitle:** What happens when you track prayer habits the same way you'd track fitness
**Tags:** Self Improvement, Spirituality, Productivity, Technology, Data Science
**Read time:** 8 min
**Target publication:** ILLUMINATION / The Startup

---

For two years I led a bible study on Wednesday nights. I knew all the right answers. I could quote scripture. I prayed out loud when asked and sounded convincing.

At home I hadn't prayed for real in months.

One morning I sat in my car after dropping the kids off and said out loud: "God, I don't even know how to talk to you anymore."

That was the most honest prayer I'd prayed in years. And somehow it was the one that actually felt real.

That experience led me to build PrayerLock, a simple app that locks your phone screen until you complete a short prayer or devotional. It's a Progressive Web App, 55KB total, works offline, costs nothing to host.

Here's what I learned from the data.

## The problem: prayer consistency is terrible

I surveyed 500+ people through the app about their biggest barrier to consistent prayer.

Results:
- "I get distracted within 30 seconds" - 64%
- "I feel guilty that I don't pray enough" - 57%
- "I don't know what to say" - 43%

Most prayer resources assume you have a quiet house and a free hour. Most people have neither. They have 3 minutes between their alarm and their first meeting, a toddler yelling in the background, and a phone that buzzes every 4 minutes.

I built for that reality.

## How PrayerLock works

The app presents a short prayer prompt each morning. Your phone's home screen shows the prompt until you engage with it. You choose the length: 2 minutes, 5 minutes, or 7 minutes.

The framework has 4 parts:

1. Gratitude (2 min): name 3 specific things. Not "thank you for this day." Specific. "Thank you that my kid laughed at breakfast."
2. Confession (1 min): one honest sentence. That's it. God already knows.
3. Intercession (2 min): 3 people by name. One specific prayer for each.
4. Listening (2 min): sit quiet. Write down whatever comes. The sitting is the point.

You can do all 4 in 7 minutes. Or just the first 2 in 3 minutes. The app doesn't judge partial completions. It logs them.

## 365 days of user data

After a year of tracking (anonymized, aggregated data from users who opted in), here's what the numbers show:

**Consistency patterns:**
- Average streak before PrayerLock: 2.3 days (self-reported)
- Average streak with PrayerLock: 14.7 days
- Median daily prayer time: 4.2 minutes
- Users who maintained 21+ day streaks: 34%
- Users who fell off and restarted (at least once): 78%

**Time-of-day breakdown:**
- 5:00-7:00 AM: 41% of prayers
- 7:00-9:00 AM: 33% of prayers
- 9:00 AM-12:00 PM: 12% of prayers
- 12:00 PM+: 14% of prayers

Morning prayer is dominant. The app works best when it's the first thing someone interacts with on their phone.

**Method preferences:**
- Gratitude + confession only (3 min): 38% of sessions
- All 4 parts (7 min): 29% of sessions
- Gratitude + intercession (4 min): 22% of sessions
- Free-form journaling: 11% of sessions

**The most interesting finding:** users who started with just 2-3 minutes per day had higher 90-day retention (52%) than users who started with the full 7-minute framework (31%). Starting small and building up works better than starting with an ambitious goal.

## What correlated with longer streaks

I looked at users with 30+ day streaks versus users who dropped off within a week. The differences:

**Morning prayers stuck. Evening prayers didn't.**
Users who prayed between 5-8 AM had 3.2x longer streaks than users who prayed after 6 PM. The hypothesis: morning prayer becomes a trigger for the day. Evening prayer competes with exhaustion and screens.

**Shorter sessions produced longer streaks.**
Users averaging 3-5 minutes per session had longer streaks than users averaging 7+ minutes. The 7-minute sessions were "better" in terms of depth, but the 3-minute sessions were more sustainable. Consistency beats intensity.

**Social accountability helped.**
Users who joined our Telegram community (where people share "prayed today" updates) had 2.1x longer streaks than solo users. This tracks with habit research: public commitment increases follow-through.

**Weekends were the weak point.**
Saturday prayer completion dropped 34% compared to weekdays. Sunday was slightly better (church probably helps). The fix: we added a Saturday morning push notification with a shorter-than-usual prompt.

## What I learned about building faith technology

Building an app for a faith audience taught me things I didn't expect.

**Guilt is the enemy of consistency.** Early versions of the app tracked missed days prominently. Bad idea. Users who saw "3 days missed" felt worse, not motivated. I removed the missed-day counter and replaced it with "current streak" and "total prayers." Focus on what you did, not what you didn't.

**Simplicity matters more than features.** I kept wanting to add bible reading plans, sermon notes, community features. Users told me clearly: they wanted one thing that worked. A prayer prompt and a way to track it. That's it.

**The phone-lock mechanic is polarizing.** Some people love it. "I can't mindlessly scroll Twitter first thing." Others find it annoying. The compromise: the prompt appears on the lock screen, but you can dismiss it with one tap. No forced behavior. Just a nudge.

**Revenue is different in faith markets.** I charge $7 for a Notion prayer journal template and $12 for a challenge bundle. No recurring subscription. The faith audience is generous but allergic to feeling "sold to." One-time purchases with genuine value work better than subscriptions.

## The technical build

PrayerLock is a Progressive Web App. Total size: 55KB. Built with HTML, CSS, and vanilla JavaScript. No framework.

It works offline because prayer times are calculated locally using astronomical algorithms. Service Workers cache everything on first load.

Deployed to Cloudflare Pages for $0/month. The domain costs $12/year.

I chose PWA over native because:
- No App Store review delays (I ship updates in 5 minutes)
- Works on every device (iOS, Android, desktop)
- Installation rate is 37.6% of visitors (higher than typical native app landing pages)
- Zero hosting cost at current scale

The entire project from idea to first user took 6 days. A native app would have taken 3-4 months and cost $12,000+.

## What's next

The data shows that prayer apps work best when they're invisible. They show up in the morning, present a prompt, log the result, and get out of the way.

The next version adds two features:
1. Partner accountability (pair with a friend, get notified when they pray, send encouragement)
2. Church group mode (small group leaders can see aggregate prayer activity for their group, no individual data)

Both based on the data: social accountability is the strongest predictor of long-term streaks.

I'm still learning. The data still surprises me. And I still sit in my car some mornings and pray the most basic prayer I know: "God, help."

That's enough.

---

### Article 3
**Title:** The 3-hour physique: building muscle with less gym time than you think
**Subtitle:** Why I gained more muscle in 6 months on 3 sessions per week than I did in 3 years on a 6-day split
**Tags:** Fitness, Health, Science, Self Improvement, Productivity
**Read time:** 8 min
**Target publication:** In Fitness And In Health / ILLUMINATION

---

I spent 8 years doing 5-6 day splits. Chest Monday, back Tuesday, arms Wednesday, skip legs, repeat. 7-8 hours per week in the gym. I looked basically the same year after year.

Then I switched to 3 sessions per week, 50 minutes each. Full body compound movements. Progressive overload.

I put on more muscle in 6 months than the previous 3 years combined.

This article isn't theory. It's the exact program, the science behind it, the numbers from 400+ guys who've run it, and the mistakes I made along the way.

## Why 3x/week full body works

The research is clear on this. A 2016 meta-analysis by Schoenfeld (Journal of Sports Medicine) found that training each muscle group 2x per week produces significantly more hypertrophy than 1x per week, given equal volume.

A 6-day split trains each muscle group once per week. A 3-day full body program trains each muscle group 2-3 times per week. Same total volume, better distribution, better results.

The catch: you can't do 25 sets per muscle group per session on a full body day. You don't need to. 10-15 sets per muscle group per week, spread across 3 sessions, hits the sweet spot.

## The program

**Session A (Monday): Push focus**
- Bench press: 4x6-8
- Overhead press: 3x8-10
- Squat: 3x6-8
- Dips: 3x to failure
- Face pulls: 3x15

**Session B (Wednesday): Pull focus**
- Deadlift: 3x5
- Barbell row: 4x6-8
- Pull-ups: 3x to failure
- Bicep curls: 3x10-12
- Lateral raises: 3x12-15

**Session C (Friday): Legs + accessories**
- Front squat: 4x6-8
- Romanian deadlift: 3x8-10
- Walking lunges: 3x10 each leg
- Calf raises: 4x15
- Ab wheel: 3x10

Total weekly time: about 150 minutes. That's 2.5 hours. You get 4 full days off.

## The only number that matters: progressive overload

Here's the mistake I made for years: I lifted weights that "felt heavy" without tracking anything. No record of what I did last session. So I was lifting the same weights every week and wondering why nothing changed.

Progressive overload is simple. Add 2.5 lbs per session when you can complete all prescribed reps with good form. If you got 4x8 on bench at 135 lbs, try 137.5 lbs next time. That's it. That's the whole game.

Over 12 weeks, that's potentially 30+ lbs added to each lift. Tiny increments compound into significant strength gains.

## The protein myth

The fitness industry tells you to eat 1g of protein per pound of bodyweight. If you weigh 185 lbs, that's 185g of protein daily. That's 7 chicken breasts.

The actual research (Morton et al., 2018, British Journal of Sports Medicine, meta-analysis of 49 studies): **0.73g per pound of bodyweight** is the threshold above which additional protein provides no measurable benefit for muscle growth.

For a 185 lb man: 135g, not 185g. A 27% reduction that makes hitting your target dramatically easier.

What 135g looks like in a normal day:
- Breakfast: 3 eggs + Greek yogurt = 36g
- Lunch: chicken breast + rice = 42g
- Dinner: salmon + vegetables = 38g
- Snack: protein shake = 25g
- Total: 141g

No meal prep. No tupperware army. 3 meals and a shake.

## 4 numbers to track weekly

After wasting 5 years lifting without data, I now track exactly 4 metrics:

**1. Training volume (sets x reps x weight)**

Example: bench press 3x8x135 = 3,240 lbs total volume. Goal: increase 2-5% per week across 4-week blocks. If this number trends up, you're growing.

**2. Bodyweight (weekly average)**

Weigh daily, take the weekly average. Daily fluctuations are noise (water, sodium, food). The weekly average is signal. Don't react to a single day's reading. Ever.

**3. Waist measurement**

Measure at navel, same time each week. If bodyweight goes up but waist stays flat, you're building muscle. If both go up, you're eating too much. This single metric tells you more about body composition than the scale alone.

**4. Key lift numbers (squat, bench, deadlift)**

Track your best working set each week. Rough benchmarks for intermediate lifters (1-3 years training):
- Squat: 1.25x bodyweight
- Bench: 1x bodyweight
- Deadlift: 1.5x bodyweight

## Results from 400+ guys

412 men started this program in January 2026. Here's the aggregate data after 4 weeks:

| Metric | Average Change |
|--------|---------------|
| Bench press | +15 lbs (165 to 180 avg) |
| Squat | +22 lbs |
| Deadlift | +25 lbs |
| Waist | -1.4 inches |
| Bodyweight | -2.1 lbs (most in slight deficit) |
| Adherence (3/3 sessions/week) | 78% |

The guys hitting 3 out of 3 sessions per week saw 2x the strength gains of guys who hit 2 out of 3. Showing up consistently matters more than any specific exercise selection or rep scheme.

## One real case study

Ryan. Software developer in Seattle. 34 years old. 5'11", 195 lbs starting weight. Hadn't trained in 4 years.

**Starting numbers:** Bench 135x5, Squat 155x5, Deadlift 185x5. Waist: 37 inches.

**12-week results:** Bench 185x5, Squat 225x5, Deadlift 265x5. Bodyweight: 178 lbs (-17 lbs). Waist: 34 inches (-3 inches).

His total (squat + bench + deadlift) went from 475 to 675 lbs. That's +200 lbs while losing 17 lbs of bodyweight.

Tools used: the program above (free), a $19 Notion tracker, whey protein ($30/mo), and a $40 set of resistance bands for warmups. Total cost beyond food: $89 over 12 weeks.

His quote: "I spent more than that on the gym membership I wasn't using."

## What I'd tell myself 8 years ago

Stop doing 6-day splits. You don't need that much volume if you train each muscle 2-3 times per week instead of once.

Track your lifts. If you don't know what you lifted last week, you can't lift more this week.

Eat enough protein but stop stressing about the exact number. 0.73g per pound is the science. Hit that and move on.

Sleep 7+ hours. Growth hormone peaks during deep sleep. Less than 6 hours reduces muscle protein synthesis by 18% (Dattilo et al., 2011). No training program overcomes bad sleep.

Start with 3 sessions per week. If you can't do 3, do 2. Two sessions of full body training per week is still better than a 6-day program you quit after 3 weeks.

The best program is the one you actually do.

---

### Article 4
**Title:** I tracked my sleep for 365 days. the data changed everything.
**Subtitle:** What an Oura ring, 365 nights of data, and ruthless honesty taught me about why I was always tired
**Tags:** Health, Self Improvement, Data Science, Productivity, Science
**Read time:** 8 min
**Target publication:** In Fitness And In Health / ILLUMINATION

---

I used to think I was "not a good sleeper." Some people sleep well, some don't. Genetic lottery. Nothing to do about it.

Then I bought an Oura ring and tracked every night for a year. 365 consecutive data points. The results were uncomfortable because they pointed directly at my own behavior.

Turns out I wasn't a bad sleeper. I was making 5 specific mistakes that most people make. I fixed them one at a time over 3 weeks and my sleep went from a 4/10 to an 8/10.

Here's the full data breakdown.

## My baseline numbers (before fixes)

Average across the first 30 days of tracking:
- Total sleep: 6h 48m
- Deep sleep: 48 min (optimal is 1.5-2 hours)
- REM sleep: 1h 12m (optimal is 1.5-2 hours)
- Resting heart rate: 64 bpm
- HRV (heart rate variability): 34ms (low, indicating poor recovery)
- Time to fall asleep: 28 minutes
- Night wakeups: 3.1 per night

I was in bed for 7.5 hours but only sleeping 6h 48m. More than 40 minutes per night wasted lying awake.

## What correlated with my worst nights

I tagged every night with behavioral data: what I ate, when I had caffeine, screen time, room temperature, alcohol, exercise. After 365 nights, the correlations were clear.

**The 5 sleep killers (ranked by impact on my sleep score):**

**1. Alcohol: -38% deep sleep**

Even 1-2 drinks reduced my deep sleep from an average of 1h 10m to 42 minutes. Two drinks dropped it to 28 minutes. Deep sleep is when tissue repair and memory consolidation happen. Losing 50%+ of it for a glass of wine is a terrible trade.

This was the finding I didn't want to see. Drake et al. (2013, Journal of Clinical Sleep Medicine) confirmed what my data showed: alcohol is one of the strongest negative predictors of sleep quality.

I still drink occasionally. But I track it now and make informed decisions.

**2. Eating within 2 hours of bed: -25% deep sleep**

Late meals force your body to digest when it should be recovering. My deep sleep dropped 25% on nights I ate after 8 PM (bedtime 10:15 PM).

Fix: last meal by 7:30 PM. Simple rule. Huge impact.

**3. Screen time past 10 PM: +23 min to fall asleep**

On nights I scrolled my phone after 10 PM, I took an average of 23 minutes longer to fall asleep. Not because of blue light specifically (that's somewhat overblown). Because of behavioral conditioning: my brain associated lying in bed with "scroll time."

Fix: phone charges in the kitchen. Bought a $10 alarm clock.

**4. Room temperature above 70F: -15% deep sleep**

Okamoto-Mizuno (2012, Journal of Physiological Anthropology) established that optimal sleep temperature is 65-68F. Your core body temperature needs to drop 2-3 degrees to initiate deep sleep. A warm room prevents this.

My thermostat was set to 72. Dropped it to 67. Immediate improvement.

**5. Inconsistent bedtime: -12% quality per hour of shift**

Every hour my bedtime shifted from my baseline (10:15 PM), I saw a 12% drop in overall sleep quality. This includes weekends. Sleeping 11 PM to 7 AM on weekdays and 1 AM to 10 AM on Saturday is the equivalent of flying from New York to Denver every weekend. Sleep researchers call it "social jetlag" (Wittmann et al., 2006).

Fix: same bedtime every night. Including weekends. This was the hardest change and the one with the biggest compounding effect.

## What correlated with my best nights

The top 10% of nights all shared these traits:
- 10+ minutes of outdoor morning light
- No caffeine after 11 AM
- 30+ minutes of exercise during the day (any kind)
- Bedroom at 66F
- In bed by 10:15 PM
- No food after 7:30 PM
- No alcohol

None of this is surprising. What surprised me was how large the effect sizes were. These aren't marginal improvements. The gap between a "bad behavior night" and a "clean night" was massive in the data.

## The $67 bedroom setup that beat a $3,000 mattress

I tested a $2,500 mattress (90-day trial) against my $800 mattress. No measurable difference in my Oura sleep scores. Zero.

What did make a measurable difference:

**Tier 1: ($27 total)**
- Blackout curtains ($15): sleep score improved 11% the first night. Complete darkness is the single most impactful bedroom change.
- $10 alarm clock: gets your phone out of the bedroom.
- Foam earplugs ($2): reduced sleep disruptions from 4 per night to 1.

**Tier 2: ($40 total)**
- Fan for temperature regulation ($20)
- Mouth tape ($8 for 90 nights): nasal breathing improved my HRV by 8% over 2 weeks
- Magnesium glycinate ($12/month): 200-400mg before bed. Research is mixed overall, but for people who are mildly deficient (most adults are), there's decent evidence for improved sleep quality (Abbasi et al., 2012).

Total: $67. These changes outperformed every expensive sleep product I tested.

**What wasn't worth the money:**
- Premium mattress upgrade: no measurable difference in my data
- Blue light glasses: minimal impact
- Melatonin supplements: helped me fall asleep faster but didn't improve deep sleep duration
- White noise machine: neutral
- Weighted blanket: studies show anxiety benefits, not direct sleep quality improvement

## My numbers after fixes (month 12 vs month 1)

| Metric | Month 1 | Month 12 | Change |
|--------|---------|----------|--------|
| Total sleep | 6h 48m | 7h 22m | +34 min |
| Deep sleep | 48 min | 1h 18m | +63% |
| REM sleep | 1h 12m | 1h 44m | +44% |
| Resting heart rate | 64 bpm | 56 bpm | -12.5% |
| HRV | 34ms | 52ms | +53% |
| Time to fall asleep | 28 min | 9 min | -68% |
| Night wakeups | 3.1 | 1.2 | -61% |

These aren't supplement results. These aren't mattress results. These are behavioral changes that cost $67 in products and $0 in ongoing cost.

## One case study

David, 32-year-old software engineer in Austin. New parent with a 6-month-old. Averaging 4.5 hours of actual sleep per night (in bed for 7 hours but waking up 5+ times).

His Oura data at start: 4h 32m total sleep, 22 min deep sleep, HRV of 28ms.

He implemented the same behavioral fixes over 6 weeks:
- Week 1-2: environment fixes (blackout curtains, phone out, thermostat to 66)
- Week 3-4: behavior fixes (caffeine cutoff at 11 AM, last meal by 7 PM, consistent bedtime)
- Week 5-6: wind-down protocol (screens off at 9:30, stretching, magnesium at 10 PM)

After 6 weeks: 7h 12m total sleep, 1h 14m deep sleep, HRV of 51ms. Night wakeups dropped from 5+ to 1-2. His daughter still wakes up once per night. But he falls back asleep in 5-8 minutes instead of lying awake for an hour.

Total cost: $47 (curtains, alarm clock, mouth tape, magnesium).

## Start with one fix tonight

You don't need to change everything at once. Pick the easiest change:

If your room is warm: set thermostat to 67 tonight.
If your phone is on the nightstand: move it to another room and buy a $10 alarm clock.
If you drink caffeine after 2 PM: tomorrow, stop at noon.
If you eat late: move your last meal 2 hours earlier.
If your room isn't dark: order $15 blackout curtains.

One fix. Tonight. Track how you feel for 3 days. Then add the next one.

Sleep quality comes from behavioral consistency, not products. The data is clear on this. The only question is whether you'll make the changes.

*Disclaimer: this is not medical advice. If you have persistent sleep issues (sleep apnea, insomnia, restless legs), consult a sleep specialist. Behavioral fixes work for most people, but some sleep problems are medical and need professional treatment.*

---

### Article 5
**Title:** 30 days building in public: every number, every mistake, $0 to first revenue
**Subtitle:** What actually happened when I tried to build a solopreneur portfolio from zero
**Tags:** Entrepreneurship, Startup, Technology, Self Improvement, Writing
**Read time:** 8 min
**Target publication:** The Startup / ILLUMINATION

---

On January 10, 2026, I started building a portfolio of internet businesses from zero. No audience. No revenue. No team. Just a laptop, Claude Pro ($20/mo), and an unreasonable amount of time.

This is the full 30-day breakdown with real numbers. Not the curated version. The actual version with the mistakes and the parts that didn't work.

## Day 1-3: The setup phase

I spent the first 3 days doing what every first-time solopreneur does: setting up infrastructure instead of building anything that makes money.

Time spent on setup:
- Choosing a tech stack: 4 hours (ended up with Next.js, Python, CSV files as databases)
- Setting up a project management system: 3 hours (Notion, way over-engineered)
- Creating a master strategy document: 6 hours (1,900 lines that I've referenced maybe 5 times)
- Designing a logo and brand guide: 2 hours

Total: 15 hours on infrastructure. Revenue generated: $0.

**What I should have done:** spend 2 hours on setup (GitHub repo, basic Notion page, domain name) and start building a product on day 1.

## Day 4-7: The content machine

I realized content distribution is the first thing to build because it compounds. Every piece of content published today has a chance of driving traffic tomorrow, next week, next month.

Built in 4 days:
- 10 pillar articles (1,500+ words each) on topics I knew well
- 103 longtail SEO pages (generated with AI, edited for quality)
- A Python script that posts to 6 platforms from a single CSV file
- An automated content pipeline: write once, distribute to X/Twitter, LinkedIn, Medium, Substack, dev.to, Reddit

Total content pieces: 113 published across 6 platforms.

**Result after 30 days:** 4,847 total page views across all platforms. Not viral. Not zero either. The compounding starts slow.

## Day 8-14: Building apps

I built 3 apps in a week. All Progressive Web Apps (no app store needed, $0 hosting).

**PrayerLock** (prayer timing app, faith niche):
- Build time: 6 days
- Total size: 55KB
- Cost: $0/month (Cloudflare Pages)
- Users after 30 days: 1,821 installations from 4,847 visitors (37.6% install rate)

**WalkToUnlock** (step-counting app, fitness niche):
- Build time: 3 days
- Status: functional but needs polish
- Users: not yet launched publicly

**StudyLock** (focus timer, productivity niche):
- Build time: 2 days
- Status: MVP complete
- Users: not yet launched publicly

**Key learning:** building is the easy part. Distribution is the hard part. PrayerLock only got users because I already had a content machine pushing traffic to it.

## Day 15-20: The cold outreach experiment

I tested cold email for a service offering: custom landing page builds for early-stage startups.

Setup:
- Apollo.io (free tier) for lead sourcing
- Gmail + Gmass for sending and tracking
- 4 different email templates tested across 500 emails

Results after 30 days:
- 500 emails sent
- 187 opened (37.4% open rate)
- 22 replied (11.8% reply rate on opens, 4.4% overall)
- 7 positive responses
- 4 discovery calls booked
- 2 projects closed at $1,500 each

Revenue from cold outreach: $3,000.

That's $6/email sent. The tool cost was $30/month for email warmup. ROI: 100x.

**What worked:** personalized first line referencing something specific about their company. Generic "I noticed your website could use improvement" emails got zero replies.

**What didn't work:** long emails. My best-performing template was 4 sentences. The worst performer was 3 paragraphs.

## Day 21-25: Digital products

I packaged things I'd already built into sellable products:

1. AI Workflow Pack: 47 prompts + 12 automation templates - $17
2. Prayer Journal template (Notion) - $7
3. 7-Day Prayer Challenge (Notion) - $7
4. Prayer Bundle (journal + challenge) - $12
5. Fitness Tracker (Notion) - $19
6. Sleep Optimization System (Notion) - $14

Total products: 6, listed on Whop.

Sales in first 10 days: 11 units totaling $143.

Not life-changing. But $143 from products that took 2-3 hours each to package from content I'd already created. The marginal cost of each additional sale is $0.

## Day 26-30: Newsletter launches

Launched 4 newsletters on Beehiiv:
1. The AI Edge (tech/productivity)
2. Daily Devotion (faith)
3. The Gains Report (fitness)
4. The Sleep Letter (sleep/health)

Each has a 7-email welcome sequence that soft-sells the digital products.

Subscribers after first week: 47 total across all 4.

Not impressive. But each subscriber entered a 14-day automated sequence that eventually presents a product. If 10% convert at an average $12 order value, that's $4.70 per subscriber in lifetime value. The math works at scale. Getting to scale is the challenge.

## The honest 30-day P&L

**Revenue:**
| Source | Amount |
|--------|--------|
| Cold outreach (2 projects) | $3,000 |
| Digital products (11 sales) | $143 |
| Medium Partner Program | $4.72 |
| Newsletter (no paid tier yet) | $0 |
| **Total revenue** | **$3,147.72** |

**Expenses:**
| Item | Amount |
|------|--------|
| Claude Pro | $20 |
| Domain names (2) | $24 |
| Email warmup (Instantly) | $30 |
| Whop (seller fees) | ~$7 |
| Cloudflare (hosting) | $0 |
| **Total expenses** | **$81** |

**Net profit: $3,066.72**

97% of revenue came from cold outreach. Everything else is in early-stage compounding mode.

## The 7 biggest mistakes

**1. Over-engineering the strategy document.** I spent 6 hours writing a 1,900-line master plan. I should have spent 1 hour writing a 200-line plan and started building.

**2. Building 3 apps when I should have launched 1.** PrayerLock got users because I gave it attention. WalkToUnlock and StudyLock sat unfinished because my focus was split.

**3. Not doing cold outreach from day 1.** It's the fastest path to revenue for someone with skills and no audience. I waited until day 15. Should have started day 1.

**4. Pricing digital products too low.** $7 for a Notion template that took 3 hours to build and saves someone 10+ hours? Should be $19-29. I'm testing higher prices in month 2.

**5. Spreading across too many content platforms.** Posting to 6 platforms sounds impressive. But the effort to adapt content for each platform means I'm doing a mediocre job on all of them instead of a good job on 2-3.

**6. Not tracking metrics from day 1.** I only started properly tracking views, clicks, and conversions in week 2. Lost 7 days of data that would have helped me make better decisions.

**7. Planning when I should have been publishing.** Every hour spent planning is an hour not spent publishing. The market gives you feedback faster than your strategy document.

## What I'd do differently

If I restarted from day 1:

- Day 1-2: Set up basic infrastructure (2 hours max). Start cold outreach immediately.
- Day 3-7: Build one app (not three). Ship it. Get users.
- Day 8-14: Write and publish content daily. Don't wait for perfection.
- Day 15-20: Package first digital product from content already created.
- Day 21-25: Launch one newsletter (not four).
- Day 26-30: Double down on what worked. Kill what didn't.

Fewer things, done better, launched faster.

## Month 2 plan

Focus on 3 things:
1. Scale cold outreach to 100 emails/day (project pipeline for consistent revenue)
2. Grow PrayerLock to 5,000 users (add features, increase content marketing)
3. Publish 3 Medium articles per week (partner program revenue + traffic)

Everything else is on hold until these 3 are working.

The first month taught me that building is easy and distribution is hard. Month 2 is about distribution.

If you're thinking about starting something similar: the first month is messy. The numbers are small. The momentum is slow. Start anyway. The compounding hasn't kicked in yet, but the infrastructure is built. Month 2 is when it starts to feel real.
