# Reddit Posts - Round 2 (30 Posts)
Generated: 2026-03-05
Subreddits: r/SideProject, r/EntrepreneurRideAlong, r/Startup, r/SaaS, r/juststart

---

## POST 1
**Subreddit:** r/SideProject
**Title:** I built a PWA for Muslim prayer tracking during Ramadan. 55KB, works offline. Here's what I learned shipping in 4 days.

**Body:**

Background: I had 3 days before Ramadan started and saw apps in the App Store charging $4.99 for basic prayer time notifications. Figured I could build something better and ship it free.

**What I built:**
- Offline-capable PWA (installs like a native app)
- Auto prayer time calculation based on geolocation
- Streak tracking for consistency
- Push notifications
- Works on iOS and Android

**The 55KB constraint was intentional.** Most prayer apps are 15-20MB. I wanted something that loaded in under 1 second on 3G.

**Tech stack:** Vanilla JS, Service Workers for offline, Adhan.js library for prayer time calculations (MIT license, 40KB itself, incredibly accurate).

**What I got wrong on day 1:**
Prayer times aren't just lat/long. You need the calculation method (MWL, ISNA, Egyptian, etc.) because different Islamic communities use different standards. Got this wrong, shipped it, had users in Qatar telling me times were off by 8 minutes. Fixed in 2 hours.

**Distribution:**
- Posted in r/islam, r/MuslimLounge, r/Muslim
- 3 Facebook Muslim community groups
- 2 WhatsApp group shares from early users

**Week 1 results:**
- 847 installs
- 4.2/5 average rating from 63 reviews
- 0 revenue (free, figuring out monetization)
- 94% retention day 1 → day 2 (prayer routine is sticky)

Biggest lesson: pick a niche where the existing solutions are genuinely bad. The top prayer app in the store hasn't been updated in 18 months and shows ads during fajr prayer. Low bar to clear.

Happy to share the architecture or the Adhan.js implementation if useful.

---

## POST 2
**Subreddit:** r/EntrepreneurRideAlong
**Title:** Month 2 of cold email outreach. Sent 847 emails. 31 replies. 6 calls. 2 clients. Here's the breakdown.

**Body:**

Sharing real numbers because I couldn't find honest data when I started.

**Setup:**
- Instantly.ai for sending ($37/mo)
- Apollo.io free tier for lead sourcing (250 leads/day limit)
- 3 burner domains, each with 2 email accounts
- Warm-up: 3 weeks before first real send

**What I sell:** AI automation setup for local businesses (CRMs, chatbots, follow-up sequences). Average deal: $1,200-$1,800 one-time + $200/mo maintenance.

**Month 1:**
- Sent: 412 emails
- Open rate: 34% (after warm-up, deliverability was good)
- Reply rate: 3.4% (14 replies)
- Calls: 2
- Closed: 0

**Month 2:**
- Sent: 435 emails
- Open rate: 41%
- Reply rate: 3.9% (17 replies)
- Calls: 4
- Closed: 2 ($1,400 + $1,200 = $2,600)

**What moved the needle:**

The sequence that worked in month 2 vs month 1 was changing email 1 from "I help businesses with AI" to a specific problem I'd noticed on their website or Google profile. Example:

Old: "I help dental practices save time with AI automation."

New: "Saw your Google reviews, you've got 47 reviews with 3 people mentioning they never got a callback. That's probably $8-12K in lost appointments per month. I fix exactly this."

Personalization at scale using Clay.com to pull the Google review data automatically. 2 hours to set up the enrichment, saves 20 minutes per prospect manually.

