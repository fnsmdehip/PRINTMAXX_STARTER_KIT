# Content Machine: Template Specification

## Overview
7 interconnected databases covering the full content lifecycle: ideation, creation, repurposing, scheduling, publishing, and performance tracking across 6 platforms.

---

## Database 1: Content Pipeline (Master Database)

### Properties

| Property | Type | Details |
|----------|------|---------|
| Content Title | Title | Hook or working title |
| Status | Select | Options: Idea, Outline, Draft, Edit, Scheduled, Published, Analyzed |
| Platform | Multi-select | Options: X/Twitter, YouTube, TikTok, LinkedIn, Newsletter, Blog |
| Content Type | Select | Options: Post, Thread, Video, Short, Carousel, Article, Newsletter Issue, Story, Reel, Podcast Clip |
| Publish Date | Date | Scheduled or actual publish date (with time) |
| Week Number | Formula | `"W" + format(toNumber(formatDate(prop("Publish Date"), "w")))` |
| Day of Week | Formula | `formatDate(prop("Publish Date"), "dddd")` |
| Topic | Select | User-defined. Pre-loaded: Building in Public, Tutorial, Opinion/Hot Take, Case Study, Behind the Scenes, Tools/Resources, Wins/Revenue, Mistakes/Lessons |
| Hook | Text | Opening line (first 280 chars for X/Twitter) |
| Body | Text (long) | Full content body or script |
| CTA | Text | Call to action (link, follow, reply prompt) |
| Media Required | Multi-select | Options: None, Image, Video, Screenshot, Screen Recording, Carousel Slides, Thumbnail |
| Media Files | Files & Media | Attached assets |
| Optimal Post Time | Text | e.g., "8:00 AM EST" - platform-specific |
| Hook Source | Relation → Hook Library | Which hook template was used |
| Repurposed From | Relation → Content Pipeline (self) | Original content piece |
| Repurposed Into | Relation → Content Pipeline (self) | Derivative content pieces |
| Linked Week | Relation → Weekly Themes | Connected to weekly theme |
| Views | Number | Post views/impressions |
| Engagement | Number | Likes + comments + shares + saves |
| Clicks | Number | Link/profile clicks |
| Saves | Number | Bookmarks/saves |
| Engagement Rate | Formula | `if(prop("Views") > 0, round(prop("Engagement") / prop("Views") * 10000) / 100, 0)` |
| Performance Tier | Formula | `if(prop("Engagement Rate") >= 5, "Viral", if(prop("Engagement Rate") >= 3, "Strong", if(prop("Engagement Rate") >= 1, "Average", if(prop("Views") > 0, "Weak", ""))))` |
| Repurpose Count | Rollup | Count of Repurposed Into relation |
| Needs Repurposing | Formula | `prop("Performance Tier") == "Viral" or prop("Performance Tier") == "Strong") and prop("Repurpose Count") == 0` |

### Views

1. **90-Day Calendar** (Calendar) - Publish Date view, color-coded by Platform. Shows 13 weeks.
2. **Pipeline Board** (Board/Kanban) - Grouped by Status. Cards show Title, Platform pills, Publish Date.
3. **This Week** (Table) - Filter: Publish Date = this week. Sorted by date/time. Shows Status, Platform, Hook.
4. **By Platform** (Table) - Grouped by Platform. Sorted by Publish Date descending.
5. **Ideas Bank** (Gallery) - Filter: Status = Idea. Sorted by created date descending. Shows Topic, Platform suggestions.
6. **Performance** (Table) - Filter: Status = Published or Analyzed. Sorted by Engagement Rate descending. Shows Views, Engagement, Clicks, Performance Tier.
7. **Needs Repurposing** (Table) - Filter: Needs Repurposing = true. High-performing content not yet repurposed.
8. **Content by Type** (Table) - Grouped by Content Type. Shows count and average engagement rate per type.

---

## Database 2: Weekly Themes

### Properties

| Property | Type | Details |
|----------|------|---------|
| Theme | Title | e.g., "Building in Public Week" |
| Week Number | Number | 1-13 (covers 90 days / 13 weeks) |
| Start Date | Date | Monday of the week |
| End Date | Formula | `dateAdd(prop("Start Date"), 6, "days")` |
| Focus Platform | Select | Which platform gets extra focus this week |
| Theme Description | Text | What this week is about, key angles |
| Linked Content | Relation → Content Pipeline | All content pieces for this week |
| Content Count | Rollup | Count of Linked Content |
| Published Count | Rollup | Count where Status = Published |
| Completion Rate | Formula | `if(prop("Content Count") > 0, round(prop("Published Count") / prop("Content Count") * 100), 0)` |
| Target Posts | Number | How many posts planned this week |

