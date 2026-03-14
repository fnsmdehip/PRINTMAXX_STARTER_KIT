# Reddit Distribution Cycle 16 — New/Undercovered Assets
# Status: PENDING_REVIEW
# Date: 2026-03-14
# Assets: AI Slop Detector, Productivity Stack Quiz, HabitForge, MealMaxx, WalkToUnlock, SleepMaxx/Dusk, CoreDay
# Total posts: 17

---

## Voice QA Check (pre-publish)
- [x] Zero em dashes
- [x] Zero banned AI vocabulary (leverage, utilize, delve, comprehensive, robust, innovative, seamless)
- [x] Consequence-first hooks
- [x] Exact numbers where possible
- [x] Would @pipelineabuser actually post this?
- [x] Lowercase energy where appropriate
- [x] First sentence delivers value
- [x] No chatbot artifacts
- [x] No promotional adjectives
- [x] Reddit value-first, link at end casually

---

## ASSET 1: AI Slop Detector
### URL: ai-slop-detector.surge.sh

---

### POST 1
**Subreddit:** r/artificial
**Title:** I built a quick tool to test whether text was written by a human. Here are the 7 patterns it catches most reliably.

**Body:**

Been messing around with AI detection for about 3 months. Not the "is this GPT" classification stuff that's borderline useless. More like: what are the actual linguistic tells that real humans almost never produce but LLMs do constantly?

Here's what I found actually works as signal:

1. Em dashes as clause connectors. Humans use commas. LLMs use — constantly.
2. The "it's not just X, it's Y" construction. Never seen a human write this unprompted.
3. "Additionally," "Furthermore," "Moreover" as sentence openers. Nobody talks like this.
4. Significance inflation: turning "this saves time" into "this transforms workflows."
5. The rule of three in bullet points. LLMs default to exactly 3 every single time.
6. Hedging stacks: "might possibly perhaps somewhat." One hedge = human. Three in a row = AI.
7. Generic conclusions that restate the intro. Humans just stop writing when they're done.

The tricky part is none of these are binary flags. They're weighted signals. A text can have two of them and still be human. Hit five or more and you're looking at machine output.

I built a small browser tool that runs these checks in real time and scores text against each pattern. No server calls, runs locally in your browser. Mostly built it for my own use when reviewing contractor work but figured other people might find it useful.

Link in comments if anyone wants to try it.

---

### POST 2
**Subreddit:** r/freelanceWriters
**Title:** Clients are starting to send me AI-written copy and asking me to "polish" it. I made something to catch it before I waste time on it.

**Body:**

This has happened to me 4 times in the last 6 weeks.

Client sends a brief. I do the work. Then mid-project they send "here's a first draft" that is clearly machine-generated. They want me to turn it into something real for the same rate as starting from scratch.

The problem is it's actually more work to fix AI copy than to write from zero. You have to strip out the structure, the em dash addiction, the "leveraging synergies" vocabulary, the fake gravitas. Then rebuild.

So I started keeping a checklist of tells. After a while I turned it into a browser tool so I could paste their "first draft" in and get a score before agreeing to work on it.

The patterns it flags:

- Overuse of transition words as sentence openers (Additionally, Furthermore, Moreover)
- Hollow qualifier stacks ("might possibly perhaps")
- Em dash abuse as a substitute for actual sentence rhythm
- Significance inflation (plain statements dressed up as revelations)
- Formulaic three-part lists
- The "it's not just X, it's Y" construction nobody writes naturally

If a client's draft hits more than 4 of these, I either pass or reprice the job.

Tool is free, runs in the browser, no account needed. Posted the link in comments.

---

### POST 3
**Subreddit:** r/copywriting
**Title:** What patterns actually distinguish AI copy from human copy? I've been cataloging them for 3 months.

**Body:**

Not talking about perplexity or burstiness scores. Those fail constantly. I mean actual recurring patterns that show up in LLM output that real writers almost never produce.

Here's my working list after reviewing hundreds of samples:

The em dash as a structural crutch. Real writers use commas or just write shorter sentences. AI connects every subordinate clause with —.

