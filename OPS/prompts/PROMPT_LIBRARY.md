# PRINTMAXX master prompt library

20 reusable prompts for recurring tasks.
Paste into Claude, ChatGPT, or any LLM. Replace {variables} with your specifics.

Generated: 2026-02-06
Voice rules: .claude/rules/copy-style.md (PRINTMAXXER weighted aggregate)

---

## Content generation prompts (1-10)

---

### Prompt 1: Tweet thread generator

```
Write a Twitter/X thread about {topic} for the {niche} audience.

Thread structure:
- Tweet 1: consequence-first hook with a specific number. no em dashes. no "I'm going to share..." openers. jump straight into the result or observation.
- Tweets 2-6: one clear point per tweet. each must contain at least one specific number, tool name, or data point. no filler. no "here's the thing..." transitions.
- Tweet 7: wrap with a concrete action the reader can take today. no "follow for more" or "like and retweet." end with value.

Voice rules:
- lowercase throughout (except proper nouns and tool names)
- short punchy sentences. heavy period usage.
- no em dashes. no exclamation points. no emojis.
- banned words: leverage, utilize, delve, comprehensive, robust, innovative, seamless, game-changer, unlock, empower, cutting-edge, additionally, furthermore, moreover
- write like @pipelineabuser: aggressive, insider energy, specific tools and numbers
- trust reader intelligence. don't over-explain.

Example hook style:
"i monitor 200+ competitor pricing pages. they drop prices, i undercut before lunch."

Output format:
Tweet 1: [hook]
Tweet 2: [point]
...
Tweet 7: [action CTA]

Character limit: each tweet under 280 characters.
```

---

### Prompt 2: Newsletter issue generator

```
Write a newsletter issue about {topic} for {audience} on {platform} (Beehiiv/Substack).

Structure:
- Subject line: specific benefit, under 50 characters, lowercase
- Preview text: one sentence that creates urgency or curiosity, under 100 characters
- Opening paragraph (2-3 sentences): lead with the most interesting finding or result. no "in this issue" or "welcome back" openers.
- Section 1: the main insight (150-200 words). must include specific numbers. use a real example.
- Section 2: the method or framework (150-200 words). step-by-step. numbered list. each step is one sentence.
- Section 3: the quick win (50-100 words). one thing the reader can do in under 10 minutes after reading.
- Closing: one sentence. a forward-looking statement about next week's topic or a question to prompt replies.

Voice rules:
- PRINTMAXXER voice: direct, numbers-heavy, no fluff
- no em dashes, no banned AI vocabulary
- sentence case headings
- write like texting a smart friend who builds things
- one CTA maximum. place it after section 3.

Output: full newsletter ready to paste into {platform} editor.
Word count: 500-700 total.
```

---

### Prompt 3: Reddit post generator

```
Write a Reddit post for r/{subreddit} about {topic}.

Reddit-specific rules:
- Title: clear, specific, no clickbait. format: "{result} - here's how" or "I {did thing}. {timeframe}. here's what happened."
- Opening: establish credibility in 1-2 sentences. "I've been doing X for Y months. here are the numbers."
- Body: 300-500 words. mix of narrative and data. break into short paragraphs (2-3 sentences max).
- Include at least 3 specific numbers (revenue, time, percentages, costs).
- End with a question to drive comments. not a CTA. Reddit hates self-promotion.
- Tone: helpful, honest, slightly self-deprecating. admit what didn't work alongside what did.
- Never link to your own products in the post. if someone asks in comments, that's different.

Voice:
- casual but knowledgeable
- "here's what actually happened" energy
- no marketing speak. Reddit downvotes that instantly.
- use "lol" or "tbh" naturally (1-2 times max)

Subreddit context: r/{subreddit} values {what_the_sub_values}. avoid {what_gets_downvoted}.

Output: Title + full post body. ready to paste.
```

---

### Prompt 4: LinkedIn post generator

