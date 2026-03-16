# Section 4: Research — 40 Production Prompts

## Market Research Prompts (121-135)

### Prompt 121: Market Size Estimation
```
Estimate the market size for [PRODUCT/SERVICE].

I need:
1. TAM (Total Addressable Market): Everyone who could theoretically use this
2. SAM (Serviceable Addressable Market): The segment I can realistically reach
3. SOM (Serviceable Obtainable Market): What I can capture in Year 1

For each level, provide:
- The number of potential customers
- Average revenue per customer (based on my pricing: [PRICE])
- Total dollar value
- Your reasoning and data sources

My product: [DESCRIPTION]
My pricing: [PRICE MODEL]
My geographic focus: [REGION]
My target customer: [WHO]

Flag any assumptions you're making so I can validate them.
```

### Prompt 122: Competitor Analysis Matrix
```
Analyze these competitors for my [PRODUCT/SERVICE]:

1. [COMPETITOR 1]
2. [COMPETITOR 2]
3. [COMPETITOR 3]
4. [COMPETITOR 4]
5. [COMPETITOR 5]

For each competitor, analyze:
- Pricing (exact plans, free tier details)
- Target customer (who they're optimized for)
- Key features (their top 5 selling points)
- Weakness (what customers complain about — check G2, Capterra, Reddit, Twitter)
- Distribution (how they acquire customers — SEO, ads, content, partnerships)
- Funding/size (bootstrapped vs. funded, team size if known)

Then provide:
- Feature gap matrix (what they all have vs. what's missing)
- The positioning white space (where NO competitor is strong)
- Recommended positioning for my product
```

### Prompt 123: Customer Pain Point Discovery
```
I'm building [PRODUCT/SERVICE] for [TARGET AUDIENCE].

Research their pain points by analyzing:
1. What questions do they ask on Reddit? (suggest 5 relevant subreddits)
2. What do they complain about on Twitter? (suggest search queries)
3. What are the 1-2 star reviews saying about competitor products?
4. What "I wish there was a tool that..." posts exist?

For each pain point found, categorize:
- Severity (hair-on-fire / important / nice-to-have)
- Frequency (how often they encounter it)
- Current workaround (what they do today)
- Willingness to pay (would they pay to solve this?)

Give me 10 pain points ranked by "willingness to pay x frequency."
```

### Prompt 124: ICP (Ideal Customer Profile)
```
Help me define my Ideal Customer Profile for [PRODUCT/SERVICE].

What I know so far:
- Product: [DESCRIPTION]
- Price: [PRICE]
- Current customers (if any): [BRIEF DESCRIPTION]

Build my ICP covering:
1. Demographics: Job title, company size, industry, revenue range
2. Psychographics: What they value, what they fear, what frustrates them
3. Behaviors: Where they hang out online, what they read, who they follow
4. Buying triggers: What event makes them start looking for a solution?
5. Objections: Top 3 reasons they'd say no and how to address each
6. Day-in-the-life: Describe a typical Tuesday for this person — where does my product fit?

Write it as a one-page profile I can reference when making product and marketing decisions.
```

### Prompt 125: Pricing Research
```
Help me price [PRODUCT/SERVICE].

Context:
- What it does: [DESCRIPTION]
- Target customer: [WHO]
- Competitors and their pricing:
  - [COMPETITOR 1]: [THEIR PRICING]
  - [COMPETITOR 2]: [THEIR PRICING]
  - [COMPETITOR 3]: [THEIR PRICING]
- My costs per customer: [COST]
- My target margin: [PERCENTAGE]

Analyze:
1. What pricing model fits best? (one-time, subscription, usage-based, freemium, credits)
2. What price point maximizes revenue? (not just signups — revenue)
3. What's the psychological anchoring strategy? (show a high price first, then my price)
4. Should I offer tiers? If yes, design 3 tiers with specific feature gates
5. What's the minimum viable price I can charge and still attract serious users? (too cheap = perceived as low quality)

Give me a pricing page mockup (text description of what each tier shows).
```

