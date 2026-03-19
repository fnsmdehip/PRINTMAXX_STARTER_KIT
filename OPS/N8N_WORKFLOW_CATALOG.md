# N8N Workflow Catalog for PRINTMAXX

Generated: 2026-03-18 | Consumer: CEO Agent, Venture Autonomy, Agent Swarm
Auto-deploy via: `OPEN_SOURCE/agent-soul/core/workflow_bridge.py`
Pre-built JSONs: `AUTOMATIONS/n8n_workflows/`
n8n instance: `n8n.printmaxx.ai` (nginx conf at `05_AUTOMATION/scripts/n8n/nginx/n8n.conf`)

---

## Design Principle

n8n fills gaps our Python scripts cannot reach. Our scrapers, posters, and intelligence pipeline are solid. n8n's value is CONNECTORS: bridging third-party services (Stripe, Gumroad, Apollo, Hunter.io, Mailchimp, Google Sheets, Airtable, SendGrid, Telegram, Facebook Graph API) without writing custom OAuth flows and REST clients for each.

Every workflow here passes these filters:
1. Cannot be trivially done in Python with `requests` alone
2. Bridges 2+ external services requiring auth/webhooks
3. Has clear revenue or efficiency impact
4. Does not duplicate existing PRINTMAXX scripts

---

## Priority Key

| Priority | Meaning | Deploy Method |
|----------|---------|---------------|
| P0 | Immediate revenue impact, deploy today | Auto-create via workflow_bridge.py |
| P1 | High value, deploy this week | Auto-create via workflow_bridge.py |
| P2 | Nice to have, backlog | Manual import or document only |

---

## VENTURE 1: LEAD GENERATION (EAS + LOCAL_BIZ)

### W01 - Google Maps Lead Scraper + Email Enrichment [P0]
**What:** Scrapes Google Maps via Apify for business leads by category + location, extracts emails from each website with GPT-4, stores enriched leads in Airtable/Google Sheets, sends Telegram notification on completion.
**PRINTMAXX venture:** EAS (Enterprise Automation Solutions), LOCAL_BIZ
**Connection:** Cron trigger (weekday mornings), feeds into `eas_lead_pipeline.py`
**Why n8n:** Apify node handles proxy rotation and anti-bot. Google Maps API requires OAuth. Airtable node handles schema mapping. Our Python scraper does Twitter/Reddit well but lacks Google Maps + Apify integration.
**Revenue impact:** Direct pipeline for EAS $1,500-4,500 deals
**Deploy:** Auto-create. JSON at `AUTOMATIONS/n8n_workflows/w01_gmaps_lead_scraper.json`
**Setup:** Apify API key, Google Sheets or Airtable creds, OpenAI key for email extraction

### W02 - Apollo Lead Scraping + Enrichment to CRM [P0]
**What:** Scrapes Apollo.io for B2B contacts matching criteria (industry, title, company size), enriches with LinkedIn data, stores in Airtable with scoring, triggers cold outreach sequence.
**PRINTMAXX venture:** EAS, OUTBOUND
**Connection:** Webhook trigger from `eas_lead_pipeline.py`, or weekly cron
**Why n8n:** Apollo has a complex API with pagination and rate limits. n8n's Apify node + built-in pagination handle this. LinkedIn enrichment requires browser session (Phantombuster/Airtop node).
**Revenue impact:** Feeds EAS pipeline directly. 10 qualified leads/week at 5% close rate = $3,500/mo
**Deploy:** Auto-create. JSON at `AUTOMATIONS/n8n_workflows/w02_apollo_lead_enrichment.json`
**Setup:** Apollo.io API key, Airtable creds, optional Phantombuster API key

### W03 - Lead Capture + Scoring + CRM Routing [P1]
**What:** Webhook receives form submissions from PRINTMAXX landing pages, enriches with Clearbit, scores lead (company size, industry, title), routes to appropriate pipeline (EAS vs FREELANCE), sends Slack/Telegram notification for hot leads.
**PRINTMAXX venture:** EAS, FREELANCE
**Connection:** Webhook on landing page form submission
**Why n8n:** Clearbit enrichment requires API integration. Lead scoring logic + conditional routing across multiple CRMs is n8n's sweet spot. Our Python scripts don't have Clearbit/HubSpot connectors.
**Revenue impact:** Catches inbound leads from deployed sites (114 sites live)
**Deploy:** Auto-create. JSON at `AUTOMATIONS/n8n_workflows/w03_lead_capture_scoring.json`
**Setup:** Clearbit API key (free tier: 50 lookups/mo), Telegram bot token

