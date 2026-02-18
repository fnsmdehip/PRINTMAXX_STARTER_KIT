# Lead gen research methods guide

Source: high-signal Twitter intel extraction. all methods are legal. some have compliance requirements noted.

Status: ALL methods PENDING_REVIEW for human validation before implementation.

---

## The stack at a glance

| Category | Methods | Cost | Time to first lead |
|----------|---------|------|--------------------|
| Reddit intel | f5bot + freesubstats | $0 | Same day |
| LinkedIn intel | People tab scraping | $0 | Same day |
| SEC filings | 10-K Risk Factors | $0 | 1-2 hours |
| Government intel | FOIA + USAspending | $0 | Same day (USAspending) / 20-60 days (FOIA) |
| Parallel dialers | Orum / Nooks / Koncert / PhoneBurner | $149-500/mo | Same day |
| Voicemail drops | Drop.co / VoiceDrop.ai | $0.05-0.25/drop | Same day |
| TCPA compliance | Co-reg / Sweepstakes / SMS keyword / Quiz | $0-200/mo | 1-7 days |

---

## Category 1: Reddit intelligence ($0)

### f5bot.com - Reddit keyword alerts

**What it does:** emails you every time your keyword gets mentioned on Reddit. set it and forget it. free.

**Why it matters:** people on Reddit literally type "looking for a tool that does X" and "is there an alternative to Y" every day. f5bot catches these in real time.

**Setup (10 minutes):**
1. Go to f5bot.com and create account
2. Add keywords in these categories:
   - **Competitor names:** every competitor brand name you can think of
   - **Pain point phrases:** "need a tool for" / "looking for alternative" / "frustrated with" / "anyone know a good"
   - **Product category terms:** your product type (e.g. "cold email tool" / "prayer app" / "fitness tracker")
   - **Your own brand:** monitor mentions of your product
3. Check email daily. respond to threads where you can genuinely help.
4. Do NOT spam. provide real value. mention your product naturally if relevant.

**Pro tips:**
- Set up separate email filter for f5bot alerts
- Respond within 2 hours for maximum visibility (Reddit rewards fast replies)
- Write helpful answers first, mention your product second
- Track which keywords generate the most leads

**Applies to:** MM007_COLD_OUTBOUND, MM006_CONTENT_FARM, MM001_APP_FACTORY, MM002_INFO_PRODUCTS

---

### freesubstats.com - Subreddit growth tracking

**What it does:** shows subscriber growth rates for any subreddit. tracks daily/weekly/monthly growth.

**Why it matters:** a subreddit growing 500+ members/day = emerging demand in that niche. get in before saturation.

**Setup (10 minutes):**
1. Go to freesubstats.com
2. Search subreddits in your target niches
3. Track these metrics:
   - **Growth rate** (subscribers/day) - >100/day = growing fast
   - **Activity rate** (posts/day) - high activity = engaged community
   - **Growth trajectory** - accelerating = opportunity window
4. Compare competitor subreddits (larger = more saturated)
5. Build content/product strategy around fastest-growing subs

**Pro tips:**
- Growth rate matters more than absolute size
- Cross-reference with f5bot keywords in that subreddit
- Emerging subreddits have less competition for visibility
- Track weekly to spot trend changes early

**Applies to:** MM006_CONTENT_FARM, MM001_APP_FACTORY, MM002_INFO_PRODUCTS, niche discovery

---

## Category 2: LinkedIn intelligence ($0)

### LinkedIn People tab competitor scraping

**What it does:** finds people who currently work at (or work with) your competitors. these are proven buyers.

**Why it matters:** someone who already uses a competitor product has budget allocated, understands the problem, and is reachable. highest quality leads possible.

**Setup (30 minutes):**
1. Go to LinkedIn > People tab
2. Use these filters:
   - **Current company:** add competitor company name
   - **Title:** add relevant decision-maker titles (VP Marketing, Head of Growth, CTO, etc.)
   - **Location:** filter to your target geography
   - **Industry:** narrow further if needed
3. These results are people who CURRENTLY USE your competitor
4. Send personalized connection request referencing something specific about them
5. Once connected, send value-first message (not a pitch)
6. After 1-2 value touches, pitch your alternative

**The message framework:**
```
Connection request:
"Hey [Name], noticed you're using [Competitor] for [function].
We're building something that solves [specific limitation of competitor].
Would love to connect."

Follow-up (after accepted):
"Quick question - what's the biggest pain point you've hit with [Competitor]?
We've been hearing [specific complaint] from a lot of teams."

Pitch (after they respond):
"We actually built [product] specifically to fix that.
[One specific differentiation]. Happy to show you a 5-min demo?"
```

