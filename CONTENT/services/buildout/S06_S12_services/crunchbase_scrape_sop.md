# Crunchbase Scrape SOP — Lead Intelligence for Cold Outbound

## What This Gets You

Crunchbase has 80M+ companies. The free tier is useless for bulk work. The real play is combining
Crunchbase signal data (funding rounds, headcount, tech stack) with direct contact enrichment.
Goal: build targeted prospect lists of companies that just raised money, are hiring, or expanded.
These signals = budget exists + pain = highest-intent cold outbound targets.

---

## Tool Stack

| Tool | Cost | What It Does |
|------|------|-------------|
| Crunchbase Pro | $49/mo | Advanced search, CSV export, org enrichment |
| Apollo.io | $49/mo (Basic) | Contact enrichment + verified emails |
| Clay | $149/mo (Starter) | Enrichment waterfall, AI research, 10K credits/mo |
| Wappalyzer | Free / $249/mo Pro | Tech stack detection by domain |
| Hunter.io | $49/mo (Starter) | Email finder + verify, 500 finds/mo |
| PhantomBuster | $56/mo | LinkedIn scraping + automation |

**Minimum viable stack (under $100/mo):** Crunchbase Pro $49 + Apollo Basic $49
**Power stack:** Clay $149 + Crunchbase Pro $49 = $198/mo (handles 10K leads/mo end-to-end)

---

## Target Signals (Priority Order)

### Signal 1: Recently Funded Companies (HIGHEST PRIORITY)
- Series A / Series B raises in last 90 days
- Why: they have fresh capital, hiring aggressively, buying new tools
- Crunchbase filter: Funding Date = last 90 days + Funding Type = Series A/B
- Lead profile: Head of Marketing, VP Growth, CMO

### Signal 2: Hiring for Growth Roles
- Job postings for: "Growth Manager," "Head of Marketing," "Content Marketing," "SEO Manager"
- Why: they're scaling revenue ops, budget unlocked
- Crunchbase + LinkedIn Jobs combo
- Lead profile: the hiring manager above that role (usually CMO or VP Marketing)

### Signal 3: Headcount Growth 20%+ YoY
- Crunchbase Pro shows employee growth percentage
- Companies growing fast = budget growing fast
- Filter: 20-500 employees (too small = no budget, too big = long sales cycle)

### Signal 4: Tech Stack Triggers
- Running Hubspot or Salesforce but no cold email tool = warm intro to cold email setup service
- Running Webflow but no analytics tool = analytics audit play
- Running Intercom but no structured onboarding = onboarding audit play
- Use Wappalyzer to detect stack, then pitch the gap

---

## Step-by-Step Workflow

### Step 1: Build Target Segment (30 min/week)

1. Open Crunchbase Pro → Organizations → Advanced Search
2. Set filters:
   - Funding Date: last 90 days
   - Funding Type: Series A (or Series B for higher-budget)
   - Employee Count: 10-200
   - Location: US (or expand to UK/Canada/AUS for less competition)
   - Industries: SaaS, eCommerce, Fintech, HealthTech (adjust per service offering)
3. Sort by Funding Date (newest first)
4. Export CSV: max 1,000 rows per export
5. Save to `AUTOMATIONS/leads/crunchbase_raw_{YYYY-MM-DD}.csv`

### Step 2: Enrich With Decision-Maker Contacts (Apollo)

1. Import Crunchbase CSV into Apollo.io → Lists → Import
2. Apollo auto-matches domain to people records
3. Filter by Title: "Chief Marketing Officer" OR "VP Marketing" OR "Head of Growth" OR "Director of Marketing"
4. Export enriched CSV with: name, title, email, LinkedIn URL, company name, website
5. Verify emails: Apollo has built-in verify, run all before using
6. Target: 80%+ email verification rate. Discard unverified.

**Alternative if Apollo is over budget:** Use Hunter.io Domain Search for top 50 companies manually. Takes longer but free tier gives 25 finds/mo.

### Step 3: Tech Stack Overlay (Wappalyzer)

