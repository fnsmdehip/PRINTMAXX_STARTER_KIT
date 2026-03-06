# Discord Bot Concepts — 5 Ideas

Full feature specs, monetization models, and build complexity for each.

---

## Bot 1: StreakBot — Habit Tracking for Discord Servers

**Core concept:** Bring the habit streak mechanic directly into Discord communities. Members check in daily, build streaks, compete on leaderboards. Accountability without leaving Discord.

**Target servers:** Study groups, fitness communities, indie hacker servers, solopreneur communities, language learning groups

**Primary commands:**
```
/checkin [habit_name]          — Mark today's habit complete
/streak [@user]                — View your or another member's streaks
/habits add [name] [emoji]     — Create a new tracked habit
/habits list                   — See your active habits
/leaderboard [habit_name]      — Top 10 streaks for a specific habit
/leaderboard all               — Overall server leaderboard by total streaks
/stats [@user]                 — Full stats: current/best streak, completion rate, join date
/freeze                        — Use a streak freeze (1 per month)
/challenge @user [habit]       — Challenge another member to same habit
```

**Auto behaviors:**
- Daily reminder DM at user-configured time: "Don't forget to check in for [habit]!"
- Streak milestone announcements in #general or configured channel: "🔥 @username just hit 30 days on 'gym'!"
- Streak broken notification: "❌ @username's 47-day 'reading' streak ended. Start again today?"
- Weekly server summary posted every Sunday: top 5 streaks, new milestones, longest streak holder

**Roles integration:**
- Auto-assign roles at milestones: "7-Day Warrior", "30-Day Beast", "100-Day Legend"
- Custom roles configurable by server admins
- Role removal if streak is broken (optional setting)

**Monetization model:**
- Free for servers up to 50 members, 3 habits per member
- StreakBot Pro server unlock: $9.99/month (unlimited members, unlimited habits, custom roles, advanced analytics)
- Annual: $79.99/year ($6.67/month)
- Revenue target: 100 servers × $9.99 = $999/month, 500 servers = $4,995/month

**Tech stack:**
- discord.js v14 (Node.js)
- PostgreSQL for streak data (Supabase free tier to start)
- Hosted: Railway ($5/month) or Fly.io
- Bot hosting budget: $10-15/month total until 20+ paying servers

**Build time:** 3-5 days solo build
**Registration:** discord.com/developers → Applications → Bot

**Server growth angle:**
- List on top.gg and discordbotlist.com (free, drives organic server adds)
- Create a demo server for prospects to try before installing
- Content: "I built a habit tracking bot for Discord in 3 days. Here's how."

---

## Bot 2: AlphaBot — Daily Business/Market Signal Digest

**Core concept:** Automated intelligence feed for indie hackers and solopreneurs. Bot posts curated business signals, trending products, and opportunity alerts directly to Discord channels.

**Target servers:** Indie hacker communities, ecom groups, dropshipping servers, affiliate marketing communities, crypto/trading groups

**What it posts (automated daily):**
- **Morning Digest (8 AM server time):** Top 5 trending products from TikTok Shop + AliExpress + Amazon Movers & Shakers
- **Niche Signal (12 PM):** One promising niche pulled from Google Trends + Reddit momentum
- **Tool Alert (3 PM):** New SaaS product from Product Hunt that might be useful/opportunistic
- **Closing Bell (6 PM):** One high-signal Twitter/X thread from the day, summarized

**Member commands:**
```
/digest                        — Get today's digest on demand
/trending [category]           — Trending products in a specific category
/niche [topic]                 — AI analysis of a niche's opportunity score
/tool [tool_name]              — Quick info on any SaaS (pricing, features, affiliate program)
/signal history [days]         — Past N days of signals as digest
/alert add [keyword]           — Get DM when keyword appears in signals
```

**Monetization model:**
- Free: 1 signal category, 24-hour delay
- AlphaBot Pro server: $29/month (all signal categories, real-time, custom keywords, export to CSV)
- Individual Pro: $9/month per user (access Pro features in any server AlphaBot is in)
- Affiliate angle: include affiliate links in tool recommendations (disclosed in bio)

**Revenue math:**
- 50 paying servers × $29 = $1,450/month
- 200 individual Pro users × $9 = $1,800/month
- Affiliate commissions: estimated $500-1,000/month at scale
- Combined: $3,750-4,250/month at 250 paying customers

**Data sources (all APIs, no scraping required):**
- Google Trends API (unofficial, PyTrends)
- Product Hunt GraphQL API
- Reddit JSON API (no auth required for public data)
- AliExpress Dropship Center (scraping or unofficial API)
- Amazon Movers & Shakers (scraping allowed for personal use)

