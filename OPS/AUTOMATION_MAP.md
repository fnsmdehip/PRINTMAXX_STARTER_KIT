# PRINTMAXX Automation Map

**Every task across every function, mapped by automation status, priority, and integration.**

Related docs:
- `OPS/automation/MASTER_AUTOMATION_PLAN.md` - Tech stack and anti-ban strategies
- `OPS/automation/AUTOMATION_WORKFLOWS_GUIDE.md` - n8n vs Make.com decision matrix
- `OPS/automation/AUTONOMOUS_TASKS.md` - What can run unattended
- `OPS/DAILY_AUTOMATED_TASKS.md` - Daily automated schedule
- `OPS/VA_TASK_SOPS.md` - VA delegation procedures

---

## Section A: Current automation status

### Content creation and posting

| Task | Current Status | Tool Used | Could Be Automated? | Priority |
|------|---------------|-----------|---------------------|----------|
| Blog post writing | Manual | Claude (Sonnet/Opus) | Semi-auto (AI drafts, human edits) | Medium |
| Social post copywriting | Manual | Claude | Semi-auto (batch generate, human review) | High |
| Image creation for posts | Manual | Canva / Midjourney / Leonardo.ai | Semi-auto (template-based auto-gen) | Medium |
| Video script writing | Manual | Claude | Semi-auto (AI drafts) | Low |
| Content repurposing (1 to 5+) | Manual | Google Docs | Semi-auto (n8n flow: input source, output variants) | High |
| Post scheduling (X) | Semi-auto | Buffer | Fully auto (Buffer API or Hypefury) | High |
| Post scheduling (IG) | Semi-auto | Buffer | Fully auto (Buffer API or Later) | High |
| Post scheduling (TikTok) | Manual | Native app | Semi-auto (Buffer or TikTok API) | Medium |
| Post scheduling (LinkedIn) | Semi-auto | Buffer | Fully auto (Buffer API) | Medium |
| Newsletter drafting | Manual | Google Docs | Semi-auto (AI draft + curated links) | Medium |
| Newsletter sending | Semi-auto | Beehiiv | Fully auto (Beehiiv schedule) | High |
| Content calendar management | Manual | Google Sheets | Semi-auto (n8n auto-populates from content queue) | Medium |
| Hashtag research | Manual | RiteTag + native search | Semi-auto (scraper + trending API) | Low |
| Comment engagement | Manual | Native apps | Manual (authenticity required) | N/A |
| Content QA review | Manual | Human review | Manual (quality gate) | N/A |

### Lead generation

| Task | Current Status | Tool Used | Could Be Automated? | Priority |
|------|---------------|-----------|---------------------|----------|
| Cold email list building | Manual | Apollo.io | Semi-auto (Apollo API + filters) | High |
| Email verification | Semi-auto | Apollo / Hunter | Fully auto (API-based verification) | High |
| Cold email sending | Not started | Instantly.ai (planned) | Fully auto (Instantly handles sequences) | Critical |
| Cold email warmup | Not started | Instantly.ai (planned) | Fully auto (Instantly auto-warms) | Critical |
| Follow-up sequences | Not started | Instantly.ai (planned) | Fully auto (automated drip) | Critical |
| LinkedIn connection requests | Manual | LinkedIn native | Semi-auto (Expandi or Dripify, use with caution) | Medium |
| LinkedIn messaging | Manual | LinkedIn native | Semi-auto (Expandi sequences) | Medium |
| Lead scoring/qualification | Manual | Google Sheets | Semi-auto (scoring formula in Sheets or n8n) | Medium |
| CRM updates | Manual | Google Sheets | Semi-auto (n8n auto-logs from email/form) | Medium |
| Landing page lead capture | Semi-auto | Next.js form | Fully auto (form > Sheets > email sequence) | High |
| Local business prospecting | Manual | Google Maps + browser | Semi-auto (scraper + enrichment API) | Low |

### Research and alpha scanning

