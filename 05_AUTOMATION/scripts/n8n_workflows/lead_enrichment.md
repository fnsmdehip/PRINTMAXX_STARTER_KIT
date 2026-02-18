# Lead Enrichment Workflow

**Purpose:** Take CSV of company names, enrich with Apollo/Hunter, score leads, route to appropriate outreach sequence.

**Workflow ID:** `lead_enrichment_v1`
**Trigger:** Webhook (on CSV upload) or manual
**Est. Run Time:** 1-3 seconds per lead

---

## Architecture Overview

```
CSV Upload (company names)
          |
          v
Parse CSV to Array
          |
          v
Split into Batches (50/batch)
          |
          v
Apollo: Company Enrichment
          |
          v
Apollo: Find Decision Makers
          |
          v
Hunter: Verify Emails
          |
          v
Lead Scoring (rules-based)
          |
          v
Route by Score:
  - HOT (80+)  -> Immediate outreach
  - WARM (50-79) -> Nurture sequence
  - COLD (<50) -> Archive/skip
          |
          v
Save to LEDGER/OUTREACH_PIPELINE.csv
```

---

## Node Configuration

### Node 1: Webhook Trigger
**Type:** `n8n-nodes-base.webhook`
**Purpose:** Receive CSV file or company list

```json
{
  "path": "lead-enrichment",
  "httpMethod": "POST",
  "responseMode": "lastNode",
  "options": {
    "rawBody": true
  }
}
```

**Webhook URL:** `https://your-n8n.com/webhook/lead-enrichment`

**Expected Input:**
```json
{
  "companies": [
    {"name": "Acme Corp", "domain": "acme.com"},
    {"name": "Beta Inc", "domain": "beta.io"}
  ]
}
```

Or CSV body:
```
company_name,domain
Acme Corp,acme.com
Beta Inc,beta.io
```

---

### Node 2: Parse Input
**Type:** `n8n-nodes-base.code`
**Purpose:** Normalize input from JSON or CSV

```javascript
const input = $input.first().json;
let companies = [];

// Check if JSON array
if (input.companies && Array.isArray(input.companies)) {
  companies = input.companies;
}
// Check if raw CSV body
else if (input.body && typeof input.body === 'string') {
  const lines = input.body.trim().split('\n');
  const headers = lines[0].split(',').map(h => h.trim());

  for (let i = 1; i < lines.length; i++) {
    const values = lines[i].split(',');
    const company = {};
    headers.forEach((h, idx) => {
      company[h] = values[idx]?.trim() || '';
    });
    companies.push({
      name: company.company_name || company.name,
      domain: company.domain || company.website
    });
  }
}

// Filter valid entries
companies = companies.filter(c => c.name && c.domain);

return companies.map(c => ({json: c}));
```

---

### Node 3: Split into Batches
**Type:** `n8n-nodes-base.splitInBatches`
**Purpose:** Process 50 leads at a time (API rate limits)

```json
{
  "batchSize": 50,
  "options": {}
}
```

---

### Node 4: Apollo - Company Enrichment
**Type:** `n8n-nodes-base.httpRequest`
**Purpose:** Get company info (industry, size, funding)

```json
{
  "method": "POST",
  "url": "https://api.apollo.io/v1/organizations/enrich",
  "authentication": "predefinedCredentialType",
  "nodeCredentialType": "apolloApi",
  "sendHeaders": true,
  "headerParameters": {
    "parameters": [
      {"name": "Content-Type", "value": "application/json"},
      {"name": "Cache-Control", "value": "no-cache"}
    ]
  },
  "sendBody": true,
  "specifyBody": "json",
  "jsonBody": "={ \"api_key\": \"{{ $env.APOLLO_API_KEY }}\", \"domain\": \"{{ $json.domain }}\" }"
}
```

**Response Fields Used:**
- `organization.name`
- `organization.estimated_num_employees`
- `organization.industry`
- `organization.founded_year`
- `organization.annual_revenue`
- `organization.linkedin_url`
- `organization.technologies` (tech stack)

---

### Node 5: Apollo - Find Decision Makers
**Type:** `n8n-nodes-base.httpRequest`
**Purpose:** Find relevant contacts (CEO, CTO, VP Marketing, etc.)

