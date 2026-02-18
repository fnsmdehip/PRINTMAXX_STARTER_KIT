# Reddit Marketing & Research Guide

**30 Target Subreddits Added to HIGH_SIGNAL_SOURCES.csv**

---

## Self-Promotion Allowed (9 Subreddits)

These allow product promotion if done correctly:

| Subreddit | Members | Best For |
|-----------|---------|----------|
| **r/SaaS** | 341K | SaaS launches, growth tactics |
| **r/SideProject** | 430K | Indie launches, feedback |
| **r/Entrepreneur** | 4.8M | Business stories, value-first promotion |
| **r/microsaas** | 155K | Micro SaaS launches |
| **r/indiehackers** | 91K | Indie builds, revenue numbers |
| **r/smallbusiness** | 2.2M | SMB tools, services |
| **r/thesidehustle** | 184K | Side income methods |
| **r/InternetIsBeautiful** | 17M | Cool tools, innovative apps |
| **r/EntrepreneurRideAlong** | 593K | Build journeys, case studies |

---

## Self-Promotion Rules (CRITICAL)

### DON'T:
- ❌ AI-generate generic posts
- ❌ Drop links in title/post
- ❌ "Check out my product" spam
- ❌ Multiple subs same day
- ❌ Copy-paste same post

### DO:
- ✅ Provide value/experience first
- ✅ Share real journey/numbers
- ✅ Answer questions genuinely
- ✅ Let people ask for product
- ✅ Wait for "link?" before sharing

---

## Posting Formula (Value-First)

**Example structure:**

```
Title: "I built [X] to solve [Y problem]. Here's what I learned."

Post:
- Context (what problem frustrated you)
- Journey (how you built it, timeframe, tech stack)
- Numbers (users, revenue, conversion rate - be honest)
- Insights (what worked, what didn't)
- Lessons (actionable takeaways for others)

[Let people ask for link in comments]
```

---

## Research Subreddits (Pain Point Mining)

Use for idea validation, not promotion:

| Subreddit | Best For |
|-----------|----------|
| **r/productivity** | App pain points |
| **r/Business_Ideas** | Validation |
| **r/Startup_Ideas** | Market gaps |
| **r/AppIdeas** | Feature requests |
| **r/GrowthHacking** | Distribution tactics |

---

## Reddit JSON Hack (Pain Point Mining)

**Script:** `AUTOMATIONS/reddit_json_miner.py`

**How it works:**
1. Add `/.json` to any Reddit URL
2. Get structured data (no API key needed)
3. Extract pain points automatically
4. Find recurring complaints (10+ times = validated idea)

**Usage:**
```bash
# Mine single subreddit
python3 AUTOMATIONS/reddit_json_miner.py --subreddit SaaS --limit 50

# Mine all 30 target subreddits
python3 AUTOMATIONS/reddit_json_miner.py --batch

# Analyze specific post
python3 AUTOMATIONS/reddit_json_miner.py --url "https://reddit.com/r/SaaS/comments/xyz"
```

**Look for:**
- "I wish someone would build..."
- "I'd pay for..."
- "Why doesn't X exist?"
- "Frustrated with..."
- Same complaint 10+ times = validated idea

---

## Content Strategy Per Subreddit Type

### For Launches (r/SideProject, r/SaaS):
- Lead with problem
- Share journey authentically
- Include real numbers (users, revenue)
- Technical stack details
- Lessons learned
- Link only when asked

### For Growth (r/Entrepreneur, r/EntrepreneurRideAlong):
- Case study format
- Month-over-month numbers
- What worked vs what didn't
- Tactical insights
- Avoid guru energy

### For Validation (r/Business_Ideas, r/AppIdeas):
- Ask specific questions
- Share mockups/wireframes
- "Would you use this?"
- Price point validation
- Don't pitch, ask for feedback

---

## Posting Frequency Limits

**Per subreddit:**
- Max 1 post per 7 days
- Max 1 comment thread per day
- Never cross-post same content

**Account age:**
- Wait 30+ days before first promotion
- Build comment karma first (100+)
- Engage genuinely before promoting

---

## Engagement Strategy

