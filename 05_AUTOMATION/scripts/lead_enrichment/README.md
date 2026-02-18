# Lead Enrichment Script

Takes a CSV of company names or domains, enriches using free APIs, and outputs contact data ready for cold outbound.

## Setup

Set API keys as environment variables:

```bash
export HUNTER_API_KEY="your_key"     # 50 free requests/month
export APOLLO_API_KEY="your_key"     # Free tier available
export CLEARBIT_API_KEY="your_key"   # Free tier (may be deprecated)
```

## Usage

```bash
# Enrich from CSV (uses all available APIs)
python3 enrich_leads.py sample_input.csv

# Specify output file
python3 enrich_leads.py leads.csv --output enriched_leads.csv

# Use specific API only
python3 enrich_leads.py leads.csv --api hunter

# Adjust rate limiting (seconds between requests)
python3 enrich_leads.py leads.csv --rate-limit 3

# Dry run (see what would be processed)
python3 enrich_leads.py leads.csv --dry-run
```

## Input CSV Format

Accepts any CSV with columns named: `company`, `company_name`, `domain`, `url`, `website`, `name`, or `organization`.

```csv
company_name,domain
Acme Corp,acme.com
TechStartup Inc,techstartup.io
```

## Output Columns

| Column | Description |
|--------|-------------|
| company_name | Company name |
| domain | Company domain |
| industry | Company industry/vertical |
| company_size | Employee count or range |
| decision_maker_name | Contact name (C-level/VP/Director prioritized) |
| decision_maker_email | Contact email |
| decision_maker_title | Contact job title |
| linkedin_url | Contact LinkedIn URL |
| source | Which API(s) provided data |
| enriched_at | Timestamp of enrichment |

## Free API Tiers

| API | Free Limit | Best For |
|-----|-----------|----------|
| Hunter.io | 25 searches/month | Email finding, domain search |
| Apollo.io | 50 credits/month | People search, org data |
| Clearbit | Limited free tier | Company enrichment |

## Demo Mode

If no API keys are set, runs in demo mode - outputs domain-normalized CSV with company names only. Useful for testing the pipeline.

## Dependencies

None (stdlib only).