| Task | Current Status | Tool Used | Could Be Automated? | Priority |
|------|---------------|-----------|---------------------|----------|
| Twitter account scraping | Semi-auto | `twitter_alpha_scraper.py` | Fully auto (cron job + Brave cookies) | High |
| Twitter bookmark extraction | Semi-auto | `twitter_alpha_scraper.py --bookmarks` | Fully auto (cron job) | High |
| Reddit 41 subreddit scraping | Semi-auto | `reddit_deep_scraper.py` | Fully auto (cron job, no browser needed) | High |
| GitHub trending scan | Manual | Browser | Fully auto (GitHub API + cron) | Medium |
| Product Hunt daily scan | Manual | Browser | Fully auto (PH API + cron) | Medium |
| Google Trends monitoring | Manual | Browser | Semi-auto (Serpapi or scraper) | Low |
| Competitor monitoring (social) | Manual | Browser | Semi-auto (scraper + diff alerts) | Medium |
| Competitor monitoring (website) | Manual | Visualping / Browser | Fully auto (Visualping) | Medium |
| Price monitoring | Manual | Browser | Fully auto (Visualping on pricing pages) | Medium |
| App Store monitoring | Manual | Browser | Semi-auto (Sensor Tower API or scraper) | Low |
| Alpha review and scoring | Manual | Human judgment | Manual (quality requires human) | N/A |
| Review mining | Manual | Browser | Semi-auto (scraper + sentiment analysis) | Low |

### Financial tracking

| Task | Current Status | Tool Used | Could Be Automated? | Priority |
|------|---------------|-----------|---------------------|----------|
| Revenue logging | Manual | `FINANCIALS/REVENUE_TRACKER.csv` | Semi-auto (Stripe webhook > n8n > CSV) | High |
| Expense logging | Manual | `FINANCIALS/EXPENSE_TRACKER.csv` | Semi-auto (bank API or Plaid > CSV) | Medium |
| P&L calculation | Manual | `FINANCIALS/P_AND_L_MONTHLY.csv` | Fully auto (formula-based from Rev + Exp) | Medium |
| Tax deduction tracking | Manual | `FINANCIALS/TAX_DEDUCTIONS_2026.csv` | Semi-auto (auto-tag from expense categories) | Low |
| Invoice generation | Not started | None | Fully auto (Stripe auto-invoicing) | Low |
| Metrics dashboard | Semi-auto | `printmaxx_quant_terminal.py` | Fully auto (reads from CSVs on schedule) | Medium |

### App building and deployment

| Task | Current Status | Tool Used | Could Be Automated? | Priority |
|------|---------------|-----------|---------------------|----------|
| App code generation | Manual | Claude Code | Semi-auto (ralph loops for scaffolding) | Medium |
| Unit test writing | Manual | Claude Code | Semi-auto (AI generates test stubs) | Medium |
| Build and compile | Manual | Xcode / npm | Fully auto (CI/CD via GitHub Actions) | High |
| App Store submission | Manual | Xcode / App Store Connect | Semi-auto (Fastlane) | Medium |
| Screenshot generation | Manual | Simulator + screenshot | Semi-auto (Fastlane Snapshot) | Low |
| ASO keyword optimization | Manual | Research | Semi-auto (keyword tracker + suggestions) | Medium |
| App Store review monitoring | Manual | Browser | Fully auto (AppFollow or Sensor Tower alerts) | Medium |
| Crash monitoring | Not started | None | Fully auto (Sentry or Crashlytics) | High |

### Email campaigns

| Task | Current Status | Tool Used | Could Be Automated? | Priority |
|------|---------------|-----------|---------------------|----------|
| Welcome sequence (new subscriber) | Not started | Beehiiv (planned) | Fully auto (Beehiiv automation) | Critical |
| Nurture sequence (leads) | Not started | Instantly (planned) | Fully auto (Instantly drip sequences) | Critical |
| Broadcast newsletters | Not started | Beehiiv (planned) | Semi-auto (write > schedule > auto-send) | High |
| Cold email campaigns | Not started | Instantly (planned) | Fully auto (after initial setup) | Critical |
| Email list segmentation | Not started | Beehiiv (planned) | Semi-auto (tag-based rules) | Medium |
| Unsubscribe handling | Not started | Beehiiv (planned) | Fully auto (platform handles) | High |
| Bounce management | Not started | Instantly (planned) | Fully auto (platform handles) | High |
| A/B testing subject lines | Not started | Beehiiv (planned) | Fully auto (built-in A/B testing) | Medium |

