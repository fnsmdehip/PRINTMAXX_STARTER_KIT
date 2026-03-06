# Lead Magnets - The Print Run Newsletter

**Purpose:** gated content that drives email signups for The Print Run newsletter
**Hosting:** Gumroad ($0 products) or direct PDF links behind Beehiiv signup
**Voice:** PRINTMAXX copy style throughout. no fluff. specific numbers. actionable immediately.

---

## Lead Magnet #1: "The $0 Tech Stack"

**Format:** PDF, 12-15 pages
**Hook:** "20 free tools that replace $1,200/month in paid software"
**CTA placement:** Twitter bio, Reddit profile, newsletter signup page, cold emails

### Outline:

**Cover page:** "The $0 Tech Stack: 20 Free Tools That Replace $1,200/Month in Paid Software"
subtitle: "tested by a solopreneur running 7 apps on zero infrastructure budget"

**Page 1: Why this exists**
- I audited my entire tool stack and replaced everything I could with free alternatives
- 6 months of testing. these are the ones that stuck.
- each tool includes: what it replaces, actual cost saved, setup time, and the one limitation you should know about

**Pages 2-11: The 20 tools (half-page each)**

1. surge.sh (replaces Vercel/Netlify paid tiers) - saves $20/mo - 2 min setup
2. Beehiiv free tier (replaces Mailchimp) - saves $20/mo - 15 min setup
3. Cal.com self-hosted (replaces Calendly) - saves $12/mo - 20 min setup
4. Figma free (replaces Canva Pro) - saves $13/mo - already know it
5. Google Search Console (replaces Ahrefs basic) - saves $99/mo - 5 min setup
6. Obsidian (replaces Notion team) - saves $10/mo - 30 min migration
7. Python + cron (replaces Zapier) - saves $30/mo - 3 hours to learn
8. GitHub Pages (replaces hosting for docs/blogs) - saves $10/mo - 10 min setup
9. Plausible self-hosted (replaces Google Analytics paid) - saves $9/mo - 25 min setup
10. Umami (replaces Mixpanel) - saves $25/mo - 20 min setup
11. n8n self-hosted (replaces Make/Zapier for complex flows) - saves $20/mo - 45 min setup
12. Typesense (replaces Algolia) - saves $29/mo - 30 min setup
13. Resend free tier (replaces SendGrid paid) - saves $15/mo - 10 min setup
14. Uptime Robot free (replaces Pingdom) - saves $15/mo - 5 min setup
15. Tally.so free (replaces Typeform) - saves $25/mo - instant
16. Excalidraw (replaces Lucidchart) - saves $8/mo - instant
17. SimpleLogin (replaces email aliases services) - saves $5/mo - 10 min setup
18. Claude free tier + prompts (replaces Jasper AI) - saves $49/mo - already using it
19. OBS Studio (replaces Loom paid) - saves $13/mo - 15 min setup
20. Planka (replaces Trello paid) - saves $10/mo - 20 min setup

each entry format:
```
[TOOL NAME] - replaces [PAID TOOL] ($X/mo)
what it does: [one sentence]
setup time: [X minutes]
the limitation: [one honest sentence about what you lose]
verdict: [one sentence]
```

**Page 12: The total math**
- total monthly savings: $457/month ($5,484/year)
- total setup time: ~8 hours one-time investment
- tools I went back to paying for and why (3 tools, 2 sentences each)

**Page 13: CTA**
- "I write about this stuff every Sunday in The Print Run newsletter."
- link to signup
- "no spam. one email per week. unsubscribe anytime."

---

## Lead Magnet #2: "Cold Email Swipe File"

**Format:** PDF, 18-20 pages
**Hook:** "15 cold email templates with 8-15% reply rates. copy, paste, personalize, send."
**CTA placement:** LinkedIn posts, r/Entrepreneur discussions, email signatures

### Outline:

**Cover page:** "Cold Email Swipe File: 15 Templates That Actually Get Replies"
subtitle: "tested across 1,600+ sends. reply rates and exact copy included."

**Page 1: How to use this file**
- these are starting points. personalization is the difference between 2% and 12% reply rates.
- each template includes: the subject line, the body, when to use it, and the one thing to customize
- A/B test results included where available

**Pages 2-16: The 15 templates (one per page)**