```json
{
  "method": "POST",
  "url": "https://api.apollo.io/v1/mixed_people/search",
  "sendBody": true,
  "specifyBody": "json",
  "jsonBody": "={ \"api_key\": \"{{ $env.APOLLO_API_KEY }}\", \"q_organization_domains\": \"{{ $json.domain }}\", \"person_titles\": [\"CEO\", \"CTO\", \"Founder\", \"VP Marketing\", \"Head of Growth\", \"Director of Marketing\"], \"per_page\": 5 }"
}
```

**Response Fields Used:**
- `people[].first_name`
- `people[].last_name`
- `people[].title`
- `people[].email`
- `people[].linkedin_url`

---

### Node 6: Hunter - Verify Emails
**Type:** `n8n-nodes-base.httpRequest`
**Purpose:** Verify email deliverability

```json
{
  "method": "GET",
  "url": "https://api.hunter.io/v2/email-verifier",
  "authentication": "predefinedCredentialType",
  "nodeCredentialType": "hunterApi",
  "qs": {
    "email": "={{ $json.email }}",
    "api_key": "{{ $env.HUNTER_API_KEY }}"
  }
}
```

**Response Fields Used:**
- `data.status` (valid, invalid, accept_all, unknown)
- `data.score` (0-100)
- `data.deliverable` (boolean)

**Logic:**
- `status: valid` -> Proceed
- `status: invalid` -> Skip contact
- `status: accept_all` -> Flag for caution
- `status: unknown` -> Include but mark

---

### Node 7: Merge Enrichment Data
**Type:** `n8n-nodes-base.code`
**Purpose:** Combine company + contact + verification data

```javascript
const company = $('Apollo - Company Enrichment').first().json;
const contacts = $('Apollo - Find Decision Makers').first().json.people || [];
const verifications = $('Hunter - Verify Emails').all().map(n => n.json);

// Map verifications to contacts
const enrichedContacts = contacts.map((contact, idx) => {
  const verification = verifications[idx]?.data || {};
  return {
    first_name: contact.first_name,
    last_name: contact.last_name,
    email: contact.email,
    title: contact.title,
    linkedin_url: contact.linkedin_url,
    email_status: verification.status || 'unknown',
    email_score: verification.score || 0,
    deliverable: verification.deliverable || false
  };
}).filter(c => c.email_status !== 'invalid');

return [{
  json: {
    company: {
      name: company.organization?.name || $('Parse Input').first().json.name,
      domain: company.organization?.primary_domain || $('Parse Input').first().json.domain,
      industry: company.organization?.industry || 'Unknown',
      employee_count: company.organization?.estimated_num_employees || 0,
      annual_revenue: company.organization?.annual_revenue || null,
      founded_year: company.organization?.founded_year || null,
      linkedin_url: company.organization?.linkedin_url || null,
      technologies: company.organization?.technologies || []
    },
    contacts: enrichedContacts,
    enriched_at: new Date().toISOString()
  }
}];
```

---

### Node 8: Lead Scoring
**Type:** `n8n-nodes-base.code`
**Purpose:** Score leads based on ICP fit

```javascript
const data = $input.first().json;
const company = data.company;
const contacts = data.contacts;

let score = 0;
const scoreBreakdown = [];

// Company Size Scoring (adjust for your ICP)
const employees = company.employee_count;
if (employees >= 10 && employees <= 50) {
  score += 25;
  scoreBreakdown.push('Company size 10-50: +25');
} else if (employees >= 51 && employees <= 200) {
  score += 20;
  scoreBreakdown.push('Company size 51-200: +20');
} else if (employees >= 201 && employees <= 500) {
  score += 15;
  scoreBreakdown.push('Company size 201-500: +15');
} else if (employees > 500) {
  score += 5;
  scoreBreakdown.push('Enterprise (500+): +5');
}

// Industry Scoring (adjust for your niche)
const targetIndustries = ['saas', 'software', 'technology', 'marketing', 'e-commerce', 'fintech'];
const industry = (company.industry || '').toLowerCase();
if (targetIndustries.some(t => industry.includes(t))) {
  score += 20;
  scoreBreakdown.push(`Target industry (${company.industry}): +20`);
}

// Tech Stack Scoring
const techSignals = ['hubspot', 'salesforce', 'intercom', 'stripe', 'shopify', 'zapier'];
const techs = (company.technologies || []).map(t => t.toLowerCase());
const matchedTech = techSignals.filter(t => techs.some(tech => tech.includes(t)));
if (matchedTech.length > 0) {
  score += matchedTech.length * 5;
  scoreBreakdown.push(`Tech signals (${matchedTech.join(', ')}): +${matchedTech.length * 5}`);
}

// Contact Quality Scoring
const hasDecisionMaker = contacts.some(c =>
  /ceo|founder|cto|vp|director|head/i.test(c.title)
);
if (hasDecisionMaker) {
  score += 15;
  scoreBreakdown.push('Has decision maker: +15');
}

// Email Deliverability Scoring
const verifiedEmails = contacts.filter(c => c.email_status === 'valid').length;
if (verifiedEmails >= 2) {
  score += 15;
  scoreBreakdown.push(`${verifiedEmails} verified emails: +15`);
} else if (verifiedEmails === 1) {
  score += 10;
  scoreBreakdown.push('1 verified email: +10');
}

// Determine tier
let tier;
if (score >= 80) {
  tier = 'HOT';
} else if (score >= 50) {
  tier = 'WARM';
} else {
  tier = 'COLD';
}

return [{
  json: {
    ...data,
    lead_score: score,
    lead_tier: tier,
    score_breakdown: scoreBreakdown
  }
}];
```