**Tech stack:**
- Python + discord.py
- PostgreSQL for user data and alert configs
- Celery for scheduled posts
- Redis for job queue
- Railway ($10/month)

**Build time:** 1 week for core, 2 weeks for Pro features

---

## Bot 3: ColdMailBot — Email Outreach Assistant Inside Discord

**Core concept:** Cold email tool integrated into Discord. Teams or solopreneurs manage their outreach pipeline inside Discord. Generate sequences, track replies, get suggestions — all via Discord commands.

**Target servers:** Agency servers, freelancer communities, sales teams, B2B SaaS communities

**Primary commands:**
```
/sequence generate [niche] [offer] [ICP]   — Generate 3-email cold sequence with Claude
/sequence save [name]                       — Save the last generated sequence
/sequence list                              — View all saved sequences
/email improve [paste email text]           — Rewrite email for higher reply rate
/subject generate [email body]             — Generate 5 subject line variations
/prospect add [name] [company] [email]     — Add prospect to pipeline
/prospect status [email]                   — Check status of a prospect
/pipeline view                             — See your pipeline (contacts by stage)
/pipeline move [email] [stage]             — Move prospect between stages
/stats                                     — Your send/open/reply rates this week
/followup needed                           — List prospects who need follow-up today
```

**Auto behaviors:**
- Daily morning post: "You have 12 follow-ups due today. Type /followup needed to see them."
- Reply rate notifications: "Your sequence 'SaaS Dev Agencies' hit a 12% reply rate. That's above average."
- Weekly performance summary per member with sequences in use

**Integrations:**
- Instantly.ai (export sequences directly)
- Apollo.io (import lead lists)
- Smartlead (webhook for reply tracking)

**Monetization:**
- Free: 1 saved sequence, 10 prospects tracked
- Pro individual: $19/month (unlimited sequences, 500 prospects, reply tracking)
- Agency server tier: $79/month (10 seats, shared sequences, team analytics)

**Revenue math:**
- 100 individual Pro × $19 = $1,900/month
- 20 agency servers × $79 = $1,580/month
- Total: $3,480/month at this scale

**Tech stack:**
- Node.js + discord.js
- Anthropic Claude API for sequence generation (Haiku model, ~$0.01 per sequence)
- PostgreSQL (Supabase)
- Railway

**Build time:** 5-7 days for core, 2 weeks for integrations

---

## Bot 4: StudyBot — Accountability and Focus for Study Servers

**Core concept:** Pomodoro timer, accountability check-ins, and study streaks built for Discord study communities. Popular with students, coding bootcamp learners, language learners.

**Target servers:** Study Together-type communities, CS student servers, language learning (Korean, Japanese, Spanish), exam prep communities (MCAT, CPA, bar exam)

**Primary commands:**
```
/pomo start [task_name]        — Start a 25-min focus session
/pomo stop                     — End session early
/pomo status                   — How many minutes left in your current session
/sessions today                — Your completed sessions today
/sessions week                 — Week summary with daily breakdown
/streak                        — Your study streak (days with 4+ sessions)
/room join [room_name]         — Join a virtual study room (see who else is studying)
/room create [name]            — Create a study room
/leaderboard                   — Top studiers this week by sessions
/goal set [sessions_per_day]   — Set your daily goal
/goal status                   — Progress toward daily goal
```

**Auto behaviors:**
- Session start announcement (optional): "@username started a focus session: 'MCAT bio review'"
- Session complete: "✅ @username completed a 25-min session on 'MCAT bio review'. That's 4/4 today!"
- Virtual study room voice channel creation (via bot permissions)
- Daily study room leaderboard posted at midnight
- Weekly streaks and awards posted Sunday

**Voice channel integration:**
- When you start a /pomo, bot moves you to a "Focus Room" voice channel
- Anyone in the room is in a focus session — social accountability
- Timer visible in channel name: "🍅 Focus Room [12min left]"

**Monetization:**
- Free servers: 1 study room, 10 users
- StudyBot Pro server: $14.99/month (unlimited rooms, unlimited users, custom roles/awards, server analytics)
- University/bootcamp tier: $49/month (white-labeled, priority support)

**Revenue math:**
- 100 servers × $14.99 = $1,499/month
- 10 institutional × $49 = $490/month
- Total: ~$2,000/month at 110 paying servers

**Growth channels:**
- Reddit: r/study, r/GetStudying, r/languagelearning, r/cscareerquestions
- Product Hunt launch
- Discord server partnerships (offer free Pro to study servers with 500+ members)
- "I built a study accountability bot" build-in-public thread