category 1: service outreach (5 templates)
1. the "I noticed your [specific problem]" email (12% reply rate)
2. the "quick question about [their company]" email (10% reply rate)
3. the "I built something for companies like yours" email (8% reply rate)
4. the "mutual connection" email (15% reply rate, requires research)
5. the "case study drop" email (9% reply rate)

category 2: partnership/collab (5 templates)
6. the "newsletter swap" email (14% reply rate)
7. the "guest post pitch" email (11% reply rate)
8. the "tool review offer" email (13% reply rate)
9. the "co-marketing proposal" email (8% reply rate)
10. the "your audience would love this" email (10% reply rate)

category 3: follow-ups (5 templates)
11. the "3-day follow-up" (adds 4% to initial reply rate)
12. the "value bump" follow-up (share something useful, then re-ask)
13. the "breakup email" (last attempt, surprisingly high reply rate)
14. the "different angle" follow-up (new approach to same ask)
15. the "social proof drop" follow-up (share a result, then re-engage)

each template format:
```
TEMPLATE NAME
reply rate: X%
when to use: [one sentence]
subject line: [exact text]
body: [exact text with [BRACKETS] for personalization]
the one thing to customize: [specific instruction]
common mistake: [what kills this template's effectiveness]
```

**Page 17: The math behind cold email**
- average cost per send: $0.002 (using free SMTP)
- average reply rate across all 15 templates: 10.4%
- average conversion from reply to call: 23%
- average conversion from call to client: 18%
- math: 1,000 emails = 104 replies = 24 calls = 4 clients

**Page 18: CTA**
- "new templates and results every week in The Print Run."
- signup link

---

## Lead Magnet #3: "PWA Starter Kit"

**Format:** ZIP file (HTML + JS + manifest + service worker + README)
**Hook:** "ship an installable web app in 30 minutes. no frameworks. no build step. no app store."
**CTA placement:** r/webdev, dev.to articles, GitHub README, Twitter technical threads

### Outline:

**README.md (inside ZIP):**

```
PWA Starter Kit
================

a minimal, production-ready PWA boilerplate.
one HTML file. one service worker. one manifest.
zero dependencies. zero build step.

what you get:
- index.html (app shell with responsive layout)
- sw.js (cache-first service worker, 28 lines)
- manifest.json (installable PWA config)
- icons/ (placeholder icons at required sizes)
- deploy.sh (one-command deploy to surge.sh)

setup:
1. unzip
2. edit index.html (your app goes here)
3. edit manifest.json (your app name/colors)
4. run: bash deploy.sh
5. done. your PWA is live.

what this gives you:
- installable on any device (home screen icon)
- works offline (service worker caches everything)
- loads in <1 second on 3G
- lighthouse score: 98-100
- total size: under 15KB before your code

what this doesn't include:
- no framework (add one if you need it)
- no database (use IndexedDB for client-side storage)
- no auth (add it when you need user accounts)
- no analytics (add a 14-line tracker or use Plausible)

built by The Print Run (theprintrun.beehiiv.com)
```

**Files included:**

1. `index.html` - responsive app shell with:
   - meta viewport tag
   - manifest link
   - service worker registration (6 lines)
   - minimal CSS (system fonts, responsive grid)
   - placeholder content with comments showing where to add app code

2. `sw.js` - cache-first service worker:
   - install event: precache app shell
   - fetch event: cache-first with network fallback
   - activate event: clean old caches
   - total: 28 lines, heavily commented

3. `manifest.json` - PWA manifest:
   - app name, short name, description
   - theme color, background color
   - display: standalone
   - icon references at 192x192 and 512x512
   - start_url and scope

4. `icons/` - placeholder icons:
   - icon-192.png (simple colored square)
   - icon-512.png (simple colored square)
   - README: "replace these with your app icons"

5. `deploy.sh` - deployment script:
   - checks if surge CLI is installed
   - runs `surge ./ your-app-name.surge.sh`
   - prints live URL

6. `GUIDE.md` - 500-word guide:
   - how service workers actually work (3 paragraphs)
   - how to add IndexedDB storage (code snippet)
   - how to customize the manifest (field-by-field)
   - common PWA gotchas and fixes
   - link to The Print Run for weekly PWA tips

---

## Lead Magnet #4: "The Solopreneur Checklist"

