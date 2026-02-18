# Automation Workflows Guide: n8n vs Make.com

**Purpose:** Comprehensive guide for choosing, setting up, and using automation platforms for PRINTMAXX operations.

**Last Updated:** 2026-01-25

---

## Executive Summary

**Bottom line:** Use n8n self-hosted for complex workflows (cost-effective at scale). Use Make.com for quick wins and non-technical users.

| Use Case | Best Choice | Why |
|----------|-------------|-----|
| High volume (10k+ ops/mo) | n8n self-hosted | Free after hosting costs |
| Quick setup, small scale | Make.com | Faster to deploy |
| Custom integrations | n8n | More flexible, code nodes |
| Budget under $50/mo | n8n on Railway | ~$5-10/mo vs $29/mo Make Pro |
| Complex AI workflows | n8n | Better Claude/OpenAI integration |
| Non-technical user | Make.com | Visual builder, less learning curve |

---

## n8n vs Make.com vs Zapier Comparison

### Feature Matrix

| Feature | n8n | Make.com | Zapier |
|---------|-----|----------|--------|
| **Pricing** | Free (self-hosted) | Free-$29/mo | $29-$99/mo |
| **Operations/mo** | Unlimited | 1K-10K | 750-2K |
| **Self-hosting** | Yes | No | No |
| **Code nodes** | Yes (JS, Python) | Limited | Limited |
| **AI integrations** | Native Claude/OpenAI | Via HTTP | Via HTTP |
| **Webhook triggers** | Yes | Yes | Yes |
| **Error handling** | Advanced | Good | Basic |
| **Branching/logic** | Advanced | Good | Basic |
| **Learning curve** | Medium | Low | Lowest |
| **Community** | Large, OSS | Growing | Largest |

### Pricing Deep Dive

**n8n Self-Hosted:**
```
Railway: $5-15/mo (depending on usage)
Hetzner VPS: $4-10/mo
Docker local: Free (your machine)
Supabase: Free tier + $25/mo database
---
Total: $5-25/mo for UNLIMITED operations
```

**Make.com:**
```
Free: 1,000 ops/mo (testing only)
Core: $9/mo (10,000 ops)
Pro: $16/mo (10,000 ops + priority)
Teams: $29/mo (10,000 ops + collaboration)
---
Most PRINTMAXX workflows: $16-29/mo
```

**Zapier:**
```
Free: 100 tasks/mo (useless)
Starter: $29/mo (750 tasks)
Professional: $99/mo (2,000 tasks)
---
Too expensive for our volume. Skip Zapier.
```

### Decision Framework

```
START
  |
  v
Volume > 5,000 ops/mo?
  |
  +-- YES --> Can self-host?
  |             |
  |             +-- YES --> n8n self-hosted
  |             |
  |             +-- NO --> Make.com Pro
  |
  +-- NO --> Need quick setup?
              |
              +-- YES --> Make.com
              |
              +-- NO --> n8n (more flexible long-term)
```

---

## n8n Deep Dive

### What is n8n?

Open-source workflow automation tool. Think Zapier, but you host it yourself and it's free. 400+ integrations, visual workflow builder, code nodes for custom logic.

### Self-Hosting Options

#### Option 1: Railway (Recommended)

**Best for:** Quick deployment, managed infrastructure, reasonable cost.

**Setup:**
```bash
# 1. Create Railway account (railway.app)
# 2. Deploy from template:
#    - Go to railway.app/template/n8n
#    - Click "Deploy Now"
#    - Set environment variables:
#      - N8N_ENCRYPTION_KEY: [generate random 32-char string]
#      - N8N_USER_MANAGEMENT_JWT_SECRET: [generate random]
#    - Deploy

# 3. Access at: https://your-app.railway.app
```

**Cost:** $5-15/mo depending on usage

**Pros:**
- One-click deploy
- Auto-scaling
- SSL included
- Easy updates

**Cons:**
- Slightly higher cost than VPS
- Less control than Docker