### Prompt 126: Niche Validation
```
I want to enter the [NICHE] market with [PRODUCT/SERVICE].

Validate this niche by answering:

1. Size: How many potential customers exist? (estimate with reasoning)
2. Growth: Is this market growing or shrinking? What's the trend?
3. Willingness to pay: Are people in this niche spending money on solutions? (provide examples)
4. Accessibility: Can I reach these customers without a large budget? (where do they congregate online?)
5. Competition: How crowded is it? Who are the top 3 players?
6. Defensibility: If I succeed, can someone easily copy me?

Score each dimension 1-5 and give an overall GO / CONDITIONAL / NO-GO recommendation with reasoning.
```

### Prompt 127: Trend Analysis
```
Analyze the trend trajectory for [TOPIC/INDUSTRY/TECHNOLOGY].

Provide:
1. Timeline: Key milestones in the last 3 years
2. Current state: Where is this trend right now? (early adopter, early majority, late majority, declining)
3. Growth indicators: What signals suggest this is growing? (search volume, funding, job postings, conference talks)
4. Decline indicators: What signals suggest this might be peaking?
5. Adjacent trends: What related trends are emerging?
6. Prediction: Where will this be in 12 months? In 3 years?
7. Action: What should I build/do NOW to capitalize on this trend before it's saturated?

Be specific — name companies, products, and people driving this trend.
```

### Prompt 128: Reddit Research Scrape
```
I'm researching [TOPIC] on Reddit. Help me extract insights.

Subreddits to analyze:
- r/[SUBREDDIT 1]
- r/[SUBREDDIT 2]
- r/[SUBREDDIT 3]

Search queries to use:
- [QUERY 1]
- [QUERY 2]
- [QUERY 3]

For each subreddit, identify:
1. Top 5 recurring questions/complaints
2. Tools/products people recommend (and which they trash)
3. Advice that gets heavily upvoted (this is what the community values)
4. Gaps — problems people describe that have no good solution
5. Language patterns — exact phrases people use to describe their problems (use these in marketing copy)

Format as a research brief I can reference when writing landing pages and ads.
```

### Prompt 129: SWOT Analysis
```
Perform a SWOT analysis for [MY BUSINESS/PRODUCT].

Context:
- What I'm building: [DESCRIPTION]
- My background/resources: [WHAT I BRING]
- My market: [TARGET MARKET]
- My competitors: [TOP 3 COMPETITORS]

For each quadrant, provide 5 specific points (not generic):

Strengths: What specific advantages do I have?
Weaknesses: What specific limitations will hold me back?
Opportunities: What specific market gaps or trends can I exploit?
Threats: What specific risks could kill this?

For each weakness and threat, suggest a specific mitigation strategy.
End with: "The single biggest opportunity here is _____ because _____."
```

### Prompt 130: Feature Prioritization
```
Help me prioritize these features for my [PRODUCT]:

[LIST 10-15 FEATURES YOU'RE CONSIDERING]

For each feature, score (1-5):
1. Impact: How much does this move the needle for users?
2. Effort: How long to build? (1 = day, 5 = month+)
3. Revenue: Does this directly lead to revenue?
4. Retention: Does this keep existing users coming back?
5. Differentiation: Does this set us apart from competitors?

Calculate: Impact x Revenue x Retention x Differentiation / Effort = Priority Score

Return a sorted list (highest priority first) with the score breakdown.
Include a "Must Build Now" (top 3), "Build Next" (next 3), and "Backlog" (rest) categorization.
```

### Prompt 131: Go-To-Market Plan
```
Create a go-to-market plan for [PRODUCT] launching on [DATE].

Product: [DESCRIPTION]
Price: [PRICE]
Target customer: [WHO]
Budget: [AMOUNT or "$0 — organic only"]
Goal: [FIRST MONTH TARGET — users, revenue, signups]

Cover these phases:

Pre-launch (2 weeks before):
- Where to build anticipation
- What content to create
- Who to reach out to
- Email list strategy

Launch day:
- Exactly what to post, where, and when
- Product Hunt launch plan (if applicable)
- Outreach messages to send

Post-launch (weeks 1-4):
- Content calendar
- Community engagement plan
- Feedback collection system
- Iteration priorities based on early data

For each action item, specify: platform, timing, content type, and expected outcome.
```