**What doesn't work:**
- Sending to info@ addresses (0 replies in 60 emails)
- Any email over 120 words (reply rate drops 60%)
- Monday morning sends (worst open rates, they're in back-to-back meetings)

**Current pipeline:**
2 proposals out, $3,600 combined. Hoping to close 1.

I'll post month 3 update in April. Ask anything.

---

## POST 3
**Subreddit:** r/SaaS
**Title:** How we validated a B2B SaaS idea in 11 days without writing code

**Body:**

We almost spent 3 months building the wrong thing. Here's the validation process that saved us.

**The idea:** A Slack bot that auto-summarizes meeting transcripts and creates action items in your project management tool.

**Day 1-2: Competitive audit**
Found 6 existing tools (Otter.ai, Fireflies, tl;dv, etc.). Looked like a crowded market. But checked reviews on G2 and Capterra, the #1 complaint across all of them: "summaries are too long and miss the actual decisions." That's a real gap.

**Day 3-4: ICP definition**
We wanted to build for everyone. Forced ourselves to pick ONE segment: engineering managers at Series A-B startups (50-200 employees). They have budget, they have too many meetings, they care about async communication.

**Day 5-7: Fake door test**
Built a Carrd landing page. $0 cost. Copy focused on the specific pain: "Get a 3-bullet summary of every meeting in Slack. The bullets are decisions made, action items assigned, and blockers raised. Nothing else."

Drove traffic with:
- 3 posts in r/devops and r/ExperiencedDevs (not sales-y, just "we're exploring this problem, would you use it?")
- $200 in LinkedIn ads targeting engineering managers

Results: 89 sign-ups in 72 hours. 23 people put in their work email (higher intent). We emailed all 23.

**Day 8-10: Customer discovery calls**
Booked 11 calls. Asked: How do you handle meeting notes now? What breaks about it? What would a perfect solution look like?

Key finding: 8 of 11 people said they'd pay for it. But not as a standalone tool. They wanted it to push directly to Linear or Jira, not just Slack. The Slack piece was actually secondary.

**Day 11: Decision**
Pivoted the core value prop before writing a line of code. Built Linear integration first, Slack notification second.

This would have taken us 6 weeks of wrong building to discover if we'd just started coding.

Now 3 months in, $2,800 MRR, 19 paying customers. Still early but product-market fit feels real.

---

## POST 4
**Subreddit:** r/juststart
**Title:** I had $0 and no audience. Here's the exact sequence I used to make my first $200 online.

**Body:**

Not a flex. This is a playbook for anyone starting from nothing.

**My situation in October 2025:**
- No email list
- No social following worth mentioning (83 Twitter followers)
- No product
- $0 budget for ads

**Step 1: Pick the problem you've already solved.**

I'd spent 2 years figuring out how to set up automated bookkeeping for freelancers using free tools (Wave + Zapier free tier + Google Sheets). It wasn't glamorous but I'd answered the same questions in 3 different freelancer Facebook groups 30+ times.

**Step 2: Build a Gumroad product in a day.**

"The Zero-Cost Freelancer Bookkeeping System", a Google Sheets template with a 15-page written guide. Made it in 8 hours on a Saturday.

Priced it at $17. Not $97, not $7. $17 is impulse-buy territory but still signals value.

**Step 3: Soft launch in communities where you've already helped people.**

Posted in 3 Facebook groups where I'd been active for 6+ months. Not "buy my thing", posted the full system as a free post, then mentioned at the bottom: "if you want the done-for-you template and step-by-step guide, I made it into a $17 product on Gumroad."

**Step 4: Wait 72 hours.**

First sale came at hour 14. Second at hour 31. By hour 72: 9 sales = $153.

**Step 5: One Reddit post.**

Posted the full method (not the product, the actual method) in r/freelance. Mentioned at the bottom that I'd packaged it into a guide if anyone wanted it. 4 more sales over a week = $68.

**Total: $221 in first 2 weeks. Zero ad spend.**

The product still sells 2-3 copies per month with zero marketing. It's not life-changing money. But it proved the model works, which gave me the confidence to build more.

Currently at $1,100/month across 5 digital products. Same playbook, different problems.

---

## POST 5
**Subreddit:** r/Startup
**Title:** We got 400 beta users in 3 weeks without a press mention or influencer. Here's the distribution playbook.

**Body:**

Our app is in a competitive space (productivity + habit tracking). No VC backing. No press contacts. No budget for influencer deals.

Here's exactly what worked to get 400 active beta users.

**Week 1: Reddit (200 users)**

Posted in 8 subreddits with "show me what you're working on" or "feedback on my side project" culture. The trick: don't post the product. Post the problem you're solving and ask if people relate.

Our post: "I've tried every habit app and they all fail me in the same way, they celebrate streaks but don't help me understand WHY I broke the streak. Anyone else?" → 340 upvotes, 82 comments, 127 DMs asking for early access.

Replied to every comment personally. Converted 60% of DMs to beta sign-ups.

**Week 1.5: ProductHunt "Coming Soon"**

Set up a PH Coming Soon page with an email capture. Not launching yet, just collecting interest. Got 47 followers organically from PH's discovery feed.

**Week 2: Direct Twitter outreach (not spam)**

Found 200 accounts who tweet about productivity tools using Twitter's advanced search. Replied to their recent tweets with genuine comments about what they said. No mention of our product. Just being a person.

After 3+ interactions, 40 people responded when we mentioned the beta in a DM. 28 joined.

**Week 2.5: Facebook Groups**

6 productivity and self-improvement groups, 1,000+ members each. Posted about our beta. NOT as an ad, as "we built this thing and want feedback from serious people." Got 89 sign-ups.

**Week 3: Small newsletter sponsorship**

Found a newsletter with 4,200 subscribers in the personal development space. Paid $85 for a sponsor slot. Got 31 sign-ups. $2.74 per user. Reasonable.

**Total: 412 beta sign-ups in 3 weeks. Paid $85.**

Currently converting to paid at 11%. Every distribution channel is trackable.

---

## POST 6
**Subreddit:** r/SideProject
**Title:** I automated my entire freelance invoicing workflow in one weekend. Here's the setup (no monthly fees).

**Body:**

I was spending 45 minutes per week on invoicing. Client follows up, I update spreadsheet, generate PDF, send email. Repeat.

Built an automated system in a weekend. Now it takes me 3 minutes. Zero monthly cost.

**Stack:**
- Google Forms (free), client details intake
- Google Sheets (free), job log and status tracking
- Google Apps Script (free), automation glue
- Gmail (free), sending invoices

**How it works:**

1. New job? Fill out a Google Form (client name, hours, rate, description). Takes 90 seconds.
2. Apps Script watches the sheet for new rows.
3. Pulls data, generates HTML email with invoice formatting.
4. Auto-calculates totals, adds payment terms, inserts bank details.
5. Sends to client automatically.
6. Logs to a "pending payment" tab.
7. When I mark invoice as "paid", moves it to archive and updates running revenue tracker.

**The Google Apps Script that handles step 2-6 is ~80 lines of code.** I can share it if people want.

**What I stopped paying for:**
- FreshBooks ($17/mo, cancelled after 3 years)
- Notion invoicing template I never actually used

**Limitations:**
- Not great for complex invoices with line items (mine are always time-based so it works)
- Doesn't handle VAT automatically (I'm in the US, not a problem)
- No client portal (clients receive a clean HTML email, not a branded portal)

**Time saved:** 42 minutes per week. 36 hours per year.

Sharing the full script in comments. Happy to help customize it.

---

## POST 7
**Subreddit:** r/EntrepreneurRideAlong
**Title:** 90 days into selling AI automation to local businesses. Revenue, what works, what kills deals.

**Body:**

Started in January 2026. Here's an honest report card at 90 days.

**Revenue:**
- Month 1: $0 (setup, learning, 0 closes)
- Month 2: $2,600 (2 clients)
- Month 3: $5,800 (4 clients, 1 upsell)
- Retainer MRR: $600/mo (3 clients x $200)
- Total 90-day revenue: $8,400

**Deal breakdown:**
- Dental practice: $1,200 setup (missed appointment automation) + $200/mo
- Plumber: $900 setup (Google review automation) + $200/mo
- Chiropractor: $2,400 setup (full CRM + follow-up sequences)
- HVAC company: $1,800 setup (lead qualification bot) + $200/mo
- Law firm: $0 (lost to "we'll think about it", never heard back)

