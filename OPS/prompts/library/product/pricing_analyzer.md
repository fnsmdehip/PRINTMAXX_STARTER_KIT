# Pricing Analyzer

Analyze pricing strategies and recommend pricing for products. Outputs pricing recommendations with rationale.

---

## System prompt

```
You are a pricing strategist for solopreneur products. You help set prices that capture value, remain competitive, and support sustainable business models.

Approach:
- Value-based pricing over cost-plus
- Consider the whole market, not just direct competitors
- Account for solopreneur constraints (no enterprise sales team)
- Think about pricing psychology and anchoring

Output format:
- Market analysis with competitor pricing
- Value-based pricing calculation
- Recommended pricing structure
- Pricing page recommendations
- Risks and mitigation
```

---

## User prompt template

```
Analyze pricing for [PRODUCT].

Product details:
- Product: [PRODUCT]
- Type: [TYPE - SaaS, course, ebook, service, tool]
- Value delivered: [VALUE - what problem it solves, outcomes]
- Target customer: [CUSTOMER]

Competitor context:
[COMPETITORS - list competitors with their pricing if known]

Business constraints:
- Costs: [COSTS - hosting, API calls, time, etc.]
- Revenue goal: [GOAL - MRR target, yearly revenue]
- Customer target: [TARGET - number of customers needed]

Questions to answer:
1. What should I charge?
2. How should I structure pricing (tiers, one-time, etc.)?
3. How does this compare to the market?
4. What are the risks of this pricing?
```

---

## Example output

**Input:**
```
Analyze pricing for a social media scheduling tool.

Product details:
- Product: SimplePost - social scheduling for solopreneurs
- Type: SaaS
- Value delivered: Save 5 hours/week on social media posting, post consistently
- Target customer: Solopreneurs and small creators

Competitor context:
- Buffer: $6-120/month
- Hootsuite: $99-739/month
- Later: $18-80/month
- Publer: $12-84/month
- Hypefury: $19-49/month

Business constraints:
- Costs: ~$2/user/month (hosting, API)
- Revenue goal: $5,000 MRR
- Customer target: Need to figure out

Questions to answer:
1. What should I charge?
2. How should I structure pricing?
3. How does this compare to the market?
4. What are the risks?
```

**Output:**

```
## Pricing analysis: SimplePost

### Market positioning

**Competitor price mapping:**

| Tool | Low Tier | Mid Tier | High Tier | Position |
|------|----------|----------|-----------|----------|
| Buffer | $6 | $15 | $100+ | Freemium, scales with channels |
| Hootsuite | $99 | $249 | $739 | Enterprise-focused |
| Later | $18 | $40 | $80 | Visual content focus |
| Publer | $12 | $24 | $84 | Budget alternative |
| Hypefury | $19 | $39 | $49 | Creator/Twitter focus |

**Market observations:**
- Wide price range ($6 to $739) based on features and target market
- Budget tier: $6-20/month
- Mid-market: $20-50/month
- Professional: $50-100/month
- Enterprise: $100+/month

**Your position:** Budget to mid-market for solopreneurs. Don't compete with enterprise.

---

### Value-based pricing analysis

**The value calculation:**

*Time saved:* 5 hours/week x 4 weeks = 20 hours/month

*What's an hour worth to a solopreneur?*
- If they value time at $50/hour (conservative)
- Monthly value = 20 hours x $50 = $1,000/month

*Pricing principle:* Charge 5-10% of value delivered.

**Value-based price range:** $50-100/month

*But wait:* Solopreneurs are price-sensitive and have alternatives. Market dynamics matter.

---

### Competitive positioning analysis

**Where you can win:**

| Factor | You | Buffer | Hypefury |
|--------|-----|--------|----------|
| Simplicity | Yes | Medium | Medium |
| Price | TBD | $6-15 | $19-49 |
| Solopreneur focus | Yes | No (teams) | Yes (creators) |
| Features | Minimal | Many | Twitter-heavy |

**Positioning options:**

1. **Undercut on price:** $9/month flat
   - Pros: Easy decision, budget conscious market
   - Cons: Low revenue per customer, need volume

2. **Match mid-market:** $19-29/month
   - Pros: Sustainable margins, quality signal
   - Cons: Need to justify vs Buffer's $6 tier

3. **Premium simple:** $49/month
   - Pros: Fewer customers needed, quality customers
   - Cons: Hard to justify without unique value

---

### Recommended pricing structure

**Recommendation: Two-tier pricing**

| Tier | Price | Includes | Target |
|------|-------|----------|--------|
| Starter | $12/month | 3 social accounts, 30 posts/month, basic analytics | Testing the waters |
| Pro | $29/month | 10 accounts, unlimited posts, advanced scheduling | Serious solopreneurs |

**Why this structure:**

1. **$12 Starter:**
   - Lower than Later ($18), above Buffer free
   - Enough for someone with 1-3 platforms
   - Easy "yes" for price-sensitive solopreneurs
   - Monthly cap encourages upgrade or validates light users

2. **$29 Pro:**
   - Sweet spot between cheap and premium
   - Unlimited removes friction
   - "Unlimited" is psychological unlock
   - Matches Hypefury's mid-tier positioning

**Annual pricing:**
- Starter: $99/year (31% discount)
- Pro: $249/year (28% discount)

---

### Revenue math

**Goal:** $5,000 MRR

| Scenario | Starter @ $12 | Pro @ $29 | MRR |
|----------|---------------|-----------|-----|
| All Starter | 417 customers | 0 | $5,000 |
| All Pro | 0 | 173 customers | $5,000 |
| Mixed (60/40) | 200 customers | 76 customers | $4,604 |
| Mixed (40/60) | 125 customers | 115 customers | $4,835 |

**Target mix:** 40% Starter, 60% Pro = ~290 total customers for $5K MRR

**Costs at scale:**
- 290 customers x $2/user = $580/month costs
- Gross margin: ~88%

---

### Pricing page recommendations

**Structure:**

```
Starter               Pro (Popular)
$12/month            $29/month
$99/year save 31%    $249/year save 28%

