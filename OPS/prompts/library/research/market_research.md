# Market Research

Research niche opportunities and market viability. Outputs actionable market intelligence.

---

## System prompt

```
You are a market research analyst for solopreneur ventures. You identify profitable niches, validate opportunities, and assess market viability.

Approach:
- Data-driven when possible
- Honest about uncertainty
- Focus on actionable insights
- Bootstrap-friendly (no enterprise research needed)

Output format:
- Clear section headers
- Bullet points for key findings
- Tables for comparisons
- Specific numbers when available
- Recommendations at the end
```

---

## User prompt template

```
Research the [NICHE/MARKET] opportunity.

Research goals:
[GOALS - market size, competition level, customer segments, pricing potential, entry barriers]

What I'm considering:
- Product idea: [IDEA]
- Business model: [MODEL - SaaS, course, service, content]
- Budget constraints: [BUDGET]
- Time constraints: [TIME]

Specific questions:
[QUESTIONS - what you need to know to make a decision]

Data sources to check:
[SOURCES - optional: specific sites, tools, or data you want analyzed]
```

---

## Example output

**Input:**
```
Research the "AI writing tools for lawyers" opportunity.

Research goals:
- Market size and growth
- Competition level
- Customer willingness to pay
- Entry barriers

What I'm considering:
- Product idea: AI tool that drafts legal documents
- Business model: SaaS
- Budget constraints: $5,000 to build MVP
- Time constraints: 3 months to launch

Specific questions:
1. Are lawyers actually using AI tools?
2. What do they pay for existing tools?
3. What's the competition like?
4. Can I build something differentiated with limited budget?
```

**Output:**

```
## Market research: AI writing tools for lawyers

### Market overview

**Market size signals:**
- US legal services market: ~$350B annually
- Legal tech market: ~$30B and growing 8% yearly
- AI in legal: Estimated $1.2B in 2024, projected $10B+ by 2030

**Why this matters for you:**
Even capturing 0.001% of legal tech = $300K revenue potential. The market is big enough.

### Adoption signals

**Are lawyers using AI tools?**
- Thomson Reuters survey (2023): 67% of lawyers report using or planning to use AI
- Clio Legal Trends Report: AI tool adoption up 35% year over year
- ABA survey: 49% of solo/small firm lawyers have tried AI tools

**Caveat:** Adoption is high but actual payment is different. Many use free tools.

**What they use AI for:**
1. Document review and summarization
2. Legal research assistance
3. Contract drafting and analysis
4. Client communication drafts
5. Billing and time tracking

Your idea (document drafting) is in the top 3 use cases.

### Competition landscape

**Major players:**
| Tool | Focus | Pricing | Funding |
|------|-------|---------|---------|
| Harvey AI | General legal AI | Enterprise ($$$) | $80M raised |
| CoCounsel (Casetext) | Research + drafting | $500/mo | Acquired by Thomson Reuters |
| Spellbook | Contract drafting | $100-300/mo | $10M raised |
| LegalRobot | Contract analysis | Freemium | Self-funded |

**Key insight:** Heavy VC funding means these companies will outspend you. But they also target larger firms.

### Gap analysis

**Who's underserved:**
1. **Solo practitioners** - Can't afford $500/mo tools
2. **Small firms (2-10 lawyers)** - Need value, not enterprise features
3. **Specific practice areas** - General tools don't serve immigration, family law, etc. well
4. **Non-US markets** - Most tools are US-focused

**Potential angles:**
- Price point: $50-99/mo for small firms
- Specialization: Pick one practice area (immigration, real estate, etc.)
- Simplicity: "Good enough" tool vs enterprise perfection
- Geography: Non-US common law markets (UK, Canada, Australia)

### Pricing data

**What lawyers pay for software:**
- Clio (practice management): $39-129/user/mo
- Westlaw (research): $400-800+/mo
- Contract tools: $50-500/mo depending on features

**Willingness to pay indicators:**
- Solo practitioners: Budget-conscious, $50-100/mo typical
- Small firms: $100-300/mo if it saves billable hours
- Mid-size firms: $300-500/mo but expect more features

**Calculation:** If you charge $79/mo and need $10K MRR for sustainability, you need ~127 customers.

### Entry barriers

**Technical barriers:**
- AI model costs: ~$0.002-0.10 per document depending on complexity
- Legal accuracy requirements: Higher bar than general writing
- Integration needs: Lawyers use Clio, MyCase, PracticePanther

**Market barriers:**
- Lawyers are skeptical of new tools
- Sales cycle is long (1-3 months typical for SaaS)
- Trust is everything (need testimonials, maybe bar association approval)
- Malpractice concerns around AI outputs

**Regulatory considerations:**
- Unauthorized practice of law rules
- Must position as "drafting assistance" not "legal advice"
- Need disclaimers about lawyer review required

### Your constraints analysis

**$5,000 budget reality:**
- Can build MVP with API-based AI (OpenAI, Anthropic)
- Can't build custom models
- Can't afford heavy marketing
- Focus on organic acquisition: content, communities, referrals

**3-month timeline reality:**
- Week 1-4: Build core document generation
- Week 5-8: Add 2-3 document templates, basic UI
- Week 9-12: Beta testing with 5-10 lawyers, iterate

This is tight but doable for an MVP.

### Recommendations

**1. Specialize immediately**
Pick ONE practice area. Suggestions:
- Immigration (forms-heavy, clear templates)
- Real estate (standardized documents)
- Employment (contracts, offer letters)

General legal AI is a losing battle against well-funded competitors.

**2. Price for solos and small firms**
- $49/mo solo tier
- $99/mo firm tier (3 users)
- Undercut the $300+ tools significantly

**3. Lead with templates, not AI**
Position as "legal document templates with AI assistance," not "AI legal tool."
This reduces the scary factor and positions against document template companies, not AI giants.

**4. Build trust early**
- Get 5 lawyer beta users before launch
- Collect testimonials before charging
- Consider partnership with a bar association or legal blogger

**5. Distribution strategy**
- Content marketing: "How to draft [X] agreement" blog posts
- Communities: Reddit (r/lawyers), legal Facebook groups
- Referrals: Offer affiliate program to legal bloggers

### Decision framework

**Green lights:**
- [ ] Market is large enough
- [ ] Competitors leave gaps you can fill
- [ ] You can build MVP in budget/time
- [ ] Clear path to first 10 customers

**Yellow flags:**
- Long sales cycles
- Trust/credibility barrier as non-lawyer
- Malpractice concern requires careful positioning

**Red flags if:**
- You have no connection to legal industry
- You can't get 5 beta users before building
- You're competing head-on with Harvey/CoCounsel

### What I can't determine

- Actual churn rates for legal SaaS
- Specific conversion rates from content
- Whether your specific product idea resonates (need customer interviews)
- Regulatory requirements in your jurisdiction

**Recommended next step:** Talk to 5-10 lawyers before building anything. Validate the problem and your specific solution.
```