**Tech stack:**
- discord.js v14 (Node.js)
- PostgreSQL for session/streak data
- Redis for active session state
- Railway ($5-15/month)

**Build time:** 4-6 days

---

## Bot 5: ContentBot — Social Media Content Generator for Creator Communities

**Core concept:** On-demand content generation inside Discord. Members paste a topic, a URL, or a rough idea and get back platform-optimized social posts, threads, hooks, and captions. Powered by Claude API.

**Target servers:** Content creator communities, marketing agencies, solopreneur servers, brand strategy Discord groups

**Primary commands:**
```
/tweet [topic or idea]                     — Generate 3 tweet options
/thread [topic]                            — Generate a 7-tweet thread
/hook [topic] [platform]                  — Generate 5 hook variations
/caption [topic] [platform] [tone]        — Generate caption for IG/TikTok/LinkedIn
/repurpose [paste content]                — Repurpose a piece of content for 4 platforms
/headline [topic] [audience]             — 5 headline/title variations
/email_subject [email topic]             — 5 email subject line variations
/bio [name] [niche] [offer]              — Write platform bio
/cta [offer] [platform]                  — 5 CTA variations
/analyze [paste post]                     — Analyze a post for strengths/weaknesses
/save [alias]                             — Save last generated content with alias
/library                                  — View your saved content pieces
```

**Auto behaviors:**
- Daily content prompt posted to a #content-ideas channel (if configured)
- "Content of the day" — one high-performing post format from recent viral examples
- Weekly "what worked this week" summary based on formats members used most

**Content style control:**
- Each user sets their voice profile once: tone (professional/casual/aggressive), niche, platform focus
- All subsequent generations use their voice profile
- Override per request: /tweet [topic] --tone=casual --platform=twitter

**Quality gate:**
- Each output includes: the content + explanation of why this hook/angle was chosen
- Confidence score: "This hook has a 70% similarity to formats that drove 10K+ impressions"

**Monetization:**
- Free: 10 generations per month per user
- ContentBot Pro individual: $12/month (unlimited, voice profiles, library)
- Server Pro: $39/month (all members get Pro, server analytics, custom templates)

**Revenue math:**
- 500 individual Pro × $12 = $6,000/month
- 50 server Pro × $39 = $1,950/month
- Total: ~$8,000/month at this scale

**API cost at scale:**
- Claude Haiku: $0.0008/1K input tokens, $0.004/1K output tokens
- Average request: ~300 input tokens + ~200 output tokens = $0.0011 per request
- 1,000 daily requests = $1.10/day = $33/month in API costs
- At $8K/month revenue, COGS = 0.4%

**Tech stack:**
- Node.js + discord.js + Anthropic SDK
- PostgreSQL for user profiles and content library
- Railway ($15/month)

**Build time:** 3-4 days for core (Claude API does the heavy lifting)

**Distribution:**
- top.gg listing
- Discord Server Discovery
- ProductHunt launch
- Content: "How I built a content bot that generates 5 tweets in 2 seconds" thread

---

## Bot Development SOP

**General Discord bot setup:**

1. Go to discord.com/developers/applications
2. Create New Application, name it
3. Navigate to "Bot" tab, click "Add Bot"
4. Enable "Message Content Intent" and "Server Members Intent" (required for most bots)
5. Permissions needed: Send Messages, Use Slash Commands, Manage Roles (for StreakBot/StudyBot), Connect/Speak (for StudyBot voice)
6. Generate OAuth2 URL with bot + applications.commands scope
7. Add to test server

**Slash command registration:**
- Global commands: 1 hour to propagate
- Guild-specific commands: instant (use for testing)
- Register with Discord REST API using your bot token

**Hosting options:**
| Option | Cost | Best For |
|--------|------|----------|
| Railway | $5/month | All bots, simplest DX |
| Fly.io | Free tier available | Scale-aware pricing |
| DigitalOcean App Platform | $5/month | More control |
| Render | Free tier (spins down) | Development only |

**Monetization implementation:**
- Lemon Squeezy for payments ($0 monthly fee, 5% + $0.50 per transaction)
- Or Paddle (better for international)
- Bot checks paid status via database lookup on every premium command
- Stripe is overkill for Discord bots — Lemon Squeezy has better Discord community reputation

**Listing for discovery:**
- top.gg (largest bot directory, 4M+ monthly visitors)
- discordbotlist.com (secondary, still worth listing)
- discords.com/bots
- bots.ondiscord.xyz
- Posting in bot-showcase channels of large Discord communities
