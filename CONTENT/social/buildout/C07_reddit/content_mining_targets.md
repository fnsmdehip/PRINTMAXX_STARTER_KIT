# Reddit Content Mining — What to Extract and Where to Use It

## The Core Insight

Reddit is the world's largest collection of authentic pain points, working solutions, and real user language. Everything on it is a primary source.

The extraction play: mine Reddit for signal, convert it to content across platforms, let AI do the synthesis work.

---

## What You're Mining For

### 1. Pain Point Language (highest value)
Real language people use when describing their problems. This is your copy.

**What to look for:**
- Posts that start with "I hate how..." / "Why does X always..." / "I've tried everything and..."
- Comment threads where people explain their frustration in detail
- Questions that have 50+ upvotes (popular frustration = market gap)

**Where to use it:**
- Landing page headlines (use their exact words, not marketing-speak)
- Cold email subject lines
- Twitter hooks
- Product descriptions

**Example extraction:**
> Reddit post: "I've tried 6 different Notion templates and none of them actually work for how I think"

Becomes cold email subject line: "most Notion templates don't work for how you actually think"

---

### 2. Proven Solutions That Work
Posts where someone shares a working framework — these have already been validated by the community's upvotes.

**What to look for:**
- Posts with 500+ upvotes explaining a specific method
- Comments that got pinned or got 100+ upvotes explaining something
- "Here's exactly what I did" posts with actual steps

