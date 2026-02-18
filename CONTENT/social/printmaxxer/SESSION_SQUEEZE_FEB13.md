# Session squeeze - Feb 13 2026
# Status: PENDING_REVIEW
# Source: Feb 13 build session (lead pipeline + 11 parallel tools)
# Voice: @pipelineabuser weighted aggregate per copy-style.md

---

## 5 standalone tweets

### Tweet 1 (system overview)

30,200 websites analyzed. 2,618 have garbage sites. cold emails already drafted for every single one. matched to live demos i built for their exact industry.

the entire pipeline runs while i sleep. 30 parallel workers. 12 sites scored per second. no human in the loop.

### Tweet 2 (specific result)

pulled 2.87 million local business records from Overture Maps. free. deduplicated to 1,454,245 unique domains. scored 30,200 websites on 5 dimensions. found 2,618 businesses paying for sites worse than the free demos i already have live.

cold emails are pre-written. each one links to a live demo matching their industry. $500-$3K per close. the math works.

### Tweet 3 (philosophical)

most ppl build the outreach system OR the product. never both at the same time.

i built 11 tools in parallel today. lead qualifier, competitor analyzer, cold email generator, proposal builder, A/B tester, enrichment engine, dashboard, and 4 more. each one feeds the next. the system compounds. individual scripts don't.

### Tweet 4 (technical flex)

my lead qualifier scores websites on 5 dimensions: design age, mobile responsiveness, SEO signals, page speed, and AIO/GIO readiness. 0-100 scale. anything below 35 gets a cold email with a link to a live demo site i already own.

70+ skip-domain patterns filter out false positives. wix.com, squarespace.com, godaddysites, everything that indicates they already use a builder. only targets truly bad custom sites.

this is not a scraper. it's a quant scoring engine for bad websites.

### Tweet 5 (honest update)

honest numbers from today:

- 1,454,245 leads in the pool
- 30,200 websites analyzed so far
- 2,618 hot (score >= 65)
- 15,739 warm (score 45-64)
- 58,295 cold emails generated
- 19 live demo sites on surge.sh ($0/mo hosting)
- 11 tools built today
- $0 revenue

the pipeline is loaded. now i need to pull the trigger on outreach. that's the hard part. everything else was the easy part.

---

## Thread (7 tweets)

### 1/7

30,200 websites analyzed while i slept. 2,618 have garbage sites. cold emails already drafted for every one of them.

here's how i built an autonomous local business lead machine in one session. real numbers, real tools, nothing theoretical.

### 2/7

data sourcing: Overture Maps has 2.87 million US business records. free. no API key, no rate limits, just download.

i wrote a pre-filter that deduplicates by domain, strips subdomains, removes known builder platforms (wix, squarespace, godaddy, etc). 2.87M filtered down to 1,454,245 unique domains worth analyzing.

### 3/7

the analysis engine scores every website on 5 dimensions:

- design age (old HTML patterns, outdated meta tags)
- mobile responsiveness (viewport, media queries)
- SEO signals (missing titles, no schema, thin content)
- page speed (image optimization, render blocking)
- AIO/GIO readiness (structured data for AI search)

30 parallel workers. 12 sites per second. 0-100 score for each. anything under 35 is a hot lead.

### 4/7

cold email pipeline auto-matches each lead to one of 16 live demo sites i already have deployed. dentist gets dental-demo.surge.sh. plumber gets plumber-demo.surge.sh. restaurant gets restaurant-site-demo.surge.sh.

3-email sequence per lead. first email shows the demo. second follows up with a specific page speed comparison. third offers a free audit call.

58,295 emails generated so far. ready to send the moment i set up a warmed inbox.

### 5/7

in one session i had 11 parallel agents building:

- local SEO competitor analyzer
- unified CLI for all tools
- cold email A/B test framework
- lead enrichment engine
- proposal generator
- interactive dashboard
- website signal scorer v2

each tool feeds the next one. competitor data improves email copy. enrichment data improves proposals. A/B results improve everything.

### 6/7

current numbers:

- 1,454,245 total leads in pool
- 30,200 websites scored
- 2,618 hot leads (bad sites, money to spend)
- 15,739 warm leads
- 58,295 cold emails pre-drafted
- 19 live demo sites ($0 hosting on surge.sh)
- pipeline runs unattended via cron at 3 AM nightly

### 7/7

the playbook is simple:

1. find businesses with bad websites (automated)
2. show them a better one that already exists (live demo link in cold email)
3. offer to build it for them ($500-$3,000)
4. use AI to build it in 2-4 hours (Lovable, Bolt, v0)
5. 90%+ margin on every deal

the hard part was building the pipeline. that's done. now it's just volume.

---

## Reddit post (r/SideProject)

**Title:** I built a system that finds local businesses with bad websites and cold emails them live demos

**Body:**

been working on this for a few weeks. wanted to share the numbers and the approach since it's a bit different from what i usually see posted here.