### Views

1. **13-Week Overview** (Table) - All 13 weeks, showing Theme, Target Posts, Published Count, Completion Rate.
2. **Current Week** (Page) - Filtered to current week. Shows theme details and linked content.
3. **Timeline** (Timeline) - Start Date to End Date. Visual week-by-week theme plan.

### Pre-loaded Themes (13 weeks)

| Week | Theme | Focus |
|------|-------|-------|
| 1 | Foundation Week | Setting up content systems, behind-the-scenes |
| 2 | Audience Research | Questions, polls, engagement-first content |
| 3 | Value Bomb Week | Tutorial-heavy, educational content |
| 4 | Story Week | Personal stories, lessons learned, journey posts |
| 5 | Tool Stack | Tool reviews, comparisons, stack reveals |
| 6 | Contrarian Week | Hot takes, unpopular opinions, debate starters |
| 7 | Case Study Week | Results, data, proof-based content |
| 8 | Community Week | Collab content, replies to others, engagement |
| 9 | Product Week | Launches, promotions, offers |
| 10 | Education Series | Multi-part tutorials, deep dives |
| 11 | Behind the Scenes | Process reveals, workspace, daily routine |
| 12 | Optimization | What worked, what didn't, pivots |
| 13 | Review and Plan | Quarter review, next quarter planning |

---

## Database 3: Hook Library

### Properties

| Property | Type | Details |
|----------|------|---------|
| Hook Text | Title | The actual hook/opening line |
| Hook Type | Select | Options: List, Story, Contrarian, Data, Question, Command, Cliffhanger, Social Proof, Prediction, Comparison |
| Target Engagement | Multi-select | Options: Saves, Shares, Replies, Clicks, Follows |
| Platform Fit | Multi-select | Options: X/Twitter, YouTube, TikTok, LinkedIn, Newsletter, Blog |
| Topic Match | Multi-select | Same topic tags as Content Pipeline |
| Example Post | Text | Link or text of a post that used this hook successfully |
| Times Used | Rollup | Count of Content Pipeline entries using this hook |
| Avg Performance | Rollup | Average Engagement Rate of linked content |
| Source | Text | Where you found this hook (account, post link) |
| Personal Best | Checkbox | This hook worked especially well for YOUR content |

### Views

1. **All Hooks** (Table) - Sorted by Hook Type. Shows Hook Text, Platform Fit, Target Engagement.
2. **By Type** (Board) - Grouped by Hook Type. Card shows Hook Text and Platform pills.
3. **Hook Roulette** (Gallery) - Sort: Random (Notion sorts by created time, but Gallery with shuffle gives variety). No filters. Click any card for inspiration.
4. **Best Performers** (Table) - Sorted by Avg Performance descending. Filter: Times Used > 0.
5. **Unused** (Table) - Filter: Times Used = 0. Hooks you haven't tried yet.
6. **By Platform** (Table) - Grouped by Platform Fit.

### Pre-loaded Hooks (120 entries)

**List Hooks (24):**
- "7 tools that saved me 10 hours this week"
- "5 mistakes I made in my first 90 days"
- "3 things nobody tells you about [topic]"
- "the 4 apps I use every single day"
- "9 free tools that replace $500/month in subscriptions"
- (19 more variations across topics)

**Story Hooks (24):**
- "I spent 6 months building something nobody wanted. here's what I learned."
- "last week a stranger sent me $500. here's why."
- "I almost quit 3 months ago. glad I didn't."
- "my first client paid me $50. my last client paid me $5,000. the difference:"
- "I got fired. best thing that ever happened."
- (19 more variations)

**Contrarian Hooks (24):**
- "stop making content calendars. they're killing your creativity."
- "unpopular opinion: you don't need a morning routine"
- "everyone says 'just start.' that's terrible advice. here's better advice:"
- "the hustle culture guys won't tell you this"
- "'consistency is key' is the worst advice for beginners"
- (19 more variations)

**Data Hooks (24):**
- "I analyzed 500 viral posts. here's what they all have in common."
- "I tracked every hour for 30 days. the results surprised me."
- "84% of solopreneurs make this mistake in their first year"
- "I A/B tested 50 hooks. the winner got 12x more engagement."
- "my last 100 posts: what worked, what flopped, the data"
- (19 more variations)