```
Write a LinkedIn post about {topic} for {audience} (targeting {industry} professionals).

Structure:
- Hook line (first line visible before "see more"): strong claim or result. must make someone stop scrolling. under 15 words.
- Body (8-12 short lines, heavy line breaks): one idea per line. use line breaks between every 1-2 sentences. LinkedIn rewards line breaks for readability.
- Include 1 personal story or specific example with real numbers.
- Close with a question that invites comments (LinkedIn algorithm rewards comment velocity in first 60 minutes).

Voice rules:
- professional but human. not corporate, not casual-bro.
- no emojis. no hashtags in the body (add 3-5 hashtags as a final line only).
- no "I'm excited to announce" or "I'm humbled" or "thrilled"
- no em dashes. no AI vocabulary.
- first person. specific. honest.

Example hook:
"I sent 10,000 cold emails last year. 14 deals closed. $73K in revenue. Here's the breakdown."

Output: full LinkedIn post. 150-250 words.
Hashtag line: #hashtag1 #hashtag2 #hashtag3
```

---

### Prompt 5: YouTube script generator

```
Write a YouTube video script about {topic} for a {niche} channel targeting {audience}.

Video length: {duration} minutes.

Script structure:
- Hook (0:00-0:30): open with the most interesting result, claim, or question. "I tested X for 30 days. here's what happened." no channel intros. no "hey guys." jump straight in.
- Context (0:30-1:30): why this matters. one specific problem the viewer has. establish stakes.
- Main content ({num_points} sections, each 1-2 minutes):
  - Section title (spoken as a transition, not a visual card)
  - Key point with specific example
  - Data or proof (number, screenshot reference, case study)
  - Quick takeaway in one sentence
- CTA (last 30 seconds): what the viewer should do next. subscribe mention is fine but brief. main CTA = action they take outside YouTube.

Voice:
- conversational. like explaining to a friend over coffee.
- no "without further ado" or "let's dive in"
- use specific tool names, not generic terms
- include timestamps in brackets: [0:00], [0:30], etc.

Retention notes (include as [EDITOR: ...] tags):
- [EDITOR: b-roll of {visual}]
- [EDITOR: text overlay: "{stat}"]
- [EDITOR: cut to screen recording here]

Output: full script with timestamps and editor notes.
Word count: approximately {duration} x 150 words.
```

---

### Prompt 6: Medium article generator

```
Write a Medium article about {topic} for the {audience} audience.

Target length: 1,200-1,800 words (7-10 minute read, Medium's sweet spot for Partner Program earnings).

Structure:
- Title: specific, under 70 characters, no clickbait. format: "How I {result} in {timeframe}" or "{Number} {things} I learned from {experience}"
- Subtitle: one sentence that adds context the title doesn't cover.
- Opening paragraph: jump straight to the insight. no "In today's world" or "Have you ever wondered." state the conclusion first, then unpack it.
- 3-5 sections with sentence case subheadings
- Each section: 200-400 words. must contain at least one specific number or example.
- Closing: 2-3 sentences. end with an action or a question. no "In conclusion" or summary paragraph.

Medium-specific optimizations:
- use subheadings every 300 words (reader retention)
- bold key phrases sparingly (1-2 per section)
- no bullet point lists longer than 5 items
- include 1-2 pull quotes using Medium's quote formatting (> )
- no external links in first 200 words (Medium penalizes early outbound links)

Voice: PRINTMAXXER weighted aggregate. direct, specific, honest about tradeoffs.

Tags (5): {tag1}, {tag2}, {tag3}, {tag4}, {tag5}

Output: full article ready to paste into Medium editor.
```

---

### Prompt 7: Email sequence generator

```
Write a {num_emails}-email sequence for {purpose} targeting {audience}.

Sequence timing: {schedule} (e.g., Day 0, Day 1, Day 3, Day 5, Day 7)

For each email provide:
- Subject line (under 50 characters, lowercase, specific benefit)
- Preview text (under 100 characters)
- Body (150-250 words)
- CTA button text (under 5 words, action verb + what they get)

Sequence arc:
- Email 1: deliver value immediately. no lengthy welcomes.
- Email 2: personal story or "how I use this" angle.
- Middle emails: education, case studies, common mistakes.
- Final email: paid offer CTA. not pushy. present the offer and let the value from previous emails do the selling.

Voice rules:
- lowercase casual. like texting a smart friend.
- no em dashes. no banned AI vocabulary.
- start each email with the most interesting line.
- no "I hope this finds you well" or "just checking in"
- one CTA per email. not two. not three. one.
- PS lines only on the final email (secondary offer or social proof).

Product being sold: {product_name} at {price}.
Lead magnet that triggered this sequence: {lead_magnet}.

Output: complete sequence, each email separated by --- dividers.
```

