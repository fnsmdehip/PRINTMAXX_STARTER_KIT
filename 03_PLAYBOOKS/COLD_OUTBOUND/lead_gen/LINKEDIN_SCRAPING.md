# LinkedIn Sales Navigator tactics

Sales Navigator is the gold standard for finding B2B leads. Here's how to use it without getting banned.

## Sales Navigator vs Free LinkedIn

| Feature | Free LinkedIn | Sales Navigator |
|---------|--------------|-----------------|
| Search results | 100/search | 2,500/search |
| Filters | Basic | 30+ advanced |
| InMail | 0 | 50/month |
| Saved leads | 0 | 10,000 |
| Lead alerts | No | Yes |
| CRM sync | No | Yes |
| Price | $0 | $99/month |

**Worth it?** If cold outbound is a core channel, yes. The filters alone save hours.

## Sales Navigator pricing

- Core: $99/month (billed annually) or $149/month (monthly)
- Advanced: $149/month (team features)
- Advanced Plus: $1,600/year (CRM integrations)

**Tip:** Get annual for 30% savings. Or: Start with monthly to test, switch to annual.

## Setting up your search

### Account filters (company level)

**Company size:**
- Self-employed: 1 person
- 1-10: Tiny, founder makes all decisions
- 11-50: Small, lean teams
- 51-200: Growing, has departments
- 201-500: Mid-market, multiple decision makers
- 500+: Enterprise, complex sales cycles

**Industry:** Pick 3-5 that match your ICP

**Geography:** Start local or US-focused for better response rates

**Growth filters:**
- Company headcount growth: Fast-growing companies have budget
- Department headcount growth: Growing marketing team? They need marketing help

### Lead filters (person level)

**Seniority:**
- Owner: Decision maker at small companies
- CXO: C-suite, final budget authority
- VP: Budget authority for their department
- Director: Strong influence, sometimes budget
- Manager: Lower success rate, but more accessible

**Function:**
- Match to who buys your thing
- Marketing function for marketing services
- IT function for tech products
- Operations for efficiency tools

**Title (keyword search):**
Use quotes for exact match:
- "VP of Marketing"
- "Director of Sales"
- "Head of Growth"

Boolean works:
- "VP Marketing" OR "Head of Marketing" OR "Marketing Director"

**Years in current position:**
- Less than 1 year: New to role, making changes, open to tools
- 1-2 years: Settled, looking to improve results

**Changed jobs in past 90 days:**
Gold filter. New leaders want to make impact. 2x response rates.

## Building your search

### Example: Agency selling to SaaS startups

**Account filters:**
- Company headcount: 11-50
- Industry: Computer Software, Internet
- Company headcount growth: 10%+ YoY
- Geography: United States

**Lead filters:**
- Seniority: CXO, VP, Director
- Function: Marketing
- Years in current position: Less than 1 year

**Result:** Recently hired marketing leaders at growing software startups.

### Example: Consultant selling to agencies

**Account filters:**
- Company headcount: 2-10
- Industry: Marketing and Advertising
- Geography: United States, United Kingdom

**Lead filters:**
- Title: "Founder" OR "CEO" OR "Owner" OR "Managing Director"
- Seniority: Owner, CXO

### Example: SaaS selling to ecommerce

**Account filters:**
- Company headcount: 51-200
- Industry: Retail, Consumer Goods
- Company headcount growth: 20%+ YoY

**Lead filters:**
- Function: Marketing, E-commerce
- Seniority: VP, Director
- Title: "Ecommerce" OR "Digital" OR "Growth"

## Extracting data (scraping)

### The rules

LinkedIn prohibits scraping. Getting caught = account banned. But everyone does it. Here's how to minimize risk:

**Safe practices:**
- Extract slowly (under 100 profiles/day)
- Use tools that mimic human behavior
- Don't run scraping 24/7
- Use dedicated LinkedIn account (not your main)
- Vary your activity patterns

**Risky practices:**
- High-volume automated scraping
- Using your main account
- Running overnight
- Extracting thousands per day

### Scraping tools

**Browser extensions (safest):**
- Dux-Soup: $14.99/month, automates visits and extracts
- Linked Helper: $15/month, full automation suite
- Evaboot: $29/month, exports Sales Nav searches directly

