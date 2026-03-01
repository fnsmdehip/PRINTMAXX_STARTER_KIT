# Browser Automation Setup Guide

## Current Status (Feb 2026)

Tools verified working:
- Playwright 1.51.0 (chromium, firefox, webkit installed)
- Selenium 4.33.0
- browser-use 0.1.40

## Quick Start

```bash
# Test everything works
python3 -c "from playwright.sync_api import sync_playwright; print('OK')"
python3 -c "from selenium import webdriver; print('OK')"

# Run account creator
python3 AUTOMATIONS/auto_account_creator.py --platform gumroad --email fnsmdehip@proton.me
```

## Fallback Chain

When one tool fails, automatically try the next:

1. **Playwright** (default) - best for most sites, headless support, auto-wait
2. **browser-use** - AI-powered, handles complex flows, good for CAPTCHAs
3. **Selenium** - legacy support, wider browser compat
4. **Python requests** - for API-only signups (no browser needed)
5. **Manual** - screenshot steps, flag for human

## Anti-Detection Setup

### Option 1: Playwright Stealth (Free)

```bash
pip install playwright-stealth
```

Use with `auto_account_creator.py` (already integrated):
- Random user agents
- Realistic viewport sizes
- Human-like mouse movements
- Random delays between actions

### Option 2: Anti-Detect Browsers (Paid)

| Browser | Price | Best For |
|---------|-------|----------|
| GoLogin | $49/mo (3 profiles) | Multiple account management |
| Multilogin | $99/mo (10 profiles) | Enterprise-grade fingerprinting |
| Dolphin Anty | $89/mo (10 profiles) | Social media accounts |
| AdsPower | Free (2 profiles) | Budget option |

Recommendation: Start with AdsPower free tier (2 profiles). Upgrade to GoLogin when managing 5+ accounts per platform.

### Option 3: SOAX Proxy Configuration

```python
# In auto_account_creator.py, set proxy:
PROXY_CONFIG = {
    "server": "proxy.soax.com:PORT",
    "username": "YOUR_USERNAME",
    "password": "YOUR_PASSWORD"
}
```

SOAX pricing:
- Residential: from $6.6/GB
- Mobile: from $12/GB (best for social media signups)
- ISP: from $4.2/GB (best for general use)

Setup: soax.com/dashboard -> Create sub-user -> Get credentials -> Add to SECRETS/PAYMENT_INFO.md

## Buying Warmed Accounts

### When to Buy vs Create

Buy when:
- Platform has aggressive new-account throttling (X/Twitter, Instagram)
- You need immediate posting ability (no warmup period)
- Account age matters for credibility (Reddit, forums)

Create when:
- Platform is easy to sign up (Gumroad, Buffer, Beehiiv)
- Fresh accounts work fine (Vercel, Surge.sh, npm)
- You need the account tied to your real identity (Stripe, PayPal)

### Where to Buy

| Source | Platform | Price Range | Quality |
|--------|----------|-------------|---------|
| AccsMarket.com | Twitter/X, Instagram, FB, TikTok | $2-$50/account | Mid-High |
| Fameswap.com | Instagram, YouTube, TikTok | $50-$5000 | High (real followers) |
| PlayerUp.com | Various social | $5-$100 | Mid |
| Z2U.com | Social, gaming | $1-$20 | Low-Mid |
| Appsally.com | Aged social accounts | $5-$30 | Mid |

### What to Look For

Good signs:
- Account age > 6 months
- Has posting history
- Email access included
- Phone verified
- No previous bans/strikes

Red flags:
- Too many followers for account age
- Generic/bot-like posting history
- No email access
- Recently mass-followed accounts
- Seller has low ratings

### Post-Purchase Checklist

1. Change password immediately
2. Update recovery email to yours
3. Enable 2FA with your authenticator
4. Change profile gradually (not all at once)
5. Post organically for 3-7 days before any automation
6. Match activity patterns to account's history

## Account Warming Schedule

### Week 1: Slow Start
- Day 1-2: Just browse, like 5-10 posts, follow 3-5 accounts
- Day 3-4: Make 1-2 posts, reply to 3-5 threads
- Day 5-7: Post 2-3 times, engage with 10-15 accounts

### Week 2: Build Up
- Post 3-5 times per day
- Follow 10-20 accounts per day
- Reply to 15-20 posts
- Share/repost 3-5 items