```python
# Batch tech stack detection — run this on your domain list
import requests
import csv
import time

WAPPALYZER_API_KEY = "your_key_here"  # Get from wappalyzer.com/api

def get_tech_stack(domain):
    url = f"https://api.wappalyzer.com/v2/lookup/?urls=https://{domain}"
    headers = {"x-api-key": WAPPALYZER_API_KEY}
    resp = requests.get(url, headers=headers)
    if resp.status_code == 200:
        data = resp.json()
        if data:
            techs = [t['name'] for t in data[0].get('technologies', [])]
            return techs
    return []

with open('leads_enriched.csv', 'r') as f_in, open('leads_with_stack.csv', 'w', newline='') as f_out:
    reader = csv.DictReader(f_in)
    fields = reader.fieldnames + ['tech_stack', 'stack_gaps']
    writer = csv.DictWriter(f_out, fieldnames=fields)
    writer.writeheader()

    for row in reader:
        domain = row.get('website', '').replace('https://', '').replace('http://', '').rstrip('/')
        stack = get_tech_stack(domain)

        # Detect gaps for pitching
        gaps = []
        if 'HubSpot' in stack and not any(x in stack for x in ['Lemlist', 'Instantly', 'Outreach']):
            gaps.append('no_cold_email_tool')
        if 'Google Analytics' not in stack and 'Segment' not in stack:
            gaps.append('no_analytics')
        if 'Intercom' in stack and 'Calendly' not in stack:
            gaps.append('no_scheduling')

        row['tech_stack'] = ', '.join(stack)
        row['stack_gaps'] = ', '.join(gaps) if gaps else 'none'
        writer.writerow(row)
        time.sleep(0.5)  # Rate limit: 2 req/sec on free tier
```

### Step 4: Score and Prioritize (Lead Scoring Matrix)

| Signal | Points |
|--------|--------|
| Funded in last 30 days | +20 |
| Funded in last 90 days | +10 |
| Headcount 20%+ growth | +15 |
| Series A ($2-10M) | +10 |
| Series B ($10-30M) | +20 |
| Has tech stack gap matching our service | +25 |
| 10-50 employees | +10 |
| 51-200 employees | +5 |
| Email verified | +10 |
| LinkedIn profile found | +5 |

**Priority tiers:**
- Tier 1 (70+ points): Contact same day
- Tier 2 (50-69 points): Contact within 48 hours
- Tier 3 (30-49 points): Contact within 1 week
- Below 30: Skip or batch for generic sequence

### Step 5: Load Into Cold Email Campaign

1. Export Tier 1 + Tier 2 to Instantly.ai (or Lemlist)
2. Segment by signal type (funded vs. hiring vs. tech gap)
3. Match copy to signal — funded companies get "congrats on the raise" opener
4. Load sequence (see cold_email_agency_sop.md for full sequences)
5. Launch with 20-50 emails/day per inbox

---

## Output Format (Standard Lead CSV)

Required columns for downstream tools:
```
first_name, last_name, email, email_verified, title, company, domain,
linkedin_url, funding_round, funding_date, headcount, tech_stack,
stack_gaps, lead_score, priority_tier, date_added
```

---

## Volume Targets

| Effort Level | Leads/Week | Emails Sent/Week | Expected Replies/Week |
|-------------|------------|-------------------|----------------------|
| Minimum (2 hrs/week) | 100 | 100 | 2-5 |
| Standard (5 hrs/week) | 500 | 500 | 10-25 |
| Aggressive (10 hrs/week) | 2,000 | 2,000 | 40-100 |
| With Clay automation | 5,000+ | 5,000+ | 100-250 |

At 2% reply rate + 25% meeting book rate = 1 meeting per 200 emails.
At 25% close rate + $1,500 avg deal: 200 emails = $1.50 expected revenue/email.
Scale to 1,000/day = $1,500/day expected. This math is why you do this.

---

## Compliance

- CAN-SPAM: include unsubscribe + physical address in every email
- GDPR: B2B emails with legitimate interest basis — must be work email, professional context
- LinkedIn scraping: use PhantomBuster with human-like delays, 100 actions/day max
- Crunchbase TOS: no automated scraping of web UI — use their official API or CSV export only
- Apollo/Hunter data: used for prospecting only, delete leads who opt out within 10 business days

---

## Weekly Operations Calendar

| Day | Task | Time |
|-----|------|------|
| Monday | Pull new Crunchbase leads (funding + hiring signals) | 30 min |
| Tuesday | Enrich with Apollo, verify emails | 30 min |
| Wednesday | Tech stack overlay (Wappalyzer), score leads | 30 min |
| Thursday | Load into Instantly, review copy, launch sequences | 30 min |
| Friday | Review replies, book meetings, update CRM | 30 min |
| Total | | 2.5 hrs/week |