---

### Prompt 8: Product description generator

```
Write a product description for {product_name} sold on {platform} (Gumroad/Whop/Etsy/Shopify) at {price}.

Target buyer: {audience} who wants to {desired_outcome}.

Structure:
- Headline: the outcome, not the product. "{Desired outcome} in {timeframe}" format.
- Subhead: who it's for + what they get. one sentence.
- What's inside (bullet list, 5-8 items): each bullet = specific deliverable + outcome. not just "PDF guide" but "47-page PDF with 12 email templates that average 14% reply rates."
- Social proof section: {num_reviews} reviews or {num_sales} sales. include 2-3 short testimonial quotes if available.
- FAQ section (3-4 questions): answer the objections. "Is this for beginners?" "How fast will I see results?" "What if it doesn't work?"
- CTA: action verb + what they get + price. "Get the templates - $29"

Voice:
- direct. specific. no hype.
- every claim backed by a number
- no "this will change your life" or "you'll never look back"
- honest about what it is and isn't

Pricing psychology: anchor against the alternative cost. "A freelancer charges $500 for this. You get the same templates for $29."

Output: full product page copy. 300-500 words.
```

---

### Prompt 9: Landing page copy generator

```
Write landing page copy for {product_or_service} targeting {audience}.

Page structure (scroll order):
1. Hero section:
   - Headline: main promise in under 10 words
   - Subheadline: who it's for + what they get (one sentence)
   - CTA button: action verb + outcome (e.g., "Get my templates")
   - Social proof line: "{X} people already using this" or "{X} five-star reviews"

2. Problem section (3-4 sentences):
   - name the specific pain point
   - quantify it ("you're spending 5 hours/week on X")
   - make them feel seen, not attacked

3. Solution section (what they get):
   - 4-6 bullet points, each with a specific deliverable and outcome
   - no vague benefits. "saves time" becomes "saves 4.5 hours per week"

4. Social proof section:
   - 3 testimonial blocks: name, role, specific result
   - if no real testimonials, skip this section entirely. never fabricate.

5. Pricing section:
   - price anchoring: compare to alternative cost
   - what's included (brief recap)
   - guarantee if applicable
   - CTA button (repeat from hero)

6. FAQ (4-5 questions):
   - address top objections
   - keep answers to 2-3 sentences each

Voice: PRINTMAXXER. direct, specific, no promotional adjectives. every sentence earns its place.

No banned words. No em dashes. Sentence case headings.

Output: full page copy organized by section. 600-900 words total.
```

---

### Prompt 10: Ad copy generator

```
Write {num_variants} ad copy variants for {product_or_service} on {platform} (Meta/TikTok/Google/X).

Target audience: {audience}
Objective: {objective} (traffic/conversions/leads)
Price point: {price}

For each variant provide:
- Primary text (the main copy above the creative): 2-4 sentences max. hook + value prop + CTA.
- Headline (bold text below creative): under 40 characters. specific outcome.
- Description (optional text below headline): under 90 characters.
- CTA button text: platform-appropriate (Learn More / Sign Up / Get Offer / Shop Now)

Platform-specific rules:
- Meta: primary text 125 characters visible before "See More." front-load the hook.
- TikTok: native voice. feels like a creator, not a brand.
- Google: keyword in headline. address search intent directly.
- X: conversational. no corporate speak. blends into the timeline.

Variant strategy:
- Variant A: pain point hook ("tired of X?")
- Variant B: result hook ("I {achieved result} in {timeframe}")
- Variant C: social proof hook ("{X} people already use this")
- Variant D: curiosity hook ("the {industry} trick nobody talks about")

Voice: match the platform's native tone while maintaining PRINTMAXXER energy. specific numbers in every variant.

Output: {num_variants} complete variants, labeled A through {letter}. ready to paste into ad manager.
```