#### Option 2: Docker (Self-Managed)

**Best for:** Technical users, maximum control, lowest cost.

**Setup:**
```bash
# 1. On your server (Hetzner, DigitalOcean, etc.)

# 2. Create docker-compose.yml:
version: '3'
services:
  n8n:
    image: n8nio/n8n
    ports:
      - "5678:5678"
    environment:
      - N8N_HOST=your-domain.com
      - N8N_PORT=5678
      - N8N_PROTOCOL=https
      - NODE_ENV=production
      - WEBHOOK_URL=https://your-domain.com/
      - N8N_ENCRYPTION_KEY=your-secret-key
    volumes:
      - ./n8n-data:/home/node/.n8n
    restart: always

# 3. Run:
docker-compose up -d

# 4. Set up nginx reverse proxy + SSL
```

**Cost:** $4-10/mo (VPS cost only)

**Pros:**
- Cheapest option
- Full control
- Run alongside other services

**Cons:**
- More setup
- You manage updates/backups
- Need nginx/SSL knowledge

#### Option 3: n8n Cloud (Managed)

**Best for:** Teams who want zero maintenance.

**Pricing:**
- Starter: $20/mo (5 workflows, 2.5k executions)
- Pro: $50/mo (15 workflows, 10k executions)
- Enterprise: Custom

**When to use:** If you value time over money and don't want to manage infrastructure.

### n8n Core Concepts

**Nodes:** Individual steps in a workflow. Types:
- **Trigger:** Starts workflow (webhook, schedule, RSS, etc.)
- **Action:** Does something (HTTP request, database, API call)
- **Logic:** Controls flow (IF, Switch, Merge, Loop)
- **Code:** Custom JavaScript/Python

**Credentials:** Stored API keys/OAuth tokens for services.

**Workflows:** Connected series of nodes from trigger to action(s).

**Executions:** Each time a workflow runs.

### Essential n8n Nodes for PRINTMAXX

| Node | Purpose | Use Case |
|------|---------|----------|
| **HTTP Request** | API calls | Claude API, social APIs, webhooks |
| **Code** | Custom logic | Data transformation, AI processing |
| **RSS Feed** | Monitor feeds | New blog posts, podcast episodes |
| **Google Sheets** | Data storage | Lead tracking, content queue |
| **Webhook** | Receive data | Form submissions, external triggers |
| **Schedule** | Time-based | Daily research, scheduled posts |
| **IF** | Branching | Content type routing |
| **Merge** | Combine data | Multiple API responses |
| **Wait** | Delays | Rate limiting, scheduled sends |
| **Send Email** | Email sending | Notifications, sequences |

---

## n8n Workflow Templates for PRINTMAXX

### Workflow 1: Social Media Auto-Post

**Trigger:** Schedule (daily or per-post times)
**Output:** Posts to X, LinkedIn, and other platforms

```
[Schedule Trigger: 9am, 12pm, 5pm]
    |
    v
[Google Sheets: Get next post from queue]
    |
    v
[IF: Post type?]
    |
    +-- text --> [X API: Post text]
    |              |
    |              v
    |            [LinkedIn API: Post text]
    |
    +-- media --> [HTTP: Download media]
                    |
                    v
                  [X API: Upload media + post]
                    |
                    v
                  [LinkedIn API: Upload + post]
    |
    v
[Google Sheets: Mark as posted]
    |
    v
[Slack: Notify "Posted: {content}"]
```