---

## VENTURE 2: EMAIL OUTREACH

### W04 - AI Cold Email Sequence with SendGrid [P0]
**What:** Pulls leads from Google Sheets, generates personalized cold emails with Claude/GPT, sends via SendGrid (bypasses Gmail spam issues), tracks opens/clicks, auto-schedules follow-up sequence (Day 1, Day 3, Day 7), marks status in sheet.
**PRINTMAXX venture:** EAS, OUTBOUND
**Connection:** Daily cron trigger, reads from Google Sheets populated by W01/W02
**Why n8n:** SendGrid node handles deliverability, bounce tracking, open tracking natively. Multi-step email sequences with conditional waits (wait 3 days, check if opened, send follow-up) are trivial in n8n but painful in raw Python.
**Revenue impact:** Direct EAS outreach. 100 emails/day, 2% reply rate = 2 conversations/day
**Deploy:** Auto-create. JSON at `AUTOMATIONS/n8n_workflows/w04_cold_email_sendgrid.json`
**Setup:** SendGrid API key ($0 for 100 emails/day free tier), Google Sheets creds, OpenAI/Anthropic key

### W05 - Newsletter System with SendGrid + Subscriber Management [P1]
**What:** Webhook captures new subscribers from landing pages, stores in Google Sheets/Airtable, weekly cron aggregates content from RSS feeds + AI summarization, generates newsletter, sends via SendGrid with freemium rate limiting, tracks engagement.
**PRINTMAXX venture:** CONTENT, NEWSLETTER
**Connection:** Webhook for signups, weekly cron for sends
**Why n8n:** Newsletter delivery + subscriber management + engagement tracking across SendGrid requires complex API orchestration. n8n template handles unsubscribe, bounce management, open tracking.
**Revenue impact:** Newsletter = recurring audience. Monetize via affiliate links, product drops.
**Deploy:** Auto-create. JSON at `AUTOMATIONS/n8n_workflows/w05_newsletter_system.json`
**Setup:** SendGrid API key, landing page webhook integration

---

## VENTURE 3: SOCIAL MEDIA (Twitter, Facebook, TikTok)

### W06 - Multi-Platform Social Post Distributor [P1]
**What:** Reads from Google Sheets content calendar, generates platform-specific variations with AI (Twitter short, LinkedIn professional, Facebook casual), posts to all platforms, marks as posted, sends confirmation to Telegram.
**PRINTMAXX venture:** CONTENT
**Connection:** Cron trigger (3x daily matching warmup schedule)
**Why n8n:** Our `twitter_warmup_poster.py` handles Twitter. n8n extends this to LinkedIn, Facebook, Instagram simultaneously via their native nodes. Cross-posting with platform-specific formatting is n8n's strength.
**Revenue impact:** 4x content distribution with same effort. Grows audience across platforms.
**Deploy:** Manual config (requires OAuth for each platform)
**Setup:** Twitter API v2, Facebook Graph API token, LinkedIn API, Google Sheets

### W07 - Facebook Group Monitor + Engagement Bot [P1]
**What:** Monitors target Facebook groups for keyword mentions (automation, AI tools, business automation), extracts posts + sentiment analysis, identifies lead opportunities, stores in Airtable, alerts via Telegram for hot leads.
**PRINTMAXX venture:** LOCAL_BIZ, EAS, CONTENT
**Connection:** Cron trigger every 4 hours
**Why n8n:** Facebook Groups API is locked down. n8n + Airtop/Bright Data browser automation nodes bypass this. Our Python scripts have zero Facebook integration.
**Revenue impact:** EAS lead channel. Business owners asking for automation help in FB groups = warm leads.
**Deploy:** Manual config (requires Airtop or Bright Data account)
**Setup:** Airtop API key or Bright Data credentials, Airtable creds, Telegram bot

### W08 - Twitter Engagement Tracker + Analytics [P2]
**What:** Pulls engagement metrics for posted tweets (likes, replies, retweets, impressions), calculates engagement rate, identifies top-performing content formats, updates analytics sheet, triggers content strategy adjustments.
**PRINTMAXX venture:** CONTENT, Twitter
**Connection:** Daily cron, reads from posting log
**Why n8n:** Twitter Analytics API integration with Google Sheets for trend analysis. Our scraper collects OTHER accounts' tweets. This tracks OUR engagement.
**Revenue impact:** Optimizes content strategy based on data, not guessing.
**Deploy:** Manual config
**Setup:** Twitter API v2 with analytics access

