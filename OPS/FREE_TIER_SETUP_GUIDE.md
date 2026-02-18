# Free Tier Tool Setup Guide

**Created:** 2026-02-12
**Purpose:** sign up for every free-tier tool that powers PRINTMAXX ops. zero cost. maximum output.
**Time to complete all 14:** 3-4 hours total
**Monthly cost:** $0

---

## the math

these 14 tools replace $2,000+/mo in paid software. combined free tiers give you:
- 100 AI phone calls per day (Bland AI)
- unlimited workflow automation (n8n self-hosted)
- 3 social channels scheduled (Buffer)
- 50 lead database credits per month (Apollo)
- unlimited scheduling links (Cal.com)
- 150 AI image tokens per day (Leonardo)
- 66 AI video credits per day (Kling)
- 10 AI songs per day (Suno)
- 60 AI video coins per day (PixVerse)
- 3 anti-detect browser profiles (GoLogin)
- unlimited bandwidth static hosting (Cloudflare Pages)
- full backend with auth + database + storage (Supabase)
- AI app builder with 200 GPT-4 credits (Dify)
- 2 VMs running 24/7 forever (Oracle Cloud)

that's a full-stack solopreneur operation for $0/mo. sign up in order below.

---

## 1. Bland AI

**what it is:** AI phone calling API. your AI agent calls real phone numbers, follows a script, handles objections, books appointments.

**signup URL:** https://app.bland.ai/signup
**free tier:** 100 calls per day. no credit card required to start. pay-per-use after free tier ($0.09/min connected).
**setup time:** 15 minutes

### step by step

1. go to https://app.bland.ai/signup
2. create account with email
3. verify email
4. grab your API key from the dashboard (Settings > API Keys)
5. test with a single call to your own phone number:

```bash
curl -X POST https://api.bland.ai/v1/calls \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "phone_number": "+1YOURPHONE",
    "task": "You are calling from a web design agency. Ask if they are happy with their current website and if they would be interested in a free website audit.",
    "voice": "maya",
    "max_duration": 2
  }'
```

6. check call recording in dashboard

### which ops it powers

| Op | How Bland Connects |
|----|--------------------|
| Local Biz Lead Gen (OP-LOCAL) | cold call scored leads from `AUTOMATIONS/savvy_lead_scraper.py` |
| Cold Outbound (OP-COLD) | follow-up calls after cold email opens |
| Appointment Setting | book discovery calls for service packages |
| Lead Qualification | AI pre-screens inbound leads before human call |

**integration path:** `AUTOMATIONS/local_biz_pipeline.py` scrapes leads -> scores them 0-100 -> feeds high-scorers to Bland API -> Bland calls them -> transfers warm leads to your phone or books on Cal.com.

**full setup guide:** `MONEY_METHODS/LOCAL_BIZ/AI_CALL_OUTREACH.md` (374 lines, 3 call scripts, TCPA compliance)

### gotchas

- TCPA compliance is real. never call numbers on the Do Not Call list. Bland handles some compliance but you're responsible for your call lists.
- free tier resets daily. 100 calls/day is plenty for starting. at 2-minute average call, that's 3+ hours of AI phone time per day.
- voice quality is good but not perfect. best for initial outreach and qualification, not closing.
- record all calls (Bland does this automatically). review first 10 calls to refine your script.

---

## 2. n8n (Self-Hosted)

**what it is:** open-source workflow automation. like Zapier but free, self-hosted, and way more powerful. connects 400+ apps with visual drag-and-drop workflows.

**signup URL:** https://n8n.io (for cloud trial) OR self-host for free forever
**free tier:** self-hosted = unlimited workflows, unlimited executions, forever. cloud = 14-day trial.
**setup time:** 30-45 minutes (Docker install)

### step by step (self-hosted on your Mac)

1. install Docker Desktop if you don't have it:
```bash
brew install --cask docker
# open Docker Desktop from Applications, let it start
```

2. run n8n:
```bash
docker run -it --rm \
  --name n8n \
  -p 5678:5678 \
  -v ~/.n8n:/home/node/.n8n \
  n8nio/n8n
```

3. open http://localhost:5678 in browser
4. create admin account (email + password)
5. you're in. start building workflows.