### Social media management

| Task | Current Status | Tool Used | Could Be Automated? | Priority |
|------|---------------|-----------|---------------------|----------|
| Account warmup | Not started | Manual + guides | Semi-auto (schedule + proxy rotation) | High |
| Follower growth (organic) | Not started | Manual engagement | Manual (authentic engagement required) | N/A |
| DM responses | Manual | Native apps | Semi-auto (canned responses for FAQ) | Low |
| Analytics collection | Manual | Native analytics | Semi-auto (n8n pulls from APIs weekly) | Medium |
| Cross-posting | Manual | Copy-paste | Fully auto (Buffer or n8n cross-post flow) | High |
| Story/Reel posting | Manual | Native apps | Semi-auto (Buffer supports IG Stories) | Medium |
| Community management | Manual | Native apps | Manual (relationship-based) | N/A |

### Analytics and reporting

| Task | Current Status | Tool Used | Could Be Automated? | Priority |
|------|---------------|-----------|---------------------|----------|
| Weekly metrics compilation | Manual | Google Sheets | Semi-auto (n8n pulls from GA + social APIs) | High |
| Dashboard updates | Semi-auto | `quant_dashboard.py` | Fully auto (runs on schedule) | Medium |
| Funnel metrics tracking | Manual | `LEDGER/FUNNEL_METRICS.csv` | Semi-auto (n8n logs from Stripe + GA) | Medium |
| A/B test analysis | Not started | None | Semi-auto (statistical significance calc) | Low |
| Revenue projection | Manual | `revenue_projector.py` | Semi-auto (runs with updated inputs) | Low |
| Content performance analysis | Manual | Native analytics | Semi-auto (API pulls + ranking) | Medium |

---

## Section B: Automation architecture diagram