**Where to use it:**
- YouTube scripts (the framework becomes your video's structure)
- Newsletter content (synthesize 5 Reddit frameworks into one guide)
- Product content (Gumroad/Notion templates built from proven approaches)
- Blog posts / SEO articles (synthesize + add unique insight)

---

### 3. Proof Points and Numbers
Real data shared publicly. These become your credibility signals.

**What to look for:**
- "I made $X in Y timeframe" posts (even if you're skeptical of the number, the timeframe/method is useful)
- "conversion rate was X%" comments
- "after 90 days I saw X% improvement" reports

**Where to use it:**
- Product copy ("frameworks from Redditors who've hit $3K/mo")
- Content credibility ("multiple Reddit reports show 20-40% increase")
- Ad copy / landing page social proof

---

### 4. Trending Topics Before They're Mainstream
Reddit is 2-6 weeks ahead of mainstream media on tech/business trends.

**What to look for:**
- Threads about tools you haven't heard of getting 1K+ upvotes
- "Has anyone tried X" questions with lots of interest
- Heated debates about a platform change (signals algorithm shift)

**Where to use it:**
- YouTube video timing (rank on YouTube before the topic blows up on Google)
- Newsletter issues ("what's coming in X that most people don't know yet")
- Twitter threads (first-mover content on trending topics)

---

### 5. Objections and Skepticism
What people push back on when they see a product or idea.

**What to look for:**
- Critical comments on showcase posts ("the problem with this is...")
- "Red flag" threads ("what should I know before buying X")
- Negative reviews in comment sections

**Where to use it:**
- Pre-emptive FAQ on landing pages
- Email sequences (handle objections before they're raised)
- Product improvement (fix what Reddit complains about)

---

## Priority Mining Targets by Category

### For Content Creation

| Subreddit | What to mine | Output format |
|---|---|---|
| r/ChatGPT | Prompt techniques getting 1K+ upvotes | YouTube tutorial, Twitter thread |
| r/learnprogramming | Top questions in last 30 days | Blog post, course outline |
| r/Entrepreneur | Case studies with specific numbers | Newsletter issue, YouTube script |
| r/SideProject | Launch posts + comment feedback | Product improvement ideas |
| r/webdev | Tool debates (Tailwind vs CSS, Next vs Nuxt) | Comparison content, SEO articles |

### For Copywriting

| Subreddit | What to mine | Output format |
|---|---|---|
| r/personalfinance | How people describe their money problems | Landing page copy, email subject lines |
| r/Freelance | Frustrations with clients, platforms, rates | Service positioning, cold email |
| r/smallbusiness | Pain points with marketing, operations | B2B product copy |
| r/productivity | Specific things that "don't work" for them | Hook angles, ad copy |

### For Product Validation

| Subreddit | What to mine | Output format |
|---|---|---|
| r/Notion | "I wish Notion could..." comments | Feature ideas, new template concepts |
| r/Entrepreneur | "Is there a tool that..." questions | SaaS idea validation |
| r/SEO | "I can't figure out why..." technical Qs | Service offering (audit/consulting) |
| r/passive_income | "I've tried X and it didn't work" | Content angle (contrarian take) |

---

## Mining Workflow (Weekly)

**Step 1: Set up tracking (one-time, 30 min)**

Install Reddit Enhancement Suite. Create custom feeds for your target subreddits. Set filters to show posts with 100+ upvotes from the last 7 days.

**Step 2: Weekly scan (15 min)**

Every Monday morning:
- Filter each target sub by "Top / This Week"
- Open top 5 posts in each
- Read the post + top 10 comments
- Copy anything useful to a scratchpad file

**Step 3: Extract and tag (10 min)**

For each piece of useful content, tag it:
- `PAIN_POINT` — language to use in copy
- `FRAMEWORK` — method to repurpose as content
- `PROOF` — number or case study to reference
- `TRENDING` — topic to build content around
- `OBJECTION` — concern to pre-handle

**Step 4: Convert to content (varies)**

Weekly batch conversion:
- 3 PAIN_POINTs → 3 Twitter hooks
- 1 FRAMEWORK → 1 newsletter section
- 1 TRENDING topic → 1 YouTube video outline
- 2 OBJECTIONs → 2 FAQ entries for landing page

---

## Automated Mining Setup

**Using our existing reddit_deep_scraper.py:**

The scraper already hits all 41 target subreddits via JSON API. No browser required.

Command: `python3 AUTOMATIONS/reddit_deep_scraper.py --scrape`

Output: JSON files in `AUTOMATIONS/reddit_scraper_output/`

**What to extract from the JSON:**

```python
# Key fields to pull
{
    "title": post title (mining for pain points, trends),
    "selftext": full body text (mining for frameworks, proof),
    "score": upvote count (filter > 100 for quality),
    "num_comments": comment count,
    "comments": [
        {
            "body": comment text,
            "score": comment karma,
        }
    ]
}
```

**Filter criteria for high-value posts:**
- `score >= 100` (validated by community)
- `num_comments >= 10` (enough discussion for signal)
- `created_utc` within last 7 days (fresh)

**Bonus: Search for specific pain points**

Reddit JSON search: `https://www.reddit.com/search.json?q={KEYWORD}&sort=top&t=month&limit=25`

No auth required. Returns top posts from the past month matching your keyword.

---

## Content Repurposing Matrix

One Reddit thread → 7+ content pieces:

| Source | Output 1 | Output 2 | Output 3 |
|---|---|---|---|
| High-karma case study | YouTube script | Twitter thread (10 tweets) | Newsletter section |
| Pain point thread (50+ comments) | Landing page headline | Email subject line swipe | Twitter hook test |
| Framework post | Notion template concept | Gumroad guide outline | Blog post structure |
| Tool debate thread | Comparison blog post | YouTube comparison video | Twitter poll + thread |
| "I tried X" post | Testimonial angle | Product positioning | Cold email hook |

---

## High-Signal Subreddits to Scrape Monthly

Ranked by quality-to-noise ratio:

1. **r/Entrepreneur** — business models, revenue reports
2. **r/SideProject** — app launches, product feedback
3. **r/juststart** — affiliate marketing, niche sites
4. **r/sweatystartup** — local biz, service business numbers
5. **r/digitalmarketing** — platform changes, campaign data
6. **r/freelance** — rate discussions, client problems
7. **r/ChatGPT** — AI tool adoption patterns
8. **r/SEO** — algorithm changes, ranking case studies
9. **r/Notion** — power user workflows, feature requests
10. **r/passive_income** — what's actually working for people right now

---

## Ethics and Attribution

- Never copy a Reddit post verbatim and publish it elsewhere
- Synthesize: take the insight, add your own experience/data, write fresh
- If you use a specific quote or case study, don't identify the user
- General statistics ("multiple Reddit users reported X") are fine
- Platform rules don't prohibit learning from public posts — they prohibit scraping for spam

The line: extracting insight = fine. Copying content = not fine.
