# COMPREHENSIVE STACK COMPARISON - ALL OPTIONS

**Every tool, every alternative, every price point. Pick your stack, A/B test, optimize.**

---

## TABLE OF CONTENTS

1. [Hosting & Deployment](#1-hosting--deployment)
2. [Domains & DNS](#2-domains--dns)
3. [Email Infrastructure](#3-email-infrastructure)
4. [Cold Email Platforms](#4-cold-email-platforms)
5. [Email Warmup](#5-email-warmup)
6. [Lead Data](#6-lead-data)
7. [Email Verification](#7-email-verification)
8. [Proxies](#8-proxies)
9. [Phone Verification](#9-phone-verification)
10. [LinkedIn Automation](#10-linkedin-automation)
11. [App Monetization](#11-app-monetization)
12. [Payment Processing](#12-payment-processing)
13. [Newsletter Platforms](#13-newsletter-platforms)
14. [Community Platforms](#14-community-platforms)
15. [AI Voice](#15-ai-voice)
16. [AI Video](#16-ai-video)
17. [AI Images](#17-ai-images)
18. [Automation](#18-automation)
19. [Social Scheduling](#19-social-scheduling)
20. [Anti-Detect Browsers](#20-anti-detect-browsers)
21. [Scraping](#21-scraping)
22. [CRM](#22-crm)
23. [Analytics](#23-analytics)
24. [Recommended Stacks](#24-recommended-stacks)

---

## 1. HOSTING & DEPLOYMENT

### VPS Providers

| Provider | Basic | Good | Location | Best For | URL |
|----------|-------|------|----------|----------|-----|
| **Hetzner** | $4/mo (2GB) | $7/mo (4GB) | EU (DE/FI) | Cheapest, self-host | https://hetzner.com |
| **DigitalOcean** | $6/mo (1GB) | $12/mo (2GB) | US/EU/Asia | Beginner friendly | https://digitalocean.com |
| **Vultr** | $5/mo (1GB) | $10/mo (2GB) | Global | Good middle ground | https://vultr.com |
| **Linode** | $5/mo (1GB) | $10/mo (2GB) | Global | Reliable | https://linode.com |
| **AWS Lightsail** | $3.50/mo | $5/mo | Global | AWS ecosystem | https://lightsail.aws.amazon.com |
| **Contabo** | $6/mo (8GB!) | $12/mo (16GB) | EU/US | Most RAM per $ | https://contabo.com |

**Winner:** Hetzner (40% cheaper than DO, same quality)

### Serverless/Edge

| Provider | Free Tier | Paid | Best For | URL |
|----------|-----------|------|----------|-----|
| **Vercel** | 100GB/mo | $20/mo | Next.js, frontend | https://vercel.com |
| **Cloudflare Pages** | Unlimited | Free | Static sites | https://pages.cloudflare.com |
| **Netlify** | 100GB/mo | $19/mo | JAMstack | https://netlify.com |
| **Railway** | $5 credit | Usage | Full-stack apps | https://railway.app |
| **Render** | Static free | $7/mo | Docker apps | https://render.com |
| **Fly.io** | 3 VMs free | Usage | Edge compute | https://fly.io |

**Winner:** Vercel for frontend, Hetzner for backend

### Self-Hosting Tools

| Tool | Cost | Use Case | URL |
|------|------|----------|-----|
| **Dokploy** | Free | One-click deploys on VPS | https://dokploy.com |
| **Coolify** | Free | Self-hosted Vercel | https://coolify.io |
| **CapRover** | Free | PaaS on your VPS | https://caprover.com |
| **Portainer** | Free | Docker management | https://portainer.io |

**Recommended:** Hetzner + Dokploy = $5/mo for everything

---

## 2. DOMAINS & DNS

### Domain Registrars

| Registrar | .com Price | Privacy | Best For | URL |
|-----------|------------|---------|----------|-----|
| **Porkbun** | $9.73/yr | Free | Cheapest | https://porkbun.com |
| **Namecheap** | $10.28/yr | Free | Popular | https://namecheap.com |
| **Cloudflare** | $9.15/yr | Free | At-cost pricing | https://cloudflare.com/registrar |
| **Google Domains** | $12/yr | Free | Simple | https://domains.google |
| **GoDaddy** | $12.99/yr | $10/yr | Avoid | https://godaddy.com |
| **Dynadot** | $9.99/yr | Free | Bulk buying | https://dynadot.com |

**Winner:** Porkbun or Cloudflare (cheapest)

### DNS Providers

| Provider | Free Tier | Paid | Best For | URL |
|----------|-----------|------|----------|-----|
| **Cloudflare** | Unlimited | Pro $20/mo | Everything | https://cloudflare.com |
| **Route53** | No | $0.50/zone | AWS users | https://aws.amazon.com/route53 |
| **DNSimple** | No | $5/mo | Developers | https://dnsimple.com |

**Winner:** Cloudflare (free, fast, security)

---

## 3. EMAIL INFRASTRUCTURE

### Email Providers (For Cold Email Domains)

| Provider | Cost/User | Inboxes | Deliverability | URL |
|----------|-----------|---------|----------------|-----|
| **Google Workspace** | $6/mo | Unlimited aliases | Best | https://workspace.google.com |
| **Microsoft 365** | $6/mo | Unlimited aliases | Very Good | https://microsoft.com/microsoft-365 |
| **Zoho Mail** | $1/mo | 5GB | Good | https://zoho.com/mail |
| **ProtonMail** | $4/mo | Limited | Good (privacy) | https://proton.me |
| **Fastmail** | $5/mo | 30GB | Good | https://fastmail.com |
| **ImprovMX** | Free | Forwarding only | N/A | https://improvmx.com |

**Winner:** Google Workspace (best deliverability)

### Pre-Warmed Inbox Services (Skip DIY Warmup)

| Service | Cost | What You Get | URL |
|---------|------|--------------|-----|
| **DeliverOn** | $49/mo/inbox | Pre-warmed sending infrastructure | https://deliveron.org |
| **Mailforge** | $3/inbox | Bulk warm inboxes | https://mailforge.ai |
| **Mailscale** | $39/mo | Pre-built email infrastructure | https://mailscale.com |
| **Inframail** | $99/mo | Done-for-you inboxes | https://inframail.io |

**A/B Test:** DIY warmup ($6/inbox) vs DeliverOn ($49/inbox) - tradeoff is time vs money

---

## 4. COLD EMAIL PLATFORMS

### Tier 1: All-in-One (Warmup + Sending)

| Tool | Price | Inboxes | Best For | URL |
|------|-------|---------|----------|-----|
| **Instantly.ai** | $37-97/mo | Unlimited | Beginners, good UI | https://instantly.ai |
| **Smartlead** | $39-94/mo | Unlimited | Scale, analytics | https://smartlead.ai |
| **Emailbison** | $39-149/mo | Unlimited | Budget, API | https://emailbison.com |
| **Lemlist** | $59-99/mo | 3 inboxes | Personalization | https://lemlist.com |
| **Woodpecker** | $49-89/mo | 2 inboxes | SMBs | https://woodpecker.co |
| **Reply.io** | $60-90/mo | 1 inbox | Multichannel | https://reply.io |
| **QuickMail** | $49/mo | 5 inboxes | Teams | https://quickmail.io |

### Tier 2: Budget Options

| Tool | Price | Best For | URL |
|------|-------|----------|-----|
| **Gmass** | $25/mo | Gmail native | https://gmass.co |
| **Mailmeteor** | $10/mo | Google Sheets | https://mailmeteor.com |
| **Yesware** | $15/mo | Tracking only | https://yesware.com |
| **Mixmax** | $29/mo | Gmail sequences | https://mixmax.com |

**Winner:** Instantly (beginners) or Smartlead (scale)

---

## 5. EMAIL WARMUP

### Standalone Warmup

| Tool | Price | Network | URL |
|------|-------|---------|-----|
| **Warmbox.ai** | $19/mo | 35k+ inboxes | https://warmbox.ai |
| **Mailwarm** | $79/mo | 1000+ inboxes | https://mailwarm.com |
| **Lemwarm** | $29/mo | Lemlist network | https://lemwarm.com |
| **Warmup Inbox** | $9/mo | Smaller | https://warmupinbox.com |
| **Mailivery** | $25/mo | Growing | https://mailivery.io |
| **Folderly** | $49/mo | Premium | https://folderly.com |

**Recommendation:** Use built-in warmup from your cold email tool first

---

## 6. LEAD DATA

### B2B Contact Databases

| Tool | Free Tier | Paid | Database | URL |
|------|-----------|------|----------|-----|
| **Apollo.io** | 600 credits/mo | $49-79/mo | 275M+ | https://apollo.io |
| **Hunter.io** | 25/mo | $49/mo | Domain search | https://hunter.io |
| **Lusha** | 5/mo | $36/mo | 100M+ | https://lusha.com |
| **RocketReach** | 5/mo | $53/mo | 700M+ | https://rocketreach.co |
| **Snov.io** | 50/mo | $39/mo | 100M+ | https://snov.io |
| **Kaspr** | 10/mo | $49/mo | LinkedIn focus | https://kaspr.io |
| **Clearbit** | 100/mo | Custom | Premium | https://clearbit.com |
| **ZoomInfo** | No | $15k+/yr | Enterprise | https://zoominfo.com |
| **Seamless.ai** | Trial | $147/mo | Real-time | https://seamless.ai |
| **Lead411** | Trial | $99/mo | Intent data | https://lead411.com |

**Winner:** Apollo.io (best free tier + paid value)

### Intent/Trigger Data

| Tool | Price | Data Type | URL |
|------|-------|-----------|-----|
| **Crunchbase** | Free-$49/mo | Funding, hiring | https://crunchbase.com |
| **BuiltWith** | $299/mo | Tech stack | https://builtwith.com |
| **G2** | Free | Review intent | https://g2.com |
| **SimilarWeb** | Free-$199/mo | Traffic data | https://similarweb.com |

---

## 7. EMAIL VERIFICATION

| Tool | Price | Speed | Accuracy | URL |
|------|-------|-------|----------|-----|
| **ZeroBounce** | $16/1k | Fast | 99%+ | https://zerobounce.net |
| **NeverBounce** | $8/1k | Fast | 98%+ | https://neverbounce.com |
| **Clearout** | $7/1k | Fast | 98% | https://clearout.io |
| **Debounce** | $10/1k | Medium | 98% | https://debounce.io |
| **Emailable** | $8/1k | Fast | 98% | https://emailable.com |
| **Bouncer** | $8/1k | Fast | 97% | https://usebouncer.com |
| **MillionVerifier** | $37/10k | Fast | 99% | https://millionverifier.com |

**Winner:** Clearout or NeverBounce (best value)

---

## 8. PROXIES

### Residential Proxies

| Provider | Min Price | Pool Size | Best For | URL |
|----------|-----------|-----------|----------|-----|
| **Soax** | $6.60/GB | 8.5M+ | Budget, clean | https://soax.com |
| **Decodo/Smartproxy** | $12.50/GB | 55M+ | Scale, social | https://smartproxy.com |
| **IPRoyal** | $7/GB | 2M+ | Budget | https://iproyal.com |
| **Bright Data** | $15/GB | 72M+ | Enterprise | https://brightdata.com |
| **Oxylabs** | $15/GB | 100M+ | Enterprise | https://oxylabs.io |
| **Webshare** | $5/GB | 30M+ | Super budget | https://webshare.io |
| **PacketStream** | $1/GB | P2P | Risky/cheap | https://packetstream.io |

### Mobile Proxies (Premium - For Main Accounts)

| Provider | Price | Type | URL |
|----------|-------|------|-----|
| **Soax Mobile** | $150/mo | Rotating | https://soax.com |
| **Smartproxy Mobile** | $200/mo | Rotating | https://smartproxy.com |
| **Proxy-Seller** | $90/mo | Dedicated | https://proxy-seller.com |
| **AirProxy** | $100/mo | Dedicated | https://airproxy.io |
| **The Social Proxy** | $90/mo | Dedicated | https://thesocialproxy.com |
| **ProxyGuys** | $100/mo | Dedicated | https://proxyguys.com |

### ISP Proxies (Middle Ground)

| Provider | Price | URL |
|----------|-------|-----|
| **Bright Data ISP** | $17/GB | https://brightdata.com |
| **Smartproxy ISP** | $14/mo (2GB) | https://smartproxy.com |
| **IPRoyal ISP** | $2.50/IP | https://iproyal.com |

**Winner:** Soax (budget) → Decodo (scale)

---

## 9. PHONE VERIFICATION

| Service | Price/SMS | Best For | URL |
|---------|-----------|----------|-----|
| **SMSPool** | $0.10-0.50 | Cheapest | https://smspool.net |
| **5sim** | $0.05-0.50 | Budget | https://5sim.net |
| **TextVerified** | $0.50-2.00 | US numbers | https://textverified.com |
| **OnlineSIM** | $0.10-0.50 | Global | https://onlinesim.io |
| **SMS-Activate** | $0.05-0.50 | Bulk | https://sms-activate.org |
| **SMSPVA** | $0.10-0.30 | Variety | https://smspva.com |

**Winner:** SMSPool (cheap + reliable)

---

## 10. LINKEDIN AUTOMATION

| Tool | Price | Type | Safety | URL |
|------|-------|------|--------|-----|
| **Expandi** | $99/mo | Cloud | Safest | https://expandi.io |
| **Dripify** | $59/mo | Cloud | Safe | https://dripify.io |
| **Waalaxy** | Free-$80/mo | Cloud | Good | https://waalaxy.com |
| **Dux-Soup** | $15-55/mo | Extension | Medium | https://dux-soup.com |
| **Phantombuster** | $30-100/mo | Cloud | Medium | https://phantombuster.com |
| **Zopto** | $215/mo | Cloud | Enterprise | https://zopto.com |
| **LinkedHelper** | $15-45/mo | Desktop | Risky | https://linkedhelper.com |
| **Salesflow** | $99/mo | Cloud | Safe | https://salesflow.io |
| **Closely** | $59/mo | Cloud | Good | https://closelyhq.com |
| **MeetAlfred** | $59/mo | Cloud | Good | https://meetalfred.com |

**Winner:** Expandi (safest) or Waalaxy (free tier)

---

## 11. APP MONETIZATION

### Subscription Management

| Tool | Price | Best For | URL |
|------|-------|----------|-----|
| **RevenueCat** | Free-$99/mo | Best overall | https://revenuecat.com |
| **Adapty** | Free-$99/mo | A/B testing | https://adapty.io |
| **Superwall** | Free-$99/mo | Paywalls | https://superwall.com |
| **Qonversion** | Free-$99/mo | Analytics | https://qonversion.io |
| **Glassfy** | Free-$29/mo | Budget | https://glassfy.io |
| **Purchasely** | Custom | Enterprise | https://purchasely.com |

**Winner:** RevenueCat (industry standard)

---

## 12. PAYMENT PROCESSING

### General Payments

| Provider | Fee | Best For | URL |
|----------|-----|----------|-----|
| **Stripe** | 2.9% + $0.30 | Standard | https://stripe.com |
| **Paddle** | 5% + $0.50 | MoR (handles tax) | https://paddle.com |
| **Lemon Squeezy** | 5% + $0.50 | Digital products | https://lemonsqueezy.com |
| **Gumroad** | 10% | Simplest | https://gumroad.com |
| **PayPal** | 2.9% + $0.30 | Legacy | https://paypal.com |
| **Wise** | 0.5-1% | International | https://wise.com |

**Winner:** Stripe (lowest fees) or Lemon Squeezy (handles everything)

---

## 13. NEWSLETTER PLATFORMS

| Platform | Free Tier | Paid | Best For | URL |
|----------|-----------|------|----------|-----|
| **Beehiiv** | 2,500 subs | $49/mo | Growth tools | https://beehiiv.com |
| **Substack** | Unlimited | 10% of paid | Writers | https://substack.com |
| **ConvertKit** | 1,000 subs | $29/mo | Creators | https://convertkit.com |
| **Mailchimp** | 500 subs | $13/mo | SMBs | https://mailchimp.com |
| **Buttondown** | 100 subs | $9/mo | Simple | https://buttondown.email |
| **Ghost** | Self-host | $9-25/mo | Publishing | https://ghost.org |
| **Revue** | Deprecated | - | Avoid | - |

**Winner:** Beehiiv (best growth tools) or Substack (simplest)

---

## 14. COMMUNITY PLATFORMS

| Platform | Price | Best For | URL |
|----------|-------|----------|-----|
| **Skool** | $99/mo | Courses + community | https://skool.com |
| **Circle** | $39-99/mo | Premium communities | https://circle.so |
| **Discord** | Free | Gaming/tech | https://discord.com |
| **Slack** | Free-$8/user | Teams | https://slack.com |
| **Whop** | Free + fees | Digital products | https://whop.com |
| **Mighty Networks** | $39-99/mo | Full platform | https://mightynetworks.com |
| **Telegram** | Free | Crypto/anon | https://telegram.org |
| **Geneva** | Free | Events | https://geneva.com |

**Winner:** Skool (all-in-one) or Discord (free)

---

## 15. AI VOICE

| Tool | Free Tier | Paid | Quality | URL |
|------|-----------|------|---------|-----|
| **ElevenLabs** | 10k chars/mo | $5-22/mo | Best | https://elevenlabs.io |
| **Play.ht** | Trial | $31/mo | Very Good | https://play.ht |
| **Murf.ai** | 10 mins | $29/mo | Good | https://murf.ai |
| **WellSaid** | Trial | $49/mo | Professional | https://wellsaidlabs.com |
| **Resemble.ai** | Trial | $24/mo | Cloning | https://resemble.ai |
| **Descript** | 1 hr/mo | $12/mo | Overdub | https://descript.com |
| **Uberduck** | Limited | $10/mo | Fun voices | https://uberduck.ai |
| **Speechify** | Limited | $139/yr | Reading | https://speechify.com |

**Winner:** ElevenLabs (best quality, MCP integration)

---

## 16. AI VIDEO

| Tool | Free Tier | Paid | Best For | URL |
|------|-----------|------|----------|-----|
| **Kling** | 66 credits/day | $5-30/mo | Longer clips | https://klingai.com |
| **Runway** | Trial | $15-95/mo | Established | https://runwayml.com |
| **Pika** | 250 credits | $8-35/mo | Stylized | https://pika.art |
| **Luma Dream Machine** | 30 gens/mo | $24-96/mo | Fast | https://lumalabs.ai |
| **Veo (Google)** | Waitlist | TBD | Best quality | https://deepmind.google/veo |
| **Sora (OpenAI)** | Waitlist | TBD | Hype | https://openai.com/sora |
| **HeyGen** | Trial | $24-120/mo | Avatars | https://heygen.com |
| **Synthesia** | Trial | $30-90/mo | Professional | https://synthesia.io |
| **D-ID** | Trial | $5.99-108/mo | Talking heads | https://d-id.com |

### Faceless Video Tools

| Tool | Price | Best For | URL |
|------|-------|----------|-----|
| **InVideo AI** | $25-60/mo | Full automation | https://invideo.io |
| **Pictory** | $23-47/mo | Blog to video | https://pictory.ai |
| **Fliki** | $28-88/mo | Quick shorts | https://fliki.ai |
| **Opus Clip** | $15-100/mo | Long to short | https://opus.pro |
| **Vizard** | $25-60/mo | Repurposing | https://vizard.ai |

**Winner:** Kling (value) or InVideo AI (faceless automation)

---

## 17. AI IMAGES

| Tool | Free Tier | Paid | Best For | URL |
|------|-----------|------|----------|-----|
| **Midjourney** | No | $10-60/mo | Best quality | https://midjourney.com |
| **Leonardo.ai** | 150/day | $12-24/mo | Free tier | https://leonardo.ai |
| **Ideogram** | 25/day | $7-20/mo | Text in images | https://ideogram.ai |
| **DALL-E 3** | ChatGPT Plus | $20/mo | Integrated | https://openai.com |
| **Stable Diffusion** | Free (local) | $10/mo (API) | Open source | https://stability.ai |
| **Adobe Firefly** | 25/mo | $5/mo | Commercial | https://firefly.adobe.com |
| **Canva AI** | Limited | $13/mo | Design | https://canva.com |
| **Flux** | Free (local) | API | Open source | https://blackforestlabs.ai |

**Winner:** Leonardo.ai (free tier) or Midjourney (quality)

---

## 18. AUTOMATION

| Tool | Free Tier | Paid | Best For | URL |
|------|-----------|------|----------|-----|
| **n8n** | Self-host | $20/mo cloud | Developers | https://n8n.io |
| **Make** | 1k ops | $9-16/mo | Visual | https://make.com |
| **Zapier** | 100 tasks | $20-100/mo | Simplest | https://zapier.com |
| **Pipedream** | 10k/mo | $19/mo | Developers | https://pipedream.com |
| **Activepieces** | Self-host | $0 | Open source | https://activepieces.com |
| **Windmill** | Self-host | $10/mo | Scripts | https://windmill.dev |

**Winner:** n8n self-hosted on Hetzner ($4/mo total)

---

## 19. SOCIAL SCHEDULING

| Tool | Free Tier | Paid | Platforms | URL |
|------|-----------|------|-----------|-----|
| **Buffer** | 3 channels | $6-120/mo | All | https://buffer.com |
| **Hypefury** | Trial | $19-49/mo | X focused | https://hypefury.com |
| **Publer** | 3 accounts | $12-28/mo | All | https://publer.io |
| **Later** | 1 profile | $25-80/mo | Visual | https://later.com |
| **Hootsuite** | No | $99/mo | Enterprise | https://hootsuite.com |
| **Metricool** | 1 account | $18-45/mo | All | https://metricool.com |
| **Typefully** | Limited | $15-39/mo | X/LinkedIn | https://typefully.com |
| **SocialBee** | Trial | $29-99/mo | All | https://socialbee.com |

**Winner:** Hypefury (X) or Buffer (multi-platform)

---

## 20. ANTI-DETECT BROWSERS

| Tool | Free Tier | Paid | Profiles | URL |
|------|-----------|------|----------|-----|
| **GoLogin** | 3 profiles | $49-99/mo | 100-300 | https://gologin.com |
| **Multilogin** | No | $99-199/mo | 100-300 | https://multilogin.com |
| **Incogniton** | 10 profiles | $30-150/mo | 50-500 | https://incogniton.com |
| **Dolphin Anty** | 10 profiles | $89-159/mo | 100-300 | https://dolphin-anty.com |
| **AdsPower** | 2 profiles | $9-50/mo | 10-100 | https://adspower.com |
| **Kameleo** | Trial | $59-199/mo | Unlimited | https://kameleo.io |

**Winner:** GoLogin (best free tier) or Multilogin (enterprise)

---

## 21. SCRAPING

| Tool | Free Tier | Paid | Best For | URL |
|------|-----------|------|----------|-----|
| **Apify** | $5/mo | $49-499/mo | Pre-built scrapers | https://apify.com |
| **Phantombuster** | 14-day trial | $69-439/mo | Social | https://phantombuster.com |
| **Octoparse** | 14-day trial | $99-249/mo | No-code | https://octoparse.com |
| **Scrapy** | Free | $0 | Developers | https://scrapy.org |
| **Playwright** | Free | $0 | Developers | https://playwright.dev |
| **Browse.ai** | 50 tasks | $49-249/mo | No-code | https://browse.ai |
| **Diffbot** | Trial | $299/mo | AI extraction | https://diffbot.com |

**Winner:** Playwright (free + powerful) or Apify (pre-built)

---

## 22. CRM

| Tool | Free Tier | Paid | Best For | URL |
|------|-----------|------|----------|-----|
| **HubSpot** | Unlimited contacts | $20-800/mo | Full suite | https://hubspot.com |
| **Pipedrive** | Trial | $15-99/mo | Sales focused | https://pipedrive.com |
| **Close** | Trial | $49-139/mo | Cold outreach | https://close.com |
| **Folk** | Free | $20-40/mo | Lightweight | https://folk.app |
| **Attio** | Free | $34-79/mo | Modern | https://attio.com |
| **Notion** | Free | $10/mo | DIY CRM | https://notion.so |
| **Airtable** | Free | $20/mo | Spreadsheet CRM | https://airtable.com |

**Winner:** HubSpot free tier or Notion (DIY)

---

## 23. ANALYTICS

| Tool | Free Tier | Paid | Best For | URL |
|------|-----------|------|----------|-----|
| **Plausible** | Trial | $9/mo | Privacy-first | https://plausible.io |
| **Fathom** | Trial | $14/mo | Simple | https://usefathom.com |
| **PostHog** | 1M events | $0 self-host | Product analytics | https://posthog.com |
| **Mixpanel** | 20M events | $25/mo | Events | https://mixpanel.com |
| **Amplitude** | 10M events | Custom | Product | https://amplitude.com |
| **Google Analytics** | Free | $0 | Standard | https://analytics.google.com |
| **Umami** | Self-host | $9/mo cloud | Privacy | https://umami.is |

**Winner:** Plausible (simple) or PostHog self-hosted (free)

---

## 24. RECOMMENDED STACKS

### BOOTSTRAP STACK (~$150/mo)

```
Hosting:      Hetzner VPS ($5) + Vercel free
Domains:      Porkbun ($40/yr total)
DNS:          Cloudflare (free)
Email:        Google Workspace 3 inboxes ($18)
Cold Email:   Emailbison ($39)
Lead Data:    Apollo free tier
Verification: Clearout ($7/1k as needed)
Warmup:       Built-in
Proxies:      Soax 5GB ($33)
Phone:        SMSPool ($10)
Voice:        ElevenLabs free tier
Scheduling:   Buffer free
Automation:   n8n self-hosted (free)
Payments:     Stripe (2.9%)
Analytics:    Plausible ($9)

TOTAL: ~$115-150/mo
```

### STANDARD STACK (~$350/mo)

```
Hosting:      Hetzner ($7) + Vercel Pro ($20)
Domains:      Cloudflare ($50/yr)
DNS:          Cloudflare (free)
Email:        Google Workspace 6 inboxes ($36)
Cold Email:   Instantly ($97)
Lead Data:    Apollo Pro ($79)
Verification: ZeroBounce ($16/1k)
Warmup:       Built-in
Proxies:      Soax 10GB ($66) + Decodo 5GB ($62)
Phone:        SMSPool ($20)
Voice:        ElevenLabs Creator ($22)
Scheduling:   Hypefury ($29)
Automation:   n8n self-hosted
Payments:     Stripe
LinkedIn:     Waalaxy free
CRM:          HubSpot free
Analytics:    PostHog self-hosted

TOTAL: ~$350-400/mo
```

### SCALE STACK (~$700/mo)

```
Hosting:      Hetzner ($15) + Vercel Team ($50)
Email:        Google Workspace 12 inboxes ($72)
Cold Email:   Smartlead ($94) + Instantly ($97)
Lead Data:    Apollo + RocketReach ($130)
Verification: NeverBounce bulk
Deliverability: GlockApps ($59)
Proxies:      Decodo 20GB ($200) + 2x Mobile ($180)
Voice:        ElevenLabs Pro ($22)
Video:        InVideo AI ($60)
Scheduling:   Hypefury ($49)
LinkedIn:     Expandi ($99)
CRM:          HubSpot Starter ($20)
Analytics:    Mixpanel ($25)

TOTAL: ~$700-900/mo
```

### A/B TEST STACK (Compare Tools)

Test these head-to-head for 30 days:
```
Cold Email:   Instantly vs Smartlead vs Emailbison
Proxies:      Soax vs Decodo
Voice:        ElevenLabs vs Play.ht
Video:        Kling vs InVideo AI
Lead Data:    Apollo vs Hunter
LinkedIn:     Expandi vs Waalaxy
Scheduling:   Hypefury vs Buffer vs Typefully
```

---

## QUICK REFERENCE: ALL URLs

### TIER 1 - BLOCKING
```
https://developer.apple.com/programs/enroll/
https://play.google.com/console/signup
```

### HOSTING
```
https://hetzner.com
https://digitalocean.com
https://vercel.com
https://cloudflare.com
```

### DOMAINS
```
https://porkbun.com
https://namecheap.com
https://cloudflare.com/registrar
```

### EMAIL INFRASTRUCTURE
```
https://workspace.google.com
https://deliveron.org
https://mailforge.ai
```

### COLD EMAIL
```
https://instantly.ai
https://smartlead.ai
https://emailbison.com
https://lemlist.com
```

### LEAD DATA
```
https://apollo.io
https://hunter.io
https://lusha.com
https://rocketreach.co
```

### VERIFICATION
```
https://zerobounce.net
https://neverbounce.com
https://clearout.io
```

### PROXIES
```
https://soax.com
https://smartproxy.com
https://iproyal.com
https://brightdata.com
```

### PHONE VERIFICATION
```
https://smspool.net
https://5sim.net
https://textverified.com
```

### LINKEDIN
```
https://linkedin.com/sales/
https://expandi.io
https://dripify.io
https://waalaxy.com
```

### APP MONETIZATION
```
https://revenuecat.com
https://adapty.io
https://superwall.com
```

### PAYMENTS
```
https://stripe.com
https://paddle.com
https://lemonsqueezy.com
https://gumroad.com
```

### NEWSLETTER
```
https://beehiiv.com
https://substack.com
https://convertkit.com
```

### COMMUNITY
```
https://skool.com
https://whop.com
https://circle.so
https://discord.com
```

### AI VOICE
```
https://elevenlabs.io
https://play.ht
https://murf.ai
```

### AI VIDEO
```
https://klingai.com
https://runwayml.com
https://invideo.io
https://heygen.com
```

### AI IMAGES
```
https://leonardo.ai
https://midjourney.com
https://ideogram.ai
```

### AUTOMATION
```
https://n8n.io
https://make.com
https://zapier.com
```

### SCHEDULING
```
https://hypefury.com
https://buffer.com
https://publer.io
```

### ANTI-DETECT
```
https://gologin.com
https://multilogin.com
```

### SCRAPING
```
https://apify.com
https://phantombuster.com
https://playwright.dev
```

### CRM
```
https://hubspot.com
https://pipedrive.com
https://notion.so
```

### ANALYTICS
```
https://plausible.io
https://posthog.com
https://mixpanel.com
```

---

**Last Updated:** 2026-01-26

**This is the comprehensive reference. Pick your stack, sign up, A/B test, optimize.**
