# Apollo.io guide for cold outbound

Apollo is the best B2B lead database for the price. 275M+ contacts. Here's how to use it effectively.

## Pricing

| Plan | Price | Credits/month | Best for |
|------|-------|---------------|----------|
| Free | $0 | 10,000 | Testing |
| Basic | $49/month | 900 | Small campaigns |
| Professional | $79/month | 1,200 | Regular outbound |
| Organization | $119/month | 2,400 | High volume |

**Credits work like this:**
- 1 credit = 1 email reveal
- 1 credit = 1 phone reveal (mobile)
- 0.5 credits = 1 email on free plan
- Export uses credits

**Hack:** Email-only exports on free plan get you 10,000 leads/month at $0.

## Setting up your ICP (Ideal Customer Profile)

Before searching, define who you're looking for:

**Company level:**
- Industry (SIC codes or keywords)
- Company size (employees)
- Revenue range
- Technologies used
- Location
- Funding stage (if targeting startups)

**Person level:**
- Job titles (multiple variations)
- Seniority level
- Department
- Time in role

## Search filters that work

### Finding decision makers

**For SMB (1-50 employees):**
- Titles: CEO, Founder, Owner, President
- These people make buying decisions directly

**For Mid-market (50-500 employees):**
- Titles: VP of [Department], Director of [Department], Head of [Department]
- Department matches your solution

**For Enterprise (500+):**
- Titles: Manager, Senior Manager, Director
- Note: Harder to cold email, expect lower reply rates

### Example searches

**Agency selling to SaaS companies:**
```
Industry: Computer Software, Internet
Employees: 11-50
Technologies: HubSpot (they're marketing-focused)
Titles: CEO, Founder, Head of Marketing, VP Marketing
Location: United States
Funding: Seed, Series A
```

**Consultant selling to agencies:**
```
Industry: Marketing and Advertising, Advertising
Employees: 5-25
Titles: Owner, Founder, Managing Director, CEO
Location: United States, United Kingdom
```

**SaaS selling to ecommerce:**
```
Industry: Retail, Consumer Goods
Technologies: Shopify, WooCommerce, Magento
Employees: 11-200
Titles: Ecommerce Manager, Digital Marketing Director, CMO
```

## Advanced filters

### Technology filter
Find companies using specific tools. Great for:
- Selling to people using competitor products
- Finding companies with specific tech stacks
- "They use X, they probably need Y"

**Examples:**
- Using Mailchimp? Might need email deliverability help
- Using WordPress? Might need development
- Using Salesforce? Probably have budget

### Hiring signals
Companies hiring for specific roles = growth indicator.

**Filter:** Job Postings > Contains > [keyword]

**Examples:**
- Hiring "SDR" = growing sales team = might need sales tools
- Hiring "Developer" = building product = might need dev services
- Hiring "Marketing Manager" = investing in marketing

### Funding signals
Recently funded companies have money to spend.

**Filter:** Funding > Recent Funding Date > Last 12 months

**Combine with:** Funding Amount > $1M+

### News and intent signals (Professional plan+)
- Recent news mentions
- Website visitor intent
- Job change alerts

## Exporting leads

### Best practices
1. Export in batches of 100-500 (easier to manage)
2. Always include: First Name, Last Name, Email, Company, Title
3. Verify emails before sending (even Apollo has ~95% accuracy)
4. Export to CSV, not directly to CRM

### Export fields to include
- First name
- Last name
- Email
- Company name
- Title
- LinkedIn URL
- Company website
- Employee count
- Industry
- Location

### Cleaning your export
1. Remove rows with no email
2. Remove duplicates (same person, multiple roles)
3. Remove catch-all domains (they'll bounce)
4. Verify with ZeroBounce or NeverBounce
5. Remove role-based emails (info@, sales@, etc.)

## Sequences in Apollo

Apollo has built-in email sending. Pros and cons:

**Pros:**
- All in one place
- Cheaper than separate tool
- Decent analytics

**Cons:**
- No inbox warmup
- Limited sending accounts
- Deliverability not as good as dedicated tools

**My recommendation:** Use Apollo for lead finding, export to Instantly for sending.

## Apollo hacks

### Saved searches
Save your ICP searches. Apollo updates them with new contacts weekly.

### Boolean search
For company names: `"Marketing Agency" OR "Digital Agency" OR "Ad Agency"`
For titles: `"CEO" OR "Founder" OR "Owner"`

### Exclude competitors
Add your competitors to an exclusion list. Don't waste credits emailing them.

### List management
Create lists by:
- Campaign
- Industry vertical
- Outreach stage
- Response status

### Contact enrichment
Have a list of company names? Upload to Apollo, it'll find contacts at those companies.

## Verification step (important)

Apollo emails are ~92-95% accurate. That means 5-8% bounces, which kills deliverability.

**Always verify before sending:**

| Tool | Price | Speed |
|------|-------|-------|
| ZeroBounce | $0.008/email | Fast |
| NeverBounce | $0.008/email | Fast |
| Bouncer | $0.006/email | Medium |
| MillionVerifier | $0.0003/email | Slower, bulk only |

**Target:** Under 3% bounce rate after verification.

## Building a lead pipeline

### Weekly process
1. Monday: Run saved searches, export new leads
2. Tuesday: Verify emails, clean list
3. Wednesday: Import to email tool, assign to campaigns
4. Thursday-Friday: Monitor responses
5. Repeat

### Volume math
- 1,000 verified leads/week
- 5% reply rate = 50 replies
- 20% of replies interested = 10 opportunities
- 20% close rate = 2 customers/week

**To hit these numbers:**
- Apollo Professional ($79/mo) gives 1,200 credits
- Verification costs ~$10 for 1,200 emails
- Total: ~$90/month for 1,200 leads/month

## Common mistakes

1. **Too broad searches** - "CEO, any industry, any size" = garbage list
2. **Not verifying** - 8% bounce rate tanks your domains
3. **Exporting everything** - Be selective, quality over quantity
4. **Ignoring company data** - Person might be right, company might be wrong
5. **One-time export** - Build ongoing pipeline, not one-shot lists

## Alternatives to Apollo

| Tool | Best for | Price |
|------|----------|-------|
| ZoomInfo | Enterprise, max data | $15K+/year |
| Cognism | EU data, GDPR compliant | $1K+/month |
| Lusha | Quick lookups | $36/month |
| RocketReach | Individual lookups | $39/month |
| Hunter.io | Email finding only | $49/month |

Apollo wins on price-to-features for most solopreneurs.

## Quick start checklist

- [ ] Sign up for Apollo (free plan to start)
- [ ] Define your ICP in writing before searching
- [ ] Build first search with tight filters
- [ ] Export 100 test leads
- [ ] Verify with ZeroBounce/NeverBounce
- [ ] Review data quality manually
- [ ] Iterate filters based on quality
- [ ] Export at scale once quality is good