**the idea**

local businesses (dentists, plumbers, restaurants, lawyers, etc.) often have terrible websites. either built in 2014 and never updated, or some generic template with placeholder text still showing. they're paying someone $50/mo to host a site that actively loses them customers.

i built a pipeline that finds these businesses automatically, scores their websites, and sends them a cold email linking to a live demo site for their industry.

**how it works**

1. data source: Overture Maps has ~2.87 million US business records. free to download. includes name, address, phone, category, and often a website URL.

2. pre-filtering: i wrote a Python script that deduplicates by domain, normalizes URLs, and filters out businesses using known website builders (Wix, Squarespace, GoDaddy, Shopify, etc.). these businesses already have "good enough" sites. i want the ones with truly bad custom sites or ancient WordPress installs. this narrows the pool from 2.87M to about 1.45M.

3. website scoring: another Python script visits each site and scores it 0-100 across 5 dimensions: design age, mobile responsiveness, SEO signals, page speed, and AIO readiness (structured data for AI search results). 30 parallel workers, processes about 12 sites per second.

4. cold email generation: for every lead scoring below 35, the system generates a personalized 3-email sequence. the first email links to a live demo site i've already built for their industry. i have 16 demo sites live right now (dental, restaurant, fitness, legal, plumber, realtor, plus premium motion versions of each).

5. demo sites: all hosted on surge.sh. $0/month. SSL included. they look like real client sites so the business owner can see exactly what they'd get.

**current numbers**

- 1,454,245 unique domains in the pool
- 30,200 websites analyzed
- 2,618 "hot" leads (score >= 65, meaning their site is bad and they're likely spending money on their business)
- 15,739 "warm" leads (score 45-64)
- 58,295 cold emails pre-drafted
- 19 live demo sites deployed

**what's next**

need to set up email infrastructure (warmed inbox, SPF/DKIM/DMARC, probably use Instantly or similar). then start sending in small batches to test reply rates.

pricing model is $500 for a basic site, $1,500 for a premium with animations, $3,000 for the full package with ongoing SEO. using AI tools (Lovable, Bolt, v0) i can build a custom site in 2-4 hours. so even the $500 tier has solid margins.

**honest caveats**

- $0 revenue so far. pipeline is loaded but nothing has been sent yet.
- cold email deliverability is the big unknown. if emails land in spam, none of this matters.
- the scoring system has false positives. some "bad" sites are actually fine for the business (a plumber doesn't need a beautiful website if they get all their leads from Google Maps).
- i built the analysis engine, not the sales engine. closing deals is a different skill set.

happy to answer questions about the technical side. the scraping, scoring, and email generation are all Python. everything runs via cron overnight.

---

---

## Additional tweets (research pipeline session)

### Tweet 6 (research pipeline)

built a pipeline that scrapes 116 twitter accounts + my bookmarks + 20 subreddits every morning at 5:30 AM. extracts alpha, scores it 0-100, auto-filters into APPROVED / PENDING / ENGAGEMENT_BAIT.

first run: 1,153 raw posts. 748 new alpha entries. 111 auto-approved. 27 pieces of content generated automatically.

runs via cron. i never touch it again.

### Tweet 7 (sourcing intel)

US customs data is public. every container that enters the country has an importer, supplier, and product description on file.

i built a scraper that pulls factory intel from ImportYeti. searched "led face mask." found 8 factories in Shenzhen. one has 1,487 shipments to US companies. contact URLs auto-generated.

this is how you find the exact factory your competitor uses. for free.

### Tweet 8 (iOS compliance)

apple rejects 40%+ of first-time app submissions. most common reason: missing PrivacyInfo.xcprivacy.

built a wrapper around RevylAI Greenlight (MIT, free) that scans all 6 of my apps before submission. checks 30+ rejection patterns, validates privacy manifests, flags fake content.

ran it on my portfolio. every app was missing the privacy manifest. fixed all 6 in one command.

### Tweet 9 (automation philosophy)

every session i build: the thing + the automation that runs the thing forever.

today: research pipeline + cron job. factory scanner + cron job. health monitor + cron job.

i will never manually run any of these again. they run at 4 AM, 5:30 AM, 5:45 AM, 6:30 AM, 7:30 AM. every day. while i sleep.

the system grows every session. it never shrinks.

## Voice check

- [x] Zero em dashes
- [x] Zero banned AI vocabulary
- [x] Consequence-first hooks
- [x] Specific numbers (30,200 / 2,618 / 1,454,245 / 58,295 / 19 / 11)
- [x] Would @pipelineabuser post this? yes
- [x] Lowercase energy
- [x] No "It's not just X, it's Y" patterns
- [x] No promotional adjectives
- [x] First sentence delivers value in every piece
- [x] One hedge max per sentence

---

*Disclaimer: Results not typical. Individual results vary based on effort, market conditions, and other factors.*