### Prompt 132: Survey Design
```
Design a customer research survey for [PURPOSE — e.g., "understanding why users churn", "validating a new feature idea", "pricing research"].

Requirements:
- Max 8 questions (completion rate drops after 8)
- Mix of question types: multiple choice, rating scale, one open-ended
- No leading questions (questions that suggest the "right" answer)
- Progressive disclosure (easy questions first, harder/personal ones last)
- Each question has a specific hypothesis it's testing

For each question, provide:
- The question text
- Answer options (if applicable)
- What hypothesis this tests
- What action I'll take based on each possible answer

Also provide:
- Where to distribute the survey ([SUGGEST CHANNELS])
- How many responses I need for statistically meaningful results
- Incentive recommendation (if needed)
```

### Prompt 133: Unit Economics Analysis
```
Calculate the unit economics for my [BUSINESS MODEL].

Inputs:
- Price: [WHAT I CHARGE]
- COGS per customer: [DIRECT COSTS — hosting, API calls, support time, etc.]
- CAC (Customer Acquisition Cost): [HOW MUCH IT COSTS TO GET ONE CUSTOMER — or "unknown, estimate for me"]
- Churn rate: [MONTHLY CHURN — or "unknown, use industry average for [INDUSTRY]"]
- Expansion revenue: [DO EXISTING CUSTOMERS BUY MORE OVER TIME?]

Calculate:
1. Gross margin per customer
2. LTV (Lifetime Value)
3. LTV:CAC ratio (healthy = 3:1 or higher)
4. Months to payback CAC
5. Break-even point (how many customers to cover fixed costs of [AMOUNT])

If LTV:CAC is below 3:1, suggest specific levers to improve it (reduce CAC, increase price, reduce churn, increase expansion revenue).
```

### Prompt 134: Keyword Research Brief
```
Perform keyword research for [NICHE/TOPIC].

I need keywords for:
1. Blog content (informational intent)
2. Landing pages (commercial/transactional intent)
3. Comparison pages ("[product] vs [product]" and "[product] alternatives")

For each keyword, estimate:
- Monthly search volume (low/medium/high if exact numbers unavailable)
- Competition level (low/medium/high)
- Content type that ranks (blog post, tool, directory, video)
- Suggested title for my content

Provide:
- 10 head terms (broad, high volume)
- 20 long-tail terms (specific, lower volume, easier to rank)
- 5 "zero-competition" terms (questions nobody's answering well)
- 5 trending terms (growing search volume)

My domain authority is [LOW/MEDIUM/HIGH or "new site"]. Prioritize keywords I can realistically rank for.
```

### Prompt 135: Market Report Summary
```
I'm going to paste a market report / research article / data dump. Summarize it for actionable use.

[PASTE THE CONTENT]

Extract:
1. The 5 most important data points (with exact numbers)
2. Trends that affect my business: [DESCRIBE YOUR BUSINESS]
3. Threats I should prepare for
4. Opportunities I should act on this month
5. Predictions for the next 6-12 months

Format as a one-page brief with bullet points. No filler. Every sentence should contain a fact, number, or actionable insight.

End with: "The one thing I should do based on this report is: _____"
```

## Competitor Analysis Prompts (136-145)

### Prompt 136: Competitor Website Teardown
```
Analyze [COMPETITOR URL] as if you're a conversion rate optimizer.

Evaluate:
1. Hero section: Is the value proposition clear in 5 seconds?
2. Social proof: What proof elements do they use? (testimonials, logos, numbers)
3. CTA strategy: How many CTAs? What do they say? Where are they placed?
4. Pricing page: How do they present pricing? What's the anchoring strategy?
5. Objection handling: Do they address common objections? (FAQ, guarantees, comparisons)
6. Trust signals: SSL, money-back guarantee, press logos, certifications

For each element, rate it (WEAK / AVERAGE / STRONG) and explain why.
Then: What can I steal (ethically) for my own landing page?
```

### Prompt 137: Competitor Content Audit
```
Analyze the content strategy of [COMPETITOR].

Look at:
1. Blog: What topics do they cover? How often do they publish? What's their top-performing post (highest social shares)?
2. Social media: Which platforms are they active on? What content types get the most engagement?
3. Email: Sign up for their newsletter. What's the welcome sequence like? How often do they email?
4. YouTube/Podcast: Do they have video/audio content? What topics get the most views?

Provide:
- Content gaps I can exploit (topics they're NOT covering)
- Content formats they're not using (that work well in this niche)
- Their estimated content budget/effort level
- The one piece of content I should create first to compete with them
```

