# Cold Email Playbook: SaaS Edition
## Get Your First 10-100 Customers via Cold Outbound

*Infrastructure setup, ICP frameworks, 7 complete email sequences, deliverability rules, and the reply-to-revenue pipeline for SaaS founders doing outbound in 2026.*

---

## Who this is for

You built a SaaS product. You might have an MVP. You might have a few beta users from your network. But you need paying customers and you need them without burning $5,000 on ads or hiring a VP of Sales you can't afford.

Cold email, done correctly, is how most B2B SaaS companies get their first 10-100 customers. Not content marketing. Not SEO. Not product-led growth. Cold email.

This playbook covers everything specific to SaaS outbound: the infrastructure that keeps you out of spam when emailing corporate inboxes, the ICP work that determines everything downstream, 7 complete multi-touch sequences with subject lines and personalization, and the process for turning replies into revenue.

Expected results with correct execution: 2-4% reply rate, 15-25% reply-to-demo conversion, 20-40% demo-to-trial conversion. Your first paying customer within 30-60 days of starting.

---

## Part 1: SaaS Cold Email Infrastructure ($0 Setup)

### Why SaaS infrastructure is different from agency outreach

Agency cold email and SaaS cold email have different risk profiles.

When you're an agency owner doing outreach, a blacklisted domain hurts your ability to close clients. Painful, but recoverable.

When you're a SaaS founder, your product domain is also your application login, your support email, your billing notifications, and your user activation emails. If your product domain gets flagged as spam, your paying customers miss password resets and invoices. That kills your product.

Separation is not optional.

---

### Step 1: Domain architecture for SaaS outbound

You need three types of domains with distinct purposes:

**Domain Type 1: Product domain (do not touch for cold email)**
```
yourproduct.com — app login, billing, support, transactional email
```
Never send cold email from this domain. Never.

**Domain Type 2: Cold outreach domains (purpose-built)**
Buy 2-3 domains specifically for outbound. Budget $25-35 total.

Naming patterns that work for SaaS outbound:
```
If your product is "Relay":
- relayhq.com          (authoritative)
- tryrelay.com         (action-oriented)
- getrelay.com         (acquisition-focused)
- relayapp.io          (.io reads as tech-native)
- relay-team.com       (team/company feel)
```

Register at Porkbun ($9-11/domain) or Namecheap ($10-12/domain).

**Domain Type 3: Newsletter/nurture domain (optional at this stage)**
```
relayupdates.com — for email sequences to demo no-shows, trial users, churned accounts
```
Skip this until you have >50 active trials.

**How many outreach domains at each stage:**
```
0-50 prospects/day:   1 outreach domain, 1 inbox
50-150 prospects/day: 2 outreach domains, 2 inboxes
150-400 prospects/day: 3-4 outreach domains, 4-6 inboxes
```

Start with 2 domains. You will burn through one eventually. Having the backup ready matters.

---

### Step 2: Email provider selection for B2B SaaS outreach

Google Workspace ($6/month per inbox) remains the default for B2B SaaS outbound because:
- Corporate IT departments whitelist Google more aggressively than Microsoft
- G Suite reputation carries into the receiving server evaluation
- SPF/DKIM/DMARC setup is straightforward

Setup per outreach domain:
1. workspace.google.com/signup
2. Enter outreach domain (not product domain)
3. Create one inbox: outreach@yourdomain.com or firstname@yourdomain.com (first name performs better)
4. Starter plan ($6/month)
5. Verify domain via DNS TXT record
6. Repeat for second outreach domain

One inbox per domain to start. Do not create multiple aliases sending at volume from one domain — this triggers spam filters faster.

---

### Step 3: DNS authentication (mandatory, not optional)

Every SaaS founder skips this. Every founder who skips it wonders why they get 0 replies.

Add these DNS records to both outreach domains within 24 hours of setup:

**SPF (Sender Policy Framework)**
```
Type: TXT
Host: @
Value: v=spf1 include:_spf.google.com ~all
TTL: 3600
```
This tells receiving servers that Google is authorized to send on behalf of your domain.

**DKIM (DomainKeys Identified Mail)**
1. In Google Workspace admin: Apps > Google Workspace > Gmail > Authenticate email
2. Generate DKIM key (2048-bit)
3. Copy the TXT record and add it to your DNS
4. Click "Start authentication" in Google admin

**DMARC (Domain-based Message Authentication)**
```
Type: TXT
Host: _dmarc
Value: v=DMARC1; p=quarantine; rua=mailto:dmarc@yourproductdomain.com; pct=100
TTL: 3600
```
Set `p=none` for the first 2 weeks while you monitor reports. Move to `p=quarantine` after.

**Custom tracking domain (important for SaaS)**

If you use an email sequencer (Instantly, Lemlist, Apollo), set up a custom tracking subdomain so click/open tracking doesn't route through the tool's shared domain:
```
Subdomain: track.yourdomain.com
CNAME: pointing to your sequencer's tracking endpoint
```
This keeps your domain clean even if the sequencer's shared tracking domain gets flagged.

Verify everything at mail-tester.com — aim for 9.5/10 minimum before sending anything.

---

### Step 4: Warmup protocol for B2B SaaS outreach

Corporate spam filters evaluate new domains and new inboxes harder than established ones. A fresh Google Workspace inbox sent to corporate emails will route to spam for the first 4-6 weeks without warmup.

**Free warmup option: Instantly.ai free tier or Warmup Inbox free plan**
Both have free tiers that handle automated warmup. Connect your inbox, leave it running for 3-4 weeks, check inbox placement scores before going live.

What warmup does: sends emails between real inboxes in a warmup network, those emails get opened and marked as important, which builds a positive sending reputation before you email real prospects.

**Warmup timeline:**
```
Week 1: 5-10 warmup emails/day. Do not send real outbound yet.
Week 2: 15-20 warmup emails/day. Still no real outbound.
Week 3: 20-25 warmup emails/day. Start real outbound at 10 emails/day.
Week 4: Keep warmup running. Scale real outbound to 25-30 emails/day.
```