**Question Hooks (24):**
- "why does nobody talk about this?"
- "what would you do with an extra 3 hours every day?"
- "is anyone else frustrated by this?"
- "what's the one tool you'd keep if you could only keep one?"
- "why are we still doing [outdated thing] in 2026?"
- (19 more variations)

---

## Database 4: Viral Post Templates

### Properties

| Property | Type | Details |
|----------|------|---------|
| Template Name | Title | e.g., "The Listicle Thread" |
| Platform | Select | X/Twitter, YouTube, LinkedIn, Newsletter |
| Format | Select | Options: Thread, Single Post, Carousel, Video Script, Newsletter, Article |
| Structure | Text (long) | Step-by-step structure with placeholders |
| Example | Text (long) | Real example of this template in action (link or text) |
| Why It Works | Text | Psychology behind the format |
| When to Use | Text | Best situations/topics for this template |
| Times Used | Rollup | Count of linked content |

### Pre-loaded Templates (38)

**X/Twitter (15):**
1. The Listicle Thread (7-10 tweets, each item = 1 tweet)
2. The Story Thread (personal story arc: hook > struggle > breakthrough > lesson)
3. The Breakdown (analyze something: tool, business, strategy)
4. The Contrarian Take (bold claim > evidence > reframe)
5. The Tutorial Thread (step-by-step how-to, screenshots)
6. The Revenue Report (transparent numbers, what worked/didn't)
7. The "I spent X hours" Thread (research dump)
8. The Challenge Post (dare the audience)
9. The Before/After (transformation)
10. The Hot Take + Caveat (provocative opener, nuanced followup)
11. The "Stop Doing X" Post (problem > alternative)
12. The Stack Reveal (my tools, my setup, my workflow)
13. The Mistake Thread (things I got wrong)
14. The Reply Bait (question + engagement trigger)
15. The Screenshot Thread (proof-based, visual)

**LinkedIn (10):**
1. The Personal Story (vulnerability + professional lesson)
2. The Framework Post (named framework with steps)
3. The Data Post (chart/stat + insight)
4. The "I was wrong" Post (humility + lesson)
5. The Carousel (10 slides, visual)
6. The Comment Magnet (question + relatable pain)
7. The Announcement (launch/milestone)
8. The Industry Opinion (take on trending topic)
9. The Repost + Add (share someone's post + your angle)
10. The "Hiring for" + Value (recruitment + give value)

**Newsletter (8):**
1. The Deep Dive (one topic, 1500 words, comprehensive)
2. The Curated List (5-10 items with commentary)
3. The Case Study (one business/person, dissected)
4. The Tool Review (honest review with alternatives)
5. The Weekly Roundup (what happened + commentary)
6. The Q&A (answer subscriber questions)
7. The Behind-the-Scenes (show your process)
8. The Prediction (what's coming next in your niche)

**YouTube Titles/Thumbnails (5):**
1. The "I Did X for Y Days" (challenge format)
2. The "How I Made $X" (proof-based)
3. The Comparison (X vs Y)
4. The Tutorial (How to X in Y Minutes)
5. The Reaction/Review (reacting to trending thing)

---

## Database 5: Repurposing Tracker

This is implemented through the self-relations in Content Pipeline (Repurposed From / Repurposed Into), but has a dedicated view page.

### Dedicated Page: Repurposing Hub

**Section 1: Repurposing Matrix**
Table showing:
- Original content (parent pieces only, where Repurposed From is empty)
- Repurpose Count per piece
- Performance of original vs derivatives

**Section 2: Repurpose Opportunities**
Linked view from Content Pipeline with filter: Needs Repurposing = true
- Shows high-performing content that hasn't been turned into anything else

**Section 3: Repurpose Playbook (Static content block)**

```
Blog Post →
  - Twitter thread (break into 7-10 tweets)
  - LinkedIn post (rewrite intro, add personal angle)
  - Newsletter section (excerpt + link)
  - TikTok script (60-sec summary of key point)
  - YouTube Short (same as TikTok with screen recording)
  - Carousel (key points as slides)

YouTube Video →
  - Blog post (transcribe + edit)
  - Twitter thread (key takeaways)
  - 3-5 YouTube Shorts (clip best moments)
  - 3-5 TikToks (same clips, different captions)
  - Newsletter deep dive (expand one section)

Twitter Thread →
  - Blog post (expand each tweet to a paragraph)
  - LinkedIn post (rewrite for professional tone)
  - Newsletter (add context + data)
  - Carousel (one tweet per slide)

Newsletter →
  - Twitter thread (compress key points)
  - Blog post (expand with SEO keywords)
  - LinkedIn article (professional reframe)
```

---

## Database 6: Analytics Dashboard

This is a page with linked database views, not a separate database. It pulls from Content Pipeline.

### Dashboard Page Layout

**Row 1: Key Metrics (3 columns)**
- Total Posts Published (count where Status = Published, this month)
- Average Engagement Rate (across all published content, this month)
- Best Performing Post (highest Engagement Rate this month, linked)

**Row 2: Platform Performance (Table)**
Linked view from Content Pipeline:
- Grouped by Platform
- Columns: Post Count, Total Views, Total Engagement, Avg Engagement Rate
- Filter: Status = Published or Analyzed
- Sorted by Avg Engagement Rate descending

**Row 3: Content Type Performance (Table)**
Linked view from Content Pipeline:
- Grouped by Content Type
- Same columns as above
- Identifies which content types (thread, video, post) perform best

**Row 4: Weekly Trend (Table)**
Linked view grouped by Week Number:
- Posts per week, total engagement per week
- Shows if you're trending up or down

**Row 5: Top 10 Posts (Table)**
Linked view sorted by Engagement Rate descending, limit 10
- Shows title, platform, views, engagement, engagement rate, performance tier

**Row 6: Double Down Indicators**
Linked view filtered to Performance Tier = "Viral" or "Strong"
- These are your winning formats. Make more of these.

---

## Database 7: Content Bank

### Properties

| Property | Type | Details |
|----------|------|---------|
| Idea | Title | Short description of the idea |
| Source | Text | Where you found it (URL, screenshot, conversation) |
| Source File | Files & Media | Screenshot, bookmark, etc. |
| Topic | Select | Same topic tags as Content Pipeline |
| Platform Fit | Multi-select | Which platforms this idea works for |
| Content Type | Select | What format would work best |
| Urgency | Select | Options: Trending (post within 48h), Timely (this week), Evergreen (anytime), Seasonal (specific date) |
| Potential | Select | Options: High, Medium, Low |
| Promoted to Pipeline | Checkbox | Whether this idea has been moved to Content Pipeline |
| Notes | Text (long) | Additional context, angles, related ideas |
| Date Added | Created time | Auto-populated |

### Views

1. **Inbox** (Gallery) - Filter: Promoted = false. Sorted by Date Added descending. Quick scan of unprocessed ideas.
2. **By Topic** (Board) - Grouped by Topic. Shows idea count per topic.
3. **Trending** (Table) - Filter: Urgency = Trending. Sorted by Date Added descending. Post these NOW.
4. **High Potential** (Table) - Filter: Potential = High. Sorted by Urgency.
5. **Promoted** (Table) - Filter: Promoted = true. Archive of ideas that became content.

---

## Cross-Database Relations Map

```
Content Pipeline ←→ Hook Library (hook source)
Content Pipeline ←→ Content Pipeline (self: repurposing chain)
Content Pipeline ←→ Weekly Themes (content-theme alignment)
Viral Post Templates → Content Pipeline (loose reference, not direct relation)
Content Bank → Content Pipeline (manual promotion, not auto-relation)
```

---

## 90-Day Pre-Structure

The template comes with 13 weekly theme entries pre-created and a suggested posting cadence:

**Default Cadence:**
- X/Twitter: 1 post/day (7/week)
- LinkedIn: 3 posts/week
- Newsletter: 1/week
- YouTube: 1/week
- TikTok: 3/week
- Blog: 1/week

**Total: ~22 pieces per week, many are repurposed from the same source content**

Each week in the 90-day structure has placeholder content entries pre-created with the correct platform tags and dates, set to "Idea" status. The user fills in the actual content as they go.

---

## Setup Instructions

1. Duplicate this template to your Notion workspace
2. Review the 13-week theme plan (customize if needed)
3. Set your posting cadence per platform (adjust placeholder entries)
4. Browse the Hook Library for inspiration
5. Start dropping ideas into the Content Bank
6. Promote ideas to the Pipeline and start creating
7. After publishing, add metrics (views, engagement, clicks) within 48 hours
8. Check the Analytics Dashboard weekly to see what's working
9. Use the Repurposing Hub to find high-performing content to turn into more content

Time to setup: 10 minutes
