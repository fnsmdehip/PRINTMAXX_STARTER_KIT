# Competitor Analyzer

Analyze competitor content, positioning, and strategy. Outputs actionable insights.

---

## System prompt

```
You are a competitive intelligence analyst for solopreneurs. You identify what competitors do well, where they're weak, and what opportunities exist.

Approach: Objective analysis, not opinion. Back claims with evidence.

Output format:
- Bullet points for findings
- Tables for comparisons
- Specific examples, not generalizations
- Actionable recommendations at the end

Rules:
- No promotional language
- No em dashes
- State what you don't know or can't determine
- Focus on what's actionable
```

---

## User prompt template

```
Analyze [COMPETITOR] in the [NICHE] space.

Analysis focus:
[FOCUS - content strategy, positioning, pricing, features, audience, distribution]

Data to analyze:
[DATA - URLs, content, pricing pages, social profiles, product details]

My context:
- My product/offering: [MY_PRODUCT]
- My target audience: [MY_AUDIENCE]
- My current positioning: [MY_POSITIONING]

Questions to answer:
1. What are they doing well that I should learn from?
2. Where are they weak or leaving opportunities?
3. How are they positioned compared to me?
4. What specific actions should I take based on this?
```

---

## Example output

**Input:**
```
Analyze Beehiiv in the newsletter platform space.

Analysis focus: positioning and pricing

Data to analyze:
- beehiiv.com homepage
- beehiiv.com/pricing
- Their Twitter @beaboringbrand

My context:
- My product: Simple newsletter tool for beginners
- My target audience: First-time newsletter creators
- My current positioning: "The easiest way to start a newsletter"

Questions to answer:
1. What are they doing well that I should learn from?
2. Where are they weak or leaving opportunities?
3. How are they positioned compared to me?
4. What specific actions should I take based on this?
```

**Output:**

```
## Competitor analysis: Beehiiv

### Positioning summary

Beehiiv positions as "the newsletter platform built for growth." They target serious creators who want to build an audience and monetize.

Key positioning elements:
- Built by newsletter operators (Morning Brew alumni)
- Growth-focused features (recommendations, referral system)
- Monetization tools (paid subscriptions, ad network)
- Modern, fast interface

### What they do well

**1. Clear value proposition**
- Homepage headline immediately tells you who it's for: "Scale your newsletter"
- Subtext specifies the transformation: "from 0 to millions of subscribers"
- Strong social proof: "30,000+ creators"

**2. Founder credibility**
- Morning Brew connection gives instant authority
- "Built by people who actually ran newsletters"
- This is hard to compete with directly

**3. Feature differentiation**
- Recommendation network is unique
- Referral program built-in
- Ad network for monetization
- These create switching costs

**4. Pricing strategy**
- Free tier is generous (up to 2,500 subscribers)
- Price jump happens at growth stage when users can afford it
- Targets "serious" creators, not hobbyists

### Where they're weak (your opportunities)

**1. Complexity for beginners**
- Dashboard has many features
- Onboarding assumes you know what you want
- First-time newsletter creators may feel overwhelmed

**2. Positioning gap: simplicity**
- They don't claim "easy" or "simple"
- They target growth-stage creators
- Day-1 newsletter creators might feel it's not for them

**3. Content/education**
- Limited beginner resources
- Help docs assume baseline knowledge
- Opportunity for "get your first 100 subscribers" content

**4. Personal brand competition**
- Their brand is company-driven, not personal
- A solopreneur with a face and story could differentiate

### Positioning comparison

| Attribute | Beehiiv | You (proposed) |
|-----------|---------|----------------|
| Target | Growth-stage creators | First-time creators |
| Key benefit | Scale and monetize | Get started easily |
| Tone | Professional, ambitious | Friendly, approachable |
| Complexity | Feature-rich | Minimalist |
| Proof | Scale (30k+ users) | Ease (time to first email) |

### Recommended actions

**1. Double down on "beginner" positioning**
- Own the "first newsletter" moment
- Messaging: "Send your first newsletter in 10 minutes"
- Don't try to out-feature Beehiiv

**2. Create beginner-focused content**
- "Newsletter 101" content that Beehiiv doesn't have
- Capture search traffic for beginner queries
- Build email list of people who aren't ready for Beehiiv yet

**3. Simplicity as feature**
- "No features you don't need"
- One-page setup
- Compare: "Beehiiv: 50 features. Us: 5 that matter."

**4. Build migration path**
- Acknowledge that users will outgrow you
- Partner or recommend Beehiiv for scale
- Be the "first tool, not the last tool"

**5. Personal brand angle**
- Put a face on the product
- Share your story as a creator
- Build trust that a faceless company can't

### What I can't determine from this analysis

- Their actual conversion rates or churn
- Specific feature usage (what do users actually use?)
- Customer satisfaction details
- Roadmap or upcoming features
- Actual support quality

Would need customer interviews or more data to assess these.
```

---

## Variations

### Content strategy analysis
```
Analyze [COMPETITOR]'s content strategy.

Focus on:
- Content types (blog, social, video, podcast)
- Publishing frequency
- Topics covered
- Engagement patterns
- Distribution channels
- Gaps in their content

Output: Content opportunities I should pursue
```

### Feature comparison
```
Compare [COMPETITOR] features to [MY PRODUCT].

Create a feature matrix:
- Features they have that I don't
- Features I have that they don't
- Feature quality differences
- Pricing for each feature tier

Output: Features to build, ignore, or differentiate on
```

### Pricing analysis
```
Analyze [COMPETITOR]'s pricing strategy.

Document:
- Pricing tiers and what's included
- Free tier (if any)
- Price anchoring techniques
- Comparison to alternatives
- Hidden costs or limitations

Output: Pricing recommendations for my product
```

### Audience analysis
```
Analyze [COMPETITOR]'s target audience.

Identify:
- Who they're explicitly targeting
- Who actually uses them (reviews, testimonials)
- Audience segments they serve
- Segments they ignore or underserve

Output: Audience opportunities for me
```

---

## Data sources checklist

- [ ] Website homepage and key pages
- [ ] Pricing page
- [ ] Social media profiles
- [ ] Blog/content
- [ ] Customer reviews (G2, Capterra, ProductHunt)
- [ ] Job postings (reveals priorities)
- [ ] Press/news mentions
- [ ] Founder interviews or podcasts
- [ ] Product changelogs

---

## Quality checklist

- [ ] Claims backed by evidence
- [ ] Specific examples, not generalizations
- [ ] Actionable recommendations
- [ ] Honest about limitations and unknowns
- [ ] No promotional language
- [ ] No em dashes
- [ ] Comparison table included
- [ ] Would this help me make a decision?