- 3 social accounts   - 10 social accounts
- 30 posts/month      - Unlimited posts
- Basic analytics     - Advanced analytics
- Email support       - Priority support
                      - Bulk scheduling
                      - Team member (1)

[Start free trial]    [Start free trial]
```

**Tactics:**

1. **Anchor with annual:** Show annual price prominently with savings percentage
2. **Default to Pro:** Mark Pro as "Popular" or "Recommended"
3. **14-day free trial:** On Pro tier, convert to paid after
4. **No free tier:** Reduces support burden, attracts serious users
5. **Money-back guarantee:** "Full refund within 30 days, no questions"

---

### Alternative pricing models considered

**Option A: Single price ($19/month)**
- Simpler to explain and manage
- Misses price-sensitive segment
- Misses upsell opportunity
- Verdict: Good for V1, consider tiers later

**Option B: Usage-based (per post)**
- Aligns with value
- Unpredictable for users
- Hard to forecast revenue
- Verdict: Too complex for solopreneurs

**Option C: Freemium**
- Lower barrier
- High support cost
- Harder to convert
- Verdict: Only if building for scale

---

### Risks and mitigation

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Price too high, no signups | Medium | High | Start lower, increase later |
| Price too low, unsustainable | Low | Medium | Easy to raise prices with new customers |
| Competitor undercuts | Medium | Medium | Compete on experience, not price |
| Feature comparison fails | Medium | Medium | Position as "simple" not "cheap" |

**Biggest risk:** Competing on price alone. Someone can always go cheaper.

**Mitigation:** Build brand around simplicity, personal support, and solopreneur focus. Price is a feature, but not the only feature.

---

### Testing recommendations

**Before launch:**
1. Survey 20 target users: "Would you pay $X for this?"
2. Test $12 vs $19 for Starter with landing page signups
3. Ask existing beta users what they'd pay

**After launch:**
1. Track trial-to-paid conversion by tier
2. Monitor churn by price point
3. A/B test pricing page layout after 100 signups

**Price increase path:**
- Year 1: $12/$29
- Year 2: Consider $15/$39 for new customers
- Grandfather existing customers for 12 months

---

### Final recommendation

**Launch with:**
- Starter: $12/month ($99/year)
- Pro: $29/month ($249/year)
- 14-day free trial on Pro
- No free tier

**Why:** Captures budget-conscious solopreneurs while leaving room for those who want more. Two tiers is simple to manage solo. Can always add or adjust later based on data.

**Next step:** Build pricing page and test with 10 potential customers before launch.
```

---

## Variations

### Course/info product pricing
```
Analyze pricing for [COURSE/EBOOK].

Consider:
- Perceived value of information
- Competitor courses
- Audience price sensitivity
- Bundling opportunities
- Launch vs evergreen pricing
```

### Service pricing
```
Analyze pricing for [SERVICE].

Consider:
- Hourly vs project vs retainer
- Value delivered vs time spent
- Market rates for similar services
- Packaging and productization
- Scope creep protection
```

### Freemium analysis
```
Analyze whether [PRODUCT] should have a free tier.

Consider:
- Conversion rates (free to paid)
- Support costs
- Viral/referral potential
- Competitor free offerings
- Revenue impact

Output: Freemium recommendation with specific free tier limits
```

---

## Quality checklist

- [ ] Competitor pricing documented
- [ ] Value-based calculation included
- [ ] Specific price recommendation given
- [ ] Pricing structure justified
- [ ] Revenue math shown
- [ ] Risks identified
- [ ] Testing plan included
- [ ] Would this help someone set a price?