**When someone comments:**
1. Reply within 1 hour (shows you're active)
2. Answer questions thoroughly
3. Provide additional value
4. Thank critics, learn from feedback
5. Only share link when explicitly asked

**Building trust:**
- Comment on others' posts genuinely
- Share insights without promoting
- Be helpful, not salesy
- Admit failures and learnings

---

## What to Track

For each post:
- Upvotes / downvotes
- Comment count
- "Link?" requests
- Click-throughs (if link shared)
- Signups from Reddit (track with UTM)

**Save to:** `LEDGER/REDDIT_POST_PERFORMANCE.csv`

Columns:
- date, subreddit, post_title, upvotes, comments, link_requests, clicks, signups

---

## Best Times to Post

**Weekdays (EST):**
- 6-8am (early commute)
- 12-2pm (lunch break)
- 5-7pm (after work)

**Avoid:**
- Late Friday (weekend drop-off)
- Sunday evening
- Holidays

---

## Automation Scripts

**Reddit JSON Miner:**
- `reddit_json_miner.py` - Extract pain points automatically
- Batch mode: mines all 30 subreddits
- Outputs CSV ready for Claude analysis

**Content Poster:**
- *(To be built)* Schedule Reddit posts
- Enforce frequency limits
- Track performance

---

## Example Successful Posts

### r/SideProject (High engagement):
```
"Built a prayer reminder app. 1K users in 30 days."

I got frustrated managing prayer times, built PrayerLock in React Native.

Tech: Expo, RevenueCat, push notifications
Time: 3 weeks nights/weekends
Users: 1,043 in first month
Revenue: $127 MRR (hard paywall, $2.99/mo)

What worked:
- Muslim community subreddits for beta
- Hard paywall from day 1 (8x vs freemium)
- Prayer time API integration

What didn't:
- Instagram ads (terrible ROAS)
- Feature bloat (stripped back to core)

Happy to answer questions.
```

*[Wait for "link?" requests in comments]*

---

## Common Mistakes to Avoid

1. **Premature promotion:** Posting before 30 days of activity
2. **Generic posts:** "Check out my app" with no context
3. **Link dumping:** URL in title or body
4. **Cross-posting:** Same post to 5 subs in 1 day
5. **Ignoring feedback:** Not replying to comments
6. **Guru energy:** "I made $10K my first month" flex
7. **No numbers:** Vague claims without specifics

---

## Pain Point Mining Workflow

1. **Daily scan** (15 min):
   - Check r/productivity, r/Business_Ideas for pain points
   - Note recurring complaints
   - Tag with potential method (APP_FACTORY, SaaS, etc)

2. **Weekly deep dive** (1 hour):
   - Run reddit_json_miner.py on top 3 subreddits
   - Analyze extracted pain points
   - Find patterns (10+ mentions = validated)

3. **Monthly validation**:
   - Post validation threads in r/AppIdeas
   - Test pricing in r/SaaS feedback threads
   - Gauge interest before building

---

## Integration with PRINTMAXX Infrastructure

**HIGH_SIGNAL_SOURCES.csv:**
- All 30 subreddits added (SRC146-SRC175)
- 9 marked auto_monitor=TRUE (self-promotion allowed)
- Signal quality rated (HIGHEST, HIGH, MEDIUM)

**Ralph Loop Integration:**
- Mega loop DAILY_RESEARCH scans Reddit sources
- Uses reddit_json_miner.py for deep threads
- Outputs to ALPHA_STAGING.csv

**Content Calendar:**
- Reddit posts scheduled in content calendar
- Frequency limits enforced
- Performance tracked

---

## The Reddit Advantage

**Why Reddit > Other Platforms:**
1. People explicitly state pain points
2. Threaded discussions = deep context
3. 10+ mentions = validated demand
4. Niche communities = targeted audience
5. Self-promotion allowed (if value-first)
6. No algorithm games, pure relevance

**The internet is telling you what to build. You just have to listen.**

---

**Next Actions:**
1. Run `python3 AUTOMATIONS/reddit_json_miner.py --batch`
2. Analyze pain points extracted
3. Identify 3 validated opportunities
4. Build MVP for highest-signal idea
5. Launch in r/SideProject with value-first post