**n8n JSON (Import this):**
```json
{
  "name": "Social Media Auto-Post",
  "nodes": [
    {
      "parameters": {
        "rule": {
          "interval": [{"field": "hours", "hoursInterval": 4}]
        }
      },
      "name": "Schedule",
      "type": "n8n-nodes-base.scheduleTrigger"
    },
    {
      "parameters": {
        "sheetId": "YOUR_SHEET_ID",
        "range": "Queue!A:F",
        "options": {"valueRenderMode": "UNFORMATTED_VALUE"}
      },
      "name": "Get Posts",
      "type": "n8n-nodes-base.googleSheets"
    },
    {
      "parameters": {
        "jsCode": "// Get first unposted item\nconst items = $input.all();\nconst unposted = items.find(item => !item.json.posted);\nif (!unposted) return [];\nreturn [unposted];"
      },
      "name": "Filter Unposted",
      "type": "n8n-nodes-base.code"
    },
    {
      "parameters": {
        "conditions": {
          "string": [{"value1": "={{$json.type}}", "value2": "text"}]
        }
      },
      "name": "Is Text?",
      "type": "n8n-nodes-base.if"
    },
    {
      "parameters": {
        "resource": "tweet",
        "text": "={{$json.content}}"
      },
      "name": "Post to X",
      "type": "n8n-nodes-base.twitter"
    }
  ]
}
```

**Setup Steps:**
1. Import workflow JSON into n8n
2. Create Google Sheet with columns: id, content, type, media_url, posted, posted_at
3. Add X API credentials in n8n
4. Add LinkedIn API credentials (optional)
5. Set schedule trigger times
6. Test with single post
7. Activate workflow

### Workflow 2: Lead Capture Automation

**Trigger:** Webhook (form submission)
**Output:** CRM entry, email sequence, Slack notification

```
[Webhook: /lead-capture]
    |
    v
[Validate Email: Is valid format?]
    |
    +-- Invalid --> [Response: Error]
    |
    +-- Valid --> [Google Sheets: Add lead]
                    |
                    v
                  [Calculate Lead Score]
                    |
                    v
                  [IF: Score > 50?]
                    |
                    +-- YES --> [Send Welcome Email]
                    |             |
                    |             v
                    |           [Add to ConvertKit sequence]
                    |             |
                    |             v
                    |           [Slack: "Hot lead: {email}"]
                    |
                    +-- NO --> [Add to nurture sequence]
    |
    v
[Response: Success JSON]
```

**Lead Scoring Logic (Code Node):**
```javascript
const lead = $input.first().json;
let score = 0;

// Email quality
if (lead.email.endsWith('.edu')) score += 10;
if (lead.email.includes('gmail') || lead.email.includes('yahoo')) score += 5;
if (lead.email.match(/^[a-z]+\.[a-z]+@/)) score += 15; // firstname.lastname pattern

// Form fields
if (lead.company) score += 20;
if (lead.budget && lead.budget > 1000) score += 30;
if (lead.role && lead.role.includes('founder')) score += 25;

// Source
if (lead.source === 'product_hunt') score += 15;
if (lead.source === 'referral') score += 20;

return [{json: {...lead, lead_score: score}}];
```

**Setup Steps:**
1. Create webhook node, copy URL
2. Add webhook URL to your form (Typeform, Tally, custom)
3. Connect Google Sheets for storage
4. Set up email provider (ConvertKit, Mailchimp) credentials
5. Configure Slack webhook for notifications
6. Test with form submission

### Workflow 3: Content Repurposing Pipeline

**Trigger:** RSS feed (new blog post)
**Output:** X thread, LinkedIn post, newsletter draft

```
[RSS Feed Trigger: blog.example.com/feed]
    |
    v
[HTTP Request: Fetch full content]
    |
    v
[Claude API: Generate X thread]
    |
    v
[Claude API: Generate LinkedIn post]
    |
    v
[Claude API: Generate newsletter section]
    |
    v
[Google Sheets: Queue all outputs]
    |
    v
[Slack: "New content repurposed: {title}"]
```

**Claude API Call (HTTP Request Node):**
```json
{
  "method": "POST",
  "url": "https://api.anthropic.com/v1/messages",
  "headers": {
    "Content-Type": "application/json",
    "x-api-key": "{{$credentials.claudeApi.apiKey}}",
    "anthropic-version": "2023-06-01"
  },
  "body": {
    "model": "claude-3-haiku-20240307",
    "max_tokens": 1024,
    "messages": [{
      "role": "user",
      "content": "Convert this blog post to a Twitter thread (7-10 tweets). First tweet should be a hook under 280 chars. Each subsequent tweet should be under 280 chars. Last tweet should be a CTA. Use specific numbers, no fluff. Blog content:\n\n{{$node['Fetch Content'].json.content}}"
    }]
  }
}
```