### Week 3: Normal Activity
- Post 5-10 times per day
- Full engagement schedule
- Start sharing links (gradually)
- Begin promotional content (10% of posts)

### Week 4+: Scale
- Full posting schedule active
- Automation can run at 50% speed
- Gradually increase to 100% automation
- Monitor for any throttling

### Platform-Specific Warming

**Twitter/X:**
- New accounts: 3-5 tweets/day for first week
- Bought accounts: match previous posting frequency
- Never post > 50 tweets/day (even with aged accounts)
- Engage in Spaces (boosts account health)

**Instagram:**
- New accounts: 1-2 posts/day, 10-20 stories
- Reels get more reach than static posts for new accounts
- Don't follow/unfollow more than 50/day
- Use 3-5 hashtags (not 30)

**LinkedIn:**
- New accounts: 1 post/day, 10 comments
- Connection requests: max 20/day
- Text posts outperform articles for engagement
- Don't use automation for first 2 weeks

**TikTok:**
- New accounts: post 1-3 times/day
- Watch content in your niche for 30 min before posting
- First few posts determine algorithm categorization
- Use trending sounds immediately

## Browser Automation Script

Main script: `AUTOMATIONS/auto_account_creator.py`

```bash
# Create a Gumroad account
python3 AUTOMATIONS/auto_account_creator.py --platform gumroad --email fnsmdehip@proton.me

# Create a Buffer account
python3 AUTOMATIONS/auto_account_creator.py --platform buffer --email fnsmdehip@proton.me

# Create with proxy
python3 AUTOMATIONS/auto_account_creator.py --platform gumroad --email fnsmdehip@proton.me --proxy "socks5://user:pass@proxy.soax.com:1080"

# Headful mode (see the browser)
python3 AUTOMATIONS/auto_account_creator.py --platform gumroad --email fnsmdehip@proton.me --headful

# All platforms at once
python3 AUTOMATIONS/auto_account_creator.py --all --email fnsmdehip@proton.me
```

## Security Notes

- NEVER automate payment/banking platforms (Stripe, PayPal, bank)
- NEVER store payment card numbers in automation scripts
- Use SECRETS/PAYMENT_INFO.md for credentials (gitignored)
- Rate limit all automation (2-5 second delays between actions)
- Screenshot every signup for verification
- Don't run multiple signups from same IP in < 1 hour
- Use residential proxies for social media signups (datacenter IPs get flagged)


---

## Pending Enhancement (ALPHA1418, Score: 26)

**Source:** 2026-02-13 | **URL:** r/EntrepreneurRideAlong
**Added:** 2026-02-18T06:49:18-05:00