### Prompt 138: Competitor Pricing Breakdown
```
Break down the pricing strategy of these competitors:

[LIST 3-5 COMPETITORS WITH THEIR PRICING PAGES]

For each:
1. Pricing model (per seat, per usage, flat rate, etc.)
2. Free tier limitations (what's free vs. what's not)
3. Price anchoring (how they make the mid-tier look attractive)
4. Enterprise pricing (custom/sales-led or self-serve?)
5. Discounts visible (annual vs. monthly difference, promo codes)
6. Hidden costs (add-ons, overage fees, required upgrades)

Analysis:
- Where's the pricing gap I can position in?
- What pricing model would disrupt this market?
- What's the price sensitivity of this customer segment?
```

### Prompt 139: Competitor Review Mining
```
Analyze reviews for [COMPETITOR] from these sources:
- G2 / Capterra / TrustPilot
- App Store / Play Store
- Reddit mentions
- Twitter mentions

For each source, extract:
1. Top 3 things users LOVE (these are table-stakes features I must have)
2. Top 3 things users HATE (these are my differentiation opportunities)
3. Feature requests that appear 3+ times (unmet demand)
4. Switching triggers (what makes people leave this competitor)
5. Exact quotes I can use in my marketing ("Unlike [competitor], we...")

Compile a "Competitor Weakness Report" — a list of their biggest vulnerabilities ranked by frequency of complaint.
```

### Prompt 140: Competitive Positioning Map
```
Create a competitive positioning map for [MY PRODUCT] vs. competitors.

Competitors:
1. [COMPETITOR 1]
2. [COMPETITOR 2]
3. [COMPETITOR 3]
4. [COMPETITOR 4]

Choose the two most important axes for my customers:
- Axis options: price (low/high), complexity (simple/powerful), audience (SMB/enterprise), speed (fast/slow), support (self-serve/high-touch), design (functional/beautiful)

Place each competitor on the 2x2 grid. Identify the empty quadrant — that's my positioning opportunity.

Then write:
1. My positioning statement: "For [AUDIENCE] who [NEED], [MY PRODUCT] is the [CATEGORY] that [DIFFERENTIATOR], unlike [COMPETITOR] which [LIMITATION]."
2. My tagline (under 8 words)
3. My 3 key differentiators (specific, not generic)
```

### Prompt 141: Competitor Ad Analysis
```
Analyze the advertising strategy of [COMPETITOR].

Research:
1. Facebook Ad Library: What ads are they running? What's the messaging? What landing pages do they use?
2. Google Ads: What keywords are they bidding on? (Use SpyFu free tier or SEMrush free trial)
3. Sponsorships: What podcasts, newsletters, or YouTube channels do they sponsor?

For each ad/channel:
- What's the hook? (first line or headline)
- What's the CTA?
- What audience are they targeting?
- Estimated spend level (low/medium/high)

Provide:
- Which of their ad strategies I should copy (and improve)
- Which I should avoid (and why)
- 3 ad angles they're NOT using that would work for my product
```

### Prompt 142: Technology Stack Analysis
```
Analyze the technology stack of [COMPETITOR WEBSITE URL].

Check using BuiltWith, Wappalyzer, or similar:
1. Frontend framework
2. Backend/hosting provider
3. Analytics tools
4. Marketing tools (email, CRM, chat)
5. Payment processor
6. CDN
7. Third-party integrations

Then assess:
- What does their tech stack tell me about their priorities?
- Where are they over-engineered? (using enterprise tools for a simple product)
- Where are they under-invested? (no analytics, basic email tool)
- What can I infer about their team size and budget?
- Technology gaps I can exploit (they're slow, they don't have mobile support, etc.)
```

### Prompt 143: Competitor Social Media Audit
```
Audit the social media presence of [COMPETITOR] across:
- Twitter: follower count, post frequency, engagement rate, content types
- LinkedIn: company page followers, post frequency, employee advocacy
- YouTube: subscriber count, average views, video topics
- TikTok: if present, what content style

For each platform:
1. What content gets the most engagement?
2. What content gets ignored?
3. How do they interact with comments/replies?
4. What's their posting schedule?
5. Do they use paid promotion on their organic posts?

Provide:
- Platform-by-platform comparison vs. my current presence
- Quick wins: things I can start doing tomorrow that they're not doing
- Content ideas inspired by their best-performing posts (differentiated, not copied)
```