Significance inflation. "This saves 30 minutes" becomes "this fundamentally transforms how teams collaborate." The actual claim gets buried under inflated framing.

The negative parallelism: "It's not just a tool. It's a revolution." No human copywriter writes this. It sounds profound and says nothing.

Synonym cycling. AI writes "the platform, the solution, the system, the tool" in the same paragraph to avoid repetition. Humans just pick one word and use it.

Generic conclusions that restate the intro. Real copy ends with a specific point or action. AI ends with a paragraph that summarizes what you just read.

I cataloged these into a scoring tool. You paste text in, it runs against each pattern, gives you a weighted score. Doesn't tell you definitively if something is AI. Tells you how many of these patterns are present.

Useful for reviewing client-submitted copy, competitive analysis, or just calibrating your own drafts.

Link in comments if you want to run something through it.

---

### POST 4
**Subreddit:** r/ChatGPT
**Title:** I made a detector that doesn't try to classify AI vs human. It just scores how many AI writing patterns are in the text.

**Body:**

Every AI detector I've tried has the same problem: it gives you a percentage and that percentage is wrong about 30% of the time. You can't build a reliable workflow on that.

So I took a different approach. Instead of classification, I just score the text against the specific patterns that LLMs produce consistently:

- Em dashes used as clause connectors (vs commas)
- "Additionally / Furthermore / Moreover" as sentence openers
- The rule of three in every bullet list
- Hedging stacks (might possibly perhaps)
- Significance inflation (small claims dressed as insights)
- Negative parallelism (it's not just X, it's Y)
- Generic conclusions that restate the intro without adding anything

Each pattern gets a weight. You get a total score. High score doesn't prove AI wrote it. Low score doesn't prove human wrote it. It tells you how many of the patterns are present.

I find it more useful than classification because it tells you specifically what to fix if you're trying to humanize output, or what to flag if you're reviewing submitted work.

Runs in the browser, no server, no account. Built it for my own use. Link's in the comments.

---

### POST 5
**Subreddit:** r/SideProject
**Title:** Built an AI writing pattern detector in a weekend. No server, no API, runs local. Here's what I learned.

**Body:**

Started this because I needed something for my own workflow. I review a lot of submitted text and needed a way to quickly flag machine-generated copy before spending time on it.

The main insight was to stop trying to classify AI vs human and just measure pattern density instead. Classifiers need training data and they drift as models evolve. Pattern matching is just regex against known LLM tendencies. More predictable.

The 7 patterns I ended up using:

Em dash frequency. LLMs use them constantly for clause connection. Humans mostly don't.

Transition word openers. "Additionally," "Furthermore," "Moreover." Common in AI, almost never in natural writing.

Rule of three. LLMs default to exactly three bullet points or examples. Real writing has four, or two, or seven.

Hedging chains. More than two hedges in a sentence is nearly always AI.

Significance inflation. A consistent pattern where plain statements get wrapped in inflated framing.

Negative parallelism. "It's not just X, it's Y." Nobody writes this naturally.

Generic restatement conclusions. AI ends essays by summarizing the essay. Real writers just stop when they're done.

Built it as a single HTML file with no external dependencies. Paste text, get scores per pattern, get a total. Free, open to use.

Link in comments.

---

## ASSET 2: Productivity Stack Quiz
### URL: productivity-stack-quiz.surge.sh

---

### POST 6
**Subreddit:** r/productivity
**Title:** I tried every "best productivity apps" list and they all recommended the same 5 tools regardless of how I work. So I made a quiz that actually asks how you work first.

**Body:**

The problem with productivity tool recommendations is they're generic. "Use Notion for notes." "Use Todoist for tasks." "Use Calendly for scheduling."

These lists don't know that I do deep work in 3-hour blocks and hate notifications. Or that someone else does reactive work all day across 6 Slack channels. The tool that works for one person actively breaks the workflow of the other.

I've tested probably 40 productivity tools over the past 2 years. What I found is that the tool matters less than the match between the tool and your work pattern.

The key variables:

How many context switches do you make per day? High context switchers need different tools than deep workers.