Google ads suspended my account for misrepresenting business location Google doesnt like that my business address is different from where i actually am? I got suspended yesterday with no warning and heres the situation my LLC is in wyoming, running fb and google ads for my saas product, everything was fine for 6 months then they decide my address is not verifiable and suspended the account, $4k a 



    ---

    ## Pending Enhancement (ALPHA1505, Score: 32)

    **Source:** 2026-02-13 | **URL:** r/SaaS
    **Added:** 2026-02-18T06:49:18-05:00

    i wish someone would have told me this before building my 1st SaaS i’ve grown [my SaaS](https://aicofounder.com) to $12k/mo.

i honestly think i could’ve saved myself months of wasted effort going down the wrong paths if i truly understood this before starting.

1. validate your idea before you start building.
2. don’t chase investors. focus on getting users instead and investors will come knockin



    ---

    ## Pending Enhancement (ALPHA1510, Score: 34)

    **Source:** 2026-02-13 | **URL:** r/SaaS
    **Added:** 2026-02-18T06:49:18-05:00

    $1.7 Millions spent on YouTube Influencers. Here's what I learned. If you want to scale your marketing with influencers but dont want to burn cash on bad deals, get scammed by fake bot views, or waste months listening to "gurus" who have never actually booked a sponsorship... then you might enjoy this.

I work as a Marketing Director for a pretty big brand and I also run my own SaaS on the side. 




    ---

    ## Pending Enhancement (ALPHA1512, Score: 36)

    **Source:** 2026-02-13 | **URL:** r/SaaS
    **Added:** 2026-02-18T06:49:18-05:00

    Your saas isn't a business yet, it's just an expensive hobby. I know that's blunt, but i see it constantly in the $2k-$10k mrr range.

Founders think they've "made it" because they have pmp and a few paying users. so they go back into their cave to build "the next big feature" or refactor the backend for the 5th time.

the reality? if you can’t walk away from your keyboard for a week and still hav



    ---

    ## Pending Enhancement (ALPHA1538, Score: 22)

    **Source:** 2026-02-13 | **URL:** r/growthhacking
    **Added:** 2026-02-18T06:49:18-05:00

    I’ve hired over 1,000 influencers and spent millions. Here is the no-bs playbook. If you want to scale your marketing with influencers but dont want to burn cash on bad deals, get scammed by fake bot views, or waste months listening to "gurus" who have never actually booked a sponsorship... then you might enjoy this.

I work as a Marketing Director for a pretty big brand and I also run my own SaaS



---

## Pending Enhancement (ALPHA1643, Score: 24)

**Source:** 2026-02-13 | **URL:** r/buildinpublic
**Added:** 2026-02-18T07:12:19-05:00

I just raised $50K from an angel by practicing the pitch with an AI clone of him first. https://preview.redd.it/z02sw50jrrhg1.png?width=990&format=png&auto=webp&s=3034c92ebe21780c5f7a7d98a9ef9234608fa361

This is going to sound insane but it worked so I'm sharing.

I built a tool that creates AI clones of real people from their public info. You paste their LinkedIn, podcasts, tweets, whatever - an



---

## Pending Enhancement (ALPHA1650, Score: 22)

**Source:** 2026-02-13 | **URL:** r/micro_saas
**Added:** 2026-02-18T07:12:19-05:00

I’ve hired over 1,000 influencers and spent millions. Here is the no-bs playbook. If you want to scale your marketing with influencers but dont want to burn cash on bad deals, get scammed by fake bot views, or waste months listening to "gurus" who have never actually booked a sponsorship... then you might enjoy this.

I work as a Marketing Director for a pretty big brand and I also run my own SaaS



---

## Pending Enhancement (ALPHA1652, Score: 24)

**Source:** 2026-02-13 | **URL:** r/micro_saas
**Added:** 2026-02-18T07:12:19-05:00

I built an exportable database of 100k+ user complaints from Reddit across 500+ niches so you never have to guess what to build again i got tired of guessing what to build so i started scraping user complaints from reddit across every niche i could find

the database now has hundreds of thousands of complaints from posts and comments across 500+ niches. each one is categorized, analyzed, and broke



---

## Pending Enhancement (ALPHA1653, Score: 36)

**Source:** 2026-02-13 | **URL:** r/micro_saas
**Added:** 2026-02-18T07:12:19-05:00

Are these saas stats any good Launched my saas december 24th about 40 days ago. I've got no expenses apart from around $5 a month for server. I've done almost $600 in sales with no adds I just make posts about it on reddit and facebook.  
Since jan 24th I've had a 5% conversion rate (from users that stay for more than 2 seconds)

Really just want to know what these stats are like. Thanks.



---

## Pending Enhancement (ALPHA1663, Score: 26)

**Source:** 2026-02-13 | **URL:** r/Solopreneur
**Added:** 2026-02-18T07:12:19-05:00

I tracked how I spent 500 hours building my first product. Here's the breakdown. 3 months ago I started building my first SaaS product while studying CS full-time.

I tracked every hour. All 500+ of them.

Here's where the time actually went (and what I'd do differently).

---

## The Time Breakdown

**Total hours:** 517
**Timeline:** 3 months (while studying full-time)

**The breakdown:**

- **Co



---

## Pending Enhancement (ALPHA1665, Score: 42)

**Source:** 2026-02-13 | **URL:** r/Solopreneur
**Added:** 2026-02-18T07:12:19-05:00

How I structured my way to my first ~$5k MRR Hey everyone,



Sharing this because my current SaaS is growing fast and I see a lot of founders stuck at the same stage I was not that long ago.



After indexing the product on Google a bit over a week ago, revenue started accelerating quickly and we’re now approaching the $10k MRR mark. Nothing magical happened, just a process that finally made thin



---

## Pending Enhancement (ALPHA1670, Score: 26)

**Source:** 2026-02-13 | **URL:** r/EntrepreneurRideAlong
**Added:** 2026-02-18T07:12:19-05:00

