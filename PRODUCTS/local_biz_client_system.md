# The Local Business Client Acquisition System: Scrape, Analyze, Pitch, Close

**Price: $97**

---

## What this is

A complete pipeline for acquiring local business clients who need website redesigns, SEO, social media management, or digital marketing. From finding prospects to closing $1,500-5,000 deals.

This isn't a generic "start an agency" guide. It's the exact system: scraping tools, analysis scripts, pitch templates, cold email sequences, pricing frameworks, and objection handling scripts. Everything you need to sign your first client this month.

Total infrastructure cost: $37-100/month. Revenue per client: $1,500-5,000 for a one-time project, or $500-2,000/month for ongoing services.

---

## Part 1: The local business opportunity (why this works)

### The market gap

There are 33 million small businesses in the US. Most have terrible websites. Many have no website at all. The ones who do have sites built in 2015 that aren't mobile-friendly, load in 8 seconds, and rank nowhere on Google.

These businesses know they need help. They just don't know who to hire or how much it should cost. Most "web agencies" charge $10,000-50,000 and take 3-6 months. A solopreneur with AI tools can deliver a better product in 1 week for $1,500-3,000.

### Why they'll pay you

Local businesses make money from local customers. Local customers find businesses on Google. If a plumber's website loads slowly, isn't mobile-friendly, and doesn't rank for "plumber near me," they're losing thousands of dollars per month in missed calls.

You're not selling a website. You're selling more customers.

### The numbers

- Average website redesign deal: $2,000-3,000
- Average monthly retainer (SEO + social): $500-1,500
- Close rate on warm leads (from analysis + custom pitch): 15-25%
- Prospects you can pitch per week: 50-100
- Expected closes per week: 8-25 pitches = 1-3 clients

1-3 new clients per week at $2,000 each = $8,000-24,000/month.

Conservative scenario (1 client per 2 weeks): $4,000-6,000/month.

---

## Part 2: Finding prospects (the scraping system)

### Method 1: Google Maps scraping (free)

Search Google Maps for:
```
[business type] near [city]
```

Examples:
- "dentist near Austin TX"
- "plumber near Dallas TX"
- "restaurant near Phoenix AZ"

For each result:
1. Click the business listing
2. Note: name, phone, website URL, rating, review count
3. Visit their website
4. Quick score: Is it mobile-friendly? Does it load fast? Modern design?

**Volume:** Manually scan 20-30 businesses per hour. Fill a spreadsheet.

### Method 2: Automated scraping (Python script)

The pipeline script automates this:

```bash
python3 local_biz_pipeline.py --urls-file my_prospects.csv
```

**What it does:**
1. Visits each website
2. Checks: mobile responsiveness, SSL certificate, page load speed, SEO basics, contact info visibility
3. Generates a score (0-100) for each site
4. Sites below 40 = high-priority prospects
5. Outputs: scored prospect list + analysis

**Input CSV format:**
```csv
url,business_name,category,city
https://joesplumbing.com,Joe's Plumbing,plumber,Austin TX
https://brightdental.com,Bright Dental,dentist,Dallas TX
```

### Method 3: Yelp + Yellow Pages (manual, high quality)

Yelp and Yellow Pages list businesses by category and location. Many businesses listed there have outdated websites or no website at all.

**Process:**
1. Search by category and city
2. Filter by businesses WITH websites (click through to check quality)
3. Also note businesses WITHOUT websites (bigger opportunity)
4. Add to your prospect spreadsheet

### Best categories to target

| Category | Deal size | Urgency to fix | Competition |
|----------|----------|----------------|-------------|
| Dentists | $3,000-5,000 | High (patients research online) | Medium |
| Plumbers | $1,500-3,000 | High (emergency searches) | Low |
| Restaurants | $1,500-3,000 | High (reviews + menu online) | Medium |
| Real estate agents | $2,000-5,000 | High (listings drive business) | High |
| Lawyers | $3,000-8,000 | High (research-heavy purchase) | Medium |
| HVAC companies | $1,500-3,000 | High (seasonal urgency) | Low |
| Auto repair shops | $1,500-2,500 | Medium | Low |
| Salons/barbers | $1,000-2,000 | Medium | Low |
| Gyms/fitness | $1,500-3,000 | Medium | Medium |
| Accountants | $2,000-4,000 | Medium | Low |

**Start with:** Dentists, plumbers, and restaurants. High urgency, decent deal sizes, used to spending on marketing.

---

## Part 3: Analyzing prospects (the audit)

### The 5-minute website audit

For each prospect website, check these 10 things:

**1. Mobile responsiveness**
Open on your phone. Does it work? Pinch-to-zoom needed? Buttons too small? Over 60% of local searches happen on mobile.

**2. Page load speed**
Use PageSpeed Insights (free, Google). Score below 50 = major problem. Load time over 3 seconds = losing 53% of visitors.