---

### Node 9: Route by Score
**Type:** `n8n-nodes-base.switch`
**Purpose:** Different paths based on lead tier

```json
{
  "rules": {
    "rules": [
      {
        "outputKey": "HOT",
        "conditions": {
          "conditions": [
            {
              "leftValue": "={{ $json.lead_tier }}",
              "rightValue": "HOT",
              "operator": "equals"
            }
          ]
        }
      },
      {
        "outputKey": "WARM",
        "conditions": {
          "conditions": [
            {
              "leftValue": "={{ $json.lead_tier }}",
              "rightValue": "WARM",
              "operator": "equals"
            }
          ]
        }
      },
      {
        "outputKey": "COLD",
        "conditions": {
          "conditions": [
            {
              "leftValue": "={{ $json.lead_tier }}",
              "rightValue": "COLD",
              "operator": "equals"
            }
          ]
        }
      }
    ]
  }
}
```

---

### Node 10a: HOT Leads - Immediate Outreach
**Type:** `n8n-nodes-base.googleSheets`
**Purpose:** Add to high-priority outreach queue

```json
{
  "operation": "append",
  "documentId": "{{ $env.LEDGER_SHEET_ID }}",
  "sheetName": "OUTREACH_PIPELINE",
  "columns": {
    "mappingMode": "defineBelow",
    "value": {
      "company_name": "={{ $json.company.name }}",
      "domain": "={{ $json.company.domain }}",
      "industry": "={{ $json.company.industry }}",
      "employee_count": "={{ $json.company.employee_count }}",
      "contact_name": "={{ $json.contacts[0].first_name }} {{ $json.contacts[0].last_name }}",
      "contact_email": "={{ $json.contacts[0].email }}",
      "contact_title": "={{ $json.contacts[0].title }}",
      "lead_score": "={{ $json.lead_score }}",
      "lead_tier": "HOT",
      "score_breakdown": "={{ $json.score_breakdown.join('; ') }}",
      "sequence": "IMMEDIATE_OUTREACH",
      "status": "QUEUED",
      "enriched_at": "={{ $json.enriched_at }}"
    }
  }
}
```

---

### Node 10b: WARM Leads - Nurture Sequence
**Type:** `n8n-nodes-base.googleSheets`
**Purpose:** Add to nurture campaign

```json
{
  "operation": "append",
  "documentId": "{{ $env.LEDGER_SHEET_ID }}",
  "sheetName": "OUTREACH_PIPELINE",
  "columns": {
    "value": {
      "sequence": "NURTURE_SEQUENCE",
      "status": "QUEUED"
    }
  }
}
```

---

### Node 10c: COLD Leads - Archive
**Type:** `n8n-nodes-base.googleSheets`
**Purpose:** Log but don't outreach

```json
{
  "operation": "append",
  "documentId": "{{ $env.LEDGER_SHEET_ID }}",
  "sheetName": "OUTREACH_ARCHIVE",
  "columns": {
    "value": {
      "sequence": "ARCHIVED",
      "status": "COLD_SKIP",
      "archive_reason": "Below threshold"
    }
  }
}
```