Warmup runs in parallel with real sending indefinitely. Never turn it off.

**Inbox placement test before launch:**
1. Set up a free GlockApps or Mail-Tester account
2. Send a test email to their seed addresses
3. Check placement across Gmail, Outlook, Yahoo, corporate Exchange
4. Target: 85%+ primary inbox. Below 70% = fix DNS before sending.

---

### Step 5: CRM setup for SaaS pipeline tracking

You do not need Salesforce. You need something that tracks where each prospect is in the cycle.

**Free option: HubSpot CRM (free tier)**
Handles contacts, companies, deals, email logging. Enough for 0-$50K ARR.

**Deal stages to set up:**
```
1. Prospect — identified, not yet emailed
2. Contacted — first email sent
3. Replied — any reply received (positive or negative)
4. Interested — expressed any interest or asked a question
5. Demo Scheduled — call on calendar
6. Demo Completed — call happened
7. Trial — in free/paid trial
8. Closed Won — paying customer
9. Closed Lost — explicit no or ghosted after demo
10. Nurture — not now, follow up in 30/60/90 days
```

Custom properties to add per contact:
- ICP score (1-5)
- Pain signal (what triggered you to reach out)
- Competitor used (if known)
- Trial start date
- Trial end date
- ARR value

**Lightweight alternative: a $0 Notion database**
Works fine at <100 active prospects. Create a table with: Name, Company, Email, Stage, Last Contact Date, Notes, Next Action. Filter by Stage. That is a functional CRM.

---

### Step 6: Three free tools for finding SaaS buyer emails

**Tool 1: Apollo.io (free tier)**
200 email credits/month free. Search by job title, company size, technology used, and industry. Best for finding VP-level and C-suite buyers at SMBs.

Search filters to use:
- Job title: "Head of Operations" / "VP Sales" / "Founder" / "CTO"
- Employee count: 10-200 (sweet spot for early SaaS)
- Technology: filter by competitor tech or adjacent tools
- Location: North America, UK, Australia (highest B2B purchasing power)

**Tool 2: Hunter.io (free tier)**
25 searches/month free. Best feature: domain search. Enter any company website, it shows all email addresses Hunter has found from that domain. Useful for finding the right person at a specific company.

Also has email verifier — paste any email, it tells you if it's valid before you send.

**Tool 3: LinkedIn (manual, free)**
Not a tool per se, but the methodology: find your ICP on LinkedIn, get their full name and company, enter into Hunter's domain search to find the email format. LinkedIn Sales Navigator is $100/month and automates this but is not necessary to start.

Bonus: Clay.com has a free tier (100 rows/month) and connects Apollo, LinkedIn, Hunter, and Clearbit into one enrichment pipeline. For building lists at scale, it is the highest-leverage tool available.

---

## Part 2: Finding Your First 100 SaaS Prospects

### ICP definition for SaaS: the four-variable framework

Vague ICP work produces vague results. "SMB companies that could use our product" is not an ICP. The following four variables define a tight ICP with enough specificity to target efficiently.

**Variable 1: Company profile**
```
Employee count:   ____ to ____ employees
Revenue range:    $____ to $____ ARR (estimate)
Industry:         Primary: ____________
                  Secondary: ____________
Geography:        ____________
Company age:      ____+ years old (established enough to have budget)
Growth signal:    Hiring? Recently funded? Expanding?
```

**Variable 2: Tech stack**
What tools does your ideal customer already use that signal they're the right fit?

Identify:
- Tools they use that your product replaces or complements
- Tools that indicate they have budget for software (e.g., Salesforce users have $1K+/year software budgets)
- Tools that indicate technical sophistication if that matters
- Tools that indicate the pain point your product solves

Example for a meeting transcription SaaS:
```
Uses: Zoom or Google Meet (they have video meetings)
Has: HubSpot or Salesforce (they care about CRM notes)
Size: 20-500 employees (big enough for meetings, small enough to not have enterprise transcription)
Pain: Sales team or CS team (needs meeting follow-up)
```

**Variable 3: Budget signal**
```
Software spend proxy: What expensive tools do they already use? Salesforce = $150+/user/month budget. HubSpot = $50-800/month budget. Intercom = $74+/month.
Company revenue proxy: Employee count x $100K average revenue per employee (rule of thumb for SMBs)
Job title spend authority: VP/Director level = $500-5K purchase authority. C-suite = $5K-50K authority.
```

Target companies where your product is less than 5% of their estimated software budget. Above that, the sales cycle gets painful.

**Variable 4: Pain signal**
This is the highest-leverage variable. A prospect who is actively experiencing the pain you solve is 5-10x more likely to reply than one who theoretically has the problem.

Pain signals to watch:
```
Posted about the problem on Twitter/Reddit/LinkedIn
Left a negative review of a competitor on G2/Capterra
Recently hired for a role that indicates the problem (e.g., hiring a "Data Analyst" = data chaos)
Recently raised funding (have budget, need to scale)
Recently posted a job for someone who would use your product
Asked a relevant question on LinkedIn, Reddit, or a Slack community
```

---

### Where to find SaaS buyers: 6 specific sources

**Source 1: G2 and Capterra reviews (highest intent)**

People who leave detailed negative reviews of competitor products are your best prospects. They have already identified the problem, already tried a solution, and are dissatisfied.

How to mine G2 reviews:
1. Go to g2.com, find your top competitor's profile
2. Filter reviews by 1-3 stars
3. Read the "Cons" section of each review
4. If the complaint matches what your product solves, find the reviewer
5. Most reviewers include their name and company — search LinkedIn for their email

What to look for in a negative review that signals high conversion potential:
- Specific complaint that your product directly solves
- Reviewer is in a decision-making role
- Company fits your ICP
- Review is recent (last 12 months)

Capterra follows the same process. Both sites index thousands of reviews per product category.

**Source 2: Product Hunt launches**

When a SaaS launches on Product Hunt, their upvoters and commenters are people already interested in that problem space. These are your prospects.