**Response Parsing (Code Node):**
```javascript
const response = $input.first().json;
const threadText = response.content[0].text;

// Split into tweets
const tweets = threadText.split('\n\n').filter(t => t.trim());

return tweets.map((tweet, i) => ({
  json: {
    tweet_number: i + 1,
    content: tweet.replace(/^\d+[\.\)]\s*/, ''), // Remove numbering
    is_hook: i === 0,
    is_cta: i === tweets.length - 1
  }
}));
```

### Workflow 4: Research Automation (RSS + Reddit Monitoring)

**Trigger:** Schedule (every 6 hours)
**Output:** ALPHA_STAGING.csv entries

```
[Schedule: Every 6 hours]
    |
    v
[RSS: r/SaaS, r/EntrepreneurRideAlong, r/juststart]
    |
    v
[Filter: Top posts, >50 upvotes]
    |
    v
[Claude API: Extract actionable alpha]
    |
    v
[IF: Has specific numbers?]
    |
    +-- YES --> [Google Sheets: Add to ALPHA_STAGING]
    |
    +-- NO --> [Google Sheets: Add as ENGAGEMENT_BAIT]
    |
    v
[Dedupe: Check if URL already exists]
    |
    v
[Slack: "{count} new alpha entries added"]
```

**Reddit RSS URLs:**
```
https://www.reddit.com/r/SaaS/top/.rss?t=day
https://www.reddit.com/r/EntrepreneurRideAlong/top/.rss?t=day
https://www.reddit.com/r/juststart/top/.rss?t=day
https://www.reddit.com/r/indiehackers/top/.rss?t=day
https://www.reddit.com/r/coldemail/top/.rss?t=day
```

**Alpha Extraction Prompt:**
```
Analyze this Reddit post for actionable alpha. Extract:
1. Specific numbers (revenue, conversion rates, costs)
2. Tools mentioned
3. Replicable method (step-by-step if available)
4. Category: APP_FACTORY | CONTENT_FORMAT | OUTBOUND | GROWTH_HACK | TOOL_ALPHA | MONETIZATION

If no specific actionable information, respond with: ENGAGEMENT_BAIT_ONLY

Post title: {{title}}
Post content: {{content}}
Upvotes: {{score}}
Comments: {{num_comments}}
```

### Workflow 5: Data Sync (Sheets to LEDGER CSVs)

**Trigger:** Schedule (hourly) or Webhook
**Output:** Synced CSV files

```
[Schedule: Every hour]
    |
    v
[Google Sheets: Read all rows from ALPHA_STAGING]
    |
    v
[Code: Convert to CSV format]
    |
    v
[GitHub API: Update LEDGER/ALPHA_STAGING.csv]
    |
    v
[If: New approved entries?]
    |
    +-- YES --> [Trigger: Integration workflow]
    |
    v
[Slack: "LEDGER synced: {row_count} entries"]
```

**CSV Conversion (Code Node):**
```javascript
const rows = $input.all();
const headers = Object.keys(rows[0].json);

let csv = headers.join(',') + '\n';
for (const row of rows) {
  const values = headers.map(h => {
    const val = row.json[h] || '';
    // Escape commas and quotes
    if (val.includes(',') || val.includes('"')) {
      return `"${val.replace(/"/g, '""')}"`;
    }
    return val;
  });
  csv += values.join(',') + '\n';
}

return [{json: {csv_content: csv, row_count: rows.length}}];
```

---

## Make.com Scenarios for PRINTMAXX

### Scenario 1: Form to CRM + Email Sequence

```
[Typeform: New Response]
    |
    v