7 months of "vibe coding" a SaaS and here's what nobody tells you Been building **Brandled** with AI and basically zero technical background. Everyone talks about how easy it is now with Claude Code, Antigravity etc.., but they leave out the part where you get completely fucked by production issues that AI can't solve.

Pure AI coding gets you maybe 60% there. You can build nice landing pages, set



---

## Pending Enhancement (ALPHA1699, Score: 40)

**Source:** 2026-02-13 | **URL:** r/AppBusiness
**Added:** 2026-02-18T07:12:19-05:00

Three years building SaaS alone. Made something so you don't have to. I've launched products multiple times. Same story every time.
Launch platforms? Need followers first. Marketplaces? Take 10% of everything. Social media? Shouting into void.
You build for months. Launch day comes. Silence.
Not because your product sucks. Because nobody knows you exist.
Every platform assumes you already made it.



---

## Pending Enhancement (ALPHA1709, Score: 26)

**Source:** 2026-02-13 | **URL:** r/startups
**Added:** 2026-02-18T07:12:19-05:00

7 months of "vibe coding" a SaaS and here's what nobody tells you (i will not promote) Been building brandled with AI and basically zero technical background. Everyone talks about how easy it is now with Claude Code, Antigravity etc.., but they leave out the part where you get completely fucked by production issues that AI can't solve.

Pure AI coding gets you maybe 60% there. You can build nice l



---

## Pending Enhancement (ALPHA1977, Score: 24)

**Source:** 2026-02-13 | **URL:** @TheShamdoo
**Added:** 2026-02-18T07:12:19-05:00

Your SaaS is leaking revenue and your dashboards won't tell you.

Parse is an AI agent that scans your entire tech stack — Stripe, HubSpot, Jira, and 40+ more — to find what you're missing.

Average finding: $150K.



---

## Pending Enhancement (ALPHA7845, Score: 32)