**Cloud tools (riskier):**
- PhantomBuster: $56/month, powerful but gets accounts banned
- Captain Data: $399/month, enterprise grade
- Apify: Pay per run, very flexible

**My recommendation:** Evaboot for Sales Navigator exports. Clean data, reasonable risk.

### Evaboot workflow

1. Build your Sales Navigator search
2. Install Evaboot Chrome extension
3. Click "Export"
4. Evaboot extracts name, title, company, LinkedIn URL
5. Enriches with email (additional cost)
6. Downloads CSV

**Limits:** 2,500 leads per search (Sales Nav limit). Run multiple searches for more.

### Manual extraction (zero risk)

If you're paranoid about bans:

1. Run Sales Navigator search
2. Open each profile manually
3. Copy to spreadsheet: Name, title, company, LinkedIn URL
4. Find emails separately (Hunter, Apollo, Snov.io)

**Speed:** ~30-40 leads/hour. Fine for low-volume campaigns.

## Lead enrichment

You have names and LinkedIn URLs. Now you need emails.

### Apollo method (recommended)
1. Export from Sales Nav with company name + person name
2. Upload to Apollo as "People Search"
3. Apollo matches and provides emails
4. Export enriched list

### Hunter.io method
1. Upload CSV with first name, last name, company domain
2. Hunter finds email pattern and verifies
3. $49/month for 500 searches

### Dropcontact method
1. Upload CSV to Dropcontact
2. Returns verified emails
3. GDPR compliant
4. $24/month for 1,000 enrichments

## Avoiding LinkedIn bans

### The ban types

**Soft ban (restriction):**
- Can't connect or message for 24-72 hours
- Usually for too many connection requests
- Recoverable

**Hard ban (suspension):**
- Account locked
- Usually for scraping or automation detection
- May require ID verification
- Sometimes permanent

### Prevention tactics

1. **Warm up new accounts** - Don't scrape day 1. Use normally for 2 weeks first.
2. **Stay under limits** - Under 100 connection requests/week, under 100 profile views/day
3. **Vary behavior** - Don't be a robot. Like posts, comment, be human.
4. **Use dedicated accounts** - Scraping account separate from networking account
5. **Quality over quantity** - 50 great leads beats 500 garbage ones

### If you get banned

1. Appeal immediately (sometimes works)
2. Don't create new account from same IP/device
3. If making new account: new email, new phone, new IP, wait 30 days

## Sales Navigator workflow

### Weekly process

**Monday:**
1. Review saved searches for new leads
2. Save new leads to lists
3. Export 200-300 via Evaboot

**Tuesday:**
1. Enrich with emails (Apollo/Hunter)
2. Verify emails (ZeroBounce)
3. Clean and dedupe

**Wednesday:**
1. Import to email tool
2. Assign to sequences
3. Send connection requests on LinkedIn (20-30)

**Thursday-Friday:**
1. Monitor email responses
2. Accept connections
3. Send LinkedIn messages to new connections
4. Book calls

### Saved searches

Create saved searches for your ICP. Sales Navigator alerts you when new people match.

**Suggested saves:**
1. Core ICP (your main target)
2. Recent job changers in ICP
3. Companies that raised funding
4. Decision makers at competitor customers

## Integration with cold email

**Multi-channel sequence:**
1. Day 1: Cold email #1
2. Day 2: LinkedIn connection request (if email opened)
3. Day 3: Cold email #2
4. Day 5: LinkedIn message (if connected)
5. Day 7: Cold email #3

**Why this works:**
- Multiple touchpoints increase awareness
- LinkedIn humanizes you (they can see your face/profile)
- Some people respond better to LinkedIn than email
- Shows persistence without being annoying

## Quick start checklist

- [ ] Get Sales Navigator (start with monthly trial)
- [ ] Build first search matching your ICP
- [ ] Install Evaboot extension
- [ ] Export 100 test leads
- [ ] Enrich with emails via Apollo
- [ ] Verify emails
- [ ] Add to email campaign
- [ ] Send LinkedIn connections in parallel
- [ ] Track which channel gets responses