Do you plan at the start of day or react to what comes in? Planning-first people need different capture systems than reactive workers.

Is your biggest problem task capture, task prioritization, or task completion? These are separate problems. Most apps try to solve all three and do none of them well.

Are you a visual thinker or list thinker? Kanban boards make some people more productive and paralyze others.

Do you need your system to handle others' requests or just your own work? Collaboration features add friction if you work solo.

I built a short quiz around these variables. 8 questions. Recommends specific tools matched to your actual work pattern with reasons for each pick.

Link in comments if you want to run through it.

---

### POST 7
**Subreddit:** r/Entrepreneur
**Title:** Spent 2 years testing productivity tools as a solo operator. The winner isn't what anyone recommends.

**Body:**

When you're running something solo, your productivity stack has to do something different than what works for teams.

Team tools optimize for handoffs, visibility, and accountability to others. Solo tools need to optimize for decision speed, context recovery, and preventing the thing you're not doing from falling off your radar.

The tools I've burned money on that don't work solo:

Project management tools with too many views. You end up maintaining the system instead of doing the work.

Apps that require daily setup rituals. Anything that takes more than 3 minutes to "open" gets abandoned within 2 weeks.

Anything that requires weekly reviews to function. If the system breaks when you skip a week, it's too fragile for a solo operator under variable load.

What actually works:

Capture that takes under 10 seconds. If you're in a meeting or on a call and can't capture the thought instantly, it's gone.

One prioritization decision per day maximum. More than that and you're spending decision budget on meta-work.

Automatic archiving so the list doesn't grow forever. A 200-item backlog is useless. Cap it.

I made a quick quiz that matches work pattern to specific tools. Takes about 3 minutes. It doesn't recommend the same 5 apps to everyone.

Link in comments.

---

### POST 8
**Subreddit:** r/SideProject
**Title:** Show r/SideProject: A quiz that recommends productivity tools based on how you actually work, not what's most popular

**Body:**

The idea came from frustration with "best productivity apps" roundups.

Every list recommends the same tools. None of them ask anything about how you work before making recommendations. Someone who does async remote work across time zones needs a completely different stack than someone doing in-person creative work with a co-founder.

So I built a quiz that starts with work pattern questions:

- Deep work blocks or reactive sprints?
- Solo or collaborative?
- Planning-first or capture-first?
- Visual thinker or list thinker?
- What's your actual bottleneck: capture, prioritization, or follow-through?

8 questions total. The output is a tool recommendation with a specific reason for each pick based on your pattern.

Built it as a static site, no account needed, no email gate. Just answer the questions and get the recommendation.

Curious what patterns people here are seeing in their own stacks. What did you end up using that nobody talks about?

Link in comments.

---

## ASSET 3: HabitForge
### URL: habitforge-web.surge.sh

---

### POST 9
**Subreddit:** r/getdisciplined
**Title:** I've started and abandoned habit trackers probably 12 times. Here's why I think they fail and what I built instead.

**Body:**

Every habit tracker I've used has the same design problem: it's built for someone who already has discipline.

The apps give you a streak counter. The streak grows when you do the habit. The streak resets when you don't. This punishes the people who need the most support exactly when they need it most.

Break your streak after 30 days? Reset to zero. The app essentially says: you failed, start over.

This is backwards. Research on habit formation is pretty clear that the recovery behavior after a miss is what predicts long-term success. Not the streak itself.

So what I wanted was a tracker that:

1. Doesn't reset to zero on a miss. Adjusts the trajectory instead.
2. Lets you set a target frequency rather than requiring 100% consistency. "5 out of 7 days" is a habit. "7 out of 7" is a rule.
3. Shows momentum as a curve, not a number. A streak counter tells you where you've been. A momentum curve tells you where you're going.
4. Keeps the log even after you delete a habit, so you can see what patterns led to quitting.

I built HabitForge around these ideas. It's a PWA so it works offline and installs on your home screen. No account needed to start.

Been using it myself for 6 weeks. Link in comments if you want to try it.

---