---

## Variations

### Quick validation research
```
Do a quick validation check for [IDEA].

In 30 minutes of research, find:
- Are people searching for this? (Google Trends, keyword tools)
- Are people paying for alternatives? (List 3-5 with pricing)
- Are people complaining about existing solutions? (Reddit, forums)
- What's the Reddit/Twitter sentiment?

Output: Go/No-Go recommendation with key evidence
```

### Niche deep dive
```
Research [NICHE] in depth.

Cover:
- Who are the customers (demographics, psychographics)
- What problems do they have (with evidence)
- What solutions exist (and their limitations)
- What would a successful product look like
- How would you reach these customers

Output: Niche viability assessment with specific opportunity
```

### Trend analysis
```
Analyze the trend around [TOPIC/TECHNOLOGY].

Determine:
- Is this growing or fading?
- What's driving the trend?
- Who's benefiting from it?
- How long might it last?
- Where are the opportunities for a solopreneur?

Output: Trend assessment with timing recommendations
```

---

## Data sources

**Free sources:**
- Google Trends
- Reddit (use search to find relevant subreddits)
- Twitter/X (search for complaints, questions)
- Product Hunt (launch reception of similar products)
- G2/Capterra reviews (competitor feedback)
- SEMrush/Ahrefs free tier (keyword volume)
- SimilarWeb (traffic estimates)

**Paid sources (if needed):**
- Statista (market data)
- IBISWorld (industry reports)
- SEMrush/Ahrefs (full keyword data)
- Crunchbase (funding data)

---

## Quality checklist

- [ ] Market size estimated with sources
- [ ] Competition mapped with specifics
- [ ] Gaps and opportunities identified
- [ ] Constraints acknowledged
- [ ] Actionable recommendations provided
- [ ] Unknowns stated clearly
- [ ] No promotional language
- [ ] Would this help make a go/no-go decision?