Find launches relevant to your category:
1. producthunt.com/search — search your category or competitor names
2. Look at launches from the last 6-12 months
3. Check the comments — who is asking questions or expressing interest
4. Export the email of anyone who says "Would love to try this" or "We use X now and this looks better"

Product Hunt also has an API that lets you pull upvoter data programmatically if you are comfortable with Python.

**Source 3: LinkedIn signal-based targeting**

Beyond basic job title search, LinkedIn's search operators let you find buyers showing active pain signals:

Search examples:
```
"looking for a [your category] tool" — people who posted about needing a solution
"switched from [competitor]" — people who have already evaluated the space
"we're hiring [role that uses your product]" — companies expanding into your use case
"[competitor name] alternative" — prospects who are evaluating options
```

LinkedIn Sales Navigator advanced search (worth the 30-day trial for list building):
- Filter by "Changed jobs in past 90 days" — new decision-makers often replace legacy tools
- Filter by "Posted on LinkedIn in past 30 days" — active, reachable prospects
- Filter by company headcount growth — companies growing fast need your tooling

**Source 4: GitHub (for developer-focused SaaS)**

If your product serves developers or technical teams, GitHub is a prospect goldmine.

Methods:
- Search for repositories that use competing open source tools or libraries
- Stars on competing open-source projects = prospect list (many have emails in their profiles)
- Issues on competing repos where users complain about limitations
- "Show HN" posts on Hacker News for companies in your space

Hacker News "Who's Hiring" threads (posted monthly) include company names, tech stacks, and sometimes specific tooling. Cross-reference with Apollo to find emails.

**Source 5: Community mining (Reddit, Slack, Discord)**

SaaS buyers ask questions in public communities. These are real-time pain signals.

Reddit searches to run weekly:
```
subreddit:entrepreneur "looking for a tool that"
subreddit:SaaS "[competitor name]"
subreddit:startups "anyone know a good [category]"
subreddit:smallbusiness "automate [problem your product solves]"
```

Slack communities where your buyers congregate:
- RevGenius (sales and revenue leaders)
- Pavilion (sales/CS leadership)
- Demand Curve (growth and marketing)
- Indie Hackers Discord (founders)
- Product Hunt Makers (product people)
- Ramen Club (B2B founders)

Find someone who asked a relevant question → Google their name + company → find email → personalize your outreach with their exact question as context.

**Source 6: Funding announcements (Crunchbase, TechCrunch)**

Companies that just raised funding are in an ideal state for outbound: they have budget, they are scaling, and they are hiring. Decision-makers who just raised are actively spending on tooling.

Crunchbase free tier: filter by funding round (Seed, Series A), date (last 90 days), industry.

TechCrunch and VentureBeat publish daily funding announcements. Set up a Google Alert for "[your industry] funding" or "[your buyer role] startup funding."

Signal strength by round:
```
Pre-seed ($500K-$2M): founders are still doing everything, not yet buying tools at scale
Seed ($2M-$5M): hiring first team, actively buying tools, price-sensitive but open
Series A ($5M-$15M): best target, have budget, scaling fast, actively evaluating vendors
Series B+ ($15M+): enterprise sales cycle kicks in, harder to reach decision-makers
```

---

### Building prospect lists from competitor review sites

This is the single highest-ROI prospecting method for early-stage SaaS. Here is the full workflow:

1. Identify 3-5 direct competitors with G2/Capterra profiles
2. Pull all 1-3 star reviews from the last 18 months
3. For each review:
   - Read the "Cons" section
   - Does it match what your product solves? Flag it.
   - Get reviewer name and company from their profile
4. Search reviewer on LinkedIn — confirm role and company
5. Enter company domain into Hunter.io — get email
6. Log in your CRM: Name, Company, Email, Specific Complaint (this becomes your personalization)
7. Email them with their specific complaint as your hook

Expected output: 50-150 prospects per competitor per quarter from this method alone. Open rates on these emails consistently run 55-70% because the personalization is genuine, not template noise.

---

### Signal-based prospecting: 5 specific templates

**Template 1: Recently Raised Funding**
```
Trigger: Company announced Seed or Series A in last 60 days
Source: Crunchbase, TechCrunch
Build the list:
- Filter Crunchbase: [your industry] + Seed/Series A + funded in last 60 days
- Get founder/VP name from LinkedIn
- Get email from Apollo or Hunter
- Note: round size, investors, what the funding will be used for (usually in the announcement)
Personalization hook: "Congrats on the [round size] raise from [investor]. Saw you're scaling [specific mention from announcement]."
```

**Template 2: Competitor Negative Reviewer**
```
Trigger: Left 1-3 star review of [competitor] on G2/Capterra
Source: G2, Capterra
Build the list:
- Go to competitor G2 profile, filter 1-3 stars, last 12 months
- Screenshot the specific complaint that your product solves
- Find reviewer name on review, search LinkedIn for email via Hunter
- Log their exact complaint verbatim
Personalization hook: "You mentioned on G2 that [exact quote from their review]."
```

**Template 3: Active Job Posting**
```
Trigger: Company posted a job that indicates they need your product
Source: LinkedIn Jobs, Indeed, Lever/Greenhouse job boards
Build the list:
- Search: "[role that uses your product]" + company size + industry
- Example: "Head of RevOps" = company needs revenue operations tooling
- Find hiring manager or relevant decision-maker at that company
- Note the specific skills they're hiring for (tells you their current pain)
Personalization hook: "Saw you're hiring a [role] — that usually means [pain point your product solves] is becoming a priority."
```

**Template 4: Posted About the Pain**
```
Trigger: Posted on LinkedIn/Twitter/Reddit about a problem your product solves
Source: LinkedIn search, Twitter/X search, Reddit search
Build the list:
- Set up saved searches for pain-point keywords in your category
- Check weekly, log anyone who posted about the problem in the last 30 days
- Get email from LinkedIn or Apollo
- Copy the exact post link and text for your reference
Personalization hook: Reference their exact post. Quote it. Show you read it.
```