**3. SSL certificate**
Is it https:// or http://? No SSL = Chrome shows "Not Secure" warning. Instant trust killer.

**4. Google Business Profile**
Search their business name on Google. Do they have a claimed, updated Google Business Profile? Many don't.

**5. Reviews**
How many Google reviews? What's the average rating? Competitors with more reviews outrank them.

**6. SEO basics**
View source (or use SEO extension). Do they have: title tag, meta description, H1 tag, alt text on images? Most local sites miss 3 of 4.

**7. Contact information**
Can you find their phone number in under 5 seconds? Is there a contact form? Many local sites bury their contact info.

**8. Call to action**
Is there a clear "Call Now" or "Book Appointment" button? Or just a wall of text?

**9. Content freshness**
When was the site last updated? Blog from 2019? Copyright year says 2022? Signs of neglect.

**10. Competitor comparison**
Search their main keyword ("dentist austin tx"). Where do they rank? Who ranks above them? What do those sites look like?

### Audit score card

| Factor | Score 0-10 | Notes |
|--------|-----------|-------|
| Mobile | | |
| Speed | | |
| SSL | | |
| Google Business | | |
| Reviews | | |
| SEO | | |
| Contact visibility | | |
| CTA | | |
| Content freshness | | |
| Competitive position | | |
| **Total** | **/100** | |

Prospects scoring below 40: priority targets. They need the most help and have the most to gain.

### The automated audit

The pipeline script generates this analysis automatically:

```
Output: prospects.csv
Columns: url, business_name, mobile_score, speed_score, ssl, seo_score,
         overall_score, priority (HIGH/MEDIUM/LOW), recommended_services
```

---

## Part 4: The pitch (what to send them)

### The custom landing page approach

This is the killer differentiator. Instead of sending a generic "I can help with your website" email, you send them a CUSTOM preview of what their website could look like.

**How it works:**
1. For high-priority prospects (score below 40), generate a modern landing page
2. Use their business name, their services, their city
3. Host it on a preview URL
4. Send them the link: "Here's what your website could look like"

They click the link and see a modern, fast, mobile-friendly version of their website. Built specifically for them. In under 30 minutes.

**The reaction:** "Wait, you already built this? How much?"

That's the conversation you want.

### Landing page generation

Use AI to generate the page:

```
Create a modern landing page for [BUSINESS NAME], a [CATEGORY] in [CITY].

Sections:
1. Hero: Business name, tagline, "Call Now" button with their phone number
2. Services: 4-6 service cards based on their website's service list
3. About: Brief about section (adapt from their current site)
4. Reviews: Placeholder testimonial section
5. Contact: Phone, address, contact form, Google Maps embed
6. Footer: Hours, social links

Design: Modern, mobile-first, fast loading
Color: [Based on their existing branding if visible, otherwise clean blue/white]
```

Deploy to Vercel or a preview subdomain. Total time: 20-30 minutes per prospect.

---

## Part 5: Cold email sequences (the outreach)

### Sequence 1: The website audit approach (highest converting)

**Email 1 (Day 0): The audit reveal**

Subject: Quick question about [BUSINESS NAME]'s website

```
Hi [FIRST NAME],

I was looking for a [CATEGORY] in [CITY] and found [BUSINESS NAME].
Noticed a few things about your website that might be costing you customers:

- Your site takes [X] seconds to load (over 3 seconds loses 53% of visitors)
- It's not fully mobile-friendly ([SPECIFIC ISSUE])
- You're not showing up for "[CATEGORY] near [CITY]" on Google

I put together a quick preview of what a modernized version could look like:
[PREVIEW LINK]

Takes 2 minutes to look at. No strings attached.

[YOUR NAME]
```

**Email 2 (Day 3): The value add**

Subject: Re: Quick question about [BUSINESS NAME]'s website

```
Hi [FIRST NAME],

Following up on the website preview I sent. Quick thought:

[BUSINESS NAME]'s competitors in [CITY] are averaging [X] Google reviews
and ranking on the first page. Right now, [BUSINESS NAME] is on page [X].

The preview I built loads in under 2 seconds and is optimized for
"[CATEGORY] [CITY]" searches. If you're interested in more customers
from Google, I'm happy to chat for 15 minutes.

[YOUR NAME]
```

**Email 3 (Day 7): The direct close**

Subject: Re: Quick question about [BUSINESS NAME]'s website

```
Hi [FIRST NAME],

Last note on this. I've helped [NUMBER] [CATEGORY] businesses in [REGION]
update their websites. Average result: 40% more calls within the first month.

If updating your website is on your radar for 2026, here's my calendar: [LINK]

If the timing isn't right, no worries at all.

[YOUR NAME]
```

### Sequence 2: The direct approach (for no-website businesses)

**Email 1:**