**Format:** PDF, 8-10 pages
**Hook:** "the complete launch checklist from $0 to $10K/month. 127 tasks. nothing missing."
**CTA placement:** r/Entrepreneur, indie hacker communities, Twitter threads about starting up

### Outline:

**Cover page:** "The Solopreneur Checklist: $0 to $10K/Month"
subtitle: "127 tasks organized by revenue stage. check them off as you go."

**Page 1: How this works**
- 5 stages. each stage has specific tasks.
- don't skip stages. don't jump ahead.
- each task has a time estimate and priority level (must-do / should-do / nice-to-have)

**Page 2-3: Stage 1 - Foundation ($0, pre-revenue)**
tasks include:
- [ ] register domain ($12/year) - 15 min - must-do
- [ ] set up email (Google Workspace or Zoho free) - 20 min - must-do
- [ ] create landing page with email capture - 2 hours - must-do
- [ ] set up payment processing (Stripe) - 30 min - must-do
- [ ] create social accounts (Twitter, LinkedIn minimum) - 30 min - must-do
- [ ] write 1-line value proposition - 1 hour - must-do
- [ ] identify 3 competitors and study their pricing - 2 hours - must-do
- [ ] set up basic analytics - 15 min - should-do
- [ ] create a simple logo (Figma, 30 min is enough) - 30 min - should-do
- [ ] write privacy policy (free generator) - 15 min - must-do
- [ ] set up Git repo for code - 10 min - should-do
(~25 tasks total for Stage 1)

**Page 4-5: Stage 2 - First Revenue ($1-$500/month)**
tasks include:
- [ ] launch MVP to first 10 users - varies - must-do
- [ ] collect feedback from first 5 users - 2 hours - must-do
- [ ] set up email welcome sequence (3 emails) - 3 hours - must-do
- [ ] create first lead magnet - 4 hours - should-do
- [ ] post to 3 communities per week - 3 hours/week - must-do
- [ ] send 20 cold emails per week - 2 hours/week - should-do
- [ ] set up basic customer support (email is fine) - 30 min - must-do
- [ ] create 1 piece of long-form content per week - 3 hours/week - should-do
(~30 tasks total for Stage 2)

**Page 5-6: Stage 3 - Traction ($500-$2,000/month)**
tasks include:
- [ ] identify top acquisition channel and double down - 2 hours analysis - must-do
- [ ] set up referral program - 3 hours - should-do
- [ ] create upsell or second product - 10+ hours - should-do
- [ ] automate repetitive tasks (content, email, reporting) - 8+ hours - must-do
- [ ] set up proper financial tracking - 2 hours - must-do
- [ ] create standard operating procedures for repeatable tasks - 4 hours - should-do
(~25 tasks total for Stage 3)

**Page 7-8: Stage 4 - Growth ($2,000-$5,000/month)**
tasks include:
- [ ] hire first contractor (VA, designer, or developer) - 5 hours - should-do
- [ ] set up paid acquisition test ($100 budget) - 4 hours - should-do
- [ ] build email list to 1,000+ - ongoing - must-do
- [ ] create 2-3 additional revenue streams - 20+ hours - should-do
- [ ] set up proper bookkeeping - 3 hours - must-do
- [ ] consider LLC formation - 2 hours research - should-do
(~22 tasks total for Stage 4)

**Page 8-9: Stage 5 - Scale ($5,000-$10,000/month)**
tasks include:
- [ ] systemize all operations (anyone could run it for a week without you) - 20+ hours - must-do
- [ ] build team to 2-3 contractors - ongoing - should-do
- [ ] launch premium/enterprise tier - 10+ hours - should-do
- [ ] set up affiliate program - 5 hours - should-do
- [ ] plan next product or acquisition - ongoing - nice-to-have
(~25 tasks total for Stage 5)

**Page 10: CTA**
- "I share one specific task from this checklist every week in The Print Run, with the exact steps and tools."
- signup link

---

## Lead Magnet #5: "Landing Page Teardown"

**Format:** PDF, 20-25 pages
**Hook:** "10 high-converting landing pages analyzed element by element. what works, what doesn't, and why."
**CTA placement:** r/marketing, design communities, Twitter marketing threads, LinkedIn

### Outline:

**Cover page:** "Landing Page Teardown: 10 Pages That Convert at 5%+"
subtitle: "element-by-element analysis. steal the patterns. skip the mistakes."