**Template 5: Churned from Competitor**
```
Trigger: Switched away from a competitor product (public post or review)
Source: Twitter/X search ("[competitor] alternative"), G2 reviews, Reddit
Build the list:
- Twitter search: "[competitor name] switched" OR "[competitor name] alternative" OR "leaving [competitor]"
- G2 reviews where they say "We moved to X after using this" (shows they're still evaluating)
- Log: who, what they switched from, why, when
Personalization hook: "Saw you moved away from [competitor]. Curious what specifically wasn't working — we built [your product] to fix exactly that."
```

---

## Part 3: SaaS Cold Email Sequences (7 Templates)

All sequences follow the same structure: initial email (Day 1) + follow-up 1 (Day 4) + follow-up 2 (Day 8). At Day 8, if no reply, mark as Closed Lost and move on. Do not send a fourth email. It damages deliverability and annoys prospects without meaningfully increasing conversion.

Personalization placeholders use [BRACKETS]. Fill these in before sending. Do not send with placeholders visible.

---

### Sequence 1: The Better Alternative

Use when: prospect is using a direct competitor. Best source: G2/Capterra reviews, LinkedIn job postings listing competitor tools, Apollo tech stack filters.

Reply rate benchmark: 3-6% (higher when personalized with their specific complaint)

**Email 1 (Day 1)**
```
Subject: [Competitor name] alternative for [Company name]

Hi [First name],

[Specific thing they said about the competitor, or the specific limitation of the competitor relevant to their company size/use case].

We built [Your product] specifically for [their type of company]. The difference:

[Competitor]: [one limitation]
[Your product]: [how you solve it]

Teams like [similar company] switched and [specific result in their first 30/60 days].

Worth a 20-minute look? I can show you the specific workflow for [their use case].

[Your name]
[Title, Company]
```

**Follow-up 1 (Day 4)**
```
Subject: Re: [Competitor name] alternative for [Company name]

Hi [First name],

Following up on my note from a few days ago.

One thing worth mentioning: [specific feature or capability that's different from competitor] is something [Company name]-sized teams consistently flag as the reason they switched.

If it's not the right time, no problem — just let me know and I won't follow up again.

[Your name]
```

**Follow-up 2 (Day 8)**
```
Subject: Re: [Competitor name] alternative for [Company name]

Last note on this from me, [First name].

If you're locked into [competitor] for now, no problem at all. But if you're reevaluating your [category] stack in the next quarter, I'm happy to do a quick comparison specific to [Company name]'s workflow — no pitch, just a technical comparison.

[Your name]
[Direct calendar link or email to reply]
```

---

### Sequence 2: The Integration Play

Use when: prospect uses tools that your product integrates with. Best source: Apollo tech stack filter, job postings that list tool requirements, LinkedIn profiles of operations/RevOps roles.

Reply rate benchmark: 4-7% (integration relevance is high-intent)

**Email 1 (Day 1)**
```
Subject: [Your product] + [Tool they use] for [Company name]

Hi [First name],

[Tool they use] users at companies like [Company name] typically spend [X hours/week] on [specific manual task] because [tool] doesn't [specific capability gap].

[Your product] connects directly to [their tool] and [specific outcome — pulls the data automatically / eliminates the manual step / closes the loop between X and Y].

[Similar company] set it up in one afternoon and [specific result].

I can walk you through the [Tool] integration specifically — takes 20 minutes. Does [day/time] work?

[Your name]
```

**Follow-up 1 (Day 4)**
```
Subject: Re: [Your product] + [Tool they use]

Hi [First name],

Quick add to my last note: the [Tool] integration we built handles [specific edge case or common problem with the integration they're probably familiar with].

Most teams we work with had tried [alternative approach] before finding us — if that's where you are, worth comparing.

Happy to send a 3-minute Loom walkthrough of the integration if that's easier than a call.

[Your name]
```

**Follow-up 2 (Day 8)**
```
Subject: Re: [Your product] + [Tool they use]

Last one from me, [First name].

If the [Tool] workflow is working fine for you, that's genuinely good to hear. If you ever find yourself needing [specific capability your integration provides], feel free to reach out.

One resource that might be useful regardless: [link to integration documentation or a relevant case study]. No sign-up required.

[Your name]
```

---

### Sequence 3: The ROI Calculator

Use when: prospect is cost-conscious or at a company size where ROI justification matters to get budget approved. Best source: Series A companies, mid-market companies with procurement processes, operations roles.

Reply rate benchmark: 2-4% (lower volume but higher quality replies when it lands)

**Email 1 (Day 1)**
```
Subject: What [Company name] is losing to [specific problem]

Hi [First name],

Quick math for [Company name]:

[Specific process your product automates]: [X] hours/week x [average loaded cost/hour for their role] = $[calculated annual cost]

[Your product] automates [that process]. Setup takes [X hours]. First-year ROI for a [their size] team: $[realistic number] saved.

[Similar company at their stage] ran this math before signing up. They were at $[X cost per year] on [process]. They're now at $[Y cost per year].

I built a 5-minute calculator specific to [their company size/type]. Want me to send it over?

[Your name]
```

**Follow-up 1 (Day 4)**
```
Subject: Re: What [Company name] is losing to [specific problem]

Hi [First name],

To make the ROI case concrete for [Company name] specifically:

- [Their likely team size doing this task]: [X] people
- Average hours spent on [process] per week: [Y]
- Loaded cost per hour: $[Z]
- Annual cost of the current approach: $[X x Y x Z x 52]

[Your product] cost at [their company size]: $[monthly price x 12]/year

Net annual savings: $[math]

These are conservative estimates. Happy to refine with your actual numbers on a call.

[Your name]
```

**Follow-up 2 (Day 8)**
```
Subject: Re: What [Company name] is losing to [specific problem]

Last note, [First name].

If the ROI framing isn't the right angle for [Company name] right now, I'm not going to keep pushing it. Different companies prioritize differently.

If it becomes relevant, the calculator I mentioned is at [link] — no email required to use it.

[Your name]
```