Subject: [BUSINESS NAME] online presence

```
Hi [FIRST NAME],

I searched for "[CATEGORY] in [CITY]" on Google and [BUSINESS NAME] didn't
come up. Your competitors are getting those calls instead.

I build websites for local businesses. Typically takes 1 week and costs
$1,500-2,500 depending on what you need. The site pays for itself when
it brings in 1-2 new customers.

Would a quick 10-minute call make sense?

[YOUR NAME]
```

### Sequence 3: The social proof approach

**Email 1:**

Subject: How [SIMILAR BUSINESS] got 47% more calls

```
Hi [FIRST NAME],

I recently rebuilt the website for [SIMILAR BUSINESS TYPE] in [NEARBY CITY].
Within 30 days:
- 47% more website visitors
- 23% more phone calls
- First page Google ranking for "[their keyword]"

Looking at [BUSINESS NAME]'s current site, I see similar opportunities.
I put together a quick preview: [LINK]

Worth a 10-minute call?

[YOUR NAME]
```

---

## Part 6: Pricing and packaging

### Package 1: Website Redesign ($1,500-3,000)

**Includes:**
- Modern, mobile-responsive website (5-10 pages)
- SEO optimization (title tags, meta descriptions, structured data)
- Google Business Profile setup/optimization
- Contact form setup
- 30 days of support after launch

**Timeline:** 5-7 business days

**Your cost:** $0 (AI builds it) + $10-20 (hosting/domain)
**Your time:** 10-15 hours over the week
**Your margin:** 95%+

### Package 2: Monthly SEO + Maintenance ($500-1,000/month)

**Includes:**
- Monthly content updates (2-4 blog posts)
- Google Business Profile management
- Review monitoring and response management
- Monthly analytics report
- Technical maintenance and updates

**Your cost:** $0 (AI writes the content)
**Your time:** 3-5 hours per client per month
**Your margin:** 90%+

### Package 3: Full Digital Presence ($2,000-5,000 setup + $1,000-2,000/month)

**Includes:**
- Website redesign (Package 1)
- Monthly SEO (Package 2)
- Social media management (3 posts/week)
- Google Ads management ($500+ ad spend managed by you)
- Monthly strategy call

**Your cost:** Client's ad budget + your time
**Your time:** 8-10 hours per client per month
**Your margin:** 80%+

### How to price

**Never price hourly.** Price by value delivered.

A dentist who gets 5 more patients per month from a better website earns $5,000-15,000 extra per month. Charging $3,000 for the website is a 2-5x ROI in the first month.

Frame every price as an investment with a specific return, not a cost.

---

## Part 7: The sales call (closing the deal)

### The 15-minute call structure

**Minutes 1-3: Rapport**
"Tell me about [BUSINESS NAME]. How long have you been in [CITY]? How do most of your customers find you?"

**Minutes 3-7: Pain discovery**
"When someone searches for [CATEGORY] in [CITY], where do you show up? How many calls does your website generate per month? What would 10-20 more calls per month mean for your business?"

**Minutes 7-10: Solution presentation**
"Based on what you've told me, here's what I'd recommend: [Package]. The preview I sent gives you a sense of the quality. I can have the full site live within [timeframe]."

**Minutes 10-13: Pricing and objection handling**
"The investment is $[PRICE]. Most of my clients see a return within the first month through increased calls. I also offer a monthly plan at $[PRICE] if you'd prefer to spread the cost."

**Minutes 13-15: Close**
"Should we get started? I have an opening next week. I'll need [50% deposit / first month payment] to reserve the slot."

### Objection handling scripts

**"That's too expensive."**
"I understand. Let me ask: if this website brings in 5 extra customers per month, what's that worth to your business? Most [CATEGORY] clients are worth $[X] each. That's $[5 x X] per month from a one-time $[PRICE] investment."

**"I need to think about it."**
"Of course. I'll send you a summary email with everything we discussed. What's the main thing you're weighing? [Listen, address the real concern]."

**"I already have a web guy."**
"Great, and I'm not trying to replace them. I'm curious: is your current site bringing in the number of calls you'd like? [If no:] That's the gap I fill. I specialize in websites that rank and convert, specifically for [CATEGORY] businesses."

**"Can you do it cheaper?"**
"I can adjust the scope. For $[LOWER PRICE], I'd do [REDUCED PACKAGE]. But honestly, the [FEATURE THEY'D LOSE] is usually what drives the most results. Most clients find the full package pays for itself fastest."

**"I don't think a website will help."**
"That's fair. Where do most of your customers come from? [Listen]. The data shows [X]% of people search online before choosing a local [CATEGORY]. Right now, those searchers are finding your competitors instead. A website captures that traffic."

---

## Part 8: Delivering the work (the fulfillment system)

### Week-by-week delivery timeline