**for always-on:** run on Oracle Cloud free VM (tool #14) instead of your Mac:
```bash
# on Oracle VM:
docker run -d \
  --name n8n \
  --restart unless-stopped \
  -p 5678:5678 \
  -v ~/.n8n:/home/node/.n8n \
  n8nio/n8n
```

### which ops it powers

| Op | Workflow |
|----|----------|
| Content Distribution | new blog post -> tweet + LinkedIn + Medium + Substack + Buffer |
| Lead Enrichment | new lead in CSV -> Apollo enrichment -> score -> route to outreach |
| Revenue Tracking | Gumroad webhook -> log to REVENUE_TRACKER.csv -> Slack notification |
| Alpha Screening | new alpha entry -> auto-score -> route to PENDING_REVIEW |
| Email Sequences | trigger-based email flows without paid ESP |
| Social Monitoring | RSS/webhook triggers when competitor posts |

**6 workflows already specced:** `AUTOMATIONS/N8N_SETUP_AND_WORKFLOWS.md`

### gotchas

- self-hosted means YOU maintain it. Docker makes this easy but it's still your responsibility.
- runs on your Mac only when Docker Desktop is running. for 24/7, deploy to Oracle Cloud free VM.
- Sustainable Use License: you can use n8n for anything EXCEPT reselling it as a competing automation platform. all PRINTMAXX use cases are fine.
- memory usage: ~200-400MB RAM. fine for a Mac. on Oracle free VM (1GB RAM), limit concurrent workflow executions to 3-5.

---

## 3. Buffer

**what it is:** social media scheduling. queue posts, set publishing times, basic analytics.

**signup URL:** https://buffer.com
**free tier:** 3 social channels, 10 scheduled posts per channel. no credit card required.
**setup time:** 10 minutes

### step by step

1. go to https://buffer.com
2. click "Get started now"
3. create account with email or Google login
4. connect 3 social accounts (pick your top 3 -- recommendation: Twitter/X + LinkedIn + Instagram)
5. go to Publishing > Queue > Settings to set posting times per channel
6. upload content from Buffer CSVs:

```
source file: AUTOMATIONS/content_posting/
available CSVs: faith_tweets, fitness_tweets, tech_tweets, meme_tweets, sleep_tweets, findom_tweets, ecom_arb_content, ramadan_tweets
```

7. Buffer accepts CSV upload: go to Publishing > click "..." menu > Import from CSV

### which ops it powers

| Op | How Buffer Connects |
|----|---------------------|
| Content Farm (CF001-CF013) | schedule posts across 3 niche accounts |
| PRINTMAXXER brand | building-in-public tweets on schedule |
| Launch campaigns | schedule product launch tweet series |
| Consistency | never miss a posting day |

**1,278+ posts ready to upload:** `LEDGER/CONTENT_CALENDAR_30DAY.csv`
**posting guide:** `OPS/CONTENT_POSTING_GUIDE.md`
**Buffer CSV format guide:** `OPS/BUFFER_CSV_UPLOAD_INSTRUCTIONS.md`

### gotchas

- 3 channels is the limit on free. choose wisely. Twitter + LinkedIn + one more.
- 10 posts per queue means you need to refill every 2-3 days (at 3-5 posts/day).
- no bulk scheduling on free tier -- you manually add or CSV import.
- analytics are basic. use platform-native analytics for real data.
- alternative: Publer ($12/mo) unlocks more channels if you outgrow Buffer free.

---

## 4. Apollo.io

**what it is:** B2B lead database with email finder, company data, and outreach tools. 275M+ contacts.

**signup URL:** https://app.apollo.io/#/sign-up
**free tier:** 50 email credits per month. 5 phone number credits per month. unlimited search. basic email sequences.
**setup time:** 10 minutes

### step by step

1. go to https://app.apollo.io/#/sign-up
2. create account with work email (Gmail works)
3. verify email
4. install Chrome extension for LinkedIn enrichment (optional but useful)
5. search for leads:
   - People search: filter by title, company size, industry, location
   - Company search: filter by industry, employee count, revenue, tech stack
6. export leads with email addresses (50/mo on free tier)

### which ops it powers

| Op | How Apollo Connects |
|----|---------------------|
| Cold Email (OP-COLD) | find prospect email addresses |
| Local Biz Lead Gen | enrich leads from `savvy_lead_scraper.py` with verified emails |
| Service Sales | find decision-makers at target companies |
| Freelance Outreach | find hiring managers for Upwork/Fiverr upsells |

**integration path:** scrape leads with `nationwide_scraper.py` -> enrich in Apollo (get verified emails) -> feed to cold email sequences from `MONEY_METHODS/COLD_OUTBOUND/`

### gotchas

- 50 credits/mo is tight. use credits only for highest-scored leads (score 70+ from savvy_lead_scraper.py).
- Apollo email verification is good but not perfect. expect 5-10% bounce rate.
- free tier limits email sending to 100/day. for volume, use separate cold email infrastructure (DeliverOn/Instantly).
- don't use your primary email domain. buy cold email domains ($12 each on Porkbun).
- Apollo tracks opens/clicks. useful for knowing which leads to follow up on.

---

## 5. Cal.com

**what it is:** open-source scheduling tool. like Calendly but free and self-hostable. booking pages, calendar sync, team scheduling.

**signup URL:** https://cal.com/signup
**free tier:** unlimited booking pages, unlimited bookings, Google/Outlook calendar sync. no credit card required.
**setup time:** 10 minutes

### step by step

1. go to https://cal.com/signup
2. create account
3. connect your Google Calendar (Settings > Calendars > Connect)
4. create event types:
   - "15-min Discovery Call" (for cold outreach leads)
   - "30-min Strategy Session" (for warm leads)
   - "60-min Implementation Call" (for high-ticket clients)
5. set availability (your real hours, not 24/7)
6. grab your booking URL: cal.com/yourusername/15min
7. add booking link to:
   - cold email signatures
   - Bland AI call scripts (transfer-to-booking)
   - Gumroad product upsell pages
   - social media bios

### which ops it powers

| Op | How Cal.com Connects |
|----|----------------------|
| Cold Outbound | CTA in cold emails: "book a call" |
| Bland AI Calls | AI transfers warm leads to your booking page |
| Service Sales | prospects self-schedule discovery calls |
| High-Ticket Products | application form -> qualified leads book calls |
| Client Onboarding | new clients book kickoff call |

**integration:** Cal.com webhooks -> n8n -> log to Notion CRM or CSV. every booked call tracked automatically.

### gotchas

- free tier is genuinely unlimited. Cal.com monetizes through team/enterprise features.
- calendar sync works with Google and Outlook. Apple Calendar requires iCloud setup.
- booking pages are simple but clean. no customization on free tier (logo, colors).
- Cal.com hosted = they handle uptime. self-hosted = more control but you maintain it.

---

## 6. Leonardo.ai

**what it is:** AI image generation. high-quality images from text prompts. models trained on different styles (photorealistic, anime, illustration).

**signup URL:** https://leonardo.ai
**free tier:** 150 tokens per day (resets daily). each image costs 1-8 tokens depending on model and size. roughly 20-75 images per day.
**setup time:** 5 minutes

### step by step

1. go to https://leonardo.ai
2. sign up with Google or email
3. verify email
4. you start with 150 daily tokens
5. go to "AI Image Generation"
6. select model:
   - "Leonardo Phoenix" = best all-around (photorealistic)
   - "Leonardo Anime XL" = anime/illustration style
   - "Leonardo Lightning" = fastest, lowest token cost (1 token per image)
7. type prompt, generate, download

### which ops it powers

| Op | How Leonardo Connects |
|----|----------------------|
| AI Influencer (AI001-AI008) | generate persona images, profile photos, content visuals |
| Content Farm | social post graphics, thumbnails |
| App Factory | app store screenshots, marketing visuals |
| POD (Print on Demand) | t-shirt designs, mug designs, poster art |
| Gumroad Products | cover images for digital products |
| Local Biz | demo website hero images for client pitches |

**asset generation prompts:** `MONEY_METHODS/APP_FACTORY/APP_ASSET_GENERATION_PROMPTS.md` (41KB, ready-to-use Leonardo/ImageFX prompts)

### gotchas

- 150 tokens/day = roughly 20-75 images depending on model. use Lightning model (1 token) for drafts, Phoenix (4-8 tokens) for finals.
- tokens reset at midnight UTC, not your local time.
- generated images are yours to use commercially. no attribution required.
- quality is competitive with Midjourney. not quite Midjourney V6 level but close and free.
- for bulk generation (100+ images), batch on Lightning model then re-generate best ones on Phoenix.

---

## 7. Kling AI

**what it is:** AI video generation. text-to-video or image-to-video. generates 5-10 second clips from prompts.

**signup URL:** https://klingai.com
**free tier:** 66 credits per day. standard quality video costs ~10 credits. roughly 6 videos per day.
**setup time:** 5 minutes

### step by step

1. go to https://klingai.com
2. create account (email signup)
3. verify email
4. go to "Video Generation"
5. choose mode:
   - Text to Video: describe what you want
   - Image to Video: upload a still image, Kling animates it
6. set duration (5s standard, 10s costs more credits)
7. generate, wait 2-5 minutes, download

### which ops it powers

| Op | How Kling Connects |
|----|-------------------|
| AI Influencer | animate persona still images into video content |
| Content Farm | short-form video for TikTok/Reels/Shorts |
| UGC Factory | AI-generated product demo videos |
| App Marketing | app promo videos from screenshots |
| POD | animated product mockups |

**combination play:** Leonardo generates still image -> Kling animates it into video -> add voiceover with ElevenLabs -> post to TikTok/YouTube Shorts. full video pipeline, $0 cost.

### gotchas

- 66 credits/day = roughly 6 standard videos. enough for daily content, not bulk production.
- generation takes 2-5 minutes per video. plan batch generation sessions.
- 5-second clips are the sweet spot on free tier. 10-second clips cost double.
- quality has improved dramatically. motion artifacts still happen but getting rarer.
- image-to-video mode produces more consistent results than text-to-video.
- credits reset daily. use them or lose them.

---

## 8. Suno

**what it is:** AI music generator. describe a song style and topic, Suno creates a full track with vocals, instruments, mixing.

**signup URL:** https://suno.com
**free tier:** 10 songs per day (50 credits, each song costs 5). non-commercial use on free tier. commercial use requires Pro ($10/mo).
**setup time:** 5 minutes

### step by step

1. go to https://suno.com
2. sign up with Google, Discord, or email
3. click "Create"
4. choose mode:
   - "Simple" = describe the vibe in a sentence
   - "Custom" = write lyrics, choose genre, set BPM
5. generate, listen, download

### which ops it powers

| Op | How Suno Connects |
|----|-------------------|
| AI Music Streaming (MM-MUSIC) | generate tracks -> distribute via DistroKid to Spotify/Apple Music |
| Content Farm | background music for video content (TikTok/YouTube) |
| App Factory | in-app audio (meditation sounds, workout beats) |
| Podcast/YouTube | intro/outro music, background tracks |

**important:** free tier songs are for personal/non-commercial use only. for monetization (Spotify, YouTube, selling), you need Pro ($10/mo). test on free tier, upgrade when ready to distribute.

### gotchas

- non-commercial restriction on free tier. do NOT upload free-tier songs to Spotify/streaming. test and experiment only.
- 10 songs/day is generous for testing. find your style, then upgrade to Pro for commercial.
- vocal quality varies. instrumental tracks are more consistently good.
- songs are 2-4 minutes. some need multiple generations to get right.
- Suno owns a non-exclusive license to free-tier generations. Pro tier = you own full commercial rights.

---

## 9. PixVerse

**what it is:** AI video generation (alternative to Kling). text-to-video and image-to-video. known for consistent character generation.

**signup URL:** https://pixverse.ai
**free tier:** 60 daily coins. standard video costs ~10 coins. roughly 6 videos per day.
**setup time:** 5 minutes

### step by step

1. go to https://pixverse.ai
2. sign up with Google or email
3. verify account
4. go to Create > Video
5. choose input mode:
   - Text to Video
   - Image to Video
   - Character to Video (consistent character across multiple videos)
6. set resolution and duration
7. generate, download

### which ops it powers

| Op | How PixVerse Connects |
|----|----------------------|
| AI Influencer | consistent character videos (same AI persona across content) |
| UGC Factory | product review style videos |
| Content Farm | B-roll and visual content for posts |
| Ads | AI-generated ad creative for Meta/TikTok |

**why both Kling AND PixVerse:** they have different strengths. Kling = better motion quality. PixVerse = better character consistency. use both. 6 videos/day from each = 12 free AI videos per day.

### gotchas

- character consistency is PixVerse's killer feature. same AI character across multiple scenes.
- 60 coins resets daily. similar volume to Kling.
- quality is slightly below Kling for general video but better for character work.
- watermark on free tier. small, in corner, can be cropped for some aspect ratios.
- commercial use allowed on free tier (check latest TOS, this has changed before).

---

## 10. GoLogin

**what it is:** anti-detect browser. run multiple browser profiles, each with a unique fingerprint. platforms can't tell they're the same person.

**signup URL:** https://gologin.com
**free tier:** 3 browser profiles. forever. no credit card required.
**setup time:** 15 minutes

### step by step

1. go to https://gologin.com
2. download the app (Mac, Windows, Linux)
3. create account with email
4. verify email
5. open GoLogin app
6. click "Create Profile"
7. configure:
   - name it (e.g., "TikTok-Fitness-Account")
   - OS fingerprint: match your actual OS
   - proxy: add SOAX proxy if you have one, or leave blank for now
   - timezone: match the account's target region
8. click "Run" to open the browser profile
9. sign into your social accounts inside this isolated browser

### which ops it powers

| Op | How GoLogin Connects |
|----|----------------------|
| Content Farm (multi-account) | separate browser profile per social account |
| AI Influencer | isolate persona accounts from each other |
| Cold Email | separate browser per email sending domain |
| Ecom Arbitrage | manage multiple marketplace seller accounts |

**why it matters:** platforms flag accounts that share browser fingerprints. if you run 5 Twitter accounts from Chrome, they link them. GoLogin gives each account its own fingerprint, cookies, and optionally IP address.

### gotchas

- 3 profiles is tight. prioritize your 3 most important accounts (highest-revenue or highest-risk).
- free tier works fine but has no proxy management. pair with SOAX ($50/mo) when you can.
- each profile stores its own cookies. closing GoLogin doesn't log you out.
- upgrade to Pro ($49/mo) for 10 profiles when content farm scales past 3 accounts.
- don't mix personal and PRINTMAXX accounts in the same GoLogin install. keep it clean.

---

## 11. Cloudflare Pages

**what it is:** static site hosting with unlimited bandwidth. deploy HTML/CSS/JS, Next.js, React, or any static site.

**signup URL:** https://dash.cloudflare.com/sign-up
**free tier:** unlimited bandwidth, unlimited requests, 500 builds per month, 1 build at a time, 100 custom domains.
**setup time:** 20 minutes

### step by step

1. go to https://dash.cloudflare.com/sign-up
2. create account with email
3. verify email
4. go to "Workers & Pages" in left sidebar
5. click "Create" > "Pages"
6. connect to Git:
   - link GitHub account
   - select repository
   - Cloudflare auto-builds and deploys on every push
7. OR direct upload:
   - drag and drop your build folder
   - instant deployment
8. custom domain (optional):
   - Pages > your project > Custom Domains > Add
   - point your domain's DNS to Cloudflare

### which ops it powers

| Op | How Cloudflare Pages Connects |
|----|-------------------------------|
| Programmatic SEO | host 600 "[service] in [city]" pages (`builds/programmatic_seo/`) |
| Landing Pages | host product and service landing pages |
| App Factory (PWA) | PWA deployment (instant, worldwide CDN) |
| Local Biz Demo Sites | host template sites for client pitches |
| Agency Website | host your own agency credibility site |

**immediate deploy:** `builds/programmatic_seo/` has 600 pages + sitemap ready. drag and drop to Cloudflare Pages. live in 60 seconds.

### gotchas

- "unlimited bandwidth" is real. Cloudflare uses this to get you on their platform. there's no catch.
- 500 builds/month on free tier. plenty for any solopreneur. each git push = 1 build.
- no server-side rendering on free tier. static sites and client-side JS only. for SSR, use Vercel.
- build time limit: 20 minutes. fine for most sites. large Next.js builds may need optimization.
- Cloudflare Pages + Cloudflare Workers (also free tier) = full serverless stack for $0.

---

## 12. Supabase

**what it is:** open-source Firebase alternative. PostgreSQL database, authentication, file storage, real-time subscriptions, edge functions.

**signup URL:** https://supabase.com/dashboard/sign-up
**free tier:** 2 free projects, 500MB database, 1GB file storage, 50K monthly active users (auth), 500K edge function invocations.
**setup time:** 15 minutes

### step by step

1. go to https://supabase.com/dashboard/sign-up
2. sign up with GitHub (recommended) or email
3. create new project
4. choose region closest to your users
5. set database password (save this)
6. wait 2-3 minutes for project to provision
7. grab credentials:
   - Project URL: `https://xxxx.supabase.co`
   - Anon Key: (public, safe for client-side)
   - Service Role Key: (secret, server-side only)
8. start building:
   - SQL Editor: create tables directly
   - Table Editor: visual interface (like a spreadsheet)
   - Auth: set up email/password or OAuth login

### which ops it powers

| Op | How Supabase Connects |
|----|----------------------|
| App Factory | backend for PWA apps (user auth, data storage) |
| Lead Tracking | store leads in a real database instead of CSVs |
| CRM | build a simple CRM for client management |
| Analytics | store event data from apps and sites |
| User Accounts | auth for premium content / gated products |
| File Storage | store uploaded files, generated assets |

**example:** PrayerLock PWA -> Supabase Auth for user accounts -> Supabase Database for prayer logs -> Supabase Storage for user profile images. full backend. $0.

### gotchas

- 2 free projects. plan which apps get their own project vs sharing a database.
- 500MB database is plenty for starting. typical text-only app uses 1-5MB for first 1000 users.
- 1GB file storage fills fast if you store images. compress before uploading.
- free tier pauses inactive projects after 1 week of no API calls. just ping it periodically.
- row-level security (RLS) is on by default. learn it. it prevents users from accessing each other's data.
- Supabase client libraries exist for JavaScript, Python, Flutter, Kotlin. drop-in integration.

---

## 13. Dify.ai

**what it is:** open-source AI app builder. create chatbots, AI agents, RAG applications, and workflow automations with a visual interface. no code required.

**signup URL:** https://cloud.dify.ai/signin
**free tier:** 200 GPT-4/Claude message credits (sandbox). unlimited custom model API calls if you bring your own key. 5 team members.
**setup time:** 15 minutes

### step by step

1. go to https://cloud.dify.ai/signin
2. sign up with email or GitHub
3. verify account
4. explore the Studio:
   - "Chat App" = build a chatbot
   - "Text Generator" = build a content generator
   - "Agent" = build an AI agent with tools
   - "Workflow" = visual multi-step AI pipeline
5. create first app:
   - click "Create Blank App" or use a template
   - define system prompt
   - add knowledge base (upload documents for RAG)
   - configure model (GPT-4, Claude, or your own API key)
   - test in preview
   - publish with shareable URL

### which ops it powers

| Op | How Dify Connects |
|----|-------------------|
| AI Chatbots for Clients | build custom chatbots for local businesses ($500-2K per build) |
| Internal Tools | AI-powered lead scorer, content reviewer, alpha screener |
| Productized AI | sell AI tools as standalone products (embed on sites) |
| Customer Support | AI support bot for your products and services |
| Content Generation | multi-step AI content pipelines (research -> outline -> write -> edit) |

**service play:** build custom Dify chatbots for local businesses. "AI receptionist that answers questions, books appointments, and never takes a day off." charge $500-2,000 per build + $200-500/mo maintenance.

### gotchas

- 200 sandbox credits run out fast if you use GPT-4/Claude. bring your own API key for unlimited usage (pay per token to OpenAI/Anthropic directly, much cheaper than platform credits).
- cloud version has usage limits. self-host on Oracle Cloud free VM for unlimited everything.
- knowledge base supports PDF, TXT, Markdown. upload your product docs and it becomes an AI sales assistant.
- apps get a shareable URL. embed on your site or share directly with clients.
- API available for programmatic access. connect to n8n for automated AI workflows.

---

## 14. Oracle Cloud

**what it is:** full cloud infrastructure. compute, storage, networking. the free tier is genuinely forever -- not a trial.

**signup URL:** https://cloud.oracle.com/sign-up
**free tier:** 2 AMD VMs (1 CPU, 1GB RAM each) OR 4 ARM VMs (shared 24GB RAM total). 200GB block storage. 10TB/mo outbound data. forever.
**setup time:** 30-45 minutes

### step by step

1. go to https://cloud.oracle.com/sign-up
2. create account (requires credit card for verification, will NOT charge you)
3. choose home region (closest to you)
4. verify email and phone
5. wait for account provisioning (can take up to 24 hours)
6. once active, create a VM:
   - go to Compute > Instances > Create Instance
   - shape: "VM.Standard.E2.1.Micro" (AMD, 1 CPU, 1GB RAM) -- this is the Always Free shape
   - image: Ubuntu 22.04
   - add your SSH public key
   - create
7. SSH in:
```bash
ssh -i ~/.ssh/your_key ubuntu@<public_ip>
```
8. install Docker:
```bash
sudo apt update && sudo apt install -y docker.io docker-compose
sudo usermod -aG docker $USER
# log out and back in
```
9. deploy n8n, Supabase, Dify, or any self-hosted tool on this VM

### which ops it powers

| Op | What Runs on Oracle VM |
|----|------------------------|
| n8n (always-on) | workflow automation running 24/7 |
| Dify (self-hosted) | AI app builder with no usage limits |
| Cron Jobs | overnight scripts that run without your Mac being on |
| Uptime Monitoring | health checks for all deployed apps |
| VPN/Proxy | personal proxy for geo-specific tasks |

**the play:** Oracle free tier + Docker = run your entire automation stack for $0. n8n, Dify, monitoring, cron jobs -- all on a VM that costs nothing and runs forever.

### gotchas

- account provisioning can take 1-24 hours. sign up today, use tomorrow.
- credit card required for verification. they charge $0.00 (or $1 temporary hold). always-free resources genuinely cost nothing.
- 1GB RAM per AMD VM is tight. run one major application per VM. n8n on VM1, Dify on VM2.
- ARM VMs share 24GB RAM pool (4 Ampere VMs). more RAM but ARM architecture means some Docker images need ARM builds.
- Oracle occasionally reclaims "idle" instances (rare, but documented). keep a small cron job running to show activity.
- free tier is specific shapes only. don't accidentally select a paid shape.
- outbound data: 10TB/mo is absurdly generous. you'll never hit this.

---

## Signup Order (Do This in One Sitting)

the order matters. later tools depend on earlier ones.

| Order | Tool | Time | Why This Order |
|-------|------|------|----------------|
| 1 | Oracle Cloud | 10 min signup (24hr provision) | start first because provisioning takes longest |
| 2 | Cloudflare Pages | 5 min | need hosting before deploying anything |
| 3 | Supabase | 5 min | need backend before building apps |
| 4 | Cal.com | 5 min | need scheduling before outreach |
| 5 | Buffer | 5 min | need scheduling before content |
| 6 | Apollo.io | 5 min | need leads before outreach |
| 7 | GoLogin | 10 min (download + install) | need before creating multi-accounts |
| 8 | Bland AI | 10 min | need API key for outreach pipeline |
| 9 | Leonardo.ai | 3 min | need images for content + products |
| 10 | Kling AI | 3 min | need video for content pipeline |
| 11 | PixVerse | 3 min | need second video source |
| 12 | Suno | 3 min | need music for video content |
| 13 | n8n | 30 min (Docker install) | needs Docker, ideally on Oracle VM |
| 14 | Dify.ai | 10 min | can self-host on Oracle VM once provisioned |

**total time:** ~2 hours of active work + wait for Oracle provisioning

---

## Integration Map (How They All Connect)

```
LEAD GENERATION
  Apollo.io (find emails) -> savvy_lead_scraper.py (score leads) -> Bland AI (call leads) -> Cal.com (book calls)

CONTENT CREATION
  Leonardo.ai (images) + Kling AI / PixVerse (video) + Suno (music) -> Buffer (schedule) -> social platforms

APP DEVELOPMENT
  Supabase (backend) + Cloudflare Pages (hosting) -> live app

AUTOMATION
  n8n (workflows) connects everything -> runs on Oracle Cloud VM (24/7)

AI TOOLS
  Dify.ai (chatbots + AI agents) -> runs on Oracle Cloud VM or cloud free tier
```

### the $0/mo full stack

```
lead gen:        Apollo (50 leads/mo) + Bland (100 calls/day) + Cal.com (unlimited bookings)
content:         Leonardo (150 tokens/day) + Kling (66 credits/day) + PixVerse (60 coins/day) + Suno (10 songs/day) + Buffer (3 channels)
hosting:         Cloudflare Pages (unlimited bandwidth) + Supabase (500MB DB + auth + storage)
automation:      n8n self-hosted (unlimited workflows) + Oracle Cloud (2 free VMs forever)
AI:              Dify.ai (200 credits or self-hosted unlimited)
security:        GoLogin (3 anti-detect profiles)
```

this replaces: Calendly ($12/mo) + Instantly ($30/mo) + Canva Pro ($13/mo) + Buffer Pro ($15/mo) + Firebase ($25/mo) + Vercel Pro ($20/mo) + Zapier ($20/mo) + Runway ($12/mo) + hosting ($20-50/mo) = **$167-197/mo saved**.

---

## After Free Tier: When to Upgrade

don't upgrade anything until it's a bottleneck.

| Tool | Upgrade When | Upgrade To | Cost |
|------|-------------|-----------|------|
| Buffer | need >3 channels or >10 posts/queue | Publer ($12/mo) or Buffer Essentials ($6/channel/mo) | $12-18/mo |
| Apollo | need >50 leads/mo | Apollo Basic ($49/mo for 900 credits) | $49/mo |
| Leonardo | need >150 tokens/day consistently | Leonardo Artisan ($12/mo for 8,500 tokens) | $12/mo |
| GoLogin | need >3 browser profiles | GoLogin Pro ($49/mo for 10 profiles) | $49/mo |
| Suno | ready to monetize music commercially | Suno Pro ($10/mo, commercial rights) | $10/mo |
| Kling | need higher quality or longer videos | Kling Standard ($8/mo) | $8/mo |
| n8n | need cloud hosting without Oracle VM | n8n Cloud ($20/mo) | $20/mo |
| Cloudflare | need server-side rendering | Vercel Pro ($20/mo) | $20/mo |
| Supabase | >500MB database or need more than 2 projects | Supabase Pro ($25/mo) | $25/mo |
| Dify | need more than 200 cloud credits | self-host on Oracle (free) or bring own API key | $0-varies |

**rule:** stay on free tier until the limitation directly costs you money. "it would be nice to have" is not a reason to upgrade. "I lost a $500 deal because I couldn't X" is.

---

## Quick Reference Card

| Tool | Free Tier | Signup URL | Setup Time |
|------|-----------|-----------|-----------|
| Bland AI | 100 calls/day | bland.ai | 15 min |
| n8n | unlimited (self-host) | n8n.io | 30-45 min |
| Buffer | 3 channels, 10 posts each | buffer.com | 10 min |
| Apollo.io | 50 credits/mo | apollo.io | 10 min |
| Cal.com | unlimited bookings | cal.com | 10 min |
| Leonardo.ai | 150 tokens/day | leonardo.ai | 5 min |
| Kling AI | 66 credits/day | klingai.com | 5 min |
| Suno | 10 songs/day | suno.com | 5 min |
| PixVerse | 60 coins/day | pixverse.ai | 5 min |
| GoLogin | 3 profiles | gologin.com | 15 min |
| Cloudflare Pages | unlimited bandwidth | cloudflare.com | 20 min |
| Supabase | 500MB DB + auth | supabase.com | 15 min |
| Dify.ai | 200 AI credits | dify.ai | 15 min |
| Oracle Cloud | 2 VMs forever | cloud.oracle.com | 30-45 min |

**total setup: ~3-4 hours. monthly cost: $0. infrastructure value: $2,000+/mo equivalent.**
