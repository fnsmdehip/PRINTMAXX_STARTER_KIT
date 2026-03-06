# Local Biz Lead Machine

## find businesses that need help. show them proof. close the deal.

---

## Part 1: Google Maps Scraping Method

Google Maps is a free database of every local business with a website, phone number, address, and reviews. you don't need paid tools to access it.

### manual method (free, 10 minutes per niche per city)

1. open Google Maps in Chrome
2. search: "[niche] in [city]" (example: "dentists in Austin TX")
3. scroll through results. Google shows 20 at a time. keep scrolling for more.
4. for each business, note:
   - business name
   - website URL
   - phone number
   - rating and review count
   - address

**what to look for:**
- businesses with websites that look outdated (you can tell from the URL pattern and the Google Maps preview)
- businesses with under 20 reviews (they're not doing marketing well)
- businesses with no website listed (they need one)
- businesses with 3-4 star ratings and complaints about "hard to reach" or "website doesn't work" (these are your warmest leads)

### faster method: Google Maps + a spreadsheet

open Google Maps in one tab. open Google Sheets in another. as you scroll through results, paste business info into your sheet.

columns for your spreadsheet:

| business name | website | phone | rating | reviews | city | niche | audit score | contacted | response |
|---|---|---|---|---|---|---|---|---|---|

this is tedious for the first 50 leads. after that, you get fast at scanning and qualifying in seconds.

### the "outsource the scrape" option

if you want to skip manual collection:
- **Google Maps scraper tools:** Outscraper, PhantomBuster, or Apify actors. $0-30/month depending on volume.
- **virtual assistant:** hire on Fiverr or Upwork. $5-10 per 100 leads scraped and entered into a spreadsheet.
- **Python script with Playwright:** automate the browser. more setup but free and unlimited.

the method doesn't matter. what matters is getting a list of 200+ businesses with websites you can audit.

### targeting the right niches

not all local businesses pay equally. rank by willingness to pay for web services:

**high willingness ($1,500-5,000 projects):**
- dentists and orthodontists
- lawyers (personal injury, family, criminal)
- plastic surgeons and med spas
- home renovation contractors
- real estate agents (individual, not brokerages)
- HVAC, plumbing, and electrical companies

**medium willingness ($500-1,500 projects):**
- restaurants and bars
- auto repair shops
- veterinarians
- fitness studios and gyms
- salons and barbershops
- daycares and tutoring centers

**lower willingness ($200-500 projects):**
- retail shops
- food trucks
- freelance professionals
- small non-profits

target the high willingness tier first. same amount of effort to close a $3,000 deal as a $500 deal.

---

## Part 2: Website Audit Automation

the audit is your sales pitch. you're not selling "web design." you're selling "here are 7 problems with your website that are costing you customers, and I can fix all of them."

### what to check (15-point audit)

run these checks on every website in your lead list. takes 2-3 minutes per site once you have the process down.

**speed and performance:**
1. **page load time.** use pagespeed.web.dev. enter their URL. anything over 3 seconds on mobile = red flag. 53% of mobile visitors leave after 3 seconds.
2. **mobile responsiveness.** open their site on your phone. does it look broken? text too small? buttons too close together? take a screenshot.
3. **Core Web Vitals.** pagespeed.web.dev shows these too. LCP, FID, CLS. if any are red, mention it.

**security and trust:**
4. **SSL certificate.** does the URL show https or http? http sites get a "Not Secure" warning in Chrome. instant trust killer.
5. **broken links.** click through the main navigation. any 404 pages? use brokenlinkcheck.com for a quick scan.
6. **contact form.** does it work? submit a test message. you'd be surprised how many contact forms go to dead email addresses.

**visibility and marketing:**
7. **Google Business Profile.** search their business name on Google. is their GBP claimed? are the hours correct? is there a description? photos?
8. **review count and recency.** when was their last Google review? if it's been 6+ months, they're leaving money on the table.
9. **meta title and description.** right-click on their homepage, "View Page Source," search for `<title>` and `<meta name="description">`. if the title is just "Home" or "Welcome," their SEO is nonexistent.
10. **social media links.** do they have social links on their website? do those links work? do the social profiles have recent posts?

**content and conversion:**
11. **clear call to action.** can you tell what they want visitors to do within 5 seconds? if the answer is no, the site isn't converting.
12. **photos.** are they using stock photos or real photos of their business? real photos convert 35% better.
13. **testimonials or reviews on site.** do they show customer reviews on their website? most local businesses don't, and it costs them.
14. **service pages.** do they have individual pages for each service? "dentist in Austin" ranks better than a single page listing all services.
15. **last update.** check the copyright year in the footer. if it says 2019, the site hasn't been touched in years.

### scoring the audit

score each item 0-2:
- 0 = major issue (broken, missing, or critically bad)
- 1 = needs improvement (exists but not optimized)
- 2 = good (no action needed)

max score: 30. your best prospects score under 15.

### presenting the audit

do NOT send a spreadsheet. send a simple document or email with:

1. **3 biggest problems** (the most visually obvious issues)
2. **what each problem costs them** (in customers lost, not technical jargon)
3. **before/after example** (show a competitor's site that does it right)
4. **your fix** (what you'd do, in plain language)

**example audit summary:**

> I looked at [business name]'s website and found a few things that might be costing you customers:
>
> 1. your site takes 7.2 seconds to load on mobile. the industry average for dentists is 2.8 seconds. Google's data shows 53% of visitors leave after 3 seconds. that's roughly half your mobile visitors bouncing before they see your site.
>
> 2. your contact form goes to a 404 error page. anyone trying to book an appointment through your website right now can't. I tested it twice.
>
> 3. your Google Business Profile hasn't had a new review in 11 months. your top competitor has 15 reviews from the last 3 months. reviews are the #1 factor in local search ranking.
>
> I can fix all three of these in about a week. want me to send a quote?

specific. numbers. no jargon. talks about their business, not your skills.

---

## Part 3: Cold Email Templates

### template 1: restaurant / food service

subject: noticed something on [restaurant name]'s website

> hi [first name],
>
> I was looking for [cuisine type] restaurants in [city] and found [restaurant name]. the food looks great based on your photos.
>
> I noticed your website takes about [X] seconds to load on mobile. for restaurants, most people search on their phones when they're hungry and deciding where to eat. a slow site means they pick the next result instead.
>
> I also noticed your online menu is a PDF. about 40% of mobile users can't open PDFs easily, which means they might not see your menu at all.
>
> I help restaurants in [city] fix these kinds of issues. usually takes 1-2 weeks and costs between $500-$1,200 depending on scope.
>
> want me to send a free audit with everything I'd fix?
>
> [your name]

### template 2: professional services (lawyers, dentists, accountants)

subject: [business name]'s Google presence

> hi [first name],
>
> I was researching [niche] in [city] and noticed [business name] ranks on page [X] for "[niche] in [city]." your top competitor, [competitor name], ranks #1 and has [X] more Google reviews.
>
> three things I noticed that might be affecting your visibility:
>
> 1. your website's meta title says "[generic title]" instead of including "[niche] in [city]"
> 2. your last Google review was [X months] ago
> 3. [one more specific issue from audit]
>
> I help [niche] practices in [city] improve their online presence. my last client, a [similar niche] in [nearby city], went from page 3 to page 1 for their main keyword in 6 weeks.
>
> can I send you a free audit?
>
> [your name]

### template 3: home services (HVAC, plumbing, contractors)

subject: [business name]'s website on mobile

> hey [first name],
>
> I pulled up [business name]'s website on my phone and ran into a few issues:
>
> - the phone number isn't clickable (customers have to memorize it and dial manually)
> - the contact form doesn't work on mobile (I tested it)
> - page takes [X] seconds to load (Google recommends under 3)
>
> for home service companies, 70%+ of customers search on their phones during emergencies. if they can't call you in one tap, they call the next company.
>
> I fix these kinds of issues for contractors and service companies. usually $800-$1,500 and done within 2 weeks.
>
> interested in a free audit?
>
> [your name]

### template 4: retail / local shops

subject: quick thought about [business name]

> hi [first name],
>
> I walked past [business name] on [street/area] and checked out your website afterward. the store looks great but the website doesn't match.
>
> a few things I noticed:
> - no Google Business Profile photos (this is free and takes 10 minutes to fix)
> - website copyright says [old year]
> - no customer reviews visible on the site
>
> I help local shops in [city] get their online presence to match their in-store experience. packages start at $500.
>
> want me to put together a quick list of everything I'd improve?
>
> [your name]

---

## Part 4: Pricing Guide

### the 3-tier structure

offer three packages. most people pick the middle one.

**tier 1: website fix ($500-800)**
- fix the specific issues from your audit
- speed optimization
- mobile responsiveness fix
- contact form repair
- SSL setup if needed
- delivered in 1 week

**tier 2: website overhaul ($1,200-2,000)**
- everything in tier 1
- new design (modern template, their branding)
- SEO basics (meta titles, descriptions, schema markup)
- Google Business Profile optimization
- 5 pages (home, about, services, contact, testimonials)
- delivered in 2-3 weeks

**tier 3: full digital presence ($2,500-4,000)**
- everything in tier 2
- custom design
- 10+ pages with individual service pages
- local SEO setup
- review generation system
- social media profile setup
- monthly reporting
- delivered in 4-6 weeks

### anchoring strategy

always present tier 3 first. when they see $3,500, tier 2 at $1,500 feels reasonable. if you present $500 first, $1,500 feels expensive.

### the retainer pitch

after the project is complete, offer ongoing maintenance:

> I can maintain everything we just built for $200-500/month. that includes hosting, security updates, monthly speed checks, Google Business Profile management, and 2 hours of content updates.

**retainer math:** 10 clients x $300/month = $3,000/month recurring. this is the real money in local business services. projects are lumpy. retainers are reliable.

### pricing psychology

- never quote in round numbers. $1,497 feels researched. $1,500 feels made up.
- always anchor against the cost of NOT fixing it. "your broken contact form has been live for 3 months. if even 5 potential patients tried to book through your site, that's $5,000-15,000 in lost revenue."
- local businesses compare you to agencies. agencies charge $5,000-20,000. you're the affordable expert.

---

## Part 5: Follow-Up Sequence

70% of local business deals close on follow-ups 2-4. never send one email and give up.

### the 5-email sequence

**email 1 (day 0):** initial outreach (use templates from Part 3)

**email 2 (day 3):**
subject: re: [original subject]

> hi [first name], following up on my note about [business name]'s website.
>
> I actually went ahead and ran a full audit. the short version: your site scores [X/30] on my 15-point check. your closest competitor scores [Y/30].
>
> happy to share the full breakdown. no charge, no obligation.
>
> [your name]

**email 3 (day 7):**
subject: [business name] vs [competitor name]

> [first name], one more data point.
>
> I compared [business name] to [competitor name] on 5 key metrics:
> - page speed: you [X]s, them [Y]s
> - Google reviews: you [X], them [Y]
> - mobile score: you [X/100], them [Y/100]
>
> the gap is fixable. most of these improvements take 1-2 weeks.
>
> worth a 10-minute call to walk through it?
>
> [your name]

**email 4 (day 14):**
subject: last thought on [business name]'s site

> hey [first name], I know you're busy running a business. just wanted to flag: the contact form issue I mentioned is still live. every day it stays broken is potential customers you're losing.
>
> if this isn't a priority right now, I get it. if it ever becomes one, I'm here.
>
> [your name]

**email 5 (day 21):**
subject: closing the loop

> [first name], last email from me about this. if website improvements are ever on your radar, here's what I'd do first:
>
> 1. fix the contact form (30 minutes)
> 2. add click-to-call to your phone number (15 minutes)
> 3. update your Google Business Profile (1 hour)
>
> those 3 things cost under $500 and would make the biggest immediate difference.
>
> my email and number are below if you ever want to chat.
>
> [your name]

### follow-up timing

- email 2: 3 days after email 1
- email 3: 4 days after email 2
- email 4: 7 days after email 3
- email 5: 7 days after email 4

total sequence: 21 days. after that, stop emailing. add them to a 90-day check-in list.

---

## Part 6: Case Study Template

every completed project becomes a case study. case studies close future clients.

### the format

```
## [business name]: [headline result]

**industry:** [niche]
**location:** [city, state]
**project:** [tier name]
**timeline:** [X weeks]
**investment:** [price range, not exact]

### the problem
[2-3 sentences about what was broken]

### what we did
[bullet list of specific fixes]

### results
- page speed: [before] -> [after]
- Google ranking: page [X] -> page [Y] for "[keyword]"
- contact form submissions: [before] -> [after] per month
- Google reviews: [before] -> [after]

### client quote
> "[quote from the business owner, even if short]"
```

**get the quote.** after every project, send this email:

> hey [first name], glad you're happy with the new site. quick favor: would you mind sharing a 1-2 sentence quote about working together? I use these on my website to show future clients what the process is like. something like "[business name] worked with [your name] on our website and [result/experience]" is perfect.

most people will do it if you make it easy. some won't. ask every time.

---

## Part 7: Objection Handling

the 5 objections you'll hear from local business owners and what to say.

### "I have a nephew/friend who does websites"

> totally understand. a lot of my clients started with a friend or family member. the main difference is that I specialize in [niche] businesses and know what drives customers in your specific industry. but if you're happy with what they're doing, that's great.

### "I don't think a website matters for my business"

> I hear that. here's a stat that might be relevant: 97% of consumers search online for local businesses. when someone searches "[niche] in [city]," your website is what convinces them to call you instead of your competitor. right now, [competitor] shows up first. their site loads in 2 seconds and has a click-to-call button. yours takes 8 seconds and the contact form is broken.

### "it's too expensive"

> I understand budget is a factor. the website fix package starts at $500, and most of that is fixing things that are actively losing you customers right now. your broken contact form alone has probably cost you more than $500 in the last 3 months.

### "I need to think about it"

> of course, take your time. just so I can follow up at the right time, is there a specific concern I can address, or is it more about timing?

(this separates real "thinking about it" from polite rejection. if they name a concern, address it. if it's timing, ask when to check back.)

### "can you guarantee results?"

> I can guarantee the deliverables: a fast, mobile-optimized site with working forms and proper SEO setup. I can show you results from similar businesses I've worked with. what I can't guarantee is how quickly Google updates rankings, because that's on Google's timeline. but the improvements I make are the same ones that moved [past client] from page 3 to page 1.

---

## what to do today

1. pick a niche and a city from Part 1
2. find 50 businesses on Google Maps (takes about 30 minutes)
3. audit the top 20 by website quality (takes about 1 hour)
4. email the 10 worst websites using templates from Part 3
5. follow up using the sequence from Part 5
6. close your first client within 2-3 weeks

50 leads. 10 emails. 1 client. $1,500. that's the math. the guide cost $17. ROI: 8,723%.

now stop reading and start scraping.