**Compliance notes:**
- LinkedIn limits: 100 connection requests/week (safe limit)
- Do not use automation tools on LinkedIn without careful rate limiting
- See `OPS/growth/PLATFORM_AUTOMATION_LIMITS_2026.md` for current safe limits
- Manual first. automate carefully later.

**Applies to:** MM007_COLD_OUTBOUND, MM004_AGENCY_SERVICES, MM062_FRACTIONAL_EXEC_SERVICE

---

## Category 3: SEC filings intelligence ($0)

### 10-K Risk Factors - Enterprise pain point extraction

**What it does:** SEC 10-K annual filings have a "Risk Factors" section where companies LEGALLY MUST disclose their biggest risks and problems. these are their actual pain points that they would pay to solve.

**Why it matters:** the company literally tells you their problems in a legal document. then you email them the solution. nobody does this. it's borderline illegal how good the intel is.

**Setup (1-2 hours for first batch):**

1. Go to SEC EDGAR: https://www.sec.gov/cgi-bin/browse-edgar
2. Search for target company name
3. Find their most recent 10-K filing (annual report)
4. Ctrl+F for "Risk Factors" section
5. Read every risk they disclose. common categories:
   - **Cybersecurity risks** = sell security services
   - **Talent retention risks** = sell HR/recruiting solutions
   - **Supply chain risks** = sell logistics/procurement tools
   - **Technology risks** = sell modernization/AI services
   - **Regulatory risks** = sell compliance solutions
   - **Competition risks** = sell differentiation/marketing services

6. Map each risk to your products/services
7. Cold email the relevant executive referencing their specific risk

**The email framework:**
```
Subject: re: [Company] cybersecurity risk factor

[Name],

I was reviewing [Company]'s latest 10-K and noticed you disclosed
[specific risk factor - quote or paraphrase from filing].

We've helped [similar company] reduce [that specific risk] by [specific result].

Worth a 15-minute conversation?

[Your name]
```

**Why this converts:**
- You're referencing something THEY wrote
- It shows you did real research (not a spray-and-pray email)
- The risk is real because their lawyers made them disclose it
- The executive responsible for that risk is incentivized to fix it
- Nobody else is doing this

**Compliance:** None needed. SEC filings are public documents. You're literally reading publicly available information.

**Applies to:** MM007_COLD_OUTBOUND, MM004_AGENCY_SERVICES, MM051_AI_AUTOMATION_AGENCY

---

## Category 4: Government contract intelligence ($0)

### USAspending.gov - Federal spending database

**What it does:** searchable database of ALL federal government spending. every contract, every vendor, every dollar amount. maintained by US Treasury.

**Why it matters:** government is the biggest customer in the world. this database tells you exactly who they buy from, how much they pay, and when contracts expire.

**Setup (1 hour):**
1. Go to https://usaspending.gov
2. Click "Award Search" or "Spending Explorer"
3. Search by:
   - **Keyword:** your industry/product category
   - **Agency:** specific government agencies
   - **NAICS code:** industry classification codes
   - **Date range:** focus on recent contracts
4. Export data to CSV
5. Analyze:
   - Which agencies spend the most in your category?
   - Who are the current vendors (your competitors)?
   - What are the contract values?
   - When do contracts expire? (rebid opportunity)
6. Build target list of:
   - Agencies with budget in your category
   - Contracting officers to contact
   - Expiring contracts to bid on

**Pro tips:**
- Filter by "Small Business" set-asides if you qualify
- Contract end dates are your best timing signal
- Current vendor + contract value = your pricing benchmark
- Start with agencies that have multiple small contracts (easier entry)

### FOIA requests - Deep contract intelligence

**What it does:** Freedom of Information Act gives you the legal right to request government documents including vendor contracts, pricing, and performance evaluations.

**Why it matters:** you can literally request the exact terms of your competitor's government contract. their pricing, their deliverables, their performance reviews.

**Setup (2-4 hours):**
1. Identify the specific information you want:
   - Vendor contracts in your category
   - Pricing schedules
   - Performance evaluation reports
   - Vendor lists for specific procurement categories
2. Find the agency's FOIA office: https://www.foia.gov
3. Submit FOIA request with:
   - Specific description of records requested
   - Date range
   - Your contact information
   - Fee waiver request (if applicable)
4. Wait 20-60 business days for response
5. When you get the documents:
   - Extract competitor pricing
   - Note contract terms and deliverables
   - Identify expiring contracts
   - Prepare your bid/pitch