---

## VENTURE 4: CONTENT PIPELINE

### W09 - Content Repurposing Factory [P0]
**What:** Takes a long-form content piece (blog post, YouTube transcript, newsletter), generates 5 Twitter posts, 1 LinkedIn post, 3 Instagram captions, 1 email newsletter section, stores all in Google Sheets with status tracking.
**PRINTMAXX venture:** CONTENT
**Connection:** Webhook trigger (called when new content is published), or manual trigger
**Why n8n:** Our `content_factory.py` generates content but lacks multi-platform formatting and storage. n8n handles the AI generation + platform-specific output + storage pipeline in one flow.
**Revenue impact:** 6x content output per piece. Compounds audience growth across platforms.
**Deploy:** Auto-create. JSON at `AUTOMATIONS/n8n_workflows/w09_content_repurposing.json`
**Setup:** OpenAI/Anthropic API key, Google Sheets creds

### W10 - RSS to Content Pipeline [P2]
**What:** Monitors RSS feeds from target blogs/newsletters, AI-summarizes new posts, generates commentary tweets and newsletter sections, queues in content calendar.
**PRINTMAXX venture:** CONTENT, NEWSLETTER
**Connection:** Cron trigger (every 6 hours)
**Why n8n:** RSS node + AI summarization + multi-output routing. Simple in n8n, would require feedparser + custom pipeline in Python.
**Revenue impact:** Consistent content without original creation effort. Content curation builds authority.
**Deploy:** Manual config
**Setup:** RSS feed URLs, OpenAI key, Google Sheets

---

## VENTURE 5: AFFILIATE MARKETING

### W11 - Amazon Affiliate Post Generator [P1]
**What:** New product link added to Google Sheets, auto-extracts ASIN, fetches product details via RapidAPI, generates review/comparison content with AI, creates social posts with affiliate links, tracks via Shlink URL shortener.
**PRINTMAXX venture:** AFFILIATE
**Connection:** Google Sheets trigger (new row), or daily cron batch
**Why n8n:** Amazon Product API + AI content gen + Shlink tracking + multi-platform posting. n8n has native nodes for all of these. Our Python scripts don't have Amazon API integration.
**Revenue impact:** Passive affiliate income. 50 product posts = potential $200-500/mo at scale.
**Deploy:** Auto-create. JSON at `AUTOMATIONS/n8n_workflows/w11_amazon_affiliate.json`
**Setup:** RapidAPI key (Amazon product data), Shlink instance, Google Sheets

### W12 - Affiliate Competitor Tracker [P2]
**What:** Monitors competitor affiliate programs twice daily via Bright Data scraping, extracts commission rates, compares to our current programs, alerts on new high-commission opportunities.
**PRINTMAXX venture:** AFFILIATE
**Connection:** Cron trigger (twice daily)
**Why n8n:** Web scraping + data comparison + alerting across multiple competitor sites. Bright Data node handles anti-bot.
**Revenue impact:** Identifies higher-commission opportunities before competitors.
**Deploy:** Manual config
**Setup:** Bright Data API key, Google Sheets

---

## VENTURE 6: REDDIT MONITORING

### W13 - Reddit Pain Point Miner with AI Analysis [P1]
**What:** Scrapes new posts from target subreddits by keyword, AI analyzes for pain points and business opportunities, scores by opportunity value, stores in Google Sheets, sends daily digest via Telegram.
**PRINTMAXX venture:** RESEARCH, EAS, CONTENT
**Connection:** Cron trigger (every 4 hours)
**Why n8n:** Our `background_reddit_scraper.py` scrapes posts but lacks AI-powered pain point analysis and opportunity scoring. n8n adds the AI analysis layer + structured output + alerting.
**Revenue impact:** Identifies EAS prospects asking for automation help. Content ideas from real problems.
**Deploy:** Auto-create. JSON at `AUTOMATIONS/n8n_workflows/w13_reddit_pain_miner.json`
**Setup:** Reddit API creds (free), OpenAI key, Google Sheets, Telegram bot

---

## VENTURE 7: PAYMENTS + PRODUCT DELIVERY