---

### Sequence 4: The Case Study Drop

Use when: you have a relevant success story from a customer similar to the prospect. Similar means: same industry, same company size, or same specific problem. Do not use a case study from a 500-person enterprise when emailing a 15-person startup.

Reply rate benchmark: 3-5%

**Email 1 (Day 1)**
```
Subject: How [Similar company] [specific result] with [Your product]

Hi [First name],

[Similar company] — [industry, similar size to prospect's company] — was dealing with [specific problem the prospect likely has].

[What they tried before your product]. [Why it wasn't working].

After switching to [Your product]: [specific result with a number]. [Time frame].

The setup for their [specific workflow] was [X hours]. They were up and running before the end of the week.

I think [Company name] has a similar situation based on [specific observation about them — their tech stack, their size, their industry]. Would it be worth a 20-minute call to walk through what we did for them?

[Your name]
```

**Follow-up 1 (Day 4)**
```
Subject: Re: How [Similar company] [specific result]

Hi [First name],

One detail from that [Similar company] implementation worth mentioning:

[Specific technical or workflow detail that would be relevant to this prospect specifically].

For [Company name], that would mean [translated benefit to their context].

Happy to send the full case study writeup — it covers the implementation in detail. Want me to send it over?

[Your name]
```

**Follow-up 2 (Day 8)**
```
Subject: Re: How [Similar company] [specific result]

Last one from me, [First name].

Full case study is here if it's ever useful: [link]

If the timing isn't right, I get it. The door's open if [Company name]'s situation changes.

[Your name]
```

---

### Sequence 5: The Free Audit

Use when: you can offer a genuine assessment of their current process that has standalone value, regardless of whether they buy. Works best for SaaS products where the audit reveals the problem the product solves.

Examples: SEO tool offering a site audit, data tool offering a pipeline audit, security tool offering a vulnerability scan.

Do not offer an audit if your product doesn't actually generate insight from their existing data. An audit that's just a sales call in disguise damages your credibility.

Reply rate benchmark: 5-9% (highest-converting sequence when the audit has real value)

**Email 1 (Day 1)**
```
Subject: Free [specific audit type] for [Company name]

Hi [First name],

I built a [specific audit] for [Company name] — takes me about 20 minutes to run, costs you nothing.

What it covers: [3-4 specific things the audit examines, with enough detail that it sounds real]

What you get: [specific deliverable — a report, a score, a list of issues, a benchmark comparison]

No pitch at the end. If the audit shows [Company name] has [problem your product solves], I'll mention what we do. If it doesn't, I'll say so.

Want me to run it?

[Your name]
```

**Follow-up 1 (Day 4)**
```
Subject: Re: Free [specific audit type] for [Company name]

Hi [First name],

Still happy to run that [audit] for [Company name].

One thing I should mention: I ran similar audits for [2-3 companies in their space] recently. The average finding was [specific benchmark — "47% of their [X] had [problem Y]" or "they were leaving $[X] on the table in [area]"].

Not saying that's true for [Company name]. That's exactly what the audit would tell you.

15 minutes to review the results together if I send it over?

[Your name]
```

**Follow-up 2 (Day 8)**
```
Subject: Re: Free [specific audit type] for [Company name]

Last note, [First name].

The offer stands if you want it later. My calendar is at [link] if it makes sense to grab time.

[Your name]
```

---

### Sequence 6: The Mutual Connection

Use when: you share a genuine community, event, investor, accelerator, or mutual contact. This is not "we're both on LinkedIn." It is a real shared context.

Valid shared contexts: same accelerator batch, same investor portfolio, same Slack community where you've both been active, same conference in the past 90 days, mutual introduction from a real contact.

Do not fabricate shared contexts. It reads immediately as spam and destroys trust before the conversation starts.

Reply rate benchmark: 7-12% (highest when the shared context is recent and specific)

**Email 1 (Day 1)**
```
Subject: Fellow [shared context] founder — quick intro

Hi [First name],

[How you know the shared context — "I'm in the YC W25 batch", "I saw your talk at SaaStr last month", "We're both in the Demand Curve Slack — I've seen your posts on [topic]"].

I'm building [Your product] — [one sentence description].

Thought there might be a fit for [Company name] specifically because [specific reason tied to what you know about them from the shared context].

Are you open to a quick call? Even just to trade notes — [shared context community] founders tend to have useful pattern matching on [relevant topic].

[Your name]
```

**Follow-up 1 (Day 4)**
```
Subject: Re: Fellow [shared context] founder

Hi [First name],

Following up on my note. I know inboxes are brutal.

One question, no agenda attached: [genuine question related to something they've shared publicly or a relevant problem in the shared community]. Curious how [Company name] handles it.

[Your name]
```

**Follow-up 2 (Day 8)**
```
Subject: Re: Fellow [shared context] founder

Last one from me, [First name].

If the timing is off, no problem. [Shared context] community is small enough that I'm sure we'll cross paths.

[Your name]
```

---

### Sequence 7: The Problem-Aware

Use when: prospect recently posted about the exact problem your product solves. The post can be on Reddit, Twitter/X, LinkedIn, Hacker News, a relevant Slack community, or any public forum. This is the highest-personalization sequence.

The key: quote their words back to them. Not paraphrase. Quote.

Reply rate benchmark: 8-15% (highest-performing sequence with maximum personalization)

**Email 1 (Day 1)**
```
Subject: Re: your post about [specific problem]

Hi [First name],

Came across your [post/comment/thread] on [platform] from [X days/weeks ago]:

"[Exact quote from their post about the problem]"

That's exactly what [Your product] was built to solve.

[One sentence on how your product addresses their specific complaint, using their words as much as possible].

[Similar company] was at the same point [timeframe] ago. [Specific result after using your product].

Worth a 20-minute look? I can show you specifically how it would work for [their use case as described in their post].

[Your name]
```