**FOIA request template:**
```
Dear FOIA Officer,

Pursuant to the Freedom of Information Act, 5 U.S.C. 552,
I request copies of the following records:

All contracts, task orders, and purchase orders for
[product/service category] awarded by [Agency Name]
between [date range].

Specifically, I request:
1. Vendor names and contract values
2. Statement of work or scope of services
3. Contract period of performance
4. Any performance evaluation reports

I am willing to pay fees up to $25 for this request.
Please contact me if fees will exceed this amount.

[Your name and contact info]
```

**Compliance:** FOIA is your legal right. No compliance concerns. Government transparency law.

**Applies to:** MM007_COLD_OUTBOUND, MM004_AGENCY_SERVICES, MM029_LOCAL_LEAD_GEN, MM063_LEAD_LIST_CURATION

---

## Category 5: Parallel dialers ($149-500/mo)

### The concept

Normal cold calling: you dial one number, wait for it to ring, get voicemail 80% of the time, hang up, dial next number. maybe 15-20 conversations per hour.

Parallel dialing: system dials 5-10 numbers simultaneously. AI detects voicemail vs human. only connects you when a real person picks up. 50-100+ conversations per hour. 5-10x productivity.

### Tool comparison

| Tool | Price | Lines | Best for | Key feature |
|------|-------|-------|----------|-------------|
| Orum | $250-500/mo | 5-10 | Solo/small team | AI-powered, clean UI |
| Nooks | $250-500/mo | 5-10 | SDR teams | Virtual floor, AI notes |
| Koncert | $200-400/mo | 5-8 | Enterprise | Local presence dialing |
| PhoneBurner | $149/mo | Power (sequential) | Solopreneurs | Voicemail drop + email |

### Orum (https://orum.com)

Best for solo operators and small teams. AI detects voicemail vs human. connects you only to live answers. 5-10 lines simultaneously.

**Setup:**
1. Sign up at orum.com
2. Upload lead list (must be DNC-scrubbed)
3. Import into CRM or use built-in tracking
4. Configure parallel settings (start with 5 lines, increase as you get comfortable)
5. Prep your call script (see Cold Outbound playbooks)
6. Start dialing

### Nooks (https://nooks.ai)

Best for teams. Virtual sales floor lets you see/hear teammates calling. AI takes notes automatically and syncs to CRM. gamification features.

**Setup:** Same as Orum but with team onboarding. AI note-taking is the killer feature. no manual CRM entry after calls.

### Koncert (https://koncert.com)

Enterprise-grade. Key feature: local presence dialing. when you call someone in Dallas, caller ID shows a Dallas area code. increases answer rates 2-3x.

**Setup:** Same as Orum. Enable local presence dialing for maximum answer rates.

### PhoneBurner (https://phoneburner.com)

Best bang for buck at $149/mo. not true parallel (power dialer = fast sequential) but includes voicemail drop and automatic email follow-up. all-in-one for solopreneurs.

**Setup:**
1. Sign up at phoneburner.com ($149/mo)
2. Upload leads
3. Record 2-3 voicemail drop messages (15-30 seconds each)
4. Create email follow-up templates
5. Start power dialing
6. No answer = drop voicemail + send email automatically
7. Answer = have conversation, log disposition
8. Built-in CRM tracks everything

**TCPA compliance for all dialers:**
- Scrub list against Do Not Call registry before loading
- Human must be on the line (no robocalling)
- Time restrictions: no calls before 8am or after 9pm local time
- Record consent where possible
- Keep call records

**Applies to:** MM007_COLD_OUTBOUND, MM004_AGENCY_SERVICES

---

## Category 6: Voicemail drops ($0.05-0.25/drop)

### Drop.co - Ringless voicemail

**What it does:** deposits voicemail directly into the recipient's voicemail box without ringing their phone. they see a missed voicemail notification.

**Why it matters:** people check voicemails. your message gets heard without the friction of a live cold call. good for warming leads before calling.

**Setup:**
1. Sign up at drop.co
2. Record voicemail script (15-30 seconds):
   ```
   "Hey [Name], this is [Your name] with [Company].
   I noticed [specific thing about their business].
   We helped [similar company] with [specific result].
   If that's interesting, my number is [number].
   Either way, hope you have a great week."
   ```
3. Upload lead list (DNC scrubbed)
4. Send drops in batches (100-500 at a time)
5. Track callback rate
6. Follow up callbacks immediately

**Compliance WARNING:**
- FCC considers ringless voicemail a "call" under TCPA
- Technically requires prior express consent
- Legality varies by state
- Lower risk: use for warm leads where some prior relationship exists
- Higher risk: cold list ringless voicemail
- Consult compliance counsel before scaling