---
---

## Research prompts (11-15)

---

### Prompt 11: Alpha extraction prompt

```
Analyze the following content from {source} and extract actionable alpha for a bootstrapped solopreneur.

Content to analyze:
"""
{paste content here}
"""

For each piece of alpha found, provide:

1. alpha_id: ALPHA{number}
2. source: {source handle or URL}
3. tactic: one-sentence description of what to do
4. category: APP_FACTORY | CONTENT_FORMAT | OUTBOUND | GROWTH_HACK | TOOL_ALPHA | MONETIZATION | SEO_GEO_ASO
5. specific_numbers: any revenue, conversion, or performance data mentioned
6. replication_steps: 3-5 concrete steps to replicate this
7. estimated_roi: how much this could make relative to time/money invested
8. confidence: HIGH (verified numbers + proof) | MEDIUM (reasonable claim + social proof) | LOW (unverified claim)
9. engagement_authenticity: check like/reply ratio. flag if suspicious.
10. earnings_verified: TRUE (screenshot/proof) | FALSE (text claim only)

Bot detection check: before trusting engagement metrics, verify:
- like-to-comment ratio is reasonable (not 10K likes with 3 comments)
- comments contain specific questions, not just "amazing!" or single emojis
- account age matches follower count
- flag as SUSPICIOUS if metrics seem inflated

If no actionable alpha exists in the content, say "NO_ALPHA_FOUND" and explain why in one sentence.

Output format: structured data, one alpha entry per block, separated by ---.
```

---

### Prompt 12: Competitor analysis prompt

```
Analyze {competitor_name} ({competitor_url}) as a competitor in the {niche} space.

Research and provide:

**1. Revenue estimation**
- estimated monthly revenue (use SimilarWeb traffic x industry conversion rates x average price)
- revenue model: subscription, one-time, freemium, ad-supported, affiliate
- pricing tiers and what each includes

**2. Traffic and distribution**
- estimated monthly visitors
- top 3 traffic sources (organic, paid, social, direct, referral)
- primary social platforms and follower counts
- content publishing frequency

**3. Product analysis**
- core product offering (what exactly do they sell)
- unique positioning (what's different about their approach)
- tech stack (check Wappalyzer or BuiltWith data)
- strengths: 3 things they do well
- weaknesses: 3 gaps or problems

**4. Growth tactics**
- how are they acquiring customers (specific channels and methods)
- content strategy: what content types, what frequency, what topics
- paid advertising: are they running ads, what platforms, what messaging
- partnerships or affiliations visible

**5. Actionable takeaways**
- 3 things to copy (with PRINTMAXX twist)
- 3 things to avoid
- 1 gap we can exploit that they're not serving

Be specific. use numbers wherever possible. no vague statements like "they have a strong brand." instead: "they have 45K Twitter followers with 3.2% average engagement rate."

Output: structured analysis. 500-800 words.
```

---

### Prompt 13: Market research prompt

```
Research the {niche/market} market for a bootstrapped solopreneur entering with {budget} budget.

Provide:

**1. Market size and growth**
- TAM (total addressable market) with source
- growth rate (CAGR) with source
- is this market growing, stable, or shrinking

**2. Customer analysis**
- who buys in this market: demographics, psychographics, income level
- where they hang out online: specific subreddits, Twitter accounts, Facebook groups, forums
- what they currently pay: price ranges for existing products
- top 3 pain points (validated by real customer complaints, not assumed)

**3. Competitive landscape**
- top 5 competitors by revenue (estimated)
- average pricing across the market
- barriers to entry: HIGH (heavy capital/regulation), MEDIUM (some expertise needed), LOW (anyone can start)
- is the market saturated, competitive, or underserved

**4. Opportunity analysis**
- underserved segments: who is NOT being served well by existing players
- pricing gaps: where is there room between free and premium
- distribution gaps: what channels are competitors NOT using
- product gaps: what do customers want that doesn't exist yet

**5. PRINTMAXX entry strategy**
- recommended entry point: what to sell, to whom, at what price
- estimated time-to-first-revenue: days/weeks
- estimated monthly revenue at 6 months (base, bull, bear case)
- recommended methods from our stack that apply (reference MM codes if known)

Stress test your own analysis: where could you be wrong? what assumptions are you making?

Output: structured research report. 600-1,000 words. every claim backed by data or clearly marked as [ESTIMATE].
```