### Prompt 144: Market Landscape Summary
```
Give me a comprehensive market landscape for [INDUSTRY/NICHE].

Include:
1. Major players (top 5 by market share or revenue)
2. Rising challengers (companies growing fast in the last 12 months)
3. Recent acquisitions or mergers
4. Funding rounds in the last year (who raised, how much, at what stage)
5. Regulatory changes or upcoming regulations
6. Technology shifts affecting the market
7. Customer behavior changes (how buying patterns are shifting)

Present this as a 2-page market brief with sections, bullet points, and a "So What?" interpretation after each section explaining what it means for a new entrant.
```

### Prompt 145: Competitor Onboarding Flow Analysis
```
Walk through [COMPETITOR]'s onboarding flow as a new user and analyze it.

Document every step:
1. Sign up page: What information do they ask for? Social login options?
2. Email verification: Required or optional?
3. Onboarding questionnaire: What questions do they ask? How do they use the answers?
4. First-run experience: What's the FIRST thing they get you to do?
5. Empty states: How do they handle screens with no data?
6. Activation moment: What's the "aha moment" they're driving toward?
7. Upgrade prompts: When and how do they first show pricing?

Rate each step (FRICTION: high/medium/low) and (VALUE: high/medium/low).

Then suggest: How should MY onboarding flow be different? What can I do in fewer steps?
```

## Alpha Extraction Prompts (146-160)

### Prompt 146: Arbitrage Opportunity Finder
```
Identify arbitrage opportunities in [MARKET/NICHE].

An arbitrage is: something you can buy/get cheaply in one place and sell/use at a higher value somewhere else.

Categories to explore:
1. Skills arbitrage: What skills are cheap to acquire but command high rates?
2. Geographic arbitrage: What's expensive in [MARKET A] but cheap in [MARKET B]?
3. Platform arbitrage: What content/products perform on [PLATFORM A] but nobody's doing on [PLATFORM B]?
4. Time arbitrage: What's becoming valuable that most people haven't noticed yet?
5. Information arbitrage: What do experts know that the general market doesn't?

For each opportunity:
- Effort to exploit (hours/dollars)
- Expected return
- Window of opportunity (how long before this closes)
- Risk level
```

### Prompt 147: Trend Monetization
```
[TREND] is growing fast right now.

Give me 10 specific ways to monetize this trend, ordered by speed-to-revenue:

For each:
1. What to sell (product, service, content, tool)
2. Who buys it (specific buyer persona)
3. How to reach them (channel)
4. Price point
5. Time to first dollar
6. Scalability (1-5)
7. Moat / defensibility (1-5)

Trend: [DESCRIBE THE TREND WITH SPECIFICS]
My skills: [WHAT I CAN DO]
My budget: [AMOUNT]
```

### Prompt 148: Revenue Reverse Engineering
```
[COMPANY/PERSON] appears to be making $[AMOUNT]/month.

Reverse engineer their revenue model:
1. What are all their revenue streams? (products, services, affiliates, ads, sponsorships)
2. Estimated revenue per stream (based on public data: pricing, audience size, engagement)
3. Cost structure (team size, tools, hosting, content production)
4. Estimated profit margin
5. Growth rate (are they growing or plateauing?)

Show your math. Use public data: social media followings, pricing pages, job postings, app store rankings, SimilarWeb estimates.

Then: Which of their revenue streams could I replicate with my resources?
```

### Prompt 149: Distribution Channel Analysis
```
What are the best distribution channels for [PRODUCT/SERVICE] targeting [AUDIENCE]?

Analyze these channels:
1. SEO / Organic search
2. Twitter / X
3. Reddit
4. LinkedIn
5. Product Hunt
6. YouTube
7. TikTok
8. Newsletters (sponsoring others')
9. Communities (Slack, Discord)
10. Partnerships / Affiliates
11. Cold outreach
12. Paid ads (Google, Meta, Reddit)

For each channel, provide:
- Relevance to my audience (LOW / MEDIUM / HIGH)
- Cost ($0 / $ / $$ / $$$)
- Time to results (DAYS / WEEKS / MONTHS)
- Effort required (LOW / MEDIUM / HIGH)
- Expected CAC range
- Example of someone in my niche who uses this channel well

Rank the top 5 channels I should focus on first, given a [BUDGET] budget and [TIMEFRAME] timeline.
```