### W14 - Stripe Payment + Digital Product Delivery [P0]
**What:** Stripe webhook fires on successful payment, verifies payment, sends product download link via email (SendGrid), adds customer to newsletter list, sends seller notification via Telegram, logs sale in Google Sheets.
**PRINTMAXX venture:** MONETIZE, PRODUCT
**Connection:** Stripe webhook trigger
**Why n8n:** Stripe webhook handling + email delivery + subscriber management + logging. This is the core revenue pipeline. n8n's Stripe Trigger node handles webhook verification, retry logic, and event types natively.
**Revenue impact:** Direct revenue. Every product sale auto-fulfilled. No manual delivery.
**Deploy:** Auto-create. JSON at `AUTOMATIONS/n8n_workflows/w14_stripe_product_delivery.json`
**Setup:** Stripe API keys (requires account - human blocker P0), SendGrid API key, Telegram bot

### W15 - Gumroad Sale Notification + CRM Sync [P1]
**What:** Gumroad webhook on sale, logs customer data to Google Sheets, sends Telegram notification, adds customer email to newsletter, tracks revenue totals.
**PRINTMAXX venture:** MONETIZE, PRODUCT
**Connection:** Gumroad webhook trigger
**Why n8n:** Gumroad has limited API. n8n webhook receiver + data transformation + multi-output routing handles the full post-sale pipeline.
**Revenue impact:** Tracks all Gumroad revenue centrally. Builds customer list for upsells.
**Deploy:** Manual config (requires Gumroad account - human blocker P0)
**Setup:** Gumroad webhook URL, Google Sheets, Telegram bot

---

## VENTURE 8: SYSTEM NOTIFICATIONS + MONITORING

### W16 - Multi-Channel Error Alerter [P1]
**What:** Catches errors from ANY n8n workflow, sends formatted alert to Telegram + email with error details, workflow name, timestamp, and suggested fix.
**PRINTMAXX venture:** META/SYSTEM
**Connection:** n8n Error Trigger (fires on any workflow failure)
**Why n8n:** Native error trigger across all workflows. Single point of failure monitoring. Our Python scripts log errors to files. n8n pushes alerts to Telegram instantly.
**Revenue impact:** Prevents silent failures. Every broken workflow = lost revenue.
**Deploy:** Auto-create. JSON at `AUTOMATIONS/n8n_workflows/w16_error_alerter.json`
**Setup:** Telegram bot token, email creds

### W17 - Daily Revenue Dashboard [P2]
**What:** Daily cron pulls data from Stripe, Gumroad, Google Sheets (affiliate tracking), aggregates total revenue, sends formatted daily summary to Telegram with trends.
**PRINTMAXX venture:** META/SYSTEM
**Connection:** Daily cron (7 AM)
**Why n8n:** Aggregates from 3+ payment sources with native connectors. Our `daily_digest.py` reports system status. This reports MONEY.
**Revenue impact:** Visibility into what's working. Data-driven doubling down.
**Deploy:** Manual config
**Setup:** Stripe API, Gumroad API, Google Sheets

---

## VENTURE 9: YOUTUBE

### W18 - YouTube Video to Multi-Platform Content [P2]
**What:** Monitors YouTube channel RSS for new videos, extracts transcript via API, generates Twitter thread, LinkedIn post, newsletter section, blog summary, TikTok script. Stores all in content calendar.
**PRINTMAXX venture:** CONTENT, YouTube
**Connection:** RSS trigger on YouTube channel
**Why n8n:** YouTube transcript extraction + AI repurposing + multi-platform output. Our `ai_video_content_pipeline.py` handles video creation. This handles distribution from existing videos.
**Revenue impact:** 1 video = 6 content pieces across platforms. Compounds reach.
**Deploy:** Manual config
**Setup:** YouTube channel RSS URL, OpenAI key, Google Sheets

---

## Auto-Deploy Workflow Summary

These workflows have ready-to-import JSON files in `AUTOMATIONS/n8n_workflows/`:

| ID | Workflow | Priority | JSON File |
|----|----------|----------|-----------|
| W01 | Google Maps Lead Scraper | P0 | `w01_gmaps_lead_scraper.json` |
| W04 | Cold Email SendGrid Sequence | P0 | `w04_cold_email_sendgrid.json` |
| W09 | Content Repurposing Factory | P0 | `w09_content_repurposing.json` |
| W14 | Stripe Product Delivery | P0 | `w14_stripe_product_delivery.json` |
| W16 | Multi-Channel Error Alerter | P1 | `w16_error_alerter.json` |
| W02 | Apollo Lead Enrichment | P0 | `w02_apollo_lead_enrichment.json` |
| W13 | Reddit Pain Point Miner | P1 | `w13_reddit_pain_miner.json` |

