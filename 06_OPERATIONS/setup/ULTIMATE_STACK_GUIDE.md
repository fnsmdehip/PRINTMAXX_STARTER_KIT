# ULTIMATE STACK GUIDE - EVERY OPTION, EVERY HACK

**The comprehensive reference with ALL alternatives, clever workarounds, free trials, DIY options, and arbitrage opportunities.**

---

## TABLE OF CONTENTS

1. [Browser Automation Stack](#1-browser-automation-stack)
2. [Automation Without n8n/Zapier (Claude Native)](#2-automation-without-n8nzapier)
3. [LinkedIn Services & DIY](#3-linkedin-services--diy)
4. [UGC Services & Arbitrage](#4-ugc-services--arbitrage)
5. [Native Ads & Paid Traffic](#5-native-ads--paid-traffic)
6. [Free Trial Leverage Strategy](#6-free-trial-leverage-strategy)
7. [Complete Tool Comparison](#7-complete-tool-comparison)
8. [Recommended Stacks by Budget](#8-recommended-stacks-by-budget)
9. [Aged/Warmed Account Purchasing](#9-agedwarmed-account-purchasing)
10. [Engagement Bootstrapping (Grey Hat Legal)](#10-engagement-bootstrapping-grey-hat-legal)
11. [Platform-Specific Growth Services](#11-platform-specific-growth-services)
12. [Paid Engagement Services (Algo-Safe Human Farms)](#12-paid-engagement-services-algo-safe-human-farms)

---

## 1. BROWSER AUTOMATION STACK

### Priority Order (Fallback Chain)

```
1. Chrome MCP (simple tasks)
      ↓ fails
2. agent-browser (Vercel Labs) - AI-optimized, snapshot refs
      ↓ fails
3. agent-browser -p browseruse (stealth cloud, anti-bot)
      ↓ fails
4. Playwriter MCP (controls YOUR Chrome)
      ↓ fails
5. Playwright MCP (Microsoft, headless)
      ↓ fails
6. Custom Playwright scripts via Bash
      ↓ fails
7. Browserbase/Steel cloud browsers
```

### Browser Tools Comparison

| Tool | Type | Cost | Best For | Anti-Bot | URL |
|------|------|------|----------|----------|-----|
| **Chrome MCP** | Extension | Free | Simple tasks | No | Built-in |
| **agent-browser** | CLI | Free | AI workflows | Partial | github.com/vercel-labs/agent-browser |
| **Playwriter** | Extension | Free | Multi-step flows | No | github.com/remorses/playwriter |
| **Playwright MCP** | SDK | Free | Headless testing | No | github.com/microsoft/playwright-mcp |
| **browser-use** | Cloud | $0.02/min | Stealth, anti-bot | Yes | browser-use.com |
| **Browserbase** | Cloud | $0.01/min | Production scale | Yes | browserbase.com |
| **Steel** | Cloud | $0.015/min | Session persistence | Yes | steel.dev |
| **Stagehand** | SDK | Free | AI actions | Partial | github.com/browserbase/stagehand |

### Task-to-Tool Matrix

| Task | Best Tool | Fallback |
|------|-----------|----------|
| Screenshot any page | Chrome MCP | agent-browser |
| Fill simple form | Chrome MCP | agent-browser |
| Multi-step login | agent-browser --profile | Playwriter |
| Anti-bot protected | agent-browser -p browseruse | Manual |
| Twitter/X scraping | browseruse | Chrome MCP (logged in) |
| LinkedIn automation | browseruse (stealth) | Manual |
| Bulk URL processing | agent-browser CLI loop | Playwright script |
| E-commerce scraping | Playwright + proxies | browseruse |

### Setup Commands

```bash
# agent-browser (Vercel Labs)
npm install -g agent-browser
agent-browser install  # Downloads Chromium

# browseruse (stealth cloud)
export BROWSER_USE_API_KEY="your-key"
agent-browser -p browseruse open https://protected-site.com

# Playwright MCP
npx @anthropic-ai/playwright-mcp

# Browserbase
npx skills add browserbase/agent-browse
```

---

## 2. AUTOMATION WITHOUT n8n/ZAPIER

### Why You Don't Need n8n/Make/Zapier

**You have Claude Max ($200/mo) which gives you:**
- Unlimited agent conversations
- Can run scripts via Bash tool
- Can schedule with cron on any VPS
- Can use Ralph loops for overnight automation
- Claude writes + runs the automation code

### Claude-Native Automation Stack

**Architecture:**
```
Hetzner VPS ($5/mo)
    ├── cron jobs (scheduling)
    ├── Python scripts (Claude writes these)
    ├── Playwright (browser automation)
    └── ralph loops (overnight builds)
```

**Instead of n8n workflow → Claude writes Python script:**
```python
# Example: Daily competitor monitor
# Claude writes this, cron runs it

import requests
from datetime import datetime

def check_competitor_prices():
    # Scrape competitors
    # Compare to yesterday
    # Alert if changes
    pass

if __name__ == "__main__":
    check_competitor_prices()
```

**Schedule with cron:**
```bash
# Run daily at 9am
0 9 * * * python3 /path/to/competitor_monitor.py
```

### Ralph Loops (Overnight Automation)

**Pattern:**
```bash
while :; do cat prompt.md | claude ; done
```

**What ralph does:**
- Fresh context each iteration (no memory rot)
- File-based state (progress.md, guardrails.md)
- Can run for hours/days unattended
- Perfect for: content generation, research, batch processing

**Run overnight:**
```bash
cd ralph && nohup ./run_all_loops.sh > ralph_overnight.log 2>&1 &
```

### When You Actually Need n8n/Make

Only if:
- Complex multi-service integrations (Slack + Airtable + Gmail + etc.)
- Non-technical team needs to modify workflows
- Visual workflow is required for clients/team

**If you DO need it:**
- Self-host n8n on Hetzner ($5/mo total)
- Or use Make.com free tier (1,000 ops/mo)

---

## 3. LINKEDIN SERVICES & DIY

### Done-For-You LinkedIn Services

| Service | Price | What They Do | URL |
|---------|-------|--------------|-----|
| **InMailers** | Per InMail | Outsourced InMail sending | inmailers.co |
| **Cleverly** | $397-797/mo | Full LinkedIn done-for-you |ly  cleverly.co |
| **LinkedSelling** | Custom | Agency LinkedIn campaigns | linkedselling.com |
| **Pearl Lemon** | $2k+/mo | LinkedIn + lead gen agency | pearllemon.com |
| **BAMF Media** | Custom | LinkedIn growth service | bamf.co |

### DIY LinkedIn Automation

| Tool | Price | Safety | Best For | URL |
|------|-------|--------|----------|-----|
| **Expandi** | $99/mo | Safest | Cloud automation | expandi.io |
| **Dripify** | $59/mo | Safe | Sequences | dripify.io |
| **Waalaxy** | Free-$80/mo | Good | Budget | waalaxy.com |
| **Dux-Soup** | $15-55/mo | Medium | Simple | dux-soup.com |
| **Phantombuster** | $69/mo | Medium | Multi-platform | phantombuster.com |
| **LinkedHelper** | $15-45/mo | Risky | Desktop only | linkedhelper.com |
| **Salesflow** | $99/mo | Safe | Teams | salesflow.io |
| **Closely** | $59/mo | Good | CRM integration | closelyhq.com |

### The Sorority BDR Hack (@codyschneiderxx)

**The play:**
- Hire college sorority girls as BDRs
- $15-20/hr (cheap labor)
- Naturally good at relationship building
- Authentic, not "salesy"
- Available part-time (flexible)

**How to execute:**
1. Post on college job boards targeting Greek life
2. Search: "sorority" on LinkedIn, filter by college students
3. Find via Instagram: Alabama Rush Day, recruitment content
4. Offer $15-20/hr base + $10-25/meeting booked bonus

**Their tasks:**
- Send 50-100 LinkedIn connection requests/day
- Send personalized follow-up messages
- Book calls with qualified prospects
- Track in CRM

**Why it works:**
- Natural relationship builders
- Comfortable with outreach (recruitment experience)
- Lower cost than traditional SDRs ($50k+/yr)
- More authentic than automation

### LinkedIn Limits (2026)

| Action | Daily Limit | Weekly Limit |
|--------|-------------|--------------|
| Connection requests | 25-30 | 150-200 |
| Messages (1st connections) | 150 | 1000 |
| InMails (if Premium) | 50 | 150 |
| Profile views | 500 | 2500 |
| Searches | 300 | 1500 |

**Safety tips:**
- Stay 50% below limits
- Warm up new accounts 2 weeks
- Use dedicated proxy per account
- Vary activity times (not robotic)

---

## 4. UGC SERVICES & ARBITRAGE

### UGC Marketplaces (Pay Premium)

| Platform | Price/Video | Best For | URL |
|----------|-------------|----------|-----|
| **Billo** | $100-300 | Quick turnaround | billo.app |
| **Insense** | $100-500 | Brand safety | insense.pro |
| **Trend.io** | $150-400 | Vetted creators | trend.io |
| **#paid** | $200-500 | Enterprise | hashtagpaid.com |
| **Grin** | Custom | Influencer management | grin.co |
| **Aspire** | Custom | Enterprise | aspire.io |
| **Collabstr** | $50-200 | Budget marketplace | collabstr.com |

### UGC Arbitrage (Cheap Sources)

**EASTERN EUROPE ($3-25/video)**

| Source | Price | Quality | How to Access |
|--------|-------|---------|---------------|
| **@dansugcmodels roster** | $3-20 | Medium-High | DM on X/Twitter |
| **@franci__ugc** | $10-30 | High | DM on X/Twitter |
| **Ukraine creators** | $3-15 | Medium | Instagram hashtags |
| **Poland creators** | $15-40 | High | #ugcpolska |
| **Romania/Bulgaria** | $10-30 | Medium-High | TikTok, Instagram |

**SOUTHEAST ASIA ($10-35/video)**

| Source | Price | Quality | How to Access |
|--------|-------|---------|---------------|
| **Philippines** | $10-30 | Medium-High | OnlineJobs.ph |
| **Indonesia** | $10-25 | Medium | Instagram |
| **Vietnam** | $10-30 | Medium | Upwork |

**LATIN AMERICA ($15-60/video)**

| Source | Price | Quality | How to Access |
|--------|-------|---------|---------------|
| **Colombia** | $20-50 | High | #ugccolombia |
| **Mexico** | $15-40 | Medium-High | Workana |
| **Brazil** | $20-60 | High | Instagram |

### AI UGC Stack (Cheapest)

| Tool | Cost | Output | URL |
|------|------|--------|-----|
| **Arcads** | Per video | Hyper-real AI actors | arcads.ai |
| **HeyGen** | $24-180/mo | AI avatars | heygen.com |
| **Creatify** | $19-89/mo | AI ad videos | creatify.ai |
| **Synthesia** | $30-90/mo | Professional presenters | synthesia.io |
| **D-ID** | $6-108/mo | Talking heads | d-id.com |
| **Sovran** | $15-50/mo | AI spokespersons | sovran.video |

### AI Video Generation Tools (Feb 2026 — Full Comparison)

**Full comparison doc:** `MONEY_METHODS/AI_INFLUENCER/AI_VIDEO_TOOLS_COMPARISON.md`

| Tool | Maker | Free Tier | Paid From | Max Length | Quality | Best For |
|------|-------|-----------|-----------|------------|---------|----------|
| **Veo 3.1** | Google | 100 credits/mo | $19.99/mo | 8s | 9.5/10 | Hero ads, cinematic realism |
| **Sora 2** | OpenAI | None (killed Jan 2026) | $20/mo (Plus) | 20s (Pro) | 9/10 | Storytelling, dialogue |
| **Seedance 2.0** | ByteDance | FREE on Xiao Yunque app | ~$9.60/mo | 15s | 9/10 | Multimodal reference, lip sync 8+ languages |
| **Kling 2.6** | Kuaishou | 66 credits/day | $6.99/mo | 2 min | 8.5/10 | Volume production, best price-to-quality |
| **Runway Gen-4.5** | Runway | Limited 720p | $12/mo | 16s | 8/10 | Creative camera, experimentation |
| **Pika 2.5** | Pika Labs | Yes (limited) | $8/mo | 10s | 7.5/10 | Quick social clips |
| **Hailuo/MiniMax** | MiniMax | 20-30 clips | $9.99/mo | 10s | 7.5/10 | Budget volume |
| **Luma Ray 3** | Luma Labs | 30 credits/mo | $7.99/mo | 10s | 7/10 | Artistic/stylized |

**Seedance 2.0 (NEW):** ByteDance's flagship. The only model accepting images + videos + audio + text simultaneously (up to 12 files). Native audio-visual generation. Phoneme-level lip sync in 8+ languages. Currently free on Xiao Yunque app during promo period. API launching Feb 24 2026.

**$0 Budget Stack:** Seedance free (Xiao Yunque) + Kling free (66/day) + Veo free (100/mo) + Pika free = 5-8 videos/day at zero cost.

**Updated Nano Banana Workflow (2026):**
```
Pinterest reference → Seedream 5.0 or Nano Banana (image gen)
  → Seedance 2.0 (video + native audio, image as reference input)
  → OR Kling 2.6 (motion, up to 2 min clips)
  → ElevenLabs (voiceover if needed, Seedance has native audio)
  → CapCut (final edit + captions)
  → Buffer/Publer (distribute)

Cost: $0 (all free tiers) to ~$0.10-0.50/video (paid tiers)
```

### UGC Arbitrage Math

```
Source: @dansugcmodels Ukraine creator = $10/video
Sell to US brand: $150/video
Margin: 93%

At 20 videos/month:
Cost: $200
Revenue: $3,000
Profit: $2,800
```

### Clip Editing Services (Cheap Labor)

| Source | Price | Best For | URL |
|--------|-------|----------|-----|
| **OnlineJobs.ph** | $3-6/hr | Filipino editors | onlinejobs.ph |
| **Upwork** | $5-15/hr | Mixed quality | upwork.com |
| **Fiverr** | $5-50/video | Quick turnaround | fiverr.com |
| **Video Husky** | $399/mo | Unlimited edits | videohusky.com |
| **Vidchops** | $195/mo | Unlimited edits | vidchops.com |

---

## 5. NATIVE ADS & PAID TRAFFIC

### Native Ad Platforms

| Platform | Min Spend | CPM | CPC | Best For | URL |
|----------|-----------|-----|-----|----------|-----|
| **MGID** | $100/day | $0.20-1.00 | $0.05-0.30 | Testing | dashboard.mgid.com |
| **Taboola** | $500/day | $0.30-1.50 | $0.10-0.60 | Scale | business.taboola.com |
| **Outbrain** | $500/day | $0.50-2.00 | $0.15-0.80 | Premium | my.outbrain.com |
| **Revcontent** | $100/day | $0.40-1.50 | $0.10-0.50 | Quality | revcontent.com |
| **Content.ad** | $50/day | $0.15-0.80 | $0.03-0.20 | Budget | content.ad |
| **Yahoo DSP** | $1k+/day | Varies | Varies | Brand safe | advertising.yahoo.com |

### Native Ads vs Meta Comparison

| Factor | Native | Meta |
|--------|--------|------|
| Account ban risk | Very low | High |
| Creative format | Headline + image | Video/image |
| Learning curve | Different | Familiar |
| Scale ceiling | Very high | Account limited |
| Creative burnout | Low | High |
| Cost per click | $0.05-0.50 | $0.50-3.00 |

### Native Ads Scaling Path

```
$100-500/day (MGID) → Test headlines/thumbnails
$500-2k/day (Taboola) → Scale winners
$2k-10k/day (Multi-platform) → Add Outbrain, Revcontent
$10k+/day → All platforms + international
```

### Paid Ads Services (Done-For-You)

| Service | Price | Platforms | URL |
|---------|-------|-----------|-----|
| **KlientBoost** | $3k+/mo | Meta, Google | klientboost.com |
| **Directive** | $5k+/mo | B2B focused | directiveconsulting.com |
| **MuteSix** | $5k+/mo | DTC focused | mutesix.com |
| **Common Thread** | $10k+/mo | Enterprise DTC | commonthreadco.com |
| **Disruptive Advertising** | $3k+/mo | Multi-platform | disruptiveadvertising.com |

### Ad Spy Tools

| Tool | Price | Platforms | URL |
|------|-------|-----------|-----|
| **Anstrex** | $80-180/mo | Native, push | anstrex.com |
| **AdPlexity** | $149-249/mo | All types | adplexity.com |
| **PowerAdSpy** | $49-249/mo | Social | poweradspy.com |
| **BigSpy** | $9-99/mo | All platforms | bigspy.com |
| **Minea** | $49-99/mo | Product ads | minea.com |
| **PiPiADS** | $77-155/mo | TikTok | pipiads.com |

---

## 6. FREE TRIAL LEVERAGE STRATEGY

### The @paoloanzn Free Trial Arbitrage

**The play:**
1. Sign up for all tools with free trials
2. Build/ship during trial period
3. Only subscribe to what you actually need
4. Stack trials strategically (not all at once)

### Free Trial Calendar

**Week 1-2:** Research & Planning
| Tool | Trial | Use During Trial |
|------|-------|------------------|
| Apollo.io | 14 days | Export all leads you need |
| Instantly | 14 days | Test email campaigns |
| Semrush | 7 days | All keyword research |
| Ahrefs | 7 days | Competitor backlink analysis |

**Week 3-4:** Content & Creative
| Tool | Trial | Use During Trial |
|------|-------|------------------|
| Midjourney | None (sub only) | Skip or use Leonardo |
| HeyGen | Credits | Generate AI videos |
| Runway | 125 credits | Test video generation |
| InVideo | 7 days | Create faceless videos |

**Week 5-6:** Automation & Scale
| Tool | Trial | Use During Trial |
|------|-------|------------------|
| Expandi | 7 days | Set up LinkedIn sequences |
| Phantombuster | 14 days | Build scraping workflows |
| Make.com | Free tier | Build key automations |

### Tools with Generous Free Tiers (Keep Forever)

| Tool | Free Tier | Good Enough For |
|------|-----------|-----------------|
| **Apollo.io** | 600 credits/mo | Initial lead research |
| **Hunter.io** | 25 searches/mo | Quick email lookups |
| **Canva** | Most features | All design needs |
| **Notion** | Unlimited | All project management |
| **HubSpot CRM** | Unlimited contacts | Full CRM |
| **Buffer** | 3 channels | Basic scheduling |
| **Mailchimp** | 500 contacts | Starting email list |
| **Leonardo.ai** | 150 tokens/day | AI images |
| **CapCut** | Full features | Video editing |
| **Loom** | 25 videos | Quick recordings |
| **Calendly** | 1 event type | Basic scheduling |
| **Typeform** | 10 responses/mo | Simple forms |
| **Airtable** | 1,200 records | Small databases |
| **Trello** | Unlimited | Task management |
| **Slack** | 90 days history | Team chat |
| **GitHub** | Unlimited | Code hosting |
| **Vercel** | 100GB | Frontend hosting |
| **Cloudflare** | Unlimited | DNS + security |
| **PostHog** | 1M events | Analytics (self-host) |
| **Plausible** | None (self-host free) | Privacy analytics |
| **n8n** | Self-host free | Automation |
| **Umami** | Self-host free | Analytics |

### Referral/Credit Hacks

| Tool | Referral Bonus | How to Get |
|------|----------------|------------|
| **DigitalOcean** | $200 credit | Use referral link |
| **Hetzner** | €20 credit | Use referral code |
| **Railway** | $5 credit | New account |
| **Render** | Free tier | No card required |
| **Vercel** | Hobby free | No card required |
| **Supabase** | 500MB free | No card required |
| **PlanetScale** | 5GB free | No card required |

---

## 7. COMPLETE TOOL COMPARISON

### Hosting

| Provider | Cheapest | Best Value | URL |
|----------|----------|------------|-----|
| **Hetzner** | $4/mo (2GB) | $7/mo (4GB) | hetzner.com |
| **Contabo** | $6/mo (8GB!) | Best RAM/$ | contabo.com |
| **DigitalOcean** | $6/mo (1GB) | $12/mo (2GB) | digitalocean.com |
| **Vultr** | $5/mo (1GB) | Good middle | vultr.com |
| **Linode** | $5/mo (1GB) | Reliable | linode.com |
| **AWS Lightsail** | $3.50/mo | AWS ecosystem | lightsail.aws |
| **Oracle Cloud** | FREE (4 cores!) | Best free | oracle.com/cloud |

**Winner:** Oracle Cloud free tier (if available) → Hetzner (paid)

### Cold Email

| Tool | Price | Unlimited Inboxes | Built-in Warmup | URL |
|------|-------|-------------------|-----------------|-----|
| **Instantly** | $37-97/mo | Yes | Yes | instantly.ai |
| **Smartlead** | $39-94/mo | Yes | Yes | smartlead.ai |
| **Emailbison** | $39-149/mo | Yes | Yes | emailbison.com |
| **Lemlist** | $59-99/mo | No (3) | Yes | lemlist.com |
| **Apollo** | $49-79/mo | No | No | apollo.io |
| **Reply.io** | $60-90/mo | No (1) | Yes | reply.io |

**Winner:** Smartlead (scale) or Instantly (beginner)

### Pre-Warmed Inboxes

| Service | Price | Skip Warmup | URL |
|---------|-------|-------------|-----|
| **DeliverOn** | $49/inbox/mo | Yes | deliveron.org |
| **Mailforge** | $3/inbox | Partial | mailforge.ai |
| **Mailscale** | $39/mo | Yes | mailscale.com |
| **Inframail** | $99/mo | Yes | inframail.io |

**Winner:** DeliverOn (time > money) or Mailforge (budget)

### Proxies

| Provider | Residential | Mobile | Best For | URL |
|----------|-------------|--------|----------|-----|
| **Soax** | $6.60/GB | $150/mo | Budget | soax.com |
| **Decodo/Smartproxy** | $12.50/GB | $200/mo | Scale | smartproxy.com |
| **IPRoyal** | $7/GB | $90/mo | Budget alt | iproyal.com |
| **Bright Data** | $15/GB | $300/mo | Enterprise | brightdata.com |
| **Oxylabs** | $15/GB | $300/mo | Enterprise | oxylabs.io |

**Winner:** Soax (budget) → Decodo (scale)

### AI Voice

| Tool | Free Tier | Paid | Quality | URL |
|------|-----------|------|---------|-----|
| **ElevenLabs** | 10k chars | $5-22/mo | Best | elevenlabs.io |
| **Play.ht** | Trial | $31/mo | Very good | play.ht |
| **Murf.ai** | 10 mins | $29/mo | Good | murf.ai |
| **Speechify** | Limited | $139/yr | Good | speechify.com |
| **Resemble.ai** | Trial | $24/mo | Cloning | resemble.ai |

**Winner:** ElevenLabs (has MCP integration for Claude)

### AI Video

| Tool | Free Tier | Paid | Best For | URL |
|------|-----------|------|----------|-----|
| **Kling** | 66 credits/day | $5-30/mo | Long clips | klingai.com |
| **Runway** | 125 credits | $15-95/mo | Quality | runwayml.com |
| **Pika** | 250 credits | $8-35/mo | Stylized | pika.art |
| **Luma** | 30 gens/mo | $24-96/mo | Fast | lumalabs.ai |
| **HeyGen** | Trial | $24-180/mo | Avatars | heygen.com |
| **InVideo AI** | Trial | $25-60/mo | Faceless | invideo.io |

**Winner:** Kling (value) or InVideo AI (faceless automation)

### Community Platforms

| Platform | Free Tier | Paid | Best For | URL |
|----------|-----------|------|----------|-----|
| **Discord** | Yes | Free | Gaming/tech | discord.com |
| **Skool** | No | $99/mo | Courses | skool.com |
| **Circle** | No | $39-99/mo | Premium | circle.so |
| **Whop** | Yes | Per sale | Products | whop.com |
| **Mighty Networks** | No | $39-99/mo | Full platform | mightynetworks.com |
| **Geneva** | Yes | Free | Events | geneva.com |
| **Telegram** | Yes | Free | Crypto/anon | telegram.org |

**Winner:** Discord (free) or Skool (paid community)

### Newsletter

| Platform | Free Tier | Paid | Best For | URL |
|----------|-----------|------|----------|-----|
| **Beehiiv** | 2,500 subs | $49/mo | Growth | beehiiv.com |
| **Substack** | Unlimited | 10% of paid | Writers | substack.com |
| **ConvertKit** | 1,000 subs | $29/mo | Creators | convertkit.com |
| **Buttondown** | 100 subs | $9/mo | Simple | buttondown.email |
| **Ghost** | Self-host | $9-25/mo | Publishing | ghost.org |

**Winner:** Beehiiv (growth) or Substack (simplest)

---

## 8. RECOMMENDED STACKS BY BUDGET

### BROKE STACK ($0-50/mo)

```
HOSTING
├── Oracle Cloud free tier (4 cores, 24GB RAM!)
├── OR Vercel free (frontend)
├── Cloudflare free (DNS, security)

EMAIL
├── Gmail free (personal sending)
├── OR Zoho Mail $1/mo (custom domain)

AUTOMATION
├── Claude Max (you have it)
├── Cron jobs on Oracle free VPS
├── ralph loops for overnight

TOOLS (all free tiers)
├── Apollo.io (600 credits/mo)
├── Hunter.io (25/mo)
├── Canva
├── Notion
├── HubSpot CRM
├── Leonardo.ai (AI images)
├── CapCut (video editing)
├── Buffer (3 channels)

TOTAL: ~$0-20/mo
```

### BOOTSTRAP STACK ($100-200/mo)

```
HOSTING
├── Hetzner VPS: $5/mo
├── Vercel free: $0
├── Cloudflare: $0

DOMAINS
├── Porkbun: ~$50/yr (4-5 domains)

EMAIL
├── Google Workspace: $18/mo (3 inboxes)
├── Emailbison: $39/mo
├── Built-in warmup

PROXIES
├── Soax 5GB: $33/mo

VOICE
├── ElevenLabs free tier: $0

LINKEDIN
├── Waalaxy free tier: $0

UGC
├── @dansugcmodels: $10-20/video as needed

TOTAL: ~$95-150/mo
```

### GROWTH STACK ($300-500/mo)

```
HOSTING
├── Hetzner: $7/mo
├── Vercel Pro: $20/mo

DOMAINS
├── Cloudflare: ~$50/yr

EMAIL
├── Google Workspace: $36/mo (6 inboxes)
├── Instantly: $97/mo
├── Apollo Pro: $79/mo

PROXIES
├── Soax: $66/mo (10GB)
├── Decodo: $62/mo (5GB backup)

VOICE
├── ElevenLabs Creator: $22/mo

VIDEO
├── Kling: $30/mo
├── CapCut: $0

LINKEDIN
├── Expandi: $99/mo

UGC
├── Eastern EU creators: ~$200/mo (20 videos)
├── HeyGen: $24/mo (AI backup)

TOTAL: ~$400-500/mo
```

### SCALE STACK ($800-1500/mo)

```
HOSTING
├── Hetzner: $15/mo (dedicated)
├── Vercel Team: $50/mo
├── Cloudflare Pro: $20/mo

EMAIL
├── Google Workspace: $72/mo (12 inboxes)
├── Smartlead: $94/mo
├── Instantly: $97/mo (backup)
├── DeliverOn: $147/mo (3 pre-warmed)
├── Apollo: $79/mo

PROXIES
├── Decodo: $200/mo (20GB)
├── Mobile proxies: $180/mo (2x dedicated)

VOICE
├── ElevenLabs Pro: $22/mo

VIDEO
├── Runway: $95/mo
├── HeyGen: $180/mo (unlimited)
├── InVideo AI: $60/mo

LINKEDIN
├── Expandi: $99/mo
├── Sales Navigator: $135/mo
├── Sorority BDRs: $500/mo (part-time)

NATIVE ADS
├── MGID: $1000/mo (testing)
├── Taboola: $5000/mo (scaling)

UGC
├── Creator network: $500/mo
├── AI backup: included above

TOTAL: ~$1200-1500/mo (excl ads spend)
```

---

## QUICK URL REFERENCE

### BLOCKING (Do First)
```
https://developer.apple.com/programs/enroll/  ($99)
https://play.google.com/console/signup  ($25)
```

### HOSTING
```
https://hetzner.com
https://oracle.com/cloud/free  (FREE!)
https://vercel.com
https://cloudflare.com
```

### DOMAINS
```
https://porkbun.com
https://cloudflare.com/registrar
```

### EMAIL
```
https://workspace.google.com
https://instantly.ai
https://smartlead.ai
https://emailbison.com
https://deliveron.org
https://apollo.io
```

### PROXIES
```
https://soax.com
https://smartproxy.com
https://iproyal.com
https://smspool.net
```

### LINKEDIN
```
https://expandi.io
https://dripify.io
https://waalaxy.com
https://inmailers.co
https://linkedin.com/sales/
```

### UGC
```
DM @dansugcmodels on X ($3-20/video)
DM @franci__ugc on X ($10-30/video)
https://billo.app
https://insense.pro
https://arcads.ai
https://heygen.com
https://creatify.ai
```

### NATIVE ADS
```
https://dashboard.mgid.com
https://business.taboola.com
https://my.outbrain.com
https://revcontent.com
```

### AI TOOLS
```
https://elevenlabs.io
https://klingai.com
https://runwayml.com
https://invideo.io
https://leonardo.ai
```

### BROWSER AUTOMATION
```
https://github.com/vercel-labs/agent-browser
https://github.com/remorses/playwriter
https://browser-use.com
https://browserbase.com
https://steel.dev
```

---

## 9. AGED/WARMED ACCOUNT PURCHASING

### Why Buy Aged Accounts

- Skip 2-4 week warmup period
- Higher trust scores = higher limits
- Faster to automation-ready state
- Better deliverability from day 1
- Can buy with established follower base

### Account Marketplaces

| Source | Platforms | Price Range | Quality | URL |
|--------|-----------|-------------|---------|-----|
| **AccsMarket** | All platforms | $15-80 | Best reputation | accsmarket.com |
| **Fameswap** | Instagram, TikTok, YT | $100-10k+ | Verified followers | fameswap.com |
| **SocialTradia** | All platforms | $50-5k | Multi-platform | socialtradia.com |
| **PlayerUp** | Gaming/social | $20-500 | Mixed quality | playerup.com |
| **Swapd** | Premium accounts | $500-50k | Verified, established | swapd.co |
| **ViralAccounts** | Instagram focus | $100-2k | Niche accounts | viralaccounts.com |
| **TooFame** | TikTok, IG | $50-1k | Budget option | toofame.com |

### What to Look For

**Good Signs:**
- Account age 6+ months
- Consistent posting history
- Real engagement (not just followers)
- No previous bans/strikes
- Clean email (not temp)
- 2FA already enabled

**Red Flags:**
- Recently mass-followed/unfollowed
- Sudden follower spikes
- Empty email or temp email
- Previous action blocks
- Suspicious country of origin
- Seller has no reputation

### Post-Purchase Protocol (CRITICAL)

```
DAY 1:
├── Change password immediately
├── Add YOUR 2FA (authenticator app)
├── Update email to yours
├── DO NOT change profile info yet
└── Just browse/watch content

DAY 2-3:
├── Light manual activity only
├── 5-10 likes, 2-3 comments
├── View stories/reels
└── NO automation, NO new connections

DAY 4-7:
├── Gradually update profile
├── Assign dedicated proxy (one account per proxy)
├── Increase activity slightly
└── Still NO automation

WEEK 2+:
├── Light automation if needed
├── Stay at 50% of normal limits
├── Monitor closely for blocks
└── Never do aggressive actions
```

### Platform-Specific Notes

| Platform | Best Source | Warmup Time | Notes |
|----------|-------------|-------------|-------|
| Instagram | Fameswap, AccsMarket | 5-7 days | Mobile proxy REQUIRED |
| TikTok | SocialTradia | 7-14 days | NO automation, manual only |
| X/Twitter | AccsMarket | 3-5 days | Most lenient |
| LinkedIn | AccsMarket | 7-14 days | Cloud automation only |
| Email domains | DeliverOn, Mailforge | 0 days | Pre-warmed, instant use |

---

## 10. ENGAGEMENT BOOTSTRAPPING (GREY HAT LEGAL)

### Legal Status Overview

| Method | Legal Status | Platform TOS | Risk Level |
|--------|--------------|--------------|------------|
| Engagement pods | ✅ LEGAL | ✅ Allowed | LOW |
| Shoutout trades | ✅ LEGAL | ✅ Allowed | NONE |
| Paid shoutouts | ✅ LEGAL | ✅ Allowed | NONE |
| Collab posts | ✅ LEGAL | ✅ Allowed | NONE |
| Launch coordination | ✅ LEGAL | ⚠️ Grey | LOW |
| Human engagement services | ✅ LEGAL | ⚠️ TOS violation | MEDIUM |
| Follow/unfollow (manual) | ✅ LEGAL | ⚠️ TOS violation | MEDIUM |
| Bought followers | ⚠️ GREY | ❌ TOS violation | MEDIUM-HIGH |
| Bot engagement | ⚠️ GREY | ❌ TOS violation | HIGH |
| Fake reviews | ❌ ILLEGAL | ❌ TOS violation | CRITICAL |

### Tier 1: Zero Risk Methods

**Engagement Pods**
- Private groups where members engage with each other's content
- Telegram, Discord, Facebook groups
- Free to join, reciprocity required
- Find: Search "engagement pod + [niche]" in Telegram

**Shoutout Trades**
- Exchange posts with similar-sized accounts
- No money changes hands
- Find similar accounts, DM for trade
- Works best with 100-1000 follower parity

**Collab Posts (Instagram)**
- Use Instagram's native collab feature
- Both accounts get reach
- Algorithm boost from dual engagement
- Best tactic for organic growth

**Cross-Promotion**
- Promote your accounts across platforms
- "Follow me on TikTok" from Instagram
- Link in bio strategies
- Email list to social

### Tier 2: Paid But Legal

| Method | Cost | Effectiveness | Where to Find |
|--------|------|---------------|---------------|
| **Paid shoutouts** | $20-500 | HIGH | DM creators directly |
| **Influencer seeding** | Product cost | HIGH | Send free products |
| **Podcast guesting** | Free-$500 | HIGH | MatchMaker.fm, PodcastGuests.com |
| **Newsletter features** | $50-500 | MEDIUM | SparkLoop, Beehiiv collabs |
| **Product Hunt launch** | Free | HIGH if executed well | producthunt.com |
| **Giveaway collaborations** | $50-500 | HIGH | Partner with 3-5 accounts |

### Tier 3: Grey Area (TOS Violation, Not Illegal)

**Human Engagement Services**

| Service | Platform | Cost | Method | URL |
|---------|----------|------|--------|-----|
| **Kicksta** | Instagram | $49-99/mo | AI-targeted likes | kicksta.co |
| **Growthoid** | Instagram | $49-99/mo | Human team | growthoid.com |
| **Upleap** | Instagram | $59-99/mo | Managed service | upleap.com |
| **SocialBee** | Multi | $29-99/mo | Scheduling + engagement | socialbee.com |

**Follow/Unfollow Services**
- Done manually by human teams
- Lower ban risk than bots
- Slower but safer growth
- Cost: $50-200/mo typically

### What's Currently Working (Jan 2026)

**Instagram:**
- ✅ Reels (algorithm priority)
- ✅ Story viewing automation (undetectable)
- ✅ Targeted likes on competitor followers
- ✅ First-comment strategy on big accounts
- ✅ Collab posts with similar accounts
- ⚠️ Follow/unfollow (works but risky)
- ❌ Mass DM automation (restricted quickly)
- ❌ Comment bots (detected immediately)
- ❌ Chrome extensions (instant detection)

**TikTok:**
- ✅ Post 3-5x/day (consistent timing)
- ✅ Duets and stitches for initial traction
- ✅ Trending sounds (within 24-48 hrs)
- ✅ Hook in first 1 second
- ❌ **ALL automation tools** (detection too aggressive)
- ❌ Bought views (algorithm detects)
- ❌ Browser-based posting (app only)
- ❌ VPN usage (instant flag)

**X/Twitter:**
- ✅ Reply-guy strategy (first to reply on big accounts)
- ✅ Quote tweets with added value
- ✅ Thread format for authority
- ✅ Posting 4-8x/day
- ✅ Engagement pods (private groups)
- ✅ Self-reply funnels for CTAs
- ⚠️ Auto-DM on follow (risky if spammy)

**LinkedIn:**
- ✅ Carousels/document posts (highest reach)
- ✅ Voice notes in DMs (3x higher response rate)
- ✅ Commenting strategy before posting
- ✅ Multi-channel: DM → Email sequence
- ⚠️ Cloud automation only (Expandi/Dripify)
- ❌ Chrome extensions (instant detection)
- ❌ Desktop automation tools (banned)

### Safe Limits (Jan 2026)

**Instagram (Aged Account 2mo+):**
| Action | Daily Limit | Notes |
|--------|-------------|-------|
| Follows | 30-50 | Spread across 8-12 hours |
| Unfollows | 30-50 | Same as follows |
| Likes | 100-150 | Wait 30-60s between |
| Comments | 20-30 | Unique, not generic |
| DMs | 10-20 | Personalized only |
| Story views | Unlimited | Safe to automate |

**TikTok (NO automation recommended):**
| Action | Daily Limit | Notes |
|--------|-------------|-------|
| Follows | 100-200 | Manual only |
| Likes | 300-500 | Manual only |
| Comments | 50-100 | Manual only |
| Videos | 3-5 | Use native scheduler |

**X/Twitter (Most Lenient):**
| Action | Daily Limit | Notes |
|--------|-------------|-------|
| Follows | 200-400 | Can be automated |
| Likes | 500-1000 | Automation OK |
| Tweets | 20-50 | Use scheduler |
| DMs | 50-100 | Personalized |
| Retweets | 200-300 | Automation OK |

**LinkedIn (Conservative Required):**
| Action | Daily Limit | Notes |
|--------|-------------|-------|
| Connection requests | 20-30 | Max 100/week free |
| Messages | 25-50 | Personalized |
| Profile views | 100-200 | Can be automated |

---

## 11. PLATFORM-SPECIFIC GROWTH SERVICES

### Instagram

| Service | Price | Method | Safety | URL |
|---------|-------|--------|--------|-----|
| **Kicksta** | $49-99/mo | AI-targeted likes | HIGH | kicksta.co |
| **Growthoid** | $49-99/mo | Human team | HIGHEST | growthoid.com |
| **Upleap** | $59-99/mo | Managed service | HIGH | upleap.com |
| **Jarvee** | $30-70/mo | Desktop automation | MEDIUM | jarvee.com |
| **Path Social** | $69-249/mo | Organic growth | HIGH | pathsocial.com |
| **Nitreo** | $49-79/mo | Targeted growth | HIGH | nitreo.com |

### TikTok

| Service | Price | Method | Safety | URL |
|---------|-------|--------|--------|-----|
| **Manual only** | Free | DIY | HIGHEST | N/A |
| **TokUpgrade** | $15-49/mo | Engagement | LOW (ban risk) | tokupgrade.com |
| **UseViral** | $12-40/mo | Boost | VERY LOW | useviral.com |

**TikTok Warning:** ALL automation services have HIGH ban risk in 2026. Manual growth only recommended.

### X/Twitter

| Service | Price | Method | Safety | URL |
|---------|-------|--------|--------|-----|
| **Hypefury** | $19-49/mo | Scheduling + engagement | HIGH | hypefury.com |
| **TweetHunter** | $49/mo | AI tweets + CRM | HIGH | tweethunter.io |
| **Tweetlio** | $12/mo | Scheduling | HIGH | tweetlio.com |
| **Circleboom** | $17-79/mo | Analytics + growth | HIGH | circleboom.com |
| **Audiense** | $39-99/mo | Audience intelligence | HIGH | audiense.com |

### LinkedIn

| Service | Price | Method | Safety | URL |
|---------|-------|--------|--------|-----|
| **Expandi** | $99/mo | Cloud automation | HIGHEST | expandi.io |
| **Dripify** | $59/mo | Drip sequences | HIGH | dripify.io |
| **Waalaxy** | $56/mo | Multi-channel | MEDIUM | waalaxy.com |
| **Salesflow** | $99/mo | Teams | HIGH | salesflow.io |
| **Closely** | $59/mo | CRM integration | HIGH | closelyhq.com |
| **LinkedHelper** | $15-45/mo | Desktop | RISKY | linkedhelper.com |

### Multi-Platform

| Service | Price | Platforms | URL |
|---------|-------|-----------|-----|
| **Buffer** | $0-120/mo | All major | buffer.com |
| **Hootsuite** | $99+/mo | All major | hootsuite.com |
| **Later** | $18-80/mo | Visual platforms | later.com |
| **Sprout Social** | $249+/mo | Enterprise | sproutsocial.com |
| **SocialBee** | $29-99/mo | All + engagement | socialbee.com |
| **Publer** | $12-25/mo | All major | publer.io |

---

## QUICK URL REFERENCE (FULL LIST)

### BLOCKING (Do First)
```
https://developer.apple.com/programs/enroll/  ($99)
https://play.google.com/console/signup  ($25)
```

### HOSTING
```
https://hetzner.com
https://oracle.com/cloud/free  (FREE!)
https://vercel.com
https://cloudflare.com
https://contabo.com  (Best RAM/$)
https://vultr.com
https://railway.app
```

### DOMAINS
```
https://porkbun.com
https://cloudflare.com/registrar
https://namecheap.com
```

### EMAIL
```
https://workspace.google.com
https://instantly.ai
https://smartlead.ai
https://emailbison.com
https://deliveron.org
https://apollo.io
https://mailforge.ai
https://hunter.io
https://neverbounce.com
```

### PROXIES
```
https://soax.com
https://smartproxy.com
https://iproyal.com
https://smspool.net
https://brightdata.com
https://oxylabs.io
```

### LINKEDIN
```
https://expandi.io
https://dripify.io
https://waalaxy.com
https://inmailers.co
https://linkedin.com/sales/
https://closely.com
https://salesflow.io
```

### INSTAGRAM GROWTH
```
https://kicksta.co
https://growthoid.com
https://upleap.com
https://nitreo.com
https://pathsocial.com
```

### X/TWITTER GROWTH
```
https://hypefury.com
https://tweethunter.io
https://tweetlio.com
https://circleboom.com
```

### UGC
```
DM @dansugcmodels on X ($3-20/video)
DM @franci__ugc on X ($10-30/video)
https://billo.app
https://insense.pro
https://arcads.ai
https://heygen.com
https://creatify.ai
https://collabstr.com
```

### NATIVE ADS
```
https://dashboard.mgid.com
https://business.taboola.com
https://my.outbrain.com
https://revcontent.com
https://content.ad
```

### AI TOOLS
```
https://elevenlabs.io
https://klingai.com
https://runwayml.com
https://invideo.io
https://leonardo.ai
https://midjourney.com
https://ideogram.ai
```

### BROWSER AUTOMATION
```
https://github.com/vercel-labs/agent-browser
https://github.com/remorses/playwriter
https://browser-use.com
https://browserbase.com
https://steel.dev
```

### AGED ACCOUNTS
```
https://accsmarket.com
https://fameswap.com
https://socialtradia.com
https://playerup.com
https://swapd.co
```

### SCHEDULING/SOCIAL MANAGEMENT
```
https://buffer.com
https://later.com
https://publer.io
https://socialbee.com
```

---

## 12. PAID ENGAGEMENT SERVICES (ALGO-SAFE HUMAN FARMS)

### Why Use Paid Engagement

- **Algorithm boost:** Initial engagement signals push content to more users
- **Social proof:** Higher numbers attract organic followers
- **Compete with big brands:** Level the playing field on new accounts
- **Kickstart growth:** Break the cold-start problem

### CRITICAL: Algo-Safe Delivery Methods

**Drip-feed is MANDATORY in 2026.** Instant delivery = instant detection.

| Delivery Type | Risk Level | How It Works |
|---------------|------------|--------------|
| **Drip-feed (3-7 days)** | LOW | Gradual delivery mimics organic growth |
| **Drip-feed (24-48 hrs)** | MEDIUM | Faster but still natural pattern |
| **Instant** | HIGH | Triggers spam detection, high drop-off |

**Never use instant delivery.** Always choose slowest option available.

### Top-Tier Engagement Services (2026)

#### Instagram

| Service | Price Range | Delivery | Retention | Best For | URL |
|---------|-------------|----------|-----------|----------|-----|
| **MediaMister** | $2-100+ | 3-4 days drip | 94%+ | Geographic targeting, businesses | mediamister.com |
| **Growthoid** | $49-99/mo | Manual/human | Very high | Organic growth, no bots | growthoid.com |
| **Famoid** | $3-50+ | API-free, safe | Good | Budget, safe delivery | famoid.com |
| **Instant Famous** | $5-100+ | Drip-feed | Good | Follower quality | instantfamous.com |
| **Stormlikes** | $2-50+ | Customizable | Moderate | Beginners, flexible | stormlikes.net |
| **Twicsy** | $3-100+ | Fast | Mixed | Long-term brand building | twicsy.com |
| **Buzzoid** | $3-100+ | Fastest | Lower | Quick social proof only | buzzoid.com |

#### TikTok

| Service | Price Range | Delivery | Retention | Best For | URL |
|---------|-------------|----------|-----------|----------|-----|
| **SocialBoosting** | $5-200+ | Gradual | High | All-around quality | socialboosting.com |
| **MediaMister** | $3-150+ | 3-4 days drip | High | Multi-platform, targeting | mediamister.com |
| **GetAFollower** | $5-100+ | Drip-feed toggle | Good | Country selection | getafollower.com |
| **Socialwick** | $3-100+ | Gradual | Good | Real users focus | socialwick.com |
| **Socialgreg** | $50-200/mo | Managed growth | Very high | Niche targeting, account manager | socialgreg.com |

#### X/Twitter

| Service | Price Range | Delivery | Retention | Best For | URL |
|---------|-------------|----------|-----------|----------|-----|
| **MediaMister** | $2-100+ | Gradual | High | Multi-platform | mediamister.com |
| **Famoid** | $3-50+ | Safe delivery | Good | Budget | famoid.com |
| **TweetAngels** | $10-200+ | Drip | Good | Twitter-focused | tweetangels.com |
| **Viralyft** | $5-100+ | Gradual | Moderate | Quick boost | viralyft.com |

### Service Selection Matrix

| Your Goal | Best Service Type | Recommended |
|-----------|-------------------|-------------|
| Long-term brand building | Managed growth (human) | Growthoid, Socialgreg |
| Geographic targeting | Country-specific | MediaMister |
| Quick social proof for launch | Fast but risky | Buzzoid (last resort) |
| Budget but safe | API-free delivery | Famoid |
| TikTok specifically | TikTok specialists | SocialBoosting |
| Multi-platform | Cross-platform provider | MediaMister |

### Algo-Safe Protocol (FOLLOW THIS)

**Before ordering:**
1. Account must be 2+ weeks old
2. Have 9+ posts already
3. Profile complete (bio, photo)
4. Some organic activity first

**Order settings:**
1. ALWAYS select drip-feed / gradual delivery
2. Choose 3-7 day delivery window
3. Start small (100-500 followers first)
4. Wait 2 weeks between orders
5. Never order more than 10-20% of current count at once

**After delivery:**
1. Continue posting normally
2. Engage with new followers
3. Don't order again for 2+ weeks
4. Monitor for action blocks

### What NOT to Do

| Bad Practice | Why It's Bad |
|--------------|--------------|
| Instant delivery | Triggers spam detection |
| 10,000 followers overnight | Obvious to algorithm and humans |
| Same service repeatedly | Pattern detection |
| Ordering during action blocks | Worsens restriction |
| Buying engagement without content | Empty account = waste of money |
| Using for sponsorship pitches | Fraud if claiming organic |

### Legal Reminder

**Legal (for algorithm boost):**
- Buying followers/engagement for your own accounts
- Using to trigger initial algorithmic exposure
- Not claiming the numbers in business pitches

**Illegal (fraud/misrepresentation):**
- Claiming bought followers as organic to get sponsorships
- Fake reviews for products (FTC banned Aug 2024)
- Screenshotting fake metrics for marketing

### Pricing Guide

**Instagram:**
- 100 followers: $2-5
- 500 followers: $8-15
- 1000 followers: $12-25
- 1000 likes: $5-15
- 100 comments: $10-30

**TikTok:**
- 100 followers: $3-6
- 1000 followers: $15-30
- 1000 views: $2-5
- 100 likes: $2-5

**X/Twitter:**
- 100 followers: $2-5
- 1000 followers: $10-20
- 100 retweets: $5-15
- 100 likes: $3-8

### Order of Operations for New Account

```
WEEK 1-2: Manual warmup only
├── Post 9-12 pieces of content
├── Engage manually 30 min/day
├── Complete profile 100%
└── Build some organic following

WEEK 3: First small order
├── Order 100-300 followers (drip 5-7 days)
├── Continue posting normally
├── Don't order anything else
└── Monitor for issues

WEEK 5: Second order (if no issues)
├── Order 300-500 more (drip 5-7 days)
├── Maybe add 500 likes spread across posts
├── Continue organic activity
└── Still posting daily

WEEK 7+: Maintenance
├── Small orders every 2-3 weeks
├── Never more than 10-20% of total
├── Mix services (don't use same one repeatedly)
└── Focus shifts to organic growth
```

---

## OPS/GROWTH FOLDER INDEX

**Path:** `OPS/growth/`

All growth-related guides are consolidated in this folder:

### Platform Playbooks
| File | Purpose |
|------|---------|
| `TWITTER_GROWTH_PLAYBOOK_2026.md` | Full X/Twitter strategy |
| `LINKEDIN_GROWTH_PLAYBOOK_2026.md` | LinkedIn organic + automation |
| `TWITTER_META_JANUARY_2026.md` | Current X algorithm meta |

### Algorithm Research
| File | Purpose |
|------|---------|
| `X_TWITTER_ALGORITHM_RESEARCH_2025.md` | X algorithm deep dive |
| `INSTAGRAM_ALGORITHM_RESEARCH_2025.md` | IG algorithm analysis |
| `LINKEDIN_ALGORITHM_RESEARCH_2025.md` | LinkedIn algorithm |
| `TIKTOK_ALGORITHM_RESEARCH_2025.md` | TikTok algorithm |
| `PINTEREST_ALGORITHM_RESEARCH_2025.md` | Pinterest algorithm |
| `X_ALGORITHM_OPTIMIZATION.md` | X optimization tactics |

### Growth Tactics
| File | Purpose |
|------|---------|
| `EDGE_GROWTH_TACTICS.md` | Grey-hat legal tactics, limits, services |
| `ENGAGEMENT_FARMING_TACTICS.md` | Reply-guy, pods, hooks, CTAs |
| `PLATFORM_AUTOMATION_LIMITS_2026.md` | Safe limits per platform |
| `NICHE_POSTING_STRATEGY.md` | Content strategy per niche |
| `GROWTH_EXPERIMENTS_FRAMEWORK.md` | A/B testing framework |

### SEO/GEO/ASO
| File | Purpose |
|------|---------|
| `SEO_GEO_ASO_TACTICS_2026.md` | Full SEO/GEO/ASO guide |
| `SEO_GEO_ASO_ACTION_PLAN_2026.md` | Action plan |
| `SEO_GEO_ASO_RESEARCH_SUMMARY_2026.md` | Research findings |
| `SEO_KEYWORD_RESEARCH_GUIDE.md` | Keyword research |
| `GTM_OPTIMIZATION_CHECKLIST.md` | GTM launch checklist |

### Conversion & Funnels
| File | Purpose |
|------|---------|
| `LANDING_PAGE_OPTIMIZATION_GUIDE.md` | Landing page best practices |
| `DM_FUNNEL_PLAYBOOK.md` | DM-based sales funnels |
| `PUSH_NOTIFICATION_STRATEGY.md` | Push notification tactics |
| `REFERRAL_PROGRAM_TEMPLATES.md` | Referral program templates |

### Other
| File | Purpose |
|------|---------|
| `PARTNERSHIP_OPPORTUNITIES.md` | Partner/collab strategies |
| `ULTIMATE_ACCOUNT_WARMUP_GUIDE.md` | Account warmup protocols |

---

## QUICK URL REFERENCE - PAID ENGAGEMENT

### Instagram Engagement
```
https://mediamister.com
https://growthoid.com
https://famoid.com
https://instantfamous.com
https://stormlikes.net
https://twicsy.com
https://buzzoid.com (fast, lower retention)
```

### TikTok Engagement
```
https://socialboosting.com
https://mediamister.com
https://getafollower.com
https://socialwick.com
https://socialgreg.com (managed growth)
```

### X/Twitter Engagement
```
https://mediamister.com
https://famoid.com
https://tweetangels.com
https://viralyft.com
```

---

**Last Updated:** 2026-01-26

**Sources:**
- [Best Social Media Engagement Tools 2026](https://ucisportfolios.pitt.edu/barirosenfeld/2025/12/21/12-best-social-media-engagement-follower-growth-tools-for-creators-2026/)
- [Best Sites to Buy TikTok Followers 2026](https://roughdraftatlanta.com/2026/01/02/buy-real-tiktok-followers/)
- [Twicsy vs Stormlikes Comparison](https://deliveredsocial.com/twicsy-vs-stormlikes-vs-views4you-is-it-legit-honest-review/)
- [Best Sites to Buy Instagram Likes 2026](https://roughdraftatlanta.com/2026/01/02/buy-real-instagram-likes/)

**Next:** Run agent to open each URL, create accounts, and prompt when payment needed.