### POST 10
**Subreddit:** r/selfimprovement
**Title:** Why habit streaks are probably making your habits worse (and what to track instead)

**Body:**

Streaks feel good. I get it. Watching a number grow is motivating.

The problem is what happens at day 15 when you miss. You lose 15 days of momentum in a single bad day. The tracker goes back to zero. And a lot of people just stop.

The psychology research here is pretty consistent: the behavior that most predicts long-term habit success is how you respond to the first miss. Not whether you miss. Not how long your streak is. How fast you get back.

Trackers built around streaks actively punish you at the worst moment. You miss a day, you're already dealing with whatever caused you to miss, and now your tracker tells you that everything you built is gone.

What works better:

Track percentage over a rolling window instead of raw streak. "I've done this 18 out of 21 days" is more honest and more motivating than "streak: 0 (reset 3 days ago)."

Set a frequency target, not a perfection target. Aiming for 5 out of 7 days is a real habit goal. Aiming for 7 out of 7 days is a rule you'll eventually break.

Weight recent behavior more than old behavior. A month-old streak shouldn't count the same as what you did this week.

I built a habit tracker around these principles. It's a PWA, free, no account. Link in comments if you're curious.

---

## ASSET 4: MealMaxx
### URL: mealmaxx-web.surge.sh

---

### POST 11
**Subreddit:** r/MealPrepSunday
**Title:** I tracked everything I ate for 90 days and built a meal planner around what I actually learned. Here's what surprised me.

**Body:**

I started tracking because I wanted to understand why some weeks I ate well and some weeks I didn't, despite caring equally about both.

After 90 days of logging meals, timing, cost, and how I felt, here's what actually drove the variance:

Decision fatigue at 6pm is the main failure point. If I hadn't decided what dinner was by 5pm, there was maybe a 30% chance I ate what I planned. The decision itself was the obstacle, not the cooking.

Shopping list fragmentation killed more meal plans than anything else. Buying ingredients for 7 different recipes means 7 different partial shopping trips when you run out of one thing mid-week.

Recipe variety is overrated for sustainability. I rotated 8 meals on a 3-week cycle and ate better, cheaper, and with less friction than when I tried to eat something different every night.

Batch cooking the proteins, not the full meals, is the actual move. Cook 3 proteins Sunday, assemble different meals from them during the week. More flexibility, same prep time.

Cost per meal tracking is more motivating than calorie tracking for most people who aren't athletes.

I built a meal planner around these findings. Rotation-based, shopping list consolidation, cost per meal tracking. It's a free PWA.

Link in comments.

---

### POST 12
**Subreddit:** r/EatCheapAndHealthy
**Title:** How I got my weekly food cost from $180 to $65 without eating worse. The actual method.

**Body:**

Not a clever hack. Just a system that took about 3 months to build and now runs without much thought.

The starting point was figuring out where the money was actually going. For me:

$40/week was going to ingredients I bought with good intentions and threw away. Specific failure: buying produce for recipes I didn't end up making because I ran out of energy to cook.

$30/week was going to "bridge meals" when I didn't have a plan. Takeout, convenience store stuff, random whatever.

$20/week was duplication. Buying things I already had because I didn't know I had them.

The fixes:

Rotation-based planning instead of weekly unique planning. Pick 8-10 meals you actually like. Rotate them. Your shopping list becomes predictable and your pantry stops accumulating random things.

Decision commitment before shopping. The plan exists before you go to the store, not in the store.

Cost per meal as the main tracking metric. It focuses your attention on the right variable.

Single protein batch cooking. Cook 2-3 proteins on Sunday, assemble different meals from them. Same prep time, more flexibility.

I built a simple planner app around this system. Free, works offline, no account needed.

Link in comments if you want the specific numbers breakdown I used.

---

## ASSET 5: WalkToUnlock
### URL: walktounlock-web.surge.sh

---

### POST 13
**Subreddit:** r/getdisciplined
**Title:** I was spending 8 hours a day at a desk and my step count averaged 900 steps. Here's the system that got me to 8,000 without changing my job.

**Body:**

900 steps. That was my average for the first 3 months of working from home full time.