### VoiceDrop.ai - AI personalized voicemail

**What it does:** same as Drop.co but uses AI voice cloning. you record a sample of your voice, then AI generates personalized voicemails with each prospect's name and company.

**Why it matters:** personalized voicemail has 2-3x callback rate vs generic drops. sounds like you personally recorded a message for them.

**Setup:**
1. Sign up at voicedrop.ai
2. Record 60-second voice sample for cloning
3. Create template with variables: {first_name}, {company}, {pain_point}
4. Upload lead list with those fields populated
5. AI generates unique voicemail per prospect
6. Send drops in batches
7. Track callbacks

**Additional compliance note:** AI-generated voice may trigger FTC synthetic media disclosure requirements. if your voice sounds AI-generated and someone asks, be honest.

**Applies to:** MM007_COLD_OUTBOUND, MM051_AI_AUTOMATION_AGENCY

---

## Category 7: TCPA-compliant lead generation ($0-200/mo)

### The TCPA problem

Telephone Consumer Protection Act (TCPA) requires prior express consent before calling or texting someone for marketing. fines: $500-$1,500 PER VIOLATION. FCC 1:1 consent rule (January 2025) now requires consent to YOUR SPECIFIC COMPANY, not generic "partners may contact you."

these four methods create rock-solid consent chains.

### Co-registration leads

**What it is:** leads that opted in on another company's site and specifically consented to be contacted by your company.

**Critical update (Jan 2025):** FCC 1:1 consent rule. the lead must have consented to YOUR SPECIFIC company name. generic "our partners" consent is no longer valid. verify this before buying ANY co-reg leads.

**How to use:**
1. Find co-reg lead providers in your niche (search "[your industry] lead generation")
2. VERIFY the consent language includes your company name specifically
3. Request sample of consent flow (screenshot the opt-in form)
4. Test with small batch (100 leads)
5. Track conversion rate vs cost per lead
6. Keep consent documentation for 5+ years

**Cost:** $5-50/lead depending on niche and qualification level

### Sweepstakes / giveaway lead gen

**What it is:** run a giveaway where entering requires providing contact info + TCPA consent. you control the entire consent chain.

**How to build:**
1. Choose prize that attracts YOUR ICP (not random people)
   - BAD: $100 Amazon gift card (attracts everyone)
   - GOOD: $500 worth of [industry-specific tool] (attracts your buyers)
2. Create landing page with:
   - Prize description
   - Entry form: name, email, phone
   - TCPA consent checkbox: "I agree to receive calls and texts from [YOUR COMPANY NAME] regarding [product/service]. Message and data rates may apply. Reply STOP to opt out."
   - Official sweepstakes rules link
3. Run ads (Meta, TikTok) to landing page
4. Collect entries = compliant leads
5. Call/text leads with compliant messaging
6. Follow up with product offer

**Compliance:**
- Must have official rules (no purchase necessary)
- State registration may be required for prizes >$500
- Consent language must name YOUR company specifically
- Keep all entry data for 5+ years

**Cost:** $1-10/lead (prize cost + ad spend amortized)

### SMS keyword opt-in

**What it is:** prospect texts a keyword to your phone number to opt in. the strongest possible TCPA consent because THEY initiated contact.

**How to build:**
1. Get SMS number:
   - Twilio: $1/mo + $0.0075/message
   - Postscript: $25/mo (Shopify focused)
   - SimpleTexting: $29/mo
2. Set up keyword trigger: "Text GROWTH to 55555"
3. Auto-reply with disclosure:
   ```
   "Thanks for opting in! You'll receive tips on [topic] from [Company].
   Msg frequency varies. Msg & data rates may apply. Reply STOP to cancel."
   ```
4. Promote keyword EVERYWHERE:
   - Twitter/X bio
   - TikTok bio
   - End of every content piece
   - Reply bait CTAs: "reply GROWTH or text GROWTH to 55555"
   - Physical marketing materials
   - Conference slides
5. Build SMS list of fully opted-in leads
6. Send value-first SMS sequence (1-2x/week max)
7. Convert to calls or sales

**Why this is gold:** the prospect texted YOU first. that's the strongest possible consent signal. combine with reply bait content strategy for maximum list building.

### Quiz funnel lead gen

**What it is:** interactive quiz that qualifies leads and captures contact info. prospect answers questions that segment them, then provides contact to get results.

**How to build:**
1. Choose quiz topic that maps to your ICP's pain point:
   - "What's your biggest growth bottleneck?"
   - "Which prayer style matches your personality?"
   - "What's your ideal workout split?"