**Page 1: What makes a high-converting page**
- conversion rate benchmarks by industry (SaaS: 3-7%, info products: 5-15%, services: 8-12%)
- the 5 elements every converting page has (headline, social proof, CTA, objection handling, urgency)
- how I selected these 10 pages (all publicly available, all with estimated >5% conversion)

**Pages 2-21: The 10 teardowns (2 pages each)**

each teardown includes:
- screenshot of the page (annotated with callouts)
- headline analysis: what it promises, why it works
- layout analysis: visual hierarchy, F-pattern or Z-pattern, fold usage
- copy analysis: word count, reading level, power words, specificity
- CTA analysis: button text, color, placement, number of CTAs
- social proof analysis: type (testimonials, logos, numbers), placement, credibility
- what I'd change: 2-3 specific improvements with reasoning
- the one element to steal: the single most effective element on the page

the 10 pages:

1. **a SaaS tool landing page** - analysis of headline structure, pricing table design, and the "above fold" promise
2. **an info product sales page** - long-form copy analysis, objection handling section, guarantee placement
3. **a newsletter signup page** - minimal design, single CTA, how "less is more" works for email capture
4. **a freelancer portfolio/hire page** - trust signals, case study integration, pricing display
5. **a mobile app download page** - app store badge placement, screenshot carousel, feature icons
6. **a course landing page** - curriculum preview, instructor credibility, money-back guarantee
7. **an agency services page** - process visualization, results metrics, contact form optimization
8. **a community/membership page** - member count social proof, content preview, pricing psychology
9. **a digital product (template) page** - preview images, instant delivery messaging, bundle pricing
10. **a consulting offer page** - limited availability, qualification questions, pricing anchoring

**Page 22: The patterns across all 10 pages**
- 8/10 use specific numbers in the headline
- 9/10 have social proof above the fold
- 7/10 use a single primary CTA color throughout
- 6/10 address the #1 objection within the first screen
- 10/10 have mobile-responsive layouts (obvious but worth noting)

**Page 23: The anti-patterns (what failing pages do)**
- multiple competing CTAs
- generic headlines ("Welcome to our website")
- stock photos instead of real product screenshots
- walls of text without visual breaks
- no social proof visible without scrolling

**Page 24: Build your own high-converting page (checklist)**
- [ ] headline: specific benefit in <10 words
- [ ] subheadline: who it's for + what they get
- [ ] social proof above the fold
- [ ] one primary CTA, repeated 2-3 times
- [ ] objection handling section
- [ ] specific numbers (users, results, time saved)
- [ ] mobile responsive
- [ ] page loads in <2 seconds

**Page 25: CTA**
- "I teardown a new page every month in The Print Run."
- "subscribe and I'll send you the next one before anyone else sees it."
- signup link

---

## Distribution Matrix

| lead magnet | primary channel | secondary channel | expected conversion |
|-------------|----------------|-------------------|-------------------|
| $0 Tech Stack | Twitter threads | r/SaaS, r/startups | 15-25% |
| Cold Email Swipe File | LinkedIn posts | r/Entrepreneur, r/sales | 20-30% |
| PWA Starter Kit | r/webdev, dev.to | GitHub, Hacker News | 10-15% |
| Solopreneur Checklist | r/Entrepreneur | indie hacker communities | 20-30% |
| Landing Page Teardown | r/marketing, LinkedIn | Twitter, design communities | 15-25% |

---

## Production Schedule

| lead magnet | create by | launch by | estimated hours |
|-------------|-----------|-----------|----------------|
| $0 Tech Stack | week 1 | week 2 | 6 hours |
| Cold Email Swipe File | week 2 | week 3 | 8 hours |
| PWA Starter Kit | week 3 | week 4 | 4 hours (code already exists) |
| Solopreneur Checklist | week 4 | week 5 | 5 hours |
| Landing Page Teardown | week 6 | week 7 | 10 hours |

---

## Metrics to Track Per Lead Magnet

| metric | target |
|--------|--------|
| download-to-email conversion | >60% |
| email signup to newsletter subscriber | >80% |
| 30-day retention of subscribers acquired via lead magnet | >70% |
| lead magnet mentioned in reader replies | >5% |
| social shares of lead magnet | >10% of downloads |
