# The Solo Developer's Launch Checklist Pack

*5 battle-tested checklists covering every critical decision point from code-complete to first paying customer. Built for solo developers who can't afford to learn what they missed the hard way.*

---

## Why This Matters

Most launches fail because of execution gaps, not product gaps. The app works. The pricing is reasonable. The positioning is fine. But the sitemap was never submitted. SPF wasn't set up. The Product Hunt submission went live at 3 PM instead of 12:01 AM. The refund policy linked to a 404.

These are $1,000 mistakes that cost $9 to prevent.

This pack covers the 5 highest-leverage failure points in a solo product launch: the technical launch sequence, SEO foundation, cold outreach deliverability, Product Hunt execution, and revenue infrastructure. Each checklist is a one-time setup you do once per product. Work through it top to bottom, check the boxes, move on.

---

## Checklist 1: App Launch Checklist

*Pre-launch infrastructure, launch day execution, and post-launch triage. 35 items.*

---

### Phase 1: Pre-Launch (Complete 7+ Days Before Launch)

**Domain and Hosting**
- [ ] Production domain purchased and pointed to hosting (not localhost, not Vercel preview URL)
- [ ] SSL certificate active (HTTPS required — Chrome flags HTTP as "Not Secure" and users bounce)
- [ ] www and non-www both redirect to your canonical domain (pick one, redirect the other)
- [ ] Custom domain email set up — yourname@yourdomain.com, not gmail (credibility signal)
- [ ] Domain auto-renew enabled (losing your domain kills all inbound links and SEO)

**Analytics and Monitoring**
- [ ] Google Analytics 4 (or Plausible / Fathom) installed and firing events on page load
- [ ] Conversion event set up — track the specific action that defines a "win" (signup, purchase, form submit)
- [ ] Error tracking installed: Sentry (free tier) or LogRocket — you need to know when users hit 500 errors
- [ ] Uptime monitor configured: UptimeRobot (free) sends you an email if the site goes down
- [ ] Server-side logging enabled — you want a paper trail when things break