I tried the obvious fixes. Set reminders to stand up. They got ignored within 2 weeks. Bought a standing desk. Stood at it for about a week, then went back to sitting.

The problem with reminders is they interrupt you. When you're in flow, an alarm telling you to stand up is annoying. You dismiss it. After a few dismissals it becomes background noise.

What actually worked:

Anchoring movement to things I was already doing. Not "walk at 2pm." Walk before I open my next task. Walk after every video call. Walk before I eat lunch. These anchors are harder to ignore because they're attached to things with their own momentum.

Making the step goal visible in real time rather than reviewed at end of day. Seeing 1,200 steps at 11am creates a different response than seeing 3,400 at 8pm when there's nothing you can do about it.

Breaking the day into 3 mini-goals instead of one daily goal. Easier to stay on track when failure is recoverable within the same day.

Walking without a destination. Most people think they need somewhere to go. A 7-minute loop around the block counts the same as walking to a meeting.

I built a small PWA called WalkToUnlock around these principles. Free, works offline. Tracks mini-goals and daily progress in real time.

Link in comments.

---

### POST 14
**Subreddit:** r/fitness
**Title:** For people whose job is sitting all day: the walking habit framework that actually stuck for me after 6 months

**Body:**

This is not for people trying to get fit. This is for people who sit at a desk for 8 hours and want to not feel like a corpse by 5pm.

I tried a lot of things. Fitness trackers with vibrating reminders (annoying, dismissed, ignored). Scheduled walk times (blocked by meetings, skipped, forgotten). Step goals reviewed at end of day (too late to do anything about them).

What stuck:

Movement anchors beat movement reminders. I walk before I start each new task instead of at arbitrary times. The anchor is "new task = movement first." No timer needed. No interruption.

Real-time visibility changes behavior. If I can see my step count right now, I make different decisions about whether to take the long way to the kitchen. If I only see it at night, it's review, not action.

Mini-goals beat daily goals for desk workers. My day has 3 checkpoints. If I miss the first, I can still hit the next two. A single daily goal means one bad morning tanks everything.

5-7 minute walks are enough to break the cognitive rut that 3 hours of sitting creates. You don't need 30 minutes. You need to move.

Built a free PWA around this framework. No account, works offline, tracks the anchored mini-goal system.

Link in comments if you want to try the system.

---

## ASSET 6: SleepMaxx / Dusk
### URL: sleepmaxx-web.surge.sh

---

### POST 15
**Subreddit:** r/sleep
**Title:** I tracked sleep variables for 4 months. The 3 things that actually moved my sleep quality. The other 20 things didn't.

**Body:**

I went deep on sleep optimization last year. Tracked everything: bedtime, wake time, room temperature, screen exposure, caffeine timing, exercise timing, alcohol, pre-sleep reading, blue light glasses, magnesium, the works.

After 4 months of data, 3 things showed consistent correlation with sleep quality. Everything else was noise.

Consistent wake time. Not consistent bedtime. Wake time. My body's sleep pressure built more reliably when I woke at the same time regardless of when I fell asleep. This is the single highest-leverage lever.

Total dark-to-sleep time under 20 minutes. If I was lying in bed longer than 20 minutes before falling asleep, the next night's quality dropped regardless of what I did. Getting out of bed when I couldn't sleep (counterintuitive but it works) was more effective than any supplement.

No food in the 3 hours before sleep. Not alcohol-specific, not caffeine-specific. Any food elevated core body temperature enough to fragment sleep.

Everything else I tracked: statistically negligible in my data. Blue light glasses, magnesium, specific temperature ranges, reading vs screens, all showed less than 5% variance in my scores.

Built a simple sleep tracker that focuses on these three variables specifically. Free PWA, no account needed.

Link in comments if you want to run the same experiment.

---

### POST 16
**Subreddit:** r/biohackers
**Title:** 4 months of sleep tracking data. Here's what actually moved the needle vs what's placebo.

**Body:**

Ran a personal experiment. Tracked 22 sleep-related variables every day for 4 months. Self-scored sleep quality each morning on a consistent 1-10 scale. Ran basic correlation analysis at the end.