---

### Node 11: Human Review Checkpoint (HOT only)
**Type:** `n8n-nodes-base.slack`
**Purpose:** Alert for HOT leads before outreach

```json
{
  "channel": "#hot-leads",
  "text": "HOT LEAD (Score: {{ $json.lead_score }})\n\nCompany: {{ $json.company.name }}\nIndustry: {{ $json.company.industry }}\nSize: {{ $json.company.employee_count }} employees\n\nPrimary Contact: {{ $json.contacts[0].first_name }} {{ $json.contacts[0].last_name }}\nTitle: {{ $json.contacts[0].title }}\nEmail: {{ $json.contacts[0].email }}\n\nScore Breakdown:\n{{ $json.score_breakdown.join('\\n') }}\n\nApprove outreach? Reply with /approve or /skip"
}
```

---

## Required Credentials

| Credential | Purpose | Free Tier |
|------------|---------|-----------|
| `apolloApi` | Company + contact enrichment | 50 credits/month |
| `hunterApi` | Email verification | 25 verifications/month |
| `googleSheetsOAuth2Api` | Data storage | Unlimited |
| `slackApi` | Notifications | Free |

---

## Environment Variables

```bash
APOLLO_API_KEY=your_apollo_key
HUNTER_API_KEY=your_hunter_key
LEDGER_SHEET_ID=1abc...xyz
```

---

## Lead Scoring Customization

Adjust scoring weights in Node 8 based on your ICP:

```javascript
// Example: SaaS-focused scoring
const SCORING_WEIGHTS = {
  companySize: {
    '1-10': 5,      // Too small
    '11-50': 25,    // Sweet spot
    '51-200': 20,   // Good
    '201-500': 15,  // Larger deals
    '500+': 5       // Enterprise (different motion)
  },
  industries: {
    'saas': 25,
    'software': 20,
    'technology': 15,
    'marketing': 15,
    'e-commerce': 10
  },
  techSignals: {
    'stripe': 10,      // Has payment (monetizing)
    'hubspot': 8,      // Doing marketing
    'salesforce': 5,   // Might be enterprise
    'zapier': 10       // Automation-minded
  },
  titles: {
    'ceo': 20,
    'founder': 20,
    'cto': 15,
    'vp marketing': 15,
    'head of growth': 15
  }
};
```

---

## Error Handling

### Apollo API Errors
- **429 Rate Limited:** Wait 60s, retry batch
- **401 Unauthorized:** Check API key
- **404 Not Found:** Company doesn't exist, skip

### Hunter API Errors
- **422 Invalid Email:** Mark as unverified
- **429 Rate Limited:** Queue for next day

### General
- Log all errors to `ENRICHMENT_ERRORS` sheet
- Continue with partial data if possible
- Alert if >20% failure rate

---

## Cost Estimation

| Service | Credits/Lead | Monthly Cost (500 leads) |
|---------|--------------|--------------------------|
| Apollo | 1 credit | $99/mo (400 credits) |
| Hunter | 1 verification | $49/mo (500 verifications) |
| n8n | - | $20/mo (cloud) |
| **Total** | - | ~$170/mo |

**Cost Optimization:**
- Skip Hunter verification for accept-all domains
- Cache company data (don't re-enrich same domain)
- Batch requests during off-peak

---

## Testing Checklist

- [ ] CSV parsing handles different formats
- [ ] Apollo returns company data
- [ ] Apollo returns contacts with emails
- [ ] Hunter verifies emails correctly
- [ ] Lead scoring matches expected ICP
- [ ] HOT leads trigger Slack alert
- [ ] WARM leads go to nurture queue
- [ ] COLD leads archive correctly
- [ ] Duplicates are handled (same domain)
- [ ] Partial failures don't break workflow

---

## Usage Examples

**cURL Request:**
```bash
curl -X POST https://your-n8n.com/webhook/lead-enrichment \
  -H "Content-Type: application/json" \
  -d '{
    "companies": [
      {"name": "Acme SaaS", "domain": "acmesaas.com"},
      {"name": "Beta Tech", "domain": "betatech.io"}
    ]
  }'
```

**CSV Upload:**
```bash
curl -X POST https://your-n8n.com/webhook/lead-enrichment \
  -H "Content-Type: text/csv" \
  --data-binary @leads.csv
```