**Day 1: Kickoff**
- Collect: business info, logo, photos, service descriptions, testimonials
- Create shared folder for client assets
- Send questionnaire (10 questions about their business, target customers, competitors)

**Days 2-3: Build**
- Generate website with AI (Claude Code or Cursor)
- Apply client branding (colors, logo, fonts)
- Add all content from questionnaire
- Set up contact form and analytics

**Day 4: Internal review**
- Test on 3 screen sizes (phone, tablet, desktop)
- Check all links
- Verify SEO elements
- Run PageSpeed Insights (target: 90+ score)

**Day 5: Client review**
- Send preview link
- Walk through on a call (15 minutes)
- Collect feedback
- Note revision requests

**Days 6-7: Revisions + launch**
- Make revisions (usually minor)
- Connect domain
- Set up Google Analytics + Search Console
- Submit sitemap to Google
- Send "Your site is live" email with analytics access

### Quality checklist (before showing client)

- [ ] Loads in under 2 seconds
- [ ] Mobile-responsive (tested on real phone)
- [ ] All images optimized (under 200KB each)
- [ ] Contact info visible on every page
- [ ] "Call Now" button works (test it)
- [ ] Contact form sends to correct email (test it)
- [ ] SSL certificate active (https://)
- [ ] Google Analytics installed
- [ ] Meta titles and descriptions on every page
- [ ] No lorem ipsum or placeholder text
- [ ] Client's real photos (not only stock)
- [ ] Correct business hours listed
- [ ] Privacy policy and terms pages exist

---

## Part 9: Client retention (turning one-time into recurring)

### The 30-day check-in

30 days after launch, email the client:
```
Hi [NAME],

It's been 30 days since [BUSINESS NAME]'s new website launched.
Here's a quick summary:

- Website visitors: [NUMBER] (up from [OLD NUMBER])
- Phone calls from website: [NUMBER]
- Google ranking for "[KEYWORD]": [POSITION]

Would you like to keep this momentum going with monthly SEO
and content updates? I have a plan at $[PRICE]/month that includes
[BRIEF DESCRIPTION].

Happy to chat if you have questions.
```

### Upsell path

```
Website redesign ($2,000)
  -> Monthly SEO ($500/month)
  -> Social media management (+$500/month)
  -> Google Ads management (+$500/month)
  -> Referral to other businesses they know

$2,000 one-time -> $1,500/month recurring
```

One client at $1,500/month = $18,000/year. 5 retained clients = $90,000/year.

### Generating referrals

After the 30-day check-in, if the client is happy:
```
Glad things are going well! Quick question: do you know any other
[CATEGORY] owners or business owners in [CITY] who could use a similar
upgrade? I'd offer them [DISCOUNT] as a thank-you for the referral.
```

Referral clients close at 40-60% (vs. 15-25% from cold outreach). They're the highest quality leads you can get.

---

## Part 10: Scaling the system

### At 5 clients/month: Solo operation

- You: Sales + fulfillment + client communication
- Revenue: $10,000-15,000/month
- Time: 40-50 hours/week
- Profit: $8,000-12,000/month (after tools)

### At 10 clients/month: First hire

- Hire a VA ($500/month) for: scheduling, client questionnaires, basic updates
- Hire a freelance developer ($1,000-2,000/month) for: overflow builds
- You: Sales + quality control + strategy
- Revenue: $20,000-30,000/month
- Profit: $15,000-25,000/month

### At 20+ clients/month: Agency mode

- 2-3 developers (freelance or part-time)
- 1 sales person (commission-based)
- 1 project manager
- You: Business development + partnerships
- Revenue: $40,000-60,000/month
- Profit: $20,000-35,000/month

### The exit option

A client base generating $10,000+/month in recurring revenue can sell for 2-4x annual revenue. 10 clients at $1,000/month = $120,000/year recurring = $240,000-480,000 exit value.

---

## Quick-start: Sign your first client in 14 days

**Days 1-2: Setup**
- Install Python dependencies for scraping script
- Set up 3 sending domains + inboxes
- Start email warmup (runs automatically for 14 days)
- Build your portfolio page (even with fake/sample projects)

**Days 3-5: Prospect**
- Scrape 100 local business websites in your target city
- Run the analysis script
- Identify 20-30 high-priority prospects (score below 40)

**Days 6-8: Create pitches**
- Generate custom landing page previews for top 10 prospects
- Write personalized email sequences for each

**Days 9-11: Outreach**
- Send email sequence 1 to first batch of 10 prospects
- While waiting for replies, scrape and analyze next 50 prospects

**Days 12-14: Close**
- Follow up on warm replies
- Book calls
- Close your first deal

$97 for this system. Your first client pays $1,500-3,000. That's a 15-30x return on your investment in this guide.

---

*Disclaimer: Results not typical. Individual results vary based on effort, market conditions, and other factors.*