```
=================================================================================
                        PRINTMAXX AUTOMATION ARCHITECTURE
=================================================================================

INPUT SOURCES                    PROCESSING                     OUTPUTS
--------------                   ----------                     -------

[Twitter 92 accts] ─────┐
[Twitter Bookmarks] ─────┤
[Reddit 41 subs] ────────┤       ┌──────────────────┐
[GitHub Trending] ────────┼──────>│  ALPHA PIPELINE  │──────> LEDGER/ALPHA_STAGING.csv
[Product Hunt] ───────────┤       │  (Python scripts) │──────> LEDGER/ALPHA_BY_CATEGORY/
[Google Trends] ──────────┤       │                  │
[Competitor Sites] ───────┘       │  Scrape > Parse  │
                                  │  > Score > Store │
                                  └──────────────────┘
                                          │
                                          │ PENDING_REVIEW
                                          v
                                  ┌──────────────────┐
                                  │  HUMAN REVIEW    │ <──── alpha-review.md rules
                                  │  (approve/reject)│
                                  └──────────────────┘
                                          │
                                          │ APPROVED
                                          v
┌─────────────────────────────────────────────────────────────────────────────┐
│                          CONTENT ENGINE (n8n / Claude)                      │
│                                                                             │
│  Alpha ──> [Claude Batch Generate] ──> Content Variants ──> QA Queue       │
│                                                                             │
│  Source content ──> [Repurposing Flow] ──> 5+ variants per platform        │
│                                                                             │
│  Calendar ──> [Auto-populate] ──> Buffer CSVs ──> Scheduled Posts          │
└─────────────────────────────────────────────────────────────────────────────┘
          │                    │                    │
          v                    v                    v
   ┌─────────────┐    ┌──────────────┐    ┌──────────────────┐
   │   BUFFER     │    │  BEEHIIV     │    │  CONTENT/        │
   │  (scheduling)│    │  (email)     │    │  (stored drafts) │
   │             │    │              │    │                  │
   │ X, IG, LI  │    │ Newsletters  │    │ social/          │
   │ TikTok     │    │ Welcome seq  │    │ email_sequences/ │
   │            │    │ Broadcasts   │    │ medium_articles/ │
   └──────┬──────┘    └──────┬───────┘    └──────────────────┘
          │                   │
          v                   v
   ┌─────────────────────────────────┐
   │       DISTRIBUTION LAYER        │
   │                                 │
   │  X/Twitter    Instagram         │
   │  LinkedIn     TikTok           │
   │  YouTube      Reddit           │
   │  Beehiiv      Medium           │
   │  Substack     Fanvue           │
   │  Pinterest    Telegram         │
   └────────────────┬────────────────┘
                    │
                    │ Engagement / Revenue
                    v
   ┌─────────────────────────────────────────┐
   │          MEASUREMENT LAYER               │
   │                                          │
   │  Google Analytics ──> Sessions, CVR      │
   │  Social Analytics ──> Followers, ER      │
   │  Stripe/Gumroad  ──> Revenue, AOV       │
   │  Beehiiv         ──> Subs, Open Rate    │
   │  App Store       ──> Downloads, Rating  │
   │                                          │
   │  All data flows to:                      │
   │  FINANCIALS/REVENUE_TRACKER.csv          │
   │  FINANCIALS/EXPENSE_TRACKER.csv          │
   │  LEDGER/FUNNEL_METRICS.csv               │
   └────────────────┬────────────────────────┘
                    │
                    v
   ┌─────────────────────────────────────────┐
   │        QUANT DASHBOARD LAYER             │
   │                                          │
   │  printmaxx_quant_terminal.py             │
   │  ops_dashboard.py                        │
   │  revenue_projector.py                    │
   │  method_performance_analyzer.py          │
   │                                          │
   │  Reads CSVs ──> Displays metrics         │
   │  ──> Flags anomalies ──> Triggers alerts │
   └──────────────────────────────────────────┘


PARALLEL TRACK: LEAD GENERATION

[Apollo.io] ─────> [Verified Emails] ─────> [Instantly.ai] ─────> [Cold Email Sequences]
                                                    │
[LinkedIn Search] ──> [Connection Requests] ──>     │
                      [Follow-up Messages]          │
                                                    v
                                            ┌──────────────┐
                                            │  LEAD INBOX   │
[Website Forms] ──> [LEDGER/leads.csv] ──>  │  (CRM Sheet)  │
[Social DMs] ──> [Manual log] ──>           │              │
                                            │  Score > Route│
                                            └──────┬───────┘
                                                   │
                                    ┌──────────────┼──────────────┐
                                    v              v              v
                               HOT leads      WARM leads     COLD leads
                               (Flag Slack)   (Nurture seq)  (Newsletter)


PARALLEL TRACK: APP FACTORY

[App Idea] ──> [Clone Research] ──> [Claude Code Build] ──> [GitHub Repo]
                                                                  │
                                                          ┌───────┴───────┐
                                                          v               v
                                                    [iOS Build]    [Web Build]
                                                          │               │
                                                          v               v
                                                    [TestFlight]   [Vercel Deploy]
                                                          │
                                                          v
                                                    [App Store Submit]
                                                          │
                                                          v
                                                    [ASO + Launch Marketing]


OVERNIGHT: RALPH LOOPS

┌─────────────────────────────────────────────────────────┐
│  ralph/.swarm/  (working automation system)              │
│                                                          │
│  while :; do                                             │
│    cat PROMPT.md | claude --dangerously-skip-permissions │
│    --print                                               │
│  done                                                    │
│                                                          │
│  Reads state from files ──> Does ONE task ──>            │
│  Writes state ──> Exits ──> Next iteration               │
│                                                          │
│  Outputs: alpha entries, content drafts, research,       │
│  code commits, data processing                           │
└─────────────────────────────────────────────────────────┘
```

---

## Section C: Automation priority matrix

### Quick wins (under 2 hours to automate, high time savings)

