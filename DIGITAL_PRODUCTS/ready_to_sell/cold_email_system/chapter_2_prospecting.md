# Chapter 2: Finding Leads With Free Tools

## What You'll Have After This Chapter

A spreadsheet of 500+ qualified prospects with their name, email, company, and a personalization data point — built entirely with free tools. No Apollo subscription. No ZoomInfo contract. No $150/month lead database.

## The Lead Qualification Framework

Before you find a single lead, define who you're looking for. A bad list with perfect emails produces nothing. A great list with mediocre emails produces clients.

Answer these five questions:

1. **What industry?** Pick one. Not "small businesses." Pick "e-commerce stores doing $500K-$5M/year" or "B2B SaaS companies with 10-50 employees." Specific.

2. **What role?** Who has the budget and authority to say yes? For most services: founder, CEO, or VP/Director of the relevant department. For design: marketing director. For development: CTO or VP Engineering. For SEO: CMO or founder.

3. **What signal means they need you?** Examples:
   - "They're hiring for the role I replace" (job posting on their careers page)
   - "Their website has obvious issues" (slow, not mobile-friendly, broken checkout)
   - "They just raised funding" (money to spend)
   - "They're running ads but their landing page is bad" (they're spending on traffic but wasting it)

4. **What's their budget?** If you charge $3K/month, don't target solo founders making $50K/year. If you charge $500/project, don't target Fortune 500 (they'll never respond to cold email).

5. **What's your disqualifier?** Who do you explicitly NOT want? Too small? Wrong geography? Competitors? Define the "not this" list.

Write these down. You'll use them as filters for every prospecting method below.

## Method 1: Google Maps Scraping (Local Businesses)

If your target is local or regional businesses (restaurants, law firms, dentists, real estate agents, contractors), Google Maps is your database.

### The Process