**What works:**

Specificity wins every time. "I help local businesses save time" = 0 interest. "I automate the Google review request you're supposed to send after every appointment but never do" = 40% response rate.

Free audit as the opener. I spend 20 minutes researching their Google profile, website, and any Yelp/Facebook presence. Show them 3 specific automation opportunities in the first call. No pitch, just analysis.

**What kills deals:**

- Using the word "AI" in the opener. Triggers skepticism. I say "automation" instead.
- Talking price before pain. If they don't feel the problem, the price is always wrong.
- Complex SOWs. My proposals are now 1 page: problem, solution, price, timeline. Lost 2 deals to over-complicated proposals.

**What I'd do differently:**

Productize faster. I'm still doing everything custom, which means each project is different and slower. Building 3 standardized packages for dental, legal, and home services this month.

**Current pipeline:** 6 active leads, $7,200 in proposals.

---

## POST 8
**Subreddit:** r/SaaS
**Title:** 6 months of user interviews taught me the one question that predicts churn before it happens.

**Body:**

We have a B2B SaaS product in the project management space. Small team (3 people). $18K MRR. Churn was killing us at month 4-6.

After 40+ user interviews, I found the one question that predicts churn 6-8 weeks before it happens:

**"How often does your team talk about [product name] in team meetings?"**

Users who mention it "weekly or more" churn at 3%. Users who say "rarely" or "never" churn at 67%.

This sounds obvious in retrospect. But we were measuring login frequency, feature usage, support tickets. None of those predicted churn as cleanly as this single question about internal communication.

**Why this works:**

When a product becomes part of how your team talks, it's embedded. When nobody mentions it, it's on the bubble.

**What we did with this:**

Built an in-app survey that fires at day 45 (before month 2 renewal). One question. If they answer "rarely" or "never," we trigger a success sequence: personal email from me, offer a 30-minute strategy call, send the "team adoption playbook" PDF we created.

**Results (4 months of data):**

- 34 users triggered the "at-risk" segment
- 19 accepted the strategy call
- 15 of 19 are still customers 3 months later (79% save rate)
- 15 users who didn't take the call: 11 churned (73% churn)

Saved ~$3,400 in MRR we would have otherwise lost.

The question works because it measures social adoption, not individual usage. Software lives or dies by team adoption, not individual power users.

---