| # | Task | Time to Automate | Weekly Time Saved | Tool | How |
|---|------|-------------------|-------------------|------|-----|
| 1 | Cross-posting to multiple platforms | 30 min | 3 hrs | Buffer | Upload Buffer CSVs from `AUTOMATIONS/content_posting/`, connect accounts, enable auto-schedule |
| 2 | Newsletter scheduling | 30 min | 1 hr | Beehiiv | Write newsletter, use Beehiiv's schedule feature instead of manual send |
| 3 | Reddit scraping (daily) | 1 hr | 2 hrs | Cron + `reddit_deep_scraper.py` | Add cron job: `0 6 * * * python3 /path/to/reddit_deep_scraper.py --all` |
| 4 | Twitter scraping (daily) | 1 hr | 2 hrs | Cron + `twitter_alpha_scraper.py` | Add cron job: `0 6 * * * python3 /path/to/twitter_alpha_scraper.py --all` |
| 5 | Email warmup | 30 min | 5 hrs | Instantly.ai | Sign up, connect inboxes, enable auto-warmup (runs 24/7 unattended) |
| 6 | Stripe revenue auto-logging | 1 hr | 1 hr | Stripe webhook + n8n | Webhook on `payment_intent.succeeded` > append to REVENUE_TRACKER.csv |
| 7 | Landing page lead capture to CRM | 1 hr | 30 min | Next.js form + Google Sheets API | Form submission > API call > append to leads.csv and trigger email |
| 8 | Content calendar auto-population | 1.5 hrs | 2 hrs | n8n + Google Sheets | When content is approved in QA queue, auto-add to calendar and generate Buffer CSV |
| 9 | Visualping competitor alerts | 1 hr | 3 hrs | Visualping | Add 10 competitor pricing pages + 10 blog pages. Alerts on change. |
| 10 | P&L auto-calculation | 30 min | 30 min | Google Sheets formulas | SUMIF formulas pulling from Revenue + Expense trackers |

**Total quick win time savings: ~20 hours/week from ~9 hours of setup work.**

### Medium effort (2-8 hours to automate, good ROI)

| # | Task | Time to Automate | Weekly Time Saved | Tool | How |
|---|------|-------------------|-------------------|------|-----|
| 1 | Cold email sequences (full pipeline) | 4 hrs | 10 hrs | Instantly.ai | Set up inboxes, import lists, create 3-step sequences, enable auto-follow-up |
| 2 | Content batch generation | 3 hrs | 8 hrs | Ralph loop + Claude | Create ralph loop: input topics > Claude generates > saves to CONTENT/ > flags for QA |
| 3 | Weekly metrics auto-report | 6 hrs | 3 hrs | n8n + GA API + social APIs | n8n flow: pull GA, X, IG, Beehiiv metrics > compile > send Slack summary every Monday |
| 4 | Lead scoring automation | 3 hrs | 2 hrs | Google Sheets + n8n | Score formula based on: company size, title seniority, engagement level > auto-route |
| 5 | GitHub trending + PH daily scan | 4 hrs | 2 hrs | Python scripts + cron | Write scrapers for GitHub API and PH API, append to ALPHA_STAGING.csv on schedule |
| 6 | App Store review monitoring | 2 hrs | 1 hr | AppFollow (free tier) or custom script | Auto-alert on new reviews, especially 1-2 star |
| 7 | Social analytics collection | 4 hrs | 2 hrs | n8n + platform APIs | Weekly pull of follower count, ER, impressions per platform > log to metrics sheet |
| 8 | Content repurposing pipeline | 6 hrs | 5 hrs | n8n + Claude API | Input: blog post URL. Output: tweet, thread, IG carousel text, LinkedIn post, video script |
| 9 | Invoice auto-generation | 2 hrs | 1 hr | Stripe Billing | Enable Stripe auto-invoicing for subscriptions and one-time payments |
| 10 | Account warmup scheduling | 4 hrs | 3 hrs | Playwright + proxy + cron | Scripted daily actions (scroll, like, post) on new accounts via residential proxy |

**Total medium effort time savings: ~37 hours/week from ~38 hours of setup work. Payback: 1 week.**

### Major projects (8+ hours, transformative impact)