1. Search Google Maps for `[business type] in [city]`
2. The results show business name, address, phone, website, and sometimes email
3. For each result that fits your ICP, collect: business name, owner name (check their website's About page), email, website URL

### Scaling It

Manually clicking through Google Maps results is slow. Use **Google Maps Scraper** by Outscraper (outscraper.com). The free tier gives you 500 records/month.

1. Enter your search query: "digital marketing agencies in Austin, TX"
2. Outscraper returns: business name, address, phone, website, Google rating, review count, category
3. Export to CSV
4. Visit each website to find the owner's name and email

This works for: restaurants, agencies, law firms, dentists, contractors, real estate, fitness studios, salons — any business with a physical location.

### Finding the Email

Most small business websites have the owner's email on the Contact or About page. If not:

**Hunter.io** (free tier): 25 searches/month. Enter the domain, get the email format and verified addresses. `hunter.io/search/domain.com`

**RocketReach** (free tier): 5 lookups/month. Better for finding specific people's emails.

**The manual method:** Most business emails follow a pattern. If the owner is "John Smith" and the domain is "acmeagency.com," try:
- john@acmeagency.com
- john.smith@acmeagency.com
- jsmith@acmeagency.com

Verify which one works using **Email Hippo** (free) or **NeverBounce** (free verification for your first 1,000 emails).

## Method 2: LinkedIn Sales Navigator (Free Workaround)

LinkedIn Sales Navigator costs $100/month. You don't need it. Here's the free alternative.

### Boolean Search on LinkedIn

LinkedIn's regular search supports Boolean operators. Use them:

```
"founder" AND "e-commerce" AND "Shopify" -recruiter -hiring
```

This finds founders of Shopify e-commerce stores who aren't recruiters or posting job ads.

More examples:
```
"CEO" AND "SaaS" AND ("series A" OR "seed funding")
"marketing director" AND "DTC" AND "brand"
"agency owner" AND ("web design" OR "development") AND "freelance"
```

### Extracting Contacts

LinkedIn doesn't show email addresses. But you can find them:

1. **Look at their LinkedIn profile** for an email in the "Contact Info" section (click the three dots, or check their About section)
2. **Check their personal website** (many list it on LinkedIn)
3. **Use their company domain + Hunter.io** to find their email pattern
4. **Use Snov.io free tier** (50 credits/month): Enter a LinkedIn URL, get their email

### Scaling LinkedIn Prospecting

**PhantomBuster free tier**: Automate LinkedIn profile scraping. 14-day trial, then limited free actions. Extract names, titles, and company info from search results.

**Export LinkedIn connections**: If you're already connected with prospects, go to Settings > Data Privacy > Get a copy of your data. LinkedIn emails you a CSV of all your connections with their emails.

### Building the List

Create a Google Sheet with these columns:
- First Name
- Last Name
- Email
- Company
- Title
- LinkedIn URL
- Personalization Note (we'll use this in Chapter 3)

Target: 100+ qualified prospects from LinkedIn.

## Method 3: Competitor Customer Poaching

Find companies already using your competitor's product. They've validated the need — they just haven't found you yet.

### How to Find Competitor Customers

**Wappalyzer** (free browser extension): Detects the technology stack of any website. Visit a potential prospect's website, click Wappalyzer, and see what tools they use.

If you sell Webflow development, find companies using Squarespace or Wix (they're on inferior platforms and might want to upgrade). Wappalyzer tells you exactly what they're running.

**BuiltWith** (free tier): Enter a technology (e.g., "Klaviyo," "Shopify," "WordPress") and see a list of websites using it. The free tier gives limited results; the paid tier is expensive. Use the free tier to build a starter list.

**G2/Capterra reviews**: Go to your competitor's G2 or Capterra page. Read the reviews. The reviewer's name, title, and company are usually visible. These are people actively using (and sometimes unhappy with) a competing product.

**Twitter/X search**: Search for competitor mentions:
```
"[competitor name]" (frustrated OR broken OR switching OR alternative)
```
People complaining about your competitor are pre-qualified leads.

### The "Switching" Pitch

When you email someone who's using a competitor, your pitch is different from a standard cold email:

"I noticed you're using [Competitor]. How's that going? I ask because we work with a lot of [Competitor] customers who switched after hitting [SPECIFIC LIMITATION]. Happy to share what we did for [SIMILAR COMPANY] if useful."

This works because you're not selling against them — you're acknowledging their current choice and offering relevant experience.

## Method 4: Job Board Mining

Companies hiring for the role you fill are telling you they have budget and need. If they're hiring a full-time designer, they might also want a freelance designer while they search (or instead of hiring full-time).

### Where to Look

- **Indeed/LinkedIn Jobs**: Search for job titles related to your service. "Web Designer," "Content Writer," "SEO Specialist."
- **Wellfound (formerly AngelList)**: Startups hiring. These companies are small enough that the founder reads their email.
- **Hacker News "Who is Hiring"**: Monthly threads. Technical companies hiring. High-quality leads.
- **WeWorkRemotely**: Remote companies. Usually smaller, founder-led.
- **Craigslist**: Local businesses posting for help. They often have budget but don't know how to hire properly.

### The Extraction

For each job posting, collect:
- Company name
- Hiring manager (sometimes listed, sometimes you need to find them on LinkedIn)
- Company website
- What they're hiring for (this becomes your personalization)

### The Pitch

"I saw you're hiring a [ROLE]. While you're searching for the right full-time person, I can handle [SPECIFIC DELIVERABLE] on a project basis. I've done this for [SIMILAR COMPANY] — delivered [RESULT] in [TIMEFRAME]. Want me to send over a few examples?"

This isn't competing with their hire. It's filling the gap while they recruit. Many of these relationships turn into ongoing contracts when they realize a freelancer is more efficient than a full-time employee for their workload.

## Method 5: Community Mining

Your prospects are talking publicly in communities. They're asking questions, sharing challenges, and looking for help. Find them.

### Where to Mine

**Reddit**: Find subreddits where your prospects hang out.
- For e-commerce clients: r/ecommerce, r/shopify, r/dropshipping
- For SaaS clients: r/SaaS, r/startups, r/indiehackers
- For agencies: r/agency, r/marketing, r/SEO

Search within subreddits for phrases like "looking for," "need help with," "can anyone recommend," "hire."

**Facebook Groups**: Join 5-10 groups where your prospects ask questions. Business owner groups, industry-specific groups, tool-specific groups (Shopify store owners, WordPress users, etc.).

**Slack/Discord communities**: Many industries have active Slack workspaces. Find them on `slofile.com` or `discord.com/servers`. Join, lurk for a week, then start helping.

**Twitter/X**: Search for people asking for your service:
```
"looking for a designer" -job -hiring
"need help with SEO" -course -free
"can anyone recommend a developer"
```

### The Community Approach

Never cold pitch in communities. It gets you banned and destroys your reputation. Instead:

1. Find someone asking a question you can answer
2. Give a genuinely helpful answer in public
3. DM them with additional help (still not pitching)
4. If they ask about your services, THEN share what you do

The lead quality from communities is 10x higher than cold email. These people have already self-identified as having the problem you solve.

## Building Your Master List

By now you should have prospects from multiple sources. Consolidate everything into one Google Sheet:

| First Name | Last Name | Email | Company | Title | Source | Personalization Note | Status |
|-----------|----------|-------|---------|-------|--------|---------------------|--------|
| Sarah | Kim | sarah@acme.com | Acme Co | Founder | LinkedIn | Just raised seed round | Not contacted |

**Email Verification (Critical)**

Before you send a single email, verify every address. Sending to invalid emails raises your bounce rate, which tanks your sender reputation.

Free verification tools:
- **NeverBounce**: 1,000 free verifications
- **ZeroBounce**: 100 free verifications
- **Email Hippo**: Single-email verification, unlimited free checks

Remove any email that comes back as "invalid" or "risky." Your bounce rate should stay below 3%.

## The Numbers Game

Here's what realistic cold email performance looks like:

- **500 prospects** on your list
- **15-25% open rate** (if your infrastructure is solid)
- **3-8% reply rate** (if your copy is good — Chapter 4)
- **15-40 replies** from 500 sends
- **5-15 positive replies** (interested in talking)
- **2-5 clients** (if your closing process works — Chapter 5)

If you charge $2K per project, 500 emails = $4K-$10K in revenue.
If you charge $3K/month retainer, 500 emails = $6K-$15K in monthly recurring revenue.

The list is the foundation. The emails are the lever. Build the list right, and the emails practically write themselves — because you know exactly who you're talking to and why they need you.

Next chapter: AI-personalized outreach that doesn't sound like AI wrote it.