### Prompt 150: Micro-SaaS Idea Generator
```
Generate 10 micro-SaaS ideas based on these constraints:

- Solo founder (just me)
- Budget: under $[AMOUNT] to build
- Must be profitable within 3 months
- Monthly revenue target: $[AMOUNT]
- My skills: [LIST YOUR SKILLS]
- Industries I know well: [LIST INDUSTRIES]

For each idea:
1. Product name + one-line description
2. Target customer (specific)
3. Problem it solves (specific)
4. How it makes money (pricing model + price point)
5. Tech stack to build it
6. Time to MVP (hours)
7. How to get first 10 customers
8. Existing competitors and why there's room for one more
9. Moat after 12 months (what makes it hard to copy)

Rank by: (potential revenue / effort to build) ratio. Highest first.
```

### Prompt 151: Underserved Audience Finder
```
Find underserved audiences in [BROAD MARKET].

An underserved audience is: a group with specific needs that current products/services don't fully address, AND who have money to spend.

For each audience found:
1. Who they are (demographics + psychographics)
2. What they need that doesn't exist (or exists poorly)
3. Where they hang out (online and offline)
4. How much they spend annually on related products
5. Why the market ignores them (too small? too niche? too hard to reach?)
6. Product/service idea tailored to them
7. Estimated market size (number of people x willingness to pay)

Find at least 5 underserved audiences. Rank by "ease of serving x willingness to pay."
```

### Prompt 152: Content Opportunity Gap
```
Find content gaps in [NICHE] — topics with high demand and low supply.

Method:
1. Search for [NICHE]-related questions on Quora, Reddit, and Google's "People Also Ask"
2. Find questions with many upvotes but bad answers
3. Find keywords where the top-ranking content is thin, outdated, or unhelpful
4. Find topics where forums have threads but no definitive blog post exists

For each gap:
- The question/topic
- Current best answer (and why it's insufficient)
- Estimated search volume (if applicable)
- Content format that would win (blog post, video, tool, template)
- Difficulty to create (1-5)
- Monetization angle (how to make money from this content)

Give me 10 gaps ranked by "search demand / difficulty to create."
```

### Prompt 153: Partnership Opportunity Map
```
Map potential partnership opportunities for [MY BUSINESS].

Categories:
1. Complementary products (they serve my customer with a non-competing product)
2. Distribution partners (they have access to my target audience)
3. Technology integrations (connecting my product to theirs adds value for both)
4. Content collaborations (co-created content that reaches both audiences)
5. Affiliate/referral (they earn by sending me customers, or vice versa)

For each opportunity:
- Company/person name
- What they do
- Why the partnership makes sense for THEM (not just me)
- Specific partnership format (integration, co-webinar, bundle, affiliate, etc.)
- How to approach them (warm intro path, cold email, Twitter DM)
- Expected outcome

Find at least 10 potential partners across the 5 categories.
```

### Prompt 154: Pricing Experiment Design
```
Design a pricing experiment for [PRODUCT].

Current pricing: [CURRENT PRICE AND MODEL]
Hypothesis: [WHAT I THINK WILL HAPPEN — e.g., "raising price from $9 to $19 won't significantly reduce conversion"]

Experiment design:
1. What to test (price, packaging, tier structure, trial length, etc.)
2. Control group vs. test group split
3. Sample size needed for statistical significance
4. Duration of test
5. Primary metric to measure (conversion rate, revenue per visitor, etc.)
6. Secondary metrics to watch
7. How to implement (A/B test tool recommendation, or manual split)
8. Decision criteria: "If [METRIC] is above [THRESHOLD], we go with the new pricing"

Also: What could go wrong with this experiment? How do I avoid false positives?
```