---

### Prompt 14: Trend detection prompt

```
Analyze the following signals and determine if {topic/trend} is a real trend or noise.

Signals to analyze:
- Google Trends data for "{search_terms}" over past {timeframe}
- Social media mentions: {any data you have}
- Revenue data: {any data you have}
- News coverage: {any data you have}

Assessment framework:

**1. Signal strength (score 1-10)**
- search volume trajectory (flat, linear growth, exponential)
- social mention velocity (is it accelerating)
- revenue signals (are people making money from this now)
- duration (has this persisted more than 30 days)

**2. Trend classification**
- BREAKOUT: new trend with exponential growth, < 6 months old. high reward, high risk of fading.
- ESTABLISHED: growing steadily for 6-24 months. lower risk, moderate reward.
- SATURATED: peaked, now stable or declining. hard to enter, easy to compete on price.
- DEAD: declining for 3+ months. avoid.
- CYCLICAL: seasonal or recurring. time entry to next cycle.

**3. Arbitrage window**
- how long until this trend is saturated (estimated weeks/months)
- current competition level: how many people are already doing this
- entry difficulty: what's needed to start (time, money, skills)

**4. PRINTMAXX action recommendation**
- ENTER NOW: strong signal, low competition, time-sensitive
- MONITOR: interesting but too early or unclear signal
- SKIP: weak signal, high competition, or poor fit for our stack
- specific method to use if entering (content, app, product, service)

Output: structured assessment. be honest about uncertainty. mark assumptions clearly.
```

---

### Prompt 15: Funnel reverse-engineering prompt

```
Reverse-engineer the funnel for {creator/company} ({url or social handle}).

Map every step of their customer journey from first touch to purchase:

**1. Discovery layer (how do people find them)**
- top 3 platforms where they publish content
- content types and frequency per platform
- follower/subscriber counts per platform
- estimated monthly reach
- paid advertising: are they running ads, on what platforms

**2. Capture layer (how do they get contact info)**
- lead magnets: what free thing do they offer
- opt-in mechanism: landing page, pop-up, bio link, DM
- estimated conversion rate from visitor to lead (industry average if unknown)

**3. Nurture layer (how do they build trust)**
- email sequence: how many emails, what timing, what content
- free content strategy: what value do they give away vs gate
- community: do they have a free community (Discord, Telegram, Facebook Group)

**4. Conversion layer (how do they sell)**
- product lineup: every product, its price, its format
- sales mechanism: webinar, email, DM, sales page, self-serve checkout
- pricing strategy: tripwire, flagship, premium tiers
- urgency/scarcity tactics used

**5. Retention and upsell layer (how do they maximize LTV)**
- subscription vs one-time
- upsell path: what do they sell after the first purchase
- referral mechanism: do they incentivize sharing
- repeat purchase frequency

**6. Estimated economics**
- estimated monthly revenue (back-calculate from visible metrics)
- estimated customer acquisition cost
- estimated lifetime value per customer
- estimated monthly profit margin

**7. What to steal (PRINTMAXX applications)**
- 3 specific tactics to adapt for our funnel
- 1 structural element to copy
- 1 thing they're doing wrong that we can fix

Output: structured funnel map. every estimate labeled [ESTIMATE]. 600-900 words.
```

---
---

## Operations prompts (16-20)

---

### Prompt 16: VA task delegation prompt