**Payment Integration**
- [ ] Stripe account fully onboarded (not just created — verify bank account, identity docs submitted)
- [ ] Test mode payment confirmed end-to-end (create a $1 test charge, refund it)
- [ ] Live mode payment confirmed with a real card for $1 (don't skip this — test mode behaves differently)
- [ ] Webhook endpoint set up and tested for payment confirmation events
- [ ] Failed payment handling exists — what happens if a card declines? (show error, don't silently fail)
- [ ] Post-purchase redirect goes somewhere useful (thank you page, onboarding, not a blank screen)

**Legal Baseline**
- [ ] Privacy Policy published at /privacy (required by GDPR, CCPA, and Google Analytics terms)
- [ ] Terms of Service published at /terms
- [ ] Refund policy is clearly stated (reduces chargebacks significantly)
- [ ] Cookie consent banner if you use tracking cookies and target EU users
- [ ] Footer links to privacy, terms, and contact visible on every page

**Pre-Launch Infrastructure**
- [ ] Waitlist or email capture is live — collect signups before launch, not just after
- [ ] Favicon set — missing favicon looks unfinished and signals low effort
- [ ] 404 page exists and has a link back to homepage
- [ ] OG image set for social sharing previews (1200x630px) — plain text link previews kill click-through rate
- [ ] Mobile responsiveness tested on actual phone, not just browser dev tools

---

### Phase 2: Launch Day

**Content Execution (Execute in This Order)**
- [ ] Social post goes live on your primary platform at launch open (Twitter/X, LinkedIn, wherever your audience is)
- [ ] Product Hunt listing submitted at 12:01 AM PST (see Checklist 4 for full PH protocol)
- [ ] Show HN post submitted: "Show HN: [Product Name] — [one-line description]" — use news.ycombinator.com/submit
- [ ] Reddit posts live in 2-3 relevant subreddits (r/sideprojects, r/indiehackers, niche-specific sub)
- [ ] Email blast sent to waitlist or existing audience with direct signup link
- [ ] Discord / Slack communities posted in (check rules — many allow launch day posts in #showcase channels)

**Monitoring (Do This All Day)**
- [ ] Check Sentry / error tracker every 2 hours — fix critical errors immediately, note minor ones
- [ ] Check analytics dashboard for traffic sources and drop-off points
- [ ] Respond to every comment, reply, and question within 30 minutes on launch day
- [ ] Screenshot milestones — first user, first payment, first 100 visitors (content for tomorrow)

---

### Phase 3: Post-Launch (Days 2-14)

- [ ] Error triage: categorize every Sentry error by frequency and user impact, fix top 3
- [ ] Funnel drop-off analysis: where are people leaving? Landing page? Signup? Payment?
- [ ] Reply to every person who signed up in the first 48 hours personally — ask what made them try it
- [ ] Create a retargeting audience in Google Ads or Meta Ads from your launch traffic (even if you don't run ads yet)
- [ ] Publish a launch retrospective post — "What I learned launching X" performs well and drives secondary traffic
- [ ] Submit to relevant directories: SaaSHub, AlternativeTo, BetaList, Microlaunch (see Revenue Infrastructure Checklist)

---

## Checklist 2: SEO Audit Checklist

*Technical, on-page, and off-page. Run this once at launch and quarterly after. 28 items.*

---

### Technical SEO

**Crawlability and Indexing**
- [ ] robots.txt exists at /robots.txt and is not blocking important pages (common mistake: staging robots.txt deployed to production)
- [ ] XML sitemap exists at /sitemap.xml and includes all indexable pages
- [ ] Sitemap submitted to Google Search Console (GSC) — without this, indexing can take weeks instead of days
- [ ] Google Search Console property verified — URL prefix or domain verification
- [ ] No important pages blocked by noindex tags (check page source for `<meta name="robots" content="noindex">`)
- [ ] Canonical URLs set on all pages (prevents duplicate content issues from URL parameters)
- [ ] HTTPS on every page — HTTP URLs are treated as separate URLs from HTTPS versions

**Page Speed (Use PageSpeed Insights: pagespeed.web.dev)**
- [ ] Mobile score above 70 (below 50 is a ranking penalty trigger)
- [ ] LCP (Largest Contentful Paint) under 2.5 seconds
- [ ] CLS (Cumulative Layout Shift) under 0.1 (layout shifts frustrate users and hurt rankings)
- [ ] Images compressed and served in WebP format where supported
- [ ] JavaScript bundles not blocking render — defer or async non-critical scripts
- [ ] Core Web Vitals passing in GSC's "Experience" report

**Structured Data**
- [ ] Schema markup added for primary content type (Product, SoftwareApplication, Article, FAQ — whichever fits)
- [ ] Structured data tested in Google's Rich Results Test (search.google.com/test/rich-results)

---

### On-Page SEO

**Title and Meta Tags (Check Every Page)**
- [ ] Title tag on every page — under 60 characters, includes primary keyword, reads naturally
- [ ] Meta description on every page — 150-160 characters, includes a call to action
- [ ] No duplicate title tags across pages (GSC flags this)
- [ ] No duplicate meta descriptions across pages

**Content Structure**
- [ ] One H1 per page — matches the page's primary topic, includes keyword naturally
- [ ] H2s used for major sections, H3s for subsections (not used for visual styling)
- [ ] Internal linking: every important page is linked from at least one other page on the site
- [ ] Images have descriptive alt text — describe what's in the image, not "image1.jpg"
- [ ] Target keyword appears in: title, H1, first paragraph, at least one H2, and naturally throughout

---

### Off-Page SEO

- [ ] Google Business Profile created if you serve local customers or want branded search coverage
- [ ] Listed on relevant niche directories (SaaSHub, AlternativeTo, Capterra, G2 — depends on product type)
- [ ] 5+ backlinks from relevant sites identified as outreach targets (not purchased — editorial links from blogs, communities, tools roundups)
- [ ] One guest post or co-marketing opportunity identified in your niche

---

## Checklist 3: Cold Email QA Checklist

*Run this before every new campaign. Skipping DNS setup alone will kill your deliverability permanently. 22 items.*

---

### Pre-Send: Infrastructure and Deliverability

**DNS Authentication (Do This Once Per Domain, Verify Before Every Campaign)**
- [ ] SPF record set in DNS — verifies that your mail server is authorized to send from this domain (check: mxtoolbox.com/spf.aspx)
- [ ] DKIM configured and enabled in your sending platform — cryptographically signs outgoing mail
- [ ] DMARC record set with at minimum `p=none` for monitoring — without it, some providers auto-reject or flag
- [ ] All three DNS records verified live — not just "set" — use MXToolbox or mail-tester.com to confirm

**Warmup Status**
- [ ] Domain is at least 30 days old before sending cold email (new domains have zero reputation)
- [ ] Inbox warmup running for minimum 14 days before campaign start (Instantly, Mailreach, or Lemwarm)
- [ ] Daily send volume within warmup limits — do not send 500 emails on day 1 of a fresh inbox
- [ ] Warmup tool showing positive sentiment trend (replies, not just opens)

**Pre-Send Technical Checks**
- [ ] Spam score tested at mail-tester.com — aim for 9+/10 before sending
- [ ] All links in email verified as live (broken links increase spam score)
- [ ] Unsubscribe mechanism present and functional (CAN-SPAM requirement in the US)
- [ ] Reply-to address is a monitored inbox — missing replies is missed revenue

---

### Copy Review

**Personalization**
- [ ] Personalization tokens tested with fallback values — `{{first_name|there}}` not `{{first_name}}` raw
- [ ] Lead list spot-checked for data quality: 10 random rows reviewed for obvious errors (wrong names, generic company, mismatched industry)
- [ ] First line is personalized enough that it cannot appear in every email sent that day

**Message Quality**
- [ ] Subject line A/B variant set up — test one variable at a time (length, question vs statement, name inclusion)
- [ ] Email body under 150 words — longer emails drop reply rate significantly
- [ ] One clear CTA, not two (reply, book a call, or click a link — pick one)
- [ ] No spam trigger words in subject or body: "free," "guarantee," "no obligation," "earn money," "click here" (check full list: spamcheck.postmarkapp.com)
- [ ] Signature includes full name, title, and company — not just a first name

---

### Post-Send Monitoring

- [ ] Bounce rate monitored after first 50 sends — if hard bounces exceed 2%, pause and clean the list
- [ ] Reply monitoring active — assign one person or tool to catch replies within 2 business hours
- [ ] Follow-up sequence triggered automatically for non-openers after 3 days (not 24 hours)

---

## Checklist 4: Product Hunt Launch Checklist

*Product Hunt is a one-shot deal. The window is 24 hours. Preparation determines the outcome. 23 items.*

---

### 2 Weeks Before Launch

**Maker Profile and Assets**
- [ ] Maker profile complete: photo, bio, Twitter linked, website linked (incomplete profiles get less credibility)
- [ ] 5+ Maker followers — follow and engage with other makers before you launch (reciprocity)
- [ ] Gallery images prepared: 3-5 screenshots showing core functionality, 1200x800px recommended
- [ ] Thumbnail (240x240px) is clean, readable at small size, and does not look like a stock photo
- [ ] Demo GIF or short video prepared (under 30 seconds) showing the product in action
- [ ] Tagline finalized — 60 characters max, describes what the product does, not what it is

**Hunter Outreach**
- [ ] Identified 3 potential hunters with 500+ followers (not required — makers can self-submit — but a well-connected hunter helps)
- [ ] Hunter outreach sent — personal message, not a template blast
- [ ] Hunter confirmed and given all assets (thumbnail, tagline, description, gallery, link)

**Description and Copy**
- [ ] Full description written: what it is, who it's for, the key differentiator, a specific use case
- [ ] First comment pre-written (you post this the moment the listing goes live — it's the first thing people read)
- [ ] Pricing clearly stated in description — "free," "freemium," "starts at $X/mo" — ambiguity kills conversions

---

### 1 Week Before

**Community Preparation**
- [ ] Personal network notified in advance: "I'm launching next Tuesday, can you upvote and comment?"
- [ ] Twitter teaser post live — include product name, launch date, and a visual
- [ ] LinkedIn teaser post live if relevant audience
- [ ] Email list notified with launch date and a direct ask to show up and support
- [ ] Relevant Slack and Discord communities notified with launch date (no direct links yet — builds anticipation)

---

### Launch Day

**Timing and First Actions (Strictly In This Order)**
- [ ] Submission live at exactly 12:01 AM PST (Pacific Standard Time — this is when the 24-hour clock starts)
- [ ] First comment posted immediately after listing goes live (your pre-written comment from the prep phase)
- [ ] Personal message sent to top 20 supporters with direct link and a specific ask to upvote and comment
- [ ] Twitter post announcing launch goes live by 6 AM PST — include Product Hunt link
- [ ] LinkedIn post live by 9 AM PST
- [ ] Email blast sent to full list by 8 AM PST — subject line: "We're live on Product Hunt today"

**All-Day Execution**
- [ ] Respond to every single comment on the Product Hunt listing within 30 minutes — the algorithm rewards engagement
- [ ] Monitor comments for negative feedback and address it directly and professionally
- [ ] Post 2-3 progress updates on social ("We hit #5! Thank you — here's what we're working on next")

---

### Post-Launch

- [ ] Thank-you post published the following day tagging key supporters
- [ ] Launch retrospective blog post written within 48 hours (traffic, revenue, lessons learned)
- [ ] Email list update sent with results and a next step (trial offer, discount, new feature)
- [ ] Supporters manually thanked via DM — this compounds for the next launch

---

## Checklist 5: Revenue Infrastructure Checklist

*This is the plumbing. Get it right once and it runs forever. 27 items.*

---

### Payment Setup

**Stripe Configuration**
- [ ] Stripe account fully onboarded: business details, bank account, identity verification complete
- [ ] Tax settings configured in Stripe (Stripe Tax for automatic tax collection, or manual exemption)
- [ ] Payment Link created for each pricing tier — test each one with a real card
- [ ] Pricing page live with all tiers clearly shown, including what is and is not in each tier
- [ ] Annual plan offered at a discount (monthly x 10) — increases LTV and reduces churn
- [ ] Free trial configured if applicable — set in Stripe subscription settings, not manually managed

**Refund and Dispute Handling**
- [ ] Refund policy published and linked from checkout page (reduces chargebacks dramatically)
- [ ] Dispute response process documented — when a chargeback comes, you have 7 days to respond
- [ ] Stripe Radar enabled for basic fraud protection (free, catches most card testing attacks)

---

### Analytics and Revenue Tracking

**Funnel Visibility**
- [ ] Visitor-to-signup conversion tracked in GA4 (or your analytics tool of choice)
- [ ] Signup-to-paid conversion tracked — this is your most important metric
- [ ] Traffic source attribution working — know whether your sales came from Product Hunt, SEO, or cold email
- [ ] Revenue dashboard set up: MRR, churn rate, and new MRR added each week (even a simple spreadsheet works)

**Cohort Analysis Baseline**
- [ ] Week-1 retention tracked: what percentage of new users are still active 7 days after signup?
- [ ] Month-1 churn tracked: what percentage of paying users cancel in month 1?
- [ ] Customer acquisition cost estimated per channel (total channel spend / customers acquired from that channel)

---

### Growth Infrastructure

**Email Capture**
- [ ] Email capture on every page where it makes sense (not just the homepage)
- [ ] Lead magnet available: free checklist, template, or tool that provides immediate value in exchange for email
- [ ] Email sequence set up for new signups: at minimum, a welcome email and a 3-day follow-up
- [ ] Email service provider configured with double opt-in (reduces spam complaints and improves deliverability)

**Upsell and Expansion Revenue**
- [ ] Upsell path exists: clear upgrade flow from free to paid, or from lower tier to higher tier
- [ ] Post-purchase email sequence includes a product recommendation or upsell offer at day 7 and day 30
- [ ] Annual plan upgrade offer sent to monthly users at day 60 (converts at 15-25% when timed correctly)
- [ ] Affiliate program considered — even a simple 30% commission structure with a unique link can multiply distribution

**Directory Listings**
- [ ] Listed on SaaSHub (free, drives long-tail SEO traffic)
- [ ] Listed on AlternativeTo under relevant competitors
- [ ] Listed on BetaList if still in early access phase
- [ ] Listed on appropriate niche directories (AppSumo marketplace, Microlaunch, Fazier — varies by product type)

---

### Legal Minimum Viable Compliance

- [ ] Terms of Service published and linked from footer — include limitation of liability clause
- [ ] Privacy Policy published — must disclose what data you collect and how it's used
- [ ] Cookie consent banner live if you serve EU users and use tracking cookies
- [ ] GDPR: users can request data deletion via email (you don't need a self-serve portal to start)

---

*Total: 135 checklist items across 5 checklists.*

---

## How to Use This Pack

Work through each checklist once per product launch. Most items are one-time setup. A few (cold email QA, SEO audit) are periodic.

Print it or copy it into Notion. Check boxes as you go. Do not skip items because they seem minor — the $1,000 mistakes are always the ones that seemed minor.

If something on a checklist doesn't apply to your product, mark it N/A and move on. The goal is zero unchecked boxes, not perfection.

---

*Priced at $9. If closing one extra customer pays for this 50x over, it was the right buy.*