[Router]
    |
    +-- [Google Sheets: Add row]
    |
    +-- [ConvertKit: Add subscriber to sequence]
    |
    +-- [Slack: Send notification]
```

**Setup:**
1. Create new scenario in Make.com
2. Add Typeform trigger, select your form
3. Add Router module
4. Branch 1: Google Sheets -> Add Row
5. Branch 2: ConvertKit -> Add Subscriber
6. Branch 3: Slack -> Send Message
7. Map fields from Typeform to each destination
8. Enable scenario

### Scenario 2: New YouTube Video to Social

```
[YouTube: Watch New Videos in Channel]
    |
    v
[HTTP: Get video details]
    |
    v
[OpenAI: Generate announcement posts]
    |
    v
[Router]
    |
    +-- [Buffer: Create post (X)]
    |
    +-- [Buffer: Create post (LinkedIn)]
    |
    +-- [Google Sheets: Log to queue]
```

**Make.com Template:** Search "YouTube to Social Media" in Templates.

### Scenario 3: RSS to Content Queue

```
[RSS: Watch Feed]
    |
    v
[Iterator: Process each item]
    |
    v
[HTTP: OpenAI - Summarize]
    |
    v
[Google Sheets: Add to Content Queue]
```

**RSS Feeds to Monitor:**
```
https://feeds.transistor.fm/indie-hackers
https://www.reddit.com/r/SaaS/.rss
https://news.ycombinator.com/rss
https://medium.com/feed/tag/startup
```

### Make.com Limitations

**Operation Limits:**
- Free: 1,000 ops/mo (too low)
- Paid: 10,000 ops/mo (watch usage)
- Each module = 1 operation
- Complex scenarios eat ops fast

**Social Media:**
- Direct X posting: Limited
- Use Buffer integration instead
- LinkedIn: Works via API

**AI Integration:**
- OpenAI: Native module
- Claude: Via HTTP module (manual setup)

**Recommendation:** Start with Make.com free tier, but plan migration to n8n as volume grows.

---

## Integration Requirements

### OpenAI/Claude API Setup

**n8n - Claude API:**
```json
{
  "name": "Claude API",
  "type": "httpRequest",
  "parameters": {
    "url": "https://api.anthropic.com/v1/messages",
    "method": "POST",
    "headers": {
      "Content-Type": "application/json",
      "x-api-key": "{{$credentials.claudeApiKey}}",
      "anthropic-version": "2023-06-01"
    },
    "body": {
      "model": "claude-3-haiku-20240307",
      "max_tokens": 1024,
      "messages": [{"role": "user", "content": "{{$json.prompt}}"}]
    }
  }
}
```

**Make.com - Claude API (HTTP Module):**
1. Add HTTP module
2. URL: `https://api.anthropic.com/v1/messages`
3. Method: POST
4. Headers:
   - `x-api-key`: Your Claude API key
   - `anthropic-version`: 2023-06-01
   - `Content-Type`: application/json
5. Body type: JSON
6. Request content: Same as above

**Model Selection:**
| Model | Use Case | Cost (per 1M tokens) |
|-------|----------|---------------------|
| claude-3-haiku | High volume, simple tasks | $0.25/$1.25 |
| claude-3-sonnet | Quality content, code | $3/$15 |
| claude-3-opus | Complex reasoning, critical | $15/$75 |

### Twitter/X API Setup

**Required:** X API Developer account (Basic tier: Free, Pro: $100/mo)

**n8n:**
1. Go to Credentials -> New -> Twitter OAuth2 API
2. Enter Client ID and Client Secret from X Developer Portal
3. Complete OAuth flow

**Make.com:**
1. Add Twitter module
2. Click "Add" on Connection
3. Sign in with X account

**Posting Limits:**
- Basic tier: 1,500 posts/mo free
- Pro tier: 3,000 posts/mo
- Use Buffer for higher volume (works with any tier)

### Google Sheets API