**Source:** r/digital_marketing (https://reddit.com/r/digital_marketing/comments/1r77omk/i_created_a_tool_to_see_who_is_really_on_my/) | **URL:** 
**Added:** 2026-02-18T07:12:19-05:00

I created a tool to see who is really on my website- Now at $2.1k a month.  There was constantly people on my website, but I never knew who. So I made clickmodus. It does a few things but mainly identifying who views my webpage. It then intent scores by analyzing which pages



---

## Pending Enhancement (ALPHA8074, Score: 24)

**Source:** r/ecommerce (https://reddit.com/r/ecommerce/comments/1r7whya/how_do_you_track_your_contribution_margin/) | **URL:** 
**Added:** 2026-02-18T07:12:19-05:00

How do you track your contribution margin?. I recently was learning a lot about contribution margin and now understood the importance it at a granular level like SKU, channel, campaign level etc. How are brands with $15-$500Mn revenue calculati



---

## Pending Enhancement (ALPHA8345, Score: 28)

**Source:** @unknown (bookmark) | **URL:** https://x.com/unknown/status/2016166731925094810
**Added:** 2026-02-18T08:39:23-05:00

I interviewed @aubreydegrey on why neither billionaires nor AI will solve aging. And why a single mouse breakthrough could be the ChatGPT moment for longevity.

0:00 - Longevity Field 20 Years On
08:58 - Are Billionaires Getting It Wrong?
17:13 - Bryan Johnson vs Peter Thiel https://t.co/OTp5pGV5eg



---

## Pending Enhancement (ALPHA8350, Score: 28)

**Source:** @unknown (bookmark) | **URL:** https://x.com/unknown/status/2022617107247382809
**Added:** 2026-02-18T08:39:23-05:00

I'm building Claude Opus 4.7 https://t.co/dSCrp0Ju1b



---

## Pending Enhancement (ALPHA8358, Score: 22)

**Source:** @unknown (bookmark) | **URL:** https://x.com/unknown/status/2022403966945149170
**Added:** 2026-02-18T08:39:23-05:00

IT'S STILL SO OVER!! These Claude Opus 4.6 one-shots are crazy.

Prompt 🏎️ 👇 https://t.co/s1QMaEKEr5



---

## Pending Enhancement (ALPHA8360, Score: 34)

**Source:** @unknown (bookmark) | **URL:** https://x.com/unknown/status/2022432102638043357
**Added:** 2026-02-18T08:39:23-05:00

want to know how to actually show up in ChatGPT, Perplexity, and Google AI Mode when someone searches for your service?

here's what most people don't understand. you can't go into ChatGPT and create a profile. there's nothing to optimize inside the platform itself.

what these



---

## Pending Enhancement (ALPHA8407, Score: 23)

**Source:** r/LocalLLaMA | **URL:** https://reddit.com/r/LocalLLaMA/comments/1r77swh/i_gave_12_llms_2000_and_a_food_truck_only_4/
**Added:** 2026-02-18T08:45:14-05:00

[r/LocalLLaMA] I gave 12 LLMs $2,000 and a food truck. Only 4 survived.



---

## Pending Enhancement (ALPHA8151, Score: 30)

**Source:** @codyschneiderxx (high-signal-accounts) | **URL:** https://x.com/codyschneiderxx/status/2023824774191837520
**Added:** 2026-02-18T08:54:05-05:00

I just had Claude Code build me a Facebook ad generator that can make 100+ on-brand ad variations in minutes for $0.

its all just code

so basically I build the template for a before after format

use claude code front end design skill

then I use Claude to find the pain points



---

## Pending Enhancement (ALPHA8157, Score: 35)

**Source:** @maverickecom (high-signal-accounts) | **URL:** https://x.com/maverickecom/status/2023965944217850115
**Added:** 2026-02-18T08:54:05-05:00

We replaced a $750K/year marketing team with 24 TikTok Shop AI Agents.

No actors.
No shoots.
No ghost creators.
No wasted samples.

Just 550+ shoppable TikTok videos per day going live on autopilot.

Here’s the exact workflow we use for 8-figure TikTok Shop brands 

Step 1 –



---

## Pending Enhancement (ALPHA8289, Score: 23)

**Source:** @jackfriks (high-signal-accounts) | **URL:** https://x.com/jackfriks/status/2023435357103247799
**Added:** 2026-02-18T08:54:13-05:00

turns out i was using minimax 2.1 instead of 2.5 and thats why i didn't believe the people who said minimax benchmarks were opus 4.6 level

still claude is more fun but this is $10/month for a 10-20% difference



---

## Pending Enhancement (ALPHA8412, Score: 20)

**Source:** @KCodes7777 (high-signal-accounts) | **URL:** https://x.com/KCodes7777/status/2023436175147409732
**Added:** 2026-02-18T08:54:24-05:00

This is insane 
This AI “people search” app is making $700,000/month.

How it works:

→ You type a name
→ It pulls public data
→ AI summarizes it

That’s it.

It’s basically a ChatGPT + Perplexity wrapper.

Why it works:

→ Viral concept
→ Emotional hook (dating,



---

## Pending Enhancement (ALPHA8204, Score: 58)

**Source:** @gregisenberg (high-signal-accounts) | **URL:** https://x.com/gregisenberg/status/2023459273590661143
**Added:** 2026-02-18T08:54:28-05:00

how to use claude code + outscraper + crawl4ai to build a profitable online directory in 4 days for under $250

1. scrape 50k–70k raw records with outscraper
2. use claude code to clean, dedupe, and structure the data in passes
3. run crawl4ai to verify live sites and filter junk

---

## Alpha Insights (Auto-Appended)

_Insights auto-appended by playbook_enhancer.py. Review and integrate as needed._

### Alpha Insight: ALPHA539 — 2026-02-28
**Source:** TechCrunch ([link](https://techcrunch.com/2025/09/29/vibe-coding-startup-anything-nabs-a-100m-valuation-after-hitting-2m-arr-in-its-first-two-weeks/))
**Category:** TOOL_ALPHA
**Method:** Vibe coding platforms validated at scale. Use Lovable/Replit for builds.
**Insight:** Vibe coding platforms: Anything $2M ARR in 2 weeks. Lovable $100M ARR in 8mo targeting $250M. Replit $150M ARR.
**Potential:** ROI: HIGHEST | Synergy: 80



---

## Pending Enhancement (ALPHA13702, Score: 30)

**Source:** r/startups (https://reddit.com/r/startups/comments/1rgipqo/startup_idea_for_receiving_commissions_quicker_i/) | **URL:** 
**Added:** 2026-02-28T06:00:01-05:00

Startup idea for receiving commissions quicker (I will not promote). TL;DR

Startup idea: A platform for commission-based workers (e.g., tech sales) to access earned commissions within 24 hours for a fee (e.g., 5% on $50k = $2,500 deduction), repaid fully upon employer