```
Create a task brief for a virtual assistant to complete {task}.

This brief must be clear enough that someone with no context about our business can execute it perfectly on the first attempt.

Structure:

**task name:** {clear, specific task name}
**deadline:** {date and timezone}
**estimated time:** {hours}
**tools needed:** {specific tool names with links}

**context (3 sentences max):**
Why this task matters. what it connects to. what happens after it's done.

**step-by-step instructions:**
1. {action verb} + {specific thing} + {where to find it}
2. {action verb} + {specific thing} + {expected result}
3. ...continue until task is complete

Each step must:
- start with an action verb (open, click, copy, paste, search, download, upload, type, select)
- specify the exact location (URL, file path, button name, menu item)
- describe the expected result so the VA can verify they did it right

**quality checks (how to know it's done right):**
- {specific check 1}
- {specific check 2}
- {specific check 3}

**common mistakes to avoid:**
- {mistake 1 and how to prevent it}
- {mistake 2 and how to prevent it}

**output deliverable:**
- {what they should send back to you}
- {format: file, link, screenshot, spreadsheet}
- {where to put it: Google Drive folder, email, Slack channel}

**if stuck:**
- try {fallback approach}
- if still stuck, message me with: what step you're on, what you tried, what error you got

Output: complete VA brief. no jargon. written for someone who speaks English as a second language.
```

---

### Prompt 17: Content calendar planning prompt

```
Create a {num_days}-day content calendar for {brand/account} on {platforms}.

Niche: {niche}
Target audience: {audience}
Content pillars (3-5 themes to rotate): {pillar1}, {pillar2}, {pillar3}, etc.
Posting frequency: {frequency per platform per day}

For each day, provide:

| Day | Platform | Content type | Topic/hook | Pillar | Best post time |
|-----|----------|-------------|------------|--------|---------------|

Content type rotation:
- Stat/data posts (2x per week per platform): specific number + insight
- Story posts (2x per week): personal experience or case study
- How-to posts (1x per week): step-by-step method
- Engagement posts (1x per week): question, poll, or hot take
- Repurposed posts (1x per week): reformat top performer from another platform

Rules:
- no back-to-back same content type
- each pillar appears at least once per week
- high-engagement days (Tue-Thu) get the strongest hooks
- weekend posts can be lighter/personal

Post time optimization by platform:
- X/Twitter: 8-9am, 12-1pm, 5-6pm EST
- LinkedIn: 7-8am, 12pm, 5-6pm EST (Tue-Thu best)
- Instagram: 11am-1pm, 7-9pm EST
- TikTok: 7-9am, 12-3pm, 7-11pm EST

Output: complete calendar as a markdown table. include a "hook idea" column with the first line of each post.
```

---

### Prompt 18: Performance review prompt

```
Analyze the performance of {method/channel/campaign} over the past {timeframe}.

Data to analyze:
"""
{paste metrics here: revenue, traffic, conversion rates, engagement, costs, etc.}
"""

Provide:

**1. Performance summary (3 sentences)**
- headline metric: what's the single most important number
- trend: improving, stable, or declining
- vs benchmark: above or below industry average

**2. What's working (top 3)**
For each:
- the specific thing that performed well
- the number proving it
- why it's working (hypothesis)
- recommendation: scale, maintain, or test further

**3. What's not working (top 3)**
For each:
- the specific thing that underperformed
- the number proving it
- likely root cause
- recommendation: fix, pause, or kill

**4. Efficiency metrics**
- revenue per hour invested
- cost per acquisition (if applicable)
- return on ad spend (if applicable)
- conversion rate at each funnel stage

**5. Recommendations for next {timeframe}**
- 3 specific actions ranked by expected impact
- 1 experiment to run (A/B test, new channel, new format)
- 1 thing to stop doing immediately

**6. Risk flags**
- anything concerning in the data
- dependencies or single points of failure
- external factors that could change results

Be honest. don't spin bad numbers. if something isn't working, say so clearly.

Output: structured performance review. 400-600 words.
```

---

### Prompt 19: A/B test design prompt