**n8n:**
1. Create project in Google Cloud Console
2. Enable Sheets API
3. Create OAuth2 credentials
4. Add credentials in n8n
5. Authorize access to your Google account

**Make.com:**
1. Add Google Sheets module
2. Click "Create a connection"
3. Sign in with Google
4. Grant permissions

**Best Practices:**
- One sheet per data type (leads, content, alpha)
- Use headers in row 1
- Include timestamp columns
- Use data validation where possible

### Email Provider Setup

**ConvertKit (Recommended for creators):**
- n8n: Native integration
- Make.com: Native integration
- Setup: API key from Settings -> Advanced

**Mailchimp:**
- n8n: Native integration
- Make.com: Native integration
- Setup: API key from Account -> Extras -> API keys

**SendGrid (Transactional):**
- n8n: Native integration
- Make.com: Native integration
- Setup: API key from Settings -> API Keys

### Webhook Configuration

**n8n Webhook URL format:**
```
https://your-n8n-instance.com/webhook/[path]
https://your-n8n-instance.com/webhook-test/[path] (testing)
```

**Make.com Webhook URL:**
1. Add "Webhooks" module -> "Custom webhook"
2. Click module to get URL
3. URL format: `https://hook.make.com/[hash]`

**Security:**
- Add authentication header check
- Validate payload structure
- Rate limit incoming requests

---

## Cost Analysis

### Monthly Operating Costs

**Scenario A: Low Volume (< 5,000 ops/mo)**

| Platform | Cost | Notes |
|----------|------|-------|
| n8n on Railway | $5-10 | Occasional usage |
| Make.com Core | $9 | 10K ops included |
| **Winner** | Make.com | Easier setup justifies cost |

**Scenario B: Medium Volume (5,000-20,000 ops/mo)**

| Platform | Cost | Notes |
|----------|------|-------|
| n8n on Railway | $10-15 | Steady usage |
| Make.com Pro | $16-29 | May hit limits |
| **Winner** | n8n | Unlimited ops wins |

**Scenario C: High Volume (20,000+ ops/mo)**

| Platform | Cost | Notes |
|----------|------|-------|
| n8n self-hosted | $5-15 | VPS + occasional scaling |
| Make.com Teams | $29+ | May need multiple workspaces |
| **Winner** | n8n | Clear cost advantage |

### API Costs (Variable)

| API | Typical Monthly Cost | Volume |
|-----|---------------------|--------|
| Claude Haiku | $5-20 | 1,000-5,000 calls |
| OpenAI GPT-4 | $20-100 | 500-2,000 calls |
| X API Basic | Free | 1,500 posts |
| X API Pro | $100 | 3,000 posts |
| Google Sheets | Free | Included with account |

### Total Stack Costs

**Budget Stack ($20-40/mo):**
```
n8n on Railway: $10
Claude Haiku: $10-20
Buffer Free: $0
Google Sheets: $0
---
Total: $20-30/mo
```

**Standard Stack ($50-100/mo):**
```
n8n on VPS: $10
Claude Haiku: $20
Buffer Essentials: $6
ConvertKit Creator: $29
---
Total: $65/mo
```

**Scale Stack ($150-250/mo):**
```
n8n on Railway (scaled): $20
Claude mix (Haiku+Sonnet): $50
Buffer Team: $12
X API Pro: $100
ConvertKit Creator: $29
---
Total: $211/mo
```

---

## Maintenance Guide

### n8n Maintenance

**Weekly:**
- Check workflow execution logs
- Review failed executions
- Clear old execution data (Settings -> Execution Data)

**Monthly:**
- Update n8n to latest version
- Review and update credentials
- Backup workflows (Export All)
- Check Railway/VPS resource usage

**Updating n8n on Railway:**
1. Railway auto-updates from Docker image
2. Pin to specific version if needed in Dockerfile
3. Check release notes before major updates

**Updating n8n Docker:**
```bash
# Pull latest image
docker pull n8nio/n8n

# Restart container
docker-compose down
docker-compose up -d

# Verify version
docker exec -it n8n n8n --version
```