**Follow-up 1 (Day 4)**
```
Subject: Re: your post about [specific problem]

Hi [First name],

Still thinking about your point on [specific element from their post].

One thing that might be useful regardless of whether [Your product] is the right fit: [genuine resource, article, or insight related to their problem that has standalone value].

[Your name]
```

**Follow-up 2 (Day 8)**
```
Subject: Re: your post about [specific problem]

Last one, [First name].

If you've already solved this or found a different approach, I'd genuinely be curious what worked.

If not, happy to do a quick walkthrough whenever it makes sense.

[Your name]
```

---

## Part 4: SaaS-Specific Deliverability

### B2B inbox placement tactics

Corporate email servers (Microsoft Exchange, Google Workspace on company domains) have stricter filters than consumer Gmail. The tactics that work for B2C email outreach fail on B2B targets.

**What corporate filters evaluate:**
- Domain age and reputation (new domains = high spam probability)
- Sending volume versus domain history (jumping from 0 to 100 emails/day immediately = flagged)
- Text-to-link ratio (lots of links = spam)
- HTML complexity (heavily formatted emails route to promotions or spam)
- Reply rate (low reply rate signals your emails are unwanted)
- Unsubscribe rate (if people mark you as spam, your domain reputation drops permanently)

**What to do:**

Send plain text, not HTML. Corporate filters treat HTML email with multiple images, bolded headers, and styled buttons as marketing email. Marketing email goes to promotions. Cold outreach goes to primary. Write emails like they are internal company messages, not newsletters. No fancy signatures with logos. No header images. No "Click here to book a demo" buttons.

Keep emails short. Under 150 words for initial email. 75-100 words for follow-ups. Longer emails have lower reply rates and worse deliverability because they pattern-match to sales automation.

One link maximum per email. If you include a calendar link, that is your one link. No additional links to case studies, websites, or documentation in the same email.

Avoid spam trigger words. The obvious ones are still flagged: "free trial," "no obligation," "limited time offer," "guaranteed." Less obvious ones that corporate filters hate: "synergy," "leverage," "best-in-class," "revolutionary," "game-changing." Write like a human, not a press release.

Use question-based CTAs, not link-based CTAs. "Worth a 20-minute call?" performs better than "Book time here: [link]" in both reply rate and deliverability.

**Monitoring tools:**
- GlockApps (inbox placement testing, $5/month): test new templates before sending to real prospects
- Google Postmaster Tools (free): monitor your domain's spam rate and reputation
- MxToolbox (free): check if your domain is on any blacklists

Check your spam rate weekly. If Gmail Postmaster shows your spam rate above 0.1%, stop sending immediately and diagnose.

---

### Avoiding spam filters when sending to corporate emails

Corporate IT departments often whitelist known vendors and blacklist unfamiliar sending domains aggressively. Here is what pushes you past those filters:

**Consistency of sending behavior.** Send at the same times each day. Do not send 0 emails Monday through Thursday and 200 on Friday. Spam patterns are often identified by volume spikes.

**Reply activity.** When prospects reply to your emails, even with "not interested," it signals to email providers that your emails are wanted. This improves your domain reputation. A 2% reply rate is better for your domain than a 0% reply rate, even if the replies are negative.