2. Build 5-7 questions that segment the lead:
   - Question 1: Industry/niche (tells you their market)
   - Question 2: Team size (tells you their budget)
   - Question 3: Current solution (tells you their awareness)
   - Question 4: Biggest pain (tells you what to sell them)
   - Question 5: Timeline (tells you urgency)
3. Results page requires: name + phone + email + TCPA consent
4. Deliver results via email immediately
5. Call leads same day (reference their quiz answers)
6. Track which quiz paths convert best (optimize over time)

**Quiz platforms:**
- Typeform: $25/mo (clean UI, good analytics)
- Interact: $27/mo (built for lead gen)
- Outgrow: $22/mo (calculator + quiz templates)

**Why this converts:** you know their problem before you call them. "Hey [Name], I saw you took our quiz and your biggest challenge is [answer]. we've helped companies exactly like yours solve that."

**Applies to:** MM007_COLD_OUTBOUND, MM002_INFO_PRODUCTS, MM015_NEWSLETTER

---

## The full stack (recommended combination)

### Tier 0 - Free ($0/mo)

Run all of these from day 1:

1. **f5bot.com** - Reddit keyword alerts (10 min setup)
2. **freesubstats.com** - Subreddit growth tracking (10 min setup)
3. **LinkedIn People tab** - Competitor customer discovery (30 min/day)
4. **SEC EDGAR 10-K** - Enterprise pain point extraction (2 hrs/week)
5. **USAspending.gov** - Government contract intelligence (1 hr/week)

Total cost: $0. total setup: 1-2 hours. immediate lead flow.

### Tier 1 - Bootstrap ($149-200/mo)

Add when revenue supports:

6. **PhoneBurner** - Power dialer + voicemail drop + email ($149/mo)
7. **SMS keyword** - Opt-in list building ($29/mo via SimpleTexting)

Total cost: ~$178/mo. ROI positive at 1 closed deal.

### Tier 2 - Scale ($500-700/mo)

Add when call volume justifies:

8. **Orum or Nooks** - Parallel dialer ($250-500/mo)
9. **VoiceDrop.ai** - AI personalized voicemail drops (usage-based)
10. **Quiz funnel** - Qualified lead gen ($25/mo)

### Tier 3 - Enterprise ($1,000+/mo)

Add for government/enterprise sales:

11. **FOIA request program** - Deep contract intelligence ($0 but high time investment)
12. **Sweepstakes campaigns** - Compliant lead gen at scale (ad spend)
13. **Co-reg partnerships** - Volume lead acquisition ($5-50/lead)

---

## Cross-pollination with existing methods

| Lead gen method | Best paired with | Why |
|-----------------|-----------------|-----|
| f5bot Reddit alerts | MM006_CONTENT_FARM + MM001_APP_FACTORY | Discover what people want, build it, post about it |
| LinkedIn People tab | MM007_COLD_OUTBOUND + MM062_FRACTIONAL_EXEC | Find decision makers, outreach with personalized pitch |
| 10-K Risk Factors | MM004_AGENCY_SERVICES + MM051_AI_AUTOMATION | Reference their disclosed risks in pitch |
| USAspending | MM029_LOCAL_LEAD_GEN + MM063_LEAD_LIST_CURATION | Government contract opportunity mapping |
| Parallel dialers | MM007_COLD_OUTBOUND | 5-10x call productivity |
| Voicemail drops | MM007_COLD_OUTBOUND | Warm leads before live call |
| SMS keyword | MM015_NEWSLETTER + MM006_CONTENT_FARM | Build compliant list from content |
| Quiz funnels | MM002_INFO_PRODUCTS + MM015_NEWSLETTER | Qualify and segment leads automatically |

---

## Implementation priority

**Start today (free, immediate value):**
1. f5bot keyword alerts
2. freesubstats subreddit tracking
3. LinkedIn People tab scraping

**Start this week (free, requires research time):**
4. SEC 10-K Risk Factor analysis
5. USAspending.gov contract mapping

**Start when budget allows ($149-200/mo):**
6. PhoneBurner power dialer
7. SMS keyword opt-in

**Scale when validated ($500+/mo):**
8. Parallel dialer upgrade
9. AI voicemail drops
10. Quiz funnel

---

## Category 8: Competitive intelligence ($0-15/mo)

### Visualping.io - Competitor change detection

**What it does:** monitors any web page for changes. price changes, hiring pages, product updates, feature removals. alerts within minutes of any change.

**Why it matters:** @pipelineabuser monitors 200+ competitor pages. price increase = their customers may switch to you. new hires = expansion signal for outreach. feature removal = gap in market you can fill.