```
Design an A/B test for {what_to_test} on {platform/channel}.

Context:
- current metric: {current_performance} (e.g., "2.1% conversion rate")
- goal: {target_improvement} (e.g., "increase to 3%+")
- traffic/volume available: {estimated_sample_size_per_week}

Provide:

**1. Hypothesis**
"If we change {specific element} from {current} to {proposed}, then {metric} will {increase/decrease} by {amount} because {reasoning}."

**2. Test design**
- Control (A): {exactly what it looks like now}
- Variant (B): {exactly what the change is}
- Optional Variant (C): {if testing 3 versions}
- traffic split: {50/50 or other ratio, with reasoning}
- minimum sample size needed for statistical significance (use 95% confidence, 80% power)
- estimated test duration based on current traffic

**3. Primary metric**
- what you're measuring: {specific metric}
- how you're measuring it: {tool or method}
- what counts as a "win": {minimum improvement to declare winner}

**4. Secondary metrics (track but don't optimize for)**
- {metric 2}
- {metric 3}

**5. Guardrail metrics (stop test if these tank)**
- {metric that should NOT decrease significantly}
- stop threshold: {what decline triggers test pause}

**6. Implementation checklist**
- [ ] {step 1: set up tracking}
- [ ] {step 2: create variant}
- [ ] {step 3: configure split}
- [ ] {step 4: QA both versions}
- [ ] {step 5: launch}
- [ ] {step 6: check results at midpoint}
- [ ] {step 7: call winner at {date}}

**7. What to do with results**
- If A wins: {keep current, investigate why B failed}
- If B wins: {implement, then test next element}
- If no significant difference: {increase sample size or test bigger change}

Output: complete test plan. ready to hand to a developer or marketing manager.
```

---

### Prompt 20: Customer persona builder prompt

```
Build a detailed customer persona for {product_or_service} in the {niche} market.

Use this information: {any customer data, reviews, survey responses, or audience insights you have}

Provide:

**1. Demographics**
- Name (fictional, representative): {name}
- Age range: {range}
- Gender: {if relevant to product}
- Location: {country, region, urban/suburban/rural}
- Income range: {annual}
- Occupation: {job title and industry}
- Education: {level}
- Family status: {single, married, kids, etc.}

**2. Psychographics**
- Values: top 3 things they care about (ranked)
- Identity: how they see themselves ("I'm a {self-description}")
- Aspirations: where they want to be in 12 months
- Fears: what keeps them up at night (related to our market)
- Frustrations: top 3 daily annoyances we can solve

**3. Behavior patterns**
- Daily routine: what does a typical day look like
- Media consumption: what platforms, what time, what content types
- Purchase behavior: impulse vs research-heavy, price sensitive vs value-driven
- Decision influencers: who do they trust (specific creators, publications, peers)
- Objections: top 3 reasons they'd say no to our product

**4. Where to find them**
- Top 3 subreddits they visit
- Top 5 Twitter/X accounts they follow
- Facebook groups or online communities
- Podcasts they listen to
- YouTube channels they watch
- Offline places they go

**5. Messaging that resonates**
- Hook that would stop them scrolling: "{specific hook}"
- Pain point to lead with: "{specific pain}"
- Transformation to promise: "From {current state} to {desired state}"
- Social proof that matters to them: {type of proof they trust most}
- Objection-handling line: "{address their #1 concern}"

**6. One paragraph that IS this person**
Write a first-person paragraph in their voice describing their current situation and what they wish existed.

Output: complete persona document. specific enough to write ads, emails, and content directly from it.
```

---
---

## Quick reference: which prompt to use

| Task | Prompt # | When to use |
|------|----------|-------------|
| Tweet thread | 1 | Twitter content batching |
| Newsletter | 2 | Weekly Beehiiv/Substack issue |
| Reddit post | 3 | Community distribution |
| LinkedIn post | 4 | B2B audience building |
| YouTube script | 5 | Video content production |
| Medium article | 6 | SEO + Partner Program revenue |
| Email sequence | 7 | Lead nurture, onboarding, sales |
| Product description | 8 | Gumroad/Whop/Etsy listings |
| Landing page | 9 | Product/service sales pages |
| Ad copy | 10 | Paid acquisition campaigns |
| Alpha extraction | 11 | Processing bookmarks, tweets, posts |
| Competitor analysis | 12 | Before entering a market |
| Market research | 13 | Evaluating new niches |
| Trend detection | 14 | Spotting opportunities |
| Funnel reverse-engineering | 15 | Studying successful creators |
| VA delegation | 16 | Outsourcing tasks |
| Content calendar | 17 | Planning content batches |
| Performance review | 18 | Weekly/monthly reviews |
| A/B test design | 19 | Optimizing conversion |
| Customer persona | 20 | Before creating any product or campaign |