**Bounce management.** Hard bounces (emails to addresses that don't exist) are the fastest way to damage your sending reputation. Verify every email before sending using NeverBounce or ZeroBounce. Target: below 2% bounce rate. Above 5% bounce rate means your list quality is poor and your domain will get flagged.

**Removing non-responders.** After 3 emails with no response, remove the prospect from future sends. Continuing to send to cold contacts depresses your engagement rate and signals low-quality sending behavior to inbox providers.

**Using a custom sending subdomain.** When configuring your sequencer, point sends through outreach.yourdomain.com rather than yourdomain.com. This isolates cold email sending reputation from any transactional email sent via the root domain.

**Separate sending IP per domain.** If your sequencer allows dedicated IP addresses (Lemlist and Smartlead have this), use them. Shared sending IPs mean your reputation is tied to other users on that IP, some of whom will spam.

---

### Optimal send times for B2B SaaS by company size

**Startups (1-25 employees)**
- Best days: Tuesday, Wednesday, Thursday
- Best times: 7:30-8:30 AM recipient local time (before their day starts), or 5:00-6:00 PM (end of day scroll)
- Worst: Monday morning (planning chaos), Friday afternoon (checked out)
- Decision-maker: usually founder/CEO, who checks email throughout the day

**SMBs (25-200 employees)**
- Best days: Tuesday, Wednesday
- Best times: 8:00-9:30 AM recipient local time
- Worst: Monday through Wednesday after 3 PM (in meetings)
- Decision-maker: VP or Director level, tends to check email in the morning before meetings start

**Mid-market (200-1000 employees)**
- Best days: Tuesday, Thursday
- Best times: 8:00-9:00 AM, or 12:00-1:00 PM
- Worst: End of quarter (budgets are locked, everyone is in sales review mode)
- Decision-maker: Director or VP who has budget authority but reports to a C-suite

**Enterprise (1000+ employees)**
Not the target for cold email at early SaaS stage. Enterprise sales cycles take 6-18 months and require a different motion entirely. Focus on SMB and mid-market until $1M ARR.

**General rules regardless of company size:**
- Send at recipient's local time, not your local time. Use your sequencer's time-zone detection.
- Never send on holidays. Use a sequencer that blocks major US/UK holidays automatically.
- Tuesday and Wednesday have consistently higher open rates than Monday, Thursday, or Friday across all research on B2B cold email timing.

---

### Volume scaling: 50/day to 200/day without burning domains

**The scaling ladder:**

```
Week 1-2 (warmup only): 0 real sends. 20-30 warmup emails/day.
Week 3: 10 real sends/day. Keep warmup running.
Week 4: 20 real sends/day.
Week 5: 35 real sends/day.
Week 6: 50 real sends/day.
Week 8: 75 real sends/day (consider adding second domain/inbox here).
Week 10: 100 real sends/day across 2 domains.
Week 12: 150 real sends/day across 3 domains.
Week 16: 200 real sends/day across 4 domains.
```

Never increase volume by more than 25-30% per week. Volume spikes are the most common cause of deliverability collapse.

**The 50-email-per-inbox-per-day ceiling:**
Do not send more than 50 emails per day per inbox. At 50+/day, deliverability starts to decline measurably. To scale past 50/day, add inboxes on new domains.

**Scaling from 1 domain to 4 domains:**
```
Domain 1 (Month 1-2): 1 inbox, up to 50 emails/day
Domain 2 (Month 2-3): 1 inbox, 50 emails/day. Rotate sends between D1 and D2.
Domain 3 (Month 3-4): 1 inbox, 50 emails/day.
Domain 4 (Month 4+): 1 inbox, 50 emails/day.
Total capacity at 4 domains: 200 emails/day.
```

**Protecting domain health when scaling:**
- Keep warmup running on all domains in parallel, indefinitely
- Monitor Google Postmaster for each sending domain weekly
- If any domain drops below 85% inbox placement, pull it out of rotation and diagnose before resuming
- Keep a "clean" domain in reserve — one domain that has never sent, warmed up and ready to replace any domain that gets burned

---

## Part 5: Converting Replies to Revenue

### Reply categorization

Every reply you receive falls into one of four categories. Mishandling the category is where most SaaS founders lose deals.

**Category 1: Interested**
Signs: any question about pricing, features, implementation, or timing. Any "how does X work" or "we might be interested." Any "can you send more info."

Wrong response: sending a PDF or a wall of text with every feature listed.
Right response: ask one clarifying question to qualify, then offer a specific time for a call.

Example reply:
```
"This looks interesting. Can you send more information?"
```

Right response:
```
"Happy to — before I send anything, quick question: what's the specific part of [pain point] that's most pressing right now? Helps me send what's actually relevant rather than everything we have.

Either way, easiest path is probably a 20-minute call. I can show you exactly how it would work for [their company]. Does [day] or [day] work?"
```

**Category 2: Objection**
The prospect is interested but has a concern they're testing you with. See the objection handling section below.

**Category 3: Not Now**
Signs: "good timing but we're mid-budget cycle," "we're locked into a contract until [date]," "we just implemented something else."

Wrong response: giving up or disappearing.
Right response: nail down a specific re-engagement date and put them in your 30/60/90 day nurture.

```
"That makes sense — thanks for the context. When would make sense to revisit? I'll put a note in my calendar and reach out then."
```

Get a specific month. Put them in a calendar reminder. Reach out then with a fresh email (not a reply to the original thread — start fresh).

**Category 4: No**
Signs: "not a fit," "we have this handled," "please don't contact me again."

Wrong response: arguing, asking why, sending a follow-up anyway.
Right response: acknowledge and close cleanly.

```
"Understood — thanks for letting me know. I'll remove [Company name] from my list. If anything changes, you know where to find me."
```

Mark as Closed Lost in CRM. Do not email again. Emailing after a hard no is both ineffective and legally problematic in some jurisdictions (CAN-SPAM, GDPR).

---

### SaaS demo booking flow

The goal of cold email is a demo, not a close. The demo is where you close. Keep the email CTA focused on a single, low-friction next step.

**Best CTA structures for SaaS cold email:**
```
High friction (avoid): "Book a 45-minute onboarding session using this link: [Calendly with 20 fields to fill out]"
Low friction (use): "Worth a 20-minute call? If yes, [day] or [day] works well for me."
```

When a prospect says yes to a call:
1. Send the calendar link immediately (respond within 2 hours max)
2. Confirm the meeting 24 hours before with a reminder
3. Send a 2-sentence pre-call context email: "For our call tomorrow — we'll cover [X], [Y], [Z]. If you have a specific use case in mind, feel free to share beforehand so I can tailor the demo."

**Demo structure for early SaaS:**
```
Minutes 0-2:   Confirm pain point ("Before I show you anything, help me understand — what specifically prompted you to take this call?")
Minutes 2-8:   Show the one thing that solves their stated pain. Not a full feature tour.
Minutes 8-12:  Show how it would work for their specific company. Use their data if possible.
Minutes 12-18: Pricing discussion. Handle objections.
Minutes 18-20: Next step: trial, pilot, or decision timeline.
```

Do not do feature tours. Show the solution to their stated problem. Everything else is noise until they've decided they want the product.

---

### Objection handling scripts (5 common SaaS objections)

**Objection 1: "We already use [competitor]"**

Wrong: "Oh, we're actually better than [competitor] because..."
Right: "Good to know. How long have you been on it, and is it fully doing what you need?"

If they say it is working: "Makes sense to stick with what works. Mind if I check back in six months in case anything changes?"

If they pause or say "mostly": "What's the thing it doesn't quite nail?" This opens the door. Listen. Then answer with your product's strength against that specific gap.

**Objection 2: "We don't have budget right now"**

Wrong: "We have a discount if you sign before end of month."
Right: "When does your budget cycle reset? We work with a lot of companies between cycles."

Alternatively: "What's your current cost of [the problem your product solves] — either in dollars or time? Sometimes the math shifts the conversation."

If they give you a re-engagement date, use it. Budget timing is a real objection, not a brush-off.

**Objection 3: "We can build this internally"**

Wrong: panic, undersell the product, match their build cost.
Right: "Totally understand — what's your build timeline looking like?"

Most companies underestimate build time by 3-5x. If they say "a few months," they mean 6-18 months. Ask: "What's the cost of the problem while you're building? And what happens if priorities shift and the build gets deprioritized?"

Then: "Teams that build internal versions of [your category] usually end up maintaining them forever. [Your product] means your engineers are working on your product, not on infrastructure."

**Objection 4: "This isn't a priority right now"**

Wrong: pushing harder, sending more information, following up weekly.
Right: "That's fair — what is the priority right now?"

Listen. Find where your product intersects with their actual priority. If it doesn't: "Makes sense. When do you think this would move up the list?" Get a timeframe and use it.

**Objection 5: "Your price is too high"**

Wrong: immediate discount, "we can be flexible," sending a lower-tier pricing breakdown.
Right: anchor to value first. "What's too high relative to — your budget, or the value you'd get from it?"

If budget: "What range works for you? There might be a starting plan that makes sense, and you can expand as you grow."

If value: "What outcome would justify the price for [Company name]?" Get their number. Then show how your product achieves it with specifics.

Do not discount in the first conversation. Discounting immediately signals that the original price was not real, which destroys confidence in your pricing across all conversations.

---

### Free trial vs paid trial decision framework

SaaS founders often default to free trials because it removes friction. The data on this is more nuanced.

**When free trials work:**
- Product has fast time-to-value (user sees benefit within the first session)
- Setup is low-friction (no data import, no team onboarding, no configuration)
- Product is self-explanatory without a sales engineer
- Target buyer is technical and self-directed

**When paid trials work better:**
- Product requires meaningful setup investment
- Your ICP includes mid-market companies where "free" signals low quality
- You need to qualify serious buyers from tire-kickers
- You have limited onboarding capacity

**The hybrid: credit card required, refundable**
Collect payment info at trial start, refundable within 14-30 days, no charge until trial converts. This filters out non-serious trials without fully removing friction.

Data point: companies that require a credit card at trial see 40-60% lower trial starts but 2-3x higher trial-to-paid conversion. Net result is usually higher revenue per outbound dollar spent.

For early-stage SaaS (pre-$10K MRR): start with free trials to learn what actually drives activation and conversion. Optimize the onboarding first. Switch to paid trials or credit-card-required once you know what "good" looks like.

---

### 30/60/90 day pipeline nurture

Not every prospect is ready to buy when you first reach them. A structured nurture turns "not now" into closed deals over time.

**The 30-day check-in**
For prospects who said "not now" or ghosted after positive early signals:
```
Subject: Checking in — [Company name]

Hi [First name],

It's been about a month since we last spoke. [Relevant development since then — new feature, new case study, or reference to something happening in their space].

Still happy to do a quick walkthrough if the timing is better now.

[Your name]
```

Keep it short. Reference the previous conversation. One sentence on what's new. One ask.

**The 60-day value drop**
Send something useful regardless of whether they respond. A short piece of content, a benchmark, or a relevant insight specific to their industry.
```
Subject: [Relevant data point for their industry]

Hi [First name],

[Data point or insight relevant to their specific situation — not generic, not marketing copy].

Thought this might be useful for [Company name] given [what you know about their business].

[Your name]
```

No ask in this email. Just value. This keeps you top of mind without being pushy.

**The 90-day re-engage**
```
Subject: Still relevant for [Company name]?

Hi [First name],

We've both been busy. Wanted to check in one more time before I stop reaching out — is [problem your product solves] something [Company name] is still dealing with, or has it been handled?

[Your name]
```

This is the last touch in the 90-day sequence. After this, mark as dormant. Reach out again only if they show a new signal (new funding, new hire, new public post about the pain).

**Nurture segmentation:**
Not all "not now" prospects are equal. Track:
- Why they said not now (budget, timing, competitor contract)
- When the constraint lifts
- Any relevant news about their company in the interim

The prospect who said "our [competitor] contract runs through Q3" should get a targeted email in late Q2, not a generic re-engagement template.

---

## Benchmarks and Metrics Reference

Use these to calibrate your expectations and diagnose performance:

**Cold email industry benchmarks (B2B SaaS, 2025-2026):**
```
Open rate:         40-60% (with domain warming and plain text)
Reply rate:        2-5% average, 5-10% with tight ICP and strong personalization
Positive reply:    20-30% of all replies (the rest are objections, not nows, or nos)
Reply-to-demo:     15-25% (of all replies, positive and mixed)
Demo-to-trial:     20-40%
Trial-to-paid:     15-25% (no credit card) / 40-60% (credit card required)
```

**What low metrics mean:**
```
Low open rate (<30%):      Deliverability problem. Fix DNS, warmup, or sending volume.
Low reply rate (<1%):      Wrong ICP, wrong sequence, or wrong offer. Not a deliverability problem.
Low demo-to-trial (<15%): Demo is feature touring, not pain solving.
Low trial-to-paid (<10%): Onboarding problem. Prospects are not reaching their "aha moment."
```

**Weekly tracking dashboard (minimum viable):**
```
Emails sent:       ___
Open rate:         ___%
Reply rate:        ___%
Positive replies:  ___
Demos scheduled:   ___
Demos completed:   ___
Trials started:    ___
Trials converted:  ___
```

Review weekly. Diagnose by layer. A weak open rate requires different action than a weak demo-to-trial rate.

---

## Quick Reference: The SaaS Cold Email Checklist

Before sending your first batch:
- [ ] Outreach domain(s) purchased and separate from product domain
- [ ] Google Workspace set up on outreach domain(s)
- [ ] SPF, DKIM, DMARC configured on all outreach domains
- [ ] Warmup running for minimum 3 weeks before any real sends
- [ ] Inbox placement test at 85%+ on GlockApps or Mail-Tester
- [ ] CRM set up with correct deal stages
- [ ] Email verifier connected (NeverBounce or ZeroBounce)
- [ ] ICP defined across all four variables
- [ ] Prospect list built from at least 2 sources
- [ ] Pain signals identified for each prospect before sending
- [ ] Sequence selected based on prospect signal type
- [ ] All personalization placeholders filled in (no [BRACKETS] visible)
- [ ] Volume under 50 emails/day per inbox
- [ ] Custom tracking subdomain configured

Before scaling past 100/day:
- [ ] Second outreach domain warmed and ready
- [ ] Google Postmaster showing <0.1% spam rate
- [ ] Bounce rate below 2%
- [ ] Reply rate at or above 2% (if below, fix before scaling)
- [ ] At least 5 demos completed to validate the motion

---

*End of Cold Email Playbook: SaaS Edition*