---

## Setup Checklist (Human Required)

| Step | Time | Unblocks |
|------|------|----------|
| Stripe account + API keys | 10 min | W14, W17 |
| SendGrid free account (100 emails/day) | 5 min | W04, W05, W14 |
| Apify free account (5 actors/mo) | 5 min | W01, W02 |
| Telegram bot via @BotFather | 3 min | W13, W14, W16, W17 |
| Google Sheets API creds (service account) | 10 min | W01-W18 |
| n8n API key generation | 2 min | All workflows |
| Total | ~35 min | All P0+P1 workflows |

---

## Integration with workflow_bridge.py

Auto-deploy any pre-built workflow:

```python
import json
from pathlib import Path

# Load pre-built workflow
wf_path = Path("AUTOMATIONS/n8n_workflows/w01_gmaps_lead_scraper.json")
workflow_json = json.loads(wf_path.read_text())

# Deploy via workflow_bridge
from workflow_bridge import WorkflowManager
with WorkflowManager() as mgr:
    result = mgr.create(workflow_json)
    mgr.activate(result["id"])
    print(f"Deployed: {result['name']} (id={result['id']})")
```

Or deploy all P0 workflows at once:

```python
import json, glob
from workflow_bridge import WorkflowManager

with WorkflowManager() as mgr:
    for path in sorted(glob.glob("AUTOMATIONS/n8n_workflows/w*.json")):
        wf = json.loads(open(path).read())
        result = mgr.create(wf)
        mgr.activate(result["id"])
        print(f"[LIVE] {result['name']}")
```

---

## Sources

- [n8n Community Workflows (8,515 templates)](https://n8n.io/workflows/)
- [n8n Lead Generation Templates (562)](https://n8n.io/workflows/categories/lead-generation/)
- [n8n Social Media Templates (490)](https://n8n.io/workflows/categories/social-media/)
- [n8n Content Creation Templates (1,346)](https://n8n.io/workflows/categories/content-creation/)
- [n8n Marketing Templates (2,650)](https://n8n.io/workflows/categories/marketing/)
- [Awesome n8n Templates (280+ on GitHub)](https://github.com/enescingoz/awesome-n8n-templates)
- [n8n Workflow Templates Collection (2,053 on GitHub)](https://github.com/Danitilahun/n8n-workflow-templates)
- [Google Maps Lead Scraper Template](https://n8n.io/workflows/5743-scrape-google-maps-leads-email-phone-website-using-apify-gpt-airtable/)
- [Apollo Lead Scraping Template](https://n8n.io/workflows/9057-automate-apollo-lead-scraping-and-email-enrichment-to-airtable-crm-with-apify/)
- [Cold Email Outreach Template](https://n8n.io/workflows/2833-smart-email-outreach-sequence-ai-powered-and-customizable/)
- [SendGrid B2B Outreach Template](https://n8n.io/workflows/6039-outreach-for-your-product-using-apollo-linkedin-gpt-41-and-sendgrid/)
- [Content Repurposing Factory](https://n8n.io/workflows/6899-repurpose-youtube-videos-to-multiple-content-types-with-openrouter-ai-and-airtable/)
- [Stripe Digital Product Delivery](https://n8n.io/workflows/9063-automate-digital-product-sales-and-delivery-with-stripe-and-email/)
- [Reddit Scraping + AI Analysis](https://n8n.io/workflows/8140-automate-content-research-with-reddit-scraping-ai-analysis-and-google-sheets/)
- [Facebook Group Scraper](https://n8n.io/workflows/10370-automated-facebook-group-scraper-posts-comments-and-sub-comments-to-supabase/)
- [Amazon Affiliate Automation](https://n8n.io/workflows/7422-amazon-affiliate-marketing-automation/)
- [Multi-Channel Error Alerting](https://n8n.io/workflows/5629-multi-channel-workflow-error-alerts-with-telegram-gmail-and-messaging-apps/)
- [Newsletter System with SendGrid](https://n8n.io/workflows/11759-email-newsletter-system-with-sendgrid-google-sheets-and-freemium-rate-limiting/)