**Setup (30 minutes):**
1. Sign up at visualping.io (free tier: 5 pages, 2 checks/day)
2. Add competitor pricing pages
3. Add competitor career/hiring pages
4. Add competitor product/feature pages
5. Set check frequency (hourly for pricing, daily for others)
6. When alert fires:
   - **Price increase:** outreach to their customers. "noticed [competitor] raised prices. we offer [same thing] at [lower price]."
   - **New hire posting:** expansion signal. offer your product to help them scale.
   - **Feature removal:** gap in market. build/promote your version.
   - **New feature launch:** update your competitive positioning.
7. Outreach within 24 hours of change for maximum impact

**Compliance:** none. monitoring public web pages is legal and standard practice.

**Applies to:** MM007_COLD_OUTBOUND, MM001_APP_FACTORY, MM006_CONTENT_FARM

---

### G2/Capterra/Trustpilot - Bad review mining

**What it does:** finds people who left 1-2 star reviews on competitor products. these are documented unhappy customers with budget (they already pay for the category).

**Why it matters:** someone who left a bad review has:
- an allocated budget (they bought the competitor)
- a documented pain point (they wrote about it)
- urgency (they're frustrated enough to write a public review)
- decision-making authority or influence (they chose the tool)

**Setup (1 hour):**
1. Search G2/Capterra/Trustpilot for your main competitors
2. Filter reviews: 1-2 stars, most recent first
3. For each review:
   - Note the specific complaints
   - Find the reviewer on LinkedIn (same name, company often visible)
   - Add to your outreach list
4. Outreach within 2 weeks of review

**The message:**
```
Hey [Name],

Saw your review of [Competitor] mentioning [specific complaint from review].

We built [Product] specifically to fix that problem.
[One sentence about how you solve it differently].

Worth a quick look? Here's a 5-minute demo: [link]
```

**Compliance:** none. public reviews on public platforms.

**Applies to:** MM007_COLD_OUTBOUND, MM004_AGENCY_SERVICES

---

### Court/PACER litigation mining

**What it does:** searches public court records for companies sued for issues your product prevents. cybersecurity breach lawsuits = security product leads. employment lawsuits = HR tool leads.

**Why it matters:** a company that just got sued for something your product prevents has:
- immediate urgency (legal action)
- budget approval (legal costs already flowing)
- executive attention (lawsuits reach the C-suite)
- motivation to prevent recurrence

**Setup (3 hours first batch):**
1. Go to CourtListener (free) or PACER ($0.10/page)
2. Search for lawsuits in your product category:
   - Data breach lawsuits > sell security products
   - Employment discrimination > sell HR compliance tools
   - OSHA violations > sell safety products
   - Contract disputes > sell project management tools
3. Identify the defendant companies
4. Research on LinkedIn for decision makers
5. Outreach: "noticed recent litigation around [issue]. our clients avoid this because [how your product helps]."

**Compliance:** none. public court records. PACER is the official US courts database.

**Applies to:** MM007_COLD_OUTBOUND, MM004_AGENCY_SERVICES, MM060_AI_COMPLIANCE_AUDIT

---

## Category 9: Multi-channel outbound ($0)

### Voice note outbound (LinkedIn/IG)

**What it does:** send personalized voice notes via social DMs instead of text. 40%+ reply rate on LinkedIn. 3x engagement vs text DMs.

**Why it matters:** voice notes are the #1 outbound pattern interrupt in 2026. @pipelineabuser confirmed: "the voice note is doing stupid numbers right now."

**Setup (1 hour):**
1. Identify your target prospect
2. Research their recent posts, company news, or content
3. Record a 45-60 second voice note:
   ```
   "Hey [Name], this is [You]. Saw your [specific post/article/company news].
   [One specific observation or compliment - not generic].
   Quick question: [one clear question relevant to their pain point].
   If that's interesting, happy to share how we've helped [similar company] with that.
   Either way, great content you're putting out."
   ```
4. Send via LinkedIn or IG DM
5. If no reply in 48 hours, follow up with text message referencing the voice note

**Why voice beats text:**
- pattern interrupt (nobody expects a voice note)
- trust signal (they hear your real voice)
- effort signal (shows you cared enough to record)
- can't be AI-generated (yet) so it feels authentic
- harder to ignore than text

**Compliance:** none. using platform features as designed.

**Applies to:** MM007_COLD_OUTBOUND, MM004_AGENCY_SERVICES

---

### Loom video prospecting

**What it does:** record personalized Loom videos showing the prospect's own website/product. 40%+ reply rates for high-value prospects.

**Why it matters:** showing someone their own website on screen is the ultimate personalization. it proves you did the research. only worth the time for $10K+ deals.

**Setup:**
1. Install Loom Chrome extension
2. Open prospect's website in one tab
3. Hit record. 45-60 seconds max.
4. Walk through one specific thing you noticed about their site/business
5. Suggest one concrete improvement
6. CTA: "happy to show you what this would look like. 15 minutes?"
7. Email with Loom link. thumbnail shows prospect's name or website.

**Compliance:** none. standard sales practice.

**Applies to:** MM007_COLD_OUTBOUND, MM004_AGENCY_SERVICES (high-ticket only)

---

### Cold DM > Voice Note > Email sequence

**What it does:** multi-channel sequence across social + voice + email. 2.5x reply rate vs email alone.

**Why it matters:** familiarity compounds across touchpoints. by the time the email arrives, they recognize your name.

**The sequence:**
```
Day 1: Cold DM on LinkedIn/X
  - Short, specific observation about their work
  - End with a question (not a pitch)

Day 3: Voice note follow-up (same platform)
  - Reference your DM
  - Add something new (company news, their recent post)
  - 45-60 seconds

Day 5: Email (new channel)
  - Reference both previous touchpoints
  - Add social proof (case study, testimonial)
  - Clear CTA (15-minute call)

Day 8: Final email follow-up
  - Breakup email: "No worries if not a fit"
  - Attach case study PDF
  - Offer to stay connected
```

**Compliance:** CAN-SPAM for emails. platform rules for DMs.

**Applies to:** MM007_COLD_OUTBOUND, MM004_AGENCY_SERVICES

---

## Category 10: Market research tools ($0)

### FB Ads Library product research

**What it does:** shows every active ad on Facebook/Instagram. if someone is paying for ads for 2+ months, they are making money. reverse-engineer winning products and funnels.

**Setup (30 minutes):**
1. Go to facebook.com/ads/library
2. Search keywords: "Ebook" "Digital Download" "PDF" "Printable" "Template" "Guide" "Course" "Planner"
3. Filter by "Active" ads running 2+ months
4. For each winner: screenshot the ad > click through to landing page > analyze the funnel
5. Note: pricing, value proposition, ad creative, landing page layout, CTA
6. Clone the approach for your niche

**Compliance:** none. Meta provides this transparency tool publicly.

**Applies to:** MM001_APP_FACTORY, MM002_INFO_PRODUCTS, MM025_DIGITAL_PRODUCTS

---

### AppKittie trending app discovery

**What it does:** daily updated list of trending apps and new big hits in app stores.

**Setup:** check appkittie.com daily > "New Big Hits" section > identify viral apps > cross-reference with niche opportunities > build adapted version in 2-4 weeks.

**Real example:** christian app launched, got 1,700+ reviews and $100K+ revenue in 5 days.

**Applies to:** MM001_APP_FACTORY

---

### TikTok trend research for apps

**What it does:** monitor TikTok trends for viral concepts that could become apps.

**Why it matters:** Connor Burd built a $185K/mo app portfolio using this exact method. heavy TikTok research + App Store cross-reference = validated demand before building.

**Setup:** monitor TikTok trends daily > search relevant hashtags > cross-reference with appkittie > identify concepts with existing audiences > partner with niche influencers > build.

**Applies to:** MM001_APP_FACTORY, MM006_CONTENT_FARM

---

## Category 11: Content distribution ($0-5K/mo)

### Reddit GEO distribution

**What it does:** Reddit provides 68% of AI answer citations. GEO-optimized Reddit posts get cited by ChatGPT, Claude, and Perplexity, driving organic traffic.

**Setup:**
1. Identify relevant subreddits
2. Create value-first posts with helpful content
3. Use specific data, tables, and structured formatting (AI loves structured content)
4. Include natural links to your site/product
5. Answer questions thoroughly (AIs prefer comprehensive answers)
6. Your posts become training data and get cited in AI responses

**Compliance:** follow subreddit rules. value-first not spam.

**Applies to:** MM011_SEO_GEO, MM006_CONTENT_FARM

---

### Clipper network distribution

**What it does:** pay 300-500 clippers $1/1K views to distribute your content across accounts simultaneously. volume testing beats single influencer gambles.

**Real numbers:** @tatealax documented 43K downloads for $6K spend.

**Setup:**
1. Build clipper roster via DMs/Whop
2. Distribute content briefs (hook + CTA + target platform)
3. Pay performance-based ($1/1K views)
4. A/B test 5-10 hook variations across the network
5. Double down on winning hooks
6. Scale the network

**Compliance:** standard influencer/affiliate payment model.

**Applies to:** MM006_CONTENT_FARM, MM001_APP_FACTORY

---

### Programmatic SEO landing pages

**What it does:** build 1000+ landing pages targeting long-tail keywords. each page = feature + niche/location variation.

**Example variations:**
- "habit tracker for nurses"
- "habit tracker for teachers"
- "habit tracker for college students"
- "prayer app for catholics"
- "prayer app for muslims"
- "fitness app for seniors"
- ...1000 more

**Setup:**
1. List all product features
2. Cross with niches/locations/professions/demographics
3. Create page template
4. Generate variations programmatically
5. Internal link to main product page
6. Each page targets a unique long-tail keyword

**Compliance:** standard SEO.

**Applies to:** MM011_SEO_GEO, MM001_APP_FACTORY

---

## Updated stack at a glance

| Category | Methods | Cost | Time to first lead |
|----------|---------|------|--------------------|
| Reddit intel | f5bot + freesubstats | $0 | Same day |
| LinkedIn intel | People tab + job change filter + profile priming | $0-99/mo | Same day |
| SEC filings | 10-K Risk Factors | $0 | 1-2 hours |
| Government intel | FOIA + USAspending | $0 | Same day (USAspending) / 20-60 days (FOIA) |
| Competitive intel | Visualping + Bad review mining + Court/PACER | $0-15/mo | Same day |
| Multi-channel outbound | Voice notes + Loom video + DM>Voice>Email | $0-15/mo | Same day |
| Market research | FB Ads Library + AppKittie + TikTok trends + IdeaBrowser + Product Hunt | $0 | Same day |
| Content distribution | Reddit GEO + Clipper network + Programmatic SEO | $0-5K/mo | 1-7 days |
| Parallel dialers | Orum / Nooks / Koncert / PhoneBurner | $149-500/mo | Same day |
| Voicemail drops | Drop.co / VoiceDrop.ai | $0.05-0.25/drop | Same day |
| TCPA compliance | Co-reg / Sweepstakes / SMS keyword / Quiz | $0-200/mo | 1-7 days |
| Enrichment | Clay + Apollo + BuiltWith | $0-995/mo | 1-4 hours |
| Automation | n8n self-hosted | $0-20/mo | 4 hours |

---

## Legal compliance audit summary

| Method | Risk Level | Notes |
|--------|-----------|-------|
| f5bot / freesubstats / Google Alerts | NONE | Public data monitoring |
| LinkedIn People tab (manual) | LOW | Using platform as designed |
| LinkedIn Sales Navigator | LOW | Using platform as designed |
| SEC 10-K / EDGAR | NONE | Public filings |
| USAspending.gov | NONE | Public government data |
| FOIA requests | NONE | Legal right under federal law |
| Visualping change detection | NONE | Public web page monitoring |
| G2/Capterra review mining | NONE | Public reviews |
| Court/PACER searches | NONE | Public court records |
| FB Ads Library | NONE | Public Meta transparency tool |
| AppKittie / Product Hunt / TikTok | NONE | Public platform data |
| Voice note DMs | LOW | Platform features as designed |
| Loom video prospecting | NONE | Standard sales practice |
| Multi-channel DM+email | LOW | CAN-SPAM compliance needed for email |
| Clay / Apollo enrichment | LOW | Public data aggregation |
| Reddit GEO distribution | LOW | Must follow subreddit rules |
| Clipper network | LOW | Standard influencer payments |
| Parallel dialers (Orum etc) | MEDIUM | TCPA compliance required: DNC scrubbing, business lines, time restrictions |
| Voicemail drops (ringless) | MEDIUM-HIGH | FCC considers a "call" under TCPA. State-specific restrictions. Consult attorney. |
| Co-registration leads | MEDIUM | FCC 1:1 consent rule (Jan 2025) requires YOUR company named specifically |
| SMS keyword opt-in | LOW | Strongest TCPA consent (prospect initiates) |
| Sweepstakes lead gen | LOW | Must have official rules. State registration for prizes >$500. |
| Quiz funnel lead gen | LOW | Include TCPA consent before results delivery |
| Sorority BDR LinkedIn | MEDIUM | LinkedIn TOS risk if accounts appear automated |
| Profile view priming | LOW | Normal LinkedIn behavior |
| n8n automation | NONE | Self-hosted infrastructure |

---

## Tracking

All methods tracked in: `LEDGER/RESEARCH_METHODS_LEAD_GEN.csv` (50 entries: LG001-LG050)

Launch directories tracked in: `LEDGER/LAUNCH_DIRECTORIES.csv` (42 entries: LD001-LD042)

Status: ALL entries PENDING_REVIEW until human validation.

Review with: `/review-alpha`