### Prompt 155: Revenue Diversification
```
I currently make money from [CURRENT REVENUE STREAM]. Help me diversify.

My business: [DESCRIPTION]
Current revenue: $[AMOUNT]/month
My audience: [SIZE AND DESCRIPTION]
My content/assets: [WHAT I'VE ALREADY BUILT]

Suggest 5 additional revenue streams I can add without:
- Requiring significant new skills
- Needing more than 10 hours/month to maintain
- Diluting my core business

For each:
1. What it is
2. How it generates revenue
3. Expected monthly revenue (conservative estimate)
4. Setup time (hours)
5. Ongoing time commitment
6. How it leverages what I already have (audience, content, expertise, code)
7. Risk if it cannibalizes my main revenue

Rank by revenue-to-effort ratio.
```

### Prompt 156: Emerging Technology Assessment
```
Assess [TECHNOLOGY] for business applications.

Current state:
1. What can it do TODAY (not in theory — actual, deployed use cases)?
2. What can't it do yet?
3. Who's using it in production? (name companies and products)
4. What does it cost? (APIs, hosting, licensing)

Business applications:
5. Top 5 business problems this technology solves
6. Which industries are adopting fastest?
7. Where is there the most money to be made?
8. What's the window of opportunity? (how long before this is commoditized?)

For a solopreneur with [MY SKILLS]:
9. What product could I build with this technology in the next 30 days?
10. What's the realistic revenue potential in the first 6 months?
11. What skills do I need to learn? (with specific learning resources)
```

### Prompt 157: Customer Interview Script
```
Write a customer interview script for [PURPOSE — e.g., "understanding how they choose a CRM", "validating a new feature idea"].

Interview length: 30 minutes
Interviewee: [CUSTOMER TYPE]

Script structure:
1. Warm-up (2 min): Build rapport, explain the purpose
2. Background (5 min): Understand their role and context
3. Problem exploration (10 min): Dig into their pain points
4. Solution exploration (8 min): How they solve the problem today
5. Reaction to concept (3 min): Show [MY IDEA] and get honest feedback
6. Wrap-up (2 min): Ask for referrals, thank them

For each section, provide:
- Exact questions to ask
- Follow-up probes for common responses
- What to listen for (signals vs. noise)
- Red flags (signs they're being polite instead of honest)

Rules: No leading questions. No "would you use this?" (everyone says yes). Focus on behavior, not opinions.
```

### Prompt 158: Supply/Demand Imbalance Finder
```
Find supply/demand imbalances I can exploit in [MARKET].

A supply/demand imbalance is: high demand + low supply = opportunity, or low demand + high supply = avoid.

Look for:
1. Services where demand outstrips supply (long wait times, high prices, poor quality)
2. Products where demand is growing faster than new competitors are entering
3. Content topics where search volume is rising but good content is scarce
4. Skills where job postings outnumber qualified candidates
5. Markets where technology has changed demand but supply hasn't adapted

For each imbalance:
- Evidence (data, trends, anecdotes)
- How to position myself to capture value
- Timeline before the gap closes
- Capital required
```

### Prompt 159: Audience Overlap Analysis
```
Find audiences adjacent to [MY CURRENT AUDIENCE] that I could expand into.

My current audience: [DESCRIPTION — who they are, what they care about]
My product: [WHAT I SELL]

For each adjacent audience:
1. Who they are
2. What they share with my current audience (overlap)
3. What's different (unique needs/pain points)
4. How I'd need to adapt my product/messaging
5. Where to find them
6. Estimated size vs. my current audience
7. Revenue potential

Find 5 adjacent audiences. Rank by: (overlap with current audience x willingness to pay x ease of reaching).
```

### Prompt 160: Alpha Signal Detection
```
I want to detect weak signals that predict [MARKET/NICHE] trends before they go mainstream.

Signal sources to monitor:
1. Patent filings (what are companies protecting?)
2. Job postings (what roles are companies suddenly hiring for?)
3. Academic papers (what research is about to commercialize?)
4. Regulatory filings (what's about to be approved/banned?)
5. Venture capital (what are VCs funding that hasn't hit the press?)
6. Developer activity (what open-source repos are suddenly popular?)
7. Community chatter (what are early adopters talking about?)

For each signal type:
- Where exactly to monitor it (specific URLs, tools, RSS feeds)
- How to filter noise from signal
- How far ahead this signal typically predicts the trend
- Example of a past trend this would have caught early

Give me a weekly monitoring checklist I can follow in 30 minutes.
```