| # | Task | Time to Automate | Impact | Tool | How |
|---|------|-------------------|--------|------|-----|
| 1 | Full content-to-distribution pipeline | 20 hrs | Eliminates 15+ hrs/week manual work | n8n + Claude API + Buffer API + Beehiiv API | End-to-end: topic > generate > QA queue > approve > schedule > post > track metrics |
| 2 | AI influencer content factory | 40 hrs | Enables entire revenue lane | ComfyUI + Leonardo.ai + CapCut + cron | Generate character images, create video content, schedule across platforms, monitor engagement |
| 3 | Mega Ralph loop (overnight automation) | 15 hrs | 6-phase daily autonomous cycle | Ralph pattern + Claude API + Python | Build the documented but not-yet-built mega loop: research > reflect > generate > execute > intel > checkpoint |
| 4 | Lead gen to close pipeline | 25 hrs | Automates entire sales funnel | Apollo API + Instantly + n8n + Stripe | Prospect > verify > send sequence > score response > route hot leads > proposal > close > invoice |
| 5 | Multi-platform analytics dashboard | 12 hrs | Real-time visibility | n8n + GA + social APIs + Sheets | Live dashboard pulling all metrics hourly, anomaly detection, automated alerts |
| 6 | CI/CD for app factory | 10 hrs | Ship apps 5x faster | GitHub Actions + Fastlane + TestFlight | Push to main > build > test > screenshot > submit to App Store |
| 7 | Automated funnel builder | 30 hrs | Rapid landing page deployment | Next.js templates + Vercel + Stripe | Template library > populate with product data > deploy > connect payments > launch |
| 8 | Self-healing scraper infrastructure | 15 hrs | Zero-downtime data collection | Python + Playwright + proxy rotation + error handling | Auto-retry on failure, proxy rotation on block, fallback chain, alert on persistent failure |

**Major projects create compounding returns. Prioritize #1 (content pipeline) and #4 (lead gen pipeline) first.**

---

## Section D: Tool integration map

### Current integrations (working)

```
Claude Code ──────── Generates ──────> CONTENT/ (drafts)
                                       LEDGER/ (data)
                                       AUTOMATIONS/ (scripts)

Python Scripts ────── Read/Write ────> LEDGER/*.csv (all tracking data)
                                       FINANCIALS/*.csv (financial data)

reddit_deep_scraper.py ── Requests ──> Reddit JSON API ──> LEDGER/ALPHA_STAGING.csv

twitter_alpha_scraper.py ── Brave Cookies ──> X/Twitter ──> LEDGER/ALPHA_STAGING.csv

quant_terminal.py ─── Reads ──> All CSVs ──> Terminal display
```

### Planned integrations (not yet set up)

```
Buffer ──────── Schedules ────────> X, IG, LinkedIn, TikTok
  ^                                    │
  │                                    v
Content Calendar (Sheets) ──> Buffer CSVs ──> Auto-post

Beehiiv ─────── Sends ───────────> Email subscribers
  ^                                    │
  │                                    v
CONTENT/email_sequences/ ──> Beehiiv sequences ──> Open/click tracking

Instantly.ai ── Sends ───────────> Cold email prospects
  ^                                    │
  │                                    v
Apollo.io ──> Verified emails ──> Instantly lists ──> Auto-sequence ──> Reply tracking

Stripe ──────── Processes ────────> Payments
  ^                                    │
  │                                    v
Gumroad/Whop ──> Product pages ──> Stripe checkout ──> FINANCIALS/REVENUE_TRACKER.csv

n8n (self-hosted) ── Orchestrates ──> All automation flows
  │
  ├──> Trigger: Stripe webhook ──> Log revenue
  ├──> Trigger: Form submission ──> Add lead + send welcome email
  ├──> Trigger: Cron (daily) ──> Pull analytics + compile report
  ├──> Trigger: Cron (daily) ──> Run research scrapers
  ├──> Trigger: New content approved ──> Add to Buffer + Beehiiv
  └──> Trigger: Visualping alert ──> Log competitor change

Vercel ──────── Hosts ────────────> Landing pages (printmaxx-site)
  ^                                    │
  │                                    v
GitHub ──> Push to main ──> Vercel auto-deploy ──> Live site

Fastlane ────── Submits ──────────> App Store
  ^                                    │
  │                                    v
GitHub Actions ──> Build iOS ──> TestFlight ──> App Store Connect
```

### Full integration topology