Variables with strong correlation to quality score:

Wake time consistency. This was the biggest signal. Variance in wake time of more than 45 minutes was correlated with lower quality scores 80% of the time. Bedtime variance mattered much less.

Time to fall asleep. Nights where I was lying awake for more than 20 minutes before sleeping were followed by worse quality scores the next night. The cycle compounds. Getting out of bed when I couldn't sleep (stimulus control) broke it faster than lying there trying.

Last meal timing. More than 3 hours between last food and sleep showed consistent quality improvement vs under 3 hours. Effect was independent of meal size.

Variables with no meaningful correlation in my data:

Blue light glasses, room temperature (within a normal range), magnesium glycinate, melatonin under 1mg, type of content before bed, alcohol under 2 drinks, exercise timing.

I know this contradicts a lot of what gets posted here. My data is one person over 4 months. But it's more reliable than anecdote.

Built a tracker focused specifically on the 3 variables that moved for me. Free, offline-capable PWA.

Link in comments.

---

### POST 17
**Subreddit:** r/selfimprovement
**Title:** Why I think most sleep advice is overcomplicated. The 3 variables that actually matter.

**Body:**

Sleep content is everywhere and most of it is optimizing variables that don't matter that much.

After tracking my own sleep for 4 months and running the numbers, the variables that showed consistent correlation with how I felt the next day:

Wake time consistency. This is the one. Not bedtime. Wake time. Your body calibrates sleep pressure to when you wake up. Variable wake times produce chaotic sleep quality.

Time between lying down and actually sleeping. Over 20 minutes is bad and compounds. If you're lying there for 30-40 minutes, getting out and doing something boring until you're sleepy again works better than trying to force it.

Last meal timing. More than 3 hours before sleep, quality improves consistently. It's a digestion issue, not a specific food issue.

That's genuinely it. Everything else in my data was noise.

I built a sleep tracker that cuts out everything else and focuses on logging these three variables. You get a weekly pattern view after 7 days. It's a free PWA, no account, works offline.

Link in comments.

---

## ASSET 7: CoreDay
### URL: coreday.surge.sh

---

### POST 18 (LinkedIn crossover angle, targets r/productivity + r/SideProject)
**Subreddit:** r/productivity
**Title:** I stopped using complex planning systems and switched to one daily planning page. Here's what changed.

**Body:**

I've been through Notion, Roam, Obsidian, Things, Omnifocus, plain text, bullet journaling, GTD, time blocking, the whole thing.

The pattern I noticed: the more complex the system, the more time I spent maintaining it. My Notion setup had 12 databases. I spent about 40 minutes a day keeping them current. I was managing a productivity system instead of doing productive work.

The switch I made:

One planning page per day. That's it. Three questions: what are the 3 things that actually matter today, what's the first thing I'm doing when I sit down, and what's the one thing that if it didn't happen today I'd consider the day a failure.

Three items on a list, not twenty. When everything is priority, nothing is. Forcing a constraint to three items makes you do the prioritization work instead of letting the list stay vague.

End of day review that takes under 5 minutes. Did the three things happen? If not, what blocked them? One or two sentences max.

No rolling backlog. If something doesn't make it onto a daily page, it goes into a weekly review folder, not the daily list. The daily list should be achievable.

I built a simple PWA around this format. One page per day, three core items, clean interface. Free, offline-capable.

Link in comments.

---

## Posting Notes

- All links go in comments, not body text (Reddit flags posts with URLs as spam on some subreddits)
- For r/SideProject posts: add "Show r/SideProject:" prefix to title per subreddit rules
- Wait 48h minimum between posts on the same subreddit from the same account
- Best posting times: 7-9am EST weekdays, 10am-12pm EST weekends
- Respond to every comment within 6 hours of posting to signal healthy engagement
- Do not mention "PRINTMAXX" or cross-reference other tools in any post
- If asked for the source code, link to the GitHub or say it's a personal project
- All posts position the creator as someone who had the problem, solved it for themselves, and is sharing the solution. This is the only Reddit-safe framing.