## POST 9
**Subreddit:** r/juststart
**Title:** The cheapest possible tech stack that can run a real business (I've tested it for 14 months)

**Body:**

I see a lot of posts about expensive stacks. Here's what I've been running for 14 months at $0-$47/month depending on the month.

**What I needed to support:**
- Lead capture
- Email marketing
- Simple CRM
- Digital product delivery
- Landing pages
- Basic analytics

**The stack:**

| Tool | Free Tier | Cost |
|------|-----------|------|
| Carrd | Up to 3 sites | Free |
| Beehiiv | Up to 2,500 subs | Free |
| Notion | Personal use | Free |
| Gumroad | Up to $10K/year | Free (9% fee) |
| Tally.so | Unlimited forms | Free |
| Cal.com | Unlimited bookings | Free |
| Plausible | First 30 days | Free → $9/mo |

**Total: $0/month until $10K product revenue**

At that point Gumroad becomes more expensive than alternatives, so switch to LemonSqueezy (same model, lower fees above $10K). Or just pay the Gumroad fee, it's still cheaper than Stripe + everything else.

**What I had to pay for eventually:**
- Plausible: $9/mo (after 30-day trial). Worth it. Google Analytics is a mess.
- Custom domain: $12/year (not monthly)
- Beehiiv paid: $42/mo at 3,000 subs. Upgrade then, not before.

**What I don't use and you probably don't need:**
- Fancy CRM (Notion handles it)
- Webflow (Carrd is good enough for lead gen)
- Any email tool with automations before 500 subscribers (premature complexity)

14 months, 3 digital products, $4,100 in revenue. Spent maybe $200 total on tooling.

---

## POST 10
**Subreddit:** r/SideProject
**Title:** My app hit a wall at 200 users. Here's the dead-end growth channels vs. the one that actually scaled.

**Body:**

Built a web app for tracking freelance client history and red flags. Got to 200 users fairly easily. Then hit a wall.

**Channels that didn't scale:**

**Reddit posts:** Got 150 users from 3 posts. But diminishing returns fast. Can't post the same thing twice, and finding new angles got exhausting.

**Twitter/X:** Posted consistently for 6 weeks. 40 followers, 22 conversions. Time-to-return ratio is brutal unless you already have an audience.

**ProductHunt launch:** 84 upvotes, 47 new users in one day. Then nothing. PH doesn't drive long-tail traffic for free tools.

**What actually scaled:**

**SEO targeting problem-specific queries.**

Users search "how to check if a client is a scammer before taking a job." I wrote a 1,200-word post on exactly that, mentioned the tool once, added a CTA at the bottom. Took 3 months to rank, then started driving 40-60 visits/day. 8% conversion to sign-up.

Now: 14 posts targeting different variations of the same problem. 400 organic visitors/month. 30-35 new sign-ups/month, passively.

**The lesson:**

Reddit is great for the first 100-300 users. It's a burst channel, not a compounding one. SEO is slow but compounding. Content that ranks in month 3 still converts in month 18.

If your tool solves a specific problem, there are people actively searching for that problem right now. Write for them first.

---

## POST 11
**Subreddit:** r/EntrepreneurRideAlong
**Title:** What happened when I raised prices 3x without changing anything else

**Body:**

In November 2025, I raised the price on my Gumroad product from $27 to $97. Changed nothing about the product.

I expected a big drop in sales. What actually happened surprised me.

**Before ($27):**
- 12 sales/month average
- Monthly revenue: $324
- Refund rate: 8% (people bought impulsively)
- Average review score: 3.9/5

**After ($97, month 1):**
- 6 sales
- Monthly revenue: $582
- Refund rate: 2%
- Average review score: 4.6/5

**After ($97, month 3):**
- 9 sales
- Monthly revenue: $873
- Refund rate: 1%
- Average review score: 4.8/5

Revenue went up 2.7x. Volume went down 25%. Quality of customers went up dramatically.

**Why the reviews improved:**

At $27, people bought on impulse and then felt let down when it required real effort to implement. At $97, only people serious about the problem bought. They implemented it, it worked, they left good reviews.

**Why refunds dropped:**

Same logic. Impulse buyers refund. Intentional buyers don't.

**What I changed to justify the new price (minimal work):**

- Added a 20-minute Loom walkthrough video
- Reformatted the PDF with better design (Canva, 3 hours)
- Added a "troubleshooting FAQ" section based on support emails I'd gotten

That's it. Same core content.

3x price increase. 2.7x revenue increase. Higher customer satisfaction. More time freed up from support.

Price is part of the product.

---

## POST 12
**Subreddit:** r/SaaS
**Title:** We lost 3 enterprise deals to the same objection. Here's how we fixed it.

**Body:**

We're a small SaaS (4 people). Product is good. But kept losing deals to larger companies in the $500-$2,000/month tier.

The objection, verbatim: "We love it but we need to know the company will still be around in 2 years."

This is the startup trust gap. Real problem, and it was costing us deals.

**What we tried that didn't work:**

- Emphasizing our team background and track record
- Offering longer trials
- Showing investor interest (we don't have VC, just revenue)

**What actually worked:**

**Escrow code commitment.** We partnered with Escrow.com to hold our source code in escrow. If we shut down, clients get the code. One legal document, one-time setup cost.

**The announcement post on LinkedIn** explaining what we did, why we did it, and what it means for customers got more engagement than anything we'd posted in a year.

**Result:**
- Closed the next 2 enterprise deals that mentioned the "will you survive" concern
- Added it to our pricing page as a feature
- Quoted explicitly in one new enterprise contract

The escrow setup cost us $400 and 8 hours of legal back-and-forth. The deals it helped close totaled $18,000 in ARR.

Sometimes the objection is real and the fix is to actually solve the problem, not to handle the objection better.

---

## POST 13
**Subreddit:** r/juststart
**Title:** First $1K month. Here's what it was (not passive income, I'm sorry).

**Body:**

January 2026: Made $1,043 online for the first time. Here's the breakdown.

- $490: Freelance automation setup (2 Fiverr clients, custom chatbot builds)
- $306: Gumroad digital products (Google Sheets templates, sold 18 copies across 3 products)
- $247: Affiliate commissions (Beehiiv affiliate program, 3 referrals)

**Total: $1,043**

Not passive. 38 hours of work. That's $27.45/hour, which is better than what I was making at my part-time job ($18/hr) but not "4-hour work week" territory.

**What I spent:**
- Instantly.ai: $37 (cold email for the Fiverr clients)
- Canva Pro: $13 (product design)
- Domain renewal: $12
- Total spend: $62

**Net: $981**

**What I did right:**

Started with services (highest margin, fastest money), used the revenue to validate product ideas, then built products from the questions clients asked. The Google Sheets templates came directly from a client saying "can you make this into something I can give my team?"

**What's next:**

Trying to get $1K MRR in passive (templates + affiliates) so services become optional. Currently at $306 MRR from passive. Need 3x growth.

Sharing because I spent 6 months reading success stories that were either fake or 10 years in the making. This is month 3, it's messy, and it's real.

---

## POST 14
**Subreddit:** r/SideProject
**Title:** Built a micro-SaaS for a niche I'm not in. Lessons from 6 months of building for someone else's problem.

**Body:**

I'm not a real estate agent. But I built a tool for them.

The tool: Automated open house follow-up sequences. Visitors sign in at an open house, get a personalized text + email sequence over the next 2 weeks.

**Why this niche:**

I was helping a friend who's a realtor and watched her manually email 40 people after every open house. She had a spreadsheet, a Gmail account, and 3 hours of post-Sunday work every week. There was no good, cheap solution that handled this specific workflow without buying into a $200/month CRM.

**Building without domain expertise:**

I got it wrong in obvious ways. Open house visitors aren't leads, they're "suspects." The follow-up has to be educational, not salesy, or agents get flagged as spammers. I didn't know this. First 10 beta users told me the sequences felt like car dealership emails.

Rewrote the copy from "I'd love to schedule a showing" to "Here's what I noticed about the market in your price range." Completely different.

**Lessons:**

1. Build WITH someone in the niche, not FOR them. My realtor friend was a co-founder in everything but title.
2. The business logic you can't see from the outside is where you'll fail. Ask "what would make this feel wrong?" in every interview.
3. Pricing in real estate is weird. Agents either pay nothing or pay a lot. $29/month felt too cheap (skepticism about quality). $79/month felt fine.

**Current stats (month 6):**
- 23 paying users
- $79/month each
- $1,817 MRR
- 87% retention at month 3

---

## POST 15
**Subreddit:** r/EntrepreneurRideAlong
**Title:** I tracked every hour I worked for 60 days. The data changed how I run my business.

**Body:**

Used Toggl Track to log everything for 60 days. January + February 2026.

**Total hours worked: 412 hours across 60 days (6.9 hours/day average)**

**How I actually spent those hours:**

| Activity | Hours | % of Time |
|----------|-------|-----------|
| Client work (billable) | 148h | 35.9% |
| Content creation | 87h | 21.1% |
| Cold outreach | 63h | 15.3% |
| Admin (invoices, emails, scheduling) | 44h | 10.7% |
| Product development | 38h | 9.2% |
| Strategy/planning | 22h | 5.3% |
| Learning/research | 10h | 2.4% |

**Revenue generated in those 60 days: $6,200**

**Effective hourly rate: $15.05/hour**

This was horrifying to see.

**The problem areas:**

Admin (10.7% of time) generated $0 directly. Content creation (21.1%) generated maybe $400 in affiliate income. Cold outreach (15.3%) generated $2,600 in new client revenue.

**What I changed starting March 1:**

- Automated invoicing (saved ~3 hours/week)
- Batch content creation (4 hours Sunday instead of 30 minutes every day)
- Hired a $12/hour VA for email management and scheduling (5 hours/week)

**Target for next 60 days:**

Get billable hours to 50%, admin to under 5%, content to under 15%. If revenue stays the same and I work 10% less, effective rate goes to $22/hour. That's the goal.

Real data makes better decisions than gut feelings.

---

## POST 16
**Subreddit:** r/SaaS
**Title:** How we cut our churn from 9% to 3% monthly in 4 months. Not by improving the product.

**Body:**

Our SaaS product hadn't changed. What changed was our onboarding.

**The problem:**

Monthly churn was 9%. That meant we needed 9% MRR growth just to stay flat. It was a treadmill.

We asked every churned user the same exit survey question: "What would have made you stay?" Expected to hear about features. Instead: "I never figured out how to [core use case]."

**Translation:** People were churning because they couldn't use what they'd paid for.

**What we changed:**

**Week 1 onboarding overhaul:**

Old flow: Sign up → dashboard → figure it out.

New flow: Sign up → 3-question wizard → personalized setup → forced first action → "you did it" moment in 8 minutes.

The "forced first action" is the key. We didn't let users reach the empty dashboard state. They had to complete one real task before seeing the full UI.

**Week 3: Success email sequence**

Day 1, 3, 7, 14, 30 emails. Not feature announcements. Use case tutorials with 2-minute Loom videos. "Here's how a user like you did X."

**Week 6: Success check-in call**

For accounts paying over $100/mo, personal email from a team member at day 14 offering a 20-minute call. Booked 31% of the segment. Conversion to long-term retained customers: 84%.

**Results (4 months):**

Month 1 after changes: 7% churn. Month 2: 5%. Month 3: 3.5%. Month 4: 3.1%.

At $40K MRR and 3% churn instead of 9%, we're retaining ~$2,400/mo more in existing revenue without acquiring a single new customer.

Onboarding is your most important marketing.

---

## POST 17
**Subreddit:** r/juststart
**Title:** The "fake it till you make it" moment that got me my first real client

**Body:**

I want to tell this story honestly because every version of it online is sanitized.

I had built exactly 0 client projects. I had 3 tutorial projects on my GitHub. I was applying to freelance gigs on Upwork and getting rejected consistently.

**The pitch that worked:**

A small e-commerce store posted on r/entrepreneur asking if anyone could help them set up abandoned cart email automation. I responded with a detailed breakdown of exactly how I'd do it: Klaviyo, the 3-email sequence structure, timing, subject line strategy, what metrics to optimize.

I wrote it like I'd done it 40 times. I had not done it once.

They hired me for $400.

**The "fake it" part:** I presented expertise I had in theory but not in practice.

**The "make it" part:** I then spent 20 hours the week before the project learning Klaviyo inside out. Watched every tutorial, set up a test account with fake data, documented my process. When I showed up to the project, I knew the tool.

**The project took 11 hours. Client was thrilled.** Said it was the most detailed setup they'd seen.

**Why I'm not embarrassed about this:**

I wasn't lying about my capability. I was lying about my experience. The capability was real, I just hadn't applied it yet. If you understand the theory deeply enough to explain it clearly, you can usually execute it.

**What I'd caution against:**

Faking expertise you genuinely don't have in ways that could hurt the client. Don't offer medical advice you don't have. Don't offer legal strategy you don't understand.

But marketing, automation, content strategy, web development? Learn it well enough to plan it, then learn to build it while you build it.

---

## POST 18
**Subreddit:** r/SideProject
**Title:** 3 small tools I built to replace $180/month of SaaS subscriptions

**Body:**

I had subscription creep. Cancellation day: discovered I was paying for tools I'd forgotten about.

Spent 2 weekends building replacements for 3 of them.

**Tool 1: Link-in-bio page (replaced Later's link page at $25/mo)**

Simple HTML file, hosted on Cloudflare Pages (free). Links, profile pic, optional analytics via Plausible ($9/mo but split across everything I host).

Build time: 4 hours. Annual saving: $300. Looks better than Later's template.

**Tool 2: Social post scheduler (replaced Buffer at $18/mo)**

Python script that reads from a Google Sheet (scheduled posts with date, platform, content columns) and uses the Twitter/X API + Instagram Graph API to post. Runs via cron job on a $4/mo DigitalOcean Droplet.

Limitations: No visual calendar, no analytics, no team features. For a solo creator who can read a spreadsheet, this is fine.

Build time: 8 hours. Annual saving: $216.

**Tool 3: Link click tracker (replaced Bitly at $35/mo)**

PHP script on the same $4/mo droplet. Redirects links, logs clicks to a CSV with timestamp and user agent. Built a simple dashboard with Chart.js.

Missing: geo-data (need a paid IP API), custom domains (I don't need them).

Build time: 6 hours. Annual saving: $420.

**Total saving: $936/year. Total build time: 18 hours.**

At my consulting rate: 18 hours isn't worth it. But these tools run indefinitely. At year 2, ROI is very real.

I don't recommend building everything. But if a tool is simple, your needs are stable, and the subscription is ongoing, build it.

---

## POST 19
**Subreddit:** r/EntrepreneurRideAlong
**Title:** Update: I quit my job 6 months ago. Here's the real financial picture.

**Body:**

People asked me to post the full financial update when I hit 6 months. Here it is.

**The setup:** Left a $72K/year marketing job in September 2025 to build digital products and consulting full-time.

**Revenue by month:**

| Month | Revenue | Main Sources |
|-------|---------|--------------|
| Sep | $1,240 | Consulting (old client relationship) |
| Oct | $890 | Products $340, Consulting $550 |
| Nov | $2,100 | Products $600, Consulting $1,500 |
| Dec | $1,650 | Products $850, Consulting $800 (slow month) |
| Jan | $3,200 | Products $900, Consulting $2,300 |
| Feb | $4,100 | Products $1,100, Consulting $3,000 |

**6-month total: $13,180**

My old job would have paid $36,000 in the same period. So I'm at 37% of my previous income.

**Costs:**

- Software/tools: $190/mo average
- Health insurance: $340/mo (this is the killer)
- Co-working 2x per week: $80/mo
- Home office expenses: ~$60/mo

**Monthly burn: ~$670 in business costs + ~$3,200 personal expenses = $3,870/month**

February was the first month I covered burn completely. 5 months in the hole before that.

**What I got wrong:**

1. Health insurance cost. I knew it intellectually but it still hurt.
2. Sales cycle length. Consulting deals take 3-6 weeks to close. Cash flow is lumpy.
3. Undervaluing my time in months 1-2. Took $50/hr projects. Now minimum is $125.

**What I'd tell someone considering this:**

Have 9 months of expenses saved. 6 months is not enough. Have one client committed before you quit if possible. And price higher than feels comfortable, you can always negotiate down.

---

## POST 20
**Subreddit:** r/SaaS
**Title:** We launched at $9/mo. Raised to $29. Then $49. Here's what each price point taught us.

**Body:**

Price discovery is the most underrated part of building SaaS. We ran 18 months of pricing experiments. Here's the data.

**$9/month (months 1-4):**
- Conversion rate: 22% trial-to-paid
- MRR at end: $2,700
- Avg support tickets per user: 3.4/month
- Churn: 11%/month
- User profile: Solopreneurs, students, people trying it on a whim

**$29/month (months 5-10):**
- Conversion rate: 14% trial-to-paid
- MRR at end: $8,700
- Avg support tickets per user: 1.9/month
- Churn: 7%/month
- User profile: Small teams, serious operators, occasional SMB

**$49/month (months 11-18):**
- Conversion rate: 11% trial-to-paid
- MRR at end: $19,600
- Avg support tickets per user: 1.1/month
- Churn: 4%/month
- User profile: Teams, consistent business use cases

**The pattern:**

Each price increase cut conversion but raised quality. Support burden dropped by 3x. Churn dropped by 2.75x. Revenue grew 7x.

At $9, we were subsidizing casual users and drowning in support. At $49, we have a real business with users who actually care about outcomes.

**The counter-intuitive lesson:**

Raising prices doesn't just increase revenue. It filters for better customers who use the product more, complain less, and stay longer. The economics compound in your favor at every level.

Current experiment: Annual plan at $399 (saves users $189). Conversion to annual: 34%. That changes cash flow dramatically.

---

## POST 21
**Subreddit:** r/juststart
**Title:** The only productivity system that's worked for me as a solo founder (and why everything else failed)

**Body:**

I've tried GTD, Notion dashboards, time blocking, Pomodoro, weekly reviews, OKRs. Most lasted 2 weeks.

Here's the only thing that's stuck for 8 months.

**The system: 1 daily priority + weekly anchor**

Every morning: Write 1 thing that makes the day a success. Not a task list. One outcome.

"Get a signed contract from Client X."
"Ship the landing page."
"Make 30 outreach calls."

Then do that first. Before email, before Slack, before Reddit.

**Weekly anchor:** Every Sunday, 20 minutes. One question: "What would make next week a success?" Write it down. That becomes the filter for everything else.

**Why everything else failed:**

- GTD: Too much maintenance. Spent more time managing the system than doing work.
- Notion dashboards: Beautiful, never actually used them to decide what to work on.
- Time blocking: Works great until the day goes sideways. Then the whole system breaks.
- Weekly reviews: Takes an hour, becomes a guilt trip, eventually skipped.

**Why this works:**

It's almost too simple to fail. One line in the morning. 20 minutes on Sunday. Nothing to maintain.

The question "did I do the 1 thing?" is binary. Much easier than evaluating a task list.

**What I pair it with:**

Time tracker (Toggl, free), not for accountability, for data. Helps me see if my time matches my priorities.

---

## POST 22
**Subreddit:** r/SideProject
**Title:** I tracked which distribution channels drove actual paying customers (not just signups). Results surprised me.

**Body:**

Built a simple source tracking setup. UTM parameters on every link, tagged in our database. 6 months of data.

**Signups by source:**

| Source | Signups | % |
|--------|---------|---|
| Reddit | 847 | 34% |
| Twitter/X | 612 | 24% |
| ProductHunt | 441 | 18% |
| Direct/organic | 287 | 11% |
| Newsletter | 198 | 8% |
| LinkedIn | 107 | 4% |

Reddit dominated signups. But then I looked at paying customers:

**Paying customers by source:**

| Source | Paying | Conversion | LTV |
|--------|--------|------------|-----|
| Newsletter | 31 | 15.7% | $284 |
| Direct/organic | 38 | 13.2% | $247 |
| LinkedIn | 12 | 11.2% | $312 |
| Twitter/X | 52 | 8.5% | $186 |
| Reddit | 48 | 5.7% | $143 |
| ProductHunt | 19 | 4.3% | $98 |

Newsletter converts at 15.7% with $284 LTV. Reddit converts at 5.7% with $143 LTV.

**The math:**

198 newsletter signups × 15.7% × $284 = $8,824 LTV
847 Reddit signups × 5.7% × $143 = $6,909 LTV

More signups from Reddit, significantly less revenue.

**What I changed:**

Stopped optimizing for Reddit virality. Started building the newsletter harder. Added 3 newsletter-specific posts per month instead of spraying Reddit.

**The lesson:**

Don't optimize for the channel that gets the most signups. Optimize for the channel that converts your signups into paying customers.

---

## POST 23
**Subreddit:** r/Startup
**Title:** Our Series A pitch failed. Here's the feedback that changed how we think about the business.

**Body:**

We pitched 14 VCs over 8 weeks. Passed on by all 14. One partner gave us detailed feedback that was the most useful thing that happened to us that year.

This is not a fundraising-is-hard story. This is a "what we learned from rejection" story.

**The feedback:**

"Your product is solving a real problem. The problem is your market size story. You're in a niche that tops out at $50M ARR, not $500M. We can't build a fund return on that. But you probably can build a great business."

We'd been trying to pitch ourselves as a platform play. We weren't. We were a point solution.

**What we changed:**

Stopped trying to be a platform. Doubled down on the niche. Raised pricing to reflect the specific value we deliver. Focused entirely on profitability.

**6 months later:**

- MRR: $67K (was $41K at pitch)
- Monthly burn: $38K (was $31K at pitch, scaled team)
- Months of runway: 11 months of cash on hand
- Monthly profit margin: positive for first time, ~$29K/month
- Net Revenue Retention: 118%

We're on a path to $1M ARR without Series A.

The VC said "you probably can build a great business." He was right. Just not a venture-scale business. That distinction matters.

Not every company should raise VC. Some companies should just be profitable.

---

## POST 24
**Subreddit:** r/juststart
**Title:** 6 questions I ask before building anything new (after building 3 things nobody wanted)

**Body:**

I built 3 things in my first year that got 0 paying customers. Here's the checklist I run now before starting.

**Question 1: Can I find people actively complaining about this problem?**

Not "would people want this." Find real people, in real forums, saying "I hate that I have to do X" or "does anyone know a tool for X?" If you can't find them in 30 minutes of searching, the problem might not be urgent enough.

**Question 2: What are people doing right now to solve this problem?**

The worse the current solution, the better your opportunity. If people are using spreadsheets or manual processes for something obviously automatable, that's a signal. If people are already using a well-funded competitor with good reviews, rethink the differentiation.

**Question 3: Who specifically am I building for?**

"Small business owners" is not an answer. "Freelance graphic designers who work with 3-5 clients simultaneously and invoice manually" is an answer. The more specific, the better you'll understand their exact workflow.

**Question 4: Can I charge for this before I build it?**

Stripe + a Google Form or a Typeform is enough to collect payment. If you can't sell it before it exists, it's harder to sell after. Pre-selling isn't always possible, but if it is, do it.

**Question 5: What's my distribution strategy?**

Where do these people hang out? How will I reach them? "Post on Reddit" is not a strategy. "Post in these 4 specific subreddits where this problem comes up regularly, and here's my content angle" is a strategy.

**Question 6: What does success look like in 90 days?**

Not revenue goals (those are lagging indicators). Leading indicator goals: X user interviews, Y signups, Z paying customers, or "I've learned the product doesn't work and I should pivot."

These 6 questions take 2 hours. They've saved me months.

---

## POST 25
**Subreddit:** r/SaaS
**Title:** I analyzed 200 SaaS pricing pages. These 8 patterns predict higher conversion.

**Body:**

Spent 3 weeks analyzing pricing pages across 200 SaaS products (B2B, $20-$500/month range). Here's what the high-converting pages had in common.

**Pattern 1: Anchoring with 3 tiers, not 2.**

2 tiers creates an either/or choice. 3 tiers gives users a "Goldilocks" option. 94% of products with strong conversion (>15% trial-to-paid) had exactly 3 tiers.

**Pattern 2: Middle tier highlighted.**

86% of products with clear "recommended" or highlighted middle tiers reported higher average revenue per user. People use the highlight as a social cue.

**Pattern 3: Annual pricing shown by default.**

Products that defaulted to annual (with monthly toggle) had 28% higher average subscription length in public case studies.

**Pattern 4: No free tier when competing on quality.**

Products in quality-first positioning (not volume) that offered a free tier had 40% lower conversion to paid than those offering trials only. Free tiers commoditize.

**Pattern 5: FAQ section that addresses objections, not features.**

High-converting pricing FAQs answered "Is this safe for X?" and "What happens to my data if I cancel?" Low-converting FAQs explained features already listed above.

**Pattern 6: Single CTA per tier.**

Pages with 2+ CTAs per tier (e.g., "Start Free" and "Contact Sales") had lower conversion than pages with one action per tier.

**Pattern 7: Social proof specific to outcome, not brand.**

"Saved us 5 hours/week" outperforms "Great product!" Specific outcomes beat general endorsements.

**Pattern 8: Money-back guarantee visible without scrolling.**

Products with guarantees above-the-fold on pricing pages had notably higher conversion. The guarantee reduces risk at the decision moment.

These patterns won't save a bad product. But if your product is solid, most of these are 1-hour fixes.

---

## POST 26
**Subreddit:** r/EntrepreneurRideAlong
**Title:** I hired a $10/hour VA for 10 hours/week. 60-day update.

**Body:**

Hired on Upwork. Here's the honest review.

**What I pay:** $10/hour, 10 hours/week = $100/week = $400/month

**What I hired for:** Email management, research tasks, data entry for lead lists, scheduling, basic customer support responses.

**The first 2 weeks (bad):**

Expected them to figure out my workflows independently. Rookie mistake. Spent 6 hours training and still had wrong outputs. Considered canceling.

**What changed at week 3:**

Built SOPs. Literally a 1-page Google Doc for every task: "How to respond to a support email" with 5 template answers. "How to research a company" with exact steps and fields to fill. "How to format a lead list" with screenshot examples.

After SOPs: work quality went to 85-90% of what I'd do myself. For non-critical tasks, 85% is fine.

**After 60 days:**

Hours per week I've reclaimed: ~8 hours
Tasks fully offloaded: email triage, lead list building, scheduling, routine support responses, social media comments monitoring
Tasks I still do myself: anything requiring judgment, content creation, client calls

**ROI calculation:**

$400/month → freed up 32 hours/month. At $100/hour consulting rate, that's $3,200 of my time freed. Even if I only convert 25% of that freed time to billable work, that's $800. Still 2x the cost.

But the real value isn't money. It's mental load. Not thinking about email triage is worth more than $400 to me.

**What I'd do differently:** Hire for a specific role, not "general assistant." Better to hire 2 specialists at 5 hours each than 1 generalist at 10.

---

## POST 27
**Subreddit:** r/SideProject
**Title:** What 400 app reviews taught me about what users actually want vs. what I thought they wanted

**Body:**

Spent 2 days reading every review of my habit tracking app. 400 reviews across App Store and Google Play. Here's what the data actually says.

**What I thought users wanted (based on feature requests in support emails):**
1. More analytics and charts
2. Social features (share streaks with friends)
3. Apple Watch integration
4. More notification customization

**What the reviews actually say (coded by sentiment and mention frequency):**

Top positive mentions:
1. "Simple" / "not overwhelming", 127 mentions
2. "Actually reminds me" (notifications work), 89 mentions
3. "Design is clean", 67 mentions
4. "Fast to open", 54 mentions

Top negative mentions:
1. "Crashes on [specific phone model]", 43 mentions
2. "Lost my streak data", 31 mentions
3. "Notifications stop working after iOS update", 28 mentions
4. "Can't edit past days", 22 mentions

**The gap:**

Users love it for being simple and fast. Users hate it for being buggy and losing data.

Support emails asked for analytics and social features. Reviews reveal the real problems: stability and reliability.

**What I built next:**

Fixed crash on Samsung A-series (took 3 days to find the bug). Added data export/backup. Fixed notification reliability on iOS 17.

Didn't build the analytics dashboard. Didn't build social features.

**Result:** 1-star reviews dropped from 18% to 7% over 3 months. Overall rating went from 3.8 to 4.4.

Read your reviews. Not your feature requests. They're different signals.

---

## POST 28
**Subreddit:** r/Startup
**Title:** The Minimum Viable Distribution test, how we validate distribution before building

**Body:**

We wasted 6 months building a product with no distribution plan. Now we validate distribution first.

**The MVD test:**

Before we build, we ask: Can we get 50 people to take a meaningful action (sign up, join waitlist, schedule a call) in 2 weeks with $0 or under $200?

If yes: we have a distribution hypothesis worth testing.
If no: either the audience doesn't exist, the problem isn't urgent, or our messaging is wrong. Figure out which one before building.

**How we run it:**

1. Build a Carrd landing page in 2 hours. Problem statement, solution sketch, email capture or waitlist.
2. Identify 3-5 specific channels where our target user is active.
3. Run 5-10 pieces of content per channel over 2 weeks (Reddit posts, Twitter threads, LinkedIn posts, FB group posts, cold DMs).
4. Measure: How many people took the action? Where did they come from? What messaging converted best?

**Last MVD test (January 2026):**

Product idea: workflow tool for content agencies.

- Posted in 3 relevant LinkedIn groups: 23 sign-ups
- Posted in 2 Slack communities: 12 sign-ups
- Cold emailed 50 agency founders from a targeted list: 15 sign-ups
- Total: 50 sign-ups in 11 days. Passed.

Built the MVP. Now 34 paying customers at $149/month.

**The test we ran in November 2025 that failed:**

Product idea: analytics for Substack newsletters.

- Tried 4 channels over 2 weeks
- Got 14 sign-ups, mostly from existing audience
- Couldn't find natural communities where this was an active problem
- Didn't build it

Saved 3 months of development.

---

## POST 29
**Subreddit:** r/juststart
**Title:** What nobody tells you about the first year of indie hacking

**Body:**

I'm 13 months in. Here's the stuff that would have helped me know in advance.

**Income is lumpy, not linear.**

I expected month-over-month growth. What actually happens: good month, bad month, good month, great month, bad month. Cash flow is a skill you have to learn. Keep 2-3 months of expenses in savings at all times.

**Your first product will probably fail. Build it anyway.**

Not because building is good practice (it is) but because you need to understand how the market responds to YOUR execution before you can improve it. Talking about what you'd build is very different from building it.

**Motivation follows action, not the other way around.**

You will have days where you don't want to work. Work anyway. Start with the smallest possible action. Motivation to keep going almost always appears once you've started.

**Your unfair advantages are worth more than you think.**

The thing you know better than most people, your old job, your niche hobby, your specific community, is more valuable than a generic "productivity app." Build for the people you actually understand.

**You will overestimate what you can do in a month and underestimate what you can do in a year.**

Month 1 expectation: launch product, get 100 paying users, make $3,000.
Month 1 reality: build product, get 12 users, make $0.
Month 12 reality: 3 products, 190 users, $2,800/month.

That's real progress by any objective measure. But it looks like failure from inside month 1.

Give it a year. Then decide.

---

## POST 30
**Subreddit:** r/EntrepreneurRideAlong
**Title:** How I went from 0 to 40 consulting clients using only inbound (no cold outreach)

**Body:**

I'm a bad salesperson. Cold outreach made me miserable. So I built an inbound system instead.

**The setup (took 4 months to build, runs passively now):**

**Layer 1: SEO content (the foundation)**

15 articles targeting specific problems my clients have. "How to set up automated follow-up for dental practices." "Best CRM for solo contractors under $50/month." Articles that answer real questions, not keyword-stuffed filler.

Time to rank: 2-4 months per article. Monthly organic traffic now: 3,200 visits. Conversion to inquiry: 2.1% = 67 inquiries/month.

**Layer 2: Case studies (the proof)**

Every client becomes a case study. Not testimonials, full breakdowns: problem, solution, result with specific numbers. 12 published.

Prospects read case studies during consideration. When they reach out, they already trust the work.

**Layer 3: YouTube (the relationship builder)**

1-2 videos per month. Not production-quality. Screen recordings with my voice explaining how I solved a specific problem. Views aren't massive (1,200/month average) but conversion from viewer to client is 6%.

**Layer 4: Email newsletter (the converter)**

Weekly email to 1,400 subscribers. Purely educational. One tip, one case study snippet, one resource. No hard pitch. Reply rate: 3.4%. People who reply are almost always ready to hire.

**Current state:**

40 active clients (mix of project-based and retainer). $12,800/month revenue. Zero cold emails sent in 8 months.

The inbound flywheel takes longer to start. But once it runs, it runs without you.

---

*Total: 30 posts across r/SideProject (9), r/EntrepreneurRideAlong (7), r/Startup (4), r/SaaS (6), r/juststart (4)*