```
┌─────────────────────────────────────────────────────────────────────┐
│                        DATA LAYER (Source of Truth)                  │
│                                                                     │
│  LEDGER/ALPHA_STAGING.csv          FINANCIALS/REVENUE_TRACKER.csv  │
│  LEDGER/CONTENT_CALENDAR_30DAY.csv FINANCIALS/EXPENSE_TRACKER.csv  │
│  LEDGER/leads.csv                  LEDGER/FUNNEL_METRICS.csv       │
│  LEDGER/MEGA_SHEET/ (10 CSVs)     LEDGER/OUTREACH_PIPELINE.csv    │
│                                                                     │
│  All tools READ FROM and WRITE TO these CSVs                        │
└──────────────────────────────┬──────────────────────────────────────┘
                               │
            ┌──────────────────┼──────────────────┐
            v                  v                  v
┌───────────────────┐ ┌──────────────────┐ ┌──────────────────┐
│  RESEARCH TOOLS   │ │  CONTENT TOOLS   │ │  REVENUE TOOLS   │
│                   │ │                  │ │                  │
│  twitter_scraper  │ │  Claude (gen)    │ │  Stripe (pay)    │
│  reddit_scraper   │ │  Buffer (sched)  │ │  Gumroad (sell)  │
│  Visualping       │ │  Canva (design)  │ │  Whop (sell)     │
│  Apollo (leads)   │ │  CapCut (video)  │ │  Beehiiv (email) │
│  Hunter (email)   │ │  Beehiiv (news)  │ │  RevenueCat (sub)│
│  Google Trends    │ │  Remotion (vid)  │ │  Fanvue (AI)     │
└───────────────────┘ └──────────────────┘ └──────────────────┘
            │                  │                  │
            v                  v                  v
┌─────────────────────────────────────────────────────────────────────┐
│                    ORCHESTRATION LAYER                               │
│                                                                     │
│  n8n (self-hosted) ── Connects everything with webhook triggers     │
│  Cron jobs ── Scheduled Python scripts for scraping                 │
│  Ralph loops ── Overnight autonomous generation                     │
│  GitHub Actions ── CI/CD for apps and site                          │
└──────────────────────────────┬──────────────────────────────────────┘
                               │
                               v
┌─────────────────────────────────────────────────────────────────────┐
│                    DISTRIBUTION LAYER                                │
│                                                                     │
│  X/Twitter ── IG ── LinkedIn ── TikTok ── YouTube                  │
│  Reddit ── Medium ── Substack ── Pinterest                          │
│  Fanvue ── Fansly ── Telegram ── Email                             │
│                                                                     │
│  Each platform fed by Buffer (scheduled) or native posting          │
└──────────────────────────────┬──────────────────────────────────────┘
                               │
                               v
┌─────────────────────────────────────────────────────────────────────┐
│                    MEASUREMENT LAYER                                 │
│                                                                     │
│  GA4 ── Platform analytics ── Stripe dashboard ── Beehiiv stats    │
│                                                                     │
│  All metrics flow back to LEDGER/FUNNEL_METRICS.csv                │
│  Quant terminal reads all CSVs for unified dashboard               │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Section E: Human-only tasks

These tasks cannot be automated. They always require a human.

### Account and identity

| Task | Why Human-Only | Frequency |
|------|---------------|-----------|
| Account creation (social, email, tools) | Requires identity verification, CAPTCHAs, phone verification | As-needed |
| KYC/identity verification | Legal requirement, biometrics | As-needed |
| Domain registration | Payment + identity tied to registrant | As-needed |
| SSL certificate management | Security-critical, tied to domain ownership | Annual |
| Two-factor authentication setup | Requires physical device access | As-needed |

### Financial and legal

| Task | Why Human-Only | Frequency |
|------|---------------|-----------|
| Payment processing (purchasing tools, services) | Financial authorization | As-needed |
| Refund decisions | Judgment call on case-by-case basis | As-needed |
| Subscription management (upgrade/downgrade/cancel) | Budget decisions | Monthly |
| Tax filing and compliance | Legal liability, CPA recommended | Annual |
| Contract review and signing | Legal liability | As-needed |
| FTC compliance review | Legal risk assessment | Before any campaign |
| Terms of service updates | Legal document requiring review | As-needed |
| Privacy policy updates | GDPR/CCPA compliance, legal review | As-needed |
| Bank account and payment processor setup | Financial identity verification | Once |

### Publishing and brand

| Task | Why Human-Only | Frequency |
|------|---------------|-----------|
| Content publishing approval (final sign-off) | Brand risk, compliance check | Daily |
| Ad campaign launch approval | Budget commitment, targeting review | As-needed |
| Press release approval | Public-facing, reputational risk | As-needed |
| Partnership and collaboration decisions | Strategic judgment | As-needed |
| Brand voice calibration | Subjective quality assessment | Monthly |
| Crisis response (negative PR, platform issues) | Requires real-time judgment | As-needed |

### Strategic decisions

| Task | Why Human-Only | Frequency |
|------|---------------|-----------|
| Method selection and prioritization | Strategy requires context + judgment | Weekly |
| Budget allocation across methods | Financial judgment | Monthly |
| Hiring decisions (VAs, freelancers) | People judgment | As-needed |
| Pivot or kill decisions (stop a method) | Sunk cost evaluation, strategic judgment | As-needed |
| Pricing decisions | Market positioning, revenue impact | As-needed |
| Product roadmap prioritization | Strategic direction | Monthly |
| Capital allocation (investments) | Financial risk management | As-needed |

### Security and infrastructure

| Task | Why Human-Only | Frequency |
|------|---------------|-----------|
| Credential management (passwords, API keys) | Security-critical | As-needed |
| Security incident response | Judgment and urgency required | As-needed |
| Backup verification | Trust-but-verify on critical data | Weekly |
| Access control (granting/revoking VA access) | Security boundary decisions | As-needed |

### Human checkpoints in automated flows

Even in automated pipelines, certain gates require human approval:

```
Content Pipeline:     Generate (auto) ──> QA Review (HUMAN) ──> Publish (auto)
Email Campaigns:      Draft (auto) ──> Approve Send (HUMAN) ──> Send (auto)
Cold Outreach:        Build List (auto) ──> Approve List (HUMAN) ──> Send (auto)
App Submission:       Build (auto) ──> TestFlight Review (HUMAN) ──> Submit (auto)
Purchases:            Research (auto) ──> PURCHASE_REQUEST.md (HUMAN) ──> Buy
Ad Campaigns:         Creative + targeting (auto) ──> Approve Budget (HUMAN) ──> Launch (auto)
Refunds:              Customer request (auto-logged) ──> Approve Refund (HUMAN) ──> Process (auto)
```

**Rule: Automate everything around the human checkpoint. Minimize the human's job to a binary approve/reject decision with all context pre-assembled.**

---

## Implementation roadmap

### Week 1: Quick wins (estimated 9 hours)
1. Set up cron jobs for twitter_alpha_scraper.py and reddit_deep_scraper.py
2. Connect Buffer to all social accounts, upload existing Buffer CSVs
3. Set up Visualping on 10 competitor pricing pages
4. Create P&L auto-calculation formulas in Google Sheets
5. Connect landing page form to leads.csv via API

### Week 2: Cold email pipeline (estimated 8 hours)
1. Sign up for Instantly.ai, connect inboxes, start warmup
2. Import first list from Apollo.io
3. Create 3-step cold email sequences
4. Set up reply tracking and lead routing

### Week 3: Content pipeline (estimated 12 hours)
1. Install n8n (self-hosted on Railway or local Docker)
2. Build content repurposing flow (input source > Claude API > output variants)
3. Build auto-calendar flow (approved content > Buffer CSV > schedule)
4. Build newsletter flow (curated links > Beehiiv draft)

### Week 4: Measurement and reporting (estimated 10 hours)
1. Build weekly metrics auto-report (n8n + GA + social APIs)
2. Set up Stripe webhook for auto revenue logging
3. Build anomaly detection alerts (20%+ changes in any metric)
4. Connect all metrics to quant dashboard

### Month 2: Major projects
1. Full content-to-distribution pipeline (20 hrs)
2. AI influencer content factory (40 hrs)
3. Lead gen to close pipeline (25 hrs)

### Month 3: Scale
1. CI/CD for app factory (10 hrs)
2. Self-healing scraper infrastructure (15 hrs)
3. Multi-platform analytics dashboard (12 hrs)