**Backup Strategy:**
```bash
# Export all workflows
curl -X GET "https://your-n8n.com/api/v1/workflows" \
  -H "X-N8N-API-KEY: your-api-key" > workflows-backup.json

# Backup credentials (encrypted)
# Stored in ~/.n8n/database.sqlite (Docker volume)
```

### Make.com Maintenance

**Weekly:**
- Review scenario history
- Check operation usage
- Fix any failed runs

**Monthly:**
- Review and optimize scenarios
- Remove unused scenarios
- Update connections if prompted

### Error Handling Best Practices

**n8n:**
```javascript
// Add error handling in Code nodes
try {
  const result = await processData();
  return [{json: {success: true, data: result}}];
} catch (error) {
  // Log error but don't fail workflow
  return [{json: {success: false, error: error.message}}];
}
```

**Rate Limit Handling:**
```javascript
// Add exponential backoff
const wait = (ms) => new Promise(resolve => setTimeout(resolve, ms));

let retries = 0;
while (retries < 3) {
  try {
    const response = await fetch(url);
    if (response.status === 429) {
      await wait(Math.pow(2, retries) * 1000);
      retries++;
      continue;
    }
    return response.json();
  } catch (error) {
    retries++;
  }
}
```

**Make.com:**
- Use built-in error handler modules
- Set up "Break" directives for rate limits
- Configure retry settings per module

---

## Quick Start Checklist

### n8n Setup (30 min)

- [ ] Create Railway account
- [ ] Deploy n8n template
- [ ] Set encryption key environment variable
- [ ] Access n8n at deployed URL
- [ ] Create first user account
- [ ] Add Google Sheets credentials
- [ ] Import first workflow template
- [ ] Test workflow execution
- [ ] Set up Slack webhook for notifications

### Make.com Setup (15 min)

- [ ] Create Make.com account
- [ ] Connect Google account
- [ ] Create first scenario from template
- [ ] Test with sample data
- [ ] Enable scenario

### PRINTMAXX Integration

- [ ] Create Google Sheet: AUTOMATION_QUEUE
- [ ] Columns: id, type, content, platform, status, created_at, posted_at
- [ ] Set up webhook endpoint for lead capture
- [ ] Connect to existing LEDGER sheets
- [ ] Test end-to-end flow

---

## Troubleshooting

### Common n8n Issues

**"Credential not found"**
- Re-authenticate the credential
- Check credential permissions
- Verify API key validity

**"Webhook not triggering"**
- Use /webhook/ URL (not /webhook-test/)
- Check workflow is active
- Verify webhook URL is correct

**"Workflow failing silently"**
- Enable error workflow in settings
- Check execution log
- Add explicit error handling nodes

**"Out of memory"**
- Increase Railway/Docker memory limit
- Process data in smaller batches
- Use streaming for large files

### Common Make.com Issues

**"Operation limit reached"**
- Upgrade plan
- Optimize scenarios to use fewer modules
- Split into multiple scenarios

**"Connection expired"**
- Reconnect the service
- Check OAuth token validity
- Review service API status

**"Scenario timing out"**
- Split long-running operations
- Use async processing
- Check for infinite loops

---

## Related Documents

- `OPS/MASTER_AUTOMATION_PLAN.md` - Full automation strategy
- `OPS/CONTENT_REPURPOSING_AUTOMATION.md` - Content pipeline specifics
- `OPS/TOOL_STACK.md` - Tool comparisons and alternatives
- `LEDGER/ALPHA_STAGING.csv` - Alpha data format
- `LEDGER/CONTENT_PIPELINE.csv` - Content queue structure

---

## Next Steps

1. **Today:** Set up n8n on Railway (30 min)
2. **This week:** Import and test social posting workflow
3. **Next week:** Build lead capture automation
4. **Month 1:** Add research automation
5. **Month 2:** Scale and optimize based on data

---

Last updated: 2026-01-25
